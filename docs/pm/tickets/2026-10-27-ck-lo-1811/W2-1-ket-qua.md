# W2-1 — Kết quả dựng cảnh `ck-f1-tro-cap-that-nghiep`

## Đã làm

- Tạo `data/long/ck-f1-tro-cap-that-nghiep/gen_scenes.py`, giữ nguyên `script.md`.
- Sinh `spec.json` và cảnh cho đủ 7 chương `ch00`–`ch06`; có `chart_rules`, `say`, 6 ảnh AI `ai01`–`ai06`, HUD/chapter đầy đủ và mô tả CK có câu bắt buộc.
- Dựng 71 cảnh; biểu đồ thật là 40/71 cảnh (56%). Thẻ chữ là 4/71 cảnh (6%).
- Biểu đồ chính waterfall `13 triệu chi phí − 9 triệu trợ cấp = thiếu 4 triệu/tháng` xuất hiện tại CH00, CH01, CH02, CH03, CH04, CH05 và CH06. Đường thiếu cộng dồn bổ sung dần, đầy đủ 4→28 triệu tại CH06.
- Tải và dùng clip Pexels: 4068575, 8004282, 5434539, 7801968, 6443909, 8125994, 5439068, 8472464. Đã loại các clip phố có xe buýt, biển hiệu và áo có logo.

## Lệnh đã chạy và kết quả

- `python data/long/ck-f1-tro-cap-that-nghiep/gen_scenes.py` — sinh spec và 7 chương.
- `python motion/long/script_lines.py ck-f1-tro-cap-that-nghiep` — 153 câu, 2.351 âm tiết.
- `python motion/long/studio_lint.py ck-f1-tro-cap-that-nghiep --strict` — 0 lỗi, còn 7 cảnh báo nhịp câu ngắn theo luật studio (không sửa lời đọc đã duyệt).
- `python motion/long/build_long.py ck-f1-tro-cap-that-nghiep tts` — có timing cho đủ 7/7 chương.
- `python motion/long/build_long.py ck-f1-tro-cap-that-nghiep html` — 7/7 HTML, không Error.
- `python motion/long/clip_sheet.py ck-f1-tro-cap-that-nghiep` — đã mở và soi sheet.
- `python scripts/long_gate.py ck-f1-tro-cap-that-nghiep --min-syl 2200` — **ĐẠT**: 2.351 âm tiết, 10,5 phút, 71 cảnh, 8,9 giây/cảnh, 7 clip khác, 6 ảnh khác, 14 URL nguồn.

## Đường dẫn bàn giao

- Clip sheet: `output/long/ck-f1-tro-cap-that-nghiep/qa_clips.jpg`.
- HTML: `output/long/ck-f1-tro-cap-that-nghiep/ck-f1-tro-cap-that-nghiep_ch00.html` đến `..._ch06.html`.
- Thumbnail: không tạo, vì luật chung của W2 cấm chạy `thumb.py`.

## Kiểm chứng và lỗi còn lại

- Không có khẳng định nào chưa kiểm được; số liệu trong cảnh lấy từ `results.json`, các khẳng định đã có URL trong `factcheck.md`.
- Không có lỗi engine còn lại. Cảnh báo studio lint nêu trên là cảnh báo nhịp câu, không phải lỗi; lời đọc được giữ nguyên theo ticket.
