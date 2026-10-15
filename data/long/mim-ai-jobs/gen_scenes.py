"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #2 "AI Có Cướp Việc Của Bạn?".

    python data/long/mim-ai-jobs/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (bản 2) + factcheck.md. Dữ kiện + nguồn: docs/channels/mind-in-the-machine/2026-10-07-long-02-research.md.
Ảnh: chỉ PD / CC0 / CC BY (kênh MIM không nhận BY-SA — build_long kiểm lại lúc tải). Clip: Pexels (ngang),
tải bằng `python motion/long/pexels.py get mim-ai-jobs <id> ...`.
Lưu ý ảnh cold open: file X-4/Friden ghi "Publicity photo from Muroc California" -> KHÔNG gắn nhãn Hampton; cảnh mở dùng
ảnh phòng "computer" NACA Langley 1951 (Hampton) có nhãn năm thật, ảnh 1952 gắn nhãn "NACA · 1952".
Nhạc: chốt trong output/long/mim-ai-jobs/bgm_picks.json — 8 bài MIM mới (07/10/2026) + Inspired ở chương kết;
gain từng chương bù độ to (Clean Soul ≈ −27 LUFS, Equatorial Complex ≈ −25 LUFS so với ≈ −11 của các bài khác).
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

IMGS = {
    "langley51": "File:NACA Laboratory Computers Help Compile Handbook (LRC-1951-B701 P-69568).tiff",   # PD · NACA Langley 06.03.1951
    "x4": "File:Langley Women Computer with X-4 with Friden machine (LRC-1952-B701 P-74769).tiff",        # PD · NACA 24.03.1952 (Muroc)
    "langley43": "File:Women Adequately Filling Posts In NACA Laboratory (LRC-1943-B701 P-33025).tiff",   # PD · NACA Langley 1943
    "ibm704": "File:IBM Electronic Data Processing Machine - GPN-2000-001881.jpg",                       # PD · NASA 1957
    "jcards": "File:Jacquard loom cards.jpg",                                                           # CC0 · Robert-brook
    "jloom": "File:PSM V39 D325 Carpet loom with jacquard attachment.jpg",                              # PD · 1891
    "lovelace": "File:Ada Lovelace portrait.jpg",                                                       # PD · A. E. Chalon ~1840
    "luddite": "File:Luddite.jpg",                                                                      # PD · tranh khắc 1812
    "powerloom": "File:Powerloom weaving in 1835.jpg",                                                  # PD · T. Allom 1835
    "keynes": "File:John Maynard Keynes 1929.jpg",                                                     # PD
    "lbj": "File:President Lyndon B. Johnson with reporters on Election Night 1964.jpg",               # PD · LBJ Library (minh hoạ)
    "switchboard": "File:Photograph of Women Working at a Bell System Telephone Switchboard (3660047829).jpg",  # No restrictions · NARA
    "strowger": "File:Strowger switches - Telephone Museum - Waltham, Massachusetts -DSC08180.jpg",      # CC0 · Daderot
    "elevgirl": "File:Elevator girl, Martha Washington Hotel in 1917.jpg",                             # PD · Bain 1917 (minh hoạ)
    "vaughan3": "File:L Dorothy Vaughan M Lessie Hunter R Vivian Adair.jpg",                            # PD · NASA
    "vaughan": "File:Dorothy Vaughan 2.jpg",                                                            # PD · NASA on The Commons
    "eniac2": "File:Two women operating ENIAC (full resolution).jpg",                                   # PD · Lục quân Mỹ 1946
    "eniacrep": "File:Reprogramming ENIAC.png",                                                         # PD · Lục quân Mỹ 1946
    "cardpunch": "File:Card puncher - NARA - 513295.jpg",                                               # PD · NARA
    "punchcard": "File:Blue-punch-card-front-horiz.png",                                                # PD
    "hinton": "File:Geoffrey Hinton - Collision 2023 - Centre Stage RCZ 1307 (cropped).jpg",            # CC BY 2.0 (như video #1)
    "xraypa": "File:Chest Xray PA 3-8-2010.png",                                                        # CC0 · Stillwaterising
    "modern": "File:Modern Times poster.jpg",                                                           # PD · áp phích 1936
    "hfmedal": "File:Hidden Figures Congressional Gold Medal Ceremony (NHQ202409180015).jpg",           # PD · NASA/Joel Kowsky 2024
}

SAY = {   # chữ hiển thị -> cách đọc (phụ đề giữ chữ gốc); "=X" = khớp đúng hoa/thường. Khoá viết thường, NFC.
    "=AI": "ây ai", "hampton": "Hem-tần", "virginia": "Vơ-gin-ni-a", "naca": "Na-ca", "nasa": "Na-xa",
    "=computer": "com-piu-tơ", "computing": "com-piu-tinh", "west": "Uét", "area": "E-ri-a",
    "jacquard": "Gia-ca", "ada": "Ây-đa", "lovelace": "Lớp-lây-xơ", "charles": "Sác-lơ", "babbage": "Ba-bít",
    "nottinghamshire": "Nót-ting-hầm-sơ", "ned": "Nét", "ludd": "Lát", "luddite": "Lát-đai",
    "napoléon": "Na-pô-lê-ông", "napoléon": "Na-pô-lê-ông", "napoleon": "Na-pô-lê-ông",   # NFC + NFD + không dấu
    "york": "Doóc", "new": "Niu", "james": "Giêm", "bessen": "Bét-xần",
    "john": "Giôn", "maynard": "Mây-nợt", "keynes": "Kên-dơ", "lyndon": "Lin-đần", "johnson": "Giôn-xần",
    "linus": "Lai-nớt", "pauling": "Pô-linh", "nobel": "Nô-ben", "oxford": "Ốc-phợt",
    "at&t": "Ây-ti-en-ti", "feigenbaum": "Phai-gần-bom", "daniel": "Đa-ni-en", "gross": "Grốt",
    "=ATM": "Ây-ti-em", "dorothy": "Đô-rô-thi", "vaughan": "Von", "langley": "Lăng-li", "fortran": "Pho-tran",
    "pennsylvania": "Pen-xin-vê-ni-a", "eniac": "Ê-ni-ác", "ibm": "ai bi em", "=704": "bảy không bốn",
    "geoffrey": "Giép-phri", "hinton": "Hin-tần", "toronto": "To-rôn-tô", "x-quang": "ích-quang",
    "works": "Uớc", "progress": "Prô-gret", "=FDA": "Ép-đi-ây", "mayo": "Mây-ô", "clinic": "Cli-ních",
    "times": "Tai-mơ", "budget": "Bát-gít", "lab": "Láp", "yale": "Dêu", "chatgpt": "chát gi pi ti",
    "stanford": "Xtan-phợt", "=ILO": "I-eo-ô", "indonesia": "In-đô-nê-xi-a", "modern": "Mo-đần",
    "charlie": "Sác-li", "chaplin": "Sáp-lin", "jetsons": "Giét-xần", "hollywood": "Hô-li-út",
    "hidden": "Hít-đần", "figures": "Phi-gơ",
}

CH = {}

