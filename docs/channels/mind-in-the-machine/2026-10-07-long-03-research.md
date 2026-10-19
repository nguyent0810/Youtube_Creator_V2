# Nghiên cứu video dài #3 — Mind in the Machine (MIM) — 07/10/2026

**Phạm vi:** chọn đề tài cho video dài thứ ba (16:9, 12–15 phút, tiếng Việt, faceless, giọng TTS Hải Đăng + motion graphics + ảnh mở,
theme "lab") và lập hồ sơ dữ kiện có nguồn. Phải **khác loại** với #1 *"AI đã chết hai lần"* (lịch sử, `data/long/mim-ai-70`) và #2
*"AI có cướp việc của bạn?"* (kinh tế việc làm, `data/long/mim-ai-jobs`). Áp dụng `motion/long/RETENTION.md` (cold open, cung A → B,
**lộ trình đổi hình thức** — #1 dùng "ba câu hỏi", #2 dùng "ba chặng đường"), `motion/long/RESEARCH-million-views.md` (Test & Compare 3 tựa,
chương có từ khoá, không bạo lực trong tựa/thumbnail) và quy trình retro sprint 1 (`docs/pm/2026-10-06-retro-1.md`: hồ sơ → kịch bản →
kiểm chứng → dàn cảnh; số tự tính đối chiếu ≥ 3 mốc).

**Kịch bản đi kèm:** `data/long/mim-ai-voice/script.md` (bản 1, chờ agent kiểm chứng).

**Phương pháp:**
- Đọc trực tiếp bằng curl/WebFetch khi mở được: bài báo khoa học (arXiv, PLOS ONE), văn bản chính phủ (FBI IC3, FCC, Hội đồng Lập pháp
  Hồng Kông), tổ chức tiêu dùng (FTC, Consumer Reports), báo chí (CNN, VietNamNet, VnEconomy). Không mở YouTube, không cào YouTube/
  Google Trends, không khoá API, không tải media.
- Trang **chặn script** hôm nay: judiciary.senate.gov (403 Akamai, cả khi tắt sandbox), web.archive.org (429), openai.com (DNS/403),
  ossoff.senate.gov, govinfo (500), gizmodo (403). Các mục dựa vào những trang này ghi rõ "đọc qua chỉ mục tìm kiếm".
- Wikimedia Pageviews REST API (vi.wikipedia, `user`, 09/07 → 06/10/2026) và Commons API (`generator=search`, 40 kết quả đầu, đọc
  `LicenseShortName`). User-Agent `yt-factory-research/1.0 (https://github.com/nguyent0810/Youtube_Creator_V2)`, giãn ~1 giây.
- **Nhãn dữ kiện:** **[bằng chứng]** = đã đọc tận nguồn gốc/chính thức hôm nay · **[SECONDARY]** = qua báo/blog/tóm tắt/chỉ mục tìm kiếm,
  chưa mở bản gốc · **[CHƯA KIỂM]** = chưa đủ tin, không đọc lên. Trích nguyên văn giữ ngôn ngữ gốc, kèm nguồn + ngày; với bài báo có bản
  quyền chỉ trích cụm ngắn. Số `[n]` trỏ tới mục 10.

---

## 1. Tóm tắt

- **Chọn: "Mẹ ơi, cứu con!" — lừa đảo giả giọng người thân bằng AI** (slug `mim-ai-voice`). Trục A "AI dễ hiểu" + mẹo dùng được ngay;
  cầu nối B qua lịch sử máy biết nói (Kempelen 1770–1791 → Voder 1939 → máy IBM hát "Daisy Bell" 1961).
- **Vì sao (3 dòng):**
  1. *Nhu cầu Việt:* lừa đảo deepfake là một trong **ba nỗi lo AI lớn nhất** của người Việt (`2026-10-06-topic-research.md` §1–2), mất việc
     đã làm ở #2; khảo sát NCA: năm 2024 cứ ~220 người thì 1 người là nạn nhân lừa đảo trực tuyến, Bộ Công an ước thiệt hại 11 tháng 2025
     **> 6.000 tỉ đồng** [16][17]. Wikipedia yếu ("Deepfake" chỉ 16 lượt/ngày) → đóng gói bằng từ người lớn tự gõ: "AI", "giả giọng", "lừa đảo".
  2. *Cold open + cảnh mạnh thứ hai có nguồn gốc:* cuộc gọi bốn phút của Jennifer DeStefano (CNN 29/04/2023 + lời khai Thượng viện
     13/06/2023) [1][2]; vụ họp video giả 200 triệu HKD ở Hồng Kông, được chính quyền Hồng Kông mô tả trong trả lời Hội đồng Lập pháp [9].
  3. *Người xem áp dụng được ngay và chia sẻ cho bố mẹ:* FBI khuyên đặt **"secret word or phrase"** cho gia đình + cúp máy gọi lại số đã biết
     [4]; FTC cùng ý [5]. Khác loại với #1 (lịch sử) và #2 (kinh tế): đây là video **an toàn cá nhân**, có hành động cụ thể tối nay.
