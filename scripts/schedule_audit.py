"""Soát lịch đăng: tránh công khai TRÙNG. Chỉ đọc YouTube, không sửa gì.

    python scripts/schedule_audit.py              # cả 3 kênh
    python scripts/schedule_audit.py --channel BUD

VÌ SAO: v1 (máy Mac, branch content-hub-backend) vẫn sản xuất và đăng lên
CÙNG các kênh (commit 29/09: "Dò sâu mọi khung giờ trước khi đăng"). Store của
v2 chỉ biết video của v2. Muốn biết có trùng không phải hỏi thẳng YouTube.

Quét TOÀN BỘ playlist uploads (không chỉ 500 video gần nhất), lấy trạng thái
từng video, rồi báo:
  1. Video hẹn giờ / mới công khai KHÔNG do v2 đăng (nguồn khác, vd v1)
  2. Hai video lên sóng cách nhau < 30 phút (chồng khung giờ)
  3. Trùng tiêu đề (đã chuẩn hoá) giữa video sắp lên và video 60 ngày gần đây
  4. Video v2 lên sóng trong khung giờ mà nguồn khác cũng có video
"""
from __future__ import annotations

import collections
import json
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402

GAP = timedelta(minutes=30)
LOOKBACK = timedelta(days=60)


def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c)).replace("đ", "d")
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", t)).strip()


def all_videos(tok: str) -> list[dict]:
    up = publish.uploads_playlist_id(tok)
    ids, page = [], None
    while True:
        p = {"part": "contentDetails", "playlistId": up, "maxResults": 50}
        if page:
            p["pageToken"] = page
        d = publish._api(tok, "GET", "playlistItems", p)
        ids += [it["contentDetails"]["videoId"] for it in d.get("items", [])]
        page = d.get("nextPageToken")
        if not page:
            break
    # Playlist uploads có thể trả CÙNG một video nhiều lần (đã gặp: một video
    # "chồng giờ" với chính nó) -> lọc trùng theo ID trước khi soát.
    ids = list(dict.fromkeys(ids))
    out = []
    for i in range(0, len(ids), 50):
        d = publish._api(tok, "GET", "videos", {"part": "snippet,status", "id": ",".join(ids[i:i + 50])})
        for v in d.get("items", []):
            st, sn = v["status"], v["snippet"]
            when = st.get("publishAt") if st["privacyStatus"] == "private" and st.get("publishAt") else sn["publishedAt"]
            out.append({"id": v["id"], "title": sn["title"], "privacy": st["privacyStatus"],
                        "scheduled": bool(st.get("publishAt")) and st["privacyStatus"] == "private",
                        "live_at": datetime.strptime(when[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)})
    return out


def audit(ch: str) -> dict:
    tok = publish.access_token(json.loads(channels.creds_path(ch).read_text(encoding="utf-8")))
    vids = all_videos(tok)
    with store.connect() as c:
        mine = {r[0]: r[1] for r in c.execute("SELECT video_id, slug FROM item WHERE channel=? AND video_id IS NOT NULL", (ch,))}
    now = datetime.now(timezone.utc)
    upcoming = [v for v in vids if v["scheduled"]]
    recent = [v for v in vids if v["live_at"] >= now - LOOKBACK]
    foreign_up = [v for v in upcoming if v["id"] not in mine]
    # chồng khung giờ: sắp theo thời điểm lên sóng
    sl = sorted([v for v in vids if v["live_at"] >= now - timedelta(days=2)], key=lambda v: v["live_at"])
    clash = [(a, b) for a, b in zip(sl, sl[1:]) if b["live_at"] - a["live_at"] < GAP]
    # trùng tiêu đề
    groups = collections.defaultdict(list)
    for v in recent + upcoming:
        groups[norm(v["title"])].append(v)
    dups = {k: vs for k, vs in groups.items() if len({v["id"] for v in vs}) > 1
            and any(v["scheduled"] for v in vs)}
    # Lưu tiêu đề TOÀN kênh cho bộ chống trùng chủ đề (factory/lines/novelty.py).
    tdir = ROOT / "data" / "channel_titles"
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / f"{ch}.json").write_text(json.dumps({"saved_at": now.isoformat(), "videos": [
        {"id": v["id"], "title": v["title"], "live_at": v["live_at"].isoformat(), "v2": v["id"] in mine}
        for v in vids]}, ensure_ascii=False), encoding="utf-8")
    return {"ch": ch, "total": len(vids), "upcoming": upcoming, "mine": mine, "foreign_up": foreign_up,
            "recent_foreign": [v for v in recent if v["id"] not in mine and not v["scheduled"]],
            "clash": clash, "dups": dups}


def fmt(v, mine):
    src = "v2:" + mine[v["id"]] if v["id"] in mine else "NGUỒN KHÁC"
    vn = v["live_at"] + timedelta(hours=7)
    return f"{vn:%d/%m %H:%M} VN  {'hẹn' if v['scheduled'] else v['privacy'][:6]:6s} {v['id']}  [{src}]  {v['title'][:60]}"


if __name__ == "__main__":
    chs = [channels.pick()] if "--channel" in sys.argv else channels.available()
    bad = 0
    for ch in chs:
        a = audit(ch)
        print(f"\n== {channels.CHANNELS[ch]['ten']} ({ch}) — {a['total']} video trên kênh · "
              f"{len(a['upcoming'])} đang hẹn giờ ({len(a['upcoming']) - len(a['foreign_up'])} của v2, "
              f"{len(a['foreign_up'])} nguồn khác) · {len(a['recent_foreign'])} video nguồn khác lên sóng 60 ngày qua")
        for v in sorted(a["foreign_up"], key=lambda v: v["live_at"])[:15]:
            print("   hẹn giờ nguồn khác:", fmt(v, a["mine"]))
        for x, y in a["clash"][:15]:
            print(f"   CHỒNG GIỜ (<30'):\n      {fmt(x, a['mine'])}\n      {fmt(y, a['mine'])}")
        for k, vs in list(a["dups"].items())[:15]:
            print(f"   TRÙNG TIÊU ĐỀ «{vs[0]['title'][:50]}»:")
            for v in vs:
                print("      " + fmt(v, a["mine"]))
        bad += len(a["clash"]) + len(a["dups"])
    print(f"\nTổng vấn đề: {bad}")
    sys.exit(1 if bad else 0)
