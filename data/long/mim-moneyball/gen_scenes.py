"""Cảnh + spec cho Long MIM `mim-moneyball`.

    python data/long/mim-moneyball/gen_scenes.py
    python data/long/mim-moneyball/gen_scenes.py --standin
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).parent
TOPIC = "mim-moneyball"
TITLE = "MONEYBALL Ngoài Đời Thật: Billy Beane Và Con Số"
STANDIN = "--standin" in sys.argv

SAY = {
    "moneyball": "Mâ-nì-bôn", "billy": "Bi-li", "beane": "Bin", "oakland": "Ô-clần",
    "scott": "Xcót", "hatteberg": "Ha-tơ-bớc", "kansas": "Can-dợt", "city": "Xi-ti",
    "toronto": "Tô-rôn-tô", "american": "A-mê-ri-cần", "league": "Lích", "al": "a en",
    "obp": "ô bê pê", "walk": "uóc", "pitcher": "pít-chờ", "era": "i a rờ",
    "sabermetrics": "xây-bờ-mét-trích", "sabr": "xây-bờ", "bill": "Bin", "james": "Giêm",
    "pete": "Pít", "palmer": "Pa-mờ", "dick": "Đích", "cramer": "Crây-mờ",
    "baseball": "bây-xờ-bôn", "abstract": "áp-xờ-trắc", "paul": "Pôn", "depodesta": "Đề-pô-đét-ta",
    "harvard": "Ha-vợt", "cleveland": "Cờ-li-vờ-lần", "peter": "Pi-tờ", "brand": "Bran",
    "art": "A-t", "howe": "Hao", "alds": "a en đê ét", "alcs": "a en xê ét",
    "minnesota": "Mi-nờ-xô-ta", "twins": "Tuyn", "michael": "Mai-cồ", "lewis": "Liu-ít",
    "mlb": "em en bê", "infield": "in-phiên", "shift": "síp", "reliever": "rờ-li-vờ",
    "hitter": "hít-tờ", "home": "hôm", "run": "rân", "first": "phớt", "base": "bây-xờ",
    "general": "giê-nờ-rồ", "manager": "ma-ni-giờ", "assistant": "a-xít-tần",
    "analytics": "a-na-lí-tích", "series": "xi-ri", "world": "uổld",
}

IMGS = {
    "beane06": "File:Billy Beane 2006.jpg",
    "beane10": "File:Billy Beane - General Manager Oakland As (5964095428).jpg",
    "depo": "File:Paul DePodesta and Jimmy Haslam (36730002206).jpg",
    "coliseum": "File:Oakland Coliseum view from upper deck.jpg",
    "night": "File:Oakland Coliseum at night.jpg",
    "overhead": "File:Oakland Coliseum overhead angle, September 2024.jpg",
    "aerial": "File:Oakland Coliseum aerial view 2024.jpg",
    "tickets": "File:Oakland Coliseum ticket booths.jpg",
    "score": "File:Baseball game score.jpg",
    "card": "File:Pac bell scorecard.jpg",
}
AI_PATH = {f"ai0{n}": f"assets/long/{TOPIC}/img/ai/ai_0{n}.png" for n in range(1, 4)}
STAND = {"ai01": "card", "ai02": "night", "ai03": "score"}
if not STANDIN:
    IMGS.update({k: f"EXT:ai:{Path(v).stem}" for k, v in AI_PATH.items()})

def im(key): return STAND[key] if STANDIN and key in STAND else key

GEO = {"usa": {"countries": ["United States of America"], "context": ["Canada", "Mexico"],
    "bbox": [-126, 25, -66, 50], "pins": [
        {"name": "Oakland", "lon": -122.27, "lat": 37.80, "label": "OAKLAND"},
        {"name": "Kansas City", "lon": -94.58, "lat": 39.10, "label": "KANSAS CITY"},
        {"name": "Minnesota", "lon": -93.27, "lat": 44.98, "label": "MINNESOTA"},
    ]}}

CHAPTER_TITLES = {
    "ch00": "Một cú đánh ở hiệp chín", "ch01": "Một mùa dài hơn chuỗi thắng",
    "ch02": "Giá trị của việc lên gôn", "ch03": "Câu hỏi cũ hơn cuốn sách",
    "ch04": "Người chọn câu hỏi", "ch05": "Bộ phim và phần không được cắt gọn",
    "ch06": "Năm trận không đủ dài", "ch07": "Tấm bảng đi khắp giải đấu",
}
LEDGER = "TẤM BẢNG CHỜ MỘT LẦN LÊN GÔN"
ROWS = [
    ("HỎI", "MỘT LẦN LÊN GÔN GIẢI THÍCH ĐƯỢC GÌ?"),
    ("1 · MÙA DÀI", "TIỀN ÍT · VẪN PHẢI THẮNG"),
    ("2 · LÊN GÔN", "ĐÈN PIN · KHÔNG PHẢI BẢN ĐỒ"),
    ("3 · CÂU HỎI", "DỮ LIỆU BẮT NIỀM TIN TRẢ LỜI"),
    ("4 · TRANH LUẬN", "NHIỀU NGƯỜI CÙNG KIỂM TRA"),
    ("5 · KHUNG HÌNH", "MỞ LẠI PHẦN BỊ CẮT GỌN"),
    ("6 · SERIES", "LOẠT NGẮN · VẪN BẤT NGỜ"),
    ("7 · LAN RỘNG", "NHÌN KỸ TRƯỚC KHI CHỌN"),
]
VM, AIL = "VIDEO MINH HỌA", "ẢNH MINH HỌA"

def chapter(no, k, title, sub, bg, title_at): return {"type":"chapter","no":str(no),"k":k,"title":title,"sub":sub,"bg":im(bg),"titleAt":title_at}
def photo(img, at, key, value, kin=None, illus=None):
    out={"type":"photo","at":at,"img":im(img),"tone":"bw","move":"in","veil":.55,"label":{"k":key,"v":value,"at":at}}
    if illus or img.startswith("ai"): out["illus"]=illus or AIL
    if img.startswith("ai") and not STANDIN: out["credit"]=False
    if kin: out["kin"]=[{"text":kin,"at":at,"acc":True}]
    return out
def broll(vid, at, text): return {"type":"broll","at":at,"vid":vid,"veil":.62,"illus":VM,"kin":[{"text":text,"at":at,"acc":True}]}
def kinetic(at,text,small=None):
    items=[{"text":text,"at":at,"acc":True}]
    if small: items.append({"text":small,"at":at,"sm":True})
    return {"type":"kinetic","at":at,"items":items}
def slam(at,text,sub): return {"type":"slam","at":at,"text":text,"sub":sub}
def date(at,day,d,sub): return {"type":"date","at":at,"day":day,"date":d,"sub":{"text":sub,"at":at}}
def print_scene(img,at,head,key,value): return {"type":"print","at":at,"img":im(img),"tone":"bw","head":head,"side":{"k":key,"h":value,"lines":[{"text":value.replace("\n"," · "),"at":at}]}}
def ledger(n,at): return {"type":"ledger","at":at,"title":LEDGER,"srcnote":"MỖI CHƯƠNG THÊM MỘT Ô","rows":[{"k":k,"v":v,"at":at} for k,v in ROWS[:n]]}
def question(at,text): return {"type":"question","at":at,"text":text}
def counter(at,to,suffix,label,frm=0,year=False): return {"type":"counter","at":at,"from":frm,"to":to,"suffix":suffix,"label":label,"year":year}
def timeline(at,bg,items): return {"type":"timeline","at":at,"bg":im(bg),"items":[{"year":y,"text":t} for y,t in items]}
def org(at,nodes): return {"type":"org","at":at,"nodes":nodes}
def a(line,word): return [line,word]

def ch00(): return [
 chapter(0,"MỞ ĐẦU","MỘT CÚ ĐÁNH\nỞ HIỆP CHÍN","04.09.2002 · OAKLAND 12–11 KANSAS CITY","night",a(0,"oakland")),
 date(a(0,"2002"),"OAKLAND · KANSAS CITY","04.09.2002","TRẬN THẮNG THỨ 20 LIÊN TIẾP"),
 slam(a(1,"11"),"11–0","OAKLAND DẪN SAU BA HIỆP"),
 {"type":"map","at":a(2,"kansas"),"geo":"usa","tag":"VỊ TRÍ GẦN ĐÚNG","pins":[{"name":"Oakland","at":a(2,"kansas")},{"name":"Kansas City","at":a(2,"kansas")}]},
 photo("ai02",a(2,"sân"),"HIỆP CHÍN","CHUỖI THẮNG CÓ THỂ ĐỨT",illus=AIL),
 print_scene("score",a(3,"hatteberg"),"ĐẦU HIỆP CHÍN","SCOTT HATTEBERG","VÀO SÂN ĐÁNH THAY"),
 kinetic(a(4,"home"),"HOME RUN","CHẠY TRỌN VÒNG VỀ NHÀ · GHI ĐIỂM"),
 slam(a(5,"12"),"12–11","OAKLAND THẮNG"),
 timeline(a(7,"20"),"coliseum",[("13.08","THẮNG TORONTO 5–4"),("04.09","THẮNG KANSAS CITY 12–11")]),
 ledger(1,a(10,"bảng")), question(a(11,"mùa"),"MỘT CÚ ĐÁNH GIẢI THÍCH\nĐƯỢC CẢ MÙA KHÔNG?")]

def ch01(): return [
 chapter(1,"CHƯƠNG MỘT","MỘT MÙA DÀI HƠN\nCHUỖI THẮNG","2002 · 103 THẮNG · 59 THUA","overhead",a(0,"oakland")),
 counter(a(0,"103"),103," THẮNG","MÙA THƯỜNG 2002",frm=0),
 slam(a(0,"59"),"103–59","ĐỨNG ĐẦU AL WEST"),
 timeline(a(1,"20"),"aerial",[("TRƯỚC CHUỖI","20–26"),("PHẦN CÒN LẠI","83–33")]),
 counter(a(3,"40"),40," TRIỆU USD","QUỸ LƯƠNG OAKLAND · XẤP XỈ",frm=0),
 kinetic(a(3,"28"),"THỨ 28 TOÀN GIẢI","NGUỒN LỰC KHÔNG GIỐNG CÁC ĐỘI GIÀU"),
 broll("7552614",a(5,"phẩm"),"MỘT CUỘC HỌP MINH HỌA · KHÔNG PHẢI OAKLAND"),
 print_scene("card",a(6,"800"),"TỔNG MÙA THƯỜNG","800 ĐIỂM CHẠY","654 ĐIỂM CHẠY ĐỂ LỌT"),
 question(a(8,"đêm"),"MỘT ĐÊM HAY MỘT CHỈ SỐ\nCÓ ĐỦ KHÔNG?"),
 ledger(2,a(10,"bảng")), kinetic(a(11,"giá"),"ĐO GIÁ TRỊ KỸ HƠN","OAKLAND ĐANG TÌM GÌ?")]

def ch02(): return [
 chapter(2,"CHƯƠNG HAI","GIÁ TRỊ CỦA\nVIỆC LÊN GÔN","OAKLAND 2002 · OBP .339","score",a(0,"moneyball")),
 kinetic(a(1,"obp"),"OBP","TỶ LỆ CẦU THỦ LÊN ĐƯỢC GÔN"),
 org(a(3,"loại"),[{"id":"hit","t":"CÚ ĐÁNH HỢP LỆ","s":"LÊN GÔN","at":a(1,"đánh")},{"id":"walk","t":"WALK","s":"PITCHER NÉM SAI VÙNG","p":"hit","at":a(2,"walk")}]),
 counter(a(4,"339"),339," PHẦN NGHÌN","OBP TOÀN ĐỘI · THỨ BA AL",frm=0),
 photo("beane06",a(5,"thần"),"MỘT CHỈ SỐ","KHÔNG PHẢI THẦN CHÚ"),
 print_scene("card",a(6,"hatteberg"),"SCOTT HATTEBERG","68 WALK","THỨ HAI ĐỘI"),
 counter(a(8,"88"),88," LẦN","XUẤT PHÁT Ở FIRST BASE",frm=0),
 broll("35557009",a(9,"đóng"),"MỘT SÂN BÓNG · MỘT VAI TRÒ MỚI"),
 slam(a(10,"68"),"ERA 3,68","THỨ BA TOÀN MLB"),
 ledger(3,a(12,"bảng")), question(a(13,"oakland"),"VÌ SAO NGƯỜI TA BẮT ĐẦU\nDÙNG NHỮNG ĐÈN PIN NÀY?")]

def ch03(): return [
 chapter(3,"CHƯƠNG BA","CÂU HỎI CŨ HƠN\nCUỐN SÁCH","1974 → 1980 · SABERMETRICS","card",a(0,"sabermetrics")),
 kinetic(a(0,"sabermetrics"),"SABERMETRICS","TÌM KIẾM TRI THỨC KHÁCH QUAN VỀ BÓNG CHÀY"),
 timeline(a(1,"1974"),"score",[("1974","STATISTICAL ANALYSIS COMMITTEE"),("1977","BASEBALL ABSTRACT ĐẦU TIÊN"),("1980","ĐẶT TÊN SABERMETRICS")]),
 print_scene("card",a(2,"1974"),"BA NGƯỜI ĐỒNG LẬP","BILL JAMES · PETE PALMER","DICK CRAMER"),
 date(a(4,"1977"),"BASEBALL ABSTRACT ĐẦU TIÊN","1977","BILL JAMES TỰ XUẤT BẢN"),
 slam(a(5,"1980"),"1980","TÊN GỌI SABERMETRICS XUẤT HIỆN"),
 kinetic(a(6,"thống"),"CHẤT VẤN THƯỚC ĐO QUEN THUỘC","BATTING AVERAGE · SỐ TRẬN THẮNG CỦA PITCHER"),
 photo("ai01",a(7,"lâu"),"TRỰC GIÁC","KHÔNG BỊ CHẾ GIỄU",illus=AIL),
 question(a(9,"hỏi"),"DỮ LIỆU GIÚP TA\nCÓ CÂU HỎI GÌ?"),
 ledger(4,a(11,"bảng")), broll("5726611",a(12,"ngân"),"MINH HỌA MỘT CUỘC THẢO LUẬN")]

def ch04(): return [
 chapter(4,"CHƯƠNG BỐN","NGƯỜI CHỌN\nCÂU HỎI","1999 → 2002 · OAKLAND","beane10",a(0,"billy")),
 photo("beane06",a(0,"general"),"BILLY BEANE","GENERAL MANAGER · OAKLAND"),
 date(a(1,"2003"),"SÁCH MONEYBALL","2003","KỂ VỀ MÙA 2002 CỦA OAKLAND"),
 photo("depo",a(3,"depodesta"),"PAUL DEPODESTA","ASSISTANT GENERAL MANAGER · 1999"),
 timeline(a(4,"harvard"),"card",[("1996","THỰC TẬP Ở CLEVELAND"),("1999","GIA NHẬP ATHLETICS")]),
 broll("5182638",a(5,"hai"),"GẬY, BÓNG VÀ HÀNG RÀO"),
 slam(a(6,"cảm"),"THÔNG TIN KHÔNG HOÀN HẢO","NHIỀU NGƯỜI CÙNG TRANH LUẬN"),
 kinetic(a(8,"cụ"),"TRANH LUẬN CỤ THỂ HƠN","KHÔNG PHẢI KHẨU HIỆU"),
 ledger(5,a(9,"bảng")), question(a(10,"điện"),"PHIÊN BẢN ĐIỆN ẢNH\nĐÃ LÀM GỌN ĐIỀU GÌ?")]

def ch05(): return [
 chapter(5,"CHƯƠNG NĂM","BỘ PHIM VÀ PHẦN\nKHÔNG ĐƯỢC CẮT GỌN","2003 · SÁCH | 2011 · PHIM","tickets",a(0,"2011")),
 timeline(a(0,"2011"),"card",[("2002","MÙA OAKLAND"),("2003","SÁCH MONEYBALL"),("2011","PHIM MONEYBALL")]),
 kinetic(a(1,"peter"),"PETER BRAND LÀ HƯ CẤU","DỰA MỘT PHẦN TRÊN NỀN TẢNG CỦA DEPODESTA"),
 photo("depo",a(3,"depodesta"),"PAUL DEPODESTA","KHÔNG CHO DÙNG TÊN THẬT TRONG PHIM"),
 question(a(3,"ý"),"ĐIỆN ẢNH CÔ ĐẶC Ý TƯỞNG\nHAY GHI LẠI LỊCH SỬ?"),
 slam(a(5,"dữ"),"KỊCH TÍNH HÓA","THEO WASHINGTON POST"),
 print_scene("beane10",a(7,"art"),"ART HOWE","MANAGER NĂM 2002","103 THẮNG · VÔ ĐỊCH AL WEST"),
 org(a(8,"obp"),[{"id":"obp","t":"OBP .339","s":"TOÀN ĐỘI","at":a(8,"obp")},{"id":"era","t":"ERA 3,68","s":"PITCHING","p":"obp","at":a(8,"era")},{"id":"mgr","t":"ART HOWE","s":"LỊCH ĐẤU DÀI","p":"era","at":a(8,"manager")}]),
 kinetic(a(10,"tổ"),"DỮ LIỆU · TỔ CHỨC · CON NGƯỜI","CÁC MẢNH GHÉP CÙNG TỒN TẠI"),
 ledger(6,a(11,"bảng")), question(a(12,"mô"),"MỘT MÔ HÌNH CÓ HỨA\nXÓA HẾT GIỚI HẠN KHÔNG?")]

def ch06(): return [
 chapter(6,"CHƯƠNG SÁU","NĂM TRẬN\nKHÔNG ĐỦ DÀI","ALDS 2002 · OAKLAND GẶP MINNESOTA","coliseum",a(0,"103")),
 {"type":"map","at":a(0,"minnesota"),"geo":"usa","tag":"VỊ TRÍ GẦN ĐÚNG","pins":[{"name":"Oakland","at":a(0,"minnesota")},{"name":"Minnesota","at":a(0,"minnesota")}]},
 kinetic(a(1,"alds"),"ALDS","CẢ MÙA DÀI NÉN VÀO MỘT SERIES NGẮN"),
 slam(a(2,"7"),"7–5","MINNESOTA THẮNG TRẬN MỘT"),
 print_scene("score",a(2,"sau"),"TRẬN MỘT","OAKLAND TỪNG DẪN","5–1"),
 timeline(a(3,"hai"),"night",[("TRẬN 2","OAKLAND THẮNG"),("TRẬN 3","OAKLAND THẮNG"),("TRẬN 4","MINNESOTA THẮNG")]),
 slam(a(4,"năm"),"1–5","OAKLAND THUA TRẬN QUYẾT ĐỊNH"),
 kinetic(a(5,"alcs"),"KHÔNG VÀO ALCS","KHÔNG PHỦ ĐỊNH MÙA 103 THẮNG"),
 broll("8275595",a(8,"biến"),"MINH HỌA MỘT KHOẢNH KHẮC CÓ THỂ ĐỔI CHIỀU"),
 question(a(10,"công"),"MỘT CÔNG THỨC CÓ THỂ\nHỨA KẾT QUẢ NĂM TRẬN?"),
 kinetic(a(11,"cải"),"XÁC SUẤT TỐT HƠN","TRONG DÀI HẠN"),   # Claude 26/10: question kéo 20 s -> thêm cảnh cho câu 11-13
 slam(a(12,"cam"),"KHÔNG CAM KẾT","CHO NĂM TRẬN KẾ TIẾP"),
 kinetic(a(13,"cúp"),"KHÔNG PHẢI CHIẾC CÚP TẤT YẾU","MÙA 2002 KỂ CHO ĐÚNG"),
 ledger(7,a(14,"bảng")), photo("ai02",a(16,"oakland"),"MÙA THƯỜNG XUẤT SẮC","SERIES NGẮN THẤT BẠI",illus=AIL)]

def ch07(): return [
 chapter(7,"CHƯƠNG BẢY","TẤM BẢNG ĐI\nKHẮP GIẢI ĐẤU","THẬP NIÊN 1990 → HIỆN ĐẠI","aerial",a(0,"michael")),
 photo("ai03",a(0,"dữ"),"CÁC CÂU LẠC BỘ","NGÀY CÀNG ÁP DỤNG CÁCH TIẾP CẬN DỰA TRÊN DỮ LIỆU",illus=AIL),
 kinetic(a(2,"shift"),"INFIELD SHIFT","BỐ TRÍ PHÒNG NGỰ THEO XU HƯỚNG ĐÁNH BÓNG"),
 org(a(3,"reliever"),[{"id":"rel","t":"RELIEVER","s":"NÉM MẠNH HƠN","at":a(3,"reliever")},{"id":"hit","t":"HITTER","s":"KIÊN NHẪN · CÓ SỨC MẠNH","p":"rel","at":a(3,"hitter")}]),
 slam(a(5,"oakland"),"XU HƯỚNG TOÀN GIẢI","KHÔNG PHẢI CÔNG LAO RIÊNG CỦA OAKLAND"),
 broll("7691559",a(6,"analytics"),"MINH HỌA PHÂN TÍCH TRONG MỘT PHÒNG HỌP"),
 kinetic(a(7,"so"),"ĐO · SO SÁNH · THỬ LẠI","ĐIỀU HIỂN NHIÊN CŨNG CẦN KIỂM CHỨNG"),
 timeline(a(8,"1990"),"overhead",[("1990s","ANALYTICS BẮT ĐẦU"),("ĐẦU 2000s","MONEYBALL XUẤT HIỆN")]),
 question(a(10,"hạn"),"TA ĐANG BỎ SÓT ĐIỀU GÌ\nCHỈ VÌ CHƯA ĐO ĐÚNG?"),
 date(a(11,"2002"),"HATTEBERG HOME RUN","04.09.2002","12–11 · TRẬN THẮNG THỨ 20"),
 ledger(8,a(13,"tám")), kinetic(a(14,"quyết"),"NHÌN KỸ HƠN","TRƯỚC KHI QUYẾT ĐỊNH")]

SCENES=[ch00,ch01,ch02,ch03,ch04,ch05,ch06,ch07]
SOURCES=[
 "https://www.mlb.com/athletics/news/athletics-to-celebrate-10th-anniversary-of-20-game-winning-streak/c-36661928",
 "https://www.mlb.com/athletics/news/twenty-wins-20-ways-to-win/c-121624",
 "https://www.baseball-reference.com/teams/OAK/2002.shtml", "https://www.mlb.com/news/ten-years-later-the-as-are-back/c-37848808",
 "https://sabr.org/sabermetrics", "https://sabr.org/50at50/analytics", "https://apnews.com/article/e67c9d939d0c27f65c5785de3a4fed10",
 "https://www.washingtonpost.com/sports/nationals/moneyball-is-compelling-but-leaves-out-much-of-the-real-story/2011/10/11/gIQAMA1cdL_story.html",
 "https://www.mlb.com/news/2002-twins-a-s-alds-recap.html", "https://www.mlb.com/news/sabermetrics-in-baseball-a-casual-fans-guide"]

def make_spec(): return {"topic":TOPIC,"title":TITLE,"channel":"MIM","theme":"lab","look":"steel","accent":"#f59e0b","master":True,"beat2":True,"say":SAY,"imgs":IMGS,"geo":GEO,"chapters":[f"ch{i:02d}" for i in range(len(SCENES))],"youtube":{
 "titles":[TITLE,"Billy Beane 2002: Moneyball Không Chỉ Là OBP","Moneyball 2002: Một Con Số Không Đủ Để Thắng"],"publish_at":"2026-11-27T13:00:00Z","playlist":"Công Nghệ Quanh Ta","category":"28","thumb":"t1.jpg",
 "summary":"Moneyball thường được nhớ như câu chuyện một đội bóng ít tiền dùng dữ liệu để đi ngược số đông. Nhưng mùa Oakland 2002 không gói trong một chỉ số hay một cú home run. Từ chuỗi 20 trận thắng, OBP và pitching, tới nền sabermetrics của Bill James, Billy Beane, Paul DePodesta, Art Howe và thất bại ở ALDS, video mở lại những phần đời thật thường bị bản kể gọn bỏ qua.",
 "more":["Phim Moneyball chỉ được nhắc bằng lời và chữ; video không sử dụng hình ảnh, âm thanh hoặc trích đoạn từ phim.","Các clip Pexels có nhãn VIDEO MINH HỌA và không mô tả một người hay sự kiện cụ thể.","Một số hình là tranh minh họa nhằm diễn đạt ý tưởng, không phải ảnh tư liệu."],"chapter_titles":CHAPTER_TITLES,"sources":SOURCES,
 "tags":["Moneyball","Billy Beane","Oakland Athletics","sabermetrics","baseball analytics","OBP","Bill James","Paul DePodesta","Art Howe","Scott Hatteberg","lịch sử công nghệ","dữ liệu"],"hashtags":["Moneyball","BaseballAnalytics","CôngNghệQuanhTa","MindInTheMachine"],"video_credits":["Ảnh Billy Beane, Paul DePodesta và Oakland Coliseum: Wikimedia Commons, CC BY hoặc Public domain.","Video minh họa: Pexels.","Tranh minh họa: tạo theo prompt nội bộ của kênh."],},"sources_internal":"Chỉ dùng kho facts.md đã duyệt. Ảnh Commons I01–I10: CC BY hoặc Public domain. Ba tranh minh họa chờ chủ kênh tạo theo ai_prompts.md."}

import re as _re


def _anchors(node, out):
    if isinstance(node, dict):
        for v in node.values():
            _anchors(v, out)
    elif isinstance(node, list):
        if len(node) == 2 and isinstance(node[0], int) and isinstance(node[1], str):
            out.append(node)
        else:
            for v in node:
                _anchors(v, out)


def fix_anchors(scenes, lines):
    """Neo [i, "từ"] mà "từ" là chữ số -> đổi sang chữ (không phải số) gần con số nhất trong câu i, chưa có cảnh nào
    neo vào (Claude 26/10/2026: "11" không khớp "11–0"; hai cảnh cùng một mốc thì engine báo "quá ngắn")."""
    found = []
    _anchors(scenes, found)
    toks = []
    for ln in lines:
        txt = ln if isinstance(ln, str) else ln.get("t", "")
        toks.append([_re.sub(r"[^\wÀ-ỹ]", "", w).lower() for w in txt.split()])
    seen = set()
    for x in found:                     # neo chữ không có trong câu (lệch sau khi tách câu): tìm câu gần nhất ±2
        if id(x) in seen or _re.search(r"\d", x[1]) or x[0] >= len(toks) or x[1].lower() in toks[x[0]]:
            seen.add(id(x)); continue
        for d in (1, -1, 2, -2):
            k = x[0] + d
            if 0 <= k < len(toks) and x[1].lower() in toks[k]:
                x[0] = k
                break
        seen.add(id(x))
    used = {(x[0], x[1]) for x in found if not _re.search(r"\d", x[1])}
    for x in found:
        if not _re.search(r"\d", x[1]) or x[0] >= len(lines):
            continue
        txt = lines[x[0]] if isinstance(lines[x[0]], str) else lines[x[0]].get("t", "")
        words = [_re.sub(r"[^\wÀ-ỹ]", "", w).lower() for w in txt.split()]
        k = next((j for j, w in enumerate(words) if x[1] in w), len(words))
        order = list(range(k - 1, -1, -1)) + list(range(k + 1, len(words)))   # gần con số trước, rồi phía sau
        for j in order:
            w = words[j]
            if w and not _re.search(r"\d", w) and (x[0], w) not in used:
                x[1] = w
                used.add((x[0], w))
                break
    return scenes


# Claude 26/10/2026: đã tách câu > 35 tiếng (ch01 câu 7, ch02 câu 1, ch07 câu 10) -> câu phía sau lùi 1
SPLIT = {1: 7, 7: 10}   # ch02 sửa neo trực tiếp trong ch02()


def shift_anchors(scenes, ch):
    if ch not in SPLIT:
        return scenes
    found = []
    _anchors(scenes, found)
    seen = set()
    for x in found:
        if id(x) not in seen and x[0] > SPLIT[ch]:   # cùng một list neo có thể được tham chiếu 2 lần
            x[0] += 1
        seen.add(id(x))
    return scenes


def main():
 spec=make_spec(); (ROOT/"spec.json").write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 for i,build_scenes in enumerate(SCENES):
  f=ROOT/f"ch{i:02d}.json"; out=json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
  out.update({"topic":TOPIC,"chapter":i,"hud":{"k":f"CHƯƠNG {i:02d}","t":CHAPTER_TITLES[f"ch{i:02d}"].upper()},"scenes":fix_anchors(shift_anchors(build_scenes(),i),out.get("lines",[]))})
  f.write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
 print(f"Đã tạo spec.json và {len(SCENES)} chương cho {TOPIC}"+(" (BẢN THAY TẠM ẢNH AI — đừng render)" if STANDIN else "."))
if __name__=="__main__": main()
