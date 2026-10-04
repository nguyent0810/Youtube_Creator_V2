"""Sinh spec (imgs/geo/youtube) + hud/bgm/scenes cho data/long/golden/chNN.json (giữ nguyên "lines").

    python data/long/golden/gen_scenes.py
Hiệu ứng chữ (fx) để trống: build_long/beatfx tự chọn. Ảnh ngoài Commons: EXT:<nguồn>:<id> (đã tải bằng media_search.py).
"""
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
RES = json.loads((D.parents[2] / "output/long/golden/research.json").read_text(encoding="utf-8"))["images"]

IDX = dict(gt_temple=0, poppy=1, mekong_pano=2, doipukhao=3, mta_recruits=4, khunsa_9=5, khunsa1974=6, burma1954=7, burma1953=8, cia_map=9,
           pods=10, khunsa=11, khunsa_crop=12, confluence1985=40, gt_pano=41, sopruak_sign=42, gt_monument=43, chiangsaen=45,
           field_fuzhou=59, poppy_turkey=60, kmt_hall=67, li_mi=69, maesalong_tea=73, kmt_hall2=74, maesalong_view=76,
           cat_c46=89, cat_c46_1950=90, c46_hainan=95, t28_laos=97, t28_line=98, t28_damaged=101,
           mekong_boats=121, sopruak_border=123, opium_pipe=127, opium_pipe2=128, gtsez1=130, ferry1=131, ferry2=132, gtsez_tower=133,
           gtsez11=134, meth_bust=148, taunggyi=151, ssa_south=168, chiang=198, uwsa=218, myawaddy=226,
           vn_patrol=248, harlem125=263, nyc42=276, bkk1971=282)
IMGS = {k: RES[i]["file"] for k, i in IDX.items()}
IMGS.update({"opium_den": "EXT:wellcome:cbk3dxpe", "patna": "EXT:wellcome:myjgzewf",
             "sat_confluence": "EXT:sentinel2:S2B_MSIL2A_20240329T034539_R104_T47QPC_20240330T073158",
             "kaitak1991": "File:啟德機場 - Landing at Kai Tak - 1991 (2350897476).jpg",
             "kaitak1971": "File:Hong Kong Kai Tak Airport 1971.jpg"})

GEO = {
    "gt": {"countries": ["Myanmar", "Laos", "Thailand"], "context": ["China", "Vietnam", "Cambodia", "India", "Bangladesh", "Taiwan"],
           "labels": {"Myanmar": "MIẾN ĐIỆN", "Laos": "LÀO", "Thailand": "THÁI LAN"}, "bbox": [93.5, 12.5, 110.5, 27.5], "box": [260, 120, 1660, 860],
           "pins": [{"name": "Tam Giác Vàng", "lon": 100.08, "lat": 20.35, "label": "TAM GIÁC VÀNG"},
                    {"name": "Tachileik", "lon": 99.88, "lat": 20.45, "label": "TACHILEIK"},
                    {"name": "Mong Hsat", "lon": 99.26, "lat": 20.53, "label": "MONG HSAT"},
                    {"name": "Chiang Mai", "lon": 98.99, "lat": 18.79, "label": "CHIANG MAI"},
                    {"name": "Mandalay", "lon": 96.08, "lat": 21.97, "label": "MANDALAY"},
                    {"name": "Yangon", "lon": 96.16, "lat": 16.84, "label": "YANGON"},
                    {"name": "Taunggyi", "lon": 97.03, "lat": 20.78, "label": "TAUNGGYI"},
                    {"name": "Kokang", "lon": 98.55, "lat": 23.69, "label": "KOKANG"},
                    {"name": "Mae Salong", "lon": 99.62, "lat": 20.16, "label": "MAE SALONG"},
                    {"name": "Vân Nam", "lon": 102.7, "lat": 25.04, "label": "VÂN NAM"},
                    {"name": "Bangkok", "lon": 100.5, "lat": 13.75, "label": "BANGKOK"},
                    {"name": "Hà Nội", "lon": 105.85, "lat": 21.03, "label": "HÀ NỘI"},
                    {"name": "Myawaddy", "lon": 98.52, "lat": 16.69, "label": "MYAWADDY"},
                    {"name": "Loi Maw", "lon": 98.1, "lat": 21.7, "label": "LOI MAW"}]},
    "asia": {"countries": ["China", "Taiwan", "Myanmar", "Thailand", "Laos"], "context": ["Vietnam", "Cambodia", "India", "Bangladesh", "South Korea", "North Korea", "Japan", "Philippines", "Mongolia"],
             "labels": {"China": "TRUNG QUỐC", "Taiwan": "ĐÀI LOAN"}, "bbox": [88.0, 8.0, 128.0, 42.0], "box": [220, 120, 1700, 860],
             "pins": [{"name": "Vân Nam", "lon": 102.7, "lat": 25.04, "label": "VÂN NAM"},
                      {"name": "Đài Bắc", "lon": 121.56, "lat": 25.04, "label": "ĐÀI LOAN"},
                      {"name": "Bắc Kinh", "lon": 116.4, "lat": 39.9, "label": "BẮC KINH"},
                      {"name": "Triều Tiên", "lon": 126.0, "lat": 39.0, "label": "TRIỀU TIÊN"},
                      {"name": "Tam Giác Vàng", "lon": 100.08, "lat": 20.35, "label": "TAM GIÁC VÀNG"},
                      {"name": "Hồng Kông", "lon": 114.17, "lat": 22.32, "label": "HỒNG KÔNG"},
                      {"name": "Bangkok", "lon": 100.5, "lat": 13.75, "label": "BANGKOK"}]},
}

FILMV = "VIDEO MINH HỌA"


def sc(t, at=None, **k):
    d = {"type": t}
    if at is not None:
        d["at"] = at
    d.update(k)
    if t == "photo" and d.get("kin"):
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

