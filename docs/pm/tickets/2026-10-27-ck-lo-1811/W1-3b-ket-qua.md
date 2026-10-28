# W1-3b — Báo cáo `ck-f3-tien-mung-cuoi`

## Đã thực hiện

- Rút CH00 từ 305 xuống **191 âm tiết**; vẫn giữ con số mở đầu, nghịch lý phong bì nhỏ cộng thành gần nửa tháng lương, lịch nhiệt và vòng bộ đếm mở ở CH00, đóng ở CH06.
- Bổ sung bốn câu có số và phép tính ở từng CH02–CH05, chỉ dùng dữ kiện trong `facts.md`.
- Cập nhật bảng **Biểu đồ**, `factcheck.md`, `analysis.py`, `check.py` và `results.json` cho các phép thay đổi đầu vào: bớt một đám bạn thân, thêm một đám đồng nghiệp, bớt một phong bì lì xì.
- Kịch bản hiện có **2.369 âm tiết**, trong khung 2.350–2.600 của ticket.

## Vòng mở chính

- Mở ở CH00 câu 1: lương mười hai triệu, tổng phong bì năm phẩy sáu triệu trong ví dụ giả định.
- Nghịch lý ở CH00 câu 2: từng phong bì nhỏ nhưng cộng lại gần nửa tháng lương.
- Vòng đóng ở CH06 câu 13–16: nhiều phong bì nhỏ, nhiều tháng, một bộ đếm chung và tỷ lệ năm phẩy sáu trên mười hai bằng bốn mươi sáu phẩy sáu bảy phần trăm.

## Bảng biểu đồ

| Chương | Biểu đồ | Số chính |
|---|---|---|
| CH00 | Heat + counter | 5,6 triệu/năm; 14 dịp |
| CH01 | Counter tỷ lệ | 500 nghìn; 4,17%; lương 12 triệu |
| CH02 | Cột theo quan hệ | 1,4; 1,5; 0,6 triệu; tổng 3,5 triệu |
| CH03 | Heat 12 tháng + cộng dồn | 0,8 sau tháng hai; 2,8 sau tháng tám; 5,6 cuối năm |
| CH04 | Cột chồng cưới | 2×700 nghìn; 3×500 nghìn; 2×300 nghìn |
| CH05 | Cột dịp khác | 0,8; 0,5; 0,3; 0,5 triệu; tổng 2,1 triệu |
| CH06 | Thác + đường cộng dồn | 12; -3,5; -2,1; 5,6 triệu; 46,67% |

## Lệnh đã chạy

| Lệnh | Kết quả |
|---|---|
| `PYTHONIOENCODING=utf-8 python data/long/ck-f3-tien-mung-cuoi/analysis.py` | Ghi `results.json`, gồm tổng cưới 3,5 triệu, dịp khác 2,1 triệu, tổng 5,6 triệu và các phép thử thay đổi đầu vào. |
| `PYTHONIOENCODING=utf-8 python data/long/ck-f3-tien-mung-cuoi/check.py` | `F3 check: OK`. |
| `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-f3-tien-mung-cuoi` | 172 câu; CH00 191 âm tiết; tổng 2.369 âm tiết. |
| `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-f3-tien-mung-cuoi --strict` | **0 lỗi**, 9 cảnh báo. |
| `PYTHONIOENCODING=utf-8 python scripts/long_gate.py ck-f3-tien-mung-cuoi --min-syl 1900` | **TRƯỢT, 19 lỗi dựng**; chi tiết dưới đây. |

## Cảnh báo lint còn lại

Chín cảnh báo không phải lỗi: hai câu liệt kê dài ở CH00 và CH04; cùng cảnh báo mật độ câu ngắn thấp ở CH00–CH06. Không thêm câu đệm chỉ để triệt cảnh báo.

## Kết quả long_gate và giới hạn W1

`long_gate` xác nhận ngưỡng lời đọc đã đạt: 2.369 âm tiết và 10 URL trong `factcheck.md`. Lệnh vẫn **không thể in ĐẠT trong W1** vì ticket `00-CHUNG-W1.md` chỉ cho phép `script.md`, `factcheck.md`, `analysis.py`, `check.py`, `results.json`, báo cáo và `chNN.json` do `script_lines.py` tạo.

Mười chín lỗi còn lại đều đòi đầu ra của vòng dựng bị cấm ở W1: thiếu `hud` và ít nhất năm loại cảnh cho bảy chương, chưa có TTS, chưa có đủ cảnh để đo thời lượng, thiếu `spec.youtube` và bảng `say`. Không tạo `gen_scenes.py`, `spec.json`, TTS, HTML, clip sheet hay thumbnail để tránh vượt phạm vi ticket.

## Khẳng định không kiểm được hoặc đã loại

- Không dùng “mùa cưới cuối năm” như một kết luận hay dự báo toàn quốc.
- Không nêu mức 300, 500 hay 700 nghìn là phổ biến hoặc chuẩn; toàn bộ là **VÍ DỤ GIẢ ĐỊNH**.
- Không có clip Pexels đã được kiểm mở trong kho; vòng W1 không có clip sheet và thumbnail.

## Đường dẫn đầu ra

- Clip sheet: chưa tạo trong W1.
- Thumbnail: chưa tạo trong W1.
