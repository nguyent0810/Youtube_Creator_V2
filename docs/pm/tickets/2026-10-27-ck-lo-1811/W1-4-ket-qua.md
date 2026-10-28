# W1-4 — Kết quả kịch bản `ck-f4-vo-chong-chia-tien`

## Đã làm

- Viết `data/long/ck-f4-vo-chong-chia-tien/script.md`: 7 chương, 2.581 âm tiết; CH00 có 202 âm tiết.
- Mở vòng chính ở CH00 câu “công bằng là cùng góp một số, cùng chịu một tỷ lệ, hay cùng có phần riêng?”; đóng ở CH06 bằng ba câu hỏi tương ứng.
- Viết `factcheck.md`, `analysis.py`, `check.py` và sinh `results.json`.
- Mọi khoản tiền Thảo–Nam được ghi là VÍ DỤ GIẢ ĐỊNH; không xếp hạng hay khuyến nghị một cách chia tiền.

## Bảng biểu đồ

| Chương | Biểu đồ |
|---|---|
| CH00 | Thu nhập 15/25, chi 26, còn 14 |
| CH01 | Thác nước 50/50; tháng 12: 24/144 |
| CH02 | Thác nước theo tỷ trọng; tháng 12: 63/105 |
| CH03 | Cột chồng quỹ chung; tháng 12: 42/42/84 |
| CH04 | So sánh ba nhánh B6 và lớp thông tin luật |
| CH05 | Các nhóm tổ chức tiền trong nghiên cứu, không xếp hạng |
| CH06 | Đường nhạy chi 24/26/28/30 và quay về B6 |

## Lệnh đã chạy

- `PYTHONIOENCODING=utf-8 python data/long/ck-f4-vo-chong-chia-tien/analysis.py` — ghi `results.json`.
- `PYTHONIOENCODING=utf-8 python data/long/ck-f4-vo-chong-chia-tien/check.py` — `CK F4 check: OK (17 phép)`.
- `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-f4-vo-chong-chia-tien` — tổng 2.581 âm tiết.
- `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-f4-vo-chong-chia-tien --strict` — `0 lỗi, 0 cảnh báo`.
- `python scripts/long_gate.py ck-f4-vo-chong-chia-tien --min-syl 1900` — **TRƯỢT 19 lỗi**. Đây là cổng dựng hoàn chỉnh: topic W1 chưa có `spec.json`, scene/hud, TTS hay asset; cổng báo thiếu các mục đó và 0 cảnh. Theo `00-CHUNG-W1.md`, ticket W1 chỉ được ghi sáu file kịch bản/tính toán, không được dựng các đầu ra trên.

## Kiểm chứng và bàn giao

- Không có khẳng định trong kho nào bị bỏ vì nguồn yếu; các kết quả nghiên cứu quốc tế đều được trình bày như liên hệ/giới hạn diễn giải.
- Không có clip sheet hoặc thumbnail ở W1; chúng thuộc khâu dựng tiếp theo.
- Lỗi lint còn lại: không có. Cổng tổng không thể in ĐẠT trong phạm vi đầu ra được ticket W1 cho phép.
