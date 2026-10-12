# Fact-check — script.md (bản 1) · ck-c3-bieu-do-nen (Chứng khoán từ số 0 — C3)

Ngày kiểm: 09/10/2026. Đối chiếu: hồ sơ `docs/channels/chung-khoan/2026-10-09-long-c3-research.md` (số `[n]` = nguồn trong hồ sơ
đó); luật kênh `2026-10-06-positioning.md` mục 1; `motion/long/RETENTION.md` ("Lời hứa lộ trình"); giáo trình `2026-10-06-research.md`
(bảng 19 tập). Chạy lại `analysis.py` (kết quả **trùng từng byte** với `results.json` và `vnindex_1w_2026.csv` đã lưu) + kiểm độc lập
bằng pandas, và đối chiếu OHLC VN-Index với **hai nguồn dữ liệu khác** (CafeF `PriceHistory.ashx`, API `vnmarket_prices` của một công
ty dữ liệu — chỉ dùng để kiểm, không nêu tên trong video) + bản tin thị trường hằng ngày ghi "gap" mở cửa. Không sửa script.

**Kết luận: OK 92 · SỬA 32 · BỎ 0** (124 hàng: 4 tiêu đề, 84 hàng lời thoại — vài dòng gộp — và 36 hàng chữ/cảnh trên màn hình).
Luật kênh, TTS, tính lại Ghi chú, nguồn ở cuối, không tính vào tổng. Trong 32 SỬA: 4 là quyết định PM (bỏ lời hứa bảng kết quả).

Nhãn: OK = đúng nguồn / chấp nhận được · SỬA = sai số, nói quá nguồn, mơ hồ, hoặc chạm luật kênh · BỎ = nên cắt câu.

**Năm điểm quan trọng nhất**
1. **"Giá mở cửa" của VN-Index = giá trị chỉ số đầu tiên sau khớp ATO — đã kiểm được, và 24/03 + 13/03 đứng vững.** Ba nguồn dữ liệu
   (VCI, CafeF, nguồn thứ ba) cùng ghi O 24/03 = **1.626,34**, O 13/03 = **1.697,72**, O 12/03 = **1.716,62**; bản tin thị trường
   cùng ngày ghi "mở cửa… với gap tăng mạnh **35.17** điểm" (24/03), "gap giảm **11.89**" (13/03), "gap giảm **11.72**" (12/03) — khớp
   tới hai chữ số thập phân. Báo: Vietnambiz 24/03 "VN-Index hồi phục **hơn 30 điểm đầu phiên**"; Người Lao Động: phiên sáng +31,52 lên
   1.622,69, đóng cửa 1.614,77 (+23,60). → **Nến đỏ mà chỉ số tăng ngày 24/03 là thật**; cây doji 13/03 là thật (cả ba nguồn: thân
   1,48 điểm, biên 28–28,5 điểm). Từ 2023, VCI **không** có phiên nào O = đóng cửa hôm trước (tức không phải "giá tham chiếu").
2. **Ngày 10/03 thì KHÔNG chắc — cây nến "xanh, bóng trên gấp ba thân" phụ thuộc nguồn.** VCI và nguồn thứ ba: O **1.664,52**; CafeF:
   O **1.697,87**, và bản tin thị trường 10/03 ghi "mở cửa… với **gap tăng mạnh 45.08 điểm**" (= 1.697,87). Với O = 1.697,87, cây nến
   10/03 là **nến đỏ** (đóng 1.676,73 < mở), thân 21,1, bóng trên 18,8 — không còn "gấp ba lần thân", không còn "bên mua thắng". Phần
   chắc chắn (cả 4 nguồn + báo): đỉnh trong phiên ~1.716,6 (VnExpress "có thời điểm tăng hơn 63 điểm, đạt 1.715"; Công Luận "vượt mốc
   1.716"), đóng cửa 1.676,73 → **đỉnh cao hơn đóng cửa gần 40 điểm**. Sửa L193, L196–197, L232 và mark màn hình cho trung lập về màu.
   (Ngoài ra bản tin PDF 10/03 của một CTCK ghi đóng cửa "1.672,27, +19,48" — **sai**, ngược 4 nguồn khác; không dùng.)
3. **Một số con số mẫu nến không bền khi đổi nguồn dữ liệu** (giá mở/cao/thấp khác nhau ở 259/1.995 phiên giữa VCI và nguồn thứ ba;
   riêng 2021 VCI ghi O = đóng cửa hôm trước ở 133/250 phiên). Chạy lại toàn bộ trên nguồn thứ ba: cây búa đúng sách vẫn **35 lần**,
   sau 5 phiên **42,9%** vs mốc 56,4% (kết luận "không hơn" còn mạnh hơn), nhưng sau 20 phiên **61,8% vs 59,7%** (hơn nhẹ) → câu
   "thậm chí còn kém một chút" (L272) **không bền**; doji **189** lần (không phải "hơn hai trăm"), đổi hướng 41,3% vs 45,0% (bền); ba chàng
   lính trắng đúng sách **2** lần (không phải 5; "0 lần từ 2023" bền); màu nến ngược màu bảng giá **16,4%** (VCI 15,2%) → "cứ sáu, bảy
   phiên". Mốc nền 58,5% / 59,2% chỉ dùng giá đóng cửa → bền (giá đóng cửa khớp 1.989/1.995 phiên).
4. **Câu trích "Phân tích kỹ thuật bằng nến không có giá trị" là của luận án tiến sĩ Marshall (Massey, 2005, một tác giả), không phải
   bài J. Banking & Finance 2006.** Đã mở bản PDF luận án: tóm tắt nguyên văn "…showed that candlestick technical analysis does not
   have value. There is no evidence that a trader adhering to candlestick technical analysis would out-perform the market." Tóm tắt bài
   2006 **vẫn không mở được** (ScienceDirect 403; RePEc lỗi DNS; Crossref/OpenAlex không có tóm tắt). L284 "Kết luận **của họ**" → ghi
   đúng là luận án. Chữ trên màn hình (L115–116) **đã đúng**. "Mười một năm" (L283): luận án ghi "1992 - 2002", nguồn thứ cấp ghi
   "01/01/1992–31/12/2001" và "35 cổ phiếu DJIA" → đổi "khoảng mười năm". "28 mẫu", giữ 10 ngày: chỉ nguồn thứ cấp → giữ "hàng chục".
5. **Quyết định PM đã áp:** bỏ lời hứa đưa "các con số chính" (bảng kết quả "đẹp") vào mô tả — thay bằng tóm tắt cách đếm + câu "không
   kết quả nào còn đứng vững sau khi tính tới việc thử nhiều mẫu cùng lúc, và chưa trừ phí" (L278–281, màn hình L109, Ghi chú L354–359,
   L383–385; khối mô tả ở mục 2). Kiểm thêm cho chắc câu ấy: Bonferroni 0,05/27 = 0,0019, p nhỏ nhất 0,047 → không qua; **chỉ giữ các
   tín hiệu cách nhau ≥ h phiên** (bỏ chồng cửa sổ), p chính xác nhị thức của 4 kết quả "đẹp" là 0,24 / 0,16 / 0,15 / 0,11 — **không
   qua cả ngưỡng 5% thô**. Câu mới đúng, thậm chí còn nhẹ nhàng.

**Các điểm khác:** Nison chỉ viết Homma "khó có dùng biểu đồ nến" (không nói chuyện thương nhân gạo là bịa — Homma có thật) → sửa L177
và ledger gạch ngang L65. Nison **phổ biến** nến ở phương Tây (1991); đã có bản dịch tiếng Anh của Seiki Shimizu, *The Japanese Chart of
Charts* (1986) → "đưa sang" thành "làm phổ biến" *[CHƯA mở nguồn Shimizu — chỉ kiến thức nền; cách nói mới vẫn đúng dù không có nó]*.
"Đại học FPT" trong lời đọc (L288) trùng tên một mã HOSE và thương hiệu một CTCK → bỏ tên trường. Nguồn màn hình L82 có tên một CTCK →
thay bằng báo. Lời gợi bài sau (L316) hứa cả xu hướng **và** MA, trong khi giáo trình xếp xu hướng tập 8, MA tập 11 → nói chung "những bài
tới". Nghiên cứu "có ích" ở **Mỹ** (Caginalp & Laurent 1998, S&P 500 1992–96: "profit of almost 1% during a two-day holding period")
cần nhắc để không gợi ý "Mỹ = đã kết luận không có giá trị".

## 1. Bảng kiểm từng dòng

### 1a. Tiêu đề

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Tiêu đề làm việc | "BIỂU ĐỒ NẾN CHO NGƯỜI MỚI: MỘT CÂY NẾN KỂ GÌ VỀ MỘT PHIÊN, VÀ ĐIỀU NÓ KHÔNG NÓI ĐƯỢC" (L1) | OK | — | Bỏ "(bản 1, chờ kiểm chứng)" khi xuất bản. |
| Tiêu đề (1) | "Biểu đồ nến cho người mới: một cây nến kể gì về một phiên, và điều nó không nói được" (L8–9) | OK | — | **Khuyến nghị.** 84 ký tự (< 100). Đúng nội dung, không hứa tín hiệu, không dự báo, không lỗi thời. |
| Tiêu đề (2) | "Nến búa, doji có báo trước giá? Kênh tự đếm 8 năm VN-Index" (L9) | OK | (không khuyến nghị) | Số đúng (8 năm, 2018–2026). Nhưng tên mẫu + "báo trước giá" kéo người tìm tín hiệu; các con số mẫu nến lại là phần **ít bền nhất** khi đổi nguồn dữ liệu (điểm 3). |
| Tiêu đề (3) | "Đọc biểu đồ nến từ số 0: thân, bóng, xanh đỏ và một tuần VN-Index thật" (L9–10) | OK | — | Đúng, an toàn, kém tò mò hơn (1). |

