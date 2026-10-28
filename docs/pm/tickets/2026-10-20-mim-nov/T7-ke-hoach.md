# T7 — Short gắn Long `mim-may-thang-poker` (lên 26/11 20:00): 4 bài, thiếu 1 so với 5 (bản 1, chờ duyệt)

Người lập: subagent T7, 20/10/2026. Chỉ viết file, không dựng, không đăng, không sửa state.sqlite. Spec: `specs-T7/<slug>.json`.

## 0. Kết luận ngắn

- **Đủ 4 bài, thiếu 1.** MIM đã có **12 Short poker** (08–12/11) phủ gần hết các chương của Long: Libratus 120 nghìn ván, 10^161, hối tiếc, tố bịp bằng toán, vá ba lỗ hổng, Claudico 2015, chia bài đối xứng, Pluribus 150 đô, Pluribus không đọc vị, DeepStack, Cepheus, Noam Brown/OpenAI. Sau khi gạch các góc ấy, còn đúng 4 góc mới có nguồn. Không độn bài thứ 5.
- Chỗ trống 1 bài: có 2 slot còn trống (25/11 11:30, 26/11 19:00), dùng cho Short của ticket khác nếu cần.
- Lô nghiêng nặng về mẫu đã thắng: 3/4 bài là SỰ KIỆN/SỐ (75%), 1/4 là THỬ (25%).

## 1. Lịch (giờ VN, lấy từ `data/shorts_slots.json` slot MIM; `scripts/shorts_grid.py` ngày 20–30/11: 0 Short, 5 slot trống mỗi ngày)

| # | Ngày | Giờ | Slug | Nhãn | Ghi chú |
|---|---|---|---|---|---|
| S1 | T3 24/11 | 11:30 | `mim-von-neumann-poker-1944` | SỰ KIỆN | bài mẫu duyệt trước (dạng ngày + khoảng cách 73 năm) |
| S2 | T3 24/11 | 19:00 | `mim-pluribus-nam-ban-sao` | SỐ | |
| S3 | T4 25/11 | 19:00 | `mim-sandholm-ghep-than` | SỰ KIỆN | |
| S4 | T5 26/11 | 11:30 | `mim-poker-sau-nguoi-het-bao-dam` | THỬ (cơ chế) | sát giờ Long 20:00; trước 20:00 nên không đè |

Không quá 2 Short/ngày; S2 và S4 cùng chủ đề Pluribus/Science 07/2019 nên cách nhau bởi S3. Chuỗi kiểu cảnh (T chữ, M clip, D số liệu, G sơ đồ): S1 M G T D M D M · S2 M G D G T M · S3 M G G T D M · S4 M G D D T M T. Mỗi bài đổi thứ tự so với bài kề, và khác khuôn 12 Short poker cũ (T M G D T G T). Không bài nào dùng khung "mẹo", không câu hỏi cuối, lời đọc không mời xem Long.

## 2. Bốn bài

### S1 — `mim-von-neumann-poker-1944` (SỰ KIỆN)
- **Tiêu đề:** Năm 1944, một nhà toán học dùng poker để hiểu tố bịp; 73 năm sau máy mới ngồi vào bàn
- **Câu mở (8 chữ):** "Một nhà toán học chọn poker năm 1944."
- **Insight duy nhất:** poker vào toán học từ 1944 như bài toán tố bịp theo một tỉ lệ; máy chỉ ngồi vào bàn năm 2017.
- **Số/nguồn:** 1944 và "hơn bảy mươi năm sau" → script CH01 + ghi chú "Khác" (von Neumann – Morgenstern, *Theory of Games and Economic Behavior*, 1944). 01/2017 Libratus thắng bốn cao thủ → CH00/CH09 + CMU News 31/01/2017. **73 năm = 2017 − 1944, kênh tự tính** (ghi trên màn: "KÊNH TỰ TÍNH"). Ý "tố bịp theo một tỉ lệ nhất định" → script CH07 (cách chơi hỗn hợp); **cần kiểm** với sách gốc/bài phân tích poker của von Neumann trước khi dựng (lời đọc chỉ nói "ván poker đơn giản hoá", không nêu con số tỉ lệ).
- **Câu chốt:** "Poker vào toán học năm 1944, và mãi tới năm 2017 máy mới ngồi vào bàn." (quay lại mở 1944)
- **Không trùng:** `mim-to-bip-bang-toan` nói cơ chế tố bịp của Libratus (2017), không nhắc von Neumann/1944; góc ở đây là lịch sử ý tưởng. CH01 chưa có Short nào.

