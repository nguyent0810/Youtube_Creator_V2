# CLIP-DOI-LAN-1: đổi clip lặp trước khi dựng (T4..T9, 40 spec MIM)

Kết quả: 120 cảnh có clip, 120 id khác nhau (trước: 96 id, 17 id lặp trong 40 spec, 21 id trùng data/stier/specs). Không còn id nào xuất hiện hơn 1 lần và không id nào trùng data/stier/specs. Chỉ dùng pexels. Mọi clip mới đều ≥ 9 giây, đã tải poster về và xem bằng mắt (cột cuối). `ms` (giây bắt đầu trong clip) giữ nguyên, đều ≤ 3 nên vẫn nằm trong clip mới. Lời đọc, số liệu và chữ trên cảnh không đổi; `_selfcheck.py` (mix_lint) của T4..T9 đều OK, đủ M D G, chữ thuần giữ nguyên mức cũ vì không đổi loại cảnh nào.

Quy ước giữ một lần dùng: với id lặp, giữ lần hợp nhất (10374892 giữ ở cuda; 17518183 giữ ở nghìn-máy-chủ; 36392049 giữ ở dendi; 36637656 giữ ở robert-williams; 5377697 giữ ở viola-jones; 6381013 giữ ở altman; 6651626 giữ ở dendi; 7579576 giữ ở khán-giả; 7688618 giữ ở joy; 8091712 giữ ở altman; 8561462 giữ ở 4500-chat (cánh cửa); 8889195 giữ ở tahoe (email); 7279738 giữ ở chat-người-lạ cảnh 0). Id đã dùng ở data/stier/specs thì thay ở mọi cảnh (lần dùng cũ coi là lần giữ). Poster các id giữ cũng đã xem lại; 34679079 và 7643473 (6 giây, màn hình laptop có chữ UI / cảnh bắt tay xa) bị thay cả hai lần.

