# T7 v2: Short gắn Long `mim-may-thang-poker` (lên 26/11 20:00), viết lại theo khung truyện có người (bản 1, chờ duyệt)

Người lập: subagent T7 v2, 20/10/2026. PHA 1: chỉ viết file. Không dựng, không render, không upload, không sửa state.sqlite, data/stier/specs hay ticket khác. Spec: `specs-v2-T7/<slug>.json`. Thay bản `T7-ke-hoach.md` + `specs-T7/` (bản cũ theo khuôn số/cơ chế, chủ kênh nhận xét "chưa hấp dẫn").

## 0. Kết luận ngắn

- **Đủ 4 bài, mỗi bài có người thật + sự kiện có ngày + bước ngoặt.** Không độn. Hai góc cũ bị bỏ vì không phải truyện: "sáu người hết bảo đảm" (cơ chế) và Pluribus-Elias dạng "ai thắng ai" (số liệu từng người không có ý nghĩa thống kê; S2 mới kể Elias theo lời ông nói, không theo thắng thua).
- Cả 4 bài kiểm bằng `mix_lint` (import từ `motion/stier/build.py`, không chạy build): không lỗi. Bài dài 115–133 chữ, ước 32–37 giây (cần đo thật khi dựng), 9–10 cảnh.
- Phát hiện ngoài phạm vi: Short cũ `mim-claudico-thua-2015` viết "con người thắng". Nguồn CMU 05/2015: cả nhóm hơn máy 732.713 phỉnh nhưng **hòa về thống kê**, và riêng Jason Les kém máy 80.482. Video đã hẹn giờ, theo memory "không sửa bài đã đăng, chỉ thay khi sai đổi nghĩa": nên PM quyết định có thay không (xem mục 5).

## 1. Lịch (từ `00-LICH-XEN-KE.md`, dòng "T7 poker")

| # | Ngày | Giờ | Slug | Nhân vật | Vì sao đặt ở đây |
|---|---|---|---|---|---|
| S1 | 21/11 (T7) | 11:30 | `mim-polaris-2007-2008` | Phil Laak, Ali Eslami; nhóm Schaeffer | Bài đầu, truyện thắng-thua đảo chiều dễ hiểu nhất, chưa cần biết Long |
| S2 | 24/11 (T3) | 19:00 | `mim-elias-bai-toan-to-bip` | Darren Elias (kỷ lục danh hiệu WPT) | Thay Chris Ferguson theo quyết định chủ kênh 20/10; đã bỏ ý cha con, von Neumann 1944 |
| S3 | 26/11 (T5) | 17:00 | `mim-sandholm-hai-cap-doi-than` | một người đàn ông ở St. Louis, một phụ nữ ở New Hampshire, Sandholm | Ba giờ trước Long 20:00; truyện cảm xúc nhất, kéo người xem sang Long. Đã ẩn danh hai bệnh nhân (20/10) |
| S4 | 29/11 (CN) | 19:00 | `mim-jason-les-ba-co-may` | Jason Les | Sau Long; nhắc Claudico/Libratus/Pluribus nên xem sau khi có Long |

Giờ gợi ý, chốt bằng `scripts/shorts_grid.py` ở pha 2. Mỗi ngày một Short T7, không đè giờ Long. Mô tả mỗi bài đã có dòng "Bản đầy đủ: https://youtu.be/Mz0HwBBSBbg (công khai từ 20:00 ngày 26/11)" (link lấy từ spec cũ, kiểm lại ở pha 2); lời đọc không mời xem Long.

Chuỗi kiểu cảnh (M clip, D số liệu, G sơ đồ, T chữ): S1 `M D G D T M G D M` · S2 `M G G D T M D D M T` · S3 `M G G M G M D D M` · S4 `M D G D M D G T M`. Khác khuôn 12 Short poker cũ (T M G D T G T), và không bài nào giống bài kề.

## 2. Bốn bài