CH["ch00"] = dict(hud={"k": "MỞ ĐẦU", "t": "MƯỜI SÁU TẤN TRÊN BỜ SÔNG MEKONG"}, bgm={"file": "gathering_darkness.mp3", "at": 0, "gain": 0.13}, scenes=[
    sc("date", None, vid="26829790", tone="night", day="PHÍA BẮC NƯỚC LÀO", date="07.1967"),
    sc("sketch", 1, art="convoy", title="Đoàn la thồ lội qua sông Mekong"),
    sc("counter", 2, bg="field_fuzhou", **{"from": 0, "to": 16}, suffix=" TẤN", countAt=[2, "mười"], label="THUỐC PHIỆN TRÊN LƯNG LA"),
    sc("counter", 3, vid="34697024", tone="night", **{"from": 0, "to": 800}, countAt=[3, "tám"], label="TAY SÚNG HỘ TỐNG"),
    sc("photo", 4, img="sat_confluence", tone="color", move="in", kin=kin(("BAN KHWAN", [4, "Ban"], "acc"), ("CHIẾN LŨY BẰNG GỖ CHƯA XẺ", [4, "khúc"])),
       label={"k": "BỜ SÔNG MEKONG PHÍA LÀO", "v": "ẢNH VỆ TINH NGÀY NAY", "at": [4, "bãi"]}),
    sc("broll", 5, vid="9733917", tone="noir", veil=0.4, illus=FILMV, kin=kin(("CẢ NGHÌN NGƯỜI", [5, "nghìn"]), ("ĐANG ĐUỔI THEO", [5, "đuổi"], "acc"))),
    sc("slam", 6, bg="burma1954", text="KHÔNG PHẢI\nCẢNH SÁT", white=True, hitAt=[6, "cảnh"]),
    sc("print", 7, img="chiang", tone="bw", side={"k": "TÀN QUÂN", "h": "QUỐC DÂN ĐẢNG", "hAt": [7, "Quốc"],
       "lines": [{"text": "Từng chiến đấu cho *Tưởng Giới Thạch*", "at": [7, "Tưởng"]}]}),
    sc("kinetic", 8, bg="mekong_pano", items=kin(("MỘT THỨ DUY NHẤT", [8, "duy"], "sm"), ("THUẾ CHO CON ĐƯỜNG", [8, "thuế"], "acc"))),
    sc("date", 9, vid="6900893", tone="noir", day="BAN KHWAN · SÚNG NỔ", date="29.07.1967"),
    sc("kinetic", 10, vid="4320605", tone="noir", items=kin(("SÚNG MÁY", [10, "Súng"]), ("SÚNG CỐI", [10, "cối,"]), ("SÚNG KHÔNG GIẬT", [10, "giật."], "acc"))),
    sc("broll", 11, vid="17118515", tone="noir", veil=0.4, illus=FILMV, kin=kin(("TRƯA HÔM SAU", [11, "Trưa"]), ("BẦU TRỜI GẦM LÊN", [11, "gầm"], "acc"))),
    sc("photo", 12, img="t28_line", tone="color", move="in", kin=kin(("SÁU MÁY BAY NÉM BOM", [12, "Sáu"], "acc")),
       label={"k": "T-28 CỦA KHÔNG QUÂN LÀO", "v": "ẢNH TƯ LIỆU · 1964 — 1973", "at": [12, "máy"]}),
    sc("kinetic", 13, bg="t28_damaged", items=kin(("KHÔNG BÊNH BÊN NÀO", [13, "bênh"]))),
    sc("slam", 14, bg="t28_damaged", text="NÉM BOM\nCẢ HAI PHE", hitAt=[14, "hai"]),
    sc("photo", 15, img="t28_laos", tone="color", move="in", kin=kin(("MỘT VỊ TƯỚNG THỨ BA", [15, "tướng"]), ("CHỜ ĐẾN LƯỢT MÌNH", [15, "chờ"], "acc"))),
    sc("print", 16, img="khunsa1974", tone="bw", side={"k": "NGƯỜI CẦM ĐẦU ĐOÀN LA", "h": "33 TUỔI", "hAt": [16, "33"],
       "lines": [{"text": "Năm *1967*", "at": [16, "mới"]}]}),
    sc("counter", 17, img="khunsa", tone="bw", **{"from": 0, "to": 2000000}, prefix="$", countAt=[17, "hai"], label="MỸ TREO THƯỞNG CHO CÁI ĐẦU CỦA ÔNG"),
    sc("slam", 18, bg="khunsa_crop", text="KHUN SA", white=True, hitAt=[18, "Khun"], sub="ÔNG VUA THUỐC PHIỆN · 1934 — 2007"),
    sc("photo", 19, img="vn_patrol", tone="bw", move="in", film=True, kin=kin(("HEROIN TỪ VÙNG ĐẤT NÀY", [19, "Heroin"]), ("BÁN CHO LÍNH MỸ Ở VIỆT NAM", [19, "Việt"], "acc")),
       label={"k": "LÍNH MỸ TUẦN TRA Ở VIỆT NAM", "v": "ẢNH TƯ LIỆU · QUÂN ĐỘI MỸ", "at": [19, "lính"]}),
    sc("photo", 20, img="myawaddy", tone="color", move="in", kin=kin(("NGƯỜI TRẺ BỊ LỪA SANG LÀM VIỆC", [20, "lừa"]), ("CÓ CẢ NGƯỜI VIỆT", [20, "Việt."], "acc")),
       label={"k": "MYAWADDY", "v": "BIÊN GIỚI MYANMAR — THÁI LAN", "at": [20, "vùng"]}),
    sc("slam", 21, bg="confluence1985", text="TAM GIÁC VÀNG", white=True, hitAt=[21, "Tam"]),
    sc("kinetic", 22, bg="li_mi", items=kin(("LÍNH CỦA TƯỞNG GIỚI THẠCH", [22, "lính"]), ("→ TRÙM THUỐC PHIỆN?", [22, "trùm"], "acc"))),
    sc("kinetic", 23, bg="khunsa", items=kin(("BỊ MỸ TRUY NÃ", [23, "truy"]), ("CHẾT GIÀ TRONG BIỆT THỰ", [23, "biệt"], "acc"))),
    sc("counter", 24, vid="14314426", tone="night", **{"from": 0, "to": 40}, prefix="~ $", suffix=" TỶ", countAt=[24, "bốn"], label="MỖI NĂM · ƯỚC TÍNH CỦA LIÊN HỢP QUỐC"),
    sc("brand", 25, sub="HỒ SƠ · TAM GIÁC VÀNG"),
    sc("map", 26, geo="gt", pins=[{"name": "Tam Giác Vàng", "at": [26, "vùng"]}], zoom="Tam Giác Vàng", zoomK=1.3),
])

