# Nghiên cứu video dài #2 — Mind in the Machine (MIM) — 07/10/2026

**Phạm vi:** đề xuất 5 ứng viên cho video dài thứ hai (16:9, 12–15 phút, tiếng Việt, faceless, giọng TTS + motion graphics + ảnh mở),
chấm điểm, chọn một và lập hồ sơ dữ kiện có nguồn. Tránh trùng video #1 *"AI đã chết hai lần"* (`2026-10-06-long-01-research.md`,
`data/long/mim-ai-70/script.md`: Perceptron, Dartmouth, Shannon, ELIZA, hai mùa đông AI, Deep Blue, backprop, AlexNet/GPU, AlphaGo,
Transformer, ChatGPT "đoán chữ", phép thử Turing 2025, Nobel 2024, phim HAL/Skynet/Doraemon). Áp dụng `motion/long/RETENTION.md`
(cold open, cung A → B, lộ trình 3 câu hỏi ở phút 1, danh sách ≤ 3 mục, mỗi chương mở một vòng và đóng ở chương sau, re-hook ~50%,
cảnh mạnh thứ hai ~75%, motif, văn hoá đại chúng gần cuối, kết mở) và quy trình retro sprint 1 (`docs/pm/2026-10-06-retro-1.md`:
hồ sơ dữ kiện → kịch bản → kiểm chứng → dàn cảnh; số liệu tự tính đối chiếu ≥ 3 mốc).

**Phương pháp:**
- Wikimedia Pageviews REST API (vi.wikipedia, `user`, theo ngày, **09/07 → 06/10/2026 = 90 ngày**; thêm tách `desktop` / `mobile-web`
  / `mobile-app` cho 28 ngày 09/09 → 06/10), MediaWiki API để giải redirect, Commons API (`generator=search`, 40 kết quả đầu,
  `prop=imageinfo&iiprop=extmetadata|size|mime`, đọc `LicenseShortName`). User-Agent
  `yt-factory-research/1.0 (https://github.com/nguyent0810/Youtube_Creator_V2)`, giãn ~1 giây.
- Google Trends: chỉ thử **RSS "Trending now" chính thức** (`trends.google.com/trending/rss?geo=VN`, 07/10): toàn xổ số, bóng đá,
  áp thấp nhiệt đới → không dùng được cho ngách công nghệ (giống nhận xét ở `2026-10-05-analysis.md`). Không gọi API explore (tránh cào).
- Báo chí, báo cáo, bài báo khoa học đọc trực tiếp khi mở được. **Không** cào YouTube, không dùng YouTube API, không tổng hợp số
  liệu kênh khác, không khoá API, không tải media.
- **Nhãn dữ kiện:** **[bằng chứng]** = đã đọc tận nguồn gốc/chính thức hôm nay · **[SECONDARY]** = qua báo/blog/tóm tắt tìm kiếm,
  chưa mở bản gốc (nhiều trang chặn script: ILO, NYT, Works in Progress, Hansard, APS…) · **[CHƯA KIỂM]** = chưa có nguồn đủ tin;
  không đọc lên nếu chưa kiểm. Số trong ngoặc vuông `[n]` trỏ tới mục 10 (Nguồn). Trích nguyên văn chỉ là cụm ngắn < 15 từ.
- **Lượt kiểm chứng trước khoá kịch bản (06/10/2026, giờ máy):** các nhãn đã đổi được đánh dấu **✎** ngay tại chỗ; bảng tổng hợp +
  nguồn mới ở **mục 11**. Mở bằng WebFetch/curl; trang chặn script thì tìm bản gốc khác (PDF kho lưu trữ ILO/EconStor, bản text NPR,
  bảng OES từng năm của BLS, FRED). Không mở YouTube.

---

## 1. Tóm tắt

- **Chọn: "AI có cướp việc của bạn? 200 năm loài người sợ máy móc — và điều thật sự đã xảy ra"** (trục A "AI dễ hiểu", cầu nối B).
- **Vì sao:**
  1. *Nỗi lo số 1 của đúng khán giả:* 61% người Việt lo mất việc vì AI (UNDP, 12/2025) [33]; báo Việt liên tục đưa tin "hơn 123.000",
     "gần 190.000" nhân sự công nghệ mất việc năm 2026 [34]; tuần này McKinsey (Fortune 03/10/2026) [35]. Người 25–44 đang đi làm là
     người lo nhất — khác với video #1 (tò mò lịch sử), video này chạm *túi tiền và sự nghiệp*.
  2. *Có dữ liệu mới, đúng lúc:* Stanford Digital Economy Lab (12/08/2026): **không** thấy mất việc diện rộng, nhưng lao động
     **22–25 tuổi** trong nghề phơi nhiễm AI cao thấp hơn mức kỳ vọng **~19%** (từ 15% một năm trước), chủ yếu do **tuyển ít đi**
     chứ không phải sa thải [12]. Đây là "chi tiết lạ" làm video khác báo chí.
  3. *Cung A → B có sẵn cảnh mở cực mạnh và ảnh PD:* "máy tính" từng là **tên một nghề** của con người (NACA/NASA, ảnh PD 38/40
     kết quả Commons) → nghề biến mất, người thì không (Dorothy Vaughan tự học FORTRAN) [3][4]. Cảnh mạnh thứ hai ở ~75%: Hinton năm
     2016 bảo "ngừng đào tạo bác sĩ X-quang" → 2025 ngành X-quang Mỹ tuyển kỷ lục [20][21]. Hinton là nhân vật của video #1 → callback.
  4. *Phân tích của riêng kênh (chống "inauthentic content"):* đặt cạnh nhau hai làn sóng — thời tổng đài (1920–40) người **đang
     làm** chịu thiệt, thế hệ **sau** vẫn ổn [8]; thời AI (2023–26) người **mới vào nghề** chịu thiệt trước [12]. "Lần này có khác:
     cái giá chuyển từ người cũ sang người mới."
  5. *Không trùng video #1* (chỉ chạm lại Hinton và thẻ đục lỗ như callback), rủi ro vừa phải nếu giữ kỷ luật "mô tả, không dự báo,
     không khuyên nghề".
