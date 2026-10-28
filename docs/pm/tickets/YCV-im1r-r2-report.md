# Báo cáo YCV-im1r vòng 2

Đã sửa đúng 5 spec p2–p6 theo bài học từ p1. Không render, không đăng, không enqueue, không đổi lịch và không dùng Git.

## Kết quả từng spec

### `mim-p2-tin-nhan-thoai`

- Mở cũ: “Tin nhắn thoại bạn gửi mấy giây? Năm 2023, một mô hình nghiên cứu chỉ cần ba giây giọng mẫu để nói giống một người lạ.”
- Mở mới: “Tin nhắn thoại ba giây bạn gửi dài bằng mẫu giọng mà một mô hình nghiên cứu dùng năm 2023.”
- Kết cũ: “Tin nhắn thoại vẫn cứ gửi. Chỉ đừng để một giọng nói, một mình, quyết định chuyện tiền bạc.”
- Kết mới: “Giọng nói có thể bị sao chép. Nhưng chuyện tiền bạc phải được xác nhận bằng cuộc gọi lại.”
- Cảnh đổi: cảnh 0 nói thẳng tình huống B và bỏ clip trừu tượng `pexels:39687575`, thay bằng tay lướt điện thoại `pexels:38410501`; cảnh 5 từ thẻ slam thành board có mũi tên “cúp máy → gọi lại → số đã lưu”; cảnh 6 chốt lại ý mở, dùng clip nền tay cầm điện thoại.
- 128 chữ. Thời lượng giọng ước tính 33,9 s theo baseline p1 (120 chữ / 31,8 s); lệch p1 khoảng 2,1 s.

### `mim-p3-nghe-nhap-lieu`

- Mở cũ: “Bạn làm nhập liệu: bảng 427 nghề của Tổ chức Lao động Quốc tế năm 2025 xếp nghề của bạn đứng đầu.”
- Mở mới: “Nếu bạn làm nhập liệu, bảng 427 nghề của ILO năm 2025 xếp nghề của bạn đứng đầu.”
- Kết cũ: “Đứng đầu bảng không có nghĩa là mất việc. Nó cho biết phần việc nào sẽ đổi trước.”
- Kết mới: “Đứng đầu bảng không báo trước một cuộc mất việc. Nó báo trước phần việc có thể đổi trước.”
- Cảnh đổi: cảnh 2 có thêm clip nền tay lướt điện thoại `pexels:38410501`; cảnh 3 đổi từ kinetic sang board mũi tên “từng việc nhỏ → chấm khả năng máy làm → lấy trung bình”. Đã bỏ từ phủ định khỏi `acc`.
- 131 chữ. Thời lượng giọng ước tính 34,7 s.

### `mim-p4-ilo-2023-van-phong`

- Mở cũ: “Tháng 8 năm 2023, Tổ chức Lao động Quốc tế chấm từng nhóm nghề trên thế giới trước AI tạo sinh.”
- Mở mới: “Tháng 8 năm 2023, ILO kết luận văn phòng là nhóm duy nhất tiếp xúc cao với AI tạo sinh.”
- Kết cũ: “Một nhóm nghề duy nhất ở mức cao. Câu hỏi còn lại: phần việc nào trong đó, máy làm thay trước.”
- Kết mới: “Một nhóm nghề duy nhất ở mức cao. Điều được đo là phần việc có thể đổi, không phải con người bị thay.”
- Cảnh đổi: cảnh 0 nêu kết luận ngay từ giây 0, thay nền bằng `pexels:38410501`; cảnh 6 bỏ câu hỏi và đổi chữ kết thành “PHẦN VIỆC CÓ THỂ ĐỔI”.
- 130 chữ. Thời lượng giọng ước tính 34,5 s; lệch p3 khoảng 0,3 s.

### `mim-p5-recsys-2016`

- Mở cũ: “Năm 2016, ba kỹ sư Google công bố cách YouTube chọn video đề xuất.”
- Mở mới: “Tháng 9 năm 2016, ba kỹ sư Google mô tả YouTube lọc hàng triệu video xuống vài chục trước mắt bạn.”
- Kết cũ: “Hàng triệu video, vài trăm ứng viên, và vài chục video trên màn hình của bạn.”
- Kết mới: “Hàng triệu video, vài trăm ứng viên, rồi vài chục trên màn hình bạn. Đó là cách bài báo năm 2016 mô tả.”
- Cảnh đổi: cảnh 0 nêu chuỗi “HÀNG TRIỆU → VÀI CHỤC VIDEO” ngay từ đầu, giữ clip đã được dùng `pexels:34337855`; cảnh 4 có thêm clip nền dữ liệu `pexels:28709421`.
- 122 chữ. Thời lượng giọng ước tính 32,3 s.

### `mim-p6-feed-cua-ban`

- Mở cũ: “Video bạn vừa lướt qua được YouTube chọn từ hàng tỉ video. Vì sao người ngồi cạnh bạn lại thấy video khác?”
- Mở mới: “Theo YouTube năm 2021, video bạn vừa lướt qua được chọn từ hàng tỉ video. Vì sao người ngồi cạnh bạn lại thấy video khác?”
- Kết cũ: “Cùng hàng tỉ video, nhưng mỗi người một cách đếm. Và video bạn vừa lướt qua được chọn theo cách đếm của riêng bạn.”
- Kết mới: “Cùng một kho video. Feed của bạn khác vì hệ thống cân tín hiệu của bạn theo một cách khác để đề xuất video.”
- Cảnh đổi: cảnh 4 có clip nền tay lướt điện thoại `pexels:38410501`; giữ nhãn nguồn trên cảnh 0 và biểu đồ “THEO YOUTUBE · 2021”. Đã bỏ từ phủ định khỏi `acc`.
- 122 chữ. Thời lượng giọng ước tính 32,3 s; lệch p5 là 0 s.

Các ước tính dùng cùng tốc độ bình quân của p1 đã duyệt; chỉ render/TTS thật mới xác nhận được thời lượng cuối cùng. Cả năm bài nằm trong 55–135 chữ và cặp p1/p2, p3/p4, p5/p6 đều có chênh ước tính không quá 3 giây.

## Kiểm tra đã chạy

- Đã chạy `python motion/stier/clips.py search <slug> <query> --src pexels` và soi poster cho cả năm bài. Poster: `motion/hf/assets/clips/sheets/mim-p2-tin-nhan-thoai.jpg`, `mim-p3-nghe-nhap-lieu.jpg`, `mim-p4-ilo-2023-van-phong.jpg`, `mim-p5-recsys-2016.jpg`, `mim-p6-feed-cua-ban.jpg`.
- Đã chạy `python motion/stier/build.py <slug> --no-render` tới khi sạch cho: `mim-p2-tin-nhan-thoai`, `mim-p3-nghe-nhap-lieu`, `mim-p4-ilo-2023-van-phong`, `mim-p5-recsys-2016`, `mim-p6-feed-cua-ban`.
- Lỗi đã sửa trong lúc kiểm: neo “nào” không còn trong kết p4; neo “trăm” không còn trong kết p5; neo “chưa” không còn trong câu p2; tỷ lệ phối cảnh p4 được cân lại bằng cách không thêm clip vào cảnh slam.
- Lint/build còn lại: không có lỗi. Không có khẳng định mới hay số mới ngoài factcheck đã chỉ định.