### S2 — `mim-pluribus-nam-ban-sao` (SỐ)
- **Tiêu đề:** Một cao thủ poker đấu năm bản sao của cỗ máy Pluribus: thử nghiệm thứ hai (Science 2019)
- **Câu mở (9 chữ):** "Một cao thủ, năm bản sao của cỗ máy."
- **Insight duy nhất:** ở thử nghiệm thứ hai, mỗi cao thủ ngồi một mình giữa năm bản sao của máy, 5.000 ván, và máy vẫn thắng.
- **Số/nguồn:** 5 bản sao, 5.000 ván mỗi người, Darren Elias (kỷ lục số danh hiệu WPT), Chris Ferguson (sáu giải WSOP) → script CH13 + CMU News tháng 7/2019 (đã đối chiếu: "5,000 hands against five copies of Pluribus"; Elias giữ kỷ lục WPT; Ferguson 6 sự kiện WSOP). "Khoảng cách có ý nghĩa thống kê" → CH13 (script).
- **Câu chốt:** "Một người đấu năm bản sao, và vẫn là máy thắng." (quay lại mở)
- **Không trùng:** `mim-pluribus-150-do` chỉ nói thử nghiệm 1 (năm cao thủ + một Pluribus, 10.000 ván); không bài nào kể thử nghiệm 2 hay tên Elias/Ferguson. **Rủi ro:** cùng nhân vật Pluribus với 2 bài cũ (150-do, khong-doc-vi); khác góc nhưng khán giả có thể thấy gần. Cần kiểm: "có ý nghĩa thống kê" cho riêng thử nghiệm 2 (bài báo Science) vì CMU chỉ nói chung "Pluribus won".

### S3 — `mim-sandholm-ghep-than` (SỰ KIỆN)
- **Tiêu đề:** Người dạy máy poker cũng ghép cặp thận: giáo sư Sandholm và lượt ghép đầu tiên ngày 27/10/2010
- **Câu mở (8 chữ):** "Người dạy máy poker cũng ghép cặp thận."
- **Insight duy nhất:** cùng một nhà nghiên cứu làm Libratus/Pluribus viết thuật toán ghép chéo thận; toán học ra quyết định khi thiếu thông tin có đời sống ngoài bàn bài.
- **Số/nguồn:** Sandholm đồng tác giả Libratus, Pluribus → script CH05/CH13/CH17 + CMU 07/2019. Ghép chéo + "thuật toán của Carnegie Mellon, lời khuyên của Sandholm là phần quan trọng của chương trình thử nghiệm" + **ngày 27/10/2010, 43 người cần thận, 45 người hiến** → ScienceDaily (CMU) 14/12/2010 (đã đọc: "first match run of the OPTN pilot program… computer run Oct. 27 … 43 transplant candidates and 45 donors"). "Bài toán rất khó": script không có; nguồn Sandholm (bài toán xếp chu trình ghép là NP-khó) — lời đọc chỉ nói "rất khó", **cần kiểm** thêm nếu muốn giữ.
- **Câu chốt:** "Người dạy máy cách tố bịp, cũng góp phần ghép đúng người cho quả thận." (quay lại mở)
- **Không trùng:** không Short nào nhắc Sandholm/ghép thận (CH17 chưa dùng). Không nêu số ca cứu sống (không có nguồn). Chủ đề y tế: giữ giọng trung tính, không hứa hẹn.

