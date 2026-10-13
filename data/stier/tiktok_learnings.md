# Bài học sản xuất TikTok – kênh Phật Giáo (BUD)

## 09/10/2026

### 1. Clip HDR của Pexels làm mất toàn bộ chữ và overlay
- **Triệu chứng:** một số clip Pexels là HEVC 10-bit HLG/PQ (BT.2020). Khi đưa vào HyperFrames, video ra mất hết chữ cảnh, phụ đề và overlay (vd. `bud-la-mung-1-thang-9/final_hdr_broken.mp4`).
- **Đã sửa tận gốc** trong `motion/stier/clips.py` (bản gốc: `clips.py.bak-20261009`):
  - `_is_hdr()` coi clip là HDR khi transfer là PQ/HLG, primaries BT.2020 hoặc pixel 10/12-bit.
  - Clip HDR được tonemap (zscale + hable) về H.264 8-bit yuv420p gắn nhãn BT.709 trước khi scale/crop. Clip SDR vẫn cắt bằng đúng lệnh cũ.
  - `ensure()` tự chuyển cả clip cũ trong cache nếu vẫn còn HDR, và giữ bản `.hdr.bak.mp4`.
- **Kiểm tra:** `ffprobe` file final phải ra `yuv420p, bt709`. Cần ffmpeg có zscale (bản gyan full build trong PATH đã có).

### 2. Hook phải TO và có chữ ngay từ 0 s
- Cảnh `question` vẽ câu hỏi bằng chữ nhỏ một dòng và không có phụ đề, nên 3 giây đầu rất yếu (`bud-hl-niet-ban…` bản nháp 1).
- **Quy tắc:** cảnh 0 dùng `kinetic`. Mục đầu có `"at": 0.0`, `acc`, `size` ~170 (1–2 chữ khoá, vd. "NIẾT-BÀN"). Các mục tiếp theo neo vào từ trong câu hook, sao cho toàn bộ câu hỏi hiện trước giây ~2,8.
- Cũng không dùng `question` ở giữa video (open loop); thay bằng `kinetic` 2 dòng để vẫn có phụ đề.
- Tránh chữ số đứng đầu một mục kinetic ("1 TAY", "1 NĂM SAU"): khung giữa hiệu ứng có lúc mất số. Viết bằng chữ ("MỘT TAY").
- **QA khung hình:** lấy khung ở 0,3/1/2/2,9 s, ở giữa và cuối mỗi câu, và 2 khung cuối. Chữ còn mờ ở khung giữa câu thường chỉ là đang hiện dần, nên phải xem thêm khung cuối câu trước khi kết luận lỗi.

### 3. Độ dài theo format
- Đo nhanh trước khi render: `nolock_build_args.py <slug> --no-render` chỉ tạo giọng đọc và timing (~30 s); xem `segments[-1].end` trong `timing.json`.
- Tốc độ thực tế ~3 từ/giây (giọng Thiền Tâm Đức, Thanh Bình), chậm hơn mức ước tính 4 từ/giây trong lịch.
- Chuyện xưa (35–45 s, gap 0,45): giữ quãng nghỉ 0,45 s (nhịp kể chuyện), cắt lời thay vì hạ gap. Khoảng ~120–125 từ / 12 câu là vừa (Tập 2: 124 từ → 35,3 s giọng).
  - Tập 1 (`bud-cx-con-khi-va-bay`) đã lỡ hạ gap từ 0,2 xuống 0 để về 43,6 s. Không lặp lại cách này.
- Lời Kinh giải mã: đọc số kệ bằng chữ ("hai trăm hai mươi bảy…") tốn ~4 s. Để số kệ trên màn hình, còn lời đọc thì nói gọn ("Kinh Pháp Cú có hai câu kệ, diễn ý:").
- Sửa lời thì phải sửa luôn mục lịch (`hook`/`caption`) để dòng hook trong caption khớp đúng lời video.

### 4. Quy trình
- Render song song bằng `grokbot-stage/nolock_build_args.py <slug> [--draft]` (bỏ khoá render, user đã đồng ý; không bao giờ tắt render khác).
- Mỗi video: nháp → xem khung hình → sửa → final → kiểm HDR/độ dài → giao vào `/workspace/tiktok/ready` + manifest (caption lịch + tác giả clip từ credits.json + nhạc thật từ music.json).

