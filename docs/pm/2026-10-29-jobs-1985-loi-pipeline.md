# Jobs 1985 (`mim-jobs-1985`): tổng kết lỗi pipeline

Ngày: 29/10/2026. Issue: #10. Đây là Long thử nghiệm đầu tiên làm theo quy trình Codex sửa, agy QA/render, Claude review.

## Số vòng phải làm

| Bước | Số vòng | Ghi chú |
|---|---|---|
| Kịch bản (Codex W1) | 3 vòng + Claude sửa cuối | bản đầu khô, đọc cả ghi chú sản xuất thành lời |
| Dựng cảnh (Codex W2) | 1 vòng, bị thay toàn bộ | Claude subagent viết lại, sau đó đi theo quy trình QA |
| QA từng cảnh (agy) | 1 | 58/127 cảnh có lỗi: 7 chặn, 33 nên sửa, 18 nhỏ |
| Sửa (Codex) | 3 vòng | vòng 2 sinh ra lỗi chặn mới (ảnh Sculley co thành một chấm) |
| Preview | 2 lần + final | lần 2 và final do Claude làm vì agy, Grok hết quota |

Lỗi kỹ thuật lẽ ra phải bị chặn ngay ở bước `html`, nhưng phải tới bước xem khung hình mới thấy. Phần lớn số vòng tốn vào đó.

## Lỗi theo nhóm, nguyên nhân gốc và cách chặn

### A. Tham số engine sai mà không bị báo lỗi (2 vòng sửa)
- Cảnh `print` bỏ qua `head`, nên 4 tiêu đề không hiện.
- `maxW`/`maxH` tính bằng pixel, nhưng Codex đặt 0.52/0.56, nên ảnh co lại còn khoảng 15 px.
- `pos` phải là chuỗi CSS, Codex lại truyền mảng.
- **Gốc:** `casewide.js` không kiểm tham số. Field sai kiểu hoặc field không dùng tới thì bị bỏ qua, không báo gì.
- **Chặn (đề xuất A1):** thêm kiểm tham số vào `build_long.py html` (cổng kỹ thuật). Gặp key lạ, `head` trong `print`, `maxW`/`maxH` < 50, hoặc `pos` không phải chuỗi thì báo lỗi.

### B. Chữ trên màn hình cắt máy móc từ lời đọc (W2)
- Lấy 5 từ đầu câu viết hoa lên màn hình; nhãn không dấu; sai đơn vị; nút `org` trùng chữ.
- **Gốc:** brief không cấm, và không có lint nào bắt.
- **Chặn (A2):**
  - lint `studio_lint`: chữ trên hình trùng tiền tố câu đọc thì báo lỗi;
  - chữ tiếng Việt thiếu dấu (nhãn toàn ASCII mà có từ tiếng Việt) thì báo lỗi.

### C. Ảnh không được xem trước khi dùng
- Ảnh `nextcube` lộ máy Minitel và chữ "3615 FRED".
- `nextcube2` chỉ thấy mặt lưới, không nhận ra là máy tính.
- `sculley06` lộ thẻ tên.
- 6 ảnh AI được nhập nhưng không cảnh nào dùng: dict bị ghi đè.
- **Gốc:** có `clip_sheet.py` cho clip, nhưng không có sheet tương ứng cho ảnh tĩnh. Cũng không có bước kiểm "mọi ảnh đã nhập đều được dùng".
- **Chặn (A3):**
  - thêm `img_sheet` (ảnh nguồn kèm khung crop 16:9 thực tế theo `focus`), bắt buộc soát trước khi dựng cảnh, giống luật clip sheet;
  - `scene_rules` báo ảnh đã nhập mà không dùng.

### D. Cảnh trống đầu cảnh
- 2 cảnh `org` chỉ có một nút trong khoảng 3 giây đầu.
- **Chặn (A4):** thêm luật `scene_rules`: phần tử con đầu tiên phải hiện trong vòng ≤ 1 giây sau khi cảnh mở.

### E. Phụ đề không được tạo tự động
- Lần upload đầu dừng ở preflight vì thiếu `captions.vi.srt`. Không có gì bị đăng.
- **Gốc:** `srt.py` không nằm trong bước `final`, và không có tài liệu nào nhắc phải chạy.
- **Chặn (A5):** `build_long.py final` tự chạy `srt.py` ở cuối.

