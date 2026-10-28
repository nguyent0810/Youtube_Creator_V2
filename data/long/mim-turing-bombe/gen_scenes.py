from pathlib import Path
import json

ROOT = Path(__file__).parent
TOPIC = "mim-turing-bombe"
TITLE = "NGƯỜI GIẢI MÃ Ngoài Đời Thật: Alan Turing Và Bombe"

SAY = {
    "turing": "Tu-rinh", "enigma": "Ê-ních-ma", "bletchley": "Blétch-li", "park": "Pác",
    "bombe": "bom-bờ", "bombes": "bom-bờ", "welchman": "Uênch-man", "warsaw": "Vác-sa-va",
    "rejewski": "Rây-ép-xki", "paris": "Pa-ri", "clarke": "Cờ-lác", "eastcote": "Ixt-cốt",
    "gordon": "Go-đần", "marian": "Ma-ri-an", "henryk": "Hen-rích", "zygalski": "Di-gan-xki",
    "jerzy": "Giê-di", "różycki": "Ru-dít-xki", "wylie": "Uai-li", "millar": "Mi-lơ",
    "hugh": "Hiu", "alexander": "A-lếch-xan-đờ", "stuart": "Xtiu-ợt", "milner-barry": "Min-nơ Ba-ri",
    "winston": "Uyn-xtơn", "churchill": "Chớc-chin", "gustave": "Gút-xtáp", "bertrand": "Béc-trăng",
    "alastair": "A-la-xtê", "denniston": "Đe-ni-xtơn", "dilly": "Đi-li", "knox": "Nóc",
    "sachsen": "Dắc-xen", "agnus": "Ác-nợt", "dei": "Đê-i", "agnes": "Ác-nịt",
    "stanmore": "Xtan-mo", "kryptologiczna": "crip-tô-lô-ghích-na", "hut": "Hất",
    "crib": "cờ-ríp", "board": "boóc", "plugboard": "plắc-boóc", "u-boat": "u-bốt",
    "sheet": "siit", "tnmoc": "Bảo tàng Máy tính Quốc gia Anh", "gchq": "gi xi ét-chờ kiu",
    "gc&cs": "gi xi và xi ét", "btm": "bi ti em", "wrns": "Ren",
    "158.962.555.217.826.360.000": "khoảng một trăm năm mươi chín tỷ tỷ",
}

IMGS = {
    "turing16": "File:Alan Turing at age 16.jpg",
    "turing1936": "File:Alan Turing (1912-1954) in 1936 at Princeton University.jpg",
    "bletchley": "File:Bletchley Park.jpg",
    "enigmaNsa": "File:Enigma Machine at NSA.jpg",
    "enigmaIwm": "File:EnigmaMachine.jpg",
    "enigmaCc0a": "File:An Enigma machine.jpg",
    "enigmaCc0b": "File:Enigma Machine.jpg",
    "enigmaPair": "File:Enigma machines.jpg",
    "enigmaWarsaw": "File:Enigma machine, Warsaw.jpg",
    "bombeClose": "File:Bombe Closeup.jpg",
    "bombe1945": "File:Wartime picture of a Bletchley Park Bombe.jpg",
}

GEO_EUROPE = {
    "countries": ["Poland", "France", "United Kingdom"],
    "context": ["Germany"],
    "bbox": [-9, 42, 25, 58],
    "pins": [
        {"name": "Warsaw", "lon": 21.01, "lat": 52.23, "label": "WARSAW"},
        {"name": "Pyry", "lon": 21.06, "lat": 52.14, "label": "PYRY"},
        {"name": "Paris", "lon": 2.35, "lat": 48.86, "label": "PARIS"},
        {"name": "Bletchley", "lon": -0.74, "lat": 52.00, "label": "BLETCHLEY PARK"},
    ],
}
GEO_ATLANTIC = {
    "countries": ["United Kingdom", "France"],
    "context": ["Ireland"],
    "bbox": [-20, 42, 10, 61],
    "pins": [
        {"name": "Bletchley", "lon": -0.74, "lat": 52.00, "label": "BLETCHLEY PARK"},
        {"name": "Eastcote", "lon": -0.39, "lat": 51.58, "label": "EASTCOTE"},
        {"name": "Stanmore", "lon": -0.30, "lat": 51.62, "label": "STANMORE"},
    ],
}

