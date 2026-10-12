# Fact-check — script.md (bản 1) · ck-b1-mua-hay-thue (Quyết định lớn — B1)

Ngày kiểm: 07/10/2026. Đối chiếu: hồ sơ `docs/channels/chung-khoan/2026-10-07-long-b1-research.md` (số `[n]` = nguồn trong hồ sơ
đó); luật kênh `2026-10-06-positioning.md` mục 1 + §3B; `motion/long/RETENTION.md` ("Lời hứa lộ trình"); `motion/long/describe.py`
(giới hạn mô tả); dữ liệu `data/ck/vnindex_1d.csv`, `chartdata._series('sjc')`. **Toàn bộ ví dụ được tính lại độc lập** bằng mô hình
Python riêng (scratchpad `b1_model.py`, mô phỏng theo tháng). Không sửa script.

**Giới hạn của lần kiểm này:** phần tra cứu web (báo cáo gốc CBRE/REFI/Savills/DKRA/VARS-IRE, văn bản luật, kế hoạch tuyển sinh Hà
Nội) **chưa trả kết quả trước khi nộp** → các dòng phụ thuộc nguồn ngoài được chấm theo hồ sơ và ghi rõ **[chưa kiểm lại nguồn
gốc]**; xem mục 6 "Việc còn mở". Phần tính toán, logic, luật kênh, RETENTION, TTS, mô tả là kết quả đầy đủ.

**Kết luận: OK 102 · SỬA 23 · BỎ 0** (125 hàng: 4 tiêu đề, 87 hàng lời thoại — vài dòng gộp — và 34 hàng chữ/cảnh trên màn hình).

Nhãn: OK = đúng nguồn / chấp nhận được · SỬA = sai số, nói quá nguồn, mơ hồ, hoặc chạm luật kênh · BỎ = nên cắt câu.

**Năm điểm quan trọng nhất**
1. **Mọi con số của ví dụ tính lại khớp** (sai khác ≤ 0,01): khoản trả T1 18,75 · T24 17,70 · T25 21,10 (+3,40 tr, +19,2%, 70,3%
   thu nhập) · lãi 24 tháng 317,35 tr · thuê 24 tháng 153,75 tr · 10 năm: người thuê 4,054 tỷ, người mua 1,550 / 2,393 / 3,091 tỷ
   (g = 0 / 3 / 5%) · hoà vốn **7,448%** · độ nhạy 6,34–8,32% · tiêu hết phần chênh 2,019 tỷ → **1,77%**. Không có lỗi số học.
2. **Hai câu giải thích sai cơ chế (dù số đúng):** L298 "ở càng lâu… vì đến một lúc nhà bên trái hết nợ" — ở 20 năm vẫn còn nợ
   300 tr (vay 25 năm); hoà vốn giảm theo thời gian ở chủ yếu vì **phí mua/bán chia cho nhiều năm hơn và tiền thuê tăng 5%/năm**
   (3 năm 8,38% → 5 năm 8,08 → 10 năm 7,45 → 15 năm 6,99 → 20 năm 6,64 → 25 năm 6,37). L297 liệt kê "lãi thả nổi, mức tăng tiền
   thuê hay số năm ở" → các giả định này chỉ cho dải **6,64–8,08%** ("hơn sáu rưỡi tới khoảng tám"); "hơn tám" (8,32) đến từ **lãi
   tiết kiệm 8%**, không có trong câu → thêm "lãi tiết kiệm" vào danh sách.
3. **L289 "Từ năm thứ ba, con số ấy lên khoảng mười lăm triệu"** nghe như phần chênh giữ ~15 tr suốt 8 năm; thực tế 15,25 tr chỉ ở
   tháng 25, rồi giảm dần còn **6,9 tr ở tháng 120** (khoản trả giảm, tiền thuê tăng). Sửa "rồi nhỏ dần".
4. **Giả định ẩn có lợi cho người thuê, chưa nói với người xem:** (a) gửi 6,8% **ghép lãi hằng tháng** (lãi thực 7,02%/năm) trong
   khi sổ 12 tháng chỉ ghép năm → nếu ghép năm, hoà vốn 7,30% (không 7,45); (b) lãi tiết kiệm 6,8% và lãi thả nổi 14% giữ nguyên 8–10
   năm; (c) giá nhà và tiền thuê đi độc lập: ở mức hoà vốn 7,45% thì tỷ suất cho thuê năm 10 rơi xuống ~2,3%, còn ở kịch bản "giá
   đứng yên" tiền thuê vẫn +5%/năm → tỷ suất lên 4,65% (kịch bản giá phẳng hơi bi quan cho người mua); (d) **người thuê phải để dành
   13,5 tr/tháng = 45% thu nhập** liên tục để đạt 4,05 tỷ — mức tiết kiệm rất cao, script có nhắc kỷ luật (CH05) nhưng không nói con
   số %; (e) bỏ qua môi giới (+1% bán → 7,56%), nội thất, tiền cọc thuê, chuyển nhà; (f) kinh phí bảo trì 2% không vào ví dụ gốc
   (nếu căn mua của chủ đầu tư → 7,66%); (g) trả gốc đều chứ không niên kim (niên kim → 7,90%); (h) thu nhập 30 tr không đổi 10 năm.
   Không giả định nào làm sai kết luận định tính; đề nghị thêm chữ nhỏ trên cảnh `slam` "≈ 7,5%" (mục 1c).
5. **Ba điểm luật kênh / lời hứa:** L350 hứa "công thức nằm ở phần mô tả" — mô tả bị trần 4.900 ký tự và `describe.py` tự co danh sách
   nguồn → cần khối công thức cố định trong `youtube.more` (đã viết, 486 ký tự, mục 4b); L356 gợi "bài sau… trả góp 0%" — positioning
   §3B có B2 nhưng **chưa có lịch** → đổi câu chung; L301 "Năm nay thì chưa." là câu ngầm dự báo ("chưa" = sẽ) và sai với sơ cấp (CBRE
   sơ cấp +21% y/y) → đổi thành câu quá khứ. L179 "các nguồn khá thống nhất" chỉ có một nguồn (CBRE qua một tạp chí) → đổi "Theo một
   công ty tư vấn".

**Năm điểm tác giả nhờ kiểm (cuối hồ sơ) — kết quả:**
(1) **Giá/m² Hà Nội lệch nguồn:** chưa mở được báo cáo gốc CBRE. Khung trình bày an toàn nhất: **không đặt bốn số lên cùng một biểu
đồ "QUÝ II/2026"** (cột Batdongsan là quý III, là giá rao; cột CBRE thứ cấp 60 tr/m² thấp bất thường so Bộ XD 123 cùng quý — rất có
thể khác định nghĩa/diện tích tính). Đề nghị bản 2: bỏ cột CBRE thứ cấp cho tới khi thấy bản gốc; lời đọc L177 "có nguồn ghi khoảng
tám mươi, có nguồn ghi hơn một trăm hai mươi triệu" (95 sơ cấp CBRE, 83 giá rao, 123 Bộ XD) — vẫn đủ minh hoạ "cùng thành phố, khác
cách đo". Căn ví dụ ~50 tr/m² vẫn "rẻ hơn mọi mức bình quân".
(2) **Tỷ suất cho thuê REFI:** chưa mở được bản gốc REFI; giữ "theo một đơn vị nghiên cứu thị trường" + nguồn trên màn "REFI, qua
CafeBiz 29/08/2026" (SECONDARY). Số 2,32 / 3,30 / 4,34 / 3,05 nhất quán nội bộ (bình quân cả nước nằm giữa) và cùng chiều Batdongsan
(~3%, 04/2026) [2] → rủi ro thấp.
(3) **Lãi vay:** 10,9% / 13–15% / 3,3–3,5 / 5,5–6,7 khớp hồ sơ [6][7] (SECONDARY). "Gốc đều là kiểu phổ biến": chưa có nguồn định
lượng → đổi "kiểu trả phổ biến" thành "**một kiểu trả hay gặp**" (L211). Nếu người xem vay niên kim, cú nhảy vẫn cùng chiều
(14,70 → 17,93 tr, +22%, đã tính lại khớp).
(4) **Tuyển sinh + 15 m²:** chưa mở văn bản Sở GD&ĐT Hà Nội; câu trích L325 là lời **bài báo** (VietNamNet), không phải văn bản → giữ
cách giới thiệu "Một bài báo… ghi rõ" (đúng); "lần đầu tiên" dựa trên tiêu đề báo [19]. **15 m² "nội thành"**: NQ 10/2023 viết theo
quận cũ; từ 01/07/2025 Hà Nội không còn cấp quận → khái niệm "nội thành" phải đọc theo văn bản hiện hành → đổi L322 thành câu mềm
(mục 1b) cho tới khi kiểm được.
(5) **Thuế phí:** 0,5% trước bạ, 2% bảo trì, 2% TNCN chuyển nhượng, miễn thuế lãi tiền gửi cá nhân — khớp hồ sơ [12][13][16][22]
(SECONDARY — trang tra cứu luật); chưa đối chiếu điều khoản gốc trong lần này. Một chỗ diễn đạt cần sửa: kinh phí bảo trì 2% theo
Luật Nhà ở là khoản **được tính vào tiền mua và ghi riêng trong hợp đồng**, không hẳn "ngoài giá bán" (L236).

## 1. Bảng kiểm từng dòng

### 1a. Tiêu đề

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Tiêu đề làm việc | "HAI CĂN HỘ GIỐNG HỆT NHAU, MỘT MUA MỘT THUÊ: MƯỜI NĂM SAU AI KHÁ HƠN?" (L1) | OK | — | Đúng mô-típ. |
| Tiêu đề (1) | "Mua nhà hay thuê nhà rồi đầu tư phần chênh? Tính thật với thu nhập 30 triệu năm 2026" (L8) | SỬA | "Mua nhà hay thuê rồi để dành phần chênh? Phép tính 10 năm với thu nhập 30 triệu" | "Tính thật" mâu thuẫn nhãn VÍ DỤ GIẢ ĐỊNH; "đầu tư" gợi chứng khoán trong khi mô hình chỉ gửi tiết kiệm 6,8%. |
| Tiêu đề (2) | "Hai căn hộ giống hệt nhau, một mua một thuê: 10 năm sau ai khá hơn?" (L9) | OK | — | **Khuyến nghị.** Khớp cold open + vòng mở 1, video trả lời bằng điều kiện (hoà vốn ~7,5%) nên không thành phán quyết; không hứa lãi, không dự báo. |
| Tiêu đề (3) | "Giá nhà phải tăng bao nhiêu mỗi năm thì mua mới hơn thuê? Bảng tự tính cho người Hà Nội, TP.HCM" (L9–10) | SỬA | "Giá nhà phải tăng bao nhiêu mỗi năm thì mua mới bằng thuê? Một phép tính 10 năm" | "hơn thuê" nghe như phán; ví dụ dùng tỷ suất 3% chung, không riêng HN/HCM. |

