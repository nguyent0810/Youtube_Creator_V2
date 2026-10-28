# Ticket YCV-8ted · agy · Vì sao lượt xem CK 7 ngày giảm 78%?

**Chỉ đọc và phân tích.** Không sửa code, không chạy trình duyệt, không gọi YouTube API.
Chỉ được viết một file: `docs/pm/tickets/YCV-8ted-report.md`.

## Dữ liệu

Studio xuất ngày 28/10/2026, số liệu tới 26/10.

**CK** (Biểu Đồ Biết Nói): `output/webauto/studio/UCseQ5p0-e0_DW35M__d_oHg/2026-10-28/`
- `summary.md`, `summary.json`, `videos.csv`
- `raw/<báo cáo>__<kỳ>/*.csv`, gồm: daily, videos, traffic_source, content_type, youtube_product, device, subscription_source…

**MIM** để so sánh: `output/webauto/studio/UCb1WzhRnuTEsW8QhF7WdCQw/2026-10-28/`

**Thêm:**
- Lịch đăng thật: `output/webauto/studio/upload_log_ck_mim.csv` (xuất từ bảng `upload_log`; `publish_at` là giờ UTC).
- Bối cảnh: `docs/pm/2026-10-28-pilot-short-hook.md` mục 1–2 (baseline 28 ngày).

## Câu hỏi

1. **Mức giảm.** Ngày nào bắt đầu giảm? Giảm ở Short hay Long? So với MIM cùng kỳ.
2. **Nguồn lưu lượng.** Nguồn nào mất nhiều nhất (Shorts feed, tìm kiếm, đề xuất, kênh)? So 28 ngày với toàn thời gian. Nếu chỉ có hai kỳ này thì nói rõ là không tách riêng được 7 ngày.
3. **Short mới.** Short đăng trong 7–10 ngày gần nhất có được hiển thị không?
   - So views của 3 ngày đầu với các Short đăng 14–20/10.
   - Theo lịch `upload_log`, mỗi ngày đăng bao nhiêu bài.
   - Có ngày nào đăng dồn không?
4. **Bài kéo view.** Vài bài viral đầu tháng có phải là phần lớn lượt xem của tuần trước, và tuần này chỉ là trở về mức bình thường?
   - Dùng `videos.csv`: views 7 ngày, 28 ngày, tuổi video.
5. **Giả thuyết.** Xếp giả thuyết theo bằng chứng:
   - hết đợt viral;
   - phân phối Short mới giảm;
   - đổi chủ đề hoặc khuôn;
   - lịch đăng;
   - hạn chế hoặc giới hạn upload.

   Mỗi giả thuyết ghi rõ: số ủng hộ, số phản bác, và cái gì cần thêm để kiểm. Ví dụ: chỉ số "xem / lướt qua" trong Studio, hiện chưa xuất được.

## Báo cáo

Viết bằng tiếng Việt, dài 60–120 dòng, ưu tiên bảng. Mọi số phải trích từ file nào, cột nào. Không suy đoán vượt dữ liệu.

Mục cuối là **"Ảnh hưởng tới pilot CK 07–12/11"**: mốc so sánh nào còn dùng được.
