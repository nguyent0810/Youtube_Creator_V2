# yt-factory

Xưởng dựng video YouTube cho kênh CL ("Into The Killer's Mind") và các kênh FS, BUD. Chủ kênh đọc tiếng Việt.

## Luật không được phá

- **Cải thiện là thêm vào hệ thống đang chạy tốt, không thay nó.** Sáu Long đã đăng (yakuza, mafia, shanghai, ripper, kowloon, golden) là chuẩn. Trước khi đổi cách làm, dựng thử một chương và so với chương tương ứng của `golden`.
- **Không đăng, không đặt lịch, không gỡ lịch, không xóa video khi chủ kênh chưa nói rõ.** Luôn upload private kèm `publishAt`. Video đã đăng thì để yên.
- **Mỗi lần chỉ làm một Long**, và chỉ sau khi chủ kênh duyệt kế hoạch rồi duyệt kịch bản. Không dựng hàng loạt: YouTube coi nội dung sản xuất hàng loạt theo khuôn là spam (`motion/long/RESEARCH-million-views.md`).
- Chỉ dùng tư liệu tự do (`motion/long/SOURCES.md`). Không ảnh AI, không clip phim, không bịa lời trích.
- Không in bí mật (token, khóa API) ra màn hình hay vào file.

## Quy trình một Long (đủ cả 8 bước, không bước nào tự bỏ)

1. **Chọn đề tài**: viết `data/long/<topic>/plan.md` (vì sao đề tài này, cold open, các vòng lặp mở). Chờ chủ kênh duyệt.
2. **Tư liệu trước, chữ sau**: `motion/long/research_long.py` và `media_search.py` → `output/long/<topic>/research.json`, soi contact sheet. Không đủ khoảng 50 ảnh tự do thì đổi đề tài.
3. **Kịch bản** `script.md`: 5.500–7.000 âm tiết (25–32 phút), 12–14 chương. Chờ chủ kênh duyệt.
4. **Cảnh viết tay** trong `gen_scenes.py` (+ `gen_scenes2.py`), theo mẫu `data/long/golden/`: mỗi câu gắn với ảnh, bản đồ, hồ sơ, biểu đồ, sketch hoặc b-roll. `scenes_from.py` chỉ cho ra bộ khung nháp (`"auto": true`), không phải cảnh.
5. **Giọng**: `build_long.py <topic> takes 3` → `stt_takes.py` → `pick` → `tts`.
6. **`html`**, rồi `render chNN --draft` vài chương để soi, rồi `render`, rồi `final`.
7. **QA bằng mắt** trên contact sheet từng chương. Sửa, render lại chương hỏng.
8. **Báo chủ kênh**, đề xuất lịch. Họ đồng ý thì ghi `"approved": "<ngày> — <lời duyệt>"` vào spec rồi mới chạy `publish_long.py`.

## Các cổng tự động (đừng tắt, đừng lách)

- `motion/long/floor.py`: sàn sản xuất. Từ chối `render`, `final`, `publish` khi kịch bản dưới 5.000 âm tiết, dưới 40 ảnh, dưới 30 cảnh b-roll, dưới 14 loại cảnh, kinetic trên 38%, chữ trên nền trống trên 12%, hoặc còn cảnh `auto`. Ngưỡng lấy từ sáu Long đã đăng. **Bị chặn nghĩa là video chưa đạt, không phải cổng sai**: bổ sung tư liệu và kịch bản, đừng hạ ngưỡng.
- `motion/variety.py audit`: nhạc nền và look phải khác ba video gần nhất.
- `motion/long/lint_html.py`, `craft.py`: lỗi con dấu, tiêu đề thẻ, clip HDR, câu quá dài.

## Sự cố 11/10/2026 (lý do có file này)

Một phiên được nhờ "cải thiện" đã dựng bốn Long (escobar, capone, bulger, namcam) trong 100 phút: bỏ bước tư liệu, kịch bản 1.300–2.100 âm tiết (7–11 phút), 94% cảnh là bốn từ đầu câu trên nền đen, rồi đặt lịch public cả bốn. Chủ kênh phải gỡ lịch và làm lại. Tự động hóa việc viết cảnh là mục tiêu đúng, nhưng đầu ra phải qua được `floor.py` và mắt chủ kênh trước khi thành video.

