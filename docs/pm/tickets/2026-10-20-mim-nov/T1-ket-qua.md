# T1 — Kết quả chọn 2 chủ đề Long MIM mới (07/12 và 10/12/2026)

Người lập: subagent T1, 20/10/2026. Pha 1: chỉ viết tài liệu, không dựng, không đăng, không sửa `state.sqlite` (chỉ đọc, chế độ `mode=ro`).

## 1. Kết luận

| Chỗ hẹn | Chủ đề chọn | Slug đề xuất | Dài | Điểm |
|---|---|---|---|---|
| T2 07/12 20:00 VN | **Dịch máy: lời hứa "vài năm nữa" lặp lại từ 1954 tới Google Dịch** | `mim-dich-may` | 22–28 phút | 21/25 |
| T5 10/12 20:00 VN | **Mã 1202: chiếc máy tính dẫn đường Apollo kêu báo động lúc hạ cánh Mặt Trăng** | `mim-apollo-1202` | 9–12 phút | 22/25 |

Dự phòng: **GPS** (thay chỗ 9–12 phút, hoặc 20–30 phút nếu bổ sung chương) và **DARPA Grand Challenge và xe tự lái** (thay chỗ 20–30 phút). Chi tiết ở mục 5.

Cả hai chủ đề chọn: không có Long nào trong 17 Long MIM đã hẹn nói về dịch máy hay Apollo; trong 160 Short MIM của `state.sqlite`/`bundles/MIM/` không Short nào về dịch máy, Georgetown, Weaver, Google Dịch, Apollo, AGC hay 1202 (đã quét tự động từ khoá; chỉ có "NASA" xuất hiện ở Long `mim-ai-jobs`, Long `mim-ai-hallucinate` và Short `mim-dorothy-vaughan-fortran` với góc khác: nữ "máy tính" người ở Langley, và câu chuyện phi hành gia kẹt trên trạm vũ trụ).

## 2. Cách đo và hai giới hạn phải nói thẳng

**Nhu cầu** đo bằng Wikimedia Pageviews REST API (vi.wikipedia, `all-access`, `user`, theo ngày). Trung vị lượt xem/ngày của 28 ngày 20/09–17/10/2026 so với cùng kỳ 2025. Gửi User-Agent `yt-factory-research/1.0`. Đây là mức quan tâm để đọc, không phải nhu cầu xem video.

1. **Không có dữ liệu Studio Research.** `data/demand/` chỉ có `MIM.json`; `MIM-studio.md` chưa tồn tại. Tôi không bịa số thay cho nó.
2. **Mọi bài tiếng Việt đều thấp và đều giảm.** Chủ đề tốt nhất chỉ vài chục tới 158 lượt/ngày; hầu hết giảm so với 2025 (có thể do cả mặt bằng đọc Wikipedia giảm, chưa chắc). "Nhu cầu" ở bảng dưới là tín hiệu tương đối, không đủ để dự báo lượt xem.

Ghi chú tên bài: bài vi.wikipedia "Dịch máy" không có dữ liệu (0/ngày, nhiều khả năng bài không tồn tại hoặc là trang chuyển hướng), nên dùng **Google Dịch** làm đại diện cho mối quan tâm; "Xe tự lái" chỉ 2/ngày trong phép đo bài đơn (số 32/ngày trong brief là cộng 2 bài); các bài DARPA Grand Challenge, Waymo, Margaret Hamilton, Máy tính dẫn đường Apollo đều 404 (không có bài tiếng Việt).

## 3. Bảng 12 ứng viên

Điểm 0–5 mỗi cột, tối đa 25: **N** nhu cầu (pageviews vi), **S** độ phủ nguồn sơ cấp mở được, **H** hình/clip dùng được (công cộng/CC, không logo), **M** mới (không trùng Long/Short đã có), **D** đủ chất liệu cho độ dài định đặt.

