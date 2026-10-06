# Nghiên cứu nguồn "demand sensing" cho FS / BUD / CL (05/10/2026)

Câu hỏi: lấy tín hiệu "người xem Việt đang muốn gì" ở đâu, **không đốt quota của 3 project upload** và
**không scrape trái ToS**. Mọi khẳng định có số nguồn `[n]` (danh sách cuối file, truy cập 05/10/2026).
Chỗ nào **chưa kiểm chứng được** thì ghi rõ. Nguồn thứ cấp (nếu có) gắn nhãn (SECONDARY).

---

## 1. TL;DR

- **Comment trong repo đúng**: `search.list` có hạn mức RIÊNG 100 lần gọi/ngày (bucket "Search Queries"),
  mỗi lần 1 đơn vị trong bucket đó, không còn là 100 đơn vị/lần như trước [1][2][3][5]. `videos.insert` cũng
  có bucket riêng 100 lần/ngày [1][2]. Các lệnh đọc khác 1 đơn vị, `videos.update` 50 đơn vị, chung
  10.000 đơn vị/ngày/project [1][2].
- **Quota tính theo Google Cloud project**, không theo kênh/người dùng: dùng tài nguyên ở project này
  không ảnh hưởng quota project khác [11]; API key "identifies your project" và quyết định quota [7].
  → đọc bằng API key ở **project riêng** thì 0 đơn vị bị trừ ở 3 project upload.
- **Nhưng cẩn thận chính sách**: Developer Policies III.D.1.c buộc "exactly one (1) API Project" cho
  mỗi API Client [8], ToS §15 cấm "exceed or circumvent" quota [9]. Project nghiên cứu chỉ sạch nếu nó là
  **một API Client riêng, mục đích riêng**. Bản thân mô hình hiện tại (1 phần mềm factory, 3 project)
  cũng đáng để chủ dự án xem lại (mục 5).
- **`chart=mostPopular` gần như vô dụng cho 3 ngách**: từ 21/07/2025 nó chỉ lấy video từ các chart
  Trending Music, Movies, Gaming [3]. Đừng xây quy trình dựa vào nó.
- **Nguồn nên dùng (miễn phí, không quota YouTube):** (1) YouTube Analytics `insightTrafficSourceDetail`
  với `YT_SEARCH`: từ khoá người xem đã gõ để tìm ra video của chính kênh [12][13]; (2) RSS "Trending
  now" của Google Trends `geo=VN`, có nút Export→RSS chính thức trên UI [19][20]; (3) Wikimedia
  Pageviews API cho vi.wikipedia, dữ liệu CC0 [28][32]; (4) tab Trends trong YouTube Studio, chỉ thao tác tay [27].
- **Nên tránh:** `suggestqueries.google.com` (API không chính thức, Google đã chặn truy cập trái phép từ
  2015 [25]); `pytrends`/gọi endpoint nội bộ của Trends Explore (robots.txt chặn `/explore?` [21]);
  scrape YouTube (YouTube ToS + Policies III.E.6 [26][8]); TikTok Research API (chỉ cho nghiên cứu học
  thuật/phi lợi nhuận ở một số vùng [41]).
- **RSS báo Việt (VnExpress, Tuổi Trẻ, Dân Trí)** ghi rõ cung cấp miễn phí cho "cá nhân và các tổ chức
  phi lợi nhuận" [37][38][40]. Kênh kiếm tiền **không nằm trong phạm vi đó** → cần xin phép hoặc bỏ.
  Thanh Niên chỉ yêu cầu ghi nguồn khi dùng lại tin [39]. GDELT là đường thay thế hợp lệ cho tin
  pháp luật (miễn phí cả dùng thương mại, cần ghi nguồn) [33].
- **Ngân sách quota đề xuất:** 0 đơn vị Data API trên 3 project upload; Analytics API khoảng 3–6 request/ngày
  (bucket Analytics riêng của mỗi kênh). Nếu chủ dự án duyệt project nghiên cứu thì dưới 100 đơn vị/ngày
  ở project đó.

---

## 2. Q1: YouTube Data API: chi phí và tách biệt quota

### 2.1 Bảng chi phí (tài liệu cập nhật 15/09/2026 [1])