CH["ch01"] = dict(hud={"k": "CHƯƠNG 01", "t": "NGÃ BA CỦA BA NƯỚC"}, bgm={"file": "echoes_of_time_v2.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("1", "CHƯƠNG MỘT", "NGÃ BA\nCỦA BA NƯỚC", "MYANMAR · LÀO · THÁI LAN", "Ngã", bg="confluence1985"),
    sc("photo", 1, img="confluence1985", tone="color", move="in", kin=kin(("SÔNG RUAK → SÔNG MEKONG", [1, "Ruak"])),
       label={"k": "NGÃ BA SÔNG · TAM GIÁC VÀNG", "v": "ẢNH NĂM 1985", "at": [1, "điểm"]}),
    sc("photo", 2, img="sopruak_border", tone="color", move="in", kin=kin(("MYANMAR · LÀO · THÁI LAN", [2, "Myanmar,"], "acc"))),
    sc("counter", 3, vid="34697024", tone="night", **{"from": 0, "to": 200000}, suffix=" KM²", countAt=[3, "hai"], label="VÙNG NÚI QUANH NGÃ BA"),
    sc("broll", 4, vid="26829488", tone="noir", veil=0.35, illus=FILMV, kin=kin(("RỪNG RẬM · SƯƠNG MÙ", [4, "Rừng"]), ("CHÍNH QUYỀN KHÓ VỚI TỚI", [4, "Chính"], "acc"))),
    sc("file", 5, k="HỌP BÁO VỀ THUỐC PHIỆN · 1971", name="MARSHALL\nGREEN", desc="Quan chức Bộ Ngoại giao Mỹ", vid="26829790", tone="noir",
       rows=[{"k": "ĐẶT TÊN CHO VÙNG NÚI", "v": "*Tam Giác Vàng*", "at": [6, "Tam"]}]),
    sc("slam", 6, bg="gt_pano", text="TAM GIÁC VÀNG", white=True, hitAt=[6, "Tam"], sub="GOLDEN TRIANGLE"),
    sc("photo", 7, img="poppy", tone="color", move="in", kin=kin(("ĐÁNG GIÁ NHƯ VÀNG", [7, "vàng."], "acc"))),
    sc("photo", 8, img="pods", tone="color", move="in", kin=kin(("CÂY ANH TÚC", [8, "anh"]), ("CHỈ TRỒNG NHỎ LẺ", [8, "nhỏ"], "acc"))),
    sc("kinetic", 9, bg="doipukhao", items=kin(("GIỮA THẾ KỶ 18", [9, "18,"], "sm"), ("BÁN CHO NGƯỜI NƯỚC NGOÀI", [9, "bán"]))),
    sc("photo", 10, img="maesalong_tea", tone="color", move="in", kin=kin(("CÁC DÂN TỘC MIỀN NÚI", [10, "dân"]), ("DƯỚI MỨC NGHÈO KHỔ", [10, "nghèo"], "acc"))),
    sc("map", 11, geo="asia", pins=[{"name": "Vân Nam", "label": "TỪ PHÍA BẮC", "at": [11, "bắc,"]}]),
    sc("date", 12, bg="field_fuzhou", day="TRUNG QUỐC XÓA SỔ THUỐC PHIỆN", date="CUỐI 1940s"),
    sc("ledger", 13, title="CHIẾN DỊCH CỦA TRUNG QUỐC", bg="field_fuzhou", rows=[{"k": "NGƯỜI NGHIỆN BUỘC ĐI CAI", "v": "10 TRIỆU", "at": [13, "Mười"]},
       {"k": "KẺ BUÔN", "v": "XỬ TỬ", "at": [13, "xử"]}, {"k": "RUỘNG ANH TÚC", "v": "TRỒNG CÂY KHÁC", "at": [13, "Ruộng"]}]),
    sc("slam", 14, bg="poppy_turkey", text="KHÔNG BIẾN MẤT\nCHỈ DỜI ĐI", hitAt=[14, "dời"]),
    sc("map", 15, geo="asia", pins=[{"name": "Vân Nam", "at": [15, "Xuống"]}, {"name": "Tam Giác Vàng", "at": [15, "Tam"]}],
       routes=[{"from": "Vân Nam", "to": "Tam Giác Vàng", "at": [15, "biên"], "until": [15, "Vàng."], "bend": 0.15}]),
    sc("photo", 16, img="burma1954", tone="bw", move="in", film=True, kin=kin(("MỘT ĐỘI QUÂN THUA TRẬN", [16, "đội"]), ("CHẠY VỀ CÙNG HƯỚNG", [16, "hướng"], "acc")),
       label={"k": "BIÊN GIỚI MIẾN ĐIỆN — TRUNG QUỐC", "v": "ẢNH TƯ LIỆU · 1954", "at": [16, "bắc,"]}),
    sc("kinetic", 17, bg="burma1954", items=kin(("KHÔNG MANG THUỐC PHIỆN", [17, "thuốc"]))),
    sc("slam", 18, bg="burma1954", text="HỌ MANG\nTHEO SÚNG", hitAt=[18, "súng."]),
])

