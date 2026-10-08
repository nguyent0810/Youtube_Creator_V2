# Đề xuất nâng cấp yt-factory (10/2026)

_08/10/2026._ Viết sau đợt sửa lỗi audit (`docs/AUDIT-2026-10-08.md`, nhánh `ccr-386a668a-yt1acx`), nên **không đề xuất lại** các bản sửa đó.

Nguồn:
- **Số đo nội bộ:** đọc trực tiếp `bundles/`, `data/` và mã; các số lấy từ agent nghiên cứu đã được kiểm lại.
- **Dữ kiện về YouTube:** lấy từ trích đoạn kết quả tìm kiếm, vì WebFetch bị chặn trong phiên này.

Ký hiệu độ tin cậy cho dữ kiện bên ngoài:

| Ký hiệu | Nghĩa |
|---|---|
| ✅ | Thấy trong trích đoạn tài liệu chính thức |
| ⚠️ | Nguồn thứ cấp, hoặc chỉ xác minh được một phần |
| ❓ | Không tìm thấy tài liệu |
| 📄 | Lấy từ tài liệu nghiên cứu sẵn có trong repo (`motion/long/RESEARCH-million-views.md`, 04/10) |

---

## 1. Tóm tắt

Sau đợt sửa lỗi, đường đăng đã có chốt: giờ hẹn, chống trùng theo tag dấu, đúng kênh, khoá, bundle bất biến. Rủi ro lớn nhất giờ nằm ở **ba chỗ khác**:

1. **Chính sách "inauthentic content".** Từ 15/07/2025, YouTube dùng tên này cho nội dung *mass-produced, generic, repetitive* và xét trên **cả kênh** ✅. Các dòng sinh từ khuôn của FS/BUD là tài sản rủi ro nhất:
   - Lịch: 6 khuôn tiêu đề cho 83 ngày, và khoảng 35% số câu lặp gần nguyên văn từ 10 lần trở lên.
   - Mỗi dòng FS dùng đúng một bài nhạc nền.
   - Một giọng đọc phủ cả ba kênh.
2. **Vận hành không người trông.** Lỗi chỉ lộ ra khi đã hỏng cả lô: token chết, hết quota, trạng thái kênh lệch với store.
   - Repo không có cảnh báo nào.
   - Không có sao lưu `state.sqlite`, trong khi đây là bản đồ duy nhất nối video với bundle.
3. **Không có vòng học từ số liệu.** `analytics_report.py` có lấy số, nhưng không nối vào việc sinh nội dung, và không có thí nghiệm có kiểm soát.

**Năm việc nên làm trong 2 tuần tới** (bốn việc cỡ S, riêng E2 cỡ M):
- **E3:** cảnh báo về điện thoại.
- **G5:** bộ điều tiết nhịp đăng. Đặc biệt cần trước khi đăng lại 83 video Lịch.
- **P4:** sao lưu.
- **Q2:** từ điển phát âm và nghe lại theo mẫu.
- **E2:** đối soát trạng thái kênh hằng ngày.

**Hai giả định trong repo không đúng với API** (chi tiết ở mục 4):
- Ghim bình luận không làm được qua API, trái với dự tính của `data/long/golden/plan.md` §4.3 ❓.
- "Video liên quan" của Shorts chỉ gắn được trong Studio ✅.

---

## 2. Bảng ưu tiên

Đợt 1 = 2 tuần tới · Đợt 2 = tháng 11 · Đợt 3 = quý tới. Công sức: S ≤ 1 ngày · M vài ngày · L ≥ 1 tuần.

