# GH-25 · Codex vòng sửa: `factcheck_lint` báo nhầm nhãn "THÁNG N"

Issue: https://github.com/nguyent0810/Youtube_Creator_V2/issues/25. Bối cảnh: `docs/pm/tickets/GH-23-fix-report.md`, mục "Factcheck CK-F3".

## Lỗi

`python motion/long/factcheck_lint.py ck-f3-tien-mung-cuoi` báo 2 lỗi nhầm:
- `1`, do nhãn lịch "LỊCH TỪ THÁNG 1";
- `8`, do nhãn lịch "LỊCH TỚI THÁNG 8".

Đây là nhãn chỉ thời điểm trên lịch, không phải dữ kiện cần nguồn.

**Không được bỏ** các lỗi thật: `0,8`/`1,3` trong ledger thiếu đơn vị, và `0,8`/`1,5`/`2,8 TRIỆU` thiếu nguồn. Nếu `0,8` trong ledger và `8` trong "THÁNG 8" đang chuẩn hóa ra cùng một số, phải tách hai trường hợp này ra. Lỗi của `0,8` vẫn phải được báo.

## Được ghi
- `motion/long/factcheck_lint.py`
- `tests/test_factcheck_lint.py`
- Báo cáo `docs/pm/tickets/GH-25-fix-report.md`

Không: sửa `data/long/**`, hạ ngưỡng, render, commit.

## Việc
1. Bỏ qua số tháng (1–12) khi số đó đi liền sau "THÁNG"/"tháng" mà **không** kèm năm hay ngày cụ thể. Ví dụ "THÁNG 1" và "tháng 8" được bỏ qua.
   - Ngày có năm hoặc có ngày cụ thể vẫn phải kiểm như cũ, ví dụ "tháng 9 năm 1985", "07.02.1997".
   - Làm tương tự cho nhãn lịch trong cảnh `calendar`, nếu có trường riêng.
2. Thêm test hồi quy, gồm 3 ca:
   - "LỊCH TỪ THÁNG 1" / "LỊCH TỚI THÁNG 8": không báo lỗi;
   - "tháng 9 năm 1985" không có trong `factcheck`: vẫn báo lỗi;
   - ledger có `0,8` khi nhãn lịch cùng chứa "THÁNG 8": `0,8` vẫn bị báo.
3. Chạy lại lint trên `ck-f3-tien-mung-cuoi` và `mim-jobs-1985`, rồi liệt kê từng lỗi còn lại. Ở `ck-f3` kỳ vọng còn đúng 5 lỗi thật: `8` (từ `0,8`), `13`, `800000`, `1500000`, `2800000`. Nếu con số khác, giải thích.
4. Chạy `python -m pytest -q tests/test_factcheck_lint.py -p no:cacheprovider`.

## Báo cáo `docs/pm/tickets/GH-25-fix-report.md`
Ghi: cách sửa, output lint trước/sau, kết quả pytest.
