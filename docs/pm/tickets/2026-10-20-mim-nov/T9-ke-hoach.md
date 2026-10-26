# T9 — 8 Short gắn Long `mim-may-choi-game` (Long lên Thứ Năm 03/12/2026 20:00) — bản 1, chờ duyệt cổng pha 1

Người viết: agent T9, 20/10/2026. Pha 1: chỉ viết file. Chưa dựng, chưa đăng, chưa sửa `state.sqlite`, không đụng file ticket khác. Spec ở `docs/pm/tickets/2026-10-20-mim-nov/specs-T9/` (chưa ghi vào `data/stier/specs`).

## 0. Kết luận ngắn

- **Đủ 8 bài**, góc đều chưa có trên kênh (mục 4: 160 Short MIM trong state.sqlite, không bài nào nhắc AlphaStar, StarCraft, Dota, OpenAI Five, Atari/DQN; không Long nào khác nhắc).
- **Lịch chỉ chứa được 6 bài** trong 01–03/12 (2/ngày × 3 ngày). Hai bài còn lại (**M7, M4**) tôi đặt tạm vào slot T5 và T7 để trống (mục 1). Chưa khoá: cần Claude chốt khi gộp lịch các ticket.
- **60/40:** 5 bài SỐ/SỰ KIỆN (M1, M2, M3, M5, M6), 3 bài THỬ (M4, M7, M8).
- **Bài mẫu để chủ kênh duyệt trước:** **M3** (`mim-game-200-nam-14-ngay`): mọi số đều lấy thẳng từ blog DeepMind, cảnh đơn giản (clip, board, cards3d, counter, clip, slam).
- **Xếp hạng độ mạnh (tự đánh giá):** mạnh M1, M3, M6; khá M2, M5, M8; **yếu hơn M4 và M7** (xem "cần kiểm" và "thiếu góc"). Nếu phải cắt thì cắt hai bài này, không độn.
- **Điểm vướng lớn nhất:** Long này **chưa có `factcheck.md`** (thư mục `data/long/mim-may-choi-game/` có `script.md`, `spec.json`, `ch00–ch23.json`, `gen_scenes.py`). Nguồn của tôi là mục "Ghi chú" cuối `script.md`. Mọi số đã đối chiếu chéo với ghi chú đó, nhưng **blog DeepMind chưa được mở lại trực tiếp** ở pha này (xem mục 5).

## 1. Lịch (giờ VN, lấy từ `data/shorts_slots.json`, slot MIM 06:30 · 11:30 · 17:00 · 19:00 · 21:30)

`scripts/shorts_grid.py 2026-11-30 2026-12-04 --channel MIM` ngày 20/10: 01–03/12 đều 0/5 slot bị chiếm. Long ngày 03/12 là 20:00 (state.sqlite: `long-mim-may-choi-game`, `2026-12-03T13:00:00Z`, `video_id` `0J3dcjPjcdI`). Ngày thường dùng 11:30 + 19:00; ngày Long dùng 11:30 + 17:00 (cách Long 3 giờ, không đè). Không quá 2 Short/ngày.

| Thứ tự | Ngày | Giờ | Mã | Slug | Nhãn | Chuỗi kiểu cảnh* |
|---|---|---|---|---|---|---|
| 1 | T3 01/12 | 11:30 | M6 | `mim-game-280-so-678` | SỐ | M D D G M T |
| 2 | T3 01/12 | 19:00 | M5 | `mim-game-ti-2018-thua-hai-tran` | SỰ KIỆN | M M D G D T |
| 3 | T4 02/12 | 11:30 | M3 | `mim-game-200-nam-14-ngay` | SỐ (bài mẫu) | M G G D M T |
| 4 | T4 02/12 | 19:00 | M8 | `mim-game-og-chu-thich-nho` | THỬ | M G M G D T |
| 5 | T5 03/12 | 11:30 | M2 | `mim-game-muoi-mu-26` | SỐ | M M D G T M D |
| 6 | T5 03/12 | 17:00 | M1 | `mim-game-nhin-qua-man-hinh` | SỰ KIỆN | M D G M G T M |
| tràn A | T5 19/11 | 17:00 | M4 | `mim-game-nam-may-khong-ai-ra-lenh` | THỬ | M D G M G T M |
| tràn B | T4 25/11 | 11:30 | M7 | `mim-game-atari-khong-day-luat` | THỬ | M M D G G D T |

