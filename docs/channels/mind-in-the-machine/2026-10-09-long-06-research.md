# Nghiên cứu video dài #6 — Mind in the Machine (MIM) — 09/10/2026

**Phạm vi:** hồ sơ dữ kiện cho video dài thứ sáu (16:9, ~12–13 phút, theme "lab", giọng Hải Đăng): **"GPU: con chip chơi game đã trở
thành trái tim của AI như thế nào?"** (slug `mim-ai-gpu`). Đề tài từ `2026-10-06-topic-research.md` §3.1 #7 ("Chip chơi game hoá ra lại
hợp để dạy AI" — Jensen Huang 121/ngày, GPU 6/ngày trên vi.wiki: người ta biết người, chưa biết khái niệm; rủi ro thấp nếu tránh giá cổ
phiếu/vốn hoá).

**Kịch bản đi kèm:** `data/long/mim-ai-gpu/script.md` (bản 1: 9 chương, 171 câu, 2.653 âm tiết, qua `script_lines.py`, 0 lỗi integrity,
không `ROADMAP_CLICHE`). **Chờ kiểm chứng** — danh sách điểm người viết chưa chắc ở mục "Ghi chú" của kịch bản.

**Nhãn:** **[bằng chứng]** = đã đọc tận nguồn gốc hôm nay · **[SECONDARY]** = qua báo / kết quả tìm kiếm · **[CHƯA KIỂM]** = cần kiểm
trước khi đọc. Lưu ý: hôm nay WebFetch lỗi DNS với computerhistory.org và spectrum.ieee.org; IEEE đọc được bằng curl.

## 1. Lộ trình và cấu trúc

- **Hình thức lộ trình: "Câu hỏi duy nhất"** — MIM #1–#5 đã dùng ba câu hỏi / chặng đường / lời thách / cảnh hẹn trước / nghịch lý.
  Câu hỏi: *"Vì sao một món đồ sinh ra để vẽ súng ống, xe đua trong game lại trở thành thứ quý nhất của cả ngành trí tuệ nhân tạo?"* —
  trả lời ở CH05 (~45%).
- **Re-hook giữa video:** chi tiết "mạng bị cắt đôi trên hai card, hai bán cầu" (CH05) + cuộc đấu giá Tahoe (CH06).
- **Cảnh mạnh thứ hai (~65%):** DGX-1 bàn giao tận tay cho OpenAI 08/2016 + 512 → 16.384 lõi.

## 2. Dữ kiện và nguồn

| # | Dữ kiện (dùng trong) | Nguồn | Nhãn |
|---|---|---|---|
| 1 | AlexNet huấn luyện **5–6 ngày trên hai GTX 580 3GB**; top-5 lỗi **15,3%** vs **26,2%** đội thứ hai (ILSVRC-2012); 60 triệu tham số, 650.000 nơ-ron; 1,2 triệu ảnh, 1.000 lớp; mạng **chia đôi trên 2 GPU** vì 3GB không đủ (CH00, CH04, CH05) | Krizhevsky, Sutskever, Hinton, *ImageNet Classification with Deep CNNs*, NeurIPS 2012 — PDF toàn văn, đọc bằng pdftotext: https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf | [bằng chứng] |
| 2 | Huấn luyện "trên máy tính có hai card Nvidia **trong phòng ngủ của Krizhevsky ở nhà bố mẹ**"; hơn một năm chỉnh/dạy lại; câu Hinton *"Ilya thought we should do it, Alex made it work, and I got the Nobel prize."*; ImageNet do Fei-Fei Li khởi xướng 2006, "every noun in the English language", hoàn thành 2009 (CH00, CH05) | Hansen Hsu (CHM), *AlexNet Source Code Is Now Open Source*, IEEE Spectrum 21/03/2025 (cập nhật 25/03/2025; Hinton duyệt đoạn trích): https://spectrum.ieee.org/alexnet-source-code | [bằng chứng] |
| 3 | GTX 580 ra mắt **09/11/2010**, giá đề xuất **499 USD**, **512 lõi CUDA** (CH00, CH06) | Neowin / APH Networks 09/11/2010 (qua tìm kiếm) | [SECONDARY] |
| 4 | Nvidia thành lập **05/04/1993**; ba người sáng lập phác ý tưởng ở **Denny's, đường Berryessa, đông San Jose**, cuối 1992 (CH01) | Wikipedia "Nvidia" + NBC 2023 (Jensen kể lại) | [SECONDARY] — cần nguồn Nvidia/Denny's gốc |
| 5 | GeForce 256 công bố **31/08/1999**, Nvidia tự gọi là "GPU đầu tiên trên thế giới" và **tự định nghĩa** thuật ngữ (CH01) | CNNfn 31/08/1999; Wikipedia "GeForce 256" | [SECONDARY] |
| 6 | MythBusters tại **NVISION 08** (San Jose, 25–28/08/2008): máy "Leonardo" bắn từng viên; máy 1.100 nòng vẽ Mona Lisa trong < 0,1 giây (CH02) | bit-tech; Wikipedia "Nvision" | [SECONDARY] — **không dùng footage** (bản quyền), chỉ kể |
| 7 | Ian Buck (Stanford) viết **Brook**; về Nvidia 2004, dẫn nhóm làm CUDA (CH03) | HPCwire "35 HPC Legends: Ian Buck"; Tom's Hardware phỏng vấn; CV Stanford | [SECONDARY] |
| 8 | CUDA công bố **08/11/2006** cùng GeForce 8800 (G80) (CH03) | Digital Engineering / Gamedeveloper 2006; Wikipedia "GeForce 8 series" | [SECONDARY] |
| 9 | Raina, Madhavan, Ng (ICML 2009): DBN **nhanh tới 55 lần** so với CPU hai lõi; DBN 4 lớp, 100 triệu tham số: **vài tuần → khoảng 1 ngày** (CH04) | Abstract qua mlanthology.org/icml/2009/raina2009icml-large | [bằng chứng] (abstract) |
| 10 | Đấu giá DNNresearch, khách sạn sòng bạc hồ Tahoe, 12/2012; Google, Microsoft, DeepMind, Baidu; bước giá ≥ 1 triệu USD; dừng ở **44 triệu USD**, về Google (CH06) | Cade Metz, *Genius Makers* (2021) — trích qua Goodreads/36kr | [SECONDARY] — kiểm bản Wired 2021 |
| 11 | Jensen Huang tự tay giao **DGX-1** cho OpenAI ở San Francisco, **08/2016**; Nvidia gọi là "world's first supercomputer dedicated to AI" (CH06) | Fortune 15/08/2016; DataCenterKnowledge 18/08/2016; TOP500 | [SECONDARY] — kiểm blog Nvidia gốc |
| 12 | RTX 4090: **16.384 lõi CUDA**, ra mắt 12/10/2022 (CH06) | Tom's Guide; custompc | [SECONDARY] — kiểm trang nvidia.com |
| 13 | Jensen Huang tới Hà Nội **09–10/12/2023** (lần đầu), gặp Thủ tướng, thăm NIC, "ngôi nhà thứ hai" (CH07) | Malay Mail 10/12/2023; VOH; vietnamfinance | [SECONDARY] |
| 14 | **05/12/2024**: Chính phủ VN – Nvidia ký thoả thuận lập **VRDC** + **trung tâm dữ liệu AI** (mở rộng TTDL của Viettel); Nvidia mua **VinBrain** (CH07) | Vietnam News 06/12/2024; VnEconomy 06/12/2024; DataCenterKnowledge | [SECONDARY] — kiểm baochinhphu.vn |