TEETH = [
    ("BỨC THƯ", "NGƯỜI XỬ LÝ MÁY"),
    ("KHÓA NGÀY", "ÁP LỰC THỜI GIAN"),
    ("BA LAN", "CÁCH ĐẶT CÂU HỎI"),
    ("NHÓM", "Ý TƯỞNG THÀNH PHƯƠNG PHÁP"),
    ("CRIB VÀ MENU", "GIẢ THUYẾT ĐỂ THỬ"),
    ("BOMBE", "LOẠI ĐƯỜNG SAI"),
    ("WRNS", "KIỂM TRA ĐIỂM DỪNG"),
    ("LỚP PHIM ẢNH", "AI CHỊU TRÁCH NHIỆM"),
]

def a(line, word):
    return [line, word]

def chapter(no, k, title, sub, bg, title_at):
    return {"type": "chapter", "no": str(no), "k": k, "title": title, "sub": sub, "bg": bg, "titleAt": title_at}

def photo(img, at, key, value, kin=None):
    out = {"type": "photo", "at": at, "img": img, "tone": "bw", "move": "in", "veil": 0.55,
           "label": {"k": key, "v": value, "at": at}}
    if kin:
        out["kin"] = [{"text": kin, "at": at, "acc": True}]
    return out

def broll(vid, at, text):
    return {"type": "broll", "at": at, "vid": vid, "veil": 0.62, "illus": "VIDEO MINH HỌA",
            "kin": [{"text": text, "at": at, "acc": True}]}

def kinetic(at, text, small=None):
    items = [{"text": text, "at": at, "acc": True}]
    if small:
        items.append({"text": small, "at": at, "sm": True})
    return {"type": "kinetic", "at": at, "items": items}

def print_scene(img, at, head, key, value):
    return {"type": "print", "at": at, "img": img, "tone": "bw", "head": head,
            "side": {"k": key, "h": value, "lines": [{"text": value, "at": at}]}}

def teeth(n, at):
    return {"type": "ledger", "at": at, "title": "SÁU RĂNG CỦA KHÓA", "srcnote": "MỖI CHƯƠNG THÊM MỘT MẮT XÍCH",
            "rows": [{"k": k, "v": v, "at": at} for k, v in TEETH[:n]]}

def question(at, text):
    return {"type": "question", "at": at, "text": text}

def ch00():
    return [
        chapter(0, "MỞ ĐẦU", "LÁ THƯ\nTRONG ĐÊM", "21.10.1941", "bletchley", a(0, "bốn")),
        broll("34645486", a(1, "alan"), "BỐN CHỮ KÝ VƯỢT CẤP"),
        {"type": "date", "at": a(2, "họ"), "day": "THƯ GỬI CHURCHILL", "date": "21.10.1941", "sub": {"text": "TURING · WELCHMAN · ALEXANDER · MILNER-BARRY", "at": a(2, "họ")}},
        photo("bletchley", a(3, "bombe"), "BLE TCHLEY PARK", "CÔNG VIỆC NHIỀU HƠN NGƯỜI", "MÁY TẠO THÊM VIỆC"),
        kinetic(a(4, "20"), "20 NHÂN VIÊN · 20 ĐÁNH MÁY · WRNS"),
        print_scene("enigmaCc0a", a(6, "máy"), "MÁY QUAY HÀNG GIỜ", "ĐIỂM NGHẼN", "CON NGƯỜI PHẢI NHÌN VÀO"),
        teeth(1, a(9, "sáu")),
        kinetic(a(10, "áp"), "RĂNG ĐẦU: KHÓA ĐỔI LIÊN TỤC"),
        question(a(13, "crib"), "CỖ MÁY, LÁ THƯ VÀ CON NGƯỜI\nPHẢI KHỚP Ở ĐÂU?"),
        photo("bombe1945", a(14, "máy"), "BOMBE THỜI CHIẾN", "CỖ MÁY KHÔNG GỬI ĐIỆN", "ĐIỆN MÃ HÓA VẪN KHÓ ĐỌC"),
    ]

