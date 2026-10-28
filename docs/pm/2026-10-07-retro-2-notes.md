# Ghi chú PM cho retro 2 (đợt C1 · Short tiết kiệm · thumbnail/phụ đề · D1 · MIM #2 · 5 Short teaser) — 07/10/2026

Đầu vào cho agent retro. Luật người dùng (07/10): video đã đăng không sửa; **một lỗi không để lặp lại lần hai** — mỗi mục
phải có biện pháp chặn tận gốc (luật, công cụ, test), và lỗi lặp lại từ retro 1 phải ghi là **lỗi quy trình**.

| # | Việc xảy ra | Đã xử lý | Lặp lại từ retro 1? |
|---|---|---|---|
| 1 | Mở bài "Trong video này, mình sẽ cùng bạn trả lời ba câu hỏi" lặp ở A1, C1, D1, MIM #2 (người dùng góp ý) | RETENTION.md mục "Lời hứa lộ trình" + checklist; D1, MIM #2 đổi trước khi đăng | mới |
| 2 | Slam chờ từ cuối câu → màn trống 1,7–4,2 s (D1 ×4, MIM #2 ×5) | Agent sửa tay từng cảnh | **CÓ — retro 1 mục 4** (luật "neo đầu câu" có nhưng không có công cụ chặn) → cần lint tự động trong build_long `html`: cảnh không nền mà phần tử đầu tiên xuất hiện > 1 s sau đầu cảnh thì báo lỗi |
| 3 | Bộ đếm (counter) đứng ở 0 vài giây → màn hình hiện "+0%" sai nghĩa (MIM #2 ×5) | Agent sửa từng cảnh | mới → cần mặc định engine: counter bắt đầu đếm ở đầu cảnh |
| 4 | Mất dấu tiếng Việt do clip-path/mask (LẦN → LÂN, TIỆM mất dấu) | Agent sửa beat.css / beat.js / casewide.js | **CÓ — retro 1 (lockup brand bị cắt dấu)** → cần ảnh gallery chữ có dấu khó (Ầ Ẫ Ỵ Ệ Ở) cho mọi hiệu ứng, chạy khi sửa engine |
| 5 | Dấu ngoặc kép lớn đè nhãn "GIỌNG ĐỌC MINH HỌA" (lab + chart) | CSS cả hai theme | **CÓ — retro 1 mục 1 (theme gallery chưa làm)** |
| 6 | Mô tả D1 8.199 ký tự > 5.000 → upload bị chặn | describe.py `fit_sources` + test | mới |
| 7 | Console Windows cp1252 làm sập script khi in tiếng Việt (qa_blank, render_lock) | Sửa từng file | **lặp 2 lần trong 1 ngày** → cần một cách chung cho mọi CLI |
| 8 | PM vá file Python qua heredoc bash → `\n`, `\1` bị hỏng (describe.py, gen_scenes.py, render_lock.py) | Sửa tay bằng Edit | **CÓ — đã ghi trong tóm tắt phiên trước** → luật PM: chỉ vá bằng Write/Edit, không heredoc có dấu `\` |
| 9 | Render song song (agent + chuỗi PM) | `factory/render_lock.py` khoá cấp HĐH, gắn vào build_long + stier build, có test | **CÓ — retro 1 mục 9** (giờ mới có công cụ) |
| 10 | Giãn nhịp CK (6 video/24 h) chặn D1 tới 17:19 | Chuỗi tự chờ | mới → lập lịch upload theo quota nhịp từ trước |
| 11 | Ảnh X-4/Friden ghi "Langley/Hampton" nhưng chụp ở Muroc: video dài đã sửa nhãn, Short teaser vẫn ghi sai | PM bắt khi duyệt Short, sửa spec | mới → ghi chú về một ảnh phải đi theo ảnh (spec imgs) sang mọi nơi dùng lại |
| 12 | Short không chạy qa_blank / contact sheet tự động | PM soát tay | mới → thêm vào stier build |
| 13 | Mô tả nhạc theo thể loại, chưa ai nghe (16 bài mới) | — | mới → nghe thử trong bản nháp |
| 15 | Chuỗi đăng D1 thử lại cố định 30×5 phút (2,5 h) nhưng lượt CK mở sau 4,2 h → D1 không lên, rồi chuỗi enqueue 2 Short D1 → Short có thể lên TRƯỚC video dài nó trỏ tới | PM dừng chuỗi trước khi có upload sai, viết lại: chờ không giới hạn, video dài trước, Short sau | mới → `publish_long` / `publish_batch` cần cờ `--wait` tự ngủ tới `next_upload_at` (không để mỗi script tự đoán số lần thử); Short teaser chỉ enqueue khi video dài đã có video_id |
| 16 | MIM #3 có câu lặp nguyên văn ("Anh ta nghi ngờ.") — integrity chỉ bắt ở bước Bundle (sau khi đã render final) | Sửa câu, dựng lại 1 chương | mới → chạy `factory.integrity.check` ngay trong `script_lines.py` (chặn trước TTS) |
| 17 | Khoá render theo chương + chờ 15 s → một lượt nhiều chương giành khoá liên tục, C2 trễ 1,5 h | Khoá lồng được, build_long giữ cả lượt, chờ 5 s, có test | mới (phát sinh từ biện pháp mục 9) |
| 14 | Agent ghi "không có Pexels key" (có PEXEL_KEY trong .local.env) | — | mới → ghi rõ trong brief agent |