| slug | cảnh | clip cũ → clip mới | lý do thay / vì sao hợp | đã xem poster |
|---|---|---|---|---|
| mim-cuda-canh-bac-2006 | 9 | pexels:6651626 → pexels:6705180 | lặp 3 lần trong 40 spec. Mới: card đồ hoạ đặt trên nền đen, đúng 'card chơi game', không chữ | có |
| mim-dgx1-qua-tang-openai-2016 | 3 | pexels:34679079 → pexels:34336609 | lặp 2 lần trong 40 spec; chỉ 6s. Mới: địa hình dữ liệu 3D xanh/vàng trên nền tối, gợi siêu máy tính | có |
| mim-fei-fei-li-14-trieu-anh | 4 | pexels:36511035 → pexels:3627321 | ảnh cũ trong hộp, lặp 2 spec. Mới: lướt kho ảnh trên điện thoại, hợp 'lọc hàng trăm triệu ảnh' | có |
| mim-fei-fei-li-14-trieu-anh | 7 | pexels:34393391 → pexels:35010179 | đã dùng ở data/stier/specs. Mới: nơ-ron xanh/tím trên nền tối, đúng 'mạng nơ-ron' | có |
| mim-patrascu-card-game-2009 | 0 | pexels:7311101 → pexels:4708325 | cảnh báo: hình (cốc nước/vẽ gốm/tay sơn) không hợp nội dung; đã dùng ở data/stier/specs. Mới: tay lắp ráp bộ máy tính, đúng 'người dựng máy' | có |
| mim-patrascu-card-game-2009 | 3 | pexels:34268300 → pexels:6700011 | cảnh báo: hình (cốc nước/vẽ gốm/tay sơn) không hợp nội dung. Mới: tay đếm tiền mặt, ý 'nhiều nghìn đô' | có |
| mim-patrascu-card-game-2009 | 5 | pexels:5875724 → pexels:40316891 | cảnh báo: hình (cốc nước/vẽ gốm/tay sơn) không hợp nội dung. Mới: quạt tản nhiệt RGB cận cảnh, đúng 'quạt' | có |
| mim-tahoe-44-trieu-hinton | 0 | pexels:7643473 → pexels:7180075 | lặp 2 lần trong 40 spec; chỉ 6s. Mới: hai người trò chuyện trong văn phòng nhỏ, ý 'công ty ba người' | có |
| mim-tahoe-44-trieu-hinton | 9 | pexels:6266251 → pexels:6266434 | đã dùng ở data/stier/specs. Mới: chồng tiền mặt và máy tính bàn, tông xanh xám, ý '44 triệu đô' | có |
| mim-jeopardy-julann-tren-may-bay | 4 | pexels:7643473 → pexels:6977375 | lặp 2 lần trong 40 spec; chỉ 6s. Mới: tivi cũ nhiễu hạt, ý đài truyền hình NBC, không logo | có |
| mim-watson-ferrucci-sai-gan-het | 4 | pexels:35332817 → pexels:7703943 | đã dùng ở data/stier/specs; chỉ 7s. Mới: đồng hồ cát, ý 'ba đến năm năm' | có |
| mim-watson-lickel-nha-hang-im-lang | 8 | pexels:7688618 → pexels:7402582 | lặp 2 lần trong 40 spec. Mới: bàn ghế trống trong quán vắng, đúng 'nhà hàng im lặng' | có |
| mim-altman-khong-nhu-bac-si | 2 | pexels:8889195 → pexels:9902177 | lặp 4 lần trong 40 spec. Mới: bóng người bên rèm cửa, kín đáo, ý 'kể chuyện riêng tư' | có |
| mim-altman-khong-nhu-bac-si | 8 | pexels:8889195 → pexels:6287766 | lặp 4 lần trong 40 spec. Mới: cận cảnh bàn mổ, bác sĩ mờ, che mặt, ý 'đặc quyền bác sĩ' | có |
| mim-chat-nguoi-la-20-3-2023 | 6 | pexels:6381013 → pexels:35158244 | lặp 2 lần trong 40 spec. Mới: mạng nút phát sáng tím trên nền tối, ý dữ liệu/số liệu | có |
| mim-chat-nguoi-la-20-3-2023 | 8 | pexels:7279738 → pexels:11349390 | lặp 2 lần trong 40 spec. Mới: bóng người đi trong sương đêm, đúng 'người lạ', không mặt | có |
| mim-deepseek-kho-chat-khong-mat-khau | 0 | pexels:8561462 → pexels:39918565 | lặp 4 lần trong 40 spec. Mới: tủ thiết bị với đèn LED xanh trên nền tối, ý 'kho dữ liệu' | có |
| mim-deepseek-kho-chat-khong-mat-khau | 8 | pexels:8561462 → pexels:7830153 | lặp 4 lần trong 40 spec. Mới: cánh cửa gỗ sơn xanh, ý 'cửa đã mở sẵn' | có |
| mim-meta-ai-sua-xe-cong-khai | 0 | pexels:36149629 → pexels:8987289 | lặp 2 lần trong 40 spec. Mới: thợ sửa động cơ ô tô, chỉ thấy tay và thân, không logo | có |
| mim-meta-ai-sua-xe-cong-khai | 7 | pexels:8091712 → pexels:6279146 | lặp 3 lần trong 40 spec. Mới: điện thoại màn trắng, ngón tay chạm, ý 'màn cảnh báo' | có |
| mim-meta-ai-sua-xe-cong-khai | 9 | pexels:36149629 → pexels:6611949 | lặp 2 lần trong 40 spec. Mới: hai tay bấm điện thoại màn trắng, ý 'hai lần bấm' | có |
| mim-samsung-ba-vu-truoc-khi-cam | 8 | pexels:8561462 → pexels:26586645 | lặp 4 lần trong 40 spec. Mới: hàng ổ khoá trên rào, ý 'tạm cấm/khoá' | có |
| mim-y-chan-chatgpt-roi-toa-huy-phat | 0 | pexels:36637656 → pexels:36633822 | lặp 2 lần trong 40 spec. Mới: toàn cảnh Rome lúc hoàng hôn, đúng 'nước Ý' | có |
| mim-y-chan-chatgpt-roi-toa-huy-phat | 9 | pexels:8091712 → pexels:6100896 | lặp 3 lần trong 40 spec. Mới: cán cân công lý trên nền xám, đúng 'toà huỷ phạt' | có |
| mim-elias-bai-toan-to-bip | 0 | pexels:36862846 → pexels:8751438 | đã dùng ở data/stier/specs. Mới: tay cầm bài, nền tím mờ, ý 'năm bản sao' ngồi chơi bài | có |
| mim-elias-bai-toan-to-bip | 5 | pexels:6948566 → pexels:6600012 | đã dùng ở data/stier/specs. Mới: quân cờ bạc/gỗ, ý 'chiến lược hỗn hợp' | có |
| mim-elias-bai-toan-to-bip | 7 | pexels:12271136 → pexels:8327801 | đã dùng ở data/stier/specs. Mới: cánh tay robot chơi cờ trên nền đen, ý 'cỗ máy gặp người giỏi nhất' | có |
| mim-jason-les-ba-co-may | 0 | pexels:6813640 → pexels:36415776 | đã dùng ở data/stier/specs. Mới: bàn poker nỉ xanh, chip và bài, không mặt | có |
| mim-jason-les-ba-co-may | 4 | pexels:11142482 → pexels:8751465 | đã dùng ở data/stier/specs. Mới: bài tung trong ánh tím mờ, hợp 'Libratus' (poker) | có |
| mim-jason-les-ba-co-may | 8 | pexels:7478342 → pexels:6650584 | đã dùng ở data/stier/specs. Mới: hai bàn tay chạm nhau trong vầng sáng tối, ý 'phía loài người' | có |
| mim-polaris-2007-2008 | 0 | pexels:36641402 → pexels:7608702 | đã dùng ở data/stier/specs. Mới: bàn tay cầm bộ bài poker, không mặt | có |
| mim-polaris-2007-2008 | 5 | pexels:5192033 → pexels:35304178 | đã dùng ở data/stier/specs. Mới: đường phố đêm đèn đỏ/vàng, tông tối (chung chung, không khẳng định là Las Vegas) | có |
| mim-polaris-2007-2008 | 8 | pexels:6058468 → pexels:6153725 | đã dùng ở data/stier/specs. Mới: tay giả robot trên nền xanh dương, ý 'ranh giới người-máy đổi chỗ' | có |
| mim-sandholm-hai-cap-doi-than | 0 | pexels:7101003 → pexels:29241126 | đã dùng ở data/stier/specs. Mới: hành lang bệnh viện tối có giường đẩy, ý 'hai quả thận' | có |
| mim-sandholm-hai-cap-doi-than | 3 | pexels:34677869 → pexels:6219899 | đã dùng ở data/stier/specs. Mới: người viết công thức trên bảng đen, ý 'viết thuật toán' | có |
| mim-sandholm-hai-cap-doi-than | 5 | pexels:13335630 → pexels:7584601 | đã dùng ở data/stier/specs. Mới: ca mổ, mọi người đeo khẩu trang, đúng 'hai ca mổ' | có |
| mim-sandholm-hai-cap-doi-than | 8 | pexels:8164796 → pexels:34995473 | đã dùng ở data/stier/specs. Mới: mạng nút tím sáng, ý 'thuật toán nối hai người' | có |
| mim-deepface-2014-bon-trieu-khuon-mat | 0 | pexels:36511035 → pexels:34268299 | ảnh cũ trong hộp, lặp 2 spec. Mới: đám đông bóng đen dưới vòm, ý 'bốn triệu khuôn mặt', không rõ mặt | có |
| mim-face-id-san-khau-2017 | 8 | pexels:17518183 → pexels:6787449 | lặp 3 lần trong 40 spec. Mới: tay cầm điện thoại màn trắng trơn, gợi mở khoá máy | có |
| mim-viola-jones-2001-may-tim-mat | 6 | pexels:36392049 → pexels:19784108 | lặp 2 lần trong 40 spec. Mới: máy ảnh compact trong tay, nền bokeh, không chữ đọc được | có |
| mim-game-alpha-red-tran-thang-dau | 3 | pexels:34679079 → pexels:8128344 | lặp 2 lần trong 40 spec; chỉ 6s. Mới: ghế gamer trống xoay trong ánh xanh, đúng 'ngồi vào ghế', không mặt | có |
| mim-game-dendi-2017 | 8 | pexels:7579576 → pexels:8087317 | lặp 2 lần trong 40 spec. Mới: robot đồ chơi trắng, ý 'máy chưa biết đồng đội' | có |
| mim-game-google-mua-atari-2014 | 0 | pexels:4835514 → pexels:36246874 | rủi ro tên/logo (arcade). Mới: toà nhà kính xám nhìn lên, ý 'công ty/Google mua' | có |
| mim-game-google-mua-atari-2014 | 3 | pexels:29467292 → pexels:8888600 | rủi ro tên/logo (arcade). Mới: băng VHS và máy chơi game cổ, ý 'Atari thập niên 70-80', không thấy nhãn | có |
| mim-game-khan-gia-chon-tuong-hai-may | 0 | pexels:6651626 → pexels:19193241 | lặp 3 lần trong 40 spec. Mới: đám đông dưới ánh sân khấu tối, đúng 'khán giả' | có |
| mim-game-mana-thua-nam-van-roi-thang | 7 | pexels:8889195 → pexels:35281906 | lặp 4 lần trong 40 spec. Mới: tay gõ bàn phím RGB xanh lục, tông tối, ý game | có |
| mim-game-og-thua-may-roi-vo-dich | 4 | pexels:10374892 → pexels:33162963 | lặp 2 lần trong 40 spec. Mới: cầu Cổng Vàng trong sương = San Francisco, không chữ/mặt người | có |
| mim-game-tai-khoan-an-danh-grandmaster | 3 | pexels:5377697 → pexels:36178907 | lặp 2 lần trong 40 spec. Mới: tay gõ laptop thiếu sáng, tông tối | có |
| mim-game-tlo-thua-roi-viet-luat | 3 | pexels:17518183 → pexels:35163081 | lặp 3 lần trong 40 spec. Mới: mạng nơ-ron hồng trên nền đen, hợp 'cỗ máy mạnh' | có |

