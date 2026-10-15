# "HAI CHIẾC CARD TRONG PHÒNG NGỦ": kịch bản lời đọc (bản 1, chờ kiểm chứng)

**Tựa chính (đề xuất):** GPU: Con Chip Chơi Game Đã Trở Thành Trái Tim Của AI Như Thế Nào?

**Kênh:** Mind in the Machine (MIM) · **Giọng:** Hải Đăng (lời trích: Ngọc Huyền, lọc radio)
**Độ dài dự kiến:** khoảng 13 phút, 9 chương (≈2.900 âm tiết)
**Hồ sơ dữ kiện + nguồn:** [docs/channels/mind-in-the-machine/2026-10-09-long-06-research.md](../../../docs/channels/mind-in-the-machine/2026-10-09-long-06-research.md)

Quy ước đọc file:
- Mỗi dòng là một câu đọc. `‖` cuối dòng = ngừng dài.
- `»` = lời trích, đọc bằng giọng trích; nguyên văn tiếng Anh hiện trên màn hình.
- **[TRÍCH DỊCH]** = câu có thật, dịch sang tiếng Việt. **[DIỄN Ý]** = trích diễn đạt lại, gắn nhãn trên hình.
- Tên nước ngoài giữ nguyên chữ trên phụ đề; cách đọc nằm trong `say` của spec.json.

