"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #13 "Deep Blue đấu Kasparov" (chuỗi Trận đấu Người – Máy, loại 20-30 phút).

    python data/long/mim-deep-blue-kasparov/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Cảnh "chess" (lab.js): bàn ghi "THẾ CỜ THẬT" chỉ dùng cho thế cờ kênh dựng tay từ biên bản (ván 6/1997 sau
nước 8.Nxe6, FEN bên dưới, đã đối chiếu từng nước 1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4 Nd7 5.Ng5 Ngf6 6.Bd3 e6 7.N1f3 h6 8.Nxe6); thế ban đầu ghi "THẾ BAN
ĐẦU". Clip: Pexels (ngang), gắn "VIDEO MINH HỌA", không phải hình ảnh của trận đấu. Áp luật studio (14/10/2026): myth / source / units; năm không đếm.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"deep": "Đíp", "blue": "Blu", "ibm": "ai bi em", "=IBM": "ai bi em", "garry": "Ga-ri", "kasparov": "Cát-xpa-rốp", "claude": "Clốt", "shannon": "Sen-nần",
       "alan": "A-lần", "turing": "Tiu-rinh", "david": "Đây-vít", "levy": "Li-vai", "hamburg": "Hăm-buốc", "carnegie": "Các-nơ-ghi", "mellon": "Me-lần",
       "thought": "Thót", "big": "Bích", "philadelphia": "Phi-la-đen-phi-a", "eniac": "Ê-ni-ác", "=ENIAC": "Ê-ni-ác", "york": "Doóc", "new": "Niu",
       "caro-kann": "Ca-rô Can", "caro": "Ca-rô", "kann": "Can", "alphago": "An-pha Gô", "=AlphaGo": "An-pha Gô", "=AI": "ây ai", "alphazero": "An-pha Di-rô", "=AlphaZero": "An-pha Di-rô", "watson": "Oát-xần", "chinook": "Chi-núc", "alberta": "An-béc-ta", "marion": "Ma-ri-ần", "tinsley": "Tin-xli", "jonathan": "Gio-na-thần", "schaeffer": "Sép-phơ", "science": "Xai-ần"}
VM = "VIDEO MINH HỌA · KHÔNG PHẢI HÌNH ẢNH TRẬN ĐẤU"
REAL = "THẾ CỜ THẬT · KÊNH DỰNG LẠI TỪ BIÊN BẢN VÁN ĐẤU"
START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
G6_8 = "r1bqkb1r/pp1n1pp1/2p1Nn1p/8/3P4/3B1N2/PPP2PPP/R1BQK2R b KQkq - 0 8"      # ván 6/1997 sau 8.Nxe6
G6_7 = "r1bqkb1r/pp1n1pp1/2p1pn1p/6N1/3P4/3B1N2/PPP2PPP/R1BQK2R w KQkq - 0 8"   # trước 8.Nxe6 (sau 7...h6)


def score(at, km, db, sub="KASPAROV – DEEP BLUE", **kw):
    return {"type": "slam", "at": at, "text": f"{km} – {db}", "sub": sub, **kw}


CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MƯỜI CHÍN NƯỚC"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "12197806", "veil": 0.55, "illus": VM,
     "kin": [{"text": "11.05.1997 · NEW YORK", "at": [0, "Ngày"], "sm": True}, {"text": "MỘT BÀN CỜ VUA", "at": [1, "có"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "HAI ĐỐI THỦ", "rows": [{"k": "MỘT BÊN", "v": "KASPAROV · VÔ ĐỊCH THẾ GIỚI", "at": 2}, {"k": "BÊN KIA", "v": "MỘT NGƯỜI ĐẶT QUÂN THEO CỖ MÁY", "at": 3}]},
    {"type": "ledger", "at": 4, "title": "VÁN THỨ SÁU · VÁN CUỐI", "rows": [{"k": "TỈ SỐ", "v": "ĐANG HOÀ", "at": 5}, {"k": "VÁN CỜ", "v": "MỚI KHOẢNG MỘT GIỜ", "at": 6}]},
    {"type": "slam", "at": 8, "text": "XIN THUA SAU 19 NƯỚC", "sub": "NHÀ VÔ ĐỊCH THẾ GIỚI ĐỨNG DẬY", "subAt": 9},
    {"type": "broll", "at": 10, "vid": "5028622", "veil": 0.55, "illus": VM,
     "kin": [{"text": "DEEP BLUE", "at": [10, "Deep"], "acc": True}, {"text": "lần đầu máy tính thắng nhà vô địch cờ vua thế giới · thể thức chuẩn", "at": 11, "sm": True}]},
    {"type": "timeline", "at": 13, "items": [{"year": "1950", "text": "một bài báo về máy chơi cờ", "at": 13}, {"year": "1997", "text": "mười chín nước ở New York", "at": [13, "và"]},
                                            {"year": "2017", "text": "một cuốn sách, hai mươi năm sau", "at": [13, "trong"]}]},
    {"type": "ledger", "at": 14, "title": "BA CÂU NÓI CỦA KASPAROV", "rows": [{"k": "1", "v": "NĂM 26 TUỔI", "at": [15, "Một"]}, {"k": "2", "v": "NĂM 34 TUỔI", "at": [15, "ba"]},
                                                                           {"k": "3", "v": "NĂM 54 TUỔI", "at": [15, "Và"]}], "total": {"k": "MỘT CON NGƯỜI", "v": "TRƯỚC MỘT CỖ MÁY", "at": 16}},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MỘT GIẤC MƠ CŨ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MỘT GIẤC MƠ CŨ", "sub": "MÁY BIẾT ĐÁNH CỜ", "vid": "34187599", "illus": VM, "titleAt": [0, "Ước"]},
    {"type": "source", "at": 1, "source": "CLAUDE SHANNON · 1949 – 1950", "ref": "LẬP TRÌNH MÁY TÍNH CHƠI CỜ", "snippet": "bài báo kỹ thuật [[đầu tiên]] về máy chơi cờ · không kèm chương trình nào",
     "hlAt": [2, "đầu"], "seal": "CHỈ LÀ CÁCH NGHĨ", "sealAt": [4, "Nó"]},
    {"type": "timeline", "at": 5, "items": [{"year": "BƯỚC 1", "text": "thử các nước đi", "at": [5, "Máy"]}, {"year": "BƯỚC 2", "text": "các nước đáp lại, rồi đáp lại nữa", "at": [5, "rồi"]},
                                           {"year": "BƯỚC 3", "text": "chấm điểm từng thế cờ, chọn hướng có lợi nhất", "at": 6}]},
    {"type": "chess", "at": 7, "fen": START, "label": {"k": "THẾ BAN ĐẦU · 20 NƯỚC ĐI ĐẦU CÓ THỂ CHỌN", "v": "SỐ VÁN CÓ THỂ XẢY RA: KHÔNG MÁY NÀO DUYỆT HẾT", "at": 8}},
    {"type": "broll", "at": 10, "vid": "7969842", "veil": 0.55, "illus": VM,
     "kin": [{"text": "ALAN TURING · NƯỚC ANH", "at": 10, "sm": True}, {"text": "TỰ LÀM CỖ MÁY BẰNG GIẤY", "at": [12, "Turing"], "acc": True},
             {"text": "gần nửa giờ cho mỗi nước · và thua một đồng nghiệp", "at": 13, "sm": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "GẦN 70 NĂM · CÙNG MỘT CÁCH NGHĨ", "at": 15, "sm": True}, {"text": "NHƯNG NHIỀU NĂM ĐẦU: CHƠI RẤT TỆ", "at": 16, "acc": True}]},
    {"type": "ledger", "at": 17, "title": "LỜI CƯỢC CỦA DAVID LEVY · 1968", "rows": [{"k": "CƯỢC", "v": "10 NĂM, KHÔNG MÁY NÀO THẮNG ÔNG", "at": 18}, {"k": "TỔNG TIỀN CƯỢC", "v": "1.250 BẢNG ANH", "at": 19},
                                                                                     {"k": "1978", "v": "LEVY THẮNG · GIỮ ĐƯỢC LỜI CƯỢC", "at": [20, "Và"]}]},
    {"type": "myth", "at": 21, "mythLab": "LEVY TỪNG NGHĨ", "myth": "MÁY CHƠI CỜ RẤT YẾU", "truthLab": "CHÍNH ÔNG VIẾT", "truth": "MẠNH HƠN TÔI TƯỞNG", "strikeAt": [22, "Nhưng"], "truthAt": [22, "mạnh"]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BA MƯƠI HAI CHIẾC MÁY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "BA MƯƠI HAI\nCHIẾC MÁY", "sub": "HAMBURG · 1985", "vid": "6058907", "illus": VM, "titleAt": [0, "Cùng"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "GARRY KASPAROV", "at": 1, "acc": True}, {"text": "22 tuổi · nhà vô địch thế giới trẻ nhất tới khi ấy", "at": 2, "sm": True}]},
    {"type": "units", "at": 3, "title": "HAMBURG · 06.1985 · ĐẤU CÙNG LÚC 32 MÁY CHƠI CỜ", "total": 32, "cols": 8, "lit": 32, "litAt": [6, "Kết"], "unitLabel": "VÁN THẮNG · KHÔNG THUA VÁN NÀO",
     "label": {"k": "HƠN NĂM GIỜ ĐI TỪ BÀN NÀY SANG BÀN KHÁC", "v": "", "at": 5}},
    {"type": "myth", "at": 7, "mythLab": "TRẬN ẤY", "myth": "DỄ DÀNG", "truthLab": "THEO LỜI KASPAROV", "truth": "CÓ MỘT VÁN THẾ KHÓ", "strikeAt": [7, "không"], "truthAt": [7, "có"]},
    {"type": "ledger", "at": 8, "title": "THÔNG ĐIỆP NĂM 1985", "rows": [{"k": "MÁY", "v": "TÍNH NHANH", "at": 9}, {"k": "TRƯỚC NHÀ VÔ ĐỊCH", "v": "VẪN LÀ NGHIỆP DƯ", "at": 10}]},
    {"type": "broll", "at": 11, "vid": "8888818", "veil": 0.55, "illus": VM,
     "kin": [{"text": "BỐN NĂM SAU · MỘT ĐỐI THỦ KHÁC HẲN", "at": 11, "sm": True}, {"text": "TỪ MỘT PHÒNG THÍ NGHIỆM CỦA SINH VIÊN", "at": 13, "acc": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CÂU NÓI THỨ NHẤT"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CÂU NÓI\nTHỨ NHẤT", "sub": "DEEP THOUGHT · 1989", "vid": "8058350", "illus": VM, "titleAt": [0, "Giữa"]},
    {"type": "timeline", "at": 1, "items": [{"year": "GIỮA THẬP NIÊN 80", "text": "chip chơi cờ của nghiên cứu sinh Carnegie Mellon", "at": [1, None, 0, 0.05]},
                                           {"year": "DẪN ĐẦU", "text": "Hứa Phong Hùng · kỹ sư sinh ra ở Đài Loan", "at": 1},
                                           {"year": "DEEP THOUGHT", "text": "tên lấy từ một cỗ máy trong tiểu thuyết", "at": 3}]},
    {"type": "ledger", "at": 4, "title": "DEEP THOUGHT · 1989", "rows": [{"k": "DANH HIỆU", "v": "VÔ ĐỊCH MÁY TÍNH CHƠI CỜ", "at": 4}, {"k": "THẮNG", "v": "DAVID LEVY · NGƯỜI ĐẶT CƯỢC", "at": 5},
                                                                     {"k": "10.1989 · NEW YORK", "v": "GẶP KASPAROV · 2 VÁN", "at": 6}]},
    {"type": "quote", "at": 7, "text": "Tôi phải thách đấu Deep Thought để bảo vệ loài người.", "who": "GARRY KASPAROV", "note": "TRÍCH DỊCH · SPORTS ILLUSTRATED, 10.1989"},
    {"type": "slam", "at": 9, "text": "CÂU NÓI THỨ NHẤT", "sub": "KASPAROV · 26 TUỔI", "subAt": 9},
    score(10, 2, 0, "KASPAROV – DEEP THOUGHT · 1989"),
    {"type": "ledger", "at": 11, "title": "NHÓM KỸ SƯ KHÔNG BỎ CUỘC", "rows": [{"k": "IBM", "v": "MỜI VỀ · DỒN TIỀN CHO DỰ ÁN", "at": 12}, {"k": "1993", "v": "ĐỔI TÊN", "at": 13}],
     "total": {"k": "DEEP THOUGHT + BIG BLUE", "v": "= DEEP BLUE", "at": 14}},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "PHILADELPHIA · 1996"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "PHILADELPHIA,\nVÁN ĐẦU TIÊN", "sub": "THÁNG 2 NĂM 1996", "vid": "6599643", "illus": VM, "titleAt": [0, "Tháng"]},
    {"type": "ledger", "at": 1, "title": "TRẬN ĐẤU SÁU VÁN · 1996", "rows": [{"k": "THỂ THỨC", "v": "CHUẨN · 2 GIỜ CHO 40 NƯỚC ĐẦU", "at": 1}, {"k": "DEEP BLUE", "v": "~100 TRIỆU THẾ CỜ/GIÂY", "at": 2}],
     "total": {"k": "AI CŨNG NGHĨ", "v": "KASPAROV SẼ THẮNG", "at": 4}},
    {"type": "broll", "at": 5, "vid": "4954316", "ms": 2, "veil": 0.55, "illus": VM,
     "kin": [{"text": "KỶ NIỆM 50 NĂM MÁY TÍNH HIỆN ĐẠI", "at": 6, "acc": True}, {"text": "1946 · ENIAC ra mắt ở Philadelphia", "at": 7, "sm": True},
             {"text": "1996 · một cỗ máy ngồi đối diện nhà vô địch", "at": 8, "sm": True}]},
    {"type": "slam", "at": 9, "text": "10.02.1996 · CỖ MÁY THẮNG", "sub": "LẦN ĐẦU: MÁY THẮNG NHÀ VÔ ĐỊCH ĐƯƠNG NHIỆM · THỜI GIAN CHUẨN", "subAt": 11},
    score(12, 0, 1, "VÁN 1 · 1996"),
    {"type": "bars", "at": 13, "title": "KẾT QUẢ CỦA KASPAROV · 6 VÁN 1996", "unit": "SỐ VÁN",
     "items": [{"k": "THẮNG", "v": 3, "lbl": "3", "at": [14, "thắng"], "acc": True}, {"k": "HOÀ", "v": 2, "lbl": "2", "at": [14, "hoà"]}, {"k": "THUA", "v": 1, "lbl": "1", "at": [14, None, 0, 0.05]}]},
    score(15, 4, 2, "CHUNG CUỘC · 1996"),
    {"type": "kinetic", "at": 16, "items": [{"text": "ÔNG VẪN LÀ NHÀ VÔ ĐỊCH", "at": 16, "sm": True}, {"text": "NHƯNG ĐÃ CÓ MỘT VẾT NỨT", "at": 17, "acc": True}, {"text": "và IBM muốn một trận nữa", "at": 18, "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "CỖ MÁY THỨ HAI"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "CỖ MÁY THỨ HAI", "sub": "15 THÁNG SAU", "vid": "6804656", "illus": VM, "titleAt": [0, "Mười"]},
    {"type": "bars", "at": 1, "title": "THẾ CỜ DEEP BLUE DUYỆT MỖI GIÂY (TRIỆU)", "unit": "THEO TƯ LIỆU VỀ TRẬN ĐẤU",
     "items": [{"k": "1996", "v": 100, "lbl": "~100", "at": [2, "gấp"]}, {"k": "1997", "v": 200, "lbl": "~200", "at": [2, "hai"], "acc": True}]},
    {"type": "counter", "at": 3, "from": 200, "to": 200, "suffix": " TRIỆU", "label": "THẾ CỜ · CHỈ TRONG MỘT GIÂY", "sub": {"text": "MỘT KỲ THỦ CHỈ CÂN NHẮC KỸ VÀI NƯỚC ĐÁNG XEM", "at": 5}},
    {"type": "kinetic", "at": 6, "items": [{"text": "ĐẠI KIỆN TƯỚNG GIÚP CỖ MÁY", "at": 6, "acc": True}, {"text": "chấm điểm thế cờ · chuẩn bị khai cuộc", "at": [6, "chấm"], "sm": True}]},
    {"type": "ledger", "at": 7, "title": "TÁI ĐẤU · NEW YORK · 05.1997", "rows": [{"k": "SỐ VÁN", "v": "SÁU", "at": [8, "Sáu"]}, {"k": "NGƯỜI THẮNG", "v": "700.000 ĐÔ LA", "at": [8, "bảy"]},
                                                                                 {"k": "NGƯỜI THUA", "v": "400.000 ĐÔ LA", "at": [8, "bốn"]}],
     "total": {"k": "GIẢI TỪ 1980", "v": "+100.000 ĐÔ LA", "at": 9}},
    {"type": "broll", "at": 10, "vid": "4954316", "veil": 0.55, "illus": VM,
     "kin": [{"text": "KHÁN PHÒNG ĐÔNG NGHẸT", "at": 10, "sm": True}, {"text": "KHÔNG CÒN “BẢO VỆ LOÀI NGƯỜI”", "at": 11, "acc": True}, {"text": "ông chỉ muốn thắng · như mọi lần", "at": 12, "sm": True}]},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "VÁN MỘT: MỘT NƯỚC CỜ LẠ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "VÁN MỘT", "title": "MỘT NƯỚC CỜ LẠ", "sub": "03.05.1997", "vid": "6058369", "illus": VM, "titleAt": [0, "Ngày"]},
    score(1, 1, 0, "VÁN 1 · 1997"),
    {"type": "kinetic", "at": 2, "items": [{"text": "NƯỚC THỨ 44 CỦA DEEP BLUE", "at": 3, "acc": True}, {"text": "một nước xe không cứu được gì", "at": 4, "sm": True}]},
    {"type": "ledger", "at": 5, "title": "ĐỘI CỦA KASPAROV ĐỌC RA", "rows": [{"k": "CÓ LẼ", "v": "MÁY THẤY ĐIỀU RẤT SÂU", "at": 6}, {"k": "MỘT TRÍ TUỆ", "v": "NGOÀI TẦM HIỂU", "at": 7}]},
    {"type": "myth", "at": 8, "mythLab": "TƯỞNG LÀ", "myth": "THIÊN TÀI", "truthLab": "THEO LỜI MỘT THÀNH VIÊN ĐỘI DEEP BLUE", "truth": "MỘT CON BỌ PHẦN MỀM", "strikeAt": [9, "Nước"], "truthAt": [9, "con"]},
    {"type": "timeline", "at": 10, "items": [{"year": "LỖI", "text": "cỗ máy kẹt trong một vòng lặp", "at": 10}, {"year": "THOÁT RA", "text": "chọn đại một nước đi hợp lệ", "at": [10, "chọn"]}], "tag": {"text": "KỂ TRONG MỘT CUỐN SÁCH NĂM 2012", "at": 13}},
    {"type": "slam", "at": 14, "text": "CHƯA CẦN THÔNG MINH HƠN", "sub": "CHỈ CẦN KHIẾN ÔNG TIN NHƯ VẬY", "subAt": 15},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "VÁN HAI: LỜI BUỘC TỘI"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "7", "k": "VÁN HAI", "title": "LỜI BUỘC TỘI", "sub": "04.05.1997", "vid": "6689582", "illus": VM, "titleAt": [0, "Ván"]},
    {"type": "myth", "at": 3, "mythLab": "MÁY THỜI ẤY", "myth": "THẤY QUÂN HỞ LÀ ĂN", "truthLab": "VÁN NÀY DEEP BLUE", "truth": "TỪ CHỐI MIẾNG MỒI", "strikeAt": [5, "Ở"], "truthAt": [6, "từ"]},
    {"type": "kinetic", "at": 6, "items": [{"text": "NHỮNG NƯỚC ÂM THẦM, CHẬM RÃI", "at": [6, "đi"], "sm": True}, {"text": "NHƯ MỘT ĐẠI KIỆN TƯỚNG", "at": [6, "như"], "acc": True}]},
    score(7, 1, 1, "SAU VÁN 2 · KASPAROV XIN THUA"),
    {"type": "source", "at": 10, "source": "PHÂN TÍCH SAU TRẬN", "ref": "THẾ CỜ LÚC KASPAROV XIN THUA", "snippet": "quân đen có thể [[chiếu tướng liên tục]] để buộc ván cờ hoà",
     "hlAt": [12, "chiếu"], "seal": "LẼ RA CÓ THỂ HOÀ", "sealAt": 13},
    {"type": "ledger", "at": 14, "title": "HAI PHÍA", "rows": [{"k": "KASPAROV NGHI", "v": "CÓ NGƯỜI CAN THIỆP", "at": 15}, {"k": "IBM NÓI", "v": "CHỈ CAN THIỆP GIỮA VÁN", "at": 16}]},
    {"type": "slam", "at": 18, "text": "CÂU NÓI THỨ HAI", "sub": "MỘT LỜI BUỘC TỘI · MANG THEO NHIỀU NĂM", "subAt": 19},
]}

CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "BA VÁN HOÀ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "8", "k": "VÁN BA, BỐN, NĂM", "title": "BA VÁN HOÀ", "sub": "CHƠI ĐỂ CHỐNG LẠI MỘT CỖ MÁY", "vid": "8427421", "illus": VM, "titleAt": [0, "Kasparov"]},
    {"type": "myth", "at": 1, "mythLab": "ÔNG KHÔNG CÒN CHƠI", "myth": "CỜ CỦA KASPAROV", "truthLab": "MÀ CHƠI", "truth": "ĐỂ CHỐNG LẠI MÁY", "strikeAt": [2, "Ông"], "truthAt": 3},
    {"type": "ledger", "at": 4, "title": "CHIẾN THUẬT KHI ĐẤU VỚI MÁY", "rows": [{"k": "TRÁNH", "v": "THẾ CỜ MỞ · TÍNH RA ĐƯỢC", "at": 6}, {"k": "KÉO VÀO", "v": "THẾ ĐÓNG · KẾ HOẠCH DÀI HẠN", "at": 7}],
     "total": {"k": "CÁI GIÁ", "v": "KHÔNG PHẢI CỜ CỦA ÔNG", "at": 8}},
    {"type": "units", "at": 9, "title": "VÁN 3 · VÁN 4 · VÁN 5", "total": 3, "cols": 3, "lit": 3, "litAt": [9, "Ván"], "unitLabel": "VÁN HOÀ"},
    score(14, "2½", "2½", "TRƯỚC VÁN CUỐI"),
    {"type": "kinetic", "at": 15, "items": [{"text": "MỌI THỨ DỒN VÀO MỘT VÁN", "at": 15, "acc": True}, {"text": "không còn là nhà vô địch tự tin của Hamburg năm nào", "at": 16, "sm": True}]},
]}

