# Nghiên cứu đề tài — Mind in the Machine (MIM) — 06/10/2026

Phạm vi: chọn đề tài cho 3 dòng Short (*AI giải thích*, *mẹo AI 30 giây*, *công nghệ đã thay đổi thế giới*) cho khán giả
phổ thông Việt Nam, tiếp nối hướng A + B trong `2026-10-05-analysis.md`. Nguồn: báo Việt, báo cáo công khai, diễn đàn,
trang trợ giúp YouTube, và Wikimedia pageviews REST API (vi.wikipedia, `user`, 28 ngày 07/09 → 04/10/2026). Không dùng
YouTube API, không cào YouTube hay Google Trends, không lập bảng số liệu kênh khác. Chỗ nào chưa chắc đều ghi **(chưa chắc)**.

## 1. Tóm tắt

- **Nhu cầu "dùng AI cho đúng" rất lớn và rất Việt.** 78% người dùng Internet VN đã dùng ít nhất một nền tảng AI
  (Decision Lab, khảo sát 7/2025) [1]; thời gian dùng app AI ở VN nửa đầu 2026 hơn gấp đôi cùng kỳ (Sensor Tower, qua
  VnExpress) [2]; 89% câu lệnh Gemini ở VN gõ bằng tiếng Việt [2][3]. Người ta đã *dùng*, cái thiếu là *dùng đúng*:
  mẹo thực dụng có cầu thật.
- **Ba nỗi lo nổi nhất: lừa đảo deepfake, mất việc, con cái học bằng AI.** 61% người Việt lo mất việc vì AI (UNDP,
  12/2025) [4]; 95,9% học sinh 15 tuổi VN từng dùng chatbot để học, cao nhất trong khảo sát PISA 2025 (công bố 9/2026)
  [5]; công an liên tục cảnh báo giả giọng, giả mặt người quen [6][7]. Đây là "nỗi đau" nên làm hook.
- **Thời điểm học đường:** từ năm học 2026–2027 mọi học sinh phổ thông học 12 tiết AI/năm [8]. Phụ huynh và giáo
  viên là khán giả mới cần giải thích khái niệm AI bằng lời thường.
- **Wikipedia-vi: người/sản phẩm quen thuộc kéo xem hơn khái niệm.** "Jensen Huang" ~121 lượt/ngày, "Mark Zuckerberg"
  ~164, "Mã QR" ~179, "Thomas Edison" ~200; trong khi "Deepfake" ~15, "Bộ xử lý đồ họa" ~6. → Giải thích khái niệm
  qua thứ người xem đã biết (QR, TikTok, Nvidia), không mở bằng thuật ngữ.
- **Chủ đề lịch sử công nghệ có mốc ngày gần:** Google mua YouTube tròn 20 năm (9/10), iPod 25 năm (23/10), tin nhắn
  ARPANET đầu tiên (29/10/1969), tuần Nobel 5–12/10 (Nobel 2024 trao cho nghiên cứu nền tảng AI) [9][10]; năm 2026
  cũng là 150 năm bằng sáng chế điện thoại của Bell và 100 năm buổi trình diễn truyền hình của Baird.
- **Tên mô hình AI đổi từng tuần — tránh làm trục nội dung.** Chỉ trong 9/2026 OpenAI có GPT-6 Astra, rồi Sol/Luna;
  API Sora bị khai tử 24/9 [11][12]. Dòng *AI giải thích* nên bám khái niệm bền (token, ảo giác, deepfake), không bám tên
  sản phẩm/giá.
- **Rủi ro chính sách là "sản xuất hàng loạt", không phải "dùng AI".** YouTube không buộc khai báo giọng AI cho video
  có kịch bản hay hoạt hình [13], nhưng chính sách *inauthentic content* chặn kiếm tiền với nội dung theo khuôn, lặp lại
  [14]. Luật AI VN (hiệu lực 1/3/2026) + Nghị định 142/2026 (1/5/2026) buộc gắn nhãn nội dung AI mô phỏng người thật
  hoặc tái hiện sự kiện thật [15][16]: liên quan trực tiếp dòng *công nghệ đã thay đổi thế giới* nếu dùng ảnh AI giống
  thật về nhân vật lịch sử.

## 2. Nhu cầu: người Việt đang hỏi, lo, tò mò gì về AI (cuối 2026)

