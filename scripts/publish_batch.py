"""Đăng lên YouTube — ba chế độ, mặc định là chế độ an toàn nhất.

    python scripts/publish_batch.py check              # không đăng gì
    python scripts/publish_batch.py probe  <slug>      # đăng 1 video, KHÔNG hẹn giờ
    python scripts/publish_batch.py run    [--limit N] # đăng thật, có hẹn giờ
    python scripts/publish_batch.py resolve <slug> <video_id|none>   # xử lý upload "không rõ"

Mọi lần ghi đi qua factory/channel.py: giãn nhịp theo kênh (CL 3 giờ/lần,
FS/BUD tối đa 24/ngày), sổ upload chống upload trùng, upload đứt giữa chừng
thì lần sau nối tiếp phiên cũ. Chưa tới lượt / hết quota / mạng đứt đều là
HOÃN, không tính là hỏng.

VÌ SAO CÓ `probe`: upload_video() chưa từng chạy lần nào. Lần chạy đầu của
một đường ghi không nên là 30 video lên kênh đang có 1.650 người theo dõi.

`probe` đăng ĐÚNG MỘT video ở chế độ private và CỐ Ý BỎ publishAt. Không có
publishAt thì YouTube không bao giờ tự chuyển sang công khai -- video nằm
im trong kênh cho tới khi con người vào xem rồi tự quyết. Nếu có gì sai
(encode hỏng, dấu tiếng Việt vỡ, mô tả lệch), nó sai ở chỗ không ai thấy.

`run` mới là chế độ thật: private + publishAt, YouTube tự chuyển công khai
đúng giờ. Vẫn KHÔNG BAO GIỜ đăng public ngay -- một lần nhầm là công khai
thật, không rút lại được.
"""
import dataclasses
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402
from factory.channel import Channel, DuplicateTitle, PacingHold, Upload  # noqa: E402
from factory.youtube_api import NetworkDown, RateLimited, UploadInDoubt, UploadInterrupted  # noqa: E402

CHANNEL = channels.pick()
CREDS = channels.creds_path(CHANNEL)
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"

# CHỈ đăng item khớp tiền tố này. Không có nó, `check` vừa cho thấy hàng đợi
# có 32 item chứ không phải 30 -- hai cái thừa là video DEMO dựng lúc thử
# nghiệm (mau-hop-menh-kim, huong-bep-quan-trong-hon). Chúng đã lọt vào
# hàng đợi qua sync_from_disk và sẽ bị đăng lên kênh thật.
#
# Hàng đợi là nơi mọi thứ dồn về, gồm cả thứ chỉ để thử. Bước đăng phải tự
# lọc, không được cho rằng mọi thứ trong hàng đợi đều đáng đăng.
# 21/09/2026: thêm 4 dòng pillar. Demo (mau-hop-menh-kim, ...) vẫn bị loại.
SLUG_PREFIX = channels.prefixes(CHANNEL)


def _creds() -> dict:
    return json.loads(CREDS.read_text(encoding="utf-8"))


def _upload_of(b, video_path: Path) -> Upload:
    # Bundle không có category: short dùng mặc định kênh; long giữ "22" như
    # upload_video cũ (video dài thật đi qua motion/long/publish_long.py).
    return Upload(slug=b.slug, video=video_path, title=b.title, description=b.description,
                  tags=tuple(b.tags), kind=b.kind, publish_at=b.publish_at,
                  category=None if b.kind == "short" else "22")


