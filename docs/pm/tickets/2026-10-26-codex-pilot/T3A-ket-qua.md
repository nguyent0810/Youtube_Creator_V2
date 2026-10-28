# T3A — Kết quả nghiên cứu Katherine Johnson

Ngày thực hiện: 26/10/2026.

## Đã làm

- Đọc `AGENTS.md`, ticket T3A và bài mẫu `data/long/mim-turing-bombe/facts.md`.
- Tạo kho 36 dữ kiện tại `data/long/mim-katherine-johnson/facts.md`: 8 chương, mỗi chương 4–5 dòng (CH00: 5; CH01: 4; CH02: 4; CH03: 4; CH04: 4; CH05: 5; CH06: 5; CH07: 5). Có 34 dòng mạnh và 2 dòng vừa; mỗi dòng đều có URL đã mở và tên nguồn.
- Thêm 14 ảnh Commons/NASA đã ghi nguồn/giấy phép và 12 ứng viên B-roll Pexels có cảnh báo logo/chữ.
- Không viết `script.md`, không tạo `gen_scenes.py`/`ch*.json`, không TTS/HTML/render/thumbnail. Đây là ticket nghiên cứu nên đã bỏ qua `python scripts/long_gate.py mim-katherine-johnson --min-syl 1900` đúng yêu cầu ticket.

## Lệnh/kiểm tra đã chạy

- `Get-Content -Raw -Encoding utf8 data/long/mim-turing-bombe/facts.md` — đọc mẫu kho dữ kiện đạt chuẩn.
- Tìm trùng trong các Long và Short bằng `Select-String` trên `data/long/mim-*/script.md` và `data/stier/specs` — có kết quả bên dưới.
- Mở trực tiếp các nguồn NASA, Smithsonian, TIME, Wikimedia Commons, VOH và Pexels; không có lệnh lint/render vì ticket cấm pha dựng.

## Kiểm trùng bắt buộc

- `mim-ai-jobs` đã kể Dorothy Vaughan tới Langley tháng 12/1943, trở thành quản lý và chuyển sang lập trình FORTRAN năm 1958. Short `mim-dorothy-vaughan-fortran` cũng kể đúng tuyến này.
- `mim-ai-jobs` chỉ để Katherine Johnson trong ghi chú “đã cắt”, không phải tuyến lời đọc phát hành. Vì vậy bài mới có thể tập trung Johnson/Friendship 7 năm 1962 mà không lặp một đoạn Long đã kể.
- Kho dữ kiện chỉ cho nhắc Dorothy Vaughan một câu (vai trò ở West Area Computing); không khai thác FORTRAN, quản lý hay tuyến đời Vaughan.

## Mỏ neo phim

- Tựa Việt có nguồn đã mở: **Bộ Ba Ưu Việt** (*Hidden Figures*, 2016), nguồn [VOH](https://voh.com.vn/phim/phim-ve-nu-quyen-452430.html), mức vừa.
- NASA xác nhận cảnh Johnson chạy xa đến nhà vệ sinh tách biệt không xảy ra với chính bà; *TIME* ghi cú điện thoại sát giờ phóng đã được nén kịch tính. Các điểm này được đánh dấu trong kho để pha viết không lặp sai khác của phim.

## Khẳng định chưa kiểm được / cần tránh

- Model máy tính **IBM 7090**, giờ phóng cụ thể, thời gian Johnson kiểm tay và các con số sai số chưa có nguồn mạnh trực tiếp đã mở trong kho; không được tự điền.
- Không dùng cảnh nhà vệ sinh, cú điện thoại sát giờ phóng, nhân vật gộp hay chi tiết phim làm đời thật. Phim không được dùng hình/clip.

## Đề xuất cold open

“20 tháng 2 năm 1962. John Glenn sắp bay ba vòng quanh Trái Đất. Trước danh sách kiểm tra, ông muốn Katherine Johnson lấy đúng các phương trình máy IBM vừa chạy và kiểm lại bằng tay.” Sau đó hiện “Friendship 7 · 20/02/1962”, nêu 4 giờ 55 phút 23 giây, rồi quay về quá trình Johnson đi đến bàn tính ấy. Cấu trúc này bám nguồn NASA, có ngày và sức ép thật, không dùng câu meta hay tái hiện phim.

## Cổng/lint và đường dẫn hình

- Lỗi lint còn lại: không áp dụng — ticket nghiên cứu, không có kịch bản/spec/cảnh để lint.
- `long_gate.py`: không chạy — ticket ghi rõ bỏ qua với ticket nghiên cứu.
- Clip sheet: chưa có, vì ticket cấm dựng/tải/render clip.
- Thumbnail: chưa có, vì ticket cấm dựng thumbnail.
