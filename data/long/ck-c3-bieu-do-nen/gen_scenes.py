"""Sinh spec.json + scenes/hud/bgm cho video dài CK C3 "Biểu đồ nến cho người mới: một cây nến kể gì về một phiên, và điều nó
không nói được" (Chứng khoán từ số 0 · Bài 3; kênh Biểu Đồ Biết Nói, theme "chart").

    python data/long/ck-c3-bieu-do-nen/gen_scenes.py     # giữ nguyên "lines" + "title" trong chNN.json (script_lines ghi)

Dữ kiện + nguồn: docs/channels/chung-khoan/2026-10-09-long-c3-research.md; kiểm chứng: factcheck.md (cùng thư mục) — chữ trên
màn hình theo mục 1c ĐÃ SỬA: ledger Homma không gạch ngang, "PHỔ BIẾN NẾN Ở PHƯƠNG TÂY", "CHUYỆN ĐẸP CHƯA CHẮC LÀ CHUYỆN THẬT",
10/03 "ĐỈNH − ĐÓNG CỬA ≈ 40 ĐIỂM" (không màu nến / "3× thân" / giá mở — giá mở 10/03 mâu thuẫn giữa nguồn), nguồn 24/03 không tên
CTCK, "6–7 PHIÊN (NGUỒN KHÁC 16%)", "MỌI NGÀY VỪA GIẢM (5 PHIÊN TRƯỚC)", ba chàng lính trắng "VÀI LẦN", "KHÔNG KẾT QUẢ NÀO ĐỨNG
VỮNG", nghiên cứu Mỹ (S&P 500) cân bằng, "NHỮNG BÀI TỚI".
Lộ trình = CẢNH HẸN TRƯỚC (RETENTION.md): CH00 dựng 5 nến 09–13/03 với dấu "THỨ SÁU · ?", CH04 "nhớ mặt nó", CH05 trả hẹn bằng
đúng cây doji 13/03 (+ 5 / 20 phiên sau).
Cảnh `candles` (chart.js + chartdata.attach): cửa sổ 3–5 phiên = cảnh "giải phẫu" nến to; nến TUẦN = `tf: "1w"` (chartdata.weekly,
gộp trong Python). Màu nến trong engine = đóng so với mở (đúng nội dung CH03).
Luật kênh: chỉ giáo dục, không khuyến nghị, không dự báo; không tên công ty chứng khoán / ứng dụng / mã cổ phiếu (kể cả tên
trường trùng mã); không dẫn bản tin CTCK. Clip Pexels ghi "VIDEO MINH HỌA". Neo: chữ ĐẦU TIÊN của mỗi cảnh neo vào từ ĐẦU câu;
slam đặt cảnh bắt đầu ngay trước chữ đập; counter đếm từ đầu cảnh; dòng ngắn có số ép fx "rise" (khỏi "scramble" ra ký tự rác);
mọi số trên màn hình có nguồn (srcnote/source), số tự tính ghi "KÊNH TỰ TÍNH/ĐẾM".
"""
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
TOPIC = D.name

ILL = "VIDEO MINH HỌA"
SRC_VNI = "DỮ LIỆU: VN-INDEX · HOSE (VNSTOCK/VCI) · KÊNH TỰ TÍNH · MINH HOẠ QUÁ KHỨ, KHÔNG PHẢI KHUYẾN NGHỊ"
SRC_COUNT = "KÊNH TỰ ĐẾM · VN-Index 08/10/2018–06/10/2026, 1.995 phiên (HOSE qua vnstock/VCI) · quá khứ, không phải tín hiệu"
SRC_RULE = "Giá tham chiếu, giá mở cửa (ATO): Quy chế giao dịch VNX, QĐ 22/QĐ-HĐTV ngày 18/04/2025"

# Bảng đọc: giữ nguyên các khoá C2 (VN-Index, HOSE… đổi = đổi khoá cache TTS) + tên riêng của bài này.
SAY = {"vn-index": "Vi En In-đéc", "hose": "hô-dê", "vic": "vi ai xi", "vhm": "vi hát em", "vre": "vi rờ e", "vpl": "vi pê en",
       "ree": "rê ê ê", "sam": "xam", "gdp": "gi đi pi", "etf": "i ti ép", "hnx": "hát en ích", "upcom": "úp-com",
       "margin": "ma-gin", "app": "áp", "vingroup": "Vin-grúp", "vietnambiz": "Việt Nam Biz",
       "fomo": "phô-mô", "vnexpress": "Vi En Ếch-prét",
       "ato": "a tê ô", "atc": "a tê xê", "krx": "ca e-rờ ích", "mtl": "em tê eo", "=LO": "eo ô", "vsd": "vi ét đê",
       "vnx": "vi en ích", "ccp": "xê xê pê", "ubcknn": "Uỷ ban Chứng khoán Nhà nước", "=T": "tê",
       # C3 (factcheck mục 3): doji "đô-gi" cố định; Homma, Bonferroni không có trong lời đọc
       "doji": "đô-gi", "nison": "nai-xơn", "marshall": "mác-sồ", "steve": "xtiv", "zealand": "di-lân", "=New": "niu",
       "dow": "đao", "jones": "giôn"}


def fx_rise(scenes):
    """Dòng ngắn có chữ số (≤ 16 ký tự, không acc) mặc định bị beatfx gán "scramble"/"type" -> ở đầu cảnh hiện ký tự rác
    hoặc trống. Ép "rise" (retro 2 checklist)."""
    for s in scenes:
        for q in (s.get("items") or []) + (s.get("kin") or []):
            t = q.get("text", "")
            if not q.get("fx") and not q.get("acc") and re.search(r"\d", t) and len(t) <= 16:
                q["fx"] = "rise"
    return scenes


def week(at, until, marks, title="VN-INDEX · TUẦN 09–13/03/2026", rng="5 PHIÊN · 5 CÂY NẾN NGÀY", **kw):
    return {"type": "candles", "at": at, "series": "vnindex", "from": "2026-03-09", "to": "2026-03-13", "drawAt": at if isinstance(at, list) else [at, None, 0, 0.15],
            "until": until, "title": title, "range": rng, "ind": [], "source": SRC_VNI, "marks": marks, **kw}


CH = {}

