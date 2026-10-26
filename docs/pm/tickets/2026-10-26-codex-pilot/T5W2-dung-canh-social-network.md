# T5W2 — DỰNG CẢNH + SPEC + SAY + PROMPT ẢNH AI cho `mim-social-network`

Claude đã duyệt `script.md` (2.261 âm tiết, lint 0 lỗi). **Không sửa lời đọc.** Không render, không upload, không chạy `thumb.py`, không gọi bot.

**Báo cáo:** `docs/pm/tickets/2026-10-26-codex-pilot/T5W2-ket-qua.md`

## Chỉ đọc

| File | Ghi chú |
|---|---|
| Ticket này | |
| `docs/codex/long-cheatsheet.md` | Toàn bộ, nhất là "Bài học Moneyball" |
| `docs/codex/long-rules.md` | Mục "Lỗi đã gặp" và "Ảnh AI" |
| `data/long/mim-moneyball/gen_scenes.py` | **Khung để chép.** Bản mới nhất, đã có `fix_anchors` (tự đổi neo chữ số, tự tìm câu gần nhất). **Bỏ** `SPLIT`/`shift_anchors` vì bài này không tách câu sau dựng |
| `data/long/mim-social-network/script.md`, `facts.md`, các `chNN.json` | Để biết `lines` |

Không đọc engine, không grep repo.

## Làm

1. **Chép khung** sang `data/long/mim-social-network/gen_scenes.py` rồi thay nội dung.
   - `publish_at`: `2026-11-29T13:00:00Z`.
   - `GEO`: bản đồ vùng Boston/Cambridge, ghim Harvard. Nếu engine không có đủ dữ liệu bản đồ cho vùng nhỏ thì dùng bản đồ nước Mỹ, ghim Cambridge, Massachusetts.
   - `SAY`: phiên âm mọi tên Anh (Zuckerberg, Harvard, Crimson, Kirkland, Winklevoss, Saverin…) và viết tắt.
   - **Mô-típ "bản đồ kết nối":** dùng `LEDGER`/`ROWS`, mỗi chương thêm một dòng. **Mỗi dòng ≤ 26 ký tự** để không tràn thẻ.
2. **Viết `ai_prompts.md`** (≤ 6 ảnh). Mỗi mục bắt đầu bằng `## ai_NN.png — …`, **đúng 2 dấu `#`**.
   - Người thật chỉ vẽ theo dáng gốc, ở góc nghiêng quay đi hoặc từ phía sau.
   - Không chữ, không logo Facebook hay Harvard.
3. **Tải clip:** `python motion/long/pexels.py get mim-social-network <id> …`. Tải thẳng theo id được. Clip in "không có bản ngang" thì thay bằng `pexels.py search`.
4. **Neo:**
   - Tăng dần theo thứ tự cảnh.
   - Không neo vào chữ số.
   - Phần tử đầu tiên của cảnh `org`/`timeline` phải neo **cùng** mốc với cảnh, nếu không sẽ có màn trống quá 1 giây.
5. **Chạy html:**
   - Chạy `gen_scenes.py --standin` → `script_lines.py` → `build_long.py tts` (đủ 8 chương) → `build_long.py html`.
   - Phải in đủ **8 dòng `chNN: … -> …html`, không có `Error`**. Lỗi thì sửa neo rồi chạy lại.
   - Sau đó chạy lại bản thật: `gen_scenes.py` rồi `script_lines.py`.
6. **Soát clip:**
   - Chạy `clip_sheet.py` rồi **mở `qa_clips.jpg` xem từng clip**.
   - Clip lộ logo sân, trường hay hãng, hoặc chữ đọc được, thì thay.
7. **Cổng cuối:** chạy `python scripts/long_gate.py mim-social-network --min-syl 1900`, phải ra **ĐẠT** (trừ khi chỉ thiếu ảnh AI).

## Báo cáo

- Kết quả `html` (8/8), `long_gate`, `clip_sheet`, kèm danh sách clip đã thay.
- Số ảnh AI cần tạo.