| # | Ứng viên | Tín hiệu nhu cầu (trung vị/ngày, 2026 so 2025) | N | S | H | M | D | Tổng | Rủi ro chính |
|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| 1 | **Dịch máy → Google Dịch** | Google Dịch 158 (×0,27); bài "Dịch máy" không tồn tại | 4 | 5 | 2 | 5 | 5 | **21** | Thiếu ảnh lịch sử dùng được; Google Dịch giảm mạnh theo năm |
| 2 | **Apollo 11, máy tính dẫn đường và báo động 1202** | Apollo 11 27 (×0,68); Neil Armstrong 42 (×0,89); Apollo 13 4,5 | 3 | 4 | 5 | 5 | 5 | **22** | Câu chuyện đã phổ biến; phần Margaret Hamilton chỉ có nguồn thứ cấp |
| 3 | ARPANET / Internet 1969 | Internet 96 (×0,72); ARPANET 4,5 (×0,60) | 4 | 5 | 4 | 2 | 5 | 20 | **Đã có Short `mim-internet-lo` (hai chữ L, O)**; vi phạm điều "không trùng góc" nếu mở bằng LO |
| 4 | GPS | GPS 26,5 (×0,73) | 3 | 5 | 5 | 5 | 4 | 22 | Không liên quan AI; 20–30 phút phải đủ 6 chương (xem mục 5) |
| 5 | DARPA Grand Challenge và xe tự lái | Tesla, Inc. 28,5 (×0,65); Xe tự lái 2 | 2 | 4 | 3 | 5 | 5 | 19 | Nguồn chính là bản tác giả tự đăng, không phải trang nhà xuất bản; nhắc tên Tesla/Uber |
| 6 | Siri và DARPA CALO | Siri 85,5 (×0,29) | 4 | 2 | 1 | 4 | 3 | 14 | Tư liệu sơ cấp rời rạc; hình gần như toàn bản quyền Apple |
| 7 | PageRank và công cụ tìm kiếm | Larry Page 22,5 (×1,05); PageRank 2 | 2 | 4 | 2 | 4 | 4 | 16 | Cần ảnh giao diện, nhãn hiệu; gần góc `mim-ai-feed` |
| 8 | Transistor và định luật Moore | Transistor 18,5 (×0,49); Định luật Moore 7,5 | 2 | 3 | 4 | 4 | 3 | 16 | Bài Moore 1965 có thể còn bản quyền; xa chủ đề AI |
| 9 | Mã vạch | Mã vạch 15 (×0,24) | 2 | 3 | 3 | 1 | 2 | 11 | **Loại**: trùng Long `mim-ma-qr` và Short `mim-qr-10-ma-vach` |
| 10 | Nobel 2024: Hopfield và Hinton | Geoffrey Hinton 7 | 1 | 4 | 2 | 1 | 3 | 11 | **Loại**: trùng Short `mim-nobel-ngo-cut`, `mim-teaser-hinton-x-quang` |
| 11 | ImageNet, AlexNet | không có bài vi | 1 | 4 | 2 | 1 | 3 | 11 | **Loại**: trùng Short `mim-alexnet-2-card` và Long `mim-ai-gpu` |
| 12 | Mùa đông AI (Dartmouth, perceptron, Lighthill) | không đo | 2 | 5 | 2 | 1 | 5 | 15 | **Loại**: trùng Short `mim-lighthill-1973`, `mim-teaser-perceptron`, `mim-shannon-1951`, `mim-turing-1950-loi-doan` |

Hai Long chọn cũng khác chủ đề game-AI (Deep Blue, AlphaGo, Watson, poker, máy chơi game đã nhiều).

Hai ứng viên điểm 22 (Apollo, GPS) hoà nhau; chọn Apollo vì (a) nhu cầu cao hơn chút (Apollo 11 + Armstrong) và (b) hợp mạch "người và máy": báo động máy tính, con người quyết định có hạ cánh hay không, gần chủ đề AI của kênh hơn GPS.

## 4. Hai chủ đề chọn

### 4.1. Long 20–30 phút (T2, 07/12): Dịch máy

**Góc.** "Vài năm nữa máy sẽ dịch mọi thứ" là lời hứa đầu tiên của ngành này, nói công khai ngày 07/01/1954. Video kể ba lần lời hứa được lặp lại và kết quả của từng lần, rồi chỉ ra chỗ giao nhau với chatbot hôm nay: bài báo Transformer 2017 vốn là một bài về dịch máy. Gợi ý hình thức lộ trình (không dùng "trả lời ba câu hỏi"): mở bằng bảng "sổ lời hứa", mỗi chương mở bằng lời hứa của thời đó rồi đối chiếu kết quả.

**Câu mở có số và ngày (gợi ý cho T2):** ngày 07/01/1954, một cỗ IBM 701 dịch hơn 60 câu tiếng Nga sang tiếng Anh, với 250 từ và 6 quy tắc. Báo chí đưa tin trang nhất; người trong cuộc dự đoán vài năm nữa sẽ có máy dịch mọi ngôn ngữ.

