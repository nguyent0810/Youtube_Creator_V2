---
id: YCV-3sx8
status: open
deps: []
links: []
created: 2026-10-28T07:29:19Z
type: task
priority: 2
assignee: nguyen-tung
tags: [CK, MIM, retro, tooling]
---
# Retro pilot CK: cài các chốt phòng lỗi còn lại (P1, P2, P3, P5, P7, P8)

Từ docs/pm/2026-10-28-retro-ck-pilot-short.md (P4, P6 đã xong): lint spec trước TTS, check_gate cho CK/MIM, cột ngày hiệu lực trong factcheck (P7), trạng thái 'replaced' trong store (P8), test font mất dấu ì/đ.

## Acceptance Criteria

Mỗi chốt có test; ghi vào retro là đã xong.


## Notes

**2026-10-28T08:48:25Z**

Review ChatGPT 28/10 thêm yêu cầu: QA gate tự động theo từng bước (spec → script → asset → render → sẵn sàng đăng), đặc biệt kiểm tra luật CK (tên ngân hàng/mã, 'nên mua/bán', nhãn VÍ DỤ GIẢ ĐỊNH, nguồn số liệu) và kiểm trùng nội dung.

**2026-10-28T09:50:31Z**

Thêm từ retro pilot MIM (docs/pm/2026-10-28-retro-mim-pilot-short.md): lint spec cho (1) hook B câu 0 có 'bạn', không mở bằng Theo/Tháng/Năm/Ngày (cần trường pilot.hook); (2) acc không chứa từ phủ định hay 'một'; (3) board ≥ 3 nút phải xếp dọc cùng x; (4) danh sách đen clip Pexels (39687575, 38410501, 28709421…) + cảnh báo title có woman/man/people/face; (5) chart 1 cột → bắt dùng counter. Giao Codex (code + test), không render.
