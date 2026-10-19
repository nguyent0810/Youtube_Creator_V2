"""Nhận lại video đã upload TAY qua Studio và ghi sổ (kênh upload="manual").

    python scripts/adopt_manual.py --channel MIM                    # quét 50 upload gần nhất
    python scripts/adopt_manual.py --channel MIM --slug <slug> --video-id <id>   # chỉ định tay
    [--limit N]   số upload gần nhất để quét (mặc định 50)

Khớp video với item bằng token yf-<slug> (tag, hoặc dòng cuối mô tả) -- không
bằng tiêu đề. Ghi upload_log (giãn nhịp + vòng phản hồi thấy video) và đánh dấu
item `published`. Chỉ ĐỌC kênh: 3 unit quota. Lý do: factory/manual.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, manual, store  # noqa: E402
from factory.channel import Channel  # noqa: E402


def _arg(name: str) -> str | None:
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def main() -> None:
    ch = channels.pick(default="MIM")
    if channels.upload_mode(ch) != "manual":
        sys.exit(f"kênh {ch} upload bằng API -- sổ đã tự ghi, không cần adopt")
    slug, vid = _arg("--slug"), _arg("--video-id")
    if bool(slug) != bool(vid):
        sys.exit("--slug và --video-id phải đi cùng nhau")
    with store.connect() as conn:
        chan = Channel.open(ch, conn)
        limit = int(_arg("--limit") or 50)
        if slug:
            manual.adopt_one(chan, conn, slug, vid, chan.api.list_uploads(limit))
            print(f"{ch}/{slug} -> {vid}")
            return
        rep = manual.adopt(chan, conn, chan.api.list_uploads(limit))
    for s, v in rep.adopted.items():
        print(f"  NHẬN   {s} -> https://youtu.be/{v}")
    for s, vs in rep.ambiguous.items():
        print(f"  NHIỀU VIDEO cùng token {s}: {vs} -- xoá bản thừa trong Studio, hoặc "
              f"--slug {s} --video-id <id>")
    for s, v in rep.unknown.items():
        print(f"  LẠ     {v} mang token {s} nhưng item không chờ ở chặng assembled")
    for s, why in rep.conflicts.items():
        print(f"  XUNG ĐỘT {s}: {why}")
    if not (rep.adopted or rep.ambiguous or rep.unknown or rep.conflicts):
        print("không có video mới nào mang token")


if __name__ == "__main__":
    main()
