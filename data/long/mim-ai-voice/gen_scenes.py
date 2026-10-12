"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #3 "AI Giả Giọng Người Thân Để Lừa Tiền".

    python data/long/mim-ai-voice/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (bản 2, đã kiểm chứng) + factcheck.md. Dữ kiện + nguồn: docs/channels/mind-in-the-machine/2026-10-07-long-03-research.md.
Ảnh: chỉ PD / CC0 / CC BY (kênh MIM không nhận BY-SA — build_long kiểm lại lúc tải). Clip: Pexels (ngang), mọi clip gắn
"VIDEO MINH HỌA"; tải bằng `python motion/long/pexels.py get mim-ai-voice <id> ...`.
Quy tắc riêng của video này (factcheck mục 2 + 5):
  - Không chiếu mặt bà DeStefano hay con gái; không dựng giọng giả của người thật. Lời trích (») đọc bằng giọng TTS của kênh,
    cảnh quote gắn thẻ "GIỌNG MÁY TẠO" (cạnh nhãn "GIỌNG ĐỌC MINH HỌA" của engine).
  - Không nêu tên dịch vụ nhân bản giọng, không chiếu trang Consumer Reports.
  - Ảnh Voder: CHỈ ảnh "The VODER fascinates the crowds" (BTQ 01/1940, Hội chợ New York 1939; Commons ghi "1922" là sai)
    và BSTJ Fig.5 (New York). Ảnh "lining up" (đo thính lực) và "Audition" KHÔNG phải Voder -> không dùng.
  - IBM 7090 = NASA Ames 06/09/1961, ẢNH MINH HỌA (không phải máy hát Daisy). Bell Labs Murray Hill = 1942.
    Máy nói Kempelen trong ảnh = bản dựng lại hiện đại.
Nhạc: chốt trong output/long/mim-ai-voice/bgm_picks.json (ghi bởi file này) — 5 bài MIM, trùng ít với mim-ai-70
(2/9) và mim-ai-jobs (3/11). Gain bù độ to: Equatorial Complex ≈ −25 LUFS, Floating Cities ≈ −20 LUFS, còn lại ≈ −10..−12.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
OUT = D.parents[2] / "output" / "long" / D.name

IMGS = {
    "turk": "File:Tuerkischer schachspieler windisch4.jpg",                                       # PD · tranh khắc thế kỷ 18
    "racknitz": "File:Racknitz - The Turk 3.jpg",                                                 # PD · Racknitz 1789 (phỏng đoán)
    "kempdraw": "File:Speech synthesizer Von Kempelen 1791.gif",                                  # PD · hình trong sách 1791
    "kemprecon": "File:Kempelen Speakingmachine.JPG",                                             # PD · bản dựng lại, Saarbrücken
    "voder": "File:VODER demonstrated on 1939 New York World Fair - The VODER fascinates the crowds - Bell Telephone Quarterly (January 1940).jpg",  # No restrictions · NY 1939
    "voderfig": "File:Homer Dudley (October 1940). \"The Carrier Nature of Speech\". Bell System Technical Journal, XIX(4);495-515. -- Fig.5 The voder being demonstrated at the New York World's Fair.jpg",  # No restrictions
    "ibm7090": "File:IBM 7090 computer.jpg",                                                     # PD · NASA Ames 06.09.1961
    "ibm7094": "File:IBM 7094 console3.agr.jpg",                                                 # CC BY 4.0 · ArnoldReinhold (CHM)
    "belllabs": "File:Bell Telephone Laboratories, Murray Hill, New Jersey. LOC gsc.5a08712.jpg",  # PD · Gottscho-Schleisner 1942
    "daisy": "File:Daisybell.jpg",                                                                # PD · bản in Úc, sau 1921
    "clarke": "File:Arthur C. Clarke 1965.jpg",                                                  # CC BY 2.0 · ITU Pictures
    "hknight": "File:Hong Kong skyscrapers in a night of typhoon.jpg",                           # CC0 · Wilfredor 2013
    "hkharbour": "File:Victoria Harbour skyscrapers.jpg",                                         # CC0 · Wilfredor 2013
}

SAY = {   # chữ hiển thị -> cách đọc (phụ đề giữ chữ gốc); "=X" = khớp đúng hoa/thường. Khoá viết thường, NFC.
    # factcheck mục 3: khoá "=" so ĐÚNG hoa/thường -> viết đúng như trong lời đọc (VALL-E, FBI, AI, C, A)
    "=AI": "ây ai", "=VALL-E": "Van-i", "=FBI": "Ép-bi-ai", "=C": "Xi", "=A": "Ơ",
    "jennifer": "Gien-ni-phơ", "destefano": "Đờ-xtê-pha-nô", "scottsdale": "Xcốt-xđêu", "arizona": "A-ri-dô-na",
    "wolfgang": "Vôn-phơ-gang", "von": "phôn", "kempelen": "Kem-pơ-lần",
    "napoléon": "Na-pô-lê-ông", "napoléon": "Na-pô-lê-ông", "napoleon": "Na-pô-lê-ông",   # NFC + NFD + không dấu
    "new": "Niu", "york": "Doóc", "bell": "Ben", "voder": "Vô-đơ", "microsoft": "Mai-crô-xốp",
    "chatgpt": "chát gi pi ti", "openai": "Ô-pần Ây-ai", "consumer": "Con-xiu-mơ", "reports": "Ri-pót",
    "college": "Co-lít", "london": "Luân Đôn", "cnn": "Xi-en-en", "hany": "Ha-ni", "farid": "Pha-rít",
    "california": "Ca-li-pho-ni-a", "berkeley": "Bơ-cơ-li", "arup": "A-rớp", "opera": "Ô-pê-ra", "sydney": "Xít-ni",
    "bkav": "Bê-kav", "messenger": "Mét-xen-giơ", "facebook": "Phây-búc", "email": "i-meo",
    "ibm": "ai bi em", "daisy": "Đây-di", "arthur": "A-thơ", "clarke": "Clác", "space": "Xpêt", "odyssey": "Ô-đi-xê",
    "hal": "Han",
}

VM = "VIDEO MINH HỌA"
GMT = {"text": "GIỌNG MÁY TẠO"}     # thẻ trên mọi cảnh lời trích: câu đọc bằng giọng TTS của kênh, không phải băng ghi âm thật

# Nhạc: chốt tay (ít trùng với 2 video MIM trước), xem docstring.
BGM_PICKS = {"ch00.0": "ice_flow.mp3", "ch01.0": "chill_wave.mp3", "ch02.0": "ouroboros.mp3", "ch03.0": "equatorial_complex.mp3",
             "ch04.0": "ice_flow.mp3", "ch05.0": "ouroboros.mp3", "ch06.0": "equatorial_complex.mp3", "ch07.0": "chill_wave.mp3",
             "ch08.0": "floating_cities.mp3"}

CH = {}