| Method | Chi phí | Bucket | Cần OAuth? | Ghi chú |
|---|---|---|---|---|
| `search.list` | 1 | **Search Queries: 100 lần/ngày** [1][2][5] | Không, trừ `forMine`/`forContentOwner` [5] | `maxResults` 0–50 [5] |
| `videos.list` (kể cả `chart=mostPopular`, `regionCode`, `videoCategoryId`) | 1 [4] | chung 10.000 | Không, trừ `myRating` [4] | `maxResults` 1–50, mặc định 5 [4] |
| `playlistItems.list` | 1 [1] | chung 10.000 | Không với playlist công khai [7] | |
| `channels.list` | 1 [1] | chung 10.000 | Không với dữ liệu công khai [7] | |
| `videoCategories.list` | 1 [1][6] | chung 10.000 | Không ghi rõ trong trang [6] | lọc bằng `regionCode` hoặc `id` [6] |
| `i18nRegions.list` | 1 [1] | chung 10.000 | | |
| `videos.insert` | 1 [1] | **Uploads: 100 lần/ngày** [1][2] | Có | Repo đo được trần thực tế ~92–93 |
| `videos.update`, `thumbnails.set` | 50 [1] | chung 10.000 | Có | |

**Kiểm chứng comment "search.list 100 lần/ngày" trong `factory/publish.py`: ĐÚNG.** Trang getting-started
ghi mặc định "100 `search.list` calls, 100 `videos.insert` calls, and 10,000 units" mỗi ngày [2]. Revision
history ngày 01/06/2026: hệ quota "granular", bắt đầu với `videos.insert` và `search.list` [3]. Trước đó
(04/12/2025) chi phí upload đã giảm từ ~1600 xuống ~100 đơn vị [3]. Lưu ý: mọi request, **kể cả request
lỗi**, tốn tối thiểu 1 điểm [2].

### 2.2 Quota theo project, API key, tách biệt

- Cloud Quotas: quota "generally apply at the Google Cloud project level" và dùng ở project này không
  ảnh hưởng project khác [11]. Trong một project, quota dùng chung cho mọi ứng dụng và IP [11].
- Data API: request không có OAuth token phải gửi API key; key "identifies your project and provides
  API access, quota" [7]. Dữ liệu riêng tư bắt buộc OAuth [7].
- **Kết luận kỹ thuật:** đọc dữ liệu công khai bằng API key của một project thứ 4 **không trừ** quota
  của 3 project upload. Các endpoint đọc công khai chạy được chỉ với API key: `search.list` (trừ
  `forMine`/`forContentOwner`) [5], `videos.list` theo `id`/`chart` (trừ `myRating`) [4],
  `channels.list`/`playlistItems.list` với dữ liệu công khai, `videoCategories.list`,
  `i18nRegions.list` (theo nguyên tắc "unauthorized requests only retrieve public data" [2][7]).

### 2.3 Chính sách: tạo thêm project có phải "lách quota"?

Trích nguyên văn (dưới 15 từ mỗi đoạn):

- **Developer Policies III.D.1.c** [8]: "you must create exactly one (1) API Project for that API Client".
  Câu tiếp theo cũng cấm dùng một project cho nhiều API Client.
- **III.D.1.b** [8]: không được dùng cách khác "to mask or misrepresent your API Client's access".
- **ToS §15 "Usage and Quotas"** [9]: "will not, and will not attempt to, exceed or circumvent use or quota restrictions."
- Định nghĩa API Client: "a website or software application ... developed by you" [8][9].

**Đọc chính sách:** quy tắc gắn **mỗi API Client với một project**, không gắn với "mỗi mục đích". Vì vậy:
- Một **công cụ nghiên cứu tách rời** (phần mềm riêng, chỉ đọc, không upload, credentials riêng) có
  project riêng thì **phù hợp** III.D.1.c, thậm chí là điều chính sách đòi hỏi.
- Nếu "project nghiên cứu" thực chất chỉ là module trong cùng factory để có thêm 10.000 đơn vị thì dễ bị
  coi là lách quota theo §15. Ranh giới do YouTube phán xét; **không có văn bản nào cho phép rõ ràng**.
