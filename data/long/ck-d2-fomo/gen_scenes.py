"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài CK D2 "FOMO: Vì Sao Lúc 'Ai Cũng Lãi' Lại Là Lúc Nguy Hiểm Nhất?".

    python data/long/ck-d2-fomo/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (bản 2, đã kiểm chứng) + factcheck.md. Số liệu: analysis.py -> results.json (kênh tự tính, VN-Index vnstock/VCI).
Luật kênh: chỉ giáo dục, không mã cổ phiếu / công ty chứng khoán / quỹ, không "nên mua/bán", không dự báo.
Cảnh dữ liệu ghi "KÊNH TỰ TÍNH · QUÁ KHỨ · KHÔNG PHẢI DỰ BÁO". beat2 bật (bố cục cảnh chữ xoay vòng, từ nhấn).
BƯỚC 1 (09/10): chỉ spec để thu giọng; scenes viết sau khi có timing.json.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C3 = json.loads((D.parent / "ck-c3-bieu-do-nen" / "spec.json").read_text(encoding="utf-8"))

SAY = {**C3["say"], "fomo": "phô-mô", "barber": "Ba-bơ", "terrance": "Te-rần", "odean": "Ô-đin", "vsd": "vi ét đê"}

R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444"
SELF = "KÊNH TỰ TÍNH · QUÁ KHỨ · KHÔNG PHẢI DỰ BÁO"
DATA = "DỮ LIỆU: HOSE (VNSTOCK/VCI), KÊNH TỰ TÍNH. MINH HOẠ QUÁ KHỨ, KHÔNG PHẢI KHUYẾN NGHỊ."
VSD = "VSD (TRUNG TÂM LƯU KÝ CHỨNG KHOÁN) · QUA BÁO CHÍ"
VM = "VIDEO MINH HỌA"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "THÁNG KỶ LỤC"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "day": "THÁNG KỶ LỤC", "date": "03.2022"},
    {"type": "counter", "at": 1, "from": 0, "to": 270217, "suffix": " TÀI KHOẢN", "label": "MỞ MỚI TRONG MỘT THÁNG", "sub": {"text": VSD, "at": 1}},
    {"type": "kinetic", "at": 2, "items": [{"text": "KỶ LỤC", "at": 2, "acc": True}, {"text": "cao nhất từ trước tới khi ấy", "at": [2, "cao"], "sm": True}]},
    {"type": "bars", "at": 3, "title": "TÀI KHOẢN MỚI (TRIỆU)",
     "items": [{"k": "2017 → 2020 CỘNG LẠI", "v": 1.04, "lbl": "1,04", "at": [4, "bốn"]}, {"k": "RIÊNG 2021", "v": 1.5, "lbl": "> 1,5", "at": [3, "triệu"], "acc": True}],
     "label": {"k": "NGUỒN", "v": VSD, "at": 3}},
    {"type": "broll", "at": 5, "vid": "6220076", "veil": 0.55, "illus": VM,
     "kin": [{"text": "QUÁN CÀ PHÊ · CHỖ LÀM · NHÓM CHAT", "at": 5, "sm": True}, {"text": "AI CŨNG CÓ CHUYỆN LÃI", "at": [5, "ai"], "acc": True}]},
    {"type": "quote", "at": 6, "text": "Mua gì cũng lên. Không vào bây giờ thì bao giờ?", "by": "LỜI TRUYỀN MIỆNG", "dy": True, "qline": 6},
    {"type": "kinetic", "at": 7, "items": [{"text": "ÍT AI ĐỂ Ý", "at": 7, "sm": True}, {"text": "ĐỈNH ĐÃ QUA", "at": [8, "đỉnh"], "acc": True},
                                          {"text": "từ hai tháng trước", "at": [8, "hai"], "sm": True}]},
    {"type": "race", "at": 9, "from": "2021-10-01", "to": "2022-11-15", "title": "VN-INDEX · 10/2021 → 11/2022", "range": "01/10/2021 → 15/11/2022",
     "drawAt": [9, "ngày"], "until": [11, "mất"], "series": [{"key": "vnindex", "label": "VN-INDEX", "color": BLUE}], "source": DATA},
    {"type": "slam", "at": 11, "text": "−40%", "sub": "1.528,57 (06/01/2022) → 911,90 (15/11/2022) · " + SELF},
    {"type": "question", "at": 12, "text": "Người vào tháng kỷ lục\ngiờ ra sao?"},
    {"type": "timeline", "at": 14, "items": [{"year": "2007", "text": "Chặng *một*", "at": 14},
                                            {"year": "2018", "text": "Chặng *hai*", "at": [14, "mười"]},
                                            {"year": "2021", "text": "Chặng *ba*", "at": [14, "mốt"]}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "CÙNG MỘT CẢM GIÁC", "at": 15}, {"text": "KẾT CỤC RẤT GIỐNG", "at": [15, "kết"], "acc": True}]},
    {"type": "brand", "at": 16, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 17, "items": [{"text": "CHỈ GIÁO DỤC", "at": 17, "acc": True}, {"text": "không khuyên mua/bán · không dự báo", "at": [17, "không"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHẶNG 01", "t": "NĂM 2007"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHẶNG MỘT", "title": "NĂM 2007", "sub": "CƠN SỐT ĐẦU TIÊN", "vid": "5028622", "illus": VM, "titleAt": [0, "thị"]},
    {"type": "date", "at": [0, "mở"], "day": "THỊ TRƯỜNG MỞ CỬA", "date": "2000"},
    {"type": "kinetic", "at": 2, "items": [{"text": "CUỐI 2006", "at": 2, "sm": True}, {"text": "≈ 732 ĐIỂM", "at": [2, "bảy"], "acc": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "TẾT 2007", "at": [3, "tết"], "acc": True}, {"text": "“ai cũng có thành tích kiếm tiền để khoe”", "at": 4, "sm": True},
                                          {"text": "SGGP · TỔNG KẾT 2007", "at": 4, "sm": True}]},
    {"type": "counter", "at": 5, "from": 0, "to": 55.72, "prefix": "+", "suffix": "%", "label": "CHỈ TRONG QUÝ 1/2007", "sub": {"text": "SGGP", "at": 5}},
    {"type": "slam", "at": 6, "text": "1.170,67", "sub": "ĐỈNH · 12/03/2007"},
    {"type": "kinetic", "at": 7, "items": [{"text": "> 200.000 TÀI KHOẢN", "at": 7, "acc": True}, {"text": "tới 08/2007 · gấp 3 cùng kỳ", "at": [7, "gấp"], "sm": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "KHỦNG HOẢNG TÀI CHÍNH THẾ GIỚI", "at": 9, "acc": True}]},
    {"type": "bars", "at": 10, "title": "VN-INDEX (ĐIỂM)",
     "items": [{"k": "ĐỈNH 12/03/2007", "v": 1170.67, "lbl": "1.170,67", "at": 10}, {"k": "ĐÁY 24/02/2009", "v": 235.5, "lbl": "235,5", "at": [10, "hai"], "acc": True}],
     "label": {"k": "NGUỒN", "v": "VNEXPRESS · NHỮNG DẤU MỐC CỦA VN-INDEX", "at": 10}},
    {"type": "kinetic", "at": 11, "items": [{"text": "−80%", "at": 11, "acc": True}, {"text": "100 TRIỆU → ~20 TRIỆU", "at": [11, "một"]},
                                           {"text": "nếu đi đúng theo chỉ số · giả định", "at": [11, "nếu"], "sm": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "ĐỨNG YÊN NHƯ CỘT MỐC", "at": 12}, {"text": "> 10 NĂM", "at": [12, "mười"], "acc": True}]},
    {"type": "slam", "at": 13, "text": "1.200", "sub": "CON SỐ SẼ QUAY LẠI"},
]}

CH["ch02"] = {"hud": {"k": "CHẶNG 02", "t": "NĂM 2018"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHẶNG HAI", "title": "NĂM 2018", "sub": "VƯỢT ĐỈNH 11 NĂM", "vid": "7140937", "illus": VM, "titleAt": [0, "ngày"]},
    {"type": "slam", "at": [0, "lên"], "text": "1.204,33", "sub": "09/04/2018"},
    {"type": "kinetic", "at": 1, "items": [{"text": "CAO NHẤT 11 NĂM", "at": 1, "acc": True}, {"text": "vượt cả đỉnh 2007", "at": [1, "vượt"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "BÁO CHÍ BÀN", "at": 2, "sm": True}, {"text": "MỐC 1.300?", "at": [2, "mốc"], "acc": True}]},
    {"type": "bars", "at": 3, "title": "VN-INDEX 2018 (ĐIỂM)",
     "items": [{"k": "ĐỈNH 09/04", "v": 1204.33, "lbl": "1.204", "at": 3}, {"k": "CUỐI THÁNG 7", "v": 935.5, "lbl": "≈ 935", "at": [3, "chín"], "acc": True}],
     "label": {"k": "NGUỒN", "v": "VIETNAM NEWS · VCSC", "at": 3}},
    {"type": "kinetic", "at": 4, "items": [{"text": "> 1/5", "at": 4, "acc": True}, {"text": "giảm từ đỉnh", "at": [4, "giảm"], "sm": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "KHÔNG KHỦNG HOẢNG LỚN", "at": 5, "sm": True}, {"text": "QUÁ NHANH · QUÁ ĐÔNG", "at": 6, "acc": True}]},
    {"type": "ledger", "at": 7, "title": "TỐC ĐỘ", "rows": [{"k": "2017", "v": "+48%", "at": 8}, {"k": "QUÝ 1/2018", "v": "+19,3% · NHANH NHẤT THẾ GIỚI", "at": 9}],
     "srcnote": "VIETNAM NEWS · BIZHUB 04/2018"},
    {"type": "broll", "at": 10, "vid": "38736270", "veil": 0.55, "illus": VM,
     "kin": [{"text": "DỐC ĐỨNG", "at": [10, "dựng"], "acc": True}, {"text": "được chụp lại, chia sẻ khắp nơi", "at": [10, "chụp"], "sm": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "ĐẮT HAY RẺ?", "at": 12, "fx": "strike", "strikeAt": [12, "không"]},
                                           {"text": "AI ĐỨNG NGOÀI = BỊ BỎ LẠI", "at": 13, "acc": True}]},
    {"type": "slam", "at": 14, "text": "CẢM GIÁC > PHÉP TÍNH"},
    {"type": "question", "at": 15, "text": "Giảm nhanh vậy,\nsao lần sau vẫn đổ xô?"},
]}

CH["ch03"] = {"hud": {"k": "CHẶNG 03", "t": "2021"}, "bgm": {"mood": "upbeat", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHẶNG BA", "title": "2021", "sub": "TỪ MỘT ĐÁY RẤT SÂU", "vid": "5467579", "illus": VM, "titleAt": [0, "tháng"]},
    {"type": "slam", "at": 1, "text": "659,21", "sub": "24/03/2020 · DỊCH BỆNH"},
    {"type": "ledger", "at": 2, "title": "VÌ SAO NGƯỜI MỚI ĐỔ VỀ", "rows": [{"k": "1", "v": "LÃI TIẾT KIỆM GIẢM", "at": [2, "lãi"]},
                                                                            {"k": "2", "v": "Ở NHÀ NHIỀU HƠN", "at": [2, "ở"]},
                                                                            {"k": "3", "v": "MỞ TÀI KHOẢN TRÊN ĐIỆN THOẠI", "at": [2, "điện"]}]},
    {"type": "bars", "at": 3, "title": "TÀI KHOẢN MỚI MỖI THÁNG",
     "items": [{"k": "01/2021", "v": 86, "lbl": "≈ 86.000", "at": 3}, {"k": "12/2021", "v": 226.58, "lbl": "226.580", "at": 4, "acc": True},
               {"k": "03/2022", "v": 270.2, "lbl": "270.217", "at": [4, "gấp"]}],
     "label": {"k": "NGUỒN", "v": VSD, "at": 3}},
    {"type": "kinetic", "at": 5, "items": [{"text": "SINH VIÊN · VĂN PHÒNG · VỀ HƯU", "at": 5}, {"text": "LẦN ĐẦU MUA CỔ PHIẾU", "at": [5, "chưa"], "acc": True}]},
    {"type": "race", "at": 6, "from": "2020-03-24", "to": "2022-01-06", "title": "VN-INDEX · ĐÁY 2020 → ĐỈNH 2022", "range": "24/03/2020 → 06/01/2022",
     "drawAt": [6, "chỉ"], "until": [7, "khoảng"], "series": [{"key": "vnindex", "label": "VN-INDEX (% SO VỚI ĐÁY)", "color": UP}], "source": DATA},
    {"type": "kinetic", "at": 8, "items": [{"text": "PHÉP ĐẾM CỦA KÊNH", "at": 8, "acc": True}, {"text": "8 năm · mọi phiên", "at": 9, "sm": True}]},
    {"type": "ledger", "at": 9, "title": "CÁCH ĐẾM", "srcnote": SELF,
     "rows": [{"k": "1", "v": "CHỈ SỐ ĐÃ TĂNG BAO NHIÊU · 12 THÁNG TRƯỚC", "at": [9, "chia"]}, {"k": "2", "v": "12 THÁNG SAU · CAO HƠN HAY THẤP HƠN?", "at": 10}]},
    {"type": "bars", "at": 11, "title": "12 THÁNG SAU: TỈ LỆ PHIÊN CHỈ SỐ THẤP HƠN",
     "items": [{"k": "TRƯỚC ĐÓ GIẢM", "v": R["after_12m"]["<0"]["share_neg_pct"], "lbl": f'{R["after_12m"]["<0"]["share_neg_pct"]}%', "at": 11},
               {"k": "TĂNG 0–20%", "v": R["after_12m"]["0-20"]["share_neg_pct"], "lbl": f'{R["after_12m"]["0-20"]["share_neg_pct"]}%', "at": [11, "tăng"]},
               {"k": "TĂNG 20–40%", "v": R["after_12m"]["20-40"]["share_neg_pct"], "lbl": f'{R["after_12m"]["20-40"]["share_neg_pct"]}%', "at": 12},
               {"k": "TĂNG > 40%", "v": R["after_12m"][">40"]["share_neg_pct"], "lbl": f'{R["after_12m"][">40"]["share_neg_pct"]}%', "at": 13, "acc": True}],
     "label": {"k": "", "v": SELF, "at": 11}},
    {"type": "slam", "at": 13, "text": "≈ 8 / 10", "sub": "12 THÁNG SAU THẤP HƠN · " + SELF},
    {"type": "kinetic", "at": 14, "items": [{"text": "CHO CÔNG BẰNG", "at": 14, "acc": True}]},
    {"type": "timeline", "at": 15, "items": [{"year": "03/2021", "text": "bắt đầu *> +40%*", "at": 15},
                                            {"year": "02/2022", "text": "kết thúc", "at": [15, "hai"]}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "1 LẦN / 8 NĂM", "at": 16, "acc": True}, {"text": "QUY LUẬT", "at": [16, "quy"], "fx": "strike", "strikeAt": [16, "luật"]}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "NHƯNG", "at": 17, "sm": True}, {"text": "HÀNG TRIỆU NGƯỜI", "at": [17, "hàng"], "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "VÌ SAO MUA ĐÚNG ĐỈNH"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "VÌ SAO\nMUA ĐÚNG ĐỈNH", "sub": "TÂM LÝ ĐÁM ĐÔNG", "vid": "38736270", "illus": VM, "titleAt": [0, "nếu"]},
    {"type": "file", "at": 1, "k": "REVIEW OF FINANCIAL STUDIES · 2008", "name": "All That Glitters", "desc": "Brad Barber · Terrance Odean",
     "rows": [{"k": "DỮ LIỆU", "v": "*hàng chục nghìn* nhà đầu tư cá nhân · Mỹ", "at": 2}, {"k": "KẾT QUẢ", "v": "mua ròng cổ phiếu *gây chú ý*", "at": 3}],
     "label": {"k": "NGUỒN", "v": "BARBER & ODEAN (2008), RFS 21(2)", "at": 1}},
    {"type": "ledger", "at": 4, "title": "“GÂY CHÚ Ý” LÀ GÌ", "rows": [{"k": "1", "v": "LÊN BÁO", "at": [4, "lên"]},
                                                                     {"k": "2", "v": "KHỐI LƯỢNG BẤT THƯỜNG", "at": [4, "lượng"]},
                                                                     {"k": "3", "v": "TĂNG / GIẢM RẤT MẠNH 1 NGÀY", "at": [4, "vừa"]}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "MUA", "at": 6, "sm": True}, {"text": "CHỌN TRONG HÀNG NGHÌN MÃ", "at": [6, "chọn"], "acc": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "→ THỨ ĐANG ĐƯỢC NHẮC", "at": 7, "acc": True}, {"text": "BÁN: CHỈ THỨ MÌNH CÓ", "at": 8}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "1 MÃ", "at": [10, "mã"], "fx": "strike", "strikeAt": [10, "mà"]}, {"text": "CẢ THỊ TRƯỜNG", "at": [10, "cả"], "acc": True}]},
    {"type": "broll", "at": 11, "vid": "5359710", "veil": 0.55, "illus": VM,
     "kin": [{"text": "TIN TỨC · NHÓM CHAT · ẢNH TÀI KHOẢN LÃI", "at": 11}]},
    {"type": "slam", "at": 12, "text": "CHÚ Ý NHẤT = GIÁ CAO NHẤT"},
    {"type": "kinetic", "at": 14, "items": [{"text": "NGƯỜI QUEN LÃI", "at": 14, "sm": True}, {"text": "MÌNH TỤT LẠI", "at": 15, "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "KHÓ CHỊU HƠN MẤT TIỀN", "at": 16, "acc": True}, {"text": "diễn giải của kênh", "at": 16, "sm": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "→ LÀM GIỐNG HỌ", "at": [17, "làm"], "acc": True}]},
    {"type": "slam", "at": 18, "text": "FOMO", "sub": "FEAR OF MISSING OUT · NỖI SỢ BỊ BỎ LỠ"},
    {"type": "kinetic", "at": 19, "items": [{"text": "LÚC RẺ", "at": 19, "sm": True}, {"text": "CHẲNG AI NÓI", "at": [19, "chẳng"]},
                                           {"text": "LÚC ĐẮT", "at": 20, "sm": True}, {"text": "AI CŨNG LÃI", "at": [20, "ai"], "acc": True}]},
    {"type": "timeline", "at": 21, "items": [{"year": "01/2022", "text": "*đỉnh* VN-Index", "at": 21},
                                            {"year": "03/2022", "text": "*kỷ lục* tài khoản mới", "at": [21, "kỷ"]}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "HAI NGƯỜI, MỘT THÁNG BA"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "HAI NGƯỜI,\nMỘT THÁNG BA", "sub": "VÍ DỤ GIẢ ĐỊNH · THEO CHỈ SỐ", "vid": "1085656", "illus": VM, "titleAt": [0, "quay"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "31/03/2022", "at": 1, "acc": True}, {"text": "hai người cùng vào thị trường", "at": [1, "hai"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "GIẢ ĐỊNH", "at": 2, "acc": True}, {"text": "theo chỉ số · không phí, thuế, cổ tức", "at": [2, "không"], "sm": True}]},
    {"type": "race", "at": 3, "from": "2022-03-31", "to": "2025-07-25", "money": 100, "title": "NGƯỜI THỨ NHẤT · DỒN 100 TRIỆU", "range": "31/03/2022 → 25/07/2025",
     "drawAt": [3, "người"], "until": [6, "trăm"], "series": [{"key": "vnindex", "label": "100 TRIỆU THEO VN-INDEX", "color": DOWN}], "source": DATA},
    {"type": "ledger", "at": 4, "title": "NGƯỜI THỨ NHẤT", "srcnote": SELF,
     "rows": [{"k": "11/2022", "v": "≈ 61 TRIỆU", "at": 4}, {"k": "12/2023", "v": "≈ 76 TRIỆU", "at": 5}, {"k": "07/2025", "v": "> 100 TRIỆU", "at": 6}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "−39 TRIỆU", "at": 8, "acc": True}, {"text": "mở tài khoản là thấy số âm", "at": [8, "mở"], "sm": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "NHÓM CHAT IM LẶNG", "at": 9}]},
    {"type": "slam", "at": 10, "text": "BÁN Ở GẦN ĐÁY", "sub": "ĐỂ KHỎI NHÌN CON SỐ ẤY"},
    {"type": "kinetic", "at": 11, "items": [{"text": "TRÊN MÀN HÌNH", "at": 11, "fx": "strike", "strikeAt": [11, "thành"]}, {"text": "→ LỖ THẬT", "at": [11, "thật"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "NGƯỜI THỨ HAI", "at": 12, "sm": True}, {"text": "3 TRIỆU MỖI THÁNG", "at": 13, "acc": True},
                                           {"text": "04/2022 → 12/2023", "at": [13, "tới"], "sm": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "LƯƠNG 10–15 TRIỆU", "at": 14}, {"text": "→ 3 TRIỆU VỪA SỨC", "at": [14, "ba"], "acc": True}]},
    {"type": "ledger", "at": 15, "title": "NGƯỜI THỨ HAI · ĐÃ BỎ VÀO 63 TRIỆU", "srcnote": SELF,
     "rows": [{"k": "12/2023", "v": "≈ 62 TRIỆU · GẦN HOÀ VỐN", "at": 16}, {"k": "07/2025", "v": "≈ 84 TRIỆU", "at": 17}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "MUA CẢ THÁNG RẺ NHẤT", "at": 18, "acc": True}, {"text": "khi không ai muốn nói về chứng khoán", "at": [18, "không"], "sm": True}]},
    {"type": "question", "at": 19, "text": "Cứ mua dần\nlà thắng?"},
    {"type": "kinetic", "at": 20, "items": [{"text": "TĂNG MỘT MẠCH", "at": 20}, {"text": "→ DỒN MỘT LẦN HƠN", "at": [20, "người"], "acc": True}]},
    {"type": "kinetic", "at": 21, "items": [{"text": "PHÉP MÀU", "at": 21, "fx": "strike", "strikeAt": [21, "nó"]}, {"text": "KHỎI ĐOÁN ĐỈNH, ĐOÁN ĐÁY", "at": [21, "đoán"], "acc": True}]},
    {"type": "kinetic", "at": 22, "items": [{"text": "NÓNG ĐẦU", "at": 22, "sm": True}, {"text": "KHÔNG CHIẾM HẾT TIỀN", "at": [22, "chiếm"], "acc": True}]},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "BA CÂU HỎI TRƯỚC KHI BẤM MUA"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "BA CÂU HỎI\nTRƯỚC KHI BẤM MUA", "sub": "2025 → NAY", "vid": "7914862", "illus": VM, "titleAt": [0, "năm"]},
    {"type": "race", "at": 1, "from": "2025-04-09", "to": "2026-05-18", "title": "VN-INDEX · 09/04/2025 → 18/05/2026", "range": "09/04/2025 → 18/05/2026",
     "drawAt": [1, "từ"], "until": [2, "đây"], "series": [{"key": "vnindex", "label": "VN-INDEX (% SO VỚI 09/04/2025)", "color": UP}], "source": DATA},
    {"type": "kinetic", "at": 2, "items": [{"text": "LẦN THỨ HAI", "at": 2, "acc": True}, {"text": "> +40% trong 12 tháng · dữ liệu của kênh", "at": [2, "chỉ"], "sm": True}]},
    {"type": "slam", "at": 3, "text": "KÊNH KHÔNG ĐOÁN", "sub": "MỘT LẦN TRONG QUÁ KHỨ KHÔNG PHẢI LỜI TIÊN TRI"},
    {"type": "kinetic", "at": 5, "items": [{"text": "CÓ THỂ TĂNG TIẾP RẤT LÂU", "at": 5, "acc": True}]},
    {"type": "ledger", "at": 6, "title": "3 CÂU TỰ HỎI · KHI AI CŨNG LÃI",
     "rows": [{"k": "1", "v": "NGOÀI VIỆC NGƯỜI KHÁC LÃI, MUA VÌ ĐÂU?", "at": 7}, {"k": "2", "v": "GIẢM 40% CÓ PHẢI BÁN ĐỂ TIÊU?", "at": 8},
              {"k": "3", "v": "VÀO MỘT LẦN HAY NHIỀU LẦN?", "at": 9}]},
    {"type": "question", "at": 10, "text": "Khi nào video này\nkhông đúng?"},
    {"type": "ledger", "at": 11, "title": "KHI NÀO KHÔNG ĐÚNG",
     "rows": [{"k": "✓", "v": "LỢI NHUẬN DOANH NGHIỆP TĂNG THẬT", "at": 11}, {"k": "✓", "v": "TIỀN NHÀN RỖI · CHỜ ĐƯỢC NHIỀU NĂM", "at": 12},
              {"k": "✓", "v": "KHÔNG MUA VÌ SỢ BỊ BỎ LỠ", "at": 13}]},
    {"type": "question", "at": 14, "text": "Bạn mở tài khoản năm nào,\nvà vì sao?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "BÀI SAU", "at": 15, "sm": True}, {"text": "LỖ RỒI CÀNG KHÔNG DÁM BÁN", "at": [15, "lỗ"], "acc": True}]},
]}

SPEC = {
    "title": "Năm 2021 Ai Cũng Lãi: Vì Sao Đó Là Lúc Nguy Hiểm Nhất?",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["vn-index", "fomo", "đỉnh", "kỷ", "lục", "tài", "khoản"],
    "say": SAY, "imgs": {},
    "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Năm 2021 Ai Cũng Lãi: Vì Sao Đó Là Lúc Nguy Hiểm Nhất?",
                   "Tháng Kỷ Lục Mở Tài Khoản Chứng Khoán Lại Đến SAU Đỉnh: Dữ Liệu 2022 Nói Gì",
                   "Ba Lần Cả Nước Đổ Xô Mua Cổ Phiếu, Và Điều Xảy Ra Sau Đó"],
        "summary": "Tháng 3/2022, nhà đầu tư Việt Nam mở hơn 270 nghìn tài khoản chứng khoán — kỷ lục — trong khi đỉnh VN-Index đã qua từ hai "
                   "tháng trước. Video đi qua ba lần cả nước đổ xô đi mua cổ phiếu (2007, 2018, 2021–2022), phép đếm của kênh trên 8 năm "
                   "VN-Index, nghiên cứu \"All That Glitters\" về vì sao nhà đầu tư cá nhân mua thứ đang gây chú ý, và ví dụ hai người cùng vào "
                   "tháng 3/2022 bằng hai cách khác nhau.",
        "more": [C3["youtube"]["more"][0],
                 "📐 CÁCH KÊNH TÍNH (quá khứ, không phải dự báo): VN-Index đóng cửa 08/10/2018–06/10/2026 (HOSE qua vnstock/VCI). Mỗi phiên được "
                 "xếp theo mức tăng 12 tháng (250 phiên) trước đó, rồi xem 12 tháng sau. Nhóm \"tăng hơn 40%\" gần như chỉ là MỘT giai đoạn "
                 "(03/2021–02/2022) — một lần, không phải quy luật. Ví dụ 100 triệu / 3 triệu mỗi tháng là giả định, đi theo chỉ số, không tính "
                 "phí, thuế, cổ tức."],
        "chapter_titles": {"ch00": "Mở đầu: tháng kỷ lục mở tài khoản (03/2022)", "ch01": "Chặng một: 2007",
                           "ch02": "Chặng hai: 2018", "ch03": "Chặng ba: 2021 và phép đếm của kênh",
                           "ch04": "Vì sao người ta mua đúng đỉnh", "ch05": "Hai người, một tháng ba",
                           "ch06": "Ba câu hỏi trước khi bấm mua"},
        "sources": ["https://thoibaotaichinhvietnam.vn/thang-3-lap-ky-luc-khi-co-toi-270000-tai-khoan-chung-khoan-duoc-mo-moi-103199.html",
                    "https://vneconomy.vn/1-5-trieu-tai-khoan-ca-nhan-mo-moi-ky-luc-chua-tung-co-tren-san-chung-khoan-viet-nam.htm",
                    "https://www.sggp.org.vn/nam-gian-kho-cua-con-ho-dang-lon-post50228.html",
                    "https://vnexpress.net/nhung-dau-moc-de-doi-cua-vn-index-2822965.html",
                    "https://vietnamnews.vn/economy/420365/vn-index-ends-2017-at-10-year-high.html",
                    "https://bizhub.vietnamnews.vn/vn-index-worlds-top-performing-market-in-q1-post293779.html",
                    "https://doi.org/10.1093/rfs/hhm079"],
        "hashtags": ["ChứngKhoán", "FOMO", "TâmLýTiềnBạc", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["FOMO", "FOMO chứng khoán", "tâm lý đầu tư", "VN-Index 2022", "mua đúng đỉnh", "tài khoản chứng khoán mở mới",
                 "đầu tư theo đám đông", "mua dần", "chứng khoán cho người mới", "tài chính cá nhân"],
        "category": C3["youtube"]["category"], "data_credit": C3["youtube"].get("data_credit"), "thumb": "t1.jpg",
        "video_credits": C3["youtube"]["video_credits"],
    },
}


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")


if __name__ == "__main__":
    main()