## Ticket (để không quên việc)

Dự án dùng `tk` ([wedow/ticket](https://github.com/wedow/ticket), MIT, bản chép trong `tools/ticket/`). Ticket là file markdown trong `.tickets/`, commit cùng repo.

- Gọi: PowerShell/cmd dùng `.\tk <lệnh>` (file `tk.cmd`, chạy bằng Git Bash, dùng được từ thư mục nào cũng được: `& "D:\Tools\Youtube Creator v2\Youtube_Creator_V2\tk.cmd" ready`). Trong Git Bash: `bash tools/ticket/tk <lệnh>`. Không gõ `bash` trong PowerShell: đó là WSL, máy này không có.
- Đầu phiên: `tk ready` (việc đang mở, đã hết phụ thuộc).
- Việc kéo dài hơn một phiên hoặc có mốc ngày: `tk create "<tiêu đề>" -p <0-4> --tags <...> -d "..." --acceptance "..."`.
- Tiến độ: `tk add-note <id> "..."`; xong: `tk close <id>`. `tk ls`, `tk query` là plugin; `tk.cmd` đã tự thêm vào PATH, Git Bash thì cần `PATH="$PWD/tools/ticket:$PATH"`.

## Điều phối agent (từ 28/10/2026)

Claude điều phối và review cuối. Các agent CLI trên máy làm ticket: Codex (`codex exec`), agy (`agy -p`), Grok (`grok -p`).

- **Giao việc:**
  1. Viết brief `docs/pm/tickets/<id>-<agent>.md`, ghi rõ phạm vi, file được ghi và file báo cáo.
  2. Chạy `python scripts/agent_ticket.py <id> --brief <brief> --expect <báo cáo> --agents codex,agy,grok`.
- **Fallback:** agent hết quota, lỗi hoặc không ghi báo cáo thì script tự chuyển agent kế tiếp. Hỏng cả danh sách thì có cờ `docs/pm/tickets/<id>.FALLBACK_CLAUDE` và thoát mã 3; khi đó Claude giao cho subagent của mình. Long vẫn dùng `scripts/codex_ticket.py`, script này có snapshot và rollback.
- **Chọn agent:** code, spec và test giao Codex. Codex **không render** (chủ kênh chọn 28/10): sandbox Windows của Codex chặn npm cache và `spawn` (Node 22, Chrome, ffmpeg), nên render và các lệnh `npx hyperframes` giao agy hoặc Grok. Phân tích giao agy hoặc Grok. agy chạy không người trông bằng `--sandbox --dangerously-skip-permissions` (chủ kênh cho phép 28/10, AI Learning cũng dùng vậy), nên brief phải ghi rõ file nào được ghi.
- **Tự sinh ticket:** đọc báo cáo của agent, thấy việc cần làm thì Claude tạo ticket mới, gắn tag `auto` và ghi ticket nguồn trong mô tả.
  - Được tự giao: phân tích, sửa code hoặc công cụ, viết spec, dựng nháp.
  - Phải chờ chủ kênh duyệt: đăng, đặt lịch, gỡ hay thay video đã đăng, đổi kế hoạch nội dung, mọi thứ ra ngoài.
- **Agent không bao giờ:** đăng, enqueue, commit, đổi lịch, hoặc thấy `YT_CREDS_DIR`.
- **Quyền tự duyệt:** agy chạy với `--sandbox --dangerously-skip-permissions`, Grok chạy với `--always-approve`. Chủ kênh cho phép cả hai từ 28/10.
- **Chốt chặn** (theo review ChatGPT 28/10, `docs/pm/2026-10-28-huong-lam-mim-ck.chatgpt-review.md`):
  - tối đa 5 ticket tag `auto` đang mở; vượt thì gộp hoặc chờ;
  - mỗi brief có input, output, tiêu chí đạt và file báo cáo cố định;
  - agent không tự xác nhận "đạt": Claude kiểm số hoặc khung hình bằng chứng trước khi đóng ticket;
  - việc đổi trạng thái đăng (upload, lịch, thay video) không bao giờ đi qua fallback tự động.
