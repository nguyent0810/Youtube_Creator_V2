# W1-1b — SỬA kịch bản `ck-f1-tro-cap-that-nghiep`

Đọc `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CHUNG-W1.md` (luật giữ nguyên) và báo cáo vòng trước `W1-1-ket-qua.md`. Mã báo cáo: `W1-1b`.

**Lỗi chặn:** tổng 1.930 âm tiết, dưới mức tối thiểu 2.300.

**Sửa:** viết thêm khoảng 450 âm tiết, đưa tổng về **2.350–2.600**. Thêm vào các chương CH02–CH05, mỗi chương 2–4 câu, chỉ dùng dữ kiện có trong `facts.md`.
- Mỗi câu thêm phải mang một con số hoặc một bước cụ thể vẽ được lên màn hình, ví dụ: điều kiện, ngày chờ, số tháng theo năm đóng, trần theo vùng, tình huống bị dừng hưởng.
- Không câu đệm. Không đổi CH00. Không đổi vòng mở.
- Cập nhật bảng "Biểu đồ" đầu `script.md` và `factcheck.md` cho các câu mới.

**Cổng:**
- chạy lại `analysis.py`, `check.py` → `OK`;
- `script_lines.py`;
- `studio_lint.py --strict` → 0 lỗi.

`long_gate` trượt vì thiếu phần dựng là bình thường ở W1. Chỉ báo các lỗi âm tiết hoặc nguồn.