### 5. Thêm (#7–#8)
- Mốc `[i, "từ", n]`: n đếm từ 0 (lần xuất hiện thứ hai là 1).
- Chữ hook có `size` 150–170 chỉ nên dài tối đa ~9 ký tự (vd. "CẢ THÀNH"); "CẢ THÀNH KHEN" ở size 150 bị cắt mép.
- Chọn clip: `grokbot-stage/cands.py <tag> "query" ...` tạo bảng poster (bỏ clip đã dùng trong sổ đa dạng, clip ≥ 8 s).


## 6. Lô #9–#12 (09/10/2026)
- Cảnh `counter` (đếm số) nhỏ, dễ trùng chữ số khi scramble → với đếm ngược nói thành lời, dùng kinetic "BA / HAI / MỘT" size 150.
- Tiêu đề `ledger` giữ ≤ 16 ký tự (vd "ĐỪNG TIN CHỈ VÌ"), dài hơn bị tràn khung.
- Hook có giờ/số ở dạng "POV: 23:00": size ≤ 140 để không cắt mép.
- Cập nhật hook/caption trong calendar TRƯỚC khi chạy meta.py (meta đọc caption từ calendar).
- Chạy `--no-render` để đo độ dài trước, cắt chữ cho vừa khung format rồi mới render final.

- 09/10/2026 16:00: Kiểm tra lượt 15:50 — #1–#12 đã render xong (tới 15/10 20:40) và có trên box /workspace/tiktok/ready; không cần render thêm lượt này.

## 7. Lô #13–#18 (09/10/2026)
- Chữ kinetic mà MỌI từ đều có trong lời đọc sẽ tự chạy hiệu ứng "sync": từng chữ chỉ sáng khi được đọc (trước đó mờ 16%). Hook cần hiện ngay trong 3 s đầu thì dùng chữ khác lời đọc (vd "MÙNG 8 ÂM" dạng số, "ĐỐ: MỖI THÁNG") hoặc chữ được đọc ngay đầu câu; neo thời gian (float) KHÔNG thắng được sync.
- KHÔNG khởi động nhiều build cùng lúc: bud_variety.json bị ghi đè đồng thời → hỏng JSON / mất bản ghi. Giãn mỗi lần khởi động ≥ 20 s; nếu hỏng: sửa bằng raw_decode và sắp lại bản ghi theo thứ tự lịch (build mới bị so với bản ghi cuối cùng, không phải video liền trước trong lịch).
- Chuyện xưa với giọng Thiền Tâm Đức ≈ 2,9 chữ/s: 130 chữ → 49,9 s; 112 chữ → 44,2 s. Mục tiêu ≤ 112 chữ cho 11 câu, gap 0,45.
- Neo "Tỳ-kheo": từ có gạch nối được chuẩn hóa thành một token ("tỳ-kheo").

## 8. Lô #19–#26 (19–22/10)
- Chữ kinetic có `size` không tự xuống dòng: giữ (số ký tự × size) ≤ ~1500. "MỘT CUỘC GỌI" size 150 (1800) và "CÒN 3 NGÀY" size 170 (1700) bị cắt ở bản nháp → hạ xuống 112/125. Kiểm tra trước khi dựng bằng vòng lặp len(text)*size trong mk.py.
- Ngày lễ (20/10 Ngày Phụ nữ VN): đổi chủ đề trong lịch sớm (đưa chủ đề cũ vào `backlog`), sửa CTA + hashtag của video cùng ngày; nội dung vẫn phải có nguồn kinh (AN 8.51, AN 1.235, Thig).
- Caption dạng danh sách: không để dòng trần "2. ..." — gộp thành câu "(diễn ý): a, b, c; d"; nhiều nguồn ngăn bằng "; ". addmeta.py đã tự kiểm tra cả hai.
- Mỗi lô: chạy --no-render tuần tự cho tất cả trước (ledger đúng thứ tự lịch), rồi mới chạy nháp 2 làn lệch nhau 30 s.

