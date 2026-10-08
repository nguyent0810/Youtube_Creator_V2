# Runbook: thay video Lịch sai dữ kiện (N1)

Cập nhật 08/10/2026. Đọc kèm `docs/AUDIT-2026-10-08.md`, mục N1.

## 1. Chuyện gì đã xảy ra

Cả 92 bundle Lịch FS (01/10 → 31/12/2026) được sinh khi `vnlunar` là bản 1.0.3/1.0.4. Mã cũ tin trường `12_gods` của thư viện, mà trường này sai. Mã hiện tại tính Trực và 12 thần độc lập, đối chiếu với `vnlunar==1.0.5` và **dừng** nếu hai bên lệch nhau.

Kết quả đối chiếu lại 92 kịch bản đã sinh:

| Sai gì | Số ngày / 92 |
|---|---|
| Trực | 92 |
| Danh mục việc nên làm / kiêng (theo trực sai) | 90 |
| Sao 12 thần | 62 |
| Gọi "hoàng đạo"/"hắc đạo" sai | 38 |
| Hướng Tài thần | 31 |
| Số việc nói ra ("chỉ được ba việc") | 30 |
| Tú tốt/xấu | 5 |

Không ngày nào đúng hoàn toàn. Hôm nay (08/10), các video 01–09/10 đã lên sóng. Từ 10/10 trở đi (83 video) vẫn đang hẹn giờ, chưa phát.

## 2. Chuẩn bị (một lần)

1. Kéo nhánh có bản sửa và cài đúng phụ thuộc. Cài vào **cả venv chạy script lẫn venv TTS** (`PY_TTS` trong `run_pipeline.py`), vì `make_lich_month.py` chạy bằng venv TTS:
   ```
   pip install -e .
   ```
   Hoặc tối thiểu: `pip install vnlunar==1.0.5`.
2. Kiểm nhanh:
   ```
   python -m pytest -q
   ```
   Nếu `vnlunar` không phải 1.0.5, mọi lệnh Lịch sẽ dừng với `LunarMismatch`. Dừng như vậy là đúng ý đồ: không sinh, không thay gì khi nguồn đối chiếu lệch.

## 3. Thay 83 video chưa lên sóng

**Làm càng sớm càng tốt: cứ mỗi ngày chậm là thêm một video sai lên sóng lúc 06:00.**

1. Xem kế hoạch (chạy khô, không đổi gì, chỉ đọc YouTube):
   ```
   python scripts/replace_lich.py --channel FS
   ```
   Kết quả mong đợi khi chạy trong ngày 08/10:

   | Nhóm | Số video |
   |---|---|
   | ĐÃ PHÁT (01–09/10) | 9 |
   | THAY (10/10 → 31/12) | 83 |

   Cuối bản in, dòng `LÔ THAY` phải kết thúc bằng `ĐẠT`: lô bundle mới đã qua kiểm chéo. Nếu là `CẦN SỬA` thì công cụ dừng, không làm gì.
2. Làm thật:
   ```
   python scripts/replace_lich.py --channel FS --apply
   ```
   Lệnh này làm, theo đúng thứ tự:
   - Gỡ lịch từng video cũ: chuyển sang private, bỏ giờ hẹn, thêm `[ĐÃ THAY]` vào đầu tiêu đề.
   - Cất bundle cũ vào `archive/bundles/FS/` (kèm video_id cũ).
   - Ghi bundle mới.
   - Đưa item về `pending` với **đúng giờ hẹn cũ**.

   Nếu lệnh dừng giữa chừng (mất mạng, hết quota), chạy lại đúng lệnh đó: ngày đã xong sẽ hiện ĐÚNG, ngày dở dang hiện KHÔI PHỤC và được làm nốt.
3. Dựng và đăng bản mới:
   ```
   python scripts/run_pipeline.py resume --channel FS
   python scripts/verify_published.py --channel FS
   ```
   Hàng đợi chạy theo giờ hẹn, gần nhất trước. Hết quota ngày thì item tự hoãn tới giờ reset (14:00 hoặc 15:00 VN, tuỳ giờ mùa hè ở Mỹ); chạy `resume` lại sau mốc đó.
4. Dọn video cũ: trong YouTube Studio, lọc tiêu đề `[ĐÃ THAY]`, kiểm vài video, rồi xoá hàng loạt. Công cụ cố ý **không xoá** video, vì xoá là vĩnh viễn.

