# W1-3b — SỬA kịch bản `ck-f3-tien-mung-cuoi`

Đọc `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CHUNG-W1.md` (luật giữ nguyên) và báo cáo vòng trước `W1-3-ket-qua.md`. Mã báo cáo: `W1-3b`.

**Lỗi chặn:**
1. CH00 dài 305 âm tiết, vượt giới hạn 230.
2. Tổng 2.020 âm tiết, dưới mức tối thiểu 2.300.

**Sửa:**
- **CH00:** rút về ≤ 220 âm tiết. Giữ con số mở đầu, nghịch lý và vòng mở. Phần cắt ra thì chuyển xuống CH01 nếu vẫn cần.
- **Tổng:** đưa về **2.350–2.600**. Thêm 2–4 câu vào mỗi chương CH02–CH05, chỉ dùng `facts.md`. Mỗi câu thêm mang một con số vẽ được: tháng, dịp, mức VÍ DỤ GIẢ ĐỊNH theo quan hệ, tỉ lệ so với lương, khung trần.
- Không câu đệm.
- Cập nhật bảng "Biểu đồ" và `factcheck.md`.

**Cổng:**
- chạy lại `analysis.py`, `check.py` → `OK`;
- `script_lines.py`;
- `studio_lint.py --strict` → 0 lỗi.

`long_gate` trượt vì thiếu phần dựng là bình thường ở W1.