# ---------------- CH00 · Một cây nến đỏ (cold open → cảnh hẹn trước → nhận diện kênh) ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MỘT CÂY NẾN KỂ GÌ"}, "bgm": {"mood": "mystery", "gain": 0.143}, "scenes": [
    {"type": "candles", "series": "vnindex", "from": "2026-03-09", "to": "2026-03-13", "drawAt": [0, "Nhìn", 0, 0.1],
     "until": [0, "đỏ"], "title": "VN-INDEX", "range": "MỘT CÂY NẾN = MỘT NGÀY GIAO DỊCH", "ind": [],
     "source": "VIDEO GIÁO DỤC · KHÔNG PHẢI LỜI KHUYÊN MUA, BÁN · DỮ LIỆU: HOSE (VNSTOCK/VCI), MINH HOẠ QUÁ KHỨ",
     "marks": [{"date": "2026-03-09", "text": "CẢ MỘT NGÀY GIAO DỊCH", "pos": "above", "tone": "gold", "at": [2, "cả"], "dx": 450, "dy": 40}]},
    {"type": "date", "at": 3, "day": "THỨ HAI", "date": "09.03.2026",
     "sub": {"text": "VN-INDEX −115,05 ĐIỂM · NGÀY CỦA BÀI 2", "at": [3, "mất"]},
     "srcnote": "Giá đóng cửa VN-Index (vnstock/VCI) · −115,05 điểm: báo Nhân Dân 09/03/2026"},
    {"type": "candles", "at": 4, "series": "vnindex", "from": "2026-03-09", "to": "2026-03-13", "drawAt": [4, "Cây", 0, 0.1],
     "until": [4, "Cây", 0, 0.5], "title": "VN-INDEX · 09/03/2026", "range": "ĐỌC MỘT CÂY NẾN", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2026-03-09", "text": "MỞ CỬA = CAO NHẤT · 1.757,73", "pos": "above", "tone": "gold", "at": [4, "mở"], "dx": 500, "dy": 40},
               {"date": "2026-03-09", "text": "ĐÓNG CỬA 1.652,79 · CÁCH ĐÁY ≈ 2 ĐIỂM", "pos": "below", "tone": "down", "at": [5, "đóng"], "dx": 200}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "VIỆC CÂY NẾN LÀM RẤT GIỎI", "at": [7, "Đó"], "sm": True},
                                          {"text": "KỂ LẠI MỘT PHIÊN ĐÃ QUA", "at": [7, "kể"]},
                                          {"text": "GỌN TRONG MỘT HÌNH", "at": [7, "gọn"], "acc": True}]},
    {"type": "quote", "at": 8, "typeAt": [9, "Thấy"], "qline": 9, "lbl": "LỜI TRUYỀN MIỆNG · DIỄN Ý",
     "text": "Thấy cây búa là đáy đã tới, thấy ba chàng lính trắng là sóng tăng bắt đầu.", "by": "Lời hay gặp trên mạng (diễn ý)"},
    {"type": "question", "at": 10, "text": "Nhìn nến,\nmình có đoán được\nngày mai không?"},
    {"type": "kinetic", "at": 11, "items": [{"text": "VIDEO NÀY SẼ ĐI TÌM", "at": [11, "Đó"]},
                                           {"text": "BẰNG DỮ LIỆU THẬT", "at": [11, "bằng"], "acc": True}]},
    week(12, [12, "quay"], [{"date": "2026-03-13", "text": "THỨ SÁU · ?", "pos": "above", "tone": "gold", "at": [12, "thứ"], "dx": -60},
                            {"date": "2026-03-13", "text": "CUỐI VIDEO: QUAY LẠI ĐÂY", "pos": "below", "tone": "gold", "at": [13, "Lúc"], "dx": -260}],
         title="CUỐI VIDEO · CÂY NẾN THỨ SÁU", rng="VN-INDEX · 09–13/03/2026"),
    {"type": "brand", "at": 14, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 15, "items": [{"text": "BÀI 3 · CHỨNG KHOÁN TỪ SỐ 0", "at": [15, "Và"], "acc": True},
                                           {"text": "chỉ nhằm giáo dục · không phải lời khuyên mua hay bán", "at": [16, "Video"], "sm": True},
                                           {"text": "không dự báo thị trường", "at": [16, "dự"], "sm": True}]},
]}

# ---------------- CH01 · Bốn con số làm nên một cây nến ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "BỐN CON SỐ LÀM NÊN MỘT CÂY NẾN"}, "bgm": {"mood": "curious", "gain": 0.076}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "BỐN CON SỐ\nLÀM NÊN MỘT CÂY NẾN", "sub": "MỞ CỬA · CAO NHẤT · THẤP NHẤT · ĐÓNG CỬA",
     "vid": "5767251", "illus": ILL, "titleAt": [0, "Ở"]},
    {"type": "timeline", "at": 1, "tag": {"text": "MỘT PHIÊN HOSE · 9:00 → 15:00 · GIỮ LẠI 4 CON SỐ", "at": [1, "Nếu"]}, "items": [
        {"year": "O", "text": "GIÁ MỞ CỬA", "at": [2, "mở"]},
        {"year": "H", "text": "GIÁ CAO NHẤT", "at": [2, "cao"]},
        {"year": "L", "text": "GIÁ THẤP NHẤT", "at": [2, "thấp"]},
        {"year": "C", "text": "GIÁ ĐÓNG CỬA", "at": [2, "đóng"]}],
     "srcnote": "O · H · L · C = open, high, low, close"},
    {"type": "broll", "at": 3, "vid": "16294424", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "NHIỆT ĐỘ MỘT NGÀY Ở NHÀ BẠN", "at": [3, "Hãy"]}]},
    {"type": "ledger", "at": 4, "title": "NHIỆT ĐỘ MỘT NGÀY · VÍ DỤ GIẢ ĐỊNH", "rows": [
        {"k": "SÁNG MỞ CỬA RA", "v": "27°", "at": [4, "Sáng"]},
        {"k": "LÚC NÓNG NHẤT", "v": "35°", "at": [4, "nóng"]},
        {"k": "LÚC MÁT NHẤT", "v": "26°", "at": [4, "mát"]},
        {"k": "TỐI VỀ", "v": "29°", "at": [4, "tối"]}],
     "total": {"k": "CHỈ GHI BUỔI TỐI", "v": "29° — KHÔNG BIẾT CẢ NGÀY", "at": [5, "buổi"]},
     "srcnote": "Ví dụ giả định để minh hoạ, không phải số đo thật"},
    {"type": "kinetic", "at": 6, "items": [{"text": "BIỂU ĐỒ ĐƯỜNG TRÊN BÁO", "at": [6, "Biểu"], "sm": True},
                                          {"text": "THƯỜNG CHỈ NỐI GIÁ ĐÓNG CỬA", "at": [6, "thường"], "acc": True}]},
    {"type": "candles", "at": 7, "series": "vnindex", "from": "2026-03-09", "to": "2026-03-13", "drawAt": [7, "Cây", 0, 0.1],
     "until": [7, "giữ"], "title": "GIẢI PHẪU CÂY NẾN", "range": "VN-INDEX · 09–13/03/2026 · O · H · L · C", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2026-03-09", "text": "THÂN = MỞ CỬA → ĐÓNG CỬA", "pos": "above", "tone": "gold", "at": [8, "Phần"], "dx": 450, "dy": 40},
               {"date": "2026-03-10", "text": "BÓNG TRÊN → CAO NHẤT", "pos": "above", "tone": "up", "at": [9, "trên"], "dx": 60},
               {"date": "2026-03-10", "text": "BÓNG DƯỚI → THẤP NHẤT", "pos": "below", "tone": "down", "at": [9, "dưới"], "dx": 400}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "1 CÂY NẾN = 1 PHIÊN", "at": [10, "Vậy"], "acc": True}]},
    {"type": "candles", "at": 11, "series": "vnindex", "from": "2026-02-02", "to": "2026-04-03", "drawAt": [11, "Biểu", 0, 0.1],
     "until": [11, "phải"], "title": "BIỂU ĐỒ NẾN NGÀY · VN-INDEX", "range": "02/2026 – 04/2026 · TỪ TRÁI SANG PHẢI", "ind": [],
     "source": SRC_VNI},
    {"type": "question", "at": 12, "text": "Mà sao lại\ngọi là nến?"},
    {"type": "broll", "at": 13, "vid": "12550702", "veil": 0.45, "illus": ILL,
     "kin": [{"text": "THÂN NẾN", "at": [13, "Vì"]},
             {"text": "BÓNG PHÍA TRÊN ≈ SỢI BẤC", "at": [13, "bóng"], "acc": True}]},
    {"type": "broll", "at": 14, "vid": "6365257", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "CÁCH VẼ ĐẾN TỪ NHẬT BẢN", "at": [14, "Cách"]},
             {"text": "CHUYỆN KỂ: THƯƠNG NHÂN GẠO, THẾ KỶ 18", "at": [15, "thương"], "acc": True}]},
    {"type": "ledger", "at": 16, "title": "CHUYỆN KỂ vs NGUỒN", "rows": [
        {"k": "CHUYỆN KỂ", "v": "THƯƠNG NHÂN GẠO, THẾ KỶ 18", "at": [16, "Người", 0, 0.05]},
        {"k": "STEVE NISON (1991)", "v": "PHỔ BIẾN NẾN Ở PHƯƠNG TÂY", "at": [16, "Steve"]},
        {"k": "NISON (1994)", "v": "KHÓ CÓ CHUYỆN THƯƠNG NHÂN ẤY DÙNG NẾN", "at": [17, "chưa"]}],
     "total": {"k": "NHIỀU KHẢ NĂNG", "v": "ĐẦU THỜI MINH TRỊ, CUỐI THẾ KỶ 19", "at": [18, "muộn"]},
     "srcnote": "Nison, Beyond Candlesticks (Wiley, 1994), qua Wikipedia \"Candlestick chart\""},
    {"type": "slam", "at": [19, "Một", 0, -0.3], "hitAt": [19, "Một"], "text": "CHUYỆN ĐẸP\nCHƯA CHẮC LÀ CHUYỆN THẬT",
     "sub": "GIỮ Ý NÀY · LÁT NỮA NÓ QUAY LẠI"},
]}