- **Rủi ro sẵn có (cần chủ dự án quyết):** factory hiện là *một* phần mềm dùng *3* project (mỗi kênh
  một project). Đọc sát chữ III.D.1.c thì mô hình này đã lệch. Tôi **không tìm thấy** điều khoản nào
  miễn trừ cho trường hợp "mỗi kênh một project".

**Các ràng buộc khác liên quan demand sensing:**
- **III.E.2.a/b (Data Aggregation)** [8]: "Do not aggregate API Data" (trừ kênh cùng content owner) và
  không dùng API để hiểu "YouTube's usage". Gom kết quả `search.list`/`mostPopular` của *kênh người khác*
  thành bảng xu hướng là vùng xám, rủi ro chính sách thật. Đây là lý do nên ưu tiên nguồn ngoài YouTube.
- **III.E.4.d** [8]: Non-Authorized Data chỉ lưu tạm, tối đa 30 ngày, sau đó xoá hoặc làm mới.
- **III.E.6** [8]: cấm scrape YouTube/Google Applications hoặc dùng dữ liệu đã scrape.

**Quy trình xin thêm quota (III.D.3 [8], [10]):** điền "YouTube API Services - Audit and Quota Extension
Form" (support.google.com/youtube/contact/yt_api_form), qua API Compliance Audit, nêu use case. Quota
được cấp **chỉ dùng cho use case đã duyệt**; đổi use case thì phải nộp audit lại [8]. Đã audit trong
12 tháng thì chỉ cần nộp lại form [10]. Từ 06/2026 có thể xin riêng theo từng bucket [3].

### 2.4 `chart=mostPopular` ở VN

- `regionCode` nhận mã ISO 3166-1 alpha-2 [4]; `videoCategoryId` chỉ dùng cùng `chart`, mặc định `0` [4].
- **Thay đổi quan trọng** [3]: từ 21/07/2025, mostPopular "will feature videos from the Trending Music,
  Movies, and Gaming charts", đi kèm việc YouTube bỏ trang Trending. → Không phản ánh nhu cầu phong
  thuỷ/Phật giáo/hình sự.
- **Chưa kiểm chứng được:** (a) `VN` có trong `i18nRegions.list` không; (b) `videoCategoryId` nào hợp lệ
  cho chart ở VN; (c) chart có chứa Shorts không; (d) tổng số kết quả tối đa qua phân trang. Tài liệu
  [4] và trang resource `videos` không nói (c) và (d). Con số "200 kết quả" hay gặp trên mạng **không có
  trong tài liệu chính thức**. Muốn biết chắc: gọi 1 lần `videoCategories.list?regionCode=VN` và
  `i18nRegions.list` (2 đơn vị) **từ project nghiên cứu, không từ project upload**.

### 2.5 YouTube Analytics API: tín hiệu "first-party"

- Là API riêng (`youtubeanalytics.googleapis.com`, repo đã dùng trong `factory/analytics.py`). Mọi request
  phải có OAuth, scope `yt-analytics.readonly` [15]; API key không đủ.
- Quota: "Each API request ... counts as one unit" [14]; server tự định giá từng truy vấn [16]. Quota này
  thuộc dịch vụ Analytics, **không trừ** 10.000 đơn vị của Data API v3. Con số trần mặc định/ngày của
  Analytics API **không được công bố** trong các trang tài liệu tôi đọc → xem ở trang Quotas của Cloud console.
- **`insightTrafficSourceDetail` khi lọc `insightTrafficSourceType==YT_SEARCH` trả về** "The search term that
  led viewers to the video." [12]. Đây chính là từ khoá người Việt đã gõ để tìm thấy video của kênh.
- Giới hạn báo cáo [13]: bắt buộc filter `insightTrafficSourceType`; metric `views`/`engagedViews`/
  `estimatedMinutesWatched`; **`maxResults` ≤ 25**; **bắt buộc `sort`**; filter tuỳ chọn `video`, `country`,
  `province`... Một số traffic source không hỗ trợ (END_SCREEN, NOTIFICATION...).
- Ngưỡng riêng tư [14]: dữ liệu bị ẩn khi lưu lượng thấp, ngưỡng không công bố. Với kênh Shorts, phần lớn
  view đến từ feed `SHORTS` chứ không từ search, nên danh sách có thể ngắn hoặc rỗng. Cần đo thử.
