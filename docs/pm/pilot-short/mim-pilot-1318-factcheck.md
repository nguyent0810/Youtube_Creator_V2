# Fact file · MIM pilot hook A/B · 13–18/11/2026

Ngày kiểm: 28/10/2026. Chỉ là hồ sơ dữ kiện cho 6 Short (25–35 s), chưa có kịch bản. Khung: `docs/pm/2026-10-28-pilot-short-hook.md` mục 5.
Cột "Nguồn": URL đã mở trong lần kiểm này, trừ khi ghi "(F.. cũ)". (F.. cũ) là nguồn đã kiểm trong `data/long/mim-ai-*/factcheck.md` nhưng lần này không mở lại được. Nhãn: **SƠ CẤP** = văn bản gốc của tổ chức hoặc tác giả; **[SECONDARY]** = báo chí thuật lại.

## 0. Trùng với Short MIM đã có (`data/stier/specs/mim-*.json`)

| Short đã có (slug) | Dữ kiện đã dùng | Ảnh hưởng tới pilot |
|---|---|---|
| `vall-e-3-giay` (đăng 20/10, 573 view), `teaser-3-giay`, `vall-e-7-nam-nghe` | VALL-E 3 giây, 60.000 giờ, 7.000 người | 14/11: **đã dùng hết** số 3 giây; chỉ nhắc lại, không làm số hook |
| `bo-xac-thuc-giong-noi` (26/10) | OpenAI 15 giây, khuyên bỏ xác thực bằng giọng | 14/11: số 15 giây cũng đã dùng |
| `4-tren-6-dich-vu`, `tai-nguoi-73-phan-tram`, `farid-tieng-khoc`, `cuoc-goi-4-phut`, `teaser-cuoc-goi-4-phut`, `gap-giau-tien`, `goi-video-vai-giay`, `hong-kong-cuoc-hop-gia`, `meo-deepfake-goi-lai`, `teaser-mat-khau-gia-dinh` | Consumer Reports, UCL 73%, DeStefano, Hồng Kông, Bkav, FBI/FTC | 13/11: chưa Short nào nói về **người nổi tiếng bị nhái giọng để quảng cáo** → chủ đề mới |
| `bang-nghe-ai` (đăng 23/10, 180 view), `bang-xemthu-blueprint` | ILO WP140 (2025): 28/29 nghề văn phòng có tiếp xúc; 1/4 việc làm; 3,3% | 15–16/11: **không** dùng lại "1/4 việc làm" hay "28/29" làm hook. Dùng số khác: điểm của **nghề nhập liệu** (WP140), hoặc ILO 2023 (WP96) |
| `oxford-47-phan-tram`, `stanford-22-25-tuoi`, `det-may-viet-nam-ilo`, `co-tong-dai-ai-tra-gia`, `keynes-15-gio`, `teaser-nghich-ly-atm`, `teaser-hinton-x-quang` | Frey–Osborne 47%, Stanford 19%, ILO 2016 dệt may 64–88% | 16/11: tránh các số này |
| (không có) | RecSys 2016, TikTok 18/06/2020, Goodrow 2021, "80 tỉ tín hiệu" | 17–18/11: chưa Short MIM nào dùng. Không có spec nào chứa "TikTok", "RecSys", "For You" |

## 1. 13/11 · Hook A · `ai-voice` · người nổi tiếng bị nhái giọng trong quảng cáo

**Ứng viên 1 (khuyên dùng): Scarlett Johansson × app Lisa AI**