**Mức độ dùng.** Decision Lab (600 người, online, 7/2025): 78% từng dùng AI trong 3 tháng; ChatGPT 81%, Gemini 51%,
Meta AI 36%; lý do chính là tiết kiệm thời gian và hỗ trợ học tập [1][17]. Sensor Tower H1/2026 (qua VnExpress): 704
triệu giờ dùng app AI, top 3 là ChatGPT, Gemini và app Việt **AI Hay**; xu hướng chuyển từ hỏi đáp sang dịch tài liệu,
làm bài tập, việc văn phòng [2]. Microsoft (qua VietNamNet): 27,9% người 15–64 tuổi dùng AI trong Q2/2026, đứng 2 Đông
Nam Á sau Singapore [3]. Work Trend Index 2026 của Microsoft: 82% người dùng AI ở VN sợ bị tụt lại nếu không áp dụng
nhanh [18]. (Các khảo sát khác nhau về mẫu và định nghĩa "dùng AI", không cộng trừ với nhau được.)

**Nỗi lo.**
- *Mất việc:* UNDP (2/12/2025) — 61% lo mất việc hoặc khó tìm việc vì AI, cao nhất Đông Nam Á; việc đầu đời như hành
  chính, soạn văn bản, dịch thuật bị nêu là dễ ảnh hưởng [4]. Đối trọng: nghiên cứu CESifo (Dân Trí 28/9/2026) chưa thấy
  AI gây thất nghiệp diện rộng ở cử nhân trẻ Mỹ [19]. → đề tài "AI lấy việc gì, chưa lấy việc gì" có cả hai phía.
- *Lừa đảo:* deepfake giả giọng/mặt người thân để vay tiền bùng lên dịp Tết 2026; Công an Hà Nội liệt kê 25 kịch bản
  lừa đảo mạng 2026, có AI/deepfake [6][7]. Công an cũng cảnh báo trào lưu up ảnh chân dung vào app tạo ảnh AI không rõ
  nguồn [20].
- *Con cái và học tập:* PISA 2025 — 95,9% học sinh VN từng dùng chatbot để học, nhưng chỉ ~41% đạt mức đọc hiểu cơ
  bản [5]; VTV (4/10/2026) nêu lo ngại suy giảm tư duy, AI tính sai [21]. Bộ GD&ĐT đưa 12 tiết AI/năm từ 2026–2027 [8].
- *Tin vào AI:* nghiên cứu EBU/BBC — 45% câu trả lời tin tức của trợ lý AI có ít nhất một lỗi đáng kể [22]; Reuters
  Institute DNR 2026: dùng chatbot để đọc tin hàng tuần tăng từ 7% lên 10%, chỉ 20% công chúng tin tin tức từ chatbot
  [23].

**Câu hỏi thực tế trên diễn đàn/báo.** Voz: có nên trả tiền ChatGPT hay Gemini, gói sinh viên bị yêu cầu xác minh lại,
mua tài khoản "giá rẻ" qua bên thứ ba/bot Telegram [24][25]; Tinhte: hướng dẫn ChatGPT "từ A–Z cho người mới" [26];
báo chí: đặt câu hỏi cụ thể, kiểm chứng thông tin y tế/pháp lý/tài chính, không nhập dữ liệu nhạy cảm [27]. VnExpress
đang chạy khảo sát thói quen dùng AI (28/9–4/10/2026) — **nên đọc kết quả khi công bố** [28].

**Tín hiệu Wikipedia-vi cho đề tài ngoài 21 chủ đề đang theo dõi** (trung vị lượt xem/ngày, 07/09–04/10/2026,
người dùng thật). Mốc so sánh: "Trí tuệ nhân tạo" 1.022, "ChatGPT" 412 (đã theo dõi).

| Bài | Trung vị/ngày | Bài | Trung vị/ngày |
|---|---:|---|---:|
| YouTube | 705 | Sam Altman | 36 |
| TikTok | 257 | GPS | 34 |
| Zalo | 206 | Flappy Bird | 30 |
| Thomas Edison | 200 | Nguyễn Hà Đông | 29 |
| Mã QR | 179 | Wi-Fi / Anh em nhà Wright | 27 / 27 |
| Mark Zuckerberg | 164 | Bluetooth | 26 |
| Nikola Tesla | 126 | Truyền hình | 25 |
| Jensen Huang | 121 | Netflix | 24 |
| Apple Inc. | 102 | Blockchain / Transistor | 23 / 22 |
| Shopee / Siri | 91 / 91 | Đèn sợi đốt | 22 |
| Android (hệ điều hành) | 80 | Phép thử Turing | 19 |
| Động cơ hơi nước | 59 | Pin Li-ion / Mã vạch | 18 / 18 |
| Microsoft / Linux / Samsung | 59 / 57 / 56 | Deepfake | 15 |
| 5G | 50 | Chuột (máy tính) | 8 |
| Instagram | 40 | Geoffrey Hinton / Ada Lovelace | 8 / 8 |
| Alexander Graham Bell | 39 | Bộ xử lý đồ họa | 6 |
| Máy bay | 37 | Deep Blue / Robot dạng người | 4 / 1,5 |
| VinFast | 114 | Bphone | 16 |
| VNG | 84 | Máy tính bảng | 7 |

