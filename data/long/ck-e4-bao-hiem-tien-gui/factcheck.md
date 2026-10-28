# Fact-check — script.md (bản 1) · ck-e4-bao-hiem-tien-gui (E4 · Bảo hiểm tiền gửi 350 triệu)

Ngày kiểm: 23/10/2026. Mọi URL dưới đây đã được mở trong phiên viết (WebFetch / tải PDF rồi trích chữ). **Phép tính:** `analysis.py` → `results.json`;
kiểm độc lập `check.py` (Decimal + công thức đóng, đọc lại file CPI trực tiếp) → **"E4 check: OK (12 phép)"**. Cổng `script_lines.py` (integrity +
cấm "trả lời ba câu hỏi") qua; `studio_lint.py` 0 lỗi 0 cảnh báo; soát neo cảnh (scratchpad `anchor_check.py`: mọi chữ neo có trong câu, mốc tăng dần,
sổ không tràn, tiêu đề biểu đồ không đè) 0 lỗi.

Nhãn: **OK** = khớp nguồn đã mở · **OK-2** = nguồn thứ cấp (báo/trang luật thuật lại văn bản), chưa mở văn bản gốc · **SUY** = suy luận của kênh từ nguồn, lời
đọc đã nói mềm · **TÍNH** = kênh tự tính (analysis.py + check.py).

## 1. Số liệu và quy định

