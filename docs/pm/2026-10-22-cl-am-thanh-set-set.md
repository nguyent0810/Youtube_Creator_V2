# CL "Into the Killer's Mind": chẩn đoán tiếng "sẹt sẹt" (22/10/2026)

Bình luận khán giả: "nội dung rất hay, âm thanh sẹt sẹt rất khó chịu mong kênh cải thiện".
Phạm vi: chỉ chẩn đoán và đề xuất. Không sửa code dùng chung, không dựng lại video, không upload, không đụng state.sqlite.

## 0. Giới hạn dữ liệu (đọc trước)

- Máy này **không có** `output/long/{golden,shanghai,yakuza,mafia,ripper,kowloon}/`: không có final.mp4, voice.wav, sfx.wav, mix.wav hay tts cache của Long CL. Long CL được dựng trên máy sản xuất (báo cáo 3 kênh cùng ngày cũng ghi máy này không có credential của CL). Trong `output/stier/` chỉ còn **một** Short CL là `alcatraz` (draft_av.mp4, voice.wav, sfx.wav). Nhạc nền CL (crypto, dark_times, long_note_four…) cũng không có trong `output/music/`.
- Vì vậy tôi lấy bằng chứng theo ba cách:
  1. **Giọng dẫn CL "Anh Khôi"**: đo voice.wav thô của Short `alcatraz` (Anh Khôi), đối chiếu với 4–5 Short của mỗi giọng khác. Trong đó có 11 Short giọng "Thiện Minh", mà code ghi là cùng embedding với Anh Khôi trong vieneu 3.8.3 (`build_long.py` dòng 170).
  2. **Tiếng động Long CL**: dựng lại `sfx.wav` của cả 6 Long CL bằng chính `sfx_long.build()` + `build_long.plan()`. Mốc thời gian là ước lượng (0,27 s/âm tiết + nghỉ theo `line_pause`), nên mức và hình phổ đúng, còn vị trí thì lệch vài giây. Bản dựng chỉ nằm trong scratchpad (`recon_sfx.py`), không ghi vào output/.
  3. **Đối chứng MIM**: `output/long/mim-apollo-1202` có đủ stem thật (voice/sfx/mix/mixpad/final).
- Chưa nghe được, và chưa đo được final của Long CL đã đăng. Mục 5 có lệnh đo để chạy trên máy sản xuất.

## 1. Số đo

### 1a. Mức, đỉnh, clipping (không phải nguyên nhân)

| File | SR | Peak | Mẫu \|x\|≥0,999 | I (LUFS) | TP | LRA |
|---|---|---|---|---|---|---|
| MIM apollo final.mp4 | 48k | −1,15 dBFS (2 mẫu) | 0 | −14,1 | −1,1 dBTP | 2,7 |
| CL Short alcatraz draft_av.mp4 | 48k | −1,33 dBFS | 0 | −14,3 | −1,3 dBTP | 1,4 |
| CL alcatraz voice.wav (Anh Khôi thô) | 48k PCM16 | −0,49 | 0 | | | |
| CL alcatraz sfx.wav | 48k | −0,92 | 0 | | | |
| MIM apollo voice.wav ×7 chương | 48k | −0,6 … −3,0 | 0 | | | |
| MIM apollo mix.wav ×7 chương | 48k | −0,18 … −1,6 | 0 | | | |
| CL Mafia sfx.wav dựng lại ×16 chương | 48k | đến 0,0 | 4/16 chương có 4–18 mẫu (np.clip) | | | |

Kết luận 1a:
- loudnorm (I −14, TP −1,5) chạy đúng.
- Không có clip trong voice/mix.
- Cả chuỗi là 48 kHz: vieneu xuất 48k, `SAMPLE_RATE = 48_000`, sfx 48k. **Không có bước chuyển 24k→48k**, nên không có aliasing do đổi tần số lấy mẫu.
- `radio()` ×1,4 không làm clip: voice của MIM ch05 có 6 câu trích mà đỉnh vẫn −2,4 dBFS.
- sfx có clip lác đác vài mẫu ở cú boom/rumble chồng nhau. Lỗi có thật nhưng quá thưa để thành "sẹt sẹt".

### 1b. Độ "rè" của giọng: xung sắc ở dải > 5 kHz trong lúc nói (`pulse.py`, `set/voicem.py`)

