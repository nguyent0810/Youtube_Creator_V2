"""Kênh Phật Giáo (BUD). 5 dòng, mỗi dòng 1 short/ngày.

Chọn theo số liệu thật của kênh (21/09/2026, 289 short gần nhất, trung vị 888):
  - "Vì sao Văn Thù cầm kiếm?" 1.517 — câu hỏi biểu tượng thắng  -> bud-visao
  - "Phật là thần hay người?" 1.285 — bẻ hiểu lầm                -> bud-hieulam
  - "Bát Chánh Đạo không phải đi từng bước" 943 — số pháp        -> bud-sophap
  - Pháp Cú 423 kệ, bản dịch CC0 (SuttaCentral)                  -> bud-phapcu
  - Lịch âm (vnlunar, đã chạy ở FS) + 13 ngày vía có nguồn        -> bud-lich (khuôn, không cạn)
"Lời Phật Dạy Ngày…" 8 giây chỉ 17 view: bài học là phải có hook + đủ ý,
không phải trích một câu rồi hết.
"""
from __future__ import annotations

from datetime import date, timedelta

from factory.lines import base
from factory.pillars.check import Draft

CHANNEL = "BUD"
PILLARS = {
    "lich":    ("bud-lich-", "06:30", "lịch Phật giáo hằng ngày"),
    "visao":   ("bud-visao-", "10:30", "vì sao — biểu tượng"),
    "hieulam": ("bud-hieulam-", "14:30", "hiểu đúng, hiểu lầm"),
    "phapcu":  ("bud-phapcu-", "18:30", "Pháp Cú mỗi ngày"),
    "sophap":  ("bud-sophap-", "21:00", "số pháp"),
}
FICTION: set = set()
STYLE = {
    "lich":    ("Thục Đoan", "meditation_impromptu_01.mp3"),
    "visao":   ("Thiền Tâm Đức", "meditation_impromptu_02.mp3"),
    "hieulam": ("Anh Khôi", "deliberate_thought.mp3"),
    "phapcu":  ("Ngọc Huyền", "meditation_impromptu_03.mp3"),
    "sophap":  ("Thiền Tâm Đức", "meditation_impromptu_01.mp3"),
}
TAGS = {
    "lich":    ["lich phat giao", "ngay via", "am lich", "phat giao"],
    "visao":   ["phat giao", "bieu tuong phat giao", "bo tat", "tuong phat"],
    "hieulam": ["phat giao", "hieu dung phat giao", "phat phap", "dao phat"],
    "phapcu":  ["kinh phap cu", "loi phat day", "dhammapada", "phat phap"],
    "sophap":  ["phat phap", "giao ly phat giao", "tu dieu de", "bat chanh dao"],
}
_CALM = ["lotus flower pond", "buddha statue temple", "incense smoke temple", "monk walking temple",
         "candle light temple", "bodhi tree leaves", "temple bell", "misty mountain temple",
         "prayer beads hands", "stone buddha garden", "sunrise over temple", "water drop lotus leaf",
         "bamboo forest light", "zen garden stones"]
BROLL = {k: _CALM for k in PILLARS}

# 13 ngày vía theo âm lịch — nguồn: Tạp chí Nghiên cứu Phật học,
# https://tapchinghiencuuphathoc.vn/cac-ngay-via-phat-bo-tat.html (đối chiếu 21/09/2026).
# (tháng, ngày) -> (tên, một câu giải thích an toàn)
VIA = {
    (1, 1): ("vía đức Phật Di Lặc", "Di Lặc được xem là vị Phật tương lai trong truyền thống Phật giáo"),
    (2, 8): ("vía Phật Thích Ca xuất gia", "ngày tưởng niệm Thái tử Tất-đạt-đa rời hoàng cung đi tìm đạo"),
    (2, 15): ("vía Phật Thích Ca nhập diệt", "ngày tưởng niệm Đức Phật nhập Niết-bàn"),
    (2, 19): ("vía Bồ Tát Quán Thế Âm đản sinh", "một trong ba ngày vía Quán Thế Âm trong năm"),
    (2, 21): ("vía Bồ Tát Phổ Hiền", "Phổ Hiền gắn với đại hạnh, hình ảnh cưỡi voi trắng"),
    (4, 8): ("vía Phật Thích Ca đản sinh", "ngày tưởng niệm Đức Phật ra đời"),
    (4, 28): ("vía Phật Dược Sư đản sinh", "Dược Sư gắn với nguyện cứu khổ bệnh tật"),
    (6, 19): ("vía Bồ Tát Quán Thế Âm thành đạo", "ngày vía thứ hai của Quán Thế Âm trong năm"),
    (7, 15): ("lễ Vu Lan", "mùa báo hiếu, gắn với tích Mục Kiền Liên cứu mẹ"),
    (7, 30): ("vía Bồ Tát Địa Tạng", "Địa Tạng gắn với đại nguyện cứu độ chúng sinh nơi khổ cảnh"),
    (9, 30): ("vía Phật Dược Sư thành đạo", "ngày vía thứ hai của Phật Dược Sư trong năm"),
    (11, 17): ("vía Phật A Di Đà đản sinh", "A Di Đà gắn với pháp môn niệm Phật Tịnh Độ"),
    (12, 8): ("vía Phật Thích Ca thành đạo", "ngày tưởng niệm Đức Phật thành đạo dưới cội Bồ-đề"),
}
SRC_VIA = "https://tapchinghiencuuphathoc.vn/cac-ngay-via-phat-bo-tat.html"


