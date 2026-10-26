"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM "GOOGLE MAPS ngoài đời thật: Ronald Reagan và chuyến bay KAL 007".

    python data/long/mim-google-maps-kal007/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md và factcheck.md. Pha 1: chỉ viết file; chưa dựng, chưa tải ảnh (imgs ghi tên File: Commons, giấy phép đã đọc qua
Commons API ngày 23/10/2026, phải đọc lại ở pha 2). Không có clip Pexels, không ảnh máy bay HL7442 (GFDL/BY-SA), không ảnh đảo Moneron (BY-SA),
không giao diện/logo Google Maps: "chấm xanh" là hình của kênh (kinetic/slam). Đường bay vẽ bằng cảnh `map` (Natural Earth / world-atlas),
ghim + tuyến là VẼ GẦN ĐÚNG, không theo dữ liệu tuyến bay; ghim "điểm trúng tên lửa" lấy toạ độ của phân tích phía Nga (Phụ lục D báo cáo ICAO 1993).
Lộ trình dạng "con số co lại": ledger "CÂY THƯỚC SAI SỐ" ở CH00 (hứa), CH02 (nấc 1: hơn 600 km), CH04 (nấc 2: ~100 m), CH06 (nấc 3: ~5 m + ai trả giá).
Mọi neo [dòng, "từ"] chỉ dùng chữ nằm trong lời đọc; không neo vào chữ số hay chữ có trong bảng "say".
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"boeing": "Bô-ing", "747": "bảy bốn bảy", "korean": "Co-ri-ần", "air": "e", "lines": "lai", "kal": "ca a eo", "007": "không không bảy",
       "seoul": "Xơ-un", "google": "Gu-gồ", "maps": "Mép", "ronald": "Rô-nân", "reagan": "Rây-gần", "anchorage": "An-cơ-rịt",
       "alaska": "A-lát-xca", "r20": "e-rờ hai mươi", "kamchatka": "Cam-chát-ca", "sakhalin": "Xa-kha-lin", "icao": "i-ca-ô",
       "bethel": "Bê-thồn", "litton": "Lít-tơn", "tokyo": "Tô-ki-ô", "rc-135": "a xê một ba năm", "805": "tám không năm",
       "osipovich": "Ô-xi-pô-vích", "larry": "Le-ri", "speakes": "Xpích", "gps": "gi pi ét", "sa": "ét a", "kentucky": "Ken-tắc-ki",
       "bill": "Biu", "clinton": "Clin-tơn", "iii": "ba", "stanislav": "Xta-nít-xláp", "petrov": "Pê-trốp", "radio": "ra-đi-ô",
       "video": "vi-đê-ô"}
VM = "ẢNH MINH HỌA"
SELF = "TỰ TÍNH"
MAPNOTE = "ĐƯỜNG VẼ GẦN ĐÚNG · KHÔNG PHẢI DỮ LIỆU TUYẾN BAY"
CH = {}

IMGS = {
    "reagan_desk": "File:President Ronald Reagan Sitting at His Desk in The Oval Office Making An Address to The Nation on The Soviet Attack on a Korean "
                   "Civilian Airliner Korean Air Liner Kal 007 - DPLA - d80766446a812417349059bb062156a8.jpg",       # Public domain (White House Photographic Office)
    "reagan_press": "File:President Ronald Reagan Making An Address to The Nation on The Soviet Attack on a Korean Civilian Airliner Korean Airliner "
                    "Kal 007 in The Oval Office with The Press - DPLA - 9bc4c4de2b320aea1739414c28bc2ddb.jpg",          # Public domain (White House Photographic Office)
    "speakes": "File:Larry Melvin Speakes, Assistant to the President Principal Deputy Press Secretary ME522-10.jpg",       # Public domain (White House, 25/08/1983)
    "clinton": "File:Bill Clinton.jpg",                                                                                  # Public domain (Bob McNeely, The White House)
    "navstar2f": "File:Navstar-2F.jpg",                                                                                  # Public domain (USAF)
    "block1": "File:GPS Block1 ExplodedView.png",                                                                        # Public domain (USAF/DTIC, 1979)
    "launch": "File:310th Space Wing GPS Satellite Launch.jpg",                                                          # Public domain (USAF, 2009 · minh hoạ)
    "deck": "File:Boeing 747-100 Flight Deck (11735285715).jpg",                                                         # CC BY 2.0 (Clemens Vasters · minh hoạ)
    "kamchatka": "File:ISS-39 Kamchatka Peninsula.jpg",                                                                  # Public domain (NASA, 2014 · minh hoạ)
    "okhotsk": "File:ISS-39 Sea of Okhotsk.jpg",                                                                         # Public domain (NASA, 2014 · minh hoạ)
    "sakhalin": "File:Sakhalin Terra MODIS.jpg",                                                                         # Public domain (NASA/GSFC MODIS, 2002 · minh hoạ)
}

GEO = {
    "pac": {"countries": ["Russia", "Japan"], "context": ["China", "South Korea", "North Korea"],
            "labels": {"Russia": "LIÊN XÔ (1983)", "Japan": "NHẬT BẢN"},
            "bbox": [124.0, 34.0, 170.0, 61.0], "box": [200, 130, 1720, 860],
            "pins": [{"name": "Anchorage", "lon": 169.0, "lat": 57.5, "label": "TỪ ANCHORAGE →"},
                     {"name": "Kamchatka", "lon": 158.65, "lat": 53.02, "label": "KAMCHATKA"},
                     {"name": "Sakhalin", "lon": 142.8, "lat": 50.0, "label": "ĐẢO SAKHALIN"},
                     {"name": "Hit", "lon": 141.547, "lat": 46.774, "label": "18:26 UTC"},
                     {"name": "Seoul", "lon": 126.98, "lat": 37.57, "label": "SEOUL · ĐÍCH ĐẾN"}]},
}

