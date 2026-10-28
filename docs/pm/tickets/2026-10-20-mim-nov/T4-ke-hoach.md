# T4 — 8 Short nhử Long `mim-ai-gpu` (lên 16/11/2026 20:00) — bản 1, chờ duyệt

Người viết: agent T4, 20/10/2026. Pha 1: chỉ viết file. Spec nằm ở `specs-T4/` (8 file JSON, theme `mim`); chưa ghi vào `data/stier/specs`, chưa dựng, chưa đăng.
Nguồn con số: `data/long/mim-ai-gpu/script.md` + `factcheck.md` (đã kiểm chứng vòng 1, 09/10) và hồ sơ `docs/channels/mind-in-the-machine/2026-10-09-long-06-research.md`. Chỗ chưa kiểm ghi **CẦN KIỂM** (mục 5).

## 1. Luật áp cho lô này

- 2 Short/ngày, 13/11 → 16/11 (4 ngày × 2 = 8 bài). Giờ lấy từ `scripts/shorts_grid.py` (đã chạy: MIM 13–24/11 đang 0/5 mỗi ngày, slot 06:30 · 11:30 · 17:00 · 19:00 · 21:30). Dùng 11:30 và 19:00; riêng 16/11 (có Long 20:00) dùng 11:30 và 17:00 để không đè Long.
- Mỗi Short mở bằng con số hoặc sự kiện có ngày, câu mở ≤ 9 chữ, một insight, câu chốt quay lại ý mở, không câu hỏi cuối, không mời xem Long trong lời đọc (nối bằng "Video liên quan" + link trong mô tả; mô tả đã có dòng "Bản đầy đủ: …" với chỗ trống ID Long, điền sau khi Long có URL).
- Không bài nào dùng khung "mẹo". Lời đọc không có chữ số (số viết bằng chữ; chữ số chỉ hiện trên màn hình).
- 60/40: 5 bài SỐ/SỰ KIỆN (khuôn đã thắng), 3 bài THỬ. Khuôn mới trong lô: **bảng tra tự dò** (bài 6) — một bài duy nhất.
- Chuẩn Short v3: `theme: mim`, giọng Thanh Bình (mặc định theme), `mix: true`, `rules: 2`, nhạc nền nhỏ (music_gain 0,18, duck 3). Làm **một bài mẫu cho chủ kênh duyệt trước** khi dựng cả lô: đề xuất bài 3 `mim-gpu-55-lan-2009` (số sạch nhất, nguồn bằng chứng, ít rủi ro clip) — thứ tự lịch dưới đây không phụ thuộc bài mẫu.
- Đổi thứ tự/loại cảnh giữa các bài kề nhau (cột "Cảnh" ở mục 2: M = ảnh/clip, T = chữ, D = số liệu, G = sơ đồ).

## 2. Lịch và 8 bài

| # | Ngày · giờ (VN) | Slug | Nhãn | Cảnh |
|---|---|---|---|---|
| 1 | T6 13/11 · 11:30 | `mim-gpu-1100-nong-mona-lisa` | SỰ KIỆN (08/2008) | M T G D G |
| 2 | T6 13/11 · 19:00 | `mim-gpu-55-lan-2009` | SỐ (ICML 2009) — **bài mẫu** | G M D T M |
| 3 | T7 14/11 · 11:30 | `mim-gpu-tahoe-44-trieu` | SỰ KIỆN (12/2012) | M G D D M T |
| 4 | T7 14/11 · 19:00 | `mim-gpu-gia-lam-buc-tranh` | THỬ (cơ chế, mốc 08/11/2006) | M M G D T |
| 5 | CN 15/11 · 11:30 | `mim-gpu-hai-ban-cau` | SỰ KIỆN (bài báo 2012) | M D G M T |
| 6 | CN 15/11 · 19:00 | `mim-gpu-bang-tra-so-loi` | THỬ (**bảng tra tự dò**) | M D G D |
| 7 | T2 16/11 · 11:30 | `mim-gpu-dgx1-openai-2016` | SỰ KIỆN (08/2016) | M G D M |
| 8 | T2 16/11 · 17:00 | `mim-gpu-ten-quang-cao-1999` | THỬ (kiểm một giai thoại tên gọi, 31/08/1999) | M M D G T |
| — | **T2 16/11 · 20:00** | *Long `mim-ai-gpu` (đã hẹn)* | | |

