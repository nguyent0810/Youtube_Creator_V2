# Kết quả T5R — nghiên cứu `mim-social-network`

## Đã làm

- Đã tạo kho dữ kiện tại `data/long/mim-social-network/facts.md`.
- Kho có 32 dữ kiện, chia đủ 8 chương (mỗi chương 4 dòng): 26 dòng **mạnh**, 6 dòng **vừa**.
- Đã ghi tên Việt của phim là **Mạng xã hội**, theo trang Netflix Việt Nam đã mở.
- Đã bổ sung 9 ảnh Commons chỉ có PD/CC0/CC BY; 10 clip Pexels ngang, có ghi chú rà logo/chữ; và 4 prompt ảnh AI theo đúng định dạng.

## Lệnh đã chạy và kết quả

- Đã đọc đúng phạm vi của ticket nghiên cứu: ticket, mục “Ảnh AI” của `docs/codex/long-rules.md`, và phần được chỉ định trong `data/long/mim-moneyball/facts.md`.
- Đã mở các URL nguồn trong kho bằng trình duyệt: The Harvard Crimson (2003, 2005, 2014), hồ sơ tòa Massachusetts và Ninth Circuit, Meta Newsroom, Netflix Việt Nam, Commons và Pexels.
- Không chạy lint, render, `script_lines.py`, `studio_lint.py` hoặc `python scripts/long_gate.py mim-social-network --min-syl 1900`: ticket xác định đây là **ticket nghiên cứu** và cấm các lệnh này.

## Điểm chưa kiểm được / không dùng làm khẳng định

- Không có nguồn đã mở đủ mạnh xác nhận Facemash dùng công thức Elo. Kho ghi rõ không được nói điều này như sự thật.
- Không có nguồn đã mở đủ mạnh để xác nhận các cảnh cụ thể trong phim: mở đầu với bạn gái, công thức Elo trên cửa sổ và các đối thoại cụ thể. Nếu bài viết sau cần nhắc, chỉ gọi đó là cảnh phim, không biến thành sự kiện đời thật.
- Các B-roll Pexels chưa tải và chưa lập clip sheet; pha dựng phải kiểm từng frame để loại logo/chữ.

## Đề xuất cold open

Mở bằng một mốc có nguồn mạnh: “Tối Chủ nhật 02/11/2003, một trang so hai ảnh sinh viên Harvard đã bị tắt. Trước đó, 450 người đã bấm hơn 22.000 lần.” Mốc 02/11 được suy ra từ bài *The Harvard Crimson* ngày 04/11/2003, bài này viết trang bị tắt vào tối Chủ nhật vừa qua. Sau cú móc này mới chuyển sang câu hỏi: từ thao tác chọn một trong hai ảnh, mạng xã hội đã tiến tới việc xếp thứ tự hàng nghìn bài đăng như thế nào?

## Câu hỏi còn bỏ ngỏ

- Có nguồn sơ cấp hoặc hồ sơ mã nguồn nào xác nhận chính xác thuật toán xếp hạng của Facemash không?
- Có nguồn mở đáng tin nào đối chiếu từng cảnh phim với sự kiện thật, đặc biệt cảnh đầu và chi tiết Elo, mà không cần dùng trích đoạn phim không?
