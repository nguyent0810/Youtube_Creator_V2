# T8 v2: 8 Short MIM "AI khuôn mặt" theo truyện có người (Long `mim-ai-khuon-mat` 30/11/2026 20:00)

Người lập: agent T8 v2, 20/10/2026. Pha 1: chỉ viết file. Chưa dựng, chưa TTS, chưa upload, không sửa `state.sqlite`, `data/stier/specs`, ticket khác. Bản đầu (`T8-ke-hoach.md`, `specs-T8/`) giữ nguyên, bị thay bởi bản này nếu được duyệt.
Spec: `docs/pm/tickets/2026-10-20-mim-nov/specs-v2-T8/<slug>.json` (+ `_selfcheck.py`). Chuẩn bài mẫu `MAU-DA-DUYET-mim-nvidia-quan-an-dem.json`: mở bằng năm/sự kiện có người, 30–35 giây, 8–9 cảnh, câu cuối là bước ngoặt kết vòng về câu mở, không "mẹo", không câu hỏi cuối, không nhắc Long trong lời đọc. Link Long trong mô tả: `https://youtu.be/7daMUBWG6mU` (state.sqlite: `long-mim-ai-khuon-mat`, hẹn 2026-11-30T13:00Z = 20:00 VN).

## 1. Lịch (từ `00-LICH-XEN-KE.md`, các dòng "T8 face")

| # | Ngày | Giờ | Slug | Nhân vật + sự kiện có ngày |
|---|---|---|---|---|
| 1 | 23/11 | 11:30 | `mim-face-id-san-khau-2017` | Craig Federighi · 12/09/2017 |
| 2 | 24/11 | 11:30 | `mim-viola-jones-2001-may-tim-mat` | Paul Viola, Michael Jones · 2001 |
| 3 | 25/11 | 11:30 | `mim-nist-2018-bon-nam-20-lan` | Patrick Grother (NIST) · 30/11/2018 |
| 4 | 26/11 | 11:30 | `mim-facenet-2015-mot-tram-hai-muoi-tam-byte` | Schroff, Kalenichenko, Philbin (Google) · 2015 |
| 5 | 27/11 | 19:00 | `mim-robert-williams-2020-theo-aclu` | Robert Williams · 01/2020, thoả thuận 28/06/2024 |
| 6 | 28/11 | 19:00 | `mim-deepface-2014-bon-trieu-khuon-mat` | Yaniv Taigman (Facebook) · 2014 |
| 7 | 30/11 | 17:00 | `mim-joy-buolamwini-mat-na-trang-2018` | Joy Buolamwini, Timnit Gebru · 2018 |
| 8 | 01/12 | 19:00 | `mim-facebook-xoa-mot-ti-mau-khuon-mat-2021` | Jerome Pesenti (Facebook/Meta) · 11/2021 |

Ghi chú: bài 8 rơi SAU Long (01/12) theo lịch gốc; nếu muốn đứng trước Long, đổi chỗ với bài ít phụ thuộc nhất. Bài 4 và 6 cách nhau một ngày vì cùng đề tài "máy nhận mặt gần bằng người" (khác công ty, khác năm). Trong lịch, không bài nào đè Long.

## 2. Tám bài

