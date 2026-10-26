# Sổ thất bại MIM / CK / CL

Đọc bảng này trước khi mở một chuỗi, khuôn hoặc lô mới. Mỗi dòng ghi một lần thử đã có số đo, bài học rút ra và thứ đã đổi trong quy trình. Ý tưởng lấy từ ADR 0017 §5 của vietneu-tts; số liệu là của kênh mình.

Thêm một dòng mỗi khi retro tìm ra một thất bại có số đo. Không ghi những gì chưa đo được.

| Ngày | Kênh | Đã thử | Số đo | Bài học | Đã đổi thành |
|---|---|---|---|---|---|
| 12/10 | CK | Bỏ trần tự giới hạn, đăng 5 Short/ngày cộng Long | YouTube trả `uploadLimitExceeded` sau khoảng 10 lần đăng/ngày; vẫn bị chặn sau hơn 18 giờ; kẹt 2 Long và 13 Short | Mỗi kênh có giới hạn riêng, không phải quota dự án | Đăng Long trước Short; khi bị chặn thì chờ khoảng 1 ngày, không thử lại liên tục |
| 12/10 | MIM, CK | Lô Short toàn chữ, rồi một bản vá toàn clip | Chủ kênh từ chối cả hai | Short phải trộn chữ, clip, biểu đồ và sơ đồ | Chuẩn mix v3; build lint `mix` |
| 12–18/10 | MIM, CK | 5 Short/ngày để tăng view | Mỗi Short vẫn kẹt khoảng 1–1,4k view (trung vị MIM 1.139, CK 1.059); kênh chỉ lớn nhờ số lượng | Tăng số lượng không phá được trần | 2–3 Short/ngày, gắn với Long |
| 12–18/10 | CK | Short đọc thị trường và nợ/thẻ tín dụng, bitcoin, VN-Index | 10/30 Short dưới 300 view, gần như không có lượt từ feed | Nhóm chủ đề này yếu trên CK | Dừng Short CK đọc thị trường chung |
| 13–20/10 | MIM | Short dạng "mẹo", chuỗi QR/Flappy | "Ở lại xem" chỉ 11–29% (trung vị kênh 28%) | Mở bằng con số hoặc sự kiện có ngày tháng, không mở kiểu "mẹo" | Khung truyện: năm, người, bước ngoặt |
| 20/10 | MIM, CK | Dùng AVP để dự đoán Short nào vượt trần | AVP không dự báo được view (MIM r ≈ −0,1) | Mỗi kênh có thước đo dự báo riêng | Theo dõi "ở lại xem" (engagedViews/views) cạnh AVP |
| 21/10 | MIM | Chép `spec.sources` vào mô tả công khai | 3 lần đăng bị từ chối (`invalidDescription`); 38 mô tả phải sửa lại | Ghi chú làm việc của agent lọt ra công khai | Tách `sources_internal`; quét mô tả trước khi đăng |
| 21/10 | MIM | Tự đổi clip trùng theo từ khoá | 41 lần đổi sai nghĩa, phải hoàn tác hết | Clip phải được chọn bằng mắt | Xem poster khi chọn clip; dùng `clip_sheet.py` trước khi render |
| 22/10 | MIM, CK | Long với tiêu đề dài 85–100 ký tự, thumbnail không có tên nhân vật chính | CTR 1,6–2,6%, chỉ khoảng 2 nghìn lượt hiển thị/28 ngày (CL: 3,4%, 96,8 nghìn) | Long phải có thứ người xem nhận ra ngay | Tiêu đề khoảng 60 ký tự; khuôn "X Ngoài Đời Thật" |
| 22/10 | CL | Loudnorm một lượt, sfx cắt cứng | Bình luận chê "âm thanh sẹt sẹt" | Đỉnh thật và tiếng tách ở đầu chương | Bộ lọc giọng CL, fade 5 ms, `audio_lint` |
| 21–23/10 | BUD (AI Learning) | Chép bảng tra của FS sang BUD | View/giờ thấp hơn mốc riêng của BUD 3–8 lần | Phải chép cơ chế (khoá cá nhân và lý do xem lại), không chép bề mặt | Trước khi chép, ghi ra mỏ neo và cách xem của kênh đích; thử 5–6 bài, mỗi lần đổi một biến |
| 23/10 | MIM, CK | Ghép Long với loudnorm một lượt | 5/25 lần ghép có đỉnh thật trên −1 dBTP (KAL −0,5) | Bộ mã hoá AAC làm đỉnh vọt lên | 26/10: thêm `alimiter` ở 4x sau loudnorm |
| 14/10 | MIM | Short Turing dùng counter đếm năm 1950 → 2000 | Khung giữa hiện "1.996" | Engine luôn chấm phân cách nghìn | 26/10: counter 1000–2100 phải khai `year` |
