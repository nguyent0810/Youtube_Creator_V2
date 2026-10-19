"""Ẩn (chuyển private) mọi video đang công khai / hẹn giờ của một kênh -- khi đổi hướng kênh.

    python scripts/hide_videos.py --channel MIM                          # chạy khô: chỉ liệt kê
    python scripts/hide_videos.py --channel MIM --apply --confirm MIM    # ẩn thật

`--confirm` phải gõ lại đúng mã kênh: một lệnh --apply nhầm kênh là ẩn sạch một kênh
đang chạy.

ẨN chứ không xoá: đảo ngược được, số liệu Analytics vẫn giữ. Trạng thái CŨ của từng
video được ghi vào output/hidden/<KÊNH>-<ngày>.json TRƯỚC khi đổi, để khôi phục được.
Mỗi video tốn 50 đơn vị quota (videos.update); hết quota thì dừng, chạy lại là làm nốt.
Đi qua factory/channel.py (Channel.hide): merge mọi trường status, không đụng snippet.

Bối cảnh: docs/channels/mind-in-the-machine/2026-10-05-analysis.md.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from factory import channels, publish, store  # noqa: E402
from factory.channel import Channel  # noqa: E402


def visible_videos(chan: Channel) -> list[dict]:
    """Mọi video của kênh mà người xem có thể thấy hoặc sẽ thấy (public,
    unlisted, private có hẹn giờ)."""
    http = chan.api
    up = http.get_json(f"{publish.API}/channels?part=contentDetails&mine=true")["items"][0][
        "contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while True:
        q = f"part=contentDetails&maxResults=50&playlistId={up}" + (f"&pageToken={page}" if page else "")
        d = http.get_json(f"{publish.API}/playlistItems?{q}")
        ids += [it["contentDetails"]["videoId"] for it in d.get("items", [])]
        page = d.get("nextPageToken")
        if not page:
            break
    out = []
    for i in range(0, len(ids), 50):
        d = http.get_json(f"{publish.API}/videos?part=snippet,status&id={','.join(ids[i:i + 50])}")
        for v in d.get("items", []):
            st = v["status"]
            if st["privacyStatus"] != "private" or st.get("publishAt"):
                out.append({"id": v["id"], "title": v["snippet"]["title"],
                            "published": v["snippet"]["publishedAt"], "status": st})
    return sorted(out, key=lambda v: v["published"])


def main() -> None:
    ch = channels.pick()
    apply = "--apply" in sys.argv
    if apply and (sys.argv[sys.argv.index("--confirm") + 1] if "--confirm" in sys.argv else None) != ch:
        sys.exit(f"Thiếu --confirm {ch}: gõ lại đúng mã kênh để xác nhận ẩn MỌI video công khai của {ch}.")
    with store.connect() as conn:
        chan = Channel.open(ch, conn)
        vids = visible_videos(chan)
        print(f"{channels.CHANNELS[ch]['ten']} ({ch}): {len(vids)} video đang hiển thị / hẹn giờ")
        for i, v in enumerate(vids, 1):
            print(f"  {i:2d}. {v['published'][:10]} [{v['status']['privacyStatus']}] {v['id']}  {v['title'][:70]}")
        if not apply:
            print("\nCHẠY KHÔ -- thêm --apply để ẩn thật.")
            return
        rec = ROOT / "output" / "hidden" / f"{ch}-{datetime.now(timezone.utc):%Y%m%dT%H%M%S}.json"
        rec.parent.mkdir(parents=True, exist_ok=True)
        if rec.exists():          # không bao giờ ghi đè bản lưu trạng thái cũ
            sys.exit(f"{rec} đã tồn tại -- chạy lại sau một giây.")
        rec.write_text(json.dumps({"channel": ch, "videos": vids}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nđã ghi trạng thái cũ -> {rec.relative_to(ROOT)}")
        done = 0
        for v in vids:
            try:
                chan.hide(v["id"])
            except publish.QuotaExceeded:
                print(f"HẾT QUOTA sau {done} video -- chạy lại sau giờ reset để làm nốt.")
                break
            done += 1
            print(f"  ẩn {done}/{len(vids)}: {v['title'][:60]}", flush=True)
        left = visible_videos(chan)
        print(f"\nXONG: đã ẩn {done}. Còn hiển thị trên kênh: {len(left)}")


if __name__ == "__main__":
    main()
