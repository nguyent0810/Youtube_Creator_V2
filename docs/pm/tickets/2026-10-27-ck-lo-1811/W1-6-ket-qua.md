# W1-6 — Kết quả kịch bản `ck-i1-100-trieu-tiet-kiem-hay-vnindex`

## Đã làm

- Viết `data/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/script.md`: 7 chương CH00–CH06, tiêu đề B3, câu hỏi trung tâm, 5 câu trước khi viết, bảng bước lập luận và bảng biểu đồ.
- CH00 mở bằng dữ kiện số 1 trong `facts.md`: 09/04/2018, VN-Index 1.204,33 điểm; không có nhân vật giả định. Vòng mở là khoảng cách giữa kết quả cuối và đoạn rơi; mở ở CH00 câu 3–4, đóng ở CH06 câu 19–25.
- Viết `analysis.py`, `check.py`, `results.json` cho hai CSV ticket cấp. Phí giả định 0,15% khi mua và bán; thuế chuyển nhượng 0,1% khi bán. `check.py` kiểm độc lập 6 phép.
- Viết `factcheck.md`, với URL cho mọi dữ kiện nguồn và phần ghi rõ giới hạn.

## Kết quả cổng W1

| Mục | Kết quả |
|---|---|
| Tổng âm tiết | 1.919 |
| CH00 | 215 âm tiết |
| `analysis.py` | Ghi `results.json` thành công |
| `check.py` | `I1 check: OK (6 phep)` |
| `script_lines.py` | Tạo đủ CH00–CH06 |
| `studio_lint.py --strict` | 0 lỗi, 0 cảnh báo |

## Biểu đồ theo chương

| Chương | Biểu đồ chính | Số neo |
|---|---|---|
| CH00 | race tuyệt đối | 09/04/2018, 1.204,33 điểm; một lần mở 100 triệu |
| CH01 | race ba vị trí | 24 lần mua, mỗi lần 4,1667 triệu |
| CH02 | race + waterfall | một lần: 54,52 triệu ở 24/03/2020 |
| CH03 | race + line | cuối 2021: 1.498,28 điểm |
| CH04 | race + bars | mua đều: 93,63 triệu ở 15/11/2022 |
| CH05 | race + dots | mốc quan sát 4,9% ngày 15/01/2024 |
| CH06 | race + counter | một lần 145,48 triệu; mua đều 180,61 triệu ở 06/10/2026 |

## Lệnh đã chạy

```text
PYTHONIOENCODING=utf-8 python data/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/analysis.py
PYTHONIOENCODING=utf-8 python data/long/ck-i1-100-trieu-tiet-kiem-hay-vnindex/check.py
PYTHONIOENCODING=utf-8 python motion/long/script_lines.py ck-i1-100-trieu-tiet-kiem-hay-vnindex
PYTHONIOENCODING=utf-8 python motion/long/studio_lint.py ck-i1-100-trieu-tiet-kiem-hay-vnindex --strict
PYTHONIOENCODING=utf-8 python scripts/long_gate.py ck-i1-100-trieu-tiet-kiem-hay-vnindex --min-syl 1900
```

`long_gate.py` đã chạy nhưng **TRƯỢT 19 lỗi**. Nguyên nhân không phải lỗi W1: ticket W1 chỉ cho ghi script, factcheck, analysis, check, results và báo cáo; chưa có `gen_scenes.py`, cảnh/HUD/spec YouTube hay TTS. Cổng yêu cầu các đầu ra W2 này nên báo thiếu HUD, tối thiểu 5 loại cảnh mỗi chương, TTS, `spec.youtube` và bảng SAY. Không chạy render; không có clip sheet hoặc thumbnail trong phạm vi W1.

## Khẳng định chưa kiểm được

Không có chuỗi lãi suất bình quân tiền gửi kỳ hạn 12 tháng theo từng năm 2018–2026 đủ chuẩn trong kho R6. Vì vậy không tính đường tiết kiệm, sức mua cuối kỳ hoặc kết luận tiết kiệm thắng/thua. Các mốc lãi suất quan sát chỉ được nói đúng phạm vi và không thay cho bình quân năm.
