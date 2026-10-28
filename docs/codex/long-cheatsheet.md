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

## Long CK: cảnh biểu đồ (theme "chart", 27/10/2026)

Khung để chép cho CK: `data/long/ck-e6-luong-huu-rut-mot-lan/gen_scenes.py`. Lô từ 18/11 phải theo luật trong `docs/pm/2026-10-27-ck-dung-hinh-hap-dan.md`:
- biểu đồ thật ≥ 35% số cảnh, thẻ chữ (`kinetic`, `question`, `slam`, `myth`) ≤ 25%;
- không quá 2 thẻ chữ liền nhau;
- biểu đồ đầu tiên neo vào câu 1 hoặc câu 2 của CH00 (trước giây 15).

Mọi số liệu tính sẵn trong `gen_scenes` (lấy từ `results.json`). Mốc `at` là `a(line, word)` như các cảnh khác.

| Cảnh | Chữ ký | Dùng khi |
|---|---|---|
| `race` + `abs` (đường) | `{"type":"race","abs":True,"unit":"TRIỆU","xlab":"THÁNG ","xstep":1,"dates":[...nhãn...],"title","range","series":[{"label","color","vals":[...]}],"calls":[{"i","s"?,"text","at"}]}` | Số theo tháng/năm. `calls` = khoanh điểm thứ `i` đang đọc |
| `waterfall` (thác) | `{"type":"waterfall","title","range","unit","start":{"k","v","at"},"steps":[{"k","v":-16,"at"}],"end":{"k","at"},"calls":[{"i","text","at"}]}` | Tổng bị trừ/cộng dần. `i`: 0 = cột đầu, 1..n = bước, n+1 = cột cuối |
| `heat` (lịch nhiệt) | `{"type":"heat","title","range","unit","cols":6,"cells":[{"k":"T1","v","note"?,"at"?}],"total":{"label":"CẢ NĂM","at"},"calls":[{"i","text","at"}]}` | 12 tháng / 12 mục. Ô sáng lần lượt, bộ đếm cộng dồn |
| `stack` (cột chồng) | `{"type":"stack","title","range","unit","keys":[{"k":"VỢ"},{"k":"CHỒNG"},{"k":"QUỸ CHUNG"}],"groups":[{"k":"50/50","vals":[..],"at"}],"calls":[{"i","text","at"}]}` | So sánh vài cách chia. Mỗi cột ≤ 4 phần |
| `bars`, `counter`, `units`, `timeline`, `ledger` | như các Long CK trước | |

- `range` là **dòng chữ phụ** cạnh tiêu đề, ví dụ `"TRIỆU ĐỒNG · VÍ DỤ GIẢ ĐỊNH"`. **Không phải khoảng trục.** Truyền mảng `[0, 30]` thì engine in nguyên "0,30" lên màn hình (lỗi F1, 27/10). Trục tự tính từ số liệu.
- `waterfall`: `start.v` là số **dương** (tổng ban đầu), `steps[].v` âm là bị trừ, dương là được cộng.
- `race` không dùng cho chuỗi gần như toàn số 0. Mốc ngày thì dùng `timeline`. `dates` phải là ngày ISO ("2025-04-09") hoặc dùng `xstep` + `xlab` (nhãn "THÁNG 1, 2…"). Nhãn chữ như "ĐẦU 2000" không hiện đúng, với dạng đó thì dùng `bars`.
- `dots` là `{"total": 100, "cols": 20, "groups": [{"from": 0, "n": 40, "cls": "red", "label": "…", "at": a(…)}]}`, mỗi chấm một người. Không dùng `items`.
- **`check.py` phải tính lại độc lập và kiểm tính khớp.** Ví dụ: các lớp của thác cộng đủ tổng. Chỉ so số gõ cứng là không đủ: F2 từng để lọt một hoá đơn hụt 5 triệu không tên (27/10).
- **Không thêm câu lặp để đủ âm tiết.** F1 W1-1b từng đọc lại 4 câu trần theo vùng ngay sau khi vừa đọc xong.
- Chữ trên biểu đồ in hoa, ≤ 26 ký tự cho `title`, ≤ 18 ký tự cho `text` của `calls`.
- Xem mẫu đã render: `python motion/long/chart_demo.py waterfall|heat|stack|line-calls`. Không cần render lại.

## Long CK: ảnh nhân vật và ảnh tĩnh (27/10/2026)

**Ảnh nhân vật VÍ DỤ GIẢ ĐỊNH** (chị Lan, anh Minh…) do Grok Bot vẽ. Ghi prompt vào `data/long/<topic>/ai_prompts.md`, mỗi mục một tiêu đề `## ai_NN.png — …`.
- Tối đa 8 ảnh mỗi bài.
- Nhân vật là người hư cấu nên **vẽ được mặt**.
- **Dòng đầu file là "hồ sơ nhân vật":** tuổi, dáng, tóc, trang phục, màu chủ đạo. Mọi prompt chép lại nguyên hồ sơ này để gương mặt giống nhau suốt video (thẻ `object_continuity`).
- Phong cách chung: ảnh minh hoạ điện ảnh, bối cảnh Việt Nam đời thường, ánh sáng ấm, khung 16:9, chừa khoảng trống một bên để đặt chữ.
- Cấm:
  - chữ, logo hay biển hiệu đọc được;
  - tên bệnh viện, ngân hàng hay công ty;
  - tiền giấy thấy rõ mệnh giá;
  - cảnh máu hoặc bệnh nặng.
- Trong `gen_scenes`: ảnh AI dùng `"EXT:ai:ai_NN"`. Cảnh `photo` của ảnh AI phải có `"credit": False`, và nếu có mặt người thì thêm `"focus": [x, y]` vào mặt.
- Mỗi chương dùng 1–2 ảnh nhân vật. Mỗi ảnh hiện ≤ 3 lần trong cả bài. Ảnh nhân vật **không thay biểu đồ**: nó mở cảnh, còn số liệu vẫn nằm ở biểu đồ ngay sau đó.

**Ảnh tĩnh cho hấp dẫn.** Cảnh `photo` có thêm 2 trường tuỳ chọn, lấy từ thẻ thư viện:

| Trường | Thẻ | Dùng khi |
|---|---|---|
| `"reveal": {"kind": "circle"\|"wipe", "at": a(…), "d": 0.9}` | `image_reveal` / `mask_reveal` | Ảnh mở dần, `circle` mở từ tiêu điểm. Dùng cho ảnh đầu chương hoặc khoảnh khắc hé lộ |
| `"zoom": {"x": 0.62, "y": 0.4, "z": 1.6, "at": a(…), "d": 1.2}` | `camera_zoom` | Phóng vào chi tiết (tờ hoá đơn, phong bì, màn hình) đúng lúc lời đọc nhắc tới |

Ken Burns có sẵn: `"move": "in"|"out"|"pan"`, kèm `"focus"`. Không để hai ảnh tĩnh liền nhau cùng một kiểu chuyển động.
- `youtube.category` phải là **mã số** "27" (Education), không phải chữ "Education": YouTube trả HTTP 400 (F1, 27/10).
