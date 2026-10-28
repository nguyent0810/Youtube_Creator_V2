# KIEM-NGUON-B — Kiểm nguồn gốc 8 Short MIM (chỉ số 7–14 trong flagged_slugs.json)

Ngày kiểm: 22/10/2026. Không sửa spec, không gọi API YouTube, không sửa state.sqlite.
Quy ước: KIỂM ĐƯỢC / LỆCH / KHÔNG KIỂM ĐƯỢC. Trích ≤ 15 chữ. Kết luận cuối mỗi slug: SẠCH / SỬA / GỠ.

Ghi chú truy cập: web.archive.org bị chặn/429; garanteprivacy.it, engadget.com, bloomberg.com, businessinsider.com, techmeme không mở được trực tiếp. Bản gốc mở được: Wiz, NIST (news + NISTIR 8238 PDF), Viola–Jones PDF (CVPR 2001), trang OpenAI (qua curl), TechCrunch, Mozilla Foundation, Tuổi Trẻ, Vietnam News, Cổng TTĐT Chính phủ.

## Tổng hợp

| # | Slug | Kết luận |
|---|------|----------|
| 7 | mim-jensen-ha-noi-nha-thu-hai | SẠCH |
| 8 | mim-chat-da-xoa-van-bi-giu | SỬA (4 chỗ nhỏ; không cần gỡ) |
| 9 | mim-y-chan-chatgpt-roi-toa-huy-phat | SẠCH (1 ghi chú tuỳ chọn) |
| 10 | mim-meta-ai-sua-xe-cong-khai | SỬA (nguồn câu "giữ riêng tư" là Engadget, không phải BI) |
| 11 | mim-altman-khong-nhu-bac-si | SẠCH |
| 12 | mim-viola-jones-2001-may-tim-mat | SẠCH (1 ghi chú tuỳ chọn) |
| 13 | mim-nist-2018-bon-nam-20-lan | SẠCH (ghi chú về "26,6 triệu ảnh") |
| 14 | mim-deepseek-kho-chat-khong-mat-khau | SẠCH |

Không bài nào phải GỠ.

---

## 7. mim-jensen-ha-noi-nha-thu-hai — SẠCH

| Khẳng định (lời đọc / màn hình) | Kết luận | Nguồn đã mở + trích |
|---|---|---|
| Tháng 12/2023 Jensen Huang tới Hà Nội (màn hình "12.2023") | KIỂM ĐƯỢC | Tuổi Trẻ (news.tuoitre.vn/...10377218): "arrived in Hanoi on Saturday" (9/12/2023), họp thứ Hai 11/12. Tuoitrenews 10/12/2023: "Nvidia wishes to establish a base in Vietnam" |
| "Báo chí ghi lại: ông muốn biến VN thành ngôi nhà thứ hai của Nvidia" (diễn ý) | KIỂM ĐƯỢC (thứ cấp, đúng mức "báo chí ghi lại") | Bloomberg 11/12/2023, tiêu đề "Nvidia Sees Vietnam as Potential Second Home, Reports Say" (qua kết quả tìm kiếm; trang Bloomberg 403) |
| 05/12/2024 VN và Nvidia ký thoả thuận | KIỂM ĐƯỢC | Cổng TTĐT CP en.baochinhphu.vn: "witnessed the signing of an agreement", 5/12/2024; Tuoitrenews 06/12/2024 |
| Lập trung tâm nghiên cứu AI + trung tâm dữ liệu AI | KIỂM ĐƯỢC | baochinhphu: "AI research and development center" và "an AI data center" |
| Nvidia mua lại VinBrain | KIỂM ĐƯỢC | Vietnam News 09/12/2024 (vietnamnews.vn/...1688676): "Nvidia also said it has acquired healthcare startup VinBrain" |
| Trung tâm dữ liệu, theo báo chí, mở rộng từ trung tâm của Viettel | KIỂM ĐƯỢC | Vietnam News (trích The Diplomat): "expansion of an AI data centre owned by ... Viettel" |
| "Chưa đầy một năm" (từ 9–11/12/2023 đến 5/12/2024) | KIỂM ĐƯỢC | 11/12/2023 → 05/12/2024 = thiếu 6 ngày so với một năm |

Cờ cũ "ngày chính xác ở Hà Nội" đã giải: 9–11/12/2023. Không cần sửa. (Tuỳ chọn cho mô tả: thêm URL Tuổi Trẻ/Cổng TTĐT.)

