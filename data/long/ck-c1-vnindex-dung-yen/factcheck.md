# Fact-check — script.md (bản 1) · ck-c1-vnindex-dung-yen (Chứng khoán từ số 0 — Bài 1)

Ngày kiểm: 06–07/10/2026. Đối chiếu: hồ sơ `docs/channels/chung-khoan/2026-10-07-long-c1-research.md` (số `[n]` = nguồn trong
hồ sơ đó) và `2026-10-06-long-01-research.md` (`[L01-n]`); luật kênh `2026-10-06-positioning.md` mục 1 và
`2026-10-06-research.md` mục 1.3; dữ liệu kênh `data/ck/breadth_2026/*.csv`, `summary.json`, `data/ck/vnindex_1d.csv` (tính lại
bằng pandas, độc lập với `motion/long/breadth.py`). Không sửa script.

**Kết luận: OK 82 · SỬA 19 · BỎ 0** (101 hàng: tiêu đề, các dòng thoại — vài dòng gộp — và 5 dòng chữ trên màn hình). Mục luật
kênh, TTS, tính lại Ghi chú và nguồn ở cuối, không tính vào tổng.

Nhãn: OK = đúng nguồn / chấp nhận được · SỬA = sai số, nói quá nguồn, mơ hồ, hoặc chạm luật kênh · BỎ = nên cắt câu.

**Ba điểm quan trọng nhất**
1. **L269 "Nếu tính từ đáy tháng ba, bức tranh dễ chịu hơn nhiều" sai với cổ phiếu điển hình.** Từ đáy 23/03 tới 30/09,
   VN-Index +11,15%, nhưng **266/400 mã (66,5%) vẫn thấp hơn giá ngày 23/03, trung vị −6,5%**, rổ đều −5,1% (tự tính từ
   `prices.csv`). Câu này chỉ đúng với chỉ số. Hồ sơ mục 4 ý 4 ("tính từ 23/03 thì phần lớn cổ phiếu đã hồi") cũng sai, cần sửa
   hồ sơ.
2. **L148 SEC bị bỏ mất vế giới hạn.** Nguyên văn: "Stocks have historically had the greatest risk and highest returns
   **among the three major asset categories**". Câu thoại nói như thể cổ phiếu rủi ro cao nhất trong mọi loại tài sản.
3. **L201 Tuổi Trẻ**: nguyên văn là "**hơn** 46% số cổ phiếu **trên thị trường** ghi nhận kết quả đầu tư âm". Bài không có
   chữ "niêm yết" (phạm vi "trên thị trường" có thể gồm cả UPCoM). Chữ trên màn hình CH03 cũng phải sửa theo.

Các số tự tính mới trong "Ghi chú" đều **khớp** khi tính lại: VRE −25,08% · phân bố 13/73/46/80/79/56/21/13/12/7 · 55,78 triệu
−7,03% · +9,1% · 4,8 triệu ≈ 9,6% · 21,45–21,46% / 52,2% / 1,28%. Lời trích Luật CK 2019 Điều 4 khoản 2 **đúng nguyên văn**
(xem mục 4).

