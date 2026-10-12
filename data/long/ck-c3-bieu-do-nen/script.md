# BIỂU ĐỒ NẾN CHO NGƯỜI MỚI: MỘT CÂY NẾN KỂ GÌ VỀ MỘT PHIÊN, VÀ ĐIỀU NÓ KHÔNG NÓI ĐƯỢC (bản 2, đã kiểm chứng)

**Kênh:** Biểu Đồ Biết Nói (CK) · **Chuỗi:** Chứng khoán từ số 0 — Bài 3 (C3) · **Giọng:** Ngọc Huyền (dẫn) · Phạm Tuyên
(dòng `HỎI:` — câu hỏi của người xem) · Xuân Vĩnh (`»` lời trích, lọc radio)
**Độ dài dự kiến:** ~12 phút (≈2.700 âm tiết đếm theo chữ), 7 chương · **Hồ sơ dữ kiện + nguồn + cách tính:**
[docs/channels/chung-khoan/2026-10-09-long-c3-research.md](../../../docs/channels/chung-khoan/2026-10-09-long-c3-research.md)
(số `[n]` trong Ghi chú = nguồn trong hồ sơ đó) · **Mã tính:** [analysis.py](analysis.py) → `results.json`, `vnindex_1w_2026.csv`
**Tiêu đề:** (1) — chốt theo fact-check (09/10/2026). Phương án đã cân nhắc: (1) *Biểu đồ nến cho người mới: một cây nến kể gì về một phiên, và điều nó
không nói được* · (2) *Nến búa, doji có báo trước giá? Kênh tự đếm 8 năm VN-Index* · (3) *Đọc biểu đồ nến từ số 0: thân, bóng, xanh
đỏ và một tuần VN-Index thật*

Quy ước: mỗi dòng là một câu đọc · `‖` = ngừng dài · `HỎI:` = giọng người hỏi · `»` = lời trích · `**[DIỄN Ý]**` = lời truyền miệng
diễn ý (nhãn DIỄN Ý trên màn hình) · `[TRÍCH DỊCH]` = câu thật dịch sang tiếng Việt.
**Luật cứng (positioning mục 1):** chỉ giáo dục — **không** "nên mua/bán/giữ", **không** tín hiệu giao dịch, không dự báo. Mọi
phép đếm mẫu nến là **đo tần suất trong quá khứ trên chỉ số** (không mua bán trực tiếp được), không tính phí/thuế — ghi trên màn
hình "KÊNH TỰ ĐẾM · QUÁ KHỨ · KHÔNG PHẢI TÍN HIỆU". **Không** nêu tên mẫu nào "hiệu quả" trong lời đọc (xem Ghi chú, mục "kết quả
đẹp"). Không nêu tên mã cổ phiếu, không nêu tên công ty chứng khoán/ứng dụng. Phiên 09–13/03 và 24/03/2026 đã qua hơn 6 tháng (luật
6). Thẻ miễn trừ 4–5 giây đầu video. Mọi cảnh dữ liệu ghi: *"Dữ liệu: HOSE (vnstock/VCI), kênh tự tính. Minh hoạ quá khứ, không
phải khuyến nghị."*

**Giữ chân:** cold open = **cây nến đỏ 09/03/2026** (khán giả C2 đã biết ngày này) phóng to, đọc không cần chữ · **lộ trình dạng
"cảnh hẹn trước"** (RETENTION.md): *"Cuối video, mình sẽ đưa bạn quay lại cây nến thứ Sáu của cùng tuần ấy…"* — không "ba câu hỏi"
(A1, C1), không "thử đoán" (D1), không "bản đồ bằng hình" (C2 — video liền trước), không "nghịch lý" (B1) · **motif** "câu chuyện
đẹp chưa chắc là chuyện thật" (gieo CH01 với giai thoại thương nhân gạo, nhắc CH05 với tên các mẫu nến + "kết quả đẹp", trả ở câu
cuối CH05) + **cây doji 13/03** (gieo CH04 "nhớ mặt nó", trả CH05) · **vòng mở 1** "nhìn nến có đoán được ngày mai?" (mở CH00, đóng
CH05) · **vòng mở 2** "cây nến thứ Sáu" (mở CH00, nhắc CH04, đóng cuối CH05 = cảnh hẹn) · **vòng mở 3** "nến xanh dài là tốt?" (mở
CH02, đóng CH05) · **re-hook ~45%** = cái bẫy màu (CH03, nến đỏ mà chỉ số tăng 24/03) · **cảnh mạnh ~75%** = kênh tự đếm 8 năm (CH05) ·
kết bằng 4 câu tự hỏi + "khi nào không đúng" + câu hỏi bình luận + gợi bài sau.

---

## Kế hoạch hình ảnh

Màu: nến tăng `#22c55e` · nến giảm `#ef4444` (màu sẵn của cảnh `candles`) · VN-Index `#38bdf8` · nhấn `#fbbf24` · **bảng giá: tăng
xanh lá, giảm đỏ, tham chiếu vàng, trần tím `#c084fc`, sàn xanh lơ `#22d3ee`** (như C2). Cảnh có sẵn (theme "chart"): chapter, kinetic,
slam, question, counter, bars (chỉ giá trị dương), ledger, timeline, date, quote, broll (Pexels), **candles**, race, breadth, basket,
book, brand.

**Tuỳ chọn của `candles`** (đã đọc `motion/hf/assets/engine/chart.js` + `motion/long/chartdata.py`): `series` ("vnindex"), `from`,
`to`, `ind` ([{k: "sma"|"ema", n}] → đường chỉ báo, **không dùng** trong bài này), `title`, `range`, `drawAt`, `until` (nến hiện dần
trái → phải), `marks` [{`date`, `text`, `at`, `pos`: above|below, `tone`: up|down|gold, `dx`, `dy`}] (vòng tròn + nhãn), `source`.
Màu nến = **đóng cửa so với mở cửa** (`b[4] >= b[1]` → xanh) — đúng nội dung CH03. Độ rộng thân = 64% khe → cửa sổ **1–5 phiên** cho
ra nến **rất to** (dùng làm cảnh "giải phẫu" thay cảnh `anatomy` chưa có). Không có khung tuần, không có tô nền một cây nến ngoài
`marks`.

**CH00 · Một cây nến đỏ**
- `candles` **một phiên** `from/to` "2026-03-09" (một cây nến chiếm gần hết màn hình), title "VN-INDEX · 09/03/2026", **không** nhãn
  lúc đầu; marks lần lượt theo lời: "MỞ CỬA = CAO NHẤT · 1.757,73" (above, gold) · "ĐÓNG CỬA 1.652,79 · CÁCH ĐÁY ≈ 2 ĐIỂM" (below,
  down).
