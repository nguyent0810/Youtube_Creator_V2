"""Xuất gói upload TAY cho kênh upload="manual" (vd MIM): video + meta.txt để dán vào Studio.

    python scripts/export_manual.py --channel MIM

Ghi output/manual/<CH>/<slug>/{<slug>.mp4, meta.txt, thumbnail.*} cho mọi item
`assembled` của kênh. Upload xong trong Studio thì chạy scripts/adopt_manual.py
để máy ghi sổ. Quy trình + lý do: factory/manual.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, manual, store  # noqa: E402

OUT = ROOT / "output" / "manual"


def main() -> None:
    ch = channels.pick(default="MIM")
    if channels.upload_mode(ch) != "manual":
        sys.exit(f"kênh {ch} upload bằng API (publish_batch.py), không xuất gói tay")
    with store.connect() as conn:
        got = manual.export(conn, ch, OUT)
    if not got:
        print(f"{ch}: không có item assembled nào chờ upload")
    for d in got:
        print(f"  {d}")
    if got:
        print(f"\n{len(got)} gói. Upload từng gói qua Studio (Private + hẹn giờ theo meta.txt), "
              f"rồi: python scripts/adopt_manual.py --channel {ch}")


if __name__ == "__main__":
    main()
