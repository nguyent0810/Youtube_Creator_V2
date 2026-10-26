# Theo dõi lỗi Codex theo từng bài

**Lỗi chặn** là lỗi mà nếu không sửa thì không đăng được. Lỗi do review của Claude hoặc do cổng bắt đều tính.

**Vòng** là một lần chạy `codex exec`.

## Turing / Bombe (thử nghiệm, chưa có `long_gate` và `AGENTS` đầy đủ)

| Vòng | Ticket | Lỗi chặn khi giao lại | Ai bắt |
|---|---|---|---|
| 1 | T1 viết + dựng | 3: ngày không nguồn, 18 cảnh toàn chữ, câu đệm | Claude |
| 2 | T1b sửa | 3: còn 5 phút, một clip lặp 8 lần, câu đệm còn sót | Claude, rồi cổng |
| 3 | T2A nghiên cứu | 0 | Claude duyệt |
| 4 | T2B viết | 3: tiêu đề hai dấu hai chấm, thiếu `SAY`, `spec.youtube` thiếu trường | Claude |
| 5 | T2C spec | 0 qua cổng; render ra 2 lỗi: "undefined", khuôn cảnh lặp | Claude xem contact sheet |
| 6 | T2D cảnh | 1: thiếu `hud`, phát hiện khi chạy `describe.py` | Claude |

**Tổng:** 6 vòng Codex, 12 lỗi chặn. Claude tự sửa 2 lỗi nhỏ: `hud` và thêm bảng phát âm.

## Katherine Johnson (lần đo sau khi cải tiến)

| Vòng | Ticket | Lỗi chặn | Ai bắt |
|---|---|---|---|
| 1 | T3A nghiên cứu | 0: 36 dữ kiện (34 mạnh), kiểm trùng đúng, tự đánh dấu chi tiết hư cấu của phim | Claude duyệt |
| 2 | T3B viết + dựng | **Hết quota sau 228.768 token**, chưa ghi file nào. Rollback chạy đúng; Claude làm chính (qua agent con) | `codex_ticket.py` |

| 2b | T3B do Claude làm thay (agent con) | 0 lỗi chặn ở cổng; đạt trong 1 vòng (2.148 âm tiết, 80 cảnh, 7,4 giây/cảnh, 38 URL). Claude sửa thêm 1 lỗi: ảnh AI sẽ bị gắn nhãn "TƯ LIỆU" vì thiếu `credit: false`. Agent con tự phát hiện engine đọc ảnh ở chỗ khác với `AGENTS.md` | Claude review |

**Kết quả:** đã đăng `jHZvT5RWAA4`, private, hẹn 25/11 lúc 20:00, có phụ đề, thumbnail và playlist. Có 6 ảnh AI do Grok Bot tạo; 6/6 đạt ngay lần đầu.

**So với bài Turing:**

| | Turing | Katherine Johnson |
|---|---|---|
| Số vòng | 6 | 2 (1 Codex + 1 agent con) |
| Lỗi chặn | 12 | 1 (Claude sửa) |
| Phần Codex | Nghiên cứu, viết, dựng | Chỉ nghiên cứu (0 lỗi) |

Vòng viết + dựng của Codex chưa đo được vì hết quota.

## Moneyball (sau tối ưu: `AGENTS.md` gọn, có cheatsheet, chạy phiên mới, effort medium)

| Vòng | Ticket | Token | Lỗi chặn | Ai bắt |
|---|---|---|---|---|
| R | T4R nghiên cứu (có search) | 95.345 | 0. Có 32 dữ kiện, 30 mạnh | Claude duyệt |
| W1 | T4W1 kịch bản | 74.590 | 0. 2.216 âm tiết, không câu đệm | Claude duyệt |
| W2 | T4W2 cảnh/spec | 65.617 | 4 (chi tiết bên dưới) | Claude, sau đó cổng mới |

**4 lỗi chặn ở W2:**

| Lỗi | Nguyên nhân | Claude đã làm |
|---|---|---|
| TTS mới chạy 3/8 chương | `long_gate` cộng thiếu thời lượng nên báo ĐẠT giả | Cổng giờ chặn khi chưa TTS đủ |
| Không tải được clip | `pexels.py get` cần `index.json`; cheatsheet chưa nói | Sửa `pexels.py`: tải thẳng theo id |
| 2 clip là bản dọc | | Claude thay bằng clip ngang |
| Bỏ qua 3 lỗi lint câu > 35 tiếng | Codex cho là "lời đọc đã duyệt" | Claude tách câu; cheatsheet ghi rõ phải tách |
| Prompt ảnh dùng tiêu đề `####` | Script gửi bot không đọc được | Sửa regex trong `ai_img_request.py` |

**Thêm lỗi chặn ở W2, phát hiện khi chạy `html`:**
- 28 neo bám vào chữ số.
- 1 cặp neo ngược thứ tự (ch00).
- 2 neo trỏ sai câu (ch02).

