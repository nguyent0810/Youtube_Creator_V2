"""Dữ liệu TẬP ĐÓNG cho 4 pillar — bài học lớn nhất từ Lịch, dùng lại.

Lịch chạy không người được là nhờ vốn từ hữu hạn (12 trực, 12 sao) khai
một lần. Bốn pillar mới cũng vậy: 12 chi, 10 can, 5 hành, 8 quái, 64 quẻ,
12 cung. Không có cái thứ 13. Khai đủ ở đây thì mọi quan hệ trong kịch bản
(xung, hợp, hại, thập thần, cặp quẻ) đều TÍNH LẠI ĐƯỢC -- bộ kiểm không tin
lời kịch bản, nó tự suy ra rồi so.

Thứ KHÔNG suy ra được (lời quẻ, lời Thoán, ngày Mặt Trời qua chòm sao) chỉ
được dùng khi có mục trong SOURCED kèm URL. Không có nguồn thì chủ đề đó bị
chặn, không được điền bằng trí nhớ.
"""
from __future__ import annotations

from dataclasses import dataclass

# ─── Ngũ hành ─────────────────────────────────────────────────────────────
HANH = ("Mộc", "Hỏa", "Thổ", "Kim", "Thủy")          # thứ tự tương sinh
SINH = {h: HANH[(i + 1) % 5] for i, h in enumerate(HANH)}   # Mộc sinh Hỏa ...
KHAC = {h: HANH[(i + 2) % 5] for i, h in enumerate(HANH)}   # Mộc khắc Thổ ...

# ─── 12 địa chi ───────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Chi:
    i: int
    name: str
    animal: str
    hanh: str
    duong: bool
    huong: str

    @property
    def gio(self) -> tuple[int, int]:
        """Khung giờ: Tý 23–1, Sửu 1–3, ... mỗi chi 2 tiếng."""
        s = (23 + 2 * self.i) % 24
        return s, (s + 2) % 24


CHI = tuple(Chi(i, *row) for i, row in enumerate((
    ("Tý", "Chuột", "Thủy", True, "chính Bắc"),
    ("Sửu", "Trâu", "Thổ", False, "Đông Bắc"),
    ("Dần", "Hổ", "Mộc", True, "Đông Bắc"),
    ("Mão", "Mèo", "Mộc", False, "chính Đông"),
    ("Thìn", "Rồng", "Thổ", True, "Đông Nam"),
    ("Tỵ", "Rắn", "Hỏa", False, "Đông Nam"),
    ("Ngọ", "Ngựa", "Hỏa", True, "chính Nam"),
    ("Mùi", "Dê", "Thổ", False, "Tây Nam"),
    ("Thân", "Khỉ", "Kim", True, "Tây Nam"),
    ("Dậu", "Gà", "Kim", False, "chính Tây"),
    ("Tuất", "Chó", "Thổ", True, "Tây Bắc"),
    ("Hợi", "Lợn", "Thủy", False, "Tây Bắc"),
)))
CHI_BY = {c.name: c for c in CHI}


def luc_xung(a: str, b: str) -> bool:
    """Đối diện trên vòng 12: cách nhau 6."""
    return abs(CHI_BY[a].i - CHI_BY[b].i) == 6


# Lục hợp: tổng chỉ số ≡ 1 (mod 12) -- Tý(0)+Sửu(1), Dần(2)+Hợi(11)...
def luc_hop(a: str, b: str) -> bool:
    return a != b and (CHI_BY[a].i + CHI_BY[b].i) % 12 == 1


def tam_hop(*names: str) -> bool:
    """Ba chi cách đều nhau 4 vị trí."""
    ix = sorted(CHI_BY[n].i for n in names)
    return len(set(ix)) == 3 and ix[1] - ix[0] == 4 and ix[2] - ix[1] == 4


def luc_hai(a: str, b: str) -> bool:
    """Hại = chi xung với BẠN HỢP của mình. Tổng chỉ số ≡ 7 (mod 12)."""
    return a != b and (CHI_BY[a].i + CHI_BY[b].i) % 12 == 7


