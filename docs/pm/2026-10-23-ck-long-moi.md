# CK — 4 Long mới cho 11/11, 13/11, 15/11, 16/11/2026 (bản 1, chờ chủ kênh duyệt)

Người viết: Claude, 23/10/2026. Bối cảnh: chủ kênh dồn lịch Long CK thành 4 Long/tuần (T2, T4, T6, CN 20:00 VN); Long đã hẹn hết vào 09/11. Báo cáo 22/10
(`docs/pm/2026-10-22-bao-cao-3-kenh.md`) cho thấy Long CK rất yếu: 106 view/28 ngày, 1,8 nghìn lượt hiển thị, CTR 1,6%, xem TB 3:10 — và đề xuất #6 "dừng Long
CK mới cho tới khi CTR > 3%". Chủ kênh đã quyết làm tiếp → bộ 4 bài này là **phép thử cơ chế mới**, không phải tăng sản lượng theo khuôn cũ.
**Chỉ viết file** (script, factcheck, chNN.json, gen_scenes.py, spec.json, analysis.py/check.py). Chưa dựng, chưa upload, không đụng state.sqlite.

## 1. Cơ chế chép (không chép bề mặt)

Theo `feedback-copy-mechanism-not-surface`: mỏ neo tự nhiên của khán giả CK là **số tiền của chính họ** + câu hỏi họ tự gõ có mốc thời gian. Bằng chứng
trên chính kênh (analytics 20/10): Short thắng là "tiền của một người qua thời gian" — `ck-lai-kep-lam-phat` 2.893 view, 49% ở lại; `ck-bao-hiem-350` 2.267
view, AVP 118%; `ck-vang-9-nam` 1.350, 49%; `ck-tiet-kiem-so-xanh` 1.288, 46%. Bài đọc thị trường chung thua (`ck-vnindex-mot-vong` 156, `ck-bitcoin-mat-nua`
196). Áp cho Long:
- **Tiêu đề** = câu người ta tự gõ + một con số tiền cụ thể (lương 25 triệu, 1,2 tỷ, 10 triệu năm 2016, 200 triệu) + mốc năm (2026, 2036, 2051).
- **Kể qua một nhân vật VÍ DỤ GIẢ ĐỊNH xuyên suốt** (chị Thu, anh Khang, chị Hạnh, anh Tuấn) **hoặc sự kiện có thật có ngày** (10/2022 tin đồn rút tiền ở
  một ngân hàng TP.HCM; 9–12/03/2023 một ngân hàng ở California; 2008 lạm phát 23%; Zimbabwe 2008–2009). Không bịa người thật, không tên ngân hàng.
- **Mỗi bài có một bảng / con số mang về** để người xem tự dò (bảng tra thuế E5; ba con số A2; ba câu tự hỏi ở mọi bài) — bản Long của "bảng tra tự dò".

## 2. Đo nhu cầu — 24 ứng viên đo, 12 ứng viên xét