# ---------------- CH00 · Cuộc gọi bốn phút ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "CUỘC GỌI BỐN PHÚT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "SCOTTSDALE · ARIZONA · MỸ", "date": "20.01.2023"},
    {"type": "broll", "at": 1, "vid": "8176782", "veil": 0.5, "illus": VM,
     "kin": [{"text": "JENNIFER DESTEFANO", "at": 1, "sm": True},
             {"text": "ĐỖ XE TRƯỚC PHÒNG TẬP MÚA", "at": [1, "đỗ"]},
             {"text": "nơi con gái út của bà đang tập", "at": [1, "nơi"], "sm": True}]},
    {"type": "broll", "at": 2, "vid": "8060389", "veil": 0.45, "illus": VM,
     "kin": [{"text": "ĐIỆN THOẠI REO", "at": 2}, {"text": "SỐ LẠ", "at": [2, "số"], "acc": True},
             {"text": "bà định không nghe", "at": 3, "sm": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "CON GÁI LỚN · 15 TUỔI", "at": 4, "sm": True},
                                          {"text": "ĐANG Ở XA · TẬP TRƯỢT TUYẾT", "at": [4, "đang"]},
                                          {"text": "BIẾT ĐÂU CON BỊ NGÃ…", "at": [4, "biết"], "acc": True}]},
    {"type": "broll", "at": 5, "vid": "6183991", "veil": 0.5, "illus": VM,
     "kin": [{"text": "BÀ BẤM NGHE", "at": 5, "sm": True}, {"text": "TIẾNG KHÓC", "at": [5, "tiếng"], "acc": True}]},
    {"type": "quote", "at": 6, "text": "Mom, I messed up!", "by": "LỜI KHAI CỦA J. DESTEFANO · THƯỢNG VIỆN MỸ, 13.06.2023",
     "lbl": "TRÍCH DỊCH", "qline": 6, "tag": GMT},
    {"type": "kinetic", "at": 7, "items": [{"text": "MỘT GIỌNG ĐÀN ÔNG CHEN VÀO", "at": 7, "sm": True},
                                          {"text": "HẮN ĐANG GIỮ CON GÁI BÀ", "at": [7, "hắn"], "acc": True}]},
    {"type": "kinetic", "at": 8, "vid": "7714378", "illus": VM, "items": [{"text": "GỌI CẢNH SÁT?", "at": 8, "sm": True},
                                                                       {"text": "KHÔNG BAO GIỜ GẶP LẠI CON", "at": [8, "không"], "acc": True}]},
    {"type": "counter", "at": 9, "from": 0, "to": 1000000, "prefix": "$", "label": "TIỀN CHUỘC HẮN ĐÒI",
     "sub": {"text": "HƠN 24 TỈ ĐỒNG (TỈ GIÁ ≥ 24.000 Đ/USD) · THEO LỜI KHAI TRƯỚC THƯỢNG VIỆN", "at": [9, "hơn"]}},
    {"type": "kinetic", "at": 10, "items": [{"text": "BÀ KHÔNG CÓ", "at": 10, "sm": True},
                                           {"text": "HẠ XUỐNG $50.000", "at": [10, "hạ"], "acc": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "MỘT CHIẾC XE VAN TRẮNG", "at": 11},
                                           {"text": "TRÙM TÚI LÊN ĐẦU BÀ", "at": [11, "trùm"], "acc": True},
                                           {"text": "để bà mang tiền mặt tới", "at": [11, "để"], "sm": True}]},
    {"type": "broll", "at": 12, "vid": "8176782", "ms": 12, "veil": 0.55, "illus": VM,
     "kin": [{"text": "TRONG PHÒNG TẬP", "at": 12, "sm": True},
             {"text": "MỘT PHỤ HUYNH GỌI CẢNH SÁT", "at": [12, "một"]},
             {"text": "một người khác gọi cho con gái lớn", "at": 13, "sm": True, "acc": True}]},
    {"type": "broll", "at": 14, "vid": "6183991", "ms": 20, "veil": 0.55, "illus": VM,
     "kin": [{"text": "MỘT CHIẾC ĐIỆN THOẠI KHÁC", "at": 14, "sm": True},
             {"text": "ĐẦU DÂY: CON GÁI BÀ", "at": 15, "acc": True},
             {"text": "đang nằm trên giường · an toàn", "at": [15, "nằm"], "sm": True}]},
    {"type": "counter", "at": 16, "from": 0, "to": 4, "suffix": " PHÚT", "label": "TẤT CẢ CHỈ DIỄN RA TRONG KHOẢNG",
     "sub": {"text": "“ONE OF THE WORST 4 MINUTES OF MY LIFE” · LỜI KHAI 13.06.2023", "at": 16}},
    {"type": "kinetic", "at": 17, "items": [{"text": "MỘT THỨ BÀ KHÔNG QUÊN ĐƯỢC", "at": 17, "sm": True},
                                           {"text": "GIỌNG NÓI ẤY", "at": [17, "giọng"], "acc": True}]},
    {"type": "broll", "at": 18, "vid": "34645273", "veil": 0.45, "illus": VM,
     "kin": [{"text": "TIẾNG NỨC NỞ", "at": 18}, {"text": "CÁCH LÊN XUỐNG GIỌNG", "at": [18, "cách"]},
             {"text": "GIỐNG HỆT CON BÀ", "at": [18, "giống"], "acc": True}]},
    {"type": "question", "at": 19, "text": "Vậy giọng nói trong điện thoại\nlà của ai?"},
    {"type": "kinetic", "at": 20, "items": [{"text": "TRƯỚC KHI TRẢ LỜI", "at": 20, "sm": True},
                                           {"text": "MÌNH THÁCH BẠN ĐOÁN MỘT CON SỐ", "at": [20, "mình"], "acc": True}]},
    {"type": "kinetic", "at": 21, "items": [{"text": "BẮT CHƯỚC GIỌNG MỘT NGƯỜI LẠ", "at": 21, "sm": True},
                                           {"text": "CỖ MÁY CẦN NGHE BAO LÂU?", "at": [21, "một", 1], "acc": True}]},
    {"type": "kinetic", "at": 22, "items": [{"text": "MỘT GIỜ?", "at": 22}, {"text": "MƯỜI PHÚT?", "at": [22, "mười"]},
                                           {"text": "MỘT PHÚT?", "at": [22, "hay"], "acc": True}]},
    {"type": "kinetic", "at": 23, "items": [{"text": "GIỮ CON SỐ ẤY TRONG ĐẦU", "at": 23, "acc": True},
                                           {"text": "vài phút nữa, bạn sẽ biết mình đoán lệch bao xa", "at": [23, "chỉ"], "sm": True}]},
    {"type": "brand", "at": 24, "sub": "AI · GIẢ GIỌNG · MỘT TỪ BÍ MẬT"},
]}

