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
    # Kim Quỹ (hoàng đạo) + Trực nguy (3 việc) -> sao mở, trực siết.
    "2026-10-01": (
        "Ngày mai là ngày hoàng đạo, nhưng lịch chỉ cho làm đúng ba việc.",
        "Sao là Kim Quỹ, thường được xếp vào nhóm hoàng đạo. "
        "Trực lại là Trực nguy. Sao mở, trực siết. "
        "Danh mục vỏn vẹn ba việc: an phủ biên cảnh, tuyển tướng, an sàng. "
        "An sàng là kê giường, sắp chỗ nằm. Việc đó thì thuận. "
        "Ngoài ra, lịch ghi gọn là mọi việc khác. "
        "Hoàng đạo không có nghĩa là muốn làm gì cũng được.",
        ["calm bedroom interior morning light", "wooden bed frame detail",
         "quiet vietnamese home interior", "soft daylight through window"],
        "Hoàng đạo mà chỉ được làm ba việc — Kim Quỹ gặp Trực nguy",
    ),
    # Trực thành rơi vào 02, 18, 30 tháng 10 -> "ba ngày" là con số ĐÃ ĐẾM.
    "2026-10-02": (
        "Cả tháng Mười chỉ có ba ngày Trực thành, và ngày mai là ngày đầu.",
        "Sao là Thiên Đức, thuộc nhóm hoàng đạo. "
        "Trực là Trực thành, trực của chuyện nên việc. "
        "Lần này sao và trực cùng một hướng. "
        "Danh mục gồm nhập học, di chuyển, khai trương, trúc đê phòng. "
        "Ai đang chờ ngày mở hàng hay chuyển nhà, đây là ngày có thể cân nhắc. "
        "Ngoài danh mục, lịch vẫn xếp là mọi việc khác. "
        "Ba ngày trong cả tháng.",
        ["vietnamese shop opening morning", "red ribbon cutting ceremony",
         "small business storefront daylight", "moving boxes new home"],
        "Cả tháng chỉ ba ngày như ngày mai — Thiên Đức gặp Trực thành",
    ),
    # Bạch Hổ (hắc đạo) NHƯNG bad_for chỉ 2 việc, không phải "mọi việc khác".
    "2026-10-03": (
        "Ngày mai là ngày Bạch Hổ, nhưng lịch chỉ kiêng đúng hai việc.",
        "Bạch Hổ thuộc nhóm sáu sao hắc đạo. "
        "Trực là Trực thu, thiên về chuyện gom về. "
        "Danh mục nên làm: tiến người, nạp tài, bắt bớ, thu tất. "
        "Phần kiêng thì rất hẹp, chỉ cầu phúc cầu tự và lên sách lên chương biểu. "
        "Nên thu tiền, kết sổ thì thuận. Còn đi lễ cầu cúng thì nên lùi. "
        "Sao dữ, mà cửa vẫn mở về một phía.",
        ["counting money vietnamese", "accounting ledger desk close up",
         "organizing documents folder", "calm office paperwork morning"],
        "Ngày Bạch Hổ chỉ kiêng hai việc — Trực thu 23/8 âm",
    ),
    # Nghịch lý VỚI 03/10: việc hôm đó kiêng thì hôm nay đứng đầu danh mục.
    "2026-10-04": (
        "Việc mà lịch vừa kiêng hôm trước, ngày mai lại đứng đầu danh mục.",
        "Sao là Ngọc Đường, thuộc nhóm hoàng đạo. "
        "Trực là Trực khai, trực của chuyện mở ra. "
        "Bảy việc nên làm, mở đầu là tế tự, cầu phúc, cầu tự. "
        "Đúng nhóm việc mà hôm trước lịch còn xếp vào phần kiêng. "
        "Sau đó mới tới xuất hành, di chuyển, lên quan lâm chính. "
        "Ngoài ra, lịch vẫn ghi mọi việc khác. "
        "Cùng việc ấy, lịch đổi ý theo ngày.",
        ["incense smoke altar close up", "vietnamese family altar morning",
         "open road travel daylight", "temple courtyard quiet"],
        "Việc hôm trước kiêng, mai lại đứng đầu — Ngọc Đường gặp Trực khai",
    ),
    # Thiên Lao + Trực bế -- hai tầng cùng nghĩa đóng.
    "2026-10-05": (
        "Ngày mai sao và trực cùng nói một chữ, mà chữ ấy là đóng.",
        "Sao là Thiên Lao, thuộc nhóm hắc đạo. Chữ lao nghĩa là nhà giam. "
        "Trực là Trực bế, chữ bế nghĩa là bịt lại. "
        "Danh mục cũng đúng một hướng: trúc đê phòng, đắp lỗ, sửa tường. "
        "Nhà có chỗ nào dột, chỗ nào nứt thì đây là ngày hợp. "
        "Còn xuất hành, khai trương thì lịch ghi thẳng là kiêng. "
        "Ngày mai để vá lại, không phải để mở ra.",
        ["repairing wall plaster hands", "home renovation tools close up",
         "fixing roof tiles", "cement trowel work detail"],
        "Sao và trực cùng nói một chữ đóng — Thiên Lao gặp Trực bế",
    ),
    # NGUỒN TỰ PHÂN BIỆT: good_for có "khai trương tàu thuyền" + "khởi công
    # làm lò"; bad_for có "Khai trương" + "khởi công xây cất". Có thật.
    "2026-10-06": (
        "Lịch ngày mai vừa cho khai trương, vừa kiêng khai trương.",
        "Sao là Huyền Vũ, thuộc nhóm hắc đạo. Trực là Trực kiến. "
        "Phần nên làm ghi: động thổ, san nền, khai trương tàu thuyền, khởi công làm lò. "
        "Phần kiêng lại ghi: khai trương, khởi công xây cất. "
        "Nguồn phân biệt rất hẹp. "
        "Cho mở lò, mở thuyền, chứ không cho mở hàng. "
        "Nên động thổ thì thuận, mở cửa hàng thì nên lùi. "
        "Cùng chữ khai trương, khác ở chỗ khai cái gì.",
        ["construction site groundbreaking", "foundation concrete work",
         "new office first day", "sunrise over building site"],
        "Vừa cho vừa kiêng khai trương — Huyền Vũ gặp Trực kiến",
    ),
    # Cả 7 việc đều là thân thể/nhà cửa, không việc nào về tiền -- đếm được.
    "2026-10-07": (
        "Cả bảy việc lịch cho làm ngày mai đều không dính tới tiền.",
        "Sao là Tư Mệnh, thuộc nhóm hoàng đạo. "
        "Trực là Trực trừ. Chữ trừ nghĩa là bỏ bớt. "
        "Danh mục gồm giải trừ, tắm gội, chỉnh dung, cạo đầu, "
        "chỉnh tay chân móng, cầu y trị bệnh, quét dọn nhà cửa. "
        "Toàn chuyện thân thể và nhà cửa. "
        "Cái hẹn khám cứ lần lữa mãi, đây là ngày hợp. "
        "Ngày hoàng đạo, nhưng để chăm mình chứ không để kiếm tiền.",
        ["cleaning house vietnamese home", "haircut barber close up",
         "decluttering tidy room", "washing hands water close up"],
        "Bảy việc, không việc nào dính tiền — Tư Mệnh gặp Trực trừ",
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
