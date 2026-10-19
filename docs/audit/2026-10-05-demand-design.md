# Thiết kế bước 3: đọc nhu cầu (lộ trình audit 05/10/2026)

Chốt sau 2 vòng phản biện Claude ↔ Grok. Nguồn và điều khoản: [`2026-10-05-demand-sources-research.md`](2026-10-05-demand-sources-research.md).
Bản đầu của Claude có "khoảng trống" suy từ từ khoá tìm kiếm, tự xếp lại chủ đề, RSS Google Trends, gắn nhãn
`demand=` để đo. Grok bác gần hết; bản cuối nhỏ và trung thực.

## v1: ba mục trong brief tuần (`scripts/feedback_loop.py` → `data/briefs/<KÊNH>.md`)

| Mục | Nguồn | Quy tắc |
|---|---|---|
| **(A) Từ khoá đã dẫn người xem tới kênh** | YouTube Analytics của chính kênh, `insightTrafficSourceDetail` + `YT_SEARCH` | **Một** truy vấn, `sort=-views`, `maxResults=25`, không đi trang; 28 ngày gồm cả hai đầu tới **mốc Analytics của bảng điểm**. Rỗng → nói rõ là rỗng; 400 → "lỗi"; chưa có mốc → không gọi. In nguyên, không tỉ lệ, không "mới" |
| **(B) Mức quan tâm (Wikipedia tiếng Việt)** | Wikimedia Pageviews, `agent=user`, CC0 | Danh sách chủ đề `data/demand/<KÊNH>.json` do chủ kênh sửa. Mức = **trung vị của tổng theo ngày** các bài trong chủ đề (28 ngày tới hôm qua UTC; ngày không có số = 0). So cùng kỳ: lùi **365 ngày**; chỉ hiện tỉ lệ khi cả hai năm ≥ 20/ngày, còn lại "chưa đủ"; năm trước không có (404 hoặc toàn 0) → "chưa có cùng kỳ"; lỗi/404 năm nay → "thiếu". Cache `wiki_daily`, chỉ lấy phần đuôi chưa có; 2 ngày gần nhất không cache. Tuần tự, 1 s/request, User-Agent có URL liên hệ, lùi khi 429 |
| **(C) Khoảng trống (YouTube Studio → Trends)** | Dán tay (không có API) | `data/demand/<KÊNH>-studio.md`, dòng đầu `Ngày: YYYY-MM-DD`; chỉ đưa vào brief khi ≤ 14 ngày tuổi |

`--no-collect` vẫn chạy (A) và (B); chỉ bỏ phần đo `video_metrics`.

## Quyết định

| # | Quyết định | Vì sao |
|---|---|---|
| 1 | Từ khoá tìm kiếm ghi là "đã dẫn người xem tới kênh", **không phải khoảng trống** | Dòng có view = nhu cầu đã được đáp ứng; khoảng trống thật chỉ có ở Studio (không API) |
| 2 | Không tỉ lệ / "mới" cho từ khoá | Top 25 bị cắt + ngưỡng riêng tư: vắng mặt ≠ 0 |
| 3 | **Không tự xếp lại chủ đề** (`next_draft` giữ nguyên) | Chủ đề FS là bảng đóng; lượt xem Wikipedia của 12 con giáp theo mùa học/tin tức, không phải nhu cầu tuần này. Biến nhu cầu thành chủ đề là việc của Claude khi viết pack |
| 4 | Không gắn nhãn `demand=` để "đo" | Không có nhóm đối chứng (một video/dòng/ngày); muốn đo phải tung đồng xu |
| 5 | Không xây RSS Google Trends, GDELT, lịch chạy hằng ngày | Mẫu thật 05/10: 10 mục, toàn thể thao/xổ số/thời tiết |
| 6 | So **cùng kỳ năm trước**, không so 28 ngày với 84 ngày trước | Mùa học (lịch sử), tin tức |
| 7 | `data/briefs/` và `data/demand/*-studio.md` vào gitignore | Brief chứa từ khoá tìm kiếm của kênh (dữ liệu Analytics được cấp quyền) |
| 8 | Từ khoá không lưu bảng thô nào ngoài brief | Gọn nhất về điều khoản lưu trữ dữ liệu API |
| 9 | Đuôi cửa sổ rỗng (404) khi cache đã có phần còn lại → tính 0, **không ghi**; ngày vắng trong payload chỉ ghi cache khi payload có ngày muộn hơn | Grok vòng 3: lần chạy sau chỉ hỏi vài ngày cuối; dump chưa có số thì cả chủ đề thành "thiếu", hoặc ngày chưa chốt bị đóng băng thành 0 |
| 10 | Bài chưa có năm trước (404) = chuỗi 0 trong bộ nhớ cho bài đó; các bài khác vẫn so được | Grok vòng 3: một bài mới xoá phép so cả chủ đề |
| 11 | Nhãn "thiếu" ghi tên bài hỏng | Phân biệt sai tên bài với lỗi mạng, để chủ kênh sửa danh sách |
| 12 | (A) bắt mọi lỗi API (429 kéo dài, mất mạng, 5xx) → "lỗi" | Review: trước đó chỉ bắt 400, lỗi khác làm chết cả brief và các kênh sau |
| 13 | Giãn nhịp cả sau request lỗi; bản dán Studio phải có ngày ở **dòng đầu**, không nhận ngày tương lai | Review hai trục |

## Đo thật lần đầu (MIM, 05/10/2026)

"Trí tuệ nhân tạo" 1.022 lượt xem/ngày, ×2,51 so với cùng kỳ; "ChatGPT / OpenAI" 450, ×1,57; Google, Facebook,
Bitcoin đang giảm (×0,27–0,63). Từ khoá tìm kiếm của kênh chỉ còn 3 dòng (video cũ đã ẩn).

## Chưa làm

Thăm dò từ khoá cho FS/BUD/CL (cần credential trên máy sản xuất); danh sách theo dõi cho FS/BUD/CL; mốc Analytics của
kênh rất nhỏ có thể đến muộn vì ngày 0 view không có dòng nào (an toàn: cửa sổ đóng muộn, không bao giờ đóng sớm).
