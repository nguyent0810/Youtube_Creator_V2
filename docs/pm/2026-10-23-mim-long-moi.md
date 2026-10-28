# Bốn Long MIM mới cho 16–22/11/2026 (khuôn "Ngoài Đời Thật") — 23/10/2026

Kênh **Mind in the Machine (MIM)**. Lịch mới là 4 Long/tuần (T2, T4, T6, CN 20:00 VN). Long đã hẹn tới hết 15/11 (`mim-apollo-1202`). Tài liệu này chọn 4 Long cho 16/11, 18/11, 20/11 và 22/11: hai bài 20–30 phút, hai bài 9–12 phút. Pha 1 chỉ viết file: chưa dựng, chưa upload, không đụng `state.sqlite` (chỉ đọc ở chế độ `-readonly` để xem lịch).

**Đầu vào:**
- Memory: chép cơ chế, không chép bề mặt; kế hoạch YPP; insight của AI Learning; nhịp Long MIM; đổi dạng lộ trình; clip sheet; mô tả không chứa ghi chú nội bộ.
- `docs/pm/2026-10-22-bao-cao-3-kenh.md`
- `docs/pm/2026-10-22-cl-ke-hoach-long-ngoai-doi-that.md`
- `docs/pm/tickets/2026-10-20-mim-nov/T1-ket-qua.md`
- Mẫu `data/long/mim-apollo-1202` và `mim-dich-may`
- `motion/long/{README,RETENTION,SOURCES}.md`

## 0. Chép cơ chế của CL, không chép bề mặt

Long CL thắng nhờ ba thứ:
1. Một mỏ neo khán giả đã biết sẵn.
2. **Một** người thật.
3. Một cold open có ngày giờ, cộng các câu hỏi hẹn chương.

Long MIM hiện chỉ có khoảng 2,3 nghìn lượt hiển thị, CTR 2,6%. Tiêu đề kiểu "Mã 1202" không có gì để người xem "nhận ra ngay".

Mỏ neo tự nhiên của MIM là một **phim hoặc app về AI/công nghệ mà người Việt đã biết**. Khuôn tiêu đề: `[PHIM/APP] Ngoài Đời Thật: [người thật] — [chi tiết tò mò]`.

Ba điều không chép từ CL:
- **Không chép độ dài:** vẫn giữ một bài 9–12 phút và một bài 20–30 phút để so.
- **Không chép giọng kể tội phạm.**
- **Không dùng hình phim:** phim chỉ được nhắc bằng lời và chữ.

## 1. Cách đo

**Nhu cầu:** Wikimedia Pageviews REST, `all-access/user`, tổng 28 ngày **24/09–21/10/2026**.
- Bài tiếng Việt lấy qua langlinks từ bài EN. "—" là không có bài vi.
- Đây là mức quan tâm để đọc, không phải nhu cầu xem video.
- Vẫn chưa có dữ liệu YouTube Studio Research cho MIM.

**Trùng lặp:** grep 19 thư mục `data/long/mim-*` (script) cùng 228 bundle Short trong `bundles/MIM` và `data/stier/specs`.

**Ảnh:** Commons API, lấy `LicenseShortName` của khoảng 15 kết quả đầu. MIM chỉ nhận PD, CC0 và CC BY, **không nhận BY-SA/GFDL**. Phải đọc lại giấy phép trước khi tải.

## 2. Bảng ứng viên (20)

**Quy ước:**
- **vi / en:** lượt xem 28 ngày của bài phim/app mỏ neo, cộng bài nhân vật nếu có.
- **Trùng:** so với Long/Short MIM đã có.