# ---------------------------------------------------------------- CH00: đường bay lệch dần (cold open + lộ trình "con số co lại")
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "ĐƯỜNG BAY LỆCH DẦN"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "bg": "okhotsk", "day": "BẮC THÁI BÌNH DƯƠNG", "date": "31.08.1983",
     "sub": {"text": "GIỜ QUỐC TẾ (UTC) · BÁO CÁO ICAO 1993", "at": [0, "giờ"]}},
    {"type": "kinetic", "at": 1, "items": [{"text": "BOEING 747 · KOREAN AIR LINES", "at": 1, "acc": True},
                                           {"text": "chuyến KAL 007 · đích đến Seoul", "at": 2, "sm": True}]},
    {"type": "slam", "at": 3, "text": "CHẤM XANH", "sub": "TRÊN GOOGLE MAPS CỦA BẠN · CÓ DÍNH TỚI CHUYẾN BAY NÀY"},
    {"type": "print", "at": 4, "img": "reagan_desk", "tone": "color",
     "side": {"k": "TỔNG THỐNG MỸ · 1981–1989", "h": "Ronald\nReagan", "lines": [{"text": "*người thật* của câu chuyện", "at": [4, "người"]}]}},
    {"type": "map", "at": 5, "geo": "pac", "tag": MAPNOTE,
     "pins": [{"name": "Anchorage", "at": 5}, {"name": "Seoul", "at": [6, "bám"]}],
     "routes": [{"from": "Anchorage", "to": "Kamchatka", "at": [7, "lệch"], "until": 9, "bend": 0.12}]},
    {"type": "ledger", "at": 9, "title": "TRONG BUỒNG LÁI", "srcnote": "ICAO 1993 · TÓM TẮT KẾT LUẬN",
     "rows": [{"k": "TỔ LÁI BIẾT ĐANG LỆCH?", "v": "KHÔNG CÓ DẤU HIỆU", "at": 9},
              {"k": "QUA", "v": "KAMCHATKA → SAKHALIN", "at": 10},
              {"k": "PHÍA SAU", "v": "TIÊM KÍCH LIÊN XÔ", "at": 11}]},
    {"type": "photo", "at": 12, "img": "sakhalin", "tone": "bw", "move": "in", "veil": 0.55, "illus": VM,
     "kin": [{"text": "≈ 06:25 GIỜ SAKHALIN · 01.09", "at": 12, "acc": True}, {"text": "trời vẫn còn tối", "at": 13, "sm": True}],
     "label": {"k": "ĐẢO SAKHALIN", "v": "ẢNH VỆ TINH NASA · 2002", "at": 12}},
    {"type": "slam", "at": 14, "text": "18:25:30 UTC", "sub": "HAI TÊN LỬA RỜI GIÁ PHÓNG · ICAO 1993 MỤC 2.15.7", "white": True},
    {"type": "ledger", "at": 15, "title": "CÂY THƯỚC SAI SỐ · “TÔI ĐANG Ở ĐÂU?”", "srcnote": "KÊNH TỰ KẺ · MỖI CHƯƠNG CO MỘT NẤC",
     "rows": [{"k": "NẤC 1 · 1983", "v": "HÀNG TRĂM KM", "at": 17},
              {"k": "NẤC 2", "v": "?", "at": 18},
              {"k": "NẤC 3", "v": "?", "at": [19, "rồi"]}],
     "total": {"k": "CUỐI VIDEO", "v": "AI TRẢ GIÁ MỖI NẤC CO", "at": 20}},
]}

