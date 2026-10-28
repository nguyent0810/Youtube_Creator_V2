"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM "OPPENHEIMER ngoài đời thật: Richard Feynman, người đua với máy IBM ở Los Alamos" (20-30 phút).

    python motion/long/script_lines.py mim-oppenheimer-feynman      # ghi "lines" + "title" từ script.md (chạy trước)
    python data/long/mim-oppenheimer-feynman/gen_scenes.py          # ghi spec.json + scenes/hud/bgm (giữ nguyên "lines" + "title")

Kịch bản + nguồn: script.md và factcheck.md. Pha 1: chỉ viết file; chưa dựng, chưa tải ảnh (imgs ghi tên File: Commons, giấy phép đã đọc qua
Commons API 23/10/2026, phải đọc lại ở pha 2 trước khi tải).
HÌNH:
  - KHÔNG có hình, cảnh, áp phích của phim Oppenheimer (2023): phim chỉ được nhắc bằng lời và chữ.
  - Ảnh Commons PD / CC0 / CC BY. Ảnh "PD-LosAlamos" (Commons ghi LicenseShortName "Attribution"): LANL cho dùng mọi mục đích, kể cả
    thương mại, với điều kiện ghi nguồn LANL -> coi như CC BY, credit "Los Alamos National Laboratory". Không dùng BY-SA ("File:IBM 601 - MfK Bern.jpg").
  - Máy IBM 601, máy Marchant, thẻ 80 cột là ảnh CÙNG LOẠI chụp ở bảo tàng / đời sau -> gắn "ẢNH MINH HỌA".
  - Ảnh vụ nổ Trinity dùng tiết chế (3 khung), chú thích trung tính; chương Cái giá dùng ảnh đổ nát Hiroshima / Nagasaki của chính phủ Mỹ (PD).
  - Không có clip Pexels (không cần); nếu pha 2 thêm, chạy motion/long/clip_sheet.py.
Lộ trình dạng "ổ khoá ba số": ledger ở CH00 (hứa) + counter "x / 3" ở CH04 (số 1), CH07 (số 2), CH11 (số 3), ledger CH12 (xếp ba số, ổ khoá mở).
  Chưa có loại cảnh "mặt số két quay" trong engine (motion/ không thuộc phạm vi pha 1) -> counter + ledger thay; nếu muốn mặt số thật, thêm cảnh ở lab.js.
Mọi neo [dòng, "từ"] chỉ dùng chữ nằm trong lời đọc; không neo vào chữ số hay chữ có trong bảng "say" (check() kiểm cả hai).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"feynman": "Phai-mần", "richard": "Rít-chợt", "los": "Lốt", "alamos": "A-la-mốt", "oppenheimer": "Óp-pen-hai-mơ", "new": "Niu",
       "mexico": "Mê-hi-cô", "trinity": "Tri-ni-ti", "princeton": "Prin-xtần", "bob": "Bóp", "wilson": "Uyn-xần", "uranium": "u-ra-ni-um",
       "hitler": "Hít-le", "chicago": "Si-ca-gô", "paul": "Pôn", "olum": "Ô-lâm", "california": "Ca-li-pho-ni-a", "santa": "Xan-ta",
       "barbara": "Ba-ba-ra", "caltech": "Can-tếch", "hans": "Han", "bethe": "Bê-tơ", "marchant": "Mác-săng", "friden": "Phrai-đần",
       "monroe": "Mơn-râu", "langley": "Lăng-li", "nasa": "na-sa", "mici": "Mít-xi", "teller": "Te-lơ", "edward": "Ét-uốt", "mary": "Me-ri",
       "frankel": "Phrăng-cồ", "stanley": "Xten-li", "fe": "Phê", "albuquerque": "An-bơ-kơ-ki", "nicholas": "Ni-cô-lát",
       "metropolis": "Mê-trô-pô-lít", "emilio": "Ê-mi-li-ô", "segrè": "Xê-grê", "plutonium": "plu-tô-ni-um", "john": "Giôn", "von": "phôn",
       "neumann": "Noi-man", "eldred": "En-đrét", "nelson": "Nen-xần", "dana": "Đây-na", "mitchell": "Mít-sần", "columbia": "Cô-lăm-bi-a",
       "ibm": "ai bi em", "=IBM": "ai bi em", "johnston": "Giôn-xtần", "naomi": "Nây-ô-mi", "livesay": "Lai-vơ-xây", "arctang": "ác-tang",
       "rơ-le": "rơ le", "kemeny": "Kê-mê-ni", "basic": "Bây-xích", "=BASIC": "Bây-xích", "hamming": "Ham-minh", "robert": "Rô-bớt",
       "christy": "Cri-xti", "fuchs": "Phúc", "tnt": "ti en ti", "=TNT": "ti en ti", "jeep": "gíp", "hiroshima": "Hi-rô-si-ma",
       "nagasaki": "Na-ga-xa-ki", "cornell": "Coóc-nen", "york": "Gioóc", "eleanor": "E-li-nơ", "ewing": "Diu-inh",
       "philadelphia": "Phi-la-đen-phi-a", "eniac": "Ê-ni-ác", "=ENIAC": "Ê-ni-ác", "stanislaw": "Xta-ni-xláp", "ulam": "U-lam",
       "poker": "pô-cơ", "neutron": "nơ-tron", "monte": "Mông-tê", "carlo": "Các-lô", "aberdeen": "A-bơ-đin", "maryland": "Me-ri-len",
       "klara": "Cla-ra", "thomas": "Tô-mát", "haigh": "Hây", "mark": "Mác", "priestley": "Prít-li", "freddy": "Phre-đi", "de": "đơ",
       "hoffmann": "Hóp-man", "pi": "pi", "nobel": "Nô-ben", "bill": "Biu", "archer": "A-chơ", "radio": "ra-đi-ô", "com-lê": "com lê"}
VM = "ẢNH MINH HỌA"
SELF = "TỰ TÍNH"
LEWIS = "N. LEWIS · TRINITY BY THE NUMBERS (LANL)"
ARCHER = "B. J. ARCHER · LA-UR-21-20164 (LANL)"
FEYN = "LOS ALAMOS FROM BELOW (FEYNMAN, 1976)"
CH = {}

IMGS = {
    "feyn": "File:Richard Feynman Los Alamos ID badge.jpg",                                       # Public domain (US Army / Atomic Heritage)
    "feyn0": "File:Richard Feynman's badge photo from Los Alamos National Laboratory.jpg",        # CC0 (LANL, qua AIP Emilio Segrè Visual Archives)
    "feyn39": "File:Richard Feynman 1939 MIT yearbook portrait.jpg",                             # Public domain (MIT Technique 1939)
    "fire16": "File:Trinity Test Fireball 16ms.jpg",                                             # Public domain (Berlyn Brixner / LANL)
    "fire25": "File:Trinity Test Fireball-25ms.jpg",                                             # Public domain (US Govt. DTRA)
    "fire53": "File:Trinity Test Fireball 53ms.jpg",                                             # Public domain (NNSA Nevada Site Office)
    "strip": "File:Trinity explosion film strip.jpg",                                            # Public domain (Berlyn Brixner)
    "oppgroves": "File:Oppenheimer and Groves at the Trinity detonation site.jpg",              # PD-LosAlamos ("Attribution": ghi nguồn LANL), 11/09/1945
    "ibm601": "File:SW45-H-57-Mus of Comm Bern IBM 601 punchcard machine.jpg",                   # CC BY 4.0 (VasuVR) · KHÔNG dùng "IBM 601 - MfK Bern.jpg" (BY-SA)
    "marchant": "File:Marchant mechanical calculator.jpg",                                       # CC0 (Bhaiyaji Smile 123, 2025)
    "sed": "File:Members of the Army's Special Engineer Detachment (SED) at Los Alamos, NM, in 1945.jpg",  # Public domain (US Army)
    "techarea": "File:Los Alamos Tech Area annotated.jpg",                                       # Public domain (LANL, qua OSTI OpenNet)
    "bldgT": "File:Building T, Tech Area, Los Alamos (2).jpg",                                   # Public domain (US Army Corps of Engineers)
    "card": "File:Blue-punch-card-front-horiz.png",                                              # Public domain (Gwern; phái sinh: agr)
    "eniac": "File:Classic shot of the ENIAC.jpg",                                               # Public domain (US Army)
    "eniacbrl": "File:Glen Beck and Betty Snyder program the ENIAC in building 328 at the Ballistic Research Laboratory.jpg",  # Public domain (US Army)
    "ulam": "File:Stanislaw Ulam ID badge.png",                                                  # Public domain (thẻ Los Alamos)
    "vonneumann": "File:JohnvonNeumann-LosAlamos.jpg",                                           # PD-LosAlamos ("Attribution": ghi nguồn LANL)
    "bethe": "File:Hans Bethe ID badge.png",                                                     # Public domain (thẻ Los Alamos)
    "livesay": "File:Naomi M. Livesay Los Alamos identity badge photo.jpg",                      # PD-LosAlamos ("Attribution": ghi nguồn LANL)
    "hiroshima": "File:AtomicEffects-Hiroshima.jpg",                                             # Public domain (US government)
    "nagasaki": "File:Destruction in Nagasaki, Japan, in September 1945 (01).jpg",               # Public domain (US Navy, USS Wichita)
}

