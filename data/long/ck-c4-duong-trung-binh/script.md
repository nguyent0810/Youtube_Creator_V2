# ĐƯỜNG TRUNG BÌNH ĐỘNG (MA) LÀ GÌ? MỘT ĐƯỜNG KẺ TÓM TẮT QUÁ KHỨ, VÀ ĐIỀU NÓ KHÔNG BIẾT (bản 1, chờ kiểm chứng)

**Kênh:** Biểu Đồ Biết Nói (CK) · **Chuỗi:** Chứng khoán từ số 0 — Bài 4 (C4) · **Giọng:** Ngọc Huyền (dẫn) · Phạm Tuyên (dòng `HỎI:`) ·
Xuân Vĩnh (`»` lời trích, lọc radio)
**Độ dài dự kiến:** ~11 phút, 6 chương · **Mã tính:** [analysis.py](analysis.py) → `results.json` (VN-Index, vnstock/VCI, 08/10/2018 → 06/10/2026)
**Tiêu đề (phương án):** (1) *Đường trung bình động MA là gì? Một đường kẻ tóm tắt quá khứ, và điều nó không biết* · (2) *MA200 "thủng
là bán"? Kênh thử trên 7 năm VN-Index* · (3) *MA cho người mới: tính tay, đọc đúng, và vì sao nó luôn đến muộn*

Quy ước: mỗi dòng là một câu đọc · `‖` = ngừng dài · `HỎI:` = giọng người hỏi · `»` = lời trích · **lời đọc không có chữ số** ·
`**[DIỄN Ý]**` = lời truyền miệng diễn ý · `[TRÍCH DỊCH]` = câu thật dịch sang tiếng Việt.
**Luật cứng:** chỉ giáo dục — **không** "nên mua/bán/giữ", **không** tín hiệu, không dự báo; **không** nói VN-Index hiện đang trên hay dưới
MA nào (dễ thành tín hiệu). Phép thử quy tắc là **minh hoạ cơ chế trên chỉ số** (không mua trực tiếp được), một giai đoạn, chọn sẵn; ghi
"KÊNH TỰ TÍNH · QUÁ KHỨ · KHÔNG PHẢI TÍN HIỆU". Không nêu mã cổ phiếu, công ty chứng khoán, phần mềm, quỹ. Thẻ miễn trừ đầu video.

**Giữ chân:** cold open = **đỉnh 06/01/2022 và đường MA200 "đến sau" sáu mươi bảy phiên** · **lộ trình dạng "câu hỏi duy nhất"** (khác D2
"chặng đường", C3 "cảnh hẹn trước", B1 "nghịch lý", C2 "bản đồ bằng hình", D1 "lời thách"): *"Một đường kẻ chỉ là trung bình cộng của những
ngày đã qua. Vậy nó biết gì về ngày mai?"* — trả lời cuối CH02 (~40%) · **re-hook ~55%** = "cắt giả" (CH03) · **cảnh mạnh ~70%** = kênh
thử sáu độ dài MA, kết quả nhảy múa (CH04) · **mô-típ** "điểm trung bình học kỳ" (gieo CH01, nhắc CH02, CH05) · kết = MA dùng để làm gì +
khi nào sai + câu hỏi bình luận + gợi bài sau (EMA).

---

## CH00 · Đường kẻ đến sau

