# Nghiên cứu video dài MIM #18 — "Mã 1202, máy tính dẫn đường Apollo 11" — 20/10/2026

**Phạm vi:** hồ sơ dữ kiện cho Long 9–12 phút (16:9, theme "lab", giọng Thanh Bình, lời trích Ngọc Huyền), slug `mim-apollo-1202`, **hẹn 10/12/2026 20:00 VN** (ticket T3, chủ đề chọn ở `docs/pm/tickets/2026-10-20-mim-nov/T1-ket-qua.md` §4.2). Pha 1: chỉ viết file; chưa dựng, chưa đăng, chưa động tới `state.sqlite`.

**Đầu ra:** `data/long/mim-apollo-1202/{script.md, factcheck.md, ch00..ch06.json, gen_scenes.py, spec.json}` + file này.

**Nhãn:** **[bằng chứng]** = đã tải và đọc tận tài liệu gốc hôm nay · **[MỘT NGUỒN]** = một tài liệu duy nhất · **[CHƯA KIỂM]** = chưa đọc được, không dùng trong lời đọc.

## 1. Kết quả với các điểm yếu T1 nêu

| Điểm yếu (T1 §6.3) | Kết quả |
|---|---|
| Thiếu giờ GET từng báo động | **Giải quyết** [bằng chứng]. NASA SP-238 bảng 5-I (tr. 33): 1202 lúc 102:38:22 · 1202 lúc 102:39:02 · 1201 lúc 102:42:18 · 1202 lúc 102:42:43 · 1202 lúc 102:42:58; động cơ mở 102:33:05, chạm đất 102:45:40. Đối chiếu độc lập bằng bản ghi nhớ Grumman 31/07/1969 (4 lần 1202 + 1 lần 1201) và bản ghi không-đối-đất. hai PDF T1 chưa mở (A5 = SP-238 và A7 = bản ghi không-đối-đất) đã tải và đọc thật |
| Vai Garman/Kranz/Laning chưa có nguồn sơ cấp | **Một phần**. Kranz: [bằng chứng] PAO 102:12 (nhắc mọi người ngồi xuống, "Good luck to all of you"). Bales và Garman: chỉ một báo cáo NASA (Tomayko CR-182505 tr. 47) [MỘT NGUỒN]; tên Garman không có trong bản ghi sơ cấp, nên lời đọc ghi "Báo cáo lịch sử của NASA ghi rằng". Laning: chỉ qua danh mục tham khảo của bài Hamilton–Zeldin 1975 (bộ lập lịch), không nêu tên đầy đủ. Garman tự viết bài NTRS 19910030341 nhưng **không tải được PDF** (hồ sơ có, bản đầy đủ không công khai) |
| Margaret Hamilton chỉ có nguồn thứ cấp | **Một phần, và cố ý hẹp**. Có một nguồn **sơ cấp do chính bà là đồng tác giả**: AIAA 75-593 (1975), NTRS 19750042668 [bằng chứng]. Lời đọc chỉ nêu những gì bài báo ghi: phần mềm hệ thống Apollo gồm các mô-đun không đồng bộ (bộ lập lịch, màn hình, khởi động lại), tên Hamilton gắn với mô-đun màn hình, và nhận định "nếu không như vậy, ít nhất một chuyến bay đã thành thảm hoạ" (bài không nói chuyến nào). **Không** nêu Huân chương Tự do, ảnh chồng giấy, hay công lao riêng trong đêm 20/07 |
| "Corrected transcript" có vấn đề bản quyền | **Tránh được**: chỉ dùng bản ghi thô của NASA (`as11-tec.pdf`, `as11-pao.pdf` ở trang Mission Transcripts) |

## 2. Thêm so với T1: bản ghi nhớ Grumman đổi hẳn chương 3–4

T1 liệt kê memo Grumman LAV-500-940 là A4 nhưng mới "có đọc đoạn 1202". Đọc toàn văn hôm nay cho ba điều T1 chưa có, cả ba đã vào script:

1. **Vì sao máy hết "phòng":** Executive có **8 core set và 5 vùng VAC** (không phải "7 core set" như hồi ký Adler/ALSJ). Việc thứ chín xin phòng → 1202; việc cần VAC khi hết 5 → 1201.
2. **Ai kích hoạt:** hai báo động đầu đến **12 giây sau mỗi lần phi hành đoàn gọi màn hình theo dõi N68** (lệnh V16N68). Lần thứ ba họ chỉ xem ~10 giây, không báo động. Aldrin nói trên sóng: "it appears to come up when we have a 1668 up" — ông nhìn đúng. Người phụ trách dẫn đường ở Houston (GUIDO) nhận ra lệnh theo dõi là gánh nặng đáng kể và Houston nhận việc theo dõi độ cao (`"We'll monitor your DELTA-H"`).
3. **Con số "10%":** MIT/IL thường thử phần mềm với 10% thời gian máy dự phòng cho xung bất ngờ (TLOSS); radar gửi 15%. P63 không chịu nổi khi có thêm lệnh theo dõi, P64 sát giới hạn. Ba báo động cuối (P64) không kèm thao tác nào của phi hành đoàn.