# ---------------------------------------------------------------- CH00: sau kính chắn gió một chiếc xe tải (cold open)
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "SAU KÍNH CHẮN GIÓ MỘT CHIẾC XE TẢI"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "day": "SA MẠC NEW MEXICO · VỤ THỬ TRINITY", "date": "16.07.1945",
     "sub": {"text": "TRỜI CÒN TỐI · VỪA TẠNH GIÔNG", "at": 1}},
    {"type": "ledger", "at": 2, "title": "ĐỒI QUAN SÁT CHÍNH", "srcnote": "BẢO TÀNG NGUYÊN TỬ QUỐC GIA (DOE) · TRINITY SITE, 1995",
     "rows": [{"k": "CÁCH TÂM NỔ", "v": "≈ 20 DẶM ≈ 32 KM", "at": [2, "cây"]},
              {"k": "HẦM GẦN NHẤT", "v": "≈ 5,7 DẶM ≈ 9 KM", "at": [2, "nhóm"]}]},
    {"type": "print", "at": 3, "img": "feyn", "tone": "bw",
     "side": {"k": "RICHARD FEYNMAN · 27 TUỔI", "h": "Nhà vật lý\nLos Alamos", "lines": [{"text": "Thẻ ra vào *thời chiến*", "at": [3, "phòng"]}]}},
    {"type": "kinetic", "at": 4, "items": [{"text": "PHIM OPPENHEIMER (2023)", "at": [4, "phim"], "acc": True},
                                           {"text": "có nhân vật Richard Feynman", "at": [4, "danh"], "sm": True},
                                           {"text": "vai do Jack Quaid đóng · theo Looper, 05/2023", "at": [4, "vật"], "sm": True}]},
    {"type": "slam", "at": 5, "text": "VÌ NHỮNG CON SỐ", "sub": "NGOÀI ĐỜI THẬT · KHÔNG PHẢI TRÊN MÀN ẢNH"},
    {"type": "kinetic", "at": 6, "items": [{"text": "RADIO IM LÌM", "at": 6},
                                           {"text": "mãi vài phút trước giờ nổ mới chạy", "at": [7, "vài"], "sm": True},
                                           {"text": "MỌI NGƯỜI: KÍNH ĐEN", "at": 8}]},
    {"type": "quote", "at": 10, "dy": True, "text": "Thứ làm hại mắt là tia cực tím. Mà tia cực tím không đi qua được kính.",
     "by": "RICHARD FEYNMAN · " + FEYN, "lbl": "DIỄN Ý", "typeAt": [10, None, 0, 0.05], "typeDur": 2.8},
    {"type": "kinetic", "at": 11, "items": [{"text": "SAU KÍNH CHẮN GIÓ XE TẢI", "at": [11, "kính"], "acc": True},
                                            {"text": "để nhìn bằng chính mắt mình", "at": [11, "nhìn"], "sm": True}]},
    {"type": "slam", "at": 12, "text": "05:29:45", "sub": "GIỜ THỜI CHIẾN MIỀN NÚI (MWT) · THEO BẢO TÀNG NGUYÊN TỬ QUỐC GIA (DOE)"},
    {"type": "photo", "at": 13, "img": "fire16", "tone": "color", "move": "in", "veil": 0.4,
     "kin": [{"text": "CHỚP SÁNG", "at": 13, "acc": True}],
     "label": {"k": "VỤ THỬ TRINITY · 16 PHẦN NGHÌN GIÂY", "v": "ẢNH: BERLYN BRIXNER / LANL", "at": 13}},
    {"type": "kinetic", "at": 15, "items": [{"text": "DỪNG Ở ĐÂY", "at": 15, "sm": True},
                                            {"text": "ĐÃ ĐƯỢC TÍNH TRƯỚC", "at": 16, "acc": True},
                                            {"text": "chưa có máy tính điện tử nào chạy cho Los Alamos", "at": 17, "sm": True}]},
    {"type": "photo", "at": 18, "img": "ibm601", "tone": "bw", "move": "in", "veil": 0.5, "illus": VM + " · MÁY CÙNG LOẠI, BẢO TÀNG BERN",
     "kin": [{"text": "MỘT CĂN PHÒNG ĐẦY MÁY ĐỤC LỖ", "at": [18, "căn"], "acc": True}],
     "label": {"k": "MÁY NHÂN ĐỤC LỖ IBM 601", "v": "ẢNH: VASUVR · CC BY 4.0", "at": 18}},
    {"type": "ledger", "at": 19, "title": "Ổ KHOÁ BA SỐ", "srcnote": "MỖI PHẦN VIDEO MỞ MỘT SỐ · KHÔNG PHẢI TRÒ ĐOÁN MẬT MÃ",
     "rows": [{"k": "SỐ 1", "v": "?", "at": 21}, {"k": "SỐ 2", "v": "?", "at": 22}, {"k": "SỐ 3", "v": "?", "at": 23}],
     "total": {"k": "ĐỦ BA SỐ", "v": "MỞ RA CÂU TRẢ LỜI", "at": 24}},
    {"type": "question", "at": 25, "text": "Làm sao tính trước một vụ nổ\nchưa ai từng thấy?"},
]}

# ---------------------------------------------------------------- CH01: cậu nghiên cứu sinh chưa có bằng
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CẬU NGHIÊN CỨU SINH CHƯA CÓ BẰNG"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CẬU NGHIÊN CỨU SINH\nCHƯA CÓ BẰNG", "sub": "PRINCETON → LOS ALAMOS", "bg": "feyn39",
     "titleAt": [0, "Vài"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "MỘT DỰ ÁN BÍ MẬT", "at": [1, "dự"], "acc": True},
                                           {"text": "tách đồng vị uranium để làm bom", "at": [1, "tách"], "sm": True}]},
    {"type": "slam", "at": 2, "text": "TỪ CHỐI", "sub": "…ĐƯỢC CHỪNG BA PHÚT"},
    {"type": "timeline", "at": 5, "items": [{"year": "15:00", "text": "*đi họp*", "at": 5},
                                           {"year": "16:00", "text": "đã có *một cái bàn* để tính", "at": 6}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "ĐI CHICAGO · VỀ KỂ LẠI", "at": 7, "acc": True}, {"text": "nhà toán học Paul Olum trêu một câu", "at": 8, "sm": True}]},   # 23/10: thẻ trích chỉ bắt đầu ở câu trích (qa_blank 9,5 s)
    {"type": "quote", "at": 9, "dy": True, "text": "Khi người ta làm phim về chuyện này, anh chàng đi báo cáo sẽ mặc com-lê, xách cặp…",
     "by": "PAUL OLUM, QUA LỜI FEYNMAN · " + FEYN, "lbl": "DIỄN Ý", "typeAt": [9, None, 0, 0.05], "typeDur": 3.0},
    {"type": "kinetic", "at": 10, "items": [{"text": "CÒN ÔNG: ÁO SƠ MI BẨN", "at": 10},
                                            {"text": "TÁM MƯƠI NĂM SAU", "at": 11, "acc": True},
                                            {"text": "phim về chuyện này ra rạp thật", "at": [11, "rạp"], "sm": True}]},
    {"type": "source", "at": 12, "source": "R. P. FEYNMAN · “LOS ALAMOS FROM BELOW”", "ref": "ENGINEERING & SCIENCE (CALTECH) · TẬP 39, SỐ 2 · 1976",
     "snippet": "bài nói ở UCSB năm 1975 · [[nhìn từ bên dưới]]: không phải người quyết định điều lớn", "hlAt": [14, "dưới"],
     "seal": "CÓ BẢN QUYỀN · VIDEO CHỈ DIỄN Ý", "sealAt": 15},
    {"type": "print", "at": 16, "img": "oppgroves", "tone": "bw", "illus": "ẢNH CHỤP 09.1945 · OPPENHEIMER (TRÁI) CÙNG TƯỚNG GROVES",
     "side": {"k": "J. ROBERT OPPENHEIMER", "h": "Người tuyển\nFeynman", "lines": [{"text": "lo cả chuyện *bệnh viện* cho vợ Feynman", "at": [17, "bệnh"]}]}},
    {"type": "kinetic", "at": 18, "items": [{"text": "“MỘT NGƯỜI TUYỆT VỜI”", "at": 18, "acc": True},
                                            {"text": "Feynman nhớ về Oppenheimer", "at": [18, "nói"], "sm": True}]},
    {"type": "photo", "at": 19, "img": "techarea", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "MỘT TẤM BẢNG ĐEN CÓ BÁNH XE", "at": 20, "acc": True}],
     "label": {"k": "KHU KỸ THUẬT LOS ALAMOS", "v": "LANL · BẢN ĐỒ CÓ CHÚ THÍCH", "at": 19}},
    {"type": "print", "at": 21, "img": "bethe", "tone": "bw",
     "side": {"k": "HANS BETHE", "h": "Trưởng\nBan Lý thuyết", "lines": [{"text": "cần một người *dám cãi lại*", "at": 22}]}},
    {"type": "counter", "at": 24, "from": 0, "to": 2304, "until": [28, "linh"], "label": "48 × 48",
     "sub": {"text": "BETHE NÓI “KHOẢNG 2.300” TRƯỚC KHI MÁY RA SỐ", "at": 27}},
    {"type": "kinetic", "at": 29, "items": [{"text": "MÁY RA ĐÚNG 2.304", "at": 29, "acc": True},
                                            {"text": "mẹo của Bethe cho những số gần 50", "at": 30, "sm": True}]},
    {"type": "bars", "at": 31, "title": "AI TÍNH NHẨM NHANH HƠN · SAU VÀI NĂM", "unit": "THEO FEYNMAN · LOS ALAMOS FROM BELOW", "max": 4,
     "items": [{"k": "BETHE THẮNG", "v": 3, "lbl": "≈ 3 / 4", "at": 32}, {"k": "FEYNMAN THẮNG", "v": 1, "lbl": "≈ 1 / 4", "at": [32, "thắng"], "acc": True}]},
    {"type": "slam", "at": 34, "text": "NGƯỜI ĐẤU MÁY", "sub": "CUỘC ĐUA THỨ HAI · SẮP TỚI"},
    {"type": "ledger", "at": 35, "title": "NHÓM CỦA FEYNMAN", "srcnote": FEYN,
     "rows": [{"k": "TRƯỞNG NHÓM", "v": "DƯỚI QUYỀN BETHE", "at": [35, "trưởng"]}, {"k": "THÀNH VIÊN", "v": "4 NGƯỜI", "at": [35, "bốn"]}]},
    {"type": "question", "at": 37, "text": "Bài toán đang chờ họ\nlớn đến mức nào?"},
]}

