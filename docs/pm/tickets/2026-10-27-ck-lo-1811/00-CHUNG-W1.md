# Luật chung cho ticket KỊCH BẢN (W1) của lô Long CK 18–25/11

**Mỗi ticket chỉ ghi:**
- `data/long/<topic>/script.md`
- `data/long/<topic>/factcheck.md`
- `data/long/<topic>/analysis.py`
- `data/long/<topic>/check.py`
- `data/long/<topic>/results.json`
- `docs/pm/tickets/2026-10-27-ck-lo-1811/<mã>-ket-qua.md`

`script_lines.py` sẽ tự tạo các file `chNN.json`; việc này được phép.

**Chỉ đọc:**
1. Ticket của mình và file này.
2. `AGENTS.md`, mục "CK".
3. `docs/codex/long-rules.md`, mục "Lỗi đã gặp".
4. `docs/codex/long-cheatsheet.md`, mục "Bài học Moneyball".
5. `data/long/<topic>/facts.md`. Đây là kho đã duyệt, **chỉ dùng dữ kiện trong kho**.
6. **Mẫu định dạng:** `data/long/ck-e6-luong-huu-rut-mot-lan/script.md` (phần đầu và CH00–CH01), `analysis.py`, `check.py`.

Không grep repo, không đọc code engine.

## Yêu cầu

- **Tiêu đề:** dùng đúng tiêu đề ở ticket, đặt ở dòng 1. Ghi thêm 2 tiêu đề phụ.
- **Độ dài:** 7 chương (CH00–CH06), **2.300–2.700 âm tiết**. Riêng CH00 ≤ 230 âm tiết.
- **Cold open (CH00):**
  - câu 1 là con số tiền của nhân vật VÍ DỤ GIẢ ĐỊNH, không chào hỏi, không câu meta;
  - câu 2 hoặc câu 3 nói đúng thứ mà biểu đồ đầu tiên sẽ hiện, để cảnh biểu đồ neo vào được trước giây 15;
  - có một nghịch lý;
  - mở **một vòng chính**, đóng ở CH06.
- **Lộ trình:** mỗi bài một dạng riêng, ghi trong ticket. Không "trả lời ba câu hỏi".
- **Viết cho biểu đồ.** Mỗi chương có ít nhất 3 câu đọc ra một con số mà màn hình có thể vẽ được (cột, đường, thác, lịch nhiệt, cột chồng, bộ đếm).
  - Đầu `script.md`, dưới mục "Biểu đồ", liệt kê biểu đồ của từng chương: loại, các điểm số, câu neo.
  - Câu neo phải nói đúng con số đó, bằng chữ.
- **Biểu đồ chính:** biểu đồ của nhân vật lớn dần qua các chương (lấy trong `facts.md`). Ít nhất 4 chương nhắc lại nó bằng lời.
- **Số:**
  - mọi số tự tính sinh trong `analysis.py` → `results.json`;
  - `check.py` tính lại bằng cách khác, phải in `OK`;
  - lời đọc **không có chữ số**: viết bằng chữ, làm tròn dễ nghe;
  - số giả định gắn "ví dụ" trong lời đọc ít nhất một lần mỗi chương.
- **Luật cứng CK:** theo `AGENTS.md`. Không phán cách nào đúng. Câu nào gần lời khuyên thì đổi thành phép tính đặt cạnh nhau.
- **Luật và chính sách:** nói kèm mốc, ví dụ "theo luật có hiệu lực từ đầu năm hai nghìn không trăm hai mươi sáu". Cái nào chưa chốt thì nói là chưa chốt.
- **Câu:** ≤ 35 tiếng. Mỗi 4–6 câu có một câu ngắn. Không câu đệm. Không nhắc "kho", "nguồn mạnh".
- **`factcheck.md`:** đủ dòng cho mọi khẳng định có số, ngày hoặc tên. Mọi năm trong kịch bản đều phải có mặt.

## Cổng (bắt buộc trong vòng)

1. `PYTHONIOENCODING=utf-8 python data/long/<topic>/analysis.py`, rồi `… check.py` → `OK`.
2. `PYTHONIOENCODING=utf-8 python motion/long/script_lines.py <topic>`.
3. `PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py <topic> --strict` cho tới khi **0 lỗi**. Câu dài thì tách ngay.

## Báo cáo `<mã>-ket-qua.md`

- Tổng số âm tiết, số âm tiết của CH00.
- Vòng mở chính: mở ở câu nào, đóng ở câu nào.
- Bảng biểu đồ theo chương.
- Kết quả `check.py` và `studio_lint`.
- Khẳng định nào bỏ vì nguồn yếu.