\*M = clip/ảnh, D = số liệu, G = sơ đồ, T = chữ. Hai bài kề nhau không cùng chuỗi. M5 và M8 cùng chuyện Dota nên cách nhau bởi M3.

**Slot tràn là đề xuất:** T5 nói 19/11 17:00 để trống; T7 nói 25/11 11:30 và 26/11 19:00 để trống (T7 chỉ có 4 bài). Tôi tránh 26/11 19:00 vì sát Long 20:00 của T7. Nếu hai slot này đã bị ticket khác lấy: (a) giữ M4, M7 làm dự phòng cho lô sau; hoặc (b) xin Claude nâng lên 3 Short/ngày ở 02/12 và 03/12 (06:30), theo quy tắc 2–3/ngày của chủ kênh. Không tự ý làm.

## 2. Từng bài

Quy ước chung: câu mở ≤ 9 chữ, đã đếm. Câu chốt quay lại ý mở, không câu hỏi cuối, không mời xem Long trong lời đọc. Mô tả mỗi Short kết bằng "Bản đầy đủ: https://youtu.be/0J3dcjPjcdI (công khai từ 20:00 ngày 03/12)" và câu "Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện." như các Short MIM trước. Mốc chương dẫn theo `script.md`.

### M6 · `mim-game-280-so-678` — SỐ (khuôn đã thắng: con số tương phản)
- **Tiêu đề:** AlphaStar bấm trung bình 280 hành động mỗi phút, ít hơn MaNa (390) và TLO (678): vì sao con số ấy chưa nói hết
- **Câu mở (7 chữ):** "Cỗ máy chậm tay hơn tuyển thủ. Trên giấy."
- **Insight duy nhất:** số trung bình thấp che mất đỉnh: trong giao tranh, tốc độ của máy có lúc vượt cả hai tuyển thủ.
- **Số + nguồn:** 280 / 390 / 678 hành động mỗi phút (trung bình) = `script.md` CH11 + ghi chú (blog DeepMind 24/01/2019: 277≈280, MaNa 390, TLO 678). "Số của TLO bị đẩy cao vì bấm phím liên tục" và "tốc độ máy có lúc cao hơn cả hai" = DeepMind làm rõ 29/01/2019 (ghi chú `script.md`).
- **Câu chốt:** "Chậm tay hơn, chỉ là con số trung bình trên giấy." (quay lại "chậm tay… trên giấy")
- **Không trùng:** xem mục 4. Gần nhất là `mim-watson-tieng-chuong` (công bằng của cuộc đua bấm chuông). Bài này không nói công bằng, không nói chuông; góc là "trung bình che đỉnh", có biểu đồ ba cột.

### M5 · `mim-game-ti-2018-thua-hai-tran` — SỰ KIỆN
- **Tiêu đề:** 08/2018: OpenAI Five thua cả hai trận ở The International, giải Dota 2 lớn nhất năm
- **Câu mở (8 chữ):** "Năm 2018, đội máy thua cả hai trận."
- **Insight duy nhất:** lần đầu ra sân khấu lớn nhất, đội máy thua cả hai trận, và nhận xét lúc ấy ("chỉ giỏi phản xạ") còn bị thử lại về sau.
- **Số + nguồn:** 08/2018, hai trận, paiN Gaming (Brazil) và đội cựu tuyển thủ hàng đầu Trung Quốc, thua cả hai (không nêu tỉ số) = CH18 + ghi chú (Wikipedia *OpenAI Five*, đọc 15/10/2026). "Gần tám tháng" = từ TI 08/2018 đến 13/04/2019 (**kênh tự tính**, ghi nhãn trên màn hình).
- **Câu chốt:** "Hai trận thua, và một nhận xét sẽ còn bị thử lại." (quay lại "thua cả hai trận")
- **Không trùng:** không Short nào nhắc OpenAI Five hay The International. Không kể kết quả với OG (để M8). Không lặp khung "người thắng duy nhất" của `mim-teaser-nuoc-78`.

