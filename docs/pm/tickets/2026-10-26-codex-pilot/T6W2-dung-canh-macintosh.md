# T6W2 — DỰNG CẢNH + SPEC + SAY + PROMPT ẢNH AI cho `mim-macintosh-1984`

Claude đã duyệt `script.md` (2.271 âm tiết, lint 0 lỗi). **Không sửa lời đọc.** Không render, không upload, không chạy `thumb.py`, không gọi bot.

**Báo cáo:** `docs/pm/tickets/2026-10-26-codex-pilot/T6W2-ket-qua.md`

## Chỉ đọc

- Ticket này.
- `docs/codex/long-cheatsheet.md`, đọc toàn bộ.
- `docs/codex/long-rules.md`, mục "Lỗi đã gặp" và "Ảnh AI".
- **Khung để chép:** `data/long/mim-social-network/gen_scenes.py`. Bản này mới nhất và đã qua render: có `fix_anchors`, ghim bản đồ khớp `GEO`, thẻ chương đúng trường.
- Trong `data/long/mim-macintosh-1984/`: `script.md`, `facts.md`, các `chNN.json` (để lấy `lines`).

Không đọc engine, không grep repo.

## Làm

1. **Tạo `gen_scenes.py`:** chép khung sang `data/long/mim-macintosh-1984/gen_scenes.py`, thay nội dung.
   - `publish_at = 2026-11-30T13:00:00Z`.
   - `TITLE` lấy từ dòng 1 của `script.md`.
   - `SAY` phiên âm: Jobs, Macintosh, Apple, Xerox, PARC, Alto, Smalltalk, Lisa, Super Bowl, Hertzfeld… và các viết tắt (RAM, 128K, GUI…).
   - Mô-típ `LEDGER`/`ROWS`: mỗi dòng ≤ 26 ký tự.
2. **Thử kỹ thuật thư viện `object_continuity`** (vật nối: con chuột một nút, không logo). Ở mỗi chương có nhắc chuột, đặt **một cảnh có hình con chuột**, neo đúng vào câu nhắc chuột trong chương đó. Hình lấy từ ảnh Commons có giấy phép hợp lệ hoặc ảnh AI. Không lặp nguyên một ảnh quá 3 lần; dùng các góc hoặc phong cách khác nhau. Mục tiêu: người xem nhận ra cùng một vật đi qua nhiều mốc.
3. **Thử kỹ thuật thư viện `pixel_art`:** 1–2 ảnh AI phong cách pixel đơn sắc như màn hình năm 1984. Đặt ở chương nói về giao diện đồ hoạ.
4. **Thử kỹ thuật thư viện `hook_frame_dau_la_thumbnail` ở cảnh:**
   - Cảnh đầu tiên sau thẻ chương 0 là **chữ lớn "24.01.1984" cộng lời hứa ngắn**, dùng `date` hoặc `kinetic`.
   - Cảnh này phải neo vào **từ đầu tiên của câu 0**, không để nền trống chờ.
5. **Viết `ai_prompts.md`** (≤ 6 ảnh). Mỗi tiêu đề mục dùng đúng `## ai_NN.png — …`.
   - Không chữ, không logo Apple.
   - Người thật chỉ vẽ theo dáng gốc, ở góc nghiêng quay đi hoặc từ phía sau.
6. **Clip:** tải bằng `pexels.py get` (tải theo id được). Clip dọc thì thay.
7. **Neo:**
   - Neo tăng dần, không neo vào chữ số.
   - Cảnh `question`/`slam` chỉ phủ câu của nó. Câu kế tiếp phải có cảnh riêng để không đứng hình quá 12 giây.
   - Ghim bản đồ (nếu có) phải trùng tên trong `GEO`.
8. **html:** chạy `gen_scenes.py --standin` → `script_lines.py` → `build_long.py tts` (đủ 8 chương) → `build_long.py html`. Phải ra **8/8, không Error**. Sau đó chạy bản thật: `gen_scenes.py`, rồi `script_lines.py`.
9. **Kiểm clip:** chạy `clip_sheet.py`, **mở ảnh ra xem**. Loại clip có logo hoặc chữ đọc được.
10. **Cổng:** `python scripts/long_gate.py mim-macintosh-1984 --min-syl 1900` phải **ĐẠT**, trừ khi chỉ còn thiếu ảnh AI.

## Báo cáo

- Kết quả html 8/8, `long_gate`, clip sheet.
- Chương nào có cảnh chuột, dùng ảnh nào.
- Ảnh pixel nằm ở đâu.
- Số ảnh AI cần tạo.