| # | Mỏ neo → người thật, sự kiện có ngày | vi | en | Trùng | Ảnh tự do | Kết luận |
|---|---|---|---|---|---|---|
| 1 | **Kẻ Hủy Diệt → Stanislav Petrov**, báo động giả Oko 26/09/1983 | Kẻ hủy diệt 685; phần 2 444; Petrov 78 | Terminator 110.811; Petrov 42.382; vụ báo động 19.013 | Không có Long. Short `mim-skynet-1997` hợp làm phễu | Có bia tưởng niệm (PD, CC0) và ảnh Không quân Mỹ (PD). **Chân dung Petrov đều BY-SA** | **CHỌN**, 20–30 phút |
| 2 | **Oppenheimer → Richard Feynman**, máy IBM và "máy tính người" ở Los Alamos; Trinity 16/07/1945 | Oppenheimer (phim) 834; Feynman 580 | phim 207.954; Feynman 84.957 | Không | Ảnh thẻ Los Alamos của Feynman (CC0, PD); Trinity (PD); IBM 601 (CC BY 4.0) | **CHỌN**, 20–30 phút |
| 3 | **Siri → Susan Bennett**, giọng thu năm 2005; Siri ra mắt 04/10/2011 | **Siri 2.449**; Steve Jobs 4.484 | Siri 27.641; Bennett 5.913 | Không. `mim-ai-voice` là chủ đề nhái giọng, góc khác | Ảnh VOA của Bennett (PD); Jobs CC BY 2.0 | **CHỌN**, 9–12 phút |
| 4 | **Google Maps → Ronald Reagan và KAL 007**, 01/09/1983 → GPS cho dân dụng | Google Maps 596; GPS 767; KAL 007 196 | Maps 105.685; KAL 25.881; GPS 30.470 | Không | Reagan đọc diễn văn về KAL 007 (PD); vệ tinh GPS (PD). Ảnh máy bay là GFDL/BY-SA nên không dùng | **CHỌN**, 9–12 phút |
| 5 | Người Giải Mã (The Imitation Game) → Turing và máy Bombe | phim 146; Turing 971; Enigma 304 | phim 63.948; Turing 196.286 | Long `mim-ai-70` đã có phép thử Turing; Short `mim-turing-1950` | Phần lớn ảnh Bombe/Enigma là BY-SA | Dự bị |
| 6 | Her → ELIZA / Weizenbaum 1966 | Her 222 | Her 56.393; ELIZA 20.728 | **Long `mim-ai-70` CH02** đã kể ELIZA | — | Loại (trùng) |
| 7 | 2001: A Space Odyssey → HAL 9000 và bài Daisy | 139 | 116.574 | **`mim-ai-voice` CH08** đã kể Daisy; `mim-ai-70` CH07 | — | Loại (trùng) |
| 8 | Hidden Figures → Katherine Johnson kiểm quỹ đạo John Glenn 20/02/1962 | — (không có bài vi); K. Johnson 218 | phim 65.939; Johnson 55.573 | `mim-ai-jobs` đã kể Dorothy Vaughan; Short `mim-dorothy-vaughan-fortran` | Rất nhiều ảnh NASA (PD) | Dự bị (người Việt ít biết phim) |
| 9 | Tôi, Người Máy (I, Robot) → Robert Williams, người đầu tiên chết vì robot, 25/01/1979 | 199 | phim 414.157; Williams 1.654 | Không | Ảnh Unimate thưa, BY-SA | Loại (nguồn sơ cấp mỏng) |
| 10 | Uber → Elaine Herzberg, xe tự lái 18/03/2018 (NTSB) | Uber 327; xe tự lái 53 | 3.637 | Không | Ảnh NTSB (PD) | Dự bị (bi kịch gần, người lái còn sống) |
| 11 | Doraemon → WABOT-1, Ichiro Kato 1973 | **Doraemon 3.757** | 38.609; WABOT không có bài | Không | Không có ảnh tự do, bản quyền Waseda và Honda | Loại (hình, nguồn tiếng Anh mỏng) |
| 12 | Ma Trận (The Matrix) | 852 | 111.242 | `mim-ai-feed` đã nhắc | — | Loại (không có một người thật và một ngày) |
| 13 | Người Sắt (Iron Man) → J.A.R.V.I.S. | 630 | 91.607 | Không | — | Loại (không có người thật) |
| 14 | Ex Machina → Eugene Goostman 07/06/2014 | 141 | 54.420 | `mim-ai-70` (phép thử Turing) | — | Loại |
| 15 | WarGames → Reagan và NSDD-145 (1984) | — | 34.011 | Không | PD | Loại (người Việt không biết phim). Đưa một câu vào bài Petrov nếu cần |
| 16 | Big Hero 6 → robot chăm sóc | 300 | 40.934 | Không | — | Loại (không có người thật) |
| 17 | WALL-E | 389 | 46.673 | Không | — | Loại (như trên) |
| 18 | Tetris → Alexey Pajitnov | 214 | 48.417 | Không | — | Loại (người còn sống, xa AI) |
| 19 | Deep Blue | 89 | 11.552 | **Đã có Long** `mim-deep-blue-kasparov` | — | Loại |
| 20 | Astro Boy (Atom) | 86 | 18.072 | Không | — | Loại (nhu cầu thấp) |

