# W1c-4 — Kết quả sửa mở đầu `ck-f4-vo-chong-chia-tien`

## Đã làm

- Giữ dòng tiêu đề theo tiêu đề (1) của brief: `Vợ 15 Triệu, Chồng 25 Triệu: Chia Tiền Nhà Sao Công Bằng?`.
- Thêm Câu hỏi trung tâm, 5 câu trước khi viết và bảng Bước lập luận vào đầu `script.md`.
- Viết lại CH00: mở bằng dữ kiện thật S4, nói số của biểu đồ thật ngay hai câu đầu, nêu nghịch lý và câu hỏi trung tâm; không đưa nhân vật giả định vào CH00.
- Chuyển Thảo–Nam và tuyên bố “Đây là ví dụ giả định để tính” xuống đầu CH01.
- Cập nhật bảng Biểu đồ: CH00 dùng cột sáu nghiên cứu / 38.534 người; CH01 bắt đầu phần biểu đồ giả định về thu nhập, chi chung và chia đều.
- Không sửa CH02–CH06. `factcheck.md` đã có dòng kiểm chứng tương ứng cho dữ kiện S4, nên không cần bổ sung khẳng định mới.

## CH00 mới (nguyên văn)

Một nghiên cứu về cách các cặp đôi tổ chức tiền đã gộp sáu nghiên cứu, với ba mươi tám nghìn năm trăm ba mươi bốn người tham gia.
Biểu đồ đầu tiên vẽ sáu nghiên cứu và ba mươi tám nghìn năm trăm ba mươi bốn người.
Nhóm gộp toàn bộ tiền trong dữ liệu ấy báo cáo mức hài lòng quan hệ cao hơn nhóm giữ tách một phần hoặc toàn bộ.
Nhưng đó là liên hệ trong nghiên cứu quốc tế, không phải lời hứa cho một gia đình cụ thể. ‖
Vậy vì sao một câu hỏi rất đời thường là “cách quản lý tài chính vợ chồng” lại không có một đáp án chia tiền duy nhất?
Nghịch lý là chia đôi tiền nhà nghe rất công bằng, nhưng người lương thấp có thể hết tiền trước.
Ba bảng sau giữ cùng một hóa đơn, rồi lần lượt hỏi về cùng số tiền, cùng tỷ lệ thu nhập, và phần riêng hay phần chung.
Câu hỏi trung tâm là: chia đôi tiền nhà nghe rất công bằng, vì sao người lương thấp lại hết tiền trước?
Cuối video, ba bảng sẽ quay lại để đóng vòng này: công bằng là cùng góp một số, cùng chịu một tỷ lệ, hay cùng có phần riêng?

## Cổng đã chạy

1. `python data/long/ck-f4-vo-chong-chia-tien/analysis.py` — chạy thành công.
2. `python data/long/ck-f4-vo-chong-chia-tien/check.py` — `CK F4 check: OK (17 phép)`.
3. `python motion/long/script_lines.py ck-f4-vo-chong-chia-tien` — CH00: 218 âm tiết; tổng: 2.635 âm tiết.
4. `python motion/long/studio_lint.py ck-f4-vo-chong-chia-tien --strict` — `0 lỗi, 0 cảnh báo`.
5. `python scripts/long_gate.py ck-f4-vo-chong-chia-tien --min-syl 1900` — **TRƯỢT (19 lỗi)**.

`long_gate` không thể in ĐẠT trong phạm vi W1c này: topic hiện có 0 cảnh, thiếu HUD/scenes của cả 7 chương, chưa có TTS, và `spec.youtube` chưa hoàn chỉnh. Ticket chung dự kiến rõ trường hợp này: “long_gate trượt vì chưa có cảnh là bình thường.” Các file cần để khắc phục (`gen_scenes.py`, `chNN.json`, `spec.json`, TTS) không nằm trong danh sách file W1c cho phép ghi, nên không sửa.

## Dữ kiện câu 0

Câu 0 lấy từ dữ kiện **#21** trong `facts.md`: Gladstone, Garbinsky và Mogilner (2022) báo cáo sáu nghiên cứu với tổng 38.534 người; nguồn S4 đã có URL mở được trong `factcheck.md`.

## Khẳng định không kiểm được

Không có khẳng định mới nào chưa kiểm được.

## Clip sheet và thumbnail

Chưa có, vì W1c chỉ sửa kịch bản mở đầu; ticket không yêu cầu dựng cảnh, clip sheet hoặc thumbnail.
