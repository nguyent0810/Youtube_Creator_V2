# Retro lô pilot MIM 13–18/11 (YCV-im1r) · Grok

**Chỉ đọc và phân tích.**
- Chỉ được ghi một file: `docs/pm/2026-10-28-retro-mim-pilot-short.md`.
- Không sửa code, không gọi API, không chạy git.

## Đã đăng

Sáu bài đều private, hẹn giờ 15:00 VN:

| Bài | Video | Ngày đăng |
|---|---|---|
| p1 | GkskSEnDiyI | 13/11 |
| p2 | 4ZOrJGfxG0g | 14/11 |
| p3 | BP6cmcFTDUs | 15/11 |
| p4 | l_4DmvqWlGA | 16/11 |
| p5 | 0SzJIAebHR4 | 17/11 |
| p6 | b-GUkOrAcc0 | 18/11 |

## Tư liệu

- Ticket: `.tickets/YCV-im1r.md` (các note theo thời gian).
- Kịch bản và factcheck:
  - `docs/pm/pilot-short/mim-pilot-scripts.md`
  - `docs/pm/pilot-short/mim-pilot-1318-factcheck.md`
- Brief và báo cáo của từng vòng: `docs/pm/tickets/YCV-im1r-*.md` (Codex vòng 1 và vòng 2, agy render).
- Spec cuối: `data/stier/specs/mim-p[1-6]-*.json`.
- Review bài mẫu của ChatGPT: chủ kênh dán vào chat. Ý chính:
  - hook yếu;
  - nhiều cảnh chữ tĩnh trên nền tối;
  - câu kết chưa đắt.
- Retro trước, để so cách viết: `docs/pm/2026-10-28-retro-ck-pilot-short.md`.

## Sự cố trong lô này

Mỗi sự cố đều có trong note ticket hoặc trong báo cáo:

1. Codex không render được: sandbox chặn npm cache và chặn spawn tiến trình.
2. Clip mở đầu bài p1 trông như sinh vật, không liên quan nội dung.
3. Clip "hậu trường" của p1 có một phụ nữ thật, dễ bị hiểu là Scarlett Johansson.
4. Từ "không" nằm trong danh sách `acc`, nên chữ "KHÔNG" bị đóng khung riêng.
5. Vòng 2, Codex viết câu mở p6 (hook B) bắt đầu bằng "Theo YouTube năm 2021". Mở như vậy là kiểu hook A, làm hỏng biến thử.
6. Câu mở p2 đọc khó và gần như ngụ ý "3 giây là đủ cho kẻ gian".
7. Agy phát hiện:
   - clip lộ giao diện ứng dụng hoặc mặt người trên màn hình điện thoại (`pexels:38410501`, Codex dùng ở 4 bài);
   - nút trên board xếp ngang bị đè lên nhau;
   - clip terminal có chữ đọc được.
8. p6 có cảnh biểu đồ một cột, khung hình gần như trống khoảng 3 giây. Đã đổi sang `counter`.

## Yêu cầu

Viết retro bằng tiếng Việt, 50–90 dòng. Với mỗi sự cố, ghi:
- nguyên nhân gốc;
- cổng tự động nào lẽ ra phải chặn được;
- đề xuất chốt chặn cụ thể: tên file hoặc hàm, kiểm tra gì, ví dụ test.

Ưu tiên những chốt máy làm được, để agent sau không lặp lại lỗi. Ví dụ:
- lint "hook B không được mở bằng 'Theo …'";
- danh sách đen các clip Pexels đã thấy lỗi;
- `board` có 3 nút trở lên thì bắt buộc xếp dọc;
- `acc` không chứa từ phủ định.

Cuối file viết mục **"Đổi gì trong brief cho agent"**: tối đa 5 dòng.
