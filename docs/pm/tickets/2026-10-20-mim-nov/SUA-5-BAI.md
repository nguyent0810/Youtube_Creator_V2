# SUA-5-BAI: sửa 5 Short MIM theo kết quả kiểm nguồn

Ngày 22/10/2026. Chủ kênh đã duyệt; bỏ qua fei-fei-li. Nguồn đề xuất: KIEM-NGUON-A.md (cuda, watson-ferrucci, samsung) và KIEM-NGUON-B.md (chat-da-xoa, meta-ai).
Đã sửa: data/stier/specs/<slug>.json, bản sao docs/pm/tickets/2026-10-20-mim-nov/specs-v2-T4|T5|T6/<slug>.json, output/chain_src/sources_public.json. Không chạy build/render, không gọi API YouTube, không sửa state.sqlite.
Lint: motion/stier/build.py mix_lint + kiểm neo/độ dài/chữ số như _selfcheck.py (script tạm ở scratchpad). Video đã tải lên YouTube vẫn là bản cũ cho tới khi chủ kênh quyết định thay (xem quy tắc replace-uploaded).

## mim-cuda-canh-bac-2006

Số từ lời đọc: 134 → 135 (+0.7%).

### Lời đọc (lines)

| Câu | Trước | Sau |
|---|---|---|
| 6 | Mà biên lãi gộp lúc ấy chỉ khoảng ba mươi phần trăm. | Mà biên lãi gộp lúc ấy chỉ khoảng ba mươi lăm phần trăm. |
| 7 | Khách chủ yếu là phòng thí nghiệm, chi phí ăn gần hết lợi nhuận. | Game thủ không muốn trả thêm, nên chi phí nuốt hết lợi nhuận gộp. |

### Chữ trên màn hình (scenes)

| Scene | Trước | Sau |
|---|---|---|
| 5 (ledger) | rows: `[{"k": "CHI PHÍ THÊM MỖI CHIP", "v": "KHOẢNG 50%", "at": [4, "nửa"]}, {"k": "BIÊN LÃI GỘP LÚC ẤY", "v": "KHOẢNG 30%", "at": [5, "ba"]}]` | rows: `[{"k": "CHI PHÍ THÊM MỖI CHIP", "v": "KHOẢNG 50%", "at": [4, "nửa"]}, {"k": "BIÊN LÃI GỘP LÚC ẤY", "v": "KHOẢNG 35%", "at": [5, "ba"]}]` |
| 6 (kinetic) | items: `[{"text": "PHÒNG THÍ NGHIỆM", "at": [6, "phòng"], "acc": true, "size": 84}, {"text": "ăn gần hết lợi nhuận", "at": [6, "ăn"], "sm": true, "size": 52}]` | items: `[{"text": "GAME THỦ", "at": [6, "Game"], "acc": true, "size": 120}, {"text": "nuốt hết lợi nhuận", "at": [6, "nuốt"], "sm": true, "size": 52}]` |

### Description

- trước: Ian Buck, nghiên cứu sinh Stanford, viết ngôn ngữ Brook để phép tính khỏi phải giả làm bức tranh; năm 2004 anh về Nvidia. Ngày 08/11/2006 Nvidia ra mắt CUDA. Theo lời Jensen Huang kể trong một podcast, CUDA làm mỗi GPU tốn thêm khoảng 50% chi phí khi biên lãi gộp của hãng khoảng 30%. Giọng đọc tổng hợp; video Pexels. ⏎  ⏎ Bản đầy đủ: https://youtu.be/Es4bogrdk-c
- sau: Ian Buck, nghiên cứu sinh Stanford, viết ngôn ngữ Brook để phép tính khỏi phải giả làm bức tranh; năm 2004 anh về Nvidia. Ngày 08/11/2006 Nvidia ra mắt CUDA. Theo lời Jensen Huang kể trong một podcast, CUDA làm mỗi GPU tốn thêm khoảng 50% chi phí khi biên lãi gộp của hãng khoảng 35%. Giọng đọc tổng hợp; video Pexels. ⏎  ⏎ Bản đầy đủ: https://youtu.be/Es4bogrdk-c

### Sources (public)

- trước: ["HPCwire — 35 HPC Legends (hồ sơ Ian Buck)", "Tom's Hardware — phỏng vấn Ian Buck", "Lex Fridman Podcast #494 — Jensen Huang"]
- sau: ["HPCwire — 35 HPC Legends (hồ sơ Ian Buck)", "Tom's Hardware — phỏng vấn Ian Buck", "Lex Fridman Podcast #494 — Jensen Huang (bản chép lời)", "https://www.digitalengineering247.com/article/nvidia-unveils-cuda/engineering-computing (thông cáo Nvidia về CUDA)", "https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf (AlexNet, 2012)"]

