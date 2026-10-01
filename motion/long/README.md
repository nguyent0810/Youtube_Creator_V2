# Video DÀI 16:9: hồ sơ graphic motion (kênh Hình Sự)

Anh em ngang của `motion/stier/` (Short dọc). Cùng ngôn ngữ hình: hồ sơ lưu trữ, tư liệu thật, một màu nhấn. Khác ở ba điểm:

- bố cục ngang 1920x1080;
- chia theo chương;
- có video B-roll Pexels và nhạc nền thật.

Bộ kỹ năng giữ chân người nghe: **[RETENTION.md](RETENTION.md)**. Đọc file này TRƯỚC khi viết kịch bản.

## Quy trình

Dùng python của `vietneu-tts/.venv`, vì bước TTS cần gói `vieneu`.

```
python motion/long/research_long.py yakuza "Yakuza" "Yamaguchi-gumi" "?Sugamo Prison"   # bài Wikipedia + ảnh Commons tự do ("?"= tìm ảnh)
python motion/long/pexels.py search yakuza "tokyo night rain" ...                      # B-roll ngang
python motion/long/pexels.py get yakuza <id> <id> ...
# viết data/long/yakuza/spec.json + ch00.json … chNN.json
python motion/long/build_long.py yakuza takes 3        # (tuỳ chọn) đọc mỗi câu 3 lần -> tts/takes.json
<.venv-video python> motion/long/stt_takes.py yakuza   # Whisper nghe lại mọi bản -> tts/transcripts.json
python motion/long/build_long.py yakuza pick           # chọn bản khớp chữ nhất -> tts/picks.json, in câu đáng nghe lại
python motion/long/build_long.py yakuza tts            # đọc giọng, cache theo từng câu (dùng picks nếu có), in thời lượng từng chương
python motion/long/build_long.py yakuza html           # ảnh, bản đồ, data.js, composition, sfx, mix từng chương
python motion/long/build_long.py yakuza render ch03 --draft   # nháp có tiếng: chNN/draft_av.mp4
python motion/long/build_long.py yakuza render         # bản thật, từng chương
python motion/long/build_long.py yakuza final          # nối chương + loudnorm -14 LUFS -> final.mp4
python motion/long/describe.py yakuza                  # mô tả: mốc chương + nguồn + ghi công ảnh/nhạc/video
```

Giọng: vieneu 3.8.3, `VOICE = "Anh Khôi"` (3.8.3 đổi tên thành "Thiện Minh", tên cũ là alias, embedding y hệt).
Bước trộn áp `VOICE_FX` (highpass 70, -2dB@200, +2.5dB@3.2k, de-esser, nén 3:1) lên giọng; spec `"master": false` để tắt
(Yakuza đặt false vì bản đã đăng dùng giọng thô). Mốc chữ luôn lấy từ voice.wav thô.

## Spec

`spec.json` gồm:

- `imgs {key: "File:..."}`: nhận PD, CC0, CC BY và CC BY-SA. Không nhận NC, ND.
- `geo {tên: {countries, bbox, pins, box}}`
- `say {chữ hiển thị: cách đọc}`: ví dụ `"inagawa-kai": "Inagawa cai"`. Phụ đề vẫn giữ chữ gốc.
- `youtube {titles, summary, sources, tags}`

Mỗi chương `chNN.json` gồm:

- `hud {k, t}`
- `bgm {file, at, gain}`
- `lines[]`: mỗi phần tử là một chuỗi, hoặc `{"t": ..., "p": giây_nghỉ}`.
- `scenes[]`

Mốc thời gian dùng giống Short:

| Cú pháp | Nghĩa |
|---|---|
| `i` | đầu câu thứ i |
| `[i, "từ", n, lệch]` | lúc đọc chữ đó (lần thứ n, cộng thêm độ lệch) |
| `[i, null, 0, lệch]` | đầu câu i cộng độ lệch |

Sai chữ neo là lỗi cứng: build dừng ngay, không để lỗi lọt vào render.

## Kịch bản → dữ liệu dựng, theme noir

- `python motion/long/script_lines.py <topic>`: chuyển `data/long/<topic>/script.md` (đã duyệt) thành `lines` của từng `chNN.json`.
  `‖` = nghỉ dài, `**[DIỄN Ý]**` = trích diễn ý, `»` = lời trích, đọc bằng `QUOTE_VOICE` (Minh Đức) qua bộ lọc radio, cảnh quote có `qline` sẽ hiện sóng âm và nhãn "GIỌNG ĐỌC MINH HỌA".
