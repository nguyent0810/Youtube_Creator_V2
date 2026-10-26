# Fact-check — script.md (bản 1) · ck-a2-luong-va-lam-phat (A2 · Lương 10 triệu năm 2016 và lạm phát)

Ngày kiểm: 23/10/2026. Mọi URL dưới đây đã được mở trong phiên viết. **Phép tính:** `analysis.py` (tỷ số chỉ số CPI) → `results.json`; kiểm độc lập
`check.py` (nhân chuỗi % lạm phát từng năm — chuỗi World Bank thứ hai) → **"A2 check: OK (24 phép)"**. `script_lines.py` qua cổng; `studio_lint.py` 0/0;
soát neo 0 lỗi. Dữ liệu tải: `wb_cpi_index.json` (FP.CPI.TOTL, 2010 = 100) và `wb_cpi_inflation.json` (FP.CPI.TOTL.ZG), API World Bank, lastupdated 08/10/2026.

Nhãn: **OK** · **OK-2** · **SUY** · **TÍNH**.

## 1. Số liệu

| # | Câu / cảnh | Giá trị | Nguồn (đã mở) | Nhãn |
|---|---|---|---|---|
| 1 | Lạm phát bình quân năm 2016–2025: 2,67 · 3,52 · 3,54 · 2,80 · 3,22 · 1,83 · 3,16 · 3,25 · 3,62 · 3,31; thấp nhất 2021, cao nhất 2024 | | https://api.worldbank.org/v2/country/VNM/indicator/FP.CPI.TOTL.ZG?format=json (trang: https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=VN) | OK — WB tính từ chỉ số bình quân năm; một số năm lệch ±0,1–0,2 điểm so con số Cục Thống kê công bố (vd 2008: WB 23,12, GSO 22,97) → lời đọc làm tròn "khoảng hai mươi ba" |
| 2 | 2008 ≈ 23%, 2011 ≈ 18,7% ("gần mười chín") | | nguồn #1 | OK |
| 3 | CPI bình quân 9 tháng 2026 +4,52%; tháng 9 +5,08% so cùng kỳ; lạm phát cơ bản 4,26%; 11 nhóm hàng | | https://www.nso.gov.vn/wp-content/uploads/2026/10/Tong-quan-CPI-chi-so-gia-vang-do-la-My-thang-9-QIII-va-9-thang-nam-2026.pdf (30/09/2026, trích chữ PDF) | OK |
| 4 | Tháng 9/2026 so cùng kỳ: giao thông +11,67 (nhiên liệu +23,96) · nhà ở-điện nước +6,47 (thuê nhà +4,88; điện sinh hoạt +4,98) · ăn uống +4,44 (lương thực +0,81; thực phẩm +3,89; ăn ngoài +7,4) · giáo dục +2,93 · thuốc-y tế +1,47 · thông tin-truyền thông +0,33 | | nguồn #3 | OK — "điện thoại, internet" = nhóm thông tin và truyền thông (diễn đạt) |
| 5 | Lương tối thiểu vùng I 2016 = 3,5 tr (NĐ 122/2015, từ 01/01/2016) | | https://vnbusiness.vn/tu-112016-tang-luong-toi-thieu-vung.html (23/11/2015) | OK-2 |
| 6 | Lương tối thiểu vùng I 2026 = 5,31 tr (NĐ 293/2025) | | https://luatvietnam.vn/bao-hiem/tu-2026-muc-dong-bhxh-bhyt-bhtn-cua-nld-va-nsdld-duoc-tinh-nhu-the-nao-563-106906-article.html (01/02/2026) | OK-2 |
| 7 | Thu nhập bình quân quý III/2026 9,2 tr, +823,8 nghìn so cùng kỳ ("gần mười phần trăm" = 9,8%) | | https://www.nso.gov.vn/wp-content/uploads/2026/10/Thong-cao-bao-chi-ve-tinh-hinh-lao-dong-viec-lam-QIII-nam-2026.pdf | OK · TÍNH |
| 8 | Zimbabwe: giữa 11/2008 lạm phát tháng "hàng tỷ phần trăm"; 01/2009 tờ 100 nghìn tỷ đô la Zimbabwe; ở đỉnh không đủ trả vé xe buýt; 04/2009 ngừng in tiền | Wikipedia ghi 79,6 hoặc 790,6 tỷ %/tháng (hai số lệch nhau) → lời đọc chỉ nói "hàng tỷ phần trăm" | https://en.wikipedia.org/wiki/Hyperinflation_in_Zimbabwe (dẫn BBC 16/01/2009, 29/01/2009) | OK-2 |
| 9 | "Cục Thống kê công bố vào cuối tháng" | thông cáo tháng 9 ký 30/09/2026 | nguồn #3 | OK |