**Cấu trúc giữ chân người xem** (theo [RETENTION.md](../../../motion/long/RETENTION.md)):
- **Cold open:** Toronto, 2012. Một sinh viên cao học huấn luyện mạng nơ-ron trên hai card đồ hoạ chơi game, đặt trong phòng ngủ ở nhà bố mẹ. Năm, sáu ngày sau, cỗ máy ấy thắng cuộc thi nhận dạng ảnh lớn nhất thế giới với khoảng cách chưa từng có.
- **Lộ trình, hình thức "Câu hỏi duy nhất"** (khác MIM #1 "ba câu hỏi", #2 "ba chặng đường", #3 "lời thách", #4 "cảnh hẹn trước", #5 "nghịch lý"): *"Vì sao một món đồ sinh ra để vẽ súng ống, xe đua trong game lại trở thành thứ quý nhất của cả ngành trí tuệ nhân tạo?"* Không liệt kê chương. Trả lời ở CH05 (giữa video): cả việc vẽ một khung hình lẫn việc dạy một mạng nơ-ron đều là hàng triệu phép tính nhỏ giống hệt nhau, làm cùng một lúc.
- **Vòng mở:** câu hỏi duy nhất (ch0 → ch5) · vì sao Nvidia làm chip cho game (ch0 → ch1) · máy vẽ thế nào (ch1 → ch2) · có ai dùng card game làm việc khác chưa (ch2 → ch3) · mạng nơ-ron cần gì (ch3 → ch4) · chuyện gì sau căn phòng ngủ (ch5 → ch6) · Việt Nam ở đâu (ch6 → ch7) · chip có phải là tất cả (ch7 → ch8).
- **Mô-típ:** (a) **căn phòng ngủ / hai chiếc card** (ch0, ch5, ch6, câu kết ch8). (b) **điểm ảnh** (ch2 hai triệu điểm ảnh, ch2 bức Mona Lisa bằng bi sơn, ch4 "mỗi điểm ảnh là một phép tính, mỗi kết nối nơ-ron cũng vậy", ch8). (c) **đầu bếp và phụ bếp** (ch2 gieo, ch4 nhắc, ch5 trả).
- **Cảnh mạnh thứ hai (~65–70%):** bàn giao siêu máy tính DGX-1 tận tay cho một phòng thí nghiệm nhỏ ở San Francisco năm 2016, nơi sau này làm ra ChatGPT; đặt cạnh con số 512 lõi (GTX 580) → 16.384 lõi (RTX 4090).
- **Trung thực:** không nói giá cổ phiếu, giá trị vốn hoá, không khen chê sản phẩm; "GPU đầu tiên" là **cách Nvidia tự gọi** GeForce 256; số lõi GPU và lõi CPU **không so ngang được** (lõi GPU nhỏ, đơn giản hơn nhiều) — lời đọc nói rõ; con số "nhanh hơn bao nhiêu lần" luôn kèm "trong bài toán ấy, so với máy ấy"; GPU **không phải** con đường duy nhất (các hãng có chip riêng cho AI) — nói ở ch8; phần Việt Nam chỉ nêu điều đã ký và đã công bố.

---

## CH00 · Hai chiếc card trong phòng ngủ

Toronto, năm 2012.
Trong một phòng ngủ ở nhà bố mẹ, một chiếc máy tính chạy liên tục suốt nhiều ngày.
Bên trong có hai card đồ hoạ, loại người ta mua để chơi game, mỗi chiếc khoảng năm trăm đô lúc ra mắt. ‖
Chủ căn phòng là Alex Krizhevsky, một nghiên cứu sinh của Đại học Toronto.
Anh không chơi game.
Anh đang dạy một cỗ máy nhìn ảnh. ‖
Đề bài đến từ một cuộc thi: cho máy xem hơn một triệu bức ảnh, rồi bắt nó gọi tên thứ có trong ảnh, giữa một nghìn loại khác nhau.
Mèo, nấm, xe cứu hoả, một con ve bé xíu.
Mỗi bức ảnh, máy được đoán năm lần. Không trúng lần nào, tính là sai. ‖
Năm, sáu ngày huấn luyện trên hai chiếc card ấy.
Rồi kết quả được công bố.
Đội đứng thứ hai sai hai mươi sáu phần trăm.
Cỗ máy của Alex chỉ sai mười lăm phần trăm. ‖
Trong một cuộc thi mà các đội thường hơn nhau vài điểm, đây là một cú nhảy.
Các đội khác dùng những phương pháp mà con người phải tự tay chỉ cho máy nhìn vào đâu: cạnh, góc, mảng màu.
Cỗ máy của Alex tự học lấy, từ ảnh.
Nhiều người coi năm ấy là lúc trí tuệ nhân tạo hiện đại bắt đầu.
Và câu hỏi của video này nằm ngay trong căn phòng ngủ ấy. ‖
Vì sao một món đồ sinh ra để vẽ súng ống, xe đua trong game lại trở thành thứ quý nhất của cả ngành trí tuệ nhân tạo?
Để trả lời, phải quay lại hai mươi năm trước đó, ở một quán ăn ven đường.

## CH01 · Một quán ăn ven đường

Cuối năm 1992, ở phía đông thành phố San Jose, bang California.
Ba kỹ sư ngồi trong một quán Denny's, loại quán ăn mở cửa thâu đêm, cà phê được rót thêm miễn phí.
Jensen Huang, Chris Malachowsky và Curtis Priem.
Họ phác thảo ý tưởng cho một công ty mới. ‖
Tháng 4 năm 1993, công ty ấy ra đời, tên là Nvidia.
Thứ họ muốn làm: chip vẽ đồ hoạ ba chiều cho máy tính cá nhân.
Thời ấy, game ba chiều đang lên, và vẽ một thế giới ba chiều trên màn hình là việc cực nặng. ‖
Năm 1999, Nvidia ra mắt GeForce 256.
Hãng gọi nó là bộ xử lý đồ hoạ đầu tiên trên thế giới, viết tắt là GPU.
Thật ra, cái tên ấy do chính Nvidia đặt và định nghĩa, như một lời quảng cáo.
Nhưng cái tên ở lại, và giờ cả ngành đều dùng. ‖
Nhiệm vụ của GPU rất rõ: vẽ hình cho game, thật nhanh, thật mượt.
Không ai trong quán ăn năm ấy nói gì về trí tuệ nhân tạo.
Muốn hiểu vì sao con chip vẽ hình về sau lại hợp với trí tuệ nhân tạo, phải xem một khung hình được vẽ ra như thế nào.

## CH02 · Hai triệu điểm ảnh

Màn hình bạn đang xem có lẽ là loại Full HD.
Ngang một nghìn chín trăm hai mươi điểm, dọc một nghìn không trăm tám mươi điểm.
Tức là khoảng hai triệu điểm ảnh. ‖
Mỗi điểm ảnh cần được tính màu: ánh sáng chiếu vào đâu, bóng đổ chỗ nào, mặt đường ướt phản chiếu ra sao.
Game chạy sáu mươi khung hình mỗi giây.
Nghĩa là hơn một trăm hai mươi triệu điểm ảnh phải được tính, trong mỗi giây. ‖
Điều quan trọng là: phép tính cho điểm ảnh này gần như giống hệt phép tính cho điểm ảnh bên cạnh.
Chỉ khác con số đầu vào.
Và điểm này không cần chờ điểm kia tính xong. ‖
Hãy hình dung một nhà bếp.
Bộ xử lý trung tâm của máy tính, CPU, giống vài đầu bếp rất giỏi.
Mỗi người nấu được món khó, xử lý được món lạ, nhưng mỗi lúc chỉ làm vài việc.
GPU thì giống hàng nghìn phụ bếp.
Mỗi người chỉ biết một việc đơn giản, như thái hành.
Nhưng nếu cần thái một núi hành, hàng nghìn phụ bếp làm cùng lúc sẽ xong trước. ‖
Điều này không có nghĩa GPU giỏi hơn CPU.
Bảo hàng nghìn phụ bếp nấu một món cần nếm đi nếm lại, quyết định từng bước, họ sẽ đứng nhìn nhau.
Máy tính của bạn cần cả hai: đầu bếp lo những việc rẽ nhánh, phức tạp, còn phụ bếp lo những việc lặp lại khổng lồ.
Vẽ game là việc lặp lại khổng lồ, nên nó thuộc về phụ bếp. ‖
Năm 2008, ở một sự kiện của chính Nvidia, hai người dẫn chương trình MythBusters đã dựng cảnh này bằng súng bắn bi sơn.
Cỗ máy thứ nhất bắn từng viên một, chậm rãi vẽ một hình đơn giản.
Cỗ máy thứ hai có một nghìn một trăm nòng, bắn cùng một lúc.
Chưa tới một phần mười giây, bức Mona Lisa hiện ra trên tấm toan. ‖
Từng viên bi là một điểm ảnh.
Và chẳng bao lâu, có người tự hỏi: nếu thay điểm ảnh bằng những con số khác thì sao?

## CH03 · Giả làm bức tranh

Những năm đầu thập niên 2000, card đồ hoạ đã mạnh hơn nhiều so với nhu cầu của phần lớn công việc văn phòng.
Một số nhà khoa học nhìn sức mạnh ấy và thấy tiếc.
Họ muốn dùng nó để tính thứ khác: dòng chảy của chất lỏng, sóng địa chấn, phân tử thuốc. ‖
Khó ở chỗ, con chip chỉ hiểu một ngôn ngữ: hình vẽ.
Thế là họ phải giả dạng phép tính của mình thành một bức tranh.
Con số được nhét vào màu của điểm ảnh, bài toán được viết như một hiệu ứng ánh sáng.
Chip tưởng mình đang vẽ, thật ra đang làm toán. ‖
Cách ấy chạy được, nhưng rất khổ.
Muốn dùng, nhà khoa học phải hiểu cả vật lý của mình lẫn mẹo vặt của dân làm game.
Ở Đại học Stanford, một nghiên cứu sinh tên là Ian Buck quyết định làm cho việc ấy dễ hơn.
Anh mê card đồ hoạ từ hồi chơi game thời sinh viên.
Anh viết một ngôn ngữ lập trình tên là Brook, để người ta viết phép tính như phép tính, còn phần giả làm bức tranh thì máy tự lo. ‖
Năm 2004, Ian Buck về làm cho Nvidia, dẫn một nhóm nhỏ.
Ngày 8 tháng 11 năm 2006, Nvidia ra mắt một dòng card mới, cùng một công cụ tên là CUDA.
Với CUDA, lập trình viên có thể ra lệnh cho GPU tính toán trực tiếp, không cần giả làm bức tranh nữa. ‖
Lúc ấy, đây là một canh bạc.
Theo lời chính Jensen Huang kể lại sau này, mỗi con chip phải gánh thêm chi phí cho phần tính toán, trong khi phần lớn người mua chỉ cần chơi game.
Phần chi phí ấy ăn gần hết lợi nhuận của hãng trong nhiều năm.
Trong nhiều năm, khách hàng của CUDA chủ yếu là các phòng thí nghiệm khoa học.
Rồi một nhóm người khác tìm đến. Họ cần một núi phép nhân.

## CH04 · Một núi phép nhân

Mạng nơ-ron nghe như bộ não, nhưng bên trong nó gần với một bảng tính khổng lồ hơn.
Mỗi kết nối là một con số, gọi là trọng số.
Ảnh đi vào, được nhân với hàng triệu trọng số, cộng lại, rồi chuyển sang lớp tiếp theo. ‖
Dạy một mạng nơ-ron nghĩa là làm việc ấy hàng triệu lần.
Mỗi lần đoán sai, chỉnh từng trọng số một chút, rồi đoán lại.
Ví dụ, máy nhìn một con mèo và đoán là con cáo.
Nó lần ngược lại xem trọng số nào đã đẩy nó về phía cáo, rồi vặn mỗi trọng số đi một chút.
Một bức ảnh chưa đủ. Phải làm vậy với hơn một triệu bức ảnh, cả bộ ảnh được lặp lại khoảng chín mươi lượt.
Mạng của Alex có sáu mươi triệu trọng số.
Mỗi bức ảnh đi qua mạng là hàng trăm triệu phép nhân. ‖
Nghe có quen không? Hàng triệu phép tính nhỏ, giống hệt nhau, không cần chờ nhau.
Đúng là một núi hành, chờ hàng nghìn phụ bếp.
Năm 2009, ở Đại học Stanford, nhóm của Andrew Ng thử dạy mạng nơ-ron trên card đồ hoạ.
Trong bài toán họ chọn, máy chạy nhanh hơn tới năm mươi lăm lần so với một bộ xử lý hai lõi thời ấy.
Một mạng lớn trước đây mất vài tuần để dạy, nay chỉ còn khoảng một ngày. ‖
Nhưng tốc độ thôi chưa đủ.
Một cỗ máy học nhìn ảnh cần thứ thứ hai: rất nhiều ảnh, có người gọi tên sẵn.
Và thứ ấy vừa mới xong, ở chính Stanford.

## CH05 · Lời giải

Năm 2006, giáo sư Lý Phi Phi, Fei-Fei Li, bắt đầu một dự án mà nhiều đồng nghiệp cho là quá sức.
Gom ảnh từ Internet cho mọi danh từ trong tiếng Anh, rồi nhờ người gọi tên từng ảnh.
Năm 2009, bộ dữ liệu ấy hoàn thành, mang tên ImageNet.
Cuộc thi ở đầu video được dựng trên chính bộ ảnh này. ‖
Thế là năm 2012, ba thứ gặp nhau trong một căn phòng ngủ ở Toronto.
Dữ liệu từ ImageNet.
Một thuật toán mà thầy của Alex, giáo sư Geoffrey Hinton, đã theo đuổi mấy chục năm.
Và hai chiếc card chơi game, chạy bằng CUDA. ‖
Có một chi tiết trong bài báo của nhóm mà mình rất thích.
Mỗi chiếc card chỉ có ba gigabyte bộ nhớ, không chứa nổi cả mạng nơ-ron.
Thế là Alex cắt đôi mạng của mình.
Một nửa nằm trên card thứ nhất, nửa kia nằm trên card thứ hai, và hai nửa chỉ trao đổi với nhau ở vài tầng nhất định.
Cỗ máy thắng cuộc thi, theo đúng nghĩa đen, có hai bán cầu. ‖
Suốt hơn một năm, Alex chỉnh từng thông số rồi dạy lại, chỉnh rồi dạy lại, cho tới khi cỗ máy vượt mọi đối thủ. ‖
Đến đây, câu hỏi của video đã có lời giải.
Con chip sinh ra để vẽ game hợp với trí tuệ nhân tạo, không phải vì nó thông minh.
Mà vì vẽ một khung hình và dạy một mạng nơ-ron, hoá ra, là cùng một kiểu việc.
Hàng triệu phép tính nhỏ, giống hệt nhau, làm cùng một lúc.
Điểm ảnh và trọng số, với con chip, chỉ là những con số. ‖
Mạng nơ-ron của Alex về sau được gọi theo tên anh: AlexNet.
Năm 2024, giáo sư Hinton nhận giải Nobel Vật lý.
Năm 2025, khi Bảo tàng Lịch sử Máy tính ở Mỹ công bố mã nguồn của AlexNet, ông tóm tắt dự án bằng một câu.
» Ilya nghĩ chúng tôi nên làm, Alex làm cho nó chạy được, còn tôi thì nhận giải Nobel. [TRÍCH DỊCH] ‖
Ilya ở đây là Ilya Sutskever, nghiên cứu sinh thứ hai trong nhóm.
Và chỉ vài tháng sau cuộc thi, ba người ấy trở thành món hàng đắt giá nhất của ngành công nghệ.

## CH06 · Từ phòng ngủ đến siêu máy tính

Tháng 12 năm 2012, ở một khách sạn sòng bạc bên hồ Tahoe, nước Mỹ, có một cuộc đấu giá kín.
Theo lời kể của nhà báo Cade Metz, món hàng là một công ty vừa lập vội, chưa có sản phẩm nào, chỉ có ba người: Hinton, Alex và Ilya.
Bốn công ty trả giá từ xa, qua thư điện tử, mỗi lần tăng ít nhất một triệu đô.
Khi giá lên tới bốn mươi tư triệu đô, Hinton dừng cuộc đấu giá, và chọn về với Google.
Ông muốn chọn nơi hợp với nghiên cứu của mình, hơn là con số cao nhất. ‖
Từ lúc ấy, các phòng thí nghiệm trí tuệ nhân tạo đua nhau mua card đồ hoạ.
Tháng 8 năm 2016, Jensen Huang tự tay mang một chiếc máy tới văn phòng của một phòng thí nghiệm nhỏ ở San Francisco.
Phòng thí nghiệm ấy mới thành lập được vài tháng, tên là OpenAI. Ilya Sutskever là một trong những người sáng lập.
Chiếc máy tên là DGX-1, được Nvidia gọi là siêu máy tính đầu tiên dành riêng cho trí tuệ nhân tạo.
Bên trong có tám GPU, xếp sát nhau. ‖
Sáu năm sau, chính phòng thí nghiệm ấy ra mắt ChatGPT.
Từ hai chiếc card trong phòng ngủ, đến tám GPU trong một chiếc hộp, rồi đến những toà nhà chứa hàng nghìn GPU.
Đó là con đường của trí tuệ nhân tạo trong một thập kỷ. ‖
Chính card đồ hoạ chơi game cũng lớn lên.
Chiếc GTX 580 mà Alex dùng có năm trăm mười hai lõi tính toán.
Chiếc RTX 4090 ra mắt năm 2022 có mười sáu nghìn ba trăm tám mươi tư lõi.
Gấp ba mươi hai lần, chỉ trong mười hai năm. ‖
Một lưu ý nhỏ: lõi của GPU không so ngang được với lõi của CPU.
Mỗi lõi GPU nhỏ và đơn giản hơn nhiều. Vẫn là chuyện phụ bếp và đầu bếp.
Điều thay đổi là số phụ bếp, và nhà bếp ngày càng giống một nhà máy. ‖
Và nhà máy ấy, từ năm 2023, bắt đầu nhìn về một nơi rất gần chúng ta.

## CH07 · Ngôi nhà thứ hai

Tháng 12 năm 2023, Jensen Huang lần đầu sang Việt Nam.
Ở Hà Nội, ông gặp Thủ tướng, thăm Trung tâm Đổi mới sáng tạo quốc gia, và nói chuyện với các công ty công nghệ trong nước.
Báo chí ghi lại câu ông nói: muốn biến Việt Nam thành ngôi nhà thứ hai của Nvidia. ‖
Một năm sau, ngày 5 tháng 12 năm 2024, Chính phủ Việt Nam và Nvidia ký thoả thuận.
Hai bên hợp tác lập một trung tâm nghiên cứu và phát triển trí tuệ nhân tạo, và một trung tâm dữ liệu trí tuệ nhân tạo ở Việt Nam.
Cùng dịp ấy, Nvidia mua lại VinBrain, một công ty khởi nghiệp Việt Nam làm trí tuệ nhân tạo cho y tế. ‖
Theo báo chí đưa tin, trung tâm dữ liệu trong thoả thuận sẽ mở rộng từ một trung tâm dữ liệu của Viettel vốn đã dùng công nghệ Nvidia.
Thoả thuận là bước đầu.
Những trung tâm ấy làm được gì, cần thêm thời gian mới biết.
Nhưng có một điều đáng để ý.
Câu chuyện bắt đầu từ hai chiếc card trong phòng ngủ, giờ đã là chuyện của các chính phủ. ‖
Vậy có phải cứ có thật nhiều chip là có trí tuệ nhân tạo?

## CH08 · Không chỉ là con chip

Nhìn lại căn phòng ngủ năm 2012, con chip chỉ là một trong ba thứ.
Không có ImageNet, hai chiếc card chẳng có gì để học.
Không có thuật toán Hinton theo đuổi mấy chục năm, chúng chỉ tính nhanh hơn một cách vô ích. ‖
GPU cũng không phải con đường duy nhất.
Nhiều hãng công nghệ lớn đã thiết kế chip riêng cho trí tuệ nhân tạo, chỉ làm đúng việc nhân ma trận.
Con chip chơi game thắng trước, vì nó có mặt đúng lúc, với một công cụ đã được mài giũa nhiều năm. ‖
Và càng nhiều chip, càng tốn điện.
Những trung tâm dữ liệu chứa hàng nghìn GPU cần nguồn điện và nước làm mát rất lớn, một câu hỏi mà nhiều nước, kể cả Việt Nam, sẽ phải tính tới.
Con chip giải được bài toán tốc độ, nhưng mở ra những bài toán khác. ‖
Còn với chúng ta, có một bài học nhỏ.
Những bước ngoặt lớn đôi khi đến từ một món đồ được dùng sai mục đích.
Một card đồ hoạ được dùng để làm toán.
Một công cụ cho phòng thí nghiệm được dùng để dạy máy nhìn. ‖
Lần tới khi bạn thấy một tấm card đồ hoạ trong cửa hàng, hãy nhớ: thứ bạn đang nhìn là hàng nghìn phụ bếp, đang chờ một núi hành.
Có thể là hai triệu điểm ảnh của một trận game.
Có thể là sáu mươi triệu trọng số của một cỗ máy đang học nhìn. ‖
Còn bạn, bạn có đang dùng món đồ nào sai mục đích, theo một cách hay ho không? Kể cho mình nghe ở phần bình luận nhé.

## Ghi chú

**Cần kiểm chứng kỹ (người viết chưa chắc):**
1. CH03 "giả dạng phép tính thành bức tranh" (GPGPU trước CUDA: dữ liệu trong texture, kernel viết như pixel shader) — cần nguồn khảo cứu (Owens et al., "A Survey of General-Purpose Computation on Graphics Hardware", 2007). Ví dụ ứng dụng (chất lỏng, địa chấn, phân tử) cần đối chiếu.
2. CH03 "canh bạc" + "chip phải gánh thêm phần dành cho tính toán" — chỉ giữ nếu có nguồn Nvidia/ phỏng vấn Jensen Huang; nếu không, đổi giọng điệu thành nhận định của kênh.
3. CH04 "hàng trăm triệu phép nhân mỗi bức ảnh" — AlexNet ≈ 0,7–1,1 tỉ phép nhân-cộng/ảnh (forward) theo nhiều nguồn; "hàng trăm triệu" là đánh giá thấp an toàn — kiểm lại.
4. CH05 "mọi danh từ trong tiếng Anh" — theo CHM/IEEE ("every noun in the English language", dùng taxonomy WordNet); ILSVRC dùng 1.000 lớp, 1,2 triệu ảnh huấn luyện.
5. CH05 năm Bảo tàng Lịch sử Máy tính công bố mã nguồn AlexNet: 20–21/03/2025 (IEEE Spectrum, Hansen Hsu, 21/03/2025).
6. CH06 "OpenAI mới thành lập được vài tháng" (thành lập 12/2015 → 08/2016 ≈ 8 tháng); Sutskever đồng sáng lập — kiểm lại; "tám GPU" trong DGX-1 (Tesla P100 ×8).
7. CH06 "ChatGPT ra mắt sáu năm sau" (30/11/2022).
8. CH07 lời Jensen Huang "ngôi nhà thứ hai" — báo VN dẫn lại; cần nguồn gốc (Reuters 10/12/2023 hoặc phát biểu 05/12/2024).
9. CH08 "nhiều hãng đã thiết kế chip riêng cho AI" — giữ chung chung (không nêu tên sản phẩm) hoặc kiểm nguồn (Google TPU công bố 05/2016).

**Không dùng:** giá cổ phiếu Nvidia, vốn hoá, tài sản Jensen Huang; video MythBusters (bản quyền) — chỉ kể lại, hình minh hoạ tự dựng.

**Gợi ý đọc tên (`say`):** Krizhevsky → Cri-giép-xki · Sutskever → Xút-xke-vơ · Hinton → Hin-tơn · Nvidia → En-vi-đi-a · GeForce → Di-pho · CUDA → Cu-đa · Jensen Huang → Gien-xần Hoang · Malachowsky → Ma-la-cốp-xki · Priem → Prim · Denny's → Đen-nis · Toronto → Tô-rôn-tô · San Jose → Xan Hô-dê · MythBusters → Mít-bớt-tơ · Mona Lisa → Mô-na Li-da · ImageNet → Im-mịt-nét · AlexNet → A-léch-nét · Andrew Ng → An-đru Ng · Stanford → Xten-phơ · OpenAI → Âu-pần Ây-ai · DGX → Đi-gi-ích · ChatGPT → Chát-gi-pi-ti · GTX → Gi-ti-ích · RTX → A-ti-ích · VinBrain → Vin-brên · Full HD → Phun ếch-đi.
