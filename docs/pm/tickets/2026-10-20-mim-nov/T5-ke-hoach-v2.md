# T5 v2 — 5 Short Watson/Jeopardy viết lại theo khung truyện có người (Long `mim-watson-jeopardy` lên 19/11/2026 20:00)

Người viết: agent T5 v2, 20/10/2026. Pha 1: chỉ viết file; không dựng, không đăng, không sửa `state.sqlite`, `data/stier/specs`, ticket khác. Spec ở `specs-v2-T5/` (5 file + `_selfcheck.py`). Bản đầu (`T5-ke-hoach.md`, `specs-T5/`) giữ nguyên, bị thay bằng bản này.

## 0. Kết luận ngắn

- **Đủ 5 bài, bài nào cũng có người thật có tên, sự kiện có ngày, bước ngoặt.** Chuẩn khung: bài mẫu `mim-nvidia-quan-an-dem` (câu mở là sự kiện có người, 9 cảnh, 30–35 s, câu cuối kết vòng về câu mở, không rào đón, không mẹo).
- **Đã đổi 4/5 góc so với bản đầu**, vì góc cũ thiếu người hoặc xung đột thật: "Jeopardy 1964 đáp án trước" (luật) thành chuyện Julann Griffin trên máy bay; "bốn năm Ferrucci" (cơ chế) thành bài thi thử 500 câu năm 2006 (15% so với 95%); "nhà hàng 2004" giữ nhưng viết thành truyện Lickel/Horn/Ferrucci có nguồn URL; "Watson không có tai" tìm được nguồn thật (Jennings sai, Watson đáp y hệt, Trebek nói "Ken vừa nói rồi"). Bỏ hẳn góc "Watson hàng trăm đáp án" (cơ chế đơn lẻ, không người). Thêm 1 góc mới (buổi đấu thử 13/01/2011).
- Tự kiểm bằng `mix_lint` (import từ `build.py`, không chạy build): 5/5 đạt (xem mục 5).
- Mọi số nguồn từ Wikipedia (IBM Watson, Merv Griffin, Jeopardy!) + AP (abc7) + `script.md`; **không có `factcheck.md`** cho Long này, các chỗ chưa kiểm ghi ở mục 4.

## 1. Lịch (từ `00-LICH-XEN-KE.md`, các dòng "T5 watson")

| Ngày | Giờ | Slug | Nhân vật | Nhãn |
|---|---|---|---|---|
| T7 14/11 | 19:00 | `mim-watson-lickel-nha-hang-im-lang` | Charles Lickel, Paul Horn, David Ferrucci | SỰ KIỆN (2004–2005, theo lời kể) |
| CN 15/11 | 19:00 | `mim-watson-khong-co-tai-oreo` | Ken Jennings, Alex Trebek | SỰ KIỆN (14/02/2011) |
| T2 16/11 | 17:00 (Long 20:00 là của T4) | `mim-watson-ferrucci-sai-gan-het` | David Ferrucci | SỐ (2006: 15% so với 95%) |
| T6 20/11 | 11:30 (sau Long) | `mim-watson-buoi-tap-kem-mot-nghin-do` | Jennings, Rutter | SỐ/SỰ KIỆN (13/01/2011) |
| CN 22/11 | 11:30 (sau Long) | `mim-jeopardy-julann-tren-may-bay` | Julann và Merv Griffin | SỰ KIỆN (30/03/1964) |

Giờ chỉ là gợi ý, chốt bằng `scripts/shorts_grid.py` ở pha 2. Ba bài trước Long (14–16/11) là phễu; hai bài sau (20, 22/11) nối bằng "Video liên quan". Mỗi chủ đề tối đa 1 bài/ngày; hai bài kề nhau trong bảng lịch khác chủ đề (đúng theo `00-LICH-XEN-KE.md`). Dải cảnh (M ảnh/clip, D số liệu, G sơ đồ, T chữ): A `MDMDGMGTM`, C `MDGTDTMGM`, B `MDDGMMDTD`, E `MDTDDMGMT`, F `MGTDMDTDM`: không bài kề nhau trùng khuôn.

