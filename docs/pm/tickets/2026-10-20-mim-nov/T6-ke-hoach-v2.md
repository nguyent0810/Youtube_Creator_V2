# T6 v2 — 8 Short lane `mim-ai-chat-privacy` (Long lên Thứ Hai 23/11/2026 20:00), viết lại theo khung truyện

Người viết: agent T6 v2, 20/10/2026. **Pha 1: chỉ viết file.** Chưa dựng, chưa render, chưa đăng, không sửa `state.sqlite` (chỉ đọc `mode=ro`), `data/stier/specs` hay ticket khác. Spec: `docs/pm/tickets/2026-10-20-mim-nov/specs-v2-T6/<slug>.json` (+ `_selfcheck.py`). Bản đầu (`T6-ke-hoach.md`, `specs-T6/`) giữ nguyên làm tham chiếu, **bị thay bằng bản này**.

## 0. Kết luận ngắn

- **Đủ 8 bài, bài nào cũng có người hoặc cơ quan thật + sự kiện có ngày + bước ngoặt.** Không bài nào là "chính sách hãng", không lời khuyên "nên/không nên", không nói hãng nào tốt/xấu (mỗi mệnh đề gắn nguồn trong câu hoặc trên màn hình; chỗ hãng/cơ quan khác nhau thì ghi "theo ...").
- **Bỏ hẳn các góc bản đầu chỉ có chính sách, không có chuyện:** Gemini giữ 3 năm, Claude 5 năm/30 ngày, trí nhớ/trò chuyện tạm thời, "ba ngả × công tắc", luật dữ liệu Việt Nam (không có người/xung đột, chỉ là điều khoản; để làm dự phòng R2 vì có sự kiện bỏ phiếu). Hai bài cũ giữ lại nhưng **kể lại bằng truyện**: 4.500 chat trên Google và Ý chặn ChatGPT; Samsung kể lại theo trình tự có ngày (và sửa một lỗi ngày của Long, mục 5).
- **Tự kiểm:** `specs-v2-T6/_selfcheck.py` (import `mix_lint`, `scene_mode`, `norm`, `ANCHORS` từ `motion/stier/build.py`, không chạy `build.py`): **0 lỗi trên 8 spec**. Đủ M D G; chữ thuần T 4–18% (≤ 35%); không 3 cảnh liền cùng kiểu; cảnh ≤ 11 s (giờ ước 4 âm tiết/giây); câu mở 8–9 chữ; 9–10 cảnh/bài; 96–116 chữ; ước 32–37 s.
- **Thiếu nền kiểm chứng:** `data/long/mim-ai-chat-privacy/` **chưa có `factcheck.md`** (script bản 1, chờ kiểm chứng). Số/ngày ở đây lấy từ nguồn sơ cấp hoặc báo đọc ngày 20/10 (bảng nguồn ở từng bài). Nhiều trang sơ cấp (openai.com, fastcompany.com, garanteprivacy.it, Mozilla, Engadget) **không tải được tự động** (403 hoặc lỗi DNS), nên phải đọc lại bản gốc trước pha 2 (mục 5).

## 1. Lịch (dòng 'T6 privacy' của `00-LICH-XEN-KE.md`; giờ gợi ý, chốt bằng `scripts/shorts_grid.py` ở pha 2)