Điều này đổi trọng tâm video từ "câu chuyện anh hùng một người" sang "máy tự đứng dậy + quy tắc viết trước + người hiểu máy", đúng với yêu cầu chỉ dùng nguồn sơ cấp.

## 3. Cấu trúc và vòng giữ chân

- **Cold open:** đèn báo thứ nhất, 5 phút 17 giây sau khi động cơ hạ cánh mở máy; Houston trả lời trong chưa đầy một phút.
- **Lộ trình dạng "nhật ký hai cột: MÁY | NGƯỜI"** (CH00 hứa; CH03 điền cột NGƯỜI; CH04 điền cột MÁY; CH05 bảng 5 lần; CH06 dòng cuối). **Khác 17 Long MIM trước** (ba câu hỏi, chặng đường, lời thách, cảnh hẹn trước, nghịch lý, câu hỏi duy nhất, bản đồ bằng hình, giải phẫu một vật, đồng hồ đếm ngược, ba vòng thi, phiên toà, bảng tỉ số, ba thanh độ tự tin, ba lá bài úp, "năm điều cờ vua không có", theo chân một tấm ảnh). **Không dùng** "trả lời ba câu hỏi" (cổng `ROADMAP_CLICHE` qua). T1 gợi ý "đồng hồ hạ cánh" nhưng `mim-flappy-bird` đã dùng "đồng hồ đếm ngược", nên đổi.
- **Vòng mở:** "dựa vào đâu mà người quyết định tiếp tục?" (mở CH00, trả lời CH03 và CH04). **Re-hook ~40%:** "90% + 15% > 100%" (CH04). **Cảnh mạnh ~75%:** đồng hồ nhiên liệu và "Eagle đã hạ cánh" (CH05).
- 7 chương, 169 câu. Chương: CH00 đèn báo thứ nhất · CH01 chiếc máy đặt hàng khi chưa có bản vẽ · CH02 cỗ máy không bao giờ làm một việc · CH03 cuốn nhật ký thứ hai (Houston) · CH04 thủ phạm là một cái radar · CH05 ba nghìn feet và đồng hồ nhiên liệu · CH06 dòng cuối của hai cuốn nhật ký.

## 4. Độ dài (đo theo chữ)

- **Tổng 2.218 chữ** (đếm âm tiết/chữ như `script_lines.py`; không tính `‖`, nhãn, ký hiệu). Theo chương: 203 · 329 · 337 · 361 · 398 · 292 · 298.
- **Đo thật tốc độ giọng:** `output/long/mim-qwerty/ch00..ch08/timing.json` (cùng giọng Thanh Bình, 1.776 chữ) cho tổng 8,55 phút → **208 chữ/phút** (cả chương, đã có khoảng nghỉ của TTS). Áp 208 chữ/phút: **≈ 10,7 phút**; `script_lines.py` đang dùng 200 chữ/phút: ≈ 11,1 phút; cộng thẻ chương và endcard 20 giây thì ≈ 11–11,5 phút. Nằm trong 9–12, không dưới 8.
- **Lệch với ticket:** ticket ghi "≈ 150 từ/phút giọng hiện dùng". Con số đo thật cao hơn nhiều (208). Nếu áp đúng 150 chữ/phút thì 2.218 chữ = 14,8 phút (vượt 12). Tôi chọn đo thật vì mục tiêu là độ dài video thật; nếu chủ kênh muốn khớp 150 chữ/phút thì phải cắt xuống ≤ 1.800 chữ (≈ 8,7 phút ở tốc độ thật, sát ngưỡng 9). **Cần Claude chốt chuẩn đo.**
- Không độn: mỗi chương có dữ kiện kiểm chứng (66 dòng `factcheck.md`); tư liệu đủ chiều sâu, không phải thêm chương.

## 5. Nguồn đã mở thật (20/10/2026)

| ID | Nguồn | Đã đọc | Dùng cho |
|---|---|---|---|
| SP-238 | NASA, *Apollo 11 Mission Report* (NTRS 19710015566, PDF 12,5 MB) | Có: §5 (bảng 5-I, hạ cánh), §9 (máy tính, nhiên liệu), §13 (quy tắc, checklist), §16 (cơ chế báo động) | Giờ GET, cơ chế radar, 15%, quy tắc "tiếp tục", sửa đổi sau chuyến bay |
| TEC | NASA, bản ghi không-đối-đất kỹ thuật Apollo 11 (`as11-tec.pdf`, 16 MB) | Có: trang 312–317 | Mọi lời thoại trích dịch, giờ 60/30 giây |
| PAO | NASA, bản tin PAO Apollo 11 (`as11-pao.pdf`, 19 MB) | Có: 102:12, 102:38–103:03 | Kranz, "Altitude 40,000", lời từ Eagle sau hạ cánh |
| GRU | Grumman LAV-500-940, 31/07/1969 (ibiblio, bản quét) | Có: toàn văn | 8 phòng/5 VAC, 12 giây, 10%/15%, P63/P64, Luminary IB |
| TOM | Tomayko CR-182505 ch. 2 (nasa.gov) | Có: `Ch2-2`..`Ch2-7` | Hợp đồng 1961, phần cứng, restart, Bales/Garman |
| HZ | Hamilton & Zeldin, AIAA 75-593 (NTRS 19750042668) | Có: toàn bài | Mô-đun bất đồng bộ; Laning/Hamilton qua tham khảo |
| A12, A14 | Apollo 12 MSC-01855 (NTRS 19760072997); Apollo 14 5-day (NTRS 19710027929) | Có: phần dẫn đường | Không báo động ở Apollo 12; vá công tắc huỷ ở Apollo 14 |
| ADL | Adler, "Program Alarms", ALSJ (© Peter Adler) | Có | Chỉ hai chi tiết, diễn ý |