## 2. Kênh tự tính (TÍNH — analysis.py, check.py OK)

CPI 2016 → 2025 ×**1,3206** (≈ +32%; bình quân **3,14%/năm**) · 2026 giả định ×1,0452 → 2016 → 2026 ×**1,3803** (≈ +38%) · 10 tr 2016 = **13,80 tr** 2026 · 10 tr để yên →
sức mua **7,25 tr** (mất 27,5% = "hơn một phần tư") · 13 tr: **−5,8%**; 13 tr theo giá 2016 = **9,42 tr**; 14 tr **+1,4%**; 15 tr **+8,7%** · tăng lương 3/5/7/10% khi giá
+4,52%: **−1,45 / +0,46 / +2,37 / +5,24%** · lương tối thiểu ×1,517 (+52%) → thực **+9,9%** · thu nhập quý III +9,8% danh nghĩa → thực **+4,5%** (so +5,08% tháng 9) ·
2008: 100 / 1,2312 ≈ **81 nghìn** · 2007 → 2012 ×**1,86** · 1996 → 2025 ×**4,62** · nửa sức mua: 3% → **23,4 năm**; 4,52% → **15,7 năm** (quy tắc 70 cho ≈ 23 / 15,5) ·
2036 (giả định): 13,8 × 1,03^10 = **18,5**; × 1,04^10 = **20,4**; × 1,05^10 = **22,5 tr** · lương 13 tr tăng đều 3/5/7%/năm → 2036: **17,5 / 21,2 / 25,6 tr** ·
1,03^10 = 1,344; 1,05^10 = 1,629 · giỏ anh Tuấn (tỷ trọng giả định 30/25/15/10/5/10/5) = **6,65%**, xăng góp 2,40 điểm = **36%**; giỏ chị Mai (40/10/15/10/10/15) = **2,77%**;
so 5,08: 6,65/5,08 = 1,31 ("cao hơn khoảng một phần ba"), 2,77/5,08 = 0,55 ("khoảng một nửa", "chỉ hơn một nửa") · ví dụ 12,5 → 13 tr: 1,04 / 1,0452 → **−0,5%**.

## 3. Chỗ yếu / rủi ro

- **Giỏ cá nhân dùng mức tăng của nhóm/mặt hàng tháng 9 so cùng kỳ** (không phải bình quân 9 tháng) — lời đọc nói "tháng chín năm nay, so với cùng tháng năm ngoái"
  và so với 5,08% của cùng tháng (không so với 4,52%).
- **"Lương tối thiểu tăng nhanh hơn giá cả" (10 năm) — OK theo #5–#6; "năm nay thu nhập bình quân cũng vậy" — OK theo #7.** Không khẳng định thu nhập bình
  quân 10 năm (chưa có chuỗi đã mở).
- **Không dự báo:** ba mức 3/4/5% gắn nhãn "GIẢ ĐỊNH · KHÔNG PHẢI DỰ BÁO" trên cảnh; lời đọc "Mình không đoán được…".
- **Khác bài cũ:** B2 (lãi kép) có đoạn "trừ lạm phát" cho tiền để dành; A2 nói về lương — câu "phần ấy gọi là lãi thực" không gọi tên bài cũ.
- **Luật cứng:** không tên ngân hàng; nguồn World Bank là tổ chức quốc tế (chỉ ở dòng nguồn); không khuyên mua vàng/gửi tiền chống lạm phát.

## Đối chiếu văn bản gốc 23/10

