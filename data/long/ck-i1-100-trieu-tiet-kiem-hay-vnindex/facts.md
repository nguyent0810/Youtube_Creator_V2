# Kho dữ kiện R6 — 100 triệu: tiết kiệm hay VN-Index?

Ngày kiểm: 27/10/2026. Đây là kho nghiên cứu cho W1, không phải kịch bản hay khuyến nghị đầu tư. URL dưới đây đã mở trong phiên. Nhãn **mạnh** là nguồn cơ quan thống kê/chính phủ hoặc dữ liệu CSV mà ticket cấp; **vừa** là báo chí/dữ liệu tổng hợp.

## Phạm vi và phương pháp phải giữ nguyên

- CSV do ticket cấp: `data/ck/vnindex_1d_2016_2018.csv` (01/12/2016–05/10/2018) và `data/ck/vnindex_1d.csv` (08/10/2018–06/10/2026), giá đóng cửa từng phiên từ HOSE qua vnstock/VCI.
- VN-Index là chỉ số giá; nó không phải sản phẩm có thể mua trực tiếp và phép tính dưới đây **không cộng cổ tức**. Mô tả cách chỉ số phản ánh thay đổi vốn hóa của cổ phiếu niêm yết HOSE: https://support.vndirect.com.vn/hc/vi/articles/13971271685273-Ch%E1%BB%89-s%E1%BB%91-VN-INDEX-l%C3%A0-g%C3%AC (**vừa**).
- Khi mô phỏng bán, áp thuế chuyển nhượng chứng khoán cá nhân 0,1% trên giá chuyển nhượng; Thông tư 111/2013/TT-BTC: https://chinhphu.vn/default.aspx?docid=169566&pageid=27160 (**mạnh**). Chưa có bộ phí giao dịch thống nhất theo từng năm, nên W1 phải để phí giao dịch là biến/ghi rõ giả định, không tự coi bằng 0 mà không nói.
- Không nêu tên tổ chức nhận tiền gửi, quỹ hay mã chứng khoán; không suy kết lợi nhuận tương lai từ backtest này.

## Dữ kiện theo chương

### CH00 — Cú rơi từ đỉnh (4)

1. Ngày 09/04/2018, CSV ticket cấp ghi VN-Index đóng cửa **1.204,33 điểm**; đây là điểm vào của phương án bỏ một lần. **mạnh — dữ liệu ticket cấp;** phương pháp chỉ số: URL phạm vi ở trên.
2. Bình quân CPI năm 2018 tăng **3,54%** so với năm trước. https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2021/12/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-12-quy-iv-va-nam-2021/ (**mạnh**).
3. Đầu năm 2018, mức bình quân tiền gửi VND kỳ hạn trên 12 tháng được nêu khoảng **6,55%/năm** (2 tháng đầu năm); đây là điểm quan sát, **không phải bình quân cả năm**. https://cafef.vn/nhieu-ngan-hang-tang-lai-suat-huy-dong-2018030723375295.chn (**vừa**).
4. Câu hỏi của video là so sánh một khoản **100 triệu đồng** đặt vào ba luật chơi từ 04/2018; đó là **VÍ DỤ GIẢ ĐỊNH**, không phải lời khuyên. **mạnh — giả định biên tập.**

### CH01 — Ba luật chơi (4)

