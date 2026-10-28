# Luật chung cho ticket DỰNG CẢNH (W2) của lô Long CK 18–25/11

Claude đã duyệt `script.md`. **Không sửa lời đọc.**
- Một câu > 35 tiếng làm lint lỗi thì được tách đôi, giữ nguyên chữ.
- Không render, không upload, không chạy `thumb.py`, không gọi bot ảnh.

**Báo cáo:** `docs/pm/tickets/2026-10-27-ck-lo-1811/<mã>-ket-qua.md`

## Chỉ đọc

- Ticket của mình và file này.
- `docs/codex/long-cheatsheet.md`: mục "Bài học Moneyball", "Bài học Social Network", "Long CK: cảnh biểu đồ", "Long CK: ảnh nhân vật và ảnh tĩnh", "Thứ tự lệnh".
- `docs/codex/long-rules.md`, mục "Lỗi đã gặp".
- **Khung để chép:** `data/long/ck-e6-luong-huu-rut-mot-lan/gen_scenes.py`. Cảnh viết bằng dict trực tiếp, có `SPEC` và `main()`.
- Trong `data/long/<topic>/`: `script.md`, `facts.md`, `results.json`, `ai_prompts.md`, các `chNN.json`.

Không đọc engine, không grep repo.

## Làm

1. **Tạo `gen_scenes.py`:** chép khung, thay nội dung.
   - `SPEC` có `"chart_rules": True`.
   - `"imgs": {"ai01": "EXT:ai:ai_01", …, "ai06": "EXT:ai:ai_06"}`. Ảnh đã ở `motion/hf/assets/long/<topic>/img/ai/` và `output/long/<topic>/img/`.
   - `"say"`: phiên âm mọi viết tắt và từ ngoại trong lời đọc. Ví dụ: BHYT, BHXH, T+2, HOSE, HNX, UPCoM. Khoá viết thường.
   - `youtube`:
     - đủ trường như khung;
     - `titles[0]` = dòng 1 của `script.md`;
     - `sources` ≥ 8 URL lấy từ `factcheck.md`;
     - mô tả có câu "Nội dung giáo dục, không phải tư vấn đầu tư.";
     - không có chữ cấm (xem `AGENTS.md`).
   - `hud {k, t}` cho mọi chương. Thẻ chương đủ `no`, `k`, `title`.
2. **Biểu đồ:** làm theo bảng "Biểu đồ" ở đầu `script.md`. Số lấy từ `results.json`, không gõ tay.
   - Biểu đồ thật ≥ 35% số cảnh. Thẻ chữ (`kinetic`, `question`, `slam`, `myth`, `quote`) ≤ 25%. Không quá 2 thẻ chữ liền nhau.
   - **Biểu đồ đầu tiên của CH00 neo vào câu 0, 1 hoặc 2.**
   - **Biểu đồ chính** (ghi trong ticket) xuất hiện lại ở ít nhất 4 chương, mỗi lần thêm điểm mới. Ở chương cuối hiện đủ.
   - **Dữ liệu thật của Việt Nam** (thêm 27/10 sau phân tích ngoài: 2 Long CK thắng đều là số liệu thật Việt Nam): mỗi bài có ≥ 2 biểu đồ dùng số thật có nguồn trong `facts.md`, ví dụ số người hưởng, tỉ lệ chi tiền túi hay cơ cấu chi tiêu Cục Thống kê. Ít nhất 1 biểu đồ nằm ở CH00 hoặc CH01. Ghi nguồn bằng `source` (cảnh race/waterfall/heat/stack) hoặc `srcnote` (cảnh bars/counter/units), ví dụ "NGUỒN: BHXH VIỆT NAM · 6 THÁNG ĐẦU 2026". Số giả định của nhân vật vẫn giữ nhãn VÍ DỤ GIẢ ĐỊNH, không trộn hai loại trong một biểu đồ.
   - Mỗi biểu đồ có ít nhất một `calls` (khoanh điểm) neo vào đúng câu đọc ra con số đó.
3. **Ảnh nhân vật:** mỗi chương 1–2 cảnh `photo`.
   - Mọi cảnh có `"credit": False`, `"illus": "ẢNH MINH HỌA"`, `"focus"` vào mặt.
   - Mỗi cảnh dùng một trong các kiểu chuyển động: `reveal` (`circle`/`wipe`), `zoom` hoặc `move` (`in`/`out`/`pan`). Không để hai ảnh liền nhau cùng kiểu.
   - Mỗi ảnh dùng ≤ 3 lần. Cảnh ảnh đứng **trước** biểu đồ của cùng ý.
4. **Clip:**
   - lấy id trong `facts.md`, tải bằng `pexels.py get`;
   - thiếu clip hoặc clip dọc thì `pexels.py search <topic> "từ khoá"` rồi `get`;
   - cần ≥ 6 clip khác nhau, mỗi clip ≤ 2 lần;
   - chạy `clip_sheet.py`, **mở ảnh ra xem**, loại clip lộ logo, chữ hay biển hiệu.
5. **Neo:**
   - tăng dần;
   - không neo vào chữ số;
   - `question`/`slam` chỉ phủ câu của nó;
   - không cảnh nào đứng quá 12 giây.
6. **html:** chạy `gen_scenes.py` → `script_lines.py` → `build_long.py <topic> tts` (đủ 7 chương) → `build_long.py <topic> html`. Phải ra **7/7, không Error**.
7. **Cổng:** `python scripts/long_gate.py <topic> --min-syl 2200` phải **ĐẠT**. Cảnh báo `focus` cũng phải sửa hết.

## Báo cáo

- Kết quả html 7/7 và `long_gate`.
- Tỉ lệ biểu đồ / thẻ chữ.
- Biểu đồ chính nằm ở chương nào.
- Clip đã dùng, và đường dẫn clip sheet.
- Lỗi engine nếu có. Ghi lại, không tự sửa.
