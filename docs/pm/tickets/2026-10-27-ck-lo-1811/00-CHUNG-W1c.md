# Luật chung cho ticket SỬA MỞ ĐẦU (W1c), theo Content Brief bản 2 đã duyệt 27/10

Đọc:
- `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CONTENT-BRIEF.md`, mục của bài mình;
- `docs/codex/long-rules.md`, hai mục cuối "Chiến lược Long 45 ngày" và "Cập nhật Áp dụng ngay";
- `script.md`, `facts.md`, `factcheck.md` của bài.

Không đọc gì khác.

**Chỉ ghi:**
- `script.md`
- `factcheck.md`
- `analysis.py`, `check.py`, `results.json` (chỉ khi phải đổi số)
- `docs/pm/tickets/2026-10-27-ck-lo-1811/<mã>-ket-qua.md`

## Sửa

1. **Viết lại CH00** theo "Hook 30 giây" trong brief.
   - **Câu 0** là sự kiện, con số thật hoặc câu hỏi thật, lấy từ `facts.md` và có nguồn. Không nhắc nhân vật ví dụ trong CH00.
   - Trong 2 câu đầu nói ra con số mà biểu đồ dữ liệu thật đầu tiên sẽ vẽ.
   - Có nghịch lý và một vòng mở chính, đóng ở CH06.
   - Nói câu hỏi trung tâm của brief.
   - CH00 ≤ 230 âm tiết.
2. **Đưa nhân vật ví dụ vào đầu CH01**, kèm một câu nói rõ "đây là ví dụ giả định để tính". Bỏ các câu trùng ở CH01 nếu cần.
3. **Dòng 1 = tiêu đề (1) trong brief.** Hai tiêu đề còn lại ghi vào dòng "Tiêu đề phụ".
4. **Đầu `script.md` thêm 3 mục:**
   - "Câu hỏi trung tâm";
   - "5 câu trước khi viết";
   - bảng "Bước lập luận": các mốc khoảng 3–5 phút, mỗi mốc một bước tiến của lập luận, ghi chương và câu.
5. Cập nhật bảng "Biểu đồ" cho CH00 và CH01. Biểu đồ đầu tiên là **số thật** có nguồn.
6. Giữ nguyên CH02–CH06, trừ chỗ phải nối câu.
7. Tổng âm tiết: **1.900–2.700** (8–13 phút).

## Cổng

- `analysis.py` và `check.py` → `OK` (chạy lại nếu có đổi số).
- `script_lines.py` (C6 dùng thêm `--allow-repeat-line`).
- `studio_lint.py --strict` → 0 lỗi.

`long_gate` trượt vì chưa có cảnh là bình thường.

## Báo cáo

- CH00 mới, nguyên văn.
- Tổng âm tiết và âm tiết CH00.
- Câu 0 lấy từ dữ kiện số mấy trong `facts.md`.