| Đợt | Mã | Đề xuất | Tác động | Công sức | Cần trước |
|---|---|---|---|---|---|
| 1 | E3 | Log có cấu trúc + cảnh báo Telegram/email | Cao | S | |
| 1 | G5 | Bộ điều tiết nhịp đăng/upload theo kênh, viết trong mã | Cao | S | |
| 1 | P4 | Sao lưu `state.sqlite`, credential, bằng chứng giấy phép | Cao | S | |
| 1 | Q2 | Từ điển phát âm dùng chung + nghe lại bằng ASR theo mẫu | Cao | S–M | |
| 1 | E2 | Đối soát kênh → SQLite hằng ngày | Cao | M | |
| 1 | G4 | Playlist tự động theo dòng | Trung bình | S | |
| 1 | M5 | Khai báo `containsSyntheticMedia` tường minh | Thấp–TB | S | |
| 2 | M1 | Đo "inauthentic" cho Shorts theo lịch sử kênh | Cao | M | E2 |
| 2 | D1 | Kho analytics trong SQLite (engagedViews, giữ chân, CTR) | Cao | M | E2 |
| 2 | D3 + G1 | Khung A/B + thí nghiệm hook "chi tiết dị thường trước" | Cao | M | D1 |
| 2 | Q1 | Sổ claim + luật 2 nguồn độc lập (CL/BUD) | Cao | M | |
| 2 | Q3 | Một cổng QA kịch bản cho mọi loại nội dung | Cao | M | |
| 2 | Q4 | Duyệt theo mẫu, ký duyệt trước publishAt | Cao | M | E3 |
| 2 | M3 | Tách giọng đọc theo kênh | Trung bình | S | |
| 2 | M4 | Lint ad-suitability cho tiêu đề/thumbnail CL | Trung bình | S | |
| 2 | G2 | Checklist Studio + ghi kết quả Test & Compare (video dài) | TB–Cao | S | |
| 2 | G6 | Bình luận: bình luận đầu, tổng hợp hằng ngày, kiểm duyệt, đính chính | Trung bình | M | |
| 3 | E1 | Một lớp publish có chốt chung cho ba đường upload | Cao | M–L | E2, G5 |
| 3 | M2 | Thẻ đồ hoạ dựng từ dữ liệu thay B-roll stock (FS/BUD) | Cao | L | D3 |
| 3 | G3 | Phễu Shorts → video dài (teaser + "video liên quan") | Cao | M | G2 |
| 3 | M6 | Sổ giấy phép từng video + kit kháng nghị Content ID | TB–Cao | M | P4 |
| 3 | P1–P3 | Thông lượng render, cache TTS theo câu, font + provenance | Trung bình | S–M | |
| 3 | E4–E7 | CLI `yf`, lockfile + lint + CI Windows, config TOML, dọn file mồ côi | Trung bình | S–M | |

---

## 3. Chi tiết

### 3.1 Vận hành: biết sớm, không mất dữ liệu

**E3. Log có cấu trúc + cảnh báo về điện thoại** · Cao · S
- **Là gì:**
  - `factory/notify.py` gửi Telegram Bot `sendMessage`, có email dự phòng. Token đặt trong biến môi trường `YF_TG_TOKEN` và `YF_TG_CHAT`.
  - Mọi script ghi `logging` dạng JSON, có `run_id`.
  - Các sự kiện cần báo:
    - Một chặng của `run_pipeline` dừng.
    - Hoãn vì quota hoặc rate limit.
    - `DuplicateTitle` hoặc `PublishAtPassed`.
    - `ChannelMismatch`.
    - `invalid_grant` khi làm mới token.
    - Render FAILED trong `queue2`.
    - Ổ đĩa sắp đầy.
    - Đối soát (E2) báo lệch.
  - Gửi thêm một bản tóm tắt hằng ngày.
- **Vì sao:**
  - Repo không dùng `logging`; log rải rác ở `drip.log`, `task.log` và các lệnh `print`. `run_pipeline` chỉ in 8 dòng cuối của mỗi chặng.
  - App OAuth ở trạng thái **Testing** thì refresh token hết hạn sau 7 ngày ✅. Lỗi này hiện chỉ lộ khi cả lô đã hỏng. Nên kiểm trạng thái app trong Google Cloud Console.
  - Theo tài liệu `videos.insert` (chưa mở lại trang trong phiên này) ⚠️: project API **chưa qua audit**, tạo sau 28/07/2020, chỉ upload được video ở chế độ private. Đừng tạo project mới để "lấy thêm quota" khi chưa tính tới điều này.
- **Bước đầu:** viết `factory/notify.py`; gọi khi `run_pipeline.py` DỪNG và trong `motion/stier/monitor.py`.

**G5. Bộ điều tiết nhịp đăng/upload theo kênh** · Cao · S
- **Là gì:** `factory/cadence.py` đặt các giới hạn theo kênh và dòng:
  - Số upload trong 24 giờ.
  - Số video lên sóng mỗi ngày.
  - Khoảng cách tối thiểu giữa các publishAt.

  `publish_batch`, `upload_one`, `publish_long` và `replace_lich` cùng đọc từ store; vượt giới hạn thì hoãn và báo (E3). Con số cụ thể do chủ kênh quyết, ví dụ CL 3 upload/ngày, FS 15.
- **Vì sao:**
  - Ngày 30/09, kênh CL nhận 61 video trong một ngày (53 video trong 47 phút), và feed ngừng đẩy Shorts của kênh.
  - Hiện luật này chỉ là quy ước (`DRIP_ONLY`, `drip.py`):
    - `publish_batch run` mặc định lấy tới 500 item.
    - `run_pipeline resume` không truyền `--limit`.
    - Đăng lại Lịch sẽ tạo 83 upload.
  - `RESEARCH-million-views.md` nói không có nguồn chính thức nào khẳng định "đăng nhiều làm hại kênh" 📄. Dù vậy, Spam policy cấm "flood" nội dung lặp lại 📄, và rủi ro này không đáng để thử.
