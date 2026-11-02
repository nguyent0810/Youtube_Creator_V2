# GH-25 — Báo cáo Codex

## Đã thực hiện

- `motion/long/studio_lint.py`
  - Thêm lỗi strict khi chữ chính của cảnh lặp từ bốn từ đầu của câu đang đọc,
    so sánh không phân biệt hoa/thường và dấu câu. Câu chứa `TRÍCH DỊCH` được miễn.
  - Thêm lỗi strict cho nhãn toàn ASCII có tiếng Việt thiếu dấu. Danh sách bằng
    chứng được giữ hẹp để giảm báo nhầm: `CONG TY`, `NAM` khi đứng với số,
    `TRIEU`, `NGUOI`, `CHUONG`, `THANG`, `TIEN`, `KHONG`, `NHIEU`, `DUOC`.
    Không bắt các từ mơ hồ/ngắn hoặc tên riêng tiếng Anh như Apple, NeXT, CEO.
- `motion/long/build_long.py`: cuối `do_final` gọi `srt.py`; lỗi tạo SRT hoặc
  không có `captions.vi.srt` sẽ làm `final` lỗi.
- `motion/long/factcheck_lint.py` mới: so số/ngày trong lời đọc và chữ cảnh với
  `factcheck.md`/`research.md`, kiểm `TRÍCH DỊCH` có nguyên văn tiếng gốc kèm URL,
  và phát hiện dòng bảng factcheck lệch bản final. Chuẩn hóa các dạng ngày
  `07.02.1997`/`7/2/1997` và lượng nói kiểu `50 nghìn`/`50.000`.
- `motion/long/publish_long.py`: với bài chưa có `video_id`, từ chối trước upload
  nếu `factcheck_lint` có lỗi; bài đã upload giữ nguyên đường đi cũ.
- `motion/long/describe.py`: không in `🎵 NHẠC NỀN` khi không có nhạc; bỏ cắt
  cứng `sources[:8]`. Chỉ rút nguồn khi toàn bộ mô tả vượt 5.000 byte.
- Thêm test cho hai luật studio, factcheck và mô tả trong ba file ticket cho phép.

## Định dạng factcheck đề xuất

Giữ bảng theo chương, nhưng mỗi câu có nhãn `TRÍCH DỊCH` cần một mục cụ thể,
không chỉ ghi nhãn chung:

```
| CH03 | [TRÍCH DỊCH] bản dịch dùng trong lời đọc. Nguyên văn: "..." | #24 | https://nguon-goc.example/... |
```

Mỗi số/ngày hiện trong lời đọc hoặc cảnh nên xuất hiện nguyên dạng hoặc tương
đương chuẩn hóa trong cột khẳng định của `factcheck.md` hoặc `research.md`.

## Lệnh đã chạy

- `python -m py_compile motion/long/studio_lint.py motion/long/factcheck_lint.py motion/long/describe.py motion/long/build_long.py motion/long/publish_long.py` — đạt.
- `python -m pytest -q tests/test_studio_lint_text.py tests/test_factcheck_lint.py tests/test_describe_fit.py` — **13 passed**; chỉ có cảnh báo pytest không ghi được `.pytest_cache` do quyền thư mục.
- `python -m pytest -q tests/` — **488 passed, 11 skipped, 14 failed, 243 errors**. Không xanh vì môi trường không cho pytest đọc/tạo `C:\Users\Tung-QA\AppData\Local\Temp\pytest-of-Tung-QA` (`PermissionError`), kéo theo các test dùng `tmp_path`; ngoài ra có 14 fail nền ở các module/asset không thuộc phạm vi ticket. Không sửa các phần đó theo giới hạn GH-25.
- Đã chạy `studio_lint.py <topic> --strict` và `factcheck_lint.py <topic>` trên toàn bộ topic MIM/CK bên dưới.

Không render, không tạo/cập nhật thumbnail hoặc clip sheet, không upload, không đổi lịch và không commit. Vì vậy đường dẫn clip sheet/thumbnail: không áp dụng cho ticket này.

## Hồi quy MIM/CK

`Tiền tố` và `thiếu dấu` là số lỗi của hai luật mới. `Factcheck` là tổng lỗi
của cổng mới; dữ liệu cũ có nhiều mục chưa đủ đối chiếu nên cần được xử lý theo
từng ticket nội dung, không được tự sửa trong GH-25.