def hop_partner(a: str) -> str:
    return next(c.name for c in CHI if luc_hop(a, c.name))


def xung_partner(a: str) -> str:
    return CHI[(CHI_BY[a].i + 6) % 12].name


# ─── 10 thiên can + thập thần ─────────────────────────────────────────────
CAN = (("Giáp", "Mộc", True), ("Ất", "Mộc", False), ("Bính", "Hỏa", True),
       ("Đinh", "Hỏa", False), ("Mậu", "Thổ", True), ("Kỷ", "Thổ", False),
       ("Canh", "Kim", True), ("Tân", "Kim", False), ("Nhâm", "Thủy", True),
       ("Quý", "Thủy", False))
CAN_BY = {n: (h, d) for n, h, d in CAN}

# (quan hệ hành, cùng âm dương?) -> tên thần
_THAN = {
    ("dong", True): "Tỷ Kiên", ("dong", False): "Kiếp Tài",
    ("toi_sinh", True): "Thực Thần", ("toi_sinh", False): "Thương Quan",
    ("toi_khac", True): "Thiên Tài", ("toi_khac", False): "Chính Tài",
    ("khac_toi", True): "Thất Sát", ("khac_toi", False): "Chính Quan",
    ("sinh_toi", True): "Thiên Ấn", ("sinh_toi", False): "Chính Ấn",
}
THAP_THAN = tuple(_THAN.values())


def quan_he(nhat_hanh: str, hanh: str) -> str:
    if hanh == nhat_hanh:
        return "dong"
    if SINH[nhat_hanh] == hanh:
        return "toi_sinh"
    if KHAC[nhat_hanh] == hanh:
        return "toi_khac"
    if KHAC[hanh] == nhat_hanh:
        return "khac_toi"
    return "sinh_toi"


def thap_than(nhat_chu: str, can: str) -> str:
    """Thần của `can` đối với Nhật chủ `nhat_chu`. Tính, không tra."""
    nh, nd = CAN_BY[nhat_chu]
    h, d = CAN_BY[can]
    return _THAN[(quan_he(nh, h), nd == d)]


# ─── Bát quái + 64 quẻ ────────────────────────────────────────────────────
# Hào đọc TỪ DƯỚI LÊN, 1 = dương (liền), 0 = âm (đứt).
QUAI = {"Càn": ("Trời", (1, 1, 1)), "Đoài": ("Đầm", (1, 1, 0)),
        "Ly": ("Lửa", (1, 0, 1)), "Chấn": ("Sấm", (1, 0, 0)),
        "Tốn": ("Gió", (0, 1, 1)), "Khảm": ("Nước", (0, 1, 0)),
        "Cấn": ("Núi", (0, 0, 1)), "Khôn": ("Đất", (0, 0, 0))}

# Thứ tự Văn Vương: (tên, quái trên, quái dưới).
_KW = """Càn Càn Càn|Khôn Khôn Khôn|Truân Khảm Chấn|Mông Cấn Khảm|Nhu Khảm Càn|
Tụng Càn Khảm|Sư Khôn Khảm|Tỷ Khảm Khôn|Tiểu_Súc Tốn Càn|Lý Càn Đoài|Thái Khôn Càn|
Bĩ Càn Khôn|Đồng_Nhân Càn Ly|Đại_Hữu Ly Càn|Khiêm Khôn Cấn|Dự Chấn Khôn|Tùy Đoài Chấn|
Cổ Cấn Tốn|Lâm Khôn Đoài|Quan Tốn Khôn|Phệ_Hạp Ly Chấn|Bí Cấn Ly|Bác Cấn Khôn|
Phục Khôn Chấn|Vô_Vọng Càn Chấn|Đại_Súc Cấn Càn|Di Cấn Chấn|Đại_Quá Đoài Tốn|
Khảm Khảm Khảm|Ly Ly Ly|Hàm Đoài Cấn|Hằng Chấn Tốn|Độn Càn Cấn|Đại_Tráng Chấn Càn|
Tấn Ly Khôn|Minh_Di Khôn Ly|Gia_Nhân Tốn Ly|Khuê Ly Đoài|Kiển Khảm Cấn|Giải Chấn Khảm|
Tổn Cấn Đoài|Ích Tốn Chấn|Quải Đoài Càn|Cấu Càn Tốn|Tụy Đoài Khôn|Thăng Khôn Tốn|
Khốn Đoài Khảm|Tỉnh Khảm Tốn|Cách Đoài Ly|Đỉnh Ly Tốn|Chấn Chấn Chấn|Cấn Cấn Cấn|
Tiệm Tốn Cấn|Quy_Muội Chấn Đoài|Phong Chấn Ly|Lữ Ly Cấn|Tốn Tốn Tốn|Đoài Đoài Đoài|
Hoán Tốn Khảm|Tiết Khảm Đoài|Trung_Phu Tốn Đoài|Tiểu_Quá Chấn Cấn|Ký_Tế Khảm Ly|Vị_Tế Ly Khảm"""