# ---------------- CH02 · Thân và bóng: phiên ấy ai thắng ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "THÂN VÀ BÓNG: PHIÊN ẤY AI THẮNG"}, "bgm": {"mood": "warm", "gain": 0.129}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "THÂN VÀ BÓNG:\nPHIÊN ẤY AI THẮNG", "sub": "HAI CÂU HỎI CHO MỘT CÂY NẾN",
     "titleAt": [0, "Đọc"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "CÂU 1 · THÂN DÀI HAY NGẮN?", "at": [1, "Câu"], "acc": True},
                                          {"text": "THÂN DÀI: GIÁ ĐI XA THEO MỘT HƯỚNG", "at": [2, "Thân"]},
                                          {"text": "THÂN RẤT NGẮN: HẾT PHIÊN, GẦN NHƯ VỀ CHỖ CŨ", "at": [3, "Thân"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "CÂU 2 · BÓNG DÀI Ở PHÍA NÀO?", "at": [4, "Câu"], "acc": True},
                                          {"text": "BÓNG TRÊN DÀI: LÊN CAO, KHÔNG GIỮ ĐƯỢC", "at": [5, "Bóng"]},
                                          {"text": "BÓNG DƯỚI DÀI: XUỐNG SÂU, ĐƯỢC KÉO LÊN", "at": [6, "Bóng"]}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "BÊN MUA · KÉO CO · BÊN BÁN", "at": [7, "Người"]},
                                          {"text": "BÓNG = CHỖ MỘT BÊN ĐÃ KÉO TỚI, RỒI BỊ KÉO VỀ", "at": [8, "Bóng"], "acc": True}]},
    {"type": "candles", "at": 9, "series": "vnindex", "from": "2026-03-09", "to": "2026-03-13", "drawAt": [9, "Thử", 0, 0.1],
     "until": [9, "sau"], "title": "VN-INDEX · 09–13/03/2026", "range": "THỨ BA 10/03 · THỨ TƯ 11/03", "ind": [],
     "source": "DỮ LIỆU: VN-INDEX (VNSTOCK/VCI) · GIÁ MỞ 10/03 KHÁC NHAU GIỮA CÁC NGUỒN DỮ LIỆU · ĐỈNH 10/03: TBTC, VNEXPRESS · KHÔNG PHẢI KHUYẾN NGHỊ",
     "marks": [{"date": "2026-03-10", "text": "VỌT LÊN ≈ 1.717 · ĐÓNG 1.676,73", "pos": "above", "tone": "gold", "at": [11, "vọt"], "dx": 200, "dy": -40},
               {"date": "2026-03-10", "text": "ĐỈNH − ĐÓNG CỬA ≈ 40 ĐIỂM", "pos": "below", "tone": "gold", "at": [13, "bốn"], "dx": 60},
               {"date": "2026-03-11", "text": "+3,08% · MỞ ≈ ĐÁY, ĐÓNG ≈ ĐỈNH", "pos": "above", "tone": "up", "at": [15, "Thứ"], "dy": -70}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "THỨ TƯ 11/03 · NẾN XANH DÀI", "at": [16, "Chỉ"], "sm": True},
                                           {"text": "MỞ GẦN ĐÁY · ĐÓNG GẦN ĐỈNH · +3,08%", "at": [16, "đóng"]},
                                           {"text": "BÊN BÁN GẦN NHƯ KHÔNG KÉO LẠI ĐƯỢC", "at": [17, "Cả"], "acc": True}],
     "srcnote": "Giá VN-Index 11/03/2026 (vnstock/VCI) · kênh tự tính"},
    {"type": "question", "at": 18, "text": "Nến xanh dài là tốt,\nnến đỏ dài là xấu?"},
    {"type": "slam", "at": [19, "Cây", 0, -0.3], "hitAt": [19, "Cây"], "text": "NẾN KỂ PHIÊN ĐÃ QUA", "sub": "KHÔNG HỨA PHIÊN SAU"},
    {"type": "kinetic", "at": 20, "items": [{"text": "PHIÊN SAU CÓ ĐI TIẾP HƯỚNG ẤY?", "at": [20, "Còn"]},
                                           {"text": "LÁT NỮA KÊNH ĐẾM THỬ", "at": [20, "Lát"], "acc": True}]},
]}