## mim-watson-ferrucci-sai-gan-het

Số từ lời đọc: 116 → 114 (-1.7%).

### Lời đọc (lines)

| Câu | Trước | Sau |
|---|---|---|
| 3 | Lượt đầu, nó đúng khoảng mười lăm phần trăm. | Lượt đầu, nó đúng chỉ chừng mười mấy phần trăm. |
| 4 | Người giỏi nhất đúng tới chín mươi lăm phần trăm, và bấm chuông nhanh gấp đôi. | Theo Wikipedia, người giỏi nhất đúng tới chín mươi lăm phần trăm. |
| 5 | Năm hai nghìn không trăm lẻ bảy, nhóm của ông được giao ba đến năm năm, và mười lăm người. | Năm hai nghìn không trăm lẻ bảy, ông Ferrucci lập một nhóm hơn hai chục người cho dự án. |
| 6 | Năm hai nghìn không trăm lẻ tám, máy đủ sức đấu với các nhà vô địch. | Cuối năm hai nghìn không trăm mười, nó đã đấu thử hơn năm mươi ván với các cựu vô địch. |
| 7 | Tháng hai năm hai nghìn không trăm mười, nó thắng người chơi thường xuyên. | Rồi IBM nói đã sẵn sàng lên truyền hình. |
| 8 | Từ sai gần hết tới thắng người, mất khoảng bốn năm. | Từ sai gần hết tới sẵn sàng thi đấu, IBM nói mất bốn năm. |

### Chữ trên màn hình (scenes)

| Scene | Trước | Sau |
|---|---|---|
| 2 (counter) | sub: `null`; to: `15` | sub: `{"text": "CÁC NGUỒN GHI 13–15%", "at": [2, "chừng"]}`; to: `14` |
| 3 (cards3d) | cards: `[{"k": "NGƯỜI GIỎI NHẤT", "v": "ĐÚNG TỚI 95%", "at": [3, "chín"]}, {"k": "BẤM CHUÔNG", "v": "NHANH GẤP ĐÔI", "at": [3, "nhanh"], "c": "acc"}]` | cards: `[{"k": "NGUỒN", "v": "THEO WIKIPEDIA", "at": [3, "Wikipedia"], "c": "acc"}, {"k": "NGƯỜI GIỎI NHẤT", "v": "ĐÚNG TỚI 95%", "at": [3, "chín"]}]` |
| 4 (kinetic) | items: `[{"text": "3–5 NĂM", "at": [4, "ba"], "acc": true}, {"text": "15 NGƯỜI", "at": [4, "mười"]}, {"text": "2007 · nhóm của Ferrucci", "at": [4, "Năm"], "sm": true, "size": 56}]` | items: `[{"text": "2007", "at": [4, "Năm"], "acc": true}, {"text": "HƠN 2 CHỤC NGƯỜI", "at": [4, "hơn"]}, {"text": "nhóm của Ferrucci", "at": [4, "nhóm"], "sm": true, "size": 56}]` |
| 5 (kinetic) | items: `[{"text": "2008", "at": [5, "Năm"], "acc": true, "size": 260}, {"text": "máy đấu được nhà vô địch", "at": [5, "đấu"], "sm": true, "size": 56}]` | items: `[{"text": "2010", "at": [5, "năm"], "acc": true, "size": 260}, {"text": "hơn 50 ván đấu thử", "at": [5, "đấu"], "sm": true, "size": 56}]` |
| 6 (date) | date: `"02.2010"`; day: `"THẮNG NGƯỜI THƯỜNG XUYÊN"`; sub: `{"text": "TRƯỚC TRẬN TRUYỀN HÌNH", "at": [6, "thắng"]}` | date: `"12.2010"`; day: `"ĐẤU THỬ VỚI CỰU VÔ ĐỊCH"`; sub: `{"text": "TRƯỚC TRẬN TRUYỀN HÌNH", "at": [6, "truyền"]}` |
| 7 (slam) | text: `"SAI GẦN HẾT → THẮNG"` | text: `"SAI GẦN HẾT → SẴN SÀNG"` |
| 8 (counter) | label: `"TỪ BÀI THỬ TỚI THẮNG NGƯỜI"`; sub: `{"text": "KÊNH TỰ TÍNH · KHOẢNG", "at": [7, "khoảng"]}` | label: `"TỪ BÀI THỬ TỚI SẴN SÀNG"`; sub: `{"text": "THEO IBM · KHOẢNG", "at": [7, "bốn"]}` |

