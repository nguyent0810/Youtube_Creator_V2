# Fact-check — script.md (bản 1) · ck-2026-kenh-dau-tu

Ngày kiểm: 06/10/2026. Đối chiếu: hồ sơ `docs/channels/chung-khoan/2026-10-06-long-01-research.md` (số `[n]` = nguồn trong hồ sơ),
luật cứng `2026-10-06-positioning.md` mục 1, dữ liệu kênh `data/ck/*.csv`. Không sửa script.

**Kết luận: OK 71 · SỬA 24 · BỎ 1** (95 hàng: tiêu đề + các dòng thoại, vài dòng gộp). Mục TTS và Ghi chú ở cuối, không tính vào tổng.

Nhãn: OK = đúng nguồn / chấp nhận được · SỬA = sai số, nói quá nguồn, mơ hồ, hoặc chạm luật kênh · BỎ = nên cắt câu.

## 1. Bảng kiểm từng dòng

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Tiêu đề | "MỌI KÊNH ĐẦU TƯ ĐỀU ĐỎ — CHỈ SỔ TIẾT KIỆM XANH" (L1) | SỬA | "NĂM 2026: BỐN KÊNH QUEN THUỘC ĐỀU ĐỎ — SỔ TIẾT KIỆM XANH. NHƯNG THẮNG THẬT KHÔNG?" | "Mọi kênh" nói quá: video chỉ xét 5 kênh; giá sơ cấp căn hộ một số nơi vẫn tăng [75][82]; sổ tiết kiệm Big-4 đầu năm lãi thực ≈ −0,3% (mục 5.4). |
| CH00 | "Đầu năm hai nghìn không trăm hai mươi sáu, giả sử bạn có một trăm triệu đồng." (L19) | OK | — | Giả định minh hoạ (hồ sơ mục 0). |
| CH00 | "…chia đều cho năm kênh mà người Việt hay chọn nhất." (L20) | SỬA | "…chia đều cho năm kênh quen thuộc với nhiều người Việt." | "Hay chọn nhất" là xếp hạng không có nguồn trong hồ sơ (luật 3). |
| CH00 | "Hai mươi triệu vào chứng khoán / mua vàng miếng / mua Bitcoin" (L21–23) | OK | — | Giả định. |
| CH00 | "Hai mươi triệu cho nhà đất." (L24) | SỬA | "Hai mươi triệu cho nhà đất — dĩ nhiên hai mươi triệu không mua được mảnh đất nào, nên kênh này mình chỉ nhìn xu hướng chung." | Hồ sơ mục 0 khuyến nghị nói rõ "20 triệu không mua được nhà đất", không đưa một con số duy nhất. |
| CH00 | "Và hai mươi triệu gửi tiết kiệm mười hai tháng ở một ngân hàng lớn." (L25) | OK | — | Không nêu tên ngân hàng ✓. |
| CH00 | "Chín tháng sau, cuối tháng chín, mình mở sổ ra xem." (L26) | OK | — | Mốc 30/09 khớp luật 6. |
| CH00 | "Chứng khoán: gần như đứng yên, hơi âm." (L27) | OK | — | 1.784,49 → 1.768,62 = −0,89% (CSV, khớp [8]). Chỉ số giá, chưa gồm cổ tức — đã ghi trên màn hình theo Ghi chú. |
| CH00 | "Vàng: mất gần tám phần trăm." (L28) | OK | — | Mua 152,8 (01/01) → bán 141,1 (30/09) = −7,7% [44][45]. |
| CH00 | "Bitcoin: âm khoảng bốn phần trăm." (L29) | SỬA | "Bitcoin: tính theo giá đô la, âm khoảng bốn phần trăm." | −4,3% là theo USD (87.498 → 83.767 [61][58]). Ví dụ bỏ tiền đồng (20 triệu), nhưng chuỗi kênh `btc_vnd_1d.csv` cho −6,5% (31/12/2025 → 30/09/2026). Tỷ giá ngầm định trong CSV giảm 26.559 → 25.931 VND/USD, ngược với tỷ giá trung tâm +2,01% [97] → chuỗi VND có vấn đề nguồn giá; đừng dùng nó cho biểu đồ cold open cho tới khi kiểm lại. |
| CH00 | "Nhà đất: giá rao giảm, và quan trọng hơn, rất khó bán." (L30) | OK | — | Giá rao −2–3% [74]; giao dịch = 63,7% cùng kỳ, hấp thụ đất nền 4–7% [73][75]. |
| CH00 | "Chỉ có cuốn sổ tiết kiệm là còn màu xanh." (L31) | OK | — | +3,9% danh nghĩa; CH04 nói rõ phần lãi thực. |
| CH00 | "Câu trả lời ngắn là: có, nhưng thắng ít hơn bạn tưởng rất nhiều." (L33) | SỬA | "Câu trả lời ngắn là: thắng trên giấy, nhưng ít hơn bạn tưởng rất nhiều." | Chữ "có" đáp câu "cứ gửi ngân hàng là thắng à?" dễ nghe thành lời khuyên (luật 2), và mâu thuẫn với CH04: sau lạm phát, người gửi Big-4 từ đầu năm ≈ −0,3% thực (1,039/1,042). |
| CH00 | Ba câu hỏi lộ trình + câu giới thiệu kênh (L34–38) | OK | — | Không có dữ kiện. |
| CH01 | "Cuối năm 2025, VN-Index đóng cửa ở 1.784 điểm." (L42) | OK | — | 1.784,49 ngày 31/12/2025 (CSV). |
| CH01 | "Cuối tháng chín năm nay, nó ở quanh 1.768 điểm." (L43) | OK | — | 1.768,62 ngày 30/09 (CSV, [8]). |
| CH01 | "Giảm chưa tới một phần trăm." (L44) | OK | — | −0,89%. |
| CH01 | "Tháng ba, căng thẳng ở Trung Đông đẩy giá dầu vượt 118 đô la một thùng." (L47) | OK | — | [7] bằng chứng. |
| CH01 | "Chỉ trong một tháng, VN-Index mất gần 11%, chạm đáy năm ở 1.586 điểm." (L48) | OK | — | Tháng 3: 1.880,33 → 1.674,49 = −10,95% (CSV). 1.586,44 là **đáy trong phiên** 23/03; đáy đóng cửa 1.591,17. "Chạm" đúng với số trong phiên — biểu đồ đóng cửa phải ghi nhãn "trong phiên 1.586" để khớp lời. |
| CH01 | "Rồi tháng tư, nó bật lên hơn 10%, và tới tháng năm thì lập đỉnh năm, 1.933 điểm." (L49) | OK | — | Tháng 4 +10,73% (CSV). 1.933,11 là **đỉnh trong phiên** 19/05; đỉnh đóng cửa 1.927,94 (18/05). Nhãn biểu đồ: ghi rõ "trong phiên". |
| CH01 | "Sau đó lại trôi xuống." (L50) | OK | — | Đỉnh → 30/09: −8,5%. |
| CH01 | "Từ đáy lên đỉnh là hơn hai mươi phần trăm." (L51) | OK | — | +21,2% (đóng cửa) / +21,9% (trong phiên). |
| CH01 | "…nhưng người vào sai thời điểm vẫn có thể lỗ nặng." (L52) | SỬA | "…nhưng ai mua theo chỉ số đúng đỉnh tháng năm thì tới cuối tháng chín vẫn lỗ gần chín phần trăm." | "Lỗ nặng" nói quá với mức chỉ số: đỉnh 1.933,11 → 1.768,62 = −8,5% (tới 06/10: −9,0%). Có số cụ thể thì rõ hơn và đúng luật 3. |
| CH01 | "Đúng, nâng hạng có hiệu lực từ hai mươi mốt tháng chín." (L54) | OK | — | LSEG/FTSE [23]. |
| CH01 | "Nhưng tiền từ các quỹ chỉ số mới chỉ vào đợt đầu khoảng mười phần trăm, trong khi khối ngoại đã bán ròng chín tháng liên tiếp, gần chín mươi lăm nghìn tỷ đồng trên sàn HOSE." (L55) | SỬA | "…trong khi khối ngoại đã bán ròng chín tháng liên tiếp, hơn chín mươi lăm nghìn tỷ đồng trên sàn HOSE." | Số đúng là **hơn 95.479,7 tỷ** [9] — "gần 95 nghìn tỷ" ngụ ý dưới 95. Đợt đầu 10% [24][21] OK; "9 tháng liên tiếp" là số toàn thị trường [27] — vẫn đúng. (Chữ "HOSE" là phạm vi số liệu, không phải quảng bá — không vi phạm luật "không nêu tên sàn", nhưng xem mục TTS.) |
| CH01 | "Tháng chín, thanh khoản xuống thấp nhất mười chín tháng." (L56) | OK | — | [8] (~16.434 tỷ/phiên HOSE); CafeF: thấp nhất từ 02/2025 [27]. |
| CH01 | "Những nhịp lên xuống lớn nhất năm nay đều có dấu tay của một nhóm cổ phiếu vốn hoá rất lớn." (L58) | SỬA | "Nhiều nhịp lên xuống lớn năm nay có dấu tay của một nhóm cổ phiếu vốn hoá rất lớn." | "Đều" nói quá: nhịp lớn nhất (tháng 3, −10,9%) nguồn gán cho Trung Đông/giá dầu, không phải nhóm Vingroup [7][12]; nhóm này kéo ở T4–T7, T9 [14][18][8]. |
| CH01 | "Nửa đầu năm, VN-Index tăng hơn bốn phần trăm, nhưng nếu bỏ nhóm đó ra, chỉ số lại âm gần hai phần trăm." (L59) | OK | — | +4,23% / −1,81% [115]; CSV 30/06: +4,23% ✓. |
| CH01 | "Nghĩa là con số VN-Index bạn thấy trên tin tức, có khi rất khác với tài khoản của chính bạn." (L60) | OK | — | Diễn giải; quỹ cổ phiếu TB −1,12% nửa đầu năm [115]. |
| CH01 | "Mình sẽ có hẳn một bài trong khoá Chứng khoán từ số không…" (L61) | OK | — | Chuỗi miễn phí (định vị mục 3C), không phải khoá trả phí. |
| CH02 | "Ngày 29/01 năm nay, ở Hà Nội, người ta xếp hàng nhiều giờ để mua vàng. Có người chờ từ trưa đến chiều… Có tiệm hết hàng." (L65–66) | OK | — | [56] (chờ 11h–15h, một số tiệm hết hàng). |
| CH02 | "Cũng chính ngày hôm đó, giá vàng miếng SJC lập đỉnh: 191,3 triệu đồng một lượng." (L67) | OK | — | [47][48] (188,3/191,3 lúc 13:25). **Lưu ý dựng:** `sjc_1d.csv` ngày 29/01 ghi 186,6/189,6 (một lần chụp/ngày) → đỉnh trên biểu đồ sẽ là 189,6, lệch lời 191,3. Thêm điểm 191,3 bằng tay hoặc ghi chú trên hình. |
| CH02 | "Ngày hôm sau, ở Mỹ, Tổng thống Trump đề cử ông Kevin Warsh làm Chủ tịch Cục Dự trữ Liên bang." (L68) | OK | — | 30/01/2026 [37]. |
| CH02 | "Thị trường cho rằng ông sẽ cứng rắn hơn với lạm phát, đồng đô la bật tăng, và vàng thế giới rơi mạnh." (L69) | OK | — | [37]: USD bật từ đáy 4 năm, vàng −5% (có lúc dưới 5.000). Kịch bản đã dùng "rơi mạnh", không dùng "mạnh nhất nhiều thập kỷ" (SECONDARY) ✓. |
| CH02 | "Tháng ba, khi giá dầu tăng vọt, giới đầu tư gần như xoá hết hy vọng lãi suất Mỹ sẽ giảm trong năm nay." (L70) | OK | — | [38]. Không nói "Fed tăng lãi suất" trước 16/09 ✓. |
| CH02 | "Vàng, vốn không trả lãi, càng kém hấp dẫn." (L71) | OK | — | Cơ chế lợi suất thực [40]; đây là giải thích, không dự báo. |
| CH02 | "Đến đầu tháng mười, vàng miếng chỉ còn khoảng một trăm bốn mươi triệu đồng một lượng khi bán ra." (L72) | SỬA | "Đến đầu tháng mười, nếu bạn bán lại cho tiệm, mỗi lượng vàng miếng chỉ còn khoảng một trăm bốn mươi triệu đồng." | "Giá bán ra" trong tiếng Việt thường hiểu là giá **tiệm bán** (142,9–143,5), còn 140 là giá **tiệm mua vào** (139,9–140,5) [46]. Câu gốc mơ hồ. |
| CH02 | "Người mua đúng đỉnh hôm xếp hàng, nếu bán bây giờ, lỗ khoảng năm mươi mốt triệu đồng mỗi lượng." (L73) | SỬA | "Người mua đúng đỉnh hôm xếp hàng, nếu bán vào đầu tháng mười, lỗ khoảng năm mươi mốt triệu đồng mỗi lượng." | Số đúng: 191,3 − 140,5 = 50,8; − 139,9 = 51,4 [43]. "Bây giờ" sẽ sai khi video được xem về sau, và chạm luật 6 (không bình luận giá hiện tại). |
| CH02 | "Còn người mua từ ngày đầu năm thì mất khoảng tám phần trăm." (L74) | OK | — | −7,7% (30/09) / −8,4% (06/10). |
| CH02 | "Giá mua vào và bán ra của vàng miếng chênh nhau khoảng ba triệu đồng." (L76) | OK | — | ~3 triệu phần lớn năm 2026 [44][45][46] (01/01 là 2 triệu). |
| CH02 | "…ngay khi bạn vừa cầm lượng vàng ra khỏi cửa hàng, bạn đã lỗ khoảng hai phần trăm. Vàng phải tăng chừng đó, bạn mới về hoà." (L77–78) | OK | — | 3/143,5 = 2,1%. |
| CH02 | "Nhìn xa hơn một chút, vàng vẫn cao hơn cùng kỳ năm ngoái, và năm 2025 vàng thế giới tăng tới 65%." (L80) | OK | — | Chỉ số giá vàng tháng 9 +12,42% so cùng kỳ [1]; 2025 +65% [114]. |
| CH02 | "Vàng không tệ." (L81, câu đầu) | BỎ | Cắt câu này, giữ: "Chỉ là năm nay, ai mua sau cơn sốt thì phải trả giá cho cơn sốt." | Phán xét "tốt/tệ" cho một loại tài sản dễ nghe thành khuyến nghị (luật 2). Phần còn lại của dòng là OK. |
| CH03 | "Đỉnh lịch sử của nó là khoảng 126 nghìn đô la, đúng một năm trước." (L86) | SỬA | "Đỉnh lịch sử của nó là khoảng một trăm hai mươi sáu nghìn đô la, vào tháng mười năm hai nghìn không trăm hai mươi lăm." | 126.198 USD ngày 06/10/2025 [58] — đúng hôm nay, nhưng "đúng một năm trước" sẽ sai khi video được xem về sau. |
| CH03 | "Đến cuối tháng sáu năm nay, nó chỉ còn khoảng 58 nghìn đô, mất hơn một nửa." (L87) | OK | — | 58.379 (30/06) / 57.718 (01/07) [61][63]; −53–54% từ đỉnh. CSV VND: −53,2% ✓. |
| CH03 | "Rồi quý ba lại bật lên hơn bốn mươi phần trăm." (L88) | OK | — | Q3 +42% theo USD [60]. (CSV VND: +37% — nếu biểu đồ dùng VND thì đổi lời thành "gần bốn mươi phần trăm".) |
| CH03 | "Tính từ đầu năm, Bitcoin âm khoảng bốn đến năm phần trăm. Tính mười hai tháng, âm gần hai mươi bảy phần trăm." (L89) | OK | — | −4,3% (tự tính) / −5,17% [60]; 12 tháng −26,9% [58]. Đúng khuyến nghị hồ sơ (không gán −4,5% cho Yahoo) ✓. |
| CH03 | "…tài sản mã hoá đã được luật công nhận là tài sản, nhưng không phải là tiền." (L90) | OK | — | Luật 71/2025/QH15, hiệu lực 01/01/2026 [65]; không phải tiền/phương tiện thanh toán [66][70]. |
| CH03 | "Đến đầu tháng mười, chưa có sàn giao dịch nào trong nước được cấp phép, và tiền trên các sàn nước ngoài không có bảo hiểm tiền gửi nào bảo vệ." (L91) | SỬA | "Đến đầu tháng mười, chưa có tổ chức nào trong nước được cấp phép, và tiền trên các sàn nước ngoài không được bảo hiểm tiền gửi Việt Nam chi trả; Bộ Tài chính cũng nói phần lớn hoạt động này không được pháp luật bảo vệ." | Vế 1 đúng [68]. Vế 2 "không có … nào" nói quá: một số sàn nước ngoài có quỹ bảo vệ riêng; điều có nguồn là bảo hiểm tiền gửi VN không áp dụng và "không được pháp luật bảo vệ" [71]. |
| CH03 | "Còn nhà đất đỏ theo một kiểu khác: không phải rơi giá ầm ầm, mà là đóng băng." (L92) | SỬA | "Còn nhà đất đỏ theo một kiểu khác: giá không rơi ầm ầm, nhưng giao dịch chậm hẳn lại — dù giá sơ cấp căn hộ ở vài nơi vẫn tăng." | "Đóng băng" nói quá: quý II vẫn có ~100.005 giao dịch (63,7% cùng kỳ) [73]; Knight Frank quý III: giao dịch căn hộ TP.HCM +40% so quý trước [82]. Thêm vế ngược chiều đúng luật 4 (hồ sơ mục 4.2). |
| CH03 | "Theo Bộ Xây dựng, quý hai năm nay cả nước có khoảng 100 nghìn giao dịch bất động sản, chỉ bằng 64% cùng kỳ năm ngoái." (L93) | OK | — | 100.005; 63,7% [73]. |
| CH03 | "Riêng đất nền, giao dịch giảm khoảng bốn mươi phần trăm." (L94) | OK | — | 73.438 = 59,9% cùng kỳ [73]; nói đúng là **giao dịch**, không phải giá ✓. |
| CH03 | "Giá rao đất nền cả nước giảm hai đến ba phần trăm, ở Hà Nội có nơi giảm tới mười bốn phần trăm so với đầu năm." (L95) | SỬA | "Giá đất nền cả nước quý hai giảm hai đến ba phần trăm so với quý một; riêng Hà Nội, giá rao đất nền bình quân quý ba thấp hơn quý một khoảng mười bốn phần trăm." | (1) −14% là **mức bình quân giá rao đất nền Hà Nội** (70 triệu/m²) [76], không phải "có nơi giảm tới". (2) Hai số khác kỳ so sánh: cả nước = quý II so quý I [74]; Hà Nội = quý III so quý I [76] — không phải "so với đầu năm". (3) Số cả nước [74] là số Bộ XD + khảo sát, không chắc chỉ là "giá rao" → bỏ chữ "rao" ở vế đầu. |
| CH03 | "Với nhà đất, con số đáng sợ không nằm ở giá, mà nằm ở chỗ: bạn có bán được không, và bán mất bao lâu." (L97) | OK | — | Nhận định, khớp số hấp thụ [75]. |
| CH03 | "…người vay mua nhà đang trả lãi khoảng 13 đến 15% một năm sau thời gian ưu đãi." (L98) | OK | — | VARS-IRE [78]. |
| CH03 | "Lãi suất cao làm người gửi tiền vui, nhưng người đi vay thì ở phía ngược lại." (L99) | OK | — | Mặt trái (luật 4) ✓. |
| CH04 | "Vì lãi suất tiền gửi tăng gần như suốt cả năm." (L104) | SỬA | "Vì lãi suất tiền gửi tăng mạnh trong nửa đầu năm." | Big-4: 5,2% → 5,9% (26/03) → 6,8% (01/06) rồi **đứng yên** tới tháng 9 [89][90][91][83]; 17/06 NHNN yêu cầu chấn chỉnh việc tăng lãi suất [96]. |
| CH04 | "Ở bốn ngân hàng lớn nhất, lãi suất mười hai tháng tăng từ 5,2% hồi đầu năm, lên 6,8% từ tháng sáu." (L105) | OK | — | [89][91][83]. Không nêu tên ✓. |
| CH04 | "Nhiều ngân hàng khác trả khoảng bảy đến tám phần trăm." (L106) | OK | — | [83]; đúng câu khuyến nghị của hồ sơ. |
| CH04 | "Lý do chính: các ngân hàng cho vay ra nhanh hơn nhiều so với số tiền họ huy động được." (L107) | SỬA | "Lý do chính: các ngân hàng cho vay ra nhanh hơn số tiền họ huy động được." | Tới 28/09: tín dụng +10,89% vs huy động +9,78% so cuối 2025 [97] — chênh ~1 điểm, không phải "nhiều". |
| CH04 | "Có lúc, tín dụng tăng nhanh gấp đôi tiền gửi." (L108) | SỬA | "Có thời điểm, hồi cuối tháng tư, tín dụng tăng nhanh gần gấp đôi tiền gửi, nếu so với cùng kỳ năm trước." | Nguồn ghi "gấp ~2 lần", tính theo cùng kỳ, ngày 28/04 [96] → thêm "gần" và nói rõ mốc. |
| CH04 | "Muốn có thêm tiền để cho vay, ngân hàng phải trả lãi cao hơn… Cộng thêm áp lực tỷ giá và lạm phát, mặt bằng lãi suất cứ thế đi lên." (L109–110) | OK | — | [93][95][96][97]. |
| CH04 | "Người gửi hai mươi triệu từ ngày đầu năm ở ngân hàng lớn được hưởng 5,2% một năm." (L112) | OK | — | [89]. |
| CH04 | "Chín tháng, tiền lãi tích luỹ khoảng 3,9%, tức khoảng 780 nghìn đồng." (L113) | OK | — | 5,2% × 9/12 = 3,9%; 20 tr × 3,9% = 780 nghìn. Chỉ nhận khi đáo hạn — L121 đã nói ✓. |
| CH04 | "…giá cả hàng hoá dịch vụ đã tăng 4,2% so với cuối năm ngoái." (L114) | OK | — | CPI 9/2026 so 12/2025 +4,20% [1]. |
| CH04 | "Xăng tăng. Đồ ăn tăng. Tiền thuê nhà tăng." (L115) | OK | — | NSO 9T: nhiên liệu +10,89%, ăn uống +4,72%, thuê nhà +4,91% [1]. |
| CH04 | "…sổ tiết kiệm xanh trên giấy, nhưng sức mua thì gần như đứng yên." (L116) | OK | — | 1,039/1,042 − 1 = −0,3% (tự tính). Có thể thêm "thậm chí hơi lùi" cho chính xác hơn. |
| CH04 | "Năm nay, không kênh nào thật sự làm bạn giàu lên. Kênh thắng chỉ là kênh không làm bạn nghèo đi." (L117) | SỬA | "Tính tới cuối tháng chín, trong năm kênh mình xét, không kênh nào thật sự làm bạn giàu lên sau lạm phát. Kênh 'thắng' chỉ là kênh làm bạn nghèo đi ít nhất." | (1) "Không kênh nào" khái quát quá phạm vi 5 kênh, và năm chưa hết. (2) Theo chính L116, sổ tiết kiệm Big-4 đầu năm vẫn hơi âm thực (−0,3%) → "không làm bạn nghèo đi" sai nhẹ. |
| CH04 | "Một, lạm phát, như bạn vừa thấy." (L120) | OK | — | — |
| CH04 | "Hai, rút trước hạn thì thường chỉ được hưởng lãi không kỳ hạn, chưa tới một phần trăm một năm." (L121) | OK | — | TT 04/2022/TT-NHNN [134]; DIV "khoảng dưới 1%/năm" [135]. |
| CH04 | "Ba, bảo hiểm tiền gửi có hạn mức: từ tháng bảy năm nay là 350 triệu đồng cho mỗi người tại mỗi ngân hàng, gồm cả gốc và lãi." (L122) | OK | — | Từ 13/07/2026, TT 05/2026/TT-NHNN [125]. (Chính xác hơn: "mỗi tổ chức nhận tiền gửi" — không bắt buộc sửa.) |
| CH04 | "…'gói tiết kiệm nội bộ, lãi 15–20%' qua link hay mã QR, công an đã cảnh báo: đó là lừa đảo." (L123) | OK | — | Công an Hà Nội 22/06/2026 [143]. |
| CH04 | "Lãi suất thật luôn được ngân hàng niêm yết công khai." (L124) | SỬA | "Theo công an, lãi suất thật được ngân hàng niêm yết công khai." | Gán nguồn [143]; "luôn" nói quá — hồ sơ ghi có mức "thực nhận" 9%+ qua mã giới thiệu/khuyến mãi không nằm trên biểu niêm yết [86]. |
| CH05 | "Nếu chỉ nhìn năm nay, bạn dễ rút ra kết luận… Nhưng hãy lùi lại một năm thôi." (L128–129) | OK | — | — |
| CH05 | "Năm 2025, VN-Index tăng gần 41%. Vàng thế giới tăng 65%." (L130) | OK | — | CSV: 1.266,78 → 1.784,49 = +40,87% ✓; vàng +65% [114]. |
| CH05 | "Còn sổ tiết kiệm năm đó chỉ được khoảng năm phần trăm." (L131) | SỬA | "Còn sổ tiết kiệm ở ngân hàng lớn năm đó chưa được tới năm phần trăm." | Big-4 12 tháng suốt 2025: 4,6–4,8% (06/2025 [107]; 4,7% trước 17/12/2025 [88]) → làm tròn lên 5 làm tiết kiệm trông tốt hơn thực tế. |
| CH05 | "Giờ lùi xa hơn: tám năm, từ tháng mười năm 2018 đến nay." (L132) | OK | — | — |
| CH05 | "Một trăm đồng gửi tiết kiệm… giờ thành khoảng 156 đồng." (L133) | OK | — | Tính lại: ×1,5607 (~5,7%/năm). Đã kiểm các mốc "suy": VCB 10/2019 = 6,8% ✓; **10/2020 = 6,0%** (hồ sơ dùng 5,8); **10/2024 = 4,6%** (hồ sơ dùng 4,7) — vietnambiz. Thay số đúng: ×1,562 → vẫn "khoảng 156" ✓. |
| CH05 | "Một trăm đồng theo VN-Index thành khoảng 177 đồng, và đó là chưa tính cổ tức." (L134) | OK | — | CSV: 996,12 (08/10/2018) → 1.759,08 (06/10/2026) = +76,6%, ~7,4%/năm ✓. |
| CH05 | "Một trăm đồng mua vàng miếng thành khoảng 383 đồng." (L135) | OK | — | Bán 36,57 (CSV 01/10/2018) → mua 139,9 (06/10, [46]) = ×3,826 ✓. Lưu ý: `sjc_1d.csv` mới tới 29/05/2026 nên mốc 06/10 lấy từ báo, không từ CSV. |
| CH05 | "…VN-Index từng rơi xuống dưới bảy trăm điểm lúc đại dịch, từng mất khoảng 40% từ đỉnh xuống đáy trong năm 2022." (L138) | OK | — | 659,21 (24/03/2020); 1.528,57 (06/01/2022) → 911,90 (15/11/2022) = −40,3% (CSV) ✓. |
| CH05 | "Vàng thì năm nay vừa mất hơn một phần tư giá trị từ đỉnh chỉ trong tám tháng." (L139) | OK | — | SJC: bán 191,3 → bán 142,9 = −25,3%; mua 188,3 → mua 139,9 = −25,7%; vàng thế giới 5.594,82 → ~4.137 = −26,1% [36][43]. 29/01 → 06/10 ≈ 8 tháng ✓. |
| CH05 | "Còn sổ tiết kiệm thì đi một đường gần như thẳng." (L140) | OK | — | Danh nghĩa. |
| CH05 | "Giai đoạn 2011 đến 2015, vàng thế giới mất gần một nửa giá trị, và phải chín năm sau mới lấy lại được đỉnh cũ." (L142) | SỬA | "Từ đỉnh tháng chín năm hai nghìn không trăm mười một tới cuối năm hai nghìn không trăm mười lăm, vàng thế giới mất khoảng bốn mươi lăm phần trăm, và phải gần chín năm kể từ đỉnh mới vượt lại mức cũ." | 1.921 → 1.045,85 = −45,6% [128][129] ("gần một nửa" hơi quá). "Chín năm sau" đặt sau "2011–2015" dễ hiểu là 2024; thực tế vượt đỉnh 2011 ngày 27/07/2020 (≈ 8 năm 11 tháng kể từ 06/09/2011) — Gulf News [128] + tin 27/07/2020. |
| CH05 | "Quá khứ không bảo đảm tương lai. Với bất kỳ kênh nào." (L143) | OK | — | SEC [123]. |
| CH05 | "…kênh có thể tăng nhiều thì cũng có thể rơi sâu. Và thời gian bạn giữ tiền quan trọng không kém chỗ bạn để tiền." (L144) | OK | — | Khung SEC về kỳ hạn [119]; giáo dục, không khuyến nghị. |
| CH06 | "Mình không ở đây để bảo bạn nên mua gì, bán gì." (L148) | OK | — | Luật 2 ✓. |
| CH06 | "Cơ quan bảo vệ nhà đầu tư Mỹ gợi ý khoảng ba đến sáu tháng chi tiêu, con số cụ thể tuỳ hoàn cảnh của bạn." (L150) | SỬA | "Các trang giáo dục nhà đầu tư ở Mỹ thường gợi ý khoảng ba đến sáu tháng chi tiêu; con số cụ thể tuỳ hoàn cảnh của bạn." | (1) Investor.gov [116] vẫn 403 — không mở được; số "3–6 tháng" chỉ thấy qua đoạn trích FINRA/Investor.gov (SECONDARY). Trang SEC mở được (sec.gov "Ten Things to Consider") chỉ ghi nhiều người giữ "tới sáu tháng thu nhập". (2) "Cơ quan bảo vệ nhà đầu tư" dễ hiểu nhầm là SIPC/cơ quan bảo hiểm; SEC là Uỷ ban Chứng khoán. Nếu muốn giữ chủ thể: "Uỷ ban Chứng khoán Mỹ khuyên nên có quỹ khẩn cấp, nhiều người giữ tới sáu tháng thu nhập" (đã kiểm). |
| CH06 | Câu hỏi Hai–Năm (L151–154) | OK | — | Khớp bảng tự kiểm, hồ sơ mục 8; dạng câu hỏi, không khuyến nghị. |
| CH06 | "Nếu bạn đang vay nợ với lãi suất cao, lãi suất tăng là tin xấu, không phải tin vui." (L156) | OK | — | Mặt trái (luật 4). |
| CH06 | "Nếu bạn mua vàng từ vài năm trước, năm nay đỏ nhưng chặng dài của bạn vẫn đang xanh." (L157) | OK | — | SJC bình quân 2024 ~84 triệu [87] < 139,9 hiện nay. (Ai mua cuối 2025 thì không đúng — "vài năm" đã loại trường hợp này.) |
| CH06 | "…nếu bạn đọc video này vào năm sau, có thể bức tranh đã đảo ngược hoàn toàn, như năm 2025 đã từng." (L158) | OK | — | Nêu khả năng, không dự báo. Nên đổi "đọc" → "xem". |
| CH06 | "Năm 2026 là một năm mà ai cũng thấy mình nghèo đi một chút, dù đang giữ tiền ở đâu." (L159) | SỬA | "Chín tháng đầu năm hai nghìn không trăm hai mươi sáu là quãng thời gian nhiều người thấy tiền để dành của mình chững lại, dù đang giữ ở đâu." | (1) "Ai cũng … nghèo đi" trái số NSO: thu nhập bình quân 9 tháng +9,1%, thực ≈ +4,4% [3]. (2) Năm chưa hết — nói về cả năm 2026 là ngầm dự báo (luật 2). |
| CH06 | "Nếu bạn thấy vậy, bạn không đơn độc… mỗi tuần mình sẽ lấy một câu hỏi tiền bạc thật…" (L160–161) | OK | — | — |
| CH06 | "Tuần sau là bài đầu tiên của khoá…: vì sao cả năm VN-Index gần như đứng yên, mà nhiều tài khoản vẫn lỗ." (L162) | SỬA | "…vì sao từ đầu năm VN-Index gần như đứng yên, mà nhiều tài khoản vẫn lỗ." | Năm chưa hết; "cả năm" sẽ sai nếu quý IV biến động. |
| CH06 | "Còn bây giờ, mình muốn nghe bạn…" (L163) | OK | — | — |