- Không vướng III.E.2 vì là dữ liệu của chính kênh (Authorized Data). Lưu lâu dài phải tuân III.E.4 [8].

---

## 3. Q2: Nguồn xu hướng miễn phí, an toàn ToS cho Việt Nam

### 3.1 Bảng so sánh

Fit: 0 = vô dụng … 3 = rất hợp.

| Nguồn | Cung cấp gì | Phủ VN / tiếng Việt | Chính thức? | Chi phí / giới hạn | ToS / license | FS | BUD | CL |
|---|---|---|---|---|---|---|---|---|
| **YT Analytics search terms** [12][13] | Từ khoá YT search dẫn tới video **của mình** | Theo khán giả kênh (VN) | API chính thức | Quota Analytics; ≤25 dòng/truy vấn | Dữ liệu kênh mình, OAuth | 3 | 3 | 3 |
| **YouTube Studio → tab Trends** [27] | Top search của khán giả 28 ngày, content gap, search term cho Shorts | Một số insight giới hạn theo nước/ngôn ngữ; **chưa xác nhận tiếng Việt** | UI chính thức, **không API** | Miễn phí, thao tác tay | Không automate (ToS YouTube [26]) | 3 | 3 | 3 |
| **Google Trends "Trending now" RSS** [19][20] | ~10 truy vấn đang nổi, `approx_traffic`, tin liên quan | `geo=VN`, tiêu đề tiếng Việt (đã thử) | Feed lấy từ nút Export→RSS chính thức; định dạng không có tài liệu | Miễn phí; không công bố rate limit | robots.txt không chặn [21]; ghi nguồn Google Trends [23] | 1 | 1 | 2 |
| **Google Trends API (alpha)** [17][18] | Search interest đã scale nhất quán, 5 năm, ngày/tuần/tháng/năm, vùng ISO 3166-2 | Có vùng/tiểu vùng; **chưa rõ có YouTube Search** | Chính thức nhưng **alpha, phải xin** | Chưa công bố | Theo điều khoản alpha | 2* | 2* | 2* |
| **Google Trends Explore (UI)** [24] | So sánh từ khoá, lọc theo property (có YouTube Search) | Có VN | UI chính thức, không API | Thủ công | Automate bị chặn (robots `/explore?` [21]) | 2 | 2 | 2 |
| **pytrends / endpoint nội bộ Trends** | Như Explore | Có | **Không chính thức** | Hay bị 429 | Rủi ro ToS [21][22], **tránh** | n/a | n/a | n/a |
| **YouTube autocomplete** (`suggestqueries`) | Gợi ý tìm kiếm | Có | **Không chính thức** [25] | n/a | Google chặn "unauthorized access" từ 2015 [25]; ToS YouTube cấm automate [26]. **Tránh** | n/a | n/a | n/a |
| **Wikimedia Pageviews** [28][31] | View/ngày theo bài; top 1000 bài/ngày của vi.wikipedia | vi.wikipedia; endpoint top theo nước VN trả 404 khi thử | API chính thức | 200 req/phút với UA hợp lệ [29] | **CC0** [28][32]; UA bắt buộc [30] | 2 | 2 | 2 |
| **GDELT DOC 2.0** [33][34] | Bài báo/timeline theo từ khoá, 3 tháng gần nhất | Tiếng Việt nằm trong 65 ngôn ngữ dịch máy [35] | API chính thức | Miễn phí; 1 request/5 giây [36] | Dùng thương mại được, **phải ghi nguồn + link** [33] | 0 | 1 | 2 |
| **RSS VnExpress / Tuổi Trẻ / Dân Trí** [37][38][40] | Tiêu đề mới theo chuyên mục (có Pháp luật) | Tiếng Việt | RSS chính thức | Miễn phí | **Chỉ cho cá nhân & tổ chức phi lợi nhuận** → kênh kiếm tiền cần xin phép | 0 | 0 | 3 |
| **RSS Thanh Niên** [39] | Như trên (có `thoi-su/phap-luat.rss`) | Tiếng Việt | RSS chính thức | Miễn phí | Dùng lại tin phải ghi "Theo Báo Thanh Niên" | 0 | 0 | 3 |
| **TikTok Research API** [41] | Dữ liệu TikTok | n/a | Chính thức | n/a | **Chỉ học thuật/phi lợi nhuận ở US, EEA, UK, CA, CH...**; loại | n/a | n/a | n/a |
| **TikTok Creative Center** | Hashtag/bài hát/video trending theo nước | **Chưa xác minh VN** (trang render bằng JS) | UI; không tìm thấy API trend công khai | Miễn phí | Chỉ thao tác tay | 2 | 2 | 1 |
| **Google Books Ngram** [43] | Tần suất từ trong sách | **Không có tiếng Việt** | | | | 0 | 0 | 0 |

