# LÃI KÉP: NỘP ÍT HƠN MỘT NỬA MÀ CUỐI CÙNG CÓ NHIỀU HƠN? PHÉP TÍNH 3 TRIỆU MỖI THÁNG (bản 1)

**Kênh:** Biểu Đồ Biết Nói (CK) · **Chuỗi:** Tiền của bạn — Bài B2 · **Giọng:** Ngọc Huyền (dẫn) · Phạm Tuyên (dòng `HỎI:`)
**Độ dài dự kiến:** ~9 phút, 7 chương · **Mã tính:** [analysis.py](analysis.py) → `results.json`
**Tiêu đề (phương án):** (1) *Lãi kép: nộp ít hơn một nửa mà cuối cùng có nhiều hơn? Phép tính 3 triệu mỗi tháng* · (2) *3 triệu mỗi tháng trong 30 năm
thành bao nhiêu? Lãi kép, và thứ lặng lẽ ăn mòn nó* · (3) *Lãi kép là gì? Năm thứ 13, tiền lãi bắt đầu vượt tiền bạn nộp*

Quy ước: mỗi dòng là một câu đọc · `‖` = ngừng dài · `HỎI:` = giọng người hỏi · **lời đọc không có chữ số**.
**Luật cứng:** chỉ giáo dục — không "nên gửi/mua/bán", không dự báo, không nêu tên ngân hàng, sản phẩm. Mọi phép tính với sáu phần trăm là **VÍ DỤ
GIẢ ĐỊNH** (lãi suất không đổi, không rút) — ghi trên màn hình; không phải mức lãi của sản phẩm nào. Hai nhân vật là giả định. Số thật chỉ có hai: sổ
mười hai tháng ở nhóm ngân hàng lớn cuộn tám năm (kênh tự tính) và lạm phát bình quân tám năm (Cục Thống kê, qua báo chí).

**Viết cho tai (chuẩn 12/10/2026):** câu một hơi, nói với "bạn", hỏi–đáp, số làm tròn.
**Giữ chân:** cold open = **Lan nộp mười năm rồi dừng, Minh nộp hai mươi năm: ai có nhiều hơn?** · **lộ trình dạng "con số mang về"** (khác các bài
trước: ba nhân vật, câu hỏi duy nhất, chặng đường, cảnh hẹn trước, nghịch lý, bản đồ bằng hình, lời thách): hứa một con số duy nhất — năm thứ mấy
thì tiền lãi một năm vượt tiền nộp một năm · **re-hook ~45%** = lời giải Lan và Minh · **cảnh mạnh ~65%** = ba tỷ chỉ còn mua được như một tỷ hai ·
**mô-típ** "quả cầu tuyết" (CH01, CH03, CH05 lăn ngược).

---

## CH00 · Hai người bạn, một câu đố

Mình có một câu đố về hai người bạn giả định, Lan và Minh.
Cả hai đều để dành ba triệu đồng mỗi tháng, với cùng một mức lãi. ‖
Lan bắt đầu năm hai mươi lăm tuổi.
Cô để dành đúng mười năm, rồi dừng hẳn. Không nộp thêm đồng nào nữa. Tiền cứ để yên đấy. ‖
Minh thì bắt đầu muộn hơn, năm ba mươi lăm tuổi.
Nhưng anh rất kiên trì. Tháng nào cũng nộp, suốt hai mươi năm, không nghỉ. ‖
Tới năm cả hai năm mươi lăm tuổi.
Lan đã nộp tổng cộng ba trăm sáu mươi triệu.
Minh đã nộp bảy trăm hai mươi triệu. Gấp đôi. ‖
HỎI: Vậy ai có nhiều tiền hơn?
Câu trả lời có thể làm bạn bất ngờ. Và nó nằm trong hai chữ, lãi kép. ‖
Trong video này, mình sẽ đưa bạn một con số để mang về.
Đó là năm thứ mấy, thì tiền lãi một năm bắt đầu lớn hơn chính số tiền bạn nộp vào trong năm.
Và sau đó, mình sẽ kể về một thứ lặng lẽ ăn mòn lãi kép, mà các bảng tính đẹp đẽ thường bỏ quên. ‖
Đây là Biểu Đồ Biết Nói. Tiền bạc, giải thích bằng dữ liệu.
Video chỉ nhằm giáo dục. Mức lãi trong các ví dụ là giả định, không phải lời khuyên, và không phải dự báo.