# ---------------- CH00 · Nghề tên là "máy tính" ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "NGHỀ TÊN LÀ “MÁY TÍNH”"}, "bgm": {"mood": "calm", "gain": 0.14}, "scenes": [
    {"type": "date", "bg": "langley51", "day": "HAMPTON · VIRGINIA", "date": "1952",
     "illus": "ẢNH: PHÒNG “MÁY TÍNH” NACA LANGLEY · 1951"},
    {"type": "photo", "at": 1, "img": "x4", "tone": "bw", "move": "in", "veil": 0.42, "focus": [0.5, 0.45],
     "kin": [{"text": "MỘT CĂN PHÒNG DÀI", "at": 1},
             {"text": "MỖI MÁY · MỘT NGƯỜI PHỤ NỮ", "at": 3, "acc": True},
             {"text": "máy tính cơ · bấm phím · cộng trừ nhân chia", "at": 2, "sm": True}],
     "label": {"k": "ẢNH NACA · 24.03.1952", "v": "BÊN MÁY TÍNH FRIDEN", "at": 2}},
    {"type": "kinetic", "at": 4, "items": [{"text": "NACA", "at": 4, "acc": True},
                                          {"text": "TIỀN THÂN CỦA NASA", "at": [4, "tiền"]},
                                          {"text": "cơ quan nghiên cứu hàng không của Mỹ", "at": [4, "cơ"], "sm": True}]},
    {"type": "photo", "at": 5, "img": "langley51", "tone": "bw", "move": "pan", "veil": 0.45,
     "kin": [{"text": "SỐ LIỆU MÁY BAY THỬ NGHIỆM", "at": 5, "sm": True},
             {"text": "TÍNH · TÍNH · VÀ TÍNH", "at": [5, "tính,"], "acc": True}],
     "label": {"k": "NACA LANGLEY · 1951", "v": "PHÒNG “MÁY TÍNH”", "at": 5}},
    {"type": "kinetic", "at": 6, "items": [{"text": "CHỨC DANH TRÊN GIẤY TỜ", "at": 6, "sm": True},
                                          {"text": "COMPUTER", "at": [6, "computer."], "acc": True}]},
    {"type": "kinetic", "at": 7, "bg": "x4", "items": [{"text": "= MÁY TÍNH", "at": 7, "acc": True, "fx": "pop"}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "HỒI ẤY, “MÁY TÍNH”", "at": 8, "sm": True},
                                          {"text": "CHƯA PHẢI CÁI MÁY", "at": [8, "chưa"]},
                                          {"text": "MÀ LÀ MỘT NGHỀ CỦA CON NGƯỜI", "at": 9, "acc": True}]},
    {"type": "slam", "at": 10, "bg": "langley51", "text": "NGHỀ ẤY\nBIẾN MẤT", "sub": "CHỈ TRONG MỘT THẾ HỆ"},
    {"type": "print", "at": 11, "img": "ibm704", "tone": "bw",
     "side": {"k": "IBM 704 · NASA, 1957", "h": "Cái tên\nđổi chủ", "lines": [
         {"text": "Từ *con người* → sang *cỗ máy*", "at": 11}]}},
    {"type": "question", "at": 12, "bg": "x4", "text": "Còn những người phụ nữ\ntrong căn phòng này?"},
    {"type": "broll", "at": 13, "vid": "9898442", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "HÔM NAY", "at": 13, "sm": True}, {"text": "MỘT CÂU TƯƠNG TỰ · VỀ AI", "at": [13, "câu"], "acc": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "BẠN ĐÃ NGHE AI ĐÓ NÓI", "at": 14},
                                           {"text": "“LẦN NÀY KHÁC.”", "at": [14, "lần"], "acc": True, "fx": "type"}]},
    {"type": "counter", "at": 15, "bg": "luddite", "from": 0, "to": 200, "suffix": " NĂM", "label": "LOÀI NGƯỜI ĐÃ NÓI CÂU ẤY"},
    {"type": "brand", "at": 16, "sub": "AI · VIỆC LÀM · 200 NĂM NỖI SỢ"},
    {"type": "ledger", "at": 17, "title": "BA CHẶNG ĐƯỜNG", "rows": [
        {"k": "1811", "v": "THỢ DỆT ĐẬP MÁY · NƯỚC ANH", "at": 17},
        {"k": "1970s", "v": "TỔNG ĐÀI · CÂY ATM", "at": 18},
        {"k": "2016", "v": "LỜI TIÊN TRI VỀ BÁC SĨ X-QUANG", "at": 19}],
     "total": {"k": "CÂU HỎI", "v": "VÌ SAO?", "at": [19, "Chuyện"]}},
]}

