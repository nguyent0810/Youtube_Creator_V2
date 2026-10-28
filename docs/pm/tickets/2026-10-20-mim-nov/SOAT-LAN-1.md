# SOÁT LẦN 1 - Short MIM tháng 11 (20/10/2026)

Phạm vi: 15 bài đã có `final.mp4` tại thời điểm soát (log: 15 dòng `OK`). Không dựng lại, không đăng, không sửa spec/state.
Cách soát: đọc `final_sheet.jpg` từng bài, tách khung rõ hơn bằng ffmpeg ở cảnh nghi ngờ, đối chiếu `data/stier/specs/<slug>.json` và `timing.json`.

Chưa dựng xong (không soát được):
- `mim-cuda-canh-bac-2006` và `mim-tahoe-44-trieu-hinton`: chỉ có voice.wav/timing.json, không có final.mp4. Log ghi FAIL: chữ kinetic rộng hơn khung ("IAN BUCK" size 190, "PHÒNG THÍ NGHIỆM" size 130; "3 NGƯỜI" size 280, "44 TRIỆU ĐÔ" size 200 và một dòng sub size 50). Cần bỏ `size` để engine tự co, rồi chạy lại. Spec của hai bài này chưa soát hình.
- Các slug còn lại trong `mim_nov_order.txt` chưa tới lượt.

## Tổng hợp

| Slug | Giây | Kết luận |
|---|---|---|
| mim-watson-lickel-nha-hang-im-lang | 30.2 | CHẶN (2 cảnh) |
| mim-nghin-may-chu-con-ba-2013 | 31.4 | CHẶN (1 cảnh) |
| mim-watson-buoi-tap-kem-mot-nghin-do | 28.2 | CHẶN (1 cảnh) |
| mim-watson-khong-co-tai-oreo | 28.3 | Sạch |
| mim-dgx1-qua-tang-openai-2016 | 36.0 | Sạch (có mục SỬA NÊN) |
| mim-watson-ferrucci-sai-gan-het | 29.1 | Sạch (có mục SỬA NÊN mạnh) |
| mim-fei-fei-li-14-trieu-anh | 32.1 | Sạch (có mục SỬA NÊN) |
| mim-chat-nguoi-la-20-3-2023 | 29.5 | Sạch (có mục SỬA NÊN) |
| mim-patrascu-card-game-2009 | 36.8 | Sạch (hơi dài) |
| mim-samsung-ba-vu-truoc-khi-cam | 28.2 | Sạch (có mục SỬA NÊN) |
| mim-jensen-ha-noi-nha-thu-hai | 33.4 | Sạch (có mục SỬA NÊN) |
| mim-chat-da-xoa-van-bi-giu | 29.9 | Sạch (có mục SỬA NÊN) |
| mim-4500-chat-link-chia-se | 29.6 | Sạch (có mục SỬA NÊN) |
| mim-polaris-2007-2008 | 33.7 | Sạch (có mục SỬA NÊN nhẹ) |
| mim-y-chan-chatgpt-roi-toa-huy-phat | 31.6 | Sạch |

Quy ước CHẶN: tên người thật hiện chữ lớn ngay trên hình người lạ; hoặc chữ/thương hiệu đọc được trong clip. Mọi bài đều không có cảnh trống kéo dài quá khoảng 1 giây (cảnh chỉ có ngày/chữ giữa khung là kiểu thiết kế, chấp nhận).
Độ dài: cả 15 bài nằm 28-37 s; không bài nào bất thường. Hai bài vượt 35 s (dgx1 36.0, patrascu 36.8) và bốn bài dưới 29 s: CHẤP NHẬN.

## Chi tiết theo slug

