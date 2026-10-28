# W1-3 — Báo cáo `ck-f3-tien-mung-cuoi`

## Đã thực hiện

- Viết `data/long/ck-f3-tien-mung-cuoi/script.md`: 7 chương, lộ trình lịch treo tường, chị Hà và toàn bộ mức tiền được nêu là **VÍ DỤ GIẢ ĐỊNH**.
- Viết bảng biểu đồ đầu kịch bản cho từng chương; biểu đồ chính là lịch nhiệt mười hai tháng và bộ đếm cộng dồn, chốt ở 5,6 triệu đồng.
- Viết `factcheck.md` với 10 dòng URL nguồn đã có trong kho dữ kiện và các dòng phép tính giả định.
- Viết `analysis.py`, `check.py`, và tạo `results.json`.

## Lệnh đã chạy

| Lệnh | Kết quả |
|---|---|
| `PYTHONIOENCODING=utf-8 python data/long/ck-f3-tien-mung-cuoi/analysis.py` | Ghi `results.json`: tổng cưới 3,5 triệu; dịp khác 2,1 triệu; tổng 5,6 triệu; tỷ lệ 46,67%. |
| `PYTHONIOENCODING=utf-8 python data/long/ck-f3-tien-mung-cuoi/check.py` | `F3 check: OK`. |
| `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-f3-tien-mung-cuoi` | 2.020 âm tiết; CH00 305 âm tiết; 165 câu. |
| `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-f3-tien-mung-cuoi --strict` | 0 lỗi, 8 cảnh báo. |
| `PYTHONIOENCODING=utf-8 python scripts/long_gate.py ck-f3-tien-mung-cuoi --min-syl 1900` | **TRƯỢT, 19 lỗi** — xem mục chặn dưới đây. |

## Vòng mở chính

- Mở tại CH00 câu 1: lương 12 triệu và tổng phong bì giả định 5,6 triệu.
- Đóng tại CH06 câu 12–15: nhiều phong bì nhỏ ở nhiều tháng chạy chung một bộ đếm, và 5,6/12 = 46,67%.

## Bảng biểu đồ theo chương

| Chương | Biểu đồ | Số chính |
|---|---|---|
| CH00 | Heat + counter | 5,6 triệu/năm |
| CH01 | Counter tỷ lệ | 500 nghìn; 4,17%; 12 triệu |
| CH02 | Cột theo quan hệ | 1,4; 1,5; 0,6 triệu |
| CH03 | Heat mười hai tháng | 0; 0,8; 0,7; 0,5; 0,3; 1,0 triệu |
| CH04 | Cột chồng cưới | 2×700 nghìn; 3×500 nghìn; 2×300 nghìn |
| CH05 | Cột dịp khác | 0,8; 0,5; 0,3; 0,5 triệu |
| CH06 | Thác + đường cộng dồn | 12; -3,5; -2,1; 5,6 triệu; 46,67% |

## Cảnh báo lint còn lại

`studio_lint --strict` không có lỗi. Tám cảnh báo là: hai câu liệt kê dài ở CH00/CH04, cùng mật độ câu ngắn thấp ở CH00, CH01, CH03, CH04, CH05 và CH06. Các cảnh báo không được tự bổ sung bằng câu đệm; cần biên tập viên quyết định nhịp đọc trước vòng dựng cảnh.

## Chặn cổng `long_gate`

Ticket W1 và `00-CHUNG-W1.md` chỉ cho phép ghi `script.md`, `factcheck.md`, `analysis.py`, `check.py`, `results.json` và báo cáo; đồng thời `script_lines.py` mới chỉ tự tạo `chNN.json`. Vì vậy W1 không được tạo `gen_scenes.py`, `spec.json`, cảnh, TTS, HTML, clip sheet hoặc thumbnail.

`long_gate` bắt buộc đúng các đầu ra của vòng dựng kế tiếp: `hud`, tối thiểu 5 loại cảnh mỗi chương, TTS cho 7 chương, thời lượng/cảnh, và `spec.youtube`. Do các file cần thiết bị ticket cấm ở W1, lệnh bắt buộc in **TRƯỢT (19 lỗi)**; không thể in ĐẠT mà không vượt phạm vi ticket. Chưa có clip sheet hoặc thumbnail trong vòng W1.

## Khẳng định không kiểm được hoặc đã loại

- Không dùng bất kỳ kết luận nào về “mùa cưới cuối năm”, vì kho không có khảo sát đại diện cho khẳng định đó.
- Không dùng mức mừng phổ biến/chuẩn; các mức 300, 500 và 700 nghìn chỉ là ví dụ giả định.
- Chưa có clip Pexels được kiểm mở, nên không đưa clip vào W1.
