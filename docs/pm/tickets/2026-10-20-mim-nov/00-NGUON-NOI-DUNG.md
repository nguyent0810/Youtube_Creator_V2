# MIM — nguồn nội dung 13/11 → 10/12/2026 (bản 1, chờ chủ kênh duyệt)

Người lập: Claude, 20/10/2026. Phạm vi chủ kênh chọn ngày 20/10: lấp khoảng trống của MIM (Short từ 13/11, Long sau 03/12), theo kế hoạch YPP, đăng **riêng tư + hẹn giờ**.

## 1. Khoảng trống đo được (state.sqlite, 20/10)

| Loại | Đã hẹn tới | Khoảng trống |
|---|---|---|
| Short MIM | 12/11 (5/ngày) | **13/11 trở đi: 0 bài** |
| Long MIM | 03/12 (T2 + T5 20:00) | **07/12, 10/12 trở đi: 0 bài**; chưa có bản 20–30 phút |
| Short CK | 31/10–14/11 đang dựng (lô 4, agent khác) | ngoài phạm vi |

## 2. Luật áp cho cả đợt

- **Kế hoạch YPP (15/10):** MIM dẫn đầu; Short **2/ngày**, mỗi Short gắn một Long đã hẹn (teaser/phễu); công sức dồn cho Long. Long: 2 bản/tuần, một 9–12 phút + một 20–30 phút, **không Long nào dưới 8 phút**.
- **Mục tiêu % ở lại ≥ 45%** (engagedViews/views). Mở bằng **con số hoặc sự kiện có ngày**, tránh khung "mẹo", câu chốt quay lại ý mở. Số liệu tuần 12–18/10: MIM trung vị 28%; series QR/Flappy/"mẹo" chỉ 11–29%.
- **Chuẩn Short v3 đã duyệt:** chạy mix lint, giọng Thanh Bình/Ngọc Huyền, nhạc nền nhỏ; làm **một bài mẫu cho chủ kênh duyệt trước** khi làm hàng loạt. Câu mở ≤ 9 chữ, một insight, không câu hỏi cuối, không mời xem Long trong lời đọc (nối bằng "Video liên quan" + link mô tả).
- **Không dùng** mở bài "trả lời ba câu hỏi"; mỗi Long đổi dạng lộ trình.
- **Chống trùng:** MIM đã có ~60 Short về Watson, poker, Deep Blue, QWERTY, CAPTCHA. Mỗi ticket Short phải đối chiếu `state.sqlite` (kind='short', channel='MIM') + `data/long/*/script.md` và **không lặp góc đã dùng**.
- **Nguồn:** mọi con số lấy từ `data/long/<chủ đề>/script.md` + `factcheck.md` đã kiểm chứng, hoặc nguồn sơ cấp có URL. Chỗ chưa kiểm ghi "cần kiểm", không bịa.
- **Chống nhàm khuôn (YPP "inauthentic content"):** mỗi Short đổi thứ tự và loại cảnh so với bài kề.
- **Clip:** chạy `motion/long/clip_sheet.py` trước khi dựng; clip không có logo, ticker, tên công ty.
- **Dựng:** không dựng bản nháp (Tạo → Đăng → Retro). **Chỉ một tiến trình dựng tại một thời điểm** (khoá `output/.render.who`; hiện agent khác đang dựng lô CK). Chạy nền qua `scripts/run_chain.py`, không sửa `.sh` đang chạy.
- **Hạn upload:** MIM chưa bị trần; CK thì có (ngoài phạm vi).

## 3. Chia việc

Hai pha, có cổng duyệt của Claude giữa hai pha.

**Pha 1 — chỉ viết, không dựng, không đăng** (các ticket chạy song song được vì chỉ ghi file docs/spec riêng):

| Ticket | Việc | Đầu ra |
|---|---|---|
| T1 | Chọn chủ đề Long mới (đối chiếu nhu cầu, trùng, nguồn) | `T1-ket-qua.md`: 2 chủ đề + lý do + danh sách nguồn |
| T2 | Long 20–30 phút (hẹn T2 07/12 20:00) | thư mục `data/long/<slug>/` đủ script/factcheck/chNN/spec — **sau khi T1 xong** |
| T3 | Long 9–12 phút (hẹn T5 10/12 20:00) | như T2 — **sau khi T1 xong** |
| T4–T9 | Short theo Long (xem bảng dưới) | `T<n>-ke-hoach.md` + spec từng Short |

**Pha 2 — sau khi Claude duyệt pha 1:** dựng (nối tiếp, một tiến trình), kiểm bảng clip và bản cuối, đăng riêng tư + hẹn giờ, retro bằng subagent.

## 4. Lịch Short (2/ngày, 13/11 → 03/12, 42 bài)

Giờ lấy từ `scripts/shorts_grid.py` / `data/shorts_slots.json`, không tự đặt. Mỗi Short gắn Long còn **phía sau** nó trong lịch (Short nhử Long sắp lên).

| Ticket | Long gắn | Ngày Long | Số Short | Khoảng ngày Short |
|---|---|---|---|---|
| T4 | `mim-ai-gpu` | 16/11 | 8 | 13/11–16/11 và rải thêm |
| T5 | `mim-watson-jeopardy` | 19/11 | 5 | 17/11–19/11 |
| T6 | `mim-ai-chat-privacy` | 23/11 | 8 | 20/11–23/11 |
| T7 | `mim-may-thang-poker` | 26/11 | 5 | 24/11–26/11 |
| T8 | `mim-ai-khuon-mat` | 30/11 | 8 | 27/11–30/11 |
| T9 | `mim-may-choi-game` | 03/12 | 8 | 01/12–03/12 |

Ticket T5, T7 ít bài vì Watson/poker đã có rất nhiều Short; nếu không đủ góc mới thì **báo thiếu, không độn**. Phần thiếu chuyển sang T4/T6/T8/T9.

## 5. Tiêu chí duyệt (Claude làm ở cổng giữa hai pha)

1. Không trùng góc với Short hiện có; không trùng giữa các ticket.
2. Mỗi con số có nguồn trong script đã kiểm chứng.
3. 60% bài theo khuôn đã thắng (số/sự kiện có ngày), 40% bài thử; có bảng tra tự dò nếu hợp.
4. Long: đủ độ dài, không độn, có factcheck; Short: đúng 8 quy tắc.
5. Lịch không đè Long, không quá 2 Short/ngày.
