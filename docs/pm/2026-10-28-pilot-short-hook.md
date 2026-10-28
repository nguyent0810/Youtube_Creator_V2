# Báo cáo Short và brief pilot hook (bản 4, 28/10/2026)

**Nguồn số liệu:**
- YouTube Analytics API, 30/09 → 28/10. Analytics trễ khoảng 2 ngày.
- Chỉ tính Short đăng đến 26/10.
- **EVR (proxy)** = engaged-view ratio = engagedViews / views, lấy qua API. Đây **không** phải chỉ số "stayed to watch" (xem / lướt qua) của Studio. Chỉ dùng để tham khảo cho tới khi có số Studio.
- Số "xem / lướt qua" và "lượt hiển thị trên feed" chỉ có trong Studio. Ngày 28/10 Chrome bị treo (chụp màn hình quá thời gian, trang không tải phần biểu đồ) nên **chưa đọc được**. Các ô đó ghi "chưa có".

## 1. Năm Short "bảng tự dò" (22–23/10, đã qua 5–6 ngày)

Mốc so sánh đúng là các Short đăng cùng giai đoạn **21–25/10**, không phải trung vị cả tháng. Lý do ở mục 2.

| Short | View | So với trung vị 21–25/10 | Hiển thị trên feed | EVR (proxy) | % xem TB | Chia sẻ | Sub mới | View từ tìm kiếm |
|---|---|---|---|---|---|---|---|---|
| ck-bang-chia-luong-50-30-20 | 901 | **2,8×** (CK 322) | chưa có | 28% (CK 26%) | 86% (CK 48%) | 0 | 1 | 13 |
| ck-bang-de-danh-den-2030 | 572 | **1,8×** | chưa có | 22% | 90% | 0 | 0 | 30 |
| mim-bang-sinh-nam | 872 | **1,3×** (MIM 675) | chưa có | 42% (MIM 23%) | 75% (MIM 58%) | 0 | 1 | 20 |
| mim-bang-gpt4-thi | 246 | 0,4× | chưa có | 29% | 81% | 0 | 0 | 6 |
| mim-bang-nghe-ai | 180 | 0,3× | chưa có | 16% | 120% | 0 | 0 | 1 |

Đọc kết quả:
- **CK:** cả 2 bài cao hơn các Short cùng kỳ. % xem TB gần gấp đôi, nhưng EVR (proxy) không cao hơn.
- **MIM:** 1/3 bài cao hơn, 2/3 bài thấp hơn rõ.
- Bảng tự dò kéo được view từ tìm kiếm (6–30 view/bài, trong khi trung vị các Short khác khoảng 1 view).
- Không bài nào có chia sẻ. Sub mới 0–1/bài, bằng mức thường.
- Đây chỉ là **quan sát, không phải bằng chứng nhân quả**. Hai bài CK trùng chủ đề "chia lương / để dành", vốn được tìm kiếm nhiều. View cao có thể do chủ đề, do kiểu bảng, hoặc do phân phối từng ngày.
- **Bản 2 của brief viết "bảng tự dò không thắng" là sai**: bản đó so với trung vị cả tháng. Ở bản này đã sửa lại.

## 2. Baseline 28 ngày: trung vị từng KPI

| KPI | CK, cả kỳ (50 Short) | CK, 18–25/10 (23) | MIM, cả kỳ (72) | MIM, 18–25/10 (41) |
|---|---|---|---|---|
| View | 723 | **229** | 928 | **713** |
| Short ≥ 1.200 view | 9 | 0 | 18 | 1 |
| EVR (proxy) | 28% | 26% | 26% | 23% |
| % xem TB | 64% | 47% | 58% | 58% |
| Thời lượng xem TB | 18 s | 14 s | 15 s | 14 s |
| Chia sẻ / 1.000 view | 0,5 | 0 | 0,07 | 0 |
| Sub mới / 1.000 view | 0,70 | 0,79 | 0,58 | 0,66 |
| Like / 1.000 view | 5,1 | 4,6 | 9,3 | 9,8 |
| % view từ Shorts feed | 97% | 98% | 97% | 97% |
| Hiển thị trên feed, "xem / lướt qua" | chưa có | chưa có | chưa có | chưa có |

