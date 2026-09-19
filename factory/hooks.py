"""Thư viện hook — 3 giây đầu quyết định người xem lướt tiếp hay dừng lại.

Đây là TÀI SẢN NỘI DUNG, không phải code hạ tầng. Nó sống ở pha sinh (trong
chat), và mục đích là để Claude có một bộ khuôn tường minh để chọn và đối
chiếu, thay vì mỗi lần lại tự nhớ ra "hook nên hay".

VÌ SAO CẦN: bộ luật retention của v1 phủ rất kỹ MỘT chiều -- nhịp độ và mật
độ thông tin (hook <=12 từ, câu cuối vọng lại hook, mọi câu giữa phải mang
giá trị mới). Không luật nào nói về CẢM XÚC hay CĂNG THẲNG. Đó là lý do kịch
bản đọc "đúng" mà không "cuốn": viết chặt, đi thẳng, và phẳng.

RANH GIỚI ĐẠO ĐỨC (giữ nguyên tiêu chuẩn từ NARRATIVE_PATTERN_LIBRARY của
dự án): giữ chân người xem phải đến từ trí tuệ, chiêm nghiệm, sự thật cảm
xúc, lòng trắc ẩn, tò mò và một câu chuyện mạch lạc -- KHÔNG BAO GIỜ từ sợ
hãi, gây sốc rỗng, cảm giác tội lỗi hay sự cấp bách giả tạo.

Mở một vòng lặp rồi đóng nó tử tế là hợp lệ. Giấu thông tin để câu view thì
không. Khác biệt nằm ở chỗ: sau khi xem xong, người ta có nhận được đúng thứ
đã hứa không.
"""
from __future__ import annotations

from dataclasses import dataclass

# Kênh nào KHÔNG được dùng kiểu hook nào. Đây là ràng buộc nội dung thật,
# không phải sở thích: Phật giáo dùng hook gây sốc là phản lại chính nội
# dung; Hình Sự dùng hook khoe số liệu cá nhân là lạc giọng kênh.
@dataclass(frozen=True)
class Hook:
    key: str
    name: str
    what: str            # cơ chế tâm lý
    how: str             # cách viết câu đầu
    example: str         # ví dụ ĐÚNG NGÁCH, không phải ví dụ chung chung
    avoid_on: tuple      # kênh không nên dùng
    trap: str            # cách hỏng thường gặp của chính kiểu này


HOOKS: tuple[Hook, ...] = (
    Hook(
        key="pain_question",
        name="Câu hỏi xoáy vào nỗi đau",
        what="Người xem thấy CHÍNH MÌNH trong câu hỏi nên không lướt được.",
        how="Nêu thẳng vấn đề họ đang gặp, ở dạng câu hỏi, không rào đón.",
        example="Bàn làm việc quay hướng này, sao mãi không thấy thuận?",
        avoid_on=(),
        trap="Hỏi quá rộng ('Bạn có tin phong thuỷ không?') -- không ai thấy mình trong đó.",
    ),
    Hook(
        key="counterintuitive",
        name="Phản trực giác",
        what="Phá một lầm tưởng phổ biến, tạo khoảng hẫng buộc phải nghe tiếp.",
        how="Nói ngược điều số đông tin, rồi giải thích ngay -- không treo lâu.",
        example="Gương đối diện cửa không phải lúc nào cũng xấu.",
        avoid_on=("BUD",),
        trap="Nói ngược mà không có căn cứ -> thành giật tít. Phải giải thích được.",
    ),
    Hook(
        key="number_result",
        name="Con số / kết quả ngay",
        what="Cụ thể hoá ngay lập tức, não bám vào con số nhanh hơn khái niệm.",
        how="Đưa số liệu hoặc mốc cụ thể vào câu đầu.",
        example="Có đúng 5 khung giờ trong ngày mai được xem là giờ hoàng đạo.",
        avoid_on=(),
        trap="Con số bịa hoặc không kiểm chứng được -- sai số liệu là sai khách quan.",
    ),
    Hook(
        key="hidden_secret",
        name="Điều ít ai biết",
        what="Khoảng trống tò mò: hứa một thứ người xem chưa có.",
        how="Đóng khung là chi tiết bị bỏ qua, KHÔNG phải bí mật thần bí.",
        example="Hướng bếp mới là thứ quyết định, không phải hướng nhà.",
        avoid_on=(),
        trap="Hứa to rồi nội dung tầm thường -- lần sau người ta không tin nữa.",
    ),
    Hook(
        key="story_open",
        name="Mở bằng câu chuyện",
        what="Tình huống cụ thể kéo người nghe vào trước khi họ kịp đánh giá.",
        how="Bắt đầu giữa một cảnh đang xảy ra, không dẫn nhập.",
        example="Một gia đình đổi đúng một thứ trong bếp, và bữa cơm thay đổi hẳn.",
        avoid_on=(),
        trap="Kể lể quá lâu mới tới ý -- câu chuyện phải chạm chủ đề trong 3 giây.",
    ),
    Hook(
        key="empathy",
        name="Đồng cảm",
        what="Chạm vào trạng thái cảm xúc người xem đang ở trong đó.",
        how="Gọi tên cảm giác trước, rồi mới đến nội dung.",
        example="Có những ngày làm gì cũng thấy vướng, không rõ vì sao.",
        avoid_on=(),
        trap="Sến hoặc chung chung -- phải là cảm giác CỤ THỂ, nhận ra được.",
    ),
)

BY_KEY = {h.key: h for h in HOOKS}


def hooks_for(channel: str) -> tuple[Hook, ...]:
    """Hook hợp lệ cho một kênh."""
    ch = (channel or "").upper()
    return tuple(h for h in HOOKS if ch not in h.avoid_on)


def prompt_block(channel: str) -> str:
    """Khối tham chiếu để dán vào lúc soạn kịch bản.

    Trình bày dạng MENU chứ không phải khuôn bắt buộc: mỗi phương án chọn
    MỘT kiểu và làm tới nơi. Trộn nhiều kiểu trong một hook 12 từ thì không
    kiểu nào đủ mạnh."""
    lines = [f"HOOK — chọn ĐÚNG MỘT kiểu cho mỗi phương án (kênh {channel}):"]
    for h in hooks_for(channel):
        lines.append(f"\n[{h.key}] {h.name}")
        lines.append(f"  cơ chế : {h.what}")
        lines.append(f"  cách viết: {h.how}")
        lines.append(f"  ví dụ  : \"{h.example}\"")
        lines.append(f"  dễ hỏng: {h.trap}")
    lines.append(
        "\nRÀNG BUỘC CHUNG: câu đầu tối đa ~12 từ (đọc xong trong ~3 giây). "
        "Vào thẳng điểm nhấn, KHÔNG mở bằng mệnh đề phụ dài kiểu \"Trong khi X thì Y...\". "
        "Giữ chân phải đến từ tò mò và sự thật cảm xúc -- KHÔNG từ sợ hãi, gây sốc rỗng, "
        "tội lỗi hay cấp bách giả tạo. Sau khi xem xong, người ta phải nhận được đúng thứ đã hứa."
    )
    return "\n".join(lines)
