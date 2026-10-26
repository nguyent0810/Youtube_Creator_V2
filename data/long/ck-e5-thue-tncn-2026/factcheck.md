# Fact-check — script.md (bản 1) · ck-e5-thue-tncn-2026 (E5 · Thuế thu nhập cá nhân 2026)

Ngày kiểm: 23/10/2026. Mọi URL dưới đây đã được mở trong phiên viết. **Phép tính:** `analysis.py` (cộng dồn từng bậc) → `results.json`; kiểm độc lập
`check.py` (công thức rút gọn "TNTT × thuế suất − số trừ", đọc lại file CPI) → **"E5 check: OK (19 phép)"**. `script_lines.py` qua cổng; `studio_lint.py`
0/0; soát neo 0 lỗi.

Nhãn: **OK** · **OK-2** (nguồn thứ cấp, chưa mở văn bản gốc) · **SUY** · **TÍNH**.

## 1. Quy định

| # | Câu / cảnh | Giá trị | Nguồn (đã mở) | Nhãn |
|---|---|---|---|---|
| 1 | Giảm trừ 2026: 15,5 tr bản thân, 6,2 tr/người phụ thuộc; cũ 11 / 4,4 | NQ 110/2025/UBTVQH15, từ kỳ tính thuế 2026 | https://tapchicongthuong.vn/nhung-diem-moi-cua-luat-thue-thu-nhap-ca-nhan-nam-2025-va-tac-dong-den-doi-song-kinh-te-xa-hoi-556804.htm (15/10/2026) · https://hethongphapluat.com/phap-luat/huong-dan-chinh-sach-phap-luat/thu-nhap-bao-nhieu-thi-phai-nop-thue-tncn-nam-2026.html | OK-2 |
| 2 | Biểu 5 bậc/tháng: ≤10 tr 5% · 10–30 10% · 30–60 20% · 60–100 30% · >100 35% | Luật 109/2025/QH15 | nguồn #1 (bảng nguyên) | OK-2 |
| 3 | Biểu 7 bậc cũ: 5/10/18/32/52/80 tr: 5/10/15/20/25/30/35%; 35% từ 80 tr | | nguồn #1 | OK-2 |
| 4 | Luật hiệu lực 01/07/2026, phần tiền lương áp dụng từ kỳ tính thuế 2026 | | nguồn #1 (bài dùng cả hai mốc) | OK-2 · **SUY** ở câu "tháng nào bị khấu trừ theo cách cũ thì tính lại khi quyết toán" — lời đọc dùng "nếu có tháng nào" |
| 5 | Ngưỡng thu nhập người phụ thuộc 1 → 3 tr/tháng | | nguồn #1 | OK-2 |
| 6 | "Mỗi người phụ thuộc chỉ được tính giảm trừ một lần vào một người nộp thuế trong năm tính thuế"; phải đăng ký | nguyên văn | https://div.gov.vn/nguoi-lao-dong-can-biet-tang-muc-giam-tru-gia-canh-va-ho-so-chung-minh-nguoi-phu-thuoc-khi-nop-thue-thu-nhap-ca-nhan (26/06/2020) | OK-2 (bài 2020, quy định chưa thấy bị bỏ — kiểm hướng dẫn Luật 2025) |
| 7 | 9 tr / 3,6 tr trước 07/2020; 11 / 4,4 từ 01/07/2020 (NQ 954/2020) | | nguồn #6 | OK-2 |
| 8 | "Giá cả tăng quá 20% thì xem xét điều chỉnh giảm trừ" | lời Thứ trưởng Bộ Tài chính, dẫn Luật hiệu lực 01/07/2013 | https://lsvn.vn/giam-tru-gia-canh-tang-len-11-trieu-dong-thu-nhap-bao-nhieu-thi-phai-nop-thue-a44930.html (05/01/2021) | OK-2 |
| 9 | Mức 9 tr áp dụng "năm 2013" | ngầm từ #8 (luật hiệu lực 01/07/2013, 9 → 11) | #8 | OK-2 (yếu) |
| 10 | Bảo hiểm người lao động: BHXH 8% · BHYT 1,5% · BHTN 1% = 10,5% | | https://luatvietnam.vn/bao-hiem/tu-2026-muc-dong-bhxh-bhyt-bhtn-cua-nld-va-nsdld-duoc-tinh-nhu-the-nao-563-106906-article.html (01/02/2026) | OK-2 |
| 11 | Lương cơ sở 2,53 tr từ 01/07/2026 (NĐ 161/2026, ban hành 15/05/2026), trần đóng BHXH 50,6 tr | | https://lsvn.vn/tag/nghi-dinh-so-1612026ndcp.html | OK-2 |
| 12 | Lương tối thiểu vùng I 2026 = 5,31 tr (NĐ 293/2025) → trần BHTN 20 × = 106,2 tr | | nguồn #10 | OK-2 |
| 13 | Thu nhập bình quân tháng quý III/2026 = 9,2 tr | | https://www.nso.gov.vn/wp-content/uploads/2026/10/Thong-cao-bao-chi-ve-tinh-hinh-lao-dong-viec-lam-QIII-nam-2026.pdf (trích chữ PDF) | OK |
| 14 | Quyết toán thuế năm 2026 diễn ra đầu 2027; uỷ quyền hoặc tự làm | thông lệ | — | SUY (nói chung chung, "theo hướng dẫn của cơ quan thuế") |
| 15 | Khấu trừ hằng tháng theo biểu luỹ tiến tháng; biểu năm = biểu tháng × 12 khi quyết toán | thông lệ người cư trú, HĐ ≥ 3 tháng | — | SUY — có câu "chưa chắc là số phải nộp", "có thể được hoàn" |
| 16 | Phụ cấp / phần tiền làm thêm giờ cao hơn giờ thường có thể được miễn | | kiến thức luật TNCN hiện hành | SUY — nói "một số khoản … có thể được miễn, theo quy định riêng" |

