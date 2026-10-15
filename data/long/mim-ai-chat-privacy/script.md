# "CUỘC TRÒ CHUYỆN CỦA BẠN ĐI ĐÂU?": kịch bản lời đọc (bản 1, chờ kiểm chứng)

**Tựa chính (đề xuất):** AI Có Học Từ Cuộc Trò Chuyện Của Bạn Không? Chuyện Gì Xảy Ra Với Những Gì Bạn Gõ Vào Chatbot

**Kênh:** Mind in the Machine (MIM) · **Giọng:** Hải Đăng (lời trích: Ngọc Huyền, lọc radio)
**Độ dài dự kiến:** ~12 phút, 8 chương
**Nguồn chính (đọc trực tiếp 09/10/2026):** OpenAI Help Center *Data controls in ChatGPT*, *Temporary chat in ChatGPT*, *Memory in ChatGPT*
(cập nhật ~09/2026); OpenAI *How your data is used to improve model performance* (cập nhật 13/03/2026); Google *Gemini Apps Privacy Hub*;
Anthropic *Updates to our consumer terms* (28/08/2025). Sự kiện: Fast Company / TechRadar / Search Engine Journal 07–08/2025 (link chia sẻ
ChatGPT trên Google); Bloomberg / The Register 02/05/2023 (Samsung). Luật 91/2025/QH15.

Quy ước: mỗi dòng là một câu đọc · `‖` = ngừng dài · `»` = lời trích (giọng trích, nguyên văn tiếng Anh hiện trên màn hình) ·
**[TRÍCH DỊCH]** = câu có thật dịch sang tiếng Việt.

**Cấu trúc giữ chân người xem:**
- **Cold open:** 31/07/2025 — hơn bốn nghìn năm trăm cuộc trò chuyện ChatGPT hiện trên Google: hồ sơ xin việc, tâm sự sức khoẻ tinh thần, mã
  nguồn công ty. Không phải bị hack: người dùng đã bấm chia sẻ và bật một ô cho phép tìm thấy.
- **Lộ trình, hình thức "Bản đồ bằng hình"** (MIM #1–#6 đã dùng: ba câu hỏi, chặng đường, lời thách, cảnh hẹn trước, nghịch lý, câu hỏi duy
  nhất): lời đọc một câu, màn hình vẽ sơ đồ **ba ngả** một tin nhắn có thể đi — *trí nhớ của trợ lý* · *dữ liệu huấn luyện* · *mắt người
  đọc* — mỗi chương sáng một ngả; CH07 sơ đồ hiện lại với "công tắc" trên từng ngả.
- **Vòng mở:** AI có học ngay không (CH00 → CH01) · nó nhớ gì về tôi (CH01 → CH02) · khi nào thành bài học (CH02 → CH03) · ai đọc được (CH03 →
  CH04) · chuyện gì xảy ra khi công ty để lộ (CH04 → CH05) · luật Việt Nam nói gì (CH05 → CH06) · làm gì ngay (CH00 → CH07).
- **Mô-típ:** "cái hộp thư" — tin nhắn gửi đi rồi thì không còn chỉ nằm trong máy bạn (gieo CH00, nhắc CH03, CH05, câu kết).
- **Trung thực:** chỉ nói điều các hãng tự viết trong trang trợ giúp/chính sách (đọc 09/10/2026), ghi rõ "theo trang trợ giúp của hãng";
  cài đặt và tên nút **có thể khác theo gói, vùng, phiên bản**; không nói hãng nào "an toàn hơn"; không khẳng định hãng "bán dữ liệu"; nhãn
  nút trên màn hình là **mô phỏng dựng bằng chữ**, không chụp giao diện thật.

---

## CH00 · Bốn nghìn rưỡi cuộc trò chuyện

