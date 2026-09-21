"""Sinh 4 Short pillar cho MỘT ngày đăng — cùng khuôn với make_lich_month.

    python scripts/make_pillars_day.py 2026-09-30          # ngày đăng (giờ VN)
    python scripts/make_pillars_day.py 2026-09-30 --dry    # chỉ in, không ghi
    python scripts/make_pillars_day.py 2026-10-01 31       # 31 ngày × 4 = 124 bundle

Mỗi pillar lấy chủ đề kế tiếp chưa làm (lịch sử đọc từ bundles/). Bản nào
không qua bộ kiểm thì KHÔNG ghi ra -- fail-closed như Lịch. Sau đó kiểm chéo
cả 4 bản với nhau và với toàn bộ lịch sử (batchcheck), trượt thì dừng.
"""
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.batchcheck import report_batch  # noqa: E402
from factory.bundle import Bundle, make_slug  # noqa: E402
from factory.pillars import check as C  # noqa: E402
from factory.pillars import topics as P  # noqa: E402

# Bốn cảm giác khác nhau -> giọng + nhạc khác nhau.
STYLE = {
    "giap": ("Minh Quân Pro", "thinking_music.mp3"),
    "tru":  ("Anh Khôi", "deliberate_thought.mp3"),
    "dich": ("Thiền Tâm Đức", "meditation_impromptu_02.mp3"),
    "menh": ("Thục Đoan", "comfortable_mystery_4.mp3"),
}
TAGS = {
    "giap": ["12 con giap", "tuoi xung", "luc xung", "phong thuy"],
    "tru":  ["tu tru", "bat tu", "menh ly", "nhat chu", "thap than"],
    "dich": ["kinh dich", "64 que", "chu dich", "triet ly phuong dong"],
    "menh": ["cung hoang dao", "chiem tinh", "huyen hoc", "thien van"],
}
VN_UTC = timedelta(hours=7)

start = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today() + timedelta(days=1)
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 1
DRY = "--dry" in sys.argv
QUIET = DAYS > 1

history = P.load_history(store.BUNDLE_DIR)
made, blocked = [], []
done_slugs = {f.stem for f in (store.BUNDLE_DIR / "FS").glob("*.json")}
# Mỗi dòng đúng MỘT bài mỗi ngày: ngày nào dòng đó đã có bài thì bỏ qua
# (chạy lại cùng dải ngày phải vô hại, không đẻ bài thứ hai).
have = {(h["pillar"], h["publish_at"]) for h in history}
kept = 0
for n in range(DAYS):
    day = start + timedelta(days=n)
    for pillar, (prefix, hhmm, feel) in P.PILLARS.items():
        hh, mm = map(int, hhmm.split(":"))
        slot = (datetime(day.year, day.month, day.day, hh, mm) - VN_UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        if (pillar, slot) in have:
            kept += 1
            continue
        d, why = P.next_draft(pillar, history, day)
        if d is None:
            blocked += [f"{day}: {w}" for w in why]
            continue
        findings = C.check(d, P.ALL_NAMES, history)
        ok = C.verdict(findings)
        h, m = map(int, hhmm.split(":"))
        when = (datetime(day.year, day.month, day.day, h, m) - VN_UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        voice, bgm = STYLE[pillar]
        b = Bundle(
            channel="FS", kind="short", slug=f"{prefix}{make_slug(d.key)}", script=d.script, title=d.title,
            description=d.title + ".\n\nNguồn: " + "; ".join(d.sources)
            + "\n\nKiến thức truyền thống, để tham khảo — không phải kết luận khoa học.",
            # Beat text cảnh đầu = tiêu đề (ngắn), không phải cả câu hook dài.
            tags=TAGS[pillar], thumbnail_text=d.title, publish_at=when, voice=voice, bgm=bgm,
            broll_queries=d.broll,
            source_note=f"pillar={pillar};key={d.key};angle={d.angle} | " + "; ".join(d.sources),
        )
        b.validate()
        made.append((pillar, hhmm, d, b, ok, findings))
        # Bản sau (cùng ngày hoặc ngày sau) phải khác bản trước -> vào lịch sử ngay.
        history.append({"pillar": pillar, "key": d.key, "angle": d.angle,
                        "script": d.script, "publish_at": when})

if not made:
    print(f"Không có bài mới (giữ nguyên {kept} slot đã có).")
    sys.exit(0)
ok_batch, batch_text = report_batch([b for *_, b, _, _ in made], label="LÔ 4 PILLAR")
if any(not ok for *_, ok, _ in made) or not ok_batch:
    print(batch_text)
    for p, hhmm, d, b, ok, f in made:
        print(f"{p} {'ĐẠT' if ok else 'CẦN SỬA'}")
        for x in f:
            if not x.ok:
                print("   >>", x.area, x.msg)
    sys.exit("DỪNG: có bản không qua kiểm. Không ghi gì.")

for p, hhmm, d, b, ok, f in ([] if QUIET else made):
    print(f"\n[{d.title}]  {hhmm} · {STYLE[p][0]}")
    print(f"`{b.slug}` · {b.word_count} từ · chấm: ĐẠT")
    print(d.script)
    print("Nguồn: " + "; ".join(d.sources))
    print("B-roll: " + ", ".join(d.broll))
    print("Kiểm: " + " · ".join(f"{x.area}" for x in f if x.ok) + f" ({len(f)}/{len(f)})")
if QUIET:
    for p, hhmm, d, b, ok, f in made:
        print(f"  {b.publish_at}  {b.slug:22s} {b.word_count:3d} từ  {d.angle}")
print()
print(batch_text)
if blocked:
    print("\nCHẶN (thiếu nguồn):", *blocked, sep="\n  ")

if not DRY:
    for *_, b, _, _ in made:
        store.save_bundle(b)
    with store.connect() as conn:
        added, total = store.sync_from_disk(conn, channel="FS")
    print(f"\nGhi {len(made)} bundle mới, giữ nguyên {kept} slot đã có, hàng đợi thêm {added}")
