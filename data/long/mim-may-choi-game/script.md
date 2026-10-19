# MÁY THẮNG GAME THỜI GIAN THỰC: ALPHASTAR, OPENAI FIVE VÀ NĂM ĐIỀU CỜ VUA KHÔNG CÓ (bản 1)

**Kênh:** Mind in the Machine (MIM) · **Chuỗi:** Trận đấu Người – Máy · **Giọng:** Thanh Bình (dẫn) · Ngọc Huyền (`»` lời trích)
**Độ dài dự kiến:** ~21 phút, 19 chương (video dài loại 20–30 phút, thứ Năm)
**Tiêu đề (phương án):** (1) *Máy thắng game thời gian thực: AlphaStar, OpenAI Five và năm điều cờ vua không có* · (2) *Từ cờ vua tới StarCraft
và Dota 2: vì sao game điện tử khó cho máy hơn cờ* · (3) *Hai trăm năm chơi game trong mười bốn ngày: cỗ máy thắng tuyển thủ chuyên nghiệp thế nào*
Quy ước: mỗi dòng là một câu đọc · `‖` = ngừng dài · `»` = lời trích.
**Viết cho tai + luật studio (14/10/2026):** câu một hơi, không câu nào quá ba mươi lăm tiếng, câu ngắn xen kẽ, liệt kê tối đa ba mục.
**Trung thực:** số liệu AlphaStar theo hai bài blog của DeepMind (24/01/2019 và 30/10/2019); OpenAI Five theo Wikipedia và báo chí (trang OpenAI không
đọc được trực tiếp) → các con số "bốn mươi lăm nghìn năm", "mười tháng", "bảy nghìn hai trăm mười lăm thắng" ghi "theo OpenAI, qua báo chí" · không
khẳng định máy "chơi gian" hay "không gian"; nêu đủ hai phía về tốc độ và tầm nhìn · không nêu tên thật đời thường của tuyển thủ ngoài tên thi đấu
đã công khai.
**Giữ chân:** cold open = **mười một ván, một người thắng duy nhất** · **lộ trình dạng "năm điều cờ vua không có", đánh dấu dần** (khác MIM trước:
ba câu nói, ba thanh độ tự tin, ba lá bài úp, bốn trạm, phiên toà, bảng tỉ số…) · **vòng mở:** ai là người thắng duy nhất và thắng thế nào (đóng
CH09) · máy có nhanh tay hơn người một cách không công bằng không (đóng CH08, CH10) · **re-hook ~50%** = Dota 2 và năm người một đội ·
**mô-típ** "sương mù".

---

## CH00 · Mười một ván

Mười một ván đấu. Một cỗ máy. Hai tuyển thủ chuyên nghiệp.
Cỗ máy thắng mười ván. ‖
Đó là kết quả DeepMind công bố cuối tháng một năm hai nghìn không trăm mười chín.
Trò chơi lần này không phải cờ vua, cũng không phải cờ vây.
Mà là StarCraft hai, một trò chơi điện tử chiến thuật thời gian thực, nơi hai người chơi xây căn cứ, gom tài nguyên, và tung quân đánh nhau. ‖
Cỗ máy ấy tên là AlphaStar.
Nó thắng tuyển thủ TLO năm ván không gỡ.
Rồi thắng tuyển thủ MaNa, một trong những người chơi giỏi nhất thế giới lúc ấy, cũng năm ván không gỡ. ‖
Nhưng có một ván thứ mười một.
Một ván đấu biểu diễn, và lần ấy, con người thắng.
Video này sẽ kể bạn nghe ván ấy diễn ra thế nào, và vì sao nó quan trọng. ‖
Ở các video trước của chuỗi, máy đã thắng người ở cờ vua, cờ vây, đố vui, và poker.
Nhưng một trò chơi điện tử có những thứ mà bàn cờ không có.
Mình sẽ đếm chúng ra, từng điều một. Có tất cả năm điều.
Và mỗi điều, là một lý do vì sao các nhà nghiên cứu từng nghĩ máy còn lâu mới thắng được.

## CH01 · Sau những bàn cờ

Năm một nghìn chín trăm chín mươi bảy, Deep Blue thắng nhà vô địch cờ vua.
Năm hai nghìn không trăm mười sáu, AlphaGo thắng Lee Sedol ở cờ vây.
Nhiều người nghĩ câu chuyện máy chơi game đến đó là xong. ‖
Nhưng với các nhà nghiên cứu, bàn cờ vẫn là một thế giới rất gọn gàng.
Hai người. Đi lần lượt. Mọi quân cờ nằm trên bàn.
Thế giới thật thì không như vậy. ‖
Thế giới thật không chờ bạn suy nghĩ xong mới chuyển động.
Bạn không nhìn thấy hết mọi thứ.
Và thường bạn không hành động một mình. ‖
Nên các phòng thí nghiệm bắt đầu tìm một sân chơi mới, giống thế giới thật hơn, nhưng vẫn có luật rõ ràng và kết quả đo được.
Họ tìm thấy nó trong những trò chơi điện tử mà hàng triệu người chơi mỗi ngày.
Hai cái tên nổi bật: StarCraft hai, và Dota hai. ‖
Hai phòng thí nghiệm, hai trò chơi, cùng trong khoảng hai năm.
DeepMind với StarCraft. OpenAI với Dota.
Và cả hai đều phải giải cùng một bài toán: những điều mà cờ vua không có.