Báo cáo W2 ghi "html đã chạy", nhưng thực tế html lỗi. Cộng thêm phần neo bị lệch do Claude tách câu sau khi đã dựng cảnh. Claude viết `fix_anchors` cho các neo chữ số, phần còn lại giao vòng T4W2b.

**Tổng 3 vòng: 235.552 token, 4 lỗi chặn.**

**Vòng W2b** (sửa neo): 52.997 token. html qua 8/8 chương.

**Claude review bản render bắt thêm 3 lỗi:**
- Clip sân Dodger Stadium lộ logo "LA". Thay clip.
- Cảnh `org` có 1,3 giây màn trống. Cổng của render chặn; sửa neo.
- Tên "DEP ODESTA" bị tách. Sửa, và `long_gate` giờ chặn tên riêng bị tách trên màn hình.

**Tổng Moneyball:** 4 vòng Codex, **288.549 token**, khoảng 9 lỗi chặn. Không lỗi nào lặp lại lỗi của bài Turing hay Johnson.

So với bài Turing (6 vòng, 12 lỗi): ít vòng hơn, và lỗi chuyển từ "nội dung và sự thật" sang "kỹ thuật dựng" (neo, clip, chính tả trên màn hình). Mỗi loại lỗi kỹ thuật đã có cổng hoặc công cụ tự chặn. Hai lỗi do công cụ, hai lỗi do Codex. Không lặp lại lỗi nào đã ghi trong "Lỗi đã gặp".

## Social Network (quy trình sau Moneyball)

| Vòng | Ticket | Token | Lỗi chặn |
|---|---|---|---|
| R | T5R nghiên cứu | 93.705 | 0. 34 dữ kiện, 28 mạnh. Elo được đánh dấu là chỉ có trong phim |
| W1 | T5W1 kịch bản + lint | 83.530 | 1: ba câu đọc lộ chữ "kho nguồn". Claude sửa, và `long_gate` giờ chặn lỗi này |
| W2 | T5W2 cảnh/spec | 125.718 | 1: ghim bản đồ sai tên, làm ch02 đứng hình 72 giây. Chỉ lộ ra sau render. `long_gate` giờ chặn, thêm `freeze_check.py` |

**Lỗi do công cụ, không phải do Codex:** `codex_ticket.py` rollback nhầm vì regex quota khớp "429" trong id clip 7490429. Đã sửa: chỉ dòng `ERROR:` thật mới tính là hết quota.

**Tổng:** 3 vòng Codex, **302.953 token, 2 lỗi chặn**. So với Moneyball: 4 vòng, 288.549 token, khoảng 9 lỗi.

- Không còn lỗi neo, clip lộ logo, câu dài hay TTS thiếu.
- Hai lỗi còn lại đều là loại mới và đã có cổng chặn.
- Kiểm ngược bằng `freeze_check` bắt được thêm Moneyball ch06: cảnh `question` đứng hình 20 giây. Đã sửa và tải lại sau khi chủ kênh duyệt.

## Macintosh 1984 (có thử 8 thẻ thư viện FS/BUD)

| Vòng | Ticket | Token | Lỗi chặn |
|---|---|---|---|
| R | T6R nghiên cứu | 89.286 | 0: 34 dữ kiện, 26 mạnh |
| W1 | T6W1 kịch bản + 3 thẻ hook | 60.779 | 0: cold open 201 âm tiết; trả một phần ở câu 2; chuột xuất hiện 7/8 chương |
| W2 | T6W2 cảnh + object_continuity + pixel_art | 116.945 | 2: (a) ảnh dọc của Jobs bị cắt giữa, mất đầu; (b) tiêu đề chương "CHÍN MƯƠI K". Claude sửa; thêm cảnh báo `focus` vào `long_gate` |

**Tổng:** 3 vòng, **267.010 token, 2 lỗi chặn**. Đã đăng `OH1RsQ9sSJg`, hẹn 30/11.

Kiểm ngược bằng cảnh báo `focus` mới: ảnh `beane06` của Moneyball cũng bị cắt mất đầu ở ch02/ch04.

**Bài học từ vòng 2:**
- Codex tiêu gần hết quota cho việc khám phá: grep và đọc `build_long.py`, `pexels.py`, thư mục của bài khác.
- Vòng chạy tiếp phiên cũ (`--resume`) mang theo cả ngữ cảnh nghiên cứu, nên mỗi lượt gọi tốn hơn.
- Sửa cho ticket sau:
  - chỉ đích danh các file mẫu cần đọc và cấm khám phá lan man;
  - vòng viết chạy phiên mới thay vì `--resume`, vì kho dữ kiện đã nằm trong `facts.md`;
  - chia vòng viết làm hai: (a) kịch bản và factcheck, (b) cảnh, spec và `SAY`. Hết quota giữa chừng thì vẫn giữ được nửa đã xong.

**Mục tiêu:** ≤ 2 vòng sau nghiên cứu, ≤ 2 lỗi chặn, không còn lỗi nào thuộc loại đã có trong mục "Lỗi đã gặp" của `AGENTS.md`.
