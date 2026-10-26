# Luật Long cho agent sản xuất (chi tiết, chuyển từ AGENTS.md ngày 26/10/2026)

Đọc cùng `docs/codex/long-cheatsheet.md`.

### Ảnh AI khi không có ảnh tự do (từ 26/10/2026)

Cảnh cần minh hoạ mà không có ảnh PD/CC0/CC BY (ví dụ cảnh trong phòng làm việc năm 1962, hay một vật đã mất) thì **không tự tạo ảnh**. Ghi prompt vào `data/long/<topic>/ai_prompts.md` để chủ kênh nhờ bot tạo.

**Định dạng một mục:**

```
#### ai_01.png — <cảnh dùng ở chNN, câu số N>
- Prompt (tiếng Anh): <mô tả chi tiết: bối cảnh, thời kỳ, ánh sáng, bố cục, phong cách>
- Khung: 16:9, 1920x1080
- Cấm: chữ hoặc số trong ảnh, logo, khuôn mặt nhận ra được của người thật
- Phong cách: <ví dụ "painterly editorial illustration, muted 1960s palette">
```

**Quy tắc:**
- **Người thật: lấy dáng gốc, không vẽ mặt** (chủ kênh, 26/10/2026):
  - Được vẽ người có thật (Johnson, Glenn…) theo **dáng gốc** trong ảnh tư liệu: vóc người, kiểu tóc, trang phục, đồ vật, bối cảnh đúng thời kỳ.
  - Chỉ vẽ ở **góc nghiêng quay đi hoặc từ phía sau**, không thấy rõ mặt.
  - Trong prompt, ghi ảnh tư liệu tham chiếu (URL Commons/NASA trong `facts.md`) và mô tả dáng cụ thể. Ví dụ: "woman in 1960s cat-eye glasses and cardigan, seen from behind at a desk with mechanical calculator".
  - Mặt người thật chỉ dùng ảnh tư liệu PD.
- **Phong cách:** minh hoạ hoặc tranh vẽ, **không giả ảnh tư liệu**, để người xem không nhầm là tư liệu thật.
- **Không gắn nhãn AI:** không thêm nhãn "AI" trên màn hình hay trong mô tả, vì bản thân ảnh đã có chữ ký AI (chủ kênh quyết định ngày 26/10/2026).
- **Đường dẫn:**
  - Chủ kênh thả ảnh vào `motion/hf/assets/long/<topic>/img/ai/ai_NN.png`.
  - Engine chỉ đọc `output/long/<topic>/img/aiNN.jpg` kèm `.json`. Claude chạy `python scripts/ai_img_import.py <topic>` để chép ảnh sang chỗ đó.
  - Từ 26/10, Claude chạy `python scripts/ai_img_request.py <topic>`. Lệnh này gửi `ai_prompts.md` cho bot tạo ảnh qua webhook (khoá đọc từ registry User, xem `docs/tools/grokbot-webhook.md`), chờ ảnh về rồi chạy `ai_img_import`. **Agent sản xuất không gọi webhook**: chỉ viết prompt.
  - Trong `IMGS`, khai key `aiNN` là `"EXT:ai:ai_NN"`.
- **Ghi công:** cảnh dùng ảnh AI phải có `"credit": false`. Nếu thiếu, engine in "ẢNH: TƯ LIỆU · PHẠM VI CÔNG CỘNG", tức là gắn nhãn tư liệu cho tranh minh hoạ, sai sự thật. Nhãn `illus` "ẢNH MINH HỌA" thì giữ, vì đó là nhãn chuẩn cho tranh minh hoạ.
- **Khi chưa có ảnh:** giữ nguyên cảnh và đường dẫn, rồi ghi trong báo cáo "chờ N ảnh AI". `html` hoặc `long_gate` có thể báo thiếu file; điều đó chấp nhận được cho tới khi ảnh về.
- **Giới hạn:** tối đa 6 ảnh AI cho một bài 9–11 phút. Ưu tiên ảnh tư liệu thật.

### Quy trình Long (theo mẫu `data/long/mim-ke-huy-diet-petrov`, `mim-google-maps-kal007`)

Đọc trước:
- `motion/long/README.md`, `RETENTION.md`, `SOURCES.md`;
- `docs/pm/2026-10-23-mim-long-moi.md`;
- `docs/pm/so-that-bai.md`.

Các bước:
1. Viết `script.md` và `factcheck.md` (nguồn là URL đã mở).
2. Chạy `python motion/long/script_lines.py <topic>`; phải qua cổng integrity.
3. Viết `gen_scenes.py`, rồi chạy `python data/long/<topic>/gen_scenes.py`, ra `spec.json` và `chNN.json`. Counter có số 1000–2100 phải khai `"year": true|false`.
4. Chạy `python motion/long/studio_lint.py <topic> --strict`; phải ra 0 lỗi.
5. Chạy `python motion/long/build_long.py <topic> tts`, rồi `... html`. Sửa mọi lỗi lint mà `html` báo.
6. Chạy `python motion/long/clip_sheet.py <topic>`, xem ảnh clip sheet; clip sai nghĩa hoặc lộ logo thì thay.
7. Chỉ render khi ticket cho phép: `build_long.py <topic> render`, rồi `final`.
8. Dựng thumbnail `motion/long/thumbs/<topic>_t1.html`, rồi chạy `python motion/long/thumb.py <topic> t1`.

