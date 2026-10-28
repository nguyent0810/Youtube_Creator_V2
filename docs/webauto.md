# webauto: lệnh tự động hoá trình duyệt dùng lại được

`python -m webauto <công cụ> <lệnh>` chạy lại **một chuỗi bước cố định** trên các trang không có API (Google Flow, ChatGPT, Muse AI, TikTok Studio). Không có LLM trong vòng lặp: script mở trang, điền, bấm, chờ, tải về, lưu file. Nhờ đó tốn 0 token cho phần thao tác, và hợp luật README ("Pha sản xuất không được phép cần LLM").

```
python -m webauto --help
python -m webauto flow generate --mode video --prompts-file clips.txt --duration 6 --out output/webauto/flow
python -m webauto chatgpt images --prompts-file images.txt --out output/webauto/chatgpt
python -m webauto chatgpt ask --file docs/pm/some-retro.md          # review, lưu <file>.chatgpt-review.md
python -m webauto muse research --questions q.txt --out docs/research/2026-10-28-muse.md
python -m webauto tiktok list
```

## Cài đặt

```
pip install -e ".[webauto]"        # playwright + mcp
python -m playwright install chrome   # chỉ khi máy chưa có Chrome
```

| Công cụ | Chạy bằng | Cần gì |
|---|---|---|
| `flow` | Playwright, profile riêng `~/.webauto/profiles/flow` | `webauto flow login` một lần (đăng nhập Google, rồi **đóng hẳn** cửa sổ Chrome). Chrome còn chạy nền sẽ khoá profile. |
| `chatgpt`, `muse`, `tiktok` | [Browsentic](https://browsentic.com) điều khiển Chrome thật đã đăng nhập | Extension Browsentic đã ghép cặp; Chrome mở, cửa sổ ở phía trước; tab đã đăng nhập sẵn trang đích. |

Đổi chỗ lưu profile bằng biến `WEBAUTO_HOME`. Đổi lệnh chạy Browsentic bằng `WEBAUTO_BROWSENTIC_CMD` (mặc định `npx -y browsentic@latest mcp`). Profile chứa cookie đăng nhập nên **nằm ngoài repo**, không bao giờ commit.

## Lệnh

### `flow generate`
Tạo ảnh hoặc video trong một dự án Flow mới, tải về `<tên>_<n>_...`.
- `--mode image|video` (mặc định image). Mặc định model: Nano Banana Pro (ảnh), Omni 1.1 Flash (video). `--model` nhận một đoạn tên model.
- `--count 1-4` số kết quả mỗi prompt (mặc định 1), `--duration 4|6|8|10` giây (video, mặc định 6), `--ratio`, `--res`, `--quality 720p|1080p|4K` (chất lượng tải; 720p là bản gốc).
- `--image khung_dau.png` (video): ảnh làm **khung bắt đầu** (image-to-video). Một ảnh dùng cho mọi prompt trong lần chạy.
- File prompt: mỗi dòng `tên | prompt` hoặc chỉ `prompt` (đặt tên `001_<tóm-tắt>`), dòng `#` và dòng trống bị bỏ.
- Flow có thể tính credit (xem dòng "Generating will use N credits" trong popup cài đặt). Video tốn đáng kể: Omni 1.1 Flash 8s x2 báo 24 credit; ảnh Nano Banana 2.1 báo 0 credit, còn Nano Banana Pro (mặc định) chưa đo.

### `chatgpt images`
Mỗi prompt tạo một ảnh bằng ChatGPT (gửi "Create an image: …"), lưu `<tên>.png`. File đã có thì bỏ qua, nên chạy lại sau khi gián đoạn không tạo trùng. Cần quy tắc Browsentic `file-download` = Allow. `--wait`, `--gap`, `--limit`.

### `chatgpt ask`
Gửi `--prompt`, hoặc nhờ review một `--file` (kèm `--instruction`, mặc định là yêu cầu review phản biện tiếng Việt), rồi **lưu câu trả lời thành markdown cho agent đọc**. `--from-chat URL` chỉ đọc lại một cuộc trò chuyện đã có (không gửi gì), dùng khi lần chạy trước bị ngắt.

### `muse research`
Hỏi Muse AI (muse.ai) một danh sách câu hỏi trong **một side chat mới**, chờ từng câu trả lời xong và gom tất cả vào một file markdown. Câu trả lời lấy bằng nút "…" > Copy rồi đọc clipboard Windows (đọc văn bản trang không đủ tin cậy với câu trả lời dài). `--adopt-first` dùng tab/side chat đang mở nếu câu 1 đã gửi tay.

### `tiktok list | create | update | delete`
Thao tác trên kênh **đang chạy thật**, nên có chốt (xem CLAUDE.md: không đăng, không xoá khi chủ kênh chưa nói rõ):
- `create`: mặc định **riêng tư** ("Only you"). Đăng friends/công khai cần `--allow-public`. Mô tả có tiền tố `--marker` (mặc định `TEST-CRUD`; bài thật truyền `--marker ""`).
  - `--schedule "YYYY-MM-DD HH:MM"`: hẹn giờ thay vì đăng ngay. Giờ đọc theo múi giờ trang Studio hiện (`--tz`, mặc định `GMT+7`); phải cách hiện tại 20 phút tới 10 ngày (giới hạn TikTok), phút chia hết cho 5 (bộ chọn chỉ có bước 5).
  - `--ai-label`: bật "AI-generated content" (Settings > Show more).
  - Trước cú bấm không hoàn tác, lệnh **đọc lại từ trang** ngày, giờ, múi giờ, quyền xem và caption; lệch là từ chối và bỏ bản nháp.
  - `--dry-run`: làm đủ mọi bước trừ cú bấm cuối, rồi bỏ bản nháp. Chạy cái này trước mỗi lần đổi giao diện.
  - Ví dụ: `python -m webauto tiktok create --video v.mp4 --caption "..." --privacy public --allow-public --marker "" --schedule "2026-11-05 19:45" --ai-label --dry-run`
- `delete`: cần `--id`; từ chối nếu bài không phải "Only me" (trừ `--allow-public`) hoặc nếu không có **đúng một** dòng khớp id. TikTok giữ bài đã xoá 30 ngày (Activity center > Recently deleted).
- `update`: **chưa kiểm chứng** (xem dưới).

## Đã kiểm chứng và chưa kiểm chứng

| | Trạng thái |
|---|---|
| `flow generate` ảnh, video, image-to-video | Đã chạy thật. |
| `chatgpt images`, `chatgpt ask` (kể cả `--from-chat`) | Đã chạy thật. |
| `muse research` | Chạy thật ở chế độ `--adopt-first`. Luồng tự mở side chat mới **chưa** kiểm chứng đủ. |
| `tiktok list`, `tiktok delete` | Đã chạy thật (xoá một bài test Only me). |
| `tiktok create` | Các bước đã chạy tay (tạo bài test Only me); chưa chạy bằng lệnh này. |
| `tiktok create --schedule/--ai-label` | Bộ chọn ngày, giờ, nhãn AI đã soát tay trên Studio 28/10/2026 (selector `DatePicker__day[aria-label*="November 5th, 2026"]`, `TimePicker__item[aria-label="Hours 19"]`); logic chốt có test; **chưa** chạy `--dry-run` qua Browsentic. |
| `tiktok update` | Chưa thành công: text gõ vào được nhưng caption trên máy chủ không đổi. TikTok chỉ cho sửa caption một lần mỗi ngày mỗi bài, nên lần Save đầu có thể đã dùng hết lượt. |

## Bài học (đừng lặp lại)

- **Cột giờ của bộ chọn hẹn giờ bỏ qua click giả** (cột phút thì nhận): phải cuộn tới rồi `page_trustedClick` vào giữa nút. Chọn xong nhãn ô giờ đổi (`19:45`), dùng chính chữ đó để kiểm.
- **mcp ≥ 2.x đổi `CallToolResult.isError` thành `is_error`**; `Browser.call` đọc cả hai.
- **`pip install -e .` lỗi "Multiple top-level packages"** vì repo flat-layout: `pyproject.toml` khai báo `[tool.setuptools.packages.find]`. Trên máy chỉ cần webauto có thể cài `playwright mcp` rồi `pip install --no-deps -e .` (bỏ qua vieneu).
- **Clipboard**: Windows dùng PowerShell, macOS dùng `pbpaste`/`pbcopy`.

- **ChatGPT chặn Chrome do script mở** bằng Cloudflare "verify you are human", tick xong vẫn hiện lại. Không né. Dùng Chrome thật qua Browsentic.
- **Browsentic từ chối thay người duyệt.** Hành động bị chặn (gửi form bằng phím Enter, tải file, đính file) từ client MCP bị từ chối cho tới khi chủ máy đặt quy tắc sang Allow trong Browsentic > Guardrails. Gửi tin bằng cách **bấm nút**, không nhấn Enter.
- **Danh sách chat/bảng chỉ vẽ phần gần khung nhìn.** Cắt câu trả lời theo vị trí câu hỏi trong văn bản trang sẽ hỏng khi câu trả lời dài. Dùng Copy + clipboard, hoặc so sánh nội dung ổn định theo thời gian.
- **Browsentic che chuỗi số dài** trong kết quả (`⟦card:…⟧`): đường dẫn file tải về và vài id video bị che. Lấy "file mới nhất trong thư mục tải", đừng tin `savedTo`; nhận diện bài TikTok bằng id chưa bị che hoặc tiêu đề.
- **Trình soạn thảo caption của TikTok bỏ qua `fillInput`**: giá trị quay về mặc định khi đăng. Phải gõ bằng phím thật (`typeText`).
- **Ảnh chụp màn hình có thể chậm một nhịp** hoặc không phản ánh vùng cuộn bên trong; kiểm tra trạng thái bằng DOM/văn bản trước khi bấm việc không hoàn tác được.
- **Bấm theo toạ độ vào khung menu** có thể trúng mục giữa (Download); bấm đúng mục, hoặc dùng selector của mục.
- Mỗi lần chạy `flow generate` tạo một **dự án Flow mới** và mỗi video tốn credit; dọn dự án thừa trong Flow.

## Thêm một công cụ mới

1. Tạo `webauto/<ten>.py` với hàm `add_parser(sub)` (đặt `set_defaults(func=...)` cho từng lệnh) và đưa vào `TOOLS` trong `webauto/cli.py`.
2. Import `mcp`/`playwright` **bên trong hàm** để `--help` chạy được trên máy chưa cài.
3. Dùng `webauto.browsentic.browser()` cho Chrome thật, `webauto.common` cho đọc file prompt và ghi markdown (`write_md` luôn gắn ghi chú "chưa kiểm chứng").
4. Hành động không hoàn tác được (đăng, xoá, thanh toán) phải có chốt mặc định an toàn và một cờ `--allow-…` rõ ràng; tách điều kiện chốt thành hàm thuần để viết test (`tests/test_webauto.py`).