# ---------------- CH01 · Cỗ máy biết nói ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CỖ MÁY BIẾT NÓI"}, "bgm": {"mood": "calm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CỖ MÁY\nBIẾT NÓI", "sub": "1770 — 1939", "bg": "turk", "titleAt": [0, "Năm"]},
    {"type": "print", "at": 1, "img": "turk", "tone": "bw", "caption": "TRANH KHẮC THẾ KỶ 18",
     "side": {"k": "KEMPELEN · 1770", "h": "Cỗ máy\nđánh cờ", "lines": [
         {"text": "Hình nộm mặc áo *kiểu Thổ Nhĩ Kỳ*", "at": 1},
         {"text": "ngồi sau *một chiếc tủ gỗ*", "at": [1, "ngồi"]}]}},
    {"type": "kinetic", "at": 2, "bg": "turk", "items": [{"text": "KHẮP CHÂU ÂU · NƯỚC MỸ", "at": 2, "sm": True},
                                                       {"text": "THẮNG PHẦN LỚN CÁC VÁN CỜ", "at": [2, "thắng"], "acc": True},
                                                       {"text": "có cả ván với Napoléon (giai thoại phổ biến)", "at": [2, "có"], "sm": True}]},
    {"type": "slam", "at": 3, "bg": "turk", "text": "MỘT TRÒ LỪA"},
    {"type": "photo", "at": 4, "img": "racknitz", "tone": "bw", "move": "in", "veil": 0.45, "focus": [0.5, 0.6],
     "kin": [{"text": "KỲ THỦ THẬT", "at": 4, "sm": True}, {"text": "GIẤU KÍN TRONG TỦ", "at": [4, "giấu"], "acc": True}],
     "label": {"k": "RACKNITZ · 1789", "v": "HÌNH VẼ PHỎNG ĐOÁN", "at": 4}},
    {"type": "kinetic", "at": 5, "bg": "racknitz", "items": [{"text": "MỘT CỖ MÁY GIẢ LÀM NGƯỜI", "at": 5},
                                                           {"text": "NHỜ MỘT CON NGƯỜI GIẤU BÊN TRONG", "at": [5, "nhờ"], "acc": True},
                                                           {"text": "hãy nhớ hình ảnh này", "at": [5, "hãy"], "sm": True}]},
    {"type": "print", "at": 6, "img": "kempdraw", "tone": "bw", "maxH": 600, "caption": "HÌNH TRONG SÁCH 1791",
     "side": {"k": "KEMPELEN", "h": "Cỗ máy\nbiết nói", "lines": [
         {"text": "Ống bễ *thay cho phổi*", "at": [7, "ống"]},
         {"text": "Mô hình *lưỡi và môi*", "at": [7, "lưỡi"]},
         {"text": "*Nguyên âm* lẫn *phụ âm*", "at": [7, "nguyên"]}]}},
    {"type": "print", "at": 8, "img": "kemprecon", "tone": "color", "caption": "BẢN DỰNG LẠI HIỆN ĐẠI",
     "side": {"k": "GẦN 20 NĂM NGHIÊN CỨU", "h": "In thành sách\nnăm 1791", "lines": [
         {"text": "Ảnh: *bản dựng lại* ở Saarbrücken", "at": 8},
         {"text": "không phải máy thế kỷ 18", "at": [8, "in"]}]}},
    {"type": "photo", "at": 9, "img": "voder", "tone": "bw", "move": "in", "veil": 0.5, "focus": [0.5, 0.45],
     "kin": [{"text": "NEW YORK · 1939", "at": 9, "acc": True},
             {"text": "HỘI CHỢ THẾ GIỚI", "at": [9, "hội"], "sm": True},
             {"text": "> 5 TRIỆU LƯỢT KHÁCH VÀO PHÒNG VODER", "at": [9, "hàng"], "sm": True}],
     "label": {"k": "BELL TELEPHONE QUARTERLY · 01.1940", "v": "“THE VODER FASCINATES THE CROWDS”", "at": 9}},
    {"type": "print", "at": 10, "img": "voderfig", "tone": "bw", "maxW": 560, "caption": "BSTJ 10.1940 · HỘI CHỢ NEW YORK",
     "side": {"k": "PHÒNG THÍ NGHIỆM BELL", "h": "VODER", "lines": [
         {"text": "*Phím*: tạo từng âm", "at": [11, "bấm"]},
         {"text": "*Cổ tay*: tiếng rít ↔ tiếng ù", "at": [11, "gạt"]},
         {"text": "*Bàn đạp*: lên xuống giọng", "at": [11, "đạp"]}]}},
    {"type": "kinetic", "at": 12, "bg": "voder", "items": [{"text": "LUYỆN TẬP NHIỀU THÁNG", "at": 12, "acc": True},
                                                         {"text": "mới nói được những câu nghe ra chữ", "at": [12, "mới"], "sm": True}]},
    {"type": "timeline", "at": 13, "items": [{"year": "1770", "text": "Cỗ máy *đánh cờ*", "at": 13},
                                            {"year": "1791", "text": "Sách về *máy nói*", "at": [13, "tới"]},
                                            {"year": "1939", "text": "*Voder* · New York", "at": [13, "voder"]}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "GIỌNG CỦA CHÚNG", "at": 14, "sm": True},
                                           {"text": "KHÔNG GIỐNG GIỌNG CỦA AI CẢ", "at": [14, "không"], "acc": True}]},
    {"type": "kinetic", "at": 15, "vid": "13283744", "illus": VM, "items": [{"text": "SUỐT CHỪNG ẤY THỜI GIAN", "at": 15, "sm": True},
                                                                         {"text": "GIỌNG NÓI = MẬT KHẨU", "at": [15, "giọng"], "acc": True},
                                                                         {"text": "nghe là biết ai", "at": [15, "nghe"], "sm": True}]},
    {"type": "slam", "at": 16, "text": "MỌI THỨ\nĐẢO NGƯỢC"},
]}