## CH01 · Lãi đẻ ra lãi

Lãi kép là gì?
Nói gọn, là lãi đẻ ra lãi. ‖
Thử với một trăm triệu, và mức lãi giả định sáu phần trăm một năm.
Hết năm đầu, bạn có một trăm lẻ sáu triệu.
Sang năm thứ hai, sáu phần trăm không tính trên một trăm triệu nữa.
Nó tính trên một trăm lẻ sáu triệu. ‖
Nên tiền lãi năm hai không phải sáu triệu, mà là sáu triệu ba trăm sáu mươi nghìn.
Ba trăm sáu mươi nghìn ấy, là lãi của tiền lãi.
Nghe chẳng đáng là bao. ‖
Nhưng hãy cho nó thời gian.
Nếu năm nào bạn cũng rút tiền lãi ra tiêu, sau ba mươi năm, bạn có hai trăm tám mươi triệu.
Còn nếu để lãi nhập vào gốc, con số là khoảng năm trăm bảy mươi tư triệu.
Hơn gấp đôi. Cùng một trăm triệu, cùng một mức lãi. ‖
Người ta hay ví lãi kép như quả cầu tuyết.
Lúc đầu nó bé xíu. Nhưng càng lăn, mỗi vòng nó dính thêm nhiều tuyết hơn vòng trước.
Vậy với ba triệu mỗi tháng, quả cầu ấy lăn thế nào?

## CH02 · Năm thứ mười ba

Vẫn với mức lãi giả định sáu phần trăm một năm. Mỗi tháng, bạn nộp ba triệu.
Sau mười năm, bạn đã nộp ba trăm sáu mươi triệu, và có khoảng bốn trăm chín mươi triệu.
Tiền lãi mới chiếm hơn một phần tư. Chưa có gì ghê gớm. ‖
Sau hai mươi năm, bạn nộp bảy trăm hai mươi triệu, và có gần một tỷ bốn.
Tiền lãi lúc này đã gần bằng tiền bạn nộp. ‖
Sau ba mươi năm, bạn nộp một tỷ không trăm tám mươi triệu.
Và có khoảng ba tỷ.
Gần hai phần ba số ấy là tiền lãi, không phải tiền bạn bỏ ra. ‖
Và đây là con số mình hứa.
Năm thứ mười ba.
Từ năm ấy, tiền lãi sinh ra trong một năm bắt đầu lớn hơn ba mươi sáu triệu bạn nộp vào trong năm.
Nói cách khác, từ năm thứ mười ba, tiền của bạn làm việc chăm hơn cả bạn. ‖
HỎI: Mười ba năm cơ à? Lâu thế.
Đúng vậy. Và đó là điều ít ai nói về lãi kép.
Mười năm đầu, nó gần như vô hình. Phần lớn người ta bỏ cuộc trước khi thấy nó. ‖
Có một mẹo tính nhẩm nổi tiếng, gọi là quy tắc bảy mươi hai.
Lấy bảy mươi hai chia cho lãi suất, ra số năm để tiền gấp đôi.
Sáu phần trăm, thì khoảng mười hai năm.

## CH03 · Lời giải cho Lan và Minh

