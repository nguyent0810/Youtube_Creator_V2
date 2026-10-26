"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM "KẺ HỦY DIỆT ngoài đời thật: Stanislav Petrov, đêm 26/9/1983".

    python data/long/mim-ke-huy-diet-petrov/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md và factcheck.md. Pha 1: chỉ viết file; chưa dựng, chưa tải ảnh/clip. imgs ghi tên File: Commons, giấy phép
đã đọc qua Commons API (extmetadata LicenseShortName) ngày 23/10/2026, phải đọc lại ở pha 2 trước khi tải.
Không dùng ảnh chân dung Petrov (mọi ảnh chân dung trên Commons là CC BY-SA, MIM không nhận). Không có hình phim Kẻ Hủy Diệt: phim chỉ
được nhắc bằng lời và chữ. Clip Pexels (vid) chỉ là B-roll trung tính, chọn từ `pexels.py search` (chưa tải; pha 2 chạy `get` rồi
`motion/long/clip_sheet.py` để soát logo/chữ).
Lộ trình dạng "bạn ngồi vào ghế trực": bảng ledger "GHẾ TRỰC · BẠN ĐANG CÓ" thêm đúng một dòng ở CH01, CH02, CH03, CH04, CH06, CH07;
cảnh question "BÁO LÊN | CHƯA" ở cuối CH00–CH07 (CH05 là ghế phía Mỹ); CH08 mới kể quyết định của Petrov.
Mọi neo [dòng, "từ"] chỉ dùng chữ nằm trong lời đọc; không neo vào chữ số hay chữ có trong bảng "say".
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"petrov": "Pê-trốp", "stanislav": "Xta-nít-xláp", "serpukhov-15": "Xéc-pu-khốp mười lăm", "serpukhov": "Xéc-pu-khốp",
       "oko": "Ô-cô", "pavel": "Pa-ven", "podvig": "Pốt-vích", "bbc": "bi bi xi", "guardian": "Gác-điần", "minuteman": "Mi-nít-men",
       "korean": "Cô-ri-ần", "air": "e", "lines": "lai", "ronald": "Rô-nân", "reagan": "Rây-gần", "yuri": "I-u-ri",
       "andropov": "An-đrô-pốp", "mikhail": "Mi-kha-in", "gorbachev": "Goóc-ba-chốp", "kgb": "ca giê bê", "nato": "Na-tô",
       "vryan": "vê-ri-an", "norad": "Nô-rát", "cheyenne": "Sai-en", "colorado": "Cô-lô-ra-đô", "washington": "Oa-sinh-tơn",
       "robert": "Rô-bớt", "gates": "Ghết", "zbigniew": "Dơ-bích-niêu", "brzezinski": "Bơ-dê-din-xki", "jimmy": "Gim-mi",
       "carter": "Các-tơ", "marshall": "Mác-san", "shulman": "Sun-man", "leonid": "Lê-ô-nít", "brezhnev": "Brê-giơ-nhép",
       "harold": "He-rôn", "brown": "Brao", "gary": "Ghe-ri", "hart": "Hát", "barry": "Be-ri", "goldwater": "Gôn-oa-tơ",
       "christian": "Cri-xchần", "science": "Xai-ần", "monitor": "Mo-ni-tơ", "scott": "Xcốt", "sagan": "Xây-gần",
       "stanford": "Xten-phợt", "kiev": "Ki-ép", "votintsev": "Vô-tin-xép", "vodka": "vốt-ca", "able": "Ây-bồn", "archer": "A-chơ",
       "leonard": "Lê-ô-nợt", "perroots": "Pe-rút", "skynet": "Xcai-nét", "warsaw": "Vác-sa-va", "dresden": "Đrét-đần",
       "fryazino": "Phri-a-di-nô", "der": "Đe", "spiegel": "Spi-gần", "new": "Niu", "york": "Oóc", "=AI": "ây ai",
       "radar": "ra-đa", "micro": "mi-crô", "apollo": "A-pô-lô"}
VM = "ẢNH MINH HỌA"
VV = "VIDEO MINH HỌA"
CH = {}

IMGS = {
    "serp": "File:NASA FIRMS 2025-07-20 Serpukhov-15.png",                                                        # Public domain (NASA LANCE FIRMS; ảnh vệ tinh 2025, địa hình cũ hơn)
    "mm3": "File:Minuteman III ICBM operational test launch (6530663).jpg",                                       # Public domain (U.S. Space Force, 24/02/2021)
    "mmsilo": "File:Minuteman II in silo 1980.jpg",                                                              # Public domain (ảnh Không quân Mỹ)
    "norad84": "File:The command Post of the North American Air Defense Command (NORAD) Cheyenne Mountain Complex DF-ST-84-06737.jpg",  # Public domain (Staff Sgt. Bob Simons, DoD)
    "cheyenne68": "File:Cheyenne Mountain NORAD entrance 1968.jpg",                                              # Public domain
    "molniya": "File:NASA molniya oblique.png",                                                                  # Public domain (NASA; sơ đồ quỹ đạo Molniya)
    "dsp": "File:DSP Phase3.jpg",                                                                                # Public domain (USAF; tranh vệ tinh DSP của Mỹ)
    "brown": "File:Harold Brown photo portrait standing.jpg",                                                    # Public domain (chân dung chính thức Bộ Quốc phòng Mỹ)
    "reagan": "File:Official Portrait of President Ronald Reagan on The Oval Office Patio (cropped).jpg",        # Public domain (Nhà Trắng, 06/06/1983)
    "e4b": "File:Boeing E-4B USAF 73-1677.jpg",                                                                  # Public domain (USAF)
    "namerica": "File:North America from low orbiting satellite Suomi NPP.jpg",                                  # Public domain (NASA/NOAA/GSFC/Suomi NPP, 2012)
    "glint": "File:ISS-31 Sunglint and clouds off Western South America.jpg",                                    # Public domain (NASA, ISS Expedition 31, 2012)
    "clouds": "File:ISS-48 Towering cumulonimbus and other clouds over the Earth (3).jpg",                       # Public domain (NASA, ISS Expedition 48, 2016)
    "memorial": "File:Stanislav Petrov memorial stone.jpg",                                                      # Public domain (Brandmeister / Togrul Safarov, 2021)
    "warsaw": "File:2023 Warszawa Ogród Sprawiedliwych, Stanisław Jewgrafowicz Pietrow.jpg",                     # CC0 (Cybularny, 2023)
}

BTN = "BÁO LÊN   |   CHƯA"
# Dòng của bảng "GHẾ TRỰC · BẠN ĐANG CÓ" (mỗi chương thêm đúng một dòng)
R = [{"k": "1 · MÀN HÌNH", "v": "1 VỤ PHÓNG · TIN CẬY TỐI ĐA"},
     {"k": "2 · CON MẮT", "v": "OKO MỚI · TỪNG HỎNG NHIỀU"},
     {"k": "3 · SỐ LƯỢNG", "v": "5 (BẢN 2004: 4) · 1 CĂN CỨ"},
     {"k": "4 · BỐI CẢNH", "v": "LÃNH ĐẠO TIN MỸ SẮP RA TAY"},
     {"k": "5 · PHÍA MỸ", "v": "TỪNG NHẦM · CẦN MẮT THỨ 2"},
     {"k": "6 · MẮT THỨ 2", "v": "KHÔNG THẤY · VỐN HAY THẾ"}]


def seat(n, at_old, at_new, note, total=None):
    """Bảng ghế trực: n-1 dòng cũ hiện ngay ở at_old, dòng thứ n hiện ở at_new."""
    rows = [dict(r, at=at_old) for r in R[:n - 1]] + [dict(R[n - 1], at=at_new)]
    s = {"type": "ledger", "at": at_old, "title": "GHẾ TRỰC · BẠN ĐANG CÓ", "srcnote": note, "rows": rows}
    if total:
        s["total"] = total
    return s


