# T5 — 5 Short gắn Long `mim-watson-jeopardy` (Long lên Thứ Năm 19/11/2026 20:00) — bản 1, chờ duyệt cổng pha 1

Người viết: agent T5, 20/10/2026. Pha 1: chỉ viết file, chưa dựng, chưa đăng, chưa sửa `state.sqlite`. Spec nằm ở `docs/pm/tickets/2026-10-20-mim-nov/specs-T5/` (chưa ghi vào `data/stier/specs`).

## 0. Kết luận ngắn

- **Đủ 5 bài, đều là góc chưa dùng.** MIM đã có **12** Short về Watson/Jeopardy (mục 3). Tôi đã lọc 22 chương của kịch bản dài: các góc đã làm (Toronto/947 đô, ngưỡng 50%, 90 máy chủ, Jennings, tỉ số 77 nghìn, Rush Holt, 62 triệu, ca bệnh giả định, bán Watson Health, bấm chuông, Project Debater, "con ngựa đá") **bị loại hết**.
- **Hai bài yếu hơn ba bài kia** (S1 và S4), lý do ở mục "cần kiểm". Nếu chủ kênh/Claude thấy mỏng thì **cắt xuống 4 bài, đừng độn**; còn 1 góc dự phòng (S6, mục 5).
- Bài mẫu để duyệt trước khi làm hàng loạt: **S2** (có con số, có khuôn đã thắng).

## 1. Lịch (giờ VN, lấy từ `data/shorts_slots.json`; `scripts/shorts_grid.py 2026-11-13 2026-11-20 --channel MIM` ngày 20/10: 17–19/11 còn trống 0/5 slot bị chiếm)

Long ngày 19/11 là 20:00 (state.sqlite: `long-mim-watson-jeopardy`, `2026-11-19T13:00:00Z`, `Mt5hYcQxH50`). Ngày thường dùng slot 11:30 + 19:00; ngày có Long dùng 11:30 (xa Long, không đè). Không quá 2 Short/ngày.

| # | Ngày | Giờ | Slug | Tiêu đề (rút gọn) | Nhãn |
|---|---|---|---|---|---|
| S2 | T3 17/11 | 11:30 | `mim-watson-bon-nam-ferrucci` | Bốn năm trước trận đấu, Watson chơi rất tệ | SỐ/SỰ KIỆN |
| S4 | T3 17/11 | 19:00 | `mim-watson-khong-nghe-thay` | Watson lặp lại đúng đáp án sai của đối thủ | THỬ |
| S3 | T4 18/11 | 11:30 | `mim-jeopardy-1964-dap-an-truoc` | Jeopardy 1964: đáp án trước, hỏi lại sau | SỐ/SỰ KIỆN |
| S5 | T4 18/11 | 19:00 | `mim-watson-hang-tram-dap-an` | Watson không hiểu câu hỏi: nó chấm điểm hàng trăm đáp án | THỬ |
| S1 | T5 19/11 | 11:30 | `mim-watson-nha-hang-2004` | Bữa tối 2004, nhà hàng im bặt (theo lời kể) | SỐ/SỰ KIỆN |

Slot 19/11 17:00 để trống (T4 cần "rải thêm" thì lấy; xem mục "cần kiểm" 8). Tỉ lệ 60/40: 3 bài số/sự kiện có ngày, 2 bài thử (cơ chế, không ngày). Mỗi cặp kề nhau khác kiểu cảnh: S2 `MDGMGT`, S4 `MGMDT`, S3 `MGDMGT`, S5 `MGMGGDT`, S1 `MGMGD` (M clip, D số liệu, G sơ đồ, T chữ). Không bài nào dùng cảnh `table` (không phải bảng tra).

## 2. Từng bài

Quy ước: câu mở ≤ 9 chữ; câu chốt quay lại ý mở, không câu hỏi cuối, không mời xem Long trong lời đọc (mô tả có "Bản đầy đủ: https://youtu.be/Mt5hYcQxH50" như các Short Watson trước). Lời đọc có "theo lời kể" khi là chuyện kể.