**Vách 18/10:**
- Short đăng từ 18/10 có view trung vị giảm mạnh: CK từ 1.129 xuống 230, MIM từ 1.215 xuống 722.
- EVR (proxy) chỉ giảm khoảng 5 điểm. Nhịp đăng không đổi (khoảng 3 Short/ngày).
- Chưa rõ nguyên nhân. Ba giả thuyết **chưa kiểm**:
  - kênh mới hết giai đoạn được thử phân phối;
  - đăng liền nhiều Short cùng một series;
  - thay đổi cách dựng.
- Pilot dùng mốc sau 18/10, không dùng mốc 1.100.

**Short → Long:** lượt xem Long đến từ link trong Short bằng **0** ở cả hai kênh, vì chưa Short nào gắn "Video liên quan".

## 3. Short dưới 300 view (CK 22 bài, MIM 11 bài)

| | CK | MIM |
|---|---|---|
| Nguồn traffic (tổng) | Shorts feed 3.262 · kênh 30 · tìm kiếm 30 · link ngoài 15 · trang khác 6 · subscriber 2 | Shorts feed 1.601 · tìm kiếm 44 · trang khác 10 · kênh 6 · link ngoài 3 |
| Tỉ lệ từ feed | 94–100% mỗi bài; riêng `ck-rut-truoc-han` 45% (11 view) | 92–100% mỗi bài; riêng `mim-skynet-1997` 12% (8 view) |
| Trạng thái (API) | 22/22 public, processed, không made-for-kids, embeddable | 11/11 như vậy |
| Hạn chế | **Chưa phát hiện hạn chế qua API** (không giới hạn vùng hay độ tuổi). Chưa kiểm mục Restrictions trong Studio. | như CK |
| EVR (proxy) trung vị | 26% (14–36%) | 18% (14–29%) |

- Phần lớn các bài này **vẫn được feed đưa ra**, nhưng người xem lướt qua.
- Hai bài có tỉ lệ feed thấp (`ck-rut-truoc-han`, `mim-skynet-1997`) cần xem trong Studio trước.
- Trong CK, 10 bài nợ/trả góp (18–19/10) có trung vị 135 view, các bài khác cùng kỳ 447. EVR (proxy) như nhau (26%). Mười bài này dồn trong 2 ngày, nên chưa tách được lý do là chủ đề hay việc dồn bài.

## 4. Short đang chờ lịch: 140 bài (28/10 → 04/12)

Mình chỉ kiểm tra, **không thay đổi bài nào**.

| | CK (20 bài, đến 06/11) | MIM (120 bài, đến 04/12) |
|---|---|---|
| Kiểu câu mở | 15/20 kiểu hook A (dữ kiện, con số hoặc nhận định bên ngoài); 5 bài mở bằng "bạn" | 115/120 kiểu hook A; 5 bài mở bằng "bạn" |
| Dồn series | E2 quỹ khẩn cấp 7 bài, C2 phiên giao dịch 7 bài trong 31/10–06/11 | AlphaGo/Lee Sedol khoảng 14 bài (28–30/10); ảo giác AI khoảng 14 (30/10–02/11); QWERTY 9 (02–04/11); Watson khoảng 14; poker khoảng 10 |
| Chồng lên pilot | Không: hàng chờ CK hết ngày 06/11 | 2 Short/ngày trong 13–18/11, xem mục 5 |

**Sửa lại về 5 cặp `-r2`: không có bài trùng nào sắp lên sóng.**
- Bản 3 đếm từ sổ nội bộ, mà sổ chưa ghi việc thay video. Mình đã kiểm trực tiếp trên YouTube ngày 28/10.
- 5 bản gốc đã ở trạng thái riêng tư, không hẹn giờ, tiêu đề "[CŨ - ĐÃ THAY] …" từ 22/10. Không bản nào bị xoá.
- 5 bản `-r2` là bản thay thế, chủ kênh đã duyệt ngày 22/10: dựng lại sau khi sửa nguồn theo hai đợt kiểm chứng KIEM-NGUON-A và KIEM-NGUON-B. Các bản này đang hẹn đúng giờ cũ.
- Như vậy đã đúng hướng "giữ bản hoàn thiện hơn" (`-r2`). Không cần thao tác thêm.

