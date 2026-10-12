"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #9 "Flappy Bird".

    python data/long/mim-flappy-bird/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). KHÔNG dùng hình ảnh / nhân vật / âm thanh của trò chơi thật: cảnh "flap" (lab.js) là hình khối
do kênh tự vẽ để minh hoạ cơ chế. Clip: Pexels (ngang), gắn "VIDEO MINH HỌA". Người thật còn sống: chỉ dùng điều đã công bố. beat2 bật.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"flappy": "Phờ-láp-pi", "bird": "bớt", "birds": "bớt", "family": "pha-mi-li", "twitter": "Tuýt-tơ", "tweet": "tuýt", "forbes": "Pho-bớt",
       "apple": "Áp-pồ", "game": "ghêm"}
VM = "VIDEO MINH HỌA"
MOCK = "HÌNH MINH HOẠ DO KÊNH TỰ VẼ · KHÔNG PHẢI HÌNH CỦA TRÒ CHƠI"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI MƯƠI HAI GIỜ NỮA"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "day": "HÀ NỘI", "date": "08.02.2014"},
    {"type": "broll", "at": 1, "vid": "31155915", "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỘT DÒNG NGẮN", "at": [1, "một"], "acc": True}]},
    {"type": "quote", "at": 2, "text": "Tôi xin lỗi những người chơi Flappy Bird. 22 giờ nữa, tôi sẽ gỡ Flappy Bird xuống. Tôi không thể chịu thêm được nữa.",
     "by": "NGUYỄN HÀ ĐÔNG · TWITTER, 08.02.2014 · TRÍCH DỊCH", "qline": 2},
    {"type": "ledger", "at": 3, "title": "LÚC ẤY: ĐỨNG ĐẦU ỨNG DỤNG MIỄN PHÍ", "rows": [{"k": "MỸ", "v": "SỐ 1", "at": [3, "Mỹ,"]}, {"k": "ANH", "v": "SỐ 1", "at": [3, "Anh,"]},
                                                                                       {"k": "TRUNG QUỐC", "v": "SỐ 1", "at": [3, "Trung"]}]},
    {"type": "counter", "at": 4, "from": 0, "to": 50000, "suffix": " USD", "until": [4, "nghìn"], "label": "TIỀN QUẢNG CÁO MỖI NGÀY",
     "sub": {"text": "THEO LỜI TÁC GIẢ · THE VERGE, 02.2014 · ≈ HƠN 1 TỶ ĐỒNG (KÊNH TỰ QUY ĐỔI)", "at": 5}},
    {"type": "slam", "at": 6, "text": "TỰ TAY TẮT ĐI"},
    {"type": "ledger", "at": 7, "title": "KHÔNG AI BẮT BUỘC", "rows": [{"k": "KHÔNG", "v": "AI ÉP", "at": 7}, {"k": "KHÔNG", "v": "CÔNG TY NÀO MUA LẠI", "at": [7, "công"]},
                                                                     {"k": "KHÔNG", "v": "TOÀ ÁN NÀO YÊU CẦU", "at": [7, "toà"]}]},
    {"type": "question", "at": 8, "text": "Vì sao?", "showAt": 8},
    {"type": "counter", "at": 9, "from": 22, "to": 22, "suffix": " GIỜ", "until": [9, "hai"], "label": "ĐỒNG HỒ DỪNG Ở ĐÂY",
     "sub": {"text": "quay về lúc trò chơi mới là một ý nghĩ", "at": 10}},
    {"type": "kinetic", "at": 11, "items": [{"text": "GẦN CUỐI VIDEO", "at": 11, "sm": True}, {"text": "ĐỒNG HỒ CHẠY TIẾP", "at": [11, "đồng"], "acc": True},
                                           {"text": "và chuyện gì xảy ra khi nó về 0", "at": 12, "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "HAI, BA NGÀY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "HAI, BA NGÀY", "sub": "NGUYỄN HÀ ĐÔNG · VẠN PHÚC, HÀ NỘI", "vid": "40120664", "illus": VM + " · HÀ NỘI",
     "titleAt": [0, "Người"]},
    {"type": "timeline", "at": 2, "items": [{"year": "16 tuổi", "text": "tự viết game", "at": [1, "tự"]},
                                           {"year": "2012", "text": "vẽ *một chú chim* cho trò chơi khác", "at": 2},
                                           {"year": "—", "text": "trò ấy *bị bỏ dở*", "at": 3},
                                           {"year": "2013", "text": "làm *một trò mới*", "at": 4}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "Ý TƯỞNG", "at": 5, "sm": True}, {"text": "TÂNG QUẢ BÓNG BÀN", "at": [5, "Tâng"], "acc": True},
                                          {"text": "cố giữ cho nó đừng rơi", "at": [5, "cố"], "sm": True}]},
    {"type": "counter", "at": 6, "from": 0, "to": 3, "suffix": " NGÀY", "until": [6, "ba"], "label": "LÀM XONG TRONG KHOẢNG 2–3 NGÀY", "sub": {"text": "THEO LỜI TÁC GIẢ", "at": 6}},
    {"type": "ledger", "at": 7, "title": "MỘT CHI TIẾT THÚ VỊ", "rows": [{"k": "BẢN ĐẦU", "v": "DỄ HƠN NHIỀU → TÁC GIẢ THẤY CHÁN", "at": 8}],
     "total": {"k": "NÊN", "v": "CHỈNH CHO KHÓ LÊN", "at": 9}},
    {"type": "date", "at": 10, "day": "LÊN KHO ỨNG DỤNG", "date": "24.05.2013"},
    {"type": "flap", "at": 11, "crashAt": [12, "hết"], "label": {"k": "MỘT ĐỘNG TÁC: CHẠM", "v": MOCK, "at": [11, "Chạm"]}},
    {"type": "broll", "at": 13, "vid": "34268782", "veil": 0.5, "illus": VM,
     "kin": [{"text": "GẦN NHƯ KHÔNG CÓ GÌ XẢY RA", "at": 13}, {"text": "NHIỀU THÁNG KHÔNG AI BIẾT TỚI", "at": 14, "acc": True}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "TÁM THÁNG IM LẶNG, RỒI BÙNG NỔ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "8 THÁNG SAU NGÀY RA MẮT", "date": "01.2014"},
    {"type": "ledger", "at": 1, "title": "ĐẦU BẢNG ỨNG DỤNG MIỄN PHÍ", "rows": [{"k": "MỸ", "v": "SỐ 1", "at": [1, "Mỹ"]}, {"k": "TRUNG QUỐC", "v": "SỐ 1", "at": [1, "Trung"]},
                                                                             {"k": "ANH", "v": "SỐ 1", "at": [1, "Anh."]}],
     "total": {"k": "HẾT THÁNG 1", "v": "ĐƯỢC TẢI NHIỀU NHẤT TRÊN KHO CỦA APPLE", "at": 2}},
    {"type": "question", "at": 3, "text": "Vì sao lại là lúc ấy?"},
    {"type": "broll", "at": 4, "vid": "7048551", "veil": 0.5, "illus": VM,
     "kin": [{"text": "KHÔNG AI CHẮC", "at": 4, "acc": True}, {"text": "xem người khác chơi · hét lên vì thua · rồi tự tải về", "at": [5, "Người"], "sm": True}]},
    {"type": "ledger", "at": 6, "title": "BA CÁCH GIẢI THÍCH", "rows": [{"k": "NGƯỜI NGOÀI", "v": "NHỜ VIDEO CHƠI GAME", "at": [6, None, 0, 0.05]},
                                                                      {"k": "NGƯỜI NGHI NGỜ", "v": "CÓ GIAN LẬN?", "at": [6, "nghi"]}],
     "total": {"k": "TÁC GIẢ", "v": "“CÓ LẼ LÀ MAY MẮN”", "at": [7, "có"]}},
    {"type": "bars", "at": 8, "title": "ĐẦU THÁNG 2/2014", "unit": "",
     "items": [{"k": "TIỀN QUẢNG CÁO MỖI NGÀY (NGHÌN USD)", "v": 50, "lbl": "~50", "at": [9, "năm"], "acc": True},
               {"k": "LƯỢT TẢI (TRIỆU)", "v": 50, "lbl": "> 50", "at": [10, "hơn"]}],
     "label": {"k": "NGUỒN", "v": "THE VERGE; ABC NEWS, 02.2014", "at": 8}},
    {"type": "ledger", "at": 11, "title": "NGHE NHƯ MỘT GIẤC MƠ", "rows": [{"k": "1 NGƯỜI", "v": "VÀI NGÀY LÀM VIỆC", "at": 11}, {"k": "KHÔNG", "v": "QUẢNG CÁO · NHÀ PHÁT HÀNH", "at": [11, "không"]}]},
    {"type": "broll", "at": 13, "vid": "6944070", "veil": 0.55, "illus": VM,
     "kin": [{"text": "THỨ LÀM NÊN CƠN SỐT", "at": 13, "sm": True}, {"text": "CŨNG LÀM ANH MẤT NGỦ", "at": [13, "cũng"], "acc": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "VÌ SAO KHÓ BỎ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "VÌ SAO\nKHÓ BỎ", "sub": "DIỄN GIẢI CỦA KÊNH · KHÔNG PHẢI LỜI TÁC GIẢ", "vid": "3913496", "illus": VM,
     "titleAt": [0, "Hãy"]},
    {"type": "ledger", "at": 2, "title": "BA BÁNH RĂNG", "srcnote": "DIỄN GIẢI CỦA KÊNH",
     "rows": [{"k": "1", "v": "HỌC TRONG MỘT GIÂY · MỘT NÚT BẤM", "at": 2}, {"k": "2", "v": "RẤT KHÓ · VÀI GIÂY LÀ THUA", "at": 3},
              {"k": "3", "v": "CHƠI LẠI NGAY · KHÔNG CHỜ", "at": 4}]},
    {"type": "flap", "at": 5, "crashAt": [6, "suýt"], "speed": 300, "label": {"k": "“SUÝT LÀM ĐƯỢC”", "v": MOCK, "at": [6, "suýt"]}},
    {"type": "kinetic", "at": 7, "items": [{"text": "LẦN THỬ TIẾP THEO", "at": 7, "sm": True}, {"text": "CÁCH ĐÚNG MỘT CÚ CHẠM", "at": [7, "cách"], "acc": True}]},
    {"type": "counter", "at": 8, "from": 0, "to": 12, "until": [9, "khoe,"], "label": "ĐIỂM SỐ: NHỎ · DỄ KHOE · DỄ GÂY NGỨA TAY", "sub": {"text": "CON SỐ MINH HOẠ", "at": 8}},
    {"type": "bars", "at": 10, "title": "GIỚI PHÊ BÌNH CHẤM", "unit": "",
     "items": [{"k": "ĐIỂM TRUNG BÌNH CÁC BÀI ĐÁNH GIÁ", "v": 52, "lbl": "52 / 100", "at": [11, "năm"], "acc": True}, {"k": "THANG ĐIỂM", "v": 100, "lbl": "100", "at": 10}],
     "label": {"k": "NGUỒN", "v": "METACRITIC · 7 BÀI", "at": 10}},
    {"type": "slam", "at": 12, "text": "CHƠI LẠI", "sub": "NGƯỜI CHƠI KHÔNG CHẤM ĐIỂM"},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "CÁI GIÁ CỦA VỊ TRÍ SỐ MỘT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "broll", "vid": "31801550", "veil": 0.5, "illus": VM,
     "kin": [{"text": "RẤT NHIỀU NGƯỜI NHÌN VÀO", "at": [0, "rất"], "acc": True}, {"text": "không phải ai cũng có thiện cảm", "at": 1, "sm": True}]},
    {"type": "ledger", "at": [1, "thiện"], "title": "NHỮNG LỜI CHÊ", "srcnote": "THEO BÁO CHÍ ĐẦU 2014",
     "rows": [{"k": "1", "v": "“HÌNH ĐI MƯỢN” → SAU ĐÓ ĐÍNH CHÍNH", "at": 2}, {"k": "2", "v": "“GIỐNG MỘT GAME NĂM 2011”", "at": 4},
              {"k": "3", "v": "TIN ĐỒN BỊ KIỆN → HÃNG ẤY PHỦ NHẬN", "at": 5}]},
    {"type": "slam", "at": 6, "text": "NẶNG NỀ HƠN", "sub": "CÓ CẢ LỜI DOẠ GIẾT TRÊN MẠNG · THE INDEPENDENT, 10.02.2014", "subAt": 7},
    {"type": "broll", "at": 8, "vid": "6944070", "ms": 14, "veil": 0.55, "illus": VM,
     "kin": [{"text": "ANH KỂ: MẤT NGỦ", "at": 8, "acc": True}, {"text": "làm để chơi vài phút · có người chơi hàng giờ", "at": 9, "sm": True}]},
    {"type": "counter", "at": 10, "from": 22, "to": 22, "suffix": " GIỜ", "until": [10, "chạy"], "label": "ĐỒNG HỒ BẮT ĐẦU CHẠY LẠI"},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "ĐỒNG HỒ VỀ KHÔNG"}, "bgm": {"mood": "mystery", "gain": 0.12}, "scenes": [
    {"type": "date", "day": "DÒNG TWEET ĐƯỢC ĐĂNG", "date": "08.02.2014"},
    {"type": "counter", "at": 1, "from": 22, "to": 21, "suffix": " GIỜ", "until": [2, "đoán"], "label": "CÒN LẠI"},
    {"type": "ledger", "at": 3, "title": "CẢ THẾ GIỚI CÔNG NGHỆ ĐOÁN", "rows": [{"k": "?", "v": "BỊ KIỆN", "at": 3}, {"k": "?", "v": "MỘT CHIÊU QUẢNG CÁO", "at": [3, "Hay"]}],
     "total": {"k": "TÁC GIẢ", "v": "“KHÔNG LIÊN QUAN GÌ TỚI PHÁP LÝ”", "at": [4, "Chuyện"]}},
    {"type": "counter", "at": 5, "from": 21, "to": 0, "suffix": " GIỜ", "until": [5, "qua."], "label": "ĐỒNG HỒ VỀ KHÔNG"},
    {"type": "date", "at": 6, "day": "BIẾN MẤT KHỎI CẢ HAI KHO ỨNG DỤNG", "date": "10.02.2014"},
    {"type": "quote", "at": 7, "text": "Flappy Bird được thiết kế để chơi trong vài phút, lúc bạn thư giãn. Nhưng nó đã thành một sản phẩm gây nghiện. Tôi nghĩ nó đã thành một vấn đề.",
     "by": "NGUYỄN HÀ ĐÔNG · FORBES, 11.02.2014 · TRÍCH DỊCH", "qline": 8},
    {"type": "ledger", "at": 9, "title": "ANH NÓI THÊM", "srcnote": "FORBES, 02.2014 · DIỄN Ý",
     "rows": [{"k": "TRÒ CHƠI", "v": "ĐÃ RA ĐI MÃI MÃI", "at": 9}, {"k": "LƯƠNG TÂM", "v": "NHẸ HƠN · NGỦ LẠI ĐƯỢC", "at": 10}]},
    {"type": "slam", "at": 11, "text": "50.000 USD / NGÀY", "sub": "ĐỔI LẤY MỘT GIẤC NGỦ", "subAt": 12},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "SAU KHI CON CHIM BIẾN MẤT"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "SAU KHI\nCON CHIM BIẾN MẤT", "sub": "NHỮNG GÌ CÒN LẠI", "vid": "10527947", "illus": VM, "titleAt": [0, "Trò"]},
    {"type": "bars", "at": 1, "title": "RAO BÁN ĐIỆN THOẠI CÒN SẴN TRÒ CHƠI (USD)", "unit": "",
     "items": [{"k": "TIN RAO TỪ", "v": 1499, "lbl": "1.499", "at": [2, "một"]}, {"k": "CÓ LƯỢT TRẢ GIÁ VƯỢT", "v": 90000, "lbl": "> 90.000", "at": [2, "chín"], "acc": True}],
     "label": {"k": "", "v": "TRANG ĐẤU GIÁ SAU ĐÓ GỠ CÁC TIN NÀY", "at": [2, "trước"]}},
    {"type": "counter", "at": 3, "from": 0, "to": 60, "prefix": ">", "suffix": " / NGÀY", "until": [4, "sáu"], "label": "TRÒ CHƠI NHÁI XUẤT HIỆN LÚC CAO ĐIỂM",
     "sub": {"text": "kho ứng dụng từ chối game có chữ “Flappy” trong tên", "at": 5}},
    {"type": "timeline", "at": 6, "items": [{"year": "08.2014", "text": "bản *Family* · chỉ cho một loại đầu thu tivi", "at": 6},
                                           {"year": "—", "text": "bản gốc trên điện thoại *không quay lại*", "at": 7},
                                           {"year": "2024", "text": "nhãn hiệu về tay *công ty khác*", "at": 9}]},
    {"type": "ledger", "at": 10, "title": "TÁC GIẢ LÊN TIẾNG · 09.2024", "srcnote": "NGUỒN: TECHCRUNCH, 15.09.2024",
     "rows": [{"k": "BẢN MỚI", "v": "KHÔNG LIÊN QUAN GÌ TỚI ANH", "at": [11, "không"]}, {"k": "ANH", "v": "KHÔNG BÁN THỨ GÌ CẢ", "at": [11, "bán"]}]},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "MỘT QUYẾT ĐỊNH NGƯỢC CHIỀU"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "bars", "title": "PHÉP ĐO QUEN THUỘC CỦA NGÀNH", "unit": "",
     "items": [{"k": "NGƯỜI DÙNG Ở LẠI ÍT", "v": 20, "lbl": "“KÉM”", "at": 0}, {"k": "NGƯỜI DÙNG Ở LẠI LÂU", "v": 90, "lbl": "“THÀNH CÔNG”", "at": 1, "acc": True}],
     "label": {"k": "", "v": "SƠ ĐỒ MINH HOẠ", "at": 0}},
    {"type": "kinetic", "at": 2, "items": [{"text": "CÓ NGƯỜI NHÌN CON SỐ ẤY", "at": [2, "có"]}, {"text": "VÀ THẤY LO", "at": [2, "thấy"], "acc": True},
                                          {"text": "không phải vì thấp · mà vì quá cao", "at": 3, "sm": True}]},
    {"type": "ledger", "at": 4, "title": "HAI CÁCH NHÌN", "rows": [{"k": "1", "v": "ANH ĐÃ QUÁ NHẠY CẢM", "at": 4}, {"k": "2", "v": "ANH THẤY SỚM MỘT ĐIỀU", "at": 5}],
     "total": {"k": "ĐIỀU ẤY", "v": "GIỮ CHÂN ≠ TỐT CHO TA", "at": 6}},
    {"type": "counter", "at": 7, "from": 22, "to": 22, "suffix": " GIỜ", "until": [7, "giờ."], "label": "MỘT NGƯỜI · MỘT DÒNG TWEET",
     "sub": {"text": "một quyết định đi ngược mọi lời khuyên kinh doanh", "at": 8}},
    {"type": "question", "at": 9, "text": "50.000 đô mỗi ngày.\nBạn có gỡ nó xuống không?", "showAt": 10},
    {"type": "kinetic", "at": 11, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 11}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [11, "ở"], "acc": True}]},
]}

