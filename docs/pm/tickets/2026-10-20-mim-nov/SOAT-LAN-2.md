# SOÁT LẦN 2 - Short MIM tháng 11 (21/10/2026)

Phạm vi: 25 bài còn lại (mọi slug trong `mim_nov_order.txt` không nằm trong SOAT-LAN-1) + soát lại 4 bài đã sửa/dựng lại. Không dựng lại, không đăng, không sửa spec/state.
Cách soát: đọc `final_sheet.jpg`, tách khung bằng ffmpeg ở cảnh nghi ngờ, đối chiếu spec/timing. Tổng 29 bài.

## Kết quả

CHẶN: 6 bài. Sạch (không CHẶN, không SỬA NÊN đáng kể): 12 bài. Còn lại có SỬA NÊN. Bốn bài soát lại: 3 bài đã hết lỗi CHẶN cũ; riêng `mim-watson-buoi-tap-kem-mot-nghin-do` hết lỗi cũ nhưng lòi lỗi CHẶN mới (xem dưới).

| Slug | Giây | Kết luận |
|---|---|---|
| mim-cuda-canh-bac-2006 | 34.7 | SỬA NÊN mạnh (thương hiệu card mờ) |
| mim-tahoe-44-trieu-hinton | 35.4 | SỬA NÊN nhẹ |
| mim-jeopardy-julann-tren-may-bay | 34.5 | Sạch |
| mim-meta-ai-sua-xe-cong-khai | 32.5 | Sạch |
| mim-face-id-san-khau-2017 | 29.7 | SỬA NÊN (chữ chồng, clip lệch nghĩa) |
| mim-altman-khong-nhu-bac-si | 31.5 | CHẶN |
| mim-viola-jones-2001-may-tim-mat | 30.5 | Sạch (board chồng nhẹ) |
| mim-elias-bai-toan-to-bip | 35.3 | SỬA NÊN (clip cờ vua lệch poker) |
| mim-nist-2018-bon-nam-20-lan | 29.7 | Sạch |
| mim-deepseek-kho-chat-khong-mat-khau | 29.0 | Sạch (SỬA NÊN nhẹ) |
| mim-facenet-2015-mot-tram-hai-muoi-tam-byte | 31.0 | CHẶN |
| mim-sandholm-hai-cap-doi-than | 34.4 | CHẶN |
| mim-robert-williams-2020-theo-aclu | 31.6 | Sạch |
| mim-game-dendi-2017 | 29.4 | CHẶN |
| mim-deepface-2014-bon-trieu-khuon-mat | 29.3 | SỬA NÊN nhẹ |
| mim-game-tlo-thua-roi-viet-luat | 32.0 | Sạch |
| mim-game-khan-gia-chon-tuong-hai-may | 27.3 | SỬA NÊN nhẹ (hơi ngắn) |
| mim-jason-les-ba-co-may | 32.9 | Sạch |
| mim-joy-buolamwini-mat-na-trang-2018 | 33.3 | Sạch (SỬA NÊN nhẹ) |
| mim-game-google-mua-atari-2014 | 33.4 | Sạch |
| mim-facebook-xoa-mot-ti-mau-khuon-mat-2021 | 27.7 | Sạch |
| mim-game-mana-thua-nam-van-roi-thang | 29.2 | CHẶN |
| mim-game-alpha-red-tran-thang-dau | 33.0 | SỬA NÊN (cảnh gần trống ~4 s) |
| mim-game-tai-khoan-an-danh-grandmaster | 32.4 | Sạch |
| mim-game-og-thua-may-roi-vo-dich | 33.4 | Sạch (SỬA NÊN nhẹ) |
| **Soát lại** mim-watson-lickel-nha-hang-im-lang | 30.9 | Hết CHẶN cũ, sạch |
| **Soát lại** mim-nghin-may-chu-con-ba-2013 | 32.0 | Hết CHẶN cũ, sạch |
| **Soát lại** mim-watson-buoi-tap-kem-mot-nghin-do | 28.8 | Hết CHẶN cũ; CHẶN MỚI (đồng hồ MONDAINE) |
| **Soát lại** mim-chat-nguoi-la-20-3-2023 | 30.1 | Sạch |

Độ dài: 27.3-35.4 s; không bài nào bất thường. Tahoe (35.4), elias (35.3) vượt nhẹ 35 s: CHẤP NHẬN. khan-gia (27.3), facebook (27.7) hơi ngắn: CHẤP NHẬN.

## Danh sách CHẶN và đề xuất sửa

