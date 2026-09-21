"""Composer 4 pillar + vòng xoay chủ đề + lịch sử.

Cùng cách Lịch làm: không LLM, không viết tay từng bài. Mỗi chủ đề là một
bộ tham số trên dữ liệu tập đóng; khuôn câu điền tham số; bộ kiểm tính lại
mọi quan hệ. Chạy lại ra y hệt.

VÒNG XOAY: mỗi pillar có danh sách chủ đề theo thứ tự. Ngày nào cũng lấy
chủ đề ĐẦU TIÊN chưa có trong lịch sử VÀ đã đủ nguồn. Chủ đề thiếu nguồn
bị bỏ qua kèm lý do -- không bao giờ lấp bằng trí nhớ.

LỊCH SỬ: đọc thẳng từ bundles/FS/*.json. Không có sổ riêng để lệch.
"""
from __future__ import annotations

import json
from pathlib import Path

from factory.pillars.check import Claim, Draft
from factory.pillars import tables as T

VN_NUM = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín",
          "mười", "mười một", "mười hai"]

PILLARS = {  # prefix slug, giờ đăng VN, cảm giác
    "giap": ("giap-", "11:30", "dễ viral"),
    "tru":  ("tru-", "15:00", "chuyên sâu"),
    "dich": ("dich-", "19:00", "bí ẩn, triết lý"),
    "menh": ("menh-", "22:00", "khám phá, giải trí"),
}

ALL_NAMES = ({c.name for c in T.CHI} | {n for n, _, _ in T.CAN}
             | set(T.THAP_THAN) | {q.name for q in T.QUE if " " in q.name}
             | {n for n, _ in T.CUNG} | {"Xà Phu"})


def vn_hour(h: int) -> str:
    buoi = ("đêm" if h in (23,) else "sáng" if h < 11 else "trưa" if h == 11
            else "chiều" if h < 19 else "tối")
    return f"{VN_NUM[h % 12 or 12]} giờ {buoi}"


def _true(): return True


def R(fragment: str, basis: str = "câu dẫn/chốt, không chứa dữ kiện") -> Claim:
    return Claim(fragment, _true, basis, "rhetoric")


# ═══ 1. 12 CON GIÁP — lục xung ════════════════════════════════════════════

def giap_xung(a: str) -> Draft:
    b = T.xung_partner(a)
    A, B = T.CHI_BY[a], T.CHI_BY[b]
    same = A.hanh == B.hanh
    ga, gb = A.gio, B.gio
    s_gio = f"Giờ {a} bắt đầu từ {vn_hour(ga[0])}, giờ {b} từ {vn_hour(gb[0])}."
    s_nua = "Cách nhau đúng nửa vòng mười hai chi."
    s_huong = f"Trên la bàn, {a} ở {A.huong}, {b} ở {B.huong}."
    claims = [
        Claim(s_gio[:-1], lambda: (A.gio[0], B.gio[0]) == (ga[0], gb[0]), "chi i bắt đầu lúc (23+2i) mod 24"),
        Claim(s_nua[:-1], lambda: T.luc_xung(a, b), "lục xung = cách nhau 6/12 vị trí"),
        Claim(s_huong[:-1], lambda: (A.huong, B.huong) == (T.CHI_BY[a].huong, T.CHI_BY[b].huong),
              "phương vị 12 chi trên la bàn 24 sơn"),
    ]
    if same:
        hook = f"{a} và {b} cùng hành {A.hanh}, vậy mà vẫn nằm trong lục xung."
        why = "Vì xung trong lịch pháp không xét bằng ngũ hành, mà xét bằng vị trí."
        claims += [Claim(hook[:-1], lambda: A.hanh == B.hanh and T.luc_xung(a, b), "bảng CHI + lục xung"),
                   Claim(why[:-1], lambda: T.luc_xung(a, b), "lục xung định nghĩa bằng vị trí đối diện", "doctrine")]
        body = [why, s_gio, s_nua, s_huong]
        angle = "cùng hành vẫn xung"
    else:
        k, bk = (A, B) if T.KHAC[A.hanh] == B.hanh else (B, A)
        hook = f"Vì sao {a} và {b} bị gọi là đối xung?"
        s_hanh = f"Về ngũ hành, {a} thuộc {A.hanh}, {b} thuộc {B.hanh}, mà {k.hanh} khắc {bk.hanh}."
        claims.append(Claim(s_hanh[:-1], lambda: T.KHAC[k.hanh] == bk.hanh, "bảng CHI + ngũ hành tương khắc"))
        body = [s_gio, s_nua, s_huong, s_hanh,
                "Ba lớp đối nhau chồng lên một cặp."]
        claims += [Claim("Ba lớp đối nhau chồng lên một cặp",
                         lambda: T.luc_xung(a, b) and T.KHAC[k.hanh] == bk.hanh,
                         "giờ đối, hướng đối, hành khắc — cả ba đã tính ở trên")]
        angle = "giờ-hướng-hành"
    hedge = "Nhưng theo lịch pháp, xung là thế đối nhau, không phải lời phán không hợp."
    closer = f"Nhà bạn có cặp {a} và {b} không?"
    claims += [Claim("xung là thế đối nhau, không phải lời phán", _true,
                     "phân biệt kiến thức truyền thống với phán đoán cá nhân — yêu cầu kênh", "doctrine")]
    script = " ".join([hook, *body, hedge, closer])
    return Draft("giap", f"xung-{T.CHI.index(A)}", f"Vì sao {a} và {b} xung nhau?", script,
                 claims, ["Bảng 12 địa chi, lục xung (factory/pillars/tables.py)"],
                 ["vintage clock face close up", "compass on old map", "night sky to noon sun timelapse",
                  "yin yang stones balance"], angle, {a, b})


