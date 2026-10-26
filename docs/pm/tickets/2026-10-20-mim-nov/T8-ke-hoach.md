# T8: 8 Short MIM gắn Long `mim-ai-khuon-mat` (lên 30/11/2026 20:00) · bản 1, chờ Claude duyệt pha 1

Người lập: agent T8, 20/10/2026. Pha 1: chỉ viết file. Chưa dựng, chưa upload, chưa sửa `state.sqlite`, chưa ghi vào `data/stier/specs`.
Spec 8 bài: `docs/pm/tickets/2026-10-20-mim-nov/specs-T8/<slug>.json` (theme `mim`, định dạng như `data/stier/specs/mim-*.json` đã duyệt).
Long gắn: `long-mim-ai-khuon-mat`, video `7daMUBWG6mU`, hẹn 2026-11-30T13:00:00Z (20:00 VN). Link này đã điền vào mô tả của 8 spec (`https://youtu.be/7daMUBWG6mU`); lời đọc KHÔNG nhắc Long.

## 1. Lịch (giờ VN, lấy từ `scripts/shorts_grid.py`, lưới MIM 06:30 · 11:30 · 17:00 · 19:00 · 21:30)

Ngày 27–30/11 của MIM đang trống hoàn toàn (grid: 0/5 mỗi ngày). Mỗi ngày 2 bài, hai bài khác nhóm. Ngày 30/11 có Long lúc 20:00 nên bài thứ hai lùi về 17:00 (như lô CK 4), các ngày còn lại 11:30 + 19:00. Tất cả đứng TRƯỚC Long, đúng luật "Short nhử Long sắp lên".

| # | Ngày | Giờ | Slug (file spec) | Nhãn |
|---|---|---|---|---|
| S1 | T6 27/11 | 11:30 | `mim-mat-ban-la-128-con-so` | SỐ |
| S2 | T6 27/11 | 19:00 | `mim-bao-gan-thi-la-cung-mot-nguoi` | THỬ (cơ chế) |
| S3 | T7 28/11 | 11:30 | `mim-face-id-mot-phan-trieu` | SỐ |
| S4 | T7 28/11 | 19:00 | `mim-vi-sao-ung-dung-bat-chop-mat` | THỬ (cơ chế) |
| S5 | CN 29/11 | 11:30 | `mim-nist-nhan-mat-gioi-gap-20-lan` | SỐ |
| S6 | CN 29/11 | 19:00 | `mim-robert-williams-30-gio` | SỰ KIỆN |
| S7 | T2 30/11 | 11:30 | `mim-bo-ba-tam-anh-day-may-nhan-mat` | THỬ (cơ chế) |
| S8 | T2 30/11 | 17:00 | `mim-gender-shades-34-phay-7` | SỐ |

Tỉ lệ: SỐ/SỰ KIỆN 5/8 = 62,5%; THỬ 3/8 = 37,5% (đúng 60/40). Không bài nào dùng khung "mẹo". Không có bảng tra tự dò (không có đại lượng nào để người xem tự dò ô của mình).
Thứ tự bài cố ý xen số và cơ chế: không có hai bài SỐ liền nhau, hai bài về thiên kiến/nhầm lẫn (S6, S8) cách nhau một ngày.
Nếu muốn đổi giờ: S7/S8 ngày 30/11 có thể dùng 11:30 + 19:00 (cách Long 1 giờ), nhưng 17:00 giữ khoảng thở 3 giờ.

## 2. Tám bài

Câu mở = câu đọc đầu (đếm tiếng ≤ 9). Khung hình 0 = chữ ≤ 5 từ trên cảnh đầu. Câu chốt đều quay về ý mở, không câu hỏi. Mọi con số trong lời đọc viết bằng chữ (như spec hiện có); chữ số chỉ có trên màn hình và trong tiêu đề/mô tả.

