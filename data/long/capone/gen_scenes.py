"""Cảnh viết tay cho Long Al Capone (ch00–ch06; ch07–ch13 ở gen_scenes2.py).

    python data/long/capone/gen_scenes.py
Ảnh: tìm theo một đoạn tên "File:…" trong research.json / commons.json (find() báo lỗi nếu không thấy hoặc trùng).
Không dùng ảnh hiện trường có thi thể. Nhạc theo mood (variety.py chọn bài).
"""
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
sys.path.insert(0, str(ROOT / "motion" / "long"))
from scenekit import FILMV, chapter, kin, sc, write  # noqa: E402

_OD = ROOT / "output" / "long" / D.name
_ALL = [i["file"] for i in json.loads((_OD / "research.json").read_text(encoding="utf-8"))["images"]]
_ALL += [i["file"] for i in json.loads((_OD / "commons.json").read_text(encoding="utf-8"))]
_ALL = list(dict.fromkeys(_ALL))


def find(sub: str) -> str:
    m = [f for f in _ALL if sub in f]
    exact = [f for f in m if f == "File:" + sub]
    if exact:
        return exact[0]
    if len(m) != 1:
        raise SystemExit(f"find({sub!r}): {len(m)} ảnh khớp {m[:4]}")
    return m[0]


IMGS = {k: find(v) for k, v in {
    "al1930": "Al Capone in 1930 (manually dusted).jpg", "al1930c": "Al Capone in 1930 (cropped)(2).jpg", "al1929": "Al Capone in 1929.jpg",
    "al_florida": "Al Capone in Florida.jpg", "mug": "AlCaponemugshotCPD.jpg", "alc_card": "Capone Alcatraz.jpg",
    "record": "criminal record in 1932", "deathcert": "Death certificate of Al Capone.jpg", "grave": "Al Capone's grave.jpg",
    "soup": "Unemployed men queued outside a depression soup kitchen opened in Chicago by Al Capone, 02-1931 - NARA - 541927.jpg",
    "cell_esp": "Al-capone-cell.jpg", "mansion": "Florida-Miami-Al Capones Mansion-1922-1.jpg", "pool": "Miami Beach Home - View of the Pool",
    "brick": "Saint Valentine's Day Massacre brick", "wall_lv": "St. Valentine's Day Massacre (52338016185).jpg",   # wall_lv = bãi cỏ ở 2122 phố Clark ngày nay (ảnh của Stephen Hogan, Chicago), KHÔNG phải bức tường ở Las Vegas
    "bullets": "Bulletfragmentsvalentimesmassacte.jpg",
    "moran": "George 'Bugs' Moran.jpg", "torrio": "Johnny Torrio - 1939.jpg", "torrio_mug": "Johnny Torrio (mugshot, 1936).jpg",
    "obanion": "Dean O'Banion 1921.jpg", "weiss": "Hymie Weiss (cropped).jpg", "ness": "Eliotness.jpg", "ness1931": "Eliot Ness in 1931.jpg",
    "wilson": "Chief of U.S. Secret Service. Washington, D.C., June 11. One of the busiest men", "irey": "Elmer Lincoln Irey.jpg",
    "hoover": "Herbert Hoover Heading To His Inauguration Ceremony (1929).jpg",
    "nyt1919": "19190117 Prohibition - Eighteenth Amendment - The New York Times.jpg", "nyt1933": "After End of Prohibition New York Times 1933 3.jpg",
    "dump": "dumping illegal booze, Santa Ana", "disposal": "5 Prohibition Disposal(9) (cropped).jpg", "wreck": "Policeman and wrecked car and cases of moonshine.jpg",
    "brewery": "clandestine underground brewery", "rx": "Prohibition-era-prescription-for-whiskey.jpg", "still": "Prohibition-era still pot",
    "speakeasy": "Speakeasy, by Guy Pene du Bois.png", "castle": "Caponescastle.jpg", "chi_1927": "Candy Shop, South Michigan Avenue, Chicago, 1927",
    "chi_lasalle": "La Salle Street, Chicago Loop", "holyname": "Holy Name Cathedral - Chicago 02.jpg", "cicero_hall": "Cicero Town Hall.jpg",
    "thompson": "Thompson SMG M1928, AM.006516, 01.jpg", "cadillac": "1929 Cadillac 341-B Sport Phaeton",
    "coney": "Steeplechase Park, Coney Island, 1910 Eugene Wemlinger Brooklyn Museum.jpg", "coney2": "Ferris Wheel, Coney Island, 1910.",
    "brooklyn": "Methodist Church, Flatbush, Brooklyn, ca. 1900.", "brooklyn2": "324 Sackett Street Brooklyn entrance.jpg",
    "esp_air": "Eastern State Penitentiary aerial crop.jpg", "esp": "Eastern State Penitentiary - Philadelphia - Pennsylvania - 09.jpg",
    "atlanta": "Entrance to the federal penitentiary, Atlanta LCCN2002698072.jpg",
    "alc_island": "Alcatraz Island photo Don Ramey Logan.jpg", "alc_cell": "Alcatraz Federal Penitentiary - Cell 181 - Al Capone.jpg",
    "alc_band": "Alcatraz band practice.jpg", "alc_laundry": "Alcatraz laundry.jpg", "alc_broadway": "Broadway Alcatraz.JPG",
    "alc_dining": "Alcatraz Dining Hall prisoners.jpg", "alc_1962": "Alcatraz Island March 1962.jpg", "alc_rules": "Alcatraz cell regulations.jpg",
    "sf": "SF From Marin Highlands3.jpg", "palm": "Palm and Hibiscus Islands and Flamingo Hotel", "palm1938": "A sunset on Palm Island, 1938.png",
    "ohare_butch": "Ensign Edward OHare.jpg", "ohare_air": "Chicago O'Hare International Airport (ORD) Aerial View",
    "ac1923": "Atlantic City Boardwalk 1923.jpg", "fedcourt": "Chicago Federal Court, 1961.jpg", "migrant": "Lange-MigrantMother02.jpg",
    "banjo": "Jazz-Age banjos, American Banjo Museum.jpg", "soup_site": "Al Capone's Soup Kitchen, Chicago IL (5325381287).jpg",
    "grave_mc": "Grave Al Capone.jpg",
}.items()}

GEO = {
    "us": {"countries": ["United States of America"], "context": ["Canada", "Mexico", "Cuba", "Bahamas"], "labels": {},
           "bbox": [-125.0, 24.0, -66.0, 50.0], "box": [200, 130, 1720, 850],
           "pins": [{"name": "Chicago", "lon": -87.63, "lat": 41.88, "label": "CHICAGO"}, {"name": "Brooklyn", "lon": -73.95, "lat": 40.65, "label": "BROOKLYN"},
                    {"name": "Miami", "lon": -80.19, "lat": 25.76, "label": "MIAMI"}, {"name": "Philadelphia", "lon": -75.16, "lat": 39.95, "label": "PHILADELPHIA"},
                    {"name": "Atlantic City", "lon": -74.42, "lat": 39.36, "label": "ATLANTIC CITY"}, {"name": "Atlanta", "lon": -84.39, "lat": 33.75, "label": "ATLANTA"},
                    {"name": "Alcatraz", "lon": -122.42, "lat": 37.83, "label": "ALCATRAZ"}, {"name": "Baltimore", "lon": -76.61, "lat": 39.29, "label": "BALTIMORE"},
                    {"name": "Michigan", "lon": -86.48, "lat": 42.1, "label": "MICHIGAN"}, {"name": "Las Vegas", "lon": -115.14, "lat": 36.17, "label": "LAS VEGAS"},
                    {"name": "Los Angeles", "lon": -118.27, "lat": 33.73, "label": "TERMINAL ISLAND"}]},
}

