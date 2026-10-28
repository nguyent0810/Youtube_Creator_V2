# Kết quả T4W2b — sửa neo `mim-moneyball`

## Đã làm

Đã chỉ sửa neo trong `data/long/mim-moneyball/gen_scenes.py`, không sửa `script.md`, `SAY`, `ROWS`, hay spec; không render và không upload.

Các neo đã sửa:

- ch05, cảnh `kinetic` Peter Brand: `[2, "peter"]` → `[1, "peter"]`.
- ch05, cảnh `question`: `[4, "phim"]` → `[3, "ý"]`.
- ch06, cảnh `print` Trận một: `[2, "5"]` → `[2, "sau"]`.

## Lệnh và kết quả

Đã chạy lặp lại sau mỗi lần sửa:

```text
PYTHONIOENCODING=utf-8 python data/long/mim-moneyball/gen_scenes.py
python motion/long/script_lines.py mim-moneyball
python motion/long/build_long.py mim-moneyball html
```

Kết quả HTML cuối: đủ 8 dòng `ch00` đến `ch07` tạo `.html`, không còn `Error`.

Đã chạy:

```text
python scripts/long_gate.py mim-moneyball --min-syl 1900
```

Kết quả: `ĐẠT` — 2.218 âm tiết, 10,4 phút, 81 cảnh, 6 clip khác nhau, 8 ảnh khác nhau, 29 URL nguồn.

Đã chạy:

```text
python motion/long/clip_sheet.py mim-moneyball
```

Kết quả: tạo clip sheet gồm 6 clip.

## Cảnh báo lint còn lại

- ch00 cảnh 6: `HOME RUN` tràn khung beat2 nhẹ; hệ thống tự co còn khoảng 95%.
- ch01, ch04, ch07: cảnh báo chữ lớn chép lời đọc.
- ch03 cảnh 1: `SABERMETRICS` tràn khung beat2 nhẹ; hệ thống tự co còn khoảng 94%.
- ch05 cảnh 7: cảnh báo phần tử đầu của sơ đồ xuất hiện sau 1,3 giây.

Các cảnh báo này không phải lỗi neo; giữ nguyên vì ticket chỉ yêu cầu sửa neo và không thay đổi nội dung đọc.

## Fact-check

Không có khẳng định mới hoặc sửa nội dung đọc; không có khẳng định nào cần kiểm lại trong ticket này.

## Tệp đầu ra

- Clip sheet: `output/long/mim-moneyball/qa_clips.jpg`
- Thumbnail: không tạo/soát trong ticket này vì ticket cấm render.