# ---------------------------------------------------------------- CH01: một con số trên la bàn
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MỘT CON SỐ TRÊN LA BÀN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MỘT CON SỐ\nTRÊN LA BÀN", "sub": "ANCHORAGE · 13:00 UTC", "bg": "deck",
     "titleAt": [0, "muốn"]},
    {"type": "slam", "at": 1, "text": "≈ 245°", "sub": "HƯỚNG LA BÀN TỪ · ĐẠT ĐƯỢC 3 PHÚT SAU KHI CẤT CÁNH · ICAO 1993 MỤC 3.7"},
    {"type": "kinetic", "at": 2, "items": [{"text": "GIỮ NGUYÊN HƯỚNG ẤY", "at": 2, "acc": True},
                                           {"text": "cho tới lúc bị tấn công", "at": [2, "tới"], "sm": True}]},
    {"type": "source", "at": 4, "source": "ICAO · THƯ LE 4/19.4-93/68 · 16/07/1993", "ref": "BÁO CÁO HOÀN TẤT ĐIỀU TRA · C-WP/9781",
     "snippet": "chiếc 747 giữ [[một hướng la bàn không đổi]] từ ngay sau khi rời Anchorage tới lúc bị tấn công", "hlAt": [4, "kết"],
     "seal": "DIỄN Ý TỪ BÁO CÁO · KHÔNG PHẢI TRÍCH NGUYÊN VĂN", "sealAt": 5},
    {"type": "timeline", "at": 6, "items": [{"year": "1983", "text": "Liên Xô *vớt* hai hộp đen", "at": 6},
                                           {"year": "01.1993", "text": "phía Nga *trao* cho ICAO", "at": [6, "trao"]},
                                           {"year": "06.1993", "text": "Hội đồng ICAO *xem xét* báo cáo", "at": 7}]},
    {"type": "ledger", "at": 7, "title": "MÁY GHI DỮ LIỆU NÓI GÌ", "srcnote": "ICAO 1993 · MỤC 1.14.3.8 VÀ TÓM TẮT",
     "rows": [{"k": "HƯỚNG GHI ĐƯỢC", "v": "245,4° (244,9°–246,0°)", "at": 7},
              {"k": "ĐỀU ĐẾN MỨC", "v": "CHỈ LÁI TỰ ĐỘNG LÀM ĐƯỢC", "at": [8, "lái"]},
              {"k": "HỎNG HÓC LỚN", "v": "KHÔNG CÓ", "at": 9}],
     "total": {"k": "KẾT LUẬN", "v": "MÁY BAY KHÔNG HỎNG", "at": 10}},
    {"type": "question", "at": 11, "text": "Vậy chuyện gì\nđã xảy ra?"},
    {"type": "photo", "at": 12, "img": "deck", "tone": "color", "move": "in", "veil": 0.55, "illus": VM,
     "kin": [{"text": "GIỮ HƯỚNG: BAY THEO MỘT CON SỐ LA BÀN", "at": 13, "acc": True},
             {"text": "DẪN ĐƯỜNG QUÁN TÍNH: BÁM TỪNG ĐIỂM ĐÃ NẠP", "at": 14}],
     "label": {"k": "BUỒNG LÁI BOEING 747-100", "v": "ẢNH: CLEMENS VASTERS · CC BY 2.0", "at": 12}},
    {"type": "ledger", "at": 15, "title": "ICAO: HAI KHẢ NĂNG", "srcnote": "ICAO 1993 · KẾT LUẬN 3.9",
     "rows": [{"k": "KHẢ NĂNG 1", "v": "ĐỂ QUÊN Ở CHẾ ĐỘ GIỮ HƯỚNG", "at": 16},
              {"k": "KHẢ NĂNG 2", "v": "LỆCH > 7,5 HẢI LÝ MỚI BẬT", "at": 17},
              {"k": "1 HẢI LÝ", "v": "≈ 1,85 KM", "at": 18}],
     "total": {"k": "ĐÈN BÁO", "v": "KHÔNG BÁO ĐANG GIỮ HƯỚNG", "at": 19}},
    {"type": "kinetic", "at": 20, "items": [{"text": "ĐÀI VÔ TUYẾN ANCHORAGE", "at": 20},
                                            {"text": "ngừng hoạt động từ 23.08.1983", "at": [20, "ngừng"], "sm": True},
                                            {"text": "CÁCH BÁM TUYẾN THƯỜNG DÙNG: KHÔNG CÓ", "at": 21, "acc": True}]},
    {"type": "counter", "at": 22, "from": 0, "to": 12, "suffix": " HẢI LÝ", "until": [22, "lệch"], "label": "LỆCH KHI NGANG TRẠM BETHEL · 49 PHÚT SAU CẤT CÁNH",
     "sub": {"text": "≈ 22 KM · ICAO 1993 MỤC 3.8 · KÊNH TỰ ĐỔI", "at": 23}},
    {"type": "kinetic", "at": 24, "items": [{"text": "ĐÁNG LẼ ĐÃ PHẢI NGHI NGỜ", "at": 24, "acc": True},
                                            {"text": "không có dấu hiệu họ nhận ra", "at": 25, "sm": True}]},
    {"type": "question", "at": 26, "text": "Ba bộ dẫn đường quán tính:\nsuốt năm tiếng, chúng ở đâu?"},
]}