## 3. Bốn chủ đề chọn và lý do

| Ngày (20:00 VN) | Slug | Tiêu đề (titles[0]) | Dài (lời đọc 210–215 âm tiết/phút; cộng nghỉ) | Lộ trình |
|---|---|---|---|---|
| T2 16/11 | `mim-oppenheimer-feynman` | OPPENHEIMER Ngoài Đời Thật: Richard Feynman — Cuộc Đua Giữa Người Và Máy IBM Ở Los Alamos | 4.948 âm tiết, 13 chương. Lời đọc ≈ 23,0–23,6 phút; cộng nghỉ ≈ 27 phút | "ổ khoá ba số" (Feynman mở két) |
| T4 18/11 | `mim-google-maps-kal007` | GOOGLE MAPS Ngoài Đời Thật: Ronald Reagan Và Chuyến Bay KAL 007 — Ai Trả Giá Cho Chấm Xanh Của Bạn | 2.217 âm tiết, 7 chương. Lời đọc ≈ 10,3–10,6 phút; cộng nghỉ ≈ 12 phút | "con số co lại": thước sai số từ hơn 600 km xuống khoảng 100 m rồi khoảng 5 m |
| T6 20/11 | `mim-ke-huy-diet-petrov` | KẺ HỦY DIỆT Ngoài Đời Thật: Stanislav Petrov — Người Không Tin Máy Tính Đêm 26/9/1983 | 4.847 âm tiết, 12 chương. Lời đọc ≈ 22,5–23,1 phút; cộng nghỉ ≈ 26 phút | "bạn ngồi vào ghế trực" (hai nút BÁO LÊN \| CHƯA) |
| CN 22/11 | `mim-siri-susan-bennett` | SIRI Ngoài Đời Thật: Susan Bennett — Giọng Nói Thu Năm 2005, Sáu Năm Sau Mới Vang Lên Trong iPhone | 2.156 âm tiết, 7 chương. Lời đọc ≈ 10,0–10,3 phút; cộng nghỉ ≈ 11,5 phút | "tua ngược cuộn băng": 2011 → 2005 → 2003, rồi tua xuôi về hôm nay |

**Kiểm tra lộ trình:** cả bốn dạng đều khác 19 dạng MIM đã dùng và khác nhau từng đôi. Không bài nào có câu "trả lời ba câu hỏi"; `script_lines.py` có chặn cụm này.

**Lý do chọn:**
- **Mỏ neo người Việt đã biết:**
  - Siri và Steve Jobs có nhu cầu tiếng Việt cao nhất trong bảng.
  - Oppenheimer là phim chiếu rạp lớn năm 2023.
  - Kẻ Hủy Diệt cộng cả hai phần có hơn 1,1 nghìn lượt.
  - Google Maps là app ai cũng dùng.
- **Mỗi bài có một người thật và một ngày giờ cho cold open:**
  - 16/07/1945 lúc 05:29:45
  - Đêm 31/08 rạng 01/09/1983
  - Đêm 25 rạng 26/09/1983
  - 04/10/2011
- **Ảnh tự do có mặt người thật cho thumbnail ở 3/4 bài:** Feynman, Reagan, Bennett.
- **Cơ chế chuỗi:** KAL 007 (T4) và Petrov (T6) cách nhau 3 tuần năm 1983. Bài T4 kết bằng câu nối sang bài T6, nên người xem có lý do xem tiếp hai đêm liền.
- **Xếp lịch:** Petrov không đặt ngay sau Apollo 1202 (15/11), vì hai bài cùng mô-típ "máy báo động, người quyết". Bài Petrov kể chiều ngược lại (máy sai, người không tin) và chỉ nhắc lại Apollo một câu.
- **Không trùng:**
  - Không có Long nào kể Petrov, Feynman/Los Alamos, KAL 007/GPS hay Siri/Bennett.
  - ELIZA, Daisy và "máy tính người" ở Langley đã có trong Long cũ. Bốn bài mới chỉ nhắc lại tối đa một câu.

## 4. Trạng thái file

