"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #1 "AI đã chết hai lần".

    python data/long/mim-ai-70/gen_scenes.py          # giữ nguyên "lines" (do motion/long/script_lines.py ghi)

Ảnh: chỉ PD / CC0 / CC BY (kênh MIM không nhận BY-SA — build_long kiểm lại lúc tải). Dữ kiện + nguồn:
docs/channels/mind-in-the-machine/2026-10-06-long-01-research.md. Clip: Pexels (ngang), tải bằng
`python motion/long/pexels.py get mim-ai-70 <id> ...`.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

IMGS = {
    "perceptron": "File:330-PSA-80-60 (USN 710739) (20897323365).jpg",                       # PD · Hải quân Mỹ
    "ibm704": "File:IBM Electronic Data Processing Machine - GPN-2000-001881.jpg",            # PD · NASA 1957
    "percdiagram": "File:Organization of a biological brain and a perceptron.png",            # PD · Rosenblatt 1958
    "turing": "File:Alan Turing (1951).jpg",                                                  # PD
    "turing16": "File:Alan Turing Aged 16.jpg",                                               # PD
    "dartmouth": "File:Baker Memorial Library, Dartmouth College - DSC09058.JPG",              # CC0 · ảnh 2013
    "mccarthy": "File:John McCarthy (computer scientist) Stanford 2006 (272020300).jpg",      # CC BY 2.0
    "minsky": "File:Marvin Minsky (1).jpg",                                                   # CC BY 2.0
    "shannon": "File:C.E. Shannon. Tekniska museet 43069.jpg",                                # CC BY 2.0
    "shannonmachine": "File:Red-Black by Claude Shannon, game-playing machine, c. 1951 - MIT Museum - Cambridge, MA - DSC09108.jpg",  # CC0
    "weizenbaum": "File:Weizenbaum 1982.jpg",                                                 # PD
    "lisp": "File:CADR - The Lisp Machine, late 1970s, view 1 - MIT Museum - DSC03747.JPG",   # CC0
    "deepblue": "File:IBM Deep Blue at Computer History Museum (9361685537).jpg",             # CC BY 2.0
    "dbchip": "File:One of Deep Blue's processors (2586060990).jpg",                          # CC BY 2.0
    "gtx580": "File:NVIDIA@40nm@Fermi@GF110@GeForce GTX 580@UA10B338 1041A1 N2Y540.000 GF110-375-A1 DSC04152 (27576804994).jpg",  # CC0
    "leesedol": "File:Lee Se-Dol.jpg",                                                        # CC BY 2.0
    "hinton": "File:Geoffrey Hinton - Collision 2023 - Centre Stage RCZ 1307 (cropped).jpg",  # CC BY 2.0
}

SAY = {   # chữ hiển thị -> cách đọc (phụ đề giữ chữ gốc); "=X" = khớp đúng hoa/thường
    "=AI": "ây ai", "dartmouth": "Đát-mâu", "mccarthy": "Mơ-ca-thi", "marvin": "Mác-vin", "minsky": "Min-xki",
    "nathaniel": "Na-tha-ni-en", "rochester": "Rô-chét-xtơ", "claude": "Clốt", "shannon": "Sen-nần", "alan": "A-lần",
    "turing": "Tiu-rinh", "frank": "Phrăng", "rosenblatt": "Râu-dần-blát", "perceptron": "pơ-xép-trôn",
    "perceptrons": "pơ-xép-trôn", "ibm": "ai bi em", "=704": "bảy không bốn", "new": "Niu", "yorker": "Doóc-cơ",
    "york": "Doóc", "eliza": "Ê-lai-dơ", "joseph": "Giô-dép", "weizenbaum": "Vai-dần-bom", "mit": "em ai ti",
    "herbert": "Hơ-bớt", "simon": "Sai-mần", "allen": "A-lần", "newell": "Niu-ồn", "seymour": "Xi-mo", "papert": "Pa-pớt",
    "james": "Giêm", "lighthill": "Lai-hiu", "garry": "Ga-ri", "kasparov": "Ca-xpa-rốp", "deep": "Đíp", "blue": "Blu",
    "philadelphia": "Phi-la-đen-phi-a", "david": "Đây-vít", "rumelhart": "Ru-mơn-hát", "geoffrey": "Giép-phri",
    "hinton": "Hin-tần", "ronald": "Rô-nan", "williams": "Uy-li-am", "nature": "Nây-chơ", "gpu": "gi pi iu",
    "imagenet": "I-mịt-nét", "toronto": "To-ron-tô", "alexnet": "A-léc-nét", "gtx": "gi ti ích", "=580": "năm tám mươi",
    "alphago": "An-pha Gô", "deepmind": "Đíp-mai", "lee": "Li", "sedol": "Xê-đôn", "seoul": "Xơ-un", "google": "Gu-gồ",
    "attention": "ơ-ten-sần", "is": "ít", "all": "o", "you": "diu", "need": "nít", "transformer": "tran-xphó-mơ",
    "openai": "Ô-pần ây ai", "chatgpt": "chát gi pi ti", "gpt-4.5": "gi pi ti bốn chấm năm", "california": "Ca-li-pho-ni-a",
    "san": "Xan", "diego": "Đi-ê-gô", "hal": "Han", "=9000": "chín nghìn", "space": "xpây", "odyssey": "Ô-đi-xi",
    "skynet": "Xcai-nét", "doraemon": "Đô-rê-mon", "hopfield": "Hóp-phin", "demis": "Đê-mít", "hassabis": "Ha-xa-bít",
    "john": "Giôn", "jumper": "Giăm-pơ", "alphafold": "An-pha Phôn", "nobel": "Nô-ben", "hampshire": "Hem-sơ",
    "cornell": "Coóc-nen", "harvard": "Ha-vớt", "bell": "Ben",
}

CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "CỖ MÁY HỌC ĐƯỢC TRÁI VÀ PHẢI"}, "bgm": {"mood": "mystery", "gain": 0.12}, "scenes": [
    {"type": "date", "bg": "perceptron", "day": "VĂN PHÒNG NGHIÊN CỨU HẢI QUÂN MỸ", "date": "07.1958",
     "illus": "ẢNH: MARK I PERCEPTRON · BẢN PHẦN CỨNG RA ĐỜI SAU"},
    {"type": "print", "at": 1, "img": "ibm704", "tone": "bw", "illus": "ẢNH MINH HỌA · MÁY CÙNG LOẠI (NASA, 1957)",
     "side": {"k": "IBM 704", "h": "≈ 5 TẤN\nTO BẰNG CĂN PHÒNG", "lines": [{"text": "Nuôi bằng *thẻ đục lỗ*", "at": [1, "phòng."]}]}},
    {"type": "punch", "at": 2, "trials": 50, "startAt": [2, "thẻ"], "until": [5, "phân"],
     "label": {"k": "THÍ NGHIỆM 1958", "v": "KHÔNG AI DẠY LUẬT", "at": [4, "luật"]}},
    {"type": "print", "at": 6, "img": "percdiagram", "tone": "color",
     "side": {"k": "FRANK ROSENBLATT", "h": "Nhà tâm lý học\nCornell", "hAt": [6, "Rosenblatt,"],
              "lines": [{"text": "Hình vẽ của ông · *1958*", "at": [6, "Cornell."]}]}},
    {"type": "kinetic", "at": 7, "items": [{"text": "PERCEPTRON", "at": [7, "perceptron,"], "acc": True},
                                          {"text": "một ý tưởng độc đáo?", "at": [7, "độc"], "sm": True}]},
    {"type": "quote", "at": 8, "text": "the first serious rival to the human brain ever devised", "by": "THE NEW YORKER · 1958 · QUA CORNELL CHRONICLE",
     "lbl": "TRÍCH DỊCH", "qline": 9, "typeAt": [9, "Đối"]},
    {"type": "slam", "at": 10, "text": "NGÕ CỤT", "sub": "CHỈ MƯỜI MỘT NĂM SAU"},
    {"type": "photo", "at": 11, "img": "perceptron", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "NÓ ĐÃ QUAY LẠI", "at": [12, "quay"], "acc": True}],
     "label": {"k": "MARK I PERCEPTRON", "v": "ẢNH HẢI QUÂN MỸ", "at": [11, "người"]}},
    {"type": "broll", "at": 13, "vid": "6963823", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "TRONG ĐIỆN THOẠI CỦA BẠN", "at": [13, "điện"], "acc": True}]},
    {"type": "brand", "at": 14, "sub": "70 NĂM TRÍ TUỆ NHÂN TẠO"},
    {"type": "kinetic", "at": 15, "items": [{"text": "MỘT MÙA HÈ", "at": [15, "mùa"], "acc": True},
                                           {"text": "là đủ để tạo bước tiến lớn?", "at": [15, "đủ"], "sm": True}]},
    {"type": "ledger", "at": 16, "title": "BA CÂU HỎI", "rows": [
        {"k": "01", "v": "AI ĐẶT TÊN — NGHĨ MẤT BAO LÂU?", "at": [17, "đặt"]},
        {"k": "02", "v": "VÌ SAO AI CHẾT HAI LẦN?", "at": [18, "chết,"]},
        {"k": "03", "v": "THỨ GÌ ĐÃ HỒI SINH NÓ?", "at": [19, "hồi"]}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MỘT MÙA HÈ ĐỂ GIẢI BÀI TOÁN TRÍ TUỆ"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MỘT MÙA HÈ\nĐỂ GIẢI BÀI TOÁN", "sub": "1950 — 1956", "bg": "turing", "titleAt": [0, "Năm"]},
    {"type": "quote", "at": 1, "text": "Can machines think?", "by": "ALAN TURING · MIND, 1950", "lbl": "TRÍCH DỊCH", "qline": 1, "typeAt": [1, "Máy"]},
    {"type": "print", "at": 2, "img": "turing", "tone": "bw", "side": {"k": "ALAN TURING · 1950", "h": "Trò chơi\nbắt chước", "lines": [
        {"text": "Trò chuyện qua *bàn phím*", "at": [3, "bàn"]}, {"text": "Đâu là máy, đâu là *người*?", "at": [3, "người,"]}]}},
    {"type": "kinetic", "at": 4, "items": [{"text": "≈ 50 NĂM NỮA", "at": [4, "năm"], "acc": True},
                                          {"text": "SAU 5 PHÚT TRÒ CHUYỆN", "at": [4, "phút"]},
                                          {"text": "người hỏi đoán sai ≥ 3 lần trong 10", "at": [4, "sai"], "sm": True}]},
    {"type": "date", "at": 6, "day": "ĐƠN XIN TÀI TRỢ", "date": "31.08.1955", "sub": {"text": "BỐN CHỮ KÝ", "at": [6, "bốn"]}},
    {"type": "print", "at": 7, "img": "mccarthy", "tone": "color", "side": {"k": "JOHN McCARTHY", "h": "Giảng viên toán\nDartmouth"}},
    {"type": "print", "at": 8, "img": "minsky", "tone": "color", "side": {"k": "MARVIN MINSKY", "h": "Harvard"}},
    {"type": "kinetic", "at": 9, "items": [{"text": "NATHANIEL ROCHESTER", "at": [9, "Rochester,"]},
                                          {"text": "KỸ SƯ IBM", "at": [9, "IBM."], "sm": True}]},
    {"type": "print", "at": 10, "img": "shannon", "tone": "bw", "side": {"k": "CLAUDE SHANNON", "h": "Cha đẻ lý thuyết\nthông tin", "lines": [
        {"text": "Phòng thí nghiệm *Bell*", "at": [10, "Bell."]}]}},
    {"type": "slam", "at": 11, "text": "TRÍ TUỆ\nNHÂN TẠO", "sub": "LẦN ĐẦU XUẤT HIỆN · ĐƠN 1955"},
    {"type": "ledger", "at": 12, "title": "HỌ XIN GÌ?", "rows": [
        {"k": "NGƯỜI", "v": "10", "at": [13, "Mười"]}, {"k": "THỜI GIAN", "v": "2 THÁNG", "at": [13, "Hai"]}],
     "total": {"k": "KINH PHÍ", "v": "$13.500", "at": [13, "ba"]}},
    {"type": "quote", "at": 14, "text": "…can in principle be so precisely described that a machine can be made to simulate it.",
     "by": "ĐỀ XUẤT DARTMOUTH · 31.08.1955", "lbl": "TRÍCH", "typeAt": [14, "mọi"]},
    {"type": "kinetic", "at": 15, "items": [{"text": "MỘT NHÓM CHỌN KỸ", "at": [15, "nhóm"]},
                                           {"text": "VÀI BÀI TOÁN · BƯỚC TIẾN LỚN", "at": [15, "bước"], "acc": True}]},
    {"type": "slam", "at": 16, "text": "MỘT MÙA HÈ."},
    {"type": "photo", "at": 17, "img": "dartmouth", "tone": "color", "move": "in", "veil": 0.55,
     "kin": [{"text": "HÈ 1956", "at": [17, "1956,"], "acc": True}, {"text": "NGÔN NGỮ · NƠ-RON · SÁNG TẠO", "at": [18, "ngôn"]}],
     "label": {"k": "DARTMOUTH · HANOVER", "v": "ẢNH MINH HỌA · CHỤP NĂM 2013", "at": [17, "Dartmouth,"]}},
    {"type": "photo", "at": 19, "img": "shannonmachine", "tone": "color", "move": "in", "veil": 0.6,
     "kin": [{"text": "MỘT CHI TIẾT ÍT NGƯỜI ĐỂ Ý", "at": [19, "chi"]}, {"text": "SHANNON · 1951", "at": [20, "1951"], "acc": True}],
     "label": {"k": "MÁY CHƠI GAME CỦA SHANNON", "v": "MIT MUSEUM · KHOẢNG 1951", "at": [20, "trò"]}},
    {"type": "guess", "at": 21, "text": "THE ROOM WAS NOT VERY LIGHT", "startAt": [21, "đoán"], "until": [23, "đoán"],
     "statAt": [24, "Sáu"], "right": 89, "total": 129, "label": {"k": "TRÒ ĐOÁN CHỮ · SHANNON 1951", "at": [21, "đoạn"]}},
    {"type": "kinetic", "at": 25, "items": [{"text": "70 NĂM SAU", "at": [25, "Bảy"], "acc": True},
                                           {"text": "trò chơi ấy có một cái tên bạn rất quen", "at": [25, "tên"], "sm": True}]},
    {"type": "kinetic", "at": 26, "items": [{"text": "NHƯNG TRƯỚC ĐÓ", "at": [26, "trước"]},
                                           {"text": "PHẢI CHỌN MỘT CON ĐƯỜNG", "at": [26, "con"], "acc": True}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "HAI CON ĐƯỜNG"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "HAI CON ĐƯỜNG", "sub": "1957 — 1968", "bg": "percdiagram", "titleAt": [0, "Ngay"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "NGẢ 1 · VIẾT LUẬT", "at": [1, "viết"]},
                                          {"text": "nếu… thì…, từng bước một", "at": [2, "quy"], "sm": True}]},
    {"type": "nn", "at": 3, "fwdAt": [4, "mô"], "backAt": [4, "sai."], "label": {"k": "NGẢ 2 · TỰ HỌC", "v": "PERCEPTRON", "at": [3, "tự"]}},
    {"type": "broll", "at": 5, "vid": "6599643", "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "1958 · SIMON & NEWELL", "at": [6, "1958,"]}, {"text": "10 NĂM: MÁY VÔ ĐỊCH CỜ VUA", "at": [6, "vô"], "acc": True}]},
    {"type": "slam", "at": 7, "text": "10 NĂM", "sub": "HÃY NHỚ CON SỐ NÀY"},
    {"type": "print", "at": 8, "img": "weizenbaum", "tone": "bw", "side": {"k": "JOSEPH WEIZENBAUM", "h": "ELIZA\nMIT · 1966", "lines": [
        {"text": "Đóng vai *nhà trị liệu*", "at": [9, "trị"]}]}},
    {"type": "chat", "at": 10, "head": "MIT · 1966 · ELIZA (TRÍCH)", "msgs": [
        {"who": "u", "text": "Men are all alike.", "at": [11, "Đàn"]},
        {"who": "m", "text": "IN WHAT WAY", "at": [12, "Theo"]},
        {"who": "u", "text": "…", "at": [12, "nào?"]},
        {"who": "u", "text": "Well, my boyfriend made me come here.", "at": [13, "Bạn"]},
        {"who": "m", "text": "YOUR BOYFRIEND MADE YOU COME HERE", "at": [14, "Bạn"]}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "KHÔNG CÓ HIỂU BIẾT", "at": [15, "hiểu"], "acc": True},
                                           {"text": "BẮT TỪ KHOÁ", "at": [16, "từ"]}, {"text": "ĐẢO “TÔI” → “BẠN”", "at": [16, "đảo"]},
                                           {"text": "GHÉP CÂU MẪU", "at": [16, "ghép"]}]},
    {"type": "quote", "at": 17, "text": "very hard to convince that ELIZA … is not human", "by": "JOSEPH WEIZENBAUM · CACM, 1966",
     "lbl": "TRÍCH"},
    {"type": "slam", "at": 18, "text": "ẢO GIÁC\nCỦA SỰ THẤU HIỂU", "sub": "“THE ILLUSION OF UNDERSTANDING”"},
    {"type": "kinetic", "at": 19, "items": [{"text": "NHỚ CÁI TÊN: ELIZA", "at": [19, "ELIZA."], "acc": True},
                                           {"text": "gần 60 năm sau, nó sẽ đọ sức lần nữa", "at": [19, "đọ"], "sm": True}]},
    {"type": "broll", "at": 20, "vid": "17342967", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "LỜI HỨA ĐI QUÁ XA", "at": [20, "hứa"]}, {"text": "MÙA HÈ SẮP KẾT THÚC", "at": [21, "mùa"], "acc": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "MÙA ĐÔNG THỨ NHẤT"}, "bgm": {"mood": "calm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "MÙA ĐÔNG\nTHỨ NHẤT", "sub": "1969 — 1980", "vid": "30123241", "titleAt": [0, "Năm"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "PERCEPTRONS", "at": [1, "Perceptrons."], "acc": True},
                                          {"text": "giới hạn của perceptron đơn giản", "at": [2, "giới"], "sm": True},
                                          {"text": "BẢN ÁN CHO CẢ CON ĐƯỜNG?", "at": [3, "bản"]}]},
    {"type": "slam", "at": 4, "text": "TIỀN CẠN", "white": True},
    {"type": "photo", "at": 5, "img": "perceptron", "tone": "bw", "move": "out", "veil": 0.62,
     "kin": [{"text": "1971", "at": [5, "1971,"]}, {"text": "SINH NHẬT THỨ 43", "at": [5, "bốn"], "acc": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "BÊN KIA ĐẠI TÂY DƯƠNG", "at": [7, "Đại"], "sm": True},
                                          {"text": "BÁO CÁO LIGHTHILL", "at": [7, "Lighthill"], "acc": True},
                                          {"text": "Hội đồng Nghiên cứu Khoa học Anh", "at": [7, "Hội"], "sm": True}]},
    {"type": "quote", "at": 8, "text": "In no part of the field have the discoveries made so far produced the major impact that was then promised.",
     "by": "JAMES LIGHTHILL · 1973", "lbl": "TRÍCH"},
    {"type": "kinetic", "at": 9, "items": [{"text": "BÙNG NỔ TỔ HỢP", "at": [9, "bùng"], "acc": True},
                                          {"text": "bài toán lớn thêm một chút → số khả năng tăng vọt", "at": [10, "tăng"], "sm": True}]},
    {"type": "broll", "at": 11, "vid": "11072965", "veil": 0.45, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "PHÒNG THÍ NGHIỆM THU HẸP", "at": [11, "thu"]}, {"text": "MÙA ĐÔNG AI", "at": [12, "mùa"], "acc": True}]},
    {"type": "nn", "at": 13, "fwdAt": [14, "giữ"], "label": {"k": "VẪN CÓ NGƯỜI GIỮ LẠI", "v": "Ý TƯỞNG NƠ-RON", "at": [14, "lặng"]}},
    {"type": "question", "at": 15, "text": "Ai sẽ đào nó lên —\nvà bằng thứ gì?"},
    {"type": "timeline", "at": 16, "items": [{"year": "HÈ", "text": "1956", "at": [16, "Câu"]},
                                            {"year": "ĐÔNG", "text": "≈ 1974", "at": [16, "nơi"]},
                                            {"year": "ĐÔNG", "text": "?", "at": [17, "chết"]}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "MÁY THẮNG NGƯỜI, NHƯNG KHÔNG HỌC GÌ"}, "bgm": {"mood": "mystery", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "MÁY THẮNG NGƯỜI\nNHƯNG KHÔNG HỌC", "sub": "1980 — 1997", "bg": "lisp", "titleAt": [0, "Những"]},
    {"type": "print", "at": 1, "img": "lisp", "tone": "color", "side": {"k": "HỆ CHUYÊN GIA", "h": "Hàng nghìn dòng\n“nếu… thì…”", "lines": [
        {"text": "Ý tưởng vẫn là *viết luật*", "at": [1, "viết"]}, {"text": "Chép kinh nghiệm *chuyên gia*", "at": [2, "chép"]},
        {"text": "Máy *chuyên dụng* để chạy AI", "at": [3, "chuyên"]}]}},
    {"type": "slam", "at": 4, "text": "BONG BÓNG VỠ"},
    {"type": "broll", "at": 5, "vid": "6647520", "veil": 0.45, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "MÙA ĐÔNG THỨ HAI", "at": [5, "Mùa"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "LỜI HỨA 1958", "at": [6, "1958,"]},
                                          {"text": "10 NĂM → VÔ ĐỊCH CỜ VUA?", "at": [6, "vô"], "acc": True}]},
    {"type": "date", "at": 7, "vid": "6599643", "day": "PHILADELPHIA", "date": "02.1996",
     "sub": {"text": "KASPAROV 4 – 2 DEEP BLUE", "at": [8, "bốn"]}, "illus": "VIDEO MINH HỌA"},
    {"type": "photo", "at": 9, "img": "deepblue", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "05.1997 · NEW YORK", "at": [9, "1997,"]}, {"text": "DEEP BLUE 3½ – 2½", "at": [10, "ba"], "acc": True}],
     "label": {"k": "DEEP BLUE", "v": "TỦ MÁY · BẢO TÀNG LỊCH SỬ MÁY TÍNH", "at": [9, "đấu"]}},
    {"type": "kinetic", "at": 11, "items": [{"text": "LẦN ĐẦU TIÊN", "at": [11, "Lần"], "acc": True},
                                           {"text": "nhà vô địch đương nhiệm thua máy · thể thức chuẩn", "at": [11, "thua"], "sm": True}]},
    {"type": "counter", "at": 12, "from": 10, "to": 39, "suffix": " NĂM", "countAt": [12, "ba"], "label": "LỜI HỨA “MƯỜI NĂM”"},
    {"type": "question", "at": 13, "text": "Deep Blue có học không?"},
    {"type": "slam", "at": 14, "text": "GẦN NHƯ KHÔNG"},
    {"type": "print", "at": 15, "img": "dbchip", "tone": "color", "side": {"k": "SỨC TÍNH", "h": "200 triệu\nthế cờ / giây", "lines": [
        {"text": "Tiêu chí do *người chỉnh tay*", "at": [15, "chỉnh"]}, {"text": "Vẫn là *viết luật*", "at": [16, "viết"]}]}},
    {"type": "go", "at": 17, "stones": 70, "label": {"k": "CỜ VÂY · 19 × 19", "v": "SỨC TÍNH KHÔNG BAO GIỜ ĐỦ", "at": [18, "mười"]}},
    {"type": "kinetic", "at": 19, "items": [{"text": "TRỰC GIÁC", "at": [19, "trực"], "acc": True},
                                           {"text": "máy phải học được thứ này", "at": [19, "học"], "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "CON CHIP CHƠI GAME CỨU AI"}, "bgm": {"mood": "upbeat", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "CON CHIP CHƠI GAME\nCỨU AI", "sub": "1986 — 2016", "bg": "gtx580", "titleAt": [0, "Quay"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "GIỮA HAI MÙA ĐÔNG", "at": [1, "giữa"]},
                                          {"text": "RUMELHART · HINTON · WILLIAMS", "at": [1, "Rumelhart,"], "sm": True},
                                          {"text": "TẠP CHÍ NATURE", "at": [1, "Nature."], "acc": True}]},
    {"type": "nn", "at": 2, "fwdAt": [3, "đoán"], "backAt": [3, "truyền"], "label": {"k": "NATURE · 1986", "v": "LAN TRUYỀN NGƯỢC", "at": [2, "lan"]}},
    {"type": "kinetic", "at": 4, "items": [{"text": "MÁY QUÁ CHẬM", "at": [4, "chậm,"]}, {"text": "DỮ LIỆU QUÁ ÍT", "at": [4, "dữ"], "acc": True}]},
    {"type": "print", "at": 5, "img": "gtx580", "tone": "color", "side": {"k": "GPU", "h": "Chip đồ hoạ\ncho game", "lines": [
        {"text": "Vẽ *hàng triệu* điểm ảnh cùng lúc", "at": [6, "triệu"]},
        {"text": "Mạng nơ-ron: *hàng triệu* phép nhân song song", "at": [7, "phép"]}]}},
    {"type": "date", "at": 8, "day": "IMAGENET · ĐẠI HỌC TORONTO", "date": "2012", "sub": {"text": "ALEXNET", "at": [8, "AlexNet."]}},
    {"type": "kinetic", "at": 9, "items": [{"text": "2 × GTX 580", "at": [9, "hai"], "acc": True}, {"text": "5–6 NGÀY HUẤN LUYỆN", "at": [9, "năm,"]}]},
    {"type": "bars", "at": 10, "title": "TỈ LỆ ĐOÁN SAI (TOP-5) · ILSVRC 2012", "unit": "%", "items": [
        {"k": "ALEXNET", "v": 15.3, "lbl": "15,3%", "at": [10, "mười"], "acc": True}, {"k": "ĐỘI THỨ HAI", "v": 26.2, "lbl": "26,2%", "at": [11, "hai"]}]},
    {"type": "slam", "at": 12, "text": "CẢ NGÀNH\nQUAY ĐẦU"},
    {"type": "photo", "at": 13, "img": "perceptron", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "PERCEPTRON · 1958", "at": [13, "perceptron"], "acc": True}],
     "label": {"k": "MARK I PERCEPTRON", "v": "ẢNH HẢI QUÂN MỸ", "at": [13, "hiểu"]}},
    {"type": "kinetic", "at": 14, "items": [{"text": "“NGÕ CỤT”", "at": [14, "cụt"]},
                                           {"text": "= NỀN MÓNG CỦA HỌC SÂU", "at": [14, "sâu."], "acc": True}]},
    {"type": "slam", "at": 15, "text": "ĐI TRƯỚC\nCỖ MÁY CỦA MÌNH", "sub": "FRANK ROSENBLATT"},
    {"type": "go", "at": 16, "stones": 40, "label": {"k": "CỜ VÂY · 19 × 19", "at": [16, "bàn"]}},
    {"type": "date", "at": 17, "day": "SEOUL · ALPHAGO vs LEE SEDOL", "date": "03.2016", "sub": {"text": "DEEPMIND", "at": [17, "DeepMind"]}},
    {"type": "counter", "at": 18, "from": 0, "to": 200000000, "prefix": "> ", "countAt": [18, "hai"], "label": "NGƯỜI THEO DÕI"},
    {"type": "go", "at": 19, "stones": 48, "hitAt": [19, "ba"], "move": "37", "prob": "≈ 1/10.000", "label": {"k": "VÁN 2 · ALPHAGO", "at": [19, "Ván"]}},
    {"type": "slam", "at": 20, "text": "0 – 3", "sub": "LEE SEDOL THUA BA VÁN LIỀN", "white": True},
    {"type": "print", "at": 21, "img": "leesedol", "tone": "color", "side": {"k": "VÁN 4", "h": "Lee Sedol"}},
    {"type": "go", "at": 22, "stones": 56, "hitAt": [22, "bảy"], "move": "78", "prob": "≈ 1/10.000", "label": {"k": "VÁN 4 · LEE SEDOL", "at": [22, "Lee"]}},
    {"type": "kinetic", "at": 24, "items": [{"text": "NƯỚC 79: ALPHAGO ĐI SAI", "at": [24, "sai"], "acc": True},
                                           {"text": "gần mười nước sau mới nhận ra", "at": [24, "nhận"], "sm": True}]},
    {"type": "slam", "at": 25, "text": "LEE SEDOL THẮNG"},
    {"type": "slam", "at": 26, "text": "4 – 1", "sub": "ALPHAGO · CON NGƯỜI", "white": True},
    {"type": "broll", "at": 27, "vid": "29890356", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "BIẾT NHÌN ✓", "at": [27, "nhìn."]}, {"text": "BIẾT CHƠI ✓", "at": [27, "chơi."]},
             {"text": "BIẾT NÓI CHUYỆN?", "at": [28, "nói"], "acc": True}]},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "ĐOÁN CHỮ TIẾP THEO"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "ĐOÁN CHỮ\nTIẾP THEO", "sub": "2017 — 2025", "vid": "38081600", "titleAt": [0, "Tháng"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "TRANSFORMER", "at": [1, "Transformer."], "acc": True},
                                          {"text": "“Attention Is All You Need” · 2017", "at": [1, "Họ"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "NHÌN CẢ CÂU CÙNG LÚC", "at": [2, "cả"]},
                                          {"text": "CHỮ NÀO CHÚ Ý ĐẾN CHỮ NÀO", "at": [2, "chú"], "acc": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "3,5 NGÀY · 8 GPU", "at": [3, "ba"], "acc": True}]},
    {"type": "date", "at": 4, "day": "OPENAI · CHATGPT", "date": "30.11.2022", "sub": {"text": "MỞ CHO MỌI NGƯỜI DÙNG THỬ", "at": [4, "dùng"]}},
    {"type": "counter", "at": 5, "vid": "6963823", "from": 0, "to": 700000000, "prefix": "≈ ", "countAt": [5, "mỗi"],
     "label": "NGƯỜI DÙNG MỖI TUẦN", "sub": {"text": "GIỮA 2025 · THEO OPENAI", "at": [5, "OpenAI,"]}},
    {"type": "question", "at": 6, "text": "Bên trong nó đang làm gì?"},
    {"type": "chat", "at": 7, "head": "MÔ PHỎNG · ĐOÁN MẨU CHỮ TIẾP THEO", "stream": True, "msgs": [
        {"who": "u", "text": "Mùa hè năm 1956 ở Dartmouth có gì đặc biệt?", "at": [7, "Nói"]},
        {"who": "m", "text": "Mùa hè năm ấy, một nhóm nhà khoa học gặp nhau để bàn về cách làm cho máy biết suy nghĩ…", "at": [7, "đoán"], "dur": 4.5}]},
    {"type": "question", "at": 10, "text": "Có nghe quen không?"},
    {"type": "guess", "at": 11, "text": "THE ROOM WAS NOT VERY LIGHT", "startAt": [11, "đoán"], "until": [11, "lạ."],
     "statAt": [12, "bảy"], "right": 89, "total": 129, "label": {"k": "SHANNON · 1951 → 2022", "at": [11, "Shannon"]}},
    {"type": "question", "at": 13, "bg": "turing", "text": "Còn lời đoán của Turing?"},
    {"type": "kinetic", "at": 14, "items": [{"text": "PHÉP THỬ TURING · 2025", "at": [14, "phép"], "acc": True},
                                           {"text": "UC San Diego · nghiên cứu chưa bình duyệt", "at": [14, "bình"], "sm": True}]},
    {"type": "chat", "at": 15, "head": "MÔ PHỎNG · PHÉP THỬ 5 PHÚT", "msgs": [
        {"who": "u", "text": "Bạn là người thật chứ?", "at": [15, "trò"]},
        {"who": "m", "text": "TẤT NHIÊN RỒI :)", "at": [15, "người"]},
        {"who": "u", "text": "Ai trong hai người là máy?", "at": [15, "đoán"]}]},
    {"type": "bars", "at": 16, "title": "BỊ CHỌN LÀ “NGƯỜI”", "unit": "%", "items": [
        {"k": "GPT-4.5 (ĐÓNG VAI NGƯỜI)", "v": 73, "at": [16, "bảy"], "acc": True}, {"k": "ELIZA (1966)", "v": 23, "at": [17, "hai"]}]},
    {"type": "timeline", "at": 18, "items": [{"year": "TURING HẸN", "text": "2000", "at": [18, "2000."]},
                                            {"year": "MÁY TỚI", "text": "≈ 2025", "at": [18, "muộn"]}]},
    {"type": "broll", "at": 20, "vid": "34719182", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "KHÔNG CHỈ CÁC NHÀ KHOA HỌC", "at": [20, "khoa"]}, {"text": "TƯỞNG TƯỢNG VỀ AI", "at": [20, "tưởng"], "acc": True}]},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "PHIM ĐÃ DẠY TA SỢ, VÀ THƯƠNG, AI"}, "bgm": {"mood": "warm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "PHIM ĐÃ DẠY TA\nSỢ, VÀ THƯƠNG, AI", "sub": "1968 · 1984 · 1969", "titleAt": [0, "Trước"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "HAL 9000", "at": [1, "HAL"], "acc": True},
                                          {"text": "2001: A Space Odyssey · 1968", "at": [1, "1968,"], "sm": True},
                                          {"text": "BÌNH THẢN TỪ CHỐI MỞ CỬA", "at": [1, "từ"]}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "SKYNET", "at": [2, "Skynet,"], "acc": True},
                                          {"text": "Kẻ hủy diệt · 1984", "at": [2, "1984,"], "sm": True}]},
    {"type": "timeline", "at": 3, "items": [{"year": "TRONG PHIM", "text": "Ngày phán xét · 1997", "at": [3, "1997."]},
                                           {"year": "NGOÀI ĐỜI", "text": "Deep Blue thắng · 1997", "at": [3, "Deep"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "VỚI NGƯỜI VIỆT", "at": [4, "Việt,"]},
                                          {"text": "AI KHÔNG ĐÁNG SỢ CHÚT NÀO", "at": [4, "đáng"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "CUỐI 1969 · NHẬT BẢN", "at": [5, "1969,"]},
                                          {"text": "một chú mèo máy màu xanh", "at": [5, "mèo"], "sm": True}]},
    {"type": "slam", "at": 6, "text": "DORAEMON"},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHÔNG MUỐN THỐNG TRỊ AI", "at": [7, "thống"]},
                                          {"text": "chỉ muốn giúp một cậu bé hay quên làm bài tập", "at": [7, "giúp"], "sm": True, "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "HAI HÌNH MẪU", "at": [8, "hình"], "sm": True},
                                          {"text": "MỘT CỖ MÁY TA PHẢI ĐỀ PHÒNG", "at": [9, "đề"]},
                                          {"text": "MỘT NGƯỜI BẠN TA MUỐN CÓ", "at": [9, "bạn"], "acc": True}]},
    {"type": "question", "at": 10, "vid": "4685169", "text": "Thứ trong điện thoại của bạn\ngần với cái nào hơn?"},
]}

CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "MÙA HÈ THỨ BẢY MƯƠI"}, "bgm": {"mood": "epic", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "MÙA HÈ\nTHỨ BẢY MƯƠI", "sub": "2024 — 2026", "bg": "hinton", "titleAt": [0, "Tháng"]},
    {"type": "photo", "at": [0, "Nobel"], "img": "hinton", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "NOBEL VẬT LÝ 2024", "at": [0, "Vật"], "acc": True}, {"text": "HOPFIELD · HINTON", "at": [0, "Hinton,"]}],
     "label": {"k": "GEOFFREY HINTON", "v": "ẢNH 2023", "at": [0, "Hopfield"]}},
    {"type": "kinetic", "at": 1, "items": [{"text": "NOBEL HOÁ HỌC 2024 · MỘT NỬA", "at": [1, "Hoá"], "acc": True},
                                          {"text": "Hassabis · Jumper · AlphaFold", "at": [1, "AlphaFold"], "sm": True}]},
    {"type": "slam", "at": 2, "text": "TỪ NGÕ CỤT\nĐẾN NOBEL"},
    {"type": "quote", "at": 3, "text": "a kind of bifurcation point in history", "by": "GEOFFREY HINTON · PHỎNG VẤN NOBEL 2024",
     "lbl": "TRÍCH"},
    {"type": "photo", "at": 4, "img": "dartmouth", "tone": "color", "move": "out", "veil": 0.55,
     "kin": [{"text": "29 – 31.10.2026", "at": [4, "tháng"]}, {"text": "KHÔNG CÒN LÀ: “MÁY CÓ THÔNG MINH?”", "at": [5, "thông"], "sm": True},
             {"text": "WHAT MUST REMAIN HUMAN?", "at": [7, "Điều"], "acc": True}],
     "label": {"k": "DARTMOUTH · AI AT 70", "v": "ẢNH MINH HỌA", "at": [4, "Dartmouth"]}},
    {"type": "timeline", "at": 8, "items": [{"year": "HÈ", "text": "1956", "at": [8, "mùa"]},
                                           {"year": "ĐÔNG", "text": "≈ 1974", "at": [10, "hai"]},
                                           {"year": "ĐÔNG", "text": "≈ 1987", "at": [10, "đông."]},
                                           {"year": "HÈ", "text": "2012", "at": [11, "hè"]},
                                           {"year": "2026", "text": "?", "at": [12, "đông"]}]},
    {"type": "print", "at": 13, "img": "turing16", "tone": "bw", "side": {"k": "ALAN TURING · 1950", "h": "“Máy suy nghĩ”", "lines": [
        {"text": "Câu hỏi *quá vô nghĩa* để bàn", "at": [13, "vô"]},
        {"text": "Cuối thế kỷ, người ta sẽ nói *máy suy nghĩ*", "at": [14, "máy"]}]}},
    {"type": "slam", "at": 15, "text": "CÓ LẼ\nLÚC ẤY ĐÃ TỚI"},
    {"type": "question", "at": 16, "vid": "17342967", "text": "Mùa hè,\nhay sắp đến mùa đông?"},
]}