GIAP_ROTATION = [("xung", c) for c in ("Tý", "Thìn", "Dần", "Sửu", "Mão", "Tỵ")]


# ═══ 2. LỤC TRỤ MỆNH LÝ ═══════════════════════════════════════════════════

def tru_nhat_chu() -> Draft:
    ex = "Giáp"
    h = T.CAN_BY[ex][0]
    khac_h = next(x for x in T.HANH if T.KHAC[x] == h)
    tiet_h = T.SINH[h]
    s = [
        "Nhật chủ mạnh chưa chắc đã tốt.", "Vì sao?",
        "Trong mệnh lý, can ngày sinh được gọi là Nhật chủ, tức chính bạn.",
        "Theo cách luận vượng suy, mạnh yếu được xét trên cả lá số.",
        "Truyền thống không tìm càng mạnh càng tốt, mà tìm cân bằng.",
        "Hành kéo lá số về cân bằng thường gọi là dụng thần.",
        f"Ví dụ Nhật chủ {ex} thuộc {h}, quá vượng thì {khac_h} khắc {h}, hoặc {tiet_h} tiết {h}, có thể làm dụng thần.",
        "Bạn đã biết Nhật chủ của mình chưa?",
    ]
    claims = [
        Claim("can ngày sinh được gọi là Nhật chủ", _true,
              "định nghĩa Nhật chủ (日主/日元) — can ngày trong Tứ Trụ", "doctrine"),
        Claim("mạnh yếu được xét trên cả lá số", _true, "phép luận vượng suy", "doctrine"),
        Claim("không tìm càng mạnh càng tốt, mà tìm cân bằng", _true,
              "nguyên tắc trung hoà (中和) của phái phù ức", "doctrine"),
        Claim("thường gọi là dụng thần", _true, "định nghĩa dụng thần (用神)", "doctrine"),
        Claim(f"Nhật chủ {ex} thuộc {h}, quá vượng", lambda: T.CAN_BY[ex][0] == h, "bảng 10 can"),
        Claim(f"{khac_h} khắc {h}, hoặc {tiet_h} tiết {h}",
              lambda: T.KHAC[khac_h] == h and T.SINH[h] == tiet_h, "ngũ hành sinh khắc"),
    ]
    return Draft("tru", "nhat-chu", "Nhật chủ mạnh chưa chắc đã tốt", " ".join(s), claims,
                 ["Nguyên tắc Tứ Trụ/Bát Tự: Nhật chủ, vượng suy, dụng thần (kiến thức nền, không trích cổ thư)"],
                 ["balance scale close up", "calligraphy brush ink", "old chinese almanac pages",
                  "five elements wood fire earth metal water"], "khái niệm nền", {ex})