# b-roll Pexels (đều ngang, SDR)
V = dict(chi_night="1826904", chi_night2="36244318", chi_river="26562654", chi_river2="26562729", chi_air="32520148", el="32334881", el2="30718439",
         vcars="4768729", whiskey="10317805", whiskey2="38917693", barrels="2932297", barrels2="5537827", flowers="36494699", flowers2="6764456",
         tax="11321636", calc="7710744", ledger="30117908", ledger2="4061896", cells="5211616", cells_alc="5243257", alc="29024923",
         sfbay="36434849", sfbay2="35288080", palms="8336610", mansion="15768401", miami="31673932", snow="6415320", snow2="15136751",
         brick="6447294", brick2="7830149", coffee="6531808", trumpet="5257929", band="2941115", train="39499562", train2="26256000",
         soup="5906568", bridge="5123482", bridge2="4865714", hat="3998445", write="7345196", write2="854192", justice="8061659",
         corridor="3192916", piano="10254015", bar="18513380", briefcase="6266764", typew="33068304", press="29906414", gavel="6699964")

CH = {}

CH["ch00"] = dict(hud={"k": "MỞ ĐẦU", "t": "TIẾNG CHÓ SỦA TRÊN PHỐ CLARK"}, bgm={"mood": "tense", "at": 0, "gain": 0.13}, scenes=[
    sc("date", None, vid=V["snow"], tone="night", day="CHICAGO · THỨ NĂM · NGÀY LỄ TÌNH NHÂN", date="14.02.1929"),
    sc("sketch", 1, art="garage", title="Khoảng 10 giờ 30 sáng · ga-ra số 2122 phố Clark"),
    sc("photo", 2, img="cadillac", tone="bw", move="in", illus="ẢNH MINH HỌA · CADILLAC ĐỜI 1929", kin=kin(("TRÔNG GIỐNG HỆT", [2, "giống"]), ("XE CỦA CẢNH SÁT", [2, "cảnh"], "acc"))),
    sc("ledger", 3, title="NHỮNG NGƯỜI BƯỚC XUỐNG", vid=V["brick"], tone="noir", rows=[{"k": "SỐ NGƯỜI", "v": "4, CÓ THỂ 6", "at": [3, "bốn"]}, {"k": "MẶC CẢNH PHỤC", "v": "2", "at": [3, "Hai"]}]),
    sc("counter", 4, vid=V["brick2"], tone="noir", **{"from": 0, "to": 7}, countAt=[4, "bảy"], label="NGƯỜI BÊN TRONG GA-RA"),
    sc("kinetic", 5, vid=V["brick"], tone="noir", items=kin(("NHƯ MỘT CUỘC KHÁM XÉT", [5, "khám"]), ("HỌ QUAY MẶT VÀO TƯỜNG", [5, "quay"], "acc"))),
    sc("broll", 6, vid=V["snow2"], tone="night", veil=0.4, illus=FILMV, kin=kin(("VÀI PHÚT SAU", [6, "Vài"], "sm"), ("CHIẾC CADILLAC RỜI ĐI", [6, "rời"]))),
    sc("kinetic", 7, vid=V["brick2"], tone="noir", items=kin(("CẢ KHU PHỐ", [7, "khu"], "sm"), ("CHỈ CÒN MỘT ÂM THANH", [7, "âm"]))),
    sc("sketch", 8, art="dogbark", title="Một con chó sủa mãi không ngừng trong ga-ra"),
    sc("slam", 9, vid=V["brick"], tone="noir", text="HIGHBALL", white=True, hitAt=[9, "Highball"], sub="TIẾNG SỦA KHIẾN HÀNG XÓM GỌI CẢNH SÁT"),
    sc("dots", 10, vid=V["corridor"], tone="noir", total=7, cols=7, title="BẢY NGƯỜI TRONG GA-RA", groups=[{"from": 0, "n": 6, "cls": "ghost", "at": [10, "bảy"]},
                                                                                                      {"from": 6, "n": 1, "cls": "gold", "label": "MỘT NGƯỜI CÒN SỐNG KHI TỚI BỆNH VIỆN", "at": [10, "một"]}]),
    sc("kinetic", 11, vid=V["corridor"], tone="noir", items=kin(("MỘT TRUNG SĨ CÚI XUỐNG", [11, "trung"]), ("HỎI ĐÚNG MỘT CÂU", [11, "đúng"], "acc"))),
    sc("quote", 12, text="Ai bắn anh?", by="TRUNG SĨ SWEENEY · BỆNH VIỆN, 14.02.1929", lbl="TRÍCH DỊCH", qline=12, typeAt=[12, "Ai"]),
    sc("quote", 13, text="Không ai cả. Không ai bắn tôi.", by="FRANK GUSENBERG", lbl="TRÍCH DỊCH", qline=13, typeAt=[13, "Không"]),
    sc("slam", 14, vid=V["corridor"], tone="noir", text="MANG THEO CÂU TRẢ LỜI", hitAt=[14, "mang"]),
    sc("print", 15, img="moran", tone="bw", side={"k": "NGƯỜI MÀ CÁC TAY SÚNG TÌM", "h": "KHÔNG CÓ MẶT", "hAt": [15, "không"],
       "lines": [{"text": "Đến trễ *vài phút*", "at": [16, "trễ"]}, {"text": "Thấy “xe cảnh sát” · rẽ đi *uống cà phê*", "at": [16, "rẽ"]}]}),
    sc("map", 17, geo="us", pins=[{"name": "Chicago", "at": [17, "Còn"]}, {"name": "Miami", "label": "FLORIDA · GẦN 2.000 KM", "at": [17, "Florida"]}],
       routes=[{"from": "Chicago", "to": "Miami", "at": [17, "cách"], "until": [17, "số"], "bend": 0.15}]),
    sc("photo", 18, img="al1930", tone="bw", kin=kin(("AL", [18, "Al"]), ("CAPONE", [18, "Capone"], "acc")), label={"k": "AL CAPONE", "v": "ẢNH NĂM 1930", "at": [18, "Tên"]}),
    sc("kinetic", 19, vid=V["chi_night"], tone="night", items=kin(("NHỮNG KẺ BẤT KHẢ XÂM PHẠM", [19, "Bất"], "serif"), ("THE UNTOUCHABLES · 1987", [19, "phim"], "sm"))),
    sc("slam", 20, bg="al1930c", text="NGOÀI ĐỜI\nKHÔNG NHƯ VẬY", hitAt=[20, "không"]),
    sc("kinetic", 21, bg="mug", items=kin(("HÀNG TRĂM VỤ ÁN MẠNG", [21, "trăm"]), ("CHƯA MỘT LẦN BỊ KẾT TỘI GIẾT NGƯỜI", [21, "chưa"], "acc"))),
    sc("broll", 22, vid=V["write"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("KHÔNG PHẢI MỘT VIÊN ĐẠN", [22, "viên"]), ("MỘT LÁ THƯ CỦA CHÍNH LUẬT SƯ", [22, "lá"], "acc"))),
    sc("print", 23, img="ness", tone="bw", side={"k": "NGƯỜI HÙNG TRONG PHIM", "h": "ELIOT NESS", "hAt": [23, "người"],
       "lines": [{"text": "Ngoài đời chỉ gặp Capone *đúng một lần*", "at": [23, "đúng"]}]}),
    sc("brand", 24, sub="HỒ SƠ · AL CAPONE"),
    sc("question", 25, bg="wall_lv", text="Ai đã ra lệnh cho bốn người đàn ông\ntrên chiếc Cadillac sáng hôm ấy?"),
    sc("map", 26, geo="us", pins=[{"name": "Chicago", "at": [26, "quay"]}, {"name": "Brooklyn", "label": "BROOKLYN · 1899", "at": [26, "Brooklyn"]}],
       routes=[{"from": "Chicago", "to": "Brooklyn", "at": [26, "về"], "until": [26, "Brooklyn"], "bend": 0.15}]),
])