**Dàn ý chương sơ bộ (9 chương, mục tiêu 24–27 phút):**

| # | Chương | Ý chính và số/ngày kiểm chứng được | Nguồn (mục 4.1.1) |
|---|---|---|---|
| 1 | 07/01/1954, buổi trình diễn | IBM 701; Georgetown (Leon Dostert) và IBM (Cuthbert Hurd); 250 từ, 6 quy tắc, khoảng 60 câu; câu mẫu "Mi pyeryedayem mislyi posryedstvom ryechi" → "We transmit thoughts by means of speech"; báo chí đăng; máy "hỏng" 2 lần trong buổi trình diễn (theo New York Herald Tribune) | S2 |
| 2 | Trước đó: dịch như giải mã | 04/03/1947 Weaver viết cho Norbert Wiener; 30/04/1947 Wiener trả lời "rất sớm"; 09/05/1947 Weaver đáp; tháng 7/1949 bản ghi nhớ; ý "bài tiếng Nga thực ra là tiếng Anh bị mã hoá" | S1 |
| 3 | Thập niên 50: tiền đổ vào | Bar-Hillel 1960: năm 1958 riêng Mỹ chi khoảng 1,5 triệu USD cho nghiên cứu liên quan MT (ước tính không chính thức, ông ghi rõ), khoảng 150 người; hội nghị Moscow 05/1958 có 347 người từ 79 viện | S5 |
| 4 | Câu "The box was in the pen" | Bar-Hillel: chữ "pen" trong ngữ cảnh đồ chơi của trẻ nghĩa là cũi chơi, chứ không phải cây bút; kết luận bài: dịch tự động chất lượng cao hoàn toàn "không phải mục tiêu hợp lý" | S5 |
| 5 | 1966: báo cáo ALPAC | Uỷ ban lập 04/1964, chủ tịch John R. Pierce (Bell Labs); 20 triệu USD trong 10 năm; so giá: dịch nội bộ 40 USD, MT hỗ trợ của FTD 36 USD, thuê ngoài 33 USD, JPRS 16 USD cho 1.000 từ Nga; câu "không có triển vọng tức thời hoặc dự đoán được" về máy dịch hữu dụng; nhưng báo cáo đồng thời đề nghị 2,5–3 triệu USD/năm cho ngôn ngữ học tính toán. Hutchins 1996: hậu quả là chấm dứt phần lớn tiền MT ở Mỹ khoảng 20 năm | S3, S4 |
| 6 | Thập niên "im lặng" nhưng vẫn chạy | Météo (Montréal) dịch bản tin thời tiết từ 1976; Systran lắp ở USAF FTD (Dayton) 1970 và Ủy ban Châu Âu mua bản Anh–Pháp 1976; TAUM dừng 1981 vì thất bại với sách hàng không | S9 |
| 7 | 1990: dữ liệu thay luật | IBM (Brown và cộng sự): kho Hansard của quốc hội Canada, khoảng 100 triệu từ, khoảng 3 triệu cặp câu, khoảng 99% cặp đúng; chuyển từ luật viết tay sang xác suất | S6 |
| 8 | 2006 → 2016: Google Dịch | 28/04/2006 công bố thống kê; đầu 2006 ra Trung rồi Ả Rập; lúc đầu 40 giờ và 1.000 máy để dịch 1.000 câu; 2012: 64 ngôn ngữ, mỗi ngày dịch lượng chữ bằng khoảng 1 triệu cuốn sách; 04/2016: hơn 500 triệu người, hơn 100 tỷ từ/ngày, 103 ngôn ngữ; 09/2016: mô hình thần kinh GNMT, báo giảm lỗi 55–85% trên vài cặp, Trung→Anh khoảng 18 triệu bản dịch/ngày | S7, S8 |
| 9 | 2014–2017: từ "chú ý" đến Transformer | Sutskever 2014 (BLEU 34,8 Anh–Pháp), Bahdanau 2014 (cơ chế "chú ý", sửa nút cổ chai vector cố định), Vaswani 2017 (28,4 BLEU Anh–Đức, 41,8 Anh–Pháp, 3,5 ngày trên 8 GPU); nối với chatbot hôm nay, nói rõ đây là một nguồn gốc, không phải "ChatGPT là máy dịch". Khác Short `mim-transformer-2017` ở chỗ: Long kể từ bài toán dịch, Short chỉ kể kiến trúc | S8 |
| 10 | Kết: huyền thoại "rượu mạnh, thịt thối" | Hutchins 1995 bóc các giai thoại "whisky is strong, but the meat is rotten" và "Invisible idiot" là truyền thuyết có từ rất lâu; đối chiếu sổ lời hứa. Chương này có thể rút nếu dư thời lượng | S10 |