5. Phương án A: 100 triệu gửi kỳ hạn 12 tháng, tái tục hàng năm theo một chuỗi lãi suất được W1 chốt nguồn. Đây là **VÍ DỤ GIẢ ĐỊNH**; số dư cuối năm = số dư đầu năm × (1 + lãi suất năm). **mạnh — công thức.**
6. Phương án B: mua theo mức đóng cửa 09/04/2018, số đơn vị quy ước = 100.000.000 / 1.204,33; giá trị hàng ngày = số đơn vị × điểm đóng cửa. **VÍ DỤ GIẢ ĐỊNH; mạnh — công thức và CSV ticket cấp.**
7. Phương án C: chia 100 triệu thành **24** phần bằng nhau, mua tại phiên đầu tiên của từng tháng từ 04/2018 đến 03/2020. Đây là **VÍ DỤ GIẢ ĐỊNH** để so thời điểm mua, không phải lịch sử giao dịch của người thật. **mạnh — giả định.**
8. Thuế 0,1% tính trên giá chuyển nhượng, vì vậy chỉ trừ ở giá trị bán cuối kỳ trong phép tính B/C; nguồn Thông tư 111/2013/TT-BTC: https://chinhphu.vn/default.aspx?docid=169566&pageid=27160 (**mạnh**).

### CH02 — Đoạn tệ nhất (4)

9. CSV ticket cấp ghi ngày 24/03/2020 VN-Index đóng cửa **659,21 điểm**, là đáy giá đóng cửa sâu nhất của phương án B trong cửa sổ 09/04/2018–06/10/2026. **mạnh — TÍNH từ CSV.**
10. So với 1.204,33 điểm ngày vào, mức 659,21 điểm thấp hơn **45,26%**. Công thức: 659,21 / 1.204,33 − 1. **mạnh — TÍNH từ CSV.**
11. CPI bình quân năm 2020 tăng **3,23%**. https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2021/12/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-12-quy-iv-va-nam-2021/ (**mạnh**).
12. Trong năm 2020, bài báo ghi một nhóm lãi suất 12–24 tháng giảm từ **6,5% xuống 6,0%/năm**; đây chỉ là quan sát nhóm, không dùng thay bình quân năm. https://www.tinnhanhchungkhoan.vn/lai-suat-vao-dot-cat-giam-moi-post248257.html (**vừa**).

### CH03 — Phục hồi và CPI (4)

13. CPI bình quân năm 2021 tăng **1,84%**, thấp nhất kể từ 2016 theo Cục Thống kê. https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2022/01/kiem-soat-lam-phat-thap-thanh-cong-cua-nam-2021-va-ap-luc-trong-nam-2022/ (**mạnh**).
14. Tháng 7/2021, mặt bằng tiền gửi VND kỳ hạn 12–24 tháng được nêu là **5,4%–6,8%/năm**; đó là **khoảng**, không phải bình quân 12 tháng. https://www.div.gov.vn/lai-suat-cho-vay-giam-lai-suat-tien-gui-on-dinh (**vừa**).
15. CSV ticket cấp ghi phiên cuối năm 2021 có VN-Index **1.498,28 điểm**; so với cuối 2020 là 1.103,87 điểm. **mạnh — TÍNH từ CSV.**
16. Chỉ số giá không bao gồm cổ tức trong backtest này, nên đây là phép đo biến động giá, không phải tổng lợi nhuận của bất kỳ quỹ nào. Mô tả VN-Index theo vốn hóa: https://support.vndirect.com.vn/hc/vi/articles/13971271685273-Ch%E1%BB%89-s%E1%BB%91-VN-INDEX-l%C3%A0-g%C3%AC (**vừa**).

### CH04 — Đỉnh 2022, đáy 2022 (4)

17. CSV ticket cấp ghi ngày 06/01/2022 VN-Index đóng cửa **1.528,57 điểm**, là đỉnh giá đóng cửa trong dữ liệu. **mạnh — TÍNH từ CSV.**
18. CSV ticket cấp ghi ngày 15/11/2022 đóng cửa **911,90 điểm**, thấp hơn 40,35% so với 1.528,57 điểm. **mạnh — TÍNH từ CSV.**
19. CPI bình quân năm 2022 tăng **3,15%**. https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2022/12/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-12-quy-iv-va-nam-2022/ (**mạnh**).
20. Cuối 2022, một mức 12 tháng được báo chí ghi từ **5,6% lên 7,4%/năm** tại một số tổ chức; đó không đại diện toàn thị trường và không được dùng làm bình quân. https://znews.vn/bidv-vietinbank-va-agribank-tang-lai-suat-huy-dong-len-7-4-nam-post1369350.html (**vừa**).

