# GH-26 · Codex vòng sửa: 2 test mới đỏ

Lead chạy pytest ngoài sandbox: 748 passed, 15 failed (14 lỗi nền cũ + 1 mới), và `test_console` có thêm 2 tên mới.

1. `tests/test_branch_gate.py::test_final_commit_records_head_dirty_state_and_time` đỏ: test tạo thư mục `output` rỗng rồi kỳ vọng `working_tree: dirty`, nhưng Git không thấy thư mục rỗng nên code ghi đúng `clean`. **Sửa test, không sửa code**: tạo một file chưa track (vd. `output/x.txt`) để có trạng thái bẩn; thêm một ca sạch kỳ vọng `working_tree: clean`.
2. `tests/test_console.py`: `scripts/precommit_size.py` và `motion/long/branch_gate.py` in ra console mà chưa gọi `factory.console.utf8_console()`. Thêm vào khối `__main__`/`main` theo đúng mẫu các CLI khác (vd. `motion/long/img_sheet.py`). Các tên cũ khác trong danh sách không thuộc phạm vi.

## Được ghi
`tests/test_branch_gate.py`, `scripts/precommit_size.py`, `motion/long/branch_gate.py`, báo cáo `docs/pm/tickets/GH-26-fix-report.md`. Không commit, không render.

## Báo cáo
Diff tóm tắt, `py_compile` các file sửa.