"FPT" (6) và "Viettel" (9,5) nhiều khả năng là trang định hướng, không phải bài chính về công ty: **chưa đo đúng**.

Chưa có bài trên vi.wikipedia (không đo được, cũng là dấu hiệu ít nội dung tiếng Việt): *AlphaGo*, *Demis Hassabis*,
prompt engineering, tác tử AI, hệ thống khuyến nghị. **Diễn giải (chưa chắc):** Edison, động cơ hơi nước, máy bay có thể
bị kéo bởi mùa học (năm học bắt đầu 5/9); Wikipedia đo nhu cầu *đọc*, không phải nhu cầu *xem*; chỉ dùng để so tương đối.

## 3. Danh sách đề tài

Định dạng: **Tựa làm việc** — hook một câu — vì sao bây giờ / bằng chứng — rủi ro sai hoặc lỗi thời.

### 3.1 "AI giải thích" (~40 giây, một khái niệm)

1. **ChatGPT thật ra chỉ đang đoán chữ tiếp theo?** — "Mỗi câu AI viết là hàng trăm lần đoán liên tiếp." — ChatGPT
   412/ngày; 3Blue1Brown dùng đúng ví dụ "kịch bản bị thiếu" [29] — Thấp; nhớ nói "đoán" là đơn giản hoá.
2. **Vì sao AI bịa mà vẫn rất tự tin? (ảo giác AI)** — "AI không biết là nó không biết." — EBU/BBC 45% câu trả lời có
   lỗi đáng kể [22] — Thấp; đừng nêu tỉ lệ lỗi chung cho "mọi AI".
3. **Token: vì sao AI đếm chữ cái sai?** — "AI không đọc chữ như bạn, nó đọc từng mẩu." — khái niệm nền, ít nội dung Việt —
   **Trung bình:** mô hình mới có thể đã sửa ví dụ đếm chữ; quay demo ngay trước khi đăng.
4. **Deepfake là gì, vì sao giọng mẹ bạn có thể bị giả?** — "Kẻ gian chỉ cần một đoạn giọng nói ngắn của bạn." —
   cảnh báo công an [6][7] — Thấp; không nêu "cần đúng X giây" nếu không có nguồn.
5. **AI có học từ cuộc trò chuyện của bạn không?** — "Huấn luyện và trò chuyện là hai chuyện khác nhau." — lời khuyên
   không nhập dữ liệu nhạy cảm [27] — **Trung bình:** cài đặt bộ nhớ/quyền riêng tư khác nhau theo app và đổi thường xuyên.
6. **Thuật toán đề xuất: vì sao TikTok biết bạn thích gì?** — "Bạn chưa nói gì, nhưng bạn đã dừng lại 3 giây." — TikTok
   257/ngày, YouTube 705/ngày; chưa có bài vi.wiki về hệ thống khuyến nghị — Thấp; không khẳng định chi tiết thuật toán
   nội bộ của một hãng.
7. **GPU: con chip làm Nvidia thành "ông lớn AI"** — "Chip chơi game hoá ra lại hợp để dạy AI." — Jensen Huang 121/ngày,
   GPU chỉ 6/ngày (người biết người, chưa biết khái niệm) — Thấp nếu tránh giá cổ phiếu/vốn hoá.
8. **AI có hiểu tiếng Việt không?** — "9 trên 10 câu lệnh Gemini ở Việt Nam gõ bằng tiếng Việt." [2] — **Trung bình:**
   chất lượng tiếng Việt thay đổi theo phiên bản; nói về nguyên lý (dữ liệu huấn luyện), không xếp hạng app.
9. **Mạng nơ-ron có giống não người không?** — "Gọi là nơ-ron, nhưng nó giống bảng tính hơn bộ não." — "Học sâu"/"Mạng
   thần kinh nhân tạo" đang theo dõi — Thấp.
10. **Tác tử AI (AI agent) khác chatbot thế nào?** — "Chatbot trả lời; tác tử thì tự đi làm việc." — 44% người được khảo
    sát doanh nghiệp đã thử AI agent (3HORIZONS/CIO Vietnam) [30]; chưa có bài vi.wiki — **Trung bình–cao:** tên sản phẩm
    agent đổi nhanh, chỉ giải thích khái niệm.
11. **"Hình mờ vô hình" trong ảnh AI là gì?** — "Một số ảnh AI mang dấu mà mắt bạn không thấy." — Luật AI 1/3/2026, NĐ 142
    [15][16]; Gemini kiểm tra SynthID [31] — **Trung bình:** SynthID chỉ áp dụng cho nội dung tạo bằng công cụ Google;
    không hứa "phát hiện được mọi ảnh AI".