### 1b. Lời thoại

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| CH00 | Hai căn giống hệt, ~2,5 tỷ (L155–156) | OK | — | Ví dụ giả định; nhãn góc bắt buộc. |
| CH00 | "…mỗi tháng chuyển cho ngân hàng gần mười chín triệu đồng" (L157) | OK | — | T1 = 18,75 ✓ (tính lại). Là tháng đầu; khoản trả đổi 15,6–21,1 qua 10 năm. |
| CH00 | "…trả chủ nhà khoảng sáu triệu" (L158) | OK | — | 6,25 ✓. |
| CH00 | Thu nhập ~30 triệu (L159) | OK | — | Giả định; cao hơn ~3 lần thu nhập bình quân thành thị 10,7 tr [A1-3] — hợp với cặp vợ chồng thành thị. |
| CH00 | HỎI + "mua chứ, tiền thuê là tiền mất" (L160–162) | OK | — | — |
| CH00 | "Tiền thuê cả năm chỉ bằng khoảng ba phần trăm giá căn nhà." (L163) | OK | — | REFI cả nước 3,05% [1]; Batdongsan HN ~3% [2] (SECONDARY). |
| CH00 | "…sau thời gian ưu đãi, vào khoảng mười ba tới mười lăm phần trăm" (L164) | OK | — | VARS-IRE 13–15% [7]; DKRA 12–15% [6] (SECONDARY). |
| CH00 | "Vậy mà trong năm năm qua, người mua căn hộ ở Hà Nội lại thắng rất đậm." (L165) | OK | — | Savills ~26%/năm [5] ≫ hoà vốn 7,45% → cách nói chấp nhận được. 1,26⁵ = 3,18 ≈ "×3" ✓ (nhất quán). |
| CH00 | "Một bên trả ít hơn hẳn, bên kia lại giàu lên nhanh hơn." + lộ trình (L166–168) | OK | — | Lộ trình "Nghịch lý" ✓ (mục 2). |
| CH00 | Chào kênh, chuỗi, miễn trừ (L169–171) | OK | — | Luật 2 ✓; thẻ miễn trừ 4–5 giây phải có trên hình. |
| CH01 | "Cùng quý hai năm nay, có nguồn ghi khoảng sáu mươi triệu, có nguồn ghi hơn một trăm hai mươi triệu." (L177) | SỬA | "Cùng thời điểm, có nguồn ghi khoảng tám mươi triệu, có nguồn ghi hơn một trăm hai mươi triệu." | Số 60 (CBRE thứ cấp, qua báo) thấp bất thường so Bộ XD 123 cùng quý, chưa kiểm định nghĩa; 83 là quý III → bỏ "quý hai". Nếu kiểm được bản gốc CBRE thì giữ nguyên câu cũ. |
| CH01 | "…người đo căn mới, người đo căn cũ, người đo giá rao, người đo giá giao dịch thật." (L178) | OK | — | Đúng bản chất bốn nguồn [3][4][A1-76]. |
| CH01 | "Có một điều các nguồn khá thống nhất: hai quý liền, Hà Nội không có căn mới mở bán nào dưới sáu mươi triệu một mét vuông." (L179) | SỬA | "Theo một công ty tư vấn, hai quý liền, Hà Nội không có dự án mới nào mở bán dưới sáu mươi triệu một mét vuông." | Chỉ một nguồn (CBRE qua Tạp chí KTTC [4]); chưa tìm được nguồn thứ hai. "căn mới… nào" tuyệt đối hơn "hàng mới" của bài báo → "dự án mới". |
| CH01 | "Vì thế căn ví dụ của mình rẻ hơn mọi mức bình quân ấy." / ~50 m², căn nhỏ, xa, cũ (L180–181) | OK | — | 50 tr/m² < mọi mức ✓. |
| CH01 | Định nghĩa tỷ suất cho thuê (L183–184) | OK | (tuỳ chọn) "…chia cho giá căn nhà, chưa trừ chi phí" | Đây là tỷ suất **gộp** [hồ sơ §1]. |
| CH01 | HN ~2,3%, HCM ~3,3% (L185–186) | OK | — | REFI qua CafeBiz [1] — [chưa kiểm lại nguồn gốc]. |
| CH01 | "Năm 2023… Hà Nội… khoảng bốn tới năm phần trăm." (L187) | OK | — | REFI 4,2% [1]; Batdongsan 4,9–5% [2]. |
| CH01 | HỎI + "Vì giá bán chạy nhanh hơn giá thuê rất nhiều… lương không chạy kịp." (L188–190) | OK | — | Diễn giải từ [1][2]. "tăng gấp mấy lần" hơi mơ hồ — có thể nói "gấp khoảng ba lần" (Savills). |
| CH01 | 33 năm / 43 năm (L192–193) | OK | — | 1/0,03 = 33,3 · 1/0,0232 = 43,1 ✓. |
| CH01 | "…khoảng sáu triệu hai trăm năm mươi nghìn đồng mỗi tháng." (L194) | OK | — | 2.500 × 3% ÷ 12 = 6,25 ✓. |
| CH01 | "Chỉ riêng tiền thuê thì khó mà đủ, phần lãi họ kỳ vọng nằm ở chỗ giá nhà tăng." (L197) | SỬA | "Nhiều người cho thuê chấp nhận tiền thuê thấp, vì kỳ vọng giá nhà tăng." | Câu gốc là *[suy luận]* nói như sự thật về mọi chủ nhà; bản sửa đúng mức nguồn [1][2]. |
| CH01 | "Giữ ý này lại nhé…" (L198) | OK | — | Vòng mở 2 ✓. |
| CH02 | Trả trước 1 tỷ, vay 1,5 tỷ 25 năm (L203–204) | OK | — | Giả định; LTV 60%. |
| CH02 | "Tháng chín năm nay, lãi vay mua nhà thường được cố định trong một tới hai năm đầu." (L205) | OK | — | DKRA: cố định 12–24 tháng [6]. Lưu ý VARS-IRE ghi 6–12 tháng [7] → "thường" chấp nhận được. |
| CH02 | "…mười một ngân hàng… bình quân khoảng mười một phần trăm" (L206) | OK | — | 10,9% [6] (SECONDARY). |
| CH02 | Thả nổi = lãi cơ sở + biên độ 3,3–3,5; thực trả 13–15% (L207–210) | OK | — | [7] (SECONDARY). |
| CH02 | "Thử tính với kiểu trả phổ biến: gốc chia đều mỗi tháng, lãi tính trên số nợ còn lại." (L211) | SỬA | "Thử tính với một kiểu trả hay gặp: gốc chia đều mỗi tháng, lãi tính trên số nợ còn lại." | "phổ biến" chưa có nguồn định lượng (hồ sơ tự ghi CHƯA KIỂM). |
| CH02 | Gốc 5 tr; lãi T1 13,75; "gần mười chín triệu, tức hơn sáu phần mười thu nhập" (L212–214) | OK | — | 18,75 / 30 = 62,5% ✓. |
| CH02 | "Tới tháng thứ hai mươi tư, còn khoảng mười bảy triệu bảy." (L216) | OK | — | 17,696 ✓. |
| CH02 | T25 lãi 14% → "khoảng hai mươi mốt triệu một trăm nghìn" (L217–218) | OK | — | 21,100 ✓. |
| CH02 | "…thêm hơn ba triệu bốn, tức tăng gần một phần năm." (L219) | OK | — | +3,404 tr; +19,24% ✓. |
| CH02 | "Lúc này, bảy phần mười thu nhập đi thẳng vào ngân hàng." (L220) | OK | — | 70,3% ✓ (tháng 25; tháng 36 còn 68%, tháng 60 64%, tháng 120 52%). |
| CH02 | "…lãi cơ sở do ngân hàng điều chỉnh theo từng kỳ. Nó có thể lên, cũng có thể xuống." (L222–223) | OK | — | Không dự báo chiều ✓. |
| CH02 | 2025 ưu đãi 5,5–6,7%; năm nay cao hơn vài điểm (L224–225) | OK | — | [7]: 2026 8,2–11% → +2,7…+4,3 điểm ✓. |
| CH02 | Lãi 24 tháng ~317 tr; thuê ~154 tr (L226–227) | OK | — | 317,35 · 153,75 ✓. |
| CH03 | "Lệ phí trước bạ là không phẩy năm phần trăm." (L233) | OK | — | NĐ 10/2022 [13] (SECONDARY — chưa mở văn bản gốc lần này). |
| CH03 | Công chứng, thẩm định, đăng ký thế chấp; làm tròn 1% ≈ 25 tr (L234–235) | OK | — | 0,5% = 12,5 tr + công chứng ~2,5 tr (TT 257/2016, CHƯA KIỂM biểu phí mới) + thẩm định/đăng ký → "làm tròn" lên 1% hợp lý. |
| CH03 | "Nếu mua căn mới của chủ đầu tư, còn hai phần trăm kinh phí bảo trì, tính riêng ngoài giá bán." (L236) | SỬA | "Nếu mua căn mới của chủ đầu tư, còn khoản kinh phí bảo trì hai phần trăm, ghi riêng trong hợp đồng." | Luật Nhà ở: khoản 2% được tính vào tiền mua và ghi rõ trong hợp đồng (bảng giá thường ghi "chưa gồm KPBT") — "ngoài giá bán" dễ hiểu sai. [22] (SECONDARY). |
| CH03 | "…thuế thu nhập cá nhân là hai phần trăm giá bán, thường do người bán nộp." (L237) | OK | — | [12] (SECONDARY): nghĩa vụ của bên chuyển nhượng; "thường" vì hai bên có thể thoả thuận ✓. |
| CH03 | Phí quản lý HN 1.200–16.500 đ/m²/tháng (L239) | OK | — | QĐ 25/2026 qua VnEconomy [15] (SECONDARY). |
| CH03 | "…ai ở thì trả… nên mình để nó ra ngoài phép so." (L240) | OK | — | Đúng với mô hình. |
| CH03 | Sửa chữa ~0,5% giá trị/năm, giả định (L241–242) | OK | — | Đã nói "mình giả định" ✓. Độ nhạy: 0% → 6,90%; 1% → 8,00%. |
| CH03 | Người thuê: tiền thuê tăng; CPI thuê nhà 9T ~5% (L245–246) | OK | — | NSO +4,91% [11] ✓ (bằng chứng trong hồ sơ). |
| CH03 | Chuyển nhà, tốn tiền sức (L247–248) | OK | — | *[suy luận]*, không số liệu — cách nói đủ mềm. |
| CH03 | +5%/năm → "gần chín triệu bảy" (L249–250) | OK | — | 6,25 × 1,05⁹ = 9,696 ✓. |
| CH04 | 1 tỷ → 6,8% (4 NH lớn, 09/2026) → 68 tr/năm, ~5,7 tr/tháng; lãi tiền gửi cá nhân không chịu thuế (L256–259) | OK | — | [A1-83]; [16] (SECONDARY). 68/12 = 5,67 ✓. |
| CH04 | "Gần bằng nhau… riêng tiền lãi của khoản trả trước đã gần đủ trả tiền thuê" (L260–262) | OK | — | 5,67/6,25 = 91% ✓. |
| CH04 | "…khi tỷ suất cho thuê thấp hơn lãi tiết kiệm, đi thuê thường rẻ hơn, nếu chỉ tính tiền ra tiền vào." (L263) | OK | — | Đúng logic chi phí sử dụng nhà (chưa tính tăng giá) ✓. |
| CH04 | 8 năm: tiết kiệm ~1,56 tỷ; VN-Index ~1,78 tỷ chưa cổ tức; vàng ~3,9 tỷ đã trừ chênh lệch (L266–269) | OK | — | Tính lại: CSV 08/10/2018 đóng 996,12 → 30/09/2026 1.768,62 = ×1,7755 ✓; SJC bán 36,57 tr (02/10/2018) → mua vào 141,1 tr (30/09/2026) = ×3,858 ✓; tích lãi ROLL = ×1,562 (script 1,5607, chênh do cách tính kỳ) ✓. |
| CH04 | "Còn căn hộ Hà Nội, theo một công ty tư vấn bất động sản, giá nay cao gấp khoảng ba lần năm 2019." (L270) | SỬA | "Còn căn hộ Hà Nội, theo một công ty tư vấn bất động sản, tới cuối năm ngoái giá đã cao gấp khoảng ba lần năm 2019." | Savills nói ở 01/2026 về 2025 [5]; quý II/2026 thứ cấp đã giảm → "nay" sai kỳ. |
| CH04 | Đòn bẩy (L271) | OK | — | Màn hình đã có "và 100% phần giảm giá" ✓. |
| CH04 | 9 tháng 2026: tiết kiệm +3,9%; VN-Index hơi âm; vàng lỗ gần 8%; căn hộ cũ HN quý II −3% (L272–276) | OK | — | 5,2% × 9/12 = 3,9 ✓; 1.784,49 → 1.768,62 = −0,89% ✓ (CSV); SJC 152,8 → 141,1 = −7,66% ✓; CBRE −3% [4]. |
| CH04 | "…quá khứ không hứa gì cho mười năm tới." (L277) | OK | — | ✓ luật 2. |
| CH04 | "…giá nhà tăng đủ nhanh để gánh hết tiền lãi." (L278) | OK | — | — |
| CH05 | Cùng ngân sách; gửi 6,8%; 1 tỷ + 25 tr gửi từ đầu (L284–287) | OK | (tuỳ chọn) thêm sau L286: "Mức lãi gửi và lãi vay, mình giữ nguyên suốt mười năm." | Giả định giữ nguyên lãi là ẩn (mục 4a). |
| CH05 | "Tháng đầu, phần chênh… khoảng mười ba triệu rưỡi." (L288) | OK | — | 19,79 − 6,25 = 13,54 ✓. |
| CH05 | "Từ năm thứ ba, con số ấy lên khoảng mười lăm triệu." (L289) | SỬA | "Đầu năm thứ ba, khi khoản trả nhảy lên, con số ấy lên khoảng mười lăm triệu, rồi nhỏ dần." | T25 = 15,25; T120 chỉ còn 6,90 (g = 0). |
| CH05 | "Sau mười năm, nhà bên phải có khoảng bốn tỷ trong sổ tiết kiệm." (L290) | OK | — | 4,054 tỷ ✓. |
| CH05 | "…còn nợ ngân hàng chín trăm triệu." (L291) | OK | — | 900 ✓. |
| CH05 | Giá đứng yên → 1,55 tỷ; +3% → 2,4; +5% → 3,1 (L292–294) | OK | — | 1,550 · 2,393 · 3,091 ✓. "Nếu" = kịch bản, không dự báo ✓. |
| CH05 | "…khoảng bảy phẩy năm phần trăm mỗi năm, đều đặn suốt mười năm." (L296) | OK | — | 7,448% ✓. Nếu ghép lãi theo năm (đúng sổ 12 tháng) → 7,30%; vẫn "khoảng bảy rưỡi". |
| CH05 | "Đổi vài giả định, như lãi thả nổi, mức tăng tiền thuê hay số năm ở, con số này chạy từ hơn sáu tới hơn tám phần trăm." (L297) | SỬA | "Đổi vài giả định, như lãi thả nổi, lãi tiết kiệm, mức tăng tiền thuê hay số năm ở, con số này chạy từ hơn sáu tới hơn tám phần trăm." | Ba giả định đã nêu chỉ cho 6,64–8,08; 6,34 và 8,32 đến từ lãi gửi 5,2% / 8%. |
| CH05 | "Ở càng lâu thì mức hoà vốn càng thấp, vì đến một lúc nhà bên trái hết nợ, còn nhà bên phải vẫn trả tiền thuê." (L298) | SỬA | "Ở càng lâu thì mức hoà vốn càng thấp, vì phí mua bán được chia cho nhiều năm hơn, còn tiền thuê thì năm nào cũng tăng." | Vay 25 năm: ở 20 năm vẫn nợ 300 tr; chiều giảm (8,38 → 6,37 từ 3 → 25 năm) đến từ phí cố định và tiền thuê tăng. |
| CH05 | "…mua nhà là đặt cược rằng giá sẽ tăng nhanh hơn mức ấy." (L299) | OK | — | Trong khuôn ví dụ ✓. |
| CH05 | "Năm năm qua, giá căn hộ Hà Nội tăng nhanh hơn thế rất nhiều." (L300) | OK | — | 26%/năm [5]. |
| CH05 | "Năm nay thì chưa." (L301) | SỬA | "Còn năm nay, giá căn hộ cũ đã chững lại, quý hai còn giảm." | "chưa" ngầm dự báo; sai với sơ cấp (+21% y/y [4]). |
| CH05 | Giả định để dành đủ 120 tháng (L303) | OK | (tuỳ chọn) "…mỗi tháng khoảng gần một nửa thu nhập." | Phần chênh 13,5–15,3 tr = 45–51% thu nhập đầu kỳ — con số giúp người xem thấy độ khó. |
| CH05 | "…họ chỉ còn khoảng hai tỷ, là một tỷ trả trước cộng tiền lãi." (L305) | OK | (tuỳ chọn) "…một tỷ trả trước, phí mua cộng tiền lãi" | 1,025 × (1+0,068/12)¹²⁰ = 2,019 ✓. |
| CH05 | "…chỉ cần tăng chừng gần hai phần trăm…" (L306) | OK | — | 1,77% ✓. |
| CH05 | "…sau mười năm, họ đã trả sáu trăm triệu tiền gốc." (L307) | OK | — | ✓. |
| CH05 | "Thuê và đầu tư phần chênh chỉ thắng khi phần chênh thật sự được đầu tư." (L309) | SỬA | "Lợi thế của người thuê chỉ thành tiền khi phần chênh thật sự được để dành." | (a) mô hình chỉ gửi tiết kiệm, không "đầu tư"; (b) "chỉ thắng khi" sai tuyệt đối: nếu giá tăng < 1,77%/năm thì người thuê tiêu hết phần chênh vẫn hơn. |
| CH06 | Ổn định, sửa bếp, nuôi chó, gia hạn hợp đồng (L313–317) | OK | — | *[suy luận]*, đúng tinh thần hai mặt. |
| CH06 | "Sổ hộ khẩu giấy đã hết giá trị từ đầu năm 2023…" (L319) | OK | — | Luật Cư trú 2020 Đ38 k3 [21]. |
| CH06 | Nhà của mình không đòi diện tích; nhà thuê cần chủ nhà đồng ý + đủ diện tích/người (L320–321) | OK | — | Luật Cư trú Đ20 [17] (SECONDARY). |
| CH06 | "Ở nội thành Hà Nội, mức ấy là mười lăm mét vuông sàn mỗi người." (L322) | SỬA | "Ở Hà Nội, khu vực trung tâm còn đòi cao hơn, tới mười lăm mét vuông sàn mỗi người." | NQ 10/2023 định nghĩa theo quận; từ 01/07/2025 Hà Nội bỏ cấp quận → phạm vi "nội thành" chưa kiểm hiện trạng (Ghi chú tác giả cũng nêu). Giữ số 15 m², mềm phạm vi; nếu kiểm được văn bản 2025–2026 thì ghi đúng phạm vi. |
| CH06 | "Năm học này, lần đầu tiên Hà Nội xét tuyển mầm non, lớp một và lớp sáu theo nơi cư trú." (L324) | OK | — | VietNamNet + Báo Chính phủ 12/03/2026 [19] (SECONDARY) — [chưa mở kế hoạch gốc Sở GD&ĐT]. |
| CH06 | Câu trích » "nơi cư trú được hiểu có thể là thường trú hoặc tạm trú" (L325) | OK | — | Giới thiệu đúng là lời "một bài báo" ✓; kiểm nguyên văn trước khi dựng. |
| CH06 | TP.HCM xét theo nơi cư trú, ưu tiên riêng (L326) | OK | — | [20] ✓; cách nói đủ mềm. |
| CH06 | "…hãy đọc kế hoạch tuyển sinh của phường mình." (L327) | OK | — | Hành động kiểm tra, không khuyến nghị mua/thuê ✓. |
| CH06 | "Khi bảy phần mười thu nhập đã dành để trả nợ…" (L329) | OK | — | ✓ (tháng 25–~40). |
| CH06 | Người thuê dễ chuyển nhưng "chưa có chỗ của riêng mình"; "Chỉ bạn tự cân" (L330–332) | OK | — | Hai mặt ✓. |
| CH07 | Bốn "khi nào không đúng": gia đình cho tiền; Đà Nẵng ~4,3% → hoà vốn thấp hơn; căn đang xây; lãi đổi (L338–341) | OK | — | Đà Nẵng tính lại → 6,09% ✓ thấp hơn. Lãi 2025 (6%/10%) → 5,66%; nếu cả lãi gửi cũng 5,2% → 4,55% — câu định tính đúng. |
| CH07 | Sáu câu tự điền (L342–349) | OK | — | Danh sách 6 mục > 3 (checklist RETENTION) — chấp nhận vì có `ledger` hiện từng dòng; mỗi câu một nhịp. |
| CH07 | "Các công thức mình dùng nằm ở phần mô tả video…" (L350) | OK | — | **Điều kiện:** khối công thức (mục 4b) phải vào `youtube.more` trong spec, không vào danh sách nguồn (bị co tự động). Nếu không làm được → đổi câu thành "Cách tính, mình ghi tóm tắt ở phần mô tả." |
| CH07 | Hai cánh cửa: cược giá nhà / cược kỷ luật (L351–355) | OK | — | Cân bằng, không phán ✓. |
| CH07 | "Bài sau của chuỗi Quyết định lớn: trả góp không phần trăm, thật ra bạn trả lãi bao nhiêu?" (L356) | SỬA | "Chuỗi Quyết định lớn sẽ còn những phép tính như thế này, cho những khoản tiền lớn khác trong đời." | B2 có trong positioning §3B nhưng chưa có lịch/kịch bản → không hứa tên bài. |
| CH07 | Câu hỏi bình luận "bạn sẽ đứng sau cánh cửa nào, và vì sao?" (L357) | OK | — | Hỏi lựa chọn của người xem, không gợi ý ✓. |

