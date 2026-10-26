# Cheatsheet dựng Long MIM (cho Codex, đọc thay engine)

**Không đọc** `motion/long/build_long.py`, `motion/hf/assets/engine/*`, `motion/stier/*`, `factory/*`, `pexels.py` hay thư mục của bài khác. Mọi thứ cần biết đều có trong cheatsheet này và trong **một file mẫu**:

> `data/long/mim-katherine-johnson/gen_scenes.py`. Bài này đã qua cổng, render và đăng. **Chép nguyên file này làm khung.** Giữ các helper ở dòng 57–163 và `main()`. Chỉ thay phần nội dung bên dưới.

## Thay những gì trong khung

| Khối | Thay bằng |
|---|---|
| `TOPIC`, `TITLE` (≤ 60 ký tự, một dấu `:`) | Của bài mới |
| `SAY` | Phiên âm mọi tên nước ngoài, viết tắt và số lớn trong lời đọc. Khoá viết thường. Ví dụ: `"nasa": "Na-sa"` |
| `IMGS` | Ảnh Commons `"File:…"` (đã kiểm PD/CC0/CC BY) hoặc `"EXT:ai:ai_NN"` cho ảnh AI |
| `AI_PATH`, `STAND` | Số ảnh AI của bài (≤ 6); `STAND` = ảnh tư liệu thay tạm cho từng ảnh AI |
| `GEO` | Bản đồ: `countries`, `context`, `bbox [lon_min, lat_min, lon_max, lat_max]`, `pins [{name, lon, lat, label}]` |
| `CHAPTER_TITLES` | `ch00`–`ch07`, tiếng Việt có dấu |
| `LEDGER`, `ROWS` | Mô-típ của bài: một tiêu đề, mỗi chương thêm 1 dòng |
| `ch00()`–`ch07()` | Cảnh của từng chương (mục dưới) |
| `make_spec()` | Đủ 11 trường `youtube`, đổi `publish_at`; giữ `"say": SAY`, `imgs`, `geo` |

## Helper: chữ ký và ý nghĩa

**Neo thời gian:** `a(line, word)` neo cảnh vào câu `line` của chương, tại từ `word`. `word` phải là chữ **có thật trong câu đó**, không phải số và không phải chữ có trong `SAY`.

| Helper | Dùng khi |
|---|---|
| `chapter(no, k, title, sub, bg, title_at)` | Cảnh đầu mỗi chương. `k = "CHƯƠNG MỘT"`; `sub` = mốc có nguồn; `bg` = key ảnh |
| `photo(img, at, key, value, kin=None)` | Ảnh tư liệu hoặc ảnh AI. Ảnh AI tự có `illus` + `credit: False` |
| `print_scene(img, at, head, key, value)` | Ảnh đặt như tờ in, có cột ghi chú |
| `broll(vid, at, text)` | Clip Pexels (id số), có nhãn VIDEO MINH HỌA |
| `kinetic(at, text, small=None)` | Chữ lớn động |
| `slam(at, text, sub)` | Một con số hoặc cụm từ đập mạnh |
| `date(at, day, d, sub)` | Mốc ngày lớn. `d = "20.02.1962"` (chữ số và dấu chấm); chữ thì để vào `day` |
| `counter(at, to, suffix, label, frm=0, year=False)` | Số đếm. Năm thì `year=True` |
| `timeline(at, bg, items)` | Dòng thời gian (xem cách dùng trong mẫu) |
| `org(at, nodes)` | Sơ đồ người hoặc tổ chức |
| `question(at, text)` | Câu hỏi treo |
| `ledger(n, at)` | Hiện mô-típ tới dòng `n` |
| `{"type": "map", "at": …, "geo": "<key GEO>"}` | Bản đồ; mẫu có ở `ch01`/`ch05` của khung |

## Luật cảnh (cổng `long_gate.py` sẽ chặn nếu sai)

- 60–80 cảnh, trung bình ≤ 9 giây/cảnh, mỗi chương ≥ 5 loại cảnh.
- Không dòng chữ hiển thị nào lặp > 2 lần. Mô-típ chỉ qua `ledger`.
- Một clip dùng ≤ 2 lần, ít nhất 6 clip khác nhau. Một ảnh dùng ≤ 3 lần.
- Mỗi cảnh minh hoạ **câu đang đọc**.

