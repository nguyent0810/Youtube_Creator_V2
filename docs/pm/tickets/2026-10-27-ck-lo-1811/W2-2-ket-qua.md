# W2-2 — Kết quả dựng cảnh `ck-f2-vien-phi-bhyt`

## Đã làm

- Dựng lại `data/long/ck-f2-vien-phi-bhyt/gen_scenes.py` và sinh lại toàn bộ `ch00`–`ch06`, `spec.json`.
- Cập nhật mô hình ví dụ theo `results.json`: tổng 30 = 25 trong phạm vi + 5 ngoài phạm vi; quỹ trả 20; tự trả trên hóa đơn 10; ngoài hóa đơn 2; gánh nặng 12 triệu. Các số hiển thị của mô hình lấy từ `results.json`.
- Cập nhật tiêu đề và lịch công bố: `Có Bảo Hiểm Y Tế Vẫn Trả 40%: Tiền Viện Phí Đi Đâu?`; `2026-11-20T13:00:00Z`.
- CH00 bắt đầu bằng biểu đồ dữ liệu thật: bao phủ BHYT 2024 (94,29%) và chi tiền túi 2025 (khoảng 40%), kèm nguồn BHXH Việt Nam. Ảnh nhân vật bắt đầu từ CH01.
- Dùng 6 ảnh minh hoạ `ai01`–`ai06`, mọi cảnh ảnh có `credit: false`, nhãn `ẢNH MINH HỌA`, focus và chuyển động.
- Sửa cấu trúc `range` thành chuỗi; thay cảnh `race` có nhãn mốc chữ bằng `bars`.

## Lệnh đã chạy

```text
python data/long/ck-f2-vien-phi-bhyt/gen_scenes.py
python motion/long/script_lines.py ck-f2-vien-phi-bhyt
python motion/long/build_long.py ck-f2-vien-phi-bhyt tts
python motion/long/build_long.py ck-f2-vien-phi-bhyt html
python scripts/long_gate.py ck-f2-vien-phi-bhyt --min-syl 2200
python scripts/long_gate.py ck-f2-vien-phi-bhyt --min-syl 1800
```

- TTS: 7/7 chương, 2.695 âm tiết, 11,68 phút.
- HTML: 7/7 chương, không Error.
- `long_gate --min-syl 2200`: **ĐẠT**.
- `long_gate --min-syl 1800`: **ĐẠT**.
- Gate cuối: 125 cảnh, 5,6 giây/cảnh, 18 URL nguồn.

## Biểu đồ

- Biểu đồ chính (thác 30 → 20 → 10 → 12 triệu) có mặt ở CH01–CH06; mỗi cảnh ghi rõ đây là ví dụ giả định.
- Các biểu đồ dữ liệu thật Việt Nam nằm ở CH00 và các chương sau, có `srcnote` nguồn BHXH Việt Nam.

## Clip, clip sheet và thumbnail

- Không dùng clip trong bản dựng này; vì vậy không tải clip và không tạo clip sheet. Không chạy thumbnail theo đúng luật W2.
- Không có thumbnail mới trong ticket này.

## Lỗi còn lại / cần lưu ý

- Không còn lỗi HTML hoặc long gate.
- Không có khẳng định chưa kiểm được: số liệu công khai dùng trong cảnh đã lấy từ `facts.md` và nguồn được nêu trong `spec.json`.