- `date` "09/03/2026" day "THỨ HAI" sub "−115,05 ĐIỂM · BÀI 2" (gọi lại C2).
- `quote` **DIỄN Ý** (nhãn "LỜI TRUYỀN MIỆNG · DIỄN Ý", `radio: true`): "Thấy cây búa là đáy đã tới…".
- `question` "Nhìn nến, có đoán được ngày mai?"
- `candles` 2026-03-09 → 2026-03-13 (5 nến), mark 13/03 "THỨ SÁU · ?" (gold) — **cảnh hẹn** → `brand` "TIỀN BẠC · GIẢI THÍCH
  BẰNG DỮ LIỆU" + thẻ "CHỨNG KHOÁN TỪ SỐ 0 · BÀI 3".

**CH01 · Bốn con số làm nên một cây nến**
- `chapter` → `timeline` đồng hồ phiên C2 (9:00 → 15:00) thu gọn, 4 mốc sáng vàng: "MỞ CỬA" · "CAO NHẤT" · "THẤP NHẤT" · "ĐÓNG CỬA".
- `broll` nhiệt kế / cửa sổ buổi sáng (Pexels "thermometer window morning") → `ledger` "NHIỆT ĐỘ MỘT NGÀY · VÍ DỤ GIẢ ĐỊNH": SÁNG 27° ·
  NÓNG NHẤT 35° · MÁT NHẤT 26° · TỐI 29° (nhãn "VÍ DỤ GIẢ ĐỊNH").
- `kinetic` "BIỂU ĐỒ ĐƯỜNG = CHỈ NỐI GIÁ ĐÓNG CỬA" (tuỳ chọn: `race` một đường VN-Index 03/2026 làm ví dụ đường).
- `candles` **3 phiên** 2026-03-09 → 2026-03-11 (nến to): marks "THÂN = MỞ CỬA → ĐÓNG CỬA" (gold, trên nến 11/03) · "BÓNG TRÊN →
  CAO NHẤT" (above, 10/03) · "BÓNG DƯỚI → THẤP NHẤT" (below, 10/03). Chữ góc "O · H · L · C".
- `kinetic` "1 CÂY NẾN = 1 PHIÊN".
- `question` "Sao lại gọi là nến?" → `broll` cây nến thật (Pexels "candle flame dark") — "ẢNH MINH HOẠ".
- `ledger` "CHUYỆN KỂ vs NGUỒN" (**không** gạch ngang): "CHUYỆN KỂ: THƯƠNG NHÂN GẠO, THẾ KỶ 18" · "STEVE NISON (1991) PHỔ BIẾN NẾN
  Ở PHƯƠNG TÂY" · "NISON (1994): KHÓ CÓ CHUYỆN THƯƠNG NHÂN ẤY DÙNG NẾN · NHIỀU KHẢ NĂNG RA ĐỜI ĐẦU THỜI MINH TRỊ, CUỐI THẾ KỶ 19".
  Nguồn trên màn: Nison, *Beyond Candlesticks* (1994), qua Wikipedia.
- `slam` "CHUYỆN ĐẸP CHƯA CHẮC LÀ CHUYỆN THẬT" (nhỏ) — gieo motif.

**CH02 · Thân và bóng: phiên ấy ai thắng**
- `chapter` → `kinetic` hai câu hỏi: "1 · THÂN DÀI HAY NGẮN?" · "2 · BÓNG DÀI Ở PHÍA NÀO?".
- `kinetic` "BÓNG = CHỖ MỘT BÊN ĐÃ KÉO TỚI, RỒI BỊ KÉO VỀ" (hình kéo co tối giản bằng chữ: "BÊN MUA ⟷ BÊN BÁN").
- `candles` 2026-03-09 → 2026-03-11, marks: 10/03 "VỌT LÊN ≈ 1.717 · ĐÓNG 1.676,73" (above, gold) + "ĐỈNH − ĐÓNG CỬA ≈ 40 ĐIỂM" ·
  11/03 "+3,08% · MỞ ≈ ĐÁY, ĐÓNG ≈ ĐỈNH" (above, up). Nguồn nhỏ: "Thời báo Tài chính, VnExpress 10/03/2026: đầu phiên +63 điểm, lên
  vùng 1.715–1.720". Chữ góc nhỏ: "Giá mở 10/03 khác nhau giữa các nguồn dữ liệu".
- `question` "Nến xanh dài là tốt?" → `slam` "NẾN KỂ PHIÊN ĐÃ QUA" sub "KHÔNG HỨA PHIÊN SAU".

**CH03 · Xanh, đỏ, và cái bẫy màu**
- `chapter` → `ledger` hai cột: "MÀU NẾN: ĐÓNG CỬA so với MỞ CỬA" · "MÀU BẢNG GIÁ: GIÁ so với THAM CHIẾU (ĐÓNG CỬA HÔM TRƯỚC)".
- `candles` 2026-03-19 → 2026-03-27, marks: 23/03 "1.591,17 · ĐÓNG CỬA THẤP NHẤT 2026 (TỚI 06/10)" (below, down) · 24/03 "NẾN ĐỎ ·
  CHỈ SỐ +1,48%" (above, gold).
- `ledger` "24/03/2026": THAM CHIẾU 1.591,17 (vàng) · MỞ CỬA ≈ 1.626 · ĐÓNG CỬA 1.614,77 · SO HÔM TRƯỚC +23,60 (xanh) · SO MỞ CỬA
  ≈ −11,6 (đỏ). Nguồn: "Thời báo Tài chính, Người Lao Động, Vietnambiz 24/03/2026 (đóng cửa +23,60; đầu phiên tăng hơn 30 điểm) · giá mở:
  dữ liệu HOSE qua vnstock/VCI".
- `question` "Ngày tốt hay ngày xấu?" → `slam` "HAI MÀU · HAI CÂU HỎI".
- `counter` 0 → 15 suffix "%" label "PHIÊN CÓ MÀU NẾN NGƯỢC MÀU BẢNG GIÁ" sub "≈ 1 PHIÊN / 6–7 PHIÊN · VN-INDEX 10/2018–10/2026 · KÊNH TỰ ĐẾM (NGUỒN DỮ LIỆU KHÁC: 16%)".
- `kinetic` "XEM CHÚ THÍCH MÀU CỦA CHÍNH BIỂU ĐỒ" + 3 kiểu nhỏ: "XANH/ĐỎ · RỖNG/ĐẶC · MÀU KHÁC".

**CH04 · Đọc một tuần, rồi gộp thành một cây**
- `chapter` → `candles` 2026-03-09 → 2026-03-13 (5 nến to), `drawAt` từng nến theo từng câu (hoặc 5 cảnh nối tiếp, mỗi cảnh thêm 1
  mark): T2 "BÊN BÁN THẮNG TRỌN PHIÊN" (down) · T3 "BỊ ĐẨY LÙI TỪ TRÊN CAO" (gold) · T4 "BÊN MUA GIỮ TỚI CUỐI" (up) · T5 "MỞ THẤP HƠN
  HÔM TRƯỚC · −1,08%" (down) · T6 "DOJI · THÂN 1,48 / BIÊN 28 ĐIỂM" (gold).
