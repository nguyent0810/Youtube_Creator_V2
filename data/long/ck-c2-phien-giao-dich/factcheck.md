# Fact-check — script.md (bản 1) · ck-c2-phien-giao-dich (Chứng khoán từ số 0 — C2)

Ngày kiểm: 07/10/2026. Đối chiếu: hồ sơ `docs/channels/chung-khoan/2026-10-07-long-c2-research.md` (số `[n]` = nguồn trong hồ sơ
đó); luật kênh `2026-10-06-positioning.md` mục 1; `motion/long/RETENTION.md` (lời hứa lộ trình); dữ liệu `data/ck/vnindex_1d.csv`
và `data/ck/breadth_2026/prices.csv` (tính lại bằng pandas). Ưu tiên văn bản gốc: Quy chế VNX 22/QĐ-HĐTV, Luật 109/2025/QH15
(bản .docx), bản tiếp thu–giải trình dự thảo thông tư thay TT 119/2020 trên ssc.gov.vn, cổng chinhphu.vn. Không sửa script.

**Kết luận: OK 101 · SỬA 15 · BỎ 0** (116 hàng: 4 tiêu đề, 77 hàng lời thoại — vài dòng gộp — và 35 hàng chữ/cảnh trên màn
hình). Mục luật kênh, TTS, tính lại Ghi chú và nguồn ở cuối, không tính vào tổng.

Nhãn: OK = đúng nguồn / chấp nhận được · SỬA = sai số, nói quá nguồn, mơ hồ, hoặc chạm luật kênh · BỎ = nên cắt câu.

**Năm điểm quan trọng nhất**
1. **Luật giao dịch dưới KRX: đã tìm được văn bản gốc.** Quyết định **22/QĐ-HĐTV ngày 18/04/2025** của Sở GDCK Việt Nam (VNX) ban
   hành *Quy chế Niêm yết và giao dịch chứng khoán niêm yết*, hiệu lực "kể từ ngày Hệ thống công nghệ thông tin… chính thức vận
   hành" (= 05/05/2025). Nguyên văn khớp script: Điều 17 khoản 2 điểm c, d (ATO/ATC "không được ưu tiên trước lệnh giới hạn mua giá
   trần hoặc lệnh giới hạn bán giá sàn đã nhập vào hệ thống trước đó"); Điều 20 khoản 2a (định kỳ: giá có khối lượng lớn nhất);
   Điều 21 (không sửa/huỷ LO, ATO trong ATO; không sửa/huỷ LO, ATC trong ATC; sửa lệnh thì "thứ tự ưu tiên… tính kể từ khi lệnh sửa
   được nhập"); Điều 31 khoản 2 (tham chiếu = giá đóng cửa ngày giao dịch gần nhất); Điều 32 (lô lẻ: khớp lệnh tập trung + thoả
   thuận, **chỉ lệnh LO**, đơn vị 1). **Giờ cụ thể (9:00/9:15/11:30/13:00/14:30/14:45/15:00) không nằm trong Quy chế VNX** mà trong
   văn bản hướng dẫn của HOSE — chưa mở được (hsx.vn trả trang rỗng); giờ vẫn chỉ có nguồn tài liệu thành viên (khớp nhau).
2. **L224 "Hàng đợi gần như không nhúc nhích" ngược với dữ liệu thanh khoản.** KL khớp VN-Index 09/03 = **1,38 tỷ cp**, cao hơn
   bình quân 2026 tới 06/03 (**1,05 tỷ**) khoảng 32%, **cao thứ 5 trong 186 phiên năm 2026**. Hàng đợi ở nhiều mã vẫn nhích, chỉ là
   bên bán đông hơn hẳn. Sửa câu (và bỏ "rất nhanh" ở L220).
3. **L199 "chưa có giá nào để xem" sai với bảng giá thực tế:** trong ATO/ATC bảng giá hiện **giá khớp dự kiến** (tài liệu thành
   viên tóm tắt quy chế HOSE dùng đúng cụm này). L200 "thay vì ai bấm nhanh hơn thì được trước" cũng gây hiểu sai: trong khớp định
   kỳ, ở mức giá biên **vẫn ưu tiên thời gian** (chính ví dụ của video: 600 cp bán ở 20.000 chỉ khớp 400). L186 "chưa ai mua bán với
   ai" sai vì giao dịch thoả thuận chạy từ 9:00.
4. **Câu "cơ quan soạn thảo nói rõ" (L265) nay có nguồn gốc trên ssc.gov.vn** — Bản tổng hợp tiếp thu, giải trình dự thảo thông tư
   thay TT 119/2020: *"Việc áp dụng cơ chế CCP là tách biệt với việc áp dụng cơ chế bán chứng khoán chờ về và giao dịch trong ngày.
   Hiện tại, cơ chế bán chứng khoán chờ về và giao dịch trong ngày chưa được thực hiện, UBCKNN sẽ căn cứ vào tình hình thực tế của
   thị trường để quyết định thời điểm triển khai theo quy định tại Thông tư 120/2020/TT-BTC."* CCP "theo kế hoạch vào quý I năm
   2027". TT 145/2026/TT-BTC ký **30/09/2026**, hiệu lực **16/11/2026** (chinhphu.vn). → Nội dung đúng; nên ghi chủ thể là UBCKNN và
   tách câu 40 âm tiết.
5. **Thiếu một thay đổi lớn ngay sau ngày đăng:** theo TT 139/2025/TT-BTC, **toàn bộ cổ phiếu niêm yết HNX chuyển sang HOSE**:
   phiên cuối ở HNX **23/12/2026**, phiên đầu ở HOSE **28/12/2026** (Thời báo Tài chính 30/09/2026). Thẻ "HNX ±10%" (L288, CH06) sẽ
   cũ đi sau 2,5 tháng → thêm vào câu "quy định còn đang thay đổi" (L292) và thẻ màn hình.