CH["ch02"] = dict(hud={"k": "CHƯƠNG 02", "t": "ĐỘI QUÂN KHÔNG CÒN ĐƯỜNG VỀ"}, bgm={"file": "deep_haze.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("2", "CHƯƠNG HAI", "ĐỘI QUÂN\nKHÔNG CÒN ĐƯỜNG VỀ", "VÂN NAM → MIẾN ĐIỆN · 1949 — 1952", "Đội", bg="li_mi"),
    sc("date", 1, vid="15506601", tone="noir", day="QUÂN GIẢI PHÓNG TIẾN VÀO VÂN NAM", date="12.1949"),
    sc("photo", 2, img="chiang", tone="bw", move="in", film=True, kin=kin(("NỘI CHIẾN GẦN KẾT THÚC", [2, "Nội"]), ("TƯỞNG GIỚI THẠCH → ĐÀI LOAN", [2, "Đài"], "acc"))),
    sc("map", 3, geo="asia", pins=[{"name": "Vân Nam", "label": "KHÔNG CÓ ĐƯỜNG RA BIỂN", "at": [3, "biển."]}, {"name": "Đài Bắc", "at": [2, "Đài"]}]),
    sc("map", 4, geo="gt", pins=[{"name": "Vân Nam", "at": [4, "con"]}, {"name": "Tachileik", "at": [4, "Miến"]}],
       routes=[{"from": "Vân Nam", "to": "Tachileik", "at": [4, "đi"], "until": [4, "Myanmar."], "bend": 0.2}]),
    sc("print", 5, img="li_mi", tone="bw", side={"k": "TẬP ĐOÀN QUÂN SỐ 8", "h": "LÝ DI", "hAt": [5, "Lý"],
       "lines": [{"text": "*Quân đoàn 26*", "at": [5, "Quân"]}, {"text": "*Sư đoàn 93*", "at": [5, "Sư"]}]}),
    sc("sketch", 6, art="convoy", title="Cùng vợ con băng rừng qua biên giới"),
    sc("kinetic", 7, bg="burma1953", items=kin(("MIẾN ĐIỆN · ĐỘC LẬP 1948", [7, "độc"]), ("CHÌM TRONG NỘI CHIẾN", [7, "nội"], "acc"))),
    sc("evidence", 8, img="burma1953", tone="color", maxW=620, maxH=760, callouts=[{"x": 0.6, "y": 0.5, "text": "QUÂN NỔI DẬY & CỘNG SẢN", "at": [8, "Karen,"], "side": "r"}]),
    sc("kinetic", 9, bg="burma1954", items=kin(("VỪA GIÀNH LẠI THẾ THƯỢNG PHONG", [9, "thượng"]), ("MỘT ĐỘI QUÂN LẠ", [9, "lạ"], "acc"))),
    sc("bars", 10, title="TÀN QUÂN QUỐC DÂN ĐẢNG Ở MIẾN ĐIỆN", unit="NGƯỜI", items=[{"k": "3.1950", "v": 1500, "at": [10, "nghìn"]}, {"k": "4.1951", "v": 4000, "at": [11, "bốn"]},
       {"k": "CUỐI 1951", "v": 6000, "at": [11, "sáu"]}, {"k": "1952", "v": 12000, "acc": True, "at": [12, "gấp"]}]),
    sc("file", 13, k="CHÍNH PHỦ MIẾN ĐIỆN · 6.1950", name="ĐẦU HÀNG\nHOẶC RỜI ĐI", desc="Yêu cầu gửi tàn quân Quốc Dân Đảng", bg="burma1954",
       rows=[{"k": "TRẢ LỜI", "v": "*Không đầu hàng · không rời đi*", "at": [14, "không"]}, {"k": "NẾU BỊ TẤN CÔNG", "v": "Đánh trả", "at": [14, "đánh"]}]),
    sc("map", 15, geo="gt", pins=[{"name": "Tachileik", "label": "BỊ ĐÁNH ĐUỔI", "at": [15, "đuổi"]}, {"name": "Mong Hsat", "at": [16, "Mong"]}],
       routes=[{"from": "Tachileik", "to": "Mong Hsat", "at": [16, "rút"], "until": [16, "Hsat,"], "bend": 0.3}], zoom="Mong Hsat", zoomK=1.4),
    sc("broll", 16, vid="15506601", tone="noir", veil=0.35, illus=FILMV, kin=kin(("THUNG LŨNG MÀU MỠ", [16, "thung"]), ("~130 KM TỚI BIÊN GIỚI THÁI", [16, "130"], "acc"))),
    sc("kinetic", 17, bg="burma1954", items=kin(("TẤN CÔNG NHIỀU LẦN", [17, "tấn"]), ("KHÔNG LẦN NÀO ĐUỔI ĐƯỢC", [17, "Không"], "acc"))),
    sc("kinetic", 18, bg="li_mi", items=kin(("KHÔNG HẬU PHƯƠNG", [18, "hậu"]), ("KHÔNG LƯƠNG", [18, "lương,"]), ("VẪN ĐỨNG VỮNG", [18, "vững"], "acc"))),
    sc("slam", 19, bg="cat_c46_1950", text="MỘT NGƯỜI BẠN\nRẤT GIÀU", hitAt=[19, "giàu."]),
    sc("map", 20, geo="asia", pins=[{"name": "Tam Giác Vàng", "label": "NỬA VÒNG TRÁI ĐẤT", "at": [20, "nửa"]}]),
])