## CH02 · Một phòng thí nghiệm an toàn

Có một câu hỏi bạn có thể đang nghĩ tới.
Sao những phòng thí nghiệm hàng đầu lại tốn nhiều công sức đến thế, chỉ để thắng một trò chơi? ‖
Câu trả lời nằm ở ba điều mà trò chơi điện tử có, còn thế giới thật thì không.
Thứ nhất, kết quả rõ ràng. Thắng hay thua, không ai phải tranh cãi.
Thứ hai, có thể chơi lại vô số lần, nhanh hơn thời gian thật rất nhiều.
Thứ ba, sai lầm không làm ai bị thương. ‖
Thử hình dung dạy một chiếc xe tự lái bằng cách cho nó tự thử và tự sai, ngoài đường thật.
Không ai cho phép điều đó.
Nhưng trong một trò chơi, cỗ máy có thể sai hàng tỷ lần, và chẳng ai bị làm sao. ‖
Đồng thời, những trò chơi chiến thuật lại có đủ những thứ khó nhất của thế giới thật.
Thông tin bị che. Đối thủ biết suy nghĩ. Kế hoạch phải kéo dài hàng giờ.
Nên trò chơi trở thành một phòng thí nghiệm hoàn hảo: đủ khó để đáng thử, đủ an toàn để được sai. ‖
Và đó là lý do câu chuyện về những trò chơi này không chỉ là chuyện của game thủ.

## CH03 · Từ những trò chơi điện tử cũ

Thật ra, DeepMind không bắt đầu với StarCraft.
Họ bắt đầu với những trò chơi điện tử cũ hơn nhiều, trên một chiếc máy chơi game từ cuối những năm bảy mươi. ‖
Tháng hai năm hai nghìn không trăm mười lăm, họ công bố trên tạp chí Nature một hệ thống tên là DQN.
Nó được thử với bốn mươi chín trò chơi Atari, những trò bắn súng, đánh bóng, lái xe đơn giản. ‖
Điều đặc biệt là cỗ máy không được dạy luật của trò nào.
Nó chỉ nhận được hình ảnh trên màn hình, danh sách các nút có thể bấm, và điểm số.
Rồi nó tự chơi, tự thử, và tự tìm ra cách để điểm số tăng lên. ‖
Theo DeepMind, hệ thống ấy giỏi hơn các phương pháp máy học trước đó ở bốn mươi ba trên bốn mươi chín trò.
Và ở hơn một nửa số trò, nó đạt trên bảy mươi lăm phần trăm điểm của một người thử nghiệm game chuyên nghiệp. ‖
Cùng một thuật toán, cùng một cấu trúc, cho tất cả các trò chơi.
Đó là lần đầu tiên nhiều người thấy rằng một cỗ máy có thể học chơi game chỉ bằng cách nhìn màn hình, như con người.
Nhưng những trò Atari ấy chỉ kéo dài vài phút, và không có đối thủ nào biết suy nghĩ.
Từ đó tới StarCraft là một bước nhảy rất xa.

## CH04 · Năm điều cờ vua không có

Hãy đặt cờ vua và một trò chơi chiến thuật thời gian thực cạnh nhau.
Rồi đếm những gì trò chơi điện tử có, mà bàn cờ không có. ‖
Điều thứ nhất: sương mù.
Trong cờ vua, bạn thấy mọi quân của đối thủ.
Trong StarCraft, phần lớn bản đồ bị che, bạn chỉ thấy những nơi quân mình đang đứng. ‖
Điều thứ hai: không có lượt.
Cờ vua cho bạn suy nghĩ rồi mới đi.
Trò chơi thời gian thực thì cứ chạy, dù bạn đã nghĩ xong hay chưa. ‖
Điều thứ ba: ván đấu rất dài.
Một ván cờ vua có vài chục nước.
Một ván StarCraft có thể kéo dài tới một giờ, với hàng chục nghìn hành động. ‖
Điều thứ tư: số lựa chọn khổng lồ ở mỗi khoảnh khắc. Mình sẽ nói kỹ ở chương sau.
Điều thứ năm: đồng đội. Có những trò chơi mà bạn không thắng một mình, mà phải phối hợp với bốn người khác. ‖
Năm điều. Sương mù, không có lượt, ván dài, lựa chọn khổng lồ, đồng đội.
Hãy nhớ danh sách này. Chúng ta sẽ đánh dấu từng điều, khi cỗ máy vượt qua nó.

