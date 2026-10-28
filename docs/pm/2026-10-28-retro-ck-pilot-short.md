# Retro lô pilot hook CK (6 Short, đăng 28/10/2026)

Phạm vi: chỉ đọc. Đã xem state.sqlite (chế độ chỉ đọc), spec, bundle, timing.json, final.mp4 (ffprobe), contact sheet p1/p2, code build/engine. Không sửa gì ngoài file này.

## 1. Đối chiếu lịch và cổng nội dung

| Ngày (19:00 VN) | Slug | Hook | video_id | item.stage / upload_log | Voice (s) | final.mp4 (s) | Look | Cảnh |
|---|---|---|---|---|---|---|---|---|
| 07/11 | ck-p1-thue-5-nam-cong-lai | B | Td06vcpnEnQ | published / done | 34,49 | **35,10** | lab | 7 |
| 08/11 | ck-p2-tra-truoc-mot-ty | A | Ojbp75PBuew | published / done | 34,09 | 34,70 | chalk | 7 |
| 09/11 | ck-p3-nuoi-xe-moi-thang | A | MFWHpGh7TY0 | published / done | 32,81 | 33,43 | blueprint | 7 |
| 10/11 | ck-p4-xe-mat-gia-moi-thang | B | 8H2qOrgbvc8 | published / done | 31,45 | 32,07 | notebook | 6 |
| 11/11 | ck-p5-mua-sau-nam-tang-40 | B | pRPBbisoCL4 | published / done | 33,05 | 33,67 | neon | 6 |
| 12/11 | ck-p6-270-nghin-tai-khoan-3-2022 | A | aebGPJQcuS0 | published / done | 31,61 | 32,23 | studio | 6 |

- Cả 6 publish_at = 12:00Z = 19:00 VN, đúng ngày. Video_id khớp. Bundle `bundles/CK/*.json` có title và mô tả khớp spec hiện tại.
- Chênh trong cặp (final): cặp 1 là 0,4 s, cặp 2 là 1,37 s, cặp 3 là 1,43 s. Đạt ±3 s.
- **p1 dài 35,10 s, vượt trần 35 s 0,1 s.** Lý do: voice 34,49 s cộng 0,6 s đuôi. Không ảnh hưởng tới phép so trong cặp, nhưng lint độ dài nên đo trên final, không đo trên voice.
- Long trong "Bản đầy đủ": B1 mua-hay-thue (public 30/10), B4 mua-xe (01/11), D2 fomo (06/11). Cả ba lên sóng trước Short tương ứng.
- Tên ngân hàng, công ty chứng khoán, hãng xe, mã cổ phiếu: quét mô tả, lời đọc và chữ trên màn hình, **không có**. "VSD" là trung tâm lưu ký, không phải công ty chứng khoán. Không có "nên mua/bán". Cả 6 mô tả có câu miễn trừ. Khối "Nguồn:" sạch (không có "hồ sơ", "[A…", "CẦN", "<>"). Tiêu đề dài 42–60 ký tự, p5 chạm đúng trần 60.
- "VÍ DỤ GIẢ ĐỊNH" có trên mọi cảnh trình bày giả định lần đầu. **Nhưng cảnh tóm tắt cuối bài nhắc lại số giả định mà không gắn nhãn:**
  - p1 cảnh 6: "≈414 TRIỆU / 5 NĂM";
  - p3 board: "≈ 3% của 4,73 triệu";
  - p4 board: "≈ 5,25 triệu / tháng" và cảnh 5: "700 → 385 SAU 5 NĂM".

  AGENTS.md ghi "số tự giả định phải ghi VÍ DỤ GIẢ ĐỊNH". Lỗi này không làm đổi nghĩa, nên theo ngưỡng thay video thì **không thay**. Cần chủ kênh chốt luật: nhãn chỉ bắt buộc ở lần đầu, hay ở mọi cảnh có số giả định?

## 2. Hook A/B có thật sự chỉ khác hook? Biến nhiễu

Chủ đề khác nhau trong cặp là do thiết kế (brief mục 5). Ngoài chủ đề, còn các biến nhiễu sau:

