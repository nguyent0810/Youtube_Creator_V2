"""Gỡ lịch public của video dài: giữ PRIVATE, bỏ publishAt. Không xóa video, không đổi tiêu đề.
    python motion/long/unschedule.py <CH> <topic> [<topic> ...] [--dry]
Đọc video_id từ output/long/<topic>/pub/result.json; ghi "unscheduled_at" + lịch cũ vào file đó.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory import channels, publish  # noqa: E402

API = "https://www.googleapis.com/youtube/v3/videos"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    ch, topics = args[0], args[1:]
    creds = json.loads(channels.creds_path(ch).read_text(encoding="utf-8"))
    H = {"Authorization": f"Bearer {publish.access_token(creds)}"}
    res = {t: json.loads((ROOT / "output/long" / t / "pub/result.json").read_text(encoding="utf-8")) for t in topics}
    r = requests.get(API, params={"part": "snippet,status,contentDetails", "id": ",".join(v["video_id"] for v in res.values())}, headers=H, timeout=60)
    r.raise_for_status()
    items = {it["id"]: it for it in r.json()["items"]}
    for t, v in res.items():
        it = items.get(v["video_id"])
        if not it:
            print(f"{t}: {v['video_id']} KHÔNG THẤY trên kênh")
            continue
        st = it["status"]
        print(f"{t}: {v['video_id']} {st['privacyStatus']} publishAt={st.get('publishAt')} dur={it['contentDetails']['duration']} | {it['snippet']['title'][:70]}")
        if dry or st["privacyStatus"] != "private" or not st.get("publishAt"):
            continue   # đã public hoặc không có lịch: không đụng
        body = {"id": v["video_id"], "status": {"privacyStatus": "private", "publishAt": None, "embeddable": st.get("embeddable", True),
                "publicStatsViewable": st.get("publicStatsViewable", True), "license": st.get("license", "youtube"),
                "selfDeclaredMadeForKids": st.get("madeForKids", False)}}
        p = requests.put(API, params={"part": "status"}, headers={**H, "Content-Type": "application/json"}, json=body, timeout=60)
        if p.status_code >= 300:
            raise SystemExit(f"PUT {t}: {p.status_code} {p.text[:300]}")
        v["was_publish_at"], v["unscheduled_at"] = st.get("publishAt"), datetime.now(timezone.utc).isoformat(timespec="seconds")
        (ROOT / "output/long" / t / "pub/result.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"   -> đã gỡ lịch, giữ private")


if __name__ == "__main__":
    main()
