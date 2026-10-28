# Kế hoạch Long CL theo khuôn "Ngoài Đời Thật" — 22/10/2026

Kênh: **Into the Killer's Mind (CL, Hình Sự)**, kênh dẫn đầu YPP từ 22/10. Tài liệu này chỉ là **kế hoạch chủ đề, gửi duyệt**. Chưa viết script, chưa dựng, chưa upload, không đụng `state.sqlite`.

Đầu vào:
- `docs/pm/2026-10-22-bao-cao-3-kenh.md`: số liệu Studio 28 ngày, 23/09–20/10.
- `data/long/golden` và `data/long/shanghai`: plan, script, spec.
- `motion/long/RETENTION.md`, `motion/long/RESEARCH-million-views.md`, `motion/long/build_long.py` (quy ước giấy phép).
- Memory: kế hoạch YPP, đổi lộ trình mở bài, clip sheet, mô tả không chứa ghi chú nội bộ.

Số liệu tự đo hôm nay (22/10):
- Wikipedia pageviews, Wikimedia REST API, người dùng thật, cùng kỳ 23/09–20/10/2026.
- Đếm bài Wikipedia EN có thật qua API (đã kiểm tồn tại; tên bài sai thì loại).
- Mẫu Commons: 30 kết quả đầu, phân loại giấy phép.
- YouTube: yt-dlp, chỉ đọc metadata, lấy view trọn đời của video có tiêu đề tiếng Việt. Kết quả tìm kiếm nhiễu nên chỉ dùng làm tín hiệu tương đối.
- File tạm nằm ngoài repo.

---

## 0. Khuôn thắng và điều rút ra

| Long CL | View 28 ngày | Xem TB | Giữ ở giây 30 | Vì sao |
|---|---|---|---|---|
| Tam Giác Vàng / Khun Sa | 4,3 nghìn | 10:38 (39,7%) | 72% | Tên địa danh quen + **một người thật** + con số ($2 triệu) + yếu tố gần người Việt trong 30 giây đầu |
| Bến Thượng Hải / Đỗ Nguyệt Sanh | 3,1 nghìn | 9:56 (31,4%) | 71% | Tên phim TVB huyền thoại + một ông trùm + cold open bữa tối 11/4/1927 |
| Yakuza | 917 | — | 78% | Chi tiết trái khoáy (phát cơm ở Kobe) |
| Mafia Ý | — | — | 67% | Dài 57 phút, quá dài |
| Hội Tam Hoàng | 171 | — | — | Trừu tượng: một tổ chức, không có một người |
| Jack the Ripper | 170 | — | — | Quá quen, và không có lời giải |

Quy tắc chọn chủ đề rút ra:
1. Tên phim/series/địa danh **khán giả Việt đã biết** đứng đầu tiêu đề.
2. **Một** nhân vật có thật làm xương sống, không chọn cả một tổ chức.
3. Có **một chi tiết lệch giữa phim và đời thật**, là thứ chỉ video này trả lời được.
4. Cold open là một cảnh có ngày giờ và có xung đột.
5. Dài 25–32 phút, 13–14 chương.
6. Tránh chủ đề không có lời giải hoặc đã bị kể quá nhiều mà không có góc mới.

---

## 1. Hiện trạng: Long CL nào đã có, lịch ra sao

**Long CL đã đăng.** Cả sáu Long trong `data/long/` đều đã công khai; các link chéo trong `spec.youtube.more` trỏ tới video thật:

| Slug | Link |
|---|---|
| golden (Tam Giác Vàng) | Long mới nhất. Script ngày 05/10, plan nói "Shanghai lên sóng tối nay" (≈04/10) |
| shanghai | u-JD1gbth1A |
| yakuza | uYuCapU-0hw |
| mafia | TGCwRhxQa6U |
| ripper | (không ghi link) |
| kowloon | sH9Zk4wsZCw |

Ngoài sáu video trên, kênh còn có các Long/video cũ làm từ trước: **Hội Tam Hoàng** (sv9N1EUsn5Q), **Tân Nghĩa An** (U4uOf2JmL94), **14K** (Mka1Ae68Rns).

**Không còn Long CL nào đang hẹn giờ trên máy này:**
- `state.sqlite` (mở mode=ro) chỉ có kênh **MIM và CK**. Bảng `item` và `upload_log` không có dòng nào của CL.
- `output/long/` không có thư mục CL.
- Báo cáo 22/10 ghi máy này không có credential API của CL.

**Nhịp Long CL hiện tại:**
- Đầu tháng 10 đăng dồn khoảng 6 Long trong khoảng hai tuần.
- Từ Tam Giác Vàng (≈06–08/10) tới nay **không có Long mới, khoảng 2 tuần trống**.
- → **Cần chủ kênh xác nhận trên Studio** rằng không có Long CL nào đang ở trạng thái lên lịch, trước khi chốt ngày.

**Short CL đã có** (`bundles/CL`, `data/stier/specs`, `data/packs/CL`), gồm 112 hồ sơ vụ án ngắn. Những Short liên quan trực tiếp tới kế hoạch:

| Short | Nội dung |
|---|---|
| `escobar5` | "Pablo Escobar: 5 sự thật, từ nhà tù tự xây tới 200 con hà mã" |
| `alcatraz` | Vụ vượt ngục 1962 |
| `valentine` | Thảm sát ngày Valentine 1929 |
| `al-capone-thue` | Al Capone ngồi tù vì tội gì |
| `elchapo` | El Chapo vượt ngục |
| `lustig`, `ponzi` | Lừa đảo |
| `petrosino` | Joe Petrosino |
| `yangnaiwu` | Án Dương Nãi Vũ |

**Quy ước ảnh của CL** (`build_long.py`):
- CL **nhận** PD, CC0, CC BY và **CC BY-SA**. Chỉ MIM và CK có cờ `no_sa`.
- Loại NC, ND và fair use.
- Không dùng ảnh từ phim, ảnh xác chết, ảnh nạn nhân, ảnh tra tấn. Đây là luật kênh, đồng thời tránh bị giới hạn quảng cáo.

---

## 2. Bảng 12 ứng viên (xếp hạng)

