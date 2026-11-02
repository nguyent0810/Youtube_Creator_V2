# GH-27 · Codex: ck-f3 thiếu đơn vị và dòng factcheck

Issue: https://github.com/nguyent0810/Youtube_Creator_V2/issues/27. Topic `ck-f3-tien-mung-cuoi` chưa đăng, chưa có `video_id`.

`python motion/long/factcheck_lint.py ck-f3-tien-mung-cuoi` còn 5 lỗi: `8` (từ `0,8`), `13`, `800000`, `1500000`, `2800000`. Các số đều là **VÍ DỤ GIẢ ĐỊNH** đã có trong `facts.md` (#15, #20, #22, bảng biểu đồ mục 1–6) nhưng chưa có dòng trong `factcheck.md`; ledger CH05 (`gen_scenes.py:94`) ghi `0,8`/`1,3` không đơn vị.

## Được ghi
- `data/long/ck-f3-tien-mung-cuoi/gen_scenes.py`, `ch*.json` sinh lại từ nó
- `data/long/ck-f3-tien-mung-cuoi/factcheck.md`
- báo cáo `docs/pm/tickets/GH-27-report.md`

**Không:** sửa `factcheck_lint.py` hay bất kỳ lint/ngưỡng nào, đổi số liệu, đổi lời đọc `script.md`, render, commit.

## Việc
1. Ledger CH05: `0,8` → `0,8 TRIỆU`, `1,3` → `1,3 TRIỆU` (hoặc đơn vị trong tiêu đề ledger, miễn lint hiểu). Giữ bố cục; nếu chữ dài làm vỡ ô thì báo.
2. Thêm dòng vào bảng `factcheck.md` cho: lì xì 0,8 triệu; ba dịp còn lại 1,3 triệu (500+300+500 nghìn); ba đám đồng nghiệp 1,5 triệu; cộng dồn tới tháng 8 là 2,8 triệu. Cột nguồn: `VÍ DỤ GIẢ ĐỊNH; …` như các dòng ví dụ hiện có, dẫn số mục `facts.md`.
3. Sinh lại ch*.json bằng cách chạy `gen_scenes.py` như hiện tại; `git diff --stat` chỉ được đổi ledger.
4. Chạy lại `factcheck_lint.py ck-f3-tien-mung-cuoi` (kỳ vọng 0 lỗi), `scene_params.py ck-f3-tien-mung-cuoi`, `studio_lint.py ck-f3-tien-mung-cuoi --strict`.

## Báo cáo `docs/pm/tickets/GH-27-report.md`
Diff tóm tắt, output ba lint trước/sau.
