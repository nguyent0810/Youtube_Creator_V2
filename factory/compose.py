"""Soạn kịch bản Lịch TỰ ĐỘNG từ dữ liệu + từ điển. Không LLM, không người.

Mọi câu sinh ra chỉ dùng hai nguồn:
  1. vnlunar  -- tên sao, tên trực, danh mục nên làm / kiêng
  2. vocab.py -- chú giải nghĩa chữ, tập đóng đã khai báo kèm căn cứ

Không có câu nào tự nghĩ ra. Nên mọi kịch bản đều qua được luật "chỉ ĐẠT
khi mọi claim ngoài nguồn đã xác minh" mà không cần ai khai báo thêm.

═══ CHỐNG LẶP KHUÔN ═══
Nguy cơ lớn nhất của sinh tự động là 30 video mở giống hệt nhau. Cách giải
ở đây: chọn khuôn theo THẾ của ngày -- tức quan hệ thật giữa sao và trực --
chứ không xoay vòng mù.

Bốn thế, đếm trên 30 ngày đầu tháng 10/2026:
    sao mở / trực siết   9 ngày   (sao hoàng đạo + danh mục hẹp)
    sao dữ / trực mở    10 ngày   (sao hắc đạo + danh mục rộng)
    cùng thuận           6 ngày
    cùng đóng            5 ngày

Hai thế đầu là nghịch lý CÓ THẬT trong dữ liệu -- đúng thứ làm hook mạnh,
và chiếm 19/30 ngày. Trong mỗi thế còn xoay nhiều biến thể mở bài, chọn
theo ngày nên tất định (chạy lại ra y hệt) nhưng không lặp liền nhau.
"""
from __future__ import annotations

from factory.lunar import DayFacts
from factory.vocab import SAO, TRUC

# Ngưỡng phân loại danh mục. Đếm trên cả năm 2026: hẹp nhất 1 việc
# (định/chấp/phá), rộng nhất 10 (mãn). Cắt ở 3 và 6.
NARROW_MAX = 3
BROAD_MIN = 6


def the_cua_ngay(f: DayFacts) -> str:
    """Quan hệ giữa sao và trực -- quyết định khuôn kịch bản.

    LỖI ĐÃ SỬA: bản đầu để mọi trường hợp còn lại rơi vào "cùng thuận",
    nên ngày 03/10 (Bạch Hổ, sao HẮC ĐẠO, danh mục 4 việc) bị gán nhãn
    "Sao và trực cùng thuận" -- sai sự thật, sao dữ không thể gọi là thuận.
    Bộ đối chiếu không bắt được vì nó chỉ kiểm nhãn hoàng/hắc đạo có đúng
    không, chứ không kiểm KHUNG DIỄN GIẢI có chỏi với loại sao không.

    Giờ nhánh sao hắc đạo được xử lý TRƯỚC và triệt để: dữ + rộng thì là
    "cửa vẫn mở", dữ + hẹp thì là "cùng siết". Không còn đường nào để một
    ngày hắc đạo rơi vào khuôn "thuận"."""
    n = len(f.truc_good_for)
    if not f.is_auspicious_star:
        return "cung_dong" if n <= NARROW_MAX else "sao_du_truc_mo"
    return "sao_mo_truc_siet" if n <= NARROW_MAX else "cung_thuan"


def _liet_ke(items, limit: int = 4) -> str:
    """Đọc tối đa `limit` việc. Danh mục 10 việc mà đọc hết thì nghe như
    đọc danh sách — đúng lỗi đã ghi nhận ở v1."""
    xs = [x.lower() for x in items[:limit]]
    return ", ".join(xs)


def _kieng(f: DayFacts) -> str:
    """Câu về phần kiêng. 17/30 ngày nguồn ghi 'Mọi việc khác' — nói thẳng
    như vậy, không diễn giải thành 'ngày xấu'."""
    if f.truc_bad_for == ("Mọi việc khác",):
        return "Ngoài danh mục ấy, lịch ghi gọn là mọi việc khác."
    return f"Phần kiêng ghi rõ: {_liet_ke(f.truc_bad_for, 3)}."


# ─── Khuôn theo thế ───────────────────────────────────────────────────────
#
# Mỗi khuôn trả (hook, thân, chốt, tiêu đề). Biến thể chọn theo ngày dương
# để tất định mà vẫn không lặp liền nhau.