| # | Ngày | Giờ | Slug | Câu mở (đếm chữ) | Người / tổ chức | Cảnh (M clip · D số liệu · G sơ đồ · T chữ) | Ước |
|---|---|---|---|---|---|---|---|
| 1 | T3 17/11 | 19:00 | `mim-chat-nguoi-la-20-3-2023` | "Năm 2023, người lạ hiện trong lịch sử chat." (9) | người dùng ChatGPT; OpenAI | M G T G D D M T M | ~35 s |
| 2 | T4 18/11 | 19:00 | `mim-samsung-ba-vu-truoc-khi-cam` | "Năm 2023, Samsung cho kỹ sư dùng ChatGPT." (8) | kỹ sư bán dẫn Samsung; The Economist Korea | M D D G M T G D M | ~33 s |
| 3 | T5 19/11 | 17:00 | `mim-chat-da-xoa-van-bi-giu` | "Người dùng xoá chat, thẩm phán bảo giữ lại." (9) | thẩm phán Ona Wang; Brad Lightcap | M D G D M D D T M | ~36 s |
| 4 | T6 20/11 | 19:00 | `mim-4500-chat-link-chia-se` | "Hơn bốn nghìn rưỡi chat hiện trên Google." (8) | phóng viên Fast Company; người dùng tự chia sẻ | M D D G T G D M M | ~34 s |
| 5 | T7 21/11 | 19:00 | `mim-y-chan-chatgpt-roi-toa-huy-phat` | "Năm 2023, nước Ý chặn ChatGPT gần một tháng." (9) | Garante (cơ quan dữ liệu Ý); toà Rome | M D G D D G M D T M | ~37 s |
| 6 | CN 22/11 | 19:00 | `mim-meta-ai-sua-xe-cong-khai` | "Anh hỏi chuyện sửa xe, ai cũng đọc được." (9) | một người đàn ông hỏi về sửa xe; Business Insider | M D G T M D G M T M | ~34 s |
| 7 | T2 23/11 | 17:00 | `mim-altman-khong-nhu-bac-si` | "Nói với ChatGPT không như nói với bác sĩ." (9) | Sam Altman; Theo Von | M D M G M G T D M | ~35 s |
| 8 | T4 25/11 | 19:00 | `mim-deepseek-kho-chat-khong-mat-khau` | "Một kho dữ liệu chat không cần mật khẩu." (9) | nhóm Wiz Research (Gal Nagli) | M D G M D D G T M | ~32 s |

- **Lưu ý lịch:** (a) dòng 19/11 17:00 trong lịch ghi "Long 20:00" ở dòng T6, còn `00-NGUON-NOI-DUNG.md` và `state.sqlite` đặt Long Watson ở 19/11 và Long chat-privacy ở **23/11 13:00Z = 20:00 VN**. Tôi coi ghi chú 19/11 là của Watson; **cần PM xác nhận**. (b) Ba Short ra trước Long (17–19/11), năm Short ra từ ngày Long; mô tả có "Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11)" (video_id lấy từ state). (c) Không quá 2 Short/ngày; mỗi ngày một Short T6.
- **Thứ tự chống nhàm:** hai bài gần nhau về đề khác nhau (lỗi hệ thống → công ty → toà → link chia sẻ → cơ quan → giao diện → lời CEO → cơ sở dữ liệu mở). Bài 3 và 7 cùng bối cảnh vụ New York Times nhưng cách 4 ngày; bài 1 và 5 cùng dính vụ lộ ngày 20/03 nhưng cách 4 ngày; bài 4 và 6 cùng "đăng nhầm" nhưng cách 2 ngày và khác sự kiện.
- **Khuôn:** cả 8 bài mở bằng sự kiện/chuyện có người hoặc con số, kết quay về câu mở bằng một bước ngoặt, không câu hỏi cuối, không mời xem Long trong lời đọc. Hướng "bài thử" (40%): bài 6 (chi tiết người sửa xe làm câu mở), bài 7 (mở bằng câu so sánh với bác sĩ), bài 8 (mở bằng "không cần mật khẩu").

## 2. Từng bài

Quy ước: câu mở đếm chữ cách nhau bằng dấu cách (năm 4 chữ số tính 1 chữ, như bài mẫu "Năm 1993, ba kỹ sư..."); số nhỏ đọc bằng chữ, năm viết số; nhãn "TRÍCH DỊCH" cho mọi câu trích; "kênh tự tính" ghi rõ.

### 1 · `mim-chat-nguoi-la-20-3-2023` (17/11 19:00)
- **Sự kiện có ngày:** 20/03/2023, lỗi trong thư viện mã nguồn mở redis-py: yêu cầu bị huỷ giữa chừng khiến kết nối trả nhầm dữ liệu; một số người dùng thấy **tiêu đề** chat của người dùng khác; OpenAI tạm ngừng ChatGPT.
- **Bước ngoặt:** 1,2% người đăng ký gói trả phí hoạt động trong 9 giờ có thể bị lộ tên, địa chỉ, 4 số cuối thẻ; OpenAI nói số người thực sự bị lộ là cực kỳ thấp. Câu chốt quay về mở: "...người lạ hiện trong lịch sử của bạn."
- **Số + nguồn:** 20/03/2023, 1,2%, 9 giờ: bài giải trình OpenAI "March 20 ChatGPT outage" (24/03/2023; trang 403) đối chiếu The Hacker News, Help Net Security, Infosecurity Magazine. **Chỉ nói "tiêu đề", không nói cả nội dung chat.**
- **Không trùng:** không Short MIM nào về lỗi lộ dữ liệu; không nhắc Ý ở bài này (để bài 5).