# ---------------------------------------------------------------- CH00: chữ "phóng" trên màn hình đỏ (cold open)
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "CHỮ “PHÓNG” TRÊN MÀN HÌNH ĐỎ"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "at": 0, "vid": "5004222", "veil": 0.55, "illus": VV,
     "kin": [{"text": "KẺ HỦY DIỆT · 1984", "at": 0, "acc": True},
             {"text": "mạng máy tính quốc phòng tự châm ngòi chiến tranh hạt nhân", "at": [0, "mạng"], "sm": True}]},
    {"type": "kinetic", "at": 1, "items": [{"text": "MỘT NĂM TRƯỚC ĐÓ", "at": 1, "sm": True},
                                           {"text": "NGOÀI ĐỜI THẬT", "at": [1, "ngoài"], "acc": True}]},
    {"type": "date", "at": 2, "day": "TRUNG TÂM CẢNH BÁO SỚM · LIÊN XÔ", "date": "26.09.1983",
     "sub": {"text": "ĐÊM 25 RẠNG SÁNG 26", "at": [2, "rạng"]}},
    {"type": "print", "at": 3, "img": "serp", "tone": "color", "illus": "ẢNH VỆ TINH NASA FIRMS 2025 · ĐỊA HÌNH CŨ HƠN",
     "side": {"k": "SERPUKHOV-15", "h": "≈ 70 KM\nTÂY NAM MÁT-XCƠ-VA",
              "lines": [{"text": "gần làng Kurilovo, tỉnh Kaluga · Podvig 2002", "at": [3, "tây"]}]}},
    {"type": "slam", "at": 4, "text": "SERPUKHOV-15", "sub": "TRẠM ĐIỀU KHIỂN VỆ TINH CẢNH BÁO SỚM · PODVIG 2002"},
    {"type": "ledger", "at": 5, "title": "NGƯỜI NGỒI GHẾ TRỰC ĐÊM NAY", "srcnote": "BBC 2013 · GUARDIAN 2017 · KHÔNG DÙNG ẢNH CHÂN DUNG",
     "rows": [{"k": "CẤP BẬC", "v": "TRUNG TÁ PHÒNG KHÔNG", "at": [5, "trung"]},
              {"k": "TÊN", "v": "STANISLAV PETROV", "at": [5, "trung"]},
              {"k": "TUỔI", "v": "44 (SINH 09.09.1939)", "at": [5, "tuổi"]}]},
    {"type": "broll", "at": 6, "vid": "14904107", "veil": 0.5, "illus": VV,
     "kin": [{"text": "CÒI BÁO ĐỘNG", "at": [6, "còi"], "acc": True}]},
    {"type": "slam", "at": 7, "text": "СТАРТ", "sub": "TIẾNG NGA: “PHÓNG” · MOSKOVSKIYE NOVOSTI 2004 · BBC: “LAUNCH”"},
    {"type": "photo", "at": 8, "img": "mm3", "tone": "bw", "move": "in", "veil": 0.55, "illus": VM,
     "kin": [{"text": "MÁY BÁO: MỸ VỪA PHÓNG MỘT TÊN LỬA", "at": [8, "báo"], "acc": True}],
     "label": {"k": "MINUTEMAN III PHÓNG THỬ · 2021", "v": "ẢNH: LỰC LƯỢNG VŨ TRỤ MỸ", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "30 NĂM SAU", "at": 9, "acc": True}, {"text": "kể với BBC tiếng Nga · 2013", "at": [9, "kể"], "sm": True}]},
    {"type": "quote", "at": 10, "text": "The siren howled, but I just sat there for a few seconds, staring at the big, back-lit, red screen with the word ‘launch’ on it.",
     "by": "STANISLAV PETROV · BBC NEWS · 26.09.2013", "lbl": "TRÍCH DỊCH", "qline": 10, "typeAt": [10, "còi"]},
    {"type": "kinetic", "at": 11, "items": [{"text": "MÌNH MỜI BẠN", "at": 11, "sm": True},
                                            {"text": "NGỒI VÀO GHẾ TRỰC", "at": [12, "ngồi"], "acc": True}]},
    {"type": "ledger", "at": 13, "title": "GHẾ TRỰC · LUẬT CHƠI", "srcnote": "MỖI CHƯƠNG THÊM MỘT DÒNG",
     "rows": [{"k": "MỖI CHƯƠNG", "v": "THÊM ĐÚNG 1 MẨU TIN ÔNG CÓ", "at": 13},
              {"k": "HOẶC", "v": "ĐỔI SANG GHẾ PHÍA MỸ", "at": [13, "đổi"]},
              {"k": "CUỐI CHƯƠNG", "v": "BẠN CHỌN: BÁO LÊN | CHƯA", "at": 14}],
     "total": {"k": "SAU ĐÓ", "v": "MỚI KỂ ÔNG ĐÃ LÀM GÌ", "at": 15}},
    {"type": "question", "at": 16, "text": "Còi vẫn đang hú.\n" + BTN},
]}

# ---------------------------------------------------------------- CH01: chiếc ghế bạn vừa ngồi
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CHIẾC GHẾ BẠN VỪA NGỒI"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CHIẾC GHẾ\nBẠN VỪA NGỒI", "sub": "VIỆC CỦA NGƯỜI TRỰC", "vid": "11533575", "illus": VV,
     "titleAt": [0, "trước"]},
    {"type": "ledger", "at": 1, "title": "VIỆC CỦA NGƯỜI TRỰC", "srcnote": "BBC NEWS · 26.09.2013",
     "rows": [{"k": "1", "v": "GHI NHẬN MỌI VỤ PHÓNG CỦA ĐỊCH", "at": [1, "ghi"]},
              {"k": "2", "v": "BÁO NGAY QUÂN ĐỘI + LÃNH ĐẠO", "at": 2}],
     "total": {"k": "KHÔNG GIỮ", "v": "NÚT BẮN", "at": 3}},
    {"type": "kinetic", "at": 4, "items": [{"text": "MỌI THỨ PHÍA SAU", "at": 4, "sm": True},
                                           {"text": "BẮT ĐẦU TỪ MỘT CÚ ĐIỆN THOẠI", "at": [4, "cú"], "acc": True}]},
    {"type": "broll", "at": 5, "vid": "8870090", "veil": 0.55, "illus": VV,
     "kin": [{"text": "MOSKOVSKIYE NOVOSTI · 27.04.2004", "at": 5, "sm": True},
             {"text": "PETROV GIẢI THÍCH", "at": [5, "giải"], "acc": True}]},
    {"type": "quote", "at": 6, "text": "Мы давали руководству страны дополнительное время для размышлений — 10–12 минут.",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004 · BẢN ĐĂNG LẠI FLB.RU", "lbl": "TRÍCH DỊCH", "qline": 6, "typeAt": [6, "chúng"]},
    {"type": "quote", "at": 7, "text": "Остальные 15 минут уже думать поздно. Надо отдавать приказ ракетам…",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004", "lbl": "TRÍCH DỊCH", "qline": 7, "typeAt": [7, "mười"]},
    {"type": "source", "at": 8, "source": "PFIAB · “THE SOVIET ‘WAR SCARE’” · 15.02.1990", "ref": "BAN CỐ VẤN TÌNH BÁO CỦA TỔNG THỐNG MỸ · GIẢI MẬT 2015",
     "snippet": "…the comprehensive coverage of US ICBM fields by [[launch-detection satellites in 1983]] significantly increased warning time…",
     "hlAt": 10, "seal": "TÀI LIỆU GỐC · NATIONAL SECURITY ARCHIVE", "sealAt": [9, "giải"]},
    {"type": "bars", "at": 11, "title": "THỜI GIAN CẢNH BÁO TÊN LỬA MỸ BẮN VÀO LIÊN XÔ", "unit": "PHÚT · PFIAB 1990", "max": 35,
     "items": [{"k": "CÓ VỆ TINH (1983)", "v": 30, "lbl": "≈ 30", "at": [11, "ba"], "acc": True},
               {"k": "CHỈ RADAR (TRƯỚC ĐẦU 1980)", "v": 13, "lbl": "≈ 13", "at": [12, "mười"]}]},
    {"type": "slam", "at": 13, "text": "CHIẾC GHẾ CÒN MỚI", "sub": "VỆ TINH PHỦ KÍN CÁC BÃI TÊN LỬA MỸ TỪ NĂM 1983"},
    {"type": "kinetic", "at": 14, "items": [{"text": "KHÔNG PHẢI NGƯỜI TRỰC THƯỜNG XUYÊN", "at": 14, "acc": True},
                                            {"text": "chuyên viên phân tích · vài lần mỗi tháng · bản 2004", "at": 15, "sm": True},
                                            {"text": "CHÍNH ÔNG VIẾT BẢN HƯỚNG DẪN", "at": 17}]},
    {"type": "ledger", "at": 18, "title": "HỌC VẤN · HAI BẢN KỂ", "srcnote": "BBC 2013 · GUARDIAN 2017",
     "rows": [{"k": "BBC 2013", "v": "HỌC DÂN SỰ · ĐỒNG ĐỘI LÀ LÍNH", "at": 18},
              {"k": "GUARDIAN 2017", "v": "TRƯỜNG KHÔNG QUÂN KIEV", "at": 21}],
     "total": {"k": "KÊNH", "v": "ĐỂ NGUYÊN CẢ HAI", "at": 22}},
    seat(1, 24, 25, "MẨU TIN 1 / 6 · BBC 2013",
         total={"k": "THỜI GIAN NGHĨ", "v": "KHÔNG CÓ QUY ĐỊNH", "at": 27}),
    {"type": "kinetic", "at": 28, "items": [{"text": "MỖI GIÂY CHẦN CHỪ", "at": [28, "mỗi"], "acc": True},
                                            {"text": "là lấy đi thời gian của lãnh đạo · BBC", "at": [28, "lấy"], "sm": True}]},
    {"type": "question", "at": 29, "text": "Một tên lửa, tin cậy cao nhất.\n" + BTN},
]}