---

## 8. mim-chat-da-xoa-van-bi-giu — SỬA

Nguồn gốc mở được: trang OpenAI "How we're responding to The New York Times' data demands" (đã tải qua curl, bản cập nhật 22/10/2025); Malwarebytes; kết quả tìm kiếm từ CyberInsider/Bloomberg Law (không mở trực tiếp được Bloomberg Law, Engadget). Lệnh toà trên docket 1:23-cv-11195 không mở được.

| Khẳng định | Kết luận | Nguồn + trích |
|---|---|---|
| 13/05/2025, thẩm phán Ona Wang, vụ NYT kiện OpenAI | KIỂM ĐƯỢC (thứ cấp) | Malwarebytes: "The order was granted May 13", Magistrate Judge Ona T. Wang; CyberInsider cùng nội dung |
| Lời đọc dòng 2 nói Wang "nhận yêu cầu" | LỆCH nhẹ | Nguồn: bà ra lệnh (granted) ngày 13/5, không phải "nhận yêu cầu" |
| Ra lệnh giữ dữ liệu vốn sẽ bị xoá, cả chat đã xoá | KIỂM ĐƯỢC | Malwarebytes: "preserve and segregate all output log data that would otherwise be deleted"; OpenAI: "even deleted ChatGPT chats" |
| Bình thường OpenAI xoá trong 30 ngày | KIỂM ĐƯỢC | OpenAI: "automatically deleted from our systems within 30 days" |
| Tháng 6 OpenAI phản đối công khai | KIỂM ĐƯỢC | Bài OpenAI đề ngày 5/6/2025 ký Brad Lightcap, COO |
| "Gọi lệnh ấy là rộng quá mức" / quote "Rộng quá mức và không cần thiết" của Lightcap | LỆCH nhẹ | Nguyên văn: "a sweeping and unnecessary demand" — nói về YÊU CẦU của NYT, không phải lệnh; từ "vastly overbroad" nằm ở phần OpenAI mô tả đơn của họ, không phải câu của Lightcap |
| "Hàng trăm triệu người dùng ... chat của họ nằm trong lệnh" | LỆCH (thiếu quy kết) | Trang OpenAI không có số này; chỉ có kết quả tìm kiếm thuật lại OpenAI nói "hundreds of millions of users". Đây là lời OpenAI, không phải dữ kiện toà. Ngoài ra lệnh không áp dụng với Enterprise/Edu/ZDR |
| Từ 26/09/2025 OpenAI không phải giữ thêm | KIỂM ĐƯỢC | OpenAI: "Our obligations under the earlier order ended on September 26, 2025" |
| "Chat xoá giữa tháng năm và tháng chín, bản đã giữ vẫn còn" | LỆCH nhẹ | OpenAI: lưu "limited historical April–September 2025 user data"; không áp dụng chat từ EEA/Thuỵ Sĩ/Anh; phần còn lại được khoá, chưa giao cho NYT |

Đề xuất sửa (cả 4 là chỉnh đúng nguồn, không đổi ý bài):

1. Dòng 2: "Ngày mười ba tháng năm 2025, thẩm phán Ona Wang ra lệnh trong vụ New York Times kiện OpenAI." (16 từ, gốc 17). Dòng 3 giữ nguyên hoặc "Lệnh buộc giữ lại dữ liệu vốn sẽ bị xoá, cả chat đã xoá." Chữ màn hình không đổi.
2. Dòng 5: "Tháng sáu, OpenAI phản đối công khai, gọi yêu cầu của các báo là quá rộng và không cần thiết." (19 từ; gốc 16 — nếu cần giữ độ dài: "Tháng sáu, OpenAI phản đối công khai, gọi yêu cầu của báo là rộng quá mức." 15 từ). Màn hình quote giữ "Rộng quá mức và không cần thiết." nhưng đổi `by` thành "BRAD LIGHTCAP · COO OPENAI · NÓI VỀ YÊU CẦU CỦA NYT · TRÍCH DỊCH".
3. Dòng 6: "Theo OpenAI, hàng trăm triệu người dùng không phải bên nào trong vụ, nhưng chat của họ nằm trong lệnh." (+3 từ, trong ±10%+; nếu chặt: "OpenAI nói hàng trăm triệu người dùng không phải bên trong vụ mà chat vẫn nằm trong lệnh."). Ledger: đổi `v` thành "THEO OPENAI: HÀNG TRĂM TRIỆU NGƯỜI DÙNG".
4. Dòng 8: "Chat xoá trong thời gian lệnh hiệu lực, một phần bản đã giữ vẫn còn." (16 từ, gốc 17). Slam sub: "TRƯỚC NGÀY 26.09.2025" giữ.

