# Ticket YCV-im1r · agy · render và tự soi 5 Short pilot MIM (p2–p6)

Spec đã sửa xong và đã qua `--no-render`. Việc của bạn là render và tự soi lần đầu. Claude review lần cuối.

## Làm theo thứ tự, mỗi lần một bài

`mim-p2-tin-nhan-thoai` → `mim-p3-nghe-nhap-lieu` → `mim-p4-ilo-2023-van-phong` → `mim-p5-recsys-2016` → `mim-p6-feed-cua-ban`

Với từng bài:

1. Render bằng `python motion/stier/build.py <slug>` (đặt `PYTHONIOENCODING=utf-8`). Chờ lệnh xong rồi mới chạy bài kế tiếp. **Không render song song.**
2. Lấy thời lượng bằng `ffprobe -v error -show_entries format=duration -of csv=p=0 output/stier/<slug>/final.mp4`.
3. Mở ảnh `output/stier/<slug>/final_sheet.jpg` và soi:
   - chữ tiếng Việt đủ dấu, nhất là "ì", "đ", "ậ", "ữ";
   - nhãn hoặc chữ không bị cắt ở mép;
   - không có logo, chữ thương hiệu hay giao diện ứng dụng đọc được;
   - không có mặt người rõ ở cảnh nói về một nghề hay một người thật;
   - chữ không bị một khung đóng riêng một từ;
   - cảnh mở đầu nêu ý chính ngay từ giây 0.
4. Có lỗi thì sửa **chỉ** `data/stier/specs/<slug>.json` rồi render lại. Được sửa: đổi clip, vị trí, `acc`.
   - Tìm clip bằng `python motion/stier/clips.py search "<từ khoá>" --src pexels --n 8`, xem bảng poster trước khi chọn.
   - **Không đổi lời đọc, không đổi số liệu.**
   - Mỗi bài render lại tối đa 2 lần. Quá 2 lần mà vẫn lỗi thì ghi vào báo cáo và chuyển bài kế tiếp.

## Ràng buộc

- Mỗi bài dài 25–35 s.
- Chênh thời lượng trong cặp không quá ±3 s. Bài p1 dài 31,8 s. Các cặp là p1/p2, p3/p4, p5/p6.
- Không đăng, không enqueue, không gọi YouTube API, không chạy git.
- Không sửa code trong `motion/` hay `factory/`.

## Báo cáo

Ghi vào `docs/pm/tickets/YCV-im1r-render-report.md`:
- bảng gồm các cột: slug, thời lượng, số lần render, lỗi đã thấy và đã sửa, lỗi còn lại;
- đường dẫn `final_sheet.jpg` của từng bài.