**Cách đọc cột:**
- **Wiki 28 ngày:** pageviews bài nhân vật / bài phim, EN và VI, kỳ 23/09–20/10/2026.
- **YT VN:** video tiếng Việt cùng chủ đề có nhiều view nhất, đo bằng yt-dlp. Là view trọn đời, chỉ là tín hiệu nhu cầu.
- **Nguồn EN:** số bài Wikipedia EN đã kiểm là có thật, trong danh sách nguồn dự kiến.
- **Ảnh:** mẫu Commons của tên nhân vật.

| # | Phim / địa danh → nhân vật | Wiki 28 ngày (EN / VI) | YT VN (tín hiệu) | Nguồn EN | Ảnh | Rủi ro | Trùng | Kết luận |
|---|---|---|---|---|---|---|---|---|
| 1 | **Narcos → Pablo Escobar** | 173.846 / 927; Narcos 35.313; Hacienda Nápoles 11.188 | Tài liệu 25 ph 980 nghìn, 22 ph 911 nghìn, 17 ph 469 nghìn | 20 | 16 PD, 12 BY-SA (Hacienda Nápoles nhiều BY-SA) | Bạo lực (đánh bom), người thân còn sống | Short `escobar5` (tốt cho phễu) | **CHỌN** |
| 2 | **Bao Thanh Thiên → Bao Chửng** | 3.931 / **3.955**; phim 1993: 1.421 / **2.507** | Tài liệu 11–23 ph: 1,87 triệu, 489 nghìn, 309 nghìn; "Phủ Khai Phong ngày nay" 2,69 triệu | 17 | Tranh/tượng PD, CC0; đền CC BY | Thấp; lệch "băng đảng" | Không | **CHỌN** |
| 3 | **Vô Gian Đạo / The Departed → Whitey Bulger** | 87.753; The Departed 164.095 / 394; Infernal Affairs 26.885 / 686 | Bulger tiếng Việt gần như trống; bản EN 1,2–3,3 triệu | 20 | Ảnh FBI PD (mugshot, vũ khí thu giữ) | Đồng phạm còn sống, đều đã bị kết án | Short `alcatraz` (Bulger từng ở Alcatraz) | **CHỌN** |
| 4 | **Peaky Blinders → Billy Kimber** | Băng 38.069 / 321; phim 130.417 / 982 | "Sự thật về Peaky Blinders" 11 ph 208 nghìn; recap 1,8–2,3 triệu | 15 | Ảnh cảnh sát 1904 (Harry Fowles) PD; Small Heath BY-SA | Nguồn mỏng (bài chính 10,9 nghìn ký tự) | Không | **CHỌN** |
| 5 | **Bố Già (The Godfather) → Frank Costello** | 54.630; The Godfather 171.024 / 1.098; Vito Corleone 29.163 / 370 | "Bố già" tiếng Việt bị phim Trấn Thành lấn át; Costello tiếng Việt 8 nghìn, EN 0,5–1,4 triệu | 18 | Ảnh phiên điều trần Kefauver PD (loại khoảng 10 ảnh NC/ND) | Nhầm với "Bố Già" Trấn Thành | Long Mafia Ý (Luciano), trùng thấp | **CHỌN** |
| 6 | **Bắt Tôi Nếu Có Thể → Frank Abagnale** | 82.692 / 329; phim 82.562 | Phê Phim phân tích phim 20 ph 955 nghìn | 18 | CC BY 2.0, CC BY-SA 4.0; Pan Am PD | **Người còn sống**, video nói câu chuyện của ông phần lớn là bịa | Short `lustig`, `ponzi` (cùng nhóm lừa đảo) | **CHỌN** |
| 7 | **Sự Im Lặng Của Bầy Cừu / Psycho → Ed Gein** | **596.974**; phim 187.867 / 3.734; Psycho 108.527 | Tài liệu 21–24 ph: 232 nghìn, 106 nghìn, 92 nghìn | 16 | PD 11 (chân dung, bia mộ, điều tra dân số 1930), BY-SA 14 | **Ghê rợn**: dễ bị giới hạn quảng cáo hoặc giới hạn tuổi | Không | **CHỌN có điều kiện** |
| 8 | Người Trong Giang Hồ / Ma Cao → Doãn Quốc Câu "Răng Gãy" | 4.772; 14K 9.062 | Phim Người Trong Giang Hồ 24,7 triệu; tài liệu 12–33 ph 51–80 nghìn | 15 | **Không có chân dung tự do** (kết quả Commons không liên quan) | Còn sống, bị Mỹ trừng phạt 12/2020 | Long 14K, Hội Tam Hoàng, Tam Giác Vàng | Dự bị |
| 9 | The Untouchables / Scarface → Al Capone | 152.522 / 735; phim 42.761 | BATTLECRY 31 ph 245 nghìn | 18 | Nhiều PD | Quá quen (giống bài học Ripper) | Short `al-capone-thue`, `valentine` | Dự bị |
| 10 | Griselda (Netflix) → Griselda Blanco | 43.572 / **50**; phim 10.701 | Tài liệu tiếng Việt thấp | 16 | 1 ảnh PD | Bạo lực | Gần Escobar | Loại đợt này (nhu cầu VN thấp) |
| 11 | The Irishman → Jimmy Hoffa | 119.347; phim 179.784 / **67** | Gần như không có tiếng Việt | 16 | Nhiều PD/CC0 | Thấp | Không | Loại (khán giả Việt không biết) |
| 12 | Truy Long / Trùm Hương Cảng → Ngô Tích Hào (Hào Què) | 1.015; Lôi Lạc 823 | Phim xã hội đen Hồng Kông hàng triệu | 16 | **Không có ảnh tự do của nhân vật** | Thấp | Kowloon | Loại (đã loại 04/10 vì cùng lý do) |

**Đã cân nhắc thêm và không đưa vào bảng:**

| Ứng viên | Lý do không đưa vào |
|---|---|
| American Gangster / Frank Lucas | Đã là vòng phụ ở chương 7 Long Tam Giác Vàng |
| Người Phán Xử / Năm Cam | Nhạy cảm trong nước, không có ảnh tự do, gia đình còn sống |
| Sói Già Phố Wall | Người còn sống, rủi ro pháp lý cao, xa ngách Hình Sự |

---