CH["ch09"] = {"hud": {"k": "CHƯƠNG 09", "t": "VÁN SÁU"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "9", "k": "VÁN SÁU", "title": "VÁN SÁU", "sub": "11.05.1997", "vid": "6058907", "ms": 2, "illus": VM, "titleAt": [0, "Ngày"]},
    {"type": "ledger", "at": 1, "title": "KASPAROV CẦM QUÂN ĐEN", "rows": [{"k": "KHAI CUỘC", "v": "CARO-KANN · PHÒNG THỦ", "at": 2}, {"k": "NƯỚC 7", "v": "ĐẨY MỘT CON TỐT", "at": 3}],
     "total": {"k": "SÁCH KHAI CUỘC", "v": "NƯỚC ẤY CÓ VẤN ĐỀ", "at": 4}},
    {"type": "chess", "at": 5, "fen": G6_7, "label": {"k": "VÁN 6 · SAU NƯỚC 7 CỦA QUÂN ĐEN", "v": REAL, "at": 5}},
    {"type": "chess", "at": 6, "fen": G6_8, "hit": "e6", "hitAt": [7, "thí"], "move": "8", "prob": "mã trắng ăn tốt e6 · thí quân",
     "label": {"k": "VÁN 6 · NƯỚC 8: DEEP BLUE THÍ CON MÃ", "v": REAL, "at": 6}},
    {"type": "question", "at": 8, "text": "Nước thí quân đã có trong sách.\nVì sao Kasparov để thế cờ đi tới đó?"},
    {"type": "ledger", "at": 12, "title": "GIẢ THUYẾT CỦA HỨA PHONG HÙNG", "rows": [{"k": "CÓ THỂ", "v": "MỘT NƯỚC LẠ ĐỂ ĐÁNH LỪA MÁY", "at": 13}, {"k": "VỚI NIỀM TIN", "v": "MÁY KHÔNG DÁM THÍ QUÂN", "at": [13, "với"]}],
     "total": {"k": "NHƯNG", "v": "MÁY CÓ SẴN NƯỚC ẤY", "at": 14}},
    {"type": "broll", "at": 15, "vid": "6599643", "ms": 4, "veil": 0.55, "illus": VM,
     "kin": [{"text": "THẾ CỜ TRƯỢT DẦN", "at": 15, "sm": True}, {"text": "VUA ĐEN KẸT GIỮA BÀN", "at": 16, "acc": True}]},
    {"type": "counter", "at": 17, "from": 19, "to": 19, "suffix": " NƯỚC", "label": "KHOẢNG MỘT GIỜ · KASPAROV XIN THUA", "sub": {"text": "11.05.1997", "at": 17}},
    score(18, "2½", "3½", "CHUNG CUỘC · 1997"),
]}

