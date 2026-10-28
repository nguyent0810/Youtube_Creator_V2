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

## Đăng nhập

Các trang đều cần tài khoản đã đăng nhập. webauto **không bao giờ tự nhập mật khẩu, không giải captcha và không né bước kiểm tra "bạn là người"** (Cloudflare của ChatGPT, xác minh 2 bước của Google...). Việc đó là của chủ tài khoản.

- Ngay sau khi mở trang, mỗi công cụ kiểm tra đã đăng nhập chưa (Flow: nút "Dự án mới" và không bị chuyển sang `accounts.google.com`; ChatGPT: không còn nút "Log in / Sign up" và không có bước "Verify you are human"; Muse: có ô chat; TikTok Studio và YouTube Studio: không bị chuyển sang trang đăng nhập).
- Nếu chưa đăng nhập, lệnh **in hướng dẫn, giữ nguyên cửa sổ Chrome, chờ bạn tự đăng nhập hoặc tự xử lý bước xác minh rồi tự chạy tiếp**. Thời gian chờ đặt bằng cờ toàn cục `--wait-login SECONDS` (mặc định 120, đặt trước tên công cụ: `python -m webauto --wait-login 300 chatgpt images ...`). `--wait-login 0` thì báo lỗi ngay kèm hướng dẫn, phù hợp khi chạy không người trông.
- `flow` dùng profile Chrome riêng của webauto: chạy `python -m webauto flow login` một lần (hoặc để `flow generate` tự chờ bạn đăng nhập trong cửa sổ nó mở). Các công cụ còn lại dùng Chrome thật của bạn qua Browsentic, nên chỉ cần đã đăng nhập sẵn trong Chrome đó.
- Phiên đăng nhập hết hạn giữa chừng (ví dụ ChatGPT đòi đăng nhập lại) được xử lý ở lần mở trang kế tiếp theo cùng cách trên.

Đổi chỗ lưu profile bằng biến `WEBAUTO_HOME`. Đổi lệnh chạy Browsentic bằng `WEBAUTO_BROWSENTIC_CMD` (mặc định `npx -y browsentic@latest mcp`). Profile chứa cookie đăng nhập nên **nằm ngoài repo**, không bao giờ commit.

## Lệnh

### `flow generate`
Tạo ảnh hoặc video trong một dự án Flow mới, tải về `<tên>_<n>_...`.
- `--mode image|video` (mặc định image). Mặc định model: Nano Banana Pro (ảnh), Omni 1.1 Flash (video). `--model` nhận một đoạn tên model.
- `--count 1-4` số kết quả mỗi prompt (mặc định 1), `--duration 4|6|8|10` giây (video, mặc định 6), `--ratio`, `--res`, `--quality 720p|1080p|4K` (chất lượng tải; 720p là bản gốc).
- `--image khung_dau.png` (video): ảnh làm **khung bắt đầu** (image-to-video). Một ảnh dùng cho mọi prompt trong lần chạy.
- `--headless`: chạy không mở cửa sổ Chrome (đã thử 28/10/2026 trên macOS: 1 ảnh Nano Banana Pro 16:9 trong 35 giây, Flow không chặn). Profile phải đã đăng nhập: chạy ẩn thì không chờ đăng nhập mà báo lỗi ngay, khi đó chạy `flow login` rồi thử lại. Profile vẫn bị khoá nếu còn cửa sổ Flow khác đang mở.
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
- `create`: mặc định **riêng tư** ("Only you"), không bao giờ đặt lịch. Đăng friends/công khai cần `--allow-public`. Mô tả luôn có tiền tố `--marker` (mặc định `TEST-CRUD`).
- `delete`: cần `--id`; từ chối nếu bài không phải "Only me" (trừ `--allow-public`) hoặc nếu không có **đúng một** dòng khớp id. TikTok giữ bài đã xoá 30 ngày (Activity center > Recently deleted).
- `update`: **chưa kiểm chứng** (xem dưới).

### `studio collect` / `studio summarize`
Gom **mọi số liệu của YouTube Studio** về file, để LLM đọc bản tổng hợp thay vì tự mở Studio (tốn token). Chỉ đọc, không đổi gì trên Studio.

```
python -m webauto studio collect                       # kênh Studio đang mở, mọi báo cáo, 5 kỳ
python -m webauto studio channels                      # các kênh của mọi tài khoản Google đã đăng nhập trong Chrome
python -m webauto studio collect --channel all         # lần lượt từng kênh, mỗi kênh một thư mục
python -m webauto studio collect --channel "biểu đồ" --periods 28d,lifetime --reports videos,daily,traffic_source
python -m webauto studio summarize --dir output/webauto/studio/<kênh>/<ngày>   # gộp lại thư mục đã thu
```

Chọn kênh: `--channel` nhận `all`, một phần tên kênh, mã `UC...` hoặc số `authuser`. Script mở `studio.youtube.com/?authuser=0,1,2...` (mỗi số là một tài khoản Google đã đăng nhập trong Chrome, như trong nút chuyển tài khoản của Studio), đọc mã và tên kênh, dừng khi số tiếp theo quay về kênh đã gặp; mọi URL xuất số liệu đều gắn `authuser` của kênh đó, nên không cần bấm chuyển tài khoản. Không có `--channel` thì lấy kênh Studio đang mở như trước. Mỗi tài khoản Google mới thấy kênh đầu tiên mà Studio mở cho nó.