## CH05 · StarCraft là gì

Nếu bạn chưa chơi StarCraft bao giờ, đây là phiên bản ngắn nhất.
Hai người chơi, mỗi người bắt đầu với một căn cứ nhỏ và vài người thợ. ‖
Thợ đi khai thác tài nguyên.
Tài nguyên dùng để xây nhà, mở công nghệ, và sản xuất quân.
Quân dùng để đi do thám, phòng thủ, và tấn công. ‖
Có ba chủng tộc, mỗi chủng tộc một kiểu quân, một kiểu chơi khác hẳn nhau.
Không có chiến thuật nào thắng tất cả.
Mỗi lựa chọn đều có một cách khắc chế. ‖
Người chơi giỏi phải làm cùng lúc rất nhiều việc.
Lo kinh tế ở nhà, điều quân ở tiền tuyến, và đoán xem đối thủ đang chuẩn bị gì sau màn sương.
Tất cả trong lúc đồng hồ vẫn chạy. ‖
Đó là lý do StarCraft được coi là một trong những môn thể thao điện tử khó nhất.
Và cũng là lý do nhiều nhà nghiên cứu coi nó là thử thách lớn tiếp theo sau cờ vây.

## CH06 · Một con số có hai mươi sáu chữ số không

Giờ là điều thứ tư trong danh sách: số lựa chọn ở mỗi khoảnh khắc.
Trong cờ vua, ở một thế cờ trung bình, bạn có khoảng vài chục nước hợp lệ. ‖
Trong StarCraft, theo DeepMind, ở mỗi bước, trung bình có khoảng mười mũ hai mươi sáu hành động hợp lệ.
Tức là số một, theo sau là hai mươi sáu chữ số không. ‖
Vì sao nhiều đến thế?
Vì mỗi hành động là một tổ hợp: chọn đơn vị nào, cho nó làm gì, và làm ở vị trí nào trên bản đồ.
Nhân những lựa chọn ấy với nhau, con số phình ra rất nhanh. ‖
Và cỗ máy phải chọn như thế, liên tục, trong một ván có thể dài tới một giờ.
Không thể duyệt hết như Deep Blue từng duyệt cờ vua.
Cũng không thể nhìn trước nhiều bước như AlphaGo, vì sương mù khiến tương lai mờ mịt hơn nhiều. ‖
Vậy cỗ máy bắt đầu học từ đâu?
Câu trả lời của DeepMind là: bắt đầu từ con người.

## CH07 · Học từ con người trước

Bước đầu tiên của AlphaStar giống cách một người mới học chơi.
Xem người khác chơi. ‖
Hãng làm ra trò chơi cung cấp cho DeepMind một kho ván đấu của người chơi thật, đã được ẩn danh.
Cỗ máy xem những ván ấy, và học bắt chước: ở tình huống này, người chơi thường làm gì. ‖
Chỉ riêng bước bắt chước này đã đủ để nó thắng trí tuệ nhân tạo dựng sẵn trong trò chơi, ở mức khó nhất, chín mươi lăm phần trăm số ván.
Theo DeepMind, mức ấy tương đương một người chơi hạng vàng. ‖
Một người chơi khá, nhưng còn rất xa mới tới chuyên nghiệp.
Bắt chước chỉ đưa cỗ máy tới ngang tầm những người nó đã xem.
Muốn vượt lên, nó cần một cách học khác. ‖
Và cách học ấy, lại quen thuộc với những ai đã xem video về AlphaGo hay máy chơi poker của kênh.
Tự chơi với chính mình.
Nhưng lần này, không phải một mình. Mà là cả một giải đấu.

## CH08 · Giải đấu của những cỗ máy

DeepMind gọi nó là AlphaStar League, giải đấu của AlphaStar.
Thay vì một cỗ máy tự chơi với bản sao của chính nó, họ tạo ra rất nhiều phiên bản, đấu với nhau liên tục. ‖
Vì sao lại cần cả một giải đấu?
Vì trong StarCraft, mỗi chiến thuật đều có cách khắc chế.
Nếu chỉ tự chơi với chính mình, cỗ máy dễ rơi vào một vòng lặp: tìm ra một mẹo, rồi chỉ giỏi chống lại đúng cái mẹo ấy. ‖
Có những phiên bản được giao nhiệm vụ riêng: chuyên đi tìm điểm yếu của các phiên bản khác.
Có phiên bản thích tấn công sớm. Có phiên bản thích phòng thủ rồi phát triển kinh tế.
Giải đấu buộc mọi phiên bản phải đối phó với đủ kiểu đối thủ. ‖
Theo DeepMind, giải đấu ấy chạy trong mười bốn ngày.
Mỗi phiên bản dùng mười sáu bộ xử lý chuyên dụng của Google.
Và trong thời gian ấy, mỗi phiên bản đã trải qua tới hai trăm năm chơi StarCraft, tính theo thời gian thật. ‖
Hai trăm năm, trong hai tuần.
Không tuyển thủ nào có thể luyện tập nhiều đến thế, dù chơi cả đời.
Và khi giải đấu kết thúc, cỗ máy được đưa ra gặp con người.

