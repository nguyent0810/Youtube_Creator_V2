# Kết quả T2A — nghiên cứu `mim-turing-bombe`

Ngày thực hiện: 26/10/2026.

## Đã làm

- Đã đọc `AGENTS.md` và các tài liệu quy trình Long được nêu trong đó, đặc biệt phần các lỗi thử nghiệm trước đây.
- Đã tạo kho nghiên cứu [facts.md](../../../../data/long/mim-turing-bombe/facts.md) theo đúng phạm vi ticket: **34 dữ kiện**, chia đủ 8 chương, mỗi chương 4–5 dữ kiện.
- Phân loại: **33 dữ kiện mạnh**, **1 dữ kiện vừa** (số 34, sự khác biệt của phim; chỉ được đọc kèm quy dẫn *Time*).
- Đã mở các nguồn GCHQ, The National Archives, DPMA, Agencja Wywiadu Ba Lan, Đại học Adam Mickiewicz, TNMOC, NSA và *Time*. Mỗi dữ kiện trong kho có URL và tên trang nguồn.
- Đã kiểm trực tiếp trường `LicenseShortName` cho 11 ảnh Commons: 8 Public domain và 3 CC0; không có CC BY-SA, GFDL, NC hoặc ND.
- Đã ghi 10 ứng viên Pexels có URL, mô tả và điều kiện bắt buộc soi logo/chữ bằng clip sheet trước khi dùng.

## Lệnh đã chạy và kết quả

| Lệnh / thao tác | Kết quả |
|---|---|
| Đọc `AGENTS.md`, ticket T2A, README/RETENTION/SOURCES và các ghi chú PM | Đã hoàn tất trước khi nghiên cứu. |
| Truy vấn, mở và đối chiếu các nguồn lịch sử chính thống trên web | Đã hoàn tất; danh sách URL nằm ngay ở từng dữ kiện trong `facts.md`. |
| Truy vấn Commons API qua hàm đọc `imageinfo()` để lấy `LicenseShortName` | 11/11 ảnh hợp lệ: Public domain hoặc CC0. |
| `python scripts/long_gate.py mim-turing-bombe --min-syl 1900` | **Không chạy**: ticket T2A là ticket nghiên cứu và ghi rõ bỏ qua cổng này. |

## Không làm (đúng yêu cầu ticket)

- Không sửa `script.md`, `factcheck.md`, `gen_scenes.py`, `spec.json` hay bất kỳ `ch*.json` nào.
- Không chạy TTS, HTML, render, final, thumbnail hoặc clip sheet.
- Không upload/sửa/xóa bất cứ nội dung YouTube nào, không đọc credential, không ghi `state.sqlite`, không dùng lệnh git.

## Lỗi lint còn lại

Không áp dụng: ticket chỉ nghiên cứu và không cho chạy các bước dựng/lint. Không phát hiện lỗi engine vì không động vào engine.

## Khẳng định chưa kiểm được / cần tránh

- Không đọc “Victory là Bombe đầu tiên chạy tháng 03/1940” hay một ngày chạy cụ thể: GCHQ đã mở chỉ xác nhận Bombe Anh đầu tiên chạy kịp Blitzkrieg ở Tây Âu; TNMOC nêu Agnus Dei/Agnes hoạt động tháng 08/1940.
- Chưa có nguồn mạnh đã mở cho Doc Keen, kích thước máy, số trống thời chiến, thời gian một lượt chạy, hay các crib cụ thể như `Keine besonderen Ereignisse`/bản tin thời tiết.
- Không tự nêu số tàu, thương vong hoặc số tháng rút ngắn chiến tranh; dữ kiện định lượng duy nhất chỉ là nhận định của “nhiều sử gia” theo NSA và đã được đánh dấu phù hợp.

## Cold open đề xuất

Đặt người xem vào đêm 21/10/1941: bốn nhà giải mã, có Alan Turing, tự gửi thư vượt cấp cho Churchill vì các Bombe đã tạo ra một nút thắt nhân lực. Đó là căng thẳng thật, có ngày, người, hậu quả rõ và dẫn tự nhiên đến câu hỏi: **một cỗ máy quay nhanh đến đâu mà vẫn cần cả một hệ thống người để biến điểm dừng thành tin tình báo?** Nguồn mạnh: [The National Archives](https://www.nationalarchives.gov.uk/explore-the-collection/stories/a-dramatic-plea-for-churchills-help/).

## Clip sheet và thumbnail

Không có, đúng phạm vi ticket nghiên cứu. Pha dựng sau phải tải lại ứng viên, tạo clip sheet và kiểm tra logo/chữ trước khi chọn; thumbnail chưa được tạo.
