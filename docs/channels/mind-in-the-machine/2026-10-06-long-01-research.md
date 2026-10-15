# Nghiên cứu video dài #1 — Mind in the Machine (MIM) — 06/10/2026

**Phạm vi:** chọn đề tài và lập hồ sơ dữ kiện cho video dài đầu tiên của MIM (16:9, 12–20 phút, tiếng Việt, faceless,
giọng TTS + motion graphics + ảnh mở). Áp dụng bài học cấu trúc từ `motion/long/RETENTION.md` và
`motion/long/RESEARCH-million-views.md` (cold open, cung A → B, hứa lộ trình ở phút 1, danh sách tối đa 3 mục, mỗi chương mở
một vòng và đóng ở chương sau, cảnh cụ thể, motif, chương văn hoá đại chúng gần cuối, kết mở). Không nhắc lại nội dung của
`2026-10-05-analysis.md`, `2026-10-06-topic-research.md`, `2026-10-06-media-sources.md`.

**Phương pháp:**
- Đối chiếu nguồn **gốc**: bài báo khoa học gốc (Turing 1950, Shannon 1951, Weizenbaum 1966, AlexNet 2012, Transformer 2017…),
  văn bản đề xuất Dartmouth 1955, báo cáo Lighthill, trang của chính tổ chức (Dartmouth, Cornell, IBM, DeepMind, Nobel, OpenAI).
  Wikipedia chỉ dùng làm con trỏ hoặc cho ngày tháng không tranh cãi, có ghi rõ.
- Wikimedia Pageviews REST API (vi.wikipedia, `user`, theo ngày, **08/07 → 05/10/2026 = 90 ngày**), Commons API
  (`prop=imageinfo&iiprop=extmetadata`, đọc `LicenseShortName`), NASA Images API, Crossref API (siêu dữ liệu bài báo). Mọi truy
  vấn dùng User-Agent `yt-factory-research/1.0 (https://github.com/nguyent0810/Youtube_Creator_V2)`, giãn ~1 giây.
- Không cào YouTube/Google, không dùng khoá API, không tải file media, không đăng ký tài khoản. Trích dẫn nguyên văn chỉ là
  cụm ngắn; còn lại tóm tắt bằng lời của mình.
- Chỗ nào chưa chắc ghi **(chưa chắc)**. Số trong ngoặc vuông `[n]` trỏ tới mục 9 (Nguồn).

---

## 1. Tóm tắt

- **Chọn: "AI đã chết hai lần: 70 năm từ một mùa hè 1956 đến ChatGPT"** (trục A, có cầu nối B).
- **Vì sao:**
  1. *Nhu cầu cao nhất trong 3 ứng viên:* "Trí tuệ nhân tạo" trung vị 358,5 lượt/ngày trong 90 ngày (tháng 10: 1.170/ngày),
     "ChatGPT" 376,5/ngày; bài "Lịch sử ngành trí tuệ nhân tạo" tăng gấp ~7 lần từ tháng 7 sang tháng 9 (11 → 78/ngày), trùng
     năm học đầu tiên dạy AI đại trà [1][32].
  2. *Đúng dịp:* Dartmouth tổ chức hội nghị "AI at 70" ngày **29–31/10/2026** [4]; bài báo lan truyền ngược (backprop) tròn
     **40 năm** (Nature, 10/1986) [16]; ChatGPT tròn **4 năm** ngày 30/11/2026; Nobel 2026 công bố tuần này (Vật lý 6/10,
     Hoá 7/10) [29].
  3. *Cung A → B mạnh, có cảnh mở sẵn:* 10 nhà khoa học xin **13.500 USD** để giải bài toán trí tuệ trong **một mùa hè** [2] →
     70 năm, hai "mùa đông", và một cỗ máy làm đúng trò chơi "đoán chữ tiếp theo" mà một trong bốn người ký đề xuất đã thử năm
     1951 [7].
  4. *Ảnh mở đủ dùng:* ~35 file PD/CC0/CC BY đã kiểm giấy phép bằng Commons API (mục 5), có cả **ảnh Hải quân Mỹ chụp
     Mark I Perceptron (PD)** cho cold open; thiếu ảnh mở của buổi họp 1956, Kasparov, giao diện ChatGPT → dựng bằng motion
     graphics.
  5. *Rủi ro thấp–vừa:* lịch sử đã ổn định; chỉ chương cuối có số liệu đổi nhanh → ghi kèm mốc thời gian.
- **Motif:** *các mùa* (mùa hè 1956 → mùa đông AI → "mùa hè" hiện tại?) và *đoán chữ tiếp theo* (Shannon 1951 → ChatGPT).
- **Thời điểm đăng đề xuất:** 22–27/10/2026 (trước hội nghị Dartmouth 29/10), sau khi Shorts đã chạy ~2 tuần. Cắt 3 Short
  "mồi" từ cold open, ELIZA và trò đoán chữ của Shannon.

---

## 2. Chấm điểm 3 ứng viên

### 2.1. Nhu cầu (vi.wikipedia, người dùng thật, trung vị lượt xem/ngày, 08/07 → 05/10/2026) [1]

| Ứng viên | Bài liên quan (trung vị/ngày) | Ghi chú |
|---|---|---|
| **A. 70 năm AI** | Trí tuệ nhân tạo **358,5** · ChatGPT **376,5** · Lịch sử ngành trí tuệ nhân tạo **31** · Alan Turing 29,5 · Học máy 18 · Phép thử Turing 9 | Trung vị theo tháng của "Trí tuệ nhân tạo": 7: 238,5 → 8: 331 → 9: 826 → 10: 1.170. "Lịch sử ngành TTNT": 11 → 26 → 78 → 71. Khả năng cao do năm học (12 tiết AI/năm từ 2026–2027 [32]) **(chưa chắc về nhân quả)** |
| B. GPU / chip → AI | Jensen Huang **91** · NVIDIA 35 · Transistor 17 · Vi mạch 10 · Định luật Moore 8 · Bộ xử lý đồ họa 5 · CUDA 2 | Người xem biết *người* (Jensen) hơn *khái niệm* (GPU), khớp nhận xét trong `topic-research` |
| C. Internet: từ "LO" đến điện thoại | World Wide Web **93,5** · Internet 69 · Wi-Fi 22 · Tim Berners-Lee 9 · Lịch sử Internet 7 · ARPANET 4 | Ổn định, không tăng theo mùa học |

Bài không có trên vi.wikipedia (404): *John McCarthy* (bài đúng là "John McCarthy (nhà khoa học máy tính)", 4/ngày), *AlphaGo*
(bài "AlphaGo đấu với Lee Sedol", 3/ngày). Văn hoá đại chúng hữu ích cho chương 7: "Doraemon" **143**/ngày, "Doraemon (nhân
vật)" 123,5, "Kẻ hủy diệt 2: Ngày phán xét" 16, "2001: A Space Odyssey (phim)" 9 [1].

**Báo chí Việt:** chủ đề "lịch sử AI / Dartmouth 1956" có bài giải thích sẵn trên Tia Sáng, VinUni và các blog [33], và nằm
trong khung chương trình học AI phổ thông 2026–2027 (báo chí đưa tin 20–21/08/2026) [32]. Chưa thấy báo Việt nào làm bài về mốc
70 năm hay hội nghị Dartmouth 10/2026 → **khoảng trống nội dung tiếng Việt** **(chưa chắc: chỉ dò bằng tìm kiếm web 06/10)**.

