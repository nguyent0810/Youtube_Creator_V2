# T6 — 8 Short gắn Long `mim-ai-chat-privacy` (Long lên Thứ Hai 23/11/2026 20:00) — bản 1, chờ duyệt cổng pha 1

Người viết: agent T6, 20/10/2026. Pha 1: chỉ viết file, chưa dựng, chưa đăng, chưa sửa `state.sqlite`. Spec nằm ở `docs/pm/tickets/2026-10-20-mim-nov/specs-T6/` (chưa ghi vào `data/stier/specs`).

## 0. Kết luận ngắn

- **Đủ 8 bài.** Không bài nào dùng khung "mẹo". Đã loại hai góc vì rơi vào khung mẹo (mục 6).
- **Tỉ lệ 60/40:** 5 bài SỐ/SỰ KIỆN có ngày hoặc con số, 3 bài THỬ (cơ chế, lời hãng tự viết, sơ đồ).
- **Chỗ yếu nhất: bài 8 `mim-ba-nga-tin-nhan`** (kết luận "chỉ hai ngả có công tắc" là tổng hợp của Long, chưa có factcheck cho từng hãng) và **bài 2** (cơ chế, chưa có nguồn sơ cấp). Cần kiểm ở mục 5 trước khi dựng.
- **Thiếu nền kiểm chứng:** `data/long/mim-ai-chat-privacy/` **chưa có `factcheck.md`**, `script.md` tự ghi "bản 1, chờ kiểm chứng" kèm 10 mục "Cần kiểm chứng". Mọi số dưới đây lấy từ `script.md` (đã ghi ✔ ở mục nào) và các URL trong `spec.json` của Long. Phải đối chiếu lại khi Long có factcheck.
- **Bài mẫu để chủ kênh duyệt trước khi làm hàng loạt:** bài 1 `mim-4500-chat-tren-google` (sự kiện có ngày + số, khuôn đã thắng, gắn thẳng cold open của Long).

## 1. Lịch (giờ VN, lấy từ `data/shorts_slots.json`; `scripts/shorts_grid.py 2026-11-20 2026-11-23 --channel MIM --free` ngày 20/10: 20–23/11 trống cả 5 slot mỗi ngày)

Long `long-mim-ai-chat-privacy` (state.sqlite: `2026-11-23T13:00:00Z` = 23/11 20:00 VN, `ejsjefnJQbI`, stage `published`). Ngày thường dùng slot **11:30 + 19:00**. Ngày có Long dùng **11:30 + 17:00** (cần 2 bài để đủ 8 trong 4 ngày; 19:00 sát giờ Long nên bỏ, 17:00 vẫn cách Long 3 giờ). Nếu muốn xa Long hơn: đổi 17:00 thành 06:30. Không quá 2 Short/ngày.

| # | Ngày | Giờ | Slug | Tiêu đề (rút gọn) | Nhãn | Cảnh (M clip · D số liệu · G sơ đồ · T chữ) |
|---|---|---|---|---|---|---|
| 1 | T6 20/11 | 11:30 | `mim-4500-chat-tren-google` | Hơn 4.500 cuộc trò chuyện ChatGPT từng hiện công khai trên Google | SỰ KIỆN | MDGTGDM |
| 2 | T6 20/11 | 19:00 | `mim-may-chi-doc-khong-hoc` | Trong lúc trò chuyện, chatbot không học gì cả | THỬ (cơ chế) | MGMTDGT |
| 3 | T7 21/11 | 11:30 | `mim-samsung-ba-lan-trong-thang` | Ba lần trong một tháng, kỹ sư Samsung đưa dữ liệu nội bộ vào ChatGPT | SỰ KIỆN | MDGDGMT |
| 4 | T7 21/11 | 19:00 | `mim-gemini-nguoi-doc-3-nam` | Google viết thẳng: một phần cuộc trò chuyện với Gemini có người đọc, giữ tới 3 năm | THỬ (lời hãng tự viết) | TGMDMM |
| 5 | CN 22/11 | 11:30 | `mim-chat-5-nam-hay-30-ngay` | Giữ 30 ngày hay 5 năm: từ 28/08/2025, người dùng gói cá nhân của Claude phải tự chọn | SỐ | MDGDTM |
| 6 | CN 22/11 | 19:00 | `mim-y-chan-chatgpt-2023` | Ý chặn ChatGPT gần một tháng năm 2023: lý do là dữ liệu người dùng | SỰ KIỆN | MDGMD |
| 7 | T2 23/11 | 11:30 | `mim-luat-du-lieu-ca-nhan-2026` | Luật Bảo vệ dữ liệu cá nhân có hiệu lực từ 01/01/2026: từ nghị định lên thành luật | SỰ KIỆN | TMDDGM |
| 8 | T2 23/11 | 17:00 | `mim-ba-nga-tin-nhan` | Tin nhắn gửi chatbot đi ba ngả: trí nhớ, dữ liệu huấn luyện, người đọc. Chỉ hai ngả có công tắc | THỬ (sơ đồ) | MGDMGT |

