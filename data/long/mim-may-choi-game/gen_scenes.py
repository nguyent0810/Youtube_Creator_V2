"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM "Máy thắng game thời gian thực: AlphaStar, OpenAI Five"
(chuỗi Trận đấu Người – Máy, loại 20-30 phút).

    python data/long/mim-may-choi-game/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Lộ trình "năm điều cờ vua không có": cảnh units 5 ô sáng dần (five()).
Clip: Pexels (ngang), gắn "VIDEO MINH HỌA · KHÔNG PHẢI HÌNH ẢNH TRẬN ĐẤU"; không chiếu hình trò chơi (bản quyền), không logo.
Luật 15/10: "≈" thay "~" trước số; counter có prefix đứng yên; không counter năm.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"=AI": "ây ai", "deepmind": "Đíp-mai", "=DeepMind": "Đíp-mai", "openai": "Ô-pần Ây Ai", "=OpenAI": "Ô-pần Ây Ai", "starcraft": "Xta-cráp",
       "=StarCraft": "Xta-cráp", "alphastar": "An-pha Xta", "=AlphaStar": "An-pha Xta", "alphago": "An-pha Gô", "=AlphaGo": "An-pha Gô", "dota": "Đô-ta",
       "=TLO": "Ti E-lờ Ô", "mana": "Ma-na", "=MaNa": "Ma-na", "protoss": "Prô-tót", "zerg": "Dớc", "grandmaster": "Gran-mát-tơ", "five": "Phai",
       "dendi": "Đen-đi", "the": "Đờ", "international": "In-tơ-ne-sần", "pain": "Pên", "=paiN": "Pên", "gaming": "Ghê-minh", "=OG": "Ô Gi",
       "san": "Xan", "francisco": "Phran-xít-cô", "atari": "A-ta-ri", "=DQN": "Đi Kiu En", "nature": "Nê-chơ", "league": "Li", "lee": "Li",
       "sedol": "Xê-đôn", "deep": "Đíp", "blue": "Blu", "wikipedia": "Uy-ki-pê-đi-a", "google": "Gu-gồ", "ukraine": "U-crai-na", "brazil": "Bra-xin"}
VM = "VIDEO MINH HỌA · KHÔNG PHẢI HÌNH ẢNH TRẬN ĐẤU"
GAMER, GAMER2, TOURN, ARCADE, SERVER, CABLES, FOG, FOG2, TEAM, CHESS, DIGI, KEYS, KEYS2 = (
    "9071216", "7849218", "7914772", "7986592", "5028622", "1085656", "4296589", "8233026", "7551536", "6599643", "854323", "7849220", "7047256")


def five(at, lit, lit_at, title="NĂM ĐIỀU CỜ VUA KHÔNG CÓ"):
    return {"type": "units", "at": at, "title": title, "total": 5, "cols": 5, "lit": lit, "litAt": lit_at, "unitLabel": "ĐÃ VƯỢT QUA"}


def bro(at, vid, kin, ms=0):
    d = {"type": "broll", "at": at, "vid": vid, "veil": 0.55, "illus": VM, "kin": kin}
    if ms:
        d["ms"] = ms
    return d


def chap(no, k, title, sub, vid, at0, ms=0):
    d = {"type": "chapter", "no": str(no), "k": k, "title": title, "sub": sub, "vid": vid, "illus": VM, "titleAt": at0}
    if ms:
        d["ms"] = ms
    return d


