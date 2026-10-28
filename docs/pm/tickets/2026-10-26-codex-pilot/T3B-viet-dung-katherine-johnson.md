# T3B — VIẾT + DỰNG trọn Long `mim-katherine-johnson` (một vòng)

**Đọc lại toàn bộ `AGENTS.md`.** File vừa được cập nhật: "Lỗi đã gặp" mục 7–9 và mục "Ảnh AI". **Kết quả:** `docs/pm/tickets/2026-10-26-codex-pilot/T3B-ket-qua.md`. Không render, không upload, không chạy `thumb.py`.

Claude đã duyệt kho `data/long/mim-katherine-johnson/facts.md` (36 dữ kiện). **Chỉ dùng dữ kiện trong kho.** Dữ kiện "vừa" phải có quy dẫn ngay trong câu đọc.

Mục tiêu của vòng này: **làm đúng từ lần đầu.** Claude đang đo số vòng và số lỗi chặn so với bài Turing (6 vòng, 12 lỗi).

## Checklist bắt buộc

Mỗi mục dưới đây là một lỗi đã từng xảy ra.

**Nội dung**

| Mục | Yêu cầu |
|---|---|
| Cold open | 20/02/1962: Glenn muốn Johnson kiểm tay các phương trình máy vừa chạy. Theo đề xuất trong báo cáo T3A |
| Độ dài | 1.900–2.300 âm tiết, 8 chương |
| Câu đệm | Không có (xem danh sách trong `long_gate.py`) |
| Phim | *Bộ Ba Ưu Việt* (*Hidden Figures*) chỉ nhắc bằng lời và chữ. Các chi tiết phim đã đánh dấu là hư cấu thì không kể như sự thật |
| Dorothy Vaughan | Tối đa 1 câu |
| Máy tính | Không đọc "IBM 7090" hay con số sai số khi kho chưa có nguồn mạnh |

**Tiêu đề và spec**

| Mục | Yêu cầu |
|---|---|
| `titles[0]` | ≤ 60 ký tự, một dấu hai chấm, ví dụ "HIDDEN FIGURES Ngoài Đời Thật: Katherine Johnson". Thêm 2 phương án dự phòng |
| `spec.youtube` | Đủ 11 trường: `publish_at` = `2026-11-25T13:00:00Z`, `playlist` = `Công Nghệ Quanh Ta`, `category` = `28`, `thumb` = `t1.jpg`, `summary`, `more`, `chapter_titles`, `sources` (≥ 8 URL công khai), `tags`, `hashtags`, `video_credits` |
| `SAY` | Viết ngay từ đầu cho mọi tên Anh, địa danh, viết tắt (NASA, NACA, IBM…) và số lớn. Mẫu: bài Turing |

**Cảnh**

| Mục | Yêu cầu |
|---|---|
| Thẻ chương | Đúng trường như Petrov: `no`, `k`, `title`, `sub`, `bg`, `titleAt` |
| `hud` | Mỗi `chNN.json` có `"hud": {"k", "t"}` |
| Số cảnh | 60–80, trung bình ≤ 9 giây/cảnh, ít nhất 5 loại cảnh mỗi chương |
| Không khuôn | Mỗi cảnh minh hoạ câu đang đọc. Không dòng chữ nào hiện quá 2 lần. Mô-típ chỉ qua `ledger` có tiêu đề cố định, mỗi chương thêm một dòng |
| Ảnh | Ưu tiên 14 ảnh NASA/Commons trong kho, mỗi ảnh tối đa 3 lần |
| Clip | Ít nhất 6 clip khác nhau, mỗi clip tối đa 2 lần. Soát bằng clip sheet |
| Counter | Năm khai `"year": true`; số lượng khai `"year": false` |

**Ảnh AI**

Tối đa 6 ảnh, chỉ cho cảnh không có ảnh tự do. Ví dụ: phòng West Area Computing năm 1953, bàn tính cơ, đêm trước 20/02/1962.
- Ghi prompt vào `data/long/mim-katherine-johnson/ai_prompts.md` theo đúng định dạng trong `AGENTS.md`.
- Người thật thì lấy dáng gốc từ ảnh tư liệu, chỉ vẽ ở góc nghiêng quay đi hoặc từ phía sau, không thấy mặt.
- Không có chữ trong ảnh. Không gắn nhãn AI.
- Trong `gen_scenes.py`, trỏ tới `assets/long/mim-katherine-johnson/img/ai/ai_NN.png`.

## Cổng

1. `script_lines.py`
2. `gen_scenes.py`
3. `studio_lint --strict` ra 0 lỗi
4. `build_long.py tts`, rồi `build_long.py html` cho đủ 8 chương. Nếu `html` chỉ báo thiếu file ảnh AI thì ghi lại, không coi là lỗi của mình.
5. `clip_sheet.py`
6. `python scripts/long_gate.py mim-katherine-johnson --min-syl 1900` ra **ĐẠT**. Nếu chỉ vướng vì ảnh AI chưa có thì ghi rõ.

## Báo cáo

- Số liệu từ `long_gate`.
- Tự kiểm checklist trên: từng mục là có hay không.
- Danh sách ảnh và clip.
- Số ảnh AI đang chờ.