12. **Phép thử Turing: máy đã qua mặt con người chưa?** — "Năm 1950, Turing hỏi: máy có thể giả làm người không?" — 19/ngày,
    "Alan Turing" đang theo dõi — Thấp; cẩn thận các tuyên bố "AI đã vượt Turing test" (tuỳ cách thử).
13. **Vì sao AI đôi khi tính sai phép tính dễ?** — "Máy tính bỏ túi không sai, nhưng chatbot thì có thể." — VTV nêu ví dụ AI
    tính sai [21] — **Cao:** mô hình mới dùng công cụ tính; phải demo lại ngay trước khi đăng, hoặc nói ở thì quá khứ.
14. **"Trí tuệ nhân tạo" được đặt tên năm 1956 như thế nào?** — "Một hội thảo mùa hè đặt tên cho cả một ngành." — 70 năm
    hội thảo Dartmouth [32] — Thấp; cầu nối sang dòng B.
15. **AI "dự đoán" thời tiết, kẹt xe ra sao?** — "Bạn dùng AI mỗi ngày mà không biết." — gợi ý mở rộng ra ngoài chatbot —
    **Trung bình:** cần ví dụ có nguồn cụ thể (Google Maps 13,5/ngày).

### 3.2 "Mẹo AI 30 giây" (một mẹo dùng được ngay)

1. **Bảo AI hỏi lại bạn trước khi trả lời** — "Thêm một câu, câu trả lời sát gấp đôi." (không nêu "gấp đôi" như số đo)
   — lời khuyên đặt câu hỏi cụ thể [27] — Thấp.
2. **Công thức 3 phần: vai trò – việc – định dạng** — "Đừng hỏi 'viết giúp tôi', hãy nói rõ ba thứ." — Tinhte/báo hướng
   dẫn người mới [26][27] — Thấp.
3. **Bắt AI ghi nguồn rồi tự bấm kiểm tra** — "AI có thể bịa cả đường link." — EBU/BBC [22] — Thấp.
4. **5 thứ không bao giờ dán vào chatbot** — "Số tài khoản, CCCD, mật khẩu…" — khuyến cáo báo chí, công an [20][27] —
   Thấp.
5. **Nghi cuộc gọi deepfake? Cúp máy, gọi lại số quen** — "Mắt và tai có thể bị lừa, số điện thoại thì khó hơn." — [6][7]
   — Thấp; tránh hướng dẫn "nhìn mắt nhấp nháy" (dễ lỗi thời).
6. **Dùng AI học mà không "mất não": xin gợi ý, đừng xin đáp án** — "Bảo AI làm thầy, đừng bảo làm hộ." — PISA 95,9% [5],
   VTV [21], 12 tiết AI [8] — Thấp; hợp phụ huynh.
7. **Nhờ AI lập lịch ôn thi theo tuần** — "Cho AI ngày thi, nó chia việc cho từng tối." — 160.000 học sinh dùng Gemini
   Canvas ôn thi/tháng [3] — Thấp.
8. **Chụp ảnh để dịch thực đơn, biển báo, hướng dẫn sử dụng** — "Camera điện thoại thành phiên dịch viên." — dịch tài liệu là
   công dụng đang tăng [2] — **Trung bình:** giao diện tính năng đổi; quay màn hình mới.
9. **Viết tin nhắn khó nói: xin 3 giọng điệu** — "Lịch sự, thẳng thắn, hay hài hước — chọn một." — tiết kiệm thời gian là lý
   do số 1 [1] — Thấp.
10. **Bảo AI phản biện ý tưởng của bạn** — "Đừng hỏi AI 'hay không', hãy hỏi 'sai ở đâu'." — 89% người dùng AI ở VN coi kết
    quả AI là điểm xuất phát để nghĩ tiếp [18] — Thấp.
11. **Nói chuyện với AI bằng giọng tiếng Việt** — "Không cần gõ, cứ nói." — hướng dẫn giọng nói tiếng Việt [33] —
    **Trung bình:** tính năng/miễn phí thay đổi theo app.
12. **Tóm tắt văn bản dài: hỏi "điều gì bất lợi cho tôi?"** — "Đọc 20 trang trong 30 giây — rồi tự đọc lại đoạn quan
    trọng." — **Trung bình:** không thay tư vấn pháp lý; phải nói rõ.
13. **Nhận diện ảnh AI: xem chữ, tay, nhãn** — "Ba chỗ AI hay để lộ." — hướng dẫn báo chí [31][34] — **Cao:** dấu hiệu
    bằng mắt đang mất dần khi AI tốt lên; nhấn mạnh kiểm tra nguồn hơn soi ảnh.
14. **Mua tài khoản AI "giá rẻ" có rủi ro gì?** — "Rẻ 10 lần, nhưng ai đang đọc cuộc trò chuyện của bạn?" — Voz bàn mua
    qua bên thứ ba/bot Telegram [25] — **Trung bình:** không nêu tên người bán; nói chung về rủi ro tài khoản dùng chung.