## 2. Kiểm luật kênh (positioning mục 1)

| Luật | Kết quả |
|---|---|
| Không bán gì | OK — không có link, nhóm, khoá trả phí. |
| Không dự báo / không khuyến nghị | 4 chỗ cần sửa: L33 ("có"), L81 ("Vàng không tệ" → BỎ), L159 (nói về cả năm 2026), L162 ("cả năm"). |
| Không nêu tên ngân hàng/sàn | OK — không tên ngân hàng, sàn crypto hay công ty chứng khoán nào. "HOSE" (phạm vi số liệu) và "SJC" (thương hiệu vàng miếng quốc gia) là thuật ngữ thị trường, chấp nhận được. |
| Mọi số có nguồn | Hầu hết có nguồn; L20 ("hay chọn nhất") không có nguồn; L150 số 3–6 tháng chỉ có nguồn SECONDARY. |
| Nói cả mặt trái | Có (CH04 lãi thực, rủi ro tiết kiệm; CH06). Thiếu vế ngược chiều của nhà đất (giá sơ cấp tăng) → thêm ở L92. |
| Dữ liệu quá khứ, không bình luận hiện tại | L73 "bây giờ", L86 "đúng một năm trước" → đổi sang mốc ngày cụ thể. |

## 3. TTS — chỗ dễ đọc sai