1. **Có clip trong 2 giây đầu: trùng hoàn toàn với hook (nặng nhất).**
   - Cả 3 bài B mở bằng kinetic trên clip Pexels toàn khung (p1 hộp đồ, p4 bãi xe, p5 hai người cầm điện thoại).
   - Cả 3 bài A mở bằng chữ hoặc bộ đếm trên nền tối, không clip (p2 counter 6,8%, p3 counter 130, p6 chữ 270.217).
   - Nếu B thắng, không tách được là nhờ "bạn + con số" hay nhờ khung hình động ở giây 0.
2. **Look khác nhau ở cả 6 bài.** `looks.resolve` tự xoay look theo sổ `data/variety/short_looks.json`. Brief yêu cầu giữ look cố định, nhưng spec không ghi `"look"`. Chữ ký chuỗi cảnh cũng khác nhau (vd. p1 `M D D T D G M`, p2 `D G T D T M G`).
3. **Chữ trên màn hình ở khung 0 không theo hook.** Người lướt tắt tiếng chỉ thấy chữ:
   - p1 (B): "6,25 TRIỆU / THÁNG", không có "bạn";
   - p5 (B): "+40% TRONG 1 NĂM", thực chất là dữ kiện bên ngoài kiểu A ("BẠN MUA VÀO LÚC NÀY?" hiện sau);
   - chỉ p4 có "CỦA BẠN" ngay khung 0.
   - Lời đọc p5 cũng lai: "Bạn mua…" đi kèm dữ kiện thị trường.
4. **Số cảnh:** cặp 2 lệch (p3 có 7 cảnh, p4 có 6). Cặp 1 và cặp 3 bằng nhau.
5. **Khuôn tiêu đề không đồng nhất.** Chỉ p1 có "bạn" trong tiêu đề. Bài A có số hoặc ngày ở đầu (p6 "Tháng 3/2022, …"). Tiêu đề cũng ảnh hưởng tới lượt hiển thị trên feed.
6. **Lịch Long cùng ngày:** Long CK lên 20:00 VN các ngày 08/11 (A), 09/11 (A), 11/11 (B). Hai ngày A có Long ngay sau, chỉ một ngày B có. Đêm trước p1 (06/11) có 2 Short và Long fomo.
7. Độ dài câu hook gần nhau: B 4,6–5,8 s, A 4,8–5,3 s. Không đáng lo.

Hệ quả khi đọc kết quả: biến 1 và biến 3 đủ để kết quả "tích cực" chỉ được ghi là **"B + clip mở bài"**, chưa phải "B". Vòng 2 nên khoá `look`, clip ở cảnh 0 (có hoặc không, như nhau trong cặp) và chữ khung 0 theo đúng hook.

## 3. Tám sự cố: nguyên nhân gốc và điểm chặn

**P1. Chữ nhấn (acc) trong hộp vàng mất dấu ("TRIEU", "KHONG CO HOA ĐON")**
- Cơ chế, khả năng cao (chưa chụp khung để xác nhận):
  - Dòng acc của CK nhận fx theo pool `"A": ["marker","outline"]` (`motion/stier/themes.py`, theme ck).
  - Fx được xoay theo seed **tiêu đề** (`motion/beatfx.py` `assign_beats`), **không theo look**. Nhận xét "phụ thuộc look" có lẽ là trùng hợp: p1 lab, p2 chalk.
  - `marker` tô dải vàng chỉ cao 78% dòng (`beat.css` `.kin .mk`, `background-size …78%`, vị trí 62%). `theme-ck.css` đổi màu chữ `.mk` thành xanh than `#0a1426`.
  - Dấu chồng của chữ hoa (Ệ, Ô, Ó, Á) nằm ngoài dải vàng, nên thành chữ xanh than trên nền tối, coi như biến mất. "Đ" vẫn còn vì gạch ngang nằm trong dải.
- Cách đã sửa: bỏ `acc` trong spec. Đây là chữa triệu chứng; engine vẫn còn lỗi.
- Chặn:
  - (a) `beat.css` `.kin .mk`: dải vàng phủ 100% chiều cao kèm padding trên, hoặc chữ ngoài dải giữ màu sáng (sửa engine, cần Claude duyệt).
  - (b) Lint trong `build.py` `plan()`, cạnh lint `wide`: theme ck, item acc có ký tự mang dấu chồng chữ hoa, và fx sẽ là `marker` → báo lỗi, hoặc ép `outline`.