Cũng cần chỉnh description nếu bài còn nhắc "gồm cả chat người dùng" mà không thêm "trừ Enterprise/Edu và EEA/Anh/Thuỵ Sĩ" — đề nghị thêm 1 câu ngắn. Không cần gỡ.

---

## 9. mim-y-chan-chatgpt-roi-toa-huy-phat — SẠCH (ghi chú tuỳ chọn)

| Khẳng định | Kết luận | Nguồn + trích |
|---|---|---|
| Garante tạm hạn chế OpenAI cuối 3/2023 (quyết định 30/03) | KIỂM ĐƯỢC (≥ 2 nguồn độc lập; văn bản gốc garanteprivacy.it không mở được DNS) | Il Post 28/04/2023 và diritto.it: Garante mở điều tra sau khi hạn chế xử lý dữ liệu; Altroconsumo qua tìm kiếm |
| Lý do: thiếu thông báo người dùng, thiếu cơ sở pháp lý | KIỂM ĐƯỢC (thứ cấp) | Tìm kiếm tổng hợp nhiều báo Ý + Teleborsa 20/12/2024 nêu lại: "base giuridica", "trasparenza" |
| ChatGPT trở lại ngày 28/04 | KIỂM ĐƯỢC | Il Post 28/04/2023: "ChatGPT è di nuovo raggiungibile dall'Italia" |
| 12/2024 Garante phạt 15 triệu euro (công bố 20/12) | KIỂM ĐƯỢC | Teleborsa/LaPresse 20/12/2024: "sanzione da 15 milioni di euro" |
| Một lý do: không báo vụ lộ dữ liệu 3/2023 | KIỂM ĐƯỢC | Teleborsa: không notifica violazione dati marzo 2023 |
| 18/03/2026 toà Rome huỷ phạt, vì thẩm quyền | KIỂM ĐƯỢC | diritto.it: "sentenza n. 4785 del 18 marzo 2026"; huỷ provv. 755/2024; "ritenendo assorbenti le censure sulla competenza" (one-stop-shop, Ireland) |
| Garante có kháng cáo không | KHÔNG KIỂM ĐƯỢC | Không nguồn nào nêu; bài không khẳng định nên không cần sửa |

Ghi chú tuỳ chọn (cosmetic, không đủ ngưỡng thay video): tiêu đề/dòng 1 "Nước Ý chặn ChatGPT" — thực tế Garante hạn chế xử lý dữ liệu và OpenAI tự chặn truy cập từ Ý; dòng 2 đã nói đúng. Toà Rome không xét nội dung vi phạm, bài không nói OpenAI vô tội nên ổn. "Gần một tháng/28 ngày" khớp (31/3–28/4).

---

## 10. mim-meta-ai-sua-xe-cong-khai — SỬA

Business Insider gốc KHÔNG mở được (403/không có trong tập mở được); Engadget chỉ lấy được qua kết quả tìm kiếm; Mozilla mở được trực tiếp; Yahoo/HuffPost mở được.

| Khẳng định | Kết luận | Nguồn + trích |
|---|---|---|
| 6/2025 Meta AI có dòng tin công khai (Discover) hiện chat người dùng đăng | KIỂM ĐƯỢC | Yahoo (HuffPost): "Discover feed"; Mozilla: "stream of real AI conversations" |
| BI thấy nhiều bài như đăng nhầm | KIỂM ĐƯỢC | Mozilla: "many of these chats appear to have been shared by mistake"; Yahoo/Mashable: "First reported by Business Insider" |
| Người hỏi chuyện sửa xe nói không định đăng công khai | KIỂM ĐƯỢC mức thứ cấp (chưa mở BI) | getcoai: BI liên hệ ~24 người, một người trả lời "hadn't intended to make his conversation public"; hyper.ai: "seeking advice on car repair" |
| Có người viết thêm "hãy giữ chuyện này riêng tư" — màn hình ghi "THEO BUSINESS INSIDER" | LỆCH (nguồn đã đọc là Engadget) | Stuff trích Engadget: "desperately added 'keep this private' to his public posts" — số nhiều, không gắn vào BI |
| Meta: không gì lên dòng tin nếu bạn không chọn đăng | KIỂM ĐƯỢC (diễn ý) | Yahoo: "private unless users go through multiple steps to share them" |
| Đăng phải bấm hai lần | KIỂM ĐƯỢC | Yahoo: "tapping 'Share' and affirmatively tapping to post" |
| Mozilla: giao diện không báo rõ là công khai | KIỂM ĐƯỢC | Mozilla: "app fails to clearly show users that their chats are going public" |
| Meta thêm màn cảnh báo trước khi đăng | KIỂM ĐƯỢC | Mozilla: "briefly implementing a mandatory warning screen"; Yahoo: "Prompts you post are public and visible to everyone" |