- **Motif:** **thẻ đục lỗ** (khung cửi Jacquard 1804 → máy Hollerith → thẻ IBM 704 ở video #1 → hôm nay) và **"lần này khác"**
  (câu mỗi thế hệ đều nói, xuất hiện ở cold open, giữa, kết).
- **Đăng đề xuất:** 26/10 → 09/11/2026 (sau video #1 hẹn 12/10 khoảng 2 tuần; trước đợt báo cáo cuối năm về việc làm). Ba Short mồi
  đăng trước 7–10 ngày.

---

## 2. Năm ứng viên và bảng điểm

### 2.1. Tín hiệu nhu cầu (ngoài YouTube)

**Wikipedia tiếng Việt** (người dùng thật, trung vị lượt xem/ngày, 09/07 → 06/10/2026; cột "tháng" = trung vị từng tháng 7 → 10) [1]:

| Ứng viên | Bài liên quan (trung vị 90 ngày · 28 ngày gần nhất · theo tháng) |
|---|---|
| **1. AI và việc làm** | Trí tuệ nhân tạo **360 · 1.075** (7: 238 → 8: 331 → 9: 826 → 10: 1.170) · Cách mạng Công nghiệp **36 · 103,5** (30 → 29 → 103 → 63) · Cách mạng Công nghiệp lần thứ tư **32 · 59,5** · Robot 21 · Tự động hóa 10 · Máy rút tiền tự động 8 · Thất nghiệp 5 · Katherine Johnson 3 · **ENIAC 17 · 327** (9 → 13 → 216 → 386, đỉnh 1.660 ngày 30/09) |
| 2. Bên trong ChatGPT | ChatGPT **377 · 411,5** · Google Gemini 35 · Học máy 18 · Mô hình ngôn ngữ lớn 8 · Ảo giác (TTNT) 6 · Transformer (học máy) 5 · Học sâu 5 |
| 3. Thuật toán đề xuất (TikTok/YouTube) | YouTube **805** · Facebook **300** · TikTok **296** · Zalo 213 · Instagram 53 · Netflix 35 · Thuật toán 12 · Bong bóng lọc 1 · *Hệ thống khuyến nghị*: chưa có bài |
| 4. Deepfake & lừa đảo giả giọng | Deepfake **12 · 16** (10 → 10 → 13,5 → 17, đang tăng) · Mạng đối nghịch tạo sinh 1 · Tổng hợp giọng nói 2 · *Lừa đảo qua mạng*: chưa có bài |
| 5. GPU / NVIDIA thành "vua AI" | Jensen Huang **92 · 121** · NVIDIA 35 · TSMC 24 · Chất bán dẫn 18 · Transistor 17 · Định luật Moore 8 · Bộ xử lý đồ họa 5 · Trung tâm dữ liệu 3 |

**Tách thiết bị (28 ngày 09/09 → 06/10)** — quan trọng vì khán giả MIM xem trên **điện thoại** [1]:

| Bài | Desktop | Mobile | Diễn giải **(chưa chắc về nhân quả)** |
|---|---:|---:|---|
| Trí tuệ nhân tạo | 69% | 30% | Phần tăng tháng 9–10 chủ yếu desktop ngày thường → khả năng cao là học sinh/giáo viên (12 tiết AI/năm từ 2026–27) |
| ChatGPT | 72% | 27% | Tương tự |
| ENIAC | **86%** | 13% | Đỉnh thứ Hai–Năm, rơi cuối tuần → bài học Tin học ở trường. Không phải khán giả MIM, nhưng cho thấy "máy tính đầu tiên" đang được dạy |
| Cách mạng Công nghiệp | 50% | 49% | Cân bằng |
| Jensen Huang | 28% | **71%** | Người lớn tò mò trên điện thoại — khớp khán giả MIM |
| Elon Musk | 25% | 74% | Như trên |
| Deepfake | 49% | 50% | Nhỏ nhưng cân bằng |

→ Mức mobile tuyệt đối vẫn lớn nhất ở "Trí tuệ nhân tạo" (~285/ngày mobile). Đóng gói video #2 nên dùng từ người lớn tự gõ: **"AI",
"mất việc", "cướp việc"** chứ không dùng thuật ngữ.

**Báo chí và báo cáo (06–07/10/2026):**
- Việc làm: báo Việt (CafeBiz/Kenh14 04/2026, Afamily 06/2026, 1thegioi) đưa tin "80.000", "123.000", "gần 190.000" nhân sự công
  nghệ mất việc năm 2026 [SECONDARY] [34]; Fortune 03/10/2026 về báo cáo McKinsey (AI tạo nhiều việc hơn số mất, sau khi xoá
  ~11 triệu việc ở Mỹ) [SECONDARY] [35]; Stanford 12/08/2026 [bằng chứng] [12]; Yale Budget Lab 01/10/2025 [bằng chứng] [13];
  ILO 05/2025 [bằng chứng ✎ — đọc PDF WP140] [14]; UNDP 61% (VietNamNet 02/12/2025) [SECONDARY — ✎ chưa tìm thấy con số này
  trong thông cáo UNDP; tìm kiếm HDR 2025 cho ra các tỉ lệ khác → **không đọc trong video**] [33].
- Deepfake: Bộ Công an cảnh báo 25 kịch bản lừa đảo 2026 (08/09/2026), có nhóm AI/Deepfake/DeepVoice; CafeF 06/10/2026 về app tạo
  ảnh AI [SECONDARY] [36].
- Thuật toán: báo Việt về "thuật toán TikTok 2026" gần như toàn bài marketing "lên xu hướng" → người Việt quan tâm *cách lên
  xu hướng*, không phải *cơ chế* [SECONDARY] [37].
- Google Trends "Trending now" VN 07/10: không có mục công nghệ nào (xsmb 200.000+, áp thấp nhiệt đới 5.000+…) [2].

### 2.2. Bảng điểm (1–5, cao = tốt; "Rủi ro": 5 = rủi ro sai thấp)

| Tiêu chí | **1. AI & việc làm** | 2. Bên trong ChatGPT | 3. Thuật toán đề xuất | 4. Deepfake giả giọng | 5. GPU/NVIDIA |
|---|---|---|---|---|---|
| **Nhu cầu** | **5** — nỗi lo số 1 (61%), tin tức dày đặc tuần này, wiki "Cách mạng Công nghiệp" ×3, "TTNT" ×4 | 5 — ChatGPT 377/ngày, nhưng 72% desktop (học sinh) | 4 — app khổng lồ nhưng là tra cứu điều hướng; "Thuật toán" 12 | 4 — tin công an liên tục; wiki nhỏ (16) | 3 — Jensen 121 (71% mobile, đúng khán giả) nhưng GPU 5 |
| **Mới so với video #1** | **5** — không trùng; Hinton + thẻ đục lỗ chỉ là callback | 2 — chương 6 của #1 đã giải thích "đoán mẩu chữ tiếp theo" + Transformer | 5 | 5 | 2 — chương 5 #1 đã kể AlexNet trên 2 card GTX 580 |
| **Hình với engine** | **5** — NACA "computers" PD 38/40; ENIAC (Lục quân Mỹ) PD; tổng đài viên PD 29/40; tranh Luddite 1812 PD; máy dệt 1835 PD; Keynes 1929 PD; Lovelace PD; biểu đồ tự vẽ (BLS, Stanford) | 3 — chỉ sơ đồ; không chụp giao diện/logo | 2 — chỉ sơ đồ; UI/logo là nhãn hiệu; hầu như không có ảnh lịch sử | 2 — không được dựng deepfake người thật; ảnh "deepfake" trên Commons phần lớn là ảnh AI người thật (theo `media-sources` mục 1.6) | 4 — die chip CC0 dồi dào, Jensen CC0 |
| **Rủi ro sai** | 3 — kinh tế học có tranh cãi; phải nói "mô tả, chưa chứng minh nhân quả"; không dự báo, không khuyên nghề | 4 — khái niệm bền; tên mô hình đổi từng tuần | 3 — cơ chế nội bộ là bí mật; chỉ có vài bài báo công khai | 2 — số liệu lừa đảo biến động; dễ thành "hướng dẫn"; nhãn AI theo NĐ 142 | 2 — giá cổ phiếu, kiểm soát xuất khẩu Mỹ–Trung |
| Thời điểm (ghi chú) | Stanford 08/2026, McKinsey 10/2026, ENIAC 80 năm (02/1946), Hinton "X-quang" tròn 10 năm (11/2016) | ChatGPT tròn 4 năm 30/11 → hợp video #3 | Netflix Prize 20 năm (02/10/2006), Google mua YouTube 20 năm (09/10) **(chưa kiểm ngày)** | Tết 2027 (mùa lừa đảo) | — |
| **Tổng (4 tiêu chí)** | **18** | 14 | 14 | 13 | 11 |

**Kết luận:** chọn **1**. Ứng viên 2 để làm **video #3 dịp ChatGPT 4 tuổi (30/11)**, mở bằng câu "video trước mình nói nó đoán chữ —
lần này mở hộp ra xem". Ứng viên 4 hợp **chuỗi Short** (mẹo cúp máy gọi lại) hơn video dài. Ứng viên 3 cần thêm nguồn công khai.

---

## 3. Xương sống câu chuyện

- **Câu hỏi trung tâm:** *Mỗi lần máy mới xuất hiện, người ta lại nói "lần này khác". 200 năm qua, lời đó sai bao nhiêu lần — và với
  AI, lần này có khác thật không?*
- **Cung A → B:** A = những người mà *nghề* bị máy lấy mất: thợ dệt 1811, "máy tính" bằng người, cô tổng đài, người lái thang máy.
  B = 2026: AI không (chưa) xoá nghề diện rộng, nhưng **cửa vào nghề** của người trẻ đang hẹp lại. Ở giữa: những lời tiên tri sai
  (Keynes, 1964, Oxford 2013, Hinton 2016) và một quy luật lặp lại: **máy lấy *việc vặt*, không lấy cả *nghề* — nhưng người đứng sai
  chỗ vẫn trả giá.**
- **Lời hứa lộ trình (phút 1), 3 câu hỏi:** (1) Máy móc đã từng thật sự cướp việc chưa — và *ai* mất? (2) Vì sao những lời tiên tri
  "máy sẽ thay người" thường sai, nhưng không phải lúc nào cũng sai? (3) Với AI, lần này khác ở đâu — và nó chạm tới ai trước?
- **Motif:** (a) **thẻ đục lỗ** — khung cửi Jacquard (ch1) → thẻ Hollerith/IBM (ch5, callback video #1) → "những tấm thẻ đã đi hết
  vòng" (ch8). (b) Câu **"lần này khác"** hiện bằng chữ đánh máy ở cold open, ch2, ch7, ch8.
- **Thời lượng:** ~14 phút ≈ 3.000–3.100 âm tiết ở 220 âm tiết/phút (tính cả lặng).

---

## 4. Dàn ý chương + dữ kiện

Ký hiệu vòng: **[Mở Vn]** / **[Đóng Vn]**. Ảnh: tên file Commons nguyên văn, tra tại `https://commons.wikimedia.org/wiki/File:<tên>`;
giấy phép là `LicenseShortName` đọc qua API ngày 07/10/2026. **Không BY-SA.** Mọi CC BY vào khối ghi công trong mô tả.

| # | Chương | Thời điểm | % video |
|---|---|---|---|
| 0 | Cold open — Nghề tên là "máy tính" | 0:00–1:15 | 0–9% |
| 1 | Những người đập máy (1811–1812) | 1:15–3:00 | 9–21% |
| 2 | "Lần này khác" — ba lời tiên tri | 3:00–4:35 | 21–33% |
| 3 | Cô tổng đài và người lái thang máy | 4:35–6:20 | 33–45% |
| 4 | Nghịch lý cây ATM (và đoạn kết thứ hai) | 6:20–7:30 | 45–54% |
| 5 | Re-hook: những "máy tính" đã đi đâu? | 7:30–9:10 | 54–65% |
| 6 | **Cảnh mạnh thứ hai:** lời tiên tri về bác sĩ X-quang | 9:10–10:50 | 65–77% |
| 7 | Lần này có khác không? (dữ liệu 2025–26 + Việt Nam) | 10:50–12:40 | 77–90% |
| 8 | Phim đã kể chuyện này thế nào + kết "Năm 2030 của Keynes" | 12:40–14:00 | 90–100% |

### 0. Cold open — "Nghề tên là 'máy tính'" (0:00–1:15)

- **Vòng:** [Mở V0] *"Trong một thế hệ, cái nghề ấy biến mất. Cái tên của nó được trao cho cỗ máy đã thay họ. Còn những người phụ nữ
  trong tấm ảnh này thì sao?"* → đóng ở ch5. Rồi chữ đánh máy **"LẦN NÀY KHÁC"** (motif) + lộ trình 3 câu hỏi.
- **Dữ kiện:**
  1. Trước máy tính điện tử, "computer" là **chức danh của người**: người làm phép tính bằng tay [bằng chứng] [3] (NASA tóm tắt bài
     *When the Computer Wore a Skirt*, NASA History News & Notes 29.1, 2012 [SECONDARY] [3a]).
  2. Phòng thí nghiệm Langley của NACA (tiền thân NASA) lập nhóm "computer" nữ đầu tiên năm **1935** [SECONDARY] [3a].
  3. Ảnh NACA 24/03/1952: các "computer" nữ với **máy tính cơ Friden**, xử lý dữ liệu máy bay thử nghiệm X-4 [bằng chứng: metadata
     Commons] [30].
  4. Katherine Johnson (NASA, 1953–1986) — khi NASA chuyển sang máy điện tử, người ta vẫn gọi bà để **kiểm tra quỹ đạo do máy tính**
     cho chuyến bay quanh Trái Đất của John Glenn [bằng chứng] [4]. (Giữ cho ch5.)
- **Cảnh kể được:** Hampton, Virginia, năm 1952. Một căn phòng đầy bàn, mỗi bàn một chiếc máy tính cơ kêu lách cách. "Máy tính" ở
  đây có tên, có lương, đi làm buổi sáng và về nhà buổi tối. Họ là con người. (Chi tiết "lách cách", "về nhà buổi tối" là mô tả chung;
  không nêu giờ làm/lương cụ thể nếu chưa kiểm.)
- **Hình:**
  - `Langley Women Computer with X-4 with Friden machine (LRC-1952-B701 P-74769).tiff` — **Public domain** (NASA Langley/NACA, 24/03/1952), 8227×6422 → **ảnh cold open + thumbnail**.
  - `NACA Laboratory Computers Help Compile Handbook (LRC-1951-B701 P-69568).tiff` — **Public domain** (NACA, Bill Taub, 06/03/1951), 8000×6119 (cùng loạt: `…P-69569`, `…P-69570`, `…P-69571`, `…P-69572`).
  - `Women Adequately Filling Posts In NACA Laboratory (LRC-1943-B701 P-33025).tiff` — **Public domain** (15/05/1943).
  - Tiff rất nặng: dùng ảnh thu nhỏ 1920 px của Commons (như `build.py` đang làm).

### 1. "Những người đập máy" (1811–1812)

- **Vòng:** [Mở V1] *"Khung cửi ấy đọc lệnh từ những tấm thẻ đục lỗ. Hãy nhớ những tấm thẻ này — chúng sẽ đi một chặng rất dài."* →
  đóng ở ch5 (ENIAC/IBM) và ch8. Câu "bài học": *họ không ghét máy, họ ghét việc máy bị dùng để ép lương* → dẫn sang ch2.
- **Dữ kiện:**
  1. Bạo loạn Luddite bắt đầu ở **Nottinghamshire năm 1811**, lan sang Yorkshire, Lancashire (1812), Leicestershire, Derbyshire;
     máy bị đập gồm khung dệt tất, khung dệt khổ rộng, **máy dệt chạy điện (power loom)**, máy xén vải [bằng chứng] [5].
  2. Lý do: **giảm lương và thất nghiệp do máy**, thêm chiến tranh Napoléon làm tắc thương mại [bằng chứng] [5].
  3. Họ đập có chọn lọc: một quan toà thời đó ghi họ hiếm khi động tới tài sản khác [bằng chứng: trích tài liệu trong [5]].
  4. "Ned Ludd / General Ludd" là **nhân vật huyền thoại** sống ở rừng Sherwood, không phải thủ lĩnh thật [bằng chứng] [5].
  5. Năm **1812** phá máy thành **tội tử hình** (Frame Breaking Act); năm **1813** có **17 người bị hành quyết** (phiên toà đặc biệt ở
     York) [bằng chứng] [5]. Lần phá máy đầu tiên: 11/03/1811 ở Arnold, 63 khung dệt [SECONDARY] [5a].
  6. Lord Byron phản đối dự luật trong bài phát biểu đầu tiên ở Thượng viện, 27/02/1812 [CHƯA KIỂM — Hansard chặn script] [5b].
     ✎ Vẫn chưa kiểm → **đã bỏ khỏi kịch bản**.
  7. Khung cửi **Jacquard** được cấp bằng sáng chế **1804**: thẻ đục lỗ quyết định sợi nào được nâng — lỗ = có, không lỗ = không
     [bằng chứng] [6]. Ada Lovelace (1843): Máy Giải tích của Babbage "weaves algebraic patterns" như khung Jacquard dệt hoa lá
     [bằng chứng] [6].
  8. Bessen (IMF 2015): máy dệt thế kỷ 19 tự động hoá **98%** lao động dệt một yard vải, vậy mà **số việc thợ dệt trong nhà máy vẫn
     tăng** [bằng chứng] [9] → mồi cho ch4.
- **Cảnh kể được:** đêm tháng 11/1811, ngoại ô Nottingham. Một nhóm thợ đeo mặt nạ, cầm búa tạ, vào xưởng, đập đúng những khung dệt
  của chủ xưởng ép lương — rồi đi, không lấy gì khác. Sáu tháng sau, việc ấy có thể khiến họ lên giá treo cổ. (Không bịa thoại; chi
  tiết "mặt nạ, búa tạ" là mô tả phổ biến **[CHƯA KIỂM]** → hoặc kiểm lại [5], hoặc chỉ nói "ban đêm".)
- **Hình:**
  - `Luddite.jpg` — **Public domain** (tranh khắc "The Leader of the Luddites", in 05/1812), 3021×3988.
  - `Powerloom weaving in 1835.jpg` — **Public domain** (T. Allom / J. Tingle, 1835), 3215×2077.
  - `Jacquard loom cards.jpg` — **CC0** (Robert-brook, 2020), 1536×2048 — cận cảnh thẻ.
  - `PSM V39 D325 Carpet loom with jacquard attachment.jpg` — **Public domain** (1891).
  - `Ada Lovelace portrait.jpg` — **Public domain** (A. E. Chalon, ~1840), 2439×3504.
  - (Tuỳ chọn) `Wooden Jacquard loom MOSI-11 5545.JPG` — **CC BY 3.0** (Clem Rutter) — ghi công.

### 2. "Lần này khác" — ba lời tiên tri (1930, 1964, 2013)

- **Vòng:** [Mở V2] Keynes hẹn **tuần làm 15 giờ** cho "cháu chắt" — tức khoảng năm **2030** → đóng ở ch8 ("còn 4 năm").
  [Mở V3] Oxford 2013: **47%** việc làm Mỹ "rủi ro cao", "có lẽ trong một hai thập kỷ" → đóng ở ch7 ("đã 13 năm").
  Quy tắc 3 mục, mục thứ ba (con số 47%) là mục người xem từng nghe nhất.
- **Dữ kiện:**
  1. **Keynes, 1930**, *Economic Possibilities for our Grandchildren*: gọi tên "một căn bệnh mới" — **technological unemployment**
     (thất nghiệp do công nghệ); dự đoán mức sống 100 năm sau cao gấp **4 đến 8 lần**; và "three-hour shifts or a fifteen-hour week"
     [bằng chứng: bản chép lại toàn văn] [7].
  2. **22/03/1964**, bản ghi nhớ *The Triple Revolution* gửi Tổng thống Lyndon B. Johnson, người ký có **Linus Pauling** (2 giải
     Nobel), Gunnar Myrdal…; cảnh báo máy tính + máy tự động ("cybernation") sẽ sớm gây thất nghiệp hàng loạt [SECONDARY] [10].
     ✎ **[bằng chứng]**: F. Levy & R. Murnane, *The New Division of Labor* (Princeton UP, 2004), chương 1 (PDF chương mẫu của NXB)
     — bản ghi nhớ **14 trang** gửi Tổng thống Johnson ngày 22/03/1964; người ký gồm Linus Pauling (2 Nobel), Gunnar Myrdal (sau này
     Nobel), Gerard Piel; cảnh báo máy tính sẽ sớm gây thất nghiệp hàng loạt [38]. Cùng chương nhận xét: máy tính **không** gây thất
     nghiệp hàng loạt nhưng làm đảo lộn bản chất công việc.
  3. Johnson lập Uỷ ban quốc gia về Công nghệ, Tự động hoá và Tiến bộ kinh tế (08/1964); báo cáo 02/1966 viết: công nghệ xoá **việc
     (jobs)**, không xoá **lao động (work)** — khi đó thất nghiệp Mỹ 3,8% [SECONDARY] [11].
     ✎ Đã mở được bài Conversable Economist (bản blogspot): câu nguyên văn "technology eliminates jobs, not work" + 3,8% khớp; vẫn
     **[SECONDARY]** (chưa mở báo cáo 1966) → trong kịch bản đọc dạng **[DIỄN Ý]**, không đọc 3,8%.
  4. **Frey & Osborne, Oxford (19/09/2013)**: xét **702** nghề, ước tính **47%** việc làm Mỹ thuộc nhóm rủi ro cao, có thể tự động hoá
     "perhaps a decade or two" [bằng chứng] [15]. Nghề được chấm xác suất cao nhất có **nhân viên chào hàng qua điện thoại**
     (telemarketer, 0,99) [bằng chứng] [15]. Trang Oxford Martin hiện ghi đồng tác giả là **Dr Maike Osborne** [bằng chứng] [15a] → trong
     lời đọc chỉ nói "hai nhà nghiên cứu ở Oxford".
- **Cảnh kể được:** tháng 3/1964, một phong bì tới Nhà Trắng. Bên trong là lời cảnh báo ký bởi một người hai lần đoạt Nobel: máy
  tính sắp lấy việc của hàng triệu người Mỹ. Hai năm sau, chính uỷ ban của Tổng thống trả lời bằng một câu ngắn. (Không đọc nguyên
  văn câu trả lời nếu chưa mở bản gốc; diễn ý + nhãn **DIỄN Ý**.)
- **Hình:**
  - `John Maynard Keynes 1929.jpg` — **Public domain**, 2048×1591 (hoặc `John Maynard Keynes (1929).jpg`, PD, 749×999).
  - `President Lyndon B. Johnson with reporters on Election Night 1964.jpg` — **Public domain** (LBJ Library, Cecil Stoughton) — gắn **ẢNH MINH HỌA** (không phải cảnh nhận bản ghi nhớ).
  - 47% / 702 nghề / 0,99: **biểu đồ tự vẽ** (thanh xác suất, không chép hình của bài báo).

### 3. "Cô tổng đài và người lái thang máy" (1920–1950s)

- **Vòng:** [Đóng V0 một phần] nghề biến mất thật. [Mở V4] *"Nghề biến mất. Nhưng ai là người trả giá — người đang làm, hay người
  sắp vào nghề?"* → đóng ở ch7 (đảo chiều thời AI).
- **Dữ kiện:**
  1. Đầu thế kỷ 20, tổng đài viên điện thoại là **một trong những nghề phổ biến nhất của phụ nữ Mỹ**; từ **1920 đến 1940**, AT&T thay
     tổng đài viên bằng **tổng đài chuyển mạch cơ khí ở hơn một nửa mạng điện thoại Mỹ** [bằng chứng] [8].
  2. Kết quả (Feigenbaum & Gross, *Quarterly Journal of Economics* 139(3), 2024): tự động hoá **xoá phần lớn** việc tổng đài, nhưng
     **không làm giảm việc làm của các thế hệ sau** — bù lại bằng việc văn phòng tầm trung và dịch vụ, kể cả những loại việc mới
     [bằng chứng] [8].
  3. Nhưng **người đang làm tổng đài** chịu thiệt nhất: 10 năm sau, họ dễ làm nghề lương thấp hơn **hoặc không còn đi làm** [bằng
     chứng] [8]. Phương pháp: nối điều tra dân số qua phả hệ [bằng chứng] [8].
     ✎ Đối chiếu lại nguyên văn tóm tắt NBER w28061 (bản 02/2024 = bản QJE 139(3):1879–1939): "among the most common jobs for
     American women"; AT&T "one of the largest automation investments in modern history", thay người "in over half of the U.S.
     telephone network"; "eliminated most of these jobs" nhưng "did not reduce future cohorts' overall employment" — bù bằng việc
     văn phòng tầm trung và dịch vụ tầm thấp, "including in new categories of work"; người đang làm "a decade later more likely to be
     in lower-paying occupations or no longer working". Đối tượng nghiên cứu là **phụ nữ trẻ** → **[bằng chứng]**, giữ nguyên.
  4. Thang máy tự động có từ khoảng **1900** nhưng người ta không dám đi; tháng 9/**1945**, khoảng **15.000** người lái thang máy,
     gác cửa, khuân vác ở New York đình công; **1,5 triệu** nhân viên văn phòng không tới được chỗ làm; thành phố thiệt ~100 triệu USD
     tiền thuế → ngành thang máy quyết chuyển sang tự động và quảng cáo để người ta tin [SECONDARY: NPR phỏng vấn sử gia Lee Gray +
     Wikipedia] [16]. (Ngày cụ thể: Wikipedia ghi 09/1945; một số nguồn ghi 04/1945 → chỉ nói "năm 1945" **[CHƯA KIỂM tháng]**.)
     ✎ Đọc bản text của NPR (text.npr.org/427990392): **[bằng chứng]** cho: thang không người lái "in 1900", người ta bước vào rồi
     bước ra; năm 1945 đình công ở New York; thiệt **100 triệu USD** tiền thuế; **1,5 triệu** nhân viên văn phòng không tới được chỗ
     làm; quảng cáo có trẻ em bấm nút, bà cụ đi thang; giọng thu âm + nút STOP đỏ; mất **hơn 50 năm** công chúng mới quen. Con số
     **15.000 người đình công không có trong NPR → không đọc**. Tháng vẫn chưa kiểm → chỉ nói "năm 1945".
- **Cảnh kể được (ngắn, ~25 giây):** sáng thứ Hai năm 1945, Manhattan. Hàng triệu người đứng dưới chân những toà nhà chọc trời — thang
  máy đứng im, vì người lái thang đình công. Không ai muốn leo 40 tầng. Mười năm sau, người ta bước vào thang, tự bấm nút. (Chi tiết
  "thứ Hai", "40 tầng" là minh hoạ → không nêu, hoặc gắn **DIỄN Ý**.)
- **Hình:**
  - `Photograph of Women Working at a Bell System Telephone Switchboard (3660047829).jpg` — **No restrictions** (U.S. National Archives), 2778×2207.
  - `Female Indian telephone switchboard operator - "Helen of Many Glacier Hotel.", 26 June 1925 LCCN2014718418.jpg` — **Public domain** (Bain News Service, 1925) — chú ý chú thích đúng người.
  - `Strowger switches - Telephone Museum - Waltham, Massachusetts -DSC08180.jpg` — **CC0** (Daderot) — tổng đài cơ khí thay người.
  - `First electromagnetic selector of Almon B Strowger.jpg` — **CC0** (Reinraum).
  - `Elevator girl, Martha Washington Hotel in 1917.jpg` — **Public domain** (Bain, 1917) → **ẢNH MINH HỌA** (không phải New York 1945).
  - Bản đồ/đồ hoạ "1,5 triệu người": tự vẽ.

### 4. "Nghịch lý cây ATM" (1970s–2035)

- **Vòng:** [Mở V5] *"Câu chuyện ATM có một đoạn kết thứ hai"* → đóng ngay cuối chương (bài học kép). Câu cầu nối sang ch5: *"Vậy còn
  những 'máy tính' bằng xương bằng thịt ở đầu video?"* (re-hook giữa video).
- **Dữ kiện:**
  1. ATM xuất hiện ở Mỹ từ **thập niên 1970**, đến 2015 có **hơn 400.000** máy; số giao dịch viên **không giảm** khi ATM lan rộng
     [bằng chứng] [9].
  2. Cơ chế: số giao dịch viên mỗi chi nhánh giảm **20 → 13 (1988–2004)**, nhưng chi nhánh rẻ hơn nên ngân hàng mở thêm — chi nhánh
     ở đô thị **tăng 43%**; việc còn lại (tư vấn, bán dịch vụ) có giá trị hơn [bằng chứng] [9].
  3. **Đoạn kết thứ hai:** BLS (Mỹ) — năm 2025 còn **339.200** giao dịch viên, dự báo **giảm 13%** giai đoạn **2025–2035**, vì người
     ta gửi séc bằng điện thoại, ít tới quầy [bằng chứng] [17]. Đỉnh số giao dịch viên thời ATM (~600.000) **[CHƯA KIỂM — tra BLS OES
     trước khi đọc số]**.
     ✎ Mở lại OOH 06/10/2026: "339,200 jobs in 2025", "-13 percent from 2025 to 2035" (−44.700), lý do: "mobile check deposits" →
     ít khách tới quầy, và máy ATM/ki-ốt video làm ít giao dịch viên mỗi chi nhánh; lương trung vị 43.030 USD (05/2025) [bằng chứng].
     **Đối chiếu ≥ 3 mốc (quy tắc retro #2):**
     - Chuỗi Employment Projections (cùng chuỗi với số 339.200, gồm cả lao động tự làm): **2014: 520,5 nghìn** (MLR 12/2015, bảng 5,
       dự báo 2024: 480,5 nghìn, −7,7%) [39] → **2025: 339,2 nghìn** [17]. Giảm 181,3 nghìn = **−34,8%** (tự tính).
     - Chuỗi OES/OEWS (chỉ lao động hưởng lương, thấp hơn EP vài %): 05/2018 **468.470** · 05/2019 **442.120** · 05/2020 **423.570** ·
       05/2021 **364.210** · 05/2023 **340.820** [40]. Xu hướng giảm đều, khớp chiều với chuỗi EP.
     - Đỉnh ~600.000: **vẫn chưa kiểm** (bảng OES trước 2019 chỉ có file zip, BLS trả 403 với script) → **không đọc**; thay bằng mốc
       2014 → 2025. Không trộn hai chuỗi trong cùng một câu đọc.
  4. Bài học (lời của kênh): máy lấy **một việc vặt** (đếm tiền) thì nghề có thể **lớn lên**; thứ thay đổi **cả cách khách hàng hành
     xử** (ngân hàng trên điện thoại) mới thu nhỏ nghề.
- **Cảnh kể được:** đặt hai hình cạnh nhau: một máy ATM, một chiếc điện thoại. Cái thứ nhất không lấy được việc của giao dịch viên.
  Cái thứ hai thì có.
- **Hình:**
  - `Automated teller machine.JPG` — **Public domain** (Elph), 4320×3240.
  - `ATM-Croatia-2024.jpg` — **CC0** (Gewild).
  - Biểu đồ 20 → 13, +43%, 339.200, −13%: tự vẽ, ghi nguồn IMF/BLS trên màn hình.
  - B-roll Pexels: tay gửi tiền qua app ngân hàng (không lộ logo).

### 5. Re-hook ~50%: "Những 'máy tính' đã đi đâu?" (1943–1971)

- **Vòng:** [Đóng V0] *"Giờ bạn đã biết những người phụ nữ ở đầu video đi đâu."* [Đóng V1] thẻ đục lỗ: từ khung cửi tới máy tính điện
  tử — và tới chiếc IBM 704 của video trước (callback một câu). [Mở V6] *"Năm 2016, người được gọi là 'cha đẻ học sâu' đưa ra một lời
  tiên tri về một nghề cụ thể."* → ch6.
- **Dữ kiện:**
  1. **Dorothy Vaughan** tới Langley năm **1943**, làm ở nhóm "West Area Computing" — nhóm toàn nữ toán học gia da đen, **bị tách
     riêng vì luật phân biệt chủng tộc**; năm **1949** thành **người giám sát da đen đầu tiên** của NACA [bằng chứng] [4a].
  2. Năm 1958 NACA thành NASA, phòng tách biệt bị xoá; Vaughan vào **Phòng Phân tích và Tính toán (ACD)** — "tiền tuyến của tính
     toán điện tử" — và trở thành **lập trình viên FORTRAN** giỏi; nghỉ hưu **1971** [bằng chứng] [4a]. Bà không bao giờ được giữ chức
     quản lý nữa [bằng chứng] [4a] → nói rõ: chuyển nghề thành công, nhưng **không phải không có giá**.
  3. **Katherine Johnson** được gọi để kiểm tra quỹ đạo máy tính tính cho chuyến bay của John Glenn [bằng chứng] [4].
  4. **ENIAC**: Lục quân Mỹ thuê gần **100 phụ nữ** làm "computer" ở Trường Moore (ĐH Pennsylvania), lương ~**1.620 USD/năm**, tính
     bảng đạn đạo; **6 người** trong số đó thành những lập trình viên đầu tiên của ENIAC [SECONDARY] [18]. Danh sách 6 người: Kay
     McNulty, Jean Jennings, Betty Snyder (Holberton), Marlyn Wescoff, Fran Bilas, Ruth Lichterman; họ phát triển **chương trình con,
     vòng lặp lồng nhau** [bằng chứng] [19].
  5. ENIAC ra mắt công chúng **15/02/1946** (tròn **80 năm** trong năm nay); trong buổi trình diễn, máy tính một quỹ đạo đạn trong
     **20 giây** — nhanh hơn thời gian viên đạn bay [SECONDARY] [18].
     ✎ **Đổi theo Penn Engineering [bằng chứng] [18]:** ENIAC "originally announced on February 14, 1946" (ngày 15/02 thường được nêu
     là lễ khánh thành → trong lời đọc chỉ nói **"tháng 2 năm 1946"**); một bài toán đạn đạo mất **12 giờ** tính tay, ENIAC giải trong
     **30 giây** (thay cho chi tiết "20 giây, nhanh hơn viên đạn" — chưa kiểm, **bỏ**); phòng 30×50 feet, 30 tấn, 18.000 bóng đèn
     chân không; 6 nữ lập trình viên: Kathleen McNulty Mauchly Antonelli, Jean Jennings Bartik, Frances (Betty) Snyder Holberton, Marlyn
     Wescoff Meltzer, Frances Bilas Spence, Ruth Lichterman Teitelbaum; trước đó họ là nhân viên dân sự ở Trường Moore "calculate
     bullet and missile trajectories". Số người làm "computer": nguồn vênh nhau ("nearly 100" ở BRL theo Army/APS; "at least 200" ở
     Trường Moore theo nguồn khác) → **không đọc con số**; lương 1.620 USD/năm chưa mở được (army.mil chặn) → **không đọc**.
     Dorothy Vaughan: NASA ghi sinh **20/09/1910**, tới Langley **12/1943** → năm 1958 bà **48 tuổi** (tự tính) — ✎ hết [CHƯA KIỂM];
     NASA: bà "sought, but never received, another management position at Langley" [bằng chứng] [4a].
  6. Máy đục thẻ Hollerith/IBM dùng cho điều tra dân số Mỹ [bằng chứng: metadata NARA trên Commons] [30] → nối thẻ Jacquard → thẻ
     IBM 704 (video #1).
- **Cảnh kể được:** 1958, Langley. Tấm biển "West Area Computing" được gỡ xuống. Một phụ nữ ngoài 40 tuổi ngồi vào lớp học FORTRAN —
  thứ ngôn ngữ của chính cỗ máy sắp làm thay việc của nhóm bà. (Tuổi: sinh 1910 → 48 tuổi năm 1958 **[CHƯA KIỂM năm sinh]**; chi tiết
  "gỡ biển" là **DIỄN Ý**.)
- **Hình:**
  - `L Dorothy Vaughan M Lessie Hunter R Vivian Adair.jpg` — **Public domain** (NASA), 1896×1502 — chú thích đúng 3 người.
  - `Dorothy Vaughan 2.jpg` — **Public domain** (NASA on The Commons), 985×1255. **Cảnh báo:** Commons có nhiều file "Dorothy Vaughan"
    là **diễn viên cùng tên** (1909–1946, phim/tạp kỹ) → chỉ dùng file có nguồn NASA.
  - `NASA human computers - Katherine Coleman Goble Johnson.jpg` — **Public domain** (NASA), 2400×3000; `Katherine johnson john glenn.png` — **Public domain** (NASA).
  - `Two women operating ENIAC (full resolution).jpg` — **Public domain** (Lục quân Mỹ, 1946), 5682×3899.
  - `Reprogramming ENIAC.png` — **Public domain** (Lục quân Mỹ, 1946); `Betty Jennings (Mrs. Bartik).jpg` — **Public domain**.
  - `Glen Beck and Betty Snyder program the ENIAC in building 328 at the Ballistic Research Laboratory.jpg` — **Public domain** (~1947).
  - `This is a card puncher, an integral part of the tabulation system used by the United States Census Bureau to compile... - NARA - 513295.jpg` — **Public domain** (NARA).
  - `IBM card storage.NARA.jpg` — **Public domain** (NARA, 11/1959).

### 6. Cảnh mạnh thứ hai (~65–77%): "Lời tiên tri về bác sĩ X-quang" (2016 → 2025)

- **Vòng:** [Đóng V6]. Mở cầu nối: *"Nếu chuyên gia giỏi nhất cũng đoán sai — thì dữ liệu nói gì về chính lúc này?"* → ch7.
- **Dữ kiện:**
  1. Tại hội nghị của Creative Destruction Lab (Toronto, **24/11/2016**), Geoffrey Hinton nói nên **ngừng đào tạo bác sĩ X-quang ngay**
     vì trong 5 năm học sâu sẽ giỏi hơn họ [SECONDARY: dẫn qua Works in Progress, NYT, The Decoder] [20][21]. Video gốc có công khai —
     **kiểm nguyên văn bằng cách nghe lại trước khi đọc**; trên màn hình chỉ trích cụm "stop training radiologists".
  2. Một phần ông đúng: mô hình AI đã vượt bác sĩ trên nhiều bài kiểm tra chuẩn; FDA (Mỹ) đã cho phép **hơn 1.000** thiết bị y tế có
     AI, **~76%** thuộc chẩn đoán hình ảnh (tính tới cuối 2025) [SECONDARY] [22].
  3. Nhưng: năm 2025, các chương trình nội trú X-quang Mỹ mở **kỷ lục 1.208** suất (+4% so với 2024); thu nhập trung bình ~**520.000
     USD**, ngành có thu nhập cao thứ hai [SECONDARY] [21]. Ở Mayo Clinic số bác sĩ X-quang **tăng 55%** từ 2016 [SECONDARY: NYT
     14/05/2025] [20].
  4. Vì sao: một nghiên cứu năm 2012 ở 3 bệnh viện thấy bác sĩ X-quang chỉ dành **~36%** thời gian để đọc ảnh — còn lại là trao đổi
     với bác sĩ khác, bệnh nhân, thủ thuật [SECONDARY] [21]; mô hình chạy tốt trên bài thi nhưng kém hơn trong bệnh viện thật; mỗi mô hình
     chỉ đọc một loại bất thường [SECONDARY] [21].
  5. Năm 2025 chính Hinton nói với NYT rằng ông đã **nói quá rộng** năm 2016 [SECONDARY] [20].
  ✎ **Kết quả kiểm chứng ch6 (06/10/2026):**
  - Works in Progress **mở được** bằng WebFetch → **[bằng chứng]** cho: Hinton 2016 "people should stop training radiologists now";
    2025 "a record **1,208** positions across all radiology specialties, a **four percent** increase from 2024"; "second-highest-paid
    medical specialty", "average income of **$520,000**, over **48 percent** higher than … 2015"; nghiên cứu 2012 ở **3 bệnh viện**:
    "only **36 percent** of their time" đọc ảnh trực tiếp. Đối chiếu NRMP 2025 (qua tóm tắt AuntMinnie/NRMP): X-quang chẩn đoán PGY-2
    1.057 suất + PGY-1 151 suất = **1.208** (tự cộng, khớp).
  - FDA: **đổi** "hơn 1.000 thiết bị, ~76%" [SECONDARY] → theo WIP: "over **700** FDA-cleared radiology models", "more than
    **three-quarters** of all medical AI devices" [bằng chứng qua WIP]. Trong lời đọc dùng số WIP.
  - Nguyên văn Hinton: câu 1 khớp ở WIP, NYT (qua tóm tắt), EMJ; câu 2 "It's just completely obvious that within five years deep
    learning is going to do better than radiologists" khớp ở ≥ 3 nguồn độc lập [SECONDARY+]. **Chưa nghe lại video** (không mở
    YouTube theo quy định) → trên màn hình chỉ trích câu 1; câu 2 đọc dạng diễn ý. Ngày 24/11/2016 vẫn [SECONDARY] → lời đọc chỉ nói
    "năm 2016, ở Toronto".
  - Mayo Clinic +55%: WIP **không có**; NYT paywall; The Decoder thuật lại NYT: ~**260** (2016) → **hơn 400** (2025) = +55% (400/260 =
    1,54, tự tính, khớp) → vẫn [SECONDARY, 2 nguồn khớp] → **chỉ đọc kèm "theo báo New York Times"**.
  - Hinton 2025 "spoke too broadly", chỉ nói về phân tích ảnh: [SECONDARY, ≥ 3 nguồn khớp] → đọc kèm "nói với New York Times".
- **Cảnh kể được:** Toronto, cuối năm 2016. Người đàn ông sau này nhận Nobel đứng trước khán phòng, nói một câu khiến cả ngành y giật
  mình. Cắt sang: 2025, Rochester, Minnesota — một phòng đọc phim có nhiều bác sĩ X-quang hơn bao giờ hết, trên màn hình của họ là
  những ô gợi ý của AI. (Khung cảnh phòng đọc phim là **ẢNH MINH HỌA**/b-roll.)
- **Hình:**
  - `Geoffrey Hinton - Collision 2023 - Centre Stage RCZ 1307 (cropped).jpg` — **CC BY 2.0** (đã dùng ở video #1, cùng ghi công).
  - `Chest radiograph with signs of congestive heart failure - annotated.jpg` — **CC0** (Mikael Häggström) — ảnh X-quang có khoanh vùng, hợp "AI gợi ý".
  - `Chest Xray PA 3-8-2010.png` — **CC0** (Stillwaterising).
  - Biểu đồ 1.208 suất / 36% thời gian / 76% thiết bị: tự vẽ.
  - B-roll Pexels: phòng đọc phim, màn hình y tế (không lộ mặt bệnh nhân).

### 7. "Lần này có khác không?" (2023–2026, và Việt Nam)

- **Vòng:** [Đóng V3] Oxford 2013 hẹn "một hai thập kỷ" — đã 13 năm. [Đóng V4] **đảo chiều**: thời tổng đài, người *đang làm* chịu
  thiệt; thời AI, người *mới vào nghề* chịu thiệt trước. Không mở vòng mới (chuẩn bị kết).
- **Dữ kiện:**
  1. **Yale Budget Lab (01/10/2025):** 33 tháng sau ChatGPT, thị trường lao động Mỹ **chưa có xáo trộn rõ rệt**; cơ cấu nghề đổi nhanh
     hơn trước một chút, nhưng xu hướng đó **có từ trước AI**; các chỉ số phơi nhiễm AI **chưa liên quan** tới thay đổi việc làm/thất
     nghiệp [bằng chứng] [13]. Lần dịch chuyển do máy tính và Internet trước đây diễn ra **qua nhiều thập kỷ** [bằng chứng] [13].
  2. **Stanford Digital Economy Lab (12/08/2026)**, dữ liệu bảng lương ADP: **không** thấy mất việc diện rộng; nhưng người **22–25 tuổi**
     trong nghề phơi nhiễm AI cao có việc làm **thấp hơn ~19%** so với nếu theo kịp bạn cùng tuổi ở nghề ít phơi nhiễm (con số này là 15%
     một năm trước); người nhiều kinh nghiệm **không** có khoảng cách tương tự; cơ chế chủ yếu là **tuyển ít người trẻ hơn**, không phải
     sa thải; giảm ở nghề dựa vào **kiến thức viết thành văn bản** (codified), tăng ở nghề dựa vào **kinh nghiệm ngầm** (tacit); tác giả
     nói rõ đây là **mô tả, chưa phải ước lượng nhân quả** [bằng chứng] [12].
  3. **ILO (05/2025):** khoảng **1/4** việc làm toàn cầu ở nghề có phơi nhiễm AI tạo sinh; chỉ **3,3%** ở mức phơi nhiễm cao nhất (nữ
     4,7%, nam 2,4%); **nhân viên văn phòng/hành chính** phơi nhiễm cao nhất; khả năng lớn là **thay đổi công việc**, không phải mất việc
     hàng loạt [SECONDARY: UN News + tóm tắt] [14] → ✎ **[bằng chứng]** (xem khối kiểm chứng ch7 bên dưới).
  4. **Việt Nam:** 61% lo mất việc vì AI (UNDP) [SECONDARY] [33]. **Kiểm tra một lời tiên tri:** năm 2016 ILO ước **86%** lao động làm công
     ngành dệt–may–da giày Việt Nam có **rủi ro tự động hoá cao** [SECONDARY] [23]; năm 2025 ngành dệt may xuất khẩu ~**46 tỉ USD** và vẫn
     dùng **hơn 3 triệu** lao động [SECONDARY] [24]; một nghiên cứu của chính ILO năm 2021 thấy tự động hoá trong ngành may **vẫn còn hạn
     chế** [SECONDARY] [25]. → Nói "chưa xảy ra *đến giờ*", không nói "ILO sai".
  5. Frey–Osborne 2013 → việc làm Mỹ: khoảng 136 triệu (2013) → khoảng 159 triệu (2025) **[CHƯA KIỂM — tra BLS CES0000000001 / FRED
     PAYEMS và đối chiếu ≥ 3 mốc theo quy tắc retro trước khi đọc]**. Không suy ra "Oxford sai" — bài báo chỉ nói *có thể* tự động hoá.
     ✎ **[bằng chứng]** FRED PAYEMS (cập nhật 02/10/2026, nghìn người, có điều chỉnh mùa vụ) [41]: 09/2013 **136.821** · 11/2016
     **145.183** · 12/2019 **151.794** · 11/2022 **154.242** · 09/2025 **158.548** · 09/2026 **159.044**. 09/2013 → 09/2026: +22,2 triệu
     (+16,2%, tự tính). Lưu ý: số mới nhất là ước tính sơ bộ, có thể còn sửa.
  ✎ **Kiểm chứng ch7 (06/10/2026):**
  - **Stanford [12] — định nghĩa chính xác "19%":** "Employment among workers ages **22–25** in highly AI-exposed occupations now stands
    about **19% below where it would be if it had kept pace with** employment among similarly aged workers in less-exposed
    occupations". Khoảng cách là **15% ở dữ liệu 07/2025** → **19% ở dữ liệu 06/2026**. Mốc gốc **11/2022**; phơi nhiễm theo thước đo
    Eloundou et al. (2024); chú thích: việc làm tuyệt đối của nhóm 22–25 ở **hai nhóm ngũ phân vị phơi nhiễm cao nhất giảm ~11%** từ
    11/2022 đến 06/2026. Người nhiều kinh nghiệm: "no comparable gap". Cơ chế: "reduced hiring of young workers rather than increased
    separations". Codified/tacit: việc làm **giảm ở người trẻ** trong nghề dựa vào kiến thức thành văn; **tăng ở người nhiều kinh
    nghiệm** trong nghề dựa vào kiến thức ngầm (✎ chính xác hoá: "tăng" là của *người nhiều kinh nghiệm*, không phải của mọi người).
    "descriptive patterns, not causal estimates". Nguồn dữ liệu ADP; tác giả Brynjolfsson, Chandar, Chen; 12/08/2026.
  - **ILO 2025 [14] → [bằng chứng] ✎** (PDF WP140, bản lưu ở EconStor/kho ILO, 05/2025, Gmyrek và cộng sự): "one in four workers are in
    an occupation with some GenAI exposure"; "3.3% of global employment falls into the highest exposure category", nữ 4,7% / nam 2,4%;
    "Clerical occupations continue to have the highest exposure levels"; "transformation of jobs is the most likely impact"; thêm:
    tổng phơi nhiễm 11% ở nước thu nhập thấp vs 34% ở nước thu nhập cao.
  - **ILO 2016 "86%" [23] → [bằng chứng một phần] ✎:** trang ILO trả 403 (cả qua curl, Wayback bị giới hạn). Bản gốc thay thế:
    ILO–IFC Better Work, *Discussion Paper 36* (Bárcia de Mattos, Eisenbraun, Kucera, Rossi, **05/2020**) [25a] — **[bằng chứng]**: dẫn
    Chang, Huynh & Rynhart (2016): **"between 64 and 88 per cent"** lao động dệt–may–da giày ở **Campuchia, Indonesia và Việt Nam** có
    rủi ro cao bị thay; nhấn mạnh ước tính là rủi ro "could be automated, and not that they will"; kết luận tự động hoá trong may mặc
    "remains limited" và các ước tính rủi ro "overstated". Con số riêng **86% cho Việt Nam** chỉ thấy qua đoạn trích công cụ tìm kiếm
    của PDF ILO → **trong lời đọc dùng khoảng 64–88% cho ba nước**, không đọc "86%".
  - **Thay số "hơn 3 triệu lao động 2025" [SECONDARY]** bằng số có nguồn gốc: bảng 1 của DP36 (UNIDO): lao động chính thức ngành may
    mặc + giày da Việt Nam **511.364 (khoảng 2000) → 2.984.980 (2017)** [bằng chứng] — gấp **5,84 lần** (tự tính). Xuất khẩu 2017:
    44,1 tỉ USD. Số 2025 (46 tỉ USD, ước của VITAS) nhiều báo khớp nhưng vẫn [SECONDARY] → không cần đọc.
  - [25] (ILR 2021) là bản tạp chí của chính DP36; trang Wiley chặn → dẫn DP36.
  6. Lời của kênh (phân tích, không phải dữ kiện): *"Lần này, cánh cửa bị khép trước là cửa vào nghề. Người trẻ học những thứ đã viết
     sẵn trong sách — đúng thứ AI đọc giỏi nhất."* Không đưa lời khuyên chọn nghề.
- **Cảnh kể được:** hai bức ảnh nhóm ghép cạnh nhau — năm 1930, những cô tổng đài trẻ: thế hệ sau họ vẫn có việc, chính họ thì không.
  Năm 2026, một lớp sinh viên mới ra trường: người có kinh nghiệm vẫn giữ việc, cửa vào thì hẹp lại. (Ảnh sinh viên: Pexels, **ẢNH MINH
  HỌA**, không nhận diện được ai.)
- **Hình:**
  - Biểu đồ đường 22–25 tuổi vs các nhóm khác (tự vẽ theo số trong [12], **không chép hình** của Stanford); thanh 15% → 19%.
  - `Sơ đồ Nhà máy Dệt Nam Định (Bảo tàng tỉnh Nam Định).jpg` — **Public domain** (chính quyền bảo hộ Pháp, 1910s), 10000×5055 — neo câu
    chuyện dệt may Việt Nam; năm thành lập nhà máy **[CHƯA KIỂM]**, chỉ nói "đầu thế kỷ 20".
  - B-roll Pexels: xưởng may, văn phòng, người trẻ gõ máy tính (không logo).

### 8. Văn hoá đại chúng + kết mở — "Năm 2030 của Keynes" (~90–100%)

- **Vòng:** [Đóng V2] Keynes hẹn tuần làm 15 giờ — còn **4 năm**. Trả motif: thẻ đục lỗ đi từ khung cửi tới ô chat; câu "lần này khác"
  hiện lần cuối, có dấu hỏi.
- **Văn hoá đại chúng (3 mục, mục ba bất ngờ nhất — chỉ nêu mốc, không dùng hình phim):**
  1. *Modern Times* (1936) — Charlie Chaplin làm công nhân bị cuốn vào bánh răng dây chuyền [CHƯA KIỂM ngày phát hành, Wikipedia] [26].
     ✎ Wikipedia: công chiếu 05/02/1936 (New York); nhân vật "getting stuck within a machine" → đọc năm 1936 [Wikipedia, đủ cho mốc năm].
  2. *The Jetsons* (1962) — ông bố tương lai đi làm chỉ để bấm nút, rất ít giờ mỗi tuần [CHƯA KIỂM số giờ cụ thể — không nêu số] [26].
     ✎ Wikipedia: phát sóng 23/09/1962; ghi "an hour a day, two days a week" — chỉ có Wikipedia → **vẫn không nêu số giờ**.
  3. *Hidden Figures* (2016) — chính là câu chuyện những "máy tính" ở đầu video [bằng chứng: NASA nhắc phim] [4a]; năm 2024 Quốc hội Mỹ
     trao Huân chương Vàng cho các "Hidden Figures" (ảnh NASA 18/09/2024) [bằng chứng: metadata Commons] [30].
- **Kết:**
  1. Keynes 1930: tuần 15 giờ và mức sống gấp 4–8 lần [bằng chứng] [7] — mức sống thì có thể đã tới; tuần 15 giờ thì chưa ai thấy
     (câu nhận xét của kênh, không nêu số liệu giờ làm nếu chưa kiểm).
  2. Câu của uỷ ban 1966: công nghệ xoá *việc*, không xoá *lao động* [SECONDARY] [11] — nhưng lịch sử tổng đài cho thấy **người đứng sai
     chỗ vẫn trả giá** [bằng chứng] [8].
  3. Câu hỏi để lại: *"Phần nào trong công việc của bạn là thứ đã viết sẵn trong sách — và phần nào chỉ bạn mới biết?"* (lấy từ phân biệt
     codified/tacit của [12]). Mời bình luận nghề của mình.
- **Hình:**
  - `Hidden Figures Congressional Gold Medal Ceremony (NHQ202409180015).jpg` — **Public domain** (NASA/Joel Kowsky, 18/09/2024).
  - `Katherine Johnson at NASA, in 1966 - Original.jpg` — **Public domain** (NASA) — trả lại tông ảnh cold open.
  - Không dùng ảnh/poster/khung hình phim (bản quyền + chính sách kênh). Dựng biểu tượng trừu tượng: bánh răng, nút bấm, bảng tính.

**Kiểm checklist RETENTION:** cold open có cảnh + câu hỏi chưa trả lời ✔ · 7 vòng (V0–V6) đóng ở chương sau ✔ · danh sách ≤ 3 mục
✔ (ch2, ch8) · motif xuất hiện ≥ 3 lần ✔ · cảnh mạnh ở 65–77% ✔ · mọi con số có nguồn + năm ✔ (trừ các mục [CHƯA KIỂM] phải xử lý).
Pattern interrupt gợi ý: câu hỏi tu từ ở 1:15, 3:00, 4:35, 6:20, 7:30, 9:10, 10:50; con số đọc tách: "mười bảy người", "bốn mươi
bảy phần trăm", "hai mươi xuống mười ba", "một nghìn hai trăm lẻ tám", "mười chín phần trăm".

---

## 5. Kiểm kê hình mở (Commons, 40 kết quả đầu, 07/10/2026) [30]

| Truy vấn | PD/CC0 | CC BY | BY-SA | Không raster | Nhận xét |
|---|---:|---:|---:|---:|---|
| human computers NACA Langley | **38** | 0 | 0 | 2 | Át chủ bài; loạt ảnh NACA 1943–1952 độ phân giải 8K |
| Katherine Johnson NASA | 33 | 0 | 1 | 6 | Đủ chân dung PD |
| Dorothy Vaughan | 15 | 0 | 1 | 24 | **Lẫn ảnh diễn viên cùng tên** — chỉ dùng file nguồn NASA |
| ENIAC / ENIAC women | 16 / 6 | 4 / 0 | 17 / 3 | 3 / 27 | Ảnh Lục quân Mỹ PD |
| Luddites | 11 (1 liên quan) | 0 | 18 | 10 | Một tranh khắc 1812 PD là đủ |
| Jacquard loom punched cards | 4 | 6 | 30 | 0 | Dùng CC0 `Jacquard loom cards.jpg` |
| power loom weaving 1835 | 3 | 1 | 0 | 36 | PD 1835 tốt |
| telephone operators switchboard | 29 | 5 | 5 | 0 | Nhiều ảnh NARA/LoC |
| elevator operator | 12 | 13 | 15 | 0 | Không có ảnh NYC 1945 PD → minh hoạ |
| John Maynard Keynes | 21 | 3 | 7 | 9 | PD 1929 |
| automated teller machine | 7 | 8 | 23 | 2 | PD/CC0 đủ |
| chest radiograph | 14 | 5 | 19 | 2 | CC0 của Häggström |
| Strowger switch | 14 | 6 | 15 | 3 | CC0 Daderot |
| Ada Lovelace portrait | 27 | 1 | 7 | 5 | PD |
| Lyndon Johnson 1964 | 27 | 3 | 2 | 8 | PD (minh hoạ) |
| radiologist reading X-ray | 1 | 0 | 1 | 38 | Không có → b-roll Pexels |

Thiếu ảnh mở cho: buổi đình công thang máy 1945, buổi nói của Hinton 2016, phòng đọc X-quang hiện đại, giao dịch viên ngân hàng →
dựng chữ/biểu đồ hoặc Pexels (gắn **ẢNH MINH HỌA**). NASA Images API (không khoá) là nguồn dự phòng cho ảnh "computer" Langley
(`LRC-…`), nhớ tránh logo NASA [36a].

---

## 6. Huyền thoại / lỗi thường gặp

| Hay nói sai | Đúng là | Nguồn |
|---|---|---|
| "Luddite là những kẻ ghét công nghệ" | Phản đối việc dùng máy để **ép lương**, bỏ thợ, trong bối cảnh chiến tranh; đập máy có chọn lọc | [5] |
| "Ned Ludd là thủ lĩnh phong trào" | Nhân vật huyền thoại | [5] |
| "Máy dệt làm thợ dệt mất việc" | Thế kỷ 19, tự động hoá 98% công dệt nhưng việc dệt trong nhà máy **tăng** (thợ thủ công tại gia thì chịu thiệt — nói rõ ai) | [9] |
| "ATM giết nghề giao dịch viên" | ATM không làm giảm; **ngân hàng trên điện thoại** mới làm nghề co lại (BLS −13% 2025–35) | [9][17] |
| "Oxford nói 47% việc làm sẽ mất" | "Rủi ro cao", **có thể** tự động hoá, "có lẽ một hai thập kỷ", chỉ cho **Mỹ** | [15] |
| "Tự động hoá chẳng ai bị thiệt" | Thế hệ sau ổn, nhưng **người đang làm** tổng đài dễ xuống nghề lương thấp/thôi việc | [8] |
| "AI đang gây thất nghiệp hàng loạt" | Yale (10/2025) chưa thấy xáo trộn rõ; Stanford (08/2026) không thấy mất việc diện rộng — nhưng người trẻ 22–25 ở nghề phơi nhiễm cao tụt ~19% | [12][13] |
| "Stanford chứng minh AI cướp việc người trẻ" | Tác giả nói là **mô tả, chưa chứng minh nhân quả** | [12] |
| "ILO nói 1/4 việc làm sẽ bị AI thay" | 1/4 có **phơi nhiễm**; chủ yếu **biến đổi** công việc; mức cao nhất chỉ 3,3% | [14] |
| "Hinton nói AI sẽ thay bác sĩ X-quang — và đúng" | Năm 2025 ngành tuyển kỷ lục; chính Hinton thừa nhận nói quá rộng | [20][21] |
| "'Máy tính' luôn là cái máy" | Là **chức danh của người** tới giữa thế kỷ 20 | [3] |
| "Lập trình viên đầu tiên của ENIAC là kỹ sư nam" | 6 phụ nữ vốn được thuê làm "computer" | [19] |
| Các con số sa thải "123.000", "190.000" trên báo Việt | Là số **toàn cầu ngành công nghệ** từ trang theo dõi tư nhân, gộp nhiều lý do; **không** đọc như số Việt Nam | [34] |
| "86% công nhân may Việt Nam sẽ mất việc" (ILO 2016) | "Rủi ro tự động hoá cao", không phải dự báo mất việc; ✎ năm 2017 ngành may mặc + giày da Việt Nam có ~2,98 triệu lao động chính thức (gấp ~5,8 lần năm 2000); ILO–IFC 2020: tự động hoá may mặc "remains limited" | [23][25a] |

---

## 7. Gợi ý phát âm cho TTS (`say` trong spec)

Mỗi tên đi kèm mô tả ngắn ở lần đầu (RETENTION mục 5). Phụ đề giữ chữ gốc.

| Chữ gốc | Gợi ý đọc | Chữ gốc | Gợi ý đọc |
|---|---|---|---|
| Luddite / Luddites | Lát-đai | Ned Ludd | Nét Lát |
| Nottingham | Nót-ting-hầm | Yorkshire | Doóc-sơ |
| Jacquard | Gia-ca | Lyon | Li-ông |
| Ada Lovelace | Ây-đa Lớp-lây-xơ | Charles Babbage | Sác-lơ Ba-bít |
| Lord Byron | Lo Bai-rơn | John Maynard Keynes | Giôn Mây-nợt Kên-dơ |
| Lyndon Johnson | Lin-đần Giôn-xần | Linus Pauling | Lai-nớt Pô-linh |
| Frey / Osborne | Phrây / Ốt-bơn | Oxford | Ốc-phợt |
| AT&T | Ây-ti-en-ti | Feigenbaum | Phai-gần-bom |
| Strowger | Xtrâu-giơ | Manhattan | Man-hát-tần |
| Bessen | Bét-xần | ATM | Ây-ti-em |
| NACA | Na-ca | Langley | Lăng-li |
| Hampton, Virginia | Hem-tần, Vơ-gin-ni-a | Friden | Phrai-đần |
| Dorothy Vaughan | Đô-rô-thi Von | Katherine Johnson | Ca-thơ-rin Giôn-xần |
| John Glenn | Giôn Glen | FORTRAN | Pho-tran |
| ENIAC | Ê-ni-ác | Pennsylvania | Pen-xin-vê-ni-a |
| Kay McNulty | Kây Mác-nan-ti | Jean Jennings | Gin Gien-ninh |
| Hollerith | Ho-lơ-rít | IBM | Ai-bi-em |
| Geoffrey Hinton | Giép-phri Hin-tần | Toronto | To-rôn-tô |
| Mayo Clinic | Mây-ô Cli-ních | Rochester, Minnesota | Rô-chét-xtơ, Mi-nê-xô-ta |
| FDA | Ép-đi-ây | Stanford | Xtan-phợt |
| Brynjolfsson | Brin-giôn-phơ-xần | ADP | Ây-đi-pi |
| Yale | Dêu | ILO / UNDP | I-eo-ô / U-en-đi-pi |
| Modern Times | Mo-đần Tai-mz | Charlie Chaplin | Sác-li Sáp-lin |
| The Jetsons | Đờ Giét-xần | Hidden Figures | Hít-đần Phi-gơ |

Lưu ý retro #8: bảng `say` hiện chỉ có ở engine dài; nếu cắt Short từ video này, cần bảng tương ứng cho engine Short (ELIZA từng bị
đánh vần). Thử giọng với "ENIAC", "FORTRAN", "AT&T" trước khi thu cả bài.

---

## 8. Đóng gói

**Tựa (3 phương án cho Test & Compare):**
1. *AI Sẽ Cướp Việc Của Bạn? 200 Năm Trước Người Ta Cũng Sợ Y Như Vậy*
2. *"Máy Tính" Từng Là Một Nghề. Nghề Đó Đã Biến Mất — Còn Người Thì Sao?*
3. *Lần Nào Máy Mới Ra Đời Cũng Có Người Nói "Lần Này Khác". Lần Này Có Khác?*

(Từ khoá người Việt tự gõ — "AI", "cướp việc", "mất việc" — ở nửa đầu tựa; tránh "Luddite", "tự động hoá" trong tựa.)

**Thumbnail:** nền xanh than theme MIM. Nửa trái: ảnh PD NACA 1952 (`Langley Women Computer with X-4 with Friden machine…`), đen trắng,
tương phản cao, cắt vào một người phụ nữ bên máy Friden; một nhãn kiểu thẻ tên đỏ ghi **"MÁY TÍNH"** chỉ vào người. Nửa phải: ô chat cyan
phát sáng + con trỏ nhấp nháy. Chữ lớn vàng/trắng **"NGHỀ NÀY ĐÃ BIẾN MẤT"** (phương án 2) hoặc **"AI CƯỚP VIỆC?"** (phương án 1). Không
logo, không mặt người còn sống. Cold open mở đúng bằng ảnh này.

**Chương YouTube (có từ khoá):** 00:00 "Máy tính" từng là một nghề · Luddite: những người đập máy · Ba lời tiên tri máy cướp việc · Tổng đài
viên và người lái thang máy · Nghịch lý máy ATM · Hidden Figures và ENIAC · Hinton và bác sĩ X-quang · AI có cướp việc người trẻ? · Năm 2030
của Keynes.

**3 Short mồi (cắt từ chính video, đăng trước 7–10 ngày):**
1. **"'Máy tính' từng là tên một nghề"** — hook 1 giây: ảnh NACA + chữ "ĐÂY LÀ MỘT CÁI MÁY TÍNH". Kết: nghề biến mất, Dorothy Vaughan tự
   học FORTRAN. (Ảnh PD, rủi ro thấp.)
2. **"Năm 2016, cha đẻ học sâu bảo: ngừng đào tạo bác sĩ X-quang. 10 năm sau…"** — kết bằng con số 1.208 suất nội trú kỷ lục. (Kiểm nguyên
   văn Hinton trước khi đăng.)
3. **"Máy ATM ra đời — số giao dịch viên ngân hàng lại tăng"** — đảo ngược trực giác; câu cuối mở vòng: "nhưng một thứ trong túi bạn thì
   làm được điều ATM không làm được" → trỏ video dài.

---

## 9. Việc phải làm trước khi khoá kịch bản

1. Mở bản gốc hoặc nguồn chính thức cho các mục [SECONDARY] sẽ đọc thành số: ILO 2025 (WP140) [14], ILO 2016 (86%) [23], NYT/Works in
   Progress (1.208 suất, 36%, Mayo +55%) [20][21], FDA list [22], ENIAC (Penn/Army) [18]. Các trang ILO, NYT, WIP, APS, Hansard chặn script
   hôm nay → cần người mở bằng trình duyệt.
2. Nghe lại video Creative Destruction Lab 2016 để chép đúng câu của Hinton.
3. Tra BLS cho chuỗi việc làm Mỹ 2013–2025 và đỉnh số giao dịch viên; đối chiếu ≥ 3 mốc (quy tắc retro #2).
4. Không đọc bất kỳ mục [CHƯA KIỂM] nào chưa xử lý (Byron, tháng đình công thang máy, năm sinh Vaughan, Jetsons, Nhà máy Dệt Nam Định).
5. Theme gallery (retro #1): video này cần cảnh *biểu đồ đường hai nhóm* (ch7) và *thẻ đục lỗ động* (motif) — dựng demo trước.

✎ **Trạng thái 06/10/2026:** mục 1 phần lớn đã xử lý (ILO 2025, WIP, ENIAC/Penn → bằng chứng; ILO 2016 → bằng chứng một phần; NYT
vẫn paywall; FDA dùng số WIP); mục 2 **chưa** (không mở YouTube) → câu 2 của Hinton đọc dạng diễn ý; mục 3 xong cho chuỗi việc làm
Mỹ + giao dịch viên 2014/2018–2025, đỉnh ~600.000 vẫn chưa → bỏ; mục 4 đã tuân thủ trong `data/long/mim-ai-jobs/script.md`.

---

## 10. Nguồn

1. Wikimedia Pageviews REST API (vi.wikipedia, `user`, daily, 20260709–20261006; theo thiết bị 20260909–20261006): `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/vi.wikipedia/{all-access|desktop|mobile-web|mobile-app}/user/{bài}/daily/{từ}/{đến}`
2. Google Trends "Trending now" RSS (VN, 07/10/2026): https://trends.google.com/trending/rss?geo=VN
3. NASA, *She Was a Computer When Computers Wore Skirts* (26/08/2008): https://www.nasa.gov/centers-and-facilities/langley/she-was-a-computer-when-computers-wore-skirts/ · 3a. S. McLennan, M. Gainer, *When the Computer Wore a Skirt: Langley's Computers, 1935–1970*, NASA History News & Notes 29(1), 2012 (bản PDF chép lại): https://rybn.org/human_computers/articles/When_the_Computer_Wore_a_Skirt_-_Langley_s_Computers.pdf ; tóm tắt: https://www.hampton.gov/3700/NASAs-Human-Computers
4. (như [3]) Katherine Johnson. · 4a. NASA, *Dorothy Vaughan* (tiểu sử): https://www.nasa.gov/people/dorothy-vaughan/
5. The National Archives (UK), *Why did the Luddites protest?*: https://www.nationalarchives.gov.uk/education/teaching-resources/why-did-the-luddites-protest/ · 5a. Nottinghamshire Heritage Gateway, *Luddites*: http://www.nottsheritagegateway.org.uk/people/luddites.htm · 5b. Hansard, HL Deb 27/02/1812 *Frame Work Bill*: https://api.parliament.uk/historic-hansard/lords/1812/feb/27/frame-work-bill (không truy cập được); con trỏ: https://en.wikipedia.org/wiki/Destruction_of_Stocking_Frames,_etc._Act_1812
6. Science and Industry Museum (Manchester), *Programming patterns: the story of the Jacquard loom*: https://www.scienceandindustrymuseum.org.uk/objects-and-stories/jacquard-loom
7. J. M. Keynes, *Economic Possibilities for our Grandchildren* (1930), bản chép: https://www.marxists.org/reference/subject/economics/keynes/1930/our-grandchildren.htm
8. J. Feigenbaum, D. P. Gross, *Answering the Call of Automation: How the Labor Market Adjusted to Mechanizing Telephone Operation*, QJE 139(3):1879–1939 (2024); NBER w28061 (11/2020, sửa 02/2024): https://www.nber.org/papers/w28061 ; https://jamesfeigenbaum.github.io/research/tele/
9. J. Bessen, *Toil and Technology*, IMF Finance & Development, 03/2015: https://www.imf.org/external/pubs/ft/fandd/2015/03/bessen.htm
10. Ad Hoc Committee, *The Triple Revolution* (22/03/1964): https://monoskop.org/images/7/7d/Ad_Hoc_Committee_1964_The_Triple_Revolution.pdf ; con trỏ: https://en.wikipedia.org/wiki/The_Triple_Revolution
11. National Commission on Technology, Automation, and Economic Progress, *Technology and the American Economy* (02/1966) — dẫn qua T. Taylor, Conversable Economist (01/12/2014): https://conversableeconomist.com/2014/12/01/automation-and-job-loss-the-fears-of-1964/
12. Stanford Digital Economy Lab, *No Widespread Displacement, but the AI Employment Gap for Young Workers Has Widened to 19%* (12/08/2026), về bài E. Brynjolfsson, B. Chandar, R. Chen, *Canaries in the Coal Mine?* (bản sửa 2026): https://digitaleconomy.stanford.edu/news/canariesaug26/ ; bài gốc: https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/
13. M. Gimbel, M. Kinder, J. Kendall, M. Lee, *Evaluating the Impact of AI on the Labor Market: Current State of Affairs*, Yale Budget Lab (01/10/2025): https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs
14. ILO Working Paper 140, *Generative AI and Jobs: A Refined Global Index of Occupational Exposure* (05/2025): https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure ; UN News (05/2025): https://news.un.org/en/story/2025/05/1163486
15. C. B. Frey, M. A. Osborne, *The Future of Employment: How Susceptible Are Jobs to Computerisation?* (Oxford Martin, 2013): https://www.oxfordmartin.ox.ac.uk/downloads/academic/The_Future_of_Employment.pdf · 15a. Oxford Martin School, *Half of jobs to be lost to computerisation?* (19/09/2013): https://www.oxfordmartin.ox.ac.uk/news/201309futureofemployment
16. NPR (Planet Money, S. Henn), *Remembering When Driverless Elevators Drew Skepticism* (31/07/2015): https://www.npr.org/2015/07/31/427990392/remembering-when-driverless-elevators-drew-skepticism ; con trỏ: https://en.wikipedia.org/wiki/Elevator_Strikes
17. U.S. BLS, Occupational Outlook Handbook, *Tellers*: https://www.bls.gov/ooh/office-and-administrative-support/tellers.htm
18. Penn Engineering, *ENIAC*: https://www.engineering.upenn.edu/about/history-heritage/eniac/ ; U.S. Army, *Women's History Month: ENIAC, first computer programmers*: https://www.army.mil/article/98817/ ; APS News (11/2022): https://www.aps.org/apsnews/2022/11/eniac-first-top-secret-program ; Encyclopedia of Greater Philadelphia: https://philadelphiaencyclopedia.org/essays/eniac/ (đọc qua tóm tắt tìm kiếm — SECONDARY)
19. IEEE Computer Society, *About Women of ENIAC*: https://www.computer.org/volunteering/awards/pioneer/about-women-of-eniac
20. S. Lohr, *Your A.I. Radiologist Will Not Be With You Soon*, The New York Times (14/05/2025) — paywall; con trỏ: https://radiologybusiness.com/topics/artificial-intelligence/ny-times-revisits-nobel-prize-winners-prediction-ai-will-render-radiologists-obsolete ; https://the-decoder.com/geoffrey-hintons-wildly-overconfident-ai-prediction-failed-now-its-a-lesson-in-humility/
21. D. Mousa, *The algorithm will see you now*, Works in Progress (09/2025): https://worksinprogress.co/issue/the-algorithm-will-see-you-now/ (không truy cập được bằng script; bản đăng lại: https://www.understandingai.org/p/ai-isnt-replacing-radiologists)
22. FDA, *Artificial Intelligence-Enabled Medical Devices* (danh sách): https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices ; tổng hợp: https://www.auntminnie.com/imaging-informatics/artificial-intelligence/article/15830219/radiology-dominates-thirty-years-of-fda-ai-device-approvals
23. ILO, *ASEAN in Transformation: The Future of Jobs at Risk of Automation* (2016): https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@ed_dialogue/@act_emp/documents/publication/wcms_579554.pdf (403 với script); bản ILO Hà Nội: https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@asia/@ro-bangkok/@ilo-hanoi/documents/publication/wcms_537822.pdf
24. Xuất khẩu dệt may 2025 ~46 tỉ USD, >3 triệu lao động: https://doanhnghiephoinhap.vn/xuat-khau-det-may-viet-nam-nam-2025-uoc-dat-46-ty-usd-121990.html ; https://m.nhipcaudautu.vn/kinh-doanh/det-may-viet-nam-dat-muc-tieu-can-moc-50-ti-usd-trong-nam-2026-3364295/
25. F. Bárcia de Mattos et al., *Disruption in the apparel industry? Automation, employment and reshoring*, International Labour Review 160(4), 2021, doi:10.1111/ilr.12213: https://onlinelibrary.wiley.com/doi/10.1111/ilr.12213
26. Wikipedia (chỉ làm con trỏ mốc phát hành): https://en.wikipedia.org/wiki/Modern_Times_(film) · https://en.wikipedia.org/wiki/The_Jetsons · https://en.wikipedia.org/wiki/Hidden_Figures
30. Wikimedia Commons API (`generator=search`, `prop=imageinfo&iiprop=extmetadata|size|mime`), 07/10/2026: https://commons.wikimedia.org/w/api.php
33. VietNamNet, *61% người Việt lo mất việc hoặc không tìm được việc làm do AI* (UNDP, 02/12/2025): https://vietnamnet.vn/61-nguoi-viet-lo-mat-viec-hoac-khong-tim-duoc-viec-lam-do-ai-2468590.html
34. Báo Việt về sa thải ngành công nghệ 2026: https://cafebiz.vn/dau-nam-2026-80000-nhan-vien-cong-nghe-mat-viec-mot-nua-la-vi-ai-176260413070253223.chn ; https://kenh14.vn/ai-dang-viet-lai-luat-choi-viec-lam-hon-123000-nhan-su-cong-nghe-mat-viec-chi-trong-nua-nam-215260625190837729.chn ; https://1thegioi.vn/gan-190-000-lao-dong-nganh-cong-nghe-bi-mat-viec-lan-song-sa-thai-do-ai-se-tiep-dien-258806.html
35. Fortune, *McKinsey: AI will create more jobs than it kills — after destroying 11 million* (03/10/2026): https://fortune.com/2026/10/03/ai-job-displacement-creation-new-careers-11-million-americans-workforce-mobility
36. Cảnh báo deepfake: https://doanhnhan.baophapluat.vn/cong-an-ha-noi-canh-bao-nguoi-dan-canh-giac-truoc-25-kich-ban-lua-dao-tren-khong-gian-mang-nam-2026-7cc6172e.html ; https://cafef.vn/tat-ca-nguoi-dan-da-dung-ung-dung-tao-anh-ai-chu-y-thong-bao-moi-tu-cong-an-188261006152248217.chn · 36a. Nội bộ: `docs/channels/mind-in-the-machine/2026-10-06-media-sources.md` (giấy phép, NASA), `motion/long/RETENTION.md`, `docs/pm/2026-10-06-retro-1.md`
37. Ví dụ bài "thuật toán TikTok 2026" trên báo/blog Việt: https://accesstrade.vn/cap-nhat-thuat-toan-tiktok-moi-nhat/ ; https://www.vira.vn/thuat-toan-tiktok-2026-huong-dan-len-xu-huong/
25a. ✎ F. Bárcia de Mattos, J. Eisenbraun, D. Kucera, A. Rossi, *Automation, employment and reshoring in the apparel industry: Long-term disruption or a storm in a teacup?*, ILO–IFC Better Work Discussion Paper 36 (05/2020): https://betterwork.org/wp-content/uploads/BW-Discussion-Paper-36-Automation_FINAL-1.pdf (đọc toàn văn bằng curl; mục 1, mục 5, bảng 1)
38. ✎ F. Levy, R. J. Murnane, *The New Division of Labor* (Princeton University Press, 2004), chương 1 (PDF chương mẫu): https://assets.press.princeton.edu/chapters/s7704.pdf
39. ✎ BLS, *Occupational employment projections to 2024*, Monthly Labor Review (12/2015), bảng 5 (Tellers 2014: 520,5 nghìn): https://www.bls.gov/opub/mlr/2015/article/occupational-employment-projections-to-2024.htm
40. ✎ BLS OES/OEWS, *43-3071 Tellers*, bảng từng năm: https://www.bls.gov/oes/2018/may/oes433071.htm · https://www.bls.gov/oes/2019/may/oes433071.htm · https://www.bls.gov/oes/2020/may/oes433071.htm · https://www.bls.gov/oes/2021/may/oes433071.htm · https://www.bls.gov/oes/2023/may/oes433071.htm
41. ✎ FRED, *All Employees, Total Nonfarm (PAYEMS)*, cập nhật 02/10/2026: https://fred.stlouisfed.org/data/PAYEMS.txt
42. ✎ NPR, bản text của [16]: https://text.npr.org/427990392 · Conversable Economist (bản blogspot của [11]): https://conversableeconomist.blogspot.com/2014/12/automation-and-job-loss-fears-of-1964.html · The Decoder (thuật lại NYT về Mayo): xem [20]

---

## 11. Kiểm chứng trước khoá kịch bản (06/10/2026) ✎

| Mục | Trước | Sau | Thay đổi trong lời đọc |
|---|---|---|---|
| ILO 2025 (1/4, 3,3%, nữ 4,7% / nam 2,4%, văn phòng, "biến đổi") [14] | SECONDARY | **bằng chứng** (PDF WP140) | Đọc đủ; thêm "nhân viên văn phòng phơi nhiễm cao nhất" |
| ILO 2016 "86% dệt may VN" [23] | SECONDARY | **bằng chứng một phần** (DP36 ILO–IFC 2020: 64–88% cho Campuchia, Indonesia, VN; "rủi ro, không phải chắc chắn") | Đọc **khoảng 64–88% cho ba nước**, không đọc "86%" |
| "Hơn 3 triệu lao động dệt may 2025" [24] | SECONDARY | Thay bằng **~2,98 triệu lao động chính thức may mặc + giày da năm 2017** (DP36, UNIDO), gấp 5,8 lần năm 2000 | Đọc "gần ba triệu, năm 2017" |
| Tự động hoá may mặc "còn hạn chế" [25] | SECONDARY | **bằng chứng** (DP36 = bản gốc của ILR 2021) | Giữ |
| Hinton 2016, câu 1 "stop training radiologists now" [20][21] | SECONDARY | **bằng chứng** qua WIP (+ NYT, EMJ khớp) | Trích câu 1 [TRÍCH DỊCH]; câu "năm năm" đọc diễn ý; chưa nghe video |
| 1.208 suất nội trú, +4%; 520.000 USD, hạng 2, +48%; 36% thời gian (2012, 3 bệnh viện) [21] | SECONDARY | **bằng chứng** (WIP mở được; 1.208 = 1.057 + 151 NRMP) | Đọc đủ |
| FDA "hơn 1.000, ~76%" [22] | SECONDARY | **Đổi** sang WIP: >700 mô hình X-quang, > ¾ thiết bị AI y tế | Đọc số WIP |
| Mayo +55% [20] | SECONDARY | SECONDARY (2 nguồn khớp: ~260 → >400) | Đọc kèm "theo New York Times" |
| Hinton 2025 "nói quá rộng" [20] | SECONDARY | SECONDARY (≥ 3 nguồn khớp) | Đọc kèm "nói với New York Times" |
| BLS giao dịch viên [17] | 339.200, −13% bằng chứng; đỉnh ~600.000 CHƯA KIỂM | 339.200 / −13% / lý do: **bằng chứng**; thêm EP 2014: 520,5 nghìn; OES 2018–2023 (5 mốc) | Đọc 2014 → 2025 (−35%); bỏ "600.000" |
| ENIAC [18] | SECONDARY (15/02/1946; 20 giây; ~100 người; 1.620 USD) | Penn **bằng chứng**: công bố 14/02/1946; 12 giờ → 30 giây; 6 tên | Đọc "tháng 2 năm 1946", "12 giờ → 30 giây"; bỏ 20 giây, số người, lương |
| Dorothy Vaughan năm sinh | CHƯA KIỂM | **bằng chứng** (NASA: 20/09/1910 → 48 tuổi năm 1958) | Đọc "gần năm mươi tuổi" |
| Stanford "19%" [12] | bằng chứng | **bằng chứng, chính xác hoá**: 22–25 tuổi, nghề phơi nhiễm cao, thấp hơn ~19% so với mức *nếu theo kịp* bạn cùng tuổi ở nghề ít phơi nhiễm; 15% (dữ liệu 07/2025) → 19% (06/2026); mốc 11/2022; "tăng" là ở người **nhiều kinh nghiệm** nghề kiến thức ngầm | Đọc đúng định nghĩa; nói rõ "mô tả, chưa phải nhân quả" |
| Feigenbaum & Gross QJE 2024 [8] | bằng chứng | **bằng chứng** (đối chiếu nguyên văn tóm tắt NBER) | Giữ; nói rõ đối tượng là phụ nữ trẻ |
| Triple Revolution 1964 [10] | SECONDARY | **bằng chứng** (Levy & Murnane 2004, ch.1): 14 trang, Pauling, Myrdal | Đọc |
| Uỷ ban 1966 "jobs, not work" [11] | SECONDARY | SECONDARY (blog trích nguyên văn) | Đọc dạng [DIỄN Ý], bỏ 3,8% |
| Thang máy 1945 [16] | SECONDARY | **bằng chứng** (bản text NPR): 1,5 triệu người, 100 triệu USD, 1900, >50 năm | Đọc; bỏ "15.000 người đình công" |
| Việc làm Mỹ 2013 → 2026 | CHƯA KIỂM | **bằng chứng** (FRED, 6 mốc) | Đọc "khoảng 137 triệu → khoảng 159 triệu" |
| UNDP 61% [33] | SECONDARY | SECONDARY (không thấy trong nguồn UNDP mở được) | **Không đọc** |
| Byron 1812; tháng đình công thang máy; số giờ Jetsons | CHƯA KIỂM | CHƯA KIỂM | **Không đọc** |
