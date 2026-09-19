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
        "Ngày mai đừng ký gì cả.",
        "Nghe hơi quá, nhưng có lý do. "
        "Lịch cũ gọi ngày mai là Trực nguy. Nguy ở đây không phải nguy hiểm. "
        "Nó là ngày mà danh mục việc nên làm hẹp lại gần hết. "
        "Cả ngày chỉ còn đúng mấy việc: kê lại giường, sắp lại chỗ nằm. "
        "Vậy thôi. "
        "Nên nếu đang định ký hợp đồng hay mở hàng, lùi một hôm. "
        "Ngày mai để dọn chỗ ngủ, không phải để ký.",
        ["calm bedroom interior morning light", "wooden bed frame detail",
         "quiet vietnamese home interior", "soft daylight through window"],
        "Ngày mai đừng ký gì cả — Trực nguy 21/8 âm",
    ),
    "2026-10-02": (
        "Tháng này chỉ có vài ngày hợp khai trương.",
        "Và ngày mai là một trong số đó. "
        "Lịch cũ gọi ngày mai là Trực thành. Thành, tức là nên việc. "
        "Không phải ngày nào cũng được vậy đâu. "
        "Có ngày lịch chỉ cho đúng một hai việc hẹp. "
        "Ngày mai thì mở: khai trương, nhập học, chuyển nhà, đều nằm trong đó. "
        "Ai đang chờ ngày mở hàng thì mai là ngày. "
        "Lưu lại đi, tháng này không còn nhiều ngày như vậy.",
        ["vietnamese shop opening morning", "red ribbon cutting ceremony",
         "small business storefront daylight", "moving boxes new home"],
        "Ngày mai hợp khai trương — Trực thành 22/8 âm",
    ),
    "2026-10-03": (
        "Ngày mai hợp đòi nợ.",
        "Nói vậy cho dễ nhớ, nhưng đúng tinh thần. "
        "Lịch cũ gọi ngày mai là Trực thu. Thu, là gom về. "
        "Việc hợp ngày này toàn nằm một phía: nạp tài, thu tất, kết sổ. "
        "Không có việc nào là mở rộng hay cho đi. "
        "Nên ngày mai đừng đầu tư, đừng ứng tiền trước. "
        "Ngồi soát lại giấy tờ, gọi mấy cuộc còn nợ. "
        "Ngày mai là ngày thu về, không phải ngày phát ra.",
        ["counting money vietnamese", "accounting ledger desk close up",
         "organizing documents folder", "calm office paperwork morning"],
        "Ngày mai hợp thu tiền, đòi nợ — Trực thu",
    ),
    "2026-10-04": (
        "Ngày mai hợp cầu hơn hợp làm.",
        "Hơi lạ, nhưng nhìn danh mục thì rõ. "
        "Lịch cũ gọi ngày mai là Trực khai. Và ba việc đứng đầu đều là cầu: "
        "cầu phúc, cầu tự, tế tự. "
        "Mãi sau mới tới xuất hành với di chuyển. "
        "Tức là ngày này mở về phía tinh thần trước, rồi mới tới phía công việc. "
        "Một nén nhang buổi sớm. Một chuyến đi đã hẹn từ lâu. "
        "Ngày mai mở lòng trước đã, việc tính sau.",
        ["incense smoke altar close up", "vietnamese family altar morning",
         "open road travel daylight", "temple courtyard quiet"],
        "Ngày mai hợp cầu phúc, xuất hành — Trực khai",
    ),
    "2026-10-05": (
        "Cả ngày mai chỉ có ba việc nên làm.",
        "Ba thôi. Và cả ba đều giống nhau một điểm. "
        "Đắp lỗ. Sửa tường. Trúc đê phòng. "
        "Toàn là bịt lại, vá lại, chặn lại chỗ đang hở. "
        "Lịch cũ gọi ngày này là Trực bế, tức là đóng. "
        "Nhà có chỗ nào dột, chỗ nào nứt, mai xử lý là hợp nhất. "
        "Ngày mai để vá lại, đừng mở ra thêm gì.",
        ["repairing wall plaster hands", "home renovation tools close up",
         "fixing roof tiles", "cement trowel work detail"],
        "Cả ngày mai chỉ có ba việc nên làm — Trực bế",
    ),
    "2026-10-06": (
        "Ngày mai là ngày đặt nền.",
        "Cả nghĩa đen lẫn nghĩa bóng. "
        "Lịch cũ gọi là Trực kiến, trực mở đầu một vòng mới trong tháng. "
        "Việc hợp cũng đúng kiểu bắt đầu: động thổ, san nền, nhận chức, xuất hành. "
        "Ai sắp khởi công hay sắp nhận bàn giao thì để ý ngày này. "
        "Còn chưa có gì để khởi công? "
        "Thì bắt đầu một thói quen cũng được. Ngày đặt nền nào cũng vậy cả.",
        ["construction site groundbreaking", "foundation concrete work",
         "new office first day", "sunrise over building site"],
        "Ngày mai là ngày đặt nền — Trực kiến 26/8 âm",
    ),
    "2026-10-07": (
        "Ngày mai hợp cắt tóc.",
        "Và danh mục việc hợp ngày mai nghe rất đời. "
        "Tắm gội, cắt tóc, cắt móng, quét dọn nhà cửa, đi khám bệnh. "
        "Không có việc nào to tát cả. "
        "Lịch cũ gọi ngày này là Trực trừ. Trừ, là bỏ bớt đi. "
        "Cái hẹn khám cứ lần lữa mãi, mai đi là hợp. "
        "Ngày mai bỏ bớt đi, từ trong nhà tới trên đầu.",
        ["cleaning house vietnamese home", "haircut barber close up",
         "decluttering tidy room", "washing hands water close up"],
        "Ngày mai hợp cắt tóc, dọn nhà — Trực trừ",
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
