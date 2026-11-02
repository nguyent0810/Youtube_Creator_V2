# Báo cáo GH-26 · 02/11/2026

Không render, không thay đổi `data/long/**`, không gọi mạng/Git fetch, không đổi lịch,
không đăng và không commit.

## Các chốt đã làm

| Chốt | Cách làm |
|---|---|
| Nhánh | Thêm `motion/long/branch_gate.py:20-44`. Cổng kiểm tra đúng quan hệ `git merge-base --is-ancestor origin/main HEAD`; phân biệt không phải Git repo, thiếu ref `origin/main`, nhánh chưa chứa main và lỗi Git khác. `build_long.py:1146-1148` gọi trước render thật (draft bỏ qua), `build_long.py:1215`/`1304` gọi trước final (trước cả lúc xóa final cũ), `publish_long.py:103` gọi trước publish. Không có cờ bỏ qua. |
| Pre-commit | Thêm `.githooks/pre-commit`, gọi `python scripts/precommit_size.py`. `scripts/precommit_size.py:21-37` đọc tên file thay đổi từ index và kích thước blob `:<path>`, chặn khi lớn hơn 50 MiB; không stat file worktree. Không chạy `git config`; Lead tự bật hooksPath như ticket nói. |
| Dấu final | `build_long.py:1196-1211` ghi `output/long/<topic>/final.commit` chỉ sau khi `final.mp4` và SRT đều xong: HEAD, `working_tree: clean|dirty`, thời điểm. Không đọc được Git thì final lỗi. |
| Ảnh dọc | `scripts/long_gate.py:124` đổi ảnh dọc thiếu `focus` từ cảnh báo thành `err`, nên CLI trả `TRƯỢT`. |
| Audio | `audio_lint.py:1-16, 166-173` ghi rõ chính sách: lỗi kỹ thuật (cạnh nối, clip cứng, true peak sau AAC, lỗi đo) chặn mọi kênh; buzz giọng chỉ chặn CL vì ngưỡng theo bộ lọc CL. `build_long.py:1232-1266` tách hai luồng; lỗi `check_final` hoặc lỗi đo sau AAC xóa `final.mp4` trước khi chặn. Không đổi ngưỡng. |
| Luật | Thêm A12 ở `docs/codex/long-rules.md:70`. |

## Test và kiểm tra

- Thêm test: `tests/test_branch_gate.py`, `tests/test_precommit_size.py`, `tests/test_long_gate_focus.py`, `tests/test_final_audio_gate.py`; sửa `tests/test_sheet_gate.py` để kiểm cổng nhánh render thật/draft.
- `python -m py_compile motion/long/branch_gate.py scripts/precommit_size.py motion/long/build_long.py motion/long/publish_long.py motion/long/audio_lint.py scripts/long_gate.py` — đạt.
- `python motion/long/branch_gate.py` trên repo thật — `ĐẠT (HEAD đã chứa origin/main)`.
- Pytest không dùng `tmp_path`: 18 passed. Lệnh đã chạy:
  `python -m pytest -q tests/test_sheet_gate.py tests/test_audio_lint.py tests/test_publish_long_preflight.py::test_main_checks_before_upload_and_creates_pub_dir tests/test_mim_long.py::test_sync_covers_kin_overlays_and_respects_a_min_time tests/test_mim_long.py::test_lab_theme_is_exempt_from_the_look_rule tests/test_mim_long.py::test_mim_long_slugs_are_exportable_for_manual_upload tests/test_mim_long.py::test_mim_description_links_cc_by_licence tests/test_ck_long.py::test_script_marks_viewer_questions tests/test_ck_long.py::test_a_track_can_be_shared_by_several_channels_but_never_leaks_to_others tests/test_ck_long.py::test_sync_gives_every_on_screen_token_a_time_even_symbols`.
- Pytest có `tmp_path` (bao gồm test mới cho Git repo tạm) bị sandbox chặn trước setup: `PermissionError [WinError 5]` khi pytest quét `C:\Users\Tung-QA\AppData\Local\Temp\pytest-of-Tung-QA`. Thử lại với `--basetemp .pytest-gh26-tmp` cũng bị `WinError 5` lúc quét chính basetemp trong workspace. Lượt đầu có 17 passed, 15 errors do giới hạn này. Lead cần chạy các test có `tmp_path` ngoài sandbox.
- Thư mục tạm `.pytest-gh26-tmp` do lần fallback tạo ra cũng không thể đọc/xóa từ sandbox sau đó; Lead có thể xóa nó khi chạy ngoài sandbox.
- Cảnh báo còn lại khi pytest: pytest không ghi được `.pytest_cache` (`WinError 5`); không có lỗi cú pháp Python. Không chạy render hay lint/render gate khác vì ticket cấm render.

## Hồi quy chỉ đọc

| Hạng mục | Phạm vi | Kết quả |
|---|---|---|
| Cổng nhánh | Repo thật | ĐẠT; HEAD đã chứa `origin/main`. |
| `long_gate.py` | 55 topic MIM/CK có `ch*.json`, `--min-syl 1900` | 6 ĐẠT, 49 TRƯỢT (có cả lỗi cũ khác của từng bài). Các topic trượt **do ảnh dọc thiếu `focus`**: `mim-ai-70`, `mim-ai-hallucinate`, `mim-ai-jobs`, `mim-apollo-1202`, `mim-dich-may`, `mim-google-maps-kal007`, `mim-katherine-johnson`, `mim-ke-huy-diet-petrov`, `mim-macintosh-1984`, `mim-moneyball`, `mim-oppenheimer-feynman`, `mim-siri-susan-bennett`, `mim-social-network`, `mim-turing-bombe`. Không topic CK nào báo lỗi focus. |
| `audio_lint.check_final` | 21 `output/long/<mim-*|ck-*>/final.mp4` có sẵn | 21/21 ĐẠT; true peak nằm trong khoảng −2.1 đến −1.0 dBTP, không file nào sẽ bị chặn bởi cổng true peak. |

## Ghi chú giao nhận

- Không có khẳng định nội dung/video cần factcheck trong ticket kỹ thuật này.
- Không có clip sheet hoặc thumbnail mới: ticket cấm render và không yêu cầu dựng topic.
