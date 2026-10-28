# T2 — Long 20–30 phút (hẹn 07/12 20:00 VN)

**Phụ thuộc:** `T1-ket-qua.md` đã xong và Claude đã chọn chủ đề. Không bắt đầu khi chưa có chủ đề chốt.

**Việc:** nghiên cứu sâu + viết kịch bản + factcheck + spec cho Long 20–30 phút, theo đúng cấu trúc các Long MIM trước: `data/long/<slug>/{script.md, factcheck.md, ch00..chNN.json, gen_scenes.py, spec.json}` (mẫu: `data/long/mim-qwerty`, `mim-ai-gpu`). Quy trình ở `motion/long/README.md`, `RETENTION.md`, `SOURCES.md`.

**Luật riêng:** độ dài lời đọc đo bằng chữ (≈ 150 từ/phút giọng hiện dùng) phải rơi trong 20–30 phút, không dưới 8 phút; mở bài khác dạng "trả lời ba câu hỏi"; chọn dạng lộ trình khác các Long cũ; mỗi khẳng định số liệu có dòng trong `factcheck.md` kèm URL; không độn để đủ giờ — nếu tư liệu thiếu, báo và đề xuất chủ đề dự phòng.

**Đầu ra:** thư mục `data/long/<slug>/` đầy đủ + `docs/channels/mind-in-the-machine/2026-10-2x-long-<slug>-research.md`. KHÔNG dựng/đăng ở pha 1.

**Làm xong khi:** script đúng độ dài, factcheck không còn dòng "chưa kiểm" cho số liệu quan trọng, `studio_lint.py` (nếu áp dụng ở bước viết) không báo lỗi cứng.

## Đọc trước
- `docs/pm/tickets/2026-10-20-mim-nov/00-NGUON-NOI-DUNG.md` (luật, lịch, tiêu chí duyệt) — bắt buộc.
- `data/briefs/MIM.md`, `data/demand/MIM.json`, `docs/channels/mind-in-the-machine/`.
- Mẫu kế hoạch Short: `docs/channels/chung-khoan/2026-10-20-lo4-shorts-plan.md`.

## Ràng buộc chung
Pha 1: CHỈ viết file (docs/spec). KHÔNG dựng/render, KHÔNG upload, KHÔNG sửa state.sqlite, KHÔNG sửa file của ticket khác, KHÔNG sửa video đã đăng. Lỗi sự kiện/số liệu thì sửa nguồn, không bịa. Báo cáo cuối: file đã tạo, chỗ "cần kiểm", chỗ thiếu góc.
