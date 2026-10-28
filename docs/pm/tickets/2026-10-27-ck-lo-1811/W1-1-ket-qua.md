# W1-1 — Kết quả kịch bản `ck-f1-tro-cap-that-nghiep`

## Đã làm

- Viết `data/long/ck-f1-tro-cap-that-nghiep/script.md`: bảy chương CH00–CH06, lộ trình đồng hồ đếm ngược, biểu đồ theo từng chương và vòng mở/đóng ở waterfall khoản thiếu.
- Viết `factcheck.md` với 14 URL đã mở từ kho dữ kiện được duyệt; không đưa khẳng định nào ngoài kho. Tất cả số của chị Lan được ghi là VÍ DỤ GIẢ ĐỊNH.
- Viết `analysis.py`, `check.py`, và tạo `results.json`.
- `script_lines.py` đã tạo `ch00.json` đến `ch06.json`, theo ngoại lệ W1 cho phép.

## Cổng đã chạy

| Lệnh | Kết quả |
|---|---|
| `PYTHONIOENCODING=utf-8 python data/long/ck-f1-tro-cap-that-nghiep/analysis.py` | Ghi `results.json`: trợ cấp 9, thiếu 4, tổng 63, thiếu lũy kế 4→28 triệu đồng. |
| `PYTHONIOENCODING=utf-8 python data/long/ck-f1-tro-cap-that-nghiep/check.py` | `CK-F1 check: OK (7 phép)` |
| `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-f1-tro-cap-that-nghiep` | 137 câu, 1.930 âm tiết; CH00 230 âm tiết. |
| `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-f1-tro-cap-that-nghiep --strict` | `0 lỗi, 7 cảnh báo` (cảnh báo về mật độ câu ngắn). |
| `python scripts/long_gate.py ck-f1-tro-cap-that-nghiep --min-syl 1900` | **TRƯỢT, 19 lỗi**; xem giới hạn W1 bên dưới. |

## Vòng mở chính

- Mở ở CH00, câu hai: “Mười ba triệu chi phí trừ chín triệu trợ cấp, chị Lan thiếu bốn triệu.”
- Đóng ở CH06, câu áp chót: “Chín triệu mỗi tháng, chi phí mười ba triệu, thiếu bốn triệu; bảy tháng thành hai mươi tám triệu trong ví dụ giả định.”

## Bảng biểu đồ

| Chương | Biểu đồ | Số neo |
|---|---|---|
| CH00 | Waterfall | 13 − 9 = 4 triệu |
| CH01 | Cột + waterfall | 15 × 60% = 9; 13 − 9 = 4 triệu |
| CH02 | Bốn chấm điều kiện + bộ đếm | 12/24, 3 tháng, 10 ngày |
| CH03 | Đường chờ + cột so luật | 10 ngày, ngày 11, 16 → 11 ngày |
| CH04 | Cột bậc thang | 84 tháng → 3 + 4 = 7 tháng; 63 triệu |
| CH05 | Cột trần vùng + waterfall | 26,55; 23,65; 20,70; 18,50 triệu |
| CH06 | Waterfall + đường tích lũy | 4 → 28 triệu; 3 ngày thông báo |

## Giới hạn cổng Long

`long_gate.py` không thể in ĐẠT ở W1 với đúng phạm vi file của ticket. Ticket chung chỉ cho phép ghi kịch bản, factcheck, hai file tính, kết quả và báo cáo; không cho phép viết `gen_scenes.py`, `spec.json`, metadata `youtube`, `hud` hay chạy TTS. Vì vậy các `chNN.json` do `script_lines.py` tạo chỉ có lời đọc, chưa có cảnh/hud; cổng báo thiếu 5 loại cảnh mỗi chương, metadata, bảng SAY và TTS, cùng thời lượng 551,4 giây/cảnh. Đây là 19 lỗi dựng, không phải lỗi nội dung kịch bản.

Không có khẳng định nào bị bỏ vì nguồn yếu. Không có clip sheet hoặc thumbnail trong ticket W1; hai artefact này chưa được tạo.