| # | Tiêu đề | Câu mở | Insight duy nhất | Con số + nguồn |
|---|---|---|---|---|
| S1 | Với máy, khuôn mặt bạn là 128 con số: nó lưu và so sánh thế nào? | "Với máy, mặt bạn là một dãy số." (8) | Máy không lưu ảnh hay nụ cười mà lưu một điểm trong không gian 128 chiều; ảnh cùng người rơi gần nhau, khác người rơi xa nhau; chẳng ai biết từng số đo gì. | 128 chiều: script CH03 · FaceNet (CVPR 2015, arXiv 1503.03832). |
| S2 | Bao gần thì máy coi là cùng một người? Ngưỡng nhận mặt do con người chọn | "Bao gần thì máy coi là cùng một người?" (9) | Ngưỡng "cùng người hay không" là lựa chọn của con người: chặt thì chính chủ bị từ chối, lỏng thì người lạ dễ lọt. | Không có số cứng. Nguồn: script CH04 (diễn lại). Hình ledger chỉ là chữ, không có số minh hoạ. |
| S3 | Người lạ mở được Face ID: một phần triệu. Nhưng con số ấy dành cho ai? | "Người lạ mở được Face ID: một phần triệu." (9) | Một phần triệu chỉ đúng với người ngẫu nhiên và khuôn mặt đã đăng ký; sinh đôi, anh chị em giống, trẻ dưới 13 tuổi thì cao hơn. | 1/1.000.000 (Face ID), 1/50.000 (Touch ID), Apple Face ID Security Guide 11/2017 (script CH04). "Chặt hơn khoảng 20 lần" = kênh tự tính (1.000.000/50.000). |
| S4 | Vì sao ứng dụng bắt bạn chớp mắt khi quét mặt? Có hai câu hỏi khác nhau | "Vì sao ứng dụng bắt bạn chớp mắt?" (8) | Nhận diện trả lời "có phải người này không"; chớp mắt/quay đầu trả lời câu khác: "có phải người thật không". | Không có số. Nguồn: script CH07 (diễn lại). Không có hướng dẫn vượt qua kiểm tra. |
| S5 | Bốn năm, máy nhận mặt giỏi gấp 20 lần: số liệu NIST 2014 và 2018 | "Bốn năm, máy nhận mặt giỏi gấp hai mươi." (9) | Trong bài thử tìm một người trong kho ảnh lớn, thất bại giảm từ ~4% xuống ~0,2% nhờ mạng nơ-ron sâu; nhưng chỉ với ảnh chất lượng tốt. | 4% (2014) → 0,2% (2018), "20 lần", NISTIR 8238 (11/2018), script CH05. |
| S6 | Bị giữ khoảng 30 giờ vì máy nhìn nhầm: chuyện Robert Williams, Detroit | "Bị giữ ba mươi giờ vì máy nhìn nhầm." (9) | Một kết quả nhận diện bị tin hơn mức nó xứng đáng dẫn tới bắt nhầm; thoả thuận 2024 cấm bắt chỉ dựa vào nó. | 01/2020, ~30 giờ, thoả thuận 06/2024 (ACLU; michiganpublic.org; cbsnews.com theo ghi chú script CH06). |
| S7 | Máy học nhận mặt bằng những bộ ba tấm ảnh: kéo gần, đẩy xa | "Máy học nhận mặt bằng những bộ ba ảnh." (9) | Cách dạy: ảnh gốc + ảnh khác của cùng người + ảnh người lạ; chỉnh mạng kéo hai ảnh cùng người lại gần, đẩy người lạ xa; lặp hàng triệu khuôn mặt. | Không có số cứng ("hàng triệu" là cách nói của script CH03). Nguồn FaceNet (triplet loss). |
| S8 | Cùng một máy, mức sai chênh hơn 40 lần: nghiên cứu Gender Shades (2018) | "Cùng một máy, sai chênh hơn bốn mươi lần." (9) | Cùng ba hệ thống, mức sai tệ nhất 0,8% (đàn ông da sáng) so với 34,7% (phụ nữ da sẫm); đây là bài đoán giới tính, KHÔNG phải nhận ra danh tính. | 0,8% / 34,7%: Buolamwini & Gebru, PMLR 81 (2018), script CH06. "Hơn 40 lần" = kênh tự tính (34,7/0,8 ≈ 43). |

