# Factcheck: 5 Short pilot CK, 08–12/11/2026

Các con số tính toán được tính lại độc lập bằng code ngày 28/10:
- VN-Index: `data/ck/vnindex_1d.csv`;
- ví dụ giả định: theo đúng tham số của Long tương ứng.

Không bài nào nêu tên ngân hàng, công ty chứng khoán, hãng xe hay mã cổ phiếu, và không có "nên mua / bán". Mọi mô tả đều có câu "Nội dung giáo dục, không phải tư vấn đầu tư."

## 08/11 · `ck-p2-tra-truoc-mot-ty` · cặp 1 · hook A · Long B1 (pXKfIo_nyVM)

| # | Câu / chữ trên hình | Loại | Kiểm |
|---|---|---|---|
| 1 | "Tháng chín năm nay, sổ tiết kiệm mười hai tháng ở bốn ngân hàng lớn trả khoảng 6,8%/năm" | **sự thật có ngày** (hook A) | Factcheck Long B1, dòng CH04: "1 tỷ → 6,8% (4 NH lớn, 09/2026)" OK, nguồn [A1-83] [16]. Không nêu tên ngân hàng. |
| 2 | Căn hộ 2,5 tỷ, trả trước 1 tỷ | giả định | Long B1: trả trước 1 tỷ (40%) |
| 3 | "≈68 triệu tiền lãi một năm" | tính | 1.000 × 6,8% = 68,0 (lãi đơn một năm, không ghép) |
| 4 | "khoảng năm triệu bảy mỗi tháng" | tính | 68 / 12 = 5,67 |
| 5 | "thuê một căn y hệt, khoảng sáu triệu hai" | giả định | 6,25 triệu (như bài 07/11) |
| 6 | "riêng tiền lãi … gần đủ trả tiền thuê" | so sánh | 5,67 / 6,25 = 91%. Cùng câu với Long B1 CH04. |
| 7 | "cần tính vào trước khi so mua với thuê" | nhận định | không khuyên mua hay thuê |

## 09/11 · `ck-p3-nuoi-xe-moi-thang` · cặp 2 · hook A · Long B4 (Bx9w_a_1YOI, hẹn 01/11)