### 1c. Chữ và cảnh trên màn hình (Kế hoạch hình ảnh)

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Màn hình CH00 | `ledger` MUA ≈ 18,75 · THUÊ ≈ 6,25 · thu nhập 30 tr (L43–44) | OK | — | ✓ + nhãn VÍ DỤ GIẢ ĐỊNH. |
| Màn hình CH00 | `kinetic` 3% → 13–15% (L46) | OK | — | ✓. |
| Màn hình CH00 | `counter` 26 %/NĂM "GIÁ CĂN HỘ HÀ NỘI · 5 NĂM QUA" (Savills) (L47) | OK | Sub: "Savills (qua Người Quan Sát, 01/2026) · tới 2025" | Nói rõ kỳ kết thúc 2025. |
| Màn hình CH00 | `slam` "NGHỊCH LÝ" / `brand` (L48–49) | OK | — | — |
| Màn hình CH01 | `bars` "GIÁ CĂN HỘ HÀ NỘI · QUÝ II/2026": CBRE thứ cấp 60 · CBRE sơ cấp 95 · giá rao quý III 83 · Bộ XD 123 (L52–53) | SỬA | Tiêu đề "GIÁ CĂN HỘ HÀ NỘI · GIỮA NĂM 2026 · TRIỆU Đ/M²"; bỏ cột CBRE thứ cấp 60 cho tới khi kiểm định nghĩa; giữ SƠ CẤP 95 (chưa VAT) · GIÁ RAO 83 (quý III) · GIAO DỊCH THỨ CẤP 123 + chú thích "CÙNG THÀNH PHỐ, KHÁC CÁCH ĐO" | Trộn kỳ (quý III trong biểu đồ quý II); 60 vs 123 cùng phân khúc thứ cấp, cùng quý — nghi khác định nghĩa. |
| Màn hình CH01 | `kinetic` "2 QUÝ LIỀN: KHÔNG CĂN MỚI NÀO DƯỚI 60 TR/M²" (L54) | SỬA | "2 QUÝ LIỀN: KHÔNG CÓ HÀNG MỚI MỞ BÁN DƯỚI 60 TR/M² (CBRE)" | Theo L179. |
| Màn hình CH01 | `ledger` căn ví dụ ~50 m² · ~50 tr/m² · 2,5 tỷ (L55) | OK | — | — |
| Màn hình CH01 | `bars` tỷ suất 2,32 · 3,30 · 4,34 · 3,05; ghi chú HN 2023 ≈ 4–5% (L57–58) | OK | — | [1][2] (SECONDARY). |
| Màn hình CH01 | `counter` 33 năm; sub 43 năm; `ledger` 6,25 tr (L60–61) | OK | — | ✓. |
| Màn hình CH02 | `ledger` lãi vay 2026 (DKRA, VARS-IRE) (L66–67) | OK | (tuỳ chọn) đưa tên tổ chức xuống dòng nguồn | Tên đơn vị nghiên cứu là nguồn, không phải ngân hàng ✓. |
| Màn hình CH02 | `kinetic` gốc đều; `counter` 18,75 ≈ 62% (L68–69) | OK | — | ✓. |
| Màn hình CH02 | `bars` khoản trả T1…T120 (L70–71) | OK | — | 18,75 · 18,25 · 17,70 · 21,10 · 20,46 · 19,06 · 15,56 ✓. |
| Màn hình CH02 | `slam` "+3,4 TRIỆU / THÁNG" ≈ +19% (L72) | OK | — | ✓. |
| Màn hình CH02 | `counter` 70% "THU NHẬP ĐI VÀO NGÂN HÀNG · TỪ THÁNG 25" (L73) | SỬA | "… · THÁNG 25" | "TỪ" ngụ ý kéo dài; tháng 36 còn 68%, tháng 60 64%. |
| Màn hình CH02 | `bars` lãi ưu đãi 2025 6,1 / 2026 9,6 (giữa dải) (L76–77) | OK | — | Cột = điểm giữa dải, có chú thích dải ✓. |
| Màn hình CH02 | `ledger` 24 tháng: lãi ≈ 317 · thuê ≈ 154 (L78) | OK | — | ✓. |
| Màn hình CH03 | `ledger` "KHI MUA" … "+ KINH PHÍ BẢO TRÌ 2%" (L81–82) | OK | — | Thêm chữ nhỏ "CHƯA GỒM TRONG VÍ DỤ" (ví dụ gốc không cộng 2%; nếu cộng → hoà vốn 7,66%). |
| Màn hình CH03 | `ledger` "KHI BÁN": thuế TNCN 2% (L83) | OK | — | [12]. |
| Màn hình CH03 | `kinetic` phí quản lý; sửa chữa 0,5% (L84–87) | OK | — | ✓. |
| Màn hình CH03 | `ledger` giá của người thuê; `bars` 6,25 · 7,24 · 8,38 · 9,70 (L89–91) | OK | — | 6,25 × 1,05³ = 7,24; ×1,05⁶ = 8,38; ×1,05⁹ = 9,70 ✓. |
| Màn hình CH04 | `ledger` 1 tỷ, 6,8%, 5,67 tr; "MIỄN THUẾ TNCN" (L96–97) | OK | — | ✓. |
| Màn hình CH04 | `race` 8 năm + nguồn (L101–104) | OK | — | Tính lại ✓ (mục 1b L266–269). |
| Màn hình CH04 | `counter` ×3 so 2019 (L105) | OK | Sub thêm "· TỚI 2025" | Theo L270. |
| Màn hình CH04 | `race` 9 tháng 2026 + CBRE −3% (L107–108) | OK | — | ✓. |
| Màn hình CH05 | `counter` 13,5 tr; sub "TỪ THÁNG 25: ≈ 15,3 TR" (L115) | SỬA | sub "THÁNG 25: ≈ 15,3 TR · THÁNG 120: ≈ 6,9 TR" | Như L289. |
| Màn hình CH05 | `ledger` 4,05 tỷ; 1,55 · 2,39 · 3,09 (L116–117) | OK | — | ✓. |
| Màn hình CH05 | `slam` "≈ 7,5% / NĂM" sub "ĐỀU ĐẶN 10 NĂM · KÊNH TỰ TÍNH · VÍ DỤ GIẢ ĐỊNH" (L119) | SỬA | sub thêm dòng thứ hai: "GIỮ NGUYÊN LÃI VAY 14%, LÃI GỬI 6,8%, THUÊ +5%/NĂM · CHƯA GỒM MÔI GIỚI, NỘI THẤT" | Hiện giả định ẩn ngay trên cảnh mạnh nhất (mục 4a). |
| Màn hình CH05 | `bars` độ nhạy 6,64 · 6,89 · 7,06 · 7,45 · 7,72 · 8,08 · 8,08 (L120–121) | OK | (tuỳ chọn) thêm "LÃI GỬI 5,2% 6,34 · LÃI GỬI 8% 8,32" để khớp lời đọc "hơn sáu tới hơn tám" | Từng số tính lại khớp. |
| Màn hình CH05 | `kinetic` "MUA = ĐẶT CƯỢC…" + "5 NĂM QUA ≈ 26%/NĂM · QUÝ II/2026: −3%" (L122) | OK | "…QUÝ II/2026: CĂN CŨ −3% SO QUÝ I" | Nói rõ phân khúc. |
| Màn hình CH05 | `ledger` 2,02 tỷ → 1,8%; `counter` 600 tr; `slam` "PHẦN CHÊNH PHẢI ĐƯỢC ĐẦU TƯ THẬT · THÌ THUÊ MỚI THẮNG" (L124–126) | SỬA | `slam` "PHẦN CHÊNH PHẢI ĐƯỢC ĐỂ DÀNH THẬT" sub "LỢI THẾ CỦA NGƯỜI THUÊ NẰM Ở ĐÓ" | Như L309. |
| Màn hình CH06 | `date` 01/01/2023; `ledger` thường trú … "HÀ NỘI NỘI THÀNH ≥ 15 M² (NQ 10/2023/NQ-HĐND)" (L131–133) | SỬA | "HÀ NỘI: KHU VỰC TRUNG TÂM ≥ 15 M² (NQ 10/2023/NQ-HĐND · KIỂM PHẠM VI SAU SẮP XẾP 2025)" — hoặc giữ nếu kiểm được phạm vi hiện hành | Như L322. |
| Màn hình CH06 | `kinetic` tuyển sinh; `quote` VietNamNet; `kinetic` TP.HCM; `counter` 70%; `slam` (L134–138) | OK | `counter` sub "THÁNG 25" như CH02 | — |
| Màn hình CH07 | `ledger` khi nào không đúng; 6 câu; "CÔNG THỨC: XEM MÔ TẢ VIDEO" (L141–145) | OK | — | Điều kiện mục 4b. |
| Màn hình CH07 | `kinetic` "QUYẾT ĐỊNH LỚN · BÀI 2 · TRẢ GÓP 0%…" (L148) | SỬA | "QUYẾT ĐỊNH LỚN · CÒN TIẾP" | Như L356. |