Ngày sáu tháng một năm hai nghìn không trăm hai mươi hai, VN-Index đóng cửa ở một nghìn năm trăm hai mươi tám điểm.
Đó là đỉnh cao nhất của cả chu kỳ ấy. ‖
Trên mạng, có một câu được nhắc đi nhắc lại.
**[DIỄN Ý]** » Giá thủng đường MA hai trăm là phải chạy.
Đường MA hai trăm là đường trung bình của hai trăm phiên gần nhất, và gần như phần mềm biểu đồ nào cũng vẽ được nó. ‖
Vậy lần ấy, giá thủng đường MA hai trăm vào lúc nào?
Ngày mười chín tháng tư.
Sáu mươi bảy phiên sau đỉnh, khi chỉ số đã thấp hơn đỉnh tám phần trăm. ‖
Đường kẻ không sai. Nó chỉ đến sau.
Và đó không phải lỗi của riêng lần ấy, mà là bản chất của nó. ‖
Một đường kẻ chỉ là trung bình cộng của những ngày đã qua.
Vậy nó biết gì về ngày mai?
Đó là câu hỏi của video này. ‖
Đây là Biểu Đồ Biết Nói. Tiền bạc, giải thích bằng dữ liệu.
Và đây là bài bốn của khoá Chứng khoán từ số không.
Video chỉ nhằm giáo dục, không phải lời khuyên mua hay bán, và không dự báo thị trường.

## CH01 · Điểm trung bình học kỳ

Hồi đi học, bạn có điểm từng bài kiểm tra, và có điểm trung bình học kỳ.
Một bài điểm kém không kéo điểm trung bình xuống nhiều.
Nhưng nếu điểm kém cứ lặp lại, điểm trung bình sẽ đi xuống dần. ‖
Đường trung bình động làm đúng như vậy với giá.
Chữ MA là viết tắt của moving average, nghĩa là trung bình trượt.
Hãy tính thử một đường MA năm phiên, bằng số thật. ‖
Năm phiên cuối cùng trước đỉnh, từ ngày ba mươi tháng mười hai năm hai nghìn không trăm hai mươi mốt.
Giá đóng cửa lần lượt khoảng một nghìn bốn trăm tám mươi sáu, một nghìn bốn trăm chín mươi tám, một nghìn năm trăm hai mươi sáu, một nghìn năm trăm hai mươi ba, và một nghìn năm trăm hai mươi chín điểm.
Cộng lại, chia năm.
Ra khoảng một nghìn năm trăm mười hai điểm.
Đó là một điểm trên đường MA năm, đặt ở ngày sáu tháng một. ‖
Sang phiên sau, bỏ phiên cũ nhất ra, thêm phiên mới nhất vào, rồi chia năm lần nữa.
Cửa sổ năm phiên trượt dần sang phải, mỗi ngày một bước.
Nối các điểm ấy lại, ta có đường trung bình động. ‖
HỎI: Vậy MA hai mươi, MA năm mươi, MA hai trăm khác nhau ở đâu?
Chỉ ở độ rộng của cửa sổ.
Hai mươi phiên là khoảng một tháng giao dịch. Hai trăm phiên là gần một năm.
HỎI: Mà sao lại là hai mươi, năm mươi, hai trăm, chứ không phải hai mươi ba hay một trăm tám mươi bảy?
Không có định luật nào cả. Đó là những con số tròn, dễ nhớ, được nhiều người dùng lâu thành quen.
Và vì nhiều người cùng nhìn một con số, nó được nhắc nhiều hơn những con số khác. ‖
Có hai cách đọc một đường trung bình mà bạn nên biết.
Cách thứ nhất là nhìn độ dốc của chính đường ấy: đang đi lên, đi ngang, hay đi xuống.
Cách thứ hai là nhìn giá đang nằm trên hay dưới đường ấy, và cách bao xa.
Cửa sổ càng rộng, đường càng mượt. Và như bạn sắp thấy, càng chậm.

## CH02 · Mượt nhưng chậm

