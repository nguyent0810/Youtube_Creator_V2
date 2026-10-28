# Danh sách duyệt: sửa bao bì Long sắp lên + dừng Short nhóm thua — 26/10/2026

Quyết định của chủ kênh (26/10): **giữ 4 Long/tuần**, chỉ sửa tiêu đề và thumbnail của các Long sắp lên, và dừng Short thuộc nhóm chủ đề thua.

Nguồn: [2026-10-26-phan-tich-thang-thua-3-kenh.md](2026-10-26-phan-tich-thang-thua-3-kenh.md).

**Nguyên tắc sửa** (rút từ số liệu, không chép khuôn):
- **MIM:** đưa người và năm lên đầu tiêu đề. Bài "AI Đã Chết Hai Lần" có CTR 4,2%; các tiêu đề chỉ hỏi chung chung có CTR 0,8–1,8%.
- **CK:** dùng dạng "một khoản tiền × một mốc thời gian". Short thắng của CK đều theo dạng này.
- **Cả hai:** tiêu đề ≤ 60 ký tự. Mọi con số phải có trong script. CK không nêu tên ngân hàng và không khuyên mua hay bán.

**Cách làm sau khi duyệt:**
- Sửa tiêu đề qua API: `Channel.edit` trên video private đã hẹn giờ, giờ đăng giữ nguyên.
- Đồng bộ `spec.json` và `upload_log` để lần đăng lại không báo DuplicateTitle.
- Không đụng nội dung video.

## A. Long MIM (16 bài)

| Lên | Tiêu đề hiện tại (ký tự) | Đề xuất | Ghi chú |
|---|---|---|---|
| **26/10 tối nay** | Vì Sao AI Bịa Mà Vẫn Rất Tự Tin? Sáu Vụ Án Không Hề Có Thật (59) | **Luật Sư Nộp 6 Vụ Án Do ChatGPT Bịa: Vì Sao AI Tự Tin?** (53) | Vụ Avianca 2023 có trong script |
| 28/10 | Vì Sao Bàn Phím Không Xếp Theo A B C? Ba Lời Buộc Tội Với QWERTY (64) | **Sholes, 1873: Vì Sao Bàn Phím Không Xếp A B C?** (45) | Sholes có trong script; năm 1873 có trên thumbnail |
| 30/10 | Thuật Toán Đề Xuất: Vì Sao TikTok Và YouTube Biết Bạn Thích Gì? (63) | Giữ tiêu đề | **Thumbnail lỗi:** chữ bị cắt ("CHƯA BẤM Đ…", "VẪN BIẾ…"). Dựng lại t1 |
| 01/11 | Deep Blue Đấu Kasparov: Mười Chín Nước Cờ Khiến Nhà Vô Địch Thế Giới Bỏ Đi (74) | **Deep Blue Đấu Kasparov 1997: 19 Nước Cờ Khiến Nhà Vô Địch Bỏ Đi** (63) | Chỉ rút gọn |
| 02/11 | GPU: Con Chip Chơi Game Đã Trở Thành Trái Tim Của AI Như Thế Nào? (65) | **AlexNet 2012: Card Chơi Game Đã Thành Trái Tim Của AI** (52) | AlexNet và GTX 580 có trong script |
| 04/11 | Watson Thắng Jeopardy!: Cỗ Máy Trả Lời "Toronto" Và Bài Học Về Độ Tự Tin (72) | **Watson Thắng Jeopardy! 2011: Cỗ Máy Trả Lời "Toronto?????"** (57) | |
| 06/11 | AI Có Học Từ Cuộc Trò Chuyện Của Bạn Không? Chuyện Gì Xảy Ra Với Những Gì Bạn Gõ Vào Chatbot (92) | **Bạn Gõ Gì Vào Chatbot, Ai Được Đọc? AI Có Học Từ Đó?** (52) | Chỉ rút gọn. Bài này đã có đính chính trong mô tả |
| 08/11 | Máy Thắng Poker: Cỗ Máy Học Cách Tố Bịp, Và Ba Lá Bài Úp (56) | **Libratus 2017: Cỗ Máy Học Tố Bịp, Thắng 4 Cao Thủ Poker** (55) | Libratus 01/2017 có trong script |
| 09/11 | Khuôn Mặt Bạn Biến Thành 128 Con Số: AI Nhận Ra Bạn Thế Nào? (60) | Giữ | Đã có con số làm mỏ neo |
| 11/11 | Máy Thắng Game Thời Gian Thực: AlphaStar, OpenAI Five Và Năm Điều Cờ Vua Không Có (81) | **AlphaStar, OpenAI Five: Khi Máy Thắng Cả Game Thời Gian Thực** (60) | Chỉ rút gọn |
| 13/11 | Dịch Máy: Lời Hứa "Vài Năm Nữa" Từ Năm 1954 Tới Google Dịch (59) | Giữ | Đã có năm |
| 15/11 | Mã 1202: Chiếc Máy Tính Báo Động Năm Lần Khi Eagle Hạ Cánh Xuống Mặt Trăng (74) | **Apollo 11, Mã 1202: Máy Tính Báo Động 5 Lần Khi Hạ Cánh** (54) | Chỉ rút gọn |
| 16–22/11 | 4 bài "Ngoài Đời Thật" (Feynman, KAL 007, Petrov, Siri) | Giữ | Đã rút gọn ngày 23/10 |