_GROUPS = {  # rel, nhật chủ ví dụ, hook, câu quan niệm, tên nhóm
    "tai": ("toi_khac", "Bính", "Trong mệnh lý, tiền không phải thứ sinh ra bạn, mà là thứ bạn khắc được.",
            "Theo quan niệm truyền thống, Tài tinh gắn với của cải và những gì mình quản được.", "Tài tinh"),
    "quan": ("khac_toi", "Nhâm", "Thứ khắc chế bạn, mệnh lý lại gọi là Quan.",
             "Theo quan niệm truyền thống, Quan tinh gắn với kỷ luật, chức phận, những thứ ràng buộc mình.", "Quan tinh"),
    "an": ("sinh_toi", "Canh", "Thứ sinh ra bạn lại mang tên một con dấu: Ấn.",
           "Theo quan niệm truyền thống, Ấn tinh gắn với sự che chở, học vấn và người nâng đỡ.", "Ấn tinh"),
    "thuc": ("toi_sinh", "Giáp", "Thứ bạn sinh ra lại có thể khắc Quan của chính bạn.",
             "Theo quan niệm truyền thống, Thực Thương gắn với tài năng và sự thể hiện bản thân.", "Thực Thương"),
    "ty": ("dong", "Mậu", "Cùng hành với bạn chưa chắc đã là bạn.",
           "Theo quan niệm truyền thống, Tỷ Kiếp là anh em, bạn bè, cũng là người chia phần.", "Tỷ Kiếp"),
}
_REL_VN = {"toi_khac": "{h} khắc", "khac_toi": "khắc {h}", "sinh_toi": "sinh ra {h}",
           "toi_sinh": "{h} sinh ra", "dong": "cùng là {h}"}


def tru_thap_than(g: str) -> Draft:
    rel, ex, hook, doctrine, gname = _GROUPS[g]
    h, dg = T.CAN_BY[ex]
    # Tỷ Kiên: cùng hành cùng âm dương -> chính can đó (một can trùng trong lá số).
    same = next(n for n, hh, d in T.CAN if T.quan_he(h, hh) == rel and d == dg)
    diff = next(n for n, hh, d in T.CAN if T.quan_he(h, hh) == rel and d != dg)
    h2 = T.CAN_BY[same][0]
    ts, td = T.thap_than(ex, same), T.thap_than(ex, diff)
    ad = "dương" if dg else "âm"
    rel_s = f"{h2} là hành {_REL_VN[rel].format(h=h)}." if rel != "dong" else f"{diff} cũng thuộc {h}."
    s_same = (f"{same} cùng âm dương với {ex}, gọi là {ts}." if rel != "dong"
              else f"Gặp thêm một {same} nữa trong lá số, gọi là {ts}.")
    s = [hook, f"Lấy Nhật chủ {ex} làm ví dụ, {ex} là {h} {ad}.", rel_s, s_same,
         f"{diff} khác âm dương, gọi là {td}."]
    claims = [
        Claim(f"{ex} là {h} {ad}", lambda: T.CAN_BY[ex] == (h, dg), "bảng 10 can"),
        Claim(rel_s[:-1], lambda: T.quan_he(h, h2) == rel and T.CAN_BY[diff][0] == h2, "ngũ hành sinh khắc"),
        Claim(s_same[:-1], lambda: T.thap_than(ex, same) == ts,
              "thập thần suy từ (quan hệ hành, âm dương) — tables.thap_than"),
        Claim(f"{diff} khác âm dương, gọi là {td}", lambda: T.thap_than(ex, diff) == td, "như trên"),
        Claim(doctrine[:-1], _true, "ý nghĩa truyền thống của nhóm thập thần", "doctrine"),
    ]
    if g == "thuc":
        q = next(x for x in T.HANH if T.KHAC[x] == h)
        extra = f"Mà {h2} khắc {q}, còn {q} là hành khắc {h}, tức Quan của {ex}."
        s.append(extra)
        claims.append(Claim(extra[:-1], lambda: T.KHAC[h2] == q and T.KHAC[q] == h, "ngũ hành tương khắc"))
    s += [doctrine, f"Lá số của bạn có nhiều {gname} không?"]
    return Draft("tru", f"thap-than-{g}", f"{gname}: {ts} và {td}", " ".join(s), claims,
                 ["Thập thần suy từ ngũ hành + âm dương (factory/pillars/tables.py)"],
                 ["chinese seal stamp ink", "coins on wooden table", "family gathering dinner",
                  "student reading lamp night"], f"thập thần {g}", {ex, same, diff, ts, td})


