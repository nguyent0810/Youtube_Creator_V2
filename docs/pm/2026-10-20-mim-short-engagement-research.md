# MIM Short "chưa hấp dẫn": nghiên cứu nguyên nhân gốc (20/10/2026)

Phạm vi: chỉ nghiên cứu, không dựng, không upload, không sửa spec hay state. Mẫu chẩn đoán: `mim-gpu-55-lan-2009` (bản mẫu chưa đăng).
Số liệu: `python scripts/analytics_report.py --channel MIM` và `--channel CK` chạy 20/10 ~10:45 (file `data/analytics/MIM/20261020T1045.json`, `data/analytics/CK/20261020T1047.json`), cộng spec trong `data/stier/specs/` và `output/stier/<slug>/timing.json`.
Đã đọc: `data/briefs/MIM.md`, `docs/pm/2026-10-12-shorts-analysis.md`, memory `project-mim-first-growth-loop`, `project-short-mix-standard`, và (nhánh origin/main của vietneu-tts) `docs/DATA_ANALYSIS_2026-10.md`, `.claude/skills/shorts-lookup/SKILL.md` + `references/retro_2026-10-19.md`. Chưa đọc kỹ `docs/pm/2026-10-13-ypp-monetization-research.md` (không cần cho kết luận về nội dung Short).

## 0. Tóm tắt

1. Thước đo hợp lý nhất: **% ở lại = engagedViews/views** (proxy của "Stayed to watch"). Từ dữ liệu FS đã biết: ≥45% thì mới vượt trần ~1.000 view. MIM hiện: trung vị 28%, chỉ 3/32 video đạt 45%. View thô của MIM bị kẹt 1.000–1.400 nên không phân biệt được video hay/dở; % ở lại thì phân biệt được (11% → 58%).
2. Nhóm cao nhất là **truyện có người, có xung đột, có bước ngoặt** (nuoc-78 58%, shannon 55%, ai-bia 52%, perceptron/eliza 44%). Nhóm thấp nhất là **mẹo, giải thích cơ chế, báo cáo, thống kê trần** (ghi-nguon 11%, qr-mien-phi 13%, lighthill 16%, deepfake 17%, qr-ban-30 17%).
3. Về hình thức, nhóm cao có **nhiều cảnh hơn, đổi hình nhanh hơn, dài hơn**: trung vị 9,5 cảnh / 32 s / 130 chữ so với nhóm thấp 6 cảnh / 24 s / 90 chữ. Quy tắc "rút còn 18-25 s" ở docs 12/10 không có bằng chứng ủng hộ, dữ liệu đi ngược lại (xem mục 1.3).
4. `mim-gpu-55-lan-2009` rơi vào đúng kiểu của nhóm thấp: không người, không xung đột, mở bằng khẳng định chung, 4,9 s/cảnh (chậm nhất mọi Short), phần cuối 6 s là câu rào đón, và hai cảnh có lỗi hình (biểu đồ trống, vòng tròn đen). Nguyên nhân hàng đầu là **kịch bản/chủ đề**, không phải engine.

## 1. Dữ liệu thật

### 1.1 Bảng top/bottom (MIM, Short, views ≥ 300, 31 video)

% ở lại = engaged/views toàn thời gian đo đến 20/10. Views thô in kèm.

