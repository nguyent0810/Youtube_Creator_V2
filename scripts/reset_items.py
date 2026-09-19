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

pattern = sys.argv[1] if len(sys.argv) > 1 else "%"
with store.connect() as conn:
    cur = conn.execute(
        "UPDATE item SET stage = 'pending', attempts = 0, error = NULL WHERE slug LIKE ?",
        (pattern,),
    )
    print(f"reset {cur.rowcount} item khớp {pattern!r}")
    print("trạng thái:", store.summary(conn))