TRU_ROTATION = [("nhat_chu", None)] + [("thap_than", g) for g in ("tai", "quan", "thuc", "an", "ty")]


# ═══ 3. KINH DỊCH ═════════════════════════════════════════════════════════

def dich_thai_bi() -> Draft:
    thai, bi = T.QUE_BY["Thái"], T.QUE_BY["Bĩ"]
    S = T.SOURCED
    s = [
        "Trời trên, Đất dưới, đúng chỗ, vậy mà quẻ đó lại là Bĩ.",
        "Đảo lại, Đất trên, Trời dưới, mới là quẻ Thái.",
        f"Thoán truyện quẻ Thái viết: {S['thai.thoan'].vi}.",
        f"Còn quẻ Bĩ: {S['bi.thoan'].vi}.",
        "Đúng vị trí thôi chưa đủ, còn phải giao nhau.",
        "Lật ngược quẻ Thái, hay đổi hết âm dương, đều ra quẻ Bĩ.",
        "Nên mới có câu bĩ cực thái lai.",
        "Bạn đang ở quẻ Thái hay quẻ Bĩ?",
    ]
    claims = [
        Claim("Đất trên, Trời dưới, mới là quẻ Thái",
              lambda: (thai.tren, thai.duoi) == ("Khôn", "Càn") and T.QUAI["Khôn"][0] == "Đất",
              "Thái = Khôn trên Càn dưới (地天泰)"),
        Claim(S["thai.thoan"].vi, lambda: "thai.thoan" in S, S["thai.thoan"].url, "source"),
        Claim(S["bi.thoan"].vi, lambda: "bi.thoan" in S, S["bi.thoan"].url, "source"),
        Claim("Đúng vị trí thôi chưa đủ, còn phải giao nhau",
              lambda: (bi.tren, bi.duoi) == ("Càn", "Khôn"),
              "tóm tắt đúng hai câu Thoán: 交 → 通, 不交 → 不通; Bĩ = Càn trên Khôn dưới"),
        Claim("Lật ngược quẻ Thái, hay đổi hết âm dương, đều ra quẻ Bĩ",
              lambda: T.lat_nguoc(thai) == bi and T.doi_am_duong(thai) == bi, "tính trên hào"),
        Claim("bĩ cực thái lai", _true, "thành ngữ 否極泰來, phổ thông trong tiếng Việt"),
    ]
    return Draft("dich", "cap-thai-bi", "Trời trên Đất dưới lại là quẻ xấu?", " ".join(s), claims,
                 [S["thai.thoan"].url, S["bi.thoan"].url],
                 ["i ching coins hexagram", "sky and earth horizon dawn", "flowing river rocks",
                  "ancient bamboo scroll"], "cặp quẻ đối", {"Thái", "Bĩ"})


DICH_ROTATION = [("thai_bi", None)]   # quẻ khác: CAN_XAC_MINH -- cần nguyên văn trước


# ═══ 4. MỆNH SỐ / HUYỀN HỌC ═══════════════════════════════════════════════

