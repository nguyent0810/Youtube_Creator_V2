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


## 11. Lô #51–#58 (4–7/11)
- Không bài nào trong lô cần chuông/chuông xoay -> chưa thêm file chuông CC0. Bài #52 "nghe mưa" chỉ có nhạc + giọng: tiếng mưa thật sẽ tốt hơn, cần hỗ trợ "ambience" (file CC0) trong sfx.py — việc nên làm trước bài tĩnh lặng tiếp theo.
- mix_lint >60% M: Short 5 cảnh với 2–3 câu dài trên clip dễ vượt. Đếm thời lượng theo câu, không theo số cảnh; đổi 1 cảnh clip sang board hoặc bỏ clip của slam.
- Look "terminal"/"left": kinetic chữ một dòng không clip trông nhỏ, lệch trái -> câu nhấn riêng dùng slam (to, giữa) thay vì kinetic không clip.
- Chuyện xưa 6 câu với Thiền Tâm Đức + gap 0,35 ra 28 s; cắt câu xuống ≤ 60 từ và gap 0,25 -> 24,6 s.
- File lịch đăng: /workspace/tiktok/ready/sched_A_B.txt ('#N | post_at | path', caption, '---').


## 12. Lô #59–#66 (8–11/11/2026)

- **Nền môi trường CC0 (mới):** spec có thể ghi `"ambience": "rain"` hoặc `{"bed": "rain"|"water", "gain": 1.0, "hits": [{"at": giây, "kind": "bell"|"gong", "gain": 1.0}]}`. File nằm ở `motion/stier/ambience/` (rain, water, bell, gong; đều CC0 1.0, nguồn ghi trong `LICENSES.json`). Nền được lặp với crossfade 1,5 s và cộng SAU bước chuẩn hoá đỉnh của sfx, nên mức không đổi giữa các video; `build.py` tự ghi dòng "Sound: …" vào credits.json → caption thêm dòng "Âm thanh: …".
  - Đã dùng: #60 mưa (gain 0.9), #61 chuông chùa ở 0,1 s, #62 suối + gong. Mức sfx.wav trung bình −24…−26 dB (so với −30 dB khi không có nền).
