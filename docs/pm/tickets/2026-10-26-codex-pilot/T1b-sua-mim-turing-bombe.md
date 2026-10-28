# T1b — Sửa Long `mim-turing-bombe` theo review của Claude

**Đọc lại `AGENTS.md`.** **Kết quả ghi vào:** `docs/pm/tickets/2026-10-26-codex-pilot/T1b-ket-qua.md`. Vẫn **không render** và **không upload**.

Bản T1 qua hết cổng tự động nhưng **chưa đạt chuẩn đăng**. Cổng chỉ là mức sàn, không phải thước đo chất lượng. Sửa đủ 4 nhóm lỗi dưới đây.

## 1. Sự thật

- **Ngày ở CH00.** CH00 đọc "Ngày 18 tháng 3 năm 1940", trong khi `factcheck.md` ghi là không chốt ngày. Hai chỗ mâu thuẫn nhau. Cách xử lý:
  - Tìm và **mở được** một nguồn ghi ngày, ví dụ Bletchley Park, Turing Archive hoặc Crypto Museum. Có nguồn thì giữ ngày và thêm dòng nguồn vào factcheck.
  - Không tìm được nguồn thì chỉ nói "tháng 3 năm 1940".
- **Thời điểm có WRNS.** Ở CH00, WRNS được kể cùng danh sách năm 1940. Phải kiểm thời điểm Wrens bắt đầu vận hành Bombe và nói đúng mốc đó.
- **Khẳng định mới.** Mọi khẳng định thêm vào phải có một dòng trong factcheck kèm URL đã mở được.

## 2. Kịch bản: viết cho người xem, không viết cho lint

- **Bỏ câu rỗng nghĩa.** Xoá các câu ngắn chỉ chèn vào để đủ tỉ lệ câu ngắn. Ví dụ:
  - "Rất chậm."
  - "Không có thời gian chờ."
  - "Mâu thuẫn là dấu hiệu tốt."
  - "Không hề tức thì."
  - "Đó là lợi thế lớn."
  - "Việc ấy rất cụ thể."
  - "Đó là câu hỏi khó."
  - "Phần còn lại mới đáng xem."

  Câu ngắn chỉ đặt sau một phán định hoặc một khoảnh khắc cảm xúc; xem `motion/long/RETENTION.md`.
- **Viết lại cold open (CH00) thành một cảnh có căng thẳng.** Bỏ kiểu liệt kê "Có Alan Turing. Có Welchman…" và bỏ câu meta "Hôm nay mình không kể phép thử Turing".
  - Ví dụ hướng đi: một ngày năm 1940, điện Enigma chặn được đang chất đống, khoá đổi lúc nửa đêm, và cỗ máy mới phải tìm ra khoá trước khi tin hết giá trị.
  - Câu hỏi treo phải trả lời ở chương sau.
- **Mỗi chương có ít nhất một chi tiết cụ thể, có nguồn.** Gợi ý:
  - một crib thật đã được tài liệu hoá, như mẫu bản tin thời tiết, nếu có nguồn;
  - Bombe chạy những gì và mất bao lâu cho một lần chạy, nếu có nguồn;
  - Rejewski và bomba năm 1938;
  - "Doc" Keen và nhà máy ở Letchworth, nếu có nguồn;
  - số lượng Bombe về cuối chiến tranh, nếu có nguồn;
  - Wrens và nơi đặt máy.

  Không có nguồn thì không dùng, nhưng phải cố tìm. Kể bằng cảnh, người và vật; không giảng lý thuyết suông.
- **Giữ khuôn chung:** 9–11 phút, mô-típ "sáu răng của chiếc khoá", tiêu đề hiện tại.

## 3. Hình: đổi cảnh dày hơn nhiều

- **Bản T1:** 18 cảnh cho 9 phút. Gồm 8 `chapter`, 8 `kinetic`, 8 `slam`, 2 `print`; khoảng 30 giây mới đổi cảnh, toàn chữ.
- **Mục tiêu:** khoảng **45–60 cảnh**, mỗi cảnh trung bình 8–12 giây, mỗi chương có ít nhất 4 loại cảnh. Đối chiếu với `data/long/mim-ke-huy-diet-petrov/ch*.json` để thấy mật độ và loại cảnh. Dùng thêm:
  - `timeline` (1938 → 1939 Pyry → 1/1940 Pháp → 3/1940 Victory …);
  - `map` hoặc `geo` (Warsaw/Pyry → Pháp → Bletchley Park), nếu engine hỗ trợ; xem các bài mẫu;
  - `org` (dây chuyền người: Ba Lan → Turing/Welchman → BTM/Keen → Wrens);
  - `counter` (chỉ với số có nguồn; năm thì khai `"year": true`);
  - `quote` (chỉ trích dẫn có nguồn);
  - B-roll Pexels qua `"vid"`. Chọn cảnh trung tính: máy đánh chữ, rơ-le, dây điện, mã Morse, sóng radio, biển đêm, bàn làm việc cũ. Không logo, không gắn tên người thật lên người lạ, không cảnh chiến tranh dàn dựng gây hiểu nhầm là tư liệu.
- **Ảnh tư liệu PD/CC0/CC BY trên Commons**, kiểm `LicenseShortName` trước khi dùng:
  - Rejewski;
  - toà nhà Bletchley Park;
  - ảnh Wrens vận hành Bombe (ảnh Crown copyright đã hết hạn thường là PD);
  - ảnh máy Enigma có giấy phép PD hoặc CC BY.

  BY-SA và GFDL vẫn bị cấm.
- **Kiểm clip:** chạy `clip_sheet.py`, mở ảnh xem và thay clip sai nghĩa.

## 4. Cổng (như T1) và báo cáo

- **Cổng:** `script_lines.py`, `gen_scenes.py`, `studio_lint.py --strict` (0 lỗi), `build_long.py tts`, `build_long.py html`, rồi `clip_sheet.py`.
- **Thumbnail:** bỏ qua `thumb.py` vì sandbox chặn npm; Claude sẽ dựng.
- **Báo cáo `T1b-ket-qua.md`:**
  - số cảnh theo loại, trước và sau;
  - các câu đã bỏ hoặc viết lại;
  - khẳng định mới kèm nguồn;
  - ảnh và giấy phép;
  - đường dẫn clip sheet.