## 3. Bảy chủ đề chọn (chi tiết)

Ghi chú chung cho cả bảy bài:
- Ngày giờ và chi tiết dưới đây đã đọc thấy trong bài Wikipedia EN ghi kèm. Chỗ nào chưa kiểm được thì ghi **[kiểm khi viết]**.
- Mỗi bài dùng một dạng **lộ trình** khác nhau theo bảng ở `RETENTION.md`. Không dạng nào lặp ở hai bài liền nhau. Không bài nào dùng "trả lời ba câu hỏi".
- Hai Long gần nhất (Tam Giác Vàng, Bến Thượng Hải) đều dùng dạng **"Trong nửa giờ tới, bạn sẽ biết/gặp…" + liệt kê ba ý**, nên bài đầu đợt mới phải đổi hẳn dạng.

### 3.1 · Narcos → Pablo Escobar

**Tiêu đề mẫu**
- A: `NARCOS Ngoài Đời Thật: Pablo Escobar — Ông Trùm Tự Xây Nhà Tù Cho Chính Mình`
- B: `NARCOS Ngoài Đời Thật: Escobar Để Lại 4 Con Hà Mã — 30 Năm Sau Thành Hơn 160 Con`

**Nhân vật:** Pablo Escobar (1949–1993).

**Cold open (≈60 giây): ngày 22/7/1992, nhà tù La Catedral trên đồi phía trên Envigado, Medellín.**
- Chính phủ đưa quân tới để chuyển ông sang một nhà tù thường.
- Ông biết trước kế hoạch, và bước ra khỏi chính nhà tù ông tự xây.
- Cắt sang hôm nay: bốn con hà mã ông nhập về cho vườn thú riêng ở Hacienda Nápoles, đến năm 2023 đã thành 166 con. Năm 2022 Colombia xếp chúng vào loài xâm hại.
- Giờ cụ thể của cuộc trốn: [kiểm khi viết].

**Lộ trình, dạng "Lời thách":** "Thử đoán: nhà tù an ninh nhất Colombia năm 1991 do ai thiết kế? Giữ câu trả lời tới chương 6."

**Ba vòng mở**

| Vòng | Câu hỏi | Đóng ở |
|---|---|---|
| 1 | Vì sao chính phủ cho trùm ma túy tự xây nhà tù | Ch6: thỏa thuận không dẫn độ với Tổng thống Gaviria năm 1991 |
| 2 | Ai thật sự hạ Escobar: Search Bloc hay Los Pepes | Ch11: ngày 2/12/1993 |
| 3 | Bốn con hà mã đã thành gì | Ch13: số liệu 2022–2023 |

**Nguồn:** 20 bài EN đã kiểm.
- Pablo Escobar, Narcos, Medellín Cartel, Hacienda Nápoles, Cocaine hippos, La Catedral.
- Avianca Flight 203, DAS Building bombing, Palace of Justice siege.
- Los Pepes, Search Bloc, Luis Carlos Galán, Rodrigo Lara Bonilla.
- Carlos Lehder, Gonzalo Rodríguez Gacha, Roberto Escobar, Cali Cartel, Medellín, Comuna 13, Virginia Vallejo.
- Bài VI "Pablo Escobar" có tồn tại.

**Ảnh**
- PD: 16/30 file trong mẫu Commons; ảnh nào là ảnh căn cước hay ảnh Search Bloc thì [kiểm khi viết].
- BY-SA: Hacienda Nápoles, hà mã, La Catedral.
- **Không dùng** các ảnh "Death of Pablo Escobar" (PD nhưng là ảnh xác chết).

**Rủi ro**
- Đánh bom máy bay Avianca 203 năm 1989: kể bằng con số, không tả cảnh thi thể.
- Người còn sống (Roberto Escobar, Virginia Vallejo, con trai Juan Pablo/Sebastián Marroquín): chỉ nêu những gì nguồn ghi.
- Vụ Avianca và DAS: Wikipedia ghi Escobar *"believed to have orchestrated"* → lời đọc dùng "bị cho là đã ra lệnh".

**Nhu cầu:** cao nhất bảng (EN 173,8 nghìn; tài liệu tiếng Việt cùng độ dài gần 1 triệu view).

**Trùng:**
- Short `escobar5` đã dùng đúng hai chi tiết "nhà tù tự xây" và "hà mã". Đây là **lợi thế phễu**: gắn Short này làm Video liên quan.
- Long phải đi sâu hơn: thỏa thuận dẫn độ, Los Pepes.
- Short `escobar5` ghi "200 con", trong khi Wikipedia ghi 166 con (11/2023). Long dùng số có nguồn.

### 3.2 · Vô Gian Đạo / The Departed → Whitey Bulger

**Tiêu đề mẫu**
- A: `VÔ GIAN ĐẠO Ngoài Đời Thật: Whitey Bulger — Ông Trùm Làm Chỉ Điểm Cho FBI 20 Năm`
- B: `Ông Trùm Thật Đằng Sau VÔ GIAN ĐẠO Bản Mỹ: 16 Năm Trốn Truy Nã, Bị Bắt Năm 81 Tuổi`

**Nhân vật:** James "Whitey" Bulger (1929–2018).
- The Departed (2006) là bản làm lại của Vô Gian Đạo (2002, Lưu Đức Hoa, Lương Triều Vỹ).
- Theo Wikipedia, phim *"loosely based on"* Bulger và đặc vụ FBI John Connolly.
- Nhân vật trùm do Jack Nicholson đóng mang tên "Frank Costello", tức là cầu nối sang bài 3.4.

**Cold open: ngày 22/6/2011, một khu chung cư ở Santa Monica, California.**
- Một ông già 81 tuổi bị bắt cùng bạn gái Catherine Greig, sau 16 năm trốn và 12 năm nằm trong danh sách 10 kẻ bị FBI truy nã gắt gao nhất.
- Chi tiết tò mò: người FBI cần bắt nhất lại là người FBI đã che chở lâu nhất.
- Năm 1994, chính đặc vụ quản lý ông, John Connolly, báo cho ông chạy.
- Giờ bắt và cách FBI dụ ông ra ngoài: [kiểm khi viết]. Không có trong bài Wikipedia; cần nguồn công khai khác (FBI, báo Boston Globe đọc được).

