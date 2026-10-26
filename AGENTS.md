# AGENTS.md — luật cho agent sản xuất (Codex) trong repo này

Repo dựng video cho 3 kênh YouTube tiếng Việt: MIM (AI/công nghệ), CK (tài chính cá nhân), CL (Hình Sự; kênh này do agent khác lo, **không đụng**).

Vai trò:
- **Claude** điều phối: viết ticket, review cuối, đăng.
- **Agent sản xuất (bạn):** làm đúng ticket được giao trong `docs/pm/tickets/`, rồi viết báo cáo vào file kết quả mà ticket chỉ định.

## Cấm tuyệt đối

- **Không upload, không sửa và không xoá gì trên YouTube.** Không chạy `publish_long.py`, `publish_batch.py`, `enqueue_*.py`, `scripts/playlists.py`. Không đọc thư mục credential (`.youtube_channels`, `YT_CREDS_DIR`).
- **Không ghi `state.sqlite`.** Muốn xem lịch thì mở ở chế độ chỉ đọc:
  ```python
  sqlite3.connect('file:state.sqlite?mode=ro', uri=True)
  ```
- **Không đụng git:** không `git commit`, `push`, `reset`, `checkout`, `stash`.
- **Không sửa code dùng chung:** `motion/hf/assets/engine/*`, `motion/long/build_long.py`, `motion/stier/*.py`, `factory/*`, `tests/*`. Nếu thấy lỗi engine thì ghi vào báo cáo, đừng tự sửa.
- **Không xoá file** ngoài thư mục topic của ticket (`data/long/<topic>/`, `output/long/<topic>/`, `motion/long/thumbs/<topic>_t*.html`).
- **Không chạy hai lệnh render cùng lúc.** Máy chỉ chạy một render một lúc (`factory/render_lock.py` tự xếp hàng). Không kill tiến trình của người khác.

## Luật nội dung

- **Sự thật:** mỗi khẳng định có số, ngày hoặc tên đều phải có một dòng trong `factcheck.md`, kèm URL đã mở được. Không mở được nguồn thì không đọc thành khẳng định: hoặc bỏ, hoặc nói rõ "theo …". Không bịa trích dẫn. Lời trích là bản dịch thì gắn `[TRÍCH DỊCH]`.
- **Ảnh:**
  - MIM chỉ nhận PD, CC0, CC BY. Không nhận CC BY-SA, GFDL, NC, ND.
  - Không dùng hình phim; phim chỉ được nhắc bằng lời và chữ.
  - Không gắn nhãn tên người thật lên clip stock của người lạ.
  - Clip không được lộ logo hay chữ đọc được của thương hiệu.
- **Mô tả công khai** (`spec.youtube.*`, `description`) không được chứa: `<`, `>`, "CẦN", "cần kiểm", "WebFetch", "factcheck", "data/long", "tìm kiếm", "agent". Ghi chú làm việc để trong `sources_internal`.
- **CK:**
  - Không nêu tên ngân hàng thương mại, công ty chứng khoán, hãng xe hay mã cổ phiếu.
  - Không nói "nên mua/bán".
  - Số tự giả định phải ghi "VÍ DỤ GIẢ ĐỊNH".
  - Mô tả có câu "Nội dung giáo dục, không phải tư vấn đầu tư."
- **Tiêu đề** ≤ 60 ký tự. MIM: người + năm + bước ngoặt, hoặc khuôn "[PHIM/APP] Ngoài Đời Thật: [người thật]". CK: một khoản tiền × một mốc thời gian.
- **Viết cho tai:** câu một hơi, nói với "bạn", số làm tròn dễ nghe. Mã tài liệu và giờ chính xác chỉ hiện trên màn hình. Không mở bài bằng "trả lời ba câu hỏi"; mỗi bài dùng một dạng lộ trình riêng.
- **Thumbnail:** chữ tiếng Việt chỉ dựng bằng `motion/long/thumb.py` (HTML), không vẽ chữ bằng AI. Phải soi `tN_small.jpg`.

## Làm Long: đọc đúng 3 file, không khám phá repo

Khi ticket là một video dài, chỉ đọc:
1. ticket;
2. `docs/codex/long-rules.md` (cổng chất lượng, lỗi đã gặp, ảnh AI);
3. `docs/codex/long-cheatsheet.md` (cấu trúc cảnh, helper, thứ tự lệnh).

Thêm vào đó là các file mẫu mà ticket chỉ đích danh.

**Không** grep hay đọc code engine, thư mục của bài khác, hay log cũ để "tìm hiểu". Cách đó từng tiêu hết quota mà chưa ghi được file nào (26/10/2026). Thiếu thông tin thì ghi câu hỏi vào báo cáo rồi dừng.

## Báo cáo

Ghi file kết quả theo ticket, gồm:
- đã làm gì, lệnh nào chạy và kết quả, lỗi lint còn lại;
- khẳng định nào không kiểm được;
- đường dẫn clip sheet và thumbnail.

Không tự nhận là xong nếu chưa chạy các cổng kiểm ở trên.