# ---------------- CH03 · Xanh, đỏ, và cái bẫy màu ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "XANH, ĐỎ, VÀ CÁI BẪY MÀU"}, "bgm": {"mood": "calm", "gain": 0.123}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "XANH, ĐỎ,\nVÀ CÁI BẪY MÀU", "sub": "HAI THỨ MÀU · HAI CÁI MỐC",
     "titleAt": [0, "Giờ"]},
    {"type": "ledger", "at": 1, "title": "HAI THỨ MÀU, HAI CÁI MỐC", "rows": [
        {"k": "MÀU NẾN", "v": "ĐÓNG CỬA so với MỞ CỬA", "at": [1, "Trên"]},
        {"k": "→ XANH / ĐỎ", "v": "ĐÓNG CAO HƠN / THẤP HƠN MỞ", "at": [2, "Nến"]},
        {"k": "MÀU BẢNG GIÁ", "v": "GIÁ so với THAM CHIẾU", "at": [4, "Trên"]}],
     "total": {"k": "THAM CHIẾU", "v": "= ĐÓNG CỬA PHIÊN HÔM TRƯỚC", "at": [4, "tức"]},
     "srcnote": SRC_RULE + " · màu bảng giá: quy ước hiển thị phổ biến"},
    {"type": "kinetic", "at": 5, "items": [{"text": "HAI CÁI MỐC KHÁC NHAU", "at": [5, "Hai"], "acc": True}]},
    {"type": "candles", "at": 6, "series": "vnindex", "from": "2026-03-19", "to": "2026-03-27", "drawAt": [6, "Nên", 0, 0.1],
     "until": [6, "lại"], "title": "VN-INDEX · 19–27/03/2026", "range": "NẾN ĐỎ MÀ CHỈ SỐ TĂNG?", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2026-03-23", "text": "1.591,17 · ĐÓNG CỬA THẤP NHẤT 2026 (TỚI 06/10)", "pos": "below", "tone": "down", "at": [8, "thấp"], "dx": 60},
               {"date": "2026-03-24", "text": "24/03 · MỞ CAO VỌT ≈ 1.626", "pos": "above", "tone": "gold", "at": [9, "mở"], "dx": 200, "dy": -200},
               {"date": "2026-03-24", "text": "ĐÓNG 1.614,77 → NẾN ĐỎ", "pos": "below", "tone": "down", "at": [10, "đóng"], "dx": 450, "dy": -60}]},
    {"type": "ledger", "at": 11, "title": "24/03/2026 · VN-INDEX", "rows": [
        {"k": "THAM CHIẾU (ĐÓNG CỬA 23/03)", "v": "1.591,17", "at": [11, "So", 0, 0.05]},
        {"k": "ĐÓNG CỬA 24/03", "v": "1.614,77", "at": [11, "hôm"]},
        {"k": "SO HÔM TRƯỚC → BẢNG GIÁ XANH", "v": "+23,60 (+1,48%)", "at": [11, "tăng"]},
        {"k": "MỞ CỬA", "v": "≈ 1.626", "at": [12, "So"]}],
     "total": {"k": "SO VỚI MỞ CỬA → NẾN ĐỎ", "v": "≈ −11,6", "at": [12, "Cây"]},
     "srcnote": "Thời báo Tài chính, Người Lao Động, Vietnambiz 24/03/2026 (đóng cửa +23,60; đầu phiên tăng hơn 30 điểm) · giá mở: dữ liệu HOSE qua vnstock/VCI"},
    {"type": "question", "at": 13, "text": "Vậy hôm đó là ngày tăng\nhay ngày giảm?"},
    {"type": "slam", "at": [14, "Cả", 0, -0.3], "hitAt": [14, "Cả"], "text": "HAI MÀU · HAI CÂU HỎI", "sub": "CẢ HAI ĐỀU ĐÚNG"},
    {"type": "kinetic", "at": 15, "items": [{"text": "MÀU NẾN: TRONG PHIÊN, ĐI LÊN HAY ĐI XUỐNG?", "at": [15, "Màu"]},
                                           {"text": "MÀU BẢNG GIÁ: SO VỚI HÔM QUA?", "at": [15, "Màu", 1], "acc": True}]},
    {"type": "counter", "at": 16, "from": 0, "to": 15, "suffix": "%", "label": "PHIÊN CÓ MÀU NẾN NGƯỢC MÀU BẢNG GIÁ",
     "sub": {"text": "≈ 1 PHIÊN / 6–7 PHIÊN · VN-INDEX 10/2018–10/2026 · KÊNH TỰ ĐẾM (NGUỒN DỮ LIỆU KHÁC: 16%)", "at": [16, "sáu"]},
     "srcnote": "Kênh tự tính · 302 / 1.990 phiên = 15,2% (vnstock/VCI) · nguồn dữ liệu thứ ba: 16,4%"},
    {"type": "kinetic", "at": 17, "items": [{"text": "RỖNG / ĐẶC · HAY MÀU KHÁC HẲN", "at": [17, "Có"], "sm": True},
                                           {"text": "XEM CHÚ THÍCH MÀU CỦA CHÍNH BIỂU ĐỒ", "at": [18, "Nên"], "acc": True}]},
]}

# ---------------- CH04 · Đọc một tuần, rồi gộp thành một cây ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "ĐỌC MỘT TUẦN, RỒI GỘP THÀNH MỘT CÂY"}, "bgm": {"mood": "upbeat", "gain": 0.093}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "ĐỌC MỘT TUẦN,\nRỒI GỘP THÀNH MỘT CÂY", "sub": "NẾN NGÀY · NẾN TUẦN · KHUNG THỜI GIAN",
     "titleAt": [0, "Giờ"]},
    week(1, [1, "năm", 1], [
        {"date": "2026-03-09", "text": "BÊN BÁN THẮNG TRỌN PHIÊN", "pos": "below", "tone": "down", "at": [2, "Thứ"], "dx": 40},
        {"date": "2026-03-10", "text": "BỊ ĐẨY LÙI TỪ TRÊN CAO", "pos": "above", "tone": "gold", "at": [3, "Thứ"], "dx": 100, "dy": -40},
        {"date": "2026-03-11", "text": "BÊN MUA GIỮ TỚI CUỐI", "pos": "below", "tone": "up", "at": [4, "Thứ"], "dy": 60},
        {"date": "2026-03-12", "text": "MỞ THẤP HƠN HÔM TRƯỚC · −1,08%", "pos": "below", "tone": "down", "at": [5, "Thứ"], "dx": -150, "dy": 80},
        {"date": "2026-03-13", "text": "DOJI · THÂN 1,48 / BIÊN 28 ĐIỂM", "pos": "above", "tone": "gold", "at": [7, "chưa"], "dx": -200, "dy": -120}],
         title="TUẦN 09–13/03/2026 · NĂM CÂY NẾN", rng="VN-INDEX · NẾN NGÀY"),
    {"type": "slam", "at": [8, "doji", 0, -0.3], "hitAt": [8, "doji"], "text": "DOJI", "sub": "NHỚ MẶT NÓ · CUỐI VIDEO QUAY LẠI"},
    {"type": "kinetic", "at": 9, "items": [{"text": "THỬ MỘT VIỆC", "at": [9, "Giờ"], "sm": True},
                                          {"text": "GỘP 5 PHIÊN → 1 CÂY NẾN", "at": [9, "gộp"], "acc": True}]},
    {"type": "ledger", "at": 10, "title": "NẾN TUẦN 09–13/03/2026", "rows": [
        {"k": "MỞ CỬA = MỞ SÁNG THỨ HAI", "v": "1.757,73", "at": [10, "Mở"]},
        {"k": "ĐÓNG CỬA = ĐÓNG CHIỀU THỨ SÁU", "v": "1.696,24", "at": [10, "Đóng"]},
        {"k": "CAO NHẤT = ĐỈNH CẢ TUẦN", "v": "1.757,73", "at": [11, "Cao"]},
        {"k": "THẤP NHẤT = ĐÁY CẢ TUẦN", "v": "1.650,75", "at": [11, "thấp"]}],
     "srcnote": "Kênh tự tính từ nến ngày VN-Index (vnstock/VCI)"},
    {"type": "candles", "at": 12, "series": "vnindex", "tf": "1w", "from": "2026-02-23", "to": "2026-03-27", "drawAt": [12, "Ta", 0, 0.1],
     "until": [12, "tuần"], "title": "VN-INDEX · NẾN TUẦN", "range": "5 TUẦN · 23/02 – 27/03/2026 · MỖI CÂY = 1 TUẦN", "ind": [],
     "source": "DỮ LIỆU: VN-INDEX (VNSTOCK/VCI) · NẾN TUẦN KÊNH TỰ GỘP TỪ NẾN NGÀY · KHÔNG PHẢI KHUYẾN NGHỊ",
     "marks": [{"date": "2026-03-09", "text": "THÂN ĐỎ", "pos": "above", "tone": "gold", "at": [12, "thân"]},
               {"date": "2026-03-09", "text": "BÓNG DƯỚI KHÁ DÀI", "pos": "below", "tone": "down", "at": [12, "bóng"]},
               {"date": "2026-03-09", "text": "TUẦN 09–13/03: −4,05% SO VỚI TUẦN TRƯỚC", "pos": "below", "tone": "down", "at": [13, "bốn"], "dx": 380, "dy": 80}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "5 NẾN NGÀY: MỘT CUỘC GIẰNG CO", "at": [14, "Cùng"]},
                                           {"text": "1 NẾN TUẦN: MỘT TUẦN GIẢM, CÓ HỒI LẠI", "at": [14, "cây", 1, -0.2], "acc": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "KHUNG THỜI GIAN", "at": [15, "Đó"], "acc": True}]},
    {"type": "candles", "at": 16, "series": "vnindex", "from": "2026-01-05", "to": "2026-10-06", "drawAt": [16, "Nến", 0, 0.1],
     "until": [16, "mỗi"], "title": "NẾN NGÀY · MỖI CÂY = 1 PHIÊN", "range": "VN-INDEX · 05/01 – 06/10/2026", "ind": [], "source": SRC_VNI},
    {"type": "candles", "at": [16, "Nến", 1, -0.15], "series": "vnindex", "tf": "1w", "from": "2026-01-05", "to": "2026-10-06",
     "drawAt": [16, "Nến", 1], "until": [16, "tuần", 1], "title": "NẾN TUẦN · MỖI CÂY = 1 TUẦN", "range": "VN-INDEX · 05/01 – 06/10/2026",
     "ind": [], "source": "DỮ LIỆU: VN-INDEX (VNSTOCK/VCI) · NẾN TUẦN KÊNH TỰ GỘP TỪ NẾN NGÀY · KHÔNG PHẢI KHUYẾN NGHỊ"},
    {"type": "kinetic", "at": 17, "items": [{"text": "CÒN CÓ NẾN THÁNG", "at": [17, "Còn"]},
                                           {"text": "NẾN 1 GIỜ · NẾN 5 PHÚT", "at": [17, "giờ"], "acc": True}]},
    {"type": "bars", "at": 18, "title": "VN-INDEX · 05/01 → 06/10/2026", "unit": "SỐ CÂY NẾN · KÊNH TỰ ĐẾM", "items": [
        {"k": "NẾN NGÀY", "v": 186, "lbl": "186", "at": [18, "trăm"]},
        {"k": "NẾN TUẦN", "v": 39, "lbl": "≈ 39", "at": [18, "ba", 0], "acc": True}],
     "srcnote": "Kênh tự đếm · 186 phiên; 39 tuần (tuần cuối 05–06/10 chưa trọn) · vnstock/VCI"},
    {"type": "question", "at": 19, "text": "Vậy xem khung nào\nmới đúng?"},
    {"type": "kinetic", "at": 20, "items": [{"text": "KHÔNG KHUNG NÀO ĐÚNG HƠN", "at": [20, "Không"], "acc": True},
                                           {"text": "KHUNG NHỎ: NHIỀU CHI TIẾT, NHIỀU NHIỄU", "at": [21, "Khung"]},
                                           {"text": "KHUNG LỚN: GỌN HƠN, PHẢN ỨNG CHẬM HƠN", "at": [21, "Khung", 1]}]},
    {"type": "kinetic", "at": 22, "items": [{"text": "AI CHỈ CHO BẠN MỘT CÂY NẾN?", "at": [22, "Nên"], "sm": True},
                                           {"text": "NẾN NGÀY, HAY NẾN TUẦN?", "at": [22, "hỏi"], "acc": True}]},
]}