**Lộ trình, dạng "Nghịch lý":** "Người FBI cần bắt nhất nước Mỹ lại là người FBI bảo vệ lâu nhất. Video này đi tìm chỗ hai điều ấy gặp nhau."

**Ba vòng mở**

| Vòng | Câu hỏi | Đóng ở |
|---|---|---|
| 1 | Vì sao FBI che cho ông | Ch5: làm chỉ điểm từ năm 1975, cung cấp tin về băng Patriarca |
| 2 | Ai báo cho ông chạy | Ch8: Connolly, 23/12/1994 |
| 3 | Kết cục | Ch13: bị đánh chết ở nhà tù Hazelton ngày 30/10/2018, vài giờ sau khi chuyển tới |

**Vòng phụ:** thời ở Alcatraz năm 1959, và việc bị cho thử LSD trong chương trình MKUltra.

**Nguồn:** 20 bài EN đã kiểm.
- Whitey Bulger, The Departed, Infernal Affairs, Winter Hill Gang, John Connolly (FBI agent).
- Stephen Flemmi, Kevin Weeks, John Martorano, Patriarca crime family, Gennaro Angiulo, William M. Bulger.
- Black Mass (film), FBI Ten Most Wanted Fugitives, Catherine Greig, South Boston.
- Alcatraz, Project MKUltra, USP Hazelton, Roger Wheeler.
- Bài VI có "Điệp vụ Boston" và "Vô gian đạo".

**Ảnh:** mẫu 30 kết quả có 27 PD (ảnh căn cước FBI 1953/1983, vũ khí thu giữ, ảnh Bộ Tư pháp Mỹ). Không dùng ảnh từ phim.

**Rủi ro**
- Connolly, Flemmi, Weeks, Martorano còn sống: chỉ nêu tội danh **đã bị kết án hoặc đã nhận**. Connolly bị kết án 2002 về tội gian lận có tổ chức (racketeering) và 2008 về tội giết người cấp độ hai.
- Bulger bị kết án năm 2013. Kể đúng con số bản án; các vụ án mạng chưa được chứng minh thì ghi "bị cáo buộc".

**Nhu cầu:** Wikipedia EN cao (Bulger 87,8 nghìn, The Departed 164 nghìn). Tiếng Việt về Bulger gần như **chưa có ai làm** → khoảng trống. Kéo khán giả qua tên Vô Gian Đạo, phim Hồng Kông khán giả Việt rất quen.

**Trùng:** thấp. Short `alcatraz` gắn làm Video liên quan.

### 3.3 · Bao Thanh Thiên → Bao Chửng (Bao Công)

**Tiêu đề mẫu**
- A: `BAO THANH THIÊN Ngoài Đời Thật: Bao Chửng — Chỉ Làm Phủ Doãn Khai Phong Hơn Một Năm`
- B: `BAO CÔNG Ngoài Đời Thật: Không Có Cẩu Đầu Trảm — Và 11 Chiếc Hộp Gỗ Năm 1973`

**Nhân vật:** Bao Chửng (999–1062), quan nhà Bắc Tống.

**Cold open: tháng 8/1973, Hợp Phì, giữa Cách mạng Văn hóa.**
- Hài cốt của Bao Chửng và gia quyến được khai quật, đựng trong **11 chiếc hộp gỗ**, chở về làng Đại Bao.
- Bí thư công xã không cho chôn và dọa hủy ngay.
- Rồi quay về chiếc cẩu đầu trảm mà khán giả Việt nhớ từ phim năm 1993: Wikipedia ghi bộ ba "long, hổ, cẩu đầu trảm" chỉ có **trong các bản dựng kịch**.
- Ngoài đời, ông làm phủ doãn Khai Phong từ **1057 đến 1058**.

**Lộ trình, dạng "Cảnh hẹn trước":** "Cuối video, mình sẽ quay lại với 11 chiếc hộp gỗ ấy, và bạn sẽ biết chúng dừng lại ở đâu."

**Ba vòng mở**

| Vòng | Câu hỏi | Đóng ở |
|---|---|---|
| 1 | Cẩu đầu trảm có thật không | Ch6: cái gì là lịch sử, cái gì là *Tam Hiệp Ngũ Nghĩa* |
| 2 | Hơn một năm ở Khai Phong ông làm gì mà thành huyền thoại | Ch8: mở cửa cho dân tự vào trình án, đàn hặc chú của sủng phi |
| 3 | 11 chiếc hộp gỗ | Ch13: số phận hài cốt và lăng mộ ngày nay |

**Nguồn:** 17 bài EN đã kiểm.
- Bao Zheng, Justice Bao (1993 TV series), Kaifeng, Song dynasty, Emperor Renzong of Song, Northern Song.
- The Seven Heroes and Five Gallants, Zhan Zhao, Gongsun Ce, Hefei, Imperial examination.
- Ouyang Xiu, Fan Zhongyan, Bianjing, Along the River During the Qingming Festival, Chen Shimei, Cases of Lord Bao.
- Bổ sung từ **zh.wikipedia** (包拯, 開封府) và bài VI "Bao Công".
- Ba tên bài EN không tồn tại (Kaifeng Fu, Bao Gong Temple, Lady Pang) → dùng bài zh.

**Ảnh**
- Tranh chân dung PD, tượng ở đền Bao Công (CC0).
- Đền và lăng ở Hợp Phì (CC BY 3.0).
- Tranh *Thanh Minh thượng hà đồ* (PD) dùng làm phông Biện Kinh.
- Không dùng ảnh phim.

**Rủi ro**
- Thấp: không bạo lực đồ họa, không người còn sống.
- Rủi ro nội dung: nguồn về thời Tống ít cảnh có ngày giờ, dễ khô. Cần dựng cảnh từ các vụ có ghi chép (vụ đàn hặc Trương Nghiêu Tá, chú của Trương quý phi [kiểm khi viết]).
- Lệch "Thế Giới Ngầm": đây là bài về **phá án và quan tòa**, vẫn đúng tên kênh Hình Sự. Đo riêng.

**Nhu cầu:** **cao nhất ở phía Việt Nam.**
- Pageviews VI của bài Bao Công (3.955) vượt cả bài EN.
- Bài phim 1993 tiếng Việt có 2.507 lượt.
- Tài liệu tiếng Việt 11–23 phút đạt 0,3–1,9 triệu view.

