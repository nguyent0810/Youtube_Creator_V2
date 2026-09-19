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
from datetime import datetime, timezone
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
        yield conn
    finally:
        conn.close()


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
        "INSERT INTO item (id, channel, kind, slug, publish_at, stage, updated_at) "
        "VALUES (?, ?, ?, ?, ?, 'pending', ?) ON CONFLICT(id) DO NOTHING",
        (bundle.id, bundle.channel, bundle.kind, bundle.slug, bundle.publish_at, _now()),
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
    sql = f"UPDATE item SET stage = ?, updated_at = ?{', ' + cols if cols else ''} WHERE id = ?"
    conn.execute(sql, (stage, _now(), *fields.values(), item_id))


def bump_attempt(conn: sqlite3.Connection, item_id: str, error: str) -> int:
    """Ghi nhận một lần thử hỏng. Trả về tổng số lần đã thử.

    Đếm ở tầng dữ liệu chứ không phải trong bộ nhớ tiến trình: batch có thể
    bị giết giữa chừng, và một item hỏng vĩnh viễn không được phép thử lại
    vô hạn qua nhiều lần chạy khác nhau."""
    conn.execute(
        "UPDATE item SET attempts = attempts + 1, error = ?, stage = 'failed', updated_at = ? WHERE id = ?",
        (error[:2000], _now(), item_id),
    )
    row = conn.execute("SELECT attempts FROM item WHERE id = ?", (item_id,)).fetchone()
    return row["attempts"] if row else 0


def next_batch(conn: sqlite3.Connection, stage: str, limit: int = 10,
               channel: str | None = None, max_attempts: int = 3) -> list[sqlite3.Row]:
    """Lấy lô việc kế tiếp, cũ nhất trước (theo publish_at).

    Bỏ qua item đã thử quá max_attempts -- một kịch bản hỏng không được
    phép chặn hàng đợi mãi mãi. Sắp theo publish_at để việc sắp tới hạn
    được làm trước, không phải theo thứ tự ngẫu nhiên của bảng."""
    sql = ("SELECT * FROM item WHERE stage = ? AND attempts < ?"
           + (" AND channel = ?" if channel else "")
           + " ORDER BY publish_at ASC LIMIT ?")
    args = [stage, max_attempts] + ([channel] if channel else []) + [limit]
    return list(conn.execute(sql, args))


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