CH["ch10"] = {"hud": {"k": "CHƯƠNG 10", "t": "SAU TRẬN"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "10", "k": "CHƯƠNG MƯỜI", "title": "SAU TRẬN", "sub": "NHẬT KÝ, TÁI ĐẤU, VÀ MỘT CỖ MÁY BỊ THÁO", "vid": "8328462", "illus": VM, "titleAt": [0, "Kasparov"]},
    {"type": "ledger", "at": 1, "title": "KASPAROV ĐÒI", "rows": [{"k": "1", "v": "XEM NHẬT KÝ TỪNG NƯỚC MÁY TÍNH", "at": 2}, {"k": "2", "v": "MỘT TRẬN ĐẤU LẠI", "at": 4}]},
    {"type": "ledger", "at": 3, "title": "IBM", "rows": [{"k": "NHẬT KÝ", "v": "SAU MỚI CÔNG BỐ", "at": 3}, {"k": "ĐẤU LẠI", "v": "TỪ CHỐI", "at": 5}],
     "total": {"k": "DEEP BLUE", "v": "BỊ THÁO DỠ", "at": [5, "Và"]}},
    {"type": "bars", "at": 7, "title": "TIỀN THƯỞNG 1997 (NGHÌN ĐÔ LA)", "unit": "THEO TƯ LIỆU VỀ TRẬN ĐẤU",
     "items": [{"k": "ĐỘI DEEP BLUE", "v": 700, "lbl": "700", "at": [8, "bảy"], "acc": True}, {"k": "GIẢI LẬP TỪ 1980", "v": 100, "lbl": "+100", "at": [8, "cộng"]}, {"k": "KASPAROV", "v": 400, "lbl": "400", "at": [8, None, 0, 0.6]}]},
    {"type": "broll", "at": 9, "vid": "5028622", "ms": 10, "veil": 0.55, "illus": VM, "kin": [{"text": "MỘT PHẦN CỖ MÁY · NAY Ở BẢO TÀNG", "at": 9, "sm": True}]},
    {"type": "question", "at": 10, "text": "Cỗ máy ấy có thật sự hiểu cờ vua?\nHay chỉ tính rất, rất nhanh?", "showAt": 11},
]}