# ---------------------------------------------------------------- CH02: những "máy tính" biết thở
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "NHỮNG “MÁY TÍNH” BIẾT THỞ"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "NHỮNG “MÁY TÍNH”\nBIẾT THỞ", "sub": "NHÓM TÍNH TAY · 1943", "bg": "marchant", "titleAt": [0, "Ở"]},
    {"type": "print", "at": 1, "img": "marchant", "tone": "color", "illus": VM + " · MÁY MARCHANT ĐỜI KHÁC, KHÔNG PHẢI MÁY Ở LOS ALAMOS",
     "side": {"k": "MÁY CỘNG CƠ KHÍ", "h": "Marchant\nFriden · Monroe", "lines": [{"text": "làm tính theo *tờ hướng dẫn*", "at": [2, "hướng"]}]}},
    {"type": "kinetic", "at": 3, "items": [{"text": "NHƯ LANGLEY CỦA NASA", "at": 3, "sm": True},
                                           {"text": "+ MỘT BÍ MẬT QUỐC GIA", "at": 4, "acc": True}]},
    {"type": "counter", "at": 5, "from": 0, "to": 12, "until": [5, "người"], "suffix": " NGƯỜI", "label": "NHÓM TÍNH TAY · MÙA XUÂN 1943",
     "sub": {"text": "PHẦN LỚN LÀ NGƯỜI TÌNH NGUYỆN · " + LEWIS, "at": [5, "tình"]}},
    {"type": "ledger", "at": 6, "title": "VÌ SAO LÀ VỢ CÁC NHÀ KHOA HỌC", "srcnote": LEWIS,
     "rows": [{"k": "VÍ DỤ", "v": "MICI TELLER · JEAN BACHER", "at": [6, "vợ"]},
              {"k": "NHÀ Ở", "v": "ĐÃ CÓ SẴN", "at": [8, "nhà"]}, {"k": "AN NINH", "v": "KHÔNG CẦN ĐIỀU TRA MỚI", "at": [8, "an"]}]},
    {"type": "file", "at": 9, "k": "NGƯỜI GIAO BÀI", "name": "MARY FRANKEL", "desc": "Bằng tâm lý học và toán · chuyên gia phương pháp số",
     "rows": [{"k": "TỜ MẪU", "v": "lấy *a* ở đâu · lấy *b* ở đâu", "at": 11}, {"k": "PHÉP TÍNH", "v": "(a + b) ÷ 2", "at": [11, "chia"]},
              {"k": "KẾT QUẢ", "v": "ghi vào ô nào", "at": [11, "ghi"]}],
     "label": {"k": "NGUỒN", "v": "VÍ DỤ NỘI SUY TUYẾN TÍNH · " + ARCHER, "at": 10}},
    {"type": "kinetic", "at": 12, "items": [{"text": "MỘT BÀI LỚN · CHẺ RA", "at": 12, "acc": True},
                                            {"text": "nhiều người làm cùng một lúc", "at": [12, "nhiều"], "sm": True}]},
    {"type": "bars", "at": 13, "title": "NHÓM TÍNH TAY LỚN DẦN", "unit": LEWIS + " · NGƯỜI", "max": 30,
     "items": [{"k": "XUÂN 1943", "v": 12, "lbl": "≈ 12", "at": 13}, {"k": "CUỐI HÈ 1943", "v": 20, "lbl": "≈ 20", "at": [13, "nữ"]},
               {"k": "VỀ SAU", "v": 25, "lbl": "25", "at": 14, "acc": True}]},
    {"type": "photo", "at": 15, "img": "bldgT", "tone": "bw", "move": "in", "veil": 0.5, "illus": VM + " · MỘT TOÀ NHÀ Ở KHU KỸ THUẬT",
     "kin": [{"text": "MÁY KÊU LẠCH CẠCH SUỐT NGÀY", "at": 16}],
     "label": {"k": "TOÀ NHÀ T · KHU KỸ THUẬT LOS ALAMOS", "v": "MANHATTAN DISTRICT HISTORY", "at": 15}},
    {"type": "slam", "at": 17, "text": "BỤI", "sub": "MÀI MÒN MÁY · PHÉP TÍNH QUAN TRỌNG LÀM HAI LẦN"},
    {"type": "question", "at": 20, "text": "Còn máy hỏng thì sao?"},
    {"type": "ledger", "at": 21, "title": "XƯỞNG SỬA MÁY TỰ PHÁT", "srcnote": FEYN + " · " + LEWIS,
     "rows": [{"k": "BAN ĐẦU", "v": "GỬI XUỐNG SANTA FE / ALBUQUERQUE", "at": 21},
              {"k": "FEYNMAN + METROPOLIS", "v": "TỰ THÁO NẮP MÁY", "at": [23, "tháo"]},
              {"k": "QUY ĐỊNH", "v": "“THÁO NẮP: HÃNG MIỄN TRÁCH”", "at": [23, "quy"]},
              {"k": "VỀ SAU", "v": "FEYNMAN LO PHẦN MÁY TÍNH", "at": 25}]},
    {"type": "kinetic", "at": 26, "items": [{"text": "CUỐI 1943: VẪN KHÔNG THEO KỊP", "at": 26},
                                            {"text": "BÀI TOÁN SẮP TỚI CÒN LỚN HƠN", "at": 27, "acc": True}]},
]}

# ---------------------------------------------------------------- CH03: một vụ nổ không được làm thử
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "MỘT VỤ NỔ KHÔNG ĐƯỢC LÀM THỬ"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "MỘT VỤ NỔ\nKHÔNG ĐƯỢC LÀM THỬ", "sub": "1943 — 1944", "bg": "techarea", "titleAt": [0, "Thử"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "NGUYÊN LIỆU QUÁ HIẾM", "at": 1}, {"text": "không có công thức gọn trên giấy", "at": 2, "sm": True},
                                           {"text": "TÍNH BẰNG SỐ · TỪNG BƯỚC", "at": 3, "acc": True}]},
    {"type": "date", "at": 4, "day": "THÍ NGHIỆM CỦA NHÓM EMILIO SEGRÈ", "date": "1944", "sub": {"text": "MÙA HÈ · MỘT TIN XẤU", "at": [4, "tin"]}},
    {"type": "ledger", "at": 5, "title": "KIỂU “KHẨU SÚNG” VỚI PLUTONIUM", "srcnote": LEWIS + " · DO PLUTONIUM-240 TỰ PHÂN HẠCH",
     "rows": [{"k": "CÁCH LÀM", "v": "BẮN 2 KHỐI NHỎ VÀO NHAU", "at": [5, "bắn"]}, {"k": "VẤN ĐỀ", "v": "GẶP NHAU QUÁ CHẬM", "at": 6},
              {"k": "HẬU QUẢ", "v": "PHẢN ỨNG BẮT ĐẦU SỚM", "at": 7}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "URANIUM: CÓ LẼ ĐỦ 1 QUẢ", "at": 8}, {"text": "PLUTONIUM: ĐỦ NHIỀU HƠN", "at": 9, "acc": True},
                                           {"text": "không còn đường lùi", "at": 10, "sm": True}]},
    {"type": "slam", "at": 11, "text": "NỔ ÉP VÀO TRONG", "sub": "IMPLOSION · CÁCH ĐỂ DÙNG ĐƯỢC PLUTONIUM"},
    {"type": "print", "at": 12, "img": "vonneumann", "tone": "bw",
     "side": {"k": "JOHN VON NEUMANN", "h": "Nhà toán học\nchuyên về dòng chảy", "lines": [{"text": "thúc đẩy cách nổ ép · *cuối 1943*", "at": [12, "thúc"]}]}},
    {"type": "timeline", "at": 13, "bg": "techarea", "items": [{"year": "1", "text": "*thuốc nổ* xếp quanh lõi", "at": 13},
                                            {"year": "2", "text": "sóng ép *chạy vào* · dội ra", "at": 15},
                                            {"year": "3", "text": "mỗi tích tắc = *một vòng tính*", "at": 16}]},
    {"type": "source", "at": 17, "source": "N. LEWIS · “TRINITY BY THE NUMBERS”", "ref": "LOS ALAMOS NATIONAL LABORATORY · LA-UR-20-30196",
     "snippet": "tính nổ ép bằng tay là [[không thực tế]], nhất là khi dùng phương trình trạng thái thật", "hlAt": [17, "không"],
     "seal": "DIỄN Ý TỪ BÀI NGHIÊN CỨU", "sealAt": [17, "tế"]},
    {"type": "date", "at": 18, "day": "FRANKEL & NELSON MANG BÀI TOÁN TỚI BETHE", "date": "10.1943", "sub": {"text": LEWIS, "at": [18, "lo"]}},
    {"type": "kinetic", "at": 19, "items": [{"text": "LỜI GIẢI TỪ MỘT NƠI BẤT NGỜ", "at": 19, "acc": True},
                                            {"text": "Dana Mitchell · người lo mua sắm", "at": [20, "mua"], "sm": True}]},
    {"type": "photo", "at": 21, "img": "card", "tone": "color", "move": "in", "veil": 0.45, "illus": VM + " · THẺ 80 CỘT ĐỜI SAU",
     "kin": [{"text": "MÁY KẾ TOÁN ĐỤC LỖ", "at": [21, "kế"], "acc": True},
             {"text": "phòng tính thiên văn · Đại học Columbia", "at": [21, "thiên"], "sm": True}],
     "label": {"k": "THẺ ĐỤC LỖ 80 CỘT", "v": "PHẠM VI CÔNG CỘNG", "at": 21}},
    {"type": "ledger", "at": 23, "title": "ĐƠN ĐẶT HÀNG", "srcnote": LEWIS + " · " + ARCHER,
     "rows": [{"k": "MÁY NHÂN", "v": "3 × IBM 601", "at": [23, "nhân"]}, {"k": "KÈM THEO", "v": "MÁY CỘNG IN · SẮP · ĐỤC THẺ", "at": [23, "phụ"]},
              {"k": "KỲ VỌNG", "v": "NHIỀU THÁNG → VÀI TUẦN", "at": 24}],
     "total": {"k": "VỀ TỚI", "v": "ĐẦU XUÂN 1944", "at": 25}},
    {"type": "question", "at": 27, "text": "Trong lúc chờ máy,\nhọ làm gì?"},
]}