| # | Câu mở (≤ 9 chữ) | Nhân vật | Sự kiện có ngày | Bước ngoặt (câu cuối) | Số + nguồn (✔ = đã mở bằng WebFetch) |
|---|---|---|---|---|---|
| 1 | "Năm 2017, Face ID từ chối trên sân khấu." | Craig Federighi (Apple) | 12/09/2017, ra mắt iPhone X: máy demo đòi mật mã, đổi máy dự phòng | "Hoá ra lần từ chối ấy là Face ID đang chạy đúng thiết kế." (theo Apple: nhiều người cầm máy trước, Face ID thử mặt lạ rồi đòi mật mã) | dưới 1/1.000.000; sinh đôi/trẻ dưới 13 cao hơn: https://support.apple.com/en-us/102381 ✔ · diễn biến: https://9to5mac.com/2017/09/13/face-id-demo-fail-details/ ✔ |
| 2 | "Năm 2001, hai người dạy máy tìm mặt người." | Paul Viola, Michael Jones | 2001, khung phát hiện mặt | "Hơn hai mươi năm sau, cách làm của hai người vẫn còn chạy ở những máy yếu." | 15 hình/giây, ảnh 384x288, Pentium III 700 MHz; ~2 hình/giây trên iPAQ: https://en.wikipedia.org/wiki/Viola%E2%80%93Jones_object_detection_framework ✔ |
| 3 | "Năm 2014, máy tìm người trượt bốn phần trăm." | Patrick Grother, NIST | 30/11/2018, báo cáo NIST 8238 | "Từ bốn phần trăm xuống không phẩy hai, nhưng chỉ với thuật toán giỏi và ảnh tốt." (Grother: năng lực các hãng chênh rất xa) | 4% (2014) → 0,2% (2018) ≈ 20 lần; 127 thuật toán/39 nhà phát triển; kho 26,6 triệu ảnh: https://www.nist.gov/node/1532616 ✔ |
| 4 | "Năm 2015, Google biến mặt người thành dãy số." | Florian Schroff, Dmitry Kalenichenko, James Philbin | 2015, bài FaceNet | "Mặt người, với máy, chỉ còn là một dãy số, và nó nhận ra người." | 128 byte/khuôn mặt; LFW 99,63%; YouTube Faces 95,12%; giảm sai ~30%: https://arxiv.org/abs/1503.03832 ✔ |
| 5 | "Tháng một 2020, Robert Williams bị bắt trước nhà." | Robert Williams (Detroit) | 01/2020 bị bắt; 28/06/2024 thoả thuận | "Riêng kết quả nhận diện khuôn mặt không còn đủ để bắt người." (theo thoả thuận, ACLU) | 30 giờ; ảnh mờ camera 2018; ảnh bằng lái hết hạn; "ông không phải người trong video" (theo ACLU): https://aclu.org/cases/williams-v-city-of-detroit-face-recognition-false-arrest ✔ |
| 6 | "Năm 2014, Facebook cho máy xem bốn triệu mặt." | Yaniv Taigman và nhóm | 2014 (CVPR), DeepFace | "Bốn triệu khuôn mặt đủ để máy gần bằng người trong bài thử ấy." | 97,35% LFW; ~4 triệu ảnh, >4.000 người; giảm sai >27%; người thật 97,53% (chỉ Wikipedia): https://en.wikipedia.org/wiki/DeepFace ✔ |
| 7 | "Máy chỉ thấy cô khi đeo mặt nạ trắng." | Joy Buolamwini, Timnit Gebru | 2018, Gender Shades | "Chiếc mặt nạ trắng ấy đã thành một con số đo được." | 34,7% (phụ nữ da sẫm) vs 0,8% (đàn ông da sáng), ba hệ thống, đoán giới tính: https://proceedings.mlr.press/v81/buolamwini18a.html ✔ · mặt nạ: https://en.wikipedia.org/wiki/Joy_Buolamwini ✔ |
| 8 | "Năm 2021, Facebook sắp xoá một tỉ khuôn mặt." | Jerome Pesenti (người viết thông báo) | 11/2021, tắt hệ thống nhận diện | "Hơn một tỉ dãy số khuôn mặt, từ nay, sẽ biến mất khỏi hệ thống ấy." | >1 tỉ mẫu khuôn mặt: https://en.wikipedia.org/wiki/DeepFace ✔ (kèm AP/Engadget chỉ qua tìm kiếm) |

Quy ước: mọi người có thật được nêu bằng "theo ACLU / theo lời Apple / theo lời cô kể / theo hãng"; không kết luận pháp lý, không nêu tên cảnh sát hay thám tử, không dùng ảnh người (clip chỉ là cảnh chung, có nhãn minh hoạ trong mô tả). Con số trong lời đọc viết bằng chữ, chữ số chỉ có ở màn hình, tiêu đề, mô tả; chỉ năm giữ chữ số như bài mẫu.

## 3. Nguồn đã kiểm (20/10/2026, WebFetch/WebSearch)

