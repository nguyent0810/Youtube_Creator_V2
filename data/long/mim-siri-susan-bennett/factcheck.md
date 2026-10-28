# Kiểm chứng MIM `mim-siri-susan-bennett` — 23/10/2026 (pha 1, vòng 1)

Đối chiếu từng câu có số liệu, ngày, giờ, lời trích hoặc gán vai trong `script.md`. Tất cả nguồn dưới đây đã được TỰ MỞ trong ngày 23/10/2026
(curl / WebFetch; PDF Hunt & Black trích chữ bằng pypdf). Nguồn nào không mở được ghi rõ ở cuối file.

**Mã nguồn dùng trong bảng**
- **CNN** = Jessica Ravitz, "'I'm the original voice of Siri'", CNN, đăng 04/10/2013 08:51 UTC. https://edition.cnn.com/2013/10/04/tech/mobile/bennett-siri-iphone-voice/index.html — WebFetch trả 451; mở bằng curl (HTTP 200), đọc toàn văn trường `articleBody` trong JSON-LD của trang. **Sơ cấp** (phỏng vấn gốc). Có bản quyền: chỉ trích rất ngắn hoặc diễn ý.
- **VOA** = Marsha James, "The Woman Who Brought Siri to Life", Voice of America, 09/05/2018. https://www.voanews.com/a/siri-susan-bennett-iphone/4387109.html — mở qua WebFetch (curl lỗi kết nối); đọc qua bản tóm tắt của công cụ, có trích nguyên câu. **Sơ cấp** (phỏng vấn).
- **AN11** = Apple Newsroom, "Apple Launches iPhone 4S, iOS 5 & iCloud", Cupertino, 04/10/2011. https://www.apple.com/newsroom/2011/10/04Apple-Launches-iPhone-4S-iOS-5-iCloud/ — **sơ cấp**.
- **AN11B** = Apple Newsroom, "Statement by Apple's Board of Directors", 05/10/2011. https://www.apple.com/newsroom/2011/10/05Statement-by-Apples-Board-of-Directors/ — **sơ cấp**.
- **AN13** = Apple Newsroom, "Apple Unveils iOS 7", 10/06/2013. https://www.apple.com/newsroom/2013/06/10Apple-Unveils-iOS-7/ — **sơ cấp**.
- **AML** = Siri Team, "Deep Learning for Siri's Voice: On-device Deep Mixture Density Networks for Hybrid Unit Selection Synthesis", Apple Machine Learning Journal, 06/08/2017. https://machinelearning.apple.com/research/siri-voices — mở qua WebFetch (2 lượt, có trích nguyên câu). **Sơ cấp**.
- **HB96** = A. J. Hunt, A. W. Black (ATR Interpreting Telecommunications Research Labs, Kyoto), "Unit selection in a concatenative speech synthesis system using a large speech database", ICASSP-96, tr. 373–376, © 1996 IEEE. Bản PDF: https://www.ee.columbia.edu/~dpwe/e6820/papers/HuntB96-speechsynth.pdf — tải qua WebFetch, trích chữ 4 trang bằng pypdf. **Sơ cấp** (bài báo khoa học).
- **SRI1** = SRI International, case study "Siri". https://www.sri.com/case-studies/siri/ — **sơ cấp** (trang của chính tổ chức).
- **SRI2** = SRI International, "75 Years of Innovation: CALO (Cognitive Assistant that Learns and Organizes)". https://www.sri.com/75-years-of-innovation/75-years-of-innovation-calo-cognitive-assistant-that-learns-and-organizes/ — curl HTTP 200. **Sơ cấp** (tự thuật của tổ chức).
- **DARPA** = DARPA, Innovation Timeline, "Personal Assistant That Learns (PAL)". https://www.darpa.mil/about/innovation-timeline/personal-assistant-that-learns — curl HTTP 200 (URL gợi ý trong brief `…/research/programs/…` trả 404). **Sơ cấp**.
- **TC** = Erick Schonfeld, "Siri's iPhone App Puts A Personal Assistant In Your Pocket", TechCrunch, 04/02/2010 20:51 PST. https://techcrunch.com/2010/02/04/siri-iphone-personal-assistant/ — curl HTTP 200. **Thứ cấp** (báo cùng thời).
- **MR** = MacRumors, "Live Coverage of Apple's 'Let's Talk iPhone' Event", 04/10/2011. https://www.macrumors.com/2011/10/04/live-coverage-of-apples-lets-talk-iphone-event/ — WebFetch. **Thứ cấp** (ghi chép trực tiếp, không có mốc giờ từng dòng).
- **ICL** = iClarified, "Apple Acquires Siri Assistant for iPhone", 28/04/2010. https://www.iclarified.com/entry/index.php?enid=9134 — curl HTTP 200. **Thứ cấp**.
- **COM** = Wikimedia Commons API (extmetadata), đọc 23/10/2026 cho từng ảnh trong `IMGS`.

