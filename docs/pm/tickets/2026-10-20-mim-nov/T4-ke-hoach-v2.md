# T4 v2 — Short MIM lane `mim-ai-gpu` (Long 16/11): viết lại theo khung truyện

Pha 1, 20/10/2026. Chỉ viết file; chưa dựng, chưa đăng. Thay `T4-ke-hoach.md` + `specs-T4/` (khuôn số/cơ chế, chủ kênh nói "chưa hấp dẫn"). Spec: `specs-v2-T4/<slug>.json` (7 file). Tự kiểm: `specs-v2-T4/_selfcheck.py` (import `mix_lint` từ `motion/stier/build.py`, không chạy build): cả 7 bài OK. Cập nhật 20/10: bài 6 thay bằng `mim-patrascu-card-game-2009` (7 file vẫn đủ).

Khung chung theo bài mẫu đã duyệt `mim-nvidia-quan-an-dem`: câu mở ≤ 9 tiếng, 9–10 cảnh, 33–35 giây, theme mim, mix true, rules 2, lời đọc không chữ số, câu cuối không phải câu hỏi và quay về ý mở. Mỗi bài có người có tên, một sự kiện có ngày, một bước ngoặt.

## 1. Bảng lịch (theo `00-LICH-XEN-KE.md`, dòng "T4 gpu", trừ bài mẫu 13/11 19:00)

| # | Ngày giờ | Slug | Câu mở | Nhân vật | Sự kiện có ngày | Bước ngoặt | Cảnh / thời lượng ước / chuỗi kiểu |
|---|---|---|---|---|---|---|---|
| 1 | 13/11 11:30 | `mim-cuda-canh-bac-2006` | "Ian Buck bắt card chơi game đi làm toán." (9) | Ian Buck, Jensen Huang | 08/11/2006 Nvidia ra mắt CUDA (Buck về Nvidia 2004) | CUDA thêm khoảng nửa chi phí mỗi chip khi biên lãi chỉ khoảng 30%, ăn gần hết lợi nhuận nhiều năm; nhưng CUDA nằm sẵn trong card chơi game ai cũng mua được | 10 cảnh, 35,0 s, MGMDGDMGDM |
| 2 | 14/11 11:30 | `mim-tahoe-44-trieu-hinton` | "Công ty ba người, chưa có sản phẩm nào." (9) | Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever; nhà báo Cade Metz (nguồn) | 12/2012 đấu giá kín bên hồ Tahoe | Giá chạm 44 triệu đô, Hinton dừng và chọn Google, vì nơi hợp nghiên cứu chứ không vì số cao nhất | 10 cảnh, 34,5 s, MDGMDTMGDM |
| 3 | 15/11 11:30 | `mim-nghin-may-chu-con-ba-2013` | "Một nghìn máy chủ để nhìn thấy mèo." (8) | Jeff Dean, Andrew Ng, Adam Coates | 2012 Google "mạng học ra con mèo" (16.000 lõi); 2013 Stanford (ICML) | Từ hơn một nghìn máy chủ xuống ba máy gắn card đồ hoạ cho mạng cùng cỡ một tỉ | 9 cảnh, 32,6 s, MDTDMDGDT |
| 4 | 16/11 11:30 (Long 20:00) | `mim-dgx1-qua-tang-openai-2016` | "Ông chủ Nvidia tự mang quà tới OpenAI." (8) | Jensen Huang, Elon Musk, Ilya Sutskever | 08/2016 giao DGX-1; 30/11/2022 ChatGPT | Món quà tám GPU tới phòng thí nghiệm mới lập vài tháng; hơn sáu năm sau ChatGPT ra mắt | 9 cảnh, 35,0 s, MDGMDMGDT |
| 5 | 17/11 11:30 | `mim-fei-fei-li-14-trieu-anh` | "Cô muốn gom ảnh cho mọi danh từ." (8) | Fei-Fei Li (Lý Phi Phi) | 2006 khởi đầu; 2009 áp phích CVPR; 04/2010 hơn 14 triệu ảnh; 2012 cuộc thi | Từ chỗ khó nhờ đồng nghiệp giúp, tới bộ ảnh mà máy cần để có thứ học | 10 cảnh, 35,0 s, MGMDMDDMGT |
| 6 | 18/11 11:30 | `mim-patrascu-card-game-2009` | "Người dựng máy cho nhóm của Hinton." (8) | Relu Patrascu (lo máy tính nghiên cứu của nhóm học máy ở Toronto); Hinton làm nền | 2009 mua card Nvidia đầu tiên (Tesla, máy chủ); 2009 thử GTX 280/285; 2012 AlexNet trên GTX 580 | Từ Tesla đắt, mua được ít, phải tranh nhau thời gian, sang card chơi game mua được nhiều; học máy nhanh khoảng 30 lần (theo bài của khoa) | 9 cảnh, ước 34,8 s, MGDMGMDDT |
| 7 | 19/11 11:30 | `mim-jensen-ha-noi-nha-thu-hai` | "Nvidia muốn Việt Nam thành ngôi nhà thứ hai." (9) | Jensen Huang | 12/2023 tại Hà Nội; 05/12/2024 ký thoả thuận, mua VinBrain | Từ lời nói thành chữ ký trong chưa đầy một năm; kết giữ rào "làm được gì còn phải chờ" | 9 cảnh, 35,2 s, MDMDGMGTM |