### 1b. Lời thoại

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| CH00 | "Nhìn cây nến đỏ rất dài này… cả một ngày giao dịch nằm trong đó." (L140–142) | OK | — | 09/03: thân/biên 98% (VCI), cả ba nguồn O 1.757,73 > C 1.652,79. |
| CH00 | "…thứ Hai, chín tháng ba năm nay, ngày VN-Index mất một trăm mười lăm điểm." (L143) | OK | — | 09/03/2026 là thứ Hai; −115,05 (C2, đã khớp Nhân Dân [C2-8]). |
| CH00 | "Cây nến kể rằng hôm ấy chỉ số mở cửa ở đúng mức cao nhất của ngày." (L144) | OK | — | O = H = 1.757,73 ở cả ba nguồn. |
| CH00 | "…đóng cửa chỉ cách đáy của phiên khoảng hai điểm." (L145) | OK | — | C − L = 2,04 (VCI) / 2,05 / 2,30 (CafeF) → "khoảng hai" đúng mọi nguồn. |
| CH00 | "Suốt phiên, chưa lúc nào chỉ số lên được cao hơn giá mở cửa." (L146) | OK | (tuỳ chọn) "Theo cây nến, suốt phiên…" | Đúng theo dữ liệu (O = H). Trước ATO chỉ số đứng ở tham chiếu 1.767,84 — đó không tính là "giá mở cửa" (điểm 1). |
| CH00 | Câu đúc kết + DIỄN Ý "Thấy cây búa là đáy đã tới…" (L147–149) | OK | — | Nhãn DIỄN Ý ✓; không gán cho ai. |
| CH00 | HỎI + "Đó chính là điều video này sẽ đi tìm, bằng dữ liệu thật." (L150–151) | OK | — | Vòng mở 1, đóng ở CH05 L290 ✓. |
| CH00 | Cảnh hẹn "Cuối video, mình sẽ đưa bạn quay lại cây nến thứ Sáu…" (L152–153) | OK | — | Hình thức "cảnh hẹn trước", trả ở L291–296 ✓ (mục 3). Doji 13/03 bền qua 3 nguồn ✓. |
| CH00 | Thương hiệu, bài ba, miễn trừ (L154–156) | OK | — | Luật 2 ✓. |
| CH01 | "Ở bài hai, mình đã đi hết một phiên HOSE, từ chín giờ sáng tới ba giờ chiều." (L160) | OK | — | C2 ✓. |
| CH01 | "…Người vẽ biểu đồ chọn giá mở cửa, giá cao nhất, giá thấp nhất, và giá đóng cửa." (L161–162) | OK | — | OHLC [1]. |
| CH01 | Ví dụ nhiệt độ + "Biểu đồ đường… thường chỉ nối các giá đóng cửa" (L163–166) | OK | (tuỳ chọn) "Biểu đồ đường **theo ngày**…" | Biểu đồ trong phiên trên báo nối giá từng phút; "thường" đã rào. *[suy luận]* |
| CH01 | "Cây nến thì giữ đủ cả bốn con số… bóng nến, hay râu nến… Biểu đồ nến ngày…" (L167–171) | OK | — | [1]. |
| CH01 | "Mà sao lại gọi là nến? Vì phần thân trông như thân cây nến, còn bóng phía trên giống sợi bấc." (L172–173) | OK | — | Tên Nhật *rōsoku-ashi* ("chân nến"); giải thích hình ảnh *[suy luận]*, chấp nhận. |
| CH01 | "Cách vẽ này đến từ Nhật Bản, và đi kèm một câu chuyện rất hay." (L174) | OK | — | Nguồn gốc Nhật: Nison [1]. |
| CH01 | "Người ta kể rằng một thương nhân buôn gạo người Nhật ở thế kỷ mười tám đã nghĩ ra nó." (L175) | OK | — | Đóng khung đúng là **lời kể** ✓ (Wikipedia: "thought to have been developed… by Munehisa Homma"). |
| CH01 | "Người đưa biểu đồ nến sang phương Tây là Steve Nison, qua một cuốn sách năm một nghìn chín trăm chín mươi mốt." (L176) | SỬA | "Người làm cho biểu đồ nến trở nên phổ biến ở phương Tây là Steve Nison, qua một cuốn sách năm một nghìn chín trăm chín mươi mốt." | Wikipedia: "introduced to the Western world by Steve Nison" — nhưng đã có bản dịch Shimizu 1986. "Phổ biến" đúng ở mọi cách hiểu. |
| CH01 | "Vài năm sau, chính ông viết rằng chuyện thương nhân gạo ấy khó có thật." (L177) | SỬA | "Vài năm sau, chính ông viết rằng, theo tìm hiểu của ông, nhiều khả năng thương nhân ấy chưa từng dùng biểu đồ nến." | Nison (*Beyond Candlesticks*, 1994, qua Wikipedia): "based on my research, it is unlikely that Homma used candle charts". Homma là người thật; Nison chỉ nghi chuyện **dùng nến**. Câu gốc nói quá nguồn. |
| CH01 | "Theo ông, nến nhiều khả năng ra đời muộn hơn, vào cuối thế kỷ mười chín." (L178) | OK | — | "more likely… developed in the early part of the Meiji period in Japan (in the late 1800s)" ✓. |
| CH01 | "Một câu chuyện đẹp chưa chắc là chuyện thật. Giữ ý ấy…" (L179) | OK | — | "Chưa chắc" đúng mức (Nison là một ý kiến, không phải bằng chứng lịch sử). |
| CH02 | Hai câu hỏi thân/bóng, ví kéo co (L183–191) | OK | — | Mô tả chuẩn [1]; kéo co *[suy luận]*. |
| CH02 | "Thử với hai ngày ngay sau cây nến đỏ hôm thứ Hai." (L192) | OK | — | — |
| CH02 | "Thứ Ba, mười tháng ba, chỉ số mở cửa quanh một nghìn sáu trăm sáu mươi lăm điểm." (L193) | SỬA | "Thứ Ba, mười tháng ba, chỉ số hồi lại sau cú giảm hôm thứ Hai." | Giá mở 10/03 **mâu thuẫn giữa nguồn**: 1.664,52 (VCI) vs 1.697,87 (CafeF; bản tin thị trường "gap tăng mạnh 45.08 điểm"). Bỏ con số mở cửa. |
| CH02 | "Đầu phiên, nó vọt lên gần một nghìn bảy trăm hai mươi. Báo chí hôm ấy cũng ghi như vậy." (L194) | OK | — | H 1.716,62 ở cả 3 nguồn; VnExpress 10/03: "có thời điểm VN-Index tăng hơn 63 điểm, đạt 1.715 điểm"; Công Luận: "vượt mốc 1.716"; TBTC [9]: "lên vùng giá 1.720". |
| CH02 | "Nhưng tới lúc đóng cửa, chỉ số chỉ còn khoảng một nghìn sáu trăm bảy mươi bảy." (L195) | OK | — | 1.676,73 (+23,94; +1,45%): VnExpress, Công Luận, TBTC [9] ✓. |
| CH02 | "Cây nến hôm ấy màu xanh, thân ngắn, với một cái bóng trên dài gấp ba lần thân." (L196) | SỬA | "Nhìn cây nến hôm ấy, phần phía trên rất dài: lúc đóng cửa, chỉ số đã thấp hơn đỉnh trong phiên gần bốn mươi điểm." | Màu và "3,27× thân" chỉ đúng với O của VCI; với O 1.697,87 nến **đỏ**, bóng trên 18,8 < thân 21,1. H − C = 39,89 đúng mọi nguồn. |
| CH02 | "Nó kể rằng bên mua thắng, nhưng đã bị đẩy lùi một đoạn dài từ chỗ cao nhất." (L197) | SỬA | "Nó kể rằng bên mua đã kéo giá lên rất cao, nhưng rồi bị đẩy lùi một đoạn dài." | "Bên mua thắng" (theo màu nến) phụ thuộc nguồn. Phiên sáng +36,15 (1.688,94), chiều bị bán (Công Luận) ✓. |
| CH02 | "Thứ Tư, mười một tháng ba… xanh dài, gần như không có bóng… tăng khoảng ba phần trăm… bên bán gần như không kéo lại được" (L198–200) | OK | — | Cả 3 nguồn: O 1.675,87, C 1.728,34, H 1.729,67–1.729,77, L 1.675,17; +3,08% ✓. |
| CH02 | HỎI "nến xanh dài là tốt…?" + trả lời (L201–203) | OK | — | Không khuyến nghị ✓; vòng mở 3 đóng ở CH05. |
| CH03 | "Trên hầu hết biểu đồ nến ở Việt Nam, nến xanh là… đóng cửa cao hơn mở cửa…" (L207–209) | OK | — | Thông lệ [1]; *[suy luận]* "hầu hết". |
| CH03 | Bảng giá so với tham chiếu = đóng cửa hôm trước; "Hai thứ màu này so với hai cái mốc khác nhau." (L210–212) | OK | — | QĐ 22/QĐ-HĐTV Điều 31 khoản 2 (C2) ✓. |
| CH03 | "Nên có những ngày chỉ số tăng, bảng giá xanh, mà cây nến lại đỏ. Thứ Ba, hai mươi bốn tháng ba…" (L213–214) | OK | — | 24/03/2026 là thứ Ba ✓; nến đỏ xác nhận 3 nguồn + gap +35,17 (điểm 1). |
| CH03 | "Hôm trước, chỉ số vừa đóng cửa ở mức thấp nhất của năm nay, khoảng một nghìn năm trăm chín mươi mốt điểm." (L215) | OK | — | 23/03 C 1.591,17 = đóng cửa thấp nhất 2026 tới 06/10 (kiểm lại; phiên 08/10: 1.738,97). Đáy trong phiên cũng 23/03 (1.586,44 VCI; 1.582,26 nguồn thứ ba). |
| CH03 | "Sáng thứ Ba, chỉ số mở cửa cao vọt, quanh một nghìn sáu trăm hai mươi sáu." (L216) | OK | — | O 1.626,34 (3 nguồn) = tham chiếu + 35,17 (bản tin "gap tăng mạnh 35.17"); Vietnambiz "hơn 30 điểm đầu phiên". |
| CH03 | "Rồi nó trôi xuống dần, và đóng cửa ở khoảng một nghìn sáu trăm mười lăm." (L217) | SỬA | "Rồi nó không giữ được mức ấy, và đóng cửa ở khoảng một nghìn sáu trăm mười lăm." | Không trôi đều: 9:35 khoảng 1.616 (Vietnambiz), hết phiên sáng 1.622,69 (NLĐ), đóng 1.614,77. "Trôi xuống dần" mô tả sai đường đi. |
| CH03 | "So với hôm trước, chỉ số tăng gần một phẩy năm phần trăm. Bảng giá xanh. So với lúc mở cửa, nó thấp hơn. Cây nến đỏ." (L218–219) | OK | — | +23,60 / +1,48% (Người Lao Động 24/03; hai bản tin thị trường cùng ngày); C − O = −11,57. |
| CH03 | HỎI + "Cả hai màu đều đúng… Màu nến hỏi… Màu bảng giá hỏi…" (L220–222) | OK | — | Tốt cho người mới. |
| CH03 | "Theo kênh tự đếm trên tám năm dữ liệu VN-Index, cứ khoảng bảy phiên lại có một phiên hai màu này ngược nhau." (L223) | SỬA | "Kênh tự đếm trên tám năm dữ liệu VN-Index: cứ sáu, bảy phiên lại có một phiên hai màu này ngược nhau." | VCI 302/1.990 = 15,2% (1/6,6); nguồn thứ ba 16,4% (1/6,1); hai giai đoạn VCI 15,2% / 15,2%. "Sáu, bảy" đúng cả hai nguồn. |
| CH03 | "Có biểu đồ còn vẽ nến tăng rỗng ruột… hãy liếc qua chú thích màu…" (L224–225) | OK | — | [1] (hollow/filled). |
| CH04 | "Giờ bạn đã có đủ đồ nghề… Thứ Hai: nến đỏ dài, gần như không bóng. Bên bán thắng trọn phiên." (L229–231) | OK | — | Bóng trên 0, bóng dưới 2,0. |
| CH04 | "Thứ Ba: nến xanh thân ngắn, bóng trên dài. Bên mua thắng, nhưng bị đẩy lùi từ trên cao." (L232) | SỬA | "Thứ Ba: bóng trên dài. Bên mua kéo giá lên cao, nhưng bị đẩy lùi một đoạn dài." | Như L196–197 (màu 10/03 phụ thuộc nguồn). |
| CH04 | "Thứ Tư: nến xanh dài. Lần này, bên mua giữ được tới cuối." (L233) | OK | — | ✓ |
| CH04 | "Thứ Năm: chỉ số mở cửa thấp hơn giá đóng cửa hôm trước, rồi giảm thêm, thành một cây nến đỏ nhỏ." (L234) | OK | — | O 1.716,62 (3 nguồn) = 1.728,34 − 11,72 (bản tin: "gap giảm 11.72"); C 1.709,61 (−1,08%). Ghi chú: O 12/03 trùng đúng H 10/03 (1.716,62) — trùng hợp, nhưng gap đã được bản tin xác nhận. |
| CH04 | "Thứ Sáu, mười ba tháng ba: một cây nến gần như không có thân… chưa tới hai điểm… gần ba mươi điểm… doji. Hãy nhớ mặt nó…" (L235–237) | OK | — | 3 nguồn: thân 1,48; biên 28,08 (VCI) / 28,54 → 5,2–5,3% (doji ≤ 10%). Gap −11,89 khớp bản tin. Đóng cửa: Nhân Dân 13/03 "giảm 13,37 điểm (-0,78%), xuống mức 1.696,24 điểm" ✓. |
| CH04 | Gộp tuần: "Mở cửa là giá mở cửa sáng thứ Hai… thân đỏ, và một cái bóng dưới khá dài… giảm khoảng bốn phần trăm… lấy lại được một đoạn từ đáy hôm thứ Hai… Một cây nến tuần cho thấy một tuần giảm, có hồi lại." (L238–243) | OK | — | O 1.757,73 · H 1.757,73 · L 1.650,75 (đáy thứ Hai) · C 1.696,24; −4,05% so với 1.767,84; bóng dưới 45,49 = 74% thân. O tuần dùng O 09/03 — 3 nguồn trùng ✓. |
| CH04 | Khung thời gian; "một trăm tám mươi sáu cây nến ngày, nhưng chỉ khoảng ba mươi chín cây nến tuần" (L244–247) | OK | — | 186 phiên (05/01–06/10/2026; phiên đầu năm là 05/01); 39 tuần = 36 tuần đủ 5 phiên + 3 tuần 2 phiên (gồm tuần cuối 05–06/10) → "khoảng" ✓. |
| CH04 | HỎI "xem khung nào mới đúng?" + trả lời (L248–251) | OK | — | *[suy luận]* hợp lý, không khuyến nghị. |
| CH05 | "Sách và mạng xã hội đặt tên cho hàng chục hình dạng nến… cây búa, doji, và ba chàng lính trắng." (L255–257) | OK | — | — |
| CH05 | "Cây búa là nến có thân nhỏ nằm trên cao, bóng dưới dài ít nhất gấp đôi thân, mọc ra sau mấy phiên giảm. Người ta nói nó báo hiệu đáy." (L258–259) | OK | — | Nison: bóng dưới ≥ 2× thân, bóng trên rất nhỏ, sau xu hướng giảm; Morris: bóng trên ≤ 10% biên — trùng định nghĩa `analysis.py` (D ≥ 2B, U ≤ 0,1R). |
| CH05 | "Doji… được gọi là dấu hiệu lưỡng lự, sắp đảo chiều." (L260) | OK | — | "Được gọi là" ✓. Nison: lưỡng lự; ý nghĩa đảo chiều mạnh nhất sau xu hướng tăng — kênh đã thử thêm theo bối cảnh (mục 4), kết luận không đổi. |
| CH05 | "Ba chàng lính trắng là ba nến xanh dài nối nhau sau một đợt giảm…" (L261) | OK | — | Nison ✓. (Code không đòi thân "dài" mà đòi bóng trên ≤ 30% biên — chấp nhận.) |
| CH05 | "Kênh đã thử đếm trên VN-Index, từ tháng mười năm 2018 tới đầu tháng mười năm nay… phải có một cái mốc để so." (L262–263) | OK | — | 08/10/2018 → 06/10/2026, 1.995 phiên ✓. |
| CH05 | "Chọn bừa một ngày bất kỳ… năm phiên sau, hay hai mươi phiên sau. Khoảng sáu trên mười lần, chỉ số cao hơn." (L264–265) | OK | — | 58,5% (n 1.986) / 59,2% (n 1.971); chỉ dùng giá đóng cửa → bền mọi nguồn. |
| CH05 | "Vì trong tám năm, VN-Index đã đi từ khoảng một nghìn lên khoảng một nghìn bảy trăm sáu mươi điểm." (L266) | OK | (tuỳ chọn) "**Một phần** vì…" | 996,12 → 1.759,08 (+76,6%) ✓. Tỉ lệ > 50% còn do phân phối lệch (nhiều tuần tăng nhẹ, ít tuần giảm mạnh) — "vì" là đơn giản hoá chấp nhận được. |
| CH05 | "Nên một mẫu nến muốn chứng tỏ nó báo tăng, phải thắng được con số sáu trên mười ấy, chứ không phải năm mươi phần trăm." (L267) | OK | — | Bài học cốt lõi ✓. |
| CH05 | HỎI + "Cây búa đúng sách xuất hiện ba mươi lăm lần trong tám năm. Năm phiên sau, chỉ số cao hơn ở khoảng năm mươi mốt phần trăm số lần." (L268–270) | OK | — | VCI: 35 lần, 51,4% [KTC 35,6–67,0]. Nguồn thứ ba: cũng 35 lần, 42,9%. |
| CH05 | "Còn với mọi ngày cũng vừa trải qua năm phiên giảm, con số ấy là năm mươi sáu phần trăm." (L271) | SỬA | "Còn với mọi ngày mà năm phiên trước đó chỉ số cũng đi xuống, con số ấy là năm mươi sáu phần trăm." | "Vừa trải qua năm phiên giảm" nghe như **năm phiên giảm liên tiếp**; định nghĩa thật: đóng cửa t−1 < đóng cửa t−6 (giảm ròng). 56,3% (n 817) ✓. |
| CH05 | "Đo sau hai mươi phiên cũng vậy: cây búa không hơn, thậm chí còn kém một chút." (L272) | SỬA | "Đo sau hai mươi phiên, cây búa cũng không hơn mốc. Ba mươi lăm lần là ít, nên chênh lệch nhỏ như vậy, theo chiều nào cũng chưa nói lên điều gì." | VCI 55,9% vs 59,7%; nguồn thứ ba **61,8% vs 59,7%** → "kém" không bền. Giữ cùng chuẩn với các kết quả "đẹp" (cũng bị coi là may rủi). |
| CH05 | "Doji xuất hiện hơn hai trăm lần." (L273) | SỬA | "Doji xuất hiện khoảng hai trăm lần." | VCI 201; nguồn thứ ba 189. |
| CH05 | "Nếu doji báo đảo chiều… Thực tế, sau doji, chỉ số đổi hướng khoảng bốn mươi ba phần trăm số lần. Ngày thường là bốn mươi lăm." (L274–275) | OK | — | 42,8% (n 201) vs 45,0% (n 1.981); nguồn thứ ba 41,3% vs 45,0%; chỉ xét doji sau 5 phiên tăng: 35,2% vs 38,4%; sau 5 phiên giảm: 54,4% vs 54,4%; sau biến động ≥ 3%: 45,1% vs 45,0% → bền. |
| CH05 | "Còn ba chàng lính trắng đúng sách thì quá hiếm: chỉ năm lần trong tám năm, và chưa lần nào từ năm 2023." (L276) | SỬA | "Còn ba chàng lính trắng đúng sách thì quá hiếm: chỉ vài lần trong tám năm, và chưa lần nào từ năm hai nghìn không trăm hai mươi ba." | VCI 5 lần (21/11/2018, 14/05/2019, 28–29/10/2021, 25/11/2021); nguồn thứ ba 2 lần (lần cuối 05/2019). "0 từ 2023" bền. |
| CH05 | "Năm lần thì không đủ để kết luận điều gì, kể cả điều tốt." (L277) | SỬA | "Vài lần thì không đủ để kết luận điều gì, kể cả điều tốt." | Theo L276. |
| CH05 | "Công bằng mà nói, kênh đã chạy hơn hai mươi phép so, và có vài kết quả trông đẹp hơn mốc." (L278) | SỬA | "Công bằng mà nói, kênh đã chạy hơn hai mươi phép so, và có vài kết quả thoạt nhìn trông đẹp hơn mốc." | **Quyết định PM.** 27 phép so (đếm lại ✓). |
| CH05 | "Nhưng chênh lệch không lớn, chưa tính phí và thuế, và chưa đủ để loại trừ may rủi." (L279) | SỬA | "Nhưng không kết quả nào còn đứng vững sau khi tính tới việc thử nhiều mẫu cùng lúc, và đó là khi còn chưa trừ phí." | **Quyết định PM.** Kiểm: Bonferroni 0,0019 vs p nhỏ nhất 0,047; bỏ chồng cửa sổ → p 0,11–0,24 (điểm 5). |
| CH05 | "Chạy đủ nhiều phép thử, kiểu gì cũng gặp vài kết quả đẹp, như tung đồng xu… năm mặt ngửa liền." (L280) | OK | — | Xác suất ≥ 1 chuỗi 5 ngửa trong 30 lần tung ≈ 0,5 — minh hoạ hợp lý. |
| CH05 | "Cách đếm và các con số chính, kênh ghi ở phần mô tả." (L281) | SỬA | "Cách kênh đếm, mình tóm tắt ở phần mô tả để bạn tự kiểm lại." | **Quyết định PM:** mô tả chỉ có cách đếm + kết luận, **không** bảng tỉ lệ từng mẫu (khối mô tả ở mục 2). |
| CH05 | HỎI "Thế các nhà nghiên cứu thì nói sao?" (L282) | OK | — | — |
| CH05 | "Nhóm của Ben Marshall ở New Zealand đã thử hàng chục mẫu nến trên các cổ phiếu thuộc chỉ số Dow Jones của Mỹ, qua mười một năm dữ liệu." (L283) | SỬA | "Nhóm của Ben Marshall ở New Zealand đã thử hàng chục mẫu nến trên các cổ phiếu thuộc chỉ số Dow Jones của Mỹ, với khoảng mười năm dữ liệu." | Luận án (Massey, đã mở): "DJIA component stock data for the 1992 - 2002 period"; thứ cấp (luận văn Lund 2016; tóm tắt tìm kiếm): "35 stocks… January 1, 1992 to December 31, 2001", "28 candlestick patterns", giữ 10 ngày. "Mười một năm" không chắc. |
| CH05 | "Kết luận của họ rất ngắn: [TRÍCH DỊCH] » Phân tích kỹ thuật bằng nến không có giá trị." (L284–285) | SỬA | L284 → "Trong luận án tiến sĩ làm nền cho nghiên cứu ấy, Marshall kết luận rất ngắn:" (L285 giữ nguyên) | Câu trích nằm trong **tóm tắt luận án 2005** (một tác giả): "…showed that candlestick technical analysis does not have value." Dịch đúng. Tóm tắt bài J. Banking & Finance 2006 chưa mở được → không gán cho bài báo/nhóm. |
| CH05 | "Cùng nhóm ấy thử ở Nhật, quê hương của nến, với ba mươi năm dữ liệu, và cũng không thấy lợi nhuận." (L286) | OK | — | Marshall, Young & Cahan, *Rev. Quant. Finance & Accounting* 31(2):191–207 (2008), doi 10.1007/s11156-007-0068-1 (Crossref ✓); 1975–2004, "not profitable… in the entire 30 year period, in three 10 year sub-periods" [SECONDARY — tóm tắt]. "Cùng nhóm" = Marshall, Young ✓. |
| CH05 | "Ở Thái Lan, phần lớn các mẫu nến trên năm mươi cổ phiếu lớn cho lợi nhuận không khác số không." (L287) | OK | (tuỳ chọn) "…cho lợi nhuận không khác số không **một cách đáng kể**." | Tóm tắt (OpenAlex, đã đọc): SET50, 03/07/2006–30/06/2016; "mean returns of most patterns are not statistically different from zero"; "candlestick patterns cannot reliably predict market directions". |
| CH05 | "Ở Việt Nam, một nhóm tác giả của Đại học FPT cũng không thấy các mẫu nến đảo chiều dự báo được xu hướng." (L288) | SỬA | "Ở Việt Nam, một nhóm tác giả ở Hà Nội cũng không thấy các mẫu nến đảo chiều dự báo được xu hướng." | Nội dung ✓ (tóm tắt, OpenAlex): 02/01/2013–15/05/2018, "the tested reversal candlesticks do not demonstrate the ability to predict the market trend"; tác giả thuộc FPT University, Hà Nội. Nhưng "FPT" trùng một mã cổ phiếu HOSE và thương hiệu một CTCK → luật kênh (không nêu tên mã/CTCK). Trích dẫn đầy đủ để ở màn hình/mô tả. |
| CH05 | "Cũng có nghiên cứu ở Đài Loan và Trung Quốc thấy vài mẫu có ích, nhưng chỉ ở vài loại cổ phiếu, vài giai đoạn." (L289) | SỬA | Hai câu: "Cũng có nghiên cứu ở Mỹ, Đài Loan và Trung Quốc thấy vài mẫu có ích, có nơi kể cả sau khi trừ phí." · "Nhưng thường chỉ là vài mẫu, ở vài loại cổ phiếu, trong vài giai đoạn." | Lu 2014 (Đài Loan 1992–2009): 4 mẫu có lãi **sau phí**, vững qua bootstrap [7, hồ sơ]; Zhu & cs. 2016: harami/cross ở cổ phiếu thanh khoản thấp, harami/nhấn chìm/piercing ở cổ phiếu nhỏ thanh khoản cao [8]; Caginalp & Laurent 1998 (S&P 500, 1992–96): mẫu 3 ngày có ý nghĩa ngoài mẫu, ~1%/2 ngày [14]. Câu gốc bỏ Mỹ và làm nhẹ Lu 2014. |
| CH05 | "Nên câu trả lời trung thực là: nếu nến có báo trước được điều gì, thì tín hiệu ấy rất mờ, và không ổn định." (L290) | OK | — | Đúng mức bằng chứng chia hai. |
| CH05 | Cảnh hẹn: "cây doji thứ Sáu… Năm phiên sau, chỉ số thấp hơn gần ba phần trăm. Thêm một phiên nữa, ngày hai mươi ba… thấp nhất của năm. Nhưng hai mươi phiên sau… cao hơn khoảng ba phần trăm." (L291–294) | OK | — | 20/03 C 1.647,81 (−2,86%); 23/03 là phiên kế tiếp (20/03 thứ Sáu) C 1.591,17; 10/04 C 1.750,00 (+3,17%). Giá đóng cửa trùng 3 nguồn. |
| CH05 | "Ai muốn nói cây nến ấy báo giảm hay báo tăng… Một câu chuyện kể sau khi đã biết kết thúc… vẫn chưa chắc là chuyện thật." (L295–296) | OK | — | Đóng motif + vòng mở 1, 2 ✓. |
| CH06 | "Mình không bảo bạn bỏ qua biểu đồ nến…" + 4 câu tự hỏi (L300–306) | OK | — | Công cụ tự quyết (luật 2) ✓. |
| CH06 | "Và đây là những lúc… Phép đếm của kênh chỉ làm trên VN-Index, trong tám năm, chưa tính phí…" (L307–308) | OK | (tuỳ chọn, thêm sau L308) "Ngay cả giá mở cửa của VN-Index, mỗi nguồn dữ liệu đôi khi cũng ghi khác nhau." | Luật 4 ✓. Câu thêm có ví dụ thật 10/03 (điểm 2). |
| CH06 | "Với cổ phiếu ít người giao dịch, một cây nến có khi chỉ là vài lệnh nhỏ…" (L309) | OK | — | *[suy luận]*; Zhu & cs. 2016 cho thấy hiệu quả thay đổi theo thanh khoản. |
| CH06 | "Giá mở cửa của một cổ phiếu là giá khớp trong phiên mở cửa, như bài hai đã kể…" (L310) | OK | — | ATO (C2, QĐ 22/QĐ-HĐTV). Trường hợp ATO không khớp: giá khớp đầu tiên — không cần nêu. |
| CH06 | "Và nhiều ứng dụng tự điều chỉnh giá cũ sau khi công ty chia cổ tức hay thưởng cổ phiếu… có thể khác con số bạn còn nhớ." (L311–312) | OK | — | vnstock giá điều chỉnh (C2) *[suy luận phổ biến]*; không nêu tên ứng dụng ✓. |
| CH06 | Tóm lại (L313–315) | OK | — | — |
| CH06 | "Bài sau, mình sẽ nối nhiều cây nến lại với nhau, để xem xu hướng, và làm quen với đường trung bình động." (L316) | SỬA | "Ở những bài tới, mình sẽ nối nhiều cây nến lại với nhau để xem xu hướng, rồi làm quen với đường trung bình động." | Giáo trình: xu hướng = tập 8, MA = tập 11 (`2026-10-06-research.md`); lịch chưa xác nhận (Ghi chú L394–395). Không ngày, không cam kết "bài 4". |
| CH06 | Câu hỏi bình luận "mẫu nến nào bạn từng được nghe là chắc ăn nhất?…" (L317) | OK | — | Không khuyến nghị; "phép đếm tiếp theo" là lời mời, không phải hẹn ngày. |