| Chỗ | Rủi ro | Gợi ý |
|---|---|---|
| "VN-Index" (L42, 48, 59, 60, 130, 134, 138, 162) | Giọng TTS tiếng Việt có thể đánh vần "V-N" hoặc đọc "index" kiểu tiếng Anh | Nghe thử; nếu sai, viết theo cách đọc trong văn bản gửi TTS, ví dụ "Vi-en In-đéc" (chỉ trong bản gửi TTS, giữ "VN-Index" trên màn hình). |
| "HOSE" (L55) | Đọc thành "hâu-z" (tiếng Anh "hose") | "Hô-se", hoặc thay bằng "sàn thành phố Hồ Chí Minh". |
| "SJC" (L67) | Đọc từng chữ theo tiếng Anh | Nghe thử; nếu cần thì "ét-giê-xê". |
| "mã QR" (L123) | "Q-R" có thể bị đọc lạ | "mã kiu-a" hoặc "mã QR" sau khi nghe thử. |
| "Kevin Warsh" (L68) | Phát âm tên riêng | Nghe thử; nếu sai thì phiên âm "Ke-vin Uo-sơ". |
| Ký hiệu "‖" và "HỎI:" | Có thể bị đọc ra thành tiếng | Lọc khỏi văn bản trước khi gửi TTS (chỉ dùng làm tín hiệu ngắt/đổi giọng). |
| Dấu ngoặc kép trong L52, L123, L144 | Một số engine ngắt giọng lạ | Không bắt buộc sửa; nghe thử. |
| Số | Mọi số trong lời thoại đã viết bằng chữ ✓ (không còn chữ số nào trong CH00–CH06 ngoài tiêu đề chương). | — |