Chương 5 và 8 là hai chương dày nhất; nếu thiếu thời lượng, chương 6 mở rộng bằng lịch sử Systran (cần thêm nguồn, xem 4.1.2).

#### 4.1.1. Nguồn đã tự mở kiểm (HTTP và đã đọc nội dung, 20/10/2026)

| ID | Nguồn | URL | Loại | Đã đọc |
|---|---|---|---|---|
| S1 | Warren Weaver, "Translation" (bản ghi nhớ 07/1949, Rockefeller Foundation) | https://mt-archive.net/Weaver-1949.pdf | Sơ cấp (văn bản gốc, bản sao do Rockefeller Foundation Archives cho phép) | Có (thư Wiener 1947) |
| S2 | John Hutchins, bản trình bày "The Georgetown-IBM experiment demonstrated in January 1954" (trích tít báo đương thời) | https://open.unive.it/hitrade/books/HutchinsGeorgetown.pdf | Sơ cấp qua sử gia (trích NYT, Herald Tribune, Newsweek) | Có |
| S3 | ALPAC, *Language and Machines*, NAS-NRC Publication 1416, 1966 | https://mt-archive.net/ALPAC-1966.pdf ; bản NAP: https://nap.nationalacademies.org/catalog/9547 | Sơ cấp (báo cáo gốc) | Có, 32.000 từ |
| S4 | John Hutchins, "ALPAC: the (in)famous report", MT News International 14, 1996 | https://mt-archive.net/90/MTNI-1996-Hutchins.pdf | Thứ cấp của chuyên gia, dùng để hiểu đúng S3 | Có |
| S5 | Yehoshua Bar-Hillel, "The present status of automatic translation of languages", *Advances in Computers* 1, 1960 | https://mt-archive.net/Bar-Hillel-1960.pdf | Sơ cấp | Có |
| S6 | Brown et al. (IBM), "A Statistical Approach to Machine Translation", *Computational Linguistics* 16(2), 06/1990 | https://aclanthology.org/J90-2002.pdf | Sơ cấp | Có |
| S7 | Google, "Breaking down the language barrier—six years in" (04/2012) và "Ten years of Google Translate" (28/04/2016) | https://translate.googleblog.com/2012/04/breaking-down-language-barriersix-years.html ; https://translate.googleblog.com/2016/04/ten-years-of-google-translate.html | Sơ cấp (hãng tự công bố, số liệu tự báo) | Có |
| S8 | arXiv: Sutskever 2014 https://arxiv.org/abs/1409.3215 ; Bahdanau 2014 https://arxiv.org/abs/1409.0473 ; GNMT 09/2016 https://arxiv.org/abs/1609.08144 ; đa ngôn ngữ 11/2016 https://arxiv.org/abs/1611.04558 ; Vaswani 2017 https://arxiv.org/pdf/1706.03762 ; blog Google Research 27/09/2016 https://research.google/blog/a-neural-network-for-machine-translation-at-production-scale/ | Sơ cấp | Có (tóm tắt, bảng 28,4 và 41,8 BLEU, 3,5 ngày) |
| S9 | John Hutchins, "Machine Translation over Fifty Years" | https://open.unive.it/hitrade/books/HutchinsFifty.pdf | Thứ cấp của chuyên gia (Météo, Systran, TAUM) | Có |
| S10 | John Hutchins, "The whisky was invisible, or Persistent myths of MT", MT News International 11, 1995 | https://aclanthology.org/www.mt-archive.info/90/MTNI-1995-Hutchins.pdf | Sơ cấp về lịch sử giai thoại (có trích báo 1963) | Có (đọc các đoạn đầu) |

Tổng: 10 mục, trong đó 7 là sơ cấp theo nghĩa văn bản gốc (S1, S3, S5, S6, S7, S8, và S2 trích báo đương thời qua sử gia), 3 là sử gia dùng để giải thích. Vượt yêu cầu ≥ 6.

#### 4.1.2. Cần kiểm trước khi viết, hoặc còn thiếu