| Ngày | Bản giữ (hẹn giờ) | Bản đã ẩn (riêng tư, không xoá) |
|---|---|---|
| 13/11 | `mim-cuda-canh-bac-2006-r2` (4Fb-7CHpMr4) | y4Af8x1-LSA |
| 16/11 | `mim-watson-ferrucci-sai-gan-het-r2` (pMwawFykXpU) | RxDrSm0nkj8 |
| 18/11 | `mim-samsung-ba-vu-truoc-khi-cam-r2` (IF-x_Fbk17k) | ZcqUE9PihX8 |
| 19/11 | `mim-chat-da-xoa-van-bi-giu-r2` (eTbcxwb-Xt0) | bszzYgqkQjg |
| 22/11 | `mim-meta-ai-sua-xe-cong-khai-r2` (ChZS8JLCtdw) | EgfzETVH1ZE |

**Vai trò của hàng chờ trong pilot:**
- Hàng chờ chỉ là **baseline quan sát cùng kỳ**, không phải nhóm đối chứng thực nghiệm, vì chủ đề, lịch đăng và độ dài khác nhau.
- Nhóm đối chứng chính là 3 Short hook A trong mỗi pilot.
- Việc dồn series là một điểm cần điều tra riêng, mình chưa đổi gì.

## 5. Brief pilot: 6 chủ đề mỗi kênh, 3 cặp có đối chứng
: 6 chủ đề mỗi kênh, 3 cặp có đối chứng

**Biến duy nhất là 2 giây mở đầu:**
- **Hook A (đối chứng):** dữ kiện hoặc con số có ngày, về thế giới bên ngoài.
- **Hook B (mới):** tình huống của chính người xem, kèm một con số cụ thể, nói với "bạn".
- Cả hai đều cụ thể, không mở bằng câu hỏi trừu tượng.

**Giữ cố định:**
- thời lượng 25–35 s, chênh trong cặp ±3 s;
- giọng, look và mức nhạc theo chuẩn mix v3;
- câu kết quay về ý mở, không có khung bảng đứng yên;
- cùng khuôn tiêu đề;
- cùng giờ đăng;
- mỗi bài gắn "Video liên quan" tới Long của cặp, Long đó đã public.

Mỗi cặp có 2 chủ đề tương đương. Bài nào nhận hook A hay B đã chia trước theo bảng dưới, không chọn lại khi viết. Mọi con số trong hook phải có dòng trong factcheck.

### CK: 07–12/11, 1 bài/ngày, 19:00 VN (hàng chờ CK trống từ 07/11)

| Ngày | Cặp, Long được hỗ trợ | Chủ đề | Hook | Hướng câu mở |
|---|---|---|---|---|
| 07/11 | 1 · `mua-hay-thue` (public 30/10) | 5 năm tiền thuê nhà cộng lại | **B** | "Bạn trả sáu triệu tiền thuê mỗi tháng…" (VÍ DỤ GIẢ ĐỊNH) |
| 08/11 | 1 | tiền trả trước khi mua nhà | **A** | dữ kiện có ngày về giá căn hộ hoặc tỉ lệ vay (nguồn thống kê) |
| 09/11 | 2 · `mua-xe` (01/11) | chi phí nuôi xe mỗi tháng | **A** | dữ kiện có ngày về chi phí hoặc thuế phí xe |
| 10/11 | 2 | xe mất giá 3 năm đầu | **B** | "Chiếc xe bạn mua năm nay, ba năm nữa còn bao nhiêu…" (VÍ DỤ GIẢ ĐỊNH) |
| 11/11 | 3 · `fomo` (06/11) | mua sau khi giá đã tăng mạnh | **B** | "Bạn mua ngay sau một năm VN-Index tăng mạnh…" (biểu đồ thật, VÍ DỤ GIẢ ĐỊNH) |
| 12/11 | 3 | mua theo đám đông | **A** | dữ kiện có ngày: số tài khoản mở mới ở đỉnh thị trường |

Hook B rơi vào ngày 07, 10 và 11; hook A vào ngày 08, 09 và 12. Thứ tự này để xu hướng theo ngày không dồn về một phía.

