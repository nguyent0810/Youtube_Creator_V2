"""Sinh 4 Short pillar cho MỘT ngày đăng — cùng khuôn với make_lich_month.

    python scripts/make_pillars_day.py 2026-09-30          # ngày đăng (giờ VN)
    python scripts/make_pillars_day.py 2026-09-30 --dry    # chỉ in, không ghi

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
from factory.bundle import Bundle  # noqa: E402
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

day = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today() + timedelta(days=1)
DRY = "--dry" in sys.argv

history = P.load_history(store.BUNDLE_DIR)
made, blocked = [], []
for pillar, (prefix, hhmm, feel) in P.PILLARS.items():
    d, why = P.next_draft(pillar, history)
    if d is None:
        blocked += why
        continue
    findings = C.check(d, P.ALL_NAMES, history)
    ok = C.verdict(findings)
    h, m = map(int, hhmm.split(":"))
    when = (datetime(day.year, day.month, day.day, h, m) - VN_UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    voice, bgm = STYLE[pillar]
    b = Bundle(
        channel="FS", kind="short", slug=f"{prefix}{d.key}", script=d.script, title=d.title,
        description=d.title + ".\n\nNguồn: " + "; ".join(d.sources)
        + "\n\nKiến thức truyền thống, để tham khảo — không phải kết luận khoa học.",
        tags=TAGS[pillar], thumbnail_text="", publish_at=when, voice=voice, bgm=bgm,
        broll_queries=d.broll,
        source_note=f"pillar={pillar};key={d.key};angle={d.angle} | " + "; ".join(d.sources),
    )
    b.validate()
    made.append((pillar, hhmm, d, b, ok, findings))
    # Bản sau trong cùng ngày cũng phải khác bản trước -> đưa vào lịch sử ngay.
    history.append({"pillar": pillar, "key": d.key, "angle": d.angle,
                    "script": d.script, "publish_at": when})

ok_batch, batch_text = report_batch([b for *_, b, _, _ in made], label="LÔ 4 PILLAR")
if any(not ok for *_, ok, _ in made) or not ok_batch:
    print(batch_text)
    for p, hhmm, d, b, ok, f in made:
        print(f"{p} {'ĐẠT' if ok else 'CẦN SỬA'}")
        for x in f:
            if not x.ok:
                print("   >>", x.area, x.msg)
    sys.exit("DỪNG: có bản không qua kiểm. Không ghi gì.")

for p, hhmm, d, b, ok, f in made:
    print(f"\n[{d.title}]  {hhmm} · {STYLE[p][0]}")
    print(f"`{b.slug}` · {b.word_count} từ · chấm: ĐẠT")
    print(d.script)
    print("Nguồn: " + "; ".join(d.sources))
    print("B-roll: " + ", ".join(d.broll))
    print("Kiểm: " + " · ".join(f"{x.area}" for x in f if x.ok) + f" ({len(f)}/{len(f)})")
print()
print(batch_text)
if blocked:
    print("\nCHẶN (thiếu nguồn):", *blocked, sep="\n  ")

if not DRY:
    for *_, b, _, _ in made:
        store.save_bundle(b)
    with store.connect() as conn:
        added, total = store.sync_from_disk(conn, channel="FS")
    print(f"\nGhi {len(made)} bundle, hàng đợi thêm {added}")
