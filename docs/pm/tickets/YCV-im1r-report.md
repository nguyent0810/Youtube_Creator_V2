# Báo cáo YCV-im1r

## Trạng thái

Đã sửa p1 và tạo đủ sáu spec MIM. Sáu lệnh `--no-render` chạy sạch sau khi chỉnh cảnh, giới hạn chữ và thời lượng. Không có thao tác đăng, enqueue, YouTube API hoặc git.

| Slug | Số chữ | Thời lượng giọng | `final.mp4` |
|---|---:|---:|---|
| `mim-p1-quang-cao-giong-gia` | 122 | 30,84 s | Chưa tạo — `output/stier/mim-p1-quang-cao-giong-gia/final.mp4` |
| `mim-p2-tin-nhan-thoai` | 123 | 32,62 s | Chưa tạo — `output/stier/mim-p2-tin-nhan-thoai/final.mp4` |
| `mim-p3-nghe-nhap-lieu` | 134 | 33,02 s | Chưa tạo — `output/stier/mim-p3-nghe-nhap-lieu/final.mp4` |
| `mim-p4-ilo-2023-van-phong` | 129 | 31,10 s | Chưa tạo — `output/stier/mim-p4-ilo-2023-van-phong/final.mp4` |
| `mim-p5-recsys-2016` | 108 | 29,26 s | Chưa tạo — `output/stier/mim-p5-recsys-2016/final.mp4` |
| `mim-p6-feed-cua-ban` | 119 | 32,14 s | Chưa tạo — `output/stier/mim-p6-feed-cua-ban/final.mp4` |

Chênh lệch giọng trong từng cặp: p1/p2 1,78 s; p3/p4 1,92 s; p5/p6 2,88 s. Tất cả nằm trong 25–35 s và ±3 s.

## Cảnh và footage Pexels

Đã xem các poster sheet khi chọn footage. Chỉ dùng cảnh trừu tượng/dữ liệu/thiết bị, không có người thật, logo hoặc chữ thương hiệu đọc được.

| Slug | Clip đã dùng |
|---|---|
| `mim-p1-quang-cao-giong-gia` | `pexels:39687575`, `pexels:34337855`, `pexels:37342578`, `pexels:34336609` |
| `mim-p2-tin-nhan-thoai` | `pexels:39687575`, `pexels:34337855`, `pexels:37342578` |
| `mim-p3-nghe-nhap-lieu` | `pexels:34336609`, `pexels:34550739`, `pexels:16863222` |
| `mim-p4-ilo-2023-van-phong` | `pexels:34550739`, `pexels:34342666`, `pexels:39459371` |
| `mim-p5-recsys-2016` | `pexels:34337855`, `pexels:37342578` |
| `mim-p6-feed-cua-ban` | `pexels:34336609`, `pexels:34578211`, `pexels:39463971` |

P1 đã được đổi từ ba cảnh M liên tiếp thành M–T–M ở ba cảnh đầu, nên qua luật mix. P3 giữ `0,70 / 1`, không hiển thị thành 70%. P6 gắn rõ `THEO YOUTUBE · 2021`, `SỐ LIỆU YOUTUBE TỰ CÔNG BỐ` và `THEO TIKTOK · 2020` tại các cảnh nêu số liệu của hãng.

## Khác với bản script

- Rút mọi tiêu đề còn tối đa 57 ký tự để đạt luật tiêu đề ≤60 ký tự. Dữ kiện không đổi.
- P2 rút các từ đệm ở câu mở, giới thiệu VALL-E và lời khuyên FBI để còn 123 chữ, đồng thời vẫn giữ 3 giây, 15 giây, trạng thái chưa phát hành rộng rãi và lời khuyên gọi lại số đã lưu.
- P3 rút câu mở thành “Bạn làm nhập liệu”, dùng `427` trên lời đọc để đủ giới hạn 134 chữ; vẫn giữ điểm 0,70/1 và rào “không phải 70%”.
- P6 bỏ cụm “Điểm mấu chốt” để chênh thời lượng với p5 không quá 3 giây.

Không có khẳng định nào trong lời đọc không có dòng factcheck. Riêng vụ Johansson dùng nguồn Variety [SECONDARY] như kịch bản; kết quả pháp lý chưa kiểm được đã không được nói.

## Cổng đã chạy và lỗi còn lại

- Đã chạy `python motion/stier/build.py <slug> --no-render` cho cả sáu slug sau lần sửa cuối; tất cả qua lint phối cảnh và sinh composition/timing/voice.
- Đã thử render tuần tự p1 bằng `python motion/stier/build.py mim-p1-quang-cao-giong-gia` ba lần: cache npm mặc định, cache tạm trong workspace, rồi cache tạm offline. Cả ba đều hỏng trước render do `npm`/hệ điều hành trả `EPERM` (`spawn EPERM`; lần đầu còn không mở được npm cache hệ thống). Đây là lỗi môi trường render, không phải lỗi lint spec.
- Vì chưa sinh được MP4, chưa thể chạy `motion/long/clip_sheet.py` hoặc tự soi sheet; clip sheet: chưa có. Thumbnail không thuộc phạm vi ticket Short này.
- Lỗi còn lại duy nhất: render HyperFrames/npm bị `EPERM`; sáu `final.mp4` chưa tồn tại.