## 2. Kiểm luật kênh (positioning mục 1) và RETENTION

| Luật | Kết quả |
|---|---|
| 1. Không bán gì / không tên ngân hàng, chủ đầu tư, dự án | OK — lời đọc không có tên ngân hàng/chủ đầu tư/dự án/công ty tư vấn ("một khảo sát ở mười một ngân hàng", "một đơn vị nghiên cứu thị trường", "một công ty tư vấn"). Trên màn hình chỉ có tên đơn vị **nguồn** (CBRE, Savills, REFI, DKRA, VARS-IRE, Batdongsan.com.vn, Bộ XD, NSO) — đúng quy ước "tên tổ chức nguồn ở dòng nguồn". Tuỳ chọn: đưa tên ra khỏi nhãn cột (`bars` CH01) xuống dòng "Dữ liệu: …". `broll` dặn không lộ tên toà nhà ✓. |
| 2. Không dự báo / không khuyến nghị | Gần đạt. Giá nhà tăng chỉ xuất hiện dạng "nếu" (L292–296) ✓; L171 miễn trừ ✓; kết "không bên nào chắc thắng" ✓. **Hai chỗ sửa:** L301 "Năm nay thì chưa" (ngầm dự báo); L309 "chỉ thắng khi" (phán quyết tuyệt đối, cũng sai số học). Tiêu đề (1)(3) có màu phán quyết nhẹ → chọn (2). |
| 3. Mọi số có nguồn | Có; số tự tính đều tính lại khớp (mục 4). Nói quá nguồn: L179 ("các nguồn khá thống nhất"), L211 ("phổ biến"), L270 ("nay"). Số thị trường còn SECONDARY (mục 6). |
| 4. Nói cả mặt trái | Có cho cả hai bên: người mua (lãi nhảy, 70% thu nhập, phí, sửa chữa, đòn bẩy hai chiều, mất việc); người thuê (tiền thuê tăng, chuyển nhà, kỷ luật, cảm giác chưa có chỗ riêng, thường trú cần chủ nhà đồng ý). CH07 "khi nào không đúng" ✓. Thiếu: giả định ẩn của mô hình (mục 4a) → thêm sub ở `slam` CH05. |
| 6. Dữ liệu quá khứ | Kỳ đã đóng (quý II, 30/09/2026) ✓. |
| Giọng tôn trọng | OK — câu trả lời quen tai "mua chứ" được tôn trọng (L161, L265 "Đúng, và dữ liệu cũng cho thấy vậy"); không chê người thuê hay người mua. |
| RETENTION — lời hứa lộ trình | OK. Hình thức **"Nghịch lý"** (L163–168: 3% vs 13–15% vs người mua thắng đậm → "điều gì phải đúng để mỗi cánh cửa thắng"). Các video CK trước: A1 và C1 "ba câu hỏi", D1 "thử đoán", C2 (liền trước) "bản đồ bằng hình" → **không lặp** ✓; "Nghịch lý" chưa dùng ở kênh CK (chỉ là ví dụ MIM trong RETENTION) ✓. Đã ghi ở mục Giữ chân ✓. |
| RETENTION — khác | 3 vòng mở đóng đúng chỗ (CH00→CH05, CH01→CH04, CH04→CH05) ✓; motif hai cánh cửa ≥ 3 lần ✓; cảnh mạnh ~75% (CH05) ✓; re-hook ~50% (L279) ✓. Danh sách > 3 mục: L338–341 (4 điều kiện) và L342–349 (6 câu) — chấp nhận vì mỗi mục là một câu riêng có `ledger`. Lưu ý chuỗi: positioning §3B **B3** "Vay mua nhà lãi ưu đãi 2 năm: chuyện gì xảy ra năm thứ 3?" trùng gần hết CH02 của B1 → nếu làm B3 cần góc khác. |