15. **So sánh điện thoại bằng AI: đưa tiêu chí trước** — "Hỏi 'máy nào tốt' là hỏi sai." — ví dụ trong hướng dẫn [26][27] —
    Thấp; không để AI nêu giá cụ thể.

### 3.3 "Công nghệ đã thay đổi thế giới" (câu chuyện một phát minh)

1. **Mã QR: sinh ra cho nhà máy ô tô, thành ví tiền người Việt** — "Ô vuông này được nghĩ ra để đếm linh kiện." — Mã QR
   179/ngày; Denso Wave 1994 [35] — Thấp.
2. **Edison không phát minh ra bóng đèn đầu tiên** — "Bóng đèn có trước Edison; ông làm ra cái bán được." — Edison
   200/ngày, Đèn sợi đốt 22 [36] — Thấp nếu nói đúng sắc thái (cải tiến, thương mại hoá).
3. **Tesla và Edison: cuộc chiến dòng điện** — "Ổ điện nhà bạn là kết quả của một cuộc chiến." — Tesla 126/ngày [37] —
   **Trung bình:** nhiều huyền thoại mạng về Tesla; chỉ dùng chi tiết có nguồn.
4. **Google mua YouTube: 20 năm (9/10/2006)** — "Một trang video chưa đầy 2 năm tuổi được bán 1,65 tỉ USD." — YouTube 705/ngày;
   mốc tròn trong tuần này [9] — Thấp (số liệu thương vụ đã công bố); **đăng trước/đúng 9/10**.
5. **Tin nhắn đầu tiên của Internet chỉ có 2 chữ: "LO"** — "Máy sập khi đang gõ chữ thứ ba." — ARPANET 29/10/1969 [38] —
   Thấp.
6. **iPod 25 tuổi: "1.000 bài hát trong túi"** — "Trước iPhone là chiếc máy nghe nhạc này." — 23/10/2001 [39]; "Steve Jobs
   và iPhone" đang theo dõi — Thấp.
7. **150 năm chiếc điện thoại (Bell, 1876)** — "Cuộc gọi đầu tiên là lời gọi trợ lý sang phòng bên." — Bell 39/ngày [40] —
   **Trung bình:** tranh cãi Meucci/Gray; nên nhắc ngắn.
8. **100 năm truyền hình (Baird, 1926)** — "TV đầu tiên chiếu hình mờ bằng đĩa quay." — Truyền hình 25/ngày [41] —
   **Trung bình:** phân biệt TV cơ (Baird) và TV điện tử (Farnsworth, Zworykin).
9. **GPS: hệ thống quân sự mở cho dân sau một thảm kịch** — "Bản đồ trên điện thoại bạn từng là bí mật quân sự." — GPS
   34/ngày; sau vụ KAL 007 (1983) [42] — **Trung bình:** nhiều mốc (1983 công bố, 2000 bỏ nhiễu chủ ý), nói đúng thứ tự.
10. **Transistor: linh kiện nhỏ làm ra thế giới số** — "Điện thoại bạn có hàng tỉ cái công tắc này." — 22/ngày; Bell Labs
    1947 [43] — Thấp; số transistor trong chip cụ thể nên lấy từ nguồn hãng.
11. **Pin Li-ion: viên pin trong túi bạn từng đoạt Nobel** — "Không có nó thì không có điện thoại, xe điện." — 18/ngày;
    Nobel Hoá 2019 [44] — Thấp; hợp tuần Nobel.
12. **Flappy Bird: trò chơi Việt làm cả thế giới phát cuồng** — "Một người Việt, vài ngày lập trình, cả thế giới chơi." —
    Flappy Bird 30/ngày, Nguyễn Hà Đông 29/ngày [45] — **Trung bình:** người thật còn sống, kín tiếng; chỉ dùng thông tin
    đã công bố, không đoán thu nhập/đời tư; kiểm "vài ngày" theo nguồn.
13. **Máy hơi nước: James Watt không phải người phát minh** — "Watt cải tiến; cỗ máy đã có từ trước." — 59/ngày [46] —
    Thấp.
14. **Anh em nhà Wright và 12 giây bay đầu tiên** — "Chuyến bay đầu tiên ngắn hơn một chiếc Short." — 27/ngày [47] — Thấp.
15. **Khi nghiên cứu AI giành giải Nobel (2024)** — "Hai giải Nobel năm 2024 dành cho nền tảng của AI." — tuần Nobel 2026
    đang diễn ra [10]; Hinton 8/ngày — Thấp với 2024; **không** nói về Nobel 2026 trước khi có kết quả chính thức.

## 4. Bài học hình thức