@dataclass(frozen=True)
class Que:
    so: int
    name: str
    tren: str
    duoi: str

    @property
    def hao(self) -> tuple[int, ...]:
        return QUAI[self.duoi][1] + QUAI[self.tren][1]


QUE = tuple(Que(i + 1, n.replace("_", " "), t, d) for i, (n, t, d) in
            enumerate(x.strip().split() for x in _KW.replace("\n", "").split("|")))
QUE_BY = {q.name: q for q in QUE}
_BY_HAO = {q.hao: q for q in QUE}


def lat_nguoc(q: Que) -> Que:      # 綜 -- xoay quẻ 180°
    return _BY_HAO[tuple(reversed(q.hao))]


def doi_am_duong(q: Que) -> Que:   # 錯 -- đổi mọi hào
    return _BY_HAO[tuple(1 - h for h in q.hao)]


# ─── 12 cung hoàng đạo phương Tây ─────────────────────────────────────────
# Cung (tropical): theo điểm xuân phân. Chòm (IAU): ngày Mặt Trời thật sự
# đứng trước chòm sao, theo NASA SpacePlace. Ngày lệch ±1 tuỳ năm.
CUNG = (  # tên, (tháng, ngày) bắt đầu
    ("Bạch Dương", (3, 21)), ("Kim Ngưu", (4, 20)), ("Song Tử", (5, 21)),
    ("Cự Giải", (6, 21)), ("Sư Tử", (7, 23)), ("Xử Nữ", (8, 23)),
    ("Thiên Bình", (9, 23)), ("Bọ Cạp", (10, 23)), ("Nhân Mã", (11, 22)),
    ("Ma Kết", (12, 22)), ("Bảo Bình", (1, 20)), ("Song Ngư", (2, 19)))
CHOM = (  # tên chòm, (tháng, ngày) Mặt Trời bắt đầu đứng trước
    ("Ma Kết", (1, 20)), ("Bảo Bình", (2, 16)), ("Song Ngư", (3, 11)),
    ("Bạch Dương", (4, 18)), ("Kim Ngưu", (5, 13)), ("Song Tử", (6, 21)),
    ("Cự Giải", (7, 20)), ("Sư Tử", (8, 10)), ("Xử Nữ", (9, 16)),
    ("Thiên Bình", (10, 30)), ("Bọ Cạp", (11, 23)), ("Xà Phu", (11, 29)),
    ("Nhân Mã", (12, 17)))


def _lookup(table, m: int, d: int) -> str:
    best = max(table, key=lambda r: r[1])[0]       # trước mốc sớm nhất = mốc muộn nhất năm trước
    for name, start in sorted(table, key=lambda r: r[1]):
        if (m, d) >= start:
            best = name
    return best


def cung_of(m: int, d: int) -> str:
    return _lookup(CUNG, m, d)


def chom_of(m: int, d: int) -> str:
    return _lookup(CHOM, m, d)