SPEC = {
    "title": "AI Đã \"Chết\" Hai Lần Trước Khi Có ChatGPT",
    "channel": "MIM", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True,
    "acc": ["perceptron", "chatgpt", "eliza", "alphago", "deep", "blue", "gpu", "alexnet", "mùa", "hè", "đông", "70"],
    "say": SAY, "imgs": IMGS, "chapters": list(CH),
    "youtube": {
        "titles": ["AI Đã \"Chết\" Hai Lần Trước Khi Có ChatGPT",
                   "Họ Nghĩ Chỉ Cần 1 Mùa Hè Để Tạo Ra AI. Mất 70 Năm.",
                   "70 Năm AI: Từ Cỗ Máy 5 Tấn Đến ChatGPT Trong Túi Bạn"],
        "summary": "Năm 1955, bốn nhà khoa học xin 10 người, 2 tháng, 13.500 đô để tạo bước tiến cho \"trí tuệ nhân tạo\". "
                   "Bảy mươi năm sau, qua hai mùa đông AI, một con chip chơi game và một trò đoán chữ từ năm 1951, ChatGPT trả lời bạn như một con người. "
                   "Đây là câu chuyện đó.",
        "more": [],
        "ch00_title": "Cỗ máy học được trái và phải (1958)",
        "chapter_titles": {"ch00": "Mở đầu: cỗ máy học được trái và phải (1958)", "ch01": "Một mùa hè để giải bài toán trí tuệ (1950–1956)",
                           "ch02": "Hai con đường: viết luật hay tự học, và ELIZA", "ch03": "Mùa đông AI thứ nhất",
                           "ch04": "Deep Blue: máy thắng người, nhưng không học", "ch05": "Con chip chơi game cứu AI: AlexNet và AlphaGo",
                           "ch06": "ChatGPT: đoán chữ tiếp theo", "ch07": "Phim đã dạy ta sợ, và thương, AI",
                           "ch08": "Kết: mùa hè thứ bảy mươi"},
        "sources": [
            "https://news.cornell.edu/stories/2019/09/professors-perceptron-paved-way-ai-60-years-too-soon",
            "http://www-formal.stanford.edu/jmc/history/dartmouth/dartmouth.html",
            "https://academic.oup.com/mind/article/LIX/236/433/986238",
            "https://doi.org/10.1002/j.1538-7305.1951.tb01366.x",
            "https://doi.org/10.1145/365153.365168",
            "https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm",
            "https://www.ibm.com/history/deep-blue",
            "https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks",
            "https://deepmind.google/research/alphago/",
            "https://arxiv.org/abs/1706.03762",
            "https://arxiv.org/abs/2503.23674",
            "https://www.nobelprize.org/prizes/physics/2024/summary/",
        ],
        "hashtags": ["AI", "TríTuệNhânTạo", "ChatGPT", "LịchSửAI", "MindInTheMachine"],
        "tags": ["trí tuệ nhân tạo", "lịch sử AI", "AI là gì", "ChatGPT", "mùa đông AI", "perceptron", "Deep Blue", "AlphaGo",
                 "Alan Turing", "Dartmouth 1956", "học sâu", "GPU", "mạng nơ-ron", "70 năm AI"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}

if __name__ == "__main__":
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec + 9 chương")
