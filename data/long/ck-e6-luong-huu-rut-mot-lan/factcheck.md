# Fact-check — script.md (bản 1) · ck-e6-luong-huu-rut-mot-lan (B5 · Rút BHXH một lần hay lương hưu)

Ngày kiểm: 23/10/2026. Mọi URL dưới đây đã được mở trong phiên viết. **Phép tính:** `analysis.py` → `results.json`; kiểm độc lập `check.py` (bảng tỷ
lệ viết tay theo lời luật + mô phỏng tháng rút dần) → **"E6 check: OK (36 phép)"**. `script_lines.py` qua cổng; `studio_lint.py` 0/0; soát neo 0 lỗi.

Nhãn: **OK** · **OK-2** (thứ cấp) · **SUY** · **TÍNH**.

## 1. Quy định và số liệu

| # | Câu / cảnh | Giá trị | Nguồn (đã mở) | Nhãn |
|---|---|---|---|---|
| 1 | Luật BHXH 2024 hiệu lực 01/07/2025; 15 năm có lương hưu (cũ 20) | | https://tuoitre.vn/plo/cach-tinh-luong-huu-theo-luat-bhxh-2024-post821894.html (PLO 01/12/2024) | OK-2 |
| 2 | Nữ: 45% ứng 15 năm, +2%/năm, tối đa 75% ở 30 năm | | nguồn #1 | OK-2 |
| 3 | Nam: 40% ứng 15 năm, +1%/năm tới 20 năm, rồi +2%/năm, tối đa 75% ở 35 năm | ví dụ ông B 18 năm 4 tháng = 43,5% (khớp +1%/năm); mốc 45% ở 20 năm theo nguồn khác trong kết quả tìm kiếm | nguồn #1 | OK-2 — PLO tóm tắt "+2%/năm" chung; cơ chế +1% suy từ ví dụ của chính bài → **kiểm Điều 66 Luật 41/2024** |
| 4 | BHXH một lần: 1,5 tháng/năm trước 2014; 2 tháng/năm từ 2014; bình quân tiền lương | | https://luatvietnam.vn/bao-hiem/dieu-kien-huong-bao-hiem-xa-hoi-1-lan-563-23984-article.html | OK-2 |
| 5 | Điều kiện người đóng trước 01/07/2025: nghỉ 12 tháng, không đóng bắt buộc/tự nguyện, chưa đủ 20 năm; định cư nước ngoài, bệnh nặng; đủ tuổi chưa đủ 15 năm → một lần hoặc trợ cấp hằng tháng | | nguồn #4 | OK-2 |
| 6 | "Đóng từ 07/2025 gần như không còn đường rút một lần" | trường hợp 12 tháng chỉ áp cho người đóng trước ngày Luật hiệu lực | nguồn #4 | SUY (đúng theo danh sách điều kiện) |
| 7 | Bình quân tiền lương được điều chỉnh trượt giá | | luật hiện hành (công cụ tính "cập nhật hệ số trượt giá" của thuvienphapluat trong kết quả tìm kiếm) | OK-2 (yếu) |
| 8 | Đã nhận một lần → thời gian ấy không tính lương hưu; chưa nhận → bảo lưu, cộng nối | | https://ketoanthuanthien.vn/hoi-dap/tai-sao-can-bao-luu-thoi-gian-tham-gia-bhxh-thay-vi-rut-mot-lan/ (cập nhật 24/05/2026, dẫn Luật 41/2024 Đ23, 64, 65, 70, 71, 79) | OK-2 (yếu: trang kế toán) |
| 9 | Tự nguyện: 22% thu nhập tự chọn (Điều 36 Luật 2024); Nhà nước hỗ trợ một phần (NĐ 159/2025) | | https://www.meinvoice.vn/tin-tuc/32269/bao-hiem-xa-hoi-tu-nguyen/ (16/11/2025) | OK-2 |
| 10 | Tuổi nghỉ hưu: nữ 57 (2026), +4 tháng/năm → 60 từ 2035; nam 61 tuổi 6 tháng (2026), +3 tháng/năm → 62 từ 2028 | bảng Điều 4 | https://vnuf.edu.vn/wp-content/uploads/2021/01/Nghi-dinh_135-2020-ND-CP..pdf (trích chữ PDF) | OK |
| 11 | Chị Hạnh sinh 1991 → 60 tuổi năm 2051 | nữ nghỉ hưu sau 2035 ở 60 | #10 | OK · TÍNH |
| 12 | 2016–2022: > 4,8 triệu người hưởng một lần; ~1,3 triệu quay lại; 20–40 tuổi ≈ 77,5%; dưới 5 năm 66,6%; 5–10 năm 23,8% ("gần chín phần mười số hồ sơ đóng dưới mười năm" = 90,4%) | báo cáo Bộ LĐ-TB&XH | https://vneconomy.vn/phan-lon-nguoi-lao-dong-rut-bao-hiem-xa-hoi-mot-lan-la-lao-dong-tre.htm (03/07/2023) | OK-2 · TÍNH (cộng 2 nhóm; nguồn tính trên hồ sơ) |
| 13 | Tuổi thọ trung bình nữ 2024: 77,3 (lúc sinh) | | https://news.tuoitre.vn/average-life-expectancy-in-vietnam-reaches-747-years-in-2024-10384693.htm (21/02/2025, Cục Thống kê) | OK |
| 14 | "Người đã sống tới 60 thường còn sống lâu hơn mốc ấy" | tính chất của tuổi thọ kỳ vọng có điều kiện | — | SUY (kiến thức nhân khẩu học chung) |
| 15 | Trợ cấp hưu trí xã hội từ 75 tuổi (người không có lương hưu, ngân sách chi); mức đề xuất 500 nghìn/tháng khi soạn nghị định | | https://hatinh.gov.vn/vi/bai-viet/nguoi-du-75-tuoi-co-the-nhan-tro-cap-huu-tri-500000-dong-moi-thang (20/01/2025, dự thảo) | OK-2 — lời đọc nói rõ "mức đề xuất khi soạn nghị định"; NĐ 176/2025 chưa mở → **kiểm mức chính thức** |
| 16 | Người hưởng lương hưu có thẻ BHYT do quỹ BHXH đóng | | — | SUY (Luật BHYT: người hưởng lương hưu thuộc nhóm do tổ chức BHXH đóng) — chưa mở nguồn → **kiểm** |
| 17 | Phần người lao động tự đóng BHXH = 8% lương | | https://luatvietnam.vn/bao-hiem/tu-2026-muc-dong-bhxh-bhyt-bhtn-cua-nld-va-nsdld-duoc-tinh-nhu-the-nao-563-106906-article.html | OK-2 |
| 18 | "Công ty của chị cũng đóng vào quỹ, song song với chị" | không nêu tỷ lệ của doanh nghiệp | — | OK (định tính) |