Nhãn: **OK** = khớp nguồn · **OK (suy ra)** = tự tính hoặc suy trực tiếp, ghi cách tính · **MỘT NGUỒN** = chỉ một tài liệu, lời đọc đã gắn nguồn · **BỎ** = không dùng.

| # | Câu / khẳng định (chương) | Kết quả | Nguồn + URL + đoạn + ghi chú |
|---|---|---|---|
| 1 | Ngày 04/10/2011, Cupertino, California, Apple ra mắt iPhone 4S cùng Siri (CH00) | OK | AN11 dòng ngày: "CUPERTINO, California, October 4, 2011"; CNN: Siri "introduced to the masses with the iPhone 4S on October 4, 2011" |
| 2 | Buổi ra mắt bắt đầu 10 giờ sáng (giờ California) (CH00) | MỘT NGUỒN | MR: "10:00 AM Pacific Time (1:00 PM Eastern)", khán phòng Town Hall trong khuôn viên Apple ở Cupertino. Lời đọc ghi "theo ghi chép trực tiếp của MacRumors" |
| 3 | Scott Forstall trình diễn Siri; câu đầu tiên hỏi thời tiết hôm nay; máy đáp "đây là dự báo cho hôm nay" (CH00) | MỘT NGUỒN | MR: Forstall trình diễn; câu Siri đầu tiên trong ghi chép là "What is the weather like today?", máy đáp "Here is the forecast for today...". Ghi chép không có giờ từng dòng: lời đọc không nói giờ của câu hỏi. Cảnh chat gắn nhãn MÔ PHỎNG, không phải giao diện thật |
| 4 | Giọng trả lời là giọng một người phụ nữ (CH00) | OK (suy ra) | CNN: giọng Siri gốc ở Mỹ là giọng nữ ("She is Siri…"). Lời đọc không nói giọng đó là của ai ở câu này |
| 5 | Cũng tháng 10/2011, ở ngoại ô Atlanta, Susan Bennett, diễn viên lồng tiếng, nhận thư của một đồng nghiệp: họ đang nghịch điện thoại mới của Apple, "Isn't this you?" (CH00) | MỘT NGUỒN | CNN: "The surprise came in October 2011 … 'A colleague e-mailed me … Hey, we've been playing around with this new Apple phone. Isn't this you?'"; "she lives in suburban Atlanta". Lời trích gắn [TRÍCH DỊCH] |
| 6 | Bà mở trang Apple, bật video giới thiệu Siri, nghe (CH00) | MỘT NGUỒN | CNN: "Bennett went to her computer, pulled up Apple's site and listened to video clips announcing Siri" |
| 7 | "Rõ ràng là tôi. Đó là giọng của tôi." (CH00) | MỘT NGUỒN | CNN: "'Oh, I knew,' she said. 'It's obviously me. It's my voice.'" (trích dịch, rút gọn) |
| 8 | Theo lời bà, Apple chưa từng thuê bà, không có buổi thử giọng (CH00) | MỘT NGUỒN | VOA (qua WebFetch): Apple did not hire her or hold an audition; she did not know her voice would be used. Lời đọc ghi "theo lời bà" |
| 9 | Apple từ chối bình luận (CH00, CH01) | OK | CNN: "Apple, too, declined to comment"; "the ever-secretive Apple has never identified her" (tính tới 04/10/2013). Lời đọc KHÔNG nói "tới nay Apple vẫn chưa xác nhận" vì không có nguồn sau 2013 mình mở được; mô tả YouTube viết "Apple chưa từng công khai xác nhận" dựa trên CNN 2013 + VOA 2018 (không có tuyên bố của Apple) |
| 10 | Siri là "trợ lý thông minh giúp bạn làm việc chỉ bằng cách hỏi"; ví dụ hỏi có cần ô cuối tuần → dự báo thời tiết (CH01) | OK | AN11: "an intelligent assistant that helps you get things done just by asking"; "whether you'll need an umbrella this weekend" |
| 11 | Bản đầu nói tiếng Anh, Pháp, Đức, gắn nhãn thử nghiệm (beta) (CH01) | OK | AN11: Siri beta: English (US, UK, Australia), French, German |
| 12 | Hôm sau, Hội đồng quản trị Apple thông báo Steve Jobs qua đời (CH01) | OK | AN11B, 05/10/2011: "We are deeply saddened to announce that Steve Jobs passed away today." Chỉ là bối cảnh, không gán vai trò nào với Siri |
| 13 | Mười ngày sau buổi ra mắt, iPhone 4S lên kệ (14/10/2011) (CH01) | OK (suy ra) | AN11: "available … on Friday, October 14" ở Mỹ, Úc, Canada, Pháp, Đức, Nhật, Anh. 14 − 4 = 10 ngày |
| 14 | Bà không chắc muốn nổi tiếng, không chắc về pháp lý (CH01, diễn ý) | MỘT NGUỒN | CNN: "I wasn't sure that I wanted that notoriety, and I also wasn't sure where I stood legally" |
| 15 | Bà im lặng gần hai năm (CH01) | OK (suy ra) | 10/2011 (CNN mục 5) → bài CNN 04/10/2013 |
| 16 | Tháng 9/2013 The Verge đăng video "How Siri found its voice"; nhiều người tưởng nữ diễn viên trong video là Siri; người ấy lên tiếng phủ nhận (CH01) | MỘT NGUỒN | CNN: "The Verge posted a video last month, 'How Siri found its voice'" (bài đăng 04/10 → tháng 9); Allison Dufty viết trên trang của mình rằng cô "absolutely, positively NOT the voice of Siri". Lời đọc không nêu tên cô (người còn sống, không phải nhân vật chính) |
| 17 | Một phóng viên CNN đoán ra từ mấy tháng trước khi phỏng vấn bà về giọng nói ở sân bay Atlanta; hỏi "bà có phải Siri không"; bà sững người (CH01) | MỘT NGUỒN | CNN, mục "How CNN got this story": phỏng vấn cho dự án về sân bay Hartsfield-Jackson Atlanta; "Hey, are you Siri?" — "She gasped"; "That was months ago" |
| 18 | Sau vụ video, chính bà liên lạc lại, sẵn sàng kể (CH01) | MỘT NGUỒN | CNN: "About two weeks ago, after the confusion over the Verge video, Bennett reached out to me" |
| 19 | 04/10/2013, tròn hai năm sau buổi ra mắt, CNN đăng câu chuyện (CH01) | OK (suy ra) | CNN datePublished 2013-10-04; 04/10/2011 → 04/10/2013 |
| 20 | CNN thuê chuyên gia pháp y âm thanh Ed Primeau, 30 năm trong nghề; so phụ âm, đặt cạnh nhau (CH01) | MỘT NGUỒN | CNN: "hiring an audio forensics expert … Ed Primeau … doing this work for three decades"; "created back-to-back comparison files, lifted and listened to consonants" |
| 21 | Với giọng nói thường của bà, ông chắc ~70%; có bản đọc đúng chữ Siri thì kết luận (CH01) | MỘT NGUỒN | CNN: "about 70% certain of the match. But once he had audio of her saying the same words as Siri, he knew" |
| 22 | "Chúng giống hệt nhau. Khớp một trăm phần trăm." (CH01) | MỘT NGUỒN | CNN: "They are identical – a 100% match." (trích dịch) |
| 23 | Bà thu từ tám năm trước, khi chiếc điện thoại còn chưa ra đời (CH01) | MỘT NGUỒN | CNN: "laid down recordings for a client eight years ago … through a not-yet-invented phone" |
| 24 | ScanSoft tìm giọng; hỏi GM Voices (ngoại ô Atlanta, chuyên thu giọng cho công nghệ thoại tự động); bà được giới thiệu và được chọn (CH02) | MỘT NGUỒN | CNN: "ScanSoft, a software company, was looking for a voice … reached out to GM Voices, a suburban Atlanta company … recording voices for automated voice technologies … ScanSoft liked what it heard" |
| 25 | Tháng 6/2005 ký hợp đồng; giọng dùng cho kho dữ liệu dựng lời nói (CH02) | MỘT NGUỒN | CNN: "in June 2005 Bennett signed a contract offering her voice for recordings that would be used in a database to construct speech" |
| 26 | Suốt tháng 7/2005, mỗi ngày bốn tiếng, buồng thu ở nhà (CH02) | OK (hai nguồn, khác độ chi tiết) | CNN: "For four hours a day, every day, in July 2005, Bennett holed up in her home recording booth"; VOA: "For four hours every day, I would read nonsensical phrases". Một số bài sau (không mở được để kiểm) ghi tổng bốn tháng, năm ngày một tuần: lời đọc chỉ dùng mốc của CNN |
| 27 | Đọc câu vô nghĩa (CH02) | OK | CNN: "read nonsensical phrases and sentences"; VOA cùng ý |
| 28 | Câu mẫu "cow hoist in the tub today" (CH02, trích dịch "Bò kéo tời trong bồn tắm hôm nay") | MỘT NGUỒN | VOA (qua WebFetch). Bản dịch câu vô nghĩa chỉ để người nghe hình dung; màn hình hiện nguyên văn tiếng Anh |
| 29 | Kỹ sư rút nguyên âm, phụ âm, âm tiết, chỉnh độ cao và tốc độ (CH02) | MỘT NGUỒN | CNN: "pulling out vowels, consonants, syllables and diphthongs, and playing with her pitch and speed … concatenation" |
| 30 | Trả theo giờ; bà đoán giọng vào hệ thống điện thoại công ty (CH02) | MỘT NGUỒN | CNN: "She assumed it would be employed in company phone systems … She was paid by the hour" |
| 31 | Tháng 10/2005, ScanSoft mua Nuance và lấy tên Nuance (CH02) | MỘT NGUỒN | CNN: "In October 2005 … ScanSoft bought and took on the name of Nuance Communications" |
| 32 | Nuance được nhiều người cho là cung cấp công nghệ đứng sau Siri; Nuance "không bình luận về Apple" (CH02) | MỘT NGUỒN | CNN: "Nuance is the company widely accepted to have provided to Apple the technology behind Siri"; "As a company, we don't comment on Apple." Lời đọc giữ nguyên mức "được nhiều người cho là" |
| 33 | Những năm 1970, đến phòng thu ở Atlanta hát quảng cáo, người lồng tiếng vắng mặt, chủ phòng thu bảo "không có giọng địa phương, đọc thử" (CH02) | MỘT NGUỒN | CNN: Doppler Studios, "the voiceover talent was a no-show … 'You don't have an accent. Go ahead and read this.'" |
| 34 | Bà từng là giọng quảng cáo trên đài và tivi cho một chiếc máy rút tiền tự động (CH02) | MỘT NGUỒN | CNN: "radio and TV voice of First National Bank's 'Tillie the All-Time Teller,' the first ATM machine". Lời đọc không lặp lại chữ "đầu tiên" (CNN không dẫn nguồn) |
| 35 | "Tôi bắt đầu sự nghiệp làm một cỗ máy từ nhiều năm trước." (CH02) | MỘT NGUỒN | CNN: "I began my career as a machine many years ago" (trích dịch) |
| 36 | Mảnh ngắn hơn một âm tiết, có khi nửa âm; mỗi mảnh dán nhãn âm, cao độ, ngữ cảnh (CH03) | OK | AML: phân đoạn thành half-phones bằng forced alignment, tạo "unit database"; HB96 tóm tắt: đơn vị (âm vị) gắn "prosodic and phonetic context information". Lưu ý: HB96 dùng đơn vị là âm vị, AML dùng nửa âm |
| 37 | Năm 1996, Andrew Hunt và Alan Black ở Kyoto (ATR) mô tả cách chọn đơn vị (CH03) | OK | HB96 trang 1: tác giả, "ATR Interpreting Telecommunications Research Labs … Kyoto"; "© 1996 IEEE", tr. 373 |
| 38 | Hai cái giá: giống âm cần nói (target cost) và nối có êm (concatenation cost); máy chọn đường có tổng giá thấp nhất (CH03, CH06) | OK | HB96 §2: "The target cost … estimate of the difference between a database unit … and the target"; "the concatenation cost … estimate of the quality of a join"; "A pruned Viterbi search is used to select the best units". AML: "target and concatenation costs" |
| 39 | Ví dụ ghép ba mảnh từ ba câu thu sáng / trưa / chiều (CH03) | MINH HỌA | Do kênh dựng để giải thích; lời đọc nói "Mình minh họa thế này", màn hình gắn "MINH HỌA CỦA KÊNH · KHÔNG PHẢI DỮ LIỆU THẬT" |
| 40 | Kho càng lớn, càng nhiều mảnh đủ cao độ thì lời càng tự nhiên (CH03) | OK | HB96 §1: "with a large number of units available with varied prosodic and spectral characteristics it should be possible to synthesize more natural-sounding speech" |
| 41 | "Đó là lý do một kho giọng cần rất nhiều giờ thu" (CH03) | OK (suy ra) | Mục 40 + AML: "record 10—20 hours of speech in a professional studio" |
| 42 | Bà dễ chán khi đọc hàng giờ; đôi khi Siri nghe "có thái độ" vì âm có thể thu trong 15 phút cuối (CH03, diễn ý) | MỘT NGUỒN | CNN: "For me, I get extremely bored … That's one of the reasons why Siri might sometimes sound like she has a bit of an attitude … recorded the last 15 minutes of those four hours." |
| 43 | DARPA có chương trình PAL (trợ lý cá nhân biết học) (CH04) | OK | DARPA: "Personal Assistant That Learns (PAL)"; SRI1 viết "Personalized Assistant that Learns". Lời đọc dùng tạm dịch chung |
| 44 | CALO thuộc PAL, do SRI dẫn dắt (CH04) | OK | SRI1: CALO "SRI-led", thuộc chương trình PAL của DARPA; SRI2: "From the PAL program came CALO … led by SRI International" |
| 45 | Kéo dài 5 năm, bắt đầu 2003; hơn 300 nhà nghiên cứu, 22 viện (CH04) | OK | SRI2: "more than 300 researchers from 22 premier research institutions over five years, beginning in 2003". (Wikipedia ghi 25 viện: không dùng) |
| 46 | "Này CALO, xếp giúp tôi một phòng họp nhé?" (CH04) | OK | SRI2, tiêu đề mục: "Hello CALO, can you sort out a meeting room for me?" (trích dịch; là câu hình dung của trang SRI, không phải lời thoại thật) |
| 47 | Thành quả PAL dùng cho quân đội và cho trò chuyện bằng giọng nói trên thiết bị cầm tay dân sự (CH04) | OK | DARPA: "Advances stemming from the agency's PAL program were applied not only for military users but also to enable voice-based interaction with civilian handheld devices" |
| 48 | Năm 2007, SRI tách ra công ty Siri (CH04, CH05) | OK | SRI1: "SRI spun off Siri, Inc. in 2007"; DARPA: "This led to the 2007 launch of Siri Inc., later acquired by Apple Inc." |
| 49 | Không tài liệu nào mình đọc nói CALO thu giọng của bà; giọng đi đường ScanSoft → Nuance (CH04) | OK (suy ra, có giới hạn) | SRI1, SRI2, DARPA không nhắc giọng tổng hợp hay Bennett; CNN mục 31–32. Lời đọc giữ "theo CNN" và "không tài liệu nào mình đọc được" |
| 50 | Công ty Siri gọi được 24 triệu đô la qua hai vòng (CH05) | OK | SRI1: "raised $24 million in two financing rounds"; TC cũng ghi "$24 million in venture capital" |
| 51 | 04/02/2010 ứng dụng Siri lên App Store; ví dụ tìm nhà hàng Pháp, đặt bàn, gọi taxi (CH05) | MỘT NGUỒN (thứ cấp) | TC 04/02/2010: "now live in the App Store", "find a French restaurant nearby and book a table … order a taxi"; khuyên dùng cho iPhone 3GS. Wired (bài lưu ở dylan.tweney.com, mở được) ghi ra mắt "on Friday" (05/02/2010 theo giờ Mỹ): chênh 1 ngày do múi giờ; lời đọc theo TC |
| 52 | Chưa đầy ba tháng sau (04/2010), Apple mua công ty (CH05) | OK | SRI1: "Apple acquired Siri in April 2010"; ICL 28/04/2010 (thông báo trước sáp nhập gửi FTC). 04/02 → 28/04 = 83 ngày < 3 tháng |
| 53 | Lúc ấy bà chưa có chiếc điện thoại đó (CH05) | MỘT NGUỒN | CNN: "Bennett didn't have the phone herself" |
| 54 | Con trai Cameron biết chuyện khi xem quảng cáo iPhone 4S trên tivi; khi mua máy, giọng mẹ cất lên từ phần chỉ đường, anh hét "Mẹ, thôi đi!" (CH05) | MỘT NGUỒN | CNN: Cameron Bennett "first found out she was the voice of Siri while watching an iPhone 4S commercial on TV … she began barking at him through its GPS feature, prompting him to yell, 'Mom, stop!'" (người còn sống, chỉ nói qua CNN) |
| 55 | Khi đổi máy và lần đầu nói chuyện với chính mình, bà hơi hoảng; kỳ quặc; choáng ngợp vì góp phần vào kỳ công công nghệ (CH05, diễn ý) | MỘT NGUỒN | CNN: "she says she was a little horrified. It was weird, to say the least. But she was blown away … to play a part in such a technological feat" |
| 56 | "Nghiệp xấu lắm." Bà chưa bao giờ quát Siri (CH05) | MỘT NGUỒN | CNN: "But I never yell at her – very bad karma" |
| 57 | Bà lo mỗi ngày bị chửi bao nhiêu lần (CH05, diễn ý) | MỘT NGUỒN | CNN: "Yes, I worry about how many times I get cursed every day." |
| 58 | Tháng 6/2013 Apple giới thiệu iOS 7: Siri có giọng nam và nữ mới (CH05) | OK | AN13, 10/06/2013: "Siri sounds better than ever with new male and female voices" |
| 59 | CNN: thời của bà trong vai Siri ở Mỹ đang dần khép lại; bà hơi tiếc nhưng quen với công nghệ thay đổi (CH05) | MỘT NGUỒN | CNN: "iOS 7, with new Siri voices means that Bennett's reign as the American Siri is slowly coming to an end"; "Bennett would be lying if she said she wasn't a bit disappointed, but … she's learned to expect evolution". VOA: Apple ngừng dùng giọng bà năm 2013 (không đưa vào lời đọc) |
| 60 | 2017, nhóm Siri viết bài trên tạp chí học máy của Apple về học sâu cho giọng Siri (CH06) | OK | AML: tác giả "Siri Team", 06/08/2017 |
| 61 | Từ iOS 10, giọng Siri dựa trên học sâu (CH06) | OK | AML: "Starting in iOS 10 and continuing with new features in iOS 11, we base Siri voices on deep learning" |
| 62 | Nền móng vẫn là cắt và ghép (hybrid unit selection) (CH06) | OK | AML tiêu đề "Hybrid Unit Selection Synthesis"; "Modern unit selection systems combine some of the benefits of the two approaches … hybrid systems" |
| 63 | Thu 10–20 giờ trong phòng thu chuyên nghiệp; kịch bản từ sách nói, chỉ đường tới câu đùa (CH06) | OK | AML: "we first need to record 10—20 hours of speech in a professional studio"; "The recording scripts vary from audio books to navigation instructions, and from prompted answers to witty jokes" |
| 64 | iOS 11: giọng nữ mới, thu hơn 20 giờ (CH06) | OK | AML: chọn "a new female voice talent", "recorded over 20 hours of speech and built a new TTS voice" |
| 65 | Mạng nơ-ron học sâu đoán hai cái giá (CH06) | OK | AML: deep mixture density network dự đoán phân bố đặc trưng dùng cho target cost và concatenation cost |
| 66 | Nghe thử từng cặp, người nghe rõ ràng thích giọng mới (CH06) | OK | AML: "In an AB pairwise subjective listening tests, listeners clearly preferred the new deep MDN-based voices over the old voices." Lời đọc không nêu số phần trăm (chỉ có trên hình) |
| 67 | Với giọng Siri trong bài 2017, mỗi mảnh âm từng do một người thật nói ra (CH06) | OK (suy ra) | Mục 62–64: unit selection ghép từ bản thu của một người đọc trong phòng thu. Lời đọc giới hạn câu này vào giọng được AML mô tả, không nói về giọng Siri hiện nay |
| 68 | Giọng đọc của video này là giọng tổng hợp (CH06) | OK | Video do hệ thống TTS của kênh đọc (giọng Thanh Bình / Ngọc Huyền) |
| 69 | Dự đoán năm 2013: đặt được giọng mình vào điện thoại, nghe nó nói lại; "Tôi thì quen rồi, nhưng có lẽ bạn thì chưa" (CH06) | MỘT NGUỒN | CNN: "I really see a time when you'll probably be able to put your own voice on your phone and have your own voice talk back to you … Which I'm used to, but maybe you aren't." (trích dịch) |
| 70 | Câu kết: theo bằng chứng CNN gom được, đó là giọng một người thật (CH06) | OK (gắn nguồn) | Mục 9, 20–22 + lời luật sư Steve Sidman và Marcus Graham (GM Voices) trong CNN; lời đọc giữ "theo những bằng chứng CNN gom được" |
| 71 | Callback 1 câu tới video về giọng nói AI (CH06) | OK | Video `mim-ai-voice` của kênh; không kể lại nội dung |