Đề xuất sửa:
- Dòng 5: "Theo Engadget, có người còn viết thêm vào bài: hãy giữ chuyện này riêng tư." (15 từ, gốc 14). Quote scene 4: `by` đổi thành "MỘT BÀI ĐÃ ĐĂNG CÔNG KHAI · THEO ENGADGET · TRÍCH DỊCH".
- Dòng 3–4: giữ, nhưng nên thêm vào description một câu "Chi tiết người hỏi sửa xe lấy từ bản tin thứ cấp về bài của Business Insider; kênh chưa mở được bài gốc." Nếu muốn giảm rủi ro hơn thì dòng 4: "Một người đàn ông hỏi chuyện sửa xe, theo Business Insider, nói anh không định đăng công khai." (17 từ, gốc 16).
- Nếu BI gốc sau này mở được và xác nhận cả hai chi tiết thì hoàn nguyên. Không cần gỡ.

---

## 11. mim-altman-khong-nhu-bac-si — SẠCH

| Khẳng định | Kết luận | Nguồn + trích |
|---|---|---|
| Tháng 7/2025, Altman trên podcast Theo Von | KIỂM ĐƯỢC | TechCrunch 25/07/2025: "This Past Weekend w/ Theo Von" #599. Ngày phát sóng: thứ Tư 23/07/2025 (TheTVDB: 23/07/2025; BI: "episode that aired Wednesday" — hai nguồn khớp) |
| Nhiều người kể chuyện riêng tư cho ChatGPT như kể với nhà trị liệu | KIỂM ĐƯỢC | TechCrunch: "People talk about the most personal sh** in their lives to ChatGPT" |
| Bác sĩ, luật sư, nhà trị liệu có đặc quyền pháp lý | KIỂM ĐƯỢC | TechCrunch: "there's legal privilege for it" (therapist, lawyer, doctor) |
| "Chúng tôi chưa tìm ra điều đó" | KIỂM ĐƯỢC | TechCrunch: "we haven't figured that out yet for when you talk to ChatGPT" |
| Nếu có kiện tụng, OpenAI có thể phải đưa chat ra | KIỂM ĐƯỢC | TechCrunch (diễn ý, không trích trực tiếp) + BI qua tìm kiếm: "we could be required to produce that" |
| Ông gọi tình trạng này "rất không ổn" | KIỂM ĐƯỢC | TechCrunch: "I think that's very screwed up" |

Cờ cũ đã giải (ngày phát sóng 23/07/2025). Không cần sửa. Tuỳ chọn: ghi "23/07/2025" vào mô tả.

---

## 12. mim-viola-jones-2001-may-tim-mat — SẠCH (ghi chú tuỳ chọn)

Đã mở bản gốc: Viola & Jones, CVPR 2001 PDF (cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf), cộng Wikipedia.

| Khẳng định | Kết luận | Trích |
|---|---|---|
| Năm 2001, Paul Viola và Michael Jones | KIỂM ĐƯỢC | Bài CVPR 2001, tác giả Viola, Jones (MERL) |
| Mẫu sáng tối; vùng mắt tối hơn vùng má | KIỂM ĐƯỢC | "region of the eyes is often darker than the region" cheeks |
| Pentium III 700 MHz, 15 hình/giây, ảnh 384×288 | KIỂM ĐƯỢC | Abstract: "15 frames per second on a conventional 700 MHz Intel Pentium III"; "384 by 288 pixel images" |
| iPAQ khoảng 2 hình/giây | KIỂM ĐƯỢC | "detection at two frames per second" trên Compaq iPaq |
| Hơn 20 năm sau, vẫn chạy ở máy yếu | KIỂM ĐƯỢC mức Wikipedia | Wikipedia: "still used in cases with limited computational power" |
| "Lưới hàng triệu ô vuông" | Cần lưu ý | Ảnh thử 384×288 chỉ ~110 nghìn điểm ảnh; câu nói chung về ảnh hiện đại nên không sai, nhưng bài báo không nói "triệu" |
| "Ô vuông quanh mặt trên màn hình máy ảnh" | KHÔNG CÓ trong nguồn | Bài báo không nhắc máy ảnh; minh hoạ chung, không có số/ngày/tên |

