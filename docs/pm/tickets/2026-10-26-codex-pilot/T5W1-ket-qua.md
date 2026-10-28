# Kết quả T5W1 — mim-social-network

## Đã thực hiện

- Viết `data/long/mim-social-network/script.md` gồm 8 chương, tiêu đề `THE SOCIAL NETWORK Ngoài Đời Thật: Facemash 2003` (một dấu `:`, 54 ký tự).
- Viết `data/long/mim-social-network/factcheck.md` với 15 URL công khai, chỉ dùng kho dữ kiện đã duyệt.
- Mô-típ: **bản đồ kết nối**. Mỗi chương thêm một ghim: trang so cặp ảnh; cánh cửa kỷ luật; địa chỉ `harvard.edu`; Coursematch; vai trò đầu tiên; hồ sơ tòa; nhãn phim; Feed.
- Không dùng Elo như sự kiện thật: chỉ gọi nó là cảnh phim và nêu rõ kho nguồn không xác nhận Facemash dùng Elo.

## Dữ kiện theo chương

| Chương | Dữ kiện đã dùng |
|---|---|
| CH00 | Crimson 04/11/2003; Facemash; House facebooks; 450 khách; ít nhất 22.000 phiếu; giới hạn kiểm chứng Elo |
| CH01 | hơn 20.000 lượt trong 24 giờ; Administrative Board; hồ sơ tố tụng 2024; phát biểu về phần khoa học máy tính |
| CH02 | danh bạ Harvard; 04/02/2004; Kirkland House; `harvard.edu`; 650 đăng ký; 4.300 tài khoản |
| CH03 | tháng 03/2004; Columbia, Stanford, Yale; 10.000; Coursematch; tháng 05/2004 gần 100.000; tháng 06/2004 đổi tên |
| CH04 | Eduardo Saverin; CFO; đầu tư, quảng cáo; Palo Alto tháng 06/2004; giới hạn không suy diễn động cơ |
| CH05 | Cameron Winklevoss, Tyler Winklevoss, Divya Narendra; cáo buộc; phán quyết 2011; 22/02/2008; 20 triệu USD; hơn một triệu cổ phiếu; xấp xỉ 65 triệu USD |
| CH06 | phim năm 2010; David Fincher; Andrew Garfield; Jesse Eisenberg; ranh giới giữa phim và hồ sơ |
| CH07 | Feed; Meta 2018; inventory, signals, predictions, relevancy score; khoảng 3.000 bài và 300 bài |

## Lệnh đã chạy

1. `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py mim-social-network`
   - Integrity qua; tổng **116 câu, 2.262 âm tiết**, trong giới hạn ticket 2.000–2.300.
2. `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py mim-social-network --strict`
   - **0 lỗi, 9 cảnh báo**. Cảnh báo còn lại: mật độ câu ngắn ở các chương và một câu CH07 bị nhận là liệt kê nhiều mục. Đây là cảnh báo, không phải lỗi strict.
3. `PYTHONIOENCODING=utf-8 python scripts/long_gate.py mim-social-network --min-syl 1900`
   - **TRƯỢT, 21 lỗi**. Cổng xác nhận 2.262 âm tiết và 15 URL, nhưng yêu cầu các phần ngoài phạm vi ticket: `hud` và ≥5 loại cảnh cho từng `chNN.json`, timing TTS, `spec.youtube` với `publish_at`, `playlist`, `chapter_titles`, `tags`, `video_credits`, ít nhất 8 `spec.youtube.sources`, cùng bảng `say`.

## Vướng mắc phạm vi

Ticket chỉ cho phép ghi ba file: `script.md`, `factcheck.md` và báo cáo này; đồng thời chỉ định `script_lines.py` được tạo thêm `chNN.json` có `lines`.

Để `long_gate.py` in **ĐẠT**, phải tạo cảnh, `spec.json` và timing TTS qua các file/lệnh không được ticket cho phép ghi hoặc đọc. Vì vậy không thể báo hoàn thành cổng cuối mà không vi phạm phạm vi ticket.

## Khẳng định không kiểm được

- Không có nguồn mạnh trong kho xác nhận Facemash dùng Elo, cảnh mở đầu với bạn gái, hoặc các đối thoại cụ thể của phim. Kịch bản không trình bày các chi tiết này là sự kiện thật.

## Clip sheet và thumbnail

- Không tạo clip sheet hoặc thumbnail: không thuộc ba file được phép của ticket.
