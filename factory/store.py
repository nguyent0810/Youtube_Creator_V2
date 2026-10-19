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

import json
import sqlite3
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
#   engine      -- cách dựng (bundle.ENGINES). Lần đầu thêm cột: suy từ slug cho
#                  hàng cũ (cl-hs- = hồ sơ S-tier, long- = video dài).
#   claimed_by / lease_until -- worker đang giữ hàng (TTS / dựng); lease hết hạn
#                  thì worker khác được nhận. Thay LOCK/FAILED/STOP2 của queue2.sh.
_MIGRATIONS = {"fail_stage": "TEXT", "retry_after": "TEXT", "engine": "TEXT",
               "claimed_by": "TEXT", "lease_until": "TEXT"}

# Một item short qua TTS hoặc dựng xong dưới vài phút; 30 phút là thừa. Worker
# chết giữa chừng thì sau 30 phút worker khác nhận lại.
CLAIM_LEASE = timedelta(minutes=30)

_RELEASE = "claimed_by = NULL, lease_until = NULL"

# Bundle cũ (trước 05/10/2026) không có `render`: suy engine từ slug -- cùng luật
# cho hàng cũ (migration) lẫn bundle cũ nạp lại (enqueue/sync_from_disk). 91 hồ
# sơ cl-hs- trên đĩa thuộc loại này; coi là assemble thì run_batch đi tìm B-roll
# Pexels cho từ khoá "hyperframes-casefile".
_LEGACY = (("cl-hs-", "casefile"), ("long-", "casewide"))
_LEGACY_ENGINE = ("CASE " + " ".join(f"WHEN slug LIKE '{p}%' THEN '{e}'" for p, e in _LEGACY)
                  + " ELSE 'assemble' END")


def _engine(bundle: Bundle) -> str:
    if bundle.render:
        return bundle.engine
    return next((e for p, e in _LEGACY if bundle.slug.startswith(p)), "assemble")


def _migrate(conn: sqlite3.Connection) -> None:
    have = {r[1] for r in conn.execute("PRAGMA table_info(item)")}
    for col, typ in _MIGRATIONS.items():
        if col not in have:
            conn.execute(f"ALTER TABLE item ADD COLUMN {col} {typ}")
            if col == "engine":
                conn.execute(f"UPDATE item SET engine = {_LEGACY_ENGINE}")


# ─── Bundle trên đĩa ──────────────────────────────────────────────────────

def bundle_path(bundle: Bundle, base: Path | None = None) -> Path:
    return (base or BUNDLE_DIR) / bundle.channel / f"{bundle.slug}.json"


def save_bundle(bundle: Bundle, base: Path | None = None) -> Path:
    """Ghi Bundle ra đĩa. Validate TRƯỚC khi ghi -- không bao giờ để một
    bundle hỏng nằm trong hàng đợi chờ hỏng tiếp ở bước đắt tiền hơn."""
    bundle.validate()
    path = bundle_path(bundle, base)
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
    cur = conn.execute(
        "INSERT INTO item (id, channel, kind, slug, publish_at, stage, engine, updated_at) "
        "VALUES (?, ?, ?, ?, ?, 'pending', ?, ?) ON CONFLICT(id) DO NOTHING",
        (bundle.id, bundle.channel, bundle.kind, bundle.slug, bundle.publish_at, _engine(bundle), _now()),
    )
    return cur.rowcount > 0


def mark(conn: sqlite3.Connection, item_id: str, stage: str, **fields) -> None:
    """Cập nhật trạng thái + đường dẫn kết quả trong MỘT câu lệnh."""
    if stage not in STAGES:
        raise ValueError(f"stage lạ: {stage!r} (hợp lệ: {STAGES})")
    allowed = {"wav_path", "timing_path", "video_path", "thumb_path", "video_id", "error"}
    bad = set(fields) - allowed
    if bad:
        raise ValueError(f"trường lạ: {sorted(bad)}")
    cols = ", ".join(f"{k} = ?" for k in fields)
    # Tiến được một chặng thì mọi lỗi tạm trước đó hết ý nghĩa.
    sql = (f"UPDATE item SET stage = ?, updated_at = ?, retry_after = NULL, {_RELEASE}"
           f"{', ' + cols if cols else ''} WHERE id = ?")
    conn.execute(sql, (stage, _now(), *fields.values(), item_id))


def bump_attempt(conn: sqlite3.Connection, item_id: str, error: str) -> int:
    """Ghi nhận một lần thử hỏng. Trả về tổng số lần đã thử.

    Đếm ở tầng dữ liệu chứ không phải trong bộ nhớ tiến trình: batch có thể
    bị giết giữa chừng, và một item hỏng vĩnh viễn không được phép thử lại
    vô hạn qua nhiều lần chạy khác nhau."""
    conn.execute(
        "UPDATE item SET attempts = attempts + 1, error = ?, "
        "fail_stage = CASE WHEN stage = 'failed' THEN fail_stage ELSE stage END, "
        f"stage = 'failed', updated_at = ?, {_RELEASE} WHERE id = ?",
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
        f"stage = 'failed', updated_at = ?, {_RELEASE} WHERE id = ?",
        (error[:2000], _now(), item_id),
    )