# ---------------------------------------------------------------- CH04: dây chuyền không có máy (SỐ 1)
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "DÂY CHUYỀN KHÔNG CÓ MÁY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "DÂY CHUYỀN\nKHÔNG CÓ MÁY", "sub": "THÁNG 3 · 1944", "bg": "ibm601", "titleAt": [0, "Hồi"]},
    {"type": "ledger", "at": 1, "title": "MÁY KẾ TOÁN IBM THỜI ẤY", "srcnote": FEYN + " · " + ARCHER + ", BẢNG I",
     "rows": [{"k": "MÁY CỘNG IN (405)", "v": "IN RA TỔNG", "at": [1, "cộng"]}, {"k": "MÁY NHÂN (601)", "v": "ĐỌC 2 SỐ TRÊN THẺ → NHÂN", "at": [1, "đọc"]},
              {"k": "MÁY SẮP (075)", "v": "SẮP THẺ THEO CỘT", "at": [1, "sắp"]}]},
    {"type": "timeline", "at": 3, "bg": "ibm601", "items": [{"year": "1", "text": "*máy cộng*", "at": 3}, {"year": "2", "text": "*máy nhân*", "at": [3, "nhân"]},
                                           {"year": "3", "text": "lại *máy cộng*", "at": [3, "lại"]}]},
    {"type": "quote", "at": 4, "dy": True, "text": "Sản xuất hàng loạt bằng máy. Khi ấy, đó là chuyện mới.", "by": "RICHARD FEYNMAN · " + FEYN,
     "lbl": "DIỄN Ý", "typeAt": [4, None, 0, 0.05], "typeDur": 2.4},
    {"type": "kinetic", "at": 6, "items": [{"text": "1 VÒNG THẺ = 1 BƯỚC THỜI GIAN", "at": 6, "acc": True},
                                           {"text": "≈ 12 thao tác · người vẫn phải can thiệp", "at": 7, "sm": True}]},
    {"type": "date", "at": 8, "day": "MÁY VẪN CHƯA VỀ", "date": "03.1944", "sub": {"text": "THỬ CHƯƠNG TRÌNH BẰNG NGƯỜI", "at": 9}},
    {"type": "photo", "at": 10, "img": "marchant", "tone": "bw", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỖI CÔ · MỘT VIỆC", "at": 10, "acc": True}],
     "label": {"k": "MÁY CỘNG MARCHANT", "v": "ẢNH: BHAIYAJI SMILE 123 · CC0", "at": 10}},
    {"type": "ledger", "at": 11, "title": "DÂY CHUYỀN BẰNG NGƯỜI", "srcnote": FEYN + " · " + LEWIS,
     "rows": [{"k": "BÀN 1", "v": "CHỈ CỘNG", "at": 11}, {"k": "BÀN 2", "v": "CHỈ NHÂN", "at": 12}, {"k": "BÀN 3", "v": "CHỈ LẬP PHƯƠNG", "at": 13},
              {"k": "→", "v": "GHI THẺ · CHUYỀN SANG BÀN BÊN", "at": 14}],
     "total": {"k": "MỤC ĐÍCH", "v": "GỠ LỖI CHƯƠNG TRÌNH", "at": 15}},
    {"type": "kinetic", "at": 16, "items": [{"text": "MỘT BẤT NGỜ", "at": 16, "sm": True},
                                            {"text": "NHANH HƠN MỖI NGƯỜI TỰ LÀM HẾT", "at": 17},
                                            {"text": "NGANG TỐC ĐỘ DỰ TÍNH CHO MÁY IBM", "at": 18, "acc": True}]},
    {"type": "split", "at": 19, "title": "KHÁC BIỆT DUY NHẤT · THEO FEYNMAN",
     "a": {"img": "ibm601", "label": "MÁY: KHÔNG MỆT · 3 CA", "at": 19},
     "b": {"img": "marchant", "label": "NGƯỜI: MỆT DẦN", "at": 20}},
    {"type": "ledger", "at": 21, "title": "CÁCH FEYNMAN MỞ KÉT", "srcnote": FEYN + " · DIỄN Ý",
     "rows": [{"k": "TỦ KIỂU MỚI", "v": "ÁP TAI · SỜ TAY ĐỀU VÔ ÍCH", "at": 22}, {"k": "LỆCH 2 VẠCH", "v": "VẪN MỞ", "at": [23, "lệch"]},
              {"k": "TỔ HỢP", "v": "≈ 8.000 · THỬ HẾT TRONG 8 GIỜ", "at": 24}]},
    {"type": "kinetic", "at": 25, "items": [{"text": "≈ HAI NĂM MÀY MÒ", "at": 25},
                                            {"text": "TỦ ĐANG MỞ → DÒ 2 SỐ CUỐI", "at": 26, "acc": True},
                                            {"text": "vừa tán chuyện vừa nghịch mặt số", "at": 27, "sm": True}]},
    {"type": "counter", "at": 28, "from": 0, "to": 20, "until": [28, "khả"], "suffix": " KHẢ NĂNG", "label": "SỐ ĐẦU · KHI ĐÃ CÓ HAI SỐ CUỐI",
     "sub": {"text": "≈ 3 PHÚT LÀ MỞ · THEO FEYNMAN", "at": 29}},
    {"type": "slam", "at": 30, "text": "CHẺ VIỆC RA", "sub": "KHÔNG DÒ CẢ BA SỐ MỘT LÚC"},
    {"type": "counter", "at": 32, "from": 0, "to": 1, "until": [32, "mở"], "suffix": " / 3", "label": "Ổ KHOÁ · SỐ THỨ NHẤT ĐÃ MỞ",
     "sub": {"text": "SỐ 1 · CHẺ VIỆC THÀNH DÂY CHUYỀN", "at": 33}},
    {"type": "source", "at": 34, "source": "B. J. ARCHER · “THE LOS ALAMOS COMPUTING FACILITY…”", "ref": "LANL · LA-UR-21-20164 · 2021",
     "snippet": "lập trình máy IBM bắt đầu bằng việc [[chẻ phương trình thành từng thao tác]]: cộng hai số này, chia hai số kia…",
     "hlAt": [34, "chẻ"], "seal": "DIỄN Ý TỪ BÀI NGHIÊN CỨU", "sealAt": [34, "lập"]},
    {"type": "kinetic", "at": 35, "items": [{"text": "CÓ TRƯỚC CẢ MÁY", "at": 35, "acc": True},
                                            {"text": "máy tới · người lắp máy thì không", "at": 37, "sm": True}]},
]}

# ---------------------------------------------------------------- CH05: những thùng máy không có thợ
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "NHỮNG THÙNG MÁY KHÔNG CÓ THỢ"}, "bgm": {"mood": "epic", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "NHỮNG THÙNG MÁY\nKHÔNG CÓ THỢ", "sub": "04.04.1944", "bg": "ibm601", "titleAt": [0, "Ngày"]},
    {"type": "ledger", "at": 1, "title": "VÌ SAO KHÔNG CÓ THỢ", "srcnote": ARCHER + " · " + LEWIS,
     "rows": [{"k": "IBM", "v": "KHÔNG ĐƯỢC BIẾT MÁY ĐI ĐÂU", "at": 1}, {"k": "THỢ GIỎI NHẤT", "v": "J. JOHNSTON · ĐÃ NHẬP NGŨ", "at": 2},
              {"k": "TỚI SAU MÁY", "v": "2–3 NGÀY (HAI NGUỒN LỆCH)", "at": [3, "tới"]}]},
    {"type": "slam", "at": 4, "text": "TỰ LẮP", "sub": "FEYNMAN · FRANKEL · NELSON · THEO BẢN VẼ ĐI DÂY"},
    {"type": "photo", "at": 6, "img": "ibm601", "tone": "color", "move": "in", "veil": 0.5, "illus": VM + " · IBM 601 Ở BẢO TÀNG BERN",
     "kin": [{"text": "PHỨC TẠP BẬC NHẤT THỜI ẤY", "at": 6, "acc": True}, {"text": "“coi chừng làm hỏng đấy!”", "at": 7, "sm": True}],
     "label": {"k": "MÁY NHÂN ĐỤC LỖ IBM 601", "v": "ẢNH: VASUVR · CC BY 4.0", "at": 6}},
    {"type": "kinetic", "at": 8, "items": [{"text": "CÓ MÁY CHẠY · CÓ MÁY KHÔNG", "at": 8, "sm": True},
                                           {"text": "MỘT CHI TIẾT BỊ CONG", "at": 9, "acc": True}, {"text": "không dám nắn · sợ gãy", "at": 10, "sm": True}]},
    {"type": "timeline", "at": 11, "items": [{"year": "THỢ TỚI", "text": "sửa *các máy còn lại*", "at": 11},
                                            {"year": "+3 NGÀY", "text": "vẫn *loay hoay*", "at": 12},
                                            {"year": "FEYNMAN", "text": "“chỗ này *bị cong*”", "at": 13}]},
    {"type": "quote", "at": 14, "dy": True, "text": "À, tất nhiên rồi, chỉ có thế thôi!", "by": "NGƯỜI THỢ IBM, QUA LỜI FEYNMAN · " + FEYN,
     "lbl": "DIỄN Ý", "qline": 14, "typeAt": [14, "tất"]},
    {"type": "kinetic", "at": 15, "items": [{"text": "NẮN LẠI · MÁY CHẠY", "at": 15, "acc": True}]},
    {"type": "ledger", "at": 16, "title": "NGƯỜI NGOÀI IBM ĐẦU TIÊN", "srcnote": LEWIS + " · DẪN NHẬN ĐỊNH CỦA HANS BETHE",
     "rows": [{"k": "BETHE:", "v": "NGOÀI IBM, LẦN ĐẦU TỰ LẮP ĐƯỢC", "at": [16, "đầu"]}]},
    {"type": "print", "at": 17, "img": "livesay", "tone": "bw",
     "side": {"k": "NAOMI LIVESAY", "h": "Nhà toán học\nlập trình máy IBM", "lines": [
         {"text": "*6 tháng* học máy IBM ở Princeton", "at": 18}, {"text": "người *duy nhất* được đào tạo bài bản", "at": 19},
         {"text": "lập trình = *cắm lại dây*", "at": 20}]}},
    {"type": "ledger", "at": 21, "title": "PHÒNG MÁY CHẠY", "srcnote": LEWIS + " · " + ARCHER,
     "rows": [{"k": "BÀI ĐẦU TIÊN", "v": "≈ 1 TUẦN SAU KHI MÁY TỚI", "at": 21}, {"k": "CA", "v": "3 CA · 24 GIỜ", "at": 22},
              {"k": "MỖI TUẦN", "v": "6 NGÀY", "at": [22, "sáu"]}]},
    {"type": "date", "at": 23, "day": "CUỘC ĐUA NGƯỜI ĐẤU MÁY", "date": "04.1944", "sub": {"text": "NHÓM TÍNH TAY vs DÀN MÁY IBM", "at": [23, "nhóm"]}},
    {"type": "kinetic", "at": 24, "items": [{"text": "HAI NGÀY ĐẦU: GẦN NHƯ HOÀ", "at": 24}, {"text": "RỒI NGƯỜI MỆT", "at": 25, "acc": True},
                                            {"text": "MÁY THÌ KHÔNG", "at": 26}]},
    {"type": "slam", "at": 27, "text": "MÁY THẮNG", "sub": "NHƯNG BÀI ĐẦU TIÊN MẤT BA THÁNG"},
    {"type": "question", "at": 29, "text": "Máy thắng,\nvậy sao vẫn mất ba tháng?"},
]}

# ---------------------------------------------------------------- CH06: ba bài trong chín tháng (re-hook ~45%)
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "BA BÀI TRONG CHÍN THÁNG"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "BA BÀI\nTRONG CHÍN THÁNG", "sub": "1944 — 1945", "bg": "sed", "titleAt": [0, "Máy"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "HÀNG TRĂM RƠ-LE MỖI MÁY", "at": 1}, {"text": "MỘT HẠT BỤI = SỐ SAI", "at": [1, "hạt"], "acc": True}]},
    {"type": "quote", "at": 2, "text": "…insensitive to small errors.", "by": "N. METROPOLIS, QUA " + LEWIS, "lbl": "TRÍCH",
     "typeAt": [2, None, 0, 0.05], "typeDur": 1.4},
    {"type": "ledger", "at": 3, "title": "CHỊU ĐƯỢC SAI SỐ NHỎ", "srcnote": LEWIS,
     "rows": [{"k": "SAI CHỮ SỐ CUỐI", "v": "BỎ QUA", "at": [3, "bỏ"]}, {"k": "SAI CHỮ SỐ LỚN", "v": "SỬA", "at": [3, "sửa"]}]},
    {"type": "slam", "at": 5, "text": "“BỆNH MÁY TÍNH”", "sub": "FEYNMAN ĐẶT TÊN"},
    {"type": "kinetic", "at": 6, "items": [{"text": "NGƯỜI MẮC ĐẦU TIÊN: FRANKEL", "at": 6, "sm": True},
                                           {"text": "BẢNG ARCTANG TỰ IN", "at": 7, "acc": True},
                                           {"text": "bảng ấy đã có sẵn · một bảng vô ích", "at": 8, "sm": True}]},
    {"type": "quote", "at": 10, "dy": True, "text": "Máy vui quá, nên người ta chơi với nó, và quên việc chính.", "by": "RICHARD FEYNMAN · " + FEYN,
     "lbl": "DIỄN Ý", "typeAt": [10, None, 0, 0.05], "typeDur": 2.2},
    {"type": "date", "at": 12, "day": "FRANKEL CHUYỂN NHÓM · FEYNMAN TRÔNG MÁY", "date": "01.1945", "sub": {"text": ARCHER, "at": 13}},
    {"type": "counter", "at": 14, "from": 0, "to": 3, "until": [14, "chín"], "suffix": " BÀI", "label": "TRONG CHÍN THÁNG · THEO FEYNMAN",
     "sub": {"text": "TIẾN ĐỘ RẤT CHẬM", "at": 15}},
    {"type": "photo", "at": 16, "img": "fire25", "tone": "bw", "move": "in", "veil": 0.6,
     "kin": [{"text": "NHỚ CHỚP SÁNG Ở ĐẦU VIDEO?", "at": 16, "acc": True}, {"text": "con đường tới nó đang tắc ở đây", "at": 17, "sm": True}],
     "label": {"k": "VỤ THỬ TRINITY · 25 PHẦN NGHÌN GIÂY", "v": "ẢNH: CHÍNH PHỦ MỸ", "at": 16}},
    {"type": "photo", "at": 18, "img": "sed", "tone": "bw", "move": "in", "veil": 0.45, "illus": "ẢNH ĐỘI SED NÓI CHUNG · KHÔNG RIÊNG NHÓM MÁY IBM",
     "kin": [{"text": "CHỌN KHẮP NƯỚC · NĂNG KHIẾU KỸ THUẬT", "at": 19, "acc": True}],
     "label": {"k": "ĐỘI KỸ SƯ ĐẶC BIỆT (SED) · LOS ALAMOS, 1945", "v": "ẢNH: QUÂN ĐỘI MỸ", "at": 18}},
    {"type": "kinetic", "at": 20, "items": [{"text": "ĐỤC LỖ NHỮNG CON SỐ", "at": 20}, {"text": "KHÔNG AI NÓI LÀ SỐ GÌ", "at": [20, "giải"], "acc": True}]},
    {"type": "slam", "at": 22, "text": "CHỖ TẮC THẬT", "sub": "KHÔNG PHẢI Ở MÁY · THEO FEYNMAN"},
    {"type": "ledger", "at": 24, "title": "BUỔI GIẢNG ĐƯỢC PHÉP", "srcnote": FEYN + " · " + LEWIS,
     "rows": [{"k": "XIN PHÉP", "v": "OPPENHEIMER", "at": [24, "xin"]}, {"k": "NGƯỜI NGHE", "v": "LÍNH VẬN HÀNH MÁY", "at": [24, "giảng"]},
              {"k": "ÁP SUẤT CAO HƠN", "v": "NĂNG LƯỢNG NHIỀU HƠN", "at": 26}],
     "total": {"k": "NHÓM TÍNH TAY", "v": "KHÔNG ĐƯỢC GIẢI THÍCH", "at": 28}},
    {"type": "kinetic", "at": 29, "items": [{"text": "CON ĐƯỜNG RẼ NGOẶT Ở ĐÂY", "at": 29, "acc": True},
                                            {"text": "những cậu lính tự nghĩ cách làm nhanh hơn", "at": 30, "sm": True}]},
]}