Hãy đặt ba đường lên cùng một biểu đồ VN-Index năm hai nghìn không trăm hai mươi hai.
MA hai mươi bám sát giá, uốn theo từng nhịp lên xuống.
MA hai trăm thì gần như một đường cong thoai thoải, phẳng lặng. ‖
Ở đỉnh tháng một, giá cắt xuống MA hai mươi và MA năm mươi sau bảy phiên, khi chỉ số đã thấp hơn đỉnh năm phần trăm.
Với MA hai trăm, phải mất sáu mươi bảy phiên. ‖
Ở chiều ngược lại, sau đáy ngày mười lăm tháng mười một năm ấy, chuyện cũng vậy.
Giá vượt lên MA hai mươi sau chín phiên, khi chỉ số đã cao hơn đáy mười phần trăm.
Vượt lên MA năm mươi sau mười một phiên.
Còn MA hai trăm, phải tới tháng sáu năm sau, một trăm ba mươi ba phiên, khi chỉ số đã cao hơn đáy mười tám phần trăm. ‖
Còn độ dốc của chính đường MA hai trăm thì sao?
Sau đáy tháng mười một, đường ấy vẫn cắm đầu đi xuống thêm hơn bảy tháng.
Phải tới giữa tháng bảy năm hai nghìn không trăm hai mươi ba, một trăm sáu mươi lăm phiên sau đáy, nó mới bắt đầu ngóc lên.
Ai chờ đường MA hai trăm quay đầu mới yên tâm, sẽ thấy đáy từ rất xa phía sau. ‖
Không có gì bí ẩn ở đây.
Đường trung bình được tính từ những ngày đã qua, nên nó luôn đi sau giá.
Cửa sổ hai trăm phiên chứa gần một năm quá khứ. Một cú quay đầu mới vài tuần chưa đủ sức kéo nó đổi hướng. ‖
Giống điểm trung bình học kỳ: một học sinh tiến bộ vượt bậc từ tháng này, điểm trung bình vẫn còn mang theo những bài kém của mấy tháng trước.
Vậy câu trả lời cho câu hỏi đầu video là:
MA không biết gì về ngày mai.
Nó chỉ tóm tắt quá khứ cho gọn, để mắt người dễ nhìn ra hướng đi chung. ‖
HỎI: Nếu chậm như vậy, sao người ta vẫn dùng?
Vì cái giá của việc nhanh hơn, như bạn sắp thấy, là sai nhiều hơn.

## CH03 · Cắt giả

Muốn nhanh hơn, người ta dùng cửa sổ ngắn hơn.
Nhưng cửa sổ ngắn thì nhạy với từng nhịp nhiễu của thị trường. ‖
Kênh đã đếm trên VN-Index, từ tháng bảy năm hai nghìn không trăm mười chín tới nay.
Mỗi lần giá đóng cửa chuyển từ trên MA hai trăm xuống dưới, hoặc ngược lại, tính là một lần đổi phía.
Trong hơn bảy năm, giá đổi phía bốn mươi lăm lần.
Hai mươi lăm lần trong số đó, giá quay lại phía cũ chỉ trong mười phiên. ‖
Người chơi gọi những lần như vậy là cắt giả.
Hãy nhìn một ví dụ, ngay trước một biến cố lớn.
Ngày hai mươi lăm tháng mười một năm hai nghìn không trăm mười chín, giá thủng MA hai trăm.
Ngày hai mươi tháng một năm sau, giá vượt lên lại. Ai bán ở lần trước, giờ thấy mình bán hớ.
Chỉ chín phiên sau, ngày ba mươi mốt tháng một, giá lại thủng. Lần này, dịch bệnh ập tới, và chỉ số rơi tới đáy tháng ba. ‖
Cùng một kiểu tín hiệu, có lần là báo động giả, có lần là thật.
Đường kẻ không cho bạn biết trước lần nào là lần nào. ‖
Bạn bán vì giá thủng đường, vài ngày sau giá lại vượt lên, bạn mua lại ở giá cao hơn.
Mỗi lần như thế, ngoài phần chênh lệch giá, còn mất phí giao dịch, và thuế khi bán. ‖
Còn khi tín hiệu là thật, như sau đỉnh năm hai nghìn không trăm hai mươi hai, giá nằm dưới MA hai trăm suốt hai trăm bảy mươi chín phiên liền, hơn một năm.
Tức là đường kẻ không vô dụng: nó cho thấy cả một năm chỉ số đi xuống.
Vấn đề là nó chỉ cho thấy khi đã đi được một đoạn, và nó không phân biệt được trước đâu là thật, đâu là giả. ‖
Cắt giả hay xảy ra nhất khi thị trường đi ngang, giá lắc lư quanh đường trung bình.
Lúc ấy, đường kẻ giống một sợi dây căng giữa phòng, còn giá cứ bước qua bước lại.
Và đó cũng là lúc nhiều người tin vào đường kẻ nhất, vì họ đang chờ một tín hiệu rõ ràng.