# ---------------- CH01 · Những người đập máy ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "NHỮNG NGƯỜI ĐẬP MÁY"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "NHỮNG NGƯỜI\nĐẬP MÁY", "sub": "1804 — 1813", "bg": "jcards", "titleAt": [0, "Muốn"]},
    {"type": "print", "at": 1, "img": "jloom", "tone": "bw",
     "side": {"k": "JACQUARD · PHÁP", "h": "Khung cửi\nđọc thẻ đục lỗ", "lines": [
         {"text": "Bằng sáng chế *1804*", "at": 1}, {"text": "Đọc lệnh từ *những tấm thẻ*", "at": [1, "đọc"]}]}},
    {"type": "photo", "at": 2, "img": "jcards", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "CÓ LỖ → SỢI NÂNG LÊN", "at": 2}, {"text": "KHÔNG LỖ → SỢI NẰM YÊN", "at": [2, "Chỗ", 1], "acc": True}],
     "label": {"k": "THẺ ĐỤC LỖ", "v": "CỦA KHUNG CỬI JACQUARD", "at": 2}},
    {"type": "print", "at": 3, "img": "lovelace", "tone": "color",
     "side": {"k": "ADA LOVELACE · 1843", "h": "Nhà toán học", "lines": [
         {"text": "*Máy Giải tích* của Charles Babbage", "at": 3},
         {"text": "so với chính *khung cửi Jacquard*", "at": [3, "khung"]}]}},
    {"type": "quote", "at": 4, "bg": "jcards", "text": "…the Analytical Engine weaves algebraical patterns just as the Jacquard-loom weaves flowers and leaves.",
     "by": "ADA LOVELACE · NOTE A, 1843", "lbl": "TRÍCH DỊCH", "qline": 4},
    {"type": "kinetic", "at": 5, "bg": "jcards", "items": [{"text": "HÃY NHỚ NHỮNG TẤM THẺ NÀY", "at": 5, "acc": True},
                                                         {"text": "chúng sẽ còn đi một chặng rất dài", "at": [5, "Chúng"], "sm": True}]},
    {"type": "photo", "at": 6, "img": "powerloom", "tone": "bw", "move": "pan", "veil": 0.5,
     "kin": [{"text": "NƯỚC ANH", "at": 6, "sm": True}, {"text": "MÁY DỆT DỆT RA… NỖI SỢ", "at": [6, "thứ"], "acc": True}],
     "label": {"k": "DỆT BẰNG MÁY · 1835", "v": "TRANH KHẮC T. ALLOM", "at": 6}},
    {"type": "date", "at": 7, "bg": "powerloom", "day": "NOTTINGHAMSHIRE · NƯỚC ANH", "date": "1811",
     "label": {"k": "1811", "v": "THỢ DỆT BẮT ĐẦU ĐẬP MÁY", "at": [7, "đập"]}},
    {"type": "print", "at": 8, "img": "luddite", "tone": "bw",
     "side": {"k": "NED LUDD", "h": "“Thủ lĩnh”\nhuyền thoại", "lines": [
         {"text": "Tranh khắc in năm *1812*", "at": 8}, {"text": "Một nhân vật *không có thật*", "at": [8, "không"]}]}},
    {"type": "slam", "at": 9, "bg": "luddite", "text": "LUDDITE", "sub": "NHỮNG NGƯỜI ĐẬP MÁY", "hitAt": [9, "Luddite."]},
    {"type": "kinetic", "at": 10, "items": [{"text": "NGÀY NAY", "at": 10, "sm": True},
                                           {"text": "LUDDITE = GHÉT CÔNG NGHỆ?", "at": [10, "ghét"]}]},
    {"type": "slam", "at": 11, "text": "HỌ KHÔNG\nGHÉT MÁY", "white": True},
    {"type": "kinetic", "at": 12, "bg": "powerloom", "items": [{"text": "HỌ PHẢN ĐỐI", "at": 12, "sm": True},
                                                             {"text": "MÁY DÙNG ĐỂ ÉP LƯƠNG", "at": [12, "ép"], "acc": True},
                                                             {"text": "VÀ CHO THỢ NGHỈ VIỆC", "at": [12, "nghỉ"]},
                                                             {"text": "chiến tranh với Napoléon · buôn bán đình trệ", "at": [12, "chiến"], "sm": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "ĐẬP CÓ CHỌN LỌC", "at": 13, "acc": True},
                                           {"text": "hiếm khi động tới tài sản khác", "at": [13, "hiếm"], "sm": True},
                                           {"text": "nguồn: The National Archives (Anh)", "at": [13, "tài"], "sm": True}]},
    {"type": "date", "at": 14, "day": "LUẬT MỚI", "date": "1812", "label": {"k": "LUẬT NĂM 1812", "v": "PHÁ MÁY: CÓ THỂ BỊ TỬ HÌNH", "at": [14, "phá"]}},
    {"type": "ledger", "at": 15, "title": "YORK · ĐẦU NĂM 1813", "rows": [
        {"k": "PHIÊN TOÀ", "v": "ĐẶC BIỆT", "at": 15},
        {"k": "BỊ TREO CỔ", "v": "17 NGƯỜI", "at": [15, "mười"]},
        {"k": "VÌ", "v": "GIẾT NGƯỜI · BẠO LOẠN · TRỘM CƯỚP", "at": [15, "giết"]}]},
    {"type": "slam", "at": 16, "text": "HỌ THUA."},
    {"type": "counter", "at": 17, "img": "powerloom", "tone": "bw", "from": 0, "to": 98, "suffix": "%",
     "label": "CÔNG SỨC DỆT MỖI THƯỚC VẢI", "sub": {"text": "MÁY DỆT CƠ KHÍ THẾ KỶ 19 · THEO JAMES BESSEN", "at": 17}},
    {"type": "kinetic", "at": 18, "items": [{"text": "VẬY MÀ", "at": 18, "sm": True},
                                           {"text": "VIỆC LÀM DỆT TRONG NHÀ MÁY TĂNG", "at": [18, "việc"], "acc": True}]},
    {"type": "slam", "at": 19, "bg": "powerloom", "text": "TRONG NHÀ MÁY", "sub": "HÃY ĐỂ Ý BA CHỮ NÀY", "hitAt": [19, "trong"]},
    {"type": "question", "at": 20, "bg": "luddite", "text": "Người được tuyển vào nhà máy\ncó phải người thợ từng cầm búa?"},
    {"type": "kinetic", "at": 21, "bg": "switchboard", "items": [{"text": "PHẢI RẤT LÂU SAU", "at": 21},
                                                               {"text": "mới có người đo bằng số liệu · với một nghề khác", "at": [21, "đo"], "sm": True, "acc": True}]},
]}

# ---------------- CH02 · Lần này khác ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BA LỜI TIÊN TRI “LẦN NÀY KHÁC”"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "LẦN NÀY KHÁC", "sub": "1930 · 1964 · 2013", "vid": "36337620", "titleAt": [0, "Mỗi"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "“LẦN NÀY KHÁC.”", "at": 1, "acc": True, "fx": "type"},
                                          {"text": "BA LỜI TIÊN TRI", "at": [1, "ba"]}]},
    {"type": "date", "at": 2, "bg": "keynes", "day": "LỜI THỨ NHẤT", "date": "1930"},
    {"type": "print", "at": 3, "img": "keynes", "tone": "bw",
     "side": {"k": "JOHN MAYNARD KEYNES", "h": "Nhà kinh tế học\nngười Anh", "lines": [
         {"text": "Bệnh mới: *thất nghiệp vì công nghệ*", "at": [3, "thất"]}]}},
    {"type": "slam", "at": 4, "text": "NHƯNG ÔNG\nLẠC QUAN", "white": True},
    {"type": "ledger", "at": 5, "title": "KEYNES HÌNH DUNG · 100 NĂM SAU", "rows": [
        {"k": "MỨC SỐNG", "v": "× 4 – 8", "at": 5},
        {"k": "TUẦN LÀM", "v": "~15 GIỜ CÓ LẼ LÀ ĐỦ", "at": [5, "mỗi"]}]},
    {"type": "timeline", "at": 6, "items": [{"year": "1930", "text": "Keynes viết", "at": 6},
                                           {"year": "2030", "text": "*100 năm sau*", "at": [6, "2030."]}]},
    {"type": "slam", "at": 7, "text": "HÃY NHỚ\nCÁI HẸN NÀY", "sub": "2030"},
    {"type": "date", "at": 8, "bg": "lbj", "day": "LỜI THỨ HAI", "date": "03.1964"},
    {"type": "photo", "at": 9, "img": "lbj", "tone": "bw", "move": "in", "veil": 0.5, "illus": "ẢNH MINH HỌA · LBJ, ĐÊM BẦU CỬ 1964",
     "kin": [{"text": "BẢN GHI NHỚ GỬI TỔNG THỐNG JOHNSON", "at": 9},
             {"text": "có chữ ký của Linus Pauling · người đoạt 2 giải Nobel", "at": [9, "Linus"], "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "LỜI CẢNH BÁO · 1964", "at": 10, "sm": True},
                                           {"text": "THẤT NGHIỆP HÀNG LOẠT", "at": [10, "thất"], "acc": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "HAI NĂM SAU · 1966", "at": 11},
                                           {"text": "ỦY BAN QUỐC GIA VỀ TỰ ĐỘNG HOÁ", "at": [11, "uỷ"], "acc": True},
                                           {"text": "do chính quyền Johnson lập ra từ năm 1964", "at": [11, "chính"], "sm": True}]},
    {"type": "quote", "at": 12, "bg": "lbj", "text": "…technology eliminates jobs, not work.",
     "by": "BÁO CÁO ỦY BAN · 02.1966 · QUA D. AUTOR (2015)", "lbl": "DIỄN Ý", "qline": 12},
    {"type": "kinetic", "at": 13, "items": [{"text": "LỜI THỨ BA", "at": 13, "acc": True},
                                           {"text": "có lẽ bạn đã từng nghe", "at": [13, "có"], "sm": True}]},
    {"type": "date", "at": 14, "day": "ĐẠI HỌC OXFORD", "date": "2013", "label": {"k": "FREY & OSBORNE", "v": "XEM XÉT 702 NGHỀ Ở MỸ", "at": [14, "bảy"]}},
    {"type": "counter", "at": 15, "from": 0, "to": 47, "suffix": "%", "label": "VIỆC LÀM Ở MỸ · NHÓM RỦI RO CAO",
     "sub": {"text": "“CÓ THỂ” BỊ MÁY TÍNH LÀM THAY · CÓ LẼ TRONG 1–2 THẬP KỶ", "at": [15, "có"]}},
    {"type": "slam", "at": 16, "text": "1 – 2 THẬP KỶ", "sub": "HÃY NHỚ CON SỐ NÀY"},
    {"type": "timeline", "at": 17, "items": [{"year": "1930", "text": "Keynes", "at": 17},
                                            {"year": "1964", "text": "Bản ghi nhớ", "at": [17, "Ba", 1]},
                                            {"year": "2013", "text": "Oxford", "at": [17, "khác"]}]},
    {"type": "question", "at": 18, "bg": "powerloom", "text": "Khi máy thật sự thắng,\nchuyện gì xảy ra với con người?"},
]}