Cách đo: lấy khung 20 ms có lời, lọc phần > 5 kHz, tính kurtosis (nhiễu Gauss = 0, xung càng nhọn càng cao) và % khung có crest > 6.

| Giọng (kênh) | kurtosis HF trung vị | kurtosis p90 | % khung crest>6 |
|---|---|---|---|
| **Anh Khôi, Short alcatraz (CL)** | **6,0** | **15,2** | **42 %** |
| **Thiện Minh** (= Anh Khôi, 5 Short) | **5,9** | **14,5** | **41 %** |
| Thanh Bình (MIM, 5 Short) | 3,6 | 8,5 | 18 % |
| Thanh Bình (MIM apollo Long) | 3,7 | 8,9 | 20 % |
| Thiền Tâm Đức | 3,6 | 12,1 | 23 % |
| Ngọc Huyền (CK/MIM trích) | 2,2 | 7,1 | 13 % |
| Quang Sơn (nam) | 1,5 | 4,6 | 2,4 % |
| Ngọc Trân / Đoan Trang / Mỹ Duyên / Ngọc Linh / Thục Đoan | 0,6–1,8 | 2,9–6,0 | 1,8–9,8 % |

Sau toàn bộ chuỗi, giọng vẫn giữ nguyên độ rè (giọng đã đi qua xử lý, đo trên final):

| | kurtosis HF | % crest>6 |
|---|---|---|
| Anh Khôi + VOICE_FX + loudnorm + AAC 192k (mô phỏng chuỗi Long CL) | 5,5 | 39,5 % |
| CL Short alcatraz (thành phẩm) | 3,7 | 31,8 % |
| MIM apollo final (5 phút) | 2,8 | 15,6 % |

Ảnh sóng (`set/hf_wave.png`):
- Anh Khôi: mỗi chu kỳ thanh môn (~8,8 ms, ~113 Hz) có **một xung HF nhọn biên độ ~0,04**, giữa hai xung gần như lặng. Đó là tiếng buzz/rè lặp theo cao độ giọng.
- Quang Sơn (cũng giọng nam): cùng dạng nhưng xung nhỏ hơn ~5 lần.
- Thanh Bình: xung dày, lẫn nhiễu, không tách rời.

Ảnh phổ (`cl_short_voice.png`, `set/ak_zoom.png` so với `mim_voice.png`): Anh Khôi có các vạch dọc băng rộng 4–15 kHz ở mọi âm tiết, phần trên 2 kHz ít hài âm rõ.

Mastering `VOICE_FX` hiện tại **làm nặng thêm**. Đo độ nổi của xung HF so với RMS giọng (trung vị):

| | độ nổi |
|---|---|
| Thô | −19,5 dB |
| Sau VOICE_FX | **−17,1 dB (tệ hơn 2,4 dB)** |

Hai nguyên nhân: EQ +2,5 dB ở 3,2 kHz (w=1,4, nên ăn rộng tới ~5 kHz) và compressor attack 5 ms + makeup ×2.

### 1c. Tiếng động tổng hợp kiểu "nhiễu" của theme noir (`sfx_long.NoirMix`)

Đo trên sfx dựng lại, đã nhân 0,42 như `mix_chapter` (trước sidechain):

| Đoạn | Peak | RMS | RMS 4–12k | Peak 4–12k |
|---|---|---|---|---|
| Tĩnh điện radio (`static`), Mafia ch04 | −16,4 | −40,1 | −45,8 | **−19,0** |
| Máy chiếu (`projector`, cảnh `film`), Mafia ch01 | −22,4 | −43,7 | −53,0 | −31,1 |
| Kim vẽ (`needle`, cảnh `sketch`), Thượng Hải ch02 | −28,7 | −43,9 | −45,2 | −28,7 |
| *(so sánh)* giọng Anh Khôi: RMS −19,3; RMS 4–12k | | | −41,9 | |
| MIM apollo static (cùng code) | −14,1 | −40,8 | −46,4 | −20,3 |

Ảnh phổ (`set/sp_radio.png`, `sp_film.png`, `sp_sketch.png`):
- `static()` cộng các cụm nhiễu 300 mẫu (6 ms) **không có fade**, 9 cụm/s. Mỗi cụm tạo một vạch dọc phủ kín 0–24 kHz, tức một tiếng "tạch" thật.
- `projector()`: 24 vạch/s phủ toàn dải.
- `needle()`: nhiễu 2,5–24 kHz, nhịp 6 Hz (sin²(2π·3t)). Nghe đúng kiểu "sẹt… sẹt… sẹt".
- Khi đọc câu trích, giọng bị lọc 300–3400 Hz nên dải trên 4 kHz **chỉ còn tiếng tĩnh điện**. Các xung −19 dBFS nổi hẳn lên.