def ch01():
    return [
        chapter(1, "CHƯƠNG MỘT", "KHÓA KHÔNG\nCHỜ BẠN", "NỬA ĐÊM · KHÓA NGÀY", "enigmaNsa", a(0, "máy")),
        broll("2915385", a(1, "dòng"), "MỘT PHÍM, NHIỀU RÔ-TO"),
        photo("enigmaNsa", a(2, "ba"), "ENIGMA", "BA RÔ-TO TRỞ LÊN", "DÒNG ĐIỆN ĐỔI ĐƯỜNG"),
        {"type": "slam", "at": a(3, "khả"), "text": "158.962.555.217.826.360.000", "sub": "KHÔNG GIAN LÝ THUYẾT CỦA ENIGMA"},
        teeth(2, a(5, "hai")),
        kinetic(a(6, "nửa"), "NỬA ĐÊM · THIẾT LẬP ĐỔI"),
        photo("enigmaIwm", a(8, "lục"), "RÔ-TO", "3 TỪ 5 · HẢI QUÂN 3 TỪ 8", "MẠNG KHÔNG DÙNG CÙNG MỘT KHÓA"),
        {"type": "counter", "at": a(9, "khoảng"), "from": 0, "to": 50, "suffix": " MẠNG", "label": "HOẠT ĐỘNG CÙNG LÚC", "year": False},
        print_scene("enigmaNsa", a(11, "đường"), "ĐIỆN VĂN CHẶN ĐƯỢC", "GIÁ TRỊ", "PHẢI TÌM ĐƯỜNG VÀO KỊP LÚC"),
        question(a(13, "loại"), "NẾU KHÔNG ĐỌC THAY CON NGƯỜI,\nBOMBE LOẠI ĐIỀU GÌ?"),
    ]

def ch02():
    return [
        chapter(2, "CHƯƠNG HAI", "BA NGƯỜI\nỞ WARSAW", "12.1932 · WARSAW", "enigmaWarsaw", a(0, "rejewski")),
        photo("enigmaWarsaw", a(0, "rejewski"), "REJEWSKI · RÓŻYCKI · ZYGALSKI", "THÁNG 12 NĂM 1932", "NỀN MÓNG TỪ BA LAN"),
        {"type": "date", "at": a(2, "cung"), "day": "CUNG SACHSEN · WARSAW", "date": "31.12.1932", "sub": {"text": "ĐIỆN ENIGMA ĐẦU TIÊN ĐƯỢC GIẢI", "at": a(2, "cung")}},
        broll("31802320", a(3, "gustave"), "MỘT HỒ SƠ ĐỔI HƯỚNG"),
        {"type": "timeline", "at": a(4, "cyclometer"), "bg": "enigmaWarsaw", "items": [{"year": "12.1932", "text": "PHÁ ENIGMA"}, {"year": "1936", "text": "CYCLOMETER"}, {"year": "09.1938", "text": "BOMBA"}, {"year": "07.1939", "text": "PYRY"}]},
        photo("enigmaPair", a(6, "henryk"), "TẤM ĐỤC LỖ ZYGALSKI", "TÌM THỨ TỰ RÔ-TO", "THAY ĐỔI KHÔNG KẾT THÚC CUỘC CHƠI"),
        kinetic(a(8, "câu"), "ĐỔI CÁCH ĐẶT CÂU HỎI"),
        {"type": "map", "at": a(9, "mật"), "geo": "europe", "pins": [{"name": "Warsaw"}, {"name": "Pyry"}, {"name": "Paris"}, {"name": "Bletchley"}]},
        teeth(3, a(11, "gchq")),
        print_scene("enigmaWarsaw", a(12, "quà"), "TRI THỨC KHÔNG BIẾN MẤT", "TỪ PYRY", "CÁCH GC&CS TIẾP CẬN ENIGMA"),
        question(a(14, "paris"), "MỘT Ý TƯỞNG ĐI TỪ WARSAW\nĐẾN PARIS RA SAO?"),
    ]

