# GH-26 fix report

## Diff tóm tắt
- `tests/test_branch_gate.py`: ca dirty nay tạo `output/x.txt` chưa track; thêm `test_final_commit_records_clean_working_tree` kỳ vọng `working_tree: clean`.
- `scripts/precommit_size.py`: khối `__main__` thêm `sys.path.insert(0, ROOT)`, `utf8_console()` trước `sys.exit(main())` (exit code giữ nguyên).
- `motion/long/branch_gate.py`: khối `__main__` thêm `sys.path` (ROOT = parents[2]) và `utf8_console()` trước `refuse()`.

## Kết quả
- `py_compile` 3 file: OK.
- pytest 3 file: 12 passed, 1 failed. `test_branch_gate` và `test_precommit_size` xanh. `test_console` chỉ còn các tên cũ: qa_mark, commons_find, dryplan, unschedule, bang_tra_look, bud_variety, script_lint (không còn precommit_size.py, branch_gate.py).