### 2 · `mim-samsung-ba-vu-truoc-khi-cam` (18/11 19:00)
- **Sự kiện có ngày:** 11/03/2023 bộ phận bán dẫn Samsung được dùng ChatGPT; 30/03/2023 The Economist Korea đưa tin ba vụ (dán mã lỗi thiết bị bán dẫn, dán mã nhờ tối ưu, đưa bản ghi cuộc họp để lấy biên bản); đầu 05/2023 thông báo nội bộ tạm cấm (Bloomberg 02/05/2023).
- **Bước ngoặt:** mở cửa 11/03, tạm cấm chưa đầy hai tháng sau. **Samsung không xác nhận chi tiết các vụ** (The Register 02/05/2023): có một câu riêng trong lời đọc và cảnh slam.
- **Nguồn:** The Register 02/05/2023 (đã đọc); The Economist Korea 30/03 qua Gigazine, Cybersecurity News, HCAMag (thứ cấp). **Cần tìm bài gốc tiếng Hàn.** "Chưa đầy hai tháng" = 11/03 → 02/05 (52 ngày), kênh tự tính.
- **Không trùng:** cùng tên Samsung với bản đầu nhưng đổi hẳn trục: bản đầu "tháng 4 / ba lần trong tháng / máy chủ ngoài khó xoá", bản này theo mốc ngày thật và nói rõ Samsung không xác nhận.

### 3 · `mim-chat-da-xoa-van-bi-giu` (19/11 17:00)
- **Sự kiện có ngày:** 13/05/2025, thẩm phán Ona T. Wang (SDNY), trong vụ The New York Times và các báo kiện OpenAI, ra lệnh giữ lại dữ liệu đầu ra ChatGPT vốn sẽ bị xoá, kể cả chat đã xoá; OpenAI phản đối công khai (đơn 03/06/2025; COO Brad Lightcap: lệnh "rộng quá mức và không cần thiết", trích dịch); nghĩa vụ giữ thêm chấm dứt từ 26/09/2025 (thoả thuận duyệt 09/10/2025), bản đã giữ trước đó vẫn còn, trừ vài ngoại lệ.
- **Bước ngoặt:** người dùng xoá chat nhưng bản đã giữ trong khoảng tháng 5–9/2025 vẫn còn. Mặc định ba mươi ngày là theo OpenAI.
- **Nguồn:** Malwarebytes (06/2025), CyberInsider, Bloomberg Law, Engadget (thứ cấp, đã đọc kết quả tìm kiếm); trang OpenAI "response to NYT data demands" 403. **Cần đọc bản gốc OpenAI và lệnh toà (docket 1:23-cv-11195).** "Hàng trăm triệu người dùng" lấy từ TechCrunch (25/07/2025), cần kiểm.
- **Không trùng:** bản đầu không có bài này; không Short MIM nào về vụ New York Times. Bài `mim-phat-5000-do-va-nhung-la-thu` là luật sư bị phạt vì án lệ AI bịa, khác hẳn.

### 4 · `mim-4500-chat-link-chia-se` (20/11 19:00)
- **Sự kiện có ngày:** cuối 07/2025 Fast Company gõ tìm kiếm trên Google, thấy **hơn 4.500** link chia sẻ ChatGPT (tên thật, hồ sơ xin việc, tài liệu công việc); 31/07/2025 OpenAI gỡ tính năng, gọi nó là "thử nghiệm ngắn ngủi" (trích dịch, theo Search Engine Journal).
- **Bước ngoặt:** không ai bị hack; chính người dùng bấm chia sẻ rồi tích thêm ô cho công cụ tìm kiếm thấy (mặc định chỉ người có link mở được).
- **Nguồn:** Search Engine Journal 31/07/2025 (đã đọc: "over 4,500", hai bước, câu của OpenAI). Bài gốc Fast Company không tải được: **cần đọc**. **Sửa lệch của Long/bản đầu:** SEJ ghi câu trên là của **OpenAI**, không nêu Dane Stuckey; không dùng tên Stuckey.
- **Không trùng:** tên bài cũ `mim-4500-chat-tren-google` thay bằng slug mới; khác bài 6 (Meta, tháng 6/2025) ở sự kiện, hãng, cơ chế.