## 2. Từng bài

Quy ước chung: theme `mim`, `mix: true`, `rules: 2`, `kicker` "TRẬN ĐẤU NGƯỜI – MÁY", lời đọc không chữ số (số bằng chữ; số chỉ hiện trên màn hình), mô tả có dòng "Bản đầy đủ: https://youtu.be/Mt5hYcQxH50 (công khai từ 20:00 ngày 19/11)", không mời xem Long trong lời đọc, không câu hỏi cuối.

### A · `mim-watson-lickel-nha-hang-im-lang` (14/11 19:00, ~31 s, 9 cảnh)
- **Câu mở (9 chữ):** "Cả nhà hàng bỏ bữa chạy ra xem tivi."
- **Nhân vật:** Charles Lickel (quản lý nghiên cứu IBM), Ken Jennings (trên tivi), Paul Horn (lãnh đạo nghiên cứu), David Ferrucci.
- **Sự kiện có ngày:** 2004 bữa tối, cả nhà hàng nín lặng xem Jennings giữa chuỗi 74 ván; 2005 Horn ủng hộ; không ai muốn nhận vì khó hơn cờ vua "không lời"; cuối cùng Ferrucci nhận lời. Lời đọc mở bằng "Theo lời kể".
- **Bước ngoặt:** "Cuối cùng, David Ferrucci nhận lời."
- **Câu cuối (kết vòng):** "Từ một nhà hàng im lặng, IBM có đề bài mới sau cờ vua."
- **Số + nguồn:** 2004, 74 ván, 2005, Horn khó tìm người nhận: Wikipedia *IBM Watson* mục Development (dẫn Baker, *Final Jeopardy*, 2011, tr. 6–8); kể lại thêm ở TechRepublic (URL trong spec); script CH01.
- **Không trùng:** `mim-jennings-74-van` nói đường đời Jennings (kỷ lục, thua, thành người dẫn), không nhắc nhà hàng/Lickel/Horn. Chỉ trùng nền "74 ván" (một con số nền, không phải góc).

