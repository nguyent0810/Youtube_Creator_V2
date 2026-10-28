# T4W1 — KỊCH BẢN + FACTCHECK cho `mim-moneyball`

Vòng này **chỉ ghi 3 file**:
- `data/long/mim-moneyball/script.md`
- `data/long/mim-moneyball/factcheck.md`
- `docs/pm/tickets/2026-10-26-codex-pilot/T4W1-ket-qua.md`

Không dựng cảnh, không TTS.

**Chỉ đọc 4 thứ:**
1. Ticket này.
2. `docs/codex/long-rules.md`, mục "Lỗi đã gặp".
3. `data/long/mim-moneyball/facts.md`: kho dữ kiện Claude đã duyệt. **Chỉ dùng dữ kiện trong kho.** Dữ kiện "vừa" phải có quy dẫn ngay trong câu đọc.
4. Mẫu định dạng `data/long/mim-katherine-johnson/script.md`: đọc CH00 và CH01 để nắm cách viết, `‖`, `»`, tiêu đề chương.

Không grep repo, không đọc code.

## Yêu cầu

- **Tiêu đề:** dòng 1 của `script.md`, ≤ 60 ký tự, một dấu `:`. Ví dụ: "MONEYBALL Ngoài Đời Thật: Billy Beane Và Con Số".
- **Độ dài:** 8 chương, **2.000–2.300 âm tiết** (khoảng 9,5–11 phút). Tự đếm, đừng để thiếu.
- **Cold open:** 04/09/2002, chiến thắng thứ 20 liên tiếp 12–11 (theo đề xuất trong T4R).
- **Mô-típ:** chọn một mô-típ, mỗi chương thêm một dòng. Ví dụ: "Bảng con số của một đội nghèo". Mô-típ phải khác "sáu răng" (bài Turing) và "sổ của một con số" (bài Johnson).
- **Viết cho tai:**
  - Câu một hơi, nói với "bạn".
  - Số làm tròn khi đọc; số chính xác chỉ hiện trên màn hình.
  - Thuật ngữ bóng chày (OBP, on-base, walk…) phải giải thích bằng tiếng Việt ở lần đầu.
- **Không câu đệm.** Danh sách có trong `long-rules.md`. Câu ngắn chỉ đặt sau phán định hoặc khoảnh khắc cảm xúc.
- **Phim *Moneyball*:** chỉ nhắc bằng lời. Chi tiết phim đã đánh dấu khác đời thật thì không kể như sự thật (ví dụ Peter Brand là nhân vật hư cấu dựa trên DePodesta).
- **`factcheck.md`:** mỗi khẳng định có số, ngày hoặc tên phải có một dòng, kèm URL lấy từ kho. Mọi năm xuất hiện trong kịch bản đều phải có trong `factcheck.md`.

## Cổng

1. `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py mim-moneyball`: phải qua cổng integrity. Lệnh này in ra tổng âm tiết; ghi con số đó vào báo cáo.
2. Tự kiểm câu đệm bằng lệnh `findstr` hoặc `Select-String` trên các câu trong danh sách `long-rules.md`.

## Báo cáo

- Tiêu đề, số âm tiết, mô-típ đã chọn.
- Số dữ kiện đã dùng ở từng chương.
- Những chỗ đã quy dẫn dữ kiện "vừa".