### S1. `mim-polaris-2007-2008` (người thắng máy rồi máy thắng lại)
- **Câu mở (9 chữ):** "Năm hai nghìn lẻ bảy, máy poker thua người."
- **Nhân vật:** Phil Laak và Ali Eslami (hai cao thủ); nhóm Jonathan Schaeffer, Đại học Alberta (Polaris).
- **Sự kiện có ngày:** 23–24/7/2007, Vancouver: bốn phiên, người thắng hai, máy thắng một, một hòa. Tháng 7/2008 (3–6/7), Las Vegas: Polaris bản mới, bốn trận: hòa, người thắng, máy thắng, máy thắng.
- **Bước ngoặt:** cùng thể thức bốn trận, kết quả đảo ngược trong đúng một năm.
- **Câu chốt (vòng về mở):** "Chỉ một năm, ranh giới giữa người và máy poker đã đổi chỗ."
- **Số + nguồn:** 2 thắng/1 thua/1 hòa 2007 và bảng bốn trận 2008: PokerNews 07/2007 (`pokernews.com/news/2007/07/laak-eslami-team-defeats-polaris-...-4136.htm`) và 07/2008 (`.../2008/07/man-machine-ii-poker-championship-polaris-defeats-stoxpoker--5357.htm`); ngày, địa điểm đối chiếu Wikipedia "Polaris (poker bot)". Schaeffer đứng đầu nhóm: PokerNews 2007. Bản mới biết đổi cách chơi theo từng người: PokerNews 2008. Alberta, Polaris 2008: script CH03.
- **Không trùng:** chưa Short nào nhắc Polaris/2007/Laak/Eslami. `mim-cepheus-68-ngay`, `mim-deepstack-11-nguoi` cùng Alberta nhưng là 2015/2017.

### S2. `mim-elias-bai-toan-to-bip` (một kỷ lục gia ngồi giữa năm bản sao, 2019) — THAY BẢN FERGUSON
- **Câu mở (9 chữ):** "Kỷ lục gia poker ngồi giữa năm bản sao."
- **Nhân vật:** Darren Elias (CMU: giữ kỷ lục số danh hiệu World Poker Tour; Meta AI: bốn lần vô địch WPT). Không còn cha con, von Neumann hay Ferguson (bỏ vì tranh cãi Full Tilt của Ferguson). Tên file giữ `bai-toan-to-bip` theo yêu cầu, không còn khớp nội dung; đổi slug được nếu chủ kênh muốn.
- **Sự kiện có ngày:** 2019 (công bố 11/07/2019), thử nghiệm Pluribus với một người và năm bản sao: Elias chơi riêng 5.000 ván. Theo Meta AI, ông kém 4,0 cược lớn/100 ván, sai số 2,2 (cùng nhóm này có Chris Ferguson, Linus Loeliger, lời đọc không nêu).
- **Bước ngoặt:** người giữ kỷ lục sau ván đấu tự nói ra điều làm cỗ máy mạnh (chiến lược hỗn hợp, "phần lớn con người không làm nổi") và rằng nó gặp những người giỏi nhất thế giới, không chỉ tay trung bình (lời Elias, dịch ý).
- **Câu chốt (vòng về mở):** "Kỷ lục gia poker ngồi giữa năm bản sao, và nói ra điều con người khó làm."
- **Số + nguồn (đã mở 20/10):** CMU News 07/2019 (`cmu.edu/news/stories/archives/2019/july/cmu-facebook-ai-beats-poker-pros.html`: kỷ lục WPT, 5.000 ván, năm bản sao, ba câu nói của Elias); Meta AI blog 11/07/2019 (bốn lần vô địch WPT, −4,0 bb/100, sai số 2,2). Hai nguồn đủ cho mọi câu; không còn nguồn UCLA/Wikipedia/Daily Bruin.
- **Không trùng:** như bản cũ, chỉ chung bối cảnh Pluribus với `mim-pluribus-150-do` và `mim-pluribus-khong-doc-vi` (đã quét spec `mim-pluribus-khong-doc-vi` trong data/stier/specs: không có cụm "hỗn hợp"/"ngẫu nhiên"; chủ đề gần nhau, nên nghe lại khi lên lịch).