### S2 · `mim-watson-bon-nam-ferrucci` — mở bài mẫu
- **Câu mở (9 chữ):** "Bốn năm trước trận đấu, Watson chơi rất tệ."
- **Insight duy nhất:** Watson không thắng nhờ một thuật toán thần kỳ mà nhờ hàng trăm phương pháp nhỏ ghép lại.
- **Số + nguồn:** khoảng 2007 giao nhóm Ferrucci; 2011 trận đấu; **4 năm = 2011 − 2007 (kênh tự tính)**; "hàng trăm phương pháp", bản đầu "trả lời đúng một phần nhỏ, chậm không thể thi đấu": `data/long/mim-watson-jeopardy/script.md` CH05 (nguồn gốc: Wikipedia *IBM Watson*).
- **Câu chốt:** "Từ một cỗ máy chơi tệ, thành người thắng cuộc, bằng hàng trăm mảnh ghép nhỏ."
- **Không trùng:** `mim-watson-90-may-chu` nói phần cứng (90 máy, 2.880 lõi, 200 triệu trang) và tên Thomas Watson; bài này nói phần mềm/đội ngũ, không dùng số phần cứng.

### S4 · `mim-watson-khong-nghe-thay` — THỬ
- **Câu mở (9 chữ):** "Watson lặp lại đáp án sai của đối thủ."
- **Insight:** cỗ máy thắng cuộc thi tri thức nhưng không có tai: nó nhận gợi ý bằng chữ, không nghe được người khác nói gì.
- **Số + nguồn:** không có số lớn; sự kiện (năm 2011, nhận gợi ý dạng chữ, đáp án sai bị lặp lại vì không nghe): `script.md` CH08 + ghi chú nguồn ("nhận gợi ý dạng chữ"). **Chi tiết "lặp lại đáp án sai" chưa có nguồn cụ thể trong ghi chú nguồn** (xem "cần kiểm" 5).
- **Câu chốt:** "Cỗ máy thắng cuộc thi tri thức ấy, nhưng không nghe được điều mà cả khán phòng vừa nghe."
- **Không trùng:** `mim-watson-tieng-chuong` nói luật bấm chuông và cánh tay cơ khí; bài này không nhắc chuông/cánh tay, chỉ nói "không nghe".

### S3 · `mim-jeopardy-1964-dap-an-truoc`
- **Câu mở (9 chữ):** "Năm 1964, một trò đố vui đảo ngược luật."
- **Insight:** luật đảo (đáp án đọc trước, người chơi hỏi lại) cộng gợi ý chơi chữ, vòng vo khiến Jeopardy khó cho máy.
- **Số + nguồn:** 1964 (Jeopardy ra đời), "năm 2007" (máy khi ấy gần như không thể), ví dụ Paris: `script.md` CH02.
- **Câu chốt:** "Luật đã ngược, gợi ý lại vòng vo. Với một cỗ máy năm 2007, gần như là không thể."
- **Không trùng:** `mim-con-ngua-da-con-ngua-da` nói nghĩa mơ hồ trong tiếng Việt; bài này nói luật chơi + kiểu gợi ý, không nhắc con ngựa/ông già.

### S5 · `mim-watson-hang-tram-dap-an` — THỬ
- **Câu mở (8 chữ):** "Watson không hiểu câu hỏi như bạn hiểu."
- **Insight:** với Watson, "hiểu" nghĩa là tạo hàng trăm đáp án rồi chấm điểm từng cái bằng bằng chứng.
- **Số + nguồn:** không có số; ba bước (mổ xẻ gợi ý, gom đáp án, tìm bằng chứng, gộp một điểm): `script.md` CH06. Lời đọc đã bỏ "hai trăm triệu trang" để không lặp bài 90 máy chủ.
- **Câu chốt:** "Với Watson, hiểu một câu hỏi nghĩa là chấm điểm hàng trăm câu trả lời." (DIỄN Ý của CH06, dòng cuối của chương)
- **Không trùng:** `mim-watson-nguong-50` nói ngưỡng 50% và ba thanh trên màn hình (độ tự tin → bấm hay im). Bài này **không nhắc ngưỡng, thanh độ tự tin, chuyện im lặng**; dừng ở bước chấm điểm.