### M3 · `mim-game-200-nam-14-ngay` — SỐ (bài mẫu)
- **Tiêu đề:** AlphaStar luyện tới 200 năm StarCraft trong giải đấu chạy 14 ngày (DeepMind, 2019)
- **Câu mở (8 chữ):** "Hai trăm năm chơi, trong mười bốn ngày."
- **Insight duy nhất:** quy mô luyện tập mà không con người nào có (200 năm trong 14 ngày).
- **Số + nguồn:** 14 ngày, 16 bộ xử lý chuyên dụng mỗi phiên bản, "tới hai trăm năm" chơi StarCraft theo thời gian thật = CH08 + ghi chú (blog DeepMind 24/01/2019: "up to 200 years"). Lời đọc giữ chữ "tới".
- **Câu chốt:** "Hai trăm năm, trong hai tuần." (quay lại mở; 14 ngày = hai tuần)
- **Không trùng:** `mim-alphago-30-trieu-nuoc-co`, `mim-alphago-zero-100-0`, `mim-alphazero-4-gio-co-vua` nói thời gian luyện của cờ vây/cờ vua, game khác, số khác. Không dùng số 45.000 năm của OpenAI (chưa đọc trực tiếp nguồn) và không nói về GPU/TPU như T4.

### M8 · `mim-game-og-chu-thich-nho` — THỬ (khuôn "tuyên bố + chú thích")
- **Tiêu đề:** 13/04/2019: OpenAI Five thắng OG, đội vô địch The International, nhưng ván đấu có chú thích nhỏ
- **Câu mở (9 chữ):** "Máy thắng nhà vô địch, có chú thích nhỏ."
- **Insight duy nhất:** chiến thắng có điều kiện: kho tướng thu nhỏ, vài cơ chế bị tắt, và chỉ máy đã luyện đúng phiên bản ấy.
- **Số + nguồn:** 13/04/2019, San Francisco, thắng hai ván đầu trước OG (vô địch TI 2018), loạt ba ván thắng hai = CH19 + ghi chú (Wikipedia, TechCrunch 15/04/2019). "Lần đầu AI thắng nhà vô địch thế giới esports" = **gắn "Theo OpenAI"** (script không gắn). "Hàng nghìn năm" luyện = CH19/CH20 (45.000 năm theo OpenAI qua báo chí; lời đọc không nêu số).
- **Câu chốt:** "Tỉ số là hai không, và chú thích nhỏ cũng thuộc về câu chuyện." (quay lại "chú thích nhỏ")
- **Không trùng:** không Short nào nói về esports hay OG. Đã **bỏ câu "báo gọi là gần như gian lận"** (Motherboard qua Wikipedia, chưa mở bài gốc), chỉ giữ phần giới hạn có trong script.

### M2 · `mim-game-muoi-mu-26` — SỐ (rủi ro trùng khuôn, xem mục 4)
- **Tiêu đề:** StarCraft: mỗi bước có khoảng 10 mũ 26 hành động hợp lệ, vì sao máy không thể duyệt hết như Deep Blue
- **Câu mở (9 chữ):** "Mỗi bước, mười mũ hai mươi sáu lựa chọn."
- **Insight duy nhất:** mỗi hành động là một tổ hợp (đơn vị nào, làm gì, ở đâu), nên số lựa chọn mỗi bước phình tới cỡ 10^26.
- **Số + nguồn:** ≈10^26 hành động hợp lệ mỗi bước, ván dài tới một giờ = CH06 + ghi chú (blog DeepMind 24/01/2019). "Vài chục nước hợp lệ ở cờ vua" = CH06, định tính, **chưa có nguồn số** (xem mục 5).
- **Câu chốt:** "Mười mũ hai mươi sáu: số một, theo sau là hai mươi sáu chữ số không." (quay lại mở)
- **Không trùng:** cùng họ "số khổng lồ" với `mim-co-vay-171-chu-so` và `mim-poker-10-mu-161`. Khác ở đối tượng (hành động mỗi bước, không phải số thế cờ) và ở lời giải thích tổ hợp ba lựa chọn. Biểu đồ cột ghi rõ "KHÔNG VẼ ĐÚNG TỈ LỆ". **Nếu Claude thấy ba bài "số có N chữ số" là quá dày, đổi M2 bằng góc dự phòng ở mục 6.**