### 2.2. Bảng điểm (1–5, cao = tốt; rủi ro: 5 = rủi ro thấp)

| Tiêu chí | A. 70 năm AI | B. GPU → AI | C. Internet |
|---|---|---|---|
| (a) Nhu cầu VN | **5** — hai bài lớn nhất ngách AI, đang tăng | 3 — chỉ Jensen Huang kéo | 3 — ổn định, không tăng |
| (b) Cung A → B + cảnh mở | **5** — "một mùa hè" → 70 năm; cold open Perceptron 1958 có ảnh PD; vòng Shannon 1951 → ChatGPT | 4 — chip chơi game → trái tim AI; cảnh AlexNet 2 card GTX 580 trong phòng ngủ **(chưa chắc chi tiết "phòng ngủ")** | 4 — "LO" sập máy 1969 → điện thoại; cảnh mạnh nhưng là trục B |
| (c) Thời điểm (10–12/2026) | **5** — Dartmouth "AI at 70" 29–31/10 [4]; backprop 40 năm (10/1986) [16]; ChatGPT 4 năm (30/11); Nobel tuần này [29] | 3 — CUDA ra mắt 2006 (20 năm) [19], tháng cụ thể **(chưa chắc)** | 3 — 29/10/1969 [35] (57 năm, không tròn) |
| (d) Hình mở 16:9 | 4 — ~35 file PD/CC0/BY đã kiểm (mục 5); NASA có ảnh IBM 704 (1957–58) và video siêu máy tính; Pexels hợp cho b-roll (bàn cờ, điện thoại, phòng máy chủ). Thiếu: ảnh họp 1956, Kasparov (chỉ BY-SA), giao diện ChatGPT | 4 — ảnh die chip CC0 của Fritzchens Fritz rất nhiều, GeForce 8800 PD 16/40 kết quả, Jensen Huang CC0; ít ảnh con người/lịch sử | **5** — ARPANET PD 18/40, IMP PD 8/40 (theo `media-sources`) |
| (e) Rủi ro | 4 — lịch sử ổn định; chương cuối có số đổi nhanh; nhân vật còn sống (Hinton, LeCun) chỉ dùng thông tin công khai | 2 — giá cổ phiếu/vốn hoá, kiểm soát xuất khẩu chip Mỹ–Trung (nhạy cảm), số liệu đổi theo quý | 5 — thấp |
| Hợp trụ cột | A (chính) + cầu nối B | A/B | B |
| **Tổng** | **23** | 16 | 20 (nhưng lệch trụ cột A) |

**Kết luận:** chọn **A**, nhưng *đóng gói* bằng từ người Việt tự gõ ("ChatGPT", "AI") thay vì "Dartmouth". B nên để làm video dài
#2 (đã có sẵn chương AlexNet làm cầu nối). C làm Short dịp 29/10.

---

## 3. Xương sống câu chuyện

- **Câu hỏi trung tâm:** *Nếu năm 1956 người ta đã nghĩ một mùa hè là đủ, thì vì sao phải mất 70 năm — và thứ cuối cùng
  "chạy được" thật ra đang làm gì?*
- **Cung A → B:** A = 1955–56: trí tuệ là thứ *viết thành luật* được, 10 người, 2 tháng, 13.500 USD [2]. B = 2025: máy *tự học
  từ dữ liệu* bằng cách đoán phần tiếp theo, 700 triệu người dùng mỗi tuần [24]. Ở giữa: lời hứa quá đà → hai mùa đông →
  ý tưởng "thua cuộc" (mạng nơ-ron) quay lại nhờ con chip chơi game.
- **Lời hứa lộ trình (phút 1), 3 câu hỏi:** (1) Ai đặt tên "trí tuệ nhân tạo", và họ nghĩ mất bao lâu? (2) Vì sao AI "chết"
  hai lần? (3) Thứ gì hồi sinh nó, và ChatGPT thật ra đang làm gì khi trả lời bạn?
- **Motif:** dải "mùa" trên HUD (Hè 1956 → Đông 1973 → Đông cuối 1980s → Hè 2012 → ?), quay lại ở cold open, giữa video, kết.
  Motif phụ: dòng chữ đoán từng ký tự (Shannon) xuất hiện ở chương 1, quay lại ở chương 6.
- **Thời lượng gợi ý:** ~15 phút ≈ 3.300 âm tiết ở 220 âm tiết/phút (RETENTION.md mục 5).

---

## 4. Dàn ý chương + dữ kiện đã kiểm

Ký hiệu vòng: **[Mở Vn]** mở vòng, **[Đóng Vn]** đóng vòng. Giấy phép ảnh ghi đúng như `LicenseShortName` trên Commons
(kiểm 06/10/2026). Tên file dùng nguyên văn để tra: `https://commons.wikimedia.org/wiki/File:<tên file>`.

### 0. Cold open — "Cỗ máy học được trái và phải" (0:00–1:10)

- **Vòng:** [Mở V0] *"Người ta gọi nó là đối thủ đầu tiên của bộ não. 13 năm sau, ý tưởng ấy bị coi là ngõ cụt."* →
  đóng ở chương 5. Rồi hứa lộ trình 3 câu hỏi.
- **Dữ kiện:**
  1. Tháng 7/1958, Văn phòng Nghiên cứu Hải quân Mỹ (ONR) trình diễn: một máy **IBM 704** — nặng **5 tấn**, to bằng một căn
     phòng — được cho ăn thẻ đục lỗ; sau **50 lần thử** nó tự phân biệt thẻ đánh dấu bên trái với bên phải [8].
  2. Người tạo ra nó, **Frank Rosenblatt** (Phòng thí nghiệm Hàng không Cornell), gọi perceptron là cỗ máy đầu tiên "capable of
     having an original idea" [8].
  3. Báo chí: New York Times giật tít "New Navy Device Learns by Doing"; tạp chí New Yorker viết đây là "the first serious
     rival to the human brain ever devised" (cả hai trích qua Cornell Chronicle) [8]. Câu NYT nổi tiếng "walk, talk, see,
     write, reproduce itself and be conscious of its existence" là **kỳ vọng của Hải quân do NYT thuật lại** — **(chưa chắc:
     chưa đọc được bản gốc NYT 08/07/1958)**; nếu dùng phải ghi "theo NYT thuật lời Hải quân".
  4. Bản phần cứng **Mark I Perceptron** dùng mắt tế bào quang điện; ảnh Hải quân mô tả máy được "dạy" bằng cách đặt chữ cái
     trước "mắt" và sửa khi nó nhận sai [9]. Máy hiện ở Bảo tàng Lịch sử Mỹ (Smithsonian) [8][11].
  5. Bài báo lý thuyết: Rosenblatt, *Psychological Review* 65 (1958), tr. 386–408 [10].
- **Cảnh kể được:** phòng máy lạnh ở Washington, chồng thẻ đục lỗ, một bên đục trái, một bên đục phải. Lần 1 máy đoán bừa.
  Lần 10 vẫn sai. Lần 50 — nó không sai nữa. Phóng viên ghi chép. (Chi tiết "phòng lạnh", vị trí Washington: **(chưa chắc)**,
  chỉ kể "một phòng máy" nếu không kiểm thêm.)