| Slug | Cảnh / clip | Vấn đề | Sửa đề xuất |
|---|---|---|---|
| mim-altman-khong-nhu-bac-si | Cảnh cuối "THEO CHÍNH ALTMAN" (~29-31 s) trên clip bác sĩ phẫu thuật (ống tiêm); cảnh thẻ trích "- SAM ALTMAN" (~17-19 s) phủ lên đầu một người lạ quay lưng | Nhãn/tên người thật đè lên người lạ; cảnh cuối còn gây hiểu nhầm Altman là bác sĩ | Đổi cả hai clip sang không có người: `pexels:36392049` (mạch neon) hoặc `pexels:28679682` (tivi cổ). Cảnh cuối có thể giữ chủ đề y khoa bằng clip dụng cụ y tế không có người nếu tìm được trong index |
| mim-facenet-2015-mot-tram-hai-muoi-tam-byte | Cảnh 1 "2015", 0-2 s, clip `coverr:HrWOLrRiqp` | Màn hình terminal đọc được "apt.datadoghq.com" (tên công ty) | Đổi sang `pexels:36392049` hoặc `pexels:7688618`; hoặc làm mờ mạnh clip. Clip cuối `pexels:8721655` (tai nghe + bàn phím) chấp nhận |
| mim-sandholm-hai-cap-doi-than | 4 cảnh liên tiếp "TUOMAS SANDHOLM" (~12-20 s), clip `pexels:35163081` | Người đàn ông trẻ viết bảng đen bị gắn tên giáo sư Sandholm (giả danh) | Đổi sang clip bảng đen/công thức không có người, hoặc `pexels:36392049` |
| mim-game-dendi-2017 | Cảnh 1 "DENDI / THUA MỘT CỖ MÁY", 0-2.5 s, clip `pexels:6651626` | Hai người đàn ông chơi tay cầm trên sofa bị gắn tên Dendi | Đổi sang `pexels:36392049` (neon) hoặc `pexels:8087317` (robot, đã dùng trong bài) |
| mim-game-mana-thua-nam-van-roi-thang | Cảnh 1 "MANA thua 0-5, rồi thắng", 0-2 s, clip `pexels:7914934` | Cô gái đeo tai nghe bị gắn tên MaNa (tuyển thủ nam) | Đổi sang clip bàn phím/màn hình không có người (đã có clip bàn phím xanh `pexels:35281906` trong bài) |
| mim-watson-buoi-tap-kem-mot-nghin-do | Cảnh đồng hồ ~18-21 s, clip `pexels:31423053` | Mặt đồng hồ đọc rõ "MONDAINE / SBB CFF FFS / OFFICIAL SWISS RAILWAYS CLOCK DESIGN" (thương hiệu). Lần 1 ghi "không đọc được": sai, ở độ phân giải thật đọc được | Đổi sang clip đồng hồ không chữ trên mặt hoặc `pexels:36392049`; chữ "KHÔNG AI SAI câu nào" giữ nguyên |

## Chi tiết theo slug (ngoài CHẶN)

### mim-cuda-canh-bac-2006 (34.7 s)
- SỬA NÊN mạnh: cảnh cuối `pexels:6705180` (card đồ hoạ) thấy mảnh chữ "ZO.." trên vỏ quạt (có vẻ hãng card), chữ đè giữa khung; cảnh 1 `34280528` có biểu tượng cube mờ ở dưới trái. Chưa đọc trọn nên không CHẶN, nhưng nên đổi clip cuối sang `pexels:36392049` nếu còn dịp.
- SỬA NÊN: cảnh "GIÁ VÔ VE" ban đầu rất mờ; dòng phụ cảnh 2012 nhỏ.
- Tốt: cuốn vở "Brook: viết toán như toán", thẻ chi phí 50 %/30 %.

### mim-tahoe-44-trieu-hinton (35.4 s)
- SỬA NÊN: cảnh 1 "3 NGƯỜI" trên clip hai thanh niên (người lạ, không nhãn tên), hơi lệch ("ba người" nhưng thấy hai).
- CHẤP NHẬN: ~3 s đầu cảnh "BA NGƯỜI ẤY" gần trống trước khi thẻ hiện; clip "CHỌN GOOGLE" người đi bộ cạnh biển cấm, không chữ.
- Tốt: hai thẻ tên Hinton/Alex-Ilya, số 14 -> 44 triệu đô rõ.

### mim-jeopardy-julann-tren-may-bay (34.5 s) - Sạch
- Clip bàn tay cạnh cửa sổ máy bay, tivi vàng nhiễu, cánh máy bay: không chữ, không người nhận diện. Tốt: thẻ "5.280 FEET", đếm ngày 30.03.1964.

### mim-meta-ai-sua-xe-cong-khai (32.5 s) - Sạch
- Thợ máy áo xanh (không mặt, không chữ); chữ "META" chỉ là overlay hoạt ảnh. Clip điện thoại/ tay, người phụ nữ mờ sau thẻ trích: không nhãn tên. Tốt: bảng "Mozilla nói", "HAI PHÍA NÓI".