## Không dùng / BỎ

- Giờ chính xác lúc Siri trả lời trên sân khấu: MR không có mốc giờ từng dòng → BỎ, chỉ nói giờ bắt đầu buổi ra mắt.
- Giá Apple mua Siri (các báo ghi 150–250 triệu hoặc ~200 triệu đô la): không có nguồn sơ cấp → BỎ.
- Ngày Apple mua chính xác 28/04/2010: chỉ ICL (thứ cấp) → lời đọc chỉ nói tháng 4/2010 (khớp SRI1).
- Tên người sáng lập Siri Inc. (Kittlaus, Cheyer, Gruber): chỉ thấy qua kết quả tìm kiếm, chưa mở nguồn → BỎ.
- "Tillie the All-Time Teller là máy ATM đầu tiên": CNN không dẫn nguồn → BỎ chữ "đầu tiên".
- Tên Allison Dufty: có trong CNN nhưng không cần cho mạch truyện → không nêu tên trong lời đọc.
- Vai trò của Steve Jobs với Siri: không có nguồn sơ cấp mở được → BỎ; chỉ nêu thông cáo 05/10/2011.
- Khẳng định "tới nay Apple vẫn chưa xác nhận": không có nguồn sau 2018 → lời đọc chỉ nói "từ chối bình luận" (2013).
- Ảnh `File:Susan Bennett (7024710127).jpg` (CC BY-SA 2.0) và `File:Susan Bennett aka Siri and iCups Creator Magdim Metshin.jpg` (CC BY-SA 4.0): MIM không nhận BY-SA → BỎ.
- Ảnh `File:Mourning Steve Jobs.jpg` (CC BY 2.0, Apple Store San Francisco 06/10/2011) và ảnh khuôn viên Infinite Loop: nguy cơ logo Apple trong khung → BỎ.
- `File:Steve Jobs and Macintosh computer, January 1984, by Bernard Gotfryd - edited.jpg` (PD): mặt trước máy Macintosh có huy hiệu táo → BỎ, thay bằng bản "no logo" CC BY 2.0.
- `File:Spectrogram -iua-.png` (CC BY 2.0): trang file không ghi tác giả → BỎ.