### S1 · `mim-watson-nha-hang-2004`
- **Câu mở (9 chữ):** "Năm 2004, cả nhà hàng im bặt nhìn tivi."
- **Insight:** IBM tìm thử thách mới sau cờ vua vì cờ gói trong 64 ô còn ngôn ngữ thì không.
- **Số + nguồn:** 2004, 1997 (Deep Blue thắng), 64 ô: `script.md` CH01; **7 năm = 2011 − 2004 (kênh tự tính)**. Chuyện bữa tối ghi **"theo lời kể được báo chí ghi lại"** (đúng như ghi chú "Trung thực" đầu script).
- **Câu chốt:** "Một khoảnh khắc im lặng trong nhà hàng, theo lời kể, đã mở đầu cho nó."
- **Không trùng:** `mim-jennings-74-van` nói đường đời Jennings (kỷ lục 2004, thua 2011, thành người dẫn); bài này nói nguồn gốc ý tưởng Watson, chỉ nhắc Jennings như người đang được xem. `mim-deep-blue-*` không nhắc nhà hàng hay 64 ô.

## 3. Bảng đối chiếu trùng

### 3a. Short MIM hiện có (state.sqlite, kind='short', channel='MIM': 160 bài; truy vấn chỉ đọc 20/10) + `data/stier/specs/mim-*.json`

12 Short đã có về Watson/Jeopardy (đã hẹn 06–12/11, trước Long 19/11):

| Slug có sẵn | Góc | Bài T5 gần nhất | Vì sao khác |
|---|---|---|---|
| mim-watson-toronto | Toronto, cược 947 đô, lý giải của Ferrucci | S4, S5 | không nhắc Toronto/947 |
| mim-watson-nguong-50 | ngưỡng 50%, ba thanh độ tự tin | S5 | S5 dừng ở chấm điểm, không ngưỡng |
| mim-watson-90-may-chu | 90 máy chủ, 2.880 lõi, 200 triệu trang, tên Thomas Watson | S2, S5 | S2 là đội + phương pháp; S5 bỏ 200 triệu |
| mim-jennings-74-van | 74 ván, "ông chủ máy tính", TED, thành người dẫn | S1 | S1 là nguồn gốc ý tưởng IBM |
| mim-watson-77-nghin-do | 77.147 / 24.000 / 21.600, gấp 3 lần, 1 triệu từ thiện, 14 năm | S2 | không dùng điểm số |
| mim-rush-holt-thang-watson | trận Washington 28/02/2011 | không | — |
| mim-watson-62-trieu-do | 62 triệu, kiểm toán 2017 | không | — |
| mim-watson-ca-benh-gia-dinh | ca bệnh giả định, STAT 2018 | không | — |
| mim-project-debater-79-62 | tranh biện 79% → 62% | không | — |
| mim-watson-health-ban-2022 | bán Watson Health | không | — |
| mim-watson-tieng-chuong | luật bấm chuông, cánh tay cơ khí | S4 | S4 không nhắc chuông |
| mim-con-ngua-da-con-ngua-da | nghĩa mơ hồ tiếng Việt | S3 | S3 nói luật Jeopardy |

Từ khoá đã quét thêm trong 160 Short MIM: nhà hàng, Ferrucci, bốn năm, 1964 (chỉ trúng `mim-1964-may-tinh-that-nghiep`, bản ghi nhớ 03/1964, **khác chủ đề**), "không nghe", Rutter, Blue Jays, Final Jeopardy: không bài nào cùng góc với S1–S5. Chưa dùng ở Short nào: chuyện nhà hàng 2004, 4 năm/hàng trăm phương pháp, luật "đáp bằng câu hỏi" + 1964, Watson không nghe, quy trình "tạo đáp án rồi chấm điểm".