# ---------------------------------------------------------------- CH07: thẻ trắng, thẻ xanh, thẻ vàng (SỐ 2)
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "THẺ TRẮNG, THẺ XANH, THẺ VÀNG"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "THẺ TRẮNG,\nTHẺ XANH, THẺ VÀNG", "sub": "SỐ THỨ HAI", "bg": "card", "titleAt": [0, "Trước"]},
    {"type": "timeline", "at": 1, "items": [{"year": "TRƯỚC", "text": "*một bài* một lúc", "at": 1},
                                           {"year": "VẤN ĐỀ", "text": "máy nhân bận · *máy cộng ngồi chơi*", "at": 2}]},
    {"type": "slam", "at": 3, "text": "TÔ MÀU THẺ", "sub": "MẸO CỦA NHỮNG CẬU LÍNH · " + LEWIS},
    {"type": "ledger", "at": 4, "title": "BA BÀI · LỆCH NHỊP", "srcnote": FEYN + " · " + LEWIS + " · KÊNH MINH HOẠ BẰNG BẢNG",
     "rows": [{"k": "THẺ TRẮNG", "v": "BÀI A · ĐANG Ở MÁY NHÂN", "at": 4}, {"k": "THẺ XANH", "v": "BÀI B · ĐANG Ở MÁY CỘNG", "at": 5},
              {"k": "THẺ VÀNG", "v": "BÀI C · ĐANG Ở MÁY SẮP", "at": 6}],
     "total": {"k": "KẾT QUẢ", "v": "KHÔNG MÁY NÀO ĐỨNG CHỜ", "at": 7}},
    {"type": "bars", "at": 8, "title": "THỜI GIAN MỘT BÀI", "unit": LEWIS + " · TÍNH THEO TUẦN", "max": 14,
     "items": [{"k": "TRƯỚC", "v": 13, "lbl": "≈ 3 THÁNG", "at": 8}, {"k": "SAU", "v": 3, "lbl": "≈ 3 TUẦN", "at": [8, "chừng"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "FEYNMAN NHỚ", "at": 9, "sm": True}, {"text": "9 THÁNG → 3 BÀI", "at": 10},
                                           {"text": "3 THÁNG → 9 BÀI", "at": [10, "giờ"], "acc": True}, {"text": "nhanh gần gấp mười", "at": 11, "sm": True}]},
    {"type": "ledger", "at": 12, "title": "MỘT CÁCH ĐẾM KHÁC", "srcnote": ARCHER + " · THEO HỒ SƠ",
     "rows": [{"k": "04 → 07.1945", "v": "12 BÀI", "at": 13}], "total": {"k": "HAI CÁCH ĐẾM", "v": "CÙNG MỘT HƯỚNG", "at": 14}},
    {"type": "counter", "at": 15, "from": 1, "to": 2, "until": [15, "thứ"], "suffix": " / 3", "label": "Ổ KHOÁ · SỐ THỨ HAI ĐÃ MỞ",
     "sub": {"text": "SỐ 2 · CHẠY SONG SONG, LỆCH NHỊP", "at": 16}},
    {"type": "kinetic", "at": 17, "items": [{"text": "TÍNH SONG SONG", "at": 17, "acc": True},
                                            {"text": "không đến từ phòng các nhà vật lý", "at": 18, "sm": True},
                                            {"text": "đến từ người vừa biết mình tính gì", "at": 19, "sm": True}]},
    {"type": "ledger", "at": 20, "title": "MÁY MẠNH LÊN · CUỐI 1944", "srcnote": ARCHER + " · " + LEWIS,
     "rows": [{"k": "GỢI Ý", "v": "JOHNSTON · NHÂN 3 SỐ MỘT LẦN", "at": 21}, {"k": "ĐÀM PHÁN", "v": "NELSON ↔ IBM", "at": 22},
              {"k": "RIÊNG LOS ALAMOS", "v": "2 MÁY CHIA ĐƯỢC", "at": [22, "chia"]}, {"k": "TRƯỚC ĐÓ", "v": "TRA THẺ NGHỊCH ĐẢO RỒI NHÂN", "at": 23}]},
    {"type": "kinetic", "at": 24, "items": [{"text": "NHỮNG CÁI TÊN VỀ SAU", "at": 24, "sm": True}, {"text": "JOHN KEMENY → BASIC", "at": 25, "acc": True},
                                            {"text": "RICHARD HAMMING → MÃ SỬA LỖI", "at": 27}]},
    {"type": "quote", "at": 29, "text": "…experiments that were impossible in the laboratory were going to be possible with computers.",
     "by": "RICHARD HAMMING · QUA " + LEWIS, "lbl": "TRÍCH DỊCH", "qline": 29, "typeAt": [29, "thí"]},
    {"type": "slam", "at": 30, "text": "HẠN CHÓT", "sub": "CẢ HỆ THỐNG BỊ ĐẨY TỚI GIỚI HẠN"},
]}

# ---------------------------------------------------------------- CH08: hạn chót ba tuần
CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "HẠN CHÓT BA TUẦN"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "HẠN CHÓT\nBA TUẦN", "sub": "1945", "bg": "bldgT", "titleAt": [0, "Gần"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "NHIỀU THIẾT KẾ ĐÃ TÍNH", "at": 1, "sm": True},
                                           {"text": "CHƯA TÍNH: THIẾT KẾ SẼ ĐEM THỬ", "at": [1, "chưa"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "THIẾT KẾ ĐƯỢC CHỌN", "srcnote": LEWIS + " · " + FEYN,
     "rows": [{"k": "LÕI", "v": "ĐẶC", "at": [2, "lõi"]}, {"k": "ĐỀ XUẤT", "v": "ROBERT CHRISTY · 09.1944", "at": [2, "đề"]}],
     "total": {"k": "CHRISTY CẦN", "v": "KẾT QUẢ SAU ≈ 3–4 TUẦN", "at": 3}},
    {"type": "slam", "at": 4, "text": "KHÔNG THỂ ĐƯỢC", "sub": "FEYNMAN ĐÁP"},
    {"type": "kinetic", "at": 5, "items": [{"text": "MỖI BÀI: LÂU HƠN THẾ NHIỀU", "at": 5},
                                           {"text": "chỉ nhanh vì chạy nhiều bài cùng lúc", "at": [5, "chỉ"], "sm": True}]},
    {"type": "question", "at": 7, "text": "Nếu dẹp hết,\nchỉ dồn sức cho một bài?"},
    {"type": "kinetic", "at": 8, "items": [{"text": "“TA LÀM ĐƯỢC KHÔNG?”", "at": [8, "ta"], "acc": True},
                                           {"text": "hai ca · làm thêm giờ", "at": 9, "sm": True}, {"text": "LUẬT MỚI: CHỈ MỘT BÀI", "at": 10}]},
    {"type": "date", "at": 11, "day": "VỢ FEYNMAN QUA ĐỜI Ở ALBUQUERQUE", "date": "1945", "sub": {"text": "THEO LỜI KỂ CỦA FEYNMAN", "at": [11, "qua"]}},
    {"type": "ledger", "at": 12, "title": "CHIẾC XE ĐI MƯỢN", "srcnote": FEYN + " · LỜI KỂ CỦA FEYNMAN",
     "rows": [{"k": "CHỦ XE", "v": "FUCHS · BẠN CÙNG KÝ TÚC XÁ", "at": [12, "bạn"]}, {"k": "FEYNMAN BIẾT VỀ SAU", "v": "FUCHS LÀ GIÁN ĐIỆP", "at": [13, "gián"]},
              {"k": "BA NGÀY SAU", "v": "QUAY LẠI PHÒNG MÁY", "at": 14}]},
    {"type": "photo", "at": 15, "img": "card", "tone": "color", "move": "out", "veil": 0.5, "illus": VM + " · THẺ ĐỜI SAU",
     "kin": [{"text": "THẺ TRẮNG · THẺ XANH · THẺ VÀNG", "at": 15, "acc": True}, {"text": "“đã bảo chỉ một bài thôi mà!”", "at": 16, "sm": True}],
     "label": {"k": "THẺ ĐỤC LỖ", "v": "PHẠM VI CÔNG CỘNG", "at": 15}},
    {"type": "kinetic", "at": 17, "items": [{"text": "“ĐI ĐI, ĐỢI ĐÃ!”", "at": 17, "acc": True}, {"text": "chuyện là thế này", "at": 18, "sm": True}]},
    {"type": "ledger", "at": 19, "title": "LỖI LAN NHƯ MỘT CĂN BỆNH", "srcnote": FEYN + " · VÍ DỤ CỦA CHÍNH FEYNMAN",
     "rows": [{"k": "MỘT LỖI", "v": "HỎNG VÀI THẺ LÂN CẬN", "at": [20, "hỏng"]}, {"k": "MỖI VÒNG", "v": "LAN RỘNG THÊM", "at": [20, "lan"]},
              {"k": "VÍ DỤ", "v": "50 THẺ · LỖI Ở THẺ 39", "at": 21}]},
    {"type": "timeline", "at": 22, "bg": "ibm601", "items": [{"year": "1", "text": "tách *xấp nhỏ* ≈ 10 thẻ", "at": 22},
                                            {"year": "2", "text": "chạy *nhanh hơn* · đuổi kịp", "at": 23},
                                            {"year": "3", "text": "*vá vào* xấp lớn", "at": [23, "vá"]}]},
    {"type": "kinetic", "at": 24, "items": [{"text": "MÀU THẺ THỨ HAI, THỨ BA", "at": 24}, {"text": "= NHỮNG XẤP VÁ", "at": [24, "vá"], "acc": True},
                                            {"text": "sếp bước vào · bị đuổi ra", "at": 25, "sm": True}]},
    {"type": "slam", "at": 27, "text": "XONG KỊP HẠN", "sub": "BÀI TOÁN CHO THIẾT KẾ SẼ ĐEM THỬ"},
    {"type": "source", "at": 28, "source": "N. LEWIS · “TRINITY BY THE NUMBERS”", "ref": "LANL · LA-UR-20-30196",
     "snippet": "mô phỏng cho thấy thiết kế lõi đặc sẽ cho [[sức nổ tốt]] · ban lãnh đạo chọn thiết kế ấy để chế tạo", "hlAt": [28, "sức"],
     "seal": "DIỄN Ý TỪ BÀI NGHIÊN CỨU", "sealAt": 29},
    {"type": "date", "at": 30, "day": "QUAY LẠI NGỌN ĐỒI", "date": "16.07.1945", "sub": {"text": "05:29:45 MWT", "at": [30, "ngọn"]}},
]}

