"""Đăng lên YouTube — ba chế độ, mặc định là chế độ an toàn nhất.

    python scripts/publish_batch.py check --channel FS             # không đăng gì
    python scripts/publish_batch.py probe <slug> --channel FS      # đăng 1 video, KHÔNG hẹn giờ
    python scripts/publish_batch.py run --channel FS [--limit N]   # đăng thật, có hẹn giờ

VÌ SAO CÓ `probe`: lần chạy đầu của một đường ghi không nên là 30 video lên
kênh đang có 1.650 người theo dõi. `probe` đăng ĐÚNG MỘT video private và
KHÔNG có publishAt -- YouTube không bao giờ tự công khai nó. Duyệt xong thì
chạy `run`: video probe mang tag dấu của bundle, nên `run` NHẬN LẠI nó và
gán lịch (publish.set_schedule), không upload bản thứ hai.

`run` là chế độ thật: private + publishAt, YouTube tự chuyển công khai đúng
giờ. Vẫn KHÔNG BAO GIỜ đăng public ngay.

CÁC CHỐT (audit 08/10/2026):
  - `probe`/`run` bắt buộc --channel, và kiểm credential đúng kênh trước khi ghi.
  - Item có giờ hẹn đã qua bị LOẠI (không upload): publishAt quá khứ = công
    khai ngay. Item bị loại cần dời lịch rồi reset.
  - Trùng tiêu đề với video KHÔNG mang dấu của bundle -> loại, không tự nhận.
  - Dòng chỉ-đăng-lẻ (S-tier `cl-hs-`) không bao giờ đăng hàng loạt ở đây.
  - Một bundle hỏng/mất chỉ loại đúng item đó, không làm chết cả lô.
  - Khoá theo kênh: hai lần `run` chồng nhau không upload trùng.
"""
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402
from factory.bundle import BundleInvalid  # noqa: E402

ARGS = channels.args_without_channel()
MODE = ARGS[0] if ARGS else "check"
CHANNEL = channels.pick(required=MODE in ("probe", "run"))

# CHỈ đăng item khớp tiền tố này. `check` từng cho thấy hàng đợi có 32 item chứ
# không phải 30 -- hai cái thừa là video DEMO dựng lúc thử nghiệm. Hàng đợi là
# nơi mọi thứ dồn về, gồm cả thứ chỉ để thử; bước đăng phải tự lọc.
SLUG_PREFIX = channels.bulk_prefixes(CHANNEL)
DRIP_ONLY = channels.drip_only(CHANNEL)


def _split(rows):
    bulk = [r for r in rows if r["slug"].startswith(SLUG_PREFIX)]
    drip = [r for r in rows if DRIP_ONLY and r["slug"].startswith(DRIP_ONLY)]
    other = [r for r in rows if r not in bulk and r not in drip]
    return bulk, drip, other


def _session(conn):
    creds = channels.load_creds(CHANNEL)
    tok = publish.access_token(creds)
    ident = channels.verify_identity(CHANNEL, tok, conn)
    return creds, tok, ident


def _missed(publish_at: str) -> bool:
    try:
        publish.check_publish_at(publish_at)
        return False
    except publish.PublishAtPassed:
        return True


def do_check() -> None:
    """Mọi thứ kiểm được mà không ghi gì lên kênh."""
    with store.connect() as conn:
        _, tok, ident = _session(conn)
        info = publish._api(tok, "GET", "channels", {"part": "statistics", "mine": "true"}, None)
        stats = info["items"][0]["statistics"]
        print(f"kênh   : {ident['title']} ({ident['id']}) -- cấu hình {CHANNEL} "
              f"({channels.CHANNELS[CHANNEL]['ten']})")
        print(f"hiện có: {stats.get('videoCount')} video, {stats.get('subscriberCount')} sub")
        allr = store.next_batch(conn, "assembled", limit=500, channel=CHANNEL)
        rows, drip, other = _split(allr)
        print(f"sẵn sàng đăng: {len(rows)} item (khớp {', '.join(SLUG_PREFIX)})")
        if drip:
            print(f"BỎ QUA {len(drip)} item dòng chỉ-đăng-lẻ ({', '.join(DRIP_ONLY)}): "
                  "dùng motion/stier/upload_one.py / drip.py")
        if other:
            print(f"BỎ QUA {len(other)} item không khớp tiền tố: {[r['slug'] for r in other]}")
        late = [r["slug"] for r in rows if _missed(r["publish_at"])]
        if late:
            print(f"LỠ GIỜ {len(late)} item (giờ hẹn đã qua/quá sát) -> `run` sẽ LOẠI, cần dời lịch: {late[:10]}")
        titles = publish.channel_titles(ident["uploads"], tok)
        for r in rows[:3]:
            b = store.load_bundle(r["channel"], r["slug"])
            dup = titles.get(b.title.strip())
            print(f"   {r['slug']}  {r['publish_at']}  "
                  f"{'TRÙNG TIÊU ĐỀ trên kênh (' + dup + ') -> run sẽ kiểm tag dấu' if dup else 'chưa có'}")
        dl = store.deferred(conn, CHANNEL)
    if dl:
        print(f"đang hoãn: {len(dl)} item, thử lại từ {dl[0]['retry_after']}")
    print("\nquota: mỗi video 1 lượt upload, trần THỰC TẾ ~92 lượt/ngày/project (tài liệu ghi 100)")