Cách làm: với mỗi (báo cáo, kỳ) script mở URL **Chế độ nâng cao** của Studio (URL tham số hoá đầy đủ: kênh, kỳ, chỉ số, chiều), bấm "Xuất chế độ xem hiện tại" > `.csv`, giải nén. Dùng cái này thay vì Analytics API (`factory/analytics.py`) vì Studio có số mà API không trả (lượt hiển thị, CTR hình thu nhỏ, bảng theo từng video, các chiều khán giả), và một lần xuất là đủ mọi dòng.

- **Báo cáo** (`--reports`): `videos` (bảng từng video, 7 chỉ số), `daily` (theo ngày), `traffic_source`, `geography`, `content_type`, `playlist`, `city`, `age`, `gender`, `new_vs_returning`, `subscription_status`, `subscription_source`, `youtube_product`, `device`, `operating_system`. `videos` thu cho cả 5 kỳ (`7d,28d,90d,365d,lifetime`), `daily` cho 4 kỳ, các chiều còn lại cho `28d` và `lifetime`.
- **Đầu ra** trong `<out>/<kênh>/<ngày>/`: `raw/<báo-cáo>__<kỳ>/{table,chart,totals}.csv` (CSV gốc của Studio), `manifest.json` (báo cáo nào lấy được, báo cáo nào không và vì sao), và bản tổng hợp:
  - `summary.md`: **file để đưa cho LLM** (gọn, khoảng 15 KB cho kênh ~140 video và 14 chiều, so với hơn 200 KB CSV gốc): tổng kênh theo kỳ, phân bố lượt xem, short vs long, lượt xem theo tuổi video, xu hướng theo ngày, top/bottom video theo views, CTR, giữ chân, sub/1k views, các bảng theo chiều.
  - `summary.json`: toàn bộ số. `videos.csv`: một dòng mỗi video, đủ chỉ số mọi kỳ, cho công cụ khác.
- **Mã Studio** cho kỳ/chiều không có tài liệu. Đã xác nhận: kỳ `week`, `4_weeks`, `quarter`, `year`, `lifetime`; chiều `VIDEO`, `DAY`, `TRAFFIC_SOURCE_TYPE`. Các chiều khác script thử lần lượt từ danh sách ứng viên (mã sai thì trang trắng, nút xuất không hiện) và lưu mã chạy được vào `~/.webauto/studio_catalog.json`. `--refresh-catalog` để dò lại. Báo cáo nào không lấy được vẫn được ghi trong `summary.md` mục "Không lấy được".
- **Giới hạn 500 dòng**: Studio chỉ xuất 500 video đứng đầu mỗi bảng (dòng chú thích "Showing top 500 results"). Khi bị cắt, `summary.md` có cảnh báo; dòng "tổng kênh" vẫn đủ nhưng xếp hạng và phân bố chỉ trên 500 video đó.
- "Short" trong tổng hợp là quy ước của script (video dài tối đa 180 giây), không phải nhãn của YouTube.
- Cần quy tắc Browsentic `file-download` = Allow. Mỗi lần xuất mở một tab mới và dùng cú bấm thật: Chrome chỉ cho một lần tải tự động mỗi thao tác người dùng và âm thầm từ chối các lần sau ("Nothing downloaded").

## Đã kiểm chứng và chưa kiểm chứng

| | Trạng thái |
|---|---|
| `flow generate` ảnh, video, image-to-video | Đã chạy thật. |
| `chatgpt images`, `chatgpt ask` (kể cả `--from-chat`) | Đã chạy thật. |
| `muse research` | Chạy thật ở chế độ `--adopt-first`. Luồng tự mở side chat mới **chưa** kiểm chứng đủ. |
| `tiktok list`, `tiktok delete` | Đã chạy thật (xoá một bài test Only me). |
| `tiktok create` | Các bước đã chạy tay (tạo bài test Only me); chưa chạy bằng lệnh này. |
| `tiktok update` | Chưa thành công: text gõ vào được nhưng caption trên máy chủ không đổi. TikTok chỉ cho sửa caption một lần mỗi ngày mỗi bài, nên lần Save đầu có thể đã dùng hết lượt. |
| `studio collect` / `summarize` | Đã chạy thật trên một kênh: 35/35 báo cáo (14 chiều, 5 kỳ) lấy được, tổng hợp ra `summary.md` ~14 KB từ hơn 200 KB CSV. Mã kỳ/chiều đọc từ bộ chọn của Studio. Mới thử trên một kênh, một ngôn ngữ giao diện (tiếng Việt; CSV luôn tiêu đề tiếng Anh). |
| Xử lý đăng nhập (`--wait-login`) | Test logic đạt; đường **đã đăng nhập** chạy tốt trên cả 5 công cụ. Đường **chưa đăng nhập** chưa thử trên trang thật (dấu hiệu nhận biết dựa trên giao diện đã thấy, có thể cần chỉnh khi trang đổi). |

## Bài học (đừng lặp lại)

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