CH["ch11"] = {"hud": {"k": "CHƯƠNG 11", "t": "MÁY CÓ “NGHĨ” KHÔNG?"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "11", "k": "CHƯƠNG MƯỜI MỘT", "title": "MÁY CÓ “NGHĨ”\nKHÔNG?", "sub": "BÊN TRONG MỘT NƯỚC ĐI", "vid": "6804656", "ms": 12, "illus": VM, "titleAt": [0, "Câu"]},
    {"type": "ledger", "at": 1, "title": "DEEP BLUE LÀ GÌ", "rows": [{"k": "1", "v": "TÌM KIẾM CỰC NHANH", "at": 1}, {"k": "2", "v": "CÁCH CHẤM ĐIỂM DO NGƯỜI VIẾT", "at": [1, "kèm"]}],
     "total": {"k": "MỖI GIÂY", "v": "~200 TRIỆU THẾ CỜ", "at": 2}},
    {"type": "chess", "at": 3, "fen": START, "label": {"k": "THẾ BAN ĐẦU · MINH HOẠ CÁCH MÁY “NHÌN TRƯỚC”", "v": "XÉT NƯỚC MÌNH → NƯỚC ĐÁP → NƯỚC ĐÁP LẠI …", "at": 4}},
    {"type": "bars", "at": 6, "title": "DEEP BLUE NHÌN TRƯỚC BAO NHIÊU NƯỚC", "unit": "THEO TƯ LIỆU VỀ DEEP BLUE",
     "items": [{"k": "THƯỜNG", "v": 8, "lbl": "6 – 8", "at": [6, "sáu"]}, {"k": "CÓ THẾ CỜ", "v": 20, "lbl": "> 20", "at": [6, "hơn"], "acc": True}]},
    {"type": "ledger", "at": 7, "title": "Ở TẦNG CUỐI: CHẤM ĐIỂM", "rows": [{"k": "1", "v": "QUÂN CÒN BAO NHIÊU", "at": [7, "quân"]}, {"k": "2", "v": "VUA CÓ AN TOÀN", "at": [7, "vua"]}, {"k": "3", "v": "CÁC QUÂN ĐỨNG CÓ TỐT", "at": [7, "các"]}],
     "total": {"k": "RỒI CHỌN", "v": "ĐƯỜNG TỚI ĐIỂM TỐT NHẤT", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "CÁCH NGHĨ CỦA SHANNON · 1950", "at": 9, "sm": True}, {"text": "CHẠY NHANH HƠN HÀNG TRIỆU LẦN", "at": 10, "acc": True}]},
    {"type": "myth", "at": 11, "mythLab": "DEEP BLUE MẠNH VÌ", "myth": "HIỂU CỜ NHƯ NGƯỜI", "truthLab": "THẬT RA", "truth": "SỨC TÍNH TOÁN", "strikeAt": [13, "Nói"], "truthAt": [13, "sức"]},
    {"type": "ledger", "at": 14, "title": "HAI CON ĐƯỜNG", "rows": [{"k": "DEEP BLUE", "v": "TÌM KIẾM + LUẬT NGƯỜI VIẾT", "at": 14}, {"k": "ALPHAGO", "v": "TỰ HỌC TỪ VÁN CỜ", "at": 15}]},
    {"type": "slam", "at": 17, "text": "KHÔNG CẦN NGHĨ GIỐNG NGƯỜI", "sub": "ĐỂ THẮNG NGƯỜI Ở MỘT TRÒ CHƠI", "subAt": 18},
]}

