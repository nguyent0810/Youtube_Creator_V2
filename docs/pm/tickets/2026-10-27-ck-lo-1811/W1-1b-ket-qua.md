# W1-1b — Kết quả sửa kịch bản `ck-f1-tro-cap-that-nghiep`

## Đã làm

- Bổ sung bốn câu có số liệu và bước vẽ được vào từng CH02–CH05, chỉ dùng dữ kiện trong `facts.md`.
- Cập nhật bảng **Biểu đồ** đầu `script.md`: thêm cửa sổ hai mươi bốn và ba mươi sáu tháng, mốc mười sáu xuống mười một ngày, bậc ba–bốn–bảy tháng, và bốn phép nhân trần vùng.
- Cập nhật `factcheck.md` cho các câu mới: điều kiện chấm dứt, mười ngày chờ/ngày thứ mười một, chênh năm ngày, công thức tám mươi bốn tháng thành bảy tháng, và bốn trần vùng.
- Tổng kịch bản: **153 câu, 2.351 âm tiết**; CH00 vẫn **230 âm tiết**. Mức này nằm trong dải 2.350–2.600 của ticket.

## Vòng mở chính

- Mở ở CH00, câu hai: “Mười ba triệu chi phí trừ chín triệu trợ cấp, chị Lan thiếu bốn triệu.”
- Đóng ở CH06, câu áp chót: “Chín triệu mỗi tháng, chi phí mười ba triệu, thiếu bốn triệu; bảy tháng thành hai mươi tám triệu trong ví dụ giả định.”

## Bảng biểu đồ theo chương

| Chương | Biểu đồ | Số neo |
|---|---|---|
| CH00 | Waterfall | 13 − 9 = 4 triệu |
| CH01 | Cột + waterfall | 15 × 60% = 9; 13 − 9 = 4 triệu |
| CH02 | Bốn chấm + bộ đếm | 12/24, 36 tháng, 3 tháng, 10 ngày, ngày 11 |
| CH03 | Đường chờ + cột so luật | 10 ngày, ngày 11; 16 → 11 ngày, chênh 5 |
| CH04 | Cột bậc thang | 12–36 tháng → 3; 48 tháng → 4; tổng 7 trên trần 12 |
| CH05 | Cột trần vùng + waterfall | 5,31 × 5 = 26,55; 4,73 × 5 = 23,65; 4,14 × 5 = 20,70; 3,70 × 5 = 18,50 |
| CH06 | Waterfall + đường tích lũy | 4 → 28 triệu; thông báo 3 ngày |

## Cổng đã chạy

| Lệnh | Kết quả |
|---|---|
| `PYTHONIOENCODING=utf-8 python data/long/ck-f1-tro-cap-that-nghiep/analysis.py` | Ghi `results.json`: trợ cấp 9, thiếu 4, tổng 63, thiếu lũy kế 4→28 triệu đồng. |
| `PYTHONIOENCODING=utf-8 python data/long/ck-f1-tro-cap-that-nghiep/check.py` | `CK-F1 check: OK (7 phép)` |
| `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-f1-tro-cap-that-nghiep` | 153 câu, 2.351 âm tiết; CH00 230 âm tiết. |
| `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-f1-tro-cap-that-nghiep --strict` | `0 lỗi, 7 cảnh báo` về mật độ câu ngắn. |
| `PYTHONIOENCODING=utf-8 python scripts/long_gate.py ck-f1-tro-cap-that-nghiep --min-syl 1900` | **TRƯỢT, 19 lỗi dựng**; chi tiết bên dưới. |

## Cổng Long chưa đạt

`long_gate.py` xác nhận phần lời đọc đạt 2.351 âm tiết và 14 URL nguồn, nhưng không thể in **ĐẠT** trong phạm vi W1: bảy `chNN.json` do `script_lines.py` tạo chưa có `hud` hoặc cảnh; chưa có TTS; và `spec.youtube`/`say`/nguồn công khai cho bản dựng chưa tồn tại. Kết quả là bảy lỗi thiếu HUD, bảy lỗi thiếu tối thiểu năm loại cảnh, cùng lỗi TTS, thời lượng mỗi cảnh, metadata YouTube, nguồn công khai và SAY.

Theo `00-CHUNG-W1.md`, W1 chỉ được ghi `script.md`, `factcheck.md`, `analysis.py`, `check.py`, `results.json`, báo cáo này và các `chNN.json` do `script_lines.py` tự tạo; ticket W1-1b cũng nói trạng thái trượt phần dựng là bình thường. Vì vậy không tạo `gen_scenes.py`, `spec.json`, TTS hay artefact dựng chỉ để che lỗi cổng.

## Khẳng định và artefact

- Không có khẳng định nào bị bỏ vì nguồn yếu; mọi dữ kiện mới đều đã có URL mở được trong `facts.md` và dòng tương ứng trong `factcheck.md`.
- Ticket W1 không có dựng clip sheet hoặc thumbnail; chưa tạo hai artefact này.
