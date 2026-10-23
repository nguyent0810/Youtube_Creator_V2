# Short bảng tra: 8 giao diện (22/10/2026)

Chủ kênh: nội dung ổn, trình bày một màu. Mỗi kênh có 4 giao diện bảng tra dừng hình; mỗi bài chọn một, không trùng bài liền trước cùng kênh.

Khuôn chung: một cảnh `table`, bảng nằm trong vùng an toàn x 40–940 (rộng 860–900 px, nút Shorts che x > 940), vùng dọc y 240–1410 (phụ đề từ 1478), chữ >= 36 px, số >= 64 px, khung cuối đứng yên >= 3 s (mọi chuyển động nền dừng trước t1-3 s). Số liệu, lời đọc, nguồn giữ nguyên.

| Khoá | Kênh | Mô tả | Màu | Font | Hiệu ứng hiện / tra | Tiêu đề đặt ở | Dùng khi |
|---|---|---|---|---|---|---|---|
| mim-crt | MIM | Terminal CRT, scanline, thanh quét | đen, xanh lá phosphor #62ff8e, viền cyan | VT323 | tiêu đề gõ từng chữ, hàng "in" bằng con trỏ, ô đảo màu, thanh quét xuống | dòng lệnh `>` trên cùng | tra theo mốc/năm, truy vấn ("hỏi máy") |
| mim-blueprint | MIM | Bản vẽ kỹ thuật kẻ lưới | xanh đậm #0b3a8f, nét trắng, khoanh cyan | Chakra Petch | nét vẽ dần, khoanh cyan vẽ quanh ô | khung tên ở DƯỚI bảng; colHead là đường kích thước | số đo, thông số, cấu trúc |
| mim-thermal | MIM | Biên lai máy in nhiệt | kem #f6f1df, chữ đen, khe in cyan | Space Mono | giấy ra từ khe, từng dòng in, thanh đen quét lên ô | đầu biên lai, giữa | điểm số, phiếu kết quả, so sánh |
| mim-heat | MIM | Bảng nhiệt neon | nền xanh than, ô lạnh→nóng (tím-xanh-lục-vàng-hồng) | Lexend | sóng chéo ô ấm dần, ô sáng viền trắng, chú giải | giữa trên, phát sáng cyan | số liệu cần thấy cao/thấp ngay |
| ck-led | CK | Bảng điện tử LED | đen, hổ phách #ffb000 | Barlow Condensed | hàng lật cơ khí, số đếm lên, ô nháy trắng-nóng, dải chạy dưới | khung viền hổ phách trên cùng | số lớn, mốc thời gian, tích luỹ |
| ck-ledger | CK | Sổ kế toán kem | kem, mực xanh, vàng highlight, bàn than | Roboto Slab + Patrick Hand | hàng viết tay, bút highlight vàng quét, tem vàng dưới | đầu trang, gạch đôi vàng | ngân sách, chia tiền, chi tiêu |
| ck-graph | CK | Giấy kẻ ô đồ thị, nến mờ, thước | xanh đêm, lưới vàng | Oswald | hàng trượt vào, kính lúp vàng chạy giữa các ô | trái, vạch vàng đứng | thị trường, lãi suất, đồ thị |
| ck-bars | CK | Ô có thanh nhiệt kế mini | than, vàng #fbbf24, chip tròn | Be Vietnam Pro 900 | thanh đầy dần + số đếm, ô sáng vàng | trái, hai dòng, dòng 2 vàng gạch chân | trần/mức so sánh giữa các ô |

Chung cho mọi bảng: kicker "BẢNG TRA" cyan (MIM) hoặc vàng (CK) ở góc trái trên; MIM có nhãn kênh trong khung (blueprint, thermal).

## Gán 6 bài đã dựng
mim-bang-nghe-ai: mim-heat · mim-bang-sinh-nam: mim-crt · mim-bang-gpt4-thi: mim-thermal · ck-bang-chia-luong-50-30-20: ck-ledger · ck-bang-de-danh-den-2030: ck-led · ck-bang-tran-thue-nha: ck-bars. Còn nhàn rỗi: mim-blueprint, ck-graph (dùng cho bài kế tiếp).

## Quy tắc xoay
1. Sổ `data/stier/bang_tra_looks.json` (picks theo thứ tự). `python motion/stier/bang_tra_look.py next MIM|CK` chọn look ít dùng nhất, khác bài liền trước; `apply <slug> [look]` ghi spec (`profile`, `look`, `cls`, `extra_css`) và sổ; `check` báo trùng liền kề.
2. Không dùng cùng look hai bài liền nhau của một kênh; trong 4 bài liên tiếp nên đủ 4 look khác nhau. Nội dung có thể ép look (`apply <slug> <look>`) nếu hợp hơn, nhưng vẫn không trùng liền trước.
3. Thêm look mới: viết hàm `L["khoá"]` trong `bang-tra-looks.js`, CSS scoped `.btl-khoá` trong `bang-tra-looks.css`, thêm vào `looks` của sổ.

## Kỹ thuật
- File mới: `motion/hf/assets/engine/bang-tra-looks.js` (thay `B.table` qua bridge `window.HFS.mount`, chỉ khi `#root` có class `btl-<khoá>`) và `bang-tra-looks.css`. Không sửa casefile.js/css, theme-*, build.py. Tất định, không Math.random/Date/fetch; số đếm và gõ chữ dùng `tl.set` (không onUpdate).
- Giữ `rows[].at` và `hl[].at` để `sfx.py` khớp tiếng.
- Tạm: build.py chỉ có `extra_css` nên spec.extra_css nối thêm thẻ `<script>` (chuỗi trong `bang_tra_look.py`). Đề xuất 2 dòng trong build.py: `spec["extra_js"]` -> `<script src="assets/engine/{extra_js}"></script>` cạnh extra_css; khi đó bỏ chuỗi nối.
- Tạm: màn che `#scrims` dời xuống (CSS scoped) để không làm tối đáy bảng.