CH["ch12"] = {"hud": {"k": "CHƯƠNG 12", "t": "MỘT TRÒ CHƠI ĐÃ CÓ LỜI GIẢI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "12", "k": "CHƯƠNG MƯỜI HAI", "title": "MỘT TRÒ CHƠI\nĐÃ CÓ LỜI GIẢI", "sub": "CỜ VUA THÌ CHƯA", "vid": "8888818", "ms": 2, "illus": VM, "titleAt": [0, "Có"]},
    {"type": "question", "at": 1, "text": "Nếu cả hai chơi hoàn hảo,\nván cờ vua kết thúc thế nào?"},
    {"type": "bars", "at": 4, "title": "SỐ CHỮ SỐ CỦA HAI CON SỐ", "unit": "ƯỚC TÍNH CỦA SHANNON · ƯỚC TÍNH THƯỜNG DÙNG",
     "items": [{"k": "SỐ VÁN CỜ VUA CÓ THỂ XẢY RA", "v": 120, "lbl": "~120", "at": [4, "một"], "acc": True}, {"k": "SỐ NGUYÊN TỬ TRONG VŨ TRỤ QUAN SÁT ĐƯỢC", "v": 80, "lbl": "~80", "at": [5, "tám"]}]},
    {"type": "slam", "at": 6, "text": "CỜ VUA CHƯA ĐƯỢC GIẢI", "sub": "KHÔNG AI BIẾT KẾT QUẢ CỦA VÁN CỜ HOÀN HẢO", "subAt": 6},
    {"type": "source", "at": 7, "source": "TẠP CHÍ SCIENCE · 2007 · ĐẠI HỌC ALBERTA", "ref": "CỜ ĐAM ĐÃ ĐƯỢC GIẢI", "snippet": "nếu cả hai chơi hoàn hảo, [[cờ đam luôn hoà]]",
     "hlAt": [10, "cờ"], "seal": "MẤT 18 NĂM", "sealAt": 11},
    {"type": "ledger", "at": 12, "title": "CHINOOK", "rows": [{"k": "1994", "v": "ĐẤU NHÀ VÔ ĐỊCH MARION TINSLEY", "at": 13}, {"k": "GIỮA CHỪNG", "v": "ÔNG RÚT LUI VÌ BỆNH", "at": 14}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "JONATHAN SCHAEFFER", "at": 15, "acc": True}, {"text": "người viết bài điểm sách cho Kasparov, 20 năm sau", "at": 16, "sm": True},
                                           {"text": "thế giới máy chơi cờ hoá ra rất nhỏ", "at": 17, "sm": True}]},
    {"type": "myth", "at": 18, "mythLab": "MÁY MẠNH NHẤT", "myth": "BIẾT LỜI GIẢI", "truthLab": "THẬT RA", "truth": "CHỈ CHƠI TỐT HƠN TA", "strikeAt": [19, "Nhưng"], "truthAt": [20, "Nó"]},
]}

CH["ch13"] = {"hud": {"k": "CHƯƠNG 13", "t": "CON NHÂN MÃ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "13", "k": "CHƯƠNG MƯỜI BA", "title": "CON NHÂN MÃ", "sub": "NGƯỜI VÀ MÁY CÙNG MỘT PHE", "vid": "8427421", "ms": 8, "illus": VM, "titleAt": [0, "Nếu"]},
    {"type": "ledger", "at": 1, "title": "KIỂU CỜ KASPAROV ĐỀ XUẤT", "rows": [{"k": "LUẬT", "v": "ĐƯỢC DÙNG MÁY SUỐT VÁN ĐẤU", "at": 2}, {"k": "TÊN GỌI", "v": "NHÂN MÃ · NỬA NGƯỜI NỬA NGỰA", "at": 3}],
     "total": {"k": "06.1998", "v": "TRẬN ĐẦU TIÊN: HOÀ", "at": 6}},
    {"type": "ledger", "at": 7, "title": "GIẢI ĐẤU TRÊN MẠNG · 2005", "rows": [{"k": "CÓ", "v": "ĐỘI CÓ ĐẠI KIỆN TƯỚNG", "at": 8}, {"k": "CÓ CẢ", "v": "SIÊU MÁY TÍNH CHƠI CỜ", "at": 9}]},
    {"type": "myth", "at": 10, "mythLab": "AI ĐƯỢC CHỜ ĐỢI SẼ THẮNG", "myth": "ĐẠI KIỆN TƯỚNG", "truthLab": "NGƯỜI THẮNG", "truth": "HAI TAY CHƠI NGHIỆP DƯ", "strikeAt": [10, "Người"], "truthAt": [10, "hai"]},
    {"type": "bars", "at": 11, "title": "HỆ SỐ CỦA HAI NGƯỜI THẮNG (USCF)", "unit": "THEO CHESSBASE, 06.2005 · ĐẠI KIỆN TƯỚNG THƯỜNG TRÊN 2.500",
     "items": [{"k": "NGƯỜI THỨ NHẤT", "v": 1685, "lbl": "1.685", "at": [12, "Hệ"]}, {"k": "NGƯỜI THỨ HAI", "v": 1398, "lbl": "1.398", "at": [12, "thấp"]}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "HỌ BIẾT KHI NÀO NÊN TIN MÁY", "at": 14, "acc": True}, {"text": "và khi nào dùng phán đoán của mình", "at": [14, "và"], "sm": True}]},
    {"type": "slam", "at": 16, "text": "NGƯỜI BÌNH THƯỜNG + MÁY + CÁCH LÀM TỐT", "sub": "> NGƯỜI RẤT GIỎI + CÁCH LÀM TỒI · Ý LỜI KASPAROV", "subAt": 17},
]}

CH["ch14"] = {"hud": {"k": "CHƯƠNG 14", "t": "CÂU NÓI THỨ BA"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "14", "k": "CHƯƠNG MƯỜI BỐN", "title": "CÂU NÓI THỨ BA", "sub": "2017 · HAI MƯƠI NĂM SAU", "vid": "34187599", "ms": 6, "illus": VM, "titleAt": [0, "Hai"]},
    {"type": "question", "at": 2, "text": "Deep Blue có gian lận không?"},
    {"type": "ledger", "at": 3, "title": "CÂU TRẢ LỜI CỦA KASPAROV", "rows": [{"k": "NHIỀU NĂM", "v": "“TÔI KHÔNG BIẾT”", "at": 3}, {"k": "SAU 20 NĂM", "v": "SUY NGHĨ · PHÂN TÍCH", "at": 4}]},
    {"type": "slam", "at": 5, "text": "KHÔNG.", "sub": "CÂU NÓI THỨ BA · KASPAROV 54 TUỔI · DIỄN Ý TỪ SÁCH 2017", "subAt": 6},
    {"type": "ledger", "at": 7, "title": "THEO CÁC BÀI ĐIỂM SÁCH", "srcnote": "MIT TECHNOLOGY REVIEW · WALL STREET JOURNAL, 2017",
     "rows": [{"k": "THỪA NHẬN", "v": "LÀ NGƯỜI THUA KHÔNG MẤY ĐẸP", "at": 7}, {"k": "XIN LỖI", "v": "VÌ NHỮNG GÌ LÀM SAU TRẬN", "at": 8}]},
    {"type": "myth", "at": 9, "mythLab": "NHƯNG ÔNG KHÔNG NÓI", "myth": "THUA MỘT TRÍ TUỆ CAO SIÊU", "truthLab": "ÔNG VẪN CHO RẰNG IBM MUỐN", "truth": "MỘT CHIẾN THẮNG ĐỂ QUẢNG BÁ", "strikeAt": [11, "Và"], "truthAt": [10, "điều"]},
]}

