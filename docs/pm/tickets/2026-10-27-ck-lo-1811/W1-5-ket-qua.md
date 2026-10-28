# W1-5 — Kết quả kịch bản `ck-c6-gia-tran-san-t2`

## Đã làm

- Viết `script.md` gồm bảy chương CH00–CH06, theo lộ trình “theo chân một trăm cổ phiếu”.
- Viết `factcheck.md` với tám URL đã mở từ kho dữ kiện; các mốc thuế, phí chung và T+0 chưa chốt đều được nêu là chưa khẳng định.
- Viết `analysis.py`, `check.py` và sinh `results.json` cho dải giá, giá trị lệnh giả định, dữ liệu hai phiên tháng tư năm hai nghìn không trăm hai mươi lăm và lịch T đến T+2.
- Chạy `script_lines.py` với `--allow-repeat-line`, vì các câu lịch T, T+1, T+2 được lặp có chủ ý để theo cùng một trăm cổ phiếu.

## Cổng đã chạy

| Lệnh | Kết quả |
|---|---|
| `PYTHONIOENCODING=utf-8 python data/long/ck-c6-gia-tran-san-t2/analysis.py` | Ghi `results.json`. |
| `PYTHONIOENCODING=utf-8 python data/long/ck-c6-gia-tran-san-t2/check.py` | `C6 check: OK (11 phép)`. |
| `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-c6-gia-tran-san-t2 --allow-repeat-line` | 189 câu, 2.300 âm tiết; CH00 229 âm tiết. |
| `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-c6-gia-tran-san-t2 --strict` | 0 lỗi, 1 cảnh báo: CH03 có 4 trên 29 câu ngắn, thấp hơn nhịp mục tiêu. |
| `python scripts/long_gate.py ck-c6-gia-tran-san-t2 --min-syl 1900` | **TRƯỢT (19 lỗi), không in ĐẠT.** |

## Lý do `long_gate` chưa đạt

Đây là ticket W1. File luật chung cho W1 giới hạn đầu ra ở `script.md`, `factcheck.md`, `analysis.py`, `check.py`, `results.json` và báo cáo; chỉ cho phép `script_lines.py` tự sinh `chNN.json`. Do đó tôi không tạo `gen_scenes.py`, `spec.json`, cảnh có `hud`, TTS, HTML, clip sheet hoặc thumbnail.

Những mục `long_gate` đang yêu cầu đều thuộc pha dựng bị ticket W1 cấm ghi: bảy chương chưa có `hud`, mỗi chương chưa có năm loại cảnh, chưa có TTS, chưa có `spec.youtube`/`say`/nguồn công khai trong spec và chưa có cảnh để đo thời lượng. Cổng chỉ xác nhận được phần W1 là 2.300 âm tiết và tám URL. Cần một ticket dựng cảnh kế tiếp để các lỗi này được xử lý hợp lệ.

## Vòng mở chính

- Mở: CH00, câu đầu: “Hai triệu đồng đã khớp, nhưng nút bán chưa bấm được.”
- Đóng: CH06: “Giá sàn giới hạn giá của từng phiên. T cộng hai giới hạn thời điểm bạn có chứng khoán để đặt lệnh bán.”

## Bảng biểu đồ theo chương

| Chương | Biểu đồ |
|---|---|
| CH00 | Lịch nhiệt T, T+1, T+2; giá trị hai triệu; một trăm cổ phiếu chưa bán được. |
| CH01 | Dải sàn 18.600, tham chiếu 20.000, trần 21.400 đồng — ví dụ giả định. |
| CH02 | Cột so sánh biên độ 7%, 20%, 15%, 40%. |
| CH03 | Cột chồng phiên 03/04/2025: 263 giảm sàn, 254 giảm khác, 13 tăng, 3 tăng trần. |
| CH04 | Lịch T đến T+2: 11:00–11:30, trước 13:00, chiều T+2. |
| CH05 | Cột chồng tiền và cổ phiếu: T/T+1 bằng 0 cổ phiếu bán được; chiều T+2 là 100. |
| CH06 | Bảng tách dải giá và thời điểm; ba ô phí, thuế, T+0 giữ trạng thái chưa chốt. |

## Khẳng định đã bỏ hoặc không kiểm được

- Không khẳng định thuế chuyển nhượng 0,1% sau 01/07/2026.
- Không nêu mức phí giao dịch chung.
- Không khẳng định T+0, bán chứng khoán chờ về hay mốc triển khai.

## Clip sheet và thumbnail

Không có. Ticket W1 không cho tạo cảnh, HTML, clip sheet hay thumbnail; các đầu ra này cần ticket dựng cảnh kế tiếp.