## Rủi ro còn lại

- Poster chỉ là khung đầu; chưa kiểm từng khung bằng clip_sheet (chưa tải/cắt video, đúng yêu cầu không dựng). Nên chạy motion/long/clip_sheet.py trước khi render để soi chữ/logo giữa clip.
- Chưa đổi loại cảnh nào (không phải đổi sang chữ/ảnh dữ liệu); tìm đủ 49 clip pexels.
- 5 clip giữ nguyên nhưng ngắn (≤7 giây): 34280528 (5s, cuda cảnh 0), 10588604, 39402054, 6101348, 27385370 (7s). Cảnh của chúng ngắn hơn clip (ước 2-5 giây) nên chưa lỗi; để nguyên, chưa soi poster.
- Một số clip mới chỉ gợi ý, không minh hoạ đúng nơi/người: 35304178 (phố đêm cho 'Las Vegas'), 36246874 (toà kính cho Google), 36633822 (Rome từ trên cao, đúng nước Ý), 7180075 và 6219899 có mặt người mẫu stock nhỏ, không phải người nổi tiếng.
- Một số id giữ lại cho lần dùng duy nhất chưa soi lại kỹ chữ: 5377697 (màn hình dữ liệu có chữ nhỏ), 17518183 (màn hình dựng phim), 8889195 và 8561462 (không chữ). Nếu clip_sheet thấy chữ đọc được thì đổi tiếp.
- motion/hf/assets/clips/index.json đã được clips.py search ghi thêm các id ứng viên (chỉ thêm, không sửa mục cũ).
