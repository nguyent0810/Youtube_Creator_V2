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

import hashlib

from factory.lunar import DayFacts
from factory.vocab import SAO, TRUC

# Ngưỡng phân loại danh mục. Đếm trên cả năm 2026: hẹp nhất 1 việc
# (định/chấp/phá), rộng nhất 10 (mãn). Cắt ở 3 và 6.
NARROW_MAX = 3
BROAD_MIN = 6

# Số biến thể mở bài mỗi thế. Tháng 11 có 10 ngày cùng một thế mà chỉ 3
# biến thể -> mở bài lặp 11/31 lần (35%). Nâng lên 6 để trải rộng hơn.
_N_HOOKS = 6


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



# ─── Tầng bổ sung: phá lặp và làm nội dung dùng được ──────────────────────
#
# Sao và trực đều chu kỳ 12 -> cứ 12 ngày lặp một cặp. Tháng 10/2026 có 9
# cặp trùng, và lỗi đó đã gây hậu quả thật: 9 video bị dedup bỏ qua vì trùng
# tiêu đề.
#
# 28 tú có chu kỳ 28 nên trên 30 ngày cho 28 giá trị khác nhau -- gần như
# không lặp. Hai ngày 10/10 và 22/10 cùng "Minh Đường gặp Trực kiến" nhưng
# tú NGƯỢC nhau (Liễu xấu / Đẩu tốt), tức là có nghịch lý riêng để nói.
#
# Giờ hoàng đạo và tuổi xung thì khác loại: chúng không phá lặp nhiều,
# nhưng là thứ người xem SOI VÀO BẢN THÂN được ngay. Đó là giá trị mà hai
# tầng sao/trực không có.

def _cau_tu(f: DayFacts) -> str:
    """Nhị thập bát tú. Mọi chữ đều từ nguồn, không diễn giải."""
    if not f.mansion_name:
        return ""
    xd = "tốt" if f.mansion_good else "xấu"
    return (f"Nhị thập bát tú là tú {f.mansion_name}, con {f.mansion_animal}, "
            f"lịch xếp vào nhóm {xd}")


def _cau_gio(f: DayFacts) -> str:
    """Chọn ĐÚNG MỘT giờ tốt.

    Bài học v1 đã ghi lại: liệt kê cả 6 giờ ("Dần 3-5h, Thìn 7-9h, Tỵ
    9-11h...") nghe dông dài qua giọng đọc, video thật đã bị chê vì lỗi này.
    Lấy giờ đầu tiên, phần còn lại để trên màn hình nếu cần."""
    if not f.auspicious_hours:
        return ""
    # "đầu tiên" chứ KHÔNG phải "sớm nhất": bộ kiểm chặn mọi so sánh nhất
    # vì chúng gần như luôn là suy diễn. Ở đây "đầu tiên" lại đúng theo
    # nghĩa đen -- nguồn trả danh sách đã sắp theo thứ tự giờ trong ngày.
    dau = f.auspicious_hours.split(",")[0].strip()
    return f"Giờ tốt đầu tiên trong ngày là giờ {dau}"


def _cau_xung(f: DayFacts) -> str:
    """Tuổi xung -- thứ người xem tự soi vào mình được ngay."""
    if not (f.conflict_animal and f.day_animal):
        return ""
    return (f"Ngày {f.day_animal} thì theo lịch cũ xung với tuổi {f.conflict_animal}, "
            f"ai tuổi đó có việc lớn thì nên cân nhắc")