`data/long/mim-ai-khuon-mat/` KHÔNG có `factcheck.md`. Máy này có mạng chập chờn: một số tên miền (www.aclu.org, www.nist.gov một số trang, tampabay.com, about.fb.com, gendershades.org, wired.com, CVF html) lỗi DNS/403/chặn. Kết quả:
- **Đã mở và khớp:** arXiv 1503.03832 (tác giả, 99,63%, 95,12%, ~30%, 128 byte); PMLR Gender Shades (34,7% / 0,8%, ba hệ thống); Apple support 102381 (dưới 1/1.000.000, sinh đôi/anh chị em/trẻ dưới 13; trang KHÔNG nêu Touch ID 1/50.000: bản T8 cũ phải bỏ so sánh này); ACLU Williams (qua `aclu.org` không `www`); NIST news 30/11/2018 (nist.gov/node/1532616); NIST 12/2019 (nist.gov/node/1603646, dùng cho dự phòng); 9to5mac Federighi; Wikipedia Viola-Jones, DeepFace, Joy Buolamwini, Helen Chan Wolf.
- **Chưa mở được (cần kiểm trước dựng):** NISTIR 8238 PDF (>10 MB; nên tải tay xem câu "ảnh chất lượng tốt" và nguyên nhân mạng nơ-ron); bài báo DeepFace gốc (số người thật 97,53% chỉ có ở Wikipedia); Meta bản gốc about.fb.com (ngày, Pesenti, mô tả lý do, Illinois: chỉ qua tìm kiếm); AP về thoả thuận Williams (điều khoản "không bắt chỉ dựa trên kết quả nhận diện": ACLU chỉ nói "bằng chứng độc lập", lời đọc dùng cách nói của ACLU); Engadget Federighi (trang trống); bài Viola-Jones 2001 gốc; "mặt nạ trắng": Wikipedia ghi cảnh báo có thể có phần chưa kiểm và đoạn này không có chú thích, cần tìm bài MIT Media Lab hoặc TED.

## 4. Tự kiểm

`specs-v2-T8/_selfcheck.py` (import `mix_lint`, `scene_mode` từ `motion/stier/build.py`; KHÔNG chạy `build.py`; không TTS, không ghi gì). Chạy `python -I specs-v2-T8/_selfcheck.py`: **TỔNG LỖI 0 trên 8 spec.**

| Slug | Chữ lời đọc | Ước giờ | Kiểu cảnh | T% | Mở |
|---|---|---|---|---|---|
| face-id-san-khau-2017 | 112 | 32 s | M D M T G G D T M | 16 | 9 |
| viola-jones-2001 | 120 | 34 s | M G G T D D M T | 27 | 9 |
| nist-2018 | 110 | 34 s | M D D G D D T M | 11 | 9 |
| facenet-2015 | 109 | 31 s | M T D G D G T M | 23 | 9 |
| robert-williams-2020 | 108 | 33 s | M G T D D G T M | 21 | 9 |
| deepface-2014 | 107 | 31 s | M D G D G T M | 9 | 9 |
| joy-buolamwini-2018 | 123 | 35 s | M G T D G D T M | 15 | 9 |
| facebook-2021 | 108 | 31 s | M D D G G T M | 10 | 9 |

Đã kiểm: theme mim, mix true, rules 2; đủ M D G; T ≤ 35%; không 3 cảnh liền cùng kiểu; cảnh ≤ 11 s (ước); mốc `[câu,"chữ"]` đều có trong câu; dòng phụ ≤ 52; counter không prefix chữ số; lời đọc không có chữ số ngoài năm; câu cuối không là câu hỏi; không chữ "mẹo". Giờ là ƯỚC LƯỢNG (4 âm tiết/giây), chưa kiểm bằng TTS: bài 5, 7 sát 35 s; NIST có M 39% (clip ở đầu và cuối). Khối `say` (cách đọc tên riêng) chưa nghe thử. Chưa kiểm: lint thật của build.py, bố cục 1080x1920, cảnh `chart` (chỉ bài 3, theme-mim.css có `.chbar`; không dùng `table`).

Clip (12 id từ `motion/hf/assets/clips/index.json`, chỉ đọc tên mô tả, chưa xem hình): 6279825 hành lang, 32259631 bàn làm việc, 17518183 màn hình bàn phím, 5377697 mã trên màn hình, 36392049 bo mạch, 10001617 và 34762047 đường phố, coverr HrWOLrRiqp coding, 8721655 laptop, 36637656 đường đêm sương, 17713400 mưa trên kính xe, 36511035 ảnh cũ trong hộp (ảnh người nhỏ, cần soát), 6120117 kính lúp, 32093831 gương vỡ, 7688618 tay robot trước tivi cũ, 8549582 nước chảy trên kính, 35057102 phố hoàng hôn. Không id nào đã có trong spec hiện có (đã loại). `clip_sheet.py` chỉ chạy cho Long (`ch*.json`), pha 2 phải soát tay 3 khung/clip: không logo, chữ, tên công ty, cận mặt; clip 36511035 (bài 6) thay nếu thấy mặt rõ.