Cuối tháng 7 năm 2025, một nhóm phóng viên công nghệ gõ vào Google một câu tìm kiếm rất đơn giản.
Họ tìm thấy hơn bốn nghìn năm trăm cuộc trò chuyện ChatGPT, nằm công khai trên kết quả tìm kiếm. ‖
Có hồ sơ xin việc, có tên thật.
Có những lời tâm sự về sức khoẻ tinh thần.
Có cả mã nguồn của công ty. ‖
Không ai bị hack cả.
Những cuộc trò chuyện ấy đã được chính người dùng bấm chia sẻ, và bật thêm một ô cho phép công cụ tìm kiếm thấy chúng.
Nhiều người có lẽ không hiểu ô ấy nghĩa là gì. ‖
Ngày 31 tháng 7, OpenAI gỡ bỏ tính năng đó.
Giám đốc an ninh thông tin của hãng gọi nó là một thử nghiệm ngắn ngủi.
» Tính năng này tạo ra quá nhiều cơ hội để mọi người vô tình chia sẻ những thứ họ không định chia sẻ. [TRÍCH DỊCH] ‖
Chuyện này làm nhiều người hỏi lại một câu cũ.
Những gì mình gõ vào chatbot, rồi đi đâu? AI có học từ cuộc trò chuyện của mình không?
Câu trả lời không phải có hay không. ‖
Một tin nhắn bạn gửi có thể đi theo ba ngả.
Vào trí nhớ của trợ lý. Vào dữ liệu để dạy phiên bản sau. Và trước mắt một con người.
Video này đi qua từng ngả, rồi chỉ bạn cách bật tắt từng cái.

## CH01 · Học và trò chuyện là hai chuyện khác nhau

Trước hết, phải tách hai việc mà ta hay gộp làm một: huấn luyện, và trò chuyện.
Huấn luyện là lúc mô hình được dạy, trên một lượng chữ khổng lồ, trong nhiều tuần hoặc nhiều tháng.
Khi xong, nó thành một khối số cố định, gọi là trọng số. ‖
Lúc bạn trò chuyện, khối số ấy không thay đổi.
Bạn dạy nó một mẹo hay, nó dùng được ngay trong cuộc trò chuyện đó.
Nhưng mô hình không tự sửa mình sau mỗi câu bạn gõ. ‖
Trong một cuộc trò chuyện, nó nhớ những gì đã nói bằng cách đọc lại cả đoạn hội thoại, mỗi lần trả lời.
Giống như bạn đưa cho một người lạ xem lại toàn bộ tin nhắn trước khi họ đáp.
Mở cuộc trò chuyện mới, tờ giấy ấy trống trơn. ‖
Tờ giấy ấy cũng có giới hạn độ dài.
Một cuộc trò chuyện rất dài, những gì nói ở đầu có thể bị cắt bớt hoặc tóm tắt lại, để còn chỗ cho phần mới.
Đó là lý do đôi khi chatbot quên điều bạn dặn từ cả trăm tin nhắn trước. ‖
Nói cách khác, trong cuộc trò chuyện, máy không học. Nó chỉ đọc.
Đọc rất nhanh, đọc toàn bộ, nhưng xong cuộc là thôi. ‖
Vậy câu "AI học từ tôi" sai à?
Không hẳn. Có hai cách để những gì bạn gõ đi xa hơn một cuộc trò chuyện.
Cách thứ nhất nằm ngay trong ứng dụng, và bạn nhìn thấy được: trí nhớ.

## CH02 · Ngả thứ nhất: trí nhớ

Nhiều trợ lý AI bây giờ có tính năng nhớ.
Theo trang trợ giúp của OpenAI, khi bật, ChatGPT có thể nhớ những sở thích và chi tiết liên quan từ các cuộc trò chuyện của bạn.
Để lần sau, bạn đỡ phải nhắc lại. ‖
Trí nhớ ấy có thể đến từ những điều bạn bảo nó ghi lại, và từ chính lịch sử trò chuyện cũ.
Bạn nói một lần rằng mình ăn chay, tuần sau nó gợi ý thực đơn không có thịt.
Tiện, nhưng cũng là một hồ sơ nhỏ về bạn, được ghi lại dần dần. ‖
Theo chính trang trợ giúp ấy, trí nhớ không giữ từng chi tiết của từng cuộc trò chuyện.
Máy tự quyết định thông tin nào liên quan để dùng, và điều nó nhớ có thể thay đổi theo thời gian.
Nghĩa là bạn không phải lúc nào cũng biết chính xác câu trả lời đang dựa vào điều gì về mình. ‖
Tin tốt là ngả này bạn kiểm soát được nhiều nhất.
Trong phần cài đặt, bạn xem được nó đang nhớ gì, xoá từng mục, hoặc tắt hẳn.
Theo OpenAI, khi bạn xoá một mục trí nhớ, nhật ký về mục ấy vẫn có thể được giữ thêm tối đa ba mươi ngày, vì lý do an toàn. ‖
Trí nhớ chỉ phục vụ riêng bạn.
Ngả thứ hai thì khác: những gì bạn gõ có thể góp vào bài học cho cả phiên bản sau.

## CH03 · Ngả thứ hai: dữ liệu huấn luyện