### Description

- trước: Năm 2006, David Ferrucci (IBM) cho Watson làm thử 500 câu hỏi cũ của Jeopardy: lượt đầu máy đúng khoảng 15%, trong khi người chơi giỏi nhất đúng tới 95% và bấm chuông nhanh gấp đôi. Năm 2007 nhóm được giao 3–5 năm và 15 người; tới 2008 máy đủ sức đấu với nhà vô địch, tới tháng 2/2010 thắng người chơi thường xuyên (Wikipedia, IBM Watson, dẫn NYT Magazine). Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật. ⏎  ⏎ Bản đầy đủ: https://youtu.be/Mt5hYcQxH50 (công khai từ 20:00 ngày 19/11).
- sau: Năm 2006, David Ferrucci (IBM) cho Watson làm thử 500 câu hỏi cũ của Jeopardy: lượt đầu máy đúng chừng 13–15% (các nguồn ghi số hơi khác nhau). Theo Wikipedia, người chơi giỏi nhất đúng tới 95%. Năm 2007 Ferrucci lập nhóm hơn hai chục người (IBM). Cuối năm 2010 Watson đã đấu thử hơn 50 ván với các cựu vô địch, và IBM nói đã sẵn sàng lên truyền hình sau bốn năm (IBM; TechCrunch, 12/2010). Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật. ⏎  ⏎ Bản đầy đủ: https://youtu.be/Mt5hYcQxH50 (công khai từ 20:00 ngày 19/11).

### Sources (public)

- trước: ["https://en.wikipedia.org/wiki/IBM_Watson", "The New York Times Magazine, 06/2010 — bài về Watson (qua Wikipedia)", "Stephen Baker — Final Jeopardy (2011)"]
- sau: ["https://en.wikipedia.org/wiki/IBM_Watson", "https://www.ibm.com/history/watson-jeopardy", "https://techcrunch.com/2010/12/14/latest-jeopardy-contestant-a-robot-named-watson/", "https://cccblog.org/2011/06/07/watsons-lead-developer-deep-analysis-speed-and-results/", "https://www.slate.com/culture/2025/09/jeopardy-game-watson-questions-final-ken-jennings.html"]

## mim-samsung-ba-vu-truoc-khi-cam

Số từ lời đọc: 108 → 113 (+4.6%).

Tiêu đề:
- trước: Samsung mở ChatGPT cho kỹ sư ngày 11/03/2023, chưa đầy hai tháng sau tạm cấm (theo báo chí)
- sau: Samsung mở ChatGPT cho kỹ sư 11/03/2023, chưa đầy hai tháng sau một bộ phận lớn tạm cấm

### Lời đọc (lines)

| Câu | Trước | Sau |
|---|---|---|
| 4 | Một kỹ sư dán mã nguồn lỗi của thiết bị bán dẫn để nhờ sửa. | Một kỹ sư dán mã nguồn lỗi của chương trình đo thiết bị nhà máy để nhờ sửa. |
| 7 | Samsung không xác nhận chi tiết các vụ này. | Samsung chưa xác nhận chi tiết các vụ này. |
| 8 | Đầu tháng năm, một thông báo nội bộ vẫn tạm cấm các công cụ AI tạo sinh. | Đầu tháng năm, thông báo gửi một bộ phận lớn vẫn tạm cấm các công cụ AI tạo sinh. |

### Chữ trên màn hình (scenes)

| Scene | Trước | Sau |
|---|---|---|
| 3 (cards3d) | cards: `[{"k": "LẦN 1", "v": "MÃ LỖI THIẾT BỊ", "at": [3, "mã"]}, {"k": "LẦN 2", "v": "MÃ CẦN TỐI ƯU", "at": [4, "mã"], "c": "acc"}]` | cards: `[{"k": "LẦN 1", "v": "MÃ LỖI CHƯƠNG TRÌNH ĐO", "at": [3, "mã"]}, {"k": "LẦN 2", "v": "MÃ CẦN TỐI ƯU", "at": [4, "mã"], "c": "acc"}]` |
| 5 (slam) | text: `"KHÔNG XÁC NHẬN"` | text: `"CHƯA XÁC NHẬN"` |
| 6 (board) | nodes: `[{"text": "THÔNG BÁO NỘI BỘ", "x": 0.5, "y": 0.3, "at": [7, "thông"], "shape": "box"}, {"text": "TẠM CẤM AI TẠO SINH", "x": 0.5, "y": 0.68, "at": [7, "tạm"], "c": "acc", "shape": "circle", "w": 740}]` | nodes: `[{"text": "THÔNG BÁO GỬI MỘT BỘ PHẬN LỚN", "x": 0.5, "y": 0.3, "at": [7, "thông"], "shape": "box", "w": 780}, {"text": "TẠM CẤM AI TẠO SINH", "x": 0.5, "y": 0.68, "at": [7, "tạm"], "c": "acc", "shape": "circle", "w": 740}]` |

