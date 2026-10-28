# CK: dựng Long thế nào cho hấp dẫn (thư viện FS/BUD + báo cáo đối thủ)

Ngày 27/10/2026. Nguồn:
- Thư viện FS/BUD, nhánh `feat/library-inventory` (8d0069c). Hồ sơ thử `ck.yaml` đặt Long CK ở trạng thái thua với 4 lý do: `ctr`, `hook`, `nhip`, `hinh`.
- Báo cáo đối thủ của Muse: `docs/pm/2026-10-27-ck-doi-thu-muse.md`.
- Đếm loại cảnh của 20 Long CK đã dựng.

## 1. Vấn đề lớn nhất: kênh tên "Biểu Đồ Biết Nói" nhưng phần lớn là thẻ chữ

Trong 1.468 cảnh của 20 Long CK:

| Nhóm | Loại cảnh | Tỉ lệ |
|---|---|---|
| **Thẻ chữ** | kinetic 393, question 133, slam 103, myth 35… | **khoảng 45%** (32–62% mỗi bài) |
| **Biểu đồ thật** | bars 116, counter 66, candles 35, race 23, units, dots | **khoảng 18%** |
| Sổ mô-típ | ledger 218 | 15% |
| Clip và ảnh | broll, photo | 3–13% |

Các bài có nhiều thẻ chữ nhất là 2026 kênh đầu tư (59%), FOMO (62%) và vàng đỉnh (57%). Đây cũng là nhóm có CTR và thời gian xem thấp nhất.

Engine `casewide.js` đã có sẵn `race`, `dots`, `units`, `split`, `calendar`, `breadth`, `basket`, nhưng gần như chưa bài nào dùng.

## 2. Quy tắc dựng cho lô Long CK từ 18/11

| # | Quy tắc | Thẻ thư viện / nguồn | Chữa lý do |
|---|---|---|---|
| 1 | **Cảnh đầu tiên là biểu đồ của chính con số hứa trong tiêu đề, hiện trước giây 15.** Không mở bằng thẻ chữ | `hook_frame_dau_la_thumbnail`; Muse: "biểu đồ ở giây 5–15" | hook |
| 2 | **Một biểu đồ chính lớn dần qua các chương.** Ví dụ: tiền của nhân vật cộng dồn qua từng chương, tương tự `ledger` nhưng là hình. Ở chương kết, biểu đồ hiện đầy đủ | `object_continuity` (đã thử ở MIM Macintosh) | nhịp |
| 3 | **Biểu đồ thật ≥ 35% số cảnh, thẻ chữ ≤ 25%**, không quá 2 thẻ chữ liền nhau | `hook_doi_nhip`: mỗi lần đổi cảnh phải mang thông tin mới | hình, nhịp |
| 4 | **Khoanh đúng điểm đang đọc trên biểu đồ** (vòng khoanh + nhãn ngắn, phần còn lại tối đi) | `highlight_callout` (xếp hạng 1 khi chạy `rank`) | hình |
| 5 | **Đường vẽ dần theo lời đọc** cho số liệu theo năm | `line_draw` | hình |
| 6 | **Mỗi Long có một vòng mở chính**, đóng ở chương cuối. Ví dụ: "con số cuối cùng không phải X mà là Y" | `hook_vong_mo` | hook |
| 7 | **Tiêu đề:** khoản tiền × mốc thời gian × nhóm người, kèm nghịch lý. Không dùng các từ "sập, toang, xoá sổ" | `chude_khoan_tien_cu_the`, `chude_neo_nhom_hep`; Muse | ctr |
| 8 | **Thumbnail có một tiêu điểm:** một con số lớn + một biểu đồ nhỏ, tối đa 3 chữ. Chữ trên thumbnail thêm nghĩa mới, không lặp tiêu đề | `thumb_mot_tieu_diem`, `thumb_it_chu_them_nghia` | ctr |

## 3. Engine còn thiếu gì

Theo thẻ thư viện, cả 4 renderer dưới đây đều thuộc loại `cong: thap` (công thấp). Engine hiện chưa có renderer nào:

| Renderer mới | Dùng cho | Bài cần |
|---|---|---|
| `line` | Đường vẽ dần + khoanh điểm (`line_draw` + `highlight_callout`) | Mọi bài có số theo năm |
| `waterfall` | Thác chi phí: tổng tiền bị trừ dần qua từng khoản | Viện phí, trợ cấp thất nghiệp, chi tiêu gia đình |
| `heat` | Lịch nhiệt 12 tháng | Tiền mừng cưới |
| `stack` | Cột xếp chồng (vợ / chồng / quỹ chung) | Chi tiêu gia đình |

Cả 4 chỉ là **thêm** renderer vào `casewide.js`, không sửa renderer cũ, nên không ảnh hưởng CL và MIM.

Codex không được sửa engine. Claude dựng 4 renderer này trước vòng W2 (dựng cảnh) của lô CK, rồi bổ sung chữ ký của chúng vào cheatsheet.

## 4. Đo

- Đăng ký ô thử thư viện `LIB-CK1`:
  - khuôn: `long_ck_giao_duc`;
  - kỹ thuật: `highlight_callout`, `line_draw` và quy tắc #1–#3;
  - đối chứng: 4 Long CK E4–A2 (11–16/11), dựng theo kiểu cũ.
- Đo vào **ngày 09/12** (14 ngày sau bài cuối, 25/11). Chỉ số: CTR, giữ chân 60 giây, thời gian xem trung bình.
- Ngưỡng thắng: CTR ≥ 3% và giữ chân 60 giây cao hơn đối chứng ít nhất 10 điểm.
