# W2-5 — Kết quả dựng cảnh `ck-c6-gia-tran-san-t2`

## Đã làm

- Tạo `data/long/ck-c6-gia-tran-san-t2/gen_scenes.py`, ghi `spec.json` và cảnh/hud cho đủ CH00–CH06.
- Giữ nguyên `script.md`; dùng số từ `results.json`, 6 ảnh `ai01`–`ai06`, và khai báo `credit: false`, `ẢNH MINH HỌA`, `focus` cho ảnh nhân vật.
- Dựng biểu đồ dải sàn–tham chiếu–trần và lịch T/T+1/T+2 xuyên các chương; trạng thái 100 cổ phiếu hoàn chỉnh ở CH05 và kết luận ở CH06.
- Tải, dùng và đã soi 7 clip Pexels: `8195667`, `11899304`, `7688068`, `6794227`, `7148966`, `5726502`, `7693395`. Hai ứng viên lỗi lúc tải/không có bản ngang (`8195667` ở lần đầu, `7652107`) đã được tải lại/thay bằng clip ngang hợp lệ. Clip sheet không thấy logo, tên công ty hay chữ đọc được ở các khung kiểm.

## Lệnh đã chạy

```text
python motion/long/script_lines.py ck-c6-gia-tran-san-t2 --allow-repeat-line
python data/long/ck-c6-gia-tran-san-t2/gen_scenes.py
python motion/long/build_long.py ck-c6-gia-tran-san-t2 tts --allow-repeat-line
python motion/long/build_long.py ck-c6-gia-tran-san-t2 html --allow-repeat-line
python motion/long/studio_lint.py ck-c6-gia-tran-san-t2 --strict
python motion/long/clip_sheet.py ck-c6-gia-tran-san-t2
python scripts/long_gate.py ck-c6-gia-tran-san-t2 --min-syl 1800
```

- TTS: đủ 7/7 chương, 2.399 âm tiết, 10,74 phút.
- HTML: đủ 7/7, không Error.
- `long_gate`: **ĐẠT** — 2.399 âm tiết; 76 cảnh tính ở cổng; 8,5 giây/cảnh; 7 clip khác nhau; 8 URL nguồn.

## Tỷ lệ cảnh

- 57/83 cảnh infographic/chart (68,7%, gồm bars, heat, stack, timeline, ledger, counter); 26 cảnh là biểu đồ số trực tiếp (`bars`/`heat`/`stack`).
- 6/83 thẻ chữ (`kinetic`/`question`), 7,2%.

## Biểu đồ chính

`100 cổ phiếu đang ở đâu?` xuất hiện ở CH00, CH01, CH02, CH03, CH04, CH05 và CH06; CH05 cho trạng thái hoàn chỉnh T/T+1/chiều T+2.

## Cảnh báo/lỗi còn lại

- `studio_lint --strict`: 0 lỗi, 2 cảnh báo về tỷ lệ câu ngắn tại CH00 và CH03. Kịch bản đã được duyệt nên không chỉnh lời đọc.
- Không có lỗi engine còn lại. Không render, upload hay tạo thumbnail.

## Đường dẫn QA

- Clip sheet: `output/long/ck-c6-gia-tran-san-t2/qa_clips.jpg`
- Thumbnail: không dựng theo yêu cầu ticket W2.