- **Bước đầu:**
  1. Chuyển luật của `drip.py` thành `factory/cadence.py`.
  2. Gọi trong `scripts/publish_batch.py` trước mỗi lần upload.

**P4. Sao lưu** · Cao · S
- **Là gì:** `scripts/backup.py` chạy hằng đêm bằng Task Scheduler:
  - Sao `state.sqlite` bằng `sqlite3.Connection.backup` (sao lưu trực tuyến an toàn).
  - Sao kèm: bằng chứng giấy phép (`output/**/img/*.json`, `data/stier/research/`), credential đã mã hoá, và `final.mp4` của video đã đăng.
  - Đẩy ra ổ ngoài hoặc thư mục đồng bộ đám mây, giữ 30 bản.
  - Diễn tập khôi phục mỗi quý.
- **Vì sao:**
  - Mọi thứ chạy trên một máy Windows.
  - `state.sqlite` chứa video_id ↔ bundle, danh tính kênh và khoá; file này bị gitignore. Mất nó thì mọi công cụ an toàn (verify, unschedule, replace_lich) mất căn cứ.
  - Bằng chứng giấy phép chỉ nằm trên máy này (audit L19).
- **Bước đầu:** viết `scripts/backup.py` (khoảng 60 dòng) và thêm một mục Task Scheduler.

**E2. Đối soát trạng thái kênh hằng ngày** · Cao · M
- **Là gì:**
  - `scripts/reconcile.py` quét toàn bộ uploads (playlistItems + `videos.list`, 1 đơn vị mỗi 50 video) vào bảng `yt_video`. Các trường: privacy, publishAt, tags (có dấu `yf<id>`), `uploadStatus`/`rejectionReason` ✅, `containsSyntheticMedia`.
  - So với store và bundle để báo lệch:
    - Video bị xoá.
    - Video private mà không có lịch.
    - Lịch khác bundle.
    - Video lạ chiếm slot.
    - Tiêu đề bị sửa trong Studio.
    - Upload bị từ chối.
    - Video "[ĐÃ THAY]" còn sót.
  - Bảng này thay `data/channel_titles/*.json` cho chống trùng, verify và analytics.
- **Vì sao:**
  - Ba đường đăng giữ ba kiểu trạng thái: store, `output/stier/uploads.json`, `output/long/*/pub/result.json`.
  - Tag dấu `yf<bundle.id>` (bản sửa C2) giờ cho phép ánh xạ video ↔ bundle chắc chắn.
  - Chi phí khoảng 10–20 đơn vị/kênh/ngày.
- **Bước đầu:** thêm migration bảng `yt_video`; tái dùng `all_videos()` của `scripts/schedule_audit.py`.

### 3.2 Đúng sự thật và nghe đúng

**Q2. Từ điển phát âm dùng chung + nghe lại theo mẫu** · Cao · S–M
- **Là gì:**
  - `data/lexicon/vi.json` cộng hàm `factory/lexicon.py::spoken()`, phủ:
    - Tên riêng nước ngoài.
    - Viết tắt (FBI, ADN, OTP, BLHS).
    - Khoảng giờ ("23-1h").
    - Số La Mã.
    - Đơn vị đo.
  - Áp ở cả ba điểm vào TTS: `factory/speak`, `motion/stier/build.speak`, `motion/long/build_long.spoken`. Bảng `say` riêng của từng spec ghi đè bảng chung.
  - Phụ đề giữ chữ hiển thị.
  - Thêm khâu nghe lại bằng faster-whisper, dùng lại cách chấm của `build_long.do_pick`:
    - 100% Short có tên ngoại ngữ.
    - Khoảng 10% Short còn lại.
- **Vì sao:**
  - 129 kịch bản Shorts CL + S-tier có 427 token không phải âm tiết tiếng Việt, xuất hiện 744 lần. Ví dụ: London ×19, FBI ×15, Chicago ×11.
  - 56/92 kịch bản Lịch có dạng "giờ Tý (23-1h)".
  - Chỉ video dài có bảng `say`, và bảng bị lặp theo từng topic.
  - Đã có lỗi đọc thật ("8-9-3" → "8 đến 9 ba"; `motion/long/README.md`).
  - Shorts không có bước kiểm nào sau TTS.
- **Rủi ro:** `word_lines` của S-tier tính trọng số theo chữ hiển thị, phải đổi sang chữ đọc như `build_long` đã làm.
- **Bước đầu:** khai thác token từ `bundles/` và `data/stier/specs/` → bản nháp khoảng 150 mục, kèm 30 test.