- **Hook trong ~1 giây đầu.** Jenny Hoyos (trò chuyện với trưởng sản phẩm Shorts Todd Sherman trên YouTube Blog): có khoảng
  một giây để giữ người xem; công thức "gây bất ngờ – tò mò – thoả mãn" [48]. Kênh MIM đã thấy điều này: Short Hai Bà
  Trưng có giữ chân đầu video >100% (phân tích 05/10).
- **Mở bằng cảnh, không bằng logo/tên kênh.** Hướng dẫn YouTube ví như phim truyền hình: cảnh hay trước, credit sau
  (dẫn lại qua bài tổng hợp, **chưa đọc bản gốc**) [49].
- **Một ý cho mỗi video, mở bằng ví dụ cụ thể.** 3Blue1Brown giải thích LLM bằng cảnh "kịch bản phim bị thiếu câu trả lời
  của AI" rồi mới đến cơ chế [29]. Áp dụng: *AI giải thích* mở bằng tình huống đời thường (cuộc gọi lạ, ảnh TikTok), không
  mở bằng định nghĩa.
- **Đơn giản nhưng có nguồn.** Kurzgesagt viết đi viết lại kịch bản để cân bằng dễ hiểu và chính xác, và làm "source sheet"
  cho mỗi video [50][51]. Với MIM: mỗi Short có 1–3 nguồn ghi ở mô tả — vừa chống sai, vừa là "giá trị nguyên bản" trước
  chính sách inauthentic content.
- **Độ dài:** Short được tới 3 phút từ 15/10/2024 [52], nhưng với một khái niệm, 30–45 giây là đủ; các blog marketing hay
  nói 15–45 giây tối ưu, **không có số liệu kiểm chứng** [53]. Giữ kế hoạch ~40 giây và để vòng phản hồi quyết.
- **Phụ đề cứng ngay khung đầu.** Nhiều người lướt Shorts tắt tiếng (con số 60–80% chỉ là "benchmark ngành" trong bài
  blog, **chưa kiểm chứng**) [49].
- **Tựa:** câu hỏi đời thường hoặc phản trực giác ("Edison không phát minh ra bóng đèn", "AI có học từ bạn không?"), dùng
  từ người xem tự gõ (ChatGPT, TikTok, QR) thay thuật ngữ. Thumbnail ít quan trọng với Shorts vì phần lớn lượt xem đến từ
  feed [48].
- **Chuỗi:** YouTube vừa ra "Shorts series" (xếp Short thành mùa/tập) nhưng **chỉ cho kênh trong YPP** [54] — chưa dùng được
  cho MIM; vẫn nên đặt tên dòng nhất quán để sau này gom.

## 5. Rủi ro & lưu ý

**Độ chính xác**
- *Tên mô hình, giá, gói cước, xếp hạng benchmark:* đổi theo tuần (GPT-6 Astra 9/2026, Sol/Luna 22/9, Sora API dừng 24/9)
  [11][12]. Không đưa vào Short evergreen; nếu bắt buộc, ghi "tại thời điểm tháng X/2026".
- *Sự kiện "nóng" chưa kiểm chứng:* tóm tắt Wikipedia "2026 in AI" có các tuyên bố lớn (AI giải bài toán Thiên niên kỷ,
  agent tự tấn công hệ thống) [55] — **không dùng** nếu chưa có nguồn gốc chính thức.
- *Huyền thoại lịch sử công nghệ:* "640K là đủ" không có bằng chứng Bill Gates nói [56]; Hedy Lamarr "phát minh Wi-Fi" là
  phóng đại (nhảy tần có trước, Wi-Fi hiện đại không dùng nhảy tần) [57]; Edison/bóng đèn, Watt/máy hơi nước. Kịch bản do AI
  viết rất dễ lặp lại các huyền thoại này: **kiểm từng con số, ngày tháng, câu trích**.
- *Số liệu khảo sát:* mỗi khảo sát định nghĩa "dùng AI" khác nhau (78%, 27,9%, 95,9%, 39%…); luôn nêu nguồn + đối tượng.
- *Ví dụ "AI sai" (đếm chữ, tính toán):* có thể đã được sửa ở bản mới — quay demo trong vòng vài ngày trước khi đăng.

**Chính sách YouTube**
- Khai báo nội dung tổng hợp/chỉnh sửa: bắt buộc khi *thực tế* và dễ nhầm là thật (người thật nói/làm điều không có, sự
  kiện thật bị sửa, cảnh thật dựng giả); **không** bắt buộc với kịch bản/infographic hỗ trợ bằng AI, hoạt hình, nội dung
  rõ ràng phi thực tế [13]. Short dựng motion graphics + giọng đọc có kịch bản thường không cần khai; dựng "ảnh tư liệu" AI
  giống thật về Edison, Bell, cảnh lịch sử → **nên bật khai báo**.