### M1 · `mim-game-nhin-qua-man-hinh` — SỰ KIỆN (bài sát Long nhất, xếp ngay trước Long)
- **Tiêu đề:** AlphaStar thắng 10 ván liền, rồi MaNa thắng ván 11: khi cỗ máy phải nhìn qua khung màn hình (2019)
- **Câu mở (8 chữ):** "Bắt máy nhìn qua màn hình, MaNa thắng."
- **Insight duy nhất:** MaNa chỉ thắng khi máy bị giới hạn nhìn qua khung màn hình như người và mới luyện bảy ngày.
- **Số + nguồn:** 10 ván thắng (TLO 5–0, MaNa 5–0, ghi hình 12/2018), phiên bản camera luyện 7 ngày, ván biểu diễn MaNa thắng = CH10, CH13 + ghi chú (blog DeepMind 24/01/2019).
- **Câu chốt:** "Khi phải nhìn như người, và chưa luyện đủ lâu, cỗ máy không còn bất khả chiến bại." (quay lại "nhìn… người")
- **Không trùng:** cố ý **không dùng khung "ván duy nhất con người thắng"** của `mim-teaser-nuoc-78` (AlphaGo). Góc ở đây là giới hạn tầm nhìn. Không nhắc câu "MaNa tìm ra cách khiến máy lúng túng" (chưa có nguồn chi tiết).

### M4 · `mim-game-nam-may-khong-ai-ra-lenh` — THỬ (yếu hơn)
- **Tiêu đề:** OpenAI Five: năm cỗ máy chơi Dota 2 thành một đội mà không ai dạy cách chia việc
- **Câu mở (9 chữ):** "Năm cỗ máy, không ai ra lệnh cho ai."
- **Insight duy nhất:** phối hợp học ra từ phần thưởng chung của cả đội, không phải từ mệnh lệnh.
- **Số + nguồn:** năm người mỗi đội, mỗi người một tướng = CH15. "Chỉ được thưởng khi cả đội thắng; học được phải hy sinh lợi ích riêng" = CH17, **lời của kênh, nguồn OpenAI chưa đọc được (403)**: cần kiểm hoặc bỏ dòng 5. Không nêu số.
- **Câu chốt:** "Không ai ra lệnh, chỉ có một phần thưởng chung." (quay lại mở)
- **Không trùng:** nhẹ nhất với `mim-pluribus-nam-ban-sao` (T7; cùng mở "năm …", khác hẳn nội dung). Nên cách xa nhau, 19/11 so với 24/11 là tạm đủ.

### M7 · `mim-game-atari-khong-day-luat` — THỬ (yếu hơn, hơi ngoài mạch "thời gian thực")
- **Tiêu đề:** DQN 2015: cỗ máy học 49 trò chơi Atari chỉ từ màn hình và điểm số, không được dạy luật nào (DeepMind, Nature)
- **Câu mở (8 chữ):** "Không ai dạy nó luật chơi nào cả."
- **Insight duy nhất:** cỗ máy chỉ nhận ba thứ (hình ảnh màn hình, các nút bấm, điểm số) mà tự học được cách chơi.
- **Số + nguồn:** 02/2015, Nature, 49 trò Atari 2600, đầu vào điểm ảnh + nút + điểm số, trên 75% điểm người thử game chuyên nghiệp ở hơn nửa số trò = CH03 + ghi chú (Mnih et al., *Nature* 518; blog DeepMind 25/02/2015).
- **Câu chốt:** "Không luật chơi nào, chỉ có màn hình và điểm số." (quay lại mở)
- **Không trùng:** không Short nào về Atari/DQN. Gần họ `mim-alphago-30-trieu-nuoc-co` (cách học) nhưng khác trò, khác phương pháp.

## 3. Cách tự kiểm spec (không có cờ `--lint-only`)

`motion/stier/build.py` **không có `--lint-only`**; chỉ có `--no-render` và `--draft`, mà cả hai đều chạy TTS và tải clip, nên pha 1 không chạy. Thay vào đó tôi tự kiểm bằng một script tạm (scratchpad, không nằm trong repo), kết quả cả 8 bài đạt:

1. Mọi file là JSON hợp lệ, khoá theo mẫu `mim-*.json` mới nhất (`theme: mim`, `mix: true`, `rules: 2`, `tts.pauses`, `say`, `imgs: {}`).
2. Mọi mốc `[câu, "chữ"(, lần)]` trong `at/until/cross` có chữ đó thật sự trong câu (cùng hàm `norm` với `build.py`). Đây là lỗi cứng của build nên đã kiểm kỹ.
3. Câu mở ≤ 9 chữ; không câu hỏi cuối; mọi chữ trong `acc` có trong lời đọc.
4. Ước tính `mix_lint` (ước thời lượng từng câu theo số từ): đủ M, D, G; chữ thuần ≤ 17%; không 3 cảnh liền cùng kiểu; không cảnh nào quá 11 s. Cảnh counter không đặt chữ số vào `prefix`; dòng phụ ≤ 52 ký tự; không đặt `size` tay cho kinetic.
5. Độ dài lời đọc 78–113 từ (≈ 23–32 s theo ước lượng 3,9 từ/s). M3 ngắn nhất (≈ 28 s sau khi thêm một câu), M5 và M6 ≈ 26 s.

**Chưa kiểm được và phải làm ở pha 2:** thời lượng thật sau TTS (mix_lint thật chạy trong build), nghe thử `say` (đặc biệt "Ti-eo-ô", "Ma-na", "An-pha Xờ-ta", "Đê Cu En", "Ô Gi", "Pên"), kiểm khung 0 và chữ cắt mép.

## 4. Bảng đối chiếu trùng

### 4a. Với Short MIM hiện có (state.sqlite, `kind='short' and channel='MIM'`: 160 bài, `publish_at` 08/10 → 12/11)

Truy vấn trong spec 160 bài và `data/long/mim-*/script.md` các từ khoá `AlphaStar, StarCraft, Dota, Atari, OpenAI Five, DQN, MaNa, TLO`: **0 kết quả** ở mọi Short và mọi Long khác (kể cả 4 từ "game" xuất hiện ở `mim-flappy-*`, `mim-alexnet-2-card`, nói về trò chơi khác). Các bài gần nhất theo góc:

| Mã | Short cũ gần nhất | Giống ở đâu | Khác ở đâu | Mức |
|---|---|---|---|---|
| M1 | `mim-teaser-nuoc-78` | "ván duy nhất người thắng máy" | game khác, và M1 không dùng khung "duy nhất"; góc giới hạn tầm nhìn | thấp (đã né) |
| M1 | `mim-nghiep-du-thang-may-14-15`, `mim-con-nguoi-danh-hay-len` | người thắng máy | khác trò, khác nguyên nhân | thấp |
| M2 | `mim-co-vay-171-chu-so`, `mim-poker-10-mu-161` | "số khổng lồ, máy không duyệt hết" | M2 nói số hành động mỗi bước và tổ hợp ba lựa chọn | **trung bình (khuôn)** |
| M3 | `mim-alphago-30-trieu-nuoc-co`, `mim-alphago-zero-100-0`, `mim-alphazero-4-gio-co-vua` | thời lượng luyện của máy | game khác, số khác, nhấn "200 năm trong 14 ngày" | thấp |
| M4 | `mim-pluribus-nam-ban-sao` (T7) | mở bằng "năm …" | khác nội dung (Dota phối hợp so với poker) | thấp |
| M5, M8 | không | | OpenAI Five chưa có Short nào | không |
| M6 | `mim-watson-tieng-chuong` | máy có "nhanh tay" hơn người không | M6 là số trung bình so với đỉnh, không bàn công bằng | thấp–trung bình |
| M7 | `mim-alphago-30-trieu-nuoc-co` | cách máy học | trò Atari, không có nước cờ người | thấp |

### 4b. Với ticket T4–T8

Đã đọc `T5-ke-hoach.md`, `T7-ke-hoach.md` và liệt kê file trong `specs-T4/…T8`. T4, T6, T8 chưa có bản kế hoạch ở thời điểm này (specs-T4 rỗng), nên **chưa đối chiếu được phần T4, T6 và T8**. T5 (Watson, Jeopardy) và T7 (poker) không có bài nào về game video; không trùng. Việc cần làm ở cổng giữa: T4 (`mim-ai-gpu`) có thể nhắc GPU/TPU và quy mô luyện, nên M3 và M4 cần so lại với T4.

## 5. Chỗ cần kiểm (không bịa; ghi để pha 2 hoặc người duyệt xử lý)