Giờ thì quay lại câu đố.
Lan nộp mười năm rồi dừng. Minh nộp hai mươi năm, số tiền gấp đôi. ‖
Năm năm mươi lăm tuổi, Minh có khoảng một tỷ ba trăm tám mươi sáu triệu.
Còn Lan?
Khoảng một tỷ sáu trăm hai mươi bảy triệu. ‖
Người nộp ít hơn một nửa, lại có nhiều hơn hai trăm bốn mươi triệu.
HỎI: Sao lại thế được?
Vì khi Lan dừng nộp ở tuổi ba mươi lăm, cô đã có sẵn gần năm trăm triệu.
Và số tiền ấy có thêm hai mươi năm để lăn.
Hai mươi năm ở mức sáu phần trăm, là hơn ba lần gấp. ‖
Còn Minh, những đồng tiền anh nộp ở năm cuối, mới chỉ kịp lăn có vài tháng.
Muốn đuổi kịp Lan, mỗi tháng Minh phải nộp khoảng ba triệu rưỡi, suốt hai mươi năm. ‖
Trong phép tính này, thứ quý nhất không phải số tiền.
Mà là mười năm đi trước.
Nhưng trước khi bạn vội kết luận, hãy nghe nốt phần còn lại. Vì có hai thứ mà phép tính đẹp đẽ này chưa nhắc tới.

## CH04 · Thứ lặng lẽ ăn mòn

Thứ đầu tiên là lạm phát.
Ba tỷ của ba mươi năm sau, không mua được nhiều như ba tỷ hôm nay. ‖
Hãy nhìn số thật của tám năm vừa qua.
Từ năm hai nghìn không trăm mười tám tới năm hai nghìn không trăm hai mươi lăm, giá cả ở Việt Nam tăng bình quân khoảng ba phẩy một phần trăm mỗi năm.
Nghe thì ít. Nhưng nó cũng là lãi kép, chỉ có điều chạy ngược chiều. ‖
Với tốc độ ấy, cứ khoảng hai mươi ba năm, sức mua của một đồng tiền còn lại một nửa.
Vậy ba tỷ của ba mươi năm sau, tính theo sức mua hôm nay, chỉ còn khoảng một tỷ hai. ‖
Vẫn hơn số tiền bạn đã nộp. Nhưng khác xa con số ba tỷ trên bảng tính.
Và đây là một con số thật nữa, để bạn so.
Tám năm qua, một cuốn sổ tiết kiệm mười hai tháng ở nhóm ngân hàng lớn, cứ đáo hạn lại gửi tiếp, biến một trăm đồng thành khoảng một trăm năm mươi sáu đồng.
Trừ đi lạm phát, còn lại khoảng một trăm hai mươi mốt đồng. ‖
Tức là lãi thật, sau khi giá cả đã tăng, chỉ hơn hai phần trăm một năm.
Không phải sáu.
Lãi kép vẫn chạy. Nhưng chậm hơn nhiều so với những bảng tính bạn hay thấy trên mạng.

## CH05 · Khi quả cầu tuyết lăn ngược

Thứ hai mà phép tính kia chưa nhắc, là lãi kép không đứng về phía ai cả.
Nó chỉ là một phép nhân.
Bạn gửi tiền, nó nhân cho bạn. Bạn nợ tiền, nó nhân cho người cho vay. ‖
Thử một ví dụ giả định.
Một khoản nợ ba mươi triệu, lãi hai mươi lăm phần trăm một năm, và bạn không trả đồng nào.
Sau một năm, nó thành hơn ba mươi tám triệu.
Sau ba năm, sáu mươi ba triệu.
Sau năm năm, hơn một trăm triệu. Gấp hơn ba lần. ‖
Cùng một quả cầu tuyết. Chỉ là lần này, nó lăn về phía bạn. ‖
Nên trước khi nghĩ tới chuyện để lãi kép làm việc cho mình, có một câu đáng hỏi trước.
Mình có khoản nợ nào đang chịu lãi cao hơn mức mình có thể kiếm được không?
Vì trả bớt một khoản nợ lãi hai mươi lăm phần trăm, cũng chính là dừng một quả cầu đang lăn ngược.

## CH06 · Khi nào phép tính này không đúng với bạn