| Dữ kiện | Giá trị chính xác | Nguồn đã mở | Loại | Kết quả |
|---|---|---|---|---|
| Ngày báo đăng | 02/11/2023 (Variety, Ethan Shanfeld) | https://au.variety.com/2023/digital/news/scarlett-johansson-legal-action-ai-app-ad-likeness-11749/ | [SECONDARY] (Variety, báo lớn) | ĐÚNG |
| Ngày quảng cáo bị phát hiện | 28/10/2023 | như trên | [SECONDARY] | ĐÚNG |
| Nơi đăng, độ dài | Quảng cáo **22 giây** trên X (Twitter), của app "Lisa AI: 90s Yearbook & Avatar" | như trên | [SECONDARY] | ĐÚNG |
| Có giọng giả | Mở bằng clip thật hậu trường *Black Widow*, sau đó là ảnh AI giống cô và **một giọng giả bắt chước cô** quảng cáo app | như trên | [SECONDARY] | ĐÚNG |
| Dòng chữ nhỏ trong quảng cáo | "Images produced by Lisa AI. It has nothing to do with this person." | như trên | [SECONDARY] | ĐÚNG |
| Phía Johansson | Người đại diện xác nhận cô **không** là người phát ngôn của app. Luật sư Kevin Yorn: "We do not take these things lightly" [TRÍCH DỊCH: "Chúng tôi không xem nhẹ những chuyện này"], theo đuổi "all legal remedies" | như trên | [SECONDARY] | ĐÚNG |
| Quảng cáo đã gỡ | "appears to have since vanished" | như trên | [SECONDARY] | ĐÚNG (chỉ là "có vẻ đã biến mất") |
| Kết quả pháp lý | Không có trong nguồn | — | — | CHƯA KIỂM ĐƯỢC → không nói "đã kiện thắng" |

**Ứng viên 2 (dự phòng): Tom Hanks × quảng cáo bảo hiểm nha khoa**

| Dữ kiện | Giá trị chính xác | Nguồn đã mở | Loại | Kết quả |
|---|---|---|---|---|
| Lời đăng Instagram | "BEWARE!! There's a video out there promoting some dental plan with an AI version of me. I have nothing to do with it." [TRÍCH DỊCH: "Cẩn thận! Có một video quảng cáo gói bảo hiểm nha khoa dùng một phiên bản AI của tôi. Tôi không liên quan gì tới nó."] | https://www.digitaltrends.com/news/tom-hanks-warns-of-ai-generated-ad-using-his-likeness/ (bài 03/10/2023) | [SECONDARY] | ĐÚNG |
| Ngày đăng | Chủ nhật, tức 01/10/2023 | như trên ("on Sunday") + kết quả tìm kiếm | [SECONDARY] | ĐÚNG (suy từ "Sunday") |
| Có nhái **giọng** không | Hanks chỉ nói "AI version of me". Digital Trends viết "apparently" có công cụ "able to mimic his voice", không nêu nguồn | như trên | [SECONDARY] | CHƯA KIỂM ĐƯỢC → không nói "giọng Tom Hanks" |
| Tên công ty, nơi chạy quảng cáo | Hanks không nêu | như trên | — | Không có |

Không mở được: bài Instagram gốc, Hollywood Reporter (chuyển hướng tollbit), CBS/NBC (403), The Fader, InsideHook, LBC (lỗi DNS).

## 2. 14/11 · Hook B · `ai-voice` · tin nhắn thoại và nhái giọng

| Dữ kiện | Giá trị chính xác | Nguồn | Loại | Kết quả |
|---|---|---|---|---|
| VALL-E cần 3 giây | "with only a 3-second enrolled recording of an unseen speaker"; nộp 05/01/2023 | https://arxiv.org/abs/2301.02111v1 (mở lại) | SƠ CẤP | ĐÚNG (đã dùng ở 3 Short) |
| OpenAI Voice Engine 15 giây | "a single 15-second audio sample", 29/03/2024 | https://openai.com/index/navigating-the-challenges-and-opportunities-of-synthetic-voices/ (F11 cũ; lần này 403) | SƠ CẤP | ĐÚNG theo lần kiểm 07/10 |
| McAfee: tỉ lệ chia sẻ giọng nói | "53% of adults share their speech data online at least once a week" (mạng xã hội, tin nhắn thoại…); Ấn Độ 86% | https://www.boomlive.in/explainers/ai-voice-scam-voice-cloning-mcafee-report-21851 (BOOM, 03/05/2023) | [SECONDARY] | CHƯA KIỂM ĐƯỢC ở nguồn gốc |
| McAfee: mẫu khảo sát | 7.054 người, 7 nước, khảo sát trực tuyến 13–19/04/2023 | như trên | [SECONDARY] | CHƯA KIỂM ĐƯỢC ở nguồn gốc |
| McAfee: con số khác | Một bài khác ghi **43%** (không rõ là toàn cầu hay một nước); "3 giây cho 85% độ khớp", "1/4 từng gặp lừa giọng AI" | chỉ thấy qua kết quả tìm kiếm | [SECONDARY] | CHƯA KIỂM ĐƯỢC |
| Báo cáo gốc | *Beware the Artificial Impostor*, McAfee, 05/2023 | PDF mcafee.com: hết thời gian chờ; BusinessWire 01/05/2023: 403 | SƠ CẤP | CHƯA KIỂM ĐƯỢC |
| Farid: bản sao khá tốt cần dưới 1 phút | "A reasonably good clone can be created with under a minute of audio" (CNN 29/04/2023) | https://edition.cnn.com/2023/04/29/us/ai-scam-calls-kidnapping-cec/index.html (F2 cũ, không mở lại) | [SECONDARY] (lời chuyên gia qua CNN) | ĐÚNG theo lần kiểm 07/10 |
| FBI khuyên hạn chế đăng giọng | "limit online content of your image or voice, make social media accounts private" (PSA 03/12/2024) | https://www.ic3.gov/PSA/2024/PSA241203 (F7 cũ) | SƠ CẤP | ĐÚNG theo lần kiểm 07/10 |