Thời lượng các đoạn có tiếng nhiễu (từ cảnh dựng lại):

| Video | Dài | film | radio | sketch | khác | Tổng | % |
|---|---|---|---|---|---|---|---|
| Thượng Hải | 35,6 ph | 145 s | 0 | 52 s | 0 | 196 s | **9,2 %** |
| Mafia | 57,6 ph* | 93 s | 67 s | 0 | 22 s (lửa, địa chấn) | 181 s | 5,3 % |
| Tam Giác Vàng | 28,8 ph | 38 s | 17 s | 29 s | 0 | 85 s | 4,9 % |
| Cửu Long | 30,6 ph | 37 s | 16 s | 14 s | 0 | 66 s | 3,6 % |
| Ripper | 35,9 ph | 11 s | 20 s | 20 s | 0 | 51 s | 2,4 % |
| Yakuza | 34,5 ph | 0 | 0 | 0 | 0 | 0 | 0 % |
| MIM apollo | 11,9 ph | 0 | 33 s | 0 | 0 | 33 s | 4,6 % |

\* độ dài ước lượng.

### 1c-bis. sfx toàn video: dải 4–12 kHz và clip (sfx ×0,42, khung 100 ms)

Kiểm chứng cách dựng lại: MIM apollo bản dựng lại cho 9,0 s/phút, bản thật đo được 9,6 s/phút. Hai số khớp, nên dùng được cho Long CL.

| Video | Giây HF > −50 dBFS | Giây HF > −60 dBFS | s/phút (> −60) | Mẫu sfx clip (≥ 0,999) |
|---|---|---|---|---|
| Tam Giác Vàng | 262 | 392 | 13,6 | 20 |
| Cửu Long | 273 | 408 | 13,4 | 22 |
| Mafia | 525 | 786 | 13,6 | 32 |
| Ripper | 280 | 395 | 11,0 | **99** |
| Thượng Hải | 291 | 523 | **14,7** | 12 |
| Yakuza | 209 | 303 | 8,8 | 8 |
| MIM apollo (dựng lại) | 82 | 106 | 9,0 | 0 |
| MIM apollo (thật) | 81 | 105 | 9,6 | 0 |

So với MIM, Long CL theme noir có thời gian sfx dải cao nhiều hơn 15–55 % theo s/phút. Long CL cũng có 8–99 mẫu clip cứng trong sfx, còn MIM thì 0. Yakuza (không theme noir) gần bằng MIM. Bảng này củng cố nguyên nhân 2 (tiếng động noir), nhưng không đổi thứ hạng: giọng vẫn là yếu tố phủ 100 % thời lượng.

### 1d. Chỗ chuyển chương: có tiếng "tách"

Chương trước kết thúc bằng lặng tuyệt đối. Mẫu **đầu tiên** của chương sau lại đã ở mức to:

| Stem | Mẫu đầu tiên | Đỉnh 5 ms đầu |
|---|---|---|
| sfx dựng lại Mafia ch01–04 | −17,6 … −33 dBFS | −9 … −11 dBFS |
| MIM apollo ch01 sfx.wav (thật) | −11,4 | −7,0 |
| MIM apollo mixpad.wav ch02 (thật) | −13,1 | −9,3 |

Nguyên nhân: `sfx_long.build` gọi `M.put(T0 - 0.35, M.whoosh(0.8), 0.45)` cho thẻ chương với T0 = 0. `Mix.put` cắt phần âm (`sig[-i:]`) **không fade**, nên whoosh bắt đầu ở giữa đường bao, thành một bước nhảy. Mỗi Long CL dính 12–15 cú "tách" như vậy. Lỗi này có ở cả MIM.

## 2. Nguyên nhân gốc (xếp theo khả năng)