CH["ch03"] = dict(hud={"k": "CHƯƠNG 03", "t": "CHIẾN DỊCH GIẤY"}, bgm={"file": "dark_times.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("3", "CHƯƠNG BA", "CHIẾN DỊCH GIẤY", "CIA · 1950 — 1953", "Chiến", bg="cat_c46"),
    sc("map", 1, geo="asia", pins=[{"name": "Triều Tiên", "label": "CHIẾN TRANH TRIỀU TIÊN", "at": [1, "Triều"]}]),
    sc("kinetic", 2, vid="18308549", tone="noir", items=kin(("WASHINGTON LO SỢ", [2, "Washington"]), ("ĐÔNG NAM Á → CỘNG SẢN", [2, "cộng"], "acc"))),
    sc("map", 3, geo="asia", pins=[{"name": "Tam Giác Vàng", "label": "ĐỘI QUÂN LÝ DI", "at": [3, "Lý"]}, {"name": "Vân Nam", "label": "QUẤY RỐI NAM TRUNG QUỐC", "at": [3, "quấy"]},
       {"name": "Triều Tiên", "at": [3, "Triều"]}], routes=[{"from": "Tam Giác Vàng", "to": "Vân Nam", "at": [3, "quấy"], "until": [3, "Quốc,"], "bend": 0.1}]),
    sc("file", 4, k="CIA · MẬT DANH", name="CHIẾN DỊCH\nGIẤY", desc="Operation Paper", bg="cat_c46",
       rows=[{"k": "PHÊ DUYỆT", "v": "*Tổng thống Truman*", "at": [5, "Truman"]}, {"k": "MƯỢN ĐƯỜNG", "v": "Thủ tướng Thái Phibun", "at": [5, "Phibun"]},
             {"k": "KHÔNG ĐƯỢC BÁO", "v": "*Bộ Ngoại giao Mỹ*", "at": [6, "Ngoại"]}], stamp={"text": "MẬT", "at": [6, "báo:"]}),
    sc("photo", 7, img="cat_c46", tone="color", move="in", kin=kin(("C-46 · C-47 KHÔNG PHÙ HIỆU", [7, "phù"]), ("≥ 5 CHUYẾN THẢ DÙ / TUẦN", [7, "năm"], "acc")),
       label={"k": "C-46 CỦA HÃNG CAT · HÃNG BAY CỦA CIA", "v": "ẢNH TƯ LIỆU · ĐÔNG DƯƠNG", "at": [7, "máy"]}),
    sc("sketch", [7, "thả"], art="airdrop", title="Thả dù tiếp tế xuống Mong Hsat"),
    sc("photo", 8, img="c46_hainan", tone="bw", move="pan", film=True, kin=kin(("ĐƯỜNG BĂNG CHO MÁY BAY 4 ĐỘNG CƠ", [8, "bốn"]), ("VŨ KHÍ MỸ TỪ ĐÀI LOAN", [8, "vũ"], "acc"))),
    sc("date", 9, bg="li_mi", day="~20.000 QUÂN ĐÁNH NGƯỢC VÀO VÂN NAM", date="05.1951"),
    sc("map", 10, geo="asia", pins=[{"name": "Vân Nam", "label": "CHIẾM 1 THỊ TRẤN + SÂN BAY", "at": [10, "chiếm"]}], zoom="Vân Nam", zoomK=1.3),
    sc("counter", 11, vid="9508953", tone="noir", **{"from": 0, "to": 40000}, countAt=[11, "bốn"], label="QUÂN GIẢI PHÓNG PHẢN CÔNG"),
    sc("kinetic", 12, bg="burma1954", items=kin(("CHƯA ĐẦY MỘT THÁNG", [12, "tháng,"]), ("THÁO CHẠY · CỐ VẤN CIA TỬ TRẬN", [12, "cố"], "acc"))),
    sc("timeline", 13, bg="burma1953", items=[{"year": "05.1951", "text": "Thất bại"}, {"year": "07.1951", "text": "*Thất bại*"}, {"year": "08.1952", "text": "*Thất bại*"}]),
    sc("file", 15, k="CUỐI 1951", name="CHIẾN DỊCH\nBỊ LỘ", desc="Thái Lan tưởng người Anh đã biết, nên nói hớ", bg="cat_c46_1950",
       rows=[{"k": "HỆ QUẢ", "v": "Đại sứ Mỹ tại Miến Điện *từ chức*", "at": [16, "từ"]}], stamp={"text": "BỊ LỘ", "at": [15, "lộ,"]}),
    sc("kinetic", 17, bg="burma1953", items=kin(("TRỚ TRÊU HƠN", [17, "Trớ"], "sm"), ("LIÊN MINH QUÂN NỔI DẬY KAREN", [17, "Karen."]))),
    sc("slam", 18, bg="burma1954", text="VŨ KHÍ MỸ\nTRONG TAY CỘNG SẢN", hitAt=[18, "cộng"]),
    sc("kinetic", 19, bg="li_mi", items=kin(("SAU 1952", [19, "1952,"], "sm"), ("KHÔNG BAO GIỜ ĐÁNH VÀO TRUNG QUỐC NỮA", [19, "không"]))),
    sc("kinetic", 20, bg="maesalong_view", items=kin(("NHƯNG CŨNG KHÔNG BỎ ĐI", [20, "bỏ"], "acc"))),
    sc("broll", 21, vid="27090146", tone="noir", veil=0.4, illus=FILMV, kin=kin(("NHIỀU TIỀN HƠN CHIẾN TRANH", [21, "tiền"], "acc"))),
])