# ---------------- CH05 · Điều cây nến không nói được ----------------
QUOTE_BY = "B. Marshall, luận án tiến sĩ, Massey University (2005) — cơ sở của bài J. Banking & Finance 2006"
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "ĐIỀU CÂY NẾN KHÔNG NÓI ĐƯỢC"}, "bgm": {"mood": "calm", "gain": 0.09}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "ĐIỀU CÂY NẾN\nKHÔNG NÓI ĐƯỢC", "sub": "KÊNH TỰ ĐẾM 8 NĂM VN-INDEX",
     "titleAt": [0, "Giờ"]},
    {"type": "ledger", "at": 1, "title": "BA MẪU NẾN QUEN TÊN · LỜI TRUYỀN MIỆNG (DIỄN Ý)", "rows": [
        {"k": "CÂY BÚA", "v": "\"BÁO ĐÁY\"", "at": [2, "búa"]},
        {"k": "DOJI", "v": "\"SẮP ĐẢO CHIỀU\"", "at": [2, "doji"]},
        {"k": "BA CHÀNG LÍNH TRẮNG", "v": "\"SÓNG TĂNG BẮT ĐẦU\"", "at": [2, "lính"]}],
     "srcnote": "Tên mẫu: Nison (1991) · \"…\" = lời truyền miệng diễn ý, không phải kết luận"},
    {"type": "candles", "at": 3, "series": "vnindex", "from": "2026-06-03", "to": "2026-06-09", "drawAt": [3, "Cây", 0, 0.1],
     "until": [3, "búa"], "title": "VÍ DỤ HÌNH CÂY BÚA", "range": "VN-INDEX · 03–09/06/2026 · CHỈ MINH HOẠ HÌNH DẠNG", "ind": [],
     "source": SRC_VNI,
     "marks": [{"date": "2026-06-09", "text": "CÂY BÚA: BÓNG DƯỚI ≥ 2× THÂN", "pos": "below", "tone": "gold", "at": [3, "bóng"], "dx": -300}]},
    {"type": "candles", "at": 5, "series": "vnindex", "from": "2026-03-09", "to": "2026-03-13", "drawAt": [5, "Doji", 0, 0.1],
     "until": [5, "như"], "title": "DOJI · CÂY NẾN THỨ SÁU", "range": "VN-INDEX · 09–13/03/2026", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2026-03-13", "text": "DOJI · \"LƯỠNG LỰ\"", "pos": "above", "tone": "gold", "at": [5, "lưỡng"], "dx": -120}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "BA CHÀNG LÍNH TRẮNG", "at": [6, "Ba"]},
                                          {"text": "3 NẾN XANH DÀI NỐI NHAU, SAU MỘT ĐỢT GIẢM", "at": [6, "ba", 1]},
                                          {"text": "\"SÓNG TĂNG BẮT ĐẦU\" · DIỄN Ý", "at": [6, "sóng"], "acc": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "KÊNH TỰ ĐẾM", "at": [7, "Kênh"], "acc": True},
                                          {"text": "VN-INDEX · 08/10/2018 → 06/10/2026 · 1.995 PHIÊN", "at": [7, "VN-Index"]},
                                          {"text": "quá khứ · không phải tín hiệu", "at": [7, "tới"], "sm": True}],
     "srcnote": "Dữ liệu: HOSE (vnstock/VCI), kênh tự tính. Minh hoạ quá khứ, không phải khuyến nghị."},
    {"type": "kinetic", "at": 8, "items": [{"text": "TRƯỚC HẾT: MỘT CÁI MỐC ĐỂ SO", "at": [8, "Nhưng"], "acc": True},
                                          {"text": "CHỌN BỪA MỘT NGÀY BẤT KỲ", "at": [9, "Chọn"]},
                                          {"text": "→ 5 PHIÊN SAU · 20 PHIÊN SAU", "at": [9, "năm"]}]},
    {"type": "counter", "at": 10, "from": 0, "to": 59, "suffix": "%", "label": "NGÀY BẤT KỲ → 20 PHIÊN SAU CHỈ SỐ CAO HƠN",
     "sub": {"text": "5 PHIÊN SAU: 58,5% · MỐC SO SÁNH · KHÔNG PHẢI 50%", "at": [10, "cao"]},
     "srcnote": SRC_COUNT + " · n = 1.971 / 1.986"},
    {"type": "candles", "at": 11, "series": "vnindex", "from": "2018-10-08", "to": "2026-10-06", "drawAt": [11, "Vì", 0, 0.1],
     "until": [11, "năm"], "title": "VN-INDEX · 8 NĂM", "range": "10/2018 – 10/2026 · NẾN NGÀY", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2018-10-08", "text": "996", "pos": "below", "tone": "gold", "at": [11, "từ"], "dx": 60},
               {"date": "2026-10-06", "text": "1.759", "pos": "above", "tone": "gold", "at": [11, "lên"], "dx": -60}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "MẪU NẾN MUỐN \"BÁO TĂNG\"", "at": [12, "Nên"], "sm": True},
                                           {"text": "PHẢI THẮNG ≈ 6/10", "at": [12, "thắng"], "acc": True},
                                           {"text": "KHÔNG PHẢI 50%", "at": [12, "không"]}]},
    {"type": "question", "at": 13, "text": "Thế cây búa\nthì sao?"},
    {"type": "kinetic", "at": 14, "items": [{"text": "CÂY BÚA ĐÚNG SÁCH", "at": [14, "Cây"]},
                                           {"text": "35 LẦN TRONG 8 NĂM", "at": [14, "ba"], "acc": True}],
     "srcnote": SRC_COUNT},
    {"type": "bars", "at": 15, "title": "SAU 5 PHIÊN, CHỈ SỐ CAO HƠN (% SỐ LẦN)",
     "unit": "KÊNH TỰ ĐẾM · QUÁ KHỨ", "max": 70, "items": [
        {"k": "CÂY BÚA (35 LẦN)", "v": 51.4, "lbl": "51,4%", "at": [15, "năm", 1], "acc": True},
        {"k": "MỌI NGÀY VỪA GIẢM (5 PHIÊN TRƯỚC)", "v": 56.3, "lbl": "56,3%", "at": [16, "năm", 1]}],
     "srcnote": SRC_COUNT + " · n = 35 / 817"},
    {"type": "kinetic", "at": 17, "items": [{"text": "SAU 20 PHIÊN: CŨNG KHÔNG HƠN MỐC", "at": [17, "Đo"]},
                                           {"text": "35 LẦN LÀ ÍT", "at": [17, "Ba"], "acc": True},
                                           {"text": "chênh nhỏ, theo chiều nào cũng chưa nói lên điều gì", "at": [17, "chênh"], "sm": True}],
     "srcnote": SRC_COUNT},
    {"type": "kinetic", "at": 18, "items": [{"text": "DOJI ≈ 200 LẦN", "at": [18, "Doji"], "acc": True},
                                           {"text": "NẾU BÁO ĐẢO CHIỀU → PHẢI HAY ĐỔI HƯỚNG HƠN", "at": [19, "Nếu"]}],
     "srcnote": SRC_COUNT + " · VCI 201 lần · nguồn dữ liệu khác 189"},
    {"type": "bars", "at": 20, "title": "SAU 5 PHIÊN, CHỈ SỐ ĐỔI CHIỀU (% SỐ LẦN)",
     "unit": "KÊNH TỰ ĐẾM · QUÁ KHỨ", "max": 60, "items": [
        {"k": "SAU DOJI (201 LẦN)", "v": 42.8, "lbl": "42,8%", "at": [20, "bốn"], "acc": True},
        {"k": "NGÀY THƯỜNG", "v": 45.0, "lbl": "45,0%", "at": [20, "Ngày"]}],
     "srcnote": SRC_COUNT + " · đổi chiều = hướng 5 phiên sau ngược hướng 5 phiên trước"},
    {"type": "kinetic", "at": 21, "items": [{"text": "BA CHÀNG LÍNH TRẮNG ĐÚNG SÁCH", "at": [21, "Còn"]},
                                           {"text": "CHỈ VÀI LẦN TRONG 8 NĂM", "at": [21, "vài"]},
                                           {"text": "0 LẦN TỪ 2023", "at": [21, "chưa"], "acc": True},
                                           {"text": "QUÁ ÍT ĐỂ KẾT LUẬN", "at": [22, "Vài"]}],
     "srcnote": SRC_COUNT + " · VCI 5 lần · nguồn dữ liệu khác 2 lần"},
    {"type": "kinetic", "at": 23, "items": [{"text": "HƠN 20 PHÉP SO", "at": [23, "Công"]},
                                           {"text": "VÀI KẾT QUẢ THOẠT NHÌN \"ĐẸP\"", "at": [23, "vài"]},
                                           {"text": "KHÔNG KẾT QUẢ NÀO ĐỨNG VỮNG KHI TÍNH ĐỦ SỐ PHÉP THỬ", "at": [24, "Nhưng"], "acc": True},
                                           {"text": "và chưa trừ phí", "at": [24, "chưa"], "sm": True}],
     "srcnote": "Kênh tự tính · 27 phép so · hiệu chỉnh nhiều phép thử (Bonferroni 0,05/27 ≈ 0,002; p nhỏ nhất 0,047)"},
    {"type": "broll", "at": 25, "vid": "7450200", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "CHẠY ĐỦ NHIỀU PHÉP THỬ", "at": [25, "Chạy"]},
             {"text": "KIỂU GÌ CŨNG GẶP VÀI KẾT QUẢ ĐẸP", "at": [25, "kiểu"]},
             {"text": "5 MẶT NGỬA LIỀN", "at": [25, "mặt"], "acc": True}]},
    {"type": "kinetic", "at": 26, "items": [{"text": "CÁCH KÊNH ĐẾM", "at": [26, "Cách"]},
                                           {"text": "TÓM TẮT Ở PHẦN MÔ TẢ", "at": [26, "tóm"], "acc": True}]},
    {"type": "question", "at": 27, "text": "Thế các nhà nghiên cứu\nthì nói sao?"},
    {"type": "broll", "at": 28, "vid": "18969594", "veil": 0.6, "illus": ILL,
     "kin": [{"text": "BEN MARSHALL & CS. · NEW ZEALAND", "at": [28, "Nhóm"]},
             {"text": "HÀNG CHỤC MẪU NẾN · CỔ PHIẾU DOW JONES", "at": [28, "hàng"]},
             {"text": "≈ 10 NĂM DỮ LIỆU", "at": [28, "mười"], "acc": True}],
     "srcnote": "Marshall, Young & Rose, Journal of Banking & Finance 30(8), 2006"},
    {"type": "quote", "at": 29, "typeAt": [30, None, 0, 0.0], "qline": 30, "lbl": "TRÍCH DỊCH",
     "text": "Phân tích kỹ thuật bằng nến không có giá trị.", "by": QUOTE_BY},
    {"type": "ledger", "at": 31, "title": "CÁC NGHIÊN CỨU", "rows": [
        {"k": "MỸ · DOW JONES · ≈ 10 NĂM", "v": "KHÔNG TẠO GIÁ TRỊ", "at": [31, None, 0, 0.15]},
        {"k": "NHẬT · 1975–2004", "v": "KHÔNG LỢI NHUẬN", "at": [31, "Nhật"]},
        {"k": "THÁI LAN · 2006–2016", "v": "ĐA SỐ KHÔNG KHÁC 0", "at": [32, "Thái"]},
        {"k": "VIỆT NAM · 2013–2018", "v": "KHÔNG DỰ BÁO ĐƯỢC", "at": [33, "Việt"]}],
     "total": {"k": "MỸ, ĐÀI LOAN, TRUNG QUỐC", "v": "VÀI MẪU CÓ ÍCH", "at": [34, "Mỹ"]},
     "srcnote": "Marshall & cs. 2006 (DJIA), 2008 (Nhật) · Tharavanij & cs. 2017 (SET50) · Ngô Tùng Sơn & cs. 2018 · có ích trong vài điều kiện: Caginalp & Laurent 1998 (S&P 500, 1992–96), Lu 2014, Zhu & cs. 2016"},
    {"type": "kinetic", "at": 36, "items": [{"text": "CÂU TRẢ LỜI TRUNG THỰC", "at": [36, "Nên"], "sm": True},
                                           {"text": "NẾU CÓ TÍN HIỆU, NÓ RẤT MỜ", "at": [36, "tín"]},
                                           {"text": "VÀ KHÔNG ỔN ĐỊNH", "at": [36, "không"], "acc": True}]},
    {"type": "candles", "at": 37, "series": "vnindex", "from": "2026-03-02", "to": "2026-04-14", "drawAt": [37, "Giờ", 0, 0.1],
     "until": [37, "hẹn"], "title": "CẢNH ĐÃ HẸN · CÂY DOJI 13/03", "range": "VN-INDEX · 02/03 – 14/04/2026 · NHÌN LẠI", "ind": [],
     "source": "DỮ LIỆU: VN-INDEX (VNSTOCK/VCI) · KÊNH TỰ TÍNH · NHÌN LẠI SAU KHI ĐÃ BIẾT KẾT THÚC · KHÔNG PHẢI KHUYẾN NGHỊ",
     "marks": [{"date": "2026-03-13", "text": "DOJI 13/03", "pos": "above", "tone": "gold", "at": [37, "doji"], "dy": -40},
               {"date": "2026-03-20", "text": "5 PHIÊN SAU: −2,9%", "pos": "below", "tone": "down", "at": [38, "thấp"], "dx": -330, "dy": -40},
               {"date": "2026-03-23", "text": "THẤP NHẤT NĂM (ĐÓNG CỬA)", "pos": "below", "tone": "down", "at": [39, "thấp"], "dx": 330},
               {"date": "2026-04-10", "text": "20 PHIÊN SAU: +3,2%", "pos": "above", "tone": "up", "at": [40, "cao"], "dx": -120}]},
    {"type": "kinetic", "at": 41, "items": [{"text": "BÁO GIẢM? BÁO TĂNG?", "at": [41, "Ai"]},
                                           {"text": "NHÌN LẠI, ĐỀU TÌM ĐƯỢC BẰNG CHỨNG", "at": [41, "nhìn"], "acc": True}]},
    {"type": "slam", "at": [42, "Một", 0, -0.3], "hitAt": [42, "Một"], "text": "KỂ SAU KHI BIẾT KẾT THÚC",
     "sub": "CHUYỆN ĐẸP CHƯA CHẮC LÀ CHUYỆN THẬT"},
]}