## 4. Tính lại các số trong "Ghi chú" (từ CSV)

| Mục Ghi chú | Kết quả tính lại | Kết luận |
|---|---|---|
| VN-Index 08/10/2018 → 06/10/2026: 996,12 → 1.759,08 = +76,6% (≈7,4%/năm) | CSV: 996,12 → 1.759,08 = **+76,59%**, CAGR **7,37%/năm** | OK |
| VN-Index đáy đóng cửa 2020: 659,21 (24/03/2020) | CSV: 659,21 ngày 24/03/2020 (cũng là mức thấp nhất của cả chuỗi 2018–2026) | OK |
| 2022: đỉnh 1.528,57 → đáy 911,9 (≈ −40%) | CSV: 1.528,57 (06/01/2022) → 911,90 (15/11/2022) = **−40,3%** (cả năm 2022: −32,78%) | OK |
| 2026: đáy 1.586,44 / đỉnh 1.933,11 (dùng ở L48–49) | Đây là số **trong phiên**; theo giá đóng cửa: đáy 1.591,17 (23/03), đỉnh 1.927,94 (18/05). Đáy → đỉnh: +21,2% (đóng cửa) / +21,9% (trong phiên) | OK — ghi nhãn "trong phiên" trên biểu đồ |
| Vàng SJC: bán 01/10/2018 36,57 → mua 06/10/2026 139,9 = ×3,83 | CSV 01/10/2018: mua 36,42 / bán 36,57 ✓. **CSV mới tới 29/05/2026** (284 dòng; 2018–2025 chỉ ~2 dòng/tháng) → không có mốc 06/10; dùng 139,9 [46]: ×**3,826** (+283%) | OK (đầu vào cuối lấy từ báo, không phải CSV) |
| Đối chiếu SJC: 01/01 = 150,8/152,8 | CSV 01/01/2026: 150,8 / 152,8 ✓ | OK |
| Đối chiếu SJC: 29/01 = 188,3/191,3 | CSV 29/01/2026: **186,6 / 189,6** (giá trị lớn nhất của cả CSV) ✗ — CSV không bắt được đỉnh 13:25 | SỬA biểu đồ — thêm điểm 191,3 bằng tay hoặc ghi chú "đỉnh trong ngày 191,3" |
| (lỗi dữ liệu) SJC 06/01/2026 | CSV ghi 150,8/152,8, kẹp giữa 155,1 (05/01) và 155,1 (07/01) → giống giá cũ bị lặp lại | Kiểm lại trước khi vẽ |
| Tiết kiệm Big-4 cuộn 12 tháng ×1,56 | Các mốc suy, kiểm lại qua vietnambiz: VCB 10/2019 6,8% ✓; 10/2020 **6,0%** (không phải 5,8); 10/2024 **4,6%** (không phải 4,7). Thay vào: **×1,562** (5,73%/năm) | OK — kết quả không đổi; cập nhật chuỗi trong hồ sơ 7.1 |
| Cold open: CK −0,9% | −0,89% | OK |
| Cold open: vàng −7,7% (152,8 → 141,1) | −7,66% | OK |
| Cold open: BTC −4,3% (USD) | USD −4,26% ✓; nhưng CSV `btc_vnd_1d` (VND): **−6,53%** tới 30/09, −3,80% tới 06/10; Q3 +37,2% (USD +42%) | OK theo USD — lời thoại phải nói "theo giá đô la" (xem L29); đừng dùng chuỗi VND cho biểu đồ khi chưa rõ nguồn giá |
| Cold open: tiết kiệm 5,2% × 9/12 = +3,9% | 3,90%; thực −0,3% so CPI +4,20% | OK |
| "rơi mạnh nhất trong nhiều thập kỷ" | Không có trong lời thoại (L69 đã dùng "rơi mạnh") | OK — không cần kiểm thêm |