# ---------------------------------------------------------------- CH09: chín mươi giây im lặng (cảnh mạnh ~75%)
CH["ch09"] = {"hud": {"k": "CHƯƠNG 09", "t": "CHÍN MƯƠI GIÂY IM LẶNG"}, "bgm": {"mood": "calm", "gain": 0.09}, "scenes": [
    {"type": "chapter", "no": "9", "k": "CHƯƠNG CHÍN", "title": "CHÍN MƯƠI GIÂY\nIM LẶNG", "sub": "TRINITY · 16.07.1945", "bg": "strip", "titleAt": [0, "ngẩng"]},
    {"type": "photo", "at": 1, "img": "fire53", "tone": "color", "move": "in", "veil": 0.45,
     "kin": [{"text": "MỘT VỆT TÍM TRÊN SÀN XE", "at": 1, "acc": True}, {"text": "“chỉ là dư ảnh”", "at": 2, "sm": True}],
     "label": {"k": "VỤ THỬ TRINITY · 53 PHẦN NGHÌN GIÂY", "v": "ẢNH: NNSA · CHÍNH PHỦ MỸ", "at": 1}},
    {"type": "ledger", "at": 3, "title": "NHỮNG GÌ FEYNMAN THẤY", "srcnote": FEYN + " · DIỄN Ý",
     "rows": [{"k": "1", "v": "TRẮNG → VÀNG → CAM", "at": 4}, {"k": "2", "v": "MÂY HIỆN RỒI TAN", "at": 5},
              {"k": "3", "v": "QUẢ CẦU CAM · VIỀN ĐEN · KHÓI", "at": 6}]},
    {"type": "counter", "at": 7, "from": 0, "to": 60, "until": [7, "phút"], "suffix": " GIÂY", "label": "TẤT CẢ CHỪNG MỘT PHÚT",
     "sub": {"text": "KHÔNG AI NÓI MỘT LỜI", "at": 8}},
    {"type": "photo", "at": 9, "img": "strip", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "NHÌN BẰNG MẮT TRẦN", "at": 9, "acc": True}, {"text": "người ở gần hơn: nằm sấp xuống đất", "at": 10, "sm": True}],
     "label": {"k": "DẢI PHIM CHỤP VỤ NỔ TRINITY", "v": "BERLYN BRIXNER · PHẠM VI CÔNG CỘNG", "at": 9}},
    {"type": "counter", "at": 11, "from": 0, "to": 90, "until": [11, "vọng"], "suffix": " GIÂY", "label": "TỪ CHỚP SÁNG TỚI TIẾNG NỔ · ≈ MỘT PHÚT RƯỠI",
     "sub": {"text": "32 KM ÷ 343 M/GIÂY ≈ 94 GIÂY · " + SELF, "at": 13}},
    {"type": "slam", "at": 14, "text": "NÓ ĐÃ CHẠY THẬT", "sub": "TIẾNG NỔ LÀM FEYNMAN TIN"},
    {"type": "quote", "at": 15, "dy": True, "text": "Âm thanh còn đặc chắc như thế ở khoảng cách ấy, nghĩa là nó đã chạy thật.", "by": "RICHARD FEYNMAN · " + FEYN,
     "lbl": "DIỄN Ý", "typeAt": [15, None, 0, 0.05], "typeDur": 2.6},
    {"type": "kinetic", "at": 16, "items": [{"text": "“ĐÓ LÀ GÌ?”", "at": 16}, {"text": "“ĐÓ LÀ QUẢ BOM.”", "at": 17, "acc": True},
                                            {"text": "người hỏi: một phóng viên", "at": 18, "sm": True}]},
    {"type": "ledger", "at": 19, "title": "VỤ THỬ TRINITY", "srcnote": "BẢO TÀNG NGUYÊN TỬ QUỐC GIA (DOE) · " + LEWIS,
     "rows": [{"k": "SỨC NỔ ƯỚC TÍNH", "v": "≈ 20.000 TẤN TNT", "at": 19}, {"k": "KIỂM CHỨNG", "v": "TÍNH TOÁN THIẾT KẾ ĐÃ CHỌN", "at": 20}],
     "total": {"k": "THẺ MÀU · MÁY QUAY TAY", "v": "ĐÃ TÍNH ĐÚNG", "at": 21}},
    {"type": "photo", "at": 22, "img": "bldgT", "tone": "bw", "move": "in", "veil": 0.5, "illus": "ẢNH TƯ LIỆU · LOS ALAMOS",   # 23/10: không đặt chữ "Feynman" lên ảnh người khác
     "kin": [{"text": "Ở LOS ALAMOS: MỞ TIỆC", "at": 22}, {"text": "Feynman đánh trống trên xe jeep", "at": 23, "sm": True}],
     "label": {"k": "TOÀ NHÀ T · KHU KỸ THUẬT", "v": "CÔNG BINH LỤC QUÂN MỸ", "at": 22}},
    {"type": "kinetic", "at": 24, "items": [{"text": "BOB WILSON", "at": [24, "rầu"], "acc": True},
                                            {"text": "người đã rủ Feynman vào dự án", "at": [24, "rủ"], "sm": True}]},
    {"type": "quote", "at": 26, "text": "It's a terrible thing that we made.", "by": "BOB WILSON, QUA LỜI FEYNMAN · " + FEYN,
     "lbl": "TRÍCH DỊCH", "qline": 26, "typeAt": [26, "kinh"]},
    {"type": "question", "at": 28, "text": "Ba tuần sau,\ncâu nói ấy có thêm tên hai thành phố."},
]}

# ---------------------------------------------------------------- CH10: cái giá
CH["ch10"] = {"hud": {"k": "CHƯƠNG 10", "t": "CÁI GIÁ"}, "bgm": {"mood": "calm", "gain": 0.08}, "scenes": [
    {"type": "chapter", "no": "10", "k": "CHƯƠNG MƯỜI", "title": "CÁI GIÁ", "sub": "06.08 · 09.08.1945", "bg": "hiroshima", "titleAt": [0, "Ngày"]},
    {"type": "date", "at": 1, "day": "NAGASAKI · 11:02 GIỜ NHẬT", "date": "09.08.1945",
     "sub": {"text": "BA NGÀY SAU HIROSHIMA (06.08.1945) · BÁO CÁO MANHATTAN DISTRICT", "at": [1, "lượt"]}},
    {"type": "kinetic", "at": 2, "items": [{"text": "MÌNH XIN KỂ CHẬM LẠI", "at": 2, "sm": True}]},
    {"type": "ledger", "at": 3, "title": "CÙNG KIỂU THIẾT KẾ", "srcnote": "BẢO TÀNG NGUYÊN TỬ QUỐC GIA (DOE) · " + LEWIS,
     "rows": [{"k": "BOM NAGASAKI", "v": "PLUTONIUM · KIỂU TRINITY", "at": [3, "cùng"]},
              {"k": "TỨC LÀ", "v": "THIẾT KẾ CÁC XẤP THẺ ĐÃ TÍNH", "at": 4}]},
    {"type": "photo", "at": 5, "img": "hiroshima", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "KHÔNG AI BIẾT CON SỐ CHÍNH XÁC", "at": 5, "acc": True}],
     "label": {"k": "HIROSHIMA SAU VỤ NỔ", "v": "ẢNH: CHÍNH PHỦ MỸ · PHẠM VI CÔNG CỘNG", "at": 5}},
    {"type": "ledger", "at": 6, "title": "ƯỚC TÍNH SỐ NGƯỜI CHẾT · TỚI CUỐI 12.1945", "srcnote": "THÀNH PHỐ HIROSHIMA · THÀNH PHỐ NAGASAKI (BÁO CÁO 07.1950)",
     "rows": [{"k": "HIROSHIMA", "v": "≈ 140.000", "at": [6, "ước"]}, {"k": "NAGASAKI", "v": "73.884", "at": [7, "ước"]}]},
    {"type": "slam", "at": 8, "text": "ĐÓ LÀ CÁI GIÁ", "sub": "HAI THÀNH PHỐ · MỘT MÙA HÈ", "white": True},
    {"type": "photo", "at": 9, "img": "nagasaki", "tone": "bw", "move": "out", "veil": 0.5,
     "kin": [{"text": "CƯ DÂN · BINH LÍNH · NGƯỜI ĐƯỢC HUY ĐỘNG", "at": 9},
             {"text": "cả lao động bị cưỡng bức từ các thuộc địa của Nhật · theo thành phố Hiroshima", "at": 10, "sm": True}],
     "label": {"k": "NAGASAKI · 09.1945", "v": "ẢNH: HẢI QUÂN MỸ · PHẠM VI CÔNG CỘNG", "at": 9}},
    {"type": "ledger", "at": 11, "title": "BÁO CÁO CỦA QUÂN ĐỘI MỸ · 1946", "srcnote": "MANHATTAN ENGINEER DISTRICT · THE ATOMIC BOMBINGS OF HIROSHIMA AND NAGASAKI",
     "rows": [{"k": "HIROSHIMA", "v": "66.000 CHẾT", "at": [11, "con"]}, {"k": "NAGASAKI", "v": "39.000 CHẾT", "at": [11, "thấp"]}],
     "total": {"k": "BÁO CÁO TỰ NHẬN", "v": "“RẤT KHÓ ƯỚC TÍNH”", "at": [11, "khó"]}},
    {"type": "kinetic", "at": 12, "items": [{"text": "FEYNMAN KỂ VỀ CHÍNH MÌNH", "at": 13}, {"text": "về dạy ở Đại học Cornell", "at": 14, "sm": True}]},
    {"type": "quote", "at": 15, "dy": True, "text": "Từ đây tới phố số 34 là bao xa? Tất cả những toà nhà này, đổ nát…", "by": "RICHARD FEYNMAN · " + FEYN,
     "lbl": "DIỄN Ý", "typeAt": [15, None, 0, 0.05], "typeDur": 3.0},
    {"type": "kinetic", "at": 17, "items": [{"text": "XÂY CẦU LÀM GÌ NỮA?", "at": 17},
                                            {"text": "GẦN 30 NĂM SAU: “TÔI MỪNG VÌ MÌNH ĐÃ SAI”", "at": 18, "acc": True}]},
    {"type": "ledger", "at": 19, "title": "MỘT ĐIỀU KHÓ NGHE HƠN", "srcnote": FEYN + " · DIỄN Ý",
     "rows": [{"k": "BẮT ĐẦU", "v": "VÌ MỘT LÝ DO TỐT", "at": 20}, {"k": "RỒI", "v": "LAO VÀO · VUI VÌ GIẢI ĐƯỢC BÀI KHÓ", "at": [20, "lao"]},
              {"k": "CUỐI CÙNG", "v": "THÔI KHÔNG NGHĨ", "at": 21}],
     "total": {"k": "CÒN NGHĨ", "v": "BOB WILSON", "at": 22}},
    {"type": "kinetic", "at": 23, "items": [{"text": "KHÔNG RA ĐỜI TRONG MỘT PHÒNG THÍ NGHIỆM VÔ CAN", "at": 24, "acc": True},
                                            {"text": "và không dừng lại khi chiến tranh kết thúc", "at": 25, "sm": True}]},
    {"type": "question", "at": 26, "text": "Sau chiến tranh,\nnhững cỗ máy ấy đi đâu?"},
]}

