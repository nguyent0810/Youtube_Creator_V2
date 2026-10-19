# Sinh cảnh từ script.md — 6 ticket

Mỗi Long đang viết tay `scenes` trong `data/long/<topic>/gen_scenes.py` (Tam Giác Vàng: `gen_scenes.py` 326 dòng + `gen_scenes2.py`). `script_lines.py` chỉ đổ lời đọc. Đây là nút thắt: khoảng một nghìn dòng mỗi video, trong khi máy dựng mất 3–4 giờ.

Sáu ticket dưới đây làm lệnh sinh cảnh cho **video sau**. Mỗi ticket xong trong một phiên và có pytest. Không sửa `chNN.json` của video đã đăng hoặc đã dựng (yakuza, mafia, shanghai, ripper, kowloon, golden). Không chạy generator lên topic đã có `gen_scenes.py` riêng.

Luật chung: cảnh đa dạng là do người viết đánh dấu, không phải do máy tự chọn một khuôn. Dòng không đánh dấu thành `kinetic` và lệnh in số dòng đó, để khỏi ra một video toàn một kiểu mà không ai thấy.

## T1. Kiểm mỏ neo

Việc: `motion/long/anchors.py` nhận `lines` (đúng dạng `script_lines.parse` trả về) và `scenes`. Soi mọi mốc `at`, `titleAt`, `hitAt`, `countAt`, `hAt`, `zoom` không tính, và `at` nằm trong `rows` / `kin` / `stamp` / `label` / `side.lines`.

Mốc hợp lệ, đúng như README:

- số nguyên `i`: đầu câu i
- `[i, "từ"]` hoặc `[i, "từ", n, lệch]`: chữ đó có trong câu i
- `[i, null, 0, lệch]`: đầu câu i

Lỗi là danh sách chuỗi tiếng Việt (chỉ số câu, chữ neo, tên trường). Không đọc, không ghi `data/long`.

Xong khi: pytest với một chương giả lập thì qua; đổi một chữ neo thành chữ không có trong câu thì có đúng một lỗi; câu trích `q` vẫn tìm được chữ.

## T2. Tách dấu cảnh khỏi lời đọc

Việc: trong `script.md`, cuối câu được phép có một dấu `{...}` . `script_lines.parse` bỏ dấu đó khỏi câu nói (kể cả câu `»` và câu có `‖`), và trả thêm danh sách dấu theo từng chương. Câu không có dấu vẫn là câu nói như hôm nay.

Dấu là một chuỗi ngắn, chưa cần hiểu hết. Ví dụ: `{slam: NÉM BOM}` , `{quote}` , `{file: DÂN QUÂN\nTỰ VỆ}` .

Xong khi: pytest trên một đoạn markdown giả lập. Câu "Súng nổ. ‖ {date: 29.07.1967}" ra lời "Súng nổ." với nghỉ dài, cộng một dấu `date`. Không có dấu `{` nào lọt vào `lines`.

## T3. Dựng cảnh từ dấu

Việc: hàm thuần `scenes_from(lines, marks)` trả `scenes` mà `build_long` đã hiểu. Bảng nhỏ, mỗi kiểu một test:

| Dấu | Cảnh |
|---|---|
| không dấu | `kinetic`, chữ là cụm ngắn cắt từ câu, `at` là chỉ số câu |
| `quote` | `quote`, gắn `qline` đúng câu có `"q"` |
| `slam: CHỮ` | `slam` |
| `date: NHÃN \| 29.07.1967` | `date` |
| `counter: 16 \| TẤN` | `counter` |
| `question: Câu hỏi?` | `question` |
| `chapter: 6 \| MƯỜI SÁU TẤN` | `chapter` |

`at` của cảnh là chỉ số câu mang dấu. T1 phải chấp nhận cả chương này.

Xong khi: pytest từng dòng của bảng. Chương toàn câu không dấu vẫn ra scene, và số cảnh `kinetic` bằng số câu.

## T4. Thẻ hồ sơ qua lint

Việc: dấu `file: TIÊU ĐỀ | mô tả` ra cảnh `type: file`. Tiêu đề dài bị tách bằng `\n` sao cho mỗi dòng vừa lòng thẻ (`lint_html`, slack 4px). Có `stamp` thì bật `ink` và đặt `x,y` trong thẻ không ảnh (mặc định 960, 600). `check_scenes` trả về rỗng.

Xong khi: pytest một tiêu đề ngắn thì một dòng; một tiêu đề dài kiểu "CỬU LONG TRẠI THÀNH" thì nhiều dòng và `check_scenes` im. Con dấu không ink không được phát ra.

## T5. Ảnh chỉ khi có tên và có trong research.json

Việc: dấu thêm được `img:khoá` hoặc `vid:123` . `img` phải là khóa trong `research.json` của topic. Khóa lạ là lỗi, không đổi thành ảnh khác, không bỏ qua. `vid` để nguyên cho bước html (HDR vẫn do `lint_html` bắt lúc dựng).

Xong khi: pytest fixture research hai ảnh. `img:khunsa` gắn đúng file. `img:khong-co` ra lỗi có tên khóa. Cảnh không có `img` vẫn dựng được.

## T6. Lệnh một topic, trên thư mục tạm

Việc: `python motion/long/gen_scenes.py <topic>` đọc `script.md` + `research.json`, ghi `scenes` (và hud/bgm tối thiểu) vào `chNN.json`, giữ nguyên `lines` đã có. Trước khi ghi: chạy T1, T3, T4, T5. Có lỗi thì không ghi và thoát khác 0.

Từ chối nếu `data/long/<topic>/gen_scenes.py` đang tồn tại. In số câu không dấu.

Xong khi: pytest dùng `tmp_path` một chương 6 câu, có file, có ảnh, có một chữ neo sai. Lần sai không tạo json. Lần đúng tạo `ch00.json`, `lines` giữ nguyên, `check_scenes` im. Chạy với topic `golden` thì thoát lỗi và không đổi file golden.