# ---------------- CH06 · Áp dụng cho bạn, và khi nào không đúng ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "ÁP DỤNG CHO BẠN"}, "bgm": {"mood": "warm", "gain": 0.101}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "ÁP DỤNG CHO BẠN —\nVÀ KHI NÀO KHÔNG ĐÚNG",
     "sub": "KHÔNG PHẢI LỜI KHUYÊN MUA HAY BÁN", "titleAt": [0, "Mình"]},
    {"type": "ledger", "at": 1, "title": "4 CÂU KHI NHÌN MỘT CÂY NẾN", "rows": [
        {"k": "01", "v": "NẾN NGÀY, NẾN TUẦN, HAY KHUNG KHÁC?", "at": [2, "Một"]},
        {"k": "02", "v": "MÀU SO VỚI MỞ CỬA HAY THAM CHIẾU?", "at": [3, "Hai"]},
        {"k": "03", "v": "THÂN, BÓNG KỂ GÌ VỀ PHIÊN ĐÃ QUA?", "at": [4, "Ba"]},
        {"k": "04", "v": "ĐỌC LẠI QUÁ KHỨ, HAY ĐOÁN NGÀY MAI?", "at": [5, "Bốn"]}],
     "total": {"k": "NẾU LÀ ĐOÁN", "v": "ĐÃ AI ĐẾM, SO VỚI MỐC?", "at": [6, "Nếu"]}},
    {"type": "ledger", "at": 7, "title": "KHI NÀO KHÔNG ĐÚNG", "rows": [
        {"k": "01", "v": "CHỈ ĐẾM TRÊN VN-INDEX · 8 NĂM · CHƯA PHÍ", "at": [8, "Phép"]},
        {"k": "02", "v": "CỔ PHIẾU ÍT GIAO DỊCH: NẾN = VÀI LỆNH", "at": [9, "Với"]},
        {"k": "03", "v": "GIÁ MỞ CỬA = GIÁ KHỚP ATO (BÀI 2)", "at": [10, "Giá"]},
        {"k": "04", "v": "GIÁ CŨ BỊ ĐIỀU CHỈNH SAU CỔ TỨC / THƯỞNG", "at": [11, "Và"]}],
     "srcnote": SRC_RULE},
    {"type": "candles", "at": 13, "series": "vnindex", "from": "2026-03-09", "to": "2026-03-13", "drawAt": [13, "Tóm", 0, 0.1],
     "until": [13, "cây"], "title": "VN-INDEX · 09/03/2026", "range": "MỘT CÂY NẾN, MỘT PHIÊN", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2026-03-09", "text": "4 CON SỐ · 1 PHIÊN · 1 HÌNH", "pos": "above", "tone": "gold", "at": [13, "bốn"], "dx": 450, "dy": 40}]},
    {"type": "slam", "at": [14, "Nó", 0, -0.3], "hitAt": [14, "Nó"], "text": "KỂ GIỎI CHUYỆN ĐÃ QUA", "sub": "KHÔNG HỨA CHUYỆN SẼ TỚI"},
    {"type": "candles", "at": 16, "series": "vnindex", "from": "2026-05-04", "to": "2026-10-06", "drawAt": [16, "Ở", 0, 0.1],
     "until": [16, "nến"], "title": "NHỮNG BÀI TỚI · NỐI CÁC CÂY NẾN", "range": "XU HƯỚNG, RỒI ĐƯỜNG TRUNG BÌNH ĐỘNG (MA)",
     "ind": [{"k": "sma", "n": 20, "label": "MA20", "at": [16, "trung"]}], "source": SRC_VNI},
    {"type": "question", "at": 17, "text": "Mẫu nến nào bạn từng nghe\nlà chắc ăn nhất?"},
]}

