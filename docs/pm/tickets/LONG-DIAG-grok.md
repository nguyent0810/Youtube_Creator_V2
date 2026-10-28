# Ticket YCV-cimp · Grok · Vì sao Long MIM và CK gần như không có lượt xem?

**Chỉ đọc và phân tích.**
- Không sửa code, không mở trình duyệt, không gọi API, không chạy git.
- Chỉ được ghi một file: `docs/pm/tickets/LONG-DIAG-report.md`.
- Được chạy python để tính toán trên các file dưới đây.

## Dữ liệu

Studio xuất ngày 28/10/2026, số liệu tới 26/10. Mỗi kênh có:
- `videos.csv`: một dòng mỗi video, có cột theo kỳ, `format` (short hoặc long, quy ước ≤180 s là short), `age_days`;
- `raw/videos__{7d,28d,90d,365d,lifetime}/table.csv`: views, giờ xem, sub, impressions, CTR, thời lượng xem trung bình, % xem trung bình;
- `raw/traffic_source__*`;
- `summary.md`.

Thư mục:
- CK: `output/webauto/studio/UCseQ5p0-e0_DW35M__d_oHg/2026-10-28/`
- MIM: `output/webauto/studio/UCb1WzhRnuTEsW8QhF7WdCQw/2026-10-28/`
- Lịch đăng: `output/webauto/studio/upload_log_ck_mim.csv` (`publish_at` là giờ UTC; slug bắt đầu bằng `long-` là Long).

Lưu ý: nhiều Long trong log đang private và có hẹn giờ; chỉ Long đã public mới có số liệu. Chiến lược Long hiện tại: `docs/pm/briefs/` và mục "Long" trong `docs/codex/long-rules.md`.

## Câu hỏi

1. **Bảng Long đã public của mỗi kênh**, mỗi Long một dòng: ngày đăng, thời lượng, impressions, CTR, views, thời lượng xem trung bình, % xem trung bình, sub, nguồn traffic chính (nếu tách được).
2. **Phân loại vấn đề của từng Long:**
   - (a) ít lượt hiển thị: YouTube không đưa ra;
   - (b) có hiển thị nhưng CTR thấp: lỗi tiêu đề hoặc thumbnail;
   - (c) có người bấm nhưng giữ chân kém: lỗi mở đầu hoặc nội dung.

   Dùng ngưỡng rõ ràng và nói rõ ngưỡng lấy từ đâu. Thiếu dữ liệu thì ghi "không đủ dữ liệu".
3. **So với Short cùng kênh:** CTR, % xem. Long có nhận lượt xem từ Short ("Shorts" / "SHORTS_CONTENT_LINKS") không?
4. **Giờ xem Long public tích luỹ** trong 365 ngày của mỗi kênh. So với mốc 4.000 giờ của YPP; giờ xem Short trên feed không được tính.
5. **Ba giả thuyết chính**, mỗi cái kèm số ủng hộ, số phản bác, và cách kiểm tra trong 2 tuần.

## Báo cáo

Viết bằng tiếng Việt, 60–120 dòng, ưu tiên bảng. Mỗi số phải ghi lấy từ file nào, cột nào. Không suy đoán vượt dữ liệu; mẫu nhỏ thì nói rõ.

Mục cuối là **"Đề xuất cho 2 tuần tới"**: tối đa 3 việc, mỗi việc có chỉ số đo được.
