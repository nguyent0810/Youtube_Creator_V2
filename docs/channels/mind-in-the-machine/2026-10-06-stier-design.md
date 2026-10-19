# S-tier cho kênh Mind in the Machine (MIM) — thiết kế v1

Chốt sau 2 vòng phản biện Claude ↔ Grok (06/10/2026). Mục tiêu: 6 Short đầu tiên của MIM, cùng chất motion graphic với
hồ sơ S-tier của kênh Hình Sự (CL), nhạc nền miễn phí, Beat Text hay hơn — **không làm thay đổi một byte nào** của
đường CL và video dài.

## Đã làm

| Phần | Cách làm | File |
|---|---|---|
| Một bộ dựng, nhiều kênh | Spec ghi `"theme": "mim"`; `themes.py` giữ giọng, màu nhấn, kiểu âm thanh, bộ hiệu ứng, nhãn. Không ghi = `"case"` (CL, mặc định cũ) | `motion/stier/themes.py`, `build.py` |
| Giao diện | `#root.theme-mim`: nền xanh than + lưới mảnh, nhấn cyan `#22d3ee`, thẻ kính tối chữ sáng, bỏ hạt phim / sepia / Playfair, ánh đỏ cứng → ánh cyan | `motion/hf/assets/engine/theme-mim.css`, `casefile.js` (nhãn, khung, tông ảnh) |
| Giọng | "Hải Đăng" (nam, Bắc, tự nhiên) — khác mọi giọng 3 kênh kia. Cache wav theo **cả lời lẫn giọng** (trước đây đổi giọng vẫn trả wav cũ) | `build.speak` |
| Nhạc nền | 6 bài Kevin MacLeod (CC BY 4.0) trong `output/music/`; chọn bài lâu chưa dùng nhất, ghi sổ ngay mỗi lần chọn (`data/variety/mim_music.json`), dựng lại cùng video ra cùng bài. Trộn như video dài: nhạc 0,16, nén theo giọng 0.03/6/40/600, cảnh `question` gần như tắt nhạc, loudnorm −14 SAU khi trộn. Bỏ tiếng nền trầm (drone), giữ tiếng động theo cảnh | `themes.pick_track`, `themes.music_filter`, `sfx.build(drone=False)` |
| Ghi công nhạc | `output/stier/<slug>/music.json` → dòng ghi công CC BY vào mô tả | `enqueue_mim.py` |
| Beat Text (MIM) | Bộ hiệu ứng riêng, **mỗi dòng một kiểu** (CL: cả cảnh chung một kiểu). Dòng lớn: rise / blur / slice / flicker; nhấn: marker / outline / flicker; `type` / `scramble` chỉ cho dòng ngắn; slam: punch / zoom / slice / outline. Từ nhấn trong phụ đề nảy nhẹ (scale 1,06, ≤0,12 s) **đúng lúc được đọc** | `beatfx.assign_beats(pools=...)`, `casefile.js` (phụ đề) |
| Vào kho | Bundle kênh MIM, engine casefile, mô tả = mô tả + nguồn + ghi công nhạc + hashtag → `export_manual` | `motion/stier/enqueue_mim.py` |
| Hạ tầng máy này | `vieneu 3.8.3` (PyPI), ffmpeg tìm theo `FFMPEG_DIR` → bản vendor máy sản xuất → PATH | `build.py`, `build_long.py` |

## Quyết định

| # | Quyết định | Vì sao |
|---|---|---|
| 1 | Một bộ dựng + theme, không tách `motion/mim/` | Mọi sửa lỗi engine dùng chung; Grok: theme bằng biến CSS thôi là không đủ (ánh đỏ, Playfair, grain cứng trong CSS) → class `.theme-mim` ghi đè từng chỗ |
| 2 | **Không** dời chữ theo nhịp nhạc | Tiếng động (whoosh −0,3 s, dấu +0,16 s) và hiệu ứng có pre-roll 0,2–0,35 s đã bám mốc lời; dời ±0,12 s làm chữ lệch tiếng, phụ đề vẫn sáng theo lời; dời ranh giới cảnh có thể làm cảnh còn vài khung |
| 3 | Beat Text hay hơn bằng **bộ hiệu ứng theo kênh + nảy từ nhấn đúng lúc đọc** | Thấy được ngay, không phá đồng bộ lời |
| 4 | `type` / `scramble` chỉ cho dòng ngắn; không `glitch` cho slam | Đổi sang JetBrains Mono sau khi `fsz()` đã đo cỡ chữ, gõ từng ký tự làm dòng căn giữa nhảy; `glitch` rung `#stage`, đánh nhau với con dấu |
| 5 | Ảnh: chỉ PD/CC0 (như CL) | CC BY-SA cần chia sẻ tương tự, ghi công trong mô tả không đủ; metadata tác giả bị bỏ sau bước kiểm |
| 6 | Chưa thêm loại cảnh mới (chat, thanh xác suất) | Thanh xác suất sẽ bị đọc như số thật — trái luật "mọi con số có nguồn" |
| 7 | Nhạc MacLeod dù có thể bị Content ID báo claim | Tác giả cho phép, gỡ claim bằng dòng ghi công; upload tay nên người thấy claim ngay; Studio chặn bài nào thì bỏ bài đó khỏi pool |
| 8 | Dựng MIM **tuần tự** | Sổ chọn nhạc ghi sau mỗi lần chọn; dựng song song sẽ chọn trùng bài |

