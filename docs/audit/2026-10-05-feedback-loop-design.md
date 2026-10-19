# Thiết kế vòng phản hồi analytics (bước 2 của lộ trình audit 05/10/2026)

Chốt sau 2 vòng phản biện Claude ↔ Grok (grok-4.7, chỉ đọc repo). Bản đầu của Claude có hồi quy
Bayes + Thompson sampling; Grok bác vì dữ liệu hiện có **không tách được** dòng nội dung và giờ đăng.
Bản cuối nhỏ hơn và trung thực hơn: đo đúng, thí nghiệm đúng, đề xuất có điều kiện.

## Vì sao không "tối ưu" ngay

Ở FS/BUD/CL, mỗi dòng luôn đăng **cùng một giờ** (`PILLARS` trong `factory/pillars/topics.py`,
`factory/lines/cl.py`, `factory/lines/bud.py`). Dòng kém hay giờ kém là cùng một biến: không mô hình
nào tách được. Thêm vào đó là các cú sốc cấp kênh (CL dồn 61 upload ngày 30/09; cập nhật Shorts
"original" 01/10/2026) sẽ bị tính nhầm vào dòng nào đăng trong tuần đó.

## Ba phần

### 1. Đo (`factory/scoreboard.py` + `factory/analytics.py`)

- Bảng `video_metrics` trong `state.sqlite`: mỗi video một dòng cho **cửa sổ 7 ngày đầu**.
- Neo vào **giờ lên sóng thật** (`status.publishAt` khi còn hẹn giờ, `snippet.publishedAt` khi đã
  public), đổi sang **ngày giờ Thái Bình Dương** bằng luật DST tự viết (Windows không có tzdata).
  YouTube Analytics tính ngày theo giờ PT: 11:30 giờ VN rơi vào ngày PT hôm trước, 22:00 thì không.
- Cửa sổ = ngày lên sóng (PT) tới +6, gồm cả hai đầu. **Vì sao 7 chứ không 3:** Analytics chỉ có số theo
  ngày PT, nên "3 ngày" thật ra dài 51 giờ nếu lên sóng 20:30 PT nhưng 71 giờ nếu 00:30 PT — thí nghiệm
  xoay giờ sẽ đo nhầm độ dài cửa sổ (review Standards tìm ra). 7 ngày: ~146–168 giờ, lệch tối đa ~13%
  và gắn với giờ đăng; thực tế nhỏ hơn vì view của Shorts dồn vào mấy ngày đầu. Đổi lại kết quả đến
  chậm hơn 4 ngày.
- Chỉ coi là **đóng** khi Analytics đã có số của ngày cuối (thăm dò một lần mỗi lần chạy; mốc được lưu
  vào `metrics_meta` để dựng lại brief không cần mạng).
- Gom theo ngày lên sóng: một truy vấn `dimensions=video` cho cả nhóm (`filters=video==id1,...`, tối đa
  500), một truy vấn `dimensions=video,insightTrafficSourceType` để cộng view từ feed Shorts (bị từ chối
  thì hỏi từng video). Đi hết các trang (`maxResults`/`startIndex`). **Không gửi `sort`**: sort theo
  `engagedViews` có thể bị 400 và làm cột quyết định NULL vĩnh viễn (Grok vòng 3).
- Lưu: `views`, `engagedViews`, view từ feed Shorts, `averageViewDuration`, `averageViewPercentage`,
  thời lượng video. Không lưu `subscribersGained` (với bộ lọc video, nó chỉ đếm sub trên trang xem,
  gần như bằng 0 với Shorts).
- `engagedViews` bị API từ chối (400) → thử lại chỉ với `views`, lưu `engaged_views = NULL`,
  **không xếp hạng** video đó. Không bao giờ chép `views` sang cột quyết định. Lần thử lại cũng hỏng
  (lỗi khác) → không ghi gì, để lần chạy sau; một nhóm hỏng không làm dừng cả kênh.

### 2. So sánh (`factory/scoreboard.py`)