### CH05 — Giai đoạn lãi suất thấp (4)

21. CPI bình quân năm 2023 tăng **3,25%**. https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2023/12/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-12-quy-iv-va-nam-2023/ (**mạnh**).
22. Đầu tháng 12/2023, lãi suất huy động bình quân kỳ hạn 12 tháng được một nguồn dữ liệu thị trường ghi **5,13%/năm**; đây là mốc quan sát tháng, không phải bình quân năm. https://tuoitre.vn/lai-suat-tiet-kiem-thap-ki-luc-nen-giam-hon-nua-thi-sao-20231206215733636.htm (**vừa**).
23. Ngày 15/01/2024, cùng loại bình quân 12 tháng được nêu **4,9%/năm**. https://tuoitre.vn/ha-them-lai-suat-binh-quan-tien-gui-12-thang-lap-day-moi-vua-xuong-dau-4-20240115180305495.htm (**vừa**).
24. CPI bình quân năm 2024 tăng **3,63%**. https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2025/01/chi-so-gia-tieu-dung-chi-so-gia-vang-va-chi-so-gia-do-la-my-thang-muoi-hai-quy-iv-va-nam-2024/ (**mạnh**).

### CH06 — Điểm dữ liệu mới (4)

25. CSV ticket cấp ghi 09/04/2025 VN-Index đóng cửa **1.094,30 điểm**. **mạnh — TÍNH từ CSV.**
26. CPI bình quân năm 2025 được Cục Thống kê công bố/ước tổng kết là **3,31%**. https://www.nso.gov.vn/tin-tuc-khac/2026/01/kinh-te-viet-nam-dat-duoc-nhung-ket-qua-quan-trong-toan-dien-nhieu-diem-sang-noi-bat/ (**mạnh**).
27. Tháng 12/2025, một bản tin thị trường nêu lãi suất huy động bình quân 12 tháng của nhóm tổ chức nhà nước ở **5,2%**; không dùng số này làm bình quân toàn hệ thống hay bình quân cả năm. https://finance.vietstock.vn/downloadedoc/18633 (**vừa**).
28. Bình quân 9 tháng 2026, CPI tăng **4,52%**; đây chưa phải CPI bình quân cả năm 2026. https://www.nso.gov.vn/tin-tuc-thong-ke/2026/10/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-chin-quy-iii-va-9-thang-nam-2026/ (**mạnh**).

## Mốc và kết quả tính sơ bộ từ CSV

| Mốc | Ngày | Đóng cửa VN-Index | Nguồn |
|---|---:|---:|---|
| Đỉnh vào tiền | 09/04/2018 | 1.204,33 | CSV ticket cấp |
| Đáy Covid | 24/03/2020 | 659,21 | CSV ticket cấp |
| Đỉnh dữ liệu | 06/01/2022 | 1.528,57 | CSV ticket cấp |
| Đáy 2022 | 15/11/2022 | 911,90 | CSV ticket cấp |
| Mốc 2025 | 09/04/2025 | 1.094,30 | CSV ticket cấp |
| Phiên cuối | 06/10/2026 | 1.759,08 | CSV ticket cấp |

**VÍ DỤ GIẢ ĐỊNH — chưa tính phí giao dịch; B/C chưa trừ thuế bán 0,1% trong số hiển thị:**