**Q1. Sổ claim + luật 2 nguồn độc lập (CL/BUD)** · Cao · M
- **Là gì:**
  - Spec S-tier, mục pack và chương video dài có thêm `claims[]`, do LLM khai trong chat: đoạn văn, loại (số / ngày / tên / trích dẫn / điều luật / số người chết), nguồn.
  - `factory/sourcing.py` (tất định) trích mọi đoạn kiểm được trong lời đọc và tiêu đề. Đoạn chưa có claim phủ thì DỪNG.
  - Claim rủi ro cao cần ≥2 nguồn khác tên miền, trong đó ≥1 nguồn không phải Wikipedia. Claim rủi ro cao gồm số liệu, ngày, khung hình phạt, trích dẫn, và mọi thứ nằm ở tiêu đề hay hook.
- **Vì sao:**
  - 92/94 spec S-tier chỉ dẫn Wikipedia; 2 spec còn lại là truyện hư cấu. 85/94 có đúng 1 nguồn.
  - Video dài chỉ dẫn Wikipedia EN/ZH.
  - Luật "đối chiếu được với bài nguồn" hiện chỉ là lời dặn.
  - Mô hình sổ claim đã chạy tốt ở FS (`factory/claims.py`). Lịch giờ cũng đã đối chiếu hai nguồn độc lập (N1).
  - Thêm nguồn ngoài Wikipedia còn giảm vùng xám "chỉ diễn đạt lại Wikipedia" 📄.
- **Rủi ro:**
  - Chậm hơn.
  - Nguồn thứ hai có thể chỉ chép lại Wikipedia. Máy không bắt được, nên để Q4 soi.
- **Bước đầu:** viết `checkable_spans()` + `validate()`, gọi đầu `motion/stier/build.build()`, thử trên 5 spec mới.

**Q3. Một cổng QA kịch bản** · Cao · M
- **Là gì:** `python -m factory.qa <file>` chạy cho mọi loại nội dung (bundle, pack, spec S-tier, chương video dài).
  - Chạy trong chat lúc sinh, và chạy lại trước TTS.
  - Gộp các bộ kiểm đang có: `integrity`, `script_craft`, `packs.check`, `batchcheck`, `novelty`.
  - Thêm phép kiểm mới:
    - Hook dài quá 12–14 từ.
    - Lời hứa của tiêu đề có xuất hiện trong 2 câu đầu không.
    - Độ phủ claim (Q1) và lexicon (Q2).
    - Lint ad-safety (M4).
    - CTA tiếng Anh "Comment …".
    - Mở bài và câu chốt lặp so với **lịch sử kênh**, không chỉ trong một lô.
  - Mặc định chỉ cảnh báo; chỉ lỗi dữ kiện và markup mới chặn.
- **Vì sao:**
  - S-tier chỉ được kiểm độ dài 55–135 từ.
  - Khoảng 2/3 spec S-tier mở bằng mốc thời gian (66–69/94, tuỳ cách đếm). Không spec nào mở bằng câu hỏi. Câu đầu trung vị 17 từ, vượt `HOOK_MAX_WORDS = 14` của chính repo.
  - 22 bundle có CTA "Comment" (FS 19, CL 2, BUD 1).
- **Bước đầu:** viết `factory/qa.py::check_any(path)`, gọi đầu tiên ở `motion/stier/build.build()`.

**Q4. Duyệt theo mẫu, ký duyệt trước giờ lên sóng** · Cao · M
- **Là gì:**
  - Chọn mẫu tất định (theo hash) cho các nhóm sau:
    - 100% của 5 video đầu tiên ở mỗi dòng, khuôn hoặc giọng mới.
    - 100% video dài.
    - 100% video "Điều luật" có khung phạt.
    - Mọi item có cảnh báo QA.
    - Khoảng 10% mỗi dòng mỗi tuần.
  - `scripts/review_pack.py` sinh trang HTML gồm contact sheet, audio, kịch bản, claim kèm nguồn. Với Lịch, có thêm một nguồn đối chiếu ngoài (lịch giấy).
  - Kết quả ghi vào bảng `review`.
  - Item được chọn mà tới T-12h chưa duyệt thì gọi `publish.unschedule()` (đã có): thà trống slot còn hơn phát sai.
- **Vì sao:**
  - N1 cho thấy bộ kiểm tự động có thể sai cùng chiều với dữ liệu.
  - B-roll lạc đề chỉ lộ ra khi nhìn khung hình.
  - Video vốn được upload trước nhiều ngày, nên đã có sẵn cửa sổ để duyệt.
- **Rủi ro:** tốn 10–15 phút người mỗi ngày; quên duyệt sẽ trống slot. Cần E3 nhắc.

### 3.3 Tuân thủ chính sách và kiếm tiền

