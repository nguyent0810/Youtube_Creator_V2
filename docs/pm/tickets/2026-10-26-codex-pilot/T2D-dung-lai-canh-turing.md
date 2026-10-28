# T2D — Dựng lại cảnh `mim-turing-bombe` (review bản render)

Claude đã render bản T2C và xem contact sheet bản cuối. Có hai lỗi chặn đăng. **Giữ nguyên `script.md`, lời đọc, TTS, `SAY` và `spec.youtube`.** Chỉ sửa phần cảnh trong `gen_scenes.py`, rồi sinh lại `ch*.json`. Không render, không upload.

**Kết quả ghi vào:** `docs/pm/tickets/2026-10-26-codex-pilot/T2D-ket-qua.md`

## Lỗi 1: thẻ chương hiện chữ "undefined"

Thẻ chương đang ghi:

```json
{"type": "chapter", "number": "05", "title": "…"}
```

Engine cần các trường như mẫu Petrov (`data/long/mim-ke-huy-diet-petrov/ch05.json`):

```json
{"type":"chapter","no":"5","k":"CHƯƠNG NĂM","title":"…\n…","sub":"<mốc ngày có nguồn>","bg":"<ảnh>","titleAt":[0,"<từ trong câu đầu>"]}
```

Thiếu `no` hoặc `k` thì giữa màn hình hiện "undefined". Sửa cả 8 chương. `sub` nên là một mốc ngày tháng có nguồn của chương đó.

## Lỗi 2: cảnh dựng theo khuôn, lặp nguyên chữ

`gen_scenes.py` đang dùng **một khuôn 9 cảnh giống nhau cho mọi chương**. Hậu quả:
- "SÁU RĂNG CỦA MỘT KHÓA" hiện 8 lần.
- "KIỂM TRA, RỒI LẠI KIỂM TRA" hiện 8 lần.
- "NẾU MÁY DỪNG Ở ĐÂY, BẠN KIỂM TRA ĐIỀU GÌ TRƯỚC?" hiện 8 lần.
- Nhiều khung gần như trống.

Người xem sẽ thấy video lặp như máy làm. Đây cũng là rủi ro "nội dung lặp khuôn" khi xét YPP.

**Yêu cầu:**
- Mỗi cảnh phải minh hoạ **đúng câu đang đọc** và neo vào từ trong câu đó (`[dòng, "từ"]`).
- Chữ trên màn hình lấy từ dữ kiện của chính chương đó, như tên người, năm, con số, vật.
- Không có dòng chữ hiển thị nào lặp quá 2 lần trong cả video.
- Mô-típ "sáu răng" chỉ hiện bằng một `ledger` có tiêu đề cố định, mỗi chương **thêm một dòng mới**, đúng cách bài Petrov làm với "GHẾ TRỰC · BẠN ĐANG CÓ".
- Gợi ý theo chương (mọi dữ kiện đều có trong `facts.md`):

| Chương | Cảnh gợi ý |
|---|---|
| CH00 | `date` 21.10.1941; `quote` dòng xin người trong thư (nếu nguồn có nguyên văn); `kinetic` "20 NHÂN VIÊN · 20 NGƯỜI ĐÁNH MÁY · WRNS" |
| CH01 | `slam` hoặc `kinetic` "158.962.555.217.826.360.000"; `ledger` 3 rô-to từ bộ 5 / bộ 8; `counter` khoảng 50 mạng (khai `"year": false`) |
| CH02 | `map` Warsaw–Pyry → Paris → Bletchley; `timeline` 12/1932 → 1936 → 9/1938 → 7/1939 |
| CH03 | `org`: Rejewski, Turing, Welchman, Clarke |
| CH04 | Crib và menu |
| CH05 | Agnus 8/1940; 211 Bombe |
| CH06 | Wrens, Eastcote, Stanmore, Jean Millar 11/1943 |
| CH07 | Phim, theo *Time* |

- Khung nền tối và trống chỉ được dùng cho khoảng lặng có chủ đích (sau dấu `‖`), không dùng làm cảnh mặc định.

## Cổng

1. Chạy `gen_scenes.py`.
2. Chạy `studio_lint --strict`, phải ra 0 lỗi.
3. Chạy `build_long.py html` cho đủ 8 chương.
4. Chạy `clip_sheet.py`.
5. Chạy `python scripts/long_gate.py mim-turing-bombe --min-syl 1900`, phải ra **ĐẠT**. Cổng này giờ chặn cả thẻ chương thiếu trường lẫn chữ lặp quá 2 lần.
