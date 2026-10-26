# Kế hoạch trình duyệt — 40 Short MIM khung truyện + 2 Long (bản 1, 20/10/2026)

Trạng thái: pha 1 xong (chỉ viết file). **Chưa dựng, chưa đăng.** Bài mẫu đã duyệt: `mim-nvidia-quan-an-dem` (13/11 19:00, đã dựng, nằm trong `data/stier/specs`).

## 1. Kiểm tự động của Claude (gộp 40 spec)
- 40 spec = T4 7, T5 5, T6 8, T7 4, T8 8, T9 8; không trùng slug với nhau và với `state.sqlite` (kênh MIM).
- Tất cả theme `mim`, `mix` bật; lời đọc không chữ số ngoài năm (giống bài mẫu đã duyệt); không bài nào kết bằng câu hỏi; câu mở ≤ 9 âm tiết.
- Số cảnh 7–10 (mục tiêu 9–13): **mềm hơn khuôn thắng**; riêng T8 `deepface`, `facebook-xoa` chỉ 7 cảnh.
- Lời đọc 91–135 từ; bài ≥ 130 từ (T4, T7, T9) có nguy cơ vượt 35 giây khi đọc thật — đo sau TTS, cắt câu phụ nếu cần.
- **17 clip Pexels bị dùng lặp 2–4 lần giữa các bài** (đặc biệt 8889195 và 8561462 ×4, 6651626 ×3, 17518183 ×3, 8091712 ×3): phải đổi để chống nhàm khuôn ở pha 2.
- Chưa kiểm được: thời lượng TTS thật, layout, hình clip (chưa ai xem khung nào), cách đọc tên riêng.

## 2. Việc cần chủ kênh quyết (khuyến nghị của Claude ghi sau mỗi mục)
1. **Long đã hẹn có lỗi sự kiện** (chưa sửa gì): Samsung/The Register/Stuckey trong `mim-ai-chat-privacy`; Lý Phi Phi 2006 trong `mim-ai-gpu`; CH20 "42.729 ván, 99,4%" trong `mim-may-choi-game`. Theo quy tắc "chỉ thay video đã upload khi sai làm đổi nghĩa": cần kiểm trạng thái upload thật rồi quyết từng cái. Khuyến nghị: sửa mô tả/ghim bình luận nếu đủ, chỉ thay video khi chủ kênh đồng ý.
2. **Short cũ `mim-claudico-thua-2015`** viết "con người thắng" nhưng nguồn CMU là hoà thống kê. Đã hẹn giờ. Khuyến nghị: thay.
3. **T7 bài Ferguson:** Chris Ferguson từng dính tranh cãi Full Tilt (từ trí nhớ agent, chưa kiểm). Khuyến nghị: đổi sang Elias (dự phòng có sẵn). **ĐÃ ÁP DỤNG 20/10:** S2 thành `mim-elias-bai-toan-to-bip` (Elias).
4. **T7 bài Sandholm** nêu tên hai bệnh nhân từ thông cáo CMU. Khuyến nghị: ẩn danh ("một người đàn ông ở St. Louis"). **ĐÃ ÁP DỤNG 20/10:** hai bệnh nhân ẩn danh.
5. **T4 bài Mona Lisa 2008** yếu (không có xung đột thật, số lệch nguồn 80 ms vs 275 ms) và bài Việt Nam yếu. Khuyến nghị: thay Mona Lisa bằng dự phòng. **ĐÃ ÁP DỤNG 20/10:** thay bằng `mim-patrascu-card-game-2009` (Relu Patrascu, Toronto 2009), giữ slot 18/11 11:30.
6. **T4 bài 3** ghép hai thí nghiệm khác nhau (Google 16.000 lõi vs 3 máy Stanford) với ghi chú "cùng cỡ mạng chừng một tỉ". Khuyến nghị: giữ chỉ khi kiểm được NYT/Google gốc.

## 3. Nguồn còn phải kiểm trước pha 2 (chung)
openai.com (403), Fast Company, Garante, NYT Magazine, Wired gốc, Meta 2021, DeepFace 97,53%, điều khoản thoả thuận Williams, NYT 25/06/2012, giá DGX-1 129.000 đô, ngày Jensen ở Hà Nội. Quy tắc: không kiểm được thì bỏ câu đó hoặc dùng bài dự phòng — không đưa vào video.

## 4. Pha 2 (khi chủ kênh duyệt)
1. Chốt lịch giờ bằng `scripts/shorts_grid.py`; đổi clip lặp; soát tay 3 khung mỗi clip.
2. Dựng nối tiếp từng bài (khoá render), kiểm bảng khung, nghe thử `say`.
3. **Kênh MIM có `upload=manual`** (xuất gói bằng `export_manual.py`): xác nhận cách đăng thật trước khi hứa đăng tự động. Đăng riêng tư + hẹn giờ.
4. Long T2 (Dịch máy, 07/12) và T3 (Apollo 1202, 10/12): dựng sau khi 40 Short xong hoặc song song nếu máy rảnh; riêng T2 cần tư liệu hình có người.
5. Retro bằng subagent sau mỗi đợt đăng; đo "ở lại xem" theo lane, dừng lane dưới 25% sau 6 bài.
