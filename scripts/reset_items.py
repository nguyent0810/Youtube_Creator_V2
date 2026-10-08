"""Đưa item về lại pending để chạy lại từ đầu.

Dùng khi sửa kịch bản trong Bundle: bản ghi trạng thái vẫn nhớ item đã
spoken/assembled nên hàng đợi bỏ qua nó. Bundle.id suy từ (channel, kind,
slug) chứ không băm script -- cố ý, để sửa câu chữ không đẻ ra content item
mới -- nên phải nói rõ là muốn làm lại.

    python scripts/reset_items.py "lich-2026%" --channel FS
    python scripts/reset_items.py "giap-%" --channel FS --dry

KHÔNG BAO GIỜ đụng item đã có video_id trên YouTube.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from factory import channels, store  # noqa: E402

# LỖI THẬT (21/09/2026): bản đầu mặc định pattern "%" khi không có tham số.
# Một lần gọi quên tham số đưa CẢ 102 item về pending, kể cả 92 video ĐÃ ĐĂNG.
# Bản sau chỉ chặn "", "%", "*" -- nhưng "%%", "_%", "%-%" vẫn khớp MỌI item
# của cả 3 kênh (audit 08/10/2026). Giờ:
#   - bắt buộc --channel, chỉ đụng item của kênh đó;
#   - pattern phải có ít nhất 3 ký tự chữ/số (một tiền tố thật);
#   - không hồi sinh item bị LOẠI vì nội dung (attempts >= 99), trừ khi
#     --include-rejected;
#   - không đẩy dòng chỉ-đăng-lẻ (S-tier) về pending: chúng có pipeline dựng
#     riêng, đi qua TTS + Pexels chung là ra một video khác hẳn.
CH = channels.pick(required=True)
ARGS = [a for a in channels.args_without_channel() if not a.startswith("--")]
if not ARGS or len(re.sub(r"[^0-9A-Za-z]", "", ARGS[0])) < 3:
    sys.exit("Phải ghi rõ pattern có ít nhất 3 ký tự chữ/số, vd: "
             "python scripts/reset_items.py \"giap-%\" --channel FS (không cho reset tất cả).")
pattern = ARGS[0]
include_rejected = "--include-rejected" in sys.argv
drip = channels.drip_only(CH)

with store.connect() as conn:
    rows = [dict(r) for r in conn.execute(
        "SELECT id, slug, stage, attempts FROM item WHERE channel = ? AND slug LIKE ? AND video_id IS NULL",
        (CH, pattern))]
    skip_rej = [r["slug"] for r in rows if r["attempts"] >= 99 and not include_rejected]
    skip_drip = [r["slug"] for r in rows if drip and r["slug"].startswith(drip)]
    todo = [r for r in rows if r["slug"] not in skip_rej and r["slug"] not in skip_drip]
    if skip_rej:
        print(f"giữ nguyên {len(skip_rej)} item đã bị LOẠI (thêm --include-rejected nếu chắc): {skip_rej[:8]}")
    if skip_drip:
        print(f"giữ nguyên {len(skip_drip)} item dòng chỉ-đăng-lẻ {drip}: dựng lại bằng motion/stier")
    if "--dry" in sys.argv:
        print(f"CHẠY KHÔ: sẽ reset {len(todo)} item khớp {pattern!r} ({CH}): {[r['slug'] for r in todo[:10]]}")
        sys.exit(0)
    for r in todo:
        conn.execute("UPDATE item SET stage = 'pending', attempts = 0, error = NULL, retry_after = NULL, "
                     "fail_stage = NULL, script_sha = NULL WHERE id = ?", (r["id"],))
    print(f"reset {len(todo)} item khớp {pattern!r} ({CH})")
    print("trạng thái:", store.summary(conn))