**Trùng:** không. Short `yangnaiwu` (án Dương Nãi Vũ đời Thanh) cùng nhóm "án xưa Trung Hoa", có thể gắn Video liên quan.

### 3.4 · Bố Già (The Godfather) → Frank Costello

**Tiêu đề mẫu**
- A: `BỐ GIÀ (The Godfather) Ngoài Đời Thật: Frank Costello — Ông Trùm Chỉ Cho Lên Sóng Đôi Bàn Tay`
- B: `BỐ GIÀ Ngoài Đời Thật: Phát Súng Năm 1957 Và Ông Trùm Nói "Tôi Không Nhận Ra Ai"`

Luôn ghi "The Godfather" trong ngoặc, vì tìm "bố già" ở Việt Nam ra phim của Trấn Thành.

**Nhân vật:** Frank Costello (1891–1973), "Thủ tướng của thế giới ngầm".
- Theo Wikipedia, Vito Corleone là nhân vật ghép từ Carlo Gambino, **Frank Costello**, Joe Bonanno và Joe Profaci.
- Chi tiết "Brando bắt chước giọng khàn của Costello" **không có** trong Wikipedia EN → không dùng, trừ khi tìm được nguồn công khai.

**Cold open: ngày 2/5/1957, sảnh tòa chung cư của Costello ở New York.**
- Vincent Gigante nổ súng; Costello bị thương nhưng sống.
- Người gác cửa nhận ra Gigante là kẻ bắn.
- Năm 1958, ra tòa, Costello khai ông **không nhận ra** kẻ tấn công. Gigante được tha bổng.
- Nối sang năm 1951, phiên điều trần Kefauver truyền hình trực tiếp toàn quốc: Costello không cho quay mặt, nên máy quay chỉ quay **đôi bàn tay bồn chồn** của ông.
- Giờ nổ súng và tên tòa nhà (The Majestic): [kiểm khi viết], không có trong bài Wikipedia.

**Lộ trình, dạng "Câu hỏi duy nhất":** "Một người gần như không bị kết án vì bạo lực, vì sao lại được gọi là ông trùm quyền lực nhất New York?"

**Ba mốc trả lời**

| Mốc | Nội dung | Đóng ở |
|---|---|---|
| 1 | Máy đánh bạc, Tammany Hall: quyền lực bằng quan hệ | Ch4 |
| 2 | Ai ra lệnh nổ súng | Ch9: Vito Genovese |
| 3 | Vito Corleone giống và khác ông ở đâu; vì sao *The Departed* đặt tên trùm là Frank Costello | Ch12 |

Mốc 3 nối với bài Bulger.

**Nguồn:** 18 bài EN đã kiểm.
- Frank Costello, The Godfather, Vito Corleone, Vincent Gigante, Lucky Luciano, Vito Genovese, Genovese crime family.
- Apalachin meeting, Kefauver Committee, Albert Anastasia, Meyer Lansky, Prohibition, The Commission, Five Families.
- Marlon Brando, Mario Puzo, Carlo Gambino, Joseph Valachi.

**Ảnh:** PD gồm "FrankCostello.jpg", "Frank Costello – Kefauver Committee" và loạt ảnh phiên điều trần (30/30 PD). **Loại** khoảng 10 file NC/ND trong mẫu.

**Rủi ro**
- Bạo lực mức trung bình.
- Không còn người sống liên quan trực tiếp.
- Sai lầm dễ mắc: nói Costello "là" Vito Corleone. Phải nói "một trong các nguyên mẫu".

**Nhu cầu:** Wikipedia EN tốt (Costello 54,6 nghìn, The Godfather 171 nghìn). Tiếng Việt về Costello **gần như trống** (8 nghìn view). Được kéo bởi tên phim Bố Già.

**Trùng:** Long Mafia Ý có dùng bài Lucky Luciano, nhưng bối cảnh là Sicily. Bài này là Mỹ, trùng thấp. Short `valentine` và `petrosino` gắn được.

### 3.5 · Peaky Blinders → Billy Kimber và băng Peaky Blinders thật

**Tiêu đề mẫu**
- A: `PEAKY BLINDERS Ngoài Đời Thật: Billy Kimber — Kẻ Đã Đánh Bại Băng Peaky Thật`
- B: `PEAKY BLINDERS Ngoài Đời Thật: Lưỡi Dao Lam Trong Mũ Là Chuyện Bịa`

**Nhân vật:** Billy Kimber (1882–1945), trùm Birmingham Boys. Ngoài ra có "Baby-faced" Harry Fowles, thành viên Peaky có ảnh căn cước cảnh sát năm 1904 (PD).

**Cold open: ngày 24/3/1890, tờ Birmingham Daily Post.**
- Tít báo kể một vụ đánh vỡ sọ ở Small Heath. Đây là lần đầu cái tên băng đảng này xuất hiện.
- Chi tiết tò mò: lưỡi dao lam khâu trong vành mũ, biểu tượng của phim, là **giải thích dân gian**. Dao cạo an toàn của Gillette chỉ có từ năm 1903 ở Mỹ.
- Băng Peaky thật bị Birmingham Boys của Kimber thay thế trước năm 1920.

**Lộ trình, dạng "Bản đồ bằng hình":** lời đọc chỉ một câu; màn hình hiện bản đồ Small Heath → Birmingham → các trường đua → Epsom → London, mỗi điểm là một chương.

**Ba vòng mở**

| Vòng | Câu hỏi | Đóng ở |
|---|---|---|
| 1 | Dao lam trong mũ có thật không | Ch3 |
| 2 | Ai hạ băng Peaky thật | Ch7: Birmingham Boys, thập niên 1910 |
| 3 | Cuộc chiến trường đua với băng Sabini kết thúc ra sao | Ch11: tháng 3/1921 phục kích ở Greenford, rồi trận "Epsom Road", 23 người bị giam |

