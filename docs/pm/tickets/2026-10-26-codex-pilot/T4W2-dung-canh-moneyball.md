# T4W2 — DỰNG CẢNH + SPEC + SAY + PROMPT ẢNH AI cho `mim-moneyball`

Claude đã duyệt `script.md` và `factcheck.md` (2.216 âm tiết). **Không sửa lời đọc.** Không render, không upload, không chạy `thumb.py`, không gọi bot tạo ảnh.

**Báo cáo:** `docs/pm/tickets/2026-10-26-codex-pilot/T4W2-ket-qua.md`

## Chỉ đọc

| File | Đọc để làm gì |
|---|---|
| Ticket này | |
| `docs/codex/long-cheatsheet.md` | Cấu trúc cảnh, helper, thứ tự lệnh. **Đọc kỹ** |
| `docs/codex/long-rules.md` | Mục "Lỗi đã gặp" và "Ảnh AI" |
| `data/long/mim-katherine-johnson/gen_scenes.py` | **Khung để chép** |
| `data/long/mim-moneyball/script.md`, `facts.md` | Lời đọc, ảnh Commons, clip Pexels, đề xuất ảnh AI |

Không đọc engine, không đọc `build_long.py`, không grep repo.

## Làm

1. **Tạo `gen_scenes.py`:** chép khung từ `mim-katherine-johnson/gen_scenes.py` sang `data/long/mim-moneyball/gen_scenes.py`, rồi thay nội dung theo bảng "Thay những gì trong khung" của cheatsheet.
   - `TOPIC = "mim-moneyball"`; `TITLE` lấy từ dòng 1 của `script.md`.
   - `publish_at`: `2026-11-27T13:00:00Z`; `playlist`: "Công Nghệ Quanh Ta".
   - Mô-típ `LEDGER`/`ROWS` là "tấm bảng chờ một lần lên gôn", 8 ô (đã nêu trong báo cáo T4W1).
   - `GEO`: bản đồ nước Mỹ, ghim Oakland, Kansas City, Minnesota (nếu chương có nhắc).
   - `SAY`: phiên âm mọi tên Anh (Beane, DePodesta, Hatteberg, Oakland, Kansas, Athletics, Howe…) và thuật ngữ (OBP, ERA, SABR, MLB, AL…). Số thập phân kiểu ".339" đọc thành "ba trăm ba mươi chín phần nghìn" hoặc cách đọc tự nhiên tương đương.
2. **Viết `ai_prompts.md`** (≤ 6 ảnh) theo định dạng trong `long-rules.md`, dựa trên mục "Đề xuất ảnh AI" của `facts.md`.
   - Người thật chỉ vẽ theo dáng gốc, ở góc nghiêng quay đi hoặc từ phía sau.
   - Ảnh không có chữ, logo đội hay số áo.
   - Trong `IMGS`, mỗi ảnh khai `"EXT:ai:ai_NN"`. Trong `STAND`, gán cho mỗi ảnh AI một ảnh Commons thay tạm.
3. **Tải clip** bằng `python motion/long/pexels.py get mim-moneyball <id> …`. Chỉ lấy id có trong `facts.md`.
4. **Chạy theo "Thứ tự lệnh" trong cheatsheet:**
   - Ảnh AI chưa có, nên soát `html` bằng `gen_scenes.py --standin`.
   - Xong thì chạy `gen_scenes.py` bản thật, rồi chạy lại `script_lines.py`.
5. **Clip sheet:** chạy `clip_sheet.py`, mở `qa_clips.jpg` xem, thay clip lộ chữ, logo hoặc sai nghĩa.
6. **Cổng chất lượng:** chạy `python scripts/long_gate.py mim-moneyball --min-syl 1900`. Phải **ĐẠT**. Nếu chỉ vướng vì ảnh AI chưa có thì ghi rõ trong báo cáo.

## Báo cáo

- Số liệu từ `long_gate`.
- Danh sách ảnh Commons và clip đã dùng.
- Số ảnh AI cần tạo.
- Có lỗi lint nào phải sửa trong lúc làm không.
