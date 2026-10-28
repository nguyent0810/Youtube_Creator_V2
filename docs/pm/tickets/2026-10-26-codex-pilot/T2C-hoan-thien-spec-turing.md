# T2C — Hoàn thiện spec và phát âm cho `mim-turing-bombe` (vòng ngắn)

Claude đã review bản T2B: nội dung đạt. Ticket này chỉ sửa các mục còn thiếu bên dưới. **Không viết lại kịch bản.** Không render, không upload, không chạy `thumb.py`.

**Kết quả:** `docs/pm/tickets/2026-10-26-codex-pilot/T2C-ket-qua.md`

## 1. Tiêu đề

- **Tiêu đề chính:** "NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing: Bombe" có hai dấu hai chấm. Đổi `TITLE` thành **"NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing Và Bombe"**, giữ ≤ 60 ký tự.
- **Phương án dự phòng:** thêm 1–2 phương án ≤ 60 ký tự.
- **`script.md`:** sửa dòng tiêu đề đầu file cho khớp.

## 2. `spec.youtube` đầy đủ như mẫu `data/long/mim-ke-huy-diet-petrov/gen_scenes.py`

Viết vào `make_spec()` trong `gen_scenes.py`, không sửa tay `spec.json`:

| Trường | Yêu cầu |
|---|---|
| `publish_at` | `"2026-11-23T13:00:00Z"` |
| `playlist` | `"Công Nghệ Quanh Ta"` |
| `category` | `"28"` |
| `thumb` | `"t1.jpg"` |
| `summary` | 2–3 câu hấp dẫn về nội dung, không lộ kết |
| `more` | Ghi chú trung thực cho người xem: lời trích là bản dịch; ảnh và clip có nhãn MINH HỌA chỉ để minh hoạ; phim chỉ được nhắc, không dùng hình phim |
| `chapter_titles` | Đủ `ch00`–`ch07`, tiếng Việt có dấu, khớp mốc chương |
| `sources` | Mọi URL **công khai** đã dùng trong `factcheck.md` (khoảng 15–20 URL), không ghi chú |
| `tags` | 10–15 tag |
| `hashtags` | 3–5 hashtag, trong đó có `CôngNghệQuanhTa` và `MindInTheMachine` |
| `video_credits` | Ghi công ảnh Commons (tác giả, giấy phép) và "Video minh hoạ: Pexels" |

**Chuỗi cấm:** không đưa `<`, `>`, "CẦN", "factcheck", "data/long", "agent", "tìm kiếm" vào bất kỳ trường công khai nào.

## 3. Bảng phát âm `SAY`

Thêm `"say": SAY` vào `make_spec()`. Xem mẫu `data/long/mim-google-maps-kal007/gen_scenes.py`: key viết thường, hoặc `"=Từ"` khi cần khớp đúng hoa/thường. Giọng Việt đọc kém các tên nước ngoài, nên phải phiên âm các từ sau (đã đếm trong lời đọc):

- **Tên và địa danh:** Turing, Enigma, Bletchley, Park, Bombe, Bombes, Welchman, Warsaw, Rejewski, Paris, Clarke, Eastcote, Gordon, Marian, Henryk, Zygalski, Jerzy, Różycki (nếu có), Wylie, Millar, Hugh, Alexander, Stuart, Milner-Barry, Winston, Churchill, Gustave, Bertrand, Alastair, Denniston, Dilly, Knox, Sachsen, Agnus Dei, Agnes, Stanmore, kryptologiczna, Hut.
- **Thuật ngữ:** crib, board, plugboard, U-boat, sheet / key sheet.
- **Viết tắt:**
  - TNMOC → "Bảo tàng Máy tính Quốc gia Anh"
  - GCHQ → "gi xi ết-chờ kiu"
  - GC&CS / GC, CS → đọc tự nhiên
  - BTM → "bi ti em"
  - WRNS → "Ren"
- **Con số:** "158.962.555.217.826.360.000" → "khoảng một trăm năm mươi chín tỷ tỷ". Màn hình vẫn hiện số đầy đủ.

**Cách kiểm:** chạy lại `tts` (chỉ những câu đổi cách đọc mới đọc lại), rồi nghe thử `output/long/mim-turing-bombe/ch01` (số lớn) và một câu có "Bletchley". Không mở được file âm thanh thì ghi rõ trong báo cáo.

## 4. Cổng

Chạy lần lượt `gen_scenes.py`, `build_long.py tts`, `build_long.py html` (đủ 8 chương), rồi `python scripts/long_gate.py mim-turing-bombe --min-syl 1900`. Cổng cuối phải ra **ĐẠT**.