1. **Chính giọng dẫn "Anh Khôi" của vieneu: xung buzz HF theo từng chu kỳ cao độ.** Khả năng cao nhất, mức chắc chắn **trung bình–cao (~65 %)**.
   - Bằng chứng: chỉ số xung cao nhất trong 12 giọng (kurtosis 6 so với 0,6–3,7). Lặp đúng ở cả 11 Short "Thiện Minh". Còn nguyên sau mastering, loudnorm và AAC. Đây là **giọng duy nhất kênh CL dùng** (Long lẫn Short, 100 % thời lượng lời).
   - MIM (Thanh Bình) cùng pipeline mà không bị chê. Trong pipeline Long CL, đây là khác biệt lớn nhất và có mặt liên tục.
   - `VOICE_FX` (EQ +2,5 dB @3,2 kHz, attack 5 ms) làm xung nổi thêm 2,4 dB.
   - Chưa nghe nên chưa thể khẳng định 100 % đây là thứ khán giả gọi là "sẹt sẹt".
2. **Tiếng động noir được thiết kế là nhiễu** (`static`, `projector`, `needle`), dựng bằng cụm nhiễu không fade nên tạo vạch tạch phủ toàn dải. Mức chắc chắn **trung bình**: chắc chắn là tiếng "sẹt" theo đúng nghĩa đen, nhưng chỉ chiếm 2–9 % thời lượng mỗi video, và Yakuza không có. Thượng Hải nặng nhất (145 s máy chiếu).
3. **Tiếng tách đầu mỗi chương** (12–15 lần/video). Chắc chắn có, nhưng thưa, nên chỉ là yếu tố phụ.
4. Loại trừ (có số đo): clip/TP (không có, TP −1,1…−1,3 dBTP), aliasing 24k→48k (không có bước đổi SR), loudnorm (đúng −14 LUFS), clip trong voice.wav do radio ×1,4 (không xảy ra). Còn clip sfx vài mẫu: có, nhưng không đáng kể.

## 3. Đề xuất sửa ở gốc

Các điểm dưới đây chạm code dùng chung (CL + MIM + CK), nên cần duyệt trước khi sửa. Video đã đăng giữ nguyên, theo luật replace-uploaded.

### S1. Giọng CL: quyết định trước, rồi mới xử lý lọc
- **S1a (gốc, cần người dùng nghe và chọn):** dựng một đoạn 60 s cùng lời bằng 3 phương án rồi nghe trên điện thoại:
  - (i) Anh Khôi hiện tại;
  - (ii) Anh Khôi với `temperature` thấp hơn, qua `_engine.infer(..., temperature=…)` (stier đã có `spec["tts"]`; `build_long.tts_line` chưa nhận kwargs);
  - (iii) một giọng nam khác ít xung, ví dụ Quang Sơn (kurtosis 1,5; 2,4 % khung).

  Đổi giọng dẫn là đổi nhận diện kênh, nên người dùng phải quyết.
- **S1b (giảm nhẹ, cho dù giữ Anh Khôi):** trong `motion/long/build_long.py`, thêm chuỗi mastering riêng cho CL (khai trong `_channels()["CL"]["voice_fx"]`, không đổi `VOICE_FX` của MIM/CK):
  ```
  VOICE_FX_CL = ("highpass=f=70,equalizer=f=200:t=q:w=1:g=-2,highshelf=f=5000:g=-5,lowpass=f=9000:poles=2,"
                 "deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=15:release=150:makeup=2")
  ```
  Thay đổi: bỏ EQ +2,5 dB @3,2 kHz, thêm shelf −5 dB từ 5 kHz + low-pass 9 kHz, attack 5 → 15 ms.

  `mix_chapter()` dòng 910 dùng `CHAN.get("voice_fx", VOICE_FX)`.

  Kết quả đo trên alcatraz: độ nổi xung HF **−17,1 dB (hiện tại) → −22,2 dB**, giảm 5 dB. Kurtosis không đổi, vì bộ lọc chỉ hạ mức xung chứ không xoá được xung. Vì thế đây chỉ là giảm nhẹ, không thay được S1a.
- Short CL (`motion/stier/build.py` dòng 789) đang trộn giọng **thô**, không qua mastering nào. Nếu giữ Anh Khôi thì nên thêm cùng chuỗi lọc trước `pan=stereo` ở nhánh fc mặc định (theme không ghi / "case").

### S2. Tiếng động noir: bỏ cạnh vuông, hạ dải cao (`motion/long/sfx_long.py`)
- `static()` dòng 79–84:
  - nhân mỗi cụm 300 mẫu với `np.hanning(300)` thay vì cộng thẳng;
  - lọc cả tín hiệu `self.lowp(…, 4000)` sau khi cộng cụm (cho khớp băng thông radio 300–3400);
  - giảm số cụm 9/s xuống ~4/s và hạ biên độ cụm 0,5–1,6 xuống 0,2–0,6;
  - ở dòng 432, hạ gain 0,12 xuống 0,06.