## CH04 · Bắn tên rồi vẽ hồng tâm

Có một phép thử mà kênh muốn bạn tự nhìn.
Giả sử một quy tắc rất đơn giản: phiên hôm trước giá đóng cửa trên đường MA thì giữ chỉ số, dưới thì đứng ngoài.
Đây là phép thử minh hoạ trên chỉ số, không thể mua trực tiếp, và là quá khứ. ‖
Từ tháng mười năm hai nghìn không trăm mười chín tới nay, nếu cứ giữ suốt, chỉ số tăng khoảng bảy mươi tám phần trăm.
Với MA hai trăm, quy tắc ấy lãi khoảng một trăm phần trăm, trước phí và thuế.
Nghe hấp dẫn. ‖
Nhưng thay hai trăm bằng một trăm, quy tắc chỉ còn lãi khoảng năm mươi lăm phần trăm, thua xa việc giữ suốt.
Tính thêm phí giao dịch giả định và thuế bán, MA một trăm còn khoảng ba mươi ba phần trăm.
MA hai mươi trước phí trông rất đẹp, khoảng một trăm ba mươi hai phần trăm. Nhưng nó đổi phía quá nhiều lần, trừ phí và thuế, chỉ còn khoảng bảy mươi phần trăm. ‖
Trong sáu độ dài kênh thử, sau phí và thuế, chỉ có MA hai trăm nhỉnh hơn giữ suốt một chút.
Và mình chỉ biết điều đó sau khi đã nhìn hết dữ liệu.
Chọn con số đẹp nhất sau khi biết kết quả, giống như bắn tên trước, rồi vẽ hồng tâm quanh mũi tên. ‖
Giới nghiên cứu gọi chuyện này là đào dữ liệu.
Năm một nghìn chín trăm chín mươi hai, ba nhà nghiên cứu Brock, Lakonishok và LeBaron thử các quy tắc đường trung bình trên chỉ số Dow Jones của Mỹ, gần chín mươi năm dữ liệu, và thấy kết quả khá tốt, chưa tính phí.
Bảy năm sau, Sullivan, Timmermann và White thử lại với gần tám nghìn quy tắc, và tính tới việc chọn quy tắc tốt nhất sau khi đã biết kết quả.
Trên mười năm dữ liệu mới, sau khi nghiên cứu đầu tiên đã công bố, họ kết luận hầu như không còn bằng chứng các quy tắc ấy mang lại giá trị kinh tế.

## CH05 · Vậy MA dùng để làm gì

MA không phải quả cầu pha lê. Nhưng nó cũng không vô dụng.
Nó là một cách tóm tắt, giống điểm trung bình học kỳ. ‖
Thứ nhất, nó lọc bớt nhiễu.
Nhìn biểu đồ ngày, mắt dễ bị cuốn theo từng phiên tăng giảm. Một đường trung bình giúp bạn thấy hướng đi chung của vài tháng.
Thứ hai, nó cho bạn một mốc để tự hỏi.
Giá đang cách đường trung bình xa hay gần, đi lên hay đi xuống đã bao lâu? ‖
Còn khi nào nó dễ sai?
Khi thị trường đi ngang, vì cắt giả.
Khi có cú sốc đột ngột, như phiên ba tháng tư năm hai nghìn không trăm hai mươi lăm, chỉ số mất gần bảy phần trăm trong một ngày.
Đường trung bình chỉ phản ứng sau khi cú sốc đã xảy ra.
Và khi bạn chọn độ dài sau khi đã nhìn kết quả. ‖
Trước khi tin một đường kẻ, bạn có thể tự hỏi ba câu.
Một: đường này tính bằng bao nhiêu phiên, và vì sao lại là con số ấy?
Hai: nếu làm theo, mỗi năm mình phải đổi phía bao nhiêu lần, mất bao nhiêu phí?
Ba: người khoe quy tắc này đã thử bao nhiêu quy tắc khác trước khi chọn nó? ‖
Còn bạn, bạn hay thấy đường trung bình nào được nhắc nhiều nhất? Kể cho mình nghe ở phần bình luận nhé.
Bài sau, mình sẽ nói về một người anh em của MA, đường EMA, thứ được quảng cáo là nhanh hơn. Và xem nó có thật sự thoát được cái bóng của quá khứ không.

