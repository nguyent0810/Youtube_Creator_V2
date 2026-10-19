# Fact-check — script.md (bản 1) · ck-d1-vang-dinh (Tâm lý tiền bạc — D1)

Ngày kiểm: 07/10/2026. Đối chiếu: hồ sơ `docs/channels/chung-khoan/2026-10-07-long-d1-research.md` (số `[n]` = nguồn trong hồ sơ
đó) và `2026-10-06-long-01-research.md` (`[L01-n]`); luật kênh `2026-10-06-positioning.md` mục 1; dữ liệu `data/ck/sjc_1d.csv`
(tính lại bằng pandas). Đã mở lại trang gốc cho các mục "cần kiểm lại" (danh sách ở mục 5). Không sửa script.

**Kết luận: OK 110 · SỬA 30 · BỎ 0** (140 hàng: 4 tiêu đề, 106 hàng lời thoại — vài dòng gộp — và 30 hàng chữ/cảnh trên màn
hình). Mục luật kênh, TTS, tính lại Ghi chú và nguồn ở cuối, không tính vào tổng.

Nhãn: OK = đúng nguồn / chấp nhận được · SỬA = sai số, nói quá nguồn, mơ hồ, hoặc chạm luật kênh · BỎ = nên cắt câu.

**Năm điểm quan trọng nhất**
1. **L202 sai đơn vị: người xếp hàng 11h → 15h mang 2 *chỉ* đi bán, không phải 2 *lượng*.** Nguyên văn Phụ Nữ Online
   29/01/2026 [29]: "anh mang 2 chỉ vàng tiết kiệm đi bán kiếm lãi, tuy nhiên đã xếp hàng từ 11g trưa, đến 3g chiều vẫn chưa
   đến lượt". Chữ trên màn hình CH03 và Ghi chú (và hồ sơ, mục "Phát hiện bất ngờ") cũng phải sửa.
2. **L153 lời trích 2020 không đúng nguyên văn.** Người Lao Động 09/02/2021 [8] viết: "…ở những thời điểm giá vàng 'nóng sốt'
   lập đỉnh lịch sử trên 60 triệu đồng/lượng, là **không còn** hiện tượng đổ xô, xếp hàng mua vàng như những năm trước."
   Script ghi "Không **có** hiện tượng đổ xô, xếp hàng." Thêm nữa, bài 24h [9] **không** có câu này: chữ "lác đác" trong 24h tả
   phố vàng **tháng 11/2021**, không phải lúc đỉnh 08/2020. Vì vậy L270 "đỉnh 2020 đến khi phố vàng vắng khách" cũng nói quá
   nguồn.
3. **L222 + bars CH04: Thanh Niên không viết "chưa từng có".** Bài [40] dẫn lời "nhiều chuyên gia kinh tế": chênh 5–6 triệu
   "là cao bất thường". (Tuổi Trẻ [41] dùng chữ "kỷ lục".) Hơn nữa chênh 5 triệu đã có từ 09–12/06/2026 [39].