### 1c. Chữ và cảnh trên màn hình (Kế hoạch hình ảnh)

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Màn hình CH00 | `candles` 09/03 marks "MỞ CỬA = CAO NHẤT · 1.757,73" · "ĐÓNG CỬA 1.652,79 · CÁCH ĐÁY ≈ 2 ĐIỂM" (L47–49) | OK | — | 3 nguồn ✓. |
| Màn hình CH00 | `date` "09/03/2026" "THỨ HAI" "−115,05 ĐIỂM · BÀI 2" (L50) | OK | — | ✓ |
| Màn hình CH00 | `quote` DIỄN Ý · `question` · `candles` 09–13/03 mark "THỨ SÁU · ?" · `brand` (L51–54) | OK | — | Nhãn DIỄN Ý ✓. |
| Màn hình CH01 | `timeline` 4 mốc · `broll` nhiệt kế + `ledger` "VÍ DỤ GIẢ ĐỊNH" · `kinetic` đường đóng cửa (L57–60) | OK | — | Số nhiệt độ có nhãn giả định ✓. |
| Màn hình CH01 | `candles` 09–11/03 marks THÂN/BÓNG TRÊN/BÓNG DƯỚI · "1 CÂY NẾN = 1 PHIÊN" (L61–63) | OK | — | Mark "BÓNG TRÊN → CAO NHẤT" trên 10/03 vẫn đúng ở mọi nguồn (có bóng trên). |
| Màn hình CH01 | `question` + `broll` nến thật "ẢNH MINH HOẠ" (L64) | OK | — | — |
| Màn hình CH01 | `ledger` "CHUYỆN KỂ vs NGUỒN": "THƯƠNG NHÂN GẠO NHẬT, THẾ KỶ 18" (gạch ngang mờ) · "STEVE NISON (1991) ĐƯA NẾN SANG PHƯƠNG TÂY" · "SAU NÀY ÔNG VIẾT: NHIỀU KHẢ NĂNG RA ĐỜI CUỐI THẾ KỶ 19" (L65–67) | SỬA | Dòng 1 **không gạch ngang**, nhãn "CHUYỆN KỂ: THƯƠNG NHÂN GẠO, THẾ KỶ 18" · dòng 2 "STEVE NISON (1991) PHỔ BIẾN NẾN Ở PHƯƠNG TÂY" · dòng 3 "NISON (1994): KHÓ CÓ CHUYỆN THƯƠNG NHÂN ẤY DÙNG NẾN · NHIỀU KHẢ NĂNG RA ĐỜI ĐẦU THỜI MINH TRỊ, CUỐI THẾ KỶ 19". Nguồn: Nison, *Beyond Candlesticks* (1994), qua Wikipedia. | Gạch ngang = khẳng định chuyện kể sai — quá nguồn (Nison là một ý kiến). |
| Màn hình CH01 | `slam` "CHUYỆN ĐẸP ≠ CHUYỆN THẬT" (L68) | SỬA | "CHUYỆN ĐẸP CHƯA CHẮC LÀ CHUYỆN THẬT" | Khớp lời đọc L179 ("chưa chắc"); dấu ≠ khẳng định quá. |
| Màn hình CH02 | `kinetic` hai câu hỏi + kéo co (L71–72) | OK | — | — |
| Màn hình CH02 | `candles` 09–11/03 marks 10/03 "VỌT LÊN ≈ 1.717 · ĐÓNG 1.676,73" + "BÓNG TRÊN ≈ 3× THÂN" · 11/03 "+3,08% · MỞ ≈ ĐÁY, ĐÓNG ≈ ĐỈNH"; nguồn nhỏ TBTC (L73–74) | SỬA | Bỏ "BÓNG TRÊN ≈ 3× THÂN" → "ĐỈNH − ĐÓNG CỬA ≈ 40 ĐIỂM"; nguồn nhỏ: "Thời báo Tài chính, VnExpress 10/03/2026: đầu phiên +63 điểm, lên vùng 1.715–1.720". Thêm chữ góc nhỏ "Giá mở 10/03 khác nhau giữa các nguồn dữ liệu" (tuỳ chọn). | Điểm 2. Cảnh `candles` sẽ vẽ nến 10/03 **xanh** theo VCI — chấp nhận vì có nhãn nguồn, lời đọc đã trung lập. |
| Màn hình CH02 | `question` "Nến xanh dài là tốt?" → `slam` "NẾN KỂ PHIÊN ĐÃ QUA" / "KHÔNG HỨA PHIÊN SAU" (L75) | OK | — | — |
| Màn hình CH03 | `ledger` hai cột màu nến vs màu bảng giá (L78) | OK | — | — |
| Màn hình CH03 | `candles` 19–27/03 marks 23/03 "1.591,17 · ĐÓNG CỬA THẤP NHẤT 2026 (TỚI 06/10)" · 24/03 "NẾN ĐỎ · CHỈ SỐ +1,48%" (L79–80) | OK | — | ✓ (3 nguồn). |
| Màn hình CH03 | `ledger` "24/03/2026": THAM CHIẾU 1.591,17 · MỞ CỬA ≈ 1.626 · ĐÓNG CỬA 1.614,77 · +23,60 · ≈ −11,6; nguồn "VNDirect, Thời báo Tài chính 24/03/2026… · giá mở: kênh tự tính" (L81–82) | SỬA | Số giữ nguyên. Nguồn: "Thời báo Tài chính, Người Lao Động, Vietnambiz 24/03/2026 (đóng cửa +23,60; đầu phiên tăng hơn 30 điểm) · giá mở: dữ liệu HOSE qua vnstock/VCI" | Tên CTCK trên màn hình chạm luật 1 (positioning). Giá mở không phải "tự tính" mà là dữ liệu; đã khớp 3 nguồn + bản tin gap +35,17. |
| Màn hình CH03 | `question` → `slam` "HAI MÀU · HAI CÂU HỎI" (L83) | OK | — | — |
| Màn hình CH03 | `counter` 0 → 15 "%" "PHIÊN CÓ MÀU NẾN NGƯỢC MÀU BẢNG GIÁ" sub "≈ 1/7 · VN-INDEX 10/2018–10/2026 · KÊNH TỰ ĐẾM" (L84) | SỬA | sub "≈ 1 PHIÊN / 6–7 PHIÊN · VN-INDEX 10/2018–10/2026 · KÊNH TỰ ĐẾM (NGUỒN DỮ LIỆU KHÁC: 16%)" | 15,2% (VCI) / 16,4% (nguồn thứ ba). |
| Màn hình CH03 | `kinetic` "XEM CHÚ THÍCH MÀU…" (L85) | OK | — | — |
| Màn hình CH04 | `candles` 09–13/03 marks T2–T6 (T3 "BỊ ĐẨY LÙI TỪ TRÊN CAO"; T5 "−1,08%"; T6 "DOJI · THÂN 1,48 / BIÊN 28 ĐIỂM") (L88–90) | OK | — | Các mark đã trung lập về màu 10/03 ✓. |
| Màn hình CH04 | `slam` "DOJI" "NHỚ MẶT NÓ" (L91) | OK | — | — |
| Màn hình CH04 | Nến tuần O 1.757,73 · H 1.757,73 · L 1.650,75 · C 1.696,24 · "−4,05% SO VỚI TUẦN TRƯỚC" + dự phòng `ledger` (L92–94) | OK | — | ✓ `vnindex_1w_2026.csv` dòng tuần 09/03. |
| Màn hình CH04 | `bars` "NẾN NGÀY 186 · NẾN TUẦN 39" (L95) | OK | — | ✓ |
| Màn hình CH04 | `question` → `kinetic` khung nhỏ/lớn → `slam` (L96–97) | OK | — | — |
| Màn hình CH05 | `ledger` "BA MẪU NẾN QUEN TÊN" (DIỄN Ý) + ví dụ `candles` 03–12/06 mark 09/06 "CÂY BÚA" (L100–101) | OK | (tuỳ chọn) chọn ví dụ rõ hơn | 09/06 đạt định nghĩa sát nút (bóng dưới = 2,003× thân; bóng trên 7,9% biên) ở cả hai nguồn — hình chưa "đẹp sách". Không hiện kết quả sau đó ✓. |
| Màn hình CH05 | `kinetic` "KÊNH TỰ ĐẾM · VN-INDEX 08/10/2018 → 06/10/2026 · 1.995 PHIÊN · QUÁ KHỨ · KHÔNG PHẢI TÍN HIỆU" (L102) | OK | — | ✓ |
| Màn hình CH05 | `counter` 0 → 59 "%" "NGÀY BẤT KỲ → 20 PHIÊN SAU CHỈ SỐ CAO HƠN" + `candles` 2018–2026 marks "996" · "1.759" (L103–104) | OK | — | 59,2% ✓; 996,12 / 1.759,08 ✓. |
| Màn hình CH05 | `bars` "MỌI NGÀY SAU 5 PHIÊN GIẢM 56,3 · CÂY BÚA (35 LẦN) 51,4" sub "sau 20 phiên: 55,9 vs 59,7" (L105–106) | SỬA | Nhãn "MỌI NGÀY VỪA GIẢM (5 PHIÊN TRƯỚC) 56,3"; sub "SAU 20 PHIÊN: CŨNG KHÔNG HƠN MỐC · 35 LẦN LÀ ÍT" | Như L271–272 (nhãn dễ hiểu thành 5 phiên giảm liên tiếp; số 20 phiên không bền giữa nguồn). |
| Màn hình CH05 | `bars` "ĐỔI CHIỀU": NGÀY THƯỜNG 45,0 · SAU DOJI (201 LẦN) 42,8 (L107) | OK | — | Số đúng với dữ liệu kênh; kết luận bền (nguồn thứ ba 41,3 vs 45,0). |
| Màn hình CH05 | `counter` 0 → 5 "BA CHÀNG LÍNH TRẮNG ĐÚNG SÁCH · 8 NĂM" sub "0 LẦN TỪ 2023 · QUÁ ÍT ĐỂ KẾT LUẬN" (L108) | SỬA | Thay bằng `kinetic` "BA CHÀNG LÍNH TRẮNG ĐÚNG SÁCH · CHỈ VÀI LẦN TRONG 8 NĂM · 0 LẦN TỪ 2023 · QUÁ ÍT ĐỂ KẾT LUẬN" (hoặc giữ counter 5, sub thêm "NGUỒN DỮ LIỆU KHÁC: 2") | Như L276. |
| Màn hình CH05 | `kinetic` "HƠN 20 PHÉP SO · VÀI KẾT QUẢ 'ĐẸP' · CHÊNH ÍT, CHƯA TÍNH PHÍ, CHƯA LOẠI ĐƯỢC MAY RỦI" → đồng xu (L109–110) | SỬA | "HƠN 20 PHÉP SO · KHÔNG KẾT QUẢ NÀO ĐỨNG VỮNG KHI TÍNH ĐỦ SỐ PHÉP THỬ · CHƯA TRỪ PHÍ" → đồng xu giữ | **Quyết định PM.** |
| Màn hình CH05 | `ledger` "CÁC NGHIÊN CỨU" (5 dòng, L111–114) | SỬA | Giữ dòng Mỹ-DJIA ("KHÔNG TẠO GIÁ TRỊ"), Nhật, Thái, Việt Nam; dòng cuối → "MỸ (S&P 500 1992–96), ĐÀI LOAN, TRUNG QUỐC · VÀI MẪU CÓ ÍCH TRONG VÀI ĐIỀU KIỆN (Caginalp & Laurent 1998; Lu 2014; Zhu & cs. 2016)" | Cân bằng như L289. Các dòng khác đúng nguồn (mục 1b L286–288). |
| Màn hình CH05 | `quote` TRÍCH DỊCH; nguồn "B. Marshall, luận án Massey University (2005), cơ sở của bài J. Banking & Finance 2006" (L115–116) | OK | — | **Đúng** — đã mở PDF luận án. |
| Màn hình CH05 | Cảnh hẹn `candles` 02/03–14/04 marks 13/03 DOJI · 20/03 "−2,9%" · 23/03 "THẤP NHẤT NĂM (ĐÓNG CỬA)" · 10/04 "+3,2%" (L117–118) | OK | — | ✓ (giá đóng cửa trùng 3 nguồn). |
| Màn hình CH05 | `slam` "KỂ SAU KHI BIẾT KẾT THÚC" sub "CHUYỆN ĐẸP ≠ CHUYỆN THẬT" (L119) | SỬA | sub "CHUYỆN ĐẸP CHƯA CHẮC LÀ CHUYỆN THẬT" | Như L68. |
| Màn hình CH06 | `ledger` 4 câu · `ledger` "KHI NÀO KHÔNG ĐÚNG" (4 thẻ) · `candles` 09/03 → `slam` (L122–125) | OK | (tuỳ chọn) thẻ 5 "GIÁ MỞ CỬA: MỖI NGUỒN CÓ THỂ GHI KHÁC" | — |
| Màn hình CH06 | `kinetic` "BÀI SAU · NỐI CÁC CÂY NẾN: XU HƯỚNG VÀ ĐƯỜNG TRUNG BÌNH ĐỘNG MA" + teaser SMA20 (L126–127) | SỬA | "NHỮNG BÀI TỚI · NỐI CÁC CÂY NẾN: XU HƯỚNG, RỒI ĐƯỜNG TRUNG BÌNH ĐỘNG MA" | Như L316. Teaser SMA20 không kèm điểm cắt / mũi tên mua bán ✓. |
| Màn hình CH06 | `question` câu hỏi bình luận (L128) | OK | — | — |

