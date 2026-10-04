# 1 triệu view cho kênh CL: cần gì và cái gì chặn (nghiên cứu ngày 04/10/2026)

Câu hỏi: với kênh "Into The Killer's Mind" (CL), Long 16:9 dài 25–35 phút và Shorts 45–60s
(motion graphic + ảnh PD/CC + B-roll Pexels + giọng TTS tiếng Việt), **cái gì quyết định một
video chạm ~1.000.000 view, và cái gì chặn nó?** Chỉ xét những thứ mình kiểm soát được.

Quy ước: mỗi khẳng định có số nguồn `[n]` ở cuối file. Nguồn **chính thức** là YouTube Help,
YouTube Blog, bài báo của Google. Nguồn nào chỉ là báo/blog/creator thì ghi **(SECONDARY)**.
Trích dẫn nguyên văn luôn dưới 15 từ.

---

## TL;DR

- **Hệ thống không "đẩy" video, nó "kéo" video cho từng người xem.** Thứ được tối ưu là
  *watch time dự kiến trên mỗi impression* cộng với *mức hài lòng* (khảo sát, like, "Không quan
  tâm"). CTR một mình không đủ, vì Google đã viết rằng xếp hạng theo CTR đẩy clickbait lên [1][2][3].
- **1 triệu view của Long gần như chắc chắn đến từ Browse + Suggested, không phải Search.**
  Ví dụ đã kiểm chứng: kênh *Giải Mã Tội Ác* chỉ có 38,1K sub nhưng có video Pablo Escobar dài
  25 phút đạt ~977K view. Chủ đề lớn + đóng gói tốt vẫn vượt quy mô kênh [M].
- **Trần thị trường đủ rộng.** YouTube tiếp cận ~62,1 triệu người ở Việt Nam (10/2025) [12].
  Ngách băng đảng / sát nhân tiếng Việt đã có nhiều video 0,6–1,2 triệu view, dài 20–32 phút [M].
- **Rủi ro lớn nhất là chính sách, không phải thuật toán.** "Inauthentic content" (đổi tên từ
  repetitious content ngày 15/07/2025) và Spam policy mô tả **gần như đúng** mô hình "cùng nhạc
  nền + hình AI lặp lại + đọc script AI" [4][6]. Kênh dùng TTS và AI **vẫn được** kiếm tiền nếu
  mỗi video có câu chuyện, góc nhìn và giá trị riêng [5].
- **Nhãn "altered or synthetic" gần như không áp vào mình**, trừ khi tạo cảnh/người thật giả
  như thật. Ví dụ: ảnh AI cho thấy một người thật đang bị bắt thì **bắt buộc** khai báo [7].
- **Shorts được chấm bằng: tỷ lệ chọn xem (không vuốt qua), AVD, AVP, like, khảo sát** [8].
  Ngày 01/10/2026 YouTube cập nhật để ưu tiên Shorts "original". Mốc này **trùng thời điểm**
  Shorts CL rơi về ~0. Đây là giả thuyết thứ hai bên cạnh vụ upload dồn ngày 30/09 [14][15].
- **Không có nguồn chính thức nào nói "đăng nhiều làm hại kênh".** YouTube chỉ nói không có
  tần suất tối thiểu [8]. Nhưng "flood" nội dung lặp lại bằng công cụ tự động thì vi phạm spam [6].
- **Mở rộng = nhiều video tốt hơn trên một kênh**, không phải nhiều kênh. Chính sách nói thẳng
  về "coordinated networks of channels" [6], và lách chế tài bằng kênh khác thì bị cấm [9][4].

---

## 1. Thuật toán phân phối quyết định thế nào

**Hai tầng: chọn ứng viên rồi xếp hạng.** Bài báo của Google (Covington và cộng sự, 2016) mô tả
quy trình: từ kho hàng triệu video, chọn ra vài trăm ứng viên, rồi xếp hạng chúng. Mục tiêu xếp
hạng là *"a simple function of expected watch time per impression"*. Bài báo cũng viết: xếp theo
CTR *"often promotes deceptive videos"* mà người xem không xem hết [1]. Cũng bài này cho biết
người dùng *"prefer fresh content, though not at the expense of relevance"* [1]. Video mới được
ưu tiên, nhưng chỉ khi thật sự hợp với người xem.

**Hài lòng, không chỉ là thời lượng xem.** Từ 2012 YouTube thêm watch time. Sau đó họ thêm
khảo sát để đo *"valued watchtime"*, cùng các tín hiệu share, like, dislike [2]. Trang Help hiện
nay liệt kê các tín hiệu: lịch sử xem, lịch sử tìm kiếm, kênh đã đăng ký, like/dislike, "Không
quan tâm", "Không đề xuất kênh này" và khảo sát hài lòng [3].

**CTR là chỉ số tương đối.** Theo YouTube, một nửa số kênh có CTR trong khoảng 2–10%. Khi video
lan ra trang chủ, tức ra khỏi nhóm khán giả lõi, CTR **tự nhiên giảm** [10]. Vì vậy CTR giảm trong
lúc impressions tăng vọt là dấu hiệu đang được mở rộng, không phải dấu hiệu hỏng.

**"Pull, not push" và việc thử trên tập nhỏ.** Todd Beaupré (Growth & Discovery) nói hệ thống
"kéo" video cho từng người mở trang chủ chứ không "đẩy" video ra hàng loạt. Ông cũng nói video cũ
có thể sống lại sau nhiều tháng khi chủ đề nóng trở lại **(SECONDARY, phỏng vấn trên Creator
Insider, trích qua SEJ)** [13]. Còn mô hình "thử video trên một nhóm nhỏ rồi nới dần" thì YouTube
**chưa mô tả chính thức** ở trang Help nào mình tìm được. Mô hình này chỉ khớp với số liệu
Shorts của mình: phần lớn video dừng ở ~1.000 view. Hãy coi nó là giả thuyết làm việc.

**Mỗi video được đánh giá riêng.** Trang "Good to know about recommendations" cho biết một video
kém **không** kéo cả kênh xuống, và thử format mới không bị phạt. Hệ thống **không** xét trạng
thái kiếm tiền khi đề xuất. Kênh mới thì cần một "critical mass" video tốt [11]. *(Diễn giải, không
trích nguyên văn.)*

**Shorts khác Long.** YouTube xếp hạng Shorts dựa trên *"% of viewers who chose to view, avg. view
duration and avg. % viewed"*. Sau đó họ xem người xem có thích hay không qua like và khảo sát
sau khi xem [8]. Analytics có chỉ số "Viewed vs. swiped away" [16]. Tóm lại, Shorts sống nhờ **giây
đầu tiên giữ được ngón tay người xem**, còn Long sống nhờ **tổng phút xem / impression**.

**Đăng nhiều hay đăng dồn có hại không?**
- Chính thức: *"no minimum posting cadence required"* [8].
- Spam policy cấm dùng công cụ tự động hoặc AI để *"churn out high volumes of similar content"*
  và *"flood our platform with repetitive content"* [6].
- YouTube không công bố ngưỡng số lượng cụ thể. Việc CL đăng 61 video trong một ngày (53 video
  trong 47 phút) **khớp với kiểu hành vi** mà spam classifier nhắm tới. Nhưng không có tài liệu
  nào xác nhận cơ chế phạt "burst". Đây là suy luận từ dữ liệu của mình.

**Cập nhật Shorts ngày 01/10/2026.** TeamYouTube (Help Community) và Rene Ritchie (Creator Insider)
thông báo hệ thống đề xuất Shorts sẽ ưu tiên nội dung original. Kênh *"primarily aggregating"*
clip của người khác sẽ *"likely see less distribution"*. Theo tường thuật, voice-over mô tả hình
ảnh và chỉnh sửa hàng loạt theo template **không** được tính là original. Đổi hướng sang nội dung
gốc thì reach "sẽ được đánh giá lại", nhưng không có mốc thời gian
**(SECONDARY: ppc.land, SocialMediaToday. Không fetch được bài gốc)** [14][15]. CL không re-upload
clip của ai. Nhưng CL dùng ảnh tư liệu + B-roll stock + template giống nhau trên hàng trăm video.
Nếu classifier gộp nhầm CL vào nhóm này thì triệu chứng sẽ đúng như mình đang thấy.

## 2. Rủi ro chính sách giới hạn việc mở rộng

**Inauthentic content** (đổi tên ngày 15/07/2025) [4]:
- Nội dung không được *"mass-produced, generic, repetitive, or manipulative"*.
- Không kiếm tiền được: *"AI-generated content made with generic or unoriginal templates"* (tạo
  cảm giác sản xuất hàng loạt).
- Không kiếm tiền được: *"Image slideshows, templated storylines, or scrolling text with minimal
  narrative"*.
- Được phép: series có cấu trúc giống nhau nếu mỗi tập có *"a distinct storyline, focus, or concept"*.
- Khi xét duyệt, YouTube xem cả kênh, đặc biệt là *"Main theme, Most viewed videos, Newest
  videos"* [4][17].

**Reused content** [4]:
- Tái sử dụng nội dung mà không có *"significant original commentary, substantive modifications"*.
- Một ví dụ đáng chú ý với mô hình TTS: video *"exclusively features readings of other materials"*
  mà mình không viết, ví dụ đọc lại text từ website. Nếu script chỉ là Wikipedia được diễn đạt
  lại rồi đọc bằng TTS thì đó là vùng xám.

**Lời giải thích của YouTube (07/2025).** Đây là *"minor update"*. Ví dụ bị nhắm tới là kênh
upload *"slideshows that all have the same narration"* hoặc truyện chỉ khác nhau bề ngoài.
YouTube cũng nói kênh dùng AI *"remain eligible for monetization"*
**(SECONDARY: SocialMediaToday trích Rene Ritchie / TeamYouTube)** [5].

**Spam policy.** Ví dụ chính thức trên trang Spam policy đúng là chân dung rủi ro của mình:
kênh dùng *"the exact same background music and repetitive AI generated imagery"* trên nhiều
video, mỗi video đọc một script do AI viết [6]. Đây là **vi phạm Community Guidelines**, không
chỉ là chuyện mất kiếm tiền.

**Nhãn altered/synthetic** [7]:
- Phải khai báo khi nội dung làm người thật trông như đang nói hoặc làm điều họ không làm, hoặc
  dựng cảnh thật chưa từng xảy ra. Ví dụ trên trang: *"Making it look like a real person has been
  arrested"*.
- Không phải khai báo: AI hỗ trợ sản xuất (outline, script, thumbnail, infographic), animation
  rõ ràng là không thật, chỉnh màu, upscale.
- Khai báo **không** làm giảm reach hay khả năng kiếm tiền. Cố tình không khai báo nhiều lần có
  thể bị gắn nhãn thủ công, gỡ video hoặc bị loại khỏi YPP.
- Trang này không có ví dụ riêng cho giọng TTS đọc dữ kiện. Giọng TTS chung chung, không giả
  giọng người thật, thì không thuộc nhóm "realistic depiction".

**Kiếm tiền với true crime.** Theo Advertiser-friendly guidelines, bạo lực trong bối cảnh tài liệu
hoặc giáo dục có thể được quảng cáo đầy đủ. Ảnh xác chết có thương tích rõ thì bị hạn chế quảng
cáo. Thumbnail hoặc title có bạo lực đồ họa sẽ kéo xuống limited/no ads dù nội dung bên trong ổn
[18]. Điều này giới hạn doanh thu, không giới hạn view. Nhưng title quá sốc (ví dụ "Điều 142…") có
thể bị giảm phân phối hoặc giới hạn độ tuổi.

## 3. Trần thị trường

- **Quy mô:** YouTube tiếp cận khoảng **62,1 triệu** người dùng ở Việt Nam (10/2025), tức
  61,0% dân số và 72,5% người dùng internet. Việt Nam có 102 triệu dân và 85,6 triệu người dùng
  internet. Số liệu do DataReportal tổng hợp từ công cụ quảng cáo của Google [12]. 1 triệu view
  chỉ cần ~1,6% số người này xem một lần (chưa tính kiều bào). Trần thị trường không phải là
  điểm nghẽn.
- **Bằng chứng trong ngách.** Đo bằng metadata YouTube (yt-dlp, không tải video) ngày 04/10/2026.
  Đây là view trọn đời, video đã đăng 1–3 năm [M]:

| Kênh (sub) | Video | Dài | View | Đăng |
|---|---|---|---|---|
| BATTLECRY - KHÁM PHÁ (417K) | Yakuza (twrco9E5NPE) | 20:11 | 1.191.438 | 12/2022 |
| Tra Án (448K) | Ted Bundy (gZV9tWFgcMs) | 31:41 | 1.154.217 | 10/2023 |
| Học viện Bò và Gấu (754K) | Mafia (-t3eR8TQT6g) | 13:03 | 1.047.297 | 07/2025 |
| Giải Mã Tội Ác (38,1K) | Pablo Escobar (loG-DIwS9KQ) | 24:59 | 976.848 | 07/2024 |
| CD Media - Khám Phá (673K) | Hội Tam Hoàng (kA3DMjraQZw) | 30:01 | 667.265 | 05/2024 |
| VỤ ÁN CÓ THẬT (431K) | Trùm mafia Trung Quốc (17LAt2uqOBM) | 30:25 | 571.696 | 02/2025 |
| Spiderum (Baram01) | Hội Tam Hoàng (V9b8vdqGkTo) | 23:37 | 325.579 | – |

  Ngoài bảng: các tư liệu vụ Năm Cam của báo chí đạt 1–3,4 triệu view (PLO, 1:38:01, 3,4 triệu),
  nhưng đó là kênh báo có footage độc quyền. **Chưa kiểm chứng** các kênh trong bảng có dùng TTS
  hay faceless không. Shorts tiếng Việt cùng ngách cũng chưa kiểm chứng.
- **Kết luận:** chủ đề Yakuza, Mafia, Escobar, Ted Bundy, Tam Hoàng **đã chứng minh** đạt
  0,6–1,2 triệu view với độ dài 20–32 phút. Muốn đạt 1 triệu thường cần thời gian (nhiều tháng),
  không phải 48 giờ đầu.

## 4. Đóng gói: thumbnail, title, 30 giây đầu, chapter, end screen

- **Test & Compare** [19]:
  - Thử tối đa 3 phương án: chỉ title, chỉ thumbnail, hoặc cả hai.
  - Phương án **có watch time cao nhất** thắng, không phải phương án có CTR cao nhất.
  - Chỉ dùng trên desktop Studio. **Không áp dụng cho Shorts.** Thường có kết quả trong vòng
    2 tuần.
  - Kết quả có thể là thắng, hòa hoặc inconclusive. Nếu inconclusive thì giữ phương án đầu.
- **30 giây đầu.** Báo cáo retention có mục Intro: % người còn xem sau 30 giây. YouTube gợi ý
  đưa đoạn hấp dẫn lên sớm và làm thumbnail/title khớp với nội dung. Key moments (dip, spike,
  độ dốc) chỉ hiện với video ≥60s và ≥100 view [20]. Đi với RETENTION.md: cold open phải trả
  đúng lời hứa của thumbnail.
- **Chapters** [21]: mốc đầu tiên phải là 00:00, ít nhất 3 mốc, mỗi chương ≥10 giây.
  Chương có thể xuất hiện ở Search, nên tên chương nên chứa từ khóa người Việt hay tìm.
- **End screen** [22]: xuất hiện trong 5–20 giây cuối, video phải ≥25 giây, tối đa 4 phần tử
  với video 16:9. Nên trỏ sang video Long kế tiếp trong playlist "Đế Chế Thế Giới Ngầm". Phiên
  xem kéo dài sang video tiếp theo thì tổng watch time của phiên tăng.

## 5. "Mở rộng" nghĩa là gì: một kênh hay nhiều kênh

- **Một kênh, nhiều video tốt.** Mỗi video được đánh giá riêng [11], nên một hit tốt vẫn kéo view
  cho cả catalog qua Suggested. Beaupré khuyên đi **sâu** vào một nhóm khán giả trước khi đi rộng.
  Ông cũng nhấn mạnh cần đủ "critical mass" nội dung trong một ngôn ngữ **(SECONDARY)** [13].
- **Nhiều kênh.** Spam policy áp dụng cho cả *"coordinated networks of channels"* [6].
  - Nếu một kênh bị chấm dứt, chủ kênh *"prohibited from using, possessing, or creating"* kênh
    khác. Lệnh cấm áp dụng cho mọi kênh hiện có [9].
  - Nếu một kênh bị tắt kiếm tiền, không được dùng kênh khác để lách [4].
  - Nhiều kênh cùng template, cùng giọng, cùng nhạc là **rủi ro dây chuyền**: một kênh dính spam
    có thể kéo theo cả mạng.
- **Điều kiện YPP** [17]: 1.000 sub và 4.000 giờ xem trong 12 tháng, hoặc 1.000 sub và 10 triệu
  view Shorts trong 90 ngày. YouTube xét **cả kênh** (người duyệt + hệ thống tự động), mất khoảng
  1 tháng.

---

## Hàm ý cho hệ thống của mình

1. **Long là đường tới 1 triệu, Shorts là đường tới sub.** Lấy watch time / impression làm chỉ
   số trung tâm. Một video 30 phút có AVP 35% cho ~10 phút/view. 1 triệu view ≈ 175K giờ xem.
   Với CTR 5% thì cần ~20 triệu impression, và lượng impression đó chỉ Browse/Suggested mới có.
2. **Chọn chủ đề "đã chứng minh".** Chọn chủ đề đã có video tiếng Việt ≥500K view (bảng mục 3).
   Làm **tốt hơn** chứ không làm **khác đi**: sâu hơn, có cung chuyện, có dữ kiện lạ.
3. **Chống "inauthentic" ngay trong engine** (đây là điểm nghẽn thật):
   - mỗi Long có một "câu hỏi trung tâm" và cung chuyện riêng;
   - script phải có phân tích, so sánh và kết luận của mình, không chỉ diễn đạt lại Wikipedia;
   - xoay nhiều track nhạc nền, không dùng một track cho mọi video;
   - thay đổi bố cục HUD, màu và nhịp theo từng chủ đề;
   - **không** dùng ảnh AI dựng người thật hay cảnh thật. Nếu buộc phải dùng thì khai báo.
4. **Shorts:**
   - không bao giờ upload dồn. Drip 2–3 video/ngày như tuần thử 05–11/10;
   - đo **Viewed vs swiped**, AVP, sub sau xem, không chỉ đo view;
   - bỏ hoặc làm lại các format AVP thấp (Vụ án 49%, Điều luật 43%), dồn sức vào format >90%;
   - ghi nhận cập nhật "original Shorts" ngày 01/10/2026 là **nguyên nhân cạnh tranh** với giả
     thuyết burst khi đọc kết quả tuần thử.
5. **Mỗi Long phải có:**
   - 2–3 phương án thumbnail/title để chạy Test & Compare;
   - chapter có từ khóa;
   - end screen trỏ sang Long kế tiếp;
   - cold open khớp thumbnail;
   - kiểm tra Intro (30 giây) trong 48 giờ đầu.
6. **Title và thumbnail không dùng từ ngữ hoặc hình ảnh bạo lực đồ họa** (giữ quảng cáo đầy đủ,
   tránh giới hạn độ tuổi). Sự rùng rợn để trong nội dung.
7. **Một kênh CL mạnh hơn nhiều kênh nhân bản.** Nếu mở thêm kênh thì phải khác ngôn ngữ hoặc
   ngách, khác hình thức, không dùng chung template, nhạc và giọng.

---

## Nguồn (truy cập 04/10/2026)

1. Covington, Adams, Sargin, *Deep Neural Networks for YouTube Recommendations*, RecSys 2016. https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/ (PDF: https://cseweb.ucsd.edu/classes/fa17/cse291-b/reading/p191-covington.pdf)
2. Cristos Goodrow, *On YouTube's recommendation system*, YouTube Official Blog, 15/09/2021. https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/
3. YouTube Help, *How YouTube recommendations work*. https://support.google.com/youtube/answer/16089387 ; How YouTube Works, Recommendations. https://www.youtube.com/howyoutubeworks/product-features/recommendations/
4. YouTube Help, *YouTube channel monetization policies* (inauthentic & reused content, cập nhật 15/07/2025). https://support.google.com/youtube/answer/1311392
5. (SECONDARY) Social Media Today, *YouTube Clarifies Changes to Monetization Rules Around Inauthentic Content*. https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/
6. YouTube Help, *Spam policy* (Automated or synthetic mass-production). https://support.google.com/youtube/answer/2801973
7. YouTube Help, *Disclosing use of altered or synthetic content*. https://support.google.com/youtube/answer/14328491
8. YouTube Help, *Search & discovery tips – Shorts*. https://support.google.com/youtube/answer/11914225?co=YOUTUBE._YTVideoType%3Dshorts
9. YouTube Help, *Channel or account terminations*. https://support.google.com/youtube/answer/2802168
10. YouTube Help, *Impressions & click-through rate*. https://support.google.com/youtube/answer/7628154
11. YouTube Help, *Good to know about recommendations*. https://support.google.com/youtube/answer/16559651
12. DataReportal, *Digital 2026: Vietnam* (số liệu ad reach Google, 10/2025). https://datareportal.com/reports/digital-2026-vietnam
13. (SECONDARY) Search Engine Journal, *How YouTube's Recommendation System Works In 2025* (phỏng vấn Todd Beaupré – Rene Ritchie). https://www.searchenginejournal.com/how-youtubes-recommendation-system-works-in-2025/538379/
14. (SECONDARY) PPC Land, *Re-uploaded Shorts lose reach as YouTube favours original clips* (01/10/2026). https://ppc.land/re-uploaded-shorts-lose-reach-as-youtube-favours-original-clips/
15. (SECONDARY) Social Media Today, *YouTube updates Shorts algorithm to put more focus on original content*. https://www.socialmediatoday.com/news/youtube-updates-shorts-algorithm-to-put-more-focus-on-original-content/831976/
16. YouTube Help Community video, *New YouTube Shorts Metric – Viewed vs Swiped Away*. https://support.google.com/youtube/community-video/273390203/new-youtube-shorts-metric-viewed-vs-swiped-away
17. YouTube Help, *YouTube Partner Program overview & eligibility*. https://support.google.com/youtube/answer/72851
18. YouTube Help, *Advertiser-friendly content guidelines* (Violence). https://support.google.com/youtube/answer/6162278
19. YouTube Help, *Test & compare thumbnails and titles*. https://support.google.com/youtube/answer/13861714
20. YouTube Help, *Measure key moments for audience retention*. https://support.google.com/youtube/answer/9314415
21. YouTube Help, *Video chapters*. https://support.google.com/youtube/answer/9884579
22. YouTube Help, *Add end screens to videos*. https://support.google.com/youtube/answer/6388789

[M] Đo trực tiếp metadata công khai của YouTube bằng `yt-dlp --skip-download` (view, độ dài, ngày đăng, số sub) ngày 04/10/2026. URL: `https://www.youtube.com/watch?v=<id>` với id trong bảng mục 3.
