# Kết quả T2D — dựng lại cảnh `mim-turing-bombe`

## Đã hoàn tất

- Chỉ sửa phần cảnh trong `data/long/mim-turing-bombe/gen_scenes.py`; giữ nguyên `script.md`, lời đọc, TTS, `SAY` và `spec.youtube`.
- Sửa đủ tám thẻ chương sang schema engine cần: mỗi thẻ có `no`, `k`, `title`, `sub`, `bg`, `titleAt`. Không còn trường `number` gây chữ `undefined`.
- Thay khuôn 9 cảnh lặp bằng tám bộ cảnh riêng, neo theo từ trong chính câu đọc. Chữ hiển thị dùng tên người, năm, số và vật thể của chương tương ứng; không còn ba câu template lặp tám lần.
- Mô-típ `SÁU RĂNG CỦA KHÓA` chỉ còn một ledger cố định; mỗi chương tích lũy đúng một dòng mắt xích mới.
- Bổ sung pin Pyry ở bản đồ chặng Warsaw–Pyry–Paris–Bletchley và pin Stanmore trên bản đồ outstation.
- Chuyển chữ lớn quá gần lời đọc ở CH02/CH07 thành từ khóa/vế đối lập. Không render, không upload, không tạo thumbnail.

## Lệnh đã chạy

| Lệnh | Kết quả |
|---|---|
| `python -m py_compile data/long/mim-turing-bombe/gen_scenes.py` | Qua kiểm tra cú pháp. |
| `python data/long/mim-turing-bombe/gen_scenes.py` | Sinh lại `spec.json` và `ch00.json` đến `ch07.json`. |
| `python motion/long/script_lines.py mim-turing-bombe` | Qua integrity; 138 câu, 2.170 âm tiết. Không chạy TTS lại. |
| `python motion/long/studio_lint.py mim-turing-bombe --strict` | 0 lỗi; còn 8 cảnh báo mật độ câu ngắn từ kịch bản giữ nguyên. |
| `python motion/long/build_long.py mim-turing-bombe html ch00 ch01 ch02 ch03 ch04 ch05 ch06 ch07` | Hoàn tất HTML cho cả tám chương. Không còn lỗi neo cảnh hoặc cảnh báo màn trống. |
| `python motion/long/clip_sheet.py mim-turing-bombe` | Tạo lại và soi clip sheet. |
| `python scripts/long_gate.py mim-turing-bombe --min-syl 1900` | **ĐẠT** — 2.170 âm tiết; 10,2 phút; 77 cảnh nội dung; 7,9 giây/cảnh; 5 clip khác; 11 ảnh khác; 20 URL nguồn. |

## Kiểm tra media

Đã soi `qa_clips.jpg`. Năm clip được dùng sau dựng cảnh gồm mạch điện trừu tượng, biển, bánh răng, máy đánh chữ và bó dây điện; không thấy logo hoặc chữ thương hiệu đọc được. Người trong B-roll không được gắn tên người thật.

## Cảnh báo/lỗi còn lại

- Không còn lỗi lint chặn hay lỗi HTML.
- Studio lint còn 8 cảnh báo mật độ câu ngắn vì T2D không được phép viết lại script; không chèn câu đệm để triệt chỉ số.
- HTML còn một cảnh báo không chặn ở CH02 từ bộ đo mức trùng chữ lớn với lời đọc. Chữ cảnh đã được đổi thành “MỘT HỒ SƠ ĐỔI HƯỚNG”; không phải chuỗi cảnh lặp hay phụ đề nguyên câu.
- Không thêm khẳng định lịch sử mới; các giới hạn factcheck từ T2B/T2C được giữ nguyên.
- Usage HyperFrames không kiểm được do npm cache báo `EPERM`; không suy đoán số dư.

## Đường dẫn QA

- Clip sheet: `output/long/mim-turing-bombe/qa_clips.jpg`
- Thumbnail: không tạo theo phạm vi ticket.