CH = {}
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MƯỜI MỘT VÁN"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": GAMER, "veil": 0.55, "illus": VM,
     "kin": [{"text": "11 VÁN · 1 CỖ MÁY · 2 TUYỂN THỦ", "at": [0, None, 0, 0.05], "acc": True}, {"text": "cỗ máy thắng mười ván", "at": 1, "sm": True}]},
    {"type": "ledger", "at": 2, "title": "STARCRAFT II · DEEPMIND · 01/2019", "rows": [{"k": "KHÔNG PHẢI", "v": "CỜ VUA · CỜ VÂY", "at": 3},
                                                                               {"k": "MÀ LÀ", "v": "CHIẾN THUẬT THỜI GIAN THỰC", "at": 4}]},
    {"type": "ledger", "at": 5, "title": "ALPHASTAR", "rows": [{"k": "VỚI TLO", "v": "5 – 0", "at": 6}, {"k": "VỚI MANA", "v": "5 – 0", "at": 7}]},
    {"type": "slam", "at": 8, "text": "VÁN THỨ MƯỜI MỘT", "sub": "VÁN BIỂU DIỄN · CON NGƯỜI THẮNG", "subAt": 9},
    {"type": "timeline", "at": 11, "items": [{"year": "1997", "text": "cờ vua", "at": [11, None, 0, 0.05]}, {"year": "2011", "text": "đố vui", "at": [11, None, 0, 0.35]},
                                            {"year": "2016", "text": "cờ vây", "at": [11, None, 0, 0.55]}, {"year": "2017", "text": "poker", "at": [11, None, 0, 0.8]}]},
    five(12, 5, [13, "năm"], "NĂM ĐIỀU BÀN CỜ KHÔNG CÓ"),
    {"type": "kinetic", "at": 14, "items": [{"text": "MỖI ĐIỀU", "at": 14, "sm": True}, {"text": "MỘT LÝ DO MÁY CÒN LÂU MỚI THẮNG", "at": [14, None, 0, 0.3], "acc": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "SAU NHỮNG BÀN CỜ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap(1, "CHƯƠNG MỘT", "SAU NHỮNG BÀN CỜ", "THẾ GIỚI GỌN GÀNG CỦA CỜ", CHESS, [0, None, 0, 0.05]),
    {"type": "ledger", "at": 1, "title": "MÁY ĐÃ THẮNG", "rows": [{"k": "1997", "v": "DEEP BLUE · CỜ VUA", "at": [1, None, 0, 0.05]}, {"k": "2016", "v": "ALPHAGO · CỜ VÂY", "at": 1}]},
    {"type": "ledger", "at": 3, "title": "BÀN CỜ LÀ THẾ GIỚI GỌN GÀNG", "rows": [{"k": "1", "v": "HAI NGƯỜI", "at": [4, None, 0, 0.05]}, {"k": "2", "v": "ĐI LẦN LƯỢT", "at": [4, None, 0, 0.3]},
                                                                             {"k": "3", "v": "MỌI QUÂN NẰM TRÊN BÀN", "at": [4, None, 0, 0.6]}]},
    bro(5, FOG, [{"text": "THẾ GIỚI THẬT KHÔNG CHỜ BẠN", "at": 6, "acc": True}, {"text": "không thấy hết · không một mình", "at": 7, "sm": True}]),
    {"type": "kinetic", "at": 9, "items": [{"text": "MỘT SÂN CHƠI MỚI", "at": 9, "sm": True}, {"text": "GẦN ĐỜI THẬT HƠN CỜ VUA", "at": [9, None, 0, 0.4], "acc": True},
                                          {"text": "nhưng luật rõ ràng · kết quả đo được", "at": [9, None, 0, 0.7], "sm": True}]},
    {"type": "ledger", "at": 11, "title": "HAI PHÒNG THÍ NGHIỆM · HAI TRÒ CHƠI", "rows": [{"k": "DEEPMIND", "v": "STARCRAFT II", "at": 13}, {"k": "OPENAI", "v": "DOTA 2", "at": [13, None, 0, 0.5]}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "MỘT PHÒNG THÍ NGHIỆM AN TOÀN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap(2, "CHƯƠNG HAI", "MỘT PHÒNG THÍ NGHIỆM\nAN TOÀN", "VÌ SAO LẠI LÀ TRÒ CHƠI?", SERVER, [0, None, 0, 0.05]),
    {"type": "ledger", "at": 2, "title": "BA ĐIỀU TRÒ CHƠI CÓ", "rows": [{"k": "1", "v": "KẾT QUẢ RÕ RÀNG", "at": 3}, {"k": "2", "v": "CHƠI LẠI VÔ SỐ LẦN", "at": 4},
                                                                     {"k": "3", "v": "SAI KHÔNG LÀM AI BỊ THƯƠNG", "at": 5}]},
    {"type": "myth", "at": 6, "mythLab": "XE TỰ LÁI", "myth": "TỰ THỬ, TỰ SAI NGOÀI ĐƯỜNG", "truthLab": "TRONG TRÒ CHƠI", "truth": "SAI HÀNG TỶ LẦN", "strikeAt": 7, "truthAt": 8},
    {"type": "kinetic", "at": 9, "items": [{"text": "MÀ VẪN ĐỦ KHÓ", "at": 9, "sm": True}, {"text": "THÔNG TIN BỊ CHE · ĐỐI THỦ BIẾT NGHĨ", "at": 10, "acc": True},
                                          {"text": "đủ khó để đáng thử · đủ an toàn để được sai", "at": 11, "sm": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "TỪ NHỮNG TRÒ CHƠI CŨ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(3, "CHƯƠNG BA", "TỪ NHỮNG TRÒ CHƠI\nĐIỆN TỬ CŨ", "DQN · 2015", ARCADE, [0, None, 0, 0.05]),
    {"type": "source", "at": 2, "source": "NATURE · 02/2015 · DEEPMIND", "ref": "DQN · 49 TRÒ CHƠI ATARI",
     "snippet": "đầu vào chỉ gồm [[hình ảnh màn hình, các nút bấm và điểm số]]", "hlAt": 5, "seal": "KHÔNG ĐƯỢC DẠY LUẬT", "sealAt": 4},
    {"type": "bars", "at": 7, "title": "DQN SO VỚI CÁC PHƯƠNG PHÁP TRƯỚC (SỐ TRÒ)", "unit": "DEEPMIND · 02/2015",
     "items": [{"k": "GIỎI HƠN", "v": 43, "lbl": "43", "at": [7, None, 0, 0.3], "acc": True}, {"k": "TỔNG SỐ TRÒ", "v": 49, "lbl": "49", "at": [7, None, 0, 0.6]}]},
    {"type": "counter", "at": 8, "from": 75, "to": 75, "prefix": "> ", "suffix": "%", "label": "ĐIỂM NGƯỜI THỬ GAME CHUYÊN NGHIỆP", "sub": {"text": "Ở HƠN MỘT NỬA SỐ TRÒ", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "MỘT THUẬT TOÁN CHO MỌI TRÒ", "at": 9, "acc": True}, {"text": "nhưng chỉ vài phút · không đối thủ biết nghĩ", "at": 11, "sm": True},
                                          {"text": "tới StarCraft: một bước nhảy rất xa", "at": 12, "sm": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "NĂM ĐIỀU CỜ VUA KHÔNG CÓ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(4, "CHƯƠNG BỐN", "NĂM ĐIỀU\nCỜ VUA KHÔNG CÓ", "ĐẾM TỪNG ĐIỀU MỘT", CHESS, [0, None, 0, 0.05], ms=8),
    bro(2, FOG2, [{"text": "1 · SƯƠNG MÙ", "at": 2, "acc": True}, {"text": "chỉ thấy nơi quân mình đứng", "at": 4, "sm": True}]),
    {"type": "myth", "at": 5, "mythLab": "CỜ VUA", "myth": "NGHĨ XONG MỚI ĐI", "truthLab": "2 · KHÔNG CÓ LƯỢT", "truth": "ĐỒNG HỒ CỨ CHẠY", "strikeAt": 6, "truthAt": 7},
    {"type": "ledger", "at": 8, "title": "3 · VÁN ĐẤU RẤT DÀI", "srcnote": "STARCRAFT: THEO DEEPMIND 01/2019", "rows": [{"k": "CỜ VUA", "v": "VÀI CHỤC NƯỚC", "at": 9},
                                                                                                           {"k": "STARCRAFT", "v": "TỚI 1 GIỜ · HÀNG CHỤC NGHÌN", "at": 10}]},
    {"type": "ledger", "at": 11, "title": "CÒN HAI ĐIỀU", "rows": [{"k": "4", "v": "LỰA CHỌN KHỔNG LỒ MỖI KHOẢNH KHẮC", "at": 11}, {"k": "5", "v": "ĐỒNG ĐỘI", "at": 12}]},
    five(13, 0, 13),
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "STARCRAFT LÀ GÌ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(5, "CHƯƠNG NĂM", "STARCRAFT LÀ GÌ", "PHIÊN BẢN NGẮN NHẤT", GAMER2, [0, None, 0, 0.05]),
    {"type": "timeline", "at": 2, "items": [{"year": "THỢ", "text": "khai thác tài nguyên", "at": 2}, {"year": "TÀI NGUYÊN", "text": "xây nhà · công nghệ · quân", "at": 3},
                                           {"year": "QUÂN", "text": "do thám · phòng thủ · tấn công", "at": 4}]},
    {"type": "ledger", "at": 5, "title": "BA CHỦNG TỘC", "rows": [{"k": "MỖI CHỦNG TỘC", "v": "MỘT KIỂU CHƠI KHÁC HẲN", "at": 5}, {"k": "MỖI CHIẾN THUẬT", "v": "CÓ CÁCH KHẮC CHẾ", "at": 7}]},
    bro(8, GAMER, [{"text": "CÙNG LÚC", "at": 8, "sm": True}, {"text": "KINH TẾ · TIỀN TUYẾN · ĐOÁN Ý ĐỐI THỦ", "at": 9, "acc": True},
                   {"text": "trong lúc đồng hồ vẫn chạy", "at": 10, "sm": True}], ms=2),
    {"type": "slam", "at": 11, "text": "THỬ THÁCH SAU CỜ VÂY", "sub": "MỘT TRONG NHỮNG MÔN THỂ THAO ĐIỆN TỬ KHÓ NHẤT", "subAt": 11},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "MƯỜI MŨ HAI MƯƠI SÁU"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    chap(6, "CHƯƠNG SÁU", "MỘT CON SỐ CÓ\nHAI MƯƠI SÁU SỐ KHÔNG", "ĐIỀU THỨ TƯ", CABLES, [0, None, 0, 0.05]),
    {"type": "bars", "at": 1, "title": "SỐ CHỮ SỐ · LỰA CHỌN MỖI BƯỚC", "unit": "THEO DEEPMIND 01/2019",
     "items": [{"k": "CỜ VUA", "v": 2, "lbl": "VÀI CHỤC", "at": 1}, {"k": "STARCRAFT", "v": 27, "lbl": "≈ 10^26", "at": 2, "acc": True}]},
    {"type": "ledger", "at": 4, "title": "VÌ SAO NHIỀU ĐẾN THẾ", "rows": [{"k": "CHỌN", "v": "ĐƠN VỊ NÀO", "at": [5, None, 0, 0.3]}, {"k": "CHO NÓ", "v": "LÀM GÌ", "at": [5, None, 0, 0.5]},
                                                                      {"k": "Ở", "v": "VỊ TRÍ NÀO", "at": [5, None, 0, 0.75]}], "total": {"k": "NHÂN LẠI", "v": "PHÌNH RẤT NHANH", "at": 6}},
    {"type": "myth", "at": 8, "mythLab": "DEEP BLUE · ALPHAGO", "myth": "DUYỆT HẾT · NHÌN TRƯỚC", "truthLab": "STARCRAFT", "truth": "KHÔNG THỂ", "strikeAt": 8, "truthAt": 9},
    {"type": "question", "at": 10, "text": "Vậy cỗ máy\nbắt đầu học từ đâu?"},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "HỌC TỪ CON NGƯỜI TRƯỚC"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap(7, "CHƯƠNG BẢY", "HỌC TỪ\nCON NGƯỜI TRƯỚC", "XEM NGƯỜI KHÁC CHƠI", GAMER2, [0, None, 0, 0.05], ms=6),
    {"type": "ledger", "at": 2, "title": "BƯỚC MỘT · BẮT CHƯỚC", "rows": [{"k": "DỮ LIỆU", "v": "VÁN ĐẤU NGƯỜI THẬT · ẨN DANH", "at": 2}, {"k": "HỌC", "v": "NGƯỜI THƯỜNG LÀM GÌ", "at": 3}]},
    {"type": "counter", "at": 4, "from": 95, "to": 95, "suffix": "%", "label": "THẮNG AI DỰNG SẴN · MỨC KHÓ NHẤT", "sub": {"text": "≈ NGƯỜI CHƠI HẠNG VÀNG · DEEPMIND", "at": 5}},
    {"type": "kinetic", "at": 6, "items": [{"text": "KHÁ · NHƯNG CÒN XA CHUYÊN NGHIỆP", "at": 6, "sm": True}, {"text": "BẮT CHƯỚC CHỈ ĐƯA TỚI NGANG NGƯỜI ĐÃ XEM", "at": 7, "acc": True}]},
    {"type": "slam", "at": 10, "text": "TỰ CHƠI VỚI CHÍNH MÌNH", "sub": "NHƯNG LẦN NÀY · CẢ MỘT GIẢI ĐẤU", "subAt": 11},
]}

CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "GIẢI ĐẤU CỦA NHỮNG CỖ MÁY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(8, "CHƯƠNG TÁM", "GIẢI ĐẤU CỦA\nNHỮNG CỖ MÁY", "ALPHASTAR LEAGUE", SERVER, [0, None, 0, 0.05], ms=10),
    {"type": "myth", "at": 1, "mythLab": "KHÔNG PHẢI", "myth": "MỘT CỖ MÁY ĐẤU BẢN SAO", "truthLab": "MÀ LÀ", "truth": "RẤT NHIỀU PHIÊN BẢN", "strikeAt": [1, None, 0, 0.4], "truthAt": [1, None, 0, 0.7]},
    {"type": "kinetic", "at": 3, "items": [{"text": "MỖI CHIẾN THUẬT ĐỀU CÓ CÁCH KHẮC CHẾ", "at": 3, "sm": True}, {"text": "TỰ CHƠI MỘT MÌNH DỄ KẸT VÒNG LẶP", "at": 4, "acc": True}]},
    {"type": "ledger", "at": 5, "title": "TRONG GIẢI ĐẤU", "rows": [{"k": "CÓ PHIÊN BẢN", "v": "CHUYÊN TÌM ĐIỂM YẾU", "at": 5}, {"k": "CÓ PHIÊN BẢN", "v": "THÍCH TẤN CÔNG SỚM", "at": 6},
                                                               {"k": "CÓ PHIÊN BẢN", "v": "PHÒNG THỦ · KINH TẾ", "at": [6, None, 0, 0.6]}]},
    {"type": "ledger", "at": 8, "title": "ALPHASTAR LEAGUE · 2018", "srcnote": "DEEPMIND · 01/2019", "rows": [{"k": "THỜI GIAN", "v": "14 NGÀY", "at": 8}, {"k": "MỖI PHIÊN BẢN", "v": "16 BỘ XỬ LÝ TPU", "at": 9}]},
    {"type": "counter", "at": 10, "from": 200, "to": 200, "prefix": "TỚI ", "suffix": " NĂM", "label": "CHƠI STARCRAFT · MỖI PHIÊN BẢN", "sub": {"text": "TÍNH THEO THỜI GIAN THẬT · TRONG HAI TUẦN", "at": 11}},
    {"type": "kinetic", "at": 12, "items": [{"text": "KHÔNG TUYỂN THỦ NÀO", "at": 12, "sm": True}, {"text": "LUYỆN NHIỀU ĐẾN THẾ", "at": [12, None, 0, 0.4], "acc": True}]},
]}

CH["ch09"] = {"hud": {"k": "CHƯƠNG 09", "t": "PHẦN THƯỞNG ĐẾN MUỘN"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    chap(9, "CHƯƠNG CHÍN", "PHẦN THƯỞNG\nĐẾN MUỘN", "MỘT KHÓ KHĂN ÍT AI NGHĨ TỚI", CABLES, [0, None, 0, 0.05], ms=10),
    {"type": "myth", "at": 2, "mythLab": "ATARI", "myth": "ĐIỂM TĂNG NGAY", "truthLab": "STARCRAFT", "truth": "BIẾT THẮNG THUA Ở CUỐI VÁN", "strikeAt": 4, "truthAt": 5},
    {"type": "question", "at": 6, "text": "Hành động nào\nđã dẫn tới chiến thắng?"},
    {"type": "ledger", "at": 7, "title": "BÀI TOÁN PHÂN BỔ CÔNG LAO", "rows": [{"k": "VÍ DỤ", "v": "ĐƯỜNG CHUYỀN PHÚT 10", "at": 8}, {"k": "VÀ", "v": "BÀN THẮNG PHÚT 80", "at": [8, None, 0, 0.6]}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "VÌ SAO PHẢI HỌC NGƯỜI TRƯỚC", "at": 9, "sm": True}, {"text": "BẮT CHƯỚC TRƯỚC · TỰ CHƠI SAU", "at": [9, "bắt"], "acc": True},
                                          {"text": "không bắt đầu từ những cú bấm ngẫu nhiên", "at": [10, "thay"], "sm": True}]},
    {"type": "timeline", "at": 11, "items": [{"year": "1", "text": "bắt chước người: điểm xuất phát hợp lý", "at": 11}, {"year": "2", "text": "200 năm giải đấu: tìm điều dẫn tới thắng", "at": [11, "giúp"]}]},
    {"type": "slam", "at": 12, "text": "ĐẾN MUỘN", "sub": "NHƯNG VỚI ĐỦ NHIỀU VÁN · VẪN ĐẾN", "subAt": 12},
]}

CH["ch10"] = {"hud": {"k": "CHƯƠNG 10", "t": "MƯỜI VÁN, MƯỜI TRẬN THẮNG"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    chap(10, "CHƯƠNG MƯỜI", "MƯỜI VÁN,\nMƯỜI TRẬN THẮNG", "12/2018 · GHI HÌNH KÍN", TOURN, [0, None, 0, 0.05]),
    {"type": "ledger", "at": 1, "title": "ĐỐI THỦ 1 · TLO", "rows": [{"k": "CHỦNG TỘC", "v": "PROTOSS ĐẤU PROTOSS", "at": 3}, {"k": "BẢN ĐỒ", "v": "MỘT · CHỌN SẴN", "at": [3, None, 0, 0.6]}],
     "total": {"k": "KẾT QUẢ", "v": "ALPHASTAR 5 – 0", "at": 4}},
    {"type": "ledger", "at": 5, "title": "ĐỐI THỦ 2 · MANA", "srcnote": "SAU THÊM MỘT TUẦN HUẤN LUYỆN", "rows": [{"k": "SỞ TRƯỜNG", "v": "PROTOSS", "at": 6}], "total": {"k": "KẾT QUẢ", "v": "ALPHASTAR 5 – 0", "at": 7}},
    {"type": "slam", "at": 8, "text": "10 / 10", "sub": "DEEPMIND CÔNG BỐ 24/01/2019", "subAt": 9},
    {"type": "myth", "at": 10, "mythLab": "CÂU HỎI KHÔNG PHẢI", "myth": "NÓ CÓ GIỎI KHÔNG", "truthLab": "MÀ LÀ", "truth": "TRÍ ÓC HAY ĐÔI TAY?", "strikeAt": 11, "truthAt": 12},
]}

CH["ch11"] = {"hud": {"k": "CHƯƠNG 11", "t": "ĐÔI TAY CỦA CỖ MÁY"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    chap(11, "CHƯƠNG MƯỜI MỘT", "ĐÔI TAY\nCỦA CỖ MÁY", "SỐ HÀNH ĐỘNG MỖI PHÚT", KEYS, [0, None, 0, 0.05], ms=8),
    {"type": "bars", "at": 2, "title": "HÀNH ĐỘNG MỖI PHÚT · TRUNG BÌNH", "unit": "DEEPMIND · 01/2019 · ALPHASTAR 277",
     "items": [{"k": "ALPHASTAR", "v": 280, "lbl": "≈ 280", "at": 2, "acc": True}, {"k": "MANA", "v": 390, "lbl": "≈ 390", "at": 3}, {"k": "TLO", "v": 678, "lbl": "≈ 678", "at": [3, None, 0, 0.6]}]},
    {"type": "ledger", "at": 5, "title": "DEEPMIND LÀM RÕ THÊM", "rows": [{"k": "SỐ CỦA TLO", "v": "ĐẨY CAO VÌ BẤM PHÍM LIÊN TỤC", "at": 6},
                                                                      {"k": "LÚC GIAO TRANH", "v": "CÓ LÚC NHANH HƠN CẢ HAI", "at": 7}]},
    bro(8, FOG, [{"text": "KHÔNG PHẢI DI CHUYỂN MÀN HÌNH", "at": 9, "acc": True}, {"text": "thấy cùng lúc mọi nơi quân mình đang thấy", "at": 10, "sm": True},
                 {"text": "sương mù vẫn còn", "at": 11, "sm": True}], ms=6),
    {"type": "kinetic", "at": 12, "items": [{"text": "KHÔNG BAO GIỜ PHẢI QUAY ĐẦU", "at": 12, "sm": True}, {"text": "LỢI THẾ · HAY KHÔNG CÔNG BẰNG?", "at": 13, "acc": True},
                                           {"text": "câu trả lời: ván thứ mười một", "at": 15, "sm": True}]},
]}

CH["ch12"] = {"hud": {"k": "CHƯƠNG 12", "t": "BA TRĂM NĂM MƯƠI PHẦN NGHÌN GIÂY"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap(12, "CHƯƠNG MƯỜI HAI", "BA TRĂM NĂM MƯƠI\nPHẦN NGHÌN GIÂY", "TỐC ĐỘ PHẢN ỨNG", DIGI, [0, None, 0, 0.05]),
    {"type": "counter", "at": 2, "from": 350, "to": 350, "prefix": "≈ ", "suffix": " MS", "label": "ĐỘ TRỄ NHÌN → HÀNH ĐỘNG · TRUNG BÌNH", "sub": {"text": "≈ MỘT PHẦN BA GIÂY · DEEPMIND 01/2019", "at": 3}},
    {"type": "question", "at": 5, "text": "Cỗ máy có bao giờ\nmệt, hay phân tâm?"},
    {"type": "myth", "at": 7, "mythLab": "CON NGƯỜI", "myth": "PHÚT 30: CHẬM LẠI", "truthLab": "CỖ MÁY", "truth": "PHÚT 50 NHƯ PHÚT ĐẦU", "strikeAt": 8, "truthAt": 9},
    {"type": "slam", "at": 10, "text": "KHÔNG THỂ NGANG NHAU HOÀN TOÀN", "sub": "CHỈ CÓ GIỚI HẠN ĐƯỢC THOẢ THUẬN TRƯỚC", "subAt": 11},
]}

CH["ch13"] = {"hud": {"k": "CHƯƠNG 13", "t": "VÁN THỨ MƯỜI MỘT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    chap(13, "CHƯƠNG MƯỜI BA", "VÁN THỨ\nMƯỜI MỘT", "VÁN ĐẤU BIỂU DIỄN", TOURN, [0, None, 0, 0.05], ms=2),
    {"type": "ledger", "at": 1, "title": "PHIÊN BẢN MỚI", "rows": [{"k": "TẦM NHÌN", "v": "QUA KHUNG MÀN HÌNH", "at": 1}, {"k": "MUỐN XEM CHỖ KHÁC", "v": "PHẢI DI CHUYỂN", "at": 2},
                                                              {"k": "HUẤN LUYỆN", "v": "7 NGÀY", "at": 3}]},
    {"type": "slam", "at": 5, "text": "MANA THẮNG", "sub": "SAU NĂM VÁN THUA LIÊN TIẾP", "subAt": 6},
    {"type": "counter", "at": 7, "from": 1, "to": 1, "suffix": " / 11", "label": "VÁN CON NGƯỜI THẮNG", "sub": {"text": "KHÔNG ĐỔI TỈ SỐ · NHƯNG ĐỔI CÂU CHUYỆN", "at": 8}},
    five(10, 3, [11, None, 0, 0.3]),
    {"type": "kinetic", "at": 12, "items": [{"text": "CÂU HỎI CÔNG BẰNG VẪN CÒN", "at": 12, "sm": True}, {"text": "TRẢ LỜI THEO CÁCH KHÓ NHẤT", "at": 13, "acc": True}]},
]}

CH["ch14"] = {"hud": {"k": "CHƯƠNG 14", "t": "ĐƯỜNG LÊN GRANDMASTER"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(14, "CHƯƠNG MƯỜI BỐN", "ĐƯỜNG LÊN\nGRANDMASTER", "MƯỜI THÁNG SAU · LUẬT CHẶT HƠN", GAMER2, [0, None, 0, 0.05], ms=8),
    {"type": "ledger", "at": 1, "title": "LUẬT MỚI · DEEPMIND 10/2019", "rows": [{"k": "TẦM NHÌN", "v": "QUA CAMERA NHƯ NGƯỜI", "at": 1}, {"k": "TỐI ĐA", "v": "22 HÀNH ĐỘNG / 5 GIÂY", "at": 2},
                                                                            {"k": "CHỦNG TỘC", "v": "CẢ BA", "at": 4}], "total": {"k": "LÀM CÙNG", "v": "TUYỂN THỦ TLO", "at": 3}},
    bro(5, KEYS2, [{"text": "MÁY CHỦ CHÍNH THỨC · CHƠI ẨN DANH", "at": 5, "acc": True}, {"text": "cùng bản đồ · cùng điều kiện", "at": 6, "sm": True},
                   {"text": "đối thủ không biết mình đấu với máy", "at": 7, "sm": True}], ms=2),
    {"type": "source", "at": 8, "source": "NATURE · 10/2019", "ref": "GRANDMASTER · CẢ BA CHỦNG TỘC", "snippet": "xếp trên [[99,8% người chơi đang có thứ hạng]]",
     "hlAt": 10, "seal": "ĐIỀU KIỆN GẦN VỚI NGƯỜI HƠN", "sealAt": [10, None, 0, 0.6]},
    {"type": "counter", "at": 11, "from": 84, "to": 84, "suffix": "%", "label": "GIỎI HƠN · CHỈ NHỜ BẮT CHƯỚC BAN ĐẦU", "sub": {"text": "PHẦN CÒN LẠI: TỰ HỌC QUA GIẢI ĐẤU", "at": 12}},
    {"type": "kinetic", "at": 13, "items": [{"text": "CHƯA PHẢI VÔ ĐỊCH THẾ GIỚI", "at": 13, "sm": True}, {"text": "NHÓM RẤT NHỎ NGƯỜI GIỎI NHẤT", "at": [13, None, 0, 0.5], "acc": True}]},
]}

CH["ch15"] = {"hud": {"k": "CHƯƠNG 15", "t": "NĂM NGƯỜI MỘT ĐỘI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(15, "CHƯƠNG MƯỜI LĂM", "NĂM NGƯỜI\nMỘT ĐỘI", "OPENAI · DOTA 2", TEAM, [0, None, 0, 0.05]),
    five(1, 4, [1, None, 0, 0.6], "ĐIỀU THỨ NĂM: ĐỒNG ĐỘI"),
    {"type": "ledger", "at": 2, "title": "MỘT VÁN DOTA 2", "rows": [{"k": "HAI ĐỘI", "v": "MỖI ĐỘI NĂM NGƯỜI", "at": 2}, {"k": "MỖI NGƯỜI", "v": "MỘT TƯỚNG · KỸ NĂNG RIÊNG", "at": 3}],
     "total": {"k": "MUỐN THẮNG", "v": "CẢ NĂM PHẢI PHỐI HỢP", "at": 4}},
    {"type": "ledger", "at": 5, "title": "ĐỘ KHÓ · SỐ LIỆU OPENAI", "srcnote": "THEO WIKIPEDIA", "rows": [{"k": "MỘT VÁN", "v": "≈ 80.000 NHỊP", "at": 5},
                                                                                                {"k": "MỖI TƯỚNG", "v": "170.000 HÀNH ĐỘNG KHẢ DĨ", "at": 6}, {"k": "MỖI NHỊP", "v": "≈ 1.000 HỢP LỆ", "at": 7}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "SƯƠNG MÙ · KHÔNG LƯỢT · VÁN DÀI", "at": 8, "sm": True}, {"text": "+ NĂM CỖ MÁY CHƠI NHƯ MỘT ĐỘI", "at": 9, "acc": True},
                                          {"text": "không ai ra lệnh cho ai", "at": 10, "sm": True}]},
    {"type": "slam", "at": 11, "text": "OPENAI FIVE", "sub": "NĂM CỦA OPENAI", "subAt": 11},
]}

CH["ch16"] = {"hud": {"k": "CHƯƠNG 16", "t": "MỘT CHỌI MỘT"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(16, "CHƯƠNG MƯỜI SÁU", "MỘT CHỌI MỘT", "THE INTERNATIONAL · 08/2017", TOURN, [0, None, 0, 0.05], ms=3),
    {"type": "ledger", "at": 1, "title": "08/2017 · THE INTERNATIONAL", "rows": [{"k": "CỖ MÁY", "v": "CHỈ CHƠI MỘT CHỌI MỘT", "at": 2}, {"k": "ĐỐI THỦ", "v": "DENDI · UKRAINE", "at": 3}],
     "total": {"k": "KẾT QUẢ", "v": "CỖ MÁY THẮNG", "at": 4}},
    {"type": "counter", "at": 5, "from": 2, "to": 2, "prefix": "≈ ", "suffix": " TUẦN", "label": "TỰ CHƠI VỚI CHÍNH MÌNH · THỜI GIAN THẬT", "sub": {"text": "THEO WIKIPEDIA", "at": 5}},
    {"type": "myth", "at": 6, "mythLab": "MỘT CHỌI MỘT", "myth": "ĐƠN GIẢN HƠN NHIỀU", "truthLab": "NHƯNG", "truth": "HƯỚNG ĐI ĐÚNG", "strikeAt": 7, "truthAt": 8},
    {"type": "question", "at": 9, "text": "Năm cỗ máy có học được\ncách phối hợp?"},
]}

CH["ch17"] = {"hud": {"k": "CHƯƠNG 17", "t": "MỘT TRĂM TÁM MƯƠI NĂM MỖI NGÀY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(17, "CHƯƠNG MƯỜI BẢY", "MỘT TRĂM TÁM MƯƠI\nNĂM MỖI NGÀY", "QUY MÔ", SERVER, [0, None, 0, 0.05], ms=18),
    {"type": "ledger", "at": 2, "title": "OPENAI FIVE · 2018", "srcnote": "THEO WIKIPEDIA", "rows": [{"k": "BỘ XỬ LÝ ĐỒ HOẠ", "v": "256", "at": [2, None, 0, 0.5]},
                                                                                               {"k": "LÕI XỬ LÝ", "v": "128.000", "at": [2, None, 0, 0.8]}]},
    {"type": "counter", "at": 3, "from": 180, "to": 180, "prefix": "≈ ", "suffix": " NĂM", "label": "CHƠI DOTA · MỖI NGÀY", "sub": {"text": "MỖI TƯỚNG: MỘT MẠNG NƠ-RON CÓ BỘ NHỚ", "at": 5}},
    {"type": "question", "at": 6, "text": "Còn chuyện phối hợp?"},
    {"type": "ledger", "at": 7, "title": "KHÔNG AI DẠY CHIA VIỆC", "rows": [{"k": "THƯỞNG", "v": "KHI CẢ ĐỘI THẮNG", "at": 8}, {"k": "DẦN HỌC", "v": "HY SINH CHO ĐỒNG ĐỘI", "at": [8, None, 0, 0.6]}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "MÙA HÈ 2018", "at": 9, "sm": True}, {"text": "GIẢI ĐẤU LỚN NHẤT · ĐỐI THỦ MẠNH NHẤT", "at": 10, "acc": True}]},
]}

CH["ch18"] = {"hud": {"k": "CHƯƠNG 18", "t": "THẤT BẠI Ở THE INTERNATIONAL"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    chap(18, "CHƯƠNG MƯỜI TÁM", "THẤT BẠI Ở\nTHE INTERNATIONAL", "08/2018", TOURN, [0, None, 0, 0.05], ms=1),
    {"type": "ledger", "at": 1, "title": "HAI TRẬN · 08/2018", "srcnote": "THEO WIKIPEDIA", "rows": [{"k": "1", "v": "PAIN GAMING · BRAZIL", "at": 1}, {"k": "2", "v": "CỰU TUYỂN THỦ TRUNG QUỐC", "at": 2}],
     "total": {"k": "KẾT QUẢ", "v": "ĐỘI MÁY THUA CẢ HAI", "at": 3}},
    {"type": "myth", "at": 4, "mythLab": "NHIỀU NGƯỜI NÓI", "myth": "CHỈ GIỎI PHẢN XẠ", "truthLab": "OPENAI", "truth": "TIẾP TỤC HUẤN LUYỆN", "strikeAt": 5, "truthAt": 6},
    {"type": "ledger", "at": 7, "title": "ĐIỂM CHUNG", "rows": [{"k": "ALPHASTAR", "v": "THUA VÁN THỨ 11", "at": [8, None, 0, 0.05]}, {"k": "OPENAI FIVE", "v": "THUA Ở THE INTERNATIONAL", "at": [8, None, 0, 0.5]}],
     "total": {"k": "CẢ HAI", "v": "QUAY LẠI MẠNH HƠN", "at": 9}},
]}

CH["ch19"] = {"hud": {"k": "CHƯƠNG 19", "t": "OG · 04/2019"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    chap(19, "CHƯƠNG MƯỜI CHÍN", "OG,\nTHÁNG TƯ 2019", "SAN FRANCISCO", TEAM, [0, None, 0, 0.05], ms=6),
    {"type": "ledger", "at": 1, "title": "13/04/2019 · SAN FRANCISCO", "rows": [{"k": "ĐỐI THỦ", "v": "OG · VÔ ĐỊCH TI 2018", "at": 1}, {"k": "THỂ THỨC", "v": "BA VÁN THẮNG HAI", "at": 2}]},
    {"type": "slam", "at": 3, "text": "2 – 0", "sub": "LẦN ĐẦU AI THẮNG NHÀ VÔ ĐỊCH THẾ GIỚI THỂ THAO ĐIỆN TỬ", "subAt": 4},
    {"type": "ledger", "at": 5, "title": "NHỮNG DÒNG CHỮ NHỎ", "rows": [{"k": "SỐ TƯỚNG", "v": "ÍT HƠN RẤT NHIỀU", "at": 6}, {"k": "MỘT VÀI CƠ CHẾ", "v": "BỊ TẮT", "at": [6, None, 0, 0.7]}],
     "total": {"k": "CÓ BÁO GỌI LÀ", "v": "“GẦN NHƯ GIAN LẬN”", "at": 7}},
    {"type": "myth", "at": 8, "mythLab": "ĐỘI OG", "myth": "PHIÊN BẢN KHÔNG QUEN", "truthLab": "CỖ MÁY", "truth": "PHIÊN BẢN ĐÃ LUYỆN", "strikeAt": 9, "truthAt": [9, None, 0, 0.4]},
    {"type": "kinetic", "at": 10, "items": [{"text": "NHÌN VÀO TỈ SỐ", "at": 10, "sm": True}, {"text": "HAY LUẬT CHƠI ĐÃ ĐỔI?", "at": [10, None, 0, 0.5], "acc": True}]},
]}

CH["ch20"] = {"hud": {"k": "CHƯƠNG 20", "t": "BỐN NGÀY, 42.729 VÁN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap(20, "CHƯƠNG HAI MƯƠI", "BỐN NGÀY,\nBỐN MƯƠI HAI NGHÌN VÁN", "MỞ CỬA CHO MỌI NGƯỜI", KEYS2, [0, None, 0, 0.05], ms=10),
    {"type": "ledger", "at": 1, "title": "OPENAI FIVE ARENA · 04/2019", "rows": [{"k": "AI CŨNG CHƠI ĐƯỢC", "v": "BỐN NGÀY", "at": 1},
                                                                            {"k": "HAI CHẾ ĐỘ", "v": "ĐẤU VỚI MÁY · CHƠI CÙNG MÁY", "at": 3}]},
    {"type": "counter", "at": 4, "from": 42729, "to": 42729, "suffix": " VÁN", "label": "VÁN CÔNG KHAI · THẮNG 99,4%", "sub": {"text": "THEO WIKIPEDIA", "at": 5}},
    {"type": "bars", "at": 6, "title": "CÁC VÁN ĐỐI ĐẦU", "unit": "SỐ LIỆU OPENAI · QUA BÁO CHÍ",
     "items": [{"k": "MÁY THẮNG", "v": 7215, "lbl": "7.215", "at": [6, None, 0, 0.6], "acc": True}, {"k": "MÁY THUA", "v": 42, "lbl": "42", "at": [6, None, 0, 0.85]}]},
    {"type": "slam", "at": 8, "text": "42 VÁN THUA", "sub": "KHÔNG NHIỀU · NHƯNG KHÔNG PHẢI SỐ KHÔNG", "subAt": 9},
    {"type": "counter", "at": 11, "from": 45000, "to": 45000, "prefix": "≈ ", "suffix": " NĂM", "label": "CHƠI DOTA · TRONG ≈ 10 THÁNG", "sub": {"text": "THEO OPENAI · QUA BÁO CHÍ", "at": 11}},
]}

CH["ch21"] = {"hud": {"k": "CHƯƠNG 21", "t": "CHƠI CÙNG MỘT ĐỘI VỚI MÁY"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap(21, "CHƯƠNG HAI MƯƠI MỐT", "CHƠI CÙNG\nMỘT ĐỘI VỚI MÁY", "CHI TIẾT ÍT ĐƯỢC NHẮC", TEAM, [0, None, 0, 0.05], ms=10),
    {"type": "counter", "at": 2, "from": 35000, "to": 35000, "prefix": "> ", "suffix": " VÁN", "label": "VÁN HỢP TÁC · NGƯỜI VÀ MÁY CÙNG ĐỘI", "sub": {"text": "THEO SỐ LIỆU ĐƯỢC BÁO CHÍ DẪN", "at": 3}},
    {"type": "myth", "at": 4, "mythLab": "KHÔNG CÒN LÀ", "myth": "AI GIỎI HƠN AI", "truthLab": "MÀ LÀ", "truth": "LÀM VIỆC CÙNG NHAU", "strikeAt": 5, "truthAt": 6},
    {"type": "ledger", "at": 7, "title": "HAI PHÍA", "rows": [{"k": "CỖ MÁY", "v": "ĐOÁN Ý NGƯỜI CHƯA GẶP", "at": 7}, {"k": "CON NGƯỜI", "v": "TIN ĐỒNG ĐỘI KHÔNG BIẾT NÓI", "at": 8}]},
    bro(9, CHESS, [{"text": "CỜ NHÂN MÃ · DEEP BLUE", "at": 9, "sm": True}, {"text": "NGƯỜI VÀ MÁY CÙNG MỘT PHE", "at": 10, "acc": True}], ms=8),
]}

CH["ch22"] = {"hud": {"k": "CHƯƠNG 22", "t": "200 NĂM VÀ 45.000 NĂM"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap(22, "CHƯƠNG HAI MƯƠI HAI", "HAI TRĂM NĂM VÀ\nBỐN MƯƠI LĂM NGHÌN NĂM", "ĐẶT CẠNH NHAU", DIGI, [0, None, 0, 0.05], ms=12),
    {"type": "ledger", "at": 1, "title": "THỜI GIAN LUYỆN TẬP", "rows": [{"k": "ALPHASTAR · MỖI PHIÊN BẢN", "v": "TỚI 200 NĂM", "at": 1}, {"k": "OPENAI FIVE", "v": "≈ 45.000 NĂM", "at": 2}]},
    {"type": "myth", "at": 3, "mythLab": "TUYỂN THỦ", "myth": "CẢ SỰ NGHIỆP", "truthLab": "CỖ MÁY", "truth": "VÀI GIỜ", "strikeAt": 4, "truthAt": [4, None, 0, 0.4]},
    {"type": "ledger", "at": 5, "title": "VỪA LÀ", "rows": [{"k": "SỨC MẠNH", "v": "KHÔNG AI LUYỆN NHIỀU THẾ", "at": 6}, {"k": "GIỚI HẠN", "v": "NGƯỜI HỌC TỪ VÀI VÁN", "at": 7}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "MANA · 42 VÁN THUA CỦA MÁY", "at": 8, "sm": True}, {"text": "NGƯỜI KIÊN NHẪN TÌM CHỖ YẾU", "at": 9, "acc": True}]},
    {"type": "slam", "at": 10, "text": "TRĂM NĂM ↔ MỘT BUỔI CHIỀU", "sub": "NHƯNG ĐÃ HỌC THÌ KHÔNG MỆT · KHÔNG QUÊN", "subAt": 11},
]}

CH["ch23"] = {"hud": {"k": "PHẦN CUỐI", "t": "NĂM ĐIỀU, ĐÃ ĐÁNH DẤU"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap(23, "PHẦN CUỐI", "NĂM ĐIỀU,\nĐÃ ĐÁNH DẤU", "QUAY LẠI DANH SÁCH", CHESS, [0, None, 0, 0.05], ms=14),
    five(1, 5, [3, None, 0, 0.3]),
    {"type": "ledger", "at": 5, "title": "MỖI DẤU TÍCH · MỘT DÒNG CHÚ THÍCH", "rows": [{"k": "1", "v": "MỘT BẢN ĐỒ · MỘT CHỦNG TỘC", "at": [6, None, 0, 0.05]},
                                                                                    {"k": "2", "v": "KHO TƯỚNG THU NHỎ", "at": [6, None, 0, 0.4]}, {"k": "3", "v": "TẦM NHÌN KHÁC NGƯỜI", "at": [6, None, 0, 0.7]}]},
    {"type": "ledger", "at": 7, "title": "NHỮNG GÌ HỌC ĐƯỢC", "rows": [{"k": "1", "v": "KẾ HOẠCH DÀI · THIẾU THÔNG TIN", "at": 10}, {"k": "2", "v": "PHỐI HỢP NHIỀU TÁC TỬ", "at": [10, None, 0, 0.4]},
                                                                  {"k": "3", "v": "BẮT CHƯỚC RỒI TỰ HỌC", "at": [10, None, 0, 0.7]}]},
    bro(11, SERVER, [{"text": "ROBOT · ĐIỀU PHỐI · TRỢ LÝ AI", "at": 11, "sm": True}, {"text": "LUẬT NÀO LÀ CÔNG BẰNG?", "at": 12, "acc": True}], ms=6),
    {"type": "question", "at": 15, "text": "Bạn sẽ chọn giới hạn nào\ncho cỗ máy khi đấu với người?"},
    {"type": "kinetic", "at": 16, "items": [{"text": "BẠN CHỌN LUẬT NÀO?", "at": 16}, {"text": "VIẾT XUỐNG BÌNH LUẬN", "at": [16, None, 0, 0.5], "acc": True}]},
]}

SPEC = {
    "title": "Máy Thắng Game Thời Gian Thực: AlphaStar, OpenAI Five Và Năm Điều Cờ Vua Không Có",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["máy", "starcraft", "dota", "năm", "điều", "thắng", "người"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(24)],
    "youtube": {
        "titles": ["Máy Thắng Game Thời Gian Thực: AlphaStar, OpenAI Five Và Năm Điều Cờ Vua Không Có",
                   "Từ Cờ Vua Tới StarCraft Và Dota 2: Vì Sao Game Điện Tử Khó Cho Máy Hơn Cờ",
                   "200 Năm Chơi Game Trong 14 Ngày: Cỗ Máy Thắng Tuyển Thủ Chuyên Nghiệp Thế Nào"],
        "summary": "Sau cờ vua và cờ vây, máy chuyển sang những trò chơi điện tử chiến thuật thời gian thực. Video kể câu chuyện AlphaStar (DeepMind, "
                   "StarCraft II): thắng TLO và MaNa 10 ván, thua ván biểu diễn thứ 11, rồi lên hạng Grandmaster với luật chặt hơn; và OpenAI Five (Dota 2): "
                   "thua ở The International 2018, thắng nhà vô địch OG năm 2019, thắng 99,4% trong 42.729 ván công khai. Qua năm điều cờ vua không có: "
                   "sương mù, không có lượt, ván dài, lựa chọn khổng lồ, đồng đội — và câu hỏi về sự công bằng giữa người và máy.",
        "more": ["Video làm nền là minh hoạ, không phải hình ảnh trận đấu hay trò chơi. Số liệu AlphaStar theo blog DeepMind 24/01/2019 và 30/10/2019 (Nature); "
                 "OpenAI Five theo Wikipedia và báo chí (các con số 45.000 năm, 10 tháng, 7.215 thắng – 42 thua là số OpenAI công bố, được báo chí dẫn lại)."],
        "chapter_titles": {"ch00": "Mở đầu: mười một ván", "ch01": "Sau những bàn cờ", "ch02": "Một phòng thí nghiệm an toàn", "ch03": "Từ những trò chơi điện tử cũ (DQN, Atari)",
                           "ch04": "Năm điều cờ vua không có", "ch05": "StarCraft là gì", "ch06": "Mười mũ hai mươi sáu lựa chọn", "ch07": "Học từ con người trước",
                           "ch08": "Giải đấu của những cỗ máy", "ch09": "Phần thưởng đến muộn", "ch10": "Mười ván, mười trận thắng", "ch11": "Đôi tay của cỗ máy",
                           "ch12": "350 phần nghìn giây", "ch13": "Ván thứ mười một", "ch14": "Đường lên Grandmaster", "ch15": "Năm người một đội: Dota 2",
                           "ch16": "Một chọi một: Dendi 2017", "ch17": "180 năm mỗi ngày", "ch18": "Thất bại ở The International 2018",
                           "ch19": "OG, tháng tư 2019", "ch20": "Bốn ngày, 42.729 ván", "ch21": "Chơi cùng một đội với máy", "ch22": "200 năm và 45.000 năm",
                           "ch23": "Năm điều, đã đánh dấu"},
        "sources": ["https://deepmind.google/discover/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/",
                    "https://deepmind.google/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/",
                    "https://en.wikipedia.org/wiki/OpenAI_Five",
                    "https://techcrunch.com/2019/04/15/openai-five-crushes-dota2-world-champs-and-soon-you-can-lose-to-it-too",
                    "https://www.engadget.com/2019-04-23-openai-five-dota-2-arena-results.html",
                    "https://research.google/blog/from-pixels-to-actions-human-level-control-through-deep-reinforcement-learning/"],
        "hashtags": ["AlphaStar", "OpenAIFive", "StarCraft", "Dota2", "MindInTheMachine"],
        "tags": ["alphastar", "openai five", "starcraft 2 ai", "dota 2 ai", "máy thắng game", "trí tuệ nhân tạo chơi game", "deepmind", "học tăng cường",
                 "người đấu với máy", "esports ai"],
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
