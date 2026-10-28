# W2-2 — DỰNG CẢNH `ck-f2-vien-phi-bhyt`
Đọc `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CHUNG-W2.md` và làm đúng. Mã báo cáo: `W2-2`.
- **Biểu đồ chính:** thác chi phí 30 → quỹ 16 → tự trả 9 → gánh nặng 11 triệu.
- Ảnh nhân vật: 6 ảnh `ai01`–`ai06` (xem `ai_prompts.md`, mục "dùng ở CHnn").
- **Vòng 2 (sau W1c, 27/10):** `gen_scenes.py` đã có từ vòng trước, nhưng CH00 và đầu CH01 của `script.md` đã viết lại.
  - Dựng lại cảnh CH00 và CH01 theo kịch bản mới. Biểu đồ đầu tiên là **số thật** có nguồn, neo vào câu 0–1. Nhân vật và ảnh `ai01` vào từ CH01.
  - Kiểm lại **mọi neo** của CH00 và CH01, vì số câu đã đổi.
  - Các chương khác giữ nguyên, chỉ chạy lại để chắc neo còn đúng.
- **Vòng 3 (Claude, 27/10, sau khi Codex hết quota): DỰNG LẠI TOÀN BỘ 7 chương.**
  - **Mô hình hoá đơn đã sửa** (bản cũ hụt 5 triệu không tên):
    - tổng 30 = 25 trong phạm vi + 5 ngoài phạm vi;
    - quỹ 80% của 25 = 20, đồng chi trả 5;
    - tự trả trên hoá đơn 10, ngoài hoá đơn 2, gánh nặng 12 (37,5%).
  - `script.md` và `results.json` đã cập nhật. **Mọi số trên cảnh phải lấy từ `results.json`.** Trong `gen_scenes.py` không được còn chữ "16 TRIỆU", "9 TRIỆU", "11 TRIỆU" hay "4 + 5".
  - Lời đọc đã đổi ở CH01, CH03, CH05, CH06. **Neo lại mọi cảnh** theo `chNN.json` mới.
  - `SPEC.title` và `youtube.titles[0]`: "Có Bảo Hiểm Y Tế Vẫn Trả 40%: Tiền Viện Phí Đi Đâu?". `publish_at`: "2026-11-20T13:00:00Z" (20:00 VN).
  - Lỗi cấu trúc cảnh của vòng trước, phải sửa:
    - `"range": [0, 30]` → chuỗi chữ;
    - cảnh `dots` dùng `items` là sai, `dots` cần `{total, groups}`; nếu không cần thì đổi sang `units` hoặc `bars`;
    - `race` có `dates` dạng chữ ("ĐẦU 2000") sẽ hiện sai nhãn, chuỗi tỉ lệ theo mốc thì dùng `bars`.
