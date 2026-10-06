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
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, demand, scoreboard, store  # noqa: E402

BRIEFS = ROOT / "data" / "briefs"          # gitignore: brief chứa từ khoá tìm kiếm của kênh
DEMAND = ROOT / "data" / "demand"          # <KÊNH>.json = danh sách chủ đề theo dõi (commit)


def run(code: str, conn, api, *, now: datetime, out_dir: Path = BRIEFS,
        collect: bool = True, wiki=None, demand_dir: Path = DEMAND, sleep=time.sleep) -> tuple[Path, dict]:
    summary = (scoreboard.collect(conn, code, api, now=now) if collect
               else {"stored": 0, "open": 0, "not_live": 0, "gone": 0, "failed": 0, "frontier": None})
    b = scoreboard.board(conn, code, frontier=summary["frontier"])
    summary["frontier"] = b.frontier          # --no-collect: mốc đã lưu từ lần đo trước
    md = scoreboard.render_brief(b)
    if wiki is not None:
        # Bước 3: nhu cầu. Chạy cả khi --no-collect (chỉ bỏ phần đo video_metrics).
        md += demand.render_demand(
            conn, code, api, wiki, frontier=b.frontier, today=now.date(),
            watchlist=demand.load_watchlist(demand_dir / f"{code}.json"),
            studio_file=demand_dir / f"{code}-studio.md", sleep=sleep)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{code}.md"
    path.write_text(md, encoding="utf-8")
    return path, summary


if __name__ == "__main__":
    from factory.analytics import HttpAnalytics
    chs = [channels.pick()] if "--channel" in sys.argv else channels.available()
    now = datetime.now(timezone.utc)
    for ch in chs:
        with store.connect() as conn:
            path, s = run(ch, conn, HttpAnalytics.open(ch), now=now, collect="--no-collect" not in sys.argv,
                          wiki=demand.HttpPageviews())
        print(f"{ch}: đo thêm {s['stored']} video · {s['open']} chờ đóng cửa sổ · "
              f"{s['not_live']} chưa lên sóng · {s['gone']} đã xoá · {s['failed']} lỗi (thử lại lần sau) · "
              f"số liệu tới {s['frontier']} -> {path.relative_to(ROOT)}")
