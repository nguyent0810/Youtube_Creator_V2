# W1c-5 — Kết quả sửa mở đầu `ck-c6-gia-tran-san-t2`

## Đã làm

- Đổi dòng tiêu đề thành tiêu đề (1) của Content Brief: `Mua Thứ Hai, Thứ Tư Mới Bán Được: T+2 Là Gì?`.
- Đưa hai tiêu đề còn lại vào hai dòng “Tiêu đề phụ”.
- Thêm “Câu hỏi trung tâm”, “5 câu trước khi viết”, bảng “Bước lập luận”, và cập nhật bảng “Biểu đồ” cho CH00/CH01.
- Viết lại CH00 theo hook số liệu thật; dời ví dụ giả định anh Tuấn xuống đầu CH01 và nêu rõ đây là ví dụ để tính.
- Giữ nguyên CH02–CH06.

## CH00 mới (nguyên văn)

> Ngày chín tháng tư năm hai nghìn không trăm hai mươi lăm, VN-Index giảm ba phẩy bốn mươi phần trăm về một nghìn không trăm chín mươi bốn phẩy ba điểm.
> Phiên đó có một trăm bốn mươi bảy mã giảm sàn.
> Đây là hai số thật của phiên mở đầu biểu đồ hôm nay.
> Chúng cho thấy một bảng giá đỏ có thể rộng đến mức nào.
> Nhưng chúng chưa trả lời câu khó hơn cho người vừa mua trong phiên ấy.
> Nếu lệnh mua đã khớp sáng thứ Hai, vì sao có lúc phải tới chiều thứ Tư mới có thể bán?
> Người mua đúng lúc giá rơi cũng chưa chắc có cổ phiếu trong ô bán ngay.
> Đó là nghịch lý của video này.
> Giá trần và giá sàn giới hạn giá trong một phiên.
> Còn lịch thanh toán giới hạn thời điểm chứng khoán vừa mua được phân bổ.
> Hai chiếc khóa này dễ bị trộn vào một.
> Vì vậy, câu hỏi trung tâm là: mua cổ phiếu sáng thứ Hai, vì sao phải tới chiều thứ Tư mới bán được, và điều đó đã làm ai mất tiền?
> Ta sẽ tách từng chiếc khóa, rồi quay lại phiên đỏ này ở cuối video.
> Trước hết, ta cần một ví dụ giả định để nhìn thấy giá và thời điểm đứng ở hai hàng khác nhau.

## Kiểm tra đã chạy

- `python data/long/ck-c6-gia-tran-san-t2/analysis.py`: tạo lại số tính, khớp các giả định.
- `python data/long/ck-c6-gia-tran-san-t2/check.py`: `C6 check: OK (11 phép)`.
- `python motion/long/script_lines.py ck-c6-gia-tran-san-t2 --allow-repeat-line`: tổng 2.412 âm tiết; CH00 230 âm tiết; tổng 189 câu.
- `python motion/long/studio_lint.py ck-c6-gia-tran-san-t2 --strict`: `0 lỗi, 2 cảnh báo` (cảnh báo phân bố câu ngắn ở CH00 và CH03).
- `python scripts/long_gate.py ck-c6-gia-tran-san-t2 --min-syl 1900`: **TRƯỢT (19 lỗi)**, không in ĐẠT.

## Lý do cổng tổng chưa đạt

Topic hiện có 0 cảnh ở cả bảy chương, thiếu HUD, TTS, `spec.youtube` và bảng `say`; vì vậy cổng báo 19 lỗi, gồm không đủ loại cảnh mỗi chương, chưa TTS, 689,1 giây/cảnh, và trường `spec.youtube` còn thiếu. Ticket W1c chỉ cho ghi `script.md`, `factcheck.md`, `analysis.py`, `check.py`, `results.json` và báo cáo; không cho sửa `gen_scenes.py`/`spec.json` hay chạy bước dựng để khắc phục các lỗi này. Không có clip sheet hoặc thumbnail để báo cáo ở pha W1c.

## Nguồn câu 0

Câu 0 lấy từ dữ kiện **#11** trong `facts.md`: phiên 09/04/2025, VN-Index giảm 38,49 điểm (3,40%) về 1.094,3 điểm; URL VTV đã mở: https://vtv.vn/kinh-te/vn-index-giam-tiep-gan-40-diem-20250409171341275.htm. Câu 1 dùng dữ kiện **#12** cùng URL: 147 mã giảm sàn.

## Khẳng định chưa kiểm được

Không bổ sung khẳng định chưa kiểm được. Các giới hạn sẵn có về thuế, phí chung và T+0 vẫn giữ nguyên ở CH06/factcheck.
