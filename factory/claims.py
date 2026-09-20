"""Sổ đăng ký claim NGOÀI dữ liệu nguồn — và cách xác minh từng loại.

LUẬT (người dùng chốt 20/09/2026):
    Chỉ được đánh ĐẠT khi MỌI claim ngoài dữ liệu nguồn đã được xác minh.
    Một câu suy diễn thành fact, hoặc một thống kê chưa kiểm tra toàn bộ
    dữ liệu, đều phải CẦN SỬA.

VÌ SAO CẦN SỔ NÀY: bộ đối chiếu trước chỉ soi được thứ CÓ trong nguồn --
tên sao, tên trực, tên việc, số lượng danh mục. Nó hoàn toàn mù với thứ
người viết TỰ THÊM VÀO. Mà đó mới đúng là chỗ ba claim sai đã lọt qua:

    "Trực nguy, tầng hẹp nhất trong mười hai trực"   (thống kê chưa đếm)
    "Bạch Hổ, sao bị kiêng nhiều nhất"               (suy diễn thành fact)
    "Sáu ngày nữa mới lại có ngày như ngày mai"      (thống kê sai)

Ba loại claim, ba cách xử lý KHÁC NHAU:

  1. THỐNG KÊ  -- "cả tháng chỉ có ba ngày Trực thành", "sáu sao hắc đạo".
     Đếm lại được từ chính vnlunar. -> TỰ ĐỘNG đếm, không tin lời khai.

  2. DIỄN GIẢI -- "chữ bế nghĩa là bịt lại", "an sàng là kê giường".
     Không đếm được, nhưng kiểm chứng được bằng tra cứu. -> BẮT BUỘC khai
     báo trong sổ dưới đây kèm căn cứ. Không khai báo thì CẦN SỬA.

  3. SUY ĐOÁN  -- "sao này bị kiêng nhiều nhất", "người xưa thường tránh".
     Không đếm được, không tra được. -> KHÔNG ĐƯỢC DÙNG.

Sổ này cố ý bắt người viết phải GÕ RA căn cứ. Viết một câu diễn giải mất ba
giây; viết căn cứ cho nó mất lâu hơn -- và chính ma sát đó là thứ ngăn suy
diễn trôi vào kịch bản.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Declared:
    """Một claim ngoài nguồn, đã được khai báo kèm căn cứ."""
    claim: str       # cụm chữ xuất hiện trong kịch bản (đã chuẩn hoá)
    basis: str       # vì sao tin được
    kind: str        # "etymology" | "gloss" | "convention"


def _norm(s: str) -> str:
    d = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in d if not unicodedata.combining(c)).strip()


# ─── Sổ diễn giải đã khai báo ─────────────────────────────────────────────
#
# Mỗi mục là một câu KHÔNG có trong vnlunar nhưng kiểm chứng được. Thêm mục
# mới nghĩa là phải viết được căn cứ -- nếu không viết nổi thì đừng dùng câu
# đó trong kịch bản.

DECLARED: tuple[Declared, ...] = (
    Declared(
        "chữ lao nghĩa là nhà giam",
        "Thiên Lao 天牢: 牢 (lao) nghĩa gốc là chuồng/ngục. Nghĩa chữ Hán-Việt "
        "phổ thông, tra được trong mọi từ điển Hán-Việt. Không suy đoán về "
        "tác dụng của sao, chỉ dịch nghĩa TÊN.",
        "etymology",
    ),
    Declared(
        "chữ bế nghĩa là bịt lại",
        "Trực bế 閉: 閉 (bế) nghĩa là đóng/khép. Cùng chữ trong 'bế quan', "
        "'bế mạc'. Dịch nghĩa tên, không phán về hiệu lực.",
        "etymology",
    ),
    Declared(
        "chữ trừ nghĩa là bỏ bớt",
        "Trực trừ 除: 除 (trừ) nghĩa là bỏ đi/dọn đi. Cùng chữ trong 'trừ khử', "
        "'tảo trừ'. Và danh mục good_for của ngày (giải trừ, tắm gội, quét dọn) "
        "khớp đúng nghĩa này -- đối chiếu được ngay trong nguồn.",
        "etymology",
    ),
    Declared(
        "an sàng là kê giường",
        "An sàng 安床: 床 (sàng) là giường, 安 (an) là đặt/yên. Thuật ngữ lịch "
        "cổ chỉ việc kê đặt giường ngủ. Dịch thuật ngữ, không thêm hiệu lực.",
        "gloss",
    ),
    Declared(
        "trực của chuyện nên việc",
        "Trực thành 成: 成 (thành) nghĩa là nên/xong. Và good_for của Trực thành "
        "(nhập học, khai trương, di chuyển) đều là việc khởi sự -- khớp nghĩa tên.",
        "etymology",
    ),
    Declared(
        "trực của chuyện mở ra",
        "Trực khai 開: 開 (khai) nghĩa là mở. good_for của Trực khai có 7 việc, "
        "nhiều thứ nhì trong 12 trực (đếm cả năm 2026) -- khớp nghĩa 'mở'.",
        "etymology",
    ),
    Declared(
        "thiên về chuyện gom về",
        "Trực thu 收: 收 (thu) nghĩa là thu vào/gom lại. good_for (nạp tài, "
        "thu tất) đều là việc thu -- khớp. Dùng 'thiên về' vì đây là diễn giải "
        "xu hướng, không phải quy tắc cứng.",
        "etymology",
    ),
)

_DECLARED_NORM = {_norm(d.claim): d for d in DECLARED}


# ─── Mẫu câu diễn giải cần khai báo ───────────────────────────────────────
#
# Bắt CẤU TRÚC chứ không bắt từ khoá: mọi câu định nghĩa/quy nạp đều phải
# đi qua sổ. Cố ý bắt rộng -- thà báo thừa rồi khai báo, còn hơn để lọt.

INTERPRETIVE = (
    # Dừng ở dấu phẩy/chấm: bắt trọn MỆNH ĐỀ diễn giải, không nuốt sang vế
    # sau. Bản đầu dùng [^.]* nên bắt cả "sàng là kê giường, sắp chỗ nằm",
    # dài hơn câu đã khai báo nên so khớp trượt.
    r"chữ\s+\w+\s+nghĩa là\s+[^.,]+",
    r"\ban\s+sàng\s+là\s+[^.,]+",
    r"trực của chuyện\s+[^.,]+",
    r"thiên về chuyện\s+[^.,]+",
)

# ─── Mẫu câu SUY ĐOÁN -- cấm hẳn, không khai báo được ─────────────────────
SPECULATIVE = (
    r"người xưa\s+(?:thường|hay|vẫn|đều)\b",
    r"\bđược cho là\b",
    r"\bnghe nói\b",
    r"\bcó lẽ\b",
    r"\bdường như\b",
    r"\bbị kiêng nhiều\b",
    r"\bai cũng\b",
)


@dataclass
class ClaimIssue:
    ok: bool
    msg: str


def check_declared(script: str) -> list[ClaimIssue]:
    """Mọi câu diễn giải phải có trong sổ; mọi câu suy đoán đều bị loại."""
    out: list[ClaimIssue] = []
    low = script.lower()

    for pat in INTERPRETIVE:
        for m in re.finditer(pat, low):
            phrase = _norm(m.group(0).strip(" ,."))
            # So khớp theo BAO HÀM hai chiều, không khớp tuyệt đối: regex
            # cắt cụm theo ranh giới câu nên phần bắt được có thể dài hơn
            # hoặc ngắn hơn câu đã khai báo ("trực của chuyện nên việc" vs
            # "trực của chuyện nên"). Khớp cứng làm khai báo hợp lệ bị báo
            # thiếu -- đã gặp thật ở 4/7 kịch bản.
            hit = next((d for k, d in _DECLARED_NORM.items()
                        if k in phrase or phrase in k), None)
            out.append(ClaimIssue(
                hit is not None,
                f"diễn giải {m.group(0).strip(' ,.')!r} — " +
                (f"đã khai báo ({hit.kind})" if hit else
                 "CHƯA khai báo trong factory/claims.py, phải viết căn cứ rồi mới dùng")))

    spec = [p for p in SPECULATIVE if re.search(p, low)]
    out.append(ClaimIssue(not spec,
                          f"có câu suy đoán không kiểm chứng được: {spec}" if spec
                          else "không có câu suy đoán"))
    return out


# ─── Thống kê: TỰ ĐẾM LẠI, không tin lời khai ─────────────────────────────

# "cả tháng Mười chỉ có ba ngày Trực thành"
_STAT_MONTH = re.compile(
    r"cả tháng\s+(\w+)\s+chỉ có\s+(\w+)\s+ngày\s+(trực\s+\w+)", re.IGNORECASE)
# "thuộc nhóm sáu sao hắc đạo"
_STAT_GODS = re.compile(
    r"nhóm\s+(\w+)\s+sao\s+(hoàng đạo|hắc đạo)", re.IGNORECASE)

WORD_NUM = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6,
            "bảy": 7, "tám": 8, "chín": 9, "mười": 10, "mười một": 11, "mười hai": 12}
MONTH_NUM = {"một": 1, "hai": 2, "ba": 3, "tư": 4, "năm": 5, "sáu": 6,
             "bảy": 7, "tám": 8, "chín": 9, "mười": 10, "mười một": 11, "mười hai": 12}


def check_statistics(script: str, target: date) -> list[ClaimIssue]:
    """Đếm lại mọi thống kê trên TOÀN BỘ khoảng thời gian được nhắc tới.

    Đây là nửa còn lại của luật: thống kê chưa kiểm tra toàn bộ dữ liệu thì
    không được đánh ĐẠT. Nên ta không kiểm 'có hợp lý không' mà đếm lại thật."""
    import vnlunar
    out: list[ClaimIssue] = []
    low = script.lower()

    for m in _STAT_MONTH.finditer(low):
        month_word, count_word, truc = m.group(1), m.group(2), m.group(3).strip()
        if month_word not in MONTH_NUM or count_word not in WORD_NUM:
            out.append(ClaimIssue(False, f"thống kê tháng không đọc được: {m.group(0)!r}"))
            continue
        mon = MONTH_NUM[month_word]
        if mon != target.month:
            out.append(ClaimIssue(False,
                                  f"nói về tháng {mon} nhưng ngày lịch thuộc tháng {target.month}"))
            continue
        # Đếm THẬT, cả tháng.
        d, n, days = date(target.year, mon, 1), 0, []
        while d.month == mon:
            got = vnlunar.get_full_info(d.day, d.month, d.year)["12_constructions"]["name"]
            if _norm(got) == _norm(truc):
                n += 1
                days.append(d.isoformat())
            d += timedelta(days=1)
        claimed = WORD_NUM[count_word]
        out.append(ClaimIssue(claimed == n,
                              f"nói '{count_word} ngày {truc}' trong tháng {mon} — "
                              f"đếm thật: {n} ngày {days}"))

    for m in _STAT_GODS.finditer(low):
        count_word, kind = m.group(1), m.group(2)
        if count_word not in WORD_NUM:
            continue
        from factory.lunar import AUSPICIOUS_GODS
        actual = len(AUSPICIOUS_GODS) if "hoàng" in kind else 12 - len(AUSPICIOUS_GODS)
        out.append(ClaimIssue(WORD_NUM[count_word] == actual,
                              f"nói 'nhóm {count_word} sao {kind}' — hệ 12 sao có {actual}"))
    return out