\* Chỉ khi được duyệt alpha. Dữ liệu chỉ tới "just 2 days ago" [18], không phải thời gian thực.

### 3.2 Ghi chú từng nguồn

**YouTube Analytics search terms.** Đây là tín hiệu tốt nhất vì đến từ chính khán giả: từ khoá họ gõ
*và* đã bấm vào video của kênh. Truy vấn mẫu cho mỗi kênh, 28 ngày gần nhất:
`dimensions=insightTrafficSourceDetail&filters=insightTrafficSourceType==YT_SEARCH&metrics=views&sort=-views&maxResults=25` [13].
Có thể lọc thêm `country==VN` [13]. Hạn chế: chỉ thấy cầu *đã được kênh đáp ứng*, không thấy khoảng trống.

**YouTube Studio Trends tab.** Hiển thị "Content gaps" (người xem tìm mà YouTube thiếu kết quả tốt) và search
term cho Shorts liên quan khán giả [27]. Đúng thứ cần nhưng **không có API**. Đề xuất: mỗi tuần một người
mở tay, chép 10–20 cụm từ vào file seed. Không tự động hoá bằng trình duyệt vì ToS YouTube cấm truy cập tự
động trừ khi có phép bằng văn bản [26].

**Google Trends.**
- *Trending now RSS*: tôi tải thử `https://trends.google.com/trending/rss?geo=VN` lúc 05/10/2026, HTTP 200,
  10 `<item>`, có `ht:approx_traffic` và tin liên quan (ví dụ "dự báo thời tiết", 2000+) [20]. Trang help xác
  nhận có export RSS và dữ liệu làm mới trung bình 10 phút/lần [19]. robots.txt của trends.google.com chỉ
  chặn `/explore?` và `/trends/explore?` [21]. Google ToS cấm truy cập tự động *khi vi phạm* chỉ dẫn máy đọc
  như robots.txt [22]. Đọc RSS vài lần/ngày là hợp lệ. Ghi nguồn theo hướng dẫn trích dẫn [23]. Hạn chế:
  chỉ là Web Search, rất chung (thời tiết, bóng đá), ít khi trúng ngách. Nên dùng như **bộ lọc "sự kiện
  nóng"** (vụ án lớn, ngày lễ, hiện tượng thiên văn), không dùng làm nguồn chủ đề chính.
- *Trends API alpha*: công bố 24/07/2025, chỉ "a very limited number of testers" [18]. Trang chính thức tới
  nay vẫn ghi đang nhận đơn alpha [17]. Không tài liệu nào nói rõ có property YouTube Search. Đáng nộp đơn
  (miễn phí), nhưng không dựa vào nó.
- *Explore UI*: Trends là mẫu ngẫu nhiên các lượt tìm trên Google và YouTube [24], lọc được theo property.
  Hữu ích khi so 2–5 ứng viên chủ đề bằng tay. Không automate.

**YouTube autocomplete.** Không có tài liệu API. Blog chính thức của Google (2015) gọi đây là "non-official,
non-published API" và chặn truy cập trái phép từ 10/08/2015 [25]. `suggestqueries.google.com/robots.txt` trả
404 khi tôi thử [44], nhưng ToS YouTube cấm truy cập tự động [26]. **Không dùng.**