### S4 — `mim-poker-sau-nguoi-het-bao-dam` (THỬ, cơ chế)
- **Tiêu đề:** Vì sao poker sáu người khó hơn tay đôi: khi toán học hết bảo đảm (Pluribus, Science 2019)
- **Câu mở (9 chữ):** "Sáu người một bàn, toán học hết bảo đảm."
- **Insight duy nhất:** ở bàn hai người máy tính được cách chơi không thua về lâu dài; ở bàn nhiều người cách chơi cân bằng ấy có thể vẫn thua, nên Pluribus phải bỏ bảo đảm lý thuyết.
- **Số/nguồn:** hai người vs sáu người → script CH12. Câu "chơi cân bằng Nash có thể là chiến lược thua ở trò chơi hơn hai người; Pluribus bỏ bảo đảm lý thuyết" → CMU News 07/2019 (đã đọc) + Brown & Sandholm, Science 365 (2019). Pluribus 07/2019 → CH13. Không dùng thuật ngữ "Nash" trong lời đọc.
- **Câu chốt:** "Ở bàn sáu người, bảo đảm của toán học biến mất, chỉ còn bằng chứng từ các ván bài." (quay lại mở)
- **Không trùng:** `mim-pluribus-150-do` nói chi phí và kết quả, không nói vì sao sáu người khó; `mim-pluribus-khong-doc-vi` nói không mô hình hoá đối thủ. Góc "bảo đảm toán học" chưa có. **Rủi ro cao nhất về trùng cảm nhận** (cùng 2019/Pluribus/sáu người), vì vậy đặt nhãn THỬ và cách S2 một bài.

## 3. Bảng đối chiếu trùng

### 3a. Với 12 Short poker MIM đã có (state.sqlite kind='short' channel='MIM': 160 bài; nội dung từ `data/stier/specs/*.json`)

| Short cũ (hẹn) | Góc | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| libratus-120-nghin-van (08/11) | 120.000 ván/20 ngày | khác (S1 chỉ lấy 01/2017 làm mốc cuối) | khác | khác | khác |
| poker-10-mu-161 (09/11) | số tình huống | khác | khác | khác | khác |
| hoc-bang-hoi-tiec (09/11) | thuật toán hối tiếc | khác | khác | khác | khác |
| to-bip-bang-toan (09/11) | tố bịp = tần suất | gần: S1 có một câu "tố bịp đúng tần suất"; góc chính (1944) khác | khác | khác | khác |
| va-3-lo-hong-moi-dem (09/11) | vá lỗ hổng mỗi đêm | khác | khác | khác | khác |
| claudico-thua-2015 (09/11) | lần thua 2015 | khác | khác | khác | khác |
| chia-bai-doi-xung (10/11) | chống may rủi | khác | khác | khác | khác |
| pluribus-150-do (10/11) | chi phí + thử nghiệm 1 | khác | gần (cùng Pluribus; thử nghiệm 2) | khác | gần (cùng sáu người) |
| deepstack-11-nguoi (10/11) | DeepStack | khác | khác | khác | khác |
| cepheus-68-ngay (10/11) | Cepheus | khác | khác | khác | khác |
| noam-brown-nghi-lau-hon (11/11) | từ poker tới chatbot | khác | khác | gần nhẹ (cùng Sandholm/Brown, nhưng ghép thận) | khác |
| pluribus-khong-doc-vi (12/11) | không mô hình hoá đối thủ | khác | khác | khác | gần (cùng Pluribus; góc bảo đảm) |

Các Short khác của MIM (Watson, Deep Blue, AlphaGo, CAPTCHA…): không có Short nào nhắc von Neumann, ghép thận hay "năm bản sao" (đối chiếu slug + tiêu đề 160 bài).