def chom_days(name: str) -> int:
    """Số ngày Mặt Trời đứng trước chòm (năm không nhuận)."""
    from datetime import date
    rows = sorted(CHOM, key=lambda r: r[1])
    i = next(k for k, r in enumerate(rows) if r[0] == name)
    a = date(2026, *rows[i][1])
    b = date(2026 + (i + 1 == len(rows)), *rows[(i + 1) % len(rows)][1])
    return (b - a).days


# ─── Văn bản CÓ NGUỒN ─────────────────────────────────────────────────────
# Chỉ mục có ở đây mới được trích. Mỗi mục đã đối chiếu tận nơi.

@dataclass(frozen=True)
class Sourced:
    key: str
    text: str        # nguyên văn
    vi: str          # nghĩa tiếng Việt dùng trong lời đọc
    url: str


SOURCED = {s.key: s for s in (
    Sourced("thai.thoan", "天地交而萬物通也", "trời đất giao nhau thì vạn vật thông",
            "https://zh.wikisource.org/wiki/周易/泰 (Thoán truyện quẻ Thái)"),
    Sourced("bi.thoan", "天地不交而萬物不通也", "trời đất không giao thì vạn vật không thông",
            "https://zh.wikisource.org/wiki/周易/否 (Thoán truyện quẻ Bĩ)"),
    Sourced("thai.quai_tu", "泰：小往大來，吉亨。", "cái nhỏ đi, cái lớn đến, tốt lành hanh thông",
            "https://zh.wikisource.org/wiki/周易/泰"),
    Sourced("bi.quai_tu", "否之匪人，不利君子貞，大往小來。", "cái lớn đi, cái nhỏ đến",
            "https://zh.wikisource.org/wiki/周易/否"),
    Sourced("nasa.virgo45", "The line from Earth through the sun points to Virgo for 45 days",
            "Mặt Trời đứng trước chòm Xử Nữ khoảng 45 ngày",
            "https://nasa.tumblr.com/post/150688852794/zodiac (NASA, Constellations and the Calendar)"),
    Sourced("nasa.axis", "Earth's axis (North Pole) doesn't point in quite the same direction",
            "trục Trái Đất không còn chỉ đúng hướng như ba nghìn năm trước",
            "https://nasa.tumblr.com/post/150688852794/zodiac"),
    Sourced("nasa.babylon", "The Babylonians lived over 3,000 years ago. They divided the zodiac into 12 equal parts",
            "người Babylon, hơn ba nghìn năm trước, chia vòng hoàng đạo thành 12 phần bằng nhau",
            "https://nasa.tumblr.com/post/150688852794/zodiac"),
)}

# Chủ đề CHƯA có nguồn -- bị chặn, không được điền bằng trí nhớ.
CAN_XAC_MINH = {
    "cân xương đoán số": "Cần bảng trọng lượng năm/tháng/ngày/giờ của Viên Thiên "
                         "Cang và bài thơ cho từng mức — chưa có bản đối chiếu.",
    "lời quẻ 60 quẻ còn lại": "Mới đối chiếu Thái, Bĩ. Quẻ khác cần lấy nguyên văn "
                              "Wikisource trước khi viết.",
}


# ═══ MỞ RỘNG (21/09/2026) — dữ liệu cho vòng chủ đề dài hạn ═══════════════

# Tháng âm của từng chi: tháng Giêng là tháng Dần, không phải tháng Tý.
THANG_AM = {c.name: (c.i - 2) % 12 + 1 for c in CHI}


def tu_hanh_xung(*names: str) -> bool:
    """Bốn chi cách đều nhau 3 vị trí = hai cặp xung đan chéo."""
    ix = sorted(CHI_BY[n].i for n in names)
    return len(set(ix)) == 4 and all(ix[k + 1] - ix[k] == 3 for k in range(3))


TAM_HOP = tuple(tuple(CHI[(s + 4 * k) % 12].name for k in range(3)) for s in (8, 11, 2, 5))
# Cục mang hành của chi GIỮA (chi vượng): Thân Tý Thìn -> Tý -> Thủy.
TAM_HOP_CUC = {g: CHI_BY[g[1]].hanh for g in TAM_HOP}
TU_HANH_XUNG = tuple(tuple(CHI[s + 3 * k].name for k in range(4)) for s in (2, 0, 1))