- **Hình ảnh là điểm yếu số 1 của chủ đề này.** Chưa tìm được ảnh Georgetown–IBM 1954 có giấy phép rõ (ảnh báo chí và ảnh IBM thường còn bản quyền). Bản sao Weaver ghi "reproduced by permission of the Rockefeller Foundation Archives": **không chiếu ảnh chụp trang**, chỉ trích ngắn và dựng chữ bằng kiểu chữ của kênh. ALPAC do NAS-NRC xuất bản 1966: chưa xác minh tình trạng bản quyền trang quét, nên chỉ trích chữ. Ảnh chụp giao diện Google Dịch không dùng. T2 phải chạy `motion/long/clip_sheet.py` và tìm trên Wikimedia Commons ảnh IBM 701, Sputnik/Chiến tranh Lạnh (NASA, công cộng) và nhãn từng ảnh. Phần còn lại dựng bằng chữ, sơ đồ tự vẽ (căn chỉnh từ, ma trận "chú ý"), thẻ trích dẫn.
- **Bản ghi trích báo đương thời** (S2): bài NYT 08/01/1954 chưa mở được bản gốc; PDF Chemical and Engineering News 1954 (`mt-archive.net/ChemEngNews-1954.pdf`) không tải được qua `curl`. Mọi câu trích báo phải ghi "theo Hutchins".
- **Giờ ngày chính xác của ALPAC:** thư gửi Seitz đề 20/08/1965; thư chuyển giao đề 27/07/1966; Hutchins ghi xuất bản "tháng 11/1966". Dùng "năm 1966" nếu không xác minh thêm tháng.
- **Số liệu Google (S7) là hãng tự báo cáo**, nói rõ "Google cho biết". Con số "1 triệu cuốn sách mỗi ngày" là ước tính của chính Google.
- **Systran** (chương 6): S9 chỉ cho ngày lắp đặt, thiếu chi tiết kinh doanh; nếu muốn đào sâu cần thêm nguồn.
- **"Vài năm nữa" lời dự đoán 1954:** S2 trích Christian Science Monitor và dự đoán của Dostert; viết "báo đương thời đưa tin rằng IBM và Georgetown kỳ vọng trong vài năm". Không gán câu này cho IBM như lời trực tiếp.
- Bài vi.wikipedia "Dịch máy" không có, nên chưa có từ khoá tiếng Việt làm chuẩn cho tiêu đề; cần xem Studio Research khi có.

### 4.2. Long 9–12 phút (T3, 10/12): Mã 1202

**Góc.** Mã báo động "1202" của máy tính dẫn đường Apollo lúc Eagle hạ cánh, 20/07/1969: máy tính quá tải công việc, tự khởi động lại, vẫn giữ lái động cơ hạ cánh, còn người ở Houston phải quyết định "tiếp tục hay huỷ" trong vài giây. Chủ đề không nói game, không trùng Short/Long nào. Gợi ý hình thức lộ trình: kể theo đồng hồ hạ cánh, mỗi chương mở bằng một con số trên màn hình (DSKY).

**Câu mở (gợi ý):** ngày 20/07/1969, trong lúc hạ cánh xuống Mặt Trăng, cái máy tính mạnh nhất trên tàu kêu báo động năm lần; Houston chỉ có vài giây để quyết định.

**Dàn ý chương sơ bộ (6 chương, mục tiêu 10–11 phút):**

