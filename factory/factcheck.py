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
from factory.lunar import CHI, GOD_ALIAS, GOD_ORDER, TRUC_ORDER, DayFacts
from factory.pillars.tables import TU28, TU_ALIAS
from factory.vocab import TRUC, lich_terms

# 12 sao hoàng đạo/hắc đạo. Dùng để bắt trường hợp kịch bản nhắc TÊN SAO
# của một ngày khác -- lỗi dễ xảy ra khi viết hàng loạt rồi copy nhầm.
# Tên phụ ("Câu Trận", "Bảo Quang") quy về tên chuẩn trước khi so.
ALL_GODS = GOD_ORDER
ALL_TRUC = TRUC_ORDER

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
    # "mai" đứng riêng cũng tính ("Ngày Rắn mai..."), nhưng "mai táng" thì không.
    says_tomorrow = bool(re.search(r"\bngày mai\b|\bmai\b(?!\s+táng)", low))
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
    named = sorted({GOD_ALIAS.get(g, g) for g in (*ALL_GODS, *GOD_ALIAS) if g.lower() in low})
    out.append(Finding(named == [facts.god_name], "FACT",
                       f"sao nhắc trong bài {named or '(không nhắc)'} — nguồn ghi {facts.god_name}"))
    # Nhãn hoàng đạo/hắc đạo phải khớp loại sao. "giờ hoàng đạo" là nhãn của
    # GIỜ, không phải của ngày -- không tính vào đây.
    if re.search(r"(?<!giờ )hoàng đạo", low) and not facts.is_auspicious_star:
        out.append(Finding(False, "FACT", f"gọi là hoàng đạo nhưng {facts.god_name} là sao hắc đạo"))
    if re.search(r"(?<!giờ )hắc đạo", low) and facts.is_auspicious_star:
        out.append(Finding(False, "FACT", f"gọi là hắc đạo nhưng {facts.god_name} là sao hoàng đạo"))

    # ─── FACT: khung diễn giải không được chỏi với loại sao ───────────────
    # Lỗi thật: ngày Bạch Hổ (hắc đạo) bị viết là "sao và trực cùng thuận".
    # Nhãn hoàng/hắc đạo thì đúng, nhưng KHUNG lại ngược -- kiểm nhãn không
    # đủ, phải kiểm cả cách diễn giải.
    THUAN = ("cùng thuận", "sao thuận", "trực cũng mở theo", "không chỏi nhau")
    hits = [k for k in THUAN if k in low]
    if hits and not facts.is_auspicious_star:
        out.append(Finding(False, "FACT",
                           f"khung 'thuận' {hits} nhưng {facts.god_name} là sao hắc đạo"))

    # ─── FACT: trực ───────────────────────────────────────────────────────
    # So khớp KHÔNG phân biệt hoa/thường: "Trực Bình" và "Trực bình" là một.
    truc_named = [t for t in ALL_TRUC if t.casefold() in low]
    out.append(Finding(truc_named == [facts.truc_name], "FACT",
                       f"trực nhắc trong bài {truc_named or '(không nhắc)'} — nguồn ghi {facts.truc_name}"))

    # ─── FACT: chú giải chữ Hán phải đúng của CHÍNH trực đó ───────────────
    # Lỗi cũ: chú giải được so theo bao hàm hai chiều với cả sổ, nên
    # "Trực trừ — 除, nghĩa là gom về" (nghĩa của Trực thu) vẫn ĐẠT.
    for m in re.finditer(r"(trực\s+\w+)\s+—\s+(\S+?),\s+nghĩa là\s+([^.]+)", low):
        canon = next((t for t in ALL_TRUC if t.casefold() == m.group(1)), None)
        term = TRUC.get(canon) if canon else None
        ok = bool(term) and m.group(2) == term.han and m.group(3).strip() == term.gloss
        out.append(Finding(ok, "FACT",
                           f"chú giải {m.group(0)!r} — từ điển: "
                           + (f"{term.han}, nghĩa là {term.gloss}" if term else "không có trực này")))

    # ─── FACT: tên việc phải có trong nguồn ───────────────────────────────
    src = _norm(" | ".join(list(facts.truc_good_for) + list(facts.truc_bad_for)))
    # Soi MỌI tên việc của tập đóng (danh mục 12 trực), không chỉ một danh
    # sách tay -- việc nào của trực khác mà lọt vào bài là bị bắt.
    LICH_TERMS = tuple(dict.fromkeys(lich_terms() + (
        "an sàng", "an phủ biên cảnh", "tuyển tướng", "nhập học", "trúc đê phòng", "khai trương",
        "tiến người", "nạp tài", "bắt bớ", "thu tất", "tế tự", "cầu phúc", "cầu tự", "xuất hành",
        "di chuyển", "động thổ", "san nền", "đắp lỗ", "sửa tường", "giải trừ", "tắm gội",
        "chỉnh dung", "cạo đầu", "cầu y trị bệnh", "quét dọn nhà cửa", "khởi công",
        "cưới hỏi", "an táng", "chôn cất", "mai táng", "ký kết", "chuyển nhà", "nhập trạch")))
    bogus = [t for t in LICH_TERMS
             if re.search(rf"(?<!\w){re.escape(t)}(?!\w)", low) and _norm(t) not in src]
    out.append(Finding(not bogus, "FACT",
                       f"việc nhắc nhưng KHÔNG có trong nguồn: {bogus}" if bogus
                       else "mọi tên việc đều có trong nguồn"))

    # ─── FACT: các tầng bổ sung (giờ, tú, tuổi xung, hướng) ───────────────
    # Bản trước KHÔNG soi những câu này: sửa "giờ Tý" thành "giờ Sửu", hay
    # chèn "tú Khuê... nhóm tốt", vẫn ĐẠT. Chúng là dữ kiện người xem làm
    # theo trực tiếp, nên phải khớp nguồn đúng từng chữ.
    hours = facts.auspicious_hours.lower()
    good_chi = {h.split(" (")[0] for h in hours.split(", ") if h}
    for s in sents:
        sl = s.lower()
        if not re.search(r"giờ (tốt|hoàng đạo)", sl):
            continue
        for m in re.finditer(r"\bgiờ (" + "|".join(c.lower() for c in CHI) + r")\b(?:\s*\(([^)]*)\))?", sl):
            chi, span = m.group(1), m.group(2)
            ok = chi in good_chi and (span is None or f"{chi} ({span})" in hours)
            out.append(Finding(ok, "FACT", f"nhắc giờ {m.group(0)!r} — giờ hoàng đạo của nguồn: "
                                           f"{facts.auspicious_hours}"))
        if "đầu tiên" in sl:
            first = hours.split(",")[0].strip()
            m = re.search(r"giờ\s+(\w+\s*\([^)]*\))", sl)
            if m:
                out.append(Finding(m.group(1).strip() == first, "FACT",
                                   f"nói giờ tốt đầu tiên là {m.group(1)!r} — nguồn: {first}"))
    tu_names = "|".join(sorted({*(n.lower() for n, _, _ in TU28), *(a.lower() for a in TU_ALIAS)},
                               key=len, reverse=True))
    for m in re.finditer(rf"\btú ({tu_names})\b", low):
        said = TU_ALIAS.get(m.group(1).capitalize(), m.group(1).capitalize())
        out.append(Finding(said.lower() == facts.mansion_name.lower(), "FACT",
                           f"nhắc tú {m.group(1)!r} — nguồn: tú {facts.mansion_name}"))
    m = re.search(r"\btú \w+, con ([^,]+), lịch xếp vào nhóm (tốt|xấu)", low)
    if m:
        nhom = "tốt" if facts.mansion_good else "xấu"
        out.append(Finding(m.group(1).strip() == facts.mansion_animal.lower() and m.group(2) == nhom,
                           "FACT", f"tú: con {m.group(1)!r}, nhóm {m.group(2)!r} — nguồn: con "
                                   f"{facts.mansion_animal}, nhóm {nhom}"))
    m = re.search(r"xung với tuổi (\w+)", low)
    if m:
        out.append(Finding(m.group(1) == facts.conflict_animal.lower(), "FACT",
                           f"tuổi xung {m.group(1)!r} — nguồn: {facts.conflict_animal}"))
    m = re.search(r"ngày (\w+) thì theo lịch cũ xung", low)
    if m:
        out.append(Finding(m.group(1) == facts.day_animal.lower(), "FACT",
                           f"con giáp của ngày {m.group(1)!r} — nguồn: {facts.day_animal}"))
    for label, want in (("tài thần", facts.wealth_god_dir), ("hỷ thần", facts.joy_god_dir)):
        m = re.search(rf"hướng {label}[^.]*?là hướng ([^.,]+)", low)
        if m:
            out.append(Finding(m.group(1).strip() == want.lower(), "FACT",
                               f"hướng {label} {m.group(1).strip()!r} — nguồn: {want}"))

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
        # Bản trước để lọt "danh mục mở tới chín việc" (thật 7) và "vỏn vẹn
        # ba, đếm chưa hết một bàn tay": số không đứng sát "danh mục".
        (r"(?:cho làm tới|mở tới|lên tới|chỉ còn)\s+(\w+)\s+việc", n_good, "good_for"),
        (r"vỏn vẹn\s+(\w+)(?=,)", n_good, "good_for"),
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
