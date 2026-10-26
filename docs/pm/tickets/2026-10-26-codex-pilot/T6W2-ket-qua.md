# Kết quả T6W2 — `mim-macintosh-1984`

## Đã làm

- Tạo `data/long/mim-macintosh-1984/gen_scenes.py`, `spec.json` và 8 file cảnh. Spec đặt lịch `2026-11-30T13:00:00Z`, có `SAY`, `youtube`, nguồn công khai, HUD/chapter đúng trường và mô-típ `ĐƯỜNG ĐI CỦA CÚ NHẤP`.
- Tạo `data/long/mim-macintosh-1984/ai_prompts.md`: 5 prompt AI. `ai_02` và `ai_04` là pixel art đơn sắc; dùng lần lượt ở CH01 và CH05/CH07.
- Tải và kiểm 6 clip Pexels: 3592341, 6803042, 4962316, 19205382, 4450059, 29542968. Đã mở clip sheet; các khung mẫu không thấy logo hoặc chữ đọc được.
- Vật nối chuột: CH00 `mouse1`, CH01 `mouse2`, CH02 `mouse1`, CH03 `mouse2`, CH04 `mouse1`, CH05 `ai04`, CH06 `mouse2`, CH07 `ai04`. Mỗi cảnh đặt đúng đoạn đang nói đến chuột/con trỏ.
- Không render, không tạo thumbnail, không upload, đúng yêu cầu ticket.

## Lệnh đã chạy và kết quả

- `python motion/long/script_lines.py mim-macintosh-1984`: 130 câu, 2.271 âm tiết.
- `python data/long/mim-macintosh-1984/gen_scenes.py --standin` → `script_lines.py` → `build_long.py ... tts` → `build_long.py ... html`: TTS đủ 8/8; HTML đủ 8/8, mỗi chương 10 cảnh tính cả thẻ chương.
- `python data/long/mim-macintosh-1984/gen_scenes.py` → `script_lines.py`: đã trả spec/cảnh về đường dẫn AI thật sau khi kiểm bằng stand-in.
- `python motion/long/clip_sheet.py mim-macintosh-1984`: đã tạo và đã mở để xem.
- `python scripts/long_gate.py mim-macintosh-1984 --min-syl 1900`: **ĐẠT** — 2.271 âm tiết, 10,8 phút, 72 cảnh, 9,0 giây/cảnh, 6 clip khác nhau, 13 ảnh khác nhau, 26 URL nguồn.

## Lỗi lint còn lại

`build_long.py ... html` không có Error, nhưng còn cảnh báo không chặn: dòng chữ lớn có thể chép nguyên lời đọc ở CH01, CH02, CH03, CH04, CH05, CH06 và CH07. Không còn lỗi chặn cổng.

## Kiểm chứng và tài sản chờ

- Không có khẳng định nào của lời đọc không kiểm được: toàn bộ số, ngày và tên dùng kho `facts.md` đã duyệt, với 26 URL công khai trong spec.
- Chờ chủ kênh tạo/import 5 ảnh AI: `ai_01.png` đến `ai_05.png`. Không gọi webhook tạo ảnh.
- Clip sheet: `output/long/mim-macintosh-1984/qa_clips.jpg`.
- Thumbnail: không tạo theo chỉ dẫn ticket (không chạy `thumb.py`).