### 5 · `mim-y-chan-chatgpt-roi-toa-huy-phat` (21/11 19:00)
- **Sự kiện có ngày:** quyết định 30/03/2023 (công bố 31/03) Garante tạm hạn chế OpenAI ở Ý: thiếu thông báo cho người dùng, thiếu cơ sở pháp lý; 28/04/2023 ChatGPT trở lại; 20/12/2024 phạt 15 triệu euro (quyết định 02/11/2024), một lý do là không báo vụ lộ dữ liệu 2023; 18/03/2026 toà Rome huỷ khoản phạt, theo báo chí Ý vì thẩm quyền (lý do chi tiết chưa công bố đầy đủ).
- **Bước ngoặt:** bị chặn gần một tháng; ba năm sau khoản phạt bị huỷ. Cảnh lịch "28 ngày" (31/03 → 28/04) là **kênh tự tính**; slam "THẨM QUYỀN" ghi "lý do theo báo chí Ý".
- **Nguồn:** Teleborsa/LaPresse 20/12/2024; filodiritto, cybersecurity360, quifinanza (30/03/2023); diritto.it, tuttotech 23/03/2026 (thứ cấp). **Cần văn bản gốc Garante (n.112, n.755) và bản án 18/03/2026; cần xem Garante có kháng cáo hay không** (nếu có, đổi câu chốt).
- **Không trùng:** bản đầu chỉ có đoạn 2023 và cảnh lịch; bản này thêm 2024 và 2026 (bước ngoặt mới). Cặp với bài 1 đã nói ở mục 1.

### 6 · `mim-meta-ai-sua-xe-cong-khai` (22/11 19:00)
- **Sự kiện có ngày:** 06/2025 ứng dụng Meta AI có dòng tin công khai Discover hiện chat người dùng đã đăng; Business Insider thấy nhiều bài trông như đăng nhầm, một người hỏi về sửa xe nói anh không định đăng công khai, có người viết "hãy giữ chuyện này riêng tư" vào bài đã đăng; Meta: không gì lên dòng tin nếu không chọn đăng; Mozilla: giao diện không báo rõ; Meta thêm màn cảnh báo trước khi đăng.
- **Bước ngoặt:** câu mở "Anh hỏi chuyện sửa xe, ai cũng đọc được" → chốt "chỉ cách công khai hai lần bấm". Có đủ lời hai phía, không gọi bên nào xấu.
- **Nguồn:** kết quả tìm kiếm về Business Insider, Engadget, Mozilla Foundation (03/07/2025); các trang gốc 403/không tải được. **Cần đọc bài Business Insider gốc** (ngày, chi tiết người sửa xe, lời nhắn "keep this private") và Engadget. Chỉ ghi "06/2025" vì chưa có ngày chính xác.
- **Không trùng:** MIM chưa có Short về Meta AI.

### 7 · `mim-altman-khong-nhu-bac-si` (23/11 17:00)
- **Sự kiện có ngày:** theo TechCrunch (25/07/2025), trên podcast *This Past Weekend* của Theo Von, Sam Altman nói bác sĩ/luật sư/nhà trị liệu có đặc quyền pháp lý còn với ChatGPT thì "chúng tôi chưa tìm ra điều đó" (trích dịch); nếu có kiện tụng OpenAI hiện có thể phải đưa chat ra; ông gọi tình trạng "rất không ổn".
- **Bước ngoặt:** người đứng đầu OpenAI tự nói khoảng trống ấy; chốt quay về mở (bác sĩ có đặc quyền, ChatGPT thì chưa, theo chính Altman). **Không nhắc lệnh toà New York Times** để tránh trùng bài 3.
- **Nguồn:** TechCrunch 25/07/2025 (đã đọc), Qz (câu "required to produce", thứ cấp). **Cần kiểm:** ngày phát sóng tập podcast; nguyên văn ý "nhiều người kể chuyện riêng tư"; có thể đổi "Tháng bảy 2025" thành "Cuối tháng bảy" khi biết ngày.
- **Không trùng:** MIM chưa có Short về Altman/đặc quyền pháp lý. Đặt ngày 23/11 17:00 cùng ngày Long (cách 3 giờ).

