"""7 Bundle Lịch Hoàng Đạo cho 01-07/10/2026.

DỮ LIỆU: lấy từ vnlunar, KHÔNG bịa. Mỗi kịch bản chỉ diễn giải đúng những
con số đã tính ra.

BỎ HẲN nhãn "Hoàng Đạo / Hắc Đạo" trong 7 kịch bản này. Lý do cụ thể, không
phải thận trọng chung chung: vnlunar tự mâu thuẫn ở 3/7 ngày --

    01/10  day_type=Hắc Đạo   nhưng sao Kim Quỹ    = "Sao tốt - Hoàng Đạo"
    04/10  day_type=Hắc Đạo   nhưng sao Ngọc Đường = "Sao tốt - Hoàng Đạo"
    06/10  day_type=Hoàng Đạo nhưng sao Huyền Vũ   = "Sao xấu - Hắc Đạo"

Theo truyền thống, Kim Quỹ/Ngọc Đường/Thiên Đức/Tư Mệnh là hoàng đạo, còn
Bạch Hổ/Thiên Lao/Huyền Vũ là hắc đạo -- tức trường `12_gods` khớp truyền
thống còn `day_type` mới là trường sai. Nhưng tôi không tự ý chọn bên khi
nội dung này ảnh hưởng tới việc người xem chọn ngày làm việc thật.

Thay vào đó, 7 kịch bản xoay quanh phần dữ liệu KHÔNG mâu thuẫn và vốn
cũng hành động được hơn: TRỰC của ngày và danh sách việc hợp với trực đó.
"Ngày mai hợp khai trương" cụ thể hơn "ngày mai là hoàng đạo" nhiều.

XƯNG HÔ: mọi kịch bản nói "ngày mai", vì video đăng trước một ngày. Lùi
lịch mà giữ câu chữ cũ thì người xem làm theo vào SAI NGÀY.
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.bundle import Bundle  # noqa: E402
from factory.lunar import facts_range  # noqa: E402

VOICE = "Anh Khôi"          # nam Bắc, phong cách kể chuyện
BGM = "asian_drums.mp3"

# Kịch bản viết tay theo đúng facts của từng ngày. Mỗi cái: hook -> căn cứ
# -> việc cụ thể -> hạ rào cản -> chốt vọng lại hook.
SCRIPTS = {
    "2026-10-01": (
        "Ngày mai không phải ngày để bắt đầu việc lớn.",
        "Lịch cũ ghi ngày mai là Trực nguy, nhóm trực được xem là chỉ hợp vài việc rất hẹp. "
        "Trong danh sách chỉ có an sàng, tức kê giường, và vài việc thuộc về sắp đặt chỗ ở. "
        "Vậy nên nếu đang định ký kết hay khai trương, lùi lại một hai hôm cũng không muộn. "
        "Ngày mai hợp để sắp xếp chỗ nằm hơn là mở đầu chuyện lớn.",
        ["calm bedroom interior morning light", "wooden bed frame detail",
         "quiet vietnamese home interior", "soft daylight through window"],
        "Ngày mai nên làm gì? Trực nguy 21 tháng 8 âm",
    ),
    "2026-10-02": (
        "Ngày mai là một trong số ít ngày hợp khai trương tháng này.",
        "Ngày 22 tháng 8 âm, ngày Kỷ Dậu, lịch cũ ghi là Trực thành. "
        "Danh sách việc hợp gồm nhập học, di chuyển, và khai trương. "
        "Nếu đang chờ ngày mở hàng hay chuyển chỗ, đây là ngày đáng cân nhắc. "
        "Ít ngày hợp khai trương như ngày mai, nên đừng để trôi qua.",
        ["vietnamese shop opening morning", "red ribbon cutting ceremony",
         "small business storefront daylight", "moving boxes new home"],
        "Ngày mai hợp khai trương — Trực thành 22 tháng 8 âm",
    ),
    "2026-10-03": (
        "Ngày mai hợp thu về hơn là cho đi.",
        "Ngày Canh Tuất, lịch cũ ghi Trực thu, và danh sách việc hợp xoay quanh nạp tài với thu tất. "
        "Nói nôm na là ngày để gom lại, kết sổ, đòi nợ cũ hơn là mở rộng. "
        "Một buổi ngồi soát lại giấy tờ cũng đã đúng tinh thần ngày này. "
        "Ngày mai là ngày thu, không phải ngày phát.",
        ["counting money vietnamese", "accounting ledger desk close up",
         "organizing documents folder", "calm office paperwork morning"],
        "Ngày mai hợp thu tiền — Trực thu 23 tháng 8 âm",
    ),
    "2026-10-04": (
        "Ngày mai là ngày hợp để cầu, không phải để làm.",
        "Ngày Tân Hợi, Trực khai, và danh sách việc hợp mở đầu bằng tế tự, cầu phúc, cầu tự. "
        "Sau đó mới tới xuất hành và di chuyển, tức là ngày thiên về khởi sự tinh thần. "
        "Một nén nhang buổi sớm hay một chuyến đi đã định sẵn đều hợp với ngày này. "
        "Ngày mai hợp để mở lòng trước, rồi mới mở việc.",
        ["incense smoke altar close up", "vietnamese family altar morning",
         "open road travel daylight", "temple courtyard quiet"],
        "Ngày mai hợp cầu phúc, xuất hành — Trực khai",
    ),
    "2026-10-05": (
        "Ngày mai là ngày để vá lại, không phải để mở ra.",
        "Ngày Nhâm Tý, lịch cũ ghi Trực bế, và cả danh sách việc hợp chỉ gồm đắp lỗ, sửa tường, trúc đê phòng. "
        "Toàn là việc bịt kín, gia cố, chặn lại những chỗ đang hở. "
        "Nếu nhà có chỗ nào dột hay nứt, ngày mai đúng là lúc để xử lý. "
        "Ngày mai hợp đóng lại hơn là mở ra.",
        ["repairing wall plaster hands", "home renovation tools close up",
         "fixing roof tiles", "cement trowel work detail"],
        "Ngày mai hợp sửa chữa — Trực bế 25 tháng 8 âm",
    ),
    "2026-10-06": (
        "Ngày mai hợp động thổ và nhận việc mới.",
        "Ngày Quý Sửu, Trực kiến, mở đầu chuỗi trực mới trong tháng. "
        "Danh sách việc hợp gồm động thổ, san nền, lên quan nhậm chức và xuất hành. "
        "Nếu có việc phải khởi công hay nhận bàn giao, đây là ngày đáng chọn. "
        "Ngày mai là ngày dựng nền, cả nghĩa đen lẫn nghĩa bóng.",
        ["construction site groundbreaking", "foundation concrete work",
         "new office first day", "sunrise over building site"],
        "Ngày mai hợp động thổ — Trực kiến 26 tháng 8 âm",
    ),
    "2026-10-07": (
        "Ngày mai hợp dọn dẹp và chăm sóc bản thân.",
        "Ngày Giáp Dần, Trực trừ, và danh sách việc hợp nghe rất đời thường. "
        "Giải trừ, tắm gội, cắt tóc, chỉnh tay chân, cầu y trị bệnh, quét dọn nhà cửa. "
        "Một buổi dọn nhà hay một lần đi khám đã lần lữa mãi đều hợp ngày này. "
        "Ngày mai hợp bỏ đi những thứ cũ, từ trong nhà tới trên người.",
        ["cleaning house vietnamese home", "haircut barber close up",
         "decluttering tidy room", "washing hands water close up"],
        "Ngày mai hợp dọn dẹp, cắt tóc — Trực trừ",
    ),
}

created = []
for f in facts_range(date(2026, 10, 1), 7):
    key = f.target.isoformat()
    hook, body, broll, title = SCRIPTS[key]
    b = Bundle(
        channel="FS", kind="short", slug=f.slug,
        script=f"{hook} {body}",
        title=title,
        description=(
            f"Lịch ngày {f.target.strftime('%d/%m/%Y')} — âm lịch {f.lunar_day}/{f.lunar_month}, "
            f"ngày {f.can_chi_day}, {f.truc_name}.\n"
            f"Việc hợp theo lịch cũ: {', '.join(f.truc_good_for)}.\n\n"
            "Nội dung tham khảo theo lịch pháp truyền thống, không phải lời khuyên chắc chắn."
        ),
        tags=["phong thuy", "lich van nien", "ngay tot", "lich am"],
        thumbnail_text="",
        publish_at=f.publish_at,
        voice=VOICE,
        bgm=BGM,
        broll_queries=broll,
        source_note=f"vnlunar {key}: {f.can_chi_day}, {f.truc_name}, tinh {f.star_name}",
    )
    store.save_bundle(b)
    created.append((f, b))

with store.connect() as conn:
    added, total = store.sync_from_disk(conn, channel="FS")

print(f"Tao {len(created)} bundle, hang doi them {added} (tong {total})\n")
for f, b in created:
    print(f"  {f.target}  {b.slug:16s}  {b.word_count:3d} tu  dang {b.publish_at}")
    print(f"      {b.title}")