### 3b. Với ticket T4–T9
Ở thời điểm lập, T4–T9 mới có file ticket (chưa có kế hoạch/spec của ticket nào để so từng bài). Rà theo đề tài:
- T9 `mim-may-choi-game`: script có nhắc poker ở dòng liên kết ("máy chơi poker của kênh") và dòng 148; đề nghị T9 **không** dùng Libratus/Pluribus/von Neumann/Sandholm.
- T5 Watson, T4 GPU, T6 chat/privacy, T8 khuôn mặt: không giao đề tài với 4 bài này. T4 có thể nhắc "huấn luyện giá rẻ" (GPU); S2 không dùng góc chi phí (đã bỏ vì 150-do).
- Cần Claude/PM đối chiếu lại khi T4–T9 nộp kế hoạch: từ khoá `Sandholm`, `Pluribus`, `Elias`, `von Neumann`.

## 4. Cần kiểm trước khi dựng

1. **S1:** ý "von Neumann chỉ ra phải tố bịp theo một tỉ lệ nhất định trong ván poker đơn giản hoá" — đối chiếu sách 1944 (hoặc bài viết thứ cấp đáng tin) vì script chỉ có câu chung chung ở CH01. 73 năm là số tự tính.
2. **S2:** "thắng với khoảng cách có ý nghĩa thống kê" cho thử nghiệm 2 (bài báo Science; CMU chỉ nói chung). Nếu không xác nhận được, đổi câu thành "Cỗ máy thắng cả hai." và đổi phụ đề slam.
3. **S3:** (a) "bài toán rất khó" và "nhóm của ông viết thuật toán" nên đối chiếu trang CMU/UNOS; (b) 43 người cần thận/45 người hiến là các số **của lượt chạy đầu tiên**, không phải số ca ghép thành công.
4. **S4:** đối chiếu bài báo Science (Brown & Sandholm 2019) để chắc "ở hơn hai người cân bằng có thể thua" và "Pluribus bỏ qua bảo đảm".
5. **Clip Pexels** (chưa tải, chỉ chọn id từ kết quả tìm, mới đọc tên mô tả): 6219899 (bảng đen), 6813640, 6259147 (đã dùng ở nhiều Short poker cũ, nên đổi nếu có clip khác), 8751436, 7608623 (dùng 2 lần: S2, S4), 6813755, 29671801, 6287762 (phẫu thuật, giữ khung rộng, không cận cảnh). **Chạy `clip_sheet`/soát khung trước khi dựng** (tờ soát chỉ chạy cho Long; với Short soát tay 3 khung): clip không logo, ticker, tên sòng bài/công ty, không thấy mặt bệnh nhân. 6259147 và 7608623 nên thay nếu soát thấy chữ.
6. **Cách đọc `say`:** "Neumann → Nôi-man", "Sandholm → Xan-hôm", "Elias → Ê-li-át", "Ferguson → Phơ-gờ-sần", "Carnegie Mellon → Các-nê-ghi Mê-lần"; nghe thử một lần (S1 và S3 nhiều tên riêng).
7. **S3 130 tiếng** sát trần (≤ 130); nếu TTS đọc quá 38 giây, cắt câu 4.

## 5. Cách đã tự kiểm spec

`build.py` không có cờ `--lint-only` (chỉ `--no-render`/`--draft`, đều chạy TTS và tải ảnh, nên không chạy ở pha 1). Đã tự kiểm bằng script riêng (scratchpad, không đưa vào repo):
- mọi neo `[câu, "chữ", lần]` đều tồn tại trong lời đọc (0 lỗi cứng);
- câu mở ≤ 9 chữ: 8/9/8/9; không câu hỏi cuối; 7 hoặc 6 câu mỗi bài; 100–130 tiếng;
- luật mix (theo `mix_lint`): mỗi bài đủ M, D, G; không 3 cảnh liền cùng kiểu; cảnh thuần chữ ≤ 2/7 số cảnh (thời lượng thật chỉ đo được khi dựng, ước lượng dưới 35%);
- `counter` không có chữ số trong `prefix`; dòng phụ ≤ 52 ký tự;
- chưa kiểm được: thời lượng từng cảnh ≤ 11 s, tương phản/bố cục (chỉ có khi render). Pha 2 chạy `build.py` đầy đủ sẽ bắt các lỗi này.

Chưa ghi gì vào `data/stier/specs`, chưa đụng state.sqlite.