- **Hình:**
  - `330-PSA-80-60 (USN 710739) (20897323365).jpg` — **Public domain** (National Museum of the U.S. Navy), Mark I Perceptron, 2836×2220.
  - `Ibm punch card.png` — **CC0** (MdeVicente), 3412×1520.
  - `IBM Electronic Data Processing Machine - GPN-2000-001881.jpg` — **Public domain** (NASA, IBM 704 ở Langley, 1957), 3000×2377.
  - NASA `ARC-1969-A-24321` (IBM 704 ở Ames, chụp 03/10/1958; trên Commons là `ARC-1958-A-24321.jpg`, **Public domain**).
    Lưu ý: đây là máy IBM 704 *khác*, chỉ dùng làm "máy cùng loại" → gắn nhãn **ẢNH MINH HỌA**.

### 1. "Một mùa hè để giải bài toán trí tuệ" (1950–1956)

- **Vòng:** [Mở V1] *"Họ xin đúng một mùa hè. Hãy nhớ con số này."* → đóng ở chương 8 (70 năm).
  [Mở V2] *"Một trong bốn người ký tên từng chơi một trò chơi đoán chữ với một người tình nguyện. 70 năm sau, trò chơi đó có
  tên là ChatGPT."* → đóng ở chương 6.
- **Dữ kiện:**
  1. Tháng 10/1950, Alan Turing mở bài *Computing Machinery and Intelligence* (Mind, tập LIX, số 236, tr. 433–460) bằng câu hỏi
     "Can machines think?" — rồi chính ông viết câu hỏi gốc ấy "too meaningless to deserve discussion" và thay bằng "trò chơi
     bắt chước" [6].
  2. Turing dự đoán: khoảng 50 năm nữa (tức ~2000), máy có bộ nhớ ~10^9 sẽ chơi trò bắt chước giỏi đến mức người hỏi trung bình
     không quá 70% cơ hội đoán đúng sau 5 phút [6]. → [Mở V3] đóng ở chương 6.
  3. Ngày **31/08/1955**, bốn người ký đề xuất *Dartmouth Summer Research Project on Artificial Intelligence*: J. McCarthy
     (Dartmouth), M. L. Minsky (Harvard), N. Rochester (IBM), C. E. Shannon (Bell Labs). Họ đề nghị "a 2 month, 10 man study"
     vào mùa hè 1956, xin **13.500 USD** [2]. **Cụm từ "artificial intelligence" đã nằm trong đề xuất 1955**, trước hội thảo.
  4. Giả định nền: mọi khía cạnh của học tập hay trí tuệ "can in principle be so precisely described that a machine can be made
     to simulate it"; và họ tin có thể tiến một bước lớn nếu một nhóm chọn lọc làm cùng nhau "for a summer" [2][3].
     Bảy chủ đề đề xuất gồm: máy tính tự động, lập trình máy dùng ngôn ngữ, **mạng nơ-ron**, tự cải thiện, trừu tượng hoá,
     ngẫu nhiên và sáng tạo… [2] (lời đọc chỉ nêu 3: ngôn ngữ, nơ-ron, sáng tạo).
  5. Quỹ Rockefeller tài trợ một phần buổi gặp 1956 [4]. Ngày cụ thể (khoảng giữa 6 → giữa 8/1956) và danh sách người tham dự
     lấy từ Wikipedia **(chưa chắc)** [31a]; người đến rồi đi, không phải "hội nghị" lớn.
  6. **Shannon 1951** (*Bell System Technical Journal* 30, tr. 50–64): cho một người đọc một đoạn văn lạ và **đoán từng chữ cái
     tiếp theo**; đoán sai thì được báo chữ đúng rồi đoán tiếp. Câu thử bắt đầu "THE ROOM WAS NOT VERY LIGHT…"; trong 129 ký tự,
     **89 (69%)** đoán đúng ngay lần đầu [7]. Shannon kết luận tiếng Anh dư thừa ~75% khi tính ảnh hưởng xa tới 100 chữ cái [7].
- **Cảnh kể được:** ở Bell Labs, một người cầm bút chì đoán từng chữ của một cuốn sách lạ: T… H… E… dấu cách… R… Mỗi chữ đoán
  đúng, Shannon gạch một nét. Hết đoạn: 69% đúng mà không cần nhìn. (Danh tính người đoán: bài báo chỉ nói "the subject" — **không**
  nói là vợ Shannon.)
- **Hình:**
  - `Alan Turing (1951).jpg` — **Public domain** (Elliott & Fry, 29/03/1951).
  - `Baker Memorial Library, Dartmouth College - DSC09058.JPG` — **CC0** (Daderot) — cảnh Hanover; gắn **ẢNH MINH HỌA** (ảnh 2013).
  - `C.E. Shannon. Tekniska museet 43069.jpg` — **CC BY 2.0** (Tekniska museet) — ghi công; hoặc `Claude Shannon c1930.png` — **Public domain** (ảnh thời trẻ).
  - `Theseus Maze by Claude Shannon, 1952 - MIT Museum - DSC03702.JPG` — **CC0** (Daderot). Thêm:
    `John McCarthy (computer scientist) Stanford 2006 (272020300).jpg` — **CC BY 2.0** (null0); `Marvin Minsky (1).jpg` — **CC BY 2.0** (Joi);
    `Bell Telephone Laboratories, Murray Hill, New Jersey. LOC gsc.5a08393.jpg` — **Public domain** (LoC, 1942).
  - Văn bản đề xuất 1955: **không** có ảnh trên Commons (40/40 kết quả không phải ảnh raster) → dựng lại bằng chữ đánh máy,
    chỉ trích cụm ngắn.

### 2. "Hai con đường, và chiếc máy biết 'lắng nghe'" (1957–1968)

- **Vòng:** [Đóng V0 một phần] đặt Perceptron (học) cạnh trường phái "viết luật". [Mở V4] *"Họ hứa: trong 10 năm, máy sẽ vô địch
  cờ vua thế giới."* → đóng ở chương 4. [Mở V5] ELIZA → đóng ở chương 6 (ELIZA đọ sức với GPT-4.5 năm 2025).
- **Dữ kiện:**
  1. Simon & Newell, *Heuristic Problem Solving: The Next Advance in Operations Research*, Operations Research 6(1), 1958,
     tr. 1–10 [12]: bài diễn văn có các dự đoán "trong vòng mười năm", trong đó máy tính sẽ vô địch cờ vua thế giới
     **(chưa chắc nguyên văn: bản gốc sau paywall; nội dung dự đoán được nhiều nguồn thứ cấp dẫn lại)**.
  2. Joseph Weizenbaum (MIT), **ELIZA**, *Communications of the ACM* 9(1), 01/1966, tr. 36–45 [13]: chương trình chạy trên hệ
     chia sẻ thời gian MAC, đóng vai nhà trị liệu kiểu Rogers.
  3. Đoạn hội thoại mẫu trong bài: người dùng gõ "Men are all alike." — máy đáp "IN WHAT WAY" … "Well, my boyfriend made me
     come here." — "YOUR BOYFRIEND MADE YOU COME HERE" [13]. Cơ chế: bắt từ khoá, xoay "tôi/bạn", gắn câu mẫu.
  4. Weizenbaum tự viết: một số người thử "very hard to convince that ELIZA … is not human"; và ELIZA cho thấy dễ thế nào để tạo
     "the illusion of understanding" [13].
  5. Chuyện "cô thư ký xin Weizenbaum ra khỏi phòng" đến từ sách *Computer Power and Human Reason* (1976) **(chưa chắc: chưa
     đọc bản gốc)** → nếu dùng, gắn **DIỄN Ý**; an toàn hơn là dùng câu (4) có nguồn.
