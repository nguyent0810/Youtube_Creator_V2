# W1c-1 — Kết quả sửa mở đầu `ck-f1-tro-cap-that-nghiep`

## Đã làm

- Đổi mở đầu CH00 từ ví dụ giả định sang dữ kiện thật: 332.629 quyết định hưởng trợ cấp thất nghiệp được tiếp nhận để chi trả trong sáu tháng đầu năm 2026.
- Đặt công thức có nguồn 60% ngay câu thứ hai và cập nhật bảng Biểu đồ: CH00 là `counter + bars` với hai dữ kiện thật; CH01 là phép tính **VÍ DỤ GIẢ ĐỊNH**.
- Dời chị Lan xuống đầu CH01, mở bằng câu xác nhận đây là ví dụ giả định để tính.
- Đổi tiêu đề phụ thành hai tiêu đề còn lại của brief; thêm Câu hỏi trung tâm, 5 câu trước khi viết và bảng Bước lập luận.
- Giữ nguyên CH02–CH06, ngoài việc nối mạch từ CH00 mới.
- Không cần đổi số trong `analysis.py`, `check.py`, `results.json`; các phép tính giả định vẫn khớp.

## CH00 mới — nguyên văn

Trong sáu tháng đầu năm hai nghìn không trăm hai mươi sáu, hệ thống tiếp nhận ba trăm ba mươi hai nghìn sáu trăm hai mươi chín quyết định.
Đó là các quyết định hưởng trợ cấp thất nghiệp được tiếp nhận để chi trả.
Nhưng trợ cấp hằng tháng theo luật là sáu mươi phần trăm bình quân lương đóng của sáu tháng gần nhất, không phải toàn bộ lương cũ.
Biểu đồ đầu tiên đặt hai dữ kiện thật cạnh nhau: ba trăm ba mươi hai nghìn sáu trăm hai mươi chín quyết định đã được tiếp nhận, và công thức sáu mươi phần trăm. ‖
Nghịch lý là bạn có thể đã đóng nhiều năm, nhưng khoản đệm vẫn có trần và chỉ chạy trong một số tháng.
Vậy trợ cấp thất nghiệp thật sự đỡ được bạn bao nhiêu tháng, và còn hở bao nhiêu?
Đó không phải câu hỏi chỉ có một con số chung cho tất cả mọi người. ‖
Nó đi qua mức lương đóng, bốn cửa điều kiện, ngày chờ và bậc tháng đã đóng.
Đến cuối video, một ví dụ giả định sẽ cho thấy bảy năm đóng được đổi thành bao nhiêu tháng, rồi khoảng hở cộng dồn ra sao.
Trước hết, ta đặt công thức sáu mươi phần trăm vào một phép tính minh họa, không phải lời hứa về mức nhận của bất kỳ ai.

## Kiểm tra đã chạy

`PYTHONIOENCODING=utf-8 python data/long/ck-f1-tro-cap-that-nghiep/analysis.py`

- Hoàn tất; số ví dụ: trợ cấp 9 triệu/tháng, thiếu 4 triệu/tháng, 7 tháng hưởng, thiếu tích lũy 28 triệu.

`PYTHONIOENCODING=utf-8 python data/long/ck-f1-tro-cap-that-nghiep/check.py`

- `CK-F1 check: OK (7 phép)`.

`PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-f1-tro-cap-that-nghiep`

- Hoàn tất không lỗi.

`PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-f1-tro-cap-that-nghiep --strict`

- `0 lỗi`, còn 7 cảnh báo về mật độ câu ngắn ở các chương; đây là cảnh báo phong cách có sẵn, không phải lỗi strict.

`PYTHONIOENCODING=utf-8 python scripts/long_gate.py ck-f1-tro-cap-that-nghiep --min-syl 1900`

- `ĐẠT`: 2.368 âm tiết, khoảng 10,5 phút; 71 cảnh, 8,9 giây/cảnh; 7 clip khác, 6 ảnh khác, 14 URL nguồn.

## Dữ kiện câu 0 và kiểm chứng

- Câu 0 lấy từ dữ kiện **24** trong `facts.md`: sáu tháng đầu năm 2026 có **332.629** quyết định hưởng TCTN để chi trả.
- Dữ kiện này đã có dòng kiểm chứng **F11** trong `factcheck.md`, nguồn BHXH Việt Nam: https://baohiemxahoi.gov.vn/tintuc/Pages/linh-vuc-bao-hiem-y-te.aspx?CateID=0&ItemID=26844
- Khẳng định 60% ở câu 2 đã có dòng **F02** trong `factcheck.md`.
- Không có khẳng định mới nào chưa kiểm được.

## Clip sheet và thumbnail

- Ticket W1c chỉ sửa kịch bản; không dựng lại clip sheet hay thumbnail trong phạm vi ticket này.