**M1. Đo "inauthentic" theo lịch sử kênh** · Cao · M
- **Là gì:** `variety.py audit-channel <CH> --window 30` đo trên 30 video gần nhất của kênh:
  - Tỉ trọng bài nhạc dùng nhiều nhất.
  - Entropy khuôn tiêu đề.
  - Độ giống kịch bản giữa các video liên tiếp (5-gram Jaccard).
  - Tỉ trọng giọng đọc và look.

  Vượt ngưỡng thì chặn ở pha sinh (`make_lich_month`, `make_pillars_day`, `enqueue`), ở bước publish chỉ cảnh báo. Ngưỡng khởi điểm gợi ý: bài nhạc nhiều nhất ≤25%, một khuôn tiêu đề ≤20%. Nhạc Shorts đưa vào `music_catalog.json` để xoay vòng như video dài.
- **Vì sao:**
  - Chính sách xét trên cả kênh ✅. Spam policy lấy ví dụ "the exact same background music" 📄.
  - Hiện trạng FS:
    - Lịch 92/92 cùng một bài `asian_drums.mp3`; mỗi dòng pillar 23/23 một bài.
    - Lịch bản mới: 6 khuôn tiêu đề cho 83 ngày (22/21/20/9/9/2).
    - Khoảng 35% số câu lặp gần nguyên văn từ 10 lần trở lên, ví dụ "Ngoài danh mục ấy, lịch ghi gọn là mọi việc khác." ×33.
    - Kiểm chéo hiện chỉ trong một lô. Hai kịch bản giống hệt nhau vẫn có thể cách nhau 360 ngày.
- **Rủi ro:** ngưỡng chỉ là heuristic, không phải ngưỡng thật của YouTube.

**M2. Thẻ đồ hoạ dựng từ dữ liệu thay B-roll stock (FS/BUD)** · Cao · L
- **Là gì:** thẻ tất định dựng bằng HyperFrames (engine S-tier đã có), dữ liệu có sẵn trong `factory/lunar.py` và `factory/pillars/tables.py`:

  | Dòng | Nội dung thẻ |
  |---|---|
  | Lịch | Can chi, sao, trực, giờ hoàng đạo, tuổi xung, hướng Tài thần |
  | Kinh Dịch | Quẻ 6 hào |
  | Pháp Cú | Thẻ kệ |
  | 12 con giáp | Vòng tam hợp / lục xung |
- **Vì sao:**
  - Mô hình B-roll stock + TTS + khuôn là mô hình rủi ro nhất trước bản cập nhật "original Shorts" ngày 01/10/2026 ⚠️📄.
  - B-roll lạc đề đã xảy ra nhiều lần (Ganesha, linh mục Công giáo trong video Phật giáo).
  - Thẻ có giá trị dùng thật: người xem chụp màn hình lịch.
- **Bước đầu:** làm nguyên mẫu `lichcard.html` + `motion/lich_card.py`, rồi A/B 2 tuần với bản B-roll (D3).

**M3. Tách giọng đọc theo kênh** · Trung bình · S
- **Hiện trạng:** "Anh Khôi" có trong 115 bundle FS, 98 bundle CL, 7 bundle BUD, và mọi video dài.
- **Đề xuất:** khai báo `voices` được phép trong `CHANNELS`, và `Bundle.validate` kiểm.
  - Giữ "Anh Khôi" cho CL, vì kênh đang kiếm tiền và khán giả đã quen.
  - FS và BUD thử giọng khác bằng `scripts/_audition_voices.py`.
- **Vì sao:** "cùng template, cùng giọng, cùng nhạc" là rủi ro dây chuyền giữa các kênh 📄.

**M4. Lint ad-suitability cho tiêu đề và thumbnail CL** · Trung bình · S
- **Là gì:** từ điển có mức độ cho tình dục, bạo lực đồ hoạ, thi thể…
  - Từ ngữ tình dục trong tiêu đề là lỗi cứng.
  - Từ ngữ bạo lực chỉ cảnh báo, kèm gợi ý cách viết trung tính.
- **Vì sao:**
  - Advertiser-friendly guidelines xét cả tiêu đề lẫn thumbnail ✅.
  - Đã có tiêu đề như "Điều 141: Tội hiếp dâm".
  - Luật #6 trong `RESEARCH-million-views.md` đã đặt ra nhưng chưa có máy kiểm 📄.

**M5. `containsSyntheticMedia` tường minh** · Thấp–TB · S
- **Là gì:** thêm trường `synthetic_media` vào Bundle/spec và gửi trong `video_meta`.
- **Vì sao:**
  - Trường có từ 30/10/2024 cho `videos.insert`/`update` ✅.
  - Từ 05/2026, YouTube tự gắn nhãn AI khi phát hiện nội dung AI chân thực chưa khai báo ⚠️.
  - Giọng TTS chung chung nhìn chung không bắt buộc khai báo ⚠️.