Không có số đáng tin về "một tin nhắn thoại trung bình dài bao nhiêu giây". Đừng bịa số này trong câu mở.

## 3. 15/11 · Hook B · `ai-jobs` · một nghề văn phòng: **nhân viên nhập liệu**

| Dữ kiện | Giá trị chính xác | Nguồn | Loại | Kết quả |
|---|---|---|---|---|
| Tài liệu | *Generative AI and Jobs: A Refined Global Index of Occupational Exposure*, ILO Working Paper 140; Paweł Gmyrek, Janine Berg, Karol Kamiński, Filip Konopczyński, Agnieszka Ładna… (ILO + NASK Ba Lan) | https://webapps.ilo.org/static/english/intserv/working-papers/wp140/index.html (toàn văn HTML) | SƠ CẤP | ĐÚNG |
| Nhập liệu đứng đầu bảng | Phụ lục 1, bảng A1: dòng đầu là "4132 Data Entry Clerks", điểm trung bình **0,70**, SD 0,03, mức 4 (cao nhất) | như trên | SƠ CẤP | ĐÚNG |
| Ý nghĩa điểm | Mỗi việc nhỏ của nghề được chấm 0–100 ("0 = không tự động hoá được, 100 = tự động hoá hoàn toàn"), sau đó quy về 0–1. Mức 4: μ ≥ 0,6 và μ − σ ≥ 0,5, tức "High and consistent GenAI exposure across tasks" | như trên (mục 3.3, bảng 5) | SƠ CẤP | ĐÚNG. **Không** đọc "AI làm được 70% công việc": 0,70 là điểm *khả năng tự động hoá trung bình của các việc*, không phải % thời gian làm việc |
| Các nghề cùng mức 4 | Đánh máy 0,65; kế toán–sổ sách 0,64; thư ký thống kê/tài chính/bảo hiểm 0,64; tính lương 0,61; bán hàng qua tổng đài 0,61 | như trên | SƠ CẤP | ĐÚNG |
| Nghề mức 3 (nếu muốn chọn nghề khác) | Thư ký (chung) 0,58; giao dịch viên ngân hàng 0,58; nhân viên tổng đài thông tin 0,58; lễ tân 0,57 | như trên | SƠ CẤP | ĐÚNG |
| Số nghề được chấm | Bảng A1 có **427** mã nghề 4 chữ số. Đếm lại: mức 4: 13 · mức 3: 38 · mức 2: 44 · mức 1: 17 · tối thiểu: 84 · không tiếp xúc: 231 | như trên (tự đếm bảng A1) | SƠ CẤP | ĐÚNG |
| 13 nghề mức 4, đa số là việc văn phòng | "Among the 13 occupations classified in gradient 4, the majority represent clerical roles, including data entry clerks, typists…" | như trên | SƠ CẤP | ĐÚNG |
| Rào: tiếp xúc ≠ mất việc | Báo chí thuật lại thông cáo: "job transformation, not mass replacement, is the more probable result" | https://nairametrics.com/2025/05/20/one-in-four-jobs-globally-threatened-by-generative-ai-ilo-report/ | [SECONDARY] | ĐÚNG |

