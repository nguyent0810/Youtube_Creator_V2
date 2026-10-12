# "BẠN CHƯA NÓI GÌ": kịch bản lời đọc (bản 2, đã kiểm chứng)

**Tựa chính:** Thuật Toán Đề Xuất: Vì Sao TikTok Và YouTube Biết Bạn Thích Gì?

**Kênh:** Mind in the Machine (MIM) · **Giọng:** Hải Đăng (lời trích: Ngọc Huyền, lọc radio)
**Độ dài dự kiến:** khoảng 13–14 phút, 9 chương (≈3.000 âm tiết đọc đủ chữ)
**Hồ sơ dữ kiện + nguồn:** [docs/channels/mind-in-the-machine/2026-10-09-long-05-research.md](../../../docs/channels/mind-in-the-machine/2026-10-09-long-05-research.md) (dàn ý mục 4, nguồn mục 10)

Quy ước đọc file:
- Mỗi dòng là một câu đọc. `‖` cuối dòng = ngừng dài.
- `»` = lời trích, đọc bằng giọng trích; nguyên văn tiếng Anh hiện trên màn hình.
- **[TRÍCH DỊCH]** = câu có thật (blog kỹ thuật, bài báo khoa học, trang trợ giúp), dịch sang tiếng Việt. **[DIỄN Ý]** = trích diễn đạt lại, gắn nhãn trên hình.
- `»` **không nhãn** = trích nguyên văn **chữ Việt gốc** (CH04 "Video này dài hơn…" là chữ tiếng Việt của chính TikTok, không phải bản dịch): nhãn trên hình "TRÍCH", không "TRÍCH DỊCH".
- Tên nước ngoài giữ nguyên chữ trên phụ đề; cách đọc nằm trong `say` của spec.json (danh sách khoá ở mục Ghi chú).

