"""Đưa item về lại pending để chạy lại từ đầu.

Dùng khi sửa kịch bản trong Bundle: bản ghi trạng thái vẫn nhớ item đã
spoken/assembled nên hàng đợi bỏ qua nó. Bundle.id suy từ (channel, kind,
slug) chứ không băm script -- cố ý, để sửa câu chữ không đẻ ra content item
mới -- nên phải nói rõ là muốn làm lại.

    python scripts/reset_items.py "lich-2026%"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from factory import store  # noqa: E402

# LỖI THẬT (21/09/2026): bản trước mặc định pattern "%" khi không có tham
# số. Một lần gọi quên tham số đưa CẢ 102 item về pending, kể cả 92 video
# ĐÃ ĐĂNG -- lần chạy đăng kế tiếp sẽ upload trùng toàn bộ kênh. Giờ: bắt
# buộc có pattern, và không bao giờ đụng item đã có video_id trên YouTube.
if len(sys.argv) < 2 or sys.argv[1].strip() in ("", "%", "*"):
    sys.exit("Phải ghi rõ pattern, vd: python scripts/reset_items.py \"giap-%\" "
             "(không cho reset tất cả).")
pattern = sys.argv[1]
with store.connect() as conn:
    cur = conn.execute(
        "UPDATE item SET stage = 'pending', attempts = 0, error = NULL "
        "WHERE slug LIKE ? AND video_id IS NULL",
        (pattern,),
    )
    print(f"reset {cur.rowcount} item khớp {pattern!r}")
    print("trạng thái:", store.summary(conn))