## CH09 · Phần thưởng đến muộn

Có một khó khăn mà ít người nghĩ tới khi nói về chuyện máy tự học chơi game.
Cỗ máy học bằng phần thưởng. Thắng thì được thưởng, thua thì không. ‖
Với trò Atari, điểm số tăng lên gần như ngay sau mỗi hành động tốt.
Cỗ máy dễ dàng nhận ra: bấm nút này lúc này, thì được điểm. ‖
Nhưng một ván StarCraft có thể kéo dài tới một giờ, với hàng chục nghìn hành động.
Và chỉ đến cuối ván, cỗ máy mới biết mình thắng hay thua.
Vậy trong hàng chục nghìn hành động ấy, hành động nào đã dẫn tới chiến thắng? ‖
Đó là một bài toán có tên riêng trong ngành: bài toán phân bổ công lao.
Giống như một đội bóng thắng một trận, và bạn phải đoán xem đường chuyền nào ở phút thứ mười đã góp phần vào bàn thắng ở phút thứ tám mươi. ‖
Đây chính là lý do bước học bắt chước con người ban đầu quan trọng đến thế.
Nó cho cỗ máy một điểm xuất phát hợp lý, thay vì phải đi từ những cú bấm ngẫu nhiên.
Rồi hai trăm năm chơi trong giải đấu, giúp nó dần nhận ra những gì thật sự dẫn tới chiến thắng.
Phần thưởng đến muộn. Nhưng với đủ nhiều ván đấu, nó vẫn đến.

## CH10 · Mười ván, mười trận thắng

Tháng mười hai năm hai nghìn không trăm mười tám, các trận đấu được ghi hình kín.
Đối thủ đầu tiên là TLO, một tuyển thủ chuyên nghiệp người Đức, chuyên chơi chủng tộc Zerg nhưng cũng đạt hạng cao nhất với chủng tộc Protoss. ‖
Vì AlphaStar mới chỉ học chơi Protoss, trên một bản đồ.
Nên mọi ván đều là Protoss đấu Protoss, trên cùng một bản đồ đã chọn sẵn.
Kết quả: AlphaStar thắng năm ván không gỡ. ‖
Sau khi được huấn luyện thêm một tuần, cỗ máy gặp đối thủ mạnh hơn.
MaNa, một tuyển thủ người Ba Lan, nổi tiếng chính với chủng tộc Protoss.
Lại năm ván không gỡ. ‖
Mười ván, mười trận thắng.
Tháng một năm sau, khi DeepMind công bố, giới StarCraft sững sờ.
Rồi rất nhanh, họ bắt đầu đặt câu hỏi. ‖
Không phải cỗ máy có giỏi không.
Mà là: nó thắng bằng trí óc, hay bằng đôi tay?

## CH11 · Đôi tay của cỗ máy

Trong StarCraft, có một chỉ số mà dân chơi rất quan tâm: số hành động mỗi phút.
Người chơi chuyên nghiệp có thể thực hiện vài trăm hành động mỗi phút. ‖
Theo DeepMind, trung bình AlphaStar thực hiện khoảng hai trăm tám mươi hành động mỗi phút.
Thấp hơn MaNa, khoảng ba trăm chín mươi. Và thấp hơn hẳn TLO, khoảng sáu trăm bảy mươi tám. ‖
Nghe như cỗ máy còn chậm tay hơn người.
Nhưng chính DeepMind sau đó cũng làm rõ thêm hai điều.
Con số của TLO bị đẩy cao vì một kiểu bấm phím liên tục mà dân chơi hay dùng, không phải hành động nào cũng có ích.
Và trong những khoảnh khắc giao tranh, tốc độ của cỗ máy có lúc vọt lên cao hơn cả hai tuyển thủ. ‖
Có một chuyện thứ hai, còn quan trọng hơn.
Phiên bản ấy không phải di chuyển màn hình như người chơi.
Nó nhìn thấy mọi phần bản đồ mà quân của nó đang thấy, cùng một lúc, như đang xem bản đồ thu nhỏ hết cỡ. ‖
Sương mù vẫn còn: nó không thấy được những gì quân mình không nhìn tới.
Nhưng nó không bao giờ phải quay đầu nhìn chỗ khác, như một người chơi ngồi trước màn hình.
Nhiều người cho rằng, chừng ấy là một lợi thế lớn. ‖
DeepMind không tránh câu hỏi này.
Và câu trả lời của họ đến ngay trong ván thứ mười một.

## CH12 · Ba trăm năm mươi phần nghìn giây