- **Cảnh kể được:** 1966, một chiếc máy đánh chữ nối vào máy tính MIT. Ai đó gõ: "Men are all alike." Máy gõ lại, chữ in hoa:
  "IN WHAT WAY". Không có trí tuệ nào bên trong — chỉ là gương phản chiếu từ khoá. Nhưng người gõ thì bắt đầu kể chuyện riêng.
- **Hình:**
  - `Organization of a biological brain and a perceptron.png` — **Public domain** (Rosenblatt 1958, hình ONR).
  - `Mark I Perceptron, Figure 2 of operator's manual.png` — **Public domain** (sổ tay vận hành, 15/02/1960).
  - `Weizenbaum 1982.jpg` — **Public domain** (RIT newsletter 1982).
  - `ELIZA conversation.png` — **Public domain**; tốt hơn: dựng lại đoạn hội thoại 1966 bằng chữ máy đánh chữ (không cần ảnh).
  - Tránh `Herbert A. Simon and Allen Newell Chess Match.jpg`: Commons ghi Public domain nhưng nguồn là ảnh trên trang AAAI qua
    Flickr cá nhân, căn cứ PD không rõ **(chưa chắc)**.

### 3. "Mùa đông thứ nhất" (1969–1980)

- **Vòng:** [Mở V6] *"Ý tưởng nơ-ron bị chôn. Ai sẽ đào nó lên — và bằng thứ gì?"* → đóng ở chương 5.
- **Dữ kiện:**
  1. Năm 1969, Minsky và Seymour Papert xuất bản sách *Perceptrons*, chỉ trích công trình của Rosenblatt và gần như "đóng nắp"
     hướng này; năm sau Minsky nhận giải Turing [8].
  2. Rosenblatt mất năm **1971**, chết đuối khi đi thuyền buồm *Shearwater* trên vịnh Chesapeake **đúng sinh nhật 43 tuổi**;
     ông mất hàng trăm nghìn USD tài trợ mỗi năm [8].
  3. Anh: báo cáo **Lighthill** (James Lighthill, Giáo sư Lucas, Cambridge; viết 07/1972, xuất bản 1973 cho Science Research
     Council) kết luận chưa phần nào của lĩnh vực tạo ra "the major impact that was then promised", và chỉ ra nguyên nhân chung là
     "combinatorial explosion" (bùng nổ tổ hợp) [14].
  4. Cornell mô tả sự lên–xuống của perceptron góp phần mở ra thời kỳ gọi là "AI winter", khi tiền tài trợ liên bang cạn [8].
  5. Mốc "mùa đông thứ nhất ~1974–1980" là quy ước của giới sử học, không phải mốc chính thức **(chưa chắc, Wikipedia)** [31b].
- **Cảnh kể được:** một người đàn ông 43 tuổi ra khơi trong ngày sinh nhật và không trở về; cỗ máy của ông nằm trong kho bảo
  tàng (vào Smithsonian năm 1967 theo bản ghi bảo tàng **(chưa chắc: trang Smithsonian chặn truy cập tự động, chi tiết lấy từ tóm
  tắt tìm kiếm)** [11]). Cắt sang: một báo cáo 1972 dùng chữ "thất vọng".
- **Hình:**
  - `Typical connections in a close-loop cross-coupled perceptron.png` — **Public domain** (Rosenblatt 1961).
  - `Isometric view of Tobermory Phase I.png` — **Public domain** (George Nagy, 1963, perceptron nhận giọng nói).
  - Báo cáo Lighthill: chỉ dựng chữ (bản quyền văn bản thuộc UKRI/STFC theo trang chilton **(chưa chắc phạm vi)** → trích
    cụm ngắn).
  - B-roll Pexels: tuyết, phòng thí nghiệm tắt đèn (gắn **ẢNH MINH HỌA**).

### 4. "Máy thắng người — nhưng không học gì" (1980s–1997)

- **Vòng:** [Đóng V4] *"Mười năm" thành **39 năm**.* [Mở V7] *"Deep Blue không tự học. Có một trò chơi không thể tính hết."* →
  đóng ở chương 5 (cờ vây).
- **Dữ kiện:**
  1. Thập niên 1980: bùng nổ "hệ chuyên gia" và máy Lisp chuyên dụng, rồi sụp đổ cuối thập niên — "mùa đông thứ hai"
     **(chưa chắc chi tiết năm, Wikipedia)** [31b]. Một máy Lisp CADR cuối 1970s đang ở MIT Museum (ảnh CC0).
  2. Tháng 02/1996 (Philadelphia) Kasparov thắng Deep Blue 4–2; tháng **05/1997** (New York) Deep Blue thắng **3,5–2,5**, hệ thống
     đầu tiên thắng nhà vô địch thế giới đương nhiệm theo thể thức thi đấu chuẩn [15].
  3. Deep Blue đánh giá **200 triệu thế cờ mỗi giây**, 32 bộ xử lý; nhóm gồm Feng-hsiung Hsu, Murray Campbell… [15].
  4. IBM dẫn lời Kasparov: lần đầu ông thấy thứ "similar to an artificial intellect" [15] (ngữ cảnh là ván nào **(chưa chắc)**).
  5. 1958 + 10 = 1968 theo dự đoán [12]; thực tế 1997 → trễ ~29 năm so với hạn, 39 năm sau lời hứa.
- **Cảnh kể được:** ván 6, tháng 5/1997, New York. Kasparov đứng dậy rời bàn sau chưa đầy 20 nước **(chưa chắc số nước — kiểm
  bằng file PGN ván 6 trước khi đọc)**. Trên bàn: hai tủ máy đen, 200 triệu thế cờ mỗi giây.
- **Hình:**
  - `Deep Blue versus Kasparov, 1997, Game 6.gif` — **CC0** (Morn) — hoạt ảnh ván 6, dựng lại thành bàn cờ động.
  - `IBM Deep Blue at Computer History Museum (9361685537).jpg` — **CC BY 2.0** (Anton Chiang).
  - `One of Deep Blue's processors (2586060990).jpg` — **CC BY 2.0** (Erik Pitti).
  - `CADR - The Lisp Machine, late 1970s, view 1 - MIT Museum - DSC03747.JPG` — **CC0** (Daderot); hoặc
    `Lisp machines in Computer History Museum.jpg` — **CC BY 2.0** (Jason Riedy).
  - Kasparov: chỉ có ảnh BY-SA (38/40) → **không dùng ảnh**, kể bằng bàn cờ.

### 5. "Con chip chơi game cứu AI" (1986–2016) — điểm giữa video, re-hook

- **Vòng:** [Đóng V0, V6] ý tưởng nơ-ron "thua cuộc" quay lại. [Đóng V7] cờ vây. [Mở V8] *"Máy đã nhìn được, chơi được. Nhưng
  nói chuyện được thì cần một mẹo khác."* → chương 6. Re-hook giữa video: quay lại ảnh Mark I Perceptron — "giờ bạn đã hiểu vì
  sao Cornell gọi nó là đi trước 60 năm" [8].
