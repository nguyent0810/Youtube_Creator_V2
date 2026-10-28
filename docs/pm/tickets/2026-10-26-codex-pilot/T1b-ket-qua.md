# T1b — Kết quả sửa `mim-turing-bombe`

## Đã làm

- Viết lại `script.md`: cold open nay là cảnh điện Enigma bị chặn và Victory phải tìm khóa trước khi khóa đổi; bỏ liệt kê nhân sự năm 1940 và bỏ câu meta.
- Sửa mốc sự thật: chỉ nói Victory hoạt động **tháng 3/1940**, không đọc ngày 18/3. WRNS được chuyển sang bối cảnh Eastcote năm 1943, với quy trình ca trực và kiểm tra điểm dừng.
- Bỏ các câu đệm bị review nêu; thay bằng chi tiết về Pyry, Rejewski, diagonal board, xưởng BTM/Keen, crib và Jean Millar.
- Bổ sung `factcheck.md` với các URL đã mở; thêm nguồn và giấy phép ảnh Turing (PDM), Rejewski (PD), Bletchley Park (PD), Enigma (CC0).
- Viết lại `gen_scenes.py`, sinh **48 cảnh** (trước: 26 cảnh: 8 chapter, 8 kinetic, 8 slam, 2 print; sau: 8 chapter, 8 broll, 8 kinetic, 8 photo, 8 ledger và 8 cảnh timeline/org/date). Mỗi chương có ít nhất bốn loại cảnh.
- Đã tìm và tải B-roll Pexels; sau khi soát, loại clip bảng điều khiển có chữ `DETENIDO` và clip máy chữ lộ nhãn. Bản cuối chỉ dùng clip `34187599`, máy đánh chữ từ trên xuống, không thấy logo hoặc chữ thương hiệu đọc được.

## Cổng đã chạy

1. `python motion/long/script_lines.py mim-turing-bombe` — qua integrity; bản cuối 80 câu, 1.100 âm tiết, TTS ước tính 5,02 phút.
2. `python data/long/mim-turing-bombe/gen_scenes.py` — sinh `spec.json` và 8 tệp chương, 48 cảnh.
3. `python motion/long/studio_lint.py mim-turing-bombe --strict` — **0 lỗi, 5 cảnh báo** về mật độ câu ngắn ở CH00, CH01, CH02, CH05, CH07.
4. `python motion/long/build_long.py mim-turing-bombe tts` — hoàn tất tạo TTS trong `output/long/mim-turing-bombe/tts/`.
5. `python motion/long/build_long.py mim-turing-bombe html` — hoàn tất HTML 8 chương. Còn 1 cảnh báo: CH00 có 1/2 dòng chữ lớn chép nguyên lời đọc.
6. `python motion/long/clip_sheet.py mim-turing-bombe` — hoàn tất và đã soi ảnh.

Không chạy `render`, `final`, thumbnail hay bất kỳ lệnh upload/xuất bản nào.

## Lưu ý bắt buộc trước duyệt

- Bản cuối còn ngắn hơn yêu cầu 9–11 phút: TTS đo 5,02 phút. Không nên đưa sang render/duyệt đăng khi chưa mở rộng nội dung có nguồn.

## Khẳng định mới và nguồn

- Victory hoạt động tháng 3/1940; Pyry 25–26/07/1939; Turing gặp nhóm Ba Lan tháng 01/1940: GCHQ, `The Pyry Forest Meeting`.
- Jean Millar tới Eastcote tháng 11/1943, làm các ca 8 giờ và vận hành/kiểm tra Bombe: GCHQ, `Jean Millar`.
- Turing/Welchman và diagonal board: tài liệu Bletchley Park `Gordon Welchman`.

Tất cả URL và ghi chú giấy phép nằm trong `data/long/mim-turing-bombe/factcheck.md`.

## Chưa kiểm được / chủ động không nói

- Không dùng ngày cụ thể của Victory.
- Không dùng số lượng Bombe, thời gian chạy, số người vận hành hay tác động quân sự.

## Đầu ra kiểm

- Clip sheet: `output/long/mim-turing-bombe/qa_clips.jpg`
- Thumbnail: không làm theo yêu cầu ticket (Claude sẽ dựng; ticket nêu bỏ qua `thumb.py`).