# ---------------------------------------------------------------- CH11: con xúc xắc điện tử (SỐ 3)
CH["ch11"] = {"hud": {"k": "CHƯƠNG 11", "t": "CON XÚC XẮC ĐIỆN TỬ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "11", "k": "CHƯƠNG MƯỜI MỘT", "title": "CON XÚC XẮC\nĐIỆN TỬ", "sub": "1945 — 1948", "bg": "eniac", "titleAt": [0, "Trong"]},
    {"type": "print", "at": 1, "img": "vonneumann", "tone": "bw",
     "side": {"k": "JOHN VON NEUMANN", "h": "Khách quen\ncủa phòng máy", "lines": [{"text": "học chạy máy từ *Livesay và Ewing*", "at": [1, "chỉ"]}]}},
    {"type": "date", "at": 2, "day": "TIN TỪ PHILADELPHIA: ENIAC", "date": "1945", "sub": {"text": "MÁY TÍNH HOÀN TOÀN BẰNG ĐIỆN TỬ", "at": 3}},
    {"type": "photo", "at": 4, "img": "eniac", "tone": "bw", "move": "in", "veil": 0.45,
     "kin": [{"text": "≈ 18.000 BÓNG ĐÈN ĐIỆN TỬ", "at": 5, "acc": True}, {"text": "nửa triệu mối hàn · Metropolis, 1987", "at": [5, "nửa"], "sm": True}],
     "label": {"k": "ENIAC", "v": "ẢNH: QUÂN ĐỘI MỸ · PHẠM VI CÔNG CỘNG", "at": 4}},
    {"type": "quote", "at": 7, "text": "No one ever had such a wonderful toy!", "by": "N. METROPOLIS · LOS ALAMOS SCIENCE, 1987", "lbl": "TRÍCH DỊCH",
     "qline": 7, "typeAt": [7, "từng"]},
    {"type": "counter", "at": 8, "from": 0, "to": 1000000, "until": [9, "triệu"], "suffix": " THẺ", "label": "BÀI TOÁN CỦA LOS ALAMOS TRÊN ENIAC · 12.1945",
     "sub": {"text": LEWIS, "at": 9}},
    {"type": "print", "at": 10, "img": "ulam", "tone": "bw",
     "side": {"k": "STANISLAW ULAM", "h": "Nhà toán học\nLos Alamos", "lines": [{"text": "chơi bài một mình · mê *poker*", "at": [11, "chơi"]}]}},
    {"type": "kinetic", "at": 13, "items": [{"text": "LẤY MẪU NGẪU NHIÊN", "at": 13, "acc": True}, {"text": "bị bỏ quên vì quá dài, quá chán", "at": 14, "sm": True},
                                            {"text": "VỚI ENIAC: SỐNG LẠI", "at": 15}]},
    {"type": "slam", "at": 16, "text": "ULAM + VON NEUMANN", "sub": "MÙA XUÂN 1946 · METROPOLIS, 1987"},
    {"type": "timeline", "at": 20, "bg": "eniac", "items": [{"year": "1", "text": "theo *từng hạt* một", "at": 20}, {"year": "2", "text": "mỗi ngã rẽ: *tung xúc xắc*", "at": [20, "tung"]},
                                            {"year": "3", "text": "lặp lại · *bức tranh chung* hiện ra", "at": 22}]},
    {"type": "date", "at": 24, "day": "THƯ VIẾT TAY GỬI TRƯỞNG BAN LÝ THUYẾT", "date": "11.03.1947", "sub": {"text": "VON NEUMANN PHÁC PHƯƠNG PHÁP · METROPOLIS, 1987", "at": [24, "phác"]}},
    {"type": "slam", "at": 25, "text": "MONTE CARLO", "sub": "TÊN DO METROPOLIS ĐẶT · ÔNG CHÚ CỦA ULAM “PHẢI ĐI MONTE CARLO”"},
    {"type": "ledger", "at": 27, "title": "XÚC XẮC TRONG MÁY · “GIỮA BÌNH PHƯƠNG”", "srcnote": "N. METROPOLIS 1987 · VÍ DỤ SỐ DO KÊNH " + SELF,
     "rows": [{"k": "SỐ", "v": "5.772", "at": [28, "bình"]}, {"k": "BÌNH PHƯƠNG", "v": "33.315.984", "at": [28, "lấy"]},
              {"k": "LẤY BỐN SỐ GIỮA", "v": "3.159 → SỐ TIẾP THEO", "at": [28, "giữa"]}]},
    {"type": "photo", "at": 29, "img": "eniacbrl", "tone": "bw", "move": "in", "veil": 0.45,
     "kin": [{"text": "ABERDEEN, MARYLAND", "at": [29, "bang"]}, {"text": "hơn 300 km · cuối 1947", "at": [29, "chuyến"], "sm": True}],
     "label": {"k": "ENIAC Ở PHÒNG THÍ NGHIỆM ĐẠN ĐẠO, ABERDEEN", "v": "ẢNH: QUÂN ĐỘI MỸ · PHẠM VI CÔNG CỘNG", "at": 29}},
    {"type": "kinetic", "at": 30, "items": [{"text": "KLARA VON NEUMANN + METROPOLIS", "at": 30, "sm": True},
                                            {"text": "CHẠY THEO CHƯƠNG TRÌNH NẠP SẴN", "at": [30, "chương"], "acc": True}]},
    {"type": "date", "at": 31, "day": "MONTE CARLO ĐẦU TIÊN TRÊN MÁY TÍNH", "date": "04.1948",
     "sub": {"text": "CHẠY TỪ 17.04 · XONG 10.05 · HAIGH, PRIESTLEY & ROPE 2014", "at": 32}},
    {"type": "quote", "at": 34, "text": "The results are very promising…", "by": "J. VON NEUMANN GỬI ULAM · 11.05.1948 · QUA HAIGH, PRIESTLEY & ROPE",
     "lbl": "TRÍCH", "typeAt": [34, None, 0, 0.05], "typeDur": 1.4},
    {"type": "counter", "at": 35, "from": 2, "to": 3, "until": [35, "cuối"], "suffix": " / 3", "label": "Ổ KHOÁ · SỐ CUỐI CÙNG ĐÃ MỞ",
     "sub": {"text": "SỐ 3 · MÁY ĐIỆN TỬ TỰ CHẠY, TUNG XÚC XẮC", "at": 36}},
]}

# ---------------------------------------------------------------- CH12: ổ khoá mở
CH["ch12"] = {"hud": {"k": "CHƯƠNG 12", "t": "Ổ KHOÁ MỞ"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "12", "k": "CHƯƠNG MƯỜI HAI", "title": "Ổ KHOÁ MỞ", "sub": "BA SỐ · MỘT LỜI GIẢI", "bg": "feyn0", "titleAt": [0, "Giờ"]},
    {"type": "ledger", "at": 1, "title": "Ổ KHOÁ BA SỐ", "srcnote": "KÊNH TỔNG HỢP TỪ CÁC CHƯƠNG TRƯỚC",
     "rows": [{"k": "SỐ 1", "v": "CHẺ VIỆC THÀNH DÂY CHUYỀN", "at": 1}, {"k": "SỐ 2", "v": "CHẠY NHIỀU VIỆC CÙNG LÚC", "at": 2},
              {"k": "SỐ 3", "v": "MÁY TỰ CHẠY · TUNG XÚC XẮC", "at": 3}],
     "total": {"k": "MỞ RA", "v": "CÁCH TÍNH TRƯỚC MỘT VỤ NỔ", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "KHÔNG NHỜ RIÊNG MỘT THIÊN TÀI", "at": 5}, {"text": "NHỜ CÁCH CHIA VIỆC", "at": 6, "acc": True},
                                           {"text": "người mệt, máy thì không", "at": 7, "sm": True}]},
    {"type": "source", "at": 8, "source": "N. METROPOLIS · “THE BEGINNING OF THE MONTE CARLO METHOD”", "ref": "LOS ALAMOS SCIENCE · SỐ 15 · 1987",
     "snippet": "song song quy mô lớn với [[hàng nghìn bộ xử lý, thậm chí hàng triệu]] · đường đi Monte Carlo về bản chất rất song song",
     "hlAt": [9, "thậm"], "seal": "DIỄN Ý TỪ BÀI VIẾT 1987", "sealAt": 10},
    {"type": "kinetic", "at": 11, "items": [{"text": "CHIP ĐỒ HOẠ HÔM NAY", "at": 11, "sm": True},
                                            {"text": "VẪN DỰA TRÊN BA SỐ ẤY", "at": [11, "dựa"], "acc": True}]},
    {"type": "print", "at": 12, "img": "feyn0", "tone": "bw",
     "side": {"k": "RICHARD FEYNMAN", "h": "1918 — 1988", "lines": [{"text": "Nobel vật lý *1965*", "at": 13}, {"text": "mất *15.02.1988*", "at": 14}]}},
    {"type": "kinetic", "at": 15, "items": [{"text": "CHUYỆN KÉT SẮT ĐỂ DÀNH", "at": 15, "acc": True}]},
    {"type": "file", "at": 16, "k": "SAU CHIẾN TRANH · MỘT NGÀY THỨ BẢY", "name": "TỦ CỦA\nFREDDY DE HOFFMANN",
     "desc": "Người phụ trách giải mật · bản sao gần như mọi tài liệu",
     "rows": [{"k": "THỬ", "v": "SỐ PI · 31-41-59…", "at": 18}, {"k": "20 PHÚT", "v": "KHÔNG MỞ", "at": 19}],
     "label": {"k": "NGUỒN", "v": FEYN + " · DIỄN Ý", "at": 16}},
    {"type": "kinetic", "at": 20, "items": [{"text": "NGƯỜI LÀM TOÁN → HẰNG SỐ TOÁN HỌC", "at": 20},
                                            {"text": "SỐ e = 2,718281828…", "at": 21, "acc": True}]},
    {"type": "slam", "at": 22, "text": "27 · 18 · 28", "sub": "BA SỐ CỦA SỐ e · TỦ MỞ"},
    {"type": "kinetic", "at": 23, "items": [{"text": "KÉT MỞ", "at": 23, "acc": True},
                                            {"text": "không đoán bừa · đoán con người phía sau ổ khoá", "at": 25, "sm": True}]},
    {"type": "question", "at": 27, "text": "Ngồi vào căn phòng năm 1944,\nbạn chọn chỗ nào?"},
    {"type": "kinetic", "at": 28, "items": [{"text": "VIẾT CHO MÌNH", "at": [28, "viết"]}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [28, "bình"], "acc": True}]},
]}

