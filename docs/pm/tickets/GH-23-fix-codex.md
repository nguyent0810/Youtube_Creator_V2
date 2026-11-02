# GH-23/GH-25 · Codex vòng sửa: các cổng mới báo nhầm

Issue liên quan: #23 và #25. Lead đã cho một subagent kiểm lại kết quả của `GH-23-report.md` và `GH-25-report.md`. Kết quả:

1. **A1 báo nhầm toàn bộ** trên golden, mafia, bulger, capone, escobar và mim-ke-huy-diet-petrov.
   - Nguyên nhân: `do_html` gọi bộ kiểm trên spec thô (khoảng `build_long.py:943`), tức là trước khi `plan()` đổi tên key.
   - Các key bị đổi tên nên bị báo nhầm:
     - `slam.hitAt` → `at` (`build_long.py:514`);
     - `quote.typeAt` → `at` (`:499`);
     - `countAt` → `at`.
   - Các key engine thực sự có đọc mà bộ kiểm không biết:
     - `counter.img`: `casewide.js:358`, `if (s.img)`;
     - `label` dạng chuỗi ở `calendar` (`:773`) và `seismo` (`:629`). `_validate_types` lại bắt `label` phải là object.
2. **`factcheck_lint` báo nhầm** trên `ck-f3-tien-mung-cuoi`:
   - nhãn tháng "T1…T12" và giá trị trục biểu đồ "0" bị coi là dữ kiện;
   - "300 NGHÌN" sinh ra cả số trần 300 lẫn số quy đổi (`factcheck_lint.py:34-35`).
3. **`tests/test_console.py`:** các CLI mới chưa gọi `factory.console.utf8_console()`: `scene_params.py`, `img_sheet.py`, `factcheck_lint.py`, `coverage_lint.py`, `scene_rules.py`, `clip_sheet.py`. Danh sách lỗi cũ còn lại không thuộc phạm vi ticket này.

## Được ghi
- `motion/long/scene_params.py`
- `motion/long/build_long.py`: chỉ chỗ gọi bộ kiểm
- `motion/long/factcheck_lint.py`
- 6 CLI nêu ở mục 3, chỉ thêm `utf8_console`
- `docs/codex/long-rules.md`
- `tests/test_scene_params.py`, `tests/test_factcheck_lint.py`
- báo cáo `docs/pm/tickets/GH-23-fix-report.md`

**Không:** sửa `data/long/**` hoặc engine; render; commit; hạ ngưỡng nào.

## Việc
1. **A1.** Bộ kiểm phải hiểu đúng các key mà `plan()` đổi tên, bằng một trong hai cách:
   - kiểm sau khi `plan()` chạy; hoặc
   - khai báo bảng alias lấy thẳng từ `plan()`, không chép tay lại một danh sách riêng.

   Thêm `counter.img`, và cho `label` dạng chuỗi ở `calendar`/`seismo`. Rà lại toàn bộ `plan()` xem còn key nào bị đổi tên hay tiêu thụ mà bảng chưa biết.
   - **Tiêu chí:** sau khi sửa, chạy `scene_params.py` trên golden, mafia, kowloon, ripper, shanghai, yakuza, bulger, capone, escobar và mim-ke-huy-diet-petrov. Lỗi A1 còn lại nào cũng phải ghi rõ trong báo cáo là REAL: engine thật sự bỏ qua key đó, kèm dòng code làm bằng chứng.
   - Thêm test cho `hitAt`, `typeAt`, `countAt`, `counter.img`, và `label` dạng chuỗi.
2. **factcheck_lint.**
   - Không coi nhãn trục hay nhãn tháng (`T1`–`T12`, `Q1`–`Q4`), giá trị 0 và số thứ tự chương là dữ kiện.
   - Với "N nghìn/triệu/tỷ", chỉ giữ một dạng chuẩn hóa.
   - Thêm test dựa trên các ca thật của `ck-f3`. Chạy lại trên `ck-f3` và liệt kê từng lỗi còn lại, kèm nhận định lỗi thật hay báo nhầm.
3. **utf8_console.** Thêm cho 6 CLI ở mục 3. `test_console` không được còn tên nào trong số này.
4. **Ghi luật vào `docs/codex/long-rules.md`**, theo đúng văn phong của file:
   - A7: mỗi cảnh dài 2,5–9 s, là lỗi chặn ở bước `html`;
   - A8: ≤ 3 lần dùng mỗi ảnh; ảnh khai trong `spec.imgs` mà không cảnh nào dùng là lỗi;
   - A4: phần tử con thứ hai phải hiện ≤ 1 s sau khi cảnh mở;
   - A9: giới hạn số dòng ledger theo theme;
   - A10: quy trình tờ soát: `img_sheet.py` và `clip_sheet.py`, xem tờ rồi mới chạy `--ok`, và `render`/`final` bị chặn khi thiếu dấu hoặc dấu cũ;
   - A11: định dạng `factcheck.md` đề xuất trong `GH-25-report.md`; `publish_long.py` chặn khi có lỗi.
5. Chạy `python -m pytest -q tests/`. Nếu sandbox chặn thư mục tạm thì ghi lại và chạy riêng các file test liên quan.

## Báo cáo `docs/pm/tickets/GH-23-fix-report.md`
- Bảng A1 trước và sau theo từng topic.
- Danh sách lỗi REAL còn lại, kèm bằng chứng.
- Lỗi factcheck còn lại ở `ck-f3`.
- Kết quả pytest.