**Nguồn:** 15 bài EN đã kiểm.
- Peaky Blinders, Peaky Blinders (TV series), Billy Kimber (gangster), Birmingham Boys, Charles Sabini, Darby Sabini.
- Small Heath, Birmingham, Epsom Derby, Bookmaker, Cillian Murphy, Steven Knight, Razor gang, Brummagem Boys, Bordesley.
- **Mỏng:** bài chính 10,9 nghìn ký tự, Birmingham Boys 4,3 nghìn ký tự. Cần thêm nguồn công khai mở được, ví dụ bảo tàng cảnh sát West Midlands hoặc bài BBC [kiểm khi viết].

**Ảnh**
- PD: ảnh căn cước cảnh sát Birmingham năm 1904 (Harry Fowles và các thành viên khác).
- BY-SA: Small Heath ngày nay.
- **Không dùng** ảnh cosplay hay ảnh diễn viên.

**Rủi ro**
- Thấp: bạo lực đường phố, không người còn sống.
- Rủi ro chính là **không đủ chất liệu cho 25 phút**. Nếu bản nghiên cứu dưới khoảng 4.500 âm tiết có nguồn thì rút xuống 20–22 phút, không độn.

**Nhu cầu:** phim (130 nghìn EN, 982 VI) và recap tiếng Việt rất mạnh (1,8–2,3 triệu view). Tài liệu "sự thật về Peaky Blinders" tiếng Việt mới ở mức 208 nghìn (11 phút), chưa có bản dài.

**Trùng:** không.

### 3.6 · Bắt Tôi Nếu Có Thể → Frank Abagnale

**Tiêu đề mẫu**
- A: `BẮT TÔI NẾU CÓ THỂ Ngoài Đời Thật: Frank Abagnale — Cú Lừa Lớn Nhất Có Thể Là Chính Câu Chuyện`
- B: `CATCH ME IF YOU CAN Ngoài Đời Thật: Phi Công Pan Am Giả… Hay Phạm Nhân Ở New York?`

**Nhân vật:** Frank Abagnale (sinh 1948, **còn sống**).

**Cold open: ngày 24/12/1968, cổng nhà tù Great Meadow, bang New York.**
- Abagnale ra tù.
- Theo hồ sơ, đây chính là những năm sách và phim nói cậu đang bay khắp thế giới trong bộ đồng phục phi công Pan Am.
- Rồi cắt sang năm 2002, ông nói với USA Today rằng mình "chỉ giả làm bác sĩ vài ngày" (diễn ý).
- Năm 2020, Alan C. Logan công bố điều tra dựa trên hồ sơ nhà tù và báo cũ.

**Lộ trình, dạng mới "Bảng kiểm chứng":**
- Mỗi chương đặt một lời kể của Abagnale lên màn hình, kết chương đóng dấu **CÓ HỒ SƠ / PHÓNG ĐẠI / KHÔNG CÓ HỒ SƠ**.
- Lời đọc chỉ hứa: "Đến cuối, bạn tự đếm xem có mấy con dấu đỏ."

**Ba vòng mở**

| Vòng | Câu hỏi | Đóng ở |
|---|---|---|
| 1 | Phi công Pan Am | Ch5 |
| 2 | Những năm 1965–1968 ông thật sự ở đâu | Ch8: Great Meadow |
| 3 | Vì sao một người như vậy vẫn được mời giảng về chống lừa đảo | Ch12 |

**Nguồn:** 18 bài EN đã kiểm.
- Frank Abagnale, Catch Me If You Can (phim, sách, nhạc kịch).
- Steven Spielberg, Leonardo DiCaprio, Tom Hanks, Pan Am, Check fraud, Impostor, Confidence trick, Joseph Shea, FBI.
- FCI Petersburg, Great Meadow Correctional Facility, The Tonight Show, To Tell the Truth, Ferdinand Waldo Demara.
- Cần thêm: tóm tắt công khai về sách của Logan (*The Greatest Hoax on Earth*, 2020) [kiểm khi viết].

**Ảnh**
- "Frank Abagnale.jpg" (CC BY 2.0), ảnh năm 2008 (CC BY-SA 4.0).
- Ảnh Pan Am và Boeing 707 thời 1960 (PD).
- Không dùng ảnh phim.

**Rủi ro: cao nhất về pháp lý trong 7 bài, vì nói về người còn sống.**
- Không tự khẳng định "ông nói dối".
- Luôn ghi nguồn:
  - "Theo điều tra của Alan Logan…"
  - "Wikipedia ghi tội có hồ sơ của ông chủ yếu là gian lận séc và trộm vặt."
  - "Chính ông năm 2002 thừa nhận đã phóng đại."
- Ghi phần trả lời hoặc phản bác của ông nếu nguồn có.

**Nhu cầu:** EN 82,7 nghìn. Tiếng Việt: Phê Phim phân tích phim đạt 955 nghìn view. Bài **không bạo lực**, hợp quảng cáo nhất trong đợt.

**Trùng:** không trùng Long. Short `lustig` và `ponzi` cùng nhóm lừa đảo, gắn Video liên quan.

### 3.7 · Sự Im Lặng Của Bầy Cừu / Psycho → Ed Gein (có điều kiện)

**Tiêu đề mẫu**
- A: `SỰ IM LẶNG CỦA BẦY CỪU Ngoài Đời Thật: Ed Gein — Một Người, Ba Ác Nhân Màn Ảnh`
- B: `PSYCHO Ngoài Đời Thật: Ed Gein Và Thị Trấn Plainfield Năm 1957`

**Nhân vật:** Ed Gein (1906–1984).

**Cold open: sáng ngày 16/11/1957, Plainfield, Wisconsin.**
- Bà Bernice Worden, chủ tiệm ngũ kim, biến mất.
- Khoảng 9 giờ 30, xe tải của tiệm được thấy chạy ra từ phía sau.
- Dừng ở cửa nhà Gein, **không** tả những gì bên trong.
- Rồi đưa lên ba tấm áp phích: Psycho (1960), Texas Chain Saw Massacre (1974), Sự Im Lặng Của Bầy Cừu (1991). Wikipedia ghi cả ba nhân vật Norman Bates, Leatherface và Buffalo Bill đều lấy cảm hứng từ ông.

**Lộ trình, dạng "Chặng đường" (đi ngược):** "Mình sẽ đi ngược ba chặng, từ màn ảnh Hollywood về một trang trại ở Wisconsin."

**Ba vòng mở**