4. **L161 + slam CH01 "Nó báo rằng giá vừa tăng rất nhanh" nói quá chính dữ liệu của video.** Ít nhất 2/11 đợt không đến sau
   một cú tăng: D (04/06/2024, xếp hàng mua giá bình ổn ở ngân hàng sau khi giá đã giảm, "gần đáy") và K (21/03/2026, "bắt
   đáy" sau khi giá giảm 5,1 triệu); ba đợt ngày vía là do lịch.
5. **Barber & Odean (L174, kinetic CH02):** tóm tắt bài chỉ nói nhà đầu tư cá nhân **mua ròng** cổ phiếu gây chú ý (dữ liệu
   môi giới Mỹ 1991–1996). Vế "không đem lại lợi nhuận vượt trội" **không có** trong tóm tắt và không mở được toàn văn (Berkeley
   lỗi DNS, SSRN/ResearchGate 403) → bỏ vế đó, thêm "ở Mỹ".

Đã xác nhận đúng nguồn: 13:25 191,3 (webgia, 7 lần điều chỉnh); 3–4 giờ sáng và quà cưới cho con gái / em gái (CafeF [28]);
62,45 (Báo Pháp luật [7]); 49,12 ngày 23/08/2011, "vàng trong nước" (Báo Đắk Lắk [1]); hàng 09/08/2011 ở Trần Nhân Tông (DTTC
[2]); 124 triệu "cao nhất từ trước tới nay", chênh 14,75 (VOV [20]); 86,8/90,3 ngày vía 2025 (Tuổi Trẻ [19]); 182/185 → 181/184,
chênh ~20 triệu, giới hạn SJC, câu "Một chỉ vàng bằng cả tháng lương, nhìn ngán quá" (VnExpress [32]); "mua trên giấy" 7–10
ngày, 90 ngày đơn lớn, 191,3 → 172 trong 48 giờ (Vietnambiz [31]); "chỉ còn hơn 2 triệu" 19/08 (Dân trí [42]); 140,5/143,5
sáng 06/10 (VietnamPlus [46]), chênh ~12,8 (Kenh14 [47]); WGC 42,1 → 36,1 tấn, >550 USD/oz; Greenwood & Shleifer: sáu nguồn
1963–2011, kỳ vọng tương quan dương với lợi nhuận vừa qua, tương quan âm với lợi nhuận kỳ vọng theo mô hình; Ngô Hương Giang
(Tiền Phong [74]). **23/03/2026** (Vietstock đăng lại trên Investing [38]): 9:58 SJC 164/167, "giảm khoảng 24,5 triệu" chiều bán
so với đỉnh, tiệm bỏ giới hạn, mua "hàng chục lượng" → "thấp hơn đỉnh hơn hai mươi triệu" **đúng**. **30/09/2026 chốt chiều
141,1/144,1** (Báo Đà Nẵng 16:52, +1,6 triệu so phiên trước; sáng 140,5/143,5) → **CSV 30/09 = 139,5/142,5 là giá 29/09 lặp lại**,
CSV 01/10 cũng vậy (VOV 01/10: 140,8/143,8).

## 1. Bảng kiểm từng dòng

### 1a. Tiêu đề

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Tiêu đề làm việc | "VÌ SAO NGƯỜI TA HAY ĐỔ XÔ MUA VÀNG ĐÚNG LÚC GIÁ ĐỈNH?" (L1) | SỬA | Không dùng làm tiêu đề đăng; dùng phương án (1) | Tiền đề chỉ đúng 4/11 đợt theo chính bảng điểm của video. Factcheck hai video trước đều bắt lỗi tiêu đề nói quá dữ liệu. |
| Tiêu đề (1) | "Xếp hàng mua vàng có phải là đỉnh? 11 lần người Việt đổ xô, đọc lại bằng dữ liệu" (L8) | OK | (tuỳ chọn, chặt hơn) "Xếp hàng mua vàng có phải là đỉnh? Đọc lại 11 đợt đổ xô (2011–2026) bằng dữ liệu" | Câu hỏi mở, video trả lời "không hẳn" ✓. "11 lần người Việt đổ xô" nghe như đếm hết; thực tế báo còn ghi thêm hàng dài 26/08/2025 (NLĐ, TP.HCM) và 22/09/2025 (Tuổi Trẻ). "11 đợt (2011–2026)" là mẫu của kênh, khớp L147. **Khuyến nghị.** |
| Tiêu đề (2) | "Vì sao người ta hay đổ xô mua vàng khi giá đang lập kỷ lục?" (L9) | SỬA | Không dùng, hoặc "Vì sao người ta đổ xô mua vàng khi giá vừa tăng mạnh?" | Đặt tiền đề "hay… khi lập kỷ lục": chỉ khoảng 5–6/11 đợt là ngày kỷ lục (A, F, G, H, J; B thì lúc đỉnh không có hàng). C, D, E, I, K không phải ngày kỷ lục. Video không trả lời câu này mà trả lời "xếp hàng có phải đỉnh". |
| Tiêu đề (3) | "Đứng trong hàng mua vàng: bộ não nghĩ gì, và bạn trả thêm những gì?" (L9–10) | OK | — | Không có khẳng định dữ kiện; khớp CH02 + CH04. An toàn nhất nhưng kém tò mò hơn (1). |

### 1b. Lời thoại

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| CH00 | "Ba, bốn giờ sáng ngày hai mươi chín tháng một…, phố Trần Nhân Tông… đã có người xếp hàng chờ mua vàng." (L129) | OK | — | CafeF [28]: "không ít người đã đến xếp hàng từ 3-4h sáng để xếp số sớm" (bài về phố Trần Nhân Tông). |
| CH00 | "Nhiều tiệm treo biển hết hàng. Ai muốn mua từ bốn chỉ trở lên phải lấy phiếu hẹn." (L130) | SỬA | "Có tiệm treo biển hết hàng. Có nơi chỉ bán ngay cho người mua dưới bốn chỉ, mua nhiều hơn phải lấy phiếu hẹn." | CafeF [28] tả **một** cửa hàng ("cửa hàng vàng đã để biển thông báo hết vàng"), và quy định cũng của một cửa hàng: "chỉ bán trực tiếp đối với số lượng vàng dưới 4 chỉ, còn nếu mua trên 4 chỉ thì… phiếu hẹn". Script khái quát thành "nhiều tiệm" và quy tắc chung; "từ bốn chỉ" ≠ "trên 4 chỉ". |
| CH00 | "Một giờ hai mươi lăm phút chiều hôm đó, giá bán vàng miếng SJC chạm một trăm chín mươi mốt triệu ba trăm nghìn…" (L131) | OK | — | webgia [30]: lần điều chỉnh thứ 5, 13:25, 188,3/191,3 (cao nhất trong 7 lần). |
| CH00 | "Đó là mức cao nhất trong lịch sử, tính tới lúc kênh làm video này." (L132) | OK | — | Tới 06/10/2026 ✓ [L01]. Kiểm lại nếu đăng muộn. |
| CH00 | "Đầu tháng mười… bạn nhận khoảng một trăm bốn mươi triệu năm trăm nghìn." (L133) | OK | — | VietnamPlus [46]: sáng 06/10 140,5/143,5 ✓ (chiều 139,9 [44]). |
| CH00 | "Mất gần năm mươi mốt triệu đồng mỗi lượng. Hơn một phần tư số tiền." (L134) | OK | — | 191,3 − 140,5 = 50,8; −26,56% ✓. |
| CH00 | HỎI + "…đọc lại báo chí mười lăm năm qua, câu trả lời trung thực là: không hẳn." (L135–137) | OK | — | 2011–2026 ✓. |
| CH00 | Ba câu hỏi lộ trình (L138–141) | OK | — | — |
| CH00 | "Đây là Biểu Đồ Biết Nói… không phải lời khuyên mua hay bán vàng." (L142–143) | OK | — | Luật 2 ✓; thẻ miễn trừ 4–5 giây vẫn phải có trên hình. |
| CH01 | "Kênh đọc lại báo chí từ năm 2011, và tìm được mười một đợt… có ghi rõ ngày và giá." (L147) | OK | (tuỳ chọn) bỏ "có ghi rõ ngày và giá" | Đợt B (cuối 07/2020) báo không ghi rõ ngày/giá xếp hàng; vẫn chấp nhận được vì đỉnh B có ngày và giá. |
| CH01 | "Câu hỏi cho mỗi đợt: người mua hôm đó, về sau lãi hay lỗ?" (L148) | OK | — | — |
| CH01 | "Tháng tám năm 2011, người ta xếp hàng ở phố vàng Trần Nhân Tông." (L149) | OK | — | DTTC [2]: "Cảnh tượng xếp hàng mua vàng lại tái diễn sáng nay trên 'phố vàng' Trần Nhân Tông" (09/08/2011). |
| CH01 | "Ngày hai mươi ba, vàng trong nước lên đỉnh bốn mươi chín triệu một trăm hai mươi nghìn…" (L150) | OK | — | Báo Đắk Lắk [1]: "ngày 23-8 được coi là đỉnh điểm khi vàng trong nước vọt lên 49,12 triệu đồng/lượng". |
| CH01 | "Năm 2020, hàng dài giữa trưa nắng xuất hiện vào cuối tháng bảy." (L151) | OK | (tuỳ chọn) "giữa trưa" thay "giữa trưa nắng" | 24h [9]: "người dân xếp hàng xuyên trưa để mua vàng vào thời điểm cuối tháng 7/2020". Chữ "nắng" chỉ có ở nguồn SECONDARY. |
| CH01 | "Còn khi giá lên đỉnh sáu mươi hai triệu bốn trăm năm mươi nghìn vào đầu tháng tám, báo chí lại ghi: » Không có hiện tượng đổ xô, xếp hàng." (L152–153) | SỬA | "Còn khi giá lên đỉnh sáu mươi hai triệu bốn trăm năm mươi nghìn vào đầu tháng tám, nửa năm sau nhìn lại, báo Người Lao Động ghi: » Không còn hiện tượng đổ xô, xếp hàng mua vàng như những năm trước." | Nguyên văn NLĐ 09/02/2021 [8]: "…ở những thời điểm giá vàng 'nóng sốt' lập đỉnh lịch sử trên 60 triệu đồng/lượng, là không còn hiện tượng đổ xô, xếp hàng mua vàng như những năm trước". Lời trích hiện tại sai chữ ("có"/"còn") và cắt vế. Đây là bài nhìn lại, không phải tin ngày đỉnh. 62,45 ✓ (Báo Pháp luật [7]: "giá kỷ lục thiết lập cuối tuần trước là 62,45"). |
| CH01 | "…báo ghi thêm năm đợt: hai ngày vía Thần Tài, một đợt xếp hàng mua ở ngân hàng, và hai ngày giá lập kỷ lục." (L154) | OK | — | C, E; D; F, G (hồ sơ 1.1) ✓. |
| CH01 | "Năm đợt này, mười hai tháng sau, người mua đều đang lãi: ít nhất khoảng bảy phần trăm, nhiều nhất… gần như nhân đôi." (L155) | OK | (tuỳ chọn) "đều có lãi" thay "đều đang lãi" | Tính lại: +11,2 · +45,5 · +92,9 · +35,1 · +7,4% ✓. Mốc 12 tháng của C là 07/02/2025 (≈ 11,5 tháng); CSV 17/02/2025 cho +12,2% — vẫn "khoảng 11–12%". |
| CH01 | "…ngày hai mươi hai tháng tư năm 2025: vàng miếng lên một trăm hai mươi tư triệu, cao nhất tới khi đó, mỗi người mua tối đa hai chỉ." (L156) | SỬA | "…vàng miếng lên một trăm hai mươi tư triệu, cao nhất tới khi đó, có nơi chỉ bán tối đa hai chỉ mỗi người." | VOV [20]: 122/124, "mức cao nhất từ trước tới nay" ✓. Giới hạn 2 chỉ chỉ có ở **bài liên quan** về một số tiệm, không phải quy định chung (và không rõ áp cho vàng miếng hay nhẫn). |
| CH01 | "Ai nghĩ 'đỉnh rồi', thì một năm sau, giá tiệm mua vào cao hơn khoảng ba mươi lăm phần trăm." (L157) | OK | — | 124 → 167,5 (CSV 22/04/2026; các ngày lân cận 166,7–168,1, không phải điểm lặp) = +35,1% ✓. |
| CH01 | "Năm 2026 có bốn đợt: …, và hai mươi mốt tháng ba, khi hàng trăm người chen nhau giữa trưa để 'bắt đáy'." (L158) | OK | — | [37] bằng chứng; 21/03/2026 là thứ Bảy. |
| CH01 | "Tới đầu tháng mười, cả bốn đợt đều đang lỗ, từ gần mười tám tới gần hai mươi bảy phần trăm." (L159) | OK | — | −26,6 · −23,6 · −26,4 · −17,8% ✓. |
| CH01 | "Cộng lại: bốn đợt rơi vào vùng đỉnh. Năm đợt, giá sau đó còn lên. Hai đợt còn lại cũng lỗ…" (L160) | OK | — | Khớp hồ sơ (A, B, H, J / C–G / I, K). Lưu ý B: hàng cuối 07/2020 ở ~56–57 (CSV 27/07: 55,45/56,9), thấp hơn đỉnh ~9%; một năm sau ≈ hoà vốn (CSV 02/08/2021 mua 56,5). "Vùng đỉnh" chấp nhận được vì L151–153 đã nói rõ. |
| CH01 | "Nghĩa là: hàng dài không báo đỉnh. Nó báo rằng giá vừa tăng rất nhanh." (L161) | SỬA | "Nghĩa là: hàng dài không báo đỉnh. Phần nhiều, nó xuất hiện sau khi giá vừa tăng rất nhanh; có lần lại vì giá vừa giảm, hay vì ngày vía." | Nói quá dữ liệu của chính video: D (04/06/2024) xếp hàng mua giá bình ổn sau khi giá đã giảm, hồ sơ ghi "gần đáy"; K (21/03/2026) xếp hàng "bắt đáy" sau khi giá giảm 5,1 triệu; C, E, I do lịch ngày vía. |
| CH01 | "Có lúc sau đó còn tăng tiếp, có lúc là đỉnh. Và lúc đứng trong hàng, không ai biết…" (L162) | OK | — | Hồ sơ 1.2 ✓; chống dự báo ✓. |
| CH01 | HỎI + "Mình đoán một phần lý do nằm ở trí nhớ." (L163–164) | OK | — | Có "mình đoán" ✓ (hồ sơ 1.2 ghi là suy luận). |
| CH01 | "…mười bốn năm sau, VnExpress vẫn viết về 'nỗi ám ảnh' của cơn sốt vàng năm 2011." (L165) | SỬA | "…hơn mười ba năm sau, VnExpress vẫn đăng ý kiến bạn đọc về 'nỗi ám ảnh' sau cú sốc vàng năm hai nghìn không trăm mười một." | Bài [6] ngày 20/03/2025 = 13,6 năm sau 08/2011. Tiêu đề: "Nỗi ám ảnh sau cú sốc vàng lên 50 triệu rồi lao dốc năm 2011"; nội dung chính là **ý kiến bạn đọc**, không phải bài của phóng viên, và không nói về "cơn sốt"/xếp hàng. |
| CH01 | "Còn những lần xếp hàng rồi giá lên tiếp, ít ai nhắc lại. Đó là cái bẫy đầu tiên của bộ não." (L166–167) | OK | — | Suy luận, hồ sơ 1.2. |
| CH02 | "Bẫy thứ nhất: cái gì dễ nhớ, mình tưởng là thường xảy ra." (L171) | OK | — | — |
| CH02 | "Hai nhà tâm lý học Tversky và Kahneman gọi đây là lối tắt 'dễ nhớ'." (L172) | OK | — | Availability heuristic, 1973 [62] (thư mục chưa mở, nhưng là kiến thức chuẩn). |
| CH02 | Ví dụ nhà hàng xóm bị trộm (L173) | OK | — | Ví dụ tự đặt, không có số. |
| CH02 | "Nghiên cứu của Barber và Odean cho thấy nhà đầu tư cá nhân hay mua những cổ phiếu đang gây chú ý, và việc đó không đem lại lợi nhuận vượt trội." (L174) | SỬA | "Nghiên cứu của Barber và Odean trên dữ liệu nhà đầu tư Mỹ cho thấy nhà đầu tư cá nhân hay mua ròng những cổ phiếu đang gây chú ý: lên tin tức, giao dịch đột biến, giá biến động mạnh." | Tóm tắt bài (RFS 2008, qua EconPapers và kết quả tìm kiếm): "individual investors are net buyers of attention-grabbing stocks, e.g., stocks in the news, stocks experiencing high abnormal trading volume, and stocks with extreme one-day returns". Dữ liệu: một công ty môi giới giá rẻ ở Mỹ, 1991–1996. Vế "không đem lại lợi nhuận vượt trội" không có trong tóm tắt, toàn văn không mở được → không đọc. |
| CH02 | "Mỗi lần vàng lập kỷ lục, ảnh hàng dài lại lên báo, và vàng thành chuyện ai cũng thấy." (L175) | SỬA | "Nhiều lần vàng lập kỷ lục, ảnh hàng dài lại lên báo, và vàng thành chuyện ai cũng thấy." | "Mỗi lần" mâu thuẫn với chính L153 và L270: đỉnh 08/2020 báo ghi không còn đổ xô, xếp hàng. |
| CH02 | "Bẫy thứ hai: sợ bị bỏ lỡ, hay còn gọi là FOMO. Tức là nỗi lo người khác đang có trải nghiệm đáng giá, còn mình thì vắng mặt." (L176–177) | OK | — | Diễn ý đúng định nghĩa Przybylski và cộng sự 2013 [68]. |
| CH02 | Ví dụ nhóm Zalo khoe "mua được hai chỉ rồi" (L178) | OK | — | Ví dụ; không mời vào nhóm nào (luật 1) ✓. |
| CH02 | "Bẫy thứ ba… Hai quán phở…" (L179–180) | OK | — | — |
| CH02 | "Các nhà kinh tế học chỉ ra: làm theo đám đông có thể hợp lý với từng người… cả đám đông có thể cùng sai." (L181–182) | OK | — | Banerjee 1992; Bikhchandani–Hirshleifer–Welch 1992 [64][65]; diễn ý đúng ý chính của mô hình thác thông tin. |
| CH02 | "Bẫy thứ tư…" + ví dụ mưa ba hôm (L183–184) | OK | — | — |
| CH02 | "Bốn tuần đầu năm 2026, giá bán vàng miếng SJC tăng khoảng hai mươi lăm phần trăm." (L185) | OK | — | 152,8 (01/01, [48]) → 191,3 (29/01) = +25,2%; 01/01 → 29/01 đúng 4 tuần ✓. |
| CH02 | "Greenwood và Shleifer, hai nhà kinh tế học, xem sáu bộ khảo sát nhà đầu tư trải gần năm mươi năm: thị trường vừa tăng mạnh, người ta càng tin nó tăng tiếp." (L186) | SỬA | "Greenwood và Shleifer, hai nhà kinh tế học, xem sáu nguồn số liệu về kỳ vọng của nhà đầu tư chứng khoán Mỹ, trải gần năm mươi năm: thị trường vừa tăng mạnh, người ta càng tin nó tăng tiếp." | Tóm tắt (SSRN/OUP): "investor expectations of future stock market returns from six data sources between 1963 and 2011" (48 năm ✓), "highly positively correlated… with past stock returns". Thiếu phạm vi "chứng khoán Mỹ" thì câu nghe như nghiên cứu về vàng/mọi thị trường. "Nguồn số liệu" sát hơn "bộ khảo sát" (có khảo sát CFO, bản tin đầu tư). |
| CH02 | "Trong khi theo các mô hình kinh tế, đó lại thường là lúc lợi nhuận kỳ vọng phía trước thấp hơn." (L187) | OK | — | Tóm tắt: "strongly negatively correlated with model-based expected returns" ✓. Không phải dự báo giá vàng. |
| CH02 | HỎI "…là dại à?" / "Không." (L188–189) | OK | — | Luật không chế giễu ✓. |
| CH02 | "Hôm hai mươi chín tháng một, có khách nói với báo rằng họ mua làm quà cưới cho con, cho em." (L190) | OK | (tuỳ chọn) "có người mua làm quà cho con gái sắp lấy chồng, có người cho em gái sắp cưới" | CafeF [28]: hai khách khác nhau ("quà tặng cho em gái sắp cưới"; "quà cho con gái sắp lấy chồng") ✓. |
| CH02 | "Học theo người xung quanh là phản xạ tự nhiên. Chỉ là trên thị trường, phản xạ ấy có giá." (L191) | OK | — | — |
| CH03 | "Có một con số khiến mình bất ngờ." (L195) | OK | — | — |
| CH03 | "Theo Hội đồng Vàng Thế giới, năm 2025, năm có ba đợt xếp hàng lên báo, nhu cầu vàng miếng và vàng xu… giảm mười bốn phần trăm, còn khoảng ba mươi sáu tấn." (L196) | SỬA | "Theo Hội đồng Vàng Thế giới, năm hai nghìn không trăm hai mươi lăm, năm có nhiều đợt xếp hàng lên báo, nhu cầu vàng miếng và vàng xu của Việt Nam lại giảm mười bốn phần trăm, còn khoảng ba mươi sáu tấn." | WGC FY2025 [53]: 42,1 → 36,1 tấn, −14% ✓. Nhưng "ba đợt" chỉ là số đợt kênh chọn (E, F, G); báo 2025 còn ghi hàng dài 26/08/2025 (NLĐ, "Người dân xếp hàng mua vàng SJC khi giá lập đỉnh ở TP HCM") và 22/09/2025 (Tuổi Trẻ, "Xếp hàng mua vàng"). Nói "ba đợt" như tổng số là sai. |
| CH03 | "Vậy hàng dài từ đâu ra? Một phần từ khan hàng." (L197) | OK | — | WGC quy một phần mức giảm cho thiếu cung ✓. |
| CH03 | "Hội đồng Vàng Thế giới ghi nhận: thiếu vàng miếng SJC đã đẩy giá trong nước cao hơn hẳn giá thế giới." (L198) | OK | — | WGC: chênh ">US$550/oz" ✓. |
| CH03 | "Mỗi đợt nóng, tiệm vàng lại giới hạn số lượng: có lúc hai chỉ một người, có lúc một lượng một ngày." (L199) | OK | — | [20] (bài liên quan); SGGP [26]: SJC "một lượng vàng miếng/ngày" 06/09/2025 ✓. |
| CH03 | "Giới hạn làm hàng dài thêm, và ngầm gửi một tín hiệu: được mua là may. Đúng vào lúc giá cao nhất." (L200) | SỬA | "Giới hạn làm hàng dài thêm, và ngầm gửi một tín hiệu: được mua là may. Mà nhiều lần, đó lại là lúc giá đang lập kỷ lục." | Suy luận (hồ sơ 3.3). "Đúng vào lúc giá cao nhất" quá tuyệt đối: giới hạn 1 lượng/khách ngày 04/06/2024 (D) là lúc giá gần đáy; 26/02/2026 (I) không phải đỉnh. |
| CH03 | "Còn cuối tháng ba 2026, khi giá đã thấp hơn đỉnh hơn hai mươi triệu, báo ghi có tiệm bỏ giới hạn: mua hàng chục lượng cũng được." (L201) | OK | — | Vietstock 23/03/2026 (đăng lại, [38]): 9:58 SJC 164/167; "giảm khoảng 24,5 triệu" chiều bán; tiệm bỏ giới hạn "1 lượng/khách", mua "hàng chục lượng". 191,3 − 167 = 24,3; CSV 23/03 bán 166 → −25,3 ✓. Bài gốc trên vietstock.vn chưa mở được; bản đăng lại ghi rõ nguồn Vietstock. |
| CH03 | "…ngay ngày hai mươi chín tháng một, có người chờ bốn tiếng để bán hai lượng vàng." (L202) | SỬA | "Hàng dài cũng không chỉ có người mua: ngay ngày hai mươi chín tháng một, có người xếp hàng từ mười một giờ trưa tới ba giờ chiều vẫn chưa tới lượt bán hai chỉ vàng." | **Sai đơn vị.** Phụ Nữ Online [29], nguyên văn: "anh mang 2 chỉ vàng tiết kiệm đi bán kiếm lãi, tuy nhiên đã xếp hàng từ 11g trưa, đến 3g chiều vẫn chưa đến lượt". Hai chỉ, không phải hai lượng; và chưa bán được. |
| CH03 | HỎI ngày vía + "Mua chút vàng lấy lộc ngày mùng mười tháng Giêng là một nét văn hoá, như mua cành đào ngày Tết." (L203–204) | OK | — | Trân trọng, không chế giễu ✓. Mùng 10 tháng Giêng ✓ [74]. |
| CH03 | "Nhà nghiên cứu Ngô Hương Giang gọi đây là tín ngưỡng, một cách giải quyết mang tính tâm lý hơn là khoa học." (L205) | SỬA | "Nhà nghiên cứu văn hoá Ngô Hương Giang gọi đây là tín ngưỡng dân gian: một cách để người ta tin và hy vọng vào năm mới, mang tính tâm lý hơn là khoa học." | Tiền Phong [74] (đã mở): bà là "nhà nghiên cứu văn hoá"; nguyên văn: "cách để con người tin, hy vọng vào năm mới. Đó là cách giải quyết mang tính tâm lý hơn là khoa học". Script cắt mất vế ấm áp, chỉ giữ vế "hơn là khoa học" → dễ nghe như coi thường tục lệ. Thêm vế đầu thì đúng nguồn hơn và tôn trọng hơn. |
| CH03 | "…mua ngày vía năm 2024, một năm sau lãi khoảng mười một phần trăm." (L206) | OK | (tuỳ chọn) "tới ngày vía năm sau, lãi khoảng mười một phần trăm" | 78,05 (giá BTMC [13]; CSV SJC 19/02/2024 = 75/78) → 86,8 (07/02/2025 [19]) = +11,2% ✓. |
| CH03 | "Ngày vía năm kế tiếp: một năm sau, số tiền gần như nhân đôi." (L207) | OK | — | 90,3 → 174,2 (CSV 06/02/2026) = +92,9%. CSV 05–09/02/2026 cùng 174,2 (có thể là giá lặp), nhưng bất kỳ giá 170–180 nào cũng ra +88% đến +99% → kết luận không đổi. |
| CH03 | "Ngày vía năm 2026: tới đầu tháng mười đang lỗ gần hai mươi bốn phần trăm." (L208) | OK | — | 184 → 140,5 = −23,6% (185 → −24,1%) ✓. |
| CH03 | "Ba năm, ba kết quả khác hẳn nhau. Ngày vía không cho biết gì về hướng giá." (L209) | OK | — | Hồ sơ 2.5. |
| CH03 | "Mua một chỉ lấy lộc là chi tiêu cho niềm vui. Chuyện chỉ khác khi một khoản tiền lớn được quyết định theo ngày vía." (L210) | OK | — | Trân trọng ✓; không khuyên. |
| CH03 | "Ngày vía năm ấy, nhiều người chuyển sang những sản phẩm vàng rất nhỏ. Một khách hàng nói với VnExpress:" (L211) | OK | — | Bài VnExpress [32] **không** nói chuyện vàng siêu nhỏ; ý này có ở Dân Việt, Sức khoẻ & Đời sống, Vietnambiz 25–26/02/2026 ("vàng siêu nhỏ" 0,05–1 chỉ). Câu thoại đúng; Ghi chú/mô tả cần thêm nguồn đó. |
| CH03 | "» Một chỉ vàng bằng cả tháng lương." (L212) | OK | — | VnExpress [32], khách Cẩm Tiên: "Một chỉ vàng bằng cả tháng lương, nhìn ngán quá". Trích nửa đầu, không đổi nghĩa ✓. |
| CH04 | "Giả sử bạn đã tới đầu hàng… ba thứ ít ai nhìn thấy." (L216) | OK | — | — |
| CH04 | "Thứ nhất: chênh lệch giữa giá bán và giá mua." (L217) | OK | — | — |
| CH04 | "Ngày hai mươi chín tháng một, tiệm bán ra 191,3 nhưng mua lại chỉ 188,3." (L218) | OK | — | webgia [30] 13:25 ✓. |
| CH04 | "Bước ra khỏi cửa, bạn đã lỗ ba triệu, khoảng một phẩy sáu phần trăm." (L219) | OK | — | 3/191,3 = 1,57% ✓. |
| CH04 | HỎI "Ba triệu trên gần hai trăm triệu…" / "Riêng nó thì nhỏ. Nhưng khoảng chênh này không đứng yên." (L220–221) | OK | — | — |
| CH04 | "Ngày hai mươi ba tháng bảy, khi giá rơi mạnh, chênh lệch mua bán của SJC lên năm triệu, có lúc sáu triệu. Báo Thanh Niên gọi đó là chưa từng có." (L222) | SỬA | "Ngày hai mươi ba tháng bảy, khi giá rơi mạnh, chênh lệch mua bán của SJC lên năm triệu, có lúc sáu triệu. Các chuyên gia được báo Thanh Niên dẫn lời gọi mức đó là cao bất thường." | Thanh Niên [40] (đã mở): "mức chênh lệch mua - bán lên tới 5 - 6 triệu đồng/lượng là cao bất thường", của "nhiều chuyên gia kinh tế"; bài **không** có chữ "chưa từng có". (Tuổi Trẻ [41] dùng "kỷ lục", nhưng chênh 5 triệu đã có 09–12/06/2026 [39].) |
| CH04 | "Nó nới rộng đúng lúc người ta hoảng muốn bán." (L223) | OK | — | Suy luận từ [40] (lực bán mạnh); 10/06 và 23/07 đều là lúc giá rơi. |
| CH04 | "Thứ hai… Giá vàng miếng SJC bằng giá vàng thế giới quy đổi, cộng một khoản chênh trong nước." (L224–225) | OK | — | Mô tả phổ thông ✓. |
| CH04 | "Ngày vía Thần Tài 2026, khoản chênh này khoảng hai mươi triệu một lượng." (L226) | OK | — | VnExpress [32] ✓ (thế giới 5.180 USD/oz). |
| CH04 | "…người mua hôm đó trả thêm khoảng một phần mười…" (L227) | OK | — | 20/185 = 10,8% (so với giá vàng thế giới quy đổi: 20/165 = 12%). "Khoảng một phần mười" là cách nói thận trọng ✓. |
| CH04 | "Ngày mười chín tháng tám, khoản chênh co lại, chỉ còn hơn hai triệu." (L228) | OK | — | Dân trí [42]: "thu hẹp xuống chỉ còn hơn 2 triệu đồng/lượng" ✓. |
| CH04 | "Phần trả thêm ấy có thể bốc hơi, kể cả khi giá thế giới đứng yên." (L229) | OK | — | Cơ chế; ví dụ thật 23/07/2026: thế giới −0,17% trong khi SJC rơi [40]. Có "có thể" ✓. |
| CH04 | Ví dụ vé xe Tết (L230) | OK | — | — |
| CH04 | "…đầu tháng mười, nó lại nới ra khoảng mười hai, mười ba triệu." (L231) | OK | — | 12,2 [44] – 12,8 (Kenh14 [47]) ✓. Nói được "không đi một chiều" ✓ (mặt trái). |
| CH04 | "Thứ ba: khan hàng, và 'mua trên giấy'. Quanh đợt sốt…, nhiều nơi thu đủ tiền rồi hẹn giao vàng sau bảy đến mười ngày, có đơn phải chờ tới chín mươi ngày." (L232–233) | OK | (tuỳ chọn) "thu tiền trước" thay "thu đủ tiền" | Vietnambiz [31]: "đặt cọc hoặc thanh toán đủ 100% tiền", vàng "7 đến 10 ngày… 90 ngày đối với các đơn hàng số lượng lớn" ✓. |
| CH04 | "Nếu giá rơi trong lúc chờ, người mua trên giấy không có vàng trong tay để bán." (L234) | OK | — | [31]: giá rơi 191,3 → 172 trong 48 giờ; giấy hẹn chỉ mua bán lại không chính thức. Câu điều kiện, đúng. |
| CH04 | "…quý một năm 2026, thu nhập bình quân của người lao động là chín triệu đồng một tháng." (L235) | OK | — | NSO 9,0 triệu [L01, positioning mục 1] ✓. |
| CH04 | "Một chỉ vàng… mua ngày 29/01 hết 19,13 triệu. Đầu tháng mười bán lại, nhận 14,05 triệu." (L236–237) | OK | — | 191,3/10 và 140,5/10 ✓. Màn hình ghi "vàng nhẫn, vàng miếng 1 chỉ có giá khác" ✓. |
| CH04 | "Mất khoảng năm triệu. Hơn nửa tháng lương." (L238) | OK | — | 5,08/9,0 = 56,4% ✓. |
| CH05 | "Giả sử bạn đã mua đúng hôm đó…" (L242) | OK | — | — |
| CH05 | Ví dụ đánh rơi / nhặt được năm trăm nghìn (L243) | OK | — | — |
| CH05 | "Kahneman và Tversky gọi đây là né sợ lỗ: người ta đo được mất so với một điểm mốc, và mất thì đau hơn được." (L244) | SỬA | "Kahneman và Tversky mô tả điều này, thường gọi là tâm lý sợ thua lỗ: người ta đo được mất so với một điểm mốc, và mất thì đau hơn được." | Nội dung đúng (1979 [60]: điểm tham chiếu, hàm giá trị dốc hơn ở vùng lỗ). Nhưng "né sợ lỗ" không phải thuật ngữ tiếng Việt quen dùng, nghe như lỗi gõ; thường dịch "tâm lý sợ thua lỗ" / "ngại lỗ". Chữ "loss aversion" cũng không phải tên gọi trong bài 1979 → "mô tả… thường gọi là". |
| CH05 | "Ước lượng của hai ông năm 1992: với người được khảo sát điển hình, một khoản lỗ nặng khoảng gấp đôi một khoản lãi cùng cỡ." (L245) | OK | — | λ trung vị 2,25, Tversky & Kahneman 1992 [61] ✓; "điển hình", "khoảng gấp đôi" đúng mức. |
| CH05 | "Với người mua đỉnh, điểm mốc là một trăm chín mươi mốt triệu ba trăm nghìn." (L246) | OK | — | — |
| CH05 | "Bán lại ở khoảng một trăm bốn mươi triệu là phải nhìn thẳng vào khoản lỗ hơn năm mươi triệu. Nên nhiều người chọn chờ." (L247) | SỬA | "…là phải nhìn thẳng vào khoản lỗ hơn năm mươi triệu. Nên rất dễ hiểu khi người ta muốn chờ." | 50,8 ✓. "Nhiều người chọn chờ" là khẳng định về hành vi thực tế, hồ sơ chỉ có kết quả tìm kiếm SECONDARY (và kết quả đó lại nói có người "nóng ruột tính bán"). Diễn thành giải thích tâm lý thì không cần số liệu. |
| CH05 | "Kênh không nói chờ là đúng hay sai. Chỉ là chờ bao lâu thì lịch sử trả lời rất khác nhau." (L248) | OK | — | Luật 2 ✓. |
| CH05 | "Theo dữ liệu giá SJC kênh tự tính, người mua đỉnh năm 2020 chờ khoảng mười chín tháng mới về lại giá đã trả." (L249) | OK | — | 62,45 → giá mua vào vượt lại giữa CSV 02/02/2022 (61,8) và 01/03/2022 (65,25) → 18–19 tháng ✓. CSV 2 điểm/tháng, nên "khoảng". |
| CH05 | "Người mua đỉnh năm 2011 chờ gần chín năm." (L250) | SỬA | "Người mua đỉnh năm hai nghìn không trăm mười một chờ gần chín năm. Hai lần ấy giá đều về lại, nhưng không có gì bảo đảm lần nào cũng vậy." | Số đúng: 49,12 → CSV 02/07/2020 mua 49,26 = 8 năm 10 tháng (CSV chỉ có từ 10/2018; giai đoạn 2012–2018 dựa vào hồ sơ). Nhưng hai ví dụ đều "về lại" mà không có câu chặn → người xem dễ hiểu thành "cứ giữ là sẽ về" (gần với khuyên giữ/dự báo, luật 2). Câu chặn ở L266 cách quá xa. |
| CH05 | HỎI "Vậy ai lỡ mua đúng đỉnh thì nên bán hay nên giữ?" / "Câu đó mình không trả lời thay bạn được, vì nó tuỳ khoản tiền ấy có ý nghĩa gì với bạn." (L251–252) | OK | — | Từ chối khuyến nghị đúng luật 2 ✓. |
| CH05 | "Nhưng có một câu hỏi giúp tách điểm mốc ra khỏi quyết định." (L253) | OK | — | — |
| CH05 | "Nếu lúc này mình đang cầm tiền mặt thay vì vàng, mình có dùng nó mua đúng chừng ấy vàng không? Và khoản tiền này, mình cần lại khi nào?" (L254) | SỬA | "Nếu lúc này mình đang cầm tiền mặt thay vì vàng, mình có dùng nó mua đúng chừng ấy vàng không? Và khoản tiền này, mình cần lại khi nào? Trả lời có hay không cũng không tự thành quyết định bán hay giữ; và nhớ rằng bán ra rồi mua lại cũng mất phần chênh lệch mua bán." | Câu "nếu cầm tiền mặt, có mua lại không" là một khung quyết định quen thuộc, nhưng ngầm dẫn tới "trả lời không → bán", tức là gần với khuyến nghị cho đúng câu HỎI "bán hay giữ". Nó cũng bỏ qua chi phí bán–mua lại mà chính CH04 vừa nhấn mạnh (3 triệu, có lúc 5–6). Thêm một câu cân bằng thì giữ được "công cụ tự quyết" (luật 2) mà không nghiêng về bán. Chữ trên màn hình giữ được. |
| CH06 | "Mình không bảo bạn nên mua, bán hay giữ vàng. Chỉ có năm câu hỏi…" (L258–259) | OK | — | Luật 2 ✓. |
| CH06 | "Một: …Nếu trong một, hai năm, mình có chịu được cảnh giá giảm hơn một phần tư không?" (L260) | OK | — | Giả định, dựa trên −26,6% đã xảy ra; không dự báo. |
| CH06 | "Hai: nếu ngày mai giá giảm mười phần trăm…" (L261) | OK | — | Phép thử giả định ✓. |
| CH06 | "Ba: mình đang trả thêm bao nhiêu?…" (L262) | OK | — | — |
| CH06 | "Bốn: mình mua vì đã so với các lựa chọn khác…" (L263) | OK | — | — |
| CH06 | "Năm: mình có nhận vàng ngay không?…" (L264) | OK | — | — |
| CH06 | "Và đây là lúc điều mình vừa nói không đúng với bạn." (L265) | OK | — | Luật 4 ✓. |
| CH06 | "Nếu bạn giữ rất lâu: theo kênh tự tính, người mua đúng đỉnh 2011, sau mười lăm năm vẫn được khoảng bảy phần trăm mỗi năm, chưa trừ lạm phát. Nhưng họ phải chịu gần chín năm âm, và quá khứ không bảo đảm tương lai." (L266) | OK | — | 49,12 → 140,5 sau 15,12 năm: ×2,860 → 7,20%/năm ✓. Có cả mặt trái + câu chặn ✓. |
| CH06 | Vàng cưới, hồi môn (L267) | OK | — | Hồ sơ mục 5 ý 3. |
| CH06 | "Nếu bạn mua đều từng ít một… Đó là cách nhiều người dùng, không phải công thức." (L268) | OK | — | Nguồn là ý kiến bạn đọc [6]; câu đã chặn "không phải công thức" ✓. |
| CH06 | Ký ức lạm phát (L269) | OK | — | Không nêu số ✓. |
| CH06 | "Và đừng lật ngược bài học: đỉnh năm 2020 lại đến khi phố vàng vắng khách. Không có hàng dài cũng không có nghĩa là an toàn." (L270) | SỬA | "Và đừng lật ngược bài học: quanh đỉnh năm hai nghìn không trăm hai mươi, báo chí ghi không còn cảnh đổ xô, xếp hàng mua vàng như những năm trước. Không có hàng dài cũng không có nghĩa là an toàn." | "Phố vàng vắng khách / lác đác" trong 24h [9] tả **11/2021**, không phải đỉnh 08/2020. Nguồn duy nhất cho lúc đỉnh là NLĐ [8] ("không còn hiện tượng đổ xô, xếp hàng"; NHNN: "tình hình mua, bán vàng miếng trầm lắng"). Không đủ để nói "vắng khách". |
| CH06 | "Tóm lại, người đứng trong hàng không dại. Họ chỉ làm điều bộ não vẫn làm…" (L271–272) | OK | — | Không chế giễu ✓. |
| CH06 | "Lần tới thấy ảnh hàng dài, câu đáng hỏi không phải 'đỉnh chưa', vì không ai biết…" (L273–274) | OK | — | Chống dự báo ✓. |
| CH06 | Câu hỏi bình luận (L275) | OK | — | — |

### 1c. Chữ và cảnh trên màn hình (Kế hoạch hình ảnh)

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Màn hình CH00 | `counter` 152,8 → 191,3 "GIÁ BÁN RA SJC · 13:25 · 29/01/2026 · CAO NHẤT LỊCH SỬ" (L44) | OK | — | [48], [30] ✓. |
| Màn hình CH00 | `race` 29/01 → 30/09 + mark "≈ −26%" (L45–47) | SỬA | Ghi đè điểm 30/09 thành **141,1 / 144,1** (chốt chiều) trước khi xuất; mark "≈ −26%" giữ được; sửa ghi chú "kết thúc ≈ −26,4%" thành "≈ −25,6%" | CSV 30/09 (139,5/142,5) = giá chốt 29/09 lặp lại; Báo Đà Nẵng 30/09 16:52: "141,1 triệu đồng/lượng mua vào và 144,1 triệu đồng/lượng bán ra", +1,6 so phiên trước [L01-45]. CSV 01/10 cũng lặp 139,5 (VOV 01/10: 140,8/143,8). Từ điểm đầu CSV 189,6: 141,1/189,6 − 1 = −25,6%; so với 191,3: −26,2%. |
| Màn hình CH00 | `slam` "≈ −51 TRIỆU / LƯỢNG · BÁN LẠI ĐẦU THÁNG 10 (GIÁ MUA VÀO 140,5) · HƠN 1/4 SỐ TIỀN" (L48) | OK | — | ✓. |
| Màn hình CH01 | `kinetic` "23/08/2011 · ĐỈNH 49,12 TRIỆU → CUỐI 2013: 34,77 (−29%)" (L55) | OK | — | [1][5]; 34,77/49,12 − 1 = −29,2% ✓. |
| Màn hình CH01 | `quote` "» Không có hiện tượng đổ xô, xếp hàng." — nguồn: Người Lao Động 09/02/2021 / 24h (L56–57) | SỬA | "» Không còn hiện tượng đổ xô, xếp hàng mua vàng như những năm trước." — nguồn: "Người Lao Động, 09/02/2021 (nhìn lại đỉnh 08/2020)" | Như L153. Bỏ "24h": bài 24h không có câu này. |
| Màn hình CH01 | `ledger` "MƯỜI HAI THÁNG SAU" +11% · +45% · +93% · +35% · +7% (L58–60) | OK | — | Tính lại khớp. |
| Màn hình CH01 | `counter` 124 → 167,5 "+35%" (L64) | OK | — | ✓. |
| Màn hình CH01 | `ledger` "2026 · TỚI ĐẦU THÁNG 10": −26,6 · −23,6 · −26,4 · −17,8 (L65) | OK | — | ✓. |
| Màn hình CH01 | `timeline` + `bars` 4 · 5 · 2 (L66–67) | OK | — | Khớp hồ sơ. |
| Màn hình CH01 | `slam` "HÀNG DÀI ≠ CHUÔNG BÁO ĐỈNH" sub "NÓ BÁO: GIÁ VỪA TĂNG RẤT NHANH" (L68) | SỬA | sub: "THƯỜNG ĐẾN SAU MỘT CÚ TĂNG NHANH" | Như L161 (D, K, ngày vía). |
| Màn hình CH01 | `kinetic` "VNEXPRESS 2025: 'NỖI ÁM ẢNH' CƠN SỐT VÀNG 2011" (L69) | SỬA | "VNEXPRESS 2025 (Ý KIẾN BẠN ĐỌC): 'NỖI ÁM ẢNH' SAU CÚ SỐC VÀNG 2011" | Như L165. |
| Màn hình CH02 | `kinetic` "Barber & Odean (2008): NHÀ ĐẦU TƯ CÁ NHÂN MUA RÒNG CỔ PHIẾU 'GÂY CHÚ Ý' · KHÔNG CÓ LỢI NHUẬN VƯỢT TRỘI" (L74–75) | SỬA | "Barber & Odean (2008), DỮ LIỆU MỸ: NHÀ ĐẦU TƯ CÁ NHÂN MUA RÒNG CỔ PHIẾU 'GÂY CHÚ Ý'" | Như L174. |
| Màn hình CH02 | `kinetic` "01/01 → 29/01/2026: 152,8 → 191,3 · +25% TRONG 4 TUẦN" (L80–81) | OK | — | +25,2% ✓. Không dùng `race` là đúng, nhưng lý do trong script ("+22%") chưa chính xác: theo giá mua vào CSV 150,8 → 186,6 = +23,7% (theo giá mua vào báo, 150,8 → 188,3 = +24,9%). |
| Màn hình CH02 | `kinetic` "Greenwood & Shleifer (2014): VỪA TĂNG MẠNH → KỲ VỌNG TĂNG TIẾP CAO NHẤT" (L82) | SỬA | "Greenwood & Shleifer (2014), CHỨNG KHOÁN MỸ 1963–2011: VỪA TĂNG MẠNH → CÀNG KỲ VỌNG TĂNG TIẾP" | Bài nói tương quan dương, không nói "cao nhất"; thiếu phạm vi. |
| Màn hình CH02 | `kinetic` "QUÀ CƯỚI CHO CON, CHO EM — LÝ DO THẬT" sub "CafeF, 29/01/2026" (L83) | OK | — | [28] ✓. |
| Màn hình CH03 | `bars` 2024 42,1 · 2025 36,1; "−14% · WGC" (L86) | OK | — | ✓. |
| Màn hình CH03 | `kinetic` "THIẾU VÀNG MIẾNG SJC → CAO HƠN THẾ GIỚI > 550 USD/OZ" sub "WGC, cuối 2025" (L87) | OK | — | ✓. |
| Màn hình CH03 | `ledger` "GIỚI HẠN MỖI NGƯỜI": … 29/01/2026 TỪ 4 CHỈ: PHIẾU HẸN · 23/03/2026 BỎ GIỚI HẠN (L88–89) | SỬA | "… 22/04/2025 2 CHỈ (CÓ NƠI) · … · 29/01/2026 TRÊN 4 CHỈ: PHIẾU HẸN (CÓ NƠI) · 23/03/2026 CÓ TIỆM BỎ GIỚI HẠN" | Như L130, L156; [38] nói về một số tiệm. |
| Màn hình CH03 | `kinetic` "29/01: CÓ NGƯỜI XẾP HÀNG 11H → 15H ĐỂ BÁN 2 LƯỢNG" (L90) | SỬA | "29/01: CÓ NGƯỜI XẾP HÀNG 11H → 15H VẪN CHƯA TỚI LƯỢT BÁN 2 CHỈ" | Như L202 — sai đơn vị. |
| Màn hình CH03 | `ledger` "MUA NGÀY VÍA": +11% · +93% · −24% → "3 NĂM · 3 KẾT QUẢ" (L93) | OK | — | ✓. |
| Màn hình CH03 | `quote` "» Một chỉ vàng bằng cả tháng lương." — một khách hàng, VnExpress 26/02/2026 (L94) | OK | — | ✓. |
| Màn hình CH04 | `ledger` 191,3 · 188,3 · 3 TRIỆU ≈ 1,6% (L97) | OK | — | ✓. |
| Màn hình CH04 | `bars` "CHÊNH MUA–BÁN SJC": 01/01 2 · 29/01 3 · 10/06 5 · 23/07 6 (CÓ LÚC); nhãn "CHƯA TỪNG CÓ — Thanh Niên" (L98–99) | SỬA | Nhãn 23/07: "CAO BẤT THƯỜNG — chuyên gia, Thanh Niên" | Như L222. Số cột ✓ ([48], [30], [39], [40]). |
| Màn hình CH04 | `bars` "SJC CAO HƠN THẾ GIỚI": 20,8 · ~20 · ~2 · ~12,5 (L101) | OK | — | [26][32][42][44][47] ✓. |
| Màn hình CH04 | `kinetic` "MUA TRÊN GIẤY: TRẢ 100% · GIAO SAU 7–10 NGÀY · ĐƠN LỚN TỚI 90 NGÀY" (L103) | SỬA | "MUA TRÊN GIẤY: ĐẶT CỌC HOẶC TRẢ ĐỦ 100% · GIAO SAU 7–10 NGÀY · ĐƠN LỚN TỚI 90 NGÀY" | [31]: "đặt cọc hoặc thanh toán đủ 100%". |
| Màn hình CH04 | `ledger` 1 chỉ 19,13 → 14,05 → `counter` 5.080.000 đ "≈ 56% THÁNG LƯƠNG 9 TRIỆU" (L104–106) | OK | — | ✓. |
| Màn hình CH05 | `kinetic` "MẤT 500 NGHÌN ≈ ĐAU GẤP ĐÔI…" sub "trung vị λ ≈ 2,25" (L110) | OK | — | [61] ✓. |
| Màn hình CH05 | `timeline` "BAO LÂU MỚI VỀ LẠI GIÁ MUA": ≈ 19 THÁNG · GẦN 9 NĂM, "kênh tự tính" (L113–114) | OK | — | ✓ (nên thêm dòng nhỏ "không bảo đảm lần sau", khớp L250 đã sửa). |
| Màn hình CH05 | `question` "Lỡ mua đỉnh: bán hay giữ?" → "KÊNH KHÔNG TRẢ LỜI THAY BẠN" → `kinetic` hai câu hỏi (L115–116) | OK | — | Luật 2 ✓. |
| Màn hình CH06 | `ledger` "KHI NÀO KHÔNG ĐÚNG" (5 thẻ), thẻ 1 "≈ 7,2%/năm danh nghĩa, chưa trừ lạm phát · kênh tự tính" (L120–121) | OK | — | ✓. |

## 2. Kiểm luật kênh (positioning mục 1)

| Luật | Kết quả |
|---|---|
| 1. Không bán gì | OK — không link, không nhóm; "nhóm Zalo" chỉ là ví dụ. Không nêu tên tiệm/doanh nghiệp vàng ngoài SJC trong lời thoại ✓ (nguồn [13] BTMC chỉ ở Ghi chú). |
| 2. Không dự báo / không khuyến nghị | Tổng thể OK (L143, L248, L252, L258, L266, L273). Ba chỗ cần sửa: **L254** (câu "cầm tiền mặt có mua lại không" ngầm dẫn tới bán, cần câu cân bằng), **L250** (hai lần "về lại" không có câu chặn → nghe như "giữ thì sẽ về"), **L161** (khẳng định quá dữ liệu). Không câu nào nói "nên mua/bán/giữ" ✓. |
| 3. Mọi số có nguồn | Có; số tự tính đều tính lại khớp (mục 4). Bốn chỗ ghi nguồn sai: L153 (nguyên văn), L202 (2 chỉ), L222 (Thanh Niên không viết "chưa từng có"), L270 (24h tả 11/2021). |
| 4. Nói cả mặt trái | Có (L265–270) và tốt; L270 cần sửa câu dẫn nguồn. |
| 6. Dữ liệu quá khứ | Biểu đồ dừng 30/09 ✓ — nhưng điểm 30/09 trong CSV sai (mục 1c). Giá "đầu tháng mười" chỉ dùng trong lời đọc ✓. |
| Không chế giễu người mua / tục ngày vía | OK nhìn chung (L189–191, L204, L210, L271). L205 nên thêm vế "cách để người ta tin, hy vọng vào năm mới" như nguồn — hiện chỉ giữ vế "tâm lý hơn là khoa học". |

## 3. TTS — chỗ dễ đọc sai

| Chỗ | Rủi ro | Gợi ý (chỉ trong bản gửi TTS) |
|---|---|---|
| "SJC" (L131, 185, 198, 222, 225, 249, 262) | Đọc tiếng Anh "ét-jay-xi", hoặc gộp thành một từ | Chọn một cách và giữ cố định, ví dụ "ét-giê-xê"; nghe thử một câu. |
| "FOMO" (L176) | "Phô-mô" / "ép-o-em-o" / "fô-mâu" | "phô-mô"; câu đã giải nghĩa "sợ bị bỏ lỡ" trước ✓. |
| "Zalo" (L178) | Thường đọc đúng "da-lô"; nghe thử | — |
| "VnExpress" (L165, 211) | "vi-en-ếch-prét" vấp | "Vi-en Ếch-prét" hoặc "báo Vi-en Ếch-prét". |
| "Tversky", "Kahneman" (L172, 244, 245 → "hai ông") | "Tê-véc-xki", "Ka-nê-man" | "Tvéc-xki", "Ca-nơ-men"; nghe thử. |
| "Barber", "Odean" (L174) | "Bác-bơ", "Ô-đi-ân" lạ | "Bác-bơ và Ô-đin". |
| "Greenwood", "Shleifer" (L186) | "Grin-vút", "Sơ-lai-phơ" | Nghe thử; có thể nói "hai nhà kinh tế học ở Harvard" nếu quá vấp (thông tin đúng). |
| "Thần Tài", "mùng mười tháng Giêng" | An toàn | — |
| "một phẩy sáu phần trăm" (L219) | An toàn | — |
| "năm một nghìn chín trăm chín mươi hai" (L245) | Dài nhưng đúng | — |
| "‖", "HỎI:", "»" | Đọc ra thành tiếng | Lọc trước khi gửi TTS (Ghi chú đã nêu ✓). |
| Chữ số | Lời thoại CH00–CH06 không còn chữ số nào (đã grep) ✓. | — |

## 4. Tính lại các số trong "Ghi chú"

| Mục Ghi chú | Kết quả tính lại / đối chiếu | Kết luận |
|---|---|---|
| Cold open 191,3 → 140,5 = −50,8, −26,6%; 139,9 → −51,4 (−26,9%) | −50,8 / −26,56%; −51,4 / −26,87% | OK |
| 2011 hoà vốn: CSV 02/07/2020 49,26 ≈ 8 năm 10 tháng | 23/08/2011 → 02/07/2020 = 8 năm 10 tháng; điểm CSV đầu tiên có mua > 49,12 (bỏ qua dòng lỗi 01/01/2020 = 140,5) | OK |
| 2020 hoà vốn: 01/03/2022 65,25 (01/02/2022 61,8) ≈ 19 tháng | 07/08/2020 → 01/03/2022 = 18,8 tháng; vượt lại ở đâu đó 02/02–01/03/2022 → 18–19 tháng | OK |
| Năm đợt: +11,2 · +45,5 · +93 · +35,1 · +7,4% | 86,8/78,05 = +11,21% · 114,9/78,98 = +45,48% · 174,2/90,3 = +92,91% · 167,5/124 = +35,08% · 145,4/135,4 = +7,39% | OK |
| Bốn đợt 2026 tới 140,5 | −26,56 · −23,64 (185: −24,05) · −26,40 · −17,84% | OK |
| Bảng điểm 4/5/2; "~54 → +4,6%" cho người xếp hàng cuối 07/2020 | CSV 27/07/2020 = 55,45/56,9 (cuối tháng 7) → CSV 02/08/2021 mua 56,5 = **−0,7%**. "~54" (SECONDARY) có vẻ là giá giữa tháng 7 | Nếu thêm lại câu này: nói "khoảng hoà vốn sau một năm", không nói "+4,6%" |
| "Mười bốn năm sau" | 23/08/2011 → 20/03/2025 = 13,6 năm | SỬA (L165: "hơn mười ba năm") |
| +25% trong 4 tuần | 191,3/152,8 = +25,20% | OK |
| Chênh mua–bán 29/01 1,57% | 3/191,3 = 1,568% | OK |
| "Một phần mười" = 20/185 = 10,8% | 10,81% | OK |
| 23/03/2026 "thấp hơn đỉnh hơn hai mươi triệu" | Bài [38]: 9:58 SJC 164/167, "khoảng 24,5 triệu"; 191,3 − 167 = 24,3; CSV 23/03 166 → 25,3 | OK |
| Thần Tài +11,2 / +93 / −23,6 | Như trên | OK |
| 1 chỉ: −5,08 triệu, 56% | 19,13 − 14,05 = 5,08; 5,08/9,0 = 56,4% | OK |
| "Chờ bốn tiếng… bán 2 lượng" [29] | Nguồn: **2 chỉ**, 11h → 15h chưa tới lượt | SỬA (L202, màn hình CH03) |
| Giữ lâu 7,2%/năm | 140,5/49,12 = 2,860; 15,12 năm → 7,20%/năm | OK |
| λ = 2,25 | Trung vị, T&K 1992 [61] | OK |
| `race` CH00 kết thúc ≈ −26,4% | Dùng CSV 30/09 lỗi (139,5). Với 141,1 chốt chiều: −25,6% (từ 189,6 CSV), −26,2% (từ 191,3) | SỬA ghi chú; mark "≈ −26%" vẫn đúng |
| `race` 04/06/2024 → 03/06/2025 ≈ +44% | 114,9/79,98 = +43,7% | OK |
| J "cách đỉnh 1,7 triệu" (không còn trong lời đọc) | 191,3 − 190,9 = 0,4; số 1,7 của [35] có thể so với một mốc khác | Không chặn |

**Hồ sơ `2026-10-07-long-d1-research.md` cần sửa theo:** mục "Phát hiện bất ngờ" ("bán 2 lượng" → "2 chỉ"); bảng 1.1 dòng B và
Tóm tắt #2 (lời trích NLĐ đúng là "không còn hiện tượng đổ xô, xếp hàng mua vàng như những năm trước"; [9] 24h không nói phố
vắng lúc đỉnh 2020 — "lác đác" là 11/2021); bảng 3.1 dòng 23/07 và [40] ("cao bất thường", không phải "chưa từng có"); mục 5 ý 6
("lác đác" → nguồn chỉ là NLĐ); bảng 1.1 dòng H "hết hàng" là một tiệm; dòng B "~54 → +4,6%" (xem trên); mục 7 thêm: CSV 30/09 và
01/10/2026 đều là giá 29/09 lặp lại.

