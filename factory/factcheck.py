"""Đối chiếu kịch bản Lịch với nguồn — Fact, Logic, Hook, Chốt, Ngày tháng.

VÌ SAO TỰ ĐỘNG HOÁ: đọc lại bằng mắt thì bỏ lọt. Ba claim sai đã lọt qua
đúng như vậy trong bản trước, và cả ba đều nghe rất thuyết phục:

    "Sáu ngày nữa mới lại có ngày như ngày mai"
        -> Trực thành rơi vào 02, 18, 30/10. Cách 16 ngày, không phải 6.
    "Trực nguy, tầng hẹp nhất trong mười hai trực"
        -> Sai. Trực định/chấp/phá chỉ có 1 việc; Trực nguy có 3.
    "Bạch Hổ, sao bị kiêng nhiều nhất"
        -> Nguồn không hề có thông tin này. Tự thêm.

Cả ba đều là SUY DIỄN nghe như dữ kiện. Đó là dạng sai nguy hiểm nhất với
nội dung lịch: người xem tin và làm theo.

BỘ NÀY KIỂM ĐƯỢC GÌ: tên sao, tên trực, tên việc, con số đếm được, và ngày
tháng. Tức là phần ĐỐI CHIẾU ĐƯỢC với nguồn.

KHÔNG KIỂM ĐƯỢC GÌ: hook có cuốn không, chốt có sắc không, giọng có đúng
chất kênh không. Những thứ đó vẫn phải người đọc lên và nghe.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from factory.claims import check_declared, check_statistics
from factory.lunar import DayFacts

# 12 sao hoàng đạo/hắc đạo. Dùng để bắt trường hợp kịch bản nhắc TÊN SAO
# của một ngày khác -- lỗi dễ xảy ra khi viết hàng loạt rồi copy nhầm.
ALL_GODS = (
    "Thanh Long", "Minh Đường", "Kim Quỹ", "Ngọc Đường", "Thiên Đức", "Tư Mệnh",
    "Bạch Hổ", "Chu Tước", "Câu Trần", "Huyền Vũ", "Thiên Hình", "Thiên Lao",
)
ALL_TRUC = (
    "Trực kiến", "Trực trừ", "Trực mãn", "Trực bình", "Trực định", "Trực chấp",
    "Trực phá", "Trực nguy", "Trực thành", "Trực thu", "Trực khai", "Trực bế",
)

# Số viết bằng chữ -> số. Kịch bản nói "ba việc", phải khớp len(good_for).
WORD_NUM = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6,
            "bảy": 7, "tám": 8, "chín": 9, "mười": 10}

# Từ khẳng định tuyệt đối -- nội dung lịch không đủ căn cứ cho mức này.
ABSOLUTE = (r"\bchắc chắn\b", r"\btuyệt đối\b", r"\bnhất định\b",
            r"\bbảo đảm\b", r"\bluôn luôn\b", r"\bkhông bao giờ sai\b")

# Cụm so sánh nhất -- gần như luôn là suy diễn trừ khi đã đếm toàn bộ.
SUPERLATIVE = (r"\bnhất trong\b", r"\bhẹp nhất\b", r"\brộng nhất\b",
               r"\bnhiều nhất\b", r"\bít nhất trong\b", r"\bduy nhất\b")

MIN_WORDS, MAX_WORDS = 65, 85
_SENT = re.compile(r"(?<=[.!?…])\s+")


def _norm(s: str) -> str:
    """Bỏ dấu + thường hoá, để so khớp tên việc không phụ thuộc cách gõ."""
    d = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in d if not unicodedata.combining(c))


@dataclass
class Finding:
    ok: bool
    area: str      # FACT | LOGIC | HOOK | CHỐT | NGÀY
    msg: str


def check(script: str, facts: DayFacts, publish_at: str) -> list[Finding]:
    out: list[Finding] = []
    sents = [s.strip() for s in _SENT.split(script.strip()) if s.strip()]
    low = script.lower()

    # ─── NGÀY: bất biến quan trọng nhất ───────────────────────────────────
    # Video đăng D-1 lúc 6h sáng. Người xem nghe "ngày mai" -> phải đúng
    # bằng ngày lịch đang nói tới. Sai chỗ này là người xem làm theo giờ
    # tốt/việc hợp vào NHẦM NGÀY.
    pub = datetime.strptime(publish_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    viewer_day = (pub + timedelta(hours=7)).date()      # giờ VN
    says_tomorrow = "ngày mai" in low or " mai " in low
    if says_tomorrow:
        out.append(Finding(
            viewer_day + timedelta(days=1) == facts.target, "NGÀY",
            f"xưng 'ngày mai'; người xem nghe ngày {viewer_day}, "
            f"ngày mai của họ = {viewer_day + timedelta(days=1)}, "
            f"lịch nói về {facts.target}"))
    else:
        out.append(Finding(False, "NGÀY",
                           "không xưng 'ngày mai' — video đăng trước một ngày nên "
                           "phải nói rõ đang nói về ngày nào"))
    if "hôm nay" in low:
        out.append(Finding(False, "NGÀY", "có chữ 'hôm nay' — sai, video đăng trước một ngày"))

    # ─── FACT: sao ────────────────────────────────────────────────────────
    named = [g for g in ALL_GODS if g.lower() in low]
    out.append(Finding(named == [facts.god_name], "FACT",
                       f"sao nhắc trong bài {named or '(không nhắc)'} — nguồn ghi {facts.god_name}"))
    # Nhãn hoàng đạo/hắc đạo phải khớp loại sao.
    if "hoàng đạo" in low and not facts.is_auspicious_star:
        out.append(Finding(False, "FACT", f"gọi là hoàng đạo nhưng {facts.god_name} là sao hắc đạo"))
    if "hắc đạo" in low and facts.is_auspicious_star:
        out.append(Finding(False, "FACT", f"gọi là hắc đạo nhưng {facts.god_name} là sao hoàng đạo"))

    # ─── FACT: trực ───────────────────────────────────────────────────────
    truc_named = [t for t in ALL_TRUC if t.lower() in low]
    out.append(Finding(truc_named == [facts.truc_name], "FACT",
                       f"trực nhắc trong bài {truc_named or '(không nhắc)'} — nguồn ghi {facts.truc_name}"))

    # ─── FACT: tên việc phải có trong nguồn ───────────────────────────────
    src = _norm(" | ".join(list(facts.truc_good_for) + list(facts.truc_bad_for)))
    # Chỉ soi những cụm đặc thù của lịch, không soi từ đời thường.
    LICH_TERMS = ("an sàng", "an phủ biên cảnh", "tuyển tướng", "nhập học",
                  "trúc đê phòng", "khai trương", "tiến người", "nạp tài",
                  "bắt bớ", "thu tất", "tế tự", "cầu phúc", "cầu tự",
                  "xuất hành", "di chuyển", "động thổ", "san nền", "đắp lỗ",
                  "sửa tường", "giải trừ", "tắm gội", "chỉnh dung", "cạo đầu",
                  "cầu y trị bệnh", "quét dọn nhà cửa", "khởi công")
    bogus = [t for t in LICH_TERMS if t in low and _norm(t) not in src]
    out.append(Finding(not bogus, "FACT",
                       f"việc nhắc nhưng KHÔNG có trong nguồn: {bogus}" if bogus
                       else "mọi tên việc đều có trong nguồn"))

    # ─── LOGIC: con số đếm được ───────────────────────────────────────────
    n_good = len(facts.truc_good_for)
    n_bad = len(facts.truc_bad_for)
    # CHỈ soi khi con số thật sự là MỘT KHẲNG ĐỊNH về danh mục của ngày.
    # Bản đầu bắt mọi cụm "<số> việc" và báo sai hai chỗ hoàn toàn hợp lệ:
    # "Cùng một việc, lịch đổi ý theo ngày" và "ba việc đầu là tế tự...".
    # Cả hai không phải claim về số lượng danh mục.
    claims = (
        (r"(?:cho làm|nên làm|danh mục|vỏn vẹn)\s+(?:đúng\s+|cả\s+)?(\w+)\s+việc", n_good, "good_for"),
        (r"(?:chỉ|đúng)\s+cho\s+làm\s+(?:đúng\s+)?(\w+)\s+việc", n_good, "good_for"),
        (r"cả\s+(\w+)\s+việc\s+lịch\s+cho\s+làm", n_good, "good_for"),
        (r"(\w+)\s+việc\s+nên\s+làm", n_good, "good_for"),
        (r"kiêng\s+(?:đúng\s+)?(\w+)\s+việc", n_bad, "bad_for"),
    )
    for pat, actual, label in claims:
        for m in re.finditer(pat, low):
            w = m.group(1)
            if w in WORD_NUM:
                out.append(Finding(WORD_NUM[w] == actual, "LOGIC",
                                   f"nói '{w} việc' ({label}) — nguồn có {actual}"))

    # ─── LOGIC: khẳng định tuyệt đối / so sánh nhất ───────────────────────
    abs_hits = [p for p in ABSOLUTE if re.search(p, low)]
    out.append(Finding(not abs_hits, "LOGIC",
                       f"khẳng định tuyệt đối: {abs_hits}" if abs_hits
                       else "không khẳng định tuyệt đối"))
    sup_hits = [p for p in SUPERLATIVE if re.search(p, low)]
    out.append(Finding(not sup_hits, "LOGIC",
                       f"so sánh nhất (phải đếm toàn bộ lịch mới được nói): {sup_hits}"
                       if sup_hits else "không so sánh nhất chưa kiểm chứng"))

    # ─── HOOK ─────────────────────────────────────────────────────────────
    hook = sents[0] if sents else ""
    hw = len(hook.split())
    out.append(Finding(3 <= hw <= 16, "HOOK", f"hook {hw} từ (cần 3–16)"))
    paradox = any(k in hook.lower() for k in
                  ("nhưng", "mà", "vừa", "vẫn", "chỉ", "không"))
    out.append(Finding(paradox, "HOOK",
                       "hook có yếu tố nghịch lý/giới hạn" if paradox
                       else "hook phẳng — chưa có nghịch lý hay giới hạn nào"))

    # ─── CHỐT ─────────────────────────────────────────────────────────────
    closer = sents[-1] if sents else ""
    cw = len(closer.split())
    out.append(Finding(cw <= 16, "CHỐT", f"chốt {cw} từ (cần ≤16 để dễ nhớ)"))

    # ─── NGOÀI NGUỒN: diễn giải phải khai báo, thống kê phải đếm lại ──────
    #
    # LUẬT: chỉ ĐẠT khi MỌI claim ngoài dữ liệu nguồn đã được xác minh. Một
    # câu suy diễn thành fact, hoặc một thống kê chưa kiểm toàn bộ dữ liệu,
    # đều phải CẦN SỬA. Phần trên chỉ soi được thứ CÓ trong nguồn -- hai
    # hàm dưới soi đúng thứ người viết TỰ THÊM VÀO, vốn là chỗ ba claim sai
    # trước đây đã lọt qua.
    for c in check_declared(script):
        out.append(Finding(c.ok, "NGOÀI", c.msg))
    for c in check_statistics(script, facts.target):
        out.append(Finding(c.ok, "THỐNG KÊ", c.msg))

    # ─── Độ dài ───────────────────────────────────────────────────────────
    total = len(script.split())
    out.append(Finding(MIN_WORDS <= total <= MAX_WORDS, "LOGIC",
                       f"{total} từ (cần {MIN_WORDS}–{MAX_WORDS})"))
    return out


def report(script: str, facts: DayFacts, publish_at: str, label: str = "") -> tuple[bool, str]:
    fs = check(script, facts, publish_at)
    ok = all(f.ok for f in fs)
    head = f"{label}  {'ĐẠT' if ok else 'CHƯA ĐẠT'}"
    body = "\n".join(f"   [{f.area:8s}] {'ok ' if f.ok else '>> '}{f.msg}" for f in fs)
    return ok, f"{head}\n{body}"