## 2. Kênh tự tính (TÍNH — analysis.py, check.py OK)

Anh Khang 25 tr, 1 NPT, BH 10,5% = 2,625 tr → sau BH 22,375 · TNTT 2026 = 0,675 tr → **33.750 đ** · 2025 (11 + 4,4): 6,975 → **447.500 đ** · 2019 (9 + 3,6):
9,775 → **727.500 đ** · giảm ≈ 13,3 lần ("hơn mười ba lần") · tiết kiệm năm 12 × 413.750 = **4,965 tr** · ngưỡng lương gộp 2026 = giảm trừ / 0,895: **17,32 /
24,25 / 31,17 tr**; 2025: 12,29 / 17,21 / 22,12 · TNTT 20 tr: cũ **2,35 tr**, mới **1,5 tr** · 50 tr, 0 NPT: TNTT 29,25 → thuế **2,425 tr** = **4,85%** lương gộp, bậc chạm
10% · con đăng ký cho vợ (không nộp thuế): thuế anh Khang **343.750 đ**, chênh **3,72 tr/năm** · thưởng 50 tr: tháng thưởng TNTT 50,675 → **6,635 tr**; cả năm khấu trừ
**7,006 tr**; TNTT năm 58,1 → thuế năm **2,905 tr** → nộp thừa **≈ 4,10 tr** · bảng tra 2026 (nghìn đ, BH trần 50,6/106,2): 15 tr 0·0·0 · 20 tr 120·0·0 · 25 tr
344·34·0 · 30 tr 635·258·0 · 40 tr 1.530·910·395 · 50 tr 2.425·1.805·1.185 · 70 tr 6.299·5.059·3.819 · 100 tr 14.108·12.248·10.388 · 2025 để so: 30 tr/1 NPT 968;
40 tr/2 NPT 1.650 · giảm trừ quy về giá 2026 (CPI WB, 2026 = +4,52%): 9 tr 2013 ≈ **13,36**, 11 tr 2020 ≈ **13,35** → 15,5 cao hơn ≈ 2,15 tr; CPI 2013→2020 +22,3%.
"Mỗi người phụ thuộc đẩy ngưỡng ≈ 6,9 tr lương gộp" = 6,2 / 0,895 = 6,93.