- **Dữ kiện:**
  1. Rumelhart, **Hinton**, Williams, *Learning representations by back-propagating errors*, Nature 323, tr. 533–536,
     **tháng 10/1986** [16] — tròn 40 năm trong tháng này (ngày 09/10 **(chưa chắc)**). Lưu ý: không phải "Hinton phát minh một mình".
  2. **AlexNet** (Krizhevsky, Sutskever, Hinton — ĐH Toronto): 60 triệu tham số, 650.000 nơ-ron; huấn luyện **5–6 ngày trên hai
     card GTX 580 3GB**; lỗi top-5 **15,3%** so với **26,2%** của đội thứ hai ở ILSVRC-2012 [17]. Bảng kết quả chính thức: đội
     "SuperVision" 0,15315; đội ISI 0,26172 [18].
  3. NVIDIA tự ghi trong dòng thời gian: 2006 ra kiến trúc CUDA mở GPU cho khoa học; 2012 AlexNet "sparks the era of modern AI"
     [19] — đây là lời *tự nhận* của hãng.
  4. **AlphaGo**: 10/2015 thắng Fan Hui 5–0; **03/2016** thắng Lee Sedol **4–1** ở Seoul, hơn 200 triệu người xem; ván 2 có
     "nước 37" xác suất ~1/10.000; ván 4 Lee Sedol đáp lại bằng "nước 78" cũng ~1/10.000 và thắng ván đó [20]. Bài Nature
     27/01/2016 [21].
  5. Cornell 2019: nhiều người cho rằng Rosenblatt đã được minh oan — nguyên lý perceptron là nền của học sâu [8].
- **Cảnh kể được (cảnh mạnh thứ hai, ~75% video có thể đặt AlphaGo):** Seoul, ván 4. Lee Sedol thua ba ván liền. Nước 78 — một
  nước mà chính máy ước chừng 1/10.000 người sẽ đi. Lần duy nhất con người thắng trong trận đó [20].
- **Hình:**
  - `NVIDIA@40nm@Fermi@GF110@GeForce GTX 580@UA10B338 1041A1 N2Y540.000 GF110-375-A1 DSC04152 (27576804994).jpg` — **CC0** (Fritzchens Fritz), die chip GTX 580.
  - `Geforce8800gtx.jpg` — **Public domain** (card GeForce 8800 GTX, đời có CUDA).
  - `Stone Pieces for Baduk (Board Game) (17173187033).jpg` — **CC0** (Gary Todd).
  - `Lee Se-Dol.jpg` — **CC BY 2.0** (LG Electronics, 2016, 650×598 — nhỏ, chỉ dùng khung thẻ).
  - `Deep Thinkers on Deep Learning (cropped to Geoffrey Hinton).jpg` — **CC BY 2.0** (Steve Jurvetson; 298×418 — rất nhỏ) hoặc
    `Geoffrey Hinton - Collision 2023 - Centre Stage RCZ 1307 (cropped).jpg` — **CC BY 2.0** (Ramsey Cardy/Collision via Sportsfile).
  - NASA video `ARC-20190821-AAV3214-ModularSupercomputer-BRollResource-NASAWeb` (b-roll siêu máy tính, Ames) — gắn **ẢNH MINH HỌA**.

### 6. "Đoán chữ tiếp theo" (2017–2025)

- **Vòng:** [Đóng V2] trò chơi Shannon 1951 = nguyên lý ChatGPT. [Đóng V3] lời tiên đoán của Turing. [Đóng V5] ELIZA đọ sức
  2025. [Đóng V8].
- **Dữ kiện:**
  1. *Attention Is All You Need* (8 tác giả, Google), nộp arXiv **12/06/2017**: bỏ hẳn hồi quy và tích chập, chỉ dùng cơ chế
     attention; đạt kết quả hàng đầu sau **3,5 ngày trên 8 GPU** [22].
  2. OpenAI giới thiệu ChatGPT ngày **30/11/2022** dưới dạng "research preview" [23] (trang OpenAI chặn truy cập tự động; ngày
     xác nhận qua nguồn thứ cấp **(chưa chắc ở mức nguồn gốc)**).
  3. Bài nghiên cứu của chính OpenAI (15/09/2025): đến **07/2025**, **700 triệu** người gửi **18 tỉ** tin nhắn mỗi tuần, ~10% người
     trưởng thành trên thế giới [24]. Số 2026 (900 triệu → 1,2 tỉ/tuần) chỉ thấy ở nguồn thứ cấp **(chưa chắc)** [37] — nếu đọc,
     nói "theo OpenAI công bố tháng X/2026" sau khi kiểm bản gốc.
  4. Cơ chế (giải thích): mô hình chọn **mẩu chữ (token)** tiếp theo có xác suất cao, lặp lại hàng trăm lần cho một câu trả lời —
     cùng tinh thần với người đoán chữ của Shannon [7]. Đây là **đơn giản hoá**; nói rõ "nói gọn là…".
  5. Jones & Bergen (UC San Diego), preprint arXiv 31/03/2025: trong phép thử Turing ba bên, 5 phút, **GPT-4.5** (được dặn đóng vai
     người) bị chọn là "người" **73%** số lần; **ELIZA** chỉ **23%** [25]. Preprint, trạng thái bình duyệt **(chưa chắc)**.
     Turing hẹn ~năm 2000 với ngưỡng 70% đoán đúng [6] → máy "đạt" muộn ~25 năm, và theo cách khác hẳn ông hình dung.
- **Cảnh kể được:** đặt hai màn hình cạnh nhau: bên trái là dòng "THE ROOM WAS NOT VERY LIGHT" hiện từng chữ với dấu gạch cho
  chữ đoán đúng (1951); bên phải là ô chat hiện từng mẩu chữ (2022). Cùng một trò chơi, cách nhau 71 năm.
- **Hình:**
  - `Red-Black by Claude Shannon, game-playing machine, c. 1951 - MIT Museum - Cambridge, MA - DSC09108.jpg` — **CC0** (Daderot) — callback Shannon.
  - `Encoder self-attention, detailed diagram.png` — **CC BY 4.0** (dvgodoy) — hoặc tự vẽ sơ đồ attention (khuyên dùng).
  - `Data center roof.jpg` — **CC0** (Rsparks3, 2025).
  - Giao diện chat: **tự dựng**, không logo, không chụp màn hình ChatGPT (nhãn hiệu/bản quyền giao diện — xem `media-sources` mục 7).
  - B-roll Pexels: tay gõ điện thoại (không lộ mặt).

### 7. Văn hoá đại chúng — "Phim đã dạy chúng ta sợ (và thương) AI thế nào" (~80% video)

- **Vòng:** không mở vòng mới; là "phần thưởng" trước kết. Quy tắc 3 mục, mục thứ ba bất ngờ nhất.
- **Dữ kiện (chỉ mốc phát hành, nguồn Wikipedia — không tranh cãi):**
  1. **HAL 9000** — phim *2001: A Space Odyssey* (1968), cỗ máy bình tĩnh từ chối mở cửa [31c].
  2. **Skynet** — *Kẻ hủy diệt* (1984) và phần 2 (1991); trong phim, "ngày phán xét" đặt vào **tháng 8/1997** — cùng năm Deep Blue
     thắng Kasparov thật ngoài đời [31d][15] **(chưa chắc ngày cụ thể trong cốt truyện; kiểm lại trước khi đọc)**.
  3. **Doraemon** — truyện tranh của Fujiko F. Fujio ra mắt **cuối 1969** [31e] **(chưa chắc tháng)** — cùng năm sách *Perceptrons*
     mở màn mùa đông AI [8]. Với khán giả Việt (bài "Doraemon" 143 lượt/ngày [1]), đây là hình mẫu "AI làm bạn" thay vì "AI diệt
     loài người".
