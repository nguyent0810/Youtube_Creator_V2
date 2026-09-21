# 4 content pillar của kênh FS: sức chứa và hướng mở rộng

Mỗi pillar được xây theo ba tầng:

1. **Chủ đề cố định.** Mỗi chủ đề là một phép duyệt trên dữ liệu tập đóng (`factory/pillars/tables.py`). Mọi quan hệ đều tính ra được từ bảng.
2. **Chủ đề có nguồn.** Lời kinh, bản dịch, số liệu thiên văn chỉ được lấy từ `SOURCED` hoặc `data/`, luôn kèm URL.
3. **Chủ đề hằng ngày.** Gắn với lịch thật của ngày đăng nên không bao giờ cạn. Mỗi pillar có 2–3 góc hằng ngày, luân phiên theo ngày.

Hàm `next_draft` chỉ trả về bài đã qua bộ kiểm. Bài nào trượt kiểm thì bị bỏ qua, không cắt bớt và không sửa tay.

Kiểm tra sức chứa (chạy khô, không ghi dữ liệu):

    python scripts/pillar_capacity.py 2026-10-01 730

## Sức chứa đo ngày 21/09/2026

| Pillar | Chủ đề cố định | Hằng ngày | Mô phỏng 730 ngày |
|---|---|---|---|
| 12 Con Giáp (11:30) | 85 | tuổi xung ngày · tuổi hợp ngày | chạy đủ, 0 bài trượt kiểm |
| Lục Trụ (15:00) | 78 | can ngày × Nhật chủ · nạp âm ngày · tàng can của chi ngày | chạy đủ, 0 bài trượt kiểm |
| Kinh Dịch (19:00) | 592 | chưa có | 591 ngày, sau đó cần thêm nguồn |
| Mệnh số (22:00) | 84 | tú của ngày · cung/chòm của ngày | chạy đủ, 0 bài trượt kiểm |

## Hướng mở rộng tiếp theo, theo thứ tự nên làm

**Kinh Dịch**
- Chạy lại `scripts/fetch_kinhdich.py` định kỳ. Wikisource tiếng Việt hiện mới có 9/64 quẻ bản dịch Ngô Tất Tố; mỗi quẻ được bổ sung thêm khoảng 8 chủ đề (lời kinh, 6 hào, lời Tượng).
- Lời Thoán truyện và Văn ngôn đã có sẵn trong các trang đó nhưng chưa được khai thác, khoảng 5 đoạn mỗi quẻ.
- Chưa có loại hằng ngày. Mai Hoa Dịch Số (lập quẻ theo năm, tháng, ngày, giờ) là ứng viên, nhưng phải có nguồn cho công thức trước khi dùng.

**12 Con Giáp**
- Tam hình, tự hình, lục phá: tính được từ bảng, nhưng cần nguồn cho định nghĩa.
- Tuổi xung năm và xung tháng, gắn với năm và tháng âm thật: loại hằng năm và hằng tháng.

**Lục Trụ**
- Nhật chủ × 10 thập thần từng cái (thay vì theo nhóm): 100 chủ đề.
- 12 trường sinh (Trường Sinh, Mộc Dục, …): cần nguồn cho bảng.
- Đại vận: cần nguồn cho cách khởi vận.

**Mệnh số / huyền học**
- Cân xương đoán số: đang bị chặn (`CAN_XAC_MINH`) cho tới khi có bảng trọng lượng và bài thơ gốc.
- Lịch sử huyền học: mỗi mục cần một `Sourced` riêng, không viết theo trí nhớ.

## Lỗi dữ liệu nguồn đã phát hiện

vnlunar **sai** ở các điểm sau, nên kênh không dùng vnlunar cho những mục này:
- **Nạp âm:** ví dụ Bính Tý bị ghi là Lộ Bàng Thổ, đúng phải là Giản Hạ Thủy. Kênh dùng bảng `NAP_AM` (zh-yue.wikipedia 納音).
- **Con vật của 28 tú:** 5 tú bị ghi sai (Tỉnh ghi "Dẫn", Nguy ghi "Nhén", Đê ghi "Lễ", Đẩu ghi "Hề", Bích ghi "Chốc"). Kênh dùng bảng `TU28` (zh.wikipedia 二十八宿). Hậu quả: 11 video Lịch đã đăng đọc sai tên con vật.
- **Tên tú 參:** vnlunar ghi là "Thâm"; tên phổ thông là Sâm (xử lý qua `TU_ALIAS`).