**Wikimedia Pageviews.** API chính thức, dữ liệu CC0 [28][32]. Bắt buộc User-Agent dạng
`<client>/<version> (<contact>)` [28][30]; client không định danh bị giới hạn 10 req/phút, bot có UA hợp lệ
200 req/phút [29]. Dữ liệu có từ 01/07/2015 [31]. Tôi đã thử: top vi.wikipedia ngày 04/10 có sẵn vào sáng
05/10. Top list **nhiễu** (Trang Chính, trang Đặc biệt, bài nghi do bot), nên phải lọc theo `agent=user` và
danh sách đen. Cách dùng hợp lý: **theo dõi danh sách bài cố định** (12 con giáp, Kinh Dịch, các Phật/Bồ
tát, ngày lễ Phật giáo, tên vụ án/nhân vật hình sự) và bắt bài có view tăng đột biến. Lượng view nhỏ (bài
"Phong thủy" chỉ ~20–35 view/ngày), nên tín hiệu yếu với FS. CL hưởng lợi nhất (tên vụ án mới nổi).
Endpoint `top-per-country/VN` trả 404 ở mọi ngày tôi thử. Nguyên nhân chưa rõ.

**GDELT.** Miễn phí cho cả mục đích thương mại, kèm ghi nguồn và link [33]. DOC 2.0 tìm trong 3 tháng gần
nhất [34]; tiếng Việt có trong danh sách dịch máy [35]. Khi gọi thử, tôi chỉ nhận thông báo yêu cầu giãn
cách 5 giây/request [36] nên **chưa xác nhận được chất lượng kết quả tiếng Việt**. Hợp với CL (khối lượng
tin về một vụ án theo thời gian). Gần như không giúp FS/BUD.

**RSS báo Việt.** Cả bốn báo đều có RSS chuyên mục Pháp luật (`vnexpress.net/rss/phap-luat.rss`,
`tuoitre.vn/phap-luat.rss`, `thanhnien.vn/rss/thoi-su/phap-luat.rss`, `dantri.com.vn/rss/phap-luat.rss`)
[37]–[40]. **Điều khoản:** VnExpress, Tuổi Trẻ, Dân Trí ghi RSS "miễn phí cho các cá nhân và các tổ chức phi
lợi nhuận" và có quyền yêu cầu ngừng bất cứ lúc nào [37][38][40]. Dân Trí còn ghi cấm sao chép nếu không
được chấp thuận [40]. Factory là hoạt động kiếm tiền nên **không thuộc nhóm được cấp phép**, kể cả khi chỉ
đọc tiêu đề làm tín hiệu nội bộ. Thanh Niên không có giới hạn phi lợi nhuận trong văn bản, chỉ yêu cầu ghi
nguồn khi dùng lại tin [39]. → Nếu cần, dùng **Thanh Niên** (chỉ làm tín hiệu, không đăng lại nội dung),
còn ba báo kia thì email xin phép trước.

**TikTok.** Research API yêu cầu tổ chức học thuật/phi lợi nhuận, độc lập với lợi ích thương mại, ở các vùng
được liệt kê [41]. Factory không đủ điều kiện. Creative Center: không xác minh được qua nguồn chính thức
rằng có chọn VN (trang render bằng JS). Các bài thứ cấp nói có chọn theo nước (SECONDARY). Chỉ dùng tay.

**Reddit / Wikidata.** Reddit gần như không có cộng đồng tiếng Việt cho 3 ngách nên bỏ qua. Wikidata là kho
tri thức, không phải tín hiệu cầu. Có thể dùng để *chuẩn hoá tên* (con giáp, Phật/Bồ tát) cho danh sách
theo dõi Wikimedia, nhưng không cần trong bản tối thiểu.

---

## 4. Đề xuất cho repo (bản tối thiểu)

Nguyên tắc: **0 đơn vị Data API trên 3 project upload**, không automate thứ không có API/feed.

| # | Nguồn | Cách chạy | Tần suất | Chi phí quota |
|---|---|---|---|---|
| 1 | YT Analytics `insightTrafficSourceDetail` + `YT_SEARCH` | Mở rộng `factory/analytics.py` (đã có OAuth Analytics cho từng kênh) | 1 truy vấn/kênh/ngày (28 ngày trượt), có thể thêm 1 truy vấn `country==VN` | 3–6 request Analytics/ngày; **0 Data API** |
| 2 | Google Trends RSS `geo=VN` | `urllib` GET, ghi vào sqlite, gắn "Data source: Google Trends" | 4–6 lần/ngày | 0 |
| 3 | Wikimedia Pageviews (vi.wikipedia) | Danh sách theo dõi ~100–300 bài theo ngách + 1 call top/ngày; UA có email liên hệ | 1 lần/ngày | 0 (≤300 req, dưới 200 req/phút nếu giãn nhịp) |
| 4 | YouTube Studio Trends tab | Người làm tay, chép vào `seeds/*.txt` | 1 lần/tuần/kênh | 0 |
| 5 (tuỳ chọn, CL) | GDELT DOC 2.0 hoặc RSS Thanh Niên Pháp luật | 1 request/5 s; ghi nguồn GDELT/Thanh Niên | 1–2 lần/ngày | 0 |