### MIM: 13–18/11, 1 bài/ngày lúc 15:00 VN (08:00 UTC)

Đã kiểm lịch: mỗi ngày 13–18/11 hàng chờ có 2 Short, lúc 11:30 VN và 17:00 hoặc 19:00 VN. Thêm pilot thì mỗi ngày có 3 Short. Bài pilot cách bài hàng chờ gần nhất ít nhất 2 giờ, và cách các Long 20:00 VN (13, 15, 16, 18/11) 5 giờ.

| Ngày | Cặp, Long được hỗ trợ | Chủ đề | Hook | Hướng câu mở |
|---|---|---|---|---|
| 13/11 | 1 · `ai-voice` (public, 9,1 giờ xem) | giọng người nổi tiếng bị nhái để quảng cáo | **A** | vụ việc có ngày, có nguồn |
| 14/11 | 1 | tin nhắn thoại có thể bị dùng để nhái giọng | **B** | "Tin nhắn thoại bạn gửi hôm qua dài bao nhiêu giây…" |
| 15/11 | 2 · `ai-jobs` (public, 4,3 giờ xem) | một nghề văn phòng cụ thể trước AI | **B** | "Nếu bạn làm [nghề], mỗi ngày bạn…" (số có nguồn) |
| 16/11 | 2 | công việc nào AI đã thay | **A** | báo cáo có ngày (ILO/OECD) |
| 17/11 | 3 · `ai-feed` (public 30/10) | thuật toán chọn video | **A** | tài liệu hoặc phát biểu có ngày |
| 18/11 | 3 | vì sao feed của bạn khác của người bên cạnh | **B** | "Video bạn vừa lướt qua được chọn từ…" |

Chọn `ai-feed` và `ai-jobs` vì hàng chờ không có Short cùng chủ đề trong khung pilot. `ai-chat-privacy` và `ai-khuon-mat` đã có sẵn Short trong hàng chờ, nên không dùng.

## 6. Cách đọc kết quả (riêng từng kênh, ở mốc 48 h và 7 ngày sau bài cuối)

**Chỉ số chính:**
- Studio "xem / lướt qua" (stayed to watch) và lượt hiển thị trên feed.
- Khi chưa có số Studio, EVR (proxy) chỉ dùng để tham khảo. Không dùng một mình để kết luận thắng hay thua.

**Bước 0, kiểm tra phân phối trước khi đọc hook:**
- Bài nào có tỉ lệ view từ feed dưới 80%, hoặc Studio báo Restrictions: tách khỏi phép so sánh, ghi lại và kiểm phân phối.
- Nếu cả 6 bài đều thấp hơn baseline quan sát cùng kỳ: kết luận là **"chưa xác định nguyên nhân; cần kiểm tra phân phối và nội dung"**. Chưa phân biệt được do chủ đề, thời điểm, đối tượng xem hay phân phối.

**Phân loại tín hiệu cho hook B so với hook A:**

| Tín hiệu | Khi nào | Việc tiếp theo |
|---|---|---|
| **Tích cực** | Cả 3 cặp, B hơn A về "xem / lướt qua" ở Studio (hoặc EVR proxy khi chưa có Studio), chênh ≥ 5 điểm ở ít nhất 2 cặp; **và** không cặp nào có một bài B vượt nhờ một bài viral (view > 3× bài cùng cặp mà tỉ lệ xem không hơn); **và** sub / 1.000 view, lượt sang Long của nhóm B không thấp hơn nhóm A | Đề xuất vòng 2: thêm 3–4 cặp mới với chủ đề khác để kiểm lại. Chủ kênh duyệt riêng. **Không tự động** mở rộng sang 10–15 Short của lô Long. |
| **Chưa rõ** | Mọi trường hợp còn lại: lệch nhau giữa các cặp, chênh < 5 điểm, một bài bất thường quyết định kết quả, hoặc thiếu số Studio | Giữ nguyên cách làm hiện tại. Ghi lại cặp nào lệch và vì sao. Chủ kênh chọn chạy thêm cặp hay đổi hướng. |
| **Tiêu cực** | B thấp hơn A ở cả 3 cặp, hoặc ở 2 cặp với chênh ≥ 5 điểm | Không dùng hook B. Báo cáo lại để chủ kênh chọn biến thử tiếp theo. |