Đã loại: NTRS 19910030341 (Garman), 19730039746 (Eyles), 19690043001 (Hall): hồ sơ có nhưng PDF không công khai (HTTP 404 ở đường tải).

## 6. Mâu thuẫn giữa nguồn và cách xử lý

| Điểm | Nguồn A | Nguồn B | Xử lý |
|---|---|---|---|
| Số core set | GRU, TOM: 8 | ADL (hồi ký): 7 | Dùng 8, ghi trong factcheck |
| Số VAC | GRU, ADL, TOM: 5 | — | 5 |
| Ô nhớ VAC | TOM: 43; ADL: 44 | — | Không dùng |
| Đơn vị 1 chu kỳ nhớ | SP-238, GRU: 11,7 / 11,72 **micro**giây | TOM `Ch2-4/5`: "11.7 **milli**seconds" (sai đơn vị) | Dùng micro giây |
| Khoảng 1202 thứ 4 → 5 | SP-238: 15 s | GRU: 16 s | "chừng mười lăm giây" |
| Chữ cuối của GO ở 1201 | TEC: "We're GO. Same type. We're GO." | PAO: "We're go. Hang tight. We're go." | Trích TEC |
| "Cột go/no-go = 20 giây" | hình SP-238 tr. 118 (OCR) | — | Không dùng |

## 7. Hình (đã đọc Commons API 20/10/2026, đọc lại ở pha 2 trước khi tải)

MIM không nhận BY-SA (`no_sa`). `spec.json` → `imgs`: `launch` (Apollo 11 Launch GPN-2000-000630, PD), `agc` (Apollo Guidance Computer (AGC), **CC BY 2.0 Steve Jurvetson**, cần credit), `lm` (AS11-44-6584, PD), `lm2` (AS11-44-6643, PD), `mcc` (Inflight Apollo XI MCC S69-40302, PD), `mcctraj` (Apollo 11 Mission Control Center - landing trajectory, PD), `site` (LRO Apollo 11 landing site, PD). **Loại** ảnh DSKY, ảnh lõi từ của Reinhold (BY-SA 4.0) và ảnh DSKY của Tamorlan (BY-SA 3.0). Không có clip Pexels; không có cảnh DSKY riêng (dùng bảng `ledger`). Không dùng ảnh người (Hamilton, Bales, Garman, Kranz) — chưa đối chiếu người chụp từng ảnh.

## 8. Chỗ cần kiểm (xem thêm `factcheck.md` mục cuối)

1. Ảnh trang: bảng 5-I, chữ "1668" (TEC tr. 312), số chú thích HZ [17]–[19]. Đã ghép bằng toạ độ chữ, chưa nhìn ảnh.
2. Ý nghĩa mốc "60 seconds / 30 seconds" (lời đọc chỉ nói "mốc của đồng hồ nhiên liệu").
3. Giờ từng câu thoại trong TEC chỉ đúng ±chục giây (OCR).
4. Chuẩn đo độ dài: 150 hay 208 chữ/phút (mục 4).
5. Tiêu đề chưa tối ưu từ khoá: chưa có Studio Research (`data/demand/MIM-studio.md`).
6. Cảnh báo `studio_lint.py`: 5 chương ít câu ngắn (cảnh báo, không phải lỗi cứng); 0 lỗi; có thể thêm vài câu ngắn khi duyệt.

## 9. Kiểm tra đã chạy

- `python motion/long/script_lines.py mim-apollo-1202` → 0 lỗi integrity, không `ROADMAP_CLICHE`; ghi `lines` vào `ch00..ch06.json`.
- `python data/long/mim-apollo-1202/gen_scenes.py` → ghi `spec.json` + scenes; tự kiểm mọi neo `[dòng, "từ"]` khớp lời đọc.
- `python motion/long/studio_lint.py mim-apollo-1202 --strict` → 0 lỗi, 5 cảnh báo.
- **Chưa chạy:** `build_long.py` (TTS, html, render) và `variety.py audit` — thuộc pha 2.

## 10. Chủ đề dự phòng

Không cần: tư liệu dư. (Nếu chuẩn đo bị buộc về 150 chữ/phút và phải cắt: bỏ CH01 phần vi mạch và CH06 phần Apollo 14, vẫn giữ trục "hai cuốn nhật ký".) Dự phòng cấp hai vẫn là GPS theo T1 §5.