# ---------------- CH02 · Ba giây ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BA GIÂY"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "BA GIÂY", "sub": "MICROSOFT · VALL-E · 01.2023", "vid": "34645273",
     "titleAt": [0, "Tháng"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "HAI CHUYỆN KHÔNG LIÊN QUAN", "at": 1, "sm": True},
                                          {"text": "NHƯNG CÙNG MỘT THÁNG", "at": [1, "nhưng"], "acc": True}]},
    {"type": "counter", "at": 2, "vid": "6892725", "illus": VM, "from": 0, "to": 60000, "suffix": " GIỜ",
     "label": "TIẾNG ANH VALL-E ĐƯỢC CHO NGHE", "sub": {"text": "CỦA HƠN 7.000 NGƯỜI NÓI · ARXIV 2301.02111", "at": [2, "hơn"]}},
    {"type": "kinetic", "at": 3, "items": [{"text": "60.000 GIỜ", "at": 3, "sm": True},
                                          {"text": "≈ GẦN 7 NĂM NGHE LIÊN TỤC", "at": [3, "gần"], "acc": True},
                                          {"text": "không ngủ · 60.000 ÷ 24 ÷ 365 ≈ 6,85 năm", "at": [3, "không"], "sm": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "GIỌNG MỘT NGƯỜI NÓ CHƯA TỪNG NGHE", "at": 4, "sm": True},
                                          {"text": "CHỈ CẦN 3 GIÂY GHI ÂM", "at": [4, "chỉ"], "acc": True}]},
    {"type": "bars", "at": 5, "title": "BẠN ĐÃ ĐOÁN BAO NHIÊU?", "unit": "VALL-E · MICROSOFT · 01.2023", "items": [
        {"k": "MỘT GIỜ", "v": 3600, "lbl": "3.600 GIÂY"}, {"k": "MƯỜI PHÚT", "v": 600, "lbl": "600 GIÂY"},
        {"k": "MỘT PHÚT", "v": 60, "lbl": "60 GIÂY"}, {"k": "VALL-E", "v": 3, "lbl": "3 GIÂY", "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "CÁCH NÓ LÀM", "at": 6, "acc": True},
                                          {"text": "có lẽ bạn đã nghe ở video đầu tiên của kênh", "at": [6, "có"], "sm": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "CHATGPT: ĐOÁN MẨU CHỮ TIẾP THEO", "at": 7},
                                          {"text": "VALL-E: ĐOÁN MẨU ÂM TIẾP THEO", "at": [7, "vall-e"], "acc": True}]},
    {"type": "broll", "at": 8, "vid": "6892725", "ms": 8, "veil": 0.5, "illus": VM,
     "kin": [{"text": "GIỌNG NÓI → NHỮNG MẨU ÂM NHỎ", "at": 8},
             {"text": "ĐOÁN MẨU TIẾP THEO… RỒI TIẾP THEO NỮA", "at": [8, "đoán"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "7.000 GIỌNG NGƯỜI", "at": 9, "acc": True},
                                          {"text": "dạy nó cách con người nói nói chung", "at": [9, "dạy"], "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "3 GIÂY CỦA BẠN", "at": 10, "sm": True},
                                           {"text": "“LẦN NÀY, HÃY NÓI NHƯ AI”", "at": [10, "lần"], "acc": True}]},
    {"type": "kinetic", "at": 11, "vid": "13283744", "illus": VM, "items": [{"text": "CÁC TÁC GIẢ CÒN THẤY", "at": 11, "sm": True},
                                                                         {"text": "GIỮ CẢ CẢM XÚC", "at": [11, "giữ"]},
                                                                         {"text": "như sự giận dữ", "at": [11, "như"], "sm": True},
                                                                         {"text": "VÀ TIẾNG VANG CĂN PHÒNG", "at": [11, "tiếng"], "acc": True}]},
    {"type": "quote", "at": 12, "text": "…potential risks in misuse of the model, such as spoofing voice identification or impersonating a specific speaker.",
     "by": "NHÓM TÁC GIẢ VALL-E · ARXIV, 01.2023", "lbl": "TRÍCH BÀI BÁO"},
    {"type": "kinetic", "at": 13, "items": [{"text": "VALL-E 2 · 2024", "at": 13, "sm": True},
                                           {"text": "“THUẦN TUÝ LÀ DỰ ÁN NGHIÊN CỨU”", "at": [13, "thuần"], "acc": True},
                                           {"text": "chưa có kế hoạch đưa ra công chúng · Microsoft Research", "at": [13, "chưa"], "sm": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "OPENAI · 03.2024", "at": 14, "sm": True},
                                           {"text": "15 GIÂY GIỌNG MẪU", "at": [14, "mười"], "acc": True},
                                           {"text": "cũng chưa mở rộng ra công chúng", "at": [14, "cũng"], "sm": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "OPENAI CÒN KHUYÊN", "at": 15, "sm": True},
                                           {"text": "BỎ DẦN XÁC THỰC TÀI KHOẢN BẰNG GIỌNG NÓI", "at": [15, "bỏ"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "PHÒNG THÍ NGHIỆM LỚN: DÈ DẶT", "at": 16},
                                           {"text": "NGOÀI KIA: CHƯA AN TOÀN", "at": [16, "ngoài"], "acc": True}]},
    {"type": "date", "at": 17, "day": "CONSUMER REPORTS · 6 DỊCH VỤ", "date": "03.2025"},
    {"type": "counter", "at": 18, "from": 0, "to": 4, "suffix": " / 6", "label": "DỊCH VỤ KHÔNG CÓ BƯỚC CƠ BẢN ĐỂ NGĂN SAO CHÉP GIỌNG NGƯỜI KHÁC",
     "sub": {"text": "CONSUMER REPORTS · 10.03.2025", "at": 18}},
    {"type": "question", "at": 19, "vid": "34645273", "ms": 6, "text": "Tai người\ncòn phân biệt được không?"},
]}

# ---------------- CH03 · Đôi tai thua cuộc ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "ĐÔI TAI THUA CUỘC"}, "bgm": {"mood": "mystery", "gain": 0.5}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "ĐÔI TAI\nTHUA CUỘC", "sub": "UCL · LONDON · 2023", "vid": "6892725", "ms": 14,
     "titleAt": [0, "Năm"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "529 NGƯỜI NGHE", "at": 1, "acc": True},
                                          {"text": "được báo trước: trong này có giọng giả", "at": [1, "được"], "sm": True}]},
    {"type": "counter", "at": 2, "from": 0, "to": 73, "suffix": "%", "label": "SỐ LẦN NHẬN RA GIỌNG GIẢ",
     "sub": {"text": "MAI ET AL. · PLOS ONE, 08.2023 · 529 NGƯỜI", "at": 2}},
    {"type": "slam", "at": 3, "text": "HƠN 1/4 SỐ LẦN\nBỊ LỪA", "sub": "100% − 73% = 27%"},
    {"type": "kinetic", "at": 4, "items": [{"text": "TIẾNG ANH · TIẾNG QUAN THOẠI", "at": 4},
                                          {"text": "KẾT QUẢ NHƯ NHAU", "at": [4, "kết"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "LÀM QUEN TRƯỚC VỚI GIỌNG GIẢ", "at": 5, "sm": True},
                                          {"text": "CHỈ KHÁ HƠN MỘT CHÚT", "at": [5, "chỉ"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "ĐÓ LÀ TRONG PHÒNG THÍ NGHIỆM", "at": 6},
                                          {"text": "ngồi yên · biết mình đang bị thử", "at": [6, "ngồi"], "sm": True}]},
    {"type": "slam", "at": 7, "text": "NGOÀI ĐỜI,\nKHÔNG AI BÁO TRƯỚC", "white": True},
    {"type": "broll", "at": 8, "vid": "8176782", "ms": 3, "veil": 0.55, "illus": VM,
     "kin": [{"text": "QUAY LẠI PHÒNG TẬP MÚA", "at": 8}, {"text": "ARIZONA · 20.01.2023", "at": [8, "ở"], "sm": True}]},
    {"type": "kinetic", "at": 9, "vid": "7714378", "ms": 4, "illus": VM, "items": [
        {"text": "CUỘC GỌI CẤP CỨU 911", "at": 9, "sm": True},
        {"text": "ĐIỀU PHỐI VIÊN NHẬN RA NGAY", "at": [9, "điều"], "acc": True}]},
    {"type": "quote", "at": 10, "text": "So that is a very popular scam.", "by": "ĐIỀU PHỐI VIÊN 911 · GHI ÂM DO CẢNH SÁT SCOTTSDALE CUNG CẤP CHO CNN",
     "lbl": "TRÍCH DỊCH", "qline": 10, "tag": GMT},
    {"type": "kinetic", "at": 11, "items": [{"text": "KHÔNG NGHE RA GIỌNG", "at": 11, "sm": True},
                                           {"text": "NGHE RA KỊCH BẢN", "at": [11, "nghe", 1], "acc": True}]},
    {"type": "ledger", "at": 12, "title": "KỊCH BẢN BA NHỊP", "srcnote": "MIM TỔNG HỢP TỪ FTC, FBI", "rows": [
        {"k": "GẤP", "v": "PHẢI LÀM NGAY", "at": 13},
        {"k": "GIẤU", "v": "KHÔNG ĐƯỢC NÓI VỚI AI", "at": 14},
        {"k": "TIỀN", "v": "CHUYỂN THEO CÁCH KHÓ ĐÒI LẠI", "at": 15}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "ỦY BAN THƯƠNG MẠI LIÊN BANG MỸ (FTC)", "at": 16, "sm": True},
                                           {"text": "TRẢ TIỀN THEO CÁCH RẤT KHÓ ĐÒI LẠI", "at": [16, "trả"], "acc": True}]},
    {"type": "kinetic", "at": 17, "vid": "7535102", "illus": VM, "items": [
        {"text": "CHUYỂN KHOẢN · TIỀN MÃ HOÁ · THẺ QUÀ TẶNG", "at": 17},
        {"text": "= DẤU HIỆU LỪA ĐẢO", "at": [17, "dấu"], "acc": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "GIỌNG NÓI CÓ THỂ GIẢ", "at": 18},
                                           {"text": "KỊCH BẢN THÌ LẶP LẠI", "at": [18, "kịch"], "acc": True}]},
    {"type": "slam", "at": 19, "text": "GẤP · GIẤU · TIỀN", "sub": "CUỐI VIDEO: VŨ KHÍ CỦA BẠN"},
    {"type": "question", "at": 20, "text": "Giọng trong điện thoại ấy\ncó thật là do AI?"},
]}