Còn một chi tiết nữa trong cuộc tranh luận về sự công bằng.
Đó là tốc độ phản ứng. ‖
Theo DeepMind, phiên bản năm hai nghìn không trăm mười tám có độ trễ trung bình khoảng ba trăm năm mươi phần nghìn giây, giữa lúc nhìn thấy và lúc hành động.
Tức là khoảng một phần ba giây. ‖
Con số ấy được đưa ra để cho thấy cỗ máy không phản ứng tức thì.
Nhưng trong một trò chơi mà mỗi khoảnh khắc đều quan trọng, những người chơi vẫn đặt câu hỏi.
Một phần ba giây trung bình, nhưng cỗ máy có bao giờ mệt, có bao giờ phân tâm không? ‖
Con người thì có.
Sau nửa giờ căng thẳng, tay người chơi chậm lại, mắt bỏ sót một góc bản đồ.
Cỗ máy thì ở phút thứ năm mươi vẫn tỉnh táo như phút đầu tiên. ‖
Không có cách nào làm cho người và máy hoàn toàn ngang nhau.
Chỉ có những giới hạn được thoả thuận trước, mà cả hai bên đều chấp nhận.
Và lần sau gặp lại, DeepMind đã đặt ra những giới hạn ấy chặt hơn nhiều.

## CH13 · Ván thứ mười một

DeepMind đã huấn luyện thêm một phiên bản khác.
Phiên bản này phải nhìn thế giới qua một khung màn hình, giống con người.
Muốn biết chuyện gì xảy ra ở góc kia bản đồ, nó phải di chuyển màn hình tới đó. ‖
Phiên bản ấy mới chỉ được huấn luyện bảy ngày.
Và nó gặp MaNa trong một ván đấu biểu diễn. ‖
Lần này, MaNa thắng.
Người chơi Protoss người Ba Lan, sau năm ván thua liên tiếp, đã tìm ra cách khiến cỗ máy lúng túng. ‖
Đó là ván duy nhất con người thắng trong mười một ván.
Một ván không làm thay đổi tỉ số. Nhưng nó cho thấy một điều quan trọng.
Khi cỗ máy phải chịu cùng giới hạn tầm nhìn như con người, và chưa được luyện đủ lâu, nó không còn bất khả chiến bại. ‖
Đánh dấu vào danh sách năm điều: sương mù, cỗ máy đã đối phó được.
Không có lượt và ván dài, nó cũng đã chơi được.
Nhưng câu hỏi về sự công bằng vẫn còn đó.
Và DeepMind quyết định trả lời nó theo cách khó nhất.

## CH14 · Đường lên Grandmaster

Mười tháng sau, DeepMind quay lại với một AlphaStar mới, và những luật chơi chặt hơn nhiều.
Lần này, cỗ máy phải nhìn qua khung màn hình như người. ‖
Số hành động của nó bị giới hạn: tối đa hai mươi hai hành động của cỗ máy trong mỗi năm giây.
Những giới hạn ấy được xây dựng cùng với chính tuyển thủ TLO.
Và nó phải chơi được cả ba chủng tộc, không chỉ Protoss. ‖
Rồi cỗ máy được đưa lên máy chủ chính thức của trò chơi, nơi người chơi khắp nơi xếp hạng với nhau.
Nó chơi ẩn danh, với cùng bản đồ, cùng điều kiện như mọi người. ‖
Những người gặp nó không hề biết mình đang đấu với một cỗ máy. ‖
Kết quả được công bố trên tạp chí Nature, cuối tháng mười năm hai nghìn không trăm mười chín.
AlphaStar đạt hạng Grandmaster, hạng cao nhất, với cả ba chủng tộc.
Cao hơn khoảng chín mươi chín phẩy tám phần trăm số người chơi đang có thứ hạng. ‖
Một chi tiết thú vị: chỉ riêng bước bắt chước người chơi ban đầu, phiên bản mới đã giỏi hơn tám mươi tư phần trăm người chơi.
Phần còn lại, nó tự học qua giải đấu của những cỗ máy.
Không phải nhà vô địch thế giới. Nhưng đã ở nhóm rất nhỏ những người giỏi nhất, trong điều kiện gần với con người hơn nhiều.

## CH15 · Năm người một đội

Trong khi DeepMind làm việc với StarCraft, ở San Francisco, OpenAI chọn một trò chơi khác: Dota hai.
Và Dota hai mang đến điều thứ năm trong danh sách: đồng đội. ‖
Một ván Dota có hai đội, mỗi đội năm người.
Mỗi người điều khiển một nhân vật, gọi là tướng, với những kỹ năng riêng.
Muốn thắng, cả năm phải phối hợp: ai giữ đường nào, khi nào cùng nhau đánh, khi nào rút lui. ‖
Theo các số liệu OpenAI công bố, được ghi lại trên Wikipedia, một ván Dota kéo dài khoảng tám mươi nghìn nhịp xử lý.
Mỗi nhân vật có tới một trăm bảy mươi nghìn hành động khả dĩ.
Và ở mỗi nhịp, có khoảng một nghìn hành động hợp lệ. ‖
Cũng có sương mù. Cũng không có lượt. Ván đấu cũng dài.
Nhưng giờ thêm một điều nữa: năm cỗ máy phải chơi như một đội.
Không ai ra lệnh cho ai. Mỗi cỗ máy tự quyết định, và phải đoán bốn cỗ máy kia sẽ làm gì. ‖
OpenAI đặt tên cho đội của mình là OpenAI Five, năm của OpenAI.