# ---------------------------------------------------------------- CH02: con mắt trên quỹ đạo
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "CON MẮT TRÊN QUỸ ĐẠO"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "CON MẮT\nTRÊN QUỸ ĐẠO", "sub": "HỆ THỐNG VỆ TINH OKO", "bg": "namerica",
     "titleAt": [0, "chưa"]},
    {"type": "ledger", "at": 1, "title": "KIỂM TRA THEO BẢN HƯỚNG DẪN", "srcnote": "MOSKOVSKIYE NOVOSTI 2004 · BBC 2013",
     "rows": [{"k": "BẢN HƯỚNG DẪN", "v": "CỦA CHÍNH PETROV", "at": [1, "bản"]},
              {"k": "BẢN 2004", "v": "30 TẦNG KIỂM TRA", "at": [2, "tầng"]},
              {"k": "KẾT QUẢ", "v": "MỌI THỨ KHỚP", "at": 3},
              {"k": "BẢN BBC 2013", "v": "28 HAY 29 TẦNG", "at": [4, "tám"]}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "CHÊNH LỆCH NHỎ", "at": 5, "sm": True}, {"text": "VẪN NÓI RA", "at": [6, "nói"], "acc": True},
                                           {"text": "cả câu chuyện đi qua trí nhớ của một người", "at": 7, "sm": True}]},
    {"type": "slam", "at": 9, "text": "OKO", "sub": "TIẾNG NGA: “CON MẮT” · HỆ THỐNG VỆ TINH CẢNH BÁO SỚM US-KS"},
    {"type": "source", "at": 10, "source": "P. PODVIG · SCIENCE & GLOBAL SECURITY 10 (2002)", "ref": "“HISTORY AND THE CURRENT STATUS OF THE RUSSIAN EARLY-WARNING SYSTEM”",
     "snippet": "Two main components of this system are considered — the network of early-warning radars, and [[the space-based early-warning system]]…",
     "hlAt": [10, "mô"], "seal": "BÀI BÁO KHOA HỌC · TR. 21–60", "sealAt": [10, "khoa"]},
    {"type": "print", "at": 11, "img": "molniya", "tone": "color", "illus": "SƠ ĐỒ MINH HỌA · NASA",
     "side": {"k": "QUỸ ĐẠO ELIP CAO", "h": "≈ 39.700 KM\n↔ ≈ 600 KM",
              "lines": [{"text": "điểm xa nhất · điểm gần nhất · Podvig 2002", "at": 12},
                        {"text": "nghiêng ≈ 63° · chu kỳ ≈ 718 phút → đúng 2 vòng mỗi ngày", "at": 14}]}},
    {"type": "kinetic", "at": 15, "items": [{"text": "ĐIỀU LẠ: GÓC NHÌN", "at": 15, "acc": True},
                                            {"text": "không nhìn thẳng xuống nước Mỹ", "at": 16, "sm": True},
                                            {"text": "NHÌN XIÊN · SÁT MÉP TRÁI ĐẤT", "at": [17, "xiên"]}]},
    {"type": "photo", "at": 18, "img": "clouds", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "LỬA TÊN LỬA TRÊN NỀN VŨ TRỤ TỐI", "at": [18, "luồng"], "acc": True},
             {"text": "góc ngẩng dưới ≈ 12° · Podvig 2002", "at": [18, "chứ"], "sm": True}],
     "label": {"k": "TRÁI ĐẤT VÀ MÂY NHÌN TỪ QUỸ ĐẠO", "v": "ẢNH NASA · ISS 2016", "at": 18}},
    {"type": "kinetic", "at": 19, "items": [{"text": "CẢM BIẾN ĐƠN GIẢN HƠN CỦA MỸ", "at": [19, "cảm"]},
                                            {"text": "NHƯNG NÓ CÓ GIÁ", "at": 20, "acc": True}]},
    {"type": "ledger", "at": 21, "title": "CÁI GIÁ CỦA GÓC NHÌN XIÊN", "srcnote": "PODVIG 2002 · TR. 42–45",
     "rows": [{"k": "MỖI VỆ TINH", "v": "≈ 6 GIỜ/NGÀY Ở ĐÚNG CHỖ", "at": 21},
              {"k": "CANH 24 GIỜ", "v": "ÍT NHẤT 4 CHIẾC", "at": 22},
              {"k": "THIẾT KẾ", "v": "TỚI 9 VỆ TINH · 9 QUỸ ĐẠO", "at": 23}]},
    {"type": "photo", "at": 24, "img": "glint", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "ÁNH NẮNG TRỰC TIẾP", "at": [25, "trực"], "sm": True},
             {"text": "ÁNH PHẢN CHIẾU TỪ MÂY", "at": [25, "phản"], "acc": True}],
     "label": {"k": "ÁNH NẮNG PHẢN CHIẾU VÀ MÂY, NHÌN TỪ ISS", "v": "ẢNH NASA · 2012", "at": 24}},
    {"type": "slam", "at": 26, "text": "MÂY", "sub": "HÃY NHỚ CHỮ NÀY"},
    {"type": "timeline", "at": 28, "bg": "clouds", "items": [{"year": "1978", "text": "Oko *chạy hạn chế*", "at": 28},
                                            {"year": "1982", "text": "*trực chiến*", "at": [28, "trực"]},
                                            {"year": "09.1983", "text": "đêm ở Serpukhov · *mới trực chiến chừng một năm*", "at": 29}]},
    {"type": "bars", "at": 30, "title": "13 VỆ TINH OKO ĐẦU TIÊN · 1972–1979", "unit": "PODVIG 2002 · TR. 41", "max": 14,
     "items": [{"k": "ĐÃ PHÓNG", "v": 13, "lbl": "13", "at": [30, "mười"]},
               {"k": "CHẠY QUÁ 100 NGÀY", "v": 7, "lbl": "7", "at": [30, "bảy"], "acc": True}]},
    {"type": "counter", "at": 31, "from": 0, "to": 11, "suffix": " / 31", "until": [33, "mốt"], "label": "VỆ TINH TỰ HUỶ VÌ MẤT LIÊN LẠC",
     "sub": {"text": "TỚI KHI GỠ BỘ TỰ HUỶ NĂM 1983 · PODVIG 2002", "at": 32}},
    seat(2, 34, 35, "MẨU TIN 2 / 6 · PODVIG 2002",
         total={"k": "ĐÊM NAY", "v": "QUA MỌI TẦNG KIỂM TRA", "at": 36}),
    {"type": "question", "at": 37, "text": "Bạn có nhấc máy báo lên không?\n" + BTN},
]}

# ---------------------------------------------------------------- CH03: một, rồi năm
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "MỘT, RỒI NĂM"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "MỘT,\nRỒI NĂM", "sub": "“PHÓNG” → “TẤN CÔNG TÊN LỬA”", "bg": "mmsilo",
     "titleAt": [0, "theo"]},
    {"type": "quote", "at": 1, "text": "A minute later the siren went off again. The second missile was launched. Then the third, and the fourth, and the fifth.",
     "by": "STANISLAV PETROV · BBC NEWS · 2013", "lbl": "TRÍCH DỊCH", "qline": 1, "typeAt": [1, "một"]},
    {"type": "kinetic", "at": 2, "items": [{"text": "PHÓNG", "at": 2, "sm": True},
                                           {"text": "TẤN CÔNG TÊN LỬA", "at": [2, "tấn"], "acc": True},
                                           {"text": "chữ trên bảng đổi · còi rú to hơn · bản 2004", "at": 3, "sm": True}]},
    {"type": "ledger", "at": 4, "title": "SỐ TÊN LỬA · CÁC BẢN KỂ", "srcnote": "MOSKOVSKIYE NOVOSTI 2004 · BBC 2013 · GUARDIAN 2017",
     "rows": [{"k": "BẢN 2004", "v": "THỨ 2, THỨ 3, THỨ 4 → 4 TÊN LỬA", "at": 5},
              {"k": "BBC 2013", "v": "ĐẾN THỨ 5 → 5 TÊN LỬA", "at": 7},
              {"k": "GUARDIAN 2017", "v": "5 TÊN LỬA MINUTEMAN", "at": 8}],
     "total": {"k": "NGUỒN CHÍNH", "v": "MỘT NGƯỜI · HAI CON SỐ", "at": 10}},
    {"type": "photo", "at": 11, "img": "mmsilo", "tone": "bw", "move": "in", "veil": 0.55, "illus": VM,
     "kin": [{"text": "TỪ ĐÂY: 5 TÊN LỬA", "at": [11, "dùng"], "acc": True},
             {"text": "bản gần nhất · nhiều báo dẫn lại", "at": [11, "gần"], "sm": True}],
     "label": {"k": "TÊN LỬA MINUTEMAN II TRONG HẦM · 1980", "v": "ẢNH KHÔNG QUÂN MỸ", "at": 11}},
    {"type": "slam", "at": 13, "text": "MỘT CĂN CỨ", "sub": "MỌI VỤ PHÓNG · THEO BẢN 2004"},
    {"type": "quote", "at": 15, "text": "Ракетные нападения с одной базы не начинаются, взлетают со всех сразу.",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004", "lbl": "TRÍCH DỊCH", "qline": 15, "typeAt": [15, "tấn"]},
    {"type": "kinetic", "at": 16, "items": [{"text": "ĐÒN PHỦ ĐẦU PHẢI Ồ ẠT", "at": 16, "acc": True},
                                            {"text": "đủ lớn để đối phương không kịp đáp trả", "at": 17, "sm": True},
                                            {"text": "5 TÊN LỬA LÀ QUÁ ÍT", "at": 18}]},
    {"type": "source", "at": 19, "source": "P. PODVIG · 2002 · PHẦN TÓM TẮT", "ref": "SCIENCE & GLOBAL SECURITY 10:21–60",
     "snippet": "The system appears to be capable of detecting a massive attack, but [[cannot be relied upon to detect individual missile launches]].",
     "hlAt": 21, "seal": "TRÍCH NGUYÊN VĂN · TR. 21", "sealAt": [21, "lẻ"]},
    {"type": "slam", "at": 22, "text": "VỤ PHÓNG LẺ", "sub": "ĐÚNG THỨ OKO KÉM NHẤT"},
    seat(3, 23, 24, "MẨU TIN 3 / 6 · BBC 2013 · BẢN 2004",
         total={"k": "MÀN HÌNH", "v": "“TẤN CÔNG”", "at": [24, "tấn"]}),
    {"type": "question", "at": 25, "text": "Bạn báo lên, hay vẫn chưa?\n" + BTN},
    {"type": "broll", "at": 26, "vid": "5004222", "ms": 8, "veil": 0.55, "illus": VV,
     "kin": [{"text": "NHÌN RA NGOÀI BOONG-KE", "at": 26, "acc": True},
             {"text": "không ai ngồi ghế này trong chân không", "at": 27, "sm": True}]},
]}