## Ghi chú

**Số liệu kênh tự tính** (`analysis.py` → `results.json`): MA5 30/12/2021–06/01/2022 = 1.485,97 · 1.498,28 · 1.525,58 · 1.522,50 ·
1.528,57 → 1.512,18 (lời đọc làm tròn số nguyên) · đỉnh 06/01/2022: cắt xuống MA20 & MA50 ngày 17/01/2022 (7 phiên, −5,0%), MA200 ngày
19/04/2022 (67 phiên, −8,0%) · đáy 15/11/2022: lên MA20 28/11 (9 phiên, +10,3%), MA50 30/11 (11 phiên, +15,0%), MA200 01/06/2023
(133 phiên, +18,3%) · quy tắc MA200 30/07/2019 → 06/10/2026: 45 lần đổi phía, 25 lần đổi lại ≤ 10 phiên · độ nhạy (09/10/2019 → 06/10/2026,
giữ suốt +78,0%; phí giả định 0,15%/chiều + thuế bán 0,1%): MA20 +131,9 / +70,3 · MA50 +80,3 / +45,8 · MA100 +54,9 / +32,5 · MA150 +81,5 / +60,3
· MA200 +99,8 / +82,2 · MA250 +81,1 / +69,2.
**Thêm (bản 1b):** chuỗi dưới MA200 dài nhất 19/04/2022 → 31/05/2023 = 279 phiên · độ dốc MA200 chuyển xuống 19/04/2022, chuyển lên
17/07/2023 (165 phiên sau đáy 15/11/2022) · ví dụ cắt giả: 25/11/2019 thủng (976,35 < 980,89), 20/01/2020 vượt (978,63 > 977,07),
31/01/2020 thủng (936,62 < 976,67), 9 phiên sau lần vượt.
**Lưu ý giai đoạn:** CH03 dùng mốc 07/2019 (khi MA200 đầu tiên có), CH04 dùng mốc 10/2019 (khi MA250 có) để mọi độ dài cùng giai đoạn — lời đọc
nói đúng mốc của từng chương.

**Cần kiểm chứng:**
1. Brock, Lakonishok & LeBaron (1992), *Journal of Finance* 47(5): 1731–1764 — Dow Jones 1897–1986, quy tắc MA + phá vùng giá, "strong support",
   chưa tính phí (kiểm câu "chưa tính phí" trong bài gốc).
2. Sullivan, Timmermann & White (1999), *Journal of Finance* 54(5): 1647–1691 — vũ trụ **7.846** quy tắc; ngoài mẫu 01/1987–12/1996:
   "scant evidence that technical trading rules were of any economic value" (đã đọc bản DP 303, LSE FMG 10/1998).
3. Phiên 03/04/2025: −87,99 điểm (−6,68%) — hồ sơ research 2026-10-06 [C*]; kiểm lại với dữ liệu kênh.
4. Phí giao dịch 0,15%/chiều là **giả định minh hoạ** (mức phí thực tế khác nhau theo công ty) — lời đọc nói "phí giao dịch giả định".
5. Thuế bán 0,1% (Luật Thuế TNCN mới hiệu lực 01/07/2026 giữ mức này — SECONDARY).