**M6. Sổ giấy phép từng video + kit kháng nghị** · TB–Cao · M
- **Là gì:**
  - Lúc dựng, tự ghi manifest `data/licenses/<CH>/<video_id>.json`. Với mọi tài sản (nhạc, ảnh, clip Pexels, font) ghi: nguồn, giấy phép, tác giả, sha256.
  - `scripts/dispute_kit.py` in sẵn lý do kháng nghị cho từng tài sản.
- **Vì sao:**
  - Content ID: bên khiếu nại có 30 ngày để trả lời ✅.
  - Nội dung CC/PD không được dùng làm tệp tham chiếu Content ID ✅.
  - Hiện bằng chứng giấy phép nằm trong thư mục bị gitignore.

### 3.4 Tăng trưởng và vòng học từ dữ liệu

**D1. Kho analytics trong SQLite** · Cao · M
- **Là gì:**
  - Các bảng mới:
    - `metric_daily`: views, **engagedViews**, phút xem, AVD, AVP, likes, shares, subs.
    - `retention`: thêm `relativeRetentionPerformance`.
    - `traffic`: nguồn truy cập.
  - Với video dài, thêm CTR và impression từ reach report của Reporting API ⚠️.
  - Gộp phần đo của `monitor.py` vào đây.
- **Vì sao:**
  - Cách đếm "view" của Shorts đổi từ 31/03/2025: lượt phát lại cũng tính, còn `engagedViews` giữ cách đếm cũ ✅.
  - Theo nguồn thứ cấp, mọi định dạng đổi cách đếm từ 24/08/2026 ⚠️.
  - So view trước và sau các mốc này là so táo với cam.
- **Không lấy được qua API** (chưa thấy tài liệu) ❓:
  - Viewed vs swiped.
  - "Khi người xem có mặt".
  - Kết quả Test & Compare.
  - CTR của feed Shorts.

  Cần ghi tay từ Studio cho một mẫu nhỏ.

**D3 + G1. Khung A/B + thí nghiệm hook đầu tiên** · Cao · M
- **Khung A/B (D3):**
  - Bundle schema v2 có `meta: {experiment, arm, hook_key, template_id}` và vẫn đọc được v1.
  - Gán nhánh tất định, cân bằng theo thứ trong tuần, khung giờ và dòng.
  - Chỉ số chính đăng ký trước:
    - Shorts: engagedViews@72h + AVP.
    - Video dài: giữ chân 30s/60s + CTR.
  - Tối thiểu khoảng 20 video mỗi nhánh.
- **Thí nghiệm đầu tiên (G1):**
  - Câu đầu ≤12 từ, mở bằng chi tiết dị thường, hành động đang diễn ra, hoặc câu hỏi.
  - Mốc thời gian chuyển lên hình (`kicker`, cảnh `date`).
  - Với FS, mở bằng việc người xem làm được.
- **Vì sao:**
  - Test & Compare không dùng được cho Shorts ✅.
  - Shorts được xếp hạng theo tỉ lệ người *chọn xem* (không vuốt qua), AVD và AVP 📄.
  - Repo đã đặt luật "câu đầu là cảnh cụ thể hoặc câu hỏi" (`pilots_2026-10.md`), nhưng 2/3 spec chưa theo.
- **Rủi ro:** view của Shorts có đuôi dày, n nhỏ thì khó kết luận. Mỗi dòng chỉ chạy một thí nghiệm tại một thời điểm.

**G2. Checklist Studio cho video dài + ghi kết quả** · TB–Cao · S
- **Là gì:** sau upload, `scripts/studio_tasks.py` sinh danh sách việc:
  - Test & Compare với 3 thumbnail `thumbs/<topic>_t1..t3` và 3 tiêu đề.
  - End screen trong 5–20 giây cuối, tối đa 4 phần tử ✅.
  - Ghim bình luận.
  - Gắn "video liên quan" cho các Short teaser.

  Kết quả ghi vào `data/experiments/packaging.jsonl`.
- **Vì sao:**
  - Test & Compare: tối đa 3 phương án, chỉ chạy trên Studio máy tính, chọn bên thắng theo watch time ✅.
  - Không thấy endpoint Data API cho Test & Compare ❓.
  - Repo đã làm sẵn 3 thumbnail cho mỗi topic, nhưng `publish_long` chỉ dùng `t1`.

**G3. Phễu Shorts → video dài** · Cao · M
- **Là gì:** mỗi video dài có 2–3 Short teaser, viết kịch bản mới chứ không cắt lại video dài, dựng bằng engine S-tier, có trường `related_long`. Gắn "video liên quan" trong Studio (G2), rồi đo nguồn traffic vào video dài trước và sau.
- **Vì sao:**
  - Link trong mô tả và bình luận Shorts không bấm được từ 31/08/2023 ✅.
  - "Video liên quan" thay thế cho link: mỗi Short gắn được một link, chỉ trỏ tới video cùng kênh, và chỉ gắn trong Studio ✅.
  - Long là đường tới 1 triệu view, Shorts là đường tới subscriber 📄.