# ---------------------------------------------------------------- CH04: mùa thu năm 1983
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "MÙA THU NĂM 1983"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "MÙA THU\nNĂM 1983", "sub": "“CƠN SỢ CHIẾN TRANH”", "vid": "30101621", "illus": VV,
     "titleAt": [0, "ba"]},
    {"type": "date", "at": [0, "quân"], "day": "CHUYẾN BAY KAL 007 BỊ BẮN RƠI", "date": "01.09.1983",
     "sub": {"text": "269 NGƯỜI THIỆT MẠNG · GUARDIAN 2017", "at": 1}},
    {"type": "kinetic", "at": 2, "items": [{"text": "KÊNH ĐÃ CÓ VIDEO RIÊNG", "at": [2, "video"], "sm": True}]},
    {"type": "print", "at": 3, "img": "reagan", "tone": "bw",
     "side": {"k": "TỔNG THỐNG MỸ · 1983", "h": "“ĐẾ QUỐC\nMA QUỶ”", "lines": [{"text": "cách Reagan gọi Liên Xô · Guardian 2017", "at": [3, "gọi"]}]}},
    {"type": "kinetic", "at": 4, "items": [{"text": "ANDROPOV TIN: MỸ ÂM MƯU ĐÁNH BẤT NGỜ", "at": [4, "tin"], "acc": True},
                                           {"text": "theo Guardian 2017", "at": [4, "theo"], "sm": True}]},
    {"type": "source", "at": 5, "source": "PFIAB · “THE SOVIET ‘WAR SCARE’” · 15.02.1990", "ref": "GIẢI MẬT MỘT PHẦN · NATIONAL SECURITY ARCHIVE 24.10.2015",
     "snippet": "Never, perhaps, in the postwar decades has the situation in the world been as [[explosive]] … as in the first half of the 1980’s. — M. Gorbachev, 02.1986",
     "hlAt": 6, "seal": "LỜI ĐỀ TỪ CỦA BÁO CÁO", "sealAt": [6, "mở"]},
    {"type": "quote", "at": 7, "dy": True, "text": "Có lẽ chưa bao giờ sau chiến tranh, tình hình thế giới lại dễ bùng nổ như nửa đầu thập niên 1980.",
     "by": "MIKHAIL GORBACHEV · 02.1986 · QUA BÁO CÁO PFIAB", "lbl": "DIỄN Ý", "qline": 7, "typeAt": [7, None, 0, 0.05], "typeDur": 3.0},
    {"type": "ledger", "at": 8, "title": "“CƠN SỢ CHIẾN TRANH” · PFIAB LIỆT KÊ", "srcnote": "PFIAB 1990 · TÓM TẮT · TR. V",
     "rows": [{"k": "TẬP TRẬN", "v": "LẦN ĐẦU: SỐNG SÓT ĐÒN BẤT NGỜ", "at": 9},
              {"k": "KGB", "v": "YÊU CẦU KHẨN · ƯU TIÊN CAO NHẤT", "at": 10}],
     "total": {"k": "NHIỆM VỤ", "v": "DẤU HIỆU MỸ/NATO SẮP ĐÁNH", "at": 11}},
    {"type": "slam", "at": 12, "text": "VRYAN", "sub": "CHƯƠNG TRÌNH MÁY TÍNH CỦA MỘT ĐƠN VỊ KGB · PFIAB 1990"},
    {"type": "kinetic", "at": 14, "items": [{"text": "ĐO TƯƠNG QUAN LỰC LƯỢNG", "at": 14},
                                            {"text": "CẢNH BÁO KHI ĐÒN PHỦ ĐẦU “CÓ THỂ CHÍNH ĐÁNG”", "at": [15, "cảnh"], "acc": True}]},
    {"type": "broll", "at": 17, "vid": "14904107", "veil": 0.55, "illus": VV,
     "kin": [{"text": "MỘT CỖ MÁY KHÁC ĐANG ĐO NỖI SỢ", "at": 17, "acc": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "“CĂNG GẦN CHẠM TRẦN”", "at": [18, "căng"], "acc": True},
                                            {"text": "Moskovskiye Novosti · 2004", "at": 18, "sm": True},
                                            {"text": "ANDROPOV SUY THẬN · CUỐI THÁNG 9 · PFIAB", "at": 20}]},
    seat(4, 21, 22, "MẨU TIN 4 / 6 · PFIAB 1990 · GUARDIAN 2017",
         total={"k": "CẢNH BÁO", "v": "NGHE RẤT CÓ LÝ", "at": 23}),
    {"type": "question", "at": 24, "text": "Biết bối cảnh ấy,\nbạn báo lên, hay vẫn chờ?\n" + BTN},
    {"type": "broll", "at": 25, "vid": "34742268", "veil": 0.5, "illus": VV,
     "kin": [{"text": "BÊN KIA ĐẠI DƯƠNG", "at": [26, "bên"], "acc": True}]},
]}

# ---------------------------------------------------------------- CH05: ba giờ sáng ở Washington (ghế phía Mỹ)
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "BA GIỜ SÁNG Ở WASHINGTON"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "BA GIỜ SÁNG\nỞ WASHINGTON", "sub": "09.11.1979", "bg": "cheyenne68",
     "titleAt": [0, "ngày"]},
    {"type": "photo", "at": 1, "img": "cheyenne68", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "BỘ CHỈ HUY PHÒNG KHÔNG BẮC MỸ", "at": [1, "bộ"], "acc": True}, {"text": "trong lòng núi · bang Colorado", "at": [1, "lòng"], "sm": True}],
     "label": {"k": "LỐI VÀO NORAD · NÚI CHEYENNE", "v": "1968 · ẢNH CÔNG CỘNG", "at": 1}},
    {"type": "photo", "at": 2, "img": "norad84", "tone": "color", "move": "out", "veil": 0.55, "illus": "ẢNH MINH HỌA · CHỤP NĂM 1984",
     "kin": [{"text": "MÀN HÌNH: LIÊN XÔ TẤN CÔNG TÊN LỬA", "at": [2, "màn"], "acc": True},
             {"text": "cùng lúc ở Bộ chỉ huy Không quân Chiến lược + Trung tâm Chỉ huy Quân sự Quốc gia", "at": 3, "sm": True}],
     "label": {"k": "PHÒNG CHỈ HUY NORAD", "v": "ẢNH BỘ QUỐC PHÒNG MỸ · BOB SIMONS", "at": 2}},
    {"type": "source", "at": 4, "source": "NATIONAL SECURITY ARCHIVE · EBB 371 · 01.03.2012", "ref": "“THE 3 A.M. PHONE CALL: FALSE MISSILE ATTACK WARNING INCIDENTS, 1979–1980”",
     "snippet": "…awakened on 9 November 1979, to be told that [[NORAD … was reporting a Soviet missile attack]].",
     "hlAt": 6, "seal": "HỒ SƠ GIẢI MẬT · DẪN HỒI KÝ R. GATES (1996)", "sealAt": [5, "hồi"]},
    {"type": "counter", "at": 7, "from": 0, "to": 250, "suffix": " TÊN LỬA", "until": [7, "mươi"], "label": "CUỘC GỌI THỨ NHẤT · THEO HỒI KÝ",
     "sub": {"text": "QUA NSA EBB 371", "at": 7}},
    {"type": "slam", "at": 8, "text": "2.200 TÊN LỬA", "sub": "CUỘC GỌI THỨ HAI · “TẤN CÔNG TOÀN DIỆN” · THEO HỒI KÝ"},
    {"type": "kinetic", "at": 9, "items": [{"text": "3–7 PHÚT ĐỂ TỔNG THỐNG QUYẾT ĐỊNH", "at": [9, "quyết"], "acc": True},
                                           {"text": "không đánh thức vợ · theo hồi ký R. Gates", "at": 10, "sm": True},
                                           {"text": "ÔNG ĐỊNH GỌI CARTER", "at": 11}]},
    {"type": "question", "at": 12, "text": "Bạn gọi Tổng thống,\nhay chờ thêm một chút?\n" + BTN},
    {"type": "kinetic", "at": 14, "items": [{"text": "CUỘC GỌI THỨ BA", "at": 14, "sm": True},
                                            {"text": "CÁC HỆ THỐNG KHÁC: KHÔNG THẤY GÌ", "at": 15, "acc": True}]},
    {"type": "slam", "at": 16, "text": "BÁO ĐỘNG GIẢ", "sub": "09.11.1979 · NORAD", "white": True},
    {"type": "photo", "at": 17, "img": "e4b", "tone": "color", "move": "in", "veil": 0.5, "illus": "ẢNH MINH HỌA · CÙNG LOẠI MÁY BAY",
     "kin": [{"text": "10 TIÊM KÍCH ĐÃ CẤT CÁNH", "at": [17, "mười"]},
             {"text": "SỞ CHỈ HUY BAY CẤT CÁNH · KHÔNG CÓ TỔNG THỐNG", "at": [18, "sở"], "acc": True}],
     "label": {"k": "BOEING E-4B · SỞ CHỈ HUY BAY KHẨN CẤP", "v": "ẢNH KHÔNG QUÂN MỸ", "at": 17}},
    {"type": "ledger", "at": 19, "title": "NGUYÊN NHÂN · HAI CÁCH KỂ", "srcnote": "NSA EBB 371 · DẪN SAGAN 1993",
     "rows": [{"k": "BÁO CHÍ 1979", "v": "NẠP NHẦM BĂNG HUẤN LUYỆN", "at": [19, "nạp"]},
              {"k": "GIẢI MẬT", "v": "GIẢ LẬP LỌT LÊN MÀN HÌNH THẬT", "at": 21},
              {"k": "CHỈ HUY NORAD", "v": "KHÔNG TÁI TẠO ĐƯỢC LỖI", "at": 22}]},
    {"type": "kinetic", "at": 23, "items": [{"text": "“KHÔNG HỀ HIẾM”", "at": [23, "hiếm"], "acc": True},
                                            {"text": "Marshall Shulman · Bộ Ngoại giao Mỹ", "at": 23, "sm": True},
                                            {"text": "và xử lý quá dễ dãi", "at": 24, "sm": True}]},
    {"type": "date", "at": 25, "day": "THƯ RIÊNG BREZHNEV GỬI CARTER", "date": "14.11.1979", "sub": {"text": "QUA ĐẠI SỨ DOBRYNIN · NSA EBB 371", "at": 25}},
    {"type": "quote", "at": 26, "text": "…fraught with a tremendous danger.", "by": "L. BREZHNEV · THƯ GỬI J. CARTER · 14.11.1979 · QUA NSA EBB 371",
     "lbl": "TRÍCH DỊCH", "qline": 26, "typeAt": [26, "sự"]},
    {"type": "quote", "at": 27, "text": "I think you will agree with me that there should be no errors in such matters.",
     "by": "L. BREZHNEV · 14.11.1979", "lbl": "TRÍCH DỊCH", "qline": 27, "typeAt": [27, "tôi"]},
    {"type": "slam", "at": 28, "text": "46¢", "sub": "THỦ PHẠM LẦN SAU · 06.1980"},
]}