def do_probe(slug: str | None) -> None:
    """Đăng ĐÚNG một video, private, KHÔNG hẹn giờ -> không bao giờ tự công khai."""
    if not slug:
        sys.exit("probe cần slug cụ thể: python scripts/publish_batch.py probe <slug> --channel X")
    b = store.load_bundle(CHANNEL, slug)
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM item WHERE channel=? AND slug=?", (CHANNEL, slug)).fetchone()
        if not row or not row["video_path"]:
            sys.exit(f"chưa dựng video cho {slug}")
        if row["video_id"] or row["stage"] == "published":
            sys.exit(f"{slug} đã có video trên kênh ({row['video_id']}) -- probe sẽ tạo bản trùng")
        with store.locked(conn, f"publish-{CHANNEL}"):
            _, tok, ident = _session(conn)
            print(f"đăng THỬ lên {ident['title']} (private, KHÔNG hẹn giờ): {b.title}")
            print(f"  file: {row['video_path']}")
            vid = publish.upload_video(b, Path(row["video_path"]), tok, schedule=False)
            conn.execute("UPDATE item SET error = ?, updated_at = ? WHERE id = ?",
                         (f"PROBE {vid}: private, chưa hẹn giờ -- duyệt xong chạy `run`", store._now(), row["id"]))
    print(f"\n  XONG. video_id = {vid}")
    print(f"  https://studio.youtube.com/video/{vid}/edit")
    print("  Video đang PRIVATE và KHÔNG có lịch -> sẽ không bao giờ tự công khai.")
    print("  Đạt thì chạy `run` (nó nhận lại video này và gán lịch); không đạt thì xoá video.")


