# W1-6b — SỬA `ck-i1-100-trieu-tiet-kiem-hay-vnindex`: đưa đường tiết kiệm vào

Đọc:
- `00-CHUNG-W1.md` và `00-CHUNG-W1c.md` (luật giữ nguyên);
- `W1-6-ket-qua.md`, `R6-ket-qua.md`;
- `script.md`, `facts.md`, `analysis.py`, `check.py` của bài.

Mã báo cáo: `W1-6b`.

**Lỗi chặn:** kịch bản đang nói trên sóng rằng "chưa có dữ liệu", "chưa xếp hạng tiết kiệm". Không đăng được. Video phải trả lời câu hỏi trung tâm.

## Cách tính tiết kiệm (Claude chốt)

- Kho chỉ có các **mốc quan sát** lãi 12 tháng: 6,55% (đầu 2018); 6,0–6,5% (2020); 5,4–6,8% (07/2021); 5,6–7,4% (cuối 2022); 5,13% (12/2023); 4,9% (01/2024); 5,2% (12/2025). Các mốc này nằm trong khoảng **5–7%/năm**.
- Dùng **3 kịch bản lãi cố định**: **5%, 6% và 7%/năm**, gửi 12 tháng, cuộn mỗi năm, từ 09/04/2018 tới 06/10/2026. Phần năm lẻ tính lãi theo tỉ lệ thời gian.
- **Đường chính 6%.** Hai đường 5% và 7% là dải mờ hai bên.
- Ghi rõ **VÍ DỤ GIẢ ĐỊNH**: lãi cố định trong khoảng đã quan sát, không phải lãi thật của một ngân hàng nào.
- Lãi tiết kiệm không có thuế thu nhập; không cần nói thêm.

## Sửa

1. **`analysis.py`:**
   - thêm 3 kịch bản tiết kiệm;
   - xuất chuỗi **cuối mỗi tháng** từ 04/2018 tới 10/2026 cho cả 3 cách: `tiet_kiem_6`, `tiet_kiem_5`, `tiet_kiem_7`, `mot_lan`, `mua_deu`;
   - ghi `results.json` ở dạng dùng thẳng được cho `race` (`dates` = nhãn tháng, `vals`).

   `check.py` tính lại giá trị cuối của tiết kiệm bằng công thức đóng.
2. **`script.md`:**
   - **xoá mọi câu kiểu "chưa có dữ liệu / chưa xếp hạng / thiếu chuỗi"**;
   - đưa kết quả 3 cách vào. Thứ tự giá trị cuối theo số tính được, ví dụ mua đều ≈ 181 triệu, tiết kiệm 6% ≈ 164 triệu, một lần ≈ 145 triệu;
   - nói rõ nghịch lý: mua đúng đỉnh vẫn có lãi nhưng thua tiết kiệm, còn mua đều thắng mà từng âm khoảng 32%;
   - CH05 đổi thành "tiết kiệm: thắng ở đâu, thua ở đâu". Nói khoảng 5–7% đã quan sát, và nếu lãi chỉ 5% thì thứ hạng đổi thế nào;
   - giữ giới hạn backtest ở chương cuối: không cổ tức, phí và thuế, quá khứ không phải dự báo;
   - 1.900–2.500 âm tiết;
   - cập nhật bảng "Biểu đồ" và "Bước lập luận".
3. **`factcheck.md`:** cập nhật theo các câu mới.

## Cổng

- `analysis.py` → `check.py` `OK`;
- `script_lines.py`;
- `studio_lint.py --strict` → 0 lỗi.