CH["ch01"] = dict(hud={"k": "CHƯƠNG 01", "t": "BA VẾT SẸO Ở BROOKLYN"}, bgm={"mood": "quiet", "at": 0, "gain": 0.12}, scenes=[
    chapter("1", "CHƯƠNG MỘT", "BA VẾT SẸO\nỞ BROOKLYN", "1899 — 1919", "Ba", bg="brooklyn"),
    sc("date", 1, bg="brooklyn", day="BROOKLYN · NEW YORK", date="17.01.1899"),
    sc("kinetic", 2, vid=V["bridge"], tone="noir", items=kin(("DÂN NHẬP CƯ TỪ GẦN NAPOLI", [2, "nhập"]), ("CHA LÀM THỢ CẮT TÓC", [3, "thợ"], "acc"))),
    sc("kinetic", 4, bg="brooklyn2", items=kin(("MỘT GIA ĐÌNH LAO ĐỘNG", [4, "lao"]), ("KHÔNG AI DÍNH TỚI TỘI PHẠM", [4, "dính"], "sm"))),
    sc("counter", 5, bg="brooklyn", **{"from": 0, "to": 9}, countAt=[5, "chín"], label="ANH CHỊ EM · AL LÀ CON THỨ TƯ"),
    sc("kinetic", 6, vid=V["write2"], tone="noir", items=kin(("Ở TRƯỜNG", [6, "trường"], "sm"), ("TỪNG LÀ HỌC SINH KHÁ", [6, "khá"]))),
    sc("slam", 7, bg="brooklyn2", text="14 TUỔI\nBỊ ĐUỔI HỌC", hitAt=[7, "đuổi"]),
    sc("kinetic", 8, vid=V["bridge2"], tone="noir", items=kin(("KHÔNG BAO GIỜ", [8, "không"], "sm"), ("QUAY LẠI TRƯỜNG NỮA", [8, "quay"]))),
    sc("ledger", 9, title="NHỮNG VIỆC VẶT", bg="coney2", rows=[{"k": "TIỆM KẸO", "v": "ĐỨNG QUẦY", "at": [9, "kẹo"]}, {"k": "SÂN BOWLING", "v": "XẾP KI", "at": [9, "xếp"]},
                                                              {"k": "XƯỞNG ĐÓNG SÁCH", "v": "LÀM CÔNG", "at": [9, "xưởng"]}]),
    sc("photo", 10, img="coney", tone="sepia", film=True, move="pan", kin=kin(("NHỮNG BĂNG TRẺ CON", [10, "băng"]), ("CHIA NHAU TỪNG GÓC PHỐ", [10, "góc"], "acc")),
       label={"k": "CONEY ISLAND · BROOKLYN", "v": "ẢNH NĂM 1910", "at": [10, "Brooklyn"]}),
    sc("print", 11, img="torrio", tone="bw", side={"k": "MỘT NGƯỜI ĐÀN ÔNG TÊN", "h": "JOHNNY TORRIO", "hAt": [11, "Johnny"],
       "lines": [{"text": "Lớn hơn Capone *17 tuổi*", "at": [12, "mười"]}, {"text": "Ăn mặc như nhà buôn · nói năng nhỏ nhẹ", "at": [12, "ăn"]}]}),
    sc("slam", 13, bg="torrio", text="CÁO GIÀ", white=True, hitAt=[13, "Cáo"]),
    sc("kinetic", 14, bg="torrio_mug", items=kin(("HÃY NHỚ CÁI TÊN NÀY", [14, "nhớ"]), ("ÔNG TA SẼ DẠY CAPONE MỌI THỨ", [14, "dạy"], "acc"))),
    sc("date", 15, bg="coney2", day="KHOẢNG NĂM ẤY · GÁC CỬA MỘT QUÁN RƯỢU Ở CONEY ISLAND", date="1917"),
    sc("file", 16, k="CONEY ISLAND · BROOKLYN", name="HARVARD INN", desc="Ông chủ: Frankie Yale, tay anh chị có tiếng", bg="coney"),
    sc("broll", 17, vid=V["bar"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("LỜI KHIẾM NHÃ", [17, "khiếm"]), ("VỚI MỘT CÔ GÁI TRONG QUÁN", [17, "cô"], "sm"))),
    sc("kinetic", 18, vid=V["piano"], tone="noir", items=kin(("ANH TRAI CÔ GÁI", [18, "Anh"], "sm"), ("RÚT DAO", [18, "rút"], "acc"))),
    sc("counter", 19, bg="al1929", **{"from": 0, "to": 3}, countAt=[19, "Ba"], label="NHÁT LÊN MÁ TRÁI"),
    sc("slam", 20, bg="al1930c", text="MẶT SẸO", hitAt=[20, "Mặt"], sub="CÁI TÊN HẮN GHÉT CAY GHÉT ĐẮNG"),
    sc("photo", 21, img="al1929", tone="bw", kin=kin(("LUÔN QUAY MÁ PHẢI", [21, "má"]), ("VỀ PHÍA ỐNG KÍNH", [21, "ống"], "acc")), label={"k": "AL CAPONE", "v": "ẢNH NĂM 1929", "at": [21, "Suốt"]}),
    sc("split", 22, title="LỜI HẮN KỂ VÀ SỰ THẬT", a={"img": "al1930c", "label": "“VẾT THƯƠNG TỪ CHIẾN TRƯỜNG”", "at": [22, "chiến"]},
       b={"img": "record", "label": "CHƯA TỪNG ĐI LÍNH MỘT NGÀY", "at": [23, "lính"]}),
    sc("slam", 24, bg="al_florida", text="SNORKY", white=True, hitAt=[24, "Snorky"], sub="“KẺ ĂN DIỆN” · CÁI TÊN BẠN BÈ GỌI"),
    sc("date", 25, bg="brooklyn", day="CƯỚI MAE, MỘT CÔ GÁI GỐC IRELAND", date="30.12.1918"),
    sc("kinetic", 26, bg="brooklyn2", items=kin(("CON TRAI HỌ: SONNY", [26, "Sonny"]), ("VỪA CHÀO ĐỜI ĐẦU THÁNG ẤY", [26, "chào"], "sm"))),
    sc("broll", 27, vid=V["ledger2"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("THỬ SỐNG LƯƠNG THIỆN", [27, "lương"]), ("LÀM KẾ TOÁN", [27, "kế"], "acc"))),
    sc("map", 28, geo="us", pins=[{"name": "Brooklyn", "at": [28, "Rồi"]}, {"name": "Chicago", "label": "CHICAGO · HƠN 1.000 KM", "at": [28, "thành"]}],
       routes=[{"from": "Brooklyn", "to": "Chicago", "at": [28, "đến"], "until": [28, "số"], "bend": 0.15}]),
    sc("slam", 29, vid=V["chi_air"], tone="noir", text="TORRIO CẦN NGƯỜI", hitAt=[29, "cần"]),
])

