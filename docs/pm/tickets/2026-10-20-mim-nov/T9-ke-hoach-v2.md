# T9 v2 — 8 Short truyện có người, gắn Long `mim-may-choi-game` (Long lên Thứ Năm 03/12/2026 20:00)

Bản 2, 20/10/2026, thay `T9-ke-hoach.md` (bản số/cơ chế, bị chủ kênh chê "chưa hấp dẫn"). Pha 1: chỉ viết file; chưa dựng, chưa đăng, không sửa `state.sqlite`, `data/stier/specs` hay ticket khác. Spec ở `specs-v2-T9/` (8 file JSON). Khuôn theo `MAU-DA-DUYET-mim-nvidia-quan-an-dem.json` và `docs/pm/2026-10-20-mim-short-engagement-research.md`: mở bằng người/sự kiện, 8–9 cảnh, 25–34 giây (ước), bước ngoặt, câu cuối kết vòng về câu mở, không rào đón.

## 0. Kết luận ngắn

- **Đủ 8 bài, mỗi bài một người thật + sự kiện có ngày + bước ngoặt.** Bỏ cả hai bài yếu cũ ("năm máy không ai ra lệnh", "Atari không dạy luật") và các bài cơ chế (280/678 APM, mười mũ hai sáu, 200 năm/14 ngày). Atari quay lại dưới dạng truyện Hassabis/Google 2014 → đường hầm Breakout 2015.
- **Lịch:** 8 slot "T9 game" trong `00-LICH-XEN-KE.md` là 11:30 từ 27/11 đến 04/12 (bản 1 xếp nhầm vào 01–03/12). Short 03/12 11:30 lên trước Long 20:00; 04/12 lên sau Long (nối bằng "Video liên quan").
- **Số liệu tự mở nguồn (DeepMind 24/01/2019, 30/10/2019, các trang Wikipedia, Vice, Google Research):** xem từng bài. **Không mở được:** openai.com (HTTP 403 mọi đường dẫn), Quartz, Engadget, The Verge, TechXplore (451), GamesBeat. Những chỗ chỉ dựa vào tóm tắt tìm kiếm ghi "CẦN KIỂM" (mục 4); bài rủi ro nhất là #4 (khán giả chọn tướng) và #5 (số 7.215/42).
- **Lỗi trong Long CH20 (không dùng):** "42.729 ván, thắng 99,4%" gộp hai thứ. Theo ghi chú nguồn của script (tweet OpenAI 22/04/2019 qua Engadget), 99,4% chỉ là ván đối đầu (7.215 thắng, 42 thua, tổng 7.257); 35.466 là ván hợp tác; 7.257 + 35.466 = 42.723, lệch 6 so với 42.729. Bài #6 chỉ dùng "7.215 thắng, 42 thua" (gắn "đối đầu"), không dùng 42.729 và 99,4%. Nên sửa CH20 của Long trước khi dựng Long (ngoài phạm vi ticket này).
- **Tự kiểm kỹ thuật:** nạp `MODE`/`scene_mode`/`mix_lint` từ `motion/stier/build.py` bằng `exec` đoạn mã đó (KHÔNG chạy `build.py`; không có cờ lint-only), dùng thời gian ước (4,2 âm tiết/giây + 0,25 s nghỉ). Cả 8 bài đạt: theme mim, mix true, rules 2, câu mở ≤ 9 chữ (đếm lại sau khi rút gọn 3 câu), lời đọc không chữ số, counter không prefix chữ số, đủ M D G, chữ thuần 7–19% (≤ 35%), không 3 cảnh liền cùng kiểu, không cảnh > 11 s, mọi mốc `[câu,"chữ"]` có trong lời, mọi clip có trong `motion/hf/assets/clips/index.json`. Chưa kiểm được: thời lượng thật sau TTS, nghe thử `say`, hình clip (chưa xem khung nào).

## 1. Lịch (giờ VN; `data/shorts_slots.json` giờ MIM 11:30; chốt lại bằng `scripts/shorts_grid.py` ở pha 2)

