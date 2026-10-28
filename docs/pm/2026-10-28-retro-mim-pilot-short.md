# Retro lô pilot hook MIM (6 Short, đăng 28/10/2026)

Phạm vi: chỉ đọc. Đã xem ticket, kịch bản, factcheck, báo cáo Codex vòng 1 / vòng 2 / agy, spec `mim-p1`–`mim-p6`, `build.py`, `clips.py`, `casefile.js`, `beat.js`, `beat.css`, và contact sheet p1 cùng p6. Không sửa code, không gọi API, không chạy git.

Sáu bài private, 15:00 VN: p1 `GkskSEnDiyI` 13/11, p2 `4ZOrJGfxG0g` 14/11, p3 `BP6cmcFTDUs` 15/11, p4 `l_4DmvqWlGA` 16/11, p5 `0SzJIAebHR4` 17/11, p6 `b-GUkOrAcc0` 18/11. Hook trong spec đã đăng: A, B, B, A, A, B. Câu mở p6 đã đăng là "Video bạn vừa lướt qua…"; cụm "Theo YouTube năm 2021" nằm ở câu đọc thứ hai.

Sheet của bản đã đăng:
- p1 cảnh 0 là `pexels:38410499`: hai tay cầm điện thoại, trên màn hình có mặt người. Clip sợi quang `39687575` không còn.
- p1 cảnh hậu trường là `pexels:34536743`: cửa sổ tròn trường quay, có người vận hành máy. Không còn khung người phụ nữ dễ đọc thành Johansson.
- p1 cảnh kết vẫn là `pexels:38410501`: một tay, màn hình điện thoại có mặt người. Bài đã hẹn giờ. Retro không sửa spec.
- p6 cảnh số là `counter` "HƠN 80 TỈ", không còn biểu đồ một cột. Board tín hiệu xếp dọc.

## Tám sự cố

**1. Codex không render được (EPERM npm)**
- Nguyên nhân: `build()` trong `motion/stier/build.py` (khoảng dòng 783) gọi `npx.cmd -y -p node@22 -p hyperframes@0.8.75 hyperframes render`. Sandbox Codex chặn ghi npm cache và chặn spawn (`spawn EPERM`). Codex thử ba chỗ đặt cache. `--no-render` trả về trước lệnh npx (dòng 780), nên lint spec vẫn chạy.
- Cổng hiện có: chưa có bước thử spawn. Brief vòng 1 vẫn giao render cho Codex.
- Chốt: `render_preflight()` ngay trước lệnh npx. Spawn `npx.cmd --version`. `PermissionError` hoặc stderr chứa `EPERM` thì `SystemExit` mã `sandbox-no-render`, và dừng. Test trong `tests/test_stier_media.py`: mock `run()` trả `EPERM` → đúng mã, lệnh `hyperframes render` không bị gọi lần hai.

**2. Clip mở p1 trông như sinh vật**
- Nguyên nhân: cảnh 0 vòng 1 là `pexels:39687575` (`abstract-glowing-fiber-optic-light-display`). `clips.ensure()` chỉ chọn file theo độ phân giải (`pick_file`). Tiêu đề và poster không vào lint. Brief vòng 1 chỉ cấm logo và chữ đọc được, nên clip trừu tượng được chọn.
- Cổng hiện có: soát poster làm tay. `ensure()` không có danh sách đen.
- Chốt: dict `DENY` trong `motion/stier/clips.py`. `ensure()` đối chiếu `ref` trước khi tải. Hạt giống: `pexels:39687575`. Test: `ensure("pexels:39687575")` → `SystemExit`. Bản đã đăng đã đổi cảnh 0 sang `pexels:38410499`. Sheet p1 cho thấy clip mới vẫn là điện thoại, trên màn hình có mặt người. Cùng họ với sự cố 7, nên `38410499` cũng vào `DENY`.

