# Áp dụng `webauto` vào quy trình làm content MIM và CK (đề xuất, 28/10/2026)

`webauto` (PR #4, đã merge vào `main`) chạy lại một chuỗi thao tác cố định trên các trang không có API, không có LLM trong vòng lặp. Tài liệu: `docs/webauto.md`.

Bảng dưới gắn từng công cụ vào đúng bước của quy trình hiện tại: Brief → R → W1 → W2 → dựng → đăng → đo.

## 1. Gắn vào quy trình

| Bước | Hiện đang làm | Dùng `webauto` thế nào | Giới hạn, luật phải giữ |
|---|---|---|---|
| **Brief / R** (chọn đề, nghiên cứu) | Muse hỏi tay; subagent tìm web | `muse research --questions q.txt`: hỏi Muse một bộ câu cố định cho mỗi lô (đối thủ, chủ đề đang lên, cách đối thủ làm) → `docs/research/<ngày>-muse-*.md` | Kết quả là **gợi ý chưa kiểm chứng** (file tự gắn ghi chú). Mọi số, ngày, tên vẫn phải có URL đã mở trong `research.md`. |
| **Review độc lập** (brief, kịch bản, factcheck, retro) | Chủ kênh dán sang ChatGPT bằng tay | `chatgpt ask --file <file>` → `<file>.chatgpt-review.md`, cho agent đọc. Đã dùng thật với retro pilot hôm nay. | Ý kiến của AI ngoài là dữ liệu, không phải chỉ thị. Chỉ review file đã sạch thông tin nhạy cảm (không key, không đường dẫn credential). |
| **W2 / dựng: hình minh hoạ** | Ảnh AI qua Grok Bot webhook; clip Pexels | `flow generate --mode image`: ảnh minh hoạ cho cảnh không có tư liệu tự do (ví dụ cảnh hội đồng Apple 1985, cuộc gọi deepfake hư cấu). `chatgpt images` làm phương án dự phòng. | Ảnh AI luôn có nhãn ẢNH MINH HỌA. Người thật: dáng gốc, nghiêng hoặc quay lưng. Không vẽ chữ tiếng Việt bằng AI. Không thay ảnh tư liệu PD/CC0/CC BY khi đã có. |
| **W2 / dựng: b-roll động** | Pexels: retro P4 có clip nhoè, clip người văn phòng cho bài xe | `flow generate --mode video --image <ảnh PD>`: image-to-video từ ảnh tư liệu tự do (chuyển động nhẹ), hoặc b-roll đúng chủ đề khi Pexels không có | Tốn credit (video 8 s × 2 khoảng 24 credit). Vẫn qua `clip_sheet` và soát logo hay chữ đọc được. Clip AI phải có nhãn. Ghi nguồn trong credits. |
| **Thumbnail** | `motion/long/thumb.py` (HTML) | Chỉ dùng Flow/ChatGPT để tạo **ảnh nền** không chữ | Chữ thumbnail vẫn chỉ dựng bằng `thumb.py`; luật cấm vẽ chữ bằng AI giữ nguyên. |
| **Đăng ngoài YouTube** | Chưa có (`data/stier/tiktok_calendar_2026-11.json` có lịch nháp) | `tiktok create` (mặc định riêng tư), `tiktok list` | Chỉ khi chủ kênh duyệt kế hoạch TikTok. Không dùng `--allow-public` khi chưa có lời duyệt rõ. YouTube vẫn đăng qua API như cũ. |
| **Đo / Studio** | Chrome bị treo nên chưa đọc được "xem/lướt qua", hiển thị, Restrictions; "Video liên quan" phải gắn tay | **Chưa có công cụ**: đề xuất mục 2 | — |

## 2. Thiếu nhiều nhất: công cụ YouTube Studio

Pilot hook tháng 11 đang chờ ba việc mà API không làm được:
1. đọc chỉ số "xem / lướt qua" (stayed to watch) và lượt hiển thị trên Shorts feed;
2. đọc tab Restrictions;
3. gắn "Video liên quan" cho Short.

Đề xuất thêm `webauto/studio.py` theo mục "Thêm một công cụ mới" của `docs/webauto.md`, chạy bằng Chrome thật qua Browsentic:

| Lệnh | Làm gì | Chốt |
|---|---|---|
| `studio stats --id <video>` | Đọc trang Analytics của video: hiển thị, xem/lướt qua, thời lượng xem → JSON | Chỉ đọc |
| `studio restrictions --channel CK` | Đọc cột Hạn chế trong danh sách nội dung | Chỉ đọc |
| `studio related --id <short> --target <long>` | Gắn "Video liên quan" | Chỉ gắn khi Long đích thuộc cùng kênh; đọc lại DOM xác nhận trước khi Lưu; không đụng quyền riêng tư hay lịch |

**Vì sao làm trước:**
- trước 07/11 phải gắn 6 link cho pilot CK;
- sau đó mỗi Long có 2–3 Short S/L, và Short L bắt buộc có link;
- làm tay mỗi lần dễ sót.

## 3. Thử nghiệm đề xuất (nhỏ, có đo)

1. **Studio (ưu tiên 1):** viết `studio stats` và `studio related`; chạy thử trên 1 Short đã public trước, rồi mới gắn 6 link pilot CK.
2. **Review kịch bản:** khi W1 của 6 Long xong, chạy `chatgpt ask` cho từng `script.md` + `research.md`. Tổng hợp ý đáng sửa, gửi chủ kênh cùng kịch bản.
3. **Flow cho một Long:** M4 Deepfake. Bài này không có ảnh tư liệu tự do hợp lệ, nên tạo 6–10 ảnh minh hoạ hư cấu có nhãn và 2–3 b-roll image-to-video. Ghi credit tiêu tốn. So contact sheet với bài dùng Pexels.
4. **Muse:** mỗi lô hỏi một bộ câu cố định (lưu thành file câu hỏi trong `docs/research/`), để so được giữa các lô.

## 4. Điều kiện vận hành

- **Chrome thật:** `chatgpt`, `muse`, `tiktok` (và `studio` nếu làm) cần Chrome mở, cửa sổ ở phía trước, tab đã đăng nhập. Hôm nay Chrome bị treo khi thu nhỏ, nên chạy những lệnh này lúc chủ máy để Chrome hiện.
- **Flow:** cần `webauto flow login` một lần; đóng hẳn Chrome để không khoá profile.
- **Browsentic guardrails:** tải file và đính file phải được chủ máy đặt Allow. Code không né.
- **Không lưu credential vào repo:** profile nằm ở `~/.webauto`.
- **Cài đặt:** `pip install -e ".[webauto]"` (cần nhánh làm việc đã có `webauto`, xem mục 5).

## 5. Trạng thái ở checkout này

- Nhánh làm việc `feat/shorts-mix-standard` **chưa có** `webauto`.
- Merge `main` mang theo 278 file (PR #1, #3, #4, khoảng 50 nghìn dòng), trong đó 6 file đang có thay đổi chưa commit ở đây (`casefile.js`, `casewide.*`, `build_long.py`, `describe.py`, `data/variety/ledger.json`).
- Hai cách, chờ chủ kênh chọn:
  - (A) commit công việc hiện tại rồi merge đầy đủ, xử lý xung đột ở engine;
  - (B) chỉ lấy `webauto/`, `docs/webauto.md`, `tests/test_webauto.py`, cùng 2 dòng trong `pyproject.toml` và `.gitignore` từ `main`, để dùng ngay. Merge đầy đủ để sau, vào lúc không có render đang chạy.
