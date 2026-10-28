"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK A2 "Lương 10 triệu năm 2016 bằng bao nhiêu tiền hôm nay?".

    python motion/long/script_lines.py ck-a2-luong-va-lam-phat      # lines + title từ script.md
    python data/long/ck-a2-luong-va-lam-phat/gen_scenes.py         # scenes/hud/bgm + spec.json (giữ nguyên lines)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (kiểm độc lập check.py). Kiểm chứng + URL: factcheck.md.
Luật kênh: chỉ giáo dục, KHÔNG dự báo — mức lạm phát 2027–2036 là giả định 3/4/5% (nhãn trên màn hình); anh Tuấn, chị Mai, tỷ trọng giỏ = VÍ DỤ GIẢ ĐỊNH;
không "nên mua vàng/gửi/đầu tư để chống lạm phát". Mô-típ: phong bì 10 triệu 2016 và phiếu lương 13 triệu 2026 (CH00, CH02, CH06).
B-roll: id Pexels từ kho đã soát của các Long CK trước — trước khi dựng: `pexels.py get` + `clip_sheet.py ck-a2-luong-va-lam-phat`; CẤM clip trạm xăng có
logo/biển hiệu hãng (31144326 đã dùng ở A1 — soát lại khung) và quầy hàng có tên thương hiệu.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN, VIOLET = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444", "#a78bfa"
HYPO = "VÍ DỤ GIẢ ĐỊNH · ANH TUẤN · LƯƠNG 10 TRIỆU NĂM 2016"
CPI_SRC = "CPI BÌNH QUÂN NĂM: WORLD BANK WDI (TỪ SỐ LIỆU CỤC THỐNG KÊ) · 2026 = BÌNH QUÂN 9 THÁNG +4,52%"
NSO9 = "CỤC THỐNG KÊ · THÁNG 9/2026 SO CÙNG KỲ"
VM = "VIDEO MINH HỌA"
assert R["salary_equiv_2026"] == 13.8 and R["power_left_2026"] == 7.25 and R["real_13"] == -5.8
Y = R["yearly"]
N36 = R["need_2036"]
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "PHONG BÌ MƯỜI TRIỆU"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "11321634", "veil": 0.55, "illus": VM,
     "kin": [{"text": "THÁNG 10/2016 · HÀ NỘI", "at": [0, "Tháng"], "sm": True}, {"text": "THÁNG LƯƠNG ĐẦU TIÊN: 10 TRIỆU", "at": [1, "Mười"], "acc": True},
             {"text": "anh Tuấn · nhân vật ví dụ", "at": [1, "Một"], "sm": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "TIỀN PHÒNG · GỬI VỀ NHÀ", "at": 3, "sm": True}, {"text": "CUỐI THÁNG VẪN CÒN DƯ", "at": [3, "cuối"], "acc": True}]},
    {"type": "bars", "at": 4, "title": "LƯƠNG CỦA ANH TUẤN (TRIỆU ĐỒNG/THÁNG)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "THÁNG 10/2016", "v": 10, "lbl": "10", "at": [4, "Mười"]}, {"k": "THÁNG 10/2026", "v": 13, "lbl": "13", "at": [4, "mười", 1], "acc": True}]},
    {"type": "slam", "at": 5, "text": "+30%", "sub": "VẬY MÀ CHẬT VẬT HƠN"},
    {"type": "broll", "at": 7, "vid": "11099870", "veil": 0.55, "illus": VM,
     "kin": [{"text": "TIỀN PHÒNG · XĂNG · BỮA TRƯA NGOÀI QUÁN", "at": 7, "sm": True}, {"text": "CUỐI THÁNG KHÔNG CÒN DƯ", "at": 8, "acc": True}]},
    {"type": "question", "at": 10, "text": "Lương tăng mà sao\nlại thấy nghèo đi?"},
    {"type": "kinetic", "at": 11, "items": [{"text": "NGHỊCH LÝ", "at": 11, "acc": True}, {"text": "lương gần như năm nào cũng tăng", "at": 12, "sm": True},
                                           {"text": "vậy mà năm nay khó hơn năm trước", "at": 13, "sm": True}]},
    {"type": "ledger", "at": 14, "title": "THỨ NẰM GIỮA HAI CẢM GIÁC ẤY", "rows": [{"k": "CÓ", "v": "TÊN · SỐ ĐO", "at": [15, "Nó"]}, {"k": "TÍNH BẰNG", "v": "MỘT PHÉP CHIA", "at": [15, "phép"]}],
     "total": {"k": "CUỐI VIDEO", "v": "3 CON SỐ CỦA BẠN · 2036", "at": 16}},
    {"type": "brand", "at": 17, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 18, "items": [{"text": "CHỈ NHẰM GIÁO DỤC", "at": 18, "acc": True}, {"text": "không dự báo giá cả · không phải lời khuyên đầu tư", "at": [18, "không"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CÁI GIỎ HÀNG CỦA CẢ NƯỚC"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CÁI GIỎ HÀNG\nCỦA CẢ NƯỚC", "sub": "CHỈ SỐ GIÁ TIÊU DÙNG (CPI)", "vid": "35878664", "illus": VM, "titleAt": [0, "Thứ"]},
    {"type": "ledger", "at": 2, "title": "CHỈ SỐ GIÁ TIÊU DÙNG", "srcnote": "CỤC THỐNG KÊ", "rows": [{"k": "GIỎ HÀNG", "v": "GẠO · THUÊ NHÀ · XĂNG · …", "at": 3},
                                                                                         {"k": "CHIA THÀNH", "v": "11 NHÓM CHÍNH", "at": 4},
                                                                                         {"k": "MỖI THÁNG", "v": "GHI GIÁ · CÔNG BỐ", "at": 5}],
     "total": {"k": "GIỎ ĐẮT LÊN BAO NHIÊU %", "v": "= LẠM PHÁT", "at": 6}},
    {"type": "question", "at": 7, "text": "Mười năm qua,\ncái giỏ đắt lên bao nhiêu?"},
    {"type": "bars", "at": 8, "title": "LẠM PHÁT BÌNH QUÂN NĂM (%)", "unit": "WORLD BANK WDI · TỪ CỤC THỐNG KÊ",
     "items": [{"k": str(y), "v": Y[str(y)] if str(y) in Y else Y[y], "lbl": f"{(Y[str(y)] if str(y) in Y else Y[y]) + 1e-9:.1f}".replace(".", ","), "at": a, **({"acc": True} if y in (2021, 2024) else {})}
               for y, a in ((2016, 8), (2018, [8, "tới"]), (2020, [8, "bình"]), (2021, 9), (2022, [9, "chỉ"]), (2024, 10), (2025, [10, "khoảng"]))]},
    {"type": "counter", "at": 12, "from": 0, "to": 32, "suffix": "%", "label": "GIỎ HÀNG ĐẮT LÊN · 2016 → 2025", "sub": {"text": "≈ 3,1%/NĂM · CỘNG DỒN 9 NĂM", "at": [12, "cái"]}},
    {"type": "ledger", "at": 13, "title": "NĂM 2026 · CHƯA HẾT", "srcnote": "CỤC THỐNG KÊ · 30/09/2026", "rows": [{"k": "BÌNH QUÂN 9 THÁNG", "v": "+4,52%", "at": 14},
                                                                                                    {"k": "THÁNG 9 SO CÙNG KỲ", "v": "+5,08%", "at": 15}]},
    {"type": "counter", "at": 16, "from": 0, "to": 38, "suffix": "%", "label": "GIỎ HÀNG ĐẮT LÊN · 2016 → 2026", "sub": {"text": "2026 GIẢ ĐỊNH = BÌNH QUÂN 9 THÁNG · KÊNH TỰ TÍNH", "at": [16, "thì"]}},
    {"type": "bars", "at": 17, "title": "MUA ĐÚNG GIỎ CỦA 10 TRIỆU NĂM 2016 (TRIỆU)", "unit": "KÊNH TỰ TÍNH",
     "items": [{"k": "NĂM 2016", "v": 10, "lbl": "10", "at": 17}, {"k": "NĂM 2026 · CẦN", "v": 13.8, "lbl": "≈ 13,8", "at": [18, "năm"], "acc": True},
               {"k": "LƯƠNG ANH TUẤN", "v": 13, "lbl": "13", "at": 19}], "label": {"k": CPI_SRC, "v": "", "at": 17}},
    {"type": "broll", "at": 20, "vid": "3752547", "veil": 0.55, "illus": VM,
     "kin": [{"text": "10 TRIỆU ĐỂ TRONG NGĂN KÉO TỪ 2016", "at": 21, "sm": True}, {"text": "SỨC MUA ≈ 7,25 TRIỆU", "at": [21, "bảy"], "acc": True},
             {"text": "tờ tiền vẫn nguyên · mất hơn một phần tư", "at": 22, "sm": True}]},
    {"type": "question", "at": 23, "text": "Lương 13 triệu của anh Tuấn\nlà tăng hay giảm?"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "TĂNG LƯƠNG BAO NHIÊU MỚI LÀ TĂNG THẬT"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "TĂNG LƯƠNG\nBAO NHIÊU MỚI LÀ THẬT", "sub": "DANH NGHĨA · THỰC", "vid": "5466766", "illus": VM, "titleAt": [0, "Có"]},
    {"type": "myth", "at": 1, "mythLab": "TĂNG DANH NGHĨA", "myth": "GHI TRÊN PHIẾU LƯƠNG", "truthLab": "TĂNG THỰC", "truth": "CẢM THẤY TRONG GIỎ HÀNG", "strikeAt": [2, "Và"], "truthAt": [2, "tăng"]},
    {"type": "kinetic", "at": 4, "items": [{"text": "LƯƠNG MỚI ÷ LƯƠNG CŨ ÷ (1 + LẠM PHÁT)", "at": 4, "acc": True}, {"text": "> 1: khá lên · < 1: nghèo đi", "at": 5, "sm": True}]},
    {"type": "counter", "at": 6, "from": 0, "to": -5.8, "suffix": "%", "label": "SỨC MUA LƯƠNG ANH TUẤN · 2026 SO VỚI 2016", "sub": {"text": "13 ÷ 10 ÷ 1,38 · " + HYPO.split(" · ")[0], "at": 7}},
    {"type": "slam", "at": 8, "text": "+30% LƯƠNG · −6% SỨC MUA", "sub": ""},
    {"type": "kinetic", "at": 9, "items": [{"text": "NGHỊCH LÝ ĐÃ CÓ LỜI GIẢI", "at": 9}, {"text": "13 TRIỆU HÔM NAY ≈ 9,4 TRIỆU GIÁ 2016", "at": 11, "acc": True},
                                          {"text": "thấp hơn tháng lương đầu tiên", "at": 12, "sm": True}]},
    {"type": "ledger", "at": 13, "title": "LƯƠNG 2026 · SỨC MUA SO VỚI 10 TR NĂM 2016", "srcnote": "KÊNH TỰ TÍNH", "rows": [
        {"k": "13 TRIỆU", "v": "≈ −5,8%", "at": [13, "Vậy"]}, {"k": "13,8 TRIỆU", "v": "≈ 0 · ĐỨNG YÊN", "at": 14},
        {"k": "14 TRIỆU", "v": "≈ +1,4%", "at": 15}, {"k": "15 TRIỆU", "v": "≈ +8,7%", "at": 16}]},
    {"type": "ledger", "at": 17, "title": "TĂNG LƯƠNG KHI GIÁ TĂNG ≈ 4,5%", "srcnote": "KÊNH TỰ TÍNH", "rows": [
        {"k": "TĂNG 3%", "v": "≈ −1,45% SỨC MUA", "at": 19}, {"k": "TĂNG 5%", "v": "≈ +0,46%", "at": 20}, {"k": "TĂNG 10%", "v": "≈ +5,2%", "at": 21}]},
    {"type": "bars", "at": 22, "title": "LƯƠNG TỐI THIỂU VÙNG I (TRIỆU/THÁNG)", "unit": "NĐ 122/2015 · NĐ 293/2025",
     "items": [{"k": "2016", "v": 3.5, "lbl": "3,5", "at": 23}, {"k": "2026", "v": 5.31, "lbl": "5,31", "at": 24, "acc": True}]},
    {"type": "kinetic", "at": 25, "items": [{"text": "+52% DANH NGHĨA", "at": 25, "sm": True}, {"text": "≈ +10% SỨC MUA SAU 10 NĂM", "at": [25, "nên"], "acc": True}]},
    {"type": "counter", "at": 26, "from": 9.2, "to": 9.2, "suffix": " TRIỆU", "label": "THU NHẬP BÌNH QUÂN THÁNG · QUÝ III/2026", "sub": {"text": "+9,8% SO CÙNG KỲ · THỰC ≈ +4,5% · CỤC THỐNG KÊ", "at": 27}},
    {"type": "kinetic", "at": 28, "items": [{"text": "BÌNH QUÂN VẪN KHÁ LÊN", "at": 28}, {"text": "NHƯNG BÌNH QUÂN LÀ BÌNH QUÂN", "at": 29, "acc": True},
                                           {"text": "có những năm giá chạy nhanh hơn mọi mức tăng lương", "at": 30, "sm": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "NHỮNG NĂM GIÁ CHẠY NHANH"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "NHỮNG NĂM\nGIÁ CHẠY NHANH", "sub": "2008 · 2011 · ZIMBABWE", "vid": "29576552", "illus": VM, "titleAt": [0, "Năm"]},
    {"type": "counter", "at": 1, "from": 0, "to": 23.1, "suffix": "%", "label": "LẠM PHÁT BÌNH QUÂN NĂM 2008", "sub": {"text": "100 NGHÌN NĂM 2007 → SỨC MUA ≈ 81 NGHÌN", "at": 2}},
    {"type": "bars", "at": 4, "title": "LẠM PHÁT BÌNH QUÂN NĂM (%)", "unit": "WORLD BANK WDI",
     "items": [{"k": "2008", "v": Y["2008"], "lbl": "23,1", "at": [4, "Ba"], "acc": True}, {"k": "2009", "v": Y["2009"], "lbl": "6,7", "at": [4, "năm", 1]},
               {"k": "2010", "v": Y["2010"], "lbl": "9,2", "at": [4, "hai"]}, {"k": "2011", "v": Y["2011"], "lbl": "18,7", "at": [4, "lạm"], "acc": True},
               {"k": "2012", "v": Y["2012"], "lbl": "9,1", "at": 5}]},
    {"type": "slam", "at": 6, "text": "GẤP ĐÔI TRONG 5 NĂM", "sub": "GIỎ HÀNG 2007 → 2012 · ×1,86"},
    {"type": "timeline", "at": 7, "title": "ZIMBABWE", "items": [{"year": "11/2008", "text": "lạm phát mỗi tháng hàng tỷ phần trăm", "at": 8},
                                                             {"year": "01/2009", "text": "tờ 100 nghìn tỷ đô la Zimbabwe", "at": 9},
                                                             {"year": "04/2009", "text": "ngừng in đồng tiền của mình", "at": 11}],
     "label": {"k": "NGUỒN: WIKIPEDIA (HYPERINFLATION IN ZIMBABWE) · DẪN BBC 16/01/2009", "v": "", "at": 7}},
    {"type": "kinetic", "at": 12, "items": [{"text": "TRƯỜNG HỢP CỰC ĐOAN", "at": 12, "sm": True}, {"text": "VIỆT NAM GẦN ĐÂY CÁCH RẤT XA", "at": 13, "acc": True}]},
    {"type": "counter", "at": 14, "from": 0, "to": 4.6, "suffix": " LẦN", "label": "GIÁ CẢ BÌNH QUÂN · 1996 → 2025", "sub": {"text": "100 NGHÌN NĂM 1996 ≈ 460 NGHÌN BÂY GIỜ", "at": 16}},
    {"type": "kinetic", "at": 17, "items": [{"text": "“NGÀY XƯA VÀI CHỤC NGHÌN ĐÃ LÀ NHIỀU”", "at": 17, "sm": True}, {"text": "HỌ NÓI ĐÚNG", "at": 18, "acc": True}]},
    {"type": "myth", "at": 19, "mythLab": "3–4%/NĂM", "myth": "HIỀN", "truthLab": "NHƯNG", "truth": "HIỀN ≠ KHÔNG CÓ", "strikeAt": [20, "Nhưng"], "truthAt": [20, "không"]},
    {"type": "ledger", "at": 22, "title": "QUY TẮC 70 · SỨC MUA CÒN MỘT NỬA SAU…", "srcnote": "70 ÷ LẠM PHÁT (%) ≈ SỐ NĂM", "rows": [
        {"k": "LẠM PHÁT 3%/NĂM", "v": "≈ 23 NĂM", "at": 24}, {"k": "LẠM PHÁT 4,5%/NĂM", "v": "< 16 NĂM", "at": 25}]},
    {"type": "question", "at": 26, "text": "Lạm phát của bạn có phải\nlạm phát của cả nước?"},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "LẠM PHÁT CỦA RIÊNG BẠN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "LẠM PHÁT\nCỦA RIÊNG BẠN", "sub": "MỖI NHÓM HÀNG MỘT TỐC ĐỘ", "vid": "32971516", "illus": VM, "titleAt": [0, "Cái"]},
    {"type": "bars", "at": 2, "title": "THÁNG 9/2026 SO CÙNG KỲ (%)", "unit": NSO9,
     "items": [{"k": "XĂNG DẦU", "v": 23.96, "lbl": "23,96", "at": 4, "acc": True}, {"k": "GIAO THÔNG", "v": 11.67, "lbl": "11,67", "at": 3},
               {"k": "ĂN NGOÀI", "v": 7.4, "lbl": "7,4", "at": [6, "riêng"]}, {"k": "NHÀ Ở·ĐIỆN", "v": 6.47, "lbl": "6,47", "at": 5},
               {"k": "THUÊ NHÀ", "v": 4.88, "lbl": "4,88", "at": [5, "tiền"]}, {"k": "ĂN UỐNG", "v": 4.44, "lbl": "4,44", "at": 6},
               {"k": "Y TẾ", "v": 1.47, "lbl": "1,47", "at": 7}, {"k": "VIỄN THÔNG", "v": 0.33, "lbl": "0,33", "at": [7, "điện"]}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "CÙNG MỘT THÁNG · MỖI NHÓM MỘT TỐC ĐỘ", "at": 8}, {"text": "BẠN TIÊU VÀO ĐÂU, BẠN CẢM THẤY THẾ ẤY", "at": 9, "acc": True}]},
    {"type": "ledger", "at": 10, "title": "GIỎ CỦA ANH TUẤN", "srcnote": "TỶ TRỌNG: VÍ DỤ GIẢ ĐỊNH · MỨC TĂNG: " + NSO9, "rows": [
        {"k": "THUÊ NHÀ · 30%", "v": "+4,88%", "at": [11, "tiền"]}, {"k": "ĂN NGOÀI · 25%", "v": "+7,4%", "at": [11, "ăn"]},
        {"k": "XĂNG · 10%", "v": "+23,96%", "at": [11, "xăng"]}, {"k": "CHỢ, ĐIỆN, KHÁC · 35%", "v": "+0,3 → +5%", "at": [11, "vài"]}],
     "total": {"k": "LẠM PHÁT CỦA ANH", "v": "≈ 6,6%", "at": 12}},
    {"type": "units", "at": 13, "title": "6,65 ĐIỂM % LẠM PHÁT CỦA ANH TUẤN", "total": 20, "cols": 10, "lit": 7, "litAt": [14, "riêng"],
     "unitLabel": "≈ 36% DO XĂNG · CHỈ 10% CHI TIÊU", "label": {"k": "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH", "v": "", "at": 13}},
    {"type": "question", "at": 16, "text": "Có ai thấp hơn không?"},
    {"type": "ledger", "at": 17, "title": "GIỎ CỦA CHỊ MAI", "srcnote": "TỶ TRỌNG: VÍ DỤ GIẢ ĐỊNH · MỨC TĂNG: " + NSO9, "rows": [
        {"k": "THỰC PHẨM · 40%", "v": "+3,89%", "at": [18, "thực"]}, {"k": "HỌC PHÍ CON · 15%", "v": "+2,93%", "at": [18, "học"]},
        {"k": "THUỐC, ĐIỆN, KHÁC · 45%", "v": "+0,3 → +5%", "at": [18, "thuốc"]}], "total": {"k": "LẠM PHÁT CỦA CHỊ", "v": "≈ 2,8%", "at": 19}},
    {"type": "bars", "at": 20, "title": "CÙNG ĐẤT NƯỚC · CÙNG THÁNG 9/2026 (%)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "ANH TUẤN", "v": R["tuan_inflation"], "lbl": "≈ 6,6", "at": [21, "một"], "acc": True}, {"k": "CẢ NƯỚC", "v": 5.08, "lbl": "5,08", "at": [21, "năm"]},
               {"k": "CHỊ MAI", "v": R["mai_inflation"], "lbl": "≈ 2,8", "at": [21, "người"]}]},
    {"type": "kinetic", "at": 22, "items": [{"text": "“CHẮC ĐÂU CHỈ CÓ THẾ”", "at": 22, "sm": True}, {"text": "VỚI HỌ, ĐÚNG LÀ KHÔNG CHỈ CÓ THẾ", "at": 23, "acc": True},
                                           {"text": "và mười năm nữa còn đáng chú ý hơn", "at": 24, "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "NĂM 2036"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "NĂM 2036", "sub": "BA MỨC GIẢ ĐỊNH · KHÔNG PHẢI DỰ BÁO", "vid": "37127207", "illus": VM, "titleAt": [0, "Mười"]},
    {"type": "question", "at": 2, "text": "Năm 2036, bao nhiêu mới bằng\nsức mua 10 triệu năm 2016?"},
    {"type": "kinetic", "at": 3, "items": [{"text": "KHÔNG AI ĐOÁN CHẮC LẠM PHÁT", "at": 3}, {"text": "BA MỨC GIẢ ĐỊNH: 3 · 4 · 5%/NĂM", "at": 5, "acc": True}]},
    {"type": "bars", "at": 6, "title": "CẦN BAO NHIÊU NĂM 2036 (TRIỆU/THÁNG)", "unit": "GIẢ ĐỊNH · KHÔNG PHẢI DỰ BÁO",
     "items": [{"k": "2016", "v": 10, "lbl": "10", "at": [6, "Với"]}, {"k": "2026", "v": 13.8, "lbl": "13,8", "at": [6, "ba"]},
               {"k": "2036 · 3%/NĂM", "v": N36["3%"], "lbl": "≈ 18,5", "at": [6, "mười"]}, {"k": "2036 · 4%/NĂM", "v": N36["4%"], "lbl": "≈ 20,4", "at": [7, "hai"]},
               {"k": "2036 · 5%/NĂM", "v": N36["5%"], "lbl": "≈ 22,5", "at": [8, "hai"], "acc": True}]},
    {"type": "slam", "at": 9, "text": "22,5 TRIỆU · CHỈ ĐỂ ĐỨNG YÊN", "sub": "MUA ĐÚNG GIỎ HÀNG CỦA 10 TRIỆU NĂM 2016"},
    {"type": "question", "at": 11, "text": "Vậy là ai cũng\nsẽ nghèo đi à?"},
    {"type": "kinetic", "at": 12, "items": [{"text": "KHÔNG HẲN", "at": 12, "acc": True}, {"text": "chỉ nghèo đi khi thu nhập tăng chậm hơn giá", "at": 14, "sm": True}]},
    {"type": "bars", "at": 15, "title": "LƯƠNG 13 TRIỆU, TĂNG ĐỀU MỖI NĂM → 2036 (TRIỆU)", "unit": "GIẢ ĐỊNH",
     "items": [{"k": "TĂNG 3%/NĂM", "v": R["salary13_2036"]["3%"], "lbl": "≈ 17,5", "at": 18}, {"k": "CẦN (GIÁ +3%)", "v": N36["3%"], "lbl": "≈ 18,5", "at": 19},
               {"k": "CẦN (GIÁ +5%)", "v": N36["5%"], "lbl": "≈ 22,5", "at": 17}, {"k": "TĂNG 7%/NĂM", "v": R["salary13_2036"]["7%"], "lbl": "≈ 25,6", "at": 16, "acc": True}]},
    {"type": "broll", "at": 20, "vid": "7710771", "veil": 0.55, "illus": VM,
     "kin": [{"text": "TIỀN TRONG NGĂN KÉO · CHẮC CHẮN THUA", "at": 21, "sm": True}, {"text": "LÃI THỰC = LÃI − MỨC TĂNG GIÁ", "at": 22, "acc": True}]},
    {"type": "myth", "at": 24, "mythLab": "KHÔNG PHẢI", "myth": "LẠM PHÁT NĂM NAY BAO NHIÊU?", "truthLab": "MÀ LÀ", "truth": "LƯƠNG VÀ TIỀN ĐỂ DÀNH CÓ NHANH HƠN LẠM PHÁT CỦA TÔI?",
     "strikeAt": [25, "Mà"], "truthAt": [25, "lương"]},
    {"type": "kinetic", "at": 26, "items": [{"text": "TỰ TRẢ LỜI BẰNG BA CON SỐ", "at": 26, "acc": True, "fx": "marker"}]},
]}

CH["ch06"] = {"hud": {"k": "PHẦN CUỐI", "t": "BA CON SỐ CỦA RIÊNG BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "BA CON SỐ\nCỦA RIÊNG BẠN", "sub": "VÀ KHI NÀO PHÉP TÍNH KHÔNG ĐÚNG", "vid": "5466772", "illus": VM, "titleAt": [0, "Con"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "1 · TĂNG THỰC CỦA LƯƠNG", "at": 1, "acc": True}, {"text": "lương tháng này ÷ cùng tháng năm ngoái ÷ (1 + lạm phát)", "at": 2, "sm": True}]},
    {"type": "ledger", "at": 3, "title": "VÍ DỤ: ANH TUẤN", "srcnote": "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH", "rows": [{"k": "NĂM NGOÁI → NĂM NAY", "v": "12,5 → 13 TRIỆU", "at": 3},
                                                                                                 {"k": "13 ÷ 12,5", "v": "1,04 · +4%", "at": 4}, {"k": "÷ 1,045", "v": "< 1", "at": 5}],
     "total": {"k": "SỨC MUA", "v": "≈ −0,5%", "at": 6}},
    {"type": "kinetic", "at": 9, "items": [{"text": "2 · LẠM PHÁT CỦA RIÊNG BẠN", "at": 9, "acc": True}, {"text": "3 khoản chi lớn nhất · tỷ trọng · mức tăng giá", "at": 10, "sm": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "3 · CON SỐ NĂM 2036", "at": 13, "acc": True}, {"text": "chi tiêu hôm nay × (1 + lạm phát)^10", "at": 14, "sm": True},
                                           {"text": "3% → × 1,34 · 5% → × 1,63", "at": 15}]},
    {"type": "ledger", "at": 16, "title": "KHI NÀO PHÉP TÍNH KHÔNG ĐÚNG", "rows": [{"k": "1", "v": "CPI LÀ BÌNH QUÂN · 2026 MỚI 9 THÁNG", "at": 17},
                                                                               {"k": "2", "v": "TỶ TRỌNG GIỎ LÀ GIẢ ĐỊNH", "at": 18}, {"k": "3", "v": "3–5% LÀ GIẢ ĐỊNH, KHÔNG DỰ BÁO", "at": 19}]},
    {"type": "bars", "at": 20, "title": "HAI TỜ GIẤY CỦA ANH TUẤN (TRIỆU ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "PHONG BÌ 2016", "v": 10, "lbl": "10", "at": 21}, {"k": "PHIẾU LƯƠNG 2026", "v": 13, "lbl": "13", "at": 22},
               {"k": "2026 · THEO GIÁ 2016", "v": 9.42, "lbl": "≈ 9,4", "at": 23, "acc": True}]},
    {"type": "broll", "at": 24, "vid": "5909917", "veil": 0.55, "illus": VM,
     "kin": [{"text": "LẠM PHÁT KHÔNG LẤY TIỀN KHỎI TÚI BẠN", "at": 24, "sm": True}, {"text": "NÓ LÀM MỖI TỜ TIỀN NHẸ ĐI", "at": 25, "acc": True}]},
    {"type": "question", "at": 26, "text": "Năm nay khoản chi nào\ncủa nhà bạn tăng nhanh nhất?"},
    {"type": "kinetic", "at": 27, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 27}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [27, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
TITLES = ["Lương 10 Triệu Năm 2016 Bằng Bao Nhiêu Tiền Hôm Nay?",
          "Lương Tăng Từ 10 Lên 13 Triệu Mà Vẫn Nghèo Đi? Phép Tính Lạm Phát 2016–2026",
          "Lạm Phát 4,5% Nhưng Của Bạn Có Thể Là 6,6%: Cách Tự Tính Lạm Phát Của Riêng Mình"]
FORMULA = ("📐 CÁCH TÍNH (kênh tự tính · thay bằng số của bạn)\n• Sức mua thực = (lương mới ÷ lương cũ) ÷ (1 + lạm phát) − 1\n"
           "• 10 triệu năm 2016 = 10 × CPI 2026 ÷ CPI 2016 ≈ 13,8 triệu (CPI bình quân năm, World Bank WDI từ số liệu Cục Thống kê; 2026 tạm dùng +4,52% "
           "bình quân 9 tháng)\n• Lạm phát của riêng bạn = Σ (tỷ trọng khoản chi × mức tăng giá của khoản đó)\n"
           "• Năm 2036 = chi tiêu hôm nay × (1 + lạm phát)^10; 3%/4%/5% là giả định, không phải dự báo")
SPEC = {
    "title": TITLES[0],
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["lạm", "phát", "lương", "giá", "triệu", "giỏ", "thực"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": TITLES,
        "summary": "Tháng 10/2016 anh Tuấn (ví dụ giả định) nhận lương 10 triệu; tháng 10/2026 phiếu lương ghi 13 triệu, tăng 30%, vậy mà anh thấy chật "
                   "vật hơn. Video đo nghịch lý ấy bằng chỉ số giá tiêu dùng: 10 triệu năm 2016 cần khoảng 13,8 triệu hôm nay, tăng lương bao nhiêu mới là "
                   "tăng thật, những năm giá chạy nhanh (2008, 2011, Zimbabwe), vì sao lạm phát của riêng bạn có thể là 6,6% hay 2,8% khi cả nước là 5,08%, "
                   "và con số năm 2036 với ba mức giả định. Cuối video: ba con số để bạn tự tính cho mình.",
        "more": ["Nội dung giáo dục, không phải tư vấn đầu tư. Kênh không dự báo lạm phát và không khuyến nghị mua, gửi hay đầu tư vào tài sản nào. "
                 "Anh Tuấn, chị Mai, mức lương và tỷ trọng giỏ chi tiêu là ví dụ giả định do kênh tự tính; mức lạm phát 2027–2036 (3%, 4%, 5%) là giả "
                 "định để so sánh. Số liệu là quá khứ, tính tới thời điểm làm video (10/2026). Nội dung do kênh biên soạn từ nguồn công khai; giọng đọc "
                 "tổng hợp.", FORMULA],
        "chapter_titles": {"ch00": "Mở đầu: phong bì mười triệu", "ch01": "Cái giỏ hàng của cả nước: 10 triệu năm 2016 bằng bao nhiêu hôm nay",
                           "ch02": "Tăng lương bao nhiêu mới là tăng thật", "ch03": "Những năm giá chạy nhanh: 2008, 2011, Zimbabwe",
                           "ch04": "Lạm phát của riêng bạn", "ch05": "Năm 2036: ba mức giả định", "ch06": "Ba con số của riêng bạn"},
        "sources": [
            "Cục Thống kê 30/09/2026 — Tổng quan thị trường giá cả tháng 9, quý III và 9 tháng năm 2026: https://www.nso.gov.vn/wp-content/uploads/2026/10/Tong-quan-CPI-chi-so-gia-vang-do-la-My-thang-9-QIII-va-9-thang-nam-2026.pdf",
            "Cục Thống kê — Thông cáo báo chí lao động việc làm quý III/2026: https://www.nso.gov.vn/wp-content/uploads/2026/10/Thong-cao-bao-chi-ve-tinh-hinh-lao-dong-viec-lam-QIII-nam-2026.pdf",
            "World Bank WDI — Inflation, consumer prices (annual %), Viet Nam: https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=VN",
            "World Bank WDI — Consumer price index (2010 = 100), Viet Nam: https://data.worldbank.org/indicator/FP.CPI.TOTL?locations=VN",
            "Cục Thống kê — Thông cáo báo chí tình hình giá tháng 12, quý IV và năm 2025 (CPI bình quân 2025 +3,31%): https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2026/01/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-muoi-hai-quy-iv-va-nam-2025/",
            "Cổng TTĐT Chính phủ — Nghị định 122/2015/NĐ-CP, lương tối thiểu vùng 2016: https://vanban.chinhphu.vn/default.aspx?pageid=27160&docid=182151",
            "Cổng TTĐT Chính phủ — Nghị định 293/2025/NĐ-CP, lương tối thiểu vùng từ 01/01/2026: https://xaydungchinhsach.chinhphu.vn/nghi-dinh-so-293-2025-nd-cp-quy-dinh-muc-luong-toi-thieu-doi-voi-nguoi-lao-dong-lam-viec-theo-hop-dong-lao-dong-119251110172808433.htm",
            "LuatVietnam 01/02/2026 — Lương tối thiểu vùng 2026 (Nghị định 293/2025/NĐ-CP): https://luatvietnam.vn/bao-hiem/tu-2026-muc-dong-bhxh-bhyt-bhtn-cua-nld-va-nsdld-duoc-tinh-nhu-the-nao-563-106906-article.html",
            "Wikipedia — Hyperinflation in Zimbabwe: https://en.wikipedia.org/wiki/Hyperinflation_in_Zimbabwe"],
        "hashtags": ["LạmPhát", "TiềnLương", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["lạm phát", "lạm phát là gì", "lạm phát việt nam", "lương 10 triệu", "lương thực tế", "chỉ số giá tiêu dùng", "CPI 2026", "lạm phát 2026",
                 "sức mua", "lạm phát ở zimbabwe", "tài chính cá nhân", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: chỉ số giá tiêu dùng bình quân năm theo World Bank WDI (từ số liệu Cục Thống kê); CPI tháng 9/2026 và thu nhập quý III/2026 "
                       "theo Cục Thống kê; phép tính và các ví dụ do kênh tự lập.",
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