### Cấu trúc cảnh (mỗi bài đổi thứ tự/loại cảnh so với bài kề; M = ảnh/clip, D = số liệu, G = sơ đồ, T = chữ)

| # | Thứ tự cảnh | Ghi chú |
|---|---|---|
| S1 | kinetic+clip (M) · counter 128 (D) · board hai điểm gần/xa (G) · slam "AI ĐO CÁI GÌ?" (T) · kinetic+cửa sổ clip (M) | khung 0 "MẶT BẠN, VỚI MÁY" |
| S2 | slam (T) · board hai dãy số (G) · kinetic+cửa sổ clip (M) · ledger chặt/lỏng (D) · kinetic+cửa sổ clip (M) | bài duy nhất mở bằng slam, không clip ở khung 0 (chữ 5 từ) |
| S3 | kinetic+clip (M) · ledger 1/50.000 vs 1/1.000.000 (D) · cards3d người ngẫu nhiên vs sinh đôi (G) · slam (T) | |
| S4 | kinetic+clip mắt (M) · cards3d "câu 1" (G) · timeline 4 trạm (D) · cards3d "câu 2" (G) · kinetic+cửa sổ clip (M) · slam (T) | nhịp nhanh, 6 cảnh |
| S5 | kinetic+clip (M) · chart cột 4% vs 0,2% (D) · board "mạng nơ-ron thay cách cũ" (G) · slam "CHỈ VỚI ẢNH TỐT" (T) · counter 20 lần (D) | |
| S6 | kinetic+clip (M) · board ảnh bằng lái ↔ video mờ (G) · counter 30 giờ (D) · cards3d thoả thuận 2024 (G) · slam (T) | không dùng ảnh người thật |
| S7 | kinetic+clip (M) · board bộ ba ảnh (G) · ledger kéo gần/đẩy xa (D) · kinetic+cửa sổ clip (M) · slam (T) | |
| S8 | kinetic+clip (M) · cards3d 0,8% vs 34,7% (G) · board "ít khuôn mặt trong dữ liệu" (G) · slam "ĐOÁN GIỚI TÍNH" (T) · counter hơn 40 lần (D) | |

Cảnh `chart` chỉ dùng ở S5 (theme-mim.css có `.chbar`); không dùng `table` (theme-mim.css chưa có khối `.tbl`).

## 3. Tự kiểm (build.py không có cờ `--lint-only`)

`python motion/stier/build.py <slug> --no-render` vẫn chạy TTS và tải ảnh/clip nên KHÔNG chạy ở pha 1. Thay vào đó đã tự kiểm bằng một script riêng (ngoài repo, scratchpad), chạy trên 8 spec:
- JSON hợp lệ; theme `mim`; `mix: true`.
- Mọi neo `[câu, "chữ", lần, lệch]` đều trỏ tới chữ có trong câu đó (build coi sai neo là lỗi cứng) và số câu hợp lệ.
- Mọi chữ trong `acc` có trong lời đọc.
- Bản sao của `mix_lint` (build.py dòng 384): có đủ M, D, G; chữ thuần T ≤ 35% (kết quả 6–19%); không kiểu nào > 60% (cao nhất 52%: S6 G; giữ ≤ 60%); không 3 cảnh liền cùng kiểu; không cảnh > 11 s (thời lượng ước tính 4,1 tiếng/giây + ngắt như `tts.pauses`).
- Câu mở ≤ 9 tiếng; câu cuối không phải câu hỏi; lời đọc không có chữ số; dòng phụ counter/slam/chart.unit ≤ 52 ký tự; counter không có chữ số/`<>≈~` trong prefix khi số chạy.
- Ước tính thời lượng 22–30 giây, 81–115 tiếng lời đọc (S6 dài nhất, 115 tiếng).
**Chưa kiểm được:** lint thật của build.py, giọng TTS, bố cục từng cảnh trên khung 1080x1920 (cần dựng). Làm ở pha 2.