- **Lặp chủ đề:** lịch cũ cho #59 cũng là "vía Dược Sư 30/9" – trùng #58. Đã đổi thành "30/9 âm – ngày cuối tháng: tự hỏi" (AN 10.48). Nhớ dò trùng với lô trước khi soạn.
- **Lint lô này:** `nhan-gui` và `chuyen-xua` đều bị chặn vì "thiếu cảnh số liệu" → cần ≥1 counter/date/ledger. Counter `to: 0` ("0 NHÀ – chưa từng có ai mất") dùng được và đúng nội dung.
- Không được lặp hook_type với video liền trước (#63 noi-dau → #64 đổi sang nghich-ly).
- **CTA dài ≥ 22 ký tự trong look notebook/terminal bị co nhỏ** (nhỏ hơn cả dòng sm). Giữ CTA ≤ 18 ký tự ("BẠN NGHĨ GÌ NHIỀU?", "GIỮ VIỆC TỐT NÀO?", "ĐIỀU ĐẦU TIÊN?"); phần còn lại đưa xuống dòng sm.
- Credit Pexels gộp theo tác giả (2 clip cùng tác giả → 1 tên), nên số tên có thể ít hơn số clip. Luôn lấy từ credits.json của bản render cuối.
- File lịch đăng: `sched_59_66.txt`, cùng định dạng.

## 13. Lượt 15:50 — 13/10/2026 (UTC+7)

### Analytics (TikTok Studio Home, @hanhtrinhgiaithoat)
- Followers ~932; 7-day video views ~1.8K (+4.2%).
- Mới đăng #7 (13/10 11:40, kệ 252): ~81 views / 7 likes (còn sớm).
- #6 (12/10 21:10, Hakuin): ~126 views / 2 likes.
- Vẫn kẹt ~110–150 views/video; avg watch trước đó ~4s, drop 0:01–0:03.

### Thuật toán 2026 (nghiên cứu ngoài + khớp analytics kênh)
- Tín hiệu chính: giữ chân 0–3s, completion, rewatch; like/follow yếu hơn.
- Hook phải có (1) chuyển động/chữ to 0–0.5s, (2) câu nói/keyword ≤1.5s, (3) "đây là cho ai" trước 3s. Cấm logo/chào/intro chậm.
- Search TikTok: nhét từ khóa vào 3s đầu (voice + chữ), caption, hashtag — vòng đời dài hơn FYP.
- Video ngắn 18–27s (đã áp từ #35) dễ completion hơn 35–45s chuyện xưa; chuyện xưa cần payoff sớm + loopable cuối.
- Pattern interrupt ~giây 3 (đổi góc/zoom/sfx) giúp qua ngưỡng scroll.

### Pipeline trạng thái lúc 15:50
- Ready trên box: #1–#66 (tới 11/11). Lịch PC: #35–#66 = rendered, #67+ = planned (specs đã có).
- Cần xác minh hàng đợi Schedule trên Studio; giữ ≥2–3 ngày lịch đăng.
- Render tiếp #67–#74 qua grokbot-stage/nolock_build_args.py (lock đang giữ bởi kênh MIM khác).

## 13. Lô #67–#74 (12–15/11/2026)

- **Vượt 60% một kiểu cảnh:** #68 có 3 clip cộng 1 clip đóng khung (win) → 60%. Đổi cảnh đóng khung thành slam không clip là đạt. Quy tắc nhanh: tối đa 3 cảnh M trong video 6 cảnh.
- **Số lời (tốc độ giọng ~3,8 từ/giây):** 58–62 từ + gap 0,3 → chỉ ~17,7 s (#74 bị ngắn); 73 từ + gap 0,3 → 26 s (#70 bị dài). Mục tiêu 65–72 từ với gap ≤ 0,2, hoặc ~60 từ nếu gap 0,5–1,0.
- Counter `to: 0` tiếp tục dùng được làm cảnh số liệu có nghĩa ("0 QUẢNG CÁO", "0 LẦN CHÁN ĐỜI", "0 CÔNG ĐỨC?").
- Cảnh báo "chuỗi cảnh trùng 1 trong 3 Short gần nhất" xuất hiện ở #70 và #74: chấp nhận được, nhưng lô sau nên đảo vị trí board/counter.
- **Nền ambience:** #69 dùng chuông lúc mở, #72 dùng sóng/suối, #74 dùng mưa nhẹ (gain 0.6).
- CTA ≤ 16 ký tự vẫn là an toàn nhất trong look có highlight ("BẠN NGHĨ LÀ GÌ?").
- File lịch đăng: `sched_67_74.txt`.


## 14. Lô #75–#82 (16–19/11/2026)

- **Đổi vị trí board/counter để tránh lặp thứ tự cảnh:** lên sẵn chuỗi cảnh cho cả lô trước khi viết lời. Chuỗi phải khác nhau trong lô và khác 3 Short gần nhất. Lô này dùng: M G D G M · M T D G M · M G D M G M · M G M T D M · M D G G M · M G T D M · M D G M G M · M T G D M → **không còn cảnh báo trùng**.
- Đưa slam không clip (T) vào vị trí 2 hoặc 4 vừa đổi nhịp, vừa giữ M ≤ 60%.
- **Độ dài:** nhan-gui với gap 0,5 + 69 từ = 26,2 s (quá dài) → gap 0,25. chuyen-xua 66 từ + gap 0,15 = 17,8 s (quá ngắn) → thêm 5 từ, gap 0,3. Công thức ước lượng: giây ≈ từ/3,4 + gap×(số câu−1) + 1.
- **Clip đúng nghĩa:** tìm "wheel wooden" ra vòng đu quay (ferris wheel), không hợp với bánh xe Pháp → đổi sang guồng nước gỗ. Cũng không dùng ống "prayer wheel" (Tây Tạng) để minh hoạ Dharmacakra, vì đó là hai vật khác nhau.
- CTA có highlight: tiếp tục giữ ≤ 16 ký tự.
- File lịch đăng: `sched_75_82.txt`.


## 15. Lô #83–#90 (20–23/11, có Rằm tháng 10 = Tết Hạ Nguyên)
- Ước lượng words/3.4 hụt ~2.5–3 s với video 6 dòng/gap 0.2 (dự 22–23 s → thực 25–26 s). Với 6 dòng: nhắm ≤ 65 từ, gap 0.1–0.15.
- Kinetic có 2 item: anchor của dòng nhỏ (sm) phải nằm SAU anchor của dòng chính, nếu không frame đầu hiện dòng nhỏ trước, chồng lên tiêu đề (#83, #90).
- Ngày đặc biệt (Rằm Hạ Nguyên): ambience water + bell/gong mở đầu, clip trăng tròn + đồng lúa VN thu hoạch; counter dạng ngày "15/10 ÂM" làm D-scene rất hợp.
- Đã xác minh 23/11/2026 = 15/10 âm (lunardate). Tên riêng Pali trên màn hình nên dùng phiên âm Việt (La Hầu La, Mạt Lợi) để tránh lỗi dấu ā/ṅ; giữ Pali trong caption.
- Thứ tự cảnh lên kế hoạch trước cho cả lô → 0 cảnh báo lặp.


## 16. Lô #91–#104 (24–30/11, kết thúc lịch tháng 11)
- Ước lượng hiệu chỉnh: words/3.4 + gap×(lines−1) + 1 + (1.5 nếu 5 dòng, 2 nếu 6 dòng) — khớp thực tế lô #83–#90.
- gen.py nay tự assert: anchor tồn tại, dòng nhỏ (sm) có anchor SAU dòng chính, số cảnh = số dòng.
- PowerShell không phân biệt hoa/thường tên biến: $S và $s là MỘT biến → đã làm hỏng r91.cmd lần đầu (tự dừng trước khi render). Dùng tên biến khác hẳn ($SL, $L).
- Tĩnh lặng (#98, #100): gap 0.5–0.6, ≤ 56 từ, ambience rain/water; vẫn cần 1 D-scene (đếm hơi thở / giây). Hook "30 giây" đổi thành "20 giây" cho khớp độ dài video thật.
- Pexels không có clip mõ gỗ (mokugyo) → dùng cận cảnh mắt cá mở cho hook "vì sao hình con cá".

## 17. Lượt 09:50 — 14/10/2026 (UTC+7)

### Analytics (Studio Home + Posts, @hanhtrinhgiaithoat)
- Followers 932; 7-day views 1.8K (+4.2%); likes 7d 107 (−51%); comments 8; shares 0.
- #9 (14/10 06:35, Kalama / Hiểu đúng #2): ~51 views early / 0 likes.
- #8 (13/10 20:30, Ba Vedehika): 124 views / 1 like.
- #7 (13/10 11:40, kệ 252): 122 views / 8 likes (best likes in recent set).
- Baseline vẫn ~110–127 views/video; #9 buổi sáng còn sớm.

### Hàng đợi Studio
- Logged in OK. Scheduled filter: queue còn tới **03/11/2026 20:45** (POV “ai cũng tìm đến bạn…” = #50).
- Đêm nay #10 (Nếu bạn sắp đi ngủ) đã schedule 14/10 19:45.
- Buffer >> 2–3 ngày; chưa cần đẩy lô #51+ trong lượt sáng.

### Nghiên cứu thuật toán (xác nhận lại 14/10)
- Tín hiệu chính vẫn: watch-time ratio / completion / rewatch > like/follow.
- Hook 3 lớp 0–3s: chuyển động/chữ to → câu nói ≤1.5s → “cho ai + được gì”.
- VN healing/Phật: lời đời thường ngắn (mối quan hệ, lo âu) thắng thuật ngữ nặng — mẫu Thầy Giác Minh Luật.
- Giữ 18–27s + keyword search trong 3s đầu + caption (đã áp từ #35). Shares = 0 trên 7 ngày → thử CTA “gửi cho người đang…” trên vài bài chưa render lại / caption sắp xếp (không đụng video đã schedule).

### Việc tiếp
- 15:50: kiểm tra #9 mature views + #10 còn schedule; nếu ổn mới xét schedule #51–#58.
- 21:50: báo cáo VN cho user.


## 14/10/2026 — BUD v2 (port Shorts Studio vào motion/stier, chỉ theme bud)
- Cảnh mới: `source` (thẻ dẫn kinh chữ lớn, "· DIỄN Ý" cùng dòng nguồn, [[tô sáng]], dấu "ĐÃ ĐỐI CHIẾU"); `quote` + `"mode":"karaoke","line":n` (chữ sáng theo mốc từ đo từ giọng; ẩn dòng phụ đề trong cảnh). Text karaoke phải trùng nguyên câu thoại.
- `"loop": true`: +0,5 s cuối lặp lại cảnh móc (kinetic+clip, hold) -> xem lại liền mạch; khung 0 vẫn là footage chạy.
- `"v2": true`: chặn khi 2 cảnh liền nhau cùng bố cục/hướng chuyển động hoặc < 3 kiểu bố cục; chạy `hyperframes check` (lint/runtime/layout/contrast) trước render, lỗi = dừng. Báo cáo: output/stier/<slug>/check.json.
- `hyperframes check` 0.8.75 không chạy được engine casefile qua <script src> (DOM chưa có) và tách thẻ <video> -> bản sao kiểm phải nhúng engine nội tuyến + cờ __HF_CHECK (thay video bằng khung giữ chỗ) + hard-link clip. Đừng dùng junction cho assets (rmtree xuyên junction là xoá thật).
- Check bắt được lỗi thật: nhãn vàng (--red của bud) trên thẻ kem chỉ 1,64:1 -> đổi nâu đậm #7a3f10. #scrims phủ thẻ là có chủ đích -> data-layout-allow-occlusion.
- Render lại bản v2 của video đã có: đặt BUD_VARIETY=off (luật "clip mở đầu đã dùng" sẽ bắt chính bản gốc).

## 14/10/2026 — BUD v2.1: thiết bị Shorts Studio trong bud (hf_*)
- 10 thiết bị: hf_wheel, hf_cycle_draw, hf_myth_strike, hf_split, hf_time_spine, hf_calendar, hf_count_ring, hf_unit_grid, hf_list_build, hf_stamp (tiền tố hf_ vì split/calendar đã có ở MIM/CK). File: motion/hf/assets/engine/hfs/*.js (chép nguyên từ feat/shorts-studio) + bridge.js; chỉ nạp khi spec bud có cảnh hf_*.
- Mọi [câu,"từ"] ở bất kỳ độ sâu trong cảnh hf_* được đổi ra giây (strikeAt, truthAt, noteAt, items[].at...). KHÔNG đặt "at" thứ hai trong cảnh (trùng khoá "at" = mốc bắt đầu cảnh).
- Nền giấy da saffron chỉ là tấm 210–1440 px: chừa kicker trên và dải phụ đề trắng dưới (nếu phủ toàn khung -> phụ đề trắng mất tương phản).
- Font BUD (Playfair) cao hơn Newsreader: count_ring cần đẩy đơn vị xuống (.cr-suf 1050px); list_build phóng chữ 104px, bỏ dòng phụ nhỏ.
- Luật mix: hf_list_build tính là D (bảng/danh sách như ledger); tối đa 1 cơ chế tròn (wheel/cycle_draw/count_ring).
- Loop: clip móc của cảnh loop giờ bắt đầu đúng lúc loop (trước đây sớm 0,2 s đè lên CTA).


## 18. Lượt 15:50 — 14/10/2026 (UTC+7)

### Analytics (Studio, 16:00)
- Followers 933 (+1 so với sáng); 7 ngày: 1.9K views (+3.5%), 99 likes (−43%), 8 comments, 0 shares, 2 profile views.
- #9 Kalama (06:35 hôm nay): 112 views / 2 likes sau ~9h → vẫn kẹt baseline 110–127.
- Top likes vẫn là bài gắn ngày âm lịch (Mùng 1 tháng 9: 117v/16♥/3 cmt) và kệ ngắn đời thường (kệ 252, kệ 227–228: 8♥). Chuyện xưa / Hiểu đúng: 1–3♥.
- Views gần như phẳng mọi format → vấn đề nằm ở 0–3s (lượt đẩy đầu ~110 người), không phải chủ đề. Chờ A/B v2 (#94/#102) + bài extra 21:30 tối nay để so.

### Hàng đợi
- Tối nay: #10 19:45 + extra-1014 (Pháp Cú 3–4 "tua lại câu nói") 21:30 — cả hai đã schedule.
- Đã schedule thêm #51–#56 (04/11 11:30 → 06/11 20:25). Queue giờ tới **06/11/2026 20:25**. Lô tiếp: #57 (07/11 09:40).
- #51 caption dư ~3 ký tự (dòng trống trước hashtag) — không sửa.
- Đổi caption (chỉ bản đăng TikTok, chưa sửa JSON): #52 CTA "Gửi cho người đang mệt", #55 "Gửi cho người bạn muốn cùng làm" → thử kéo shares (7 ngày = 0).
- Lưu ý: hộp thoại "Continue to post? … Post now" sau khi bấm Schedule chỉ bỏ qua chờ kiểm duyệt; bài vẫn giữ giờ hẹn.

### Việc tiếp
- 21:50: báo cáo VN cho user; so #10 và extra 21:30.
- Lô sau: #57–#62 khi buffer cần (vẫn >20 ngày).


## §19 — 2026-10-14 21:50

### Analytics (Studio Home + Posts, ~22:05 VN)
- Followers **933**; 7 ngày: **1.9K** views (+3.5% / +64), likes **99** (−43%), comments **8**, shares **0**, profile views **2**. Traffic vẫn ~97% For You.
- Hôm nay: **#9** Kalama 06:35 = **112v / 2♥** (ổn định baseline); **#10** POV ngủ 19:45 = **45v / 1♥** (~2h); **extra-1014** Pháp Cú 3–4 21:30 = **0v** (mới lên).
- Hôm qua: #8 Ba Vedehika 124v/1♥; #7 kệ 252 122v/8♥ (likes tốt nhất gần đây).
- #10 sớm thấp hơn buổi sáng cùng ngày — đo lại sáng mai; extra cần ≥6–12h trước khi kết luận.

### Calendar / queue (PC JSON, không phải Studio)
- Calendar `tiktok_calendar_2026-11.json`: **104/104** entries; status field = `planned`×34 (#1–#34) + `rendered`×70 (#35–#104). Không có cờ `scheduled` riêng trong JSON.
- Hôm nay theo lịch: **#9** 06:35 Kalama (planned trong JSON); **#10** 19:45 nhắn gửi ngủ (planned trong JSON).
- Frontier Studio (theo §18 / memory 15:50): queue đã schedule tới **06/11 20:25 (#56)**; lô tiếp **#57 (07/11 09:40)**.
- Box ready #57–#64 có đủ mp4; staging PC: `grokbot-stage\b51\` (#57–58) + `b59\` (#59–64). Desktop `grokbot-tiktok` giữ #67–74 (allowlist CopyToBox).

### Research tips (late 2026, nguồn ngoài — giữ factual)
1. **Completion + 0–2s hook** nặng hơn like/follow; cắt mọi thứ làm drop sớm; mở bằng promise/visual/câu hỏi (miraflow 2026; Multilogin 2026 ~40–50% weight completion/watch).
2. **Độ dài**: niche healing/VN thường ổn **21–60s**; short 11–30s dễ virality nếu completion cao; 60–180s chỉ khi retention nửa đầu mạnh (Toklytics VN creator; Multilogin).
3. **Giờ VN**: sweet spot đại trà ~**18–21h** (đỉnh ~20h); kênh healing/Phật thường thêm sáng sớm (~6h) — đo bằng analytics kênh mình, không tin bảng chung (nhanhieu.ai / Buffer Mar 2026; ekhoo Tịnh Tâm ~6AM).
4. **Nội dung Phật VN**: 1–3 câu punch đời thường (cô đơn, giận, ngủ), không thuyết giảng dài; keyword trong 3s đầu + caption để Search (Rest of World Giác Minh Luật; Fint VN search playbook).
5. **CTA save/share/comment** rõ (gửi cho ai đang mệt) — shares/comments là tín hiệu utility; kênh đang 0 shares/7d (§18) → ưu tiên CTA hỏi ngắn ngữ pháp tự nhiên.

Nguồn: miraflow.ai TikTok Best Practices 2026; multilogin.com TikTok algorithm 2026; fint-global VN search; gma-asia TikTok VN; nhanhieu.ai khung giờ; restofworld.org Giác Minh Luật; toklytics @minhtrithienvien.

### Việc tiếp
- Điền số Studio vào khối analytics trên (cùng lượt 21:50).
- Lô schedule tiếp: **#57+ từ 07/11 09:40** khi buffer Studio cần (hiện còn tới 06/11).
- So retention #10 + extra-1014 vs baseline ~110–127; chờ A/B v2 (#94/#102).

## §20 — 2026-10-15 09:50

### Analytics (Studio Home @hanhtrinhgiaithoat)
- Followers: **933** (following 1; total likes 23K)
- 7d views: **1.9K** (+137 / +7.6%); profile views 5
- 7d likes: **98** (−51 / −34.2%); comments **7**; shares **0**
- Baseline posts vẫn ~110–150v:
  - #10 POV ngủ (14/10 19:45): **119v / 4♥**
  - #9 Kalama (14/10 06:35): **112v / 2♥**
  - #8 Ba Vedehika (13/10 20:30): **124v / 1♥**
  - #7 kệ 252 (13/10 11:40): **122v / 8♥**
- **extra-1014** Pháp Cú 3–4 (14/10 21:30): **0v / 0♥ / 0💬** sau ~12h — bất thường (không phân phối hoặc counter lệch). Theo dõi thêm tới 21:50; nếu vẫn 0 → kiểm tra bị hạn chế / watermark / upload lỗi.
- Hôm nay 15/10 đã schedule (0v vì chưa tới giờ): 11:55 #11 bọt nước; **12:15** Niệm Phật test; **18:15** Lá trong tay v3; 20:40 #12 đi bộ. 11:55↔12:15 chỉ cách 20 phút (chật).

### Calendar / queue
- Studio last slot: **06/11 20:25** (#56 cô đơn / SN 45.2). Trước đó 06/11 11:15 Kinh Điềm Lành. Ước ~46 scheduled.
- #51 cũ "Lá trong tay" quiz **vẫn** schedule **04/11 11:30** (trùng nội dung với test 18:15 hôm nay).
- PC **offline** lúc 09:50 → không sync `tiktok_learnings.md` / calendar JSON trên D:\. Append này nằm box: `/workspace/tiktok/learnings_append_20.md`.
- Buffer >> 2–3 ngày → **không** render/schedule #57+ lượt này. Next batch khi cần: #57 (07/11 09:40).

### Research tips (15/10)
1. Watch time / completion / replay > like; share/save/comment quan trọng (Hootsuite Jun 2026) — kênh vẫn **0 shares/7d**.
2. Hook 0–3s: câu hỏi / pain đời thường; SEO keyword VN trong caption + chữ + VO.
3. Phật VN: 1–3 câu punch, hạn chế thuật ngữ dày (pattern Giác Minh Luật).
4. Variety format giúp tránh feed lặp; giữ bud_variety.
5. A/B hôm nay: slot 12:15 vs 18:15 — đo khi đủ tuổi trước khi đổi lịch hàng loạt.

Nguồn: Studio Home 15/10 09:50; blog.hootsuite.com/tiktok-algorithm; socialboost.asia; vietnamnet Giác Minh Luật.

### Việc tiếp
- 21:50: cập nhật views extra-1014 + A/B 12:15/18:15; ping user VN nếu routine yêu cầu.
- PC online: sync §20 vào PC learnings; hỏi user xóa #51 (4/11) và #93 (25/11) nếu A/B thắng.
- Chỉ schedule #57+ khi buffer Studio < ~3 ngày.

## §21 — 2026-10-15 15:50

### Analytics (Studio, read-only)
- Followers 933; 7d views 1.9K (+7.6%); likes 98 (−34%); comments 7; shares 0; profile views 5.
- #11 bọt nước (15/10 11:55, old style, Đố vui #1): **114v / 12♥** sau ~4h — like rate cao nhất gần đây (~10%).
- **Niệm Phật v2 test (15/10 12:15): 0v sau ~3.5h.**
- **extra-1014 Pháp Cú 3–4 (14/10 21:30): 1v sau ~18h.** Không có cờ hạn chế; privacy Everyone.
- #10 POV ngủ 120v/4♥; #9 Kalama 112v/2♥; #8 124v/1♥; #7 122v/8♥.

### Chẩn đoán
- File v2 giống hệt file cũ về kỹ thuật (h264 1080x1920 30fps, AAC 48k stereo, Lavf62, 4–5 Mbps) → không phải lỗi encode.
- Cả 2 bài ~0 view đều là **bài "extra"** ngoài 2 slot/ngày, và đăng sát bài khác (21:30 cách 19:45 1h45; 12:15 cách 11:55 chỉ 20 phút). Giả thuyết mạnh: TikTok không đẩy batch đầu cho bài đăng dồn/quá dày (3–4 bài/ngày) trên kênh nhỏ — **không phải** do style v2.
- Hệ quả: A/B style v2 vs cũ đang **bị nhiễu** (v2 trùng với extra slot). Bài 18:15 Lá trong tay v3 cũng là extra (ngày có 4 bài: 11:55, 12:15, 18:15, 20:40) → kết quả cũng nhiễu.

### Đề xuất (chờ user / 21:50)
- Không thêm bài extra; giữ tối đa 2 bài/ngày, cách nhau ≥ 6h.
- Test v2 công bằng: **thay thế** một slot thường (vd #94 25/11, #102 29/11 đã dùng v2) thay vì thêm bài.
- Không xoá #51 cũ (04/11) / #93 cũ (25/11) cho tới khi có kết quả A/B sạch.

## §22 — 2026-10-15 21:50

### Trạng thái pipeline
- PC DESKTOP-2JA218A **offline** → không sync calendar/learnings lên D:\…; không render lô mới.
- Studio schedule tới **06/11 20:25** (#56 “Nếu bạn đang thấy…”) ≫ 2–3 ngày → **không schedule/render** lượt này. Next batch khi cần: #57 (07/11 09:40).
- Box ready #1–#104 đủ. 0 drafts; không restriction.

### Analytics (Studio, @hanhtrinhgiaithoat)
- Followers **933**; 7d views **1.9K** (+7.6%); likes **98** (−34.2%); comments **7**; shares **0**; profile views **5** (+150%).
- Traffic: FYP 96.1%, Search 2.1%, Profile 1.6%, Following 0.2%.

### Hôm nay / gần đây (views / likes / comments)
- **#11 bọt nước** 15/10 11:55: **115 / 12 / 0** — like-rate cao nhất gần đây (~10%).
- **Niệm Phật v2** 15/10 12:15: **không thấy trong Posts** (0 match caption; không có slot 12:15) — có thể xoá/fail/ẩn; cần xác minh.
- **#51v3 Lá trong tay** 15/10 18:15 (extra/new-style): **1 / 0 / 0** sau ~3.7h — gần như không phân phối.
- **#12 đi bộ** 15/10 20:40: **31 / 0 / 0** (~1.3h, còn sớm).
- extra-1014 Pháp Cú 3–4 14/10 21:30: **1 / 0 / 0** sau ~24h.
- #10 POV ngủ 120/4; #9 Kalama 112/2; #8 124/1; #7 122/8.

### Kết luận cadence / A/B
- Hai bài “extra/new-style” (Pháp Cú 3–4, Lá trong tay) = ~1 view; bài thường ~110–125. Niệm Phật test biến mất khỏi list → A/B style **vẫn nhiễu** + thêm rủi ro upload.
- Nghiên cứu 2026: early engagement quyết định FYP (đặc biệt <1K follower); completion/rewatch > like; đăng dồn chất lượng thấp hại hơn giúp. → **tối đa 2 bài/ngày**, cách ≥ ~6h; **không thêm extra**.
- A/B Shorts-mix chỉ trên slot thường đã gắn (#94/#102 v2); giữ #51 cũ 04/11 và #93 cũ 25/11 đến khi user quyết.

### Việc đang đổi
1. Không đăng extra / không dồn 3–4 bài/ngày.
2. Ưu tiên format đố vui (like-rate #11) + POV/hook đau đã đạt ~100v.
3. Học: search traffic còn 2.1% — caption/keyword âm lịch vẫn nên giữ để kéo Search.

### Blocker
- PC offline (learnings §20–§22 chỉ trên box). Bật PC để sync `tiktok_learnings.md` và render #57+ khi buffer gần hết (~22 ngày còn lại → chưa gấp).
- Niệm Phật 12:15 thiếu trên Studio — hỏi user / lần sau kiểm tra lại lịch sử xoá.

## §23 — 2026-10-16 09:50

### Analytics (Studio Home @hanhtrinhgiaithoat)
- Followers: **933**; 7d views: **1.9K** (+7.6%); likes **98** (−34%); comments **7**; shares **0**.
- Hôm nay: **#13** "Đức Phật không chê tiền…" 16/10 06:35: **~76v / 11♥ / 2💬** (~3.5h).
- Hôm qua:
  - **#12** đi bộ: **111v / 10♥**
  - **#11** bọt nước: **115v / 12♥**
  - **Lá trong tay** 18:15: vẫn **1v**
  - **Niệm Phật** 12:15: giờ đã thấy trong Posts nhưng **0v / ~22h**
  - **extra-1014**: vẫn **1v**

### Cadence / A/B
- Bài extra (3–4/ngày) vẫn gần như **0 reach** → giữ **tối đa 2 bài/ngày**; không thêm extra.
- A/B style v2 vẫn nhiễu vì trùng slot extra; chưa đủ tín hiệu sạch để đổi lịch hàng loạt.

### Calendar / queue
- Studio buffer tới **06/11 20:25 (#56)**; ~**43** scheduled; next batch **#57 (07/11 09:40)**.
- PC **online** lại; box ready **#57–#104**. Buffer ~21 ngày ≫ 3 → **không** render/schedule lượt này.
- Calendar JSON vẫn `planned` cho bài sớm; **Studio = source of truth** cho frontier schedule.

### Pending user (ghi chú — không ping)
- #51 cũ vẫn schedule **04/11 11:30**
- #93 cũ vẫn trên calendar **25/11**

### Việc tiếp
- Chỉ schedule #57+ khi buffer Studio < ~3 ngày.
- Giữ max 2/ngày; ưu tiên slot thường đã gắn v2 (#94/#102) khi test style.

## §24 — 2026-10-16 15:50

### Analytics (Studio Home @hanhtrinhgiaithoat)
- Followers: **933**; 7d views: **1.9K** (+31, +1.7%); likes **82** (−19, −18.8%); comments **6**; shares **0**. Profile views 6 (+200%).
- Hôm nay: **#13** "Đức Phật không chê tiền…" 06:35: **117v / 13♥ / 2💬** (lên từ ~76v sáng). #14 POV mất người thân **20:10** vẫn scheduled.
- Hôm qua: #11 bọt nước **116v/12♥**; #12 đi bộ **113v/10♥**; Lá trong tay **1v**; Niệm Phật **0v**; extra-1014 **1v**.

### Cadence / A/B
- Extra vẫn ~0 reach → giữ **max 2 bài/ngày**.
- Regular ~110–120v ổn định; engagement #13 khá (13♥/117v).

### Calendar / queue
- Studio buffer tới **06/11 20:25 (#56)**; ~43 scheduled; next **#57 (07/11 09:40)**.
- PC **online**; box ready **#57–#104** (48/48). Buffer ~21 ngày ≫ 3 → **không** render/schedule.
- Pending (không ping): #51 cũ 04/11 11:30; #93 cũ 25/11.

### Việc tiếp
- Chỉ schedule #57+ khi buffer Studio < ~3 ngày.
- 21:50: báo user ngắn (VN) theo routine.

## §25 — 2026-10-19 (nghiên cứu công thức + lô v3 #57–#64)
**Nghiên cứu đầy đủ:** `research_cong_thuc_2026-10-19.md` (bản trên box `/workspace/tiktok/`; mọi số liệu đều có link nguồn).
- **Chẩn đoán 10–18/10:** mọi bài dừng ở 110–160 view; rớt ở 0:01–0:03; xem trung bình 4–5,6 s; xem hết 0–5%; share = 0; ~96% traffic từ For You. → kẹt ở cửa 1 vì **hook/khung đầu**, không phải bị bóp. Bài đăng chen (3–4 bài/ngày) = 0–1 view → **giữ 2 bài/ngày, cách nhau ≥ 6 h, không chen.**
- **Theo nguồn chính thức của TikTok:** xem hết một video dài là tín hiệu nặng; follower không phải yếu tố trực tiếp. Thứ tự tín hiệu (không chính thức): watch/completion → rewatch → share qua DM → save → comment → like.
- **Mốc:** giữ chân 3 s ≥ 55–60%; mặt bằng nền tảng xem 3,75 s và 4% xem hết (Metricool). Kênh mình mới ngang mức trung bình.
- **Hook:** khoảng trống tò mò và tính cấp bách thắng (OSF, 46.605 hook). Hook cảm xúc kéo share. Không dạo đầu, không "Hôm nay…/Nếu bạn…/POV…".
- **Độ dài:** Buffer (1,1 triệu video) cho thấy video 30–60 s có reach cao hơn, nhưng hook mới quyết định → thử Chuyện xưa 30–40 s.
- **SEO:** từ khóa nói ra trong 3 s đầu, hiện trên màn, có trong 100 ký tự đầu caption; 3–5 hashtag cụ thể; bật phụ đề tự động tiếng Việt.

### Công thức v3 "Đố · Hé · Làm · Gửi"
1. 0–2 s: câu đố hoặc nghịch lý đời thường ≤ 10 chữ, có từ khóa; chữ to + clip chuyển động ở khung 0; A/B/C hoặc "số mấy?" hiện trên màn.
2. Vòng mở → đáp án ở 35–60%; có một câu móc lại ở 30–75%.
3. Hé một câu kinh (dẫn nguồn ≤ 8 chữ, ghi "diễn ý", số hiệu đưa lên thẻ nguồn).
4. Làm một việc cụ thể có con số (10 phút, 3 chữ, 1 dòng, 1 cái tên).
5. Gửi: câu cuối là câu hỏi, gọi lại hook, kèm **người nhận cụ thể** hoặc comment một chữ.
6. 18–25 s, nhịp 3,2–3,5 từ/giây (Chuyện xưa thử 30–40 s).
7. Series có số: Đố bạn đời thường #N · 14 ngày biết ơn · Ngày N · Phật dạy về tiền #N · Chuyện xưa · Tập N.
8. Caption: dòng 1 = từ khóa + câu hỏi; CTA "💬 … · 📩 Gửi cho …"; 3–5 hashtag.
9. Một tuần 14 bài: 4 Đố, 3 Phật pháp đời thường, 2 lịch âm, 2 Chuyện xưa, 2 tĩnh lặng, 1 Hiểu đúng/Vì sao; POV ≤ 1 bài/tuần.

### Lô v3 #57–#64 (07–10/11, giữ nguyên giờ đăng để A/B sạch)
Spec: `data/stier/specs/*-v3.json` (nguồn sinh: `plan_v3/mkspecs.py` trên box). Bài cũ vẫn giữ trong manifest dưới `old_path`.
- **Lỗi gate gặp phải và cách sửa:**
  - `counter` có suffix ngắn ("4 KIỂU", "3 CHỮ") → cỡ chữ 300px làm dấu chồng lên `countlbl` → content_overlap. **Dùng suffix ≥ 8 ký tự** ("4 KIỂU BẠN", "3 CHỮ THÔI").
  - `hf_stamp`: kick "ĐÁP ÁN" chồng big "C" (t≈8 s) → để kick rỗng.
  - `hf_stamp` kick đập vào số to ở #60 → thay bằng `counter`.
  - Chữ to kinetic cuối quá dài chồng chữ nhỏ → rút ngắn ("GIỮ VIỆC TỐT NÀO?").
- **Nhịp R6:** gap 0,1–0,15 cho ra 4,1–4,3 từ/giây với giọng Thanh Bình (78–93 từ / 20–22 s). **Quy tắc nhanh: số từ ≤ 3,4 × (thời lượng TTS − 1); mỗi +0,1 gap ≈ +0,1 s × (số dòng − 1).** Bài 8 dòng ~85 từ cần gap ≈ 0,7–0,85.
- Gate cho phép chồng dòng trong cùng một cảnh kinetic (build.py bỏ qua) → `check.json` có thể ghi ok=False dù END OK; tin dòng END.

### Thử nghiệm (đo ở 48 h, trong Studio)
Mục tiêu mỗi video: 3 s ≥ 55% · xem trung bình ≥ 7 s · xem hết ≥ 10% · share ≥ 1 · tim/view ≥ 8% · comment ≥ 2 · view ≥ 250 (≥ 500 = qua cửa 1).
- **E1:** v3 vs baseline (#57–#72 vs bài tháng 10).
- **E2:** CTA gửi vs CTA comment.
- **E3:** độ dài 30–40 s.
- **E4:** series 14 ngày biết ơn (ngày 1/5/11/15).
- **E5:** khung trưa vs sáng.
- Mỗi nhánh cần ≥ 6 video mới kết luận; nhánh thua 2 tuần liền thì bỏ. **Mục tiêu tháng 11: ≥ 3 video > 500 view, 1.000 follower trước 30/11.**
- Lịch tháng 12 nháp (2 bài/ngày, #105–#166): `data/stier/tiktok_calendar_2026-12.json`.

## 26 - 2026-10-19 (lô v3 #65-#72: bài học lint + dựng)

- Câu được tách chỉ theo dấu . ! ? — dấu phẩy, hai chấm không cắt câu. Mỗi câu ≤ 14 từ, phần dẫn nguồn trước dấu hai chấm ≤ 8 từ (R3).
- Regex trích dẫn bắt cả "kinh điển", "chép kinh", "lời kệ": tránh các từ này trước mốc 25 % thời lượng. Có trích kinh thì phải có "diễn ý" (R10).
- "Kinh Pháp Cú, diễn ý" đã quá dày (R8: "pháp cú diễn" > 3/15 kịch bản). Xoay vòng: "Phật dạy, diễn ý:", "Kinh Pháp Cú dạy:", "Một câu kệ:", "Kệ Pháp Cú dạy:".
- R2 (câu nối "nhưng / thật ra") đo theo thời gian thật sau TTS (30-75 %), không theo số từ — giọng chậm đẩy câu nối ra sớm hơn ước tính. Đặt câu nối ở khoảng 40-60 % số từ.
- Tốc độ đo được (giây/từ, chưa tính gap): Thanh Bình 0,23 · Ngọc Linh 0,26 · Ngọc Trân 0,29 · Thục Đoan 0,29 · Quang Sơn 0,32-0,33 · Thiền Tâm Đức 0,33 · Mỹ Duyên 0,35. Giọng chậm chỉ đạt ~2,9-3,0 từ/giây dù gap = 0; muốn 3,2-3,5 từ/giây thì dùng Thanh Bình / Ngọc Trân / Thục Đoan / Ngọc Linh.
- Clip mở đầu phải khớp lời: kiểm ảnh thu nhỏ trước khi dựng (#67 suýt dùng tượng Di Lặc không có nhục kế cho câu hỏi về nhục kế).

## §27 — 2026-10-19 09:50 (UTC+7)

### Analytics (Studio Posts snapshot ~09:55)
- Logged in @hanhtrinhgiaithoat OK.
- Recent published: 18/10 POV tên độc ~146v/5♥; 18/10 Đố vui #3 ~147v/6♥; 17/10 Kẻ thù ~151v/3♥; 17/10 mùng 8 quiz ~162v/7♥; 16/10 POV phone 136v/2♥; 16/10 tiền 119v/13♥/2💬.
- Baseline vẫn ~110–160 view. Đố vui ổn định; bài tiền vẫn tỉ lệ tim cao nhất.
- Hôm nay #19 (5 cách gỡ oán giận) và #20 (Pháp Cú 103) còn scheduled (UI Studio hiện giờ UTC: 19/10 04:25 và 13:25 = 11:25 và 20:25 VN).

### Hàng đợi / sản xuất
- Lịch Nov: buffer Studio cần xác nhận đủ tới #56 (lượt này thấy vài bài scheduled ở đầu list — phải lọc Scheduled để đếm đủ; 15:50 sẽ xác nhận lại nếu cần).
- Đợt render v3 sáng 19/10 (nolock batch rb2–rb6): #73–#80, #83–#85 OK; #81 và #82 FAIL layout content_overlap (cần sửa spec rồi render lại). #86+ đang chạy.
- Tháng 12: `tiktok_calendar_2026-12.json` đã có 62 bài `planned-v3` trên PC. Công thức Đố/Hé/Làm/Gửi đã chốt trong research 19/10.
- Không đăng chen / không đổi slot đã schedule (theo yêu cầu user 19/10).

### Việc tiếp
- Sửa layout #81/#82 rồi render lại.
- Hoàn rb4→rb6 (#86–#104 v3 trừ A/B giữ nguyên nếu có).
- 15:50: đếm đủ Scheduled + kiểm #19 đã lên; 21:50 báo cáo VN.

### Bổ sung §27b — cùng lượt 09:50 (sau khi search Studio)
- Posts list mặc định **không hiện hết** bài scheduled xa: search "Rằm tháng 9" thấy hàng đợi còn tới ít nhất **28/10** (vía Quán Âm #36–#38), kèm #29 Rằm 24/10. Buffer thực tế vẫn > 2–3 ngày; **không** cần refill ồ ạt.
- Lượt này từng schedule nhầm trùng: #27 và #28 mỗi cái 2 lần (giờ UI UTC). Đã yêu cầu xóa bản sai (giữ 23/10 11:45 VN và 20:00 VN).
- Quy tắc: trước khi schedule thêm, **search caption/slug** hoặc lọc Scheduled đủ sâu — đừng kết luận thiếu buffer chỉ vì đầu list.
- Render v3 rb5: thêm FAIL layout (#90 ha-nguyen-biet-on, #95 nghiep, #96 tu-trach, #97 5-dieu-truoc-khi-noi). Cùng dạng content_overlap như #81/#82 (đã patch spec, chờ rb81).

### 28 - lượt 15:50 ngày 19/10
- Studio 7 ngày: 2K view (+4.6%), 85 tim (−25.4%), 7 bình luận, 1 share, 7 lượt xem hồ sơ; For You 96.7%, Search 2.1%. Khán giả 93.3% VN; 35–44 tuổi 26.9%, 45–54 24.7%, 55+ 22%.
- 17/10: quiz mùng 8 162v/7♥; "Kẻ thù" 151v/3♥. 18/10: Đố vui lời cuối 147v/6♥; POV tên độc 147v/5♥.
- **#19 (19/10 11:25, 5 cách gỡ oan gia, nhạc Arcadia) KẸT 1 view sau ~4.5h**: không có nhãn/cảnh báo, quyền "Everyone", video công khai mở được, nhưng traffic source toàn "-", avg watch 0.91s, thumbnail trong analytics màu xám. Giống hệt 15/10 18:15 "Lá trong tay" (1v), 14/10 21:30 extra Pháp Cú 3–4 (1v), 15/10 12:15 Niệm Phật (0v).
- Đã loại trừ: file mp4 bình thường (h264 1080x1920 30fps, AAC, âm lượng −16.9 dB trung bình, frame đầu có hình + chữ). Nhạc Arcadia không phải nguyên nhân (#3 và #13 cũng dùng Arcadia vẫn 110+ view).
- Giả thuyết: TikTok kiểm duyệt/xử lý bị treo âm thầm (thumbnail xám = chưa xử lý xong), hoặc lọc trùng lặp nội dung. Chưa xác nhận.
- Việc tiếp: lượt 21:50 kiểm lại #19 và #20 (20:25). Nếu #19 vẫn ~1 view và #20 bình thường → báo user, đề xuất (không tự làm) đăng lại #19 ở slot trống sau. Nếu #20 cũng kẹt → báo user là vấn đề cấp tài khoản.

## 29 - 2026-10-19 21:50 (UTC+7) — stub PC/box check (chưa có số Studio mới)

### Pending Studio
- **Chưa recheck Studio trong lượt executor này.** Cần parent/agent có browser xác nhận lại **#19** (11:25, 5 cách gỡ oan gia — kẹt 1v lúc 15:50) và **#20** (20:25, Pháp Cú 103) rồi mới ghi analytics.

### PC / box (đã kiểm)
- Calendar Nov: 104 entries; Dec: 	iktok_calendar_2026-12.json 62 entries (#105–#166, planned-v3).
- #57–#104: 43× `rendered-v3`; giữ cũ/A-B: #92/#93 (old), #94/#101/#102 (v2).
- Box `/workspace/tiktok/ready`: 43 file `*-v3.mp4` cho #57–#104 (thiếu đúng 5 số A/B trên). Research: `/workspace/tiktok/research_cong_thuc_2026-10-19.md`.
- #57 v3 sẵn: PC `output\stier\bud-dv-thang-cai-nhau-v3\final.mp4` + box `57-bud-dv-thang-cai-nhau-v3.mp4`; lịch 07/11 09:40; **chưa schedule** (buffer tới #56 = 06/11 20:25).
- Render lock/who trỏ long CK (cũ); không thấy python/ffmpeg đang chạy. **Không cần render BUD tối nay.**

### Việc tiếp
- Điền số #19/#20 từ Studio vào mục này (hoặc §30) khi có.
- Chỉ schedule #57+ khi buffer Studio < ~3 ngày.


## §30 — 2026-10-20 04:50 (UTC+7) — vì sao có bài 0–1 view + SEO caption #57–#104

### Chẩn đoán (so 5 bài kẹt với ~20 bài thường 110–162v)
- Bài kẹt: extra-1014 Pháp Cú 3–4 (14/10 21:30, 1v), Niệm Phật v2 (15/10 12:15, 0v rồi biến mất khỏi Posts), #51v3 Lá trong tay (15/10 18:15, 1v), #19 (19/10 11:25, 1v), #20 (19/10 20:25, kẹt theo user).
- Dấu hiệu chung: traffic source "-", xem TB 0,91 s, thumbnail xám → bài **không được vào lô thử FYP** (giữ phân phối/xử lý), không phải "nội dung yếu" (nội dung yếu vẫn có 50–150v lô đầu).
- KHÔNG phải nguyên nhân (giống hệt bài thường): cấu trúc caption, độ dài 560–710 ký tự, 4–5 hashtag cùng bộ (#loiphatday #chualanh #phattaitam…), credit Kevin MacLeod/Pexels, nhạc (Arcadia, Healing cũng có ở bài 110+v), độ dài 23–30 s, file mp4 (h264 1080x1920, có tiếng), giờ đăng (bài thường đạt 110–162v ở mọi khung 06:35–21:20; #19 11:25 và #20 20:25 cùng kẹt). Footage: 0 clip Pexels nào bị dùng lại giữa #0–#22.
- Bản lịch đăng #13–#26 (sched_*.txt) đã bỏ URL → link trong caption không giải thích được #19/#20. Các bài extra đăng tay có thể còn URL (chưa kiểm được).
- Tương quan mạnh: (1) 3/5 bài là **extra** chen vào ngày 3–4 bài, cách bài khác 20 phút–1h45; (2) **trùng nội dung**: Lá trong tay v3 = #51 đã xếp lịch 04/11; Niệm Phật v2 = #93; Pháp Cú 3–4 (oán giận) → 5 ngày sau #19 cũng "gỡ oán giận"; (3) đăng lại/xoá (Niệm Phật biến mất) → bộ lọc trùng lặp/spam có thể giữ cả các bài sau trong 1–5 ngày. Kiểm chứng: #21 (20/10 07:05) và #22 (20:35) — nếu bình thường thì đó là giữ tạm thời.
- Web (2026): 0 view + thumbnail xám = đang xử lý/review hoặc "not eligible for FYP"; nguyên nhân hay gặp: đăng lại/trùng lặp, đăng dồn, bài chưa xử lý xong; KHÔNG xoá-đăng lại cùng file. 3–5 hashtag liên quan; từ khóa ở dòng đầu; link trong caption không bấm được, nên bỏ.

### Đã sửa (#57–#104, chưa lên lịch TikTok)
- Caption SEO (`plan_v3/seo.py`, gọi cuối `mkcaps.caption`): dòng 1 có cụm từ khóa tiếng Việt hay tìm ("Lời Phật dạy khi…", "Đố vui Phật pháp", "Nghiệp là gì"…); bỏ mọi URL; nguồn rút gọn "Nguồn: Kinh Pháp Cú, kệ 201"; credit "Nhạc: Kevin MacLeod (CC BY 4.0) · Video: Pexels" (CC BY vẫn đủ ghi công); bỏ dòng âm thanh CC0 (CC0 không bắt ghi công); "#1" trong chữ → "số 1" (TikTok biến thành hashtag rác); hashtag 3–5: 1–2 chủ đề + #loiphatday #phatphap #phatgiao, bỏ tag tự đặt không ai tìm (#badieu #songtinh #nhangui #tamanmoingay #phattaitam #phatphapnhiemmau…). Độ dài ~700 → ~500 ký tự.
- Giờ đăng: dữ liệu không cho thấy giờ là nguyên nhân → giữ nguyên (2/ngày, ≥6h). Không render lại (hook/chữ trên hình không đổi).
- Manifest: `pre_seo_caption` giữ bản cũ; calendar 11 cập nhật caption/hashtags #57–#104.

### Luật mới
- Không đăng extra; không đăng 2 bài cùng chủ đề/kinh trong 7 ngày; không đăng lại/xoá-đăng lại; một bài kẹt thì chờ 24–48 h, không đăng bản sao.
- Rủi ro trùng sắp tới: #51 (04/11, đã xếp lịch) trùng Lá trong tay v3 đã đăng 15/10; #93 trùng Niệm Phật v2; #74 kệ 5 hận thù gần chủ đề oán giận (#19, extra-1014) nhưng cách >3 tuần.
