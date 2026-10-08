"""Sinh Bundle Lịch cho N ngày liên tiếp — tự động, không người can thiệp.

    python scripts/make_lich_month.py 2027-01-01 31

Mọi câu đều từ factory/lunar.py (tính độc lập + đối chiếu kép với vnlunar)
và factory/vocab.py. Không LLM, không viết tay. Chạy lại bao nhiêu lần cũng
ra y hệt (khuôn chọn theo ngày, tất định).

Bundle nào KHÔNG qua được bộ đối chiếu thì KHÔNG được ghi ra -- fail-closed.
Thà thiếu một ngày còn hơn đăng một ngày sai, vì người xem làm theo.

GHI SAU KIỂM CHÉO LÔ (audit 08/10/2026): bản cũ ghi từng bundle ra đĩa TRƯỚC
khi kiểm chéo cả lô; lô trượt thì thoát nhưng file vẫn nằm đó, lần chạy sau
coi là "đã có", lô rỗng nên qua kiểm, rồi sync đưa tất cả vào hàng đợi. Giờ
cả lô sinh trong bộ nhớ, qua kiểm chéo rồi mới ghi.
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.batchcheck import report_batch  # noqa: E402
from factory.lich import CHANNEL, build_bundle  # noqa: E402
from factory.lunar import facts_range  # noqa: E402

if len(sys.argv) < 2:
    sys.exit(__doc__)
start = date.fromisoformat(sys.argv[1])
days = int(sys.argv[2]) if len(sys.argv) > 2 else 30

made, skipped, kept = [], [], []
for f in facts_range(start, days):
    # BẤT BIẾN: bundle đã có (có thể đã lên kênh) thì KHÔNG ghi đè. Khuôn câu
    # đổi theo thời gian; ghi đè sẽ làm bundle lệch với video đang ở trên
    # kênh (tiêu đề lệch -> verify báo sai, chống trùng theo tiêu đề hỏng).
    if (store.BUNDLE_DIR / CHANNEL / f"{f.slug}.json").exists():
        kept.append(f.slug)
        continue
    b, text, the = build_bundle(f)
    if b is None:
        skipped.append((f.target, text))
        continue
    made.append((f, b, the))

# KIỂM CHÉO CẢ LÔ trước khi đưa vào hàng đợi. Kiểm từng bundle riêng lẻ
# không bao giờ thấy tiêu đề trùng -- lỗi đó đã làm mất 9 video.
ok_batch, batch_text = report_batch([b for _, b, _ in made], label="LÔ") if made else (True, "LÔ  không có bundle mới")
print(batch_text)
if not ok_batch:
    sys.exit("DỪNG: lô không qua kiểm chéo. Không ghi bundle nào, không đưa vào hàng đợi.")

for _, b, _ in made:
    store.save_bundle(b)

with store.connect() as conn:
    added, total = store.sync_from_disk(conn, channel=CHANNEL)

print(f"Sinh {len(made)}/{days} bundle mới, giữ nguyên {len(kept)} đã có, hàng đợi thêm {added} (tổng {total})")
if skipped:
    print(f"\nBỎ QUA {len(skipped)} ngày không qua đối chiếu:")
    for d, t in skipped:
        print(t)
print()
for f, b, the in made:
    print(f"  {f.target}  {b.word_count:3d} từ  {the:18s}  {b.title[:52]}")