| Hạng | Short | Views | % ở lại | Dài (s) | Cảnh | s/cảnh | Chữ (lời) | Mở bằng năm/số? | Kiểu |
|---|---|---|---|---|---|---|---|---|---|
| 1 | teaser-nuoc-78 | 1.409 | 58% | 35,1 | 13 | 2,7 | 135 | có (2016) | truyện đối đầu, có bước ngoặt, kết lửng |
| 2 | shannon-1951 | 1.273 | 55% | 22,8 | 8 | 2,9 | 94 | có (1951) | thí nghiệm mà người xem tự thử được |
| 3 | ai-bia | 1.233 | 52% | 35,4 | 9 | 3,9 | 132 | không | mâu thuẫn "tự tin mà sai", có câu hỏi–đáp |
| 4 | youtube-20-nam | 1.246 | 44% | 30,2 | 9 | 3,4 | 115 | có | sự kiện có ngày, giá |
| 5 | teaser-perceptron | 1.313 | 44% | 32,0 | 11 | 2,9 | 133 | có | truyện sống-chết-sống lại |
| 6 | teaser-eliza | 1.288 | 44% | 34,1 | 14 | 2,4 | 135 | có | có đoạn đối thoại trên màn hình |
| 7 | nobel-ngo-cut | 1.316 | 42% | 31,8 | 6 | 5,3 | 95 | không | "ngõ cụt rồi Nobel" |
| 8 | ai-doan-chu | 1.013 | 40% | 30,4 | 10 | 3,0 | 127 | không | khái niệm có ví dụ gõ chữ |
| 24-31 (thấp) | alphago-nuoc-37 | 1.218 | 21% | 23,0 | 6 | 3,8 | 86 | không | chỉ một sự kiện, không có hồi kết |
| | qr-ban-30 | 1.009 | 17% | 24,8 | 6 | 4,1 | 98 | có số % | giải thích cơ chế |
| | meo-deepfake-goi-lai | 992 | 17% | 28,5 | 9 | 3,2 | 118 | không | mẹo |
| | lighthill-1973 | 1.257 | 16% | 24,2 | 6 | 4,0 | 93 | không | báo cáo, "mùa đông AI" trừu tượng |
| | qr-mien-phi | 1.006 | 13% | 24,4 | 6 | 4,1 | 96 | không | "vì sao miễn phí" |
| | meo-ai-ghi-nguon | 591 | 11% | 19,6 | 7 | 2,8 | 86 | không | mẹo |

Trung vị 31 video: 28%. Spearman với % ở lại: thời lượng +0,56, số chữ +0,52, số cảnh +0,38, mật độ chữ trên màn hình +0,27, số cảnh có clip nền -0,18, view thô +0,53, % xem trung bình (avp) -0,06. avp không dự đoán gì, đúng như memory đã ghi (video vòng lặp có avp 126-127% mà ở lại chỉ 28-29%).

Hạng 7 (nobel) có 5,3 s/cảnh nhưng vẫn 42%: nội dung có kịch tính (từng bị bỏ rơi rồi thắng) bù cho nhịp chậm. Nhịp không phải yếu tố duy nhất.

### 1.2 So sánh có hệ thống

| Trục | Nhóm cao (8) | Nhóm thấp (8) | Bằng chứng |
|---|---|---|---|
| Câu mở | 4/8 có năm hoặc số cụ thể; còn lại là một mâu thuẫn ("tự tin mà bịa", "ngõ cụt rồi Nobel") | 1/8 có năm; phần lớn là khẳng định/câu hỏi chung ("Muốn bắt AI bịa?", "Bạn quét QR mỗi ngày mà…") | Mở có năm: trung vị 44% (n=9) so với 26% (n=22) |
| Có người/xung đột/bước ngoặt | Có ở 6/8 (Lee Sedol thua rồi thắng, Rosenblatt, Weizenbaum, Shannon) | Gần như không có; QR, Lighthill, "mẹo" là cơ chế và quy tắc | Đọc lời đọc 13 Short |
| Cách kết | Kết lửng/mở vòng ("AI đã chết hai lần", "Ai giống người hơn?") hoặc chốt có trọng lượng | Kết là câu tổng kết trung tính ("Một thói quen mới, hình thành nhanh như thế đấy", "Vài phút kiểm tra, đỡ một lần chia sẻ…") | Đọc câu cuối từng Short |
| Độ dài / số cảnh | 32 s, 9,5 cảnh | 24 s, 6 cảnh | Trung vị; dur ≥ 29 s: 44% (n=8) so với < 29 s: 25% (n=23) |
| Nhịp | 2,4-3,9 s/cảnh (trừ nobel) | 3,8-4,1 s/cảnh | Mục 1.1 |
| Chữ trên màn hình | 225-465 ký tự | 214-345 ký tự | Không phân biệt được (Spearman +0,27 yếu) |
| Loại cảnh | Có `date`, `quote`, `question`, `ledger`, `calendar`: trung vị 44-58% | `board`/`cards3d`: 24-27% so với 31-39% khi không có | n nhỏ (1-17 mỗi nhóm), chỉ là gợi ý. Cảnh `board`/`cards3d` xuất hiện từ lô v3 (13/10) trở đi nên lẫn với "Short sau 14/10 đều dưới 40%" |
| Clip nền | Không khác biệt, Spearman -0,18 | | |