## CH16 · Một chọi một

Nhưng trước khi có năm, đã có một.
Tháng tám năm hai nghìn không trăm mười bảy, tại giải đấu Dota lớn nhất năm, The International. ‖
OpenAI đưa lên sân khấu một cỗ máy chỉ chơi một chọi một.
Đối thủ là Dendi, một tuyển thủ chuyên nghiệp người Ukraine, rất nổi tiếng trong cộng đồng Dota. ‖
Cỗ máy thắng.
Theo Wikipedia, nó đã học bằng cách tự chơi với chính mình trong khoảng hai tuần, tính theo thời gian thật. ‖
Một chọi một là phiên bản đơn giản hơn nhiều của Dota.
Không có đồng đội, ít lựa chọn chiến thuật hơn.
Nhưng nó cho OpenAI biết hướng đi của mình là đúng. ‖
Câu hỏi tiếp theo khó hơn rất nhiều.
Năm cỗ máy có học được cách phối hợp với nhau như năm con người không?

## CH17 · Một trăm tám mươi năm mỗi ngày

Cách OpenAI dạy năm cỗ máy, nghe thì rất đơn giản: tự chơi với chính mình, hàng trăm lần mỗi ngày, trong nhiều tháng.
Cái khác nằm ở quy mô. ‖
Theo số liệu năm hai nghìn không trăm mười tám, hệ thống chạy trên hai trăm năm mươi sáu bộ xử lý đồ hoạ, và một trăm hai mươi tám nghìn lõi xử lý.
Mỗi ngày, nó trải qua lượng ván đấu tương đương khoảng một trăm tám mươi năm chơi. ‖
Một trăm tám mươi năm, mỗi ngày.
Mỗi nhân vật được điều khiển bởi một mạng nơ-ron có bộ nhớ, để nhớ những gì vừa xảy ra trong ván. ‖
Còn chuyện phối hợp thì sao?
Không ai dạy năm cỗ máy cách chia việc.
Chúng chỉ được thưởng khi cả đội thắng, và dần dần học được rằng có những lúc phải hy sinh lợi ích riêng cho đồng đội. ‖
Tới mùa hè năm ấy, đội máy đã thắng được nhiều đội nghiệp dư mạnh.
Và OpenAI quyết định thử sức ở nơi khó nhất: The International.

## CH18 · Thất bại ở The International

Tháng tám năm hai nghìn không trăm mười tám, OpenAI Five chơi hai trận tại The International.
Một trận với đội paiN Gaming của Brazil.
Một trận với một đội tuyển gồm những cựu tuyển thủ hàng đầu Trung Quốc. ‖
Cả hai trận, đội máy đều thua. ‖
Sau trận, nhiều người kết luận: cỗ máy chỉ giỏi phản xạ, chứ chưa biết chiến lược.
OpenAI không bỏ cuộc.
Họ tiếp tục huấn luyện, thêm nhiều tháng nữa. ‖
Đây là điểm chung thú vị giữa hai câu chuyện.
AlphaStar thua ván thứ mười một. OpenAI Five thua ở The International.
Và cả hai phòng thí nghiệm đều quay lại, mạnh hơn.

## CH19 · OG, tháng tư năm hai nghìn không trăm mười chín

Ngày mười ba tháng tư năm hai nghìn không trăm mười chín, ở San Francisco.
Đối thủ của OpenAI Five lần này là OG, đội vừa vô địch The International năm trước. ‖
Nhà vô địch thế giới, đối đầu năm cỗ máy, trong một loạt trận ba ván thắng hai. ‖
OpenAI Five thắng cả hai ván đầu.
Lần đầu tiên, một trí tuệ nhân tạo đánh bại nhà vô địch thế giới ở một môn thể thao điện tử. ‖
Nhưng cũng như với AlphaStar, câu chuyện có những dòng chữ nhỏ.
Ván đấu được chơi với một số giới hạn: số tướng được chọn ít hơn rất nhiều so với trò chơi đầy đủ, và một vài cơ chế bị tắt đi.
Có bài báo thậm chí gọi chiến thắng ấy là gần như gian lận, vì kho tướng bị đơn giản hoá ở cả hai bên. ‖
Đội OG chơi một phiên bản Dota mà họ không quen.
Còn cỗ máy chơi đúng phiên bản mà nó đã luyện hàng nghìn năm.
Đánh giá chiến thắng ấy thế nào, tuỳ bạn nhìn vào tỉ số, hay vào luật chơi.