- `projector()` dòng 86–95: tick 1100 Hz có nửa phần là nhiễu trắng. Lọc `self.lowp(c, 2500)` và hạ gain lặp 0,8 xuống 0,4 (`build` dòng 376 đang để 0,16).
- `needle()` dòng 97–99: đổi bp 2500–9000 thành 1500–5000 và hạ ×0,35 xuống ×0,2.
- `Mix.put` (`motion/stier/sfx.py` dòng 103–111): khi `i < 0` (tín hiệu bị cắt đầu), nhân 5 ms đầu với ramp 0→1. Cách này sửa luôn tiếng tách đầu chương cho cả 3 kênh (mục 1d). Hoặc trong `sfx_long.build` dòng 186, đặt whoosh của thẻ chương ở `max(0, T0 - 0.35)`.
- Lưới an toàn: thay `np.clip(M.bed * 0.5, -1, 1)` ở `sfx_long.py` dòng 439 bằng limiter mềm, ví dụ `np.tanh(M.bed * 0.5)`, để bỏ clip cứng ở cú boom chồng.
- Thêm tuỳ chọn: trong `mix_chapter` dòng 910, lọc nhánh sfx `[1:a]volume=0.42,lowpass=f=10000[s0]` để chặn mọi vạch HF trên 10 kHz.

### S3. Ranh giới chương (`build_long.do_final`, dòng 997–1001)
Thêm `afade=t=in:d=0.005,afade=t=out:st={vd-0.005}:d=0.005` vào bước tạo mixpad. Lưới an toàn này chặn mọi bước nhảy ở chỗ nối, kể cả khi S2 chưa làm.

### S4. Lint âm thanh (chặn tái phát, theo luật "không lặp lỗi")
Thêm `motion/long/audio_lint.py`, chạy sau `html` (mix.wav đã có) và trước `final`. Fail khi gặp một trong các điều sau:
- (a) mẫu đầu/cuối của mixpad > −60 dBFS;
- (b) sfx.wav có mẫu ≥ 0,999;
- (c) voice sau mastering có kurtosis HF trung vị > 4,5 (in cảnh báo kèm tên giọng);
- (d) final có TP > −1,0 dBTP hoặc I lệch ±1 LU khỏi −14.

## 4. Không làm trong việc này
Không sửa code, không dựng lại, không upload, không đụng state.sqlite. Các file đo nằm ở scratchpad phiên này (thư mục `set/`, gồm `voicem.py`, `pulse.py`, `recon_sfx.py`, ảnh phổ và sfx dựng lại).

## 5. Cách kiểm sau khi sửa

1. **Trên máy sản xuất**, đo final đã đăng của 3 Long mới nhất để xác nhận giả thuyết trên dữ liệu thật:
   ```
   ffmpeg -i output/long/<topic>/final.mp4 -vn -af "astats=measure_perchannel=none,ebur128=peak=true" -f null -
   python pulse.py output/long/<topic>/ch03/voice.wav output/long/<topic>/ch03/mix.wav
   ffmpeg -ss 600 -t 20 -i output/long/<topic>/final.mp4 -lavfi showspectrumpic=s=1200x500:scale=log out.png
   ```
   Kỳ vọng: TP ≈ −1 dBTP, 0 clip, kurtosis HF của voice ≈ 6.
2. **A/B nghe (người dùng):** cùng một chương ngắn có câu trích + cảnh film, dựng 2 bản (hiện tại / sau sửa), nghe bằng loa điện thoại và tai nghe. Đây là bước duy nhất xác nhận được đúng "sẹt sẹt".
3. **Số đo phải đạt:**

   | Chỉ số | Ngưỡng |
   |---|---|
   | Độ nổi xung HF giọng sau mastering (`pulse.py`) | ≤ −22 dB |
   | Kurtosis HF nếu đổi giọng | ≤ 3 |
   | Ảnh phổ đoạn radio/film | không còn vạch dọc > 8 kHz |
   | Mẫu đầu/cuối mỗi `mixpad.wav` | < −60 dBFS |
   | sfx.wav, mẫu ≥ 0,999 | 0 |
   | final | I −14 ±1 LUFS, TP ≤ −1,0 dBTP |