def _iso(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def do_check() -> None:
    """Mọi thứ kiểm được mà không ghi gì lên kênh."""
    tok = publish.access_token(_creds())
    up = publish.uploads_playlist_id(tok)
    info = publish._api(tok, "GET", "channels",
                        {"part": "snippet,statistics", "mine": "true"}, None)
    it = info["items"][0]
    print(f"kênh   : {it['snippet']['title']}")
    print(f"hiện có: {it['statistics'].get('videoCount')} video, "
          f"{it['statistics'].get('subscriberCount')} sub")
    with store.connect() as conn:
        allr = store.next_batch(conn, "assembled", limit=500, channel=CHANNEL)
    rows = [r for r in allr if r["slug"].startswith(SLUG_PREFIX)]
    bỏ = [r["slug"] for r in allr if not r["slug"].startswith(SLUG_PREFIX)]
    print(f"sẵn sàng đăng: {len(rows)} item (khớp {', '.join(SLUG_PREFIX)})")
    if bỏ:
        print(f"BỎ QUA {len(bỏ)} item không khớp tiền tố: {bỏ}")
    titles = publish.channel_titles(up, tok)
    for r in rows[:3]:
        b = store.load_bundle(r["channel"], r["slug"])
        dup = titles.get(b.title.strip())
        print(f"   {r['slug']}  {r['publish_at']}  "
              f"{'ĐÃ CÓ TRÊN KÊNH -> sẽ bỏ qua' if dup else 'chưa có'}")
    with store.connect() as conn:
        dl = store.deferred(conn, CHANNEL)
        chan = Channel.open(CHANNEL, conn)
        nxt = chan.next_upload_at()
        unfinished = chan.unfinished()
    if dl:
        print(f"đang hoãn: {len(dl)} item, thử lại từ {dl[0]['retry_after']}")
    p = chan.pacing
    print(f"giãn nhịp: tối thiểu {p.min_gap}/lần, tối đa {p.max_per_24h}/24 giờ "
          f"-> upload tiếp sớm nhất {_iso(nxt)}")
    if unfinished:
        print(f"upload dở dang (sẽ nối tiếp phiên cũ, hoặc chờ `resolve`): {unfinished}")
    print(f"\nquota: mỗi video 1 lượt upload, trần THỰC TẾ ~92 lượt/ngày/project "
          f"(tài liệu ghi 100)")


def do_probe(slug: str) -> None:
    """Đăng ĐÚNG một video, private, KHÔNG hẹn giờ -> không bao giờ tự công khai."""
    b = store.load_bundle(CHANNEL, slug)
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM item WHERE channel=? AND slug=?",
                           (CHANNEL, slug)).fetchone()
    if not row or not row["video_path"]:
        sys.exit(f"chưa dựng video cho {slug}")

    print(f"đăng THỬ (private, KHÔNG hẹn giờ): {b.title}")
    print(f"  file: {row['video_path']}")
    with store.connect() as conn:
        u = dataclasses.replace(_upload_of(b, Path(row["video_path"])), publish_at=None)
        vid = Channel.open(CHANNEL, conn).upload(u, unscheduled=True).video_id
    print(f"\n  XONG. video_id = {vid}")
    print(f"  https://studio.youtube.com/video/{vid}/edit")
    print("  Video đang PRIVATE và KHÔNG có lịch -> sẽ không bao giờ tự công khai.")
    print("  Vào xem, kiểm hình/tiếng/mô tả. Đạt thì chạy `run`: nó dùng lại đúng video")
    print("  này và gán lịch, không upload lần hai. Không đạt thì xoá trong Studio.")


def do_resolve(slug: str, video_id: str) -> None:
    """Upload "không rõ" (phiên hết hạn giữa chừng): người đã nhìn kênh và biết."""
    with store.connect() as conn:
        vid = None if video_id.lower() == "none" else video_id
        Channel.open(CHANNEL, conn).resolve(slug, vid)
        row = conn.execute("SELECT id FROM item WHERE channel=? AND slug=?", (CHANNEL, slug)).fetchone()
        if row and vid:
            store.mark(conn, row["id"], "published", video_id=vid)
        elif row:
            store.mark(conn, row["id"], "assembled")    # bỏ hoãn, lần `run` sau upload lại
    print(f"{slug}: " + (f"ghi nhận video {vid}" if vid else "không có video -- lần chạy sau upload lại"))