| # | Câu / cảnh | Giá trị | Nguồn (đã mở) | Nhãn |
|---|---|---|---|---|
| 1 | Hạn mức từ 13/07/2026 | 350 triệu/người/tổ chức, gồm gốc và lãi; Thông tư 05/2026/TT-NHNN | https://div.gov.vn/tu-ngay-13-7-2026-han-muc-chi-tra-tien-bao-hiem-cua-bao-hiem-tien-gui-viet-nam-la-350-trieu-dong (đăng 15/07/2026) | OK |
| 2 | Mức trước đó | 125 triệu, QĐ 32/2021/QĐ-TTg (20/10/2021); tăng 225 triệu = +180% ("gần gấp ba" = ×2,8) | cùng nguồn #1 | OK |
| 3 | 93,68% người gửi được bảo vệ toàn bộ ở 350 triệu → "cứ khoảng 16 người có 1 người vượt" | 100/6,32 = 15,8 | https://doanhnhan.baophapluat.vn/luat-bao-hiem-tien-gui-nam-2025-nhung-diem-moi-nguoi-gui-tien-can-quan-tam-add14ad3.html (13/09/2026) | OK-2 · TÍNH |
| 4 | Tiền gửi được bảo hiểm = tiền gửi bằng đồng Việt Nam của cá nhân (có kỳ hạn, không kỳ hạn, tiết kiệm, chứng chỉ tiền gửi) | Điều 17 Luật BHTG 2025 | nguồn #3 | OK-2 |
| 5 | Không được bảo hiểm: sở hữu > 5% vốn; người quản lý/điều hành; giấy tờ có giá vô danh (lời đọc chọn 3/5 nhóm) | | nguồn #3 | OK-2 |
| 6 | Ba trường hợp phát sinh nghĩa vụ trả; tối đa 45 ngày (cũ 60) | | nguồn #3 | OK-2 |
| 7 | Chi trả đặc biệt: Thống đốc có thể quyết định cao hơn hạn mức, tối đa bằng toàn bộ tiền gửi được bảo hiểm | | nguồn #3 | OK-2 |
| 8 | Luật mới: bỏ mức cố định trong luật, Thống đốc quyết định theo thời kỳ; không còn chờ tuyên bố phá sản | Luật 111/2025/QH15 | https://luatvietnam.vn/bao-hiem/luat-bao-hiem-tien-gui-2025-va-4-diem-moi-dang-chu-y-563-105890-article.html | OK-2 |
| 9 | "Luật mới có hiệu lực từ năm nay" | 01/05/2026 theo tóm tắt tìm kiếm (thuvienphapluat trả 403) | — | OK-2 (yếu: chưa mở được trang có ngày hiệu lực) |
| 10 | "Mỗi quý, các tổ chức đóng phí cho một quỹ dự phòng" | phí nộp trước ngày 20 tháng đầu quý sau | tóm tắt Luật 111/2025 (thuvienphapluat, kết quả tìm kiếm) + LuatVietnam nhắc "quỹ dự phòng nghiệp vụ" | OK-2 (yếu) |
| 11 | Lịch sử: 30 tr (1999) → 50 tr (2005) → 75 tr (05/08/2017, QĐ 21/2017) → 125 tr (2021) → 350 tr (2026); 50 tr giữ ~12 năm | | https://baophapluat.vn/han-muc-tra-tien-bao-hiem-cong-cu-huu-hieu-de-bao-ve-nguoi-gui-tien-post359929.html (24/08/2020) + nguồn #1 | OK-2 |
| 12 | 75 tr bảo vệ "khoảng 87%", 125 tr "hơn 92%" | 87,72% (Báo PL 2020; nguồn khác 87,32%) · "trên 92%" | nguồn #11 · https://div.gov.vn/han-muc-tra-tien-bao-hiem-cong-cu-toi-uu-bao-ve-quyen-loi-nguoi-gui-tien (12/09/2024) | OK-2 |
| 13 | 10/2022: tin đồn mạng xã hội, người dân xin rút trước hạn ở một ngân hàng TP.HCM; 10/10/2022 Thống đốc: tiền gửi "được nhà nước đảm bảo trong mọi trường hợp" | xếp hàng từ chiều 07/10 | https://daidoanket.vn/thong-doc-nhnn-moi-khoan-tien-gui-tai-ngan-hang-deu-duoc-nha-nuoc-dam-bao-10233840.html (10/10/2022 09:18) · VnEconomy 10/10/2022 (URL chứa tên ngân hàng → không đưa vào mô tả) | OK |
| 14 | "Dòng người dần thưa đi" | | thitruongtaichinhtiente.vn (tìm kiếm: "diễn biến tích cực … dần ổn định") | OK-2 (yếu: chưa mở bài) |
| 15 | Lãi 12 tháng đầu 10/2026 "từ gần sáu tới hơn bảy phần trăm" | nhóm thấp 5,9%, nhiều nơi ≥ 7%, cao 7,5% | https://tapchikinhtetaichinh.vn/lai-suat-ty-gia-hom-nay-lai-huy-dong-binh-quan-len-6-46-nam-usd-ngan-hang-giam-gia-169067.html (09/10/2026) | OK — lưu ý: NHNN yêu cầu giảm ≥ 0,5 điểm từ 19/10 → mức 7% của ví dụ là **giả định**, đã gắn nhãn |
| 16 | California 03/2023: 8/3 thông báo; 9/3 rút > 40 tỷ USD; dự kiến > 100 tỷ ngày 10/3; ≈ 85% tiền gửi; ~94% tiền gửi không được bảo hiểm cuối 2022 | | https://www.federalreserve.gov/publications/files/svb-review-20230428.pdf (trích chữ PDF) | OK |
| 17 | 10/3 đóng cửa; 12/3/2023 bảo đảm toàn bộ tiền gửi theo ngoại lệ rủi ro hệ thống; hạn mức 250.000 USD; cổ đông/người nắm nợ không được bảo vệ | | https://www.congress.gov/crs_external_products/IF/PDF/IF12378/IF12378.2.pdf + tóm tắt CRS IN12125 | OK (cổ đông/trái chủ: OK-2 qua tóm tắt CRS) |
| 18 | "Người gửi chủ yếu là công ty, quỹ đầu tư mạo hiểm" | "concentrated network of VC investors and technology firms" | nguồn #16 | OK |

## 2. Kênh tự tính (TÍNH — analysis.py, check.py OK)

