# T9 — 8 Short gắn Long `mim-may-choi-game` (lên 03/12 20:00)

**Việc:** viết kế hoạch + spec 8 Short MIM nhử Long này, 2 Short/ngày theo lịch mục 4 của 00-NGUON-NOI-DUNG.md.

**Đầu ra** (thư mục `docs/pm/tickets/2026-10-20-mim-nov/`):
1. `T9-ke-hoach.md`: bảng lịch (ngày, giờ lấy từ `scripts/shorts_grid.py`), mỗi bài: tiêu đề, câu mở ≤ 9 chữ, insight duy nhất, con số + nguồn (đoạn trong `data/long/mim-may-choi-game/script.md` hoặc URL), nhãn (SỐ/SỰ KIỆN | THỬ), lý do không trùng.
2. Một file spec JSON mỗi bài theo định dạng `motion/stier/README.md` + `themes.py` (theme `mim`), lưu `docs/pm/tickets/2026-10-20-mim-nov/specs-T9/<slug>.json` (KHÔNG ghi vào `data/stier/specs` ở pha 1).
3. Bảng đối chiếu trùng với toàn bộ Short MIM hiện có (query state.sqlite) và với các ticket T4–T9 khác.

**Làm xong khi:** đủ 8 bài hoặc báo rõ số bài thiếu và lý do; mỗi con số có nguồn; không có bài nào dùng khung "mẹo"; câu mở và câu chốt đúng luật; spec qua được `python motion/stier/build.py <spec> --lint-only` nếu có cờ đó, nếu không thì ghi cách đã tự kiểm.

## Đọc trước
- `docs/pm/tickets/2026-10-20-mim-nov/00-NGUON-NOI-DUNG.md` (luật, lịch, tiêu chí duyệt) — bắt buộc.
- `data/briefs/MIM.md`, `data/demand/MIM.json`, `docs/channels/mind-in-the-machine/`.
- Mẫu kế hoạch Short: `docs/channels/chung-khoan/2026-10-20-lo4-shorts-plan.md`.

## Ràng buộc chung
Pha 1: CHỈ viết file (docs/spec). KHÔNG dựng/render, KHÔNG upload, KHÔNG sửa state.sqlite, KHÔNG sửa file của ticket khác, KHÔNG sửa video đã đăng. Lỗi sự kiện/số liệu thì sửa nguồn, không bịa. Báo cáo cuối: file đã tạo, chỗ "cần kiểm", chỗ thiếu góc.