# ---------------------------------------------------------------- CH06: con chip bốn mươi sáu xu (re-hook)
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "CON CHIP BỐN MƯƠI SÁU XU"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "CON CHIP\nBỐN MƯƠI SÁU XU", "sub": "03.06.1980", "bg": "norad84",
     "titleAt": [0, "ngày"]},
    {"type": "ledger", "at": 1, "title": "BẢN TIN NORAD GỬI CÁC BỘ CHỈ HUY", "srcnote": "NSA EBB 371 · DOD FACT SHEET 06.1980",
     "rows": [{"k": "NGÀY THƯỜNG", "v": "000", "at": 2},
              {"k": "03.06.1980", "v": "002", "at": 4},
              {"k": "RỒI", "v": "200", "at": [4, "rồi"]}],
     "total": {"k": "BẢN TIN BÁO", "v": "200 TÊN LỬA TỪ TÀU NGẦM", "at": 5}},
    {"type": "kinetic", "at": 6, "items": [{"text": "TỔ LÁI RA MÁY BAY NÉM BOM · NỔ MÁY", "at": 7, "acc": True},
                                           {"text": "sở chỉ huy bay lăn tới vị trí cất cánh", "at": 8, "sm": True},
                                           {"text": "RỒI DỪNG LẠI", "at": 9}]},
    {"type": "print", "at": 10, "img": "dsp", "tone": "color", "illus": "TRANH MINH HỌA · KHÔNG QUÂN MỸ",
     "side": {"k": "VỆ TINH CẢNH BÁO DSP CỦA MỸ", "h": "NHỮNG CON MẮT\nĐỘC LẬP", "lines": [{"text": "vệ tinh + radar: không thấy gì bất thường", "at": [11, "thấy"]}]}},
    {"type": "slam", "at": 12, "text": "46¢", "sub": "VI MẠCH HỎNG + THIẾT KẾ BẢN TIN CÓ LỖI · THEO LẦU NĂM GÓC"},
    {"type": "kinetic", "at": 13, "items": [{"text": "06.06.1980 · CHẠY THỬ · LỖI LẶP LẠI", "at": [13, "lặp"]}]},
    {"type": "print", "at": 14, "img": "brown", "tone": "bw",
     "side": {"k": "HAROLD BROWN", "h": "BỘ TRƯỞNG\nQUỐC PHÒNG MỸ", "lines": [{"text": "báo Tổng thống Carter · 06.1980", "at": 14},
                                                                         {"text": "khi thử, không làm con chip hỏng lại được", "at": 15}]}},
    {"type": "date", "at": 16, "day": "BÁO CÁO HART–GOLDWATER GỬI THƯỢNG VIỆN", "date": "10.1980",
     "sub": {"text": "“RECENT FALSE ALERTS FROM THE NATION’S MISSILE ATTACK WARNING SYSTEM”", "at": [16, "báo"]}},
    {"type": "counter", "at": 17, "from": 0, "to": 147, "suffix": " BÁO ĐỘNG GIẢ", "until": [17, "bảy"], "label": "TRONG 18 THÁNG · CS MONITOR 30.10.1980",
     "sub": {"text": "4 LẦN ĐỦ ĐỂ LỰC LƯỢNG CHIẾN LƯỢC BẮT ĐẦU CHUẨN BỊ", "at": 19}},
    {"type": "kinetic", "at": 20, "items": [{"text": "HAROLD BROWN → TỔNG THỐNG CARTER", "at": 20, "sm": True}, {"text": "06.1980", "at": [20, "viết"], "acc": True}]},
    {"type": "quote", "at": 21, "text": "We must be prepared for the possibility that another, unrelated malfunction may someday generate another false alert.",
     "by": "H. BROWN · GỬI TỔNG THỐNG CARTER · 06.1980 · QUA NSA EBB 371", "lbl": "TRÍCH DỊCH", "qline": 21, "typeAt": [21, "chúng"]},
    {"type": "quote", "at": 22, "text": "…we must continue to place our confidence in the human element of our missile attack warning system.",
     "by": "H. BROWN · 06.1980 · QUA NSA EBB 371", "lbl": "TRÍCH DỊCH", "qline": 22, "typeAt": [22, "chúng"]},
    {"type": "kinetic", "at": 23, "items": [{"text": "các nhà báo hỏi Lầu Năm Góc · 1980", "at": 23, "sm": True},
                                            {"text": "“PHẢN ỨNG DÂY CHUYỀN”?", "at": [24, "phản"], "acc": True},
                                            {"text": "“hy vọng họ có hệ thống an toàn như chúng tôi”", "at": 25, "sm": True}]},
    {"type": "broll", "at": 26, "vid": "5004222", "ms": 8, "veil": 0.55, "illus": VV,
     "kin": [{"text": "QUAY LẠI CHIẾC GHẾ", "at": 26, "acc": True},
             {"text": "phía Mỹ: có những con mắt khác nói ngược lại", "at": 27, "sm": True}]},
    {"type": "kinetic", "at": 28, "items": [{"text": "SCOTT SAGAN · ĐẠI HỌC STANFORD", "at": 28, "sm": True},
                                            {"text": "ĐỔ LỖI CHO CON CHIP, CHO MỘT NGƯỜI", "at": [29, "đổ"], "acc": True},
                                            {"text": "thay vì nhìn vào thiết kế cả hệ thống", "at": [29, "thay"], "sm": True}]},
    seat(5, 30, 31, "MẨU TIN 5 / 6 · NSA EBB 371 · CSMONITOR 1980"),
    {"type": "question", "at": 32, "text": "Chờ nguồn tin thứ hai,\nhay báo lên trước?\n" + BTN},
]}

# ---------------------------------------------------------------- CH07: con mắt thứ hai im lặng
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "CON MẮT THỨ HAI IM LẶNG"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "CON MẮT THỨ HAI\nIM LẶNG", "sub": "KÊNH QUAN SÁT PHỤ", "bg": "namerica",
     "titleAt": [0, "quay"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "MỘT CON MẮT THỨ HAI", "at": [1, "con"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "VỆ TINH OKO · BÊN TRONG", "srcnote": "PODVIG 2002 · TR. 40",
     "rows": [{"k": "KÍNH CHÍNH", "v": "GƯƠNG ≈ 50 CM · HỒNG NGOẠI", "at": [2, "kính"]},
              {"k": "KÍNH NHỎ", "v": "GÓC RỘNG · HỒNG NGOẠI + THƯỜNG?", "at": 3},
              {"k": "DÙNG ĐỂ", "v": "KÊNH QUAN SÁT PHỤ", "at": [4, "kênh"]}]},
    {"type": "photo", "at": 5, "img": "namerica", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "LÃNH THỔ MỸ NHÌN TỪ VỆ TINH", "at": [5, "màn"], "acc": True}],
     "label": {"k": "BẮC MỸ NHÌN TỪ VỆ TINH SUOMI NPP", "v": "ẢNH NASA / NOAA · 2012", "at": 5}},
    {"type": "quote", "at": 6, "text": "На экране — территория США, вид со спутников… в оптическом диапазоне… и в инфракрасном.",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004", "lbl": "TRÍCH DỊCH", "qline": 6, "typeAt": [6, "trên"]},
    {"type": "quote", "at": 7, "text": "Но просто наблюдать — этого мало для принятия решения. Нужен судья беспристрастный. То бишь компьютер.",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004", "lbl": "TRÍCH DỊCH", "qline": 7, "typeAt": [7, "nhưng"]},
    {"type": "kinetic", "at": 8, "items": [{"text": "ĐÊM ẤY, CON MẮT THỨ HAI NÓI GÌ?", "at": 8, "acc": True}]},
    {"type": "ledger", "at": 9, "title": "CON MẮT THỨ HAI · HAI BẢN KỂ", "srcnote": "BBC 2013 · MOSKOVSKIYE NOVOSTI 2004",
     "rows": [{"k": "BBC 2013", "v": "QUAN SÁT: KHÔNG THẤY TÊN LỬA", "at": [9, "không"]},
              {"k": "BẢN 2004", "v": "NHÌN TRỰC TIẾP: CHẲNG THẤY GÌ", "at": 12},
              {"k": "NHƯNG", "v": "NGÀY THƯỜNG CŨNG HAY NHƯ THẾ", "at": 13}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "chỉ là bộ phận hỗ trợ · BBC", "at": 14, "sm": True},
                                            {"text": "QUYẾT ĐỊNH DỰA TRÊN SỐ LIỆU MÁY TÍNH", "at": 15, "acc": True},
                                            {"text": "VÀ THUỘC VỀ NGƯỜI TRỰC", "at": 16}]},
    {"type": "bars", "at": 17, "title": "CẢNH BÁO TÊN LỬA MỸ · NHẮC LẠI CHƯƠNG MỘT", "unit": "PHÚT · PFIAB 1990", "max": 35,
     "items": [{"k": "VỆ TINH", "v": 30, "lbl": "≈ 30", "at": [18, "vệ"], "acc": True},
               {"k": "RADAR MẶT ĐẤT", "v": 13, "lbl": "≈ 13", "at": [18, "mười"]}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "RADAR CÒN PHẢI CHỜ NHIỀU PHÚT", "at": [19, "chờ"], "acc": True},
                                            {"text": "chiếc ghế không có nhiều phút như thế", "at": 20, "sm": True}]},
    {"type": "slam", "at": 22, "text": "QUÁ MẠNH, QUÁ RÕ", "sub": "ĐIỀU LÀM PETROV NGHI · BBC 2013 · 28–29 TẦNG KIỂM TRA"},
    {"type": "broll", "at": 24, "vid": "14904107", "veil": 0.55, "illus": VV,
     "kin": [{"text": "BẢN 2004 · CÂU THẲNG THỪNG HƠN", "at": 24, "sm": True}]},
    {"type": "quote", "at": 25, "text": "Компьютер по определению — дурак. Мало ли что он за пуск примет…",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004", "lbl": "TRÍCH DỊCH", "qline": 25, "typeAt": [25, "máy"]},
    seat(6, 26, 28, "MẨU TIN 6 / 6 · BBC 2013 · BẢN 2004 · PFIAB",
         total={"k": "MÁY", "v": "CHẮC CHẮN · RADAR CHƯA THẤY", "at": 29}),
    {"type": "question", "at": 30, "text": "Lần hỏi cuối.\n" + BTN},
]}