### C · `mim-watson-khong-co-tai-oreo` (15/11 19:00, ~30 s, 9 cảnh)
- **Câu mở (9 chữ):** "Ken Jennings đáp sai, và Watson đáp y hệt."
- **Nhân vật:** Ken Jennings, Alex Trebek, Watson.
- **Sự kiện có ngày:** 14/02/2011, trận đầu lên sóng; gợi ý về bánh Oreo; Jennings đáp "những năm hai mươi" (sai), Watson bấm chuông và đáp lại đúng câu ấy; Trebek: "Không. Ken vừa nói rồi!" (AP, trích dịch).
- **Bước ngoặt:** Watson không nghe được câu trả lời của người chơi khác (nhận gợi ý bằng chữ).
- **Câu cuối:** "Cỗ máy thắng cuộc thi ấy, nhưng không nghe nổi câu vừa vang lên." (kết vòng "đáp y hệt".)
- **Nguồn:** abc7/AP (https://abc7.com/archive/7958839: Oreo, "What is 1920s?", "No. Ken said that!"), Wikipedia *IBM Watson* (mục First match), script CH08.
- **Không trùng:** `mim-watson-tieng-chuong` nói luật bấm chuông/cánh tay cơ khí; bài này là Watson không có tai, không nhắc chuông-như-luật. Có "bấm chuông" một lần như động từ chỉ hành động.

### B · `mim-watson-ferrucci-sai-gan-het` (16/11 17:00, ~30 s, 9 cảnh)
- **Câu mở (8 chữ):** "Năm trăm câu thử, Watson sai gần hết."
- **Nhân vật:** David Ferrucci và nhóm.
- **Sự kiện có ngày:** 2006 thi thử 500 câu cũ của Jeopardy: đúng khoảng 15%, người giỏi nhất đúng tới 95% và bấm chuông nhanh gấp đôi; 2007 được giao 3–5 năm và 15 người; 2008 đấu được nhà vô địch; 02/2010 thắng người chơi thường xuyên.
- **Bước ngoặt:** từ sai gần hết tới thắng người, khoảng bốn năm (kênh tự tính: 2010 trừ 2006).
- **Câu cuối:** "Từ sai gần hết tới thắng người, mất khoảng bốn năm."
- **Nguồn:** Wikipedia *IBM Watson* mục Development (dẫn NYT Magazine 06/2010); script CH05 chỉ có "chơi tệ", không có 15%/95%.
- **Không trùng:** `mim-watson-90-may-chu` nói phần cứng và tên Thomas Watson; bài này là kết quả thi thử và con người. Không nhắc 90 máy, 2.880 lõi, 200 triệu trang. Nhẹ chạm A (cùng nhắc Ferrucci nhận việc) nhưng A kết ở "nhận lời", B bắt đầu từ bài thi thử.

### E · `mim-watson-buoi-tap-kem-mot-nghin-do` (20/11 11:30, ~29 s, 9 cảnh)
- **Câu mở (8 chữ):** "Ken Jennings chỉ kém Watson một nghìn đô."
- **Nhân vật:** Jennings, Brad Rutter, Watson.
- **Sự kiện có ngày:** 13/01/2011 đấu thử trước báo giới, lần công khai đầu tiên; 15 câu; Watson 4.400, Jennings 3.400, Rutter 1.200 đô; không ai sai; hôm sau ghi hình trận thật, giữ kín tới tháng hai.
- **Bước ngoặt:** "khi lên sóng, khoảng cách ấy không còn nhỏ như thế" (thật: 77.147 so với 24.000, gấp hơn ba lần).
- **Câu cuối (kết vòng):** "Nhưng khi lên sóng, khoảng cách ấy không còn nhỏ như thế."
- **Nguồn:** Wikipedia *IBM Watson* (mục Practice match, dẫn ZDNet 13/01/2011); bản tin cùng ngày (Salon, qua tóm tắt tìm kiếm) khớp 4.400/3.400/1.200.
- **Không trùng:** `mim-watson-77-nghin-do` dùng 77.147/24.000/21.600 của trận thật; bài này là buổi tập trước đó, con số khác; tên Rutter xuất hiện ở bảng điểm.

### F · `mim-jeopardy-julann-tren-may-bay` (22/11 11:30, ~34 s, 9 cảnh)
- **Câu mở (8 chữ):** "Trên máy bay, một người vợ ra đề."
- **Nhân vật:** Julann Griffin, Merv Griffin (người dẫn chương trình), Art Fleming (người dẫn đầu tiên).
- **Sự kiện có ngày:** chuyến bay Duluth về New York (không ghi năm); bà nói sao không đưa đáp án trước; đọc thử "5.280", câu hỏi "một dặm dài bao nhiêu feet"; NBC mua không cần xem bản chạy thử; lên sóng 30/03/1964, tên đầu "What's the Question?".
- **Bước ngoặt:** NBC mua ngay; kết nối Watson: 47 năm sau câu đố ấy thành đề thi của một cỗ máy (kênh tự tính: 2011 trừ 1964).
- **Câu cuối:** "Bốn mươi bảy năm sau, câu đố trên máy bay ấy trở thành đề thi của một cỗ máy."
- **Nguồn:** Wikipedia *Merv Griffin* (đoạn Griffin kể với AP), Wikipedia *Jeopardy!* (ngày 30/03/1964).
- **Không trùng:** MIM chưa có Short nào về nguồn gốc Jeopardy; `mim-con-ngua-da-con-ngua-da` là nghĩa mơ hồ tiếng Việt. Khác bản đầu (luật chơi + ví dụ Paris): đây là chuyện có người.

## 3. Bảng đối chiếu trùng

### 3a. Short MIM trong `state.sqlite` (mở mode=ro, kind='short', channel='MIM': 160 bài, 20/10)

Quét từ khoá watson/jeopardy/jennings/ibm/ferrucci/merv/griffin/trebek/đố vui/nhà hàng trên slug + quét nội dung `data/stier/specs/mim-*.json` (Lickel, Julann, Griffin, Eyser, Oreo, Fleming, Horn, "nhà hàng", "không nghe": không trúng). Còn đúng 12 slug Watson/Jeopardy; không bài nào cùng góc:

| Slug đã có | Góc đã có | Bài v2 gần nhất | Khác ở đâu |
|---|---|---|---|
| mim-watson-toronto | Toronto, cược 947 | C, E | không nhắc Toronto/cược |
| mim-watson-nguong-50 | ngưỡng 50% | B | B nói bài thi thử 2006, không ngưỡng/thanh tự tin |
| mim-watson-90-may-chu | 90 máy chủ, 2.880 lõi | B | không dùng phần cứng |
| mim-jennings-74-van | đời Jennings | A, C | A là Lickel; C là phiên trận 14/02 |
| mim-watson-77-nghin-do | 77.147/24.000/21.600 | E | E là buổi tập 13/01, số khác |
| mim-rush-holt-thang-watson | Washington 28/02 | không | |
| mim-watson-62-trieu-do, -ca-benh-gia-dinh, -health-ban-2022, mim-project-debater-79-62 | y tế, tranh biện | không | |
| mim-watson-tieng-chuong | luật bấm chuông | C | C là "không có tai" |
| mim-con-ngua-da-con-ngua-da | nghĩa mơ hồ | F | F là nguồn gốc luật đảo |

### 3b. Ticket T4, T6–T9 (đã có `T4/T6/T7/T8/T9-ke-hoach.md` và specs-T4…T9)
Quét "watson/jeopardy/jennings/ferrucci/griffin/lickel/trebek" trong các `T*-ke-hoach.md` và `specs-T4…T9/*.json`: chỉ có nhắc tên slug Watson cũ (T4 `mim-watson-90-may-chu`, T9 `mim-watson-tieng-chuong`). Không bài nào dùng góc A–F. T7 (poker) cùng series Người–Máy nhưng không nhắc Jeopardy.

## 4. Cần kiểm trước khi dựng (pha 2)

1. **Không có `factcheck.md`** cho `mim-watson-jeopardy`. Con số mới (15%, 95%, 500 câu, 3–5 năm, 15 người, 4.400/3.400/1.200, 5.280, 30/03/1964) **không có trong script**; nguồn là Wikipedia + AP. Nên bổ sung vào factcheck của Long.
2. **A (Lickel):** Wikipedia và TechRepublic kể khác nhau về tên nhà hàng và độ dài chuỗi thắng (74 ván so với "75 ngày"); lời đọc ghi "theo lời kể" và không nêu tên nhà hàng. TechRepublic chưa mở được bản đầy đủ (chỉ qua tóm tắt tìm kiếm); nên đối chiếu NYT Magazine (Clive Thompson, 06/2010) hoặc *Final Jeopardy* của Baker.
3. **C (Oreo):** AP qua abc7 xác nhận Oreo, "What is 1920s?", "No. Ken said that!". Tên mục "Name That Decade" và lời giải thích của IBM chỉ thấy qua tóm tắt tìm kiếm, **không đưa vào lời đọc**. Lời trích Trebek dịch từ AP, hiện thành `quote` với "TRÍCH DỊCH".
4. **B:** 15%, 95%, "nhanh gấp đôi", 3–5 năm, 15 người chỉ từ Wikipedia (dẫn NYT Magazine, chưa mở được). "Bốn năm" là kênh tự tính (02/2010 trừ 2006; tháng của bài thi thử 2006 không rõ).
5. **E:** 4.400/3.400/1.200 có 2 nguồn (Wikipedia + bản tin); chi tiết "Jennings và Watson hoà trước câu cuối 1.000 đô" chỉ có Wikipedia (dẫn ZDNet, chưa mở được) nên **không đưa vào lời đọc**; câu mở dùng "kém một nghìn đô" (có 2 nguồn). Địa điểm (Yorktown Heights) cũng chưa kiểm, không dùng.
6. **F:** lời Griffin là qua AP, đăng lại ở Wikipedia; năm chuyến bay không rõ (nguồn khác ghi 1963), **không đưa năm vào lời đọc**. Cảnh `quote` là trích dịch lời AP. Nên đối chiếu bản gốc AP hoặc sách của Griffin.
7. **Clip (chưa soi hình, chỉ chọn theo tiêu đề index; BẮT BUỘC chạy `motion/long/clip_sheet.py` trước khi dựng):** A `38406367, 6951584, 7643614, 7688618`; C `39402054, 8717005, 8246857`; B `7812440, 35332817, 7955145`; E `40122777, 31423053, 7005913`; F `10588604, 7643473, 38753809`. Không trùng id với 12 Short Watson cũ, với T4–T9 hay bài mẫu (đã đối chiếu). Cảnh clip không đại diện một nơi cụ thể; nếu clip có chữ/logo, thay.
8. **Phát âm `say`:** tên Lickel, Horn, Trebek, Griffin, Julann, Fleming, Oreo, NBC, feet cần nghe thử khi dựng.
9. **Độ dài thật:** ước ~29–34 s; TTS thật chưa đo. F (133 từ) sát trần 135, cân nhắc cắt nửa câu nếu vượt 35 s.

## 5. Tự kiểm (đã chạy, không chạy build)

`specs-v2-T5/_selfcheck.py` (bản sao mẫu `specs-T4/_selfcheck.py`, import `mix_lint` từ `motion/stier/build.py`): 5/5 OK. Kiểm: 55–135 từ (105–133), câu mở ≤ 9 chữ, câu cuối không "?", lời đọc không chữ số, mọi mốc neo khớp chữ, cảnh ≥ 0,9 s, không `~`, counter không prefix số, `mix_lint` (đủ M/D/G, chữ thuần ≤ 35%, không kiểu nào > 60%, không 3 cảnh liền cùng kiểu, không cảnh > 11 s). Không kiểm được: TTS thật, layout, hình clip.

## 6. Góc đã bỏ / dự phòng

- **Bỏ:** "Watson hàng trăm đáp án" (cơ chế đơn lẻ, không người, dễ thành nhóm 13–17% ở lại); góc luật Jeopardy thuần (đã thay bằng F).
- **Dự phòng (chưa đủ nguồn, không dùng):** (1) Trebek ban đầu chấp nhận câu "What is a leg?" của Watson về George Eyser, bản phát sóng cắt cảnh ấy (Wikipedia dẫn Ars Technica 15/02/2011, chưa mở được; nguồn khác ghi Jennings đáp "một bàn tay"); (2) trận suýt bị huỷ tháng 05/2010 vì IBM và nhà sản xuất Harry Friedman bất đồng (Wikipedia dẫn Baker; chưa tìm được URL riêng); (3) 100 trận thử, Watson thắng 65%, người dẫn thử là Todd Alan Crain của The Onion (Wikipedia). Không nên làm thêm quá 6 bài từ Long này.

## 7. File đã tạo

- `docs/pm/tickets/2026-10-20-mim-nov/T5-ke-hoach-v2.md`
- `docs/pm/tickets/2026-10-20-mim-nov/specs-v2-T5/mim-watson-lickel-nha-hang-im-lang.json`
- `.../specs-v2-T5/mim-watson-khong-co-tai-oreo.json`
- `.../specs-v2-T5/mim-watson-ferrucci-sai-gan-het.json`
- `.../specs-v2-T5/mim-watson-buoi-tap-kem-mot-nghin-do.json`
- `.../specs-v2-T5/mim-jeopardy-julann-tren-may-bay.json`
- `.../specs-v2-T5/_selfcheck.py`
