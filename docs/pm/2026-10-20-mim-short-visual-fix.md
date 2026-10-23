# Sửa hình ảnh Short MIM mẫu `mim-gpu-55-lan-2009` (20/10/2026)

Chủ kênh xem bản mẫu: "chưa hấp dẫn, cần sửa". Phần này chỉ về hình ảnh, engine và clip. Lời đọc và số liệu giữ nguyên, không upload, không đụng state.sqlite.

## Nguyên nhân gốc
1. **Biểu đồ trống.** Spec dùng `chart` với hai cột 1 và 55. Cột "1" chỉ cao vài px, cột 55 chỉ hiện ở chữ "năm" nên 5 giây đầu của cảnh là một đường kẻ và một con số "1". Engine lại giới hạn biểu đồ trong khung y 560–1150 và cỡ số trên cột tối đa 76 px, nên số 55 nhỏ và mờ, nửa màn hình bỏ trống. Chọn sai cảnh: dữ kiện "gấp 55 lần" là một con số, không phải hai đại lượng cần so cột.
2. **Clip nền không liên quan.** `pexels:3147349` là thùng máy tính tối tím (RGB), `pexels:854969` là thùng máy mở, đầu clip tối đen. Không nói gì về học sâu hay card đồ hoạ trong nghiên cứu, chỉ là "cảnh máy tính chung chung".
3. **Khoảng đen đầu cảnh vòng tròn.** Cửa sổ `win` của look "circle" cắt ra một vòng tròn nhỏ; clip 854969 mở đầu bằng cảnh tối nên vòng tròn đen khoảng 1 giây.
4. **Nhãn "VIDEO MINH HOẠ".** Do spec ghi `winLabel`; không có giá trị cho người xem, và ghi công đã nằm trong mô tả.
5. **Cấu trúc nghèo so với các Short giữ chân tốt** (`mim-shannon-1951`, `mim-teaser-nuoc-78`, `mim-ai-bia`): họ dùng 8–13 cảnh, chữ lớn, bộ đếm số lớn, sổ liệt kê, ít clip. Bản mẫu chỉ có 5 cảnh, trong đó 2 cảnh clip chiếm hơn 60% thời lượng.

## Thay đổi
- **Spec** `data/stier/specs/mim-gpu-55-lan-2009.json` (bản gốc trước khi sửa lưu ở scratchpad; bản trong `docs/pm/tickets/.../specs-T4/` không đụng):
  - Chart được thay bằng cảnh `counter` đếm từ 1 lên 55 "×" đúng lúc đọc "card chạy nhanh hơn tới năm mươi lăm lần", nhãn "LẦN NHANH HƠN CPU 2 LÕI".
  - Thêm cảnh `ledger` "HAI BÊN SO TÀI" (card đồ hoạ so với CPU 2 lõi) cho câu "Họ đem so với một bộ xử lý hai lõi".
  - Clip nền đổi sang cận cảnh bo mạch/chip (`pexels:6755168`, `pexels:6755162`): tông xanh đen lạnh khớp theme, có nội dung chuyển động ngay từ giây đầu, không logo/chữ/tên công ty.
  - Cảnh cuối bỏ cửa sổ vòng tròn và nhãn "VIDEO MINH HOẠ", dùng clip tràn khung với màn che 0,5.
  - Mix: G, M, D, D, T, M (M 50%, qua mix_lint).
- **Engine** `motion/hf/assets/engine/casefile.js`, cảnh `chart`: chỉ khi `theme-mim` thì khung biểu đồ mặc định cao hơn (y 470–1300 thay 560–1150), số trên cột tối đa 170 px (thay 76) và đặt cao hơn. CK và case không đổi một byte nhánh chạy (điều kiện `TH.cls === "theme-mim"`); chưa dựng lại Short CK vì đây chỉ là nhánh rẽ theo theme. Biểu đồ MIM đã đăng không bị dựng lại.

## Điều còn yếu
- Cảnh `counter` và `ledger` dùng nửa trên khung; nửa dưới (y 1000–1450) vẫn khá trống. Muốn sửa hẳn phải thêm tuỳ chọn căn giữa dọc cho counter (engine chung) — chưa làm.
- Cảnh clip đầu vẫn là chữ trên clip chung chung (bo mạch), chưa có hình tư liệu về Stanford hay nghiên cứu (không có ảnh PD phù hợp).
- Chart 1 so với 55 vẫn không nên dùng cho hai đại lượng chênh quá lớn; khi dùng nên đặt cột lớn vào đúng lúc lời đọc nêu nó.