CH["ch02"] = dict(hud={"k": "CHƯƠNG 02", "t": "HỌC TRÒ CỦA CÁO GIÀ"}, bgm={"mood": "mystery", "at": 0, "gain": 0.12}, scenes=[
    chapter("2", "CHƯƠNG HAI", "HỌC TRÒ CỦA\nCÁO GIÀ", "CHICAGO · 1919 — 1923", "Học", bg="chi_1927"),
    sc("date", 1, vid=V["chi_river"], tone="noir", day="KHOẢNG NĂM ẤY · AL CAPONE ĐẶT CHÂN TỚI CHICAGO", date="1919"),
    sc("kinetic", 2, vid=V["el"], tone="noir", items=kin(("VIỆC ĐẦU TIÊN", [2, "Việc"], "sm"), ("CHẲNG CÓ GÌ OAI PHONG", [2, "oai"]))),
    sc("file", 3, k="SỐ 2222 ĐẠI LỘ WABASH", name="BỐN CON HAI", desc="Đặt theo chính số nhà của nó", bg="chi_lasalle",
       rows=[{"k": "VIỆC CỦA CAPONE", "v": "Gác cửa · *mời khách*", "at": [3, "gác"]}]),
    sc("org", 5, bg="chi_1927", nodes=[{"id": "c", "t": "BIG JIM COLOSIMO", "s": "ÔNG CHỦ · NHÀ CHỨA, SÒNG BẠC", "cls": "top", "at": [5, "Big"]},
                                      {"id": "t", "t": "JOHNNY TORRIO", "s": "CHÁU · CÁNH TAY PHẢI", "p": "c", "at": [5, "dượng"]},
                                      {"id": "a", "t": "AL CAPONE", "s": "GÁC CỬA", "p": "t", "cls": "acc", "at": [6, "hài"]}]),
    sc("kinetic", 7, vid=V["barrels"], tone="noir", items=kin(("TORRIO NHÌN THẤY", [7, "Torrio"], "sm"), ("MỘT THỨ LỚN HƠN NHIỀU", [7, "lớn"]))),
    sc("date", 8, bg="nyt1919", day="LỆNH CẤM RƯỢU CÓ HIỆU LỰC TRÊN TOÀN NƯỚC MỸ", date="17.01.1920"),
    sc("slam", 9, bg="al1930c", text="SINH NHẬT THỨ 21\nCỦA AL CAPONE", hitAt=[9, "sinh"]),
    sc("ledger", 10, title="TỪ NỬA ĐÊM 17.01.1920", bg="dump", rows=[{"k": "SẢN XUẤT RƯỢU", "v": "PHẠM PHÁP", "at": [10, "sản"]}, {"k": "VẬN CHUYỂN", "v": "PHẠM PHÁP", "at": [10, "vận"]},
                                                                    {"k": "BÁN", "v": "PHẠM PHÁP", "at": [10, "bán"]}, {"k": "UỐNG", "v": "KHÔNG CẤM", "at": [11, "Uống"]}]),
    sc("slam", 12, bg="rx", text="TRÊN 0,5% CỒN\nĐỀU BỊ CẤM", hitAt=[12, "nửa"]),
    sc("photo", 13, img="disposal", tone="bw", film=True, move="in", kin=kin(("CHỈ SAU MỘT ĐÊM", [13, "đêm"]), ("RƠI VÀO TAY GIỚI TỘI PHẠM", [13, "tội"], "acc")),
       label={"k": "ĐỔ BỎ RƯỢU BỊ TỊCH THU", "v": "ẢNH TƯ LIỆU THỜI CẤM RƯỢU", "at": [13, "Chỉ"]}),
    sc("broll", 14, vid=V["whiskey2"], tone="noir", veil=0.35, illus=FILMV, kin=kin(("HÀNG CHỤC TRIỆU NGƯỜI VẪN MUỐN UỐNG", [14, "triệu"]), ("VÀ SẴN SÀNG TRẢ TIỀN", [14, "trả"], "acc"))),
    sc("photo", 15, img="speakeasy", tone="color", kin=kin(("QUÁN RƯỢU LẬU", [15, "quán"]), ("SAU HIỆU GIẶT · TIỆM THUỐC · TẦNG HẦM", [15, "hiệu"], "sm")),
       label={"k": "“SPEAKEASY” · TRANH CỦA GUY PÈNE DU BOIS", "v": "TRANH MINH HỌA", "at": [15, "Những"]}),
    sc("bars", 16, bg="nyt1919", title="QUÁN RƯỢU LẬU Ở NEW YORK · CÁC ƯỚC TÍNH", unit="QUÁN", items=[{"k": "THẤP NHẤT", "v": 30000, "at": [16, "ba"]}, {"k": "CAO NHẤT", "v": 100000, "acc": True, "at": [16, "một"]}]),
    sc("ledger", 17, title="LỰC LƯỢNG THỰC THI LỆNH CẤM", bg="wreck", rows=[{"k": "QUÂN SỐ", "v": "MỎNG", "at": [17, "mỏng"]}, {"k": "LƯƠNG", "v": "THẤP", "at": [17, "lương"]},
                                                                         {"k": "VÀ", "v": "RẤT DỄ MUA", "at": [17, "dễ"]}]),
    sc("split", 18, title="HAI CÁCH NHÌN", a={"img": "torrio", "label": "TORRIO: NHẢY VÀO NGAY", "at": [18, "nhảy"]}, b={"img": "chi_1927", "label": "COLOSIMO: NGẦN NGẠI", "at": [18, "ngần"]}),
    sc("date", 19, vid=V["coffee"], tone="noir", day="BIG JIM COLOSIMO BỊ BẮN CHẾT TRONG QUÁN CỦA MÌNH", date="11.05.1920"),
    sc("kinetic", 20, bg="mug", items=kin(("CAPONE NẰM TRONG SỐ", [20, "Capone"], "sm"), ("NHỮNG NGƯỜI BỊ NGHI", [20, "nghi"]))),
    sc("slam", 21, vid=V["gavel"], tone="noir", text="KHÔNG AI BỊ TRUY TỐ", hitAt=[21, "truy"]),
    sc("kinetic", 22, vid=V["justice"], tone="noir", items=kin(("BẠN SẼ CÒN NGHE CÂU ẤY", [22, "nghe"]), ("NHIỀU LẦN NỮA", [22, "nhiều"], "acc"))),
    sc("org", 23, bg="chi_lasalle", nodes=[{"id": "t", "t": "JOHNNY TORRIO", "s": "LÊN THAY", "cls": "top", "at": [23, "Torrio"]},
                                          {"id": "a", "t": "AL CAPONE", "s": "CÁNH TAY PHẢI", "p": "t", "cls": "acc", "at": [23, "Capone"]}]),
    sc("kinetic", 24, bg="torrio", items=kin(("CHIA ĐỊA BÀN", [24, "chia"]), ("HÒA BÌNH RẺ HƠN CHIẾN TRANH", [24, "hòa"], "acc"))),
    sc("kinetic", 25, vid=V["chi_air"], tone="noir", items=kin(("MỖI BĂNG MỘT KHU", [25, "Mỗi"]), ("KHÔNG AI LẤN SANG AI", [25, "lấn"], "sm"))),
    sc("kinetic", 26, vid=V["chi_river2"], tone="noir", items=kin(("TRONG VÀI NĂM", [26, "vài"], "sm"), ("NGUYÊN TẮC ẤY CÓ TÁC DỤNG", [26, "tác"]))),
    sc("broll", 27, vid=V["briefcase"], tone="noir", veil=0.35, illus=FILMV, kin=kin(("TIỀN ĐỔ VỀ", [27, "Tiền"]), ("KHÔNG AI KỊP ĐẾM", [27, "kịp"], "acc"))),
    sc("counter", 28, bg="still", **{"from": 0, "to": 1200}, countAt=[28, "một"], label="QUÁN RƯỢU LẬU ĐƯỢC BẢO KÊ · THEO MỘT ƯỚC TÍNH"),
    sc("kinetic", 29, bg="fedcourt", items=kin(("MỘT THỊ TRƯỞNG MỚI", [29, "thị"]), ("MUỐN DỌN DẸP THÀNH PHỐ", [29, "dọn"], "acc"))),
    sc("kinetic", 30, vid=V["chi_night2"], tone="night", items=kin(("MỘT CÁCH GIẢI QUYẾT", [30, "cách"], "sm"), ("RẤT GỌN", [30, "gọn"]))),
    sc("slam", 31, bg="cicero_hall", text="MUA HẲN\nMỘT THỊ TRẤN", hitAt=[31, "hẳn"]),
])