# ---------------------------------------------------------------- CH02: ba bộ máy không ai giao tay lái (nấc 1)
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BA BỘ MÁY KHÔNG AI GIAO TAY LÁI"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "BA BỘ MÁY\nKHÔNG AI GIAO TAY LÁI", "sub": "DẪN ĐƯỜNG QUÁN TÍNH", "bg": "deck",
     "titleAt": [0, "theo"]},
    {"type": "ledger", "at": [0, "ba"], "title": "DẪN ĐƯỜNG QUÁN TÍNH TRÊN CHIẾC 747", "srcnote": "ICAO 1993 · MỤC 1.6.3",
     "rows": [{"k": "SỐ BỘ", "v": "3 · LITTON LTN-72R", "at": [0, "ba"]},
              {"k": "MỖI BỘ", "v": "CẢM BIẾN + MÁY TÍNH", "at": 1},
              {"k": "NỐI SÓNG RADIO ĐỂ TỰ CHỈNH", "v": "KHÔNG", "at": 2}]},
    {"type": "slam", "at": 3, "text": "< 2 HẢI LÝ / GIỜ", "sub": "SAI SỐ CỦA BỘ DẪN ĐƯỜNG QUÁN TÍNH · ICAO 1993 MỤC 2.7"},
    {"type": "kinetic", "at": 4, "items": [{"text": "BA BỘ SOI LẪN NHAU", "at": 4},
                                           {"text": "màn hình đáng lẽ đã cho thấy độ lệch", "at": 5, "sm": True},
                                           {"text": "LÁI TỰ ĐỘNG KHÔNG DO CHÚNG ĐIỀU KHIỂN", "at": 6, "acc": True}]},
    {"type": "slam", "at": 7, "text": "MÁY BIẾT ĐƯỜNG", "sub": "CHỈ LÀ KHÔNG AI GIAO TAY LÁI · ICAO 1993 KẾT LUẬN 3.11"},
    {"type": "ledger", "at": 9, "title": "ĐỘ LỆCH VỀ PHÍA BẮC", "srcnote": "ICAO 1993 · MỤC 2.8.1 · ƯỚC TỪ DỮ LIỆU BAY VÀ RADAR",
     "rows": [{"k": "NABIE", "v": "≈ 60 HẢI LÝ", "at": 10}, {"k": "NUKKS", "v": "≈ 100 HẢI LÝ", "at": [11, "hai"]},
              {"k": "NEEVA", "v": "≈ 160 HẢI LÝ", "at": [11, "ba"]}],
     "total": {"k": "≈", "v": "300 KM · KÊNH TỰ ĐỔI", "at": 12}},
    {"type": "map", "at": 13, "geo": "pac", "tag": MAPNOTE,
     "pins": [{"name": "Kamchatka", "label": "16:40–17:08 UTC · CHẶN KHÔNG THÀNH", "at": [13, "chặn"]},
              {"name": "Sakhalin", "label": "BẮT KỊP", "at": 14}],
     "routes": [{"from": "Anchorage", "to": "Kamchatka", "at": 13, "until": [13, "chặn"], "bend": 0.12},
                {"from": "Kamchatka", "to": "Sakhalin", "at": [13, "nhưng"], "until": 14, "bend": 0.1}]},
    {"type": "ledger", "at": 15, "title": "TRÊN ĐẢO SAKHALIN", "srcnote": "ICAO 1993 · MỤC 1.9.5 · TÓM TẮT KẾT LUẬN",
     "rows": [{"k": "18:20 UTC", "v": "TOKYO CHO LÊN 35.000 BỘ", "at": 15},
              {"k": "PHÍA LIÊN XÔ HIỂU", "v": "ĐỘNG TÁC NÉ TRÁNH", "at": [16, "né"]},
              {"k": "TƯỞNG LÀ", "v": "MÁY BAY TRINH SÁT RC-135", "at": [17, "trinh"]},
              {"k": "GỌI QUA TẦN SỐ CẤP CỨU", "v": "KHÔNG", "at": [18, "cấp"]}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "TIÊM KÍCH SỐ 805 · PHI CÔNG OSIPOVICH", "at": 19, "acc": True},
                                            {"text": "theo bản ghi liên lạc Liên Xô in trong báo cáo ICAO", "at": [19, "liên"], "sm": True}]},
    {"type": "quote", "at": [20, "phi"], "dy": True, "text": "Phi công tiêm kích nói ông không hề biết đó là máy bay chở khách.",
     "by": "PHI CÔNG CHIẾC 805 (OSIPOVICH, THEO BẢN GHI LIÊN LẠC) · PHỎNG VẤN DO ICAO TÓM TẮT, MỤC 1.16.1", "lbl": "DIỄN Ý", "typeAt": [20, "phi"],
     "typeAt": [20, "phi"], "typeDur": 2.6},
    {"type": "slam", "at": 21, "text": "18:26:02 UTC", "sub": "QUẢ TÊN LỬA ĐẦU TIÊN NỔ · ICAO 1993"},
    {"type": "kinetic", "at": 22, "items": [{"text": "269 NGƯỜI TRÊN MÁY BAY", "at": 22}, {"text": "không ai sống sót", "at": [22, "không"], "sm": True}]},
    {"type": "ledger", "at": 23, "title": "CÂY THƯỚC SAI SỐ", "srcnote": "PHÂN TÍCH PHÍA NGA · PHỤ LỤC D BÁO CÁO ICAO 1993 (ICAO KHÔNG THÔNG QUA)",
     "rows": [{"k": "LÚC TRÚNG TÊN LỬA", "v": "≈ 350 HẢI LÝ KHỎI R20", "at": [23, "lệch"]},
              {"k": "NẤC 1", "v": "HƠN 600 KM", "at": 24}],
     "total": {"k": "NẤC ĐẦU TIÊN", "v": "ĐÃ CHỐT", "at": 25}},
    {"type": "question", "at": 26, "text": "Sau đêm ấy,\nnước Mỹ đã làm gì?"},
]}

