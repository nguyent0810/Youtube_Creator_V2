# Kết quả T4W2 — `mim-moneyball`

## Đã làm

- Tạo `data/long/mim-moneyball/gen_scenes.py` theo khung `mim-katherine-johnson`, gồm spec, 8 chương, 81 cảnh, bảng mô-típ 8 ô, bản đồ Hoa Kỳ (Oakland, Kansas City, Minnesota), bảng phát âm `SAY` và metadata YouTube.
- Tạo `data/long/mim-moneyball/ai_prompts.md` với 3 prompt ảnh minh họa. Các cảnh dùng ảnh AI khai `EXT:ai:ai_NN`; bản `--standin` dùng ảnh Commons thay tạm.
- Đã soát HTML bằng `gen_scenes.py --standin`, sau đó chạy lại bản thật và chạy lại `script_lines.py`.
- Không sửa `script.md` hoặc `factcheck.md`.

## Lệnh đã chạy và kết quả

```text
python motion/long/script_lines.py mim-moneyball
→ 108 câu, 2.216 âm tiết

python data/long/mim-moneyball/gen_scenes.py --standin
python motion/long/script_lines.py mim-moneyball
python motion/long/build_long.py mim-moneyball tts
python motion/long/build_long.py mim-moneyball html
→ đã sửa một lỗi neo trùng ở ch04 cảnh 1 (đổi neo từ “beane” sang “general”).

python data/long/mim-moneyball/gen_scenes.py
python motion/long/script_lines.py mim-moneyball
python motion/long/studio_lint.py mim-moneyball --strict

python motion/long/clip_sheet.py mim-moneyball
→ dừng do thiếu output/long/mim-moneyball/broll/7552614.mp4.

python scripts/long_gate.py mim-moneyball --min-syl 1900
→ mim-moneyball: âm tiết 2216, phút 1.2, cảnh 81, giây/cảnh 0.9,
  clip khác 6, ảnh khác 8, URL nguồn 29
→ ĐẠT
```

## Lỗi lint còn lại

`studio_lint.py --strict` còn 3 lỗi và 8 cảnh báo câu ngắn. Cả ba lỗi là câu dài trong lời đọc đã được Claude duyệt, nên không sửa:

- ch01 dòng 7: 36 tiếng;
- ch02 dòng 1: 37 tiếng;
- ch07 dòng 10: 36 tiếng.

## Clip sheet / Pexels

Đã thử tải đúng các ID được duyệt bằng:

```text
python motion/long/pexels.py get mim-moneyball 7552614 8135918 5726611 6930656 8275595 7691559
```

Lệnh dừng trước khi tải vì thiếu `output/long/mim-moneyball/broll/index.json`. Vì vậy chưa có `output/long/mim-moneyball/qa_clips.jpg` để mở và kiểm tra logo/chữ. Các clip được khai trong cảnh là: `7552614`, `8135918`, `5726611`, `6930656`, `8275595`, `7691559`.

## Ảnh

- Commons dùng trong spec: Billy Beane 2006; Billy Beane tại Leaders Event 2010; Paul DePodesta and Jimmy Haslam; Oakland Coliseum (upper deck, night, overhead, aerial, ticket booths); Baseball game score; Pac Bell scorecard. Tất cả là các file I01–I10 đã được duyệt CC BY hoặc Public domain trong `facts.md`.
- Chờ tạo 3 ảnh AI: `ai_01.png`, `ai_02.png`, `ai_03.png`. Prompt nằm tại `data/long/mim-moneyball/ai_prompts.md`; chưa gọi bot tạo ảnh.

## Khẳng định không kiểm được

Không có khẳng định mới nào được thêm ngoài kho `facts.md` đã duyệt. Không dùng tựa Việt không có nguồn của phim, không suy luận tỷ lệ quỹ lương với đội khác, và không dùng chi tiết phim làm sự kiện lịch sử.
