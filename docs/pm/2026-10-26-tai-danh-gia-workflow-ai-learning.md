# Tái đánh giá workflow AI Learning (vietneu-tts) từ 20/10 tới 26/10/2026, chọn phần đưa vào V2

Ngày 26/10/2026. Lần này chỉ đánh giá: không sửa code V2, không commit, chỉ đọc repo vietneu-tts.

- **Nguồn (A):** `D:\Tools\Youtube Creator v2\vietneu-tts`, `git log origin/main --since=2026-10-20`, 29 commit (PR #26, #27, #29, #30, #32, #33).
- **Đích (B):** repo này, gồm MIM, CK và CL.
- **Cách làm:**
  - Với mỗi mục, đọc commit và ADR ở (A).
  - Tìm mục tương đương trong `motion/long`, `motion/stier`, `motion/hf/assets/engine`, `factory`, `scripts`, `tests`.
  - Đo trên dữ liệu của (B) khi có thể: độ to của Short/Long, nhịp cảnh của 43 Long, SEO của 43 Long, `check.json` của Short, các counter có giá trị dạng năm.
- **Bối cảnh (B):**
  - Bài học "chép cơ chế, không chép bề mặt": BUD thua khi chép bề mặt của FS.
  - Long đo được: CL CTR 3,4%, AVD 9:28; MIM/CK Long CTR 1,6–2,6%.
  - Không sửa video đã đăng. Chỉ thay video riêng tư đã upload khi lỗi làm đổi nghĩa.

## 1. Bảng tổng hợp

Cột "Kiểm chứng ở A":

- **số kênh**: có số đo kết quả trên kênh;
- **số kỹ thuật**: có đo trước/sau trên file, chưa có số kênh;
- **giả thuyết**: chưa đo.

| # | Mục (A) | Commit | B đã có? | Kiểm chứng ở A | Đặc thù FS/BUD? | Khuyến nghị | Giờ | Rủi ro chính |
|---|---|---|---|---|---|---|---|---|
| 1 | Năm hiện "1.863" (counter chấm nghìn) | cef6509 | **Chưa. Lỗi có thật ở B**: Short MIM đã đăng hiện "1.996" | số kỹ thuật | Không | **ÁP NGAY**, dùng cờ tường minh thay cho heuristic | 1,5 | Đổi `casewide.js`/`casefile.js` (dùng chung) thì khoá render của Long đang dựng dở bị đổi |
| 2 | Limiter đỉnh thật (bước cuối ticket 68) | 8efd3e1 | Một phần: B đo TP và chặn, nhưng không chặn đỉnh bằng limiter | số kỹ thuật | Không | **ÁP NGAY** | 1,5 | Bước ghép cuối dùng chung cho cả 3 kênh |
| 3 | Khoá chương băm nội dung file local | 08c3d94 | **Chưa**: `render_key` không băm ảnh | số kỹ thuật (1 lỗi thật) | Không | **ÁP NGAY** | 1 | Khoá đổi thì các chương đang dở render lại một lần |
| 4 | Sổ thất bại (ADR 0017 §5) | 6da1db3 | Rải trong retro và memory, chưa có một bảng | quy trình | Không | **ÁP NGAY** (chỉ tài liệu) | 1 | Không |
| 5 | Pacing p50/p90, cảnh > 25 s cần `slow_hold` | 882346f | Chưa có số liệu nhịp; có `late_first`, `qa_blank`, `studio_lint` | số kỹ thuật, ngưỡng 2–4 s chưa A/B | Không | **ÁP CÓ CHỈNH**: chỉ báo/cảnh báo, không chặn | 2 | Thấp, chỉ là kiểm |
| 6 | `seo_check` trước khi đăng Long + `seo.keyword` | 7fb3867, e0859a0 | Phần lớn đã đạt; thiếu keyword và cảnh báo tiêu đề | audit tình trạng, chưa có số kết quả | Không | **ÁP CÓ CHỈNH**: bản tối giản | 1,5 | Không đụng engine |
| 7 | `gate_overflow`: mọi `*_overflow` chặn, 0 mẫu cũng là lỗi | 552b4e3 | Có `check_gate`, nhưng chỉ cho BUD v2 và chỉ lỗi mức `error` | số kỹ thuật (14 short đạt, bắt 2 lỗi thật) | Không | **ÁP CÓ CHỈNH**: cảnh báo trước, chặn sau | 3–4 | Thêm 1–2 phút mỗi Short; dương tính giả trên phần trang trí |
| 8 | Dấu chồng chữ hoa bị `clipPath inset(0%)` cắt | 3725e1d, ea7c12a | Có `diacritics_gallery` (lab/chart), nhưng còn 2 chỗ chưa phủ | số kỹ thuật | Không | **ÁP CÓ CHỈNH** | 2 | Engine dùng chung; cần gallery xác nhận |
| 9 | Điểm rơi dốc nhất của Short + câu đang đọc (ticket 71) | 7721a73 | Có đường giữ chân (`monitor.py`, `analytics_report.py`), chưa ghép với câu | 1 lần chạy BUD | Không | **ÁP CÓ CHỈNH** | 3 | Chỉ đọc |
| 10 | Lint khuôn nhân vật Long (4 mã) | e0859a0 | Chưa có lint. Khuôn này **gốc từ CL** | giả thuyết (A chưa có số) | Không (gốc CL) | **ÁP CÓ CHỈNH**: chỉ cảnh báo, ngưỡng theo CL | 3 | Không |
| 11 | Cổng Long tách nội dung / phân phối | 82d9901 (ADR 0001) | Chưa có tiêu chí duyệt Long | giả thuyết (đọc 22/11) | Không | **ÁP CÓ CHỈNH**: ngưỡng theo B | 1 | Không |
| 12 | Gỡ "mùi AI": bỏ `back.out`/`bounce`, chữ đã hiện thì đứng yên | cef6509 | B ít hơn nhiều (casewide 3+1, chart 10, lab 4) | giả thuyết thẩm mỹ | Không | **ÁP CÓ CHỈNH**: chỉ engine Long | 1,5 | Engine dùng chung |
| 13 | Nhạc lấn giọng bị loại khỏi Long; SFX −12 dB; `duck_db` | 8efd3e1 | Có ducking bằng sidechain; chưa đo bài lấn giọng; chưa biết mức SFX | số kỹ thuật | Không | **ÁP CÓ CHỈNH**: đo trước, rồi mới đặt ngưỡng | 2 | Thấp |
| 14 | Đo bằng bài trúng, nhân khuôn sớm, luật dừng khuôn | e073e37, 6da1db3 | Đã có luật dừng theo % ở lại; chưa có "bài trúng" | **số kênh** (FS), ngưỡng của FS/BUD | Ngưỡng thì có, cơ chế thì không | **THỬ (backtest)** trên dữ liệu B | 2 | Chỉ đọc |
| 15 | AVP so theo nhóm độ dài | e073e37 | B đo AVP thô: r ≈ −0,1 với view (MIM) | **số kênh** (FS) | Ngưỡng thì có | **THỬ (backtest)** trước khi đưa vào brief | (gộp #14) | Chỉ đọc |
| 16 | Độ to hai lượt; Long −16 LUFS | 8efd3e1 | B đã đạt đích (Long −14,0; Short −14,2 tới −15,2) | số kỹ thuật | Không | **BỎ QUA** (giữ −14) | 0 | — |
| 17 | Ảnh dọc tự vào khung 16:9; media `crop` | 08c3d94 | Đã có `motion/mediafit.py` (cover/blur) | — | Ảnh AI (A) | **BỎ QUA** | 0 | — |
| 18 | Thư viện motion 234 mẫu | a4aa970 | — | chấm theo tiêu đề, chưa xem video | Có (độ hợp FS/BUD) | **BỎ QUA** (quy ước ease đã gộp vào #12) | 0 | — |
| 19 | Dấu 吉 cạnh chữ nghĩa xấu; nhãn tư liệu/stock/ảnh AI | 5d68250 | — | — | Có | **BỎ QUA** | 0 | — |
| 20 | `review_yeartable` (vệt sáng bảng năm) | 4e918ec, 487573c | — | — | Có | **BỎ QUA** | 0 | — |
| 21 | `hf_long_retention` | e0859a0 | **B là gốc** (`monitor.py`) | — | — | **BỎ QUA** | 0 | — |

## 2. Chi tiết từng mục

### 1. Năm hiện thành "1.863" (ÁP NGAY, có chỉnh)

**(A) đã làm gì.** Ở `longform.js` (cef6509), một số nguyên từ 1000 tới 2100, không có hậu tố, và nhãn không chứa từ chỉ đơn vị đếm thì được coi là năm, nên không chấm nghìn. Spec ghi `plain` thì cờ này thắng heuristic. Test: `tests/test_longform_motion_spec.py`.

**(B) hiện tại.**

- Lỗi này có thật ở B. Hàm `vn()` ở `casewide.js:318/324` và `casefile.js:180/184` luôn chấm nghìn.
- Short `mim-turing-1950-loi-doan` có counter 1950 → 2000, nhãn "NĂM TURING HẸN". `final_sheet.jpg` cho thấy khung giữa hiện **"1.996"**. Short này đã upload, hẹn 14/10.
- `studio_lint` chặn counter đếm tới một năm, nhưng chỉ chạy cho Long. Luật đó cũng không bắt lỗi định dạng số.

**Không chép heuristic của (A).** Chạy heuristic ấy trên spec của B thì sai ít nhất 4 counter đếm số lượng:

- `golden/ch06`: 1000, nhãn "QUÂN QUỐC DÂN ĐẢNG BÁM THEO";
- `shanghai/ch10`: 1000, "MẶT NẠ PHÒNG ĐỘC";
- `mim-ai-jobs/ch06`: 1208, "SUẤT NỘI TRÚ…";
- `yakuza/ch10`: 2000, "THÀNH VIÊN BỊ LOẠI MỖI NĂM". Nhãn có chữ "NĂM" nên luật cũ của A cũng coi nhầm là năm.

**Đề xuất.**

1. Thêm cờ tường minh `"year": true` trong spec counter. Có cờ thì engine không chấm nghìn.
2. Thêm lint chặn: counter có `from` hoặc `to` trong khoảng 1000–2100, không có `suffix` và không khai `year` → bắt người viết khai `year: true|false`.
3. Đặt lint ở `build.py` (Short) và `studio_lint` (Long).

**Ước lượng.** Khoảng 1,5 giờ, kèm test.

**Rủi ro.**

- Sửa `casewide.js` làm đổi `render_key` của mọi Long đang dở. Nên làm giữa hai lô.
- Short Turing đã đăng: theo luật thay video, đây là lỗi hình thức (số vẫn đọc ra năm), nên giữ nguyên. Hỏi chủ kênh nếu muốn thay.

### 2. Limiter đỉnh thật (ÁP NGAY)

**(A) đã làm gì.** `hyperframes_bridge.mux_audio` (8efd3e1):

1. trộn;
2. đo;
3. tăng gain tới đích;
4. `aresample=192000,alimiter=…` chặn đỉnh thật ở −1 dBTP;
5. đo lại.

Lý do: loudnorm một lượt chỉ ra Short FS −20,8 LUFS, BUD −17,9 LUFS. Sau khi sửa: −14,2 LUFS, đỉnh −1,3 dBTP.

**(B) hiện tại.**

- Bước ghép cuối của Long (`build_long.py:1036`) và của Short (`stier/build.py:791`, `themes.py:211`) dùng loudnorm một lượt, `TP=-1.5`.
- Long của B **đã đạt độ to**: log có 25 lần đo, tất cả từ −14,0 tới −14,2 LUFS.
- Nhưng **5/25 lần có true peak > −1 dBTP** (−0,5, −0,7 ×3, −0,9). Với CL, `audio_lint` khi đó **xoá final.mp4 và chặn**, nên phải ghép lại.
- Short: đo 8 Short mới nhất, được −14,2 tới −15,2 LUFS, hụt nhẹ.

**Đề xuất.** Thêm `aresample=192000,alimiter=limit≈-1.5dB…,aresample=48000` sau loudnorm, ở cả hai nơi ghép cuối. Không cần đổi sang hai lượt.

**Ước lượng.** 1,5 giờ, kèm đo lại 2 Long và 2 Short.

**Rủi ro.** Thấp. Đây là bước cuối của cả 3 kênh, nên đo lại bằng `audio_lint` trước khi áp chung.

### 3. Khoá chương băm nội dung file (ÁP NGAY)

**(A) đã làm gì.** Thay ảnh mà giữ nguyên tên thì render báo "đã có" và dùng chương cũ. Sửa ở 08c3d94: `chapter_key` băm cả nội dung ảnh local (với clip thì lấy cỡ + mtime).

**(B) hiện tại.** `build_long.render_key` băm `data.js`, composition, engine và ID của B-roll. Nó **không băm ảnh**, nên thay ảnh trùng tên sẽ gặp đúng lỗi này.

**Đề xuất.** Băm thêm cỡ + mtime (hoặc sha1) của mọi ảnh/clip local mà `data.js` tham chiếu.

**Ước lượng.** 1 giờ.

**Rủi ro.** Khoá đổi nên các chương đang dở render lại một lần.

### 4. Sổ thất bại (ÁP NGAY, chỉ tài liệu)

**(A) đã làm gì.** ADR 0017 §5: một bảng 22 dòng gồm thử gì, số đo, bài học, đã đổi thành gì. Phải đọc bảng này trước khi mở chuỗi mới.

**(B) hiện tại.** Bài học nằm rải trong `docs/pm/*retro*` và memory (copy-mechanism, upload limit, mix standard…).

**Đề xuất.** Tạo `docs/pm/so-that-bai.md`, gom các thất bại đã có số:

- BUD chép bề mặt FS;
- CK bị chặn upload sau khoảng 10 video/ngày;
- Shorts chững ở khoảng 1k;
- Long MIM/CK CTR 1,6–2,6%;
- CL "sẹt sẹt";
- …

Chỉ là tài liệu, không cần code.

**Ước lượng.** 1 giờ.

### 5. Pacing p50/p90, cảnh > 25 s (ÁP CÓ CHỈNH)

**(A) đã làm gì.** `hf_batch_render.pacing()` (882346f) báo:

- p50/p90 giây mỗi cảnh, nhịp phút đầu và phút cuối (cảnh báo khi trên 4 s/cảnh);
- cảnh đứng hơn 25 s thì **chặn**, trừ khi spec ghi `"slow_hold": {"<câu>": "lý do"}`.

Ngưỡng 2–4 s lấy từ dữ liệu nhà cung cấp (33 video), chưa có A/B (ADR 0009).

**(B) đo trên 43 Long.** Tính bằng `t0` các cảnh trong `data.js`:

- **MIM:** p50 4,5–9,5 s, p90 8,2–16 s. Chỉ 3/23 Long có cảnh > 25 s.
- **CK:** p50 5,4–9,8 s, p90 11–22 s. 11/20 Long có cảnh > 25 s, dài nhất 37 s. Phần lớn là `ledger`/`bars`/`candles` (ví dụ `ck-d1-vang-dinh` ch06 37 s, `ck-c3-bieu-do-nen` có 5 cảnh > 25 s).
- **Lưu ý:** cảnh của B chứa beat chữ chạy bên trong, và `ledger` hiện từng hàng, nên "một cảnh" không có nghĩa là hình đứng yên.

**Đề xuất.**

- Thêm vào `build_long` (bước html) một dòng báo p50/p90/max cùng danh sách cảnh > 25 s.
- Cảnh > 25 s **chỉ cảnh báo**, kèm khoá `slow_hold` để ghi lý do.
- Nếu thêm `qa_blank` cho Long thì chỉ đo "hình đứng yên thật" (khung hình không đổi).
- Không chặn cho tới khi có số giữ chân CK cho thấy cảnh dài làm rơi.

**Ước lượng.** 2 giờ.

**Rủi ro.** Thấp, vì đây chỉ là kiểm.

### 6. `seo_check` trước khi đăng Long (ÁP CÓ CHỈNH)

**(A) đã làm gì.** `seo_check.check_row` chạy trong `upload_long.py` (ADR 0016):

- **ERROR:**
  - keyword không nằm trong 4 từ đầu tiêu đề hoặc trong 150 ký tự đầu mô tả;
  - hơn 60 hashtag;
  - thumbnail sai cỡ hoặc nặng hơn 2 MiB.
- **WARN:** tiêu đề > 60 ký tự, dưới 8 tag, hơn 5 hashtag, thiếu mốc chương, keyword không có trong 3 câu đầu.

Bằng chứng là audit tình trạng của chính A (165/225 Long thiếu mốc chương…). Chưa có số kết quả.

**(B) audit 43 Long.**

- Đã đạt:
  - thiếu mốc chương: 0;
  - dưới 8 tag: 0;
  - hơn 5 hashtag: 0;
  - mô tả dưới 200 từ: 0;
  - thumbnail đúng 1280×720 và dưới 2 MB: 46/46.
- Còn thiếu:
  - `keyword`: 0/43 spec có khai;
  - tiêu đề > 60 ký tự: 31/43. Khuôn "X Ngoài Đời Thật" của CL thường dài nên chỉ cảnh báo.

**Đề xuất.**

- Thêm `spec.youtube.seo.keyword`.
- Trong `publish_long.preflight`:
  - **chặn** khi keyword không nằm trong 4 từ đầu tiêu đề hoặc 150 ký tự đầu mô tả;
  - **cảnh báo** khi tiêu đề > 60 ký tự, hoặc tag đầu khác keyword.
- Không bê cả `seo_check.py`, vì B đã có `describe.py` và luật mô tả không chứa ghi chú nội bộ.

**Ước lượng.** 1,5 giờ.

**Rủi ro.** Không đụng engine.

### 7. `gate_overflow` (ÁP CÓ CHỈNH)

**(A) đã làm gì.** `hf_qa.gate_overflow` (552b4e3) chạy `hyperframes inspect` bằng font thật, rồi:

- coi **mọi** phát hiện `*_overflow` là lỗi, bất kể mức;
- coi 0 mẫu là lỗi;
- cho qua phần tràn có chủ đích nếu gắn `data-layout-allow-overflow`.

Lý do: lô TN2 lọt tiêu đề 18 ký tự cỡ 96 px và lưới 5 cột tràn mép.

**(B) hiện tại.**

- `stier/build.check_gate` chạy `hyperframes check`, nhưng **chỉ cho `theme=bud` + `v2`**, và **chỉ chặn mức `error`**. Đây đúng là điểm mù mà A vừa vá.
- Đếm `output/stier/*/check.json`: **37/51** file có phát hiện tràn bị bỏ qua. Tổng cộng 203 phát hiện: 129 `canvas_overflow`, 71 `container_overflow`, 2 `text_box_overflow`, gần hết ở mức `info`.
- MIM/CK/CL dựa vào ước lượng bằng `text_em`: kinetic `size` > 980 px, dòng phụ > 52 ký tự, `beatfx.overflow_lines` cho Long. Cách này không đo bằng font thật.

**Đề xuất.**

1. Mở rộng `check_gate` (hoặc thêm `inspect`) cho mọi theme Short.
2. Đếm `*_overflow` ở mọi mức.
3. Gắn `data-layout-allow-overflow` cho phần trang trí như vệt sáng, grain, vignette.
4. Chạy **1 tuần ở chế độ cảnh báo**, đọc lại 203 phát hiện cũ để lọc dương tính giả, rồi mới chuyển sang chặn.

**Ước lượng.** 3–4 giờ.

**Rủi ro.** Mỗi Short thêm khoảng 1–2 phút `npx`. Nếu chặn sớm thì kẹt chuỗi render.

### 8. Dấu chồng chữ hoa (ÁP CÓ CHỈNH)

**(A) đã làm gì.**

- Thẻ chữ khoá và tiêu đề kết thúc bằng `clipPath inset(0%)` cắt dấu dòng đầu ("THỀ" thành "THÊ"). A đổi sang lề âm `inset(-40% … -40% …)` (3725e1d).
- Thiết bị `window` tô thiếu vùng dấu (ea7c12a).

**(B) hiện tại.**

- Đã có `diacritics_gallery.py` cho theme lab/chart. Ảnh `22_chapter.png` cho thấy đủ dấu.
- **Chưa phủ hai chỗ:**
  - `casewide.js:117`, thẻ chương deco (theme shanghai, CL): `clipPath: inset(0% 0% 100% 0%)` → `inset(0% 0% 0% 0%)`. Đây đúng mẫu lỗi của A, mà gallery không dựng theme `case`/deco.
  - `bang-tra-looks.js:102/219/302/347/359`: hiện hàng bằng `inset(0 … 0 …)`, cạnh trên/dưới bằng 0. Look này dùng cho Short MIM/CK đang chạy.
- B không có thiết bị `window`, nên bỏ qua phần đó.

**Đề xuất.**

- Mở rộng gallery sang theme `case` (cả deco) và các look `bang-tra`.
- Chỗ nào gallery thấy mất dấu thì đổi sang lề âm theo cách của A.

**Ước lượng.** 2 giờ, gồm 1 lần render gallery.

**Rủi ro.** Engine dùng chung, nhưng gallery là lưới an toàn.

### 9. Điểm rơi dốc nhất của Short (ÁP CÓ CHỈNH)

**(A) đã làm gì.** `hf_brief` (7721a73) lấy đường giữ chân (cửa sổ 7 ngày PT) của n Short thấp nhất và n Short cao nhất trong tuần sạch, tìm giây rơi dốc nhất, ghép với câu TTS đang đọc, rồi gom theo các nhóm 0–2, 2–5, 5–10, ≥ 10 s.

Kết quả 1 lần chạy BUD: rơi dốc nhất ở giây 4,4–5,1, đúng lúc sang câu 2. ADR 0006 ghi câu 2 cụ thể rơi 3,4%/s, câu 2 chung chung rơi 8,1%/s.

**(B) hiện tại.**

- `monitor.py` và `analytics_report.py` đã lấy `audienceWatchRatio`, nhưng chỉ đọc ở vài mốc cố định (60 s, 120 s cho Long).
- `timing.json` của mỗi Short đã có mốc câu.

**Đề xuất.** Thêm vào scoreboard/brief một mục "điểm rơi + câu đang đọc" cho Short MIM/CK/CL. Đây là dữ liệu để thử theo kiểu "chép cơ chế" (câu 2 cụ thể), không phải luật mới.

**Ước lượng.** 3 giờ.

**Rủi ro.** Chỉ đọc. Lỗi API thì chỉ ghi một dòng báo.

### 10. Lint khuôn nhân vật Long (ÁP CÓ CHỈNH)

**(A) đã làm gì.** `long_script_lint.py`, với `format: "nhan_vat"`, có 4 cảnh báo:

- `CAU_HOI_HEN_CHUONG`: 2–3 câu hỏi trong 90 s đầu, hẹn đúng số chương có thật;
- `SO_CHUONG`: 12–16 chương;
- `THOI_LUONG`: ≥ 30 phút;
- `NHAN_VAT`: tên nhân vật có trong cold open và trong ≥ 70% chương.

A chưa có số kết quả. Bốn tập thử đọc vào 22/11 và 01/12.

**Bối cảnh B.** Khuôn này **lấy từ CL** (ADR 0001 dẫn AVD 9:28 của CL). B có bảng khuôn thắng trong `docs/pm/2026-10-22-cl-ke-hoach-long-ngoai-doi-that.md`:

- một nhân vật;
- cold open có ngày giờ;
- 25–32 phút, 13–14 chương.

B chưa có lint cho khuôn này.

**Đề xuất.**

- Viết lint cảnh báo theo ngưỡng của B (13–14 chương, 25–32 phút, không ép ≥ 30 phút).
- Áp cho CL và các Long MIM dạng nhân vật (alphago, deep-blue, siri…).
- Chép cơ chế (câu hỏi hẹn chương, nhân vật xuyên suốt), không chép ngưỡng của A.

**Ước lượng.** 3 giờ.

**Rủi ro.** Không đụng render.

### 11. Cổng Long: nội dung và phân phối (ÁP CÓ CHỈNH)

**(A) đã làm gì.** ADR 0001 sửa ngày 24/10 tách hai cổng:

- **Cổng nội dung** (cần ≥ 2/3): AVD ≥ 6 phút, còn ≥ 60% ở phút 1, CTR ≥ 4,5%.
- **Cổng phân phối** (cần 1/2): ≥ 300 view/7 ngày, hoặc lượt hiển thị ≥ 2 lần trung vị.

Qua cổng nội dung mà rớt cổng phân phối thì sửa đóng gói, không bỏ khuôn.

**Đề xuất cho B.**

- Dùng cách đọc hai cổng này cho duyệt Long MIM/CK.
- Ngưỡng lấy từ B:
  - CL (AVD 9:28, CTR 3,4%) làm mốc trên;
  - CTR MIM/CK hiện 1,6–2,6%, nên ngưỡng 4,5% của A quá cao để làm cổng ban đầu.
- Ghi vào doc kế hoạch Long.

**Ước lượng.** 1 giờ, chỉ tài liệu.

### 12. Gỡ "mùi AI" trong engine Long (ÁP CÓ CHỈNH)

**(A) đã làm gì.** cef6509:

- đổi 54 `back.out` sang `power3.out`/`expo.out`, và 2 `bounce` sang `expo.out`;
- bỏ rung và phồng sau khi chữ đã hiện;
- thêm `tabular-nums` cho số đếm.

Chưa có số kênh. Động lực là chủ kênh chê giọng/hình "như robot".

**(B) hiện tại.** B ít hơn hẳn:

- `casewide.js`: 3 `back.out` + 1 `bounce` (dòng 70, 267, 457, 497);
- `chart.js`: 10 `back.out`;
- `lab.js`: 4 `back.out`;
- Short (`casefile.js`, `bang-tra-looks.js`, `beat.js`) cũng có, nhưng look v3 của Short đã được duyệt.

**Đề xuất.**

- Chỉ đổi trong engine Long (casewide/chart/lab), rồi soát bằng gallery.
- Thêm `font-variant-numeric: tabular-nums` cho `.count`.
- Không đụng Short đã duyệt.

**Ước lượng.** 1,5 giờ.

**Rủi ro.** Đổi khoá render của Long đang dở.

### 13. Nhạc lấn giọng, mức SFX (ÁP CÓ CHỈNH: đo trước)

**(A) đã làm gì.**

- `hf_music.MASKS_VOICE` loại 5 bài có dao động RMS > 14 dB hoặc dồn năng lượng ở dải giữa khỏi Long.
- Đỉnh SFX mặc định thấp hơn giọng 12 dB.
- `duck_db` chỉnh được.

**(B) hiện tại.**

- `mix_chapter` đã nén nhạc theo giọng bằng sidechain (threshold .03, ratio 6), SFX `volume=0.42` + sidechain.
- `audio_lint` đo buzz, TP, tiếng tách.
- B có chuẩn "BGM nhỏ" cho Short (memory short-mix-standard).
- Chưa đo bài nào trong `music_catalog.json` lấn giọng, và chưa biết khoảng cách SFX–giọng thực tế.

**Đề xuất.** Viết một script đo theo đúng tiêu chí của A (RMS swing, năng lượng dải giữa, đỉnh SFX so với giọng) trên catalog và trên 2 Long. Có số rồi mới đặt danh sách loại.

**Ước lượng.** 2 giờ.

### 14–15. Bài trúng, AVP theo nhóm độ dài, luật dừng khuôn (THỬ: backtest)

**(A) đã làm gì.** ADR 0017 (e073e37, 6da1db3), dựa trên số kênh FS:

- top 10 bài chiếm 74% view;
- nhóm 2027 có trung vị 15.431 view.

Bốn luật rút ra:

- **Thước đo chính:** số bài > 10k view mỗi tuần.
- **Nhân khuôn:** hạng view ≥ 0,9 và AVP ≥ 1,3 lần trung vị nhóm cùng độ dài.
- **Dừng khuôn:** ≥ 6 bài, trung vị dưới sàn, không bài nào > 3 lần sàn.
- **AVP > 100% đứng một mình là tín hiệu yếu:** 8/9 Short dưới 15 s vượt 100% mà trung vị chỉ 883 view.

**(B) hiện tại.**

- `factory/scoreboard.py` đã có luật dừng theo **% ở lại** (6 bài, trung vị < 25%) và ngưỡng 45%.
- B ghi rõ AVP thô không dự báo được view (MIM r ≈ −0,1).
- B chưa có bài 10k ổn định (Shorts chững ở khoảng 1k), nên ngưỡng 10k của A vô nghĩa với B.

**Đề xuất.** Backtest trên `scoreboard` của B (khoảng 2 giờ):

1. AVP chia cho trung vị nhóm cùng độ dài (< 15, 15–19, 20–29, ≥ 30 s) có tương quan với view/sub hơn AVP thô không?
2. Định nghĩa "bài trúng" là ≥ 3 lần trung vị kênh trong cửa sổ.

Chỉ đưa vào brief nếu backtest cho tương quan rõ. Luật dừng theo % ở lại giữ nguyên.

### 16. Độ to hai lượt, Long −16 LUFS (BỎ QUA)

B đã đạt đích nhờ loudnorm trên cả bản mix: Long −14,0 tới −14,2, Short −14,2 tới −15,2. Vấn đề thật của B là đỉnh, đã xử lý ở mục 2.

Mức −16 cho Long là lựa chọn của A, và A tự ghi "chưa có nguồn chính thức". Đổi sang −16 thì Long B nhỏ hơn Short cùng kênh.

### 17. Ảnh dọc vào khung 16:9, media `crop` (BỎ QUA)

`motion/mediafit.py` đã quyết định cover hay blur (contain trên nền nhoè) cho cả Short và Long, gồm ảnh in cho Short. `crop` sinh ra vì A dùng ảnh AI trùng byte trong chương; B không có luồng ảnh AI.

### 18. Thư viện motion 234 mẫu (BỎ QUA)

- `references/prompt_motion/` chấm theo tiêu đề/prompt, chưa xem video.
- Độ hợp được chấm cho FS/BUD.
- Phần dùng được (bỏ blur-in/`back.out`, dùng `expo.out`, ngắt bằng cắt cứng) đã gộp vào mục 12.

### 19–21. Bỏ qua vì đặc thù hoặc B đã có

- **Dấu 吉 cạnh chữ nghĩa xấu:** chỉ có ở FS.
- **Nhãn tư liệu/stock/ảnh AI trong pacing:** B không có ảnh AI. Nếu muốn, có thể thêm tỉ lệ nguồn vào báo cáo của mục 5.
- **`review_yeartable`:** chỉ dùng cho bảng năm của FS.
- **`hf_long_retention`:** tự ghi là chép từ `motion/stier/monitor.py` của B.

## 3. Thứ tự triển khai

### Đợt 1 (≤ 1 ngày công, rủi ro thấp)

Làm giữa hai lô render, vì mục 1 và 3 đổi khoá render.

| Thứ tự | Việc | Giờ | Kiểm |
|---|---|---|---|
| 1 | Cờ `year` cho counter (casewide/casefile) + lint ở `build.py` và `studio_lint` | 1,5 | Test đơn vị; dựng lại spec Turing ở chế độ chỉ-html để xem số |
| 2 | `alimiter` đỉnh thật sau loudnorm (Long + Short) | 1,5 | `audio_lint` trên 2 Long + 2 Short: TP ≤ −1, LUFS giữ trong ±0,3 |
| 3 | `render_key` băm ảnh/clip local | 1 | Test: thay ảnh cùng tên thì khoá đổi |
| 4 | `seo.keyword` + preflight SEO tối giản trong `publish_long` | 1,5 | Test preflight; chạy thử trên 2 spec |
| 5 | Báo cáo pacing p50/p90/max, cảnh > 25 s chỉ cảnh báo, có `slow_hold` | 2 | So với số trong mục 5 |
| 6 | `docs/pm/so-that-bai.md` | 1 | — |

Tổng khoảng 8,5 giờ.

### Đợt 2 (tuần sau)

- `gate_overflow` cho mọi theme Short, chế độ cảnh báo trong 1 tuần (3–4 giờ).
- Mở rộng gallery dấu sang theme `case`/deco và `bang-tra`, sửa `inset` (2 giờ).
- Mục điểm rơi + câu đang đọc trong brief (3 giờ).
- Lint khuôn nhân vật cho CL/MIM (3 giờ).
- Đo nhạc lấn giọng và mức SFX (2 giờ).
- Ease của engine Long (1,5 giờ).
- Tài liệu cổng Long hai lớp (1 giờ).

### Đợt 3 (thử)

- Backtest AVP theo nhóm độ dài và "bài trúng" trên scoreboard B.
- Chỉ đưa vào brief khi có tương quan.
- Đối chiếu kết quả 4 Long nhân vật của A (22/11, 01/12) và các mốc TN2–TN4 (05/11, 09/11, 10/11) trước khi siết ngưỡng ở mục 10 và 11.

## 4. Ghi chú

- Mọi số của (B) trong tài liệu này đều đo ngày 26/10:
  - log `audio_lint` trong `output/`;
  - `ebur128` của 8 `output/stier/*/final.mp4`;
  - `data.js` của 43 Long;
  - spec + `description.txt` + thumbnail của 43 Long;
  - 51 file `check.json`.
- Không sửa code, không commit, không ghi vào repo (A).
- Short Turing ("1.996") đã đăng. Theo luật, không sửa video đã đăng nếu lỗi chỉ là hình thức; cần chủ kênh quyết nếu muốn thay.