# ---------------------------------------------------------------- CH03: lời hứa ngày 16 tháng 9 (re-hook)
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "LỜI HỨA NGÀY 16 THÁNG 9"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "LỜI HỨA\nNGÀY 16 THÁNG 9", "sub": "NHÀ TRẮNG · 1983", "bg": "reagan_press",
     "titleAt": [0, "tám"]},
    {"type": "photo", "at": [0, "lên"], "img": "reagan_press", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "05.09.1983 · 20:00", "at": [0, "lên"]}, {"text": "TỘI ÁC CHỐNG LẠI LOÀI NGƯỜI", "at": [1, "tội"], "acc": True}],
     "label": {"k": "PHÒNG BẦU DỤC · BÀI PHÁT BIỂU VỀ KAL 007", "v": "WHITE HOUSE PHOTOGRAPHIC OFFICE", "at": 0}},
    {"type": "quote", "at": 3, "text": "The 747 is equipped with the most modern computerized navigation facilities, but a computer must respond to input provided by human hands.",
     "by": "RONALD REAGAN · DIỄN VĂN 05.09.1983 · AMERICAN PRESIDENCY PROJECT", "lbl": "TRÍCH DỊCH", "qline": 3, "typeAt": [3, "một"], "typeDur": 3.0},
    {"type": "quote", "at": 4, "text": "No one will ever know whether a mistake was made in giving the computer the course or whether there was a malfunction.",
     "by": "RONALD REAGAN · DIỄN VĂN 05.09.1983", "lbl": "TRÍCH DỊCH", "qline": 4, "typeAt": [4, "sẽ"], "typeDur": 2.8},
    {"type": "kinetic", "at": 5, "items": [{"text": "MƯỜI NĂM SAU · HỘP ĐEN", "at": 5, "sm": True}, {"text": "KHÔNG TRỤC TRẶC", "at": [5, "không"], "acc": True},
                                           {"text": "lỗi nằm ở cách dùng máy", "at": 6, "sm": True}]},
    {"type": "print", "at": 7, "img": "speakes", "tone": "bw",
     "side": {"k": "16.09.1983 · HỌP BÁO 12:30", "h": "Larry\nSpeakes", "lines": [{"text": "*phó thư ký báo chí* Nhà Trắng", "at": [8, "phó"]},
                                                                                {"text": "đọc tuyên bố, *không phải* Reagan", "at": [8, "không"]}]}},
    {"type": "quote", "at": 10, "text": "…the United States is prepared to make available to civilian aircraft the facilities of its Global Positioning System when it becomes operational in 1988.",
     "by": "TUYÊN BỐ DO LARRY SPEAKES ĐỌC · 16.09.1983 · REAGAN LIBRARY", "lbl": "TRÍCH DỊCH", "qline": 10, "typeAt": [10, "hoa"], "typeDur": 3.4},
    {"type": "slam", "at": 11, "text": "GPS", "sub": "HỆ THỐNG ĐỊNH VỊ TOÀN CẦU · GLOBAL POSITIONING SYSTEM"},
    {"type": "ledger", "at": 12, "title": "ĐỌC KỸ CÂU ẤY", "srcnote": "REAGAN LIBRARY · TUYÊN BỐ 16.09.1983",
     "rows": [{"k": "DÀNH CHO", "v": "MÁY BAY DÂN SỰ", "at": 13},
              {"k": "CHỮ “MIỄN PHÍ”", "v": "KHÔNG CÓ", "at": 14},
              {"k": "REAGAN PHÁT MINH GPS?", "v": "KHÔNG", "at": 15}]},
    {"type": "timeline", "at": 16, "items": [{"year": "1973", "text": "chương trình GPS *được duyệt*", "at": 16},
                                            {"year": "22.02.1978", "text": "vệ tinh thử nghiệm *đầu tiên*", "at": 17}]},
    {"type": "photo", "at": 18, "img": "block1", "tone": "bw", "move": "in", "veil": 0.5,
     "kin": [{"text": "1983: HỆ THỐNG CÒN DANG DỞ", "at": 18, "acc": True}, {"text": "lời hứa hẹn mốc 1988", "at": 19, "sm": True}],
     "label": {"k": "BẢN VẼ VỆ TINH GPS BLOCK I", "v": "USAF · 1979", "at": 18}},
    {"type": "kinetic", "at": 20, "items": [{"text": "MỞ MỘT HỆ THỐNG QUÂN SỰ", "at": 20, "acc": True},
                                            {"text": "cho máy bay chở dân thường", "at": [20, "cho"], "sm": True}]},
    {"type": "slam", "at": 21, "text": "CHẤM XANH", "sub": "GOOGLE MAPS · MỘT BUỔI SÁNG Ở SAKHALIN · 1983", "white": True},
    {"type": "question", "at": 22, "text": "Vì sao chấm xanh\nchưa chính xác ngay?"},
]}

# ---------------------------------------------------------------- CH04: một trăm mét cố ý (nấc 2)
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "MỘT TRĂM MÉT CỐ Ý"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "MỘT TRĂM MÉT\nCỐ Ý", "sub": "SELECTIVE AVAILABILITY", "bg": "navstar2f",
     "titleAt": [0, "mốc"]},
    {"type": "photo", "at": 1, "img": "navstar2f", "tone": "color", "move": "in", "veil": 0.5, "illus": "ẢNH MINH HỌA · VỆ TINH GPS ĐỜI SAU",
     "kin": [{"text": "VỆ TINH THẾ HỆ HAI ĐẦU TIÊN", "at": [1, "thế"], "acc": True}, {"text": "phóng 14.02.1989 · sau mốc đã hứa", "at": [1, "phóng"], "sm": True}],
     "label": {"k": "VỆ TINH GPS BLOCK IIF · KHÔNG PHẢI VỆ TINH 1989", "v": "USAF", "at": 1}},
    {"type": "slam", "at": 3, "text": "SA", "sub": "SELECTIVE AVAILABILITY · “KHẢ DỤNG CÓ CHỌN LỌC”"},
    {"type": "source", "at": 4, "source": "GPS.GOV · SELECTIVE AVAILABILITY", "ref": "TRANG CHÍNH THỨC CỦA CHÍNH PHỦ MỸ VỀ GPS",
     "snippet": "SA là [[sự cố ý làm suy giảm]] tín hiệu GPS công cộng, vì lý do an ninh quốc gia", "hlAt": [4, "suy"],
     "seal": "DỊCH TỪ TRANG GỐC", "sealAt": [4, "an"]},
    {"type": "question", "at": 5, "text": "Nhoè cỡ nào?"},
    {"type": "counter", "at": 6, "from": 100, "to": 100, "suffix": " MÉT", "label": "MÁY DẪN ĐƯỜNG Ô TÔ · KHI CÒN SA",
     "sub": {"text": "BẢN TIN NHÀ TRẮNG 01.05.2000 (OSTP)", "at": [6, "phạm"]}},
    {"type": "ledger", "at": 7, "title": "CÂY THƯỚC SAI SỐ", "srcnote": "KÊNH TỰ KẺ · NGUỒN TỪNG NẤC: ICAO 1993 · NHÀ TRẮNG 2000",
     "rows": [{"k": "NẤC 1 · 1983", "v": "HƠN 600 KM", "at": 7}, {"k": "NẤC 2 · CÒN SA", "v": "≈ 100 M", "at": [7, "thứ"]}],
     "total": {"k": "NẤC 3", "v": "?", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "HAI ĐƯỜNG CAO TỐC SONG SONG", "at": 9, "acc": True},
                                           {"text": "máy khó biết xe đang ở đường nào", "at": 10, "sm": True}]},
    {"type": "counter", "at": 11, "from": 45, "to": 45, "suffix": " MÉT", "label": "BÁN KÍNH CHỨA 95% ĐIỂM ĐO · KHI CÒN SA · 01.05.2000",
     "sub": {"text": "NOAA NGS · TRẠM CORS ERLANGER, KENTUCKY · ĐĂNG TRÊN GPS.GOV", "at": 12}},
    {"type": "kinetic", "at": 13, "items": [{"text": "DƯỚI SÂN HAY TRÊN KHÁN ĐÀI?", "at": [14, "dưới"], "acc": True},
                                            {"text": "ví dụ trên gps.gov · diễn ý", "at": 13, "sm": True}]},
    {"type": "photo", "at": 15, "img": "launch", "tone": "color", "move": "out", "veil": 0.55, "illus": VM,
     "kin": [{"text": "NHIỄU PHÁT RA TỪ CHÍNH VỆ TINH", "at": 15, "acc": True}, {"text": "người dùng không tự gỡ được", "at": 16, "sm": True}],
     "label": {"k": "PHÓNG VỆ TINH GPS IIR-21", "v": "USAF · 2009", "at": 15}},
    {"type": "timeline", "at": 18, "items": [{"year": "03.1996", "text": "văn bản Tổng thống: *bỏ SA chậm nhất 2006*", "at": 18},
                                            {"year": "MỖI NĂM", "text": "*xem xét lại* một lần", "at": 19}]},
    {"type": "question", "at": 20, "text": "Ai sẽ ký\nquyết định đó?"},
]}