CH["ch04"] = dict(hud={"k": "CHƯƠNG 04", "t": "THUẾ TRÊN CÁNH ĐỒNG HOA"}, bgm={"file": "oppressive_gloom.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("4", "CHƯƠNG BỐN", "THUẾ TRÊN\nCÁNH ĐỒNG HOA", "BANG SHAN · 1952 — 1961", "Thuế", vid="27090146", tone="noir"),
    sc("map", 1, geo="gt", pins=[{"name": "Mong Hsat", "label": "TỎA RA KHẮP BANG SHAN", "at": [1, "tỏa"]}], zoom="Mong Hsat", zoomK=1.25),
    sc("counter", 2, bg="burma1954", **{"from": 0, "to": 1000000}, countAt=[2, "một"], label="DÂN DƯỚI QUYỀN CAI TRỊ CỦA TÀN QUÂN"),
    sc("kinetic", 3, bg="burma1954", items=kin(("BẮT LÍNH NGƯỜI SHAN · WA · LAHU", [3, "Shan,"]), ("12.000 QUÂN", [3, "mười"], "acc"))),
    sc("ledger", 4, title="THUẾ CỦA TÀN QUÂN", bg="field_fuzhou", rows=[{"k": "LƯƠNG THỰC", "v": "✓", "at": [4, "lương"]}, {"k": "TIỀN", "v": "✓", "at": [4, "tiền,"]},
       {"k": "THUỐC PHIỆN", "v": "TRÊN HẾT", "at": [4, "trên"]}]),
    sc("sketch", 5, art="harvest", title="Trồng nhiều anh túc hơn để đủ nộp thuế"),
    sc("bars", 6, title="SẢN LƯỢNG THUỐC PHIỆN MIẾN ĐIỆN (TẤN/NĂM)", unit="TẤN", items=[{"k": "1948", "v": 30, "at": [6, "ba"]}, {"k": "GIỮA 1950s", "v": 600, "acc": True, "at": [7, "sáu"]}]),
    sc("slam", 8, bg="poppy_turkey", text="GẤP 20 LẦN", white=True, hitAt=[8, "hai"]),
    sc("map", 9, geo="gt", pins=[{"name": "Mong Hsat", "at": [9, "Gần"]}, {"name": "Chiang Mai", "at": [11, "Chiang"]}],
       routes=[{"from": "Mong Hsat", "to": "Chiang Mai", "at": [9, "chở"], "until": [9, "Lan."], "bend": 0.2}]),
    sc("split", 10, title="MỘT CHUYẾN · HAI CHIỀU", a={"img": "cat_c46_1950", "label": "LÊN: VŨ KHÍ · QUÂN NHU", "at": [10, "vũ"]}, b={"img": "field_fuzhou", "label": "VỀ: THUỐC PHIỆN", "at": [11, "thuốc"]}),
    sc("file", 12, k="NGƯỜI NHẬN HÀNG Ở CHIANG MAI", name="MỘT TƯỚNG\nCẢNH SÁT THÁI", desc="Quyền lực, và là khách hàng của CIA", vid="5909916", tone="noir"),
    sc("map", 13, geo="gt", pins=[{"name": "Kokang", "label": "OLIVE YANG · KOKANG", "at": [13, "Olive"]}], zoom="Kokang", zoomK=1.3),
    sc("kinetic", 14, bg="burma1953", items=kin(("1953 · ĐUỔI ĐƯỢC TÀN QUÂN", [14, "Bà"]))),
    sc("slam", 15, bg="field_fuzhou", text="RỒI HỢP TÁC\nVỚI HỌ", hitAt=[15, "hợp"]),
    sc("timeline", 16, bg="burma1953", items=[{"year": "1953", "text": "Miến Điện kiện lên *Liên Hợp Quốc*"}, {"year": "1954", "text": "Lý Di *giải tán quân*"},
       {"year": "1960–61", "text": "Chiến dịch chung *Miến Điện + Trung Quốc*"}]),
    sc("counter", 18, bg="kmt_hall", **{"from": 0, "to": 6000}, countAt=[18, "sáu"], label="NGƯỜI VẪN Ở LẠI"),
    sc("photo", 20, img="maesalong_view", tone="color", move="in", kin=kin(("MỘT SỐ Ở LẠI NÚI BẮC THÁI LAN", [20, "Thái"])),
       label={"k": "MAE SALONG · BẮC THÁI LAN", "v": "ẢNH NGÀY NAY", "at": [20, "núi"]}),
    sc("date", 21, bg="kmt_hall2", day="ĐÀI LOAN CẮT NGUỒN TIỀN", date="1961", stamp={"text": "CẮT TIỀN", "at": [21, "cắt"]}),
    sc("slam", 22, bg="li_mi", text="CÂU HỎI THỨ NHẤT", white=True, hitAt=[22, "đầu"], sub="ĐÃ CÓ CÂU TRẢ LỜI"),
    sc("quote", 23, text="Muốn giữ quân đội thì phải buôn thuốc phiện.", by="LẬP LUẬN CỦA CÁC TƯỚNG TÀN QUÂN · DIỄN Ý", dy=True, typeAt=[23, "muốn"]),
    sc("counter", 24, bg="field_fuzhou", **{"from": 0, "to": 90}, suffix="%", countAt=[24, "chín"], label="THUỐC PHIỆN CỦA MIẾN ĐIỆN"),
    sc("sketch", 25, art="convoy", title="Đoàn la dài tới 600 con, chở gần 20 tấn"),
    sc("slam", 26, bg="mekong_pano", text="THUẾ QUÁ CẢNH", white=True, hitAt=[26, "thuế"]),
    sc("kinetic", 27, bg="kmt_hall", items=kin(("ĐỘI QUÂN YÊU NƯỚC", [27, "yêu"]), ("TRẠM THU PHÍ CỦA CẢ VÙNG NÚI", [27, "thu"], "acc"))),
    sc("kinetic", 28, bg="mekong_pano", items=kin(("KHÔNG AI DÁM KHÔNG NỘP", [28, "dám"]))),
    sc("print", 29, img="khunsa1974", tone="bw", side={"k": "CHO TỚI KHI", "h": "MỘT CHÀNG TRAI TRẺ", "hAt": [29, "chàng"],
       "lines": [{"text": "Từng được chính họ *huấn luyện*", "at": [29, "huấn"]}, {"text": "Quyết định *không nộp nữa*", "at": [29, "không"]}]}),
])