### S3. `mim-sandholm-hai-cap-doi-than` (hai cặp, ngày 6/12/2010)
- **Câu mở (9 chữ):** "Hai người lạ, hai quả thận, một thuật toán."
- **Nhân vật:** một người đàn ông ở St. Louis, một phụ nữ ở New Hampshire (đúng như thông cáo CMU ghi nơi ở; đã ẩn danh 20/10: không tên, không tên người hiến, không bệnh lý), giáo sư Tuomas Sandholm và nhóm Carnegie Mellon.
- **Sự kiện có ngày:** 27/10/2010 lượt chạy ghép đầu tiên của chương trình thử nghiệm quốc gia OPTN (43 người cần thận, 45 người hiến); 6/12/2010 hai ca mổ: vị hôn thê của người đàn ông hiến cho người phụ nữ, người thân của bà hiến cho ông (mỗi người hiến không hợp với người thân của mình nên đổi chéo).
- **Bước ngoặt:** ghép chéo: mỗi người nhận được quả thận từ người hiến của cặp kia.
- **Câu chốt (vòng về mở):** "Hai người lạ, hai quả thận, một thuật toán nối họ lại."
- **Số + nguồn:** ScienceDaily (CMU) 14/12/2010 (`sciencedaily.com/releases/2010/12/101214111917.htm`: tên, ngày mổ, ai hiến cho ai, 43/45, Sandholm dẫn dắt phát triển thuật toán); 29/11/2010 (`.../2010/11/101116122859.htm`: lượt đầu ghép được bảy người, không dùng trong lời đọc). Sandholm đồng tác giả Libratus/Pluribus: script CH05, CH13, CH17.
- **Không trùng:** chưa Short nào nhắc Sandholm hay ghép thận (đối chiếu từ khoá; "thận" ở captcha/watson là "thận trọng").

### S4. `mim-jason-les-ba-co-may` (một người, ba cỗ máy)
- **Câu mở (9 chữ):** "Một cao thủ poker, ba cỗ máy, bốn năm."
- **Nhân vật:** Jason Les.
- **Sự kiện có ngày:** 2015 Pittsburgh, Claudico: cả nhóm hơn 732.713 phỉnh nhưng hòa thống kê, riêng Les là người duy nhất kém máy (−80.482). 2017 (11–30/01), Libratus: Les thua 880.087 phỉnh, nhiều nhất trong bốn người. 2019, Pluribus công bố (11/07): Les nằm trong nhóm cao thủ đã đấu, nhận xét nó là "quái vật tố bịp".
- **Bước ngoặt:** người duy nhất đứng sau Claudico trở thành người thua nặng nhất trước Libratus, rồi gọi cỗ máy thứ ba là quái vật tố bịp.
- **Câu chốt (vòng về mở):** "Ba cỗ máy, bốn năm, và cả ba lần Les đều ngồi ở phía loài người."
- **Số + nguồn:** CMU News 05/2015 (qua tìm kiếm: Li +529.033, Polk +213.671, Kim +70.491, Les −80.482; hòa thống kê); Wikipedia "Libratus" (Les −880.087, tổng −1.766.250 khớp phép cộng); Meta AI blog 11/07/2019 (danh sách cao thủ có Jason Les; "It is an absolute monster bluffer", dịch ý).
- **Không trùng:** cùng sự kiện với `mim-claudico-thua-2015` và `mim-libratus-120-nghin-van` nhưng khác góc (một người xuyên ba cỗ máy). **Rủi ro trùng cảm nhận trung bình**; đặt sau Long và cách `claudico-thua-2015` (09/11) 20 ngày.

## 3. Bảng đối chiếu trùng

### 3a. Với 12 Short poker MIM đã có (state.sqlite mode=ro, kind='short', channel='MIM': 160 bài; lời đọc từ `data/stier/specs/*.json`)

Quét từ khoá polaris, laak, eslami, ferguson, neumann, sandholm, crowder, jason, les, elias, ghép thận trên slug, tiêu đề và lời đọc của 160 Short: **không bài nào chứa**. Các bài chứa claudico/libratus/pluribus/alberta/poker:

| Short cũ (hẹn) | Góc | S1 Polaris | S2 Elias | S3 Sandholm | S4 Les |
|---|---|---|---|---|---|
| libratus-120-nghin-van (08/11) | 120.000 ván | khác | khác | khác | gần: có nhắc Libratus 2017, góc người |
| poker-10-mu-161 (09/11) | số tình huống | khác | khác | khác | khác |
| hoc-bang-hoi-tiec (09/11) | thuật toán hối tiếc | khác | khác | khác | khác |
| to-bip-bang-toan (09/11) | tố bịp là tần suất | khác | gần nhẹ: cùng chủ đề tố bịp; góc là cha con và 1944 | khác | gần nhẹ: có chữ "tố bịp" ở câu trích |
| va-3-lo-hong-moi-dem (09/11) | vá lỗ hổng | khác | khác | khác | khác |
| claudico-thua-2015 (09/11) | lần 2015 | khác | khác | khác | gần: cùng sự kiện Claudico; góc cá nhân Les |
| chia-bai-doi-xung (10/11) | chống may rủi | khác | khác | khác | khác |
| pluribus-150-do (10/11) | chi phí, thử nghiệm 1 | khác | gần: cùng Pluribus; thử nghiệm 2, người | khác | khác |
| deepstack-11-nguoi (10/11) | DeepStack | khác | khác | khác | khác |
| cepheus-68-ngay (10/11) | Cepheus | khác (cùng Alberta, khác năm) | khác | khác | khác |
| noam-brown-nghi-lau-hon (11/11) | Brown, OpenAI | khác | khác | gần nhẹ: cùng nhóm Sandholm; nội dung khác hẳn | khác |
| pluribus-khong-doc-vi (12/11) | không đọc vị | khác | khác | khác | khác |