**Không đưa vào:** `search.list`/`mostPopular` từ project upload, autocomplete, pytrends, scrape TikTok/YouTube,
RSS VnExpress/Tuổi Trẻ/Dân Trí (khi chưa có phép).

**Nếu chủ dự án muốn kiểm tra mức cạnh tranh bằng `search.list`** (ví dụ "chủ đề X đã có bao nhiêu video tuần
này"), thì làm trong **project nghiên cứu riêng, API key, là một API Client tách biệt**. Mức hợp lý: ≤30 lần
`search.list`/ngày (bucket 100) + ≤10 đơn vị `videos.list` = khoảng 40 lượt/ngày, 0 trên project upload. Chỉ dùng
để ra quyết định nội bộ cho từng chủ đề, **không lưu quá 30 ngày** (III.E.4.d) và không gom thành bảng
thống kê xu hướng YouTube (III.E.2.b) [8].

---

## 5. Câu hỏi mở / cần chủ dự án quyết

1. **Mô hình 3 project cho 1 factory.** III.D.1.c [8] yêu cầu đúng một project cho mỗi API Client. Factory hiện
   có 3 project cho cùng một phần mềm. Có chấp nhận rủi ro này không, có hợp nhất về một project rồi xin
   tăng quota qua audit [10] không? Việc này **quan trọng hơn** câu hỏi project nghiên cứu.
2. **Có tạo project nghiên cứu thứ 4 không?** Chỉ nên tạo nếu công cụ nghiên cứu là phần mềm/credentials
   tách biệt, mục đích khác (chỉ đọc). Nếu chỉ cần nguồn ở mục 4 (#1–#5) thì **không cần** project nào mới.
3. **Nộp đơn Google Trends API alpha?** Miễn phí, không ràng buộc, nhưng phải mô tả use case và cam kết phản hồi [17].
4. **Email xin phép VnExpress/Tuổi Trẻ/Dân Trí** để dùng RSS cho mục đích thương mại (chỉ đọc tiêu đề)?
5. **Ai làm phần tay hằng tuần** (YouTube Studio Trends tab, Trends Explore, Creative Center)?
6. **Cần đo thực tế:** search terms của các kênh Shorts có đủ dữ liệu vượt ngưỡng riêng tư không [14]. Chạy thử
   1 truy vấn/kênh trước khi thiết kế bảng.
7. **Chưa kiểm chứng:** VN có trong `i18nRegions`; category hợp lệ cho mostPopular ở VN; mostPopular có Shorts
   không; trần tổng kết quả của chart; trần ngày mặc định của Analytics API; Creative Center có VN; nguyên nhân
   `top-per-country/VN` 404; chất lượng kết quả GDELT tiếng Việt.

---

## 6. Nguồn (truy cập 05/10/2026)

1. YouTube Data API – Quota Calculator (cập nhật 15/09/2026). https://developers.google.com/youtube/v3/determine_quota_cost
2. YouTube Data API – Getting started, mục Quota usage (cập nhật 14/09/2026). https://developers.google.com/youtube/v3/getting-started
3. YouTube Data API – Revision history (mục 10/07/2025, 04/12/2025, 01/06/2026). https://developers.google.com/youtube/v3/revision_history
4. YouTube Data API – Videos: list. https://developers.google.com/youtube/v3/docs/videos/list
5. YouTube Data API – Search: list. https://developers.google.com/youtube/v3/docs/search/list
6. YouTube Data API – VideoCategories: list. https://developers.google.com/youtube/v3/docs/videoCategories/list
7. YouTube – Obtaining authorization credentials. https://developers.google.com/youtube/registering_an_application
8. YouTube API Services – Developer Policies (cập nhật 14/09/2026), các mục III.D.1, III.D.3, III.E.2, III.E.4, III.E.6. https://developers.google.com/youtube/terms/developer-policies
9. YouTube API Services – Terms of Service (§15 Usage and Quotas). https://developers.google.com/youtube/terms/api-services-terms-of-service
10. YouTube Data API – Quota and Compliance Audits (cập nhật 14/09/2026). https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits
11. Google Cloud – Cloud Quotas overview (cập nhật 30/09/2026). https://docs.cloud.google.com/docs/quotas/overview
12. YouTube Analytics API – Dimensions (insightTrafficSourceType/Detail). https://developers.google.com/youtube/analytics/dimensions
13. YouTube Analytics API – Channel reports (Traffic source detail). https://developers.google.com/youtube/analytics/channel_reports
14. YouTube Analytics API – Data model (quota, ngưỡng dữ liệu; cập nhật 14/09/2026). https://developers.google.com/youtube/analytics/data_model
15. YouTube Analytics API – reports.query. https://developers.google.com/youtube/analytics/reference/reports/query
16. YouTube Analytics and Reporting APIs – overview. https://developers.google.com/youtube/reporting
17. Google Search Central – Get early access to the Google Trends API alpha. https://developers.google.com/search/apis/trends
18. Google Search Central Blog – Introducing the Google Trends API (alpha), 24/07/2025. https://developers.google.com/search/blog/2025/07/trends-api
19. Trends Help – Explore the searches that are trending now. https://support.google.com/trends/answer/3076011
20. Google Trends – Trending now RSS, geo=VN (tải thử trực tiếp, HTTP 200, 10 item). https://trends.google.com/trending/rss?geo=VN
21. trends.google.com/robots.txt (đọc trực tiếp). https://trends.google.com/robots.txt
22. Google Terms of Service, mục "Don't abuse our services" (hiệu lực 30/07/2026). https://policies.google.com/terms
23. Trends Help – Citing Google Trends data. https://support.google.com/trends/answer/4365538
24. Google Search Central – Get started with Google Trends (cập nhật 10/12/2025). https://developers.google.com/search/docs/monitor-debug/trends-start
25. Google Search Central Blog – Update on the Autocomplete API, 24/07/2015. https://developers.google.com/search/blog/2015/07/update-on-autocomplete-api
26. YouTube Terms of Service (mục Permissions and Restrictions). https://www.youtube.com/t/terms
27. YouTube Help – Explore trends on YouTube (Trends tab trong YouTube Studio). https://support.google.com/youtube/answer/11962757
28. Wikimedia Analytics API – Access policy (CC0, User-Agent). https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/access-policy.html
29. MediaWiki – Wikimedia APIs/Rate limits (sửa 03/06/2026). https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits
30. Wikimedia Foundation User-Agent Policy (sửa 27/03/2026). https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
31. Wikimedia Analytics API – Page views reference. https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html
32. Wikimedia dumps – Pageviews readme (CC0). https://dumps.wikimedia.org/other/pageviews/readme.html
33. GDELT Project – About (điều khoản sử dụng). https://www.gdeltproject.org/about.html
34. GDELT Blog – GDELT DOC 2.0 API Debuts. https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
35. GDELT Blog – GDELT Translingual: Translating the Planet (danh sách ngôn ngữ). https://blog.gdeltproject.org/gdelt-translingual-translating-the-planet/
36. GDELT DOC API – phản hồi thực tế khi gọi thử (thông báo giãn cách 5 giây). https://api.gdeltproject.org/api/v2/doc/doc
37. VnExpress – trang RSS và điều khoản sử dụng. https://vnexpress.net/rss
38. Tuổi Trẻ – trang RSS và điều khoản sử dụng. https://tuoitre.vn/rss.htm
39. Thanh Niên – trang RSS và điều kiện sử dụng. https://thanhnien.vn/rss.html
40. Dân Trí – trang RSS và điều khoản sử dụng. https://dantri.com.vn/rss.htm
41. TikTok for Developers – Research API (điều kiện). https://developers.tiktok.com/products/research-api/
42. TikTok Creative Center (không đọc được nội dung, render bằng JS). https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en
43. Google Books Ngram Viewer – Info (danh sách corpus). https://books.google.com/ngrams/info
44. suggestqueries.google.com/robots.txt (thử trực tiếp: 404). https://suggestqueries.google.com/robots.txt