### Description

- trước: Theo The Economist Korea (30/03/2023), bộ phận bán dẫn của Samsung cho dùng ChatGPT từ 11/03/2023, và có ba vụ đưa thông tin nội bộ vào công cụ này: mã nguồn lỗi của một thiết bị bán dẫn, mã cần tối ưu, và bản ghi một cuộc họp. Samsung không xác nhận chi tiết các vụ (The Register, 02/05/2023). Theo bản thông báo nội bộ mà Bloomberg được xem (02/05/2023), Samsung tạm cấm công cụ AI tạo sinh trên thiết bị của công ty. Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện. Thông tin theo nguồn đã ghi, đọc ngày 20/10/2026; chưa có bản kiểm chứng riêng của kênh. ⏎  ⏎ Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11).
- sau: Theo The Economist Korea (30/03/2023), bộ phận bán dẫn của Samsung cho dùng ChatGPT từ 11/03/2023, và có ba vụ đưa thông tin nội bộ vào công cụ này: mã nguồn lỗi của chương trình đo thiết bị nhà máy, mã cần tối ưu, và bản ghi một cuộc họp. Samsung chưa xác nhận chi tiết các vụ (The Register, 02/05/2023). Theo bản thông báo nội bộ mà Bloomberg được xem (02/05/2023), Samsung tạm cấm công cụ AI tạo sinh tại một bộ phận lớn, trên thiết bị của công ty. Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện. Thông tin theo nguồn đã ghi, đọc ngày 20/10/2026; chưa có bản kiểm chứng riêng của kênh. ⏎  ⏎ Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11).

### Sources (public)

- trước: ["The Economist Korea, 30/03/2023 (qua Gigazine, Cybersecurity News, HCAMag)", "https://www.theregister.com/2023/05/02/samsung_generative_ai_ban/", "Bloomberg, 02/05/2023 — thông báo nội bộ của Samsung về lệnh cấm công cụ AI tạo sinh"]
- sau: ["The Economist Korea, 30/03/2023 (qua Gigazine, Cybersecurity News, HCAMag)", "https://cybersecuritynews.com/chatgpt-leaks-samsung-data/", "https://www.theregister.com/2023/05/02/samsung_generative_ai_ban/", "Bloomberg, 02/05/2023 — thông báo nội bộ của Samsung gửi một bộ phận lớn về lệnh cấm công cụ AI tạo sinh"]

## mim-chat-da-xoa-van-bi-giu

Số từ lời đọc: 113 → 117 (+3.5%).

### Lời đọc (lines)

| Câu | Trước | Sau |
|---|---|---|
| 2 | Ngày mười ba tháng năm 2025, thẩm phán Ona Wang nhận yêu cầu trong vụ New York Times kiện OpenAI. | Ngày mười ba tháng năm 2025, thẩm phán Ona Wang ra lệnh trong vụ New York Times kiện OpenAI. |
| 3 | Bà ra lệnh giữ lại dữ liệu vốn sẽ bị xoá, cả chat đã xoá. | Lệnh buộc giữ lại dữ liệu vốn sẽ bị xoá, cả chat đã xoá. |
| 5 | Tháng sáu, OpenAI phản đối công khai, gọi lệnh ấy là rộng quá mức. | Tháng sáu, OpenAI phản đối công khai, gọi yêu cầu của báo là rộng quá mức. |
| 6 | Hàng trăm triệu người dùng không phải bên nào trong vụ, nhưng chat của họ nằm trong lệnh. | Theo OpenAI, hàng trăm triệu người dùng không phải bên nào trong vụ, nhưng chat của họ nằm trong lệnh. |
| 8 | Chat xoá giữa tháng năm và tháng chín, bản đã giữ vẫn còn. | Chat xoá trong thời gian lệnh hiệu lực, một phần bản đã giữ vẫn còn. |

