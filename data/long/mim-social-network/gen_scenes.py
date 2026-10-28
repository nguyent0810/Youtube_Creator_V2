"""Cảnh + spec cho Long MIM `mim-social-network`."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).parent
TOPIC = "mim-social-network"
TITLE = "MẠNG XÃ HỘI Ngoài Đời Thật: Mark Zuckerberg"
STANDIN = "--standin" in sys.argv

SAY = {
 "mark":"Mác", "zuckerberg":"Dúc-cơ-bớc", "harvard":"Ha-vợt", "crimson":"Crim-dần", "facemash":"Phâys-mét",
 "facebook":"Phây-xờ-búc", "thefacebook":"Đờ Phây-xờ-búc", "kirkland":"Kớc-lần", "columbia":"Cờ-lăm-bi-a", "stanford":"Xtan-phợt", "yale":"Dâyl",
 "coursematch":"Coóc-mét", "palo":"Pa-lô", "alto":"An-tô", "dustin":"Đớt-tin", "moskovitz":"Mót-cô-vít", "andrew":"An-đriu", "mccollum":"Mơ-cô-lầm",
 "eduardo":"Ê-đu-a-đô", "saverin":"Xa-vơ-rin", "cfo":"xi ép ô", "cameron":"Ca-mơ-rần", "tyler":"Tai-lờ", "winklevoss":"Uyn-cồ-vót", "divya":"Đíp-ya", "narendra":"Na-ren-đờ-ra", "connectu":"Cờ-nét-u",
 "netflix":"Nét-phlích", "david":"Đa-vít", "fincher":"Phin-chờ", "jesse":"Je-xi", "eisenberg":"Ai-xần-bớc", "garfield":"Ga-phiu", "meta":"Me-ta", "feed":"phít", "elo":"Ê-lô", "inventory":"in-ven-tơ-ri", "signals":"xích-nồ", "predictions":"pờ-rờ-đích-shần", "relevancy":"rê-lơ-vần-xi"
}
IMGS = {
 "mark":"File:MarkZuckerberg.jpg", "memorial07":"File:Harvard_memorial_hall.jpg", "memorial16":"File:Memorial Hall, Harvard.jpg",
 "memorial24":"File:HarvardMemorialHall24June07.jpg", "chapel":"File:Harvard Yard chapel.jpg", "yard":"File:Harvard Yard, Harvard University, Cambridge MA.jpg",
 "weld":"File:Weld Hall - Harvard University.jpg", "hall":"File:Harvard Hall - Harvard University.jpg", "campus":"File:Harvard University.jpg"
}
AI_PATH={f"ai0{i}":f"assets/long/{TOPIC}/img/ai/ai_0{i}.png" for i in range(1,5)}
STAND={"ai01":"weld","ai02":"hall","ai03":"yard","ai04":"campus"}
if not STANDIN: IMGS.update({k:f"EXT:ai:{Path(v).stem}" for k,v in AI_PATH.items()})
def im(k): return STAND[k] if STANDIN and k in STAND else k
GEO={"boston":{"countries":["United States of America"],"context":["Canada","Mexico"],"bbox":[-71.22,42.25,-70.95,42.47],"pins":[{"name":"Harvard","lon":-71.1167,"lat":42.3770,"label":"HARVARD"}]}}
CHAPTER_TITLES={"ch00":"Một trang bị tắt","ch01":"Cánh cửa kỷ luật","ch02":"Một danh bạ có lối vào","ch03":"Đường nối ra ngoài trường","ch04":"Những vai trò đầu tiên","ch05":"Một tranh chấp có hồ sơ","ch06":"Phim không phải hồ sơ","ch07":"Ai đứng ở đầu Feed"}
LEDGER="BẢN ĐỒ KẾT NỐI"
ROWS=[("MỞ ĐẦU","SO CẶP ẢNH"),("1 · QUY TẮC","CỬA KỶ LUẬT"),("2 · CỔNG VÀO","EMAIL TRƯỜNG"),("3 · MỞ RỘNG","LỚP HỌC CHUNG"),("4 · VAI TRÒ","VỐN VÀ QUẢNG CÁO"),("5 · HỒ SƠ","CÁO BUỘC KHÁC ÁN"),("6 · PHIM","KHÔNG LÀ HỒ SƠ"),("7 · FEED","THỨ TỰ NỘI DUNG")]
VM,AIL="VIDEO MINH HỌA","ẢNH MINH HỌA"
def a(line,word): return [line,word]
def chapter(no,k,title,sub,bg,at): return {"type":"chapter","no":str(no),"k":k,"title":title,"sub":sub,"bg":im(bg),"titleAt":at}
def photo(img,at,key,value,kin=None):
 o={"type":"photo","at":at,"img":im(img),"tone":"bw","move":"in","veil":.55,"label":{"k":key,"v":value,"at":at}}
 if img.startswith("ai"): o.update({"illus":AIL,"credit":False})
 if kin:o["kin"]=[{"text":kin,"at":at,"acc":True}]
 return o
def broll(vid,at,text): return {"type":"broll","at":at,"vid":vid,"veil":.62,"illus":VM,"kin":[{"text":text,"at":at,"acc":True}]}
def kinetic(at,text,small=None): return {"type":"kinetic","at":at,"items":[{"text":text,"at":at,"acc":True}]+([{"text":small,"at":at,"sm":True}] if small else [])}
def slam(at,text,sub): return {"type":"slam","at":at,"text":text,"sub":sub}
def date(at,day,d,sub): return {"type":"date","at":at,"day":day,"date":d,"sub":{"text":sub,"at":at}}
def print_scene(img,at,head,key,value): return {"type":"print","at":at,"img":im(img),"tone":"bw","head":head,"side":{"k":key,"h":value,"lines":[{"text":value,"at":at}]}}
def ledger(n,at): return {"type":"ledger","at":at,"title":LEDGER,"srcnote":"MỖI CHƯƠNG THÊM MỘT ĐƯỜNG","rows":[{"k":k,"v":v,"at":at} for k,v in ROWS[:n]]}
def question(at,text): return {"type":"question","at":at,"text":text}
def counter(at,to,suffix,label,frm=0,year=False): return {"type":"counter","at":at,"from":frm,"to":to,"suffix":suffix,"label":label,"year":year}
def timeline(at,bg,items): return {"type":"timeline","at":at,"bg":im(bg),"items":[{"year":y,"text":t} for y,t in items]}
def org(at,nodes): return {"type":"org","at":at,"nodes":nodes}

def ch00(): return [
 chapter(0,"MỞ ĐẦU","MỘT TRANG\nBỊ TẮT","04.11.2003 · FACEMASH","memorial07",a(0,"facemash")),
 date(a(0,"crimson"),"HARVARD CRIMSON","04.11.2003","MỘT TRANG VỪA BỊ TẮT"),
 photo("mark",a(1,"mark"),"NGƯỜI LẬP TRANG","MARK E. ZUCKERBERG"),
 photo("ai01",a(1,"harvard"),"PHÒNG KÝ TÚC XÁ","MINH HỌA BỐI CẢNH"),
 photo("ai02",a(2,"facemash"),"CƠ CHẾ","SO HAI ẢNH NGẪU NHIÊN"),
 org(a(3,"house"),[{"id":"house","t":"HOUSE","s":"DANH BẠ ẢNH","at":a(3,"house")},{"id":"pair","t":"SO CẶP","s":"HAI ẢNH","p":"house","at":a(3,"house")}]),
 kinetic(a(4,"giao"),"KHÔNG PHẢI MẠNG XÃ HỘI","MỘT GIAO DIỆN ÉP CHỌN"),
 broll("946146",a(5,"gom"),"GÕ BÀN PHÍM MINH HỌA · KHÔNG PHẢI SỰ KIỆN THẬT"),
 counter(a(8,"450"),450," KHÁCH","THEO ZUCKERBERG VỚI CRIMSON"),
 counter(a(8,"22000"),22000," LƯỢT","Ít NHẤT · THEO CRIMSON"),
 ledger(1,a(13,"bản")),question(a(14,"thiên"),"AI ĐÃ BỊ ĐƯA VÀO\nHỆ THỐNG NÀY?")]
def ch01(): return [
 chapter(1,"CHƯƠNG MỘT","CÁNH CỬA\nKỶ LUẬT","FACEMASH · QUY TẮC · ĐỒNG Ý","memorial16",a(0,"facemash")),
 counter(a(1,"20000"),20000," LƯỢT","TRONG 24 GIỜ · THEO CRIMSON"),
 print_scene("chapel",a(2,"administrative"),"HARVARD COLLEGE","ADMINISTRATIVE BOARD","CƠ QUAN KỶ LUẬT"),
 photo("ai03",a(3,"harvard"),"PHẢN ỨNG","MINH HỌA KHUÔN VIÊN ĐÊM"),
 kinetic(a(4,"đơn"),"HỒ SƠ TỐ TỤNG","KHÔNG PHẢI PHÁN QUYẾT"),
 timeline(a(6,"crimson"),"yard",[("2003","PHÁT BIỂU VỚI CRIMSON"),("2014","CRIMSON NHÌN LẠI")]),
 slam(a(8,"động"),"KHÔNG SUY DIỄN","TỪ MỘT PHÁT BIỂU"),
 org(a(10,"danh"),[{"id":"access","t":"GIỚI HẠN","s":"DANH BẠ","at":a(10,"danh")},{"id":"compare","t":"SO SÁNH","s":"NGỮ CẢNH MỚI","p":"access","at":a(10,"danh")}]),
 ledger(2,a(11,"bản")),question(a(12,"dữ"),"DỮ LIỆU ĐƯỢC LẤY\nVÀ ĐẶT CON NGƯỜI Ở ĐÂU?")]
def ch02(): return [
 chapter(2,"CHƯƠNG HAI","MỘT DANH BẠ\nCÓ LỐI VÀO","04.02.2004 · KIRKLAND HOUSE","weld",a(0,"thefacebook")),
 print_scene("hall",a(1,"house"),"DANH BẠ HOUSE","ẢNH VÀ SỐ ĐIỆN THOẠI","GIỚI HẠN TRUY CẬP"),
 kinetic(a(2,"ngăn"),"CÁC NGĂN RIÊNG","THÔNG TIN ĐÃ TỒN TẠI"),
 date(a(3,"thefacebook"),"KIRKLAND HOUSE","04.02.2004","THEFACEBOOK ĐI VÀO HOẠT ĐỘNG"),
 {"type":"map","at":a(3,"kirkland"),"geo":"boston","tag":"VỊ TRÍ GẦN ĐÚNG","pins":[{"name":"Harvard","at":a(3,"kirkland")}]},
 photo("mark",a(4,"harvard"),"CỔNG VÀO","BAN ĐẦU CHỈ HARVARD"),
 slam(a(5,"email"),"HARVARD.EDU","ĐIỀU KIỆN ĐĂNG KÝ"),
 counter(a(7,"650"),650," NGƯỜI","24 GIỜ ĐẦU"),
 counter(a(8,"4300"),4300," TÀI KHOẢN","HAI TUẦN ĐẦU"),
 org(a(10,"hồ"),[{"id":"profile","t":"HỒ SƠ","s":"MỘT NGƯỜI","at":a(10,"hồ")},{"id":"network","t":"MẠNG","s":"NGƯỜI QUEN","p":"profile","at":a(10,"hồ")}]),
 ledger(3,a(12,"bản")),question(a(13,"cổng"),"CỔNG NÀY CÓ ĐI QUA\nĐƯỢC TRƯỜNG KHÁC KHÔNG?")]
def ch03(): return [
 chapter(3,"CHƯƠNG BA","ĐƯỜNG NỐI\nRA NGOÀI TRƯỜNG","03–06.2004 · MỞ RỘNG","campus",a(0,"columbia")),
 timeline(a(1,"10000"),"yard",[("03.2004","10.000 ĐĂNG KÝ"),("05.2004","GẦN 100.000 NGƯỜI")]),
 kinetic(a(2,"mạng"),"NGƯỜI BẠN MUỐN TÌM","CŨNG PHẢI Ở TRONG MẠNG"),
 slam(a(3,"coursematch"),"COURSEMATCH","XEM BẠN BÈ HỌC LỚP NÀO"),
 org(a(4,"môn"),[{"id":"course","t":"MÔN HỌC","s":"NHỊP CHUNG","at":a(4,"môn")},{"id":"friend","t":"BẠN BÈ","s":"MỐI NỐI","p":"course","at":a(4,"môn")}]),
 broll("7490429",a(6,"lớp"),"KHUÔN VIÊN ĐẠI HỌC MINH HỌA · KHÔNG PHẢI HARVARD"),
 counter(a(7,"100000"),100000," NGƯỜI","GẦN ĐÚNG · THEO CRIMSON"),
 timeline(a(9,"facebook"),"memorial24",[("05.2004","NHÓM ĐI PALO ALTO"),("06.2004","ĐỔI TÊN FACEBOOK")]),
 photo("campus",a(10,"mốc"),"MỞ RỘNG","MỐC SỰ KIỆN KHÔNG ĐỌC Ý NGHĨ"),
 ledger(4,a(11,"bản")),question(a(12,"hạ"),"MỘT DANH BẠ ĐÃ THÀNH\nHẠ TẦNG NHƯ THẾ NÀO?")]
def ch04(): return [
 chapter(4,"CHƯƠNG BỐN","NHỮNG VAI TRÒ\nĐẦU TIÊN","2005 · TÀI CHÍNH · QUẢNG CÁO","hall",a(0,"câu")),
 kinetic(a(1,"vai"),"KHÔNG CHỈ MỘT NGƯỜI","NHIỀU VAI TRÒ BAN ĐẦU"),
 print_scene("memorial24",a(2,"eduardo"),"HỒ SƠ CRIMSON","EDUARDO SAVERIN","CFO CỦA FACEBOOK"),
 org(a(4,"đầu"),[{"id":"capital","t":"ĐẦU TƯ SỚM","s":"TÀI CHÍNH","at":a(4,"đầu")},{"id":"ads","t":"QUẢNG CÁO","s":"ĐIỀU PHỐI","p":"capital","at":a(4,"đầu")}]),
 timeline(a(5,"zuckerberg"),"weld",[("TRƯỚC LẬP TRÌNH","TIẾP CẬN SAVERIN"),("06.2004","NHÓM ĐI PALO ALTO")]),
 broll("5672679",a(6,"trình"),"KHUÔN VIÊN ĐẠI HỌC MINH HỌA · KHÔNG GẮN DANH TÍNH"),
 slam(a(8,"đẩy"),"THAY ĐỔI VỊ TRÍ","KHÔNG SUY ĐOÁN ĐỘNG CƠ"),
 photo("yard",a(9,"kiện"),"ĐIỀU BIẾT CHẮC","MỐC SỰ KIỆN CÓ NGUỒN"),
 kinetic(a(11,"thận"),"THẬN TRỌNG","KHÔNG LÀM CÂU CHUYỆN NHẠT ĐI"),
 ledger(5,a(13,"bản")),question(a(14,"đường"),"KHI MỘT ĐƯỜNG NỐI ĐỔI,\nNGUỒN NÓI ĐẾN ĐÂU?")]
def ch05(): return [
 chapter(5,"CHƯƠNG NĂM","MỘT TRANH CHẤP\nCÓ HỒ SƠ","2008 → 2011 · CONNECTU","memorial07",a(0,"cameron")),
 org(a(0,"tyler"),[{"id":"group","t":"WINKLEVOSS · NARENDRA","s":"MẠNG CHO SINH VIÊN","at":a(0,"tyler")},{"id":"zuck","t":"ZUCKERBERG","s":"HỖ TRỢ XÂY DỰNG","p":"group","at":a(0,"tyler")}]),
 kinetic(a(1,"pháp"),"HỒ SƠ PHÁP LÝ","TÁCH CÁO BUỘC VÀ KẾT LUẬN"),
 print_scene("chapel",a(2,"cáo"),"TÒA KHU VỰC 9","CÁO BUỘC","KHÔNG PHẢI KẾT LUẬN SỰ THẬT"),
 slam(a(4,"kết"),"BA NHÃN KHÁC NHAU","CÁO BUỘC · DÀN XẾP · PHÁN QUYẾT"),
 timeline(a(6,"2008"),"hall",[("22.02.2008","HÒA GIẢI TOÀN CẦU"),("2011","THI HÀNH DÀN XẾP")]),
 counter(a(7,"20"),20," TRIỆU USD","TIỀN MẶT · THEO HỒ SƠ TÒA"),
 counter(a(8,"65"),65," TRIỆU USD","GIÁ TRỊ XẤP XỈ KHI ĐÓ"),
 photo("memorial16",a(9,"đạo"),"ĐIỀU KHOẢN","KHÔNG PHẢI THƯỚC ĐO ĐẠO ĐỨC"),
 ledger(6,a(13,"bản")),question(a(14,"phán"),"LÀM SAO XEM TRANH CHẤP\nMÀ KHÔNG TƯỞNG TƯỢNG ÁN?")]
def ch06(): return [
 chapter(6,"CHƯƠNG SÁU","PHIM KHÔNG\nPHẢI HỒ SƠ","2010 · MẠNG XÃ HỘI","memorial24",a(0,"phim")),
 date(a(1,"mark"),"MẠNG XÃ HỘI","2010","DAVID FINCHER ĐẠO DIỄN"),
 photo("mark",a(2,"netflix"),"MÔ TẢ NETFLIX","SỰ TRỖI DẬY TỪ HARVARD"),
 kinetic(a(3,"nhãn"),"CHUYỂN THỂ TỪ SÁCH","DỰA TRÊN CÂU CHUYỆN CÓ THẬT"),
 slam(a(4,"eduardo"),"KHÔNG TỰ THÀNH TƯ LIỆU","MỌI CẢNH THOẠI"),
 org(a(5,"mark"),[{"id":"eduardo","t":"ANDREW GARFIELD","s":"VAI EDUARDO","at":a(5,"andrew")},{"id":"mark","t":"JESSE EISENBERG","s":"VAI MARK","p":"eduardo","at":a(5,"jesse")}]),
 timeline(a(7,"bạn"),"yard",[("CẢNH PHIM","CẦN GỌI ĐÚNG TÊN"),("HỒ SƠ","KIỂM PHẦN TRẢ LỜI")]),
 broll("946146",a(9,"phim"),"NGƯỜI DÙNG MÁY TÍNH MINH HỌA · KHÔNG PHẢI NHÂN VẬT THẬT"),
 photo("chapel",a(12,"người"),"NGƯỜI THẬT CÒN SỐNG","CÂU THOẠI CÓ THỂ BỊ NHỚ SAI"),
 ledger(7,a(13,"bản")),question(a(14,"feed"),"TỪ HAI ẢNH NGẪU NHIÊN\nĐẾN HỆ THỐNG NÀO?")]
def ch07(): return [
 chapter(7,"CHƯƠNG BẢY","AI ĐỨNG Ở\nĐẦU FEED","TỪ SO CẶP ĐẾN XẾP HẠNG","campus",a(0,"facemash")),
 photo("ai04",a(2,"meta"),"FEED HIỆN ĐẠI","MINH HỌA XẾP THỨ TỰ"),
 kinetic(a(3,"feed"),"FEED","DÒNG BÀI KHI MỞ ỨNG DỤNG"),
 org(a(4,"inventory"),[{"id":"inventory","t":"INVENTORY","s":"BÀI CÓ THỂ HIỆN","at":a(4,"inventory")},{"id":"signals","t":"SIGNALS","s":"TÍN HIỆU","p":"inventory","at":a(4,"signals")},{"id":"predict","t":"PREDICTIONS","s":"DỰ ĐOÁN","p":"signals","at":a(4,"predictions")},{"id":"score","t":"SCORE","s":"XẾP THỨ TỰ","p":"predict","at":a(4,"relevancy")}]),
 kinetic(a(6,"signals"),"TÍN HIỆU","HỆ THỐNG QUAN SÁT ĐƯỢC"),
 slam(a(8,"score"),"RELEVANCY SCORE","ĐIỂM SẮP THỨ TỰ LIÊN QUAN"),
 timeline(a(10,"bình"),"hall",[("PHẢN ỨNG","TÍN HIỆU TƯƠNG TÁC"),("BÌNH LUẬN","TÍN HIỆU THẢO LUẬN"),("CHIA SẺ","TÍN HIỆU LAN TRUYỀN")]),
 counter(a(11,"meta"),3000," BÀI","KHẢ DĨ MỖI NGÀY · THEO META"),
 counter(a(11,"khi"),300," BÀI","NGƯỜI DÙNG LƯỚT · THEO META"),
 photo("campus",a(12,"kiểm"),"LỜI META GIẢI THÍCH","KHÔNG PHẢI KIỂM TOÁN ĐỘC LẬP"),
 ledger(8,a(13,"bản")),kinetic(a(15,"bản"),"GIỮ NGUYÊN KHOẢNG TRỐNG","KHI NGUỒN CHƯA NÓI")]
SCENES=[ch00,ch01,ch02,ch03,ch04,ch05,ch06,ch07]
SOURCES=["https://www.thecrimson.com/article/2003/11/4/hot-or-not-website-briefly-judges/","https://www.thecrimson.com/article/2014/2/4/facebook-ten-years-feature-1/","https://www.thecrimson.com/article/2005/2/24/key-players-three-full-time-employees-have/?page=single","https://law.justia.com/cases/federal/appellate-courts/ca9/08-16745/08-16745-2011-04-11.html","https://law.justia.com/cases/massachusetts/court-of-appeals/volumes/95/95massappct202.html","https://www.netflix.com/vn/title/70132721","https://about.fb.com/news/2018/05/inside-feed-news-feed-ranking/","https://about.fb.com/news/2018/01/news-feed-fyi-bringing-people-closer-together/","https://about.fb.com/news/2018/09/us-brazil-elections/"]
def make_spec(): return {"topic":TOPIC,"title":TITLE,"channel":"MIM","theme":"lab","look":"steel","accent":"#ef4444","master":True,"beat2":True,"say":SAY,"imgs":IMGS,"geo":GEO,"chapters":[f"ch{i:02d}" for i in range(8)],"youtube":{"titles":[TITLE,"Mark Zuckerberg 2004: Bản Đồ Ra Đời Facebook"],"publish_at":"2026-11-29T13:00:00Z","playlist":"Công Nghệ Quanh Ta","category":"28","thumb":"t1.jpg","summary":"Từ Facemash ở Harvard năm 2003 đến Feed hiện đại, video lần theo các trang báo đương thời, hồ sơ tòa và mô tả công khai của Meta. Đây là bản đồ của dữ kiện, cáo buộc, dàn xếp và những khoảng trống cần giữ nguyên.","more":["Phim Mạng xã hội chỉ được nhắc bằng lời và chữ; video không sử dụng hình ảnh, âm thanh hoặc trích đoạn từ phim.","Các clip Pexels có nhãn VIDEO MINH HỌA và không mô tả một người hay sự kiện cụ thể.","Một số hình là tranh minh họa nhằm diễn đạt ý tưởng, không phải ảnh tư liệu."],"chapter_titles":CHAPTER_TITLES,"sources":SOURCES,"tags":["Mark Zuckerberg","Facebook","Facemash","Harvard","The Social Network","Meta","Feed ranking","lịch sử công nghệ"],"hashtags":["MarkZuckerberg","Facebook","CôngNghệQuanhTa","MindInTheMachine"],"video_credits":["Ảnh khuôn viên và Mark Zuckerberg: Wikimedia Commons, CC BY hoặc Public domain.","Video minh họa: Pexels.","Tranh minh họa: tạo theo prompt nội bộ của kênh."]},"sources_internal":"Chỉ dùng kho facts.md đã duyệt. Ảnh Commons I01-I09: CC BY, CC0 hoặc Public domain. Bốn tranh minh họa chờ chủ kênh tạo theo ai_prompts.md."}
def _anchors(node,out):
 if isinstance(node,dict):
  for v in node.values(): _anchors(v,out)
 elif isinstance(node,list):
  if len(node)==2 and isinstance(node[0],int) and isinstance(node[1],str): out.append(node)
  else:
   for v in node:_anchors(v,out)
def fix_anchors(scenes,lines):
 found=[]; _anchors(scenes,found); used=set()
 for x in found:
  text=lines[x[0]] if isinstance(lines[x[0]],str) else lines[x[0]].get("t","")
  words=[re.sub(r"[^\wÀ-ỹ]","",w).lower() for w in text.split()]
  if x[1].lower() in words and not re.search(r"\d",x[1]): used.add((x[0],x[1].lower())); continue
  pos=next((i for i,w in enumerate(words) if x[1].lower() in w),len(words))
  for i in list(range(pos-1,-1,-1))+list(range(pos+1,len(words))):
   if words[i] and not re.search(r"\d",words[i]) and (x[0],words[i]) not in used: x[1]=words[i]; used.add((x[0],words[i])); break
 return scenes
def main():
 (ROOT/"spec.json").write_text(json.dumps(make_spec(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 for i,fn in enumerate(SCENES):
  f=ROOT/f"ch{i:02d}.json"; out=json.loads(f.read_text(encoding="utf-8")); out.update({"topic":TOPIC,"chapter":i,"hud":{"k":f"CHƯƠNG {i:02d}","t":CHAPTER_TITLES[f"ch{i:02d}"].upper()},"scenes":fix_anchors(fn(),out["lines"])})
  f.write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
 print(f"Đã tạo spec.json và {len(SCENES)} chương cho {TOPIC}"+(" (BẢN THAY TẠM ẢNH AI — đừng render)" if STANDIN else "."))
if __name__=="__main__": main()
