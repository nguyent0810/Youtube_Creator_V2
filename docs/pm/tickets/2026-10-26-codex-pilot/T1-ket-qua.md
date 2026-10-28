# T1 — MIM Alan Turing và Bombe: báo cáo sản xuất

Thời gian thực hiện: 26/10/2026.

## Kết quả đã hoàn thành

- Đã tạo topic `data/long/mim-turing-bombe/`: `script.md`, `factcheck.md`, `gen_scenes.py`, `spec.json` và 8 tệp chương `ch00.json`–`ch07.json`.
- Tiêu đề chọn: **NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing Và Bombe** (57 ký tự). Có hai phương án dự phòng trong `spec.youtube.titles`.
- Lộ trình giữ chân: **“một khóa bị thiếu”** — sáu mắt xích người–máy–quy trình. Không lặp dạng của bài Petrov; phép thử Turing chỉ nhắc một câu.
- Kịch bản: 8 chương, 166 câu, 1.818 âm tiết. TTS đo 8,51 phút lời đọc; HTML có các chương tổng 530,2 giây, cộng endcard 20 giây là khoảng **9 phút 10 giây**.
- `publish_at` là `2026-11-23T13:00:00Z`; playlist là `Công Nghệ Quanh Ta`.
- Không có hình phim. Ảnh duy nhất khai báo là chân dung Alan Turing tuổi 16, Wikimedia Commons, **Public Domain Mark 1.0**. Không dùng ảnh Bombe/Enigma vì các ứng viên thường CC BY-SA.

## Các cổng đã chạy

| Cổng / lệnh | Kết quả |
|---|---|
| `python motion/long/script_lines.py mim-turing-bombe` | Qua integrity; sinh 8 chương, 1.818 âm tiết. |
| `python data/long/mim-turing-bombe/gen_scenes.py` | Sạch: `spec + 8 chương`. |
| `python motion/long/studio_lint.py mim-turing-bombe --strict` | **0 lỗi, 0 cảnh báo**. |
| `python motion/long/build_long.py mim-turing-bombe tts` | Thành công; tổng 8,51 phút lời đọc. |
| `python motion/long/build_long.py mim-turing-bombe html` | Thành công; 8 HTML chương được tạo. Đã sửa một neo cảnh trùng mốc trước khi chạy lại. |
| `python motion/long/clip_sheet.py mim-turing-bombe` | Chạy thành công, báo không có clip trong các `ch*.json`; không có clip sheet để xem vì dự án không dùng Pexels/B-roll. |
| Quét chuỗi cấm trong phần công khai `spec.youtube` | Sạch. Chuỗi `factcheck` chỉ nằm trong `sources_internal`, không công khai. |
| `python motion/long/thumb.py mim-turing-bombe t1` | **Chưa thành công**: npm/hyperframes bị Windows trả `EPERM` khi `npx` spawn/tạo cache. Đã thử lại một lần và thử cache trong workspace, vẫn lỗi. |

## Thumbnail và clip sheet

- Mẫu thumbnail đã tạo: `motion/long/thumbs/mim-turing-bombe_t1.html`.
- Thumbnail thiết kế dùng chân dung PD, chữ “GIẢI MÃ ENIGMA / MÁY BOMBE / 1940”.
- Chưa có `output/long/mim-turing-bombe/t1.jpg` và `t1_small.jpg` vì lỗi môi trường npm nêu trên; vì vậy **chưa thể soi thumbnail cỡ mobile**. Claude cần chạy lại `thumb.py` sau khi hết khóa/quyền chặn npm.
- Không có đường dẫn clip sheet: lệnh xác nhận dự án có 0 clip; tất cả cảnh dùng graphic/text và chân dung tư liệu.

## Nguồn và điểm chưa kiểm được

- Đã mở GCHQ về cuộc gặp Pyry và mối liên hệ Rejewski–Turing–Bombe; Bletchley Park về Welchman/diagonal board; Turing Digital Archive; và Commons cho giấy phép chân dung. URL đầy đủ và từng khẳng định nằm trong `data/long/mim-turing-bombe/factcheck.md`.
- Không đọc ngày cụ thể trong tháng 3/1940 cho Victory; nguồn được dùng chỉ xác nhận tháng.
- Không dùng số lượng Bombe, số lượng người vận hành hay tuyên bố định lượng về tác động quân sự, vì chưa có nguồn đã mở đủ mạnh.

## Giới hạn tuân thủ

Không chạy `render` hoặc `final`; không upload; không đọc credential; không ghi `state.sqlite`; không dùng lệnh git; không sửa mã dùng chung.