| Topic | Tiền tố | Thiếu dấu | Factcheck |
|---|---:|---:|---:|
| ck-2026-kenh-dau-tu | 0 | 0 | 30 |
| ck-a2-luong-va-lam-phat | 0 | 0 | 22 |
| ck-b1-mua-hay-thue | 0 | 0 | 53 |
| ck-b2-lai-kep | 0 | 0 | 1 |
| ck-b3-tra-gop-0 | 0 | 0 | 1 |
| ck-b4-mua-xe | 0 | 0 | 1 |
| ck-c1-vnindex-dung-yen | 0 | 0 | 56 |
| ck-c2-phien-giao-dich | 0 | 0 | 60 |
| ck-c3-bieu-do-nen | 0 | 0 | 55 |
| ck-c4-duong-trung-binh | 0 | 0 | 1 |
| ck-c5-co-tuc | 0 | 0 | 1 |
| ck-c6-gia-tran-san-t2 | 0 | 0 | 39 |
| ck-d1-vang-dinh | 0 | 0 | 41 |
| ck-d2-fomo | 0 | 0 | 50 |
| ck-d3-lo-khong-dam-ban | 0 | 0 | 1 |
| ck-e1-mua-deu-moi-thang | 0 | 0 | 1 |
| ck-e2-quy-khan-cap | 0 | 0 | 1 |
| ck-e3-no-the-tin-dung | 0 | 0 | 1 |
| ck-e4-bao-hiem-tien-gui | 0 | 0 | 22 |
| ck-e5-thue-tncn-2026 | 0 | 0 | 44 |
| ck-e6-luong-huu-rut-mot-lan | 0 | 0 | 16 |
| ck-f1-tro-cap-that-nghiep | 0 | 0 | 16 |
| ck-f2-vien-phi-bhyt | 0 | 0 | 24 |
| ck-f3-tien-mung-cuoi | 0 | 0 | 10 |
| ck-f4-vo-chong-chia-tien | 0 | 0 | 41 |
| ck-g1-thuong-tet-2027 | 0 | 0 | 0 |
| ck-i1-100-trieu-tiet-kiem-hay-vnindex | 0 | 0 | 45 |
| mim-ai-70 | 0 | 0 | 1 |
| mim-ai-chat-privacy | 0 | 0 | 1 |
| mim-ai-feed | 0 | 0 | 54 |
| mim-ai-gpu | 0 | 0 | 17 |
| mim-ai-hallucinate | 0 | 0 | 38 |
| mim-ai-jobs | 0 | 0 | 61 |
| mim-ai-khuon-mat | 0 | 0 | 1 |
| mim-ai-voice | 0 | 0 | 53 |
| mim-alphago-lee-sedol | 0 | 0 | 1 |
| mim-apollo-1202 | 0 | 0 | 11 |
| mim-captcha | 0 | 0 | 1 |
| mim-deep-blue-kasparov | 0 | 0 | 1 |
| mim-deepfake-lua-dao-2025 | 0 | 0 | 0 |
| mim-dich-may | 0 | 0 | 18 |
| mim-flappy-bird | 0 | 0 | 1 |
| mim-google-maps-kal007 | 0 | 0 | 12 |
| mim-jobs-1985 | 1 | 0 | 2 |
| mim-katherine-johnson | 2 | 0 | 3 |
| mim-ke-huy-diet-petrov | 0 | 0 | 8 |
| mim-lecun-1989 | 0 | 0 | 0 |
| mim-luat-ai-2026 | 0 | 0 | 0 |
| mim-ma-qr | 0 | 0 | 1 |
| mim-macintosh-1984 | 0 | 0 | 8 |
| mim-may-choi-game | 0 | 0 | 1 |
| mim-may-thang-poker | 0 | 0 | 1 |
| mim-moneyball | 1 | 0 | 3 |
| mim-oppenheimer-feynman | 0 | 0 | 12 |
| mim-qwerty | 0 | 0 | 1 |
| mim-siri-susan-bennett | 0 | 0 | 12 |
| mim-social-network | 1 | 0 | 3 |
| mim-turing-bombe | 1 | 0 | 4 |
| mim-watson-jeopardy | 0 | 0 | 1 |
| mim-web-1989-1993 | 0 | 0 | 0 |

## Jobs 1985 và điểm chưa chắc

- Có bắt lỗi retro `TRÍCH DỊCH`: checker thấy ba nhãn/câu dùng nhãn trong bản
  cuối (bao gồm nhãn cảnh CH01); `factcheck.md` có URL liên quan nhưng không có
  nguyên văn tiếng gốc theo định dạng bắt buộc, nên báo lỗi.
- Có bắt lỗi retro lệch final: mục CH08 về Apple–Microsoft/Microsoft đầu tư
  150 triệu USD không còn số liệu tương ứng trong bài, nên báo `lệch bản final`.
- `studio_lint` cũng tìm thấy một lỗi tiền tố hiện có ở Jobs: CH06 cảnh 4,
  `SAU CUỘC SO SÁNH`; không sửa nội dung vì GH-25 cấm sửa `data/long/**`.
- Việc nhận diện tiếng Việt thiếu dấu chủ ý không bao quát mọi từ ASCII để tránh
  báo nhầm tên riêng, viết tắt và từ tiếng Anh. Các từ/cụm nằm ngoài danh sách
  bằng chứng ở trên cần được bổ sung qua test trước khi biến thành lỗi strict.
- Lệnh kiểm quota HyperFrames không chạy do npm cache bị `EPERM`; ticket cấm
  render nên không có quota/render nào được sử dụng.
- Lần thử chạy pytest với `--basetemp` tạo thư mục tạm rỗng `.pytest-gh25` ở
  root workspace. Lệnh xóa chính xác thư mục này bị sandbox chặn; cần xóa thủ
  công nếu workspace yêu cầu sạch tuyệt đối.