| Cách | Giá trị 06/10/2026 | Âm sâu nhất | Tháng dưới 100 triệu | Về lại 100 triệu |
|---|---:|---|---:|---|
| Bỏ một lần 09/04/2018 | 146,06 triệu | 24/03/2020: 54,74 triệu (−45,26%) | 60 | cần W1 xác nhận ngày hồi phục theo tiêu chí sau ngày mua |
| Mua đều 24 tháng (phiên đầu tháng 04/2018–03/2020) | 181,38 triệu | 24/03/2020: 67,97 triệu (−32,03%; sau khi đã góp đủ) | 10 | 18/11/2020 |
| Gửi 12 tháng cuốn chiếu | **chưa chốt** | không áp dụng nếu không tất toán trước hạn | 0 theo giả định gốc được bảo toàn | không áp dụng |

W1 phải chạy lại với (i) thuế bán 0,1%, (ii) phí giao dịch được nêu rõ hoặc làm hai kịch bản, và (iii) chuỗi **bình quân 12 tháng theo từng năm** có nguồn. Không được thay chuỗi đó bằng các mốc lãi suất đơn lẻ ở trên.

## Bộ số cho biểu đồ

1. **Đường đua chính** — `race`, triệu đồng; các điểm 04/2018, 03/2020, 01/2022, 11/2022, 04/2025, 10/2026; B/C từ CSV, A chờ chuỗi lãi suất chuẩn.
2. **VN-Index các mốc căng thẳng** — `line`; 1.204,33; 659,21; 1.528,57; 911,90; 1.094,30; 1.759,08 điểm; nguồn CSV ticket cấp.
3. **Mức giảm từ đỉnh vào tiền** — `waterfall`; 100 → 54,74 → 146,06 triệu, phương án B; VÍ DỤ GIẢ ĐỊNH, công thức theo CSV.
4. **Mua đều sau góp đủ** — `bars`; 100; 67,97; 100; 181,38 triệu; VÍ DỤ GIẢ ĐỊNH, theo CSV.
5. **CPI 2018–2026** — `line`; 3,54; 2,79; 3,23; 1,84; 3,15; 3,25; 3,63; 3,31; 4,52% (2026 là 9 tháng); nguồn URL Cục Thống kê ở trên.
6. **Lãi suất quan sát, không dùng thay bình quân năm** — `dots`; 6,55 (đầu 2018); 5,4–6,8 (07/2021); 5,13 (12/2023); 4,9 (15/01/2024); 5,2 (12/2025); %/năm, nguồn từng URL ở trên.
7. **Số tháng dưới 100 triệu** — `bars`; B: 60; C: 10 (chỉ tính từ lúc C góp đủ); A: 0 theo giả định gốc được bảo toàn; VÍ DỤ GIẢ ĐỊNH/TÍNH CSV.
8. **24 lần mua đều** — `heat`; mỗi ô 4,1667 triệu đồng trong 04/2018–03/2020; tổng 100 triệu; VÍ DỤ GIẢ ĐỊNH, công thức 100/24.
9. **Sức mua 100 triệu** — `counter`; chỉ số CPI lũy kế phải tính từ chuỗi 2018–2025 đã chốt; 2026 chưa dùng vì mới có 9 tháng. Công thức: tích (1+CPI năm); nguồn Cục Thống kê.

## Biểu đồ chính

`race` ba đường giá trị danh nghĩa, mốc đầu 100 triệu. CH00 thêm điểm 09/04/2018; CH02 thêm đáy 24/03/2020; CH03 thêm cuối 2021; CH04 thêm đỉnh 06/01 và đáy 15/11/2022; CH05 thêm cuối 2023/2024; CH06 thêm 09/04/2025; CH07 thêm 06/10/2026 và lớp ghi chú CPI. Đường tiết kiệm chỉ bật sau khi W1 chốt bộ lãi suất chuẩn.

## Cold open