CH["ch15"] = {"hud": {"k": "CHƯƠNG 15", "t": "ĐỐI THỦ TIẾP THEO"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "15", "k": "CHƯƠNG MƯỜI LĂM", "title": "ĐỐI THỦ\nTIẾP THEO", "sub": "IBM CẦN MỘT THỬ THÁCH KHÓ HƠN", "vid": "5028622", "ms": 18, "illus": VM, "titleAt": [0, "Còn"]},
    {"type": "myth", "at": 3, "mythLab": "CỜ VUA", "myth": "LUẬT RÕ RÀNG · 64 Ô", "truthLab": "NGÔN NGỮ CON NGƯỜI", "truth": "ĐỐ MẸO · CHƠI CHỮ · VÒNG VO", "strikeAt": [4, "Còn"], "truthAt": [5, "Một"]},
    {"type": "ledger", "at": 6, "title": "02.2011 · 14 NĂM SAU", "rows": [{"k": "CỖ MÁY MỚI", "v": "WATSON", "at": 7}, {"k": "ĐỐI THỦ", "v": "HAI NGƯỜI GIỎI NHẤT", "at": 8}]},
    {"type": "slam", "at": 9, "text": "WATSON THẮNG", "sub": "CÂU CHUYỆN CỦA MỘT VIDEO KHÁC TRONG CHUỖI", "subAt": 10},
]}

CH["ch16"] = {"hud": {"k": "CHƯƠNG 16", "t": "MỘT CÁCH NGHĨ KHÁC"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "16", "k": "CHƯƠNG MƯỜI SÁU", "title": "HAI MƯƠI NĂM SAU,\nMỘT CÁCH NGHĨ KHÁC", "sub": "ALPHAZERO · 12.2017", "vid": "6599643", "ms": 8, "illus": VM, "titleAt": [0, "Tháng"]},
    {"type": "ledger", "at": 1, "title": "ALPHAZERO KHÔNG CÓ", "rows": [{"k": "1", "v": "KHO KHAI CUỘC DO NGƯỜI SOẠN", "at": 2}, {"k": "2", "v": "CÁCH CHẤM ĐIỂM DO NGƯỜI VIẾT", "at": 3}],
     "total": {"k": "CHỈ CÓ", "v": "LUẬT CHƠI · RỒI TỰ CHƠI", "at": 4}},
    {"type": "bars", "at": 6, "title": "100 VÁN VỚI PHẦN MỀM MẠNH NHẤT", "unit": "SAU KHOẢNG 4 GIỜ TỰ HỌC · THEO DEEPMIND",
     "items": [{"k": "THẮNG", "v": 28, "lbl": "28", "at": [7, "hai"], "acc": True}, {"k": "HOÀ", "v": 72, "lbl": "72", "at": [7, "hoà"]}, {"k": "THUA", "v": 0.5, "lbl": "0", "at": [7, "không"]}]},
    {"type": "bars", "at": 8, "title": "THẾ CỜ XEM MỖI GIÂY", "unit": "THEO TƯ LIỆU VỀ HAI CỖ MÁY",
     "items": [{"k": "DEEP BLUE · 1997", "v": 200000, "lbl": "~200 TRIỆU", "at": [9, None, 0, 0.05]}, {"k": "ALPHAZERO · 2017", "v": 80, "lbl": "~80 NGHÌN", "at": [9, "tám"], "acc": True}]},
    {"type": "myth", "at": 11, "mythLab": "DEEP BLUE THẮNG NHỜ", "myth": "NHÌN RẤT RỘNG", "truthLab": "ALPHAZERO THẮNG NHỜ", "truth": "BIẾT NHÌN VÀO ĐÂU", "strikeAt": [12, "AlphaZero"], "truthAt": [12, "biết"]},
    {"type": "kinetic", "at": 14, "items": [{"text": "KHÔNG PHẢI ĐƯỢC DẠY NHƯ NGƯỜI", "at": 16, "sm": True}, {"text": "MÀ TỰ TÌM RA", "at": 17, "acc": True}]},
    {"type": "question", "at": 19, "text": "Còn con người thì sao?"},
]}

CH["ch17"] = {"hud": {"k": "CHƯƠNG 17", "t": "HAI TRĂM TRIỆU THẾ CỜ MỖI GIÂY"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "17", "k": "PHẦN CUỐI", "title": "HAI TRĂM TRIỆU\nTHẾ CỜ MỖI GIÂY", "sub": "BA CÂU NÓI CẠNH NHAU", "vid": "12197806", "ms": 8, "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "timeline", "at": 1, "items": [{"year": "26 TUỔI · 1989", "text": "“tôi phải bảo vệ loài người”", "at": 1}, {"year": "34 TUỔI · 1997", "text": "chắc chắn đã có người giúp cỗ máy · diễn ý", "at": 2},
                                           {"year": "54 TUỔI · 2017", "text": "không, nó không gian lận · diễn ý", "at": 3}]},
    {"type": "ledger", "at": 4, "title": "MỘT HÀNH TRÌNH", "rows": [{"k": "1", "v": "COI MÁY LÀ KẺ THÙ", "at": [4, "coi"]}, {"k": "2", "v": "NGHI NGỜ NÓ", "at": [4, "nghi"]}, {"k": "3", "v": "CHẤP NHẬN NÓ", "at": [4, "chấp"]}],
     "total": {"k": "CÓ LẼ CŨNG LÀ", "v": "HÀNH TRÌNH CỦA TA", "at": 5}},
    {"type": "broll", "at": 6, "vid": "8427421", "ms": 2, "veil": 0.55, "illus": VM,
     "kin": [{"text": "ỨNG DỤNG CỜ MIỄN PHÍ > MỌI NHÀ VÔ ĐỊCH", "at": 6, "acc": True}, {"text": "nhưng cờ vua không chết", "at": 8, "sm": True}]},
    {"type": "myth", "at": 9, "mythLab": "CỖ MÁY TỪNG LÀ", "myth": "ĐỐI THỦ", "truthLab": "GIỜ LÀ", "truth": "NGƯỜI THẦY KIÊN NHẪN NHẤT", "strikeAt": [11, "Cỗ"], "truthAt": [11, "người"]},
    {"type": "ledger", "at": 12, "title": "CÂU HỎI ĐÃ ĐỔI", "rows": [{"k": "KHÔNG CÒN LÀ", "v": "AI GIỎI HƠN AI", "at": 14}], "total": {"k": "MÀ LÀ", "v": "LÀM VIỆC CÙNG NHAU THẾ NÀO", "at": 15}},
    {"type": "question", "at": 16, "text": "Bạn đứng ở câu nói nào\ntrong ba câu nói ấy?"},
]}