- **Thứ tự:** hai bài cùng loại không đứng liền (bài 1 và 3 đều "lộ dữ liệu" nên cách bài 2; bài 3 và 6 đều chuyện 2023 nên cách bài 4, 5). Bài 8 (tổng quan ba ngả) đặt cuối, sát Long nhất.
- **Chống nhàm khuôn:** mỗi cặp kề nhau khác thứ tự và loại cảnh; cảnh đầu luân phiên kinetic có clip nền (1, 3, 6), kinetic cửa sổ video (2, 5, 8), slam (4, 7).
- **Không dùng cảnh `table` (bảng tra tự dò):** bảng thời hạn giữ dữ liệu (30 ngày / 72 giờ / 3 năm / 5 năm) lặp lại chính số của bài 4 và 5, nên trùng góc; bảng "ba ngả × công tắc" chưa kiểm từng hãng.
- Không bài nào gắn Short vào ngày 20–23/11 của kênh khác; các ticket T4–T9 không đè ngày của T6 (T5 17–19/11, T7 24–26/11).

## 2. Từng bài

Quy ước: câu mở ≤ 9 chữ (đếm từ cách nhau bởi dấu cách); câu chốt quay lại ý mở, không câu hỏi cuối, không mời xem Long trong lời đọc (mô tả có "Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11)"). Số bằng chữ khi nhỏ, chữ số khi là ngày/năm. Ngày/giờ đọc ước 4 âm tiết/giây.

### 1 · `mim-4500-chat-tren-google` — SỰ KIỆN, bài mẫu (~34 s)
- **Câu mở (9 chữ):** "Bốn nghìn rưỡi cuộc trò chuyện hiện trên Google."
- **Insight duy nhất:** không ai bị hack: người dùng tự bấm chia sẻ rồi bật một ô cho công cụ tìm kiếm thấy.
- **Số + nguồn:** hơn 4.500 cuộc trò chuyện (Fast Company, qua Search Engine Journal / TechRadar 07–08/2025) và 31/07/2025 OpenAI gỡ tính năng: `data/long/mim-ai-chat-privacy/script.md` CH00; URL `https://www.searchenginejournal.com/openai-is-pulling-shared-chatgpt-chats-from-google-search/552671/`. **Cần kiểm** (mục 5).
- **Câu chốt:** "Bốn nghìn rưỡi cuộc trò chuyện kia không bị đánh cắp. Chúng nằm sau một cánh cửa mà chính chủ đã mở."
- **Không trùng:** MIM chưa có Short nào về quyền riêng tư của chatbot (mục 3). Gần nhất `mim-sieu-cong-cu-tim-kiem` (ChatGPT không phải công cụ tìm kiếm): khác hẳn góc.