## 4. Bảng đối chiếu trùng

### 4a. Với Short MIM hiện có (state.sqlite: 160 Short MIM, kind='short', channel='MIM', đọc slug + tiêu đề/dòng đầu của spec; lưới 27–30/11 trống)
Từ khoá đã rà trong mọi `data/stier/specs/mim-*.json` và `data/long/*/script.md`: FaceNet, Face ID, NIST, Gender Shades, Williams, chớp mắt, nhận diện khuôn mặt, embedding, triplet, "bộ ba ảnh", "128 chiều", Buolamwini. Kết quả: không Short nào có; `mim-nobel-ngo-cut` chỉ có "Williams" là David Rumelhart-Hinton-Williams (lan truyền ngược 1986), người khác hoàn toàn.

Các Short gần đề tài nhất:

| Short có sẵn | Nội dung | Bài T8 gần nhất | Vì sao không trùng |
|---|---|---|---|
| `mim-quet-mat-10-trieu` (26/10) | Quy định quét mặt trên 10 triệu; chặn kẻ lạ, không chặn chính chủ bị lừa | S4, S2 | Đó là quy định + lừa đảo bằng giọng giả. T8 không nhắc ngưỡng 10 triệu, không nhắc lừa đảo; S4 nói vì sao có bước chớp mắt (người thật vs ảnh), S2 nói ngưỡng khoảng cách của máy. Khác góc, khác con số. |
| `mim-goi-video-vai-giay`, `mim-hong-kong-cuoc-hop-gia` | Gọi video/cuộc họp giả bằng deepfake | S4 | Deepfake là chủ đề kẻ giả mạo; S4 chỉ nói cơ chế kiểm tra "người thật" của app, không nói về giả mạo. |
| `mim-captcha-*` (nhiều bài) | Kiểm tra "bạn có phải người không" | S4 | Cùng ý "có phải người thật không" nhưng CAPTCHA là chuột/chữ méo, bài này là quét khuôn mặt. Các bài CAPTCHA đã hẹn 21–23/10, cách xa 27/11. |
| `mim-turing-73`, `mim-tai-nguoi-73-phan-tram` | Máy bị nhầm là người; tai người nhận 73% giọng giả | S8 | Khác đối tượng (hội thoại/giọng nói). |
| `mim-17-lan-toi-khong-biet`, `mim-9-tren-10-hoc-sinh-dung-ai` | Mẫu "một con số + cơ chế" | cả 8 | Chỉ giống khuôn dựng, không giống nội dung. |

### 4b. Với ticket T4–T9
- T5: đã có 5 spec trong `specs-T5/` (Watson/Jeopardy); T7: có `T7-ke-hoach.md` + 4 spec poker. Không có từ khoá khuôn mặt/nhận diện/sinh trắc nào. T7-ke-hoach.md ghi rõ "T8 khuôn mặt: không giao đề tài".
- T4 (GPU), T6 (chat/privacy), T9 (máy chơi game): lúc lập chưa có kế hoạch/spec (`specs-T4` trống). Rà theo đề tài: T6 có rủi ro đụng chữ "riêng tư/dữ liệu sinh trắc". T8 không có bài nào về chat/riêng tư/AI lưu dữ liệu, nên không giao. Cần Claude đối chiếu lại khi T6 nộp: từ khoá `khuôn mặt`, `sinh trắc`, `Face ID`, `NIST`, `FaceNet`.
- Clip Pexels: đối chiếu id với `data/stier/specs/mim-*.json` và `specs-T5/T7`: không id nào của T8 bị dùng lại sau khi đổi `28709421` (clip dữ liệu đã dùng ở 18 Short) sang `5545115`.

## 5. Chỗ cần kiểm trước khi dựng