## Clip Pexels

- Tải: `python motion/long/pexels.py get <topic> <id> …`. Chỉ dùng id đã ghi trong `facts.md`. Từ 26/10/2026 tải thẳng theo id, không cần `search` trước.
  - Lệnh in "không có bản ngang ≤1920 -- bỏ qua" nghĩa là clip dọc. Phải thay bằng clip ngang. Tìm bằng `pexels.py search <topic> "từ khoá"`, rồi `get` id mới.
- Soát: `python motion/long/clip_sheet.py <topic>`, mở `output/long/<topic>/qa_clips.jpg` xem. Clip lộ chữ, logo hoặc sai nghĩa thì thay.

## Bài học Moneyball (26/10/2026)

- **Vòng kịch bản (W1):** phải chạy `script_lines.py` và `studio_lint.py --strict` rồi sửa hết lỗi câu > 35 tiếng **ngay trong W1**. Tách câu sau khi đã dựng cảnh thì mọi neo phía sau bị lệch, sửa rất tốn.
- **Neo phải tăng dần.** Cảnh sau phải neo vào từ đứng **sau** neo của cảnh trước, tính theo (câu, vị trí từ). Neo ngược hoặc trùng thì engine báo "cảnh quá ngắn".
- **Không neo vào chữ số.** Ví dụ "11" không khớp với "11–0".
- **"Qua html" nghĩa là** in đủ 8 dòng `chNN: … -> …html` và không có `Error`. Chạy bản `--standin` mà không đọc lỗi thì chưa tính là qua.

## Bài học Social Network và Moneyball sau render (26/10/2026)

- **Ghim trong cảnh `map` phải trùng tên ghim trong `GEO`.** Ví dụ `{"name": "Harvard"}` thì `GEO` cũng phải có `"name": "Harvard"`. Sai tên thì engine lỗi và **cả chương đứng hình ở thẻ chương** (72 giây). `long_gate.py` giờ chặn lỗi này.
- **Cảnh `question` hay `slam` không được kéo dài.** Cảnh kế tiếp phải neo vào câu ngay sau, không được để một thẻ chữ tĩnh 20 giây. Claude chạy thêm `scripts/freeze_check.py` sau render: đứng hình > 12 giây là trượt.

- **Ảnh dọc có mặt người** (chân dung, ảnh thẻ) khi đưa vào cảnh `photo` hay `chapter` phải có `"focus": [0.5, 0.12–0.2]`, để khung 16:9 lấy đúng vùng mặt. Thiếu `focus` thì engine cắt giữa ảnh: bài Macintosh chỉ còn vest và tay của Jobs. `long_gate.py` cảnh báo trường hợp này.

## Thứ tự lệnh

Đặt `PYTHONIOENCODING=utf-8` cho mọi lệnh.

1. `python motion/long/script_lines.py <topic>`: đưa lời đọc từ `script.md` vào `chNN.json`.
2. `python data/long/<topic>/gen_scenes.py`, rồi chạy lại `script_lines.py`. `gen_scenes` ghi đè `chNN.json` không kèm `lines`.
3. `python motion/long/studio_lint.py <topic> --strict` phải ra **0 lỗi**.
   - Câu quá 35 tiếng thì **tách thành 2 câu** trong `script.md`, giữ nguyên ý, kể cả khi kịch bản đã được duyệt.
   - Tách câu xong, kiểm lại neo `a(line, word)` của các câu phía sau trong chương đó, vì số thứ tự câu đã lệch.
4. `python motion/long/build_long.py <topic> tts` cho **đủ mọi chương**: phải có `output/long/<topic>/chNN/timing.json` cho từng chương. Rồi chạy `… html`. Nếu ảnh AI chưa có thì chạy `gen_scenes.py --standin` để soát html, sau đó chạy lại bản thật.
5. `python scripts/long_gate.py <topic> --min-syl 1900` phải ra **ĐẠT**.