CH["ch05"] = dict(hud={"k": "CHƯƠNG 05", "t": "CẬU BÉ TRƯƠNG KỲ PHU"}, bgm={"file": "night_cave.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("5", "CHƯƠNG NĂM", "CẬU BÉ\nTRƯƠNG KỲ PHU", "BANG SHAN · 1934 — 1967", "Cậu", bg="khunsa1974"),
    sc("date", 1, bg="taunggyi", day="LÀNG LOI MAW · BANG SHAN", date="17.02.1934"),
    sc("file", 2, k="HỒ SƠ · NHÂN VẬT", name="TRƯƠNG KỲ PHU", desc="Tên Hán: 張奇夫", bg="khunsa1974",
       rows=[{"k": "CHA", "v": "Người Hoa", "at": [2, "Hoa,"]}, {"k": "MẸ", "v": "Người Shan", "at": [2, "Shan."]}]),
    sc("ledger", 3, title="TUỔI THƠ", rows=[{"k": "3 TUỔI", "v": "CHA MẤT", "at": [3, "cha"]}, {"k": "5 TUỔI", "v": "MẸ QUA ĐỜI", "at": [3, "qua"]},
       {"k": "NUÔI LỚN BỞI", "v": "ÔNG NỘI · TRƯỞNG LÀNG", "at": [4, "ông"]}]),
    sc("kinetic", 4, bg="taunggyi", items=kin(("HỌ TRƯƠNG Ở BANG SHAN", [4, "Họ"], "sm"), ("TỪ THẾ KỶ 18", [4, "18."]))),
    sc("kinetic", 5, bg="gt_temple", items=kin(("ANH EM: TRƯỜNG DÒNG", [5, "dòng."]), ("CẬU: KHÔNG", [5, "không."], "acc"))),
    sc("photo", 6, img="gt_temple", tone="color", move="in", kin=kin(("VÀI NĂM LÀM CHÚ TIỂU", [6, "tiểu"]))),
    sc("slam", 7, bg="khunsa1974", text="GẦN NHƯ\nMÙ CHỮ", hitAt=[7, "đọc"]),
    sc("slam", 8, bg="khunsa1974", text="NHƯNG HỌC RẤT NHANH\nCÁCH CẦM SÚNG", white=True, hitAt=[8, "súng."]),
    sc("kinetic", 9, bg="burma1954", items=kin(("ĐẦU THẬP NIÊN 1950", [9, "1950,"], "sm"), ("QUỐC DÂN ĐẢNG HUẤN LUYỆN", [9, "huấn"]))),
    sc("counter", 10, bg="khunsa1974", **{"from": 0, "to": 16}, suffix=" TUỔI", countAt=[10, "mười"], label="ĐÃ CÓ BĂNG NHÓM RIÊNG"),
    sc("kinetic", 11, bg="burma1953", items=kin(("VÀI TRĂM NGƯỜI", [11, "vài"]), ("ĐỔI PHE LIÊN TỤC", [11, "đổi"], "acc"))),
    sc("split", 12, title="HÔM NAY · NGÀY MAI", a={"img": "burma1954", "label": "THEO CHÍNH PHỦ", "at": [12, "chính"]}, b={"img": "ssa_south", "label": "THEO QUÂN NỔI DẬY", "at": [12, "nổi"]}),
    sc("date", 13, bg="taunggyi", day="ĐỀ NGHỊ CỦA CHÍNH PHỦ MIẾN ĐIỆN", date="1963"),
    sc("file", 14, k="THỎA THUẬN · 1963", name="DÂN QUÂN\nTỰ VỆ", desc="Đánh quân nổi dậy bang Shan", bg="taunggyi",
       rows=[{"k": "ĐỔI LẠI", "v": "Dùng *đất và đường* của nhà nước", "at": [15, "đất"]}, {"k": "ĐỂ", "v": "*Trồng và buôn thuốc phiện*", "at": [15, "buôn"]}]),
    sc("kinetic", 16, bg="taunggyi", items=kin(("DÂN QUÂN TỰ NUÔI MÌNH", [16, "tự"]), ("KHÔNG TỐN NGÂN SÁCH", [16, "ngân"], "acc"))),
    sc("kinetic", 17, vid="6197173", tone="noir", items=kin(("TIỀN THUỐC PHIỆN", [17, "tiền"]), ("→ VŨ KHÍ CHỢ ĐEN LÀO, THÁI", [17, "chợ"], "acc"))),
    sc("slam", 18, bg="mta_recruits", text="TRANG BỊ TỐT HƠN\nQUÂN CHÍNH PHỦ", hitAt=[18, "tốt"]),
    sc("print", 19, img="khunsa_9", tone="bw", side={"k": "CUỐI THẬP NIÊN 1960", "h": "TRƯƠNG KỲ PHU", "hAt": [19, "Trương"],
       "lines": [{"text": "Một trong những thủ lĩnh dân quân *mạnh nhất*", "at": [19, "mạnh"]}]}),
    sc("map", 20, geo="gt", pins=[{"name": "Loi Maw", "label": "ĐÈO LOI MAW", "at": [20, "Loi"]}], zoom="Loi Maw", zoomK=1.35),
    sc("split", 21, title="HAI MẶT", a={"img": "burma1954", "label": "NGOÀI: PHỤC VỤ CHÍNH PHỦ", "at": [21, "Ngoài"]}, b={"img": "li_mi", "label": "TRONG: TÌNH BÁO QUỐC DÂN ĐẢNG", "at": [21, "tình"]}),
    sc("question", 22, bg="mekong_pano", text="Tại sao phải nộp thuế\ncho tàn quân Quốc Dân Đảng?"),
])