### 1.3 Cặp so sánh gần như cùng chủ đề (bằng chứng mạnh nhất)

- **AlphaGo nước 37 vs nước 78:** cùng ván cờ, cùng 2016. `alphago-nuoc-37` (23 s, 6 cảnh, kể một sự kiện) 21%. `teaser-nuoc-78` (35 s, 13 cảnh, "chỉ thắng một ván" -> thua ba -> nước 78 -> máy đáp sai -> thắng -> cliffhanger) 58%.
- **Đoán chữ:** `shannon-1951` (một người đoán chữ tiếp theo, 69%) 55% vs `ai-doan-chu` (giải thích khái niệm) 40%.
- **AI bịa:** `ai-bia` (mâu thuẫn, câu hỏi–đáp, con số 45%) 52% vs `meo-ai-ghi-nguon` (mẹo) 11%.

Chủ đề giống, khác biệt nằm ở cấu trúc kể chuyện và nhịp. Điều này loại bỏ nghi ngờ "chỉ do chủ đề".

### 1.4 CK (để kiểm chứng chéo)

Trung vị % ở lại 31%, 5/28 đạt 45%. Cao: lai-kep-lam-phat 49% (2.893 view), vang-9-nam 49%, 24-03-2020 48%, mua-deu-97-lan 48%, tiet-kiem-so-xanh 46%. Thấp: khoi-ngoai-9-thang 21%, vang-dinh-51-trieu 20%, trailer 23%. Nhóm cao mở bằng **một con số tiền của chính người xem** ("ba triệu mỗi tháng", "gửi tiết kiệm mười hai tháng"), nhóm thấp mở bằng sự kiện thị trường vĩ mô. Thời lượng CK trung vị 26 s, 6 cảnh: không có chênh lệch thời lượng rõ như MIM. Hai kênh cho cùng kết luận ở một điểm: **có người xem trong câu chuyện (hoặc có tiền của họ) thì ở lại, trừu tượng thì lướt**.

### 1.5 Khớp với các tài liệu cũ

- FS (`DATA_ANALYSIS_2026-10.md`): chủ đề quyết định ở lại rất mạnh (2027 50%, năm sinh 52% so với Kinh Dịch 15%); chỗ nào có "chìa khoá cá nhân" thì ở lại cao. Đổi hook của nhóm yếu không giúp. Nhóm Short thắng lớn là bảng tự dò (Tam Tai 51.340 view, avp 132%).
- docs 12/10 (mục 7): "một insight, bỏ ngày tháng" và "ép ngắn" là suy đoán của PM và agy. Dữ liệu 8 ngày sau cho thấy **ngày tháng cụ thể đi cùng nhóm cao** (44% so với 26%) và Short dài hơn khá hơn. Hai quy tắc này cần xem lại.
- memory 19/10: "lead with a number or dated event, avoid mẹo, close by returning to the opening idea". Dữ liệu ủng hộ hai ý đầu; ý thứ ba ("quay về câu mở") chưa có bằng chứng: nhóm cao kết bằng cliffhanger hoặc chốt có trọng lượng, chưa thấy mẫu vòng lặp rõ ràng.

## 2. Chẩn đoán `mim-gpu-55-lan-2009`

Spec: 5 cảnh, 24,55 s, 97 chữ, 4,9 s/cảnh (chậm nhất mọi Short MIM ≥ 300 view; nhóm cao 2,4-3,9). Lời đọc: "Vài tuần dạy máy, rút còn một ngày. Năm 2009, nhóm Andrew Ng ở Stanford thử dạy mạng nơ-ron trên card đồ hoạ. Họ so với bộ xử lý hai lõi. Card nhanh hơn tới 55 lần. Mạng lớn vài tuần còn một ngày. Đó là kết quả của một thí nghiệm, trên một bài toán, so với một loại máy. Nhưng vài tuần đã thành một ngày."