- **Cảnh kể được:** một đứa trẻ Việt những năm 1990 đọc Doraemon dưới gầm bàn; cùng lúc ở Mỹ, giới nghiên cứu AI đang trong mùa
  đông thứ hai. (Chi tiết "những năm 1990 ở VN" là bối cảnh chung, không nêu số liệu.)
- **Hình:** **không** dùng ảnh phim/nhân vật (bản quyền; kể cả ảnh đạo cụ HAL trên Commons là tác phẩm phái sinh). Dùng chữ
  động, đồ hoạ trừu tượng tự vẽ (một chấm đỏ, một bóng người kim loại, một cánh cửa thần kỳ… **không** sao chép thiết kế nhân vật).

### 8. Kết mở — "Mùa hè thứ 70" (~90–100%)

- **Vòng:** [Đóng V1] *"Họ xin một mùa hè. Đã là 70 mùa hè."* Trả motif mùa: còn là mùa hè, hay mùa đông thứ ba đang tới?
- **Dữ kiện:**
  1. 08/10/2024: Nobel Vật lý cho **John Hopfield** và **Geoffrey Hinton** "for foundational discoveries and inventions that enable
     machine learning with artificial neural networks" [26]. 09/10/2024: nửa Nobel Hoá cho **Demis Hassabis** và **John Jumper**
     (AlphaFold2 dự đoán cấu trúc gần như toàn bộ ~200 triệu protein đã biết) [27].
  2. Trong phỏng vấn Nobel, Hinton nói ta đang ở một "bifurcation point" và cần tìm cách giữ quyền kiểm soát [28].
  3. Dartmouth, nơi đặt tên ngành, tổ chức hội nghị **"AI at 70: What Must Remain Human?"** ngày **29–31/10/2026**; Yann LeCun
     nhận giải AI at 70; hiệu trưởng nói câu hỏi đã đổi từ "máy có mô phỏng được trí tuệ không" sang "làm sao để AI tăng cường
     chứ không thay thế phán đoán của con người" [4][5].
  4. Callback Turing: ông coi câu "máy có nghĩ được không" là vô nghĩa, nhưng tin cuối thế kỷ người ta sẽ nói "máy nghĩ" mà không
     ai cãi [6]. → câu hỏi để lại cho người xem.
  5. Nobel 2026: Vật lý công bố 6/10, Hoá 7/10 [29] — **kiểm kết quả trước khi khoá kịch bản**; không đoán trước.
- **Cảnh kể được:** Hanover, cuối tháng 10/2026, lá đỏ. 70 năm trước, 10 người hẹn nhau ở đây cho một mùa hè. Năm nay, câu hỏi
  trên băng-rôn là: điều gì phải giữ lại cho con người? (Chi tiết "lá đỏ" là mô tả mùa thu chung → gắn **ẢNH MINH HỌA** nếu dùng b-roll.)
- **Hình:**
  - `Geoffrey Hinton - Collision 2023 - Centre Stage RCZ 1307 (cropped).jpg` — **CC BY 2.0**.
  - `Baker Memorial Library, Dartmouth College - DSC09058.JPG` — **CC0** (trả cảnh chương 1).
  - `Alan Turing Aged 16.jpg` — **Public domain** (callback cuối).
  - `JensenHuangSC18.jpg` — **CC0** — chỉ nếu nhắc tới cầu nối sang video #2 (GPU).

---

## 5. Kiểm kê hình mở

**Đếm Commons** (`generator=search`, namespace File, 40 kết quả đầu, phân loại theo `LicenseShortName`, 06/10/2026):

| Truy vấn | PD/CC0 | CC BY | BY-SA | Không phải raster | Nhận xét |
|---|---:|---:|---:|---:|---|
| Alan Turing | 16 | 2 | 21 | 1 | Đủ chân dung PD |
| Frank Rosenblatt / Mark I perceptron | 1 + 2 | 0 | 3 | — | Ảnh Hải quân PD là "át chủ bài" |
| Claude Shannon | 14 | 4 | 9 | 13 | Nhiều ảnh máy của Shannon (MIT Museum, CC0) |
| Deep Blue | 5 (gồm 2 ảnh tàu tên Deep Blue) | 6 | 28 | 1 | Dùng BY |
| Garry Kasparov | 1 (chữ ký) | 1 | 38 | 0 | Không có ảnh dùng được |
| AlphaGo Lee Sedol | 0 | 2 | 12 | 10 | Ảnh nhỏ |
| Marvin Minsky | 4 (không phải chân dung) | 9 | 8 | 19 | Dùng BY |
| John McCarthy | 0 liên quan | 1 | 5 | 33 | Một ảnh BY |
| Geoffrey Hinton | 0 | 10 | 30 | 0 | Dùng BY |
| IBM 704 | 8 | 3 | 6 | 23 | NASA PD |
| GTX 580 / GeForce 8800 | 12 / 16 | 1 / 3 | 5 / 19 | — | Chip PD/CC0 dồi dào |
| Dartmouth AI 1956 / đề xuất | 0 | 0 | 0 | 13 / 40 | **Không có ảnh 1956** → dựng chữ |
| HAL 9000 | 6 (phần lớn không liên quan) | 8 | 18 | 8 | **Không dùng** (phái sinh từ đạo cụ phim) |

**NASA Images API** (không khoá): "IBM 704" 2 kết quả (`LRC-1957-B701_P-05391`, `ARC-1969-A-24321`); "supercomputer" 67 kết quả,
12 video trên trang đầu (vd. `ARC-20190821-AAV3214-ModularSupercomputer-BRollResource-NASAWeb`, ảnh `GSFC_20171208_Archive_e002030`
"Discover Supercomputer"); "artificial intelligence" 96 (chủ yếu ảnh hội nghị NASA 2024, ít giá trị); "neural network" 1; "GPU" 0.
Tránh logo NASA, ghi "Nguồn: NASA" (quy tắc trong `media-sources` mục 5).

**Smithsonian:** Mark I Perceptron có bản ghi NMAH `nmah_334414` [11]; trang si.edu và collections.si.edu trả 403/lỗi DNS với script
hôm nay → **chưa xác định được ảnh có CC0 không** **(chưa chắc)**. IBM nói Deep Blue được đưa về Smithsonian [15] — cũng chưa kiểm
ảnh. Không dùng tới khi có người kiểm bằng tay.

**Pexels (b-roll):** hợp lý cho cảnh khái niệm: bàn cờ vua/cờ vây, tay gõ điện thoại, hành lang máy chủ, tuyết (mùa đông),
khuôn viên mùa hè. **Chưa đếm** (cần khoá API). Không dùng clip có mặt người rõ ở chương nói về lừa đảo/nguy cơ.

**Giấy phép theo kênh:** PD/CC0/CC BY được, **không** BY-SA (theo chính sách đường dựng video dài và quyết định #5 của
`stier-design`). Mọi file CC BY phải vào khối ghi công trong mô tả: tác giả + giấy phép + link file.

---

## 6. Huyền thoại / lỗi thường gặp cần tránh

