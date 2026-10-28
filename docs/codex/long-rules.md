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


## Chiến lược Long 45 ngày (chủ kênh, 27/10/2026), áp cho MIM và CK

Toàn văn ở `docs/pm/2026-10-27-chien-luoc-long-45-ngay.md`.

- **Độ dài:** mặc định 10–15 phút (2.100–3.200 âm tiết). Chỉ làm 20–30 phút khi chủ đề đủ nội dung. Không độn, không lặp lời dẫn.
- **Một câu hỏi trung tâm mỗi bài**, ghi ở đầu `script.md`. Chương cuối trả lời đúng câu đó.
- **Mốc cấu trúc:**
  - 0–30 giây: hook, tức tình huống, bí ẩn hoặc mâu thuẫn. Không mở bằng định nghĩa hay lịch sử.
  - 30 giây đến 2 phút: bối cảnh, và vì sao người xem nên quan tâm.
  - Cứ 3–5 phút có một **bước tiến lập luận**: bằng chứng mới, góc nhìn đối lập, phản biện hoặc hệ quả. Ghi các bước này vào bảng "Bước lập luận" đầu `script.md`.
  - Phần kết: trả lời, tổng hợp, và điều người xem rút ra được.
- **5 câu trước khi viết** (ghi vào đầu `script.md`):
  1. Người xem là ai?
  2. Họ tò mò hay lo điều gì?
  3. Vì sao chọn video này trên Home?
  4. Thumbnail truyền một ý nào?
  5. Tiêu đề khớp với 30 giây đầu thế nào?
- **Tiêu đề:** không đặt như tên bài học hay báo cáo, không liệt kê. Dùng câu hỏi, nghịch lý, hệ quả, nhưng không giật tít sai sự thật.
- **CK:** mỗi bài ghi rõ nguồn, giai đoạn, phương pháp, giả định và giới hạn kết luận. Không suy lợi nhuận tương lai từ quá khứ.

### Cập nhật "Áp dụng ngay" (chủ kênh, 27/10/2026, sau khi xem CD Media - Why?, Học viện Bò và Gấu, KIẾN THỨC THÚ VỊ, Anh Ba Tài Chính)

- **Content Brief bắt buộc trước khi sản xuất.** Thiếu brief thì không viết kịch bản. Mẫu: `docs/pm/tickets/2026-10-27-ck-lo-1811/00-CONTENT-BRIEF.md`. Brief gồm:
  - nhu cầu người xem, câu hỏi trung tâm, góc tiếp cận khác biệt;
  - 3 tiêu đề và 2 ý thumbnail;
  - hook 30 giây;
  - cấu trúc, nguồn dữ liệu, độ dài đề xuất.
- **Không mở bằng nhân vật giả định**, kiểu "Lan và Minh", "Tuấn và Khoa". Cũng không mở bằng định nghĩa hay lịch sử dài dòng.
  - Câu đầu phải là một trong ba thứ: sự kiện có thật kèm ngày, con số thật có nguồn, hoặc câu hỏi thật của người xem.
  - Ví dụ giả định chỉ vào từ CH01 trở đi, và nói rõ là ví dụ.
- **Cấu trúc documentary:** hook → vấn đề → bối cảnh → bằng chứng và dữ liệu → nghịch lý hoặc bước ngoặt → phân tích → kết luận. Không chạy slide chữ liên tục.
- **Thumbnail:**
  - 3–6 chữ lớn, một hình hoặc một cặp đối lập.
  - **Không ghi "VÍ DỤ GIẢ ĐỊNH"** trên thumbnail; giả định thì nói rõ trong video.
  - Không dùng biểu đồ nhỏ nhiều chữ, không dùng hình không liên quan.
- **Ảnh:** ưu tiên tư liệu thật (sự kiện, nhân vật) khi có quyền dùng. Không giả làm ảnh tư liệu: ảnh AI luôn mang nhãn ẢNH MINH HỌA.
- **Độ dài thử nghiệm:** MIM 10–15 phút, CK 8–13 phút. Chỉ làm 20–30 phút khi chủ đề thật sự cần.

## Cấm lách cổng bằng cảnh đệm (27/10/2026, lô CK 18–22/11)

Lô W2 này, 3/4 bài qua `long_gate` nhưng phải dựng lại toàn bộ cảnh, vì cảnh được sinh ra để đủ tỉ lệ chứ không bám lời đọc:
- vòng lặp `for` chèn `counter` / `bars` một cột / `timeline` có nhãn giữ chỗ ("ĐIỂM DỮ LIỆU 00A", "MỐC THEO DÕI 01-2", "LỚP TIỀN 3");
- một bộ cảnh rập khuôn lặp lại ở mọi chương ("… · CHƯƠNG 0N");
- 7 thẻ `ledger` giống hệt nhau ("CẦN NHÌN / CẢ ĐOẠN ĐƯỜNG");
- cảnh neo đều 2 câu một cảnh, không khớp con số đang được đọc.

Luật:
1. Mỗi cảnh phải hiện đúng con số hoặc sự kiện mà câu ở `at` đang nói.
2. Không sinh cảnh bằng vòng lặp, trừ khi dữ liệu thật sự là một chuỗi (ví dụ 24 ô `heat` của 24 lần mua).
3. Thiếu cảnh để đủ ≤ 9 s/cảnh thì tách câu dài ra thành nhiều cảnh có thông tin, không chèn thẻ đệm.
4. Tự rà: đọc từng câu trong `chNN.json`, rồi đối chiếu với cảnh neo ở câu đó.

Claude sẽ trả lại mọi bài có cảnh đệm.

## Short đi kèm Long: hai loại S và L (28/10/2026, chủ kênh duyệt)

**Nguyên tắc:** Short không phải trailer của Long. Short phải tự có giá trị. Long phải cung cấp chiều sâu, hoặc lời giải tiếp theo mà Short chưa thể trình bày.

Mỗi Short ghi loại trong spec: `"short_type": "S"` hoặc `"short_type": "L"`. Nhãn này chỉ dùng nội bộ, không đưa vào mô tả.

| | Loại S: tăng sub | Loại L: kéo Long |
|---|---|---|
| Nội dung | Trả lời trọn một vấn đề trong 20–35 s | Giải quyết một phần hữu ích, rồi để lại câu hỏi tiếp nối mà Long thật sự trả lời |
| Kết | Kết luận rõ | Câu hỏi tiếp nối có giá trị. **Không** dùng kiểu "muốn biết đáp án thì xem video dài", không giấu đáp án để câu view |
| KPI | stayed-to-watch, giữ chân, chia sẻ, sub/1.000 view | lượt vào Long (`SHORTS_CONTENT_LINKS`), chất lượng xem Long, sub |
| "Video liên quan" | Gắn khi có Long cùng đề, nhưng không tính KPI chuyển đổi | Bắt buộc, và đúng Long trả lời câu hỏi ấy |

- **Long nhận traffic từ Short L:** 10 giây đầu phải nhắc lại đúng câu hỏi của Short L, rồi mới mở rộng.
- **2–3 Short mỗi Long chỉ là thử nghiệm.** Không áp máy móc cho mọi Long. Brief của từng Long ghi rõ Short nào là S, Short nào là L, và mỗi Short trả lời phần nào.
- **Chưa trộn với pilot hook tháng 11.** Pilot CK 07–12/11 và MIM 13–18/11 giữ nguyên thiết kế (tất cả là loại S). Cấu trúc Short L được thử ở một lô riêng sau pilot.
- **Không bắt buộc Short L hơn Short S:** cố giữ thông tin có thể làm giảm giữ chân, nên phải đo, không mặc định là tốt hơn.