## 2. Kênh tự tính (TÍNH — analysis.py, check.py OK; mọi số quy về giá hôm nay)

10 năm × 2 × 10 tr = **200 tr** (4 năm trước 2014 + 6 năm sau → 180 tr, minh hoạ) · phần tự đóng 8% × 10 × 120 = **96 tr** → 200/96 = 2,08 ("gấp đôi") · nữ 15/20/25/30
năm: **4,5 / 5,5 / 6,5 / 7,5 tr**; nam 15 năm 4,0 tr · hoà 200 tr: 44,4 tháng (≈ 63 tuổi 8 tháng); 30 năm: 26,7 tháng (≈ 62 tuổi) · tới 77,3 tuổi: 17,3 × 12 × 4,5
= **934 tr** · đóng thêm 5 năm: 8% → **48 tr**; tự nguyện 22% → **132 tr** (chưa trừ hỗ trợ) · 200 × (1 + r)^25: −1% **156** · 0% 200 · 1% **256** · 2% **328** ·
3% **419** tr · 328 tr rút 4,5 tr/tháng, lãi thực 2%/năm → **≈ 78 tháng** (6,5 năm, ≈ 66,5 tuổi) · nợ 200 tr lãi 30%/năm → ~60 tr lãi/năm (giả định).

## 3. Chỗ yếu / rủi ro

