"""Đặt LẠI giờ hẹn gốc cho video v2 đã bị gỡ lịch (unschedule.py). Chỉ sửa status.

    python scripts/reschedule.py --channel FS                 # chạy khô
    python scripts/reschedule.py --channel FS --apply
    python scripts/reschedule.py --channel FS --prefix giap- --apply

Lý do tồn tại (30/09/2026): gỡ lịch 183 video FS do hiểu nhầm yêu cầu; người
dùng muốn GIỮ NGUYÊN mọi video đã lên lịch. Khôi phục theo thứ tự lên sóng
sớm nhất trước. Mỗi video 50 đơn vị quota (videos.update part=status); hết
quota thì dừng, chạy lại sau giờ reset để làm nốt -- idempotent: chỉ đụng
item còn đánh dấu UNSCHEDULED.

Video có giờ gốc đã qua thì để private và báo lại: gửi publishAt quá khứ
thì YouTube CÔNG KHAI NGAY (không phải từ chối như ghi chú cũ ở đây viết).

Đọc trạng thái THẬT trước khi ghi: video đã bị xoá trong Studio, đã công
khai, hay đã có lịch thì bỏ qua và báo -- bản cũ chết ở lỗi đầu tiên không
phải quota, mọi video phía sau nằm private và lần lượt lỡ giờ.
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402

CH = channels.pick(required=True)
ARGS = channels.args_without_channel()
APPLY = "--apply" in ARGS
PREFIXES = tuple(ARGS[i + 1] for i, a in enumerate(ARGS[:-1]) if a == "--prefix")


def main() -> None:
    tok = publish.access_token(channels.load_creds(CH))
    now = datetime.now(timezone.utc)
    done, missed, skipped = 0, [], []
    with store.connect() as conn:
        channels.verify_identity(CH, tok, conn)
        rows = [dict(r) for r in conn.execute(
            "SELECT id, slug, video_id, publish_at FROM item WHERE channel=? AND error LIKE 'UNSCHEDULED%' "
            "ORDER BY publish_at", (CH,)) if not PREFIXES or r["slug"].startswith(PREFIXES)]
        print(f"{len(rows)} video cần đặt lại giờ hẹn" + ("" if APPLY else " (CHẠY KHÔ — thêm --apply)"))
        for r in rows:
            when = publish.parse_publish_at(r["publish_at"])
            if when <= now + timedelta(minutes=15):
                missed.append(r["slug"])
                continue
            try:
                cur = publish.video_status(r["video_id"], tok)
            except publish.QuotaExceeded:
                print(f"HẾT QUOTA sau {done} video — chạy lại sau giờ reset để làm nốt.")
                break
            if cur is None:
                skipped.append(f"{r['slug']}: video {r['video_id']} không còn trên kênh")
                continue
            st = cur["status"]
            if st.get("privacyStatus") != "private" or st.get("publishAt"):
                skipped.append(f"{r['slug']}: đang {st.get('privacyStatus')}"
                               f"{' hẹn ' + st['publishAt'] if st.get('publishAt') else ''} -- không đụng")
                continue
            if not APPLY:
                print(f"   sẽ đặt {r['publish_at']}  {r['slug']}")
                continue
            try:
                publish.set_schedule(r["video_id"], r["publish_at"], tok)
            except publish.QuotaExceeded:
                print(f"HẾT QUOTA sau {done} video — chạy lại sau giờ reset để làm nốt "
                      f"{len(rows) - done - len(missed) - len(skipped)}.")
                break
            except publish.PublishError as e:
                skipped.append(f"{r['slug']}: lỗi {e}")
                continue
            conn.execute("UPDATE item SET stage='published', attempts=0, error=NULL, updated_at=? WHERE id=?",
                         (now.strftime("%Y-%m-%dT%H:%M:%SZ"), r["id"]))
            done += 1
            print(f"   {r['publish_at']}  {r['slug']}  đã đặt lại", flush=True)
    print(f"ĐÃ ĐẶT LẠI {done} video.")
    if missed:
        print(f"Giờ gốc đã qua (để private, cần xử lý tay): {missed}")
    for s in skipped:
        print(f"Bỏ qua: {s}")


if __name__ == "__main__":
    main()
