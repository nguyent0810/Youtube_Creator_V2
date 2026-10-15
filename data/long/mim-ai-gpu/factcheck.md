# Kiểm chứng MIM #6 `mim-ai-gpu` — 09/10/2026 (PM, vòng 1)

Đối chiếu các mục "Cần kiểm chứng" trong `script.md` (mục Ghi chú) + các con số chính. Nguồn chi tiết: `docs/channels/mind-in-the-machine/2026-10-09-long-06-research.md`.

| # | Câu (chương) | Kết quả | Nguồn / ghi chú |
|---|---|---|---|
| 1 | Hai GTX 580 3GB, 5–6 ngày; 15,3% vs 26,2%; 60 triệu tham số (CH00, CH04) | OK | NeurIPS 2012 toàn văn (pdftotext) |
| 2 | Phòng ngủ ở nhà bố mẹ; hơn một năm chỉnh/dạy lại; câu Hinton "…I got the Nobel prize" (CH00, CH05) | OK | IEEE Spectrum / CHM, Hansen Hsu 21/03/2025 (Hinton duyệt) |
| 3 | Mạng chia đôi trên 2 GPU vì 3GB; hai nửa chỉ trao đổi ở vài tầng (CH05) | OK | NeurIPS 2012 §3.2: "puts half of the kernels on each GPU… communicate only in certain layers" |
| 4 | "Cả bộ ảnh lặp lại khoảng chín mươi lượt" (CH04) | SỬA → đã sửa | Paper: "roughly 90 cycles through the training set" (bản 1 viết "hàng chục lượt mỗi bức") |
| 5 | Giả dạng phép tính thành bức tranh (dữ liệu trong texture, chương trình như shader) (CH03) | OK (đơn giản hoá) | Owens et al., *A Survey of GPGPU*, Computer Graphics Forum 26(1), 2007 |
| 6 | Ian Buck, Brook, về Nvidia 2004, dẫn nhóm làm CUDA; mê GPU từ chơi game thời sinh viên (CH03) | OK [SECONDARY] | HPCwire "35 HPC Legends"; Tom's Hardware phỏng vấn |
| 7 | "Canh bạc" CUDA: chi phí thêm ăn gần hết lợi nhuận (CH03) | SỬA → đã gắn nguồn lời kể | Jensen Huang, Lex Fridman Podcast #494 (CUDA +~50% chi phí/GPU khi biên lãi gộp ~30%). Lời đọc ghi "theo lời chính Jensen Huang kể lại" |
| 8 | Raina, Madhavan, Ng 2009: tới 55 lần so với CPU hai lõi; vài tuần → ~1 ngày (CH04) | OK | Abstract ICML 2009 |
| 9 | Đấu giá Tahoe 12/2012, 4 công ty, bước ≥ 1 triệu USD, dừng 44 triệu, chọn Google (CH06) | SỬA → "bốn công ty trả giá từ xa" | Wired 2021 (trích *Genius Makers*, Cade Metz). Bản 1 viết "các tập đoàn lớn" — DeepMind khi ấy là startup |
| 10 | DGX-1 giao tận tay OpenAI, 08/2016, 8 GPU; OpenAI lập 12/2015, Sutskever đồng sáng lập (CH06) | OK [SECONDARY] | Fortune 15/08/2016; DataCenterKnowledge; DGX-1 = 8× Tesla P100 |
| 11 | ChatGPT "sáu năm sau" (30/11/2022) (CH06) | OK | 08/2016 → 11/2022 ≈ 6 năm 3 tháng |
| 12 | GTX 580 512 lõi, ~499 USD; RTX 4090 16.384 lõi, 2022; ×32, 12 năm (CH00, CH06) | OK [SECONDARY] | 16.384/512 = 32; 2010 → 2022 |
| 13 | Hà Nội 12/2023, "ngôi nhà thứ hai" (CH07) | OK — lời đọc đã ghi "báo chí ghi lại" | Bloomberg 11/12/2023 "Nvidia sees Vietnam as potential second home, reports say"; Tuổi Trẻ 10/12/2023 |
| 14 | 05/12/2024 thoả thuận VRDC + TTDL AI (mở rộng TTDL Viettel); mua VinBrain (CH07) | OK [SECONDARY] | Vietnam News 06/12/2024; DataCenterKnowledge |
| 15 | Nobel Vật lý 2024 của Hinton (CH05) | OK | — |

**Còn mở (không chặn thu âm):** Denny's: ảnh `2484 Berryessa Road.jpg` cần xem mô tả Commons có đúng quán Denny's không trước khi dùng (nếu không, dùng cảnh tự dựng). GeForce 256 / NVISION 08 / CUDA 08/11/2006 mới ở mức [SECONDARY] — đủ cho lời đọc dạng mốc thời gian.

**Kết luận:** OK 12 · SỬA 3 (đã sửa trong script.md) · BỎ 0. Có thể chạy `script_lines.py` → TTS.