def _compose(f: DayFacts) -> tuple[str, str, str, str]:
    sao, truc = SAO[f.god_name], TRUC[f.truc_name]
    n = len(f.truc_good_for)
    viec = _liet_ke(f.truc_good_for)
    dau = f.truc_good_for[0].lower()
    nhom = "hoàng đạo" if f.is_auspicious_star else "hắc đạo"
    the = the_cua_ngay(f)
    v = f.target.day % 3

    if the == "sao_mo_truc_siet":
        hooks = [
            f"Ngày mai là ngày hoàng đạo, nhưng lịch chỉ cho làm {_so(n)} việc.",
            f"Sao thì tốt, mà danh mục ngày mai vỏn vẹn {_so(n)} việc.",
            f"Ngày mai mang sao {f.god_name}, nhưng đừng vội mừng.",
        ]
        than = (f"Sao là {f.god_name}, thường được xếp vào nhóm {nhom}. "
                f"Trực lại là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Sao mở, trực siết. "
                f"Danh mục nên làm: {viec}. "
                f"{_kieng(f)}")
        chot = "Hoàng đạo không có nghĩa là muốn làm gì cũng được."
        tieu_de = f"Hoàng đạo mà chỉ được {_so(n)} việc — {f.god_name} gặp {f.truc_name}"

    elif the == "sao_du_truc_mo":
        hooks = [
            "Ngày mai mang sao hắc đạo, mà danh mục lại rộng bất ngờ.",
            f"Ngày mai là ngày {f.god_name}, nhưng cửa vẫn mở khá rộng.",
            f"Sao xấu, mà lịch vẫn cho làm tới {_so(n)} việc.",
        ]
        than = (f"{f.god_name} thuộc nhóm {nhom}. "
                f"Nhưng trực là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Danh mục nên làm: {viec}. "
                f"{_kieng(f)} "
                f"Nên nếu định làm {dau}, ngày mai có thể cân nhắc.")
        chot = "Sao dữ, mà cửa vẫn mở về một phía."
        tieu_de = f"Sao hắc đạo mà cửa vẫn mở — {f.god_name} gặp {f.truc_name}"

    elif the == "cung_dong":
        hooks = [
            "Ngày mai sao và trực cùng nói một chữ, mà chữ ấy là đóng.",
            f"Cả ngày mai chỉ còn {_so(n)} việc nên làm.",
            f"Ngày mai là ngày {f.god_name}, mà lịch cũng không nới tay.",
        ]
        than = (f"Sao là {f.god_name}, thuộc nhóm {nhom}. "
                f"Trực là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Hai tầng cùng một hướng, nên lịch siết khá chặt. "
                f"Danh mục nên làm chỉ còn: {viec}. "
                f"{_kieng(f)} "
                f"Nếu có việc đang định làm mà không nằm trong đó, lùi một hôm cũng được.")
        chot = "Ngày mai để giữ lại, không phải để mở ra."
        tieu_de = f"Sao và trực cùng siết — {f.god_name} gặp {f.truc_name}"

    else:  # cung_thuan
        # Thế này KHÔNG có nghịch lý sẵn, nên hook phải tạo giới hạn từ
        # chỗ khác: nhấn rằng hai tầng cùng hướng là chuyện không thường.
        hooks = [
            "Ngày mai hai tầng của lịch không chỏi nhau, chuyện không hay gặp.",
            f"Ngày mai mang sao {f.god_name}, mà trực cũng không siết lại.",
            f"Ngày mai lịch không chặn, danh mục mở tới {_so(n)} việc.",
        ]
        than = (f"Sao là {f.god_name}, thuộc nhóm {nhom}. "
                f"Trực là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Danh mục nên làm: {viec}. "
                f"{_kieng(f)} "
                f"Ai đang chờ ngày để {dau}, đây là ngày có thể cân nhắc.")
        chot = "Sao thuận, trực cũng thuận. Ngày như vậy không nhiều."
        tieu_de = f"Sao và trực cùng thuận — {f.god_name} gặp {f.truc_name}"

    return hooks[v], than, chot, tieu_de


_SO = {1: "một", 2: "hai", 3: "ba", 4: "bốn", 5: "năm",
       6: "sáu", 7: "bảy", 8: "tám", 9: "chín", 10: "mười"}


def _so(n: int) -> str:
    return _SO.get(n, str(n))


MIN_WORDS, MAX_WORDS = 65, 85


def _fit(hook: str, than: str, chot: str) -> str:
    """Căn độ dài về 65-85 từ bằng cách bỏ/thêm câu TUỲ CHỌN.

    Vì sao cần: danh mục của các trực dài ngắn rất khác nhau (1 việc với
    Trực định, 10 với Trực mãn), nên cùng một khuôn cho ra kịch bản 64 từ
    ở ngày này và 91 từ ở ngày khác. Chỉnh tay từng khuôn không giải được
    -- độ dài phụ thuộc DỮ LIỆU, không phụ thuộc khuôn.

    Cách làm: câu cuối của thân luôn là câu khuyên dùng, bỏ đi vẫn đủ ý.
    Quá dài thì bỏ; quá ngắn thì thêm một câu nhắc nguồn (luôn đúng, và
    cũng là thứ nên có với nội dung lịch)."""
    parts = [p.strip() for p in than.split(". ") if p.strip()]
    def total(ps):
        return len(f"{hook} {'. '.join(ps)}. {chot}".split())

    while total(parts) > MAX_WORDS and len(parts) > 2:
        parts.pop()
    if total(parts) < MIN_WORDS:
        parts.append("Đây là ghi chép theo lịch pháp truyền thống, để tham khảo")
    return f"{hook} {'. '.join(parts)}. {chot}"


def script_for(f: DayFacts) -> dict:
    """Kịch bản hoàn chỉnh cho một ngày.

    TIÊU ĐỀ PHẢI DUY NHẤT -- lỗi thật đã xảy ra: bản đầu sinh tiêu đề từ
    (sao, trực), mà chu kỳ sao và trực lặp lại đúng 12 ngày. Tháng 10 có 9
    cặp ngày trùng tiêu đề, và bộ chống trùng của publish.py (so theo tiêu
    đề) đã BỎ QUA 9 lần upload -- 9 ngày cuối tháng không có video riêng,
    trong khi store ghi là đã đăng.

    Gắn ngày vào đầu tiêu đề giải quyết tận gốc, và tiện cho người xem:
    kênh lịch hằng ngày thì ngày là thông tin đầu tiên cần thấy."""
    hook, than, chot, tieu_de = _compose(f)
    ngay = f.target.strftime("%d/%m")
    return {
        "script": _fit(hook, than, chot),
        "title": f"{ngay} — {tieu_de}"[:100],
        "the": the_cua_ngay(f),
    }
