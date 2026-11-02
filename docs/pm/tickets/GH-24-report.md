# GH-24 report — QA ảnh tĩnh và cổng dấu soát

## Đã làm

- Thêm `motion/long/img_sheet.py <topic>` để tạo `output/long/<topic>/qa_imgs.jpg` bằng Pillow. Mỗi ảnh dùng thực tế có thẻ riêng: ảnh gốc, các khung crop 16:9 theo từng `focus`, crop thực tế, và nhãn `chNN#i` / loại cảnh / số lần dùng. Cảnh `print` hiện bản mô phỏng bố trí `B.print` với ảnh nguyên tỉ lệ, không crop 16:9.
- Thêm `--ok` cho `img_sheet.py` và `clip_sheet.py`. Lệnh chỉ ghi dấu sau khi tờ tương ứng đã tồn tại.
- Thêm cổng trong `build_long.py`: `render` (kể cả `--draft`) và `final` dừng khi thiếu dấu hoặc dấu không khớp cảnh hiện tại; `final` còn kiểm trước khi xóa `final.mp4` cũ. Thông báo đưa chính xác hai lệnh tạo tờ và xác nhận `--ok`. Topic không có loại asset nào thì không đòi dấu loại đó.
- Thêm `tests/test_img_sheet.py` và `tests/test_sheet_gate.py`: hash ổn định, đổi `focus` hoặc clip/ms làm dấu cũ, dấu khớp đi qua, và `do_render` / `do_final` vào cổng trước khi làm việc khác.

## Định dạng dấu

- `output/long/<topic>/qa_imgs.ok`: một dòng SHA-256 hex (64 ký tự) của danh sách đã sắp xếp các mục `{"key": ..., "focus": [...]|null}`. Danh sách giữ cả số lần dùng.
- `output/long/<topic>/qa_clips.ok`: một dòng SHA-256 hex (64 ký tự) của danh sách đã sắp xếp các mục `{"id": ..., "ms": ...}`.

## Lệnh đã chạy

```powershell
$env:PYTHONIOENCODING='utf-8'; python -m py_compile motion/long/img_sheet.py motion/long/clip_sheet.py motion/long/build_long.py
$env:PYTHONIOENCODING='utf-8'; python motion/long/img_sheet.py mim-jobs-1985
$env:PYTHONIOENCODING='utf-8'; python -m pytest -q -p no:cacheprovider tests/test_img_sheet.py tests/test_sheet_gate.py
$env:PYTHONIOENCODING='utf-8'; python -m pytest -q tests/
```

Kết quả:

- `py_compile`: đạt.
- Test GH-24: **7 passed in 1.33s**.
- `tests/` đầy đủ: **478 passed, 14 failed, 243 errors, 11 skipped**; không xanh. Lỗi setup chủ đạo là `PermissionError` khi pytest truy cập `C:\Users\Tung-QA\AppData\Local\Temp\pytest-of-Tung-QA`; lỗi trải khắp các test ngoài phạm vi GH-24. Đây là lỗi lint/test còn lại cần môi trường có quyền thư mục tạm để chạy lại.
- Một lần thử chuyển pytest sang basetemp trong repo tạo mục `.pytest-gh24` nhưng sandbox cũng từ chối truy cập mục đó; không dùng mục này cho kết quả test và không xóa vì nó nằm ngoài phạm vi topic của ticket.

## Tờ soát Jobs 1985

- Tờ: `output/long/mim-jobs-1985/qa_imgs.jpg`.
- Đã mở và tự kiểm: `nextcube` không có vì không còn cảnh nào dùng; `sculley06` có khung crop vùng mặt và bản `print` nguyên tỉ lệ; cả sáu ảnh AI `ai01`–`ai06` đều có trong tờ.
- Không chạy `--ok` cho Jobs 1985. Hiện chưa có `qa_imgs.ok` hoặc `qa_clips.ok`, để Lead soát và ký sau.

## Topic MIM/CK hiện chưa có dấu cần thiết

Tất cả 60 topic hiện tại chưa đủ dấu QA:

```text
ck-2026-kenh-dau-tu
ck-a2-luong-va-lam-phat
ck-b1-mua-hay-thue
ck-b2-lai-kep
ck-b3-tra-gop-0
ck-b4-mua-xe
ck-c1-vnindex-dung-yen
ck-c2-phien-giao-dich
ck-c3-bieu-do-nen
ck-c4-duong-trung-binh
ck-c5-co-tuc
ck-c6-gia-tran-san-t2
ck-d1-vang-dinh
ck-d2-fomo
ck-d3-lo-khong-dam-ban
ck-e1-mua-deu-moi-thang
ck-e2-quy-khan-cap
ck-e3-no-the-tin-dung
ck-e4-bao-hiem-tien-gui
ck-e5-thue-tncn-2026
ck-e6-luong-huu-rut-mot-lan
ck-f1-tro-cap-that-nghiep
ck-f2-vien-phi-bhyt
ck-f3-tien-mung-cuoi
ck-f4-vo-chong-chia-tien
ck-g1-thuong-tet-2027
ck-i1-100-trieu-tiet-kiem-hay-vnindex
mim-ai-70
mim-ai-chat-privacy
mim-ai-feed
mim-ai-gpu
mim-ai-hallucinate
mim-ai-jobs
mim-ai-khuon-mat
mim-ai-voice
mim-alphago-lee-sedol
mim-apollo-1202
mim-captcha
mim-deep-blue-kasparov
mim-deepfake-lua-dao-2025
mim-dich-may
mim-flappy-bird
mim-google-maps-kal007
mim-jobs-1985
mim-katherine-johnson
mim-ke-huy-diet-petrov
mim-lecun-1989
mim-luat-ai-2026
mim-ma-qr
mim-macintosh-1984
mim-may-choi-game
mim-may-thang-poker
mim-moneyball
mim-oppenheimer-feynman
mim-qwerty
mim-siri-susan-bennett
mim-social-network
mim-turing-bombe
mim-watson-jeopardy
mim-web-1989-1993
```
