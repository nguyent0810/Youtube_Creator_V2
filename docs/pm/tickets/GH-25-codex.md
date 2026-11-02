# GH-25 · Codex: lint chữ trên hình, SRT trong final, factcheck, mô tả (A2, A5, A11, A12)

- Issue: https://github.com/nguyent0810/Youtube_Creator_V2/issues/25
- Bối cảnh: `docs/pm/2026-10-29-jobs-1985-loi-pipeline.md`, các mục B, E và phần "Bổ sung sau retro".
- **Chạy sau GH-24**: cả ba ticket cùng sửa `build_long.py`.

## Được ghi
- `motion/long/studio_lint.py`
- `motion/long/build_long.py`: chỉ sửa `do_final`
- `motion/long/describe.py`
- `motion/long/factcheck_lint.py` (file mới)
- `motion/long/publish_long.py`: chỉ sửa phần cổng trước khi upload
- `tests/test_studio_lint_text.py`, `tests/test_factcheck_lint.py` (mới), `tests/test_describe_fit.py`
- Báo cáo: `docs/pm/tickets/GH-25-report.md`

**Không được:** sửa `data/long/**`, render, upload, commit.

## Việc

1. **A2, `studio_lint.py`**: thêm 2 luật, cả hai là lỗi ở chế độ `--strict`.
   - **Chữ trên hình trùng tiền tố câu đọc.** Chữ chính của cảnh (kinetic, slam, tiêu đề…) trùng ≥ 4 từ đầu của câu đang đọc trong cảnh, so sánh không phân biệt hoa thường và dấu câu. Lỗi gốc ở W2: `" ".join(L[i].split()[:5]).upper()`. Trích dẫn có nhãn TRÍCH DỊCH được miễn.
   - **Nhãn tiếng Việt thiếu dấu.** Chuỗi toàn ASCII mà chứa từ tiếng Việt quen thuộc viết không dấu (vd `NAM`, `TRIEU`, `NGUOI`, `CONG TY`).
     - Dựng danh sách từ có chứng cứ, và miễn tên riêng tiếng Anh: Apple, NeXT, CEO…
     - Ưu tiên tránh báo nhầm; trường hợp không chắc thì đưa vào báo cáo.
2. **A5, `do_final`**: cuối bước này gọi `motion/long/srt.py`, để tạo `captions.vi.srt`. `srt.py` lỗi thì `final` báo lỗi.
3. **A11, `factcheck_lint.py <topic>`**
   - Mọi số và ngày trên hình (chữ cảnh) và trong `script.md` phải có trong `factcheck.md` hoặc `research.md`.
   - Mỗi câu có nhãn TRÍCH DỊCH phải có nguyên văn tiếng gốc kèm nguồn trong `factcheck.md`.
   - Mục trong `factcheck.md` không còn xuất hiện trong bài thì báo "lệch bản final". Retro gặp mục Microsoft $150M đã bỏ khỏi bài nhưng vẫn nằm trong bảng.
   - Đọc `data/long/mim-jobs-1985/factcheck.md` để nắm định dạng thực tế. Nếu định dạng giữa các bài không thống nhất, đề xuất một định dạng và ghi vào báo cáo; không sửa file dữ liệu.
   - `publish_long.py` từ chối đăng khi `factcheck_lint` có lỗi. Chỉ áp dụng cho bài chưa có `video_id`, giống cách `floor` đang làm.
4. **A12, `describe.py`**
   - Bỏ dòng `🎵 NHẠC NỀN` khi không có nhạc.
   - Xem lại giới hạn `[:8]` nguồn (khoảng dòng 134) và `fit_sources`. Nguồn được trích trực tiếp trong lời đọc không được bị cắt; giới hạn chỉ áp dụng khi mô tả vượt 5.000 byte.
5. **Test và hồi quy**
   - Mỗi luật có ca đạt và ca trượt.
   - `python -m pytest -q tests/` phải xanh.
   - Chạy `studio_lint` (2 luật mới) và `factcheck_lint` trên mọi topic MIM/CK trong `data/long/`. Ghi một bảng: topic, số lỗi theo từng luật.
   - Với Jobs 1985, ghi rõ lint có bắt được hai lỗi retro đã nêu hay không: thẻ TRÍCH DỊCH ở ch01 là diễn ý, và `factcheck.md` lệch bản final.

## Báo cáo `docs/pm/tickets/GH-25-report.md`
Gồm: luật đã thêm, danh sách từ thiếu dấu, định dạng `factcheck` đề xuất, kết quả pytest, bảng hồi quy, các điểm chưa chắc.
