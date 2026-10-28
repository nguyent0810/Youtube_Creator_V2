---
id: YCV-9tns
status: open
deps: []
links: [YCV-8ted, YCV-g8ms]
created: 2026-10-28T07:20:59Z
type: task
priority: 1
assignee: nguyen-tung
tags: [do-dac, pilot, studio, CK, MIM]
---
# Đo đạc: baseline Studio và kết quả pilot hook Short (CK 07–12/11, MIM 13–18/11)

Mục tiêu: không quên các mốc đo của pilot hook A/B và có số Studio thật thay cho EVR proxy.

Đã có:
- 28/10: baseline Studio 3 kênh bằng `python -m webauto studio collect --channel <tên>` → output/webauto/studio/<UC id>/2026-10-28/summary.md (CK 35/35, MIM 35/35, CL 34/35). Số liệu Studio tới 26/10.
- Ghi nhận: 7 ngày gần nhất CK -78% views (6.154 vs 28.203), Short điển hình chỉ 3 lượt xem; MIM -40%.
- Luật đọc kết quả: docs/pm/2026-10-28-pilot-short-hook.md mục 6 (tích cực / chưa rõ / tiêu cực, không tự mở rộng).

Mốc đo:
- Trước 07/11: gắn 'Video liên quan' cho 6 Short pilot CK (p1/p2 → pXKfIo_nyVM, p3/p4 → Bx9w_a_1YOI, p5/p6 → ULLEUHkYz9g); chạy lại studio collect làm baseline sát ngày.
- CK: 48 h sau bài cuối = 14/11, 7 ngày = 19/11.
- MIM (13–18/11, chưa dựng): 20/11 và 25/11.

Còn thiếu: 'xem / lướt qua' (stayed to watch) và lượt hiển thị trên feed Shorts KHÔNG có trong bản xuất hiện tại của studio collect (chỉ có hiển thị hình thu nhỏ). Cần tìm mã chỉ số trong Studio hoặc đọc tay.

## Acceptance Criteria

- Có summary Studio ở các mốc 06/11, 14/11, 19/11 (CK) và 20/11, 25/11 (MIM).
- Bảng cặp A/B theo mục 6 của brief pilot, mỗi kênh một kết luận tích cực / chưa rõ / tiêu cực.
- Chỉ số 'xem / lướt qua' lấy được bằng script hoặc ghi rõ là đọc tay.
- Báo chủ kênh; không tự mở rộng pilot.


## Notes

**2026-10-28T08:00:52Z**

Biến nhiễu: Long CK 20:00 ngày 08/11 (7K1zP3ZdabQ), 09/11 (Ss_unzSu7DY), 11/11 (dQ3HLAXf12U), 1 giờ sau Short pilot; chủ kênh quyết giữ nguyên (28/10).

**2026-10-28T09:14:21Z**

Thêm từ YCV-cimp: ghi impressions, CTR, AVD của mỗi Long ở 24h/72h/7d; chỉ số: số Long đủ 7 ngày trước 11/11 có CTR ≥ 2% và AVD ≥ 3:00 nhưng impressions < 1.000.
