"""Sinh Bundle Lịch cho N ngày liên tiếp — tự động, không người can thiệp.

    python scripts/make_lich_month.py 2026-10-01 30

Mọi câu đều từ vnlunar + factory/vocab.py. Không LLM, không viết tay. Chạy
lại bao nhiêu lần cũng ra y hệt (khuôn chọn theo ngày, tất định).

Bundle nào KHÔNG qua được bộ đối chiếu thì KHÔNG được ghi ra -- fail-closed.
Thà thiếu một ngày còn hơn đăng một ngày sai, vì người xem làm theo.
"""
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402
from factory.compose import script_for  # noqa: E402
from factory.batchcheck import report_batch  # noqa: E402
from factory.factcheck import report  # noqa: E402
from factory.lunar import facts_range  # noqa: E402
from factory.vocab import broll_for  # noqa: E402

VOICE = "Anh Khôi"
BGM = "asian_drums.mp3"

# B-roll theo THẾ của ngày, không theo từng ngày: thế quyết định tông của
# kịch bản (siết / mở / cùng thuận / cùng đóng) nên hình cũng nên theo đó.
BROLL = {
    "sao_mo_truc_siet": ["calm vietnamese home interior", "wooden door closed detail",
                         "morning light through window", "quiet traditional house"],
    "sao_du_truc_mo":   ["open road sunrise vietnam", "busy market morning",
                         "hands counting money", "wooden gate opening"],
    "cung_dong":        ["repairing wall plaster hands", "closed wooden shutters",
                         "cement trowel work detail", "quiet empty room"],
    "cung_thuan":       ["vietnamese shop opening morning", "sunrise over rice field",
                         "incense smoke altar close up", "warm home interior daylight"],
}

start = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date(2026, 10, 1)
days = int(sys.argv[2]) if len(sys.argv) > 2 else 30

made, skipped = [], []
for f in facts_range(start, days):
    sc = script_for(f)
    ok, text = report(sc["script"], f, f.publish_at, label=str(f.target))
    if not ok:
        skipped.append((f.target, text))
        continue
    b = Bundle(
        channel="FS", kind="short", slug=f.slug,
        script=sc["script"],
        title=sc["title"],
        description=(
            f"Lịch ngày {f.target.strftime('%d/%m/%Y')} — âm lịch {f.lunar_day}/{f.lunar_month}, "
            f"ngày {f.can_chi_day}, sao {f.god_name}, {f.truc_name}.\n"
            f"Nên làm: {', '.join(f.truc_good_for)}.\n"
            f"Kiêng: {', '.join(f.truc_bad_for)}.\n\n"
            "Ghi chép theo lịch pháp truyền thống, để tham khảo."
        ),
        tags=["phong thuy", "lich van nien", "ngay tot", "lich am"],
        thumbnail_text="",
        publish_at=f.publish_at,
        voice=VOICE, bgm=BGM,
        # Hình bám DANH MỤC VIỆC THẬT của ngày, không bám thế: chỉ có 4
        # thế nên 61 video trước đó dùng chung đúng 4 bộ từ khoá.
        broll_queries=broll_for(f.truc_good_for, BROLL[sc["the"]],
                                offset=f.target.day),
        source_note=f"vnlunar {f.target}: {f.can_chi_day}, sao {f.god_name}, {f.truc_name}",
    )
    store.save_bundle(b)
    made.append((f, b, sc["the"]))

# KIỂM CHÉO CẢ LÔ trước khi đưa vào hàng đợi. Kiểm từng bundle riêng lẻ
# không bao giờ thấy tiêu đề trùng -- lỗi đó đã làm mất 9 video.
ok_batch, batch_text = report_batch([b for _, b, _ in made], label="LÔ")
print(batch_text)
if not ok_batch:
    sys.exit("DỪNG: lô không qua kiểm chéo. Không đưa vào hàng đợi.")

with store.connect() as conn:
    added, total = store.sync_from_disk(conn, channel="FS")

print(f"Sinh {len(made)}/{days} bundle, hàng đợi thêm {added} (tổng {total})")
if skipped:
    print(f"\nBỎ QUA {len(skipped)} ngày không qua đối chiếu:")
    for d, t in skipped:
        print(t)
print()
for f, b, the in made:
    print(f"  {f.target}  {b.word_count:3d} từ  {the:18s}  {b.title[:52]}")