# ---------------- CH04 · Có thật là AI không? ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "CÓ THẬT LÀ AI KHÔNG?"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "CÓ THẬT\nLÀ AI KHÔNG?", "sub": "ARIZONA · 2023", "vid": "34645273", "ms": 9,
     "titleAt": [0, "Câu"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "THEO CNN", "at": 1, "sm": True},
                                          {"text": "CHƯA ĐƯỢC XÁC MINH", "at": [1, "chưa"], "acc": True},
                                          {"text": "vụ này có dùng AI hay không", "at": [1, "vụ"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "BÀ DESTEFANO", "at": 2, "sm": True}, {"text": "TIN LÀ CÓ", "at": [2, "tin"], "acc": True}]},
    {"type": "date", "at": 3, "day": "LỜI KHAI TRƯỚC TIỂU BAN THƯỢNG VIỆN MỸ", "date": "13.06.2023"},
    {"type": "kinetic", "at": 4, "items": [{"text": "HAI THÁNG TRƯỚC · 04.2023 · NÓI VỚI CNN", "at": 4, "sm": True},
                                          {"text": "GS. HANY FARID · UC BERKELEY", "at": [4, "hany"]},
                                          {"text": "BẢN SAO GIỌNG KHÁ TỐT: CHƯA TỚI 1 PHÚT GHI ÂM", "at": [4, "bản"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "NHƯNG THEO HIỂU BIẾT LÚC ẤY", "at": 5, "sm": True},
                                          {"text": "CHƯA GIẢ ĐƯỢC TIẾNG GÀO KHÓC HOẢNG LOẠN", "at": [5, "chưa"], "acc": True},
                                          {"text": "…dù vậy, không dám loại trừ hoàn toàn", "at": 6, "sm": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "CÓ THỂ LÀ AI", "at": 7},
                                          {"text": "CŨNG CÓ THỂ: MỘT ĐOẠN GHI ÂM TIẾNG KHÓC BẤT KỲ", "at": [7, "cũng"], "acc": True}]},
    {"type": "kinetic", "at": 8, "vid": "8530312", "illus": VM, "items": [
        {"text": "VỚI MỘT NGƯỜI MẸ ĐANG HOẢNG LOẠN", "at": 8, "sm": True},
        {"text": "CHUYỆN ẤY GẦN NHƯ KHÔNG QUAN TRỌNG", "at": [8, "chuyện"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "FBI GIẢI THÍCH VỚI CNN", "at": 9, "sm": True},
                                          {"text": "NGƯỜI THÂN ĐANG HOẢNG LOẠN", "at": [9, "người"]},
                                          {"text": "KHÔNG KỊP HỎI: GIỌNG THẬT HAY KHÔNG?", "at": [9, "không"], "acc": True}]},
    {"type": "slam", "at": 10, "text": "NỖI SỢ LÀM NỐT\nPHẦN CÒN LẠI"},
    {"type": "quote", "at": 11, "text": "A mother knows her child.", "by": "JENNIFER DESTEFANO · CNN, 29.04.2023",
     "lbl": "TRÍCH DỊCH", "qline": 11, "tag": GMT},
    {"type": "kinetic", "at": 12, "items": [{"text": "BÀ NÓI ĐÚNG", "at": 12, "acc": True},
                                           {"text": "vì thương con, bà nghe ra tiếng con ở một nơi không hề có con", "at": 13, "sm": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "CUỐI VIDEO", "at": 14, "sm": True},
                                           {"text": "MỘT THỨ MÁY KHÔNG SAO CHÉP ĐƯỢC", "at": [14, "một"], "acc": True}]},
    {"type": "broll", "at": 15, "vid": "7206746", "veil": 0.5, "illus": VM,
     "kin": [{"text": "TRƯỚC ĐÓ: MỘT VỤ CÓ HÌNH VÀ GIỌNG GIẢ", "at": 15, "sm": True},
             {"text": "NẠN NHÂN KHÔNG HỀ HOẢNG LOẠN", "at": [15, "nạn"], "acc": True}]},
]}

# ---------------- CH05 · Cuộc họp không có ai thật ----------------
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "CUỘC HỌP KHÔNG CÓ AI THẬT"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "CUỘC HỌP\nKHÔNG CÓ AI THẬT", "sub": "HỒNG KÔNG · 01.2024", "vid": "2856781",
     "titleAt": [0, "Hồng"]},
    {"type": "broll", "at": 1, "vid": "7643848", "veil": 0.55, "illus": VM,
     "kin": [{"text": "NHÂN VIÊN TÀI CHÍNH · CÔNG TY ĐA QUỐC GIA", "at": 1, "sm": True},
             {"text": "EMAIL TỪ “GIÁM ĐỐC TÀI CHÍNH”", "at": [1, "như"], "acc": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "EMAIL", "at": 2, "sm": True},
                                          {"text": "“GIAO DỊCH CẦN GIỮ BÍ MẬT”", "at": [2, "giao"], "acc": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "ANH TA NGHI NGỜ", "at": 3},
                                          {"text": "có thể là thư lừa đảo", "at": [3, "có"], "sm": True}]},
    {"type": "broll", "at": 4, "vid": "5486225", "veil": 0.45, "illus": VM,
     "kin": [{"text": "MỜI VÀO MỘT CUỘC HỌP VIDEO", "at": 4, "sm": True},
             {"text": "MẶT QUEN · GIỌNG QUEN", "at": [5, "mặt"], "acc": True}]},
    {"type": "slam", "at": 6, "text": "ANH TA HẾT NGHI", "white": True},
    {"type": "counter", "at": 7, "vid": "2856781", "ms": 14, "illus": VM, "from": 0, "to": 200, "suffix": " TRIỆU",
     "label": "ĐÔ LA HỒNG KÔNG · CHIA LÀM 15 LẦN · VÀO 5 TÀI KHOẢN", "labelAt": [7, "chia"],
     "sub": {"text": "CẢNH SÁT HỒNG KÔNG · THEO LEGCO, RTHK, AFP", "at": 7}},
    {"type": "kinetic", "at": 8, "items": [{"text": "≈ 25 TRIỆU USD", "at": 8, "acc": True},
                                          {"text": "HƠN 600 TỈ ĐỒNG", "at": [8, "hơn"]},
                                          {"text": "CNN: 25,6 triệu USD · quy đổi theo tỉ giá ≥ 24.000 đ/USD", "at": [8, "hơn"], "sm": True}]},
    {"type": "slam", "at": 9, "text": "KHÔNG AI\nLÀ NGƯỜI THẬT"},
    {"type": "date", "at": 10, "day": "HỘI ĐỒNG LẬP PHÁP HỒNG KÔNG", "date": "26.06.2024",
     "label": {"k": "NGƯỜI ĐỨNG ĐẦU NGÀNH AN NINH", "v": "CUỘC HỌP ĐƯỢC GHI HÌNH SẴN", "at": [10, "cuộc"]}},
    {"type": "broll", "at": 11, "vid": "5486225", "ms": 22, "veil": 0.55, "illus": VM,
     "kin": [{"text": "DỰNG TỪ VIDEO + GIỌNG NÓI CÔNG KHAI", "at": 11, "sm": True},
             {"text": "CỦA CHÍNH NGƯỜI BỊ GIẢ MẠO", "at": [11, "của"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "VÌ LÀ GHI HÌNH SẴN", "at": 12, "sm": True},
                                           {"text": "KHÔNG AI TRÒ CHUYỆN QUA LẠI", "at": [12, "không"], "acc": True},
                                           {"text": "“sếp” rời cuộc họp → chỉ đạo qua tin nhắn", "at": 13, "sm": True}]},
    {"type": "photo", "at": 14, "img": "hknight", "tone": "color", "move": "in", "veil": 0.5, "illus": "ẢNH MINH HỌA · HỒNG KÔNG, 2013",
     "kin": [{"text": "ARUP · 05.2024", "at": 14, "sm": True}, {"text": "XÁC NHẬN LÀ NẠN NHÂN", "at": [14, "xác"], "acc": True}],
     "label": {"k": "CÔNG TY KỸ THUẬT ARUP (ANH)", "v": "ĐỨNG SAU NHÀ HÁT OPERA SYDNEY", "at": [14, "nhà"]}},
    {"type": "quote", "at": 15, "text": "We can confirm that fake voices and images were used.", "by": "ARUP · QUA CNN, 17.05.2024",
     "lbl": "TRÍCH DỊCH", "qline": 15, "tag": GMT},
    {"type": "kinetic", "at": 16, "items": [{"text": "ANH TA KHÔNG HỀ CẢ TIN", "at": 16, "sm": True},
                                           {"text": "ANH TA NGHI NGỜ", "at": [16, "anh"], "acc": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "NHƯNG ĐỂ KẺ GIAN DẪN VÀO CUỘC KIỂM TRA", "at": 17, "sm": True},
                                           {"text": "KIỂM TRA BẰNG ĐÚNG THỨ ĐÃ BỊ LÀM GIẢ", "at": [17, "kiểm", 1]},
                                           {"text": "KHUÔN MẶT · GIỌNG NÓI", "at": [17, "khuôn"], "acc": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "VỤ LỪA CHỈ LỘ RA", "at": 18, "sm": True},
                                           {"text": "KHI ANH TA TỰ LIÊN HỆ TRỤ SỞ CHÍNH", "at": [18, "khi"], "acc": True}]},
    {"type": "question", "at": 19, "text": "Ở Việt Nam, gọi video để kiểm tra,\ncòn đủ không?"},
]}