### 2.1 Lỗi kịch bản / chủ đề (nguyên nhân hàng đầu)

- **Không người, không xung đột.** Andrew Ng chỉ là một cái tên trong câu 2; không có ai bị bất ngờ, thua, hoặc nghi ngờ. So với nuoc-78 (Lee Sedol thua rồi thắng) hay perceptron (cỗ máy 5 tấn, báo chí gọi là đối thủ của não người), đây là một kết quả đo, đúng kiểu "báo cáo" như lighthill 16%.
- **Khung 0 trừu tượng.** "Vài tuần dạy máy, rút còn một ngày" không nói ai, không nói tại sao tôi phải quan tâm, và là thẻ chữ chứ không phải hình. Nhóm cao mở bằng sự kiện có người ("Năm 2016, con người chỉ thắng AlphaGo đúng một ván", "Trò chơi của ChatGPT có từ năm 1951"). Con số kịch tính (55 lần) bị hoãn tới giây 11,7.
- **Hơn 6 s cuối là câu rào đón.** Câu 6 ("kết quả của một thí nghiệm, trên một bài toán, so với một loại máy") đúng về trung thực nhưng chiếm khoảng 4 s, và cảnh "MỘT THÍ NGHIỆM" kéo dài 6 s (frame 10-13 trong sheet) không có nội dung mới. Các video ở lại thấp (qr-mien-phi, nuoc-37) cũng kết bằng câu giảm lực. Rào đón cần giữ vì luật dữ kiện, nhưng nên nén còn nửa câu và đặt trước đoạn chốt.
- **Chủ đề GPU/học sâu có nhu cầu nền thấp.** Wikipedia tiếng Việt (bảng trong `data/briefs/MIM.md` phần Nhu cầu): "Chất bán dẫn và Nvidia" 30 lượt/ngày (x0,54 so với năm trước), "Học máy/mạng nơ-ron" 30/ngày (x0,50), so với "Trí tuệ nhân tạo" 1.156 (x2,85) và ChatGPT/OpenAI 394. Lưu ý: đây là mức quan tâm tìm hiểu, không phải nhu cầu xem video; Short sống nhờ feed nên nhu cầu tìm kiếm chỉ là gợi ý. Mẫu liên quan: alexnet-2-card (hai card chơi game, 28%) trung bình thấp.
- Phải thừa nhận: không có Short GPU nào trong dữ liệu thật để so, nên "GPU là chủ đề xấu" là **suy đoán**; chỉ chắc chắn rằng đóng gói kiểu "kết quả đo" cho % ở lại thấp.

### 2.2 Lỗi hình ảnh / engine (nhìn từ final_sheet.jpg, 13 khung mẫu cách ~1,9 s)

- **Cảnh biểu đồ trống:** khung 5-6 (khoảng 8,5-11 s) chỉ có tiêu đề và đường nền; thanh "1" nhỏ xuất hiện trước, cột 55 chỉ hiện ở khoảng 12,5 s và ngay khung sau đã mờ khi chuyển cảnh. Cột lớn nhất và là nhân vật chính của Short gần như không có khung nào nhìn rõ trong các khung mẫu. Lưu ý: chỉ xem 13 khung, chưa soi từng frame, nhưng chữ "55" ở khung 8 nhỏ và xám đúng là chữ số đầu tiên cần được nhìn thấy.
- **Khoảng đen đầu cảnh vòng tròn:** khung 10-11 (cảnh `kinetic` có `win`) cửa sổ tròn gần như đen vài giây rồi clip mới hiện; kéo dài hơn nửa cảnh cuối.
- **Cảnh 2 là 6 s tĩnh:** "STANFORD · 2009 / ANDREW NG" (khung 2-4) lặp lại gần như cùng một hình 6 s, đã khiến cảnh dài nhất chính là câu 2 về tên riêng, vô nghĩa với người chưa biết.
- **Hình nhịp thấp:** 5 cảnh trong 24,5 s. Ở nhóm cao là 9-14 cảnh.