# ---------------------------------------------------------------- CH05: nửa đêm ngày 1 tháng 5 (cảnh mạnh ~75%)
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "NỬA ĐÊM NGÀY 1 THÁNG 5"}, "bgm": {"mood": "epic", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "NỬA ĐÊM\nNGÀY 1 THÁNG 5", "sub": "NHÀ TRẮNG · 2000", "bg": "navstar2f",
     "titleAt": [0, "ngày"]},
    {"type": "print", "at": [0, "công"], "img": "clinton", "tone": "color",
     "side": {"k": "01.05.2000 · TUYÊN BỐ CỦA TỔNG THỐNG", "h": "Bill\nClinton", "lines": [{"text": "*Nhà Trắng* công bố", "at": [0, "công"]}]}},
    {"type": "quote", "at": 1, "text": "Today, I am pleased to announce that the United States will stop the intentional degradation of the Global Positioning System (GPS) "
                                       "signals available to the public beginning at midnight tonight.",
     "by": "BILL CLINTON · TUYÊN BỐ 01.05.2000 · CLINTON WHITE HOUSE ARCHIVES", "lbl": "TRÍCH DỊCH", "qline": 1, "typeAt": [1, "hôm"], "typeDur": 3.6},
    {"type": "kinetic", "at": 2, "items": [{"text": "CHÍNH XÁC HƠN TỚI 10 LẦN", "at": 2, "acc": True},
                                           {"text": "“free of charge” · miễn phí cho người dùng khắp thế giới", "at": [3, "miễn"], "sm": True}]},
    {"type": "slam", "at": 4, "text": "MIỄN PHÍ", "sub": "CHỮ NÀY CÓ TRONG TUYÊN BỐ 2000 · KHÔNG CÓ TRONG TUYÊN BỐ 1983"},
    {"type": "date", "at": 5, "bg": "navstar2f", "day": "SA TẮT · SAU 0 GIỜ (MIỀN ĐÔNG MỸ)", "date": "02.05.2000",
     "sub": {"text": "CÙNG LÚC TRÊN TOÀN BỘ CHÒM VỆ TINH · GPS.GOV", "at": 6}},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHÔNG AI PHẢI THAY MÁY THU", "at": 7, "acc": True}]},
    {"type": "bars", "at": 8, "title": "BÁN KÍNH CHỨA 95% ĐIỂM ĐO · TRẠM KENTUCKY", "unit": "NOAA NGS · GPS.GOV (MÉT)", "max": 50,
     "items": [{"k": "CÒN SA · 01.05.2000", "v": 45, "lbl": "45,0", "at": [8, "bốn"]}, {"k": "TẮT SA · 03.05.2000", "v": 6.3, "lbl": "6,3", "at": [8, "sáu"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "CÂY THƯỚC LẠI SẮP CO", "at": 9, "acc": True},
                                           {"text": "từ khán đài · tới từng vạch kẻ", "at": 10, "sm": True}]},
    {"type": "quote", "at": 12, "text": "…emergency teams responding to a cry for help can now determine what side of the highway they must respond to, thereby saving precious minutes.",
     "by": "BILL CLINTON · TUYÊN BỐ 01.05.2000", "lbl": "TRÍCH DỊCH", "qline": 12, "typeAt": [12, "các"], "typeDur": 3.0},
    {"type": "question", "at": 13, "text": "Ai trả giá\ncho nấc co này?"},
    {"type": "ledger", "at": 14, "title": "CÁI GIÁ CỦA QUÂN ĐỘI MỸ", "srcnote": "TUYÊN BỐ 01.05.2000 · GPS.GOV (QUYẾT ĐỊNH 09.2007)",
     "rows": [{"k": "BỎ", "v": "LÀM NHOÈ TOÀN CẦU", "at": 14},
              {"k": "THAY BẰNG", "v": "CHẶN THEO TỪNG KHU VỰC", "at": [15, "chặn"]},
              {"k": "ĐỀ XUẤT", "v": "BỘ TRƯỞNG QUỐC PHÒNG", "at": [16, "bộ"]},
              {"k": "2007", "v": "GPS III KHÔNG CÓ SA", "at": 17}]},
    {"type": "slam", "at": 18, "text": "CÒN MỘT KHOẢN GIÁ", "sub": "NẰM TRONG TÚI MỘT NHÓM NGƯỜI RẤT CỤ THỂ"},
]}

