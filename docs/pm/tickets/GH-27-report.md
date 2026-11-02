# GH-27 — Báo cáo

## Đã làm

- Sửa ledger CH05 trong `data/long/ck-f3-tien-mung-cuoi/gen_scenes.py`: `0,8` thành `0,8 TRIỆU` và `1,3` thành `1,3 TRIỆU`; bố cục ledger giữ nguyên.
- Thêm bốn dòng factcheck, đều ghi rõ **VÍ DỤ GIẢ ĐỊNH** và trỏ tới `facts.md`: lì xì 0,8 triệu (#15), ba dịp còn lại 1,3 triệu (#20), ba đám đồng nghiệp 1,5 triệu (#22), và cộng dồn tới tháng 8 là 2,8 triệu (bảng biểu đồ mục 1–6).
- Chạy `python data/long/ck-f3-tien-mung-cuoi/gen_scenes.py`; kết quả: `spec + 7 chương`. JSON các chương được sinh lại; `ch05.json` có hai giá trị ledger kèm đơn vị TRIỆU.

Không chạy `git diff --stat` vì AGENTS.md của repo cấm mọi thao tác git. Không sửa số liệu, `script.md`, lint/ngưỡng; không render, không đăng, không đổi lịch hay commit.

## Lệnh và kết quả

Các lệnh đều chạy với `PYTHONIOENCODING=utf-8`.

| Cổng | Trước sửa | Sau sửa |
|---|---|---|
| `python motion/long/factcheck_lint.py ck-f3-tien-mung-cuoi` | 5 lỗi: `8`, `13`, `800000`, `1500000`, `2800000` | 0 lỗi |
| `python motion/long/scene_params.py ck-f3-tien-mung-cuoi` | 0 lỗi, 0 cảnh báo (A1/A7/A8/A9 đều 0) | 0 lỗi, 0 cảnh báo (A1/A7/A8/A9 đều 0) |
| `python motion/long/studio_lint.py ck-f3-tien-mung-cuoi --strict` | 0 lỗi, 9 cảnh báo | 0 lỗi, 9 cảnh báo |

## Lỗi/cảnh báo còn lại

`studio_lint --strict` còn 9 cảnh báo đã có trước thay đổi: hai câu liệt kê quá 3 mục (CH00 dòng 5, CH04 dòng 21) và tỷ lệ câu ngắn ở CH00–CH06. Ticket cấm đổi lời đọc `script.md`, nên không sửa các cảnh báo này.

## Kiểm chứng và tài sản

- Không có khẳng định mới nào chưa kiểm được: cả bốn số thêm vào đều là VÍ DỤ GIẢ ĐỊNH và dẫn mục tương ứng trong `facts.md` theo brief.
- Clip sheet: không tạo/soi trong ticket này; đường dẫn chuẩn là `output/long/ck-f3-tien-mung-cuoi/qa_clips.jpg`.
- Thumbnail: không tạo/soi trong ticket này; ticket không cho render hay sửa thumbnail.
