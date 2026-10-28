# R6 — NGHIÊN CỨU: `ck-i1-100-trieu-tiet-kiem-hay-vnindex`

Đọc trước `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CHUNG-R.md` và làm đúng luật trong đó. Mã báo cáo: `R6`.

**Đọc thêm:**
- mục **B3** trong `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CONTENT-BRIEF.md`;
- `docs/codex/long-rules.md`, hai mục cuối.

## Dữ liệu có sẵn (không tải lại)

| File | Nội dung |
|---|---|
| `data/ck/vnindex_1d_2016_2018.csv` | 01/12/2016 → 05/10/2018 |
| `data/ck/vnindex_1d.csv` | 08/10/2018 → 06/10/2026 |

Cả hai là giá đóng cửa VN-Index từng phiên, nguồn HOSE qua vnstock/VCI. Đỉnh 09/04/2018 đóng cửa 1.204,33. Đọc bằng `csv` trong Python. Được viết `data/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/analysis.py` để tính thử.

## Cần gom

1. **Lãi tiết kiệm 12 tháng bình quân theo từng năm, 2018–2026.**
   - Nguồn: Ngân hàng Nhà nước, Cục Thống kê, báo lớn dẫn số bình quân thị trường. **Không nêu tên ngân hàng.**
   - Ghi rõ đây là mức bình quân hay khoảng.
2. **Lạm phát CPI bình quân từng năm 2018–2026**, nguồn Cục Thống kê / GSO, để quy về sức mua.
3. **Giới hạn của backtest:**
   - VN-Index là **chỉ số giá**, không gồm cổ tức;
   - phí giao dịch và thuế 0,1% khi bán;
   - không ai mua được "chỉ số" trực tiếp; nếu nhắc quỹ chỉ số thì chỉ nói chung, không nêu tên quỹ.
4. **Mốc thật cho câu chuyện, mỗi mốc có ngày và số điểm từ dữ liệu:**
   - đỉnh 04/2018;
   - đáy Covid 03/2020;
   - đỉnh 01/2022;
   - đáy 11/2022;
   - 04/2025;
   - phiên cuối có trong dữ liệu.
5. **Ba cách tính thử** (`analysis.py`, gắn VÍ DỤ GIẢ ĐỊNH), cùng 100 triệu:
   - (a) gửi tiết kiệm 12 tháng, cuộn mỗi năm theo lãi bình quân;
   - (b) bỏ một lần vào VN-Index ngày 09/04/2018;
   - (c) chia đều mua mỗi tháng trong 24 tháng từ 04/2018.

   Với mỗi cách, ghi:
   - giá trị cuối;
   - lúc âm sâu nhất (ngày và %);
   - số tháng giá trị dưới 100 triệu;
   - thời gian về lại vốn.
6. **Kiểm trùng:**
   - `ck-e1-mua-deu-moi-thang` (3 triệu mỗi tháng, 8 năm, từ 10/2018);
   - `ck-2026-kenh-dau-tu` (100 triệu chia 5 kênh năm 2026).

   Bài này khác ở chỗ bắt đầu **đúng đỉnh 2018** và so **một lần** với **mua đều** với **tiết kiệm**. Ghi rõ chỗ khác.
7. Cold open, 3 tiêu đề, 2 thumbnail theo brief B3. Cập nhật nếu số thật khác.
8. 8–10 clip Pexels ngang, trung tính. Không bảng giá đọc được, không logo.