1. **Không có `data/long/mim-ai-khuon-mat/factcheck.md`** (thư mục chỉ có script.md, spec.json, ch00–ch08.json, gen_scenes.py). Luật nguồn của đợt nói "script + factcheck đã kiểm chứng". T8 chỉ dựa vào phần "Nguồn" của script.md, chưa được kiểm độc lập. Cần có factcheck (hoặc T2/T3 bổ sung) trước khi dựng.
2. **Không có mạng ở máy này khi lập**: chưa mở được URL nguồn nào. URL trong `sources` của spec: arXiv 1503.03832 (chắc chắn đúng), NIST IR 8238, PMLR Gender Shades, ACLU Williams là địa chỉ nhớ lại, Apple Face ID Security Guide chưa có URL. Phải mở và đối chiếu từng con số trước khi dựng (mỗi spec có ghi "URL cần kiểm").
3. **S3:** (a) 1/1.000.000 và 1/50.000 đúng bản tháng 11/2017 (guide có bản sau đổi số?). (b) cụm "khuôn mặt đã đăng ký" và "anh chị em sinh đôi, trẻ dưới 13 tuổi". (c) "Chặt hơn khoảng hai mươi lần" là kênh tự tính, đã ghi trong mô tả; nếu muốn bỏ thì xoá dòng 3 và ô ledger.
4. **S5:** 4% (2014) → 0,2% (2018) là tỉ lệ thất bại tìm kiếm 1:N của thuật toán tốt nhất; đối chiếu bài thử cụ thể trong NISTIR 8238 để chắc không lẫn với điều kiện khác. Nhãn cột chart dùng "≈".
5. **S6:** (a) "bị giữ khoảng ba mươi giờ"; ghi "khoảng" trên màn hình, câu mở bỏ chữ "khoảng" cho đủ 9 tiếng (đã ghi "khoảng" trong tiêu đề và câu 4). (b) Thoả thuận tháng 06/2024: nội dung "cảnh sát thành phố không được bắt người chỉ dựa trên kết quả nhận diện khuôn mặt" (script ghi 2024; đối chiếu ACLU). (c) Slam cuối "TIN QUÁ MỨC / CON SỐ CỦA MÁY, HƠN MỨC XỨNG ĐÁNG" là nhận định của script, không phải kết luận pháp lý: nếu Claude thấy nặng, đổi thành "BỊ BẮT CHỈ VÌ MÁY" hoặc bỏ slam. (d) Người có thật, đã là vụ kiện công khai; bài không dùng ảnh người, không đoán lý do ngoài hồ sơ.
6. **S8:** đảm bảo người xem hiểu đây là bài đoán giới tính (đã có slam "KHÔNG PHẢI NHẬN RA DANH TÍNH" + câu 6) và con số là mức sai TỆ NHẤT trong ba hệ thống. Không nêu tên công ty (đúng luật: clip không có tên công ty; script cũng không nêu). "Hơn 40 lần" = kênh tự tính.
7. **S1:** "chẳng ai biết chính xác từng con số ấy đo cái gì" là câu của script CH03; tìm một câu của bài FaceNet hoặc tổng quan nói embedding không diễn giải được để có nguồn trực tiếp.
8. **S4:** câu 3–4 gọi "Bốn trạm nhận diện khuôn mặt" (khái niệm của Long). Đã có timeline liệt kê 4 trạm ngay trên màn hình để Short tự đứng được, nhưng nếu thấy khó hiểu, đổi câu 4 thành "Các bước nhận diện khuôn mặt trả lời câu ấy." Không có hướng dẫn vượt kiểm tra.
9. **Clip:** 8 spec dùng 12 id chọn từ chỉ mục cục bộ `motion/hf/assets/clips/index.json` (chỉ đọc tên mô tả, chưa xem hình, chưa tải): 7299417 (cận mặt), 5545115 (người lướt ảnh trên điện thoại), 7821861 (cầm điện thoại), 7299411 và 3761686 (mắt), 37215129 (đám đông nhìn từ trên), 8225802 (cận mặt nữ), 7477609 (nam đeo kính nhìn camera), 33315117 (code mờ), 7597755 (phản chiếu trên kim loại), 6452590 và 7477917 (cận mặt nữ). **`motion/long/clip_sheet.py` chỉ đọc `data/long/<topic>/ch*.json` (khoá `vid`), không chạy được cho Short.** Pha 2 cần `python motion/stier/clips.py get ...` rồi tự soát 3 khung/clip (không logo, không chữ, không tên công ty; với S6 và S8 (nội dung nhầm lẫn/bắt nhầm) tránh clip cận mặt một người dễ nhận ra, ưu tiên cảnh mờ hoặc đám đông). Các clip chỉ minh hoạ; đã có nhãn "VIDEO MINH HOẠ" ở cảnh cửa sổ, mô tả có câu "không phải cảnh thật của sự kiện".
   Clip 7597755 (13 s), 7821861 (8 s) ngắn: kiểm tra `ms` + độ dài cảnh không vượt hết clip.