### 3b. Với T4–T9 (cũ và v2, `specs-T4`…`specs-T9`, `T8-ke-hoach-v2.md`)
- Quét tên và từ khoá trong mọi spec T4, T5, T6, T8, T9: không bài nào nhắc Polaris, Laak, Eslami, Ferguson, von Neumann, Sandholm, ghép thận, Jason Les. `T8-ke-hoach-v2.md` mục khác ghi T7 là nhân vật khác với T8: khớp.
- T9 `mim-may-choi-game` có dòng nhắc poker ở liên kết: giữ lời đề nghị cũ, T9 không dùng Libratus, Pluribus, Polaris, Sandholm, Ferguson.
- `T1-ket-qua.md` có "Polaris" nhưng là tên tên lửa Polaris (dự án máy tính của MIT), không liên quan Polaris poker. Không xung đột; chỉ cần tiêu đề có chữ "poker" khi nhắc Polaris.
- Clip: không id nào trùng với 7 id của Short poker cũ (28709421, 6259147, 6664998, 8720746, 6962281, 4841217, 6962433), cũng không 6259147/7608623. Đã đổi các clip bàn cờ/máy chữ từng dùng nhiều ở Short Deep Blue/QWERTY. Còn trùng: 12271136 (máy tính cũ) đã dùng ở `mim-daisy-bell-may-hat`; 34677869 dùng ở một Short bud của kênh khác. Chấp nhận, đổi nếu muốn sạch tuyệt đối.

## 4. Cần kiểm trước khi dựng

1. **S2 (Elias), nguồn:** đã mở CMU và Meta AI 20/10. CMU không nêu số danh hiệu nên lời đọc nói "kỷ lục danh hiệu"; "bốn lần" chỉ ở màn hình, theo Meta (đối chiếu số WPT của Elias nếu muốn). Ba câu của Elias là dịch ý, màn hình đã ghi "dịch ý". "Ngồi giữa năm bản sao": mô tả hình ảnh của thử nghiệm một người đấu năm bản sao, đúng nguồn.
2. **S2, số kết quả:** −4,0 cược lớn/100 ván, sai số 2,2 (Meta); lời đọc chỉ nêu số, không kết luận thắng thua có ý nghĩa thống kê cho riêng ông. Meta ghi ông ở nhóm "một người, năm máy"; CMU ghi chung "thắng có ý nghĩa thống kê" ở mức gộp (không dùng). Thời lượng ước 35,0 s (135 chữ): sát trên.
3. **S1, đội người 2008**: PokerNews 07/2008 ghi bảy người, Wikipedia ghi sáu; lời đọc dùng "cả một đội cao thủ" (không nêu số). Kết quả bốn trận tại Gaming Life Expo (3–6/7/2008): hòa, người thắng, máy thắng, máy thắng (PokerNews, bảng quy đổi theo "big blind"); tổng chuỗi gồm hai trận ngoài hội chợ là 3 thắng–2 thua–1 hòa, không dùng. Hòa/thắng tính theo ngưỡng 25 cược nhỏ (2007): "sát nút" là diễn giải, PokerNews 2007 ghi người hơn tổng cộng khoảng 36,5 cược nhỏ.
4. **S3, ba điểm**: (a) "Hai người lạ" là suy ra (hai cặp ở hai bang); thông cáo không nói họ chưa biết nhau, có thể đổi "hai gia đình". (b) ĐÃ ÁP DỤNG 20/10: hai bệnh nhân ẩn danh thành "một người đàn ông ở St. Louis" và "một phụ nữ ở New Hampshire" (lời đọc, cảnh, mô tả, `say`, nguồn; đã mở lại ScienceDaily/CMU 14/12/2010: thông cáo ghi đúng hai nơi này). Còn cụm "vị hôn thê" và "người thân" (nguồn: em/chị dâu), không gọi tên. (c) Giữ giọng trung tính: không nêu kết quả sức khoẻ sau mổ, không hứa hẹn. "cùng nhóm ở Carnegie Mellon viết thuật toán" khớp thông cáo (Sandholm dẫn dắt; thuật toán 2006 của Sandholm, Blum, Abraham; về sau thêm nghiên cứu sinh).
5. **S4**: số Claudico và Libratus lấy qua kết quả tìm kiếm (CMU 05/2015, Wikipedia); chưa mở trang CMU gốc do trình duyệt công cụ lỗi mạng với `cmu.edu` ở lần đọc cuối. Les có tham gia thử nghiệm Pluribus: chỉ từ danh sách trong blog Meta (không biết kết quả riêng của anh, bài không nêu). Câu trích "con quái vật tố bịp" dịch từ "an absolute monster bluffer"; ghi [DỊCH Ý] ở mô tả nếu cần.
6. **Clip** (đã soi khung giữa video của 12 id local, không logo, ticker, chữ đọc được; riêng 12330877 có chữ ASUS nên không dùng): 36641402, 5192033, 6058468 (S1); 36862846, 6948566, 12271136 (S2); 7101003, 34677869, 13335630, 8164796 (S3); 6813640, 11142482, 7478342 (S4). 6813640 (bài tây) chỉ có ở S4. Chạy `clip_sheet.py`/soát 3 khung trước khi dựng; clip mang tính minh hoạ, không phải cảnh thật (mô tả ghi rõ).
7. **Cách đọc `say`:** đã khai báo các tên riêng (Cờ-rít Phơ-gờ-sần, Plu-ri-bớt, Xan-hôm, Tu-ô-mát, Các-nê-ghi Mê-lần, Giây-sần Lét, Ét-la-mi…); nghe thử một lần. Năm đọc dạng "hai nghìn lẻ bảy", "hai nghìn mười chín" (cách nói thường); S3 có "hai nghìn không trăm mười".
8. **Thời lượng thật**: ước 32–37 giây theo 3,9 chữ/giây. S2 (133 chữ) và S3 (134 chữ) sát trên; nếu TTS đọc quá 36 giây, cắt câu cuối của dòng 6 ở S2 hoặc dòng 1 ở S3.