- **Lộ trình — hình thức "Lời thách"** (không lặp "ba câu hỏi" của #1, "chặng đường" của #2): *"Để bắt chước giọng một người lạ, một cỗ máy
  cần nghe người ấy nói bao lâu? Một giờ? Mười phút? Hay một phút? Giữ con số ấy — chỉ vài phút nữa bạn sẽ biết."* → đáp: **ba giây** (VALL-E) [6].
- **Mô-típ:** (a) "A mother knows her child" — cold open (ý), ch4 (trích), kết (trả lại); (b) **máy đội lốt người**: cỗ máy đánh cờ có người
  giấu bên trong (1770) → giọng người mà bên trong là máy (2026); (c) chuông **số lạ** (SFX) ở ch0, ch5, ch6.
- **Câu hỏi để lại:** "Nhà bạn đã có mật khẩu gia đình chưa? Đừng viết từ thật — chỉ kể bạn sẽ nói với ai đầu tiên."
- **Đăng đề xuất:** cuối 11 → giữa 12/2026 (sau #2 26/10–09/11), **trước mùa Tết 2027** (Tết 06/02/2027) — mùa báo chí cảnh báo giả giọng vay
  tiền [topic-research §2]. Ba Short mồi đăng trước 7–10 ngày; Short "mật khẩu gia đình" có thể đăng lại sát Tết.
- **Lệch khỏi gợi ý cũ:** hồ sơ #2 (§2.2) đề xuất "Bên trong ChatGPT" cho #3 dịp ChatGPT 4 tuổi (30/11). Không chọn vì ch6 của #1 đã giải thích
  "đoán mẩu chữ tiếp theo" + Transformer (trùng), 72% lượt xem wiki ChatGPT là desktop (học sinh), và giá trị áp dụng thấp hơn. Video này
  vẫn **callback** ý "đoán mẩu tiếp theo" ở ch2 (VALL-E là mô hình ngôn ngữ trên mẩu âm thanh) — nối kênh mà không lặp.

---

## 2. Ứng viên và bảng điểm

### 2.1. Tín hiệu nhu cầu

**Wikipedia tiếng Việt** (người dùng thật, trung vị/ngày; 90 ngày 09/07 → 06/10/2026 · 28 ngày đầu · 28 ngày cuối; đo hôm nay) [21]:

| Bài | 90 ngày | 28 ngày đầu → cuối | Mobile-web (28 ngày cuối) |
|---|---:|---:|---:|
| Trí tuệ nhân tạo | 361 | 225,5 → 1.097,5 | 302,5 |
| ChatGPT | 378,5 | 374 → 417,5 | 103 |
| Deepfake | 12 | 10 → 16 | 7,5 |
| Ảo giác (trí tuệ nhân tạo) | 6 | 4,5 → 6,5 | 1 |
| Tổng hợp giọng nói | 2 | 2 → 2 | 0 |
| *Lừa đảo* | chưa có bài (404) | | |

→ Wikipedia không đo được nỗi lo lừa đảo (đọc tra cứu ≠ sợ bị lừa). Bằng chứng nhu cầu chính là **dư luận + số liệu chính thức**:
- Khảo sát NCA 2024 (16/12/2024, 59.000 người): 1/220 người dùng là nạn nhân; ước thiệt hại **18.900 tỉ đồng**; **96,64%** bị làm phiền bởi
  cuộc gọi rác [SECONDARY, Tuổi Trẻ / VnEconomy] [16].
- Khảo sát NCA 2025 (01–18/12/2025, 60.300 người): **1/555 (0,18%)**, lần đầu giảm sau nhiều năm; chỉ **32,12%** nạn nhân báo cơ quan chức
  năng; mạo danh công an là kịch bản phổ biến nhất; "theo thống kê mới nhất từ Bộ Công an", 11 tháng đầu 2025 thiệt hại "ước tính trên
  6.000 tỷ đồng" [SECONDARY, VietNamNet] [17].
- Công an các địa phương cảnh báo deepfake gọi video vay tiền liên tục (Ninh Bình, Hà Nội — 25 kịch bản lừa đảo 2026) [SECONDARY] [18].
- Lưu ý: khảo sát NCA là **trực tuyến, tự nguyện**, không phải mẫu đại diện; không cộng/trừ với số Bộ Công an.

### 2.2. Bảng điểm (1–5, cao = tốt; "Rủi ro": 5 = rủi ro sai thấp)

| Tiêu chí | **1. Giả giọng người thân** | 2. Vì sao AI bịa (ảo giác) | 3. Bên trong ChatGPT | 4. Thuật toán đề xuất | 5. GPU / Nvidia |
|---|---|---|---|---|---|
| Nhu cầu VN | **5** — nỗi lo top 3, cảnh báo công an liên tục, chạm cả nhà | 4 — người dùng AI đông, EBU/BBC 45% câu trả lời tin tức có lỗi; wiki 6/ngày | 4 — wiki 417/ngày nhưng 72% desktop | 4 — app khổng lồ, nhưng báo Việt hỏi "lên xu hướng", không hỏi cơ chế | 3 — Jensen 121/ngày, GPU 6 |
| Cold open | **5** — cuộc gọi bốn phút, có ghi âm 911 + lời khai Thượng viện | 5 — luật sư nộp 6 án lệ ChatGPT bịa (Mata v. Avianca, 2023) [CHƯA KIỂM — chưa đọc hồ sơ toà] | 3 | 2 | 3 |
| Áp dụng được | **5** — mật khẩu gia đình, cúp máy gọi lại (FBI, FTC) | 4 — bắt AI ghi nguồn rồi tự kiểm | 2 | 3 | 1 |
| Khác #1/#2 | **5** | 4 | 2 — trùng ch6 #1 | 5 | 2 — trùng ch5 #1 (AlexNet/GPU) |
| Hình | 3 — ảnh PD lịch sử (Voder, Kempelen, Bell Labs); cảnh hiện đại phải Pexels + đồ hoạ; **không** dựng deepfake | 3 | 3 | 2 | 4 |
| Rủi ro sai | 3 — vụ DeStefano chưa xác minh có AI; số lừa đảo biến động; tránh thành "hướng dẫn" | 4 | 4 | 3 | 2 |
| **Tổng** | **26** | 24 | 18 | 19 | 15 |

**Kết luận:** chọn 1. Ứng viên 2 (ảo giác) là ứng viên mạnh cho #4 — cần đọc hồ sơ toà *Mata v. Avianca* (S.D.N.Y., 2023) và bài OpenAI
"Why language models hallucinate" (09/2025) trước khi chấm lại.

---

## 3. Xương sống câu chuyện

- **Câu hỏi trung tâm:** *Nếu một cỗ máy nói được bằng giọng con bạn, bạn còn tin được điều gì?*
- **Cung A → B:** A = giọng nói là **mật khẩu lâu đời nhất** của con người ("nghe là biết ai"; máy nói thì khó và giọng không giống ai —
  Kempelen, Voder). B = 2023–2026: một mô hình nghiên cứu chỉ cần **ba giây** giọng mẫu; tai người bỏ sót **hơn 1/4** giọng giả; cả cuộc họp
  video có thể là giả. Ở giữa: kẻ gian không thắng nhờ giọng mà nhờ **kịch bản** (gấp — giấu — tiền). Kết: lòng tin phải chuyển từ **giọng**
  sang **quy trình + một từ bí mật**.
- **Phân tích riêng của kênh (chống "inauthentic content"):**
  1. "Điều phối viên 911 không nghe giọng, cô ấy nghe ra kịch bản" → phòng vệ bằng nhận diện kịch bản, không bằng soi giọng.
  2. Người nhân viên Hồng Kông **đã nghi và đã kiểm tra** — nhưng kiểm bằng đúng hai thứ bị làm giả (mặt, giọng).
  3. Xác thực sinh trắc học (QĐ 2345) **chứng minh người chuyển là bạn** → chặn kẻ lạ dùng tài khoản, **không** chặn chính bạn tự chuyển khi
     bị lừa. (Suy luận của kênh, nêu rõ là nhận xét.)
- **Thời lượng:** ~2.900 âm tiết (bộ đếm của kịch bản) ≈ 13–14 phút.

---

## 4. Dàn ý chương + dữ kiện

Ký hiệu vòng: **[Mở Vn]** / **[Đóng Vn]**. Ảnh: tên file Commons nguyên văn (`https://commons.wikimedia.org/wiki/File:<tên>`), giấy phép
đọc qua API ngày 07/10/2026. **Không BY-SA.** CC BY vào khối ghi công trong mô tả.

| # | Chương | Âm tiết | % lũy kế |
|---|---|---:|---:|
| 0 | Cold open — Cuộc gọi bốn phút (+ lời thách) | ~339 | 12% |
| 1 | Cỗ máy biết nói (1770 → 1939) | ~306 | 22% |
| 2 | Ba giây (VALL-E, OpenAI, Consumer Reports) | ~393 | 36% |
| 3 | Đôi tai thua cuộc (UCL 73%; kịch bản gấp–giấu–tiền) | ~297 | 46% |
| 4 | Re-hook: Có thật là AI không? | ~288 | 56% |
| 5 | **Cảnh mạnh thứ hai:** Cuộc họp không có ai thật (Hồng Kông) | ~342 | 68% |
| 6 | Cuộc gọi vài giây (Việt Nam) | ~404 | 82% |
| 7 | Mật khẩu gia đình (áp dụng) | ~299 | 92% |
| 8 | Daisy (văn hoá đại chúng + kết) | ~229 | 100% |

### 0. Cold open — "Cuộc gọi bốn phút"

- **Vòng:** [Mở V0] *"Vậy giọng nói trong điện thoại là của ai?"* → đóng ở ch4. [Mở V1] lời thách con số → đóng ở ch2.
- **Dữ kiện:**
  1. Cuộc gọi đến **20/01/2023 khoảng 16:55**, khi bà vừa đỗ xe trước phòng tập múa ở **Scottsdale, Arizona**; con gái lớn **15 tuổi**
     (Brianna) đang đi tập cho giải trượt tuyết; số lạ [SECONDARY: CNN 29/04/2023, Faith Karimi] [1].
  2. Giọng con gái: *"Mom! I messed up!"*; bà kể: *"The voice sounded just like Brie's, the inflection, everything"* [SECONDARY] [1].
     Lời khai Thượng viện ghi: *"MOM THESE BAD MEN HAVE ME, HELP ME, HELP ME!!"* [SECONDARY: nội dung PDF chính thức đọc qua chỉ mục công cụ
     tìm kiếm; PDF trả 403] [2].
  3. Gã đàn ông đe doạ nếu gọi cảnh sát; đòi **1 triệu USD**, hạ xuống **50.000 USD** khi bà nói không có; định đón bà bằng **xe tải trắng**,
     trùm túi lên đầu để mang tiền mặt [SECONDARY] [1]. (Không đọc phần đe doạ tình dục/ma tuý.)
  4. Một phụ huynh khác gọi 911; người khác gọi cho chồng/con gái lớn; có người đưa điện thoại: con gái nói *"Mom, I'm in bed… I'm safe"*
     [SECONDARY] [1]. "Those **four minutes** of terror" [SECONDARY] [1].
  5. Bà khai trước **Tiểu ban Nhân quyền và Pháp luật, Uỷ ban Tư pháp Thượng viện Mỹ**, phiên "Artificial Intelligence and Human Rights",
     **13/06/2023** (chủ toạ Jon Ossoff) [SECONDARY: trang phiên điều trần + crowell.com] [2].
- **Cảnh kể được:** bãi đỗ xe phòng tập múa, chiều thứ Sáu tháng 1, điện thoại để loa ngoài. (20/01/2023 là thứ Sáu — tự kiểm bằng lịch;
  không cần đọc.)
- **Hình:**
  - B-roll **Pexels** (ẢNH MINH HỌA): "woman phone call car", "worried mother phone", "dance studio children" — chưa chọn ID (khoá Pexels
    trên máy chưa cấu hình, xem `2026-10-06-media-sources.md` §1.4).
  - Đồ hoạ tự dựng: màn hình gọi đến "SỐ LẠ", đồng hồ đếm 4:00, hai con số 1.000.000 → 50.000 USD.
  - **Không** dùng ảnh bà DeStefano/con gái (ảnh CNN có bản quyền; nạn nhân là người thật).

### 1. "Cỗ máy biết nói" (1770 → 1939)

- **Vòng:** [Mở V2] cỗ máy đánh cờ "giả làm người nhờ một con người giấu bên trong — hãy nhớ hình ảnh này" → đóng ở ch8 (đảo ngược).
- **Dữ kiện:**
  1. **Cỗ máy đánh cờ "Người Thổ"** của Wolfgang von Kempelen ra mắt **1770** (để gây ấn tượng với Nữ hoàng Maria Theresa); thắng phần lớn
     các ván, kể cả với Napoléon và Benjamin Franklin; thực ra **một kỳ thủ giấu bên trong** điều khiển [SECONDARY: Wikipedia "Mechanical Turk"] [22].
  2. Kempelen làm **máy nói** chạy bằng **ống bễ**, có mô hình **lưỡi và môi**, tạo được cả nguyên âm lẫn phụ âm; mô tả năm **1791**
     [SECONDARY: Wikipedia "Speech synthesis"]; sách *Mechanismus der menschlichen Sprache…* ghi **gần 20 năm** nghiên cứu, năm in ghi
     **1789** ở Wikipedia "Wolfgang von Kempelen" → **vênh năm**, lời đọc dùng "cuối thế kỷ mười tám" [22].
  3. **Voder** (Bell Telephone Laboratories, Homer Dudley, 1937–38) trình diễn ở **Hội chợ Thế giới New York 1939** (và San Francisco);
     điều khiển bằng **phím**, **thanh cổ tay** (chuyển "buzz"/"hiss"), **bàn đạp** (cao độ); "after **months** of practice" mới nói ra chữ;
     **20 người vận hành** được Helen Harper đào tạo [SECONDARY: Wikipedia "Voder", dẫn Dudley, *The Carrier Nature of Speech*, BSTJ 19(4),
     10/1940 và Bell Telephone Quarterly 01/1940] [23].
- **Hình:**
  - `Tuerkischer schachspieler windisch4.jpg` — **Public domain** (tranh khắc thế kỷ 18), 600×523.
  - `“The Turk.” Engraving in Joseph Friedrich Racknitz, Ueber den schachspieler des herrn von Kempelen und dessen nachbildung (2919837469).jpg`
    — **No restrictions** (Library Company of Philadelphia), 900×823. **Lưu ý:** tranh của Racknitz (1789) là **phỏng đoán** cách người chơi
    giấu trong tủ, không phải bản vẽ cơ chế thật → chú thích "hình vẽ phỏng đoán, 1789".
  - `Speech synthesizer Von Kempelen 1791.gif` — **Public domain** (bản khắc trong sách của Kempelen), 479×875.
  - `Kempelen Speakingmachine.JPG` — **Public domain** (ảnh của Fabian Brackhane), 750×561. **Lưu ý:** đây là **bản dựng lại** (Saarbrücken),
    không phải máy gốc thế kỷ 18 → chú thích "bản dựng lại".
  - `VODER demonstrated on 1939 New York World Fair - The VODER fascinates the crowds - Bell Telephone Quarterly (January 1940).jpg` —
    **No restrictions** (Internet Archive Book Images), 2002×1462; cùng loạt: `… - lining up for hearing tests …`, `… - Audition! …`.
    **Lưu ý ngày/nơi:** metadata Commons ghi ngày **"1922"** (sai — nguồn là tạp chí 01/1940); Voder diễn ở **cả New York lẫn San
    Francisco** năm 1939 → phải đối chiếu chú thích trên trang quét gốc trước khi ghi "New York" (bài học ảnh NACA "Hampton" thực ra Muroc).
  - `Homer Dudley (October 1940). "The Carrier Nature of Speech". Bell System Technical Journal, XIX(4);495-515. -- Fig.5 The voder being demonstrated at the New York World's Fair.jpg`
    — **No restrictions**, 1692×2030 (chú thích gốc có ghi New York — dùng ảnh này nếu cần chắc nơi chụp).
  - `… Fig.8 Schematic circuit of the voder.jpg` — **No restrictions** — sơ đồ cho cảnh "phím/cổ tay/bàn đạp".

### 2. "Ba giây" (2023–2025)

- **Vòng:** [Đóng V1] "Ba giây. Bạn đã đoán bao nhiêu?" Callback #1: "ChatGPT đoán mẩu chữ tiếp theo; VALL-E làm vậy với âm thanh".
  Cầu nối: "tai người còn phân biệt được không?" → ch3.
- **Dữ kiện:**
  1. **VALL-E** (Microsoft; Wang, Chen, Wu… ; arXiv 2301.02111, **05/01/2023**) [bằng chứng] [6]:
     - *"synthesize high-quality personalized speech with only a 3-second enrolled recording of an unseen speaker as an acoustic prompt"*
     - *"we scale up the TTS training data to 60K hours of English speech"*; LibriLight *"with over 7000 unique speakers"*
     - coi TTS là bài toán mô hình ngôn ngữ trên mã âm thanh rời rạc; *"advanced prompting-based large-model techniques (as in GPTs)"*
     - *"VALL-E could preserve the speaker's emotion and acoustic environment of the acoustic prompt"*; ví dụ *"reverberation"*, *"anger"*
     - Broader impacts: *"it may carry potential risks in misuse of the model, such as spoofing voice identification or impersonating a
       specific speaker"*
  2. **VALL-E 2** (arXiv 2406.05370, 08/06/2024): *"achieving human parity for the first time"* trên LibriSpeech/VCTK [bằng chứng] [7].
     Câu *"VALL-E 2 is purely a research project. Currently, we have no plans to incorporate VALL-E 2 into a product or expand access to the
     public"* [SECONDARY: dẫn qua the-decoder, Tom's Guide; chưa mở trang dự án Microsoft] [7a].
  3. **OpenAI Voice Engine** (29/03/2024): *"a single 15-second audio sample"*; "cautious and informed approach to a broader release";
     khuyến nghị *phasing out voice based authentication* cho tài khoản ngân hàng [SECONDARY: đoạn trích tìm kiếm của trang chính thức;
     openai.com chặn script] [8].
  4. **Consumer Reports** (10/03/2025), 6 dịch vụ nhân bản giọng: *"Four fail to take basic steps to stop unauthorized voice cloning."*
     [bằng chứng: trang báo cáo] [10]. (Tên 6 công ty có trong báo cáo — **không đọc tên**, theo nguyên tắc không chỉ đích danh.)
  5. Hany Farid (UC Berkeley) với CNN 04/2023: *"A reasonably good clone can be created with under a minute of audio"*; nhân bản có thể
     "for as little $5 a month" [SECONDARY] [1].
- **Phân tích của kênh:** 60.000 giờ = 6,85 năm nghe liên tục → "gần bảy năm" (tự tính). Ẩn dụ: "Bảy nghìn giọng dạy nó cách người ta nói;
  ba giây của bạn chỉ cho nó biết nói như ai" (diễn giải in-context learning, không phải trích).
- **Trung thực:** VALL-E là mô hình **nghiên cứu**, không phải công cụ của kẻ gian; ba giây là kết quả **trên bộ thử chuẩn**, không phải "kẻ
  gian chỉ cần ba giây". Không nêu tên dịch vụ, không hướng dẫn cách nhân bản.
- **Hình:** đồ hoạ tự dựng (sóng âm cắt thành "mẩu", thanh 3 giây vs 60.000 giờ, khối "đoán mẩu tiếp theo" tái dùng phong cách ch6 của #1);
  `Spectrogram of I owe you.png` — **Public domain** (436×227, nhỏ → chỉ làm hoạ tiết); B-roll Pexels "sound wave", "server room".

### 3. "Đôi tai thua cuộc"

- **Vòng:** [Mở V3] "Cô ấy không nghe giọng, cô ấy nghe ra kịch bản" + ba nhịp **gấp — giấu — tiền** → đóng ở ch7. Cầu nối về V0.
- **Dữ kiện:**
  1. **Mai, Bray, Davies, Griffin (UCL), *Warning: Humans cannot reliably detect speech deepfakes*, PLOS ONE 18(8): e0285333, 02/08/2023**
     (CC BY) [bằng chứng] [11]: *"We presented genuine and deepfake audio to n = 529 individuals"*; *"Listeners only correctly spotted the
     deepfakes 73% of the time, and there was no difference in detectability between the two languages"* (tiếng Anh, tiếng Quan Thoại);
     *"providing examples of speech deepfakes only improves results slightly"*.
  2. Ghi âm 911 (Cảnh sát Scottsdale cung cấp cho CNN): điều phối viên nhận ra ngay: *"So that is a very popular scam"* [SECONDARY] [1].
  3. **FTC** (Alvaro Puig, **20/03/2023**) [bằng chứng] [5]: *"All he needs is a short audio clip of your family member's voice — which he
     could get from content posted online — and a voice-cloning program."*; *"Call the person who supposedly contacted you and verify the
     story. Use a phone number you know is theirs."*; cảnh giác khi bị đòi *"wire money, send cryptocurrency, or buy gift cards"* — gần như
     không lấy lại được.
  4. "Gấp — giấu — tiền" là **khung của kênh** tổng hợp từ FTC [5], FBI [4] và chính vụ DeStefano (đe doạ không gọi cảnh sát) [1]; trên
     màn hình ghi "MIM tổng hợp từ FTC, FBI".
- **Hình:** biểu đồ tự vẽ 73% / 27% (529 người, 2 ngôn ngữ); ba thẻ chữ GẤP · GIẤU · TIỀN; b-roll Pexels người nghe tai nghe.

### 4. Re-hook ~50%: "Có thật là AI không?"

- **Vòng:** [Đóng V0] trung thực: **không ai biết chắc**. [Mở V4] "một thứ máy không sao chép được" → ch7. [Mở V5] "một vụ cảnh sát tin chắc
  có hình và giọng giả; nạn nhân không hoảng loạn" → ch5.
- **Dữ kiện:**
  1. CNN: *"Law enforcement has not verified whether AI was used in her case, but DeStefano believes scammers cloned her daughter's
     voice."* [SECONDARY] [1].
  2. Farid: theo hiểu biết của ông (04/2023), phần mềm chưa nhân bản được dải cảm xúc như **tiếng khóc hoảng loạn của trẻ**, nhưng không
     loại trừ hoàn toàn [SECONDARY] [1].
  3. Đặc vụ FBI Siobhan Johnson (Chicago) với CNN: giữa cuộc gọi căng thẳng, người thân "often is not going to question whether it's the live
     voice" [SECONDARY, câu thuật của CNN] [1]; FBI chưa thấy số vụ bắt cóc ảo tăng rõ trong thời AI [SECONDARY] [1] (không đọc, giữ trong hồ sơ).
  4. *"A mother knows her child"* — DeStefano [SECONDARY] [1] → [TRÍCH DỊCH] "Mẹ thì nhận ra con mình".
- **Hình:** chữ đánh máy "CHƯA XÁC MINH", ảnh trừu tượng sóng âm vỡ; nhắc lại đồ hoạ cuộc gọi ở cold open (đóng vòng bằng hình).

### 5. Cảnh mạnh thứ hai (~56–68%): "Cuộc họp không có ai thật" (Hồng Kông, 2024)

- **Vòng:** [Đóng V5]. [Mở V6] "gọi video để kiểm tra, ở Việt Nam còn đủ không?" → ch6.
- **Dữ kiện:**
  1. **Trả lời chất vấn LCQ9 của Bộ trưởng An ninh Tang Ping-keung tại Hội đồng Lập pháp, 26/06/2024** [bằng chứng] [9]:
     - *"In end-January 2024, the Police received one fraud case involving the use of deepfake technology to fabricate a pre-recorded video
       conference."*
     - Kẻ gian *"impersonated the Chief Financial Officer of the informant's head office in the United Kingdom (UK)"*; nạn nhân chuyển tiền tới
       *"five local bank accounts and suffered a loss of about HK$200 million"*.
     - *"the pre-recorded video conference was generated using downloaded online public video clips and voices of the impersonated officer"*
     - *"there was actually no interaction between the informant and the fraudster"*; kẻ gian kết thúc cuộc họp *"under some pretext"* rồi chỉ
       đạo tiếp qua tin nhắn.
     - Vụ thứ hai: **20/05/2024**, họp video **gần 30 phút**, gần **4 triệu HKD** (giữ trong hồ sơ, không đọc).
     - Tới 31/05/2024 cảnh sát Hồng Kông mới ghi nhận **3** vụ liên quan deepfake (08/2023, 01/2024, 05/2024).
  2. **CNN 17/05/2024**: Arup (hãng kỹ thuật Anh, đứng sau những công trình như Nhà hát Opera Sydney) xác nhận là nạn nhân: *"we can confirm
     that fake voices and images were used"*; số tiền ~**25,6 triệu USD**, chuyển qua **15 giao dịch** (RTHK dẫn cảnh sát); nhân viên ban đầu
     nghi email là lừa đảo, hết nghi sau cuộc họp vì người dự *"looked and sounded just like colleagues he recognized"* [SECONDARY] [12].
- **Hình:**
  - `Hong Kong skyscrapers in a night of typhoon.jpg` — **CC0** (Wilfredor, 2013), 2300×1528; `Victoria Harbour skyscrapers.jpg` — **CC0**.
    → **ẢNH MINH HỌA** (không phải văn phòng Arup).
  - Đồ hoạ tự dựng: lưới họp video 4–6 ô, từng ô "vỡ" thành sóng âm/điểm ảnh; bộ đếm 15 lần chuyển → 200 triệu HKD; thẻ chữ trích LegCo.
  - B-roll Pexels "video conference laptop office" (ẢNH MINH HỌA, không lộ logo phần mềm).

### 6. "Cuộc gọi vài giây" (Việt Nam)

- **Vòng:** [Đóng V6] không đủ. Mở và đóng trong chương: "quét khuôn mặt chứng minh điều gì?". Cầu nối "Vậy bạn cần gì?" → ch7.
- **Dữ kiện:**
  1. **Bkav, 02/02/2024** (qua VnEconomy): một nhân viên văn phòng ở Hà Nội; bạn nhắn Messenger hỏi vay; chị đòi gọi video; cuộc gọi
     *"chỉ kéo dài vài giây do 'mạng chập chờn'"*; chuyển tiền; tài khoản Facebook đã bị chiếm, kẻ gian **dựng sẵn video deepfake mặt +
     giọng**; nhiều bạn bè, người thân khác cũng bị lừa, **"hàng chục triệu đồng"** [SECONDARY] [13]. Tên nạn nhân trong bài có thể là
     tên đặt → **không đọc tên**.
  2. **NCA 2024 / 2025** — xem §2.1 [SECONDARY] [16][17]. Câu nguyên văn (VietNamNet): *"khoảng 555 người dùng tham gia khảo sát thì có 1
     người cho biết mình là nạn nhân của lừa đảo, tương đương tỷ lệ 0,18%"*. Hiệp hội quy một phần cho chuyên án của Bộ Công an, tuyên
     truyền, và *"các quy định mới của Ngân hàng Nhà nước về xác thực sinh trắc học"* (nhận định của Hiệp hội, **không phải** chứng minh nhân quả).
  3. **QĐ 2345/QĐ-NHNN** (18/12/2023, hiệu lực **01/07/2024**): xác thực sinh trắc học khuôn mặt khi chuyển **> 10 triệu đồng/lần** hoặc
     **tổng > 20 triệu đồng/ngày** (và khi đăng nhập thiết bị mới, kích hoạt app lần đầu) [SECONDARY: luatvietnam, Tạp chí Công Thương,
     Thị trường Tài chính Tiền tệ khớp nhau] [14].
  4. Bộ Công an: thiệt hại 11 tháng đầu 2025 **> 6.000 tỉ đồng** [SECONDARY qua VietNamNet] [17]; **32,12%** nạn nhân báo cơ quan chức năng [17].
- **Không đọc:** dự báo 2026 của NCA ("sẽ đẩy mạnh Deepfake") — là dự báo; các vụ tống tiền bằng video nhạy cảm ghép mặt (không hợp kênh).
- **Hình:** đồ hoạ tự dựng (bong bóng chat "cho mình vay…", cuộc gọi video 3 giây rồi "Mất kết nối"; thanh 1/220 → 1/555 có chú thích
  "khảo sát trực tuyến"; ngưỡng 10/20 triệu). B-roll Pexels "Asian office worker smartphone", "face scan phone" (không lộ logo ngân hàng).
  Không dùng logo Bkav/NCA/NHNN (nhãn hiệu) — chỉ chữ.

### 7. "Mật khẩu gia đình" (áp dụng)

- **Vòng:** [Đóng V3] ba nhịp thành bước một. [Đóng V4] thứ máy không sao chép được = từ bí mật.
- **Dữ kiện:**
  1. **FBI PSA I-120324-PSA, 03/12/2024**, *Criminals Use Generative Artificial Intelligence to Facilitate Financial Fraud* [bằng chứng] [4]:
     - *"Criminals generate short audio clips containing a loved one's voice to impersonate a close relative in a crisis situation, asking for
       immediate financial assistance or demanding a ransom."*
     - *"Create a secret word or phrase with your family to verify their identity."*
     - *"Listen closely to the tone and word choice…"*; *"If possible, limit online content of your image or voice…"*
     - *"Verify the identity of the person calling you by hanging up the phone, researching the contact of the bank or organization purporting
       to call you, and call the phone number directly."*
     - *"Do not send money, gift cards, cryptocurrency, or other assets to people you do not know or have met only online or over the phone."*
  2. **FTC 20/03/2023**: gọi lại bằng số đã biết; không liên lạc được thì qua người nhà/bạn bè của họ [bằng chứng] [5].
  3. Lời khuyên đặc vụ FBI qua CNN (2023): *"Create a family password"*, nhờ người khác trong phòng gọi cho người thân [SECONDARY] [1].
  4. DeStefano sau vụ việc ngại nghe số lạ, *"rarely says a word until the caller does"* [SECONDARY] [1].
- **Thêm của kênh (lời khuyên thường thức, nói rõ là của kênh):** thống nhất từ bí mật khi gặp mặt; không đăng/gõ vào tin nhắn; tránh tên thú
  cưng, ngày sinh; dặn cả bố mẹ, ông bà. "Đừng gọi lại vào số vừa gọi tới" (số gọi đến có thể bị giả mạo — FCC có trang về caller ID spoofing;
  [CHƯA KIỂM trang FCC], lời đọc không giải thích kỹ thuật).
- **Hình:** thẻ 3 bước (DỪNG · CÚP MÁY GỌI LẠI · HỎI MẬT KHẨU); b-roll Pexels "Vietnamese family dinner" / "Asian family meal" (ẢNH MINH HỌA),
  "elderly man phone"; ổ khoá trừu tượng.

### 8. "Daisy" — văn hoá đại chúng + kết

- **Vòng:** [Đóng V2] máy đội lốt người đảo chiều. Callback #1 (HAL 9000, ch7 của `mim-ai-70`). Trả mô-típ "mẹ thì nhận ra con mình".
- **Dữ kiện:**
  1. **1961**, Bell Labs: máy tính IBM hát **"Daisy Bell"** (Harry Dacre, **1892**) — bài hát đầu tiên do máy tổng hợp tiếng nói hát; nhóm John
     Kelly Jr., Carol Lochbaum, phần đệm Max Mathews [SECONDARY: Wikipedia "Daisy Bell", Guinness World Records] [24].
     **Vênh model:** Wikipedia ghi **IBM 7090**, nhiều nguồn khác ghi **7094** → lời đọc "một chiếc máy tính IBM".
  2. Arthur C. Clarke nghe màn trình diễn khi thăm Bell Labs và đưa vào *2001: A Space Odyssey* (1968): HAL 9000 hát "Daisy Bell" khi bị
     tắt dần [SECONDARY] [24]. Năm thăm (1962 theo Wikipedia) không đọc.
- **Hình:**
  - `IBM 7090 computer.jpg` — **Public domain** (NASA Ames, 06/09/1961), 2566×2009 → **ẢNH MINH HỌA**: máy 7090 ở NASA Ames, **không phải** máy
    hát Daisy ở Bell Labs (chú thích rõ nơi chụp).
  - `IBM 7094 console3.agr.jpg` — **CC BY 4.0** (ArnoldReinhold, 2024, Bảo tàng Lịch sử Máy tính) → ghi công; ẢNH MINH HỌA.
  - `Bell Telephone Laboratories, Murray Hill, New Jersey. LOC gsc.5a08712.jpg` — **Public domain** (Gottscho-Schleisner, **1942**),
    8836×6417 → toà nhà năm 1942, **không phải** ảnh buổi trình diễn 1961; nơi trình diễn (Murray Hill?) **chưa kiểm** → ẢNH MINH HỌA.
  - `Daisybell.jpg` — **Public domain**, 484×640. **Lưu ý:** bìa bản nhạc **Úc, sau 1921**, không phải bản in 1892 → chỉ dùng làm hoạ tiết, chú
    thích "bản in Úc, sau 1921".
  - Không dùng hình/âm thanh phim *2001* (bản quyền) — dựng chấm đỏ trừu tượng (đã có ở #1, kiểm lại cảnh ấy trước khi dùng lại).

**Checklist RETENTION:** cold open có cảnh + câu hỏi chưa trả lời ✔ · lộ trình "Lời thách" ≠ #2 "chặng đường" ✔ · 8 vòng (V0–V6 + vòng
sinh trắc) đóng ở chương sau ✔ · danh sách ≤ 3 mục (Một giờ/Mười phút/Một phút; gấp/giấu/tiền; ba bước; bố mẹ/vợ/con) ✔ · motif ≥ 3 lần ✔ ·
mỗi chương kết bằng câu cầu nối/câu hỏi ✔ · cảnh mạnh thứ hai 56–68% (sớm hơn mốc ~75%; bù bằng cảnh Việt Nam 68–75% và chương văn hoá đại
chúng cuối) ⚠ · số liệu có nguồn + năm ✔ (trừ các mục [SECONDARY] ở mục 9).

---

## 5. Kiểm kê hình mở (Commons, 40 kết quả đầu, 07/10/2026) [20]

| Truy vấn | PD/CC0 | CC BY | BY-SA | Không raster | Nhận xét |
|---|---:|---:|---:|---:|---|
| Kempelen speaking machine | 5 | 0 | 4 | 31 | Bản khắc 1791 + ảnh bản dựng lại |
| Kempelen chess Turk engraving | 6 | 0 | 0 | 3 | Tranh khắc thế kỷ 18 (Racknitz = phỏng đoán) |
| Voder Bell | **10** | 0 | 1 | 29 | Ảnh Bell Telephone Quarterly/BSTJ 1940; **metadata ngày "1922" sai** |
| IBM 7094 | 5 | 4 | 2 | 29 | PD là ảnh 7090 của NASA/Weather Bureau, **không phải Bell Labs** |
| Bell Labs Murray Hill | **38** | 0 | 2 | 0 | Ảnh kiến trúc LoC 1942 |
| Daisy Bell sheet music | 5 | 0 | 0 | 35 | Chỉ có bìa Úc sau 1921 |
| Hong Kong skyline night Central | 4 | 10 | 25 | 1 | Dùng CC0 Wilfredor |
| spectrogram speech | 2 | 2 | 7 | 29 | Ảnh nhỏ; tự vẽ tốt hơn |
| rotary telephone handset | 4 | 3 | 5 | 16 | `Western electric 201 telephone.jpg` PD |
| smartphone incoming call | 0 | 1 | 0 | 31 | Không có → đồ hoạ tự dựng |

Thiếu ảnh mở cho: DeStefano, phòng tập múa, cuộc họp Arup, văn phòng Hà Nội, quét khuôn mặt ngân hàng → đồ hoạ + **Pexels** (ẢNH MINH HỌA).
Ảnh "deepfake" trên Commons phần lớn là ảnh AI của người thật → **không dùng** (theo `2026-10-06-media-sources.md` §1.6). **Không** tạo giọng
giả người thật để "minh hoạ"; nếu cần, dùng giọng TTS của kênh với nhãn **GIỌNG MÁY TẠO** (đúng tinh thần NĐ 142/2026 về gắn nhãn).

**Pexels (chưa chọn ID — cần khoá):** "woman phone call car", "worried mother phone", "dance studio", "video conference laptop",
"Asian office worker smartphone", "face scan phone", "elderly man phone", "Asian family dinner", "sound wave", "server room".

---

## 6. Huyền thoại / lỗi thường gặp

| Hay nói sai | Đúng là | Nguồn |
|---|---|---|
| "Vụ DeStefano đã được xác nhận là AI giả giọng" | Cơ quan chức năng **chưa xác minh**; bà **tin** là AI | [1] |
| "Kẻ gian chỉ cần 3 giây giọng của bạn" | 3 giây là kết quả **mô hình nghiên cứu VALL-E** trên bộ thử chuẩn; chuyên gia nói "dưới một phút", "có người cho là vài giây" | [6][1] |
| "Nghe kỹ là phân biệt được giọng AI" | Người nghe được báo trước vẫn chỉ đúng 73%; luyện trước chỉ khá hơn chút | [11] |
| "Gọi video thấy mặt là chắc ăn" | Hồng Kông 2024: cả cuộc họp là video dựng sẵn; Bkav 2024: cuộc gọi vài giây | [9][13] |
| "Xác thực khuôn mặt chống được lừa đảo giả giọng" | Chặn kẻ lạ dùng tài khoản bạn; **không** chặn chính bạn tự chuyển (nhận xét của kênh) | [14] |
| "Lừa đảo trực tuyến ở VN giảm từ 18.900 tỉ xuống 6.000 tỉ" | Hai con số khác nguồn, khác phương pháp, khác kỳ → **không so** | [16][17] |
| "NCA nói năm 2026 deepfake sẽ bùng nổ" | Là **dự báo** của Hiệp hội, không phải dữ kiện | [17] |
| "Máy tính đầu tiên biết hát là IBM 7094" | Nguồn vênh 7090/7094 → nói "máy tính IBM" | [24] |
| "Máy đánh cờ Kempelen là AI đầu tiên" | Là **trò lừa**, người giấu bên trong | [22] |
| "OpenAI/Microsoft đã tung công cụ nhân bản giọng cho mọi người" | Cả hai **giữ lại**/hạn chế (SECONDARY); thị trường thì có dịch vụ khác, 4/6 thiếu biện pháp cơ bản | [7a][8][10] |

---

## 7. Gợi ý phát âm cho TTS (`say` trong spec)

| Chữ gốc | Gợi ý đọc | Chữ gốc | Gợi ý đọc |
|---|---|---|---|
| Jennifer DeStefano | Gien-ni-phơ Đờ-xtê-pha-nô | Scottsdale, Arizona | Xcốt-xđêu, A-ri-dô-na |
| Wolfgang von Kempelen | Vôn-phơ-gang phôn Kem-pơ-lần | Napoléon | Na-pô-lê-ông |
| Voder | Vô-đơ | Bell | Ben |
| Microsoft | Mai-crô-xốp | VALL-E | Van-i |
| ChatGPT | chát gi pi ti (đã có) | OpenAI | Ô-pần Ây-ai |
| Consumer Reports | Con-xiu-mơ Ri-pót | College London | Co-lít Luân Đôn |
| CNN | Xi-en-en | Hany Farid | Ha-ni Pha-rít |
| California, Berkeley | Ca-li-pho-ni-a, Bơ-cơ-li | FBI | Ép-bi-ai |
| Arup | A-rớp | Opera Sydney | Ô-pê-ra Xít-ni |
| Bkav | Bê-kav | Messenger / Facebook | Mét-xen-giơ / Phây-búc |
| IBM | ai bi em (đã có) | Daisy Bell | Đây-di Ben |
| Arthur C. Clarke | A-thơ Xi Clác | 2001: A Space Odyssey | Hai nghìn không trăm lẻ một: A Xpêt Ô-đi-xê |
| HAL 9000 | Han chín nghìn | Hồng Kông | (tiếng Việt) |

Thử giọng trước: "DeStefano", "VALL-E", "Bkav", "Arthur C. Clarke", "2001", "HAL 9000". Nếu cắt Short, engine Short cần bảng `say` tương ứng
(retro #8).

---

## 8. Đóng gói

**Tựa (3 phương án cho Test & Compare):**
1. *"Mẹ Ơi, Cứu Con!" — Khi AI Nói Bằng Giọng Người Thân Của Bạn*
2. *AI Giả Giọng Người Thân Để Lừa Tiền: Một Từ Bí Mật Có Thể Cứu Cả Nhà*
3. *Một Mô Hình AI Chỉ Cần Nghe Bạn Nói Ba Giây. Đây Là Cách Không Bị Lừa*

**Thumbnail:** nền theme "lab". Màn hình điện thoại cuộc gọi đến "CON GÁI" với sóng âm đỏ, nửa sóng âm hoá mạch điện/điểm ảnh; chữ lớn
**"GIỌNG NÀY LÀ GIẢ"** (phương án 1) hoặc **"3 GIÂY"** (phương án 3). Không mặt người thật, không logo, không hình bạo lực/bắt cóc (giữ quảng
cáo đầy đủ — `RESEARCH-million-views.md` mục 4, hàm ý 6). Cold open mở đúng bằng màn hình cuộc gọi ấy.

**Chương YouTube (có từ khoá):** 00:00 Cuộc gọi "bắt cóc" bằng giọng con gái · Cỗ máy biết nói đầu tiên · AI giả giọng chỉ cần 3 giây? ·
Tai người có nhận ra giọng AI? · Có thật là AI không? · Vụ lừa đảo deepfake 200 triệu HKD · Lừa đảo gọi video ở Việt Nam · Mật khẩu gia
đình: 3 bước chống giả giọng · Daisy và HAL 9000.

**3 Short mồi (cắt từ chính video):**
1. **"Máy cần nghe bạn bao lâu để giả giọng bạn?"** — lời thách trong 1 giây, đáp "ba giây" (VALL-E, nghiên cứu) + câu "đây là mô hình nghiên
   cứu"; kết: "người nghe chỉ nhận ra 73%". Rủi ro thấp.
2. **"Cả cuộc họp video là giả: 200 triệu đô la Hồng Kông"** — kết bằng câu LegCo "không có ai trò chuyện qua lại". Rủi ro thấp (nguồn chính phủ).
3. **"Mật khẩu gia đình — FBI khuyên làm ngay"** — 3 bước; đăng lại sát Tết 2027. Rủi ro thấp; hợp chia sẻ cho bố mẹ.

---

## 9. Việc phải làm trước khi khoá kịch bản

1. **Mở PDF lời khai DeStefano** (judiciary.senate.gov, 403 với script) bằng trình duyệt; đối chiếu: số tiền 1 triệu → 50.000 USD, xe tải trắng,
   lời con gái. Nếu PDF khác CNN, theo PDF.
2. **OpenAI Voice Engine** (29/03/2024) và **trang dự án VALL-E 2** của Microsoft: mở bằng trình duyệt để nâng [SECONDARY] → [bằng chứng];
   nếu không được, cắt câu Microsoft (giữ OpenAI kèm "theo OpenAI").
3. **"15 giao dịch"** (RTHK qua CNN): tìm thông cáo cảnh sát Hồng Kông 02/2024 hoặc bản tin RTHK; nếu không, bỏ cụm "chia làm mười lăm lần".
4. **QĐ 2345/QĐ-NHNN**: mở văn bản gốc (sbv.gov.vn / vbpl.vn) để chép đúng ngưỡng 10 triệu/20 triệu trước khi vẽ.
5. **Số NCA 2024/2025 + 6.000 tỉ của Bộ Công an**: tìm báo cáo NCA gốc (nca.org.vn) hoặc thông cáo Bộ Công an; hiện mới qua VietNamNet/Tuổi Trẻ.
6. **Ảnh Voder**: mở trang quét Bell Telephone Quarterly 01/1940 để xác nhận ảnh nào chụp ở New York, ảnh nào ở San Francisco (metadata Commons
   ghi ngày sai "1922").
7. **Daisy Bell**: chốt model (7090 hay 7094) và nơi trình diễn (Murray Hill?) bằng nguồn Bell Labs/Nokia Bell Labs hoặc CHM; tới lúc đó giữ
   "máy tính IBM", "Phòng thí nghiệm Bell".
8. Theme gallery (retro #1): cảnh mới cần demo trước khi dàn: **màn hình cuộc gọi đến** (số lạ/tên người thân), **lưới họp video vỡ dần**,
   **thanh "3 giây vs 60.000 giờ"** (thang log), **thẻ 3 bước**.
9. Cảnh "đoán mẩu tiếp theo" ở ch2 tái dùng phong cách ch6 của #1 — kiểm `data/long/mim-ai-70/ch06.json` để không lặp y nguyên (chống
   "inauthentic": đổi hình mẩu chữ thành mẩu sóng âm).

---

## 10. Nguồn (truy cập 07/10/2026)

1. F. Karimi, *'Mom, these bad men have me': She believes scammers cloned her daughter's voice in a fake kidnapping*, CNN, 29/04/2023 (đọc toàn văn bằng curl): https://edition.cnn.com/2023/04/29/us/ai-scam-calls-kidnapping-cec/index.html
2. U.S. Senate Committee on the Judiciary, Subcommittee on Human Rights and the Law, *Artificial Intelligence and Human Rights*, 13/06/2023 — *Written Statement of Jennifer DeStefano* (PDF, 403 với script; đọc qua chỉ mục tìm kiếm): https://www.judiciary.senate.gov/imo/media/doc/2023-06-13%20PM%20-%20Testimony%20-%20DeStefano.pdf ; trang phiên: https://www.judiciary.senate.gov/committee-activity/hearings/artificial-intelligence-and-human-rights ; tóm tắt: https://www.crowell.com/en/insights/client-alerts/us-senate-hearing-on-artificial-intelligence-and-human-rights
3. (dự phòng) Gizmodo, *Mom Recounts 'Terrorizing' Deepfake Kidnapping Scam in Gripping Testimony* (06/2023, 403): https://gizmodo.com/ai-deepfake-kidnapping-scam-congress-hearing-1850536490
4. FBI / IC3, *Criminals Use Generative Artificial Intelligence to Facilitate Financial Fraud*, Alert I-120324-PSA, 03/12/2024 (đọc toàn văn): https://www.ic3.gov/PSA/2024/PSA241203
5. FTC Consumer Advice (A. Puig), *Scammers use AI to enhance their family emergency schemes*, 20/03/2023: https://consumer.ftc.gov/consumer-alerts/2023/03/scammers-use-ai-enhance-their-family-emergency-schemes
6. C. Wang, S. Chen, Y. Wu et al. (Microsoft), *Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers* (VALL-E), arXiv:2301.02111, 05/01/2023 (đọc PDF): https://arxiv.org/abs/2301.02111
7. S. Chen et al., *VALL-E 2: Neural Codec Language Models are Human Parity Zero-Shot Text to Speech Synthesizers*, arXiv:2406.05370, 08/06/2024: https://arxiv.org/abs/2406.05370 · 7a. (SECONDARY) The Decoder, *VALL-E 2…*: https://the-decoder.com/vall-e-2-microsofts-new-ai-voice-tech-is-so-good-theyre-afraid-to-release-it/ ; Tom's Guide: https://tomsguide.com/ai/microsoft-just-made-an-ai-voice-generator-so-convincing-its-too-dangerous-to-release
8. OpenAI, *Navigating the Challenges and Opportunities of Synthetic Voices*, 29/03/2024 (chặn script; đọc qua đoạn trích tìm kiếm): https://openai.com/index/navigating-the-challenges-and-opportunities-of-synthetic-voices/
9. Government of the HKSAR, *LCQ9: Combating frauds involving deepfake* (trả lời của Bộ trưởng An ninh Tang Ping-keung tại Hội đồng Lập pháp), 26/06/2024 (đọc toàn văn): https://www.info.gov.hk/gia/general/202406/26/P2024062600192.htm
10. Consumer Reports, *New Report: Do These 6 AI Voice Cloning Companies Do Enough to Prevent Misuse?*, 10/03/2025: https://innovation.consumerreports.org/new-report-do-these-6-ai-voice-cloning-companies-do-enough-to-prevent-misuse/ ; thông cáo: https://www.consumerreports.org/media-room/press-releases/2025/03/consumer-reports-assessment-of-ai-voice-cloning-products
11. K. T. Mai, S. Bray, T. Davies, L. D. Griffin, *Warning: Humans cannot reliably detect speech deepfakes*, PLOS ONE 18(8): e0285333, 02/08/2023 (CC BY; đọc toàn văn): https://doi.org/10.1371/journal.pone.0285333
12. K. Magramo, *British engineering giant Arup revealed as $25 million deepfake scam victim*, CNN, 17/05/2024 (đọc toàn văn): https://edition.cnn.com/2024/05/16/tech/arup-deepfake-scam-loss-hong-kong-intl-hnk/index.html
13. VnEconomy, *Cảnh báo hiện tượng dùng AI giả mạo hình ảnh, giọng nói để lừa tiền* (cảnh báo của Bkav, 02/02/2024): https://vneconomy.vn/canh-bao-hien-tuong-dung-ai-gia-mao-hinh-anh-giong-noi-de-lua-tien.htm
14. Quyết định 2345/QĐ-NHNN (18/12/2023, hiệu lực 01/07/2024) — qua: https://luatvietnam.vn/tin-van-ban-moi/tu-2024-chuyen-khoan-tren-10-trieu-dong-phai-xac-thuc-sinh-trac-hoc-186-96491-article.html ; https://tapchicongthuong.vn/chinh-thuc-tu-1-7-2024--chuyen-tien-tren-10-trieu-dong-phai-xac-thuc-bang-khuon-mat--van-tay-122879.htm
15. FCC, *FCC Makes AI-Generated Voices in Robocalls Illegal*, 08/02/2024 (đọc PDF; không dùng trong lời đọc, giữ làm bối cảnh: *"calls made with AI-generated voices are 'artificial' under the Telephone Consumer Protection Act (TCPA)"*): https://docs.fcc.gov/public/attachments/DOC-400393A1.pdf
16. Tuổi Trẻ, *Người Việt mất 18.900 tỉ đồng vì bị lừa đảo trong năm 2024* (khảo sát NCA, 16/12/2024): https://tuoitre.vn/nguoi-viet-mat-18-900-ti-dong-vi-bi-lua-dao-trong-nam-2024-20241216095908927.htm ; VnEconomy: https://vneconomy.vn/thiet-hai-do-lua-dao-truc-tuyen-nam-2024-tai-viet-nam-len-toi-gan-19-000-ty-dong.htm
17. VietNamNet, *Chỉ 32,12% nạn nhân bị lừa đảo trực tuyến có báo cơ quan chức năng* (khảo sát NCA 2025; số Bộ Công an 11 tháng 2025) (đọc toàn văn): https://vietnamnet.vn/chi-32-12-nan-nhan-bi-lua-dao-truc-tuyen-co-bao-co-quan-chuc-nang-2479618.html ; *Tội phạm mạng sẽ dùng nhiều công nghệ Deepfake để lừa đảo trong năm 2026* (dự báo — không đọc): https://vietnamnet.vn/toi-pham-mang-se-dung-nhieu-cong-nghe-deepfake-de-lua-dao-trong-nam-2026-2479714.html
18. Cảnh báo deepfake của công an địa phương (SECONDARY): https://thitruongtaichinhtiente.vn/canh-bao-thu-doan-lua-dao-bang-cuoc-goi-video-deepfake-83388.html ; https://doanhnhan.baophapluat.vn/cong-an-ha-noi-canh-bao-nguoi-dan-canh-giac-truoc-25-kich-ban-lua-dao-tren-khong-gian-mang-nam-2026-7cc6172e.html
19. Nội bộ: `docs/channels/mind-in-the-machine/2026-10-06-topic-research.md` (§1–2, 3.1 #4, 3.2 #5), `2026-10-05-analysis.md`, `2026-10-07-long-02-research.md` (§2.2), `2026-10-06-media-sources.md`, `motion/long/RETENTION.md`, `motion/long/RESEARCH-million-views.md`, `docs/pm/2026-10-06-retro-1.md`
20. Wikimedia Commons API (`generator=search`, `prop=imageinfo&iiprop=extmetadata|size|mime`), 07/10/2026: https://commons.wikimedia.org/w/api.php
21. Wikimedia Pageviews REST API (vi.wikipedia, `user`, daily, 20260709–20261006; `all-access` và `mobile-web`): `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/vi.wikipedia/{access}/user/{bài}/daily/20260709/20261006`
22. Wikipedia (con trỏ, SECONDARY): https://en.wikipedia.org/wiki/Mechanical_Turk ; https://en.wikipedia.org/wiki/Wolfgang_von_Kempelen ; https://en.wikipedia.org/wiki/Speech_synthesis (mục History)
23. Wikipedia, *Voder* (SECONDARY) — dẫn H. Dudley, *The Carrier Nature of Speech*, Bell System Technical Journal 19(4):495–515, 10/1940 và T. W. Williams, *At the New York World's Fair*, Bell Telephone Quarterly 19(1), 01/1940: https://en.wikipedia.org/wiki/Voder
24. Wikipedia, *Daisy Bell* (SECONDARY): https://en.wikipedia.org/wiki/Daisy_Bell ; Guinness World Records, *First song performed using computer speech synthesis*: https://www.guinnessworldrecords.com/world-records/454935-first-song-performed-using-computer-speech-synthesis