# Câu thực hành xoay vòng theo ngày -- lời khuyên nhẹ, không phải dữ kiện.
PRACTICE = [
    "Việc nhỏ cho hôm nay: bớt một lời nặng, thêm một lời tử tế.",
    "Thử dành năm phút ngồi yên, chỉ theo dõi hơi thở vào ra.",
    "Hôm nay có thể ăn chay một bữa, hoặc đơn giản là ăn chậm lại.",
    "Gọi điện hỏi thăm cha mẹ cũng là một cách thực hành hiếu hạnh.",
    "Trước khi nổi giận, thử đếm chậm đến mười.",
    "Tặng một món đồ mình không còn dùng cho người cần hơn.",
    "Tối nay trước khi ngủ, nhớ lại một điều tốt mình đã làm trong ngày.",
    "Buông điện thoại một giờ, nghe người thân nói trọn một câu chuyện.",
    "Nếu làm ai buồn lòng, hôm nay là ngày tốt để nói lời xin lỗi.",
    "Tưới một chậu cây, dọn một góc nhà, cho tâm cũng gọn gàng theo.",
    "Nhìn một người khó chịu với mình và thử nghĩ: họ cũng đang có nỗi khổ riêng.",
    "Làm một việc tốt mà không kể cho ai biết.",
]
CLOSE = ["Hôm nay bạn định làm một việc tốt nào?", "Bạn thường chuẩn bị gì cho những ngày này?",
         "Comment một điều bạn biết ơn hôm nay.", "Bạn có hay đi chùa ngày rằm, mùng một không?"]


def _event(f):
    """Sự kiện của một ngày âm (nếu có): ngày vía, rằm, mùng 1."""
    key = (f.lunar_month, f.lunar_day)
    if key in VIA:
        return VIA[key]
    if f.lunar_day == 15:
        return (f"rằm tháng {f.lunar_month} âm lịch", "ngày trăng tròn, nhiều gia đình đi chùa, ăn chay, tụng kinh")
    if f.lunar_day == 1:
        return (f"mùng 1 tháng {f.lunar_month} âm lịch", "ngày đầu tháng âm, nhiều người đi chùa cầu an")
    return None


def lich_ngay(history, day) -> Draft | None:
    if day is None:
        return None
    from factory.lunar import facts_for
    f = facts_for(day)
    ev = _event(f)
    ld, lm = f.lunar_day, f.lunar_month
    am = f"mùng {ld}" if ld <= 10 else f"ngày {ld}"
    tip = PRACTICE[day.toordinal() % len(PRACTICE)]
    close = CLOSE[day.toordinal() % len(CLOSE)]
    if ev:
        name, gloss = ev
        s = [f"Hôm nay là {name}, nhưng ý nghĩa thật của ngày này là gì?",
             f"Ngày {day.day} tháng {day.month} dương lịch, nhằm {am} tháng {lm} âm lịch.",
             f"Đây là {gloss}.", tip,
             "Không cần mâm cao cỗ đầy, một tâm thành là đủ để bắt đầu.", close]
        key = day.isoformat()
        title = f"{day.day}/{day.month}: {name[0].upper() + name[1:]}"
    else:
        # Đếm THẬT trên lịch: quét tới sự kiện kế tiếp, không ước lượng.
        n, nxt, nf = None, None, None
        for k in range(1, 40):
            g = facts_for(day + timedelta(days=k))
            e = _event(g)
            if e:
                n, nxt, nf = k, e, g
                break
        if not nxt:
            return None
        name, gloss = nxt
        nam = f"mùng {nf.lunar_day}" if nf.lunar_day <= 10 else f"ngày {nf.lunar_day}"
        when = "" if "âm lịch" in name else f", nhằm {nam} tháng {nf.lunar_month} âm lịch"
        s = [f"Còn {n} ngày nữa là {name}{when}.",
             f"Hôm nay {day.day} tháng {day.month} là {am} tháng {lm} âm lịch.",
             f"{name[0].upper() + name[1:]} là {gloss}.", tip, close]
        if len(" ".join(s).split()) < 62:        # ngày ngắn chữ -> thêm một lời nhắc thứ hai
            s.insert(-1, PRACTICE[(day.toordinal() + 5) % len(PRACTICE)])
        key = day.isoformat()
        title = f"Còn {n} ngày tới {name}"
    from factory.pillars.expand import pick_broll
    return Draft("lich", key, title, " ".join(s), [],
                 ["Lịch âm: vnlunar", f"Ngày vía: {SRC_VIA}"], pick_broll(BROLL["lich"], key), "lich", set())


TEMPLATES = {"lich": lich_ngay}
_self = __import__(__name__, fromlist=["x"])
next_draft = base.make_next_draft(_self)
ALL_NAMES: set = set()


def load_history(bundle_dir):
    return base.load_history(bundle_dir, CHANNEL)


def check_draft(d, history):
    return base.check_draft(_self, d, history)