# ---------------------------------------------------------------- CH08: cuộc gọi (cảnh mạnh)
CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "CUỘC GỌI"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "CUỘC GỌI", "sub": "SERPUKHOV-15 · RẠNG SÁNG 26.09.1983", "vid": "8706309", "illus": VV,
     "titleAt": [0, "theo"]},
    {"type": "quote", "at": 1, "text": "All I had to do was to reach for the phone… but I couldn’t move. I felt like I was sitting on a hot frying pan.",
     "by": "STANISLAV PETROV · BBC NEWS · 2013", "lbl": "TRÍCH DỊCH", "qline": 1, "typeAt": [1, "nhưng"]},
    {"type": "kinetic", "at": 2, "items": [{"text": "RẤT ÍT THỜI GIAN", "at": [2, "ít"], "acc": True}]},
    {"type": "quote", "at": 3, "text": "За те две-три минуты толком ничего не проанализируешь. Остаётся интуиция.",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004", "lbl": "TRÍCH DỊCH", "qline": 3, "typeAt": [3, "trong"]},
    {"type": "broll", "at": 4, "vid": "9088981", "veil": 0.5, "illus": VV,
     "kin": [{"text": "ÔNG NHẤC MÁY", "at": [4, "nhấc"], "acc": True},
             {"text": "gọi sĩ quan trực · sở chỉ huy quân đội Liên Xô", "at": 5, "sm": True}]},
    {"type": "slam", "at": 6, "text": "HỆ THỐNG TRỤC TRẶC", "sub": "KHÔNG PHẢI: “BỊ TẤN CÔNG” · BBC 2013"},
    {"type": "quote", "at": 9, "text": "I knew perfectly well that nobody would be able to correct my mistake if I had made one.",
     "by": "STANISLAV PETROV · BBC NEWS · 2013", "lbl": "TRÍCH DỊCH", "qline": 9, "typeAt": [9, "tôi"]},
    {"type": "question", "at": 10, "text": "Vậy câu trả lời\ncho hai cái nút?"},
    {"type": "slam", "at": 11, "text": "BÁO LÊN: MÁY SAI", "sub": "ÔNG BÁO ĐIỀU NGƯỢC LẠI VỚI CỖ MÁY"},
    {"type": "ledger", "at": 12, "title": "HAI BÀN TAY", "srcnote": "MOSKOVSKIYE NOVOSTI 2004",
     "rows": [{"k": "MỘT TAY", "v": "ỐNG NGHE · BÁO CÁO CẤP TRÊN", "at": [12, "ống"]},
              {"k": "TAY KIA", "v": "MICRO · RA LỆNH CHO KÍP TRỰC", "at": 13}],
     "total": {"k": "HÃY NHỚ", "v": "SẼ QUAY LẠI KHI ĐIỀU TRA", "at": 14}},
    {"type": "kinetic", "at": 15, "items": [{"text": "NẾU ÔNG SAI", "at": [15, "nếu"], "sm": True},
                                            {"text": "VÀI PHÚT SAU · NHỮNG VỤ NỔ ĐẦU TIÊN", "at": [15, "những"], "acc": True}]},
    {"type": "counter", "at": 16, "from": 0, "to": 23, "suffix": " PHÚT", "until": [16, "cả"], "label": "KHÔNG CÓ GÌ ĐẾN CẢ",
     "sub": {"text": "BBC 2013", "at": 16}},
    {"type": "quote", "at": 17, "text": "Twenty-three minutes later I realised that nothing had happened. If there had been a real strike, then I would already know about it. It was such a relief.",
     "by": "STANISLAV PETROV · BBC NEWS · 2013", "lbl": "TRÍCH DỊCH", "qline": 17, "typeAt": [17, None, 0, 0.05], "typeDur": 3.2},
    {"type": "bars", "at": 18, "title": "ÔNG ƯỚC KHẢ NĂNG ĐÊM ẤY", "unit": "% · BBC 2013", "max": 100,
     "items": [{"k": "BÁO ĐỘNG GIẢ", "v": 50, "lbl": "50", "at": [18, "năm", 1]},
               {"k": "TẤN CÔNG THẬT", "v": 50, "lbl": "50", "at": [18, "năm", 2], "acc": True}]},
    {"type": "slam", "at": 20, "text": "50 / 50", "sub": "“CHƯA BAO GIỜ CHẮC TUYỆT ĐỐI” · BBC 2013"},
    {"type": "kinetic", "at": 21, "items": [{"text": "NGƯỜI KHÁC TRỰC → CÓ LẼ ĐÃ BÁO LÊN", "at": [21, "đồng"], "acc": True},
                                            {"text": "theo Petrov · BBC 2013", "at": 21, "sm": True}]},
    {"type": "source", "at": 22, "source": "BBC NEWS · 26.09.2013", "ref": "“STANISLAV PETROV: THE MAN WHO MAY HAVE SAVED THE WORLD”",
     "snippet": "This was a breach of his instructions, a dereliction of duty. [[The safe thing to do would have been to pass the responsibility on]], to refer up.",
     "hlAt": 24, "seal": "TRÍCH NGẮN · TIẾNG ANH", "sealAt": [24, "đẩy"]},
    {"type": "quote", "at": 26, "text": "I had all the data. If I had sent my report up the chain of command, nobody would have said a word against it.",
     "by": "STANISLAV PETROV · BBC NEWS · 2013", "lbl": "TRÍCH DỊCH", "qline": 26, "typeAt": [26, "tôi"]},
    {"type": "kinetic", "at": 27, "items": [{"text": "BẤM “BÁO LÊN” KHÔNG HỀ NGỐC", "at": [27, "ngốc"], "acc": True},
                                            {"text": "đúng điều bản hướng dẫn yêu cầu", "at": 28, "sm": True}]},
    {"type": "ledger", "at": 29, "title": "GHẾ TRỰC · ĐỦ SÁU MẨU TIN", "srcnote": "CÁC CHƯƠNG 1–7",
     "rows": [dict(r, at=29) for r in R],
     "total": {"k": "VÀ MỘT NGƯỜI", "v": "CÂN CHÚNG VỚI CỖ MÁY", "at": [29, "bàn"]}},
    {"type": "photo", "at": 30, "img": "glint", "tone": "color", "move": "in", "veil": 0.55, "illus": VM,
     "kin": [{"text": "VỆ TINH ĐÃ THẤY GÌ?", "at": [30, "vệ"], "acc": True}],
     "label": {"k": "ÁNH NẮNG VÀ MÂY NHÌN TỪ ISS", "v": "ẢNH NASA · 2012", "at": 30}},
]}

# ---------------------------------------------------------------- CH09: ánh nắng trên mây
CH["ch09"] = {"hud": {"k": "CHƯƠNG 09", "t": "ÁNH NẮNG TRÊN MÂY"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "9", "k": "CHƯƠNG CHÍN", "title": "ÁNH NẮNG\nTRÊN MÂY", "sub": "CÁC ĐOÀN ĐIỀU TRA", "bg": "clouds", "titleAt": [0, "câu"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "KHÔNG NGỦ MẤY NGÀY · UỶ BAN KÉO TỚI", "at": [1, "ngủ"]},
                                           {"text": "GIAI THOẠI: NỬA LÍT RƯỢU, NGỦ 28 TIẾNG", "at": [2, "giai"], "fx": "strike", "strikeAt": [3, "cấm"]},
                                           {"text": "thị trấn quân sự cấm rượu · Petrov, 2004", "at": 3, "sm": True}]},
    {"type": "source", "at": 4, "source": "P. PODVIG · 2002 · TR. 39–40", "ref": "SCIENCE & GLOBAL SECURITY 10",
     "snippet": "In 1983 the system almost generated a serious false alarm, which was later attributed to problems with the software being [[unable to cope with sun reflections properly]].",
     "hlAt": 5, "seal": "DẪN SANG FORDEN 2001 · KÊNH CHƯA MỞ ĐƯỢC", "sealAt": [6, "dẫn"]},
    {"type": "kinetic", "at": 7, "items": [{"text": "NHỮNG QUỸ ĐẠO NHẤT ĐỊNH", "at": [8, "quỹ"]},
                                           {"text": "MỘT GÓC ỐNG KÍNH NHẤT ĐỊNH", "at": [8, "góc"]},
                                           {"text": "DẢI HỒNG NGOẠI", "at": [8, "hồng"], "acc": True}]},
    {"type": "slam", "at": 9, "text": "“TRÒ ĐÙA CỦA CHÚA TỪ VŨ TRỤ”", "sub": "PETROV · MOSKOVSKIYE NOVOSTI 2004"},
    {"type": "photo", "at": 10, "img": "glint", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "NẮNG PHẢN CHIẾU TRÊN ĐỈNH MÂY", "at": [11, "phản"], "acc": True},
             {"text": "bị nhầm thành một vụ phóng · Guardian 2017", "at": [11, "thành"], "sm": True}],
     "label": {"k": "ÁNH NẮNG PHẢN CHIẾU, MÂY NHÌN TỪ ISS", "v": "ẢNH NASA · 2012", "at": 10}},
    {"type": "slam", "at": 12, "text": "MÂY", "sub": "CHỮ Ở CHƯƠNG HAI · PODVIG 2002 TR. 45"},
    {"type": "kinetic", "at": 13, "items": [{"text": "NGƯỜI THIẾT KẾ ĐÃ BIẾT", "at": [13, "thiết"], "acc": True},
                                            {"text": "nhiều vệ tinh cùng canh một chỗ", "at": 14, "sm": True},
                                            {"text": "ĐÊM ẤY VẪN LỌT QUA", "at": 15}]},
    {"type": "ledger", "at": 16, "title": "NGUYÊN NHÂN · NGUỒN NÓI GÌ", "srcnote": "KÊNH ĐỐI CHIẾU 23.10.2026",
     "rows": [{"k": "PODVIG", "v": "PHẦN MỀM NHẦM NẮNG PHẢN CHIẾU", "at": 16},
              {"k": "GUARDIAN", "v": "NẮNG PHẢN CHIẾU TRÊN ĐỈNH MÂY", "at": 16},
              {"k": "WIKIPEDIA", "v": "MÂY CAO + GÓC HIẾM (CHƯA RÕ)", "at": [16, "mây"]}],
     "total": {"k": "KÊNH", "v": "DỪNG Ở HAI NGUỒN ĐẦU", "at": 17}},
    {"type": "timeline", "at": 18, "bg": "glint", "items": [{"year": "1982", "text": "Oko *trực chiến* · nhìn xiên", "at": 18},
                                            {"year": "1983", "text": "*báo động giả*", "at": [18, "phóng"]},
                                            {"year": "02.1991", "text": "vệ tinh *thế hệ hai* · nhìn được trên nền mặt đất", "at": 19}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "CÒN NGƯỜI NGỒI GHẾ?", "at": 20, "acc": True}]},
    {"type": "ledger", "at": 21, "title": "CUỘC ĐIỀU TRA", "srcnote": "MOSKOVSKIYE NOVOSTI 2004",
     "rows": [{"k": "TƯỚNG Y. VOTINTSEV", "v": "ĐÍCH THÂN TỚI", "at": [21, "đích"]},
              {"k": "LÚC ĐẦU", "v": "HỨA ĐỀ NGHỊ KHEN THƯỞNG", "at": [22, "hứa"]},
              {"k": "RỒI HỎI", "v": "SAO NHẬT KÝ TRỰC ĐỂ TRỐNG?", "at": 23},
              {"k": "PETROV ĐÁP", "v": "1 TAY ỐNG NGHE · 1 TAY MICRO", "at": 24}]},
    {"type": "slam", "at": 25, "text": "KHIỂN TRÁCH", "sub": "VÌ CUỐN NHẬT KÝ · KHÔNG KHEN THƯỞNG · BBC 2013 + BẢN 2004"},
    {"type": "quote", "at": 28, "text": "Если награждать меня за тот случай, то кто-то за него же должен был очень крупно пострадать.",
     "by": "S. PETROV · MOSKOVSKIYE NOVOSTI · 2004", "lbl": "TRÍCH DỊCH", "qline": 28, "typeAt": [28, "nếu"]},
    {"type": "kinetic", "at": 29, "items": [{"text": "IM LẶNG MƯỜI NĂM", "at": [29, "im"], "acc": True},
                                            {"text": "“xấu hổ cho quân đội Liên Xô” · BBC", "at": 30, "sm": True},
                                            {"text": "tự xin rời quân ngũ · bản 2004", "at": 31, "sm": True}]},
    {"type": "broll", "at": 32, "vid": "5004222", "veil": 0.55, "illus": VV,
     "kin": [{"text": "THÁNG 11 NĂM 1983", "at": 32, "acc": True},
             {"text": "lại có người ở giữa vòng lặp", "at": 33, "sm": True}]},
]}

