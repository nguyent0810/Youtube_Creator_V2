---
id: YCV-00ig
status: open
deps: []
links: []
created: 2026-10-28T08:30:45Z
type: chore
priority: 4
assignee: nguyen-tung
tags: [tooling, codex, render]
---
# Codex: chế độ full-access cho ticket render (khi cần)

Hiện tại (chủ kênh chọn 28/10) Codex không render: sandbox Windows của Codex chặn ghi npm cache ở AppData (EPERM open) và chặn spawn tiến trình con (spawn EPERM: node@22, Chrome headless, ffmpeg) khi build.py gọi 'npx -p node@22 -p hyperframes@0.8.75'. Render giao agy/Grok. Khi cần Codex render: thêm tuỳ chọn --full-access vào scripts/agent_ticket.py (và codex_ticket.py) để chạy 'codex exec -s danger-full-access' CHỈ cho ticket render, vẫn bỏ YT_CREDS_DIR khỏi env, brief cấm đăng/commit. Cân nhắc trước: cài sẵn hyperframes/node vào motion/hf để bớt tải qua npx. Tham khảo openai/codex#18675.

## Acceptance Criteria

Chủ kênh đồng ý bật; một render Codex chạy thật thành công với full-access; ghi lại rủi ro trong CLAUDE.md mục Điều phối agent.

