# W2-4 — Kết quả dựng cảnh `ck-f4-vo-chong-chia-tien`

## Đã làm

- Tạo `data/long/ck-f4-vo-chong-chia-tien/gen_scenes.py` và sinh `spec.json` cùng cảnh cho đủ 7 chương.
- Giữ nguyên lời đọc. `script_lines.py` ghi nhận 2.621 âm tiết, thời lượng TTS 11,82 phút.
- Dùng số trong `results.json`; biểu đồ chính B6 (cột xếp chồng) xuất hiện ở CH00, CH01, CH02, CH03, CH04, CH05 và CH06, mỗi lần có tiêu đề/ngữ cảnh riêng.
- Có 79 cảnh: 31 cảnh biểu đồ (39,2%) và 10 thẻ chữ/hỏi (12,7%).
- Dùng 6 ảnh AI `ai01`–`ai06`, có `credit: false`, nhãn ẢNH MINH HỌA, focus mặt và chuyển động xen kẽ.
- Tải và rà clip; loại rocket, bảng công thức/chữ đọc được, tiền mặt lộ mệnh giá và clip có logo. Bản cuối dùng 15 clip khác nhau, mỗi clip không quá 2 lần.

## Lệnh và kết quả

- `python motion/long/script_lines.py ck-f4-vo-chong-chia-tien` — 2.621 âm tiết.
- `python motion/long/studio_lint.py ck-f4-vo-chong-chia-tien --strict` — `0 lỗi, 0 cảnh báo`.
- `python motion/long/build_long.py ck-f4-vo-chong-chia-tien tts` — đủ CH00–CH06; tổng 11,82 phút.
- `python motion/long/build_long.py ck-f4-vo-chong-chia-tien html` — 7/7: CH00 8 cảnh, CH01 13, CH02 13, CH03 12, CH04 13, CH05 13, CH06 15; không Error.
- `python motion/long/clip_sheet.py ck-f4-vo-chong-chia-tien` — đã mở và soi clip sheet.
- `python scripts/long_gate.py ck-f4-vo-chong-chia-tien --min-syl 1800` — `ĐẠT`.
- Đã chạy thêm ngưỡng ticket chung: `--min-syl 2200` — `ĐẠT`.

## Kiểm chứng và lỗi

- Không có khẳng định nào không kiểm được; 10 URL nguồn có trong spec, lấy từ kho facts đã được ticket cho phép.
- Không còn lỗi lint hoặc lỗi engine. Trong quá trình dựng đã sửa neo cảnh trùng, mood nhạc không có và một clip ngắn; đây là lỗi dữ liệu cảnh, không sửa engine.

## Clip và đầu ra

- Clip cuối: `6963484`, `6963962`, `6963483`, `9869607`, `6962712`, `7735859`, `6963478`, `8122601`, `7646693`, `4052868`, `6963485`, `6963967`, `6963496`, `6964248`, `6963493`, `7735862`, `9870505`, `6963976`.
- Clip sheet: `output/long/ck-f4-vo-chong-chia-tien/qa_clips.jpg`.
- HTML chương: `output/long/ck-f4-vo-chong-chia-tien/ch00/` đến `ch06/`.
- Thumbnail: không chạy theo luật W2; chưa tạo thumbnail.