CH["ch03"] = dict(hud={"k": "CHƯƠNG 03", "t": "CICERO, THỊ TRẤN BỊ MUA ĐỨT"}, bgm={"mood": "tense", "at": 0, "gain": 0.12}, scenes=[
    chapter("3", "CHƯƠNG BA", "CICERO\nTHỊ TRẤN BỊ MUA ĐỨT", "1924 — 1926", "Cicero", bg="cicero_hall"),
    sc("photo", 1, img="cicero_hall", tone="color", move="in", kin=kin(("CICERO", [1, "Cicero"]), ("HƠN 50.000 DÂN · SÁT RÌA CHICAGO", [1, "sát"], "sm")),
       label={"k": "TÒA THỊ CHÍNH CICERO", "v": "ẢNH NGÀY NAY", "at": [1, "nằm"]}),
    sc("ledger", 2, title="CICERO CÓ", bg="cicero_hall", rows=[{"k": "CHÍNH QUYỀN", "v": "RIÊNG", "at": [2, "chính"]}, {"k": "CẢNH SÁT", "v": "RIÊNG", "at": [2, "cảnh"]},
                                                              {"k": "BẦU CỬ", "v": "RIÊNG", "at": [2, "bầu"]}]),
    sc("date", 3, vid=V["el2"], tone="noir", day="NGÀY BẦU CỬ THỊ TRƯỞNG CICERO", date="01.04.1924"),
    sc("broll", 4, vid=V["vcars"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("NGƯỜI CỦA TORRIO VÀ CAPONE", [4, "Torrio"], "sm"), ("TRÀN VÀO TỪ SÁNG SỚM", [4, "tràn"]))),
    sc("kinetic", 5, bg="thompson", items=kin(("ĐỨNG TRƯỚC CÁC PHÒNG PHIẾU", [5, "phòng"]), ("VỚI SÚNG TRONG TAY", [5, "súng"], "acc"))),
    sc("ledger", 6, title="NGÀY BẦU CỬ Ở CICERO", bg="cicero_hall", rows=[{"k": "CỬ TRI", "v": "BỊ DỌA", "at": [6, "dọa"]}, {"k": "NHÂN VIÊN KIỂM PHIẾU", "v": "BỊ BẮT CÓC", "at": [6, "bắt"]},
                                                                        {"k": "THÙNG PHIẾU", "v": "BỊ CƯỚP", "at": [6, "cướp"]}]),
    sc("kinetic", 7, vid=V["chi_air"], tone="noir", items=kin(("CẢNH SÁT CHICAGO", [7, "Cảnh"]), ("ĐƯỢC CỬ SANG DẸP LOẠN", [7, "dẹp"], "acc"))),
    sc("broll", 8, vid=V["el"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("CẢNH SÁT MẶC THƯỜNG PHỤC", [8, "thường"]), ("CHẠM MẶT MỘT NGƯỜI TRÊN PHỐ", [8, "chạm"], "sm"))),
    sc("slam", 9, vid=V["brick"], tone="noir", text="HỌ NỔ SÚNG", hitAt=[9, "nổ"]),
    sc("file", 10, k="CICERO · 01.04.1924", name="FRANK\nCAPONE", desc="Anh trai của Al", bg="al1930c", stamp={"text": "TỬ VONG", "at": [10, "chết"]}),
    sc("slam", 11, bg="cicero_hall", text="ỨNG VIÊN CỦA BĂNG ĐẢNG\nVẪN THẮNG", hitAt=[11, "thắng"]),
    sc("kinetic", 12, bg="mug", items=kin(("CICERO TỪ ĐÓ", [12, "Cicero"], "sm"), ("THUỘC VỀ CAPONE", [12, "thuộc"], "acc"))),
    sc("kinetic", 13, vid=V["chi_night"], tone="night", items=kin(("VIÊN THỊ TRƯỞNG MỚI HIỂU RÕ", [13, "hiểu"]), ("AI ĐÃ ĐƯA MÌNH LÊN", [13, "đưa"], "acc"))),
    sc("kinetic", 14, vid=V["justice"], tone="noir", items=kin(("TƯƠNG TRUYỀN", [14, "Tương"], "sm"), ("BỊ XÔ NGÃ TRÊN BẬC THỀM TÒA THỊ CHÍNH", [14, "xô"]))),
    sc("slam", 15, vid=V["gavel"], tone="noir", text="KHÔNG CẢNH SÁT NÀO\nCAN THIỆP", hitAt=[15, "can"]),
    sc("kinetic", 16, vid=V["chi_night2"], tone="night", items=kin(("ĐẠI BẢN DOANH", [16, "đại"], "sm"), ("KHÁCH SẠN HAWTHORNE", [16, "Hawthorne"]))),
    sc("broll", 17, vid=V["barrels2"], tone="noir", veil=0.35, illus=FILMV, kin=kin(("SÒNG BẠC MỞ SUỐT NGÀY ĐÊM", [17, "sòng"]), ("XE BIA CHẠY NHƯ XE CHỞ SỮA", [17, "bia"], "acc"))),
    sc("kinetic", 18, vid=V["chi_river"], tone="noir", items=kin(("HAI NĂM SAU", [18, "hai"], "sm"), ("MỘT SỰ VIỆC KHÁC", [18, "sự"]))),
    sc("date", 19, vid=V["bar"], tone="night", day="TRỢ LÝ CÔNG TỐ WILLIAM McSWIGGIN BỊ BẮN CHẾT", date="27.04.1926"),
    sc("kinetic", 20, bg="mug", items=kin(("CAPONE BỊ NGHI", [20, "nghi"]), ("BIẾN MẤT VÀI THÁNG · RỒI TỰ RA TRÌNH DIỆN", [20, "biến"], "sm"))),
    sc("slam", 21, vid=V["gavel"], tone="noir", text="KHÔNG AI BỊ TRUY TỐ", hitAt=[21, "truy"]),
    sc("kinetic", 22, vid=V["justice"], tone="noir", items=kin(("LẦN THỨ HAI", [22, "hai"]), ("BẠN NGHE CÂU NÀY", [22, "nghe"], "sm"))),
    sc("question", 23, bg="fedcourt", text="Vì sao lại như vậy?"),
    sc("counter", 24, vid=V["briefcase"], tone="noir", **{"from": 0, "to": 105}, prefix="$", suffix=" TRIỆU", countAt=[24, "một"], label="MỖI NĂM · ƯỚC TÍNH CỦA VĂN PHÒNG CÔNG TỐ LIÊN BANG"),
    sc("counter", 25, vid=V["calc"], tone="noir", **{"from": 0, "to": 15}, prefix="$", suffix=" TRIỆU", countAt=[25, "mười"], label="MỖI NĂM · CHO MỘT KHOẢN DUY NHẤT: HỐI LỘ"),
    sc("ledger", 26, title="DANH SÁCH NHẬN TIỀN", bg="fedcourt", rows=[{"k": "CẢNH SÁT TUẦN TRA", "v": "●", "at": [26, "Cảnh"]}, {"k": "THẨM PHÁN", "v": "●", "at": [26, "Thẩm"]},
                                                                      {"k": "NGHỊ VIÊN", "v": "●", "at": [26, "Nghị"]}, {"k": "NGƯỜI KIỂM PHIẾU", "v": "●", "at": [26, "Người"]}]),
    sc("kinetic", 27, vid=V["ledger"], tone="noir", items=kin(("ĐỀU LÀ ƯỚC TÍNH", [27, "ước"]), ("BĂNG ĐẢNG KHÔNG ĐỂ LẠI SỔ SÁCH", [27, "sổ"], "acc"))),
    sc("kinetic", 28, vid=V["chi_night2"], tone="night", items=kin(("CẢ THÀNH PHỐ BIẾT", [28, "biết"]), ("AI TRẢ LƯƠNG CHO AI", [28, "trả"], "acc"))),
    sc("counter", 29, bg="chi_1927", **{"from": 0, "to": 729}, countAt=[29, "bảy"], label="VỤ GIẾT NGƯỜI LIÊN QUAN BĂNG ĐẢNG · 1919 — 1933"),
    sc("slam", 30, vid=V["gavel"], tone="noir", text="RẤT ÍT VỤ\nCÓ NGƯỜI BỊ KẾT ÁN", hitAt=[30, "ít"]),
    sc("kinetic", 31, vid=V["corridor"], tone="noir", items=kin(("NHÂN CHỨNG KHÔNG NHỚ GÌ", [31, "nhớ"]), ("NGƯỜI SỐNG SÓT KHÔNG BIẾT AI BẮN", [31, "sống"], "acc"))),
    sc("slam", 32, bg="holyname", text="PHÍA BẮC CHICAGO", hitAt=[32, "bắc"], sub="CÓ MỘT NGƯỜI KHÔNG CHỊU CHIA PHẦN"),
])