### 8 · `mim-deepseek-kho-chat-khong-mat-khau` (25/11 19:00)
- **Sự kiện có ngày:** 29/01/2025 nhóm Wiz Research (bài của Gal Nagli) công bố một cơ sở dữ liệu ClickHouse của DeepSeek mở hoàn toàn, không cần xác thực, trên hai tên miền phụ của DeepSeek; có hơn một triệu dòng nhật ký gồm lịch sử trò chuyện, khoá bí mật, chi tiết hệ thống; Wiz báo ngay, DeepSeek nhanh chóng đóng lại.
- **Bước ngoặt:** "kho không cần mật khẩu nên chẳng ai phải phá khoá". Không nêu có ai khác đã vào hay chưa (Wiz không nêu).
- **Nguồn:** Wiz blog 29/01/2025 (**nguồn sơ cấp, đã đọc 20/10**). "Hơn một triệu" là "over 1 million log entries" của Wiz.
- **Không trùng:** không Short MIM nào về DeepSeek hay cơ sở dữ liệu mở (`mim-internet-lo`, `mim-captcha-*` chỉ chung chữ "mạng"/"bảo mật").

## 3. Bảng đối chiếu trùng

### 3a. Short MIM trong `state.sqlite` (`mode=ro`, kind='short', channel='MIM': **160 hàng**) và spec đã dựng `data/stier/specs`
Quét slug (state chỉ có slug) và nội dung spec theo từ khoá: samsung, garante, deepseek, altman, redis, meta ai, new york times, wiz, riêng tư, chatgpt. **Không Short nào trùng góc.**

| Short hiện có | Bài T6 v2 gần nhất | Vì sao không trùng |
|---|---|---|
| `mim-phat-5000-do-va-nhung-la-thu`, `mim-2000-quyet-dinh-toa-an`, `mim-ba-luan-an-khong-co-that`, `mim-sau-vu-an-khong-co-that` (án lệ AI bịa, luật sư) | 3, 5 | Cùng "toà + ChatGPT" nhưng nói AI bịa án lệ; T6 nói dữ liệu người dùng |
| `mim-chatgpt-700-trieu` (quy mô người dùng), `mim-sieu-cong-cu-tim-kiem` | 1, 4 | Quy mô / ChatGPT không phải công cụ tìm kiếm |
| `mim-teaser-hinton-x-quang` (nhắc báo New York Times phỏng vấn Hinton) | 3 | Chỉ chung tên báo, khác hẳn nội dung |
| `mim-teaser-mat-khau-gia-dinh`, `mim-4-tren-6-dich-vu`, `mim-bo-xac-thuc-giong-noi`, `mim-quet-mat-10-trieu`, `mim-lua-dao-1-tren-555`, `mim-hong-kong-cuoc-hop-gia` (giọng giả/lừa đảo) | 8 | Bảo mật tài khoản/giọng nói, không phải dữ liệu chat |
| `mim-captcha-cham-diem-ngam` (tag "quyền riêng tư") | — | Tag chung, nội dung CAPTCHA |
| `mim-noam-brown-nghi-lau-hon` (nhắc OpenAI) | 3, 4, 7 | Chỉ chung tên hãng |
| Long `mim-ai-feed`, `mim-ai-hallucinate`, `mim-ai-voice` | — | Không có sự kiện nào trong 8 bài này |

