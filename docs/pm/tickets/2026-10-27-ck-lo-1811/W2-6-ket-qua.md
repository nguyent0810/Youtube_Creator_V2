# W2-6 — kết quả dựng cảnh

## Đã làm

- Tạo `data/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/gen_scenes.py`, sinh `spec.json` và cảnh cho đủ 7 chương `ch00`–`ch06`.
- Dùng đường đua `race` lấy trực tiếp chuỗi tháng trong `results.json`: tiết kiệm 6%, bỏ một lần và mua đều. Biểu đồ chính mở ở CH00 và được cập nhật theo mốc tại CH01–CH06.
- Có các biểu đồ số liệu thật VN-Index/CPI kèm nguồn trên cảnh; mọi mức tiền, phí và lãi cố định đều gắn nhãn ví dụ giả định.
- Tải, dựng và soi clip sheet: 14 clip khác nhau, mỗi clip dùng không quá 2 lần. Đã thay các clip có giấy tờ, chữ/mệnh giá hoặc đồ họa có số đọc được.
- Không render, không upload và không chạy `thumb.py`, đúng phạm vi W2.

## Lệnh đã chạy

```text
python motion/long/script_lines.py ck-i1-100-trieu-tiet-kiem-hay-vnindex
python data/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/gen_scenes.py
python motion/long/studio_lint.py ck-i1-100-trieu-tiet-kiem-hay-vnindex --strict
python motion/long/build_long.py ck-i1-100-trieu-tiet-kiem-hay-vnindex tts
python motion/long/build_long.py ck-i1-100-trieu-tiet-kiem-hay-vnindex html
python motion/long/clip_sheet.py ck-i1-100-trieu-tiet-kiem-hay-vnindex
python scripts/long_gate.py ck-i1-100-trieu-tiet-kiem-hay-vnindex --min-syl 1800
```

- HTML: 7/7 chương, không có Error.
- Cổng cuối: `ĐẠT` — 1.879 âm tiết, 8,2 phút, 55 cảnh, 9,0 giây/cảnh, 8 clip khác, 17 URL nguồn.
- Tỷ lệ cảnh: 55 tổng; biểu đồ/dữ liệu 26 cảnh (47%); thẻ chữ `question`/`kinetic` 7 cảnh (13%).
- `studio_lint --strict`: 0 lỗi, còn 3 cảnh báo mật độ câu ngắn ở CH01, CH05, CH06. `html` còn 1 cảnh báo CH06 về dòng chữ lớn trùng lời đọc; không phải lỗi cổng.

## Kiểm chứng và giới hạn

- Không có khẳng định chưa kiểm được mới. Các giới hạn mô phỏng vẫn được giữ: VN-Index là chỉ số giá, không cộng cổ tức; phí, thuế và lãi cố định là giả định; kết quả quá khứ không dự báo tương lai.

## Đường dẫn QA

- Clip sheet: `output/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/qa_clips.jpg`
- Thumbnail: chưa tạo theo chỉ đạo W2 không chạy `thumb.py`; đường dẫn dự kiến: `output/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/t1.jpg`.