Khung B gợi ý: "Nếu bạn làm nhập liệu, trong bảng chấm 427 nghề của ILO năm 2025, nghề của bạn đứng đầu…". Bám đúng chữ "tiếp xúc" và "điểm", không nói "bị thay".

## 4. 16/11 · Hook A · `ai-jobs` · báo cáo có ngày của ILO

Không dùng lại WP140 làm hook, vì `bang-nghe-ai` đã dùng. Khuyên dùng **ILO 2023 (WP96)**.

| Dữ kiện | Giá trị chính xác | Nguồn | Loại | Kết quả |
|---|---|---|---|---|
| Tài liệu | *Generative AI and Jobs: A global analysis of potential effects on job quantity and quality*, ILO Working Paper 96; Gmyrek, Berg, Bescond | https://webapps.ilo.org/static/english/intserv/working-papers/wp096/index.html (toàn văn HTML) | SƠ CẤP | ĐÚNG |
| Ngày | 08/2023 (có bản ghi 21/08/2023) | chỉ thấy qua kết quả tìm kiếm; trang ilo.org lỗi DNS hoặc bị Cloudflare chặn | [SECONDARY] | CHƯA KIỂM ĐƯỢC ngày cụ thể → đọc "tháng 8 năm 2023" |
| Văn phòng là nhóm duy nhất có mức tiếp xúc cao | "only the broad occupation of clerical work is highly exposed… with 24 per cent of clerical tasks considered highly exposed and an additional 58 percent with medium-level exposure" | WP96 như trên | SƠ CẤP | ĐÚNG |
| Các nhóm nghề khác | "the greatest share of highly exposed tasks oscillates between 1 and 4 per cent, and medium exposed tasks do not exceed 25 p[er cent]" | WP96 | SƠ CẤP | ĐÚNG |
| Bổ trợ hơn thay thế | "more likely to be of augmenting work… as opposed to fully automating occupations" | WP96 | SƠ CẤP | ĐÚNG |
| Thu nhập thấp/cao | Tự động hoá: 0,4% việc làm ở nước thu nhập thấp, 5,5% ở nước thu nhập cao; bổ trợ: 10,4% và 13,4% | WP96 | SƠ CẤP | ĐÚNG |
| Phụ nữ | "more than double the share of women potentially affected by automation" | WP96 | SƠ CẤP | ĐÚNG |
| Bản 2025 (WP140) để so | Ngày 20/05/2025; "one in four jobs globally (24%)"; 3,3% ở mức cao nhất (nữ 4,7%, nam 2,4%); "one in three jobs in high-income countries" | WP140 (SƠ CẤP); ngày 20/05/2025 qua Nairametrics [SECONDARY] | SƠ CẤP / [SECONDARY] | ĐÚNG. Thông cáo ghi **25%**, văn bản ghi **24%**. Dùng 24% (văn bản gốc) |
| "AI đã thay việc nào" | Cả hai báo cáo đo **tiếp xúc tiềm năng**, không đếm việc đã mất | WP96, WP140 | SƠ CẤP | Đề bài "công việc nào AI đã thay" **không có số ILO đỡ**. Đổi góc thành "ILO chấm nghề nào chạm AI nhiều nhất" |

OECD: chưa mở nguồn nào trong lần kiểm này. Không dùng.

## 5. 17/11 · Hook A · `ai-feed` · tài liệu có ngày về cách thuật toán chọn video