| # | Câu / chữ trên hình | Loại | Kiểm |
|---|---|---|---|
| 1 | Phí sử dụng đường bộ ô tô con không kinh doanh: 130 nghìn đồng/tháng | **sự thật có ngày** (hook A) | Nghị định 90/2023/NĐ-CP, hiệu lực 01/02/2024: xe chở người dưới 10 chỗ đăng ký tên cá nhân 130.000 đ/tháng ([Tạp chí Tòa án](https://tapchitoaan.vn/index.php/muc-thu-che-do-thu-nop-mien-quan-ly-va-su-dung-phi-su-dung-duong-bo-tu-ngay-01-thang-02-nam-20249948.html)). Từ 2026, Nghị định 364/2025/NĐ-CP giữ 130.000 đ/tháng cho xe chở người tối đa 8 chỗ không kinh doanh vận tải ([LSVN](https://lsvn.vn/chinh-thuc-bo-dan-tem-thu-phi-duong-bo-tren-kinh-o-to-a168088.html)). **Đã sửa** câu đọc từ "Từ năm 2023…" thành "Năm nay … vẫn là", và ghi nguồn NĐ 364/2025. Ngày hiệu lực cụ thể của NĐ 364/2025 chưa kiểm được, nên không đọc ra. |
| 2 | Xe 700 triệu, 12.000 km/năm | giả định | Long B4 `analysis.py` |
| 3 | Xăng ≈1,7 triệu/tháng | tính | 12.000/100 × 7 × 24.000 = 20,16 triệu/năm, tức 1,68/tháng |
| 4 | Gửi xe 1,5 triệu | giả định | Long B4 |
| 5 | Bảo hiểm vật chất ≈0,9 triệu | tính | 1,5% × 700 / 12 = 0,875 |
| 6 | Bảo dưỡng 0,5 triệu | tính | 6 / 12 |
| 7 | Bắt buộc + đường bộ 0,17 triệu | tính | (1,56 + 0,437 × 1,1) / 12 = 0,17. TNDS 437.000 đ chưa VAT theo NĐ 67/2023, Long B4 Ghi chú. |
| 8 | "khoảng bốn triệu bảy mỗi tháng" | tính | `results.json` run_month_y1 = 4,73 |
| 9 | "chừng ba phần trăm của bốn triệu bảy" | tính | 0,13 / 4,73 = 2,7% |

## 10/11 · `ck-p4-xe-mat-gia-moi-thang` · cặp 2 · hook B · Long B4

| # | Câu / chữ trên hình | Loại | Kiểm |
|---|---|---|---|
| 1 | "Chiếc xe bảy trăm triệu bạn mua năm nay…" | hook B, giả định | — |
| 2 | Bán lại 55% sau 5 năm | giả định | Long B4 (RESALE5 = 0,55), giống Long script dòng 87 |
| 3 | ≈385 triệu; mất 315 triệu | tính | 700 × 0,55 = 385; 700 − 385 = 315 |
| 4 | "khoảng năm triệu hai mỗi tháng", ≈5,25 | tính | 315 / 60 = 5,25 |
| 5 | "nhiều hơn tiền nuôi xe năm đầu, khoảng bốn triệu bảy" | tính | 5,25 > 4,73 |
| 6 | "tiền thuê chỉ vừa đủ bù phần mất giá" | nhận định | câu tương tự Long B4 dòng 91 |

**Lưu ý:** brief bản 4 ghi chủ đề "xe mất giá 3 năm đầu". Đã đổi sang **trung bình theo 5 năm**, cho khớp đúng giả định của Long B4. Long không có lịch mất giá theo từng năm, nên nếu nói "3 năm" kênh phải tự đặt thêm một giả định mới.

## 11/11 · `ck-p5-mua-sau-nam-tang-40` · cặp 3 · hook B · Long D2 (ULLEUHkYz9g, hẹn 06/11)

| # | Câu / chữ trên hình | Loại | Kiểm |
|---|---|---|---|
| 1 | "dữ liệu từ năm 2018 đến nay" | dữ liệu | CSV 08/10/2018 → 06/10/2026 |
| 2 | Ngày có mức tăng > 40% so với 12 tháng trước rơi gần hết vào 03/2021 → 01/2022 | tính | Tính lại: 194 ngày có đủ 12 tháng sau, từ 11/03/2021 tới 28/01/2022. Long D2: 197 ngày, 10/03/2021 → 08/02/2022 (lệch do cách lấy ngày). Nhóm thứ hai (12/2025 → 05/2026) chưa đủ 12 tháng sau nên không tính. |
| 3 | "khoảng tám trên mười trường hợp đang lỗ", 79% | tính | tính lại 79%; Long D2 cũng 79% |
| 4 | "Mức giữa là giảm khoảng bảy phần trăm" | tính | trung vị −7,4% (cả hai cách tính) |
| 5 | "những ngày khác, mức giữa tăng khoảng mười lăm phần trăm" | tính | tính lại: trung vị +14,7% cho mọi ngày còn lại. Long D2 chỉ có theo nhóm (+16,5 / +20,5 / +4,6), không có số gộp. |
| 6 | Biểu đồ: 659 (24/03/2020) · 1.182 (11/03/2021) · 1.529 (06/01/2022) · 912 (15/11/2022) | dữ liệu | CSV: 659,21 · 1.181,73 · 1.528,57 · 911,90 |
| 7 | "một giai đoạn trong quá khứ, không phải quy luật, càng không phải dự báo" | miễn trừ | Đúng: chỉ có **một** giai đoạn đủ dữ liệu. Chưa tính cổ tức, phí, thuế (có ghi trên hình và trong mô tả). |

## 12/11 · `ck-p6-270-nghin-tai-khoan-3-2022` · cặp 3 · hook A · Long D2

| # | Câu / chữ trên hình | Loại | Kiểm |
|---|---|---|---|
| 1 | "Tháng 3/2022, hơn 270 nghìn tài khoản chứng khoán mới", 270.217 | **sự thật có ngày** (hook A) | Factcheck Long D2 #2: VSD qua Thời báo Tài chính VN 07/04/2022, cá nhân 270.011 + tổ chức 206 = 270.217. OK. |
| 2 | Đỉnh "hơn 1.520 điểm vào đầu tháng một" | dữ liệu | 06/01/2022 đóng 1.528,57 |
| 3 | Cuối tháng 3 "quanh 1.490" | dữ liệu | 31/03/2022 đóng 1.492,15 |
| 4 | Giữa tháng 11 "khoảng 912" | dữ liệu | 15/11/2022 đóng 911,90 (đáy năm 2022) |
| 5 | "Giảm gần 40% từ cuối tháng 3", −38,9% | tính | 911,90 / 1.492,15 − 1 = −38,9% |
| 6 | "Đám đông đến khi chỉ số đã ở gần đỉnh" | nhận định | 31/03/2022 thấp hơn đỉnh 2,4%. Không nói "kỷ lục", vì không kiểm được tháng 3/2022 có phải tháng mở nhiều tài khoản nhất hay không. |
| 7 | "tám tháng sau, chỉ số mất gần bốn mươi phần trăm" | tính | 31/03 → 15/11 khoảng 7,5 tháng. Đọc "tám tháng" là làm tròn. |

## Chồng chủ đề cần biết

- `ck-mot-trieu-ruoi-tai-khoan-2021` (hẹn 30/10) nói về tài khoản năm 2021. Bài 12/11 dùng số tháng 3/2022.
- Có sẵn spec Short `ck-b4-tien-nuoi-xe` và `ck-b4-khoan-khong-hoa-don` (cùng chủ đề với 09/11 và 10/11). Hai spec này **chưa từng vào hàng chờ hay upload**. Pilot không dùng chúng, để giữ cùng khuôn dựng giữa A và B.