**P2. Bảng viết tay / mono mất dấu huyền trong "nghìn" (blueprint, studio)**
- Board dùng phông `Patrick Hand` (bảng paper) hoặc `JetBrains Mono` (blueprint), xem `casefile.css` `.bdn` và `.bd-blueprint`. Phông nạp từ Google Fonts ở `build.py`, khoảng dòng 596.
- Chưa rõ cơ chế (thiếu glyph, dấu tổ hợp hay hộp `lineHeight = fs+54`). Cần render một khung tĩnh để kiểm.
- Cách đã sửa: đổi chữ ("130.000 đ", "270.217"). Cũng là chữa triệu chứng.
- Chặn:
  - (a) Thêm bài kiểm phông một lần: render một khung có đủ bảng chữ tiếng Việt (à ả ã á ạ, ì ỉ ĩ í ị, Ầ Ệ Ộ Ữ…) trên mọi kiểu board, card và kin của 8 look, rồi so OCR hoặc so mắt. Đặt trong `scripts/`, chạy lại mỗi khi sửa `casefile.css`.
  - (b) Khi chưa rõ cơ chế, cho board của theme ck/mim dùng `Be Vietnam Pro`, như `.bd-glass`.

**P3. Nhãn điểm biểu đồ line bị cắt ở mép phải, nhãn điểm đầu đè số trục**
- `casefile.js` dòng 515 đặt `chtag` theo `pos` mà không giới hạn trong vùng X0..X1, và không tránh nhãn trục.
- Chặn:
  - (a) Engine: kẹp x của tag trong [40, 1040 − bề rộng], tự đổi `pos` ở điểm đầu và điểm cuối.
  - (b) Đáng làm nhất: bật `check_gate()` (`build.py`, hiện chỉ chạy cho `theme == "bud" and v2`) cho Short CK/MIM `mix`. Hàm này chạy `hyperframes check` (layout, overflow, contrast) giữa mỗi cảnh, nên bắt được chữ tràn khung và chữ chồng nhau. Lúc đầu để `strict=False` cho tới khi hết báo nhầm.

**P4. Clip 238×426 bị phóng toàn khung; clip người văn phòng cho bài xe**
- **Lỗi thật trong `motion/stier/clips.py` `ensure()`, đoạn chọn file.**
  - Khoá sắp xếp là `(min(w,h) < need, max(w,h))`. Khi **không** file nào đạt `need` (khe "full" cần 1080), mọi file đều mang giá trị True, và bản **nhỏ nhất** đứng đầu.
  - Ví dụ: bộ clip đại lý xe 7154xxx chỉ có tối đa 1066×1920, nên hàm chọn bản 238×426. Đã kiểm trên `index.json`: pexels:7154236, 7154241 và 14 clip khác cùng dạng.
- Sửa đề xuất: khi không file nào đạt `need`, chọn file **lớn nhất**; nếu cạnh ngắn < 0,7·need thì `SystemExit`.
- Độ liên quan của clip: `clip_sheet.py` chỉ dùng cho Long. Short không có tờ soát clip nào trước render. Đề xuất `clips.py sheet <slug>`: 3 khung mỗi clip kèm tiêu đề Pexels, để người duyệt đọc trước khi dựng.

**P5. Counter 0→414 bị chặn**
- Luật đúng: `build.py` `plan()` có `bad_pre` (prefix "≈" kèm số chạy thì số trung gian đọc như dữ kiện).
- Lỗi nằm ở thời điểm chặn: luật chạy **sau TTS**, và generator không biết luật này.
- Chặn: tách các lint tĩnh của spec (`~`, counter prefix, năm, dòng phụ > 52 ký tự, chart CSS) thành `spec_lint(spec)` chạy **trước** `speak()`, cộng lệnh `build.py --lint-only` để generator gọi ngay.

