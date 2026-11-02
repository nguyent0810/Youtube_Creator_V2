# GH-23/GH-25 — báo cáo vòng sửa Codex

## Đã làm

- Chuyển kiểm A1 sang cảnh đã qua `plan()`: source chỉ kiểm khai báo ảnh, còn contract cảnh kiểm trên `data.js` đã lập kế hoạch. Vì vậy `hitAt`, `typeAt`, `countAt` không còn bị coi là key engine lạ trước khi được đổi thành `at`.
- Bổ sung contract cho `counter.img`, `calendar`/`seismo.label` dạng chuỗi và `kinetic.lay` (trường do `plan()` sinh ra).
- Sửa `factcheck_lint`: bỏ giá trị 0, số thứ tự chương, nhãn trục/tháng đã nhận diện; số có đơn vị chỉ còn một dạng chuẩn, đồng thời hiểu dấu phẩy thập phân của `0,8 TRIỆU` là `800000`.
- Thêm `utf8_console()` ở `scene_params.py`, `img_sheet.py`, `factcheck_lint.py`, `coverage_lint.py`, `scene_rules.py`, `clip_sheet.py`; mỗi CLI tự thêm repo root vào import path khi chạy trực tiếp.
- Bổ sung A4/A7/A8/A9/A10/A11 vào `docs/codex/long-rules.md`.
- Thêm hồi quy trong `tests/test_scene_params.py` và `tests/test_factcheck_lint.py`.

## A1 trước / sau

| Topic | A1 trước | A1 sau |
|---|---:|---:|
| golden | 51 | 0 |
| mafia | 102 | 0 |
| kowloon | 65 | 0 |
| ripper | 49 | 0 |
| shanghai | 46 | 0 |
| yakuza | 32 | 0 |
| bulger | 65 | 0 |
| capone | 73 | 0 |
| escobar | 71 | 0 |
| mim-ke-huy-diet-petrov | 23 | 0 |

Lệnh: `python motion/long/scene_params.py golden mafia kowloon ripper shanghai yakuza bulger capone escobar mim-ke-huy-diet-petrov`.

Lệnh trả mã 1 vì các cổng khác vẫn đúng: golden 5 A8, mafia 1 A8, kowloon 8 A8, ripper 13 A8, shanghai 12 A8, yakuza 7 A8, bulger 1 A8, capone 4 A8, escobar 5 A8; Petrov 66 A7 và 2 A9. Không còn A1. Đây là lỗi dữ liệu/cảnh có thật, ngoài phạm vi ticket; không sửa `data/long/**`.

Không còn A1 REAL. Bằng chứng cho ba alias là chính `build_long.py:499`, `:514` và nhánh `counter` trong `plan()` — tất cả đổi alias sang `at` trước khi scene được đưa vào engine. `kinetic.lay` cũng xuất hiện sau `assign_beats()` trong `plan()`, nên được cho phép ở contract hậu-plan.

## Factcheck CK-F3

Trước sửa: 10 lỗi. Sau sửa, `python motion/long/factcheck_lint.py ck-f3-tien-mung-cuoi` còn 6 lỗi và trả mã 1:

| Số chuẩn hoá | Nhận định |
|---|---|
| 1 | FALSE POSITIVE: nhãn lịch “LỊCH TỪ THÁNG 1”. |
| 8 | Mixed: nhãn lịch “LỊCH TỚI THÁNG 8” là false positive, nhưng còn có nhãn ledger `0,8` không có đơn vị/nguồn rõ ràng. |
| 13 | REAL: nhãn ledger `1,3` không có đơn vị/nguồn rõ ràng. |
| 800000 | REAL: callout `0,8 TRIỆU` không có mục factcheck/research tương ứng. |
| 1500000 | REAL: callout `1,5 TRIỆU` không có mục factcheck/research tương ứng. |
| 2800000 | REAL: callout `2,8 TRIỆU` không có mục factcheck/research tương ứng. |

Không đổi dữ liệu CK để che các lỗi còn lại. Các cảnh được ghi rõ `VÍ DỤ GIẢ ĐỊNH` hiện không còn đòi URL.

## Kiểm thử

- PASS: `python -m pytest -q tests/test_scene_params.py tests/test_factcheck_lint.py -p no:cacheprovider` → `16 passed`.
- Đã chạy: `python -m pytest -q tests/`. Sandbox không cho pytest đọc `C:\Users\Tung-QA\AppData\Local\Temp\pytest-of-Tung-QA`; chạy lại với `--maxfail=1` dừng ở `tests/test_agent_ticket.py::test_xong_khi_co_bao_cao_moi` với `PermissionError [WinError 5]`, trước khi test code.
- `tests/test_console.py::test_every_cli_calls_utf8_console` còn fail do 7 CLI cũ ngoài phạm vi: `scripts/qa_mark.py`, `motion/long/commons_find.py`, `motion/long/dryplan.py`, `motion/long/unschedule.py`, `motion/stier/bang_tra_look.py`, `motion/stier/bud_variety.py`, `motion/stier/script_lint.py`. Không còn tên nào trong 6 CLI của ticket.
- Đã chạy `--help` thành công cho năm CLI có argparse trong scope; `factcheck_lint.py` là CLI positional không có `--help`, nhưng entry point đã gọi `utf8_console()` trước khi in kết quả.

## Sheet / thumbnail

Không áp dụng: ticket chỉ sửa cổng và cấm render; không tạo clip sheet hay thumbnail.