- *Inauthentic content* (đổi tên từ "repetitious" 7/2025): nội dung "sản xuất hàng loạt", theo khuôn, không thêm giá trị
  thì không được kiếm tiền; YouTube xét theo chủ đề chính, video nhiều view, video mới nhất [14][58]. 21 Short/tuần cùng
  khuôn là rủi ro thật: mỗi video cần góc nhìn/ví dụ riêng, nguồn riêng, không chỉ đổi chữ.

**Pháp luật Việt Nam**
- Luật Trí tuệ nhân tạo (134/2025/QH15) hiệu lực 1/3/2026 [15]; Nghị định 142/2026 (từ 1/5/2026): tổ chức, cá nhân dùng AI
  trong hoạt động nghề nghiệp/thương mại phải gắn nhãn dễ nhận biết cho âm thanh/hình/video AI **mô phỏng người thật** hoặc
  **tái hiện sự kiện thật**; có thể đặt nhãn trong tựa, mô tả, phụ đề [16][59]. **(Chưa chắc)** kênh chưa kiếm tiền có thuộc
  diện "nghề nghiệp/thương mại" không — an toàn nhất là gắn nhãn mọi hình AI giống thật.
- Không dùng giọng AI nhái người nổi tiếng/người thật.

**Đề tài nhạy cảm nên tránh**
- Chính trị, lãnh đạo, chủ quyền, tôn giáo; deepfake của người thật (kể cả để "minh hoạ" lừa đảo — dùng nhân vật hư cấu).
- Lời khuyên y tế, pháp lý, tài chính/đầu tư bằng AI; khuyên mua bán tiền mã hoá.
- Chỉ đích danh app/người bán là lừa đảo khi không có kết luận của cơ quan chức năng.
- Hướng dẫn "lách" (vượt kiểm duyệt AI, gian lận thi cử, tài khoản lậu).
- Nhân vật còn sống (Nguyễn Hà Đông, Jensen Huang…): chỉ thông tin đã công bố, không đoán đời tư/tài sản.

## 6. Nguồn