**P6. `sources` có ghi chú nội bộ hoặc rỗng**
- Bài học 21/10 (`feedback-public-description-no-internal-notes`) mới nằm trong memory và AGENTS.md, **chưa thành code**.
- `enqueue_ck.py` chỉ kiểm câu miễn trừ. `Bundle.validate()` (`factory/bundle.py`) chỉ chặn `<>` ở **tiêu đề**, không chặn ở mô tả.
- Chặn, đáng làm nhất vì phủ mọi kênh: trong `Bundle.validate()` cho kind short/long, chặn mô tả có `<`, `>`, "CẦN", "cần kiểm", "WebFetch", "factcheck", "data/", "tìm kiếm", "agent", "hồ sơ Long", `\[[A-Z]\d+-\d+\]`; chặn khối "Nguồn:" rỗng.
- `enqueue_ck.py` / `enqueue_mim.py`: `spec["sources"]` phải là list không rỗng.
- Lưu ý: `enqueue_ck` chỉ ghi bundle khi bundle **chưa tồn tại**. Nếu đã enqueue bản có ghi chú nội bộ, sửa spec xong bundle vẫn giữ mô tả cũ. Lần này đã kiểm: bundle khớp spec. Nên ghi đè bundle khi stage chưa phải `published`.

**P7. Hook sai mốc thời gian ("Từ năm 2023…")**
- Nguyên nhân: lẫn **năm số hiệu nghị định** (90/2023) với **ngày hiệu lực** (01/02/2024). Factcheck có dòng NĐ 90/2023, nhưng không có cột "hiệu lực từ / còn hiệu lực" và không đối chiếu đúng cụm thời gian trong câu đọc.
- `factory/factcheck.py` và `factory/claims.py` viết cho kênh Lịch, không dùng được cho CK.
- Chặn:
  - (a) Mẫu factcheck CK: mỗi dòng dữ kiện pháp lý có cột "hiệu lực từ" và "văn bản hiện hành (kiểm ngày …)".
  - (b) Lint nhẹ `motion/stier/script_lint.py`, mở rộng cho CK: câu đọc có "từ năm YYYY" hoặc "năm YYYY" mà spec hoặc factcheck nhắc "Nghị định …/YYYY" thì cảnh báo "năm số hiệu ≠ năm hiệu lực". Câu 0 phải có mọi con số khớp một dòng factcheck (brief mục 5 đã yêu cầu).

**P8. Báo cáo sai "5 cặp -r2 đều đang hẹn giờ"**
- `state.sqlite` vẫn ghi bản gốc là `published` kèm `publish_at`. Đã kiểm: `mim-cuda-canh-bac-2006` y4Af8x1-LSA và `mim-watson-ferrucci-sai-gan-het` RxDrSm0nkj8, cùng giờ với bản `-r2`.
- `factory/store.py` `STAGES` không có trạng thái "đã thay / đã ẩn". Việc thay video làm tay, không có script ghi sổ.
- Chặn:
  - (a) Thêm stage hoặc cột `replaced_by`, và script thay video (ẩn bản gốc, đổi tiêu đề, ghi sổ) dùng chung.
  - (b) Luật báo cáo: mọi câu "đang hẹn / sẽ lên" phải đối chiếu `videos.list status` (privacyStatus, publishAt) trước khi viết, không đọc từ sổ.
  - (c) Bộ đếm hàng chờ (`motion/stier/monitor.py` hoặc báo cáo PM) cảnh báo khi hai item cùng kênh có cùng `publish_at`.

## 4. Thứ tự ưu tiên đề xuất (chưa làm, chờ duyệt)

1. Sửa `clips.ensure` chọn bản nhỏ nhất (P4). Lỗi thật, sửa 1 dòng, ảnh hưởng mọi Short có clip không đủ 1080.
2. Quét mô tả trong `Bundle.validate()` và chặn `sources` rỗng (P6). Phủ mọi kênh, biến bài học thành code.
3. `spec_lint` chạy trước TTS cộng `--lint-only` (P5, và là chỗ đặt lint P1b).
4. Bật `check_gate` cho CK/MIM ở chế độ cảnh báo (P3, có thể cả P1).
5. Engine: dải marker và kẹp tag biểu đồ (P1a, P3a). Cần Claude duyệt vì sửa code dùng chung.
6. Bài kiểm phông tiếng Việt cho 8 look (P2).
7. Stage "replaced" và đối chiếu API trước khi báo lịch (P8).
8. Mẫu factcheck pháp lý có cột hiệu lực, cộng lint năm số hiệu (P7).
9. Pilot vòng 2: ghi `"look"` cố định theo cặp, clip ở cảnh 0 giống nhau trong cặp, chữ khung 0 theo đúng hook (mục 2).

## 5. Ghi chú quy trình