OpenAI viết thẳng trong trang chính sách của mình.
» ChatGPT, chẳng hạn, được cải thiện nhờ huấn luyện thêm trên các cuộc trò chuyện của mọi người, trừ khi bạn chọn không tham gia. [TRÍCH DỊCH] ‖
Với các dịch vụ cho cá nhân, mặc định là có thể dùng.
Muốn tắt, có một công tắc tên là Improve the model for everyone, nghĩa là cải thiện mô hình cho mọi người.
Tắt đi, những cuộc trò chuyện mới của bạn sẽ không được dùng để huấn luyện. ‖
Anthropic, hãng làm ra Claude, đổi chính sách vào ngày 28 tháng 8 năm 2025.
Người dùng các gói cá nhân phải tự chọn có cho dùng cuộc trò chuyện để huấn luyện hay không.
Nếu đồng ý, dữ liệu có thể được giữ tới năm năm. Nếu không, thời hạn vẫn là ba mươi ngày. ‖
Với Gemini của Google, cài đặt quan trọng tên là Keep Activity, giữ lại hoạt động.
Theo trang trợ giúp, khi tắt nó và không gửi phản hồi, những cuộc trò chuyện sau đó của bạn không được dùng để cải thiện mô hình. ‖
Có một điểm chung đáng nhớ.
Cả ba hãng đều tách riêng các gói cho doanh nghiệp: dữ liệu ở đó mặc định không dùng để huấn luyện.
Còn với người dùng thường như chúng ta, mặc định thường là bật, và việc tắt là việc của mình.
Như một lá thư đã bỏ vào hộp: muốn nó không được mở ra đọc, phải dặn trước khi gửi. ‖
Mà nói tới đọc, ngả thứ ba mới là ngả ít người nghĩ tới nhất.

## CH04 · Ngả thứ ba: một con người

Nhiều người nghĩ cuộc trò chuyện với AI chỉ có mình và cái máy.
Trang quyền riêng tư của Gemini viết rõ:
» Một phần các cuộc trò chuyện được người đánh giá xem xét, bao gồm cả nhà cung cấp dịch vụ được Google đào tạo, để giúp cải thiện các dịch vụ của Google. [TRÍCH DỊCH] ‖
Người đánh giá xem câu trả lời của AI có kém, sai hay gây hại không, và gợi ý câu trả lời tốt hơn.
Chi tiết đáng chú ý nằm ở thời hạn.
Những cuộc trò chuyện đã được người xem xét không bị xoá khi bạn xoá lịch sử. Chúng được giữ tới ba năm. ‖
Google tự đưa ra một lời khuyên ngay trên trang ấy.
» Xin đừng nhập thông tin bí mật mà bạn không muốn người đánh giá nhìn thấy. [TRÍCH DỊCH]
Đây là một trong những câu thật lòng nhất mà một hãng công nghệ viết cho người dùng. ‖
Ngay cả khi tắt lưu hoạt động, hay dùng trò chuyện tạm thời, Google vẫn giữ cuộc trò chuyện trong bảy mươi hai giờ, để trả lời bạn và để giữ an toàn.
OpenAI cũng giữ bản sao trò chuyện tạm thời tối đa ba mươi ngày, vì lý do an toàn. ‖
Vậy chuyện gì xảy ra khi những gì được gõ vào không phải chuyện riêng của một người, mà là bí mật của cả một công ty?

## CH05 · Ba lần trong một tháng

Tháng 4 năm 2023, ở bộ phận bán dẫn của Samsung, các kỹ sư bắt đầu dùng ChatGPT để làm việc.
Một người dán mã nguồn nội bộ vào để nhờ sửa lỗi.
Một người khác dán ghi chép của một cuộc họp. ‖
Trong vòng một tháng, công ty ghi nhận ba lần thông tin nội bộ bị đưa vào ChatGPT như vậy.
Đầu tháng 5, Samsung gửi thông báo nội bộ: tạm cấm dùng các công cụ AI tạo sinh trên máy tính của công ty. ‖
Theo tài liệu mà hãng tin Bloomberg được xem, điều Samsung lo không phải là AI học ngay lập tức.
Mà là dữ liệu đã nằm trên máy chủ bên ngoài, khó lấy lại, khó xoá, và có thể lộ ra cho người khác. ‖
Cùng thời gian ấy, ở châu Âu, một cơ quan nhà nước còn đi xa hơn.
Ngày 31 tháng 3 năm 2023, cơ quan bảo vệ dữ liệu của Ý tạm thời chặn ChatGPT trên toàn nước Ý.
Lý do họ nêu: người dùng không được thông báo đầy đủ, và việc thu thập dữ liệu cá nhân hàng loạt để huấn luyện thiếu cơ sở pháp lý. ‖
Gần một tháng sau, ngày 28 tháng 4, ChatGPT được hoạt động trở lại ở Ý, sau khi OpenAI đáp ứng nhiều yêu cầu của cơ quan này.
Cũng trong những ngày ấy, ngày 25 tháng 4, OpenAI ra mắt cách tắt lịch sử trò chuyện, để những cuộc trò chuyện ấy không bị dùng huấn luyện.
Đó là tiền thân của công tắc mà bạn sẽ thấy ở cuối video. ‖
Đó chính là điểm mấu chốt của cả video này.
Bấm gửi rồi, tin nhắn không còn chỉ nằm trong máy bạn.
Nó nằm trong hộp thư của người khác, theo luật chơi của người khác.

