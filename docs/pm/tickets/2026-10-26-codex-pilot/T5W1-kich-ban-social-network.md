# T5W1 — KỊCH BẢN + FACTCHECK cho `mim-social-network`

## Phạm vi

**Chỉ ghi 3 file:**
- `data/long/mim-social-network/script.md`
- `data/long/mim-social-network/factcheck.md`
- `docs/pm/tickets/2026-10-26-codex-pilot/T5W1-ket-qua.md`

Lệnh `script_lines.py` sẽ tạo thêm các `chNN.json` chứa `lines`. Điều đó chấp nhận được.

**Chỉ đọc:**
1. Ticket này.
2. `docs/codex/long-rules.md`, mục "Lỗi đã gặp".
3. `docs/codex/long-cheatsheet.md`, mục "Bài học Moneyball".
4. `data/long/mim-social-network/facts.md`. Đây là kho đã duyệt. **Chỉ dùng dữ kiện trong kho.** Dữ kiện "vừa" phải có quy dẫn ngay trong câu đọc.
5. Mẫu định dạng: CH00 và CH01 của `data/long/mim-moneyball/script.md`.

Không grep repo, không đọc code.

## Yêu cầu

- **Tiêu đề:** dòng 1 của `script.md`, ≤ 60 ký tự, một dấu `:`. Ví dụ: "THE SOCIAL NETWORK Ngoài Đời Thật: Facemash 2003".
- **Độ dài:** 8 chương, **2.000–2.300 âm tiết**.
- **Cold open:** theo đề xuất trong T5R, có ngày giờ.
- **Mô-típ:** chọn một mô-típ, mỗi chương thêm một dòng. Phải khác "sáu răng" (Turing), "sổ một con số" (Johnson) và "tấm bảng lên gôn" (Moneyball).
- **Người thật còn sống:**
  - Chỉ kể sự kiện có nguồn.
  - Không suy diễn động cơ hay tính cách.
  - Lời trích lấy đúng nguồn trong kho, gắn `[TRÍCH DỊCH]`.
- **Công thức Elo:** chỉ nhắc như một cảnh trong phim. Kho không có nguồn mạnh xác nhận Facemash thật sự dùng Elo.
- **Viết cho tai:**
  - Câu một hơi, nói với "bạn".
  - Thuật ngữ (thuật toán, xếp hạng, House…) phải giải thích ngay lần đầu xuất hiện.
  - Không có câu đệm.
- **`factcheck.md`:** mỗi khẳng định có số, ngày hoặc tên phải có một dòng kèm URL. Mọi năm có trong kịch bản đều phải xuất hiện trong `factcheck.md`.

## Cổng (bắt buộc trong vòng này)

1. Chạy `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py mim-social-network`. Phải qua integrity; ghi số âm tiết in ra.
2. Chạy `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py mim-social-network --strict`. Lỗi "câu > 35 tiếng" thì **tách câu ngay trong `script.md`**, chạy lại bước 1 và 2 cho tới khi ra **0 lỗi**. Cảnh báo không cần sửa.

## Báo cáo

- Tiêu đề, số âm tiết, mô-típ đã chọn.
- Số dữ kiện đã dùng ở từng chương.
- Kết quả `studio_lint`.