SPEC = {
    "title": "Deep Blue Đấu Kasparov: Mười Chín Nước Cờ Khiến Nhà Vô Địch Thế Giới Bỏ Đi",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["deep", "blue", "kasparov", "máy", "thua", "thắng", "nước", "câu"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(18)],
    "youtube": {
        "titles": ["Deep Blue Đấu Kasparov: Mười Chín Nước Cờ Khiến Nhà Vô Địch Thế Giới Bỏ Đi",
                   "Ngày Máy Tính Thắng Nhà Vô Địch Cờ Vua: Câu Chuyện Thật Của Deep Blue, 1997",
                   "Kasparov Thua Máy: Một Con Bọ, Một Lời Buộc Tội, Và Hai Mươi Năm Để Nói “Không”"],
        "summary": "Ngày 11/5/1997, sau 19 nước cờ, nhà vô địch thế giới Garry Kasparov xin thua cỗ máy Deep Blue của IBM: lần đầu một máy tính thắng "
                   "nhà vô địch cờ vua trong trận đấu thể thức chuẩn. Video kể lại câu chuyện qua ba câu nói của Kasparov: năm 1989 “phải bảo vệ loài "
                   "người”, năm 1997 một lời buộc tội, và năm 2017 câu trả lời “không”. Kèm con bọ phần mềm ở ván một, ván hai có thể hoà, nước thí mã ở "
                   "ván sáu, và chuyện “nhân mã”: người cùng máy chơi chung một phe.",
        "more": ["Bàn cờ ghi \"THẾ CỜ THẬT\" là thế cờ ván 6 (11/5/1997) do kênh dựng lại từng nước từ biên bản: 1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4 Nd7 "
                 "5.Ng5 Ngf6 6.Bd3 e6 7.N1f3 h6 8.Nxe6. Video làm nền không phải hình ảnh trận đấu. Chuyện “con bọ” ở nước 44 ván 1 là theo lời một thành "
                 "viên đội Deep Blue, kể trong cuốn sách “The Signal and the Noise” (Nate Silver, 2012). Câu “Không” ở chương 13 là diễn ý theo các bài "
                 "điểm sách “Deep Thinking” (Kasparov, 2017); lời trích được dịch và đọc bằng giọng máy."],
        "chapter_titles": {"ch00": "Mở đầu: mười chín nước", "ch01": "Một giấc mơ cũ: Shannon, Turing và lời cược của Levy", "ch02": "Ba mươi hai chiếc máy (Hamburg 1985)",
                           "ch03": "Câu nói thứ nhất: Deep Thought, 1989", "ch04": "Philadelphia 1996: ván đầu tiên", "ch05": "Cỗ máy thứ hai: 200 triệu thế cờ mỗi giây",
                           "ch06": "Ván một: một nước cờ lạ", "ch07": "Ván hai: lời buộc tội", "ch08": "Ba ván hoà", "ch09": "Ván sáu: nước thí mã",
                           "ch10": "Sau trận", "ch11": "Máy có “nghĩ” không?", "ch12": "Một trò chơi đã có lời giải: cờ đam", "ch13": "Con nhân mã: người và máy cùng một phe", "ch14": "Câu nói thứ ba",
                           "ch15": "Đối thủ tiếp theo: Watson", "ch16": "AlphaZero: một cách nghĩ khác", "ch17": "Hai trăm triệu thế cờ mỗi giây"},
        "sources": ["https://en.wikipedia.org/wiki/Deep_Blue_(chess_computer)", "https://en.wikipedia.org/wiki/Deep_Blue_versus_Garry_Kasparov",
                    "https://en.wikipedia.org/wiki/Deep_Blue_versus_Kasparov,_1996,_Game_1", "https://en.wikipedia.org/wiki/Deep_Blue_versus_Kasparov,_1997,_Game_6",
                    "https://www.computerhistory.org/chess/levys-bet/", "https://chessprogramming.org/Kasparov_Simul_vs_32_Micros_Hamburg_1985",
                    "https://vault.si.com/vault/1989/10/30/its-mind-over-matter-2-0-gary-kasparov-crushed-a-computer-for-all-of-humanity",
                    "https://en.chessbase.com/post/dark-horse-zacks-wins-freestyle-che-tournament/8",
                    "https://www.technologyreview.com/2017/07/10/150540/kasparov-thinks-deeply-about-his-battle-with-a-machine/",
                    "https://historyofinformation.com/detail.php?entryid=94"],
        "hashtags": ["DeepBlue", "Kasparov", "CờVua", "TríTuệNhânTạo", "MindInTheMachine"],
        "tags": ["deep blue", "kasparov", "deep blue vs kasparov", "máy tính thắng cờ vua", "ibm deep blue", "cờ vua", "lịch sử ai", "người đấu với máy",
                 "trí tuệ nhân tạo", "advanced chess", "nhân mã"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        for sc in c["scenes"]:              # quote: "who" + "note" -> "by"; "qline" = dòng lời trích (dòng "at" hoặc dòng ngay sau)
            if sc["type"] == "quote" and "who" in sc:
                k = sc["at"]
                is_q = lambda i: isinstance(d["lines"][i], dict) and d["lines"][i].get("q")
                sc["qline"] = k if is_q(k) else k + 1
                assert is_q(sc["qline"]), (name, k)
                sc["by"] = f'{sc.pop("who")} · {sc.pop("note")}'
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")


if __name__ == "__main__":
    main()
