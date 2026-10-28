# Ticket YCV-im1r · Codex · 6 Short pilot MIM 13–18/11 (spec + render)

Repo: thư mục hiện tại. Đọc trước:
- `.tickets/YCV-im1r.md`
- `docs/pm/pilot-short/mim-pilot-scripts.md`: kịch bản đã viết, gồm **lời đọc, tiêu đề, mô tả, nguồn** của 6 bài.
- `docs/pm/pilot-short/mim-pilot-1318-factcheck.md`: dữ kiện. Mọi số trên hình phải khớp file này.
- `docs/pm/2026-10-28-pilot-short-hook.md`, mục 5: biến thử duy nhất là câu mở 2 giây, còn lại giữ cố định.
- Mẫu spec MIM: `data/stier/specs/mim-bo-xac-thuc-giong-noi.json`, `data/stier/specs/mim-turing-1950-loi-doan.json`.

## Việc

1. **Sửa bài 13/11 đã có: `data/stier/specs/mim-p1-quang-cao-giong-gia.json`.**
   - Lời đọc giữ nguyên.
   - Lệnh `python motion/stier/build.py mim-p1-quang-cao-giong-gia --no-render` đang báo: `phối cảnh chưa đạt (luật mix 12/10/2026): 3 cảnh liền cùng kiểu M (cảnh 0–2)`.
   - Đọc luật mix trong `motion/stier/build.py` (tìm "luật mix") để biết kiểu nào tính là M. Sắp lại cảnh cho đạt luật.
2. **Viết 5 spec còn lại**, theo đúng slug, lời đọc, tiêu đề, mô tả và nguồn trong `mim-pilot-scripts.md`:
   - `mim-p2-tin-nhan-thoai`
   - `mim-p3-nghe-nhap-lieu`
   - `mim-p4-ilo-2023-van-phong`
   - `mim-p5-recsys-2016`
   - `mim-p6-feed-cua-ban`

   Mỗi spec phải có:
   - `"theme": "mim"`, `"short_type": "S"`;
   - khối `"pilot": {"pair", "hook", "long", "date"}` như bài p1;
   - `sources` chỉ gồm URL https.

   Được rút câu chữ cho đủ ràng buộc 55–135 chữ. Không đổi số liệu. Không thêm dữ kiện nằm ngoài factcheck.
3. **Hình:**
   - **Không dùng ảnh người thật.** MIM chỉ nhận ảnh PD/CC0/CC BY. Johansson không có ảnh hợp lệ.
   - Clip Pexels: tìm bằng `python motion/stier/clips.py search "<từ khoá>" --src pexels --n 8`, xem bảng poster, chọn clip không có logo hay chữ đọc được.
   - Số liệu do hãng tự công bố (YouTube 80 tỉ tín hiệu, TikTok 2020) phải ghi "THEO YOUTUBE · 2021" / "THEO TIKTOK · 2020" trên hình.
   - Điểm ILO 0,70 không bao giờ hiển thị thành "70%".
4. **Dựng:**
   - Mỗi bài chạy `python motion/stier/build.py <slug> --no-render` trước, sửa tới khi sạch. Sau đó render bằng `python motion/stier/build.py <slug>`.
   - **Mỗi lần chỉ render một bài.**
   - Mỗi bài dài 25–35 s; độ dài chênh trong cùng cặp không quá ±3 s.
   - Sau mỗi bài, chạy `python motion/long/clip_sheet.py` (hoặc bảng khung của build) và tự soi:
     - chữ tiếng Việt không mất dấu, đặc biệt "ì", "đ";
     - nhãn không bị cắt ở mép;
     - không có logo.
5. **Không đăng, không enqueue, không gọi YouTube API, không commit.** Claude review rồi mới đăng.

## Báo cáo (in ở cuối)

Viết `docs/pm/tickets/YCV-im1r-report.md`, gồm:
- bảng: slug, số chữ, thời lượng giọng, đường dẫn `final.mp4`;
- clip đã dùng;
- mọi chỗ đã rút hoặc đổi so với kịch bản;
- lỗi còn lại.