SPEC = {
    "title": "OPPENHEIMER Ngoài Đời Thật: Feynman Đua Với Máy IBM",
    "channel": "MIM", "theme": "lab", "accent": "#f59e0b", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["số", "khoá", "máy", "người", "thẻ", "mệt", "song", "xúc"],
    "say": SAY, "imgs": IMGS, "chapters": [f"ch{i:02d}" for i in range(13)],
    "youtube": {
        "titles": ["OPPENHEIMER Ngoài Đời Thật: Feynman Đua Với Máy IBM",
                   "OPPENHEIMER Ngoài Đời Thật: Richard Feynman — Căn Phòng Thẻ Đục Lỗ Đã Tính Trước Quả Bom",
                   "OPPENHEIMER Ngoài Đời Thật: Richard Feynman — Trước Khi Có Máy Tính, Người Ta Tính Bom Bằng Gì?"],
        "summary": "Ngày 16/7/1945, lúc 5 giờ 29 phút 45 giây sáng, Richard Feynman, nhà vật lý có tên trong phim OPPENHEIMER (2023), ngồi sau kính chắn gió "
                   "một chiếc xe tải để nhìn vụ thử Trinity bằng mắt thường. Chớp sáng ấy đã được tính trước, khi chưa có máy tính điện tử nào chạy cho Los Alamos: "
                   "bằng những \"máy tính\" người với máy cộng Marchant, rồi bằng dàn máy đục lỗ IBM mà Feynman cho đua với người. "
                   "Video mở một ổ khoá ba số: dây chuyền chia việc, thẻ màu chạy song song, và con xúc xắc điện tử Monte Carlo trên ENIAC năm 1948, "
                   "cùng cái giá ở Hiroshima và Nagasaki.",
        "more": ["Phần lớn chuyện của Feynman lấy từ bài nói của chính ông, \"Los Alamos From Below\" (Engineering & Science, Caltech, 1976); video chỉ diễn ý, "
                 "trích nguyên văn đúng một câu ngắn. Số liệu về nhóm tính tay và máy IBM lấy từ hai bài nghiên cứu của Phòng thí nghiệm Quốc gia Los Alamos "
                 "(N. Lewis; B. J. Archer, 2021); khi lời kể của Feynman và hồ sơ lệch nhau (tốc độ làm bài, số ngày người thợ IBM tới sau), video nói cả hai. "
                 "Giờ nổ 5:29:45 theo tập \"Trinity Site\" của Bảo tàng Nguyên tử Quốc gia Mỹ; vài tài liệu khác ghi lệch vài chục giây. "
                 "Tên diễn viên đóng Feynman trong phim chỉ dựa trên một bài báo giải trí. Số người chết là ước tính của chính quyền thành phố Hiroshima và Nagasaki; "
                 "con số chính xác đến nay vẫn chưa ai biết. Video không dùng hình ảnh nào của bộ phim. Ảnh máy IBM 601, máy Marchant và thẻ đục lỗ là ảnh minh hoạ cùng loại."],
        "chapter_titles": {"ch00": "Mở đầu: sau kính chắn gió một chiếc xe tải (16/7/1945)", "ch01": "Cậu nghiên cứu sinh chưa có bằng",
                           "ch02": "Những \"máy tính\" biết thở", "ch03": "Một vụ nổ không được làm thử", "ch04": "Dây chuyền không có máy (số thứ nhất)",
                           "ch05": "Những thùng máy không có thợ", "ch06": "Ba bài trong chín tháng", "ch07": "Thẻ trắng, thẻ xanh, thẻ vàng (số thứ hai)",
                           "ch08": "Hạn chót ba tuần", "ch09": "Chín mươi giây im lặng", "ch10": "Cái giá: Hiroshima và Nagasaki",
                           "ch11": "Con xúc xắc điện tử: Monte Carlo và ENIAC (số thứ ba)", "ch12": "Ổ khoá mở"},
        "sources": [
            "https://calteches.library.caltech.edu/34/3/FeynmanLosAlamos.htm",
            "https://arxiv.org/pdf/2103.06211",
            "https://arxiv.org/pdf/2103.05705",
            "https://mcnpx.lanl.gov/pdf_files/Article_1987_LAS_Metropolis_125--130.pdf",
            "https://www.tomandmaria.com/Tom/Writing/LosAlamosBetsOnENIAC.pdf",
            "https://www.gutenberg.org/files/277/277.txt",
            "https://www.gutenberg.org/cache/epub/685/pg685.txt",
            "https://www.city.hiroshima.lg.jp/english/peace/1029875/1010074.html",
            "https://nagasakipeace.jp/en/reference/materials/kids/higai.html",
            "https://www.nobelprize.org/prizes/physics/1965/feynman/facts/",
            "https://www.looper.com/1281583/who-does-jack-quaid-play-in-oppenheimer/",
        ],
        "hashtags": ["Oppenheimer", "RichardFeynman", "LịchSửMáyTính", "CôngNghệQuanhTa", "MindInTheMachine"],
        "tags": ["oppenheimer ngoài đời thật", "richard feynman", "feynman los alamos", "dự án manhattan", "máy tính người", "máy ibm đục lỗ",
                 "phương pháp monte carlo", "eniac", "vụ thử trinity", "lịch sử máy tính", "công nghệ quanh ta"],
        "category": "28", "thumb": "t1.jpg", "playlist": "Công Nghệ Quanh Ta", "publish_at": "2026-11-16T13:00:00Z",
        "video_credits": ["Ảnh: Los Alamos National Laboratory (ghi nguồn theo yêu cầu của LANL); Quân đội, Hải quân và chính phủ Mỹ (phạm vi công cộng); "
                          "máy IBM 601: VasuVR, CC BY 4.0; máy Marchant: Bhaiyaji Smile 123, CC0 (ghi tự động theo ảnh)"],
    },
    # Ghi chú làm việc (không lên YouTube): thumbnail dự kiến dùng "feyn0" (CC0, ảnh thẻ Los Alamos của Feynman) + chữ "NGƯỜI vs MÁY";
    # không dùng ảnh/áp phích phim. Pha 2: đọc lại giấy phép từng ảnh, soi lại ảnh "card"/"marchant" (đời sau, chỉ minh hoạ).
    "sources_internal": ["factcheck.md: mọi dòng số liệu / giờ / lời trích", "Commons API LicenseShortName đọc 23/10/2026"],
}


def _norm(w):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


def _anchors(o, path=""):
    """Duyệt mọi mốc dạng int / [dòng, từ, n, lệch] để kiểm tra. Khoá nhận mốc: at, *At, until, hlAt..."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("at", "until", "titleAt", "hlAt", "sealAt", "typeAt", "qline") or k.endswith("At"):
                yield (path + "/" + k, v)
            else:
                yield from _anchors(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _anchors(v, path + f"[{i}]")


def check():
    """Kiểm neo với lines (sau script_lines.py): lỗi nếu dòng không có, từ neo không nằm trong dòng, từ neo là chữ số, hoặc từ neo nằm trong SAY."""
    bad = []
    say = {_norm(k.lstrip("=")) for k in SAY}
    for name, c in CH.items():
        f = D / f"{name}.json"
        if not f.exists():
            bad.append(f"{name}: chưa có {f.name} (chạy script_lines.py trước)")
            continue
        lines = json.loads(f.read_text(encoding="utf-8"))["lines"]
        text = [(x if isinstance(x, str) else x["t"]) for x in lines]
        for si, s in enumerate(c["scenes"]):
            for p, v in _anchors(s):
                if isinstance(v, bool) or not isinstance(v, (int, list)):
                    continue
                cands = v if (isinstance(v, list) and v and isinstance(v[0], list)) else [v]
                for a in cands:
                    i = a if isinstance(a, int) else (a[0] if a else None)
                    if not isinstance(i, int) or isinstance(i, bool) or not (0 <= i < len(text)):
                        bad.append(f"{name} cảnh {si} {p}: dòng {a!r} ngoài phạm vi 0..{len(text) - 1}")
                        continue
                    if isinstance(a, list) and len(a) > 1 and isinstance(a[1], str):
                        w = _norm(a[1])
                        if w.isdigit() or w in say:
                            bad.append(f"{name} cảnh {si} {p}: chữ neo {a[1]!r} là chữ số hoặc nằm trong SAY")
                        toks = [_norm(t) for t in text[i].split()]
                        n = a[2] if len(a) > 2 else 0
                        if toks.count(w) <= n:
                            bad.append(f"{name} cảnh {si} {p}: dòng {i} không có chữ {a[1]!r} (lần {n}): {text[i]}")
    for k in {s.get("img") for c in CH.values() for s in c["scenes"]} | {s.get("bg") for c in CH.values() for s in c["scenes"]} \
            | {s[x]["img"] for c in CH.values() for s in c["scenes"] for x in ("a", "b") if isinstance(s.get(x), dict)}:
        if k and k not in IMGS:
            bad.append(f"ảnh {k!r} không có trong IMGS")
    yt = json.dumps(SPEC["youtube"], ensure_ascii=False)
    for w in ("<", ">", "CẦN", "cần kiểm", "WebFetch", "factcheck", "data/long", "tìm kiếm", "agent"):
        if w in yt:
            bad.append(f"youtube.* có chữ cấm {w!r}")
    if len(SPEC["youtube"]["titles"][0]) > 100:
        bad.append("titles[0] dài hơn 100 ký tự")
    return bad


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương,", sum(len(c["scenes"]) for c in CH.values()), "cảnh")
    bad = check()
    if bad:
        print("NEO LỖI:\n  " + "\n  ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
