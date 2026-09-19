"""Khung viết kịch bản Short — và bộ chấm trước khi thu âm.

ĐIỂM CỐT LÕI, nhắc lại vì đây là chỗ dễ quên nhất:
kịch bản audio không cần "viết hay", nó cần NGHE HAY. Một câu đẹp trên giấy
có thể rất dở khi đọc thành tiếng.

Bảy kịch bản Lịch đầu tiên của tôi hỏng đúng ở đây. Chúng đúng dữ liệu, đủ
thông tin, nhưng viết như niên giám: "Ngày Canh Tuất, lịch cũ ghi Trực thu,
và danh sách việc hợp xoay quanh nạp tài với thu tất." Không ai nói thế.
Không có căng thẳng, không mở vòng lặp, không có khoảnh khắc trả thưởng.

CÔNG THỨC:
    Hook -> Context -> Tension -> Value -> Payoff -> CTA

Không phải sáu câu -- là sáu VAI TRÒ. Một short 20 giây có thể gộp Context
vào Hook, hoặc bỏ CTA. Nhưng nếu thiếu Tension thì người xem không có lý do
nghe tiếp, và thiếu Payoff thì họ thấy bị lừa.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# ─── Mười kỹ năng ─────────────────────────────────────────────────────────

SKILLS = (
    ("hook", "1–3 giây đầu phải cho một lý do cụ thể để xem tiếp"),
    ("story", "Nén mở–thân–kết vào 20–60 giây, vẫn có hình dáng câu chuyện"),
    ("copy", "Câu ngắn, rõ, có cảm xúc, kích thích tò mò"),
    ("retention", "Liên tục mở vòng lặp, chuyển ý, trả thưởng"),
    ("voice", "Viết như người đang NÓI, không phải như người đang viết"),
    ("rhythm", "Biết chỗ nào câu ngắn, chỗ nào ngắt nhịp, chỗ nào nhấn"),
    ("psychology", "Chạm đúng nỗi đau/mong muốn/tò mò của nhóm người xem này"),
    ("visual", "Lời phải dễ ghép với B-roll, caption, beat text"),
    ("compression", "Bỏ MỌI câu không đóng góp cho hook, chuyện, hoặc payoff"),
    ("cta", "Nếu cần, kết tự nhiên — không phải giọng quảng cáo"),
)

# ─── Dấu hiệu văn viết lọt vào lời nói ────────────────────────────────────
#
# Đây là những cụm tôi thật sự đã dùng trong 7 kịch bản đầu. Chúng đọc lên
# nghe như đang đọc tài liệu, không như đang kể cho ai nghe.

BOOKISH = (
    r"\bdanh sách\b", r"\bbao gồm\b", r"\bgồm có\b", r"\bnói chung\b",
    r"\bcác loại\b", r"\bđược xem là\b.*\bnhóm\b", r"\bthuộc về\b",
    r"\bxoay quanh\b", r"\bnói nôm na\b", r"\btức là\b.*\btức là\b",
    r"\bvà vài việc\b", r"\bvà cả\b.*\bchỉ gồm\b",
)

# Câu quá dài đọc lên bị hụt hơi. 22 từ là mốc tôi lấy từ chính 7 kịch bản
# hỏng: những câu vượt mốc này đều là câu nghe nặng nhất.
MAX_WORDS_PER_SENTENCE = 22
HOOK_MAX_WORDS = 14

_SENT = re.compile(r"(?<=[.!?…])\s+")


@dataclass
class Check:
    ok: bool
    note: str


def split_sentences(script: str) -> list[str]:
    return [s.strip() for s in _SENT.split(script.strip()) if s.strip()]


def review(script: str) -> list[Check]:
    """Chấm một kịch bản TRƯỚC KHI thu âm.

    Chỉ kiểm được thứ đo được -- nhịp, độ dài, dấu hiệu văn viết, lặp từ.
    Hook có hay không, chuyện có cuốn không thì vẫn phải người đọc lên và
    nghe. Bộ này để loại bản rõ ràng hỏng, không để phong bản hay."""
    out: list[Check] = []
    sents = split_sentences(script)

    if not sents:
        return [Check(False, "kịch bản rỗng")]

    hook_words = len(sents[0].split())
    out.append(Check(hook_words <= HOOK_MAX_WORDS,
                     f"hook {hook_words} từ (tối đa {HOOK_MAX_WORDS}) — quá dài thì "
                     "điểm nhấn tới sau giây thứ 3"))

    long_ones = [s for s in sents if len(s.split()) > MAX_WORDS_PER_SENTENCE]
    out.append(Check(not long_ones,
                     f"{len(long_ones)} câu dài quá {MAX_WORDS_PER_SENTENCE} từ — "
                     "đọc lên bị hụt hơi" if long_ones else "độ dài câu ổn"))

    found = [p for p in BOOKISH if re.search(p, script, re.I)]
    out.append(Check(not found,
                     f"{len(found)} cụm văn viết lọt vào — nghe như đọc tài liệu"
                     if found else "không có cụm văn viết"))

    # Nhịp: cần TRỘN câu ngắn và câu dài. Toàn câu đều đều nghe như máy đọc.
    lens = [len(s.split()) for s in sents]
    spread = max(lens) - min(lens)
    out.append(Check(spread >= 6,
                     f"chênh lệch dài/ngắn chỉ {spread} từ — nhịp phẳng, thêm một "
                     "câu thật ngắn để tạo nhấn" if spread < 6 else f"nhịp có biến thiên ({spread} từ)"))

    # Câu cuối phải vọng lại câu đầu -- đóng vòng lặp đã mở.
    first_words = {w.lower().strip(".,!?") for w in sents[0].split() if len(w) > 3}
    last_words = {w.lower().strip(".,!?") for w in sents[-1].split() if len(w) > 3}
    out.append(Check(bool(first_words & last_words),
                     "câu cuối không vọng lại từ nào của hook — vòng lặp chưa đóng"
                     if not (first_words & last_words) else "câu cuối đóng vòng lặp"))

    return out


def report(script: str, label: str = "") -> str:
    checks = review(script)
    head = f"{label}  {'ĐẠT' if all(c.ok for c in checks) else 'CẦN SỬA'}"
    body = "\n".join(f"   {'ok ' if c.ok else '>> '}{c.note}" for c in checks)
    return f"{head}\n{body}"
