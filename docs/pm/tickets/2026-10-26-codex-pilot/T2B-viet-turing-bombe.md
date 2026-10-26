# T2B — VIẾT và DỰNG Long `mim-turing-bombe` từ kho dữ kiện

**Đọc lại `AGENTS.md`** (cổng chất lượng, "Lỗi đã gặp"). **Kết quả ghi vào:** `docs/pm/tickets/2026-10-26-codex-pilot/T2B-ket-qua.md`. Không render, không upload, không chạy `thumb.py`.

Claude đã duyệt kho `data/long/mim-turing-bombe/facts.md` (34 dữ kiện). Viết lại toàn bộ `script.md`, `factcheck.md`, `gen_scenes.py`, rồi sinh `spec.json` và `ch*.json`. **Chỉ dùng dữ kiện trong kho.** Dữ kiện mức "vừa" phải có quy dẫn ngay trong câu đọc.

## Yêu cầu nội dung

- **Cold open:** đêm 21/10/1941, bốn nhà giải mã, trong đó có Turing, gửi thư vượt cấp cho Churchill. Treo câu hỏi rồi lùi về 1932/1939.
  - Ghi chú: Churchill đáp bằng chữ "Action this day". Chỉ dùng chi tiết này nếu nguồn National Archives trong kho có ghi; không có thì bỏ.
- **Lộ trình:** giữ mô-típ "sáu răng của chiếc khoá" hoặc chọn một dạng mới. Mỗi chương dùng 3–5 dữ kiện trong kho, kể bằng cảnh, người và vật cụ thể.
- **Phim:** *The Imitation Game* chỉ nhắc bằng lời và chữ, không dùng hình phim. Dữ kiện phim khác đời thật (#34) phải có quy dẫn *Time*.
- **Victory 3/1940:** kho ghi chưa có nguồn mạnh, nên không đọc. Nếu cần một mốc máy chạy thì dùng mốc Agnus 8/1940 (TNMOC) đúng như kho ghi.
- **Độ dài:** 1.900–2.300 âm tiết, khoảng 9–11 phút, 8 chương. **Không câu đệm.** Câu ngắn chỉ đặt sau phán định hoặc khoảnh khắc cảm xúc.
- **Tiêu đề:** `titles[0]` ≤ 60 ký tự, theo khuôn "NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing …".

## Yêu cầu hình

- 60–80 cảnh, trung bình ≤ 9 giây/cảnh, mỗi chương ít nhất 5 loại cảnh. Đối chiếu bài KAL 007 (`data/long/mim-google-maps-kal007/ch*.json`) và Petrov để chọn loại cảnh: `timeline`, `map`/`geo`, `org`, `counter` (năm khai `"year": true`), `quote`, `ledger`, `photo`/`print`, `kinetic`, `slam`, `broll`.
- Dùng 11 ảnh hợp lệ trong kho (PD/CC0) và các clip Pexels ứng viên. Mỗi clip dùng tối đa 2 lần, ít nhất 6 clip khác nhau.
- Chạy `clip_sheet.py`, mở ảnh xem từng clip, loại clip lộ logo, chữ hoặc sai nghĩa.
- Con số 158.962.555.217.826.360.000 khoá rất hợp cho cảnh `slam` hoặc `kinetic`. Đọc tròn thành "khoảng 159 tỷ tỷ"; trên màn hình hiện số đầy đủ.

## Cổng (phải qua hết)

1. `python motion/long/script_lines.py mim-turing-bombe`
2. `python data/long/mim-turing-bombe/gen_scenes.py`
3. `python motion/long/studio_lint.py mim-turing-bombe --strict` ra 0 lỗi
4. `python motion/long/build_long.py mim-turing-bombe tts`, rồi `... html`
5. `python motion/long/clip_sheet.py mim-turing-bombe`
6. **`python scripts/long_gate.py mim-turing-bombe --min-syl 1900` phải in ĐẠT**

## Báo cáo `T2B-ket-qua.md`

- Số liệu từ `long_gate`.
- Số dữ kiện đã dùng theo chương.
- Danh sách clip và ảnh kèm giấy phép.
- Đường dẫn clip sheet.
- Những gì còn lo ngại.