| Hay nói sai | Đúng là | Nguồn |
|---|---|---|
| "Thuật ngữ AI ra đời *tại* hội thảo Dartmouth 1956" | Đã có trong văn bản đề xuất ký 31/08/1955 | [2] |
| "Dartmouth 1956 là một hội nghị lớn" | Một dự án nghiên cứu mùa hè, đề xuất "2 tháng, 10 người", người đến rồi đi **(chưa chắc chi tiết tham dự)** | [2][31a] |
| "Turing hỏi 'máy có nghĩ được không' và trả lời là có" | Ông cho câu hỏi gốc là vô nghĩa, thay bằng trò chơi bắt chước; chỉ *dự đoán* cách người ta sẽ nói năm 2000 | [6] |
| "Rosenblatt nói máy sẽ biết đi, biết nói, có ý thức" | Câu đó là kỳ vọng của Hải quân do NYT thuật lại **(chưa chắc: chưa đọc bản gốc)**; Rosenblatt nói "có ý tưởng độc đáo" | [8] |
| "Minsky chứng minh mạng nơ-ron vô dụng" | Sách 1969 phân tích giới hạn của perceptron (một lớp); bị *hiểu* thành án tử cho cả hướng. Nói "chỉ trích", không nói "chứng minh vô dụng" **(chưa chắc nội dung kỹ thuật, chưa đọc sách)** | [8][31f] |
| "Deep Blue là AI biết học" | Tìm kiếm cưỡng bức 200 triệu thế cờ/giây với hàm đánh giá do người chỉnh | [15] |
| "AlphaGo thắng Lee Sedol 5–0" | 4–1; Lee Sedol thắng ván 4 (nước 78). 5–0 là trận với Fan Hui 2015 | [20] |
| "Hinton một mình phát minh lan truyền ngược" | Bài 1986 có 3 tác giả (Rumelhart, Hinton, Williams); ý tưởng có tiền thân trước đó **(chưa chắc)** | [16] |
| "NVIDIA phát minh ra GPU năm 1999" | Đó là cách NVIDIA tự mô tả; chip đồ hoạ có trước. Nói "NVIDIA gọi là GPU đầu tiên" | [19] |
| "ChatGPT hiểu bạn / tra Internet để trả lời" | Mô hình sinh mẩu chữ tiếp theo theo xác suất (đơn giản hoá); việc tra web là tính năng thêm, tuỳ phiên bản | [22][7] |
| "ChatGPT đã vượt phép thử Turing" | Nghiên cứu 2025 thử **GPT-4.5** (được dặn đóng vai người), preprint; không phải ChatGPT 2022 | [25] |
| "Mùa đông AI = không ai nghiên cứu" | Tiền tài trợ cạn, nghiên cứu vẫn tiếp tục (Hinton 1986 nằm giữa hai mùa đông) | [8][16] |
| "Người đoán chữ trong thí nghiệm Shannon là vợ ông" | Bài báo chỉ ghi "the subject" | [7] |
| Đọc kết quả Nobel 2026 khi chưa công bố | Vật lý 6/10, Hoá 7/10/2026 — đợi kết quả chính thức | [29] |

---

## 7. Gợi ý phát âm cho TTS tiếng Việt

Theo RETENTION.md: mỗi tên nước ngoài đi kèm mô tả ngắn ở lần đầu ("Alan Turing, nhà toán học Anh…"). Đề xuất cách viết
phiên âm trong kịch bản đọc (phụ đề giữ chữ gốc):

| Chữ gốc | Gợi ý đọc | Chữ gốc | Gợi ý đọc |
|---|---|---|---|
| Dartmouth | Đát-mâu | Hanover | Ha-nô-vơ |
| John McCarthy | Giôn Mơ-ca-thi | Marvin Minsky | Mác-vin Min-xki |
| Claude Shannon | Clốt Sen-nần | Nathaniel Rochester | Na-tha-ni-en Rô-chét-xtơ |
| Alan Turing | A-lần Tiu-rinh | Frank Rosenblatt | Phrăng Râu-dần-blát |
| Perceptron | Pơ-xép-trôn | IBM 704 | Ai-bi-em bảy-không-bốn |
| ELIZA | Ê-lai-dơ | Joseph Weizenbaum | Giô-dép Vai-dần-bom |
| Herbert Simon / Allen Newell | Hơ-bớt Sai-mần / A-lần Niu-ồn | Lighthill | Lai-hiu |
| Deep Blue | Đíp Blu | Garry Kasparov | Ga-ri Ca-xpa-rốp |
| Lisp | Líp-xp | AlexNet | A-léc-nét |
| ImageNet | I-mịt-nét | GPU | Gi-pi-iu |
| NVIDIA / CUDA | En-vi-đi-a / Cu-đa | GeForce GTX 580 | Gi-pho Gi-ti-ích năm-tám-mươi |
| Geoffrey Hinton | Giép-phri Hin-tần | AlphaGo | An-pha Gô |
| Lee Sedol | Li Xê-đôn | Transformer | Tran-xphó-mơ |
| ChatGPT | Chát Gi-pi-ti | OpenAI | Ô-pần Ai |
| token | tô-kần | GPT-4.5 | Gi-pi-ti bốn chấm năm |
| Hopfield | Hóp-phin | Demis Hassabis | Đê-mít Ha-xa-bít |
| Yann LeCun | Gian Lơ-căng | HAL 9000 | Han chín nghìn |
| Skynet | Xcai-nét | Rockefeller | Rốc-cơ-phe-lơ |

Viết tắt: đọc "trí tuệ nhân tạo" ở lần đầu rồi "AI" (ây-ai) — cần thử giọng Hải Đăng đọc "AI" có ra "ây-ai" không, nếu không
thì viết "ây ai" trong kịch bản đọc.

---

## 8. Đóng gói

**Tựa (3 phương án cho Test & Compare):**
1. *AI Đã "Chết" Hai Lần Trước Khi Có ChatGPT*
2. *Họ Nghĩ Chỉ Cần 1 Mùa Hè Để Tạo Ra AI. Mất 70 Năm.*
3. *70 Năm AI: Từ Cỗ Máy 5 Tấn Đến ChatGPT Trong Túi Bạn*

(Đặt "ChatGPT"/"AI" ở nửa đầu tựa: đây là từ người Việt tự gõ [1]; tránh "Dartmouth" trong tựa.)

**Thumbnail:** nền xanh than của theme MIM; nửa trái là ảnh Mark I Perceptron (PD, đen trắng, tương phản cao, cắt vào mớ dây
cáp); nửa phải một ô chat cyan phát sáng với con trỏ nhấp nháy; chữ lớn vàng/trắng **"CHẾT 2 LẦN"** (hoặc **"70 NĂM"** cho
phương án 3). Không logo OpenAI/NVIDIA, không mặt người thật. Cold open phải mở đúng bằng ảnh Perceptron để khớp thumbnail.

**Chương YouTube (gợi ý tên có từ khoá):** 00:00 Cỗ máy học trái phải (1958) · Hội thảo Dartmouth 1956: AI ra đời · ELIZA:
chatbot đầu tiên · Mùa đông AI · Deep Blue thắng Kasparov · GPU, AlexNet, AlphaGo · ChatGPT đoán chữ thế nào · Phim và AI · 70 năm
AI: tiếp theo là gì?

**Short mồi (từ chính video, đăng trước 1–2 tuần):** (1) "Năm 1958, máy tính 5 tấn học được trái và phải sau 50 lần thử"; (2)
"Chatbot 1966 khiến người ta tưởng là người thật"; (3) "Năm 1951 Shannon đã chơi trò mà ChatGPT đang chơi".

