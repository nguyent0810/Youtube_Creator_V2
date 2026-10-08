# Thư viện bên thứ ba dùng lúc render (khoá phiên bản, không tải mạng)

| File | Nguồn | Phiên bản | sha256 |
|---|---|---|---|
| `gsap.min.js` | npm `gsap` (`dist/gsap.min.js`, tarball khớp `dist.integrity` của registry) | 3.14.2 | `c174bfce53a729418d57a8ad8625e7247c793a22fef8e2851e3cfa3de9cd8280` |

Giấy phép GSAP: GSAP Standard License (https://gsap.com/standard-license), giữ nguyên phần đầu file.

Vì sao chép vào repo: trước đây mọi composition tải GSAP từ cdn.jsdelivr.net lúc render
(không SRI). CDN lỗi là render hỏng, và luật "no network fetches" của `motion/hf/CLAUDE.md`
bị vi phạm (audit 08/10/2026, T15). Đổi phiên bản: thay file, cập nhật bảng trên, chạy
`python -m pytest tests/test_motion_fixes.py` (kiểm mọi trang trỏ đúng file này).