# ---------------- CH06 · Cuộc gọi vài giây ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "CUỘC GỌI VÀI GIÂY"}, "bgm": {"mood": "mystery", "gain": 0.5}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "CUỘC GỌI\nVÀI GIÂY", "sub": "HÀ NỘI · 2024 — 2025", "vid": "34081856",
     "titleAt": [0, "Đầu"]},
    {"type": "chat", "at": 1, "head": "MÔ PHỎNG · THEO MÔ TẢ CỦA BKAV", "msgs": [
        {"who": "u", "text": "Ok, mai nói tiếp nhé!", "at": 1},
        {"who": "m", "text": "Ừ, bye bye!", "at": [1, "chào"]},
        {"who": "m", "text": "À khoan… cho mình vay ít tiền được không?", "at": [1, "quay"]},
        {"who": "u", "text": "Gọi video cho mình đã.", "at": 2}]},
    {"type": "kinetic", "at": 3, "vid": "5617952", "illus": VM, "items": [{"text": "GỌI VIDEO: VÀI GIÂY", "at": 3, "acc": True},
                                                                       {"text": "rồi tắt · “mạng chập chờn”", "at": [3, "rồi"], "sm": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "THẤY MẶT · NGHE ĐÚNG GIỌNG", "at": 4, "sm": True},
                                          {"text": "CHỊ CHUYỂN TIỀN", "at": [4, "chị"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "THỰC RA", "at": 5, "sm": True},
                                          {"text": "TÀI KHOẢN FACEBOOK ĐÃ BỊ CHIẾM", "at": [5, "tài"], "acc": True},
                                          {"text": "video giả dựng sẵn · cả mặt lẫn giọng chủ tài khoản", "at": 6, "sm": True}]},
    {"type": "kinetic", "at": 7, "vid": "7280532", "illus": VM, "items": [
        {"text": "BẠN BÈ, NGƯỜI THÂN KHÁC CŨNG BỊ LỪA", "at": 7, "sm": True},
        {"text": "TỔNG CỘNG HÀNG CHỤC TRIỆU ĐỒNG", "at": [7, "tổng"], "acc": True},
        {"text": "theo Bkav · VnEconomy, 02.02.2024", "at": [7, "tổng"], "sm": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "GIỐNG HỒNG KÔNG", "at": 8},
                                          {"text": "NHỎ HƠN · GẦN HƠN", "at": [8, "nhỏ"], "acc": True}]},
    {"type": "question", "at": 9, "text": "Còn bức tranh chung?"},
    {"type": "kinetic", "at": 10, "vid": "31873137", "illus": VM, "items": [
        {"text": "HIỆP HỘI AN NINH MẠNG QUỐC GIA", "at": 10},
        {"text": "KHẢO SÁT TRỰC TUYẾN · MỖI CUỐI NĂM", "at": [10, "khảo"], "sm": True, "acc": True}]},
    {"type": "bars", "at": 11, "title": "TỰ NHẬN LÀ NẠN NHÂN", "unit": "KHẢO SÁT TRỰC TUYẾN NCA · KHÔNG PHẢI MẪU ĐẠI DIỆN",
     "items": [{"k": "2024", "v": 0.4545, "lbl": "1 / 220", "at": [11, "hai"]},
               {"k": "2025", "v": 0.1802, "lbl": "1 / 555", "at": [12, "một"], "acc": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "HIỆP HỘI CHO RẰNG", "at": 13, "sm": True},
                                           {"text": "CHUYÊN ÁN CỦA CÔNG AN", "at": [13, "chuyên"]},
                                           {"text": "+ QUY ĐỊNH XÁC THỰC SINH TRẮC HỌC", "at": [13, "quy"], "acc": True}]},
    {"type": "ledger", "at": 14, "title": "TỪ 01.07.2024 · QĐ 2345", "srcnote": "NGUỒN: NGÂN HÀNG NHÀ NƯỚC (SBV.GOV.VN)", "rows": [
        {"k": "> 10 TRIỆU/LẦN", "v": "SINH TRẮC HỌC", "at": [14, "hơn"]},
        {"k": "> 20 TRIỆU/NGÀY", "v": "SINH TRẮC HỌC", "at": [14, "hay"]},
        {"k": "THƯỜNG GẶP", "v": "QUÉT KHUÔN MẶT", "at": [14, "quét"]}]},
    {"type": "broll", "at": 15, "vid": "8090195", "veil": 0.5, "illus": VM,
     "kin": [{"text": "QUÉT KHUÔN MẶT", "at": 15, "sm": True}, {"text": "CHỨNG MINH ĐIỀU GÌ?", "at": [15, "chứng"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "NGƯỜI CHUYỂN TIỀN = CHÍNH BẠN", "at": 16},
                                           {"text": "GIÚP CHẶN KẺ LẠ DÙNG TÀI KHOẢN", "at": 17, "acc": True}]},
    {"type": "slam", "at": 18, "text": "KHÔNG CHẶN ĐƯỢC\nCHÍNH BẠN", "white": True},
    {"type": "counter", "at": 19, "from": 0, "to": 6000, "prefix": "> ", "suffix": " TỈ Đ",
     "label": "THIỆT HẠI LỪA ĐẢO TRỰC TUYẾN · 11 THÁNG 2025 (ƯỚC TÍNH)",
     "sub": {"text": "THEO BỘ CÔNG AN · QUA VIETNAMNET, 07.01.2026", "at": 19}},
    {"type": "kinetic", "at": 20, "items": [{"text": "KHẢO SÁT TRỰC TUYẾN NCA", "at": 20, "sm": True},
                                           {"text": "CHỈ ≈ 1/3 NẠN NHÂN BÁO CƠ QUAN CHỨC NĂNG", "at": [20, "chỉ"], "acc": True},
                                           {"text": "32,12% · khảo sát 12.2025", "at": [20, "báo"], "sm": True}]},
    {"type": "kinetic", "at": 21, "items": [{"text": "Ở BƯỚC CUỐI CÙNG", "at": 21, "sm": True},
                                           {"text": "VẪN LÀ CHÍNH BẠN", "at": [21, "vẫn"], "acc": True}]},
    {"type": "question", "at": 22, "text": "Vậy bạn cần gì?"},
]}

