# Kết quả T5W2 — `mim-social-network`

## Đã làm

- Giữ nguyên `script.md`; dựng `gen_scenes.py`, `spec.json` và 8 chương cảnh cho mô-típ **BẢN ĐỒ KẾT NỐI**.
- Điền `publish_at` `2026-11-29T13:00:00Z`, `SAY`, bản đồ Boston/Cambridge ghim Harvard, mô tả YouTube và 15 URL nguồn công khai.
- Viết `data/long/mim-social-network/ai_prompts.md`: 4 ảnh AI chờ tạo (`ai_01.png`–`ai_04.png`), đều là minh họa không chữ/logo; người thật chỉ từ sau lưng/dáng nghiêng.
- Tải và soát clip. Đã loại clip `14314426` sau khi xem sheet vì màn hình/thiết bị và trang phục không đủ sạch; thay bằng `946146`. Ba clip dùng cuối: `946146`, `7490429`, `5672679`.

## Lệnh đã chạy và kết quả

- `python motion/long/pexels.py get mim-social-network ...`: tải clip ngang thành công.
- `python data/long/mim-social-network/gen_scenes.py --standin` → `python motion/long/script_lines.py mim-social-network` → `python motion/long/build_long.py mim-social-network tts` → `python motion/long/build_long.py mim-social-network html`: HTML đủ **8/8** (`ch00`–`ch07`), không có `Error`.
- `python data/long/mim-social-network/gen_scenes.py` → `python motion/long/script_lines.py mim-social-network`: 2.261 âm tiết, 116 câu.
- `python motion/long/clip_sheet.py mim-social-network`: đã mở và soát sheet.
- `python scripts/long_gate.py mim-social-network --min-syl 1900`: **ĐẠT** — 2.261 âm tiết, 10,2 phút, 82 cảnh, 7,5 giây/cảnh, 3 clip khác nhau, 11 ảnh khác nhau, 15 URL nguồn.

## Lỗi/cảnh báo còn lại

- HTML có 3 cảnh báo không chặn ở CH01, CH05, CH06: một dòng chữ lớn mỗi chương còn bám sát lời đọc. Không có lỗi HTML hay lỗi `long_gate`.
- Không có khẳng định chưa kiểm được thêm: lời đọc giữ nguyên và dùng kho nguồn đã duyệt. Những chi tiết không có nguồn xác nhận trong lời đọc đã được gọi rõ là cảnh phim hoặc khoảng trống của nguồn.
- Chờ **4 ảnh AI** được chủ kênh tạo/import; không render.

## Đường dẫn kiểm tra

- Clip sheet: `output/long/mim-social-network/qa_clips.jpg`
- HTML: `output/long/mim-social-network/mim-social-network_ch00.html` đến `mim-social-network_ch07.html`
- Thumbnail: không tạo theo chỉ thị ticket.