## 1. Bảng kiểm từng dòng

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Tiêu đề | "TỪ ĐẦU NĂM VN-INDEX GẦN NHƯ ĐỨNG YÊN — SAO TÀI KHOẢN CỦA BẠN VẪN LỖ?" (L1) | SỬA | "TỪ ĐẦU NĂM VN-INDEX GẦN NHƯ ĐỨNG YÊN — SAO TÀI KHOẢN VẪN CÓ THỂ LỖ?" | "Từ đầu năm" đã đúng (bài học từ factcheck trước). Nhưng "tài khoản của bạn vẫn lỗ" là khẳng định về người xem, trong khi chính kịch bản (L255) nói không có số liệu về tỷ lệ nhà đầu tư lãi/lỗ, nên có nguy cơ thành tiêu đề gây hiểu nhầm (research 1.4, chính sách spam/lừa dối). |
| CH00 | "Giả sử tối thứ Tư, ba mươi tháng chín năm hai nghìn không trăm hai mươi sáu…" (L117) | OK | — | 30/09/2026 là thứ Tư (01/01/2026 là thứ Năm; +272 ngày). |
| CH00 | "Bạn kéo biểu đồ VN-Index về đầu năm: âm không phẩy chín phần trăm." (L118) | OK | — | 1.784,49 → 1.768,62 = −0,89% (`vnindex_1d.csv`). |
| CH00 | "Gần như đứng yên. Bạn thở phào. Rồi bạn bấm sang tài khoản của mình." (L119–120) | OK | — | — |
| CH00 | "Ba mã cổ phiếu… âm mười hai… âm hai mươi… dương ba. Cả tài khoản: âm gần mười phần trăm." (L121–123) | OK | — | Giả định; (−12 − 20 + 3)/3 = −9,67%. Màn hình ghi "VÍ DỤ GIẢ ĐỊNH" ✓. |
| CH00 | "HỎI: … App sai, hay mình sai?" / "Không ai sai cả. Chỉ là VN-Index đo một chuyện khác…" (L124–126) | OK | — | — |
| CH00 | "…theo số liệu kênh tự tính, ngày ba mươi tháng chín, cứ bốn cổ phiếu trên sàn HOSE thì gần ba cổ phiếu thấp hơn giá cuối năm ngoái." (L127) | OK | — | 291/400 = 72,8% → 2,91/4 (`summary.json` → `ytd_q3`, tính lại khớp). Mẫu 400/405 mã, giá điều chỉnh (L197–198 đã nói). |
| CH00 | Ba câu hỏi lộ trình (L128–131) | OK | — | — |
| CH00 | "Đây là Biểu Đồ Biết Nói… Video chỉ nhằm giáo dục, không phải lời khuyên mua hay bán bất kỳ cổ phiếu nào." (L132–134) | OK | — | Luật 2 ✓. Thẻ miễn trừ 4–5 giây (research 1.5) vẫn cần có trên hình. |
| CH01 | Ví dụ quán phở: cổ tức, chênh lệch giá (L138–141) | OK | — | Ví dụ giả định; khớp hồ sơ mục 5.1. |
| CH01 | "…doanh nghiệp được chia thành hàng triệu, có khi hàng tỷ phần." (L142) | OK | — | Số cổ phiếu niêm yết trong dữ liệu: nhỏ nhất ~6,1 triệu, lớn nhất ~9,26 tỷ (`breadth_2026.csv`, `listed_share`). |
| CH01 | "Luật Chứng khoán Việt Nam viết: » Cổ phiếu là loại chứng khoán xác nhận quyền và lợi ích hợp pháp của người sở hữu đối với một phần vốn cổ phần của tổ chức phát hành." (L143–144) | OK | (tuỳ chọn) "Luật Chứng khoán năm hai nghìn không trăm mười chín viết:" | **Đúng nguyên văn** Điều 4 khoản 2, Luật 54/2019/QH14 (thông qua 26/11/2019), đối chiếu hai bản: luatvietnam.vn và hethongphapluat.com (thuvienphapluat trả 403; vbpl.vn không tải nội dung). Trên màn hình ghi "Luật Chứng khoán 2019 (54/2019/QH14), Điều 4 khoản 2". |
| CH01 | "Nói gọn: mua cổ phiếu là mua một phần nhỏ của một doanh nghiệp, không phải mua một cái mã." (L145) | OK | — | Diễn giải đúng định nghĩa. |
| CH01 | "HỎI: Vậy mua cổ phiếu là mình làm chủ công ty luôn à?" / "Bạn thành đồng sở hữu… cả cổ tức lẫn chênh lệch giá đều không được bảo đảm." (L146–147) | OK | — | SEC: "you could lose some or all of your money" [L01-119]. |
| CH01 | "Uỷ ban Chứng khoán Mỹ nhắc người mới: trong lịch sử, cổ phiếu là nhóm tài sản rủi ro cao nhất, đổi lại có lợi nhuận cao nhất." (L148) | SỬA | "Uỷ ban Chứng khoán Mỹ nhắc người mới: trong ba nhóm tài sản chính là cổ phiếu, trái phiếu và tiền mặt, cổ phiếu trong lịch sử có rủi ro cao nhất, và cũng có lợi nhuận cao nhất." | Nguyên văn (sec.gov, Beginners' Guide to Asset Allocation [L01-119]): "Stocks have historically had the greatest risk and highest returns **among the three major asset categories**." Câu thoại bỏ vế "trong ba nhóm", thành khẳng định tuyệt đối (sai: tiền mã hoá, phái sinh… rủi ro hơn). "Đổi lại" nghe như một sự đánh đổi chắc chắn; SEC chỉ nói "historically". |
| CH01 | "Người mua và người bán gặp nhau ở sở giao dịch. Lớn nhất Việt Nam là Sở Giao dịch Chứng khoán Thành phố Hồ Chí Minh, gọi tắt là HOSE." (L149–150) | OK | — | HOSE ≈ 95% vốn hoá cổ phiếu niêm yết toàn thị trường [7] (CafeF 05/10/2026, đã mở). |
| CH01 | Ẩn dụ khu chợ; "nhờ một công ty chứng khoán đi chợ hộ, và trả phí." (L151–152) | OK | — | Không nêu tên công ty chứng khoán ✓. |
| CH01 | "Phiên chợ đầu tiên, ngày hai mươi tám tháng bảy năm hai nghìn, chỉ có hai cổ phiếu: REE và SAM." (L153) | OK | — | VnExpress [5] (đã mở): phiên đầu 28/07/2000, 1.000 REE + 3.200 SAM, ~71 triệu đồng. |
| CH01 | "Cuối tháng chín năm nay, HOSE có bốn trăm lẻ năm cổ phiếu, tổng vốn hoá khoảng hai phần ba GDP năm hai nghìn không trăm hai mươi lăm." (L154) | OK | — | CafeF [7] (đã mở): 405 cổ phiếu, 8,55 triệu tỷ = 66,52% GDP 2025. "Cuối tháng chín năm nay" sẽ cũ khi video được xem năm sau; nếu muốn bền thì "cuối tháng chín năm hai nghìn không trăm hai mươi sáu" (không bắt buộc). |
| CH01 | "Chợ mở cửa thế nào, lệnh được khớp ra sao, mình để dành cho bài hai." (L155) | OK | — | — |
| CH02 | "VN-Index đo biến động của toàn bộ cổ phiếu niêm yết trên HOSE, bắt đầu từ một trăm điểm ngày hai mươi tám tháng bảy năm hai nghìn." (L159–160) | OK | — | [3][4] bằng chứng. |
| CH02 | "Cách tính dựa trên vốn hoá, tức giá một cổ phiếu nhân với số cổ phiếu của doanh nghiệp." (L161) | OK | — | [4]. Giữ ở mức này là đúng, vì việc có free-float hay không **chưa có văn bản gốc riêng của VN-Index** (hồ sơ 1.3, 8). Không nói thêm "không free-float". |
| CH02 | "Mỗi ngày, tổng vốn hoá được đem so với một mức gốc." (L162) | OK | — | Công thức gốc [4]. Bản đơn giản hoá (không nói chuyện chỉnh hệ số chia); trên màn hình đã có "Mô tả phổ thông". |
| CH02 | "HỎI: … giá trung bình…?" / "Không… VN-Index không cho mỗi cổ phiếu một phiếu bầu như nhau. Doanh nghiệp càng lớn, giá của nó càng kéo chỉ số mạnh." (L163–166) | OK | — | Trọng số theo vốn hoá [3][4]. |
| CH02 | Giỏ hàng: gà 50 nghìn + 10 bó rau × 5 nghìn = 100 → gà +20% = 60, rau −10% = 4,5 → 105, +5%; "Mười trên mười một món giảm giá" (L167–170) | OK | — | 60 + 45 = 105 ✓. |
| CH02 | "Theo kênh tự tính ngày ba mươi tháng chín, riêng mã VIC chiếm khoảng một phần năm tổng vốn hoá cổ phiếu trên HOSE." (L171–172) | OK | — | Tính lại: 21,05% (406 mã) / 21,45% (400 mã). Theo tổng vốn hoá HOSE công bố 8,55 triệu tỷ [7]: VIC ≈ 1.769 nghìn tỷ ≈ 20,7%. Cả ba cách đều ≈ 1/5. |
| CH02 | "Mười mã lớn nhất chiếm khoảng một nửa." (L173) | OK | — | 51,24% (406) / 52,23% (400). Mười mã: VIC, VHM, VCB, BID, CTG, TCB, GAS, VPB, MBB, MCH. |
| CH02 | "Còn hai trăm mã nhỏ nhất, gần một nửa số cổ phiếu trên sàn, cộng lại chỉ khoảng một phẩy hai lăm phần trăm." (L174) | OK | — | 1,246% (406) / 1,275% (400); 200/405 = 49,4%. |
| CH02 | "Mã lớn nhất nặng gấp hơn mười lăm lần cả hai trăm mã đó cộng lại." (L175) | OK | (tuỳ chọn, sát số hơn) "…nặng gần gấp mười bảy lần…" | 21,05/1,246 = 16,9; 21,45/1,275 = 16,8. "Hơn mười lăm" đúng nhưng hơi thấp. |
| CH02 | "…hồi đầu năm, mã lớn nhất chỉ chiếm khoảng mười sáu phần trăm." (L176) | OK | — | VIC w0 = 16,16%, đầu năm cũng là mã lớn nhất (VHM thứ hai 6,02%). |
| CH02 | Nhiệt kế cạnh lò lớn nhất nhà (L177–178) | OK | — | Hồ sơ mục 5.4. |
| CH03 | Tên chương "Năm 2026: chỉ số đứng yên, ba phần tư cổ phiếu đi xuống" (L180, thẻ `chapter`) | SỬA | "Chín tháng 2026: chỉ số đứng yên, ba phần tư cổ phiếu đi xuống" | Năm chưa hết (cùng lỗi "cả năm" ở factcheck trước, L162). |
| CH03 | "Ngày ba mươi mốt tháng mười hai năm hai nghìn không trăm hai mươi lăm, VN-Index đóng cửa ở một nghìn bảy trăm tám mươi tư điểm." (L183) | OK | — | 1.784,49 (CSV; [L01-8]). |
| CH03 | "Ngày ba mươi tháng chín năm nay, nó đóng cửa quanh một nghìn bảy trăm sáu mươi tám điểm." (L184) | OK | — | 1.768,62. |
| CH03 | "Giảm khoảng mười sáu điểm, chưa tới một phần trăm." (L185) | OK | — | −15,87 điểm, −0,89%. |
| CH03 | "Kênh lấy giá đóng cửa của bốn trăm cổ phiếu HOSE có đủ giá ở cả hai mốc, rồi đếm từng mã." (L187) | OK | — | n = 400 (406 trừ 6 mã niêm yết mới: AAN, DMX, GEL, HPA, LPS, TTE). |
| CH03 | "Hai trăm chín mươi mốt mã thấp hơn cuối năm ngoái. Tức là bảy mươi hai phẩy tám phần trăm. Gần ba phần tư." (L188–189) | OK | — | Tính lại: 291 dưới / 1 đứng (ORS) / 108 trên. |
| CH03 | "Mã đứng giữa hàng, người ta gọi là trung vị, giảm hơn mười một phần trăm." (L190–191) | OK | — | −11,345% (trung bình của mã thứ 200 và 201: −11,39 và −11,30). |
| CH03 | "Một phần ba số mã giảm từ hai mươi phần trăm trở lên, trong khi chỉ ba mươi hai mã tăng từ hai mươi phần trăm trở lên." (L192) | OK | — | 132/400 = 33,0%; 32 mã ≥ +20%. |
| CH03 | "Nếu bỏ vào mỗi mã một khoản tiền bằng nhau, chiếc giỏ đó âm khoảng mười phẩy sáu phần trăm." (L193) | OK | — | Bình quân đều −10,58%. |
| CH03 | "Khoảng cách gần mười điểm phần trăm so với VN-Index chính là cái giá của một chiếc giỏ bị lệch." (L194) | OK | (tuỳ chọn) "…phần lớn là cái giá…" | 10,58 − 0,89 = 9,69 điểm %. Ghi chú: cùng 400 mã, cùng giá điều chỉnh, rổ theo vốn hoá ≈ +1,2% (+21,7 điểm) → chênh do trọng số thực ra ≈ 11,8 điểm, nên "gần mười" là cách nói thận trọng, không nói quá. |
| CH03 | "HỎI: Mấy con số này ở đâu ra vậy?…" / "Đúng vậy, kênh tự tính từ giá đóng cửa công khai, cách tính ghi đầy đủ trong mô tả." (L195–196) | OK | — | Mô tả phải có đoạn "Cách tính" của hồ sơ mục 2.1 (luật 3). |
| CH03 | "…mã đã rời sàn trong năm không có trong mẫu, nên con số thật có thể còn tệ hơn." (L197) | OK | — | Survivorship, hồ sơ 2.1(a). "Có thể" ✓. |
| CH03 | "Còn giá dùng ở đây đã điều chỉnh theo cổ tức, nên số này hơi đẹp hơn giá trên bảng điện." (L198) | OK | — | Hồ sơ 2.1(b). Việc vnstock trả giá điều chỉnh vẫn là [SECONDARY, 21], nhưng đối chiếu tay PNJ/VIC khớp. |
| CH03 | "Hồi tháng tư, báo Tuổi Trẻ gọi hiện tượng này bằng một cụm từ: » Xanh chỉ số, đỏ danh mục." (L199–200) | OK | — | [9] đã mở: tiêu đề 16/04/2026 "Cổ phiếu Vingroup tiếp tục kéo trụ, VN-Index vẫn 'xanh chỉ số, đỏ danh mục'". |
| CH03 | "Năm hai nghìn không trăm hai mươi lăm, VN-Index tăng gần bốn mươi mốt phần trăm, nhưng theo Tuổi Trẻ, khoảng bốn mươi sáu phần trăm cổ phiếu niêm yết vẫn có lợi suất âm." (L201) | SỬA | "Năm hai nghìn không trăm hai mươi lăm, VN-Index tăng gần bốn mươi mốt phần trăm, nhưng theo Tuổi Trẻ, hơn bốn mươi sáu phần trăm số cổ phiếu trên thị trường vẫn có kết quả đầu tư âm." | [11] đã mở, nguyên văn: "hơn 46% số cổ phiếu trên thị trường ghi nhận kết quả đầu tư âm". Bài **không** có chữ "niêm yết" ("trên thị trường" có thể gồm UPCoM, là sàn đăng ký giao dịch, không phải niêm yết). Bài không nói ai tính ra con số 46%. Vế 1 đúng: CSV 2025 +40,87%; bài viết "gần 41%". |
| CH03 | "Chỉ số đo một chiếc giỏ có trọng số, không đo một cổ phiếu điển hình." (L202) | OK | — | — |
| CH04 | "Vậy cái gì giữ cho chỉ số gần như đứng yên? Con gà to nhất trong giỏ." (L206–207) | OK | — | Đóng vòng mở ✓. |
| CH04 | "Từ cuối năm ngoái tới ba mươi tháng chín, giá cổ phiếu VIC tăng khoảng một phần ba." (L208) | OK | — | `prices.csv`: 169,6 → 227,9 = +34,38% (giá điều chỉnh). |
| CH04 | "Theo ước tính của kênh, riêng mã này kéo VN-Index lên khoảng một trăm điểm, trong khi cả chỉ số giảm khoảng mười sáu điểm." (L209) | OK | — | 1.784,49 × 16,16% × 34,38% = 99,1 (`pts_q3` = 99,14). Đây là con số **phụ thuộc giả định "không free-float, không trần"** (Ghi chú "Cần kiểm lại", hồ sơ mục 8): nên có email xác nhận của HOSE trước khi đăng. |
| CH04 | "Nói cách khác: nếu VIC chỉ đứng giá, VN-Index cuối tháng chín có thể đã thấp hơn khoảng một trăm điểm." (L210) | OK | — | Phép giả định về quá khứ, có "có thể", không phải dự báo. |
| CH04 | "Cả nhóm bốn mã liên quan tới Vingroup giữ cho chỉ số khoảng một trăm lẻ năm điểm, dù hai trong bốn mã đó giảm." (L211) | SỬA | "Cả nhóm bốn mã liên quan tới Vingroup cộng lại cũng chỉ giữ khoảng một trăm điểm, vì có hai trong bốn mã đó giảm." | Số đúng: VIC +99,1 + VHM +15,8 + VRE −4,2 + VPL −5,9 = **+104,9**. VRE −25,08% **xác nhận** (`prices.csv`: 32,5 → 24,35); VPL −15,92% ✓. Nhưng (1) hồ sơ 2.4 dặn "con số điểm từng mã ghi 'khoảng', không ghi số lẻ", và "một trăm lẻ năm" nghe chính xác giả với một ước tính lệch ~38 điểm; (2) "dù" sai quan hệ logic: hai mã giảm chính là **lý do** cả nhóm chỉ hơn VIC 5 điểm. |
| CH04 | "Phần còn lại của thị trường, khoảng ba phần tư vốn hoá, kéo chỉ số xuống khoảng tám mươi điểm, tương đương giảm khoảng sáu phần trăm." (L212) | OK | — | Phần còn lại: w0 = 74,8%; −83,2 điểm; bình quân theo vốn hoá −6,24%. |
| CH04 | "Đây là ước tính thô, không khớp tuyệt đối với chỉ số, nên bạn chỉ cần nhớ độ lớn." (L213) | SỬA | "Đây là ước tính thô: cộng các phần này lại sẽ không ra đúng mức giảm mười sáu điểm của chỉ số, vì vậy bạn chỉ cần nhớ chiều và độ lớn." | Người nghe tự cộng +105 − 80 = +25 so với −16 thực tế: lệch ~40 điểm, lớn hơn cả mức biến động của chỉ số. "Không khớp tuyệt đối" nói nhẹ hơn thực tế. Tổng ước tính +21,7 so với −15,87 (`summary.json` → `points_q3`). |
| CH04 | "Báo Vietnambiz cũng tính ra kết quả cùng chiều: nửa đầu năm VN-Index tăng hơn bốn phần trăm, nhưng bỏ nhóm Vingroup ra thì âm gần hai phần trăm." (L214) | SỬA | "Một chuyên gia phân tích được báo Vietnambiz dẫn lời cũng ra kết quả cùng chiều: nửa đầu năm VN-Index tăng hơn bốn phần trăm, nhưng bỏ nhóm Vingroup ra thì âm gần hai phần trăm." | [13] đã mở: +4,23% và "loại trừ… nhóm Vingroup, chỉ số chung lại giảm khoảng 1,81%" ✓, nhưng số do **giám đốc nghiên cứu của một công ty tư vấn đầu tư** đưa ra, không phải báo tự tính. Không cần nêu tên công ty. Chữ nguồn trên màn hình CH04 cũng ghi "Vietnambiz (dẫn chuyên gia)". CSV 30/06: +4,23% ✓. |
| CH04 | "HỎI: Vậy cứ mua mấy mã lớn nhất là chắc ăn…?" / "Kênh không trả lời câu hỏi nên mua mã nào. Nhưng dữ liệu cho thấy hai điều." (L215–216) | OK | — | Luật 2 ✓. |
| CH04 | "Một, ngay trong mười mã lớn nhất sàn, năm nay có mã giảm hơn hai mươi phần trăm, và chính nó kéo chỉ số xuống nhiều nhất." (L217) | OK | — | MCH −21,91%, ≈ −11,2 điểm, âm nhiều nhất trong ước tính; hạng 10 về vốn hoá ngày 30/09 (hạng 7 đầu năm). Không đọc tên mã ✓. "Kéo xuống nhiều nhất" cũng là ước tính của kênh (cùng phương pháp L209). |
| CH04 | "Hai, đây là nhìn lại. Không ai biết trước năm nào, mã nào sẽ là con gà tăng giá." (L218) | OK | — | Chống dự báo ✓. |
| CH04 | "Và đây là khoảnh khắc mình muốn bạn nhớ nhất." (L219) | OK | — | — |
| CH04 | "Ngày mười tám tháng năm, VN-Index đóng cửa ở mức cao nhất năm, gần một nghìn chín trăm hai mươi tám điểm, cao hơn đầu năm tám phần trăm." (L220) | SỬA | "Ngày mười tám tháng năm, VN-Index đóng cửa ở mức cao nhất từ đầu năm tới nay, gần một nghìn chín trăm hai mươi tám điểm, cao hơn cuối năm ngoái tám phần trăm." | 1.927,94; +8,04% ✓ (đỉnh đóng cửa; đỉnh trong phiên 1.933,11 ngày 19/05). Năm chưa hết: quý IV có thể có đỉnh mới, và "cao nhất năm" sẽ sai khi video được xem sau đó (cùng lý do "cả năm" ở factcheck trước). Chữ "tới nay" có thể thay bằng "tính tới cuối tháng chín". |
| CH04 | "Nhìn chỉ số, đó là ngày đẹp nhất năm." (L221) | SỬA | "Nhìn chỉ số, đó là ngày đẹp nhất trong chín tháng đầu năm." | Cùng lý do L220. |
| CH04 | "Nhưng cùng ngày hôm đó, sáu mươi tư phần trăm cổ phiếu trên HOSE vẫn thấp hơn giá đầu năm." (L222) | OK | — | `breadth_daily.csv` 18/05: 64,0%; tính lại từ `prices.csv`: 256/400 = 64,0% ✓. |
| CH04 | "Từ đáy tháng ba tới đầu tháng mười, tỉ lệ này chưa lúc nào xuống dưới năm mươi tám phần trăm." (L223) | SỬA | "Từ đáy tháng ba tới cuối tháng chín, tỉ lệ này chưa lúc nào xuống dưới năm mươi tám phần trăm." | Số đúng: thấp nhất 58,0% ngày 14/04 (sau 23/03), tới 06/10 vẫn vậy. Nhưng mốc chốt của video là 30/09 (luật 6: không dùng dữ liệu phiên đang "nóng"); kết quả không đổi khi cắt ở 30/09. |
| CH05 | "Giờ quay lại tài khoản… năm cơ chế…" / "Thứ nhất: bạn không sở hữu chỉ số, bạn sở hữu vài mã." (L227–228) | OK | — | — |
| CH05 | "Năm nay nhóm cổ phiếu giảm đông hơn hẳn, nên cầm ba, bốn mã chọn gần như ngẫu nhiên thì dễ rơi vào nhóm giảm hơn." (L229) | OK | — | 72,8% mã giảm; suy luận đơn giản (hồ sơ 3.1). |
| CH05 | "Ngay cả các quỹ cổ phiếu, nửa đầu năm trung bình âm khoảng một phần trăm, trong khi VN-Index tăng hơn bốn phần trăm." (L230) | OK | — | [13]: "hiệu suất bình quân của 28 quỹ mở cổ phiếu… (giảm 1,12%)". Chữ trên màn hình có thể ghi "28 QUỸ MỞ CỔ PHIẾU". |
| CH05 | "Thứ hai: thời điểm… Giả sử cuối năm ngoái bạn bỏ mười triệu, lời lỗ đúng theo VN-Index. Ngày mười tám tháng năm… bỏ thêm năm mươi triệu." (L231–233) | OK | (tuỳ chọn) "…bạn bỏ thêm năm mươi triệu, cũng theo đúng VN-Index." | Giả định; nói rõ khoản thứ hai cũng theo chỉ số thì phép tính L234 mới khớp. |
| CH05 | "Đến ba mươi tháng chín, sáu mươi triệu đó còn khoảng năm mươi lăm phẩy tám triệu: âm khoảng bảy phần trăm, dù chỉ số âm chưa tới một phần trăm." (L234) | OK | — | Tính lại: 10 × 1.768,62/1.784,49 = 9,911; 50 × 1.768,62/1.927,94 = 45,868 → **55,779 triệu, −7,03%** ✓. |
| CH05 | Ẩn dụ xe buýt ở đỉnh đồi (L235) | OK | — | — |
| CH05 | "Ai bỏ thêm tiền đúng ngày đáy hai mươi ba tháng ba thì ngược lại, đang lãi." (L236) | SỬA | "Ai bỏ thêm năm mươi triệu đúng ngày đáy hai mươi ba tháng ba thì ngược lại: tới cuối tháng chín, cả tài khoản lãi khoảng chín phần trăm." | Số đúng: 9,911 + 50 × 1.768,62/1.591,17 = 9,911 + 55,576 = **65,49 triệu, +9,15%** ✓. "Đang" là thì hiện tại, sẽ sai khi video được xem về sau (factcheck trước, "bây giờ"); nêu mốc và độ lớn thì rõ hơn. |
| CH05 | "Nhưng không ai biết trước đâu là đỉnh, đâu là đáy. Ví dụ này để hiểu cơ chế, không phải để canh đáy." (L237) | OK | — | Luật 2 ✓. |
| CH05 | "Thứ ba: phí và thuế. Mỗi lần bán, bạn nộp thuế không phẩy một phần trăm giá bán, kể cả khi bán lỗ." (L238–239) | OK | — | **Nâng từ SECONDARY lên bằng chứng:** Báo Chính phủ (baochinhphu.vn, 27/03/2026): Luật Thuế TNCN 109/2025/QH15, "thu nhập từ chuyển nhượng chứng khoán thực hiện nộp thuế 0,1% trên giá chuyển nhượng chứng khoán từng lần". Thuế tính trên giá bán nên có cả khi lỗ ✓. |
| CH05 | "Mỗi chiều mua hay bán, phí môi giới thường khoảng không phẩy mười lăm tới không phẩy ba mươi lăm phần trăm, tuỳ công ty." (L240) | SỬA | "Mỗi chiều mua hay bán, phí môi giới thường khoảng không phẩy mười lăm tới không phẩy ba mươi lăm phần trăm, có nơi thấp hơn, tuỳ công ty." | Dải 0,15–0,35% và trần 0,5% chỉ có từ trang tổng hợp/blog (Topi, VFS, VCBS — SECONDARY, như hồ sơ [17]); cùng các trang đó cho biết có nơi thu thấp hơn hoặc 0% theo gói. Thêm "có nơi thấp hơn" để không nói quá. Chưa có biểu phí gốc của 3–5 công ty (việc còn mở của hồ sơ). |
| CH05 | "HỎI: Phí có không phẩy mấy phần trăm…?" / "Vì nó cộng dồn theo số lần giao dịch." (L241–242) | OK | — | — |
| CH05 | "Với mức phí thấp, một vòng mua rồi bán tốn khoảng không phẩy bốn phần trăm số tiền." (L243) | SỬA | "Lấy mức phí không phẩy mười lăm phần trăm mỗi chiều, một vòng mua rồi bán tốn khoảng không phẩy bốn phần trăm số tiền." | 0,15 + 0,15 + 0,1 = 0,4% ✓. Nhưng 0,15% là **đầu dưới của dải phổ biến**, không phải "mức thấp" (L240 vừa nói có nơi thấp hơn). Nêu rõ giả định thì người xem tự thay mức phí của mình. |
| CH05 | "Tài khoản năm mươi triệu, mỗi tháng xoay hết vốn hai lần, một năm trả khoảng bốn triệu tám trăm nghìn đồng phí và thuế." (L244) | OK | — | 50 triệu × 0,4% × 24 = **4,8 triệu** ✓ (tính tuyến tính, giá không đổi, bỏ qua vốn giảm dần). |
| CH05 | "Gần mười phần trăm số vốn, hơn nửa tháng lương của người thu nhập chín triệu." (L245) | OK | — | 4,8/50 = 9,6%; 4,8 > 4,5 ✓. Thu nhập bình quân quý I/2026 = 9,0 triệu (positioning mục 1, NSO). |
| CH05 | "Thứ tư: vay ký quỹ, hay margin… kính lúp… phải trả tiền thuê." (L246–247) | OK | — | — |
| CH05 | "Giả sử bạn có năm mươi triệu, vay thêm năm mươi triệu với lãi mười ba phẩy năm phần trăm một năm, mức phổ biến đầu năm nay." (L248) | OK | (tuỳ chọn) "…mức khá thường gặp đầu năm nay." | [14] đã mở: 12,75% → 13,5% (cuối 01), 13,8% → 14% (giữa 02), 13% (03), một nơi giữ ~12,5%. 13,5% nằm giữa dải 12,5–14% → chấp nhận được. |
| CH05 | "Sáu tháng sau, cổ phiếu giảm mười phần trăm. Không vay, bạn mất mười phần trăm. Có vay, bạn mất gần hai mươi bảy phần trăm vốn của mình." (L249–250) | OK | — | 90 − (50 + 3,375) = 36,625 → **−26,75%** ✓. |
| CH05 | "Kể cả khi cổ phiếu đứng yên suốt sáu tháng, tiền lãi vẫn lấy đi gần bảy phần trăm vốn." (L251) | OK | — | 3,375/50 = 6,75% ✓. |
| CH05 | "Giảm sâu hơn, bạn có thể bị bán bớt cổ phiếu để thu nợ, đúng lúc giá đang thấp." (L252) | OK | — | Cơ chế chung, có "có thể"; tỷ lệ ký quỹ từng nơi CHƯA KIỂM nhưng câu không nêu số. |
| CH05 | "Thứ năm: cảm xúc. Mua đuổi khi chỉ số lên đỉnh, bán tháo khi chỉ số rơi…" (L253–254) | OK | — | Suy luận (hồ sơ 3.5), không nêu số. |
| CH05 | "Ở Việt Nam, mình không tìm thấy số liệu công khai nào về tỷ lệ nhà đầu tư đang lãi hay lỗ, nên sẽ không đưa ra con số nào." (L255) | OK | — | Hồ sơ 3.5, 8. Lời thoại nói đúng mức ("không tìm thấy"); xem hàng chữ màn hình CH05 bên dưới. |
| CH06 | "Mình không bảo bạn nên mua, bán hay giữ gì. Chỉ có năm câu hỏi…" (L259–260) | OK | — | Luật 2 ✓. |
| CH06 | Câu Một–Ba (L261–263) | OK | — | Câu hỏi tự kiểm, không khuyến nghị. |
| CH06 | "Bốn: mình có vay margin không, và nếu cổ phiếu giảm thêm hai mươi phần trăm thì sao?" (L264) | SỬA | "Bốn: mình có vay margin không, và nếu cổ phiếu giảm hai mươi phần trăm thì tài khoản còn bao nhiêu?" | "Giảm **thêm**" có thể nghe như ngụ ý thị trường sẽ còn giảm (luật 2: không dự báo). Bỏ "thêm" thì vẫn là phép thử sức chịu đựng. |
| CH06 | "Năm: lần gần nhất mình mua, là vì hiểu doanh nghiệp đó, hay vì thấy chỉ số đang lên?" (L265) | OK | — | — |
| CH06 | "Nếu tài khoản của bạn có những mã lớn đã tăng mạnh năm nay, nó có thể tốt hơn chỉ số. Độ lệch của chiếc giỏ cắt cả hai chiều." (L266–267) | OK | — | Mặt trái (luật 4), không nêu mã ✓. |
| CH06 | "Nếu bạn mua quỹ ETF mô phỏng chỉ số, kết quả bám chỉ số mà quỹ theo, trừ phí, và nhiều quỹ không theo VN-Index." (L268) | OK | (tuỳ chọn) "…trừ phí và sai lệch, và nhiều quỹ theo những chỉ số khác như VN30, không phải VN-Index." | Suy luận (hồ sơ 4.2); "nhiều quỹ không theo VN-Index" đúng dù số quỹ theo VN-Index là ít hay bằng không. Nêu "VN30" thì cụ thể hơn. Câu trung tính, không gợi ý mua. |
| CH06 | "Nếu tính từ đáy tháng ba, bức tranh dễ chịu hơn nhiều. Tính từ giữa tháng một, nó còn tệ hơn. Đầu năm chỉ là một mốc trên lịch." (L269) | SỬA | "Mốc tính cũng đổi kết quả: tính từ đáy tháng ba, VN-Index tăng hơn mười một phần trăm, dù hai phần ba số cổ phiếu vẫn thấp hơn giá hôm đó; tính từ giữa tháng một, cả chỉ số lẫn đa số cổ phiếu đều giảm sâu hơn. Đầu năm chỉ là một mốc trên lịch." | **Sai với cổ phiếu điển hình.** Tính lại từ `prices.csv`, 23/03 → 30/09: VN-Index **+11,15%**, rổ theo vốn hoá +13,5%, nhưng **266/400 mã (66,5%) vẫn thấp hơn giá 23/03, trung vị −6,5%**, rổ đều −5,1%. "Dễ chịu hơn nhiều" chỉ đúng với chỉ số và tài khoản đi theo chỉ số. Vế "giữa tháng một" đúng: 19/01 → 30/09 VN-Index −6,75%, 312/400 (78%) mã giảm, trung vị −13,8%. Bản ngắn hơn nếu cần giữ độ dài: "Tính từ đáy tháng ba, VN-Index tăng hơn mười một phần trăm; tính từ giữa tháng một, nó giảm gần bảy phần trăm. Đầu năm chỉ là một mốc trên lịch." **Hồ sơ mục 4 ý 4 cũng sai, cần sửa.** |
| CH06 | "Và số liệu ở đây chỉ gồm cổ phiếu trên HOSE, chưa tính HNX và UPCoM." (L270) | OK | — | Hồ sơ 2.1(c). |
| CH06 | "Tóm lại, VN-Index không nói sai… vài mã rất lớn quyết định phần lớn… Còn tài khoản của bạn là…" (L271–273) | OK | — | 10 mã ≈ 51–52% vốn hoá. |
| CH06 | "Nếu năm nay tài khoản của bạn đỏ… không có nghĩa bạn kém cỏi… thước đo không dành cho mình." (L274–275) | OK | — | — |
| CH06 | "Bài hai… Lệnh của bạn đi đâu, giá được khớp ra sao, và vì sao mua hôm nay mà chưa bán ngay được." (L276–277) | OK | — | T+2, T+0 chưa áp dụng [research A14/A16]; kiểm lại trước khi làm bài 2. |
| CH06 | Câu hỏi bình luận, "Không cần nêu tên mã nhé." (L278) | OK | — | Tránh bình luận hỏi mã ✓. |
| Màn hình CH03 | `kinetic` "2025: VN-INDEX +40,9% · ~46% CỔ PHIẾU NIÊM YẾT LỢI SUẤT ÂM" (L67) | SỬA | "2025: VN-INDEX +40,9% · HƠN 46% CỔ PHIẾU TRÊN THỊ TRƯỜNG ĐẦU TƯ ÂM (TUỔI TRẺ)" | Như L201. +40,9% khớp CSV (+40,87%). |
| Màn hình CH04 | `candles` mark 18/05 "Đỉnh năm 1.927,94 (đóng cửa) · +8,0%" (L76) | SỬA | "Cao nhất từ đầu năm · 1.927,94 (đóng cửa) · +8,0%" | Như L220. Số đúng (+8,04%). |
| Màn hình CH05 | `kinetic` "LÃI 13,5%/NĂM CHẠY KỂ CẢ KHI GIÁ ĐỨNG YÊN → −6,75%" (L88–89) | SỬA | "LÃI 13,5%/NĂM CHẠY KỂ CẢ KHI GIÁ ĐỨNG YÊN → −6,75% VỐN SAU 6 THÁNG" | Thiếu mốc thời gian, dễ đọc thành −6,75%/năm. |
| Màn hình CH05 | `kinetic` "VIỆT NAM: KHÔNG CÓ SỐ LIỆU CÔNG KHAI VỀ TỶ LỆ NHÀ ĐẦU TƯ LÃI/LỖ" (L90) | SỬA | "VIỆT NAM: KÊNH CHƯA TÌM THẤY SỐ LIỆU CÔNG KHAI VỀ TỶ LỆ NHÀ ĐẦU TƯ LÃI/LỖ" | Chữ trên hình khẳng định tuyệt đối; lời thoại (L255) và hồ sơ (CHƯA KIỂM) chỉ nói "không tìm thấy". |
| Màn hình CH03 | `bars` phân bố "…Tô đỏ 5 cột trái, xanh 5 cột phải" (L60–62) | OK | — | Tính lại khớp đúng **13 · 73 · 46 · 80 · 79 · 56 · 21 · 13 · 12 · 7** với khoảng nửa mở bên phải `[a, b)`; cột "0…+10" chứa 1 mã đứng giá (ORS 0,00%), nên cột xanh đầu tiên có 1 mã không tăng. Có thể ghi "0…+10 (gồm 1 mã đứng giá)". Nếu engine chia khoảng đóng bên phải thì ra 13·73·46·80·**80**·56·**20**·13·12·7, nên phải dùng `[a, b)`. |

## 2. Kiểm luật kênh (positioning mục 1, research 1.3)

| Luật | Kết quả |
|---|---|
| Không bán gì | OK — không link, không nhóm, không tên app/công ty chứng khoán. B-roll "không lộ tên app" ✓. |
| Không dự báo / không khuyến nghị | OK về tổng thể (L134, L216, L218, L237, L259). Cần sửa 4 chỗ nghe như nói về tương lai hoặc trạng thái "hiện tại": L220–221 + mark CH04 ("cao nhất năm" khi năm chưa hết), L236 ("đang lãi"), L264 ("giảm thêm"). Chương CH03 "Năm 2026" → "Chín tháng 2026". |
| Mã cổ phiếu chỉ để giải thích cơ chế chỉ số | OK — VIC và "nhóm Vingroup" chỉ dùng cho tỷ trọng/đóng góp điểm, không đánh giá doanh nghiệp; MCH không đọc tên; REE/SAM là sự kiện lịch sử. Chỉ hiện chữ VIC trên treemap ✓. |
| Mọi số có nguồn | Có; số tự tính đều tính lại khớp (mục 4). Hai chỗ ghi nguồn chưa đúng: L214 (Vietnambiz dẫn lời chuyên gia, không phải báo tự tính), L201 (phạm vi "trên thị trường", không phải "niêm yết"). Phí 0,15–0,35% vẫn SECONDARY. |
| Nói cả mặt trái (luật 4) | Có đoạn "khi nào không đúng" (L266–270). L269 phải sửa vì vế "từ đáy tháng ba" sai với cổ phiếu điển hình. |
| Dữ liệu quá khứ (luật 6) | Mốc chốt 30/09 ✓, nhưng L223 dùng dữ liệu tới "đầu tháng mười" (06/10), nên đổi thành "cuối tháng chín". **Lưu ý cho người duyệt:** research 1.3 ghi ví dụ VN-Index nên dùng giai đoạn "đã kết thúc ≥ 3 tháng trước ngày đăng", positioning luật 6 ghi "ít nhất vài tuần". Mốc 30/09 chỉ cách ngày đăng dự kiến khoảng 2–3 tuần: đạt luật 6 nhưng không đạt mức 3 tháng của research 1.3. Người duyệt cần chốt một chuẩn. |
| Miễn trừ | Lời thoại có (L134); thẻ 4–5 giây đầu + mô tả (research 1.5) phải có trên bản dựng. |

## 3. TTS — chỗ dễ đọc sai

| Chỗ | Rủi ro | Gợi ý (chỉ trong bản gửi TTS; màn hình giữ nguyên) |
|---|---|---|
| "VN-Index" (rất nhiều dòng, L118–L278) | Đánh vần "V-N", hoặc đọc "index" kiểu tiếng Anh | Dùng bảng `SAY` của video trước (ví dụ "Vi-en In-đéc"); nghe thử một câu. |
| "HOSE" (L127, 150, 172, 187, 222, 270, 276) | Đọc thành "hâu-z" (tiếng Anh "hose") | "Hô-se" / "hô-dê", nghe thử. Nếu vẫn lạ thì "sàn thành phố Hồ Chí Minh" ở vài chỗ. |
| "VIC" (L172, 208, 210) | Đọc "vích" hoặc "vi-ai-xi" lẫn lộn giữa các câu | Chọn **một** cách đọc và dùng cố định, ví dụ "vê-i-xê"; nghe thử. |
| "REE và SAM" (L153) | "REE" thành "ri", "SAM" thành tên riêng "Sam" | Đánh vần: "e-rờ e e" và "ét a em-mờ", nghe thử. |
| "GDP" (L154) | Đọc "gi-đi-pi" tiếng Anh | "giê-đê-pê". |
| "Vingroup" (L211, 214) | Nửa Việt nửa Anh ("vin-grúp") | "Vin-gờ-rúp", nghe thử. |
| "Vietnambiz" (L214) | Tên báo dài, dễ vấp | "Việt Nam Biz"; hoặc theo L214 đã sửa, nói "báo Vietnambiz" một lần. |
| "ETF" (L268) | Đọc tiếng Anh "i-ti-ép" hoặc gộp chữ | "e-tê-ép" (cách đọc phổ biến ở VN), nghe thử. |
| "HNX và UPCoM" (L270) | "HNX" đánh vần tiếng Anh; "UPCoM" đọc "úp-com" hoặc từng chữ | "hát-en-ích" và "úp-com". |
| "margin" (L246, 264) | Đọc "mác-gin" / "mạc-dzin" | "ma-gin", nghe thử; L246 đã có "vay ký quỹ" đi trước ✓. |
| "App" (L124, giọng HỎI) | "áp" hay "a-pê-pê" | "áp". |
| "một phẩy hai lăm" (L174) | Dạng nói tắt, TTS có thể đọc "hai lăm" thành "hai năm" | Nếu lạ thì "một phẩy hai mươi lăm". |
| "ngày mười tám tháng năm" (L220, 233) | "tháng năm" (May) có thể bị ngắt thành "tháng / năm" | Nghe thử; nếu cần thì "tháng Năm". |
| "‖", "HỎI:", "»" | Đọc ra thành tiếng | Lọc trước khi gửi TTS (Ghi chú đã nêu ✓). |
| Số | Lời thoại CH00–CH06 không còn chữ số nào (đã kiểm bằng grep) ✓. | — |

## 4. Tính lại các số trong "Ghi chú" (từ CSV) và các lời trích

| Mục Ghi chú | Kết quả tính lại / đối chiếu | Kết luận |
|---|---|---|
| VN-Index 31/12/2025 → 30/09/2026: −0,89%, −15,87 điểm | 1.784,49 → 1.768,62: **−0,889%, −15,87** | OK |
| Độ rộng (n = 400): 291 / 108 / 1; trung vị −11,35%; rổ đều −10,58%; ≤ −20%: 132; ≥ +20%: 32 | Tính lại từ `breadth_2026.csv` (`pct_ytd_q3`): 291 / 108 / 1; −11,345; −10,578; 132; 32 | OK |
| "Gần mười điểm phần trăm" = 9,69 | 10,578 − 0,889 = 9,69 | OK |
| Phân bố 30/09: 13·73·46·80·79·56·21·13·12·7 | Khớp với khoảng `[a, b)`; với khoảng `(a, b]` ra 13·73·46·80·80·56·20·13·12·7 | OK — engine phải dùng `[a, b)` |
| Tập trung 30/09: 21,46% · 52,2% · 1,28% (400 mã); 21,0 · 51,2 · 1,25 (406 mã) | 400 mã: **21,45–21,46%** (giá 30/09 từ `prices.csv` hoặc `c0 × (1+pct)`) · **52,23%** · **1,275%**; 406 mã: 21,05 · 51,24 · 1,246 | OK |
| "Hơn mười lăm lần" = 16,8 | 16,8 (400) / 16,9 (406) | OK (có thể nói "gần mười bảy") |
| Đầu năm VIC ≈ 16,2%; 10 mã ≈ 47,6% | 16,16%; 47,57%; VIC là mã lớn nhất đầu năm | OK |
| VIC +34,38%, ≈ +99 điểm | `prices.csv` 169,6 → 227,9 = +34,375%; 1.784,49 × 0,1616 × 0,34375 = 99,1 | OK |
| Nhóm Vingroup ≈ +104,9; phần còn lại ≈ −83,2; rổ không Vingroup ≈ −6%; tổng +21,7 so với −15,9 | 104,91; −83,20; −6,24% theo vốn hoá (w0 = 74,83%); tổng 21,71 | OK |
| **VRE −25,08%** (tự tính thêm) | `prices.csv`: 31/12/2025 = 32,50 → 30/09 = 24,35 → **−25,08%**; `pts_q3` ≈ −4,16 điểm, w0 0,93% | **OK — xác nhận** |
| VPL −15,92% | 94,2 → 79,2 = −15,92% | OK |
| MCH −21,91%, ≈ −11,2 điểm, trong 10 mã lớn nhất 30/09 | 178,0 → 139,0 = −21,91%; −11,17 điểm; hạng 10 về vốn hoá 30/09 (hạng 7 đầu năm) | OK |
| 18/05: 1.927,94 (+8,04%); 64,0% dưới giá đầu năm | CSV ✓; tính lại từ `prices.csv`: 256/400 = 64,0% | OK |
| Thấp nhất sau 23/03 = 58,0% (14/04); tốt nhất 19/01 = 37,2% | ✓ / ✓ (`breadth_daily.csv`) | OK — nhưng lời thoại nên cắt ở 30/09 (L223) |
| (mới) Từ đáy 23/03 → 30/09 | VN-Index +11,15%; **266/400 mã dưới giá 23/03 (66,5%)**, trung vị −6,50%, rổ đều −5,1%, rổ vốn hoá +13,5% | Lời thoại L269 và hồ sơ mục 4 ý 4 **sai**, xem bảng mục 1 |
| (mới) Từ 19/01 → 30/09 | VN-Index −6,75%; 312/400 mã giảm (78%), trung vị −13,75% | Vế "giữa tháng một… tệ hơn" OK |
| **Xe buýt: 55,78 triệu, −7,03%** | 9,9111 + 45,8681 = **55,779 → −7,035%** | OK |
| **Thêm 50 triệu ở đáy 23/03: 65,49 triệu, +9,1%** | 9,9111 + 55,5760 = **65,487 → +9,15%** | OK |
| **Phí: 50 triệu × 0,4% × 24 = 4,8 triệu ≈ 9,6%** | 4.800.000 đ; 9,6% (tuyến tính) | OK |
| Margin: −26,75% / −6,75% | 36,625 → −26,75%; 46,625 → −6,75% | OK |
| Cold open −9,67% | (−12 − 20 + 3)/3 = −9,67 | OK |
| Giỏ hàng 100 → 105 | ✓ | OK |
| 2025: VN-Index +40,9% | CSV 31/12/2024 → 31/12/2025: +40,87% | OK |
| 30/06: +4,23% (khớp Vietnambiz) | 1.860,01/1.784,49 − 1 = +4,23% | OK |
| **Luật CK 2019 Điều 4 khoản 2 (nguyên văn)** | "Cổ phiếu là loại chứng khoán xác nhận quyền và lợi ích hợp pháp của người sở hữu đối với một phần vốn cổ phần của tổ chức phát hành." Khớp từng chữ với lời trích L144 (luatvietnam.vn: Luật 54/2019/QH14, 26/11/2019; hethongphapluat.com). thuvienphapluat 403; vbpl.vn không tải được nội dung | OK — nguyên văn |
| **SEC** [L01-119] | "Stocks have historically had the greatest risk and highest returns among the three major asset categories." / "…you could lose some or all of your money." | L148 SỬA (thiếu "trong ba nhóm tài sản chính") |
| Ghi chú "Thứ trong tuần: 30/09/2026 là thứ Tư" | ✓ | OK |

## 5. Nguồn kiểm thêm trong lần fact-check này

- Luật Chứng khoán 2019 (54/2019/QH14), toàn văn — LuatVietnam: https://luatvietnam.vn/chung-khoan/luat-chung-khoan-2019-179050-d1.html ; Điều 4: https://hethongphapluat.com/luat-chung-khoan-2019/dieu-4 (thuvienphapluat.vn trả 403; vbpl.vn chỉ trả trang chờ)
- SEC — Beginners' Guide to Asset Allocation, Diversification, and Rebalancing: https://www.sec.gov/about/reports-publications/investorpubsassetallocationhtm
- VnExpress — Hậu trường phiên giao dịch đầu tiên với 2 cổ phiếu [5]: https://vnexpress.net/hau-truong-phien-giao-dich-dau-tien-voi-2-co-phieu-4133477.html
- CafeF 05/10/2026 — vốn hoá HOSE tháng 9 [7]: https://cafef.vn/von-hoa-co-phieu-tren-hose-boc-hoi-298000-ty-dong-trong-thang-9-188261005202836242.chn (405 cổ phiếu, 8,55 triệu tỷ, 66,52% GDP 2025, ~95%)
- Tuổi Trẻ 16/04/2026 [9]: https://tuoitre.vn/co-phieu-vingroup-tiep-tuc-keo-tru-vn-index-van-xanh-chi-so-do-danh-muc-20260416140700503.htm
- Tuổi Trẻ 14/01/2026 [11]: https://tuoitre.vn/chung-khoan-tang-gan-41-mot-nam-vi-sao-nhieu-nguoi-van-thua-lo-20260114171752752.htm ("hơn 46% số cổ phiếu trên thị trường ghi nhận kết quả đầu tư âm"; "gần 41%"; bỏ Vingroup +10,6%)
- Vietnambiz [13]: https://vietnambiz.vn/gui-tiet-kiem-vuot-nhieu-kenh-dau-tu-nua-dau-nam-202671014143080.htm (+4,23%; bỏ Vingroup −1,81%; 28 quỹ mở cổ phiếu −1,12%; số do chuyên gia một công ty tư vấn đầu tư đưa ra)
- Tuổi Trẻ 18/03/2026 — lãi margin [14]: https://tuoitre.vn/lai-suat-margin-len-den-14-cong-ty-chung-khoan-bat-dau-chuyen-ap-luc-sang-nha-dau-tu-20260318140649637.htm (12,5–14%)
- Báo Chính phủ — Thuế TNCN đối với chuyển nhượng chứng khoán (Luật 109/2025/QH15, 0,1% trên giá chuyển nhượng từng lần): https://baochinhphu.vn/thue-thu-nhap-ca-nhan-doi-voi-chuyen-nhuong-chung-khoan-10226032718480641.htm
- Phí môi giới 0,15–0,35%, trần 0,5% (SECONDARY, trang tổng hợp): https://topi.vn/phi-giao-dich-chung-khoan.html ; https://www.vfs.com.vn/chi-phi-giao-dich-chung-khoan

**Việc còn mở (không chặn bản 2):** email HOSE xác nhận phương pháp VN-Index (ảnh hưởng L209–213); biểu phí gốc của 3–5 công ty chứng khoán cho dải
0,15–0,35%; sửa hồ sơ `2026-10-07-long-c1-research.md` mục 4 ý 4 theo số mục 4 ở trên; người duyệt chốt chuẩn "≥ 3 tháng" hay "vài tuần" (mục 2).
