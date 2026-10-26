"""Cảnh + spec cho Long MIM `mim-katherine-johnson` (T3B, 26/10/2026).

    python data/long/mim-katherine-johnson/gen_scenes.py            # bản thật: 6 ảnh AI trỏ tới img/ai/ai_NN.png
    python data/long/mim-katherine-johnson/gen_scenes.py --standin  # CHỈ để soát html khi ảnh AI chưa về: thay tạm bằng ảnh tư liệu

Giữ nguyên "lines"/"title" mà script_lines.py đã ghi trong chNN.json; chỉ ghi topic, chapter, hud, scenes.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).parent
TOPIC = "mim-katherine-johnson"
TITLE = "HIDDEN FIGURES Ngoài Đời Thật: Katherine Johnson"
STANDIN = "--standin" in sys.argv

SAY = {
    "katherine": "Ca-thơ-rin", "johnson": "Giôn-xơn", "john": "Giôn", "glenn": "Glen", "friendship": "Phren-síp",
    "mercury": "Mơ-kiu-ri", "atlas": "Át-lát", "nasa": "Na-sa", "naca": "en a xê a", "ibm": "ai bi em",
    "langley": "Lăng-li", "west": "Uét", "virginia": "Vơ-gin-ni-a", "white": "Oai", "sulphur": "Xan-phơ",
    "springs": "Xpơ-rinh", "state": "Xtết", "college": "Có-lịch", "university": "Diu-ni-vơ-xi-ti",
    "claytor": "Clây-tơ", "james": "Giêm", "goble": "Gô-bồ", "dorothy": "Đo-rô-thi", "vaughan": "Von",
    "area": "E-ri-a", "computing": "com-piu-tinh", "computers": "com-piu-tơ", "computer": "com-piu-tơ",
    "maneuver": "Mơ-nu-vơ", "loads": "Lốt", "branch": "Bren-chờ", "henry": "Hen-ri", "pearson": "Pia-sơn",
    "sputnik": "Xpút-ních", "notes": "Nốt", "on": "ơn", "space": "Xpết", "technology": "Tếch-nô-lô-gi",
    "task": "Tát", "group": "Grúp", "freedom": "Phri-đơm", "alan": "A-lan", "shepard": "Se-pợt",
    "washington": "Oa-sinh-tơn", "canaveral": "Ca-na-vơ-rồ", "bermuda": "Bơ-miu-đa",
    "ted": "Tét", "skopinski": "Xcô-pin-xki", "apollo": "A-pô-lô", "module": "mô-đun", "landsat": "Len-xát",
    "barack": "Ba-rắc", "obama": "Ô-ba-ma", "hidden": "Hít-đần", "figures": "Phi-giơ", "time": "Tai",
    "101": "một trăm linh một",
}

IMGS = {
    "kj1966": "File:Katherine Johnson at NASA, in 1966.jpg",                                  # I01 · Public domain (NASA)
    "kjComp": "File:NASA human computers - Katherine Coleman Goble Johnson.jpg",               # I02 · Public domain (NASA)
    "kj1980": "File:Katherine Johnson at NASA Langley Research Center 1980.jpg",               # I03 · Public domain (NASA)
    "kj1983": "File:Katherine Johnson 1983.jpg",                                               # I04 · Public domain (NASA)
    "kj1985": "File:Katherine Johnson 1985.jpg",                                               # I05 · Public domain (NASA)
    "kj2014": "File:Katherine Johnson at NASA Langley in 2014.jpg",                            # I06 · Public domain (NASA)
    "kjMedal": "File:Katherine Johnson Receives Presidential Medal of Freedom.jpg",             # I07 · NASA/Bill Ingalls, no restrictions
    "paper": "File:Johnson NASA Paper.jpg",                                                    # I08 · Public domain (NASA, 09/1960)
    "kjGlobe": "File:Katherine johnson john glenn.png",                                        # I09 · Public domain (NASA, 1960)
    "launch": "EXT:nasa:6205817",          # I14 · Mercury-Atlas 6 cất cánh · images.nasa.gov · PD (media_search get)
    "glennIn": "EXT:nasa:9139490",         # I13 · Glenn vào tàu Friendship 7 · images.nasa.gov · PD
    "orbitCam": "EXT:nasa:s62-00303",      # camera trên Friendship 7 chụp Glenn · images.nasa.gov · PD
    "pad": "EXT:nasa:s62-00490",           # Mercury-Atlas 6 trên bệ, Cape Canaveral · images.nasa.gov · PD
}

# Ảnh AI (prompt: ai_prompts.md). Chủ kênh thả file vào AI_PATH; engine đọc output/long/<topic>/img/<key>.jpg + <key>.json
# (xem báo cáo T3B-ket-qua.md mục "Ảnh AI").
AI_PATH = {f"ai0{n}": f"assets/long/{TOPIC}/img/ai/ai_0{n}.png" for n in range(1, 7)}
STAND = {"ai01": "kjComp", "ai02": "kjGlobe", "ai03": "kj1980", "ai04": "kj1983", "ai05": "kj1985", "ai06": "kj2014"}
if not STANDIN:
    IMGS.update({k: f"EXT:ai:{Path(v).stem}" for k, v in AI_PATH.items()})


def im(key):
    return STAND[key] if STANDIN and key in STAND else key


GEO = {
    "east": {
        "countries": ["United States of America"],
        "context": ["Canada", "Mexico", "Cuba", "Bahamas"],
        "bbox": [-92, 23, -60, 44],
        "pins": [
            {"name": "WSS", "lon": -80.30, "lat": 37.80, "label": "WHITE SULPHUR SPRINGS"},
            {"name": "Washington", "lon": -77.04, "lat": 38.90, "label": "WASHINGTON"},
            {"name": "Canaveral", "lon": -80.60, "lat": 28.40, "label": "CAPE CANAVERAL"},
            {"name": "Bermuda", "lon": -64.75, "lat": 32.30, "label": "BERMUDA"},
        ],
    },
}

CHAPTER_TITLES = {
    "ch00": "Kiểm lại bằng tay",
    "ch01": "Cô bé đi nhanh hơn lớp học",
    "ch02": "Cánh cửa hẹp",
    "ch03": "Computer là một nghề",
    "ch04": "Từ đuôi máy bay tới quỹ đạo",
    "ch05": "Bài kiểm tra tay trước Friendship 7",
    "ch06": "Dấu tên trên báo cáo",
    "ch07": "Ghi nhận muộn và lớp phim",
}

LEDGER = "SỔ CỦA MỘT CON SỐ ĐÁNG TIN"
ROWS = [
    ("HỎI", "VÌ SAO MỘT CON SỐ ĐÁNG TIN?"),
    ("1 · NỀN", "NGƯỜI ĐƯỢC RÈN KỸ TỪ NHỎ"),
    ("2 · VIỆC", "ĐƯỢC TRAO ĐÚNG BÀI TOÁN"),
    ("3 · NGHỀ", "ĐỌC DỮ LIỆU · TÍNH · VẼ ĐỒ THỊ"),
    ("4 · KINH NGHIỆM", "QUEN DỮ LIỆU BAY THẬT"),
    ("5 · ĐỐI CHIẾU", "HAI CÁCH TÍNH · MỘT ĐÁP ÁN"),
    ("6 · TÊN", "CÓ NGƯỜI ĐỨNG TÊN"),
    ("7 · KHỚP", "NGƯỜI VÀ MÁY PHẢI KHỚP"),
]
VM, AIL = "VIDEO MINH HỌA", "ẢNH MINH HỌA"


def chapter(no, k, title, sub, bg, title_at):
    return {"type": "chapter", "no": str(no), "k": k, "title": title, "sub": sub, "bg": im(bg), "titleAt": title_at}


def photo(img, at, key, value, kin=None, illus=None):
    out = {"type": "photo", "at": at, "img": im(img), "tone": "bw", "move": "in", "veil": 0.55,
           "label": {"k": key, "v": value, "at": at}}
    if illus or img.startswith("ai"):
        out["illus"] = illus or AIL
    if img.startswith("ai") and not STANDIN:
        out["credit"] = False   # Claude 26/10: engine tự in "TƯ LIỆU · PHẠM VI CÔNG CỘNG" -> sai với tranh minh hoạ
    if kin:
        out["kin"] = [{"text": kin, "at": at, "acc": True}]
    return out


def broll(vid, at, text):
    return {"type": "broll", "at": at, "vid": vid, "veil": 0.62, "illus": VM, "kin": [{"text": text, "at": at, "acc": True}]}


def kinetic(at, text, small=None):
    items = [{"text": text, "at": at, "acc": True}]
    if small:
        items.append({"text": small, "at": at, "sm": True})
    return {"type": "kinetic", "at": at, "items": items}


def slam(at, text, sub):
    return {"type": "slam", "at": at, "text": text, "sub": sub}


def date(at, day, d, sub):
    return {"type": "date", "at": at, "day": day, "date": d, "sub": {"text": sub, "at": at}}


def print_scene(img, at, head, key, value):
    return {"type": "print", "at": at, "img": im(img), "tone": "bw", "head": head,
            "side": {"k": key, "h": value, "lines": [{"text": value.replace("\n", " · "), "at": at}]}}


def ledger(n, at):
    return {"type": "ledger", "at": at, "title": LEDGER, "srcnote": "MỖI CHẶNG ĐỜI THÊM MỘT DÒNG",
            "rows": [{"k": k, "v": v, "at": at} for k, v in ROWS[:n]]}


def question(at, text):
    return {"type": "question", "at": at, "text": text}


def counter(at, to, suffix, label, frm=0, year=False):
    return {"type": "counter", "at": at, "from": frm, "to": to, "suffix": suffix, "label": label, "year": year}


def timeline(at, bg, items):
    return {"type": "timeline", "at": at, "bg": im(bg), "items": [{"year": y, "text": t} for y, t in items]}


def org(at, nodes):
    return {"type": "org", "at": at, "nodes": nodes}


def a(line, word):
    return [line, word]


def ch00():
    return [
        chapter(0, "MỞ ĐẦU", "KIỂM LẠI\nBẰNG TAY", "20.02.1962 · FRIENDSHIP 7", "pad", a(0, "glenn")),
        kinetic(a(1, "ibm"), "MÁY IBM · PHƯƠNG TRÌNH QUỸ ĐẠO NẠP SẴN", "TỪ LÚC PHÓNG TỚI LÚC RƠI XUỐNG BIỂN"),
        print_scene("glennIn", a(2, "glenn"), "KIỂM TRA TRƯỚC CHUYẾN BAY", "JOHN GLENN", "MỘT YÊU CẦU LẠ"),
        photo("ai03", a(3, "ông"), "CÙNG CON SỐ MÁY VỪA CHẠY", "TỰ TAY TÍNH LẠI"),
        photo("kj1966", a(4, "katherine"), "KATHERINE JOHNSON", "ẢNH: NASA · 1966"),
        slam(a(5, "hidden"), "HIDDEN FIGURES", "BỘ BA ƯU VIỆT · PHIM CHỈ ĐƯỢC NHẮC BẰNG LỜI"),
        date(a(8, "glenn"), "MERCURY-ATLAS 6 · FRIENDSHIP 7", "20.02.1962", "NGƯỜI MỸ ĐẦU TIÊN LÊN QUỸ ĐẠO TRÁI ĐẤT"),
        print_scene("launch", a(9, "mục"), "DỰ ÁN MERCURY", "MỤC TIÊU", "LÊN QUỸ ĐẠO\nQUAN SÁT CON NGƯỜI\nVỀ AN TOÀN"),
        broll("854264", a(11, "theo"), "MÁY ĐIỆN TỬ CÓ THỂ TRỤC TRẶC · MẤT ĐIỆN"),
        slam(a(14, "chuyến"), "4:55:23", "THỜI GIAN BAY CỦA FRIENDSHIP 7"),
        question(a(15, "nhưng"), "VÌ SAO MỘT PHI HÀNH GIA\nTIN CÂY BÚT CỦA BÀ?"),
        ledger(1, a(16, "cuốn")),
    ]


def ch01():
    return [
        chapter(1, "CHƯƠNG MỘT", "CÔ BÉ ĐI NHANH\nHƠN LỚP HỌC", "1918 · WEST VIRGINIA", "kj1983", a(0, "katherine")),
        date(a(0, "white"), "WHITE SULPHUR SPRINGS · WEST VIRGINIA", "26.08.1918", "NGÀY SINH CỦA KATHERINE JOHNSON"),
        photo("ai04", a(1, "13"), "13 TUỔI", "HỌC TRUNG HỌC TRONG KHUÔN VIÊN ĐẠI HỌC"),
        {"type": "map", "at": a(2, "west"), "geo": "east", "tag": "VỊ TRÍ GẦN ĐÚNG", "pins": [{"name": "WSS", "at": a(2, "west")}]},
        slam(a(5, "claytor"), "W. W. SCHIEFFELIN CLAYTOR", "GIÁO SƯ TOÁN · NGƯỜI HƯỚNG DẪN QUAN TRỌNG"),
        counter(a(6, "1937"), 1937, "", "TỐT NGHIỆP LOẠI XUẤT SẮC", frm=1937, year=True),
        photo("ai06", a(8, "bà"), "VIRGINIA", "TRƯỜNG CÔNG LẬP DÀNH CHO HỌC SINH DA ĐEN"),
        broll("3196291", a(10, "với"), "TỪ BỤC GIẢNG TỚI PHÒNG THÍ NGHIỆM?"),
        kinetic(a(12, "tốc"), "THỨ NHẤT: TỐC ĐỘ", "THỨ HAI: MỘT NGƯỜI THẦY"),
        ledger(2, a(16, "dòng")),
        question(a(17, "cánh"), "CÁNH CỬA NĂM 1939\nMỞ RỘNG ĐẾN ĐÂU?"),
    ]


def ch02():
    return [
        chapter(2, "CHƯƠNG HAI", "CÁNH CỬA\nHẸP", "1939 → 1953", "kjComp", a(0, "năm")),
        kinetic(a(1, "johnson"), "3 SINH VIÊN DA ĐEN ĐẦU TIÊN", "WEST VIRGINIA UNIVERSITY · 1939"),
        slam(a(2, "bà"), "NGƯỜI PHỤ NỮ DUY NHẤT", "TRONG BA NGƯỜI ĐƯỢC MỜI"),
        print_scene("kj1983", a(3, "rời"), "SAU HỌC KỲ ĐẦU", "RỜI CAO HỌC", "LẬP GIA ĐÌNH\nVỚI JAMES GOBLE"),
        timeline(a(4, "1952"), "kj1980", [("1937", "TỐT NGHIỆP"), ("1939", "CAO HỌC"), ("1952", "NACA LANGLEY TUYỂN NGƯỜI"), ("1953", "VÀO LANGLEY")]),
        photo("ai01", a(6, "west"), "WEST AREA COMPUTING", "BỘ PHẬN DO DOROTHY VAUGHAN PHỤ TRÁCH"),
        counter(a(8, "mười"), 16, " NĂM", "TỪ TẤM BẰNG TỚI PHÒNG TÍNH TOÁN"),
        broll("5682784", a(10, "hai"), "MANEUVER LOADS BRANCH"),
        kinetic(a(11, "tạm"), "TẠM THỜI → CHÍNH THỨC", "SAU HAI TUẦN"),
        ledger(3, a(13, "dòng")),
        question(a(14, "computer"), "COMPUTER Ở LANGLEY\nLÀ AI?"),
    ]


def ch03():
    return [
        chapter(3, "CHƯƠNG BA", "COMPUTER LÀ\nMỘT NGHỀ", "THẬP NIÊN 1940 · LANGLEY", "kj1985", a(0, "langley")),
        photo("kjComp", a(1, "1940"), "NASA HUMAN COMPUTERS", "ẢNH: NASA", "PHỤ NỮ MỸ GỐC PHI CÓ BẰNG ĐẠI HỌC"),
        slam(a(2, "west"), "WEST AREA COMPUTERS", "KHU LÀM VIỆC TÁCH BIỆT"),
        broll("6272049", a(4, "đọc"), "ĐỌC PHIM DỮ LIỆU · TÍNH · VẼ ĐỒ THỊ"),
        kinetic(a(5, "thước"), "THƯỚC TRƯỢT · MÁY TÍNH CƠ", "MỖI CON SỐ ĐI QUA TAY MỘT NGƯỜI"),
        photo("ai01", a(7, "phân"), "PHÂN BIỆT CHỦNG TỘC · NASA HISTORY", "CHÍNH SÁCH Ở MIỀN NAM VÀ TRONG QUÂN ĐỘI", "KHU ĂN VÀ NHÀ VỆ SINH TÁCH RIÊNG"),
        org(a(10, "johnson"), [
            {"id": "wac", "t": "WEST COMPUTERS", "s": "VÀI TUẦN", "at": a(10, "johnson")},
            {"id": "frd", "t": "FLIGHT RESEARCH DIVISION", "s": "VỚI HENRY PEARSON", "p": "wac", "at": a(11, "phân")},
            {"id": "stf", "t": "SPACE TASK FORCE", "s": "1958", "p": "frd", "at": a(12, "từ")},
        ]),
        broll("8197039", a(12, "bầu"), "TỪ BẢNG SỐ TỚI BẦU TRỜI"),
        ledger(4, a(13, "dòng")),
        question(a(15, "bài"), "BÀI TOÁN ĐẦU TIÊN\nNẰM SAU ĐUÔI MÁY BAY"),
    ]


def ch04():
    return [
        chapter(4, "CHƯƠNG BỐN", "TỪ ĐUÔI MÁY BAY\nTỚI QUỸ ĐẠO", "1953 → 1961", "kj1980", a(0, "trong")),
        photo("ai05", a(1, "tai"), "NHIỄU ĐỘNG VỆT ĐUÔI", "WAKE TURBULENCE"),
        date(a(3, "sputnik"), "LIÊN XÔ PHÓNG SPUTNIK", "1957", "CÔNG VIỆC CỦA JOHNSON ĐỔI HƯỚNG"),
        print_scene("kj1980", a(5, "notes"), "NOTES ON SPACE TECHNOLOGY", "1958", "PHẦN TOÁN HỌC\nCỦA JOHNSON"),
        timeline(a(6, "nasa"), "pad", [("1957", "SPUTNIK"), ("1958", "NACA → NASA"), ("1958", "SPACE TASK GROUP"), ("05.1961", "FREEDOM 7")]),
        kinetic(a(8, "johnson"), "ĐI CÙNG SPACE TASK GROUP", "ĐÃ LÀM VỚI NHIỀU NGƯỜI TRONG NHÓM"),
        broll("9056542", a(10, "tính"), "TÍNH TRƯỚC CHO CHUYẾN BAY CHƯA CẤT CÁNH"),
        slam(a(11, "freedom"), "FREEDOM 7 · 05.1961", "PHÂN TÍCH QUỸ ĐẠO · ALAN SHEPARD"),
        broll("854262", a(12, "đó"), "CHUYẾN BAY CÓ NGƯỜI ĐẦU TIÊN CỦA HOA KỲ"),
        ledger(5, a(14, "dòng")),
        question(a(15, "john"), "CÒN JOHN GLENN\nVÀ QUỸ ĐẠO?"),
    ]


def ch05():
    return [
        chapter(5, "CHƯƠNG NĂM", "BÀI KIỂM TRA\nTAY", "TRƯỚC 20.02.1962", "orbitCam", a(0, "chuẩn")),
        {"type": "map", "at": a(1, "mạng"), "geo": "east", "tag": "VỊ TRÍ GẦN ĐÚNG · MÁY IBM CỦA MẠNG FRIENDSHIP 7",
         "pins": [{"name": "Washington", "at": a(1, "washington")}, {"name": "Canaveral", "at": a(1, "canaveral")},
                  {"name": "Bermuda", "at": a(1, "bermuda")}]},
        org(a(2, "phương"), [
            {"id": "trk", "t": "TRẠM THEO DÕI", "s": "KHẮP THẾ GIỚI", "at": a(2, "phương")},
            {"id": "ibm", "t": "MÁY IBM", "s": "PHƯƠNG TRÌNH QUỸ ĐẠO", "p": "trk", "at": a(2, "máy")},
            {"id": "f7", "t": "FRIENDSHIP 7", "s": "TỪ LÚC PHÓNG TỚI LÚC ĐÁP", "p": "ibm", "at": a(2, "đáp")},
        ]),
        broll("854266", a(4, "glenn"), "PHI HÀNH GIA DÈ CHỪNG MÁY ĐIỆN TỬ"),
        photo("kjGlobe", a(5, "johnson"), "KATHERINE JOHNSON · LANGLEY", "ẢNH: NASA", "CÙNG CON SỐ · CÙNG PHƯƠNG TRÌNH"),
        photo("ai02", a(6, "tay"), "MÁY TÍNH CƠ TRÊN BÀN", "KIỂM BẰNG TAY"),
        {"type": "quote", "at": 8, "text": "Get the girl to check the numbers.", "by": "JOHN GLENN · THEO LỜI KỂ LẠI · NASA LANGLEY",
         "lbl": "TRÍCH DỊCH", "qline": 9, "typeAt": [9, "hãy"]},
        kinetic(a(10, "katherine"), "“CÔ GÁI ẤY” LÀ KATHERINE JOHNSON", "THEO NASA LANGLEY"),
        {"type": "quote", "at": 11, "text": "If she says they're good, then I'm ready to go.", "by": "JOHN GLENN · LỜI JOHNSON KỂ LẠI · TIỂU SỬ NASA",
         "lbl": "TRÍCH DỊCH", "qline": 12, "typeAt": [12, "nếu"]},
        kinetic(a(13, "đây"), "TRÍ NHỚ ≠ BĂNG GHI ÂM", "LỜI KỂ LẠI CỦA JOHNSON"),
        photo("launch", a(16, "glenn"), "MERCURY-ATLAS 6 CẤT CÁNH", "ẢNH: NASA", "20.02.1962 · LÊN QUỸ ĐẠO"),
        ledger(6, a(18, "dòng")),
    ]


def ch06():
    return [
        chapter(6, "CHƯƠNG SÁU", "DẤU TÊN\nTRÊN BÁO CÁO", "1960 → 1969", "paper", a(0, "thật")),
        {"type": "source", "at": a(1, "1960"), "source": "NASA · 09.1960", "ref": "JOHNSON · SKOPINSKI · ĐỒNG TÁC GIẢ",
         "snippet": "[[Determination of Azimuth Angle at Burnout]] for Placing a Satellite Over a Selected Earth Position",
         "hlAt": a(1, "góc"), "seal": "TÊN BÁO CÁO", "sealAt": a(1, "đứng")},
        kinetic(a(2, "vệ"), "ĐẶT VỆ TINH LÊN TRÊN MỘT ĐIỂM ĐÃ CHỌN", "ĐIỂM HẠ CÁNH XÁC ĐỊNH TRƯỚC"),
        photo("paper", a(4, "nasa"), "TRANG ĐẦU BÁO CÁO · 09.1960", "ẢNH: NASA", "LẦN ĐẦU MỘT PHỤ NỮ Ở PHÂN BAN ĐỨNG TÊN"),
        broll("854266", a(6, "apollo"), "SAU MERCURY LÀ APOLLO"),
        date(a(7, "apollo"), "APOLLO 11 · HẠ CÁNH MẶT TRĂNG", "1969", "JOHNSON TÍNH QUỸ ĐẠO"),
        print_scene("kj1985", a(9, "module"), "ĐÓNG GÓP LỚN NHẤT · THEO CHÍNH BÀ", "APOLLO", "LUNAR MODULE\n↔ COMMAND AND SERVICE MODULE"),
        question(a(11, "bạn"), "VẾ KHÓ NHẤT\nCỦA DỰ ÁN MERCURY?"),
        slam(a(12, "đưa"), "ĐƯA NGƯỜI VỀ AN TOÀN", "TỪ MERCURY TỚI APOLLO"),
        ledger(7, a(14, "dòng")),
    ]


def ch07():
    return [
        chapter(7, "CHƯƠNG BẢY", "GHI NHẬN MUỘN\nVÀ LỚP PHIM", "1986 → 2020", "kj2014", a(0, "năm")),
        counter(a(1, "26"), 26, " BÁO CÁO", "VIẾT HOẶC ĐỒNG VIẾT TRONG 33 NĂM"),
        photo("kjMedal", a(2, "obama"), "PRESIDENTIAL MEDAL OF FREEDOM", "24.11.2015 · ẢNH: NASA / BILL INGALLS"),
        date(a(3, "2017"), "KATHERINE G. JOHNSON COMPUTATIONAL RESEARCH FACILITY", "22.09.2017", "NASA LANGLEY CẮT BĂNG KHÁNH THÀNH"),
        kinetic(a(5, "phim"), "PHIM ≠ HỒ SƠ", "NHƯNG PHIM GIÚP TÊN BÀ ĐI XA"),
        print_scene("kj2014", a(6, "nasa"), "NASA GIẢI THÍCH", "CẢNH NHÀ VỆ SINH", "KHÔNG XẢY RA\nVỚI CHÍNH BÀ"),
        slam(a(8, "time"), "THEO TIME", "CẢNH GỌI ĐIỆN SÁT GIỜ PHÓNG ĐÃ ĐƯỢC NÉN LẠI"),
        broll("3196425", a(11, "một"), "MỘT NGƯỜI NGỒI TÍNH LẠI BẰNG TAY"),
        timeline(a(12, "katherine"), "kj1966", [("1953", "VÀO LANGLEY"), ("1986", "NGHỈ HƯU"), ("2015", "HUÂN CHƯƠNG TỰ DO"), ("2020", "QUA ĐỜI · 101 TUỔI")]),
        ledger(8, a(15, "con")),
        question(a(17, "ai"), "AI ĐÃ KIỂM LẠI CON SỐ NÀY,\nVÀ BẰNG CÁCH NÀO?"),
    ]


SCENES = [ch00, ch01, ch02, ch03, ch04, ch05, ch06, ch07]

SOURCES = [
    "https://www.nasa.gov/history/friendship7/index.html",
    "https://www.nasa.gov/centers-and-facilities/langley/katherine-johnson-biography/",
    "https://www.nasa.gov/history/langleys-computers-1935-1970/",
    "https://www.nasa.gov/general/from-computers-to-leaders-women-at-nasa-langley/",
    "https://www.nasa.gov/image-article/katherine-johnson-receives-presidential-medal-of-freedom-2/",
    "https://www.nasa.gov/centers-and-facilities/ivv/nasa-langleys-katherine-johnson-computational-research-facility-officially-opens/",
    "https://www.nasa.gov/podcasts/houston-we-have-a-podcast/nasa-in-hollywood/",
    "https://time.com/4594571/hidden-figures-john-glenn-space-race/",
    "https://www.nasa.gov/history/friendship7/pages/photos.html",
]


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
        "geo": GEO,
        "chapters": [f"ch{i:02d}" for i in range(len(SCENES))],
        "youtube": {
            "titles": [
                TITLE,
                "Katherine Johnson 1962: Phép Tính Tay Trước Friendship 7",
                "John Glenn 1962: Vì Sao Ông Đòi Tính Lại Bằng Tay?",
            ],
            "publish_at": "2026-11-25T13:00:00Z",
            "playlist": "Công Nghệ Quanh Ta",
            "category": "28",
            "thumb": "t1.jpg",
            "summary": "Trước chuyến bay quỹ đạo đầu tiên của nước Mỹ năm 1962, các máy tính IBM đã được nạp sẵn phương trình dẫn đường cho Friendship 7. Vậy mà John Glenn vẫn muốn một người phụ nữ ở Langley tính lại cùng những con số ấy bằng tay. Đó là Katherine Johnson. Từ cô bé học vượt lớp ở West Virginia, qua phòng West Area Computing tách biệt, tới những phép tính cho Freedom 7, Friendship 7 và Apollo, đây là câu chuyện ngoài đời thật phía sau bộ phim Hidden Figures, và lý do một con số chỉ đáng tin khi người và máy cùng khớp.",
            "more": [
                "Các lời trích trong video là bản dịch sang tiếng Việt; hai câu của John Glenn là lời được kể lại theo NASA, không phải bản ghi âm nguyên văn.",
                "Hidden Figures (Bộ Ba Ưu Việt) chỉ được nhắc bằng lời và chữ; video không sử dụng hình ảnh từ phim.",
                "Video Pexels có nhãn VIDEO MINH HỌA, không tái hiện một người hay một sự kiện cụ thể.",
            ],
            "chapter_titles": CHAPTER_TITLES,
            "sources": SOURCES,
            "tags": ["Katherine Johnson", "Hidden Figures", "Bộ Ba Ưu Việt", "John Glenn", "Friendship 7", "NASA",
                     "Project Mercury", "human computer", "lịch sử công nghệ", "máy tính", "tàu vũ trụ", "Apollo 11",
                     "West Area Computing", "công nghệ quanh ta"],
            "hashtags": ["KatherineJohnson", "HiddenFigures", "NASA", "CôngNghệQuanhTa", "MindInTheMachine"],
            "video_credits": [
                "Ảnh Katherine Johnson và báo cáo năm 1960: NASA qua Wikimedia Commons, Public domain.",
                "Ảnh chuyến bay Friendship 7: NASA Image and Video Library, Public domain.",
                "Video minh họa: Pexels.",
            ],
        },
        "sources_internal": "Chỉ dùng kho facts.md (T3A, đã duyệt). Ảnh Commons I01–I09 và 4 ảnh images.nasa.gov tải bằng media_search; 6 ảnh minh họa theo ai_prompts.md, chủ kênh tạo.",
    }


def main():
    spec = make_spec()
    (ROOT / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for i, build_scenes in enumerate(SCENES):
        f = ROOT / f"ch{i:02d}.json"
        out = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}   # giữ lines/title của script_lines.py
        out.update({"topic": TOPIC, "chapter": i,
                    "hud": {"k": f"CHƯƠNG {i:02d}", "t": CHAPTER_TITLES[f"ch{i:02d}"].upper()},
                    "scenes": build_scenes()})
        f.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Đã tạo spec.json và {len(SCENES)} chương cho {TOPIC}" + (" (BẢN THAY TẠM ẢNH AI — đừng render)" if STANDIN else "") + ".")


if __name__ == "__main__":
    main()