## 5. Nguồn kiểm thêm trong lần fact-check này

- SEC — Ten Things to Consider Before You Make Investing Decisions: https://www.sec.gov/investor/pubs/tenthingstoconsider.htm ("up to six months of their income in savings")
- Investor.gov — Save for a rainy day [116]: vẫn trả 403 → số 3–6 tháng còn SECONDARY
- Gulf News — vàng vượt 1.900 USD sau 9 năm [128]: https://gulfnews.com/business/markets/gold-crosses-1900-an-ounce-after-nine-years-1.1595596558203 (đỉnh 2011: 1.921 USD ngày 06/09/2011)
- Tin vàng vượt đỉnh 2011 ngày 27/07/2020 (CRU/PR Newswire): https://www.prnewswire.com/news-releases/cru-gold-entering-unchartered-waters-as-price-surpasses-2011-record-301104037.html
- Vietnambiz — Vietcombank 10/2020 (12 tháng 6,0%): https://vietnambiz.vn/lai-suat-ngan-hang-vietcombank-moi-nhat-thang-10-2020-20201001120453139.htm
- Vietnambiz — Vietcombank 10/2024 (12 tháng 4,6%): https://vietnambiz.vn/thang-102024-lai-suat-ngan-hang-vietcombank-cao-nhat-la-bao-nhieu-2024101135646946.htm
- Vietnambiz — Vietcombank 10/2019 (≥12 tháng 6,8%): https://vietnambiz.vn/lai-suat-ngan-hang-vietcombank-moi-nhat-thang-10-2019-2019100112041312.htm
