# GH-24 · Codex: tờ soát ảnh tĩnh + chặn render khi chưa soát (A3, A10)

- Issue: https://github.com/nguyent0810/Youtube_Creator_V2/issues/24
- Bối cảnh: mục C trong `docs/pm/2026-10-29-jobs-1985-loi-pipeline.md` (Jobs 1985). Có 3 lỗi chỉ phát hiện khi xem khung hình: ảnh `nextcube` lộ máy Minitel, `sculley06` lộ thẻ tên, và clip lộ chữ "MacBook Pro". Lỗi clip xảy ra dù `clip_sheet.py` đã có sẵn, vì không ai bắt buộc phải soát tờ đó.
- **Chạy sau GH-23**, vì cả hai cùng sửa `build_long.py`.

## Được ghi

- `motion/long/img_sheet.py` (mới)
- `motion/long/clip_sheet.py`
- `motion/long/build_long.py`: chỉ phần chặn trong `do_render` / `cmd_render`
- `tests/test_img_sheet.py` và `tests/test_sheet_gate.py` (mới)
- báo cáo `docs/pm/tickets/GH-24-report.md`

Không làm: sửa `data/long/**`, render video, commit.

## Việc

1. **A3 `img_sheet.py <topic>`** → `output/long/<topic>/qa_imgs.jpg`.
   - Mỗi ảnh nằm trong một ô, gồm:
     - ảnh gốc thu nhỏ, có vẽ **khung crop 16:9** đúng như engine sẽ cắt. Khung tính theo `focus` của từng lần dùng; ảnh được dùng với nhiều `focus` thì vẽ nhiều khung.
     - bên cạnh là bản crop 16:9 thực tế.
     - nhãn gồm key ảnh, các cảnh dùng ảnh (`chNN#i`), loại cảnh và số lần dùng.
   - Cảnh `print` không cắt 16:9. Với cảnh này, vẽ khung theo cách `B.print` trong `casewide.js` xếp ảnh.
   - Dùng Pillow, không dùng ffmpeg `drawtext` (từng segfault vì fontconfig). Nhãn cần font có dấu tiếng Việt: tìm font mà repo đang dùng.
2. **A10, dấu "đã soát".** Thêm cờ `--ok` cho `clip_sheet.py <topic>` và `img_sheet.py <topic>`.
   - Cờ này ghi `qa_clips.ok` / `qa_imgs.ok`, chứa hash của danh sách đang dùng: clip id và `ms`, hoặc key ảnh và `focus`.
   - Người soát (agy hoặc Claude) chạy `--ok` **sau khi đã xem** tờ soát. Cờ không tự chạy khi dựng tờ.
3. **Chặn render.** `build_long.py render` (cả `--draft`) và `final` từ chối khi thiếu dấu, hoặc khi hash trong dấu không còn khớp danh sách hiện tại (cảnh đã đổi sau khi soát).
   - Thông báo phải nói rõ cần chạy lệnh nào.
   - Topic không có clip thì không cần `qa_clips.ok`; không có ảnh thì không cần `qa_imgs.ok`.
4. **Test.**
   - Hash ổn định.
   - Đổi `focus` hoặc thay clip thì dấu thành cũ.
   - Render bị chặn khi thiếu dấu hoặc dấu cũ; qua khi dấu khớp. Test cổng chặn bằng cách gọi hàm, không render thật.
   - `python -m pytest -q tests/` phải xanh.
5. **Chạy thử** `img_sheet.py mim-jobs-1985`. Mở ảnh kết quả và tự kiểm 3 điều: ảnh `nextcube` không còn trong bài; khung crop của `sculley06`; ảnh AI có nằm trong tờ.
   - **Không** chạy `--ok` cho Jobs 1985: Lead sẽ tự soát.

## Báo cáo `docs/pm/tickets/GH-24-report.md`

Gồm:
- lệnh đã chạy;
- đường dẫn tờ soát Jobs 1985;
- định dạng file dấu;
- kết quả pytest;
- danh sách topic MIM/CK hiện chưa có dấu: tất cả, nên ghi ra để biết lượng việc soát lại khi bật cổng.