## 5. Bảng đối chiếu trùng

### 5a. Short MIM trong `state.sqlite` (mode=ro): 160 Short MIM, hẹn từ 08/10 đến 12/11/2026 (không có Short MIM nào từ 13/11)
Slug có "mat/face/nhan/quet": `mim-da-nghi-van-mat-600-ty`, `mim-quet-mat-10-trieu`, `mim-lee-sedol-khong-nhan-kem-hon`, `mim-nhan-ma-2005`. Quét từ khoá trên mọi `data/stier/specs/mim-*.json` và `data/long/*/script.md`: Bledsoe, Viola, DeepFace, Federighi, Buolamwini, Grother, Taigman, Detroit, Super Bowl, khuôn mặt, nhận diện, Face ID, sinh trắc, quét mặt.

| Short có sẵn | Nội dung | Bài v2 gần nhất | Không trùng vì |
|---|---|---|---|
| `mim-quet-mat-10-trieu` (26/10) | quy định quét mặt trên 10 triệu, chặn kẻ lạ | 1 (Face ID), 5 | không nhắc ngân hàng, 10 triệu, lừa đảo; bài 1 là sự kiện sân khấu 2017 |
| `mim-lua-dao-1-tren-555` | khảo sát lừa đảo; nhắc xác thực sinh trắc khi chuyển tiền | cả 8 | khác đối tượng (lừa đảo), không có truyện khuôn mặt |
| `mim-captcha-may-gioi-hon-nguoi` | mô hình nhận diện ảnh giải CAPTCHA (ETH Zurich 2024) | 3, 4, 6 | nhận diện ảnh giải CAPTCHA, không phải nhận mặt |
| `mim-meo-deepfake-goi-lai`, `mim-goi-video-vai-giay` | deepfake | 8 | giả mạo, không phải dữ liệu mặt |
| `mim-da-nghi-van-mat-600-ty` | "mất" tiền (không liên quan mặt) | — | chỉ trùng từ "mặt" trong slug |

Không có Short nào về FaceNet, Face ID, NIST, Gender Shades, Williams, DeepFace, Viola-Jones, Meta. Không lặp Nvidia/Denny's/Krizhevsky/AlexNet.

### 5b. Với T4–T9 và T8 cũ
- **T6** (chat/privacy, 8 spec: Google 4.500 chat, ba ngả tin nhắn, chat 5 năm hay 30 ngày, Gemini người đọc, luật dữ liệu 2026, máy chỉ đọc không học, Samsung, ý chặn ChatGPT 2023): không spec nào có khuôn mặt/sinh trắc/Face ID/Facebook. Gần nhất về ý: bài 8 v2 (Facebook xoá dữ liệu mặt, "dữ liệu cá nhân") và `mim-luat-du-lieu-ca-nhan-2026`: khác sự kiện, khác nhân vật, khác nguồn; không nói luật. Lịch T6 và T8 xen kẽ ở 23–25/11 (T8 11:30, T6 19:00 hoặc 17:00), khác ngày giờ, khác chủ đề.
- **T4** (GPU), **T5** (Watson), **T7** (poker: Pluribus có chữ "Facebook AI" là Noam Brown/Sandholm, nhân vật khác), **T9** (game): không từ khoá khuôn mặt/nhận diện. T4–T9 chỉ khác chủ đề với T8; DeepFace là AI ảnh, không đụng GPU (T4 `mim-gpu-*` không nói DeepFace).
- **T8 cũ** (`specs-T8/`, 8 bài khuôn số/cơ chế): bỏ hẳn "ngưỡng nhận mặt", "chớp mắt", "bộ ba ảnh" (cơ chế, không có người), "Face ID một phần triệu" riêng (gộp vào bài 1 làm số phụ), "NIST 20 lần" (giữ, đổi thành truyện Grother), "Williams", "Gender Shades", "128 con số" (giữ góc FaceNet, đổi thành truyện ba tác giả Google). Hai bản không đăng cùng nhau: v2 thay v1.

## 6. Cần kiểm trước khi dựng (theo mức nghiêm trọng)