# ---------------------------------------------------------------- CH06: chấm xanh của bạn (nấc 3 + đóng vòng)
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "CHẤM XANH CỦA BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "CHẤM XANH\nCỦA BẠN", "sub": "HÔM NAY", "bg": "launch", "titleAt": [0, "hôm"]},
    {"type": "slam", "at": [0, "ghi"], "text": "≈ 5 MÉT", "sub": "ĐIỆN THOẠI · TRỜI THOÁNG · 4,9 M THEO GPS.GOV"},
    {"type": "ledger", "at": 2, "title": "CÂY THƯỚC SAI SỐ · ĐỦ BA NẤC", "srcnote": "ICAO 1993 · NHÀ TRẮNG 2000 · GPS.GOV",
     "rows": [{"k": "NẤC 1 · 1983", "v": "HƠN 600 KM", "at": 2}, {"k": "NẤC 2 · CÒN SA", "v": "≈ 100 M", "at": [2, "nấc"]},
              {"k": "NẤC 3 · HÔM NAY", "v": "≈ 5 M", "at": [2, "ba"]}],
     "total": {"k": "CHẤM XANH", "v": "ĐỨNG TRÊN CẢ BA NẤC", "at": 3}},
    {"type": "question", "at": 4, "text": "Ai trả tiền\ncho chấm xanh?"},
    {"type": "quote", "at": 7, "text": "The American taxpayer pays for the GPS service enjoyed throughout the world.",
     "by": "GPS.GOV · “WHO PAYS FOR GPS?”", "lbl": "TRÍCH DỊCH", "qline": 7, "typeAt": [7, "người"], "typeDur": 2.4},
    {"type": "kinetic", "at": 8, "items": [{"text": "KHÔNG THU PHÍ TRỰC TIẾP", "at": [8, "phí"], "acc": True},
                                           {"text": "luật và chính sách của Mỹ", "at": 8, "sm": True},
                                           {"text": "BẠN KHÔNG TRẢ · CÓ NGƯỜI TRẢ", "at": 10}]},
    {"type": "ledger", "at": 11, "title": "AI TRẢ GIÁ CHO MỖI NẤC CO", "srcnote": "REAGAN LIBRARY 1983 · TUYÊN BỐ CLINTON 2000 · GPS.GOV",
     "rows": [{"k": "HÀNG TRĂM KM", "v": "KAL 007 · LỜI HỨA 1983", "at": 12},
              {"k": "≈ 100 M → VÀI MÉT", "v": "MỸ THÔI LÀM NHOÈ", "at": 13},
              {"k": "≈ 5 M MỖI NĂM", "v": "TIỀN THUẾ CỦA NGƯỜI MỸ", "at": 14}]},
    {"type": "photo", "at": 15, "img": "reagan_desk", "tone": "bw", "move": "out", "veil": 0.55,
     "kin": [{"text": "“BÀN TAY CON NGƯỜI ĐƯA VÀO”", "at": [16, "bàn"], "acc": True}, {"text": "Reagan · 05.09.1983", "at": 16, "sm": True}],
     "label": {"k": "PHÒNG BẦU DỤC · 05.09.1983", "v": "WHITE HOUSE PHOTOGRAPHIC OFFICE", "at": 15}},
    {"type": "date", "at": 17, "day": "MÁY BÁO ĐỘNG LIÊN XÔ: “MỸ PHÓNG TÊN LỬA”", "date": "26.09.1983",
     "sub": {"text": "NGƯỜI NGỒI TRƯỚC MÀN HÌNH: STANISLAV PETROV · THEO NPR", "at": 18}},
    {"type": "kinetic", "at": 19, "items": [{"text": "THỨ SÁU NÀY", "at": 19, "acc": True}, {"text": "video tiếp theo của kênh", "at": [19, "kênh"], "sm": True}]},
    {"type": "question", "at": 20, "text": "Chấm xanh từng dắt bạn\nsang nhầm đường chưa?"},
    {"type": "kinetic", "at": 21, "items": [{"text": "LỆCH BAO XA · Ở ĐÂU", "at": 21}, {"text": "KỂ MÌNH NGHE Ở BÌNH LUẬN", "at": [21, "kể"], "acc": True}]},
]}