def ch03():
    return [
        chapter(3, "CHƯƠNG BA", "NGƯỜI ĐƯỢC NHỚ TÊN\nVÀ CẢ NHÓM", "09.1939 · HUT 8", "turing1936", a(0, "turing")),
        broll("34187599", a(1, "hut"), "HUT 8 · LIÊN LẠC HẢI QUÂN"),
        {"type": "timeline", "at": a(2, "paris"), "bg": "turing1936", "items": [{"year": "09.1939", "text": "HUT 8"}, {"year": "01.1940", "text": "PARIS"}, {"year": "1940", "text": "CLARKE"}, {"year": "1941", "text": "BANBURISMUS"}]},
        {"type": "org", "at": a(3, "gchq"), "nodes": [{"id": "rej", "t": "REJEWSKI", "s": "NỀN MÓNG", "at": a(3, "gchq")}, {"id": "tur", "t": "TURING", "s": "HUT 8", "p": "rej", "at": a(3, "nền")}, {"id": "wel", "t": "WELCHMAN", "s": "DIAGONAL BOARD", "p": "tur", "at": a(3, "thiết")}, {"id": "cla", "t": "CLARKE", "s": "BANBURISMUS", "p": "tur", "at": a(3, "bombe")}]},
        kinetic(a(4, "phim"), "KHÔNG PHẢI MỘT NGƯỜI TRONG PHÒNG KÍN"),
        photo("turing1936", a(6, "gordon"), "GORDON WELCHMAN", "HUT 6 · DIAGONAL BOARD", "MỘT CẢI TIẾN LỚN CHO BOMBE"),
        photo("turing16", a(8, "joan"), "JOAN CLARKE", "HUT 8 · BANBURISMUS", "GIẢM BỚT THỜI GIAN XỬ LÝ"),
        print_scene("turing1936", a(9, "bayes"), "MÁY GIẢM VIỆC", "NGƯỜI", "GIẢM VIỆC CHO MÁY"),
        teeth(4, a(10, "hệ")),
        question(a(15, "crib"), "MỘT CỖ MÁY MUỐN CHẠY\nCẦN ĐIỂM XUẤT PHÁT NÀO?"),
    ]

def ch04():
    return [
        chapter(4, "CHƯƠNG BỐN", "MỘT ĐOẠN CHỮ\nĐỦ DÀI", "01.1941 · CRIB ROOM", "enigmaCc0a", a(0, "crib")),
        kinetic(a(1, "20"), "CRIB · TỪ 20 CHỮ CÁI TRỞ LÊN"),
        photo("enigmaCc0a", a(2, "toàn"), "KHÔNG CẦN CẢ BỨC ĐIỆN", "CHỈ CẦN MỘT MẢNH CÓ LÝ", "GIẢ THUYẾT BẮT ĐẦU TỪ MỘT MẢNH"),
        print_scene("enigmaCc0a", a(3, "dây"), "NẾU ĐOẠN NÀY NẰM Ở ĐÂY", "CÂU HỎI", "DÂY NÀO TỰ MÂU THUẪN"),
        {"type": "slam", "at": a(4, "menu"), "text": "MENU", "sub": "ĐẦU VÀO ĐỂ BOMBE THỬ RÔ-TO"},
        photo("enigmaCc0b", a(5, "bombe"), "BOMBE", "THỬ THIẾT LẬP RÔ-TO", "KHÔNG ĐỌC HỘ CẢ BỨC ĐIỆN"),
        kinetic(a(8, "kiểm"), "GIẢ THUYẾT CÓ TỰ ĐÁ NHAU KHÔNG?"),
        teeth(5, a(11, "đường")),
        {"type": "date", "at": a(12, "shaun"), "day": "SHAUN WYLIE VÀO HUT 8", "date": "01.1941", "sub": {"text": "PHỤ TRÁCH CRIB ROOM", "at": a(12, "shaun")}},
        kinetic(a(13, "wylie"), "WYLIE WOs · THỨ TỰ RÔ-TO ĐỔI"),
        question(a(17, "người"), "SAU ĐIỂM DỪNG CỦA MÁY,\nAI QUYẾT ĐỊNH NÓ ĐÁNG TIN?"),
    ]