## 3. TTS — chỗ dễ đọc sai

| Chỗ | Rủi ro | Gợi ý (chỉ trong bản gửi TTS) |
|---|---|---|
| "VN-Index" (L268, L274) | Gạch nối, đánh vần | Bảng `SAY` "Vi En In-đéc" như A1/C1. |
| "một nghìn hai tới mười sáu nghìn rưỡi đồng" (L239, 31 âm tiết — dài nhất) | "một nghìn hai" có thể nghe thành 1.002; câu dài | "một nghìn hai trăm tới mười sáu nghìn năm trăm đồng"; tách câu sau "thang máy". |
| "sáu triệu hai", "năm triệu bảy", "mười bảy triệu bảy", "ba triệu bốn" | Cách nói tắt — TTS đọc đúng chữ, người nghe hiểu ✓ | Giữ. |
| "phẩy" (nhiều chỗ) | Ổn | Nghe thử "hai phẩy ba", "bốn phẩy ba". |
| L325 `»` giữa dòng ("…ghi rõ: » nơi cư trú…") | Đổi giọng giữa câu; engine có thể tách sai | Tách thành hai dòng: dòng dẫn (Ngọc Huyền) + dòng trích (Xuân Vĩnh, radio). |
| "Đà Nẵng", "Biểu Đồ Biết Nói", "tạm trú/thường trú" | Ổn | Nghe thử. |
| "‖", "HỎI:", "»" | Đọc ra thành tiếng | Lọc trước TTS (Ghi chú đã nêu ✓). |
| Chữ số trong lời thoại | Không có chữ số nào ở L155–357 (đã quét) ✓; câu dài nhất 31 âm tiết (< 35) ✓ | — |

## 4. Tính lại các số trong "Ghi chú"

Mô hình độc lập (scratchpad `b1_model.py`): mỗi tháng m, người mua chi C_m = khoản trả (gốc đều 5 tr + dư nợ × lãi/12; 11% tháng
1–24, 14% từ tháng 25) + V·(1+g)^((m−1)/12)·0,5%/12; người thuê W₀ = 1.025 tr, W_m = W_{m−1}·(1+6,8%/12) + (C_m − thuê_m), thuê_m =
6,25·1,05^⌊(m−1)/12⌋; sau N năm: mua = V·(1+g)^N·0,98 − dư nợ; hoà vốn = nghiệm g (chia đôi).

| Mục Ghi chú | Kết quả tính lại / đối chiếu | Kết luận |
|---|---|---|
| Thuê 6,25; năm 10 9,70; 33,3 / 43,1 / 30,3 năm | 6,25 · 9,696 · 33,3 · 43,1 · 30,3 | OK |
| T1 18,75 (62,5%) · T12 18,25 · T24 17,70 · T25 21,10 (70,3%) · +3,40 (+19,2%) · T36 20,46 · T60 19,06 · T120 15,56 | 18,750 · 18,246 · 17,696 · 21,100 · +3,404 (+19,24%) · 20,458 · 19,058 · 15,558; 62,5% · 70,3% | OK |
| Lãi 24 tháng 317,4; thuê 24 tháng 153,75 | 317,35 · 153,75 | OK |
| 1 tỷ × 6,8% = 5,67 tr/tháng | 5,667 | OK |
| 8 năm: ×1,5607 · ×1,7755 · ×3,858 | ROLL ×1,5622 (chênh nhỏ, cách tính kỳ) · 996,12 → 1.768,62 = ×1,7755 · 36,57 → 141,1 = ×3,858 | OK |
| 9 tháng: +3,89% · −0,89% · −7,66% | 3,90 · −0,889 · −7,66 | OK |
| 10 năm: W₁₂₀ 4,05 · dư nợ 0,90 · mua 1,55 / 2,39 / 3,09 | 4,054 · 0,900 · 1,550 / 2,393 / 3,091 (g = 7,5%: 4,150 vs 4,126; g = 10%: 5,455 vs 4,157 — khớp bảng hồ sơ) | OK |
| Phần chênh T1 13,54 · T25 15,25 | 13,54 · 15,25 · **T120 6,90** (không có trong Ghi chú) | OK (bổ sung T120 cho L289) |
| Hoà vốn 7,45% | 7,448% | OK |
| Độ nhạy: thuê +8% 7,06 · lãi gửi 5,2/5,7/8% 6,34/6,68/8,32 · tỷ suất 2,32/3,3% 8,08/7,16 · thả nổi 12/15% 6,89/7,72 · 5 năm 8,08 · 20 năm 6,64 · bỏ thuế bán 7,23 · lãi 2025 5,66 | 7,06 · 6,34 / 6,68 / 8,32 · 8,08 / 7,16 · 6,89 / 7,72 · 8,08 · 6,64 · 7,23 · 5,66 | OK, từng số |
| Tiêu hết phần chênh: 2,02 tỷ → 1,77% | 2,019 · 1,768% | OK |
| Gốc đã trả 600 tr; chi 10 năm người mua ~2,32 tỷ, người thuê ~0,94 tỷ | 600 · 2,322 · 0,943 | OK |
| Phụ lục niên kim 14,70 → 17,93 (+22%) | 14,70 · dư nợ T24 1.474,6 · 17,93 (+22,0%) | OK |

### 4a. Giả định ẩn / không thực tế — độ nhạy bổ sung (kênh tự tính, không có trong hồ sơ)

| Giả định trong ví dụ | Thực tế hơn | Hoà vốn | Người xem có được nói? |
|---|---|---|---|
| Gửi 6,8% ghép lãi **tháng** (lãi thực 7,02%) | Sổ 12 tháng ghép **năm** | 7,30% (−0,15) | Không |
| Lãi vay 14% và lãi gửi 6,8% giữ nguyên 8–10 năm | Đổi theo chu kỳ (2025: ưu đãi 6%, thả nổi 10%, gửi ~5,2%) | 4,55% nếu cả hai về mức 2025 | Một phần (CH07 định tính) |
| Không môi giới khi bán | +1% giá bán | 7,56% | Không (Ghi chú có) |
| Không kinh phí bảo trì 2% | Căn mua của chủ đầu tư | 7,66% | Có nhắc 2% (CH03), không nói ví dụ bỏ qua |
| Gốc đều | Niên kim | 7,90% | Không |
| Tiền thuê +5%/năm độc lập với giá nhà | Ở g = 0, tỷ suất năm 10 lên 4,65%; ở g = 7,45%, xuống 2,29% | — | Không |
| Người thuê để dành 13,5–15,3 tr/tháng (45–51% thu nhập) | Mức tiết kiệm rất cao | Tiêu hết → 1,77% | Có (CH05), nhưng không nói % thu nhập |
| Thu nhập 30 tr không đổi 10 năm; 62–70% thu nhập trả nợ | Ngân hàng có thể không duyệt tỷ lệ này (chưa kiểm quy định/thực tế) | — | CH06 nói "sức chịu đựng" |
| Tỷ suất 3% | HN 2,32% / Đà Nẵng 4,34% | 8,08% / 6,09% | Có |
| Ở 3 / 15 / 25 năm | — | 8,38 / 6,99 / 6,37% | Có (5, 20 năm) |

