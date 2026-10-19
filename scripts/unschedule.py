"""Gỡ lịch hẹn các video v2 CHƯA lên sóng của một kênh -> private, KHÔNG hẹn giờ.

    python scripts/unschedule.py --channel FS           # chạy khô, chỉ liệt kê
    python scripts/unschedule.py --channel FS --apply   # gỡ thật

Dùng khi nhường kênh cho nguồn khác (30/09/2026: người dùng giao Phong Thủy và
Phật Giáo cho kênh kia xử lý). KHÔNG xoá video -- xoá là vĩnh viễn; video bị
gỡ lịch nằm im ở private, không bao giờ tự công khai, muốn xoá thì làm hàng
loạt trong YouTube Studio. Chỉ đụng video mà store v2 ghi là của v2 VÀ YouTube
xác nhận đang private + có publishAt trong tương lai.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402
from factory.channel import Channel  # noqa: E402

CH = channels.pick()
APPLY = "--apply" in sys.argv

tok = publish.access_token(json.loads(channels.creds_path(CH).read_text(encoding="utf-8")))
with store.connect() as conn:
    rows = {r["video_id"]: dict(r) for r in conn.execute(
        "SELECT id, slug, video_id, publish_at FROM item WHERE channel=? AND video_id IS NOT NULL", (CH,))}
now = datetime.now(timezone.utc)
todo = []
ids = list(rows)
for i in range(0, len(ids), 50):
    d = publish._api(tok, "GET", "videos", {"part": "status", "id": ",".join(ids[i:i + 50])})
    for v in d.get("items", []):
        st = v["status"]
        pa = st.get("publishAt")
        if st["privacyStatus"] == "private" and pa and datetime.fromisoformat(pa.replace("Z", "+00:00")) > now:
            todo.append((rows[v["id"]], st))
todo.sort(key=lambda x: x[0]["publish_at"])
print(f"{CH}: {len(rows)} video v2 trên kênh · {len(todo)} đang hẹn giờ chưa lên sóng"
      + ("" if todo else ""))
if todo:
    print(f"   từ {todo[0][0]['publish_at']} ({todo[0][0]['slug']}) tới {todo[-1][0]['publish_at']} ({todo[-1][0]['slug']})")
if not APPLY:
    print("CHẠY KHÔ — thêm --apply để gỡ lịch thật.")
    sys.exit(0)

done = 0
with store.connect() as conn:
    chan = Channel.open(CH, conn)
    for r, _st in todo:
        # Gỡ lịch = private không publishAt. Channel merge mọi trường status khác.
        chan.reschedule(r["video_id"], None)
        conn.execute("UPDATE item SET stage='failed', attempts=99, error=?, updated_at=? WHERE id=?",
                     (f"UNSCHEDULED {now:%Y-%m-%d}: nhường kênh cho nguồn khác theo yêu cầu người dùng",
                      now.strftime("%Y-%m-%dT%H:%M:%SZ"), r["id"]))
        done += 1
        if done % 10 == 0:
            print(f"   đã gỡ {done}/{len(todo)}")
print(f"ĐÃ GỠ LỊCH {done} video (private, không hẹn giờ).")
