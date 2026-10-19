# Kiểm chứng CK D2 `ck-d2-fomo` — 09/10/2026 (PM, vòng 1)

| # | Câu (chương) | Kết quả | Nguồn / ghi chú |
|---|---|---|---|
| 1 | Mọi số VN-Index 2018-10 → 2026-10 (đỉnh 06/01/2022 1.528,57; đáy 15/11/2022 911,90; vượt lại 25/07/2025; +132%; −40%; ví dụ 100 triệu / 3 triệu mỗi tháng; nhóm "> +40%") | OK — chạy lại `analysis.py` ra đúng `results.json` | vnstock/VCI, `data/ck/vnindex_1d.csv` |
| 2 | 03/2022: "hơn hai trăm bảy mươi nghìn tài khoản" (CH00) | OK | VSD qua Thời báo Tài chính VN 07/04/2022: cá nhân 270.011 + tổ chức 206 = **270.217** |
| 3 | 12/2021 kỷ lục 226.580; năm 2021 > 1,5 triệu, > tổng 2017–2020 (1,04 triệu) (CH00, CH03) | OK [SECONDARY] | VnEconomy, Báo Đấu thầu, Thời báo Tài chính (VSD) |
| 4 | 01/2021 ~86.000 tài khoản mới (CH03) | OK [SECONDARY] | Thị trường Tài chính Tiền tệ "Tháng 1/2021, hơn 86.000 tài khoản" |
| 5 | Cuối 2006 ~732 điểm; Q1/2007 +55,72%; đỉnh 12/03/2007 1.170,67; > 200.000 tài khoản tới 08/2007, gấp 3 cùng kỳ (CH01) | OK [SECONDARY] | SGGP tổng kết 2007; VnExpress "Những dấu mốc để đời của VN-Index" |
| 6 | "Bàn nhậu ngày Tết… hỏi lãi bao nhiêu" (CH01) | SỬA → lời dẫn báo | Bản 1 là hình ảnh kênh tự nghĩ ra; nay theo SGGP "hầu như ai cũng có thể khoe những thành tích kiếm tiền" |
| 7 | Đáy 24/02/2009 235,5 → "khoảng hai trăm ba mươi sáu", "mất khoảng tám mươi phần trăm" (CH01) | OK | 235,5 / 1.170,67 = −79,9% |
| 8 | 2017 +48%; Q1/2018 +19,33%, "nhanh nhất thế giới quý ấy" (CH02) | SỬA → thêm số cụ thể | Vietnam News "VN Index ends 2017 at 10-year high"; Bizhub/Vietstock 04/2018 "VN-Index world's top-performing market in Q1" |
| 9 | Đỉnh 09/04/2018 1.204,33; cuối 07/2018 ~935 (CH02) | OK [SECONDARY] | Vietnam News / VCSC daily |
| 10 | "Báo chí bàn mốc 1.300 điểm" (CH02) | OK | Vietnam News / Vietstock 01/2018 "VN Index expected to surpass 1,300 points in 2018" |
| 11 | "Mở tài khoản bằng điện thoại vài phút" (CH03) | SỬA → "mở ngay trên điện thoại, không cần ra quầy" | eKYC chứng khoán triển khai từ 08/2020 (Thị trường Tài chính Tiền tệ 14/08/2020). "Vài phút" không có nguồn; không nêu tên công ty |
| 12 | Barber & Odean 2008: cá nhân mua ròng cổ phiếu gây chú ý (lên báo, khối lượng bất thường, biến động một ngày cực mạnh); lý do = bài toán tìm kiếm khi mua, khi bán chỉ bán thứ đang có (CH04) | OK (abstract, nhiều nguồn) | RFS 21(2): 785–818. Thêm "hàng chục nghìn nhà đầu tư cá nhân" (dữ liệu môi giới chiết khấu Mỹ) |
| 13 | Đoạn "thấy mình tụt lại phía sau" (CH04) | GIỮ — diễn giải của kênh, không gắn nguồn, không trình bày như kết quả nghiên cứu | — |
| 14 | 2025: đáy 09/04/2025 → đỉnh 18/05/2026 +76%; "lần thứ hai" > +40%/12 tháng (CH06) | OK — kênh tự tính; lời đọc không dự báo | `results.json` run2025; nhóm > +40% thứ hai: 05/12/2025 → 27/05/2026 |

**Kiểm luật kênh:** không mã cổ phiếu, không tên công ty chứng khoán/quỹ, không "nên mua/bán", không dự báo (CH06 nói "chưa ai biết, kênh không đoán") ✔ · ví dụ CH05 ghi "giả định, theo chỉ số, không phí/thuế/cổ tức" ✔ · lời đọc không chữ số ✔ (cổng `script_lines`).

**Kết luận:** OK 10 · SỬA 4 (đã sửa) · BỎ 0. Có thể dàn cảnh + TTS.