## CH06 · Ở Việt Nam

Ở Việt Nam, từ ngày 1 tháng 1 năm 2026, Luật Bảo vệ dữ liệu cá nhân chính thức có hiệu lực.
Đây là đạo luật riêng đầu tiên của Việt Nam về dữ liệu cá nhân, được Quốc hội thông qua tháng 6 năm 2025.
Trước đó, từ tháng 7 năm 2023, việc này chỉ nằm trong một nghị định, Nghị định mười ba. Giờ nó được nâng lên thành luật. ‖
Luật đặt ra nguyên tắc: dữ liệu cá nhân chỉ được thu thập và xử lý đúng phạm vi, đúng mục đích cụ thể.
Hành vi mua bán dữ liệu cá nhân có thể bị phạt tới mười lần khoản thu có được từ vi phạm. ‖
Nhưng luật không thay được thói quen.
Thứ dễ bảo vệ nhất vẫn là thứ bạn chưa bao giờ gõ vào.
Vậy cụ thể, nên làm gì?

## CH07 · Bật tắt từng ngả

Quay lại tấm bản đồ ba ngả. Mỗi ngả có một công tắc.
Tên nút có thể khác theo gói, theo vùng và theo phiên bản, nhưng chức năng thì giống nhau. ‖
Ngả trí nhớ: vào phần cài đặt, mục cá nhân hoá hoặc trí nhớ.
Xem nó đang nhớ gì về bạn, xoá những gì không muốn giữ, hoặc tắt hẳn. ‖
Ngả huấn luyện: với ChatGPT là công tắc Improve the model for everyone trong phần kiểm soát dữ liệu.
Với Claude là cài đặt cho phép dùng dữ liệu để huấn luyện trong phần quyền riêng tư.
Với Gemini là Keep Activity. ‖
Ngả con người: không có công tắc nào tắt được hoàn toàn.
Cách duy nhất là cẩn thận với những gì bạn gõ.
Khi cần hỏi chuyện nhạy cảm, hãy dùng chế độ trò chuyện tạm thời: không lưu vào lịch sử, không dùng để huấn luyện, dù vẫn có thể được giữ một thời gian ngắn vì lý do an toàn. ‖
Và có năm thứ không nên dán vào chatbot nào, dù đã tắt mọi công tắc.
Số căn cước. Mật khẩu và mã xác thực. Số tài khoản, số thẻ ngân hàng.
Thông tin riêng của người khác. Và tài liệu nội bộ của nơi bạn làm. ‖
Cuối cùng, nút chia sẻ.
Một đường link chia sẻ là một cánh cửa mở. Ai có link đều đọc được, và bốn nghìn rưỡi cuộc trò chuyện năm 2025 là lời nhắc rằng cánh cửa ấy có thể mở rộng hơn bạn tưởng. ‖
AI không học từ bạn trong từng câu trò chuyện.
Nhưng những gì bạn gõ có thể đi xa hơn cuộc trò chuyện ấy rất nhiều.
Còn bạn, bạn đã từng dán vào chatbot thứ gì mà giờ nghĩ lại thấy hơi lo không? Kể cho mình nghe ở phần bình luận nhé, nhớ đừng dán lại nó.

## Ghi chú