| Vòng | Câu hỏi | Đóng ở |
|---|---|---|
| 1 | Vì sao một người có tới ba "phiên bản" trên phim | Ch9 |
| 2 | Vì sao 11 năm sau mới ra tòa | Ch10: năm 1957 bị kết luận không đủ năng lực hầu tòa, năm 1968 mới xử |
| 3 | Ông kết thúc ở đâu | Ch12: viện Mendota, mất năm 1984 |

**Nguồn:** 16 bài EN đã kiểm.
- Ed Gein, The Silence of the Lambs, Psycho (phim và tiểu thuyết), Robert Bloch, The Texas Chain Saw Massacre.
- Plainfield, Mendota Mental Health Institute, Bernice Worden, Mary Hogan, Waushara County.
- Buffalo Bill, Leatherface, Monster: The Ed Gein Story, Insanity defense, Alfred Hitchcock.

**Ảnh:** PD gồm chân dung "Ed-Gein.jpeg", tờ điều tra dân số 1930, bia mộ; Plainfield (BY-SA). **Cấm** ảnh hiện trường.

**Rủi ro: cao nhất về quảng cáo.**
- Chi tiết thi thể dễ khiến video bị giới hạn quảng cáo hoặc giới hạn tuổi.
- Script phải qua một vòng "lọc đồ họa": nói "đồ vật làm từ hài cốt" ở mức tối thiểu, không liệt kê.
- Thumbnail không có máu.
- Điều kiện để làm bài này: bài 3.1–3.3 đạt ≥ 1.000 view trong 7 ngày, và chủ kênh đồng ý chủ đề.

**Nhu cầu:** EN **597 nghìn** trong 28 ngày, cao nhất bảng (có thể do mùa Halloween hoặc phim Netflix). Tài liệu tiếng Việt 92–232 nghìn.

**Trùng:** không. Hợp đúng tên kênh *Into the Killer's Mind*.

### Dự bị (nếu một bài ở trên rớt khi nghiên cứu)

**R1. Người Trong Giang Hồ / Ma Cao → Doãn Quốc Câu "Răng Gãy".**
- Chi tiết tò mò: ông **tự đặt làm phim về đời mình** (*Hào Giang Phong Vân / Casino*, 1998, Nhậm Đạt Hoa đóng). Vài tháng sau ông bị bắt; năm 1999 bị kết án 15 năm.
- Rủi ro:
  - Còn sống.
  - Bị Bộ Tài chính Mỹ trừng phạt ngày 9/12/2020. Wikipedia ghi ông *"reportedly"* dính tới trung tâm lừa đảo ở Myanmar → lời đọc phải nói "bị cáo buộc", kèm việc ông phủ nhận nếu nguồn có.
  - **Không có chân dung tự do.**
- Chỉ làm nếu tìm được ảnh hợp lệ; nếu làm, nối được với Tam Giác Vàng.

**R2. The Untouchables → Al Capone.**
- Chi tiết tò mò: ngồi tù vì trốn thuế, 11 năm.
- Nhiều ảnh PD.
- Lo là chủ đề quá quen, giống bài học Ripper. Short `al-capone-thue` đã dùng chi tiết chính.

---

## 4. Lịch đăng đề xuất

**Nhịp: 2 Long CL/tuần, Thứ Ba và Thứ Sáu, 20:00 giờ Việt Nam.**

Lý do chọn nhịp 2 Long/tuần:
- Một Long kiểu Khun Sa mang về khoảng 4,3 nghìn × 10,6 phút ≈ **760 giờ xem**.
- Mốc 8.000 giờ cần khoảng 10 bài như vậy trong 12 tháng, cộng phần đuôi của các Long cũ.
- Nhịp dồn đầu tháng 10 (6 Long trong khoảng 2 tuần) rồi bỏ trống 2 tuần làm Long mới hết "tươi".
- 2 Long/tuần, mỗi bài cách nhau 3–4 ngày:
  - đủ thời gian đo 7 ngày bài trước trước khi khóa thumbnail bài sau;
  - vừa sức làm nghiên cứu, viết script, dựng và QA (không làm bản nháp, theo memory);
  - không đụng trần upload mỗi ngày của kênh.

Lý do chọn giờ:
- 20:00 là giờ Long của MIM.
- Short CL trước đây đăng 18:30 hoặc 21:30.
- **Cần chủ kênh xem Studio > Khán giả > "Khi người xem của bạn ở trên YouTube"** của CL rồi chốt giờ.