- **Generator lệch so với spec đã sửa.** `scratchpad/gen_pilot_ck.py` vẫn chứa bản trước khi sửa: "Từ năm hai nghìn không trăm hai mươi ba", clip 7154236/7154241, "130 nghìn / tháng", acc trên "KHÔNG CÓ HOÁ ĐƠN". **Chạy lại generator sẽ ghi đè các bản sửa.** Không dùng lại file này; nếu cần, sinh lại từ spec hiện tại.
- Lỗi P1, P2, P3 và phần độ liên quan của P4 chỉ lộ ra trên contact sheet, ở mức 2 giây/khung. Đó là cổng duy nhất bắt được, và hoàn toàn làm tay.

## 6. Còn làm tay trước 07/11

- [ ] Gắn **"Video liên quan"** trong Studio (Chrome) cho cả 6 Short: p1, p2 → B1 mua-hay-thue (pXKfIo_nyVM); p3, p4 → B4 mua-xe (Bx9w_a_1YOI); p5, p6 → D2 fomo (ULLEUHkYz9g). API không làm được việc này. Brief tính lượt Short → Long, nên thiếu là mất chỉ số.
- [ ] Đọc baseline Studio ("xem / lướt qua", lượt hiển thị trên feed) trước 07/11. Pilot đọc kết quả ở mốc 48 h và 7 ngày sau 12/11.
- [ ] Chủ kênh chốt luật nhãn "VÍ DỤ GIẢ ĐỊNH" cho cảnh tóm tắt (mục 1).

## Cập nhật 28/10: đã sửa P4, P6 (sau review ChatGPT)

- **P4:** thêm `motion/stier/clips.py:pick_file()`.
  - Chọn bản nhẹ nhất có cạnh ngắn ≥ mức cần; nếu không có bản nào đủ thì chọn bản lớn nhất.
  - Dừng hẳn nếu bản lớn nhất vẫn dưới 50% mức cần.
  - Kiểm thử hồi quy, 4 ca, trong `tests/test_stier_media.py`: có bản đạt chuẩn; không bản nào đạt nhưng còn dùng được (ca 7154241); mọi bản đều quá nhỏ; ô cửa sổ.
- **P6:** thêm `factory/bundle.py:internal_note_issues()`, được gọi trong `Bundle.validate()`, nên chạy ở mọi lần lưu hoặc đưa bundle vào hàng chờ.
  - Chặn: `<` `>`, "cần kiểm", WebFetch/factcheck, đường dẫn repo (trừ khi nằm trong URL), mã kiểu `[A1-83]`, "hồ sơ Long/bài/nguồn", khối "Nguồn:" rỗng.
  - Cố ý không chặn "tìm kiếm" và "agent", vì là từ thường trong mô tả MIM.
  - Kiểm thử: 4 ca ghi chú nội bộ, 1 ca nguồn rỗng, 4 ca chữ công khai hợp lệ (`tests/test_bundle_and_store.py`).
- **Quét lại 693 bundle trên máy:** khoảng 24 bundle MIM đã hẹn giờ vẫn chứa "CẦN KIỂM", "data/long/…" trong mô tả lưu trên máy.
  - Đọc trực tiếp YouTube API: mô tả công khai của **mọi** video MIM và CK đều sạch.
  - Ngoại lệ: `ck-bang-de-danh-den-2030` (Gy31ReYpvIM, đang công khai) có khối "Nguồn:" rỗng. Lỗi thẩm mỹ, chưa sửa.
- **Spec pilot:** `sources` đổi về dạng chỉ có link https cho đúng `tests/test_ck_stier.py`. Mô tả các video đã upload giữ nguyên.
- **Generator cũ** `gen_pilot_ck.py` đã khoá (chạy là dừng ngay).
- **Bộ kiểm thử:** 606 đạt, 9 lỗi có từ trước (thiếu `vnlunar`, 5 CLI chưa gọi `utf8_console`, câu lặp cố ý của C6 và ai-voice). Không lỗi nào do thay đổi lần này.
- **Chưa làm:** lint spec trước TTS, `check_gate` cho CK/MIM ở chế độ cảnh báo, P7 (cột ngày hiệu lực trong factcheck), P8 (trạng thái "đã thay" trong store), bài kiểm phông (P2).