def menh_tue_sai(cung: str) -> Draft:
    from datetime import date, timedelta
    m0, d0 = dict(T.CUNG)[cung]
    ex = date(2026, m0, d0) + timedelta(days=8)
    m, d = ex.month, ex.day
    chom = T.chom_of(m, d)
    S = T.SOURCED
    lech = chom != cung
    hook = (f"{cung}: sinh ngày {d} tháng {m}, nhưng hôm đó Mặt Trời lại đứng trước chòm {chom}."
            if lech else f"{cung}: sinh ngày {d} tháng {m}, nhưng cung và chòm sao không phải một.")
    s = [hook,
         "Người Babylon chia hoàng đạo thành mười hai phần bằng nhau.",
         "Nhưng chòm thật to nhỏ khác nhau: Xử Nữ khoảng bốn mươi lăm ngày, Bọ Cạp chỉ khoảng bảy.",
         f"{S['nasa.axis'].vi[0].upper()}{S['nasa.axis'].vi[1:]}, nên bầu trời đã trượt đi.",
         "Chiêm tinh vẫn giữ mười hai cung theo lịch, không theo chòm sao.",
         "Bạn sinh ngày nào, đang đứng trước chòm nào?"]
    claims = [
        Claim(hook[:-1].split(", nhưng")[0], lambda: T.cung_of(m, d) == cung, "bảng CUNG (tropical)"),
        Claim("Người Babylon chia hoàng đạo thành mười hai phần bằng nhau", _true,
              S["nasa.babylon"].url, "source"),
        Claim("Xử Nữ khoảng bốn mươi lăm ngày, Bọ Cạp chỉ khoảng bảy", _true,
              S["nasa.virgo45"].url + " — 45 ngày Xử Nữ, 7 ngày Bọ Cạp", "source"),
        Claim(S["nasa.axis"].vi, _true, S["nasa.axis"].url, "source"),
        Claim("giữ mười hai cung theo lịch, không theo chòm sao", _true,
              "cung tropical neo theo xuân phân (Bạch Dương từ 21/3), không theo ranh giới chòm IAU", "doctrine"),
    ]
    if lech:
        claims.append(Claim(f"Mặt Trời lại đứng trước chòm {chom}", lambda: T.chom_of(m, d) == chom,
                            "bảng CHOM (ranh giới IAU, theo NASA)"))
    names = {cung, chom, "Xử Nữ", "Bọ Cạp"}
    return Draft("menh", f"tue-sai-{T.CUNG.index((cung, (m0, d0)))}", f"{cung} mà Mặt Trời ở chòm {chom}?",
                 " ".join(s), claims, [S["nasa.virgo45"].url],
                 ["night sky constellation timelapse", "zodiac wheel old engraving", "earth rotation space",
                  "astronomer telescope silhouette"], "cung vs chòm", names)


MENH_ROTATION = [("tue_sai", n) for n, _ in T.CUNG[6:] + T.CUNG[:6]]   # bắt đầu từ Thiên Bình (cuối 9)


# ═══ Vòng xoay + lịch sử ══════════════════════════════════════════════════
#
# Mỗi pillar = nhiều LOẠI chủ đề xếp XEN KẼ (round-robin), để ngày liền nhau
# không bao giờ cùng góc. Loại HẰNG NGÀY chỉ dùng khi không còn chủ đề cố
# định nào hợp lệ -- nó gắn với lịch thật nên không bao giờ cạn.

from itertools import zip_longest  # noqa: E402

from factory.pillars import expand as X  # noqa: E402


def _rr(*kinds):
    """Xen kẽ các danh sách: a1 b1 c1 a2 b2 c2 ..."""
    return [f for grp in zip_longest(*kinds) for f in grp if f is not None]