| Ngày | Giờ | Slug | Trò | Kiểu cảnh (M clip/ảnh, D số, G sơ đồ, T chữ) |
|---|---|---|---|---|
| T6 27/11 | 11:30 | `mim-game-dendi-2017` | Dota | M D T G D M T G M |
| T7 28/11 | 11:30 | `mim-game-tlo-thua-roi-viet-luat` | StarCraft | M G D M G D M T |
| CN 29/11 | 11:30 | `mim-game-khan-gia-chon-tuong-hai-may` | Dota | M D G D M G T M D |
| T2 30/11 | 11:30 | `mim-game-google-mua-atari-2014` | Atari | M D G M D G M M T |
| T3 01/12 | 11:30 | `mim-game-mana-thua-nam-van-roi-thang` | StarCraft | M G D M G T D M T |
| T4 02/12 | 11:30 | `mim-game-alpha-red-tran-thang-dau` | Dota | M D G M D T G D M |
| T5 03/12 | 11:30 | `mim-game-tai-khoan-an-danh-grandmaster` | StarCraft | M D G M G D G T |
| T6 04/12 | 11:30 | `mim-game-og-thua-may-roi-vo-dich` | Dota | M G D D M T D G M |

Ghi chú: ngày thứ trong tuần theo lịch 2026 (27/11 là thứ Sáu); cột "T" chỉ để dễ đọc, giờ chốt theo lịch xen kẽ. Hai bài kề nhau khác trò hoặc khác kiểu mở (Dota/StarCraft/Atari luân phiên, không có hai bài StarCraft liền). Alpha Red (02/12) nhắc OG thắng/ thua máy; OG (04/12) kể trọn chuyện đó, nên OG nên lên sau Alpha Red. Nếu chủ kênh muốn OG sát Long hơn, hoán 03/12 ↔ 04/12 (Grandmaster ra sau Long). 60/40: 5 bài SỰ KIỆN CÓ NGÀY (#1, #3, #4, #6, #7), 3 bài THỬ khuôn truyện (#2 Atari/Google, #5 Alpha Red, #8 Benchmark).

Mô tả mỗi Short kết bằng "Bản đầy đủ: https://youtu.be/0J3dcjPjcdI (công khai từ 20:00 ngày 03/12)" và câu "Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện." (đã có sẵn trong spec). Lời đọc không mời xem Long.

## 2. Từng bài

### #1 `mim-game-dendi-2017` (27/11)
- **Câu mở (9 chữ):** "Dendi thua cỗ máy trên sân khấu lớn nhất."
- **Nhân vật:** Dendi (tên thi đấu của một tuyển thủ Dota người Ukraine; không nêu tên đời thường), cùng SumaiL, Arteezy (thua bot trong tuần ấy).
- **Sự kiện có ngày:** tháng 08/2017, The International 2017 (bài OpenAI "Dota 2" đề ngày 11/08/2017; lời đọc chỉ ghi "tháng tám", không ghi ngày).
- **Bước ngoặt:** người nổi tiếng nhất làng Dota ngồi xuống và thua một bot chỉ tự chơi với chính nó; một năm sau OpenAI mang tới năm cỗ máy; câu chốt quay về câu mở "Dendi thua một cỗ máy, và nó chưa biết đồng đội là gì."
- **Số + nguồn:** không số lớn; "một chọi một", "tuần ấy bot thắng SumaiL, Arteezy", "tự chơi với chính mình". Đã mở: Wikipedia OpenAI Five (Dendi, Ukraine, thua bot 1v1 tại TI 2017, 08/2017). **Chưa mở được:** https://openai.com/index/dota-2 (403), https://qz.com/1052409/ (403): câu SumaiL/Arteezy và "không dùng bắt chước hay cây tìm kiếm" dựa tóm tắt tìm kiếm → CẦN KIỂM. Không dùng lời "This guy is scary" (chưa có nguồn mở được) và không nói Dendi "bỏ cuộc giữa ván".
- **Không trùng:** xem mục 3 (không Short nào về Dota/Dendi).

### #2 `mim-game-tlo-thua-roi-viet-luat` (28/11)
- **Câu mở (8 chữ):** "TLO thua năm ván, rồi ngồi viết luật."
- **Nhân vật:** Dario "TLO" Wünsch, người Đức, chuyên Zerg nhưng chơi Protoss cho thí nghiệm.
- **Sự kiện có ngày:** cuối 2018 (5–0 trước AlphaStar, ghi hình); 30/10/2019 (bản mới, giới hạn do TLO cùng đặt).
- **Bước ngoặt:** người thua đầu tiên thành người cùng viết luật hạn chế cỗ máy: 22 hành động mỗi 5 giây, nhìn qua khung màn hình; nhận xét "không còn cảm giác siêu nhân". Kết vòng "Người thua năm ván, giờ là người viết luật."
- **Số + nguồn (đã mở):** DeepMind 24/01/2019 https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/ (TLO 5–0; lời TLO "ngạc nhiên vì cỗ máy mạnh"); DeepMind 30/10/2019 https://deepmind.google/discover/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/ (22 hành động mỗi 5 giây, camera, TLO cộng tác giao diện và giới hạn, lời "doesn't feel superhuman"); TechCrunch 24/01/2019 https://techcrunch.com/2019/01/24/starcraft-ii-playing-ai-alphastar-takes-out-pros-undefeated/ (TLO chơi Zerg, thử Protoss). Lời đọc diễn đạt lại, không trích nguyên văn.
- **Lưu ý:** "chuyên Zerg" lấy từ TechCrunch/script; blog DeepMind không nêu.

### #3 `mim-game-khan-gia-chon-tuong-hai-may` (29/11)
- **Câu mở (8 chữ):** "Khán giả chọn tướng để hại cỗ máy."
- **Nhân vật:** Blitz cùng bốn người chơi hàng đầu (Cap, Fogged, Merlini, MoonMeander; lời đọc chỉ nêu Blitz) và khán giả khoảng 100 nghìn người.
- **Sự kiện có ngày:** 05/08/2018, San Francisco, OpenAI Five Benchmark.
- **Bước ngoặt:** máy thắng hai ván đầu; ván ba khán giả được chọn tướng cho máy, cố ý chọn đội hình dở, và con người thắng (máy thắng loạt 2–1). Kết: khán giả vẫn hạ được nó một ván.
- **Số + nguồn:** 05/08/2018, 2–1, chọn tướng, ~100.000 người xem: https://openai.com/index/openai-five-benchmark-results (403 khi mở) + PC Gamer/techxplore qua tìm kiếm; Wikipedia OpenAI Five (đã mở) chỉ xác nhận "thắng cựu tuyển thủ ngày 06/08/2018". **CẦN KIỂM trước khi dựng; nếu không kiểm được, bỏ bài (dự phòng D1).**

### #4 `mim-game-google-mua-atari-2014` (30/11)
- **Câu mở (9 chữ):** "Google mua một công ty dạy máy chơi Atari."
- **Nhân vật:** Demis Hassabis (cùng Shane Legg, Mustafa Suleyman).
- **Sự kiện có ngày:** 26/01/2014 Google xác nhận mua DeepMind (giá theo báo chí 400–650 triệu USD; lời đọc "được đồn tới ... triệu đô"); 25/02/2015 công bố DQN trên Nature.
- **Bước ngoặt:** công ty bán chỉ vì một hệ thống chơi Atari; hơn một năm sau nó tự đào đường hầm ở Breakout, không ai dạy luật. Kết: "Công ty dạy máy chơi Atari, và cỗ máy ấy tự tìm ra đường hầm."
- **Số + nguồn (đã mở):** Wikipedia DeepMind (26/01/2014; 400–650 triệu USD "reportedly"; Hassabis nói bắt đầu bằng trò Atari thập niên 70–80; ba người lập) https://en.wikipedia.org/wiki/DeepMind ; blog Google Research/DeepMind 25/02/2015 https://research.google/blog/from-pixels-to-actions-human-level-control-through-deep-reinforcement-learning/ (pixel + nút + điểm; đường hầm Breakout). Lời đọc không khẳng định mua vì Atari (chỉ đặt hai sự việc cạnh nhau). Không dùng số "600 ván" (chỉ báo chí).
- **Khác bài "Atari không dạy luật" cũ:** có người, có thương vụ có ngày, bước ngoặt là đường hầm.

### #5 `mim-game-mana-thua-nam-van-roi-thang` (01/12)
- **Câu mở (8 chữ):** "MaNa thua năm ván, rồi thắng cỗ máy."
- **Nhân vật:** Grzegorz "MaNa" Komincz, người Ba Lan, chuyên Protoss.
- **Sự kiện có ngày:** 19/12/2018 (5–0 trước máy; lời đọc "tháng mười hai"); cuối 01/2019 ván trực tiếp với bản mới nhìn qua khung màn hình, luyện bảy ngày; 30/10/2019.
- **Bước ngoặt:** MaNa thắng; chín tháng sau anh nói các giới hạn mới khiến ván đấu đáng xem. Kết: "Anh thua năm ván, và thắng khi cỗ máy phải nhìn như người."
- **Số + nguồn (đã mở):** DeepMind 24/01/2019 (MaNa 5–0 ghi hình 19/12; ván biểu diễn MaNa thắng bản camera luyện 7 ngày); DeepMind 30/10/2019 (lời MaNa về giới hạn); TechCrunch 24/01/2019 (bản "human-style" bị MaNa đánh bại). Ngày chính xác của ván trực tiếp (24/01/2019) **chưa có nguồn mở được nói thẳng**, lời đọc chỉ ghi "cuối tháng một". Không kể chiến thuật MaNa dùng (Escapist/Reddit chỉ qua tìm kiếm, không mở được).
- **Không dùng khung "ván duy nhất người thắng"** (đã dùng ở `mim-teaser-nuoc-78`).

### #6 `mim-game-alpha-red-tran-thang-dau` (02/12)
- **Câu mở (9 chữ):** "Mở cửa vài giờ, con người thắng trận đầu."
- **Nhân vật:** đội chuyên nghiệp Alpha Red (Thái Lan); Greg Brockman (đồng sáng lập OpenAI) và một tuyển thủ Thụy Điển (Wagamama, lời đọc không nêu tên).
- **Sự kiện có ngày:** 18/04/2019, OpenAI mở Arena cho mọi người đấu OpenAI Five; năm ngày sau trận thắng OG (13/04/2019).
- **Bước ngoặt:** vài giờ sau khi mở cửa, Alpha Red thắng một ván khoảng 45 phút; Brockman viết "First human victory"; tuyển thủ nói máy không học nữa, còn người thì có. Kết: máy thắng bảy nghìn hai trăm mười lăm ván đối đầu, thua bốn mươi hai, nhưng trận thua đầu đến chỉ sau vài giờ.
- **Số + nguồn:** Vice/Motherboard 19/04/2019 https://vice.com/en/article/we-will-win-openais-dota-2-team-is-crushing-humans-online-but-players-are-not-giving-up (**đã mở**: Alpha Red, Thái Lan, ~45 phút, tweet Brockman, lời Wagamama). 7.215 thắng/42 thua: tweet OpenAI 22/04/2019 qua Engadget https://www.engadget.com/2019-04-23-openai-five-dota-2-arena-results.html (**không mở được**, qua tìm kiếm) → CẦN KIỂM. Vice còn ghi tại thời điểm viết bot đã thua 9 ván, nên câu "trận thua đầu tiên" **chỉ gắn với lời Brockman** và "vài giờ sau khi mở cửa"; nếu OpenAI/Engadget cho thấy trận thua đầu là ván khác, đổi câu 9 thành "Nhưng người đã thắng chỉ sau vài giờ".

### #7 `mim-game-tai-khoan-an-danh-grandmaster` (03/12, trước Long)
- **Câu mở (8 chữ):** "Một tài khoản ẩn danh leo bảng xếp hạng."
- **Nhân vật:** AlphaStar (tài khoản ẩn danh) và các tuyển thủ duyệt luật; lời nhận xét của Diego "Kelazhur" Schwimer (lời đọc không nêu tên).
- **Sự kiện có ngày:** giữa 2019 (từ 07/2019) trên bảng xếp hạng châu Âu; cuối 08/2019 lên Grandmaster; 30/10/2019 công bố trên Nature.
- **Bước ngoặt:** điều kiện như người (camera, giới hạn hành động, ba chủng tộc) mà vẫn lên hạng cao nhất, trên khoảng 99,8% người chơi có hạng; "tài khoản ẩn danh ấy hóa ra là AlphaStar".
- **Số + nguồn (đã mở):** DeepMind 30/10/2019 (Grandmaster cả ba chủng tộc, trên 99,8% trên Battle.net, ẩn danh, 22 hành động/5 giây, chuyên gia duyệt, lời Kelazhur); Wikipedia AlphaStar (từ 07/2019 ẩn danh; cuối 08/2019 Grandmaster; ghi "top 0,2%", khớp 99,8%). **Không nói "đối thủ không biết đang đấu máy"** (Wikipedia: người chơi đồng ý tham gia).
- **Chồng nhẹ** với #2 và #5 (cùng nguồn 30/10/2019): khác nhân vật chính và khác bước ngoặt; không nhắc con số 22 ở lời đọc.

### #8 `mim-game-og-thua-may-roi-vo-dich` (04/12, sau Long)
- **Câu mở (8 chữ):** "Nhà vô địch thua máy, rồi lại vô địch."
- **Nhân vật:** đội OG (N0tail, JerAx, Topson, Ceb, Ana; lời đọc chỉ nói "OG").
- **Sự kiện có ngày:** 05/2018 thay ba thành viên, đi từ vòng loại mở; 08/2018 Vancouver, vô địch The International (3–2 trước PSG.LGD, hơn 11 triệu USD); 13/04/2019 San Francisco, thua OpenAI Five; 20–25/08/2019 Thượng Hải, thắng Team Liquid 3–1, đội đầu tiên vô địch TI hai lần.
- **Bước ngoặt:** nhà vô địch thua máy rồi vô địch thêm lần nữa. Kết: "Thua máy một lần, rồi vô địch thêm một lần nữa."
- **Số + nguồn (đã mở):** Wikipedia OG https://en.wikipedia.org/wiki/OG_(esports) ; The International 2018 https://en.wikipedia.org/wiki/The_International_2018 ; The International 2019 https://en.wikipedia.org/wiki/The_International_2019 ; ngày 13/04/2019 theo Wikipedia OpenAI Five + TechCrunch 15/04/2019 (qua Long CH19). Lời đọc **không** nêu tỉ số trận với máy và **không** nêu "OG thua hai ván" (Wikipedia OG chỉ ghi OG lost).
- Bài sát Long nhất (CH19); nếu ưu tiên tease Long, hoán sang 03/12.

## 3. Bảng đối chiếu trùng

Phương pháp: `state.sqlite` mở `mode=ro` (bảng `item`: 160 Short MIM, `publish_at` 08/10 → 12/11; chỉ có slug, không có nội dung) + quét toàn bộ 161 `data/stier/specs/mim-*.json` và `data/long/mim-*/script.md` (trừ Long này) với các từ khoá AlphaStar, StarCraft, Dota, OpenAI Five, Atari, DQN, MaNa, TLO, Dendi, Breakout, esports: **0 trùng**. Quét riêng DeepMind/Hassabis/Atari/2014/OG: chỉ gặp chuyện cờ vây và CAPTCHA/Flappy.

| Bài | Short/ticket gần nhất | Giống | Khác | Mức |
|---|---|---|---|---|
| #1 Dendi | `mim-gpu-dgx1-openai-2016` (T4; OpenAI 2016) | nhắc OpenAI | T4 nói siêu máy tính DGX-1, #1 nói trận Dota 2017 | thấp |
| #1, #3, #6, #8 | `mim-noam-brown-nghi-lau-hon`, `mim-chatgpt-700-trieu`, `mim-bo-xac-thuc-giong-noi` | chỉ chung tên OpenAI | khác sự kiện | không |
| #2, #5, #7 | `mim-teaser-nuoc-78`, `mim-nghiep-du-thang-may-14-15`, `mim-con-nguoi-danh-hay-len` (cờ vây) | "người thắng/đứng cạnh máy" | khác trò, khác người, không dùng "ván duy nhất" | thấp |
| #4 Atari/Google | `mim-alphago-30-trieu-nuoc-co` (sub "DEEPMIND · 2014–2016") | nhắc DeepMind | kia nói cách học AlphaGo; #4 nói thương vụ Google và Breakout | thấp |
| #2, #5, #7 | nhau (cùng blog 30/10/2019) | luật hạn chế AlphaStar | mỗi bài một người và một bước ngoặt khác | trung bình (nên cách ≥ 2 ngày, đã làm) |
| #3, #6 | `mim-watson-tieng-chuong` (T5) | "máy có công bằng không" | không bàn chuông/độ trễ | thấp |
| T5, T7, T8 mới (`T5/T7/T8-ke-hoach.md`) | Watson, poker (Pluribus, Libratus...), khuôn mặt | | không bài nào về trò chơi điện tử | không |
| T6 (`T6-ke-hoach.md`) | OpenAI chính sách dữ liệu | chung tên OpenAI | khác hẳn | không |
| T4 (`T4-ke-hoach.md` dòng 92) | "T9 có OpenAI Five (2018–2019) — khác sự kiện" | | #1 (2017), #3 (08/2018), #6 (04/2019), #8 (OG) không nhắc DGX-1/GPU | không |

Các số khổng lồ ("N chữ số", 10^26), 200 năm/14 ngày và 280/678 APM **đã bỏ** để tránh họ "số có N chữ số" và khuôn cơ chế.

## 4. Cần kiểm (không bịa)

1. **openai.com trả 403** với mọi trang (Dota 2, Benchmark results, TI 2018 results, Defeats world champions). Dendi/SumaiL/Arteezy (#1), 2–1 + khán giả chọn tướng + ~100.000 người xem (#3) và 7.215/42 (#6) đang dựa vào tóm tắt tìm kiếm, PC Gamer, Engadget qua tìm kiếm. Đọc lại bằng trình duyệt trước khi dựng. Nếu #3 không kiểm được thì thay bằng D1.
2. **#5:** ngày 24/01/2019 của ván trực tiếp; kiểm "MaNa thắng" bằng một nguồn nêu rõ ngày (lời đọc hiện chỉ ghi "cuối tháng một").
3. **#2:** "chuyên Zerg" (TechCrunch/script); nếu không muốn nhờ nguồn ngoài thì bỏ cụm này.
4. **#6:** thứ tự "trận thua đầu tiên" (xem trên); "Thụy Điển" (Wagamama) lấy từ Vice, đã mở.
5. **#8:** "thay ba thành viên" (TI 2018 Wikipedia) so với Wikipedia OG nêu Fly và s4 rời, ana, Ceb, Topson vào; đã chọn cách nói "thay ba thành viên".
6. **Clip:** 20 ID Pexels chọn theo tên trong `index.json`, **chưa xem khung nào**. Kiểm sổ bằng `motion/stier/clips.py get` + soát hình đầu/giữa/cuối; bỏ clip có logo, biển hiệu, tên giải, UI game. Rủi ro cao: `4835514` (máy arcade, #4), `29467292` (arcade, #4), `6651626` (người chơi game, dùng ở #1 và #3), `7579576` (dùng ở #1 và #3: nếu trùng cũng nên thay). Không dùng clip giải đấu `9071004`, `9071003`, `9071005`. `motion/long/clip_sheet.py` chỉ đọc `data/long/<chủ đề>/ch*.json`, chưa chạy được cho Short; chưa ghi `data/variety`.
7. **Tên riêng cần nghe thử (`say`):** "Đen-đi", "Su-meo", "Ác-ti-zi", "Ha-xa-bít", "Brếch-ao", "Ô Gi", "Lích-quịt", "Blít", "Gờ-ran-ma-xtơ", "Nây-chơ".
8. **Mô tả:** các spec dùng `sources` là chuỗi có ghi chú (như bài mẫu), cần dọn nếu `build.py` chỉ chấp nhận URL.

## 5. Dự phòng (đủ nguồn, chưa dùng)

- **D1 (thay #3 nếu không kiểm được):** 22–23/08/2018, OpenAI Five thua cả hai trận tại The International (paiN Gaming, rồi đội cựu tuyển thủ Trung Quốc). Đã mở: Wikipedia TI 2018. Chưa mở: thời lượng 51/45 phút (openai.com). Yếu về nhân vật.
- **D2:** 01/2019, người xem bắt gặp AlphaStar bùng lên 900–1.500 hành động/phút so với trung bình 280; DeepMind làm rõ ngày 29/01/2019; 10 tháng sau luật mới. Số 900/1.500 chỉ có ở blog Alex Irpan (đã mở) và tìm kiếm, **cần kiểm**; chồng với #2.
- **Không dùng được:** tỉ số từng ván TI 2018; chiến thuật của MaNa; "bốn mươi lăm nghìn năm" và các số "thời gian luyện" của OpenAI (chưa có nguồn mở được); hai bài yếu cũ.
