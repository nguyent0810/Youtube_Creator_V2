"""Sinh spec (imgs/geo/youtube) + hud/bgm/scenes cho data/long/kowloon/chNN.json. Giữ nguyên "lines" (từ script_lines.py).

    python data/long/kowloon/gen_scenes.py
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
RES = json.loads((D.parents[2] / "output/long/kowloon/research.json").read_text(encoding="utf-8"))["images"]

# key -> chỉ số ảnh trong research.json (output/long/kowloon/imglist.txt)
IDX = dict(kwc1898=0, map1915=1, kwc1989=2, gate_plaques=3, street1991=4, park1991=5, yamen=6, model_bronze=7, kawasaki=8,
           kwc1975=9, frontage=10, alley=11, night=12, aerial1989=13, streetmap=14, park2018=15, parkgate=16, model_early=17,
           kwc_tif=24, aerial1989b=33, kowloon1930s=34, aerial_crop=35, kaitak_view=36, kaitak3=37, kaitak_sign=41,
           kaitak1991=45, kaitak1971=47, plane_road=50, li_vos=56, li_1896=63, keying=64, keying_meet=65, nt_proclaim=66,
           nt_takeover=67, kathingwai=69, shameen_map=78, shameen_bund=79, shamian1870=81, swt1950=85, southgate_bw=89,
           park2025=95, southgate_found=98, oldsouthgate=99, yamen_front=105, cannon=106, yamen_night=110, cannon2=112,
           skm_fire=113, hk1960s=119, grocery=121, canal1950s=128, kaitak_hist=143, cockpit1953=145, a300=146,
           checker=147, liberation1945=150, jp1942=166, opium_rest=169, opium_afong=170, wanchai1970s=174,
           convention_map=175, nt_diorama=178, hkmap1950s=186, wires=191, checkerhill=31, park2024=32)
IMGS = {k: RES[i]["file"] for k, i in IDX.items()}

GEO = {
    "region": {"countries": ["China"], "context": ["Taiwan", "Vietnam", "Laos", "Philippines"], "labels": {"China": "TRUNG QUỐC"},
               "bbox": [104.0, 18.0, 124.0, 41.0], "box": [220, 130, 1700, 860],
               "pins": [{"name": "Hồng Kông", "lon": 114.17, "lat": 22.32, "label": "HỒNG KÔNG"},
                        {"name": "Quảng Châu", "lon": 113.26, "lat": 23.13, "label": "QUẢNG CHÂU"},
                        {"name": "Nam Kinh", "lon": 118.8, "lat": 32.06, "label": "NAM KINH"},
                        {"name": "Bắc Kinh", "lon": 116.4, "lat": 39.9, "label": "BẮC KINH"},
                        {"name": "Đài Bắc", "lon": 121.56, "lat": 25.04, "label": "ĐÀI BẮC"}]},
    "world": {"countries": ["United Kingdom", "China"], "context": ["France", "Germany", "Spain", "Italy", "India", "Russia", "Iran", "Egypt",
                                                                 "Saudi Arabia", "Turkey", "Pakistan", "Thailand", "Vietnam", "Myanmar"],
              "labels": {"United Kingdom": "ANH", "China": "TRUNG QUỐC"}, "bbox": [-12.0, 5.0, 125.0, 62.0], "box": [140, 130, 1780, 860],
              "pins": [{"name": "London", "lon": -0.13, "lat": 51.5, "label": "LONDON"},
                       {"name": "Hồng Kông", "lon": 114.17, "lat": 22.32, "label": "HỒNG KÔNG"}]},
}

FILMV = "VIDEO MINH HỌA"


def sc(t, at=None, **k):
    d = {"type": t}
    if at is not None:
        d["at"] = at
    d.update(k)
    if t == "photo" and d.get("kin"):          # chữ phủ đỏ trên ảnh sepia/sáng: nền phải đủ tối mới đọc được
        d["veil"] = max(d.get("veil", 0), 0.52)
    return d


def kin(*items):
    out = []
    for it in items:
        text, at, *rest = it
        e = {"text": text, "at": at}
        for r in rest:
            e[r] = True
        out.append(e)
    return out


def chapter(no, k, title, sub, word, **bg):
    return sc("chapter", None, no=no, k=k, title=title, sub=sub, titleAt=[0, word], **bg)


CH = {}

# ---------------- CH00 ----------------
CH["ch00"] = dict(hud={"k": "MỞ ĐẦU", "t": "MÁI NHÀ DƯỚI CÁNH MÁY BAY"}, bgm={"file": "gathering_darkness.mp3", "at": 0, "gain": 0.13}, scenes=[
    sc("photo", None, img="kaitak_sign", tone="color", move="in", veil=0.25, kin=kin(("DƯỚI 200 MÉT", [0, "200"], "acc")),
       label={"k": "SÂN BAY KHẢI ĐỨC · HỒNG KÔNG", "v": "CUA GẤP SANG PHẢI", "at": [0, "cua"]}),
    sc("photo", 1, img="aerial1989", tone="color", move="in", veil=0.3, kin=kin(("MỘT KHỐI BÊ TÔNG", [1, "khối"]))),
    sc("counter", 2, bg="kwc_tif", **{"from": 0, "to": 350}, countAt=[2, "Ba"], label="TÒA NHÀ DÍNH CHẶT VÀO NHAU",
       sub={"text": "CAO MƯỜI BỐN TẦNG", "at": [2, "mười"]}),
    sc("kinetic", 3, bg="kwc1989", items=kin(("KHÔNG KHE HỞ", [3, "khe"]), ("KHÔNG QUẢNG TRƯỜNG", [3, "quảng"]), ("GẦN NHƯ KHÔNG CÓ BẦU TRỜI", [3, "bầu"], "acc"))),
    sc("counter", 4, bg="aerial_crop", **{"from": 0, "to": 33000}, countAt=[4, "33.000"], label="NGƯỜI · TRÊN 2,6 HECTA",
       sub={"text": "≈ BA SÂN BÓNG ĐÁ", "at": [4, "ba"]}),
    sc("slam", 5, bg="aerial1989b", text="MẬT ĐỘ CAO NHẤT\nHÀNH TINH", hitAt=[5, "cao"], sub="≈ 1,2 TRIỆU NGƯỜI / KM² · 1987"),
    sc("photo", 6, img="alley", tone="bw", move="in", veil=0.3, kin=kin(("ÁNH MẶT TRỜI KHÔNG CHẠM TỚI", [6, "mặt"]))),
    sc("broll", 7, vid="4761733", tone="noir", veil=0.35, illus=FILMV, kin=kin(("ĐÈN HUỲNH QUANG · GIỮA TRƯA", [7, "huỳnh"]))),
    sc("broll", 8, vid="14090580", tone="night", veil=0.35, illus=FILMV, kin=kin(("NHỮNG CON PHỐ THẮP NẾN", [8, "thắp"]), ("CHO NGƯỜI NGHIỆN", [8, "nghiện"], "acc"))),
    sc("kinetic", 9, bg="night", items=kin(("NHA SĨ KHÔNG GIẤY PHÉP", [9, "nha"]), ("XƯỞNG CÁ VIÊN", [9, "cá"]), ("SÒNG BẠC · NHÀ THỔ", [9, "sòng"], "acc"))),
    sc("broll", 10, vid="3350820", tone="noir", veil=0.4, illus=FILMV, kin=kin(("CẢNH SÁT CHỈ VÀO", [10, "cảnh"]), ("KHI ĐI THÀNH ĐOÀN", [10, "đoàn"], "acc"))),
    sc("kinetic", 11, vid="10244482", tone="night", items=kin(("2024", [11, "2024:"], "sm"), ("CỬU LONG THÀNH TRẠI", [11, "Cửu"], "serif"), ("VÂY THÀNH", [11, "Vây"], "acc"))),
    sc("broll", 12, vid="13633629", tone="night", veil=0.35, illus=FILMV, kin=kin(("CỔ THIÊN LẠC · HỒNG KIM BẢO", [12, "Cổ"]), ("HẺM RỘNG MỘT SẢI TAY", [12, "sải"], "acc"))),
    sc("slam", 13, bg="street1991", text="NGOÀI ĐỜI THẬT\nCÒN KỲ LẠ HƠN", white=True, hitAt=[13, "kỳ"]),
    sc("photo", 14, img="map1915", tone="sepia", move="in", veil=0.55, kin=kin(("TRÊN GIẤY TỜ", [14, "giấy"]), ("KHÔNG THUỘC VỀ HỒNG KÔNG", [14, "không"], "acc"))),
    sc("split", 15, title="MỘT MẢNH ĐẤT · HAI CHỦ QUYỀN", a={"img": "nt_takeover", "label": "ANH: KHÔNG CAI TRỊ", "at": [15, "Anh"]},
       b={"img": "li_1896", "label": "TRUNG QUỐC: KHÔNG CAI QUẢN", "at": [16, "Trung"]}),
    sc("slam", 17, bg="kwc1989", text="BA KHÔNG QUẢN", white=True, hitAt=[17, "ba"], sub="三不管"),
    sc("kinetic", 18, bg="kwc1898", items=kin(("MỘT PHÁO ĐÀI NHỎ CỦA NHÀ THANH", [18, "pháo"]), ("NỬA THẾ KỶ GIẰNG CO", [18, "giằng"], "acc"))),
    sc("broll", 19, vid="7285454", tone="noir", veil=0.4, illus=FILMV, kin=kin(("MỘT LÃNH SỰ QUÁN BỊ ĐỐT", [19, "đốt"]))),
    sc("question", 20, bg="night", text="Bao nhiêu cuộc đột kích\nđể lấy lại thành trại?"),
    sc("photo", 21, img="southgate_bw", tone="bw", move="in", veil=0.35, kin=kin(("HAI TẤM BIA ĐÁ", [21, "bia"]), ("BIẾN MẤT TRONG CHIẾN TRANH", [21, "biến"], "acc"))),
    sc("slam", 22, bg="gate_plaques", text="CẢ THẾ GIỚI\nĐANG GỌI SAI TÊN", hitAt=[22, "sai"]),
    sc("slam", 23, bg="aerial1989", text="CỬU LONG THÀNH TRẠI", white=True, hitAt=[23, "Cửu"], sub="HỒ SƠ · 1847 — 1994",
       stamp={"text": "BA KHÔNG QUẢN", "at": [23, "Trại."], "x": 1080, "y": 650, "rot": -9}),
    sc("sketch", 24, art="fort", title="Một pháo đài canh chừng người Anh"),
])

# ---------------- CH01 ----------------
CH["ch01"] = dict(hud={"k": "CHƯƠNG 01", "t": "PHÁO ĐÀI CANH CHỪNG NGƯỜI ANH"}, bgm={"file": "echoes_of_time_v2.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("1", "CHƯƠNG MỘT", "PHÁO ĐÀI\nCANH CHỪNG NGƯỜI ANH", "VỊNH CỬU LONG · 1839 — 1854", "Pháo", bg="kwc1898"),
    sc("map", 1, geo="region", pins=[{"name": "Hồng Kông", "label": "VỊNH CỬU LONG", "at": [1, "vịnh"]}], zoom="Hồng Kông", zoomK=1.25),
    sc("broll", 2, vid="2123151", tone="noir", veil=0.35, illus=FILMV, kin=kin(("HÀNG TRĂM NĂM YÊN ẮNG", [2, "trăm"]))),
    sc("photo", 3, img="opium_afong", tone="sepia", move="in", veil=0.35, film=True, kin=kin(("TÀU BUÔN THUỐC PHIỆN", [3, "thuốc"]), ("CỦA NGƯỜI ANH", [3, "Anh"], "acc"))),
    sc("date", 4, bg="shamian1870", day="TRƯỚC CHIẾN TRANH NHA PHIẾN", date="1839", sub={"text": "THÊM QUÂN · THỦY BINH TỚI CỬU LONG", "at": [4, "thủy"]}),
    sc("file", 5, k="HỒ SƠ · NHÀ THANH", name="LẠI ÂN TƯỚC", desc="Tướng chỉ huy ở Cửu Long", bg="kwc1898",
       rows=[{"k": "ĐỐI THỦ", "v": "*Charles Elliot*", "at": [6, "Charles"]}, {"k": "THỜI ĐIỂM", "v": "Mới tới được 2 tháng", "at": [6, "hai"]}]),
    sc("ledger", 7, title="10 NGÀY · 1839", rows=[{"k": "SỐ TRẬN", "v": "6", "at": [7, "sáu"]}, {"k": "THẮNG (THEO BÁO CÁO NHÀ THANH)", "v": "6", "at": [8, "thắng"]}],
       total={"k": "NGUỒN", "v": "BÁO CÁO GỬI TRIỀU ĐÌNH", "at": [8, "triều"]}),
    sc("slam", 9, bg="opium_rest", text="THẮNG TRẬN NHỎ\nTHUA CUỘC CHIẾN LỚN", hitAt=[9, "lớn."]),
    sc("timeline", 10, bg="map1915", items=[{"year": "1842", "text": "Hiệp ước *Nam Kinh*"}, {"year": "", "text": "Đảo Hồng Kông → *nước Anh*"}]),
    sc("broll", 11, vid="2852294", tone="noir", veil=0.35, illus=FILMV, kin=kin(("CỜ ANH BÊN KIA VỊNH", [11, "cờ"]))),
    sc("kinetic", 12, vid="17471485", tone="noir", items=kin(("THUỘC ĐỊA", [12, "thuộc"]), ("TÀU BÈ TẤP NẬP", [12, "tấp"]), ("BUÔN LẬU", [12, "buôn"], "acc"))),
    sc("print", 13, img="keying", tone="color", side={"k": "1846 · LƯỠNG QUẢNG TỔNG ĐỐC", "h": "KỲ ANH", "hAt": [13, "Kỳ"],
       "lines": [{"text": "Xin xây *một tòa thành* ở Cửu Long", "at": [13, "thành"]}, {"text": "Để kiểm soát *tàu thuyền ra vào*", "at": [13, "kiểm"]}]}),
    sc("photo", 14, img="keying_meet", tone="sepia", move="pan", veil=0.35, kin=kin(("KHÔNG TỪ QUỐC KHỐ", [14, "quốc"]), ("QUYÊN GÓP · QUAN LẠI & THƯƠNG NHÂN", [14, "quyên"], "acc"))),
    sc("date", 15, bg="model_early", day="TÒA THÀNH HOÀN THÀNH", date="31.05.1847"),
    sc("sketch", 16, art="fort", title="Tường đá hoa cương · cao 4 m · dày 4,6 m"),
    sc("ledger", 17, title="THÀNH CỬU LONG · 1847", rows=[{"k": "VỌNG LÂU", "v": "6", "at": [17, "sáu"]}, {"k": "CỔNG", "v": "4 · CỔNG CHÍNH HƯỚNG NAM", "at": [17, "bốn"]},
       {"k": "PHÁO", "v": "32", "at": [18, "ba"]}], total={"k": "MẶT BẮC", "v": "TỰA NÚI · KHÔNG PHÁO", "at": [19, "núi"]}),
    sc("photo", 20, img="kwc1898", tone="sepia", move="in", veil=0.3, film=True, kin=kin(("CỔNG NAM", [20, "cổng"]), ("MỘT TẤM BIA ĐÁ KHẮC TÊN THÀNH", [20, "bia"], "acc"))),
    sc("slam", 21, bg="kwc1898", text="HÃY NHỚ\nTẤM BIA ẤY", white=True, hitAt=[21, "nhớ"]),
    sc("kinetic", 22, bg="yamen_front", items=kin(("1847", [22, "Cùng"], "sm"), ("LONG TÂN NGHĨA HỌC", [22, "Long"], "serif"), ("TRƯỜNG MIỄN PHÍ CHO DÂN NGHÈO", [22, "miễn"], "acc"))),
    sc("date", 23, bg="kwc1898", day="TÒA THÀNH BỊ CHIẾM LẦN ĐẦU", date="1854", sub={"text": "LOẠN THÁI BÌNH THIÊN QUỐC", "at": [24, "Thái"]}),
    sc("slam", 24, bg="opium_afong", text="THIÊN ĐỊA HỘI", white=True, hitAt=[24, "Thiên"], sub="天地會 · KHỞI NGHĨA CHIẾM THÀNH"),
    sc("kinetic", 25, vid="14090582", tone="noir", items=kin(("HỘI KÍN", [25, "hội"]), ("TỔ TIÊN CỦA HỘI TAM HOÀNG", [25, "Tam"], "serif", "acc"))),
    sc("broll", 26, vid="9508953", tone="noir", veil=0.4, illus=FILMV, kin=kin(("THUÊ LÍNH ĐÁNH THUÊ TỪ HỒNG KÔNG", [26, "thuê"]))),
    sc("slam", 27, bg="kwc1975", text="MỘT TRĂM NĂM SAU\nHỌ TRỞ LẠI", hitAt=[27, "trở"]),
    sc("kinetic", 28, bg="kwc1975", items=kin(("VÀ LẦN ĐÓ", [28, "lần"], "sm"), ("HỌ Ở LẠI RẤT LÂU", [28, "lâu."], "serif", "acc"))),
    sc("photo", 29, img="convention_map", tone="sepia", move="in", veil=0.35, kin=kin(("MỘT BẢN HIỆP ƯỚC", [30, "hiệp"]), ("ĐỂ LẠI MỘT HÒN ĐẢO", [31, "đảo."], "acc"))),
])

# ---------------- CH02 ----------------
CH["ch02"] = dict(hud={"k": "CHƯƠNG 02", "t": "HÒN ĐẢO TRONG BẢN HIỆP ƯỚC"}, bgm={"file": "deep_haze.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("2", "CHƯƠNG HAI", "HÒN ĐẢO\nTRONG BẢN HIỆP ƯỚC", "TÂN GIỚI · 1898 — 1915", "Hòn", bg="convention_map"),
    sc("kinetic", 1, bg="li_vos", items=kin(("1898", [1, "1898,"], "sm"), ("NHÀ THANH SUY YẾU", [1, "suy"]), ("CƯỜNG QUỐC ĐÒI ĐẤT", [1, "đòi"], "acc"))),
    sc("date", 2, bg="convention_map", day="HIỆP ƯỚC KÝ Ở BẮC KINH", date="09.06.1898"),
    sc("photo", 3, img="convention_map", tone="sepia", move="in", veil=0.3, kin=kin(("THUÊ 99 NĂM", [3, "99"], "acc")),
       label={"k": "BẢN ĐỒ ĐÍNH KÈM HIỆP ƯỚC", "v": "HƠN 200 HÒN ĐẢO", "at": [3, "hai"]}),
    sc("slam", 4, bg="nt_diorama", text="TÂN GIỚI", white=True, hitAt=[4, "Tân"], sub="新界 · NEW TERRITORIES"),
    sc("photo", 5, img="kwc1898", tone="sepia", move="in", veil=0.35, kin=kin(("MỘT NGOẠI LỆ", [5, "ngoại"], "acc"))),
    sc("kinetic", 6, bg="map1915", items=kin(("THÀNH CỬU LONG", [6, "thành"], "serif"), ("VẪN THUỘC NHÀ THANH", [6, "Thanh."], "acc"))),
    sc("file", 7, k="ĐIỀU KIỆN", name="KHÔNG CẢN TRỞ\nPHÒNG THỦ HỒNG KÔNG", desc="Quan lại nhà Thanh được ở lại làm việc", bg="kwc1898"),
    sc("counter", 8, bg="kwc1898", **{"from": 0, "to": 744}, countAt=[8, "744"], label="NGƯỜI TRONG THÀNH · 1898", sub={"text": "PHẦN LỚN LÀ LÍNH", "at": [8, "lính."]}),
    sc("map", 9, geo="region", pins=[{"name": "Hồng Kông", "label": "MỘT CHẤM NHỎ CỦA NHÀ THANH", "at": [9, "chấm"]}], zoom="Hồng Kông", zoomK=1.35),
    sc("photo", 10, img="nt_proclaim", tone="sepia", move="in", veil=0.35, kin=kin(("CHƯA ĐẦY MỘT NĂM", [10, "năm."]))),
    sc("photo", 11, img="kathingwai", tone="bw", move="in", veil=0.35, film=True, kin=kin(("THÁNG 4 · 1899", [11, "Tháng"]), ("CÁC DÒNG HỌ NỔI DẬY", [11, "nổi"], "acc")),
       label={"k": "LÀNG CÓ TƯỜNG BAO CÁT KHÁNH VI", "v": "THẬP NIÊN 1920", "at": [11, "dòng"]}),
    sc("slam", 12, bg="nt_takeover", text="CHIẾN TRANH\nSÁU NGÀY", white=True, hitAt=[12, "sáu"], sub="14 — 19.04.1899"),
    sc("counter", 13, bg="nt_takeover", **{"from": 0, "to": 500}, countAt=[13, "khoảng"], label="DÂN QUÂN TỬ TRẬN", sub={"text": "THUA TRƯỚC PHÁO VÀ TÀU CHIẾN ANH", "at": [13, "pháo"]}),
    sc("kinetic", 14, bg="kwc1898", items=kin(("NGƯỜI ANH NGHI", [14, "nghi"]), ("QUAN TRONG THÀNH GIÚP QUÂN NỔI DẬY", [14, "ngầm"], "acc"))),
    sc("date", 15, bg="nt_takeover", day="QUÂN ANH TIẾN VÀO THÀNH", date="05.1899", stamp={"text": "TRỤC XUẤT", "at": [16, "trục"]}),
    sc("photo", 17, img="nt_proclaim", tone="sepia", move="in", veil=0.4, kin=kin(("SẮC LỆNH · 27.12.1899", [17, "sắc"]))),
    sc("quote", 18, text="Thành Cửu Long, trong suốt thời hạn thuê nói trong Hiệp ước, là một phần không thể tách rời của thuộc địa Hồng Kông của Nữ hoàng.",
       by="SẮC LỆNH VIỆN CƠ MẬT ANH · 1899", lbl="TRÍCH DỊCH", qline=18, typeAt=[18, "Thành"]),
    sc("kinetic", 19, bg="map1915", items=kin(("VỀ LÝ THUYẾT", [19, "lý"], "sm"), ("MỌI CHUYỆN ĐÃ XONG", [19, "xong."], "serif"))),
    sc("slam", 20, bg="li_vos", text="NHÀ THANH\nKHÔNG CHỊU", white=True, hitAt=[20, "không"]),
    sc("print", 21, img="li_vos", tone="color", side={"k": "1900 · TRÊN ĐƯỜNG TỚI QUẢNG CHÂU", "h": "LÝ HỒNG CHƯƠNG", "hAt": [21, "Lý"],
       "lines": [{"text": "Ghé *Hồng Kông*", "at": [21, "ghé"]}, {"text": "Không bao giờ *từ bỏ chủ quyền*", "at": [22, "từ"]}]}),
    sc("kinetic", 23, bg="kwc1898", items=kin(("MỘT TÒA THÀNH NHỎ", [23, "nhỏ"]), ("CHẲNG ĐÁNG GÂY CHUYỆN", [23, "đáng"], "acc"))),
    sc("split", 24, title="1900", a={"img": "nt_takeover", "label": "ANH RÚT QUÂN", "at": [24, "rút"]}, b={"img": "li_1896", "label": "NHƯNG KHÔNG TRẢ THÀNH", "at": [25, "trả"]}),
    sc("slam", 26, bg="map1915", text="CHƯA TỪNG CÓ", hitAt=[26, "chưa"]),
    sc("kinetic", 27, bg="map1915", items=kin(("ANH: ĐẤT CỦA ANH", [27, "Anh,"]), ("NHƯNG KHÔNG ĐƯA LUẬT VÀO", [27, "luật"], "acc"))),
    sc("kinetic", 28, bg="kwc1898", items=kin(("NHÀ THANH: ĐẤT TRUNG HOA", [28, "Trung"]), ("NHƯNG KHÔNG CÒN SỨC", [28, "sức"], "acc"))),
    sc("slam", 29, bg="kwc1898", text="VÙNG ĐẤT\nKHÔNG AI QUẢN", white=True, hitAt=[29, "quản"]),
    sc("date", 30, bg="yamen", day="TRONG THÀNH KHÔNG CÒN AI Ở", date="1904"),
    sc("photo", 31, img="yamen_front", tone="color", move="in", veil=0.35, kin=kin(("DINH QUAN CŨ", [31, "dinh"]), ("TRẠI TẾ BẦN · NGƯỜI GIÀ · TRẺ MỒ CÔI", [31, "tế"], "acc"))),
    sc("evidence", 32, img="map1915", tone="color", maxW=760, maxH=760, callouts=[{"x": 0.62, "y": 0.42, "text": "“PHỐ NGƯỜI HOA”", "at": [32, "Phố"], "side": "r"}]),
    sc("photo", 33, img="kowloon1930s", tone="bw", move="pan", veil=0.35, kin=kin(("ĐIỂM THAM QUAN", [33, "tham"]), ("TÀN TÍCH CỦA TRIỀU ĐẠI ĐÃ MẤT", [33, "tàn"], "acc"))),
    sc("slam", 34, bg="kwc1898", text="NHỮNG BỨC TƯỜNG\nSẮP BIẾN MẤT", hitAt=[34, "biến"]),
])

# ---------------- CH03 ----------------
CH["ch03"] = dict(hud={"k": "CHƯƠNG 03", "t": "BỨC TƯỜNG BỊ THÁO ĐI"}, bgm={"file": "dark_times.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("3", "CHƯƠNG BA", "BỨC TƯỜNG\nBỊ THÁO ĐI", "1933 — 1945", "Bức", bg="kowloon1930s"),
    sc("photo", 1, img="kowloon1930s", tone="bw", move="in", veil=0.3, film=True, kin=kin(("THẬP NIÊN 1930", [1, "1930,"]), ("KHU NHÀ Ổ CHUỘT", [1, "ổ"], "acc"))),
    sc("date", 2, bg="map1915", day="KẾ HOẠCH PHÁ DỠ · LÀM CÔNG VIÊN", date="1933"),
    sc("kinetic", 3, bg="kowloon1930s", items=kin(("ĐỔI ĐẤT · CẤP NHÀ MỚI", [3, "đổi"]), ("NHƯNG QUÁ XA", [4, "xa,"], "acc"), ("KHÔNG CHỊU ĐI", [4, "chịu"]))),
    sc("file", 5, k="ĐƠN KÊU CỨU", name="HƠN 20 HỘ", desc="Gửi thẳng tới chính phủ Trung Hoa Dân Quốc", bg="kowloon1930s",
       rows=[{"k": "NAM KINH", "v": "“*Đất Trung Hoa*”", "at": [6, "đất"]}]),
    sc("slam", 7, bg="kwc1898", text="LẠI MỘT LẦN\nGIẰNG CO", hitAt=[7, "giằng"]),
    sc("kinetic", 8, bg="jp1942", items=kin(("ANH MẠNH TAY HƠN", [8, "mạnh"]), ("CHIẾN TRANH TRUNG NHẬT", [8, "Trung"], "acc"))),
    sc("date", 9, bg="kowloon1930s", day="NHÀ CỬA TRONG THÀNH BỊ SAN PHẲNG", date="1940"),
    sc("ledger", 10, title="CÒN LẠI · 1940", rows=[{"k": "DINH QUAN", "v": "✓", "at": [10, "dinh"]}, {"k": "NGÔI TRƯỜNG", "v": "✓", "at": [10, "trường"]}, {"k": "NHÀ CỔ", "v": "1", "at": [10, "cổ."]}]),
    sc("photo", 11, img="jp1942", tone="bw", move="in", veil=0.35, film=True, kin=kin(("12.1941", [11, "tháng"]), ("NHẬT CHIẾM HỒNG KÔNG", [11, "Nhật"], "acc"))),
    sc("photo", 12, img="canal1950s", tone="bw", move="pan", veil=0.35, kin=kin(("MỞ RỘNG SÂN BAY KHẢI ĐỨC", [12, "Khải"]))),
    sc("slam", 13, bg="kwc1898", text="DỠ TOÀN BỘ\nTƯỜNG THÀNH", hitAt=[13, "dỡ"]),
    sc("photo", 14, img="kaitak_hist", tone="bw", move="in", veil=0.35, kin=kin(("ĐÁ XẾP TỪ 1847", [14, "1847"]), ("CHÔN LÀM NỀN SÂN BAY", [14, "chôn"], "acc"))),
    sc("kinetic", 15, bg="jp1942", items=kin(("NGƯỜI LÀM", [15, "Người"], "sm"), ("TÙ BINH ĐỒNG MINH", [15, "tù"], "serif", "acc"))),
    sc("photo", 16, img="swt1950", tone="bw", move="in", veil=0.3, kin=kin(("TỐNG VƯƠNG ĐÀI", [16, "Tống"]), ("CŨNG BỊ PHÁ", [16, "phá"], "acc")),
       label={"k": "KHỐI ĐÁ TƯỞNG NIỆM VUA TỐNG", "v": "ẢNH 1950 · PHẦN CÒN SÓT LẠI", "at": [16, "hoàng"]}),
    sc("kinetic", 17, bg="liberation1945", items=kin(("1945", [17, "1945,"], "sm"), ("KHÔNG CÒN TƯỜNG", [17, "tường."]), ("KHÔNG CÒN CỔNG", [18, "cổng."], "acc"))),
    sc("photo", 19, img="kwc1898", tone="sepia", move="in", veil=0.45, kin=kin(("TẤM BIA TRÊN CỔNG NAM", [19, "bia"]), ("KHÔNG CÒN Ở ĐÓ", [19, "còn"], "acc"))),
    sc("question", 20, bg="kwc1898", text="Tấm bia đã đi đâu?"),
    sc("kinetic", 21, vid="9442282", tone="noir", items=kin(("MẤT TƯỜNG", [21, "mất"]), ("CHỈ CÒN KHOẢNH ĐẤT TRỐNG", [21, "trống."], "acc"))),
    sc("slam", 22, bg="map1915", text="NÓ THUỘC VỀ AI?", white=True, hitAt=[22, "thuộc"]),
    sc("broll", 23, vid="9508953", tone="noir", veil=0.4, illus=FILMV, kin=kin(("BA NĂM SAU CHIẾN TRANH", [23, "ba"]), ("MỘT TÒA NHÀ BỐC CHÁY", [23, "cháy"], "acc"))),
])

# ---------------- CH04 ----------------
CH["ch04"] = dict(hud={"k": "CHƯƠNG 04", "t": "NGỌN LỬA Ở QUẢNG CHÂU"}, bgm={"file": "oppressive_gloom.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("4", "CHƯƠNG BỐN", "NGỌN LỬA\nỞ QUẢNG CHÂU", "1945 — 1950", "Ngọn", bg="shameen_bund"),
    sc("photo", 1, img="liberation1945", tone="bw", move="in", veil=0.35, film=True, kin=kin(("1945 · NHẬT ĐẦU HÀNG", [1, "đầu"]), ("ANH TRỞ LẠI", [1, "trở"], "acc"))),
    sc("map", 2, geo="region", pins=[{"name": "Nam Kinh", "label": "NỘI CHIẾN QUỐC CỘNG", "at": [2, "nội"]}, {"name": "Hồng Kông", "label": "HỒNG KÔNG", "at": [3, "Hồng"]}],
       routes=[{"from": "Nam Kinh", "to": "Hồng Kông", "at": [3, "chạy"], "until": [3, "Kông."]}]),
    sc("photo", 4, img="hkmap1950s", tone="sepia", move="in", veil=0.35, kin=kin(("KHÔNG TIỀN THUÊ", [4, "thuê,"]), ("KHÔNG GIẤY PHÉP", [4, "phép."], "acc"))),
    sc("counter", 5, bg="kwc1975", **{"from": 0, "to": 2000}, countAt=[5, "hai"], label="NGƯỜI DỰNG LỀU · 1947"),
    sc("kinetic", 6, bg="li_1896", items=kin(("TRUNG HOA DÂN QUỐC", [6, "Dân"]), ("ĐỀ NGHỊ LẬP LÃNH SỰ TRONG THÀNH", [6, "lãnh"], "acc"))),
    sc("file", 7, k="LỆNH CỦA CHÍNH QUYỀN HỒNG KÔNG · 11.1947", name="TỰ DỠ NHÀ\nRỜI ĐI TRONG 2 TUẦN", desc="Áp dụng cho toàn bộ dân trong thành", bg="kwc1975"),
    sc("slam", 8, bg="kwc1975", text="KHÔNG AI ĐI", white=True, hitAt=[8, "ai"]),
    sc("date", 9, vid="7714378", tone="noir", day="CẢNH SÁT & BINH LÍNH KÉO VÀO", date="05.01.1948"),
    sc("ledger", 10, title="05.01.1948", rows=[{"k": "NHÀ BỊ PHÁ", "v": "70+", "at": [10, "bảy"]}, {"k": "BỊ BẮT", "v": "2", "at": [10, "bắt"]}]),
    sc("map", 11, geo="region", pins=[{"name": "Hồng Kông", "at": [11, "Tin"]}, {"name": "Nam Kinh", "label": "NAM KINH", "at": [11, "liền."]}],
       routes=[{"from": "Hồng Kông", "to": "Nam Kinh", "at": [11, "bay"], "until": [11, "liền."]}]),
    sc("file", 12, k="BỘ NGOẠI GIAO TRUNG HOA DÂN QUỐC", name="CÔNG HÀM\nPHẢN ĐỐI", desc="Gửi đại sứ Anh · tháng 1.1948", bg="li_vos"),
    sc("quote", 14, text="Chính phủ Trung Quốc có quyền tài phán đối với thành Cửu Long, và hoàn toàn không có ý định từ bỏ quyền tài phán ấy.",
       by="CÔNG HÀM GỬI ĐẠI SỨ ANH · 08.01.1948", lbl="TRÍCH DỊCH", qline=14, typeAt=[14, "Chính"]),
    sc("photo", 15, img="shameen_bund", tone="sepia", move="in", veil=0.35, kin=kin(("12.01.1948 · QUẢNG CHÂU", [15, "12"]), ("SINH VIÊN KÉO TỚI SA DIỆN", [15, "Sa"], "acc")),
       label={"k": "KHU SA DIỆN · QUẢNG CHÂU", "v": "BƯU THIẾP ĐẦU THẾ KỶ 20", "at": [15, "biểu"]}),
    sc("broll", 16, vid="7285454", tone="noir", veil=0.35, illus=FILMV, kin=kin(("ĐỐT TỔNG LÃNH SỰ QUÁN ANH", [16, "đốt"], "acc"))),
    sc("kinetic", 17, bg="kwc1975", items=kin(("< 3 HECTA · KHÔNG TƯỜNG · KHÔNG CỔNG", [17, "ba"]), ("KHỦNG HOẢNG NGOẠI GIAO", [17, "khủng"], "serif", "acc"))),
    sc("slam", 18, bg="map1915", text="CÂU HỎI THỨ NHẤT", white=True, hitAt=[18, "đầu"], sub="ĐÃ CÓ CÂU TRẢ LỜI"),
    sc("split", 19, title="VÌ SAO KHÔNG BÊN NÀO LÙI?", a={"img": "nt_takeover", "label": "ANH: THỂ DIỆN THUỘC ĐỊA", "at": [19, "thể"]},
       b={"img": "li_vos", "label": "TRUNG QUỐC: MẢNH ĐẤT CUỐI CÙNG", "at": [20, "cuối"]}),
    sc("slam", 21, bg="kwc1975", text="CẢ HAI\nĐỨNG YÊN", hitAt=[21, "đứng"]),
    sc("file", 22, k="BỘ NGOẠI GIAO ANH · 04.02.1948", name="MỘT CÔNG THỨC\nLẠ LÙNG", desc="Đề xuất giải quyết vấn đề thành Cửu Long", bg="nt_proclaim",
       rows=[{"k": "NGUYÊN TẮC", "v": "Trung Quốc *có* quyền tài phán", "at": [23, "nguyên"]}, {"k": "THỰC TẾ", "v": "Trung Quốc *không bao giờ* dùng", "at": [23, "không"]}]),
    sc("map", 24, geo="region", pins=[{"name": "Đài Bắc", "label": "DÂN QUỐC → ĐÀI LOAN", "at": [24, "Đài"]}, {"name": "Bắc Kinh", "label": "CHÍNH QUYỀN MỚI", "at": [25, "Bắc"]}]),
    sc("kinetic", 25, bg="hkmap1950s", items=kin(("“VÀO LÚC THÍCH HỢP”", [25, "thích"], "serif"))),
    sc("kinetic", 26, bg="kwc1975", items=kin(("HỒNG KÔNG", [26, "Hồng"], "sm"), ("BÀN TAY KHÔNG CHẠM", [26, "bàn"], "serif", "acc"))),
    sc("kinetic", 27, bg="kwc1989", items=kin(("HỒNG KÔNG KHÔNG DÁM QUẢN", [27, "dám"]), ("ANH KHÔNG MUỐN QUẢN", [27, "muốn"]), ("TRUNG QUỐC KHÔNG THỂ QUẢN", [27, "thể"], "acc"))),
    sc("slam", 28, bg="kwc1989", text="BA KHÔNG QUẢN", white=True, hitAt=[28, "Ba"], sub="三不管"),
    sc("slam", 29, bg="aerial1989", text="LUẬT DUY NHẤT\nCỦA THÀNH TRẠI", hitAt=[29, "luật"]),
    sc("broll", 30, vid="35735035", tone="noir", veil=0.4, illus=FILMV, kin=kin(("KHÔNG CÓ LUẬT", [30, "không"]), ("SẼ CÓ NGƯỜI ĐẶT LUẬT", [30, "đặt"], "acc"))),
])

if __name__ == "__main__":
    spec = json.loads((D / "spec.json").read_text(encoding="utf-8"))
    spec["imgs"], spec["geo"] = IMGS, GEO
    (D / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    import importlib.util, sys
    extra = D / "gen_scenes2.py"
    if extra.exists():
        spec2 = importlib.util.spec_from_file_location("g2", extra)
        m = importlib.util.module_from_spec(spec2)
        sys.modules["gen_scenes"] = sys.modules[__name__]
        spec2.loader.exec_module(m)
        CH.update(m.CH)
    for name, v in CH.items():
        f = D / f"{name}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        d.update(v)
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(name, len(d["lines"]), "câu", len(d["scenes"]), "cảnh")