# Tàng can: can ẩn trong chi (bản khí trước).
TANG_CAN = {"Tý": ("Quý",), "Sửu": ("Kỷ", "Quý", "Tân"), "Dần": ("Giáp", "Bính", "Mậu"),
            "Mão": ("Ất",), "Thìn": ("Mậu", "Ất", "Quý"), "Tỵ": ("Bính", "Canh", "Mậu"),
            "Ngọ": ("Đinh", "Kỷ"), "Mùi": ("Kỷ", "Đinh", "Ất"), "Thân": ("Canh", "Nhâm", "Mậu"),
            "Dậu": ("Tân",), "Tuất": ("Mậu", "Tân", "Đinh"), "Hợi": ("Nhâm", "Giáp")}
CAN_NAMES = tuple(n for n, _, _ in CAN)


def can_hop(a: str, b: str) -> bool:
    return abs(CAN_NAMES.index(a) - CAN_NAMES.index(b)) == 5


# Hợp hoá: Giáp Kỷ -> Thổ, Ất Canh -> Kim, Bính Tân -> Thủy, Đinh Nhâm -> Mộc, Mậu Quý -> Hỏa
CAN_HOP_HOA = {CAN_NAMES[i]: ("Thổ", "Kim", "Thủy", "Mộc", "Hỏa")[i] for i in range(5)}


def can_xung(a: str, b: str) -> bool:
    """Cách 6, cùng âm dương, khắc nhau. Mậu Kỷ ở giữa, không có cặp xung."""
    ia, ib = CAN_NAMES.index(a), CAN_NAMES.index(b)
    return abs(ia - ib) == 6 and "Mậu" not in (a, b) and "Kỷ" not in (a, b)


# Nạp âm 60 hoa giáp -- KHÔNG lấy từ vnlunar (đã đo: sai, ví dụ Bính Tý ghi
# Lộ Bàng Thổ thay vì Giản Hạ Thủy). Nguồn: zh-yue.wikipedia 納音.
NAP_AM = ("Hải Trung Kim", "Lư Trung Hỏa", "Đại Lâm Mộc", "Lộ Bàng Thổ", "Kiếm Phong Kim",
          "Sơn Đầu Hỏa", "Giản Hạ Thủy", "Thành Đầu Thổ", "Bạch Lạp Kim", "Dương Liễu Mộc",
          "Tuyền Trung Thủy", "Ốc Thượng Thổ", "Tích Lịch Hỏa", "Tùng Bách Mộc", "Trường Lưu Thủy",
          "Sa Trung Kim", "Sơn Hạ Hỏa", "Bình Địa Mộc", "Bích Thượng Thổ", "Kim Bạch Kim",
          "Phú Đăng Hỏa", "Thiên Hà Thủy", "Đại Trạch Thổ", "Thoa Xuyến Kim", "Tang Đố Mộc",
          "Đại Khê Thủy", "Sa Trung Thổ", "Thiên Thượng Hỏa", "Thạch Lựu Mộc", "Đại Hải Thủy")
NAP_AM_HANH = {n: n.split()[-1] for n in NAP_AM}


def can_chi_60(k: int) -> str:
    return f"{CAN_NAMES[k % 10]} {CHI[k % 12].name}"


def year_index(y: int) -> int:
    return (y - 4) % 60          # 1984 = Giáp Tý = 0