### 2 · `mim-may-chi-doc-khong-hoc` — THỬ (cơ chế, không ngày) (~34 s)
- **Câu mở (9 chữ):** "Trong lúc trò chuyện, chatbot không học gì cả."
- **Insight duy nhất:** lúc trò chuyện trọng số đứng yên; máy đọc lại cả cuộc trò chuyện mỗi lần trả lời; cuộc mới thì giấy trống; việc dữ liệu có được dùng để dạy bản sau là câu hỏi khác.
- **Số + nguồn:** không có con số. Cơ chế lấy từ `script.md` CH01; câu "dữ liệu có thể dùng để huấn luyện" dẫn trang OpenAI *How your data is used to improve model performance* (✔ #3 trong script). **Cần kiểm** nguồn kỹ thuật cho phần "cắt/tóm tắt" (mục 5).
- **Câu chốt:** "Trong cuộc trò chuyện, máy không học. Nó chỉ đọc."
- **Không trùng:** `mim-ai-doan-chu` (ChatGPT đoán chữ tiếp theo) nói cách sinh chữ, bài này nói việc không học lúc chat: khác câu hỏi con.

### 3 · `mim-samsung-ba-lan-trong-thang` — SỰ KIỆN (~37 s, hơi dài)
- **Câu mở (8 chữ):** "Một tháng, ba lần dán dữ liệu nội bộ."
- **Insight duy nhất:** nỗi lo của công ty không phải AI học ngay mà là dữ liệu đã nằm ở máy chủ bên ngoài, khó lấy lại, khó xoá.
- **Số + nguồn:** 04/2023, ba lần trong khoảng một tháng, đầu 05/2023 tạm cấm: `script.md` CH05 (đã sửa theo kiểm chứng vòng 1 ngày 09/10: Bloomberg 02/05/2023, qua The Register); URL `https://www.theregister.com/2023/05/02/samsung_generative_ai_ban/`. **Cần kiểm** phạm vi lệnh cấm (mục 5).
- **Câu chốt:** "Chỉ ba lần trong một tháng, và một công ty lớn đã tạm cấm cả công cụ."
- **Không trùng:** chưa có Short nào về Samsung/lộ dữ liệu công ty trong 160 Short MIM.
- **Rủi ro độ dài:** ước ~139 âm tiết (> 130). Khi đo giọng thật mà > 36 s thì cắt "Một người khác dán ghi chép một cuộc họp".

### 4 · `mim-gemini-nguoi-doc-3-nam` — THỬ (khuôn "hãng tự viết", mở bằng lời của chính hãng) (~31 s)
- **Câu mở (9 chữ):** "Google viết thẳng: có người đọc một phần chat."
- **Insight duy nhất:** một phần cuộc trò chuyện Gemini được người đánh giá xem xét, và những cuộc đã xem không bị xoá khi xoá lịch sử, giữ tới ba năm.
- **Số + nguồn:** "tới 3 năm" ✔ #5 trong script (Gemini Apps Privacy Hub, đọc 09/10/2026), URL `https://support.google.com/gemini/answer/13594961?hl=en`. Câu trích dịch "Xin đừng nhập thông tin bí mật mà bạn không muốn người đánh giá nhìn thấy" ✔ cùng trang, nhãn TRÍCH DỊCH trên màn hình.
- **Câu chốt:** "Một phần chat có người đọc, và chính hãng nói thẳng điều đó."
- **Không trùng:** là lời khuyên của hãng, **không** phải lời khuyên của kênh ("không mẹo"); không nói "Google kém an toàn hơn".

### 5 · `mim-chat-5-nam-hay-30-ngay` — SỐ (~29 s)
- **Câu mở (9 chữ):** "Giữ ba mươi ngày hay năm năm: bạn chọn."
- **Insight duy nhất:** từ 28/08/2025 người dùng gói cá nhân của Claude tự chọn có cho huấn luyện hay không; đồng ý thì giữ tới 5 năm, không thì vẫn 30 ngày.
- **Số + nguồn:** 28/08/2025, 5 năm / 30 ngày ✔ #4 trong script (Anthropic, *Updates to our consumer terms*), URL `https://www.anthropic.com/news/updates-to-our-consumer-terms`. **"Hơn 60 lần" là kênh tự tính:** 5 năm ≈ 1.825 ngày ÷ 30 ngày ≈ 60,8; ghi rõ "KÊNH TỰ TÍNH" trên màn hình và trong mô tả.
- **Câu chốt:** "Ba mươi ngày hay năm năm, là lựa chọn của bạn."
- **Không trùng:** khác bài 4 (hãng khác, ý khác: quyền chọn vs người đọc). Biểu đồ cột vẽ đúng tỉ lệ 30 : 1.825 ngày (cột 30 ngày rất mỏng: đúng như dữ liệu).

### 6 · `mim-y-chan-chatgpt-2023` — SỰ KIỆN (~33 s)
- **Câu mở (9 chữ):** "Một quốc gia từng chặn ChatGPT gần một tháng."
- **Insight duy nhất:** cơ quan bảo vệ dữ liệu của Ý chặn tạm thời ChatGPT từ 31/03 đến 28/04/2023 vì chuyện dữ liệu người dùng.
- **Số + nguồn:** 31/03/2023, 28/04/2023, hai lý do (thiếu thông báo đầy đủ; thiếu cơ sở pháp lý để thu thập dữ liệu hàng loạt cho huấn luyện): `script.md` CH05 + ghi chú #9 (nguồn thứ cấp: privacylaws.com, Fox Business, The Decoder), URL `https://www.privacylaws.com/news/italy-s-garante-imposes-and-then-withdraws-a-ban-on-chatgpt/`. **28 ô lịch = 28 ngày là kênh tự tính** (31/03 → 28/04). **Cần kiểm** văn bản gốc của Garante (mục 5).
- **Câu chốt:** "Gần một tháng, vì một câu hỏi về dữ liệu của người dùng."
- **Không trùng:** không có Short nào về Ý/Garante. Không nhắc "25/04/2023 OpenAI ra mắt nút tắt lịch sử" để giữ một insight (dự phòng R3, mục 6).

### 7 · `mim-luat-du-lieu-ca-nhan-2026` — SỰ KIỆN (~33 s)
- **Câu mở (9 chữ):** "Từ 2026, dữ liệu cá nhân có luật riêng."
- **Insight duy nhất:** Luật Bảo vệ dữ liệu cá nhân (91/2025/QH15) thông qua 26/06/2025, hiệu lực 01/01/2026, nâng việc này từ nghị định lên luật, với nguyên tắc đúng phạm vi, đúng mục đích.
- **Số + nguồn:** ✔ #7, #10 trong script (LuatVietnam, PwC 01/2026), URL `https://luatvietnam.vn/tin-van-ban-moi/da-co-luat-bao-ve-du-lieu-ca-nhan-2025-so-91-2025-qh15-186-102925-article.html`. **Không dùng** "đạo luật đầu tiên" và "phạt tới 10 lần khoản thu" (nguồn thứ cấp, chưa kiểm điều luật gốc). Lời đọc không nhắc năm 2023 và "Nghị định mười ba" để giữ nhịp; năm 2023 và "Nghị định 13" chỉ hiện trên màn hình (timeline).
- **Câu chốt:** "Từ năm 2026, dữ liệu cá nhân ở Việt Nam đã có một đạo luật riêng."
- **Không trùng:** chưa có Short MIM nào về luật dữ liệu. Mô tả có "Nội dung giáo dục, không phải tư vấn pháp lý."

### 8 · `mim-ba-nga-tin-nhan` — THỬ (sơ đồ ba ngả) (~25 s)
- **Câu mở (8 chữ):** "Một tin nhắn, ba ngả đi khác nhau."
- **Insight duy nhất:** ba ngả (trí nhớ, dữ liệu huấn luyện, người đánh giá), hai ngả đầu có công tắc, ngả thứ ba không.
- **Số + nguồn:** không có con số lớn. Khung "ba ngả" và "công tắc" lấy từ `script.md` CH00 + CH07; nguồn: help.openai.com *Data controls in ChatGPT*, Gemini Privacy Hub, Anthropic (URL trong spec). **Cần kiểm kỹ** (mục 5).
- **Câu chốt:** "Một tin nhắn, ba ngả, và chỉ hai ngả có công tắc."
- **Không trùng:** là bản đồ tổng, chỉ nhắc tên ba ngả, không lặp số hay sự kiện của bài 1–7. Có chồng nhẹ với bài 4 (ngả người đọc) và bài 5 (ngả huấn luyện): nếu duyệt thấy trùng, thay bằng R1 (mục 6).
- Sơ đồ là **mô phỏng dựng bằng chữ**, ghi trong mô tả; không chụp giao diện thật.

## 3. Bảng đối chiếu trùng

### 3a. Với Short MIM hiện có (state.sqlite `kind='short' channel='MIM'`: 160 hàng; lọc theo spec trong `data/stier/specs/mim-*.json` + script các Long)

Từ khoá đã quét: samsung, gemini, anthropic/claude, openai, quyền riêng tư, dữ liệu cá nhân, garante/Ý chặn, chia sẻ/link, huấn luyện, trọng số, tờ giấy, "bốn nghìn rưỡi / 4.500". Kết quả: **không Short nào về quyền riêng tư của chatbot**. Hàng gần nhất:

| Short hiện có | Bài T6 gần nhất | Vì sao không trùng |
|---|---|---|
| `mim-ai-doan-chu` ChatGPT đoán chữ tiếp theo | 2 | Nói cách sinh chữ; bài 2 nói máy không học lúc chat, đọc lại cả cuộc trò chuyện |
| `mim-sieu-cong-cu-tim-kiem` (luật sư, ChatGPT không phải công cụ tìm kiếm) | 1 | Chung chữ "tìm kiếm" nhưng khác sự kiện, khác ý |
| `mim-chatgpt-700-trieu` (700 triệu người dùng) | 1, 3 | Quy mô sử dụng, không phải dữ liệu |
| `mim-noam-brown-nghi-lau-hon` (nhắc OpenAI) | 1, 6 | Chỉ chung tên hãng |
| `mim-9-tren-10-hoc-sinh-dung-ai` (PISA chatbot) | 7 | Chung "Việt Nam + chatbot" nhưng khác số liệu và ý |
| `mim-captcha-cham-diem-ngam` (tag "quyền riêng tư") | — | Tag chung, nội dung CAPTCHA |
| 4 Short giọng giả / lừa đảo (`mim-bo-xac-thuc-giong-noi`, `mim-quet-mat-10-trieu`, …) | 8 | Bảo mật tài khoản, khác ngả dữ liệu chat |

Long MIM có trùng chủ đề không: Long `mim-ai-feed` (bảng tin đề xuất) chỉ chung chữ "quyền riêng tư" trong ghi chú; Long `mim-ai-gpu` có "trọng số" nhưng nói con chip, không trùng bài 2.

### 3b. Với T4–T9 khác (đã đọc `specs-T4..T9` và `T5/T7-ke-hoach.md` ngày 20/10)

- T4 (GPU, 8 file), T5 (Watson, 5), T7 (poker, 4), T8 (khuôn mặt, 8), T9 (game, 5): không file nào nhắc Samsung, Gemini, Anthropic, quyền riêng tư, luật dữ liệu, Ý chặn, chia sẻ cuộc trò chuyện. **Không trùng góc.**
- T8 là chủ đề gần nhất về "dữ liệu cá nhân" (khuôn mặt). Bài 7 của T6 (luật dữ liệu) và bài T8 `mim-vi-sao-ung-dung-bat-chop-mat` không chung ý; nếu T8 sau này thêm "luật dữ liệu cá nhân" thì giữ ở T6 và loại ở T8.
- **Clip:** 17 clip T6 không trùng clip nào trong `specs-T4..T9` (đã so id; clip có trong `motion/hf/assets/clips/index.json`, đều có bản dọc).
- **Slot:** T6 dùng 20–23/11, không ngày nào chung với T4/T5/T7/T8/T9.

## 4. Cách tự kiểm (build.py không có cờ `--lint-only`)

`python motion/stier/build.py <slug> --no-render` vẫn chạy TTS (tốn thời gian, chạm cache giọng), nên **không chạy ở pha 1**. Thay bằng `docs/pm/tickets/2026-10-20-mim-nov/specs-T6/_selfcheck.py` (chỉ đọc, không dựng): import `mix_lint`, `scene_mode`, `norm`, `ANCHORS` từ `motion/stier/build.py` rồi kiểm:

- mọi mốc `[câu, "chữ"(, lần, lệch)]` có đúng chữ trong câu (sai là lỗi cứng ở build thật);
- 55–135 chữ, câu mở ≤ 9 chữ, không kết bằng "?", không chữ "mẹo", không mời xem video trong lời, tiêu đề ≤ 100 ký tự;
- dòng phụ counter/slam/chart ≤ 52 ký tự, counter không hiện "năm", không "~", prefix counter không chữ số;
- `mix_lint` (phải có M, D, G; thuần chữ ≤ 35%; một kiểu ≤ 60%; không 3 cảnh liền cùng kiểu; cảnh ≤ 11 s) trên giờ **ước lượng** 4 âm tiết/giây + `tts.pauses`.

Kết quả ngày 20/10: **0 lỗi trên 8 spec**. Phần chưa kiểm được ở pha 1 (cần build thật): giờ thật của giọng, chữ kinetic có tràn khung 980 px không (không đặt `size` tay nên engine tự co), `hold_open`, cảnh `quote` có clip nền, mix lint lần cuối trên giờ đo thật.

## 5. Cần kiểm (trước khi dựng)

1. **Không có `factcheck.md` cho Long.** Toàn bộ số của 8 Short dựa vào `script.md` bản 1. Cần chạy lại các mục "Cần kiểm chứng" (1, 4, 5, 6, 7, 9, 10) khi Long (T-factcheck) xong; sửa Short theo Long, không bịa.
2. **Trang chính sách có thể đã đổi** từ lần đọc 09/10/2026 (OpenAI, Google, Anthropic). Đọc lại trước khi dựng bài 4, 5, 8.
3. **Bài 1:** "hơn 4.500" và nội dung (hồ sơ xin việc, tên thật, mã nguồn) mới qua SEJ/TechRadar; chưa đọc bài gốc Fast Company. Không dùng câu trích của Dane Stuckey (chưa có nguyên văn).
4. **Bài 2:** "cuộc trò chuyện quá dài thì phần đầu bị cắt hoặc tóm tắt" là cách làm phổ biến, tuỳ ứng dụng; chưa có trang sơ cấp. Ngoài ra, câu mở "không học gì cả" đúng với trọng số; tính năng trí nhớ (đọc lại ghi chú đã lưu) là chuyện khác: nên có nguồn rõ hoặc đổi "chatbot" thành "mô hình" nếu bị phản biện.
5. **Bài 3:** phạm vi lệnh cấm Samsung ("máy tính của công ty" so với một bộ phận), "bộ phận bán dẫn" (script ghi Device Solutions/ Device eXperience chưa chốt). Lời đọc chỉ nêu 2 trong 3 lần (mã nguồn, ghi chép họp), không nêu lần thứ ba.
6. **Bài 4:** nguyên văn tiếng Anh câu của Google để dịch sát; tên công tắc "Keep Activity" không còn trong lời đọc (đã bỏ để tránh sai tên).
7. **Bài 5:** hạn 08/10/2025 của Anthropic đã qua; "gói cá nhân" gồm những gói nào; loại trừ Work/API/Gov/Education (đã đưa vào mô tả, không đọc trong lời).
8. **Bài 6:** văn bản gốc của Garante (31/03/2023, 28/04/2023) chưa có URL sơ cấp trong kho; hiện chỉ có nguồn thứ cấp.
9. **Bài 7:** đọc điều luật gốc cho "đúng phạm vi, đúng mục đích" và ngày thông qua/hiệu lực; xác nhận NĐ 13/2023 bị thay thế (NĐ 356/2025) nếu muốn nhắc.
10. **Bài 8 (rủi ro cao nhất):** "chỉ hai ngả có công tắc" và "ngả người đọc không tắt hẳn được" cần đối chiếu từng hãng; nếu không kiểm được, đổi câu 4–5 thành "theo trang trợ giúp của OpenAI/Google…" hoặc thay bài bằng R1.
11. **Clip:** chưa chạy `motion/long/clip_sheet.py`; tên clip lấy từ `clips/index.json`, chưa xem hình. Phải xem bảng clip để loại cảnh có logo, tên công ty, ticker, nội dung trên màn hình (đặc biệt `pexels:8888530`, `7579576`, `7341928`, `12910159`, `4823889`, `7439142` có màn hình thiết bị).
12. **TTS:** bảng `say` đã có Gu-gồ, Giê-mi-nai, Ô-pần ây ai, En-thờ-ro-píc, Clốt, Xam-xung, Blum-bớc, hách; nghe thử "Ý" (nước Ý) và "ChatGPT" (chát gi pi ti) ở lần dựng đầu, "Nghị định" không nằm trong lời bài 7.
13. **Link Long trong mô tả** lấy từ state (`ejsjefnJQbI`); nếu Long bị thay video thì cập nhật cả 8 mô tả.
14. **Độ dài:** bài 3 ước 37 s, bài 1 ước 34 s (> mục tiêu ~35 s thì cắt câu phụ); số ước từ 4 âm tiết/giây, chưa đo giọng.

## 6. Chỗ thiếu góc, dự phòng, và góc đã bỏ

Đủ 8 bài, không độn. Tuy vậy 3 bài có góc mỏng hơn: **bài 2** (cơ chế, không ngày), **bài 8** (tổng quan, chồng nhẹ bài 4 và 5), **bài 7** (nguồn thứ cấp). Nếu cần cắt, bỏ theo thứ tự 8 → 2 → 7.

**Dự phòng (chưa viết spec):**
- **R1** "Trò chuyện tạm thời không biến mất ngay": OpenAI giữ bản sao tối đa 30 ngày, Google giữ 72 giờ (script CH04, ✔ #5 và #8). Dùng thay bài 8.
- **R2** "Xoá một mục trí nhớ, nhật ký vẫn giữ tối đa 30 ngày" (OpenAI, ✔ #2). Số 30 ngày trùng R1, chọn một.
- **R3** "25/04/2023: OpenAI ra mắt cách tắt lịch sử trò chuyện" (OpenAI blog, CNBC): sự kiện có ngày, nhưng chung câu chuyện với bài 6.
- **R4** "Gói doanh nghiệp mặc định không dùng để huấn luyện, gói cá nhân thì khác" (script CH03 ✔ #3): hợp với bài 5 nhưng chồng ý.

**Đã bỏ vì khung "mẹo":** (a) "năm thứ không nên dán vào chatbot" (CH07); (b) "bật tắt từng công tắc: bước 1, 2, 3" (hướng dẫn thao tác, lại phụ thuộc tên nút và giao diện thật). Hai góc này nên để Long làm.

## 7. Ghi chú cho pha 2

- Bài mẫu duyệt trước: bài 1. Sau duyệt mới dựng 7 bài còn lại, **một tiến trình dựng tại một thời điểm** (khoá `output/.render.who`), chạy nền qua `scripts/run_chain.py`.
- Trước khi dựng: chạy `clip_sheet.py` cho 17 clip, đối chiếu lại số với factcheck của Long, kiểm trang chính sách một lần nữa.
- Sau khi đăng riêng tư + hẹn giờ: gắn "Video liên quan" (link Long) trong Studio nếu cần; retro bằng subagent.
- Mô tả mỗi bài đã có: nguồn, nhãn "kênh tự tính" (bài 5, 6), "mô phỏng dựng bằng chữ" (bài 8), lời nhắc cài đặt có thể khác theo gói/vùng/phiên bản (bài 1–5, 8), "Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels" và dòng "Bản đầy đủ".