10. **Cách đọc `say`:** FaceNet → "Phây-nét", Google → "Gu-gồ", Face → "Phây", ID → "ai đi", Apple → "Áp-pồ", NIST → "en ai ét ti", Detroit → "Đi-troi", Robert → "Rô-bớt", Williams → "Uy-li-ừm". Nghe thử một lần trước khi dựng hàng loạt (S3, S5, S6 nhiều tên riêng).
11. Tiêu đề S1 chứa chữ "128" và S5/S8 có "20 lần", "40 lần": đã thể hiện là kênh tự tính ở mô tả.
12. Mô tả mỗi bài đã có link Long `https://youtu.be/7daMUBWG6mU`, lấy từ `state.sqlite` (item `long-mim-ai-khuon-mat`, stage published, hẹn 30/11 20:00). Nếu T2/T3 thay video, phải đổi 8 chỗ.

## 6. Chỗ thiếu góc / góc dự phòng

Đủ 8 bài, không thiếu. Góc dự phòng nếu Claude loại bài nào (cùng nguồn script, chưa trùng):
- **Căn thẳng ảnh:** "thêm một bước, sai giảm hơn ba lần": FaceNet LFW 98,87% (cắt giữa) → 99,63% (có căn thẳng) = sai 1,13% → 0,37% (kênh tự tính ≈ 3 lần). Nhãn SỐ. Chưa dùng vì số kênh tự tính, và dễ gần S1/S7 (đều FaceNet).
- **Tìm khuôn mặt bằng mẫu sáng tối (CH01):** vùng mắt tối hơn má, sống mũi sáng hơn. Nhãn THỬ. Mỏng (không có số, không có nguồn sơ cấp trong script; nêu Viola-Jones 2001 phải tự kiểm).
- **Anh chị em sinh đôi/trẻ dưới 13 tuổi riêng (CH04):** đã gói trong S3 để giữ một insight; có thể tách thành bài riêng nhưng trùng nguồn Apple.
- **"Ảnh chất lượng tốt" (CH05):** đã gói trong S5.
Góc KHÔNG khai thác: quy định 10 triệu/20 triệu (đã có `mim-quet-mat-10-trieu`); cách vượt kiểm tra người thật (cấm theo luật script).

## 7. Đề nghị cho pha 2

1. Dựng S1 làm bài mẫu duyệt trước (chuẩn Short v3): mở bằng chữ, số lớn đếm lên 128, giọng Thanh Bình. Sau duyệt mới dựng 7 bài còn lại, tuần tự, khoá `output/.render.who`.
2. Trước khi dựng: xử lý mục 5 điểm 1, 2, 9, 10.
3. Đăng riêng tư + hẹn giờ đúng bảng mục 1; chạy lại `scripts/shorts_grid.py 2026-11-27 2026-11-30 --channel MIM` để chắc không ai chiếm slot trong lúc chờ (lúc lập: 0/5).
4. Sau đăng: retro bằng subagent.