- `spec.theme = "noir"`: khung điện ảnh 96px, phụ đề nằm trong dải đen dưới, cảnh `film: true` có nhấp nháy và tiếng máy chiếu.
- Cảnh riêng của noir: `seismo` (băng địa chấn, `hitAt`), `saint` (thẻ thánh cháy, `burnAt/burnDur/burnTo`), `paper` (trang báo mô phỏng),
  `pizzini` (giấy đánh máy + `cipher` chữ→số kiểu Provenzano), `dots` (mỗi chấm một người, `groups`), `board` (bảng ghim + dây đỏ),
  `memorial` (tên khắc đá), `calendar` (lịch xé `from/days/endAt`), `sticker` (tờ dán Addiopizzo).
- Mọi cảnh nhận `sfx: [{k: "gavel"|"bell"|"heart"|"match"|"slap"|…, at}]` để đặt tiếng tay.
- `bgm` có thể là danh sách đoạn `{file, at, gain, start, end, fin, fout}` (start/end là mốc lời) để đổi nhạc giữa chương.

## Loại cảnh (casewide.js)

| Loại | Dùng cho |
|---|---|
| `chapter` | Thẻ chương |
| `broll` | Video Pexels, có thể kèm `kin` (chữ phủ) |
| `photo` | Ảnh tràn khung, Ken Burns |
| `print` | Ảnh in cạnh khối chữ; dành cho ảnh dọc hoặc chân dung |
| `file` | Thẻ hồ sơ; dòng thông tin hiện dần theo lời đọc |
| `kinetic` | Chữ động |
| `slam` | Một dòng chữ đập mạnh |
| `question` | Câu hỏi; nhạc tắt, ẩn phụ đề |
| `counter` | Số đếm |
| `bars` | Biểu đồ cột |
| `timeline` | Dòng thời gian ngang |
| `map` | Bản đồ |
| `quote` | Trích dẫn; `dy:true` gắn nhãn DIỄN Ý |
| `org` | Sơ đồ gia đình hoặc tổ chức |
| `ledger` | Bảng kê |
| `split` | Hai ảnh đặt cạnh nhau |
| `date` | Ngày tháng |
| `cards` | Ván bài lật |
| `evidence` | Tang vật |

Nhiều cảnh nhận thêm các trường sau:

- Nền: `vid` (id Pexels, `ms` = giây bắt đầu trong clip) hoặc `bg` (ảnh).
- Lớp phủ: `label`, `tag`, `illus`, `stamp`.

Credit ảnh tự hiện theo giấy phép.

## Bẫy đã gặp

- `<video>` phải được **nướng tĩnh** vào HTML. HyperFrames bỏ qua thẻ video do script tạo ra. Build tự kiểm tra clip có đủ dài cho cảnh không.
- Anh Khôi đọc "8-9-3" thành "8 đến 9 ba", nên phải viết bằng chữ. Đuôi "-kai" bị đọc thành "ki", nên cần map `say`.
- Tốc độ render khoảng 2,7 lần thời lượng thực (video 34 phút mất khoảng 90 phút).
- `motion/hf/assets/long` là junction trỏ tới `output/long`, nên ảnh và video không phải copy.

## Đăng: thumbnail, SEO, phụ đề, playlist

- Thumbnail: mẫu ở `thumbs/`, copy vào `motion/hf/compositions/long/` rồi render 1 khung.
  - Công thức rút từ nghiên cứu CTR: độ tương phản cao là biến mạnh nhất, tiếp theo là gương mặt hoặc hình người.
  - Chữ chỉ 0–3 từ, bổ sung cho tiêu đề chứ không lặp lại.
  - Tối đa 2–3 thành phần, không khí poster phim.
  - Luôn soi ở cỡ mobile (~200px).
  - Làm 3 bản để A/B test bằng Test & Compare trong Studio.
- `python motion/long/describe.py <topic>`: mô tả ≤5000 **byte**, gồm hook 2 dòng đầu chứa từ khóa, link xem tiếp, mốc chương, nguồn, ghi công.
- `python motion/long/srt.py <topic>`: phụ đề tiếng Việt từ mốc từng từ.
- `python motion/long/publish_long.py <topic> CL <publishAt UTC> --playlist "Tên" "Mô tả" <id…>`: chạy lần lượt các bước sau.
  1. upload private + publishAt
  2. category
  3. thumbnail
  4. phụ đề
  5. playlist mới
  - Chạy lại thì các bước đã xong được bỏ qua.