- Nguồn luật đều thứ cấp (PLO, LuatVietnam, MISA, trang kế toán); thuvienphapluat 403. Trước dựng: mở toàn văn Luật 41/2024/QH15 — Điều 64, 66 (tỷ lệ),
  70–71 (một lần), 23 (trợ cấp hằng tháng), 21 (hưu trí xã hội), và NĐ 176/2025 (mức trợ cấp).
- Mô hình "giá hôm nay" giả định lương hưu điều chỉnh theo giá — lời đọc nói rõ ở CH06.
- **Luật cứng:** không "nên rút/không nên rút" (đã quét); có chương công bằng cho người rút (CH05); câu "Nên rút một lần…" đổi thành "Vì thế, rút một lần…"
  để TTS/khán giả không nghe nhầm là khuyên.

## Đối chiếu văn bản gốc 23/10

Văn bản gốc đã mở: **Luật BHXH 41/2024/QH15**, Công báo số 987 + 988 ngày 25/08/2024 (PDF 88 trang, có lớp chữ) —
https://congbao.chinhphu.vn/van-ban/luat-so-41-2024-qh15-42576.htm. **Trợ cấp hưu trí xã hội:** NĐ 176/2025/NĐ-CP (https://vanban.chinhphu.vn/?pageid=27160&docid=214435)
và NĐ 335/2026/NĐ-CP ngày 21/08/2026 qua Báo Điện tử Chính phủ — https://baochinhphu.vn/chinh-sach-moi-co-hieu-luc-tu-thang-10-2026-102261001102816112.htm;
văn bản hợp nhất 15/2026/VBHN-BYT (540.000 đ) — https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-dinh-quy-dinh-ve-tro-cap-huu-tri-xa-hoi-119260908165726071.htm.

