# Research M3 · Máy học đọc chữ viết tay như thế nào? (gốc 1989)

Bước R, 28/10/2026. Chưa phải kịch bản. Quy ước: SƠ CẤP / [SECONDARY]; ĐÚNG / SAI / CHƯA KIỂM ĐƯỢC. "(chỉ snippet)" = chỉ thấy trong kết quả tìm kiếm, chưa mở được trang.
Không mở được lần này: acm.org/media-center (403), awards.acm.org (403), engineering.fb.com, cifar.ca, smithsonianmag.com, cedar.buffalo.edu, cs.princeton.edu (lỗi DNS), image-net.org (từ chối kết nối), ieeexplore (trang rỗng), cbsnews (403).

## 0. Chốt điều kiện duyệt: năm 1989 đóng góp ĐÚNG điều gì

| Hạng mục | Nội dung chốt | Nguồn |
|---|---|---|
| Đóng góp của bài 1989 | Đưa **ràng buộc của bài toán vào kiến trúc mạng** (kết nối cục bộ, chia sẻ trọng số) rồi **huấn luyện toàn bộ bằng lan truyền ngược**, áp vào chữ số mã bưu chính viết tay của Bưu điện Mỹ. **Một mạng duy nhất học trọn quy trình** từ ảnh chữ số đã chuẩn hoá tới kết quả phân loại, không cần bộ trích đặc trưng làm tay. | Abstract: "constraints can be integrated into a backpropagation network through the architecture of the network"; "A single network learns the entire recognition operation" — https://mlanthology.org/neco/1989/lecun1989neco-backpropagation |
| Điểm khác với nhóm cùng phòng 1988–89 | Denker và cộng sự (cũng Bell Labs) đã có mạng 2D đọc mã bưu chính, nhưng hệ số bộ lọc phải **thiết kế tay**; bài LeCun 1989 **học hệ số tích chập trực tiếp từ ảnh** bằng lan truyền ngược | https://en.wikipedia.org/wiki/Convolutional_neural_network [SECONDARY]; https://en.wikipedia.org/wiki/LeNet [SECONDARY] |
| KHÔNG phải phát minh của 1989 | (1) ý tưởng mạng phân tầng kiểu thị giác, bất biến vị trí: Fukushima 1980; (2) lan truyền ngược: Linnainmaa 1970, Werbos, Rumelhart–Hinton–Williams 1986; (3) chia sẻ trọng số + gradient: TDNN của Waibel 1987 (cho âm vị), mạng bất biến dịch của Wei Zhang 1988 (cho ký tự) | xem bảng 1 |
| Câu an toàn để đọc | "Năm 1989, một nhóm bảy người ở Bell Labs cho thấy có thể dạy một mạng nơ-ron đọc chữ số mã bưu chính viết tay từ đầu tới cuối, bằng lan truyền ngược. Họ đứng trên vai các ý tưởng có từ trước." | tổng hợp từ các dòng trên |

## 1. Bảng dữ kiện