### Cổng chất lượng (bắt buộc, từ 26/10/2026)

Các cổng lint chỉ là mức sàn kỹ thuật. Trước khi báo xong một Long, phải chạy:

```
python scripts/long_gate.py <topic> --min-syl 1900
```

Lệnh phải in **ĐẠT**. Các ngưỡng được đo trên bài mẫu Petrov và KAL 007:

| Ngưỡng | Giá trị |
|---|---|
| Âm tiết lời đọc | ≥ 1.900 (≈ 9 phút) |
| Thời lượng mỗi cảnh | ≤ 9 giây |
| Loại cảnh mỗi chương | ≥ 5 |
| Một clip dùng lại (bài 9–12 phút) | ≤ 2 lần |
| Một ảnh dùng lại | ≤ 3 lần |
| URL nguồn trong `factcheck.md` | ≥ 8 |
| Tiêu đề | ≤ 60 ký tự |

Ngoài ra: mọi năm trong kịch bản phải có trong `factcheck.md`, và không được có câu đệm.

**Bài mẫu để so:**
- Petrov: 22,5 phút; 179 cảnh (7,6 giây/cảnh); ít nhất 7 loại cảnh mỗi chương; 15 ảnh khác nhau.
- KAL 007: 10,5 phút; 82 cảnh (7,7 giây/cảnh); không dùng clip, chỉ ảnh và đồ hoạ (bản đồ, timeline, counter).

Mỗi chương của hai bài này có 3–4 dữ kiện cụ thể có nguồn.

### Lỗi đã gặp (đừng lặp lại)

Thử nghiệm Codex T1/T1b, 26/10/2026:

1. **Chèn câu đệm rỗng nghĩa cho qua tỉ lệ câu ngắn của lint.** Ví dụ: "Rất chậm.", "Đó là câu hỏi khó.". Câu ngắn chỉ đặt sau một phán định hoặc khoảnh khắc cảm xúc.
2. **Bị yêu cầu bỏ câu đệm thì chỉ xoá, không viết nội dung thay.** Bài tụt từ 9 xuống 5 phút. Thiếu độ dài thì phải **tìm thêm dữ kiện có nguồn**, không được để bài ngắn đi.
3. **Đọc một ngày cụ thể (18/3/1940) trong khi chính `factcheck.md` ghi là chưa chốt được.**
4. **Một clip lặp 8 lần; 9 phút chỉ có 18 cảnh và toàn chữ.**
5. **Cold open liệt kê tên người thay vì dựng một cảnh có căng thẳng; câu meta "Hôm nay mình không kể…".**
6. **Coi việc qua lint là xong.** Xong nghĩa là `long_gate.py` in ĐẠT **và** nội dung đáng xem.
7. **Thẻ chương ghi sai trường.** Đã ghi `"number": "05"` thay cho `no`/`k`, nên engine hiện chữ "undefined" giữa màn hình ở cả 8 chương. Thẻ chương đúng (theo `mim-ke-huy-diet-petrov/ch05.json`):

   ```json
   {"type":"chapter","no":"5","k":"CHƯƠNG NĂM","title":"…","sub":"<mốc>","bg":"<ảnh>","titleAt":[0,"<từ>"]}
   ```

   Mỗi `chNN.json` cũng phải có `"hud": {"k": "CHƯƠNG 05", "t": "<TIÊU ĐỀ>"}`. Thiếu `hud` thì `describe.py` chết và mô tả không có danh sách chương.
8. **Một khuôn cảnh cho mọi chương.** Một khuôn 9 cảnh được dùng lại ở cả 8 chương, nên cùng một dòng chữ hiện 8 lần. Mỗi cảnh phải minh hoạ đúng câu đang đọc, và chữ trên màn hình lấy từ dữ kiện của chính chương đó. Mô-típ lặp chỉ được làm bằng `ledger` có tiêu đề cố định, mỗi chương thêm một dòng mới.
9. **Quên bảng `SAY` và để `spec.youtube` trống.** Phải viết ngay từ đầu, theo mẫu Petrov và KAL:
   - `SAY` phiên âm mọi tên nước ngoài, viết tắt (TNMOC, NASA…) và số rất lớn.
   - `spec.youtube` gồm: `publish_at`, `playlist`, `category`, `thumb`, `summary`, `more`, `chapter_titles`, `sources` (≥ 8 URL công khai), `tags`, `hashtags`, `video_credits`.

**Nghiên cứu trước, viết sau:** khi ticket chia đôi, ticket nghiên cứu chỉ gom kho dữ kiện có URL (`facts.md`). Ticket viết chỉ dùng dữ kiện trong kho đó.