### 3b. Các ticket T4–T9
Đến 20/10 chỉ có file ticket (`T4`…`T9`), **chưa có `T<n>-ke-hoach.md` nào**, nên đối chiếu theo đề bài chủ đề: T4 GPU, T6 chat riêng tư, T7 poker, T8 nhận diện khuôn mặt, T9 máy chơi game: không có Watson/Jeopardy; các góc "AI tự tin khi sai / không dám nói không biết" (CH19 của Long) **đã bị tôi loại** vì dễ đụng nhóm AI bịa (`mim-ai-bia`, `mim-17-lan-toi-khong-biet`) và T6. **Phải đối chiếu lại khi các ticket kia nộp kế hoạch**, nhất là T7 (poker, Deep Blue/Libratus cùng series Người–Máy có thể cũng nhắc 1997).

## 4. Tự kiểm spec (không có `--lint-only`)

`motion/stier/build.py` **không có cờ `--lint-only`** (chỉ `--draft`, `--no-render`; `build()` luôn gọi TTS và tải ảnh, nên không chạy ở pha 1). Tôi tự kiểm bằng script riêng (copy luật từ `build.py`), kết quả 5/5 đạt:
- 55–135 từ (96–108 từ); `rules: 2` nên câu cuối không kết bằng "?"; câu mở ≤ 9 chữ.
- Mọi mốc neo `[câu, "chữ"]` khớp nguyên một chữ trong câu (cách `build.py` so: bỏ dấu câu, không phân biệt hoa/thường).
- Luật mix 12/10 (`mix_lint`, ước lượng thời lượng ~0,31 s/chữ): có đủ M, D, G; cảnh thuần chữ ≤ 31% (luật ≤ 35%); không kiểu nào > 60%; không 3 cảnh liền cùng kiểu; không cảnh > 11 s.
- Dòng phụ ≤ 52 ký tự; không `counter` hiện năm; không dấu "~"; counter chỉ dùng cho "4 NĂM" và "1 ĐIỂM".
- **Chưa kiểm được:** thời lượng thật (TTS Thanh Bình), layout/contrast khi render, chữ đọc `say`. Cần `build.py <slug> --draft`… nhưng theo luật "không dựng nháp", sẽ kiểm trên bản cuối khi pha 2 dựng nối tiếp. Nên chạy `mix_lint` thật (import từ build.py) trước khi dựng.

## 5. Chỗ thiếu góc, góc dự phòng

- **Không thiếu số bài, nhưng mỏng:** Watson đã bị khai thác kỹ (12 Short). Ngoài 5 bài trên, chỉ còn **1 dự phòng**: **S6** "Ghi hình tháng Một, phát tối 14–16/02/2011" (khi khán giả bật cười vì Toronto, trận đã ghi xong từ tháng Một; script CH08; dễ đụng bài Toronto nên chưa dùng) và hai ý yếu hơn (Rutter là người kiếm nhiều tiền thưởng nhất lịch sử chương trình tới lúc đó; Watson dẫn xa thì thận trọng/bị bám đuổi thì liều: gần như trùng `mim-watson-nguong-50`). **Không nên làm thêm quá 6 bài từ Long này.**
- Các chương bị loại (đã có Short hoặc thuộc ticket khác): CH00/09 Toronto, CH04 chuông, CH05 phần cứng, CH07 ngưỡng, CH10–11 Jennings, CH12 Holt, CH13–15 y tế, CH17 Debater, CH18 bán, CH19 chatbot không dám nói "không biết".

## 6. Cần kiểm trước khi dựng (pha 2)