## B. Long CK (13 bài)

| Lên | Tiêu đề hiện tại (ký tự) | Đề xuất | Ghi chú |
|---|---|---|---|
| **26/10 tối nay** | Vì Sao Có Ngày Muốn Bán Cổ Phiếu Mà Không Bán Được? Một Phiên HOSE Từ 9 Giờ Tới 15 Giờ (86) | **Ngày VN-Index Mất 115 Điểm: Vì Sao Muốn Bán Mà Không Bán Được?** (62) | "115 điểm" có trong script |
| 28/10 | Quỹ Khẩn Cấp: Cần Bao Nhiêu, Mất Bao Lâu, Để Ở Đâu? Tờ Phiếu Ba Ô Trống (71) | **Hoá Đơn Viện 15 Triệu: Quỹ Khẩn Cấp Cần Bao Nhiêu?** (50) | 15 triệu có trên thumbnail và trong Short e2 |
| 30/10 | Hai Căn Hộ Giống Hệt Nhau, Một Mua Một Thuê: 10 Năm Sau Ai Khá Hơn? (67) | **Trả Góp 19 Triệu Hay Thuê 6 Triệu: 10 Năm Sau Ai Khá Hơn?** (57) | Số có trên thumbnail, là ví dụ giả định |
| 01/11 | Mua Xe 700 Triệu: Mỗi Tháng Thật Sự Tốn Bao Nhiêu? Trả Thẳng, Trả Góp Hay Chưa Mua (82) | **Mua Xe 700 Triệu: Mỗi Tháng Thật Sự Tốn Bao Nhiêu?** (49) | Chỉ rút gọn |
| 02/11 | Biểu Đồ Nến Cho Người Mới: Một Cây Nến Kể Gì Về Một Phiên, Và Điều Nó Không Nói Được (84) | **Một Cây Nến Đỏ Kể Gì? Biểu Đồ Nến Cho Người Mới** (46) | Chỉ rút gọn |
| 04/11 | Cổ Tức 10% Là 10% Của Cái Gì? Giải Mã Một Tờ Thông Báo Cổ Tức (61) | **Cổ Tức 10% Mà Chỉ Được 2,5%? Đọc Đúng Thông Báo Cổ Tức** (54) | 2,5% có trong script (ví dụ giả định) |
| 06/11 | FOMO: Vì Sao Lúc "Ai Cũng Lãi" Lại Là Lúc Nguy Hiểm Nhất? (57) | **Năm 2021 Ai Cũng Lãi: Vì Sao Đó Là Lúc Nguy Hiểm Nhất?** (55) | Mốc 2021→2022 có trên thumbnail |
| 08/11 | Vì Sao Lỗ Rồi Lại Càng Không Dám Bán? Chiếc Cân Lệch Trong Đầu Người Đầu Tư (75) | **Lỗ Rồi Càng Không Dám Bán: Vì Sao Lỗ Đau Gấp Đôi Lãi?** (52) | ⚠ Kiểm lại "×2" trong script trước khi sửa |
| 09/11 | Đường Trung Bình Động MA Là Gì? Một Đường Kẻ Tóm Tắt Quá Khứ, Và Điều Nó Không Biết (83) | **MA200 Báo Muộn 67 Phiên: Đường Trung Bình Động Là Gì?** (53) | ⚠ Kiểm lại "67 phiên" trong script |
| 11–16/11 | 4 bài E4, E5, E6, A2 | Giữ | Đã rút gọn ngày 23/10 |

## C. Thumbnail