## CH20 · Bốn ngày, bốn mươi hai nghìn ván

Ngay sau trận đấu với OG, OpenAI làm một điều mà DeepMind chưa làm.
Họ mở cửa cho bất kỳ ai cũng có thể chơi với OpenAI Five, trong bốn ngày. ‖
Người chơi khắp thế giới đăng ký.
Có hai chế độ: đấu với đội máy, hoặc chơi cùng đội với các cỗ máy. ‖
Theo Wikipedia, trong bốn ngày ấy, đội máy chơi bốn mươi hai nghìn bảy trăm hai mươi chín ván công khai.
Và thắng chín mươi chín phẩy bốn phần trăm. ‖
Theo con số OpenAI công bố, được báo chí dẫn lại, ở các ván đối đầu, đội máy thắng bảy nghìn hai trăm mười lăm ván, chỉ thua bốn mươi hai.
Phần còn lại là các ván hợp tác, khi người và máy chơi cùng một đội. ‖
Bốn mươi hai ván thua.
Không nhiều, nhưng cũng không phải con số không.
Nó nhắc rằng ngay cả cỗ máy đã luyện hàng nghìn năm vẫn có chỗ để con người tìm ra. ‖
Theo OpenAI, qua báo chí, tới lúc ấy đội máy đã trải qua khoảng bốn mươi lăm nghìn năm chơi Dota, trong khoảng mười tháng huấn luyện.

## CH21 · Chơi cùng một đội với máy

Trong bốn ngày mở cửa ấy, có một chi tiết ít được nhắc tới.
Phần lớn các ván không phải là người đấu với máy. ‖
Theo con số được báo chí dẫn lại, có hơn ba mươi lăm nghìn ván hợp tác.
Ở đó, người chơi và các cỗ máy chơi chung một đội, cùng chống lại một đội khác. ‖
Điều ấy đặt ra một câu hỏi mới, khác hẳn mọi trận đấu trước.
Không còn là ai giỏi hơn ai.
Mà là, người và máy có làm việc được cùng nhau không. ‖
Một cỗ máy đã quen phối hợp với bốn bản sao của chính nó, giờ phải đoán ý một con người mà nó chưa từng gặp.
Một con người phải tin vào quyết định của một đồng đội không biết nói. ‖
Nếu bạn đã xem video về Deep Blue của kênh, bạn sẽ nhớ chuyện cờ nhân mã, khi người và máy ngồi chung một phe.
Gần hai mươi năm sau, câu chuyện ấy lặp lại, lần này trong một trò chơi điện tử năm người.

## CH22 · Hai trăm năm và bốn mươi lăm nghìn năm

Hãy đặt hai con số cạnh nhau.
Hai trăm năm chơi StarCraft cho mỗi phiên bản AlphaStar năm hai nghìn không trăm mười tám.
Bốn mươi lăm nghìn năm chơi Dota cho OpenAI Five. ‖
Một tuyển thủ chuyên nghiệp có thể chơi chục nghìn ván trong cả sự nghiệp.
Một cỗ máy chơi số ván ấy trong vài giờ. ‖
Đó vừa là sức mạnh, vừa là giới hạn của cách làm này.
Sức mạnh, vì không có con người nào luyện tập được nhiều như thế.
Giới hạn, vì con người học được rất nhiều chỉ từ vài ván. ‖
MaNa thua năm ván, rồi thắng ván biểu diễn, trước một phiên bản bị giới hạn tầm nhìn và mới luyện bảy ngày.
Bốn mươi hai ván thua của OpenAI Five cũng đến từ những người chơi kiên nhẫn tìm chỗ yếu. ‖
Cỗ máy cần hàng trăm năm để học điều con người học trong một buổi chiều.
Nhưng một khi đã học, nó không mệt, không quên, và không mất bình tĩnh.

## CH23 · Năm điều, đã đánh dấu

Hãy quay lại danh sách năm điều cờ vua không có.
Sương mù: đã vượt qua. Không có lượt: đã vượt qua. Ván dài: đã vượt qua. ‖
Lựa chọn khổng lồ ở mỗi khoảnh khắc: đã vượt qua.
Đồng đội: năm cỗ máy đã học cách chơi như một đội. ‖
Năm điều, đều đã được đánh dấu.
Nhưng mỗi dấu tích đều đi kèm một dòng chú thích.
Một bản đồ, một chủng tộc, một kho tướng thu nhỏ, một tầm nhìn khác người. ‖
Từ năm hai nghìn không trăm mười chín, cả DeepMind lẫn OpenAI đều chuyển sự chú ý khỏi trò chơi điện tử.
Không phải vì đã hết việc để làm.
Mà vì những gì học được từ đó đã sẵn sàng cho những bài toán lớn hơn. ‖
Lập kế hoạch dài hạn khi thiếu thông tin. Phối hợp nhiều tác tử cùng lúc. Học từ con người trước, rồi tự học vượt lên.
Những ý tưởng ấy giờ nằm trong robot, trong các hệ thống điều phối, và trong những trợ lý trí tuệ nhân tạo mà bạn dùng mỗi ngày. ‖
Còn câu hỏi về sự công bằng giữa người và máy, có lẽ sẽ không bao giờ có một câu trả lời trọn vẹn.
Cỗ máy không có đôi tay, không có đôi mắt, không có một buổi chiều mệt mỏi.
Mỗi lần ta đặt nó ngồi trước một trò chơi của con người, ta lại phải quyết định: luật nào là công bằng. ‖
Nếu được chọn một giới hạn cho cỗ máy khi đấu với người, bạn sẽ chọn giới hạn nào?
Kể cho mình nghe ở phần bình luận nhé.