## 2. Kiểm luật kênh (positioning mục 1), RETENTION và khối mô tả

| Luật | Kết quả |
|---|---|
| 1. Không bán gì / không nêu tên CTCK, mã, ứng dụng | **2 chỗ SỬA:** "Đại học FPT" (L288 — "FPT" trùng mã HOSE và thương hiệu CTCK) và nguồn màn hình có tên CTCK (L82). Ghi chú/hồ sơ dẫn bản tin CTCK là tài liệu nội bộ, được; **mô tả video không dán link bản tin CTCK** — dùng TBTC, VnExpress, Nhân Dân, Người Lao Động, Vietnambiz, Công Luận. Không có ứng dụng/app nào được nêu ✓. |
| 2. Không dự báo / không khuyến nghị | OK. Không câu nào "nên mua/bán/giữ". Rủi ro "đọc thành tín hiệu" đã giảm theo quyết định PM: lời đọc không nêu tên mẫu "đẹp", mô tả không có tỉ lệ từng mẫu. Câu L272 sửa giúp tránh ngụ ý ngược ("cây búa báo giảm"). Teaser SMA20 (L127) — không vẽ giao cắt. |
| 3. Mọi số có nguồn | Có. Số tự tính tái lập được (chạy lại trùng từng byte). Sai/không bền: L193, L196–197, L232 (giá mở 10/03), L223 (tỉ lệ màu), L272, L273, L276–277 (đổi nguồn dữ liệu), L283 ("mười một năm"), L284 (gán câu trích). |
| 4. Nói cả mặt trái | Có: L278–280 (đa kiểm định), L289 (nghiên cứu ngược chiều), L307–312. Gợi ý thêm câu "giá mở cửa mỗi nguồn ghi khác nhau" (L308) — mặt trái thật, có ví dụ 10/03. |
| 6. Dữ liệu quá khứ | Phiên 09–24/03/2026 đã qua > 6 tháng ✓; "thấp nhất của năm" đúng tới 08/10/2026 (đóng cửa 1.738,97). Nếu đăng sau một phiên đóng cửa < 1.591,17 → "thấp nhất tính tới lúc ấy". |
| Giọng tôn trọng | OK — HỎI được trả lời nghiêm túc; L300 không chê người dùng nến. |
| RETENTION — lời hứa lộ trình | OK. Hình thức **"cảnh hẹn trước"** (L152–153), ghi ở mục Giữ chân ✓; khác video liền trước cùng kênh (C2: "bản đồ bằng hình") ✓; không dùng "ba câu hỏi" ✓. **Trả hẹn:** L291–296 quay lại đúng cây nến thứ Sáu 13/03 và cho người xem tự đọc (L235–237 đã dạy) ✓; lời hứa phụ "tám năm dữ liệu VN-Index nói gì về những lời hứa kia" trả ở L262–277 ✓. Doji 13/03 đã kiểm bền qua 3 nguồn → cảnh hẹn an toàn. |
| RETENTION — gợi bài sau | SỬA L316/L126: chung chung "những bài tới", không ngày, không số bài (giáo trình: xu hướng tập 8, MA tập 11). |
| RETENTION — khác | 3 vòng mở đóng đúng chỗ ✓; motif "chuyện đẹp" 3 lần (L179, L280, L296) ✓; cảnh mạnh ~75% (kênh tự đếm) ✓; không danh sách > 3 mục trong lời đọc (L302–305 là 4 câu hỏi đánh số — đã có ở C1/C2, chấp nhận vì là công cụ tự kiểm); 2.686 âm tiết (đếm lại) ≈ 12 phút như khuôn kênh CK. |