- **Bắt buộc:** MIM 30/10 "Thuật toán đề xuất". Chữ đang bị cắt mép, phải dựng lại t1 bằng `thumb.py`, kiểm `t1_small.jpg`, rồi tải lên.
- Các thumbnail khác đều đã có con số hoặc người làm mỏ neo. Mình chưa đề xuất làm lại để tiết kiệm công.
- Sau 7 ngày, bài nào CTR vẫn dưới 2% thì làm lại thumbnail theo khuôn của bài "AI Đã Chết Hai Lần".

## D. Short nhóm chủ đề thua: dừng (bỏ hẹn giờ, giữ private)

Nhóm thua đã đo được:
- **MIM:** CAPTCHA, bảng tra nghề, thống kê lao động không có nhân vật (14–26% ở lại xem, 105–262 view).
- **CK:** nợ, thẻ, trả góp, ô ngân sách (14–30% ở lại xem, 51–139 view) và Short đọc thị trường chung.

**Dừng chắc chắn** (cùng nhóm đã thua):

| Kênh | Lên | Slug | Lý do |
|---|---|---|---|
| MIM | 27/10 04:00 | mim-lua-dao-1-tren-555 | Thống kê tỉ lệ, không có nhân vật |
| MIM | 27/10 10:00 | mim-6-nghin-ty-mot-phan-ba | Thống kê tỉ lệ, không có nhân vật |
| MIM | 02/11 10:00 | mim-luat-58-88-phan-tram | Thống kê tỉ lệ |
| MIM | 02/11 12:00 | mim-2000-quyet-dinh-toa-an | Thống kê |
| MIM | 02/11 14:00 | mim-9-tren-10-hoc-sinh-dung-ai | Thống kê khảo sát |
| CK | 29/10 12:00 | ck-ba-cau-hoi-khi-ai-cung-lai | Đọc thị trường chung |
| CK | 30/10 05:00 | ck-mot-trieu-ruoi-tai-khoan-2021 | Đọc thị trường chung |
| CK | 31/10 10:00 | ck-e2-mot-hoa-don-hai-cai-gia | Có góc "trả tối thiểu" (nợ) |

**Cân nhắc** (gần nhóm thua nhưng có nhân vật hoặc tình huống; mình đề xuất giữ):
- mim-17-lan-toi-khong-biet và mim-55-phan-tram-trich-dan-ma: thống kê, nhưng gắn với Long "AI bịa" tối nay.
- ck-fomo-den-khi-gia-cao: gắn với Long D2.

**Lấp chỗ trống:** không dựng gấp. Slot trống thì để trống. Short đã lên lịch vẫn đủ 2–3 bài/ngày.

## Đã làm (26/10, chủ kênh duyệt cả danh sách)

- **18 tiêu đề Long** đã sửa qua API.
  - Kiểm lại bằng API: cả 29 Long vẫn private và giữ nguyên giờ hẹn.
  - `upload_log`, `spec.json`, `gen_scenes.py` và `bundles` đã đồng bộ.
  - Hai số ⚠ có trong script:
    - "67 phiên" (MA200 sau đỉnh 06/01/2022);
    - "thường quanh mức gấp đôi". Tiêu đề D3 vì vậy viết "Gần Gấp Đôi".
- **Thumbnail MIM 30/10** đã dựng lại và tải lên.
  - Bản cũ cắt chữ vì dựng ngày 09/10, trước khi có bộ tự co chữ.
  - Bản cũ được giữ ở `output/long/mim-ai-feed/t1_cu_0910.jpg`.
  - ChatGPT cũng tạo một bản để so ("VẪN BIẾT BẠN THÍCH GÌ?"): ảnh `output/long/mim-ai-feed/so_sanh_thumb_chatgpt.jpg`. Mình chưa dùng bản này.
- **8 Short ở mục D** đã bỏ hẹn giờ, vẫn để private.
  - Trong `item.error` có ghi "tam_dung 26/10" kèm giờ hẹn cũ.
  - Cột `stage` vẫn là `published`, nên báo cáo analytics sẽ thấy các video này với 0 view.

## E. Việc sau khi duyệt

1. Sửa 2 tiêu đề lên tối nay (26/10) trước 18:00.
2. Sửa các tiêu đề còn lại sau khi kiểm 2 số ⚠.
3. Dựng lại thumbnail MIM 30/10.
4. Bỏ hẹn giờ 8 Short ở mục D.
5. Đồng bộ `spec.json`, `upload_log` và `state.sqlite`.
6. Ghi sổ thất bại và đo lại CTR sau 7 ngày.
