"""Cảnh viết tay cho Long Whitey Bulger (ch00–ch06; ch07–ch13 ở gen_scenes2.py).

    python data/long/bulger/gen_scenes.py
Ảnh: tìm theo một đoạn tên "File:…" trong research.json / commons.json (find() báo lỗi nếu không thấy hoặc trùng).
Không dùng ảnh nạn nhân, không ảnh hiện trường. Nhạc theo mood (variety.py chọn bài).
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
    "mug2011": "Whitey Bulger US Marshals Service Mug1.jpg", "b1994": "James Bulger 1994.jpg", "surv": "FBI surveillance photograph of James J. Bulger",
    "mug1959": "James J. Bulger - 1959 mugshot.jpg", "alc1959": "James J. Bulger in 1959.jpg", "mug1983": "Bulger 1983s FBI Mugshot.jpg",
    "mug1947": "Whitey Bulger 1947.jpg", "mug1953": "James Joseph Bulger, Jr. (1929-2018) on March 16, 1953.jpg", "mug1956": "Whitey Bulger Prison Mugshot 1956.jpg",
    "weeks_surv": "Whitey Bulger - Kevin Weeks.jpg", "rotary": "Whitey Bulger Rotary Variety Store surveillance.jpg", "poster": "Whitey Bulger Poster.jpg",
    "weeks": "Kevin Weeks mugshot 2.png", "apt": "1012 3rd Street Santa Monica CA.agr.jpg", "coleman": "Federal Correctional Complex Coleman.jpg",
    "hazelton": "USP Hazelton.jpg", "chart": "Winter Hill Gang chart.jpg", "connolly": "John Zip Connolly 1983 cropped.png",
    "flemmi65": "Stephen Flemmi.jpg", "flemmi95": "Stephen Flemmi 1995 FBI Mugshot.jpg", "mural": "Southie Mural.JPG",
    "moakley": "MoakleyFederalCourthouseRear.JPG", "moakley2": "2008 MoakleyCourthouse Boston 2669012840.jpg",
    "southie_air": "South Boston from the air.jpg", "southie_pan": "South Boston landscape cropped.jpg", "map1890": "Boston MKL Bd. 3 1890",
    "billy_flynn": "Boston Mayor Ray Flynn and Massachusetts Senate President William M. Bulger", "billy": "Senate President William M. Bulger (9519685196) 3.jpg",
    "patriarca": "Patriarca crime family chart.jpg", "alc_island": "Alcatraz Island photo Don Ramey Logan.jpg", "alc_1962": "Alcatraz Island March 1962.jpg",
    "alc_broadway": "Broadway Alcatraz.JPG", "oldcolony": "BostonMA OldColonyAve LookingSouthFromFootbridge.jpg", "triple": "JP double three decker.jpg",
    "castle": "Fort Independence on Castle Island.JPG", "b1950": "Park Street Church and Tremont Street 1950s postcard.jpg",
    "kenmore": "Kenmore Square 1950s postcard (2).jpg", "route2": "Route 2 and Boston skyline, circa 1970s.jpg",
    "fbi_hq": "Fbi headquarters.jpg", "fbi_hq2": "FBI Headquarters - J. Edgar Hoover Building (53840035941).jpg", "lsd": "Eye of horus blotter art.jpg",
    "atlanta": "Entrance to the federal penitentiary, Atlanta LCCN2002698072.jpg", "atl_loc": "U.S. Penitentiary, Atlanta, Ga. (LOC).jpg",
    "wollaston": "Wollaston Beach 2023.jpg", "wollaston_night": "Wollaston Beach Night Panorama.jpg",
    "suffolk": "Suffolk Downs horse racing.JPG", "suffolk_board": "Suffolk Downs race results board.JPG",
    "tulsa": "Southern Hills Country Club entrance gate.jpg", "tulsa2": "Southern Hills Country Club golf course as seen from over fence.jpg",
    "globe": "Boston Globe building Sept 2009.jpg", "statehouse": "Boston -Massachusetts State House (48718911666).jpg",
    "dome": "Dome-Massachusetts-State-House-Boston.jpg", "promenade": "Third Street Promenade (a) 06 Sept 2017.jpg",
    "pier_air": "Aerial Photo of Santa Monica Pier.jpg", "sm_beach": "Santa Monica Beach with pier 2.JPG",
    "reykjavik": "Approaching Reykjavik - aerial 2021-10-05.jpg", "reyk_pano": "Reykjavik northeast aerial panorama.jpg",
    "dolby": "Dolby Theatre.jpg", "kodak": "Hollywood Kodak Theatre 3.jpg", "cg_heli": "Coast Guard helicopter, North End, Boston.jpg",
    "winterhill": "Broadway in Winter Hill looking west Oct 2024.jpg", "winterhill_snow": "Winter storm in Winter Hill Dec 20 24.jpg",
    "northend": "North End, Boston, United States (Unsplash).jpg", "prince": "98 Prince Street.jpg", "tucson": "United States Penitentiary, Tucson.jpg",
}.items()}

GEO = {
    "us": {"countries": ["United States of America"], "context": ["Canada", "Mexico", "Cuba", "Bahamas"], "labels": {},
           "bbox": [-125.0, 24.0, -66.0, 50.0], "box": [200, 130, 1720, 850],
           "pins": [{"name": "Boston", "lon": -71.06, "lat": 42.36, "label": "BOSTON"}, {"name": "Indiana", "lon": -87.5, "lat": 41.6, "label": "INDIANA"},
                    {"name": "Atlanta", "lon": -84.39, "lat": 33.75, "label": "ATLANTA"}, {"name": "Alcatraz", "lon": -122.42, "lat": 37.83, "label": "ALCATRAZ"},
                    {"name": "Tulsa", "lon": -95.99, "lat": 36.15, "label": "TULSA"}, {"name": "Miami", "lon": -80.19, "lat": 25.76, "label": "FLORIDA"},
                    {"name": "Santa Monica", "lon": -118.49, "lat": 34.02, "label": "SANTA MONICA"}, {"name": "Tucson", "lon": -110.97, "lat": 32.22, "label": "ARIZONA"},
                    {"name": "Coleman", "lon": -82.01, "lat": 28.77, "label": "FLORIDA"}, {"name": "Hazelton", "lon": -79.5, "lat": 39.67, "label": "TÂY VIRGINIA"}]},
    "world": {"countries": ["United Kingdom", "Ireland", "Italy", "Uruguay"],
              "context": ["United States of America", "Canada", "Mexico", "Brazil", "Argentina", "France", "Spain", "Portugal", "Germany", "Morocco", "Algeria",
                          "Colombia", "Venezuela", "Peru", "Bolivia", "Chile", "Paraguay", "Cuba", "Greenland", "Iceland", "Norway", "Sweden", "Mauritania", "Mali",
                          "Libya", "Tunisia", "Nigeria", "Niger", "Senegal", "Poland"],
              "labels": {}, "bbox": [-125.0, -42.0, 25.0, 64.0], "box": [200, 130, 1720, 850],
              "pins": [{"name": "London", "lon": -0.13, "lat": 51.5, "label": "LONDON"}, {"name": "Ireland", "lon": -8.0, "lat": 53.2, "label": "IRELAND"},
                       {"name": "Italy", "lon": 12.5, "lat": 42.5, "label": "Ý"}, {"name": "Uruguay", "lon": -56.0, "lat": -33.0, "label": "URUGUAY"},
                       {"name": "Santa Monica", "lon": -118.49, "lat": 34.02, "label": "SANTA MONICA"}]},
    "ice": {"countries": ["United States of America", "Iceland"], "context": ["Canada", "Greenland", "Mexico", "Cuba", "Ireland", "United Kingdom"],
            "labels": {}, "bbox": [-128.0, 22.0, -8.0, 68.0], "box": [200, 130, 1720, 850],
            "pins": [{"name": "Reykjavik", "lon": -21.9, "lat": 64.13, "label": "REYKJAVIK"}, {"name": "Santa Monica", "lon": -118.49, "lat": 34.02, "label": "SANTA MONICA"}]},
}

# b-roll Pexels (đều ngang, SDR)
V = dict(smpier="9699835", smpier2="13868202", smair="14472673", coast_city="30971952", elevator="34779661", cat="3718610", cat2="34550347", cat3="3070350",
         cash="5466769", cash2="6326929", bos_sunset="38127969", bos_air="12595930", bos_air2="12595928", bos_air3="12595926", roofs="12595890",
         bos_dusk="37543344", bos_water="31080972", bos_street="38716471", snowlot="35818301", xmas="29465786", xmas_house="4076197", snowcity="7178617",
         bar="2912918", church="5481220", church2="12350425", safe="39060937", syringe="6290576", vials="8534418", acid="3578210", acid2="3582427",
         race="31653765", race2="34943028", golf="6573413", golf2="4784177", lot="16960302", drive="33931911", drive_bw="31940380", drive2="35677223",
         tape="8382683", tape2="32296437", tape3="11124042", phone="10397452", files="6549976", box="8371852", cards="6550666", doc="7710453",
         beachcar="10811520", press="29906415", press2="38826405", lotto="2982434", radio="8319633", dash="31220606", reyk="38551466", reyk2="4595479",
         reyk3="36837900", tvstatic="11999581", heli="32954102", lawyer="8135313", tunnel="2845945", fog="37669026", fog2="29792712", letter="7343476",
         hk="2856781", hk2="34933784", projector="855120", theater="7988642", projector2="856593", boats="3376554", boats2="16685626", london="39618428",
         garage="8987273", garage2="8986894", dental="6763242", window="6175387", alc="29024923", sfbay="36434849", cells="5211616", cells2="5243257",
         gavel="6699964", justice="8061659", typew="33068304", corridor="3192916")

CH = {}

CH["ch00"] = dict(hud={"k": "MỞ ĐẦU", "t": "CĂN HỘ 303"}, bgm={"mood": "tense", "at": 0, "gain": 0.13}, scenes=[
    sc("date", None, vid=V["smpier"], tone="noir", day="SANTA MONICA · CALIFORNIA · THỨ TƯ", date="22.06.2011"),
    sc("photo", 1, img="apt", tone="color", move="in", kin=kin(("CĂN HỘ 303", [1, "303"]), ("CHARLIE VÀ CAROL GASKO", [1, "Charlie"], "acc")),
       label={"k": "SỐ 1012 PHỐ 3 · SANTA MONICA", "v": "ẢNH NGÀY NAY", "at": [1, "Ở"]}),
    sc("broll", 2, vid=V["cash"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("TRẢ TIỀN THUÊ BẰNG TIỀN MẶT", [2, "tiền"]), ("LUÔN ĐÚNG HẠN", [2, "đúng"], "acc"))),
    sc("kinetic", 3, bg="apt", items=kin(("HÀNG XÓM BIẾT GÌ VỀ HỌ?", [3, "Hàng"]), ("GẦN NHƯ KHÔNG GÌ CẢ", [3, "Gần"], "acc"))),
    sc("sketch", 4, art="catfeed", title="Người vợ hay cho một con mèo hoang ăn trước cửa"),
    sc("kinetic", 5, vid=V["coast_city"], tone="noir", items=kin(("KHOẢNG 4 GIỜ CHIỀU", [5, "giờ"], "sm"), ("MỘT YÊU CẦU LẠ TỪ ĐẶC VỤ LIÊN BANG", [5, "yêu"]))),
    sc("broll", 6, vid=V["phone"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("GỌI LÊN CĂN 303", [6, "gọi"]), ("NGĂN CHỨA ĐỒ DƯỚI GA-RA VỪA BỊ CẠY", [6, "ngăn"], "sm"))),
    sc("sketch", 7, art="elevator", title="Khoảng 5 giờ 45 · một ông già mặc đồ trắng bước ra khỏi thang máy"),
    sc("slam", 8, vid=V["elevator"], tone="noir", text="NHỮNG KHẨU SÚNG\nCHĨA VỀ PHÍA ÔNG", hitAt=[8, "súng"]),
    sc("kinetic", 9, bg="apt", items=kin(("KHÔNG CHỊU QUỲ XUỐNG", [9, "quỳ"]), ("XƯNG TÊN: CHARLES GASKO", [9, "Charles"], "acc"))),
    sc("slam", 10, vid=V["lot"], tone="night", text="RỒI ÔNG ĐỔI Ý", hitAt=[10, "đổi"]),
    sc("quote", 11, text="Các anh biết tôi là ai mà. Tôi là Whitey Bulger.", by="JAMES “WHITEY” BULGER · THEO LỜI THUẬT CỦA FBI, 22.06.2011", lbl="TRÍCH DỊCH", qline=11, typeAt=[11, "Các"]),
    sc("photo", 12, img="mug2011", tone="color", kin=kin(("81 TUỔI", [12, "tám"], "acc")), label={"k": "JAMES “WHITEY” BULGER", "v": "ẢNH HỒ SƠ · 2011", "at": [12, "Ông"]}),
    sc("photo", 13, img="poster", tone="color", frame=True, kin=kin(("LẨN TRỐN 16 NĂM", [13, "mười"]), ("TOP 10 TRUY NÃ CỦA FBI", [13, "danh"], "acc")),
       label={"k": "THÔNG BÁO TRUY NÃ CỦA FBI", "v": "TƯ LIỆU", "at": [13, "Ông"]}),
    sc("counter", 14, vid=V["cash2"], tone="noir", **{"from": 0, "to": 2}, prefix="$", suffix=" TRIỆU", countAt=[14, "hai"], label="TIỀN THƯỞNG CHO AI CHỈ RA ÔNG TA"),
    sc("kinetic", 15, vid=V["window"], tone="noir", items=kin(("CÁC ĐẶC VỤ KHOÉT TƯỜNG", [15, "khoét"]), ("CĂN HỘ 303", [15, "303"], "acc"))),
    sc("counter", 16, bg="apt", **{"from": 0, "to": 30}, countAt=[16, "ba"], label="KHẨU SÚNG GIẤU TRONG TƯỜNG"),
    sc("counter", 17, vid=V["cash"], tone="noir", **{"from": 0, "to": 822198}, prefix="$", countAt=[17, "tám"], label="TIỀN MẶT"),
    sc("broll", 18, vid=V["hk"], tone="night", veil=0.4, illus=FILMV, kin=kin(("VÔ GIAN ĐẠO", [18, "Vô"], "serif"), ("HỒNG KÔNG · 2002", [18, "Hồng"], "sm"))),
    sc("timeline", 19, bg="dolby", items=[{"year": "2002", "text": "Vô Gian Đạo"}, {"year": "2006", "text": "*Điệp Vụ Boston*"}, {"year": "2007", "text": "Oscar *Phim hay nhất*"}]),
    sc("kinetic", 20, vid=V["projector"], tone="noir", items=kin(("NHÂN VẬT ÔNG TRÙM", [20, "ông"]), ("XÂY DỰNG TỪ MỘT NGƯỜI CÓ THẬT", [20, "thật"], "acc"))),
    sc("slam", 21, bg="mug2011", text="ÔNG GIÀ Ở\nCĂN HỘ 303", hitAt=[21, "303"]),
    sc("kinetic", 22, vid=V["files"], tone="noir", items=kin(("HỒ SƠ CHỈ ĐIỂM", [22, "hồ"]), ("DÀY 700 TRANG Ở FBI", [22, "bảy"], "acc"))),
    sc("print", 23, img="connolly", tone="bw", side={"k": "LỜI HỨA THỨ HAI", "h": "MỘT ĐẶC VỤ", "hAt": [23, "đặc"],
       "lines": [{"text": "Lớn lên cách nhà ông ta *vài cánh cửa*", "at": [23, "cách"]}]}),
    sc("broll", 24, vid=V["reyk"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("MỘT CỰU HOA HẬU", [24, "hoa"]), ("LÀM ĐƯỢC ĐIỀU FBI KHÔNG LÀM NỔI", [24, "điều"], "acc"))),
    sc("brand", 25, sub="HỒ SƠ · WHITEY BULGER"),
    sc("question", 26, bg="fbi_hq", text="Vì sao kẻ bị FBI truy nã gắt gao nhất\nlại từng là người của chính FBI?"),
    sc("map", 27, geo="us", pins=[{"name": "Santa Monica", "at": [27, "Để"]}, {"name": "Boston", "label": "BOSTON · HƠN 70 NĂM TRƯỚC", "at": [27, "Boston"]}],
       routes=[{"from": "Santa Monica", "to": "Boston", "at": [27, "quay"], "until": [27, "Boston"], "bend": 0.15}]),
])

CH["ch01"] = dict(hud={"k": "CHƯƠNG 01", "t": "CẬU BÉ Ở OLD HARBOR"}, bgm={"mood": "quiet", "at": 0, "gain": 0.12}, scenes=[
    chapter("1", "CHƯƠNG MỘT", "CẬU BÉ Ở\nOLD HARBOR", "BOSTON · 1929 — 1952", "Cậu", bg="southie_air"),
    sc("date", 1, bg="map1890", day="JAMES JOSEPH BULGER CHÀO ĐỜI · VÙNG BOSTON", date="03.09.1929"),
    sc("kinetic", 2, bg="map1890", items=kin(("NƠI SINH CHÍNH XÁC", [2, "Nơi"], "sm"), ("MỖI TÀI LIỆU GHI MỘT KHÁC", [2, "mỗi"]))),
    sc("kinetic", 3, vid=V["roofs"], tone="noir", items=kin(("CHA LÀ CÔNG NHÂN", [3, "công"]), ("MẤT MỘT CÁNH TAY VÌ TAI NẠN", [3, "cánh"], "sm"))),
    sc("counter", 4, bg="triple", **{"from": 0, "to": 6}, countAt=[4, "sáu"], label="ĐỨA CON · MẸ Ở NHÀ TRÔNG"),
    sc("photo", 5, img="oldcolony", tone="bw", move="in", kin=kin(("THÁNG 5.1938", [5, "1938"], "sm"), ("KHU NHÀ Ở XÃ HỘI OLD HARBOR", [5, "Old"], "acc")),
       label={"k": "ĐẠI LỘ OLD COLONY · KHU OLD HARBOR BÊN PHẢI", "v": "ẢNH NĂM 2013", "at": [5, "Tháng"]}),
    sc("slam", 6, bg="mural", text="SOUTHIE", white=True, hitAt=[6, "Southie"], sub="CÁI TÊN THÂN MẬT CỦA NAM BOSTON"),
    sc("photo", 7, img="southie_air", tone="color", move="in", kin=kin(("BÁN ĐẢO CỦA NGƯỜI LAO ĐỘNG", [7, "bán"]), ("GỐC IRELAND", [7, "Ireland"], "acc")),
       label={"k": "NAM BOSTON NHÌN TỪ TRÊN CAO", "v": "ẢNH NGÀY NAY", "at": [7, "Southie"]}),
    sc("photo", 8, img="triple", tone="color", move="pan", illus="ẢNH MINH HỌA · NHÀ BA TẦNG KIỂU BOSTON",
       kin=kin(("NHÀ BA TẦNG CHEN NHAU", [8, "ba"]), ("NHÀ THỜ GÓC NÀY · QUÁN RƯỢU GÓC KIA", [8, "thờ"], "sm"))),
    sc("broll", 9, vid=V["church"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("TRUNG THÀNH VỚI KHU PHỐ TRƯỚC", [9, "trung"]), ("RỒI MỚI TỚI THỨ GÌ KHÁC", [9, "rồi"], "sm"))),
    sc("slam", 10, bg="mural", text="KHÔNG AI NÓI CHUYỆN\nVỚI CẢNH SÁT", hitAt=[10, "không"], sub="LUẬT BẤT THÀNH VĂN CỦA SOUTHIE"),
    sc("photo", 11, img="mug1947", tone="bw", kin=kin(("TÓC VÀNG NHẠT", [11, "tóc"], "sm"), ("“WHITEY”", [11, "Whitey"], "acc")),
       label={"k": "JAMES BULGER · ẢNH HỒ SƠ CẢNH SÁT BOSTON", "v": "NĂM 1947", "at": [11, "Vì"]}),
    sc("slam", 12, bg="mug1947", text="CẬU GHÉT CÁI TÊN ẤY", hitAt=[12, "ghét"]),
    sc("split", 13, title="HAI CÁI TÊN", a={"img": "mug1953", "label": "NGƯỜI THÂN GỌI: JIM", "at": [13, "Jim"]}, b={"img": "poster", "label": "CẢNH SÁT VÀ BÁO CHÍ: WHITEY", "at": [13, "Chỉ"]}),
    sc("print", 14, img="billy", tone="bw", side={"k": "NGƯỜI EM TRAI", "h": "WILLIAM BULGER", "hAt": [14, "William"],
       "lines": [{"text": "Mọi người gọi là *Billy*", "at": [14, "Billy"]}, {"text": "Chăm học · mê *tiếng La-tinh*", "at": [15, "chăm"]}, {"text": "Muốn *làm chính trị*", "at": [15, "chính"]}]}),
    sc("slam", 16, bg="billy_flynn", text="HÃY NHỚ NGƯỜI EM NÀY", hitAt=[16, "nhớ"]),
    sc("kinetic", 17, bg="oldcolony", items=kin(("CÁCH NHÀ BULGER VÀI CÁNH CỬA", [17, "vài"]), ("MỘT GIA ĐÌNH GỐC IRELAND KHÁC", [17, "gia"], "sm"))),
    sc("counter", 18, bg="southie_pan", **{"from": 0, "to": 11}, suffix=" TUỔI", countAt=[18, "mười"], label="CẬU CON TRAI NHÀ ẤY KÉM WHITEY"),
    sc("print", 19, img="connolly", tone="bw", side={"k": "TÊN CẬU BÉ · ẢNH NĂM 1983", "h": "JOHN CONNOLLY", "hAt": [19, "John"],
       "lines": [{"text": "Theo lời ông ta kể về sau", "at": [20, "Theo"]}, {"text": "Được Whitey mua cho *một que kem*", "at": [20, "que"]},
                 {"text": "Được cứu khỏi *một trận đòn*", "at": [20, "cứu"]}]}),
    sc("kinetic", 21, vid=V["files"], tone="noir", items=kin(("40 NĂM SAU", [21, "bốn"], "sm"), ("NGƯỜI MỞ HỒ SƠ CHỈ ĐIỂM Ở FBI", [21, "mở"], "acc"))),
    sc("date", 22, bg="mug1947", day="WHITEY BỊ BẮT LẦN ĐẦU · 14 TUỔI", date="1943"),
    sc("kinetic", 23, vid=V["roofs"], tone="noir", items=kin(("THEO CÁC TIỂU SỬ", [23, "Theo"], "sm"), ("BỎ NHÀ ĐI THEO MỘT GÁNH XIẾC", [23, "gánh"]))),
    sc("ledger", 24, title="NHỮNG NĂM SAU ĐÓ", bg="mug1953", rows=[{"k": "TRỘM CẮP", "v": "●", "at": [24, "trộm"]}, {"k": "ĐÁNH NHAU", "v": "●", "at": [24, "đánh"]},
                                                                  {"k": "CƯỚP", "v": "●", "at": [24, "cướp"]}]),
    sc("photo", 25, img="mug1953", tone="bw", kin=kin(("1948 · VÀO KHÔNG QUÂN MỸ", [25, "Không"]), ("GIẢI NGŨ DANH DỰ NĂM 1952", [26, "giải"], "acc")),
       label={"k": "JAMES BULGER · ẢNH HỒ SƠ CẢNH SÁT BOSTON", "v": "16.03.1953", "at": [25, "Năm"]}),
    sc("kinetic", 27, bg="b1950", items=kin(("TRỞ VỀ BOSTON", [27, "Trở"]), ("CẬU KHÔNG TÌM VIỆC", [27, "không"], "sm"))),
    sc("slam", 28, vid=V["safe"], tone="noir", text="CẬU TÌM NGÂN HÀNG", hitAt=[28, "ngân"]),
])

CH["ch02"] = dict(hud={"k": "CHƯƠNG 02", "t": "ALCATRAZ VÀ NHỮNG MŨI TIÊM"}, bgm={"mood": "dark", "at": 0, "gain": 0.12}, scenes=[
    chapter("2", "CHƯƠNG HAI", "ALCATRAZ VÀ\nNHỮNG MŨI TIÊM", "1956 — 1965", "Alcatraz", bg="alc_island"),
    sc("kinetic", 1, bg="kenmore", items=kin(("GIỮA THẬP NIÊN 1950", [1, "1950"], "sm"), ("MỘT BĂNG CƯỚP ĐI TỪ BANG NÀY SANG BANG KHÁC", [1, "băng"]))),
    sc("map", 2, geo="us", pins=[{"name": "Boston", "label": "MASSACHUSETTS · RHODE ISLAND", "at": [2, "Massachusetts"]}, {"name": "Indiana", "at": [2, "Indiana"]}],
       routes=[{"from": "Boston", "to": "Indiana", "at": [2, "rồi"], "until": [2, "Indiana"], "bend": 0.15}]),
    sc("date", 3, bg="mug1956", day="BỊ BẮT TRONG MỘT HỘP ĐÊM Ở NGOẠI Ô BOSTON", date="1956"),
    sc("counter", 4, vid=V["gavel"], tone="noir", **{"from": 0, "to": 20}, suffix=" NĂM TÙ", countAt=[4, "hai"], label="BẢN ÁN CHO TỘI CƯỚP NGÂN HÀNG"),
    sc("photo", 5, img="mug1956", tone="bw", kin=kin(("27 TUỔI", [5, "hai"], "acc")), label={"k": "JAMES BULGER · ẢNH HỒ SƠ NHÀ TÙ", "v": "NĂM 1956", "at": [5, "Hắn"]}),
    sc("photo", 6, img="atlanta", tone="bw", film=True, move="in", kin=kin(("NHÀ TÙ LIÊN BANG ATLANTA", [6, "Atlanta"])),
       label={"k": "CỔNG NHÀ TÙ LIÊN BANG ATLANTA", "v": "ẢNH TƯ LIỆU", "at": [6, "Nơi"]}),
    sc("kinetic", 7, bg="atl_loc", items=kin(("NĂM 1957", [7, "1957"], "sm"), ("MỘT LỜI ĐỀ NGHỊ DÀNH CHO TÙ NHÂN", [7, "lời"]))),
    sc("broll", 8, vid=V["vials"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("TÌNH NGUYỆN THAM GIA NGHIÊN CỨU Y KHOA", [8, "tình"]), ("SẼ ĐƯỢC XÉT GIẢM ÁN", [8, "giảm"], "acc"))),
    sc("kinetic", 9, vid=V["syringe"], tone="noir", items=kin(("NGƯỜI TA BẢO HỌ", [9, "bảo"], "sm"), ("TÌM THUỐC CHỮA TÂM THẦN PHÂN LIỆT", [9, "tâm"]))),
    sc("slam", 10, vid=V["acid"], tone="noir", text="SỰ THẬT THÌ KHÁC", hitAt=[10, "khác"]),
    sc("file", 11, k="CHƯƠNG TRÌNH BÍ MẬT CỦA CIA", name="MK-ULTRA", desc="Cơ quan Tình báo Trung ương Mỹ", bg="atl_loc", stamp={"text": "BÍ MẬT", "at": [11, "bí"]}),
    sc("photo", 12, img="lsd", tone="color", move="in", illus="ẢNH MINH HỌA · GIẤY THẤM LSD", kin=kin(("LSD", [12, "LSD"], "acc"), ("CHẤT GÂY ẢO GIÁC CỰC MẠNH", [12, "ảo"]))),
    sc("kinetic", 13, vid=V["syringe"], tone="noir", items=kin(("BÁC SĨ CỦA MỘT ĐẠI HỌC DANH TIẾNG", [13, "bác"]), ("TÙ NHÂN KHÔNG BIẾT AI TRẢ TIỀN", [13, "trả"], "sm"))),
    sc("counter", 14, vid=V["acid2"], tone="noir", **{"from": 0, "to": 50}, prefix="> ", countAt=[14, "năm"], label="LẦN TIÊM TRONG KHOẢNG 18 THÁNG · THEO LỜI BULGER"),
    sc("broll", 15, vid=V["acid"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("THẤY MÁU CHẢY RA TỪ TƯỜNG", [15, "máu"]), ("SUỐT ĐỜI KHÔNG NGỦ ĐƯỢC YÊN", [15, "ngủ"], "acc"))),
    sc("split", 16, title="LỜI KỂ VÀ HỒ SƠ", a={"img": "mug1956", "label": "“50 LẦN”: CHỈ CÓ LỜI HẮN", "at": [16, "năm"]}, b={"img": "atl_loc", "label": "CHƯƠNG TRÌNH: MỸ ĐÃ THỪA NHẬN", "at": [17, "thừa"]}),
    sc("date", 18, bg="alc_1962", day="BỊ NGHI MƯU VƯỢT NGỤC · CHUYỂN TỚI ALCATRAZ", date="11.1959"),
    sc("photo", 19, img="alc1959", tone="bw", kin=kin(("SỐ TÙ", [19, "số"], "sm"), ("1428", [19, "1428"], "acc")), label={"k": "JAMES BULGER · ALCATRAZ", "v": "ẢNH HỒ SƠ · 11.1959", "at": [19, "Hắn"]}),
    sc("photo", 20, img="alc_island", tone="color", move="pan", kin=kin(("ALCATRAZ ĐÃ GẦN NGÀY ĐÓNG CỬA", [20, "đóng"]), ("AL CAPONE RỜI ĐẢO 20 NĂM TRƯỚC", [20, "Capone"], "sm")),
       label={"k": "ĐẢO ALCATRAZ · VỊNH SAN FRANCISCO", "v": "ẢNH NGÀY NAY", "at": [20, "Alcatraz"]}),
    sc("photo", 21, img="alc_broadway", tone="color", move="in", kin=kin(("KHOẢNG BA NĂM", [21, "ba"]), ("ĐỌC SÁCH VÀ TẬP THỂ LỰC", [21, "đọc"], "acc")),
       label={"k": "DÃY BUỒNG GIAM “BROADWAY” · ALCATRAZ", "v": "ẢNH NGÀY NAY", "at": [21, "Hắn"]}),
    sc("kinetic", 22, vid=V["alc"], tone="noir", items=kin(("VỀ SAU HẮN VIẾT", [22, "viết"], "sm"), ("QUÃNG THỜI GIAN HẮN NHỚ NHẤT TRONG ĐỜI", [22, "nhớ"]))),
    sc("date", 23, vid=V["sfbay"], tone="noir", day="ĐƯỢC THA CÓ ĐIỀU KIỆN · SAU KHOẢNG CHÍN NĂM", date="03.1965"),
    sc("kinetic", 24, bg="southie_pan", items=kin(("35 TUỔI", [24, "ba"]), ("TRỞ VỀ SOUTHIE", [24, "trở"], "acc"))),
    sc("photo", 25, img="statehouse", tone="color", move="in", kin=kin(("NGƯỜI EM BILLY", [25, "Billy"]), ("ĐÃ ĐẮC CỬ VÀO NGHỊ VIỆN BANG", [25, "đắc"], "acc")),
       label={"k": "TÒA NGHỊ VIỆN BANG MASSACHUSETTS", "v": "ẢNH NGÀY NAY", "at": [25, "Trong"]}),
    sc("split", 26, title="HAI ANH EM, HAI CON ĐƯỜNG", a={"img": "mug1959", "label": "JAMES: ALCATRAZ", "at": [26, "anh"]}, b={"img": "billy", "label": "WILLIAM: NGHỊ VIỆN", "at": [26, "con"]}),
    sc("slam", 27, bg="statehouse", text="CẢ HAI ĐỀU DẪN TỚI\nQUYỀN LỰC", hitAt=[27, "quyền"]),
])

CH["ch03"] = dict(hud={"k": "CHƯƠNG 03", "t": "CUỘC CHIẾN NAM BOSTON"}, bgm={"mood": "tense", "at": 0, "gain": 0.12}, scenes=[
    chapter("3", "CHƯƠNG BA", "CUỘC CHIẾN\nNAM BOSTON", "1965 — 1975", "Cuộc", bg="route2"),
    sc("kinetic", 1, bg="statehouse", items=kin(("CÔNG NHÂN VỆ SINH TRONG TÒA NHÀ CÔNG QUYỀN", [1, "vệ"]), ("VIỆC DO NGƯỜI EM XIN CHO", [1, "em"], "sm"))),
    sc("slam", 2, vid=V["bos_street"], tone="noir", text="VIỆC ẤY KHÔNG KÉO DÀI", hitAt=[2, "không"]),
    sc("file", 3, k="NAM BOSTON · CUỐI THẬP NIÊN 1960", name="BĂNG\nKILLEEN", desc="Băng cá độ ở Southie · Whitey đi thu tiền", bg="southie_pan"),
    sc("split", 4, title="NĂM 1971 · HAI BĂNG Ở SOUTHIE", a={"img": "mural", "label": "BĂNG KILLEEN", "at": [4, "Killeen"]}, b={"img": "oldcolony", "label": "BĂNG MULLEN", "at": [4, "Mullen"]}),
    sc("kinetic", 5, vid=V["snowlot"], tone="night", items=kin(("NGƯỜI CỦA HAI BÊN", [5, "hai"], "sm"), ("LẦN LƯỢT NGÃ XUỐNG", [5, "ngã"]))),
    sc("date", 6, bg="triple", day="THỦ LĨNH BĂNG KILLEEN BỊ BẮN CHẾT TRƯỚC NHÀ", date="1972"),
    sc("slam", 7, bg="mug1959", text="WHITEY ĐỨNG TRƯỚC\nMỘT LỰA CHỌN", hitAt=[7, "lựa"]),
    sc("photo", 8, img="winterhill", tone="color", move="in", kin=kin(("THỊ TRẤN BÊN KIA SÔNG", [8, "thị"], "sm"), ("HOWIE WINTER", [8, "Howie"], "acc")),
       label={"k": "KHU WINTER HILL · SOMERVILLE", "v": "ẢNH NGÀY NAY", "at": [8, "Hắn"]}),
    sc("evidence", 9, img="chart", tone="bw", callouts=[{"x": 0.5, "y": 0.06, "text": "BĂNG WINTER HILL · SƠ ĐỒ KHOẢNG NĂM 1975", "at": [9, "Winter"], "side": "r"},
                                                         {"x": 0.3, "y": 0.5, "text": "BĂNG GỐC IRELAND MẠNH NHẤT VÙNG BOSTON", "at": [10, "mạnh"], "side": "l"}]),
    sc("kinetic", 11, vid=V["bar"], tone="noir", items=kin(("NHỮNG TAY SÚNG KHÉT TIẾNG", [11, "tay"]), ("JOHN MARTORANO", [11, "John"], "acc"))),
    sc("counter", 12, vid=V["gavel"], tone="noir", **{"from": 0, "to": 20}, countAt=[12, "hai"], label="VỤ GIẾT NGƯỜI · MARTORANO THỪA NHẬN TRƯỚC TÒA"),
    sc("org", 13, bg="winterhill_snow", nodes=[{"id": "w", "t": "HOWIE WINTER", "s": "DÀN XẾP NGỪNG BẮN", "cls": "top", "at": [13, "Winter"]},
                                              {"id": "s", "t": "NAM BOSTON", "s": "HAI BĂNG NHẬP LÀM MỘT", "p": "w", "at": [13, "nhập"]},
                                              {"id": "b", "t": "WHITEY BULGER", "s": "VỪA Ở PHE THUA", "p": "s", "cls": "acc", "at": [14, "Whitey"]}]),
    sc("ledger", 15, title="WINTER HILL KIỂM SOÁT", bg="route2", rows=[{"k": "CÁ ĐỘ", "v": "●", "at": [15, "cá"]}, {"k": "CHO VAY NẶNG LÃI", "v": "●", "at": [15, "vay"]},
                                                                      {"k": "TIỀN BẢO KÊ", "v": "●", "at": [15, "bảo"]}, {"k": "ĐỊA BÀN", "v": "BỜ SÔNG → BẾN CẢNG", "at": [15, "bờ"]}]),
    sc("ledger", 16, title="THÓI QUEN CỦA WHITEY", bg="mug1983", rows=[{"k": "THUỐC LÁ", "v": "KHÔNG", "at": [16, "hút"]}, {"k": "RƯỢU", "v": "HẦU NHƯ KHÔNG", "at": [16, "rượu"]},
                                                                      {"k": "THỂ DỤC", "v": "MỖI NGÀY", "at": [17, "tập"]}, {"k": "NGỦ", "v": "BAN NGÀY", "at": [17, "ngủ"]}]),
    sc("slam", 18, vid=V["phone"], tone="noir", text="KHÔNG BAO GIỜ\nNÓI QUA ĐIỆN THOẠI", hitAt=[18, "điện"]),
    sc("kinetic", 19, bg="mug1983", items=kin(("KIỂM SOÁT MỌI THỨ", [19, "kiểm"]), ("VÀ KHÔNG TIN AI", [19, "tin"], "acc"))),
    sc("date", 20, bg="surv", day="KẾT ĐÔI VỚI MỘT NGƯỜI SẼ ĐI CÙNG HẮN 20 NĂM", date="1974"),
    sc("print", 21, img="flemmi65", tone="bw", side={"k": "ẢNH HỒ SƠ NĂM 1965", "h": "STEPHEN FLEMMI", "hAt": [21, "Stephen"],
       "lines": [{"text": "Flemmi có *một bí mật*", "at": [22, "bí"]}]}),
    sc("slam", 23, vid=V["files"], tone="noir", text="NGƯỜI CUNG CẤP TIN\nCHO FBI", hitAt=[23, "cung"], sub="TỪ THẬP NIÊN 1960"),
    sc("kinetic", 24, bg="fbi_hq", items=kin(("Ở BOSTON", [24, "Boston"], "sm"), ("FBI CHỈ QUAN TÂM MỘT KẺ THÙ", [24, "kẻ"]))),
    sc("photo", 25, img="patriarca", tone="bw", kin=kin(("KHÔNG PHẢI CÁC BĂNG GỐC IRELAND", [25, "Không"], "sm"), ("MAFIA GỐC Ý", [26, "mafia"]), ("GIA ĐÌNH PATRIARCA", [26, "Patriarca"], "acc")),
       label={"k": "SƠ ĐỒ GIA ĐÌNH PATRIARCA", "v": "TƯ LIỆU ĐIỀU TRA", "at": [26, "Mà"]}),
    sc("photo", 27, img="prince", tone="color", kin=kin(("MỘT VĂN PHÒNG NHỎ", [27, "văn"]), ("Ở KHU BẮC THÀNH PHỐ", [27, "Bắc"], "acc")),
       label={"k": "SỐ 98 PHỐ PRINCE · KHU BẮC BOSTON", "v": "ẢNH NGÀY NAY", "at": [27, "Thủ"]}),
    sc("kinetic", 28, vid=V["tape"], tone="noir", items=kin(("ĐỂ ĐÁNH MAFIA", [28, "mafia"], "sm"), ("FBI CẦN NGƯỜI BÊN TRONG THẾ GIỚI NGẦM", [28, "người"]))),
    sc("date", 29, bg="fbi_hq2", day="MỘT ĐẶC VỤ TRẺ ĐƯỢC ĐIỀU VỀ BOSTON", date="1975"),
    sc("slam", 30, bg="connolly", text="ANH TA LỚN LÊN\nỞ OLD HARBOR", hitAt=[30, "Old"]),
])

CH["ch04"] = dict(hud={"k": "CHƯƠNG 04", "t": "CUỘC GẶP Ở BÃI WOLLASTON"}, bgm={"mood": "mystery", "at": 0, "gain": 0.12}, scenes=[
    chapter("4", "CHƯƠNG BỐN", "CUỘC GẶP Ở\nBÃI WOLLASTON", "MÙA THU 1975", "Cuộc", bg="wollaston"),
    sc("print", 1, img="connolly", tone="bw", side={"k": "RỜI SOUTHIE ĐI HỌC · RỒI VÀO FBI", "h": "JOHN CONNOLLY", "hAt": [1, "John"],
       "lines": [{"text": "Nổi tiếng nhờ tóm một tay mafia Boston", "at": [2, "tóm"]}, {"text": "đang lẩn trốn ở *New York*", "at": [2, "New"]}]}),
    sc("kinetic", 3, bg="fbi_hq", items=kin(("ĐƯỢC CHUYỂN VỀ QUÊ NHÀ", [3, "chuyển"]), ("MANG THEO MỘT Ý TƯỞNG", [3, "ý"], "acc"))),
    sc("sketch", 4, art="beachcar", title="Mùa thu 1975 · bãi biển Wollaston, phía nam Boston · theo các lời kể"),
    sc("split", 5, title="HAI NGƯỜI TRONG XE", a={"img": "connolly", "label": "ĐẶC VỤ FBI", "at": [5, "đặc"]}, b={"img": "mug1983", "label": "ÔNG TRÙM NAM BOSTON", "at": [6, "ông"]}),
    sc("slam", 7, bg="oldcolony", text="LỚN LÊN CÁCH NHAU\nVÀI CÁNH CỬA", hitAt=[7, "cách"]),
    sc("kinetic", 8, vid=V["beachcar"], tone="noir", items=kin(("LỜI ĐỀ NGHỊ", [8, "Lời"], "sm"), ("RẤT ĐƠN GIẢN", [8, "đơn"]))),
    sc("org", 9, bg="wollaston_night", nodes=[{"id": "m", "t": "MAFIA GỐC Ý", "s": "GIA ĐÌNH PATRIARCA", "cls": "top", "at": [9, "Mafia"]},
                                             {"id": "f", "t": "FBI", "s": "KẺ THÙ", "p": "m", "at": [9, "kẻ"]},
                                             {"id": "w", "t": "WHITEY", "s": "ĐỐI THỦ", "p": "m", "cls": "acc", "at": [9, "đối"]}]),
    sc("question", 10, bg="wollaston_night", text="Vậy tại sao không cùng nhau loại chúng?"),
    sc("kinetic", 11, bg="fbi_hq2", items=kin(("VỚI FBI", [11, "FBI"], "sm"), ("ĐÓ LÀ MỘT MÓN HỜI", [11, "món"]))),
    sc("date", 12, vid=V["tape2"], tone="noir", day="MÁY NGHE LÉN TRONG VĂN PHÒNG THỦ LĨNH MAFIA BOSTON", date="1981"),
    sc("kinetic", 13, bg="northend", items=kin(("HAI NĂM SAU", [13, "Hai"], "sm"), ("CẢ BỘ SẬU BỊ BẮT", [13, "bắt"], "acc"))),
    sc("kinetic", 14, vid=V["cards"], tone="noir", items=kin(("TRONG HỒ SƠ", [14, "hồ"], "sm"), ("BULGER VÀ FLEMMI ĐƯỢC GHI CÔNG", [14, "ghi"]), ("VÌ GIÚP MÔ TẢ CĂN PHÒNG", [14, "mô"], "sm"))),
    sc("question", 15, bg="northend", text="Khi mafia gốc Ý sụp đổ,\nai lấp đầy khoảng trống?"),
    sc("slam", 16, bg="winterhill", text="BĂNG WINTER HILL", white=True, hitAt=[16, "Winter"]),
    sc("kinetic", 17, vid=V["files"], tone="noir", items=kin(("SAU CUỘC GẶP ẤY", [17, "gặp"], "sm"), ("FBI MỞ MỘT HỒ SƠ MỚI", [17, "mở"]))),
    sc("file", 18, k="HỒ SƠ NGƯỜI CUNG CẤP TIN · FBI BOSTON", name="BS 1544", desc="James J. Bulger", bg="fbi_hq",
       rows=[{"k": "HẠNG", "v": "*TE* · Top Echelon", "at": [19, "TE"]}, {"k": "NGHĨA LÀ", "v": "Cấp chỉ điểm *cao nhất*", "at": [19, "cấp"]}]),
    sc("counter", 20, vid=V["box"], tone="noir", **{"from": 0, "to": 700}, prefix="≈ ", countAt=[20, "bảy"], label="TRANG HỒ SƠ · SAU 15 NĂM"),
    sc("kinetic", 21, bg="mug2011", items=kin(("VỀ PHÍA BULGER", [21, "Bulger"], "sm"), ("HẮN CHỐI CHO TỚI NGÀY CHẾT", [21, "chối"]))),
    sc("split", 22, title="LỜI CỦA BULGER", a={"img": "mug1983", "label": "KHÔNG BAO GIỜ BÁN TIN", "at": [22, "bán"]}, b={"img": "fbi_hq", "label": "CHỈ MUA TIN TỪ ĐẶC VỤ ĂN TIỀN", "at": [22, "mua"]}),
    sc("kinetic", 23, vid=V["gavel"], tone="noir", items=kin(("BẠN SẼ NGHE LẠI LỜI CHỐI ẤY", [23, "nghe"]), ("TRƯỚC TÒA", [23, "tòa"], "acc"))),
    sc("photo", 24, img="globe", tone="color", move="in", kin=kin(("CONNOLLY CÓ CÁCH GIẢI THÍCH KHÁC", [24, "cách"]), ("NÓI VỚI BÁO BOSTON GLOBE", [24, "Globe"], "sm")),
       label={"k": "TÒA SOẠN BÁO BOSTON GLOBE", "v": "ẢNH NĂM 2009", "at": [24, "Còn"]}),
    sc("quote", 25, text="Chúng tôi tóm được bốn mươi hai tội phạm thứ thiệt, bằng cách buông hai tên.", by="JOHN CONNOLLY · NÓI VỚI BÁO BOSTON GLOBE", lbl="TRÍCH DỊCH", qline=25, typeAt=[25, "Chúng"]),
    sc("photo", 26, img="surv", tone="color", kin=kin(("HAI TÊN ĐƯỢC BUÔNG", [26, "Hai"]), ("BULGER VÀ FLEMMI", [26, "Bulger"], "acc")),
       label={"k": "BULGER VÀ FLEMMI · ẢNH THEO DÕI CỦA FBI", "v": "TƯ LIỆU", "at": [26, "tên"]}),
    sc("kinetic", 27, vid=V["doc"], tone="noir", items=kin(("TRÊN GIẤY TỜ", [27, "giấy"], "sm"), ("ĐÓ LÀ MỘT CUỘC TRAO ĐỔI", [27, "trao"]))),
    sc("slam", 28, vid=V["drive_bw"], tone="noir", text="MỘT THỨ KHÁC HẲN", hitAt=[28, "khác"]),
    sc("kinetic", 29, bg="mug1983", items=kin(("NGƯỜI ĐƯỢC BẢO VỆ", [29, "bảo"]), ("ĐÃ HIỂU RA MỘT ĐIỀU", [29, "hiểu"], "sm"))),
    sc("kinetic", 30, vid=V["tape3"], tone="noir", items=kin(("KHÔNG CHỈ CÓ MỘT TẤM KHIÊN", [30, "tấm"]))),
    sc("slam", 31, bg="fbi_hq2", text="MỘT ĐÔI TAI\nBÊN TRONG FBI", hitAt=[31, "đôi"]),
])

CH["ch05"] = dict(hud={"k": "CHƯƠNG 05", "t": "CÁI TÊN BỊ GẠCH KHỎI CÁO TRẠNG"}, bgm={"mood": "epic", "at": 0, "gain": 0.11}, scenes=[
    chapter("5", "CHƯƠNG NĂM", "CÁI TÊN BỊ GẠCH\nKHỎI CÁO TRẠNG", "1979 — 1981", "Cái", bg="suffolk"),
    sc("kinetic", 1, bg="winterhill", items=kin(("CUỐI THẬP NIÊN 1970", [1, "1970"], "sm"), ("MỘT TRÒ RẤT CŨ", [1, "trò"]))),
    sc("broll", 2, vid=V["race"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("MUA CHUỘC CÁC NÀI NGỰA", [2, "nài"]), ("DÀN XẾP KẾT QUẢ KHẮP BỜ ĐÔNG", [2, "dàn"], "acc"))),
    sc("photo", 3, img="suffolk_board", tone="color", illus="ẢNH MINH HỌA · TRƯỜNG ĐUA SUFFOLK DOWNS, BOSTON",
       kin=kin(("MỘT NGƯỜI TRONG ĐƯỜNG DÂY BỊ BẮT", [3, "bắt"]), ("VÀ QUYẾT ĐỊNH KHAI", [3, "khai"], "acc"))),
    sc("date", 4, vid=V["typew"], tone="noir", day="CÁO TRẠNG LIÊN BANG ĐƯỢC CÔNG BỐ", date="02.1979"),
    sc("dots", 5, vid=V["doc"], tone="noir", total=21, cols=7, title="21 CÁI TÊN TRONG CÁO TRẠNG",
       groups=[{"from": 0, "n": 1, "cls": "red", "label": "HOWIE WINTER · ĐỨNG ĐẦU", "at": [6, "Howie"]},
               {"from": 1, "n": 20, "cls": "hollow", "label": "HẦU NHƯ MỌI NHÂN VẬT CHỦ CHỐT", "at": [7, "mọi"]}]),
    sc("slam", 8, bg="surv", text="CHỈ THIẾU HAI NGƯỜI", white=True, hitAt=[8, "thiếu"]),
    sc("kinetic", 9, bg="fbi_hq", items=kin(("TRƯỚC KHI CÁO TRẠNG ĐƯỢC KÝ", [9, "ký"], "sm"), ("CONNOLLY VÀ CẤP TRÊN TỚI GẶP CÔNG TỐ VIÊN", [9, "gặp"]))),
    sc("kinetic", 10, vid=V["lawyer"], tone="noir", items=kin(("NGUỒN TIN KHÔNG THỂ THIẾU", [10, "nguồn"]), ("TRONG CUỘC CHIẾN CHỐNG MAFIA", [10, "chống"], "sm"))),
    sc("file", 11, k="CÁO TRẠNG DÀN XẾP ĐUA NGỰA · 02.1979", name="BULGER\nFLEMMI", desc="Chỉ còn là đồng phạm không bị truy tố", bg="suffolk",
       stamp={"text": "GẠCH TÊN", "at": [11, "gạch"]}),
    sc("counter", 13, vid=V["cells"], tone="noir", **{"from": 0, "to": 10}, suffix=" NĂM TÙ", countAt=[14, "mười"], label="HOWIE WINTER · ÔNG CHỦ CỦA BĂNG"),
    sc("kinetic", 15, bg="winterhill_snow", items=kin(("BĂNG WINTER HILL", [15, "Winter"], "sm"), ("MẤT NGƯỜI ĐỨNG ĐẦU", [15, "mất"]))),
    sc("slam", 16, bg="mug1983", text="CHIẾC GHẾ TRỐNG", hitAt=[16, "ghế"], sub="NGƯỜI NGỒI VÀO: WHITEY BULGER"),
    sc("broll", 17, vid=V["garage"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("ĐẠI BẢN DOANH MỚI", [17, "đại"], "sm"), ("GA-RA TRÊN PHỐ LANCASTER", [17, "Lancaster"], "acc"))),
    sc("kinetic", 18, vid=V["tape"], tone="noir", items=kin(("CẢNH SÁT BANG", [18, "Cảnh"]), ("TỪNG ĐẶT MÁY NGHE LÉN Ở ĐÓ", [18, "nghe"], "acc"))),
    sc("broll", 19, vid=V["window"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("TỪ CĂN NHÀ BÊN KIA ĐƯỜNG", [19, "bên"]), ("CHỤP ĐƯỢC HẮN TIẾP MỌI TAY MAFIA CÓ MÁU MẶT", [19, "chụp"], "acc"))),
    sc("slam", 20, vid=V["garage2"], tone="noir", text="BỖNG CHUYỂN SANG\nTHỜI TIẾT", hitAt=[20, "thời"], sub="CHỈ ÍT NGÀY SAU"),
    sc("kinetic", 21, vid=V["tape3"], tone="noir", items=kin(("AI ĐÓ", [21, "Ai"], "sm"), ("ĐÃ BÁO CHO HẮN", [21, "báo"], "acc"))),
    sc("kinetic", 22, vid=V["bos_dusk"], tone="noir", items=kin(("LẦN ĐẦU TIÊN", [22, "đầu"], "sm"), ("CÁC CƠ QUAN KHÁC NHẬN RA ĐIỀU KHÔNG ỔN", [22, "nhận"]))),
    sc("photo", 23, img="rotary", tone="color", kin=kin(("MỖI LẦN HỌ TỚI GẦN", [23, "gần"]), ("HẮN LẠI BIẾT TRƯỚC", [23, "biết"], "acc")),
       label={"k": "ẢNH THEO DÕI BULGER CỦA DEA", "v": "NĂM 1989", "at": [23, "Mỗi"]}),
    sc("broll", 24, vid=V["xmas"], tone="night", veil=0.4, illus=FILMV,
       kin=kin(("MỖI MÙA GIÁNG SINH", [24, "Giáng"]), ("THEO LỜI KHAI CỦA ĐỒNG PHẠM", [24, "lời"], "sm"), ("PHONG BÌ VÀ QUÀ TỚI VÀI ĐẶC VỤ", [24, "phong"], "acc"))),
    sc("kinetic", 25, vid=V["cash2"], tone="noir", items=kin(("MỘT CẤP TRÊN CỦA CONNOLLY", [25, "cấp"]), ("VỀ SAU THỪA NHẬN ĐÃ NHẬN TIỀN", [25, "thừa"], "acc"))),
    sc("kinetic", 26, vid=V["files"], tone="noir", items=kin(("TIN BULGER ĐƯA CHO FBI", [26, "tin"]), ("THƯA DẦN · NHẠT DẦN", [26, "thưa"], "sm"))),
    sc("slam", 27, vid=V["tape2"], tone="noir", text="TIN ĐI THEO\nCHIỀU NGƯỢC LẠI", hitAt=[27, "ngược"]),
    sc("kinetic", 28, bg="fbi_hq2", items=kin(("CÓ NHỮNG TIN", [28, "tin"], "sm"), ("ĐỒNG NGHĨA VỚI MỘT BẢN ÁN", [28, "bản"], "acc"))),
])

CH["ch06"] = dict(hud={"k": "CHƯƠNG 06", "t": "NHỮNG NGƯỜI BIẾT QUÁ NHIỀU"}, bgm={"mood": "sad", "at": 0, "gain": 0.12}, scenes=[
    chapter("6", "CHƯƠNG SÁU", "NHỮNG NGƯỜI\nBIẾT QUÁ NHIỀU", "1981 — 1985", "Những", bg="tulsa2"),
    sc("map", 1, geo="us", pins=[{"name": "Boston", "at": [1, "Ngày"]}, {"name": "Tulsa", "label": "TULSA · OKLAHOMA · 27.05.1981", "at": [1, "Tulsa"]}],
       routes=[{"from": "Boston", "to": "Tulsa", "at": [1, "tại"], "until": [1, "Oklahoma"], "bend": 0.15}]),
    sc("broll", 2, vid=V["golf"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("DOANH NHÂN ROGER WHEELER", [2, "Roger"]), ("VỪA CHƠI XONG MỘT VÁN GOLF", [2, "golf"], "sm"))),
    sc("kinetic", 3, vid=V["golf2"], tone="noir", items=kin(("CHỦ MỘT CÔNG TY CÁ CƯỢC THỂ THAO", [3, "chủ"]), ("NGHI WINTER HILL RÚT RUỘT TIỀN CỦA MÌNH", [3, "nghi"], "acc"))),
    sc("photo", 4, img="tulsa", tone="color", move="in", kin=kin(("BÃI ĐẬU XE CỦA CÂU LẠC BỘ", [4, "bãi"])),
       label={"k": "CÂU LẠC BỘ SOUTHERN HILLS · TULSA", "v": "ẢNH NGÀY NAY", "at": [4, "Ông"]}),
    sc("kinetic", 5, vid=V["bos_water"], tone="noir", items=kin(("MỘT NGƯỜI Ở BOSTON", [5, "Boston"]), ("BIẾT AI ĐỨNG SAU", [5, "biết"], "acc"))),
    sc("file", 6, k="BOSTON · ĐẦU NĂM 1982", name="BRIAN\nHALLORAN", desc="Tìm tới FBI · xin được bảo vệ để đổi lấy lời khai", bg="fbi_hq"),
    sc("slam", 8, bg="fbi_hq2", text="TIN ẤY KHÔNG Ở YÊN\nTRONG TÒA NHÀ FBI", hitAt=[8, "không"]),
    sc("date", 9, vid=V["boats2"], tone="noir", day="HALLORAN RỜI MỘT QUÁN ĂN Ở BỜ CẢNG NAM BOSTON", date="11.05.1982"),
    sc("kinetic", 10, vid=V["bos_street"], tone="noir", items=kin(("MỘT NGƯỜI QUEN CHO ĐI NHỜ XE", [10, "nhờ"]), ("MICHAEL DONAHUE", [10, "Michael"], "acc"))),
    sc("ledger", 11, title="MICHAEL DONAHUE", bg="southie_pan", rows=[{"k": "NGHỀ", "v": "TÀI XẾ XE TẢI", "at": [11, "tài"]}, {"k": "GIA ĐÌNH", "v": "CHA CỦA BA ĐỨA CON", "at": [11, "cha"]},
                                                                     {"k": "VỚI THẾ GIỚI ẤY", "v": "KHÔNG DÍNH GÌ", "at": [11, "không"]}]),
    sc("seismo", 12, bg="oldcolony", label="BỜ CẢNG NAM BOSTON · CHIỀU 11.05.1982", read="MỘT CHIẾC XE KHÁC TRỜ TỚI", hitAt=[12, "trờ"]),
    sc("memorial", 13, title="TƯỞNG NIỆM", names=[{"n": "BRIAN HALLORAN", "s": "1982", "at": [13, "Cả"]}, {"n": "MICHAEL DONAHUE", "s": "TÀI XẾ XE TẢI · 1982", "at": [13, "đều"]}]),
    sc("map", 14, geo="us", pins=[{"name": "Tulsa", "at": [14, "Tulsa"]}, {"name": "Miami", "label": "FLORIDA · BA THÁNG SAU", "at": [14, "Florida"]}]),
    sc("broll", 15, vid=V["boats"], tone="noir", veil=0.4, illus=FILMV, kin=kin(("1984 · NGƯ DÂN TRẺ JOHN McINTYRE", [15, "John"]), ("KỂ VỀ MỘT CON TÀU CHỞ VŨ KHÍ", [15, "tàu"], "acc"))),
    sc("slam", 16, vid=V["boats2"], tone="noir", text="VÀI TUẦN SAU\nANH BIẾN MẤT", hitAt=[16, "biến"]),
    sc("counter", 17, vid=V["fog"], tone="noir", **{"from": 0, "to": 16}, suffix=" NĂM", countAt=[17, "Mười"], label="SAU ĐÓ NGƯỜI TA MỚI TÌM THẤY ANH"),
    sc("kinetic", 18, vid=V["snowcity"], tone="noir", items=kin(("ĐẦU NĂM 1985", [18, "1985"], "sm"), ("DEBORAH HUSSEY · 26 TUỔI", [18, "Deborah"]), ("CŨNG BIẾN MẤT", [18, "biến"], "acc"))),
    sc("kinetic", 19, bg="flemmi65", items=kin(("CON RIÊNG CỦA NGƯỜI PHỤ NỮ", [19, "con"]), ("SỐNG CÙNG STEPHEN FLEMMI", [19, "Stephen"], "sm"))),
    sc("date", 20, bg="moakley", day="BỒI THẨM ĐOÀN XEM XÉT 19 VỤ GIẾT NGƯỜI", date="2013"),
    sc("slam", 21, bg="moakley2", text="11 VỤ\nCHỨNG MINH ĐƯỢC", hitAt=[21, "mười"]),
    sc("memorial", 22, title="TRONG ĐÓ CÓ", names=[{"n": "ROGER WHEELER", "s": "TULSA · 1981", "at": [22, "Wheeler"]}, {"n": "BRIAN HALLORAN", "s": "BOSTON · 1982", "at": [22, "Halloran"]},
                                                  {"n": "MICHAEL DONAHUE", "s": "BOSTON · 1982", "at": [22, "Donahue"]}, {"n": "JOHN McINTYRE", "s": "1984", "at": [22, "McIntyre"]}]),
    sc("dots", 23, bg="moakley", total=19, cols=10, title="19 VỤ GIẾT NGƯỜI BỊ CÁO BUỘC",
       groups=[{"from": 0, "n": 11, "cls": "red", "label": "11 VỤ: CHỨNG MINH ĐƯỢC", "at": 23},
               {"from": 11, "n": 7, "cls": "hollow", "label": "7 VỤ: CHƯA ĐỦ CHỨNG CỨ", "at": [23, "Bảy"]},
               {"from": 18, "n": 1, "cls": "gold", "label": "1 VỤ: KHÔNG THỂ KẾT LUẬN", "at": [23, "Một"]}]),
    sc("kinetic", 24, vid=V["corridor"], tone="noir", items=kin(("PHẦN LỚN NHỮNG NGƯỜI ẤY", [24, "Phần"], "sm"), ("CÓ MỘT ĐIỂM CHUNG", [24, "điểm"]))),
    sc("slam", 25, bg="fbi_hq", text="ĐÃ NÓI, HOẶC SẮP NÓI\nVỚI NHÀ CHỨC TRÁCH", hitAt=[25, "nói"]),
    sc("kinetic", 26, vid=V["justice"], tone="noir", items=kin(("SUỐT NHỮNG NĂM ẤY", [26, "Suốt"], "sm"), ("KHÔNG MỘT CÁO TRẠNG NÀO CHẠM TỚI HẮN", [26, "cáo"]))),
    sc("photo", 27, img="mural", tone="color", move="in", kin=kin(("TRÊN ĐƯỜNG PHỐ SOUTHIE", [27, "Southie"]), ("NGƯỜI TA KỂ VỀ HẮN NHƯ MỘT NGƯỜI CHE CHỞ", [27, "che"], "acc")),
       label={"k": "BÍCH HỌA Ở NAM BOSTON", "v": "ẢNH NĂM 2004", "at": [27, "Trên"]}),
    sc("ledger", 28, title="HUYỀN THOẠI VỀ WHITEY", bg="southie_air", rows=[{"k": "BÀ CỤ", "v": "XÁCH ĐỒ GIÚP", "at": [28, "xách"]}, {"k": "LỄ TẠ ƠN", "v": "TẶNG GÀ TÂY", "at": [28, "gà"]},
                                                                           {"k": "MA TÚY", "v": "KHÔNG VÀO KHU PHỐ", "at": [29, "ma"]}]),
    sc("slam", 30, vid=V["bos_dusk"], tone="noir", text="ÍT NHẤT\nNGƯỜI TA KỂ NHƯ VẬY", hitAt=[30, "kể"]),
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
    write(__file__, CH, IMGS, GEO, endcardBg="sm_beach")