CH["ch04"] = dict(hud={"k": "CHƯƠNG 04", "t": "TIỆM HOA VÀ NGAI VÀNG TUỔI 26"}, bgm={"mood": "dark", "at": 0, "gain": 0.12}, scenes=[
    chapter("4", "CHƯƠNG BỐN", "TIỆM HOA VÀ\nNGAI VÀNG TUỔI 26", "1924 — 1926", "Tiệm", bg="holyname"),
    sc("kinetic", 1, vid=V["chi_river2"], tone="noir", items=kin(("PHÍA BẮC CHICAGO", [1, "bắc"]), ("MỘT BĂNG NGƯỜI GỐC IRELAND", [1, "băng"], "acc"))),
    sc("print", 2, img="obanion", tone="bw", side={"k": "THỦ LĨNH BĂNG PHÍA BẮC", "h": "DEAN O'BANION", "hAt": [2, "Dean"],
       "lines": [{"text": "Buôn rượu lậu · vẻ ngoài *rất hiền*", "at": [2, "buôn"]}, {"text": "Ban ngày, hắn *bán hoa*", "at": [3, "bán"]}]}),
    sc("photo", 4, img="holyname", tone="color", move="in", kin=kin(("TIỆM HOA ĐỐI DIỆN NHÀ THỜ LỚN", [4, "đối"]), ("VÒNG HOA CHO ĐÁM TANG GIANG HỒ", [4, "vòng"], "acc")),
       label={"k": "NHÀ THỜ CHÍNH TÒA HOLY NAME · CHICAGO", "v": "ẢNH NGÀY NAY", "at": [4, "Tiệm"]}),
    sc("kinetic", 5, vid=V["flowers2"], tone="noir", items=kin(("HÒA BÌNH KIỂU TORRIO ĐỔ VỠ", [5, "đổ"]), ("O'BANION GÀI ÔNG TA VÀO MỘT VỤ BẮT GIỮ", [5, "gài"], "sm"))),
    sc("date", 6, vid=V["flowers"], tone="noir", day="BA NGƯỜI ĐÀN ÔNG BƯỚC VÀO TIỆM HOA", date="10.11.1924"),
    sc("kinetic", 7, vid=V["flowers"], tone="noir", items=kin(("O'BANION CHÌA TAY RA BẮT", [7, "chìa"]))),
    sc("slam", 8, bg="obanion", text="MỘT NGƯỜI GIỮ TAY\nHAI NGƯỜI NỔ SÚNG", hitAt=[8, "nổ"]),
    sc("split", 9, title="AI CHỦ MƯU?", a={"img": "torrio", "label": "ĐƯỢC CHO LÀ TORRIO", "at": [9, "Torrio"]}, b={"img": "obanion", "label": "CHƯA BAO GIỜ ĐƯỢC CHỨNG MINH", "at": [9, "chưa"]}),
    sc("slam", 10, vid=V["chi_night"], tone="night", text="BĂNG PHÍA BẮC\nKHÔNG CẦN CHỨNG MINH", hitAt=[10, "không"]),
    sc("date", 11, vid=V["vcars"], tone="noir", day="XE CỦA CAPONE BỊ PHỤC KÍCH · HẮN THOÁT", date="12.01.1925"),
    sc("kinetic", 12, vid=V["snow"], tone="night", items=kin(("MƯỜI HAI NGÀY SAU", [12, "Mười"]), ("ĐẾN LƯỢT TORRIO", [12, "lượt"], "acc"))),
    sc("seismo", 13, bg="torrio_mug", label="CHICAGO · 24.01.1925", read="TORRIO BỊ BẮN TRƯỚC CỬA NHÀ", hitAt=[13, "bắn"]),
    sc("kinetic", 14, bg="torrio", items=kin(("CÁO GIÀ SỐNG SÓT", [14, "sống"]), ("NHƯNG ÔNG TA ĐÃ HIỂU", [14, "hiểu"], "acc"))),
    sc("broll", 15, vid=V["cells"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("TỪ TRONG NHÀ TÙ", [15, "nhà"]), ("TORRIO GỌI CAPONE TỚI", [15, "gọi"], "acc"))),
    sc("kinetic", 16, vid=V["train2"], tone="noir", items=kin(("GIAO LẠI TOÀN BỘ", [16, "giao"]), ("RỒI RỜI NƯỚC MỸ VỀ Ý", [16, "rời"], "sm"))),
    sc("slam", 17, bg="al1929", text="AL CAPONE\n26 TUỔI", white=True, hitAt=[17, "hai"]),
    sc("ledger", 18, title="NHỮNG GÌ HẮN THỪA HƯỞNG · ƯỚC TÍNH", bg="al_florida", rows=[{"k": "TỔ CHỨC", "v": "KHOẢNG 1.000 NGƯỜI", "at": [18, "nghìn"]}, {"k": "QUỸ LƯƠNG", "v": "$300.000 / TUẦN", "at": [18, "ba"]},
                                                                                     {"k": "VÀ", "v": "MỘT CUỘC CHIẾN", "at": [19, "cuộc"]}]),
    sc("slam", 20, bg="al1930c", text="HẮN KHÔNG CHẠY", hitAt=[20, "không"]),
    sc("split", 21, title="THẦY VÀ TRÒ", a={"img": "torrio", "label": "TORRIO: KÍN TIẾNG, CHIA ĐỊA BÀN", "at": [21, "thầy"]}, b={"img": "al1929", "label": "CAPONE: KHÔNG TIN ĐIỀU ĐÓ", "at": [21, "không"]}),
    sc("kinetic", 22, vid=V["brick2"], tone="noir", items=kin(("MỘT THỨ VŨ KHÍ MỚI", [22, "vũ"], "acc"))),
    sc("evidence", 23, img="thompson", tone="color", callouts=[{"x": 0.3, "y": 0.5, "text": "TIỂU LIÊN THOMPSON", "at": [23, "Thompson"], "side": "l"},
                                                                {"x": 0.72, "y": 0.42, "text": "THIẾT KẾ CHO CHIẾN HÀO THẾ CHIẾN I", "at": [23, "chiến"], "side": "r"}]),
    sc("kinetic", 24, bg="thompson", items=kin(("CHIẾN TRANH KẾT THÚC TRƯỚC", [24, "kết"], "sm"), ("BÁN GẦN NHƯ TỰ DO Ở MỸ", [24, "bán"]))),
    sc("slam", 25, vid=V["typew"], tone="noir", text="“CHIẾC MÁY ĐÁNH CHỮ”", white=True, hitAt=[25, "máy"], sub="CÁCH BÁO CHÍ CHICAGO GỌI KHẨU THOMPSON"),
    sc("counter", 26, bg="chi_1927", **{"from": 0, "to": 133}, countAt=[26, "một"], label="TAY ANH CHỊ BỊ GIẾT Ở CHICAGO · 1925 — 1926"),
    sc("slam", 27, vid=V["gavel"], tone="noir", text="GẦN NHƯ KHÔNG VỤ NÀO\nCÓ NGƯỜI BỊ KẾT ÁN", hitAt=[27, "không"]),
    sc("print", 28, img="weiss", tone="bw", side={"k": "THỦ LĨNH MỚI CỦA BĂNG PHÍA BẮC", "h": "HYMIE WEISS", "hAt": [28, "Hymie"],
       "lines": [{"text": "Đang chuẩn bị *một câu trả lời*", "at": [29, "chuẩn"]}, {"text": "Chicago *chưa từng thấy*", "at": [29, "chưa"]}]}),
])