def _foreign_days(tok: str, conn) -> set:
    """Các ngày (giờ VN, từ hôm nay) mà video KHÔNG do v2 đăng sẽ/đang lên sóng."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from schedule_audit import all_videos
    mine = {r[0] for r in conn.execute("SELECT video_id FROM item WHERE video_id IS NOT NULL")}
    today = (datetime.now(timezone.utc) + timedelta(hours=7)).date()
    return {(v["live_at"] + timedelta(hours=7)).date() for v in all_videos(tok)
            if v["id"] not in mine and (v["live_at"] + timedelta(hours=7)).date() >= today}


def do_run(limit: int) -> None:
    tok = publish.access_token(_creds())       # chỉ cho các lệnh ĐỌC bên dưới
    with store.connect() as conn:
        allr = store.next_batch(conn, "assembled", limit=500, channel=CHANNEL)
        match = [r for r in allr if r["slug"].startswith(SLUG_PREFIX)]
        rows = match[:limit]
        print(f"{len(rows)} item sẽ đăng (private + hẹn giờ), "
              f"bỏ qua {len(allr) - len(match)} item không khớp")
        if not rows:
            print("trạng thái:", store.summary(conn))
            return

        # Chụp danh sách tiêu đề trên kênh MỘT lần cho cả lô.
        titles = publish.channel_titles(publish.uploads_playlist_id(tok), tok)
        print(f"chống trùng: đã chụp {len(titles)} tiêu đề gần nhất trên kênh")
        chan = Channel.open(CHANNEL, conn, channel_titles=titles)

        # CHỐT CHẶN NGUỒN KHÁC (30/09/2026): v1/máy khác vẫn hẹn giờ lên CÙNG
        # kênh với kho trạng thái riêng -- store v2 không biết. Ngày 30/09 06:00
        # kênh FS đã lên 2 video Lịch cùng lúc. Nên trước khi upload: đọc lịch
        # thật của kênh; ngày (giờ VN) nào nguồn khác đã có video sắp/đang lên
        # sóng thì v2 KHÔNG đăng vào ngày đó -- để lại hàng đợi, báo rõ.
        busy = _foreign_days(tok, conn) if "--ignore-other" not in sys.argv else set()
        if busy:
            print(f"nguồn khác đã chiếm {len(busy)} ngày: "
                  f"{', '.join(d.strftime('%d/%m') for d in sorted(busy)[:12])}{'…' if len(busy) > 12 else ''}")

        for i, r in enumerate(rows, 1):
            b = store.load_bundle(r["channel"], r["slug"])
            vn_day = (datetime.strptime(r["publish_at"], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=7)).date()
            if vn_day in busy:
                print(f"  [{i}/{len(rows)}] {b.slug}  BỎ QUA: ngày {vn_day:%d/%m} nguồn khác đã có video "
                      f"(dời lịch lô này, hoặc --ignore-other nếu chắc chắn)")
                continue
            try:
                res = chan.upload(_upload_of(b, Path(r["video_path"])))
                store.mark(conn, b.id, "published", video_id=res.video_id)
                print(f"  [{i}/{len(rows)}] {b.slug}  {res.url}  hẹn {res.publish_at}"
                      f"{'  (đã có sẵn, không upload lại)' if res.reused else ''}")
            except PacingHold as exc:
                # Chưa tới lượt theo luật giãn nhịp: item này và mọi item sau
                # hoãn tới mốc được upload tiếp. Không tính là hỏng.
                when = _iso(exc.until)
                for rr in rows[i - 1:]:
                    store.defer(conn, rr["id"], f"PacingHold: {exc}", when)
                print(f"  [{i}/{len(rows)}] ĐỦ NHỊP — hoãn {len(rows) - i + 1} item tới {when}")
                break
            except (UploadInterrupted, RateLimited, NetworkDown) as exc:
                # Đứt sau khi đã có phiên: video có thể đã tạo xong. Lần sau
                # Channel hỏi lại phiên, không upload lại. Mạng / API đang
                # nghẽn -> dừng lô, thử lại sau 15 phút.
                store.defer(conn, b.id, f"UploadInterrupted: {exc}",
                            _iso(datetime.now(timezone.utc) + timedelta(minutes=15)))
                print(f"  [{i}/{len(rows)}] {b.slug}  ĐỨT GIỮA CHỪNG — sẽ nối tiếp phiên cũ: {exc}")
                break
            except UploadInDoubt as exc:
                store.defer(conn, b.id, f"UploadInDoubt: {exc}",
                            _iso(datetime.now(timezone.utc) + timedelta(days=1)))
                print(f"  [{i}/{len(rows)}] {b.slug}  KHÔNG RÕ đã lên kênh chưa — xem Studio rồi chạy:\n"
                      f"      publish_batch.py resolve {b.slug} <video_id|none> --channel {CHANNEL}")
            except DuplicateTitle as exc:
                # Tiêu đề thuộc về video khác: lỗi NỘI DUNG, thử lại vô ích.
                # Trước đây chỗ này âm thầm ghi video_id của video kia (9 ngày Lịch).
                store.reject(conn, b.id, f"DuplicateTitle: {exc}")
                print(f"  [{i}/{len(rows)}] {b.slug}  TRÙNG TIÊU ĐỀ — loại, cần sửa bundle: {exc}")
            except publish.QuotaExceeded as exc:
                # Hết hạn mức: item này VÀ mọi item sau đều hoãn tới lúc
                # reset, không tính là hỏng. Gọi tiếp chỉ nhận lại đúng lỗi.
                when = publish.next_quota_reset()
                for rr in rows[i - 1:]:
                    store.defer(conn, rr["id"], f"QuotaExceeded: {exc}", when)
                print(f"  [{i}/{len(rows)}] HẾT QUOTA — hoãn {len(rows) - i + 1} item "
                      f"tới {when} (không tính là hỏng)")
                break
            except Exception as exc:
                n = store.bump_attempt(conn, b.id, f"{type(exc).__name__}: {exc}")
                print(f"  [{i}/{len(rows)}] {b.slug}  LỖI (lần {n}): {exc}")
            time.sleep(2)   # nhẹ tay với API
        print("\ntrạng thái:", store.summary(conn))


if __name__ == "__main__":
    if MODE in ("probe", "run") and channels.upload_mode(CHANNEL) == "manual":
        # Không để Channel ném ManualChannel giữa lô rồi bị đếm là "hỏng".
        sys.exit(f"kênh {CHANNEL} upload TAY: scripts/export_manual.py --channel {CHANNEL}, "
                 f"upload qua Studio, rồi scripts/adopt_manual.py --channel {CHANNEL}")
    if MODE == "check":
        do_check()
    elif MODE == "probe":
        do_probe(sys.argv[2] if len(sys.argv) > 2 else "lich-20261001")
    elif MODE == "resolve":
        if len(sys.argv) < 4:
            sys.exit(__doc__)
        do_resolve(sys.argv[2], sys.argv[3])
    elif MODE == "run":
        lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 500
        print(f"kênh {CHANNEL} ({channels.CHANNELS[CHANNEL]['ten']})")
        do_run(lim)
    else:
        sys.exit(__doc__)