### mim-watson-lickel-nha-hang-im-lang (30.24 s) - CHẶN
| # | Loại | Cảnh / thời điểm | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | CHẶN (giả danh) | Cảnh 3 kinetic, ~8-12 s, clip `pexels:6951584` | Nhãn "KEN JENNINGS" chữ lớn đè lên phụ nữ ngồi xem tivi. Người xem sẽ hiểu đó là Ken Jennings | Đổi clip sang `pexels:28679682` (tivi cổ trong phòng khách, không có người; hợp câu "cả quán nín lặng xem") |
| 2 | CHẶN (giả danh) | Cảnh 6 kinetic, ~16-19 s, clip `pexels:7643614` | Nhãn "PAUL HORN" đè lên nhóm 4 người ở văn phòng quanh laptop (người lạ) | Đổi clip sang `pexels:36392049` (đường mạch neon trừu tượng, không có người) hoặc bỏ clip, giữ nền tối |
| 3 | SỬA NÊN | Cảnh 1, ~0.8 s, `pexels:38406367` | Có nhân viên phục vụ đi ngang khung, chữ "CẢ NHÀ HÀNG · BỎ BỮA" chạy hiện dần đè lên bàn ăn; chỉ là hoạt ảnh, sau đó đọc được | Giữ |
| 4 | CHẤP NHẬN | Cảnh cuối, `pexels:7402582` | Bàn ghế trống khớp "nhà hàng im lặng"; chữ không tràn | Giữ |
| 5 | Tốt | Cảnh 8 (bảng "KHÔNG LỜI / ĐẦY NGÔN NGỮ"), cảnh counter "74 VÁN" | Rõ, khớp lời | Giữ |

### mim-nghin-may-chu-con-ba-2013 (31.38 s) - CHẶN
| # | Loại | Cảnh / thời điểm | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | CHẶN (chữ/thương hiệu trong clip) | Cảnh 1 kinetic "1.000 / MÁY CHỦ", 0-1.9 s, clip `pexels:39645503` | Trên màn hình trong clip đọc được "MERCEDES-BENZ GLC 300 Coupé" (tên hãng + tên xe); phía dưới còn khung chat của một ứng dụng nhắn tin. Cũng lệch nghĩa: không phải máy chủ | Đổi sang `pexels:36392049` (mạch neon trừu tượng) hoặc `pexels:7688618` (bàn tay robot trước tivi) |
| 2 | CHẤP NHẬN | Cảnh "JEFF DEAN / ANDREW NG", ~12-15 s, clip `pexels:17518183` | Điện thoại đặt trên giá + bàn phím + bảng màu; không có người nên không giả danh, nhưng cũng không liên quan nghĩa | Giữ (tuỳ ý đổi cùng clip ở mục 1) |
| 3 | CHẤP NHẬN | ~6-8 s ("Chưa ai bảo nó: đây là mèo.") | Nửa khung chỉ có một dòng chữ giữa nền tối; là cảnh `question`, chữ đủ lớn | Giữ |
| 4 | Tốt | Biểu đồ cột 1.000 -> 3 và slam "1.000 -> 3" cuối | Số liệu rõ, đúng lời | Giữ |

### mim-watson-buoi-tap-kem-mot-nghin-do (28.18 s) - CHẶN
| # | Loại | Cảnh / thời điểm | Vấn đề | Đề xuất |
|---|---|---|---|---|
| 1 | CHẶN (giả danh + chữ trong clip) | Cảnh 1 kinetic, 0-2.5 s, clip `pexels:40122777` | Nhãn "KÉM 1.000 ĐÔ / Ken Jennings · Watson" đè lên một người đàn ông trẻ đứng sau bục phát biểu. Phần dưới bục đọc được chữ trên huy hiệu ("... Graduate College") | Đổi sang `pexels:7688618` (bàn tay robot trước tivi cổ; gợi người - máy, không có mặt người) hoặc `pexels:6977375` (tivi nhiễu) |
| 2 | SỬA NÊN | Cảnh cuối `pexels:7005913` ("LÊN SÓNG") | Chữ "LÊN SÓNG" và dòng phụ cắt ngang tượng cúp ở giữa khung, hơi rối | Đẩy chữ lên nửa trên khung hoặc giảm veil |
| 3 | CHẤP NHẬN | Cảnh đồng hồ `pexels:31423053` (~20-22 s) | Mặt đồng hồ kiểu nhà ga có dòng chữ nhỏ không đọc được ở kích thước phát | Giữ |
| 4 | Tốt | Bảng điểm "WATSON 4.400 / JENNINGS 3.400 / RUTTER 1.200" | Số khớp lời, không có người giả | Giữ |