1. **Thư mục `data/long/mim-watson-jeopardy/` không có `factcheck.md`** (chỉ `script.md` có phần "Ghi chú nguồn"). Ticket yêu cầu lấy số từ script đã kiểm; thực tế chỉ có ghi chú nguồn trong script. Các số tôi dùng đều nằm trong script, nhưng chưa có file kiểm riêng.
2. **S1:** chuyện nhà hàng 2004 là lời kể báo chí, script không ghi URL/tên báo. Tìm nguồn có URL (bài báo 2010–2011 về Watson) và ghi vào `sources`; nếu không tìm được thì giữ nguyên câu "theo lời kể" hoặc bỏ bài.
3. **S2:** "khoảng năm 2007", "bản đầu trả lời đúng một phần nhỏ, chậm không thể thi đấu", "hàng trăm phương pháp": đối chiếu lại Wikipedia *IBM Watson* (mục lịch sử/DeepQA) và/hoặc bài của Ferrucci. Spec ghi "khoảng". Không dùng con số cụ thể (không ghi "hai giờ một câu" hay tỉ lệ đúng vì script không có).
4. **S3:** ngày ra đời 1964 lấy từ script CH02; đối chiếu Wikipedia *Jeopardy!* (đã thêm vào `sources`). Câu "máy năm 2007 gần như không thể" là nhận định của script (DIỄN Ý), đừng ghi như dữ kiện.
5. **S4 (rủi ro cao nhất):** script CH08 nói "có lần nó đưa ra đúng một đáp án sai mà người chơi trước vừa nói, vì nó không nghe", **không có ngày, chủ đề, người chơi, nguồn**. Spec cố ý không nêu tên/ngày. Phải tìm nguồn 2011 (lời Ferrucci/IBM về việc Watson không nghe) trước khi dựng; **không tìm được thì bỏ S4, thay bằng S6**.
6. **S5:** mô tả theo script (DIỄN Ý từ tài liệu hệ thống); kiểm "hàng trăm đáp án" theo tài liệu IBM/Wikipedia.
7. **Clip:** tôi dùng lại ID Pexels đã dùng cho các Short Watson trước (`7005884`, `6962281`, `4841217`, `8567113`) vì đã qua một lần chọn; **bắt buộc chạy `motion/long/clip_sheet.py` trước khi dựng** (không logo/ticker/tên công ty) và nên **đổi sang ID chưa dùng** để 12 + 5 Short Watson không lặp cảnh nền. Các cảnh clip mang nhãn "VIDEO MINH HOẠ" khi ở dạng cửa sổ.
8. **Slot:** 17–19/11 hiện trống, nhưng T4 ("rải thêm" sau 16/11) và T6 (20–23/11) có thể muốn dùng các slot kề; đối chiếu `shorts_grid.py` ở cổng giữa hai pha.
9. **Bài mẫu:** theo chuẩn v3, làm S2 trước cho chủ kênh duyệt; các bài sau chỉ dựng nối tiếp khi S2 đạt (một tiến trình dựng, khoá `output/.render.who`, qua `scripts/run_chain.py`).
10. **Mô tả:** mỗi spec đã có dòng "Bản đầy đủ: https://youtu.be/Mt5hYcQxH50 (công khai từ 20:00 ngày 19/11)" như các Short Watson cũ; Long đã ở trạng thái `published` (riêng tư + hẹn giờ).

## 7. File đã tạo

- `docs/pm/tickets/2026-10-20-mim-nov/T5-ke-hoach.md` (file này)
- `docs/pm/tickets/2026-10-20-mim-nov/specs-T5/mim-watson-bon-nam-ferrucci.json`
- `docs/pm/tickets/2026-10-20-mim-nov/specs-T5/mim-watson-khong-nghe-thay.json`
- `docs/pm/tickets/2026-10-20-mim-nov/specs-T5/mim-jeopardy-1964-dap-an-truoc.json`
- `docs/pm/tickets/2026-10-20-mim-nov/specs-T5/mim-watson-hang-tram-dap-an.json`
- `docs/pm/tickets/2026-10-20-mim-nov/specs-T5/mim-watson-nha-hang-2004.json`