### 2.3 Lỗi chọn clip

- `pexels:3147349` (thùng máy tính tím, tối) làm nền cho "STANFORD · 2009" không liên quan đến Stanford hay mạng nơ-ron; veil 0,5 làm tối thêm, lại là hình đầu tiên sau khung hook. `pexels:854969` ở cuối (bên trong thùng máy) cũng chung vấn đề: hình minh hoạ chứ không phải bằng chứng. Quy tắc 5 của docs 12/10 ("bằng chứng trực quan thay B-roll chung chung") bị vi phạm. Nhưng dữ liệu cho thấy số clip nền không dự đoán % ở lại (Spearman -0,18), nên **đây là lỗi nhỏ so với 2.1**; sửa thì tốt, nhưng thay clip tốt hơn không cứu được kịch bản.

### 2.4 Phân loại

| Loại lỗi | Mức tác động (đã/chưa đo) |
|---|---|
| Kịch bản/chủ đề (không người, mở trừu tượng, kết rào đón) | Cao; đo được gián tiếp qua nhóm (12 Short mẫu), chưa đo bằng thử trực tiếp |
| Nhịp (4,9 s/cảnh, 5 cảnh) | Trung bình-cao; tương quan +0,38 với số cảnh, +0,56 với thời lượng; có thể lẫn với kiểu truyện |
| Hình ảnh/engine (biểu đồ trống, vòng tròn đen) | Trung bình; là lỗi chất lượng thật nhưng chưa có thước đo tác động lên % ở lại |
| Chọn clip | Thấp; tương quan nhỏ |

## 3. Đề xuất (xếp theo tác động)

Mỗi đề xuất ghi rõ chỗ nào là dữ liệu, chỗ nào là suy đoán. Tất cả đo bằng `python scripts/analytics_report.py --channel MIM` (cột %ở lại), so với đường nền trung vị 28% và ngưỡng 45%, trên lô ≥ 6 Short cùng cách làm (n nhỏ thì chỉ là tín hiệu).