### mim-watson-khong-co-tai-oreo (28.26 s) - Sạch
- Clip: máy quay trường quay (`39402054`), khán giả (`8717005`), người cầm micro (`8246857`) đều không có nhãn tên người trên hình; tên "Ken Jennings", "Alex Trebek" chỉ nằm trong cảnh chữ nền tối. Không logo.
- CHẤP NHẬN: dòng nguồn trong thẻ trích dẫn ("ALEX TREBEK · BẢN TIN AP") chữ rất nhỏ.
- CHẤP NHẬN: người đàn ông cầm micro (`8246857`) minh hoạ chung chung cho "thắng cuộc thi"; không có tên nên không đánh lừa.
- Tốt: bảng "bánh Oreo / thập niên nào?" và cảnh "CÙNG MỘT ĐÁP ÁN SAI"; kể chuyện rõ.

### mim-dgx1-qua-tang-openai-2016 (35.99 s) - Sạch
- SỬA NÊN: cảnh 1 (`6170600`, người giao hàng bốc thùng cạnh xe) dưới câu "Ông chủ Nvidia tự mang quà": người xem dễ hiểu đó là Jensen Huang. Không có nhãn tên nên chưa tới mức chặn. Nếu rảnh đổi sang `pexels:6269877` đã dùng ở cảnh sau hoặc một clip hộp quà không có người.
- SỬA NÊN: cảnh `34336609` (lưới 3D vàng-xanh, "theo cách Nvidia gọi / SIÊU MÁY TÍNH AI ĐẦU TIÊN") dòng chữ thứ hai mờ, tương phản thấp khi mới hiện.
- CHẤP NHẬN: 36 s, hơi quá mục tiêu 35 s.
- Tốt: thẻ "8 GPU", thẻ giá "KHOẢNG 129.000 ĐÔ", sơ đồ mốc 12.2015 / 08.2016.

### mim-watson-ferrucci-sai-gan-het (29.06 s) - Sạch (một mục SỬA NÊN mạnh)
- SỬA NÊN (mạnh): clip `7812440` (3 người đàn ông bên bảng trắng) ở 0-2.7 s; khi cảnh "2006 / DAVID FERRUCCI · IBM" chạy, chữ "DAVID" hiện cạnh đầu một người trong clip. Có thể bị hiểu là Ferrucci. Đề xuất đổi clip sang `pexels:7688618` hoặc `pexels:36392049`.
- CHẤP NHẬN: hai cảnh đồng hồ cát (`7703943`, `7955145`) là ẩn dụ thời gian; nền tối, nửa khung gần như chỉ có chữ số lớn.
- Tốt: counter 15 %, thẻ "ĐÚNG TỚI 95%" và "NHANH GẤP ĐÔI", "4 NĂM" cuối.

### mim-fei-fei-li-14-trieu-anh (32.05 s) - Sạch
- SỬA NÊN: cảnh 1 (`6549271`, người phụ nữ bước ra giữa giá sách) dưới câu "Cô muốn gom ảnh cho mọi danh từ". Chỉ thấy dáng tối, nhưng khớp "cô" nên có thể bị hiểu là Fei-Fei Li. Đổi sang cảnh thư viện không có người nếu có.
- SỬA NÊN: cảnh "HƠN 160 TRIỆU" (`3627321`, người cuộn ảnh trên điện thoại) chữ đè lên đúng chỗ ngón tay; vẫn đọc được.
- CHẤP NHẬN: khoảng 27-28 s, nửa khung gần trống (chỉ có phụ đề) giữa "Thiếu bộ ảnh ấy..." và slam cuối, ngắn.
- Tốt: lớp lớp "49 NGHÌN NGƯỜI", "14 TRIỆU ẢNH", bảng "BỘ ẢNH + HAI CARD".

