# GH-26 · Codex: 5 chốt chặn đã duyệt (từ #11 và #12)

Issue: https://github.com/nguyent0810/Youtube_Creator_V2/issues/26. Bối cảnh: `docs/pm/tickets/GH-11-report.md`, comment cuối của #11 và #12. Chủ kênh duyệt 02/11/2026.

## Được ghi
- `motion/long/build_long.py`: chỉ chỗ gọi cổng trong `do_render` (bản thật, không `--draft`) và `do_final`
- `motion/long/publish_long.py`: chỉ chỗ gọi cổng
- `motion/long/audio_lint.py`
- `scripts/long_gate.py`
- file mới `motion/long/branch_gate.py`
- file mới `.githooks/pre-commit` và `scripts/precommit_size.py`
- `docs/codex/long-rules.md`: thêm luật, đúng văn phong file
- test mới/sửa trong `tests/`
- báo cáo `docs/pm/tickets/GH-26-report.md`

**Không:** sửa `data/long/**`, hạ bất kỳ ngưỡng nào, render, commit, chạy `git config`, chạy `git fetch`/mạng.

## Việc
1. **Nhánh thiếu `origin/main`** (`branch_gate.py`). Trước `render` bản thật, `final` và `publish`: chạy `git merge-base --is-ancestor origin/main HEAD`. Mã 1 → chặn, in hướng dẫn `git fetch origin && git merge origin/main`. Không có ref `origin/main` hoặc không phải repo git → chặn kèm thông báo rõ. Không thêm cờ bỏ qua. Bản `--draft` không bị chặn. Test bằng repo git tạm (`tmp_path`), không đụng repo thật.
2. **Hook trước commit**: `.githooks/pre-commit` gọi `python scripts/precommit_size.py`, chặn khi có file staged > 50 MB (đọc kích thước blob staged, không phải file trên đĩa). Test logic Python bằng repo tạm. Lead sẽ tự bật `core.hooksPath`.
3. **Commit hash trong dấu QA của final**: sau khi `final.mp4` ghi xong (và SRT xong), ghi `output/long/<topic>/final.commit` gồm commit HEAD và cờ working tree bẩn/sạch, kèm thời điểm. Không đọc được git → `final` lỗi.
4. **Ảnh dọc thiếu `focus`** trong `scripts/long_gate.py` (~dòng 113–124): từ `warn` thành lỗi chặn, cùng cách các lỗi khác của file đang chặn.
5. **`audio_lint` bước final cho MIM/CK**: hiện `block = channel == "CL"` (`build_long.py` ~dòng 1210). Tách:
   - kiểm kỹ thuật (`check_parts`: clip/đỉnh sfx…; `check_final`: true peak sau AAC; công cụ đo hỏng) → **chặn mọi kênh**;
   - kiểm buzz giọng `check_voices` (ngưỡng lấy theo bộ lọc giọng CL) → giữ chặn CL, kênh khác cảnh báo như cũ. Ghi rõ lý do trong docstring.
   Không đổi ngưỡng nào. Khi `final` bị chặn vì kiểm kỹ thuật thì xóa `final.mp4` hỏng như nhánh CL hiện tại.
6. **Hồi quy (chỉ đọc, không render):**
   - chạy `branch_gate` trên repo thật, ghi kết quả;
   - chạy `long_gate.py` trên mọi topic MIM/CK có ch*.json, liệt kê topic trượt vì ảnh dọc thiếu `focus`;
   - chạy `audio_lint.check_final` trên mọi `output/long/<mim-*|ck-*>/final.mp4` có sẵn, liệt kê file sẽ bị chặn.
7. Chạy `python -m pytest -q` các file test liên quan. Nếu sandbox chặn thư mục tạm thì ghi lại, Lead sẽ chạy ngoài sandbox.

## Báo cáo `docs/pm/tickets/GH-26-report.md`
Cách làm từng chốt (file:dòng), danh sách test, bảng hồi quy mục 6, kết quả pytest.