## Nguồn không mở được (23/10/2026)

- CNN qua WebFetch: HTTP 451 (đã mở bằng curl, đọc đủ).
- DARPA URL gợi ý `https://www.darpa.mil/research/programs/personalized-assistant-that-learns`: 404; dùng trang Innovation Timeline.
- `http://www.ai.sri.com/project/CALO`: không phân giải được tên miền.
- Edinburgh Research Archive (bản ghi bài Hunt & Black): 403; dùng bản PDF ở Columbia.
- The Drum (2018), CS Monitor (2013), AppleInsider (2013), telecoms.com: 202/403/lỗi kết nối → không dùng để đối chiếu.
- Bài phỏng vấn The Verge / NPR với bà Bennett: không tìm thấy bản mở được → không dùng.

## Nguồn yếu

1. **Gần như mọi chi tiết về Susan Bennett dựa trên MỘT bài CNN (2013)**, cộng VOA (2018) cho câu mẫu và việc Apple không thuê. Apple không xác nhận; chuyên gia pháp y do chính CNN thuê. Lời đọc luôn ghi "theo CNN / theo lời bà".
2. **Giờ 10:00 và câu hỏi thời tiết đầu tiên** chỉ có ghi chép trực tiếp của MacRumors (thứ cấp, không mốc giờ từng dòng).
3. **Ngày ứng dụng Siri lên App Store (04/02/2010)** chỉ có TechCrunch (thứ cấp); Wired ghi "thứ Sáu" (05/02).
4. Bài AML đọc qua WebFetch (bản tóm tắt + câu trích), chưa đọc bằng mắt toàn văn; các câu trích trong lời đọc là câu công cụ trả về nguyên văn.
5. VOA đọc qua WebFetch (curl lỗi kết nối); câu mẫu "cow hoist in the tub today" là câu công cụ trả về nguyên văn — pha 2 nên mở lại bằng trình duyệt.

