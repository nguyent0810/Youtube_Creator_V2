# GH-25 — Báo cáo vòng sửa Codex

## Đã làm

- Sửa `motion/long/factcheck_lint.py`: nhận diện số tháng theo **vị trí xuất hiện** sau `THÁNG/tháng`, chỉ bỏ qua các tháng 1–12 là nhãn độc lập. Nếu cụm đó có năm hoặc ngày cụ thể thì vẫn soát như dữ kiện.
- Cách soát theo span giữ tách biệt `THÁNG 8` và `0,8`: nhãn lịch không còn tạo lỗi, còn giá trị `0,8 TRIỆU` vẫn chuẩn hoá thành `800000` và vẫn bị báo khi thiếu nguồn.
- Quy tắc áp dụng cho mọi chữ hiển thị, gồm cả chữ của scene `calendar` có trường riêng.
- Thêm test hồi quy cho ba trường hợp của ticket: nhãn tháng độc lập, tháng kèm năm, và `0,8` cùng nhãn `THÁNG 8`; đồng thời chốt thêm trường hợp ngày cụ thể.
- Không sửa `data/long/**`, không render, không đổi lịch, không đăng hay commit.

## Lệnh đã chạy và kết quả

Trước khi sửa:

```text
python motion/long/factcheck_lint.py ck-f3-tien-mung-cuoi
6 lỗi: 1, 8, 13, 800000, 1500000, 2800000

python motion/long/factcheck_lint.py mim-jobs-1985
3 lỗi: 816; TRÍCH DỊCH (3 câu nhưng 0 mục đủ nguyên văn và URL);
lệch bản final ở CH08

python -m pytest -q tests/test_factcheck_lint.py -p no:cacheprovider
7 passed in 0.16s
```

Sau khi sửa:

```text
python -m pytest -q tests/test_factcheck_lint.py -p no:cacheprovider
8 passed in 0.18s

python motion/long/factcheck_lint.py ck-f3-tien-mung-cuoi
5 lỗi: 8, 13, 800000, 1500000, 2800000

python motion/long/factcheck_lint.py mim-jobs-1985
3 lỗi: 816; TRÍCH DỊCH (3 câu nhưng 0 mục đủ nguyên văn và URL);
lệch bản final ở CH08
```

## Lỗi lint còn lại

- `ck-f3-tien-mung-cuoi`: `8` còn lại là giá trị đã chuẩn hoá từ `0,8`, không phải nhãn `THÁNG 8`; bốn lỗi số còn lại là `13`, `800000`, `1500000`, `2800000`.
- `mim-jobs-1985`: `816`; ba câu `[TRÍCH DỊCH]` thiếu mục factcheck có nguyên văn tiếng gốc và URL; mục CH08 lệch bản final.

Không có khẳng định nội dung nào được kiểm hay thay đổi trong vòng sửa công cụ này.