def ch05():
    return [
        chapter(5, "CHƯƠNG NĂM", "CỖ MÁY LÀM\nMỘT VIỆC", "08.1940 · AGNUS DEI", "bombeClose", a(0, "tnmoc")),
        broll("6079428", a(1, "kết"), "DIAGONAL BOARD · GIẢM DỪNG GIẢ"),
        kinetic(a(2, "dừng"), "ĐIỂM DỪNG GIẢ KHÔNG PHẢI LỜI GIẢI"),
        photo("bombeClose", a(3, "diagonal"), "DIAGONAL BOARD", "GIẢM CÁC NGÕ CỤT", "THÔNG LƯỢNG TĂNG LÊN"),
        print_scene("bombeClose", a(4, "ngõ"), "GIỜ LAO ĐỘNG", "KHÔNG BỊ NUỐT", "BỞI CÁC NGÕ CỤT"),
        {"type": "date", "at": a(5, "agnus"), "day": "AGNUS DEI · AGNES", "date": "08.1940", "sub": {"text": "BOMBE TỪ TURING VÀ WELCHMAN", "at": a(5, "agnus")}},
        kinetic(a(6, "british"), "BTM · KỸ THUẬT VÀ CHẾ TẠO"),
        photo("bombe1945", a(8, "dây"), "BẢN THIẾT KẾ VÀO XƯỞNG", "DÂY · BÁNH XE · TIẾP ĐIỂM", "Ý TƯỞNG THÀNH QUY TRÌNH"),
        {"type": "counter", "at": a(9, "211"), "from": 0, "to": 211, "suffix": " BOMBE", "label": "ĐƯỢC CHẾ TẠO", "year": False},
        teeth(6, a(11, "dây")),
        question(a(15, "điểm"), "ĐIỂM DỪNG NÀY\nLÀ MANH MỐI HAY LỜI GIẢI?"),
    ]

def ch06():
    return [
        chapter(6, "CHƯƠNG SÁU", "BA CA, MƯỜI MÁY\nMỘT ĐIỂM DỪNG", "11.1943 · EASTCOTE", "bletchley", a(0, "millar")),
        broll("34645486", a(1, "eastcote"), "EASTCOTE · BA CA TÁM GIỜ"),
        {"type": "date", "at": a(3, "10"), "day": "JEAN MILLAR · WRNS", "date": "11.1943", "sub": {"text": "MỖI BAY CÓ 10 BOMBE", "at": a(3, "10")}},
        kinetic(a(4, "hai"), "HAI NGƯỜI · MỘT MÁY · MỘT MENU"),
        print_scene("bletchley", a(5, "bánh"), "NẠP BÁNH XE MÀU", "THEO MENU", "CẮM MẶT SAU THEO CHỈ DẪN"),
        kinetic(a(7, "dừng"), "DỪNG LẠI · GHI THIẾT LẬP"),
        teeth(7, a(10, "bletchley")),
        {"type": "map", "at": a(12, "wrns"), "geo": "atlantic", "pins": [{"name": "Bletchley"}, {"name": "Eastcote"}, {"name": "Stanmore"}]},
        kinetic(a(14, "20"), "20 NỮ NHÂN VIÊN · 20 NGƯỜI ĐÁNH MÁY"),
        photo("enigmaPair", a(17, "dữ"), "DỮ LIỆU · KIỂM TRA · CHUYỂN ĐI", "MẮT XÍCH BẮT BUỘC", "HỆ THỐNG NHANH BẰNG ĐIỂM CHẬM NHẤT"),
        question(a(19, "bí"), "BÍ MẬT KÉO DÀI SAU CHIẾN TRANH\nĐỂ LẠI ĐIỀU GÌ?"),
    ]