CH["ch05"] = dict(hud={"k": "CHƯƠNG 05", "t": "MỘT NGHÌN VIÊN ĐẠN Ở HAWTHORNE"}, bgm={"mood": "epic", "at": 0, "gain": 0.11}, scenes=[
    chapter("5", "CHƯƠNG NĂM", "MỘT NGHÌN VIÊN ĐẠN\nỞ HAWTHORNE", "CICERO · 20.09.1926", "Một", bg="thompson"),
    sc("date", 1, vid=V["coffee"], tone="noir", day="CAPONE ĐANG ĂN TRƯA · KHÁCH SẠN HAWTHORNE, CICERO", date="20.09.1926"),
    sc("kinetic", 2, vid=V["vcars"], tone="noir", items=kin(("TIẾNG SÚNG NGOÀI PHỐ", [2, "tiếng"]), ("MỘT CHIẾC XE PHÓNG VỤT QUA", [2, "phóng"], "sm"))),
    sc("kinetic", 3, vid=V["coffee"], tone="noir", items=kin(("MỌI NGƯỜI CHẠY RA CỬA XEM", [3, "chạy"]))),
    sc("slam", 4, vid=V["brick"], tone="noir", text="CHỈ LÀ MỒI NHỬ", hitAt=[4, "mồi"]),
    sc("sketch", 5, art="motorcade", title="Khoảng mười chiếc xe chạy chậm ngang qua khách sạn"),
    sc("kinetic", 7, bg="al1930c", items=kin(("VỆ SĨ FRANK RIO", [7, "Frank"]), ("XÔ HẮN XUỐNG SÀN · NẰM ĐÈ LÊN", [7, "xô"], "acc"))),
    sc("counter", 8, bg="thompson", **{"from": 0, "to": 1000}, prefix="> ", countAt=[8, "một"], label="VIÊN ĐẠN GĂM VÀO KHÁCH SẠN VÀ CÁC CỬA TIỆM"),
    sc("slam", 9, vid=V["brick2"], tone="noir", text="KHÔNG MỘT AI\nTHIỆT MẠNG", white=True, hitAt=[9, "không"]),
    sc("kinetic", 10, vid=V["corridor"], tone="noir", items=kin(("MỘT PHỤ NỮ ĐI ĐƯỜNG", [10, "phụ"]), ("BỊ MẢNH KÍNH LÀM TỔN THƯƠNG MẮT", [10, "mảnh"], "sm"))),
    sc("kinetic", 11, vid=V["briefcase"], tone="noir", items=kin(("CAPONE TRẢ", [11, "trả"], "sm"), ("TOÀN BỘ VIỆN PHÍ", [11, "toàn"], "acc"))),
    sc("photo", 12, img="al_florida", tone="bw", move="in", kin=kin(("KIỂU VIỆC HẮN RẤT GIỎI LÀM", [12, "giỏi"])), label={"k": "AL CAPONE Ở FLORIDA", "v": "ẢNH TƯ LIỆU", "at": [12, "Đó"]}),
    sc("split", 13, title="MỘT ÔNG TRÙM CẦN", a={"img": "al1930c", "label": "ĐƯỢC YÊU MẾN", "at": [13, "yêu"]}, b={"img": "thompson", "label": "VÀ ĐƯỢC SỢ HÃI", "at": [13, "sợ"]}),
    sc("date", 14, bg="holyname", day="HYMIE WEISS BỊ BẮN CHẾT TRƯỚC TIỆM HOA CŨ CỦA O'BANION", date="11.10.1926"),
    sc("timeline", 15, bg="holyname", items=[{"year": "11.1924", "text": "O'Banion"}, {"year": "10.1926", "text": "*Weiss*"}, {"year": "1927", "text": "Moran *lên thay*"}]),
    sc("print", 16, img="moran", tone="bw", side={"k": "BIỆT DANH “BUGS” · GÃ ĐIÊN", "h": "GEORGE MORAN", "hAt": [16, "George"],
       "lines": [{"text": "Người *uống cà phê muộn* ở đầu video", "at": [17, "uống"]}]}),
    sc("slam", 18, vid=V["chi_night"], tone="night", text="CAPONE Ở ĐỈNH CAO", hitAt=[18, "đỉnh"]),
    sc("photo", 19, img="castle", tone="bw", kin=kin(("KHÁCH SẠN LEXINGTON", [19, "Lexington"], "acc"), ("1928 · THUÊ NHIỀU TẦNG LẦU", [19, "thuê"], "sm")),
       label={"k": "KHÁCH SẠN LEXINGTON · CHICAGO", "v": "ẢNH TƯ LIỆU", "at": [19, "Năm"]}),
    sc("photo", 20, img="mansion", tone="color", move="in", kin=kin(("BIỆT THỰ 14 PHÒNG · ĐẢO PALM", [20, "biệt"]), ("$40.000", [20, "bốn"], "acc")),
       label={"k": "BIỆT THỰ CỦA CAPONE · MIAMI", "v": "ẢNH NGÀY NAY", "at": [20, "Cũng"]}),
    sc("kinetic", 21, bg="pool", items=kin(("GIẤY TỜ", [21, "Giấy"], "sm"), ("ĐỨNG TÊN VỢ HẮN", [21, "tên"]))),
    sc("ledger", 22, title="ÔNG TRÙM ĂN DIỆN", bg="al1930", rows=[{"k": "VEST", "v": "MAY ĐO", "at": [22, "vest"]}, {"k": "MŨ PHỚT", "v": "TRẮNG", "at": [22, "mũ"]},
                                                                 {"k": "NHẪN", "v": "KIM CƯƠNG", "at": [22, "nhẫn"]}, {"k": "VÀ", "v": "THÍCH PHÓNG VIÊN", "at": [22, "phóng"]}]),
    sc("kinetic", 23, vid=V["band"], tone="noir", items=kin(("BOA CẢ TRĂM ĐÔ", [23, "boa"]), ("ĐƯỢC VỖ TAY Ở SÂN BÓNG CHÀY", [23, "vỗ"], "sm"))),
    sc("kinetic", 24, bg="al_florida", items=kin(("CHỈ LÀ NGƯỜI LÀM ĂN", [24, "làm"]), ("BÁN THỨ DÂN CHÚNG MUỐN MUA", [24, "bán"], "sm"))),
    sc("broll", 25, vid=V["whiskey"], tone="noir", veil=0.35, illus=FILMV, kin=kin(("NHIỀU NGƯỜI THẤY KHÔNG SAI", [25, "không"]), ("CHÍNH HỌ ĐANG UỐNG RƯỢU CỦA HẮN", [26, "uống"], "acc"))),
    sc("kinetic", 27, vid=V["snow"], tone="night", items=kin(("HÌNH ẢNH ẤY", [27, "hình"], "sm"), ("SẮP VỠ", [27, "vỡ"]))),
    sc("slam", 28, vid=V["brick"], tone="noir", text="MỘT GA-RA\nTRÊN PHỐ CLARK", hitAt=[28, "ga-ra"]),
])