## 3. Tư liệu hình (giấy phép đã đọc qua Commons API, 09/10/2026)

> **Sửa 09/10 (PM):** kênh MIM **không nhận BY-SA** (`build_long._channels` `no_sa`). Bỏ: ảnh Nobel của Hinton, EVGA GTX 580, trụ sở
> Nvidia, 2484 Berryessa Road, DGX của dllu. Thay bằng: `hinton` = *Geoffrey Hinton at Collision 2024 in Toronto (cropped).jpg* (CC BY 2.0),
> `sutskever` = *Naveen Rao and Ilya Sutskever Stanford 2014.jpg* (CC BY 2.0), `gp100` = nhân Tesla P100 (GPU trong DGX-1, CC0). Bảng dưới
> giữ để tra; danh sách dùng thật nằm ở `IMGS` trong `data/long/mim-ai-gpu/gen_scenes.py`.

| Khoá đề xuất | File Commons | Giấy phép |
|---|---|---|
| `gf256` | File:VisionTek GeForce 256.jpg (2048×1216) | Public domain |
| `gtx580die` | File:NVIDIA@40nm@Fermi@GF110@GeForce GTX 580@… (nhiều ảnh die, 6000×4000) | CC0 |
| `gtx580` | File:EVGAGeforceGTX580.jpg (4031×1910) | CC BY-SA 4.0 |
| `jensen` | File:Jensen Huang (cropped) (2024).jpg | CC BY 4.0 |
| `hinton` | File:Geoffrey Hinton at the 2024 Nobel Lectures.jpg | CC BY-SA 4.0 |
| `feifei` | File:Fei-Fei Li at AI for Good 2017.jpg | CC BY 2.0 |
| `dennys` | File:2484 Berryessa Road.jpg — **cần kiểm** có phải quán Denny's không | CC BY-SA 4.0 |
| `nvhq` | File:NVIDIA Headquarters.jpg | CC BY-SA 4.0 |
| `dgx` | File:Nvidia DGX front view dllu.jpg / video "Nvidia DGX Station … .webm" (3840×2160, CC BY 3.0) | CC BY-SA 4.0 / CC BY 3.0 |

**B-roll Pexels** (`python motion/long/pexels.py search mim-ai-gpu …`, chỉ mục `output/long/mim-ai-gpu/broll/index.json`): card đồ hoạ cận
cảnh 5466792, man-holding-a-video-card 7380236, CPU 5467579, quạt tản nhiệt 3147349, chơi game đêm 10620285, phòng game giải đấu
7914862, cáp máy chủ 1085656, ổ cứng lưu trữ 5028622.

**Cảnh tự dựng (không có tư liệu):** bếp — đầu bếp vs hàng nghìn phụ bếp (lưới chấm), lưới 1920×1080 điểm ảnh, "bức tranh giả" (số trong
màu điểm ảnh), bảng tính trọng số, mạng chia đôi hai bán cầu, đồng hồ đấu giá tăng từng triệu, 512 → 16.384 lõi (lưới chấm đếm).

## 4. Không dùng

Giá cổ phiếu, vốn hoá, tài sản cá nhân; footage MythBusters/Nvidia keynote (bản quyền); logo Nvidia làm chủ thể thumbnail; mọi khẳng định
"nhanh hơn X lần" không kèm điều kiện so sánh.