(Số thứ tự ở mục 3 trùng với bảng này. Bài mẫu là #2.)

## 3. Chi tiết từng bài

Câu mở là dòng 0 của `lines`; câu chốt là dòng cuối. Độ dài ước 25–30 giây (97–116 từ).

### #1 `mim-gpu-1100-nong-mona-lisa` — SỰ KIỆN
- **Tiêu đề:** Năm 2008, 1.100 nòng súng bi sơn vẽ xong bức Mona Lisa trong chưa đầy một phần mười giây
- **Mở (9 chữ):** "Một nghìn một trăm nòng súng bắn cùng lúc."
- **Insight duy nhất:** vẽ nhanh = số đông làm cùng lúc, đúng cách card đồ hoạ làm việc (mỗi viên bi = một điểm ảnh).
- **Số + nguồn:** 1.100 nòng, dưới 0,1 giây, NVISION 08 (25–28/08/2008, San Jose), hai người dẫn MythBusters — `script.md` CH02; research mục 2 dòng 6 (bit-tech, Wikipedia "Nvision") **[SECONDARY — CẦN KIỂM URL gốc]**. Chỉ kể lại, không dùng footage (bản quyền, ghi ở "Không dùng").
- **Chốt:** "Một nghìn một trăm nòng, cùng một lúc: đó là cách một con chip vẽ."
- **Không trùng:** MIM chưa có Short MythBusters/Mona Lisa; Short `mim-alexnet-2-card` chỉ nói "vẽ hàng triệu điểm ảnh" ở câu cuối, không dùng thí nghiệm này.

### #2 `mim-gpu-55-lan-2009` — SỐ (bài mẫu)
- **Tiêu đề:** Năm 2009: dạy mạng nơ-ron trên card đồ hoạ nhanh hơn tới 55 lần, vài tuần còn một ngày
- **Mở (8 chữ):** "Vài tuần dạy máy, rút còn một ngày."
- **Insight:** card đồ hoạ rút thời gian dạy một mạng lớn từ vài tuần xuống khoảng một ngày — kèm điều kiện: một bài toán, so với CPU hai lõi.
- **Số + nguồn:** 55 lần; mạng 4 lớp 100 triệu tham số; vài tuần → khoảng một ngày — Raina, Madhavan, Ng, ICML 2009, abstract: https://mlanthology.org/icml/2009/raina2009icml-large/ ; `factcheck.md` dòng 8 (OK, bằng chứng); `script.md` CH04.
- **Chốt:** "Nhưng vài tuần đã thành một ngày." (câu 5 nói rõ "kết quả của một thí nghiệm, trên một bài toán, so với một loại máy").
- **Không trùng:** chưa có Short nào về Andrew Ng/2009; `mim-alexnet-2-card` là 2012.

### #3 `mim-gpu-tahoe-44-trieu` — SỰ KIỆN
- **Tiêu đề:** Tháng 12/2012: công ty ba người, chưa có sản phẩm, được trả giá tới 44 triệu đô
- **Mở (7 chữ):** "Ba người, bốn mươi bốn triệu đô."
- **Insight:** thứ được định giá là cách dạy máy nhìn, không phải sản phẩm.
- **Số + nguồn:** đấu giá kín bên hồ Tahoe 12/2012; 4 công ty trả giá từ xa; bước ≥ 1 triệu đô; Hinton dừng ở 44 triệu đô, chọn Google — Cade Metz, *Genius Makers* (2021) qua Wired 2021; `factcheck.md` dòng 9 (đã sửa "bốn công ty"); `script.md` CH06. Lời đọc ghi "Theo nhà báo Cade Metz".
- **Chốt:** "Ba người, và một cách dạy máy nhìn, đáng ít nhất bốn mươi bốn triệu đô."
- **Ảnh:** Hinton, `File:Geoffrey Hinton at Collision 2024 in Toronto (cropped).jpg` (CC BY 2.0, đã dùng ở Long; MIM không nhận BY-SA).
- **Không trùng:** `mim-nobel-ngo-cut` và `mim-teaser-hinton-x-quang` nói Nobel/X-quang, không nói đấu giá.

### #4 `mim-gpu-gia-lam-buc-tranh` — THỬ (cơ chế)
- **Tiêu đề:** Trước CUDA, nhà khoa học phải giả dạng phép tính thành bức tranh để card đồ hoạ chịu làm toán
- **Mở (9 chữ):** "Chip tưởng mình đang vẽ, thật ra làm toán."
- **Insight:** trước CUDA, muốn dùng card đồ hoạ làm toán phải giả bài toán thành bức tranh; CUDA (08/11/2006) cho ra lệnh tính thẳng.
- **Số + nguồn:** mốc 08/11/2006 CUDA + GeForce 8800 (research dòng 8, **SECONDARY**); cơ chế "giả làm bức tranh" — Owens et al. 2007, `factcheck.md` dòng 5 (OK, đơn giản hoá, spec ghi "ĐƠN GIẢN HOÁ" trên hình). Ví dụ ứng dụng (chất lỏng, địa chấn, phân tử thuốc) **CẦN KIỂM** với Owens et al. (`script.md` Ghi chú mục 1).
- **Chốt:** "Từ ngày ấy, chip không còn phải giả vờ vẽ."
- **Vì sao THỬ:** khuôn "một cơ chế bất ngờ" thay vì con số lớn; đo % ở lại so với bài số.
- **Không trùng:** chưa có Short về CUDA/GPGPU.

### #5 `mim-gpu-hai-ban-cau` — SỰ KIỆN
- **Tiêu đề:** AlexNet phải cắt đôi vì mỗi card chỉ có 3 gigabyte: cỗ máy thắng ImageNet có hai bán cầu
- **Mở (7 chữ):** "Mạng nơ-ron ấy có hai bán cầu."
- **Insight:** bộ nhớ 3 GB của mỗi card buộc nhóm cắt đôi mạng, hai nửa chỉ nói chuyện với nhau ở vài tầng.
- **Số + nguồn:** 3 GB/card, chia đôi kernel trên 2 GPU, "chỉ giao tiếp ở một số tầng", kích thước mạng bị giới hạn bởi bộ nhớ GPU — Krizhevsky, Sutskever, Hinton, NeurIPS 2012 (mục 1, 3.2): https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf ; `factcheck.md` dòng 3 (OK, bằng chứng); `script.md` CH05.
- **Chốt:** "Cỗ máy thắng cuộc thi ấy, theo đúng nghĩa đen, có hai bán cầu."
- **Không trùng:** `mim-alexnet-2-card` (13/10) kể 15,3% vs 26,2%, 5–6 ngày, "vì sao card chơi game"; bài này chỉ nói cắt đôi do bộ nhớ, không dùng các số ấy. Đây là **bài gần nhất** với một Short có sẵn — xem mục 4 ghi chú.

### #6 `mim-gpu-bang-tra-so-loi` — THỬ (bảng tra tự dò, khuôn mới)
- **Tiêu đề:** Card đồ hoạ của bạn có bao nhiêu lõi? Bảng tra 5 đời card từ 2010 đến 2022
- **Mở (7 chữ):** "Card của bạn có bao nhiêu lõi?"
- **Insight:** số lõi tăng 32 lần từ GTX 580 (2010) đến RTX 4090 (2022); người xem dừng hình tìm đời card của mình. Hàng 512 và 16.384 là con số của Long; cột "SO 580" là phép chia cho 512 (kênh tự tính).
- **Số + nguồn:** 512 lõi và 16.384 lõi, ×32, 12 năm — `factcheck.md` dòng 12 (OK, SECONDARY); `script.md` CH06. Ba hàng giữa (GTX 1080 2016 = 2.560; RTX 2080 Ti 2018 = 4.352; RTX 3090 2020 = 10.496) **CẦN KIỂM trên trang thông số nvidia.com trước khi dựng**; nếu không kiểm được thì rút bảng còn 2 hàng và đổi thành bài `cards3d` (spec phải sửa).
- **Chốt:** "Cùng một dòng card, mười hai năm, gấp ba mươi hai lần." Lưu ý "lõi GPU không so ngang lõi CPU" có trong lời đọc và dòng chân bảng.
- **Cảnh `table`** đã có trong engine (`casefile.js` B.table); hl hiện ô 512 rồi ô 16.384; quay lại bảng ở cuối để dừng hình (≤ 20 s mỗi cảnh, mix lint cho phép D tới 80%). Cần chữ nhãn ≥ 36 px trong khung 1080×1920 — kiểm contact sheet pha 2.
- **Không trùng:** MIM chưa có Short bảng tra; chưa có Short nào về số lõi (Short Watson nói 2.880 lõi CPU của IBM Power 750 — khác hẳn).

### #7 `mim-gpu-dgx1-openai-2016` — SỰ KIỆN
- **Tiêu đề:** Tháng 8/2016, Jensen Huang tự tay mang siêu máy tính 8 GPU tới một phòng thí nghiệm AI mới lập
- **Mở (9 chữ):** "Tám GPU trong một chiếc hộp, giao tận tay."
- **Insight:** từ hai card trong phòng ngủ tới tám GPU trong một hộp, tới ChatGPT sáu năm sau.
- **Số + nguồn:** 08/2016 DGX-1, 8 GPU, OpenAI "mới lập được vài tháng" (12/2015→08/2016); ChatGPT 30/11/2022 — Fortune 15/08/2016, DataCenterKnowledge 18/08/2016; `factcheck.md` dòng 10, 11 (OK, SECONDARY); `script.md` CH06. Nvidia gọi DGX-1 là siêu máy tính đầu tiên cho AI — lời đọc ghi rõ "Nvidia gọi".
- **Chốt:** "Từ hai chiếc card trong phòng ngủ, tới tám GPU trong một chiếc hộp."
- **Không trùng:** có Short nhắc OpenAI (`mim-chatgpt-700-trieu`, `mim-bo-xac-thuc-giong-noi`, `mim-noam-brown-nghi-lau-hon`) nhưng không ai nói DGX-1; T9 có OpenAI Five (2018–2019) — khác sự kiện.

### #8 `mim-gpu-ten-quang-cao-1999` — THỬ (kiểm giai thoại tên gọi)
- **Tiêu đề:** Chữ GPU ra đời năm 1999 như một lời quảng cáo: Nvidia tự đặt tên và tự định nghĩa
- **Mở (7 chữ):** "Chữ GPU là một lời quảng cáo."
- **Insight:** "GPU đầu tiên" là cách chính Nvidia gọi và định nghĩa GeForce 256.
- **Số + nguồn:** 31/08/1999 GeForce 256 — CNNfn 31/08/1999; Wikipedia "GeForce 256" (research dòng 5, **SECONDARY**); `script.md` CH01 ("do chính Nvidia đặt và định nghĩa, như một lời quảng cáo"). **CẦN KIỂM** nguồn gốc (thông cáo Nvidia 1999) trước khi dựng.
- **Chốt:** "Một lời quảng cáo, đã thành tên gọi của cả một ngành."
- **Ảnh:** `File:VisionTek GeForce 256.jpg` (Public domain, research mục 3).
- **Không trùng:** chưa có Short về lịch sử chữ GPU/GeForce.

## 4. Bảng đối chiếu trùng

**Short MIM hiện có (state.sqlite, `kind='short'`, `channel='MIM'`):** 160 bài, từ 08/10 → 12/11/2026 (đã đọc đủ danh sách slug) + quét toàn bộ `data/stier/specs/mim-*.json` bằng từ khoá: mona, tahoe, 44 triệu, 55 lần, bán cầu, DGX, GeForce, CUDA, Brook, MythBusters, lõi, ba gigabyte, đấu giá, siêu máy tính, Andrew Ng, giả dạng.

| Bài | Short MIM gần nhất | Kết luận |
|---|---|---|
| #1 Mona Lisa 1.100 nòng | không có | không trùng |
| #2 55 lần 2009 | `mim-alexnet-2-card` (2012, GPU), `mim-transformer-2017` (3,5 ngày trên 8 GPU) | khác mốc, khác số, khác bài báo |
| #3 Tahoe 44 triệu | `mim-nobel-ngo-cut`, `mim-teaser-hinton-x-quang` (Hinton) | khác sự kiện |
| #4 giả làm bức tranh | không có | không trùng |
| #5 hai bán cầu | `mim-alexnet-2-card` | **cùng nhân vật AlexNet, khác góc/số**; không dùng 15,3%/26,2%/5–6 ngày; Short kia đăng 13/10, cách bài này hơn một tháng. Nếu chủ kênh thấy gần quá thì thay bằng dự phòng "ImageNet đến trước chip" (mục 6) |
| #6 bảng số lõi | `mim-watson-90-may-chu` (2.880 lõi CPU) | khác đối tượng; bảng chỉ GPU |
| #7 DGX-1 | `mim-pluribus-150-do` ("không cần bộ xử lý đồ hoạ") | khác sự kiện |
| #8 chữ GPU | không có | không trùng |

**Ticket khác (đọc `T5-ke-hoach.md`, `T7-ke-hoach.md`, spec `specs-T5/T7/T8/T9` có sẵn lúc 20/10; chưa có `T6-ke-hoach.md`, `T8-ke-hoach.md`, `T9-ke-hoach.md`):** quét tiêu đề + lời đọc các spec T5, T7, T8, T9 tìm GPU/Nvidia/card/CUDA/ImageNet/AlexNet/Hinton/OpenAI/lõi/DGX/Stanford. Chỉ có T9 nhắc OpenAI (OpenAI Five, 08/2018 và 04/2019) — khác hẳn DGX-1 (08/2016). T7 ghi rõ "T4 có thể nhắc huấn luyện giá rẻ (GPU)" và không lấn góc nào của T4. T6 chưa có spec: đề tài chat/riêng tư, không giao với GPU. **Việc còn lại: đối chiếu lại khi T6, T8, T9 nộp kế hoạch** (nguy cơ nhỏ: T8 nhận diện khuôn mặt có thể nhắc ImageNet/AlexNet — T4 dùng AlexNet ở #5, #6 (một câu), nhờ T8 tránh số 3 GB và hai bán cầu).

**Trong chính lô T4:** không có hai bài cùng số; AlexNet xuất hiện ở #3 (nhắc 2012), #5, #6 (một câu); số 512/16.384 chỉ ở #6.

## 5. Cần kiểm trước khi dựng (pha 2)

1. #1: "dưới một phần mười giây" và "Mona Lisa" — nguồn bit-tech/Wikipedia là thứ cấp; tìm bản tin gốc (Nvidia/NVISION 08, kênh MythBusters).
2. #4: ví dụ chất lỏng/địa chấn/phân tử thuốc ↔ Owens et al. 2007; ngày CUDA 08/11/2006 là thứ cấp.
3. #6: số lõi GTX 1080, RTX 2080 Ti, RTX 3090 và năm ra mắt từng đời (nvidia.com); xác nhận 512 và 16.384 ở nvidia.com (factcheck mới ở mức SECONDARY).
4. #7: URL bài Fortune 15/08/2016 và blog Nvidia gốc về DGX-1; "OpenAI mới lập được vài tháng" (12/2015→08/2016 ≈ 8 tháng).
5. #8: thông cáo Nvidia 31/08/1999 về "GPU đầu tiên"; "hơn hai mươi năm sau" là diễn đạt của kênh.
6. **Clip Pexels** (chưa soát): `2539566` (bắn sơn), `7609195`, `3147349`, `7141174`, `31767906`, `1085656`, `7140928`, `5466792` (card cận cảnh — dễ có logo hãng), `854969`, `36139323`. Chạy bản tương đương `motion/long/clip_sheet.py` (3 khung/clip) cho các clip của Short trước khi render; clip không được có logo, ticker, tên công ty; thay clip nào dính (đặc biệt `5466792`).
7. Chỗ đọc tên (`say`) cần nghe thử: Tahoe, MythBusters, Krizhevsky, Sutskever, Cade Metz, DGX, GPU.
8. Chiều rộng chữ kinetic, vị trí nhãn/stamp trên khung 1080×1920 chỉ biết lúc build (chưa dựng).

## 6. Góc còn dư / chỗ thiếu góc

Đủ 8 bài; không phải độn. Nhưng nguồn của Long này phần lớn ở mức SECONDARY (mục 5), nên chất lượng kiểm chứng là điểm yếu, không phải số góc. Góc dư nếu bài nào bị loại:

- **ImageNet đến trước chip:** Lý Phi Phi khởi xướng 2006, hoàn thành 2009, "mọi danh từ trong tiếng Anh", 1,2 triệu ảnh huấn luyện, 1.000 lớp (IEEE Spectrum 21/03/2025; bài báo NeurIPS) — nhưng gần AlexNet; thay cho #5 nếu cần.
- **108 triệu lượt:** 1,2 triệu ảnh × khoảng 90 vòng qua bộ ảnh ≈ 108 triệu lượt đi qua mạng — phép nhân tự tính từ bài báo (CH04); nhãn SỐ, "kênh tự tính".
- **120 triệu điểm ảnh mỗi giây:** 1.920 × 1.080 × 60 = 124.416.000 (kênh tự tính từ CH02); gần câu cuối của `mim-alexnet-2-card`.
- **Canh bạc CUDA:** theo lời Jensen Huang (Lex Fridman Podcast #494) chi phí mỗi GPU tăng khoảng một nửa — **chưa kiểm tận nguồn, không có trong script**; chỉ dùng nếu đọc transcript.
- **Việt Nam:** Jensen Huang tới Hà Nội 12/2023 ("ngôi nhà thứ hai"), 05/12/2024 thoả thuận + VinBrain (CH07) — hợp khán giả Việt nhưng là chính trị/kinh doanh, lệch khung công nghệ; nhu cầu "Chất bán dẫn và Nvidia" trên vi.wiki chỉ 30 lượt/ngày (×0,54 so cùng kỳ, `data/briefs/MIM.md`) nên chủ đề GPU là cầu thấp: các Short sống nhờ khuôn mở bằng số/sự kiện, không nhờ từ khoá.
- Bỏ vì không đủ nguồn hoặc rủi ro: số phép nhân mỗi ảnh (CH04 "hàng trăm triệu", còn CẦN KIỂM), chip riêng của các hãng (CH08, chưa có nguồn), giá cổ phiếu/vốn hoá (cấm).

## 7. Cách đã tự kiểm spec

`motion/stier/build.py` **không có** cờ `--lint-only`; `--no-render` vẫn chạy TTS/tải ảnh nên không dùng ở pha 1. Thay bằng `specs-T4/_selfcheck.py` (chạy: `python docs/pm/tickets/2026-10-20-mim-nov/specs-T4/_selfcheck.py`) — nạp trực tiếp `MODE`, `scene_mode`, `mix_lint` từ `build.py` và lặp lại các luật cứng của `build()`: JSON hợp lệ; 55–135 từ; câu mở ≤ 9 chữ; không kết bằng "?"; lời đọc không chữ số; không có "~"; mọi mốc `[câu, "chữ", lần]` neo vào chữ có thật trong câu; counter không prefix có số khi đang đếm, không hiện năm, dòng phụ ≤ 52 ký tự; mix lint (có M, D, G; chữ ≤ 35%; không 3 cảnh liền cùng kiểu; cảnh ≤ 11 s, bảng ≤ 20 s) với thời gian ước 4,2 âm tiết/giây. Kết quả 8/8 OK. Giới hạn: thời gian là ước lượng; chưa kiểm chiều rộng chữ kinetic, tải ảnh/clip, phát âm TTS.
