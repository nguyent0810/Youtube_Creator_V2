# W1-2 — Kết quả ck-f2-vien-phi-bhyt

## Đã làm

- Viết `data/long/ck-f2-vien-phi-bhyt/script.md`: bảy chương CH00–CH06 theo lộ trình “bóc hoá đơn”, dùng Minh và toàn bộ con số hóa đơn dưới nhãn **VÍ DỤ GIẢ ĐỊNH**.
- Viết `factcheck.md` với 16 URL đã nằm trong kho dữ kiện duyệt; không thêm dữ kiện ngoài kho.
- Viết `analysis.py`, `check.py`; đã sinh `results.json`.
- `script_lines.py` đã sinh `ch00.json` đến `ch06.json`.

## Số liệu kịch bản

- Tổng: **2.694 âm tiết**, 171 câu.
- CH00: **203 âm tiết**, dưới giới hạn 230.
- Vòng mở chính: mở tại CH00 câu 1, “Ba mươi triệu trong bảy ngày… mười một triệu”; đóng tại CH06 câu 31–33, đối chiếu lại ba mươi, mười sáu, chín và mười một triệu cùng giới hạn của từng lớp chi phí.

| Chương | Biểu đồ |
|---|---|
| CH00 | Waterfall tổng 30 → quỹ 16 → trên hóa đơn 9 → gánh nặng 11 triệu |
| CH01 | Dots 7 ngày, 5 dòng KCB, 3 khoản ngoài hóa đơn |
| CH02 | Timeline các mốc 2025–2026 |
| CH03 | Cột 80/95/100% và ngưỡng 5 năm liên tục |
| CH04 | Cột điều kiện 100/100/50% mức hưởng |
| CH05 | Waterfall hoàn chỉnh 30 → 16 → 9 → 11 triệu |
| CH06 | Đường chi tiền túi khoảng 60% → 40% → mục tiêu dưới 30% |

## Lệnh đã chạy

```text
PYTHONIOENCODING=utf-8 python data/long/ck-f2-vien-phi-bhyt/analysis.py
PYTHONIOENCODING=utf-8 python data/long/ck-f2-vien-phi-bhyt/check.py
→ F2 check: OK (8 phép)

PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-f2-vien-phi-bhyt
→ TỔNG 2.694 âm tiết

PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-f2-vien-phi-bhyt --strict
→ 0 lỗi, 6 cảnh báo về mật độ câu ngắn

PYTHONIOENCODING=utf-8 python scripts/long_gate.py ck-f2-vien-phi-bhyt --min-syl 1900
→ TRƯỢT (19 lỗi)
```

## Trạng thái cổng tổng

Không thể báo hoàn tất cổng `long_gate.py`: ticket W1 chỉ cho phép ghi sáu file kịch bản/tính toán nêu trong `00-CHUNG-W1.md`, trong khi `long_gate.py` yêu cầu phần dựng chưa thuộc ticket này: `spec` có `youtube`/`say`, HUD và tối thiểu năm loại cảnh mỗi chương, cùng TTS đủ bảy chương. Cổng báo thiếu đúng các đầu ra đó (19 lỗi); không có lỗi về âm tiết hay URL nguồn.

Không tạo clip sheet hoặc thumbnail vì W1 không cho phép dựng cảnh/render/thumbnail. Đường dẫn hiện chưa có: `output/long/ck-f2-vien-phi-bhyt/qa_clips.jpg`; thumbnail chưa có: `motion/long/thumbs/ck-f2-vien-phi-bhyt_t1.html`.

## Kiểm chứng nội dung

Không có khẳng định nào bị bỏ vì nguồn yếu. Các mốc 2024, 2025, 2026, 2028–2030 và 2030 trong lời đọc đều có dòng nguồn trong `factcheck.md`. Các số tiền của Minh là phép tính giả định, được `check.py` kiểm lại.