| # | Khẳng định | Giá trị chính xác | URL đã mở | Loại | Kết luận |
|---|---|---|---|---|---|
| 1 | Bài 1989 | "Backpropagation Applied to Handwritten Zip Code Recognition", Neural Computation **1(4): 541–551**, DOI 10.1162/neco.1989.1.4.541 | https://mlanthology.org/neco/1989/lecun1989neco-backpropagation | SƠ CẤP (trang thư mục dẫn bài gốc) | ĐÚNG |
| 2 | 7 tác giả | Y. LeCun, B. Boser, J. S. Denker, D. Henderson, R. E. Howard, W. Hubbard, L. D. Jackel | như trên (đã kiểm 28/10 trong brief-facts) | SƠ CẤP | ĐÚNG |
| 3 | Dữ liệu | chữ số mã bưu chính viết tay "provided by the U.S. Postal Service" | như trên | SƠ CẤP | ĐÚNG |
| 4 | Sai số bản thử 1989 | ~1% lỗi trên tập thử mã bưu chính, tỉ lệ từ chối ~9% | https://en.wikipedia.org/wiki/LeNet | [SECONDARY] | CHƯA KIỂM ĐƯỢC ở bài gốc, chỉ nói "theo các tổng kết sau này" hoặc bỏ |
| 5 | LeCun vào Bell Labs | 1988, phòng Adaptive Systems Research do Lawrence D. Jackel đứng đầu; trước đó postdoc ở Toronto 1987–88 (nhóm Hinton) | https://amturing.acm.org/award_winners/lecun_6017366.cfm | SƠ CẤP (ACM, tác giả Thomas Haigh) | ĐÚNG |
| 6 | Neocognitron | Fukushima, "Neocognitron: A self-organizing neural network model for a mechanism of pattern recognition unaffected by shift in position", Biological Cybernetics **36: 193–202**, xuất bản **tháng 4/1980**; học **không giám sát** ("learning without a teacher"), nhận mẫu "without affected by their positions" | https://link.springer.com/article/10.1007/BF00344251 | SƠ CẤP | ĐÚNG |
| 7 | Lan truyền ngược phổ biến 1986 | Rumelhart, Hinton, Williams, "Learning representations by back-propagating errors", Nature **323: 533–536**, **09/10/1986** | https://www.nature.com/articles/323533a0 | SƠ CẤP | ĐÚNG |
| 8 | Lan truyền ngược có trước 1986 | Linnainmaa 1970 (chế độ ngược của vi phân tự động); Werbos áp vào mạng nhiều lớp 1982; Rumelhart tự phát triển ~1982, bài 1986 "góp phần phổ biến" | https://en.wikipedia.org/wiki/Backpropagation | [SECONDARY] | ĐÚNG (mức thứ cấp) — nói "đã có người tìm ra trước đó" là đủ, không cần đọc tên Linnainmaa |
| 9 | Chia sẻ trọng số trước 1989 | TDNN, Waibel và cộng sự **1987** (nhận dạng âm vị), "first CNN utilizing weight sharing in combination with a training by gradient descent"; Wei Zhang và cộng sự **1988**, mạng bất biến dịch cho ký tự | https://en.wikipedia.org/wiki/Convolutional_neural_network | [SECONDARY] | ĐÚNG (mức thứ cấp) |
| 10 | Bài 1998 (LeNet-5) | LeCun, Bottou, Bengio, Haffner, "Gradient-Based Learning Applied to Document Recognition", Proc. IEEE **86(11): 2278–2324** | https://mlanthology.org/misc/1998/lecun1998misc-gradientbased | SƠ CẤP | ĐÚNG |
| 11 | Câu về séc (nguyên văn) | "It is deployed commercially and reads several million cheques per day." — nằm trong **Abstract**, tức trang đầu bài, **tr. 2278** | như trên (mlanthology trích nguyên câu abstract) | SƠ CẤP | ĐÚNG. Số trang suy ra từ vị trí abstract; PDF gốc tải được nhưng font mã hoá, không trích được chữ để kiểm thân bài |
| 12 | Thân bài 1998 ghi "millions of checks per month" | — | (brief-facts 28/10, không mở lại được thân bài) | — | CHƯA KIỂM ĐƯỢC lần này; **đừng đọc** |
| 13 | "Hơn 10% séc ở Mỹ" | ACM viết: "LeCun suggests that at one point it was reading more than 10% of all the checks written in the US." Wikipedia LeNet: NCR triển khai từ **6/1996**, ước ~20 triệu séc/ngày, ~10% séc Mỹ vào **2001** | https://amturing.acm.org/award_winners/lecun_6017366.cfm ; https://en.wikipedia.org/wiki/LeNet | SƠ CẤP (ACM, nhưng là lời LeCun tự kể) / [SECONDARY] | ĐÚNG có điều kiện: chỉ được nói "**theo lời LeCun kể với ACM**, có lúc hơn 10%". An toàn nhất vẫn là "hàng triệu tấm séc mỗi ngày" (dòng 11) |
| 14 | Hệ thống đọc séc | làm "in the early 1990s in collaboration with Bengio, Leon Bottou and Patrick Haffner"; cấp phép cho nhà cung cấp hệ thống ngân hàng như **NCR**; xử lý ở trung tâm tập trung vì cần máy mạnh | https://amturing.acm.org/award_winners/lecun_6017366.cfm | SƠ CẤP | ĐÚNG |
| 15 | MNIST | 60.000 ảnh huấn luyện + 10.000 ảnh thử, ảnh 28×28; trộn từ NIST SD-3 (nhân viên Cục Điều tra dân số) và SD-7 (học sinh trung học); làm ra khoảng **1994** | https://en.wikipedia.org/wiki/MNIST_database ; https://en.wikipedia.org/wiki/LeNet | [SECONDARY] | ĐÚNG. **MNIST KHÔNG phải dữ liệu của bài 1989** (1989 dùng dữ liệu USPS) |
| 16 | AlexNet 2012 | Krizhevsky, Sutskever, Hinton, NIPS 2012; top-5 **15,3%** so với **26,2%** của đội thứ hai ở ILSVRC-2012; 60 triệu tham số, 650.000 nơ-ron | https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf | SƠ CẤP | ĐÚNG |
| 17 | Lý do 1: dữ liệu | "Until recently, datasets of labeled images were relatively small -- on the order of tens of thousands of images"; ImageNet "over 15 million labeled high-resolution images in over 22,000 categories" | như trên (mục 1–2) | SƠ CẤP | ĐÚNG |
| 18 | Lý do 2: sức tính | CNN "have still been prohibitively expensive to apply in large scale to high-resolution images"; huấn luyện "between five and six days to train on two GTX 580 3GB GPUs" | như trên (mục 1) | SƠ CẤP | ĐÚNG |
| 19 | Tác giả AlexNet tự nói | "our results can be improved simply by waiting for faster GPUs and bigger datasets" | như trên | SƠ CẤP | ĐÚNG |
| 20 | GPU cho CNN trước 2012 | Chellapilla 2006 (CNN đầu tiên trên GPU); Cireșan và cộng sự 2011 tăng tốc ~60 lần so với CPU | https://en.wikipedia.org/wiki/Convolutional_neural_network | [SECONDARY] | ĐÚNG (mức thứ cấp); dùng để tránh nói "AlexNet là người đầu tiên dùng GPU" |
| 21 | Turing Award | Giải **2018**, công bố **27/3/2019**, Bengio, Hinton, LeCun; trích dẫn: "For conceptual and engineering breakthroughs that have made deep neural networks a critical component of computing." | https://amturing.acm.org/award_winners/lecun_6017366.cfm (citation) ; https://ai.meta.com/blog/-turing-award-presented-to-yann-lecun-geoffrey-hinton-and-yoshua-bengio/ (đăng 27/3/2019) | SƠ CẤP (ACM, trang người nhận giải) + [SECONDARY] (Meta) | ĐÚNG. Thông cáo báo chí ACM vẫn 403 |
| 22 | Tiền thưởng 1 triệu USD, Google tài trợ | 1.000.000 USD | (chỉ snippet kết quả tìm kiếm) | — | CHƯA KIỂM ĐƯỢC → không đọc số tiền |
| 23 | LeCun hiện nay | NYU; Facebook/Meta 2013–2025; "Advanced Machine Intelligence Labs, 2025-present" | https://amturing.acm.org/award_winners/lecun_6017366.cfm | SƠ CẤP | ĐÚNG — chức danh hiện tại dễ đổi, chỉ hiện chữ trên màn hình nếu cần |
| 24 | CNN trong điện thoại hôm nay | ACM: kỹ thuật này dùng trên Android cho nhận dạng giọng nói của Google Assistant (chép lời thời gian thực) và dịch qua camera của app dịch | https://amturing.acm.org/award_winners/lecun_6017366.cfm | SƠ CẤP (ACM, viết ~2019) | ĐÚNG, nói "theo ACM" |
| 25 | Viết tay trên bàn phím điện thoại | Gboard nhận chữ viết tay **hơn 100 ngôn ngữ**; mô hình là mạng hồi quy (QRNN xen lớp tích chập và hồi quy), **không phải** CNN thuần | https://research.google/blog/rnn-based-handwriting-recognition-in-gboard/ (07/3/2019) | SƠ CẤP | ĐÚNG — cẩn thận: đừng nói "Gboard chạy LeNet" |
| 26 | Bưu điện Mỹ hôm nay: thư không đọc được chuyển ảnh về trung tâm mã hoá từ xa ở Salt Lake City | ~1,2 tỷ ảnh/năm; 55 trung tâm năm 1997 | (chỉ snippet: smithsonianmag, cbsnews, nalc.org) | — | CHƯA KIỂM ĐƯỢC |