SPEC = {
    "title": "GOOGLE MAPS Ngoài Đời Thật: KAL 007 Và Lời Hứa GPS Của Reagan",
    "channel": "MIM", "theme": "lab", "accent": "#34d399", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["thước", "nấc", "lệch", "GPS", "miễn", "nhoè", "chấm", "hướng"],
    "say": SAY, "imgs": IMGS, "geo": GEO, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["GOOGLE MAPS Ngoài Đời Thật: KAL 007 Và Lời Hứa GPS Của Reagan",
                   "GOOGLE MAPS Ngoài Đời Thật: Ronald Reagan, KAL 007 Và Lời Hứa Mở GPS Cho Người Dân",
                   "GOOGLE MAPS Ngoài Đời Thật: Ronald Reagan Và KAL 007 — Từ Lệch 600 Km Tới Sai 5 Mét"],
        "summary": "Ngày 31/08/1983 (giờ quốc tế), chiếc Boeing 747 chuyến KAL 007 lệch dần khỏi tuyến R20 rồi bị bắn hạ gần đảo Sakhalin; mười sáu ngày sau, "
                   "Nhà Trắng của Tổng thống Ronald Reagan tuyên bố sẽ mở GPS cho máy bay dân sự, một khởi điểm của chấm xanh trên Google Maps của bạn. "
                   "Video theo một cây thước sai số co lại ba nấc: hơn 600 km năm 1983, khoảng 100 m khi tín hiệu còn bị cố ý làm nhoè, và chừng 5 m trên điện thoại hôm nay. "
                   "Mọi giờ, mọi con số lấy từ báo cáo ICAO năm 1993, văn bản của Nhà Trắng và trang chính thức gps.gov.",
        "more": ["Về nguồn: báo cáo ICAO 1993 đưa ra hai khả năng (lái tự động để quên ở chế độ giữ hướng, hoặc bật dẫn đường quán tính khi máy bay đã lệch quá 7,5 hải lý); "
                 "video nói cả hai, không chọn. Con số \"350 hải lý, hơn 600 km\" lúc trúng tên lửa là của phân tích phía Nga đính kèm báo cáo, Hội đồng ICAO không thông qua "
                 "phần kết luận của báo cáo. Tuyên bố mở GPS ngày 16/09/1983 do phó thư ký báo chí Larry Speakes đọc, nói Tổng thống đã quyết định; văn bản không có chữ "
                 "\"miễn phí\" và Reagan không phải người phát minh GPS. Con số 100 m là ví dụ máy dẫn đường ô tô trong bản tin Nhà Trắng năm 2000; 45 m và 6,3 m là số đo "
                 "của một trạm NOAA ở Kentucky. Lời phi công Liên Xô là diễn ý theo phần phỏng vấn do ICAO tóm tắt. Bản đồ đường bay là hình vẽ gần đúng của kênh."],
        "chapter_titles": {"ch00": "Mở đầu: đường bay lệch dần", "ch01": "Một con số trên la bàn", "ch02": "Ba bộ máy không ai giao tay lái",
                           "ch03": "Lời hứa ngày 16 tháng 9", "ch04": "Một trăm mét cố ý", "ch05": "Nửa đêm ngày 1 tháng 5",
                           "ch06": "Chấm xanh của bạn"},
        "sources": [
            "https://aviation-is.better-than.tv/KAL007%20ICAO%20DESTRUCTION%20OF%20KOREAN%20AIR%20LINES%20BOEING%20747.pdf",
            "https://www.presidency.ucsb.edu/documents/address-the-nation-the-soviet-attack-korean-civilian-airliner",
            "https://www.reaganlibrary.gov/research/speeches/91683c",
            "https://clintonwhitehouse4.archives.gov/textonly/WH/EOP/OSTP/html/0053_2.html",
            "https://clintonwhitehouse4.archives.gov/textonly/WH/EOP/OSTP/html/0053_4.html",
            "https://www.gps.gov/selective-availability",
            "https://archive.gps.gov/systems/gps/modernization/sa/data/",
            "https://archive.gps.gov/systems/gps/performance/accuracy/",
            "https://archive.gps.gov/policy/funding/",
            "https://www.nationalacademies.org/read/4920/chapter/85",
            "https://www.npr.org/sections/thetwo-way/2017/09/18/551792129/stanislav-petrov-the-man-who-saved-the-world-dies-at-77",
        ],
        "hashtags": ["GoogleMaps", "GPS", "KAL007", "CôngNghệQuanhTa", "MindInTheMachine"],
        "tags": ["google maps", "gps", "kal 007", "chuyến bay kal 007", "ronald reagan", "gps miễn phí", "selective availability",
                 "lịch sử gps", "công nghệ quanh ta", "lịch sử công nghệ", "định vị điện thoại", "icao"],
        "category": "28", "thumb": "t1.jpg", "playlist": "Công Nghệ Quanh Ta", "publish_at": "2026-11-18T13:00:00Z",
        "video_credits": ["Ảnh Nhà Trắng, Không quân Mỹ và NASA (phạm vi công cộng); ảnh buồng lái Boeing 747-100: Clemens Vasters, CC BY 2.0 (ghi tự động theo ảnh); "
                          "bản đồ: dữ liệu Natural Earth / world-atlas"],
    },
    "sources_internal": "Báo cáo ICAO 1993: bản quét đầy đủ 298 trang (thư LE 4/19.4-93/68, 16/07/1993) đăng lại ở aviation-is.better-than.tv, đọc bằng pdftotext ngày 23/10/2026; "
                        "chưa tìm được bản trên icao.int. Trang af.mil (mốc hoạt động đầy đủ 1995) không mở được nên không dùng.",
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
    """Kiểm neo với lines (sau script_lines.py): lỗi nếu dòng không có, từ neo không nằm trong dòng, hoặc từ neo là chữ số / chữ trong SAY."""
    bad = []
    say = {_norm(k) for k in SAY}
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
    return bad


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")
    bad = check()
    if bad:
        print("NEO LỖI:\n  " + "\n  ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