**Khối mô tả — phương pháp (thay bảng kết quả; 381 ký tự + link, ≤ 500):**

> CÁCH KÊNH ĐẾM (quá khứ, không phải tín hiệu): VN-Index 08/10/2018–06/10/2026, 1.995 phiên (HOSE qua vnstock/VCI). Với mỗi mẫu nến,
> kênh đếm tỉ lệ số lần chỉ số cao hơn sau 5 và 20 phiên, rồi so với mọi ngày cùng bối cảnh (mốc ~59%, không phải 50%). Tổng cộng 27
> phép so. Không kết quả nào còn đứng vững sau khi tính tới việc thử nhiều mẫu cùng lúc, và chưa trừ phí, thuế. Mã tính: [link analysis.py]

(Không có tỉ lệ thắng của từng mẫu. Các số đã đọc trong video — 35 / 51% / 56%, ~200 / 43% / 45% — đã có nguồn "kênh tự đếm" trên màn
hình; mục nguồn trong mô tả dẫn link mã tính + các bài báo học thuật, **không** link bản tin CTCK.)

## 3. TTS — chỗ dễ đọc sai

| Chỗ | Rủi ro | Gợi ý (chỉ trong bản gửi TTS) |
|---|---|---|
| "doji" (L237, L260, L273, L275, L291) | "đô-ji", "đốt-gi" | "đô-gi", cố định. |
| "Steve Nison" (L176), "Ben Marshall" (L283), "Marshall" (L284 bản sửa) | Đánh vần | "xtiv nai-xơn", "ben mác-sồ", "mác-sồ". |
| "New Zealand", "Dow Jones" (L283) | "niu de-lan", "đâu giôn" | "niu di-lân", "đao giôn". |
| "VN-Index", "HOSE" | Gạch nối / "hô-xe" | Bảng `SAY` như C1/C2 ("hô-dê"). |
| "FPT" (L288) | — | Bỏ theo bản sửa. |
| Chữ số trong lời đọc | Không có chữ số nào CH00–CH06 (đã grep) ✓ | — |
| Câu dài nhất | Không câu nào > 32 âm tiết ✓; câu sửa L289 đã tách đôi | — |
| "‖", "HỎI:", "»", nhãn | Đọc ra thành tiếng | Lọc trước TTS (Ghi chú đã nêu ✓). |

