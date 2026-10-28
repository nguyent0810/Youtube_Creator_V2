# Đối chiếu phân tích của bot (ChatGPT trên điện thoại) với số liệu kênh

Ngày 27/10/2026. Chủ kênh chuyển báo cáo của bot. Bot đếm view từ lúc đăng tới 27/10: MIM có 8 Long, CK có 8 Long. File này ghi Claude đồng ý điểm nào, không đồng ý điểm nào, và đổi gì.

## Đồng ý, và đã làm theo

1. **CK: số liệu thật của Việt Nam thắng bài giáo trình.**
   - Hai Long thắng: "3 triệu mỗi tháng theo VN-Index 8 năm" (82 view) và "11 đợt xếp hàng mua vàng" (55 view). Cả hai đều backtest trên dữ liệu thật.
   - Các bài giáo trình chỉ được 9–13 view: lãi kép, Chứng Khoán Từ Số 0 bài 1, VN-Index mất 115 điểm.
   - **Đã đổi:** ticket W2 của lô 18–25/11 bắt mỗi bài có ≥ 2 biểu đồ dữ liệu thật Việt Nam, kèm nguồn, ít nhất một biểu đồ ở CH00 hoặc CH01. Kho của F1 và F2 đã có số thật (332.629 quyết định hưởng trợ cấp trong 6 tháng đầu 2026; tỉ lệ chi tiền túi khoảng 40%). F3 và F4 chỉ có Khảo sát mức sống của Cục Thống kê, nên yếu hơn.
2. **Cắt 8–10 Short cho một Long thì Short kể hết nội dung, người xem không cần mở bản dài.** Ví dụ AlphaGo: gần 10 Short, bản dài chỉ 38 view.
   - **Đề xuất:** 2–3 Short mỗi Long. Mỗi Short đi một góc riêng, không kể kết, và gắn "video liên quan" trỏ về Long. Áp từ lô Short tiếp theo, **chờ chủ kênh duyệt**.
3. **Thumbnail CK quá kỹ thuật.** Ví dụ bài "mất 115 điểm" vẽ sơ đồ giờ khớp lệnh. Đã có luật một tiêu điểm (`thumb_mot_tieu_diem`) cho lô mới.

## Không đồng ý, hoặc cần đo thêm

1. **"Nhân vật hư cấu làm giảm niềm tin."** Chính ví dụ thắng mà bot đưa ra lại phản bác điều này: Long "3 triệu theo VN-Index" (82 view, thắng nhất CK) dùng cặp nhân vật giả định "Cô Đều, Anh Xui, Chị May". Short thắng của CK ("3 tỷ của 30 năm sau", 3.210 view) cũng là ví dụ giả định.
   - **Giả thuyết đúng hơn:** nhân vật hư cấu không hại, nếu đi kèm dữ liệu thật. Chỉ có nhân vật mà không có dữ liệu mới yếu.
   - Lô 18–25/11 giữ nhân vật và thêm dữ liệu thật (mục trên). Đo bằng ô `LIB-CK1`.
2. **MIM: "dừng làm chuyện lịch sử công nghệ".** Số mẫu quá nhỏ, chỉ 8 Long, từ 8 đến 371 view.
   - Theo Studio (28 ngày), "AI Đã Chết Hai Lần" là bài lịch sử nhưng có CTR cao nhất, 4,2%.
   - "AI giả giọng" nhiều view hơn vì có 2.180 lượt hiển thị, nhưng CTR chỉ 1,7%.
   - Vì vậy không nên rút ra luật "đời sống thắng lịch sử" khi chưa xem CTR và giữ chân 30 giây của từng cặp. Đây cũng là bước mà ChatGPT tự gợi ý.
   - **Giữ lịch MIM tới 30/11** (đã lên). Lô MIM tháng 12 sẽ trộn hai nhánh: AI tác động tới tiền và an toàn của người Việt, và người + năm + bước ngoặt. Rồi đo cùng điều kiện.
3. **"Giọng tổng hợp và slide chữ"** chưa có bằng chứng là bị YouTube phạt. Riêng "slide chữ" thì đúng: CK có 45% cảnh là thẻ chữ, và đã có luật biểu đồ ≥ 35%.

## Việc cần chủ kênh quyết

- Đổi tỉ lệ cắt Short xuống 2–3 Short mỗi Long, mỗi Short một góc riêng.
- Kéo số liệu Studio cho 2 cặp đối chứng: Impressions, CTR, Browse/Suggested, AVD, giữ chân 30 giây.
  - MIM: AI giả giọng và AlphaGo.
  - CK: 3 triệu theo VN-Index và mất 115 điểm.