### mim-face-id-san-khau-2017 (29.7 s)
- SỬA NÊN (mạnh): cảnh sơ đồ "APPLE GIẢI THÍCH" (khoảng 13-21 s): thanh gạch ngang cắt qua tiêu đề và hộp "NHIỀU NGƯỜI CẦM MÁY" chồng lên tiêu đề (4 khung liên tiếp). Đọc được nhưng xấu.
- SỬA NÊN: "SÂN KHẤU · IPHONE X" trên clip hành lang văn phòng hai người đi bộ (không phải sân khấu); "máy demo trên sân khấu" trên clip bàn phím. Lệch nghĩa, không có nhãn tên người nên không CHẶN. Craig Federighi chỉ ở thẻ chữ.

### mim-viola-jones-2001-may-tim-mat (30.5 s) - Sạch
- Camera trong tay, nền sàn chứng khoán mờ; thẻ tên VIOLA/JONES chữ thuần. SỬA NÊN nhẹ: sơ đồ "VỚI MÁY ẢNH LÀ GÌ?" thanh gạch cắt chữ tiêu đề (lỗi sơ đồ chung).

### mim-elias-bai-toan-to-bip (35.3 s)
- SỬA NÊN: cảnh ~18-27 s đặt clip cờ vua (quân cờ, cánh tay robot chơi cờ) dưới nội dung poker/Pluribus; lệch nghĩa. Nên đổi sang clip bài/chip poker (bài `pexels:6700011`/`4708325` từng dùng ở bài Patrascu) hoặc neon.
- SỬA NÊN: "NGƯỜI GIỎI NHẤT THẾ GIỚI" và dòng "điểm mạnh nhất của Pluribus" trên clip cờ vua tương phản thấp, chữ nhỏ.
- Clip đầu (người cầm bài, tím) không nhãn tên; thẻ "DARREN ELIAS" nằm trên nền tối. Không giả danh.

### mim-nist-2018-bon-nam-20-lan (29.7 s) - Sạch
- Đường phố có xe buýt, đám đông tối; không chữ đọc được, không nhãn tên. Tốt: cột biểu đồ 4 % -> 0,2 %, "20 LẦN".

### mim-deepseek-kho-chat-khong-mat-khau (29.0 s) - Sạch
- SỬA NÊN nhẹ: cảnh "TỰ CHẠY LỆNH" (người phụ nữ lớn tuổi ghi sổ ngoài hiên) lệch nghĩa, người lạ không nhãn; chữ "Wiz" trong phụ đề là tên công ty, không phải người. Cửa kim loại/ máy chủ tối: không chữ.

### mim-robert-williams-2020-theo-aclu (31.6 s) - Sạch
- Không có clip người: đêm mờ, kính mưa. "Robert Williams" chỉ ở phụ đề/chữ. Tốt: sơ đồ ACLU, "30 GIỜ", cặp "CHƯA ĐỦ / PHẢI CÓ". SỬA NÊN nhẹ: sơ đồ "THEO HỒ SƠ ACLU" gạch cắt tiêu đề (lỗi sơ đồ chung).

### mim-deepface-2014-bon-trieu-khuon-mat (29.3 s)
- SỬA NÊN nhẹ: cảnh cuối (`pexels:6120117`: biểu đồ chứng khoán + kính lúp, 25-29 s) lệch nghĩa so với "bốn triệu khuôn mặt"; chữ cyan mờ trên nền sáng. Có thể đổi sang clip tối.
- Clip 1 bóng người ngược sáng, không nhãn tên. Tốt: thẻ 97,35 %/97,53 %, "GIẢM HƠN 27 %".

### mim-game-tlo-thua-roi-viet-luat (32.0 s) - Sạch
- Phím bàn phím, mạng tím, bàn nhiều màn hình; "TLO" là chữ thuần trên nền tối. Không người, không logo.

### mim-game-khan-gia-chon-tuong-hai-may (27.3 s)
- SỬA NÊN nhẹ: "2 - 0 máy thắng hai ván đầu" trên clip người đàn ông có râu trước màn hình biểu đồ chứng khoán (lệch nghĩa, người lạ, không nhãn tên); sơ đồ "OPENAI FIVE" ellipse bị ellipse "NGƯỜI CHƠI GIỎI" đè lên.
- CHẤP NHẬN: 27.3 s hơi ngắn.

### mim-jason-les-ba-co-may (32.9 s) - Sạch
- Bàn poker, chip, bài, bàn tay: chip không in chữ; thẻ "CLAUDICO", tên Les chỉ ở chữ nền tối. Cảnh cuối hai bàn tay chạm nhau: hợp "người - máy".