1,2 tỷ − 350 = **850 tr**; − 125 = **1.075 tr** ("hơn một tỷ") · 350 × 1,07 = **374,5 tr** (+24,5) · 350 / 1,07 = **327,1 tr** · 300 tr cuộn 7%: 321 / 343,5 /
**367,5** (vượt ở năm 3; lời đọc "gần ba trăm bốn mươi bốn", "khoảng ba trăm sáu mươi tám") · 1.200 × 1,07 = 1.284 → ⌈1.284/350⌉ = **4 nơi** · vợ chồng mỗi
người một sổ: 700 tr · hạn mức quy về giá 2025 bằng CPI bình quân năm (World Bank WDI FP.CPI.TOTL, file `wb_cpi_index.json`, cập nhật 08/10/2026,
https://data.worldbank.org/indicator/FP.CPI.TOTL?locations=VN): 30 tr 1999 ≈ **120,2** · 50 tr 2005 ≈ **163,6** · 75 tr 2017 ≈ **95,7** · 125 tr 2021 ≈ **142,5**.

## 3. Suy luận & chỗ yếu (đã nói mềm trong lời đọc)

- **SUY:** "tiền gửi bằng đô la không nằm trong diện này" — suy từ định nghĩa Điều 17 (chỉ "bằng đồng Việt Nam"); "bảo hiểm nhân thọ, trái phiếu công ty,
  chứng chỉ quỹ bán ở quầy không phải tiền gửi" — suy từ định nghĩa, không có câu nguyên văn trong nguồn. Rủi ro thấp; luật sư duyệt nếu cần.
- **SUY:** "hạn mức tính cho mỗi tổ chức, không phải mỗi chi nhánh" — từ cụm "tại một tổ chức tham gia bảo hiểm tiền gửi"; chi nhánh là cùng pháp nhân.
- **SUY:** "nơi gửi có niêm yết là tổ chức tham gia bảo hiểm tiền gửi không?" — luật cũ bắt buộc niêm yết giấy chứng nhận; chưa mở điều tương ứng Luật 2025.
- **Yếu:** #9, #10, #14 chưa mở được trang gốc (thuvienphapluat 403). Trước dựng: mở toàn văn Luật 111/2025/QH15 (Điều 17, 18, 21, 22, 36, hiệu lực).
- **Luật cứng:** lời đọc không tên ngân hàng thương mại; "Ngân hàng Nhà nước", "Thống đốc" = cơ quan quản lý. Nguồn Fed có "svb" trong URL (chữ tắt), nhãn
  trong mô tả đã viết "một ngân hàng ở California". Nếu chủ kênh muốn tuyệt đối không chữ tắt tên ngân hàng trong mô tả → bỏ dòng nguồn Fed, giữ CRS.
- Không câu nào nói ngân hàng cụ thể nào yếu; câu "phần ngoài hạn mức không có nghĩa là mất trắng" tránh gây hoảng.

## Đối chiếu văn bản gốc 23/10

Văn bản gốc đã mở: **Luật 111/2025/QH15** bản ký số, Cổng TTĐT Chính phủ — https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/111-qh15-2025.signed.pdf
(bản quét 19 trang, đọc từng trang ảnh; trang mô tả https://vanban.chinhphu.vn/?classid=1&docid=216549&orggroupid=1&pageid=27160) · **Thông tư 05/2026/TT-NHNN**,
Công báo số 447 ngày 28/07/2026 — https://congbao.chinhphu.vn/van-ban/thong-tu-so-05-2026-tt-nhnn-470097/67202.htm · **Luật 06/2012/QH13** (luật cũ) —
https://vanban.chinhphu.vn/default.aspx?pageid=27160&docid=163543.

| Ý (lời đọc / màn hình / mô tả) | Kết luận | Văn bản gốc · trích ≤ 15 chữ |
|---|---|---|
| Hạn mức 350 triệu, gồm gốc và lãi, một người tại một tổ chức | **ĐÚNG** | TT 05/2026 Đ3: "(gồm cả tiền gốc và tiền lãi) của một người tại một tổ chức" |
| Hiệu lực hạn mức 13/07/2026 | **ĐÚNG** | TT 05/2026 Đ5: "có hiệu lực kể từ ngày 13 tháng 7 năm 2026" |
| Luật mới "có hiệu lực từ năm nay" | **ĐÚNG** | Luật 111 Đ40: "có hiệu lực thi hành từ ngày 01 tháng 5 năm 2026" |
| Thống đốc quyết định hạn mức theo từng thời kỳ (bỏ mức cố định) | **ĐÚNG** | Đ22.1: "quy định hạn mức chi trả tiền bảo hiểm trong từng thời kỳ" |
| Tiền gửi được bảo hiểm = VND của cá nhân: có kỳ hạn, không kỳ hạn, tiết kiệm, chứng chỉ tiền gửi | **ĐÚNG** | Đ17: "tiền gửi bằng đồng Việt Nam của cá nhân" |
| Không được bảo hiểm: sở hữu > 5% vốn; người quản lý, điều hành; giấy tờ có giá vô danh | **ĐÚNG** | Đ18.1, 18.2, 18.4: "Tiền mua các giấy tờ có giá vô danh" |
| "Mỗi quý ... đóng phí cho một quỹ dự phòng. Khi có chuyện, quỹ ấy đứng ra trả" | **LỆCH (nhẹ)** | Đ19.6 phí "nộp định kỳ hằng quý" cho tổ chức BHTG; Đ30.4c chênh lệch thu chi mới "trích lập vào quỹ dự phòng nghiệp vụ"; Đ38 trả từ quỹ ấy → **đã sửa**: "đóng phí bảo hiểm cho tổ chức bảo hiểm tiền gửi … tổ chức ấy trả từ quỹ dự phòng của mình" |
| Ba trường hợp phát sinh nghĩa vụ trả: (1) phương án phá sản được duyệt; (2) kiểm soát đặc biệt, lỗ > vốn + quỹ dự trữ, đình chỉ nhận tiền gửi | **ĐÚNG** | Đ21.1–21.2: "lỗ lũy kế lớn hơn 100% giá trị của vốn điều lệ" |
| (3) "khi Ngân hàng Nhà nước yêu cầu chi trả để giữ an toàn hệ thống" | **LỆCH** | Đ36.1: NHNN "báo cáo Chính phủ quyết định việc yêu cầu" trả → **đã sửa** lời đọc + màn hình: "Chính phủ quyết định yêu cầu chi trả" |
| "So với luật cũ, không phải chờ tới lúc có quyết định tuyên bố phá sản nữa" (lời đọc) + màn hình "KHÔNG CÒN PHẢI CHỜ TUYÊN BỐ PHÁ SẢN" | **LỆCH** | Luật 06/2012 Đ22 gốc: nghĩa vụ phát sinh khi NHNN "có văn bản chấm dứt kiểm soát đặc biệt" — luật cũ bản gốc cũng không đòi tuyên bố phá sản → **đã bỏ**; thay bằng "Mốc bắt đầu tính là lúc một trong ba điều ấy xảy ra" / "TÍNH TỪ LÚC PHÁT SINH NGHĨA VỤ TRẢ" |
| Tối đa 45 ngày, thay vì 60 ngày | **ĐÚNG** | Luật 111 Đ24.4: "Trong thời hạn tối đa 45 ngày"; Luật 06/2012 Đ23: "Trong thời hạn 60 ngày" |
| Chi trả đặc biệt: Thống đốc quyết định cao hơn hạn mức, tối đa toàn bộ tiền gửi được bảo hiểm | **ĐÚNG** (chỉ ở trường hợp 2, 3 của Đ21 — lời đọc đã nói "trường hợp đặc biệt", "từng trường hợp") | Đ22.2: "tối đa bằng toàn bộ các khoản tiền gửi được bảo hiểm" |
| Phần ngoài hạn mức "không có nghĩa là mất trắng … chờ xử lý tài sản" | **ĐÚNG** | Đ25: "được giải quyết trong quá trình xử lý tài sản" |
| Hạn mức tính cho mỗi người, mỗi tổ chức (không theo chi nhánh) | **ĐÚNG** (chi nhánh: suy từ "tại một tổ chức") | TT 05 Đ3 + Luật Đ23.1: "của một người tại một tổ chức tham gia" |
| Câu tự hỏi "nơi tôi gửi có niêm yết là tổ chức tham gia BHTG không?" | **ĐÚNG** | Đ16: công khai "tại tất cả các điểm giao dịch có nhận tiền gửi" |
| 93,68% người gửi được bảo vệ toàn bộ ở 350 triệu | **ĐÚNG** (trang của BHTGVN — cơ quan chính thức, không phải văn bản QPPL) | div.gov.vn 15/07/2026 (mục #1) |
| 125 triệu từ 2021 (QĐ 32/2021); lịch sử 30/50/75 triệu; 87% / 92% | **KHÔNG KIỂM ĐƯỢC** bản gốc QĐ 21/2017, 32/2021 trong phiên này (chỉ trang BHTGVN + Báo Pháp luật) | Giữ — số khớp trang chính thức BHTGVN; rủi ro thấp |
| Fed: 40 tỷ USD / 85% / 94% không được bảo hiểm | **ĐÚNG** (đã mở PDF Fed ở bản 1) | **Dòng nguồn Fed (URL chứa chữ tắt tên ngân hàng) đã bỏ khỏi mô tả**; giữ CRS; nhãn màn hình "BÁO CÁO CỦA FED 28/04/2023" không có tên ngân hàng |

Mô tả: nguồn LuatVietnam (thứ cấp) thay bằng 2 nguồn gốc (Công báo TT 05/2026, PDF Luật 111/2025); dòng `data_credit` ghi "văn bản gốc ở trên". Số không đổi →
analysis.py không cần chạy lại; check.py OK (12 phép); script_lines.py + studio_lint.py 0/0; soát neo cảnh 0 lỗi.