## 2. Dòng thời gian

| Năm | Mốc | Nguồn (dòng) |
|---|---|---|
| 1970 | Linnainmaa: chế độ ngược của vi phân tự động | 8 [SECONDARY] |
| 4/1980 | Fukushima công bố Neocognitron (học không giám sát) | 6 |
| 9/10/1986 | Rumelhart–Hinton–Williams, Nature | 7 |
| 1987 | Waibel: TDNN, chia sẻ trọng số + gradient | 9 [SECONDARY] |
| 1987–88 | LeCun postdoc ở Toronto với Hinton | 5 |
| 1988 | LeCun vào Bell Labs; Wei Zhang: mạng bất biến dịch cho ký tự; Denker: mạng đọc mã bưu chính, bộ lọc thiết kế tay | 5, 9, bảng 0 |
| 1989 | Bài Neural Computation 1(4), dữ liệu USPS | 1–3 |
| đầu 1990s → 6/1996 | Hệ thống đọc séc làm đầu 1990s; NCR triển khai 6/1996 | 14 / 13 [SECONDARY] |
| ~1994 | MNIST ra đời | 15 [SECONDARY] |
| 11/1998 | Bài Proc. IEEE: LeNet-5, "several million cheques per day" | 10–11 |
| 2006–2011 | CNN chạy trên GPU (Chellapilla; Cireșan) | 20 [SECONDARY] |
| 2012 | AlexNet: 15,3% vs 26,2% | 16–19 |
| 27/3/2019 | Công bố Turing Award 2018 | 21 |