→ Kết luận định tính của video (mua = cược giá tăng ~6–8%/năm; thuê = cược kỷ luật) **đứng vững** trước mọi biến thể trên. Chỉ cần
sub ở `slam` CH05 (mục 1c) để không giấu giả định.

### 4b. Khối công thức cho mô tả YouTube (486 ký tự — đặt trong `youtube.more` của spec, không vào danh sách nguồn)

`describe.py` đặt `meta["more"]` trước mục chương và chỉ co **danh sách nguồn** cho vừa 4.900 ký tự → khối này luôn còn nguyên.

```
🧮 CÔNG THỨC (ví dụ giả định trong video · kênh tự tính · thay bằng số của bạn)
• Tỷ suất cho thuê = tiền thuê 1 năm ÷ giá nhà
• Trả gốc đều: gốc/tháng = khoản vay ÷ số tháng; lãi/tháng = dư nợ × lãi năm ÷ 12
• Người thuê, mỗi tháng: Sổ = Sổ tháng trước × (1 + lãi gửi ÷ 12) + (trả ngân hàng + sửa chữa − tiền thuê); sổ ban đầu = tiền trả trước + phí mua
• Người mua sau N năm = giá nhà × (1 + g)^N × (1 − 2% thuế bán) − dư nợ
• Hoà vốn = mức g làm hai bên bằng nhau (ví dụ: ≈ 7,45%/năm)
```

Nếu không chèn được khối này → đổi L350 thành "Cách tính, mình tóm tắt ở phần mô tả video." và `kinetic` CH07 "CÁCH TÍNH: XEM MÔ TẢ".

**Ghi chú "Cần kiểm lại" — trả lời:** báo cáo gốc CBRE/REFI/Savills/VARS-IRE/DKRA: chưa mở (vẫn SECONDARY) · "các nguồn khá thống
nhất": không có nguồn thứ hai → đổi "Theo một công ty tư vấn" (L179) · CBRE 60 tr/m²: bỏ cột, lời đọc "tám mươi… hơn một trăm hai mươi"
(L177) · "kiểu trả phổ biến" → "một kiểu trả hay gặp" (L211) · phí công chứng: lời đọc không nói số ✓ · trước bạ 0,5%, miễn thuế lãi
gửi, 2% TNCN: khớp hồ sơ, chưa đối chiếu điều khoản gốc · "phần lãi họ kỳ vọng" → dùng câu tác giả đề xuất (L197) · TP.HCM: giữ câu
mềm ✓ · câu trích VietNamNet: giữ "một bài báo" ✓ · 15 m²: mềm phạm vi (L322) · "thắng rất đậm": **xác nhận** (26%/năm ≫ 7,45%) ·
mô hình đơn giản hoá: thêm sub (mục 1c) · công thức mô tả: mục 4b · bài sau: câu chung (L356) · TTS: mục 3.

## 5. Nguồn đã dùng trong lần fact-check này

- Hồ sơ B1 (các nguồn [1]–[24], [A1-n]) — đối chiếu nội bộ, chưa mở lại từng link.
- `data/ck/vnindex_1d.csv`: 08/10/2018 đóng 996,12 · 31/12/2025 đóng 1.784,49 · 30/09/2026 đóng 1.768,62.
- `motion/long/chartdata._series('sjc')`: 02/10/2018 (36,42 / 36,57) · 31/12/2025 (150,8 / 152,8) · 30/09/2026 (141,1 / 144,1) triệu/lượng.
- `motion/long/describe.py` (DESC_CAP 4.900; `fit_sources` co danh sách nguồn; `meta["more"]` giữ nguyên).
- `2026-10-06-positioning.md` §1 (7 luật), §3B (B2 trả góp 0%, B3 lãi ưu đãi năm thứ 3 — chưa có lịch).
- `motion/long/RETENTION.md` "Lời hứa lộ trình"; script `Giữ chân` của A1, C1, C2, D1.

## 6. Việc còn mở (cần làm trước bản 2)

- **CBRE Hà Nội quý II/2026** bản gốc: định nghĩa giá thứ cấp ~60 tr/m² (so Bộ XD 123); câu "không có hàng mới dưới 60 tr/m²" + nguồn thứ hai.
- **REFI** tỷ suất cho thuê quý II/2026 — bản gốc hoặc báo thứ hai.
- **Savills** "+200% so 2019", "26%/năm" — sơ cấp hay thứ cấp.
- **DKRA / VARS-IRE** — bản gốc; tỷ lệ áp dụng "gốc đều" vs niên kim.
- **Luật 109/2025/QH15**: điều khoản miễn thuế lãi tiền gửi cá nhân và thuế 2% chuyển nhượng BĐS (văn bản gốc); **Luật Nhà ở 2023 Đ152**
  (2%, cách ghi trong hợp đồng); **NĐ 10/2022** + sửa đổi 2025 (0,5%, giá tính); biểu phí công chứng sau Luật Công chứng 2024.
- **Cư trú Hà Nội**: NQ 10/2023 còn hiệu lực? phạm vi "nội thành" sau bỏ cấp quận 01/07/2025; có NQ mới theo Luật Thủ đô 2024 chưa.
- **Kế hoạch tuyển sinh 2026–2027 của Sở GD&ĐT Hà Nội** (số hiệu, ngày; câu "thường trú hoặc tạm trú"; thứ tự ưu tiên thường trú/tạm trú); TP.HCM tương tự.
- Tiền gửi 12 tháng Big4 6,8% (09/2026) và 5,2% (01/2026); CPI thuê nhà +4,91% (đọc PDF NSO).

## 9. Kiểm nguồn gốc (lượt 2)

Ngày kiểm: 07/10/2026. Lượt này mở lại nguồn cho các dòng **[chưa kiểm lại nguồn gốc]** và mục 6 "Việc còn mở". Gom từ ba nguồn: (a) tự mở
trong lượt này: Luật 109/2025/QH15 bản Công báo số 37 ngày 22/01/2026 (PDF trên legalzone.vn; đã đọc Điều 4, 14, 24, 29), Tạp chí KTTC
07/07/2026, VietnamFinance 07/07/2026, VnEconomy bản tiếng Anh 08/07/2026, VietnamNews (CBRE quý IV/2024, để xem CBRE định nghĩa giá), CafeF
14/08/2026 (Savills), CafeBiz 29/08/2026 (REFI), Dân trí 03/09/2026 (DKRA), VnExpress 02/09/2026 (Bộ XD), Điều 152 Luật Nhà ở 2023 (nguyên
văn qua thuvienphapluat); (b) báo cáo của **helper số liệu thị trường**; (c) báo cáo của **helper luật/tuyển sinh** (mở qua bản sao vì
thuvienphapluat trả 403). Riêng **cbre.vn / cbre.com / mktgdocs.cbre.com không phân giải được tên miền**, còn REFI và Savills không có bản
gốc công khai → các số đó vẫn là **[SECONDARY]**, nhưng nay đã khớp nguyên văn với ít nhất một bài báo dẫn lại.

**Kết luận lượt 2:** xác nhận 17 · **SỬA mới: 6 lời đọc + 8 chữ/cảnh trên màn hình** · **rút lại 2 SỬA của lượt 1** (L177, L236) ·
không kiểm được tới bản gốc 4 (đã có câu mềm hơn hoặc nhãn nguồn).

### 9.1 Giá căn hộ Hà Nội (CBRE ~60 · sơ cấp ~95 · Bộ XD ~123) và câu "hai quý liền"

| Mục | Kết quả nguồn | Kết luận lượt 2 |
|---|---|---|
| CBRE thứ cấp ~60 tr/m², quý II/2026 | CBRE họp báo 07/07/2026 (TC KTTC, VietnamFinance, VnEconomy, VietnamNews): giá bán trung bình thứ cấp **giảm gần 3% so quý trước, còn khoảng 60 tr/m²** (Cafeland ghi −2,5%), lần giảm theo quý đầu tiên từ cuối 2022. Bản quý II **không in định nghĩa**. Quy ước CBRE ở các bản trước (VietnamNews, quý IV/2024): giá **trên m² diện tích sàn bán được (NSA ≈ thông thủy), chưa VAT, chưa phí**; thứ cấp tính trên rổ dự án CBRE theo dõi. → 60 là **giá thứ cấp trung bình theo CBRE** (m² thông thủy, chưa VAT), **không cùng thước đo** với Bộ XD | **Xác nhận** số và kỳ (quý II). Định nghĩa: [chưa kiểm tới bản gốc CBRE], suy theo quy ước CBRE |
| CBRE sơ cấp ~95 tr/m² | Nguyên văn TC KTTC: "khoảng 95 triệu đồng/m2 (chưa bao gồm VAT, phí bảo trì và trước chiết khấu)", +12% q/q, +21% y/y | **Xác nhận** |
| Bộ XD ~123 tr/m² | VnExpress 02/09/2026: "giá căn hộ bình quân khoảng 123 triệu đồng mỗi m2, giảm gần 3,9%"; TP.HCM "giá thứ cấp chung cư bình quân khoảng 108". Bài Báo Chính phủ 21/08 [3] **không có số giá**. Theo helper, −3,9% / −3,6% là báo tự suy từ quý I (128 / 112) | **Xác nhận** số 123 (thứ cấp, bình quân). −3,9% chỉ ở Ghi chú → ghi "theo báo dẫn Bộ XD" |
| Batdongsan giá rao | Theo helper: quý III so với quý I/2026 là **87 → 84 tr/m²** (−3%) | **SỬA** số trên màn: 83 → **84** |
| "Hai quý liền… không có… dưới 60 tr/m²" | CBRE: "quý thứ hai liên tiếp thị trường không xuất hiện dự án mới có giá dưới 60 triệu đồng/m2" (VietnamFinance; VnEconomy: "excluding VAT, maintenance fees and discounts"). **Có nguồn thứ hai độc lập**: Savills quý II/2026 (CafeF 14/08/2026): "toàn bộ nguồn cung sơ cấp trên thị trường Hà Nội hiện đều có giá trên 70 triệu đồng/m²" (giá sơ cấp trung bình theo Savills ≈ 116 tr/m²) | **Xác nhận**: nói "các nguồn" là có cơ sở, nhưng "hai quý liền" chỉ CBRE nói |

