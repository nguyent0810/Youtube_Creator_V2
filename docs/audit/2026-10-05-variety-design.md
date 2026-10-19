# Thiết kế bước 5: chống lặp khuôn + kiểm markup trước TTS (đề xuất 5 của audit)

Chốt sau 2 vòng phản biện Claude ↔ Grok. Bản đầu của Claude là một **cổng chặn** `gate.check()` gọi trong
`store.enqueue`, chặn theo ngưỡng câu trùng / Jaccard. Grok bác: chặn ở đó làm kẹt `sync_from_disk` và bỏ rơi
video đã dựng, và đo cho thấy lặp nằm ở **bộ sinh** (khuôn câu cố định, một file nhạc mỗi dòng), không ở từng
bundle. Bản cuối: sửa bộ sinh, đo vào brief, kiểm markup đúng chỗ còn hở.

## Đo trước khi làm (05/10/2026, 347 bundle, mỗi bài so với 30 bài trước cùng kênh)

| Dòng | Câu trùng nguyên văn với MỘT bài gần đây (trung vị) | Ghi chú |
|---|---|---|
| FS `lich-` (92, sinh bằng code) | 0,50 (max 0,89) | "Ngoài danh mục ấy..." 34 bài, "Sao mở, trực siết." 28, giờ tốt 30+16+10 |
| FS `menh-tue` | 0,83 | 12 cung chỉ khác câu hook: một video viết 12 lần |
| CL `cl-dieu` | 0,43 | |
| BUD `bud-lich` | 0,20 | |
| Còn lại (S-tier 91, các dòng BUD/CL khác) | ≈ 0 | |

Nhạc nền: **mỗi dòng đúng một file** (Lịch 92/92 `asian_drums.mp3`). Giọng: khác nhau theo dòng.
B-roll Lịch: 61 bài tháng 10–11 dùng chung 4 bộ hình (bộ sinh cũ); từ tháng 12 bám danh mục việc, 0 việc thiếu hình.

## Đã làm

1. **`menh_tue_sai` còn MỘT chủ đề** (`factory/pillars/topics.py`), giữ khoá `tue-sai-6` đã đăng để `next_draft`
   bỏ qua -- không sinh bản thứ 13.
2. **Lịch đa dạng cách nói** (`factory/compose.py`): `_pick(f, salt, xs)` -- mỗi danh sách tự chọn chỉ số theo độ
   dài của nó, băm (sao, trực, tên danh sách) + `ordinal // 12`. Thêm 3–4 cách nói cho các câu thân bất biến:
   câu kiêng ("mọi việc khác" / danh mục kiêng), câu giờ tốt, "Sao mở, trực siết.", "Hai tầng cùng một hướng...".
   Mọi ô dữ liệu (giờ, danh mục, nhánh "Mọi việc khác") vẫn lấy từ nguồn của ngày.
3. **Nhạc nền Lịch xoay theo ngày** (`compose.lich_bgm`, `scripts/make_lich_month.py`): 5 file FS đã dùng,
   `ordinal % 5`; chỉ chọn file có thật trong `vietneu-tts/bgm` (thiếu file thì `run_batch` dựng video không nhạc).
   Dòng khác giữ nhạc riêng (bản sắc series). `make_lich_month` báo việc chưa có hình riêng.
4. **Đo độ lặp khuôn** (`factory/sameness.py`, `scripts/sameness_report.py`, cuối brief tuần): mỗi dòng, 28 ngày
   cuối -- trung vị qua các video của tỉ lệ câu trùng **khuôn** (bỏ số, ngoặc, tên riêng) với MỘT video khác cùng
   dòng; top khuôn lặp; tỉ lệ nhạc nền / bộ hình phổ biến nhất (chỉ cho short `assemble`). Không bao giờ ném.
5. **Kiểm markup ngay trước TTS ở hai bộ dựng chưa có cổng** (`integrity.require_speakable`): `motion/long`
   `tts_line` (trước engine VÀ trước cache), `motion/stier` `speak` (cả hồ sơ, trước câu đầu). Soi chuỗi thô sắp
   đọc, không soi spec. Bắt được ngay một lỗi thật: `data/long/ripper/ch12.json` có nhãn `[DIỄN Ý]` trong lời đọc
   (parser chỉ bóc `**[DIỄN Ý]**`) -- đã sửa parser + dữ liệu.

## Quyết định

| # | Quyết định | Vì sao |
|---|---|---|
| 1 | **Không** cổng chặn trong `enqueue` / `save_bundle` | `sync_from_disk` là vòng `enqueue` tự commit: một file trượt làm mọi file sau không vào hàng đợi, và bộ sinh không ghi đè file đã có -> kẹt vĩnh viễn. S-tier / `publish_long` gọi `enqueue` SAU khi đã dựng -> video bị bỏ rơi |
| 2 | Không ngưỡng chữ cứng | Câu trùng 0,5 chỉ là sàn khuôn của Lịch; Jaccard 0,6 không tách được gì ở các dòng khác |
| 3 | Lịch không bị chặn mà **sửa bộ sinh** | Bộ sinh tất định: chặn không làm nó viết khác đi |
| 4 | Chọn biến thể theo `ordinal // 12`, mỗi danh sách tự `% len` | Cặp (sao, trực) lặp 12 ngày -> lần sau chắc chắn lệch; `day // 12` reset đầu tháng; `v % 6` rồi `% 4` lệch về chỉ số 0, 1 |
| 5 | Chỉ xoay nhạc **Lịch** | Dòng 7 bài một nhạc là bản sắc series; 92 bài + mỗi ngày một bài mới là "hàng loạt" |
| 6 | Số đo = max theo hàng xóm rồi trung vị | Trung vị mọi cặp giấu đúng bài sinh đôi |
| 7 | Markup chỉ soi chuỗi sắp đưa vào `infer` | Spec S-tier có `*7 NGÀY*` (tiêu đề cảnh) và URL nguồn hợp lệ; câu lặp ở S-tier/long có thể cố ý |
| 8 | Không ghi lại bundle cũ | Bundle bất biến; video đã/đang lên kênh khớp bundle |

## Kết quả

- 120 ngày Lịch giả lập (chu kỳ sao/trực thật): khuôn câu trùng trung vị **0,75 → 0,50**; câu nguyên văn
  **0,62 → 0,38**; mọi biến thể vẫn qua `factcheck` (test). Phần 0,50 còn lại là các câu mang dữ liệu
  ("Sao là X, thuộc nhóm...", "Trực là X — ..., nghĩa là ...", "Danh mục nên làm: ...").
- Quét 3.616 câu S-tier + video dài trên đĩa: 1 câu có markup (lỗi `[DIỄN Ý]` ở trên), đã sửa -> 0.
- Kiểm đột biến: 16 đột biến, đều bị bắt (2 lỗ test được lấp trong lúc kiểm).

## Chưa làm / lưu ý

- **Lịch đã sinh sẵn tới 31/12/2026** và bộ sinh không ghi đè -> thay đổi (2)(3) tới người xem từ **01/01/2027**.
  Muốn sớm hơn: sinh lại các ngày CHƯA upload trên máy sản xuất (cần biết ngày nào chưa lên kênh).
- `cl-dieu` (43%), `bud-lich` (80% theo khuôn), các dòng pillar FS (60–80% theo khuôn) hiện ra trong brief --
  sửa ở bộ sinh từng dòng là việc kế tiếp, theo số đo.
- Máy này thiếu `vnlunar` nên chưa chạy `make_lich_month` thật; test dùng ngày giả lập theo đúng chu kỳ.