Và giờ là phần mình luôn giữ ở cuối mỗi video.
Những lúc mà các con số vừa rồi không còn đúng với bạn. ‖
Thứ nhất, không có mức lãi nào đứng yên ba mươi năm.
Chỉ trong tám năm qua, lãi tiền gửi mười hai tháng ở nhóm ngân hàng lớn đã dao động từ dưới năm, tới hơn bảy phần trăm.
Đổi mức lãi giả định từ sáu xuống bốn phần trăm, ba tỷ kia chỉ còn khoảng hai tỷ mốt. ‖
Thứ hai, phép tính giả định bạn không rút ra lần nào trong ba mươi năm.
Không ốm đau, không mất việc, không việc gấp. Ngoài đời hiếm ai được như thế. ‖
Thứ ba, ba triệu của hôm nay và ba triệu của hai mươi năm nữa, là hai con số rất khác nhau so với thu nhập của bạn. ‖
Nên thay vì tin một bảng tính, bạn có thể tự hỏi ba câu.
Mức lãi trong bảng tính ấy là thật, hay là giả định?
Nó đã trừ lạm phát chưa?
Và mình có khoản nợ nào đang lăn ngược không? ‖
Lan không giỏi hơn Minh. Cô chỉ bắt đầu sớm hơn mười năm.
Còn quả cầu tuyết, dù lăn xuôi hay ngược, thì thứ nó cần nhất luôn là thời gian. ‖
Còn bạn, bạn bắt đầu để dành từ năm bao nhiêu tuổi?
Kể cho mình nghe ở phần bình luận nhé.

## Ghi chú

**Phép tính ví dụ** (`analysis.py` → `results.json`; lãi 6%/năm, nhập gốc hằng tháng, nộp cuối tháng, không rút — VÍ DỤ GIẢ ĐỊNH): 100 triệu để yên: lãi
đơn 30 năm 280, lãi kép (ghép năm) 574,3; lãi năm hai 6,36 triệu · nộp 3 triệu/tháng: 10 năm nộp 360 → 491,6 (lãi 26,8%); 20 năm nộp 720 → 1.386,1
(lãi 48,1%); 30 năm nộp 1.080 → 3.013,5 (lãi 64,2%) · năm đầu tiên tiền lãi trong năm > 36 triệu: **năm thứ 13** · Lan: 491,6 sau 10 năm, để yên 20 năm
→ 1.627,4 (×3,31); Minh: 1.386,1; chênh 241,3; Minh cần ~3,52 triệu/tháng để bằng Lan · quy tắc 72: 72/6 = 12 (chính xác 11,9 năm) · lạm phát 3,1%/năm →
sức mua còn một nửa sau 22,7 năm; 3.013,5 / 1,031^30 = 1.205,9 · nợ 30 triệu, 25%/năm (ghép tháng), không trả: 38,4 / 63,0 / 103,4 sau 1 / 3 / 5 năm ·
độ nhạy 30 năm: 4% → 2.082; 8% → 4.471.
**Số thật:** CPI bình quân năm 2018–2025: 3,54 · 2,79 · 3,23 · 1,84 · 3,15 · 3,25 · 3,63 · 3,31 (trung bình cộng 3,09%; hồ sơ A1 mục 6.3, 2018–2023 là
nguồn thứ cấp dẫn Cục Thống kê) · sổ 12 tháng nhóm ngân hàng lớn cuộn 10/2018 → 10/2026: ×1,56; CPI cùng kỳ ≈ +29% → thực ≈ ×1,21 (~2,4%/năm) (hồ sơ A1
mục 7.1, kênh tự tính, vài mốc suy từ tháng lân cận) · biên độ lãi 12 tháng 8 năm: 4,6% (06/2025) – 7,4% (11/2022, đầu 2023).
**Không nói:** câu "kỳ quan thứ tám" gán cho Einstein (không có nguồn gốc đáng tin). Lãi 25%/năm của khoản nợ là ví dụ giả định, không gán cho loại vay nào.