## 5. Dự phòng

- **S2 đã thay Ferguson bằng Elias (20/10).** Dự phòng còn lại: Dong Kim (thua ít nhất trước Libratus, −85.649, từng thắng Claudico), cần bước ngoặt thật.
- **Thay S4** (nếu coi trùng `claudico-thua-2015`): Ứng viên thay: chuyện đêm trận Libratus (Jimmy Chou tin máy đổi chiến thuật riêng cho từng người, nguồn Engadget 10/02/2017, cần đọc lại).
- **Short cũ Claudico**: sai đổi nghĩa "con người thắng" so với "hòa thống kê". Theo memory (thay video đã tải lên chỉ khi sai đổi nghĩa, hỏi trước): đề nghị PM cân nhắc; nếu giữ, S4 đã nói đúng "hòa thống kê" nên hai bài mâu thuẫn nhẹ.
- **Slot trống**: lịch cũ chỉ có 4 slot T7 trong `00-LICH-XEN-KE.md`, đủ 4 bài; không còn slot trống.

## 6. Cách đã tự kiểm spec (không chạy `build.py`)

Dùng script riêng (scratchpad, không đưa vào repo), `from build import mix_lint, scene_mode` rồi mô phỏng mốc thời gian 0,255 s/chữ + nghỉ theo `tts.pauses`:
- mọi neo `[câu, "chữ", lần]` tồn tại trong lời đọc (0 lỗi); lời đọc không có chữ số; câu mở 9 chữ ở cả 4 bài; counter không có `prefix`;
- `mix_lint` trả về rỗng cho cả 4 bài (có M, D, G; chữ thuần T từ 0% đến 20% ước tính, dưới 35%; không 3 cảnh liền cùng kiểu; cảnh dài nhất 5,9 s, dưới 11 s);
- dòng phụ `slam`/`counter`/`chart.unit` ≤ 52 ký tự; mọi chữ `size` ghi tay nằm trong khung 980 px (các `size` quá rộng đã bỏ để engine tự co).
- Chưa kiểm được (chỉ có khi dựng): thời lượng cảnh thật, tương phản, `looks.resolve`, TTS, lỗi hình. Pha 2 chạy `build.py` đầy đủ sẽ bắt.

Chưa ghi gì vào `data/stier/specs`, chưa đụng state.sqlite, chưa chạy build.
