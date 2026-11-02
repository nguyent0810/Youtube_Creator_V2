# GH-23 · Codex: cổng kỹ thuật kiểm tham số cảnh Long (A1, A4, A7, A8, A9)

- Issue: https://github.com/nguyent0810/Youtube_Creator_V2/issues/23
- Bối cảnh: `docs/pm/2026-10-29-jobs-1985-loi-pipeline.md`, các mục A, D và phần "Bổ sung sau retro".
- Engine của Long là `motion/hf/assets/engine/casewide.js`. Chỉ được đọc file này, không sửa.

## Mục tiêu

Lỗi tham số và lỗi nhịp cảnh phải bị chặn ở `python motion/long/build_long.py <topic> html`, trước khi render, thay vì để agy hay người soát khung hình mới thấy.

## Được ghi

- `motion/long/scene_params.py`: file mới, chứa bộ kiểm.
- `motion/long/build_long.py`: chỉ để gọi bộ kiểm trong `do_html` và sửa các hàm sẵn có `late_first`, `ledger_overflow`.
- `motion/long/scene_rules.py`
- `tests/test_scene_params.py`: file mới.
- `tests/test_long_scene_rules.py`, `tests/test_late_first.py`
- Báo cáo `docs/pm/tickets/GH-23-report.md`

**Không:** sửa `data/long/**` hay `casewide.js`; render; chạy TTS; commit; hạ ngưỡng nào.

## Việc

### 1. A1: kiểm tham số theo loại cảnh
- Trong `scene_params.py`, dựng bảng key hợp lệ cho từng `type` cảnh, rút ra bằng cách đọc các hàm `B.<type>` trong `casewide.js`.
- Những lỗi phải bắt được:
  - key không nằm trong bảng của loại cảnh đó;
  - `head` trong cảnh `print`, vì engine chỉ vẽ `side.k`, `side.h`, `side.lines`;
  - `maxW`/`maxH` nhỏ hơn 50, vì đơn vị là pixel;
  - `pos` hoặc `focus` sai kiểu so với những gì engine đọc;
  - accent của `kinetic` không khớp chữ nào trong dòng (retro: chữ "AMELIO" không hiện);
  - nhãn `quote` không phải nhãn engine hiển thị được.
- Mọi key engine bỏ qua thì coi là lỗi. Trường hợp không chắc thì ghi vào báo cáo và để ở mức cảnh báo, kèm lý do.
- Lỗi in dạng `chNN#i type: <vấn đề>` và dừng `html` bằng `SystemExit`.

### 2. A7: độ dài cảnh
- Cảnh dưới `MIN_SHOT_S` (2,5 s) hoặc trên 9 s là lỗi chặn ở bước `html`. Trước đây `scene_rules` chỉ cảnh báo.
- Cảnh chương (`chapter`) và cảnh cuối chương: xem `docs/codex/long-rules.md` có ngoại lệ nào không. Không tự đặt ngoại lệ mới; nếu thấy cần thì ghi vào báo cáo.

### 3. A8: số lần dùng ảnh
- Mỗi key ảnh (`img`/`bg`/ảnh trong `print`…) dùng tối đa 3 lần trên toàn bài, theo luật trong `long-rules.md`.
- Ảnh có trong `spec.imgs` mà không cảnh nào dùng: báo lỗi (retro: 6 ảnh AI bị ghi đè dict nên không được dùng).

### 4. A9: ledger
- `ledger_overflow` hiện chỉ đo chiều ngang. Thêm giới hạn số dòng (rows + total), để bảng không đè vùng phụ đề.
- Rút giới hạn từ CSS/JS của engine (chiều cao dòng, vị trí `#caps`); không đoán. Ghi phép tính vào báo cáo.

### 5. A4: phần tử con hiện muộn
- `late_first`/`first_delay` đã có sẵn, nhưng không bắt được 2 cảnh `org` của Jobs 1985: chỉ một nút hiện trong khoảng 3 s đầu, xem `GH-10-preview2-report.md`.
- Tìm lý do, rồi quy định: với cảnh có nhiều phần tử con (`org`, `timeline`, `rows`, `items`, `callouts`…), **phần tử con thứ hai** cũng phải hiện trong ≤ 1 s sau khi cảnh mở, hoặc nêu một luật tương đương đo được.
- Đặt luật này là lỗi chặn trong `html`.

### 6. Hồi quy
- Viết test cho từng luật: mỗi luật có ca đạt và ca trượt. Thêm một ca dựng lại đúng lỗi Sculley ở Jobs 1985: `maxH` 0.52, `pos` dạng mảng.
- Chạy `python -m pytest -q tests/`: phải xanh, kể cả các test cũ.
- Chạy bộ kiểm mới (không chạy `html` đầy đủ) trên mọi topic MIM và CK trong `data/long/` (đọc `spec.json` → `channel`), và trên 6 Long CL chuẩn: yakuza, mafia, shanghai, ripper, kowloon, golden.
- Báo cáo ghi một bảng gồm: topic, kênh, số lỗi theo từng luật. Jobs 1985 bản hiện tại phải **qua** A1/A7/A8 (đã sửa tay); nếu không qua thì giải thích.

## Báo cáo `docs/pm/tickets/GH-23-report.md`

- Bảng key hợp lệ theo loại cảnh, kèm dòng tương ứng trong `casewide.js`.
- Các luật đã thêm, ngưỡng và nguồn của ngưỡng.
- Kết quả pytest.
- Bảng hồi quy.
- Những gì chưa chắc.