## Rủi ro hình

- **Thumbnail:** ảnh VOA của bà Bennett (PD, Voice of America, 09/05/2018; có bản cắt dọc) dùng được, là gương mặt người thật CÒN SỐNG: không ghép chữ gán lời bà chưa nói, không ghép logo Apple/Siri, không hình iPhone thật. Đề xuất: mặt bà + cuộn băng (ảnh Tim Reckmann CC BY 2.0) + 0–3 chữ (ví dụ "GIỌNG CỦA AI?"). Phải ghi credit VOA trong mô tả.
- Ảnh Steve Jobs (Matt Buchanan, CC BY 2.0, bản "no logo" 27/01/2010): người đã mất, chỉ dùng một lần ở CH01, nhãn ghi năm 2010 để không gây hiểu nhầm là ảnh buổi ra mắt 2011; pha 2 soi lại xem còn chi tiết thương hiệu nào trong khung.
- Ảnh micro (Shixart1985, CC BY 2.0): pha 2 soi tên hãng trên micro; nếu lộ, cắt khung hoặc thay.
- Ảnh phổ âm "I owe you" (PD) chỉ 436 px: chỉ dùng trong cảnh `print` cỡ nhỏ.
- Không có ảnh SRI/DARPA tự do phù hợp (SRI HQ là CC BY-SA 3.0): CH04 dùng hoàn toàn cảnh chữ/bảng của kênh.
- **Clip Pexels** (mới TÌM, chưa tải): 35451425, 6952886, 6892725, 7643472, 5102361, 12321388 — bắt buộc chạy `motion/long/clip_sheet.py` trước khi dựng; loại clip có logo táo trên máy, tên phần mềm âm thanh, nhãn hiệu trên đầu băng. Clip phụ nữ thu âm / nói điện thoại gắn "VIDEO MINH HỌA" để không bị hiểu là bà Bennett.
- Hai cảnh `chat` (câu hỏi thời tiết, ứng dụng 2010) là khung kênh tự vẽ, nhãn MÔ PHỎNG; không mô phỏng giao diện Siri/iOS.