CH["ch06"] = dict(hud={"k": "CHƯƠNG 06", "t": "MƯỜI SÁU TẤN"}, bgm={"file": "impact_lento.mp3", "at": 0, "gain": 0.12}, scenes=[
    chapter("6", "CHƯƠNG SÁU", "MƯỜI SÁU TẤN", "TRẬN CHIẾN THUỐC PHIỆN · 1967", "Mười", vid="6900893", tone="noir"),
    sc("file", 1, k="TUYÊN BỐ · 2.1967", name="THU THUẾ\nQUÁ CẢNH", desc="Trương Kỳ Phu đòi thuế với thuốc phiện Quốc Dân Đảng đi qua vùng mình", bg="khunsa1974"),
    sc("slam", 2, bg="khunsa1974", text="LỜI TUYÊN CHIẾN", hitAt=[2, "tuyên"]),
    sc("kinetic", 3, bg="field_fuzhou", items=kin(("MỘT VIỆC TÁO BẠO HƠN", [3, "táo"]))),
    sc("ledger", 4, title="LÔ HÀNG 1967", bg="field_fuzhou", rows=[{"k": "THUỐC PHIỆN", "v": "16 TẤN", "at": [4, "mười"]}, {"k": "LỚN CHƯA TỪNG CÓ", "v": "✓", "at": [4, "chưa"]},
       {"k": "TRỊ GIÁ", "v": "~$500.000", "at": [4, "năm"]}]),
    sc("file", 5, k="NGƯỜI MUA", name="TƯỚNG OUANE\nRATTIKONE", desc="Chỉ huy quân đội Hoàng gia Lào vùng tây bắc", bg="t28_laos",
       rows=[{"k": "CƠ SỞ", "v": "Xưởng tinh chế ở *Ban Khwan*", "at": [6, "Ban"]}]),
    sc("kinetic", 7, bg="mta_recruits", items=kin(("NẾU LÔ HÀNG ĐẾN NƠI", [7, "lô"], "sm"), ("+1.000 TAY SÚNG", [7, "nghìn"]), ("NGANG NGỬA QUỐC DÂN ĐẢNG", [7, "ngang"], "acc"))),
    sc("slam", 8, bg="mekong_pano", text="KHÔNG NỘP\nMỘT ĐỒNG THUẾ", hitAt=[8, "nộp"]),
    sc("sketch", 9, art="convoy", title="Hàng trăm con la · 800 tay súng · 300 km đường núi"),
    sc("broll", 10, vid="18308549", tone="noir", veil=0.4, illus=FILMV, kin=kin(("MẠNG LƯỚI VÔ TUYẾN", [10, "vô"]), ("THEO DÕI TỪNG BƯỚC", [10, "từng"], "acc"))),
    sc("counter", 11, vid="9733917", tone="noir", **{"from": 0, "to": 1000}, countAt=[11, "bảy"], label="QUÂN QUỐC DÂN ĐẢNG BÁM THEO"),
    sc("map", 12, geo="gt", pins=[{"name": "Tam Giác Vàng", "label": "BAN KHWAN · BỜ SÔNG PHÍA LÀO", "at": [12, "Ban"]}], zoom="Tam Giác Vàng", zoomK=1.6),
    sc("photo", 13, img="sat_confluence", tone="color", move="in", kin=kin(("QUỐC DÂN ĐẢNG ĐUỔI TỚI", [13, "đuổi"]))),
    sc("counter", 14, bg="mekong_pano", **{"from": 0, "to": 250000}, prefix="$", countAt=[14, "hai"], label="GIÁ ĐỂ RÚT ĐI"),
    sc("date", 15, vid="6900893", tone="noir", day="KHÔNG AI CHỊU · NỔ SÚNG", date="29.07.1967"),
    sc("photo", 16, img="t28_line", tone="color", move="in", kin=kin(("TRƯA 30.07 · SÁU CHIẾC T-28", [16, "T-28"]), ("KHÔNG QUÂN HOÀNG GIA LÀO", [16, "Hoàng"], "acc"))),
    sc("counter", 17, bg="t28_damaged", **{"from": 0, "to": 5}, suffix=" LƯỢT / NGÀY", countAt=[17, "bốn,"], label="NÉM BOM LIÊN TỤC HAI NGÀY"),
    sc("slam", 18, bg="t28_damaged", text="CẢ HAI PHE\nNGƯỜI · LA · TẤT CẢ", hitAt=[18, "hai"]),
    sc("ledger", 19, title="VÒNG VÂY CỦA TƯỚNG OUANE", rows=[{"k": "PHÍA NAM", "v": "QUÂN DÙ", "at": [19, "dù"]}, {"k": "PHÍA BẮC", "v": "BỘ BINH", "at": [19, "bộ"]},
       {"k": "TRÊN SÔNG", "v": "TÀU TUẦN TRA", "at": [19, "tàu"]}]),
    sc("ledger", 20, title="THƯƠNG VONG", rows=[{"k": "PHE TRƯƠNG KỲ PHU", "v": "82 NGƯỜI", "at": [20, "tám"]}, {"k": "QUỐC DÂN ĐẢNG", "v": "70 NGƯỜI", "at": [21, "bảy"]}],
       total={"k": "QUỐC DÂN ĐẢNG", "v": "BỊ VÂY 2 TUẦN", "at": [21, "bao"]}),
    sc("slam", 22, bg="t28_laos", text="NGƯỜI THẮNG DUY NHẤT", white=True, hitAt=[22, "thắng"], sub="TƯỚNG OUANE RATTIKONE"),
    sc("kinetic", 23, bg="field_fuzhou", items=kin(("GOM HẾT THUỐC PHIỆN", [23, "gom"]), ("MIỄN PHÍ", [23, "Miễn"], "acc"))),
    sc("photo", 24, img="patna", tone="sepia", move="in", illus="TRANH MINH HỌA · XƯỞNG THUỐC PHIỆN PATNA, ẤN ĐỘ, THẾ KỶ 19",
       kin=kin(("HAI NĂM SAU", [24, "Hai"]), ("HEROIN SỐ 4", [24, "số"], "acc"))),
    sc("map", 25, geo="asia", pins=[{"name": "Tam Giác Vàng", "at": [25, "vượt"]}, {"name": "Hồng Kông", "label": "→ MỸ · CHÂU ÂU", "at": [25, "Mỹ,"]}],
       routes=[{"from": "Tam Giác Vàng", "to": "Hồng Kông", "at": [25, "châu"], "until": [25, "Âu."], "bend": 0.15}]),
    sc("photo", 26, img="vn_patrol", tone="bw", move="in", film=True, kin=kin(("KHÁCH HÀNG", [26, "khách"], "sm"), ("LÍNH MỸ Ở VIỆT NAM", [26, "Việt"], "acc"))),
    sc("slam", 27, bg="khunsa1974", text="MẤT TRẮNG", hitAt=[27, "trắng."]),
    sc("counter", 28, bg="mta_recruits", **{"from": 0, "to": 50}, prefix="> ", suffix="%", countAt=[28, "nửa"], label="QUÂN BỎ ĐI · CUỐI 1968"),
    sc("kinetic", 29, bg="khunsa1974", items=kin(("ĐỜI ANH TA ĐÃ HẾT?", [29, "hết."], "serif"))),
    sc("broll", 30, vid="5266812", tone="noir", veil=0.4, illus=FILMV, kin=kin(("THẾ GIỚI BẮT ĐẦU CHÚ Ý", [30, "chú"]), ("NHỜ PHIM ẢNH", [30, "phim"], "acc"))),
])

if __name__ == "__main__":
    spec = json.loads((D / "spec.json").read_text(encoding="utf-8"))
    spec["imgs"], spec["geo"] = IMGS, GEO
    (D / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    import importlib.util
    extra = D / "gen_scenes2.py"
    if extra.exists():
        sys.modules["gen_scenes"] = sys.modules[__name__]
        s2 = importlib.util.spec_from_file_location("g2", extra)
        m = importlib.util.module_from_spec(s2)
        s2.loader.exec_module(m)
        CH.update(m.CH)
    for name, v in CH.items():
        f = D / f"{name}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        d.update(v)
        for x in d["scenes"]:   # con dấu trên thẻ giấy: screen blend làm nhạt màu đỏ -> dùng mực (multiply)
            if x["type"] == "file" and x.get("stamp"):
                x["stamp"].setdefault("ink", True)
                if not x.get("img"):   # thẻ không ảnh nằm ở x 460–1460: giữ con dấu trong thẻ
                    x["stamp"].setdefault("x", 960); x["stamp"].setdefault("y", 600)
                if not x.get("img"):   # thẻ không ảnh nằm ở x 460–1460: giữ con dấu trong thẻ
                    x["stamp"].setdefault("x", 960); x["stamp"].setdefault("y", 600)
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(name, len(d["lines"]), "câu", len(d["scenes"]), "cảnh")