## 3. Chỗ yếu / rủi ro

- **Văn bản gốc chưa mở** (thuvienphapluat 403): Luật 109/2025/QH15, NQ 110/2025, NĐ 161/2026. Các số khớp giữa ≥ 2 nguồn thứ cấp (Tạp chí Công Thương,
  Hệ thống pháp luật, kết quả tìm kiếm thuvienphapluat/LSVN). Trước dựng: mở toàn văn Luật 109/2025 Điều 9 (biểu) và điều hiệu lực/chuyển tiếp.
- **Nửa đầu 2026** trần BH là 46,8 tr (lương cơ sở 2,34) → các ô ≥ 50 tr của bảng tra áp từ 07/2026 (đã ghi "TỪ 07/2026" trên thẻ chương).
- **Luật cứng:** không tư vấn thuế, không chỉ dịch vụ; ví dụ "đăng ký con cho ai" chỉ trình bày phép tính, không khuyên. Nguồn #6 là bài trên div.gov.vn
  (trang của Bảo hiểm tiền gửi VN đăng lại hướng dẫn thuế) — nhãn trên màn hình ghi rõ "dẫn lại".

## Đối chiếu văn bản gốc 23/10

Văn bản gốc đã mở: **Luật Thuế TNCN 109/2025/QH15**, Công báo số 37 ngày 22/01/2026 (PDF có lớp chữ) — https://congbao.chinhphu.vn/van-ban/luat-so-109-2025-qh15-468671.htm
(bản ký số quét: https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/luat109-2025.pdf). Luật sửa đổi 24/04/2026 chỉ sửa khoản 1 Điều 7 (ngưỡng doanh thu hộ kinh
doanh) — không đụng biểu thuế/giảm trừ (https://xaydungchinhsach.chinhphu.vn/thong-qua-luat-sua-doi-bo-sung-4-luat-thue-thu-nhap-ca-nhan-thue-gia-tri-gia-tang-thue-thu-nhap-doanh-nghiep-thue-tieu-thu-dac-biet-119260424140703304.htm).
**Luật BHXH 41/2024/QH15** (Công báo 987+988) cho phần bảo hiểm.

| Ý | Kết luận | Văn bản gốc · trích ≤ 15 chữ |
|---|---|---|
| Biểu 5 bậc/tháng: đến 10 tr 5% · 10–30 10% · 30–60 20% · 60–100 30% · > 100 35% | **ĐÚNG** | Luật 109 Đ9.2: "Trên 60 đến 100 … 30"; "Trên 100 … 35" |
| Giảm trừ 15,5 tr bản thân, 6,2 tr/người phụ thuộc | **ĐÚNG** | Đ10.1: "15,5 triệu đồng/tháng (186 triệu đồng/năm)"; "6,2 triệu đồng/tháng" |
| "Từ năm nay" / áp dụng cả kỳ tính thuế 2026; luật hiệu lực 01/07/2026 | **ĐÚNG** | Đ29.2: tiền lương "áp dụng từ kỳ tính thuế năm 2026"; Đ29.1 "01 tháng 7 năm 2026" |
| Câu mở CH05 "theo luật áp dụng từ giữa năm 2026" | **LỆCH** | Phần tiền lương áp cho cả năm 2026 (Đ29.2); "từ 07/2026" chỉ đúng cho trần bảo hiểm → **đã sửa**: "theo luật mới, với trần bảo hiểm từ tháng bảy năm 2026" |
| "Mỗi người phụ thuộc chỉ được tính giảm trừ một lần, vào một người nộp thuế, **trong một năm**" + màn hình "… trong năm tính thuế", nguồn "dẫn lại div.gov.vn 2020" | **LỆCH (nhẹ)** | Đ10.3: "chỉ được tính giảm trừ một lần vào một người nộp thuế" (không có "trong năm") → **đã sửa** lời + màn hình; nguồn màn hình đổi thành "LUẬT THUẾ TNCN 109/2025/QH15 · ĐIỀU 10 · KHOẢN 3" |
| "Khi giá cả tăng quá 20%, mức giảm trừ sẽ được xem xét điều chỉnh" (trình bày như nguyên tắc hiện hành) | **LỆCH** | Đ10.2 luật mới: "Căn cứ biến động của giá cả, thu nhập, Chính phủ trình…" — bỏ ngưỡng 20% → **đã sửa** thành "Luật thuế cũ có một nguyên tắc"; màn hình ref "LUẬT CŨ · LUẬT 2025 XÉT THEO GIÁ CẢ VÀ THU NHẬP". Ngưỡng 20% của luật cũ: KHÔNG KIỂM ĐƯỢC bản gốc Luật 26/2012 (chỉ LSVN) — giữ, rủi ro thấp |
| Ngưỡng thu nhập người phụ thuộc 1 → 3 tr/tháng | **ĐÚNG qua Cổng TTĐT Chính phủ** (chưa mở toàn văn Thông tư 87/2026/TT-BTC) | Luật Đ10.4b giao "mức do Bộ trưởng Bộ Tài chính quy định"; xaydungchinhsach.chinhphu.vn 07/07/2026: "không vượt quá 03 triệu đồng" (TT 87/2026) → nguồn thêm vào mô tả |
| Người phụ thuộc: con chưa thành niên; cha mẹ, vợ/chồng không có (hoặc thu nhập thấp) | **ĐÚNG** | Đ10.4 |
| Tiền làm thêm giờ "phần trả cao hơn giờ thường có thể được miễn" | **LỆCH (nhẹ)** | Đ4.8 luật mới: "Tiền lương làm việc ban đêm, làm thêm giờ" được miễn (chi tiết do Chính phủ) → **đã sửa**: "tiền lương làm thêm giờ và làm đêm, có thể được miễn theo quy định chi tiết" |
| Bảo hiểm trừ trước khi tính thuế | **ĐÚNG** | Đ8.2: trừ "các khoản đóng góp bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp" |
| BHXH người lao động 8% | **ĐÚNG** | Luật 41/2024 Đ33: "Mức đóng hằng tháng bằng 8% tiền lương" |
| Trần đóng 20 lần mức tham chiếu (= lương cơ sở 2,53 tr → 50,6 tr) | **ĐÚNG phần "20 lần"** (Luật 41/2024 Đ31: "cao nhất bằng 20 lần mức tham chiếu"); lương cơ sở 2,53 tr (NĐ 161/2026): **KHÔNG KIỂM ĐƯỢC** bản gốc | Giữ (chỉ ảnh hưởng ô ≥ 50 tr của bảng tra) |
| BHYT 1,5%, BHTN 1%; lương tối thiểu vùng I 5,31 tr | 5,31 tr **ĐÚNG** (NĐ 293/2025 qua Cổng TTĐT Chính phủ); 1,5% / 1%: **KHÔNG KIỂM ĐƯỢC** bản gốc Luật BHYT / Luật Việc làm trong phiên | Giữ — tỷ lệ ổn định nhiều năm |
| Biểu 7 bậc cũ; 9 / 3,6 tr (2013) → 11 / 4,4 tr (07/2020) | **KHÔNG KIỂM ĐƯỢC** bản gốc Luật 26/2012, NQ 954/2020 | Giữ — khớp ≥ 2 nguồn; là số lịch sử |
| Thu nhập bình quân quý III/2026 9,2 tr | **ĐÚNG** (PDF Cục Thống kê, bản 1) | — |

Số không đổi → analysis.py không cần chạy lại; check.py OK (19 phép); script_lines.py + studio_lint.py 0/0; soát neo cảnh 0 lỗi. Mô tả: thêm nguồn Công báo
Luật 109/2025 và Cổng TTĐT Chính phủ (ngưỡng 3 triệu).
