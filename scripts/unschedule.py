"""Gỡ lịch hẹn các video v2 CHƯA lên sóng của một kênh -> private, KHÔNG hẹn giờ.

    python scripts/unschedule.py --channel FS                                   # chạy khô
    python scripts/unschedule.py --channel FS --prefix lich- --from 2026-10-10  # chỉ Lịch từ 10/10
    python scripts/unschedule.py --channel FS --prefix lich- --apply            # gỡ thật

KHÔNG xoá video -- xoá là vĩnh viễn; video bị gỡ lịch nằm im ở private,
không bao giờ tự công khai, muốn xoá thì làm hàng loạt trong YouTube Studio.
Chỉ đụng video mà store v2 ghi là của v2 VÀ YouTube xác nhận đang private +
có publishAt trong tương lai.

--prefix (lặp lại được) và --from/--to (ngày lên sóng, giờ VN) để gỡ ĐÚNG
một phần: bản cũ chỉ có "gỡ hết" -- muốn gỡ riêng 83 video Lịch sai dữ kiện
thì sẽ kéo theo cả 4 dòng pillar.

Item bị gỡ được đánh dấu UNSCHEDULED trong store; `reschedule.py` đặt lại
đúng giờ gốc nếu đổi ý. Muốn THAY bằng video mới thì xoá video cũ trong
Studio rồi reset item (xem docs/RUNBOOK-lich.md).
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402

CH = channels.pick(required=True)
ARGS = channels.args_without_channel()
APPLY = "--apply" in ARGS


def _opt_all(flag: str) -> list[str]:
    return [ARGS[i + 1] for i, a in enumerate(ARGS[:-1]) if a == flag]


PREFIXES = tuple(_opt_all("--prefix"))
FROM = date.fromisoformat(_opt_all("--from")[0]) if _opt_all("--from") else None
TO = date.fromisoformat(_opt_all("--to")[0]) if _opt_all("--to") else None
bad = [p for p in PREFIXES if not p.startswith(channels.prefixes(CH))]
if bad:
    sys.exit(f"tiền tố {bad} không thuộc kênh {CH} (có: {', '.join(channels.prefixes(CH))})")


def _wanted(row) -> bool:
    if PREFIXES and not row["slug"].startswith(PREFIXES):
        return False
    vn_day = (publish.parse_publish_at(row["publish_at"]) + timedelta(hours=7)).date()
    return (FROM is None or vn_day >= FROM) and (TO is None or vn_day <= TO)


def main() -> None:
    tok = publish.access_token(channels.load_creds(CH))
    with store.connect() as conn:
        ident = channels.verify_identity(CH, tok, conn)
        rows = {r["video_id"]: dict(r) for r in conn.execute(
            "SELECT id, slug, video_id, publish_at FROM item WHERE channel=? AND video_id IS NOT NULL", (CH,))
            if _wanted(r)}
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
    scope = (f" · tiền tố {', '.join(PREFIXES)}" if PREFIXES else "") + \
            (f" · từ {FROM}" if FROM else "") + (f" · tới {TO}" if TO else "")
    print(f"{ident['title']} ({CH}){scope}: {len(rows)} video v2 khớp · {len(todo)} đang hẹn giờ chưa lên sóng")
    if todo:
        print(f"   từ {todo[0][0]['publish_at']} ({todo[0][0]['slug']}) tới "
              f"{todo[-1][0]['publish_at']} ({todo[-1][0]['slug']})")
    if not APPLY:
        print("CHẠY KHÔ — thêm --apply để gỡ lịch thật.")
        return

    done = 0
    with store.connect() as conn, store.locked(conn, f"publish-{CH}"):
        for r, st in todo:
            # videos.update part=status GHI ĐÈ toàn bộ status: bỏ publishAt = gỡ lịch.
            try:
                publish._api(tok, "PUT", "videos", {"part": "status"}, {
                    "id": r["video_id"],
                    "status": {"privacyStatus": "private",
                               "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", False),
                               "embeddable": st.get("embeddable", True),
                               "publicStatsViewable": st.get("publicStatsViewable", True),
                               "license": st.get("license", "youtube")},
                })
            except publish.QuotaExceeded:
                print(f"HẾT QUOTA sau {done} video — chạy lại sau giờ reset để gỡ nốt.")
                break
            except publish.PublishError as e:
                print(f"   {r['slug']}: LỖI {e} -- bỏ qua, gỡ tiếp")
                continue
            conn.execute("UPDATE item SET stage='failed', attempts=99, error=?, updated_at=? WHERE id=?",
                         (f"UNSCHEDULED {now:%Y-%m-%d}: video {r['video_id']} gỡ lịch (vẫn private)",
                          now.strftime("%Y-%m-%dT%H:%M:%SZ"), r["id"]))
            done += 1
            if done % 10 == 0:
                print(f"   đã gỡ {done}/{len(todo)}")
    print(f"ĐÃ GỠ LỊCH {done} video (private, không hẹn giờ).")


if __name__ == "__main__":
    main()