**G4. Playlist tự động theo dòng** · Trung bình · S
- **Hiện trạng:** `publish_bundle(..., playlist_id=…)` đã có tham số, nhưng `publish_batch` không truyền, nên Shorts không vào playlist nào.
- **Đề xuất:**
  - Thêm map `playlists` vào `CHANNELS`.
  - Gọi `playlistItems.insert` sau upload (50 đơn vị).

**G6. Bình luận trong giới hạn API** · Trung bình · M
- **Là gì:**
  - (a) Bình luận đầu tiên do LLM viết sẵn, đăng khi video công khai (`commentThreads.insert`, 50 đơn vị). Ghim thì làm tay.
  - (b) Tổng hợp hằng ngày các câu hỏi chưa trả lời. LLM soạn câu trả lời trong chat, script đăng lên.
  - (c) Kiểm duyệt spam lừa đảo (số điện thoại, Zalo, "lấy lại tiền") bằng `comments.setModerationStatus` ✅.
  - (d) Nhật ký đính chính, kèm dòng "ĐÍNH CHÍNH" trong mô tả. Dùng ngay cho phương án (B) của 9 video Lịch đã phát.
- **Lưu ý:**
  - Cần cấp lại OAuth với scope `youtube.force-ssl`.
  - Bản đầu chỉ đọc.

### 3.5 Sản xuất và kỹ thuật

| Mã | Đề xuất | Vì sao |
|---|---|---|
| P1 | Đặt `--workers` của HyperFrames tường minh, thử `--gpu` ⚠️, render 2 chương song song khi đủ RAM | Render video dài khoảng 2,7 lần thời lượng (34 phút → khoảng 90 phút), tuần tự từng chương |
| P2 | Cache TTS theo câu dùng chung cho ba đường; khoá cache gồm phiên bản vieneu | S-tier phải đọc lại cả bài khi sửa một câu; vieneu 3.8.3 đổi tên giọng |
| P3 | Vendor font (OFL) vào `assets/vendor/fonts`; hash font đưa vào `render_key`; `provenance.json` cho mỗi bản final | Phần còn lại của T15: font vẫn tải từ Google lúc render, font đổi là ngắt dòng đổi |
| E1 | Một `factory/publisher.py` có `preflight()` chung cho cả ba đường upload; video dài vào store | Mỗi chốt an toàn đang phải vá riêng vào 3 script (e10d1a1, 8087d13) |
| E4 | CLI `yf` (`[project.scripts]`), lệnh phá huỷ mặc định chạy khô | 25 script + 30 file motion, mỗi file đọc argv một kiểu (từng gây sự cố C3) |
| E5 | `uv lock` cho hai venv; ghim vieneu, hyperframes, node; thêm ruff và job `windows-latest` vào CI | pyproject mới chỉ có cận dưới; máy sản xuất chạy Windows nhưng CI chạy ubuntu |
| E6 | `config/channels.toml`: khung giờ, giọng, playlist, nhịp đăng; bí mật lấy từ biến môi trường | Cấu hình nghiệp vụ rải ở `channels.py`, `enqueue.py` (`SLOTS_VN`), `lunar.py` |
| E7 | Chuyển file mồ côi vào `attic/` | Họ composition `engine.js` (16 file), `_smoke_*`, script một lần. **Lưu ý:** `monitor.py` đang import `WEEK` từ script tuần test, phải tách trước |

---

## 4. Việc API không làm được: làm bằng checklist Studio

| Việc | Qua Data API? | Cách làm |
|---|---|---|
| Ghim bình luận | Không thấy phương thức ❓ (chỉ có list/insert/update/delete/setModerationStatus) | Tay, trong G2 |
| "Video liên quan" của Shorts | Không ✅ (chỉ Studio) | Tay, trong G2/G3 |
| End screen | Không thấy endpoint ❓ | Tay, trong G2 |
| Test & Compare | Không thấy endpoint ❓ | Tay; ghi kết quả bằng `studio_tasks --done` |
| Bài đăng Cộng đồng | Không thấy endpoint ❓ | Tay |
| Bình luận, kiểm duyệt, playlist, `containsSyntheticMedia`, `localizations` | Có ✅ | Tự động (G4, G6, M5) |

**Không đề xuất** dùng trình duyệt tự động để thao tác Studio. Cách này có rủi ro điều khoản dịch vụ, và dễ vỡ.

---

## 5. Thứ tự gợi ý

