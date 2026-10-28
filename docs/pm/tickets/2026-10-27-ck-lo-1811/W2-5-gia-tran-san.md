# W2-5 — DỰNG CẢNH `ck-c6-gia-tran-san-t2`
Đọc `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CHUNG-W2.md` và làm đúng. Mã báo cáo: `W2-5`.
- **Biểu đồ chính:** dải trần/sàn (bars hoặc candles giả định) + lịch T, T+1, T+2 (timeline hoặc calendar): 100 cổ phiếu và tiền đang ở đâu.
- Ảnh nhân vật: 6 ảnh `ai01`–`ai06` (xem `ai_prompts.md`, mục "dùng ở CHnn").
- `script_lines.py` chạy với `--allow-repeat-line` (câu lặp cố ý T, T+1, T+2). CH00 mở bằng phiên thật 09/04/2025; nhân vật vào từ CH01.
- `build_long.py tts` và `html` cũng thêm `--allow-repeat-line`.