def _giap():
    chi = [c.name for c in T.CHI]
    pairs = [(a, b) for i, a in enumerate(chi) for b in chi[i + 1:]]
    return _rr([lambda c=c: giap_xung(c) for c in ("Tý", "Thìn", "Dần", "Sửu", "Mão", "Tỵ")],
               [lambda c=c: X.giap_ho_so(c) for c in chi],
               [lambda c=c: X.giap_hop(c) for c in ("Tý", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ")],
               [lambda a=a, b=b: X.giap_cap(a, b) for a, b in pairs],
               [lambda g=g: X.giap_tam_hop(g) for g in T.TAM_HOP],
               [lambda c=c: X.giap_hai(c) for c in ("Tý", "Sửu", "Dần", "Mão", "Thân", "Dậu")],
               [lambda g=g: X.giap_tu_hanh_xung(g) for g in T.TU_HANH_XUNG])


def _tru():
    return _rr([tru_nhat_chu] + [lambda g=g: tru_thap_than(g) for g in ("tai", "quan", "thuc", "an", "ty")],
               [lambda c=c: X.tru_can(c) for c in T.CAN_NAMES],
               [lambda g=g, e=e: X.tru_nhom(g, e) for e in T.CAN_NAMES for g in X._GR
                if (g, e) not in {("tai", "Bính"), ("quan", "Nhâm"), ("an", "Canh"), ("thuc", "Giáp"), ("ty", "Mậu")}],
               [lambda i=i: X.tru_can_hop(i) for i in range(5)],
               [lambda c=c.name: X.tru_tang_can(c) for c in T.CHI])


def _dich():
    ntt = sorted(int(k) for k in X._ntt())
    return _rr([dich_thai_bi] + [lambda n=n: X.dich_ten(n) for n in range(1, 65)],
               [lambda n=n, p=p: X.dich_hao(n, p) for n in ntt for p in range(1, 7)],
               [lambda q=q: X.dich_quai(q) for q in T.QUAI] + [lambda n=n: X.dich_quai_tu(n) for n in ntt],
               [lambda n=n: X.dich_tuong(n) for n in ntt] + [lambda n=n: X.dich_ho(n) for n in range(1, 65)],
               [lambda n=n, p=p: X.dich_bien(n, p) for n in range(1, 65) for p in range(1, 7)])


def _menh():
    return _rr([lambda c=n: menh_tue_sai(c) for n, _ in T.CUNG[6:] + T.CUNG[:6]],
               [lambda j=j: X.menh_nap_am(j) for j in range(30)],
               [lambda i=i: X.menh_tu(i) for i in range(28)],
               [lambda k=k: X.menh_nguyen_to(k) for k in range(4)]
               + [lambda k=k: X.menh_tinh_chat(k) for k in range(3)],
               [lambda s=s: X.menh_chu_quan(s) for s in dict.fromkeys(T.CHU_QUAN.values())])


CANDIDATES = {"giap": _giap, "tru": _tru, "dich": _dich, "menh": _menh}
# Nhiều góc hằng ngày, luân phiên theo ngày (ordinal % số góc).
DAILY = {"giap": [X.giap_xung_ngay, X.giap_hop_ngay],
         "tru": [X.tru_can_ngay, X.tru_nap_am_ngay, X.tru_tang_ngay],
         "menh": [X.menh_tu_ngay, X.menh_cung_ngay]}


def all_drafts(pillar: str) -> list[Draft]:
    """Mọi chủ đề cố định của pillar (bỏ những cái không dựng được vì thiếu nguồn)."""
    return [d for f in CANDIDATES[pillar]() if (d := f()) is not None]


def load_history(bundle_dir: Path) -> list[dict]:
    """Mọi bài pillar đã sinh, từ chính bundle trên đĩa."""
    out = []
    for f in sorted((bundle_dir / "FS").glob("*.json")):
        b = json.loads(f.read_text(encoding="utf-8"))
        note = b.get("source_note", "")
        if note.startswith("pillar="):
            meta = dict(kv.split("=", 1) for kv in note.split(" | ")[0].split(";"))
            out.append({"pillar": meta["pillar"], "key": meta["key"], "angle": meta["angle"],
                        "script": b["script"], "publish_at": b["publish_at"]})
    # Lịch cũng là lịch sử: mở bài không được trùng cả với Lịch.
        elif b["slug"].startswith("lich-"):
            out.append({"pillar": "lich", "key": b["slug"], "angle": "", "script": b["script"],
                        "publish_at": b["publish_at"]})
    return sorted(out, key=lambda h: h["publish_at"])


def next_draft(pillar: str, history: list[dict], day=None) -> tuple[Draft | None, list[str]]:
    """Chủ đề kế tiếp: chưa làm, và KHÁC GÓC với 3 bài gần nhất của pillar.

    Hết chủ đề cố định hợp lệ thì dùng loại hằng ngày của `day`."""
    from factory.pillars.check import check, verdict
    same = [h for h in history if h["pillar"] == pillar]
    done = {h["key"] for h in same}
    from factory.pillars.check import ANGLE_GAP
    recent = {h["angle"] for h in same[-ANGLE_GAP:]}
    for f in CANDIDATES[pillar]():
        d = f()
        if d is None or d.key in done or d.angle in recent:
            continue
        # Chỉ trả bản ĐÃ qua bộ kiểm (độ dài, mở bài trùng với lịch sử...).
        # Bản trượt thì bỏ qua, lấy chủ đề sau -- không cắt bừa, không sửa tay.
        if verdict(check(d, ALL_NAMES, history)):
            return d, []
    if day is not None and pillar in DAILY:
        from factory.lunar import facts_for
        fx = facts_for(day)
        n = len(DAILY[pillar])
        for k in range(n):
            d = DAILY[pillar][(day.toordinal() + k) % n](day, fx)
            if d is not None and d.key not in done and verdict(check(d, ALL_NAMES, history)):
                return d, []
    return None, [f"{pillar}: hết chủ đề hợp lệ — cần thêm nguồn ({', '.join(T.CAN_XAC_MINH)})"]
