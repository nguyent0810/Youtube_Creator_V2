---
id: YCV-cimp
status: closed
deps: []
links: []
created: 2026-10-28T08:48:24Z
type: task
priority: 1
assignee: nguyen-tung
tags: [auto, long-diag, MIM, CK, do-dac]
---
# Chẩn đoán vì sao Long MIM/CK gần như không có lượt xem

Sinh từ review ChatGPT 28/10 (docs/pm/2026-10-28-huong-lam-mim-ck.chatgpt-review.md, ưu tiên 1): phân loại từng Long đã public thành ít hiển thị / CTR thấp / giữ chân kém trước khi quyết chủ đề, packaging hay kịch bản. Giao Grok: docs/pm/tickets/LONG-DIAG-grok.md.

## Acceptance Criteria

Báo cáo docs/pm/tickets/LONG-DIAG-report.md, Claude review, đề xuất ≤3 việc có chỉ số.


## Notes

**2026-10-28T09:13:09Z**

grok xong (938 s), báo cáo docs/pm/tickets/LONG-DIAG-report.md. Chờ Claude review.

**2026-10-28T09:14:20Z**

Claude review 28/10: đạt (kiểm lại sywk-F-yW7k 7.834 impr/1,51%/404 views, xIfNPP1PLl8 1.843/0,71%/23). Kết luận: 16 Long public, 8 Long dừng dưới 1.000 impressions, 7/8 Long đã được hiển thị có CTR < 2%; giữ chân không phải vấn đề chính (1/16). Long không nhận view từ Short. Giờ Long 365 ngày: CK 10,8 giờ, MIM 37,8 giờ (<1% mốc 4.000).