# ---------------- CH03 · Cô tổng đài và người lái thang máy ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CÔ TỔNG ĐÀI VÀ NGƯỜI LÁI THANG MÁY"}, "bgm": {"mood": "curious", "gain": 0.16}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CÔ TỔNG ĐÀI\nVÀ NGƯỜI LÁI THANG MÁY", "sub": "1920 — 1945", "bg": "switchboard", "titleAt": [0, "Đầu"]},
    {"type": "photo", "at": 1, "img": "switchboard", "tone": "bw", "move": "in", "veil": 0.42,
     "kin": [{"text": "CẮM DÂY · NỐI MÁY", "at": 1, "acc": True}],
     "label": {"k": "TỔNG ĐÀI BELL SYSTEM", "v": "ẢNH LƯU TRỮ QUỐC GIA MỸ", "at": 1}},
    {"type": "kinetic", "at": 2, "items": [{"text": "MỘT TRONG NHỮNG NGHỀ PHỔ BIẾN NHẤT", "at": 2},
                                          {"text": "CỦA PHỤ NỮ MỸ", "at": [2, "phụ"], "acc": True}]},
    {"type": "date", "at": 3, "bg": "strowger", "day": "AT&T · TỔNG ĐÀI CƠ KHÍ", "date": "1920 – 1940",
     "label": {"k": "AT&T · 1920 – 1940", "v": "HƠN MỘT NỬA MẠNG ĐIỆN THOẠI MỸ", "at": [3, "hơn"]}},
    {"type": "print", "at": 4, "img": "strowger", "tone": "color",
     "side": {"k": "BỘ CHUYỂN MẠCH STROWGER", "h": "Tổng đài\ncơ khí", "lines": [
         {"text": "Một trong những khoản *đầu tư tự động hoá lớn nhất*", "at": 4}]}},
    {"type": "slam", "at": 5, "text": "PHẦN LỚN\nCÔNG VIỆC BIẾN MẤT"},
    {"type": "kinetic", "at": 6, "items": [{"text": "GẦN MỘT THẾ KỶ SAU", "at": 6},
                                          {"text": "JAMES FEIGENBAUM · DANIEL GROSS", "at": [6, "James"], "acc": True},
                                          {"text": "lần theo từng người qua các cuộc điều tra dân số", "at": [6, "lần"], "sm": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "KẾT QUẢ · 2024", "at": 7, "sm": True},
                                          {"text": "HAI MẶT", "at": [7, "hai"], "acc": True}]},
    {"type": "ledger", "at": 8, "title": "FEIGENBAUM & GROSS · 2024", "rows": [
        {"k": "LỚP ĐẾN SAU", "v": "KHÔNG THIẾU VIỆC", "at": 8},
        {"k": "→", "v": "VĂN PHÒNG · DỊCH VỤ · NGHỀ MỚI", "at": 9},
        {"k": "NGƯỜI ĐANG LÀM", "v": "CHỊU THIỆT NHẤT", "at": 10},
        {"k": "10 NĂM SAU", "v": "LƯƠNG THẤP HƠN / THÔI VIỆC", "at": 11}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "CÂU HỎI TỪ THỜI ĐẬP MÁY", "at": 12, "sm": True},
                                           {"text": "ĐÃ CÓ CÂU TRẢ LỜI", "at": [12, "đã"], "acc": True},
                                           {"text": "ít nhất cho một nghề", "at": [12, "ít"], "sm": True}]},
    {"type": "kinetic", "at": 13, "bg": "switchboard", "items": [{"text": "LỚP ĐẾN SAU: VẪN ỔN", "at": 13},
                                                                {"text": "NGƯỜI ĐỨNG ĐÚNG CHỖ CỖ MÁY ĐI QUA: TRẢ GIÁ", "at": [13, "Nhưng"], "acc": True}]},
    {"type": "question", "at": 14, "bg": "switchboard", "text": "Người trả giá: người đang làm,\nhay người sắp vào nghề?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "TỚI THỜI AI", "at": 15, "acc": True},
                                           {"text": "câu trả lời có thể sẽ khác", "at": [15, "câu"], "sm": True}]},
    {"type": "slam", "at": 16, "text": "MÁY KHÔNG THẮNG CHỈ NHỜ GIỎI"},
    {"type": "print", "at": 17, "img": "elevgirl", "tone": "bw", "illus": "ẢNH MINH HỌA · NGƯỜI LÁI THANG MÁY, 1917",
     "side": {"k": "THANG MÁY KHÔNG NGƯỜI LÁI", "h": "Có từ\nkhoảng 1900", "lines": [
         {"text": "Người ta bước vào, *không thấy ai điều khiển*", "at": [17, "bước"]},
         {"text": "… rồi lại *bước ra*", "at": [17, "ra."]}]}},
    {"type": "date", "at": 18, "day": "NEW YORK · ĐÌNH CÔNG", "date": "1945",
     "label": {"k": "ĐÌNH CÔNG CỦA NGƯỜI LÁI THANG", "v": "1,5 TRIỆU NHÂN VIÊN VĂN PHÒNG KHÔNG TỚI ĐƯỢC CHỖ LÀM", "at": [18, "một"]}},
    {"type": "broll", "at": 19, "vid": "7706076", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "TỪ LÚC RA ĐỜI → LÚC QUEN DÙNG", "at": 19, "sm": True},
             {"text": "HƠN 50 NĂM", "at": [19, "hơn"], "acc": True}]},
]}

