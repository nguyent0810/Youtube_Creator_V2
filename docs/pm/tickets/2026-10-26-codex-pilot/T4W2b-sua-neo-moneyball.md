# T4W2b — Sửa neo cảnh `mim-moneyball` cho tới khi `html` qua

**Kết quả:** `docs/pm/tickets/2026-10-26-codex-pilot/T4W2b-ket-qua.md`

| Mục | Nội dung |
|---|---|
| **Chỉ sửa** | `data/long/mim-moneyball/gen_scenes.py`, phần `ch00()`–`ch07()` |
| **Không sửa** | `script.md`, `SAY`, `ROWS`, `spec`. Không render, không upload |
| **Chỉ đọc** | Ticket này, `docs/codex/long-cheatsheet.md` (mục "Helper"), `gen_scenes.py`, các `chNN.json` (lấy `lines` để biết câu thứ mấy có chữ gì) |
| **Không đọc** | Engine |

## Bối cảnh

Claude đã tách 3 câu dài: ch01 câu 7, ch02 câu 1, ch07 câu 10. Số thứ tự câu phía sau vì thế lệch đi. `gen_scenes.py` hiện có `fix_anchors` (tự đổi neo chữ số, tự tìm câu gần nhất) và `SPLIT`/`shift_anchors`.

Lỗi còn lại khi chạy `html` thuộc 2 loại:

1. **`câu i không có chữ 'x'`**: neo trỏ sai câu.
2. **`cảnh N quá ngắn … trùng mốc với cảnh N-1`**: hai cảnh liền nhau neo vào cùng một chỗ, hoặc cảnh sau neo vào một từ **đứng trước** neo của cảnh trước. Neo phải tăng dần theo thứ tự cảnh: (câu, vị trí từ) của cảnh sau phải lớn hơn của cảnh trước.

## Làm (lặp tới khi qua)

1. Chạy:
   ```
   PYTHONIOENCODING=utf-8 python data/long/mim-moneyball/gen_scenes.py
   python motion/long/script_lines.py mim-moneyball
   python motion/long/build_long.py mim-moneyball html
   ```
2. Đọc lỗi. Mở `chNN.json` của chương bị lỗi, xem `lines`, rồi **sửa neo trực tiếp** trong hàm `chNN()`. Chọn một từ có thật trong câu đúng, không phải chữ số, đứng sau neo của cảnh trước.
3. Lặp lại bước 1 cho tới khi `html` in đủ 8 dòng `chNN: … -> …html`, không còn `Error`.
4. Cảnh báo "tràn chữ beat2" hay "dòng sổ dài": sửa nếu dễ, bằng cách rút gọn chữ trong cảnh hoặc bỏ `size`.
5. Chạy `python scripts/long_gate.py mim-moneyball --min-syl 1900` (phải in **ĐẠT**) và `python motion/long/clip_sheet.py mim-moneyball`.

## Báo cáo

- Danh sách neo đã sửa: chương, cảnh, neo cũ → neo mới.
- Kết quả của `html`, `long_gate`, `clip_sheet`.