**3. Clip hậu trường p1 có một phụ nữ thật**
- Nguyên nhân: cảnh "đoạn hậu trường thật" của bản render mẫu có một phụ nữ, dễ đọc thành Scarlett Johansson. Đã đổi sang `pexels:34536743` (`behind-the-scenes-film-set-camera-operation`). Sheet p1 đã đăng là cửa sổ tròn trường quay, có người vận hành máy. Id clip cũ không còn trong spec và không nằm trong bốn clip vòng 1 (đều trừu tượng). Log vòng 2 có ứng viên đúng kiểu lỗi: `pexels:39690158` (`elegant-woman-in-yellow-dress-on-red-carpet`). Brief cấm ảnh người thật. Máy không đọc tiêu đề Pexels.
- Cổng hiện có: chưa có.
- Chốt: trong `ensure()`, khi index đã có `title`, từ chối title khớp `\b(woman|man|people|girl|boy|actress|actor|face|crowd)\b`. Test: title `…woman…red-carpet-39690158` bị chặn; title `behind-the-scenes-film-set-camera-operation-34536743` được giữ.

**4. Từ "không" trong `acc` bị đóng khung riêng**
- Nguyên nhân: `plan()` (`build.py` 576–583), spec `mix`, lấy từng mục `acc`, `norm()`, rồi khớp từng từ của dòng kinetic `sync`. Từ khớp nhận class `emw` (`beat.js`). CSS `.kin .sw.emw` (`beat.css`) quét hộp đỏ sau đúng một từ và đổi chữ sang màu tối. Vòng 1, p3 có `"acc"` chứa `"không"`. Cùng cơ chế: p4 có từ đơn `"một"`, nên "MỘT" trong "MỘT NHÓM DUY NHẤT" bị khung riêng. Cụm `"không phẩy bảy"` là một chuỗi; `norm` dính thành `khôngphẩybảy`, không khớp từ "không".
- Cổng hiện có: `mix_lint` không xem `acc`.
- Chốt: `acc_lint(spec)` trong `build()`, trước `speak()` (cạnh luật 55–135 từ). Mục `acc` tách ra còn một token thuộc {không, chẳng, chưa, đừng, một, các, những, của, và, là} thì `SystemExit`. Test: `["không"]` và `["một"]` lỗi; `["không phẩy bảy"]` và `["đứng đầu"]` sạch.

**5. Vòng 2, câu mở p6 (hook B) bắt đầu bằng "Theo YouTube năm 2021"**
- Nguyên nhân: Codex đưa nhãn nguồn lên đầu câu. Đó là khuôn hook A (dữ kiện có ngày, về thế giới bên ngoài). `pilot.hook` của p6 là `"B"`: tình huống của người xem, có "bạn". Báo cáo r2 ghi đúng câu mở đó. Spec và sheet đã đăng đã sửa: `lines[0]` là "Video bạn vừa lướt qua…"; "Theo YouTube năm 2021" là `lines[1]`, trên hình là nhãn dưới số.
- Cổng hiện có: `script_lint.py` chỉ chạy khi `theme == "bud"`.
- Chốt: `pilot_lint(spec)` trong `build()`, trước `speak()`, khi có `pilot.hook`. Hook B: câu 0 chứa "bạn" và không khớp `^(Theo|Tháng|Năm|Ngày)\b`. Hook A: câu 0 có năm hoặc "tháng". Test: câu r2 của p6 lỗi; câu đã đăng của p6 sạch; câu p1 "Tháng 10 năm 2023…" sạch.

**6. Câu mở p2 khó đọc, sát ý "3 giây là đủ cho kẻ gian"**
- Nguyên nhân: bản r2 là một cụm không dấu ngắt: "Tin nhắn thoại ba giây bạn gửi dài bằng mẫu giọng mà một mô hình nghiên cứu dùng năm 2023." Factcheck (rủi ro 14/11) và brief vòng 2: 3 giây chỉ là thông số mô hình nghiên cứu, chưa mở cho công chúng. "dài bằng mẫu giọng" dính tin nhắn của người xem vào mẫu đó. Luật nằm trong văn bản. Spec đã đăng tách câu: "…có dài hơn ba giây không? Năm 2023, một mô hình nghiên cứu chỉ cần ba giây giọng mẫu."
- Cổng hiện có: chưa có.
- Chốt: cùng `pilot_lint`, slug `mim-p2-tin-nhan-thoai`. Câu có "ba giây" thì cấm "đủ", "dài bằng", "kẻ gian"; câu đó phải chứa "mô hình" hoặc "nghiên cứu"; câu 0 phải có dấu ngắt trước từ thứ 16. Test: câu r2 lỗi; câu đã đăng sạch.