# ---------------- CH04 · Nghịch lý cây ATM ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "NGHỊCH LÝ CÂY ATM"}, "bgm": {"mood": "upbeat", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "NGHỊCH LÝ\nCÂY ATM", "sub": "THẬP NIÊN 70 — 2035", "vid": "3876885", "titleAt": [0, "Giờ"]},
    {"type": "broll", "at": 1, "vid": "5849599", "veil": 0.45, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "ATM Ở MỸ", "at": 1}, {"text": "TỪ THẬP NIÊN 70", "at": [1, "thập"], "acc": True}]},
    {"type": "counter", "at": 2, "vid": "3876885", "ms": 6, "illus": "VIDEO MINH HỌA", "from": 0, "to": 400000, "prefix": "> ", "label": "MÁY ATM Ở MỸ · 2015"},
    {"type": "kinetic", "at": 3, "items": [{"text": "BẠN SẼ ĐOÁN", "at": 3, "sm": True},
                                          {"text": "GIAO DỊCH VIÊN… TIÊU RỒI?", "at": [3, "giao"], "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "THEO JAMES BESSEN", "at": 4, "sm": True},
                                          {"text": "TRONG LÚC ATM LAN RỘNG", "at": [4, "trong"]},
                                          {"text": "GIAO DỊCH VIÊN: KHÔNG HỀ GIẢM", "at": [4, "không"], "acc": True}]},
    {"type": "question", "at": 5, "text": "Vì sao?"},
    {"type": "bars", "at": 6, "title": "GIAO DỊCH VIÊN CẦN CHO MỘT CHI NHÁNH ĐÔ THỊ", "items": [
        {"k": "1988", "v": 20, "lbl": "20", "at": [6, "hai"]}, {"k": "2004", "v": 13, "lbl": "13", "at": [6, "mười"], "acc": True}]},
    {"type": "counter", "at": 7, "from": 0, "to": 43, "prefix": "+", "suffix": "%",
     "label": "SỐ CHI NHÁNH NGÂN HÀNG Ở ĐÔ THỊ", "sub": {"text": "CHI NHÁNH RẺ HƠN → MỞ THÊM", "at": 7}},
    {"type": "kinetic", "at": 8, "vid": "5849599", "ms": 4, "illus": "VIDEO MINH HỌA", "items": [{"text": "MÁY: ĐẾM TIỀN", "at": 8},
                                                      {"text": "NGƯỜI: TƯ VẤN · GIỚI THIỆU DỊCH VỤ", "at": [8, "Còn"], "acc": True}]},
    {"type": "slam", "at": 9, "text": "ĐOẠN KẾT\nTHỨ HAI"},
    {"type": "bars", "at": 10, "title": "GIAO DỊCH VIÊN NGÂN HÀNG Ở MỸ · BLS", "items": [
        {"k": "2014", "v": 520.5, "lbl": "520,5 NGHÌN", "at": [10, "năm", 1]},
        {"k": "2025", "v": 339.2, "lbl": "339,2 NGHÌN", "at": 11, "acc": True}],
     "stamp": {"text": "−34,8%", "at": [11, "Mất"], "x": 760, "y": 430, "rot": -8}},
    {"type": "broll", "at": 12, "vid": "3876885", "ms": 14, "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "DỰ BÁO CỦA BLS · 2025 → 2035", "at": 12, "sm": True},
             {"text": "−13% NỮA", "at": [12, "mười"], "acc": True},
             {"text": "séc gửi qua điện thoại · ít ai ra quầy · ATM đời mới", "at": [12, "gửi"], "sm": True}]},
    {"type": "broll", "at": 13, "vid": "7535106", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "MỘT CÂY ATM · MỘT CHIẾC ĐIỆN THOẠI", "at": 13, "sm": True},
             {"text": "ATM: THAY MỘT THAO TÁC", "at": 14},
             {"text": "ĐIỆN THOẠI: ĐỔI CÁCH KHÁCH HÀNG CƯ XỬ", "at": 15, "acc": True}]},
    {"type": "question", "at": 16, "bg": "x4", "text": "Còn những “máy tính”\nbằng xương bằng thịt?"},
]}

# ---------------- CH05 · Những "máy tính" đã đi đâu? ----------------
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "NHỮNG “MÁY TÍNH” ĐÃ ĐI ĐÂU?"}, "bgm": {"mood": "warm", "gain": 0.3}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "NHỮNG “MÁY TÍNH”\nĐÃ ĐI ĐÂU?", "sub": "1943 — 1971", "bg": "langley43", "titleAt": [0, "Tháng"]},
    {"type": "print", "at": 1, "img": "vaughan3", "tone": "bw", "caption": "TRÁI: DOROTHY VAUGHAN · L. HUNTER · V. ADAIR",
     "side": {"k": "WEST AREA COMPUTING", "h": "Nữ toán học gia\nda đen", "lines": [
         {"text": "Bị buộc làm việc *tách riêng*", "at": [1, "bị"]},
         {"text": "theo *luật phân biệt chủng tộc*", "at": [1, "luật"]}]}},
    {"type": "date", "at": 2, "bg": "vaughan", "day": "DOROTHY VAUGHAN", "date": "1949",
     "label": {"k": "NĂM 1949", "v": "NGƯỜI GIÁM SÁT DA ĐEN ĐẦU TIÊN CỦA NACA", "at": [2, "người"]}},
    {"type": "kinetic", "at": 3, "items": [{"text": "1958: NACA → NASA", "at": 3, "acc": True},
                                          {"text": "văn phòng tách biệt bị xoá bỏ", "at": [3, "Những"], "sm": True}]},
    {"type": "print", "at": 4, "img": "vaughan", "tone": "bw",
     "side": {"k": "DOROTHY VAUGHAN", "h": "Ở tuổi 48", "lines": [
         {"text": "Sang *Phòng Phân tích và Tính toán*", "at": [4, "Phòng"]},
         {"text": "Lập trình viên *FORTRAN* thành thạo", "at": [4, "lập"]}]}},
    {"type": "kinetic", "at": 5, "bg": "ibm704", "items": [{"text": "NGÔN NGỮ CỦA CHÍNH CỖ MÁY", "at": 5, "acc": True},
                                                         {"text": "đang làm thay việc của nhóm bà", "at": [5, "đang"], "sm": True}]},
    {"type": "slam", "at": 6, "text": "ĐỪNG VỘI KỂ\nCHUYỆN CỔ TÍCH", "white": True},
    {"type": "kinetic", "at": 7, "bg": "vaughan3", "items": [{"text": "THEO NASA", "at": 7, "sm": True},
                                                           {"text": "KHÔNG ĐƯỢC GIAO LẠI VỊ TRÍ QUẢN LÝ NÀO", "at": [7, "không"], "acc": True},
                                                           {"text": "cho tới khi nghỉ hưu · 1971", "at": [7, "nghỉ"], "sm": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "CHUYỂN NGHỀ THÀNH CÔNG", "at": 8},
                                          {"text": "NHƯNG KHÔNG PHẢI KHÔNG CÓ GIÁ", "at": [8, "Nhưng"], "acc": True}]},
    {"type": "kinetic", "at": 9, "bg": "langley51", "items": [{"text": "KHÔNG CHỈ Ở LANGLEY", "at": 9, "acc": True}]},
    {"type": "kinetic", "at": 10, "bg": "eniac2", "items": [{"text": "ĐẠI HỌC PENNSYLVANIA · THẾ CHIẾN II", "at": 10, "sm": True},
                                                          {"text": "PHỤ NỮ LÀM “MÁY TÍNH”", "at": [10, "phụ"]},
                                                          {"text": "tính quỹ đạo đạn pháo", "at": [10, "quỹ"], "sm": True, "acc": True, "fx": "rise"}]},
    {"type": "photo", "at": 11, "img": "eniac2", "tone": "bw", "move": "in", "veil": 0.45,
     "kin": [{"text": "6 LẬP TRÌNH VIÊN ĐẦU TIÊN", "at": 11}, {"text": "ENIAC · CÔNG BỐ 02.1946", "at": [11, "công"], "acc": True}],
     "label": {"k": "ENIAC · 1946", "v": "ẢNH LỤC QUÂN MỸ", "at": 11}},
    {"type": "bars", "at": 12, "bg": "eniacrep", "title": "MỘT BÀI TOÁN ĐẠN ĐẠO", "items": [
        {"k": "TÍNH TAY", "v": 43200, "lbl": "12 GIỜ", "at": [12, "mười"]},
        {"k": "ENIAC", "v": 30, "lbl": "30 GIÂY", "at": [12, "ba"], "acc": True}]},
    {"type": "photo", "at": 13, "img": "jcards", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "CÒN NHỮNG TẤM THẺ ĐỤC LỖ?", "at": 13, "acc": True}]},
    {"type": "print", "at": 14, "img": "cardpunch", "tone": "bw",
     "side": {"k": "ĐIỀU TRA DÂN SỐ MỸ", "h": "Máy\nđục thẻ", "lines": [
         {"text": "*Có lỗ* là có · *không lỗ* là không", "at": 14}]}},
    {"type": "print", "at": 15, "img": "ibm704", "tone": "bw",
     "side": {"k": "IBM 704 · NASA, 1957", "h": "Ở video trước\ncủa kênh", "lines": [
         {"text": "Cũng nuôi bằng *thẻ đục lỗ*", "at": 15}]}},
    {"type": "slam", "at": 16, "bg": "punchcard", "text": "TỪ SỢI VẢI,\nTỚI CON SỐ."},
    {"type": "kinetic", "at": 17, "bg": "vaughan3", "items": [{"text": "MỘT VÀI NGƯỜI NHƯ HỌ", "at": 17, "acc": True},
                                                            {"text": "nghề biến mất · người đi theo chính cỗ máy đã thay họ", "at": 18, "sm": True}]},
    {"type": "kinetic", "at": 19, "bg": "xraypa", "items": [{"text": "2016", "at": 19, "acc": True},
                                                          {"text": "“CHA ĐẺ” CỦA HỌC SÂU", "at": [19, "cha"]},
                                                          {"text": "một lời tiên tri về một nghề rất cụ thể", "at": [19, "lời"], "sm": True}]},
]}