| Dữ kiện | Giá trị chính xác | Nguồn | Loại | Kết quả |
|---|---|---|---|---|
| Bài báo | Covington, Adams, Sargin (Google), *Deep Neural Networks for YouTube Recommendations*, RecSys '16, 15–19/09/2016, Boston | https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45530.pdf (mở lại PDF, F9) | SƠ CẤP | ĐÚNG |
| Hai vòng: triệu → trăm → chục | Hình 2: "video corpus **millions** → candidate generation → **hundreds** → ranking → **dozens**"; "only a few hundred videos are being scored rather than the millions scored in candidate generation" | như trên | SƠ CẤP | ĐÚNG |
| Quy mô | "one of the largest scale and most sophisticated industrial recommendation systems in existence"; "more than a billion users"; "approximately one billion parameters… trained on hundreds of billions of examples" | như trên | SƠ CẤP | ĐÚNG |
| Thời gian xem hơn tỉ lệ nhấp | "Ranking by click-through rate often promotes deceptive videos that the user does not complete ("clickbait") whereas watch time better captures engagement" | như trên | SƠ CẤP | ĐÚNG |
| TikTok, 18/06/2020 | *How TikTok recommends videos #ForYou*: 3 nhóm yếu tố là tương tác, thông tin video, cài đặt thiết bị/tài khoản | https://newsroom.tiktok.com/how-tiktok-recommends-videos-for-you?lang=en (mở lại) | SƠ CẤP | ĐÚNG |
| TikTok: số follow không phải yếu tố trực tiếp | "neither follower count nor whether the account has had previous high-performing videos are direct factors" | như trên | SƠ CẤP | ĐÚNG |

Lưu ý: chuỗi triệu → trăm → chục đã có trong Long `ai-feed` (script L106–108). Dùng trong Short là để hỗ trợ Long, không phải lặp Short.

## 6. 18/11 · Hook B · `ai-feed` · vì sao feed của bạn khác người bên cạnh