### 3b. T4–T9 cũ (`specs-T4..T9`, 20/10) và giữa 8 bài với nhau
- **T4 (GPU, 8), T5 (Watson, 5), T7 (poker, 4), T9 (game, 5):** không file nào nhắc Samsung/Garante/DeepSeek/Altman/Meta AI/Redis/lệnh toà (grep). **Không trùng.**
- **T8 (khuôn mặt/sinh trắc, 8 file):** `mim-robert-williams-30-gio` (bắt nhầm do nhận diện mặt), `mim-gender-shades-34-phay-7`, `mim-face-id-mot-phan-trieu`, `mim-nist-nhan-mat-gioi-gap-20-lan`, `mim-mat-ban-la-128-con-so`, `mim-vi-sao-ung-dung-bat-chop-mat`, `mim-bo-ba-tam-anh-day-may-nhan-mat`, `mim-bao-gan-thi-la-cung-mot-nguoi`. Đều là **ảnh/khuôn mặt/độ chính xác nhận diện**, không có chat, không có cơ quan quản lý dữ liệu. **Điểm chạm duy nhất có thể xảy ra:** nếu T8 đưa "cơ quan bảo vệ dữ liệu phạt/chặn" (ví dụ Garante) hoặc "Clearview" thì chạm bài 5; hiện **không có**, nên không trùng. Quy ước: sự kiện Garante–OpenAI thuộc T6.
- **Bản T6 cũ (`specs-T6/`, bị thay):** 8 slug cũ không còn dùng; `mim-samsung-ba-lan-trong-thang` và `mim-y-chan-chatgpt-2023`, `mim-4500-chat-tren-google` được viết lại trong bài 2, 5, 4. Không đưa vào hàng đợi song song.
- **Clip:** 17 clip (16 khác nhau) lấy từ `motion/hf/assets/clips/index.json` (đều có bản dọc), **không trùng clip nào trong `data/stier/specs/*.json`, `specs-T4..T9`** (đã so id; bản đầu T6 trùng 6 clip với Short đã dựng, đã thay).
- **Giữa 8 bài:** hai bài dùng chung clip cửa (bài 4 và 8 cùng `pexels:8561462`, cách 5 ngày) và `8091712`/`7279738` lặp **trong một bài** để vòng về câu mở (cố ý). Nếu muốn tách: đổi clip cửa của bài 4 trước khi dựng.

## 4. Kiểm tra kỹ thuật (đã chạy `_selfcheck.py`, 0 lỗi)
theme `mim`, `mix: true`, `rules: 2`; câu mở 8–9 chữ; lời đọc không chữ số (chỉ năm 4 chữ số như bài mẫu; ngày, số lượng, phần trăm đọc bằng chữ); counter không prefix chữ số ("HƠN " chỉ là chữ); đủ M D G; T ≤ 18%; không 3 cảnh liền cùng kiểu; cảnh ≤ 11 s (ước); không "mẹo", không "?" cuối, không mời xem video trong lời; tiêu đề ≤ 100 ký tự. **Chưa kiểm được ở pha 1 (cần build thật):** giờ giọng thật (ước 32–37 s; bài 5 có 4 chữ "năm" nên có thể vượt, nếu > 36 s thì cắt câu "Một lý do..."), chữ kinetic tràn khung, hold_open, mix_lint lần cuối trên giờ đo, cách giọng đọc "Ý", "Garante", "DeepSeek", "Wiz" (đã có bảng `say`, cần nghe thử).

## 5. Cần kiểm (trước pha 2)