| # | Chương | Ý chính và số/ngày kiểm chứng được | Nguồn (mục 4.2.1) |
|---|---|---|---|
| 1 | 20/07/1969: đèn báo 1202 | Phi hành đoàn không nhận ra mã; Houston: "We're GO on that alarm" (theo bản tóm tắt ALSJ, không chép nguyên văn dài); 60 giây nhiên liệu báo lúc 75 feet, phân tích sau cho thấy còn khoảng 45 giây | A4, A1 |
| 2 | Chiếc máy tính có từ hợp đồng 09/08/1961 | NASA ký với MIT Instrumentation Lab; Milton Trageser quản lý dự án, David Hoag giám đốc kỹ thuật; nhóm Polaris chuyển sang gần như nguyên vẹn; chưa có đặc tả đầy đủ cho tới cuối 1962 | A2 |
| 3 | Bộ nhớ nhỏ xíu | 36.864 từ 15-bit bộ nhớ cố định, 2.048 từ bộ nhớ ghi được (ALSJ); phần mềm chia nhau từng ô nhớ, có ô dùng cho tới 7 việc | A3 |
| 4 | Vì sao "tràn": công việc thừa từ radar hẹn gặp | Công tắc radar hẹn gặp đặt sai tạo việc dư; 7 "core set" (12 từ) và 5 vùng VAC (44 từ); khi hết chỗ sinh mã 1202 (hết core set) hoặc 1201 (hết VAC) | A3, A5 |
| 5 | Máy không bỏ cuộc | Memo Grumman 31/07/1969: 4 lần 1202 và 1 lần 1201 trong giai đoạn hạ cánh; máy khởi động lại, khởi động lại việc quan trọng (lái động cơ, cập nhật màn hình DSKY), không khởi động lại các việc radar sai; MIT đã thử khởi động lại rất nhiều | A5, A3 |
| 6 | Sau Apollo 11 | Apollo 12 cải tiến cảm biến nhiên liệu (ALSJ); Don Eyles viết bản vá Apollo 14 bỏ qua công tắc huỷ lỗi (ALSJ); mã nguồn Comanche055 và Luminary099 do Virtual AGC/MIT Museum số hoá, đăng GitHub, ghi "public domain" | A3, A4, A6 |

Nếu thiếu thời lượng (dưới 9 phút), thêm chương thứ 7 về phiên mô phỏng 1202 ngày cuối trước phóng (hiện chỉ có nguồn thứ cấp, xem 4.2.2).

#### 4.2.1. Nguồn đã tự mở kiểm (20/10/2026)

| ID | Nguồn | URL | Loại | Đã đọc |
|---|---|---|---|---|
| A1 | NASA/ALSJ, "Apollo 11 Lunar Surface Journal: Mission Summary" | https://www.nasa.gov/wp-content/uploads/static/history/alsj/a11/a11.summary.html | Sơ cấp (trang NASA) | Có (đoạn 1202, 60 giây nhiên liệu) |
| A2 | J. E. Tomayko, *Computers in Spaceflight: The NASA Experience* (NASA CR-182505, 1988), chương 2 | https://www.nasa.gov/wp-content/uploads/static/history/computers/Ch2-2.html và https://www.nasa.gov/wp-content/uploads/static/history/computers/Ch2-5.html | Sơ cấp (báo cáo NASA); mục lục: https://www.nasa.gov/wp-content/uploads/static/history/computers/contents.html | Có (hợp đồng 1961; phần cứng) |
| A3 | NASA/ALSJ, "Program Alarms" (bài hồi ký của Peter Adler và Don Eyles; Fred Martin) | https://history.nasa.gov/wp-content/uploads/static/history/alsj/a11/a11.1201-pa.html | Sơ cấp mức hồi ký của người trong cuộc | Có (bộ nhớ, core set, VAC) |
| A4 | Grumman, memo LAV-500-940, 31/07/1969, "Program Alarms in Powered Descent - Apollo 11" | https://www.ibiblio.org/apollo/Documents/Memo-Tillman690731_text.pdf | Sơ cấp (tài liệu nhà thầu, bản quét có OCR) | Có |
| A5 | NASA, "Apollo 11 postflight analysis and mission report" (NASA-SP-238, NTRS 19710015566) | https://ntrs.nasa.gov/citations/19710015566 | Sơ cấp | Chỉ mở trang hồ sơ; **chưa tải PDF** (tên "SP-238" cần kiểm vì tên thường gọi của báo cáo nhiệm vụ là MSC-00171) |
| A6 | Virtual AGC / MIT Museum, mã nguồn AGC (đăng lại ở GitHub, trang khai "public domain", hợp đồng NAS 9-4065) | https://github.com/chrislgarry/Apollo-11 | Sơ cấp (mã nguồn gốc); giấy phép cần kiểm | Có |
| A7 | NASA, Mission Transcripts: bản ghi kỹ thuật không-đối-đất Apollo 11 (626 trang), bản tin PAO (629 trang), bản ghi trên tàu chỉ huy (248 trang) | https://www.nasa.gov/history/mission-transcripts-mercury-gemini-and-apollo/ | Sơ cấp; trang không có tuyên bố bản quyền | Chỉ mở trang liệt kê; PDF trực tiếp (kèm mã `?emrc=`) chưa mở bằng `curl` |