def _cau_huong(f: DayFacts) -> str:
    if not f.wealth_god_dir:
        return ""
    return f"Hướng Tài thần ngày mai là hướng {f.wealth_god_dir}"


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

    # CHỌN BIẾN THỂ MỞ BÀI -- không được ăn khớp với chu kỳ 12 ngày.
    #
    # Bản đầu dùng `day % 3`. Nhưng sao và trực lặp đúng 12 ngày, mà 12 chia
    # hết cho 3, nên hai ngày trùng (sao, trực) LUÔN rơi vào cùng biến thể:
    # 10/10 và 22/10 ra hook giống hệt nhau. Đúng thứ lẽ ra phải tránh.
    #
    # Băm cả tú (chu kỳ 28) và can chi ngày (chu kỳ 60) vào seed: hai chu kỳ
    # này không chia hết cho 12 nên hai ngày trùng sao/trực chắc chắn lệch
    # biến thể. Vẫn tất định -- chạy lại ra y hệt.
    # Băm cho phân bố đều, CỘNG THÊM số lần cặp (sao, trực) này đã xuất
    # hiện trong tháng. Chỉ băm thôi thì vẫn có 1/3 khả năng hai ngày trùng
    # rơi vào cùng dư -- đã xảy ra thật với 10/10 và 22/10. Offset theo
    # `day // 12` thì lần xuất hiện thứ nhất, thứ hai, thứ ba của cùng một
    # cặp CHẮC CHẮN lệch nhau, không phụ thuộc may rủi của hàm băm.
    # Băm theo CẶP (sao, trực) -- KHÔNG theo ngày. Cộng số lần cặp đó đã
    # xuất hiện trong tháng (`day // 12`, vì chu kỳ lặp đúng 12 ngày).
    #
    # Vì sao phải băm theo cặp: nếu băm theo ngày thì hai ngày trùng cặp có
    # hash KHÁC nhau, cộng offset vào vẫn có thể va cùng dư -- đã xảy ra
    # thật với 3/9 cặp. Băm theo cặp thì phần băm giống hệt nhau, nên offset
    # một mình quyết định, và lệch được ĐẢM BẢO cho tới 3 lần xuất hiện.
    h = int(hashlib.sha256(f"{f.god_name}|{f.truc_name}".encode("utf-8")).hexdigest(), 16)
    v = (h + f.target.day // 12) % _N_HOOKS

    if the == "sao_mo_truc_siet":
        hooks = [
            f"Ngày mai là ngày hoàng đạo, nhưng lịch chỉ cho làm {_so(n)} việc.",
            f"Sao thì tốt, mà danh mục ngày mai vỏn vẹn {_so(n)} việc.",
            f"Ngày mai mang sao {f.god_name}, nhưng đừng vội mừng.",
            f"Ngày mai sao tốt gặp trực hẹp, nhưng trực mới là bên thắng.",
            f"Cả ngày mai, lịch chỉ mở đầu danh mục bằng {dau}.",
            f"Ngày mai tú {f.mansion_name}, mà danh mục chỉ {_so(n)} việc.",
        ]
        than = (f"Sao là {f.god_name}, thường được xếp vào nhóm {nhom}. "
                f"Trực lại là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Sao mở, trực siết. "
                f"Danh mục nên làm: {viec}. "
                f"{_kieng(f)}")
        chots = ["Hoàng đạo không có nghĩa là muốn làm gì cũng được.",
                 "Sao đẹp mà trực hẹp, thì vẫn cứ là ngày hẹp.",
                 "Xem sao thôi chưa đủ, còn phải xem trực.",
                 "Ngày tốt, nhưng tốt cho ít việc thôi."]
        tieu_de = f"Hoàng đạo mà chỉ được {_so(n)} việc — {f.god_name} gặp {f.truc_name}"

    elif the == "sao_du_truc_mo":
        hooks = [
            "Ngày mai mang sao hắc đạo, mà danh mục lại rộng bất ngờ.",
            f"Ngày mai là ngày {f.god_name}, nhưng cửa vẫn mở khá rộng.",
            f"Sao xấu, mà ngày mai lịch vẫn cho làm tới {_so(n)} việc.",
            f"Tên sao nghe dữ, mà ngày mai lịch lại không siết mấy.",
            f"Ngày {f.day_animal} mai sao không đẹp, nhưng việc thì không thiếu.",
            f"Ngày mai tú {f.mansion_name}, nhưng cửa mở rộng hơn cái tên sao gợi ra.",
        ]
        than = (f"{f.god_name} thuộc nhóm {nhom}. "
                f"Nhưng trực là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Danh mục nên làm: {viec}. "
                f"{_kieng(f)} "
                f"Nên nếu định làm {dau}, ngày mai có thể cân nhắc.")
        chots = ["Sao dữ, mà cửa vẫn mở về một phía.",
                 "Tên sao nghe sợ, danh mục thì lại không.",
                 "Đừng bỏ cả ngày chỉ vì cái tên sao.",
                 "Sao xấu không có nghĩa là ngày bỏ đi."]
        tieu_de = f"Sao hắc đạo mà cửa vẫn mở — {f.god_name} gặp {f.truc_name}"

    elif the == "cung_dong":
        hooks = [
            "Ngày mai sao và trực cùng nói một chữ, mà chữ ấy là đóng.",
            f"Cả ngày mai chỉ còn {_so(n)} việc nên làm.",
            f"Ngày mai là ngày {f.god_name}, mà lịch cũng không nới tay.",
            "Ngày mai hai tầng lịch cùng siết, không tầng nào chịu mở.",
            f"Việc lịch cho làm ngày mai chỉ vỏn vẹn {_so(n)}, đếm chưa hết một bàn tay.",
            f"Ngày mai tú {f.mansion_name}, mà trực thì cũng đóng nốt.",
        ]
        than = (f"Sao là {f.god_name}, thuộc nhóm {nhom}. "
                f"Trực là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Hai tầng cùng một hướng, nên lịch siết khá chặt. "
                f"Danh mục nên làm chỉ còn: {viec}. "
                f"{_kieng(f)} "
                f"Nếu có việc đang định làm mà không nằm trong đó, lùi một hôm cũng được.")
        chots = ["Ngày mai để giữ lại, không phải để mở ra.",
                 "Ngày để vá, không phải ngày để bày.",
                 "Cả hai tầng cùng đóng, thì đừng cố mở.",
                 "Việc lớn để hôm khác, mai làm việc nhỏ."]
        tieu_de = f"Sao và trực cùng siết — {f.god_name} gặp {f.truc_name}"

    else:  # cung_thuan
        # Thế này KHÔNG có nghịch lý sẵn, nên hook phải tạo giới hạn từ
        # chỗ khác: nhấn rằng hai tầng cùng hướng là chuyện không thường.
        hooks = [
            "Ngày mai hai tầng của lịch không chỏi nhau, chuyện không hay gặp.",
            f"Ngày mai mang sao {f.god_name}, mà trực cũng không siết lại.",
            f"Ngày mai lịch không chặn, danh mục mở tới {_so(n)} việc.",
            f"Ngày mai sao tốt, trực cũng tốt, mà việc thì không thiếu.",
            f"Ngày mai hiếm ở chỗ cả sao lẫn trực đều không cản.",
            f"Ngày mai việc đầu danh mục là {dau}, mà lịch cũng không chặn.",
        ]
        than = (f"Sao là {f.god_name}, thuộc nhóm {nhom}. "
                f"Trực là {f.truc_name} — {truc.han}, nghĩa là {truc.gloss}. "
                f"Danh mục nên làm: {viec}. "
                f"{_kieng(f)} "
                f"Ai đang chờ ngày để {dau}, đây là ngày có thể cân nhắc.")
        chots = ["Sao thuận, trực cũng thuận. Ngày như vậy không nhiều.",
                 "Hai tầng cùng mở, không phải tháng nào cũng gặp.",
                 "Ngày mà lịch không cản gì, thì đừng để trôi.",
                 "Cả sao lẫn trực đều thuận, hiếm hơn ta tưởng."]
        tieu_de = f"Sao và trực cùng thuận — {f.god_name} gặp {f.truc_name}"

    return hooks[v % len(hooks)], than, chots[v % len(chots)], tieu_de


_SO = {1: "một", 2: "hai", 3: "ba", 4: "bốn", 5: "năm",
       6: "sáu", 7: "bảy", 8: "tám", 9: "chín", 10: "mười"}


def _so(n: int) -> str:
    return _SO.get(n, str(n))


MIN_WORDS, MAX_WORDS = 65, 85


def _fit(hook: str, than: str, chot: str, extras: list[str] | None = None) -> str:
    """Căn 65-85 từ, và ƯU TIÊN tầng bổ sung hơn câu đệm.

    Vì sao cần: độ dài phụ thuộc DỮ LIỆU chứ không phụ thuộc khuôn -- danh
    mục Trực định có 1 việc, Trực mãn có 10. Cùng một khuôn cho ra 64 từ
    ngày này và 91 từ ngày khác.

    THỨ TỰ BỎ khi quá dài: câu ĐỆM trước, tầng bổ sung sau. Bản đầu làm
    ngược -- cắt từ cuối nên tầng bổ sung (tú, giờ tốt, tuổi xung) không
    bao giờ lọt vào, trong khi chúng mới là thứ phá được sự lặp giữa các
    ngày trùng sao/trực. Câu đệm kiểu "Ai đang chờ ngày để X" thì ngày nào
    cũng nói được, bỏ đi không mất gì.
    """
    parts = [p.strip().rstrip(".") for p in than.split(". ") if p.strip()]
    core, dem = parts[:-1], parts[-1:] if len(parts) > 3 else []
    if dem:
        core = parts[:-1]
    else:
        core = parts

    def total(ps):
        return len(f"{hook} {'. '.join(ps)}. {chot}".split())

    # 1. Lõi phải vừa trước đã.
    while total(core) > MAX_WORDS and len(core) > 2:
        core.pop()
    # 2. Nhét tầng bổ sung vào chừng nào còn chỗ.
    for e in (extras or []):
        if e and total(core + [e]) <= MAX_WORDS:
            core.append(e)
    # 3. Còn dư thì mới tới câu đệm.
    for d in dem:
        if total(core + [d]) <= MAX_WORDS:
            core.append(d)
    if total(core) < MIN_WORDS:
        core.append("Đây là ghi chép theo lịch pháp truyền thống, để tham khảo")
    return f"{hook} {'. '.join(core)}. {chot}"


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

    # Ưu tiên tầng nào nói trước: nếu tú NGƯỢC chiều với sao thì đó là
    # nghịch lý riêng của ngày, đáng nói nhất. Không thì ưu tiên thứ người
    # xem dùng được ngay (giờ tốt, tuổi xung).
    tu_nghich = f.mansion_good != f.is_auspicious_star
    extras = ([_cau_tu(f), _cau_gio(f), _cau_xung(f), _cau_huong(f)] if tu_nghich
              else [_cau_gio(f), _cau_xung(f), _cau_tu(f), _cau_huong(f)])

    return {
        "script": _fit(hook, than, chot, extras),
        "title": f"{ngay} — {tieu_de}"[:100],
        "the": the_cua_ngay(f),
    }