CH["ch06"] = dict(hud={"k": "CHƯƠNG 06", "t": "MƯỜI GIỜ RƯỠI SÁNG LỄ TÌNH NHÂN"}, bgm={"mood": "dark", "at": 0, "gain": 0.12}, scenes=[
    chapter("6", "CHƯƠNG SÁU", "MƯỜI GIỜ RƯỠI SÁNG\nLỄ TÌNH NHÂN", "2122 PHỐ CLARK · 14.02.1929", "Mười", bg="wall_lv"),
    sc("sketch", 1, art="garage", title="Ga-ra số 2122 phố Clark · kho hàng của băng Moran"),
    sc("dots", 2, vid=V["snow"], tone="night", total=7, cols=7, title="SÁNG 14.02.1929 · BẢY NGƯỜI CÓ MẶT",
       groups=[{"from": 0, "n": 5, "cls": "red", "label": "5 NGƯỜI THUỘC BĂNG MORAN", "at": [3, "Năm"]},
               {"from": 5, "n": 1, "cls": "hollow", "label": "JOHN MAY · THỢ MÁY", "at": [4, "John"]},
               {"from": 6, "n": 1, "cls": "gold", "label": "REINHARDT SCHWIMMER · CỰU THỢ KÍNH MẮT", "at": [5, "Reinhardt"]}]),
    sc("sketch", 6, art="dogbark", title="Highball bị buộc vào gầm một chiếc xe"),
    sc("kinetic", 7, vid=V["brick"], tone="noir", items=kin(("NHỮNG KẺ LẠ MẶT BƯỚC VÀO", [7, "lạ"]), ("HAI TÊN MẶC CẢNH PHỤC", [7, "Hai"], "acc"))),
    sc("slam", 8, vid=V["brick2"], tone="noir", text="ÚP MẶT VÀO TƯỜNG", hitAt=[8, "úp"]),
    sc("seismo", 9, bg="thompson", label="2122 PHỐ CLARK · KHOẢNG 10 GIỜ 30 SÁNG", read="HAI KHẨU TIỂU LIÊN THOMPSON", hitAt=[9, "nổ"]),
    sc("counter", 10, bg="bullets", **{"from": 0, "to": 70}, countAt=[10, "Bảy"], label="VIÊN ĐẠN · CỘNG THÊM HAI PHÁT SÚNG SĂN"),
    sc("kinetic", 11, vid=V["snow2"], tone="night", items=kin(("HAI TÊN GIƠ TAY LÊN TRỜI", [11, "giơ"]), ("HAI TÊN MẶC CẢNH PHỤC CHĨA SÚNG PHÍA SAU", [11, "chĩa"], "sm"))),
    sc("slam", 12, vid=V["snow"], tone="night", text="NGƯỜI ĐI ĐƯỜNG TƯỞNG\nCẢNH SÁT VỪA BẮT AI ĐÓ", hitAt=[12, "tưởng"]),
    sc("print", 13, img="moran", tone="bw", side={"k": "THOÁT CHẾT VÌ ĐẾN MUỘN", "h": "BUGS MORAN", "hAt": [13, "Bugs"],
       "lines": [{"text": "Chỉ nói *một câu* với phóng viên", "at": [14, "một"]}]}),
    sc("quote", 15, text="Chỉ Capone mới giết người kiểu đó.", by="BUGS MORAN · NÓI VỚI PHÓNG VIÊN, 2.1929", lbl="TRÍCH DỊCH", qline=15, typeAt=[15, "Chỉ"]),
    sc("kinetic", 16, bg="al_florida", items=kin(("BẰNG CHỨNG NGOẠI PHẠM", [16, "ngoại"]), ("GẦN NHƯ HOÀN HẢO", [16, "hoàn"], "acc"))),
    sc("map", 17, geo="us", pins=[{"name": "Chicago", "at": [17, "Hắn"]}, {"name": "Miami", "label": "MIAMI · ĐANG LÀM VIỆC VỚI NHÀ CHỨC TRÁCH", "at": [17, "Miami"]}],
       routes=[{"from": "Chicago", "to": "Miami", "at": [17, "Florida"], "until": [17, "Miami"], "bend": 0.15}]),
    sc("question", 18, bg="wall_lv", text="Vậy ai đã nổ súng?"),
    sc("date", 19, vid=V["snow2"], tone="night", day="FRED BURKE BẮN CHẾT MỘT CẢNH SÁT Ở BANG MICHIGAN", date="12.1929"),
    sc("evidence", 20, img="thompson", tone="color", callouts=[{"x": 0.5, "y": 0.5, "text": "HAI KHẨU THOMPSON TRONG NHÀ BURKE", "at": [20, "hai"], "side": "r"}]),
    sc("photo", 21, img="bullets", tone="color", move="in", kin=kin(("GIÁM ĐỊNH ĐẠN", [21, "Giám"]), ("KHỚP VỚI VỤ Ở PHỐ CLARK", [21, "khớp"], "acc")),
       label={"k": "MẢNH ĐẠN TỪ VỤ PHỐ CLARK", "v": "HIỆN VẬT", "at": [21, "đạn"]}),
    sc("kinetic", 22, bg="bullets", items=kin(("MỘT TRONG NHỮNG LẦN ĐẦU TIÊN", [22, "đầu"], "sm"), ("KHOA HỌC ĐƯỜNG ĐẠN RA TÒA", [22, "đường"]))),
    sc("file", 23, k="FRED BURKE", name="ÁN\nCHUNG THÂN", desc="Vì giết viên cảnh sát ở Michigan", bg="thompson",
       rows=[{"k": "VỀ GA-RA PHỐ CLARK", "v": "*Chưa bao giờ bị xét xử*", "at": [23, "chưa"]}]),
    sc("kinetic", 24, vid=V["typew"], tone="noir", items=kin(("1935 · MỘT LỜI KHAI", [24, "1935"]), ("NÓI CAPONE LÀ NGƯỜI RA LỆNH", [24, "ra"], "acc"))),
    sc("slam", 25, vid=V["gavel"], tone="noir", text="NHIỀU NHÀ SỬ HỌC\nKHÔNG TIN", hitAt=[25, "không"]),
    sc("kinetic", 26, vid=V["ledger"], tone="noir", items=kin(("BIÊN BẢN ĐIỀU TRA CHÍNH THỨC", [26, "Biên"], "sm"), ("KHÉP LẠI BẰNG MỘT DÒNG", [26, "dòng"]))),
    sc("quote", 27, text="Hung thủ: những kẻ chưa rõ danh tính.", by="BIÊN BẢN ĐIỀU TRA TỬ THI", lbl="TRÍCH DỊCH", qline=27, typeAt=[27, "Hung"]),
    sc("photo", 28, img="brick", tone="color", kin=kin(("GẦN 100 NĂM", [28, "trăm"]), ("KHÔNG AI TỪNG RA TÒA", [28, "ra"], "acc")),
       label={"k": "VIÊN GẠCH TỪ BỨC TƯỜNG GA-RA PHỐ CLARK", "v": "HIỆN VẬT BẢO TÀNG", "at": [28, "Gần"]}),
    sc("slam", 29, bg="wall_lv", text="KHÔNG AI\nCHỨNG MINH ĐƯỢC", white=True, hitAt=[29, "không"]),
    sc("kinetic", 30, vid=V["press"], tone="noir", items=kin(("NHƯNG CÔNG CHÚNG", [30, "công"], "sm"), ("KHÔNG CẦN TÒA ÁN", [30, "tòa"], "acc"))),
])

if __name__ == "__main__":
    extra = D / "gen_scenes2.py"
    if extra.exists():
        import importlib.util
        sys.modules["gen_scenes"] = sys.modules[__name__]
        s2 = importlib.util.spec_from_file_location("g2", extra)
        m = importlib.util.module_from_spec(s2)
        s2.loader.exec_module(m)
        CH.update(m.CH)
    write(__file__, CH, IMGS, GEO, endcardBg="alc_island")