**7. Agy: UI điện thoại, nút board đè nhau, chữ terminal**
- UI điện thoại. Nguyên nhân: `pexels:38410501` (`scrolling-through-social-media-on-smartphone`) lộ giao diện và mặt người trên màn hình. Codex vòng 2 gắn vào bốn bài: p2, p3, p4, p6. Agy đã thay ở bốn bài đó. Cổng hiện có: `ensure()` không đọc title "social-media" / "smartphone". Chốt: cùng `DENY` mục 2, cộng `clip_lint` quét `scenes[].clip` trước `speak()`. Test: spec chứa `38410501` hoặc `38410499` thì `SystemExit`. Sheet p1 đã đăng vẫn có cả hai.
- Nút board. Nguyên nhân: `B.board` (`casefile.js`) vẽ đúng `x, y`, không đo chồng. Ba nút `circle` cùng `y: 0.5`, rộng khoảng 420–640 px, trên bảng 940 px, nên elip đè nhau (p2 cảnh 5, p3 cảnh 3, p5 cảnh 6, trước khi agy xếp dọc). Cổng hiện có: `check_gate()` chỉ chạy khi `theme == "bud"` và `v2`, và cần npm. Chốt: `board_lint(scene)` trước `speak()`. Từ 3 nút thì cùng `x`, và các hộp không giao. Hộp ước lượng như engine: rộng lấy `w` hoặc 640, cao `fs + 54`, tâm `(x * 940, y * 880)`. Test: ba nút `y = 0.5` và khác `x` thì lỗi; `x = 0.5` với `y` 0,25 / 0,50 / 0,75 thì sạch.
- Chữ terminal. Nguyên nhân: `pexels:28709421` (`digital-data-display-on-screen`) ở p5 cảnh 4 có dòng đọc được `bytes=32 tiempo=10ms TTL=60`. Cổng hiện có: title "digital-data-display" không bị chặn. Chốt: đưa id vào `DENY`. Test: `ensure("pexels:28709421")` → `SystemExit`.

**8. p6 biểu đồ một cột, khung gần trống khoảng 3 giây**
- Nguyên nhân: cảnh 1 vòng 2 là `chart` / `bars` với một cột "HƠN 80 TỈ", `at` neo vào một từ giữa câu. `B.chart` để cột rộng tối đa 260 px và mọc tại `b.at`. Trước mốc đó khung còn tiêu đề và lưới. `qa_short()` gọi `qa_blank.scan` rồi chỉ in, không `SystemExit`. Lưới mảnh có thể vượt `THRESH = 9`, nên mắt thấy trống mà cổng im. Claude đã đổi sang `counter` `from = to = 80`. Sheet p6 đã đăng là số "HƠN 80 TỈ", không còn cột.
- Cổng hiện có: `qa_blank` không chặn, và không biết "một cột".
- Chốt: trong `build()`, trước `speak()`, cạnh kiểm CSS `.chbar`: `type == "chart"` và `len(bars) < 2` thì `SystemExit`, và chỉ đường sang `counter` với `from == to`. Test: một cột "HƠN 80 TỈ" lỗi; counter 80→80 sạch.

## Đổi gì trong brief cho agent

- Codex không render. Gặp mã `sandbox-no-render` thì dừng và báo, không đổi npm cache.
- Hook B: câu 0 có "bạn", và không bắt đầu bằng "Theo", "Tháng", "Năm", "Ngày".
- `acc` không chứa từ phủ định hay từ đơn "một". Board từ 3 nút thì xếp dọc, cùng `x`.
- Cấm `pexels:39687575`, `38410499`, `38410501`, `28709421`, và mọi title Pexels có woman, man, people, face.
- p2: "ba giây" đi cùng "mô hình nghiên cứu"; cấm "đủ", "dài bằng", "kẻ gian". Một số thì dùng `counter`, không dùng biểu đồ một cột.
