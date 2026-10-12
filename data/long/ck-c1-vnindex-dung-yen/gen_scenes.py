"""Sinh spec.json + scenes/hud/bgm cho video dài CK C1 "Từ đầu năm VN-Index gần như đứng yên — sao tài khoản vẫn có thể lỗ?"
(Chứng khoán từ số 0 · Bài 1; kênh Biểu Đồ Biết Nói, theme "chart").

    python data/long/ck-c1-vnindex-dung-yen/gen_scenes.py     # giữ nguyên "lines" + "title" trong chNN.json (script_lines ghi)

Dữ kiện + nguồn: docs/channels/chung-khoan/2026-10-07-long-c1-research.md; kiểm chứng: factcheck.md (cùng thư mục).
Số tự tính: data/ck/breadth_2026/ (motion/long/breadth.py) + data/ck/vnindex_1d.csv; cảnh breadth/basket do
motion/long/chartdata.py (attach_breadth, attach_basket) nhúng dữ liệu. Mốc chốt 31/12/2025 → 30/09/2026 (giá đóng cửa).
Luật kênh: chỉ giáo dục, không khuyến nghị, không dự báo; chỉ ghi tên mã VIC (treemap labels ["VIC"]), không nêu tên công
ty chứng khoán; MCH không đọc/hiện tên. Clip: Pexels (ngang), mọi b-roll ghi "VIDEO MINH HỌA".
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

UP, DN, GOLD, BLUE = "#4ade80", "#f87171", "#fbbf24", "#38bdf8"
VG = ["VIC", "VHM", "VRE", "VPL"]          # nhóm Vingroup (chỉ VIC được ghi tên trên ô)
ILL = "VIDEO MINH HỌA"

# Bảng đọc giữ nguyên bản đã dùng khi chạy TTS (đổi bảng = đổi khoá cache TTS).
SAY = {"vn-index": "Vi En In-đéc", "hose": "hô-dê", "vic": "vi ai xi", "vhm": "vi hát em", "vre": "vi rờ e", "vpl": "vi pê en",
       "ree": "rê ê ê", "sam": "xam", "gdp": "gi đi pi", "etf": "i ti ép", "hnx": "hát en ích", "upcom": "úp-com",
       "margin": "ma-gin", "app": "áp", "vingroup": "Vin-grúp", "vietnambiz": "Việt Nam Biz", "sjc": "ét giây xi"}

CH = {}

# ---------------- CH00 · Mở ứng dụng ngày 30/09 (cold open → 3 câu hỏi → nhận diện kênh) ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "CHỈ SỐ ĐỨNG YÊN, TÀI KHOẢN ĐỎ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "broll", "vid": "39494572", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "TỐI THỨ TƯ · 30/09/2026", "at": [0, "tối"]},
             {"text": "giáo dục, không phải khuyến nghị · ví dụ giả định", "at": [0, "Giả"], "sm": True}]},
    {"type": "kinetic", "at": 1, "items": [{"text": "VN-INDEX · TỪ ĐẦU NĂM", "at": [1, "Bạn"], "sm": True},
                                          {"text": "−0,9%", "at": [1, "âm"], "acc": True},
                                          {"text": "GẦN NHƯ ĐỨNG YÊN", "at": [2, "Gần"]}]},
    {"type": "broll", "at": 3, "vid": "6689151", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "TÀI KHOẢN CỦA BẠN", "at": [3, "Rồi"], "acc": True}]},
    {"type": "ledger", "at": 4, "title": "VÍ DỤ GIẢ ĐỊNH · 3 MÃ BẰNG TIỀN", "rows": [
        {"k": "MÃ A", "v": "−12%", "at": [5, "Một"]},
        {"k": "MÃ B", "v": "−20%", "at": [5, "Một", 1]},
        {"k": "MÃ C", "v": "+3%", "at": [5, "Một", 2]}],
     "total": {"k": "CẢ TÀI KHOẢN", "v": "≈ −10%", "at": [6, "Cả"]}},
    {"type": "question", "at": 7, "text": "Chỉ số gần như không giảm,\nsao mình lỗ gần 10%?\nApp sai, hay mình sai?"},
    {"type": "slam", "at": 8, "text": "KHÔNG AI SAI CẢ", "sub": "VN-INDEX ĐO MỘT CHUYỆN KHÁC VỚI TÀI KHOẢN CỦA BẠN"},
    {"type": "breadth", "at": 10, "date": "2026-09-30", "title": "400 CỔ PHIẾU HOSE · MỖI Ô MỘT MÃ",
     "range": "30/09/2026 · SO VỚI 31/12/2025", "drawAt": [10, "theo"], "chipAt": [10, "gần"], "chip": "≈ 3/4 DƯỚI GIÁ CUỐI 2025"},
    {"type": "ledger", "at": 11, "title": "BA CÂU HỎI", "rows": [
        {"k": "01", "v": "CỔ PHIẾU, HOSE, VN-INDEX LÀ GÌ?", "at": [12, "Một,"]},
        {"k": "02", "v": "CHỈ SỐ ĐỨNG YÊN, SAO MÃ LẠI GIẢM?", "at": [13, "Hai,"]},
        {"k": "03", "v": "VÌ SAO TÀI KHOẢN CÓ THỂ LỖ?", "at": [14, "Ba,"]}]},
    {"type": "brand", "at": 15, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 16, "items": [{"text": "BÀI 1 · CHỨNG KHOÁN TỪ SỐ 0", "at": [16, "bài"], "acc": True},
                                           {"text": "chỉ nhằm giáo dục · không phải lời khuyên mua bán",
                                            "at": [17, "Video"], "sm": True}]},
]}

# ---------------- CH01 · Cổ phiếu là gì, HOSE là gì ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CỔ PHIẾU LÀ GÌ, HOSE LÀ GÌ"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CỔ PHIẾU LÀ GÌ,\nHOSE LÀ GÌ", "sub": "CHỨNG KHOÁN TỪ SỐ 0 · BÀI 1",
     "vid": "35782362", "titleAt": [0, "Trước"]},
    {"type": "broll", "at": 1, "vid": "34770825", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "GÓP VỐN MỞ QUÁN PHỞ", "at": [1, "góp"]}, {"text": "5 NGƯỜI · MỖI NGƯỜI 1/5", "at": [1, "mỗi"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "QUÁN PHỞ 5 NGƯỜI GÓP", "rows": [
        {"k": "LÃI CUỐI NĂM CHIA NHAU", "v": "CỔ TỨC", "at": [2, "chia"]},
        {"k": "BÁN LẠI PHẦN GÓP", "v": "CHÊNH LỆCH GIÁ", "at": [3, "bán"]},
        {"k": "GIÁ BÁN LẠI", "v": "CAO HƠN, HOẶC THẤP HƠN", "at": [3, "cao"]}]},
    {"type": "broll", "at": 4, "vid": "36082305", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "CỔ PHIẾU CŨNG VẬY", "at": [4, "Cổ"]},
             {"text": "HÀNG TRIỆU, CÓ KHI HÀNG TỶ PHẦN", "at": [4, "triệu,"], "acc": True}]},
    {"type": "quote", "at": 5, "qline": 6, "typeDur": 5.6, "lbl": "NGUYÊN VĂN",
     "text": "Cổ phiếu là loại chứng khoán xác nhận quyền và lợi ích hợp pháp của người sở hữu đối với một phần vốn cổ phần của tổ chức phát hành.",
     "by": "Luật Chứng khoán 2019 (54/2019/QH14), Điều 4 khoản 2"},
    {"type": "kinetic", "at": 7, "items": [{"text": "MUA MỘT PHẦN NHỎ CỦA DOANH NGHIỆP", "at": [7, "mua"], "acc": True},
                                          {"text": "không phải mua một cái mã", "at": [7, "không"], "sm": True}]},
    {"type": "question", "at": 8, "text": "Mua cổ phiếu là\nlàm chủ công ty luôn à?"},
    {"type": "kinetic", "at": 9, "items": [{"text": "ĐỒNG SỞ HỮU", "at": [9, "Bạn"]},
                                          {"text": "PHẦN RẤT NHỎ", "at": [9, "rất"]},
                                          {"text": "CỔ TỨC, CHÊNH LỆCH GIÁ: KHÔNG BẢO ĐẢM", "at": [9, "bảo"], "acc": True}]},
    {"type": "ledger", "at": 10, "title": "UỶ BAN CHỨNG KHOÁN MỸ (SEC)", "rows": [
        {"k": "3 NHÓM", "v": "CỔ PHIẾU · TRÁI PHIẾU · TIỀN MẶT", "at": [10, "ba"]},
        {"k": "RỦI RO (LỊCH SỬ)", "v": "CAO NHẤT: CỔ PHIẾU", "at": [10, "rủi"]},
        {"k": "LỢI NHUẬN (LỊCH SỬ)", "v": "CAO NHẤT: CỔ PHIẾU", "at": [10, "lợi"]}]},
    {"type": "broll", "at": 11, "vid": "35782362", "ms": 6, "veil": 0.55, "illus": ILL,
     "kin": [{"text": "NGƯỜI MUA ⇄ NGƯỜI BÁN", "at": [11, "Người"]},
             {"text": "HOSE · SỞ GIAO DỊCH CHỨNG KHOÁN TP.HCM", "at": [12, "Lớn"], "acc": True}]},
    {"type": "broll", "at": 13, "vid": "35878664", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "MỘT KHU CHỢ CÓ BAN QUẢN LÝ", "at": [13, "Hãy"]},
             {"text": "CÔNG TY CHỨNG KHOÁN \"ĐI CHỢ HỘ\" · CÓ PHÍ", "at": [14, "Bạn"], "acc": True}]},
    {"type": "date", "at": 15, "day": "PHIÊN GIAO DỊCH ĐẦU TIÊN Ở HOSE", "date": "28.07.2000",
     "sub": {"text": "CHỈ 2 CỔ PHIẾU: REE · SAM", "at": [15, "chỉ"]}},
    {"type": "counter", "at": 16, "from": 2, "to": 405, "suffix": " CỔ PHIẾU", "countAt": [16, "Cuối"], "until": [16, "cổ"],
     "label": "HOSE · CUỐI THÁNG 9/2026", "sub": {"text": "TỔNG VỐN HOÁ ≈ 2/3 GDP 2025", "at": [16, "vốn"]}},
    {"type": "kinetic", "at": 17, "items": [{"text": "CHỢ MỞ CỬA THẾ NÀO? LỆNH KHỚP RA SAO?", "at": [17, "Chợ"]},
                                           {"text": "→ BÀI 2", "at": [17, "bài"], "acc": True}]},
]}

# ---------------- CH02 · VN-Index: giá của một chiếc giỏ có trọng số ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "VN-INDEX: CHIẾC GIỎ CÓ TRỌNG SỐ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "VN-INDEX:\nGIÁ CỦA MỘT CHIẾC GIỎ", "sub": "CHỈ SỐ CÓ TRỌNG SỐ",
     "vid": "7681176", "ms": 20, "titleAt": [0, "Giờ"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "VN-INDEX", "at": [1, "VN-Index"], "acc": True},
                                          {"text": "ĐO TOÀN BỘ CỔ PHIẾU NIÊM YẾT TRÊN HOSE", "at": [1, "toàn"]},
                                          {"text": "GỐC: 100 ĐIỂM · 28/07/2000", "at": [1, "bắt"], "sm": True}]},
    {"type": "ledger", "at": 2, "title": "CÁCH TÍNH · MÔ TẢ PHỔ THÔNG", "rows": [
        {"k": "VỐN HOÁ", "v": "GIÁ × SỐ CỔ PHIẾU", "at": [2, "Cách"]},
        {"k": "MỖI NGÀY", "v": "TỔNG VỐN HOÁ ÷ MỨC GỐC", "at": [3, "Mỗi"]},
        {"k": "GỐC 28/07/2000", "v": "100 ĐIỂM", "at": [3, "gốc."]}]},
    {"type": "question", "at": 4, "text": "VN-Index là giá trung bình\ncủa các cổ phiếu?"},
    {"type": "slam", "at": 5, "text": "KHÔNG", "sub": "CHỖ NGƯỜI MỚI HAY NHẦM NHẤT"},
    {"type": "kinetic", "at": 6, "items": [{"text": "KHÔNG PHẢI MỖI MÃ MỘT PHIẾU BẦU", "at": [6, "không"]},
                                          {"text": "DOANH NGHIỆP CÀNG LỚN → KÉO CHỈ SỐ CÀNG MẠNH", "at": [7, "Doanh"], "acc": True}]},
    {"type": "bars", "at": 8, "title": "GIỎ HÀNG 100 NGHÌN ĐỒNG", "unit": "NGHÌN ĐỒNG", "items": [
        {"k": "GÀ · TUẦN NÀY", "v": 50, "lbl": "50", "at": [8, "gà"]},
        {"k": "10 BÓ RAU · TUẦN NÀY", "v": 50, "lbl": "50", "at": [8, "mười"]},
        {"k": "GÀ · TUẦN SAU", "v": 60, "lbl": "60 (+20%)", "at": [9, "sáu"], "acc": True},
        {"k": "10 BÓ RAU · TUẦN SAU", "v": 45, "lbl": "45 (−10%)", "at": [9, "giảm"]}]},
    {"type": "broll", "at": 10, "vid": "35878664", "ms": 30, "veil": 0.55, "illus": ILL,
     "kin": [{"text": "CẢ GIỎ: 100 → 105 NGHÌN (+5%)", "at": [10, "Cả"]},
             {"text": "10/11 MÓN GIẢM GIÁ — GIỎ VẪN TĂNG", "at": [11, "Mười"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "VN-INDEX CŨNG LÀ MỘT CHIẾC GIỎ", "at": [12, "VN-Index"]},
                                           {"text": "CHỈ LÀ \"CON GÀ\" TO HƠN NHIỀU", "at": [12, "gà"], "acc": True}]},
    {"type": "basket", "at": 13, "date": "2026-09-30", "groupSmall": 200, "labels": ["VIC"],
     "title": "VỐN HOÁ HOSE · MỖI Ô MỘT CỔ PHIẾU", "range": "30/09/2026 · DIỆN TÍCH Ô = VỐN HOÁ", "drawAt": [13, "Theo"],
     "captions": [{"k": "VIC", "v": "≈ 21%", "at": [13, "VIC"], "mark": ["VIC"]},
                  {"k": "10 MÃ LỚN NHẤT", "v": "≈ 52%", "at": [14, "Mười"], "mark": "top10", "tone": "blue"},
                  {"k": "200 MÃ NHỎ NHẤT", "v": "≈ 1,3%", "at": [15, "hai"], "mark": "group", "tone": "down"}]},
    {"type": "bars", "at": 16, "title": "MÃ LỚN NHẤT ≈ 17 LẦN CẢ 200 MÃ NHỎ NHẤT", "unit": "% VỐN HOÁ HOSE · KÊNH TỰ TÍNH", "items": [
        {"k": "200 MÃ NHỎ NHẤT · 30/09", "v": 1.28, "lbl": "≈ 1,3%", "at": [16, "Mã"]},
        {"k": "VIC · 31/12/2025", "v": 16.16, "lbl": "≈ 16%", "at": [17, "đầu"]},
        {"k": "VIC · 30/09/2026", "v": 21.46, "lbl": "≈ 21%", "at": [16, "mười"], "acc": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "NHIỆT KẾ ĐẶT CẠNH CÁI LÒ LỚN NHẤT NHÀ", "at": [18, "nhiệt"]},
                                           {"text": "BÁO ẤM ≠ CẢ NHÀ ĐỀU ẤM", "at": [19, "chưa"], "acc": True}]},
]}

# ---------------- CH03 · Chín tháng 2026: chỉ số đứng yên, 3/4 cổ phiếu đi xuống ----------------
DIST = [("<−50%", 13), ("−50…−30", 73), ("−30…−20", 46), ("−20…−10", 80), ("−10…0", 79),
        ("0…+10", 56), ("+10…+20", 21), ("+20…+30", 13), ("+30…+50", 12), ("≥+50%", 7)]   # [a, b), mốc 30/09 (factcheck mục 4)


def _dist_items():
    out = []
    for k, (lbl, v) in enumerate(DIST):
        if k < 3:      # giảm ≥ 20%: 132 mã
            at, acc = [10, "giảm", 0, round(0.12 * k, 2)], True
        elif k >= 7:   # tăng ≥ 20%: 32 mã
            at, acc = [10, "tăng", 0, round(0.12 * (k - 7), 2)], True
        else:
            at, acc = [10, "Một", 0, round(0.1 * (k - 3), 2)], False
        out.append({"k": lbl, "v": v, "lbl": str(v), "at": at, **({"acc": True} if acc else {})})
    return out


CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "9 THÁNG 2026: 3/4 CỔ PHIẾU ĐI XUỐNG"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CHÍN THÁNG 2026:\nCHỈ SỐ ĐỨNG YÊN", "sub": "BA PHẦN TƯ CỔ PHIẾU ĐI XUỐNG",
     "vid": "39494572", "ms": 7, "titleAt": [0, "Bây"]},
    {"type": "candles", "at": 1, "series": "vnindex", "from": "2025-12-01", "to": "2026-09-30", "drawAt": [1, "Ngày"],
     "until": [2, "nó"], "title": "VN-INDEX · KHUNG NGÀY", "range": "12/2025 – 09/2026", "ind": [],
     "marks": [{"date": "2025-12-31", "text": "31/12: 1.784,49 (đóng cửa)", "pos": "below", "tone": "gold", "at": [1, "VN-Index"], "dx": 260, "dy": 40},
               {"date": "2026-09-30", "text": "30/09: 1.768,62 (đóng cửa)", "pos": "below", "tone": "down", "at": [2, "đóng"], "dx": -300, "dy": 40}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "−0,9% · ≈ −16 ĐIỂM", "at": [3, "Giảm"], "acc": True},
                                          {"text": "31/12/2025 → 30/09/2026 · giá đóng cửa", "at": [3, "mười"], "sm": True},
                                          {"text": "CÒN TỪNG CỔ PHIẾU?", "at": [4, "Còn"]}]},
    {"type": "breadth", "at": 5, "date": "2026-09-30", "title": "KÊNH ĐẾM TỪNG MÃ · 400 CỔ PHIẾU HOSE",
     "range": "30/09/2026 · SO VỚI 31/12/2025", "drawAt": [5, "Kênh"], "until": [5, "đếm"], "countAt": [6, "Hai"],
     "countSub": "THẤP HƠN CUỐI 2025", "chipAt": [7, "Gần"]},
    {"type": "breadth", "at": 8, "date": "2026-09-30", "title": "XẾP HÀNG: GIẢM NHIỀU NHẤT → TĂNG NHIỀU NHẤT",
     "range": "30/09/2026", "drawAt": [8, "Thử"], "until": [8, "tăng"], "medianAt": [9, "trung"]},
    {"type": "bars", "at": 10, "title": "400 MÃ HOSE THEO MỨC THAY ĐỔI · 31/12 → 30/09", "unit": "SỐ MÃ · KÊNH TỰ TÍNH",
     "items": _dist_items()},
    {"type": "ledger", "at": 11, "title": "HAI CHIẾC GIỎ · 31/12 → 30/09", "rows": [
        {"k": "RỔ CHIA ĐỀU 400 MÃ", "v": "≈ −10,6%", "at": [11, "Nếu"]},
        {"k": "VN-INDEX (THEO VỐN HOÁ)", "v": "−0,9%", "at": [12, "Khoảng"]}],
     "total": {"k": "CHÊNH LỆCH", "v": "GẦN 10 ĐIỂM %", "at": [12, "giá"]}},
    {"type": "question", "at": 13, "text": "Mấy con số này ở đâu ra?\nCác bạn tự đếm à?"},
    {"type": "kinetic", "at": 14, "items": [{"text": "KÊNH TỰ TÍNH", "at": [14, "Đúng"], "acc": True},
                                           {"text": "từ giá đóng cửa công khai · cách tính đầy đủ trong mô tả", "at": [14, "giá"], "sm": True}]},
    {"type": "ledger", "at": 15, "title": "HAI ĐIỂM NÊN BIẾT", "rows": [
        {"k": "MÃ RỜI SÀN TRONG NĂM", "v": "KHÔNG CÓ TRONG MẪU", "at": [15, "mã"]},
        {"k": "→ SỐ THẬT", "v": "CÓ THỂ TỆ HƠN", "at": [15, "tệ"]},
        {"k": "GIÁ ĐÃ ĐIỀU CHỈNH CỔ TỨC", "v": "HƠI ĐẸP HƠN", "at": [16, "Còn"]}]},
    {"type": "quote", "at": 17, "qline": 18, "lbl": "NGUYÊN VĂN", "text": "Xanh chỉ số, đỏ danh mục.",
     "by": "Báo Tuổi Trẻ, 16/04/2026"},
    {"type": "kinetic", "at": 19, "items": [{"text": "2025: VN-INDEX +40,9%", "at": [19, "Năm"]},
                                           {"text": "theo Tuổi Trẻ (14/01/2026)", "at": [19, "Tuổi"], "sm": True},
                                           {"text": "HƠN 46% CỔ PHIẾU TRÊN THỊ TRƯỜNG ĐẦU TƯ ÂM", "at": [19, "hơn"], "acc": True}]},
    {"type": "slam", "at": 20, "text": "CHỈ SỐ ≠ CỔ PHIẾU ĐIỂN HÌNH", "sub": "CHỈ SỐ ĐO MỘT CHIẾC GIỎ CÓ TRỌNG SỐ"},
]}

# ---------------- CH04 · Ai đang giữ điểm cho VN-Index? ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "AI ĐANG GIỮ ĐIỂM CHO VN-INDEX?"}, "bgm": {"mood": "epic", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "AI ĐANG GIỮ ĐIỂM\nCHO VN-INDEX?", "sub": "ĐÓNG GÓP ĐIỂM · 2026",
     "titleAt": [0, "Vậy"]},
    {"type": "basket", "at": 1, "date": "2026-09-30", "groupSmall": 200, "labels": ["VIC"], "tileInfo": "pct", "color": "pct",
     "title": "VỐN HOÁ HOSE · MÀU = % THAY ĐỔI", "range": "31/12/2025 → 30/09/2026", "drawAt": [1, "Con"], "colorAt": [2, "Từ"],
     "captions": [{"k": "VIC · 31/12/2025 → 30/09", "v": "+34,4%", "at": [2, "VIC"], "tone": "up", "mark": ["VIC"]},
                  {"k": "KÉO VN-INDEX (ƯỚC TÍNH)", "v": "≈ +100 ĐIỂM", "at": [3, "kéo"], "tone": "gold"},
                  {"k": "CẢ VN-INDEX", "v": "≈ −16 ĐIỂM", "at": [3, "cả"], "tone": "down"}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "NẾU VIC CHỈ ĐỨNG GIÁ", "at": [4, "nếu"]},
                                          {"text": "VN-INDEX 30/09: CÓ THỂ THẤP HƠN ≈ 100 ĐIỂM", "at": [4, "thấp"], "acc": True}]},
    {"type": "basket", "at": 5, "date": "2026-09-30", "groupSmall": 200, "labels": ["VIC"], "tileInfo": "pct", "color": "pct",
     "title": "NHÓM VINGROUP · 4 MÃ", "range": "31/12/2025 → 30/09/2026", "drawAt": [5, "Cả"],
     "highlight": VG, "hlAt": [5, "Vingroup"],
     "captions": [{"k": "NHÓM VINGROUP (4 MÃ)", "v": "≈ +105 ĐIỂM", "at": [5, "giữ"], "tone": "gold"},
                  {"k": "2 / 4 MÃ TRONG NHÓM", "v": "GIẢM", "at": [5, "hai"], "tone": "down", "mark": ["VRE", "VPL"]},
                  {"k": "PHẦN CÒN LẠI (≈ −6%)", "v": "≈ −80 ĐIỂM", "at": [6, "Phần"], "tone": "down"}]},
    {"type": "ledger", "at": 7, "title": "ĐÓNG GÓP ĐIỂM · ƯỚC TÍNH THÔ", "rows": [
        {"k": "VIC", "v": "≈ +100 ĐIỂM", "at": [7, "Đây"]},
        {"k": "NHÓM VINGROUP (4 MÃ)", "v": "≈ +105 ĐIỂM", "at": [7, "cộng"]},
        {"k": "PHẦN CÒN LẠI", "v": "≈ −80 ĐIỂM", "at": [7, "phần"]}],
     "total": {"k": "VN-INDEX THỰC TẾ", "v": "≈ −16 ĐIỂM", "at": [7, "mười"]}},
    {"type": "kinetic", "at": 8, "items": [{"text": "VIETNAMBIZ (DẪN CHUYÊN GIA) · NỬA ĐẦU 2026", "at": [8, "Một"], "sm": True},
                                          {"text": "VN-INDEX: +4,23%", "at": [8, "tăng"]},
                                          {"text": "BỎ NHÓM VINGROUP: ≈ −1,81%", "at": [8, "bỏ"], "acc": True}]},
    {"type": "question", "at": 9, "text": "Cứ mua mấy mã lớn nhất\nlà chắc ăn?"},
    {"type": "slam", "at": 10, "text": "KÊNH KHÔNG TRẢ LỜI\n\"NÊN MUA MÃ NÀO\"", "sub": "NHƯNG DỮ LIỆU CHO THẤY HAI ĐIỀU"},
    {"type": "kinetic", "at": 11, "items": [{"text": "01 · TRONG 10 MÃ LỚN NHẤT: CÓ MÃ ≈ −22%", "at": [11, "Một,"]},
                                           {"text": "CHÍNH NÓ KÉO CHỈ SỐ XUỐNG NHIỀU NHẤT", "at": [11, "kéo"], "acc": True},
                                           {"text": "02 · ĐÂY LÀ NHÌN LẠI", "at": [12, "Hai,"]}]},
    {"type": "slam", "at": [12, "Không"], "text": "KHÔNG AI BIẾT TRƯỚC", "sub": "NĂM NÀO, MÃ NÀO SẼ LÀ \"CON GÀ\" TĂNG GIÁ"},
    {"type": "date", "at": 13, "day": "KHOẢNH KHẮC ĐÁNG NHỚ NHẤT", "date": "18.05.2026"},
    {"type": "candles", "at": 14, "series": "vnindex", "from": "2025-12-01", "to": "2026-09-30", "drawAt": [14, "Ngày"],
     "until": [14, "cao"], "title": "VN-INDEX · KHUNG NGÀY", "range": "12/2025 – 09/2026", "ind": [],
     "marks": [{"date": "2026-05-18", "text": "Đóng cửa 1.927,94 · +8,0%", "pos": "above", "tone": "up", "at": [14, "gần"], "dx": 260, "dy": -10}]},
    {"type": "breadth", "at": 15, "date": "2026-05-18", "title": "CAO NHẤT TỪ ĐẦU NĂM TỚI 30/09 · 400 MÃ HOSE",
     "range": "31/12/2025 → 18/05/2026", "drawAt": [15, "Nhìn"], "until": [15, "đó"], "countAt": [15, "đó"],
     "countSub": "DƯỚI GIÁ ĐẦU NĂM", "chipAt": [15, "chỉ"],
     "animate": {"from": "2026-01-05", "to": "2026-05-18", "every": 3, "at": [15, "ngày"], "until": [16, "cùng"]}},
    {"type": "kinetic", "at": 17, "items": [{"text": "TỪ ĐÁY 23/03 → 30/09/2026", "at": [17, "Từ"], "sm": True},
                                           {"text": "TỈ LỆ MÃ DƯỚI GIÁ ĐẦU NĂM", "at": [17, "tỉ"]},
                                           {"text": "CHƯA LÚC NÀO < 58%", "at": [17, "chưa"], "acc": True}]},
]}

# ---------------- CH05 · Tài khoản của bạn không phải là VN-Index (5 cơ chế) ----------------
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "TÀI KHOẢN ≠ VN-INDEX"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "TÀI KHOẢN CỦA BẠN\nKHÔNG PHẢI LÀ VN-INDEX",
     "sub": "CHỌN MÃ · THỜI ĐIỂM · PHÍ & THUẾ · MARGIN · CẢM XÚC", "vid": "7681176", "titleAt": [0, "Giờ"]},
    {"type": "broll", "at": 1, "vid": "7681176", "ms": 8, "veil": 0.55, "illus": ILL,
     "kin": [{"text": "01 · CHỌN MÃ", "at": [1, "Thứ"]},
             {"text": "BẠN SỞ HỮU VÀI MÃ, KHÔNG SỞ HỮU CHỈ SỐ", "at": [1, "bạn"], "acc": True},
             {"text": "nhóm giảm đông hơn hẳn → vài mã dễ rơi vào nhóm giảm", "at": [2, "Năm"], "sm": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "NỬA ĐẦU 2026", "at": [3, "Ngay"], "sm": True},
                                          {"text": "28 QUỸ MỞ CỔ PHIẾU (TB): −1,12%", "at": [3, "quỹ"], "acc": True},
                                          {"text": "VN-INDEX: +4,23%", "at": [3, "VN-Index"]}]},
    {"type": "candles", "at": 4, "series": "vnindex", "from": "2025-12-01", "to": "2026-09-30", "drawAt": [4, "Thứ"],
     "until": [5, "Giả"], "title": "02 · THỜI ĐIỂM BỎ TIỀN VÀO", "range": "VN-INDEX · 12/2025 – 09/2026", "ind": [],
     "source": "VÍ DỤ GIẢ ĐỊNH, LỜI LỖ THEO ĐÚNG VN-INDEX · MINH HOẠ, KHÔNG PHẢI CANH ĐÁY",
     "marks": [{"date": "2025-12-31", "text": "+10 triệu", "pos": "below", "tone": "gold", "at": [5, "mười"], "dx": 200, "dy": 40},
               {"date": "2026-05-18", "text": "+50 triệu", "pos": "above", "tone": "gold", "at": [6, "thêm"], "dx": 220, "dy": -10}]},
    {"type": "ledger", "at": 7, "title": "VÍ DỤ GIẢ ĐỊNH · 30/09", "rows": [
        {"k": "BỎ VÀO (31/12 + 18/05)", "v": "60 TRIỆU", "at": [7, "Đến"]},
        {"k": "CÒN LẠI 30/09", "v": "≈ 55,8 TRIỆU", "at": [7, "năm"]},
        {"k": "VN-INDEX CÙNG KỲ", "v": "−0,9%", "at": [7, "dù"]}],
     "total": {"k": "TÀI KHOẢN", "v": "≈ −7,0%", "at": [7, "âm"]}},
    {"type": "broll", "at": 8, "vid": "36133125", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "LÊN XE Ở ĐỈNH ĐỒI", "at": [8, "lên"]},
             {"text": "CHỈ ĐI ĐÚNG QUÃNG XUỐNG DỐC", "at": [8, "xuống"], "acc": True}]},
    {"type": "bars", "at": 9, "title": "60 TRIỆU BỎ VÀO · GIÁ TRỊ NGÀY 30/09", "unit": "TRIỆU ĐỒNG", "items": [
        {"k": "VỐN BỎ VÀO", "v": 60, "lbl": "60 TR", "at": [9, "Ai"]},
        {"k": "THÊM TIỀN 18/05 (ĐỈNH)", "v": 55.78, "lbl": "≈ 55,8 TR", "at": [9, "Ai", 0, 0.35]},
        {"k": "THÊM TIỀN 23/03 (ĐÁY)", "v": 65.49, "lbl": "≈ 65,5 TR (≈ +9%)", "at": [9, "đáy"], "acc": True}]},
    {"type": "slam", "at": 10, "text": "ĐỂ HIỂU CƠ CHẾ,\nKHÔNG PHẢI ĐỂ CANH ĐÁY", "sub": "KHÔNG AI BIẾT TRƯỚC ĐÂU LÀ ĐỈNH, ĐÂU LÀ ĐÁY"},
    {"type": "ledger", "at": 11, "title": "03 · PHÍ VÀ THUẾ", "rows": [
        {"k": "THUẾ MỖI LẦN BÁN", "v": "0,1% GIÁ BÁN", "at": [12, "Mỗi"]},
        {"k": "→ KỂ CẢ KHI", "v": "BÁN LỖ", "at": [12, "kể"]},
        {"k": "PHÍ MÔI GIỚI / CHIỀU", "v": "≈ 0,15–0,35%", "at": [13, "Mỗi"]},
        {"k": "→ CÓ NƠI", "v": "THẤP HƠN", "at": [13, "có"]}]},
    {"type": "question", "at": 14, "text": "Phí chỉ không phẩy mấy phần trăm,\nsao ăn mòn được nhiều?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "CỘNG DỒN THEO SỐ LẦN GIAO DỊCH", "at": [15, "Vì"]},
                                           {"text": "0,15% MUA + 0,15% BÁN + 0,1% THUẾ", "at": [16, "Lấy"]},
                                           {"text": "≈ 0,4% MỖI VÒNG", "at": [16, "bốn"], "acc": True}]},
    {"type": "counter", "at": 17, "from": 0, "to": 4800000, "suffix": " đ", "countAt": [17, "Tài"], "until": [17, "bốn"],
     "label": "PHÍ + THUẾ 1 NĂM · 50 TRIỆU, XOAY VỐN 2 LẦN/THÁNG",
     "sub": {"text": "≈ 9,6% VỐN · HƠN NỬA THÁNG LƯƠNG 9 TRIỆU", "at": [18, "Gần"]}},
    {"type": "kinetic", "at": 19, "items": [{"text": "04 · VAY KÝ QUỸ (MARGIN)", "at": [19, "Thứ"]},
                                           {"text": "KÍNH LÚP: PHÓNG TO CẢ LÃI LẪN LỖ", "at": [20, "kính"], "acc": True},
                                           {"text": "và kính lúp này phải trả tiền thuê", "at": [20, "thuê."], "sm": True}]},
    {"type": "ledger", "at": 21, "title": "VÍ DỤ MARGIN (GIẢ ĐỊNH)", "rows": [
        {"k": "VỐN CỦA BẠN", "v": "50 TRIỆU", "at": [21, "Giả"]},
        {"k": "VAY THÊM", "v": "50 TRIỆU", "at": [21, "vay"]},
        {"k": "LÃI VAY", "v": "13,5%/NĂM", "at": [21, "lãi"]},
        {"k": "6 THÁNG SAU", "v": "CỔ PHIẾU −10%", "at": [22, "Sáu"]}]},
    {"type": "bars", "at": 23, "title": "VỐN CÒN LẠI SAU 6 THÁNG · CỔ PHIẾU −10%", "unit": "TRIỆU ĐỒNG · ĐÃ TRỪ LÃI VAY", "items": [
        {"k": "VỐN BAN ĐẦU", "v": 50, "lbl": "50 TR", "at": [23, "Không"]},
        {"k": "KHÔNG VAY", "v": 45, "lbl": "45 TR (−10%)", "at": [23, "mất"]},
        {"k": "VAY 1:1", "v": 36.63, "lbl": "≈ 36,6 TR (≈ −27%)", "at": [23, "Có"], "acc": True}]},
    {"type": "kinetic", "at": 24, "items": [{"text": "LÃI 13,5%/NĂM CHẠY KỂ CẢ KHI GIÁ ĐỨNG YÊN", "at": [24, "Kể"]},
                                           {"text": "→ −6,75% VỐN SAU 6 THÁNG", "at": [24, "gần"], "acc": True},
                                           {"text": "giảm sâu hơn: có thể bị bán bớt để thu nợ, đúng lúc giá thấp", "at": [25, "Giảm"], "sm": True}]},
    {"type": "broll", "at": 26, "vid": "39494572", "ms": 12, "veil": 0.55, "illus": ILL,
     "kin": [{"text": "05 · CẢM XÚC", "at": [26, "Thứ"]},
             {"text": "MUA ĐUỔI KHI LÊN ĐỈNH · BÁN THÁO KHI RƠI", "at": [27, "Mua"], "acc": True},
             {"text": "mỗi lần: thêm phí, thuế và rủi ro thời điểm", "at": [27, "mỗi"], "sm": True}]},
    {"type": "kinetic", "at": 28, "items": [{"text": "VIỆT NAM: KÊNH CHƯA TÌM THẤY SỐ LIỆU CÔNG KHAI", "at": [28, "Ở"]},
                                           {"text": "VỀ TỶ LỆ NHÀ ĐẦU TƯ LÃI / LỖ", "at": [28, "tỷ"], "acc": True},
                                           {"text": "nên không đưa ra con số nào", "at": [28, "không", 1], "sm": True}]},
]}

# ---------------- CH06 · Áp dụng cho bạn, và khi nào không đúng ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "ÁP DỤNG CHO BẠN"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "ÁP DỤNG CHO BẠN —\nVÀ KHI NÀO KHÔNG ĐÚNG",
     "sub": "KHÔNG PHẢI LỜI KHUYÊN MUA, BÁN HAY GIỮ", "titleAt": [0, "Mình"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "5 CÂU HỎI", "at": [1, "Chỉ"], "acc": True},
                                          {"text": "để bạn tự soi tài khoản của mình", "at": [1, "tự"], "sm": True}]},
    {"type": "ledger", "at": 2, "title": "5 CÂU TỰ KIỂM", "rows": [
        {"k": "01", "v": "MẤY MÃ? MỖI MÃ CHIẾM BAO NHIÊU?", "at": [2, "Một:"]},
        {"k": "02", "v": "SO VỚI VN-INDEX HAY TIỀN ĐÃ NẠP?", "at": [3, "Hai:"]},
        {"k": "03", "v": "BAO NHIÊU LƯỢT? BAO NHIÊU PHÍ, THUẾ?", "at": [4, "Ba:"]},
        {"k": "04", "v": "CÓ MARGIN? GIẢM 20% CÒN BAO NHIÊU?", "at": [5, "Bốn:"]},
        {"k": "05", "v": "VÌ HIỂU DOANH NGHIỆP, HAY VÌ CHỈ SỐ?", "at": [6, "Năm:"]}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN?", "at": [7, "những"]},
                                          {"text": "CÓ MÃ LỚN ĐÃ TĂNG MẠNH → CÓ THỂ TỐT HƠN CHỈ SỐ", "at": [8, "Nếu"]},
                                          {"text": "ĐỘ LỆCH CỦA GIỎ CẮT CẢ HAI CHIỀU", "at": [8, "Độ"], "acc": True}]},
    {"type": "broll", "at": 9, "vid": "7578628", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "QUỸ ETF MÔ PHỎNG CHỈ SỐ", "at": [9, "Nếu"]},
             {"text": "BÁM CHỈ SỐ MÀ QUỸ THEO, TRỪ PHÍ", "at": [9, "bám"], "acc": True},
             {"text": "nhiều quỹ không theo VN-Index", "at": [9, "nhiều"], "sm": True}]},
    {"type": "ledger", "at": 10, "title": "MỐC TÍNH ĐỔI KẾT QUẢ", "rows": [
        {"k": "ĐÁY 23/03 → 30/09: VN-INDEX", "v": "+11,15%", "at": [10, "VN-Index"]},
        {"k": "MÃ VẪN DƯỚI GIÁ 23/03", "v": "266/400 ≈ 2/3", "at": [10, "hai"]}],
     "total": {"k": "ĐẦU NĂM", "v": "CHỈ LÀ MỘT MỐC TRÊN LỊCH", "at": [10, "Đầu"]}},
    {"type": "kinetic", "at": 11, "items": [{"text": "CHỈ GỒM CỔ PHIẾU TRÊN HOSE", "at": [11, "Và"]},
                                           {"text": "chưa tính HNX và UPCoM", "at": [11, "chưa"], "sm": True}]},
    {"type": "slam", "at": 12, "text": "VN-INDEX KHÔNG NÓI SAI", "sub": "NÓ ĐO MỘT CHIẾC GIỎ CÓ TRỌNG SỐ"},
    {"type": "ledger", "at": 14, "title": "TÀI KHOẢN CỦA BẠN LÀ", "rows": [
        {"k": "01", "v": "VÀI MÃ BẠN CHỌN", "at": [14, "vài"]},
        {"k": "02", "v": "THỜI ĐIỂM BỎ TIỀN VÀO", "at": [14, "thời"]},
        {"k": "03", "v": "PHÍ & THUẾ MỖI LẦN MUA BÁN", "at": [14, "phí"]},
        {"k": "04", "v": "TIỀN VAY (NẾU CÓ)", "at": [14, "vay"]}]},
    {"type": "broll", "at": 15, "vid": "6689151", "ms": 2, "veil": 0.55, "illus": ILL,
     "kin": [{"text": "TÀI KHOẢN ĐỎ KHI CHỈ SỐ ĐỨNG YÊN", "at": [15, "Nếu"]},
             {"text": "≠ BẠN KÉM CỎI", "at": [15, "không"], "acc": True},
             {"text": "có khi chỉ là một thước đo không dành cho mình", "at": [16, "thước"], "sm": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "BÀI 2", "at": [17, "Bài"], "sm": True},
                                           {"text": "MỘT PHIÊN GIAO DỊCH Ở HOSE DIỄN RA THẾ NÀO?", "at": [17, "phiên"], "acc": True},
                                           {"text": "lệnh đi đâu · khớp giá ra sao · vì sao chưa bán ngay được", "at": [18, "Lệnh"], "sm": True}]},
    {"type": "question", "at": 19, "text": "Từ đầu năm, tài khoản của bạn đi\ncùng chiều hay ngược chiều VN-Index?\nVì chọn mã, thời điểm, hay phí?"},
]}

TITLE = "Từ Đầu Năm VN-Index Gần Như Đứng Yên — Sao Tài Khoản Vẫn Có Thể Lỗ? | Chứng Khoán Từ Số 0 · Bài 1"
DISCLAIMER = ("Nội dung giáo dục, không phải tư vấn đầu tư hay tư vấn tài chính cá nhân. Không khuyến nghị mua/bán bất kỳ "
              "tài sản nào. Ví dụ dùng dữ liệu quá khứ; quá khứ không đảm bảo tương lai. Nội dung do kênh biên soạn từ nguồn "
              "công khai; giọng đọc tổng hợp.")   # y nguyên A1
METHOD = ("📐 CÁCH TÍNH (kênh tự tính): 400 cổ phiếu HOSE có giá đóng cửa ở cả hai mốc 31/12/2025 và 30/09/2026 (giá lịch sử "
          "đã điều chỉnh theo cổ tức, truy xuất qua vnstock/VCI); không gồm 6 mã niêm yết mới trong năm; mã đã rời sàn trong năm "
          "không có trong mẫu. Kết quả: 291 mã thấp hơn giá cuối 2025 (72,8%), trung vị −11,35%, rổ chia đều −10,58%; VN-Index "
          "−0,89%. Vốn hoá = giá đóng cửa × số cổ phiếu niêm yết. Đóng góp điểm (ước tính thô): điểm VN-Index 31/12/2025 × tỉ "
          "trọng vốn hoá đầu năm × % thay đổi giá. VN-Index được mô tả ở mức phổ thông; phương pháp chi tiết theo quy tắc chỉ số "
          "của HOSE. Ví dụ tài khoản, phí và margin là giả định để minh hoạ cơ chế.")
SPEC = {
    "title": TITLE, "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20,
    "acc": ["vn-index", "hose", "vic", "giỏ", "tài", "khoản", "lỗ", "trung", "vị", "phí", "thuế", "margin", "vốn", "hoá"],
    "say": SAY, "imgs": {}, "chapters": list(CH),
    "youtube": {
        "titles": [TITLE, "VN-Index Gần Như Đứng Yên, Sao 3/4 Cổ Phiếu Lại Giảm? | Chứng Khoán Từ Số 0",
                   "VN-Index Là Gì — Và Vì Sao Tài Khoản Của Bạn Không Đi Theo Nó"],
        "summary": "Từ 31/12/2025 tới 30/09/2026, VN-Index gần như đứng yên (−0,9%) — nhưng cứ 4 cổ phiếu trên HOSE thì gần 3 "
                   "thấp hơn giá cuối năm ngoái. Bài 1 khoá Chứng khoán từ số 0: cổ phiếu, sàn HOSE và VN-Index là gì, chỉ số được "
                   "tính ra sao, vì sao vài mã rất lớn giữ điểm cho cả chỉ số, và vì sao tài khoản của bạn có thể lỗ dù chỉ số không "
                   "giảm. Dữ liệu thật, kênh tự tính, giải thích dễ hiểu.",
        "more": [DISCLAIMER, METHOD],
        "chapter_titles": {"ch00": "Mở đầu: chỉ số đứng yên, tài khoản đỏ", "ch01": "Cổ phiếu là gì, HOSE là gì",
                           "ch02": "VN-Index: giá của một chiếc giỏ có trọng số",
                           "ch03": "Chín tháng 2026: chỉ số đứng yên, ba phần tư cổ phiếu đi xuống",
                           "ch04": "Ai đang giữ điểm cho VN-Index?", "ch05": "Tài khoản của bạn không phải là VN-Index",
                           "ch06": "Áp dụng cho bạn — và khi nào không đúng"},
        "sources": [
            "Dữ liệu kênh tự tính — giá đóng cửa HOSE truy xuất qua Vnstock (nguồn VCI): https://vnstocks.com/docs/vnstock-data/du-lieu-giao-dich",
            "HOSE — Quy tắc quản lý bộ chỉ số HOSE-Index, phiên bản 4.0 (QĐ 747/QĐ-SGDHCM, bản dịch tiếng Anh): https://static2.vietstock.vn/vietstock/2024/12/30/20241230_25_12_hose_index_4_0_translation.pdf",
            "Luật Chứng khoán 2019 (54/2019/QH14), Điều 4: https://luatvietnam.vn/chung-khoan/luat-chung-khoan-2019-179050-d1.html",
            "VnExpress — Hậu trường phiên giao dịch đầu tiên với 2 cổ phiếu: https://vnexpress.net/hau-truong-phien-giao-dich-dau-tien-voi-2-co-phieu-4133477.html",
            "CafeF 05/10/2026 — Vốn hoá cổ phiếu trên HOSE tháng 9/2026: https://cafef.vn/von-hoa-co-phieu-tren-hose-boc-hoi-298000-ty-dong-trong-thang-9-188261005202836242.chn",
            "Tuổi Trẻ 16/04/2026 — \"Xanh chỉ số, đỏ danh mục\": https://tuoitre.vn/co-phieu-vingroup-tiep-tuc-keo-tru-vn-index-van-xanh-chi-so-do-danh-muc-20260416140700503.htm",
            "Tuổi Trẻ 14/01/2026 — Chứng khoán tăng gần 41% một năm, vì sao nhiều người vẫn thua lỗ: https://tuoitre.vn/chung-khoan-tang-gan-41-mot-nam-vi-sao-nhieu-nguoi-van-thua-lo-20260114171752752.htm",
            "Vietnambiz — Gửi tiết kiệm vượt nhiều kênh đầu tư nửa đầu năm 2026: https://vietnambiz.vn/gui-tiet-kiem-vuot-nhieu-kenh-dau-tu-nua-dau-nam-202671014143080.htm",
            "Báo Chính phủ — Thuế TNCN đối với chuyển nhượng chứng khoán (0,1%): https://baochinhphu.vn/thue-thu-nhap-ca-nhan-doi-voi-chuyen-nhuong-chung-khoan-10226032718480641.htm",
            "Tuổi Trẻ 18/03/2026 — Lãi suất margin lên đến 14%: https://tuoitre.vn/lai-suat-margin-len-den-14-cong-ty-chung-khoan-bat-dau-chuyen-ap-luc-sang-nha-dau-tu-20260318140649637.htm",
            "Phí giao dịch phổ biến (tổng hợp): https://www.vcbs.com.vn/chi-tiet-kien-thuc-co-ban/phi-giao-dich-chung-khoan",
            "SEC — Beginners' Guide to Asset Allocation, Diversification, and Rebalancing: https://www.sec.gov/about/reports-publications/investorpubsassetallocationhtm",
        ],
        "hashtags": ["ChứngKhoán", "VNIndex", "ChứngKhoánTừSố0", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["chứng khoán cho người mới", "chứng khoán từ số 0", "VN-Index là gì", "cổ phiếu là gì", "HOSE là gì",
                 "cách tính VN-Index", "VN-Index 2026", "chứng khoán 2026", "độ rộng thị trường", "xanh chỉ số đỏ danh mục",
                 "phí giao dịch chứng khoán", "margin là gì", "tài chính cá nhân"],
        "category": "27",
        "data_credit": "📊 DỮ LIỆU BIỂU ĐỒ: giá đóng cửa cổ phiếu và VN-Index trên HOSE, truy xuất qua Vnstock (nguồn VCI); số liệu tổng hợp do kênh tự tính.", "thumb": "t1.jpg",
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
    print("spec + %d chương, %d cảnh" % (len(CH), sum(len(c["scenes"]) for c in CH.values())))