- Không dừng sớm. Chỉ dừng nếu có lỗi nội dung, vi phạm chính sách hoặc lỗi sản xuất nghiêm trọng.
- Mục tiêu pilot là biết hook cá nhân hoá có làm nhiều người **chọn xem** hơn không. Pilot không nhằm chứng minh công thức nào chắc chắn vượt 1.000 view.
- CK và MIM được đọc và quyết định riêng.

**Điều tra song song (không phải biến của pilot):**
- Vách 18/10: CK giảm khoảng 80%, MIM khoảng 41%.
- Cụm 10 bài nợ/trả góp của CK dồn trong 2 ngày, trung vị 135 view, trong khi EVR (proxy) như các bài khác.
- Khi Studio đọc được, so lượt hiển thị trên feed trước và sau 18/10, và của cụm nợ/trả góp, để tách yếu tố chủ đề khỏi yếu tố lịch đăng.

## 7. Quyết định của chủ kênh (28/10) và trạng thái

- **Lịch:** duyệt MIM 13–18/11, 1 Short pilot/ngày (đã kiểm giờ, xem mục 5). Lịch CK 07–12/11 giữ nguyên.
- **5 cặp `-r2`:** đã đối chiếu. Bản `-r2` là bản đã sửa nguồn, đang được hẹn giờ; bản gốc đã ẩn từ 22/10. Không cần thao tác thêm.
- **Studio** không chặn việc chuẩn bị. Khi Chrome hoạt động, đọc theo thứ tự:
  1. lượt hiển thị trên feed và "xem / lướt qua" của 5 bài bảng tự dò và 10 bài so sánh;
  2. tab Restrictions của các Short dưới 300 view, ưu tiên `ck-rut-truoc-han` và `mim-skynet-1997`.
  Số nào chưa lấy được thì ghi "chưa có", không suy diễn.
- **Đang làm:** script và factcheck Short mẫu CK 07/11 (hook B). Kiểm xong mới dựng. Không sản xuất hàng loạt, không đổi các Short khác trong hàng chờ.

## 8. Pilot CK đã đăng (28/10, riêng tư, hẹn 19:00 VN)

| Ngày | Cặp | Hook | Video | Long gắn "Video liên quan" |
|---|---|---|---|---|
| 07/11 | 1 | B | Td06vcpnEnQ | pXKfIo_nyVM |
| 08/11 | 1 | A | WCSoVk1wSOE | pXKfIo_nyVM |
| 09/11 | 2 | A | 0wfbPYvzL9g | Bx9w_a_1YOI |
| 10/11 | 2 | B | 8H2qOrgbvc8 | Bx9w_a_1YOI |
| 11/11 | 3 | B | pRPBbisoCL4 | ULLEUHkYz9g |
| 12/11 | 3 | A | FeUtqQtle5I | ULLEUHkYz9g |

**Thay video cùng ngày:**
- Retro phát hiện cả 3 bài B mở bằng clip toàn khung, còn 3 bài A mở bằng chữ trên nền tối.
- Theo duyệt của chủ kênh, 3 bài A đã được dựng lại (`-r2`) để 2 giây đầu cũng là clip toàn khung kèm con số lớn.
- 3 bản cũ (Ojbp75PBuew, MFWHpGh7TY0, aebGPJQcuS0) đã chuyển riêng tư, không hẹn giờ, tiêu đề "[CŨ - ĐÃ THAY]". Không bản nào bị xoá.

**Biến gây nhiễu còn lại**, phải ghi kèm khi đọc kết quả (chi tiết: `docs/pm/2026-10-28-retro-ck-pilot-short.md`):
- look khác nhau giữa các bài (tự xoay vòng);
- khuôn tiêu đề không đồng nhất;
- số cảnh trong cặp 2 chênh nhau 1;
- Long CK lên sóng 20:00 ngày 08/11 và 09/11 (đều là ngày hook A).

**Còn làm tay trước 07/11:** gắn "Video liên quan" trong Studio cho cả 6 bài (cần Chrome).