1. **Viết lại theo khung truyện: người -> thử/đối đầu -> bước ngoặt -> kết lửng, cho mọi Short "kết quả/sự kiện".** Nhóm cao đều có khung này, nuoc-78 vs nuoc-37 là thí nghiệm tự nhiên (58% so với 21%). Với GPU-55: kể về nhóm Stanford dạy mạng nơ-ron, vì sao ai cũng chê card đồ hoạ chỉ để chơi game, tính ra mất vài tuần trên CPU -> một ngày; kết lửng sang AlexNet 2012 (đã có Short alexnet). Đo: lô 6 Short viết theo khung này có trung vị % ở lại ≥ 40% hay không. Chắc: tương quan; suy đoán: nhân quả (chủ đề dễ kể cũng dễ ở lại).
2. **Mở bằng năm/sự kiện hoặc con số có người, không mở bằng khái niệm.** 44% (n=9) so với 26% (n=22). Với GPU-55: "Năm 2009, một nhóm ở Stanford đem card chơi game đi dạy máy." thay cho "Vài tuần dạy máy, rút còn một ngày." Đo: % ở lại theo nhóm "mở có năm" so với "không", theo tuần.
3. **Bỏ trần 25 s, thử 30-35 s với 9-13 cảnh, mỗi cảnh ≤ 3,5 s.** 44% (n=8, ≥ 29 s) so với 25% (n=23). Cảnh báo: lẫn với kiểu truyện (teaser) vì 3/8 là teaser; không có thử nghiệm riêng. Cần thử A/B bằng hai lô cùng chủ đề (ví dụ hai Short cùng chuỗi, một 25 s, một 33 s). Đo: % ở lại và avp theo lô.
4. **Dừng/hạ các loại mẹo, "vì sao… miễn phí", giải thích cơ chế đơn lẻ** (ghi-nguon 11%, qr-mien-phi 13%, lighthill 16%, deepfake 17%, qr-ban-30 17%). 5 trong 6 video thấp nhất thuộc nhóm này, đã có 3 video "mẹo/giải thích" lặp. Nếu giữ, bắt buộc có một nhân vật cụ thể ở câu 1-2. Đo: trung vị series "mẹo/cơ chế" sau 6 Short; < 25% thì dừng (đúng luật dừng đã có trong `analytics_report`).
5. **Viết cho câu cuối là đỉnh, không phải rào đón.** Rào đón (trung thực) vẫn giữ nhưng nén xuống một mệnh đề, đặt giữa lời đọc; câu cuối phải là bước ngoặt hoặc câu hỏi mở dẫn sang video dài (như eliza, perceptron, nuoc-78: cả ba kết bằng "AI đã chết hai lần"). Lưu ý: ba video này đều là teaser của cùng một video dài nên không tách được hiệu ứng kết lửng khỏi hiệu ứng teaser. Đo: so % ở lại của Short kết lửng với kết tổng kết cùng chủ đề; đo thêm views của video dài (hiện còn ~0-70) để biết kết lửng có đưa người sang không.
6. **Sửa lỗi engine đã thấy ở sheet, không phụ thuộc kịch bản.** (a) Biểu đồ: dựng bar từ frame đầu của cảnh hoặc chờ từ khoá `at` nhưng giữ khung kết thúc ≥ 1,5 s với cột lớn rõ, chữ số ≥ 90 px; không để axis trống khi lời đọc đã nói số; (b) cảnh cửa sổ tròn: bắt đầu clip từ mốc có hình, không để khoảng đen (đã gặp ở GPU-55); (c) cảnh tĩnh > 4 s phải có chuyển động hoặc đổi hình. Cách đo: chạy `clip_sheet.py`/`final_sheet` và soát từng khung chính: biểu đồ có cột chính rõ ở ≥ 2 khung liền. Đây là sửa chất lượng, tác động lên % ở lại là suy đoán.
7. **Chọn clip là bằng chứng hoặc bỏ clip.** Cho Short này: bỏ nền thùng máy tím; dùng ảnh/cảnh liên quan (ảnh Stanford, hình card đồ hoạ cổ điển trong Commons có giấy phép phù hợp) hoặc để cảnh sơ đồ tự dựng CPU hai lõi vs hàng trăm lõi. Tác động nhỏ theo dữ liệu (Spearman -0,18, không có hiệu ứng rõ); làm sau các mục trên.
8. **Dò chủ đề theo ưu tiên có "chìa khoá cá nhân" kiểu FS** (số tiền/giờ/việc làm của chính người xem). CK có bằng chứng nội bộ (mua đều 3 triệu/tháng 48%). Với MIM: chuỗi "việc làm và máy" (Keynes, Oxford 47%, Stanford 22-25 tuổi) là ứng viên nhưng chưa có số (Short mới). Đo: % ở lại của chuỗi đó khi Analytics đủ ngày (>=3 ngày). Suy đoán, chưa có bằng chứng trực tiếp trên MIM.

### Thứ tự làm đề xuất

1 và 2 (cùng kịch bản), 5, rồi 3 (A/B), 6 (sửa engine ngay vì không tốn công đo), 4 (cắt lịch), 7, 8.

## 4. Hạn chế của nghiên cứu này

- n nhỏ (31 Short MIM, 28 CK), một tuần dữ liệu, nhiều biến lẫn (kiểu truyện, teaser, ngày đăng, hình thức v1/v2/v3). Spearman không loại được nhân quả ngược (chủ đề tốt thì viết dài, dựng nhiều cảnh).
- `engagedViews/views` là proxy của "Stayed to watch" (đã ghi nhận trong memory 20/10), chưa có cột "viewed vs swiped away" từ Studio để đối chiếu.
- Chủ kênh nhận xét "chưa hấp dẫn" khớp với kết luận nhưng chưa được đo trên chính Short này (chưa đăng).
- Kết luận về GPU-55 dựa vào lời đọc/spec và 13 khung mẫu trong `final_sheet.jpg`, chưa xem video đầy đủ.
- Không dùng Wikipedia pageviews như nhu cầu xem video; xem mục 2.1.
