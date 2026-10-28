# Báo cáo T6W1 — mim-macintosh-1984

## Đã thực hiện

- Viết `data/long/mim-macintosh-1984/script.md`: 8 chương, tiêu đề `STEVE JOBS 1984: Macintosh biết nói bằng hình` (45 ký tự, một dấu hai chấm).
- Viết `data/long/mim-macintosh-1984/factcheck.md`: đối chiếu các mốc, số liệu, tên riêng và nhận định quy dẫn với 26 URL công khai từ kho dữ kiện đã duyệt.
- Chạy `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py mim-macintosh-1984` hai lần cuối: tổng 2.271 âm tiết; CH00 201 âm tiết.
- Chạy `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py mim-macintosh-1984 --strict`: **0 lỗi**, 7 cảnh báo phong cách về mật độ câu ngắn và một câu liệt kê ở CH00.
- Chạy `PYTHONIOENCODING=utf-8 python scripts/long_gate.py mim-macintosh-1984 --min-syl 1900`: **TRƯỢT, 21 lỗi**.

## Hook và cấu trúc

- Mở đầu CH00 nêu đúng mốc `24 tháng 01 năm 1984` và lời hứa cụ thể về chuột một nút.
- Câu trả một phần lời hứa nằm ở CH00, dòng 7 của `script.md`: Macintosh có phần trình diễn tự giới thiệu trong ngày ra mắt.
- Lộ trình: PARC → bộ nhớ 128K → Super Bowl → sân khấu 24/01 → chuột/giao diện → phim *Steve Jobs* → di sản.
- Câu hỏi treo ở cuối CH00: vì sao ý tưởng đã được thấy từ năm 1979 vẫn thành bước ngoặt ở năm 1984.
- Vật nối “chuột một nút” xuất hiện ở CH00, CH01, CH02, CH03, CH04, CH05, CH06 và CH07.

## Không kiểm được / giới hạn

- Không có khẳng định nào dùng ngoài kho dữ kiện đã duyệt. Các nhận định nguồn xếp mức “vừa” đều đọc với quy dẫn rõ (Computer History Museum, Smithsonian, Netflix Việt Nam, TIME hoặc lời Sorkin).
- Không tạo hoặc gọi ảnh AI, không dùng tư liệu phim.

## Blocker cổng tổng

Ticket chỉ cho phép ghi ba file: `script.md`, `factcheck.md`, và báo cáo này. Sau `script_lines.py`, các `chNN.json` chỉ có lời đọc; chưa có cảnh, `hud`, `spec.youtube`, `say`, hoặc timing TTS.

Vì vậy `long_gate.py` báo thiếu HUD và tối thiểu 5 loại cảnh tại cả 8 chương, thiếu TTS cho CH00–CH07, cảnh trung bình 648,9 giây, và thiếu các trường `spec.youtube` (`publish_at`, `playlist`, `chapter_titles`, `tags`, `video_credits`, `sources`, `say`). Các artefact cần để sửa nằm ngoài danh sách “Chỉ ghi” của ticket; không tự ý tạo `gen_scenes.py`, `spec.json` hay chạy TTS/render.

Không có clip sheet hoặc thumbnail trong ticket W1 này; chưa tạo.