| Ý | Kết luận | Văn bản gốc · trích ≤ 15 chữ |
|---|---|---|
| Luật hiệu lực 01/07/2025 | **ĐÚNG** | Đ140.1: "có hiệu lực thi hành từ ngày 01 tháng 7 năm 2025" |
| Đủ 15 năm đóng là có lương hưu | **ĐÚNG** | Đ64.1: "thời gian đóng bảo hiểm xã hội bắt buộc từ đủ 15 năm" |
| Nữ 45% ứng 15 năm, +2%/năm, tối đa 75% | **ĐÚNG** | Đ66.1a: "45% … tương ứng 15 năm … thêm 2%, mức tối đa bằng 75%" |
| Nam 40% ứng 15 năm, +1%/năm tới 20 năm, sau đó +2%, tối đa 75% (35 năm) | **ĐÚNG** | Đ66.1b: "từ đủ 15 năm đến dưới 20 năm … 40% … thêm 1%" |
| Một lần: 1,5 tháng/năm trước 2014; 2 tháng/năm từ 2014; bình quân tiền lương | **ĐÚNG** | Đ70.3a–b: "Bằng 1,5 tháng … trước năm 2014"; "Bằng 02 tháng … từ năm 2014" |
| Bình quân tiền lương được điều chỉnh theo trượt giá | **ĐÚNG** | Đ73.2: "được điều chỉnh trên cơ sở chỉ số giá tiêu dùng" |
| Người đóng trước 01/07/2025: nghỉ 12 tháng, không đóng bắt buộc/tự nguyện, chưa đủ 20 năm | **ĐÚNG** | Đ70.1đ: "sau 12 tháng không thuộc đối tượng … chưa đủ 20 năm" |
| Người đóng từ 07/2025 gần như không còn đường rút; còn định cư nước ngoài, bệnh nặng | **ĐÚNG** (suy từ danh sách Đ70.1 a–e) | Đ70.1b "Ra nước ngoài để định cư"; 70.1c "ung thư, bại liệt, xơ gan mất bù…" |
| Đã nhận một lần → đồng hồ năm đóng về 0 ("xoá thời gian đóng") | **ĐÚNG** — nay có văn bản gốc (thay nguồn trang kế toán) | Đ5.3: "đã được tính hưởng bảo hiểm xã hội một lần thì không được tính" |
| Không rút → bảo lưu, cộng nối | **ĐÚNG** | Đ71: "thì được bảo lưu thời gian đóng bảo hiểm xã hội" |
| Tự nguyện 22% thu nhập tự chọn; Nhà nước hỗ trợ một phần | **ĐÚNG** | Đ36.1: "đóng bằng 22% mức thu nhập làm căn cứ"; Chính phủ quy định mức hỗ trợ |
| Đủ tuổi chưa đủ 15 năm → một lần hoặc trợ cấp hằng tháng | **ĐÚNG** | Đ70.1a + Đ23.1: "được hưởng trợ cấp hằng tháng từ chính khoản đóng" |
| Đóng tiếp (kể cả tự nguyện) cho đủ 15 năm | **ĐÚNG** | Đ33.7: thiếu trên 06 tháng "có quyền đóng tiếp bảo hiểm xã hội tự nguyện" |
| Người hưởng lương hưu có thẻ BHYT do quỹ BHXH đóng | **ĐÚNG** — nay có văn bản gốc | Đ119.2a: quỹ BHXH "Chi đóng bảo hiểm y tế cho … Người đang hưởng lương hưu" |
| Từ 75 tuổi, người không có lương hưu được trợ cấp hưu trí xã hội, ngân sách chi | **ĐÚNG** | Đ21.1a "Từ đủ 75 tuổi trở lên"; Đ22.1 mức "do Chính phủ quy định" (70–75 tuổi hộ nghèo/cận nghèo: video không nhắc) |
| "Mức đề xuất khi soạn nghị định là 500 nghìn/tháng" (lời đọc) + màn hình "MỨC ĐỀ XUẤT KHI SOẠN NGHỊ ĐỊNH" + nguồn mô tả "đề xuất … Hà Tĩnh 2025" | **LỆCH** | 500 nghìn **đã là mức chính thức** từ 01/07/2025 (NĐ 176/2025); NĐ 335/2026 sửa khoản 1 Điều 3 NĐ 176 "từ 500.000 đồng/tháng lên 540.000 đồng/tháng", hiệu lực 05/10/2026 → **đã sửa** lời đọc: "Mức chung hiện nay là năm trăm bốn mươi nghìn đồng một tháng, từ tháng mười năm nay"; màn hình 500 → 540 "TỪ 05/10/2026 (NĐ 335/2026)"; mô tả: bỏ nguồn Hà Tĩnh, thêm Báo Chính phủ 01/10/2026 + NĐ 176/2025 |
| Tuổi nghỉ hưu nữ 57 (2026) → 60 (2035), nam 61t6t → 62 (2028) | **ĐÚNG** (PDF NĐ 135/2020 Điều 4, bản 1) | — |
| Số liệu 2016–2022 (4,8 triệu lượt, 1,3 triệu quay lại, 66,6% / 23,8%) | **KHÔNG KIỂM ĐƯỢC** bản gốc báo cáo Bộ LĐ-TB&XH | Giữ — câu đã nói "báo cáo của Bộ Lao động khi ấy", số khớp VnEconomy |
| Phần người lao động tự đóng 8% | **ĐÚNG** | Đ33: "Mức đóng hằng tháng bằng 8% tiền lương" |

Số tự tính không đổi (500/540 không vào phép tính) → analysis.py không cần chạy lại; check.py OK (36 phép); script_lines.py + studio_lint.py 0/0; soát neo
cảnh 0 lỗi. Nguồn trang kế toán (Thuận Thiên) bỏ khỏi mô tả, thay bằng Công báo Luật 41/2024.