- `slam` "DOJI" sub "NHỚ MẶT NÓ".
- **`candles` khung tuần (MỞ RỘNG đề xuất, xem cuối mục)**: một cây nến tuần 09–13/03 cạnh 5 nến ngày: O 1.757,73 · H 1.757,73 · L
  1.650,75 · C 1.696,24 · "−4,05% SO VỚI TUẦN TRƯỚC". *(Dự phòng: `ledger` "NẾN TUẦN 09–13/03" bốn dòng O/H/L/C + `kinetic` "THÂN ĐỎ ·
  BÓNG DƯỚI DÀI".)*
- `bars` "VN-INDEX TỪ 01/01 TỚI 06/10/2026": NẾN NGÀY 186 · NẾN TUẦN 39.
- `question` "Khung nào mới đúng?" → `kinetic` "KHUNG NHỎ: NHIỀU CHI TIẾT, NHIỀU NHIỄU · KHUNG LỚN: GỌN, CHẬM" → `slam` "NẾN NGÀY HAY NẾN
  TUẦN?".

**CH05 · Điều cây nến không nói được**
- `chapter` → `ledger` "BA MẪU NẾN QUEN TÊN" (mỗi dòng hình chữ + lời truyền miệng, nhãn DIỄN Ý): CÂY BÚA — "BÁO ĐÁY" · DOJI — "SẮP ĐẢO
  CHIỀU" · BA CHÀNG LÍNH TRẮNG — "SÓNG TĂNG BẮT ĐẦU". Ví dụ hình thật: `candles` 2026-06-03 → 2026-06-12 mark 09/06 "CÂY BÚA" (gold).
- `kinetic` "KÊNH TỰ ĐẾM · VN-INDEX 08/10/2018 → 06/10/2026 · 1.995 PHIÊN · QUÁ KHỨ · KHÔNG PHẢI TÍN HIỆU".
- `counter` 0 → 59 suffix "%" label "NGÀY BẤT KỲ → 20 PHIÊN SAU CHỈ SỐ CAO HƠN" sub "MỐC SO SÁNH · KHÔNG PHẢI 50%" → `candles` toàn bộ
  2018-10-08 → 2026-10-06 (chỉ để thấy chiều đi lên, marks đầu/cuối "996" · "1.759").
- `question` "Thế cây búa thì sao?" → `bars` "SAU 5 PHIÊN, CHỈ SỐ CAO HƠN (% SỐ LẦN)": MỌI NGÀY VỪA GIẢM (5 PHIÊN TRƯỚC) 56,3 ·
  **CÂY BÚA (35 LẦN) 51,4** (sub: "SAU 20 PHIÊN: CŨNG KHÔNG HƠN MỐC · 35 LẦN LÀ ÍT").
- `bars` "SAU 5 PHIÊN, CHỈ SỐ ĐỔI CHIỀU (% SỐ LẦN)": NGÀY THƯỜNG 45,0 · **SAU DOJI (201 LẦN) 42,8**.
- `kinetic` "BA CHÀNG LÍNH TRẮNG ĐÚNG SÁCH · CHỈ VÀI LẦN TRONG 8 NĂM · 0 LẦN TỪ 2023 · QUÁ ÍT ĐỂ KẾT LUẬN".
- `kinetic` "HƠN 20 PHÉP SO · KHÔNG KẾT QUẢ NÀO ĐỨNG VỮNG KHI TÍNH ĐỦ SỐ PHÉP THỬ · CHƯA TRỪ PHÍ" → `kinetic` đồng xu "5 MẶT NGỬA
  LIỀN" (minh hoạ chữ).
- `ledger` "CÁC NGHIÊN CỨU": MỸ · CỔ PHIẾU DOW JONES 1992–2002 · KHÔNG GIÁ TRỊ (Marshall, Young & Rose, J. Banking & Finance 2006) · NHẬT ·
  1975–2004 · KHÔNG LỢI NHUẬN (Marshall, Young & Cahan 2008) · THÁI LAN · SET50 2006–2016 · ĐA SỐ KHÔNG KHÁC 0 (Tharavanij & cs., SAGE Open
  2017) · VIỆT NAM · 2013–2018 · KHÔNG DỰ BÁO ĐƯỢC XU HƯỚNG (Ngô Tùng Sơn & cs., IMMS 2018) · MỸ (S&P 500 1992–96), ĐÀI LOAN, TRUNG
  QUỐC · VÀI MẪU CÓ ÍCH TRONG VÀI ĐIỀU KIỆN (Caginalp & Laurent 1998; Lu 2014; Zhu & cs. 2016).
- `quote` **TRÍCH DỊCH** (`radio: true`): "Phân tích kỹ thuật bằng nến không có giá trị." — nguồn trên màn: B. Marshall, luận án Massey
  University (2005), cơ sở của bài J. Banking & Finance 2006.
- **Cảnh hẹn** `candles` 2026-03-02 → 2026-04-14, marks: 13/03 "DOJI" (gold) · 20/03 "5 PHIÊN SAU: −2,9%" (below, down) · 23/03 "THẤP
  NHẤT NĂM (ĐÓNG CỬA)" (below, down) · 10/04 "20 PHIÊN SAU: +3,2%" (above, up).
- `slam` "KỂ SAU KHI BIẾT KẾT THÚC" sub "CHUYỆN ĐẸP CHƯA CHẮC LÀ CHUYỆN THẬT".

**CH06 · Áp dụng cho bạn, và khi nào không đúng**
- `chapter` → `ledger` "4 CÂU KHI NHÌN MỘT CÂY NẾN" (hiện theo lời).
- `ledger` "KHI NÀO KHÔNG ĐÚNG" (4 thẻ): CHỈ ĐẾM TRÊN VN-INDEX, 8 NĂM, KHÔNG PHÍ · CỔ PHIẾU ÍT GIAO DỊCH: NẾN = VÀI LỆNH · GIÁ MỞ CỬA =
  GIÁ KHỚP ATO (BÀI 2) · GIÁ CŨ BỊ ĐIỀU CHỈNH SAU CỔ TỨC / THƯỞNG.
- `candles` 2026-03-09 (một nến to, như cold open) → `slam` "KỂ GIỎI CHUYỆN ĐÃ QUA" sub "KHÔNG HỨA CHUYỆN SẼ TỚI".
- `kinetic` gợi bài sau: "NHỮNG BÀI TỚI · NỐI CÁC CÂY NẾN: XU HƯỚNG, RỒI ĐƯỜNG TRUNG BÌNH ĐỘNG MA" (+ `candles` có `ind` [{k:"sma", n:20}] làm
  teaser 2 giây).
- `question` câu hỏi bình luận.

**Mở rộng đề xuất** (chưa có trong engine — có dự phòng; không sửa engine khi có render, retro 2 luật PM 3):
1. **`candles` khung tuần**: thêm khoá `tf: "1w"` cho `chartdata.attach` — gộp phiên theo tuần (T2→T6: mở = mở phiên đầu, cao/thấp =
   max/min, đóng = đóng phiên cuối, KL = tổng) **trong Python**, engine không đổi (nhãn trục "T3/2026" vẫn đúng). Dữ liệu tuần 2026 đã
   có sẵn ở `data/long/ck-c3-bieu-do-nen/vnindex_1w_2026.csv` (analysis.py ghi) để đối chiếu. *(Dự phòng: `ledger`.)*
2. **Nhãn tuỳ chọn trên trục giá cho một nến** (O/H/L/C ở mép phải) — *không bắt buộc*: `marks` 2 nhãn (above/below) là đủ cho CH00/CH01.

---

## CH00 · Một cây nến đỏ

Nhìn cây nến đỏ rất dài này.
Nó không có một chữ nào, không có một con số nào.
Nhưng nếu biết đọc, bạn sẽ thấy cả một ngày giao dịch nằm trong đó. ‖
Bạn biết ngày này rồi: thứ Hai, chín tháng ba năm nay, ngày VN-Index mất một trăm mười lăm điểm.
Cây nến kể rằng hôm ấy chỉ số mở cửa ở đúng mức cao nhất của ngày.
Sau đó nó gần như chỉ đi xuống, và đóng cửa chỉ cách đáy của phiên khoảng hai điểm.
Suốt phiên, chưa lúc nào chỉ số lên được cao hơn giá mở cửa. ‖
Đó là việc một cây nến làm rất giỏi: kể lại một phiên đã qua, gọn trong một hình.
Nhưng trên mạng, người ta hay hứa với bạn nhiều hơn thế:
**[DIỄN Ý]** » Thấy cây búa là đáy đã tới, thấy ba chàng lính trắng là sóng tăng bắt đầu.
HỎI: Vậy nhìn nến, mình có đoán được ngày mai không?
Đó chính là điều video này sẽ đi tìm, bằng dữ liệu thật. ‖
Cuối video, mình sẽ đưa bạn quay lại cây nến thứ Sáu của cùng tuần ấy, một cây nến mà sách gọi là dấu hiệu lưỡng lự.
Lúc đó bạn sẽ tự đọc được nó, và sẽ thấy tám năm dữ liệu VN-Index nói gì về những lời hứa kia.
Đây là Biểu Đồ Biết Nói. Tiền bạc, giải thích bằng dữ liệu.
Và đây là bài ba của khoá Chứng khoán từ số không.
Video chỉ nhằm giáo dục, không phải lời khuyên mua hay bán, và không dự báo thị trường.

## CH01 · Bốn con số làm nên một cây nến

Ở bài hai, mình đã đi hết một phiên HOSE, từ chín giờ sáng tới ba giờ chiều.
Nếu chỉ được giữ lại bốn con số của cả phiên ấy, bạn sẽ giữ những số nào?
Người vẽ biểu đồ chọn giá mở cửa, giá cao nhất, giá thấp nhất, và giá đóng cửa. ‖
Hãy nghĩ tới nhiệt độ một ngày ở nhà bạn.
Sáng mở cửa ra là bao nhiêu độ, lúc nóng nhất bao nhiêu, lúc mát nhất bao nhiêu, và tối về còn bao nhiêu.
Nếu chỉ ghi nhiệt độ buổi tối, bạn biết ngày hôm ấy kết thúc ra sao, nhưng không biết nó đã trải qua những gì.
Biểu đồ đường bạn hay thấy trên báo giống như vậy: nó thường chỉ nối các giá đóng cửa với nhau. ‖
Cây nến thì giữ đủ cả bốn con số.
Phần thân là đoạn từ giá mở cửa tới giá đóng cửa.
Hai sợi mảnh ở trên và dưới gọi là bóng nến, hay râu nến, kéo tới giá cao nhất và giá thấp nhất của phiên.
Vậy một cây nến là một phiên.
Biểu đồ nến ngày là nhiều phiên như thế đặt cạnh nhau, từ trái sang phải. ‖
HỎI: Mà sao lại gọi là nến?
Vì phần thân trông như thân cây nến, còn bóng phía trên giống sợi bấc.
Cách vẽ này đến từ Nhật Bản, và đi kèm một câu chuyện rất hay.
Người ta kể rằng một thương nhân buôn gạo người Nhật ở thế kỷ mười tám đã nghĩ ra nó.
Người làm cho biểu đồ nến trở nên phổ biến ở phương Tây là Steve Nison, qua một cuốn sách năm một nghìn chín trăm chín mươi mốt.
Vài năm sau, chính ông viết rằng, theo tìm hiểu của ông, nhiều khả năng thương nhân ấy chưa từng dùng biểu đồ nến.
Theo ông, nến nhiều khả năng ra đời muộn hơn, vào cuối thế kỷ mười chín. ‖
Một câu chuyện đẹp chưa chắc là chuyện thật. Giữ ý ấy trong đầu nhé, lát nữa nó sẽ quay lại.

## CH02 · Thân và bóng: phiên ấy ai thắng

Đọc một cây nến, bạn chỉ cần hỏi hai câu.
Câu thứ nhất: thân dài hay ngắn?
Thân dài nghĩa là từ lúc mở cửa tới lúc đóng cửa, giá đã đi được một quãng xa theo một hướng.
Thân rất ngắn nghĩa là hết phiên, giá gần như quay về chỗ bắt đầu. ‖
Câu thứ hai: bóng dài ở phía nào?
Bóng trên dài nghĩa là trong phiên, giá đã lên khá cao, nhưng không giữ được tới lúc đóng cửa.
Bóng dưới dài thì ngược lại: giá đã xuống khá sâu, rồi được kéo lên trở lại.
Người ta hay ví bên mua và bên bán như hai đội kéo co.
Bóng nến là chỗ một bên đã kéo tới, rồi bị kéo về. ‖
Thử với hai ngày ngay sau cây nến đỏ hôm thứ Hai.
Thứ Ba, mười tháng ba, chỉ số hồi lại sau cú giảm hôm thứ Hai.
Đầu phiên, nó vọt lên gần một nghìn bảy trăm hai mươi. Báo chí hôm ấy cũng ghi như vậy.
Nhưng tới lúc đóng cửa, chỉ số chỉ còn khoảng một nghìn sáu trăm bảy mươi bảy.
Nhìn cây nến hôm ấy, phần phía trên rất dài: lúc đóng cửa, chỉ số đã thấp hơn đỉnh trong phiên gần bốn mươi điểm.
Nó kể rằng bên mua đã kéo giá lên rất cao, nhưng rồi bị đẩy lùi một đoạn dài. ‖
Thứ Tư, mười một tháng ba, là một cây nến xanh dài, gần như không có bóng.
Chỉ số mở cửa gần đáy, đóng cửa gần đỉnh của phiên, tăng khoảng ba phần trăm.
Cả phiên ấy, bên bán gần như không kéo lại được chút nào.
HỎI: Vậy nến xanh dài là tốt, nến đỏ dài là xấu à?
Cây nến chỉ cho biết phiên ấy đã diễn ra thế nào.
Còn phiên sau có đi tiếp theo hướng ấy không, đó là một câu hỏi khác. Lát nữa mình sẽ đếm thử.

## CH03 · Xanh, đỏ, và cái bẫy màu

Giờ tới màu sắc, chỗ người mới hay nhầm nhất.
Trên hầu hết biểu đồ nến ở Việt Nam, nến xanh là phiên đóng cửa cao hơn mở cửa.
Nến đỏ là phiên đóng cửa thấp hơn mở cửa.
Còn ở bài hai, bạn đã thấy bảng giá tô màu theo một cách khác.
Trên bảng giá, xanh nghĩa là cao hơn giá tham chiếu, tức giá đóng cửa của phiên hôm trước. Đỏ là thấp hơn.
Hai thứ màu này so với hai cái mốc khác nhau. ‖
Nên có những ngày chỉ số tăng, bảng giá xanh, mà cây nến lại đỏ.
Thứ Ba, hai mươi bốn tháng ba, là một ngày như vậy.
Hôm trước, chỉ số vừa đóng cửa ở mức thấp nhất của năm nay, khoảng một nghìn năm trăm chín mươi mốt điểm.
Sáng thứ Ba, chỉ số mở cửa cao vọt, quanh một nghìn sáu trăm hai mươi sáu.
Rồi nó không giữ được mức ấy, và đóng cửa ở khoảng một nghìn sáu trăm mười lăm.
So với hôm trước, chỉ số tăng gần một phẩy năm phần trăm. Bảng giá xanh.
So với lúc mở cửa, nó thấp hơn. Cây nến đỏ. ‖
HỎI: Thế rốt cuộc hôm đó là ngày tăng hay ngày giảm?
Cả hai màu đều đúng. Chúng chỉ trả lời hai câu hỏi khác nhau.
Màu nến hỏi: trong phiên, giá đi lên hay đi xuống? Màu bảng giá hỏi: so với hôm qua, giá cao hơn hay thấp hơn?
Kênh tự đếm trên tám năm dữ liệu VN-Index: cứ sáu, bảy phiên lại có một phiên hai màu này ngược nhau.
Có biểu đồ còn vẽ nến tăng rỗng ruột, nến giảm tô đặc, hoặc dùng màu khác hẳn.
Nên trước khi đọc, hãy liếc qua chú thích màu của chính biểu đồ ấy.

## CH04 · Đọc một tuần, rồi gộp thành một cây

Giờ bạn đã có đủ đồ nghề để đọc nguyên một tuần.
Tuần từ chín tới mười ba tháng ba: năm cây nến, năm câu chuyện.
Thứ Hai: nến đỏ dài, gần như không bóng. Bên bán thắng trọn phiên.
Thứ Ba: bóng trên dài. Bên mua kéo giá lên cao, nhưng bị đẩy lùi một đoạn dài.
Thứ Tư: nến xanh dài. Lần này, bên mua giữ được tới cuối.
Thứ Năm: chỉ số mở cửa thấp hơn giá đóng cửa hôm trước, rồi giảm thêm, thành một cây nến đỏ nhỏ.
Thứ Sáu, mười ba tháng ba: một cây nến gần như không có thân.
Giá mở cửa và giá đóng cửa cách nhau chưa tới hai điểm, dù trong phiên chỉ số đã đi lên đi xuống gần ba mươi điểm.
Cây nến kiểu này có tên riêng: doji. Hãy nhớ mặt nó, cuối video mình sẽ quay lại. ‖
Giờ thử một việc: gộp cả năm phiên thành một cây nến duy nhất.
Mở cửa là giá mở cửa sáng thứ Hai. Đóng cửa là giá đóng cửa chiều thứ Sáu.
Cao nhất và thấp nhất là đỉnh và đáy của cả tuần.
Ta được một cây nến tuần: thân đỏ, và một cái bóng dưới khá dài.
Nó kể rằng cả tuần, chỉ số giảm khoảng bốn phần trăm, nhưng đã lấy lại được một đoạn từ đáy hôm thứ Hai.
Cùng một tuần ấy, năm cây nến ngày cho thấy một cuộc giằng co. Một cây nến tuần cho thấy một tuần giảm, có hồi lại. ‖
Đó là thứ người ta gọi là khung thời gian.
Nến ngày thì mỗi cây là một phiên. Nến tuần thì mỗi cây là một tuần.
Còn có nến tháng, hay nến chỉ dài một giờ, năm phút.
Từ đầu năm nay tới đầu tháng mười, VN-Index có một trăm tám mươi sáu cây nến ngày, nhưng chỉ khoảng ba mươi chín cây nến tuần.
HỎI: Vậy xem khung nào mới đúng?
Không có khung nào đúng hơn khung nào.
Khung nhỏ cho thấy nhiều chi tiết, và cũng nhiều nhiễu. Khung lớn gọn hơn, nhưng phản ứng chậm hơn.
Nên khi ai đó chỉ cho bạn một cây nến, câu đầu tiên hãy hỏi: nến ngày, hay nến tuần?

## CH05 · Điều cây nến không nói được

Giờ tới những lời hứa ở đầu video.
Sách và mạng xã hội đặt tên cho hàng chục hình dạng nến.
Ba cái tên người mới hay gặp nhất là cây búa, doji, và ba chàng lính trắng.
Cây búa là nến có thân nhỏ nằm trên cao, bóng dưới dài ít nhất gấp đôi thân, mọc ra sau mấy phiên giảm.
Người ta nói nó báo hiệu đáy.
Doji, như cây nến thứ Sáu, được gọi là dấu hiệu lưỡng lự, sắp đảo chiều.
Ba chàng lính trắng là ba nến xanh dài nối nhau sau một đợt giảm, được coi là sóng tăng bắt đầu. ‖
Kênh đã thử đếm trên VN-Index, từ tháng mười năm hai nghìn không trăm mười tám tới đầu tháng mười năm nay.
Nhưng trước hết, phải có một cái mốc để so.
Chọn bừa một ngày bất kỳ trong tám năm ấy, rồi nhìn năm phiên sau, hay hai mươi phiên sau.
Khoảng sáu trên mười lần, chỉ số cao hơn.
Vì trong tám năm, VN-Index đã đi từ khoảng một nghìn lên khoảng một nghìn bảy trăm sáu mươi điểm.
Nên một mẫu nến muốn chứng tỏ nó báo tăng, phải thắng được con số sáu trên mười ấy, chứ không phải năm mươi phần trăm. ‖
HỎI: Thế cây búa thì sao?
Cây búa đúng sách xuất hiện ba mươi lăm lần trong tám năm.
Năm phiên sau, chỉ số cao hơn ở khoảng năm mươi mốt phần trăm số lần.
Còn với mọi ngày mà năm phiên trước đó chỉ số cũng đi xuống, con số ấy là năm mươi sáu phần trăm.
Đo sau hai mươi phiên, cây búa cũng không hơn mốc. Ba mươi lăm lần là ít, nên chênh lệch nhỏ như vậy, theo chiều nào cũng chưa nói lên điều gì. ‖
Doji xuất hiện khoảng hai trăm lần.
Nếu doji báo đảo chiều, thì sau nó, chỉ số phải hay đổi hướng hơn bình thường.
Thực tế, sau doji, chỉ số đổi hướng khoảng bốn mươi ba phần trăm số lần. Ngày thường là bốn mươi lăm.
Còn ba chàng lính trắng đúng sách thì quá hiếm: chỉ vài lần trong tám năm, và chưa lần nào từ năm hai nghìn không trăm hai mươi ba.
Vài lần thì không đủ để kết luận điều gì, kể cả điều tốt. ‖
Công bằng mà nói, kênh đã chạy hơn hai mươi phép so, và có vài kết quả thoạt nhìn trông đẹp hơn mốc.
Nhưng không kết quả nào còn đứng vững sau khi tính tới việc thử nhiều mẫu cùng lúc, và đó là khi còn chưa trừ phí.
Chạy đủ nhiều phép thử, kiểu gì cũng gặp vài kết quả đẹp, như tung đồng xu đủ lâu thì sẽ có lúc ra năm mặt ngửa liền.
Cách kênh đếm, mình tóm tắt ở phần mô tả để bạn tự kiểm lại. ‖
HỎI: Thế các nhà nghiên cứu thì nói sao?
Nhóm của Ben Marshall ở New Zealand đã thử hàng chục mẫu nến trên các cổ phiếu thuộc chỉ số Dow Jones của Mỹ, với khoảng mười năm dữ liệu.
Trong luận án tiến sĩ làm nền cho nghiên cứu ấy, Marshall kết luận rất ngắn:
[TRÍCH DỊCH] » Phân tích kỹ thuật bằng nến không có giá trị.
Cùng nhóm ấy thử ở Nhật, quê hương của nến, với ba mươi năm dữ liệu, và cũng không thấy lợi nhuận.
Ở Thái Lan, phần lớn các mẫu nến trên năm mươi cổ phiếu lớn cho lợi nhuận không khác số không.
Ở Việt Nam, một nhóm tác giả ở Hà Nội cũng không thấy các mẫu nến đảo chiều dự báo được xu hướng.
Cũng có nghiên cứu ở Mỹ, Đài Loan và Trung Quốc thấy vài mẫu có ích, có nơi kể cả sau khi trừ phí.
Nhưng thường chỉ là vài mẫu, ở vài loại cổ phiếu, trong vài giai đoạn.
Nên câu trả lời trung thực là: nếu nến có báo trước được điều gì, thì tín hiệu ấy rất mờ, và không ổn định. ‖
Giờ là cảnh mình đã hẹn: cây doji thứ Sáu, mười ba tháng ba.
Năm phiên sau, chỉ số thấp hơn gần ba phần trăm.
Thêm một phiên nữa, ngày hai mươi ba tháng ba, chỉ số đóng cửa ở mức thấp nhất của năm.
Nhưng hai mươi phiên sau cây doji ấy, chỉ số lại cao hơn khoảng ba phần trăm.
Ai muốn nói cây nến ấy báo giảm hay báo tăng, nhìn lại đều tìm được bằng chứng.
Một câu chuyện kể sau khi đã biết kết thúc, nghe đẹp đến mấy, vẫn chưa chắc là chuyện thật.

## CH06 · Áp dụng cho bạn, và khi nào không đúng

Mình không bảo bạn bỏ qua biểu đồ nến. Nó là cách gọn nhất để xem lại một phiên, một tuần.
Chỉ có bốn câu, để bạn tự hỏi mỗi khi nhìn một cây nến.
Một: đây là nến ngày, nến tuần, hay một khung nào khác?
Hai: màu này so với giá mở cửa, hay so với giá tham chiếu?
Ba: thân dài hay ngắn, bóng dài ở phía nào, và nó kể gì về phiên đã qua?
Bốn: mình đang đọc lại quá khứ, hay đang cố đoán ngày mai?
Nếu là đoán, hãy hỏi tiếp: đã có ai đếm xem cách đoán ấy đúng bao nhiêu lần, so với một ngày bất kỳ chưa? ‖
Và đây là những lúc điều vừa nói không đúng hoàn toàn.
Phép đếm của kênh chỉ làm trên VN-Index, trong tám năm, chưa tính phí. Một cổ phiếu riêng lẻ, hay một giai đoạn khác, có thể cho kết quả khác.
Với cổ phiếu ít người giao dịch, một cây nến có khi chỉ là vài lệnh nhỏ, nên hình dạng của nó nói rất ít.
Giá mở cửa của một cổ phiếu là giá khớp trong phiên mở cửa, như bài hai đã kể, nên có thể cách xa giá đóng cửa hôm trước.
Và nhiều ứng dụng tự điều chỉnh giá cũ sau khi công ty chia cổ tức hay thưởng cổ phiếu.
Nên cây nến năm xưa trên màn hình có thể khác con số bạn còn nhớ. ‖
Tóm lại, một cây nến là bốn con số của một phiên, vẽ thành một hình.
Nó kể rất giỏi chuyện đã xảy ra: ai thắng, giằng co ra sao, đã đi xa tới đâu.
Nhưng nó không hứa được chuyện sẽ xảy ra.
Ở những bài tới, mình sẽ nối nhiều cây nến lại với nhau để xem xu hướng, rồi làm quen với đường trung bình động.
Còn bây giờ, mình muốn nghe bạn: mẫu nến nào bạn từng được nghe là chắc ăn nhất? Biết đâu, nó sẽ là phép đếm tiếp theo của kênh. ‖

---

## Ghi chú

**Số tự tính** (dữ liệu kênh `data/ck/vnindex_1d.csv` — vnstock/VCI, 08/10/2018 → 06/10/2026, 1.995 phiên; mã
`data/long/ck-c3-bieu-do-nen/analysis.py` → `results.json`; cách tính chi tiết ở hồ sơ mục 4–5):
- **09/03/2026** (CH00): O **1.757,73** = H 1.757,73 (bóng trên 0) · L 1.650,75 · C **1.652,79** (cách đáy **2,04 điểm** → "khoảng hai
  điểm") · thân 104,94 / biên 106,98 = 98%. −115,05 điểm (−6,51%) — số của C2, đã khớp báo chí [C2-7][C2-8].
- **10/03** (CH02): **O mâu thuẫn giữa nguồn** — 1.664,52 (VCI, nguồn thứ ba) vs 1.697,87 (CafeF; bản tin thị trường "gap tăng
  45.08") → lời đọc và chữ trên màn hình **không** dùng màu nến / "3× thân" / giá mở. Phần chắc chắn (4 nguồn + báo): H **1.716,62**
  ("gần một nghìn bảy trăm hai mươi"; TBTC [9] "lên vùng giá 1.720", VnExpress "có thời điểm… đạt 1.715", Công Luận "vượt mốc 1.716")
  · L 1.651,29 · C **1.676,73** (+23,94; +1,45%) · **H − C = 39,89** ("thấp hơn đỉnh gần bốn mươi điểm"). (Theo VCI: thân 12,21,
  bóng trên 3,27× thân; theo CafeF: nến đỏ, thân 21,1, bóng trên 18,8 — cảnh `candles` vẽ theo VCI, có chữ góc "giá mở khác nhau
  giữa các nguồn".)
- **11/03** (CH02): O 1.675,87 ≈ L 1.675,17 ("mở cửa gần đáy") · C 1.728,34 ≈ H 1.729,67 ("đóng cửa gần đỉnh") · **+3,08%** ("khoảng ba
  phần trăm") · thân/biên 96%.
- **12/03**: O 1.716,62 < C hôm trước 1.728,34 ("mở cửa thấp hơn giá đóng cửa hôm trước") · C 1.709,61 (−1,08%) · nến đỏ thân 7,01.
- **13/03** (doji): O 1.697,72 · H 1.716,75 · L 1.688,67 · C **1.696,24** (−13,37; −0,78%, khớp báo [11]) · thân **1,48** ("chưa tới hai
  điểm") · biên **28,08** ("gần ba mươi điểm") · thân/biên 5,3% (≤ 10% → doji theo định nghĩa của kênh).
- **Nến tuần 09–13/03**: O 1.757,73 · H 1.757,73 · L 1.650,75 · C 1.696,24 · so đóng cửa 06/03 (1.767,84): **−4,05%** ("khoảng bốn
  phần trăm") · thân 61,49, bóng dưới 45,49 ("khá dài"), bóng trên 0.
- **24/03** (CH03): C hôm trước (23/03) **1.591,17** = đóng cửa thấp nhất 2026 tính tới 06/10 · O **1.626,34** ("quanh một nghìn sáu trăm
  hai mươi sáu") · H 1.630,63 · L 1.602,92 · C **1.614,77** ("khoảng một nghìn sáu trăm mười lăm") · **+23,60 / +1,48%** (khớp báo
  [12][13]) · C − O = −11,57 → nến đỏ.
- **Màu nến ngược màu bảng giá** (CH03): 1.990 phiên hợp lệ có phiên trước; nến đỏ mà chỉ số tăng **216**, nến xanh mà chỉ số giảm
  **86** → **302 = 15,2%** (1/15,2% = 6,6); nguồn thứ ba **16,4%** (1/6,1) → lời đọc "cứ sáu, bảy phiên". 2026 có 14 + 6 phiên như vậy.
- **Khung thời gian** (CH04): 01/01 → 06/10/2026 = **186** phiên = 186 nến ngày; **39** nến tuần (tuần cuối 05–06/10 chưa trọn → lời
  đọc "khoảng").
- **Mốc so sánh** (CH05): mọi ngày hợp lệ, chỉ số cao hơn sau 5 phiên **58,5%** (n = 1.986), sau 20 phiên **59,2%** (n = 1.971) → "khoảng
  sáu trên mười". Cả giai đoạn **996,12 → 1.759,08 (+76,6%)** ("từ khoảng một nghìn lên khoảng một nghìn bảy trăm sáu mươi").
- **Cây búa đúng sách** (bóng dưới ≥ 2× thân, bóng trên ≤ 10% biên, sau 5 phiên giảm): **35 lần**; sau 5 phiên cao hơn **51,4%** (KTC 95%
  35,6–67,0) vs mốc "mọi ngày sau 5 phiên giảm" **56,3%**; sau 20 phiên **55,9%** vs **59,7%**. Độ nhạy: định nghĩa lỏng (bóng trên ≤
  thân) 52,3% / 60,5% vs 56,3% / 59,7%; bối cảnh "dưới MA10" 45,9% / 50,0% vs 56,4% / 61,0% → kết luận "không hơn" giữ nguyên. Nguồn thứ ba: cũng 35 lần, 42,9% vs 56,4%
  (5 phiên) nhưng **61,8% vs 59,7%** (20 phiên) → lời đọc chỉ nói "không hơn mốc", không nói "kém".
- **Doji** (thân ≤ 10% biên): **201 lần** (nguồn thứ ba 189 → "khoảng hai trăm"); **đổi hướng** (hướng 5 phiên sau ngược hướng 5 phiên trước) **42,8%** vs
  ngày thường **45,0%** ("bốn mươi ba" / "bốn mươi lăm"); nguồn thứ ba 41,3% vs 45,0%.
- **Ba chàng lính trắng đúng sách** (3 nến xanh, đóng cửa cao dần, mở trong thân nến trước, bóng trên ≤ 30% biên, sau 5 phiên giảm):
  **5 lần** (nguồn thứ ba: 2) → lời đọc "vài lần"; lần cuối trước 2023 (bản không cần bối cảnh: 10 lần, cũng **0 lần từ 2023**).
- **"Hơn hai mươi phép so"**: 8 mẫu × 2 khung = 16, + 3 bản độ nhạy × 2 = 6, + nến dài xanh/đỏ × 2 = 4, + doji đổi hướng = 1 → **27**.
- **Kết quả "đẹp"** (KHÔNG đọc tên trong lời — tránh thành tín hiệu; chỉ để trong hồ sơ, **KHÔNG đưa vào mô tả** — quyết định PM 09/10): "ba nến xanh liền" (định nghĩa lỏng, n =
  69) sau 5 phiên cao hơn 71,0% vs 58,5% (p ≈ 0,05), sau 20 phiên 69,6% vs 59,2% (p ≈ 0,10); nhấn chìm tăng (n = 44) sau 5 phiên 70,5% vs
  56,3% (p ≈ 0,06–0,08), sau 20 phiên 65,1% vs 59,7% (p ≈ 0,5); doji sau 20 phiên 65,7% vs 59,2% (p ≈ 0,05–0,07); nến xanh dài (n = 217)
  sau 5 phiên 64,1% vs 58,5% (p ≈ 0,08). Không cái nào qua ngưỡng 5% sau khi tính 27 phép so; cửa sổ chồng nhau làm p thật còn lớn
  hơn. Chênh lợi suất TB 5 phiên của "ba nến xanh liền" ≈ 0,7 điểm % (0,88% vs 0,19%), cùng cỡ chi phí một vòng mua–bán (phí 2 chiều +
  thuế 0,1%, C2). Fact-check: Bonferroni 0,05/27 = 0,0019 (p nhỏ nhất 0,047); chỉ giữ tín hiệu cách nhau ≥ h phiên → p 0,11–0,24.
- **Cảnh hẹn — doji 13/03** (CH05): 5 phiên sau (20/03) C 1.647,81 → **−2,86%** ("gần ba phần trăm"); 23/03 C **1.591,17** = đóng cửa
  thấp nhất 2026 (tới 06/10); 20 phiên sau (10/04) C 1.750,00 → **+3,17%** ("khoảng ba phần trăm").

**Số có nguồn (không tự tính):** Nison 1991 làm phổ biến nến ở phương Tây; sau này (*Beyond Candlesticks*, 1994) viết khó có chuyện Homma dùng
nến, nhiều khả năng ra đời đầu thời Minh Trị, cuối thế kỷ 19 [1]; màu bảng giá theo tham chiếu (C2 [19], SECONDARY); giá tham chiếu =
giá đóng cửa phiên gần nhất, giá mở cửa = giá khớp ATO (C2, QĐ 22/QĐ-HĐTV); báo chí 10/03, 13/03, 24/03 [9]–[13]; Marshall, Young &
Rose 2006 (cổ phiếu DJIA, kỳ dữ liệu 1992–2001/2002 chưa thống nhất → "khoảng mười năm") [2] + luận án 2005 (câu trích) [3]; Marshall, Young & Cahan 2008 (Nhật 1975–2004) [4]; Tharavanij,
Siraprapasiri & Rajchamaha 2017 (SET50 2006–2016) [5]; Ngô Tùng Sơn & cs. 2018 (Việt Nam 2013–2018) [6]; Lu 2014 (Đài Loan 1992–2009) [7];
Zhu, Atri & Yegen 2016 (Trung Quốc 1999–2008) [8].

**Cần kiểm lại trước khi dựng:**
- **Đã xác nhận (fact-check 09/10):** giá mở VN-Index (VCI) = giá trị chỉ số đầu tiên sau khớp ATO — khớp gap trong bản tin 12/03,
  13/03, 24/03 và 3 nguồn dữ liệu; **trừ 10/03** (nguồn mâu thuẫn — lời đọc đã sửa để không phụ thuộc). 24/03 mở 1.626,34 (gap +35,17;
  Vietnambiz "hơn 30 điểm đầu phiên").
- **Đã xác nhận: câu trích từ luận án** — "candlestick technical analysis does not have value" nằm trong **tóm tắt luận án** của Ben
  Marshall (Massey, 2005) [3] (fact-check đã mở PDF); tóm tắt bài J. Banking & Finance 2006 [2] **chưa** mở được → lời đọc gán cho luận
  án ("Marshall kết luận"), không gán cho bài báo/nhóm. Kỳ dữ liệu: luận án "1992 - 2002", thứ cấp "01/01/1992–31/12/2001" → "khoảng
  mười năm".
- **"Hàng chục mẫu nến"** (Marshall 2006): một nguồn thứ cấp ghi **28 tín hiệu** — chưa thấy ở bản gốc → giữ "hàng chục".
- **Nghiên cứu Việt Nam** [6]: chỉ đọc được tóm tắt qua kết quả tìm kiếm (ACM chặn); tên tác giả/hội nghị đã khớp Crossref. Kiểm nội
  dung "không dự báo được xu hướng" trên bản PDF. Đây là bài hội nghị, không phải tạp chí — lời đọc chỉ nói "một nhóm tác giả".
- **Giai thoại Homma**: Nison (qua Wikipedia [1]) chỉ viết "it is unlikely that Homma used candle charts" — Homma là người thật → lời
  đọc nói "nhiều khả năng thương nhân ấy chưa từng dùng biểu đồ nến", ledger không gạch ngang. Sách gốc chưa mở.
- **PM 09/10:** mô tả chỉ có khối phương pháp (factcheck mục 2), **không** bảng tỉ lệ từng mẫu. Lời đọc "Cách kênh đếm, mình tóm tắt
  ở phần mô tả" được thực hiện bằng khối ấy (spec `youtube.more`).
- **"Cứ sáu, bảy phiên"**: VCI 15,2%, nguồn thứ ba 16,4% — lời đọc đúng cả hai nguồn.
- **"Mức thấp nhất của năm nay"** (23/03, CH03 và CH05): đúng theo **giá đóng cửa** tới 06/10/2026 (1.591,17); đáy trong phiên thấp nhất
  2026 cũng là 23/03 (**1.586,44**, kênh đã kiểm `low.min()`). Hồ sơ C1 cũng ghi 1.591,17 là đáy năm theo đóng cửa. Nếu video lên lịch
  sau một phiên đóng cửa thấp hơn → sửa thành "thấp nhất tính tới lúc ấy".
- **"Nhiều ứng dụng tự điều chỉnh giá cũ"**: dữ liệu `breadth_2026` của kênh là giá điều chỉnh (C2 Ghi chú) — đúng với vnstock; câu chung
  "nhiều ứng dụng" là *[suy luận]* phổ biến, không nêu tên ứng dụng.
- **TTS:** "doji" (đọc "đô-gi"), "VN-Index" (bảng `SAY`), "HOSE" ("hô-dê"), "Steve Nison" ("xtiv nai-xơn"), "Ben Marshall" ("ben mác-sồ"),
  "New Zealand" ("niu di-lân") — nghe thử. Lọc `‖`, `HỎI:`, `»`, nhãn trước khi gửi TTS (script_lines đã làm).
- **Gợi bài sau** — lời đọc chung "những bài tới" (xu hướng, rồi MA), không ngày, không số bài: giáo trình gốc tập 8 xu hướng, tập 11
  MA; lịch khoá học chưa xác nhận.
- **Tiêu đề:** (2) có số "8 năm" và tên mẫu — hấp dẫn hơn nhưng dễ bị hiểu là video "tín hiệu"; (1) an toàn với luật kênh. Tránh "chính
  xác 100%", "bí kíp", "sập".