for c in CH.values():
    fx_rise(c["scenes"])

# Nhạc nền: chọn TAY (ghi sẵn vào bgm_picks.json, variety.resolve_bgm dùng cache) — 21 bài CK đều đã dùng 1 lần trong 3 video
# gần nhất (C1, D1, C2), picker theo hash dễ trùng ≥ 4 bài với một video (Jaccard > 35%). Bộ này: 3 bài của C1, 2 của D1, 2 của C2
# (≤ 27%); bài ch05 dài 12 phút (chương ~4 phút). Gain: chuẩn hoá volumedetect 90 s về mức C2 (mean + 20·log10(gain) ≈ −38,5 dB).
BGM = {"ch00.0": "investigations.mp3", "ch01.0": "sidewalk_shade.mp3", "ch02.0": "frost_waltz.mp3", "ch03.0": "dreamer.mp3",
       "ch04.0": "lobby_time.mp3", "ch05.0": "perspectives.mp3", "ch06.0": "wholesome.mp3"}

TITLE = "Biểu Đồ Nến Cho Người Mới: Một Cây Nến Kể Gì Về Một Phiên, Và Điều Nó Không Nói Được"
DISCLAIMER = ("Nội dung giáo dục, không phải tư vấn đầu tư hay tư vấn tài chính cá nhân. Không khuyến nghị mua/bán bất kỳ "
              "tài sản nào, không phải tín hiệu giao dịch, không dự báo thị trường. Ví dụ dùng dữ liệu quá khứ; quá khứ không "
              "đảm bảo tương lai. Nội dung do kênh biên soạn từ nguồn công khai; giọng đọc tổng hợp.")
# Khối phương pháp: factcheck mục 2 (quyết định PM 09/10 — KHÔNG bảng tỉ lệ từng mẫu), câu mã tính thay link bằng lời mời hỏi.
METHOD = ("📐 CÁCH KÊNH ĐẾM (quá khứ, không phải tín hiệu): VN-Index 08/10/2018–06/10/2026, 1.995 phiên (HOSE qua vnstock/VCI). "
          "Với mỗi mẫu nến, kênh đếm tỉ lệ số lần chỉ số cao hơn sau 5 và 20 phiên, rồi so với mọi ngày cùng bối cảnh (mốc ~59%, "
          "không phải 50%). Tổng cộng 27 phép so. Không kết quả nào còn đứng vững sau khi tính tới việc thử nhiều mẫu cùng lúc, "
          "và chưa trừ phí, thuế. Mã tính toán: kênh lưu lại và gửi khi bạn hỏi trong bình luận.")