### Chữ trên màn hình (scenes)

| Scene | Trước | Sau |
|---|---|---|
| 2 (board) | nodes: `[{"text": "NEW YORK TIMES KIỆN OPENAI", "x": 0.5, "y": 0.28, "at": [2, "Bà"], "shape": "box", "w": 780}, {"text": "GIỮ CẢ CHAT ĐÃ XOÁ", "x": 0.5, "y": 0.68, "at": [2, "cả"], "c": "acc", "shape": "circle", "w": 740}]` | nodes: `[{"text": "NEW YORK TIMES KIỆN OPENAI", "x": 0.5, "y": 0.28, "at": [2, "Lệnh"], "shape": "box", "w": 780}, {"text": "GIỮ CẢ CHAT ĐÃ XOÁ", "x": 0.5, "y": 0.68, "at": [2, "cả"], "c": "acc", "shape": "circle", "w": 740}]` |
| 4 (quote) | by: `"BRAD LIGHTCAP · COO OPENAI · TRÍCH DỊCH"` | by: `"BRAD LIGHTCAP · COO OPENAI · NÓI VỀ YÊU CẦU CỦA NYT · TRÍCH DỊCH"` |
| 5 (ledger) | rows: `[{"k": "BÊN TRONG VỤ KIỆN", "v": "BÁO · OPENAI", "at": [5, "bên"]}, {"k": "NẰM TRONG LỆNH", "v": "HÀNG TRĂM TRIỆU NGƯỜI DÙNG", "at": [5, "chat"]}]` | rows: `[{"k": "BÊN TRONG VỤ KIỆN", "v": "BÁO · OPENAI", "at": [5, "bên"]}, {"k": "NẰM TRONG LỆNH", "v": "THEO OPENAI: HÀNG TRĂM TRIỆU NGƯỜI DÙNG", "at": [5, "chat"]}]` |

### Description

- trước: Ngày 13/05/2025, thẩm phán Ona T. Wang (Toà án Liên bang quận Nam New York), trong vụ The New York Times và các báo kiện OpenAI, ra lệnh OpenAI giữ lại dữ liệu đầu ra ChatGPT vốn sẽ bị xoá, gồm cả chat người dùng đã xoá. OpenAI phản đối công khai (đơn phản đối 03/06/2025; COO Brad Lightcap gọi lệnh là rộng quá mức, không cần thiết). Nghĩa vụ giữ thêm dữ liệu mới chấm dứt từ 26/09/2025 theo thoả thuận được duyệt ngày 09/10/2025; dữ liệu đã giữ trước đó vẫn còn, trừ vài ngoại lệ. Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện. Thông tin theo nguồn đã ghi, đọc ngày 20/10/2026; chưa có bản kiểm chứng riêng của kênh. ⏎  ⏎ Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11).
- sau: Ngày 13/05/2025, thẩm phán Ona T. Wang (Toà án Liên bang quận Nam New York), trong vụ The New York Times và các báo kiện OpenAI, ra lệnh OpenAI giữ lại dữ liệu đầu ra ChatGPT vốn sẽ bị xoá, gồm cả chat người dùng đã xoá. OpenAI phản đối công khai (đơn phản đối 03/06/2025; COO Brad Lightcap gọi yêu cầu của các báo là rộng quá mức, không cần thiết). Nghĩa vụ giữ thêm dữ liệu mới chấm dứt từ 26/09/2025 theo thoả thuận được duyệt ngày 09/10/2025; OpenAI cho biết đã lưu một phần dữ liệu lịch sử từ tháng 4 đến tháng 9/2025 và phần này vẫn còn. Theo OpenAI, hàng trăm triệu người dùng không phải bên trong vụ nhưng chat của họ nằm trong phạm vi lệnh; lệnh không áp dụng với Enterprise, Edu và một số chế độ không lưu dữ liệu. Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện. Thông tin theo nguồn đã ghi, đọc ngày 20/10/2026; chưa có bản kiểm chứng riêng của kênh. ⏎  ⏎ Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11).

### Sources (public)