# ---------------- CH07 · Mật khẩu gia đình ----------------
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "MẬT KHẨU GIA ĐÌNH"}, "bgm": {"mood": "calm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "MẬT KHẨU\nGIA ĐÌNH", "sub": "FBI · 03.12.2024", "vid": "9243207",
     "titleAt": [0, "Tháng"]},
    {"type": "quote", "at": 1, "text": "Create a secret word or phrase with your family to verify their identity.",
     "by": "FBI · PSA I-120324-PSA, 03.12.2024", "lbl": "TRÍCH DỊCH", "qline": 1, "tag": GMT},
    {"type": "kinetic", "at": 2, "items": [{"text": "THỨ MÁY KHÔNG SAO CHÉP ĐƯỢC", "at": 2, "acc": True},
                                          {"text": "không nằm trong đoạn ghi âm nào của bạn trên mạng", "at": [2, "không"], "sm": True}]},
    {"type": "ledger", "at": 3, "title": "VỚI ĐIỀU KIỆN", "rows": [
        {"k": "1", "v": "THỐNG NHẤT KHI GẶP MẶT", "at": [3, "cả"]},
        {"k": "2", "v": "KHÔNG ĐĂNG LÊN MẠNG", "at": [3, "đăng"]},
        {"k": "3", "v": "KHÔNG GÕ VÀO TIN NHẮN", "at": [3, "gõ"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "ĐỪNG CHỌN THỨ NGƯỜI NGOÀI ĐOÁN ĐƯỢC", "at": 4},
                                          {"text": "tên con chó · ngày sinh", "at": [4, "tên"], "sm": True, "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "FBI CŨNG KHUYÊN", "at": 5, "sm": True},
                                          {"text": "HẠN CHẾ ĐĂNG ẢNH VÀ GIỌNG NÓI", "at": [5, "hạn"], "acc": True},
                                          {"text": "để tài khoản mạng xã hội ở chế độ riêng tư", "at": [5, "để"], "sm": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "NÊN LÀM.", "at": 6},
                                          {"text": "NHƯNG ĐỪNG CHỈ TRÔNG VÀO VIỆC GIẤU GIỌNG", "at": [6, "nhưng"], "acc": True}]},
    {"type": "slam", "at": 7, "text": "HÃY DỰA VÀO\nMỘT QUY TRÌNH"},
    {"type": "kinetic", "at": 8, "items": [{"text": "MẬT KHẨU + GẤP · GIẤU · TIỀN", "at": 8, "sm": True},
                                          {"text": "= BA BƯỚC", "at": [8, "ba", 1], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "BƯỚC 1 · DỪNG LẠI", "at": 9, "acc": True},
                                          {"text": "khi nghe thấy gấp, giấu, tiền", "at": [9, "khi"], "sm": True},
                                          {"text": "CÀNG BỊ GIỤC, CÀNG PHẢI CHẬM", "at": [9, "càng"]}]},
    {"type": "broll", "at": 10, "vid": "8060393", "veil": 0.55, "illus": VM,
     "kin": [{"text": "BƯỚC 2 · CÚP MÁY", "at": 10, "acc": True},
             {"text": "tự bấm số đã lưu · đừng gọi lại số vừa gọi tới", "at": [10, "tự"], "sm": True},
             {"text": "không liên lạc được → gọi người nhà khác, bạn bè của họ", "at": 11, "sm": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "BƯỚC 3", "at": 12, "sm": True},
                                           {"text": "HỎI MẬT KHẨU GIA ĐÌNH", "at": [12, "hỏi"], "acc": True}]},
    {"type": "broll", "at": 13, "vid": "9243207", "ms": 6, "veil": 0.5, "illus": VM,
     "kin": [{"text": "KẺ GIAN CÓ THỂ MƯỢN GIỌNG", "at": 13, "sm": True},
             {"text": "NHƯNG KHÔNG BIẾT TỪ CẢ NHÀ NÓI BÊN MÂM CƠM", "at": [13, "nhưng"], "acc": True}]},
    {"type": "broll", "at": 14, "vid": "8872099", "veil": 0.5, "illus": VM,
     "kin": [{"text": "ĐỪNG CHỈ DẶN CON CÁI", "at": 14, "sm": True},
             {"text": "DẶN CẢ BỐ MẸ, ÔNG BÀ", "at": [14, "dặn", 1], "acc": True},
             {"text": "kiểu lừa này từ lâu đã nhắm vào ông bà, bằng giọng của cháu", "at": 15, "sm": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "BÀ DESTEFANO · TỪ HÔM ẤY", "at": 16, "sm": True},
                                           {"text": "NGẠI NGHE SỐ LẠ", "at": [16, "ngại"], "acc": True},
                                           {"text": "im lặng cho tới khi người gọi lên tiếng trước", "at": [16, "im"], "sm": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "BẠN KHÔNG CẦN SỢ ĐẾN THẾ", "at": 17}]},
    {"type": "slam", "at": 18, "text": "BA BƯỚC.\nMỘT TỪ."},
]}

# ---------------- CH08 · Daisy ----------------
CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "DAISY"}, "bgm": {"mood": "epic", "gain": 0.3}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "DAISY", "sub": "BELL LABS · ĐẦU THẬP NIÊN 1960", "bg": "belllabs",
     "titleAt": [0, "Đầu"]},
    {"type": "print", "at": 1, "img": "ibm7090", "tone": "bw", "caption": "IBM 7090 · NASA AMES · 06.09.1961",
     "illus": "ẢNH MINH HỌA · KHÔNG PHẢI CHIẾC MÁY ĐÃ HÁT",
     "side": {"k": "MÁY TÍNH IBM HÁT", "h": "Bài hát đầu tiên\ngiọng tổng hợp", "lines": [
         {"text": "Theo cách *thường được ghi nhận*", "at": 1},
         {"text": "Nguồn vênh: *1960 hay 1961* · IBM 704 / 7090 / 7094", "at": [1, "giọng"]}]}},
    {"type": "print", "at": 2, "img": "daisy", "tone": "bw", "maxH": 600, "caption": "BẢN IN Ở ÚC · SAU 1921",
     "side": {"k": "HARRY DACRE", "h": "“Daisy Bell”", "lines": [{"text": "Viết từ năm *1892*", "at": 2}]}},
    {"type": "kinetic", "at": 3, "bg": "belllabs", "items": [{"text": "GIỌNG NÓ", "at": 3, "sm": True},
                                                           {"text": "RÈ RÈ · ĐỀU ĐỀU", "at": [3, "rè"]},
                                                           {"text": "CHẲNG GIỐNG GIỌNG CỦA AI", "at": [3, "chẳng"], "acc": True}],
     "label": {"k": "BELL LABS · MURRAY HILL", "v": "ẢNH NĂM 1942", "at": 3}},
    {"type": "print", "at": 4, "img": "clarke", "tone": "bw", "caption": "ARTHUR C. CLARKE · 1965",
     "side": {"k": "NHÀ VĂN", "h": "Arthur C.\nClarke", "lines": [
         {"text": "Từng nghe *màn trình diễn ấy*", "at": 4},
         {"text": "→ đưa vào *2001: A Space Odyssey*", "at": [4, "đưa"]}]}},
    {"type": "kinetic", "at": 5, "bg": "ibm7094", "illus": "ẢNH MINH HỌA · IBM 7094", "items": [
        {"text": "VIDEO ĐẦU TIÊN CỦA KÊNH", "at": 5, "sm": True},
        {"text": "NHỚ HAL 9000?", "at": [5, "nhớ"], "acc": True},
        {"text": "khi bị tắt dần, HAL hát lại chính bài Daisy", "at": [5, "khi"], "sm": True}]},
    {"type": "photo", "at": 6, "img": "racknitz", "tone": "bw", "move": "out", "veil": 0.5, "focus": [0.5, 0.6],
     "kin": [{"text": "HƠN 200 NĂM TRƯỚC", "at": 6, "sm": True}, {"text": "NGƯỜI GIẤU TRONG MÁY", "at": [6, "nhờ"], "acc": True}],
     "label": {"k": "RACKNITZ · 1789", "v": "HÌNH VẼ PHỎNG ĐOÁN", "at": 6}},
    {"type": "broll", "at": 7, "vid": "34645273", "ms": 2, "veil": 0.45, "illus": VM,
     "kin": [{"text": "HÔM NAY", "at": 7, "sm": True}, {"text": "GIỌNG NGƯỜI THÂN QUEN", "at": [7, "giọng"]},
             {"text": "BÊN TRONG LÀ CỖ MÁY", "at": [7, "bên"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "GIỌNG NÓI TỪNG LÀ MẬT KHẨU", "at": 8}]},
    {"type": "slam", "at": 9, "text": "MẬT KHẨU ẤY\nĐÃ LỘ"},
    {"type": "kinetic", "at": 10, "items": [{"text": "BÀ DESTEFANO NÓI ĐÚNG", "at": 10, "sm": True},
                                           {"text": "MẸ THÌ NHẬN RA CON MÌNH", "at": [10, "mẹ"], "acc": True}]},
    {"type": "ledger", "at": 11, "title": "THÊM MỘT BƯỚC KIỂM TRA", "rows": [
        {"k": "1", "v": "CÚP MÁY", "at": [11, "cúp"]},
        {"k": "2", "v": "GỌI LẠI", "at": [11, "gọi"]},
        {"k": "3", "v": "MỘT TỪ BÍ MẬT", "at": [11, "bí"]}]},
    {"type": "question", "at": 12, "text": "Nhà bạn đã có\nmật khẩu gia đình chưa?"},
    {"type": "kinetic", "at": 13, "items": [{"text": "ĐỪNG VIẾT TỪ THẬT", "at": 13, "acc": True},
                                           {"text": "vào phần bình luận", "at": [13, "vào"], "sm": True}]},
    {"type": "broll", "at": 14, "vid": "9243207", "ms": 18, "veil": 0.5, "illus": VM,
     "kin": [{"text": "CHỈ CẦN KỂ", "at": 14, "sm": True},
             {"text": "BẠN SẼ NÓI VỚI AI ĐẦU TIÊN?", "at": [14, "bạn"], "acc": True},
             {"text": "BỐ MẸ · VỢ · HAY CON?", "at": [14, "bố"]}]},
]}