# ---------------------------------------------------------------- CH10: tháng 11, rồi một bộ phim
CH["ch10"] = {"hud": {"k": "CHƯƠNG 10", "t": "THÁNG 11, RỒI MỘT BỘ PHIM"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "10", "k": "CHƯƠNG MƯỜI", "title": "THÁNG 11,\nRỒI MỘT BỘ PHIM", "sub": "ABLE ARCHER 83 · KẺ HỦY DIỆT 1984",
     "vid": "30101621", "illus": VV, "titleAt": [0, "đầu"]},
    {"type": "date", "at": 1, "day": "TẬP TRẬN DIỄN RA TRONG KHOẢNG", "date": "03–11.11.1983",
     "sub": {"text": "PFIAB 1990 · ABLE ARCHER 83", "at": [1, "tập"]}},
    {"type": "ledger", "at": 2, "title": "ABLE ARCHER 83 · ĐIỂM MỚI", "srcnote": "PFIAB 1990",
     "rows": [{"k": "1", "v": "TẬP QUY TRÌNH DÙNG HẠT NHÂN", "at": 3},
              {"k": "2", "v": "ĐIỆN GIẢ: BÌNH THƯỜNG → BÁO ĐỘNG", "at": 4}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "NHƯ TRONG KHỦNG HOẢNG THẬT", "at": [5, "khủng"], "acc": True},
                                           {"text": "không quân Liên Xô ở Đức, Ba Lan · báo động cao", "at": 6, "sm": True}]},
    {"type": "source", "at": 7, "source": "PFIAB · 15.02.1990", "ref": "VỀ LEONARD PERROOTS · TÌNH BÁO KHÔNG QUÂN MỸ Ở CHÂU ÂU",
     "snippet": "…his recommendation, made in ignorance, not to raise US readiness in response — [[a fortuitous, if ill-informed, decision]]…",
     "hlAt": 9, "seal": "BÁO CÁO GIẢI MẬT 2015", "sealAt": [9, "may"]},
    {"type": "quote", "at": 10, "text": "…these officers acted correctly out of instinct, not informed guidance…",
     "by": "PFIAB · “THE SOVIET ‘WAR SCARE’” · 1990", "lbl": "TRÍCH DỊCH", "qline": 10, "typeAt": [10, "những"]},
    {"type": "quote", "at": 12, "text": "In 1983 we may have inadvertently placed our relations with the Soviet Union on a hair trigger.",
     "by": "PFIAB · “THE SOVIET ‘WAR SCARE’” · 1990", "lbl": "TRÍCH DỊCH", "qline": 12, "typeAt": [12, "năm"]},
    {"type": "kinetic", "at": 13, "items": [{"text": "HAI LẦN TRONG HAI THÁNG", "at": [13, "hai"], "sm": True},
                                            {"text": "CHỐT AN TOÀN CUỐI CÙNG: MỘT CON NGƯỜI", "at": 14, "acc": True}]},
    {"type": "date", "at": 15, "day": "KẺ HỦY DIỆT RA RẠP Ở MỸ", "date": "26.10.1984",
     "sub": {"text": "1.012 RẠP · VIỆN PHIM MỸ (AFI)", "at": [15, "nghìn"]}},
    {"type": "kinetic", "at": 16, "items": [{"text": "một người lính từ tương lai kể · tóm tắt của AFI", "at": [16, "người"], "sm": True},
                                            {"text": "CHIẾN TRANH HẠT NHÂN DO MÁY TÍNH MẠNG LƯỚI QUỐC PHÒNG GÂY RA", "at": 17, "acc": True}]},
    {"type": "slam", "at": 18, "text": "SKYNET", "sub": "TÊN MẠNG LƯỚI TRONG PHIM · CHỈ NHẮC TÊN, KHÔNG DÙNG HÌNH PHIM"},
    {"type": "kinetic", "at": 19, "items": [{"text": "KHÔNG CÓ BẰNG CHỨNG", "at": [20, "bằng"], "acc": True},
                                            {"text": "phim lấy cảm hứng từ đêm ở Serpukhov", "at": [20, "phim"], "sm": True},
                                            {"text": "năm 1984: chuyện của Petrov còn là bí mật", "at": 21, "sm": True}]},
    {"type": "ledger", "at": 22, "title": "HAI MẶT CỦA MỘT NỖI SỢ", "srcnote": "KÊNH ĐẶT CẠNH NHAU · AFI · BBC 2013",
     "rows": [{"k": "TRONG PHIM", "v": "MÁY TỰ QUYẾT, KHÔNG CÓ NGƯỜI", "at": 23},
              {"k": "1983", "v": "MÁY BÁO “TẤN CÔNG” · TIN CẬY CAO", "at": 24}],
     "total": {"k": "KHÁC NHAU", "v": "MỘT NGƯỜI NGỒI Ở GIỮA", "at": 25}},
    {"type": "photo", "at": 26, "img": "warsaw", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "THẾ GIỚI BIẾT TÊN ÔNG BẰNG CÁCH NÀO?", "at": [26, "thế"], "acc": True}],
     "label": {"k": "VƯỜN NGƯỜI CÔNG CHÍNH · WARSAW", "v": "ẢNH: CYBULARNY · CC0 · 2023", "at": 26}},
]}