Số liệu thô: `data/demand/CK-2026-10-23.json`. **Wikipedia** = lượt xem 12 tháng 10/2025–09/2026 (Wikimedia REST pageviews, user, all-access). **YT gợi ý** =
Google autocomplete `ds=yt`, hl=vi, gl=vn (câu người ta thật sự gõ; không phải lượng tìm). Hạn chế: Wikipedia tiếng Việt chỉ là chỉ báo tương đối (người Việt
tìm tài chính trên Google/YouTube nhiều hơn); Studio Research tab (quyết định #7 ngày 15/10) chưa kéo được trong phiên này.

| # | Ứng viên | Wikipedia vi 12 tháng | YT gợi ý (trích) | Bằng chứng kênh | Trùng? | Kết luận |
|---|---|---|---|---|---|---|
| 1 | **Lạm phát & sức mua của lương** | Lạm phát **13.546** · Chỉ số giá tiêu dùng **6.458** · Tiền lương 2.536 | "lạm phát 2025", "lạm phát ở việt nam", "lạm phát ở zimbabwe", "lương 10 triệu …" (6 gợi ý) | Short lãi kép–lạm phát **2.893** (top kênh) | B2 có đoạn "trừ lạm phát" cho tiền để dành; A1 về 5 kênh đầu tư → góc **lương** mới | **CHỌN (A2)** |
| 2 | **Bảo hiểm xã hội: rút một lần / lương hưu** | Bảo hiểm xã hội **4.467** (Lương hưu: không có bài) | "cách tính lương hưu năm 2026", "rút bảo hiểm xã hội một lần", "… bao lâu có tiền", "đóng BHXH tự nguyện bao nhiêu năm thì được hưởng lương hưu" | — | Không | **CHỌN (B5/E6)** |
| 3 | **Thuế thu nhập cá nhân 2026** | Thuế TNCN **2.520** · Thuế 8.160 | "thuế thu nhập cá nhân 2026", "tính thuế thu nhập cá nhân 2026", "giảm trừ gia cảnh …" | — | Không | **CHỌN (E5)** |
| 4 | **Bảo hiểm tiền gửi 350 triệu** | (không có bài riêng) · Ngân hàng 9.133 | "bảo hiểm tiền gửi", "ngân hàng phá sản thì người gửi tiền" | Short `ck-bao-hiem-350` **2.267 view, AVP 118%** | Chỉ trùng Short (Long nối Short thắng = mục đích) | **CHỌN (E4)** |
| 5 | Mô hình Ponzi / "lãi 2%/tháng" | Mô hình Ponzi **5.829** | "lừa đảo đầu tư tài chính", "… qua mạng", "mô hình ponzi" | Short "tiết kiệm nội bộ" 863 | Positioning D3 chưa làm | Dự phòng #1 (nhân vật: 100 triệu vào gói 2%/tháng; Madoff 11/12/2008) |
| 6 | Nghỉ hưu cần bao nhiêu tiền (quy tắc 4%) | en FIRE movement 158.122 · en Trinity study 45.162 (toàn cầu) | "cần bao nhiêu tiền để nghỉ hưu" (1 gợi ý) | — | Gần E6 | Dự phòng #2 (nhu cầu VN mỏng) |
| 7 | Bảo hiểm nhân thọ: huỷ năm thứ 3 mất bao nhiêu | 1.194 | "hủy hợp đồng bảo hiểm nhân thọ" (2 gợi ý) | — | Positioning B5 | Loại lần này (rủi ro pháp lý + tên doanh nghiệp) |
| 8 | Lương tối thiểu vùng 2026 | 510 | "lương tối thiểu vùng 2026" | — | Gộp vào A2 | Gộp |
| 9 | Vay tiêu dùng / app vay | Tín dụng đen 37 | gợi ý toàn tên app/công ty | — | Gần E3, B3 | Loại (tên thương hiệu) |
| 10 | Học phí đại học / nuôi con | Học phí 745 | gợi ý toàn tên trường | — | — | Loại |
| 11 | Tiền điện bậc thang | — | "tiền điện tăng", "tiền điện tháng 8" | — | — | Loại (ngoài tài chính cá nhân lõi, dễ dính tên doanh nghiệp) |
| 12 | Lãi suất / tiết kiệm | Lãi suất 2.848 · Tiết kiệm 1.387 · Lãi kép 3.421 | "gửi tiết kiệm mỗi tháng 1 triệu" | — | A1, B2, E1, E2 | Loại (đã có) |

Không trùng 12+ Long CK đã có (A1 kênh đầu tư 2026, B1 mua/thuê, B2 lãi kép, B3 trả góp 0%, B4 mua xe, C1–C5 chứng khoán, D1 vàng đỉnh, D2 FOMO, D3 lỗ không
dám bán, E1 mua đều, E2 quỹ khẩn cấp, E3 nợ thẻ) và 28 Short lô 4 (C2, E2, B1, B4, C3 — `docs/channels/chung-khoan/2026-10-20-lo4-shorts-plan.md`).

## 3. Bốn bài và lịch

Độ dài ước theo **tốc độ thật giọng CK**: đo trên `output/long/ck-*/chNN/timing.json` của 16 Long đã dựng = **200–226 âm tiết/phút** (đã gồm nghỉ; khuôn câu ngắn
E2/E3 ≈ 200). Ước = âm tiết ÷ 215…200 + ~0,5 phút (màn kết 20 s, thẻ chương).

| Ngày (20:00) | Thư mục | Tiêu đề chính | Âm tiết | Độ dài ước | Lộ trình | Neo |
|---|---|---|---|---|---|---|
| **T4 11/11** | `data/long/ck-e4-bao-hiem-tien-gui` | Ngân Hàng Phá Sản Thì Người Gửi Tiền Được Trả Bao Nhiêu? Phép Tính Với 1,2 Tỷ Tiết Kiệm | 2.777 | **13,5–14,5 phút** | Cảnh hẹn trước (chị Thu quay lại quầy với 4 cuốn sổ) | chị Thu 1,2 tỷ · 10/2022 · California 03/2023 |
| **T6 13/11** | `data/long/ck-e5-thue-tncn-2026` | Lương 25 Triệu Nộp Thuế Bao Nhiêu Năm 2026? Bảng Tra Thuế Thu Nhập Cá Nhân Mới | 2.605 | **12,5–13,5 phút** | Bảng tra hẹn trước + "đi cùng một đồng lương" | anh Khang: 3 phiếu lương 727,5k → 447,5k → 33,75k |
| **CN 15/11** | `data/long/ck-e6-luong-huu-rut-mot-lan` | Rút Bảo Hiểm Xã Hội Một Lần Được Bao Nhiêu? Đóng 10 Năm Lương 10 Triệu: 200 Triệu Hay Lương Hưu | 2.662 | **13–14 phút** | Bản đồ bằng hình: đường thẳng 2026 → 2051, ba ngã rẽ | chị Hạnh 200 tr vs 4,5 tr/tháng từ 2051 |
| **T2 16/11** | `data/long/ck-a2-luong-va-lam-phat` | Lương 10 Triệu Năm 2016 Bằng Bao Nhiêu Tiền Hôm Nay? Lạm Phát 10 Năm Và Lương Của Bạn Năm 2036 | 2.581 | **12,5–13,5 phút** | Nghịch lý / câu hỏi duy nhất | anh Tuấn 10 → 13 tr (sức mua −5,8%) · 2008 · Zimbabwe |

Mỗi thư mục có 2 tiêu đề phụ trong `spec.json → youtube.titles` để A/B. Thứ tự đặt bài có bằng chứng kênh mạnh nhất (bảo hiểm tiền gửi) lên đầu tuần.
Gợi ý Short nối (chưa viết, tuỳ chủ kênh): E4 "gốc cộng lãi: sổ 300 triệu tự vượt hạn mức năm thứ 3"; E5 bảng tra thuế dừng hình (khuôn bảng tra 20/10);
E6 "rút xong, đồng hồ năm đóng về số không"; A2 "lạm phát của bạn có thể là 6,6%".

## 4. Đã kiểm gì

- Mọi số tự tính có `analysis.py` → `results.json` và `check.py` tính lại bằng cách khác: E4 OK 12 phép · E5 OK 19 · E6 OK 36 · A2 OK 24.
- `motion/long/script_lines.py` (cổng integrity + chặn "trả lời ba câu hỏi") qua cả 4; `studio_lint.py` 0 lỗi 0 cảnh báo cả 4 (câu ≤ 35 tiếng, đủ câu ngắn,
  không liệt kê > 3 mục).
- Mô phỏng `build_long.plan()` với mốc thời gian giả (210 âm tiết/phút): mọi neo tìm được chữ, không cảnh quá ngắn, không sổ tràn, không tiêu đề biểu đồ đè,
  không mốc chưa đổi ra giây, không màn trống > 1 s.
- Quét mô tả: có câu "Nội dung giáo dục, không phải tư vấn đầu tư." cả 4; không `< >`, "CẦN KIỂM", "factcheck", "data/long"; lời đọc không tên ngân hàng, không
  "nên mua/bán/gửi/rút".

## 5. Nguồn yếu (chi tiết ở từng `factcheck.md`)

- **Văn bản luật gốc chưa mở được** (thuvienphapluat trả 403): Luật BHTG 111/2025 (ngày hiệu lực, Điều 17–18), Luật Thuế TNCN 109/2025 + NQ 110/2025, Luật
  BHXH 41/2024 (Điều 66 tỷ lệ nam, Điều 70–71, 23, 21), NĐ 176/2025 (mức trợ cấp hưu trí xã hội — lời đọc nói "mức đề xuất"). Các số đều khớp ≥ 1–2 nguồn
  thứ cấp (báo, trang luật, trang cơ quan). **Việc trước dựng: mở toàn văn từ Cổng TTĐT Chính phủ / Công báo.**
- E6: "rút xong thì thời gian đóng không tính lương hưu" chỉ có nguồn trang kế toán; "người hưởng lương hưu có thẻ BHYT do quỹ BHXH đóng" chưa mở nguồn.
- E4: "quỹ dự phòng, phí nộp mỗi quý" và "dòng người thưa đi" chỉ qua kết quả tìm kiếm; tỷ lệ 87% (2017) lệch giữa hai nguồn (87,72 / 87,32).
- A2: CPI bình quân năm lấy World Bank WDI (từ số liệu Cục Thống kê) — vài năm lệch ±0,1–0,2 điểm so số GSO công bố; năm 2026 tạm dùng bình quân 9 tháng.
- Lãi tiết kiệm đang giảm sau chỉ đạo 19/10 → mọi mức lãi trong E4/E6 đã ghi là giả định.

## 6. Rủi ro luật cứng CK

- **Tên ngân hàng:** lời đọc không có. E4 dùng "Ngân hàng Nhà nước/Thống đốc" (cơ quan quản lý) — cần chủ kênh xác nhận coi đây là cơ quan, không phải "tên
  ngân hàng". Nguồn Fed trong mô tả E4 có chữ tắt "svb" trong URL — nếu muốn tuyệt đối, bỏ dòng này (giữ CRS). Đã thay nguồn VnEconomy có tên ngân hàng trong
  đường dẫn bằng Đại Đoàn Kết.
- **Khuyến nghị:** E6 (rút hay không) và E5 (đăng ký người phụ thuộc cho ai) là hai chỗ dễ nghe như lời khuyên — kịch bản chỉ đặt phép tính cạnh nhau, có chương
  công bằng cho người đã rút, câu "không bảo bạn chia hay không chia".
- **Dự báo:** A2 chỉ dùng ba mức giả định 3/4/5% cho 2027–2036, nhãn "GIẢ ĐỊNH · KHÔNG PHẢI DỰ BÁO".
- **Tư vấn thuế/pháp lý:** E5, E6 gắn "không phải tư vấn thuế"/"kiểm tra với cơ quan BHXH"; quy định ghi "theo thời điểm 10/2026".

## 7. Chưa làm (bước dựng, theo quy trình)

`pexels.py get` cho id trong từng `gen_scenes.py` (đang dùng lại clip đã soát logo của Long CK trước — nên thay bớt để khỏi lặp diện mạo, `variety.py audit`),
`clip_sheet.py` + soát logo, thumbnail 3 bản, TTS/nghe thử ("phẩy", "Zimbabwe", "California"), `describe.py` kiểm ≤ 5.000 byte.
