# Kết quả T2B — viết Long `mim-turing-bombe`

## Phạm vi đã hoàn tất

- Viết lại toàn bộ `data/long/mim-turing-bombe/script.md`: 8 chương, 138 câu, 2.170 âm tiết. Trục kể là bức thư ngày 21/10/1941 → khóa đổi mỗi ngày → nền móng Ba Lan → crib/menu → Bombe loại giả thuyết → người vận hành/kiểm tra → lớp phim ảnh.
- Viết lại `factcheck.md` với nguồn đã mở cho mọi khẳng định có tên, số hoặc ngày trong lời đọc. Có 20 URL nguồn được gate đếm. Chi tiết mức vừa về The Imitation Game được nói dưới dạng “theo Time”; không đọc Victory tháng 03/1940, ngày 18/03 hay các chi tiết Doc Keen chưa kiểm được.
- Viết lại `gen_scenes.py`, sinh `spec.json` và `ch00.json` đến `ch07.json`: 80 cảnh tổng (72 cảnh nội dung), 9 cảnh nội dung/chương, nhiều hơn 5 loại cảnh/chương. Counter 159 và 211 đều khai `year: false`; các năm ở date/timeline không dùng counter.
- Tiêu đề chính: `NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing: Bombe` — đúng 60 ký tự. Mô tả công khai đã soát không có từ cấm.
- Đã dựng TTS và HTML; không render video, không tạo thumbnail, không chạy `thumb.py`, đúng giới hạn ticket.

## Cổng và lệnh đã chạy

| Lệnh | Kết quả |
|---|---|
| `python motion/long/script_lines.py mim-turing-bombe` | Qua integrity; 138 câu, 2.170 âm tiết. |
| `python data/long/mim-turing-bombe/gen_scenes.py` | Sinh `spec.json` và 8 chương cảnh. |
| `python motion/long/studio_lint.py mim-turing-bombe --strict` | 0 lỗi, 8 cảnh báo mật độ câu ngắn. Không thêm câu đệm để triệt cảnh báo. |
| `python motion/long/build_long.py mim-turing-bombe tts` | Hoàn tất timing/TTS cho 8 chương, tổng khoảng 10,1 phút. |
| `python motion/long/build_long.py mim-turing-bombe html ch00 ch01 ch02 ch03 ch04 ch05 ch06 ch07` | Hoàn tất HTML cho 8 chương; mỗi chương 10 cảnh và 1 clip. |
| `python motion/long/clip_sheet.py mim-turing-bombe` | Đã tạo và soi trực quan clip sheet. |
| `python scripts/long_gate.py mim-turing-bombe --min-syl 1900` | **ĐẠT** — 2.170 âm tiết; 10,1 phút; 72 cảnh nội dung; 8,4 giây/cảnh; 6 clip khác; 11 ảnh khác; 20 URL nguồn. |

Ghi chú harness HyperFrames: lệnh usage của skill đã thử nhưng npm cache của máy báo `EPERM`; workflow bắt buộc của repo qua `build_long.py` vẫn hoàn tất HTML bình thường. Đây không phải lỗi nội dung hay lỗi dựng HTML.

## Media đã dùng và đã soát

Ảnh Commons trong `facts.md`: I01–I05, I09–I11 là Public domain; I06–I08 là CC0. Tổng 11 ảnh khác, không dùng CC BY-SA/GFDL/NC/ND.

Clip Pexels Free đã dùng (không gắn danh tính người thật):

- `34645486` — minh họa mạch điện trừu tượng, dùng 2 lần.
- `2915385` — đường chân trời biển, dùng 2 lần.
- `31802320` — bánh răng cơ khí, dùng 1 lần.
- `34187599` — máy đánh chữ, dùng 1 lần.
- `8334262` — sóng biển nhìn từ trên cao, dùng 1 lần.
- `6079428` — bó dây điện, dùng 1 lần.

Lần soi đầu đã loại ba clip có giấy tờ chữ đọc được hoặc nhãn radio “ZENITH / STEREOPHONIC”. Clip sheet cuối không thấy logo, mã hay chữ đọc được.

## Đường dẫn QA

- Clip sheet: `output/long/mim-turing-bombe/qa_clips.jpg`
- Thumbnail: không tạo theo yêu cầu ticket; không có đường dẫn thumbnail.

## Lỗi/cảnh báo và điều chưa kiểm được

- Không còn lỗi lint chặn. Studio lint còn 8 cảnh báo về tỷ lệ câu ngắn; các câu không bị rút ngắn bằng câu đệm, để giữ mạch dữ kiện và mức 2.170 âm tiết.
- Không khẳng định Victory tháng 03/1940, ngày 18/03, thông số cơ khí/Doc Keen, ví dụ crib cụ thể chưa có nguồn mạnh, hay tác động định lượng U-boat. Những giới hạn này đã được ghi rõ trong `factcheck.md`.
- Không render/final, upload hay thao tác YouTube.