SPEC = {
    "title": "AI Giả Giọng Người Thân Để Lừa Tiền: Một Từ Bí Mật Có Thể Cứu Cả Nhà",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "endcardBg": "voder",
    "acc": ["ai", "vall-e", "voder", "kempelen", "fbi", "ftc", "daisy", "deepfake", "giây", "gấp", "giấu", "tiền"],
    "say": SAY, "imgs": IMGS, "chapters": list(CH),
    "youtube": {
        "titles": ["AI Giả Giọng Người Thân Để Lừa Tiền: Một Từ Bí Mật Có Thể Cứu Cả Nhà",
                   "\"Mẹ Ơi, Cứu Con!\" — Khi AI Nói Bằng Giọng Người Thân Của Bạn",
                   "Một Mô Hình AI Chỉ Cần Ba Giây Giọng Mẫu. Đây Là Cách Không Bị Lừa"],
        "summary": "Một người mẹ ở Arizona nghe giọng con gái khóc trong điện thoại, bị đòi một triệu đô la; bốn phút sau, con gái gọi lại "
                   "từ trên giường. Từ cỗ máy biết nói của Kempelen, chiếc Voder năm 1939, tới mô hình VALL-E chỉ cần ba giây giọng mẫu: "
                   "vì sao tai người không còn nhận ra giọng giả, những vụ lừa bằng giọng và hình giả ở Hồng Kông và Việt Nam, "
                   "và ba bước cùng một \"mật khẩu gia đình\" mà FBI khuyên mọi nhà nên có.",
        "more": ["Chưa cơ quan nào xác minh cuộc gọi bà DeStefano nhận được có dùng AI hay không; video không khẳng định điều đó. "
                 "Video không nêu tên dịch vụ nhân bản giọng nào và không hướng dẫn cách làm giả. Lời trích trong video được đọc bằng "
                 "giọng máy của kênh (gắn nhãn GIỌNG MÁY TẠO), không phải ghi âm thật. Số liệu của Hiệp hội An ninh mạng Quốc gia là "
                 "khảo sát trực tuyến, không phải mẫu đại diện."],
        "ch00_title": "Cuộc gọi bốn phút: \"Mẹ ơi, cứu con!\"",
        "chapter_titles": {"ch00": "Mở đầu: cuộc gọi bốn phút ở Arizona (2023)", "ch01": "Cỗ máy biết nói: Kempelen và Voder (1770–1939)",
                           "ch02": "Ba giây: VALL-E và AI nhân bản giọng nói", "ch03": "Tai người nhận ra giọng giả được bao nhiêu?",
                           "ch04": "Vụ DeStefano có thật là AI không?", "ch05": "Hồng Kông: cuộc họp video không có ai thật",
                           "ch06": "Việt Nam: cuộc gọi video vài giây và quét khuôn mặt", "ch07": "Mật khẩu gia đình: ba bước để không bị lừa",
                           "ch08": "Kết: Daisy, bài hát đầu tiên của máy tính"},
        "sources": [
            "https://www.govinfo.gov/content/pkg/CHRG-118shrg52709/html/CHRG-118shrg52709.htm",
            "https://www.ic3.gov/PSA/2024/PSA241203",
            "https://consumer.ftc.gov/consumer-alerts/2023/03/scammers-use-ai-enhance-their-family-emergency-schemes",
            "https://arxiv.org/abs/2301.02111v1",
            "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0285333",
            "https://www.info.gov.hk/gia/general/202406/26/P2024062600192.htm",
            "https://sbv.gov.vn/en/w/sbv622877",
            "https://www.microsoft.com/en-us/research/project/vall-e-x/vall-e-2/",
            "https://openai.com/index/navigating-the-challenges-and-opportunities-of-synthetic-voices/",
            "https://edition.cnn.com/2023/04/29/us/ai-scam-calls-kidnapping-cec/index.html",
            "https://edition.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk/index.html",
            "https://edition.cnn.com/2024/05/16/tech/arup-deepfake-scam-loss-hong-kong-intl-hnk/index.html",
            "https://hongkongfp.com/2024/02/05/multinational-loses-hk200-million-to-deepfake-video-conference-scam-hong-kong-police-say/",
            "https://innovation.consumerreports.org/new-report-do-these-6-ai-voice-cloning-companies-do-enough-to-prevent-misuse/",
            "https://vietnamnet.vn/chi-32-12-nan-nhan-bi-lua-dao-truc-tuyen-co-bao-co-quan-chuc-nang-2479618.html",
            "https://vneconomy.vn/canh-bao-hien-tuong-dung-ai-gia-mao-hinh-anh-giong-noi-de-lua-tien.htm",
            "https://archive.org/details/belltelephonemag19amerrich",
            "https://www.guinnessworldrecords.com/world-records/454935-first-song-performed-using-computer-speech-synthesis",
        ],
        "hashtags": ["AI", "LừaĐảo", "GiảGiọng", "Deepfake", "MindInTheMachine"],
        "tags": ["AI giả giọng", "giả giọng người thân", "lừa đảo bằng AI", "deepfake giọng nói", "lừa đảo qua điện thoại",
                 "mật khẩu gia đình", "nhân bản giọng nói", "trí tuệ nhân tạo", "VALL-E", "FBI", "lừa đảo cuộc gọi video",
                 "deepfake Hồng Kông", "xác thực sinh trắc học", "Voder", "Daisy Bell", "lịch sử công nghệ"],
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
    pk = OUT / "bgm_picks.json"           # nhạc chốt tay: resolve_bgm dùng picks có sẵn, không tự chọn lại
    old = json.loads(pk.read_text(encoding="utf-8")) if pk.exists() else {}
    if old != BGM_PICKS:
        pk.parent.mkdir(parents=True, exist_ok=True)
        pk.write_text(json.dumps(BGM_PICKS, indent=1), encoding="utf-8")
    print(f"spec + {len(CH)} chương")