Các nhóm khác có thể gặp, tuỳ thời điểm chạy:
- **THAY-SÁT:** còn dưới 12 giờ là lên sóng. Vẫn thay, vì thà trống slot còn hơn phát lịch sai. Muốn chừa lại thì thêm `--keep-near`; đổi ngưỡng bằng `--lead <giờ>`.
- **GỠ:** video cũ còn hẹn nhưng không kịp đăng bản thay. Công cụ chỉ gỡ lịch và đánh dấu item bị loại.
- **LỠ:** giờ hẹn đã qua mà video không công khai. Công cụ để yên.
- **KHÔNG DỰNG:** kịch bản mới không qua đối chiếu. Công cụ để yên; cần xem tay phần báo cáo in kèm.

Chỉ làm một đoạn ngày: `--from 2026-10-20 --to 2026-11-30`.

## 4. Chín video đã phát (01–09/10)

Công cụ **không đụng** video đã công khai. Đây là quyết định của chủ kênh. Bảng dưới là các ngày đó (sao · trực):

| Ngày | Video đã nói | Đúng là | Sai thêm |
|---|---|---|---|
| 01/10 | Kim Quỹ · Trực nguy | Bạch Hổ · Trực bế | hoàng/hắc đạo, việc |
| 02/10 | Thiên Đức · Trực thành | Ngọc Đường · Trực kiến | việc, số việc, tú |
| 03/10 | Bạch Hổ · Trực thu | Thiên Lao · Trực trừ | việc, số việc, Tài thần |
| 04/10 | Ngọc Đường · Trực khai | Huyền Vũ · Trực mãn | hoàng/hắc đạo, việc |
| 05/10 | Thiên Lao · Trực bế | Tư Mệnh · Trực bình | hoàng/hắc đạo, việc |
| 06/10 | Huyền Vũ · Trực kiến | Câu Trần · Trực định | việc, số việc, Tài thần |
| 07/10 | Tư Mệnh · Trực trừ | Thanh Long · Trực chấp | việc, Tài thần |
| 08/10 | Câu Trần · Trực mãn | Minh Đường · Trực chấp | hoàng/hắc đạo, việc, số việc, Tài thần |
| 09/10 | Thanh Long · Trực bình | Thiên Hình · Trực phá | hoàng/hắc đạo, việc |

Có hai cách xử lý:
- **(A) Chuyển sang private trong Studio (khuyến nghị).** Các ngày này đã qua nên video không còn giá trị xem lại. Để công khai thì thông tin sai còn nằm trên kênh. Private đảo ngược được bất cứ lúc nào.
- **(B) Để công khai, ghim bình luận đính chính** theo bảng trên. Cách này giữ lượt xem, nhưng ít người đọc bình luận ghim trên Shorts.

Danh sách video_id: xem nhóm ĐÃ PHÁT trong bản in của bước 3.1.

## 5. BUD: "Vì sao tượng Phật có dái tai dài?" (30/10)

Kênh BUD đã có một video **cùng nguyên tiêu đề**, do nguồn khác đăng (ghi nhận trong `factory/lines/novelty.py`).
- **Mã cũ:** sẽ "nhận" video đó thay cho bundle `bud-visao-dai-tai-dai`, nên ngày 30/10 không có video của v2.
- **Mã mới:** `publish_batch` LOẠI item này (`DuplicateTitle`), không upload, không nhận video lạ. Không cần làm gì.

Khuyến nghị: **để nó bị loại.** Đổi tiêu đề không giải quyết được gì, vì kênh đã có video cùng chủ đề, và đăng lặp chủ đề là đúng thứ bộ chống trùng ngăn. Muốn lấp slot 30/10 thì sinh một bài BUD khác.

## 6. Sau này

- `make_lich_month.py` và `replace_lich.py` dựng bundle bằng cùng một hàm (`factory/lich.py`), nên bản "thay" và bản "sinh" luôn giống nhau.
- Đã sửa cách chọn biến thể câu mở (`factory/compose.py`): offset theo số ngày tuyệt đối thay vì theo ngày trong tháng. Bản cũ cho 09/11 và 03/12/2026 ra kịch bản **trùng nguyên văn**. Kiểm chéo từng tháng không thấy, nhưng lô thay 83 ngày thì thấy. Giờ trên 2026-10 → 2028, hai kịch bản giống hệt nhau cách nhau ít nhất 360 ngày.
- **Danh mục "nên làm/kiêng"** vẫn là bản cổ mà kênh đã dùng (ghim trong `factory/vocab.py`, `TRUC_VIEC`). `vnlunar` 1.0.5 đã thay bằng câu diễn giải hiện đại, có chỗ ngược bản cổ (vd Trực kiến và động thổ). Nếu muốn theo bản mới thì đây là quyết định nội dung, cần sửa `TRUC_VIEC`.
