# T6W1 — KỊCH BẢN + FACTCHECK cho `mim-macintosh-1984`

**Chỉ ghi:**
- `data/long/mim-macintosh-1984/script.md`
- `data/long/mim-macintosh-1984/factcheck.md`
- `docs/pm/tickets/2026-10-26-codex-pilot/T6W1-ket-qua.md`

`script_lines.py` sẽ tự tạo các file `chNN.json` chứa `lines`; việc này được phép.

**Chỉ đọc:**
1. Ticket này.
2. `docs/codex/long-rules.md`, mục "Lỗi đã gặp".
3. `docs/codex/long-cheatsheet.md`, mục "Bài học Moneyball" và "Bài học Social Network".
4. `data/long/mim-macintosh-1984/facts.md`. Đây là kho đã duyệt. **Chỉ dùng dữ kiện trong kho.** Dữ kiện "vừa" phải có quy dẫn ngay trong câu đọc.
5. Mẫu định dạng: CH00 và CH01 của `data/long/mim-social-network/script.md`.

Không grep repo, không đọc code.

## Yêu cầu

- **Tiêu đề:** dòng 1, ≤ 60 ký tự, một dấu `:`, mỏ neo đứng đầu. Ví dụ: "STEVE JOBS Ngoài Đời Thật: Chiếc Macintosh 1984".
- **Độ dài:** 8 chương, **2.000–2.300 âm tiết**.
- **Thử 3 thẻ hook của thư viện FS/BUD** (đây là thử nghiệm, Claude sẽ đo):
  - `hook_frame_dau_la_thumbnail`: câu đầu tiên là mốc **24/01/1984** cộng một lời hứa cụ thể. Không chào hỏi, không câu meta.
  - `hook_long_60_giay`:
    - Cold open (CH00) dài **≤ 60 giây** lời đọc, tức khoảng ≤ 210 âm tiết.
    - Trong 30 giây đầu phải **trả một phần nhỏ** của lời hứa, ví dụ một chi tiết lạ có thật trong buổi ra mắt.
    - Từ giây 30 đến 60, nói video sẽ đi qua những mốc nào, và mở một câu hỏi sẽ đóng ở giữa hoặc cuối video.
  - `chude_nguoi_nam_buoc_ngoat`: một người (Jobs, nhưng không kể như một mình ông làm), một năm (1984), một bước ngoặt (máy tính nói bằng hình).
- **Vật nối:** con chuột một nút. Nhắc trong lời đọc ở ít nhất 4 chương, để cảnh của vòng sau có chỗ neo.
- **Người thật:** chỉ sự kiện có nguồn. Đội Mac và Xerox PARC được ghi công đúng mức kho cho phép.
- **Phim** *Steve Jobs* (2015) chỉ được nhắc. Chi tiết phim khác đời thật chỉ kể khi kho có nguồn.
- **Viết cho tai:**
  - Thuật ngữ (giao diện đồ hoạ, dòng lệnh, RAM, con trỏ…) phải giải thích ngay lần đầu.
  - Không câu đệm.
  - Không nhắc "kho" hay "nguồn mạnh" trong lời đọc.
- **`factcheck.md`:** đủ dòng cho mọi khẳng định có số, ngày hoặc tên. Mọi năm xuất hiện trong kịch bản đều phải có mặt trong `factcheck.md`.

## Cổng (bắt buộc trong vòng)

1. Chạy `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py mim-macintosh-1984`.
2. Chạy `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py mim-macintosh-1984 --strict` cho tới khi **0 lỗi**. Câu dài thì tách ngay.
3. Tự đếm âm tiết của CH00 và ghi vào báo cáo (mục tiêu ≤ 210).

## Báo cáo

- Tiêu đề, tổng số âm tiết, số âm tiết của CH00.
- Câu "trả một phần" nằm ở dòng nào.
- Lộ trình và câu hỏi treo.
- Chương nào nhắc con chuột.
- Kết quả `studio_lint`.