### mim-chat-nguoi-la-20-3-2023 (29.49 s) - Sạch
- SỬA NÊN: thẻ cards3d "TRONG THANH LỊCH SỬ" đọc thành "thanh lịch sử" dễ gây hiểu nhầm; lời đọc là "trong lịch sử chat". Đề xuất đổi chữ thành "TRONG LỊCH SỬ CHAT".
- SỬA NÊN: cảnh `35158244` (mạng tím) chữ "số người thực sự bị lộ · theo OpenAI" rất nhỏ và mờ trên nền tím.
- CHẤP NHẬN: các cảnh chỉ có chữ ("NGỪNG HOẠT ĐỘNG", "ĐI NHẦM NGƯỜI") nửa khung trống nhưng là slam chủ ý.
- Tốt: sổ tay "Một yêu cầu bị huỷ / KẾT NỐI TRẢ NHẦM DỮ LIỆU", cảnh cuối bóng người trong sương hợp "người lạ".

### mim-patrascu-card-game-2009 (36.79 s) - Sạch
- CHẤP NHẬN: 36.8 s, vượt mục tiêu 35 s khoảng 2 s.
- CHẤP NHẬN: cảnh đầu (`4708325`, tay lắp phần cứng) và cảnh tiền (`6700011`) là minh hoạ chung, không có tên người trên hình; tên Relu Patrascu nằm ở thẻ chữ.
- Tốt: quạt RGB cho "NÓNG · NGỐN ĐIỆN", bảng "HAI LỰA CHỌN".

### mim-samsung-ba-vu-truoc-khi-cam (28.17 s) - Sạch
- SỬA NÊN: cảnh cuối (`26586645`, hàng khoá tình yêu trên hàng rào) chữ ngày "11.03.2023" của cảnh timeline lộ mờ qua clip (chồng chữ ở đầu cảnh). Ẩn dụ "cấm" bằng ổ khoá cũng hơi xa nghĩa; có thể đổi sang clip ổ khoá đơn.
- CHẤP NHẬN: cảnh 1 và 2 hiện chữ "SAMSUNG · 2023" trên người đàn ông trong hành lang kính; không có logo trong clip, không có tên người, nhưng minh hoạ chung dễ bị hiểu là cảnh thật ở Samsung (mô tả video đã ghi "video minh hoạ lấy từ Pexels").
- Tốt: "3 VỤ", thẻ "HAI LẦN DÁN VÀO", "KHÔNG XÁC NHẬN".

### mim-jensen-ha-noi-nha-thu-hai (33.43 s) - Sạch
- SỬA NÊN: cảnh VinBrain (`7195646`, nữ bác sĩ da trắng đeo tai nghe) trên chữ "MUA LẠI VINBRAIN / công ty Việt Nam": người xem dễ nghĩ đó là nhân viên VinBrain. Đổi sang clip không có người (mạch neon `36392049`) hoặc phòng khám trừu tượng.
- CHẤP NHẬN: cảnh cuối (`36209988`) phố có xe máy, biển cửa hàng nhỏ không đọc được, một xe có biểu tượng hãng rất nhỏ.
- CHẤP NHẬN: ở ~22 s bảng "Trung tâm của Viettel" hiện trên nền clip sáng; vẫn đọc được nhờ gradient.
- Tốt: thẻ trích dẫn đủ nguồn, cảnh phố Hà Nội mở đầu.