4. Đối chứng MIM sau khi sửa `Mix.put`/`do_final`: chạy lại `html` + `final` cho một Long MIM bất kỳ **trong scratchpad / bản nháp**, so stem trước và sau. Mẫu đầu chương phải im, các chỉ số khác giữ nguyên.
5. Theo dõi bình luận Long CL tiếp theo (chỉ số trong bảng việc của báo cáo 3 kênh: "không còn bình luận chê âm").

## Đã sửa 23/10 (phương án B: giữ giọng "Anh Khôi" + bộ lọc mới)

Chủ kênh đã nghe và chọn bản `fx_proposed`. Chưa dựng lại hay đăng lại video nào, lịch và state.sqlite giữ nguyên.

### Code đã sửa
- **S1b, bộ lọc giọng riêng cho CL.**
  - `motion/stier/themes.py` có thêm `VOICE_FX_CL`, đúng chuỗi của `fx_proposed`. Hằng này gắn vào theme `"case"` qua khoá `voice_fx`.
  - Short: `motion/stier/build.py` chèn `VOICE_FX_CL` vào nhánh giọng `[1:a]` chỉ khi theme có `voice_fx`. Theme mim/ck/bud không có khoá này nên giọng vẫn thô như cũ.
  - Long: `build_long._channels()["CL"]` có `voice_fx`. `mix_chapter` dùng `CHAN.get("voice_fx", VOICE_FX)`, nên MIM/CK vẫn dùng VOICE_FX cũ, còn `"master": false` vẫn tắt lọc.
- **S2, tiếng động.**
  - `motion/stier/sfx.py`:
    - `Mix.put` thêm fade 5 ms khi tiếng bị cắt đầu hoặc đuôi (dùng chung cho mọi kênh);
    - `Mix.write` thêm fade 5 ms ở hai mép file;
    - thêm hàm `soft_clip` (giữ nguyên dưới knee, nén tanh phía trên), thay cho `np.clip` khi cộng ambience (knee 0,9, nên mức cũ không đổi).
  - `motion/long/sfx_long.py`:
    - `static()`: cụm nhiễu nhân cửa sổ Hann, 4 cụm/s thay cho 9, biên độ 0,2–0,6, low-pass 4 kHz;
    - `projector()`: tick qua low-pass 2,5 kHz, gain ×0,4;
    - `needle()`: dải 1,5–5 kHz, gain ×0,2;
    - đầu ra dùng `soft_clip(…, 0.8, 0.98)` thay cho `np.clip`.
- **S3:** `build_long.do_final` thêm `afade` 5 ms vào/ra cho mỗi `mixpad.wav`.
- **S4, lint âm thanh.**
  - File mới `motion/long/audio_lint.py`, ngưỡng ghi trong code:
    - buzz đo trên giọng **đã qua chuỗi lọc của kênh**. Kurtosis HF > 4,5 là giọng kiểu buzz (cảnh báo). Nếu thêm độ nổi xung HF > −21,0 dB thì báo LỖI;
    - true peak > −1,0 dBTP;
    - mẫu đầu/cuối mixpad > −60 dBFS;
    - sfx có mẫu ≥ 0,999;
    - chỗ "tách", tức đang lặng (< −60 dBFS) mà một mẫu nhảy lên > −30 dBFS.
  - Kênh CL: lỗi thì xoá final rồi dừng (`SystemExit`). Kênh khác chỉ in WARNING. Nếu công cụ đo hỏng: CL chặn, kênh khác chỉ cảnh báo.
  - Gọi ở `do_final` (trước khi ghép, và TP sau khi ra final) và ở `stier/build.audio_gate` (ngay sau mux).
  - Đo trên thành phẩm thì sfx/nhạc lấn dải cao, nên độ nổi xung vô nghĩa (MIM final ra −15 dB, tệ hơn cả CL). Vì vậy lint đo trên giọng đã lọc.
- Test mới `tests/test_audio_lint.py` (5 test).

### Số đo trước/sau
Giọng Anh Khôi đã lọc, đo theo cách của `pulse.py`:

| | độ nổi xung HF | kurtosis | % crest>6 |
|---|---|---|---|
| alcatraz thô (Short cũ) | −19,5 dB | 6,0 | 42,2 % |
| alcatraz + VOICE_FX cũ (Long CL cũ) | −17,0 dB | 5,64 | 40,4 % |
| **alcatraz + VOICE_FX_CL** | **−22,2 dB** | 5,58 | 39,0 % |
| 4 Short Thiện Minh (= Anh Khôi) + VOICE_FX_CL | −21,8 … −23,3 dB | 4,8–6,3 | 35–40 % |
| (thô / VOICE_FX cũ của 4 Short đó) | −18,9…−20,6 / −16,5…−18,0 | | |

Short CL `alcatraz`, thành phẩm dựng lại (`--draft`; nhánh tiếng giống hệt final):

| | độ nổi HF | kurtosis | crest>6 | TP | LUFS | chỗ "tách" sfx | mép cuối sfx |
|---|---|---|---|---|---|---|---|
| trước | −17,8 dB | 3,69 | 31,7 % | −1,3 dBTP | −14,3 | 1 | −24,8 dBFS |
| sau | −20,2 dB | 3,46 | 30,7 % | −1,3 dBTP | −14,5 | 0 | lặng |

Long CL, sfx dựng lại bằng `recon_sfx.py` (mốc ước lượng):

| | mẫu clip | "tách" | mép chương lớn nhất |
|---|---|---|---|
| Mafia, 16 chương: trước | 32 | 18 | −11 dBFS |
| Mafia, 16 chương: sau | 0 | 10 | lặng |
| Ripper, 14 chương: trước | 99 | 18 | −12 dBFS |
| Ripper, 14 chương: sau | 0 | 9 | lặng |

- 9–10 chỗ "tách" còn lại nằm giữa chương. Đó là các tiếng chạm có attack gần 0 (gõ búa, tick…), chưa sửa. Lint chỉ cảnh báo loại này.
- Tiếng noir, đo trên một đoạn mẫu:
  - `static`: đỉnh 4–12 kHz giảm từ −20,7 xuống −40,8 dBFS;
  - `projector`: từ −36,6 xuống −59,9 dBFS;
  - `needle`: từ −30,6 xuống −40,7 dBFS.
- Cả ba tiếng nhỏ hơn 5–7 dB RMS.

MIM đối chứng: Short `mim-nvidia-quan-an-dem` dựng lại.
- Lint không chặn, không cảnh báo giọng: độ nổi −15,5 dB, kurtosis 3,69.
- Final cũ và bản dựng lại cùng −14,5 LUFS, TP −1,4 dBTP. Phổ 9 dải 60 Hz–20 kHz lệch ≤ 0,1 dB, tức giọng Thanh Bình không đổi.
- Long MIM apollo: lệnh mixpad mới cho mép = lặng. Trong phần nằm ngoài 10 ms ở hai mép, mẫu giống hệt bản cũ (sai khác tối đa 0,0). Các mixpad cũ (trước sửa) bị lint báo tách ở 6/7 chương, đúng như chẩn đoán.

### Test, bản nghe
- `pytest tests`: 576 qua. 13 lỗi có sẵn từ trước khi sửa (test_ck_stier bang-tra, test_claims, test_console, test_lines, test_pillars), không liên quan việc này.
- Bản nghe ở `output/chain_src/ab_giong_cl/`:
  - `sau_alcatraz_short_15s.m4a` và `truoc_alcatraz_short_15s.m4a`;
  - `sau_tiengdong_noir_15s.m4a` và `truoc_tiengdong_noir_15s.m4a` (radio, máy chiếu, kim; khuếch ×8 cho dễ nghe).
- Đã khôi phục `output/stier/{alcatraz, mim-nvidia-quan-an-dem}`, assets/compositions và sổ variety về bản cũ. Bản dựng thử nằm trong scratchpad.

### Rủi ro / việc còn lại
- Bộ lọc chỉ hạ mức xung, khoảng 3–5 dB. Kurtosis vẫn ~5,6, nên lint luôn in cảnh báo "giọng kiểu buzz" cho CL. Muốn hết hẳn thì phải đổi giọng (S1a).
- Long CL đang dở trên máy sản xuất mà còn `sfx.wav` cũ (có clip) sẽ bị lint chặn ở `final`. Cần chạy lại `html` để dựng lại sfx/mix.
- Tiếng noir nhỏ và tối hơn rõ rệt. Nên nghe lại một chương có radio/film trên Long CL kế tiếp.
- Long CL chưa được dựng thật trên máy này. Cần chạy lệnh ở mục 5 trên máy sản xuất sau Long CL kế tiếp.