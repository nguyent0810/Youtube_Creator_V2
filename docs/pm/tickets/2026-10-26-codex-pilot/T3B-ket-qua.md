# T3B — Kết quả: Long `mim-katherine-johnson`

Ngày 26/10/2026. Claude làm thay Codex (Codex hết quota), theo đúng ticket T3B và `AGENTS.md`. Không render, không upload, không chạy `thumb.py`, không ghi `state.sqlite`, không đụng git hay code dùng chung.

## Số liệu `long_gate` (bản thật, sau TTS)

```
python scripts/long_gate.py mim-katherine-johnson --min-syl 1900
mim-katherine-johnson: âm tiết 2148, phút 9.8, cảnh 80, giây/cảnh 7.4, clip khác 9, ảnh khác 17, URL nguồn 38
ĐẠT
```

`long_gate` chỉ đếm cảnh thân, tức là 80 cảnh thân cộng 8 thẻ chương. Gate không đọc file ảnh nên không vướng ảnh AI.

## Lệnh đã chạy

| Bước | Lệnh | Kết quả |
|---|---|---|
| 1 | `script_lines.py` | Qua cổng integrity: 138 câu, 2.148 âm tiết, 8 chương |
| 2 | `gen_scenes.py` | Tạo `spec.json` và `ch00–ch07.json`. Giữ `lines`/`title` của `script_lines` (gen_scenes đọc file cũ rồi chỉ cập nhật các khoá của nó). Đã chạy lại `script_lines` sau đó |
| 3 | `studio_lint --strict` | 0 lỗi, 0 cảnh báo (có sửa tỉ lệ câu ngắn bằng cách rút gọn câu có sẵn, không thêm câu đệm) |
| 4 | `build_long.py tts` | Xong 8 chương, tổng 9,83 phút |
| 5 | `build_long.py html` (bản thật) | Dừng ở `EXT:ai:ai_01: chưa có ai01.jpg`. Đây là lỗi thiếu ảnh AI, được chấp nhận |
| 5b | `gen_scenes.py --standin`, rồi `html` | Thay tạm 6 ảnh AI bằng ảnh tư liệu để soát phần còn lại. Đủ 8 chương, không lỗi. Đã sửa 1 dòng sổ tràn thẻ và 2 dòng chữ chép nguyên lời đọc. `late_report`: không có màn trống đầu cảnh |
| 6 | `pexels.py search/get` | Tải 11 clip ứng viên. Id 8195667 không ra trong các lượt tìm nên không tải |
| 7 | `media_search.py get … nasa` | Tải 4 ảnh NASA của Friendship 7, đều PD |
| 8 | `clip_sheet.py` | `output/long/mim-katherine-johnson/qa_clips.jpg`. Đã xem ảnh. Loại 11899304 (màn hình và bàn phím văn phòng hiện đại) và 5466768 (có tiền giấy đô la). Không thấy logo hãng |
| 9 | `gen_scenes.py` (bản thật) → `script_lines` → `studio_lint` → `long_gate` | 0 lỗi, ĐẠT |

**Chú ý:** các file `*.html` và `data.js` hiện nằm trong `output/long/mim-katherine-johnson/` được dựng từ bản thay tạm. Không render từ chúng. Còn `spec.json` và `chNN.json` hiện đã là bản thật, trỏ 6 ảnh AI. Khi ảnh về, phải chạy lại `html`.

## Checklist ticket

| Mục | Có/Không | Ghi chú |
|---|---|---|
| Cold open 20/02/1962, Glenn muốn Johnson kiểm tay | Có | Theo đề xuất T3A. Không nói việc kiểm diễn ra đúng ngày 20/02, chỉ nói "trong phần kiểm tra trước chuyến bay" |
| 1.900–2.300 âm tiết, 8 chương | Có | 2.148 âm tiết |
| Không câu đệm | Có | Gate không bắt câu nào trong danh sách. Câu ngắn đặt sau phán định ("Glenn không bỏ máy.", "Bài toán đổi chiều.") |
| Phim chỉ bằng lời và chữ, không kể chi tiết hư cấu như thật | Có | Cảnh nhà vệ sinh và cú gọi sát giờ phóng chỉ nêu kèm quy dẫn NASA/TIME (dữ kiện 35, 36) |
| Dorothy Vaughan ≤ 1 câu | Có | Chỉ ở CH02 câu 6 |
| Không "IBM 7090", không con số sai số | Có | Chỉ nói "máy tính IBM" |
| `titles[0]` ≤ 60 ký tự, có 2 phương án dự phòng | Có | "HIDDEN FIGURES Ngoài Đời Thật: Katherine Johnson" (48 ký tự) |
| `spec.youtube` đủ 11 trường | Có | Có thêm `titles`. `publish_at` 2026-11-25T13:00:00Z, playlist "Công Nghệ Quanh Ta", category 28, thumb t1.jpg, 9 URL nguồn |
| `SAY` cho tên Anh, địa danh, viết tắt | Có | Khoảng 60 mục (NASA, NACA, IBM, Langley, Canaveral, Bermuda, Skopinski…) |
| Thẻ chương đúng trường `no`/`k`/`title`/`sub`/`bg`/`titleAt` | Có | |
| `hud` ở mỗi chNN | Có | |
| 60–80 cảnh, ≤ 9 giây/cảnh, ≥ 5 loại/chương | Có | 80 cảnh thân (88 nếu tính thẻ chương), 7,4 giây/cảnh, 7–10 loại mỗi chương |
| Không khuôn; chữ không lặp quá 2 lần; mô-típ qua `ledger` | Có | Một ledger "SỔ CỦA MỘT CON SỐ ĐÁNG TIN", mỗi chương thêm một dòng. Gate không bắt chữ lặp |
| Ưu tiên ảnh kho, mỗi ảnh ≤ 3 lần | Có | 9/9 ảnh Commons I01–I09, cộng 4 ảnh NASA (I13, I14 và 2 ảnh Friendship 7 khác). Ảnh dùng nhiều nhất 2 lần. Không dùng I10–I12 vì chỉ là trang ảnh NASA, đã có bản Commons tương đương |
| ≥ 6 clip khác nhau, mỗi clip ≤ 2 lần, soát bằng clip sheet | Có | 9 clip; 854266 dùng 2 lần, còn lại 1 lần |
| Counter: năm khai `year: true`, số lượng `false` | Có | 1937 → `true`; 16 năm và 26 báo cáo → `false` |
| Ảnh AI ≤ 6, đúng định dạng, người thật chỉ thấy từ sau/nghiêng quay đi, không chữ, không nhãn AI | Có | `data/long/mim-katherine-johnson/ai_prompts.md` |