---

## Ghi chú

**AlphaStar (DeepMind):**
- Blog 24/01/2019 "AlphaStar: Mastering the real-time strategy game StarCraft II": trận ghi hình 19/12/2018; TLO 5–0; MaNa 5–0 (sau thêm một tuần huấn luyện);
  Protoss đấu Protoss, bản đồ CatalystLE, phiên bản 4.6.2; ván biểu diễn: MaNa thắng một phiên bản dùng giao diện camera, huấn luyện 7 ngày; khởi đầu
  bằng học có giám sát từ ván ẩn danh do Blizzard cung cấp, thắng AI "Elite" 95% (≈ hạng vàng); AlphaStar League 14 ngày, 16 TPU mỗi agent, mỗi agent
  "up to 200 years of real-time StarCraft play"; APM trung bình ≈ 280 (277) so với MaNa 390, TLO 678 (TLO bị đẩy cao do bấm phím liên tục; bùng nổ APM
  hiệu dụng của AlphaStar có lúc cao hơn cả hai — làm rõ 29/01/2019); giao diện thô, không phải di chuyển camera, chỉ thấy đơn vị trong tầm nhìn; ≈ 10^26
  hành động hợp lệ mỗi bước; ván tới một giờ, hàng chục nghìn nước.
- Blog 30/10/2019 + Nature 575 (2019): Grandmaster cả ba chủng tộc; trên 99,8% người chơi đang xếp hạng trên Battle.net; chơi ẩn danh, cùng bản đồ và điều
  kiện; nhìn qua camera; tối đa 22 hành động agent mỗi 5 giây; giới hạn làm cùng TLO; chính sách bắt chước ban đầu tốt hơn 84% người chơi.
**OpenAI Five:**
- Wikipedia *OpenAI Five* (đọc 15/10/2026): 08/2017 thắng Dendi 1v1 tại TI 2017, học tự chơi ~2 tuần; TI 2018 thua paiN Gaming và đội cựu tuyển thủ Trung
  Quốc (không nêu tỉ số); 04/2019 thắng OG (vô địch TI 2018) loạt ba ván, San Francisco; Arena 4 ngày 42.729 ván công khai, thắng 99,4%; 2018: ~180 năm
  mỗi ngày, 256 GPU P100, 128.000 lõi CPU; LSTM 4.096 đơn vị; ~80.000 nhịp mỗi ván, 170.000 hành động khả dĩ mỗi tướng, ~1.000 hành động hợp lệ mỗi nhịp;
  Motherboard: "basically cheating" vì kho tướng đơn giản hoá.
- TechCrunch 15/04/2019: 2–0 trước OG; Engadget 23/04/2019 (số liệu OpenAI): đối đầu 7.215 thắng – 42 thua, 35.466 ván hợp tác; báo chí dẫn OpenAI: ~45.000
  năm tự chơi trong ~10 tháng → lời đọc "theo OpenAI, qua báo chí". Trang openai.com không đọc trực tiếp được (403).
**DQN:** Mnih và cộng sự, "Human-level control through deep reinforcement learning", *Nature* 518 (02/2015); blog DeepMind/Google 25/02/2015:
49 trò Atari 2600; đầu vào: điểm ảnh, tập nút bấm, điểm số; hơn phương pháp trước ở 43/49 trò; hơn 75% điểm người thử nghiệm chuyên nghiệp ở hơn nửa số trò.
**Độ trễ AlphaStar:** blog 24/01/2019: "a delay between observation and action of 350ms on average".
**Kênh tự diễn đạt:** "chục nghìn ván trong cả sự nghiệp" là ước lượng thô để so sánh quy mô (không gán số) · CH18 "những ý tưởng ấy giờ nằm trong…" là
diễn giải chung của kênh, không gán cho sản phẩm cụ thể.
**Không nói:** tên thật đời thường của tuyển thủ; tỉ số từng ván ở TI 2018; chiến thuật cụ thể mà các đội người dùng để thắng (chưa đối chiếu nguồn).