def ch07():
    return [
        chapter(7, "CHƯƠNG BẢY", "NGƯỜI TRONG\nVÒNG LẶP", "1945 · SAU CHIẾN TRANH", "bombe1945", a(0, "bombes")),
        broll("2915385", a(1, "outstation"), "TỪ BLETCHLEY RA NGOÀI"),
        {"type": "map", "at": a(2, "sau"), "geo": "atlantic", "pins": [{"name": "Bletchley"}, {"name": "Eastcote"}, {"name": "Stanmore"}]},
        kinetic(a(3, "gần"), "CHỈ MỘT PHẦN CÒN LẠI"),
        print_scene("bombeClose", a(3, "2.000"), "BẢN VẼ BTM", "GẦN 40 NĂM", "HỒ SƠ TRỞ VỀ SAU GẦN BỐN THẬP NIÊN"),
        teeth(8, a(4, "nsa")),
        kinetic(a(5, "nút"), "LỊCH SỬ KHÔNG PHẢI PHÉP MÀU"),
        photo("turing16", a(6, "imitation"), "ALAN TURING", "PHIM CHỈ LÀ MỘT LỚP", "KHÔNG DÙNG HÌNH PHIM"),
        {"type": "slam", "at": a(7, "christopher"), "text": "CHRISTOPHER LÀ HƯ CẤU", "sub": "THEO TIME · MÁY NGOÀI ĐỜI LÀ BOMBE"},
        kinetic(a(13, "phương"), "PHƯƠNG PHÁP CẦN NGƯỜI VẬN HÀNH"),
        question(a(19, "trách"), "CÔNG CỤ BẮT ĐẦU TỪ GIẢ ĐỊNH NÀO,\nVÀ AI KIỂM TRA ĐIỂM DỪNG CUỐI?"),
    ]

SCENES = [ch00, ch01, ch02, ch03, ch04, ch05, ch06, ch07]