### mim-chat-da-xoa-van-bi-giu (29.87 s) - Sạch
- SỬA NÊN: cảnh 1 (`5637306`) có người đàn ông áo vest mờ phía sau búa gõ, dưới câu "thẩm phán bảo giữ lại"; thẩm phán là bà Ona Wang. Nên đổi sang clip búa thẩm phán không có người.
- SỬA NÊN: cảnh trích dẫn (`7812445`, hai người đàn ông tranh luận) có dòng ghi nguồn "BRAD LIGHTCAP · COO OPENAI" cỡ nhỏ: tên thật cạnh người lạ. Chữ nguồn rất nhỏ nên chưa chặn; nếu đổi clip thì dùng cảnh không người.
- CHẤP NHẬN: ~25 s hiệu ứng nhiễu chữ "BẢN ĐÃ GIỮ VẪN CÒN" trước khi rõ (hiệu ứng glitch).
- Tốt: counter "30 NGÀY", bảng "NEW YORK TIMES KIỆN OPENAI", ngày 26.09.2025.

### mim-4500-chat-link-chia-se (29.55 s) - Sạch
- SỬA NÊN: cảnh mở đầu (`9757994`, người đeo kính râm gõ phím, mã đỏ trên áo) gợi "hacker" trong khi nội dung nhấn "không ai bị hack". Nên đổi sang clip tìm kiếm / màn hình laptop không có mặt người.
- CHẤP NHẬN: khung trích dẫn "Một thử nghiệm ngắn ngủi" trống nửa giây đầu rồi chữ hiện.
- Tốt: hai thẻ "TÊN THẬT / HỒ SƠ XIN VIỆC", sổ tay "Hai cú bấm", "MỘT CÁNH CỬA chính chủ đã mở".

### mim-polaris-2007-2008 (33.74 s) - Sạch
- SỬA NÊN (nhẹ): tiêu đề chạy ở góc trên cố định "VANCOUVER · 2007" giữ nguyên suốt các cảnh 2008 / Las Vegas.
- SỬA NÊN (nhẹ): cảnh bàn tay robot (`6153725`) chữ "ĐỔI CHỖ" nằm đè lên bàn tay, tương phản thấp khi mới hiện.
- CHẤP NHẬN: ~12 s nửa khung trống giữa hai cảnh (bảng vừa tắt); ngắn. Clip phố đêm (`35304178`) dùng cho "Las Vegas" là minh hoạ chung.
- Tốt: biểu đồ "SỐ TRẬN MÁY THẮNG 1 -> 2", bảng "VANCOUVER 2007 · 4 PHIÊN", tên Laak/Eslami chỉ ở cảnh chữ.

### mim-y-chan-chatgpt-roi-toa-huy-phat (31.63 s) - Sạch
- Không có người thật gắn tên trên hình, không logo, chữ không tràn.
- CHẤP NHẬN: ~18-20 s một nhịp gần trống khi sổ "KHOẢN PHẠT" tắt.
- Tốt: lịch gạch chéo "GẦN MỘT THÁNG BỊ CHẶN", thẻ "THIẾU THÔNG BÁO / THIẾU CƠ SỞ PHÁP LÝ", ba mốc 2023 / 2024 / 2026.

## Gợi ý sửa gộp (chỉ spec, khi được phép)
1. Lickel: cảnh 3 `6951584` -> `28679682`; cảnh 6 `7643614` -> `36392049`.
2. Nghìn máy chủ: cảnh 1 `39645503` -> `36392049` (hoặc `7688618`).
3. Buổi tập kém một nghìn đô: cảnh 1 `40122777` -> `7688618`.
Poster đã xem để chọn: 36392049 (mạch neon hồng-tím, không chữ), 7688618 (tay robot xanh trước tivi cổ), 28679682 (tivi cổ trong phòng khách), 6977375 (tivi nhiễu trên nền vàng).