**Lời đọc:**
- **L177** "Cùng quý hai năm nay, có nguồn ghi khoảng sáu mươi triệu, có nguồn ghi hơn một trăm hai mươi triệu." → **giữ nguyên câu gốc,
  rút lại SỬA của lượt 1** (60 và 123 đều là quý II/2026, đều có nguồn). L178 giải thích "khác cách đo" là đủ.
- **L179 — SỬA (thay câu lượt 1):** "Có một điều hai công ty tư vấn cùng ghi nhận: quý hai năm nay, Hà Nội không có căn mới mở bán nào dưới
  sáu mươi triệu một mét vuông." (31 âm tiết). Nếu muốn giữ "hai quý liền" thì dùng câu lượt 1 ("Theo một công ty tư vấn, hai quý liền…").

**Màn hình:**
- **`bars` CH01 (L52–53) — SỬA (thay khuyến nghị lượt 1):** được giữ lại cột CBRE 60, nhãn "THỨ CẤP · GIÁ TB THEO CBRE (M² THÔNG THỦY,
  CHƯA VAT)" · "SƠ CẤP · CBRE (CHƯA VAT, TRƯỚC CHIẾT KHẤU)" 95 · "GIÁ RAO CHUNG CƯ · QUÝ III (Batdongsan.com.vn)" **84** · "BÌNH QUÂN THỨ
  CẤP (BỘ XD, QUA BÁO)" 123. Tiêu đề "GIÁ CĂN HỘ HÀ NỘI · GIỮA NĂM 2026 · TRIỆU Đ/M²" (vì có cột quý III), chú thích "CÙNG THÀNH PHỐ, KHÁC
  CÁCH ĐO · KHÔNG SO TRỰC TIẾP".
- **`kinetic` CH01 (L54) — SỬA:** "QUÝ II/2026: KHÔNG CÓ CĂN MỚI MỞ BÁN DƯỚI 60 TR/M²" + chữ nhỏ "CBRE: QUÝ THỨ 2 LIÊN TIẾP (CHƯA VAT) ·
  SAVILLS: MỌI HÀNG SƠ CẤP TRÊN 70 TR/M²".

### 9.2 Tỷ suất cho thuê, Savills, lãi vay, kiểu trả

| Mục (dòng) | Kết quả nguồn | Kết luận lượt 2 |
|---|---|---|
| REFI quý II/2026 HN 2,32 · HCM 3,30 · ĐN 4,34 · cả nước 3,05 (L185–186, L339, `bars` L57) | Nguyên văn CafeBiz 29/08/2026: "lợi suất căn hộ bình quân cả nước giảm còn 3,05%; Hà Nội thấp nhất ở mức 2,32%, TP.HCM 3,30%, trong khi Đà Nẵng… tăng lên 4,34%"; HN 2023 "khoảng 4,2%". Báo cáo REFI gốc không công khai; theo helper chỉ có một bài (CafeBiz, lấy từ Markettimes) | **Không kiểm được tới bản gốc** → giữ lời đọc mềm "theo một đơn vị nghiên cứu thị trường" (đã có ✓); nguồn trên màn "REFI, qua CafeBiz 29/08/2026 · một nguồn" |
| Batdongsan HN ≈ 3% (04/2026), 4,9–5% đầu 2023 | Theo helper: khớp (Báo Xây dựng 15/04/2026) | **Xác nhận** — L187 "bốn tới năm" ✓ |
| Savills ~26%/năm, "×3 so 2019" (L165, L270, `counter` L47, L105) | Theo helper: Người Quan Sát 16/01/2026 (lời bà Đỗ Thị Thu Hằng): ~26%/năm trong 5 năm, "cao hơn 200% so với 2019" → **mốc cuối là năm 2025**; không nói sơ cấp hay thứ cấp | **Xác nhận** số; SỬA L270 của lượt 1 vẫn giữ ("…tới cuối năm ngoái giá đã cao gấp khoảng ba lần…", 32 âm tiết). Sub màn hình "SAVILLS · 2019 → 2025" |
| DKRA 10,9% (L206, `ledger` L66) | Nguyên văn Dân trí 03/09/2026: "lãi suất vay mua nhà đối với khoản cố định 12-24 tháng tại 11 ngân hàng thương mại **phổ biến ở mức 10,9%** một năm"; chữ "bình quân khoảng 11%" chỉ ở **sapo của báo**, không phải lời DKRA. "12–15%" sau ưu đãi là lời của báo | **SỬA**: "bình quân" → "phổ biến" |
| VARS-IRE biên 3,3–3,5, thực trả 13–15% (L164, L207–210) | Theo helper: VnExpress 04/08/2026 xác nhận "khoảng 3,3–3,5%" và 13–15%; **mức ưu đãi 2026 là 8,5–11%** (không phải 8,2), cố định 6–12 tháng; 2025: 5,5–6,7% ✓ | Lời đọc **xác nhận**; **SỬA** `bars` L76: dải 2026 "8,5–11" → cột **9,75** (thay cho 8,2–11 → 9,6). L225 "cao hơn vài điểm" vẫn đúng |
| Gốc đều (dư nợ giảm dần) là kiểu phổ biến? (L211) | Theo helper: báo ghi dư nợ giảm dần "thường áp dụng" (VietNamNet 13/03/2026 có công thức gốc đều); không có số liệu tỷ lệ | **Không kiểm được tỷ lệ** → giữ SỬA lượt 1: "Thử tính với một kiểu trả hay gặp: …" |

**Lời đọc — SỬA mới:**
- **L206:** "Một khảo sát ở mười một ngân hàng cho mức phổ biến khoảng mười một phần trăm một năm." (19 âm tiết)

**Màn hình — SỬA mới:** `ledger` L66 "BÌNH QUÂN ≈ 10,9%" → "PHỔ BIẾN ≈ 10,9% (DKRA, 11 NH, CỐ ĐỊNH 12–24 THÁNG)" · `bars` L76 "2026 ·
8,5–11 → cột 9,75". Hồ sơ dòng [7] sửa 8,2 → 8,5.

### 9.3 Luật và phí

| Mục (dòng) | Văn bản gốc | Kết luận lượt 2 |
|---|---|---|
| Miễn thuế lãi tiền gửi cá nhân (L258, `ledger` L96) | **Luật 109/2025/QH15, Điều 4 khoản 6** (Công báo, đã đọc): "Thu nhập từ lãi trái phiếu chính phủ, lãi trái phiếu chính quyền địa phương, lãi tiền gửi tại tổ chức tín dụng, lãi từ hợp đồng bảo hiểm nhân thọ." Luật thông qua 10/12/2025, hiệu lực 01/07/2026 (Điều 29) | **Xác nhận** |
| Thuế 2% khi bán (L237, `ledger` L83) | **Điều 14 khoản 1**: thuế TNCN từ chuyển nhượng BĐS của cá nhân cư trú "được xác định bằng giá chuyển nhượng nhân (x) với thuế suất 2%" (không có thuế trên phần lãi). Người nộp là bên bán, hai bên có thể thoả thuận (helper). **Phát hiện mới:** **Điều 4 khoản 2** miễn thuế cho "thu nhập từ chuyển nhượng nhà ở… trong trường hợp cá nhân chỉ có một nhà ở, đất ở duy nhất tại Việt Nam"; theo helper, NĐ 253/2026 (30/06/2026, qua vov.vn) thêm điều kiện sở hữu ≥ 183 ngày [SECONDARY]. Cặp vợ chồng trong ví dụ bán căn nhà duy nhất → **rất có thể được miễn** | Câu L237 đúng như quy tắc chung nhưng **thiếu ngoại lệ chạm thẳng vào ví dụ** → **SỬA (thêm một câu)**. Bỏ thuế bán → hoà vốn 7,23% (đã tính ở mục 4) — vẫn trong dải "hơn sáu tới hơn tám" |
| Kinh phí bảo trì 2% (L236, `ledger` L81–82) | **Luật Nhà ở 2023, Điều 152 khoản 1** (nguyên văn): người mua căn của chủ đầu tư "phải đóng kinh phí bảo trì là 2% giá trị căn hộ…; khoản tiền này được **tính riêng với tiền bán**… và được quy định rõ trong hợp đồng mua bán". Lượt 1 dựa vào cách viết của Luật Nhà ở 2014 ("tính vào tiền bán") — **dẫn sai luật đang áp dụng** | **Rút lại SỬA L236 của lượt 1**: câu gốc "tính riêng ngoài giá bán" khớp Luật 2023. Với căn mua lại: nếu cần nói thì "kiểm tra chủ đầu tiên đã nộp chưa", không nói "không áp dụng" (helper); lời đọc hiện không nói gì về chỗ này ✓ |
| Lệ phí trước bạ 0,5% (L233) | Theo helper: NĐ 10/2022 Điều 8 vẫn 0,5%; NĐ 51/2025 và 175/2025 không đổi mức với nhà đất; tính theo giá hợp đồng nếu cao hơn bảng giá UBND; người mua nộp | **Xác nhận** |
| Phí công chứng (Ghi chú, hồ sơ §3, lượt 1 mục 1b L234–235) | Theo helper: TT 257/2016 (sửa bởi TT 111/2017) vẫn còn hiệu lực (LuatVietnam 17/06/2026); khung 1–3 tỷ = **1 triệu + 0,06%** phần vượt 1 tỷ → căn 2,5 tỷ ≈ **1,9 triệu**. Hồ sơ ghi 0,1% → 2,5 triệu là **sai** (0,1% là khung 100 triệu–1 tỷ) | Lời đọc không nói số → không sửa script. **Sửa Ghi chú/hồ sơ**: 0,1% → 0,06%, 2,5 → 1,9 tr. "Làm tròn 1% ≈ 25 tr" vẫn đúng chiều (0,5% + 1,9 tr + thẩm định, đăng ký thế chấp ≈ 15–17 tr; làm tròn lên, hơi thiệt cho người mua) |
| Phí quản lý HN (L239) | Theo helper: QĐ 25/2026/QĐ-UBND (13/02/2026, hiệu lực 23/02/2026) sửa QĐ 33/2025; có thang máy 1.200–16.500 đ/m²/tháng | **Xác nhận** |
| 15 m² sàn/người "nội thành" (L322, `ledger` L132–133) | Luật Cư trú 2020 Điều 20: nhà của mình không đòi diện tích ✓; nhà thuê, mượn, ở nhờ: chủ nhà đồng ý + diện tích do HĐND tỉnh quy định, **mức sàn 8 m²/người nằm ngay trong Luật** ✓. NQ 10/2023/NQ-HĐND (thông qua 06/07/2023, áp dụng tới hết 2030): nội thành 15, ngoại thành 8 m²; "nội thành" khi ban hành = **12 quận cũ**. Báo 01/2026 vẫn dẫn NQ này; **không tìm thấy NQ thay thế** sau khi bỏ cấp quận (01/07/2025); cách hiểu "nội thành" hiện hành **không có văn bản** | **Không kiểm được phạm vi** → câu mềm hơn (thay câu lượt 1) |