## 3. Nhịp câu chuyện (6–8 nhịp)

| Nhịp | Bước lập luận | Dữ kiện dùng |
|---|---|---|
| 1. Hôm nay | Điện thoại đọc chữ viết tay, dịch qua camera, chép lời — tất cả là "máy nhìn" | 24, 25 |
| 2. Bài toán | Một chữ số "7" mỗi người viết một kiểu; máy chỉ thấy lưới điểm ảnh | hình MNIST (mục 5), 15 |
| 3. Những người đi trước | Fukushima 1980: máy nhận mẫu bất kể vị trí, nhưng tự học không thầy; 1986: lan truyền ngược được phổ biến | 6, 7, 8 |
| 4. 1989 ở Bell Labs | Ghép hai thứ: cấu trúc kiểu "bộ lọc trượt" + học bằng lan truyền ngược, trên mã bưu chính thật của USPS; một mạng làm trọn từ ảnh tới đáp án | bảng 0, 1–3, 5 |
| 5. Ra đời thật | Đọc séc ngân hàng: "several million cheques per day" (1998) | 10, 11, 14 |
| 6. Nghịch lý: thắng mà vẫn bị lép | Chạy được cho chữ số nhỏ, nhưng ảnh lớn thì quá tốn; dữ liệu có nhãn chỉ cỡ vài chục nghìn ảnh | 17, 18 |
| 7. 2012 | ImageNet 15 triệu ảnh + 2 GPU GTX 580, 5–6 ngày huấn luyện → 15,3% so với 26,2% | 16–19, 20 |
| 8. Kết | Turing Award 2019 cho ba người; ý tưởng 1989 nằm trong điện thoại bạn | 21, 24 |

**Nghịch lý / bước ngoặt có nguồn:** cùng một ý tưởng đã "đọc hàng triệu tấm séc mỗi ngày" vào 1998 (dòng 11), nhưng 14 năm sau tác giả AlexNet vẫn viết CNN "prohibitively expensive" với ảnh độ phân giải cao (dòng 18). Thứ thay đổi không phải ý tưởng chính, mà là dữ liệu và GPU (dòng 17–19).

## 4. Rủi ro và giới hạn

| Loại | Chi tiết | Cách nói |
|---|---|---|
| Người còn sống | LeCun, Bengio, Hinton, Fukushima, các đồng tác giả 1989 (đa số) | Không suy diễn động cơ; không dùng chữ "cha đẻ" như sự thật — nếu dùng thì "báo chí hay gọi là…" |
| "Một người phát minh" | Rủi ro chính của bài | Luôn nói "nhóm bảy người ở Bell Labs"; nêu Fukushima 1980 và 1986 trước khi tới 1989 |
| 10% séc | Chỉ là lời LeCun tự kể (ACM) + Wikipedia | "theo lời LeCun kể với ACM", hoặc bỏ; ưu tiên "hàng triệu tấm mỗi ngày" |
| Số trang câu séc | 2278 suy từ vị trí abstract | Chỉ hiện "Proc. IEEE, 1998" trên màn hình, không cần đọc số trang |
| MNIST | Dễ nhầm là dữ liệu 1989 | MNIST ~1994; 1989 là dữ liệu USPS |
| AlexNet "đầu tiên dùng GPU" | SAI | Đã có CNN trên GPU từ 2006, 2011 (dòng 20) |
| Điện thoại | Bàn phím viết tay Gboard dùng mạng hồi quy, không phải LeNet | Nói "con cháu của ý tưởng này", "theo ACM" cho ví dụ Android |
| Tiền thưởng Turing | Chưa mở được nguồn | Không đọc "1 triệu đô" |
| Câu phải nói "theo…" | 10% séc; ví dụ Android (ACM); sai số ~1% bản 1989 (Wikipedia) | — |

