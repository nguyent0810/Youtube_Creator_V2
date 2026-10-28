# KIEM-NGUON-A: kiểm nguồn gốc 7 Short MIM (chỉ số 0-6 trong flagged_slugs.json)

Ngày kiểm: 22/10/2026. Không sửa spec, không gọi API YouTube, không sửa state.sqlite.
Ghi chú môi trường: một số miền (nytimes, wired, fortune, lexfridman, openai.com, aaai, web.archive.org) không mở được từ công cụ (chặn/403/DNS). Chỗ nào không mở được bản gốc ghi rõ và đã đối chiếu thay bằng bản PDF tác giả hoặc từ 2 nguồn độc lập trở lên.

## Tóm tắt

| # | Slug | Kết luận |
|---|---|---|
| 0 | mim-cuda-canh-bac-2006 | SỬA: biên lãi gộp 35% chứ không phải 30%; bỏ ý "khách chủ yếu là phòng thí nghiệm" |
| 1 | mim-nghin-may-chu-con-ba-2013 | SẠCH |
| 2 | mim-dgx1-qua-tang-openai-2016 | SẠCH (có 1 ghi chú không bắt buộc) |
| 3 | mim-watson-ferrucci-sai-gan-het | SỬA: "15 người / 3-5 năm", "2008 đấu được nhà vô địch", "15%" chưa đứng vững; đề xuất viết lại 3 câu |
| 4 | mim-fei-fei-li-14-trieu-anh | SỬA nhẹ (tùy chọn): bỏ "về sau" ở câu Wired |
| 5 | mim-chat-nguoi-la-20-3-2023 | SẠCH |
| 6 | mim-samsung-ba-vu-truoc-khi-cam | SỬA nhẹ: câu mã nguồn "thiết bị bán dẫn"; câu thông báo nội bộ nói như cấm toàn Samsung |

Không slug nào cần GỠ.

---

## 0. mim-cuda-canh-bac-2006