## 4. Tính lại các số trong "Ghi chú" + kiểm `analysis.py`

**Chạy lại:** `python data/long/ck-c3-bieu-do-nen/analysis.py` → `results.json` và `vnindex_1w_2026.csv` **trùng từng byte** với bản
lưu. Không có nhìn trước (look-ahead): bối cảnh dùng đóng cửa t−1, t−6; SMA10 và trung vị thân dời 1 phiên; lợi suất từ đóng cửa t.

| Mục Ghi chú | Kết quả tính lại / đối chiếu | Kết luận |
|---|---|---|
| 09/03: O = H 1.757,73 · L 1.650,75 · C 1.652,79 · cách đáy 2,04 · thân/biên 98% | Khớp; 3 nguồn cùng O/H/C; L 1.650,49–1.650,75 | OK |
| 10/03: O 1.664,52 · H 1.716,62 · L 1.651,29 · C 1.676,73 · bóng trên 3,27× thân | H, L, C khớp; **O mâu thuẫn**: CafeF 1.697,87 + bản tin "gap tăng 45.08" → 3,27× và màu xanh không bền | SỬA (L327–329) |
| 11/03, 12/03 | Khớp 3 nguồn; gap 12/03 −11,72 khớp bản tin | OK |
| 13/03 doji: thân 1,48 · biên 28,08 · 5,3% | Khớp; nguồn thứ ba biên 28,54 (5,2%); gap −11,89 khớp bản tin | OK |
| Nến tuần 09–13/03: −4,05%, thân 61,49, bóng dưới 45,49 | Khớp | OK |
| 24/03: O 1.626,34 · H 1.630,63 · L 1.602,92 · C 1.614,77 · +23,60 / +1,48% · C − O −11,57 | Khớp 3 nguồn + gap +35,17 | OK |
| Màu ngược: 216 + 86 = 302 / 1.990 = 15,2% | 15,18%; hai giai đoạn 15,2% / 15,2%; nguồn thứ ba 16,4% (2023–2026: 14,9%). Nếu bỏ phiên thân < 0,1%: 10,5% | OK, đổi lời đọc "sáu, bảy phiên" |
| 186 nến ngày · 39 nến tuần | 186 (05/01–06/10); 39 = 36 tuần × 5 phiên + 3 tuần × 2 phiên | OK |
| Mốc nền 58,5% (n 1.986) · 59,2% (n 1.971) · 996,12 → 1.759,08 (+76,6%) | Khớp; vừa giảm 56,3% / 59,7% (n 817 / 806) | OK |
| Cây búa 35 · 51,4% [35,6–67,0] vs 56,3% · 20 phiên 55,9% vs 59,7%; độ nhạy | Khớp. Nguồn thứ ba: 35 lần, 42,9% vs 56,4%, **61,8% vs 59,7%**. Bỏ chồng cửa sổ (5 phiên): n 31, 54,8%, p 0,86 | OK, sửa lời L272 |
| Doji 201 · đổi hướng 42,8% vs 45,0% | Khớp; nguồn thứ ba 189 · 41,3% vs 45,0%; theo bối cảnh: sau tăng 35,2/38,4, sau giảm 54,4/54,4, biến động ≥ 3% 45,1/45,0 | OK, sửa "hơn hai trăm" |
| Ba chàng lính trắng đúng sách 5 (lỏng: 10), 0 từ 2023 | Khớp (VCI); nguồn thứ ba 2 | Sửa "năm lần" → "vài lần" |
| "27 phép so" | 16 + 6 + 4 + 1 = 27 ✓ (chưa tính 8 phép "ngày ngẫu nhiên" — là kiểm lại, không phải phép so mới) | OK |
| Kết quả "đẹp": ba nến xanh liền 71,0% p 0,047 (n 69) · nhấn chìm 70,5% p 0,08 · doji 20 phiên 65,7% p 0,07 · nến xanh dài 64,1% p 0,08 | Khớp. **Chồng cửa sổ:** 22/69 tín hiệu "ba nến xanh liền" là ngày liền kề. Chỉ giữ tín hiệu cách ≥ h phiên, p chính xác nhị thức: 0,24 (n 47) / 0,16 (n 41) / 0,15 (n 72) / 0,11 (n 147). Bonferroni 0,0019, Holm, BH (p·27 ≥ 1,2): **không cái nào qua** | OK; câu PM đúng |
| Chênh lợi suất TB ≈ 0,7 điểm % (0,88 vs 0,19) | 0,69 ✓ | OK |
| Cảnh hẹn: −2,86% (20/03) · 1.591,17 (23/03) · +3,17% (10/04) | Khớp | OK |