# ---------------- CH06 · Lời tiên tri về bác sĩ X-quang ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "LỜI TIÊN TRI VỀ BÁC SĨ X-QUANG"}, "bgm": {"mood": "mystery", "gain": 0.5}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "LỜI TIÊN TRI\nVỀ BÁC SĨ X-QUANG", "sub": "2016 — 2026", "bg": "hinton", "titleAt": [0, "Năm"]},
    {"type": "quote", "at": 1, "bg": "hinton", "text": "People should stop training radiologists now.",
     "by": "GEOFFREY HINTON · TORONTO, 2016", "lbl": "TRÍCH DỊCH", "qline": 1},
    {"type": "print", "at": 2, "img": "hinton", "tone": "color",
     "side": {"k": "HINTON · DIỄN Ý", "h": "Nobel Vật lý\n2024", "lines": [
         {"text": "Trong khoảng *5 năm*", "at": 2},
         {"text": "có thể là *10 năm*", "at": [2, "có"]},
         {"text": "học sâu sẽ *làm tốt hơn* bác sĩ X-quang", "at": [2, "học"]}]}},
    {"type": "photo", "at": 3, "img": "xraypa", "tone": "color", "move": "in", "veil": 0.4, "illus": "ẢNH MINH HỌA",
     "kin": [{"text": "ĐỌC PHIM = NHÌN ẢNH, TÌM BẤT THƯỜNG", "at": 3},
             {"text": "đúng thứ máy vừa học giỏi", "at": [3, "đúng"], "sm": True, "acc": True}]},
    {"type": "slam", "at": 4, "text": "MỘT PHẦN,\nÔNG ĐÃ ĐÚNG"},
    {"type": "counter", "at": 5, "bg": "xraypa", "from": 0, "to": 700, "prefix": "> ", "label": "MÔ HÌNH AI X-QUANG ĐƯỢC FDA CHO PHÉP",
     "sub": {"text": "≈ 3/4 SỐ THIẾT BỊ Y TẾ CÓ AI · THEO WORKS IN PROGRESS", "at": [5, "chiếm"]}},
    {"type": "question", "at": 6, "bg": "xraypa", "text": "Mười năm sau,\nnghề bác sĩ X-quang ra sao?"},
    {"type": "counter", "at": 7, "bg": "xraypa", "from": 0, "to": 1208, "label": "SUẤT NỘI TRÚ X-QUANG Ở MỸ · 2025 · KỶ LỤC"},
    {"type": "broll", "at": 8, "vid": "7579841", "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "≈ $520.000 / NĂM", "at": 8, "acc": True},
             {"text": "thu nhập trung bình · cao thứ hai trong các chuyên khoa", "at": [8, "cao"], "sm": True}]},
    {"type": "counter", "at": 9, "bg": "hinton", "from": 0, "to": 55, "prefix": "+", "suffix": "%",
     "label": "BÁC SĨ X-QUANG Ở MAYO CLINIC · TỪ 2016", "sub": {"text": "THEO BÁO NEW YORK TIMES", "at": 9}},
    {"type": "question", "at": 10, "text": "Chuyện gì đã xảy ra?"},
    {"type": "counter", "at": 11, "vid": "5724099", "illus": "VIDEO MINH HỌA", "from": 0, "to": 36, "suffix": "%",
     "label": "THỜI GIAN TRỰC TIẾP ĐỌC ẢNH", "sub": {"text": "NGHIÊN CỨU 2012 · 3 BỆNH VIỆN", "at": 11}},
    {"type": "slam", "at": 12, "text": "MỘT PHẦN\nCỦA MỘT VIỆC", "sub": "CHƯA PHẢI CẢ NGHỀ"},
    {"type": "kinetic", "at": 13, "bg": "hinton", "items": [{"text": "2025 · THEO BÁO NEW YORK TIMES", "at": 13, "sm": True},
                                                          {"text": "HINTON: ĐÃ NÓI QUÁ RỘNG", "at": [13, "nói", 1]},
                                                          {"text": "SAI THỜI ĐIỂM, KHÔNG SAI HƯỚNG ĐI", "at": 14, "acc": True}]},
    {"type": "question", "at": 15, "bg": "xraypa", "text": "Dữ liệu nói gì\nvề chính lúc này?"},
]}