def defer(conn: sqlite3.Connection, item_id: str, error: str, retry_after: str) -> None:
    """Lỗi TẠM THỜI: giữ nguyên chặng, ẩn khỏi hàng đợi tới `retry_after`.

    Vì sao tách khỏi bump_attempt: tháng 12 video thứ 31 dính HTTP 429 hết
    hạn mức upload. Video không có gì sai -- chỉ là đến lượt quá muộn. Nếu
    tính đó là một lần HỎNG thì ba ngày quota đầy liên tiếp là item bị loại
    vĩnh viễn, trong khi nó hoàn toàn hợp lệ."""
    conn.execute(f"UPDATE item SET error = ?, retry_after = ?, updated_at = ?, {_RELEASE} WHERE id = ?",
                 (error[:2000], retry_after, _now(), item_id))


def requeue_failed(conn: sqlite3.Connection, max_attempts: int = 3) -> list[str]:
    """Đưa item hỏng (chưa quá max_attempts) về lại ĐÚNG chặng đã hỏng.

    Item cũ chưa có fail_stage thì suy từ kết quả đã có: có video thì hỏng
    lúc đăng, có wav thì hỏng lúc dựng, không có gì thì hỏng lúc TTS."""
    rows = list(conn.execute(
        "SELECT id, slug, fail_stage, wav_path, video_path FROM item "
        "WHERE stage = 'failed' AND attempts < ?", (max_attempts,)))
    for r in rows:
        back = r["fail_stage"] or ("assembled" if r["video_path"]
                                   else "spoken" if r["wav_path"] else "pending")
        conn.execute(f"UPDATE item SET stage = ?, fail_stage = NULL, updated_at = ?, {_RELEASE} "
                     "WHERE id = ?", (back, _now(), r["id"]))
    return [r["slug"] for r in rows]


def next_batch(conn: sqlite3.Connection, stage: str, limit: int = 10,
               channel: str | None = None, max_attempts: int = 3,
               engine: str | None = None) -> list[sqlite3.Row]:
    """Lấy lô việc kế tiếp, cũ nhất trước (theo publish_at).

    Bỏ qua item đã thử quá max_attempts -- một kịch bản hỏng không được
    phép chặn hàng đợi mãi mãi. Sắp theo publish_at để việc sắp tới hạn
    được làm trước, không phải theo thứ tự ngẫu nhiên của bảng."""
    where, args = _ready(stage, max_attempts, _now(), channel, engine)
    return list(conn.execute(f"SELECT * FROM item WHERE {where} ORDER BY publish_at ASC LIMIT ?", args + [limit]))


def _ready(stage: str, max_attempts: int, now: str, channel: str | None,
           engine: str | None) -> tuple[str, list]:
    """Điều kiện "hàng sẵn sàng làm": đúng chặng, chưa quá số lần thử, hết hoãn,
    không ai đang giữ. engine=None = mọi engine (publish_batch đăng cả S-tier)."""
    where = ("stage = ? AND attempts < ? AND (retry_after IS NULL OR retry_after <= ?)"
             " AND (lease_until IS NULL OR lease_until <= ?)")
    args = [stage, max_attempts, now, now]
    if channel:
        where += " AND channel = ?"
        args.append(channel)
    if engine:
        where += " AND COALESCE(engine, 'assemble') = ?"
        args.append(engine)
    return where, args


def claim(conn: sqlite3.Connection, stage: str, worker: str, *, channel: str | None = None,
          engine: str | None = None, max_attempts: int = 3, now: datetime | None = None) -> sqlite3.Row | None:
    """Giành MỘT hàng sẵn sàng ở `stage` cho `worker` trong một transaction ghi.

    Trước đây next_batch không giành gì: hai worker TTS cùng nhận một lô, làm hai
    lần, lần ghi sau thắng. Mọi cách kết thúc hàng (mark, bump_attempt, reject,
    defer, requeue_failed) đều thả lease."""
    t = now or datetime.now(timezone.utc)
    stamp = t.strftime("%Y-%m-%dT%H:%M:%SZ")
    until = (t + CLAIM_LEASE).strftime("%Y-%m-%dT%H:%M:%SZ")
    where, args = _ready(stage, max_attempts, stamp, channel, engine)
    conn.execute("BEGIN IMMEDIATE")
    try:
        row = conn.execute(f"SELECT id FROM item WHERE {where} ORDER BY publish_at ASC LIMIT 1", args).fetchone()
        if row is not None:
            conn.execute("UPDATE item SET claimed_by = ?, lease_until = ? WHERE id = ?", (worker, until, row["id"]))
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    conn.execute("COMMIT")
    return None if row is None else conn.execute("SELECT * FROM item WHERE id = ?", (row["id"],)).fetchone()


def release(conn: sqlite3.Connection, item_id: str, worker: str) -> None:
    """Thả hàng mà không đổi chặng (worker dừng giữa chừng một cách có kiểm soát)."""
    conn.execute(f"UPDATE item SET {_RELEASE} WHERE id = ? AND claimed_by = ?", (item_id, worker))


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