def _foreign_days(tok: str, conn) -> set:
    """Các ngày (giờ VN, từ hôm nay) mà SHORT không do v2 đăng sẽ/đang lên sóng.

    Chỉ tính Shorts (<= 3 phút): video dài của chính kênh (publish_long.py
    không ghi vào store) từng làm cả ngày Shorts CL bị coi là "bận"."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from schedule_audit import all_videos
    mine = {r[0] for r in conn.execute(
        "SELECT video_id FROM item WHERE channel = ? AND video_id IS NOT NULL", (CHANNEL,))}
    today = (datetime.now(timezone.utc) + timedelta(hours=7)).date()
    return {(v["live_at"] + timedelta(hours=7)).date() for v in all_videos(tok)
            if v["id"] not in mine and (v["live_at"] + timedelta(hours=7)).date() >= today
            and (v.get("seconds") is None or v["seconds"] <= 180)}


def _publish_with_backoff(b, path, creds, tok, titles):
    """Giới hạn tốc độ (RateLimited) là chuyện vài chục giây: chờ rồi thử lại."""
    for attempt in range(3):
        try:
            return publish.publish_bundle(b, path, creds, token=tok, known_titles=titles)
        except publish.RateLimited:
            if attempt == 2:
                raise
            time.sleep(30 * 2 ** attempt)


def do_run(limit: int) -> None:
    with store.connect() as conn, store.locked(conn, f"publish-{CHANNEL}"):
        creds, tok, ident = _session(conn)
        tok_at = time.monotonic()
        allr = store.next_batch(conn, "assembled", limit=500, channel=CHANNEL)
        match, drip, other = _split(allr)
        rows = match[:limit]
        print(f"kênh {ident['title']}: {len(rows)} item sẽ đăng (private + hẹn giờ), "
              f"bỏ qua {len(other)} không khớp tiền tố, {len(drip)} item chỉ-đăng-lẻ")
        if not rows:
            print("trạng thái:", store.summary(conn))
            return

        # Chụp danh sách tiêu đề trên kênh MỘT lần cho cả lô.
        titles = publish.channel_titles(ident["uploads"], tok)
        print(f"chống trùng: đã chụp {len(titles)} tiêu đề gần nhất trên kênh")

        # CHỐT NGUỒN KHÁC (30/09/2026): v1/máy khác vẫn hẹn giờ lên CÙNG kênh với
        # kho trạng thái riêng. Ngày (giờ VN) nào nguồn khác đã có Short sắp/đang
        # lên sóng thì v2 không đăng vào ngày đó -- để lại hàng đợi, báo rõ. Item
        # bị bỏ qua mà để quá giờ sẽ bị LOẠI ở lần chạy sau (chốt giờ đã qua),
        # không bao giờ lên sóng muộn.
        busy = _foreign_days(tok, conn) if "--ignore-other" not in sys.argv else set()
        if busy:
            print(f"nguồn khác đã chiếm {len(busy)} ngày: "
                  f"{', '.join(d.strftime('%d/%m') for d in sorted(busy)[:12])}{'…' if len(busy) > 12 else ''}")

        for i, r in enumerate(rows, 1):
            tag = f"  [{i}/{len(rows)}] {r['slug']}"
            try:
                b = store.load_bundle(r["channel"], r["slug"])
            except (BundleInvalid, OSError) as exc:
                store.reject(conn, r["id"], f"BUNDLE HỎNG/MẤT: {exc}")
                print(f"{tag}  LOẠI: bundle không đọc được ({exc})")
                continue
            # Giờ hẹn lấy từ BUNDLE (thứ sẽ gửi lên YouTube), không từ DB.
            vn_day = (publish.parse_publish_at(b.publish_at) + timedelta(hours=7)).date()
            if vn_day in busy:
                print(f"{tag}  BỎ QUA: ngày {vn_day:%d/%m} nguồn khác đã có Short "
                      f"(dời lịch lô này, hoặc --ignore-other nếu chắc chắn)")
                continue
            if _missed(b.publish_at):
                store.reject(conn, r["id"], f"LỠ GIỜ: hẹn {b.publish_at} đã qua/quá sát -- không upload "
                                            "(publishAt quá khứ = công khai ngay). Dời lịch rồi reset item.")
                print(f"{tag}  LOẠI: giờ hẹn {b.publish_at} đã qua -- cần dời lịch")
                continue
            if r["script_sha"] and r["script_sha"] != store.script_sha(b.script):
                store.reject(conn, r["id"], "KỊCH BẢN ĐÃ ĐỔI SAU KHI DỰNG: video là bản cũ. "
                                            "reset_items để dựng lại.")
                print(f"{tag}  LOẠI: kịch bản đã đổi sau khi dựng video")
                continue
            # access_token sống 60 phút; lô lớn hoặc mạng chậm thì vượt -- làm mới sớm.
            if time.monotonic() - tok_at > 40 * 60:
                tok, tok_at = publish.access_token(creds), time.monotonic()
            try:
                res = _publish_with_backoff(b, Path(r["video_path"]), creds, tok, titles)
            except publish.QuotaExceeded as exc:
                # Hết hạn mức NGÀY: item này VÀ mọi item sau đều hoãn tới lúc reset,
                # không tính là hỏng. Gọi tiếp chỉ nhận lại đúng lỗi.
                when = publish.next_quota_reset()
                for rr in rows[i - 1:]:
                    store.defer(conn, rr["id"], f"QuotaExceeded: {exc}", when)
                print(f"{tag}  HẾT QUOTA — hoãn {len(rows) - i + 1} item tới {when} (không tính là hỏng)")
                break
            except publish.RateLimited as exc:
                later = (datetime.now(timezone.utc) + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
                store.defer(conn, r["id"], f"RateLimited: {exc}", later)
                print(f"{tag}  GIỚI HẠN TỐC ĐỘ — hoãn item này tới {later}")
                continue
            except (publish.PublishAtPassed, publish.DuplicateTitle) as exc:
                store.reject(conn, r["id"], f"{type(exc).__name__}: {exc}")
                print(f"{tag}  LOẠI: {exc}")
                continue
            except Exception as exc:
                n = store.bump_attempt(conn, r["id"], f"{type(exc).__name__}: {exc}")
                print(f"{tag}  LỖI (lần {n}): {exc}")
                continue
            store.mark(conn, r["id"], "published", video_id=res.video_id)
            note = " (NHẬN LẠI bản đã upload)" if res.adopted else ""
            print(f"{tag}  {res.url}  hẹn {res.scheduled_at}{note}")
            for w in res.warnings:
                print(f"      cảnh báo: {w}")
            time.sleep(2)   # nhẹ tay với API
        print("\ntrạng thái:", store.summary(conn))


if __name__ == "__main__":
    if MODE == "check":
        do_check()
    elif MODE == "probe":
        do_probe(ARGS[1] if len(ARGS) > 1 else None)
    elif MODE == "run":
        lim = int(ARGS[ARGS.index("--limit") + 1]) if "--limit" in ARGS else 500
        try:
            do_run(lim)
        except store.LockBusy as exc:
            sys.exit(str(exc))
    else:
        sys.exit(__doc__)
