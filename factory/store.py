"""Nơi Bundle sống, và trạng thái sản xuất của từng cái.

HAI KHO TÁCH RIÊNG, CÓ CHỦ ĐÍCH:

  bundles/<channel>/<slug>.json   -- thứ Claude sinh ra. BẤT BIẾN.
  state.sqlite                    -- thứ máy làm với nó. Thay đổi liên tục.

Vì sao không gộp: Bundle là đầu vào do con người/Claude tạo, cần đọc được
bằng mắt, review được trong git diff, sửa tay được khi cần. Trạng thái sản
xuất là dữ liệu máy sinh, thay đổi mỗi bước, và cần truy vấn ("còn slot nào
chưa render?"). Nhét chung vào một chỗ thì hoặc mất khả năng đọc, hoặc mất
khả năng truy vấn.

v1 gộp chung vào registry.json rải rác theo kênh, và trả giá đúng ở đây:
mỗi câu hỏi vận hành ("tuần sau còn thiếu mấy slot?") lại phải viết code mới
để quét file, còn việc ghi đồng thời thì phải dựng flock + backup rotation +
production-write guard -- khoảng 500 dòng chỉ để một file JSON không hỏng.
SQLite làm việc đó sẵn, đúng, và miễn phí.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from factory.bundle import Bundle, BundleInvalid

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_DIR = ROOT / "bundles"
DB_PATH = ROOT / "state.sqlite"

# Trạng thái sản xuất. Tiến MỘT CHIỀU, không quay lui: mỗi bước đều tốn máy
# (TTS, render, upload) nên phải biết chắc bước nào đã xong để chạy lại
# không làm lại từ đầu.
STAGES = ("pending", "spoken", "assembled", "published", "failed")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS item (
    id           TEXT PRIMARY KEY,
    channel      TEXT NOT NULL,
    kind         TEXT NOT NULL,
    slug         TEXT NOT NULL,
    publish_at   TEXT NOT NULL,
    stage        TEXT NOT NULL DEFAULT 'pending',
    wav_path     TEXT,
    timing_path  TEXT,
    video_path   TEXT,
    thumb_path   TEXT,
    video_id     TEXT,
    error        TEXT,
    attempts     INTEGER NOT NULL DEFAULT 0,
    updated_at   TEXT NOT NULL,
    UNIQUE (channel, slug)
);
CREATE INDEX IF NOT EXISTS idx_item_queue ON item (stage, publish_at);
CREATE INDEX IF NOT EXISTS idx_item_channel ON item (channel, publish_at);
-- Kênh YouTube mà credential của từng kênh trỏ tới (channels.verify_identity).
CREATE TABLE IF NOT EXISTS channel_identity (
    channel     TEXT PRIMARY KEY,
    channel_id  TEXT NOT NULL,
    title       TEXT,
    first_seen  TEXT NOT NULL
);
-- Khoá liên tiến trình: hai lần đăng chạy chồng nhau là upload trùng.
CREATE TABLE IF NOT EXISTS lock (
    name        TEXT PRIMARY KEY,
    owner       TEXT NOT NULL,
    acquired_at TEXT NOT NULL,
    expires_at  TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@contextmanager
def connect(db_path: Path | None = None):
    """Kết nối SQLite ở chế độ WAL.

    WAL cho phép một tiến trình đọc trong khi tiến trình khác ghi -- đúng
    tình huống hay gặp: xem tiến độ trong lúc batch đang chạy. Đây cũng là
    thứ thay thế toàn bộ flock của v1, và nó chạy trên Windows (fcntl thì
    không).

    isolation_level=None -> tự quản transaction tường minh, không để sqlite3
    âm thầm mở transaction rồi giữ khoá lâu hơn cần thiết."""
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, isolation_level=None, timeout=30.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.executescript(_SCHEMA)
        _migrate(conn)
        yield conn
    finally:
        conn.close()


# Cột thêm sau khi DB đã có dữ liệu thật (91 video trên kênh). CREATE TABLE
# IF NOT EXISTS không thêm cột vào bảng cũ, nên phải ALTER tay.
#   fail_stage  -- item hỏng ở chặng nào, để thử lại đúng chặng đó chứ không
#                  làm lại TTS + dựng cho một lỗi chỉ xảy ra lúc upload.
#   retry_after -- lỗi TẠM (hết quota): item giữ nguyên chặng, chỉ ẩn khỏi
#                  hàng đợi tới mốc này. Không tính là một lần hỏng.
#   script_sha  -- băm kịch bản lúc TTS/dựng. Kịch bản đổi sau đó thì video
#                  đã dựng là LỖI THỜI: không được đăng với metadata mới.
_MIGRATIONS = {"fail_stage": "TEXT", "retry_after": "TEXT", "script_sha": "TEXT"}


def script_sha(script: str) -> str:
    return hashlib.sha256(script.encode("utf-8")).hexdigest()[:16]


def _migrate(conn: sqlite3.Connection) -> None:
    have = {r[1] for r in conn.execute("PRAGMA table_info(item)")}
    for col, typ in _MIGRATIONS.items():
        if col not in have:
            conn.execute(f"ALTER TABLE item ADD COLUMN {col} {typ}")


# ─── Bundle trên đĩa ──────────────────────────────────────────────────────

def bundle_path(bundle: Bundle, base: Path | None = None) -> Path:
    return (base or BUNDLE_DIR) / bundle.channel / f"{bundle.slug}.json"


def save_bundle(bundle: Bundle, base: Path | None = None, overwrite: bool = False) -> Path:
    """Ghi Bundle ra đĩa. Validate TRƯỚC khi ghi -- không bao giờ để một
    bundle hỏng nằm trong hàng đợi chờ hỏng tiếp ở bước đắt tiền hơn.

    Bundle là BẤT BIẾN: đã có file khác nội dung thì KHÔNG ghi đè, trừ khi
    gọi rõ overwrite=True. Bản cũ ghi đè âm thầm -- sửa tiêu đề/kịch bản sau
    khi đã dựng là đăng VIDEO CŨ với METADATA MỚI (Bundle.id không băm
    kịch bản nên hàng đợi không biết có gì đổi)."""
    bundle.validate()
    path = bundle_path(bundle, base)
    if path.exists() and not overwrite:
        old = Bundle.from_json(path.read_text(encoding="utf-8"))
        if {**old.to_dict(), "created_at": ""} == {**bundle.to_dict(), "created_at": ""}:
            return path               # y hệt -> vô hại
        raise BundleInvalid(f"bundle đã tồn tại và khác nội dung: {path} -- bundle bất biến; "
                            "muốn thay thật thì dùng overwrite=True (và reset item để dựng lại)")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(bundle.to_json(), encoding="utf-8")
    tmp.replace(path)  # atomic trên cả POSIX lẫn Windows
    return path


def load_bundle(channel: str, slug: str, base: Path | None = None) -> Bundle:
    path = (base or BUNDLE_DIR) / channel / f"{slug}.json"
    if not path.exists():
        raise BundleInvalid(f"không thấy bundle: {path}")
    return Bundle.from_json(path.read_text(encoding="utf-8"))


def iter_bundles(channel: str | None = None, base: Path | None = None):
    """Duyệt mọi bundle trên đĩa. Bundle hỏng thì NÉM, không bỏ qua im lặng
    -- một file hỏng nằm im trong hàng đợi là thứ sẽ phát hiện ra vào lúc
    tệ nhất."""
    root = base or BUNDLE_DIR
    if not root.exists():
        return
    dirs = [root / channel] if channel else sorted(p for p in root.iterdir() if p.is_dir())
    for d in dirs:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.json")):
            yield Bundle.from_json(f.read_text(encoding="utf-8"))


# ─── Hàng đợi sản xuất ────────────────────────────────────────────────────

def enqueue(bundle: Bundle, conn: sqlite3.Connection) -> bool:
    """Đưa bundle vào hàng đợi. Trả True nếu là hàng mới.

    Đã có rồi thì KHÔNG đụng vào stage/đường dẫn đã ghi -- nạp lại cùng một
    bundle phải là thao tác vô hại, không được reset công việc đã làm xong.
    Đây chính là cái v1 phải dựng 'production-write guard' để đạt được."""
    bundle.validate()
    try:
        cur = conn.execute(
            "INSERT INTO item (id, channel, kind, slug, publish_at, stage, updated_at) "
            "VALUES (?, ?, ?, ?, ?, 'pending', ?) ON CONFLICT(id) DO NOTHING",
            (bundle.id, bundle.channel, bundle.kind, bundle.slug, bundle.publish_at, _now()),
        )
    except sqlite3.IntegrityError as exc:
        raise BundleInvalid(f"{bundle.channel}/{bundle.slug}: đã có item cùng slug nhưng khác kind "
                            "-- đổi kind là một content item khác, phải đổi slug") from exc
    if cur.rowcount > 0:
        return True
    # Đã có: KHÔNG đụng stage/đường dẫn. Riêng publish_at thì đồng bộ theo file
    # khi item CHƯA lên kênh -- bản cũ giữ giờ cũ trong DB trong khi upload lại
    # đọc giờ mới từ file, và mọi script soát lịch đọc nhầm giờ.
    conn.execute("UPDATE item SET publish_at = ?, updated_at = ? "
                 "WHERE id = ? AND video_id IS NULL AND publish_at != ?",
                 (bundle.publish_at, _now(), bundle.id, bundle.publish_at))
    return False


def mark(conn: sqlite3.Connection, item_id: str, stage: str, **fields) -> None:
    """Cập nhật trạng thái + đường dẫn kết quả trong MỘT câu lệnh."""
    if stage not in STAGES:
        raise ValueError(f"stage lạ: {stage!r} (hợp lệ: {STAGES})")
    allowed = {"wav_path", "timing_path", "video_path", "thumb_path", "video_id", "error", "script_sha"}
    bad = set(fields) - allowed
    if bad:
        raise ValueError(f"trường lạ: {sorted(bad)}")
    cols = ", ".join(f"{k} = ?" for k in fields)
    # Tiến được một chặng thì mọi lỗi tạm trước đó hết ý nghĩa.
    sql = (f"UPDATE item SET stage = ?, updated_at = ?, retry_after = NULL"
           f"{', ' + cols if cols else ''} WHERE id = ?")
    cur = conn.execute(sql, (stage, _now(), *fields.values(), item_id))
    if cur.rowcount == 0:
        # Lỗi thật đã gặp: id tính lại từ bundle đã đổi kind -> cập nhật 0 dòng,
        # video đã upload mà store không biết.
        raise KeyError(f"không có item {item_id} trong store -- không ghi được trạng thái {stage!r}")


def bump_attempt(conn: sqlite3.Connection, item_id: str, error: str) -> int:
    """Ghi nhận một lần thử hỏng. Trả về tổng số lần đã thử.

    Đếm ở tầng dữ liệu chứ không phải trong bộ nhớ tiến trình: batch có thể
    bị giết giữa chừng, và một item hỏng vĩnh viễn không được phép thử lại
    vô hạn qua nhiều lần chạy khác nhau."""
    conn.execute(
        "UPDATE item SET attempts = attempts + 1, error = ?, "
        "fail_stage = CASE WHEN stage = 'failed' THEN fail_stage ELSE stage END, "
        "stage = 'failed', updated_at = ? WHERE id = ?",
        (error[:2000], _now(), item_id),
    )
    row = conn.execute("SELECT attempts FROM item WHERE id = ?", (item_id,)).fetchone()
    return row["attempts"] if row else 0


def reject(conn: sqlite3.Connection, item_id: str, error: str) -> None:
    """Loại hẳn một item vì lỗi NỘI DUNG (vd toàn vẹn văn bản): thử lại vô ích,
    nên đặt attempts vượt ngưỡng để requeue_failed không đưa nó về hàng đợi."""
    conn.execute(
        "UPDATE item SET attempts = 99, error = ?, "
        "fail_stage = CASE WHEN stage = 'failed' THEN fail_stage ELSE stage END, "
        "stage = 'failed', updated_at = ? WHERE id = ?",
        (error[:2000], _now(), item_id),
    )


def defer(conn: sqlite3.Connection, item_id: str, error: str, retry_after: str) -> None:
    """Lỗi TẠM THỜI: giữ nguyên chặng, ẩn khỏi hàng đợi tới `retry_after`.

    Vì sao tách khỏi bump_attempt: tháng 12 video thứ 31 dính HTTP 429 hết
    hạn mức upload. Video không có gì sai -- chỉ là đến lượt quá muộn. Nếu
    tính đó là một lần HỎNG thì ba ngày quota đầy liên tiếp là item bị loại
    vĩnh viễn, trong khi nó hoàn toàn hợp lệ."""
    conn.execute("UPDATE item SET error = ?, retry_after = ?, updated_at = ? WHERE id = ?",
                 (error[:2000], retry_after, _now(), item_id))


def requeue_failed(conn: sqlite3.Connection, max_attempts: int = 3,
                   channel: str | None = None) -> list[str]:
    """Đưa item hỏng (chưa quá max_attempts) về lại ĐÚNG chặng đã hỏng.

    Item cũ chưa có fail_stage thì suy từ kết quả đã có: có video thì hỏng
    lúc đăng, có wav thì hỏng lúc dựng, không có gì thì hỏng lúc TTS."""
    rows = list(conn.execute(
        "SELECT id, slug, fail_stage, wav_path, video_path FROM item "
        "WHERE stage = 'failed' AND attempts < ?" + (" AND channel = ?" if channel else ""),
        (max_attempts, channel) if channel else (max_attempts,)))
    for r in rows:
        back = r["fail_stage"] or ("assembled" if r["video_path"]
                                   else "spoken" if r["wav_path"] else "pending")
        conn.execute("UPDATE item SET stage = ?, fail_stage = NULL, updated_at = ? "
                     "WHERE id = ?", (back, _now(), r["id"]))
    return [r["slug"] for r in rows]


def next_batch(conn: sqlite3.Connection, stage: str, limit: int = 10,
               channel: str | None = None, max_attempts: int = 3) -> list[sqlite3.Row]:
    """Lấy lô việc kế tiếp, cũ nhất trước (theo publish_at).

    Bỏ qua item đã thử quá max_attempts -- một kịch bản hỏng không được
    phép chặn hàng đợi mãi mãi. Sắp theo publish_at để việc sắp tới hạn
    được làm trước, không phải theo thứ tự ngẫu nhiên của bảng."""
    sql = ("SELECT * FROM item WHERE stage = ? AND attempts < ?"
           " AND (retry_after IS NULL OR retry_after <= ?)"
           + (" AND channel = ?" if channel else "")
           + " ORDER BY publish_at ASC LIMIT ?")
    args = [stage, max_attempts, _now()] + ([channel] if channel else []) + [limit]
    return list(conn.execute(sql, args))


def deferred(conn: sqlite3.Connection, channel: str | None = None) -> list[sqlite3.Row]:
    """Item đang chờ lỗi tạm hết hạn (vd. quota reset)."""
    sql = ("SELECT * FROM item WHERE retry_after IS NOT NULL AND retry_after > ?"
           + (" AND channel = ?" if channel else "") + " ORDER BY publish_at")
    return list(conn.execute(sql, [_now()] + ([channel] if channel else [])))


def summary(conn: sqlite3.Connection) -> dict[str, dict[str, int]]:
    """Đếm theo kênh và trạng thái -- câu hỏi vận hành hay hỏi nhất.

    Ở v1 đây là đoạn code phải viết mới mỗi lần muốn biết; ở đây là một câu
    SELECT."""
    out: dict[str, dict[str, int]] = {}
    for row in conn.execute("SELECT channel, stage, COUNT(*) AS n FROM item GROUP BY channel, stage"):
        out.setdefault(row["channel"], {})[row["stage"]] = row["n"]
    return out


def sync_from_disk(conn: sqlite3.Connection, base: Path | None = None,
                   channel: str | None = None) -> tuple[int, int]:
    """Nạp mọi bundle trên đĩa vào hàng đợi. Trả (số mới, tổng số thấy).

    Đây là cầu nối giữa hai pha: Claude ghi file JSON trong chat, gọi hàm
    này một lần, và pha sản xuất có việc để làm. Chạy lại bao nhiêu lần
    cũng vô hại."""
    added = total = 0
    for b in iter_bundles(channel=channel, base=base):
        total += 1
        if enqueue(b, conn):
            added += 1
    return added, total


# ─── Khoá liên tiến trình ─────────────────────────────────────────────────

class LockBusy(RuntimeError):
    pass


@contextmanager
def locked(conn: sqlite3.Connection, name: str, ttl_minutes: int = 180):
    """Giữ khoá `name` trong lúc chạy khối lệnh. Đã có người giữ thì ném LockBusy.

    Vì sao cần: `run_pipeline resume` chạy định kỳ chồng lên một lần chạy tay,
    hay drip/upload_one chồng lên publish_batch, sẽ cùng lấy MỘT hàng đợi và
    upload trùng video. Khoá có hạn (ttl) để tiến trình chết giữa chừng không
    khoá vĩnh viễn."""
    owner = f"{os.getpid()}-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)
    conn.execute("DELETE FROM lock WHERE name = ? AND expires_at <= ?", (name, _now()))
    cur = conn.execute(
        "INSERT INTO lock (name, owner, acquired_at, expires_at) VALUES (?, ?, ?, ?) "
        "ON CONFLICT(name) DO NOTHING",
        (name, owner, _now(), (now + timedelta(minutes=ttl_minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")))
    if cur.rowcount == 0:
        row = conn.execute("SELECT owner, acquired_at, expires_at FROM lock WHERE name = ?", (name,)).fetchone()
        raise LockBusy(f"đang có tiến trình khác giữ khoá {name!r} (từ {row['acquired_at']}, hết hạn "
                       f"{row['expires_at']}). Chờ nó xong; nếu chắc chắn nó đã chết thì xoá dòng "
                       f"{name!r} trong bảng lock.")
    try:
        yield owner
    finally:
        conn.execute("DELETE FROM lock WHERE name = ? AND owner = ?", (name, owner))