SPEC = {
    "title": TITLE, "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO",
    "acc": ["vn-index", "hose", "doji", "búa", "bấc", "mốc"],
    "say": SAY, "imgs": {}, "chapters": list(CH),
    "youtube": {
        "titles": [TITLE, "Đọc Biểu Đồ Nến Từ Số 0: Thân, Bóng, Xanh Đỏ Và Một Tuần VN-Index Thật"],
        "summary": "Một cây nến gói cả một phiên giao dịch vào bốn con số: mở cửa, cao nhất, thấp nhất, đóng cửa. Bài 3 khoá Chứng "
                   "khoán từ số 0 đọc những cây nến VN-Index thật: ngày 09/03/2026 mở cửa ở đúng đỉnh, tuần 09–13/03 năm câu chuyện, "
                   "ngày 24/03 nến đỏ mà chỉ số vẫn tăng, rồi gộp năm nến ngày thành một nến tuần. Sau đó kênh tự đếm tám năm dữ liệu "
                   "VN-Index để xem cây búa, doji, ba chàng lính trắng có báo trước được gì không, và các nghiên cứu nói gì. "
                   "Giải thích dễ hiểu, dữ liệu thật, không khuyến nghị.",
        "more": [DISCLAIMER, METHOD],
        "chapter_titles": {"ch00": "Mở đầu: một cây nến đỏ", "ch01": "Bốn con số làm nên một cây nến",
                           "ch02": "Thân và bóng: phiên ấy ai thắng", "ch03": "Xanh, đỏ, và cái bẫy màu",
                           "ch04": "Đọc một tuần, rồi gộp thành một cây", "ch05": "Điều cây nến không nói được",
                           "ch06": "Áp dụng cho bạn, và khi nào không đúng"},
        "sources": [
            "Dữ liệu kênh tự tính — VN-Index (HOSE) qua Vnstock, nguồn VCI: https://vnstocks.com/docs/vnstock-data/du-lieu-giao-dich",
            "Wikipedia — Candlestick chart (lịch sử; trích S. Nison, Beyond Candlesticks, Wiley 1994): https://en.wikipedia.org/wiki/Candlestick_chart",
            "B. Marshall (2005), luận án tiến sĩ, Massey University — Candlestick technical trading strategies: can they create value for investors?: https://mro.massey.ac.nz/items/edc6c1cf-63d9-4c94-a13d-92ffe1a53481/full",
            "Marshall, Young & Rose (2006), Journal of Banking & Finance 30(8): 2303–2323: https://doi.org/10.1016/j.jbankfin.2005.08.001",
            "Marshall, Young & Cahan (2008), Review of Quantitative Finance and Accounting 31(2): 191–207: https://doi.org/10.1007/s11156-007-0068-1",
            "Tharavanij, Siraprapasiri & Rajchamaha (2017), SAGE Open 7(4): https://doi.org/10.1177/2158244017736799",
            "Ngô Tùng Sơn & cs. (2018), IMMS '18 (ACM) — mẫu nến đảo chiều trên thị trường Việt Nam: https://doi.org/10.1145/3277139.3277161",
            "Caginalp & Laurent (1998), Applied Mathematical Finance 5(3–4): https://ideas.repec.org/a/taf/apmtfi/v5y1998i3-4p181-205.html",
            "Lu (2014), Pacific-Basin Finance Journal 26: 65–78: https://ideas.repec.org/a/eee/pacfin/v26y2014icp65-78.html",
            "Zhu, Atri & Yegen (2016), Pacific-Basin Finance Journal 37: 116–127: https://ideas.repec.org/a/eee/pacfin/v37y2016icp116-127.html",
            "Thời báo Tài chính 10/03/2026 — VN-Index phục hồi mạnh: https://thoibaotaichinhvietnam.vn/chung-khoan-ngay-103-vn-index-phuc-hoi-manh-nhung-rui-ro-van-hien-huu-193453.html",
            "VnExpress 10/03/2026 — VN-Index tăng gần 24 điểm: https://vnexpress.net/vn-index-tang-gan-24-diem-5048812.html",
            "Công Luận 10/03/2026: https://congluan.vn/chung-khoan-hom-nay-10-3-2026-hoi-phuc-manh-vn-index-tang-gan-24-diem-10332937.html",
            "Nhân Dân 13/03/2026 — VN-Index giảm tiếp hơn 13 điểm: https://nhandan.vn/ocop/chung-khoan-ngay-133-co-phieu-dau-khi-bi-ban-manh-vn-index-giam-tiep-hon-13-diem-post948183.html",
            "Thời báo Tài chính 24/03/2026 — VN-Index tăng điểm trở lại: https://thoibaotaichinhvietnam.vn/chung-khoan-ngay-243-hoi-phuc-tich-cuc-vn-index-tang-diem-tro-lai-173089.html",
            "Người Lao Động 24/03/2026: https://tuoitre.vn/nld/vn-index-phuc-hoi-gan-24-diem-co-phieu-ngan-hang-bat-dong-san-dan-song-196260324155859073.htm",
            "Vietnambiz 24/03/2026 — hồi phục hơn 30 điểm đầu phiên: https://vietnambiz.vn/vn-index-hoi-phuc-hon-30-diem-dau-phien-sac-xanh-lan-rong-20263249443760.htm",
            "Nhân Dân 09/03/2026 — VN-Index giảm kỷ lục: https://nhandan.vn/ocop/chung-khoan-ngay-93-hon-230-co-phieu-xanh-lo-vn-index-giam-ky-luc-post947238.html",
            "VNX — Quy chế niêm yết và giao dịch (QĐ 22/QĐ-HĐTV ngày 18/04/2025): https://luatvietnam.vn/chung-khoan/quyet-dinh-22-qd-hdtv-2025-ban-hanh-quy-che-niem-yet-va-giao-dich-chung-khoan-399805-d1.html",
        ],
        "hashtags": ["ChứngKhoán", "BiểuĐồNến", "ChứngKhoánTừSố0", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["biểu đồ nến", "biểu đồ nến cho người mới", "cách đọc biểu đồ nến", "nến nhật", "chứng khoán từ số 0",
                 "chứng khoán cho người mới", "nến doji", "nến búa", "ba chàng lính trắng", "nến tuần nến ngày",
                 "khung thời gian", "VN-Index", "màu nến và bảng giá", "phân tích kỹ thuật", "tài chính cá nhân"],
        "category": "27",
        "data_credit": "📊 DỮ LIỆU BIỂU ĐỒ: VN-Index (HOSE), truy xuất qua Vnstock (nguồn VCI); nến tuần, tỉ lệ và phép đếm mẫu nến "
                       "do kênh tự tính; mốc báo chí theo Thời báo Tài chính, VnExpress, Công Luận, Nhân Dân, Người Lao Động, "
                       "Vietnambiz. Ví dụ nhiệt độ là giả định.",
        "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels"],
    },
}

if __name__ == "__main__":
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    pk = ROOT / "output" / "long" / TOPIC / "bgm_picks.json"
    pk.parent.mkdir(parents=True, exist_ok=True)
    pk.write_text(json.dumps(BGM, indent=1), encoding="utf-8")
    print("spec + %d chương, %d cảnh" % (len(CH), sum(len(c["scenes"]) for c in CH.values())))