## 5. Ứng viên hình ảnh (chỉ PD / CC0 / CC BY — giấy phép đọc qua Commons API ngày 28/10/2026)

| File | Giấy phép | Dùng cho | Kết luận |
|---|---|---|---|
| https://commons.wikimedia.org/wiki/File:Mnist.png | **CC0** (Matheus Espala, 2025) | lưới chữ số viết tay | NHẬN |
| https://commons.wikimedia.org/wiki/File:NIST_SD-19_f1002_33.png | **Public domain** (NIST, 1995) | mẫu viết tay gốc của NIST | NHẬN |
| https://commons.wikimedia.org/wiki/File:MNIST_(52063061876).jpg | **CC BY 2.0** (Flickr, 2021) | ảnh minh hoạ MNIST; ghi công tác giả | NHẬN (kiểm nội dung ảnh trước khi dùng) |
| https://commons.wikimedia.org/wiki/File:Yann_Lecun_during_a_talk_at_EPFL.jpg | **CC BY 4.0** (Alain Herzog, 5/10/2018) | ảnh LeCun | NHẬN, ghi "Alain Herzog / EPFL, CC BY 4.0" |
| https://commons.wikimedia.org/wiki/File:Yann_Lecun_during_a_conference_at_EPFL,_Lausanne,_5_october_2018.jpg | **CC BY 4.0** (Alain Herzog) | ảnh LeCun, dự phòng | NHẬN |
| File:MnistExamples.png, File:MnistExamplesModified.png, File:MNIST_dataset_example.png | CC BY-SA 4.0 | — | LOẠI |
| File:Yann_LeCun_-_2018_(cropped).jpg, (29146901108), (41208595340), 2025 (cropped) | CC BY-SA 2.0 | — | LOẠI |
| File:Yann_LeCun_at_the_University_of_Minnesota.jpg | CC BY-SA 3.0 | — | LOẠI |
| Fukushima, Hinton, Bengio, nhóm Bell Labs 1989 | chưa tìm ảnh hợp lệ | — | **cần ảnh AI theo luật người thật** (dáng gốc, nghiêng hoặc quay lưng, không nhãn AI) hoặc chỉ dùng chữ |
| Sơ đồ mạng tích chập, lưới điểm ảnh "7" | tự dựng bằng HTML/motion | — | khuyến nghị |

Giấy phép bộ dữ liệu MNIST (trang yann.lecun.com/exdb/mnist chỉ còn danh mục file, không thấy điều khoản): CHƯA KIỂM ĐƯỢC → không lấy ảnh trực tiếp từ bộ dữ liệu; dùng Mnist.png (CC0) hoặc tự viết tay.

## 6. Câu hỏi còn mở cho người viết kịch bản

1. Có nêu tên Denker (mạng 1988 bộ lọc thiết kế tay) không? Nó làm rõ đúng điểm mới của 1989, nhưng thêm một cái tên.
2. Có dùng "10% séc" kèm "theo lời LeCun" không, hay chỉ "hàng triệu tấm mỗi ngày"? Khuyến nghị: dùng câu 1998.
3. Ví dụ "điện thoại hôm nay": chọn dịch qua camera (ACM) hay bàn phím viết tay (Google, nhưng là mạng hồi quy)? Cần một câu nối trung thực.
4. Có cần ví dụ Việt Nam (quét CCCD, đọc hoá đơn)? Chưa có nguồn — phải tìm thêm nếu dùng.
5. Thông cáo ACM 27/3/2019 vẫn 403; nếu muốn chiếu ảnh chụp thông cáo thì cần người mở bằng trình duyệt.

## 7. Short S / L (ý tưởng, chưa dựng)

| Loại | Ý | Dữ kiện |
|---|---|---|
| S | "Máy nhìn chữ số 7 thế nào?" — lưới 28×28, bộ lọc trượt tìm nét ngang, nét chéo; trả lời trọn trong 30 giây | 15, bảng 0 (hình Mnist.png CC0) |
| S | "Năm 1998, một mạng nơ-ron đọc hàng triệu tấm séc mỗi ngày" — ý tưởng AI đã đi làm thật từ thế kỷ trước | 10, 11, 14 |
| L | "Ý tưởng 1989 phải đợi hơn 20 năm": nêu đúng hai lý do có nguồn (dữ liệu vài chục nghìn ảnh; ảnh lớn quá tốn sức tính), để lại câu hỏi "năm 2012 chuyện gì xảy ra?" → Long trả lời bằng AlexNet | 17, 18, 16 |