1. “Ngày 9 tháng 4 năm 2018, 100 triệu đặt vào VN-Index ở 1.204 điểm. Chưa đầy hai năm sau, cùng phép tính còn khoảng 54,7 triệu. Nhưng đến phiên dữ liệu cuối, nó lại vượt 146 triệu. Nếu biết đoạn rơi ấy trước, bạn có chịu nổi để giữ không?” Biểu đồ race xuất hiện trước giây 15.
2. “100 triệu không đổi, nhưng một cách phải chịu 60 tháng dưới vốn; một cách mua dần chỉ có 10 tháng sau khi góp đủ. Con số cuối cùng có thể đẹp hơn, vậy vì sao đoạn đường lại quan trọng hơn kết quả?” Biểu đồ cột tháng âm xuất hiện trước giây 15.

## Tiêu đề và thumbnail

- `100 Triệu Từ 2018: Gửi Tiết Kiệm Hay Mua VN-Index?`
- `100 Triệu Đúng Đỉnh 2018: Giờ Còn Bao Nhiêu?`
- `100 Triệu Trong 8 Năm: Mua Một Lần Hay Mua Đều?`

1. Chữ lớn **100 TRIỆU → ?**, ba đường đua đơn giản; không ghi giả định.
2. Chữ lớn **ĐỈNH 2018**, một mũi tên rơi cạnh nhãn **TIẾT KIỆM**; không có logo/tên tổ chức.

## Clip Pexels ngang — ứng viên, phải soi lại trước dùng

| ID | Nội dung | Ghi chú |
|---:|---|---|
| 6963480 | tay bấm máy tính, sổ | 16:9; soi logo/chữ |
| 6780089 | tay và máy tính | 16:9; soi logo/chữ |
| 8195661 | người dùng máy tính | 16:9; soi logo/chữ |
| 6794227 | người trước laptop biểu đồ | 16:9; soi logo/chữ trên màn hình |
| 7593891 | tay, máy tính, ghi chú | cần xác nhận khung ngang trước tải |
| 6962707 | giấy tờ và máy tính | cần che/bỏ chữ đọc được |
| 7016911 | giao thông thành phố trên cao | 16:9; soi biển hiệu |
| 8342359 | viết sổ từ trên xuống | 16:9; soi chữ |
| 5212605 | viết sổ cạnh laptop | 16:9; soi logo/chữ |
| 7594719 | ghi chép ở bàn bếp | 16:9; soi logo/chữ |

Nguồn các ID: https://www.pexels.com/video/a-person-computing-using-calculator-6963480/ ; https://www.pexels.com/video/person-using-calculator-6780089/ ; https://www.pexels.com/video/a-man-using-the-calculator-8195661/ ; https://www.pexels.com/video/a-man-is-sitting-in-front-of-a-laptop-with-a-stock-market-chart-6794227/ ; https://www.pexels.com/video/close-up-video-of-a-person-using-calculator-7593891/ ; https://www.pexels.com/video/a-person-computing-using-calculator-6962707/ ; https://www.pexels.com/video/video-of-a-city-traffic-7016911/ ; https://www.pexels.com/video/girl-writing-in-notebook-8342359/ ; https://www.pexels.com/video/man-writing-on-his-notebook-5212605/ ; https://www.pexels.com/video/man-writing-in-notebook-7594719/ .

## Rủi ro và việc còn mở

- **Chưa kiểm được:** một chuỗi lãi suất **bình quân tiền gửi 12 tháng theo từng năm 2018–2026**. Các URL thu được mới là khoảng/mốc tháng hoặc nhóm tổ chức; không được gọi chúng là “bình quân năm”. Đây là blocker duy nhất để tính hợp lệ phương án A và giá trị thực sau CPI.
- 2026 mới có CPI bình quân 9 tháng 4,52%, chưa có số cả năm; không ghi nó là CPI bình quân năm.
- Không ai mua trực tiếp được VN-Index; mô phỏng là chỉ số giá, không có cổ tức, không phản ánh chênh lệch theo sản phẩm thực tế.
- Phí giao dịch, thời điểm khớp lệnh, chênh lệch giá và thuế làm kết quả thực tế khác mô phỏng. Không nói “nên mua/bán/gửi”.