**Năm điểm tác giả nhờ kiểm — kết quả:** (1) ATO/ATC không chen trước LO trần/sàn đặt trước, không sửa/huỷ trong ATO/ATC, sửa giá /
tăng KL xếp lại, lô lẻ chỉ LO và khớp như lô chẵn: **đúng, nguồn gốc = QĐ 22/QĐ-HĐTV** (VNX, 18/04/2025); MTL (cùng MOK, MAK) là các
lệnh thị trường trong Quy chế, tài liệu thành viên ghi HOSE nhận LO + MTL trong khớp liên tục; giờ giao dịch: chỉ tài liệu thành viên.
(2) "Chạy CCP không có nghĩa là có ngay T+0": **đúng, nguồn ssc.gov.vn** (trích ở trên); quý I/2027: ssc.gov.vn + Chủ tịch UBCKNN
(Vietstock 03/06/2026); TT 145/2026 hiệu lực 16/11/2026: **đúng** (chinhphu.vn). (3) TT 120/2020 **Điều 10 = "Giao dịch trong ngày"**
(nguyên tắc: hợp đồng giao dịch trong ngày, một tài khoản/CTCK…) — **đúng** (LSVN 15/02/2021 trích Điều 10; ssc.gov.vn dẫn "theo quy
định tại Thông tư 120/2020/TT-BTC"). (4) Trần phí 0,45% (TT 102/2021, thay TT 128/2018, từ 01/01/2022): **không tìm thấy văn bản thay
thế**; TT 83/2024 và 125/2026, 34/2026 chỉ áp cho giá dịch vụ của VNX/VSDC, không đụng phí môi giới CTCK → giữ, nhưng chữ "mức trần"
dễ lẫn với "giá trần" (L268). T+2 về trưa: **đúng** — VSD từ 29/08/2022 hoàn tất thanh toán 11:00–11:30 ngày T+2, thành viên phân bổ
cho khách **trước 13:00**, bán được phiên chiều T+2 (trước đó phải chờ sáng T+3); dự thảo CCP vẫn thanh toán 11:30 sáng T+2.
**Ví dụ thứ Năm / thứ Sáu đúng từng ngày:** mua thứ Năm 05/03 → T+1 thứ Sáu 06/03 → **T+2 thứ Hai 09/03**, bán được **từ 13:00 thứ
Hai** (không bán được ATO hay phiên sáng thứ Hai, nên vào hàng ở giá sàn **sau** những người đặt từ sáng); mua thứ Sáu 06/03 → T+1 thứ
Hai 09/03 → **T+2 thứ Ba 10/03**, bán được **từ 13:00 thứ Ba**; cả ngày thứ Hai không có cổ phiếu để đặt lệnh bán (người đặt lệnh bán
phải có đủ chứng khoán trên tài khoản — ssc.gov.vn). Bán thứ Hai 09/03 → tiền về thứ Tư 11/03. 05–11/03 đều có phiên trong dữ liệu
(không có ngày nghỉ). (5) 09/03/2026: **233 mã giảm sàn trên HOSE** (Nhân Dân, Thời báo Tài chính); 349 (Mekong ASEAN) / 339 (Stockbiz)
là toàn thị trường → script dùng đúng 233 + "trên HOSE"; "hàng loạt cổ phiếu dư bán sàn lên đến hàng triệu cổ phiếu" (TBTC, nguyên
văn) — script nói "không có ai mua" hơi quá → "không còn ai mua ở giá ấy"; bối cảnh: chiến sự Mỹ–Israel với Iran, WTI > 110 USD,
chứng khoán châu Á giảm mạnh cùng ngày (Caixin/NST/NPR 09/03/2026; TBTC: thị trường quốc tế giảm sâu, giá dầu; Mekong ASEAN dẫn báo cáo
CTCK: xung đột Trung Đông) → câu bối cảnh **đúng**.

## 1. Bảng kiểm từng dòng

### 1a. Tiêu đề

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Tiêu đề làm việc | "NGÀY VN-INDEX MẤT 115 ĐIỂM: MỘT PHIÊN GIAO DỊCH HOSE VẬN HÀNH THẾ NÀO?" (L1) | OK | — | −115,05 ✓. |
| Tiêu đề (1) | "Ngày VN-Index mất 115 điểm: một phiên giao dịch HOSE vận hành thế nào?" (L8) | OK | — | Số thật, không phóng đại ✓. Nhược điểm: mở bằng tin thị trường 7 tháng trước → dễ thu hút người tìm nhận định/dự báo, trong khi video không giải thích vì sao chỉ số giảm. |
| Tiêu đề (2) | "Vì sao có ngày muốn bán cổ phiếu mà không bán được? Một phiên HOSE từ 9 giờ tới 15 giờ" (L9) | OK | — | **Khuyến nghị.** Đúng câu hỏi trung tâm (vòng mở 2, đóng ở CH03) mà video trả lời trọn vẹn; không lỗi thời; không hứa lãi, không dự báo; có "có ngày" nên không phóng đại. 09/03 vẫn ở thumbnail/cold open. |
| Tiêu đề (3) | "Giá trần, giá sàn, ATO, ATC, T+2: đi hết một phiên chứng khoán cùng người mới" (L9–10) | OK | — | Đúng nội dung, tốt cho tìm kiếm, nhưng là danh sách 5 thuật ngữ → kém tò mò nhất. |

### 1b. Lời thoại

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| CH00 | "Giả sử chiều thứ Hai, chín tháng ba năm hai nghìn không trăm hai mươi sáu, bạn mở bảng giá trên điện thoại." (L140) | OK | — | 09/03/2026 là thứ Hai ✓. |
| CH00 | "Hơn một nửa số mã trên sàn HOSE hiện cùng một màu: xanh lơ." (L141) | OK | — | 233/(11+10+366) = 233/387 = 60,2% ✓ (số cuối phiên; câu đặt "chiều" là hợp lý). 387 không gồm chứng quyền. |
| CH00 | "Trên bảng giá, xanh lơ nghĩa là giá sàn, mức thấp nhất một cổ phiếu được phép xuống trong ngày." (L142) | OK | — | Màu là quy ước hiển thị; định nghĩa giá sàn ✓. |
| CH00 | "Hôm ấy, giữa lúc căng thẳng ở Trung Đông làm thị trường thế giới và giá dầu chao đảo, VN-Index mất một trăm mười lăm điểm." (L143) | OK | (tuỳ chọn) "giữa lúc xung đột ở Trung Đông…" | Caixin/NST 09/03/2026: chiến sự Mỹ–Israel với Iran, WTI vượt 110 USD/thùng, chứng khoán châu Á giảm mạnh, VN-Index −6% được nêu tên; TBTC [11]: thị trường quốc tế giảm sâu, giá dầu; Mekong ASEAN [10]: báo cáo CTCK "xung đột tại Trung Đông". "Căng thẳng" là cách nói nhẹ hơn thực tế. |
| CH00 | "Đây là lần đầu tiên chỉ số giảm hơn một trăm điểm trong một phiên." (L144) | OK | — | Mekong ASEAN [10] nguyên văn "lần đầu tiên…giảm trên 100 điểm một phiên"; dữ liệu kênh 2018–2026: chỉ 1 phiên < −100. Trước 2018 không thể: chỉ số là bình quân gia quyền các mã bị chặn ±7% (trước đó ±5%), đỉnh 2007 ~1.170 và 04/2018 ~1.204 → tối đa ~84 điểm/phiên. |
| CH00 | "Trên HOSE, hai trăm ba mươi ba mã giảm sàn, chỉ mười một mã tăng." (L145) | OK | — | Nhân Dân [8]: "11 mã tăng, 10 mã đứng giá, 366 mã giảm, trong đó 233 mã giảm sàn" ✓; TBTC [11] cũng 233. |
| CH00 | "Theo kênh tự tính, cổ phiếu đứng giữa hàng hôm ấy giảm khoảng sáu phẩy tám phần trăm, tức là sát mức sàn." (L146) | OK | — | Tính lại: n = 395, trung vị −6,80% ✓. |
| CH00 | "Nhưng chi tiết lạ nhất không nằm ở con số." (L147) | OK | — | — |
| CH00 | "Hết phiên, nhiều mã vẫn còn hàng triệu cổ phiếu đang chờ bán ở giá sàn, mà không có ai mua." (L148) | SỬA | "Hết phiên, hàng loạt mã vẫn còn hàng triệu cổ phiếu chờ bán ở giá sàn, mà không còn ai đặt mua ở giá ấy." | TBTC [11]: "hàng loạt cổ phiếu dư bán sàn lên đến hàng triệu cổ phiếu". Dư bán ở giá sàn lúc đóng cửa nghĩa là **không còn** lệnh mua ở giá sàn; nhưng trong ngày vẫn có người mua (KL khớp 1,38 tỷ cp) → "không có ai mua" nói quá. |
| CH00 | HỎI "…mình muốn bán mà cũng không bán được à?" / "Đúng vậy." (L149–150) | OK | — | — |
| CH00 | "Và có những người còn không được đặt lệnh bán, dù đã mua cổ phiếu từ thứ Sáu tuần trước." (L151) | OK | — | T+2 (thứ Sáu → thứ Ba) + nhà đầu tư "vẫn phải có đủ chứng khoán trên tài khoản trước khi đặt lệnh bán", bán chờ về "chưa được thực hiện" (ssc.gov.vn, bản giải trình dự thảo thay TT 119) ✓. |
| CH00 | "Để hiểu vì sao, mình sẽ đi cùng phiên chợ hôm ấy theo chiếc đồng hồ trên màn hình, từ chín giờ sáng tới ba giờ chiều, rồi thêm hai ngày sau tiếng chuông." (L152) | OK | — | Lộ trình "bản đồ bằng hình" ✓ (mục 2). 34 âm tiết, sát ngưỡng 35. |
| CH00 | Chào kênh, bài hai, miễn trừ (L153–155) | OK | — | Luật 2 ✓; thẻ miễn trừ 4–5 giây vẫn phải có trên hình. |
| CH01 | "Ở bài một, mình ví HOSE như một khu chợ có ban quản lý, và bạn nhờ công ty chứng khoán đi chợ hộ." (L159) | OK | — | Khớp C1 L151–152 ✓. |
| CH01 | Lệnh đi từ ứng dụng → CTCK → hệ thống Sở; "bốn thứ" (L160–161) | OK | — | — |
| CH01 | Lệnh giới hạn: "mua với giá cao nhất là bao nhiêu, hoặc bán với giá thấp nhất là bao nhiêu" (L162–163) | OK | — | Định nghĩa LO (Quy chế 22, tài liệu thành viên): "mua… tại mức giá xác định hoặc thấp hơn; bán… tại mức giá xác định hoặc cao hơn" ✓. |
| CH01 | "Trên HOSE, một lô chẵn là một trăm cổ phiếu… từ một tới chín mươi chín cổ phiếu, bạn dùng lô lẻ." (L164–166) | OK | — | Lô chẵn 100 (tối đa 500.000/lệnh), lô lẻ 1–99 [3]; QĐ 22 Điều 32 khoản 3: đơn vị lô lẻ là 01 cổ phiếu ✓. |
| CH01 | "Từ khi HOSE chạy hệ thống mới, lô lẻ được khớp trong cùng các phiên như lô chẵn, nhưng chỉ đặt được lệnh giới hạn." (L167) | OK | — | QĐ 22/QĐ-HĐTV Điều 32 khoản 1–2 ("khớp lệnh tập trung và… thoả thuận"; "chỉ được phép nhập lệnh LO đối với giao dịch lô lẻ"); thông báo HOSE 13/03/2025 (Vietstock): lô lẻ thêm khớp định kỳ ✓. Lô lẻ khớp trên sổ lệnh riêng — câu không nói ngược lại. |
| CH01 | HỎI một lô bao nhiêu tiền / "Tuỳ mã." / "…cổ phiếu đứng giữa sàn HOSE có giá khoảng mười lăm nghìn đồng." (L168–170) | OK | — | Tính lại: 406 mã, giá đóng cửa gần nhất ≤ 30/09/2026, trung vị 15.400 ✓ (giá điều chỉnh; 367 mã có phiên đúng 30/09: 14.200). |
| CH01 | "Vậy một lô khoảng một triệu rưỡi, chưa tính phí, chưa tới một phần năm tháng thu nhập chín triệu." (L171) | OK | (tuỳ chọn) "…chưa tới một phần năm thu nhập bình quân một tháng, khoảng chín triệu." | 1,54/9,0 = 17,1% ✓. Thêm "bình quân" cho khớp màn hình và nguồn (NSO quý I/2026). |
| CH01 | Bước giá 10 / 50 / 100 đồng (L172–175) | OK | — | Tài liệu thành viên [3]: < 10.000: 10 đ · 10.000–49.950: 50 đ · ≥ 50.000: 100 đ ✓. |
| CH01 | "Mỗi sáng, mỗi cổ phiếu có một giá tham chiếu, thường là giá đóng cửa của phiên trước." (L176–177) | OK | — | QĐ 22 Điều 31 khoản 2: "giá đóng cửa của ngày giao dịch gần nhất trước đó" ✓; "thường" che các trường hợp đặc biệt ✓. |
| CH01 | ±7% trần/sàn; ví dụ 20.000 → 21.400 / 18.600 (L178–180) | OK | — | ±7% [3]; 20.000 × 1,07 = 21.400; × 0,93 = 18.600 (bội của 50) ✓. |
| CH01 | "Bảng giá thường tô giá trần màu tím, giá sàn màu xanh lơ, giá tham chiếu màu vàng." (L181) | OK | — | Quy ước hiển thị, không phải quy định Sở; "thường" ✓. |
| CH01 | "Giữ hai chữ giá sàn trong đầu nhé…" (L182) | OK | — | Gieo motif ✓. |
| CH02 | "Chín giờ sáng, chợ mở. Nhưng mười lăm phút đầu, chưa ai mua bán với ai cả." (L186) | SỬA | "Chín giờ sáng, chợ mở. Nhưng mười lăm phút đầu, chưa lệnh mua bán nào được khớp cả." | Giao dịch **thoả thuận** chạy từ 9:00–11:30 [3] → "chưa ai mua bán với ai" sai về chữ. Ý đúng: lệnh khớp lệnh chưa khớp. |
| CH02 | ATO; "Hệ thống chỉ gom lệnh lại"; "…mức giá khớp được nhiều cổ phiếu nhất." (L187–189) | OK | — | QĐ 22 Điều 20 khoản 2a: "mức giá thực hiện mà tại đó khối lượng giao dịch đạt lớn nhất" ✓. |
| CH02 | Ví dụ sổ lệnh: 400 / 300 / 800, "Đó là giá mở cửa." (L190–194) | OK | — | Tính lại lũy kế: 19.900 → min(1.500; 400) = 400 · 20.000 → min(800; 1.000) = 800 · 20.100 → min(300; 1.800) = 300 ✓. |
| CH02 | "Ai khớp cũng khớp ở cùng một giá. Kể cả người đặt mua hai mươi nghìn một trăm, cũng chỉ trả hai mươi nghìn." (L195–196) | OK | — | ✓. |
| CH02 | "Trong mười lăm phút gom lệnh, lệnh đã đặt thì không sửa, không huỷ được." (L197) | OK | — | QĐ 22 Điều 21 khoản 2: "không được phép sửa, hủy các lệnh LO, ATO" ✓. |
| CH02 | HỎI "…sao không đợi xem giá rồi mới đặt?" / "Vì lúc ấy chưa có giá nào để xem. Giá mở cửa chỉ thành hình khi mọi lệnh đã được gom đủ." (L198–199) | SỬA | Giữ câu HỎI; thay L199: "Vì lúc ấy chưa có giá khớp thật. Bảng giá chỉ hiện một giá dự kiến, và nó còn đổi cho tới khi gom xong lệnh lúc chín giờ mười lăm." | Trong ATO/ATC bảng giá hiển thị **giá khớp dự kiến** (tài liệu thành viên [3] mục 5.3: "giá hiển thị… là giá khớp dự kiến"). Người mới mở app sẽ thấy giá nhảy lúc 9:00–9:15 → câu hiện tại mâu thuẫn với điều họ thấy. |
| CH02 | "Cách gom này cho những lệnh dồn từ tối hôm trước một cái giá chung, thay vì ai bấm nhanh hơn thì được trước." (L200) | SỬA | "Cách gom này cho mọi lệnh đặt trước giờ mở cửa cùng một cái giá, thay vì mỗi người một giá tuỳ lúc bấm." | *[suy luận]* của kênh. "Thay vì ai bấm nhanh hơn thì được trước" sai một nửa: khớp định kỳ **vẫn ưu tiên thời gian** ở mức giá biên (ví dụ của chính video: 600 cp bán ở 20.000 chỉ khớp 400 — ai đặt trước khớp trước), và CH02 L203 lại nói "ai đến trước thì đứng trước" → tự mâu thuẫn. Bỏ "tối hôm trước" (giờ nhận lệnh trước là của từng CTCK). |
| CH02 | "…hệ thống giao dịch mới mà HOSE chạy từ tháng năm năm hai nghìn không trăm hai mươi lăm, gọi là KRX." (L201) | OK | — | Báo Chính phủ 05/05/2025 [6] ✓. |
| CH02 | "Lệnh ATO không còn được chen lên trước những lệnh mua giá trần, hay lệnh bán giá sàn, đã đặt từ trước. Nghĩa là ở giá sàn, ai đến trước thì đứng trước." (L202–203) | OK | — | **Nguồn gốc:** QĐ 22/QĐ-HĐTV (VNX, 18/04/2025) Điều 17 khoản 2 điểm c: ATO "không được ưu tiên trước lệnh giới hạn mua giá trần hoặc lệnh giới hạn bán giá sàn đã nhập vào hệ thống trước đó" ✓. "Không còn" đúng: trước KRX, ATO/ATC được ưu tiên trước LO. |
| CH02 | "Hôm chín tháng ba, chi tiết nhỏ này quyết định ai bán được, ai không." (L204) | SỬA | "Hôm chín tháng ba, ở những mã nằm sàn, thứ tự xếp hàng ấy quyết định ai bán được trước." | Không có dữ liệu sổ lệnh nào cho thấy riêng quy tắc ATO "quyết định" ai bán được; điều quyết định là ưu tiên thời gian ở giá sàn (mà quy tắc ATO chỉ là một phần). Câu hiện tại nói quá nguồn. |
| CH03 | Khớp liên tục, hai luật, "giá khớp là giá của lệnh đang nằm chờ sẵn" (L208–212) | OK | — | Tài liệu thành viên [3] mục 3–4 ("giá thực hiện là mức giá của các lệnh giới hạn đối ứng nằm chờ trên sổ lệnh") ✓. |
| CH03 | Ví dụ mua 20.100 gặp bán chờ 20.050 → khớp 20.050 (L213–214) | OK | — | 20.050 hợp lệ (bước 50) ✓. |
| CH03 | "Còn nếu dùng lệnh thị trường, bạn nhận ngay giá tốt nhất đang chờ, nhưng không biết trước chính xác mình sẽ trả bao nhiêu." (L215) | OK | — | MTL: mua ở giá bán thấp nhất đang có, phần còn lại thành LO (QĐ 22 Điều 17 khoản 2b; [3]) ✓. Có thể khớp nhiều mức giá → "không biết trước chính xác" đúng. |
| CH03 | "Mười một giờ rưỡi, chợ nghỉ trưa tới một giờ chiều, rồi khớp liên tục tiếp tới hai giờ rưỡi." (L216) | OK | — | [3][4] (tài liệu thành viên; Quy chế VNX không ghi giờ cụ thể). |
| CH03 | "Trong lúc khớp liên tục, lệnh chưa khớp có thể sửa giá, sửa số lượng, hoặc huỷ. Nhưng sửa giá hay tăng số lượng thì lệnh phải xếp lại từ cuối hàng." (L217–218) | OK | (tuỳ chọn) thêm "mỗi lần chỉ sửa một thứ" | QĐ 22 Điều 21 khoản 3 (LO được sửa giá, khối lượng, huỷ; "thứ tự ưu tiên… tính kể từ khi lệnh sửa được nhập"); giảm KL giữ thứ tự (thông báo HOSE 13/03/2025) ✓. Không sửa đồng thời giá và KL [3]. |
| CH03 | "Giờ quay lại ngày chín tháng ba. Khi gần như ai cũng muốn bán, giá rơi xuống sàn rất nhanh, và không được thấp hơn nữa." (L219–220) | SỬA | L220: "Khi gần như ai cũng muốn bán, giá có thể rơi xuống sàn, và không được thấp hơn nữa." | Không có nguồn về tốc độ rơi của từng mã; TBTC [11] tả chỉ số "giảm sâu từ đầu phiên", có lúc "phục hồi nhẹ", rồi giảm tiếp tới cuối phiên — tức không phải một mạch. |
| CH03 | Hàng người bán ở giá sàn theo thời gian; "cột dư bán"; "chỉ khớp khi có người mua đi tới tận chỗ bạn đứng" (L221–223) | OK | — | Ưu tiên thời gian ✓; dư bán ở giá sàn là khối lượng chờ bán ✓. |
| CH03 | "Hôm ấy, người mua quá ít. Hàng đợi gần như không nhúc nhích." (L224) | SỬA | "Hôm ấy, ở nhiều mã, người mua quá ít so với người bán. Hàng đợi nhích rất chậm, và hết phiên vẫn còn dài." | **Ngược dữ liệu:** KL khớp HOSE 1,38 tỷ cp (Nhân Dân; CSV 1.380.753.348) = cao hơn bình quân 2026 khoảng 32%, phiên thanh khoản cao thứ 5/186 của năm 2026 (kênh tự tính). Hàng có nhích; vấn đề là bên bán đông hơn. |
| CH03 | HỎI "Vậy giá sàn là để bảo vệ ai?…" / "Biên độ không chặn việc giảm giá. Nó chỉ giới hạn mỗi ngày, giá đi được bao xa." (L225–226) | OK | — | ✓. |
| CH03 | "Hết phiên, mọi người có một đêm để đọc thêm thông tin, trước khi giá lại được phép đi tiếp bảy phần trăm." (L227) | OK | — | *[suy luận]* đúng cơ chế (không nói mục đích chính thức) — chấp nhận. |
| CH03 | "Mặt trái là đúng ngày bạn cần bán nhất, bạn có thể phải xếp sau rất nhiều người, và hết ngày vẫn chưa tới lượt." (L228) | OK | — | Luật 4 (mặt trái) ✓. |
| CH03 | Re-hook "Giờ bạn đã hiểu vì sao…" + "Còn mười lăm phút quyết định giá của cả sáng hôm sau." (L229–230) | OK | — | Đóng vòng 2, mở vòng 3 ✓. |
| CH04 | ATC 14:30, chốt 14:45, "theo luật khớp được nhiều nhất" (L234–235) | OK | — | QĐ 22 Điều 20; giờ [3]. |
| CH04 | "Lệnh ATC cũng không được chen lên trước những lệnh mua trần, bán sàn đã đặt từ trước." (L236) | OK | — | QĐ 22 Điều 17 khoản 2 điểm d ✓. |
| CH04 | "Giá đóng cửa này sẽ là giá tham chiếu của sáng hôm sau. Lệnh nào tới lúc ấy chưa khớp thì hết hiệu lực…" (L237–238) | OK | — | QĐ 22 Điều 31; LO "có hiệu lực… cho đến khi kết thúc đợt khớp lệnh định kỳ đóng cửa" [3]; ATC chưa khớp hết hiệu lực ✓. |
| CH04 | "Từ hai giờ bốn mươi lăm tới ba giờ chỉ còn giao dịch thoả thuận…, thường là những lô lớn." (L239) | OK | — | [3] (thoả thuận 13:00–15:00, khớp lệnh hết 14:45) ✓. |
| CH04 | "VN-Index đóng cửa ở khoảng một nghìn sáu trăm năm mươi ba điểm, gần như đúng mức thấp nhất trong ngày." (L240–241) | OK | — | 1.652,79; đáy 1.650,75 (cách 2,04 điểm) ✓. |
| CH04 | "Sáng thứ Ba, giá tham chiếu của những mã nằm sàn chính là giá sàn hôm trước…" (L242) | OK | — | Hệ quả trực tiếp của Điều 31 ✓. |
| CH04 | Thứ Ba +1,5%, thứ Tư +3%, lấy lại hai phần ba (L243–244) | OK | — | +1,45% · +3,08% · 65,7% ✓. |
| CH04 | HỎI "bán hớ" / "Nhìn lại thì dễ nói vậy." / 23/03 thấp hơn ~60 điểm (L245–247) | OK | — | 1.591,17 → thấp hơn 61,62 ✓; 23/03 là đáy đóng cửa 2026 ✓. Cân bằng hai chiều ✓. |
| CH04 | "Không ai biết trước ngày mai. Video này không chấm đúng sai…" (L248–249) | OK | — | Luật 2 ✓. |
| CH05 | T+2: "T là ngày khớp lệnh. Hai ngày làm việc sau đó, tiền và cổ phiếu mới thật sự đổi chủ." (L253–256) | OK | — | [3]: cổ phiếu/CCQ/CW T+2 ✓. |
| CH05 | "Từ năm hai nghìn không trăm hai mươi hai, cổ phiếu về vào khoảng trưa ngày T cộng hai, nên bán được từ phiên chiều hôm đó." (L257) | OK | — | VSD từ 29/08/2022: thanh toán 11:00–11:30 T+2 (trước đó 15:30–16:00), thành viên phân bổ trước 13:00, bán được phiên chiều T+2 thay vì sáng T+3 (LSVN, VnBusiness [12]) ✓. Dự thảo CCP vẫn thanh toán "11h30 sáng T+2" (ssc.gov.vn). |
| CH05 | "Ai mua hôm thứ Năm, năm tháng ba, thì cổ phiếu về trưa thứ Hai. Chiều thứ Hai, họ được bán, đúng lúc giá đang nằm sàn." (L258–259) | OK | (tuỳ chọn, nối motif hàng đợi) thêm: "Và họ vào hàng ở giá sàn sau tất cả những người đã đặt lệnh từ sáng." | Lịch: 05/03 (thứ Năm) → T+2 = 09/03 (thứ Hai), bán từ 13:00 ✓. |
| CH05 | "Ai mua hôm thứ Sáu, sáu tháng ba, thì phải tới chiều thứ Ba mới bán được. Cả ngày thứ Hai, họ chỉ có thể đứng nhìn." (L260–261) | OK | — | 06/03 → T+2 = 10/03 (thứ Ba) ✓; không có bán chờ về ✓. |
| CH05 | HỎI mua sáng bán chiều; "giao dịch trong ngày… T cộng không" (L262–263) | OK | — | — |
| CH05 | "Quy định đã có chỗ cho nó, nhưng tới tháng mười năm nay vẫn chưa triển khai, và cũng chưa được bán cổ phiếu đang chờ về." (L264) | OK | — | TT 120/2020 **Điều 10 "Giao dịch trong ngày"** (LSVN 15/02/2021 trích các nguyên tắc của Điều 10); ssc.gov.vn: "Hiện tại, cơ chế bán chứng khoán chờ về và giao dịch trong ngày chưa được thực hiện" ✓. |
| CH05 | "Cơ chế bù trừ mới dự kiến chạy từ quý một năm hai nghìn không trăm hai mươi bảy, nhưng cơ quan soạn thảo nói rõ: chạy cơ chế đó không có nghĩa là có ngay giao dịch trong ngày." (L265) | SỬA | "Cơ chế bù trừ mới dự kiến chạy từ quý một năm hai nghìn không trăm hai mươi bảy. Nhưng Uỷ ban Chứng khoán Nhà nước đã nói rõ: đó là việc riêng, chưa kéo theo giao dịch trong ngày. Khi nào có, Uỷ ban sẽ quyết định theo tình hình thị trường." | Nội dung đúng; nguồn gốc nay là văn bản UBCKNN trên ssc.gov.vn (bản tiếp thu, giải trình dự thảo thay TT 119/2020): "Việc áp dụng cơ chế CCP là tách biệt với việc áp dụng cơ chế bán chứng khoán chờ về và giao dịch trong ngày… UBCKNN sẽ căn cứ vào tình hình thực tế của thị trường để quyết định thời điểm triển khai"; quý I/2027 cùng văn bản + Chủ tịch UBCKNN (Vietstock 03/06/2026). Câu cũ 40 âm tiết (quá ngưỡng 35) và "cơ quan soạn thảo" mơ hồ với người mới. |
| CH05 | "Chiều bán cũng vậy: tiền bán hôm nay, hai ngày làm việc sau mới thật sự về tài khoản." (L266) | OK | — | T+2 ✓ (dịch vụ ứng trước tiền bán của CTCK có phí — không cần nêu). |
| CH05 | "Còn chuyện tiền phí. Mỗi chiều mua hay bán, công ty chứng khoán thu phí môi giới. Mức trần là không phẩy bốn mươi lăm phần trăm, thực tế thường thấp hơn nhiều." (L267–268) | SỬA | L268: "Mỗi chiều mua hay bán, công ty chứng khoán thu phí môi giới. Quy định cho thu tối đa không phẩy bốn mươi lăm phần trăm, thực tế thường thấp hơn nhiều." | TT 102/2021/TT-BTC (từ 01/01/2022, thay TT 128/2018): môi giới cổ phiếu "tối đa 0,45% giá trị giao dịch" ✓; không tìm thấy văn bản thay thế (TT 83/2024, 34/2026, 125/2026 chỉ áp cho VNX/VSDC). Nhưng chữ **"mức trần"** trong video vừa dạy "giá trần" → người mới dễ nghe nhầm thành giá trần của cổ phiếu. |
| CH05 | "Mỗi lần bán, bạn nộp thêm thuế không phẩy một phần trăm trên giá bán, kể cả khi bán lỗ." (L269) | OK | — | Luật 109/2025/QH15 Điều 13 khoản 2: thuế = giá chuyển nhượng × 0,1% "theo từng lần chuyển nhượng" → kể cả khi lỗ ✓. |
| CH05 | "Luật thuế thu nhập cá nhân mới, hiệu lực từ một tháng bảy năm nay, giữ nguyên mức này:" + lời trích (L270–271) | OK | — | Đã đối chiếu bản .docx Luật 109/2025/QH15 (10/12/2025): Điều 13 khoản 2 nguyên văn "…được xác định bằng giá chuyển nhượng nhân (x) với thuế suất 0,1% theo từng lần chuyển nhượng" — lời trích chỉ bỏ "(x)" ✓; Điều 29 khoản 1: hiệu lực 01/07/2026 (trừ thu nhập kinh doanh, tiền lương áp dụng từ kỳ tính thuế 2026) ✓. |
| CH05 | Ví dụ một lô, phí 0,15%: −8.000 · ≈ −3.000 · ≈ +2.000 (L272–275) | OK | — | Tính lại khớp (mục 4). |
| CH05 | "Số tiền nhỏ, nhưng như bài một đã tính, nó lớn dần theo số lần bạn mua bán." (L276) | OK | — | C1 L243–244 (≈ 0,4%/vòng; 4,8 triệu/năm với 50 triệu xoay 2 lần/tháng) ✓. |
| CH06 | "Mình không bảo bạn nên mua hay bán lúc nào. Chỉ có năm câu…" (L280–281) | OK | — | Luật 2 ✓. |
| CH06 | Năm câu tự kiểm (L282–286) | OK | — | Câu 4: "phải đợi hai ngày làm việc, tới phiên chiều mới bán được, và tiền bán còn chờ thêm hai ngày nữa" ✓. Không câu nào gợi mua/bán. |
| CH06 | "Biên độ bảy phần trăm là của HOSE. Sàn HNX là mười phần trăm, sàn UPCoM là mười lăm phần trăm." (L287–288) | OK | — | [18, SECONDARY]; khớp dữ kiện cùng ngày (Mekong ASEAN: một mã HNX giảm sàn −10%). Xem L292: cổ phiếu niêm yết HNX chuyển sang HOSE từ 28/12/2026. |
| CH06 | ±20% ngày đầu niêm yết / sau tạm ngừng ≥ 25 phiên; CK hạn chế khớp định kỳ 15 phút (L289–290) | OK | — | [3]: "±20%… tạm ngừng, đình chỉ giao dịch từ hai mươi lăm (25) ngày giao dịch liên tiếp trở lên"; thông báo HOSE 13/03/2025: CK hạn chế "giao dịch cả ngày", định kỳ 15 phút ✓. |
| CH06 | "Nhà đầu tư tổ chức nước ngoài có cơ chế riêng. Họ được đặt lệnh mua cổ phiếu khi chưa có đủ tiền trong tài khoản." (L291) | OK | (tuỳ chọn) "Họ có thể được đặt lệnh mua…" | NPF (TT 68/2024; TT 145/2026 giữ: luatvietnam "Nhà đầu tư nước ngoài là tổ chức được mua cổ phiếu không cần đủ tiền khi đặt lệnh") ✓. Thực tế tuỳ CTCK đánh giá → "có thể được" chặt hơn. |
| CH06 | "Và quy định còn đang thay đổi. Một thông tư mới về bù trừ, thanh toán có hiệu lực từ mười sáu tháng mười một, nên trước khi đặt lệnh, hãy kiểm lại quy định hiện hành." (L292) | SỬA | "Và quy định còn đang thay đổi. Một thông tư mới về bù trừ, thanh toán có hiệu lực từ mười sáu tháng mười một năm nay. Cuối tháng mười hai, cổ phiếu niêm yết trên HNX cũng dự kiến chuyển hết sang HOSE. Nên trước khi đặt lệnh, hãy kiểm lại quy định hiện hành." | TT 145/2026/TT-BTC ký 30/09/2026, hiệu lực 16/11/2026 (chinhphu.vn) ✓. **Thiếu:** TT 139/2025/TT-BTC → phiên cuối cổ phiếu niêm yết ở HNX 23/12/2026, phiên đầu ở HOSE 28/12/2026 (Thời báo Tài chính 30/09/2026) — làm thẻ "HNX ±10%" lỗi thời ngay sau ngày đăng. Câu cũ 38 âm tiết → tách. |
| CH06 | Tóm lại (L293–297) | OK | — | L294 liệt kê 4 mục (RETENTION: tối đa 3) — xem mục 2. L296 "chỉ rơi tối đa bảy phần trăm" đúng cho ngày thường trên HOSE; ngoại lệ ±20% đã nói ở L289 ✓. |
| CH06 | Gợi bài 3 + câu hỏi bình luận (L298–299) | OK | — | Bài 3 = tập 5 giáo trình ("Biểu đồ đường, cột, nến") sau khi C2 gộp tập 3+4 ✓ (`2026-10-06-research.md` L286). |

### 1c. Chữ và cảnh trên màn hình (Kế hoạch hình ảnh)

| Chương | Câu trích (dòng) | Kết luận | Gợi ý sửa | Nguồn / ghi chú |
|---|---|---|---|---|
| Màn hình CH00 | `date` + `broll` điện thoại + `kinetic` ô "SÀN" xanh lơ, "XANH LƠ = GIÁ SÀN" (L43–45) | OK | — | Không lộ app/CTCK ✓. |
| Màn hình CH00 | `candles` mark "−115,05 ĐIỂM · 1.652,79" + "LẦN ĐẦU GIẢM > 100 ĐIỂM/PHIÊN" (L46–47) | OK | — | ✓. |
| Màn hình CH00 | `ledger` "HOSE · 09/03/2026": TĂNG 11 · ĐỨNG 10 · GIẢM 366 · SÀN 233 (L48–49) | OK | — | Nhân Dân [8] ✓ (TBTC chỉ xác nhận 233). |
| Màn hình CH00 | `breadth` 395 ô, "TRUNG VỊ −6,8% · SÀN = −7%" (L50–51) | OK | — | Tính lại ✓. Ghi "giá điều chỉnh, kênh tự tính". |
| Màn hình CH00 | `kinetic` "DƯ BÁN GIÁ SÀN: HÀNG TRIỆU CỔ PHIẾU · KHÔNG CÓ NGƯỜI MUA" (L52) | SỬA | "HÀNG LOẠT MÃ DƯ BÁN SÀN HÀNG TRIỆU CỔ PHIẾU · KHÔNG CÒN NGƯỜI MUA Ở GIÁ SÀN" (nguồn: Thời báo Tài chính 09/03/2026) | Như L148. |
| Màn hình CH00 | `question` + `timeline` đồng hồ phiên + `brand` (L53–55) | OK | — | — |
| Màn hình CH01 | `broll` chợ + `kinetic` "ỨNG DỤNG → CTCK → HỆ THỐNG CỦA SỞ (KRX)" (L58–59) | OK | — | — |
| Màn hình CH01 | `ledger` "MỘT LỆNH GIỚI HẠN (LO)" + `kinetic` "LÔ CHẴN = 100 · LÔ LẺ = 1–99 · LÔ LẺ: CÙNG PHIÊN, CHỈ LỆNH LO" (L60–61) | OK | Đổi nguồn trên màn: "Quy chế giao dịch CK niêm yết (VNX, QĐ 22/QĐ-HĐTV, 2025)" | QĐ 22 Điều 32 ✓. |
| Màn hình CH01 | `counter` 1.540.000 đ, "≈ 1/6 THU NHẬP BÌNH QUÂN 9 TRIỆU" (L62–63) | OK | — | 17,1% ≈ 1/6 ✓. |
| Màn hình CH01 | `bars` bước giá 126 · 234 · 46 mã, n = 406 (L64–66) | OK | — | Tính lại ✓ (giá điều chỉnh). |
| Màn hình CH01 | `ledger` khung giá 21.400 / 20.000 / 18.600; `kinetic` tham chiếu; `slam` "GIÁ SÀN" (L67–69) | OK | — | ✓. |
| Màn hình CH02 | `timeline` 9:00; `book` + `bars` 400 · 800 · 300 (L72–75) | OK | — | Tính lại ✓; nhãn "VÍ DỤ GIẢ ĐỊNH". |
| Màn hình CH02 | `kinetic` "15 PHÚT GOM LỆNH · KHÔNG SỬA, KHÔNG HUỶ · 9:15 KHỚP MỘT LẦN" (L76) | OK | — | QĐ 22 Điều 21 khoản 2 ✓. |
| Màn hình CH02 | `date` "05/05/2025" + `kinetic` "LỆNH ATO KHÔNG CHEN TRƯỚC LỆNH BÁN GIÁ SÀN ĐÃ ĐẶT TRƯỚC" (nguồn: "thông báo HOSE 13/03/2025 qua báo chí; quy định giao dịch HOSE 05/2025") (L78–79) | SỬA | Nguồn trên màn: "Quy chế Niêm yết và giao dịch CK niêm yết — VNX, QĐ 22/QĐ-HĐTV ngày 18/04/2025, Điều 17" | Chữ đúng; nguồn nay có văn bản gốc, không cần "qua báo chí". |
| Màn hình CH03 | `ledger` "HAI LUẬT KHỚP LỆNH" + "GIÁ KHỚP = GIÁ LỆNH ĐANG CHỜ" (L83–84) | OK | — | ✓. |
| Màn hình CH03 | `book` 20.100 gặp 20.050 → "KHỚP 20.050" (L85) | OK | — | ✓. |
| Màn hình CH03 | `kinetic` "LỆNH THỊ TRƯỜNG (MTL): KHỚP NGAY GIÁ TỐT NHẤT ĐANG CHỜ · PHẦN CÒN LẠI → LỆNH LO" (L86) | OK | — | QĐ 22 Điều 17 khoản 2b ✓. |
| Màn hình CH03 | `kinetic` "SỬA GIÁ / TĂNG SỐ LƯỢNG → XẾP LẠI CUỐI HÀNG · GIẢM SỐ LƯỢNG → GIỮ CHỖ" (L87) | OK | — | QĐ 22 Điều 21 khoản 3b; HOSE 13/03/2025 ✓. |
| Màn hình CH03 | `date` "09/03/2026" → `book` hàng đợi giá sàn, ô "LỆNH CỦA BẠN" (L88–89) | OK | Bắt buộc góc màn "VÍ DỤ GIẢ ĐỊNH" ngay trên cảnh này | Vì cảnh đi liền thẻ ngày thật, người xem dễ tưởng là sổ lệnh thật của một mã. |
| Màn hình CH03 | `broll` hàng người + "ẢNH MINH HOẠ"; `question` → `kinetic` biên độ (L90–91) | OK | — | ✓. |
| Màn hình CH03 | `slam` "MUỐN BÁN ≠ BÁN ĐƯỢC" (L92) | OK | — | — |
| Màn hình CH04 | `kinetic` "14:30–14:45 · GOM LỆNH · KHÔNG SỬA, KHÔNG HUỶ · ATC KHÔNG CHEN TRƯỚC… · GIÁ ĐÓNG CỬA = GIÁ THAM CHIẾU NGÀY MAI" (L96–97) | OK | — | QĐ 22 Điều 17, 21, 31 ✓. |
| Màn hình CH04 | `kinetic` "LỆNH CHƯA KHỚP → HẾT HIỆU LỰC · 14:45–15:00 CHỈ CÒN THOẢ THUẬN" (L98) | OK | — | [3] ✓. |
| Màn hình CH04 | `candles` marks 1.652,79 / 1.650,75 · 1.728,34 "≈ 2/3" · 1.591,17 "≈ 62 ĐIỂM" (L99–100) | OK | — | ✓. |
| Màn hình CH04 | `ledger` +1,45% · +3,08% · 1.591,17 "nhìn lại, không ai biết trước" (L101–102) | OK | — | ✓. |
| Màn hình CH04 | `question` → `slam` "KHÔNG AI BIẾT TRƯỚC NGÀY MAI" (L103) | OK | — | — |
| Màn hình CH05 | `kinetic` "T = NGÀY KHỚP · T+2 = HAI NGÀY LÀM VIỆC SAU · CỔ PHIẾU VỀ ~11:30 → BÁN ĐƯỢC TỪ PHIÊN CHIỀU" (VSD, từ 29/08/2022) (L107) | SỬA | "… · CỔ PHIẾU VỀ TÀI KHOẢN TRƯỚC 13:00 NGÀY T+2 → BÁN ĐƯỢC TỪ PHIÊN CHIỀU" | 11:00–11:30 là giờ VSD và ngân hàng hoàn tất thanh toán; thành viên phân bổ cho khách **trước 13:00** (thông báo VSD qua LSVN/VnBusiness). "~11:30" dễ khiến người xem thử đặt bán lúc 11:30. |
| Màn hình CH05 | `timeline` tuần 05–11/03/2026 (A mua thứ Năm, B mua thứ Sáu…) (L108–109) | OK | — | Lịch đúng từng ngày (xem đầu file) ✓. |
| Màn hình CH05 | `kinetic` "T+0 · BÁN CHỨNG KHOÁN CHỜ VỀ: CHƯA TRIỂN KHAI (10/2026)" + "CCP DỰ KIẾN QUÝ I/2027 — KHÔNG ĐỒNG NGHĨA CÓ NGAY T+0" (L110–111) | OK | Nguồn trên màn: "UBCKNN (ssc.gov.vn), 2026" | ✓. |
| Màn hình CH05 | `ledger` "PHÍ MÔI GIỚI · TRẦN 0,45% MỖI CHIỀU (THỰC TẾ THƯỜNG THẤP HƠN) · THUẾ TNCN 0,1% GIÁ BÁN · KỂ CẢ KHI LỖ" (L112–113) | SỬA | "PHÍ MÔI GIỚI · TỐI ĐA 0,45% MỖI CHIỀU (TT 102/2021 · THỰC TẾ THƯỜNG THẤP HƠN) · THUẾ TNCN 0,1% GIÁ BÁN · KỂ CẢ KHI LỖ" | Như L268 ("TRẦN" lẫn với giá trần). |
| Màn hình CH05 | `quote` Luật 109/2025/QH15, Điều 13 khoản 2, `radio: true` (L114) | OK | — | Nguyên văn đã đối chiếu ✓. |
| Màn hình CH05 | `ledger` một lô phí 0,15% + `slam` "+2 BƯỚC GIÁ MỚI HOÀ VỐN" "VÍ DỤ GIẢ ĐỊNH · PHÍ TUỲ CÔNG TY" (L115–117) | OK | — | Tính lại ✓. |
| Màn hình CH06 | `ledger` "5 CÂU TRƯỚC LỆNH ĐẦU TIÊN" (L120) | OK | — | — |
| Màn hình CH06 | `ledger` "KHI NÀO KHÔNG ĐÚNG" (6 thẻ) … "QUY ĐỊNH ĐANG ĐỔI: THÔNG TƯ 145/2026 HIỆU LỰC 16/11/2026" (L121–122) | SỬA | Thẻ 6: "QUY ĐỊNH ĐANG ĐỔI: TT 145/2026 HIỆU LỰC 16/11/2026 · CỔ PHIẾU NIÊM YẾT HNX CHUYỂN SANG HOSE TỪ 28/12/2026 (DỰ KIẾN)"; thẻ 5: "TỔ CHỨC NƯỚC NGOÀI: CÓ THỂ MUA KHÔNG CẦN ĐỦ TIỀN TRƯỚC" | Như L292, L291. |
| Màn hình CH06 | `timeline` trọn vẹn → `slam` "HIỂU LUẬT CHƠI TRƯỚC" sub "RỒI MỚI BẤM NÚT"; gợi bài 3; `question` (L123–125) | OK | (tuỳ chọn) sub "TRƯỚC KHI BẤM NÚT" | "Rồi mới bấm nút" hơi giống lời giục giao dịch — xem mục 2. |

## 2. Kiểm luật kênh (positioning mục 1) và RETENTION

| Luật | Kết quả |
|---|---|
| 1. Không bán gì / không nêu tên CTCK, ngân hàng | OK — lời thoại và chữ màn hình không có tên CTCK, ngân hàng, app, mã cổ phiếu (đã rà; chỉ có HOSE, HNX, UPCoM, KRX, VN-Index). Tên CTCK chỉ nằm trong link nguồn của hồ sơ. Cảnh `broll` dặn không lộ app ✓. |
| 2. Không dự báo / không khuyến nghị | OK (L155, L248–249, L280). Không câu nào "nên mua/bán/giữ". **Câu người mới có thể hiểu thành lời khuyên (mức nhẹ):** (a) L171 "một lô… chưa tới một phần năm tháng thu nhập" — có thể nghe như "rẻ, mua được"; giữ được vì là phép đo chi phí, nhưng đừng thêm câu khích lệ. (b) L272–275 "+2 bước mới bắt đầu có lãi" — có thể bị hiểu thành mẹo lướt sóng; đã có nhãn "VÍ DỤ GIẢ ĐỊNH" và L276 nói phí lớn dần theo số lần mua bán ✓. (c) `slam` CH06 "RỒI MỚI BẤM NÚT" và L281 "trước khi bấm lệnh đầu tiên" ngầm giả định người xem sẽ giao dịch — chấp nhận cho khoá người mới, tuỳ chọn đổi "TRƯỚC KHI BẤM NÚT". (d) L259 "Chiều thứ Hai, họ được bán, đúng lúc giá đang nằm sàn" — không ngụ ý nên bán; ổn. |
| 3. Mọi số có nguồn | Có. Số tự tính đều tính lại khớp (mục 4). Ba chỗ nói quá nguồn: L148 ("không có ai mua"), L224 ("không nhúc nhích" — ngược dữ liệu KL), L204 ("quyết định ai bán được"). Một câu suy luận sai cơ chế: L200. |
| 4. Nói cả mặt trái | Có: L228 (mặt trái biên độ), L246–247 (nhìn lại hai chiều), L287–292 (khi nào không đúng). Nên thêm HNX → HOSE (L292). |
| 6. Dữ liệu quá khứ | Phiên 09/03 đã qua 7 tháng ✓; quy định ghi "tại thời điểm 10/2026" ✓. |
| Giọng tôn trọng | OK — L246 "Nhìn lại thì dễ nói vậy", L249 không chấm đúng sai; HỎI L225 được trả lời nghiêm túc. |
| RETENTION — lời hứa lộ trình | OK. Hình thức **"bản đồ bằng hình"** (L152 một câu + `timeline` đồng hồ phiên 8 mốc), khác video liền trước cùng kênh (D1: "thử đoán"); không dùng "trả lời ba câu hỏi" (A1, C1 đã dùng 2/5 video gần nhất — C2 không lặp) ✓. Ghi rõ ở mục Giữ chân ✓. |
| RETENTION — khác | ≥ 3 vòng mở, đóng đúng chỗ ✓; motif đồng hồ + hàng đợi giá sàn ≥ 3 lần ✓; cảnh mạnh ~75% (CH05) ✓. L294 liệt kê **4** mục ("giờ gom lệnh, giờ khớp liên tục, một khung giá mỗi ngày, và hai ngày chờ") > 3 — tuỳ chọn gộp "giờ gom lệnh và giờ khớp liên tục" thành "giờ gom lệnh, giờ khớp lệnh". Độ dài ~2.500 âm tiết < 6.800 của checklist — mục tiêu 11–12 phút đã ghi, chấp nhận theo khuôn kênh CK. |

## 3. TTS — chỗ dễ đọc sai

| Chỗ | Rủi ro | Gợi ý (chỉ trong bản gửi TTS) |
|---|---|---|
| "HOSE" (11 lần) | Đọc "hô-xe", "hốt", hoặc đánh vần | "hô-dê" như C1; giữ cố định. |
| "VN-Index" (L143, L241) | Gạch nối | Bảng `SAY` như C1. |
| "ATO", "ATC" (L187, L202, L234, L236) | "a-tô", "át-xê" | "a tê ô", "a tê xê"; nghe thử một câu. |
| "KRX" (L201) | "kờ-rếch" | "ca e ích" (hoặc "hệ thống K R X" đánh vần). |
| "HNX", "UPCoM" (L288) | "hách-nếch"; "úp-côm" lệch chữ hoa giữa | "hát en ích"; "úp-côm". |
| "T cộng hai", "T cộng không" (L255, L257, L263) | "T" đọc "ti" | "tê cộng hai". |
| "giá trần" vs "mức trần" (L268) | Người nghe lẫn nghĩa | Đã sửa L268 thành "tối đa". |
| Câu dài: L265 (40 âm tiết), L292 (38), L271 lời trích (36), L285 (36, có dấu câu), L152 (34) | Hụt hơi | L265, L292 đã tách trong bản sửa; L271 là nguyên văn luật — để giọng Xuân Vĩnh đọc chậm, chèn ngắt sau "chứng khoán". |
| "hai mươi nghìn không trăm năm mươi" (L213–214, L274) | Ổn | — |
| "‖", "HỎI:", "»" | Đọc ra thành tiếng | Lọc trước khi gửi TTS (Ghi chú đã nêu ✓). |
| Chữ số | Lời thoại CH00–CH06 không có chữ số nào (đã grep) ✓ | — |

## 4. Tính lại các số trong "Ghi chú"

| Mục Ghi chú | Kết quả tính lại / đối chiếu | Kết luận |
|---|---|---|
| VN-Index 06/03 → 09/03: 1.767,84 → 1.652,79 = −115,05, −6,51%; đáy 1.650,75 | −115,05; −6,508%; close − low = 2,04 | OK |
| Kỷ lục điểm; theo % xếp thứ 3 | Giảm điểm: −115,05 > −94,76 (20/10/2025) > −87,99 (03/04/2025); %: −6,677 (03/04/2025) > −6,674 (28/01/2021) > −6,508 (09/03/2026); chỉ 1 phiên < −100 điểm trong 1.995 phiên | OK |
| Độ rộng 09/03: 395 mã, giảm 368 · tăng 11 · đứng 16, trung vị −6,80%, 198 mã ≤ −6,8%, ngưỡng ≤ −6,45% ra 249 | Khớp từng số | OK |
| "Hơn một nửa" = 233/387 = 60,2% | 60,21% | OK |
| 10/03 +1,45%, 11/03 +3,08%, lấy lại 65,7%, 23/03 thấp hơn 61,62 | +1,448% · +3,078% · 65,67% · 61,62; 23/03 = đáy đóng cửa năm 2026 | OK |
| Giá trung vị HOSE ≤ 30/09: 15.400 (n = 406); 367 mã đúng 30/09: 14.200; 1 lô 1,54 triệu = 17% của 9,0 | 15,4 · 14,2 · 1.540.000 · 17,1% | OK (giá điều chỉnh) |
| Bước giá 126 · 234 · 46 | 126 · 234 · 46 | OK |
| Khung giá 21.400 / 18.600 | ✓ | OK |
| Ví dụ ATO 400 / 800 / 300 | ✓ (lũy kế mua 1.500/800/300; bán 400/1.000/1.800) | OK |
| Phí một lô: −8.000; −3.012,5; +1.975; hoà vốn 20.080 | 2.003.000 mua; bán 20.000 → 1.995.000; 20.050 → 1.999.987,5; 20.100 → 2.004.975; P = 2.003.000/(100 × 0,9975) = 20.080,2 | OK |
| Lịch T+2 tuần 09/03 | 05/03 thứ Năm → 09/03 thứ Hai; 06/03 thứ Sáu → 10/03 thứ Ba; bán 09/03 → 11/03 thứ Tư; 05–11/03 đều có phiên | OK |
| (Thêm) Thanh khoản 09/03 | 1,381 tỷ cp vs bình quân 01/01–06/03/2026 1,047 tỷ (trung vị 1,039) → +32%; cao thứ 5/186 phiên 2026 | Dùng cho sửa L224 |

**Ghi chú "Cần kiểm lại" — trả lời:** Quy chế gốc = **QĐ 22/QĐ-HĐTV (VNX) 18/04/2025**, hiệu lực từ ngày KRX vận hành (05/05/2025);
giờ cụ thể vẫn chỉ tài liệu thành viên · "Lần đầu > 100 điểm" chắc chắn đúng (lập luận biên độ, mục 1b L144) · 233 = HOSE ✓ · "dư bán
sàn hàng triệu" ✓ (TBTC nguyên văn "hàng loạt cổ phiếu dư bán sàn lên đến hàng triệu cổ phiếu") · bối cảnh Trung Đông/giá dầu ✓ (giữ) ·
TT 120 Điều 10 = "Giao dịch trong ngày" ✓ (giữ "quy định đã có chỗ") · "cơ quan soạn thảo" → nguồn gốc UBCKNN trên ssc.gov.vn ✓ ·
0,45% chưa thấy văn bản thay thế · cổ phiếu về trưa T+2 ✓ (dự thảo CCP vẫn 11:30 sáng T+2) · HNX/UPCoM vẫn SECONDARY · bài 3 ✓.

**Hồ sơ `2026-10-07-long-c2-research.md` cần sửa theo:** mục 1 dòng "Quy chế Sở" → QĐ 22/QĐ-HĐTV ngày 18/04/2025 (nâng nhãn mục 2.2,
2.3, 2.4 lô lẻ, 2.5 tham chiếu, 2.6 lên [bằng chứng]; giờ 2.1 giữ [thành viên]); mục 3 "Cách gọi dân gian T+2,5 là trước 2022" **sai
chiều**: trước 29/08/2022 cổ phiếu về chiều T+2 và phải chờ **sáng T+3** mới bán; từ 29/08/2022 bán được chiều T+2; mục 3 + 6: TT 145/2026
ký 30/09/2026 (9 chương, 65 điều), nguồn chinhphu.vn; trích UBCKNN ssc.gov.vn thay [14]; mục 6 thêm dòng **23/12/2026 → 28/12/2026:
cổ phiếu niêm yết HNX chuyển sang HOSE (TT 139/2025/TT-BTC)**; mục 2.5: KOSPI 09/03/2026 "−12,06%" (Stockbiz) mâu thuẫn báo quốc tế
(KOSPI có lúc −9%, kích hoạt ngắt mạch, đóng cửa khoảng −6% — tóm tắt kết quả tìm kiếm Caixin/NST, chưa mở bài) — không dùng là đúng.

## 5. Nguồn đã mở trong lần fact-check này

- **QĐ 22/QĐ-HĐTV ngày 18/04/2025 (VNX) — Quy chế Niêm yết và giao dịch chứng khoán niêm yết** (Điều 2, 13, 17, 20, 21, 24, 31, 32):
  https://luatvietnam.vn/chung-khoan/quyet-dinh-22-qd-hdtv-2025-ban-hanh-quy-che-niem-yet-va-giao-dich-chung-khoan-399805-d1.html ;
  trang VNX: https://vnx.vn/vi/van-ban-phap-ly/6 (thuvienphapluat 403)
- Tài liệu thành viên tóm tắt quy định HOSE 03/05/2025 [3] (đã trích văn bản PDF: giờ, giá khớp dự kiến ATO/ATC, LO hiệu lực tới hết
  ATC, ±20%, bước giá, lô lẻ, sửa/huỷ, T+2) — link trong hồ sơ
- Thông báo HOSE 13/03/2025 qua Vietstock: https://vietstock.vn/2025/03/hose-thong-tin-ve-quy-dinh-giao-dich-cua-he-thong-moi-143-1281145.htm
- **UBCKNN — Bản tổng hợp ý kiến, tiếp thu, giải trình dự thảo Thông tư thay thế TT 119/2020** (2026): https://ssc.gov.vn/cs/idcplg?IdcService=GET_FILE&allowInterrupt=1&dDocName=APPSSCGOVVN1620170388&dID=180856&filename=Ban+tiep+thu+giai+trinh+y+kien.pdf
- **TT 145/2026/TT-BTC** — chinhphu.vn: https://xaydungchinhsach.chinhphu.vn/mot-so-noi-dung-chinh-cua-thong-tu-145-2026-tt-btc-quy-dinh-hoat-dong-dang-ky-luu-ky-bu-tru-va-thanh-toan-giao-dich-chung-khoan-119261005165752419.htm
- Kinh tế Chứng khoán 19/08/2026 (câu "cơ quan soạn thảo… không đồng nghĩa"): https://kinhtechungkhoan.vn/ccp-du-kien-van-hanh-tu-quy-i2027-thi-truong-chung-khoan-chuan-bi-cho-co-che-moi ;
  Vietstock 03/06/2026 (Chủ tịch UBCKNN, CCP quý I/2027): https://vietstock.vn/2026/06/ubcknn-huong-toi-van-hanh-co-che-doi-tac-bu-tru-trung-tam-ccp-vao-quy-12027-830-1449894.htm
- TT 120/2020 Điều 10 (giao dịch trong ngày) — LSVN 15/02/2021: https://lsvn.vn/nguyen-tac-hoat-dong-giao-dich-chung-khoan-trong-ngay1613406397-a100508.html
- **Luật Thuế TNCN 109/2025/QH15** — bản .docx (Điều 13 khoản 2; Điều 29 khoản 1–2): https://hrspring.vn/wp-content/uploads/2026/07/109_2025_QH15_665870.docx
- TT 102/2021/TT-BTC (0,45%, thay TT 128/2018): https://luatvietnam.vn/chung-khoan/thong-tu-102-2021-tt-btc-213084-d1.html ; TT 83/2024 / 34/2026 / 125/2026
  chỉ áp cho VNX/VSDC: https://vanban.chinhphu.vn/?classid=1&docid=219289&orggroupid=4&pageid=27160
- VSD từ 29/08/2022 (11:00–11:30 T+2, bán chiều T+2): https://lsvn.vn/nha-dau-tu-duoc-ban-co-phieu-nhan-tien-som-hon-1-ngay1661739512-a123157.html ; [12]
- HNX → HOSE 28/12/2026 (TT 139/2025/TT-BTC) — Thời báo Tài chính 30/09/2026: https://thoibaotaichinhvietnam.vn/chot-thoi-diem-chuyen-toan-bo-co-phieu-niem-yet-ve-hose-204623.html
- Phiên 09/03/2026: Nhân Dân [8]; Thời báo Tài chính [11]; Mekong ASEAN [10] (link trong hồ sơ); bối cảnh quốc tế: https://www.caixinglobal.com/2026-03-09/asia-stocks-dive-as-oil-spikes-on-iran-crisis-102421276.html ;
  https://www.nst.com.my/amp/business/corporate/2026/03/1400466/asian-shares-plunge-iran-conflict-worsens (qua tóm tắt tìm kiếm)
- HNX ±10%, UPCoM ±15% [18, SECONDARY]

**Việc còn mở (không chặn bản 2):** văn bản hướng dẫn giao dịch của HOSE dưới KRX (số quyết định, có giờ giao dịch cụ thể) — hsx.vn
không trả nội dung, các nguồn tìm được chỉ ra QĐ 352/QĐ-SGDHCM (2021, trước KRX); trạng thái hiệu lực chính thức của TT 102/2021 trên
vbpl.vn (chưa thấy văn bản thay thế); HNX/UPCoM ±10/±15% từ quy chế gốc; việc bảng giá hiển thị "giá khớp dự kiến" trong ATO (nguồn
thành viên — kiểm bằng ảnh chụp bảng giá bất kỳ lúc 9:05); bài gốc Caixin/NST chưa mở trực tiếp.
