"""Đặt LẠI giờ hẹn gốc cho video v2 đã bị gỡ lịch (unschedule.py). Chỉ sửa status.

    python scripts/reschedule.py --channel FS

Lý do tồn tại (30/09/2026): gỡ lịch 183 video FS do hiểu nhầm yêu cầu; người
dùng muốn GIỮ NGUYÊN mọi video đã lên lịch. Khôi phục theo thứ tự lên sóng
sớm nhất trước. Mỗi video 50 đơn vị quota (videos.update part=status); hết
quota thì dừng, chạy lại sau giờ reset (14:00 VN) để làm nốt -- idempotent:
chỉ đụng item còn đánh dấu UNSCHEDULED. Video có giờ gốc đã qua thì để
private và báo lại (YouTube không nhận publishAt trong quá khứ).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402

CH = channels.pick()
tok = publish.access_token(json.loads(channels.creds_path(CH).read_text(encoding="utf-8")))
now = datetime.now(timezone.utc)
done, missed = 0, []
with store.connect() as conn:
    rows = [dict(r) for r in conn.execute(
        "SELECT id, slug, video_id, publish_at FROM item WHERE channel=? AND error LIKE 'UNSCHEDULED%' "
        "ORDER BY publish_at", (CH,))]
    print(f"{len(rows)} video cần đặt lại giờ hẹn")
    for r in rows:
        when = datetime.strptime(r["publish_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if when <= now + timedelta(minutes=2):
            missed.append(r["slug"])
            continue
        try:
            publish._api(tok, "PUT", "videos", {"part": "status"}, {
                "id": r["video_id"],
                "status": {"privacyStatus": "private", "publishAt": r["publish_at"],
                           "selfDeclaredMadeForKids": False, "embeddable": True,
                           "publicStatsViewable": True, "license": "youtube"}})
        except publish.QuotaExceeded:
            print(f"HẾT QUOTA sau {done} video — chạy lại sau 14:00 VN để làm nốt {len(rows) - done - len(missed)}.")
            break
        conn.execute("UPDATE item SET stage='published', attempts=0, error=NULL, updated_at=? WHERE id=?",
                     (now.strftime("%Y-%m-%dT%H:%M:%SZ"), r["id"]))
        done += 1
        print(f"   {r['publish_at']}  {r['slug']}  đã đặt lại", flush=True)
print(f"ĐÃ ĐẶT LẠI {done} video.")
if missed:
    print(f"Giờ gốc đã qua (để private, cần xử lý tay): {missed}")