Giờ là gợi ý của file lịch, chốt bằng `scripts/shorts_grid.py` ở pha 2. Thứ tự đặt bài mạnh trước (1, 2, 3) và bài 4 trước Long 20:00 ngày 16/11. Ước lượng thời lượng theo công thức của `_selfcheck.py` (4,2 tiếng/giây + nghỉ), chưa có TTS thật.

## 2. Số + nguồn từng bài

| # | Số trên màn hình / lời đọc | Nguồn | Trạng thái |
|---|---|---|---|
| 1 | CUDA thêm khoảng 50% chi phí mỗi chip; biên lãi gộp khoảng 30% (lời Jensen Huang kể); Buck về Nvidia 2004; CUDA 08/11/2006 | `factcheck.md` dòng 6, 7 (Lex Fridman Podcast #494); `script.md` CH03 | Dòng 7 đã gắn "theo lời kể". Ngày 08/11/2006 và năm 2004 mức SECONDARY |
| 2 | 12/2012, 4 công ty, từ xa, mỗi lần tăng ≥ 1 triệu đô, dừng 44 triệu, chọn Google; GTX 580 khoảng 500 đô | `factcheck.md` dòng 9, 12 (Wired 2021 trích Cade Metz) | OK; giá card SECONDARY |
| 3 | 16.000 lõi / hơn 1.000 máy (Google 2012); 3 máy → 1 tỉ tham số; 16 máy → hơn 11 tỉ (ICML 2013); chưa ai bảo mạng "mèo" là gì | ICML 2013 (`proceedings.mlr.press/v28/coates13.html`); The Register 18/06/2013; blog Google 06/2012 qua tìm kiếm | Số máy/tham số của Stanford kiểm được ở abstract. "Hơn 1 tỉ kết nối" của Google và NYT 25/06/2012 chưa đọc bản gốc: cần kiểm |
| 4 | tám GPU; 08/2016; OpenAI lập 12/2015; ChatGPT 30/11/2022; giá khoảng 129.000 đô | `factcheck.md` dòng 10, 11; Fortune 15/08/2016; Entrepreneur | Giá và chi tiết ký lời chúc chỉ có ở báo; cần kiểm với thông cáo Nvidia |
| 5 | 49 nghìn người, 167 nước, hơn 160 triệu ảnh ứng viên, hơn 14 triệu ảnh (30/04/2010), áp phích CVPR 2009 ở Florida, 2006 khởi đầu, Wired: khó nhờ đồng nghiệp | Wikipedia "ImageNet" (dẫn Wired); `script.md` CH05, CH08 | Nguồn gốc Wired chưa đọc: cần kiểm. `script.md` ghi Stanford năm 2006, sai: 2006 cô chưa ở Stanford |
| 6 | 30 lần nhanh hơn máy chủ nhiều lõi thời ấy; Tesla "nhiều nghìn đô" một hệ thống; GTX 280/285 năm 2009, sau đó 480/580; AlexNet 2012 trên GTX 580 | John DiMarco (Khoa Khoa học máy tính ĐH Toronto), blog 06/11/2023, `cs.toronto.edu/~jdd/blog.cgi/2023/11/06` (đã đọc 20/10/2026); `script.md` CH05 | Bài không nêu ngày mua chính xác, model Tesla, giá card chơi game: lời đọc không nói giá card chơi game. "30 lần" là kết quả của nhóm, lời đọc ghi "theo khoa". Thay bài Mona Lisa 2008 theo quyết định chủ kênh 20/10 |
| 7 | 12/2023 Hà Nội; 05/12/2024 ký thoả thuận; VinBrain; trung tâm dữ liệu mở rộng từ Viettel | `factcheck.md` dòng 13, 14 | SECONDARY; lời đọc ghi "báo chí ghi lại", chỉ nêu điều đã ký |

## 3. Vì sao không trùng

Đối chiếu `state.sqlite` (mode=ro, 160 Short MIM, tới 12/11) và spec bài mẫu. Short hiện có liên quan GPU: `mim-alexnet-2-card` (ImageNet 2012, 15%/26%, hai card), `mim-nobel-ngo-cut` (một dòng 2012), `mim-teaser-hinton-x-quang`, `mim-nvidia-quan-an-dem` (bài mẫu, Denny's 1993 + Krizhevsky 2012 + 15,3%).

| # | Gần nhất | Giống | Khác |
|---|---|---|---|
| 1 | bài mẫu, `mim-alexnet-2-card` | cuối nhắc card chơi game dạy máy nhìn (một câu, không tên, không số) | góc là canh bạc chi phí CUDA 2006 và Ian Buck; không Denny's, không 15,3% |
| 2 | bài mẫu, `mim-nobel-ngo-cut` | Krizhevsky chỉ là một trong ba tên | góc là cuộc đấu giá 12/2012 và lý do Hinton dừng; không có cuộc thi, không có 15,3% |
| 3 | `mim-watson-90-may-chu` (2.880 lõi) | cùng nói số máy/lõi | khác hãng, năm, bài toán; góc là thu nhỏ từ nghìn máy xuống ba |
| 4 | bài mẫu | cùng Jensen Huang | khác sự kiện (2016 giao máy), khác kết (ChatGPT) |
| 5 | `mim-alexnet-2-card` | ImageNet là cái tên của cuộc thi | góc là người làm bộ ảnh (Fei-Fei Li); câu 2012 chỉ một dòng, không số, không tên đội |
| 6 | `mim-alexnet-2-card` (ImageNet 2012, hai card), bài mẫu | cùng nhắc AlexNet/GTX 580 ở câu gần cuối | góc là người dựng máy (Patrascu) và quyết định 2009 chọn card chơi game; không Denny's, không 15,3%, Krizhevsky không xuất hiện; câu AlexNet 2012 chỉ một dòng, không số |
| 7 | `mim-9-tren-10-hoc-sinh-dung-ai` (Việt Nam, AI) | cùng bối cảnh Việt Nam | khác đối tượng, khác sự kiện |

Ticket T5–T9 cũ (kế hoạch + specs): không file nào nhắc Nvidia, GPU, CUDA, ImageNet, Hinton, DGX. T7 có góc "huấn luyện giá rẻ" (Pluribus dưới 150 đô); bài 3 không dùng góc chi phí. T9 (máy chơi game) dùng AlphaStar/Atari, không đụng. Long `mim-ai-70` có hai dòng nói GPU và ImageNet, không phải Short. Mỗi Short chỉ có một chủ đề mỗi ngày, hai bài liền nhau khác chủ đề (T4 chiếm 11:30; T5 ở 19:00).

Clip: 24 clip Pexels (chưa clip nào có trong specs MIM khác, đã kiểm bằng cách quét toàn bộ `data/stier/specs/mim-*.json` + specs các ticket); không clip nào lặp giữa 7 bài. Tên clip chỉ là mô tả chung (bàn phím, thư viện, đường phố), **chưa xem hình**: bắt buộc chạy `motion/long/clip_sheet.py` ở pha 2 để loại clip có logo/biển/chữ. Hai clip Hà Nội (34935995 và 32598233) dùng đúng cho Hà Nội; hai clip y tế/bàn phím chỉ minh hoạ chung chung, không đại diện nơi cụ thể.

## 4. Bài yếu

- ~~Bài 6 (Mona Lisa 2008)~~ **đã thay ngày 20/10** bằng `mim-patrascu-card-game-2009` (chủ kênh duyệt kế hoạch, bỏ vì không có xung đột thật, số lệch nguồn). Lý do không chọn dự phòng cũ: Hinton-Nobel dính Krizhevsky và `mim-nobel-ngo-cut`; Raina-Ng 2009 chưa tìm được xung đột có nguồn; "hai bán cầu" cùng nhân vật với bài mẫu. Bài mới yếu vừa: xung đột là hạn chế (đắt, hiếm, nóng) chứ không phải tranh cãi giữa người với người.
- **Bài 7 (Việt Nam): yếu thứ hai.** Xung đột mỏng (từ lời hứa tới chữ ký). Bù bằng độ gần với người xem Việt; nguồn SECONDARY.
- **Bài 4 (DGX-1): trung bình.** Món quà và bước ngoặt ChatGPT có, nhưng không có người nào "thua hay nghi ngờ".
- Mạnh: bài 1, 2 (xung đột chi phí và đấu giá), 3 (thu nhỏ từ nghìn máy xuống ba), 5 (một người đi ngược khó khăn).

## 5. Danh sách cần kiểm (trước khi dựng)

1. Bài 1: ngày 08/11/2006 và năm 2004 (thông cáo Nvidia / HPCwire). Lời "nằm sẵn trong card chơi game ai cũng mua được": CUDA ra cùng dòng GeForce 8800, cần xác nhận.
2. Bài 2: đọc lại Wired 2021 để chắc "dừng ở 44 triệu", "từ xa", "mỗi lần tăng ≥ 1 triệu". Giá GTX 580 khoảng 500 đô.
3. Bài 3: đọc bản gốc NYT 25/06/2012 và blog Google 26/06/2012 (số lõi, số kết nối, "chưa ai bảo là mèo"). So sánh hai thí nghiệm khác nhau (kết nối của Google, tham số của Stanford); lời đọc và màn hình đều ghi "hai thí nghiệm khác nhau, cùng cỡ mạng chừng một tỉ", cần chủ kênh đồng ý có giữ so sánh này không. Register ghi "lõi", báo khác ghi "bộ xử lý".
4. Bài 4: lời chúc Jensen Huang ký lên máy (các báo khác nhau chỗ ký) nên lời đọc chỉ diễn ý; giá 129.000 đô; ngày giao máy chính xác (khoảng 12/08/2016); Musk có mặt hay không (lời đọc chỉ nói gửi lời chúc).
5. Bài 5: Wired gốc (đồng nghiệp ngại giúp); "hơn 160 triệu ảnh ứng viên"; sửa `script.md` CH05 (Stanford 2006 sai).
6. Bài 6 (Patrascu): nguồn duy nhất là blog của một nhân viên khoa (DiMarco, 2023), hồi tưởng sau 14 năm; cần chủ kênh đồng ý dùng. "Rẻ hơn" không có trong lời đọc (chỉ nói "mua được nhiều chiếc"). Ngày mua Tesla (đầu 2009) là suy từ "by 2009"; kiểm bài báo Raina-Ng/Mohamed-Dahl nếu muốn. Mô tả ghi GTX 480/580 "sau đó". Clip 7311101, 34268300, 5875724 là ba clip từ bài Mona Lisa cũ, chưa xem hình: chạy `clip_sheet.py`, bỏ clip có logo/chữ. Tên `say`: Relu → Rê-lu, Patrascu → Pa-trát-xcu (kiểm khi nghe TTS).
7. Bài 7: ngày Jensen Huang ở Hà Nội (khoảng 10/12/2023); "chưa đầy một năm"; nguồn gốc lời "ngôi nhà thứ hai" (hiện chỉ báo chí ghi lại, màn hình ghi rõ "diễn ý").
8. Mọi bài: link Long trong mô tả (`https://youtu.be/Es4bogrdk-c`, lấy từ bài mẫu) cần xác nhận đúng ID Long `mim-ai-gpu`.
9. Pha 2: đọc tên (`say`) khi nghe TTS thật; kiểm thời lượng thật (ước 33–35 s) và cảnh dài nhất ≤ 11 s; hai cảnh `counter` bài 5 (49 nghìn, 14 triệu) xem số chạy có hợp "gần/hơn".

## 6. Góc dự phòng và góc đã bỏ

Dự phòng (có người, cần nguồn thêm nếu dùng):
- Hinton 03/2025: "Ilya nghĩ chúng tôi nên làm, Alex làm cho nó chạy được, còn tôi nhận Nobel" (`factcheck.md` dòng 2; dính Krizhevsky nên chỉ dùng nếu chủ kênh thấy không lặp bài mẫu).
- Hai bán cầu (mạng cắt đôi vì card 3 GB): đã kiểm, nhưng cùng nhân vật Krizhevsky với bài mẫu.
- Raina–Madhavan–Ng 2009 (tới 55 lần, vài tuần thành một ngày): có người nhưng không có xung đột thật nào có nguồn; chỉ làm nếu tìm được lời kể/trích dẫn về sự hoài nghi lúc ấy.
- Thay cho bài 6: đã dùng góc Patrascu (mục 4). Còn dự phòng: Hinton 03/2025 (cần chủ kênh chấp nhận trùng Krizhevsky), Raina-Ng 2009 (cần xung đột có nguồn).

Bỏ khỏi bản cũ (không có người/xung đột thật, theo yêu cầu "không độn"): bảng tra số lõi card (`mim-gpu-bang-tra-so-loi`, chỉ là bảng, không người), "GPU là một lời quảng cáo" (`mim-gpu-ten-quang-cao-1999`, chỉ có hãng), "giả làm bức tranh" (`mim-gpu-gia-lam-buc-tranh`, đã gộp vào bài 1 với Ian Buck), "tám GPU trong một hộp" và "hai bán cầu" (xem trên). Cần thêm góc cho bảng tự dò (khuôn thắng của FS) thì phải thêm một người thật; hiện không có.
