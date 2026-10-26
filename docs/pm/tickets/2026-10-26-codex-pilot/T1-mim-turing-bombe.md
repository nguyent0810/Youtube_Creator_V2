# T1 — Long MIM: NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing và cỗ máy Bombe

**Giao cho:** Codex (thử nghiệm vai trò sản xuất). **Đọc `AGENTS.md` trước.** **Kết quả ghi vào:** `docs/pm/tickets/2026-10-26-codex-pilot/T1-ket-qua.md`.

## Mục tiêu

Dựng **một Long MIM dài 9–12 phút**, đi đến hết bước `html` + clip sheet + thumbnail. **Không render video**: Claude sẽ render, review rồi đăng.

| Mục | Giá trị |
|---|---|
| Topic (thư mục) | `mim-turing-bombe` → `data/long/mim-turing-bombe/` |
| Lịch | Thứ Hai 23/11/2026 20:00 VN. Ghi `publish_at` là `2026-11-23T13:00:00Z` trong `spec.youtube` theo mẫu bài Petrov |
| Playlist | "Công Nghệ Quanh Ta" (như các Long MIM khác) |
| Giọng | Thanh Bình (dẫn) và Ngọc Huyền (lời trích `»`), như mẫu Petrov |
| Mẫu cấu trúc | `data/long/mim-google-maps-kal007` (bài 9–12 phút, 7 chương) và `data/long/mim-ke-huy-diet-petrov` |

## Nội dung

**Mỏ neo:** phim *The Imitation Game* (2014); tên tiếng Việt khi chiếu ở VN cần kiểm, dự kiến "Người Giải Mã". Phim chỉ nhắc bằng lời và chữ, **không dùng hình phim**.

**Người thật và mốc thời gian:**
- Alan Turing; bản thiết kế Bombe (1939–1940) phá khoá Enigma tại Bletchley Park.
- Cold open có ngày giờ cụ thể. Ví dụ: chiếc Bombe đầu tiên, "Victory", bắt đầu chạy năm 1940; ngày chính xác cần kiểm.

**Khoảng cách phim và đời thật là móc giữ chân.** Phim kể máy tên "Christopher" do một mình Turing làm. Đời thật có Gordon Welchman (diagonal board), các kỹ sư British Tabulating Machine Company (Harold "Doc" Keen), thợ máy và người vận hành (WRNS), và nền tảng từ bom Ba Lan "Bomba" (Rejewski, 1938). Mỗi khác biệt chỉ đọc khi có nguồn.

**Không trùng:** Long `mim-ai-70` đã kể phép thử Turing; Short `mim-turing-1950-loi-doan` cũng vậy. Bài này về **Bombe/Enigma**; phép thử Turing chỉ được nhắc tối đa một câu.
- Grep `data/long/mim-*/script.md` và `data/stier/specs/*turing*` để kiểm trùng.

**Lộ trình:** chọn một dạng **chưa dùng** (danh sách các dạng đã dùng có trong `script.md` của bài Petrov, mục "Giữ chân").

**Tiêu đề:**
- `titles[0]` ≤ 60 ký tự, theo khuôn "NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing …".
- Đưa 2 phương án dự phòng vào `titles[1..2]`.

**Ảnh:**
- Chỉ dùng PD, CC0, CC BY. Đọc lại `LicenseShortName` trên Commons trước khi dùng.
- Ảnh Bombe/Enigma thường là CC BY-SA, nên phải tránh.
- Ảnh chân dung Turing thời trẻ có thể là PD; phải kiểm.
- B-roll Pexels: không lộ logo, không gắn tên người thật lên người lạ.

**Thumbnail:**
- Tạo `motion/long/thumbs/mim-turing-bombe_t1.html`, theo mẫu `mim-oppenheimer-feynman_t1.html`.
- Có mặt Turing nếu có ảnh tự do; chữ ≤ 5 từ, có năm.
- Chạy `thumb.py`, rồi soi `t1_small.jpg`.

## Cổng phải qua trước khi báo xong

1. `python motion/long/script_lines.py mim-turing-bombe` qua cổng integrity.
2. `python data/long/mim-turing-bombe/gen_scenes.py` chạy sạch.
3. `python motion/long/studio_lint.py mim-turing-bombe --strict` ra 0 lỗi.
4. `python motion/long/build_long.py mim-turing-bombe tts`, rồi `... html`: hết lỗi, ghi lại thời lượng.
5. `python motion/long/clip_sheet.py mim-turing-bombe`, xem ảnh và thay clip sai.
6. Quét `spec.youtube` và mô tả không còn các chuỗi cấm (xem `AGENTS.md`).
7. **Không** chạy `render` hoặc `final`. **Không** upload.

## Báo cáo (`T1-ket-qua.md`)

- Tiêu đề chọn, thời lượng, số chương, dạng lộ trình.
- Kết quả từng cổng.
- Khẳng định không kiểm được, kèm cách đã xử lý.
- Ảnh đã dùng và giấy phép.
- Đường dẫn clip sheet và thumbnail.
- Thời gian làm.