## v2 (06/10/2026, sau khi chủ kênh xem bản đầu: "toàn chữ, không có hình")

| Phần | Cách làm | File |
|---|---|---|
| Beat Text "sync" | Dòng chữ lớn mà MỌI chữ đều được đọc trong cảnh -> từng chữ hiện đúng lúc đọc (`SyncCursor`: đúng thứ tự, chữ chưa dùng, trong [t0, t1), không sớm hơn at − 0,35 s). Thiếu một chữ -> giữ hiệu ứng cũ. Dòng mở đầu (at < 0,3 s) không sync: khung 0 là hook + thumbnail | `beatfx.apply_sync`, `beat.js` BEAT.sync |
| Phụ đề karaoke | Chữ đang đọc màu nhấn, đọc xong về trắng (đổi tức thì, không mờ dần); chữ nhấn + số giữ màu nhấn | `casefile.js` |
| Dòng terminal | `"fx":"type"` CHỈ khi spec ghi rõ: canh trái + dấu nhắc "> " (cỡ chữ tính cả dấu nhắc) | `theme-mim.css`, `casefile.js` |
| Glitch trên chữ | Tách kênh màu trên chính dòng chữ, không rung khung | `beat.js` BEAT.glitch, `beat.css` |
| Nền sống | Lưới nền trôi chậm suốt video (không đụng chữ) | `casefile.js` (TH.drift) |
| Clip nền | `"clip": "pexels:<id>"` / `"coverr:<id>"` trên cảnh; tải + cắt sẵn 1080x1920 30 fps không tiếng vào `motion/hf/assets/clips/` (gitignore); thẻ `<video>` nướng tĩnh như video dài; màn che `veil` | `motion/stier/clips.py`, `build.py` |
| Ảnh | Commons PD/CC0 + **CC BY** (không BY-SA, không NC/ND) cho kênh MIM, lưu tác giả + giấy phép; ảnh NASA (`NASA:<id>`) | `build.license_ok`, `fetch_img`, `fetch_nasa` |
| Ghi công | `output/stier/<slug>/credits.json` (ảnh + clip) -> mô tả video cùng ghi công nhạc | `enqueue_mim.credit_lines` |
| Đối chiếu dữ kiện | 6 kịch bản đối chiếu với nguồn (agent): sửa các chỗ nói quá ("đúng một việc", "Meta mô tả nó", "ĐÚNG = SAI", "22:30", "tin nhắn của Internet", "bớt bịa", mẹo deepfake thiếu phương án dự phòng + thêm nguồn FTC) | `data/stier/specs/mim-*.json` |

Nguồn clip: Pexels (chính, nhiều clip dọc) + Coverr (phụ: gần như toàn 16:9, ghi công bắt buộc, gói Demo 50 lần gọi/giờ, bỏ clip AI-generated/premium).

## Chưa làm

- Lớp "nhịp nhạc" không đụng chữ (`#pulse`, lưới chớp theo beat): tắt mặc định; chỉ bật sau khi nghe lưới beat trên bản trộn đã nén.
- Ảnh/clip minh hoạ (Pexels khi có `PEXELS_API_KEY`, ảnh PD/CC0 cho chủ đề lịch sử): 6 video đầu chỉ dùng chữ động + số + mốc thời gian.
- Dòng nội dung MIM trong `factory/lines` (để vòng phản hồi/xoay giờ hiểu 3 dòng); hiện slug `mim-` là một dòng.