## Ảnh và clip

- **Ảnh tư liệu:** `kj1966`, `kjComp`, `kj1980`, `kj1983`, `kj1985`, `kj2014`, `kjMedal`, `paper`, `kjGlobe` lấy từ Commons; `launch`, `glennIn`, `orbitCam`, `pad` lấy từ images.nasa.gov. Tất cả đều PD hoặc No restrictions.
- **Clip Pexels:**
  - 854264 (đếm ngược, ch00);
  - 3196291 (bảng đen, ch01);
  - 5682784 (nhóm tính toán, ch02);
  - 6272049 (tay cầm phấn, ch03);
  - 8197039 (bảng xanh, ch03);
  - 9056542 (máy tính và giấy, ch04);
  - 854262 (tên lửa, ch04);
  - 854266 (tàu con thoi, ch05 và ch06);
  - 3196425 (phụ nữ viết phương trình, ch07).

## Ảnh AI: chờ 6 ảnh

- **Danh sách và chỗ dùng:**
  - `ai_01`: phòng West Area Computing (ch02, ch03);
  - `ai_02`: máy tính cơ trên bàn ban đêm (ch05);
  - `ai_03`: Johnson nhìn từ phía sau tại bàn (ch00);
  - `ai_04`: cô bé 13 tuổi đi vào khuôn viên trường (ch01);
  - `ai_05`: minh hoạ nhiễu động vệt đuôi (ch04);
  - `ai_06`: lớp học trường dành cho học sinh da đen, thập niên 1930 (ch01).
- **Vênh giữa luật và engine** (ghi lại để Claude quyết, tôi không sửa code dùng chung):
  - `AGENTS.md` bảo thả ảnh vào `assets/long/<topic>/img/ai/ai_NN.png`.
  - Nhưng `build_long.fetch_img` chỉ đọc ảnh qua `spec.imgs`. Với ref `EXT:…`, nó cần cặp `output/long/<topic>/img/<key>.jpg` và `<key>.json`.
  - Vì vậy `gen_scenes.py` khai `AI_PATH` trỏ đúng đường dẫn `img/ai/ai_0N.png` mà luật yêu cầu, và trong `spec.imgs` khai `"ai0N": "EXT:ai:ai_0N"`.
  - Khi ảnh về, cần chuyển `img/ai/ai_0N.png` thành `img/ai0N.jpg`, kèm `ai0N.json` dạng `{"file","license","artist","title","source"}`, rồi mới chạy được `html`.
  - Thư mục `output/long/mim-katherine-johnson/img/ai/` đã có sẵn và đang trống.
  - `describe.py` sẽ đọc `license` trong json đó để in phần ghi công. Cần chọn giá trị sao cho mô tả không ghi "AI", đúng quyết định của chủ kênh.

## Không kiểm được

- **URL nguồn:** tôi không mở lại từng URL. Dùng nguyên kho `facts.md` mà T3A đã mở và Claude đã duyệt. Giấy phép ảnh Commons I01–I09 thì đã kiểm lại qua API Commons.
- **Hình hiển thị và phát âm:** chưa render, nên chưa xem được khung hình thật (tràn chữ, bố cục bản đồ, thẻ chương) và chưa nghe được phát âm theo bảng `SAY`.
- **Clip:**
  - 854264 có đồng hồ đếm "0:0" nhỏ ở góc trên trái. Đây là số, không phải thương hiệu; tôi đã chấp nhận.
  - Clip 854266 có đoạn khung 4:3 chất lượng thấp, tuỳ đoạn engine cắt.
  - Ba clip tên lửa là tàu con thoi hiện đại. Chúng mang nhãn VIDEO MINH HỌA và chữ trên màn hình không gọi chúng là Friendship 7 hay Freedom 7.
- **Thumbnail:** chưa dựng, vì ticket cấm `thumb.py`.

## File

- `data/long/mim-katherine-johnson/`: `script.md`, `factcheck.md`, `gen_scenes.py`, `ai_prompts.md`, `spec.json`, `ch00–ch07.json`
- Clip sheet: `output/long/mim-katherine-johnson/qa_clips.jpg`
