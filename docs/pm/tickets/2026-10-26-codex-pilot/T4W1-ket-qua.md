# Kết quả T4W1 — mim-moneyball

## Đã làm

- Đã viết `data/long/mim-moneyball/script.md`: 8 chương CH00–CH07, tiêu đề `MONEYBALL Ngoài Đời Thật: Billy Beane Và Con Số` (47 ký tự, một dấu hai chấm), 2.216 âm tiết.
- Mô-típ đã chọn: **tấm bảng chờ một lần lên gôn**. Mỗi chương thêm một ô dữ kiện: khoảnh khắc quyết định; ngân sách; OBP; sabermetrics; cuộc tranh luận; phần bị phim cắt gọn; giới hạn series ngắn; ảnh hưởng lan rộng.
- Đã viết `data/long/mim-moneyball/factcheck.md` với 29 dòng kiểm chứng và URL từ kho dữ kiện được duyệt.
- Không dựng cảnh, không TTS, không tạo spec hoặc `chNN.json`, đúng phạm vi “chỉ ghi 3 file” của ticket.

## Dữ kiện đã dùng theo chương

| Chương | Dữ kiện dùng từ kho |
|---|---|
| CH00 | #01–04: chuỗi 20 trận, 13/08–04/09/2002, trận 12–11, diễn biến 11–0 và home run của Hatteberg. |
| CH01 | #05–08: mùa 103–59, nhịp 20–26 rồi 83–33, quỹ lương 40.004.167 USD/hạng 28, 800–654 runs. |
| CH02 | #09–12: OBP .339 hạng ba AL, 68 walk và 88 lần xuất phát first base của Hatteberg, ERA 3,68 hạng ba MLB. |
| CH03 | #13–16: định nghĩa sabermetrics, nhóm SABR năm 1974, Baseball Abstract năm 1977/1980, cách chất vấn chỉ số truyền thống. |
| CH04 | #17–20: Beane, DePodesta năm 1999, nền tảng Harvard/Cleveland 1996, quy dẫn vừa theo Washington Post về xung đột con người. |
| CH05 | #21–24: phim năm 2011 và sách năm 2003, Peter Brand hư cấu, Art Howe và mùa 103 thắng, quy dẫn vừa theo Washington Post. |
| CH06 | #25–28: ALDS 2002 với Minnesota, tỷ số trận 1, diễn biến trận 2–4, trận 5 thua 1–5. |
| CH07 | #29–32: lan rộng của phân tích dữ liệu, các xu hướng toàn giải, analytics hiện đại, mô tả xu hướng thập niên 1990–đầu 2000. |

Các dữ kiện độ tin **vừa** đã quy dẫn trực tiếp trong lời đọc bằng “Theo Washington Post...”; không có khẳng định nào dùng ngoài kho hoặc không kiểm được.

## Lệnh đã chạy và kết quả

1. `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py mim-moneyball`
   - Kết quả: qua integrity, 108 câu, **2.216 âm tiết**.
   - Theo chương: CH00 260; CH01 250; CH02 277; CH03 248; CH04 228; CH05 294; CH06 306; CH07 353 âm tiết.

2. `Select-String` tìm hai câu đệm được nêu trong `long-rules.md` (`Rất chậm.` và `Đó là câu hỏi khó.`).
   - Kết quả: không có dòng khớp.

3. `python scripts/long_gate.py mim-moneyball --min-syl 1900`
   - Kết quả: **TRƯỢT (20 lỗi)**. Phần lời đọc đạt 2.216 âm tiết, 10,6 phút ước tính và 29 URL, nhưng cổng báo thiếu HUD, tối thiểu 5 loại cảnh mỗi chương, timing/cảnh dưới 9 giây, `spec.youtube` và bảng `SAY`.
   - Đây là cổng không thể đạt trong ticket này: ticket giới hạn đầu ra chỉ gồm `script.md`, `factcheck.md` và báo cáo này, đồng thời cấm dựng cảnh; các lỗi còn lại đều đòi hỏi `spec.json`, `chNN.json`, cảnh/timing và cấu hình TTS. Không tạo file dựng ngoài phạm vi để tránh vi phạm ticket.

## Lỗi lint còn lại và bàn giao

- Integrity kịch bản: không còn lỗi.
- Long gate: còn 20 lỗi dựng/cấu hình như trên, chưa thể in `ĐẠT` trong phạm vi ticket.
- Clip sheet: không có, vì ticket không dựng cảnh.
- Thumbnail: không có, vì ticket không yêu cầu thumbnail.