- trước: ["https://www.malwarebytes.com/blog/news/2025/06/openai-forced-to-preserve-chatgpt-chats", "https://cyberinsider.com/us-court-orders-openai-to-preserve-all-chatgpt-logs-indefinitely/", "https://news.bloomberglaw.com/litigation/openai-continues-to-fight-discovery-order-over-privacy-concerns", "https://engadget.com/ai/openai-no-longer-has-to-preserve-all-of-its-chatgpt-data-with-some-exceptions-192422093.html", "OpenAI — response to NYT data demands: https://openai.com/index/response-to-nyt-data-demands/"]
- sau: ["https://www.malwarebytes.com/blog/news/2025/06/openai-forced-to-preserve-chatgpt-chats", "https://cyberinsider.com/us-court-orders-openai-to-preserve-all-chatgpt-logs-indefinitely/", "https://news.bloomberglaw.com/litigation/openai-continues-to-fight-discovery-order-over-privacy-concerns", "https://engadget.com/ai/openai-no-longer-has-to-preserve-all-of-its-chatgpt-data-with-some-exceptions-192422093.html", "OpenAI — How we're responding to The New York Times' data demands: https://openai.com/index/response-to-nyt-data-demands/"]

## mim-meta-ai-sua-xe-cong-khai

Số từ lời đọc: 116 → 116 (+0.0%).

### Lời đọc (lines)

| Câu | Trước | Sau |
|---|---|---|
| 5 | Có người còn viết thêm vào bài đã đăng: hãy giữ chuyện này riêng tư. | Theo Engadget, có người còn viết thêm vào bài: hãy giữ chuyện này riêng tư. |

### Chữ trên màn hình (scenes)

| Scene | Trước | Sau |
|---|---|---|
| 4 (quote) | by: `"MỘT BÀI ĐÃ ĐĂNG CÔNG KHAI · THEO BUSINESS INSIDER · TRÍCH DỊCH"` | by: `"MỘT BÀI ĐÃ ĐĂNG CÔNG KHAI · THEO ENGADGET · TRÍCH DỊCH"` |

### Description

- trước: Tháng 6/2025, ứng dụng Meta AI có dòng tin công khai Discover hiện những cuộc trò chuyện với chatbot mà người dùng đã đăng. Business Insider thấy nhiều bài trông như đăng nhầm; một người đàn ông hỏi về sửa xe nói anh không định đăng công khai; một người viết thêm vào bài đã đăng lời nhắn giữ riêng tư. Meta nói không có gì lên dòng tin nếu người dùng không chọn đăng; Mozilla nói giao diện không báo rõ bài sẽ công khai; Meta thêm màn cảnh báo trước khi đăng (Engadget; Mozilla Foundation). Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện. Thông tin theo nguồn đã ghi, đọc ngày 20/10/2026; chưa có bản kiểm chứng riêng của kênh. ⏎  ⏎ Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11).
- sau: Tháng 6/2025, ứng dụng Meta AI có dòng tin công khai Discover hiện những cuộc trò chuyện với chatbot mà người dùng đã đăng. Business Insider thấy nhiều bài trông như đăng nhầm; một người đàn ông hỏi về sửa xe nói anh không định đăng công khai; theo Engadget, có người viết thêm vào bài đã đăng lời nhắn giữ riêng tư. Meta nói không có gì lên dòng tin nếu người dùng không chọn đăng; Mozilla nói giao diện không báo rõ bài sẽ công khai; Meta thêm màn cảnh báo trước khi đăng (Engadget; Mozilla Foundation). Chi tiết người hỏi sửa xe lấy từ bản tin thứ cấp về bài của Business Insider; kênh chưa mở được bài gốc. Giọng đọc tổng hợp; video minh hoạ lấy từ Pexels, không phải cảnh thật của sự kiện. Thông tin theo nguồn đã ghi, đọc ngày 20/10/2026; chưa có bản kiểm chứng riêng của kênh. ⏎  ⏎ Bản đầy đủ: https://youtu.be/ejsjefnJQbI (công khai từ 20:00 ngày 23/11).

### Sources (public)

- trước: ["https://engadget.com/social-media/meta-warns-users-to-avoid-sharing-personal-or-sensitive-information-in-its-ai-app-233900625.html", "https://www.mozillafoundation.org/en/campaigns/meta-help-users-stop-accidentally-sharing-private-ai-conversations/", "Business Insider (06/2025) — bài về dòng tin Discover của ứng dụng Meta AI và các bài đăng nhầm"]
- sau: ["https://engadget.com/social-media/meta-warns-users-to-avoid-sharing-personal-or-sensitive-information-in-its-ai-app-233900625.html", "https://www.mozillafoundation.org/en/campaigns/meta-help-users-stop-accidentally-sharing-private-ai-conversations/", "Business Insider (06/2025) — bài về dòng tin Discover của ứng dụng Meta AI và các bài đăng nhầm (qua bản tin thứ cấp)"]