# ---------------- CH07 · Lần này có khác không? ----------------
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "LẦN NÀY CÓ KHÁC KHÔNG?"}, "bgm": {"mood": "calm", "gain": 0.55}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "LẦN NÀY\nCÓ KHÁC KHÔNG?", "sub": "2013 — 2026", "vid": "37439076", "titleAt": [0, "Quay"]},
    {"type": "timeline", "at": 1, "items": [{"year": "2013", "text": "Oxford: 1–2 thập kỷ", "at": 1},
                                           {"year": "2026", "text": "*13 năm*", "at": [1, "mười"]},
                                           {"year": "≈ 2033", "text": "mốc 2 thập kỷ · chưa tới", "at": [1, "mốc"]}]},
    {"type": "bars", "at": 2, "title": "VIỆC LÀM NGOÀI NÔNG NGHIỆP Ở MỸ", "unit": "FRED · PAYEMS", "items": [
        {"k": "09.2013", "v": 136.8, "lbl": "≈ 137 TRIỆU", "at": [2, "một"]},
        {"k": "09.2026 (SƠ BỘ)", "v": 159.0, "lbl": "≈ 159 TRIỆU", "at": 3, "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "NÓI CHO CÔNG BẰNG", "at": 4, "sm": True},
                                          {"text": "OXFORD: “CÓ THỂ BỊ TỰ ĐỘNG HOÁ”", "at": [4, "bài"]},
                                          {"text": "KHÔNG ĐOÁN BAO NHIÊU NGƯỜI THẤT NGHIỆP", "at": [4, "chứ"], "acc": True}]},
    {"type": "question", "at": 5, "vid": "9898442", "ms": 1, "text": "Còn AI tạo sinh thì sao?"},
    {"type": "date", "at": 6, "day": "YALE BUDGET LAB", "date": "10.2025",
     "label": {"k": "33 THÁNG SAU CHATGPT", "v": "CHƯA THẤY THỊ TRƯỜNG LAO ĐỘNG MỸ XÁO TRỘN RÕ RỆT", "at": [6, "ba"]}},
    {"type": "date", "at": 7, "day": "ĐẠI HỌC STANFORD · DỮ LIỆU BẢNG LƯƠNG", "date": "08.2026",
     "label": {"k": "STANFORD DIGITAL ECONOMY LAB", "v": "MỘT CHI TIẾT KHÁC", "at": [7, "một", 1]}},
    {"type": "slam", "at": 8, "text": "KHÔNG MẤT VIỆC\nTRÊN DIỆN RỘNG", "sub": "STANFORD · 2026"},
    {"type": "bars", "at": 9, "title": "NGƯỜI 22–25 TUỔI · NGHỀ PHƠI NHIỄM AI CAO",
     "unit": "MÔ TẢ, CHƯA PHẢI NHÂN QUẢ", "items": [
        {"k": "07.2025", "v": 15, "lbl": "≈ −15%", "at": 10},
        {"k": "06.2026", "v": 19, "lbl": "≈ −19%", "at": [9, "mười"], "acc": True},
        {"k": "NGƯỜI NHIỀU KINH NGHIỆM", "v": 0, "lbl": "KHÔNG CÓ", "at": 11}]},
    {"type": "broll", "at": 12, "vid": "7685209", "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "KHÔNG PHẢI SA THẢI", "at": 12, "sm": True},
             {"text": "MÀ LÀ TUYỂN ÍT NGƯỜI TRẺ HƠN", "at": [12, "mà"], "acc": True},
             {"text": "nghề dựa vào kiến thức đã viết thành văn bản", "at": 13, "sm": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "CHÍNH CÁC TÁC GIẢ NHẤN MẠNH", "at": 14, "sm": True},
                                           {"text": "MÔ TẢ, CHƯA PHẢI NHÂN QUẢ", "at": [14, "mô"], "acc": True}]},
    {"type": "photo", "at": 15, "img": "switchboard", "tone": "bw", "move": "out", "veil": 0.5,
     "kin": [{"text": "CÒN NHỚ CÔ TỔNG ĐÀI?", "at": 15, "acc": True}]},
    {"type": "ledger", "at": 16, "title": "HỒI ẤY · CÔ TỔNG ĐÀI", "rows": [
        {"k": "NGƯỜI ĐANG LÀM", "v": "CHỊU THIỆT", "at": 16},
        {"k": "LỚP ĐẾN SAU", "v": "VẪN ỔN", "at": [16, "còn"]}]},
    {"type": "broll", "at": 17, "vid": "37439076", "ms": 3, "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "LẦN NÀY · NẾU XU HƯỚNG ẤY ĐÚNG", "at": 17, "sm": True},
             {"text": "CỬA VÀO NGHỀ KHÉP LẠI TRƯỚC", "at": [17, "cánh"], "acc": True},
             {"text": "CÁI GIÁ CÓ THỂ ĐANG CHUYỂN: NGƯỜI CŨ → NGƯỜI MỚI", "at": 18}]},
    {"type": "question", "at": 19, "vid": "31359566", "text": "Còn ở Việt Nam?"},
    {"type": "broll", "at": 20, "vid": "31359566", "ms": 4, "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "ILO · 2016", "at": 20, "sm": True},
             {"text": "CAMPUCHIA · INDONESIA · VIỆT NAM", "at": [20, "Campuchia,"]},
             {"text": "64–88% LAO ĐỘNG DỆT MAY, GIÀY DA: RỦI RO CAO", "at": [20, "sáu"], "acc": True}]},
    {"type": "kinetic", "at": 21, "items": [{"text": "CÁC TÁC GIẢ NÓI RÕ", "at": 21, "sm": True},
                                           {"text": "RỦI RO ≠ CHẮC CHẮN", "at": [21, "rủi"], "acc": True}]},
    {"type": "counter", "at": 22, "vid": "18092543", "from": 511364, "to": 2984980,
     "label": "LAO ĐỘNG CHÍNH THỨC · MAY MẶC & GIÀY DA VIỆT NAM · 2017",
     "sub": {"text": "GẤP GẦN 6 LẦN SO VỚI KHOẢNG NĂM 2000 (511.364)", "at": [22, "gấp"]}},
    {"type": "kinetic", "at": 23, "items": [{"text": "ILO–IFC · 2020", "at": 23, "sm": True},
                                           {"text": "TỰ ĐỘNG HOÁ NGÀNH MAY: CÒN HẠN CHẾ", "at": [23, "tự"]},
                                           {"text": "ÍT NHẤT TỚI 2020: CẢNH BÁO CHƯA THÀNH SỰ THẬT", "at": 24, "acc": True}]},
    {"type": "kinetic", "at": 25, "items": [{"text": "“LẦN NÀY CÓ KHÁC KHÔNG?”", "at": 25, "fx": "type"},
                                           {"text": "CHƯA AI BIẾT CHẮC", "at": [25, "chưa"], "acc": True}]},
]}

