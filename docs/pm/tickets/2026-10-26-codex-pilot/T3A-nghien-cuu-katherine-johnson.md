# T3A — NGHIÊN CỨU: kho dữ kiện cho Long `mim-katherine-johnson`

**Ticket nghiên cứu.** Không viết kịch bản, không tạo `gen_scenes.py`/`ch*.json`, không render. Bỏ qua yêu cầu chạy `long_gate.py`.

| Mục | Giá trị |
|---|---|
| Đọc trước | `AGENTS.md` (nhất là "Cổng chất lượng" và "Lỗi đã gặp"); bài mẫu `data/long/mim-turing-bombe/facts.md` (kho dữ kiện đạt chuẩn) |
| Đầu ra | `data/long/mim-katherine-johnson/facts.md` |
| Báo cáo | `docs/pm/tickets/2026-10-26-codex-pilot/T3A-ket-qua.md` |

## Đề tài

- **Mỏ neo:** phim *Hidden Figures* (2016).
  - Tìm tên chiếu ở Việt Nam qua nguồn mở được.
  - Phim chỉ nhắc bằng lời và chữ, không dùng hình phim.
- **Người thật:** Katherine Johnson (NASA Langley).
- **Mốc trung tâm:**
  - Chuyến bay Friendship 7 của John Glenn, 20/02/1962.
  - Glenn yêu cầu Johnson kiểm tay quỹ đạo do máy IBM tính. Chỉ dùng câu nói nổi tiếng nếu có nguồn mạnh như NASA, và ghi rõ là lời kể lại.
- **Lịch:** Long 9–11 phút, đăng thứ Tư 25/11/2026 lúc 20:00 VN (`2026-11-25T13:00:00Z`).

## Kiểm trùng (bắt buộc)

Long `mim-ai-jobs` và Short `mim-dorothy-vaughan-fortran` đã kể Dorothy Vaughan và FORTRAN.

1. Grep `data/long/mim-*/script.md` và `data/stier/specs/*` để biết đã kể gì.
2. Bài này xoay quanh **Johnson và chuyến bay 1962**. Vaughan chỉ được nhắc tối đa một câu.
3. Ghi kết quả kiểm trùng vào báo cáo.

## Cần gom

- **Số dữ kiện:** tối thiểu **30**, chia cho 8 chương, mỗi chương 3–5 dữ kiện.
- **Mỗi dòng gồm:**
  - khẳng định;
  - ít nhất một số, ngày, tên hoặc vật cụ thể;
  - URL đã mở, kèm tên trang;
  - độ tin: **mạnh** (NASA, Smithsonian, Lưu trữ quốc gia, đại học, sách) hoặc **vừa**.
- **Nhóm nên đào:**
  - Tuổi thơ và học vấn của Johnson: West Virginia, vào đại học sớm.
  - Năm vào NACA Langley và nhóm West Area Computers.
  - Phân biệt chủng tộc thời đó: chỉ dùng chi tiết có nguồn mạnh, đừng lấy từ phim.
  - Việc Johnson tính quỹ đạo cho Alan Shepard (1961).
  - Friendship 7: ngày bay, số vòng quanh Trái Đất, máy IBM 7090, lời đề nghị của Glenn.
  - Apollo 11: các tính toán liên quan.
  - Huân chương Tự do Tổng thống năm 2015.
  - Toà nhà mang tên bà.
  - Phim khác đời thật ở đâu: chỉ dùng nguồn bình luận đáng tin, và gắn mức "vừa" nếu nguồn chỉ là báo.
- **Ảnh và B-roll** (ghi ở cuối file `facts.md`):
  - 12–15 ảnh Commons hoặc NASA. Ảnh NASA thường là PD; vẫn kiểm `LicenseShortName` trên Commons.
  - 10–15 clip Pexels trung tính (bầu trời đêm, tên lửa phóng không logo, giấy tính toán, bút chì, máy tính cổ, bảng đen), mỗi clip ghi chú "không logo/chữ".

## Báo cáo

- Số dữ kiện theo chương (mạnh/vừa).
- Kết quả kiểm trùng.
- Tên phim ở Việt Nam, kèm nguồn.
- Câu hỏi còn bỏ ngỏ.
- Đề xuất cold open có ngày giờ (từ dữ kiện mạnh nhất).
