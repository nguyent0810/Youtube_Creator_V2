"""Từ điển thuật ngữ lịch — 12 trực, 12 sao. TẬP ĐÓNG, khai một lần.

VÌ SAO FILE NÀY TỒN TẠI: luật "mọi claim ngoài nguồn phải được xác minh"
đúng, nhưng nếu mỗi kịch bản lại phải khai báo tay thì không tự động hoá
được. Với 7 kịch bản thì chịu được; với 465 short thì không.

Lối thoát nằm ở chỗ: vốn từ của nội dung Lịch là TẬP ĐÓNG. Đúng 12 trực và
đúng 12 sao, không bao giờ có cái thứ 13. Khai đủ 24 mục ở đây là phủ được
MỌI kịch bản Lịch về sau -- người không phải can thiệp lần nào nữa.

Nên đây không phải nới lỏng luật. Đây là làm cho luật TỰ THOẢ MÃN ĐƯỢC.

NGUYÊN TẮC VIẾT CHÚ GIẢI:
  - Chỉ dịch nghĩa TÊN (chữ Hán), không phán về hiệu lực của ngày.
  - Mỗi mục phải đối chiếu được với danh mục good_for thật trong vnlunar.
    Nếu nghĩa chữ không khớp danh mục thì ghi rõ là không khớp, đừng uốn.
  - Không có mục nào nói "sao này tốt hơn sao kia" -- nguồn không có
    thông tin đó, và đó đúng là dạng suy diễn đã từng lọt qua.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    name: str        # đúng tên vnlunar trả về
    han: str         # chữ Hán
    gloss: str       # nghĩa chữ, dùng được trong lời đọc
    basis: str       # căn cứ + đối chiếu với danh mục thật


# ─── 12 TRỰC ──────────────────────────────────────────────────────────────

TRUC: dict[str, Term] = {t.name: t for t in (
    Term("Trực kiến", "建", "dựng lên",
         "建 nghĩa là dựng/lập. Danh mục thật: động thổ, san nền, lên quan "
         "nhậm chức — đều là việc khởi dựng. Khớp."),
    Term("Trực trừ", "除", "bỏ bớt đi",
         "除 nghĩa là trừ bỏ/dọn đi. Danh mục thật: giải trừ, tắm gội, cạo "
         "đầu, quét dọn nhà cửa — đều là việc loại bỏ. Khớp."),
    Term("Trực mãn", "滿", "đầy",
         "滿 nghĩa là đầy/tròn. Danh mục thật rộng nhất trong 12 trực (10 "
         "việc: khai trương, nạp tài, mở kho, may cắt...). Khớp nghĩa 'đầy'."),
    Term("Trực bình", "平", "san bằng",
         "平 nghĩa là bằng phẳng. Danh mục thật chỉ 2 việc, đều là san sửa: "
         "tu sửa tường, bình trị đạo đồ. Khớp."),
    Term("Trực định", "定", "cố định lại",
         "定 nghĩa là định/yên. Danh mục thật chỉ 1 việc: quan đái (đội mũ "
         "đeo đai, tức lễ định danh phận). Khớp nghĩa 'định'."),
    Term("Trực chấp", "執", "nắm giữ",
         "執 nghĩa là cầm/giữ. Danh mục thật chỉ 1 việc: bắt bớ. Khớp."),
    Term("Trực phá", "破", "phá bỏ",
         "破 nghĩa là vỡ/phá. Danh mục thật chỉ 1 việc: cầu y trị bệnh — "
         "hiểu theo nghĩa phá bệnh. Chỉ dùng chú giải này kèm danh mục thật, "
         "không suy rộng ra là 'ngày xấu'."),
    Term("Trực nguy", "危", "chông chênh",
         "危 nghĩa là cao/nguy. Danh mục thật hẹp, 3 việc quanh chỗ nằm và "
         "biên cảnh. Chú giải dừng ở nghĩa chữ; nguồn KHÔNG nói ngày này xấu."),
    Term("Trực thành", "成", "nên việc",
         "成 nghĩa là nên/xong. Danh mục thật: nhập học, khai trương, di "
         "chuyển — đều là việc khởi sự. Khớp."),
    Term("Trực thu", "收", "gom về",
         "收 nghĩa là thu vào. Danh mục thật: nạp tài, thu tất, tiến người "
         "— đều là việc thu. Khớp."),
    Term("Trực khai", "開", "mở ra",
         "開 nghĩa là mở. Danh mục thật 7 việc: tế tự, cầu phúc, xuất hành, "
         "lên quan lâm chính. Khớp."),
    Term("Trực bế", "閉", "bịt lại",
         "閉 nghĩa là đóng/khép. Danh mục thật: trúc đê phòng, đắp lỗ, sửa "
         "tường — đều là việc bịt kín. Khớp."),
)}


# ─── 12 SAO ───────────────────────────────────────────────────────────────
#
# CHÚ Ý: chú giải sao CHỈ dịch nghĩa tên. vnlunar không cung cấp gì ngoài
# nhãn hoàng đạo/hắc đạo, nên mọi câu kiểu "sao này chủ về tiền bạc" đều là
# suy diễn và KHÔNG có ở đây.

SAO: dict[str, Term] = {t.name: t for t in (
    Term("Thanh Long", "青龍", "rồng xanh", "Tên gọi. Nhóm hoàng đạo theo vnlunar."),
    Term("Minh Đường", "明堂", "nhà sáng", "Tên gọi. Nhóm hoàng đạo theo vnlunar."),
    Term("Kim Quỹ", "金匱", "hòm vàng", "Tên gọi. Nhóm hoàng đạo theo vnlunar."),
    Term("Ngọc Đường", "玉堂", "nhà ngọc", "Tên gọi. Nhóm hoàng đạo theo vnlunar."),
    Term("Thiên Đức", "天德", "đức trời", "Tên gọi. Nhóm hoàng đạo theo vnlunar."),
    Term("Tư Mệnh", "司命", "coi mệnh", "Tên gọi. Nhóm hoàng đạo theo vnlunar."),
    Term("Bạch Hổ", "白虎", "hổ trắng", "Tên gọi. Nhóm hắc đạo theo vnlunar."),
    Term("Chu Tước", "朱雀", "chim sẻ đỏ", "Tên gọi. Nhóm hắc đạo theo vnlunar."),
    Term("Câu Trần", "勾陳", "móc giữ", "Tên gọi. Nhóm hắc đạo theo vnlunar."),
    Term("Huyền Vũ", "玄武", "rùa đen", "Tên gọi. Nhóm hắc đạo theo vnlunar."),
    Term("Thiên Hình", "天刑", "hình phạt trời", "Tên gọi. Nhóm hắc đạo theo vnlunar."),
    Term("Thiên Lao", "天牢", "ngục trời", "Tên gọi. Nhóm hắc đạo theo vnlunar."),
)}

assert len(TRUC) == 12 and len(SAO) == 12, "tập đóng: phải đúng 12 và 12"


def gloss_phrases() -> tuple[str, ...]:
    """Mọi cụm chú giải hợp lệ, để bộ kiểm claim nhận là đã khai báo."""
    out = []
    for t in TRUC.values():
        out += [f"{t.name.lower()} nghĩa là {t.gloss}",
                f"chữ {t.name.split()[-1].lower()} nghĩa là {t.gloss}",
                f"trực của chuyện {t.gloss}"]
    for s in SAO.values():
        out += [f"{s.name.lower()} nghĩa là {s.gloss}",
                f"tên nghĩa là {s.gloss}"]
    return tuple(out)