1. Meta 2021 (bài 8): mở about.fb.com để chắc ngày, Pesenti, ">1 tỉ mẫu", lý do. Nếu không xác nhận được dòng lý do, bỏ board và cards3d (giữ ngày + số + slam).
2. DeepFace người thật 97,53% (bài 6): đối chiếu bài báo CVPR gốc; nếu không khớp, bỏ dòng 4, ô ledger thứ hai và slam.
3. Williams (bài 5): mở AP/ACLU thoả thuận để chắc câu "riêng kết quả nhận diện không còn đủ để bắt". Hiện lời đọc dùng "theo ACLU, bằng chứng độc lập"; câu cuối là suy ra từ thoả thuận (bị cấm bắt chỉ dựa trên kết quả nhận diện, theo AP). Chủ kênh duyệt giọng điệu: slam cuối "KHÔNG CÒN ĐỦ ĐỂ BẮT" có thể đổi thành "CẦN BẰNG CHỨNG KHÁC".
4. Joy Buolamwini (bài 7): đoạn mặt nạ chỉ có Wikipedia (không chú thích); cần bài MIT Media Lab/TED. Nếu không có, mở bằng "Năm 2018, hai nhà nghiên cứu thử ba hệ thống." và bỏ ba dòng đầu.
5. NIST 2018 (bài 3): tải NISTIR 8238 xem điều kiện "ảnh chất lượng tốt"; hiện câu cuối dựa vào biometricupdate.com qua tìm kiếm.
6. Viola-Jones (bài 2): bài báo 2001 gốc cho "15 hình/giây" và "mẫu sáng tối"; "vẫn còn chạy ở máy yếu" theo Wikipedia.
7. Facenet (bài 4): câu "bộ ba ảnh" từ script (triplet loss), đối chiếu mục trong bài báo.
8. Nghe thử khối `say` (Phây-nét, Gu-gồ, Đi-troi, Uy-li-ừm, Bu-lam-guy-ni...).
9. Khung giờ ước chưa đo bằng TTS (bài 5, 7 sát 35 s).

## 7. Dự phòng (đã có nguồn hoặc đã dò)

- **NIST 12/2019 (Patrick Grother, nist.gov/node/1603646 ✔):** 189 thuật toán của 99 nhà phát triển, 18,27 triệu ảnh của 8,49 triệu người; sai nhận nhầm chênh 10 đến 100 lần giữa các nhóm tuỳ thuật toán; một số thuật toán châu Á ít chênh. Nhân vật Grother (trùng bài 3, chỉ dùng nếu bỏ bài 3 hoặc bài 7).
- **Super Bowl XXXV, Tampa, 01/2001:** camera quét mặt khán giả; theo kết quả tìm kiếm, 19 người bị gắn cờ, không ai bị bắt (cần mở Tampa Bay Times/ACLU; chưa mở được; chưa có nhân vật có tên).
- **Woody Bledsoe, Helen Chan Wolf, Charles Bisson (đầu thập niên 1960):** người đánh dấu toạ độ mắt, mũi tay, máy so khớp (Wikipedia Helen Chan Wolf ✔); "40 ảnh/giờ" gắn nhãn citation-needed, nguồn tài trợ CIA theo Wired chưa mở được. Có truyện nhưng thiếu số cứng.
- **Góc BỎ (không có chuyện thật hoặc cấm):** ngưỡng nhận mặt, chớp mắt/kiểm tra người thật, quy định 10 triệu, cách vượt xác thực. Không độn thêm bài; hiện đủ 8 bài, dự phòng chỉ dùng khi một bài ở mục 6 không qua kiểm.

## 8. Đề nghị pha 2

1. Giải quyết mục 6 (1 đến 4) trước; bài nào không qua thì thay bằng dự phòng hoặc bỏ phần có vấn đề.
2. Dựng bài 1 làm mẫu duyệt (Thanh Bình), rồi 7 bài còn lại tuần tự, khoá `output/.render.who`; chạy `clips.py` + soát khung hình tay; không dựng bản nháp.
3. Đăng riêng tư + hẹn giờ theo bảng mục 1; chạy `scripts/shorts_grid.py 2026-11-23 2026-12-01 --channel MIM` kiểm slot trống ngay trước khi đăng.
4. Retro bằng subagent sau khi đăng.
