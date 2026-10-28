# R6 — Kết quả nghiên cứu `ck-i1-100-trieu-tiet-kiem-hay-vnindex`

Đã ghi kho nghiên cứu tại `data/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/facts.md`.

- Dữ kiện: 28 dòng, 7 chương × 4; nguồn mạnh 20, vừa 8. Có 10 nguồn Pexels ứng viên và các URL đã mở.
- Bảng/biểu đồ: 9 bộ số, gồm race chính, mốc VN-Index, CPI, lãi suất quan sát, drawdown, tháng dưới vốn và lịch mua đều.
- Có 2 cold open, 3 tiêu đề (đều dưới 60 ký tự), 2 ý thumbnail.
- Đã đọc CSV ticket cấp bằng Python để kiểm các mốc: 09/04/2018 1.204,33; 24/03/2020 659,21; 06/01/2022 1.528,57; 15/11/2022 911,90; 09/04/2025 1.094,30; 06/10/2026 1.759,08.
- Lệnh đã chạy: đọc 30 dòng mẫu `factcheck.md`; Python đọc hai CSV và tính kiểm độc lập các mốc/biến động. Không chạy lint, TTS, HTML, render, thumbnail hay `long_gate`, vì đây là ticket nghiên cứu và `00-CHUNG-R.md` cấm các bước đó.

## Chưa kiểm được / blocker W1

Chưa có chuỗi lãi suất **bình quân tiền gửi 12 tháng theo từng năm 2018–2026** từ nguồn đủ chuẩn. Kho chỉ lưu các khoảng/mốc quan sát có nguồn và đánh dấu rõ không phải bình quân năm. Vì vậy chưa tính phương án tiết kiệm, sức mua cuối kỳ và chưa gọi bất kỳ mốc lãi suất nào là bình quân năm. CPI 2026 hiện chỉ có số bình quân 9 tháng 4,52%, chưa có số cả năm.

Không có clip sheet hay thumbnail ở ticket R6; các ID clip mới là ứng viên, bắt buộc tải và soi logo/chữ ở W2.