### F. Mô tả đếm ảnh AI vào "phạm vi công cộng"
- Mô tả ghi "8 ảnh PD/CC0", trong khi thật ra chỉ có 2 ảnh PD/CC0.
- **Đã sửa gốc:** `describe.py` bỏ qua `EXT:ai:` ở cả hai nhánh (MIM/CK và CL).

### G. Gate sai kênh
- `floor` dùng ngưỡng CL cho MIM nên chặn render.
- **Đã sửa:** floor theo kênh (GH-12), có test hồi quy.

### H. Hạ tầng agent
- Codex treo khi tải model TTS từ HF Hub, và không render được vì sandbox (EPERM). Lệnh giao chạy kiểu detached không báo khi xong.
- agy hết quota (reset sau khoảng 33 giờ); Grok hết hạn mức (lỗi 402).
- **Đã làm:**
  - TTS và render để agy/Claude chạy;
  - lệnh giao việc chạy nền có waiter.
- **Còn mở:** cần một agent render dự phòng ngoài Claude. Xem ghi chú quota agy ở cuối.

### I. Codex so nhầm engine (YCV-ahg7 vòng 1)
- So với `longform.js` trong khi Long dùng `casewide.js`.
- **Chặn (A6):** ghi rõ trong `docs/codex/long-rules.md`: engine của Long là `motion/hf/assets/engine/casewide.js`.

## Thứ tự đề xuất (chờ duyệt)

| Mã | Việc | Loại | Ước lượng tiết kiệm |
|---|---|---|---|
| A1 | Kiểm tham số engine ở bước `html` | cổng kỹ thuật | 2 vòng sửa + 1 preview |
| A3 | `img_sheet` + báo ảnh nhập không dùng | quy trình + lint | 1 vòng sửa |
| A2 | Lint chữ trên hình: trùng lời đọc, thiếu dấu | lint | cả vòng W2 |
| A4 | Luật phần tử con đầu cảnh ≤ 1 giây | `scene_rules` | 1 vòng nhỏ |
| A5 | `final` tự tạo SRT | pipeline | 1 lần upload hỏng |
| A6 | Ghi rõ engine Long trong `long-rules` | tài liệu | — |

Không đề xuất hạ hay đổi ngưỡng nào. Các ngưỡng mới (A1, A4) phải có test hồi quy, chạy lại trên các Long đã đăng để xem bao nhiêu bài trượt, rồi mới bật.

## Bổ sung sau retro độc lập (29/10, sau khi upload `fanXUEAttLw`)

Retro không thấy lỗi nào đổi nghĩa trong video đã đăng, nên giữ nguyên video. Các lỗi nhỏ:
- Ngày IPO của Pixar ghi 28.11.1995; các nguồn khác ghi 29/11.
- Thẻ TRÍCH DỊCH ở ch01 thực ra là diễn ý.
- "Mười hai năm sau" là làm tròn; thực tế khoảng 11 năm 3 tháng.
- Mô tả có tiêu đề NHẠC NỀN nhưng phần đó trống.
- `factcheck.md` lệch với bản final (vẫn còn mục Microsoft; Toy Story ghi sai chương).

Retro thấy thêm mấy lỗi tôi bỏ sót ở trên:
- Cảnh ngắn hơn 2,5 giây (22/127 ở bản W2): `scene_rules` chỉ cảnh báo, không chặn.
- Có ảnh dùng 7–9 lần, vượt luật ≤ 3 lần, mà không có lint nào đếm.
- Bảng ledger 7–8 dòng tràn xuống vùng phụ đề.
- Clip lộ chữ "MacBook Pro". Đây là lỗi quy trình (không soát clip sheet), không phải thiếu công cụ.
- A1 phải kiểm tham số theo từng loại cảnh (kinetic accent, nhãn quote), không chỉ cảnh `print`.

Đề xuất thêm, chờ duyệt:

| Mã | Việc |
|---|---|
| A7 | Chuyển `min_shot`/`max_shot` từ cảnh báo thành lỗi chặn |
| A8 | Lint đếm số lần dùng mỗi ảnh (≤ 3) |
| A9 | Giới hạn số dòng ledger |
| A10 | Chặn render khi cảnh b-roll chưa có clip sheet đã soát |
| A11 | Trước khi đăng, đồng bộ `factcheck.md` với bản final; mỗi câu TRÍCH DỊCH phải có nguyên văn |
| A12 | `describe.py`: bỏ tiêu đề NHẠC NỀN khi không có nhạc; xem lại giới hạn số nguồn |
