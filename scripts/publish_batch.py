"""Đăng lên YouTube — ba chế độ, mặc định là chế độ an toàn nhất.

    python scripts/publish_batch.py check              # không đăng gì
    python scripts/publish_batch.py probe  <slug>      # đăng 1 video, KHÔNG hẹn giờ
    python scripts/publish_batch.py run    [--limit N] # đăng thật, có hẹn giờ

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
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import publish, store  # noqa: E402

CREDS = Path(r"C:\Tools\Youtuber\vietneu-tts\.youtube_channels\phong_thuy.json")
CHANNEL = "FS"
MODE = sys.argv[1] if len(sys.argv) > 1 else "check"

# CHỈ đăng item khớp tiền tố này. Không có nó, `check` vừa cho thấy hàng đợi
# có 32 item chứ không phải 30 -- hai cái thừa là video DEMO dựng lúc thử
# nghiệm (mau-hop-menh-kim, huong-bep-quan-trong-hon). Chúng đã lọt vào
# hàng đợi qua sync_from_disk và sẽ bị đăng lên kênh thật.
#
# Hàng đợi là nơi mọi thứ dồn về, gồm cả thứ chỉ để thử. Bước đăng phải tự
# lọc, không được cho rằng mọi thứ trong hàng đợi đều đáng đăng.
SLUG_PREFIX = "lich-"


def _creds() -> dict:
    return json.loads(CREDS.read_text(encoding="utf-8"))


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
    print(f"sẵn sàng đăng: {len(rows)} item (khớp {SLUG_PREFIX!r})")
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
    if dl:
        print(f"đang hoãn chờ quota: {len(dl)} item, thử lại từ {dl[0]['retry_after']}")
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

    # Bỏ publishAt: dựng bản sao bundle với publish_at rỗng thì validate sẽ
    # chặn, nên can thiệp thẳng vào payload qua tham số của upload_video.
    tok = publish.access_token(_creds())
    print(f"đăng THỬ (private, KHÔNG hẹn giờ): {b.title}")
    print(f"  file: {row['video_path']}")

    import factory.publish as P
    orig = P.upload_video

    def _no_schedule(bundle, video_path, token):
        # Vá đúng một lần, chỉ trong lệnh probe: bỏ publishAt khỏi payload.
        real_meta = {}
        saved = P.json.dumps

        def spy(obj, *a, **kw):
            if isinstance(obj, dict) and "status" in obj:
                obj["status"].pop("publishAt", None)
                real_meta.update(obj)
            return saved(obj, *a, **kw)

        P.json.dumps = spy
        try:
            return orig(bundle, video_path, token)
        finally:
            P.json.dumps = saved

    vid = _no_schedule(b, Path(row["video_path"]), tok)
    print(f"\n  XONG. video_id = {vid}")
    print(f"  https://studio.youtube.com/video/{vid}/edit")
    print("  Video đang PRIVATE và KHÔNG có lịch -> sẽ không bao giờ tự công khai.")
    print("  Vào xem, kiểm hình/tiếng/mô tả. Đạt thì chạy `run`; không đạt thì xoá.")


def do_run(limit: int) -> None:
    creds = _creds()
    tok = publish.access_token(creds)
    tok_at = time.monotonic()
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

        for i, r in enumerate(rows, 1):
            b = store.load_bundle(r["channel"], r["slug"])
            # access_token sống 60 phút; 92 upload mất ~20 phút, nhưng lô
            # lớn hơn hoặc mạng chậm thì vượt -- làm mới trước khi hết hạn.
            if time.monotonic() - tok_at > 40 * 60:
                tok, tok_at = publish.access_token(creds), time.monotonic()
            try:
                res = publish.publish_bundle(b, Path(r["video_path"]), creds,
                                             token=tok, known_titles=titles)
                store.mark(conn, b.id, "published", video_id=res.video_id)
                print(f"  [{i}/{len(rows)}] {b.slug}  {res.url}  hẹn {res.scheduled_at}")
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


if MODE == "check":
    do_check()
elif MODE == "probe":
    do_probe(sys.argv[2] if len(sys.argv) > 2 else "lich-20261001")
elif MODE == "run":
    lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 500
    do_run(lim)
else:
    sys.exit(__doc__)