# ---------------------------------------------------------------- CH11: người ở giữa vòng lặp
CH["ch11"] = {"hud": {"k": "CHƯƠNG 11", "t": "NGƯỜI Ở GIỮA VÒNG LẶP"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "11", "k": "CHƯƠNG MƯỜI MỘT", "title": "NGƯỜI Ở GIỮA\nVÒNG LẶP", "sub": "1991 → HÔM NAY", "bg": "warsaw", "titleAt": [0, "câu"]},
    {"type": "ledger", "at": 1, "title": "CÂU CHUYỆN LỘ RA · HAI MỐC", "srcnote": "MOSKOVSKIYE NOVOSTI 2004 · GUARDIAN 2017",
     "rows": [{"k": "BẢN 2004", "v": "VOTINTSEV KỂ · ĐẦU THẬP NIÊN 90", "at": [1, "phỏng"]},
              {"k": "GUARDIAN 2017", "v": "HỒI KÝ ÔNG TƯỚNG · 1998", "at": [2, "hồi"]}],
     "total": {"k": "KÊNH", "v": "ĐỂ CẢ HAI", "at": 3}},
    {"type": "timeline", "at": 4, "bg": "memorial", "items": [{"year": "2006", "text": "vinh danh tại *trụ sở Liên Hợp Quốc*", "at": 4},
                                           {"year": "2013", "text": "*giải Hoà bình Dresden*", "at": [5, "giải"]}]},
    {"type": "print", "at": 6, "img": "memorial", "tone": "color",
     "side": {"k": "WARSAW · BA LAN", "h": "“LIỀU MÌNH\nNHÂN DANH\nNHÂN LOẠI”", "lines": [{"text": "phiến đá tưởng niệm Stanislav Petrov (1939–2017)", "at": [6, "phiến"]}]}},
    {"type": "date", "at": 7, "day": "STANISLAV PETROV MẤT Ở FRYAZINO", "date": "19.05.2017",
     "sub": {"text": "TIN ĐƯỢC ĐƯA RA 18.09.2017 · GUARDIAN", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "KHÔNG NHẬN MÌNH LÀ ANH HÙNG", "at": [9, "anh"], "acc": True}]},
    {"type": "quote", "at": 10, "text": "That was my job. But they were lucky it was me on shift that night.",
     "by": "STANISLAV PETROV · BBC NEWS · 2013", "lbl": "TRÍCH DỊCH", "qline": 10, "typeAt": [10, "đó"]},
    {"type": "kinetic", "at": 11, "items": [{"text": "DER SPIEGEL · 2010", "at": 11, "sm": True}, {"text": "QUA GUARDIAN 2017", "at": [11, "dẫn"]}]},
    {"type": "quote", "at": 12, "text": "We are wiser than the computers. We created them.",
     "by": "STANISLAV PETROV · DER SPIEGEL 2010 · QUA GUARDIAN 2017", "lbl": "TRÍCH DỊCH", "qline": 12, "typeAt": [12, "chúng"]},
    {"type": "broll", "at": 13, "vid": "14904107", "veil": 0.55, "illus": VV,
     "kin": [{"text": "máy không chỉ báo động", "at": 13, "sm": True},
             {"text": "GỢI Ý · XẾP HẠNG · CHẤM ĐIỂM · TRẢ LỜI", "at": [14, "gợi"], "acc": True}]},
    {"type": "source", "at": 15, "source": "QUY ĐỊNH (EU) 2024/1689 · ĐẠO LUẬT AI", "ref": "ĐIỀU 14 · GIÁM SÁT CỦA CON NGƯỜI · KHOẢN 4(B)",
     "snippet": "…to remain aware of the possible tendency of automatically relying or over-relying on the output… [[(automation bias)]]",
     "hlAt": 17, "seal": "VĂN BẢN LUẬT · TIẾNG ANH", "sealAt": [16, "dựa"]},
    {"type": "ledger", "at": 18, "title": "ĐIỀU 14 · NGƯỜI GIÁM SÁT PHẢI CÓ THỂ", "srcnote": "EU AI ACT · ĐIỀU 14(4)(D)–(E)",
     "rows": [{"k": "BỎ QUA", "v": "DISREGARD", "at": [18, "bỏ"]},
              {"k": "GHI ĐÈ", "v": "OVERRIDE", "at": [18, "ghi"]},
              {"k": "ĐẢO NGƯỢC", "v": "REVERSE", "at": [18, "đảo"]},
              {"k": "DỪNG", "v": "NÚT “STOP”", "at": [18, "nút"]}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "1983: KHÔNG CÓ ĐIỀU LUẬT NÀO", "at": [19, "luật"]},
                                            {"text": "BẢN HƯỚNG DẪN BẢO LÀM NGƯỢC LẠI", "at": 20, "acc": True}]},
    {"type": "ledger", "at": 21, "title": "HAI CHIỀU CỦA MỘT VÒNG LẶP", "srcnote": "VIDEO APOLLO 11 CỦA KÊNH · VIDEO NÀY",
     "rows": [{"k": "1969", "v": "MÁY BÁO ĐỘNG · NGƯỜI CHO ĐI TIẾP", "at": [21, "báo"]},
              {"k": "1983", "v": "MÁY CHẮC CHẮN · NGƯỜI KHÔNG TIN", "at": [22, "chắc"]}]},
    {"type": "question", "at": 23, "text": "Bạn bấm BÁO LÊN ở mẩu tin thứ mấy?\n" + BTN},
    {"type": "kinetic", "at": 25, "items": [{"text": "GHI CON SỐ VÀO BÌNH LUẬN", "at": [25, "ghi"], "acc": True},
                                            {"text": "và điều gì làm bạn đổi ý", "at": [25, "điều"], "sm": True}]},
]}

SPEC = {
    "title": "KẺ HỦY DIỆT Ngoài Đời Thật: Petrov, Người Không Tin Máy Tính",
    "channel": "MIM", "theme": "lab", "accent": "#f59e0b", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["báo", "máy", "phóng", "mây", "người", "ghế", "chưa", "tấn"],
    "say": SAY, "imgs": IMGS, "chapters": [f"ch{i:02d}" for i in range(12)],
    "youtube": {
        "titles": ["KẺ HỦY DIỆT Ngoài Đời Thật: Petrov, Người Không Tin Máy Tính",
                   "KẺ HỦY DIỆT Ngoài Đời Thật: Máy Tính Báo Mỹ Phóng 5 Tên Lửa, Và Một Người Không Tin",
                   "Đêm 26/9/1983: Vệ Tinh Báo Tấn Công Hạt Nhân, Stanislav Petrov Nhấc Máy Báo “Hệ Thống Hỏng”"],
        "summary": "Phim Kẻ Hủy Diệt (1984) tưởng tượng một mạng máy tính quốc phòng tự gây ra chiến tranh hạt nhân; một năm trước đó, "
                   "đêm 25 rạng 26/9/1983, trung tá Stanislav Petrov ngồi ghế trực ở Serpukhov-15 khi hệ thống vệ tinh Oko báo Mỹ phóng tên lửa. "
                   "Video mời bạn ngồi vào ghế của ông: mỗi chương thêm một mẩu tin ông có (hoặc người phía Mỹ từng có), rồi bạn chọn báo lên hay chưa. "
                   "Từ quỹ đạo nhìn xiên của vệ tinh, báo động giả của NORAD năm 1979 và con chip 46 xu năm 1980, tới cuộc gọi báo "
                   "\"hệ thống trục trặc\", ánh nắng trên đỉnh mây, Able Archer 83 và điều 14 của Đạo luật AI châu Âu.",
        "more": ["Lời của Stanislav Petrov trong video lấy từ các phỏng vấn đã đăng: báo Moskovskiye Novosti (27/04/2004), BBC (26/09/2013) và "
                 "Der Spiegel 2010 (qua Guardian 2017). Các bản kể lệch nhau ở vài chỗ và video nói thẳng từng chỗ: bốn hay năm tên lửa, "
                 "30 hay 28–29 tầng kiểm tra, học vấn của ông, và năm câu chuyện được công bố. Nguyên nhân kỹ thuật chỉ nêu ở mức các nguồn mở được: "
                 "bài báo khoa học của Pavel Podvig (2002) viết phần mềm không xử lý đúng ánh nắng phản chiếu; Guardian viết ánh nắng trên đỉnh mây. "
                 "Chuyện cố vấn Brzezinski lúc ba giờ sáng chỉ đi qua hồi ký của Robert Gates. Phim Kẻ Hủy Diệt chỉ được nhắc tên, không dùng hình phim, "
                 "và không có bằng chứng phim lấy cảm hứng từ vụ việc. Video không dùng ảnh chân dung Petrov."],
        "chapter_titles": {"ch00": "Mở đầu: chữ \"phóng\" trên màn hình đỏ", "ch01": "Chiếc ghế bạn vừa ngồi", "ch02": "Con mắt trên quỹ đạo",
                           "ch03": "Một, rồi năm", "ch04": "Mùa thu năm 1983", "ch05": "Ba giờ sáng ở Washington",
                           "ch06": "Con chip bốn mươi sáu xu", "ch07": "Con mắt thứ hai im lặng", "ch08": "Cuộc gọi",
                           "ch09": "Ánh nắng trên mây", "ch10": "Tháng 11, rồi một bộ phim", "ch11": "Người ở giữa vòng lặp"},
        "sources": [
            "https://scienceandglobalsecurity.org/archive/sgs10podvig.pdf",
            "https://www.bbc.co.uk/news/world-europe-24280831",
            "https://flb.ru/info/27637.html",
            "https://www.theguardian.com/world/2017/sep/18/soviet-officer-who-averted-cold-war-nuclear-disaster-dies-aged-77",
            "https://nsarchive2.gwu.edu/nukevault/ebb533-The-Able-Archer-War-Scare-Declassified-PFIAB-Report-Released/",
            "https://nsarchive2.gwu.edu/nukevault/ebb533-The-Able-Archer-War-Scare-Declassified-PFIAB-Report-Released/2012-0238-MR.pdf",
            "https://nsarchive2.gwu.edu/nukevault/ebb371/",
            "https://www.csmonitor.com/1980/1030/103032.html",
            "https://catalog.afi.com/Catalog/moviedetails/57224",
            "https://en.wikipedia.org/wiki/The_Terminator",
            "https://artificialintelligenceact.eu/article/14/",
        ],
        "hashtags": ["StanislavPetrov", "KẻHủyDiệt", "CôngNghệ", "CôngNghệQuanhTa", "MindInTheMachine"],
        "tags": ["stanislav petrov", "kẻ hủy diệt", "the terminator", "skynet", "báo động giả hạt nhân 1983", "chiến tranh lạnh",
                 "vệ tinh oko", "con người trong vòng lặp", "able archer 83", "công nghệ quanh ta", "lịch sử máy tính"],
        "category": "28", "thumb": "t1.jpg", "playlist": "Công Nghệ Quanh Ta", "publish_at": "2026-11-20T13:00:00Z",
        "video_credits": ["Ảnh Wikimedia Commons: NASA, NOAA, Không quân và Lực lượng Vũ trụ Mỹ, Bộ Quốc phòng Mỹ, Nhà Trắng (phạm vi công cộng); "
                          "phiến đá tưởng niệm ở Warsaw: Brandmeister (phạm vi công cộng); Vườn Người Công chính Warsaw: Cybularny (CC0)",
                          "Video B-roll: Pexels"],
    },
    "sources_internal": "factcheck.md (mã nguồn PODVIG, BBC13, MN04, GUA17, PFIAB, EBB371, CSM80, AFI, WP-TERM, EUAI). Không mở được: "
                        "Washington Post 1999 (403), Forden/CATO 2001 (chặn), DoD 3000.09 (403), NYT 2017 (403), Dresden Friedenspreis (DNS).",
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
    """Kiểm neo với lines (sau script_lines.py): lỗi nếu dòng không có, từ neo không nằm trong dòng, hoặc từ neo nằm trong SAY.
    Trả về danh sách lỗi."""
    bad = []
    say = {k.lstrip("=").lower() for k in SAY}
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
                        toks = [_norm(t) for t in text[i].split()]
                        n = a[2] if len(a) > 2 else 0
                        if toks.count(_norm(a[1])) <= n:
                            bad.append(f"{name} cảnh {si} {p}: dòng {i} không có chữ {a[1]!r} (lần {n}): {text[i]}")
                        if _norm(a[1]) in say or _norm(a[1]).isdigit():
                            bad.append(f"{name} cảnh {si} {p}: chữ neo {a[1]!r} là chữ số hoặc nằm trong SAY")
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