### mim-joy-buolamwini-mat-na-trang-2018 (33.3 s) - Sạch
- SỬA NÊN nhẹ: cảnh 1 "MẶT NẠ TRẮNG máy mới thấy cô" trên clip toà nhà nghiêng trong ảnh nằm giữa cánh đồng hoa; trừu tượng, không liên quan nghĩa nhưng không gây hại. Không có người, không nhãn tên. Tốt: bảng 0,8 % / 34,7 %.

### mim-game-google-mua-atari-2014 (33.4 s) - Sạch
- Toà nhà kính "GOOGLE MUA" là toà nhà chung, không bảng hiệu; băng cartridge kiểu Famicom không đọc được chữ (lệch nhẹ vì không phải Atari). Hầm nhện neon cho "đường hầm Breakout" hợp. Thẻ DEMIS HASSABIS / LEGG · SULEYMAN chữ thuần.

### mim-facebook-xoa-mot-ti-mau-khuon-mat-2021 (27.7 s) - Sạch
- Kính mưa, đường phố đêm: không người nhận diện, không chữ. Sơ đồ "LÝ DO HÃNG NÊU" gạch cắt tiêu đề (lỗi sơ đồ chung). 27.7 s hơi ngắn: CHẤP NHẬN.

### mim-game-alpha-red-tran-thang-dau (33.0 s)
- SỬA NÊN: cảnh "Chiến thắng đầu tiên của con người." (~16-20 s): chỉ một dòng chữ nhỏ ở giữa nền tối, sát hai mép, phụ đề trống khoảng 3-4 s: gần như cảnh trống. Nên làm cảnh có clip hoặc tăng cỡ chữ.
- SỬA NÊN nhẹ: "ALPHA RED · Thái Lan" trên clip người ngồi ghế quay lưng/ bóng (không nhận diện nên chấp nhận).

### mim-game-tai-khoan-an-danh-grandmaster (32.4 s) - Sạch
- Toà nhà đêm, tay gõ phím; chữ không bị chồng. Tốt: ghi chú "Điều kiện như người", thẻ "99,8 % NGƯỜI CHƠI".

### mim-game-og-thua-may-roi-vo-dich (33.4 s) - Sạch
- SỬA NÊN nhẹ: cảnh 1 "NHÀ VÔ ĐỊCH" trên clip sân vận động bóng đá (khán giả vỗ tay), lệch môn (Dota); cầu Golden Gate cho San Francisco hợp; người đàn ông ngồi laptop cho "THUA MÁY" là người lạ không nhãn tên, chấp nhận.

### Soát lại 4 bài
- mim-watson-lickel-nha-hang-im-lang: "KEN JENNINGS" nay trên tivi cổ không người; "PAUL HORN" trên mạch neon; cảnh cuối nhà hàng trống, chữ đọc được. Hết CHẶN.
- mim-nghin-may-chu-con-ba-2013: cảnh 1 nay là bàn tay robot nền tím, không chữ Mercedes. Hết CHẶN. JEFF DEAN / ANDREW NG trên clip điện thoại + bàn phím, không người.
- mim-watson-buoi-tap-kem-mot-nghin-do: cảnh 1 nay là tivi vàng không người, hết lỗi giả danh. Nhưng cảnh đồng hồ có "MONDAINE / SBB CFF FFS" đọc được: CHẶN MỚI (bảng trên). SỬA NÊN còn lại: chữ "LÊN SÓNG" đè tượng cúp.
- mim-chat-nguoi-la-20-3-2023: toàn nền tối, bàn tay/ điện thoại mờ, mạng tím; không người, không chữ trong clip. Sạch.

## Danh sách bài sạch (không CHẶN, không SỬA NÊN đáng kể)
mim-jeopardy-julann-tren-may-bay, mim-meta-ai-sua-xe-cong-khai, mim-viola-jones-2001-may-tim-mat, mim-nist-2018-bon-nam-20-lan, mim-deepseek-kho-chat-khong-mat-khau, mim-robert-williams-2020-theo-aclu, mim-game-tlo-thua-roi-viet-luat, mim-jason-les-ba-co-may, mim-joy-buolamwini-mat-na-trang-2018, mim-game-google-mua-atari-2014, mim-facebook-xoa-mot-ti-mau-khuon-mat-2021, mim-game-tai-khoan-an-danh-grandmaster, mim-game-og-thua-may-roi-vo-dich, cùng ba bài soát lại mim-watson-lickel-nha-hang-im-lang, mim-nghin-may-chu-con-ba-2013, mim-chat-nguoi-la-20-3-2023.

Ghi chú hệ thống: sơ đồ "board" có thanh gạch dưới tiêu đề cắt chữ/ bị hộp con chồng lên ở nhiều bài (face-id nặng nhất). Nên sửa ở engine sau, không chặn đăng.