1. **Không có `factcheck.md` của Long**; đọc lại mọi số khi Long có factcheck, sửa Short theo Long hoặc ngược lại.
2. **Lỗi trong `script.md` của Long (cần báo T-Long):** (a) CH05 ghi "Tháng 4 năm 2023, kỹ sư Samsung bắt đầu dùng ChatGPT": theo The Economist Korea, được dùng từ **11/03/2023**, báo đăng **30/03**, nên các vụ xảy ra trong tháng 3; (b) "điều Samsung lo là dữ liệu nằm ở máy chủ ngoài, khó xoá" **không có** trong bản The Register đã đọc (Samsung không xác nhận, bản tin nói lo ngại IP/bảo mật chung); chỉ giữ nếu tìm thấy trong Bloomberg gốc; (c) CH00 gán câu "thử nghiệm ngắn ngủi" cho Dane Stuckey, SEJ gán cho OpenAI.
3. **Trang gốc chưa đọc được:** OpenAI (March 20 outage; response to NYT), Fast Company, Garante (provv. 112, 755), bản án Rome 18/03/2026, Mozilla, Engadget, Business Insider (bài Meta AI). Tìm bản lưu hoặc đọc trực tiếp trước khi dựng.
4. **Bài 1:** "cực kỳ thấp" (OpenAI nói số người bị lộ) lấy từ tóm tắt tìm kiếm; cần xác nhận nguyên văn. Chỉ nói tiêu đề chat; không nói nội dung.
5. **Bài 2:** "chưa đầy ba tuần sau" = 11/03 → 30/03 (19 ngày), kênh tự tính; bộ phận (DS/bán dẫn) theo Economist Korea, chưa có bản gốc.
6. **Bài 3:** có thể có chênh lệch ngày giữa nguồn (lệnh 13/05, phản đối 03/06; OpenAI công bố blog ~05–06/06); "bản đã giữ vẫn còn" đúng với dữ liệu giữ trước 26/09 (trừ vùng EEA/Thuỵ Sĩ/Anh và ngoại lệ khác), nên câu chốt "bản đã giữ vẫn còn" chỉ đúng một phần: **cần đọc bản gốc thoả thuận 09/10/2025** và cân nhắc thêm "trừ vài ngoại lệ".
7. **Bài 4:** SEJ nói "over 4,500"; tìm thấy "nearly 4,500" ở một nguồn thứ cấp (Shopifreaks): ghi "hơn" theo SEJ, **đối chiếu bản Fast Company**.
8. **Bài 5:** văn bản Garante; liệu Garante kháng cáo bản án Rome; "28 ngày" kênh tự tính.
9. **Bài 6:** ngày chính xác bài Business Insider, "keep this private", số người liên lạc; Meta đã gỡ dòng tin Discover chưa (một nguồn thứ cấp nói có, chưa kiểm).
10. **Bài 7:** ngày phát sóng podcast; nguyên văn các câu trích.
11. **Bài 8:** "báo ngay, nhanh chóng đóng" là lời Wiz; không nêu ai khác đã truy cập (Wiz không nói); không gắn thêm tin về lệnh chặn DeepSeek ở nước nào (chưa kiểm).
12. **Clip:** chưa chạy `motion/long/clip_sheet.py`; tên clip chỉ lấy từ `clips/index.json`. Phải xem bảng clip để loại cảnh có logo/biển hiệu/chữ màn hình thiết bị (rủi ro cao hơn: `7279738`, `8889195`, `9757994`, `6414097`, `36149629` có điện thoại/máy tính) và cảnh trông như một nơi cụ thể (`36637656` phố đêm sương mù: không được gắn "ở Ý" trên màn hình; hiện chỉ chữ "NƯỚC Ý CHẶN CHATGPT"). Cảnh quote trên clip giữ veil 0,72.
13. **Mô tả:** mỗi bài ghi "Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels", "chưa có bản kiểm chứng riêng của kênh", nguồn, và dòng Long. Không có lời tư vấn pháp lý.

## 6. Dự phòng và góc đã bỏ

Đủ 8 bài, không độn. Bài yếu nhất về nguồn: **6 (Meta AI, nguồn đọc qua tìm kiếm)** và **3 (nguồn thứ cấp)**; nếu không kiểm được, thay bằng:
- **R1 · Bard 2023:** 28/09/2023 The Register tìm thấy link chia sẻ Bard trong kết quả Google bằng toán tử `site:`; Danny Sullivan (Google Search Liaison): Google không định để các chat được lập chỉ mục và đang chặn (The Register, đã đọc). Chung chủ đề với bài 4 (chia sẻ → tìm kiếm); chỉ dùng thay bài 4/6 nếu một trong hai rớt.
- **R2 · Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15:** Quốc hội thông qua 26/06/2025, 433/435 đại biểu tán thành (LSVN, đối chiếu nhiều nguồn), hiệu lực 01/01/2026; NĐ 356/2025. Có người/ngày/số phiếu nhưng yếu về truyện; dùng nếu cần bài hướng Việt Nam. Không dùng "phạt gấp 10 lần" khi chưa đọc điều luật gốc.
- **R3 · Samsung giới hạn 1.024 byte mỗi câu hỏi** (nguồn thứ cấp), gộp được vào bài 2 nếu cần dài thêm.
- **Không làm:** vụ Palisades 2025 (chat làm chứng cứ, liên quan một bị cáo cụ thể, đã loại để tránh nhắm vào cá nhân); mọi bài "chính sách" nêu ở mục 0; Gemini/Claude/ChatGPT "nên bật tắt gì" (lời khuyên, khung mẹo).
