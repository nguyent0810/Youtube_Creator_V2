"""Vòng phản hồi hằng tuần: đo -> bảng điểm -> brief cho pha sinh trong chat.

    python scripts/feedback_loop.py                 # cả 3 kênh
    python scripts/feedback_loop.py --channel FS
    python scripts/feedback_loop.py --no-collect    # chỉ dựng lại brief từ số đã đo

Chỉ ĐỌC YouTube. Ghi: bảng video_metrics trong state.sqlite và
data/briefs/<KÊNH>.md. Brief là thứ Claude đọc trước khi viết bundle/pack
mới (pha sinh); pha sản xuất vẫn không cần LLM. Thứ duy nhất vòng này tự
đổi trên kênh là giờ đăng, qua thí nghiệm xoay giờ (factory/rotation.py)
mà make_pillars_day áp khi sinh bài -- không phải ở đây.

Thiết kế: docs/audit/2026-10-05-feedback-loop-design.md.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, scoreboard, store  # noqa: E402

BRIEFS = ROOT / "data" / "briefs"


def run(code: str, conn, api, *, now: datetime, out_dir: Path = BRIEFS,
        collect: bool = True) -> tuple[Path, dict]:
    summary = (scoreboard.collect(conn, code, api, now=now) if collect
               else {"stored": 0, "open": 0, "not_live": 0, "gone": 0, "failed": 0, "frontier": None})
    b = scoreboard.board(conn, code, frontier=summary["frontier"])
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{code}.md"
    path.write_text(scoreboard.render_brief(b), encoding="utf-8")
    return path, summary


if __name__ == "__main__":
    from factory.analytics import HttpAnalytics
    chs = [channels.pick()] if "--channel" in sys.argv else list(channels.CHANNELS)
    now = datetime.now(timezone.utc)
    for ch in chs:
        with store.connect() as conn:
            path, s = run(ch, conn, HttpAnalytics.open(ch), now=now, collect="--no-collect" not in sys.argv)
        print(f"{ch}: đo thêm {s['stored']} video · {s['open']} chờ đóng cửa sổ · "
              f"{s['not_live']} chưa lên sóng · {s['gone']} đã xoá · {s['failed']} lỗi (thử lại lần sau) · "
              f"số liệu tới {s['frontier']} -> {path.relative_to(ROOT)}")