- Mỗi slug có đủ `script.md`, `factcheck.md`, `chNN.json`, `gen_scenes.py`, `spec.json`. Mỗi dòng trong factcheck là một khẳng định, kèm URL đã mở ngày 23/10/2026.
- `spec.youtube` có:
  - `publish_at`
  - `playlist: "Công Nghệ Quanh Ta"`
  - accent riêng: #f59e0b, #34d399, xanh/đỏ của Petrov, #f472b6
- Đã chạy cả ba bước, kết quả:
  - `script_lines.py`: qua cổng integrity.
  - `gen_scenes.py`: không còn neo lỗi.
  - `studio_lint.py`: **0 lỗi, 0 cảnh báo** ở cả 4 bài.
- Quét `youtube.*` tìm `< > CẦN WebFetch factcheck data/long "tìm kiếm" agent`: sạch.

## 5. Nguồn yếu và rủi ro (đọc trước khi duyệt)

**Oppenheimer:**
- Giờ nổ 05:29:45 chỉ có một nguồn (DOE 1995). Có nguồn ghi 5:29:21. Không mở được báo cáo LA-6300-H (OSTI từ chối kết nối).
- Vai Jack Quaid đóng Feynman chỉ có một bài giải trí (Looper). Chi tiết này chỉ hiện trên màn hình, không đọc.
- Hồi ức của Feynman (thẻ màu, 9 bài trong 3 tháng) chỉ có một nguồn. Lời đọc nói "theo Feynman" hoặc nêu cả hai phiên bản.
- Tổng thời lượng cộng nghỉ khoảng 27 phút. Muốn về 26 phút thì bỏ khoảng 30 dấu `‖`.

**KAL 007:**
- Báo cáo ICAO 1993 chỉ đọc được qua bản đăng lại của bên thứ ba, không phải icao.int.
- Con số hơn 600 km (350 NM) lúc trúng tên lửa chỉ có trong phụ lục phân tích của Nga.
- Tiêu đề đã bỏ chữ "miễn phí", vì thông cáo 16/09/1983 (do Larry Speakes đọc) không có chữ này. "Free of charge" chỉ xuất hiện năm 2000.

**Petrov:**
- Lời kể của Petrov tự mâu thuẫn (4 hay 5 tên lửa; số tầng kiểm tra). Lời đọc nói thẳng từng chỗ lệch.
- Nguyên nhân kỹ thuật chỉ dựa vào một câu của Podvig và một câu của Guardian. Ý "mây cao, quỹ đạo Molniya" là chưa kiểm được và lời đọc nói rõ như vậy.
- Không mở được Washington Post 1999, NYT 2017 và DoD 3000.09. Phần kết thay bằng Điều 14 Đạo luật AI của EU, đọc qua trang chép lại vì EUR-Lex không tải được.
- **Thumbnail không có mặt Petrov** (mọi chân dung đều BY-SA). Đề xuất dùng chữ "СТАРТ" đỏ cộng hai nút, hoặc ảnh bia tưởng niệm (PD).

**Siri:**
- Gần như mọi chi tiết về bà Bennett đến từ CNN 2013 (cộng VOA 2018). Apple không xác nhận, và chuyên gia pháp y âm thanh do chính CNN thuê. Bà Bennett còn sống: mọi câu về bà đều nói qua nguồn.
- Giờ 10:00 và câu hỏi thời tiết đầu tiên chỉ có trong ghi chép trực tiếp của MacRumors (thứ cấp).
- Ngày app Siri lên App Store chỉ có TechCrunch.
- Bài VOA và Apple ML Journal mới đọc qua bản tóm tắt, cần mở lại bằng trình duyệt.

## 6. Việc còn lại trước pha dựng (cần chủ kênh duyệt)

1. Duyệt 4 tiêu đề và thứ tự lịch.
2. Đọc lại giấy phép từng ảnh qua Commons API, rồi `pexels.py get` các clip đã ghi trong gen_scenes. Sau đó chạy `clip_sheet.py`, loại clip có logo hoặc chữ hãng (đặc biệt điện thoại và phòng thu ở bài Siri).
3. Nghe thử bảng `say`: Feynman, Albuquerque, Osipovich, Speakes, ScanSoft, Nuance, Serpukhov…
4. Làm thumbnail theo công thức CL: một mặt người thật + 3–5 chữ. Bài Petrov dùng phương án chữ.
5. Short phễu: 2–3 Short mỗi Long, gắn "Video liên quan" về Long tương ứng. Riêng `mim-skynet-1997` đã có, gắn về bài Petrov.