- Thước đo quyết định: **thứ hạng phần trăm của `engagedViews` trong cùng tuần** (tuần ISO theo ngày
  PT), cùng kênh, cùng loại (short/long). Hoà thì lấy hạng trung bình (midrank).
- Tuần chỉ được xếp hạng khi **mọi video trong tuần đã đóng cửa sổ**. Bỏ hẳn tuần 28/09–04/10/2026
  (lẫn cú sốc 30/09 và 01/10) và mọi tuần trước đó. Tuần dưới 15 video cùng loại: hiển thị trong danh sách
  tuần nhưng **không xếp hạng** (pool 2 video thì hạng chỉ là 0 hoặc 1 — một video dài sẽ đứng đầu brief
  của Shorts).
- Dòng = tiền tố slug dài nhất khớp (`cl-hoso-` không bị nhầm sang `cl-hs-`). Giờ = giờ VN lúc lên sóng.
- Bảng điểm và gợi ý chỉ dùng **4 tuần đã đóng gần nhất** (theo mốc Analytics có số). Không dùng "28 ngày
  lịch": tuần chỉ đóng sau 12 ngày nên 28 ngày lịch còn ~16 ngày dùng được, mỗi ô giờ không bao giờ đủ
  5 video (Grok vòng 4). Views thô luôn in cạnh thứ hạng.
- Brief (`data/briefs/<KÊNH>.md`) cho pha sinh trong chat: điểm từng dòng (trung vị, IQR, n); 5 video
  cao nhất và thấp nhất kèm tiêu đề, câu mở đầu, chủ đề; các góc (angle) xếp hạng trong từng dòng
  → danh sách "viết thêm kiểu này".

### 3. Thí nghiệm xoay giờ (lần ghi tự động duy nhất)

- Ngày `d`, dòng thứ `i` nhận giờ thứ `(i + d) mod n` trong các giờ **không ghim** của kênh. Mỗi dòng
  vẫn đúng 1 video/ngày, nên không làm cạn pack hữu hạn; chỉ hoán đổi giờ.
- Ghim: dòng Lịch (FS `lich` 06:00 nằm ngoài `PILLARS`; BUD `lich` 06:30) — đó là giờ hẹn quen của khán giả.
- Bật theo kênh trong `factory/channels.py` (`rotate`). FS và BUD bật; **CL tắt** trong giai đoạn cứu kênh,
  brief ghi rõ "chưa tách được hiệu ứng giờ".
- `make_pillars_day` chống trùng theo **(dòng, ngày VN)**, không theo `(dòng, giờ)`: đổi giờ không được
  đẻ thêm video thứ hai và không đốt chủ đề kế tiếp. Bundle đã ghi không bao giờ bị sửa giờ.
- Ngày làm dở (đã có bài theo giờ cũ): giờ đã có video là của nó; dòng còn lại lấy giờ theo công thức
  nếu còn trống, không thì lấy giờ trống còn lại — không bao giờ hai video cùng một phút.

### Đề xuất giờ cố định: chỉ là gợi ý trong brief, không tự áp

Sau khi đủ dữ liệu xoay: với mỗi dòng Shorts, **trong 4 tuần đã đóng gần nhất**, so giờ tốt nhất và kém nhất
bằng trung vị thứ hạng. Chỉ gợi ý
khi mỗi ô có **n ≥ 5** từ **ít nhất 2 tuần khác nhau**, tuần ≥ 15 video, và chênh **≥ 0,25** hạng.
Luôn in views trung vị thô bên cạnh: chênh 0,25 hạng có thể chỉ là 900 so với 1.100 view.

## Cố ý không làm trong lần này

Hồi quy, Thompson sampling, biến thứ trong tuần, tương quan tín hiệu kịch bản ↔ retention (chọn mẫu
lệch: video ít view không có đường cong), đường cong retention, cửa sổ 28 ngày, tự áp giờ cố định,
xếp lại chủ đề tự động. Lý do chung: chưa đủ dữ liệu sạch sau 01/10 để những thứ đó không in ra nhiễu.