SPEC = {
    "title": "Flappy Bird: Kiếm 50.000 Đô Mỗi Ngày, Vì Sao Nguyễn Hà Đông Tự Tay Gỡ Game?",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["flappy", "bird", "gỡ", "giờ", "đô", "ngủ", "nghiện"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(8)],
    "youtube": {
        "titles": ["Flappy Bird: Kiếm 50.000 Đô Mỗi Ngày, Vì Sao Nguyễn Hà Đông Tự Tay Gỡ Game?",
                   "22 Giờ Cuối Của Flappy Bird: Trò Chơi Việt Làm Cả Thế Giới Phát Cuồng",
                   "Làm Trong Vài Ngày, Đứng Đầu Thế Giới, Rồi Biến Mất: Chuyện Thật Của Flappy Bird"],
        "summary": "Tháng 2/2014, một lập trình viên ở Hà Nội tự tay gỡ trò chơi đang đứng đầu thế giới và mang về khoảng 50.000 đô mỗi ngày. Video "
                   "kể lại theo một chiếc đồng hồ đếm ngược 22 giờ: trò chơi ra đời trong vài ngày thế nào, tám tháng không ai biết tới rồi bùng nổ "
                   "ra sao, vì sao nó khó bỏ, cái giá của vị trí số một, và lời giải thích của chính tác giả.",
        "more": ["Video chỉ dùng những điều Nguyễn Hà Đông đã nói công khai (Twitter, The Verge, Forbes, CNBC) và điều báo chí đã đăng; không suy đoán "
                 "về thu nhập hay đời tư. Phần \"vì sao khó bỏ\" và phần kết là diễn giải của kênh. Hình minh hoạ cơ chế trò chơi do kênh tự vẽ bằng "
                 "hình khối, không dùng hình ảnh, nhân vật hay âm thanh của trò chơi. Con số lượt tải khác nhau giữa các nguồn (ABC News: hơn 50 "
                 "triệu). \"Hơn 1 tỷ đồng mỗi ngày\" là kênh tự quy đổi theo tỷ giá đầu năm 2014. Lời trích được dịch và đọc bằng giọng máy."],
        "chapter_titles": {"ch00": "Mở đầu: \"22 giờ nữa, tôi sẽ gỡ Flappy Bird\"", "ch01": "Hai, ba ngày: trò chơi ra đời",
                           "ch02": "Tám tháng im lặng, rồi bùng nổ", "ch03": "Vì sao khó bỏ (diễn giải của kênh)",
                           "ch04": "Cái giá của vị trí số một", "ch05": "Đồng hồ về không: 10/02/2014",
                           "ch06": "Sau khi con chim biến mất", "ch07": "Một quyết định ngược chiều"},
        "sources": [
            "https://en.wikipedia.org/wiki/Flappy_Bird",
            "https://abcnews.com/Technology/flappy-bird-creator-pulled-game-addictive-product/story?id=22461633",
            "https://www.cnbc.com/2014/05/14/flappy-bird-is-coming-back-to-app-store.html",
            "https://techcrunch.com/2024/09/15/flappy-birds-creator-disavows-official-new-version-of-the-game/",
            "https://now.temple.edu/news/2024-09-20/flappy-bird-return-after-10-year-hiatus-true-story-behind-worlds-most-viral-mobile-game",
        ],
        "hashtags": ["FlappyBird", "NguyễnHàĐông", "CôngNghệ", "GameViệt", "MindInTheMachine"],
        "tags": ["Flappy Bird", "Nguyễn Hà Đông", "vì sao Flappy Bird bị gỡ", "game Việt", "lịch sử Flappy Bird", "game gây nghiện", "công nghệ",
                 "câu chuyện công nghệ", "dotGears", "ứng dụng số 1 thế giới"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")


if __name__ == "__main__":
    main()
