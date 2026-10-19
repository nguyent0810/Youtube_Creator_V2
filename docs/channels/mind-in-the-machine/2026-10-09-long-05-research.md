# Nghiên cứu video dài #5 — Mind in the Machine (MIM) — 09/10/2026

**Phạm vi:** hồ sơ dữ kiện có nguồn cho video dài thứ năm (16:9, 12–14 phút, tiếng Việt, faceless, giọng TTS Hải Đăng + motion graphics + ảnh
mở, theme "lab"): **"Thuật toán đề xuất: vì sao TikTok/YouTube biết bạn thích gì?"** (slug `mim-ai-feed`). Đề tài từ
`2026-10-06-topic-research.md` §3.1 #6 ("Bạn chưa nói gì, nhưng bạn đã dừng lại 3 giây" — TikTok 257/ngày, YouTube 705/ngày trên vi.wiki; chưa
có bài vi.wiki "hệ thống khuyến nghị"; rủi ro: "không khẳng định chi tiết thuật toán nội bộ của một hãng"). Áp dụng `motion/long/RETENTION.md`
(cold open, **lộ trình đổi hình thức** — #1 "ba câu hỏi", #2 "ba chặng đường", #3 "lời thách", #4 "cảnh hẹn trước" → #5 **"nghịch lý"**), checklist
retro 2 (`docs/pm/2026-10-07-retro-2.md`, "Quy trình cho video kế tiếp" bước 1–4) và khuôn hồ sơ/kịch bản MIM #4.

**Kịch bản đi kèm:** `data/long/mim-ai-feed/script.md` (bản 1, đã qua `python motion/long/script_lines.py mim-ai-feed`: 9 chương, 174 câu,
2.937 âm tiết đếm thô, 0 lỗi integrity, không có `ROADMAP_CLICHE`; chờ agent kiểm chứng).

**Phương pháp:**
- Đọc tận gốc khi mở được: **bài báo khoa học** (Covington et al. 2016 — PDF toàn văn qua `pdftotext`; Feuerverger et al. 2012 — PDF toàn văn
  arXiv), **blog chính hãng** (YouTube 2021 — HTML toàn văn qua curl; Netflix Tech Blog 2012 — toàn văn qua trình duyệt), **thông cáo Netflix
  21/09/2009** (bản PDF lưu ở asc.ohio-state.edu), **trang trợ giúp** TikTok (EN + VI) và YouTube (EN + VI) — đọc bằng trình duyệt ngày
  09/10/2026 (trang TikTok dựng bằng JS, curl chỉ ra khung), **Cổng TTĐT Chính phủ** (baochinhphu.vn) cho phần Việt Nam.
- Tóm tắt (abstract) qua **arXiv API** và **Europe PMC** cho các nghiên cứu bộ lọc/hang thỏ; siêu dữ liệu xuất bản qua **Crossref**.
- Trang **chặn script / không mở được** hôm nay: newsroom.tiktok.com (curl trả 000, WebFetch lúc đầu được, sau đó lỗi DNS), web.archive.org
  (429 — không đọc được bảng xếp hạng gốc netflixprize.com), science.org (Cloudflare), EUR-Lex (chuyển hướng → không đọc nguyên văn DSA).
- Wikimedia Commons API (`generator=search`, 40 kết quả đầu, đọc `LicenseShortName`), User-Agent `yt-factory-research/1.0
  (https://github.com/nguyent0810/Youtube_Creator_V2)`, giãn ~1 giây. Pexels qua `motion/long/pexels.py search mim-ai-feed …` (khoá đọc từ
  `.local.env`, không in; chỉ tìm, chưa tải; chỉ mục `output/long/mim-ai-feed/broll/index.json`).
- **Nhãn dữ kiện:** **[bằng chứng]** = đã đọc tận nguồn gốc hôm nay · **[tóm tắt]** = đọc abstract chính thức, chưa đọc toàn văn ·
  **[SECONDARY]** = qua báo/kết quả tìm kiếm · **[CHƯA KIỂM]** = chưa đủ tin, không đọc lên. Trích nguyên văn giữ tiếng Anh. Số `[n]` trỏ tới mục 10.

---

## 1. Tóm tắt

- **Đề tài:** máy đề xuất đoán sở thích thế nào (lọc cộng tác → tín hiệu ngầm: thời gian xem, xem hết/lướt qua), các hãng tự công bố được gì,
  nghiên cứu độc lập nói gì về "hang thỏ", và **cách dạy lại bảng tin** (YouTube + TikTok, đã kiểm trang trợ giúp 10/2026). Trục A "AI dễ
  hiểu" + B "công nghệ đổi thế giới" (Netflix Prize 2006–2009 làm trục lịch sử).
- **Vì sao bây giờ (3 dòng):**
  1. *Nhu cầu Việt:* YouTube (705/ngày) và TikTok (257/ngày) thuộc nhóm bài vi.wiki công nghệ được đọc nhiều nhất; chưa có bài vi.wiki
     về hệ thống khuyến nghị (topic-research §2). Bộ TT&TT từng đưa **thuật toán phân phối nội dung** của TikTok vào đợt kiểm tra toàn diện
     2023 [22][23].
  2. *Cold open có nguồn gốc kiểm được:* chung kết Netflix Prize 26/07/2009 — hai đội bằng điểm tới chữ số thập phân thứ tư, đội nộp sớm hơn
     **20 phút** thắng [1][2] [bằng chứng].
  3. *Giải thích có nguồn gốc chính hãng + phản biện độc lập:* YouTube (blog 2021 + bài RecSys 2016), TikTok (newsroom 2020 + trang trợ giúp
     2026), đặt cạnh 5 nghiên cứu bình duyệt bất đồng nhau (FAT* 2020, Sci Adv 2023, PNAS 2023, PNAS 2024, Science 2023).
- **Lộ trình — hình thức "Nghịch lý"** (không lặp 4 hình thức của #1–#4): *"Cỗ máy được khách hàng chấm điểm cẩn thận thì bị cất đi. Cỗ máy
  hiếm khi hỏi bạn câu nào lại thành thứ bạn lướt mỗi ngày. Video này đi tìm lời giải cho nghịch lý ấy."* → trả ở ch5 (giữa video: "máy không
  cần hỏi, vì việc xem của bạn đã trả lời thay"). Kèm lời hứa thực hành "cuối video… dạy lại bảng tin" → trả ở ch8.
- **Mô-típ:** (a) **"Bạn chưa nói gì / câu trả lời im lặng"** (ch0 → ch4 → ch5 → ch8); (b) **những ngôi sao** (chấm sao Netflix → YouTube hỏi
  lại 1–5 sao "lùi xuống làm giám khảo" → Netflix bỏ năm sao 2017 → câu kết "thứ quý nhất là những giây bạn dừng lại"); (c) **hai mươi phút /
  một phần trăm nghìn** (ch0, ch5, ch8).
- **Cảnh mạnh thứ hai (~67–74%):** "bot phản thực tế" (Hosseinmardi et al., PNAS 2024): bot chỉ nghe theo đề xuất lại xem **ít** nội dung thiên
  lệch hơn người thật — đồng tác giả là chính người đứng tên đầu nghiên cứu "hang thỏ" 2020 [15][18]; nối sang thí nghiệm **tắt thuật toán**
  (Science 2023) ở ch7 [19].
- **Câu hỏi để lại:** "Video gần nhất khiến bạn giật mình, kiểu 'sao nó biết mình thích cái này', là video gì?"
- **Đăng đề xuất:** sau #4. Không có mốc ngày lễ; chủ đề thường xanh. Phần thực hành (ch8) phụ thuộc giao diện → **kiểm lại tên nút trên app
  thật trong tuần đăng**.

---

## 2. Chấm ứng viên

| Tiêu chí | Điểm (1–5) | Lý do |
|---|---:|---|
| Cold open | **5** [bằng chứng] | Hai nguồn độc lập khớp nhau: thông cáo Netflix (24 phút trước khi đóng) + Statistical Science 2012 (20 phút sau, 0,856704 vs 0,856714) |
| Rủi ro sai | 3 | Nguồn chính hãng dễ thành quảng cáo → chỉ dùng phần **mô tả cơ chế** + nói rõ "theo YouTube/TikTok"; các số -70%, <1% của YouTube ghi "YouTube tự công bố"; nghiên cứu hang thỏ bất đồng → nêu cả hai phía |
| Nhu cầu VN | 4 | Ai cũng dùng TikTok/YouTube; phần thực hành dùng ngay; Bộ TT&TT 2023 có nhắc thuật toán |
| Hình | 2 | Gần như không có ảnh mở phù hợp (logo/giao diện có bản quyền) → dựng bằng chữ/đồ hoạ: bảng xếp hạng, ma trận sao, phễu, hai bot; Pexels cho cảnh lướt điện thoại |
| Độ khác so với #1–#4 | 5 | #1 lịch sử AI, #2 việc làm, #3 giả giọng, #4 ảo giác; #5 là AI **chạy ngầm** mỗi ngày |

---

## 3. Xương sống câu chuyện

- **Câu hỏi trung tâm:** *Vì sao một cỗ máy hiếm khi hỏi bạn câu nào lại đoán trúng gu bạn hơn cỗ máy được trả một triệu đô để đoán số sao
  bạn chấm?*
- **Cung A → B:** A = "đề xuất = đoán điều bạn **nói** bạn thích" (số sao, Netflix Prize). B = đề xuất hiện nay dựa nhiều nhất vào điều bạn
  **làm** (xem hết, lướt qua, thời gian xem) — theo chính lời hãng; hệ quả: (1) riêng tư hơn (vụ lần ngược dữ liệu Netflix), (2) câu hỏi "hang
  thỏ" — bằng chứng bất đồng, (3) quyền kiểm soát nằm ở chính hành vi của bạn + vài nút có thật.
- **Phân tích riêng của kênh (chống "inauthentic content"):**
  1. Nối **ba giai đoạn** bằng một mô-típ: sao (Netflix 2006) → cú nhấp (YouTube 2011) → thời gian xem (YouTube 2012, TikTok 2020) → sao quay
     lại làm "giám khảo" (YouTube đo "valued watchtime" bằng khảo sát 1–5 sao, 2021). Ba mảnh từ ba nguồn chính hãng khác nhau.
  2. "Các hãng công bố nguyên liệu, không công bố công thức": đặt lời hãng (TikTok: tương tác/thời gian xem "generally weighted more heavily")
     cạnh kiểm định độc lập (Boeker & Urman 2022: follow > thích > tỉ lệ xem) — không mâu thuẫn trực tiếp (khác thời điểm, khác phép đo) nhưng
     cho thấy không nên rút gọn thành "chỉ cần xem lâu".
  3. Cùng một nhà khoa học (Manoel Horta Ribeiro) đứng tên ở nghiên cứu 2020 (người dùng trôi về cực đoan) và 2024 (đề xuất kéo về ôn hoà) →
     minh hoạ trung thực rằng câu trả lời **đổi theo năm và cách đo** (và theo thay đổi năm 2019 của YouTube).
- **Thời lượng:** ~3.115 âm tiết đọc đủ chữ (đếm thô `script_lines.py` 2.937) ≈ 13,8 phút ở 225 âm tiết/phút (nhịp đo được của MIM #4).

---

## 4. Dàn ý chương + dữ kiện

Ký hiệu vòng: **[Mở Vn]** / **[Đóng Vn]**. Ảnh: tên file Commons nguyên văn, giấy phép đọc qua API ngày 09/10/2026. **Không BY-SA.**

| # | Chương | Câu | Âm tiết thô | Âm tiết đọc đủ* | % lũy kế |
|---|---|---:|---:|---:|---:|
| 0 | Cold open — Hai mươi phút, một triệu đô (+ nghịch lý) | 22 | 326 | ~338 | 11% |
| 1 | Những người giống bạn (lọc cộng tác; giải tiến bộ 2007) | 19 | 309 | ~324 | 21% |
| 2 | Một triệu đô không dùng tới (streaming; lần ngược dữ liệu) | 17 | 311 | ~332 | 32% |
| 3 | Cú nhấp biết nói dối (YouTube 2008–2021; RecSys 2016) | 20 | 325 | ~354 | 43% |
| 4 | Bạn chưa nói gì (TikTok 2020 + 2026; Boeker & Urman) | 20 | 324 | ~335 | 54% |
| 5 | **Re-hook:** Lời giải của nghịch lý | 11 | 179 | ~191 | 60% |
| 6 | Hang thỏ (Ribeiro 2020, Chen 2023, **Hosseinmardi 2024 = cảnh mạnh thứ hai**, Haroon 2023) | 24 | 457 | ~500 | 76% |
| 7 | Tắt thuật toán đi (Science 2023; DSA; Bộ TT&TT 2023) | 17 | 321 | ~350 | 87% |
| 8 | Dạy lại bảng tin của bạn (YouTube + TikTok; kết) | 24 | 385 | ~391 | 100% |
| | **Tổng** | **174** | **2.937** | **~3.115** | ≈ 13,8 phút |

\* Số đọc đủ chữ ("2009" = 6 âm tiết, "8,43" ≈ 5). Nếu TTS nháp > 14,5 phút, cắt theo thứ tự: (a) câu "Năm 2017, chính Netflix bỏ hẳn thang
năm sao…" (ch5, [SECONDARY]); (b) cặp câu Haroon "Đề xuất từ các kênh có vấn đề…" (ch6, giữ trên hình); (c) câu "Thời thuê đĩa…" (ch2).

### 0. Cold open — "Hai mươi phút, một triệu đô"

- **Vòng:** [Mở V0] nghịch lý "cỗ máy được chấm điểm bị cất đi; cỗ máy không hỏi lại thắng" → **đóng ở ch5**. [Mở V1] "cuối video… dạy lại
  bảng tin" → **đóng ở ch8**.
- **Dữ kiện:**
  1. Thông cáo Netflix, New York, 21/09/2009 (PRNewswire) [1] [bằng chứng]: *"After almost three years and submissions by more than 40,000 teams
     from 186 countries, Netflix … today awarded the $1 million Netflix Prize … the competition's goal of a 10 percent improvement over the
     accuracy of the Netflix movie recommendation system when the competition was launched in Oct. 2006."* · *"Netflix said 'BellKor's
     Pragmatic Chaos' edged out a team called 'The Ensemble,' … with the winning submission coming just 24 minutes before the conclusion of the
     nearly three-year-long contest. … it took a team of external and internal judges several weeks to validate the winner after the contest
     closed on July 26."* · BPC = *"the merging of three teams that had previously competed against one another"*; 7 thành viên (Áo, Canada,
     Israel, Mỹ). Netflix khi đó: *"the world's largest online movie rental service"*, gửi DVD qua thư.
  2. Feuerverger, He, Khatri, *Statistical Science* 27(2), 2012 [2] [bằng chứng]: bắt đầu 02/10/2006; mốc RMSE ≤ 90% × 0,9525 = **0,8572** trên
     bộ test; *"on July 26, 2009, the Grand Prize winning entry was submitted by the 'BellKor's Pragmatic Chaos' team, attaining RMSE values of
     0.8554 and 0.8567 on the quiz and test sets"* · *"Twenty minutes after that submission … a competing submission was made by 'The
     Ensemble' … 0.8553 on the quiz set, and … 0.8567 on the test set. To two additional decimal places … 0.856704 by the winners, and 0.856714
     by the runners up. Since the contest rules were based on test set RMSE, and also were limited to four decimal places, these two
     submissions were in fact a tie. … the prize went to the earlier submission."* · Bảng xếp hạng công khai chỉ hiện điểm **quiz**.
  3. Netflix Tech Blog 2012 [3] [bằng chứng]: bản thắng giải cuối không đưa vào sản phẩm (xem ch2).
- **Trung thực:** "24 phút trước khi đóng" (Netflix) và "20 phút sau" (Feuerverger) khớp nhau; một số báo viết "22 phút" → lời đọc theo hai
  nguồn trên, **không** nêu giờ:phút. "Hai liên minh dẫn đầu cùng vượt vạch mười phần trăm": cả hai ≥ 10% trên quiz và test (10,06%). "Netflix
  nhận về cỗ máy thắng giải": đội *"licensed its work to Netflix"* [1].
- **Hình:** bảng xếp hạng **dựng lại bằng chữ** (2 hàng, cột QUIZ công khai / TEST giữ kín; số 0,8554/0,8553 rồi 0,8567 = 0,8567), đồng hồ đếm
  ngược 24:00 → 04:00; nhãn nguồn [1][2]. Pexels (VIDEO MINH HỌA): 6864480 / 6864483 "browsing at a cd store" (gợi thời đĩa), 3694918
  "packing DVD collection". Không ảnh thành viên đội (ảnh báo chí có bản quyền), không logo Netflix làm chủ thể. Ảnh `Netflixenvelope.jpg`
  (CC BY 2.5, BlueMint, 2006, 490 px, có logo) — **không dùng** (nhỏ, logo).

### 1. "Những người giống bạn"

- **Vòng:** [Mở V2] "khi bài thắng giải tới tay Netflix, thì chính Netflix đã đổi khác" → ch2.
- **Dữ kiện:**
  1. Dữ liệu [2] [bằng chứng]: **100.480.507** lượt chấm, **480.189** khách, **17.770** phim, 10/1998–12/2005, thang 1–5 sao; ma trận *"about 99%
     sparse"*. Thông cáo [1]: *"contained only movie titles, star ratings and dates but no text reviews"*.
  2. Ví dụ lọc cộng tác — TikTok Support "How TikTok recommends content" (đọc 09/10/2026) [10] [bằng chứng]: *"If User A likes videos 1, 2, and 3;
     User B likes videos 1, 2, 3, 4, and 5; then the recommender system may predict User A will also like videos 4 and 5."*
  3. Ví dụ YouTube — Goodrow 2021 [7] [bằng chứng]: *"if you like tennis videos and our system notices that others who like the same tennis videos
     as you also enjoy jazz videos, you may be recommended jazz videos, even if you've never watched a single one before"*.
  4. Giải tiến bộ 2007 — Netflix Tech Blog 2012 [3] [bằng chứng]: *"the Korbell team won the first Progress Prize with an 8.43% improvement. They
     reported more than 2000 hours of work … final combination of 107 algorithms"*; Netflix đưa **Matrix Factorization (SVD)** và **RBM** vào sản
     phẩm (*"we put the two algorithms into production, where they are still used"*).
  5. Bản cuối: *"blending hundreds of predictive models"* [3]; BPC = 3 đội gộp [1].
- **Phân tích của kênh:** "dãy số như bản đồ khẩu vị" = diễn giải **đơn giản hoá** của phân rã ma trận (nói rõ "nói thật đơn giản" trong lời).
- **Hình:** bảng sao 6×8 với phần lớn ô trống (99%), ô "?" được điền dần; bảng "người A / người B / video 1–5" của TikTok (dựng lại, ghi nguồn);
  hai chấm trên "bản đồ khẩu vị" 2D dịch lại gần nhau.

### 2. "Một triệu đô không dùng tới"

- **Vòng:** [Đóng V2]. [Mở V3] "một công ty khác học bài học ấy… qua những cú nhấp chuột" → ch3.
- **Dữ kiện:**
  1. Netflix Tech Blog, *Netflix Recommendations: Beyond the 5 stars (Part 1)*, X. Amatriain & J. Basilico, 06/04/2012 [3] [bằng chứng]: *"We
     evaluated some of the new methods offline but the additional accuracy gains that we measured did not seem to justify the engineering
     effort needed to bring them into a production environment."* · *"Netflix launched an instant streaming service in 2007, one year after the
     Netflix Prize began."* · thời DVD: *"selection is distant in time from viewing … and we get no feedback during viewing"* · streaming: *"we can
     observe viewing statistics such as whether a video was watched fully or only partially."* · *"now 75% of what people watch is from some sort
     of recommendation."*
  2. Cuộc thi thứ hai, công bố cùng ngày 21/09/2009 [1] [bằng chứng]: *"predicting movie enjoyment by members who don't rate movies often, or at
     all, by taking advantage of demographic and behavioral data carrying implicit signals"*.
  3. A. Narayanan, V. Shmatikov (Đại học Texas tại Austin), *Robust De-anonymization of Large Sparse Datasets* (IEEE S&P 2008; arXiv cs/0610105)
     [4] [tóm tắt]: *"Using the Internet Movie Database as the source of background knowledge, we successfully identified the Netflix records of
     known users, uncovering their apparent political preferences and other potentially sensitive information."*
  4. Huỷ cuộc thi thứ hai 12/03/2010 (blog Neil Hunt, trích qua báo/EPIC) [5] [SECONDARY]: *"We have reached an understanding with the FTC and
     have settled the lawsuit with plaintiffs."* · Feuerverger 2012 [2] [bằng chứng] xác nhận: *"Fearing legal consequences, a second and related
     contest … was canceled"* sau lập luận của Narayanan & Shmatikov.
- **Hình:** thẻ trích blog 2012 (chữ, không logo); thanh "xem hết / xem một phần" (dựng); vòng tròn 75%; hai bảng (IMDb công khai ↔ Netflix ẩn
  danh) nối bằng đường khớp → một hàng sáng lên (minh hoạ, không tên người thật). Pexels: 6943542 "man in bed looking at phone".

### 3. "Cú nhấp biết nói dối"

- **Vòng:** [Đóng V3]. [Mở V4] "ở TikTok, câu chuyện bắt đầu từ ngón tay cái" → ch4.
- **Dữ kiện:**
  1. Cristos Goodrow, *On YouTube's recommendation system*, YouTube Official Blog, 15/09/2021 [7] [bằng chứng]: *"I've spent over a decade at
     YouTube building our recommendation system"* · *"Back in 2008 … The system ranked videos based on popularity to create one big 'Trending'
     page."* · *"we learned back in 2011 that clicking on a video doesn't mean you actually watched it"* (ví dụ Wimbledon: *"it's a person in
     their bedroom talking about the match"*) · *"That's why we added in watchtime in 2012."* · *"learning every day from over 80 billion pieces
     of information we call signals"* (đã cắt khỏi lời đọc để vừa thời lượng) · *"valued watchtime … user surveys that ask you to rate the video
     you watched from one to five stars … Only videos that you rate highly with four or five stars are counted as valued watchtime."* · *"we've
     trained a machine learning model to predict potential survey responses for everyone."*
  2. P. Covington, J. Adams, E. Sargin (Google), *Deep Neural Networks for YouTube Recommendations*, RecSys '16, 15–19/09/2016, Boston [8]
     [bằng chứng, toàn văn]: kiến trúc hai tầng *candidate generation* + *ranking*; Hình 2: video corpus "millions" → "hundreds" → "dozens";
     *"Although explicit feedback mechanisms exist on YouTube (thumbs up/down, in-product surveys, etc.) we use the implicit feedback of watches
     to train the model, where a user completing a video is a positive example. This choice is based on the orders of magnitude more implicit
     user history available"* · *"Ranking by click-through rate often promotes deceptive videos that the user does not complete ('clickbait')
     whereas watch time better captures engagement."* · mục tiêu xếp hạng *"generally a simple function of expected watch time per impression"*.
- **Trung thực:** bài 2016 mô tả hệ thống **năm 2016**; lời đọc nói "mô hình trong bài". "Ba kỹ sư Google" ✓ (3 tác giả, Google Mountain View).
- **Hình:** phễu ba tầng (vẽ lại theo Hình 2, ghi nguồn); thẻ trích "clickbait"; minh hoạ Wimbledon: ảnh `Centre Court (26 June 2009,
  Wimbledon).jpg` (**CC BY 2.0**, Squeaky Knees, 26/06/2009, sân Trung tâm Wimbledon, London) hoặc `Centre court 2006.JPG` (**PD**, Clavecin,
  Wimbledon 2006) — **ẢNH MINH HỌA**; ảnh `YouTube HQ 1.JPG` (**CC BY 3.0**, BrokenSphere, 09/08/2010, trụ sở YouTube, San Bruno, California) —
  dùng ngắn, không phóng to logo. Thang 1–5 sao, 4–5 sao sáng lên "THỜI GIAN XEM CÓ GIÁ TRỊ".

### 4. "Bạn chưa nói gì"

- **Vòng:** [Đóng V4]. Vòng nội bộ "có ai kiểm tra từ bên ngoài?" → trả ngay (Boeker & Urman).
- **Dữ kiện:**
  1. TikTok Newsroom, *How TikTok recommends videos #ForYou*, 18/06/2020 [9] [bằng chứng — đọc qua WebFetch, trích đoạn; chưa có bản lưu thô]:
     ba nhóm yếu tố (*"User interactions such as the videos you like or share, accounts you follow, comments you post, and content you create"*;
     *"Video information … captions, sounds, and hashtags"*; *"Device and account settings like your language preference, country setting, and
     device type"* — *"receive lower weight"*) · *"A strong indicator of interest, such as whether a user finishes watching a longer video from
     beginning to end, would receive greater weight than a weak indicator, such as whether the video's viewer and creator are both in the same
     country."* · *"Neither follower count nor whether the account has had previous high-performing videos are direct factors"* · *"we invite
     new users to select categories of interest, like pets or travel"* · *"Your For You feed generally won't show two videos in a row made with
     the same sound or by the same creator."* · *"long-press on a video and tap 'Not Interested'"* · nhắc "filter bubble".
  2. TikTok Support, *How TikTok recommends content* (EN, đọc 09/10/2026) [10] [bằng chứng]: For You — *"User interactions: Content you like,
     share, comment on, and watch in full or skip…"* · *"For most users, user interactions, which may include the time spent watching a video,
     are generally weighted more heavily than others."* · *"How important each factor is can change over time."* · bỏ qua bước chọn chủ đề →
     *"we start by showing you recent posts that are popular with others on TikTok"*.
  3. TikTok Support, *For You* / *Đề xuất* (EN + VI) [11] [bằng chứng]: nút Chia sẻ → **"Tại sao đăng bài này hiển thị"** (EN "Why this post");
     lý do mẫu: **"Video này dài hơn và có vẻ như bạn thích những video dài hơn."** (nguyên văn tiếng Việt của TikTok).
  4. M. Boeker, A. Urman, *An Empirical Investigation of Personalization Factors on TikTok*, Proceedings of the ACM Web Conference 2022,
     tr. 2298–2309, doi 10.1145/3485447.3512102 (arXiv 2201.12271) [13] [tóm tắt]: sock-puppet; thử ngôn ngữ, vị trí, follow, like, thời gian
     xem; *"all the tested factors influence the content recommended"*; *"the follow-feature has the strongest influence, followed by the
     like-feature and video view rate."* (Bài lưu ở kho ZORA của Đại học Zurich → lời đọc "ở Thuỵ Sĩ"; **chưa mở trang tác giả** để xác nhận
     đơn vị của cả hai.)
  5. Goodrow 2021 [7]: *"our recommendation system doesn't operate off of a 'recipe book'"* · *"the importance of each signal depends on you"*.
- **Trung thực:** không nêu "3 giây" (không nguồn). Không suy diễn trọng số cụ thể. Bản 1 đã **bỏ** câu "số người theo dõi không phải yếu tố
  trực tiếp" (dễ lẫn với kết quả "follow mạnh nhất" — hai chuyện khác nhau: follower count của người làm video vs. việc *bạn* follow).
- **Hình:** ba cột "BẠN LÀM GÌ · VIDEO CÓ GÌ · MÁY CỦA BẠN" (trọng số nặng/nhẹ); thẻ "Tại sao đăng bài này hiển thị" **dựng lại bằng chữ**
  (không chụp app); bảng xếp hạng ba yếu tố Boeker & Urman. Pexels: 38667506 "scrolling social media on smartphone at night", 35888104
  "scrolling smartphone news feed in close-up", 9785300 "hands scrolling on the phone" (kiểm từng khung: **không** để lộ giao diện/logo TikTok
  hay mặt nhà sáng tạo; bỏ 14377165 "scrolling through the TikTok feed").

### 5. Re-hook ~54–60%: "Lời giải của nghịch lý"

- **Vòng:** [Đóng V0]. [Mở V5] "nó có kéo bạn xuống một cái hang thỏ không?" → ch6.
- **Dữ kiện:** 0,856704 vs 0,856714 → lệch **0,00001** [2]; YouTube 2021 [7]: *"Recommendations drive a significant amount of the overall
  viewership on YouTube, even more than channel subscriptions or search."* (lời đọc "một phần đáng kể", **không** nói "phần lớn"); Netflix bỏ
  5 sao, đổi sang thích/không thích (công bố 16/03/2017, áp dụng từ 04/2017) [6] [SECONDARY].
- **Hình:** thanh 0,856704 | 0,856714 phóng to tới chữ số thứ 6; ngôi sao vỡ thành dải "thời gian xem".

### 6. "Hang thỏ" (cảnh mạnh thứ hai ~67–74%)

- **Vòng:** [Đóng V5] (trả lời có điều kiện). [Mở V6] "nếu tắt hẳn thuật toán đi thì sao?" → ch7.
- **Dữ kiện:**
  1. M. H. Ribeiro, R. Ottoni, R. West, V. A. F. Almeida, W. Meira, *Auditing Radicalization Pathways on YouTube*, FAT* '20 (27/01/2020),
     tr. 131–141, doi 10.1145/3351095.3372879; arXiv 1908.08313 (22/08/2019) [15] [tóm tắt]: *"We analyze 330,925 videos posted on 349 channels"*
     (Media, Alt-lite, I.D.W., Alt-right) · *"Processing 72M+ comments, we show … that users consistently migrate from milder to more extreme
     content"* · khuyến nghị đo 05–07/2019: *"Alt-lite content is easily reachable from I.D.W. channels, while Alt-right videos are reachable
     only through channel recommendations."* (EPFL Thuỵ Sĩ + UFMG Brazil.)
  2. YouTube 2021 [7] [bằng chứng, số hãng tự công bố]: *"In 2019 we first began demoting borderline content in recommendations, resulting in a
     70% drop in watchtime on non-subscribed, recommended borderline content in the U.S."* · *"consumption of borderline content that comes from
     our recommendations is significantly below 1%"* (không đọc).
  3. A. Y. Chen, B. Nyhan, J. Reifler, R. E. Robertson, C. Wilson, *Subscriptions and external links help drive resentful users to alternative
     and extremist YouTube channels*, Science Advances 9(35):eadd8080, 30/08/2023 [16] [tóm tắt]: *"paired behavioral and survey data …
     recruited from a representative sample in 2020 (n = 1181)"* · *"exposure … is heavily concentrated among a small group of people with high
     prior levels of gender and racial resentment"* · *"These viewers often subscribe to these channels … and follow external links to them. In
     contrast, nonsubscribers rarely see or follow recommendations"* · *"YouTube's algorithms were not sending people down 'rabbit holes'
     during our observation window in 2020, possibly due to changes … in 2019."*
  4. **Cảnh mạnh thứ hai** — H. Hosseinmardi, A. Ghasemian, M. Rivera-Lanas, M. Horta Ribeiro, R. West, D. J. Watts, *Causally estimating the
     effect of YouTube's recommender system using counterfactual bots*, PNAS 121(8):e2313377121, 13/02/2024 (arXiv 2308.10398) [18] [tóm tắt]:
     *"By comparing bots that replicate real users' consumption patterns with 'counterfactual' bots that follow rule-based trajectories, we show
     that, on average, relying exclusively on the recommender results in less partisan consumption, where the effect is most pronounced for
     heavy partisan consumers."* · *"YouTube's sidebar recommender 'forgets' their partisan preference within roughly 30 videos regardless of
     their prior history, while homepage recommendations shift more gradually"* · *"at least since the algorithm changes that YouTube
     implemented in 2019, individual consumption patterns mostly reflect individual preferences, where algorithmic recommendations play, if
     anything, a moderating role."*
  5. M. Haroon, M. Wojcieszak, A. Chhabra, X. Liu, P. Mohapatra, Z. Shafiq, *Auditing YouTube's recommendation system for ideologically
     congenial, extreme, and problematic recommendations*, PNAS 120(50):e2213020120, 05/12/2023 [17] [tóm tắt]: *"100,000 sock puppets"* ·
     *"YouTube's algorithm recommends congenial content to its partisan users … congenial recommendations increase deeper in the trail for
     right-leaning users"* · *"We do not find meaningful increases in ideological extremity"* · *"proportion of these problematic
     recommendations is low (max of 2.5%), they are still encountered by over 36.1% of users"*.
- **Trung thực:** (a) mô tả bot thứ hai "đi cùng con đường tới một điểm, rồi chỉ bấm theo đề xuất" là **diễn giải** từ "counterfactual bots that
  follow rule-based trajectories" + hiểu biết về thiết kế bài — **cần đối chiếu Methods** (mục 9.2); (b) "ác cảm về giới và chủng tộc" = dịch
  "gender and racial resentment" (thang đo khảo sát); (c) "từ kênh báo chí chính thống tới kênh cực hữu" = nhóm Media → Alt-right; không đọc tên
  nhóm (IDW, Alt-lite) — hiện trên hình; (d) không có nghiên cứu TikTok tương đương trong hồ sơ → lời đọc nói "phần lớn chỉ xét YouTube, ở Mỹ";
  (e) số -70% ghi "YouTube tự công bố".
- **Hình:** dòng thời gian 2019 (Ribeiro; YouTube đổi) → 2020 (Chen thu dữ liệu) → 2023 (Chen, Haroon) → 2024 (Hosseinmardi); sơ đồ **hai bot**
  tách nhánh (đường người thật vs. đường "chỉ bấm đề xuất"), thanh thiên lệch thấp hơn ở nhánh bot; số 2,5% / 36,1%. Pexels (MINH HỌA): 37478253
  "aerial view of green labyrinth", 39885123 "man exploring a hedge maze".

### 7. "Tắt thuật toán đi"

- **Vòng:** [Đóng V6]. [Mở V7] "bảng tin của bạn vẫn được dạy bởi… chính bạn" → ch8.
- **Dữ kiện:**
  1. A. M. Guess, N. Malhotra, J. Pan, P. Barberá, H. Allcott, … (2020 Facebook & Instagram Election Study), *How do social media feed
     algorithms affect attitudes and behavior in an election campaign?*, Science 381(6656):398–404, 27/07/2023, doi 10.1126/science.abp9364 [19]
     [tóm tắt]: *"We assigned a sample of consenting users to reverse-chronologically-ordered feeds instead of the default algorithms. Moving
     users out of algorithmic feeds substantially decreased the time they spent on the platforms and their activity. … The amount of political
     and untrustworthy content they saw increased on both platforms, the amount of content classified as uncivil or containing slur words they
     saw decreased on Facebook … the chronological feed did not significantly alter levels of issue polarization, affective polarization,
     political knowledge, or other key attitudes during the 3-month study period."* · **Errata:** 05/12/2024 (doi 10.1126/science.adu8261 —
     **chưa đọc**, science.org chặn) và 19/03/2026 (doi 10.1126/science.aeh2575 — theo tóm tắt [SECONDARY]: cách đếm bài "carousel" Instagram;
     *không* ảnh hưởng ước lượng thực nghiệm). Lời đọc chỉ dùng ba kết luận chính của tóm tắt.
  2. TikTok Newsroom, 04/08/2023, *Fulfilling our commitments under the DSA* [12] [SECONDARY — qua đoạn trích kết quả tìm kiếm; trang lỗi DNS khi
     mở]: người dùng châu Âu tắt cá nhân hoá → For You và LIVE *"show popular videos from both the places where they live and around the
     world"*; Following/Friends theo thứ tự thời gian. Xác nhận bằng trang trợ giúp hiện hành [10] [bằng chứng]: *"The For You feed will become a
     Popular feed and serve popular content from your region and internationally."* · *"Note: This non-personalization feature is only
     available in the EU and Kazahkstan."* (chính tả gốc của TikTok); trang For You [11]: *"If you're located in the European Economic Area
     (EEA), the UK, or Switzerland, you can turn off personalized recommendations"*.
  3. Bộ TT&TT, họp báo 06/04/2023 (Cục trưởng Cục PTTH&TTĐT Lê Quang Tự Do) — Báo Điện tử Chính phủ [22] [bằng chứng]: *"…từ năm 2022 đến nay
     trên Tiktok đã có nhiều nội dung vi phạm như … sử dụng thuật toán phân phối nội dung tự động để tạo xu hướng nhằm phát tán nội dung giật
     gân, câu view, bất chấp đó là nội dung độc hại, phản cảm…"*; *"Bộ cũng sẽ kiểm tra các thuật toán, cách thức, quy trình phân phối nội dung
     của nền tảng Tiktok."*
  4. Bộ TT&TT công bố kết quả 05/10/2023 — Báo Điện tử Chính phủ [23] [bằng chứng]: *"Sau hơn 4 tháng triển khai kiểm tra toàn diện…"*; yêu cầu
     TikTok Singapore *"không sử dụng thuật toán để tạo xu hướng hoặc đề xuất đến người dùng các nội dung vi phạm pháp luật Việt Nam"*. Kiểm tra
     bắt đầu 15/05/2023 [22][24].
- **Trung thực:** Bộ TT&TT đã sáp nhập vào Bộ KH&CN (2025) → lời đọc giữ tên lúc sự việc diễn ra ("Bộ Thông tin và Truyền thông", năm 2023).
  Lời đọc dùng đúng mức ngôn từ của văn bản (nêu đánh giá của Bộ, không thêm kết luận). **Không** nêu số người dùng TikTok Việt Nam: bài
  mst.gov.vn 04/07/2024 [25] ghi ba con số khác nhau (49,9 triệu, ~45 triệu, ~20 triệu) từ nguồn thứ cấp → không đủ tin. Không nói "luật DSA
  buộc…" chi tiết điều khoản (chưa đọc nguyên văn EUR-Lex hôm nay) — lời đọc chỉ "theo Đạo luật Dịch vụ số".
- **Hình:** hai bảng tin cạnh nhau (THEO THUẬT TOÁN ↔ MỚI NHẤT LÊN ĐẦU), ba thẻ kết quả Science; ảnh `Berlaymont building in Brussels.jpg`
  (**CC0**, almathias, 07/05/2016, trụ sở Ủy ban châu Âu, Brussels) hoặc `European Commission in Brussels.jpg` (**CC0**, Jai79, 15/04/2011) —
  ẢNH MINH HỌA; bản đồ "có nút tắt cá nhân hoá" (EU/EEA, UK, Thuỵ Sĩ, Kazakhstan) với Việt Nam xám; thẻ trích Báo Chính phủ 06/04 + 05/10/2023
  (chữ, không chụp trang). Pexels: 35369142 "bustling street scene in Hanoi" (bối cảnh VN, MINH HỌA).

### 8. "Dạy lại bảng tin của bạn" (áp dụng + kết)

- **Vòng:** [Đóng V1], [Đóng V7]. Trả mô-típ (a) "lướt qua cũng là một câu trả lời", (b) "những ngôi sao không phải thứ quý nhất", (c) "hai mươi
  phút".
- **Dữ kiện (đã kiểm trang trợ giúp 09/10/2026):**
  1. YouTube Help 6342839 *Manage your recommendations & search results* (EN + bản VI "Quản lý nội dung đề xuất và kết quả tìm kiếm") [20]
     [bằng chứng]: More ⋮ → **"Không quan tâm"** (Not interested) → "Xin cho biết lý do"; **"Không đề xuất kênh này"** (Don't recommend channel);
     xoá phản hồi trong Hoạt động của tôi; **"Ẩn bớt video Shorts"**; *"Turn off your history … when you're researching a subject for a school
     project that you aren't personally interested in"* (VN: "dự án ở trường"); *"If you don't want video recommendations on Home, you can delete
     and turn off your watch history."*; recommendations *"also based on videos that you've liked"*; YouTube *"may also use data from your Google
     Account activity"*.
  2. YouTube Help 95725 *View, delete, or turn on or off watch history* [21] [bằng chứng]: Android — ảnh hồ sơ → Settings → Manage all history →
     Controls → bỏ chọn "Include the YouTube videos you watch"; *"If you delete some or all of your watch history, YouTube won't base future video
     recommendations on that content."* · *"If you have no relevant or significant recent watch history and have indicated you do not wish to
     receive future recommendations based on that history, YouTube features like recommendations on the YouTube homepage are removed."*
  3. TikTok Support *Refresh your For You feed* [11] [bằng chứng]: Profile → Menu ☰ → Settings and privacy → **Content Preferences** → Refresh your
     For You feed; *"we'll show you some popular content. Your interactions with this content … will help reshape your For You feed"*; *"Once you
     refresh the feed, it can't be undone."*; chỉ ảnh hưởng For You.
  4. TikTok Support *Manage topics* [11] [bằng chứng]: Settings and privacy → Content preferences → Manage topics → *"Move the slider to adjust how
     much you want to see of each topic"* (ví dụ chủ đề: sports, food & drinks, lifestyle); *"it might take some time for us to personalize your
     feed"*.
  5. TikTok Support *For You* (VI) [11] [bằng chứng]: **"Không quan tâm"**, **"Làm mới bảng tin"**, **"Lọc từ khóa"** (*"xóa nội dung chứa các từ
     cụ thể và biến thể của chúng cùng các hashtag khỏi bảng tin Đề xuất và Đã follow"*), **"Quản lý chủ đề"**. Thao tác "nhấn giữ → Not
     Interested": bài newsroom 2020 [9].
  6. "Quên sau ~30 video" (cột đề xuất bên cạnh), trang chủ đổi chậm hơn — Hosseinmardi et al. 2024 [18] [tóm tắt]; lời đọc nói rõ "trong thí
     nghiệm năm 2024", "khi bot chuyển sang xem nội dung ôn hoà".
- **Danh sách trong lời đọc ≤ 3 mục:** ba việc (nói "không" · dọn lịch sử · chủ động chọn); mỗi việc ≤ 2–3 nút.
- **Không** khuyên "xoá app", "dùng VPN để có nút EU" hay lách quy định; không hứa "reset hoàn toàn" (YouTube còn dùng hoạt động Google + lượt
  thích; TikTok làm mới chỉ tác động bảng tin Đề xuất).
- **Hình:** menu **mô phỏng bằng chữ** theo trang trợ giúp (không chụp app, không logo), nhãn "Theo trang trợ giúp YouTube/TikTok, 10/2026 —
  giao diện có thể khác theo phiên bản"; thanh trượt chủ đề; kết bằng ngôi sao mờ dần, thay bằng vạch thời gian "dừng lại" sáng lên. Pexels:
  6611954 "man scrolling on mobile phone screen", 6756650 "person scrolling through a smartphone".

**Checklist RETENTION:** cold open có cảnh + câu hỏi chưa trả lời ✔ · lộ trình **"Nghịch lý"** ≠ #4 "Cảnh hẹn trước" (và ≠ #1–#3) ✔ · 8 vòng
(V0–V7) đóng ở chương sau ✔ · danh sách lời đọc ≤ 3 mục ✔ ("thứ nhất/hai/ba" ch7, "ba việc" ch8, tín hiệu "thích/xem hết/lướt qua") · mô-típ ≥ 3
lần ✔ (cả ba) · mỗi chương kết bằng câu cầu nối/câu hỏi ✔ · re-hook 54–60% ✔ (#4: 47–56%) · cảnh mạnh thứ hai 67–74% ✔ · pattern interrupt mỗi
chương (câu hỏi tu từ ch4/ch5/ch6, câu ngắn "Bạn chưa nói gì.", "Nhưng chưa nên kết luận vội.", trích dẫn) ✔ · số liệu có nguồn + năm ✔.

---

## 5. Kiểm kê hình mở (Commons, 40 kết quả đầu, 09/10/2026) [26]

| Truy vấn | PD/CC0 | CC BY | BY-SA | Nhận xét |
|---|---:|---:|---:|---|
| Netflix DVD envelope | 1 | 1 | 0 | `Netflixenvelope.jpg` CC BY 2.5 (2006, 490 px, logo) → không dùng; kết quả PD còn lại là sách djvu |
| Netflix headquarters Los Gatos | 0 | 0 | 5 | Toàn BY-SA → không dùng |
| Netflix Prize | 20 | 8 | 12 | Gần như toàn ảnh không liên quan (Obama); `Netflix prize.jpg` "PD, own work" 598 px không rõ nội dung/nguồn gốc → **không dùng** |
| YouTube headquarters San Bruno | 11 | 25 | 4 | `YouTube HQ 1.JPG`…`13.JPG` CC BY 3.0, BrokenSphere, 09/08/2010, San Bruno — dùng ngắn, ghi công |
| Wimbledon Centre Court | 4 | 7 | 29 | `Centre Court (26 June 2009, Wimbledon).jpg` CC BY 2.0; `Centre court 2006.JPG` PD (Clavecin) — ẢNH MINH HỌA cho ví dụ của Goodrow |
| Google data center servers | 24 | 4 | 10 | `Google Datacenter - The Dalles, Oregon (17832143871).jpg` CC BY 2.0, Tony Webster, 17/05/2015 (ngoại thất) — tuỳ chọn cho "80 tỉ tín hiệu" (đã cắt) |
| European Commission Berlaymont | 3 | 28 | 9 | CC0: `Berlaymont building in Brussels.jpg` (2016), `European Commission in Brussels.jpg` (2011) |
| Video rental store shelves | 7 | 1 | 0 | `Kino Balt Interier VHS koutek u.jpg` CC0 (2026, Séc) — không đúng bối cảnh Mỹ; dùng Pexels thay |
| Hanoi people using smartphones / Saigon street smartphone | 2 / 0 | 0 | 2 | Không có ảnh phù hợp → Pexels |

Thiếu ảnh mở cho: bảng xếp hạng Netflix Prize, giao diện TikTok/YouTube, thành viên các đội (→ dựng bằng chữ/đồ hoạ). **Không** dùng ảnh chụp
màn hình app (giao diện + nội dung nhà sáng tạo có bản quyền), **không** dùng ảnh do AI tạo.

**Pexels (đã tìm 09/10, chưa tải; chỉ mục `output/long/mim-ai-feed/broll/index.json`):** 38667506, 35888104, 9785300, 6756650, 6611954,
32606402, 38410500 (lướt điện thoại — soát từng khung không lộ logo/nội dung app) · 6943542, 7986756 (xem điện thoại trên giường) · 6864480,
6864483, 3694918 (cửa hàng đĩa, gói đĩa DVD) · 37478253, 39885123, 35120433 (mê cung) · 35369142, 35369136, 29326758 (phố Hà Nội/TP.HCM) · 7140928,
38496190 (phần cứng máy chủ). Tất cả nhãn **VIDEO MINH HỌA**. **Loại:** 14377165 (lộ bảng tin TikTok thật).

---

## 6. Huyền thoại / lỗi thường gặp

| Hay nói sai | Đúng là | Nguồn |
|---|---|---|
| "TikTok chỉ cần biết bạn xem bao lâu" / "dừng 3 giây là nó biết" | TikTok: nhiều nhóm yếu tố, tương tác (gồm thời gian xem) *thường* nặng hơn; kiểm định 2022: follow > thích > tỉ lệ xem; không có nguồn cho "3 giây" | [9][10][13] |
| "Thuật toán là một công thức bí mật cố định" | YouTube: không có "recipe book", trọng số tuỳ từng người; TikTok: tầm quan trọng mỗi yếu tố đổi theo thời gian. Hãng công bố nguyên liệu, không công bố trọng số | [7][10] |
| "Netflix dùng thuật toán thắng giải một triệu đô" | Netflix dùng 2 thuật toán từ giải tiến bộ 2007; bản thắng giải 2009 "không đáng công sức kỹ thuật" để đưa vào | [3] |
| "Dữ liệu đã ẩn danh thì an toàn" | Bộ dữ liệu Netflix Prize bị lần ngược bằng IMDb; cuộc thi thứ hai bị huỷ | [4][2][5] |
| "YouTube đẩy mọi người vào cực đoan" / "YouTube vô can" | Bằng chứng bất đồng: 2019 thấy người dùng trôi dần; sau thay đổi 2019, các nghiên cứu 2023–2024 thấy tiếp xúc tập trung ở nhóm nhỏ tự tìm đến, đề xuất kéo về ôn hoà — nhưng vẫn có đề xuất hợp quan điểm và 36,1% tài khoản giả gặp kênh có vấn đề | [15][16][17][18] |
| "Tắt thuật toán thì bảng tin sạch, bớt phân cực" | Thí nghiệm 3 tháng (Mỹ 2020): ít dùng hơn, **nhiều** nội dung chính trị + nguồn kém tin cậy hơn, phân cực không đổi đáng kể | [19] |
| "Người Việt cũng tắt được cá nhân hoá TikTok" | Trang trợ giúp: chỉ EU/EEA, UK, Thuỵ Sĩ, Kazakhstan | [10][11] |
| "Xoá lịch sử là reset hoàn toàn" | YouTube còn dựa vào lượt thích và hoạt động Google; TikTok "Làm mới" chỉ tác động bảng tin Đề xuất và không hoàn tác được | [20][11] |
| "YouTube nói đề xuất chiếm phần lớn lượt xem" | Nguyên văn: "a significant amount … even more than channel subscriptions or search" | [7] |
| "TikTok Việt Nam có X triệu người dùng" (một con số) | Một bài trên cổng mst.gov.vn (07/2024) ghi 3 con số khác nhau từ nguồn thứ cấp → không dùng | [25] |

---

## 7. Gợi ý phát âm cho TTS (`say` trong spec)

| Chữ gốc | Gợi ý đọc | Chữ gốc | Gợi ý đọc |
|---|---|---|---|
| Netflix | Nét-phlích | BellKor's Pragmatic Chaos | Ben-co Prắc-ma-tích Kê-ọt |
| The Ensemble | Đơ An-xam-bồ | TikTok / YouTube | Tíc-tóc / Diu-túp |
| jazz | giát | Wimbledon | Uim-bồn-đần |
| Cristos Goodrow | Crít-tốt Gút-râu | Google | Gu-gồ |
| RecSys | Réc-xít | IMDb | Ai-em-đi-bi |
| Manoel Horta Ribeiro | Ma-nu-eo Óc-ta Ri-bây-rô | PNAS | Pi-en-ây-ét |
| Meta / Facebook / Instagram | Mê-ta / Phây-búc / In-xta-gram | Science | Xai-ần |
| Texas / Brazil | Tếch-xát / Bra-xin | follow | phô-lô |

Thử giọng trước: "BellKor's Pragmatic Chaos", "The Ensemble", "Wimbledon", "Horta Ribeiro", "IMDb"; "8,43" (đã cắt khỏi bản 1 — nếu đưa lại),
"2,5" = "hai phẩy năm"; "1998" = "một nghìn chín trăm chín mươi tám".

---

## 8. Đóng gói

**Tựa (3 phương án cho Test & Compare):**
1. *Thuật Toán Đề Xuất: Vì Sao TikTok Và YouTube Biết Bạn Thích Gì?* (tựa chính)
2. *AI Đoán Bạn Thích Gì Như Thế Nào? Từ Cuộc Thi 1 Triệu Đô Của Netflix Tới TikTok*
3. *Bạn Chưa Nói Gì, Thuật Toán Đã Biết: Cách Dạy Lại Bảng Tin TikTok, YouTube*

**Thumbnail:** nền lab; một ngón tay cái dừng trên màn hình điện thoại **trống** (không giao diện thật), vạch thời gian sáng "0:00 → dừng"; chữ
lớn **"BẠN CHƯA NÓI GÌ"** + nhỏ "thuật toán đã biết" (PA 1) hoặc ngôi sao vỡ + **"1 TRIỆU ĐÔ… KHÔNG DÙNG"** (PA 2). Không logo TikTok/YouTube/
Netflix làm chủ thể, không mặt người thật.

**Chương YouTube (có từ khoá):** 00:00 Netflix Prize: 20 phút, 1 triệu đô · Lọc cộng tác: máy tìm người giống bạn · Vì sao Netflix không dùng
thuật toán thắng giải · Thuật toán YouTube: từ cú nhấp tới thời gian xem · Thuật toán TikTok: bảng tin Đề xuất chọn video thế nào · Lời giải: điều
bạn làm, không phải điều bạn nói · Hang thỏ YouTube: nghiên cứu nói gì? · Tắt thuật toán thì sao? · Cách dạy lại bảng tin TikTok, YouTube.

**3 Short mồi (cắt từ chính video):**
1. **"Hai mươi phút, một triệu đô"** — chung kết Netflix Prize, hoà tới chữ số thứ tư [1][2]. Rủi ro thấp.
2. **"TikTok tự nói lý do: 'Video này dài hơn và có vẻ như bạn thích những video dài hơn'"** — + cách xem "Tại sao đăng bài này hiển thị" [10][11].
   Rủi ro thấp (kiểm lại tên nút trên app trước khi đăng).
3. **"Tắt thuật toán đi thì sao?"** — thí nghiệm Science 2023 [19]. Rủi ro thấp–trung bình (nói đúng phạm vi: Mỹ, Facebook/Instagram, 3 tháng).

---

## 9. Việc phải làm trước khi khoá kịch bản

1. **Bảng xếp hạng gốc Netflix Prize** (netflixprize.com/leaderboard, Wayback 429 hôm nay): xác nhận thứ tự + thời điểm nộp; nếu có giờ:phút
   chính xác thì có thể đưa lên hình. Lời đọc hiện dựa trên [1] + [2] (khớp nhau).
2. **PNAS 2024 (Hosseinmardi) — phần Methods:** xác nhận cách mô tả bot thứ hai ("đi cùng con đường tới một điểm, rồi chỉ bấm theo đề xuất"),
   và ngữ cảnh "~30 video" (sidebar, người xem thiên lệch chuyển sang ôn hoà).
3. **App thật (Android, tiếng Việt, 10/2026):** tên mục TikTok "Cài đặt và quyền riêng tư → Tùy chọn nội dung → Làm mới bảng tin / Quản lý chủ
   đề / Lọc từ khóa"; thao tác "nhấn giữ → Không quan tâm"; YouTube "⋮ → Không quan tâm / Không đề xuất kênh này", "Quản lý toàn bộ nhật ký".
4. **TikTok Newsroom 2020 + 04/08/2023:** lưu bản thô (newsroom.tiktok.com lỗi DNS từ máy này) — đối chiếu câu [TRÍCH DỊCH] "strong indicator…".
5. **Netflix 2017 (bỏ năm sao)** và **huỷ cuộc thi thứ hai (2010)**: tìm bản gốc (about.netflix.com / blog Netflix) — đang [SECONDARY]; nếu không
   tìm được, cắt câu 2017 (mục cắt (a)) và giữ câu 2010 nhờ Feuerverger 2012.
6. **Boeker & Urman:** xác nhận đơn vị công tác (Đại học Zurich?) → nếu khác, đổi "ở Thuỵ Sĩ" thành "hai nhà nghiên cứu châu Âu".
7. **Science 2023 errata 12/2024**: đọc nội dung (science.org bị Cloudflare chặn script) — nếu chạm tới ba kết luận chính thì sửa ch7.
8. Kiểm chứng (agent): đối chiếu từng [TRÍCH DỊCH] với nguyên văn ở mục 4 (đặc biệt câu TikTok 2020 dịch gọn, câu Covington dịch "clickbait").
9. Cảnh mới cần demo trước khi dàn (retro 2, bước 5): **bảng xếp hạng hai hàng quiz/test** (counter phải đếm từ đầu cảnh — retro 2 mục 3);
   **ma trận sao 99% trống**; **phễu triệu → trăm → chục**; **hai bot tách nhánh**; **menu mô phỏng** (chữ hoa có dấu: "KHÔNG QUAN TÂM",
   "LÀM MỚI BẢNG TIN" — soát gallery dấu).

---

## 10. Nguồn (truy cập 09/10/2026)

1. Netflix, Inc., *Netflix Awards $1 Million Netflix Prize and Announces Second $1 Million Challenge*, PRNewswire, New York, 21/09/2009 (đọc toàn văn, bản lưu PDF): https://www.asc.ohio-state.edu/statistics/statgen/joul_aut2009/NetflixAwardsOneMillionPrize2009.pdf (gốc: http://netflix.mediaroom.com/index.php?s=43&item=327)
2. A. Feuerverger, Y. He, S. Khatri, *Statistical Significance of the Netflix Challenge*, Statistical Science 27(2):202–231, 2012, doi:10.1214/11-STS368 (đọc toàn văn arXiv): https://arxiv.org/abs/1207.5649
3. X. Amatriain, J. Basilico, *Netflix Recommendations: Beyond the 5 stars (Part 1)*, Netflix Technology Blog, 06/04/2012 (đọc toàn văn): https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429
4. A. Narayanan, V. Shmatikov, *Robust De-anonymization of Large Sparse Datasets*, IEEE Symposium on Security and Privacy 2008; arXiv cs/0610105 (đọc tóm tắt): https://arxiv.org/abs/cs/0610105
5. [SECONDARY] Huỷ Netflix Prize 2, 12/03/2010 (trích blog Neil Hunt): EPIC https://archive.epic.org/2010/03/netflix-cancels-contest-over-p.html ; Infosecurity https://www.infosecurity-magazine.com/news/netflix-cans-anonymous-data-contest
6. [SECONDARY] Netflix bỏ năm sao, 16–17/03/2017: The Fader https://www.thefader.com/2017/03/17/netflix-has-scrapped-its-star-ratings-system
7. C. Goodrow, *On YouTube's recommendation system*, YouTube Official Blog, 15/09/2021 (đọc toàn văn): https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/
8. P. Covington, J. Adams, E. Sargin, *Deep Neural Networks for YouTube Recommendations*, RecSys '16, Boston, 15–19/09/2016 (đọc toàn văn PDF): https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/ (PDF: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf)
9. TikTok Newsroom, *How TikTok recommends videos #ForYou*, 18/06/2020 (đọc qua WebFetch, trích đoạn): https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
10. TikTok Support, *How TikTok recommends content* (EN, đọc bằng trình duyệt 09/10/2026): https://www.tiktok.com/support/faq_detail?id=7655285288050104852&category=web_using_tiktok
11. TikTok Support, *For You* (EN + VI "Đề xuất"), *Refresh your For You feed*, *Manage topics* (đọc 09/10/2026): https://support.tiktok.com/en/using-tiktok/exploring-videos/for-you ; https://www.tiktok.com/support/faq_detail?id=7581820706028296760&category=web_account&lang=vi-VN ; https://support.tiktok.com/en/account-and-privacy/account-privacy-settings/refresh-your-for-you-feed ; https://support.tiktok.com/en/account-and-privacy/account-privacy-settings/manage-topics
12. [SECONDARY] TikTok Newsroom, *An update on fulfilling our commitments under the Digital Services Act*, 04/08/2023 (qua kết quả tìm kiếm; trang lỗi DNS khi mở): https://newsroom.tiktok.com/en-eu/fulfilling-commitments-dsa-update
13. M. Boeker, A. Urman, *An Empirical Investigation of Personalization Factors on TikTok*, Proceedings of the ACM Web Conference 2022, tr. 2298–2309, doi:10.1145/3485447.3512102 (đọc tóm tắt): https://arxiv.org/abs/2201.12271
14. (đã đọc tóm tắt, không dùng trong lời) K. Vombatkere et al., *TikTok and the Art of Personalization: Investigating Exploration and Exploitation on Social Media Feeds*, ACM Web Conference 2024: https://arxiv.org/abs/2403.12410
15. M. H. Ribeiro, R. Ottoni, R. West, V. A. F. Almeida, W. Meira, *Auditing Radicalization Pathways on YouTube*, FAT* '20, tr. 131–141, doi:10.1145/3351095.3372879 (đọc tóm tắt): https://arxiv.org/abs/1908.08313
16. A. Y. Chen, B. Nyhan, J. Reifler, R. E. Robertson, C. Wilson, *Subscriptions and external links help drive resentful users to alternative and extremist YouTube channels*, Science Advances 9(35):eadd8080, 30/08/2023, doi:10.1126/sciadv.add8080 (đọc tóm tắt qua Europe PMC)
17. M. Haroon et al., *Auditing YouTube's recommendation system for ideologically congenial, extreme, and problematic recommendations*, PNAS 120(50):e2213020120, 05/12/2023, doi:10.1073/pnas.2213020120 (đọc tóm tắt qua Europe PMC)
18. H. Hosseinmardi, A. Ghasemian, M. Rivera-Lanas, M. Horta Ribeiro, R. West, D. J. Watts, *Causally estimating the effect of YouTube's recommender system using counterfactual bots*, PNAS 121(8):e2313377121, 13/02/2024, doi:10.1073/pnas.2313377121 (đọc tóm tắt): https://arxiv.org/abs/2308.10398
19. A. M. Guess et al., *How do social media feed algorithms affect attitudes and behavior in an election campaign?*, Science 381(6656):398–404, 27/07/2023, doi:10.1126/science.abp9364 (đọc tóm tắt qua Europe PMC, PMID 37498999); errata doi:10.1126/science.adu8261 (05/12/2024, chưa đọc), doi:10.1126/science.aeh2575 (19/03/2026, [SECONDARY])
20. YouTube Help 6342839, *Manage your recommendations & search results* (EN + VI, Android, đọc 09/10/2026): https://support.google.com/youtube/answer/6342839?hl=vi&co=GENIE.Platform%3DAndroid
21. YouTube Help 95725, *View, delete, or turn on or off watch history* (Android, đọc 09/10/2026): https://support.google.com/youtube/answer/95725?hl=en&co=GENIE.Platform%3DAndroid
22. Báo Điện tử Chính phủ, *Sẽ kiểm tra toàn diện Tiktok trong tháng 5 tới*, 06/04/2023: https://baochinhphu.vn/se-kiem-tra-toan-dien-tiktok-trong-thang-5-toi-102230406173207889.htm
23. Báo Điện tử Chính phủ, *Kết quả kiểm tra toàn diện hoạt động của Tiktok tại Việt Nam*, 05/10/2023: https://baochinhphu.vn/ket-qua-kiem-tra-toan-dien-hoat-dong-cua-tiktok-tai-viet-nam-102231005164335301.htm
24. [SECONDARY] VnEconomy, *Phát hiện TikTok có nhiều sai phạm tại Việt Nam* (Nam Anh, 06/06/2023; Thứ trưởng Nguyễn Thanh Lâm, họp báo 05/06): https://vneconomy.vn/phat-hien-tiktok-co-nhieu-sai-pham-tai-viet-nam.htm
25. (không dùng số) Cổng TTĐT Bộ KH&CN, *Lành mạnh hoá mạng xã hội TikTok, bảo vệ chủ quyền không gian mạng*, 04/07/2024: https://mst.gov.vn/lanh-manh-hoa-mang-xa-hoi-tiktok-bao-ve-chu-quyen-khong-gian-mang-197240704092432398.htm
26. Wikimedia Commons API (`generator=search`, `prop=imageinfo&iiprop=extmetadata|size|mime`), 09/10/2026: https://commons.wikimedia.org/w/api.php
27. Pexels Videos API qua `motion/long/pexels.py search` (09/10/2026), chỉ mục: `output/long/mim-ai-feed/broll/index.json`
28. Nội bộ: `docs/channels/mind-in-the-machine/2026-10-06-topic-research.md` (§2, §3.1 #6), `2026-10-07-long-04-research.md` + `data/long/mim-ai-hallucinate/` (khuôn), `motion/long/RETENTION.md`, `docs/pm/2026-10-07-retro-2.md`
