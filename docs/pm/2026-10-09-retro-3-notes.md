# Ghi chú PM cho retro 3 (09/10/2026) — đợt C3 · D2 · MIM #4 · #5 · #6

Ghi ngay khi phát hiện; retro (subagent) đọc file này + retro 1–2. Mỗi mục: chuyện gì · đã xử lý gì · cần chặn bằng máy gì.

## Quy trình
1. **Bỏ bản nháp (người dùng duyệt 09/10):** Tạo > Đăng > Retro. Render thẳng final, soát contact sheet trên final; lỗi chặn mới render
   lại chương đó. Tiết kiệm ~50% thời gian render. Ghi memory `feedback-no-draft-render`.
2. **Chuỗi nhiều kênh bị kẹt theo lượt upload (2 lần trong ngày: final_r4, final_r6):** MIM hết 6 lượt/24 h (5 teaser + MIM #3) -> `--wait`
   chặn luôn C3/D2 của CK ~18 h. Xử lý: tách `c3_now`, `final_r7_d2`, `final_r7_gpu`. **Chặn bằng máy (chưa làm):** run_chain từ chối chuỗi
   gọi publish cho > 1 kênh, hoặc publish_long --wait in cảnh báo khi chuỗi còn bước sau nó. Memory `feedback-background-chains` đã thêm luật.
3. **RAM là nút thắt render (1–2 worker hyperframes, CPU 13–28%):** Chrome/Rambox/Grok/Slack chiếm 7–8 GB. Người dùng đóng bớt app. Cân
   nhắc `--workers` cố định + nhắc đóng app khi có chuỗi render dài.
4. **Grok (TikTok) dùng chung khoá render** (stier short `bud-…` giữ khoá 15–25 phút/lượt) — không phải lỗi, nhưng làm hàng đợi YouTube chậm;
   test `test_console` đỏ vì `motion/stier/bud_variety.py` (của Grok) thiếu `utf8_console()` — không sửa (ngoài phạm vi YouTube).

## Nội dung / hình
5. **Beat text lặp (người dùng góp ý):** 35–50% số cảnh là kinetic cùng một khuôn, 40–50% dòng "sync", chữ chép nguyên lời đọc.
   Đã làm: beat2 (bố cục hero/split/corner/ladder/frame, từ nhấn, sync 1/3 cảnh, cảnh báo chữ chép nguyên lời) — chỉ bật cho spec `beat2`,
   engine trong beat2.js/css riêng (render_key video cũ không đổi). Test `tests/test_beat2.py`.
6. **beat2 lỗi lần đầu (MIM #6: 11 đoạn qa_blank):** sync hiện cả dòng mờ 16% khi chữ đầu đọc muộn > 1,2 s; dòng chính neo vào từ giữa câu
   nên đầu cảnh chỉ có chữ nhỏ. Đã sửa: `apply_sync(max_lead=1.2)`, `pull_main`, lint `light_start` (render từ chối). Còn sót ở D2: 1 cảnh
   dòng chính hiện sau đúng 1,0 s -> **hạ ngưỡng pull_main xuống ~0,8 s**.
7. **qa_blank báo giả:** biểu đồ đang vẽ (candles/race) và thẻ trích dẫn/ledger có khung nhưng chữ chưa hiện bị tính là "trống" (C3: 4,
   D2: 3 — PM xem từng đoạn, duyệt đăng). **Chặn bằng máy:** gen_scenes — cảnh quote/ledger neo vào câu có nội dung đầu tiên (thẻ trích chờ
   3–4 s là có thật, nên sửa); qa_blank — cho phép đánh dấu "chart drawing" theo data.js thay vì chỉ đo năng lượng khung hình.
8. **Thumbnail tràn chữ (MIM #5 t1/t2, D2 t1 nhãn pill):** đã chặn bằng máy — `thumb.py` FIT tự thu chữ `.big/.pill/.tag/[data-fit]` vào
   khung an toàn 40 px. MIM #5 dùng t3.
9. **Nhạc nền trùng 64% (MIM #6 tự chọn theo mood):** thư viện MIM chỉ 14 bài; chọn tay 5 bài Jaccard ≤ 0,27. **Cần:** mở rộng thư viện MIM,
   hoặc resolve_bgm tự tối ưu Jaccard thay vì chọn "ít dùng nhất" theo từng chương.
10. **Ảnh BY-SA lọt vào danh sách nghiên cứu MIM #6** (kênh no_sa) — bắt được trước khi dựng; build_long cũng kiểm lúc tải. Nên để
    `commons.py`/research lọc BY-SA ngay từ bước tìm.
11. **Playlist:** 8 video dài trước đó không vào playlist nào (chuỗi không có bước playlist). Đã làm: `data/playlists.json` + `scripts/playlists.py`
    + publish_long tự thêm. Playlist cũ giữ nguyên (người dùng chọn).
15. **Tràn chữ beat2 (lỗi thật, QA không bắt):** hero/split tính cỡ chữ với hệ số 0,62–0,64 (thiếu cho chữ IN HOA đậm) -> "KHÔNG THAY
    ĐỔI" (MIM #7), "NHANH · MƯỢT" (MIM #6), "ĐẮT HAY RẺ?", "→ LÀM GIỐNG HỌ" (D2), "ĐỘ DỐC MA200" (C4) bị cắt mép; hero 4 dòng đè phụ đề.
    Bắt được nhờ PM soát contact sheet + lưới mọi cảnh bố cục. Đã sửa: K_CAPS 0,72, beat2.js tự co khi scrollWidth > clientWidth, hero
    ≤ 3 dòng + căn giữa cả khối, test giới hạn đáy 860 px. MIM #6/#7 chặn trước khi đăng, render lại. **D2, C4 đã đăng (private) mang lỗi —
    chờ người dùng quyết thay hay giữ.** **Cần:** qa tự động đo tràn chữ (DOM: scrollWidth/bbox ngoài khung) chứ không chỉ năng lượng khung hình.
16. **Tiến trình upload chờ lâu dùng code cũ:** publish_long khởi chạy 09/10 trưa (trước khi thêm bước playlist) chờ tới lượt 10/10 07:44 ->
    MIM #4 lên kênh không vào playlist. Đã chạy `playlists.py sync` bù. **Cần:** chuỗi gọi `playlists.py sync --channel X` sau mỗi lần đăng
    (lệnh riêng, nạp code mới) thay vì chỉ dựa vào publish_long.
17. **MIM #5 (engine cũ) 9 đoạn trống ở QA final** (sync mờ chờ lời, thẻ trích chờ gõ) — bật beat2 cho video này trước khi đăng.
14. **Biểu đồ nến nhiều phiên vẽ chậm = qa_blank (C4: 4 đoạn, 1–4,5 s, gồm 3,2 s ĐẦU VIDEO):** khung, trục đã hiện nhưng nến mọc dần từ trái
    qua; với 300–400 phiên, mấy giây đầu gần trống. PM duyệt đăng (không sai, không hỏng). **Cần:** cảnh candles mở video / mở chương
    hiện sẵn ≥ 30% nến ngay khung đầu (hoặc drawAt ngắn hơn khi số nến lớn); qa_blank đọc data.js để không tính cảnh chart đang vẽ.
13. **Chuỗi không dừng khi `html` lỗi (MIM #7 r8):** html chết ở ch05 (clip 13,7 s < 6+7,8 s cần) rồi ch06 (cảnh trùng mốc 0 với chapter);
    chuỗi lọc output bằng grep nên mất dòng lỗi, đi tiếp tới render rồi mới hỏng (mất ~20 phút chờ khoá). Kèm: `late_report` bỏ qua
    chương thiếu data.js nên PM tưởng "OK". Đã sửa: late_report báo THIẾU data.js; mẫu chuỗi mới (r10) kiểm mã thoát html.
    **Còn cần:** gen_scenes lint "cảnh trùng mốc với chapter" (lỗi lặp 3 lần hôm nay: MIM #6 ch04–07, D2 ch01–02, MIM #7 ch06) và kiểm độ dài
    clip ngay trong gen_scenes (đã có ở html, nhưng nên báo sớm hơn).
12. **MSYS `ln -s` chép thư mục thay vì tạo link** (2,6 GB assets) — đã xoá, dùng junction (PowerShell `New-Item -ItemType Junction`).
