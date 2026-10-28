"""Cảnh + spec cho Long MIM `mim-macintosh-1984`."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).parent
TOPIC = "mim-macintosh-1984"
TITLE = "STEVE JOBS 1984: Macintosh biết nói bằng hình"
STANDIN = "--standin" in sys.argv

SAY = {
 "steve":"Xti-vơ", "jobs":"Giốp", "macintosh":"Mác-in-tót", "apple":"Áp-pồ",
 "xerox":"Dê-rốc", "parc":"Pa-rờ-xi", "alto":"An-tô", "smalltalk":"X-môn-tóc",
 "lisa":"Li-sa", "super":"Xu-pờ", "bowl":"Bâu", "hertzfeld":"Hớt-phên",
 "macwrite":"Mác-rai-tờ", "macpaint":"Mác-pâynt", "datapro":"Đa-ta-prô",
 "folklore":"Phô-cờ-lo", "wimp":"uyn-đâu ai-cần mơ-nu poi-tơ", "gui":"gi-u-ai",
 "ram":"ram", "crt":"xi-a-ti", "mhz":"mê-ga-héc", "ibm":"ai-bi-em",
 "next":"Nét-xờt", "imac":"ai-mác", "netflix":"Nét-phlích", "cnet":"xi-nét",
 "cbs":"xi-bi-ét", "time":"Thai-mờ", "usd":"đô la Mỹ", "kb":"ki-lô-bai"
}
IMGS = {
 "mac1":"File:Macintosh 128k computer, January 1984, by Bernard Gotfryd - (cropped to remove individual).jpg",
 "jobs1":"File:Steve Jobs and Macintosh computer, January 1984, by Bernard Gotfryd - edited.jpg",
 "jobs2":"File:Steve Jobs (Apple computer) (LOC).jpg",
 "mac2":"File:Apple Museum (Prague) Macintosh 128K (1984) - 1.jpg",
 "mac3":"File:Apple Museum (Prague) Macintosh 128K (1984) - 2.jpg",
 "alto1":"File:Xero Alto Computer.jpg", "alto2":"File:Xerox Alto full.jpg",
 "mouse1":"File:Computer mouse-2005.jpg",
 "mouse2":"File:A computer mouse in black and white with a computer keyboard behind it.jpg",
 "floppy":"File:3.5in floppy disk illustration.svg"
}
AI_PATH={f"ai0{i}":f"assets/long/{TOPIC}/img/ai/ai_0{i}.png" for i in range(1,6)}
STAND={"ai01":"alto1","ai02":"mac2","ai03":"jobs1","ai04":"mouse1","ai05":"mac3"}
if not STANDIN: IMGS.update({k:f"EXT:ai:{Path(v).stem}" for k,v in AI_PATH.items()})
def im(k): return STAND[k] if STANDIN and k in STAND else k
GEO={}
CHAPTER_TITLES={"ch00":"Cú nhấp đã được nhìn thấy","ch01":"Chín mươi K để làm việc","ch02":"Quảng cáo đi trước chiếc máy","ch03":"Ngày chiếc máy tự giới thiệu","ch04":"Cái giá của một mặt bàn","ch05":"Chuột không chỉ để chỉ","ch06":"Bộ phim và khoảng cách thật","ch07":"Điều còn lại trên màn hình"}
LEDGER="ĐƯỜNG ĐI CỦA CÚ NHẤP"
ROWS=[("MỞ ĐẦU","PARC VÀ CON TRỎ"),("1 · BỘ NHỚ","CHỈ CÒN 90K"),("2 · TÍN HIỆU","QUẢNG CÁO ĐI TRƯỚC"),("3 · SÂN KHẤU","MÁY TỰ GIỚI THIỆU"),("4 · GÓI MÁY","MẶT BÀN NHÌN THẤY"),("5 · GIAO DIỆN","CHUỘT VÀ CON TRỎ"),("6 · PHIM","GIỮ KHOẢNG CÁCH"),("7 · DI SẢN","NHIỀU NGƯỜI CÙNG LÀM")]
VM,AIL="VIDEO MINH HỌA","ẢNH MINH HỌA"
def a(line,word): return [line,word]
def chapter(no,k,title,sub,bg,at): return {"type":"chapter","no":str(no),"k":k,"title":title,"sub":sub,"bg":im(bg),"titleAt":at}
def photo(img,at,key,value,kin=None):
 o={"type":"photo","at":at,"img":im(img),"tone":"bw","move":"in","veil":.55,"label":{"k":key,"v":value,"at":at}}
 if img.startswith("ai"): o.update({"illus":AIL,"credit":False})
 if kin: o["kin"]=[{"text":kin,"at":at,"acc":True}]
 return o
def broll(vid,at,text): return {"type":"broll","at":at,"vid":vid,"veil":.62,"illus":VM,"kin":[{"text":text,"at":at,"acc":True}]}
def kinetic(at,text,small=None): return {"type":"kinetic","at":at,"items":[{"text":text,"at":at,"acc":True}]+([{"text":small,"at":at,"sm":True}] if small else [])}
def slam(at,text,sub): return {"type":"slam","at":at,"text":text,"sub":sub}
def date(at,day,d,sub): return {"type":"date","at":at,"day":day,"date":d,"sub":{"text":sub,"at":at}}
def print_scene(img,at,head,key,value): return {"type":"print","at":at,"img":im(img),"tone":"bw","head":head,"side":{"k":key,"h":value,"lines":[{"text":value,"at":at}]}}
def ledger(n,at): return {"type":"ledger","at":at,"title":LEDGER,"srcnote":"MỖI CHƯƠNG THÊM MỘT MỐC","rows":[{"k":k,"v":v,"at":at} for k,v in ROWS[:n]]}
def question(at,text): return {"type":"question","at":at,"text":text}
def counter(at,to,suffix,label,frm=0,year=False): return {"type":"counter","at":at,"from":frm,"to":to,"suffix":suffix,"label":label,"year":year}
def timeline(at,bg,items): return {"type":"timeline","at":at,"bg":im(bg),"items":[{"year":y,"text":t} for y,t in items]}
def org(at,nodes): return {"type":"org","at":at,"nodes":nodes}

def ch00(): return [
 chapter(0,"MỞ ĐẦU","CÚ NHẤP\nĐÃ ĐƯỢC THẤY","1979 · PARC · ALTO","alto1",a(1,"Điều")),
 kinetic(a(0,"Steve"),"24.01.1984","MỘT LỜI HỨA BẰNG HÌNH"),
 photo("jobs1",a(1,"máy"),"PHẦN TRÌNH DIỄN","MÁY TỰ GIỚI THIỆU"),
 photo("mouse1",a(2,"chuột"),"VẬT NỐI","CHUỘT MỘT NÚT · KHÔNG LOGO"),
 photo("ai01",a(3,"PARC"),"PHÒNG THÍ NGHIỆM","MINH HỌA BỐI CẢNH"),
 print_scene("alto2",a(4,"Alto"),"XEROX PARC","GIAO DIỆN ĐỒ HỌA","CỬA SỔ · BIỂU TƯỢNG · MENU"),
 timeline(a(5,"Super"),"mac1",[("1979","THĂM PARC"),("1984","MACINTOSH RA MẮT")]),
 slam(a(6,"Sau"),"TỪ Ý TƯỞNG ĐẾN SÂN KHẤU","PARC · BỘ NHỚ · QUẢNG CÁO"),
 ledger(1,a(6,"chuột")), question(a(7,"bước"),"Ý TƯỞNG ĐÃ CÓ TRƯỚC,\nVÌ SAO 1984 VẪN ĐÁNG NHỚ?")]
def ch01(): return [
 chapter(1,"CHƯƠNG MỘT","90K\nĐỂ LÀM VIỆC","128K RAM · MÙA THU 1983","mac2",a(0,"Hertzfeld")),
 counter(a(0,"128K"),128,"K RAM","MỘT PHẦN TÁM MEGABYTE"),
 kinetic(a(1,"RAM"),"BỘ NHỚ LÀM VIỆC","NƠI CHƯƠNG TRÌNH GIỮ VIỆC ĐANG LÀM"),
 counter(a(3,"16K"),16,"K","DÀNH CHO HỆ THỐNG"),
 photo("ai02",a(4,"màn"),"MÀN HÌNH PIXEL","MINH HỌA GIAO DIỆN ĐƠN SẮC"),
 photo("mouse2",a(11,"chuột"),"VẬT NỐI","CON TRỎ CẦN CHỖ TRONG BỘ NHỚ"),
 broll("3592341",a(14,"desktop"),"GÕ PHÍM MINH HỌA · KHÔNG PHẢI SỰ KIỆN THẬT"),
 slam(a(16,"giá"),"2.495 USD","MỘT LỜI HỨA PHẢI CHẠY MƯỢT"),
 ledger(2,a(18,"90K")), question(a(19,"lại"),"LÀM SAO MỘT CÚ NHẤP\nKHÔNG KHIẾN MÁY ĐỨNG LẠI?")]
def ch02(): return [
 chapter(2,"CHƯƠNG HAI","QUẢNG CÁO ĐI\nTRƯỚC CHIẾC MÁY","22.01.1984 · SUPER BOWL XVIII","mac3",a(0,"Macintosh")),
 date(a(1,"Ngày"),"QUÝ BA SUPER BOWL","22.01.1984","QUẢNG CÁO 1984 PHÁT SÓNG"),
 timeline(a(2,"hai"),"mac1",[("22.01","QUẢNG CÁO"),("24.01","GIỚI THIỆU MÁY")]),
 counter(a(4,"1,5"),15," TRIỆU USD","CHI PHÍ QUẢNG CÁO · THEO CHM",year=False),
 kinetic(a(6,"Apple"),"MỘT SÂN KHẤU ĐẮT TIỀN","KHÔNG TỰ CHỨNG MINH THÀNH CÔNG"),
 slam(a(9,"nhịp"),"NHỊP KỂ ĐI TRƯỚC VẬT THỂ","HAI NGÀY TRƯỚC KHI GẶP MÁY"),
 photo("mouse1",a(11,"chuột"),"VẬT NỐI","BÀN TAY CỦA LỜI HỨA"),
 broll("6803042",a(12,"phản"),"THAO TÁC CHUỘT MINH HỌA · KHÔNG GẮN DANH TÍNH"),
 ledger(3,a(14,"khó")), question(a(15,"không"),"LỜI HỨA CÓ THÀNH\nCÁCH DÙNG MÁY THẬT SỰ?")]
def ch03(): return [
 chapter(3,"CHƯƠNG BA","NGÀY CHIẾC MÁY\nTỰ GIỚI THIỆU","24.01.1984 · BẢN DEMO","jobs1",a(0,"Support")),
 date(a(0,"ngày"),"MACINTOSH 128K","24.01.1984","NGÀY GIỚI THIỆU"),
 photo("jobs2",a(1,"Hertzfeld"),"ĐỘI NGŨ","HÀO HỨNG VÀ LO LẮNG"),
 print_scene("floppy",a(3,"đĩa"),"BẢN DEMO","ĐĨA MỀM 3,5 INCH","PHẦN MỀM PHẢI VÀO MÁY"),
 photo("ai03",a(5,"sân"),"HẬU TRƯỜNG","MINH HỌA SÂN KHẤU 1984"),
 slam(a(7,"ba"),"LỜI JOBS TẠI SỰ KIỆN","KHÔNG PHẢI KẾT LUẬN ĐỘC LẬP"),
 kinetic(a(8,"độc"),"SÂN KHẤU MUỐN BẠN NHỚ","LỊCH SỬ CẦN PHÂN BIỆT"),
 photo("mouse2",a(12,"chuột"),"VẬT NỐI","TRỎ VÀO THỨ ĐANG THẤY"),
 ledger(4,a(15,"hướng")), question(a(16,"thực"),"BÊN TRONG 128K CÓ GÌ\nĐỂ CỬ CHỈ NÀY CÓ NGHĨA?")]
def ch04(): return [
 chapter(4,"CHƯƠNG BỐN","CÁI GIÁ CỦA\nMỘT MẶT BÀN","8 MHZ · 128K · 16-BIT","mac2",a(0,"Museum")),
 counter(a(0,"8"),8," MHZ","BỘ VI XỬ LÝ"),
 kinetic(a(2,"16-bit"),"KIẾN TRÚC 16-BIT","MỘT MÔ TẢ KỸ THUẬT"),
 print_scene("mac3",a(4,"Gói"),"DANH MỤC DATAPRO","2.495 USD","RAM · Ổ ĐĨA · CRT · CHUỘT"),
 photo("mouse1",a(4,"chuột"),"VẬT NỐI","CỬA VÀO CỦA CẢ GÓI MÁY"),
 timeline(a(7,"tháng"),"mac1",[("01.1984","GIAO MÁY ĐẦU TIÊN"),("3.000","ĐẠI LÝ ỦY QUYỀN")]),
 slam(a(10,"kênh"),"3.000 ĐẠI LÝ","DỮ KIỆN PHÂN PHỐI · KHÔNG PHẢI DOANH SỐ"),
 broll("4962316",a(15,"Chuột"),"BÀN PHÍM VÀ CHUỘT MINH HỌA · KHÔNG GẮN THƯƠNG HIỆU"),
 ledger(5,a(16,"nhàng")), question(a(17,"đơn"),"MỘT MÀN HÌNH ĐƠN GIẢN\nĐÃ ĐỔI GÌ Ở BÊN DƯỚI?")]
def ch05(): return [
 chapter(5,"CHƯƠNG NĂM","CHUỘT KHÔNG\nCHỈ ĐỂ CHỈ","WIMP · LISA · MACPAINT","mouse1",a(0,"Museum")),
 kinetic(a(1,"WIMP"),"CỬA SỔ · BIỂU TƯỢNG","MENU · CON TRỎ"),
 photo("ai04",a(3,"Chuột"),"VẬT NỐI","CHUỘT MỘT NÚT VÀ CON TRỎ PIXEL"),
 slam(a(5,"bấm"),"NHÌN · TRỎ · BẤM","KHÔNG CẦN NHỚ MỘT CHUỖI LỆNH"),
 timeline(a(6,"Lisa"),"mac3",[("LISA","NỖ LỰC ĐẦU"),("MACINTOSH","NỖ LỰC THỨ HAI")]),
 counter(a(8,"512"),512," × 342","ĐIỂM ẢNH ĐEN TRẮNG"),
 kinetic(a(11,"vùng"),"BA VÙNG ĐỆM","MỖI VÙNG BẰNG TOÀN BỘ MÀN HÌNH"),
 broll("19205382",a(14,"giao"),"CHUỘT VÀ BÀN PHÍM MINH HỌA · KIỂM LOGO TRƯỚC DÙNG"),
 ledger(6,a(16,"bước")), question(a(17,"gàng"),"KHI PHIM KỂ LẠI,\nCHI TIẾT NÀO DỄ BỊ NÉN ĐI?")]
def ch06(): return [
 chapter(6,"CHƯƠNG SÁU","BỘ PHIM VÀ\nKHOẢNG CÁCH THẬT","2015 · BA LẦN RA MẮT","jobs2",a(0,"Steve")),
 print_scene("jobs2",a(2,"Boyle"),"PHIM STEVE JOBS","DANNY BOYLE","AARON SORKIN · MICHAEL FASSBENDER"),
 timeline(a(4,"Macintosh"),"mac1",[("1984","MACINTOSH"),("1988","NEXT"),("1998","IMAC")]),
 kinetic(a(5,"hậu"),"HỖN LOẠN HẬU TRƯỜNG","CÁCH BỘ PHIM ĐẶT TRỌNG TÂM"),
 slam(a(7,"hồ"),"KHÔNG ĐỌC PHIM NHƯ HỒ SƠ","THEO LỜI GIẢI THÍCH CỦA SORKIN"),
 photo("alto2",a(8,"tài"),"TRỞ VỀ TÀI LIỆU","PARC · 128K · QUẢNG CÁO · SÂN KHẤU"),
 photo("mouse2",a(9,"Chuột"),"VẬT NỐI","GIAO DIỆN · PHẦN MỀM · BỘ NHỚ"),
 broll("4450059",a(10,"đội"),"GÕ PHÍM MINH HỌA · KHÔNG PHẢI ĐỘI MAC"),
 ledger(7,a(11,"kịch")), question(a(12,"nhận"),"GIỮ KHOẢNG CÁCH CÓ LÀM\nCÂU CHUYỆN BỚT HẤP DẪN?")]
def ch07(): return [
 chapter(7,"CHƯƠNG BẢY","ĐIỀU CÒN LẠI\nTRÊN MÀN HÌNH","1984 · MỘT TRẢI NGHIỆM","mac1",a(0,"Museum")),
 kinetic(a(2,"Macintosh"),"ĐƯA ĐỒ HỌA TỚI NHIỀU NGƯỜI","THEO COMPUTER HISTORY MUSEUM"),
 timeline(a(4,"Alto"),"alto1",[("ALTO","CÓ TRƯỚC"),("LISA","CÓ TRƯỚC"),("1984","GHÉP THÀNH TRẢI NGHIỆM")]),
 slam(a(7,"biểu"),"NHÌN MỘT BIỂU TƯỢNG","MỘT THAO TÁC BẮT ĐẦU"),
 photo("ai04",a(8,"chuột"),"VẬT NỐI","MỘT CÚ NHẤP · MỘT THAY ĐỔI"),
 photo("ai05",a(10,"đội"),"ĐỘI PHẦN MỀM","MINH HỌA LAO ĐỘNG TẬP THỂ"),
 print_scene("mac2",a(12,"Support"),"TƯƠNG THÍCH KỸ THUẬT","SYSTEM 1.0 → 7.0.1P","KHÔNG PHẢI THỐNG KÊ PHỔ BIẾN"),
 broll("29542968",a(16,"hình"),"THAO TÁC MÁY TÍNH MINH HỌA · KHÔNG GẮN DANH TÍNH"),
 ledger(8,a(18,"nhớ")), kinetic(a(19,"cử"),"MỘT CÚ NHẤP","NHIỀU Ý TƯỞNG · THỬ NGHIỆM · LAO ĐỘNG")]
SCENES=[ch00,ch01,ch02,ch03,ch04,ch05,ch06,ch07]
SOURCES=["https://computerhistory.org/blog/the-lisa-apples-most-influential-failure/","https://www.computerhistory.org/revolution/story/348","https://computerhistory.org/apple-timeline/","https://folklore.org/Monkey_Lives.html","https://americanhistory.si.edu/explore/stories/remembering-apples-1984-super-bowl-ad","https://www.computerhistory.org/tdih/january/22/","https://support.apple.com/en-me/112190","https://www.folklore.org/StoryView.py?detail=medium&project=Macintosh&sortOrder=Sort+by+Date&story=The+Times_They_Are_A-Changin.txt&topic=The+Launch","https://www.computerhistory.org/revolution/personal-computers/17/303/1203","https://bitsavers.computerhistory.org/pdf/datapro/datapro_reports_70s-90s/Apple/M09-057-10_8411_Apple_Macintosh.pdf","https://time.com/4012824/the-man-who-would-be-jobs/","https://www.cbsnews.com/news/19-questions-you-might-be-asking-after-seeing-steve-jobs/"]
def make_spec(): return {"topic":TOPIC,"title":TITLE,"channel":"MIM","theme":"lab","look":"steel","accent":"#ef4444","master":True,"beat2":True,"say":SAY,"imgs":IMGS,"geo":GEO,"chapters":[f"ch{i:02d}" for i in range(8)],"youtube":{"titles":[TITLE,"Macintosh 1984: Cú Nhấp Đưa Hình Ảnh Lên Màn Hình"],"publish_at":"2026-11-30T13:00:00Z","playlist":"Công Nghệ Quanh Ta","category":"28","thumb":"t1.jpg","summary":"Macintosh năm 1984 không xuất hiện từ khoảng trống. Video lần theo PARC, bộ nhớ 128K, quảng cáo Super Bowl, sân khấu ra mắt và cách giao diện đồ họa cùng chuột đến gần nhiều người hơn.","more":["Phim Steve Jobs chỉ được nhắc bằng lời và chữ; video không dùng hình ảnh, âm thanh hay trích đoạn từ phim.","Clip Pexels có nhãn VIDEO MINH HỌA và không mô tả một người hay sự kiện cụ thể.","Một số cảnh là tranh minh họa nhằm diễn đạt ý tưởng, không phải ảnh tư liệu."],"chapter_titles":CHAPTER_TITLES,"sources":SOURCES,"tags":["Steve Jobs","Macintosh","Apple","Xerox PARC","giao diện đồ họa","chuột máy tính","lịch sử công nghệ"],"hashtags":["Macintosh","SteveJobs","CôngNghệQuanhTa","MindInTheMachine"],"video_credits":["Ảnh: Wikimedia Commons, CC BY, CC0 hoặc Public domain.","Video minh họa: Pexels.","Tranh minh họa: tạo theo prompt nội bộ của kênh."]},"sources_internal":"Chỉ dùng kho facts.md đã duyệt. Ảnh Commons I01-I10 đã kiểm giấy phép; năm tranh minh họa chờ chủ kênh tạo theo ai_prompts.md."}
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
# Claude 27/10/2026: ảnh dọc của Jobs bị cắt giữa -> mất đầu. Lấy nét lên vùng mặt.
FACE = {"jobs1": [0.5, 0.12], "jobs2": [0.5, 0.18]}


def face_focus(scenes):
    for s in scenes:
        k = s.get("img") or s.get("bg")
        if k in FACE:
            s["focus"] = FACE[k]
    return scenes


def main():
 (ROOT/"spec.json").write_text(json.dumps(make_spec(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 for i,fn in enumerate(SCENES):
  f=ROOT/f"ch{i:02d}.json"; out=json.loads(f.read_text(encoding="utf-8")); out.update({"topic":TOPIC,"chapter":i,"hud":{"k":f"CHƯƠNG {i:02d}","t":CHAPTER_TITLES[f"ch{i:02d}"].upper()},"scenes":fix_anchors(face_focus(fn()),out["lines"])})
  f.write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
 print(f"Đã tạo spec.json và {len(SCENES)} chương cho {TOPIC}"+(" (BẢN THAY TẠM ẢNH AI — đừng render)" if STANDIN else "."))
if __name__=="__main__": main()