# ---------------- CH08 · Năm 2030 của Keynes ----------------
CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "NĂM 2030 CỦA KEYNES"}, "bgm": {"mood": "epic", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "NĂM 2030\nCỦA KEYNES", "sub": "1930 → 2030", "bg": "keynes", "titleAt": [0, "Nỗi"]},
    {"type": "print", "at": 1, "img": "modern", "tone": "bw",
     "side": {"k": "MODERN TIMES · 1936", "h": "Charlie Chaplin", "lines": [
         {"text": "Bị cuốn vào *trong lòng cỗ máy*", "at": [1, "cuốn"]}]}},
    {"type": "kinetic", "at": 2, "items": [{"text": "THE JETSONS · 1962", "at": 2, "acc": True},
                                          {"text": "ông bố tương lai đi làm chỉ để bấm nút", "at": [2, "ông"], "sm": True}]},
    {"type": "photo", "at": 3, "img": "hfmedal", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "HIDDEN FIGURES · 2016", "at": 3, "acc": True},
             {"text": "những “máy tính” ở Langley lên phim Hollywood", "at": [3, "những"], "sm": True}],
     "label": {"k": "HUY CHƯƠNG VÀNG QUỐC HỘI MỸ · 2024", "v": "TƯỞNG NIỆM DOROTHY VAUGHAN", "at": [3, "Hollywood"]}},
    {"type": "print", "at": 4, "img": "keynes", "tone": "bw",
     "side": {"k": "KEYNES · 1930", "h": "Tuần làm\n15 giờ?", "lines": [
         {"text": "Ông *hình dung*: có thể là đủ", "at": [4, "Ông"]}]}},
    {"type": "counter", "at": 5, "bg": "keynes", "from": 0, "to": 4, "suffix": " NĂM",
     "label": "CÒN LẠI TỚI MỐC 2030", "sub": {"text": "MỐC TRĂM NĂM: 2030", "at": 5}},
    {"type": "kinetic", "at": 6, "bg": "lbj", "items": [{"text": "ỦY BAN 1966: ĐÚNG MỘT NỬA", "at": 6},
                                                      {"text": "XOÁ CÔNG VIỆC, KHÔNG XOÁ LAO ĐỘNG", "at": [6, "công"], "acc": True}]},
    {"type": "photo", "at": 7, "img": "switchboard", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "NỬA CÒN LẠI: CÔ TỔNG ĐÀI", "at": 7},
             {"text": "SAI CHỖ · SAI LÚC · VẪN TRẢ GIÁ", "at": [7, "người"], "acc": True}]},
    {"type": "timeline", "at": 8, "bg": "jcards", "items": [{"year": "1804", "text": "Sợi vải · *Jacquard*", "at": 8},
                                                          {"year": "1946", "text": "Con số · *ENIAC*", "at": [8, "con"]},
                                                          {"year": "HÔM NAY", "text": "*Ô chat*", "at": [8, "ô"]}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "VÀ MỖI LẦN…", "at": 9, "sm": True},
                                          {"text": "“LẦN NÀY KHÁC?”", "at": [9, "lần"], "acc": True, "fx": "type"}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "CÓ THỂ HỌ ĐÚNG.", "at": 10},
                                           {"text": "CÓ THỂ KHÔNG.", "at": [10, "Có", 1], "acc": True}]},
    {"type": "broll", "at": 11, "vid": "6913262", "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "DỮ LIỆU BAN ĐẦU GỢI Ý", "at": 11, "sm": True},
             {"text": "AI CHẠM TỚI TRƯỚC: NGƯỜI TRẺ MỚI VÀO NGHỀ", "at": [11, "người"], "acc": True},
             {"text": "ở công việc dựa vào kiến thức đã viết thành văn bản", "at": [11, "công"], "sm": True}]},
    {"type": "broll", "at": 12, "vid": "6214598", "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "MỘT CÂU HỎI CHO BẠN", "at": 12, "acc": True},
             {"text": "trả lời thật lòng ở phần bình luận", "at": [12, "trả"], "sm": True}]},
    {"type": "question", "at": 13, "bg": "punchcard", "text": "Phần nào trong công việc của bạn\nđã được viết sẵn trong sách?"},
    {"type": "question", "at": 14, "bg": "x4", "text": "Và phần nào,\nchỉ bạn mới biết?"},
]}

SPEC = {
    "title": "AI Có Cướp Việc Của Bạn? 200 Năm Trước Người Ta Cũng Sợ Y Như Vậy",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "endcardBg": "x4",
    "acc": ["ai", "luddite", "keynes", "oxford", "atm", "eniac", "fortran", "hinton", "chatgpt", "nasa", "naca", "2030"],
    "say": SAY, "imgs": IMGS, "chapters": list(CH),
    "youtube": {
        "titles": ["AI Có Cướp Việc Của Bạn? 200 Năm Trước Người Ta Cũng Sợ Y Như Vậy",
                   "\"Máy Tính\" Từng Là Một Nghề. Nghề Đó Đã Biến Mất — Với AI, Còn Người Thì Sao?",
                   "Lần Nào Máy Mới Ra Đời Cũng Có Người Nói \"Lần Này Khác\". Với AI, Có Khác Không?"],
        "summary": "Năm 1952, \"máy tính\" là chức danh của những người phụ nữ ngồi tính bằng máy bấm phím ở NACA. Chỉ trong một thế hệ, nghề ấy biến mất. "
                   "Từ những người đập máy năm 1811, cô tổng đài, cây ATM, tới lời tiên tri của Geoffrey Hinton về bác sĩ X-quang và dữ liệu mới nhất "
                   "về AI tạo sinh: máy móc đã thật sự cướp việc của ai, vì sao lời tiên tri \"máy thay người\" thường sai, và lần này có khác không?",
        "more": ["Video không đưa ra dự báo hay lời khuyên chọn nghề. Số liệu của Stanford (2026) là mô tả, chưa phải bằng chứng nhân quả, "
                 "đúng như chính các tác giả nhấn mạnh."],
        "ch00_title": "\"Máy tính\" từng là một nghề",
        "chapter_titles": {"ch00": "Mở đầu: \"máy tính\" từng là một nghề (1952)", "ch01": "Luddite: những người đập máy (1804–1813)",
                           "ch02": "Ba lời tiên tri máy cướp việc: Keynes, 1964, Oxford", "ch03": "Cô tổng đài và người lái thang máy",
                           "ch04": "Nghịch lý máy ATM và giao dịch viên ngân hàng", "ch05": "Dorothy Vaughan, ENIAC: những \"máy tính\" đã đi đâu?",
                           "ch06": "Hinton và lời tiên tri về bác sĩ X-quang", "ch07": "AI có cướp việc người trẻ? Dữ liệu 2025–2026",
                           "ch08": "Kết: năm 2030 của Keynes"},
        "sources": [
            "https://www.nasa.gov/people/dorothy-vaughan/",
            "https://www.nationalarchives.gov.uk/education/teaching-resources/why-did-the-luddites-protest/",
            "https://www.nber.org/papers/w28061",
            "https://www.bls.gov/ooh/office-and-administrative-support/tellers.htm",
            "https://www.engineering.upenn.edu/about/history-heritage/eniac/",
            "https://www.oxfordmartin.ox.ac.uk/downloads/academic/The_Future_of_Employment.pdf",
            "https://digitaleconomy.stanford.edu/news/canariesaug26/",
            "https://budgetlab.yale.edu/research/evaluating-impact-ai-labor-market-current-state-affairs",
            "https://www.imf.org/external/pubs/ft/fandd/2015/03/bessen.htm",
            "https://www.marxists.org/reference/subject/economics/keynes/1930/our-grandchildren.htm",
            "https://www.understandingai.org/p/ai-isnt-replacing-radiologists",
            "https://www.fourmilab.ch/babbage/sketch.html",
        ],
        "hashtags": ["AI", "TríTuệNhânTạo", "ViệcLàm", "MấtViệc", "MindInTheMachine"],
        "tags": ["AI cướp việc", "AI có cướp việc", "mất việc vì AI", "trí tuệ nhân tạo", "việc làm", "tự động hoá", "Luddite",
                 "Keynes", "ATM", "Hidden Figures", "Dorothy Vaughan", "ENIAC", "Geoffrey Hinton", "bác sĩ X-quang", "ChatGPT",
                 "lịch sử công nghệ"],
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
    print(f"spec + {len(CH)} chương")
