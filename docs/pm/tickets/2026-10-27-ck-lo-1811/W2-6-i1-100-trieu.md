# W2-6 — DỰNG CẢNH `ck-i1-100-trieu-tiet-kiem-hay-vnindex`
Đọc `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CHUNG-W2.md` và làm đúng. Mã báo cáo: `W2-6`.
- **Biểu đồ chính:** `race` + `abs`, 3 đường (tiết kiệm / bỏ một lần / mua đều), triệu đồng theo tháng, từ 04/2018. Số lấy từ `results.json`.
  - Mỗi chương vẽ tới một mốc thời gian.
  - Có `calls` ở lúc âm sâu nhất và lúc về lại vốn.
- **Thêm `candles`** (VN-Index thật) ở 1–2 chương cho các mốc: đỉnh 04/2018, Covid 03/2020, đỉnh 01/2022. Dùng `"series": "vnindex"`, đoạn ≥ 10/2018. Đoạn trước 10/2018 vẽ bằng `race` từ `results.json`.
- **Ngoại lệ:** bài này **không có ảnh nhân vật AI**. Bỏ mục 3 của luật chung. Thay bằng clip (ít nhất 8 clip khác nhau) và biểu đồ.
- Nguồn trên biểu đồ: "DỮ LIỆU: HOSE QUA VNSTOCK · KÊNH TỰ TÍNH · VÍ DỤ GIẢ ĐỊNH 100 TRIỆU".
- **Vòng sau quota (27/10):** `script.md` và `results.json` đã được Claude sửa (W1-6b): có 3 kịch bản tiết kiệm 5/6/7% và chuỗi `monthly` theo tháng, dùng thẳng cho `race`. Đường tiết kiệm chính 6% màu xanh lá, dải 5% và 7% màu nhạt.