Ghi chú tuỳ chọn: nếu muốn chặt, dòng 3 có thể là "một lưới hàng trăm nghìn đến hàng triệu ô vuông" và dòng 8 thêm "theo Wikipedia". Không đủ ngưỡng thay video đã đăng.

---

## 13. mim-nist-2018-bon-nam-20-lan — SẠCH (ghi chú)

Đã mở: NIST news (nist.gov/node/1532616) và toàn văn NISTIR 8238 (nvlpubs.nist.gov/nistpubs/ir/2018/NIST.IR.8238.pdf, tải bằng curl, 42 MB).

| Khẳng định | Kết luận | Trích |
|---|---|---|
| 2014: trượt ~4% | KIỂM ĐƯỢC | NIST news: "4% in 2014"; NISTIR: miss rate rank-1 2013-OCT NEC-30 = 4.1% (báo cáo tháng 4/2014) |
| 2018: ~0,2%; giỏi hơn ~20 lần | KIỂM ĐƯỢC | NIST: "got 20 times better"; NISTIR: "factor of 20 fewer misses"; Microsoft-4 6/2018 rank-1 0,23% |
| 127 thuật toán, 39 nhà phát triển | KIỂM ĐƯỢC (có lệch nội bộ) | NIST news: "127 ... from 39 different developers"; NISTIR mục Overview "39 commercial developers and one university" nhưng Exec Summary ghi "45 developers" |
| Kho 26,6 triệu ảnh | KIỂM ĐƯỢC có sắc thái | NISTIR: "26.6 million ... live portrait photos of 12.3 million individuals" là bộ dữ liệu chính; phép so 2014↔2018 chạy trên kho 1,6 triệu người; kết quả <0,2% là trên kho 12 triệu |
| Grother: năng lực giữa các hãng chênh rất xa | KIỂM ĐƯỢC | "There remains a very wide spread of capability across the industry" |
| "Chỉ với thuật toán giỏi và ảnh tốt" | KIỂM ĐƯỢC (cờ cũ đã giải) | NISTIR Exec Summary: "With good quality portrait photos, ... error rates below 0.2%" |
| 30/11/2018 | KIỂM ĐƯỢC | NIST news: "November 30, 2018" |

Ghi chú: dòng 3–4 nói "tìm một người trong kho 26,6 triệu ảnh" hơi gộp hai điều (bộ dữ liệu vs kho thử); cosmetic, không đổi ý. Tuỳ chọn thay "kho" bằng "bộ thử" ở dòng 4 và bảng "KHO 26,6 TRIỆU ẢNH" → "BỘ THỬ 26,6 TRIỆU ẢNH". Không cần thay video.

---

## 14. mim-deepseek-kho-chat-khong-mat-khau — SẠCH

Đã mở: wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak.

| Khẳng định | Kết luận | Trích |
|---|---|---|
| 29/01/2025, Wiz công bố | KIỂM ĐƯỢC | "Published: January 29, 2025, by Gal Nagli" |
| CSDL mở, không xác thực | KIỂM ĐƯỢC | "completely open and unauthenticated" (ClickHouse) |
| Tự chạy lệnh ngay trong trình duyệt | KIỂM ĐƯỢC | giao diện /play "allowed direct SQL execution from a browser" |
| Hai tên miền phụ của DeepSeek | KIỂM ĐƯỢC | oauth2callback.deepseek.com và dev.deepseek.com (cổng 9000/8123) |
| Hơn một triệu dòng nhật ký | KIỂM ĐƯỢC | "over 1 million" dòng trong bảng log_stream |
| Có lịch sử chat, khoá bí mật, chi tiết hệ thống | KIỂM ĐƯỢC | "chat history, secret keys, backend details" |
| Wiz báo ngay, DeepSeek nhanh chóng đóng | KIỂM ĐƯỢC | "promptly secured the exposure" (Wiz không nêu mốc thời gian) |

Chỉ có một nguồn (Wiz), nhưng là nguồn gốc nên đủ; bài đã ghi "theo Wiz" trong mô tả. Không cần sửa.