| Dữ kiện | Giá trị chính xác | Nguồn | Loại | Kết quả |
|---|---|---|---|---|
| YouTube lọc từ hàng tỉ video | "Today, our system sorts through **billions of videos** to recommend content tailored to your specific interests." (15/09/2021, Cristos Goodrow) | https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/ (mở lại bằng curl) | SƠ CẤP (lời hãng) | ĐÚNG |
| 80 tỉ tín hiệu | "learning every day from over **80 billion** pieces of information we call signals" | như trên | SƠ CẤP (lời hãng) | ĐÚNG. Phải nói rõ "YouTube tự công bố, 2021" |
| Các tín hiệu chính | "clicks, watchtime, survey responses, sharing, likes, and dislikes" | như trên | SƠ CẤP | ĐÚNG |
| Mỗi người nặng nhẹ khác nhau | "the importance of each signal depends on you" (ví dụ: người hay chia sẻ mọi video thì lượt chia sẻ của họ được tính nhẹ đi) | như trên | SƠ CẤP | ĐÚNG |
| Không có công thức cố định | "doesn't operate off of a 'recipe book'" | như trên | SƠ CẤP | ĐÚNG |
| TikTok: không có một bảng tin chung | "there's no one For You feed"; mỗi bảng tin "unique and tailored to that specific individual" (18/06/2020) | https://newsroom.tiktok.com/how-tiktok-recommends-videos-for-you?lang=en | SƠ CẤP | ĐÚNG |
| TikTok: cài đặt máy được tính nhẹ | Ngôn ngữ, quốc gia, loại thiết bị "receive lower weight" vì người dùng không chủ động bày tỏ là sở thích | như trên | SƠ CẤP | ĐÚNG |
| TikTok: tín hiệu mạnh và yếu | Xem hết một video dài được tính nặng hơn tín hiệu yếu như ở cùng nước với người làm video | như trên + F11 cũ (nguyên văn) | SƠ CẤP | ĐÚNG |
| TikTok 2026: tương tác thường nặng hơn | "user interactions, which may include the time spent watching a video, are generally weighted more heavily than others" | TikTok Support id 7655285288050104852 (F12 cũ, không mở lại) | SƠ CẤP | ĐÚNG theo lần kiểm 09/10 |
| Kiểm tra độc lập | Boeker & Urman (WWW '22): follow ảnh hưởng mạnh nhất, rồi tới thích, rồi tới tỉ lệ xem | https://arxiv.org/abs/2201.12271 (F14 cũ) | SƠ CẤP | ĐÚNG theo lần kiểm 09/10 |

Câu mở B: "Video bạn vừa lướt qua được YouTube chọn từ hàng tỉ video…" là đúng nguồn với YouTube. **Không** gán "hàng tỉ" cho TikTok: TikTok không công bố số này trong các nguồn đã mở. **Không** trộn "hàng tỉ" (2021) với "hàng triệu" (RecSys 2016) trong cùng một câu.

## Đề xuất số dùng cho hook

- **13/11 (A):** 28/10/2023, một quảng cáo 22 giây trên X dùng giọng giả bắt chước Scarlett Johansson; luật sư của cô theo đuổi biện pháp pháp lý (Variety, 02/11/2023).
- **14/11 (B):** "Tin nhắn thoại bạn gửi hôm qua…" + số **3 giây** (VALL-E, arXiv, 01/2023), chỉ làm nền vì đã dùng ở 3 Short. Số mới 53% (McAfee) **chưa kiểm được gốc**, chỉ dùng khi chủ kênh chấp nhận nhãn [SECONDARY].
- **15/11 (B):** "Nếu bạn làm nhập liệu…": ILO 2025 xếp nghề này **đầu bảng**, điểm 0,70/1, cao nhất trong 427 nghề.
- **16/11 (A):** Tháng 8/2023, ILO: văn phòng là nhóm nghề duy nhất có mức tiếp xúc cao, **24%** việc nhỏ ở mức cao, thêm 58% ở mức vừa.
- **17/11 (A):** RecSys, 09/2016, ba kỹ sư Google: **hàng triệu → vài trăm → vài chục** video.
- **18/11 (B):** "Video bạn vừa lướt qua được chọn từ **hàng tỉ** video", học từ **hơn 80 tỉ** tín hiệu (YouTube tự công bố, 15/09/2021).

## Rủi ro

- **Nhái giọng (13/11):** Johansson chỉ có nguồn [SECONDARY] (Variety). Không thấy kết quả vụ kiện, nên chỉ nói "theo đuổi biện pháp pháp lý". Không đọc tên app trong lời thoại (quy tắc "không nêu tên dịch vụ nhân bản giọng" của Long `ai-voice`). Không suy đoán động cơ của ai. Hanks: không nói là "giọng" vì chưa có nguồn chắc.
- **Quy tắc nhà (14/11):** factcheck `ai-voice` §2 ghi "không nêu bao nhiêu giây giọng là 'đủ' cho kẻ gian". Số 3 và 15 giây chỉ được nói là thông số của **mô hình nghiên cứu, chưa mở cho công chúng**. Câu mở B gắn "tin nhắn thoại của bạn" với "đủ để nhái" thì sát ranh hướng dẫn và doạ quá dữ liệu. Nên kết bằng lời khuyên FBI (hạn chế công khai giọng, cúp máy, gọi lại).
- **McAfee:** PDF gốc và BusinessWire không mở được. Các bài thuật lại vênh nhau (53% hay 43%). Chưa đủ chuẩn SƠ CẤP.
- **Ý nghĩa điểm ILO:** đọc 0,70 là "AI làm được 70% công việc của bạn" là **sai**. Đó là điểm trung bình khả năng tự động hoá của các việc nhỏ, dữ liệu chấm ở Ba Lan rồi mở rộng toàn cầu, và chỉ là **tiếp xúc tiềm năng**.
- **Đề bài 16/11 "AI đã thay":** cả ILO 2023 lẫn 2025 đều không đếm việc đã mất. Phải đổi khung câu.
- **Ngày ILO:** ngày 20/05/2025 và 08/2023 chỉ có qua nguồn phụ (ilo.org chặn). Đọc "tháng 5/2025" và "tháng 8/2023" là an toàn.
- **Lặp chủ đề:** `bang-nghe-ai` (23/10) đã dùng WP140, nên 15/11 phải dùng số nghề cụ thể, không dùng "1/4". 14/11 đã dùng hết 3 và 15 giây ở 3 Short. Biến hook B có thể bị lẫn với hiệu ứng "đã xem rồi".
- **Số do hãng tự công bố** (80 tỉ tín hiệu, hàng tỉ video, TikTok 2020) phải ghi nhãn "theo YouTube / theo TikTok" trên hình và trong mô tả.