1. https://vneconomy.vn/techconnect/decision-lab78-cu-dan-mang-viet-nam-da-su-dung-ai.htm
2. https://vnexpress.net/nguoi-viet-danh-700-trieu-gio-cho-ung-dung-ai-trong-nua-nam-5104333.html
3. https://vietnamnet.vn/viet-nam-bo-xa-nhieu-nuoc-dong-nam-a-ve-ty-le-nguoi-lao-dong-su-dung-ai-2559704.html
4. https://vietnamnet.vn/61-nguoi-viet-lo-mat-viec-hoac-khong-tim-duoc-viec-lam-do-ai-2468590.html
5. https://thanhnien.vn/gan-96-hoc-sinh-viet-dung-ai-ty-le-cao-nhat-the-gioi-185260910183700006.htm
6. https://vneconomy.vn/canh-bao-hien-tuong-dung-ai-gia-mao-hinh-anh-giong-noi-de-lua-tien.htm
7. https://doanhnhan.baophapluat.vn/cong-an-ha-noi-canh-bao-nguoi-dan-canh-giac-truoc-25-kich-ban-lua-dao-tren-khong-gian-mang-nam-2026-7cc6172e.html
8. https://giaoducthudo.giaoducthoidai.vn/trien-khai-dai-tra-noi-dung-giao-duc-ai-tu-nam-hoc-2026-2027-220207.html
9. https://en.wikipedia.org/wiki/History_of_YouTube
10. https://www.nobelprize.org/prizes/about/prize-announcement-dates/ ; https://en.wikipedia.org/wiki/2024_Nobel_Prizes
11. https://en.wikipedia.org/wiki/GPT-6 ; https://www.kucoin.com/news/flash/openai-launches-gpt-6-sol-and-luna-cuts-api-prices-by-50
12. https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation
13. https://support.google.com/youtube/answer/14328491
14. https://support.google.com/youtube/answer/1311392
15. https://mst.gov.vn/ai-la-cong-cu-ho-tro-quyet-dinh-cuoi-cung-van-la-con-nguoi-19726030111172663.htm ; https://baochinhphu.vn/viet-nam-chinh-thuc-co-luat-tri-tue-nhan-tao-ai-102251210164948585.htm
16. https://luatvietnam.vn/tin-van-ban-moi/2-truong-hop-noi-dung-do-ai-tao-ra-bat-buoc-phai-gan-nhan-tu-01-5-2026-186-108836-article.html
17. https://advertisingvietnam.com/article/thi-truong-ai-tieu-dung-viet-nam-2025-voi-78-dan-so-truc-tuyen-da-dung-ai-nguoi-viet-chon-nen-tang-nao-cho-tung-tac-vu-p26978
18. https://news.microsoft.com/source/asia/2026/06/24/bao-cao-chi-so-xu-huong-cong-viec-nam-2026-luc-luong-lao-dong-viet-nam-da-san-sang-cho-ky-nguyen-ai-doanh-nghiep-can-chuyen-minh-de-but-pha/?lang=vi
19. https://dantri.com.vn/khoa-hoc/nghien-cuu-moi-he-lo-su-that-ve-nguy-co-ai-cuop-viec-nguoi-tre-20260927215616843.htm
20. https://doisongphapluat.com.vn/cong-an-canh-bao-nguy-co-lo-lot-du-lieu-ca-nhan-tu-trao-luu-tao-anh-bang-ai-thap-nien-80-a734573.html
21. https://vtv.vn/hoc-sinh-lam-dung-ai-khi-cong-cu-ho-tro-lam-suy-giam-tu-duy-100261003225835725.htm
22. https://www.cdpinstitute.org/news/ai-assistants-rife-with-errors-ebu-and-bbc/
23. https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/emerging-uses-ai-chatbots-news-and-what-it-means-journalism
24. https://voz.vn/t/phan-van-giua-gemini-advanced-va-chatgpt-plus.1099251/
25. https://voz.vn/t/hoi-ve-cac-goi-cuoc-ai-cua-chatgpt-gemini.1241024/
26. https://tinhte.vn/thread/cach-su-dung-chatgpt-tu-a-z-cho-nguoi-moi-bat-dau.4041575/
27. https://cafef.vn/loi-khuyen-cho-tat-ca-nhung-ai-hay-dung-chatgpt-tim-kiem-thong-tin-188260525105214147.chn
28. https://vnexpress.net/vnexpress-khao-sat-thoi-quen-dung-ai-cua-doc-gia-5125402.html
29. https://www.3blue1brown.com/lessons/mini-llm
30. https://cafebiz.vn/cio-summit-2026-ai-da-giup-nhan-vien-lam-nhanh-hon-vi-sao-doanh-nghiep-van-kho-bien-thanh-doanh-thu-17626100214482298.chn
31. https://quantrimang.com/meta-cong-cu-dong-dau-nhan-dang-video-do-ai-tao-206562
32. https://en.wikipedia.org/wiki/Dartmouth_workshop
33. https://tuoitre.vn/plo/ky-nguyen-so/cach-su-dung-chatgpt-bang-giong-noi-tieng-viet-post719709.html
34. https://thanhnien.vn/nhan-dien-noi-dung-do-ai-tao-ra-bang-cach-nao-1852511141436386.htm
35. https://vi.wikipedia.org/wiki/Mã_QR
36. https://vi.wikipedia.org/wiki/Thomas_Edison ; https://en.wikipedia.org/wiki/Incandescent_light_bulb
37. https://en.wikipedia.org/wiki/War_of_the_currents
38. https://en.wikipedia.org/wiki/ARPANET
39. https://en.wikipedia.org/wiki/IPod
40. https://en.wikipedia.org/wiki/Invention_of_the_telephone
41. https://en.wikipedia.org/wiki/John_Logie_Baird
42. https://en.wikipedia.org/wiki/Global_Positioning_System
43. https://en.wikipedia.org/wiki/Transistor
44. https://www.nobelprize.org/prizes/chemistry/2019/summary/
45. https://vi.wikipedia.org/wiki/Flappy_Bird
46. https://en.wikipedia.org/wiki/Watt_steam_engine
47. https://en.wikipedia.org/wiki/Wright_Flyer
48. https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/
49. https://www.teleprompter.com/blog/how-to-go-viral-on-youtube-shorts
50. https://kurzgesagt.org/what-we-do?visit=videos
51. https://10.studio/the-incredible-amount-of-work-behind-kurzgesagts-beautiful-animated-videos/
52. https://www.socialmediatoday.com/news/youtube-expands-3-minute-shorts-to-all-users/736967/
53. https://ltx.io/blog/short-form-video
54. https://techcrunch.com/2026/09/23/youtubes-new-short-series-feature-brings-episodic-viewing-to-shorts/
55. https://en.wikipedia.org/wiki/2026_in_artificial_intelligence
56. https://quoteinvestigator.com/2011/09/08/640k-enough/
57. https://www.americanscientist.org/blog/the-long-view/the-seventh-claim
58. https://www.plagiarismtoday.com/2025/07/08/youtube-targets-inauthentic-content/
59. https://thanhnien.vn/tu-ngay-13-hinh-anh-video-do-ai-tao-ra-phai-gan-nhan-nhan-biet-185260228095842219.htm
60. Wikimedia Pageviews REST API (CC0): https://wikimedia.org/api/rest_v1/ — `per-article/vi.wikipedia/all-access/user/{bài}/daily/20260907/20261004`