E3 → G5 → P4 → Q2 → E2 → D1 → D3 + G1 → Q1/Q3/Q4 → M1 → E1 → M2/G3.

Mọi đề xuất giữ luật kiến trúc của repo:
- Chữ (claim, lexicon, bình luận đầu, biến thể A/B, câu trả lời) do LLM viết trong pha sinh.
- Pha sản xuất chỉ chạy quy tắc tất định và gọi API.

---

## 6. Nguồn

### Chính sách, tính năng và API của YouTube/Google

| Nguồn | Dùng cho | Độ tin cậy |
|---|---|---|
| [Channel monetization policies](https://support.google.com/youtube/answer/1311392) | "inauthentic content", 15/07/2025 | ✅ |
| [Spam policy](https://support.google.com/youtube/answer/2801973) | flood, cùng nhạc nền | 📄 |
| [Disclosing altered or synthetic content](https://support.google.com/youtube/answer/14328491) | | ✅ |
| [Google blog: improving AI labels](https://blog.google/intl/en-in/products/platforms/improving-ai-labels-for-viewers-and-creators/) | 05/2026 | ⚠️ |
| [Data API revision history](https://developers.google.com/youtube/v3/revision_history) | `containsSyntheticMedia` 30/10/2024 | ✅ |
| [Data API: Videos](https://developers.google.com/youtube/v3/docs/videos) | publishAt, uploadStatus, rejectionReason, localizations | ✅ |
| [Quota costs](https://developers.google.com/youtube/v3/determine_quota_cost) | | ✅ |
| [Comments guide](https://developers.google.com/youtube/v3/guides/implementation/comments) | | ✅ |
| [comments.setModerationStatus](https://developers.google.com/youtube/v3/docs/comments/setModerationStatus) | | ✅ |
| [Analytics API revision history](https://developers.google.com/youtube/analytics/revision_history) | engagedViews, đếm view Shorts 31/03/2025 | ✅ |
| [Analytics metrics](https://developers.google.com/youtube/analytics/metrics) | | ✅ |
| [Reporting API revision history](https://developers.google.com/youtube/reporting/revision_history) | reach report 15/01/2026 | ⚠️ |
| [A/B test titles & thumbnails](https://support.google.com/youtube/answer/16391400) | | ✅ |
| [Test & compare thumbnails](https://support.google.com/youtube/answer/13861714) | | ✅ |
| [Add a related video to your Shorts](https://support.google.com/youtube/answer/14075157) | | ✅ |
| [Sharing links with your audiences](https://support.google.com/youtube/answer/13748639) | link Shorts không bấm được | ✅ |
| [Add end screens](https://support.google.com/youtube/answer/6388789) | | ✅ |
| [Advertiser-friendly content guidelines](https://support.google.com/youtube/answer/6162278) | | ✅ |
| [Dispute a Content ID claim](https://support.google.com/youtube/answer/2797454) | | ✅ |
| [Content eligible for Content ID](https://support.google.com/youtube/answer/2605065) | | ✅ |
| [Shorts discovery tips](https://support.google.com/youtube/answer/11914225) | | 📄 |
| [Google OAuth 2.0: refresh token expiration](https://developers.google.com/identity/protocols/oauth2#expiration) | 7 ngày ở trạng thái Testing | ✅ |
| [Zoomph](https://help.zoomph.com/youtube-views-update-august-2026) · [Emplifi](https://docs.emplifi.io/platform/latest/home/youtube-metric-update-august-2026) · [vidIQ](https://vidiq.com/blog/post/youtube-view-count-update/) | đổi cách đếm view 08/2026 | ⚠️ |
| [Tubefilter 26/03/2025](https://www.tubefilter.com/2025/03/26/youtube-shorts-views-counting-stats/) | đếm view Shorts | ⚠️ |

### Kỹ thuật

| Nguồn | Độ tin cậy |
|---|---|
| [HyperFrames (GitHub)](https://github.com/heygen-com/hyperframes) | ⚠️ |
| [VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS) | ⚠️ |
| [VietNormalizer (arXiv 2603.04145)](https://arxiv.org/abs/2603.04145) | ✅ |
| [vinorm](https://pypi.org/project/vinorm/) | ✅ |
| [uv](https://docs.astral.sh/uv/) | |
| [Telegram Bot API: sendMessage](https://core.telegram.org/bots/api#sendmessage) | ⚠️ |
| [Python sqlite3 Connection.backup](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup) | |

### Tài liệu trong repo

`docs/AUDIT-2026-10-08.md`, `docs/RUNBOOK-lich.md`, `motion/long/RESEARCH-million-views.md`, `motion/long/RETENTION.md`, `motion/long/SOURCES.md`, `data/stier/pilots_2026-10.md`, `data/long/golden/plan.md`.