def make_spec():
    return {
        "topic": TOPIC,
        "title": TITLE,
        "channel": "MIM",
        "theme": "lab",
        "look": "steel",
        "accent": "#f59e0b",
        "master": True,
        "beat2": True,
        "say": SAY,
        "imgs": IMGS,
        "geo": {"europe": GEO_EUROPE, "atlantic": GEO_ATLANTIC},
        "chapters": [f"ch{i:02d}" for i in range(len(SCENES))],
        "youtube": {
            "titles": [
                TITLE,
                "Alan Turing 1941: Bước Ngoặt Của Bombe",
                "Alan Turing 1939: Từ Ba Lan Đến Bombe",
            ],
            "summary": "Đêm 21 tháng 10 năm 1941, Alan Turing và ba đồng nghiệp vượt cấp gửi một lá thư tới Winston Churchill. Từ chiếc khóa Enigma đổi mỗi ngày đến một cỗ máy chỉ biết loại dần đường sai, câu chuyện lần theo những mắt xích con người đã làm nên Bombe. Và khi máy dừng lại, vì sao công việc quan trọng nhất vẫn thuộc về người kiểm tra?",
            "more": [
                "Các lời trích trong video là bản dịch sang tiếng Việt khi nguồn gốc không phải tiếng Việt.",
                "Ảnh Commons và video Pexels có nhãn MINH HỌA, dùng để giải thích bối cảnh chứ không tái hiện một sự kiện cụ thể.",
                "The Imitation Game chỉ được nhắc bằng lời và chữ; video không sử dụng hình phim.",
            ],
            "chapter_titles": {
                "ch00": "Lá thư trong đêm",
                "ch01": "Khóa không chờ bạn",
                "ch02": "Ba người ở Warsaw",
                "ch03": "Người được nhớ tên, và những người giữ mắt xích",
                "ch04": "Một đoạn chữ để mở cả mê cung",
                "ch05": "Cỗ máy không tìm đáp án, nó loại đường sai",
                "ch06": "Ba ca, mười máy, một điểm dừng",
                "ch07": "Người ở trong vòng lặp",
            },
            "sources": [
                "https://www.nationalarchives.gov.uk/explore-the-collection/stories/a-dramatic-plea-for-churchills-help/",
                "https://www.dpma.eu/english/our_office/publications/milestones/computerpioneers/enigma/index.html",
                "https://www.tnmoc.org/bh-2-the-enigma-machine",
                "https://wmi.amu.edu.pl/wydzial/historia/biogramy/marian-rejewski",
                "https://aw.gov.pl/pl/historia/dekryptaz-szyfru-enigmy/104,Dekryptaz-szyfru-Enigmy.html",
                "https://www.gchq.gov.uk/information/the-pyry-forest-meeting",
                "https://www.gchq.gov.uk/information/alan-turing",
                "https://www.gchq.gov.uk/information/gordon-welchman",
                "https://www.gchq.gov.uk/information/joan-clarke",
                "https://www.gchq.gov.uk/information/shaun_wylie",
                "https://www.gchq.gov.uk/person/shaun-wylie",
                "https://www.tnmoc.org/bombe",
                "https://www.gchq.gov.uk/information/international-womens-month-jean-millar",
                "https://www.nsa.gov/History/National-Cryptologic-Museum/Exhibits-Artifacts/Exhibit-View/Article/2719176/world-war-2-enigma/",
                "https://time.com/3609585/the-true-story-of-the-imitation-game/",
            ],
            "tags": ["Alan Turing", "Enigma", "Bombe", "Bletchley Park", "giải mã", "mật mã", "lịch sử công nghệ", "Thế chiến thứ hai", "Joan Clarke", "Marian Rejewski", "Gordon Welchman", "Bletchley", "máy tính", "công nghệ quanh ta"],
            "hashtags": ["AlanTuring", "Enigma", "Bombe", "CôngNghệQuanhTa", "MindInTheMachine"],
            "category": "28",
            "thumb": "t1.jpg",
            "playlist": "Công Nghệ Quanh Ta",
            "publish_at": "2026-11-23T13:00:00Z",
            "video_credits": [
                "Ảnh Commons: Matt Crypto, Karsten Sperling, Garrethe, Brandmeister/Togrul Safarov, Robert-brook và Joshbressers; Public domain hoặc CC0.",
                "Ảnh Alan Turing và Bombe: Public domain; tác giả được ghi theo trang Commons khi có.",
                "Video minh họa: Pexels.",
            ],
        },
        "sources_internal": "Kịch bản chỉ sử dụng kho facts.md; ảnh Wikimedia Commons PD/CC0 và B-roll Pexels được ghi trong facts.md.",
    }

def main():
    (ROOT / "spec.json").write_text(json.dumps(make_spec(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for i, build_scenes in enumerate(SCENES):
        out = {"topic": TOPIC, "chapter": i, "hud": {"k": f"CHƯƠNG {i:02d}", "t": make_spec()["youtube"]["chapter_titles"][f"ch{i:02d}"].upper()}, "scenes": build_scenes()}   # hud: describe.py lấy tiêu đề chương (Claude 26/10)
        (ROOT / f"ch{i:02d}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Đã tạo spec.json và {len(SCENES)} chương cho {TOPIC}.")

if __name__ == "__main__":
    main()