Tổng: 7 mục mở được (A1–A7); 5 mục đã đọc nội dung gốc (A1–A4, A6) và 2 mục mới mở trang hồ sơ (A5, A7). **Cần mở PDF của A5 và A7 trong T3 trước khi cam kết thời điểm giờ-phút hoặc lời thoại.**

#### 4.2.2. Cần kiểm trước khi viết, hoặc còn thiếu

- **Lời thoại và giờ GET**: các nguồn đã đọc chưa cho giờ GET từng báo động. Phải lấy từ A7 (bản ghi kỹ thuật) hoặc A5, rồi tự kiểm. Không dùng bản "corrected transcript" của ALSJ: kết quả tìm kiếm cho biết bản này có bản quyền (chưa tự xác minh); chỉ dùng bản ghi thô của NASA.
- **Steve Bales, Jack Garman, Gene Kranz**: nguồn đọc được chỉ gồm A1 (nêu Bales) và các bài thứ cấp (Wikipedia, báo, Space.com). Vai trò Garman cần nguồn sơ cấp (A7 hoặc phỏng vấn lịch sử truyền miệng của NASA, chưa tìm). Trước khi tìm được, chỉ ghi "Bales khuyến nghị tiếp tục" như A1.
- **Margaret Hamilton**: chỉ tìm được nguồn thứ cấp (Computer History Museum). A3 không nhắc bà. Không nêu công trạng cụ thể của Hamilton (phần mềm "priority displays", Huân chương Tự do 22/11/2016) trước khi có nguồn sơ cấp (hồ sơ Nhà Trắng, bài của chính bà). Nếu không tìm được thì bỏ.
- **J. Halcombe Laning (bộ điều hành bất đồng bộ)**: nguồn đã mở chưa nêu; cần tìm tài liệu MIT/NASA.
- **Giờ hạ cánh UTC**, và số liệu "hiện còn 45 giây thay vì 20": lấy từ A1 (ALSJ nói "20 giây" là con số đọc ra lúc đó, phân tích sau là khoảng 45); ghi rõ là ước tính sau nhiệm vụ.
- **Hình**: ảnh và phim NASA không chịu bản quyền ở Mỹ, nhưng không dùng logo NASA kiểu "NASA bảo trợ"; ảnh Eyles/Hamilton/Bales cá nhân có thể có người chụp riêng, cần đối chiếu từng ảnh. Nhớ rằng chương trình mô phỏng DSKY phải tự dựng, không chép từ phim.
- **Nhu cầu thấp**: Apollo 11 27/ngày (×0,68). Tiêu đề phải có sức hút riêng ("1202" + một con số), không dựa vào từ khoá.

## 5. Hai ứng viên dự phòng

| Dự phòng | Thay chỗ | Điểm | Vì sao chưa chọn | Nguồn đã mở được (chưa đọc kỹ hết) |
|---|---|---|---|---|
| **GPS: từ tiếng bíp của Sputnik tới tắt "nhiễu cố ý" 2000** | 9–12 phút (hoặc 20–30 phút nếu thêm chương) | 22 | Hoà điểm với Apollo; ít liên quan tới AI | Guier & Weiffenbach (JHU APL Technical Digest 18(2)): https://secwww.jhuapl.edu/techdigest/Content/techdigest/pdf/V18-N02/18-02-Guier.pdf ; Tuyên bố Nhà Trắng 01/05/2000 "The United States' Decision to Stop Degrading Global Positioning System Accuracy": https://clintonwhitehouse4.archives.gov/textonly/WH/EOP/OSTP/html/0053_2.html ; trang GPS.gov về Selective Availability: https://archive.gps.gov/systems/gps/modernization/sa/ ; các bản tóm tắt: bản ghi họp báo và bản dữ kiện (`clintonwhitehouse6.archives.gov`, chỉ thấy qua tìm kiếm). Chương sơ bộ: Sputnik (1957) và đo Doppler; Transit (hoạt động 1964, mở cho dân sự 1967, theo bản tin APL 2003); Navstar; chuyến bay KAL 007 (1983) và quyết định mở cho dân sự (**cần nguồn, chưa mở được**); Chiến tranh Vùng Vịnh (**cần nguồn**); 01/05/2000; GPS III 2007 không có SA |
| **DARPA Grand Challenge: năm xe không ai tới đích, rồi Stanley** | 20–30 phút | 19 | Nhu cầu thấp (Xe tự lái 2/ngày); nguồn chính là bản tác giả tự đăng; còn cần hình sạch logo | Thrun et al., "Stanley", *J. Field Robotics* 23(9) 2006: https://pages.cs.wisc.edu/~dyer/cs540/handouts/thrun.stanley05.pdf (bản sao trên trang giảng viên, **không phải trang nhà xuất bản**); hồ sơ CMU RI: https://ri.cmu.edu/publications/stanley-the-robot-that-won-the-darpa-grand-challenge ; NTSB (Uber, Tempe): https://www.ntsb.gov/investigations/AccidentReports/Reports/HAR1905.pdf (**trả về HTML, cần kiểm lại có phải báo cáo**); báo cáo DARPA 2004/2005 chưa mở được (`archive.darpa.mil` lỗi kết nối). Số hiện có: 2005 dài 132 dặm, Stanley xong 6 giờ 53 phút 58 giây (theo bài báo) |