**Cấu trúc giữ chân người xem** (theo [RETENTION.md](../../../motion/long/RETENTION.md)):
- **Cold open:** ngày 26/07/2009, cuộc thi Netflix Prize một triệu đô khép lại: hai đội bằng điểm tới chữ số thập phân thứ tư, đội nộp sớm hơn hai mươi phút thắng. Rồi chi tiết lạ: Netflix không đưa bản thắng giải ấy vào chạy thật.
- **Lộ trình, hình thức "Nghịch lý"** (khác MIM #1 "ba câu hỏi", #2 "ba chặng đường", #3 "lời thách", #4 "cảnh hẹn trước"): "Cỗ máy được bạn chấm điểm cẩn thận thì bị cất đi; cỗ máy hiếm khi hỏi bạn lại thành thứ bạn lướt mỗi ngày. Video này đi tìm lời giải cho nghịch lý ấy." Không đếm số câu hỏi, không liệt kê chương. Lời giải trả ở ch5 (giữa video). Kèm một lời hứa thực hành ("cuối video… dạy lại bảng tin") → trả ở ch8.
- **Vòng mở:** nghịch lý chấm sao vs không cần hỏi (ch0 → ch5) · cách dạy lại bảng tin (ch0 → ch8) · Netflix đổi khác khi bài thắng giải tới tay (ch1 → ch2) · cú nhấp "nói dối" (ch2 → ch3) · hãng nói vậy, ai kiểm từ bên ngoài? (ch4 nội bộ) · hang thỏ (ch5 → ch6) · tắt hẳn thuật toán thì sao? (ch6 → ch7) · ai dạy bảng tin mỗi ngày (ch7 → ch8).
- **Mô-típ:** (a) **"Bạn chưa nói gì / câu trả lời im lặng"**: ch0 (máy hiếm khi hỏi), ch4 (dừng lại đã là câu trả lời), ch5 (việc xem trả lời thay), ch8 (lướt qua cũng là câu trả lời, câu kết). (b) **Những ngôi sao**: ch0–ch2 (chấm sao Netflix), ch3 (YouTube hỏi lại 1–5 sao, "ngôi sao lùi xuống làm giám khảo"), ch5 ("ngôi sao chỉ là điều bạn nói"; Netflix bỏ năm sao 05/04/2017 chỉ còn trên hình), ch8 (câu kết). (c) **Hai mươi phút / một phần trăm nghìn**: ch0, ch5, ch8.
- **Cảnh mạnh thứ hai (~67–74%, đỉnh "bot chỉ nghe theo đề xuất lại xem ôn hoà hơn người thật"):** thí nghiệm "bot phản thực tế" (PNAS 2024), đặt cạnh nghiên cứu 2020 của cùng một nhà khoa học; nối sang thí nghiệm tắt thuật toán (Science 2023) ở ch7.
- **Trung thực:** chỉ nói điều các hãng tự công bố (blog, bài báo, trang trợ giúp) hoặc nhà nghiên cứu đo được; không suy đoán "công thức bí mật"; nói rõ hãng công bố nguyên liệu, không công bố trọng số; các nghiên cứu hang thỏ **bất đồng**, nêu cả hai phía + năm + phạm vi (YouTube, Mỹ); số YouTube tự công bố nói rõ là của YouTube; không dự báo; không có con số người dùng TikTok Việt Nam (chưa có nguồn chính thức thống nhất).

---

## CH00 · Hai mươi phút, một triệu đô

Ngày 26 tháng 7 năm 2009, một cuộc thi kéo dài gần ba năm bước vào những phút cuối cùng.
Giải thưởng là một triệu đô la, do Netflix treo từ năm 2006, khi hãng còn chỉ cho thuê đĩa phim qua bưu điện.
Đề bài nghe rất đơn giản: đoán xem mỗi khách hàng sẽ chấm một bộ phim mấy sao.
Ai đoán chính xác hơn hệ thống của chính Netflix mười phần trăm, người ấy thắng. ‖
Hơn bốn mươi nghìn đội, từ một trăm tám mươi sáu quốc gia, đã nộp bài.
Đến ngày cuối, hai liên minh dẫn đầu cùng vượt vạch mười phần trăm.
Hai mươi bốn phút trước giờ đóng cửa, đội BellKor's Pragmatic Chaos nộp bài.
Hai mươi phút sau, đội The Ensemble nộp bài của mình. ‖
Trên bảng xếp hạng công khai, The Ensemble nhỉnh hơn một chút.
Nhưng giải thưởng được chấm trên một phần dữ liệu khác, giữ kín.
Ở đó, hai đội bằng điểm nhau, tới tận chữ số thập phân thứ tư.
Ban giám khảo mất vài tuần để kiểm tra lại. Theo luật, bài nộp trước thắng. ‖
Hai mươi phút, đáng giá một triệu đô.
Nhưng chi tiết lạ nhất đến sau đó.
Netflix nhận về cỗ máy thắng giải, rồi không đưa bản thắng giải ấy vào chạy thật.
Còn hôm nay, TikTok hay YouTube hiếm khi hỏi bạn chấm một video mấy sao.
Vậy mà bạn vẫn hay có cảm giác chúng biết bạn thích gì. ‖
Cỗ máy được khách hàng chấm điểm cẩn thận thì bị cất đi.
Cỗ máy hiếm khi hỏi bạn câu nào lại thành thứ bạn lướt mỗi ngày.
Video này đi tìm lời giải cho nghịch lý ấy.
Và ở cuối video, mình sẽ chỉ bạn cách dạy lại bảng tin của chính mình.
Bắt đầu từ cách những cỗ máy này nghĩ: chúng không cần hiểu bạn, chỉ cần tìm ra người giống bạn.

## CH01 · Những người giống bạn

Bộ dữ liệu Netflix trao cho các đội có hơn một trăm triệu lượt chấm điểm.
Của gần nửa triệu khách hàng, cho gần mười tám nghìn bộ phim, từ năm 1998 đến năm 2005.
Mỗi dòng chỉ ghi một khách hàng đã chấm một bộ phim mấy sao, vào ngày nào.
Xếp thành một cái bảng, chín mươi chín phần trăm số ô bỏ trống.
Đề bài, thực chất, là điền vào những ô trống ấy. ‖
Ý tưởng cốt lõi có tên là lọc cộng tác. Nói đơn giản: tìm những người giống bạn.
Trang trợ giúp của TikTok có một ví dụ.
Người A thích video số một, số hai và số ba.
Người B thích cả năm video, từ số một tới số năm.
Hệ thống có thể đoán: người A cũng sẽ thích video số bốn và số năm. ‖
YouTube kể một ví dụ khác: bạn hay xem quần vợt, và những người thích đúng những video ấy cũng thích nhạc jazz.
Thế là bạn có thể được gợi ý nhạc jazz, dù chưa từng xem video jazz nào.
Máy không cần biết jazz là gì. Nó chỉ cần biết ai giống ai. ‖
Năm 2007, sau một năm thi, đội dẫn đầu nhận giải thưởng tiến bộ đầu tiên, nhờ trộn một trăm linh bảy thuật toán lại với nhau.
Netflix chọn hai thuật toán mạnh nhất trong số đó, đưa vào hệ thống thật.
Một trong hai, nói thật đơn giản, tóm mỗi người và mỗi bộ phim thành một dãy số, như một bản đồ khẩu vị.
Hai dãy số nằm gần nhau, nghĩa là gu gần nhau. ‖
Phải thêm hai năm nữa, và ba đội đối thủ gộp lại thành một, mới vượt được mốc mười phần trăm.
Và khi bài thắng giải tới tay Netflix, thì chính Netflix đã đổi khác.

## CH02 · Một triệu đô không dùng tới

Năm 2012, trên blog kỹ thuật của hãng, hai chuyên gia Netflix viết về bản thắng giải.
» Phần chính xác tăng thêm mà chúng tôi đo được có vẻ không đáng với công sức kỹ thuật để đưa vào vận hành thật. [TRÍCH DỊCH]
Một lý do, theo chính bài ấy, nằm ở hai chữ: trực tuyến. ‖
Năm 2007, một năm sau khi cuộc thi bắt đầu, Netflix mở dịch vụ xem phim trực tuyến.
Với phim trực tuyến, hãng thấy được điều mà số sao không bao giờ nói.
» Chúng tôi có thể quan sát số liệu xem, chẳng hạn một video được xem hết hay chỉ xem một phần. [TRÍCH DỊCH] ‖
Cũng trong bài ấy, hãng tự công bố: khoảng ba phần tư những gì người ta xem đến từ đề xuất.
Thật ra, ngay hôm trao giải năm 2009, Netflix đã công bố cuộc thi thứ hai.
Lần này, đoán gu của cả những người hiếm khi chấm sao, dựa vào hành vi.
Cuộc thi ấy không bao giờ diễn ra. ‖
Hai nhà nghiên cứu ở Đại học Texas đã chỉ ra rằng bộ dữ liệu "ẩn danh" của cuộc thi thứ nhất có thể bị lần ngược.
Chỉ cần đối chiếu với những lời chấm phim công khai trên trang IMDb, họ nhận ra hồ sơ Netflix của một số người dùng.
Lộ cả những sở thích có thể nhạy cảm, như quan điểm chính trị. ‖
Năm 2010, sau một vụ kiện và câu hỏi từ cơ quan quản lý của Mỹ, Netflix huỷ cuộc thi ấy.
Bài học đầu tiên: dấu vết bạn để lại khi xem nói nhiều hơn số sao bạn chấm. Và cũng riêng tư hơn.
Một công ty khác học cùng bài học ấy theo cách khác: qua những cú nhấp chuột.

## CH03 · Cú nhấp biết nói dối

Năm 2021, ông Cristos Goodrow, người hơn mười năm xây hệ thống đề xuất của YouTube, kể lại.
Năm 2008, YouTube xếp video theo độ phổ biến, thành một trang Thịnh hành chung cho mọi người.
Rồi họ dựa vào cú nhấp: bấm vào tức là muốn xem. ‖
Năm 2011, họ nhận ra bấm vào không có nghĩa là đã thật sự xem.
Ví dụ của chính ông: bạn tìm đoạn video trận đấu ở Wimbledon.
Ảnh và tiêu đề hứa có cảnh trận đấu. Bấm vào, chỉ là một người ngồi trong phòng ngủ bình luận.
Năm 2012, YouTube đưa thời gian xem vào hệ thống. ‖
Năm 2016, ba kỹ sư Google mô tả hệ thống đề xuất của YouTube tại hội nghị chuyên ngành RecSys.
Họ viết thẳng:
» Xếp hạng theo tỉ lệ nhấp thường đẩy lên những video đánh lừa, mà người xem không xem hết. Còn thời gian xem phản ánh sự quan tâm tốt hơn. [TRÍCH DỊCH]
Dù có nút thích, nút không thích và khảo sát, mô hình trong bài được dạy chủ yếu bằng việc xem.
Người dùng xem hết một video được tính là một ví dụ tích cực, vì dấu vết xem nhiều hơn những cú bấm chủ động gấp bội. ‖
Hệ thống chạy qua hai vòng.
Vòng một lọc từ hàng triệu video xuống còn vài trăm.
Vòng hai chấm điểm từng video, xếp lại, để vài chục video hiện lên màn hình của bạn. ‖
Và có một chi tiết làm mình bất ngờ.
Để biết video có thật sự đáng xem không, YouTube hỏi lại: chấm từ một đến năm sao.
Chỉ những video được bốn hoặc năm sao mới tính là thời gian xem có giá trị. Ai không trả lời, máy đoán hộ câu trả lời.
Những ngôi sao của Netflix chưa biến mất. Chúng chỉ lùi xuống làm giám khảo. ‖
Còn ở TikTok, câu chuyện bắt đầu từ ngón tay cái của bạn.

## CH04 · Bạn chưa nói gì

Tháng 6 năm 2020, TikTok giải thích cách bảng tin Đề xuất chọn video.
Khi bạn mới vào, họ có thể mời bạn chọn vài chủ đề, như thú cưng hay du lịch.
Bỏ qua cũng được: máy sẽ bắt đầu bằng những video đang phổ biến.
Rồi mọi thứ bạn làm đều thành tín hiệu: bạn thích video nào, xem hết video nào, lướt qua video nào. ‖
TikTok viết rằng các tín hiệu nặng nhẹ khác nhau.
» Xem hết một video dài từ đầu tới cuối là dấu hiệu mạnh, được tính nặng hơn dấu hiệu yếu như ở cùng nước với người làm video. [TRÍCH DỊCH]
Trang trợ giúp năm nay của TikTok viết:
» Với phần lớn người dùng, các tương tác, có thể gồm thời gian xem một video, thường được tính nặng hơn các yếu tố khác. [TRÍCH DỊCH]
Bấm nút chia sẻ, chọn "Tại sao đăng bài này hiển thị", bạn có thể thấy một lý do rất thật thà.
» Video này dài hơn và có vẻ như bạn thích những video dài hơn. ‖
Bạn chưa nói gì. Chưa bấm gì.
Bạn chỉ dừng lại xem. Và việc dừng lại ấy đã là một câu trả lời. ‖
Nhưng đó là lời của chính hãng. Có ai kiểm tra từ bên ngoài không? ‖
Năm 2022, hai nhà nghiên cứu ở Thuỵ Sĩ dựng những tài khoản tự động trên TikTok để thử.
Họ thử từng yếu tố một: ngôn ngữ và vị trí, follow và thả tim, rồi thời gian xem.
Kết quả: yếu tố nào cũng làm bảng tin thay đổi.
Mạnh nhất là follow, rồi tới thả tim, rồi mới tới tỉ lệ xem. ‖
Nghĩa là bức tranh không đơn giản là "cứ xem lâu là xong".
Chính YouTube cũng viết rằng hệ thống không có cuốn sách công thức nào, và mỗi tín hiệu nặng nhẹ tuỳ từng người.
Các hãng công bố nguyên liệu. Họ không công bố công thức.

## CH05 · Lời giải của nghịch lý

Giờ quay lại hai mươi phút ở cuối cuộc thi Netflix.
Trên thang đo sai số, hai đội lệch nhau đúng một phần trăm nghìn.
Cả thế giới đã đua nhau đoán những ngôi sao cho thật chính xác.
Nhưng ngôi sao chỉ là điều bạn nói về một bộ phim. ‖
Còn thứ các cỗ máy đề xuất hôm nay dựa vào nhiều nhất, theo chính lời các hãng, là điều bạn làm.
Bạn xem gì, xem bao lâu, và lướt qua gì.
Đó là lời giải của nghịch lý. Máy không cần hỏi, vì việc xem của bạn đã trả lời thay. ‖
Còn YouTube viết năm 2021 rằng đề xuất mang lại một phần đáng kể lượt xem, nhiều hơn cả kênh đã đăng ký hay tìm kiếm.
Nhưng nếu một cỗ máy cứ đi theo chỗ bạn dừng lại lâu, sẽ có một câu hỏi đáng lo hơn.
Nó có kéo bạn, từng video một, xuống một cái hang thỏ không?

## CH06 · Hang thỏ

"Hang thỏ" là cảm giác video này dẫn tới video khác, mỗi lúc một cực đoan hơn.
Năm 2019, một nhóm ở Thuỵ Sĩ và Brazil, do Manoel Horta Ribeiro đứng tên đầu, kiểm tra giả thuyết ấy trên YouTube.
Họ phân tích hơn ba trăm ba mươi nghìn video, từ kênh báo chí chính thống tới kênh cực hữu.
Qua bảy mươi hai triệu bình luận, họ thấy người dùng đều đặn đi từ nội dung ôn hoà hơn sang nội dung cực đoan hơn. ‖
Nhưng bình luận khó cho biết người xem tự tìm đến, hay được máy dẫn đến.
Cũng năm 2019, YouTube bắt đầu giảm đề xuất loại nội dung họ gọi là sát lằn ranh: chưa vi phạm quy định, nhưng gần vi phạm.
YouTube tự công bố: ở Mỹ, thời gian xem loại này qua đề xuất giảm bảy mươi phần trăm. ‖
Một nghiên cứu năm 2023 theo dõi hơn một nghìn người tình nguyện trong năm 2020.
Video từ các kênh cực đoan tập trung ở một nhóm nhỏ, vốn đã mang nặng ác cảm về giới và chủng tộc. Họ thường tự đăng ký kênh, hoặc bấm link từ nơi khác.
Người không đăng ký thì hiếm khi được dẫn tới đó. ‖
Rồi đến thí nghiệm mà mình thấy khéo nhất.
Năm 2024, trên tạp chí PNAS, một nhóm có chính Manoel Horta Ribeiro dùng thứ họ gọi là bot phản thực tế.
Một bot lặp lại đúng lịch sử xem của một người thật.
Ba bot khác cùng xem sáu mươi video đầu ấy, rồi từ đó chỉ bấm theo đề xuất của YouTube. ‖
Kết quả: trung bình, bot chỉ nghe theo đề xuất lại xem ít nội dung thiên lệch chính trị hơn người thật.
Các tác giả kết luận: ít nhất từ sau thay đổi năm 2019, chính sở thích của người xem quyết định phần lớn họ xem gì.
Còn đề xuất, nếu có tác động, lại kéo về phía ôn hoà. ‖
Nhưng chưa nên kết luận vội.
Cũng năm 2023, một nhóm khác dùng một trăm nghìn tài khoản giả trên YouTube.
Họ thấy đề xuất nghiêng về quan điểm sẵn có, càng đi sâu càng rõ với tài khoản thiên hữu, dù không cực đoan dần lên. ‖
Các nghiên cứu này khác nhau về năm, về cách đo, và phần lớn chỉ xét YouTube, ở Mỹ.
Câu trả lời trung thực nhất lúc này: hang thỏ có thể có, nhưng không phải ai cũng bị kéo xuống.
Và thuật toán không phải lực duy nhất. Vậy nếu tắt hẳn thuật toán đi thì sao?

## CH07 · Tắt thuật toán đi

Đã có người thử, ở quy mô lớn.
Mùa bầu cử Mỹ năm 2020, các nhà khoa học phối hợp với Meta làm một thí nghiệm kéo dài ba tháng.
Một nhóm người dùng Facebook và Instagram tình nguyện được chuyển sang bảng tin xếp theo thời gian: bài mới nhất lên đầu, không có thuật toán xếp hạng. ‖
Kết quả, công bố năm 2023 trên tạp chí Science, có ba điều đáng chú ý.
Thứ nhất: họ dùng ứng dụng ít hẳn đi.
Thứ hai: họ gặp nhiều nội dung chính trị hơn, và nhiều nội dung từ nguồn kém tin cậy hơn, so với thuật toán thời điểm đó.
Thứ ba: sau ba tháng, mức độ phân cực và các quan điểm chính trị của họ không thay đổi đáng kể. ‖
Tắt thuật toán không tự động làm bảng tin sạch hơn. Nó chỉ làm bảng tin khác đi.
Ở châu Âu, từ tháng 8 năm 2023, theo Đạo luật Dịch vụ số, TikTok cho người dùng tắt cá nhân hoá.
Khi ấy, bảng tin Đề xuất chỉ còn những video đang phổ biến, ở nơi bạn sống và trên thế giới.
Nhưng theo trang trợ giúp của TikTok, tính năng này chỉ có ở Liên minh châu Âu và vài nơi khác. Không có Việt Nam. ‖
Ở Việt Nam, chuyện này đã lên tới cơ quan quản lý.
Tháng 4 năm 2023, Bộ Thông tin và Truyền thông nêu việc TikTok dùng thuật toán để tạo xu hướng, phát tán nội dung giật gân, câu view.
Tháng 10 năm 2023, sau hơn bốn tháng kiểm tra toàn diện, Bộ công bố kết luận.
Trong đó có yêu cầu: không dùng thuật toán để tạo xu hướng hay đề xuất tới người dùng những nội dung vi phạm pháp luật Việt Nam. ‖
Luật có thể vạch ra giới hạn.
Nhưng mỗi ngày, bảng tin của bạn vẫn được dạy bởi một người rất quen: chính bạn.

## CH08 · Dạy lại bảng tin của bạn

Tin tốt là cả YouTube lẫn TikTok đều có nút để bạn nói thẳng với máy. Mình gom lại thành ba việc.
Việc thứ nhất: nói "không" cho rõ ràng.
Trên YouTube, bấm dấu ba chấm cạnh video, chọn "Không quan tâm", hoặc "Không đề xuất kênh này".
Trên TikTok, nhấn giữ video, chọn "Không quan tâm".
Lướt qua thật nhanh cũng là một câu trả lời: nó nằm ngay trong danh sách tín hiệu TikTok công bố. ‖
Việc thứ hai: dọn lịch sử.
Trên YouTube, bạn có thể xoá từng video khỏi nhật ký xem.
Hoặc tạm tắt nhật ký khi tìm hiểu một chủ đề mình không thật sự quan tâm, như khi làm bài tập ở trường.
Nếu xoá và tắt hết nhật ký xem, trang chủ YouTube sẽ không còn video đề xuất nữa.
Trên TikTok, trong phần cài đặt, mục Tùy chọn nội dung, có nút "Làm mới bảng tin Đề xuất".
Máy cho bạn xem vài video phổ biến, để học lại gu của bạn. Làm mới rồi thì không hoàn tác được. ‖
Việc thứ ba: chủ động chọn.
TikTok có "Quản lý chủ đề": kéo thanh trượt để xem nhiều hơn hay ít hơn từng chủ đề, như thể thao hay ẩm thực.
Có cả "Lọc từ khoá", để chặn những video chứa những chữ bạn không muốn thấy.
Đừng mong bảng tin đổi hẳn sau một lần bấm. Nhưng nó cũng không nhớ mãi.
Trong nghiên cứu công bố năm 2024, khi bot chuyển sang xem nội dung ôn hoà, cột đề xuất bên cạnh video quên sở thích cũ sau chừng ba mươi video.
Trang chủ thì đổi chậm hơn. ‖
Netflix từng trả một triệu đô để đoán bạn sẽ chấm một bộ phim mấy sao.
Hai mươi phút quyết định ai nhận giải.
Hoá ra những ngôi sao không phải thứ quý nhất. Thứ quý nhất là những giây bạn dừng lại.
Máy không hiểu bạn như một người bạn. Nó chỉ thấy bạn giống ai, và bạn dừng ở đâu.
Nên muốn có một bảng tin tốt hơn, không cần ghét thuật toán. Chỉ cần dừng lại đúng chỗ.
Vậy mình hỏi bạn: video gần nhất khiến bạn giật mình, kiểu "sao nó biết mình thích cái này", là video gì?
Để lại ở phần bình luận nhé. ‖

---

## Ghi chú

**Tựa (3 phương án cho Test & Compare, có từ khoá "thuật toán"/"AI"):**
1. *Thuật Toán Đề Xuất: Vì Sao TikTok Và YouTube Biết Bạn Thích Gì?* (tựa chính; khớp câu người Việt tự gõ "thuật toán TikTok", "vì sao TikTok biết mình thích gì")
2. *AI Đoán Bạn Thích Gì Như Thế Nào? Từ Cuộc Thi 1 Triệu Đô Của Netflix Tới TikTok*
3. *Bạn Chưa Nói Gì, Thuật Toán Đã Đoán: Cách Dạy Lại Bảng Tin TikTok, YouTube* (bản 2, theo factcheck: "đã biết" mạnh hơn điều video chứng minh — máy đoán từ hành vi)

(Không viết "TikTok đọc được suy nghĩ", "thuật toán bí mật", "thao túng": không có nguồn. Không nêu "3 giây" — hook ở topic-research §3.1 #6 không có nguồn cho con số này.)

**Số tự tính (đối chiếu hồ sơ mục 4):**
- Netflix Prize: mở 02/10/2006 [F]; đóng 26/07/2009; công bố 21/09/2009 [PR]. "Gần ba năm" = 2 năm 10 tháng ✓.
- BellKor's Pragmatic Chaos nộp **24 phút trước khi đóng** (thông cáo Netflix) [PR]; The Ensemble nộp **20 phút sau** (Feuerverger, He & Khatri, Statistical Science 2012) [F] → The Ensemble nộp ~4 phút trước khi đóng. Hai nguồn khớp nhau.
- Bảng công khai (quiz): The Ensemble 0,8553 < BPC 0,8554 (RMSE thấp hơn = tốt hơn) → "nhỉnh hơn một chút" ✓. Bộ test (giữ kín): cả hai 0,8567; sáu chữ số: 0,856704 vs 0,856714 → lệch 0,00001 = "một phần trăm nghìn" ✓; luật làm tròn 4 chữ số → hoà, bài nộp trước thắng [F].
- Mục tiêu: RMSE ≤ 90% × 0,9525 = 0,8572 ✓ (blog Netflix 2012 + [F]). 0,8567 = cải thiện 10,06% ✓.
- Dữ liệu: 100.480.507 lượt chấm ("hơn một trăm triệu"); 480.189 khách ("gần nửa triệu"); 17.770 phim ("gần mười tám nghìn"); 10/1998–12/2005; ma trận ~99% trống [F].
- Giải tiến bộ 2007: KorBell 8,43%, >2.000 giờ, 107 thuật toán; Netflix đưa SVD + RBM vào sản phẩm [N12].
- 40.000 đội, 186 nước [PR]. BPC = gộp 3 đội, 7 thành viên (Áo, Canada, Israel, Mỹ) [PR].
- Netflix 2012: "75% of what people watch is from some sort of recommendation" → "khoảng ba phần tư" ✓ [N12].
- YouTube: 2008 xếp theo phổ biến; 2011 bài học cú nhấp; 2012 thêm watch time; 2019 hạ borderline → −70% (Mỹ, đề xuất không đăng ký); 80 tỉ tín hiệu; khảo sát 1–5 sao, chỉ 4–5 sao = valued watchtime [Y21].
- Covington et al. 2016: hàng triệu → hàng trăm → hàng chục (Hình 2); "a user completing a video is a positive example"; "orders of magnitude more implicit user history" → "nhiều đến mức không cùng tầm" [C16].
- Ribeiro et al.: 330.925 video, 349 kênh, 72 triệu+ bình luận, khuyến nghị đo 05–07/2019, công bố FAT* 01/2020 → lời đọc "năm 2019… kiểm tra" (thời điểm thu thập/arXiv 22/08/2019) [R20].
- Chen et al.: n = 1.181, dữ liệu 2020, công bố 30/08/2023 [CH23]. Haroon et al.: 100.000 sock puppet; tối đa 2,5%; 36,1% tài khoản → "hơn một phần ba" [H23]. Hosseinmardi et al.: PNAS 13/02/2024; ~30 video [HM24]. Thiết kế (Methods, arXiv 2308.10398v2): mỗi lần thử **4 bot** đăng nhập cùng xem **60 video đầu** trong lịch sử xem (máy tính, 10/2021–12/2022) của một người thật; rồi **1 bot đối chứng** xem tiếp 60 video của chính người ấy, **3 bot phản thực tế** theo quy tắc: "up next" (video đầu cột bên) / ngẫu nhiên trong 30 video đầu cột bên / ngẫu nhiên trong 15 video đầu trang chủ. 125 người, 1.304 quỹ đạo; thí nghiệm chạy đầu năm 2023. Thí nghiệm "quên sau ~30 video" (ch8) là thiết kế khác, 2 bot.
- Guess et al.: Science 27/07/2023; 3 tháng; bầu cử Mỹ 2020 [G23].
- Bộ TT&TT: họp báo 06/04/2023 (đánh giá thuật toán tạo xu hướng); kiểm tra từ 15/05/2023; công bố kết luận 05/10/2023 ("sau hơn 4 tháng") [VN1][VN2].

**Bản 2 (09/10/2026, theo factcheck.md):** áp 8 bản SỬA (L28, L76, L81, L167, L173, L186, L210, L216 của bản 1) và cả ba mục cắt theo thứ tự (a) "Năm 2017, chính Netflix bỏ hẳn thang năm sao…" → (b) cặp câu Haroon "Đề xuất từ các kênh có vấn đề…" (cắt cùng bản SỬA L173; 2,5% / 36,1% giữ trên hình) → (c) "Thời thuê đĩa…". Ước ~3.068 âm tiết đọc đủ (factcheck mục 4). Hai mục bù nếu TTS nháp vẫn > ~14 phút: (d) vế "so với thuật toán thời điểm đó" (CH07) lên thẻ hình; (e) cắt "Nghĩa là bức tranh không đơn giản là 'cứ xem lâu là xong'." (CH04).

**Ước lượng độ dài (bản 1; đếm thô `script_lines.py` / đọc đủ chữ, vd. "2009" = 6 âm tiết):**

| Chương | Câu | Thô | Đọc đủ | % lũy kế |
|---|---:|---:|---:|---:|
| CH00 Hai mươi phút, một triệu đô | 22 | 326 | ~338 | 11% |
| CH01 Những người giống bạn | 19 | 309 | ~324 | 21% |
| CH02 Một triệu đô không dùng tới | 17 | 311 | ~332 | 32% |
| CH03 Cú nhấp biết nói dối | 20 | 325 | ~354 | 43% |
| CH04 Bạn chưa nói gì | 20 | 324 | ~335 | 54% |
| CH05 Lời giải của nghịch lý (re-hook) | 11 | 179 | ~191 | 60% |
| CH06 Hang thỏ (cảnh mạnh thứ hai) | 24 | 457 | ~500 | 76% |
| CH07 Tắt thuật toán đi | 17 | 321 | ~350 | 87% |
| CH08 Dạy lại bảng tin của bạn | 24 | 385 | ~391 | 100% |
| **Tổng** | **174** | **2.937** | **~3.115** | ≈ 13,8 phút ở 225 âm tiết/phút (nhịp đo của MIM #4) |

Nếu TTS nháp > 14,5 phút, cắt theo thứ tự: (a) câu "Năm 2017, chính Netflix bỏ hẳn thang năm sao…" (ch5, [SECONDARY]); (b) cặp câu Haroon "Đề xuất từ các kênh có vấn đề…" (ch6, giữ trên hình); (c) câu "Thời thuê đĩa…" (ch2). Đã cắt khỏi bản 1 (giữ trong hồ sơ): "80 tỉ tín hiệu" (YouTube 2021), "2.000 giờ / 8,43%" (giải tiến bộ 2007), "số người theo dõi không phải yếu tố trực tiếp" (TikTok 2020), "không hai video liền nhau cùng người/cùng nhạc" (TikTok 2020).

**Khoá `say` cần thêm vào spec.json** (khoá viết thường, `=` là khớp nguyên từ):
`netflix` Nét-phlích · `bellkor's` Ben-co · `pragmatic` Prắc-ma-tích · `chaos` Kê-ọt · `the`/`ensemble` Đơ / An-xam-bồ · `tiktok` Tíc-tóc · `youtube` Diu-túp · `jazz` Giát · `wimbledon` Uim-bồn-đần · `cristos` Crít-tốt · `goodrow` Gút-râu · `google` Gu-gồ · `recsys` Réc-xít · `imdb` Ai-em-đi-bi · `manoel` Ma-nu-eo · `horta` Óc-ta · `ribeiro` Ri-bây-rô · `pnas` Pi-en-ây-ét · `meta` Mê-ta · `facebook` Phây-búc · `instagram` In-xta-gram · `science` Xai-ần · `texas` Tếch-xát · `brazil` Bra-xin · `follow` phô-lô · `bot` bót · `link` linh · `view` viu · `blog` bờ-lóc. (`=2,5` thừa từ bản 2: câu Haroon đã cắt.)
Thử giọng trước: "BellKor's Pragmatic Chaos", "The Ensemble", "Wimbledon", "Horta Ribeiro", "IMDb", "RecSys", "bot", "câu view", "blog". Kiểm "1998", "2009" đọc đúng.

**Nhãn trên hình cần có:**
- [TRÍCH DỊCH] Netflix Tech Blog, 06/04/2012 (X. Amatriain, J. Basilico): "…the additional accuracy gains that we measured did not seem to justify the engineering effort needed to bring them into a production environment." · "…we can observe viewing statistics such as whether a video was watched fully or only partially."
- [TRÍCH DỊCH] Covington, Adams, Sargin, RecSys 2016: "Ranking by click-through rate often promotes deceptive videos that the user does not complete ("clickbait") whereas watch time better captures engagement." (Lời đọc dịch "clickbait" thành "video đánh lừa, mà người xem không xem hết".)
- [TRÍCH DỊCH] TikTok Newsroom, 18/06/2020: "A strong indicator of interest, such as whether a user finishes watching a longer video from beginning to end, would receive greater weight than a weak indicator, such as whether the video's viewer and creator are both in the same country." (lời đọc dịch gọn).
- [TRÍCH DỊCH] TikTok Support, "How TikTok recommends content" (đọc 09/10/2026): "For most users, user interactions, which may include the time spent watching a video, are generally weighted more heavily than others."
- [TRÍCH] (không phải TRÍCH DỊCH) TikTok Support (tiếng Việt), "Đề xuất": "Video này dài hơn và có vẻ như bạn thích những video dài hơn." (nguyên văn tiếng Việt của TikTok — hiện đúng chữ, không dịch).
- Bảng xếp hạng **dựng lại bằng chữ** (không chụp website): BellKor's Pragmatic Chaos — quiz 0,8554 / test 0,8567 · The Ensemble — quiz 0,8553 / test 0,8567; nhãn "Nguồn: Feuerverger, He & Khatri, Statistical Science 2012; thông cáo Netflix 21/09/2009". Không ghi giờ:phút cụ thể (chưa đọc bảng gốc): ghi "24 phút trước giờ chốt" / "20 phút sau".
- Bảng 3×5 "người A / người B / video 1–5" (ví dụ của TikTok Support); sơ đồ phễu "hàng triệu → vài trăm → vài chục" (vẽ lại theo Hình 2 của Covington et al.).
- Thanh "0,856704 / 0,856714" ở ch5.
- Biểu đồ: "−70% (Mỹ, YouTube tự công bố, 2019)"; "1.181 người (2020)"; "100.000 tài khoản giả · tối đa 2,5% · 36,1% gặp · tỉ lệ tăng dần theo độ sâu" (thay cho câu đã cắt); "75% · Netflix tự công bố, 2012"; "Netflix bỏ 5 sao, 05/04/2017" (thay câu cắt (a)). Sơ đồ bot ch6 = **1 + 3 nhánh**: 60 video học chung → bot đối chứng (lịch sử thật) + 3 bot phản thực tế (up next / ngẫu nhiên 30 đầu cột bên / ngẫu nhiên 15 đầu trang chủ), nhãn "Mỹ · máy tính · thí nghiệm đầu 2023 · PNAS 2024". Sơ đồ **hai bot** chỉ dùng cho kết quả "quên sau ~30 video" (ch8).
- Science 2023: ba thẻ "ÍT DÙNG HƠN · NHIỀU NỘI DUNG CHÍNH TRỊ + NGUỒN KÉM TIN CẬY HƠN · PHÂN CỰC: KHÔNG ĐỔI ĐÁNG KỂ" + nhãn "Facebook/Instagram, Mỹ, 3 tháng, 2020".
- Ch8: **mô phỏng** menu, nhãn "MÔ PHỎNG GIAO DIỆN" (dựng bằng chữ theo trang trợ giúp, không chụp app thật, không logo): YouTube "Không quan tâm" / "Không đề xuất kênh này" / "Tạm dừng lưu nhật ký xem" (nhãn app Android VI; không ghi "Tắt nhật ký"); TikTok "Không quan tâm" / "Cài đặt và quyền riêng tư → Tùy chọn nội dung → Làm mới bảng tin Đề xuất" / "Quản lý chủ đề" / "Lọc từ khóa". Nhãn "Theo trang trợ giúp YouTube/TikTok, 10/2026 — giao diện có thể khác theo phiên bản".
- Không logo TikTok/YouTube/Netflix làm chủ thể; không chiếu video của nhà sáng tạo thật; không mặt người thật của các nhóm thi (ảnh báo chí có bản quyền).

**Cần kiểm lại trước khi thu âm:**
1. **Giờ nộp bài Netflix Prize**: "24 phút trước khi đóng" (thông cáo Netflix) và "20 phút sau" (Feuerverger, He & Khatri 2012) khớp nhau; TechCrunch "4 phút trước khi đóng" cũng khớp. Bảng xếp hạng gốc **vẫn chưa mở được** (Wayback 429) → giữ quyết định không hiện giờ:phút.
2. **Thiết kế "bot phản thực tế"** (ch6): **đã chốt** bằng Methods (arXiv 2308.10398v2): 4 bot, 60 + 60 video, 1 đối chứng + 3 quy tắc → lời đọc bản 2 "Ba bot khác cùng xem sáu mươi video đầu ấy…".
3. **Nhãn giao diện tiếng Việt TikTok** ("Không quan tâm", "Làm mới bảng tin Đề xuất", "Quản lý chủ đề", "Lọc từ khóa", "Tại sao đăng bài này hiển thị") lấy từ trang trợ giúp TikTok bản tiếng Việt 09/10/2026; đường dẫn tiếng Việt chính thức "Cài đặt và quyền riêng tư → Tùy chọn nội dung → Làm mới bảng tin Đề xuất". Còn phải mở app thật kiểm "Tại sao đăng bài này hiển thị" / "Tại sao lại là video này" và cử chỉ "nhấn giữ → Không quan tâm" (có trong bài 2020).
4. **Netflix bỏ năm sao (2017)**: nguồn gốc *Goodbye Stars, Hello Thumbs*, about.netflix.com, 05/04/2017. Câu đã cắt (mục cắt (a), vì thời lượng); ý giữ trên hình.
5. **Huỷ cuộc thi thứ hai (2010)**: thư khép hồ sơ của FTC 12/03/2010 (Netflix *"intended to suspend plans for Prize 2"*); *Doe v. Netflix* (N.D. Cal., 17/12/2009) và blog Neil Hunt vẫn [SECONDARY]; Feuerverger, He & Khatri 2012 xác nhận. Lời đọc "một vụ kiện và câu hỏi từ cơ quan quản lý của Mỹ" = FTC.
6. Danh sách nơi có nút tắt cá nhân hoá: trang "How TikTok recommends content" ghi "EU and Kazakhstan"; trang "For You" ghi "EEA, the UK, or Switzerland" → lời đọc "Liên minh châu Âu và một vài nơi khác. Việt Nam không có trong danh sách" đúng với cả hai.
