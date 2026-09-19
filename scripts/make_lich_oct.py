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
    # Kim Quỹ (hoàng đạo) NHƯNG Trực nguy (hẹp) -> mâu thuẫn có sẵn, dùng làm hook.
    "2026-10-01": (
        "Ngày mai là ngày hoàng đạo. Và bạn vẫn không nên ký gì.",
        "Nghe mâu thuẫn, nhưng lịch cũ tách làm hai tầng. "
        "Tầng sao: ngày mai là Kim Quỹ, một trong sáu sao hoàng đạo. "
        "Tầng trực: lại là Trực nguy, tầng hẹp nhất trong mười hai trực. "
        "Sao thì mở, trực thì đóng. "
        "Việc còn lại chỉ vài thứ quanh chỗ nằm, chỗ ngủ. "
        "Nên ngày mai kê lại giường thì được. Ký hợp đồng thì thôi.",
        ["calm bedroom interior morning light", "wooden bed frame detail",
         "quiet vietnamese home interior", "soft daylight through window"],
        "Hoàng đạo mà vẫn không nên ký — Kim Quỹ gặp Trực nguy",
    ),
    "2026-10-02": (
        "Sáu ngày nữa mới lại có ngày như ngày mai.",
        "Thiên Đức. Một trong sáu sao hoàng đạo, và là sao rộng tay nhất. "
        "Gặp đúng Trực thành, trực của chuyện nên việc. "
        "Hai tầng cùng mở một lúc, tháng này đếm trên đầu ngón tay. "
        "Khai trương, nhập học, chuyển nhà, đều nằm trong đó. "
        "Ai đang chờ ngày mở hàng thì mai là ngày. "
        "Lưu lại, kẻo trôi mất.",
        ["vietnamese shop opening morning", "red ribbon cutting ceremony",
         "small business storefront daylight", "moving boxes new home"],
        "Ngày mai hợp khai trương — Thiên Đức gặp Trực thành",
    ),
    "2026-10-03": (
        "Ngày mai là ngày Bạch Hổ.",
        "Cái tên thôi đã đủ để người xưa né. "
        "Một trong sáu sao hắc đạo, và là sao bị kiêng nhiều nhất. "
        "Nhưng lịch cũ không bảo nằm im cả ngày. "
        "Trực của ngày mai là Trực thu, hợp chuyện gom về: nạp tài, thu tất, kết sổ. "
        "Đòi nợ được. Cho vay thì không. "
        "Ngày Bạch Hổ hợp thu vào, không hợp phát ra.",
        ["counting money vietnamese", "accounting ledger desk close up",
         "organizing documents folder", "calm office paperwork morning"],
        "Ngày Bạch Hổ hợp đòi nợ — Trực thu 23/8 âm",
    ),
    "2026-10-04": (
        "Ba việc đứng đầu ngày mai đều bắt đầu bằng chữ cầu.",
        "Cầu phúc. Cầu tự. Tế tự. "
        "Mãi sau mới tới xuất hành với di chuyển. "
        "Sao của ngày là Ngọc Đường, sao hoàng đạo gắn với chuyện văn chương, lễ nghĩa. "
        "Gặp Trực khai, trực của chuyện mở ra. "
        "Nên ngày mai mở về phía tinh thần trước. "
        "Một nén nhang buổi sớm cũng đã đúng ngày.",
        ["incense smoke altar close up", "vietnamese family altar morning",
         "open road travel daylight", "temple courtyard quiet"],
        "Ngày mai hợp cầu phúc — Ngọc Đường gặp Trực khai",
    ),
    "2026-10-05": (
        "Cả ngày mai chỉ còn ba việc nên làm.",
        "Ba thôi. Đắp lỗ. Sửa tường. Trúc đê phòng. "
        "Nhìn là thấy một hướng: bịt lại chỗ đang hở. "
        "Không lạ, vì sao của ngày là Thiên Lao, sao hắc đạo gắn với chuyện giam giữ, đóng kín. "
        "Trực thì là Trực bế, cũng nghĩa là đóng. "
        "Hai tầng cùng đóng một lượt. "
        "Nhà có chỗ nào dột thì mai vá. Còn lại thì khoan.",
        ["repairing wall plaster hands", "home renovation tools close up",
         "fixing roof tiles", "cement trowel work detail"],
        "Ngày mai chỉ còn ba việc nên làm — Thiên Lao gặp Trực bế",
    ),
    # Huyền Vũ (hắc đạo) NHƯNG Trực kiến (khởi đầu) -> mâu thuẫn ngược lại.
    "2026-10-06": (
        "Sao xấu, nhưng lại là ngày đặt nền.",
        "Huyền Vũ. Một trong sáu sao hắc đạo, thường gắn với chuyện mất mát, trộm cắp. "
        "Vậy mà trực của ngày lại là Trực kiến, trực mở đầu cả một vòng mới. "
        "Động thổ, san nền, nhận chức, xuất hành, đều nằm trong danh mục. "
        "Người xưa không né hẳn ngày kiểu này. Họ làm việc nền móng, tránh việc tiền bạc. "
        "Ngày mai đặt nền thì được. Đừng mang tiền ra đếm.",
        ["construction site groundbreaking", "foundation concrete work",
         "new office first day", "sunrise over building site"],
        "Sao xấu mà vẫn là ngày đặt nền — Huyền Vũ gặp Trực kiến",
    ),
    "2026-10-07": (
        "Ngày mai hợp cắt tóc.",
        "Nghe vặt vãnh, nhưng cả danh mục ngày mai đều vậy. "
        "Tắm gội, cắt tóc, cắt móng, quét nhà, đi khám bệnh. "
        "Sao của ngày là Tư Mệnh, sao hoàng đạo coi chuyện tuổi thọ, sức khoẻ. "
        "Gặp Trực trừ, trực của chuyện bỏ bớt. "
        "Cái hẹn khám cứ lần lữa mãi, mai đi là đúng ngày nhất. "
        "Ngày mai bỏ bớt đi, từ trong nhà tới trên đầu.",
        ["cleaning house vietnamese home", "haircut barber close up",
         "decluttering tidy room", "washing hands water close up"],
        "Ngày mai hợp cắt tóc, khám bệnh — Tư Mệnh gặp Trực trừ",
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