1. **Long này thiếu `factcheck.md`**. Ghi chú nguồn trong `script.md` là cơ sở duy nhất. Trước khi dựng, mở lại các blog DeepMind 24/01/2019, 29/01/2019 (làm rõ APM), 30/10/2019 và các số CH06, CH08, CH11, CH13.
2. **M2:** "một thế cờ vua có vài chục nước hợp lệ" chỉ có trong lời kể (CH06), chưa có số hay nguồn. Giữ "vài chục". Nếu cần số, phải tìm nguồn (không dùng 35 khi chưa kiểm).
3. **M4:** "chỉ được thưởng khi cả đội thắng… hy sinh lợi ích riêng" là lời kênh (CH17); trang openai.com không đọc trực tiếp được (403). Cần đối chiếu blog OpenAI Five hoặc bỏ câu 5.
4. **M5:** "nhiều người nhận xét: chỉ giỏi phản xạ, chưa biết chiến lược" lấy từ CH18, **không gắn báo cụ thể**. Cần kiểm hoặc đổi thành lời chung hơn. "Gần tám tháng" là kênh tự tính (TI 2018 diễn ra khoảng cuối 08/2018 đến 13/04/2019).
5. **M8:** "lần đầu AI thắng nhà vô địch thế giới esports" phải giữ "Theo OpenAI". Giới hạn kho tướng/cơ chế "cho cả hai bên" là CH19; chưa nêu số tướng (Wikipedia có số nhưng không nằm trong script đã duyệt).
6. **M6:** kiểm lại câu "tốc độ có lúc vọt cao hơn cả hai" và "số của TLO bị đẩy cao" đúng như bài làm rõ 29/01/2019.
7. **Lỗi trong Long (không thuộc ticket này, chỉ báo):** CH20 viết "42.729 ván công khai, thắng 99,4%". Ghi chú nguồn cho thấy 99,4% là của các ván đối đầu (7.215 thắng, 42 thua, tổng 7.257), còn 35.466 ván hợp tác; 7.257 + 35.466 = 42.723, không bằng 42.729 (lệch 6). Tôi không dùng bất kỳ số nào trong đoạn này.
8. **Clip Pexels:** ID lấy qua tìm kiếm Pexels (portrait), chọn theo tên, **chưa xem hình**. `motion/long/clip_sheet.py` chỉ đọc `data/long/<chủ đề>/ch*.json`, không đọc spec Short, nên chưa dùng được cho Short. Pha 2: tải bằng `motion/stier/clips.py get` rồi soát khung đầu, giữa, cuối bằng mắt; bỏ clip có logo, tên giải, tên công ty, UI game. Rủi ro cao nhất: clip giải đấu (`9071004`, `7915042`, `9071005`), máy arcade (`4836573`), người chơi có màn hình (`9071003`, `8128031`, `8128500`).
9. **Tên riêng trong lời đọc:** không nêu tên đời thường của tuyển thủ (TLO, MaNa là tên thi đấu công khai, đúng như script).
10. **Clip trùng với Short cũ:** nhiều Short MIM dùng chung vài ID Pexels (28709421, 39270835…). Tôi chọn ID mới cho cả 8 bài nhưng chưa kiểm sổ clip; pha 2 chạy kiểm trùng với `data/variety`.

## 6. Chỗ thiếu góc

- **Đủ số bài, nhưng có hai bài yếu (M4, M7).** M7 (Atari) ngoài mạch "game thời gian thực" của Long, chỉ nối nhờ CH03. M4 phụ thuộc một câu chưa có nguồn.
- **Góc dự phòng chưa dùng, đều có trong script:** (a) CH14: AlphaStar chơi ẩn danh trên máy chủ chính thức, đạt hạng Grandmaster, cao hơn khoảng 99,8% người chơi xếp hạng, người gặp nó không biết mình đấu với máy (SỰ KIỆN, 10/2019); (b) CH12: độ trễ khoảng 350 mili-giây giữa lúc nhìn và lúc hành động; (c) CH09: bài toán phần thưởng đến muộn (hàng chục nghìn hành động, chỉ cuối ván mới biết thắng thua); (d) CH16: 08/2017, máy một chọi một thắng Dendi ở The International; (e) CH20–21: bốn ngày mở cửa, 7.215 thắng – 42 thua ở các ván đối đầu, và hơn 35 nghìn ván hợp tác (người chơi cùng đội với máy). Góc (a) mạnh hơn M7, và là phương án thay thế tôi khuyên nếu cắt M7 hoặc M2.
- **Không dùng được:** tỉ số từng ván ở TI 2018 (nguồn không nêu); chiến thuật MaNa dùng để thắng (script ghi "chưa đối chiếu nguồn").
