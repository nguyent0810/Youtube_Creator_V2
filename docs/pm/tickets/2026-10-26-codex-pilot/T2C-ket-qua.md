# Kết quả T2C — hoàn thiện spec và phát âm `mim-turing-bombe`

## Đã hoàn tất

- Không viết lại nội dung; chỉ sửa dòng tiêu đề đầu của `script.md` để khớp title chính: `NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing Và Bombe` (50 ký tự).
- Sửa `TITLE` và bổ sung hai phương án dự phòng: 38 và 37 ký tự, đều dưới giới hạn 60.
- Hoàn thiện `make_spec()` trong `gen_scenes.py`, không sửa tay `spec.json`: lịch phát hành, playlist, category, thumbnail, tóm tắt ba câu không lộ kết, ghi chú trung thực, 8 tiêu đề chương, 15 URL nguồn công khai, 14 tag, 5 hashtag và credit Commons/Pexels.
- Bổ sung bảng `SAY` và nối vào spec bằng `"say": SAY`. Bảng bao phủ toàn bộ tên, địa danh, thuật ngữ, viết tắt và số lớn mà ticket nêu.
- Kiểm tra chuỗi đọc sau thay thế: `Bletchley Park` thành “Blétch-li Pác”; `158.962.555.217.826.360.000` thành “khoảng một trăm năm mươi chín tỷ tỷ”; `GC&CS` và `GCHQ` cũng được thay theo bảng phát âm.
- Không render, không tạo thumbnail, không chạy `thumb.py`, không upload và không thao tác YouTube.

## Lệnh đã chạy

| Lệnh | Kết quả |
|---|---|
| `python data/long/mim-turing-bombe/gen_scenes.py` | Sinh lại `spec.json` và 8 chương cảnh từ nguồn duy nhất `gen_scenes.py`. |
| `python motion/long/script_lines.py mim-turing-bombe` | Qua integrity, 138 câu và 2.170 âm tiết. |
| `python motion/long/studio_lint.py mim-turing-bombe --strict` | 0 lỗi; 8 cảnh báo mật độ câu ngắn giữ nguyên từ T2B. |
| `python motion/long/build_long.py mim-turing-bombe tts` | Hoàn tất TTS/timing với bảng phát âm mới cho 8 chương. |
| `python motion/long/build_long.py mim-turing-bombe html ch00 ch01 ch02 ch03 ch04 ch05 ch06 ch07` | Hoàn tất HTML cho cả 8 chương. |
| `python scripts/long_gate.py mim-turing-bombe --min-syl 1900` | **ĐẠT** — 2.170 âm tiết, 10,2 phút, 72 cảnh nội dung, 8,5 giây/cảnh, 6 clip khác, 11 ảnh khác, 20 URL nguồn. |

## Kiểm tra phát âm

Không có công cụ phát âm thanh tương tác trong môi trường này nên không thể nghe trực tiếp các file âm thanh của `ch01` và câu có Bletchley. Đã kiểm tra đầu vào TTS sau khi áp dụng `SAY`; các chuỗi trọng yếu hiển thị đúng như trên. TTS đã tạo lại timing cho cả tám chương.

## Lỗi/cảnh báo còn lại và giới hạn sự thật

- Studio lint còn 8 cảnh báo về tỷ lệ câu ngắn, không có lỗi chặn. Không thêm câu đệm để làm đẹp chỉ số.
- Không thêm khẳng định lịch sử mới. Các giới hạn từ T2B vẫn giữ nguyên: không khẳng định Victory tháng 03/1940, ngày 18/03, chi tiết Doc Keen, thông số cơ khí, crib ví dụ cụ thể hoặc tác động định lượng chưa kiểm được.
- Kiểm tra usage HyperFrames không lấy được số dư do npm cache báo `EPERM`; không suy đoán usage. Workflow HTML của repo vẫn chạy thành công.

## Đường dẫn QA

- Clip sheet đã soi ở T2B: `output/long/mim-turing-bombe/qa_clips.jpg`
- Thumbnail: không tạo theo yêu cầu ticket.
