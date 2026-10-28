"""SEO caption cleaner (lượt 20/10): từ khóa tìm kiếm ở đầu, 3-5 hashtag có người tìm, không URL, credit ngắn.
Dùng: from seo import seo_clean; seo_clean(n, caption)"""
import re
# cụm từ khóa tiếng Việt người dùng hay gõ tìm (đặt đầu dòng 1 nếu hook chưa chứa)
KW = {57:"Lời Phật dạy khi cãi nhau",58:"Phật Dược Sư",59:"Lời Phật dạy cuối tháng",60:"Lời Phật dạy khi mất ngủ",
61:"Mùng 1 tháng 10 âm lịch",62:"Lời Phật dạy khi tự trách",63:"Lời Phật dạy về tình bạn",64:"Lời Phật dạy khi lòng nặng",
65:"Đố vui Phật pháp",66:"Chuyện Phật giáo",67:"Tượng Phật",68:"Lời Phật dạy về tập trung",69:"Vía Tổ Đạt Ma",
70:"Chuyện Tổ Đạt Ma",71:"Đố vui Phật pháp",72:"Lời Phật dạy khi đang giận",73:"Vô thường là gì",74:"Lời Phật dạy về hận thù",
75:"Thắp hương xin Phật",76:"Lời Phật dạy khi tự ti",77:"Đố vui Phật pháp",78:"Chuyện thiền",79:"Biểu tượng Phật giáo",
80:"Lời Phật dạy khi bị ghét",81:"Lời Phật dạy mỗi sáng",82:"Lời Phật dạy khi so sánh",83:"Ngày Nhà giáo 20/11",
84:"Chuyện Phật giáo",85:"Đố vui Phật pháp",86:"Bát phong là gì",87:"Lời Phật dạy về thương mình",88:"Chuyện người mù sờ voi",
89:"Rằm tháng 10 Tết Hạ Nguyên",90:"Tết Hạ Nguyên",91:"Mõ chùa hình con cá",92:"Lời Phật dạy về góp ý",93:"Niệm Phật là gì",
94:"Lời Phật dạy về thói quen",95:"Nghiệp là gì",96:"Lời Phật dạy khi tự trách",97:"Lời Phật dạy về lời nói",
98:"Thiền thư giãn văn phòng",99:"Lời Phật dạy về giữ tâm",100:"Phật dạy về tiền",101:"Tràng hạt 108 hạt",
102:"Lời Phật dạy về buông bỏ",103:"Đố vui Phật pháp",104:"Lời Phật dạy về lời nói"}
# hashtag tự đặt, gần như không ai tìm -> bỏ
COINED = {'badieu','songtinh','nhangui','kiemchecongian','trian','dobandoithuong','kinhthicalaviet','kinhphattuthuyet','lahaula',
 'chentra','ruamu','108','loau','tuti','8ngongio','batphapthegian','haimuiten','giuminh','huongnguocgio','tamtinh','moca',
 'kienthuc','doivai','nguoimusovoi','cuoithang','kinhtangchi','kinhtuongung','kinhtrungbo','30thang9amlich','baiphapdautien',
 'tichtieuthanhdai','gopy','bantot','nantam','kiennhan','tamtu','suynghitichcuc','luottin','yeuthuongbanthan','thaphuong',
 'giandu','khiemton','tinhlang','badieu','hieudung','visao','tamanmoingay','phattaitam','phatphapnhiemmau','14ngaybieton','danggian'}
CORE = ['loiphatday','phatphap','phatgiao']
def tags_for(n, old):
    last = [l for l in old.strip().split('\n') if re.fullmatch(r'(#\w+\s*)+', l.strip())]
    t = [x for x in re.findall(r'#(\w+)', last[-1] if last else '') if not x.isdigit() and x.lower() not in COINED and x not in ('phatgiao',)]
    t = [x for x in t if x not in CORE][:2]
    if n in (65,71,77,85,103) and 'dovuiphatphap' not in t: t = ['dovuiphatphap'] + t[:1]
    out = t + CORE
    return ' '.join('#'+x for x in out[:5])
def short_src(line):
    s = re.sub(r'\s*[–-]\s*https?://\S+', '', line)
    s = re.sub(r'\s*—\s*bản Anh Bhikkhu Sujato \(CC0\), SuttaCentral', '', s)
    s = re.sub(r'https?://\S+', '', s).strip(' ;–-')
    return s
def seo_clean(n, cap):
    parts = [p for p in cap.split('\n\n')]
    keep, src = [], []
    for p in parts:
        lines = []
        for l in p.split('\n'):
            if l.startswith('Nguồn:'): src.append(short_src(l))
            elif l.startswith(('Nhạc:', 'Âm thanh:', 'Phần diễn giải')) or re.fullmatch(r'(#\w+\s*)+', l.strip()): pass
            else: lines.append(l)
        if lines: keep.append('\n'.join(lines))
    first = keep[0]; kw = KW.get(n)
    if kw and kw.lower() not in first.lower():
        first = f"{kw} · {first}"
    keep[0] = first
    keep = [re.sub(r'#(\d+)', r'số \1', k) for k in keep]   # '#1' trong chữ bị TikTok hiểu là hashtag rác
    credit = "Nhạc: Kevin MacLeod (CC BY 4.0) · Video: Pexels"
    tail = ('\n'.join(src) + '\n' if src else '') + credit
    out = '\n\n'.join(keep + [tail, tags_for(n, cap)])
    assert 'http' not in out
    return out