**Kiểm chứng vòng 1 (PM 09/10, chiều):** Samsung — sự cố ở bộ phận Device Solutions (bán dẫn), 3 vụ (mã nguồn, biên bản họp); thông báo gửi
bộ phận Device eXperience, "tạm cấm trên máy tính công ty từ 01/05" (Business Today, SamMobile, Bloomberg 02/05/2023) → câu CH05 đã sửa ·
Data controls ChatGPT ra mắt **25/04/2023** ("turn off chat history… won't be used to train") — trước khi Ý mở lại 28/04 → bỏ câu nhân quả,
thay bằng mốc thời gian + "tiền thân" (OpenAI blog *New ways to manage your data in ChatGPT*; CNBC 25/04/2023) · câu Stuckey: chưa đọc được
bài X gốc — nguyên văn lấy từ TechRadar/SEJ 08/2025, giữ nhãn TRÍCH DỊCH, ghi nguồn báo trên màn hình.

**Cần kiểm chứng:**
1. CH00: "hơn 4.500" (Fast Company, qua Search Engine Journal / TechRadar 07–08/2025); 31/07/2025 Dane Stuckey (CISO OpenAI) gỡ tính năng, câu
   "a short-lived experiment" + "introduced too many opportunities for folks to accidentally share things they didn't intend to" — đọc
   bài gốc / bài đăng X của Stuckey để lấy nguyên văn hiển thị.
2. CH02: Memory — trang *Memory in ChatGPT* (đọc 09/10/2026): nguồn trí nhớ gồm past chats, saved memories, custom instructions…; xoá saved
   memory: "may retain logs of deleted saved memories for up to 30 days for safety and debugging purposes" ✔ đã đọc.
3. CH03: câu OpenAI "ChatGPT, for instance, improves by further training on the conversations people have with it, unless you opt out" ✔
   (trang *How your data is used…*, cập nhật 13/03/2026); công tắc "Improve the model for everyone" ✔ (*Data controls in ChatGPT*); doanh
   nghiệp: "By default, OpenAI does not use content from ChatGPT Business, Enterprise, Edu… workspaces to train" ✔.
4. CH03: Anthropic 28/08/2025, 5 năm / 30 ngày, hạn 08/10/2025, loại trừ Claude for Work/API/Gov/Education ✔ (trang Anthropic). Tên công tắc
   hiện tại trong ứng dụng ("Help improve Claude"?) — kiểm lại trước khi dựng, lời đọc dùng mô tả chung.
5. CH03–04: Gemini Privacy Hub ✔ đã đọc: human reviewers; giữ tới 3 năm; 72 giờ khi Keep Activity tắt / trò chuyện tạm thời; "Temporary chats
   are not used to train"; câu "Please don't enter confidential information that you wouldn't want a reviewer to see…" ✔. "Keep Activity bật
   mặc định cho người lớn" — SECONDARY, lời đọc không nói "mặc định" cho Gemini.
6. CH05: Samsung — Bloomberg 02/05/2023 (qua The Register, Forbes AU, Fox Business): 3 lần trong ~1 tháng, mã nguồn + ghi chép họp, cấm ở
   bộ phận lớn (Device eXperience?) — kiểm phạm vi lệnh cấm ("một trong các bộ phận lớn nhất" vs "toàn công ty") rồi sửa câu cho đúng.
9. CH05: Garante (Ý) chặn tạm thời 31/03/2023, cho hoạt động lại 28/04/2023; lý do: thiếu thông tin cho người dùng, thiếu cơ sở pháp lý
   thu thập dữ liệu để huấn luyện (+ sự cố lộ dữ liệu 20/03/2023); OpenAI thêm cách từ chối dùng dữ liệu huấn luyện (privacylaws.com, Fox
   Business, The Decoder). Câu "công tắc… ra đời một phần từ lần bị chặn" là diễn giải — kiểm: Data Controls (tắt lịch sử) ra mắt 25/04/2023,
   trước khi Ý mở lại; nếu không khớp thì đổi thành "cùng thời gian ấy".
10. CH06: NĐ 13/2023/NĐ-CP hiệu lực 01/07/2023, bị Luật 91/2025 + NĐ 356/2025 thay thế (LuatVietnam, PwC 01/2026).
7. CH06: Luật 91/2025/QH15 thông qua 26/06/2025, hiệu lực 01/01/2026 ✔ (LuatVietnam); "phạt tới 10 lần khoản thu" cho mua bán dữ liệu ✔
   (SECONDARY — đọc điều luật gốc); "đạo luật riêng đầu tiên" — kiểm (trước đó có NĐ 13/2023, không phải luật).
8. CH04: "OpenAI giữ bản sao trò chuyện tạm thời tối đa 30 ngày" ✔ (*Temporary chat in ChatGPT*).