Nguồn gốc đã mở: **Niên giám Thống kê 2024 (Cục Thống kê)**, biểu 309 "CPI bình quân năm (năm trước = 100)" —
https://www.nso.gov.vn/wp-content/uploads/2025/06/NGTK-Cuc-TK-2024_BQ.pdf · thông cáo giá năm 2025 —
https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2026/01/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-muoi-hai-quy-iv-va-nam-2025/ · thông cáo/thông cáo kinh tế – xã hội
GSO các năm 2016, 2019, 2011 (kết quả trên nso.gov.vn / gso.gov.vn) · NĐ 122/2015 (https://vanban.chinhphu.vn/default.aspx?pageid=27160&docid=182151) · NĐ 293/2025
(https://xaydungchinhsach.chinhphu.vn/nghi-dinh-so-293-2025-nd-cp-quy-dinh-muc-luong-toi-thieu-doi-voi-nguoi-lao-dong-lam-viec-theo-hop-dong-lao-dong-119251110172808433.htm).

| Năm | GSO/NSO (%) | WB dùng trong bài (%) | Chênh |
|---|---|---|---|
| 2016 | 2,66 | 2,67 | 0,01 |
| 2017 · 2018 · 2019 | 3,53 · 3,54 · 2,79 (thông cáo GSO 12/2019) | 3,52 · 3,54 · 2,80 | ≤ 0,01 |
| 2020 · 2021 · 2022 · 2023 · 2024 | 3,23 · 1,84 · 3,15 · 3,25 · 3,63 (Niên giám 2024, biểu 309: "103,23 101,84 103,15 103,25 103,63") | 3,22 · 1,83 · 3,16 · 3,25 · 3,62 | ≤ 0,01 |
| 2025 | 3,31 ("CPI bình quân năm 2025 tăng 3,31% so với năm 2024") | 3,31 | 0 |
| 2011 | 18,58 ("tăng 18,58% so với bình quân năm 2010") | — | lời đọc "gần mười chín" — **ĐÚNG** |
| 2008 | 22,97 (số GSO; chưa mở thông cáo 2008) | 23,12 | lời đọc "khoảng hai mươi ba" — **ĐÚNG** |

| Ý | Kết luận | Ghi chú |
|---|---|---|
| 2016→2025 +32%, bình quân ≈ 3,1%/năm; thấp nhất 2021 (~1,8), cao nhất 2024 (~3,6) | **ĐÚNG** | Nhân chuỗi số GSO: ×1,3208, 3,14%/năm (WB ×1,3206) |
| 2016→2026 +38% (2026 = bình quân 9 tháng 4,52%); 10 tr → 13,8 tr; 13 tr: −5,8%; 14 tr +1,4%; 15 tr +8,7%; 13 tr = 9,4 tr giá 2016 | **ĐÚNG** | Chuỗi GSO cho ×1,3805 → các số làm tròn không đổi |
| 9 tháng 2026 +4,52%; tháng 9 +5,08%; nhóm hàng tháng 9 | **ĐÚNG** | PDF Cục Thống kê 30/09/2026 (bản 1) |
| 2008: 100 nghìn → ~81 nghìn; 2007→2012 gần gấp đôi | **ĐÚNG** (2011 đã mở; 2008–2010, 2012 là số GSO quen dùng, chưa mở thông cáo từng năm) | GSO 22,97; 6,88; 9,19; 18,58; 9,21 → 100/1,2297 = 81,3; ×1,86 — khớp WB |
| 1996→2025 ×4,6 | **KHÔNG KIỂM ĐƯỢC** từng năm 1996–2015 trên bản GSO trong phiên | Giữ — chuỗi WB lấy từ số liệu Cục Thống kê; các năm đã đối chiếu lệch ≤ 0,15 điểm |
| Lương tối thiểu vùng I 3,5 tr (2016) và 5,31 tr (2026) | **ĐÚNG** | NĐ 122/2015 (vùng I 3.500.000 đ, từ 01/01/2016); NĐ 293/2025 (vùng I 5.310.000 đ, từ 01/01/2026) |
| Thu nhập bình quân quý III/2026 9,2 tr, +9,8% | **ĐÚNG** | PDF Cục Thống kê (bản 1) |
| Zimbabwe 2008–2009 | **KHÔNG KIỂM ĐƯỢC** nguồn nhà nước (ngoài phạm vi cổng VN) | Giữ — lời đọc đã nói mềm "hàng tỷ phần trăm" |

**Bài sạch:** không sửa lời đọc / màn hình. Chỉ thêm 3 nguồn chính thức vào mô tả (thông cáo CPI 2025, NĐ 122/2015, NĐ 293/2025). check.py OK (24 phép);
studio_lint.py 0/0; soát neo cảnh 0 lỗi.
