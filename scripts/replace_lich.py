"""Thay video Lịch sai dữ kiện (N1) bằng bản dựng lại từ lịch đã sửa. Mặc định CHẠY KHÔ.

    python scripts/replace_lich.py --channel FS                          # in kế hoạch, không đổi gì
    python scripts/replace_lich.py --channel FS --apply                  # làm thật
    python scripts/replace_lich.py --channel FS --from 2026-10-20 --to 2026-11-30 --apply
    python scripts/replace_lich.py --channel FS --apply --keep-near      # chừa các ngày quá sát
rồi:
    python scripts/run_pipeline.py resume --channel FS                   # dựng + đăng bản mới

Mỗi ngày Lịch (bundle lich-YYYYMMDD) rơi vào đúng một nhóm:
  ĐÚNG        kịch bản qua bộ đối chiếu mới và store khớp -> để yên
  ĐÃ PHÁT     video đã công khai -> KHÔNG đụng; xử lý tay (docs/RUNBOOK-lich.md)
  THAY        có video chưa lên sóng -> gỡ lịch video cũ (private, không hẹn, tiêu
              đề thêm "[ĐÃ THAY] "), cất bundle cũ vào archive/, ghi bundle mới,
              item về pending để pipeline dựng + đăng lại đúng giờ cũ
  THAY-SÁT    như THAY nhưng còn dưới --lead giờ (mặc định 12) là lên sóng: có thể
              không kịp dựng lại, slot trống. Vẫn thay -- thà trống còn hơn phát
              lịch sai mà người xem làm theo; --keep-near để chừa lại
  GỠ          video cũ còn hẹn nhưng không còn kịp đăng bản thay -> chỉ gỡ lịch
              (trừ khi --keep-near), item bị LOẠI
  CHƯA ĐĂNG   chưa có video -> cất bundle cũ, ghi bundle mới, item về pending
  KHÔI PHỤC   lần chạy trước dừng giữa chừng (bundle đã mới, store còn trỏ video
              cũ / audio cũ) -> làm nốt
  LỠ          giờ lên sóng đã qua, video không công khai -> để yên, chỉ báo
  KHÔNG DỰNG  kịch bản mới KHÔNG qua đối chiếu -> để yên, phải xem tay

Không xoá video nào (xoá là vĩnh viễn): video cũ nằm ở private, tiêu đề có
"[ĐÃ THAY]" để lọc rồi xoá hàng loạt trong Studio khi đã chắc. Lô bundle mới
phải qua kiểm chéo như make_lich_month.py, không thì không làm gì. Chạy lại
an toàn: ngày đã thay xong thành ĐÚNG.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, lich, lunar, publish, store  # noqa: E402
from factory.batchcheck import report_batch  # noqa: E402
from factory.bundle import Bundle  # noqa: E402
from factory.factcheck import report  # noqa: E402

PREFIX = "lich-"
TITLE_TAG = "[ĐÃ THAY] "
REASON = "N1: Trực/12 thần tính sai (vnlunar 1.0.3/1.0.4), thay bằng bản đối chiếu kép"
ARCHIVE = ROOT / "archive" / "bundles"     # NGOÀI bundles/: iter_bundles() duyệt mọi thư mục con trong đó
VN = timezone(timedelta(hours=7))
ACTIVE = ("THAY", "THAY-SÁT", "GỠ", "CHƯA ĐĂNG", "KHÔI PHỤC")


@dataclass
class Day:
    slug: str
    target: date
    old: Bundle
    new: Bundle | None = None
    item: dict | None = None
    yt: dict | None = None
    group: str = ""
    note: str = ""
    unschedule: bool = False       # gỡ lịch + gắn "[ĐÃ THAY]" cho video cũ
    write: bool = False            # cất bundle cũ + ghi bundle mới
    reset: bool = False            # item về pending, quên video cũ
    reject: bool = False           # item bị LOẠI (không kịp thay)
    errors: list = field(default_factory=list)

    @property
    def slot(self) -> datetime:
        return publish.parse_publish_at((self.new or self.old).publish_at)


def slug_date(slug: str) -> date:
    s = slug[len(PREFIX):]
    return date(int(s[:4]), int(s[4:6]), int(s[6:8]))


def load_days(ch: str, frm: date | None, to: date | None) -> list[Day]:
    out = []
    for p in sorted((store.BUNDLE_DIR / ch).glob(f"{PREFIX}*.json")):
        b = Bundle.from_json(p.read_text(encoding="utf-8"))
        d = slug_date(b.slug)
        if (frm is None or d >= frm) and (to is None or d <= to):
            out.append(Day(slug=b.slug, target=d, old=b))
    return out


def yt_status(video_ids: list[str], token: str) -> dict[str, dict]:
    """{video_id: {title, privacyStatus, publishAt}} -- video đã xoá thì không có mặt."""
    out = {}
    for i in range(0, len(video_ids), 50):
        d = publish._api(token, "GET", "videos", {"part": "snippet,status", "id": ",".join(video_ids[i:i + 50])})
        for v in d.get("items", []):
            out[v["id"]] = {"title": v["snippet"]["title"], "privacyStatus": v["status"]["privacyStatus"],
                            "publishAt": v["status"].get("publishAt")}
    return out


def _consistent(day: Day) -> bool:
    """Bundle đã đúng: store có còn trỏ vào sản phẩm của bundle CŨ không?"""
    it, v = day.item, day.yt
    if it is None:
        return True
    if it.get("video_id"):
        # video đã xoá, hay tiêu đề khác bundle (vd đã gắn "[ĐÃ THAY]") -> store trỏ vào video CŨ
        return v is not None and v["title"] == day.old.title
    sha = it.get("script_sha")
    return sha is None or sha == store.script_sha(day.old.script)


def classify(days: list[Day], now: datetime, lead: timedelta, keep_near: bool) -> None:
    for day in days:
        f = lunar.facts_for(day.target)               # LunarMismatch -> dừng cả lô (vnlunar lệch bản ghim)
        ok_old, _ = report(day.old.script, f, day.old.publish_at, label=str(day.target))
        if ok_old:
            if _consistent(day):
                day.group = "ĐÚNG"
                continue
            day.new, day.group = day.old, "KHÔI PHỤC"
        else:
            day.new, text, _ = lich.build_bundle(f)
            if day.new is None:
                day.group, day.note = "KHÔNG DỰNG", text
                continue
        it, v = day.item, day.yt
        has_video = bool(it and it.get("video_id")) and v is not None
        if it and it.get("video_id") and v is None:
            day.note = f"video cũ {it['video_id']} không còn trên kênh (đã xoá?) -- coi như chưa đăng"
        can_upload = day.slot > now + publish.MIN_LEAD
        if has_video and v["privacyStatus"] != "private":
            day.group = "ĐÃ PHÁT"
            continue
        scheduled = has_video and bool(v.get("publishAt"))
        if not can_upload:
            if scheduled and not keep_near:
                day.group, day.unschedule, day.reject = "GỠ", True, True
            else:
                day.group = "LỠ"
            continue
        if day.group != "KHÔI PHỤC":
            day.group = "CHƯA ĐĂNG" if not has_video else ("THAY" if day.slot >= now + lead else "THAY-SÁT")
            if day.group == "THAY-SÁT" and keep_near:
                day.group, day.note = "LỠ", "chừa lại (--keep-near): video cũ SAI vẫn sẽ phát"
                continue
            day.write = True
        day.unschedule = has_video and v["privacyStatus"] == "private" and not v["title"].startswith(TITLE_TAG)
        day.reset = it is not None


def plan(ch: str, frm: date | None, to: date | None, now: datetime, lead: timedelta, keep_near: bool,
         token: str | None, status_fn=yt_status) -> tuple[list[Day], bool, str]:
    days = load_days(ch, frm, to)
    with store.connect() as conn:
        items = {r["slug"]: dict(r) for r in conn.execute(
            "SELECT * FROM item WHERE channel = ? AND slug LIKE ?", (ch, PREFIX + "%"))}
    for day in days:
        day.item = items.get(day.slug)
    vids = sorted({d.item["video_id"] for d in days if d.item and d.item.get("video_id")})
    yt = status_fn(vids, token) if vids else {}
    for day in days:
        if day.item and day.item.get("video_id"):
            day.yt = yt.get(day.item["video_id"])
    classify(days, now, lead, keep_near)
    fresh = [d.new for d in days if d.write]
    ok, text = report_batch(fresh, label="LÔ THAY") if fresh else (True, "LÔ THAY  không có bundle mới")
    return days, ok, text


def archive(day: Day, now: datetime) -> Path:
    dst = ARCHIVE / day.old.channel / f"{day.slug}.{now:%Y%m%dT%H%M%SZ}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps({
        "replaced_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "reason": REASON,
        "old_video_id": (day.item or {}).get("video_id"), "old_youtube": day.yt,
        "new_title": day.new.title if day.new else None, "bundle": day.old.to_dict(),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return dst


def apply(days: list[Day], token: str | None, now: datetime, unschedule_fn=publish.unschedule) -> dict:
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    done = {"gỡ lịch": 0, "bundle mới": 0, "về pending": 0, "loại": 0, "lỗi": 0}
    ch = days[0].old.channel if days else "FS"
    with store.connect() as conn, store.locked(conn, f"publish-{ch}"):
        for day in sorted((d for d in days if d.group in ACTIVE), key=lambda d: d.slot):
            # THỨ TỰ có chủ ý: gỡ lịch -> cất + ghi bundle -> sửa store. Dừng giữa
            # chừng ở bất kỳ đâu thì lần chạy sau thấy bundle mới + store cũ = KHÔI PHỤC,
            # và không lúc nào store trỏ "pending" vào một kịch bản SAI.
            vid = (day.item or {}).get("video_id")
            if day.unschedule:
                try:
                    unschedule_fn(vid, token, TITLE_TAG)
                    done["gỡ lịch"] += 1
                except publish.QuotaExceeded:
                    print(f"HẾT QUOTA ở {day.slug} -- chạy lại cùng lệnh sau giờ reset để làm nốt.")
                    break
                except (publish.RateLimited, OSError) as e:   # bị giới hạn tốc độ / mất mạng: dừng, đừng trượt qua cả lô
                    print(f"DỪNG ở {day.slug}: {e} -- chạy lại cùng lệnh sau ít phút để làm nốt.")
                    done["lỗi"] += 1
                    break
                except publish.PublishError as e:
                    print(f"   {day.slug}: LỖI gỡ lịch {e} -- bỏ qua ngày này, video cũ giữ nguyên")
                    day.errors.append(str(e))
                    done["lỗi"] += 1
                    continue
            if day.write:
                archive(day, now)
                store.save_bundle(day.new, overwrite=True)
                done["bundle mới"] += 1
            if day.reject:
                conn.execute("UPDATE item SET stage='failed', attempts=99, error=?, updated_at=? WHERE id=?",
                             (f"{REASON}: gỡ lịch {vid}, không kịp thay", stamp, day.item["id"]))
                done["loại"] += 1
            elif day.reset:
                conn.execute(
                    "UPDATE item SET stage='pending', video_id=NULL, wav_path=NULL, timing_path=NULL, "
                    "video_path=NULL, thumb_path=NULL, attempts=0, error=NULL, retry_after=NULL, "
                    "fail_stage=NULL, script_sha=NULL, publish_at=?, updated_at=? WHERE id=?",
                    (day.new.publish_at, stamp, day.item["id"]))
                done["về pending"] += 1
            elif day.write:                      # bundle chưa từng vào hàng đợi
                store.enqueue(day.new, conn)
                done["về pending"] += 1
    return done


def _vn(dt: datetime) -> str:
    return dt.astimezone(VN).strftime("%d/%m %H:%M")


def show(days: list[Day], batch_text: str, now: datetime, lead: timedelta) -> None:
    order = ["ĐÃ PHÁT", "THAY", "THAY-SÁT", "GỠ", "CHƯA ĐĂNG", "KHÔI PHỤC", "LỠ", "KHÔNG DỰNG", "ĐÚNG"]
    print(f"Lịch FS · {len(days)} ngày · bây giờ {_vn(now)} VN · ngưỡng sát {lead.total_seconds() / 3600:g} giờ")
    for g in order:
        grp = [d for d in days if d.group == g]
        if not grp:
            continue
        print(f"\n{g} ({len(grp)})")
        for d in grp[:200]:
            vid = (d.item or {}).get("video_id") or "-"
            st = (d.yt or {}).get("privacyStatus", "")
            line = f"  {d.target:%d/%m/%Y}  lên {_vn(d.slot)} VN  video {vid} {st}"
            if d.new is not None and d.new.title != d.old.title:
                line += f"\n      cũ: {d.old.title}\n      mới: {d.new.title}"
            if d.note:
                line += f"\n      {d.note.splitlines()[0][:160]}"
            print(line)
    print("\n" + batch_text)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv if argv is None else argv
    ch = channels.pick(argv, required=True)
    if ch != lich.CHANNEL:
        raise SystemExit(f"Lịch chỉ có ở kênh {lich.CHANNEL}")
    args = channels.args_without_channel(argv)

    def opt(flag):
        return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else None

    frm = date.fromisoformat(opt("--from")) if opt("--from") else None
    to = date.fromisoformat(opt("--to")) if opt("--to") else None
    lead = timedelta(hours=float(opt("--lead") or 12))
    apply_ = "--apply" in args
    keep_near = "--keep-near" in args
    now = datetime.now(timezone.utc)

    token = publish.access_token(channels.load_creds(ch))
    with store.connect() as conn:
        channels.verify_identity(ch, token, conn)
    try:
        days, ok, batch_text = plan(ch, frm, to, now, lead, keep_near, token)
    except lunar.LunarMismatch as e:     # vnlunar không phải bản ghim -> không tin được "bản mới"
        raise SystemExit(f"DỪNG: {e}")
    show(days, batch_text, now, lead)
    if not ok:
        print("\nDỪNG: lô bundle mới không qua kiểm chéo -- không làm gì.")
        return 1
    if not apply_:
        print("\nCHẠY KHÔ -- thêm --apply để làm thật.")
        return 0
    done = apply(days, token, now)
    print("\nĐÃ LÀM: " + ", ".join(f"{k} {v}" for k, v in done.items()))
    print("Tiếp: python scripts/run_pipeline.py resume --channel FS   (dựng + đăng bản mới, đúng giờ cũ)")
    print("Video cũ: lọc tiêu đề \"[ĐÃ THAY]\" trong YouTube Studio để xoá khi đã chắc.")
    return 1 if done["lỗi"] else 0


if __name__ == "__main__":
    sys.exit(main())