---

## 9. Nguồn

1. Wikimedia Pageviews REST API (vi.wikipedia, all-access, user, daily, 20260708–20261005): `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/vi.wikipedia/all-access/user/{bài}/daily/20260708/20261005`
2. McCarthy, Minsky, Rochester, Shannon, *A Proposal for the Dartmouth Summer Research Project on Artificial Intelligence*, 31/08/1955: http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html
3. Dartmouth, *Artificial Intelligence (AI) Coined at Dartmouth*: https://home.dartmouth.edu/about/artificial-intelligence-ai-coined-dartmouth
4. Dartmouth News, *Dartmouth to Host AI at 70 Conference in October* (08/2026): https://home.dartmouth.edu/news/2026/08/dartmouth-host-ai-70-conference-october
5. Dartmouth, AI 70th anniversary signature events: https://ai.dartmouth.edu/70th-anniversary ; https://home.dartmouth.edu/news/2026/02/celebrating-ai-milestone-and-guiding-future
6. A. M. Turing, *Computing Machinery and Intelligence*, Mind LIX(236):433–460, 10/1950: https://academic.oup.com/mind/article/LIX/236/433/986238 (doi:10.1093/mind/LIX.236.433)
7. C. E. Shannon, *Prediction and Entropy of Printed English*, Bell System Technical Journal 30:50–64, 01/1951: https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf (doi:10.1002/j.1538-7305.1951.tb01366.x)
8. Cornell Chronicle (M. Lefkowitz, 25/09/2019), *Professor's perceptron paved the way for AI – 60 years too soon*: https://news.cornell.edu/stories/2019/09/professors-perceptron-paved-way-ai-60-years-too-soon
9. Ảnh Hải quân Mỹ 330-PSA-80-60 (USN 710739), mô tả trên Commons: https://commons.wikimedia.org/wiki/File:330-PSA-80-60_(USN_710739)_(20897323365).jpg
10. F. Rosenblatt, *The perceptron: A probabilistic model for information storage and organization in the brain*, Psychological Review 65:386–408 (1958), doi:10.1037/h0042519 (siêu dữ liệu: https://api.crossref.org/works/10.1037/h0042519)
11. Smithsonian NMAH, *Electronic Neural Network, Mark I Perceptron*: https://americanhistory.si.edu/collections/object/nmah_334414 (403 với script; chi tiết qua tóm tắt tìm kiếm — chưa chắc)
12. H. A. Simon, A. Newell, *Heuristic Problem Solving: The Next Advance in Operations Research*, Operations Research 6(1):1–10 (1958): https://pubsonline.informs.org/doi/10.1287/opre.6.1.1 (paywall)
13. J. Weizenbaum, *ELIZA — A Computer Program For the Study of Natural Language Communication Between Man and Machine*, CACM 9(1):36–45, 01/1966, doi:10.1145/365153.365168; bản đọc: https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf
14. J. Lighthill, *Artificial Intelligence: A General Survey* (07/1972; in trong *Artificial Intelligence: a paper symposium*, SRC 1973): https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm
15. IBM, *Deep Blue*: https://www.ibm.com/history/deep-blue
16. D. Rumelhart, G. Hinton, R. Williams, *Learning representations by back-propagating errors*, Nature 323:533–536, 10/1986, doi:10.1038/323533a0 (siêu dữ liệu: https://api.crossref.org/works/10.1038/323533a0)
17. A. Krizhevsky, I. Sutskever, G. Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NIPS 2012: https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html (PDF: https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)
18. ImageNet, ILSVRC2012 results: https://image-net.org/challenges/LSVRC/2012/results.html
19. NVIDIA, Corporate timeline: https://www.nvidia.com/en-us/about-nvidia/corporate-timeline/
20. Google DeepMind, *AlphaGo*: https://deepmind.google/research/breakthroughs/alphago/
21. D. Silver et al., *Mastering the game of Go with deep neural networks and tree search*, Nature 529:484–489 (27/01/2016), doi:10.1038/nature16961
22. A. Vaswani et al., *Attention Is All You Need*, arXiv:1706.03762 (12/06/2017): https://arxiv.org/abs/1706.03762
23. OpenAI, *Introducing ChatGPT* (30/11/2022): https://openai.com/index/chatgpt/ (403 với script); xác nhận ngày qua TechCrunch: https://techcrunch.com/2025/11/30/chatgpt-launched-three-years-ago-today/
24. A. Chatterji et al. (OpenAI), *How People Use ChatGPT* (15/09/2025): https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf
25. C. R. Jones, B. K. Bergen, *Large Language Models Pass the Turing Test*, arXiv:2503.23674 (31/03/2025): https://arxiv.org/abs/2503.23674
26. Nobel Prize, Physics 2024 press release (08/10/2024): https://www.nobelprize.org/prizes/physics/2024/press-release/
27. Nobel Prize, Chemistry 2024 press release (09/10/2024): https://www.nobelprize.org/prizes/chemistry/2024/press-release/
28. Nobel Prize, Geoffrey Hinton — interview & facts: https://www.nobelprize.org/prizes/physics/2024/hinton/interview/ ; https://www.nobelprize.org/prizes/physics/2024/hinton/facts/
29. Nobel Prize, announcement dates 2026: https://www.nobelprize.org/prizes/about/prize-announcement-dates/
30. MIT News, *Marvin Minsky, "father of artificial intelligence," dies at 88* (25/01/2016): https://news.mit.edu/2016/marvin-minsky-obituary-0125
31. Wikipedia (chỉ làm con trỏ / mốc không tranh cãi): (a) https://en.wikipedia.org/wiki/Dartmouth_workshop · (b) https://en.wikipedia.org/wiki/AI_winter · (c) https://en.wikipedia.org/wiki/2001:_A_Space_Odyssey · (d) https://en.wikipedia.org/wiki/Terminator_2:_Judgment_Day · (e) https://en.wikipedia.org/wiki/Doraemon · (f) https://en.wikipedia.org/wiki/Perceptrons_(book)
32. VTV, *Học sinh phổ thông sẽ được học AI đại trà từ năm học 2026-2027*: https://vtv.vn/hoc-sinh-pho-thong-se-duoc-hoc-ai-dai-tra-tu-nam-hoc-2026-2027-100260820224933772.htm
33. Báo/blog Việt về lịch sử AI: https://tiasang.com.vn/nua-the-ky-tri-tue-nhan-tao-4982917.html ; https://vinuni.edu.vn/vi/tri-tue-nhan-tao-ra-doi-khi-nao/
34. Wikimedia Commons API (`generator=search`, `prop=imageinfo&iiprop=extmetadata|size`): https://commons.wikimedia.org/w/api.php · NASA Images API: https://images-api.nasa.gov/search · Crossref API: https://api.crossref.org/works/
35. UCLA Samueli, *Internet50* (29/10/1969, 3420 Boelter Hall): https://samueli.ucla.edu/internet50/
36. Nội bộ: `docs/channels/mind-in-the-machine/2026-10-06-media-sources.md` (quy tắc giấy phép, NASA), `motion/long/RETENTION.md`
37. (Thứ cấp, chưa chắc) Số người dùng ChatGPT 2026: https://fourweekmba.com/ai-chatgpt-12b-weekly-users-devday-2026-distribution/