**Lời đọc — SỬA mới:**
- **L237 — giữ câu gốc, thêm ngay sau:** "Nếu đó là căn nhà duy nhất, khoản thuế này có thể được miễn, nhưng ví dụ của mình vẫn tính vào."
  (22 âm tiết)
- **L322 (thay câu lượt 1):** "Hà Nội còn đặt mức cao hơn, mười lăm mét vuông sàn mỗi người, cho khu nội thành cũ." (19 âm tiết)

**Màn hình — SỬA mới:**
- `ledger` "KHI BÁN" (L83): thêm dòng "MIỄN NẾU LÀ NHÀ Ở DUY NHẤT (CÓ ĐIỀU KIỆN) · VÍ DỤ VẪN TÍNH 2%"; nguồn "Luật Thuế TNCN 109/2025, Đ4 k2,
  Đ14 · hiệu lực 01/07/2026".
- `ledger` CH03 (L81–82): **giữ** "MUA CỦA CHỦ ĐẦU TƯ: + KINH PHÍ BẢO TRÌ 2%" (đúng Đ152 k1); vẫn nên thêm chữ nhỏ "CHƯA GỒM TRONG VÍ DỤ"
  (lượt 1).
- `ledger` CH06 (L132–133): "HÀ NỘI, KHU NỘI THÀNH CŨ ≥ 15 M² (NQ 10/2023/NQ-HĐND, ÁP DỤNG TỚI 2030)" · giữ "≥ 8 M² SÀN/NGƯỜI (LUẬT CƯ
  TRÚ, Đ20)".
- `bars` độ nhạy CH05 (tuỳ chọn): thêm cột "BỎ THUẾ BÁN (NHÀ DUY NHẤT) 7,23".
- Khối công thức mô tả (mục 4b): dòng người mua thêm "(thuế bán 2% — có thể được miễn nếu là nhà ở duy nhất)" (≈ +56 ký tự, vẫn dưới trần).

### 9.4 Tuyển sinh Hà Nội 2026–2027

| Mục (dòng) | Nguồn | Kết luận lượt 2 |
|---|---|---|
| Xét theo nơi cư trú, gồm tạm trú? Thường trú có xếp trên tạm trú? | Theo helper: **Công văn 1161/SGDĐT-QLT ngày 25/03/2026** của Sở GD&ĐT Hà Nội: xét tuyển theo nơi cư trú, xếp theo **khoảng cách** (bản đồ số GIS), dữ liệu VNeID; **không có thứ bậc thường trú trên tạm trú** | **Xác nhận** ý của L324–L327 (nhà thuê vẫn được xét) |
| Câu trích » L325 | VietNamNet 12/03/2026, nguyên văn: "Phụ huynh và học sinh lưu ý nơi cư trú được hiểu có thể là thường trú hoặc tạm trú" → đoạn script trích **khớp từng chữ** (nửa sau của câu); giới thiệu "Một bài báo… ghi rõ" đúng | **Xác nhận** |
| "lần đầu tiên" (L324, `kinetic` L134) | Lấy từ tiêu đề VietNamNet. Theo helper: trước đây Hà Nội phân tuyến theo **địa giới hành chính**, và việc nhận học sinh tạm trú không phải điều mới → "lần đầu" dễ hiểu thành "trước đây người tạm trú bị loại", tức nói quá | **SỬA nhẹ** |
| TP.HCM (L326) | Theo helper: QĐ 1700/QĐ-UBND 27/03/2026: xét theo "nơi ở hiện tại" qua VNeID, không phân biệt thường trú/tạm trú | **Xác nhận**; câu mềm "với cách xếp ưu tiên riêng" vẫn đúng |

**Lời đọc — SỬA mới:**
- **L324:** "Năm học này, Hà Nội xét tuyển mầm non, lớp một và lớp sáu theo nơi cư trú và khoảng cách tới trường." (23 âm tiết)

**Màn hình — SỬA mới:** `kinetic` L134 "HÀ NỘI 2026–2027: XÉT MẦM NON, LỚP 1, LỚP 6 THEO NƠI CƯ TRÚ (THƯỜNG TRÚ HOẶC TẠM TRÚ) + KHOẢNG CÁCH" ·
`quote` L135 nguồn thêm "· Công văn 1161/SGDĐT-QLT (25/03/2026)".

### 9.5 Lãi gửi Big4 và CPI thuê nhà

| Mục (dòng) | Nguồn | Kết luận lượt 2 |
|---|---|---|
| 12 tháng, 4 NH lớn 6,8% (09/2026) (L257, L286) | Theo helper: VietNamNet 09/09/2026 | **Xác nhận** |
| 5,2% (01/2026) (L273, `race` L107) | Theo helper: VnEconomy 27/01/2026 — mức **trong tháng một**, không phải đúng ngày 01/01 | Lời đọc L273 không nêu mức → **xác nhận**; nhãn màn hình "TIẾT KIỆM 5,2% (01/2026)" đúng ✓; Ghi chú/hồ sơ "mở 01/01" → "tháng 1" |
| CPI thuê nhà +4,91% (L246, `ledger` L89) | NSO 30/09/2026 (PDF, helper đọc): "chỉ số giá nhà ở thuê tăng 4,91%" là **bình quân 9 tháng so với cùng kỳ 2025**, không phải mức tăng từ đầu năm tới tháng chín | **SỬA nhẹ** (lời đọc dễ hiểu thành tăng từ tháng một tới tháng chín) |

**Lời đọc — SỬA mới:**
- **L246:** "Chín tháng đầu năm nay, giá thuê nhà trong rổ chỉ số giá tiêu dùng cao hơn cùng kỳ năm ngoái khoảng năm phần trăm." (25 âm tiết)

**Màn hình — SỬA mới:** `ledger` L89 "CPI THUÊ NHÀ 9T/2026: +4,91% SO CÙNG KỲ (BÌNH QUÂN, NSO)".

### 9.6 Tổng hợp thay đổi so với lượt 1

**SỬA mới — lời đọc (6):** L179 (câu mới, thay câu lượt 1) · L206 "bình quân" → "phổ biến" · L237 thêm câu miễn thuế nhà ở duy nhất ·
L246 "cao hơn cùng kỳ năm ngoái" · L322 "khu nội thành cũ" (thay câu lượt 1) · L324 bỏ "lần đầu tiên". Giữ hai SỬA lượt 1 nay đã có nguồn
xác nhận lý do: L270 "tới cuối năm ngoái" và L211 "một kiểu trả hay gặp".

**SỬA mới — màn hình (8):** `bars` giá CH01 (giữ CBRE 60 với nhãn đúng cách đo; 83 → 84) · `kinetic` L54 (CBRE + Savills) · `ledger` L66
"phổ biến" · `bars` L76 dải 8,5–11 / cột 9,75 · `ledger` "KHI BÁN" miễn nhà ở duy nhất · `ledger` L89 CPI so cùng kỳ · `ledger` L132–133
"khu nội thành cũ" · `kinetic` L134 bỏ "LẦN ĐẦU".

**Rút lại SỬA của lượt 1 (2):** L177 (giữ "sáu mươi… hơn một trăm hai mươi": cùng quý II, có nguồn) · L236 (giữ "tính riêng ngoài giá
bán": đúng nguyên văn Đ152 k1 Luật Nhà ở 2023).

**Sửa Ghi chú / hồ sơ (không chạm lời đọc):** phí công chứng 0,06% → ≈ 1,9 tr · Batdongsan 83 → 84 · VARS-IRE ưu đãi 2026 8,2 → 8,5 ·
DKRA 10,9% là mức "phổ biến" · Bộ XD −3,9% là báo tính · Savills không nói sơ cấp/thứ cấp, mốc cuối 2025 · lãi gửi 5,2% là "tháng
1/2026" · thuế bán: Điều 4 k2 miễn nhà ở duy nhất (NĐ 253/2026, ≥ 183 ngày — SECONDARY).

**Còn mở (không kiểm được tới bản gốc):** định nghĩa giá thứ cấp CBRE quý II (không truy cập được cbre.vn) · báo cáo REFI gốc (mới có
một bài báo) · phạm vi "nội thành" của NQ 10/2023 sau 01/07/2025 · nguyên văn NĐ 253/2026 (điều kiện 183 ngày).

**Nguồn mở trong lượt 2:** legalzone.vn (Luật 109/2025, Công báo số 37) · tapchikinhtetaichinh.vn …-161086.html (07/07/2026) ·
vietnamfinance.vn …-d147239.html (07/07/2026) · en.vneconomy.vn/hanoi-apartment-supply-hits-six-year-high.htm · vietnamnews.vn/economy/1690315
(CBRE quý IV/2024, quy ước NSA) · cafef.vn …188260814143655062.chn (Savills, 14/08/2026) · cafebiz.vn …176260829091836212.chn (REFI) ·
dantri.com.vn …20260903083127075.htm (DKRA) · vnexpress.net/gia-chung-cu-dat-nen-ha-nhiet-5112330.html (Bộ XD) · thuvienphapluat (Đ152
Luật Nhà ở 2023, qua kết quả tìm kiếm) · doanhnghiephoinhap.vn (NQ 10/2023, bài 06/07/2023). Các mục ghi "theo helper" lấy từ báo cáo của
hai helper (Cafeland 07/07, Người Quan Sát 16/01, Báo Xây dựng 15/04, VnExpress 04/08, VietNamNet 13/03 và 09/09, VnEconomy 27/01, NSO PDF
30/09, Công văn 1161/SGDĐT-QLT, QĐ 1700/QĐ-UBND TP.HCM, hrspring.vn bản Luật 109, LuatVietnam 17/06/2026, vov.vn NĐ 253/2026, Tuổi Trẻ
01/2026).