**Kiểm định nghĩa so với sách (`analysis.py`):** búa (D ≥ 2B, U ≤ 0,1R, sau giảm) = Nison + Morris ✓; doji (B ≤ 0,1R) — ngưỡng định lượng
phổ biến (có tác giả dùng 5%) ✓; ba chàng lính trắng: mở trong thân nến trước, đóng cao dần ✓ nhưng không đòi thân dài (lỏng hơn Nison);
nhấn chìm tăng: thân nay bao thân hôm trước ✓; bối cảnh "giảm 5 phiên" thay cho EMA10 của Marshall & cs. — đã thử độ nhạy "dưới MA10"
✓. **Hạn chế cần ghi trong hồ sơ:** (a) định nghĩa "open" của VCI không nhất quán theo thời gian — 2021 có 133/250 phiên O = đóng cửa hôm
trước (2019: 15, 2020: 19, 2022: 19, 2023–2026: 0–1); giá mở/cao/thấp lệch với nguồn thứ ba ở 259/1.995 phiên; (b) `binom_p` là xấp xỉ
chuẩn và coi mốc là hằng số — ổn vì n mốc lớn; (c) khoảng tin cậy Wilson và kiểm định "ngày ngẫu nhiên" bỏ qua chồng cửa sổ → lạc quan
(code đã ghi chú); (d) mốc "vừa giảm" có chứa chính các ngày tín hiệu (35/817) — sai lệch không đáng kể; (e) ba con quạ đen n = 2 — vô nghĩa,
nên bỏ khỏi đếm "8 mẫu" nếu viết lại.