def nap_am_of(k: int) -> str:
    return NAP_AM[(k % 60) // 2]


# 28 tú -- KHÔNG lấy con vật từ vnlunar (đã đo: sai 5 tú, vd Đẩu ghi "Hề",
# Tỉnh ghi "Dẫn"). Nguồn: zh.wikipedia 二十八宿 (角木蛟 ... 軫水蚓).
TU28 = tuple(zip(
    "Giác Cang Đê Phòng Tâm Vĩ Cơ Đẩu Ngưu Nữ Hư Nguy Thất Bích Khuê Lâu Vị Mão Tất Chủy Sâm "
    "Tỉnh Quỷ Liễu Tinh Trương Dực Chẩn".split(),
    ("Mộc", "Kim", "Thổ", "Nhật", "Nguyệt", "Hỏa", "Thủy") * 4,
    ("Giao long", "Rồng", "Lạc", "Thỏ", "Cáo", "Hổ", "Báo", "Giải trãi", "Trâu", "Dơi", "Chuột",
     "Én", "Lợn", "Du", "Sói", "Chó", "Trĩ", "Gà", "Quạ", "Khỉ", "Vượn", "Hãn", "Dê", "Hoẵng",
     "Ngựa", "Hươu", "Rắn", "Giun"),
))
TU_PHUONG = ("phương Đông", "phương Bắc", "phương Tây", "phương Nam")
TU_TUONG = ("Thanh Long", "Huyền Vũ", "Bạch Hổ", "Chu Tước")
TU_BY = {n: (i, h, a) for i, (n, h, a) in enumerate(TU28)}

# Chiêm tinh phương Tây: nguyên tố, tính chất, sao chủ quản cổ điển.
CUNG_NAMES = tuple(n for n, _ in CUNG)
NGUYEN_TO = {n: ("Lửa", "Đất", "Khí", "Nước")[i % 4] for i, n in enumerate(CUNG_NAMES)}
TINH_CHAT = {n: ("Tiên phong", "Kiên định", "Linh hoạt")[i % 3] for i, n in enumerate(CUNG_NAMES)}
CHU_QUAN = dict(zip(CUNG_NAMES, ("sao Hỏa", "sao Kim", "sao Thủy", "Mặt Trăng", "Mặt Trời",
                                 "sao Thủy", "sao Kim", "sao Hỏa", "sao Mộc", "sao Thổ",
                                 "sao Thổ", "sao Mộc")))
# Tiên phong = bốn cung mở đầu ở xuân phân, hạ chí, thu phân, đông chí.
TIET_KHI_MO_DAU = {"Bạch Dương": "xuân phân", "Cự Giải": "hạ chí",
                   "Thiên Bình": "thu phân", "Ma Kết": "đông chí"}

SOURCED.update({s.key: s for s in (
    Sourced("tu28", "角木蛟 亢金龍 氐土貉 ... 翼火蛇 軫水蚓", "28 tú, con vật và thất diệu",
            "https://zh.wikipedia.org/wiki/二十八宿"),
    Sourced("napam", "甲子乙丑海中金 ... 壬戌癸亥大海水", "bảng nạp âm 60 hoa giáp",
            "https://zh-yue.wikipedia.org/wiki/納音"),
    Sourced("ntt", "Kinh Dịch — Ngô Tất Tố dịch", "bản dịch Kinh Dịch của Ngô Tất Tố",
            "https://vi.wikisource.org/wiki/Kinh_Dịch"),
)})

# vnlunar viết 參 là "Thâm"; tên phổ thông là Sâm.
TU_ALIAS = {"Thâm": "Sâm"}
SOURCED["hetu.duongquai"] = Sourced(
    "hetu.duongquai", "陽卦多陰，陰卦多陽，其故何也？陽卦奇，陰卦偶。",
    "quái dương nhiều hào âm, quái âm nhiều hào dương; quái dương lẻ, quái âm chẵn",
    "https://zh.wikisource.org/wiki/周易/繫辭下 (Hệ từ hạ)")


def ho_quai(q: Que) -> Que:
    """Hỗ quái: hào 2-3-4 làm quái dưới, 3-4-5 làm quái trên."""
    h = q.hao
    return _BY_HAO[h[1:4] + h[2:5]]


def bien_quai(q: Que, pos: int) -> Que:
    h = list(q.hao)
    h[pos - 1] = 1 - h[pos - 1]
    return _BY_HAO[tuple(h)]


def can_chi_60_index(cc: str) -> int:
    return next(i for i in range(60) if can_chi_60(i) == cc)
