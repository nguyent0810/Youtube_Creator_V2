"""Sự thật lịch — dữ liệu tính toán được, KHÔNG BAO GIỜ do model nghĩ ra.

Đây là ranh giới quan trọng nhất của kênh Phong Thủy: ngày âm, Can Chi,
Hoàng Đạo/Hắc Đạo, giờ tốt, hướng tốt đều là dữ kiện KHÁCH QUAN. Sai là sai
thật, và người xem làm theo thì ảnh hưởng thật.

ĐĂNG TRƯỚC MỘT NGÀY: nội dung của ngày D lên lúc 6h sáng ngày D-1. Biết giờ
tốt/hướng tốt vào đúng buổi sáng hôm đó thì đã muộn để sắp xếp công việc.
Kéo theo một ràng buộc BẮT BUỘC về câu chữ: kịch bản phải xưng "ngày mai",
không phải "hôm nay" -- lùi lịch mà giữ câu chữ cũ thì người xem làm theo
giờ tốt vào SAI NGÀY.

═══ HAI NGUỒN ĐỘC LẬP PHẢI KHỚP NHAU ═══

LỖI THẬT (phát hiện 08/10/2026): vnlunar 1.0.3/1.0.4 tính Trực bằng
(ngày âm + tháng âm + 2) % 12 và 12 thần bằng (chi ngày + 8) % 12, bỏ qua
tháng. Cả 92 video Lịch 10–12/2026 vì vậy nói SAI TRỰC (0/92 đúng) và
38/92 ngày đảo hoàng đạo ↔ hắc đạo. Không bộ kiểm nào bắt được, vì bộ kiểm
đối chiếu kịch bản với... chính vnlunar. Một nguồn duy nhất thì không thể
tự phát hiện mình sai.

Nên giờ mọi dữ kiện cốt lõi được TÍNH LẠI ĐỘC LẬP ngay trong file này, theo
quy tắc truyền thống viết thành mã, rồi so với vnlunar. Lệch ở bất kỳ trường
nào là ném LunarMismatch -- pipeline dừng, không sinh kịch bản:

  can chi ngày   số ngày Julius (JDN): (JDN + 49) mod 60, 0 = Giáp Tý
  tháng (Trực)   theo TIẾT KHÍ: kinh độ Mặt Trời (Meeus), Lập Xuân = Dần;
                 ngày giao tiết thuộc tháng mới (nên Trực lặp lại đúng ngày đó)
  Trực           (chi ngày − chi tháng tiết khí) mod 12, 0 = Kiến
  12 thần        Thanh Long khởi theo chi tháng: Dần Thân → Tý, Mão Dậu → Dần,
                 Thìn Tuất → Thìn, Tỵ Hợi → Ngọ, Tý Ngọ → Thân, Sửu Mùi → Tuất.
                 Tháng tính theo THÁNG ÂM (tục lệ lịch Việt, cũng là mặc định
                 god_basis="lunar" của vnlunar 1.0.5); tháng nhuận dùng chi của
                 tháng thường cùng số.
  giờ hoàng đạo  cùng quy tắc khởi Thanh Long, áp cho 12 giờ theo chi NGÀY
  28 tú          chu kỳ 28 ngày gắn với tuần: (JDN + 11) mod 28, 0 = Giác
                 (khớp luật thất diệu: Giác/Đẩu/Khuê/Tỉnh luôn rơi vào thứ Năm)
  tuổi xung      chi ngày + 6

Những thứ KHÔNG tự tính được (ngày âm, danh mục việc) thì: ngày âm vẫn lấy
từ vnlunar (thuật toán đổi lịch âm của thư viện không đổi giữa các bản);
danh mục việc lấy từ bảng ĐÃ GHIM trong factory/vocab.py, không lấy từ thư
viện -- vnlunar 1.0.5 thay toàn bộ danh mục của cả 12 trực, và chuyện đổi
nguồn nội dung phải là quyết định có chủ đích, không phải tác dụng phụ của
một lần `pip install -U`.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

# 6h sáng ICT = 23:00 UTC ngày hôm trước.
# Sáu sao hoàng đạo trong hệ 12 sao. Còn lại là hắc đạo.
AUSPICIOUS_GODS = frozenset({"Thanh Long", "Minh Đường", "Kim Quỹ",
                             "Ngọc Đường", "Thiên Đức", "Tư Mệnh"})

PUBLISH_UTC_HOUR, PUBLISH_UTC_MINUTE = 23, 0
LEAD_DAYS = 1

CAN = ("Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý")
CHI = ("Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi")
CHI_ANIMALS = ("Chuột", "Trâu", "Hổ", "Mèo", "Rồng", "Rắn", "Ngựa", "Dê", "Khỉ", "Gà", "Chó", "Lợn")
HOUR_RANGES = ("23-1h", "1-3h", "3-5h", "5-7h", "7-9h", "9-11h",
               "11-13h", "13-15h", "15-17h", "17-19h", "19-21h", "21-23h")

# Tên chuẩn dùng trong kịch bản (khớp factory/vocab.py). So khớp không phân
# biệt hoa/thường: vnlunar 1.0.4 viết "Trực kiến", 1.0.5 viết "Trực Kiến".
TRUC_ORDER = ("Trực kiến", "Trực trừ", "Trực mãn", "Trực bình", "Trực định", "Trực chấp",
              "Trực phá", "Trực nguy", "Trực thành", "Trực thu", "Trực khai", "Trực bế")
GOD_ORDER = ("Thanh Long", "Minh Đường", "Thiên Hình", "Chu Tước", "Kim Quỹ", "Thiên Đức",
             "Bạch Hổ", "Ngọc Đường", "Thiên Lao", "Huyền Vũ", "Tư Mệnh", "Câu Trần")
GOD_ALIAS = {"Câu Trận": "Câu Trần", "Bảo Quang": "Thiên Đức", "Kim Đường": "Thiên Đức"}

# Hỷ thần theo can ngày: Giáp Kỷ → Đông Bắc, Ất Canh → Tây Bắc, Bính Tân →
# Tây Nam, Đinh Nhâm → Nam, Mậu Quý → Đông Nam (quy tắc cổ, khớp vnlunar 1.0.5).
JOY_GOD_DIR = ("Đông Bắc", "Tây Bắc", "Tây Nam", "Nam", "Đông Nam",
               "Đông Bắc", "Tây Bắc", "Tây Nam", "Nam", "Đông Nam")
# Tài thần theo can ngày: Giáp Ất → Đông Nam, Bính Đinh → Đông, Mậu → Bắc,
# Kỷ → Nam, Canh Tân → Tây Nam, Nhâm → Tây, Quý → Tây Bắc (bản Thông Thư phổ
# biến, khớp vnlunar 1.0.5). vnlunar 1.0.4 dùng một bảng khác hẳn -- sai ở
# mọi ngày -- nên câu "Hướng Tài thần" trong các video cũ cũng sai.
WEALTH_GOD_DIR = ("Đông Nam", "Đông Nam", "Đông", "Đông", "Bắc",
                  "Nam", "Tây Nam", "Tây Nam", "Tây", "Tây Bắc")

# Kinh độ Mặt Trời cách mốc giao tiết dưới ngưỡng này (độ, ~1 giờ) lúc nửa
# đêm thì công thức Meeus rút gọn không đủ chính xác để chắc ngày giao tiết.
# Khi đó chấp nhận tháng của vnlunar cho riêng Trực, mọi trường khác vẫn kiểm.
_TERM_EPSILON_DEG = 0.05


class LunarMismatch(RuntimeError):
    """vnlunar và phép tính độc lập ra hai kết quả khác nhau.

    Cố ý là lỗi CỨNG: một trong hai đang sai, và không có cách nào biết bên
    nào mà không có người xem xét. Sinh kịch bản tiếp là đưa dữ kiện chưa
    kiểm lên kênh -- đúng thứ đã xảy ra với 92 video Lịch."""


@dataclass(frozen=True)
class DayFacts:
    """Sự thật lịch của MỘT ngày. Mọi trường cốt lõi đã qua đối chiếu kép."""
    target: date
    lunar_day: int
    lunar_month: int
    can_chi_day: str
    day_type: str          # "Hoàng Đạo" | "Hắc Đạo" -- suy từ god_name
    god_name: str          # sao của ngày, vd "Kim Quỹ", "Thiên Đức"
    truc_name: str         # tên chuẩn, vd "Trực thành"
    truc_good_for: tuple   # bảng ghim trong factory/vocab.py
    truc_bad_for: tuple
    star_name: str         # 12 trực tinh, vd "Định"
    star_desc: str
    mansion_name: str      # nhị thập bát tú, vd "Khuê"
    mansion_good: bool
    # ─── Các tầng bổ sung ────────────────────────────────────────────────
    # Sao và trực đều là chu kỳ 12, nên cứ 12 ngày lại lặp đúng một cặp.
    # Những tầng dưới đây có chu kỳ KHÁC nên phá được sự lặp, và phần lớn
    # còn hành động được hơn: giờ tốt và tuổi xung là thứ người xem soi
    # vào bản thân ngay được.
    mansion_animal: str    # con vật của tú, vd "Nai", "Sói"
    mansion_element: str   # thất diệu của tú
    day_of_week: str       # "Thứ bảy"
    nayin_name: str        # nạp âm, vd "Tòng Bách Mộc" -- chu kỳ 60
    auspicious_hours: str  # "Sửu (1-3h), Thìn (7-9h)..."
    good_directions: str   # hướng xuất hành -- vnlunar ghi là CHƯA có nguồn, đừng dùng
    conflict_animal: str   # tuổi xung, vd "Lợn"
    conflict_chi: str      # chi xung, vd "Hợi"
    day_animal: str        # con giáp của ngày, vd "Rắn"
    wealth_god_dir: str    # hướng Tài thần
    joy_god_dir: str       # hướng Hỷ thần
    lunar_leap: bool = False   # ngày thuộc tháng âm nhuận

    @property
    def publish_at(self) -> str:
        """ISO UTC. 6h ICT ngày (target - LEAD_DAYS) = 23:00 UTC ngày trước đó."""
        day = self.target - timedelta(days=1 + LEAD_DAYS)
        return datetime(day.year, day.month, day.day, PUBLISH_UTC_HOUR,
                        PUBLISH_UTC_MINUTE, tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @property
    def is_auspicious_star(self) -> bool:
        """Dựa trên SAO (đã đối chiếu kép), không dựa trên nhãn của thư viện."""
        return self.god_name in AUSPICIOUS_GODS

    @property
    def slug(self) -> str:
        return f"lich-{self.target.strftime('%Y%m%d')}"


# ─── Tính độc lập: không import vnlunar ─────────────────────────────────────

def jdn(d: date) -> int:
    """Số ngày Julius của ngày dương lịch."""
    return d.toordinal() + 1721425


def day_can_chi(d: date) -> tuple[int, int]:
    """(chỉ số can, chỉ số chi) của ngày. 0 = Giáp / Tý."""
    i = (jdn(d) + 49) % 60
    return i % 10, i % 12


def sixty_index(d: date) -> int:
    """Chỉ số hoa giáp 0..59 của ngày (0 = Giáp Tý)."""
    return (jdn(d) + 49) % 60


def sun_longitude(jd: float) -> float:
    """Kinh độ biểu kiến của Mặt Trời, độ (Meeus rút gọn, sai số ~0,01°)."""
    t = (jd - 2451545.0) / 36525
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    m = math.radians(357.52911 + 35999.05029 * t - 0.0001537 * t * t)
    c = ((1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(m)
         + (0.019993 - 0.000101 * t) * math.sin(2 * m) + 0.000289 * math.sin(3 * m))
    omega = math.radians(125.04 - 1934.136 * t)
    return (l0 + c - 0.00569 - 0.00478 * math.sin(omega)) % 360


def _jd_end_of_vn_day(d: date) -> float:
    end = datetime(d.year, d.month, d.day, tzinfo=timezone.utc) + timedelta(hours=24 - 7)
    return 2440587.5 + end.timestamp() / 86400


def solar_month_chi(d: date) -> tuple[int, bool]:
    """(chi tháng theo tiết khí, có_chắc_chắn). Lập Xuân mở tháng Dần.

    Lấy kinh độ lúc HẾT ngày (24:00 giờ VN): tiết giao lúc nào trong ngày thì
    cả ngày đó thuộc tháng mới -- đó là lý do Trực lặp lại đúng ngày giao tiết."""
    lam = sun_longitude(_jd_end_of_vn_day(d))
    rel = (lam - 315) % 360
    k = math.floor(rel / 30)
    edge = min(rel - 30 * k, 30 * (k + 1) - rel)
    return (k + 2) % 12, edge >= _TERM_EPSILON_DEG


def truc_index(d: date) -> tuple[int, bool]:
    """(chỉ số Trực 0 = Kiến, có_chắc_chắn)."""
    _, chi = day_can_chi(d)
    m, sure = solar_month_chi(d)
    return (chi - m) % 12, sure


def thanh_long_start(chi: int) -> int:
    """Chi nơi Thanh Long khởi, cho tháng (khi xét ngày) hoặc ngày (khi xét giờ)."""
    return ((chi - 2) % 6) * 2


def god_index(day_chi: int, month_chi: int) -> int:
    return (day_chi - thanh_long_start(month_chi)) % 12


def auspicious_hours_of(day_chi: int) -> str:
    """Sáu giờ hoàng đạo của ngày, cùng định dạng vnlunar trả về."""
    start = thanh_long_start(day_chi)
    hours = [h for h in range(12) if GOD_ORDER[(h - start) % 12] in AUSPICIOUS_GODS]
    return ", ".join(f"{CHI[h]} ({HOUR_RANGES[h]})" for h in hours)


def mansion_index(d: date) -> int:
    """Chỉ số 28 tú, 0 = Giác. Chu kỳ 28 ngày, gắn cố định với thứ trong tuần."""
    return (jdn(d) + 11) % 28


# ─── Đối chiếu với vnlunar ─────────────────────────────────────────────────

def _canon(name: str, order: tuple[str, ...], alias: dict[str, str] | None = None) -> str | None:
    name = (alias or {}).get(name.strip(), name.strip())
    return next((x for x in order if x.casefold() == name.casefold()), None)


def _tu_animal(name: str, fallback: str) -> str:
    from factory.pillars.tables import TU_ALIAS, TU_BY
    name = TU_ALIAS.get(name, name)
    return TU_BY[name][2] if name in TU_BY else fallback


def facts_for(target: date) -> DayFacts:
    import vnlunar
    from factory.pillars.tables import TU28, TU_ALIAS, TU_GOOD, nap_am_of
    from factory.vocab import TRUC_VIEC

    info = vnlunar.get_full_info(target.day, target.month, target.year)
    lunar = info["lunar"]
    lib_ver = getattr(vnlunar, "__version__", "?")

    can_i, chi_i = day_can_chi(target)
    ti, truc_sure = truc_index(target)
    gi = god_index(chi_i, (lunar["month"] + 1) % 12)
    mi = mansion_index(target)
    xung = (chi_i + 6) % 12

    ours = {
        "can chi ngày": f"{CAN[can_i]} {CHI[chi_i]}",
        "trực": TRUC_ORDER[ti],
        "sao (12 thần)": GOD_ORDER[gi],
        "giờ hoàng đạo": auspicious_hours_of(chi_i),
        "tú": TU28[mi][0],
        "tú tốt/xấu": TU_GOOD[mi],
        "chi xung": CHI[xung],
        "tuổi xung": CHI_ANIMALS[xung],
        "con giáp ngày": CHI_ANIMALS[chi_i],
        "hướng Tài thần": WEALTH_GOD_DIR[can_i],
        "hướng Hỷ thần": JOY_GOD_DIR[can_i],
    }
    mansion = info.get("28_mansions") or {}
    ages = info.get("conflicting_ages") or {}
    gods_dir = info.get("god_directions") or {}
    raw_truc = (info.get("12_constructions") or {}).get("name", "")
    raw_god = (info.get("12_gods") or {}).get("name", "")
    theirs = {
        "can chi ngày": (info.get("can_chi") or {}).get("day", ""),
        "trực": _canon(raw_truc, TRUC_ORDER) or raw_truc,
        "sao (12 thần)": _canon(raw_god, GOD_ORDER, GOD_ALIAS) or raw_god,
        "giờ hoàng đạo": info.get("auspicious_hours", ""),
        "tú": TU_ALIAS.get(mansion.get("name", ""), mansion.get("name", "")),
        "tú tốt/xấu": bool(mansion.get("good")),
        "chi xung": ages.get("conflict_chi", ""),
        "tuổi xung": ages.get("conflict_animal", ""),
        "con giáp ngày": ages.get("day_animal", ""),
        "hướng Tài thần": gods_dir.get("wealth_god", ""),
        "hướng Hỷ thần": gods_dir.get("joy_god", ""),
    }
    if not truc_sure:
        # Giao tiết sát nửa đêm: phép tính rút gọn không đủ chắc để phân xử ngày.
        # Chỉ chấp nhận khi vnlunar ra một trong hai trực khả dĩ (trước/sau tiết).
        alt = {TRUC_ORDER[ti], TRUC_ORDER[(ti + 1) % 12], TRUC_ORDER[(ti - 1) % 12]}
        if theirs["trực"] in alt:
            ours["trực"] = theirs["trực"]

    bad = [f"{k}: vnlunar {lib_ver} ghi {theirs[k]!r}, tính độc lập ra {ours[k]!r}"
           for k in ours if ours[k] != theirs[k]]
    if bad:
        raise LunarMismatch(
            f"Lịch {target}: hai nguồn không khớp -> DỪNG, không sinh kịch bản.\n  "
            + "\n  ".join(bad)
            + "\nNếu vừa đổi phiên bản vnlunar: cài lại bản đã ghim (pip install vnlunar==1.0.5).")

    truc = ours["trực"]
    god = ours["sao (12 thần)"]
    good_for, bad_for = TRUC_VIEC[truc]
    stars = info.get("12_stars") or {}
    return DayFacts(
        target=target,
        lunar_day=lunar["day"],
        lunar_month=lunar["month"],
        can_chi_day=ours["can chi ngày"],
        day_type="Hoàng Đạo" if god in AUSPICIOUS_GODS else "Hắc Đạo",
        god_name=god,
        truc_name=truc,
        truc_good_for=good_for,
        truc_bad_for=bad_for,
        star_name=stars.get("name", truc.split()[-1].capitalize()),
        star_desc=stars.get("description", ""),
        mansion_name=ours["tú"],
        mansion_good=ours["tú tốt/xấu"],
        mansion_animal=_tu_animal(ours["tú"], mansion.get("animal", "")),
        mansion_element=TU28[mi][1],
        day_of_week=(info.get("solar") or {}).get("day_of_week", ""),
        nayin_name=nap_am_of(sixty_index(target)),
        auspicious_hours=ours["giờ hoàng đạo"],
        good_directions=(info.get("directions") or {}).get("good_text", ""),
        conflict_animal=ours["tuổi xung"],
        conflict_chi=ours["chi xung"],
        day_animal=ours["con giáp ngày"],
        wealth_god_dir=ours["hướng Tài thần"],
        joy_god_dir=ours["hướng Hỷ thần"],
        lunar_leap=bool(lunar.get("leap")),
    )


def facts_range(start: date, days: int) -> list[DayFacts]:
    return [facts_for(start + timedelta(days=i)) for i in range(days)]


def truc_name_of(d: date) -> str:
    """Trực của một ngày (đã đối chiếu kép). Dùng cho bộ đếm thống kê."""
    return facts_for(d).truc_name