## Người còn sống được nhắc

- **Susan Bennett**: qua CNN (04/10/2013) và VOA (09/05/2018); mọi lời trích gắn [TRÍCH DỊCH], mọi cảm xúc ("hơi hoảng", "choáng ngợp", "hơi tiếc") là lời bà kể với CNN, gắn DIỄN Ý.
- **Cameron Bennett** (con trai): qua CNN, một chi tiết ("Mẹ, thôi đi!").
- **Ed Primeau** (chuyên gia pháp y âm thanh): qua CNN, kết luận và cách làm.
- **Scott Forstall**: qua ghi chép trực tiếp MacRumors, chỉ việc trình diễn Siri.
- **Allison Dufty**: không nêu tên; chỉ nói "nữ diễn viên lồng tiếng trong video" phủ nhận, qua CNN.
- **Andrew Hunt, Alan Black**: qua bài báo ICASSP-96 của chính họ.
- **Jessica Ravitz** (phóng viên CNN): chỉ nêu tên trên màn hình là tác giả bài báo; vai "đoán ra trước" theo chính bài của bà.

**Kết luận:** 71 dòng: OK 30 (kể cả 1 dòng "OK, hai nguồn") · OK (suy ra) 7 · MỘT NGUỒN 33 (đều đã gắn nguồn trong lời đọc) · MINH HỌA 1. Không còn số liệu nào trong lời đọc thiếu nguồn đã mở.
