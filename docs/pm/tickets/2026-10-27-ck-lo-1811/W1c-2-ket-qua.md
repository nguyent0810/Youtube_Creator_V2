# W1c-2 — Kết quả sửa mở đầu `ck-f2-vien-phi-bhyt`

## Đã làm

- Đổi tiêu đề sang tiêu đề (1) của Content Brief: `Có Bảo Hiểm Y Tế Vẫn Trả 40%: Tiền Viện Phí Đi Đâu?`; hai tiêu đề còn lại đã chuyển vào dòng **Tiêu đề phụ**.
- Bổ sung đầu `script.md`: câu hỏi trung tâm, 5 câu trước khi viết và bảng bước lập luận.
- Viết lại CH00 theo hook dữ kiện thật, không dùng nhân vật giả định: cuối 2024 có 94,29% dân số tham gia BHYT, nhưng năm 2025 chi trực tiếp từ tiền túi khoảng 40% tổng chi y tế.
- Đổi biểu đồ mở CH00 thành hai cột số liệu thật; thêm dòng kiểm chứng gộp cho hai dữ kiện hook trong `factcheck.md`.
- Đưa anh Minh xuống câu đầu CH01, với câu xác nhận rõ: đây là ví dụ giả định để tính, không phải ca bệnh hoặc báo giá thật.
- Giữ nguyên CH02–CH06, ngoài phần nối vòng mở ở CH00 với kết CH06.

## CH00 mới (nguyên văn)

> Cuối năm hai nghìn không trăm hai mươi bốn, chín mươi bốn phẩy hai chín phần trăm dân số đã có bảo hiểm y tế.
> Nhưng năm hai nghìn không trăm hai mươi lăm, tiền túi vẫn khoảng bốn mươi phần trăm tổng chi y tế.
> Trên màn hình là hai cột số. ‖
> Đó là nghịch lý.
> Nó nói một tỷ lệ trên thẻ, một khoản trên hóa đơn và một khoản gia đình phải xoay không phải lúc nào cũng là cùng một thứ.
> Vậy có thẻ bảo hiểm y tế rồi, vì sao người Việt vẫn tự trả gần nửa tiền khám chữa bệnh?
> Phần ấy nằm ở đâu trên hóa đơn? ‖
> Video này không dùng hai tỷ lệ toàn hệ thống để đoán hóa đơn của riêng bạn.
> Nó sẽ tách từng lớp tiền: phần trong phạm vi, phần đồng chi trả, phần ngoài phạm vi và chi phí đi cùng.
> Cuối video, ta quay lại.
> Lộ trình miễn chi phí khám chữa bệnh cơ bản đến năm hai nghìn không trăm ba mươi có thể chạm lớp nào, và lớp nào vẫn ở ngoài?

## Kiểm tra

| Lệnh | Kết quả |
|---|---|
| `python data/long/ck-f2-vien-phi-bhyt/analysis.py` | Số waterfall và các ngưỡng được in lại đúng. |
| `python data/long/ck-f2-vien-phi-bhyt/check.py` | `F2 check: OK (8 phép)`. |
| `python motion/long/script_lines.py ck-f2-vien-phi-bhyt` | CH00: 188 âm tiết; toàn bài: 2.698 âm tiết. |
| `python motion/long/studio_lint.py ck-f2-vien-phi-bhyt --strict` | `0 lỗi, 7 cảnh báo`. |
| `python scripts/long_gate.py ck-f2-vien-phi-bhyt --min-syl 1900` | `ĐẠT` — 2.698 âm tiết, 82 cảnh, 8,6 giây/cảnh, 6 clip khác, 6 ảnh khác, 18 URL nguồn. |

CH00 lấy câu 0 từ dữ kiện **#23** trong `facts.md` (95,525 triệu người, khoảng 94,29% dân số tham gia BHYT cuối 2024), kết hợp dữ kiện **#19** (chi tiền túi khoảng 40% năm 2025). Cả hai URL đã được ghi ở `factcheck.md`.

Không còn khẳng định nào trong phần sửa không kiểm được.

## Cảnh báo lint còn lại

- CH01, CH02, CH03, CH04, CH05 và CH06 có mật độ câu ngắn dưới gợi ý.
- CH04 cảnh 7–9 có ba cảnh `counter` liên tiếp.

Đây là cảnh báo có sẵn ở các chương được yêu cầu giữ nguyên; lint nghiêm ngặt vẫn trả 0 lỗi.

## Tài sản QA

- Clip sheet: `output/long/ck-f2-vien-phi-bhyt/qa_clips.jpg` — không chạy lại trong ticket W1c vì ticket chỉ sửa lời mở và không cho sửa cảnh.
- Thumbnail: `motion/long/thumbs/ck-f2-vien-phi-bhyt_t1.html` — không sửa hoặc soi lại trong ticket W1c.