| Ngày (VN) | Long | Lộ trình | Ghi chú |
|---|---|---|---|
| **Thứ Sáu 30/10** | 3.1 Narcos → Escobar | Lời thách | Bài mở đợt, nhu cầu cao nhất. Trước đó phải sửa xong lỗi âm thanh "sẹt sẹt" (đề xuất #3 của báo cáo) |
| Thứ Ba 03/11 | 3.2 Vô Gian Đạo → Bulger | Nghịch lý | |
| Thứ Sáu 06/11 | 3.3 Bao Thanh Thiên → Bao Chửng | Cảnh hẹn trước | Bài thử ngoài "băng đảng" |
| Thứ Ba 10/11 | 3.4 Bố Già → Costello | Câu hỏi duy nhất | Cặp với Bulger (cái tên Frank Costello trong *The Departed*) |
| **Mốc kiểm 12/11** | — | — | Xem view 7 ngày và giữ chân giây 30 của 3.1–3.3. Bao Công dưới 1.000 view/7 ngày thì đợt sau bỏ nhóm "không băng đảng". Escobar hoặc Bulger dưới 1.000 thì xem lại thumbnail và tiêu đề trước khi đổi chủ đề |
| Thứ Sáu 13/11 | 3.5 Peaky Blinders → Kimber | Bản đồ bằng hình | Có thể rút xuống 20–22 phút |
| Thứ Ba 17/11 | 3.6 Bắt Tôi Nếu Có Thể → Abagnale | Bảng kiểm chứng | Cần duyệt pháp lý lời đọc |
| **Review 4 tuần 19/11** | — | — | Theo quyết định YPP số 4: nếu giờ xem không gấp đôi kỳ trước thì đổi cách chọn chủ đề |
| Thứ Sáu 20/11 | 3.7 Ed Gein, hoặc dự bị R1/R2 | Chặng đường | Chỉ làm khi qua điều kiện ở 3.7 |

**Quy trình mỗi bài** (theo memory):
1. Nghiên cứu, viết script, chủ kênh duyệt.
2. Dựng thẳng bản cuối.
3. Chạy `clip_sheet.py`, soát logo và chữ trong clip.
4. Quét mô tả tìm `<`, `>`, "CẦN", "WebFetch", "data/long". `sources` công khai chỉ chứa URL thật.
5. Upload private kèm hẹn giờ ngay khi dựng xong. Long đi trước Short.

Mỗi Long:
- thêm vào playlist "Thế Giới Ngầm Toàn Cầu" (Bao Công có thể vào một playlist riêng "Kỳ Án");
- gắn end screen trỏ sang Long kế tiếp trong cặp (Escobar → Bulger → Costello; Bao Công → Abagnale).

**Việc chặn:** máy này chưa có credential API của CL nên **không hẹn giờ tự động được**. Hoặc chủ kênh upload trên Studio, hoặc cấp OAuth cho CL trước 29/10.

---

## 5. Short nhử cho mỗi Long

Quy ước:
- 2–3 Short/Long, dài 25–45 giây, cắt từ chính các cảnh của Long.
- Đăng từ ngày Long công khai tới ngày +3.
- Gắn **Video liên quan** trỏ về Long. Long phải đã công khai thì mới gắn được, nên gắn ngay khi Long lên sóng.
- Câu cuối mỗi Short hỏi đúng vòng mở mà Long trả lời.
- Tiêu đề Short không lặp tiêu đề Long.

| Long | Short nhử (tiêu đề mẫu → vòng mở dẫn sang) | Short cũ gắn thêm |
|---|---|---|
| 3.1 Escobar | 1. "Chính phủ Colombia để trùm ma túy tự thiết kế nhà tù" → vòng 1<br>2. "Ngày 22/7/1992: ông trùm bước ra khỏi nhà tù của chính mình" → cold open<br>3. "Bốn con hà mã, ba mươi năm sau" → vòng 3 | `escobar5`, `elchapo` |
| 3.2 Bulger | 1. "Trùm Boston làm chỉ điểm cho FBI suốt 20 năm" → vòng 1<br>2. "Bắt năm 81 tuổi sau 16 năm trốn truy nã" → cold open<br>3. "Từ Alcatraz tới thí nghiệm LSD của CIA" → vòng phụ | `alcatraz` |
| 3.3 Bao Công | 1. "Cẩu đầu trảm của Bao Công có thật không?" → vòng 1<br>2. "Bao Công thật chỉ làm phủ doãn Khai Phong hơn một năm" → vòng 2<br>3. "11 chiếc hộp gỗ năm 1973" → vòng 3 | `yangnaiwu` |
| 3.4 Costello | 1. "Ông trùm chỉ cho truyền hình quay đôi bàn tay" → cold open<br>2. "Bị bắn vào đầu, ra tòa nói không nhận ra ai" → vòng 2<br>3. "Vì sao trùm trong Vô Gian Đạo bản Mỹ tên Frank Costello?" → vòng 3, nối sang Bulger | `valentine`, `petrosino` |
| 3.5 Peaky | 1. "Dao lam trong mũ Peaky Blinders là chuyện bịa" → vòng 1<br>2. "Băng Peaky thật bị ai đánh bại?" → vòng 2 | — |
| 3.6 Abagnale | 1. "Phim nói cậu đang lái máy bay. Hồ sơ nói cậu đang ở tù." → vòng 2<br>2. "Chính ông thừa nhận: bác sĩ vài ngày, không phải một năm" → vòng 1 | `lustig`, `ponzi` |
| 3.7 Gein | 1. "Một người, ba ác nhân trên màn ảnh" → vòng 1<br>2. "Vì sao 11 năm sau mới ra tòa?" → vòng 2 | — |

Tổng là 18 Short mới trong 3 tuần, khoảng 1 Short/ngày. Nhịp này nằm dưới mức 2–3 Short/ngày của quyết định YPP số 3, nên còn chỗ cho các Short CL khác.

---

## 6. Rủi ro tổng hợp

| Rủi ro | Bài | Cách xử lý |
|---|---|---|
| **Người còn sống bị nói là bịa chuyện** | 3.6 Abagnale | Chỉ nói qua nguồn: Logan 2020, Wikipedia, lời chính ông năm 2002. Không có câu khẳng định của kênh. Chủ kênh duyệt lời đọc |
| Ghê rợn → giới hạn quảng cáo hoặc giới hạn tuổi | 3.7 Gein, và một phần 3.1 Escobar | Lọc đồ họa, không ảnh hiện trường hay xác chết, thumbnail không máu |
| Tội danh chưa xử | 3.1 (Avianca), 3.2 (các vụ án mạng chưa chứng minh), R1 | Dùng "bị cho là", "bị cáo buộc"; chỉ nói chắc những tội đã bị kết án |
| Nhầm tên phim | 3.4 | Luôn ghi "(The Godfather)" |
| Nguồn mỏng | 3.5 Peaky, 3.3 Bao Công | Thêm nguồn zh/VI và nguồn công khai khác; được rút còn 20–22 phút, không độn |
| Lệch khán giả "Thế Giới Ngầm" | 3.3 Bao Công, 3.6 Abagnale | Mốc kiểm ngày 12/11 |
| Vận hành | Cả đợt | Chưa có credential CL; lỗi âm thanh "sẹt sẹt" chưa sửa; chưa xác nhận trên Studio là không có Long CL nào đang hẹn |

---

## 7. Cần chủ kênh duyệt

1. Danh sách 7 bài và thứ tự. Riêng 3.7 (Ed Gein) là có điều kiện.
2. Nhịp 2 Long/tuần, Thứ Ba và Thứ Sáu, 20:00; bài đầu Thứ Sáu 30/10.
3. Bao Công: thử chủ đề "quan tòa/kỳ án" ngoài nhóm băng đảng.
4. Abagnale: chấp nhận mức rủi ro pháp lý với cách nói qua nguồn.
5. Cách upload CL: qua Studio, hoặc cấp OAuth cho máy này.
