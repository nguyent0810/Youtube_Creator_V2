"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK E4 "Ngân hàng phá sản thì người gửi tiền được trả bao nhiêu?".

    python motion/long/script_lines.py ck-e4-bao-hiem-tien-gui      # lines + title từ script.md
    python data/long/ck-e4-bao-hiem-tien-gui/gen_scenes.py         # scenes/hud/bgm + spec.json (giữ nguyên lines)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (kiểm độc lập check.py). Kiểm chứng + URL: factcheck.md.
Luật kênh: chỉ giáo dục; không tên ngân hàng thương mại (vụ 10/2022 = "một ngân hàng ở TP.HCM", vụ 03/2023 = "một ngân hàng ở California");
mọi cảnh của ví dụ chị Thu gắn "VÍ DỤ GIẢ ĐỊNH"; không "nên gửi/rút/chia".
B-roll: id Pexels lấy từ kho đã soát logo của các Long CK trước (clip_sheet 15/10). TRƯỚC KHI DỰNG: `pexels.py get` cho topic này rồi chạy
`clip_sheet.py ck-e4-bao-hiem-tien-gui` — soát lại, và cân nhắc thay vài clip để không lặp diện mạo với Long CK gần nhất (variety.py audit).
Neo: chữ đầu tiên của mỗi cảnh neo vào chữ đầu câu; slam ngay chữ đập.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN, VIOLET = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444", "#a78bfa"
HYPO = "VÍ DỤ GIẢ ĐỊNH · LÃI 7%/NĂM · KÊNH TỰ TÍNH"
LAW = "THÔNG TƯ 05/2026/TT-NHNN · TỪ 13/07/2026"
VM = "VIDEO MINH HỌA"
assert R["thu"]["uncovered"] == 850 and R["institutions_needed"] == 4 and R["roll_300_cross_year"] == 3
RL = R["limit_real_2025"]
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MỘT TỶ HAI TRONG MỘT CUỐN SỔ"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "35561857", "veil": 0.55, "illus": VM,
     "kin": [{"text": "THÁNG 10 NĂM 2022", "at": [0, "Đầu"], "sm": True}, {"text": "MỘT TIN ĐỒN TRÊN MẠNG XÃ HỘI", "at": [0, "một"], "acc": True}]},
    {"type": "broll", "at": 2, "vid": "6229548", "veil": 0.55, "illus": VM,
     "kin": [{"text": "XIN RÚT TIỀN TRƯỚC HẠN", "at": [2, "xin"], "acc": True}, {"text": "chấp nhận mất lãi", "at": [3, "chấp"], "sm": True}]},
    {"type": "date", "at": 4, "date": "10/10/2022", "sub": {"text": "THỐNG ĐỐC: TIỀN GỬI “ĐƯỢC NHÀ NƯỚC ĐẢM BẢO TRONG MỌI TRƯỜNG HỢP”", "at": 4}},
    {"type": "kinetic", "at": 6, "items": [{"text": "DÒNG NGƯỜI DẦN THƯA ĐI", "at": 6}, {"text": "BỐN NĂM SAU · MỘT CÂU HỎI BÌNH TĨNH HƠN", "at": 7, "sm": True},
                                          {"text": "VỀ CUỐN SỔ CỦA CHÍNH BẠN", "at": [8, "về"], "acc": True}]},
    {"type": "ledger", "at": 9, "title": "CHỊ THU", "srcnote": "VÍ DỤ GIẢ ĐỊNH", "rows": [{"k": "TUỔI", "v": "52", "at": 9},
                                                                                        {"k": "ĐỂ DÀNH 25 NĂM", "v": "1,2 TỶ", "at": [10, "một"]},
                                                                                        {"k": "Ở ĐÂU", "v": "1 CUỐN SỔ · 1 NƠI", "at": [11, "một"]}]},
    {"type": "question", "at": 12, "text": "Nơi ấy không trả được tiền,\nchị Thu được trả lại bao nhiêu?"},
    {"type": "kinetic", "at": 13, "items": [{"text": "CÓ TRONG LUẬT · VỪA ĐỔI THÁNG 7/2026", "at": 13}, {"text": "và vài chữ nhỏ ít người đọc kỹ", "at": 14, "sm": True}]},
    {"type": "broll", "at": 15, "vid": "8471105", "veil": 0.55, "illus": VM,
     "kin": [{"text": "CUỐI VIDEO", "at": 15, "sm": True}, {"text": "CHỊ THU QUAY LẠI QUẦY · VỚI 4 CUỐN SỔ", "at": [16, "chị"], "acc": True},
             {"text": "và một câu hỏi khác", "at": 17, "sm": True}]},
    {"type": "brand", "at": 18, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 19, "items": [{"text": "CHỈ NHẰM GIÁO DỤC", "at": 19, "acc": True},
                                           {"text": "không phải lời khuyên gửi, rút hay chia tiền · không nói về ngân hàng nào", "at": [19, "không"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "350 TRIỆU"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CON SỐ\n350 TRIỆU", "sub": "HẠN MỨC TRẢ TIỀN BẢO HIỂM", "vid": "6980366", "illus": VM, "titleAt": [0, "Bắt"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "HẠN MỨC TRẢ TIỀN BẢO HIỂM", "at": 1, "acc": True},
                                          {"text": "= số tối đa được trả khi nơi bạn gửi tiền đổ vỡ", "at": 2, "sm": True}]},
    {"type": "bars", "at": 3, "title": "HẠN MỨC (TRIỆU ĐỒNG · MỖI NGƯỜI · MỖI NƠI)", "unit": "GỒM GỐC VÀ LÃI",
     "items": [{"k": "TỪ 2021", "v": 125, "lbl": "125", "at": [4, "Trước"]}, {"k": "TỪ 13/07/2026", "v": 350, "lbl": "350", "at": [3, "ba"], "acc": True}],
     "label": {"k": LAW, "v": "", "at": 3}},
    {"type": "slam", "at": 5, "text": "GẦN GẤP BA", "sub": "+180%"},
    {"type": "ledger", "at": 6, "title": "AI TRẢ KHOẢN NÀY?", "rows": [{"k": "KHÔNG PHẢI", "v": "NGÂN HÀNG CỦA BẠN", "at": 7},
                                                                    {"k": "MỖI QUÝ", "v": "NƠI NHẬN TIỀN GỬI ĐÓNG PHÍ", "at": 8}],
     "total": {"k": "KHI CÓ CHUYỆN", "v": "QUỸ DỰ PHÒNG TRẢ", "at": 9}},
    {"type": "question", "at": 10, "text": "Phải đổ vỡ tới mức nào\nthì mới được trả?"},
    {"type": "kinetic", "at": 11, "items": [{"text": "LUẬT 2025 · BA TRƯỜNG HỢP PHẢI TRẢ", "at": 11, "acc": True},
                                           {"text": "1 · phương án phá sản được duyệt", "at": 12, "sm": True},
                                           {"text": "2 · kiểm soát đặc biệt, lỗ vượt vốn, đình chỉ nhận tiền gửi", "at": 13, "sm": True},
                                           {"text": "3 · Chính phủ quyết định yêu cầu chi trả", "at": 14, "sm": True}]},
    {"type": "counter", "at": 16, "from": 45, "to": 45, "suffix": " NGÀY", "label": "TỐI ĐA ĐỂ TRẢ · TRƯỚC ĐÂY 60 NGÀY",
     "sub": {"text": "TÍNH TỪ LÚC PHÁT SINH NGHĨA VỤ TRẢ", "at": 17}},
    {"type": "bars", "at": 18, "title": "1,2 TỶ CỦA CHỊ THU (TRIỆU ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "CHẮC CHẮN ĐƯỢC TRẢ", "v": 350, "lbl": "350", "at": [20, "khoản"], "acc": True},
               {"k": "NẰM NGOÀI HẠN MỨC", "v": 850, "lbl": "850", "at": [21, "Tám"]}]},
    {"type": "kinetic", "at": 22, "items": [{"text": "TRƯỚC 13/07/2026: NGOÀI HẠN MỨC 1.075 TRIỆU", "at": 22, "sm": True},
                                           {"text": "NGOÀI HẠN MỨC ≠ MẤT TRẮNG", "at": 23, "acc": True},
                                           {"text": "= chờ xử lý tài sản sau đó, không còn là lời hứa chắc chắn", "at": 24, "sm": True}]},
    {"type": "slam", "at": 25, "text": "CÒN MỘT CHI TIẾT", "sub": "CUỐN SỔ TỰ VƯỢT HẠN MỨC"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "GỐC CỘNG LÃI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "GỐC CỘNG LÃI", "sub": "VÀ CUỐN SỔ TỰ LỚN LÊN", "vid": "13107027", "illus": VM, "titleAt": [0, "Hạn"]},
    {"type": "myth", "at": 1, "mythLab": "NHIỀU NGƯỜI NGHĨ", "myth": "350 TRIỆU TIỀN GỐC", "truthLab": "THẬT RA", "truth": "350 TRIỆU CẢ GỐC LẪN LÃI",
     "strikeAt": [1, "Không"], "truthAt": [1, "gốc"]},
    {"type": "source", "at": 2, "source": "LÃI 12 THÁNG · KHẢO SÁT BÁO CHÍ 09/10/2026", "ref": "LÃI SUẤT GIẢ ĐỊNH CỦA VÍ DỤ",
     "snippet": "niêm yết phổ biến [[từ gần 6% tới hơn 7%]] · ví dụ dùng 7%", "hlAt": [3, "gần"], "seal": "VÍ DỤ GIẢ ĐỊNH", "sealAt": 4},
    {"type": "bars", "at": 5, "title": "GỬI ĐÚNG 350 TRIỆU, 1 NĂM SAU (TRIỆU ĐỒNG)", "unit": HYPO.split(" · ")[0],
     "items": [{"k": "HẠN MỨC", "v": 350, "lbl": "350", "at": [5, "Một"]}, {"k": "GỐC + LÃI", "v": 374.5, "lbl": "374,5", "at": [5, "ba"], "acc": True}]},
    {"type": "slam", "at": 6, "text": "+24,5 TRIỆU", "sub": "ĐÃ NGOÀI HẠN MỨC"},
    {"type": "question", "at": 7, "text": "Gửi tối đa bao nhiêu\nđể gốc + lãi một năm vẫn trong hạn mức?"},
    {"type": "counter", "at": 8, "from": 0, "to": 327, "suffix": " TRIỆU", "label": "GỐC TỐI ĐA · LÃI 7%/NĂM · 12 THÁNG", "sub": {"text": "350 ÷ 1,07 · " + HYPO.split(" · ")[0], "at": 9}},
    {"type": "bars", "at": 11, "title": "SỔ 300 TRIỆU CUỘN CẢ GỐC LẪN LÃI (TRIỆU ĐỒNG)", "unit": HYPO.split(" · ")[0],
     "items": [{"k": "NĂM 1", "v": 321, "lbl": "321", "at": [12, "Năm"]}, {"k": "NĂM 2", "v": 343.5, "lbl": "≈ 344", "at": [13, "Năm"]},
               {"k": "NĂM 3", "v": 367.5, "lbl": "≈ 368", "at": [14, "Sang"], "acc": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "KHÔNG GỬI THÊM ĐỒNG NÀO", "at": 15, "sm": True}, {"text": "CUỐN SỔ TỰ BƯỚC QUA VẠCH", "at": 16, "acc": True}]},
    {"type": "ledger", "at": 17, "title": "HẠN MỨC TÍNH CHO…", "rows": [{"k": "MỖI NGƯỜI", "v": "VỢ + CHỒNG = 700 TRIỆU", "at": [19, "Mỗi"]},
                                                                     {"k": "MỖI TỔ CHỨC", "v": "KHÔNG PHẢI MỖI CHI NHÁNH", "at": 20}],
     "total": {"k": "2 PHÒNG GIAO DỊCH", "v": "VẪN 1 HẠN MỨC", "at": 21}},
    {"type": "question", "at": 22, "text": "Có nhiều người\nvượt hạn mức không?"},
    {"type": "units", "at": 23, "title": "MỨC 350 TRIỆU · NGƯỜI GỬI ĐƯỢC BẢO VỆ TOÀN BỘ", "total": 16, "cols": 16, "lit": 15, "litAt": [23, "chín"],
     "unitLabel": "≈ 93,7% · CỨ KHOẢNG 16 NGƯỜI CÓ 1 NGƯỜI VƯỢT", "label": {"k": "SỐ LIỆU CÔNG BỐ KHI NÂNG HẠN MỨC (QUA BÁO PHÁP LUẬT)", "v": "", "at": 24}},
    {"type": "kinetic", "at": 26, "items": [{"text": "350 TRIỆU LÀ NHIỀU HAY ÍT?", "at": 26, "acc": True}, {"text": "nhìn lại 25 năm của chính con số này", "at": 27, "sm": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "25 NĂM CỦA MỘT HẠN MỨC"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "25 NĂM\nCỦA MỘT HẠN MỨC", "sub": "1999 → 2026", "vid": "9160920", "illus": VM, "titleAt": [0, "Bảo"]},
    {"type": "timeline", "at": 1, "title": "HẠN MỨC BẢO HIỂM TIỀN GỬI (TRIỆU ĐỒNG)", "items": [
        {"year": "1999", "text": "30", "at": 1}, {"year": "2005", "text": "50 · đứng yên 12 năm", "at": 2}, {"year": "2017", "text": "75", "at": 4},
        {"year": "2021", "text": "125", "at": 5}, {"year": "2026", "text": "350", "at": 6}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "CHỈ CÓ TĂNG?", "at": 7}, {"text": "tiền năm 1999 đâu phải tiền hôm nay", "at": 8, "sm": True},
                                          {"text": "QUY VỀ GIÁ NĂM 2025 BẰNG CHỈ SỐ GIÁ TIÊU DÙNG", "at": 9, "acc": True}]},
    {"type": "bars", "at": 10, "title": "HẠN MỨC QUY VỀ GIÁ 2025 (TRIỆU ĐỒNG)", "unit": "CPI BÌNH QUÂN NĂM · KÊNH TỰ TÍNH",
     "items": [{"k": "30 TR · 1999", "v": RL["1999"], "lbl": f"≈ {round(RL['1999'])}", "at": [10, "Ba"]},
               {"k": "50 TR · 2005", "v": RL["2005"], "lbl": f"≈ {round(RL['2005'])}", "at": [11, "Năm"]},
               {"k": "75 TR · 2017", "v": RL["2017"], "lbl": f"≈ {round(RL['2017'])}", "at": [12, "Còn"], "acc": True},
               {"k": "125 TR · 2021", "v": RL["2021"], "lbl": f"≈ {round(RL['2021'])}", "at": [18, "Lên"]}],
     "label": {"k": "DỮ LIỆU: WORLD BANK WDI (TỪ SỐ LIỆU CỤC THỐNG KÊ) · KÊNH TỰ TÍNH", "v": "", "at": 10}},
    {"type": "slam", "at": 14, "text": "NHỎ ĐI THẬT", "sub": "12 NĂM ĐỨNG YÊN · GIÁ VẪN LÊN"},
    {"type": "kinetic", "at": 16, "items": [{"text": "MỘT CON SỐ ĐỨNG YÊN", "at": 16, "sm": True}, {"text": "GIỮA NỀN GIÁ ĐI LÊN = ĐANG NHỎ DẦN", "at": [16, "giữa"], "acc": True}]},
    {"type": "bars", "at": 17, "title": "NGƯỜI GỬI ĐƯỢC BẢO VỆ TOÀN BỘ (%)", "unit": "THEO HẠN MỨC",
     "items": [{"k": "75 TRIỆU", "v": 87, "lbl": "≈ 87", "at": [17, "khoảng"]}, {"k": "125 TRIỆU", "v": 92, "lbl": "> 92", "at": [18, "hơn"]},
               {"k": "350 TRIỆU", "v": 93.68, "lbl": "93,68", "at": [19, "gần"], "acc": True}],
     "label": {"k": "NGHIÊN CỨU QUA BÁO CHÍ 2020 · DIV 2024 · BÁO PHÁP LUẬT 09/2026", "v": "", "at": 17}},
    {"type": "broll", "at": 20, "vid": "7710771", "veil": 0.55, "illus": VM,
     "kin": [{"text": "25 NĂM ĐỂ DÀNH CỦA CHỊ THU", "at": 20}, {"text": "có năm cuốn sổ lớn nhanh hơn lá chắn", "at": 21, "sm": True}]},
    {"type": "ledger", "at": 22, "title": "LUẬT BẢO HIỂM TIỀN GỬI 2025", "rows": [{"k": "BỎ", "v": "CON SỐ CỐ ĐỊNH TRONG LUẬT", "at": 22},
                                                                               {"k": "THỐNG ĐỐC", "v": "QUYẾT ĐỊNH THEO THỜI KỲ", "at": 23}]},
    {"type": "question", "at": 25, "text": "Thứ gì trông như sổ tiết kiệm\nmà nằm ngoài lá chắn?"},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "TRÔNG NHƯ SỔ TIẾT KIỆM"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "NHỮNG THỨ TRÔNG\nNHƯ SỔ TIẾT KIỆM", "sub": "ĐƯỢC VÀ KHÔNG ĐƯỢC BẢO HIỂM", "vid": "7841584", "illus": VM, "titleAt": [0, "Luật"]},
    {"type": "source", "at": 1, "source": "LUẬT BẢO HIỂM TIỀN GỬI 2025 · ĐIỀU 17 (QUA BÁO PHÁP LUẬT)", "ref": "TIỀN GỬI ĐƯỢC BẢO HIỂM",
     "snippet": "[[tiền gửi bằng đồng Việt Nam của cá nhân]] · có kỳ hạn, không kỳ hạn, tiết kiệm, chứng chỉ tiền gửi", "hlAt": [1, "tiền"], "seal": "ĐỨNG TÊN BẠN", "sealAt": 3},
    {"type": "ledger", "at": 4, "title": "KHÔNG ĐƯỢC BẢO HIỂM (MỘT PHẦN)", "rows": [{"k": "SỞ HỮU > 5% VỐN", "v": "CỦA CHÍNH NƠI ĐÓ", "at": 5},
                                                                                  {"k": "NGƯỜI QUẢN LÝ", "v": "ĐIỀU HÀNH Ở ĐÓ", "at": 6},
                                                                                  {"k": "GIẤY TỜ CÓ GIÁ", "v": "VÔ DANH", "at": [7, "vô"]}]},
    {"type": "question", "at": 8, "text": "Người bình thường\nthì liên quan gì?"},
    {"type": "kinetic", "at": 9, "items": [{"text": "LIÊN QUAN Ở CHỖ ĐỊNH NGHĨA", "at": 9}, {"text": "CHỈ TIỀN GỬI BẰNG ĐỒNG VIỆT NAM", "at": 10, "acc": True},
                                          {"text": "tiền gửi bằng đô la: ngoài diện này", "at": 11, "sm": True}]},
    {"type": "broll", "at": 12, "vid": "7735497", "veil": 0.55, "illus": VM,
     "kin": [{"text": "BÁN Ở QUẦY · KHÔNG PHẢI TIỀN GỬI", "at": 12, "acc": True}, {"text": "bảo hiểm nhân thọ", "at": 13, "sm": True},
             {"text": "trái phiếu công ty", "at": 14, "sm": True}, {"text": "chứng chỉ quỹ", "at": 15, "sm": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "CÙNG NHÂN VIÊN · CÙNG CHIẾC BÀN", "at": 16, "sm": True}, {"text": "KHÁC SẢN PHẨM · KHÁC RỦI RO", "at": 17, "acc": True},
                                           {"text": "không nằm trong hạn mức 350 triệu", "at": 18, "sm": True}]},
    {"type": "question", "at": 19, "text": "Làm sao biết\nthứ mình đang cầm là gì?"},
    {"type": "myth", "at": 20, "mythLab": "TỜ GIẤY GHI", "myth": "HỢP ĐỒNG BẢO HIỂM · TRÁI PHIẾU · CHỨNG CHỈ QUỸ", "truthLab": "TIỀN GỬI LÀ",
     "truth": "SỔ TIẾT KIỆM · HỢP ĐỒNG / CHỨNG CHỈ TIỀN GỬI · CÓ TÊN BẠN", "strikeAt": [22, "Nếu"], "truthAt": [21, "Nếu"]},
    {"type": "kinetic", "at": 23, "items": [{"text": "KHÔNG CÓ NGHĨA LÀ XẤU", "at": 23}, {"text": "mỗi loại có luật riêng", "at": 24, "sm": True},
                                           {"text": "KÝ Ở QUẦY ≠ ĐƯỢC BẢO HIỂM NHƯ TIỀN GỬI", "at": 25, "acc": True}]},
    {"type": "broll", "at": 26, "vid": "40200251", "veil": 0.6, "illus": VM,
     "kin": [{"text": "BÊN KIA ĐẠI DƯƠNG", "at": 26, "sm": True}, {"text": "SỤP TRONG HAI NGÀY", "at": [26, "sụp"], "acc": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "40 TỶ ĐÔ LA TRONG MỘT NGÀY"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "40 TỶ ĐÔ LA\nTRONG MỘT NGÀY", "sub": "CALIFORNIA · THÁNG 3/2023", "vid": "34796502", "illus": VM, "titleAt": [0, "Tháng"]},
    {"type": "timeline", "at": 1, "title": "MỘT NGÂN HÀNG Ở CALIFORNIA · 03/2023", "items": [
        {"year": "8/3", "text": "vài thông báo về tài chính", "at": 2}, {"year": "9/3", "text": "> 40 tỷ USD rút trong một ngày", "at": 4},
        {"year": "10/3", "text": "đóng cửa", "at": 7}, {"year": "12/3", "text": "bảo đảm toàn bộ tiền gửi", "at": 14}],
     "label": {"k": "NGUỒN: BÁO CÁO CỦA FED 28/04/2023 · CRS (QUỐC HỘI MỸ)", "v": "", "at": 1}},
    {"type": "counter", "at": 5, "from": 0, "to": 85, "suffix": "%", "label": "TIỀN GỬI MUỐN RỜI ĐI · 9 + 10/3", "sub": {"text": "> 40 TỶ USD NGÀY 9/3 · DỰ KIẾN > 100 TỶ NGÀY 10/3", "at": 6}},
    {"type": "slam", "at": 8, "text": "CHƯA TỚI HAI NGÀY", "sub": "TỪ MỘT THÔNG BÁO TỚI CÁNH CỬA ĐÓNG"},
    {"type": "question", "at": 9, "text": "Bên đó cũng có\nbảo hiểm tiền gửi mà?"},
    {"type": "units", "at": 10, "title": "HẠN MỨC MỸ 250.000 USD · CUỐI 2022", "total": 50, "cols": 10, "lit": 47, "litAt": [11, "chín"],
     "unitLabel": "≈ 94% TIỀN GỬI VƯỢT HẠN MỨC", "label": {"k": "NGƯỜI GỬI CHỦ YẾU LÀ CÔNG TY", "v": "", "at": 12}},
    {"type": "kinetic", "at": 13, "items": [{"text": "PHẦN LỚN TIỀN NẰM NGOÀI LÁ CHẮN", "at": 13, "acc": True}, {"text": "một tin xấu, ai cũng muốn chạy trước", "at": [13, "chỉ"], "sm": True}]},
    {"type": "ledger", "at": 14, "title": "12/03/2023 · NGOẠI LỆ RỦI RO HỆ THỐNG", "rows": [{"k": "TIỀN GỬI", "v": "BẢO ĐẢM TOÀN BỘ", "at": 15},
                                                                                         {"k": "CỔ ĐÔNG, TRÁI CHỦ", "v": "KHÔNG", "at": 17}]},
    {"type": "source", "at": 18, "source": "LUẬT BẢO HIỂM TIỀN GỬI 2025 (QUA BÁO PHÁP LUẬT)", "ref": "CHI TRẢ ĐẶC BIỆT",
     "snippet": "Thống đốc có thể quyết định [[hạn mức cao hơn]], tối đa bằng toàn bộ tiền gửi được bảo hiểm", "hlAt": [19, "cao"],
     "seal": "TỪNG TRƯỜNG HỢP CỤ THỂ", "sealAt": 20},
    {"type": "myth", "at": 22, "mythLab": "PHẦN TRÊN HẠN MỨC", "myth": "PHỤ THUỘC MỘT QUYẾT ĐỊNH", "truthLab": "PHẦN TRONG HẠN MỨC", "truth": "CHẮC CHẮN · VIẾT SẴN TRONG LUẬT",
     "strikeAt": [24, "Phần"], "truthAt": [23, "Phần"]},
    {"type": "kinetic", "at": 25, "items": [{"text": "10/2022: CÂU NÓI GIÚP NGƯỜI DÂN YÊN TÂM", "at": 25, "sm": True},
                                           {"text": "TRÊN GIẤY: HẠN MỨC CHO MỖI NGƯỜI, Ở MỖI NƠI", "at": 26, "acc": True}]},
    {"type": "question", "at": 27, "text": "Với 1,2 tỷ của chị Thu,\nphần chắc chắn lớn tới đâu?"},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "BỐN CUỐN SỔ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "BỐN CUỐN SỔ\nCỦA CHỊ THU", "sub": "VÀ KHI NÀO PHÉP TÍNH KHÔNG ĐÚNG", "vid": "6266262", "illus": VM, "titleAt": [0, "Quay"]},
    {"type": "ledger", "at": 1, "title": "1,2 TỶ · LÃI 7% · SAU 1 NĂM", "srcnote": HYPO, "rows": [{"k": "GỐC + LÃI", "v": "≈ 1.284 TRIỆU", "at": [1, "sau"]},
                                                                                            {"k": "MỖI NƠI TỐI ĐA", "v": "350 TRIỆU", "at": [2, "Chia"]}],
     "total": {"k": "CẦN ÍT NHẤT", "v": "4 NƠI", "at": [2, "bốn"]}},
    {"type": "units", "at": 3, "title": "4 CUỐN SỔ · MỖI CUỐN ≈ 300 TRIỆU", "total": 4, "cols": 4, "lit": 4, "litAt": [4, "toàn"],
     "unitLabel": "CẢ GỐC LẪN LÃI TRONG HẠN MỨC", "label": {"k": HYPO, "v": "", "at": 3}},
    {"type": "question", "at": 6, "text": "Vậy là cứ\nchia ra cho chắc?"},
    {"type": "ledger", "at": 8, "title": "CÁI GIÁ CỦA VIỆC CHIA", "rows": [{"k": "4 NƠI", "v": "4 MỨC LÃI · 4 LẦN ĐÁO HẠN", "at": 9},
                                                                       {"k": "RÚT TRƯỚC HẠN", "v": "THƯỜNG CHỈ CÒN LÃI KKH", "at": 10},
                                                                       {"k": "NHIỀU NGƯỜI", "v": "1 NƠI QUEN LÀ ĐỦ YÊN TÂM", "at": 11}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "KHÔNG BẢO BẠN CHIA HAY KHÔNG", "at": 12}, {"text": "CHỈ ĐẶT HAI CON SỐ CẠNH NHAU", "at": 13, "acc": True},
                                           {"text": "tiền của bạn ở mỗi nơi · hạn mức", "at": [13, "tiền"], "sm": True}]},
    {"type": "ledger", "at": 14, "title": "KHI NÀO PHÉP TÍNH KHÔNG ĐÚNG", "rows": [{"k": "1", "v": "LÃI 7% LÀ GIẢ ĐỊNH", "at": 15},
                                                                                {"k": "2", "v": "HẠN MỨC CÓ THỂ CÒN ĐỔI", "at": 16},
                                                                                {"k": "3", "v": "LỚP BẢO VỆ CUỐI CÙNG", "at": 17}]},
    {"type": "ledger", "at": 18, "title": "BA CÂU TỰ HỎI TRƯỚC CUỐN SỔ", "rows": [{"k": "1", "v": "GỐC + LÃI KỲ TỚI Ở MỖI NƠI?", "at": 19},
                                                                                 {"k": "2", "v": "TIỀN GỬI VNĐ, ĐỨNG TÊN TÔI?", "at": 20},
                                                                                 {"k": "3", "v": "CÓ NIÊM YẾT THAM GIA BHTG?", "at": 21}]},
    {"type": "broll", "at": 22, "vid": "5909916", "veil": 0.55, "illus": VM,
     "kin": [{"text": "CẢNH ĐÃ HẸN", "at": 22, "sm": True}, {"text": "BỐN CUỐN SỔ MỎNG HƠN", "at": [23, "bốn"], "acc": True},
             {"text": "25 năm: “kỳ này lãi bao nhiêu?”", "at": 24, "sm": True}]},
    {"type": "slam", "at": 26, "text": "PHẦN NÀO ĐƯỢC LUẬT BẢO VỆ?", "sub": "CÂU HỎI MỚI CỦA CHỊ THU"},
    {"type": "myth", "at": 27, "mythLab": "LÃI SUẤT", "myth": "TIỀN LỚN NHANH TỚI ĐÂU", "truthLab": "HẠN MỨC", "truth": "BAO NHIÊU LÀ CHẮC CHẮN",
     "strikeAt": [28, "Hạn"], "truthAt": [28, "bao"]},
    {"type": "question", "at": 29, "text": "Bạn đã cộng gốc với lãi\nđể so với hạn mức chưa?"},
    {"type": "kinetic", "at": 30, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 30}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [30, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
TITLES = ["Ngân Hàng Phá Sản, Gửi 1,2 Tỷ Được Trả Bao Nhiêu?",
          "Bảo Hiểm Tiền Gửi 350 Triệu Từ 2026: Gửi 1 Tỷ Ở Một Nơi Thì Được Bảo Vệ Bao Nhiêu?",
          "Gửi Tiết Kiệm 400 Triệu Có Được Bảo Hiểm Hết Không? Hạn Mức Tính Cả Gốc Lẫn Lãi"]
SPEC = {
    "title": TITLES[0],
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["hạn", "mức", "gốc", "lãi", "sổ", "triệu", "bảo"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": TITLES,
        "summary": "Từ 13/07/2026, hạn mức bảo hiểm tiền gửi là 350 triệu đồng cho mỗi người, tại mỗi tổ chức, tính cả gốc lẫn lãi (trước đó 125 "
                   "triệu). Video theo cuốn sổ 1,2 tỷ của chị Thu (ví dụ giả định): nếu nơi gửi đổ vỡ thì phần nào chắc chắn được trả, vì sao một sổ "
                   "300 triệu để cuộn lãi có thể tự vượt hạn mức, hạn mức 25 năm qua nhỏ đi ra sao khi quy về giá hôm nay, thứ gì bán ở quầy giao dịch "
                   "nhưng không phải tiền gửi, và chuyện bốn mươi tỷ đô la rời một ngân hàng ở California chỉ trong một ngày năm 2023.",
        "more": ["Nội dung giáo dục, không phải tư vấn đầu tư. Kênh không khuyến nghị gửi, rút hay chia tiền ở bất kỳ tổ chức nào và không đánh giá "
                 "sức khoẻ của ngân hàng nào. Chị Thu, số tiền 1,2 tỷ và lãi suất 7%/năm là ví dụ giả định do kênh tự tính. Quy định mô tả theo thời "
                 "điểm làm video (10/2026) và có thể thay đổi; hạn mức nay do Thống đốc Ngân hàng Nhà nước quyết định theo từng thời kỳ. Nội dung do "
                 "kênh biên soạn từ nguồn công khai; giọng đọc tổng hợp.",
                 "📐 CÁCH KÊNH TÍNH: hạn mức 350 triệu gồm cả gốc và lãi → gốc tối đa để gốc + lãi 12 tháng vẫn trong hạn mức = 350 ÷ (1 + lãi suất); "
                 "với lãi giả định 7%: ≈ 327 triệu. Sổ 300 triệu cuộn cả gốc lẫn lãi 7%/năm: 321 → 343,5 → 367,5 triệu (vượt ở năm thứ 3). Hạn mức các "
                 "thời kỳ quy về giá năm 2025 bằng chỉ số giá tiêu dùng bình quân năm (World Bank WDI, từ số liệu Cục Thống kê): 30 triệu (1999) ≈ 120; "
                 "50 triệu (2005) ≈ 164; 75 triệu (2017) ≈ 96; 125 triệu (2021) ≈ 142 triệu."],
        "chapter_titles": {"ch00": "Mở đầu: một tỷ hai trong một cuốn sổ", "ch01": "Con số 350 triệu: ai trả, khi nào, bao lâu",
                           "ch02": "Gốc cộng lãi: cuốn sổ tự vượt hạn mức", "ch03": "25 năm của một hạn mức (quy về giá hôm nay)",
                           "ch04": "Những thứ trông như sổ tiết kiệm mà không phải tiền gửi", "ch05": "40 tỷ đô la rời một ngân hàng trong một ngày (03/2023)",
                           "ch06": "Bốn cuốn sổ của chị Thu và khi nào phép tính không đúng"},
        "sources": [
            "Công báo — Thông tư 05/2026/TT-NHNN, hạn mức chi trả 350 triệu đồng, hiệu lực 13/07/2026: https://congbao.chinhphu.vn/van-ban/thong-tu-so-05-2026-tt-nhnn-470097/67202.htm",
            "Cổng TTĐT Chính phủ — Luật Bảo hiểm tiền gửi số 111/2025/QH15 (văn bản gốc): https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/111-qh15-2025.signed.pdf",
            "BHTGVN — Từ 13/7/2026 hạn mức chi trả 350 triệu đồng: https://div.gov.vn/tu-ngay-13-7-2026-han-muc-chi-tra-tien-bao-hiem-cua-bao-hiem-tien-gui-viet-nam-la-350-trieu-dong",
            "Báo Pháp luật (Doanh nhân) 13/09/2026 — Luật Bảo hiểm tiền gửi 2025, những điểm mới: https://doanhnhan.baophapluat.vn/luat-bao-hiem-tien-gui-nam-2025-nhung-diem-moi-nguoi-gui-tien-can-quan-tam-add14ad3.html",
            "BHTGVN 12/09/2024 — Hạn mức trả tiền bảo hiểm: https://div.gov.vn/han-muc-tra-tien-bao-hiem-cong-cu-toi-uu-bao-ve-quyen-loi-nguoi-gui-tien",
            "Báo Pháp luật 24/08/2020 — Hạn mức trả tiền bảo hiểm qua các thời kỳ: https://baophapluat.vn/han-muc-tra-tien-bao-hiem-cong-cu-huu-hieu-de-bao-ve-nguoi-gui-tien-post359929.html",
            "Đại Đoàn Kết 10/10/2022 — Thống đốc: tiền gửi của người dân được Nhà nước đảm bảo trong mọi trường hợp: https://daidoanket.vn/thong-doc-nhnn-moi-khoan-tien-gui-tai-ngan-hang-deu-duoc-nha-nuoc-dam-bao-10233840.html",
            "Congressional Research Service IF12378 — systemic risk exception, 12/03/2023: https://www.congress.gov/crs_external_products/IF/PDF/IF12378/IF12378.2.pdf",
            "Tạp chí Kinh tế Tài chính 09/10/2026 — lãi suất 12 tháng đầu tháng 10: https://tapchikinhtetaichinh.vn/lai-suat-ty-gia-hom-nay-lai-huy-dong-binh-quan-len-6-46-nam-usd-ngan-hang-giam-gia-169067.html",
            "World Bank WDI — Consumer price index (2010 = 100), Viet Nam: https://data.worldbank.org/indicator/FP.CPI.TOTL?locations=VN"],
        "hashtags": ["BảoHiểmTiềnGửi", "TiếtKiệm", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["bảo hiểm tiền gửi", "hạn mức bảo hiểm tiền gửi 350 triệu", "ngân hàng phá sản thì người gửi tiền", "gửi tiết kiệm có an toàn không",
                 "luật bảo hiểm tiền gửi 2025", "tiền gửi được bảo hiểm", "sổ tiết kiệm", "tài chính cá nhân", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: quy định theo Luật Bảo hiểm tiền gửi số 111/2025/QH15 và Thông tư 05/2026/TT-NHNN (văn bản gốc ở trên); chỉ số giá tiêu dùng "
                       "theo World Bank WDI (từ số liệu Cục Thống kê); ví dụ chị Thu và phép tính do kênh tự lập.",
        "video_credits": Y4["video_credits"],
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