URL đã mở:
- Digital Engineering 24/7 (bản thông cáo Nvidia): https://www.digitalengineering247.com/article/nvidia-unveils-cuda/engineering-computing
- Bản chép lời Lex Fridman #494 (scribehawk): https://scribehawk.com/transcript/jensen-huang-nvidia-the-4-trillion-company-the-ai-revolution-lex-fridman-podcast (lexfridman.com không mở được; singjupost cũng không mở được; glennklockwood.com/garden/jensen xác nhận thêm)
- AlexNet (Krizhevsky, Sutskever, Hinton, NeurIPS 2012), PDF: papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf
- HPCwire 35 Legends Ian Buck (https://www.hpcwire.com/35-hpc-legends-ian-buck) mở trực tiếp bị 403; đối chiếu qua kết quả tìm kiếm HPCwire + blogs.nvidia.com/blog/author/ian-buck + trang Princeton CS (2004).

| Khẳng định | Kết luận | Bằng chứng |
|---|---|---|
| Ian Buck viết Brook ở Stanford, phép tính khỏi giả làm bức tranh | KIỂM ĐƯỢC | HPCwire: PhD Stanford về stream computing dẫn tới "Brook" rồi CUDA |
| Năm 2004 Nvidia thuê anh | KIỂM ĐƯỢC (qua tìm kiếm, nhiều nguồn) | blog Nvidia: joined in 2004 after Stanford PhD; Princeton CS 2004 |
| 08/11/2006 Nvidia ra mắt CUDA | KIỂM ĐƯỢC | Digital Engineering: thân bài "today, November 8, unveiled a new architecture" (đầu trang ghi 1/11 nhưng thân bài và sportsvideo.org đăng 09/11/2006 khớp 8/11) |
| Jensen: mỗi chip thêm khoảng 50% chi phí | KIỂM ĐƯỢC | Lex #494 ~00:15:31: "we increased our cost by 50%" (chi phí GeForce) |
| Biên lãi gộp lúc ấy khoảng 30% | LỆCH | Lex #494: "we were a 35% gross margin company" (scribehawk, nhiều bản tóm tắt cũng ghi 35%). 30% chỉ có trong kênh tự ghi |
| "Khách chủ yếu là phòng thí nghiệm" | KHÔNG KIỂM ĐƯỢC | Jensen nói kế hoạch là đưa CUDA lên mọi GeForce để nhà nghiên cứu và sinh viên dùng về sau; không nói khách chủ yếu là phòng thí nghiệm; lo ngại là game thủ không muốn trả thêm |
| "Chi phí ăn gần hết lợi nhuận" | LỆCH nhẹ | Jensen: chi phí thêm "consumed all of the gross profit dollars" (nuốt hết) |
| CUDA nằm trong card chơi game ai cũng mua được | KIỂM ĐƯỢC | Lex #494: đưa CUDA lên mọi GeForce |
| Sáu năm sau (2012) có người mua đúng loại card ấy để dạy máy nhìn | KIỂM ĐƯỢC | AlexNet: "two GTX 580 3GB GPUs", năm 2012 |

Đề xuất sửa (giữ độ dài ±10%):
- Câu 6 (lines[5]) mới: "Mà biên lãi gộp lúc ấy chỉ khoảng ba mươi lăm phần trăm." Màn hình ledger hàng 2: v = "KHOẢNG 35%" (at [5,"ba"] vẫn khớp từ "ba"). description: đổi "biên lãi gộp của hãng khoảng 30%" thành "khoảng 35%".
- Câu 7 (lines[6]) mới: "Game thủ không muốn trả thêm, nên chi phí ấy nuốt hết lợi nhuận gộp." Màn hình kinetic scene 6: items = "GAME THỦ" (at [6,"Game"], acc) và "nuốt hết lợi nhuận" (at [6,"nuốt"], sm).
- Thêm vào sources_internal: bản chép lời Lex #494 đã đối chiếu.

---

## 1. mim-nghin-may-chu-con-ba-2013

URL đã mở:
- https://proceedings.mlr.press/v28/coates13.html không mở được (DNS); mở bản PDF tác giả http://proceedings.mlr.press/v28/coates13.pdf (đọc bằng pypdf)
- arXiv 1112.6209 (Le, Ng, Dean và cộng sự): https://arxiv.org/abs/1112.6209
- Google blog (bản gốc Dean và Ng): https://blog.google/topics/machine-learning/using-large-scale-brain-simulations-for/
- The Register 18/06/2013: https://www.theregister.com/2013/06/18/google_deep_learning_ai/
- NYT 25/06/2012: chặn, không mở; không cần vì blog gốc đã mở.

| Khẳng định | Kết luận | Bằng chứng |
|---|---|---|
| 2012 Google cho mạng nơ-ron xem ảnh YouTube | KIỂM ĐƯỢC | blog Google: "unlabeled YouTube stills" |
| Không ai bảo nó mèo là gì | KIỂM ĐƯỢC | blog: "this network had never been told what a cat was" |
| 16.000 lõi xử lý | KIỂM ĐƯỢC | blog: "across 16,000 of our CPU cores" |
| Hơn 1.000 máy chủ / 1.000 máy | KIỂM ĐƯỢC | arXiv: "cluster of 1,000 machines (16,000 cores)"; Register: "1,000 machines" (lưu ý nguồn nói đúng 1.000, mô tả đang viết "hơn 1.000") |
| Mạng chừng 1 tỉ kết nối | KIỂM ĐƯỢC | blog: "more than 1 billion connections"; arXiv: "about 1 billion connections" |
| Jeff Dean và Andrew Ng viết trên blog Google | KIỂM ĐƯỢC | blog.google, bài về mạng nhận ra mèo |
| 2013 Stanford (Coates, nhóm Ng): 3 máy, 1 tỉ tham số | KIỂM ĐƯỢC | ICML 2013: "train 1 billion parameter networks on just 3 machines in a couple of days" |
| 16 máy, hơn 11 tỉ | KIỂM ĐƯỢC | cùng bài: "over 11 billion parameters using just 16 machines" |
| Máy chủ gắn card đồ hoạ bán sẵn | KIỂM ĐƯỢC | "COTS HPC ... cluster of GPU servers"; Register: GTX 680 |
| "Cùng cỡ mạng chừng 1 tỉ" (kết nối vs tham số) | KIỂM ĐƯỢC có lưu ý | Bài ICML tự đặt đối chiếu với các mạng "over 1 billion parameters" của Google; scene đã ghi chú "tham số, không phải kết nối" |

Kết luận: SẠCH, không cần sửa. Tùy chọn: description "hơn 1.000 máy chủ" đổi "khoảng 1.000 máy chủ".

---

## 2. mim-dgx1-qua-tang-openai-2016

URL đã mở:
- Entrepreneur: https://www.entrepreneur.com/business-news/elon-musks-artificial-intelligence-project-just-got-a-free-supercomputer/280944
- TechCrunch 05/04/2016 (GTC): https://techcrunch.com/2016/04/05/nvidia-announces-a-supercomputer-aimed-at-deep-learning-and-ai
- Wikipedia OpenAI (thành lập 12/2015, Sutskever đồng sáng lập): https://en.wikipedia.org/wiki/OpenAI
- Fortune, Data Center Knowledge, Top500, blog Nvidia: không mở được (DNS/chuyển hướng lạ); đối chiếu qua kết quả tìm kiếm trích các bài này.

| Khẳng định | Kết luận | Bằng chứng |
|---|---|---|
| Tháng 8/2016 Jensen Huang tự mang tới văn phòng OpenAI ở San Francisco | KIỂM ĐƯỢC | Entrepreneur: "personally delivered ... to OpenAI's San Francisco office", công bố 15/08/2016 |
| Tám GPU trong một thùng | KIỂM ĐƯỢC | TechCrunch: "eight Tesla P100 cards"; Entrepreneur "250 servers in a box" |
| Nvidia gọi là siêu máy tính đầu tiên cho AI | KIỂM ĐƯỢC mức thứ cấp | Tìm kiếm: TechRadar, itWire, eWeek ghi "world's first deep learning supercomputer"; TechCrunch không dùng cụm này; không mở được thông cáo gốc. Câu lời đọc đã ghi "Nvidia gọi", có thể giữ |
| Giá khoảng 129.000 đô | KIỂM ĐƯỢC | TechCrunch (GTC 04/2016): "costs $129,000"; Entrepreneur: $129,000 |
| Ký lên máy, lời chúc cho Elon Musk và cả nhóm | KIỂM ĐƯỢC | Entrepreneur: "To Elon and the OpenAI Team!" |
| OpenAI mới lập vài tháng (12/2015) | KIỂM ĐƯỢC | Entrepreneur: "debuted in December"; Wikipedia: December 2015 (8 tháng) |
| Ilya Sutskever đồng sáng lập | KIỂM ĐƯỢC | Wikipedia OpenAI liệt kê Sutskever |
| ChatGPT ra mắt 30/11/2022; "hơn sáu năm" | KIỂM ĐƯỢC mức thứ cấp | Nhiều nguồn ghi 30/11/2022 (trang gốc OpenAI không mở được); 8/2016 đến 11/2022 = 6 năm 3 tháng |

Kết luận: SẠCH. Không cần sửa.

---

## 3. mim-watson-ferrucci-sai-gan-het

URL đã mở:
- Wikipedia IBM Watson (mục Development): https://en.wikipedia.org/wiki/IBM_Watson
- NYT Magazine 06/2010, Baker 2011: không mở được (nytimes chặn, archive.org chặn).
- Slate 09/2025 (trích Ferrucci): https://www.slate.com/culture/2025/09/jeopardy-game-watson-questions-final-ken-jennings.html
- CCC Blog (bài nói của Ferrucci 2011): https://cccblog.org/2011/06/07/watsons-lead-developer-deep-analysis-speed-and-results/
- IBM History: https://www.ibm.com/history/watson-jeopardy
- TechCrunch 14/12/2010: https://techcrunch.com/2010/12/14/latest-jeopardy-contestant-a-robot-named-watson/
- AI Magazine "Building Watson" (DeepQA): không mở được PDF; chỉ đọc tóm tắt qua tìm kiếm.

| Khẳng định | Kết luận | Bằng chứng |
|---|---|---|
| 2006 Ferrucci cho Watson thử 500 câu Jeopardy cũ | KIỂM ĐƯỢC chỉ qua Wikipedia (dẫn NYT) | Wikipedia: "500 clues from past Jeopardy! episodes" |
| Lượt đầu đúng khoảng 15% | KIỂM ĐƯỢC một phần, số lệch nhẹ | Wikipedia: "about 15%"; Ferrucci (CCC): hệ thống 2007 "plateaued at 14 percent"; Slate trích Ferrucci: 13%. Nguồn nói 13-15% |
| Người giỏi nhất đúng tới 95%, bấm chuông nhanh gấp đôi | KHÔNG KIỂM ĐƯỢC ngoài Wikipedia | Chỉ Wikipedia ("up to 95%", "twice as quickly"); không tìm được nguồn thứ hai; tìm kiếm chỉ thấy "85-95% sau khi giành chuông" |
| 2007 nhóm được giao 3 đến 5 năm và 15 người | KHÔNG KIỂM ĐƯỢC / xung đột | Chỉ Wikipedia; IBM History: "more than two dozen" người, "five years"; tóm tắt DeepQA: "core team of about 20 researchers" |
| 2008 máy đủ sức đấu với nhà vô địch | KHÔNG KIỂM ĐƯỢC | Chỉ Wikipedia/fandom; không nguồn nào khác nêu mốc 2008 |
| 02/2010 thắng người chơi thường xuyên | KIỂM ĐƯỢC chỉ qua Wikipedia | TechCrunch 12/2010 chỉ nói đấu hơn 50 ván thử với cựu vô địch, không nêu kết quả |
| "Mất khoảng bốn năm" (kênh tự tính) | KIỂM ĐƯỢC có nguồn tốt hơn | TechCrunch/IBM 12/2010: "After four years, our scientific team believes that Watson is ready" |

Đề xuất sửa (giữ nhịp, độ dài ±10%):
- lines[2] (câu 3) mới: "Lượt đầu, nó đúng chỉ chừng mười mấy phần trăm." Màn hình counter scene 2: giữ số 15 nhưng đổi label thành "WATSON ĐÚNG · LƯỢT ĐẦU · KHOẢNG 13-15%" hoặc đổi to=14 với label "KHOẢNG · THEO CÁC NGUỒN 13-15%". (Phải đổi `until` nếu bỏ chữ "mười".)
- lines[4] (câu 5) mới: "Năm hai nghìn không trăm lẻ bảy, ông Ferrucci lập một nhóm hơn hai chục người cho dự án." (IBM History "more than two dozen"). Màn hình scene 4: "3–5 NĂM" và "15 NGƯỜI" thành "2007" và "HƠN 2 CHỤC NGƯỜI"; dòng nhỏ "nhóm của Ferrucci" giữ.
- lines[5-6] (câu 6, 7) mới, thay hai mốc 2008 và 02/2010: "Cuối năm hai nghìn không trăm mười, nó đã đấu thử hơn năm mươi ván với các cựu vô địch." và "Rồi IBM nói đã sẵn sàng lên truyền hình." (nguồn TechCrunch/Register 12/2010). Màn hình: scene 5 "2008 / máy đấu được nhà vô địch" thành "2010 / hơn 50 ván đấu thử" ; scene 6 date "02.2010" đổi thành "12.2010", day "ĐẤU THỬ VỚI CỰU VÔ ĐỊCH".
- lines[7] (câu 8) mới: "Từ sai gần hết tới sẵn sàng thi đấu, IBM nói mất bốn năm." Counter: sub = "THEO IBM · KHOẢNG" (thay "KÊNH TỰ TÍNH").
- Phương án thay thế nếu muốn giữ cấu trúc cũ và chỉ gắn nguồn: thêm "Theo Wikipedia" trước các mốc 95%, 3-5 năm, 2008; không khuyến nghị vì độ tin cậy kém.
- Không cứu được bằng nguồn nào hơn thì vẫn giữ video (không cần GỠ) vì sự kiện cốt lõi (sai gần hết, thắng người chơi giỏi) vững; chỉ các số chi tiết cần làm mềm.

---

## 4. mim-fei-fei-li-14-trieu-anh

URL đã mở:
- Wikipedia ImageNet: https://en.wikipedia.org/wiki/ImageNet
- AlexNet PDF (NeurIPS 2012): papers.nips.cc ... c399862d3b9d6b76c8436e924a68c45b-Paper.pdf
- Substack tổng hợp (nguồn yếu, chỉ tham khảo): https://proofoverpromise.substack.com/p/chapter-4-the-undeniable-signal-part
- Wired gốc: wired.com bị chặn, không mở được. Quartz và Princeton: 403/DNS.

| Khẳng định | Kết luận | Bằng chứng |
|---|---|---|
| 2006 Lý Phi Phi mở dự án | KIỂM ĐƯỢC có lưu ý | Wikipedia: "began working on the idea in 2006"; một nguồn thứ cấp yếu ghi 2007. Giữ 2006 theo Wikipedia |
| Theo Wired, cô khó nhờ đồng nghiệp giúp | KIỂM ĐƯỢC chỉ qua Wikipedia | Wikipedia dẫn Wired 2018: "had a hard time getting faculty members to help out" (Wired nói lúc cô đề xuất dự án, không phải "về sau") |
| Gần 50.000 người, 167 nước, lọc hơn 160 triệu ảnh ứng viên | KIỂM ĐƯỢC | Wikipedia: "49K workers from 167 countries ... over 160M candidate images" (7/2008-4/2010) |
| 2009 ra mắt ở CVPR (Florida) dạng áp phích | KIỂM ĐƯỢC | Wikipedia: "first presented as a poster at CVPR 2009 in Florida" |
| Tháng 4/2010 có hơn 14 triệu ảnh | KIỂM ĐƯỢC | Wikipedia: 14,197,122 ảnh ngày 30/04/2010 |
| 2012 mạng nơ-ron trên card chơi game thắng cuộc thi dùng bộ ảnh này | KIỂM ĐƯỢC | AlexNet (NeurIPS 2012): huấn luyện trên "two GTX 580 3GB GPUs"; thắng ILSVRC-2012 |
| "Hai chiếc card" | KIỂM ĐƯỢC | cùng bài báo, hai GPU |

Đề xuất sửa nhẹ (tùy chọn, không bắt buộc):
- lines[2] mới: "Theo tạp chí Wired, cô khó nhờ được đồng nghiệp giúp." (bỏ "về sau", chữ đổi ít, độ dài giảm khoảng 10%). Màn hình giữ nguyên.
- Không cần sửa mục khác. Ghi chú nội bộ cũ về "Stanford 2006" không xuất hiện trong lời đọc nên không ảnh hưởng.

---

## 5. mim-chat-nguoi-la-20-3-2023

URL đã mở:
- Bài gốc OpenAI https://openai.com/index/march-20-chatgpt-outage trả 403 cả hai đường dẫn; archive.org bị chặn.
- Help Net Security: https://www.helpnetsecurity.com/2023/03/27/chatgpt-data-leak/ (mở được, trích thư OpenAI gửi người dùng)
- ForkLog 27/03/2023: https://forklog.com/en/chatgpt-outage-exposed-subscribers-payment-information/ (mở được, trích bài OpenAI)
- The Hacker News: 403 trực tiếp; nội dung bài OpenAI được trích lại qua kết quả tìm kiếm (OpenAI, The Hacker News, Security Affairs, Sonatype).

| Khẳng định | Kết luận | Bằng chứng |
|---|---|---|
| 20/03 một số người thấy tiêu đề chat của người khác | KIỂM ĐƯỢC | Help Net: chỉ tiêu đề cuộc trò chuyện bị lộ |
| OpenAI cho ChatGPT ngừng hoạt động để tìm nguyên nhân | KIỂM ĐƯỢC qua bài OpenAI trích trong kết quả tìm kiếm | Câu OpenAI: "took ChatGPT offline ... due to a bug in an open-source library"; Help Net/ForkLog chỉ nói "outage" |
| Lỗi trong thư viện mã nguồn mở, yêu cầu bị huỷ có thể trả nhầm dữ liệu | KIỂM ĐƯỢC | ForkLog: lỗi "in an open-source library called redis-py"; request cancellation trả dữ liệu hỏng cho truy vấn khác |
| 1,2% người dùng gói trả phí | KIỂM ĐƯỢC | Help Net: 1.2% ChatGPT Plus subscribers (đang hoạt động trong khung giờ đó) |
| Trong chín giờ | KIỂM ĐƯỢC | Help Net: "nine-hour window"; ForkLog: 4:00-13:00 ET |
| Có thể lộ tên, địa chỉ, bốn số cuối thẻ | KIỂM ĐƯỢC | Help Net: first and last name, billing address ... (còn email, hạn thẻ; không có số thẻ đầy đủ) |
| OpenAI nói số người thực sự bị lộ cực kỳ thấp | KIỂM ĐƯỢC | ForkLog: "extremely low" |

Kết luận: SẠCH (đối chiếu qua 2 bài mở được cộng nhiều bản trích; bài gốc OpenAI 403 đã nêu). Nên ghi trong description rằng bài gốc OpenAI không mở được từ máy kênh, nếu muốn chặt chẽ.

---

## 6. mim-samsung-ba-vu-truoc-khi-cam

URL đã mở:
- Cybersecurity News (trích Economist Korea): https://cybersecuritynews.com/chatgpt-leaks-samsung-data/
- The Register 02/05/2023: https://www.theregister.com/2023/05/02/samsung_generative_ai_ban/
- Kết quả tìm kiếm AI Incident Database, Android Authority, TechRadar (trang TechRadar mở ra chỉ có menu).
- The Economist Korea gốc (economist.co.kr): không tìm thấy/mở được. Bloomberg: không mở (paywall); The Register dẫn lại.

| Khẳng định | Kết luận | Bằng chứng |
|---|---|---|
| Bộ phận bán dẫn (DS) cho dùng ChatGPT từ 11/03/2023 | KIỂM ĐƯỢC mức thứ cấp | Cybersecurity News dẫn Economist Korea: DS cho phép "from the 11th", DX còn cấm; AIID: 11/03/2023; "khoảng 20 ngày" trước khi rò rỉ khớp bản tin 30/03 |
| Chưa đầy ba tuần sau báo Hàn đưa tin ba vụ | KIỂM ĐƯỢC mức thứ cấp | AIID: Economist Korea 30/03/2023 (19 ngày) nêu ít nhất ba vụ |
| Vụ 1: dán mã nguồn lỗi của thiết bị bán dẫn nhờ sửa | LỆCH nhẹ | Nguồn: mã nguồn chương trình tải CSDL đo lường thiết bị (semiconductor facility measurement DB download program), không phải mã của con chip |
| Vụ 2: dán mã nhờ tối ưu | KIỂM ĐƯỢC | mã nhận diện năng suất (yield) và thiết bị lỗi, nhờ tối ưu |
| Vụ 3: biến bản ghi họp thành biên bản | KIỂM ĐƯỢC | nhân viên chuyển bản ghi họp qua Naver Clova thành tài liệu rồi đưa vào ChatGPT để lập biên bản/tài liệu họp |
| Samsung không xác nhận chi tiết các vụ | KIỂM ĐƯỢC (nên nhẹ hơn) | The Register: các vụ là báo cáo chưa được xác nhận, Samsung không trả lời yêu cầu xác nhận; chỉ xác nhận có thông báo nội bộ |
| Thông báo nội bộ đầu tháng 5 tạm cấm AI tạo sinh | KIỂM ĐƯỢC nhưng phạm vi | The Register (02/05/2023, dẫn Bloomberg): thông báo gửi "one of its biggest divisions", cấm tạm thời ChatGPT/Bard; không phải cấm toàn tập đoàn |
| Mở cửa 11/03, tạm cấm chưa đầy hai tháng sau | KIỂM ĐƯỢC | 11/03 đến 02/05 = 52 ngày |

Đề xuất sửa nhẹ:
- lines[3] mới: "Một kỹ sư dán mã nguồn lỗi của chương trình đo thiết bị nhà máy để nhờ sửa." Màn hình scene 3 card 1: v = "MÃ LỖI CHƯƠNG TRÌNH ĐO" (at [3,"mã"] giữ).
- lines[6] mới: "Samsung chưa xác nhận chi tiết các vụ này." Màn hình slam: "CHƯA XÁC NHẬN".
- lines[7] mới: "Đầu tháng năm, một thông báo gửi một bộ phận lớn vẫn tạm cấm các công cụ AI tạo sinh." Màn hình board: node "THÔNG BÁO NỘI BỘ" thành "THÔNG BÁO GỬI MỘT BỘ PHẬN LỚN". Title/description: thêm "tại một bộ phận lớn" sau "Samsung tạm cấm".
- Nếu không muốn sửa video đã tải: hai chỗ cuối là ranh giới "chỉ sửa khi đổi nghĩa" theo quy tắc replace-uploaded; chỗ "thiết bị bán dẫn" là sắc thái, có thể giữ.