## 5. Nguồn đã mở trong lần fact-check này

- Người Lao Động (tuoitre.vn/nld) 09/02/2021 [8] — nguyên văn "không còn hiện tượng đổ xô, xếp hàng mua vàng như những năm trước": https://tuoitre.vn/nld/kinh-te/1-nam-song-gio-cua-gia-vang-sjc-khi-vuot-dinh-62-trieu-dong-luong-20210209002616492.htm
- 24h 17/11/2021 [9] — "lác đác" là 11/2021; "xếp hàng xuyên trưa… cuối tháng 7/2020": https://www.24h.com.vn/thi-truong-tieu-dung/gia-vang-tang-du-doi-vuot-moc-62-trieu-dong-canh-tuong-bat-ngo-o-pho-vang-tran-nhan-tong-c52a1307504.html
- Báo Pháp luật 11/08/2020 [7] — 62,45: https://doanhnhan.baophapluat.vn/chi-sau-1-dem-gia-vang-sjc-boc-hoi-tiep-12-trieu-dongluong-31995.html
- Báo Đắk Lắk [1]; DTTC [2] — 49,12 ngày 23/08/2011; xếp hàng 09/08/2011 (link trong hồ sơ)
- VnExpress 20/03/2025 [6] — ý kiến bạn đọc: https://vnexpress.net/noi-am-anh-sau-cu-soc-vang-len-50-trieu-roi-lao-doc-nam-2011-4863794.html
- CafeF 29/01/2026 [28]; Phụ Nữ Online 29/01/2026 [29] ("2 chỉ vàng"); webgia 29/01/2026 [30] (link trong hồ sơ)
- Vietnambiz 04/02/2026 [31]; VnExpress 26/02/2026 [32]; VOV 22/04/2025 [20]; Tuổi Trẻ 07/02/2025 [19] (link trong hồ sơ)
- Vàng siêu nhỏ ngày vía 2026: https://suckhoedoisong.vn/ngay-via-than-tai-2026-vang-sieu-nho-hut-khach-169260226110957011.htm ; https://danviet.vn/ngay-via-than-tai-2026-gia-vang-cao-chot-vot-nguoi-dan-san-san-pham-vang-sieu-nho-d1405642.html
- Vietstock qua Investing 23/03/2026 [38]: https://vn.investing.com/news/commodities-news/tiem-vang-o-at-xa-hang-cho-mua-thoai-mai-khi-gia-chenh-toi-gan-30-trieuluong-2568859
- Thanh Niên 23/07/2026 [40] ("cao bất thường"); Tuổi Trẻ 23/07/2026 [41] ("kỷ lục"); Dân trí 19/08/2026 [42]; VietnamPlus 06/10/2026 [46]; Kenh14 06/10/2026 [47] (12,8 triệu) (link trong hồ sơ)
- SJC 30/09/2026 chốt chiều 141,1/144,1: https://baodanang.vn/gia-vang-ngay-30092026-sjc-tang-len-1411-1441-trieu-dongluong-3353622.html ; VOV 01/10: https://vov.vn/thi-truong/gia-vang-hom-nay-110-vang-sjc-giam-con-1408-1438-trieu-dongluong-post1337397.vov
- Xếp hàng khác năm 2025: https://nld.com.vn/gia-vang-mieng-sjc-lap-dinh-nhieu-nguoi-o-tp-hcm-xep-hang-cho-mua-196250826140124765.htm ; https://tuoitre.vn/xep-hang-mua-vang-2025092208193267.htm
- SGGP 07/09/2025 [26] (qua kết quả tìm kiếm; sggp.org.vn lỗi DNS): 1 lượng vàng miếng/ngày, chênh >20 triệu
- Tiền Phong 05/02/2025 [74] — Ngô Hương Giang, "nhà nghiên cứu văn hoá": https://tienphong.vn/co-nen-mua-vang-ngay-via-than-tai-post1714576.tpo
- WGC FY2025 [53] (qua bản sao PDF và VOV English): 42,1 → 36,1 tấn, >550 USD/oz
- Greenwood & Shleifer (2014) — tóm tắt (SSRN 2199762 / OUP): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2199762 (Harvard lỗi DNS)
- Barber & Odean (2008) — tóm tắt (EconPapers): https://econpapers.repec.org/RePEc:oup:rfinst:v:21:y:2008:i:2:p:785-818 (toàn văn Berkeley lỗi DNS; SSRN/ResearchGate 403 → vế "lợi nhuận vượt trội" chưa kiểm được)

**Việc còn mở (không chặn bản 2):** bài gốc Vietstock 23/03/2026 trên vietstock.vn; toàn văn Barber & Odean nếu muốn giữ vế lợi
nhuận; sửa hồ sơ theo mục 4; ghi đè điểm 30/09 trong `race`.
