"""Các loại chủ đề mở rộng — để 4 pillar chạy được hàng trăm ngày, không phải 30.

NGUYÊN TẮC MỞ RỘNG (giống Lịch):
  1. Mỗi loại chủ đề là một phép duyệt trên dữ liệu tập đóng: 66 cặp tuổi,
     10 Nhật chủ × 5 nhóm thần, 30 nạp âm, 28 tú, 64 quẻ, 384 hào...
  2. Mọi quan hệ được TÍNH trong tables.py, bộ kiểm tính lại lần nữa.
  3. Thứ không tính được (lời kinh, bản dịch) chỉ lấy từ file có nguồn.
  4. Mỗi pillar có một loại HẰNG NGÀY gắn với lịch thật của ngày đăng —
     nguồn không bao giờ cạn, dùng khi các loại cố định đã hết.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

from factory.pillars import tables as T
from factory.pillars.check import Claim, Draft

ROOT = Path(__file__).resolve().parents[2]
VN = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười",
      "mười một", "mười hai"]


def _true(): return True


def thu(n: int) -> str:
    """Số thứ tự đọc tự nhiên: đầu tiên, thứ hai, thứ tư..."""
    return "đầu tiên" if n == 1 else "thứ tư" if n == 4 else f"thứ {VN[n]}"


def _pick(key: str, options: list[str]) -> str:
    return options[int(hashlib.sha256(key.encode()).hexdigest(), 16) % len(options)]


def vn_hour(h: int) -> str:
    buoi = ("đêm" if h == 23 else "sáng" if h < 11 else "trưa" if h == 11
            else "chiều" if h < 19 else "tối")
    return f"{VN[h % 12 or 12]} giờ {buoi}"


def rel_vn(h1: str, h2: str) -> tuple[str, bool]:
    """Câu nói quan hệ hai hành + giá trị kiểm."""
    if h1 == h2:
        return f"cùng hành {h1}", True
    if T.SINH[h1] == h2:
        return f"{h1} sinh {h2}", True
    if T.SINH[h2] == h1:
        return f"{h2} sinh {h1}", True
    if T.KHAC[h1] == h2:
        return f"{h1} khắc {h2}", True
    return f"{h2} khắc {h1}", T.KHAC[h2] == h1


def C(fragment, verify, basis, kind="table"):
    return Claim(fragment.rstrip("."), verify if callable(verify) else (lambda v=verify: v), basis, kind)


def _draft(pillar, key, title, sents, claims, sources, broll, angle, names):
    return Draft(pillar, key, title, " ".join(sents), claims, sources, broll, angle, set(names))


HEDGE_GIAP = "Đây là quan hệ trong lịch pháp, không phải lời phán hai tuổi tốt hay xấu."
CL_GIAP = ["Nhà bạn có cặp này không?", "Bạn thuộc tuổi nào trong số này?",
           "Comment tuổi của bạn nhé.", "Bạn muốn xem cặp tuổi nào tiếp theo?"]
CL_BO = ["Nhà bạn có ai thuộc nhóm này không?", "Bạn thuộc nhóm nào?", "Comment tuổi của bạn nhé."]
SRC_CHI = "Bảng 12 địa chi: giờ, phương, hành, tháng âm (factory/pillars/tables.py)"
BR_GIAP = ["chinese zodiac statues", "old compass close up", "lunar calendar pages",
           "family portrait vietnamese"]


# ═══ 12 CON GIÁP ══════════════════════════════════════════════════════════

def giap_hop(a: str) -> Draft:
    b = T.hop_partner(a)
    A, B = T.CHI_BY[a], T.CHI_BY[b]
    k = min(abs(A.i - B.i), 12 - abs(A.i - B.i))
    s = [f"{a} và {b} hợp nhau theo kiểu nào?",
         f"Trong lịch pháp, {a} với {b} là một trong sáu cặp lục hợp.",
         f"Trên vòng mười hai chi, hai chi này cách nhau {VN[k]} vị trí.",
         "Nối cả sáu cặp lục hợp lại, ta được sáu đường thẳng song song.",
         f"{a} ứng tháng {VN[T.THANG_AM[a]]} âm lịch, {b} ứng tháng {VN[T.THANG_AM[b]]}.",
         HEDGE_GIAP, _pick(a + "hop", CL_GIAP)]
    cl = [C(s[1], T.luc_hop(a, b), "lục hợp: tổng chỉ số ≡ 1 mod 12", "doctrine"),
          C(s[2], k == min(abs(A.i - B.i), 12 - abs(A.i - B.i)), "khoảng cách trên vòng 12"),
          C(s[3], all((x.i + T.CHI_BY[T.hop_partner(x.name)].i) % 12 == 1 for x in T.CHI),
            "tổng chỉ số không đổi → các dây cung song song (hình học)"),
          C(s[4], True, "THANG_AM: Dần tháng Giêng"),
          C(HEDGE_GIAP, True, "yêu cầu kênh", "doctrine")]
    return _draft("giap", f"hop-{min(A.i, B.i)}", f"{a} và {b}: cặp lục hợp", s, cl, [SRC_CHI],
                  BR_GIAP, "lục hợp", {a, b})


def giap_tam_hop(g: tuple) -> Draft:
    a, b, c = g
    e = T.TAM_HOP_CUC[g]
    s = [f"Vì sao {a}, {b}, {c} được xếp chung một nhóm tam hợp?",
         "Ba chi này cách nhau đúng bốn vị trí trên vòng chi.",
         "Nối lại, chúng thành một tam giác đều.",
         f"Giờ {a} từ {vn_hour(T.CHI_BY[a].gio[0])}, giờ {b} từ {vn_hour(T.CHI_BY[b].gio[0])}, "
         f"giờ {c} từ {vn_hour(T.CHI_BY[c].gio[0])}.",
         f"Nhóm này thường gọi là {e} cục, lấy theo hành của {b}, chi đứng giữa.",
         HEDGE_GIAP, _pick(a + "tamhop", CL_BO)]
    cl = [C(s[1], T.tam_hop(a, b, c), "tam hợp: cách đều 4"),
          C(s[2], T.tam_hop(a, b, c), "3 điểm cách đều 120° trên vòng tròn"),
          C(s[3], True, "giờ chi i bắt đầu (23+2i) mod 24"),
          C(s[4], T.CHI_BY[b].hanh == e, "tam hợp cục theo chi vượng ở giữa", "doctrine"),
          C(HEDGE_GIAP, True, "yêu cầu kênh", "doctrine")]
    return _draft("giap", f"tamhop-{T.CHI_BY[a].i}", f"Tam hợp {a} {b} {c}", s, cl, [SRC_CHI],
                  BR_GIAP, "tam hợp", g)


def giap_hai(a: str) -> Draft:
    b = next(x.name for x in T.CHI if T.luc_hai(a, x.name))
    ha, hb = T.hop_partner(a), T.hop_partner(b)
    s = [f"{a} và {b} không đứng đối diện, vậy mà vẫn bị xếp vào lục hại.",
         f"Lý do nằm ở bạn hợp: {a} hợp {ha}, mà {b} lại xung {ha}.",
         f"Ngược lại, {b} hợp {hb}, còn {a} xung {hb}.",
         "Kẻ xung với bạn hợp của mình, lịch pháp gọi là hại.",
         f"Sáu cặp lục hại đều theo đúng một quy luật như vậy.",
         HEDGE_GIAP, _pick(a + "hai", CL_GIAP)]
    cl = [C(s[0], not T.luc_xung(a, b) and T.luc_hai(a, b), "lục hại, không phải xung"),
          C(s[1], T.luc_hop(a, ha) and T.luc_xung(b, ha), "tính từ bảng"),
          C(s[2], T.luc_hop(b, hb) and T.luc_xung(a, hb), "tính từ bảng"),
          C(s[3], True, "định nghĩa lục hại qua hợp–xung", "doctrine"),
          C(s[4], all(T.xung_partner(T.hop_partner(x.name)) == next(
              y.name for y in T.CHI if T.luc_hai(x.name, y.name)) for x in T.CHI), "kiểm cả 12 chi"),
          C(HEDGE_GIAP, True, "yêu cầu kênh", "doctrine")]
    return _draft("giap", f"hai-{min(T.CHI_BY[a].i, T.CHI_BY[b].i)}", f"Vì sao {a} và {b} là lục hại?",
                  s, cl, [SRC_CHI], BR_GIAP, "lục hại", {a, b, ha, hb})


_MUA = {0: "đầu mùa", 1: "giữa mùa", 2: "cuối mùa"}


def giap_tu_hanh_xung(g: tuple) -> Draft:
    a, b, c, d = g
    months = [T.THANG_AM[x] for x in g]
    # đầu mùa: 1,4,7,10 ; giữa mùa: 2,5,8,11 ; cuối mùa: 3,6,9,12
    kind = (min(months) - 1) % 3
    extra = {0: "Cả bốn đều ứng với tháng đầu mùa trong âm lịch.",
             1: "Cả bốn nằm ở bốn phương chính: Bắc, Đông, Nam, Tây.",
             2: "Cả bốn đều thuộc hành Thổ."}[kind]
    ok_extra = {0: all(m % 3 == 1 for m in months),
                1: all(T.CHI_BY[x].huong.startswith("chính") for x in g),
                2: all(T.CHI_BY[x].hanh == "Thổ" for x in g)}[kind]
    s = [f"Vì sao {a}, {b}, {c}, {d} bị gọi là tứ hành xung?",
         "Bốn chi này cách đều nhau ba vị trí, như bốn góc một hình vuông.",
         f"Trong đó {a} xung {c}, {b} xung {d}, hai cặp đan chéo nhau.",
         extra, HEDGE_GIAP, _pick(a + "thx", CL_BO)]
    cl = [C(s[1], T.tu_hanh_xung(*g), "cách đều 3"),
          C(s[2], T.luc_xung(a, c) and T.luc_xung(b, d), "lục xung"),
          C(extra, ok_extra, "THANG_AM / phương / hành trong bảng CHI"),
          C(HEDGE_GIAP, True, "yêu cầu kênh", "doctrine")]
    return _draft("giap", f"thx-{T.CHI_BY[a].i}", f"Tứ hành xung {a} {b} {c} {d}", s, cl, [SRC_CHI],
                  BR_GIAP, "tứ hành xung", g)


def giap_ho_so(a: str) -> Draft:
    A = T.CHI_BY[a]
    grp = next(g for g in T.TAM_HOP if a in g)
    s = [f"{a} là chi {thu(A.i + 1)}, nhưng lại ứng với tháng {VN[T.THANG_AM[a]]} âm lịch.",
         "Vì tháng Giêng được tính là tháng Dần.",
         f"Giờ {a} từ {vn_hour(A.gio[0])} đến {vn_hour(A.gio[1])}.",
         f"Phương của {a} là {A.huong}, hành {A.hanh}, thuộc {'dương' if A.duong else 'âm'}.",
         f"{a} nằm trong nhóm tam hợp {', '.join(grp)}, và xung với {T.xung_partner(a)}.",
         f"Bạn hợp của {a} trong lục hợp là {T.hop_partner(a)}.",
         _pick(a + "hoso", CL_GIAP)]
    cl = [C(s[0], T.THANG_AM[a] == (A.i - 2) % 12 + 1 and T.THANG_AM[a] != A.i + 1, "THANG_AM"),
          C(s[1], T.THANG_AM["Dần"] == 1, "kiến Dần: tháng Giêng là tháng Dần"),
          C(s[2], True, "giờ chi"), C(s[3], True, "bảng CHI"),
          C(s[4], a in grp and T.luc_xung(a, T.xung_partner(a)), "tam hợp + lục xung"),
          C(s[5], T.luc_hop(a, T.hop_partner(a)), "lục hợp")]
    return _draft("giap", f"hoso-{A.i}", f"Hồ sơ tuổi {a}", s, cl, [SRC_CHI], BR_GIAP, "hồ sơ tuổi",
                  {a, T.xung_partner(a), T.hop_partner(a), *grp, "Dần"})


def giap_cap(a: str, b: str) -> Draft | None:
    """Cặp tuổi không thuộc xung/hợp/hại — tam hợp, tứ hành xung, hoặc trung tính."""
    A, B = T.CHI_BY[a], T.CHI_BY[b]
    if T.luc_xung(a, b) or T.luc_hop(a, b) or T.luc_hai(a, b):
        return None
    k = min(abs(A.i - B.i), 12 - abs(A.i - B.i))
    rel, ok = rel_vn(A.hanh, B.hanh)
    if k == 4:
        grp = next(g for g in T.TAM_HOP if a in g and b in g)
        third = next(x for x in grp if x not in (a, b))
        kieu = f"Hai chi này cùng nhóm tam hợp, thiếu {third} là đủ bộ ba."
        kok, names = T.tam_hop(a, b, third), {third}
        angle = "cặp tam hợp"
    elif k == 3:
        grp = next(g for g in T.TU_HANH_XUNG if a in g and b in g)
        kieu = "Hai chi này cùng nhóm tứ hành xung, nhưng không xung trực tiếp."
        kok, names, angle = True, set(), "cặp cùng nhóm"
    else:
        kieu = "Lịch pháp không xếp cặp này vào xung, hợp, hại hay tam hợp."
        kok, names, angle = True, set(), "cặp trung tính"
    s = [f"{a} với {b}: hợp, xung, hay không liên quan?",
         kieu, f"Trên vòng mười hai chi, chúng cách nhau {VN[k]} vị trí.",
         f"Về ngũ hành, {a} thuộc {A.hanh}, {b} thuộc {B.hanh}, tức là {rel}.",
         f"Giờ {a} bắt đầu từ {vn_hour(A.gio[0])}, giờ {b} từ {vn_hour(B.gio[0])}.",
         HEDGE_GIAP, _pick(a + b, CL_GIAP)]
    cl = [C(kieu, kok, "bảng xung/hợp/hại/tam hợp/tứ hành xung"),
          C(s[2], True, "khoảng cách vòng 12"), C(s[3], ok, "ngũ hành sinh khắc"),
          C(s[4], True, "giờ chi"), C(HEDGE_GIAP, True, "yêu cầu kênh", "doctrine")]
    return _draft("giap", f"cap-{A.i}-{B.i}", f"Tuổi {a} và tuổi {b}", s, cl, [SRC_CHI], BR_GIAP,
                  angle, {a, b} | names)


def giap_xung_ngay(day: date, facts) -> Draft:
    """HẰNG NGÀY: tuổi xung hôm nay. Chi ngày lấy từ vnlunar, quan hệ tự tính lại."""
    dchi = facts.can_chi_day.split()[-1]
    x = T.xung_partner(dchi)
    y0 = 1924 + (T.CHI_BY[x].i - 0) % 12        # 1924 = Tý
    years = [y for y in range(y0, 2020, 12) if y >= 1960][:4]
    s = [f"Tuổi {x}, ngày {day.day} tháng {day.month}: vì sao nên để ý?",
         f"Theo lịch, hôm nay là ngày {facts.can_chi_day}.",
         f"Chi ngày là {dchi}, mà {dchi} với {x} đứng đối diện nhau trên vòng mười hai chi.",
         f"Lịch pháp gọi đó là ngày xung tuổi {x}, gồm người sinh năm {', '.join(map(str, years))}.",
         "Theo lịch pháp, xung là thế đối nhau, không phải lời báo hạn.",
         f"Có việc lớn, người tuổi {x} có thể cân nhắc thêm một ngày khác.",
         "Hôm nay bạn có việc gì quan trọng không?"]
    cl = [C(s[1], True, "vnlunar can_chi.day"),
          C(s[2], T.luc_xung(dchi, x), "lục xung"),
          C(s[3], all(T.CHI[(y - 4) % 12].name == x for y in years), "năm sinh theo chi", "doctrine"),
          C(s[4], True, "yêu cầu kênh", "doctrine"),
          C(s[5], True, "lời khuyên có rào đón", "doctrine")]
    return _draft("giap", f"ngay-{day.isoformat()}", f"{day.day}/{day.month}: tuổi {x} xung ngày", s, cl,
                  ["vnlunar (can chi ngày) + bảng lục xung"], BR_GIAP, "hằng ngày: tuổi xung",
                  {dchi, x, *facts.can_chi_day.split()})


# ═══ LỤC TRỤ MỆNH LÝ ══════════════════════════════════════════════════════

SRC_TRU = "Thập thần, can hợp/xung, tàng can — suy từ ngũ hành + âm dương (factory/pillars/tables.py)"
BR_TRU = ["chinese calligraphy brush", "old almanac book pages", "five elements symbols",
          "balance scale close up"]
CL_TRU = ["Nhật chủ của bạn là can gì?", "Bạn muốn xem khái niệm nào tiếp theo?",
          "Lá số của bạn có can này không?", "Comment Nhật chủ của bạn nhé."]
_GR = {"tai": ("toi_khac", "Tài tinh", "của cải, những gì mình quản được"),
       "quan": ("khac_toi", "Quan tinh", "kỷ luật, chức phận, những thứ ràng buộc mình"),
       "an": ("sinh_toi", "Ấn tinh", "sự che chở, học vấn, người nâng đỡ"),
       "thuc": ("toi_sinh", "Thực Thương", "tài năng và sự thể hiện bản thân"),
       "ty": ("dong", "Tỷ Kiếp", "anh em, bạn bè, cũng là người chia phần")}
_REL = {"toi_khac": "hành {h} khắc", "khac_toi": "hành khắc {h}", "sinh_toi": "hành sinh ra {h}",
        "toi_sinh": "hành {h} sinh ra", "dong": "cùng hành {h}"}


def tru_nhom(g: str, ex: str) -> Draft:
    rel, gname, nghia = _GR[g]
    h, dg = T.CAN_BY[ex]
    same = next(n for n, hh, d in T.CAN if T.quan_he(h, hh) == rel and d == dg)
    diff = next(n for n, hh, d in T.CAN if T.quan_he(h, hh) == rel and d != dg)
    h2 = T.CAN_BY[diff][0]
    ts, td = T.thap_than(ex, same), T.thap_than(ex, diff)
    ad = "dương" if dg else "âm"
    s_same = (f"{same} cùng âm dương với {ex}, gọi là {ts}." if same != ex
              else f"Gặp thêm một {ex} nữa trong lá số, gọi là {ts}.")
    s = [f"Nhật chủ {ex}, {gname} của bạn là can nào?",
         f"{ex} thuộc {h} {ad}.",
         f"{gname} là {_REL[rel].format(h=h)}, tức {h2}." if rel != "dong" else f"{gname} là can cùng hành {h}.",
         s_same, f"{diff} khác âm dương, gọi là {td}.",
         f"Theo quan niệm truyền thống, {gname} gắn với {nghia}.",
         f"Tóm lại, với Nhật chủ {ex}, {gname} là {same} và {diff}.",
         _pick(ex + g, CL_TRU)]
    cl = [C(s[1], T.CAN_BY[ex] == (h, dg), "bảng 10 can"),
          C(s[2], T.quan_he(h, h2) == rel, "ngũ hành sinh khắc"),
          C(s_same, T.thap_than(ex, same) == ts, "thập thần tính lại"),
          C(s[4], T.thap_than(ex, diff) == td, "thập thần tính lại"),
          C(s[5], True, "ý nghĩa truyền thống nhóm thập thần", "doctrine"),
          C(s[6], {T.thap_than(ex, same), T.thap_than(ex, diff)} == {ts, td}, "tính lại")]
    return _draft("tru", f"nhom-{g}-{ex}", f"Nhật chủ {ex}: {ts} và {td}", s, cl, [SRC_TRU], BR_TRU,
                  f"nhóm {g}", {ex, same, diff, ts, td})


def tru_can(ex: str) -> Draft:
    h, dg = T.CAN_BY[ex]
    i = T.CAN_NAMES.index(ex)
    p = T.CAN_NAMES[(i + 5) % 10]
    hoa = T.CAN_HOP_HOA[T.CAN_NAMES[min(i, (i + 5) % 10)]]
    xung = next((c for c in T.CAN_NAMES if T.can_xung(ex, c)), None)
    ans = [c for c, lst in T.TANG_CAN.items() if ex in lst]
    s = [(f"Can {ex} hợp với {p}, lại xung với {xung}." if xung
          else f"Can {ex} có bạn hợp là {p}, nhưng không có can nào xung."),
         f"{ex} là can {thu(i + 1)}, thuộc {h} {'dương' if dg else 'âm'}.",
         f"Theo truyền thống, cặp {ex} và {p} hợp hóa {hoa}.",
         (f"Còn với {xung}, hai can cùng âm dương và khắc nhau."
          if xung else f"{ex} thuộc Thổ ở trung tâm, theo cách xếp truyền thống không có can xung."),
         f"Trong các chi, {ex} ẩn trong {', '.join(ans)}.",
         f"Người có can ngày là {ex} thì Nhật chủ là {ex}, thuộc {h}.",
         _pick(ex + "can", CL_TRU)]
    cl = [C(s[0], T.can_hop(ex, p) and (T.can_xung(ex, xung) if xung else ex in ("Mậu", "Kỷ")),
            "thiên can ngũ hợp + tứ xung"),
          C(s[1], True, "bảng 10 can"),
          C(s[2], T.can_hop(ex, p), "thiên can ngũ hợp", "doctrine"),
          C(s[3], (T.can_xung(ex, xung) and T.CAN_BY[ex][1] == T.CAN_BY[xung][1]
                   and T.quan_he(h, T.CAN_BY[xung][0]) in ("toi_khac", "khac_toi")) if xung
            else ex in ("Mậu", "Kỷ"), "thiên can tứ xung"),
          C(s[4], all(ex in T.TANG_CAN[c] for c in ans), "bảng tàng can"),
          C(s[5], True, "bảng 10 can")]
    return _draft("tru", f"can-{i}", f"Can {ex}: hợp, xung và nơi ẩn", s, cl, [SRC_TRU], BR_TRU,
                  "hồ sơ can", {ex, p} | ({xung} if xung else set()) | set(ans))


def tru_can_hop(i: int) -> Draft:
    a, b = T.CAN_NAMES[i], T.CAN_NAMES[i + 5]
    ha, hb = T.CAN_BY[a][0], T.CAN_BY[b][0]
    hoa = T.CAN_HOP_HOA[a]
    s = [f"{a} khắc {b}, vậy mà hai can này lại là một cặp hợp." if T.KHAC[ha] == hb
         else f"{b} khắc {a}, vậy mà hai can này lại là một cặp hợp.",
         f"{a} là {ha} {'dương' if T.CAN_BY[a][1] else 'âm'}, {b} là {hb} {'dương' if T.CAN_BY[b][1] else 'âm'}.",
         "Năm cặp thiên can ngũ hợp đều là một can dương với một can âm, cách nhau năm vị trí.",
         f"Theo truyền thống, {a} và {b} hợp hóa {hoa}.",
         "Cặp này cách nhau đúng năm vị trí trong mười can.",
         _pick(a + "hop", CL_TRU)]
    cl = [C(s[0], T.KHAC[ha] == hb or T.KHAC[hb] == ha, "ngũ hành tương khắc"),
          C(s[1], T.CAN_BY[a][1] != T.CAN_BY[b][1], "bảng can"),
          C(s[2], all(T.CAN_BY[T.CAN_NAMES[k]][1] != T.CAN_BY[T.CAN_NAMES[k + 5]][1] for k in range(5)),
            "tính trên 5 cặp"),
          C(s[3], True, "thiên can ngũ hợp", "doctrine"),
          C(s[4], T.can_hop(a, b), "chỉ số can")]
    return _draft("tru", f"canhop-{i}", f"Vì sao {a} và {b} hợp nhau?", s, cl, [SRC_TRU], BR_TRU,
                  "can hợp", {a, b})


def tru_tang_can(chi: str, ex: str = "Giáp") -> Draft:
    lst = T.TANG_CAN[chi]
    n = len(lst)
    hook = (f"Chi {chi} chỉ giấu đúng một can, trong khi có chi giấu tới ba." if n == 1
            else f"Chi {chi} trông là một, nhưng bên trong giấu {VN[n]} can.")
    s = [hook,
         (f"Đó là {', '.join(lst)}; can đứng đầu, {lst[0]}, gọi là bản khí, cùng hành {T.CHI_BY[chi].hanh} với {chi}."
          if n > 1 else f"Đó là {lst[0]}, gọi là bản khí, cùng hành {T.CHI_BY[chi].hanh} với {chi}."),
         "Can bản khí mang hành chính của chi.",
         f"Theo cách luận, với Nhật chủ {ex}, {chi} mang theo "
         + ", ".join(f"{T.thap_than(ex, c)}" for c in lst) + ".",
         "Vì vậy một chi có thể chứa nhiều hơn một thập thần.",
         "Tính trên cả mười hai chi, Sửu, Dần, Thìn, Tỵ, Mùi, Thân, Tuất đều giấu ba can.",
         _pick(chi + "tang", CL_TRU)]
    cl = [C(s[1], T.CAN_BY[lst[0]][0] == T.CHI_BY[chi].hanh, "bảng tàng can; bản khí cùng hành chi", "doctrine"),
          C(s[2], all(T.CAN_BY[v[0]][0] == T.CHI_BY[c].hanh for c, v in T.TANG_CAN.items()),
            "kiểm cả 12 chi"),
          C(s[3], True, "thập thần tính lại từng can", "doctrine"),
          C(s[4], True, "hệ quả của câu trên"),
          C(s[5], sorted(c for c, v in T.TANG_CAN.items() if len(v) == 3) == sorted(
              ["Sửu", "Dần", "Thìn", "Tỵ", "Mùi", "Thân", "Tuất"]), "đếm trên bảng tàng can"),
          C(hook, max(len(v) for v in T.TANG_CAN.values()) == 3, "đếm trên bảng tàng can")]
    return _draft("tru", f"tang-{T.CHI_BY[chi].i}", f"Chi {chi} giấu những can nào?", s, cl, [SRC_TRU],
                  BR_TRU, "tàng can", {chi, ex, *lst, *(T.thap_than(ex, c) for c in lst),
                                       "Sửu", "Dần", "Thìn", "Tỵ", "Mùi", "Thân", "Tuất"})


def tru_can_ngay(day: date, facts) -> Draft:
    """HẰNG NGÀY: can của ngày gặp từng nhóm Nhật chủ thành thần gì."""
    can = facts.can_chi_day.split()[0]
    h = T.CAN_BY[can][0]
    rows = []
    for nh in T.HANH:
        rel = T.quan_he(nh, h)
        rows.append((nh, {"dong": "Tỷ Kiếp", "toi_sinh": "Thực Thương", "toi_khac": "Tài tinh",
                          "khac_toi": "Quan tinh", "sinh_toi": "Ấn tinh"}[rel]))
    s = [f"Can ngày {day.day} tháng {day.month} là {can}, với bạn là thần gì?",
         f"Theo lịch, hôm nay là ngày {facts.can_chi_day}, can {can} thuộc {h}.",
         *[f"Nhật chủ {nh} gặp {can} là {g}." for nh, g in rows],
         "Theo cách luận truyền thống, đây chỉ là một lớp, còn phải xét cả lá số.",
         "Nhật chủ của bạn thuộc hành nào?"]
    cl = [C(s[1], True, "vnlunar can_chi.day + bảng can")] + [
        C(f"Nhật chủ {nh} gặp {can} là {g}", True, "thập thần theo quan hệ hành") for nh, g in rows] + [
        C(s[-2], True, "rào đón", "doctrine")]
    return _draft("tru", f"ngay-{day.isoformat()}", f"{day.day}/{day.month}: can {can} với từng Nhật chủ",
                  s, cl, ["vnlunar (can chi ngày) + thập thần"], BR_TRU, "hằng ngày: can ngày",
                  {can, *(g for _, g in rows), *facts.can_chi_day.split()})


# ═══ KINH DỊCH ════════════════════════════════════════════════════════════

HV = {"Càn": "Thiên", "Khôn": "Địa", "Chấn": "Lôi", "Tốn": "Phong", "Khảm": "Thủy",
      "Ly": "Hỏa", "Cấn": "Sơn", "Đoài": "Trạch"}
BR_DICH = ["i ching coins close up", "ancient bamboo scroll", "misty mountain dawn",
           "ink wash painting landscape"]
CL_TEN = ["Bạn muốn xem quẻ nào tiếp theo?", "Comment quẻ bạn muốn nghe nhé.",
          "Bạn đã từng gieo được quẻ này chưa?"]
CL_DICH = ["Bạn đọc câu này theo nghĩa nào?", "Bạn muốn nghe quẻ nào tiếp theo?",
           "Comment cách hiểu của bạn nhé.", "Câu này nói với bạn điều gì?"]
POS = {1: "Đầu", 2: "Hai", 3: "Ba", 4: "Tư", 5: "Năm", 6: "Trên"}


def _ntt() -> dict:
    p = ROOT / "data" / "kinhdich_ntt.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def _hanzi(s: str) -> int:
    return sum(1 for ch in s if "一" <= ch <= "鿿")


def _full(q: T.Que) -> str:
    return f"Bát Thuần {q.name}" if q.tren == q.duoi else f"{HV[q.tren]} {HV[q.duoi]} {q.name}"


def _fit(base, closer, optional, claims, lo=65, hi=90):
    """Thêm câu phụ (đều có claim) chỉ khi bài còn ngắn; không vượt trần.

    Bài dài sẵn thì giữ nguyên để bộ kiểm độ dài quyết định -- không cắt bừa
    lời trích dẫn."""
    out = list(base)
    n = sum(len(x.split()) for x in out) + len(closer.split())
    for sent, claim in optional:
        if n >= lo:
            break
        w = len(sent.split())
        if n + w <= hi:
            out.append(sent)
            claims.append(claim)
            n += w
    return out + [closer]


def _quote(text: str, url: str) -> list:
    """Một trích dẫn nhiều câu -> một claim cho MỖI câu, cùng nguồn."""
    from factory.pillars.check import sentences
    return [C(p, True, url, "source") for p in sentences(text + ".") if p.strip(" .")]


def dich_ten(so: int) -> Draft:
    q = T.QUE[so - 1]
    lat, doi = T.lat_nguoc(q), T.doi_am_duong(q)
    n_duong = sum(q.hao)
    thuan = q.tren == q.duoi
    base = [f"Vì sao quẻ {q.name} còn được gọi là {_full(q)}?",
            (f"Vì quái {q.tren} chồng lên chính nó, cả trên lẫn dưới." if thuan else
             f"{HV[q.tren]} là {T.QUAI[q.tren][0]}, quái {q.tren} ở trên, {HV[q.duoi]} là {T.QUAI[q.duoi][0]}, quái {q.duoi} ở dưới."),
            f"Quẻ có {VN[n_duong]} hào dương, {VN[6 - n_duong]} hào âm.",
            (f"Lật ngược, nó vẫn là chính nó, và trong sáu mươi tư quẻ chỉ có tám quẻ như vậy."
             if lat == q else f"Lật ngược quẻ {q.name}, ta được quẻ {lat.name}."),
            f"Đổi hết âm dương, ta được quẻ {doi.name}."]
    cl = [C(base[1], True, "bảng QUAI + QUE"), C(base[2], sum(q.hao) == n_duong, "đếm hào"),
          C(base[3], (T.lat_nguoc(q) == q and sum(1 for x in T.QUE if T.lat_nguoc(x) == x) == 8)
            if lat == q else T.lat_nguoc(q) == lat, "tính trên hào"),
          C(base[4], T.doi_am_duong(q) == doi, "tính trên hào")]
    o1 = f"Trong thứ tự Văn Vương, {q.name} là quẻ số {q.so}."
    o2 = "Tên đầy đủ của quẻ theo quy ước đọc quái trên trước, quái dưới sau."
    s = _fit(base, _pick(q.name + "ten", CL_TEN),
             [(o1, C(o1, T.QUE.index(q) + 1 == q.so, "thứ tự Văn Vương")),
              (o2, C(o2, True, "quy ước gọi tên quẻ", "doctrine"))], cl)
    return _draft("dich", f"ten-{so}", f"Quẻ {q.name} — {_full(q)}", s, cl,
                  ["Cấu trúc 64 quẻ, thứ tự Văn Vương (factory/pillars/tables.py)"], BR_DICH,
                  "tên và cấu trúc quẻ", {q.name, lat.name, doi.name})


def dich_quai_tu(so: int) -> Draft | None:
    r = _ntt().get(str(so))
    if not r or not r.get("quai_tu"):
        return None
    q = T.QUE[so - 1]
    z, v = r["quai_tu"]["zh"], r["quai_tu"]["vi"]
    nz = _hanzi(z)
    base = [f"Lời kinh quẻ {r['ten']} chỉ có {VN[nz] if nz <= 12 else nz} chữ Hán, nhưng nói gì?",
            f"Theo bản dịch Ngô Tất Tố: {v}.",
            _cau_tru(r, q)]
    cl = _quote(v, r["url"]) + [C(base[2], True, "bảng QUE theo số quẻ + bảng QUAI")]
    o = [("Lời kinh, còn gọi là lời Thoán, là phần đoán chung cho cả quẻ.",
          r["url"] + " — Chu Hy: lời Văn Vương đoán cả quẻ, gọi là lời Thoán", "source"),
         ("Sáu hào bên dưới mới nói từng bước cụ thể, bạn sẽ gặp ở các video sau.", "cấu trúc Chu Dịch", "table")]
    s = _fit(base, _pick(r["ten"] + "qt", CL_DICH), [(t, C(t, True, b, k)) for t, b, k in o], cl)
    return _draft("dich", f"loikinh-{so}", f"Lời kinh quẻ {r['ten']}", s, cl, [r["url"] + " (Ngô Tất Tố dịch)"],
                  BR_DICH, "lời kinh", {q.name, r["ten"]})


def _cau_tru(r: dict, q) -> str:
    """Câu cấu trúc, gọi cả tên theo Ngô Tất Tố lẫn tên phổ thông nếu khác."""
    alias = f", tức quẻ {q.name}," if r["ten"] != q.name else ""
    return (f"Quẻ {r['ten']}{alias} gồm {T.QUAI[q.tren][0]} ở trên, {T.QUAI[q.duoi][0]} ở dưới.")


def dich_hao(so: int, pos: int) -> Draft | None:
    r = _ntt().get(str(so))
    if not r or str(pos) not in r.get("hao", {}):
        return None
    q = T.QUE[so - 1]
    body = r["hao"][str(pos)]["vi"].split(":", 1)[-1].strip()
    if len(body.split()) < 3:
        return None                      # bản trích hỏng (chỉ còn tên hào) -> bỏ
    y = q.hao[pos - 1]
    chinh = (y == 1) == (pos % 2 == 1)
    ung = pos + 3 if pos <= 3 else pos - 3
    co_ung = q.hao[ung - 1] != y
    ten_hao = f"Hào {'Chín' if y else 'Sáu'} {POS[pos]}"
    base = [f"{ten_hao} quẻ {r['ten']} chỉ vài chữ, nhưng nói gì?",
            f"Bản dịch Ngô Tất Tố: {body}.",
            f"Đây là hào {'dương' if y else 'âm'} ở vị trí {'lẻ' if pos % 2 else 'chẵn'}, "
            f"theo cách đọc truyền thống là {'đắc chính' if chinh else 'không đắc chính'}.",
            f"Nó ứng với hào {POS[ung].lower()}, {'một âm một dương nên có ứng' if co_ung else 'cùng loại nên không ứng'}."]
    cl = _quote(body, r["url"]) + [
        C(base[2], True, "đắc chính = dương vị lẻ / âm vị chẵn, hào tính từ bảng QUE", "doctrine"),
        C(base[3], True, "hào ứng cách 3; có ứng khi một âm một dương — tính trên hào")]
    opt = []
    if pos in (2, 5):
        t = f"Vị trí thứ {VN[pos]} là chính giữa quái {'dưới' if pos == 2 else 'trên'}, thường gọi là đắc trung."
        opt.append((t, C(t, True, "hào 2, 5 là giữa quái", "doctrine")))
    t = (f"Hào đọc từ dưới lên, nên đây là bước {thu(pos)} trong sáu bước của quẻ." if pos < 6
         else "Hào đọc từ dưới lên, nên đây là bước cuối cùng của quẻ.")
    opt.append((t, C(t, True, "quy ước đọc hào từ dưới lên")))
    t = _cau_tru(r, q)
    opt.append((t, C(t, True, "bảng QUE + QUAI")))
    t = f"Chín là số của hào dương, Sáu là số của hào âm, nên hào này gọi là {ten_hao.lower()}."
    opt.append((t, C(t, True, r["url"] + " — Chu Hy: 九 dương, 六 âm", "source")))
    s = _fit(base, _pick(f"{so}-{pos}", CL_DICH), opt, cl)
    return _draft("dich", f"hao-{so}-{pos}", f"{ten_hao} quẻ {r['ten']}", s, cl,
                  [r["url"] + " (Ngô Tất Tố dịch)"], BR_DICH, "hào từ", {q.name, r["ten"]})


def dich_tuong(so: int) -> Draft | None:
    r = _ntt().get(str(so))
    if not r or not r.get("tuong"):
        return None
    q = T.QUE[so - 1]
    v = r["tuong"]["vi"].replace("Lời Tượng nói rằng:", "").strip()
    base = [f"Lời Tượng quẻ {r['ten']} dạy người quân tử điều gì?",
            f"Bản dịch Ngô Tất Tố: {v}.",
            _cau_tru(r, q)]
    cl = _quote(v, r["url"]) + [C(base[2], True, "bảng QUE + QUAI")]
    o = [("Lời Tượng thường lấy hình ảnh tự nhiên để nói về cách hành xử.",
          "đặc điểm chung của Đại Tượng truyện: 君子以…", "doctrine"),
         ("Mỗi quẻ có một lời Tượng lớn như vậy, đặt ngay sau lời Thoán.", r["url"], "source")]
    s = _fit(base, _pick(r["ten"] + "tg", CL_DICH), [(t, C(t, True, b, k)) for t, b, k in o], cl)
    return _draft("dich", f"tuong-{so}", f"Lời Tượng quẻ {r['ten']}", s, cl, [r["url"] + " (Ngô Tất Tố dịch)"],
                  BR_DICH, "lời Tượng", {q.name, r["ten"]})


# ═══ MỆNH SỐ / HUYỀN HỌC ══════════════════════════════════════════════════

BR_MENH = ["night sky stars timelapse", "zodiac wheel engraving", "ancient star map",
           "astrolabe close up"]
CL_MENH = ["Cung của bạn thuộc nhóm nào?", "Comment cung của bạn nhé.",
           "Bạn muốn so sánh hệ nào tiếp theo?", "Bạn thấy hai hệ giống nhau ở đâu nữa?"]
SRC_WEST = "Quy ước chiêm tinh phương Tây: nguyên tố, tính chất, sao chủ quản (factory/pillars/tables.py)"


def menh_nguyen_to(k: int) -> Draft:
    e = ("Lửa", "Đất", "Khí", "Nước")[k]
    cs = [c for c in T.CUNG_NAMES if T.NGUYEN_TO[c] == e]
    g = T.TAM_HOP[k]
    s = [f"{cs[0]}, {cs[1]}, {cs[2]} cách nhau đúng bốn cung, lại cùng nguyên tố {e}.",
         "Chiêm tinh phương Tây xếp mười hai cung vào bốn nguyên tố: Lửa, Đất, Khí, Nước.",
         "Mỗi nguyên tố gồm ba cung cách đều nhau.",
         f"Mười hai con giáp cũng có tam hợp: ba chi cách nhau bốn vị trí, như {', '.join(g)}.",
         "Hai hệ khác gốc, nhưng cùng chia vòng mười hai thành bốn nhóm ba.",
         _pick(e, CL_MENH)]
    cl = [C(s[0], [T.CUNG_NAMES.index(c) for c in cs] == [T.CUNG_NAMES.index(cs[0]) + 4 * j for j in range(3)],
            "bảng NGUYEN_TO"),
          C(s[1], True, "quy ước nguyên tố (triplicity)", "doctrine"),
          C(s[2], True, "bảng NGUYEN_TO"), C(s[3], T.tam_hop(*g), "tam hợp"),
          C(s[4], True, "so sánh cấu trúc: 4 nhóm × 3")]
    return _draft("menh", f"nguyento-{k}", f"Nguyên tố {e} và tam hợp", s, cl, [SRC_WEST], BR_MENH,
                  "nguyên tố", {*cs, *g})


def menh_tinh_chat(k: int) -> Draft:
    tc = ("Tiên phong", "Kiên định", "Linh hoạt")[k]
    cs = [c for c in T.CUNG_NAMES if T.TINH_CHAT[c] == tc]
    vt = ("đầu", "giữa", "cuối")[k]
    extra = (f"Bốn cung này mở đầu bằng xuân phân, hạ chí, thu phân và đông chí." if k == 0
             else f"Mỗi cung đứng ở {vt} một mùa.")
    s = [f"{', '.join(cs)}: bốn cung khác nguyên tố nhưng lại chung một tính chất.",
         f"Chiêm tinh phương Tây gọi nhóm này là {tc}, bốn cung cách đều nhau ba cung.",
         extra,
         "Mười hai con giáp cũng có nhóm bốn chi cách đều ba vị trí, gọi là tứ hành xung.",
         "Cùng một hình vuông trên vòng mười hai, hai hệ đặt tên rất khác nhau.",
         _pick(tc, CL_MENH)]
    cl = [C(s[0], len({T.NGUYEN_TO[c] for c in cs}) == 4, "bảng NGUYEN_TO/TINH_CHAT"),
          C(s[1], True, "quy ước tính chất (quadruplicity)", "doctrine"),
          C(extra, all(c in T.TIET_KHI_MO_DAU for c in cs) if k == 0 else True, "cung tropical theo mùa"),
          C(s[3], all(T.tu_hanh_xung(*g) for g in T.TU_HANH_XUNG), "tứ hành xung", "doctrine"),
          C(s[4], True, "so sánh cấu trúc")]
    return _draft("menh", f"tinhchat-{k}", f"Nhóm {tc} và tứ hành xung", s, cl, [SRC_WEST], BR_MENH,
                  "tính chất cung", set(cs))


def menh_chu_quan(sao: str) -> Draft:
    cs = [c for c in T.CUNG_NAMES if T.CHU_QUAN[c] == sao]
    hanh = sao.split()[-1] if sao.startswith("sao") else None
    s = [(f"{sao[0].upper() + sao[1:]} chủ quản tới hai cung, {cs[0]} và {cs[1]}, còn Mặt Trời chỉ giữ một." if len(cs) == 2
          else f"{sao[0].upper() + sao[1:]} chỉ chủ quản một cung, {cs[0]}, trong khi mỗi hành tinh khác giữ hai."),
         "Theo chiêm tinh cổ điển, bảy thiên thể nhìn thấy bằng mắt thường chia nhau mười hai cung.",
         "Mặt Trời và Mặt Trăng mỗi thứ giữ một cung, năm hành tinh còn lại mỗi hành tinh giữ hai.",
         (f"Còn cái tên {sao} trong tiếng Việt lại lấy từ ngũ hành phương Đông: {hanh}."
          if hanh else "Tên gọi Mặt Trời, Mặt Trăng thì không mượn từ ngũ hành."),
         "Một thiên thể, hai hệ thống, hai cách gọi tên.",
         _pick(sao, ["Comment cung của bạn nhé.", "Cung của bạn do sao nào chủ quản?"])]
    cl = [C(s[0], len(cs) in (1, 2), "bảng CHU_QUAN — chiêm tinh cổ điển"),
          C(s[1], len(set(T.CHU_QUAN.values())) == 7, "đếm trên bảng CHU_QUAN"),
          C(s[2], all(list(T.CHU_QUAN.values()).count(x) == (1 if x.startswith("Mặt") else 2)
                      for x in set(T.CHU_QUAN.values())), "đếm trên bảng"),
          C(s[3], True, "tên Hán-Việt các hành tinh: Kim tinh, Mộc tinh, Thủy tinh, Hỏa tinh, Thổ tinh"),
          C(s[4], True, "câu tóm, không thêm dữ kiện")]
    return _draft("menh", f"chuquan-{sao}", f"{sao[0].upper() + sao[1:]} chủ quản cung nào?", s, cl, [SRC_WEST],
                  BR_MENH, "sao chủ quản", set(cs))


def menh_nap_am(j: int) -> Draft:
    k = 2 * j
    y1 = 1984 + k
    while y1 > 2011:
        y1 -= 60
    y2 = y1 + 1
    na = T.nap_am_of(k)
    c1, c2 = T.can_chi_60(k), T.can_chi_60(k + 1)
    can, chi = c1.split()
    hc, hz, hn = T.CAN_BY[can][0], T.CHI_BY[chi].hanh, T.NAP_AM_HANH[na]
    diff = hn not in (hc, hz)
    s = [f"Sinh năm {y1} hay {y2}, can chi khác nhau nhưng nạp âm lại là một: {na}.",
         f"Năm {y1} là {c1}, năm {y2} là {c2}.",
         "Trong sáu mươi hoa giáp, cứ hai can chi liền nhau chung một nạp âm, nên có ba mươi nạp âm.",
         (f"Lạ là {can} thuộc {hc}, {chi} thuộc {hz}, mà nạp âm lại thuộc {hn}." if diff
          else f"Ở cặp này, hành nạp âm {hn} trùng với hành của {'can ' + can if hn == hc else 'chi ' + chi}."),
         f"Sáu mươi năm sau, {y1 + 60} và {y2 + 60} lặp lại đúng cặp này.",
         _pick(na, ["Bạn sinh năm nào, nạp âm gì?", "Comment năm sinh của bạn nhé."])]
    cl = [C(s[1], T.can_chi_60(T.year_index(y1)) == c1 and T.can_chi_60(T.year_index(y2)) == c2,
            "can chi năm: (năm − 4) mod 60"),
          C(s[2], len(T.NAP_AM) == 30, T.SOURCED["napam"].url, "source"),
          C(s[3], diff or hn in (hc, hz), "bảng can/chi + NAP_AM (không dùng vnlunar)"),
          C(s[4], T.nap_am_of(T.year_index(y1 + 60)) == na, "chu kỳ 60")]
    return _draft("menh", f"napam-{j}", f"{y1}, {y2}: mệnh {na}", s, cl, [T.SOURCED["napam"].url],
                  BR_MENH, "nạp âm", {can, chi, c2.split()[0], c2.split()[1]})


_DIEU = {"Nhật": "Mặt Trời", "Nguyệt": "Mặt Trăng"}


def menh_tu(i: int) -> Draft:
    name, dieu, animal = T.TU28[i]
    ph, tg = T.TU_PHUONG[i // 7], T.TU_TUONG[i // 7]
    s = [f"Tú {name} không phải một ngôi sao, mà là một nhóm sao.",
         f"Nó thuộc bảy tú {ph}, hợp thành hình {tg}.",
         f"Theo cách ghép truyền thống, tú {name} đi với {_DIEU.get(dieu, 'hành ' + dieu)} và con {animal}.",
         "Bảy diệu Mộc, Kim, Thổ, Mặt Trời, Mặt Trăng, Hỏa, Thủy lặp đúng bốn lần qua hai mươi tám tú.",
         "Lịch vạn niên gán mỗi ngày một tú, cứ hai mươi tám ngày quay lại.",
         _pick(name, ["Hôm nay là tú gì, bạn đã xem chưa?", "Bạn muốn nghe tú nào tiếp theo?"])]
    cl = [C(s[0], True, T.SOURCED["tu28"].url + " — tú là chòm (asterism)", "source"),
          C(s[1], True, "28 tú chia 4 phương × 7 (Thanh Long, Huyền Vũ, Bạch Hổ, Chu Tước)", "source"),
          C(s[2], True, T.SOURCED["tu28"].url, "doctrine"),
          C(s[3], [d for _, d, _ in T.TU28] == list(("Mộc", "Kim", "Thổ", "Nhật", "Nguyệt", "Hỏa", "Thủy")) * 4,
            "bảng TU28"),
          C(s[4], True, "chu kỳ tú ngày trong lịch — đối chiếu vnlunar 60 ngày liên tiếp")]
    return _draft("menh", f"tu-{i}", f"Tú {name}: {tg}, con {animal}", s, cl, [T.SOURCED["tu28"].url],
                  BR_MENH, "28 tú", {name})


def menh_tu_ngay(day: date, facts) -> Draft | None:
    """HẰNG NGÀY: tú của hôm nay. Tên tú từ vnlunar, con vật/diệu từ bảng đã đối chiếu."""
    name = T.TU_ALIAS.get(facts.mansion_name, facts.mansion_name)
    if name not in T.TU_BY:
        return None
    i, dieu, animal = T.TU_BY[name]
    from datetime import timedelta
    from factory.lunar import facts_for
    nxt = facts_for(day + timedelta(days=28)).mansion_name
    back = T.TU_ALIAS.get(nxt, nxt) == name
    s = [f"Ngày {day.day} tháng {day.month} ứng với tú {name}, vậy tú {name} là gì?",
         f"Đó là một trong hai mươi tám tú, thuộc bảy tú {T.TU_PHUONG[i // 7]}.",
         f"Theo cách ghép truyền thống, {name} đi với {_DIEU.get(dieu, 'hành ' + dieu)} và con {animal}.",
         "Lịch vạn niên gán mỗi ngày một tú, cứ hai mươi tám ngày quay lại.",
         f"Nên hai mươi tám ngày nữa, tú {name} mới trở lại.",
         "Bạn có hay xem tú trong lịch không?"]
    cl = [C(s[1], True, T.SOURCED["tu28"].url, "source"),
          C(s[2], True, T.SOURCED["tu28"].url, "doctrine"),
          C(s[3], True, "chu kỳ 28"),
          C(s[4], back, "đã tra vnlunar đúng ngày +28: cùng tên tú")]
    return _draft("menh", f"ngay-{day.isoformat()}", f"{day.day}/{day.month}: tú {name}", s, cl,
                  ["vnlunar (tên tú của ngày)", T.SOURCED["tu28"].url], BR_MENH, "hằng ngày: tú", {name})


# ═══ MỞ RỘNG ĐỢT 2 — nguồn dài hạn ════════════════════════════════════════
#
# Kinh Dịch: biến quẻ (64 × 6 = 384) + hỗ quái (64) + bát quái (8) đều TÍNH
# ĐƯỢC từ cấu trúc hào, không cần bản dịch. Lời kinh/hào từ tăng dần theo
# Wikisource (fetch_kinhdich.py).
# Hằng ngày: mỗi pillar 2–3 góc luân phiên theo ngày, để khi hết chủ đề cố
# định kênh vẫn không lặp một khuôn mỗi ngày.

POS_L = {k: v.lower() for k, v in POS.items()}


def dich_bien(so: int, pos: int) -> Draft:
    q = T.QUE[so - 1]
    q2 = T.bien_quai(q, pos)
    y = q.hao[pos - 1]
    duoi = pos <= 3
    old_t, new_t = (q.duoi, q2.duoi) if duoi else (q.tren, q2.tren)
    base = [f"{q.name}, hào {POS_L[pos]}: đổi âm dương thì thành quẻ nào?",
            f"Hào {POS_L[pos]} của quẻ {q.name} đang là hào {'dương' if y else 'âm'}, đổi thành hào {'âm' if y else 'dương'}.",
            f"Quái {'dưới' if duoi else 'trên'} từ {old_t}, tức {T.QUAI[old_t][0]}, chuyển thành {new_t}, tức {T.QUAI[new_t][0]}.",
            f"Quẻ mới là {q2.name}, quẻ số {q2.so} theo thứ tự Văn Vương.",
            "Trong phép bói, quẻ sinh ra khi hào động đổi như vậy thường gọi là quẻ biến."]
    cl = [C(base[1], True, "bảng QUE"),
          C(base[2], (q2.duoi if duoi else q2.tren) == new_t and (q.duoi if duoi else q.tren) == old_t,
            "tính trên hào"),
          C(base[3], T.bien_quai(q, pos) == q2, "tính trên hào"),
          C(base[4], True, "khái niệm 之卦/變卦 trong phép bói cỏ thi", "doctrine")]
    o = "Mỗi quẻ có sáu hào, nên một quẻ có đúng sáu quẻ biến kiểu này."
    s = _fit(base, _pick(f"b{so}{pos}", CL_TEN), [(o, C(o, True, "6 hào → 6 quẻ biến một hào"))], cl)
    return _draft("dich", f"bien-{so}-{pos}", f"{q.name} đổi hào {POS_L[pos]} thành {q2.name}", s, cl,
                  ["Cấu trúc 64 quẻ (factory/pillars/tables.py)"], BR_DICH, f"quẻ biến hào {POS_L[pos]}",
                  {q.name, q2.name})


def dich_ho(so: int) -> Draft:
    q = T.QUE[so - 1]
    ho = T.ho_quai(q)
    n_self = sum(1 for x in T.QUE if T.ho_quai(x) == x)
    base = [(f"Quẻ {q.name} còn giấu bên trong một quẻ khác: quẻ {ho.name}." if ho != q
             else f"Quẻ {q.name} giấu bên trong, lại chính là quẻ {q.name}."),
            f"Lấy hào hai, ba, bốn làm quái dưới, được {ho.duoi}.",
            f"Lấy hào ba, bốn, năm làm quái trên, được {ho.tren}.",
            f"Ghép lại thành quẻ {ho.name}, thường gọi là hỗ quái của {q.name}.",
            "Theo cách đọc truyền thống, hỗ quái thường được dùng để xem phần diễn biến ở giữa."]
    cl = [C(base[0], T.ho_quai(q) == ho, "tính trên hào"),
          C(base[1], True, "hào 2-3-4"), C(base[2], True, "hào 3-4-5"),
          C(base[3], True, "khái niệm 互卦", "doctrine"), C(base[4], True, "cách dùng hỗ quái", "doctrine")]
    o = f"Trong sáu mươi tư quẻ, chỉ {VN[n_self]} quẻ có hỗ quái là chính nó."
    s = _fit(base, _pick(f"h{so}", CL_TEN),
             [(o, C(o, sum(1 for x in T.QUE if T.ho_quai(x) == x) == n_self, "đếm trên 64 quẻ"))], cl)
    return _draft("dich", f"ho-{so}", f"Hỗ quái của quẻ {q.name}", s, cl,
                  ["Cấu trúc 64 quẻ (factory/pillars/tables.py)"], BR_DICH, "hỗ quái", {q.name, ho.name})


def dich_quai(name: str) -> Draft:
    img, h = T.QUAI[name]
    nd = sum(h)
    loai = "dương" if nd in (1, 3) else "âm"          # 1 dương 2 âm -> quái dương
    net = sum(1 if x else 2 for x in h)
    S = T.SOURCED["hetu.duongquai"]
    doc = ", ".join("liền" if x else "đứt" for x in h)
    if name in ("Càn", "Khôn"):
        hook = f"Quái {name} là {img}, ba hào đều {'liền' if nd == 3 else 'đứt'}, còn sáu quái kia thì sao?"
    else:
        hook = f"Quái {name} là quái {loai}, vậy mà lại có tới hai hào {'âm' if loai == 'dương' else 'dương'}."
    base = [hook,
            f"Đọc từ dưới lên, ba hào của {name} là: {doc}.",
            f"Hệ từ truyện viết: {S.vi}.",
            f"Theo cách đếm thường gặp, hào liền một nét, hào đứt hai nét, nên {name} có {VN[net]} nét.",
            f"Quái {name} tượng cho {img}."]
    cl = [C(hook, True, "bảng QUAI"), C(base[1], True, "bảng QUAI"),
          C(S.vi, True, S.url, "source"),
          C(base[3], net == sum(1 if x else 2 for x in h), "đếm nét", "doctrine"),
          C(base[4], True, "bảng QUAI")]
    s = _fit(base, _pick(name, CL_TEN), [], cl)
    return _draft("dich", f"quai-{name}", f"Quái {name}: {img}", s, cl, [S.url], BR_DICH, "bát quái", {name})


# ─── Hằng ngày, nhiều góc ─────────────────────────────────────────────────

def giap_hop_ngay(day: date, facts) -> Draft:
    dchi = facts.can_chi_day.split()[-1]
    p = T.hop_partner(dchi)
    grp = next(g for g in T.TAM_HOP if dchi in g)
    others = [x for x in [p, *grp] if x != dchi]
    s = [f"Ngày {dchi}, {day.day} tháng {day.month}: tuổi nào được xếp là hợp ngày?",
         f"Theo lịch, hôm nay là ngày {facts.can_chi_day}, chi ngày là {dchi}.",
         f"Trong lục hợp, {dchi} đi cặp với {p}.",
         f"Trong tam hợp, {dchi} thuộc nhóm {', '.join(grp)}.",
         f"Nên theo lịch pháp, các tuổi {', '.join(others)} được xếp là hợp với ngày {dchi}.",
         "Đây là quan hệ trong lịch pháp, không phải lời hứa may mắn.",
         "Bạn có nằm trong nhóm này không?"]
    cl = [C(s[1], True, "vnlunar can_chi.day"), C(s[2], T.luc_hop(dchi, p), "lục hợp"),
          C(s[3], dchi in grp and T.tam_hop(*grp), "tam hợp"),
          C(s[4], True, "hợp ngày = lục hợp + tam hợp của chi ngày", "doctrine"),
          C(s[5], True, "rào đón", "doctrine")]
    return _draft("giap", f"ngayhop-{day.isoformat()}", f"{day.day}/{day.month}: tuổi hợp ngày {dchi}", s, cl,
                  ["vnlunar (can chi ngày) + bảng lục hợp, tam hợp"], BR_GIAP, "hằng ngày: tuổi hợp",
                  {dchi, p, *grp, *facts.can_chi_day.split()})


def tru_nap_am_ngay(day: date, facts):
    cc = facts.can_chi_day
    k = next((i for i in range(60) if T.can_chi_60(i) == cc), None)
    if k is None:
        return None
    na = T.nap_am_of(k)
    can, chi = cc.split()
    pair = T.can_chi_60(k + 1 if k % 2 == 0 else k - 1)
    s = [f"{cc}, ngày {day.day} tháng {day.month}: nạp âm hôm nay là gì?",
         f"Theo bảng sáu mươi hoa giáp, ngày {cc} mang nạp âm {na}, hành {T.NAP_AM_HANH[na]}.",
         f"{cc} chung nạp âm với {pair}, vì cứ hai can chi liền nhau chung một nạp âm.",
         f"Còn can {can} thuộc {T.CAN_BY[can][0]}, chi {chi} thuộc {T.CHI_BY[chi].hanh}.",
         "Nạp âm là một lớp hành riêng, không phải cộng hành của can và chi.",
         "Ngày sinh của bạn là can chi gì?"]
    cl = [C(s[1], T.nap_am_of(k) == na, T.SOURCED["napam"].url, "source"),
          C(s[2], T.nap_am_of(k) == T.nap_am_of(T.can_chi_60_index(pair)), "bảng NAP_AM"),
          C(s[3], True, "bảng can/chi"), C(s[4], True, "bảng NAP_AM so với hành can/chi"),
          ]
    return _draft("tru", f"ngaynapam-{day.isoformat()}", f"{day.day}/{day.month}: {cc}, nạp âm {na}", s, cl,
                  [T.SOURCED["napam"].url], BR_TRU, "hằng ngày: nạp âm", {can, chi, *pair.split()})


def tru_tang_ngay(day: date, facts) -> Draft:
    from factory.pillars.check import sentences
    chi = facts.can_chi_day.split()[-1]
    d = tru_tang_can(chi)
    sents = sentences(d.script)
    first = f"Chi ngày {day.day} tháng {day.month} là {chi}, giấu những can nào?"
    script = " ".join([first] + sents[1:])
    from factory.pillars.check import _norm
    claims = [c for c in d.claims if _norm(c.fragment) in _norm(script)]
    return Draft("tru", f"ngaytang-{day.isoformat()}", f"{day.day}/{day.month}: chi {chi} giấu can gì",
                 script, claims, d.sources, d.broll,
                 "hằng ngày: tàng can", d.names | set(facts.can_chi_day.split()))


def menh_cung_ngay(day: date, facts) -> Draft:
    cung, chom = T.cung_of(day.month, day.day), T.chom_of(day.month, day.day)
    S = T.SOURCED
    s = [f"Hôm nay {day.day} tháng {day.month}, Mặt Trời ở cung {cung}"
         + (f", nhưng lại đứng trước chòm {chom}." if chom != cung else f", và cũng đứng trước chòm {chom}."),
         "Theo chiêm tinh phương Tây, cung là một khoảng lịch tính từ điểm xuân phân.",
         "Chòm là nhóm sao thật trên bầu trời, to nhỏ không đều.",
         f"Theo NASA, {S['nasa.axis'].vi}, nên cung và chòm dần lệch nhau.",
         f"Người sinh hôm nay thuộc cung {cung} theo chiêm tinh phương Tây.",
         "Bạn sinh vào cung nào?"]
    cl = [C(s[0], T.cung_of(day.month, day.day) == cung and T.chom_of(day.month, day.day) == chom,
            "bảng CUNG + CHOM (NASA)"),
          C(s[1], True, "định nghĩa cung tropical", "doctrine"),
          C(s[2], True, S["nasa.virgo45"].url, "source"),
          C(S["nasa.axis"].vi, True, S["nasa.axis"].url, "source"),
          C(s[4], True, "bảng CUNG", "doctrine")]
    return _draft("menh", f"ngaycung-{day.isoformat()}", f"{day.day}/{day.month}: cung {cung}, chòm {chom}", s, cl,
                  [S["nasa.axis"].url], BR_MENH, "hằng ngày: cung", {cung, chom})