## 9. Lô #27–#34 (09/10/2026)
- **Marker/tape fx cắt dấu thanh phía trên** (Ũ, Ằ, Ậ…): luôn chạy `mkscan.py <slugs>` sau draft; item nào bị cờ thì đặt `fx="outline"` (đã sửa BÁT QUAN TRAI, RẰM THÁNG 9, LẤY THIỆN THAY ÁC, VÌ SAO?, VŨNG BÙN).
- **Tốc độ giọng thực tế chậm hơn ước tính**: Quang Sơn ~3.0 từ/s, Mỹ Duyên ~2.9 → #27 (32.6s) và #33 (31.4s) vượt max format, phải cắt lời. Thanh Bình lại nhanh (~3.7) → #32 thiếu min 35s, phải thêm chi tiết đúng nguyên truyện ("nhất là người trẻ đẹp. Nguy hiểm lắm."). Đo voice-only trước khi render draft.
- **Scene không clip** (`clip: null`) dùng tốt cho open_shot "chu-tren-nen" (chữ trên nền tối, hook đọc được từ giây 1).
- **Khởi động build cách nhau ≥20s kể cả giữa các lane khác nhau** — lô này có 2 lần suýt đụng (4s, 1s); ledger vẫn hợp lệ nhưng đừng thử vận may. Lane nên chờ file `.done` + `timeout 20`.
- **Render bị huỷ "render_cancelled_parent_exited"**: một final (#33) chết sau 12s khi khởi động gần lúc lane khác kết thúc; chỉ cần xếp lại, không phải lỗi spec.
- **Lịch**: rằm tháng 9 = Nam tông mãn hạ / lễ Tự tứ (Pavāraṇā). "Ngày Tăng Bảo / Tự tứ Bắc tông" là rằm tháng 7 — không gọi rằm 9 là Ngày Tăng Bảo.
- **Pexels không có clip tượng ấn xúc địa nhận diện được** — dùng tượng ngồi B&W + cận cảnh tay chạm đất/rêu, chữ ghi rõ "ấn xúc địa".
- **Clip CTA**: tránh cảnh cặp đôi áp má/ôm tình cảm cho video ngày vía (#34 đổi sang đèn trên sông 34614213).

## 9. Lô #35–#42 (27–30/10) — chuẩn "mix" cho BUD (13/10/2026)
- build.py: luật mix_lint / hold khung 0 / chặn size >980px nay áp cho cả theme "bud" (trước chỉ mim, ck). theme-bud.css có thêm khối CSS biểu đồ `.ch*` (bài học ec85ff8) + tông vàng nghệ cho cards3d/board glass.
- Analytics (13/10): người xem rời ở giây 1–3, xem TB ~4 s, xem hết 0–5 %; bài tốt nhất là bài theo ngày âm lịch (mùng 1/9: xem TB 10,6 s, 12,7 % xem hết, có lượt từ tìm kiếm). => Khung 0 = clip có chuyển động + câu "nỗi đau" (MẤT NGỦ?, LƯỚT CẢ NGHÌN DÒNG, CẦN AI ĐÓ LẮNG NGHE?), không dùng thẻ chữ. Độ dài 19–27 s. Kết bằng câu HỎI để kéo bình luận. Caption có từ khoá tìm được (19/9 âm lịch, vía Quán Âm, mất ngủ, kinh Pháp Cú).
- Clip trăng/đêm (moon) quá tối cho khung 0 -> mở bằng clip có người/ánh sáng ấm; trăng để giữa video.
- cards3d 4 thẻ tràn xuống vùng phụ đề -> tối đa 3 thẻ; 4 ý thì dùng ledger.
- mix_lint: "một kiểu cảnh > 60%" dễ dính với Short toàn clip -> mỗi Short cần ≥1 board/cards3d và ≥1 counter/date/ledger. Look xoay theo sổ short_looks.json (kênh BUD), cảnh báo chuỗi cảnh trùng 3 video gần nhất.
- Nút cuối của board xuất hiện khi từ neo được đọc: neo nút "kết luận" sớm trong câu, nếu neo ở cuối câu chỉ thấy <1 s.
- Start-Process render lane PHẢI ở lệnh Shell trả về ngay; nếu lệnh Shell bị đẩy nền/kết thúc trong lúc render, HyperFrames báo render_cancelled_parent_exited.


## 10. Lô #43–#50 (31/10–3/11)
- Đổi chủ đề #45 (4 việc ổn định = AN 8.54, trùng #41) sang "chia tiền 4 phần" (DN 31). Trước mỗi lô: kiểm tra trùng nguồn kinh với 10 video gần nhất.
- Không có âm chuông thật trong repo (sfx tự tổng hợp: scratch/whoosh). Bài về chuông/chuông xoay cần nạp file chuông CC0 vào thư viện sfx trước khi làm.
- Board: neo nút cuối sớm (giữa câu), không neo từ cuối câu (vd "Phật.", "giúp") -> nút chỉ hiện <1 s. Sửa #44/#50 bằng neo sớm.
- cards3d: giữ ≤3 thẻ, chữ "k" là nhãn nhỏ — ý chính phải nằm ở "v". Counter dùng làm số liệu (4 PHẦN, 10 PHÚT, 22) khi bài không có số thật -> chọn số có nghĩa, tránh số trích dẫn khô (vd "22" kinh số).
- Tất cả 8 video 17–27 s; mở bằng clip có chuyển động + câu đau/đố.