Dự trữ cấp ba nếu cả hai phương án trên hỏng: **ARPANET/Internet 1969** (điểm 20, nhu cầu tốt nhất trong nhóm: Internet 96/ngày). Điều kiện: không mở bằng "L, O" và không lặp góc Short `mim-internet-lo`; nên chọn góc "văn hoá RFC", gói tin và Licklider. Nguồn RFC và RFC editor mở được: https://www.rfc-editor.org/rfc/rfc1 , https://www.rfc-editor.org/rfc/rfc2555 , https://www.rfc-editor.org/rfc/rfc801 (chưa đọc).

## 6. Điểm yếu còn lại (nói thẳng)

1. **Nhu cầu chưa đo được đúng.** Không có Studio Research; Pageviews tiếng Việt đều thấp và giảm; "Dịch máy" không có bài. Điểm nhu cầu của hai chủ đề là suy đoán tương đối. Cần dán Studio Research vào `data/demand/MIM-studio.md` trước khi đặt tiêu đề cuối.
2. **Hình của Long dịch máy.** Chưa có ảnh 1954 xác minh được; bản sao Weaver có hạn chế; ảnh giao diện Google Dịch bị loại. Nguy cơ video thành "nói trên chữ", dễ làm tụt % ở lại. Cần T2 chạy `clip_sheet.py` sớm; nếu cuối cùng không tìm đủ tư liệu hình thì hoán đổi sang GPS (hình NASA, USAF, đài thiên văn đều công cộng).
3. **Chiều sâu Apollo còn mỏng ở người và giờ**: thiếu giờ GET từng báo động, vai Garman/Kranz/Hamilton/Laning chưa có nguồn sơ cấp; hai PDF NASA quan trọng (A5, A7) chưa mở thật. 9–12 phút khả thi với 6 chương, nhưng phải mở hai PDF đó trước khi viết.
4. **Số liệu của Google** (500 triệu người, 100 tỷ từ/ngày, 55–85% giảm lỗi, 18 triệu bản dịch/ngày) là hãng tự báo cáo; phải ghi "theo Google".
5. **Trùng góc một phần**: chương 9 của Long dịch máy chạm Short `mim-transformer-2017` (đã đăng 15/10) và Long `mim-ai-70` có nhắc Transformer một dòng. Đã tách bằng góc "bài toán dịch" nhưng T2 phải đọc lại script `mim-ai-70` (dòng 180) và bundle Short để không lặp câu.
6. **Rủi ro "nội dung theo khuôn"**: Dịch máy kể theo sổ lời hứa và Apollo kể theo đồng hồ, hai hình thức khác nhau; tránh dùng chung bộ khung chương với các Long đã có.
7. **Chưa kiểm cách tính điểm với chủ kênh**: điểm 0–5 là phán đoán của tôi dựa trên dữ liệu ở bảng; Apollo và GPS hoà điểm (22).

## 7. Bàn giao cho T2/T3

- T2 (`mim-dich-may`): bám S1–S10; trước khi viết, tải bản PDF S3 và S5 vào `data/long/mim-dich-may/sources/` (nếu thư mục dùng chung quy ước đó) để trích số trang cho `factcheck.md`. Mỗi con số ghi nguồn và trang.
- T3 (`mim-apollo-1202`): mở PDF A5, A7; ghi giờ GET; bỏ hoặc xác minh mọi phần liên quan Hamilton, Garman, Kranz trước khi vào script.
- Cả hai: không dùng "trả lời ba câu hỏi" mở bài; mở bằng ngày hoặc con số; mọi tuyên bố về Google hoặc NASA phải có nguồn trong factcheck.