**Ghi chú "Cần kiểm lại" — trả lời:** giá mở VN-Index (VCI) = giá trị chỉ số đầu tiên sau khớp ATO — xác nhận bằng gap trong bản tin 12/03,
13/03, 24/03 và 3 nguồn dữ liệu; **trừ 10/03** (nguồn mâu thuẫn) · câu trích → luận án 2005 (đã mở PDF), tóm tắt bài 2006 **chưa** mở
được · "28 tín hiệu", "35 cổ phiếu", "1992–2001": thứ cấp (luận văn Lund 2016, tóm tắt tìm kiếm) → giữ "hàng chục", đổi "khoảng mười năm"
· nghiên cứu Việt Nam: tóm tắt đầy đủ (OpenAlex) xác nhận "do not demonstrate the ability to predict the market trend", tác giả FPT
University Hà Nội; **chưa** đọc toàn văn PDF · Homma: câu Nison xác nhận qua Wikipedia (có ISBN), **chưa** mở sách · "không đọc tên kết
quả đẹp": PM quyết **giữ** + **không** đưa bảng vào mô tả · "cứ khoảng bảy phiên" → "sáu, bảy phiên" · "thấp nhất của năm" đúng tới
08/10/2026 · gợi bài sau → "những bài tới".

**Ghi chú trong script cần sửa theo (không tính vào tổng):** L327–329 (10/03: thêm "O mâu thuẫn giữa nguồn; lời đọc không dùng màu/3×");
L340–341 (thêm 16,4% nguồn thứ ba); L346–352 (thêm kết quả nguồn thứ ba); L354–359 giữ trong hồ sơ nhưng ghi "KHÔNG đưa vào mô tả"; L363
"Nison 1991 đưa nến sang phương Tây" → "phổ biến"; L375–378 → "đã xác nhận: câu trích từ luận án"; **L383–385 thay hẳn** bằng "PM
09/10: mô tả chỉ có khối phương pháp (factcheck mục 2), không bảng tỉ lệ từng mẫu"; L394–395 khớp với L316 mới. **Các tệp `ch00–ch06.json`
chép lời thoại → áp cùng các SỬA.**

**Hồ sơ `2026-10-09-long-c3-research.md` cần sửa theo:** bảng Tóm tắt #5 và mục 3 hàng 10/03 (O mâu thuẫn: 1.664,52 vs 1.697,87); mục 3
đối chiếu báo chí — thêm VnExpress, Công Luận (10/03), Nhân Dân (13/03), Người Lao Động, Vietnambiz (24/03); ghi bản tin PDF 10/03 "1.672,27"
là sai; mục 6 dòng Marshall 2006 — câu trích thuộc luận án, kỳ dữ liệu 1992–2001/2002 chưa thống nhất; dòng Nhật thêm doi
10.1007/s11156-007-0068-1; dòng Việt Nam nâng nhãn nội dung lên [bằng chứng — tóm tắt]; dòng Thái nâng [bằng chứng]; mục 9 bullet cuối
(bảng trong mô tả) → theo quyết định PM; thêm hạn chế "định nghĩa open của VCI 2021".

## 5. Nguồn đã mở trong lần fact-check này

- **Luận án Marshall (2005), Massey University** — bản PDF (trang tóm tắt): https://mro.massey.ac.nz/bitstreams/7afc8049-23a1-4fe9-ac3a-792d6403ef1c/download ;
  trang mục lục: https://mro.massey.ac.nz/items/edc6c1cf-63d9-4c94-a13d-92ffe1a53481/full
- Marshall, Young & Rose (2006) — Crossref (thông tin xuất bản, không có tóm tắt): https://api.crossref.org/works/10.1016/j.jbankfin.2005.08.001 ;
  EconPapers (chỉ metadata): https://econpapers.repec.org/article/eeejbfina/v_3a30_3ay_3a2006_3ai_3a8_3ap_3a2303-2323.htm ; ScienceDirect 403
- Luận văn Lund (2016), mô tả thứ cấp MYR 2006 (35 cổ phiếu DJIA 1992–2001, EMA10) và MYC 2008: https://lup.lub.lu.se/luur/download?func=downloadFile&recordOId=8877738&fileOId=8877838
- Marshall, Young & Cahan (2008) — Crossref: https://api.crossref.org/works/10.1007/s11156-007-0068-1 ; tóm tắt qua tìm kiếm: https://ideas.repec.org/a/kap/rqfnac/v31y2008i2p191-207.html [SECONDARY]
- Tharavanij & cs. (2017) — tóm tắt đầy đủ qua OpenAlex: https://doi.org/10.1177/2158244017736799
- Ngô Tùng Sơn & cs. (2018) — tóm tắt + đơn vị (OpenAlex): https://api.openalex.org/works/doi:10.1145/3277139.3277161
- Zhu, Atri & Yegen (2016) — tóm tắt qua tìm kiếm: https://ideas.repec.org/a/eee/pacfin/v37y2016icp116-127.html [SECONDARY]; Lu (2014) — chỉ metadata
- Caginalp & Laurent (1998) — tóm tắt qua tìm kiếm: https://ideas.repec.org/a/taf/apmtfi/v5y1998i3-4p181-205.html [SECONDARY]
- Wikipedia "Candlestick chart" (History; trích Nison, *Beyond Candlesticks*, Wiley 1994, ISBN 9780471007203): https://en.wikipedia.org/wiki/Candlestick_chart
- **Báo chí:** VnExpress 10/03/2026 https://vnexpress.net/vn-index-tang-gan-24-diem-5048812.html · Công Luận 10/03/2026
  https://congluan.vn/chung-khoan-hom-nay-10-3-2026-hoi-phuc-manh-vn-index-tang-gan-24-diem-10332937.html · Nhân Dân 13/03/2026
  https://nhandan.vn/ocop/chung-khoan-ngay-133-co-phieu-dau-khi-bi-ban-manh-vn-index-giam-tiep-hon-13-diem-post948183.html · Người Lao Động
  24/03/2026 https://tuoitre.vn/nld/vn-index-phuc-hoi-gan-24-diem-co-phieu-ngan-hang-bat-dong-san-dan-song-196260324155859073.htm ·
  Vietnambiz 24/03/2026 https://vietnambiz.vn/vn-index-hoi-phuc-hon-30-diem-dau-phien-sac-xanh-lan-rong-20263249443760.htm
- **Bản tin thị trường (chỉ để kiểm "gap" mở cửa, không dẫn trong video):** Shinhan Market Rader 10/03, 12/03, 13/03, 24/03/2026
  (https://shinhansec.com.vn/uploads/report/Market_Rader_2026_03_13_VN1.pdf ; `…_2026_03_10_VN.pdf`, `…_03_12_VN.pdf`, `…_03_24_VN.pdf`);
  VNDirect Daily Recap 10/03 (ghi sai 1.672,27), 13/03, 24/03 (link trong hồ sơ [10]–[12])
- **Dữ liệu đối chiếu OHLC:** CafeF https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol=VNINDEX&StartDate=03/02/2026&EndDate=04/14/2026&PageIndex=1&PageSize=50 ;
  API `vnmarket_prices` (code:VNINDEX, 08/10/2018–06/10/2026, 1.995 phiên)
- Giáo trình 19 tập: `docs/channels/chung-khoan/2026-10-06-research.md` (tập 8 xu hướng, tập 11 MA)

**Việc còn mở (không chặn bản 2):** tóm tắt bài J. Banking & Finance 2006 (để chốt số mẫu và kỳ dữ liệu); toàn văn bài IMMS 2018 (ACM);
sách *Beyond Candlesticks* bản gốc; giá mở thật 10/03/2026 (cần ảnh chụp biểu đồ trong phiên của HOSE hoặc nguồn thứ tư) — lời đọc đã
sửa để không phụ thuộc; tóm tắt Lu 2014 bản gốc (hiện dựa hồ sơ [7]); nguồn Shimizu 1986 (không dùng trong lời đọc).
