"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK B5/E6 "Rút BHXH một lần được bao nhiêu? 200 triệu hay lương hưu".

    python motion/long/script_lines.py ck-e6-luong-huu-rut-mot-lan      # lines + title từ script.md
    python data/long/ck-e6-luong-huu-rut-mot-lan/gen_scenes.py         # scenes/hud/bgm + spec.json (giữ nguyên lines)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (kiểm độc lập check.py). Kiểm chứng + URL: factcheck.md.
Luật kênh: chỉ giáo dục, KHÔNG "nên rút / không nên rút"; chị Hạnh, lương đóng 10 tr, lãi thực 0–3% = VÍ DỤ GIẢ ĐỊNH; mọi số tiền quy về giá hôm nay.
Mô-típ: một đường thẳng 25 năm (2026 → 2051) với ba ngã rẽ — timeline ở CH00, CH03, CH06 + b-roll con đường.
B-roll: id Pexels từ kho đã soát của các Long CK trước — trước khi dựng: `pexels.py get` + `clip_sheet.py ck-e6-luong-huu-rut-mot-lan`
(cân nhắc thay vài clip để không lặp diện mạo, variety.py audit).
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN, VIOLET = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444", "#a78bfa"
HYPO = "VÍ DỤ GIẢ ĐỊNH · CHỊ HẠNH · LƯƠNG ĐÓNG 10 TRIỆU · GIÁ HÔM NAY"
LAW = "LUẬT BHXH 2024 (41/2024/QH15) · HIỆU LỰC 01/07/2025"
VM = "VIDEO MINH HỌA"
F = R["female"]
G = R["lump_grow_2051"]
assert R["lump_now"] == 200 and F["15"]["pension"] == 4.5 and G["2%"] == 328 and round(R["lump_2pct_as_4_5_months"]) == 78
ROAD = [{"year": "2026", "text": "nghỉ việc · 10 năm đóng"}, {"year": "2027", "text": "ngã rẽ 1: rút một lần"},
        {"year": "2031", "text": "ngã rẽ 2: đủ 15 năm"}, {"year": "2051", "text": "ngã rẽ 3: 60 tuổi · lương hưu"}]
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI TRĂM TRIỆU TRƯỚC MẶT"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "6466354", "veil": 0.55, "illus": VM,
     "kin": [{"text": "THÁNG 6/2026 · NGHỈ VIỆC SAU 10 NĂM", "at": [0, "Tháng"], "sm": True}, {"text": "CHỊ HẠNH · 35 TUỔI", "at": [1, "Chị"], "acc": True},
             {"text": "nhân vật ví dụ giả định", "at": [1, "một"], "sm": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "MỘT CÂU RẤT NHIỀU NGƯỜI TỪNG NGHE", "at": 3, "sm": True},
                                          {"text": "“NGHỈ RỒI THÌ RÚT BẢO HIỂM ĐI”", "at": 4, "acc": True}]},
    {"type": "counter", "at": 5, "from": 0, "to": 200, "suffix": " TRIỆU", "label": "RÚT BHXH MỘT LẦN · 10 NĂM · LƯƠNG ĐÓNG 10 TRIỆU", "sub": {"text": "= 20 THÁNG LƯƠNG · " + HYPO.split(" · ")[0], "at": 7}},
    {"type": "ledger", "at": 8, "title": "HAI TRĂM TRIỆU ĐỦ ĐỂ…", "rows": [{"k": "1", "v": "TRẢ MỘT KHOẢN NỢ", "at": [8, "trả"]}, {"k": "2", "v": "SỬA LẠI CĂN BẾP", "at": [8, "sửa"]},
                                                                        {"k": "3", "v": "GỬI VỀ QUÊ CHO BỐ MẸ", "at": [8, "gửi"]}]},
    {"type": "slam", "at": 9, "text": "Ở NGAY TRƯỚC MẶT", "sub": ""},
    {"type": "bars", "at": 11, "title": "NGƯỜI HƯỞNG BHXH MỘT LẦN · 2016–2022 (TRIỆU LƯỢT)", "unit": "BỘ LĐ-TB&XH",
     "items": [{"k": "NHẬN MỘT LẦN", "v": 4.8, "lbl": "> 4,8", "at": [11, "hơn"], "acc": True}, {"k": "HỒ SƠ ĐÓNG DƯỚI 10 NĂM", "v": 4.34, "lbl": "≈ 90%", "at": 12}],
     "label": {"k": "QUA VNECONOMY 03/07/2023", "v": "", "at": 11}},
    {"type": "question", "at": 13, "text": "200 triệu bây giờ,\nhay lương hưu 25 năm nữa?"},
    {"type": "kinetic", "at": 14, "items": [{"text": "CÂU HỎI CỦA VIDEO NÀY", "at": 14}, {"text": "KHÔNG CÓ MỘT ĐÁP ÁN CHO MỌI NGƯỜI", "at": 15, "acc": True}]},
    {"type": "timeline", "at": 16, "title": "MỘT ĐƯỜNG THẲNG 25 NĂM · BA NGÃ RẼ", "items": [dict(x, at=a) for x, a in zip(ROAD, [16, [16, "từ"], 17, [17, "mỗi"]])]},
    {"type": "brand", "at": 18, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 19, "items": [{"text": "CHỈ NHẰM GIÁO DỤC", "at": 19, "acc": True},
                                           {"text": "không phải lời khuyên rút hay không rút · mọi số tiền quy về giá hôm nay", "at": [19, "không"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "NGÃ RẼ 1", "t": "HAI TRĂM TRIỆU ĐẾN TỪ ĐÂU"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "NGÃ RẼ MỘT", "title": "HAI TRĂM TRIỆU\nĐẾN TỪ ĐÂU", "sub": "RÚT BẢO HIỂM XÃ HỘI MỘT LẦN", "vid": "7490451", "illus": VM, "titleAt": [0, "Ngã"]},
    {"type": "ledger", "at": 2, "title": "MỨC HƯỞNG BHXH MỘT LẦN", "srcnote": LAW, "rows": [{"k": "MỖI NĂM TỪ 2014", "v": "2 THÁNG LƯƠNG BÌNH QUÂN", "at": 3},
                                                                                       {"k": "MỖI NĂM TRƯỚC 2014", "v": "1,5 THÁNG", "at": 4}],
     "total": {"k": "LƯƠNG BÌNH QUÂN", "v": "ĐIỀU CHỈNH TRƯỢT GIÁ", "at": 5}},
    {"type": "ledger", "at": 7, "title": "CHỊ HẠNH", "srcnote": HYPO, "rows": [{"k": "ĐÓNG TỪ", "v": "2016 · 10 NĂM", "at": 7}, {"k": "10 × 2 THÁNG", "v": "20 THÁNG LƯƠNG", "at": 8}],
     "total": {"k": "20 × 10 TRIỆU", "v": "200 TRIỆU", "at": 9}},
    {"type": "bars", "at": 10, "title": "10 NĂM CỦA CHỊ HẠNH (TRIỆU ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "PHẦN CHỊ TỰ ĐÓNG (8%)", "v": R["own_contrib_10y"], "lbl": "≈ 96", "at": [11, "khoảng"]}, {"k": "RÚT MỘT LẦN", "v": 200, "lbl": "200", "at": 12, "acc": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "CÔNG TY CŨNG ĐÓNG VÀO QUỸ", "at": 13, "sm": True}, {"text": "KHÔNG PHẢI ‘LẤY LẠI ĐÚNG TIỀN MÌNH’", "at": 14, "acc": True},
                                           {"text": "một khoản quy đổi theo công thức luật định", "at": 15, "sm": True}]},
    {"type": "question", "at": 16, "text": "Nghỉ việc là\nrút được ngay à?"},
    {"type": "ledger", "at": 18, "title": "ĐIỀU KIỆN (ĐÓNG TRƯỚC 01/07/2025)", "srcnote": "LUẬT BHXH 2024 · ĐIỀU 70 (QUA LUATVIETNAM)",
     "rows": [{"k": "NGHỈ ĐỦ", "v": "12 THÁNG", "at": [18, "mười"]}, {"k": "KHÔNG ĐÓNG", "v": "BẮT BUỘC LẪN TỰ NGUYỆN", "at": 19},
              {"k": "TỔNG THỜI GIAN", "v": "CHƯA ĐỦ 20 NĂM", "at": [19, "tổng"]}]},
    {"type": "date", "at": 20, "day": "GIỮA NĂM", "date": "2027", "sub": {"text": "SỚM NHẤT CHỊ HẠNH CÓ THỂ NHẬN", "at": 20}},
    {"type": "kinetic", "at": 21, "items": [{"text": "ĐÓNG TỪ 01/07/2025 TRỞ ĐI", "at": 21, "sm": True}, {"text": "GẦN NHƯ KHÔNG CÒN ĐƯỜNG RÚT MỘT LẦN", "at": [21, "gần"], "acc": True},
                                           {"text": "trừ vài trường hợp: định cư nước ngoài, bệnh nặng…", "at": 22, "sm": True}]},
    {"type": "myth", "at": 24, "mythLab": "ĐÃ RÚT MỘT LẦN", "myth": "10 NĂM ĐÃ THANH TOÁN XONG", "truthLab": "CHƯA RÚT", "truth": "10 NĂM ĐƯỢC BẢO LƯU · CỘNG NỐI",
     "strikeAt": [25, "Nếu"], "truthAt": [26, "Đổi"]},
    {"type": "kinetic", "at": 27, "items": [{"text": "KHÔNG MẤT ĐI ĐÂU", "at": 27}, {"text": "LUẬT MỚI LÀM 10 NĂM ẤY ĐÁNG GIÁ HƠN", "at": 28, "acc": True}]},
]}

CH["ch02"] = {"hud": {"k": "NGÃ RẼ 2", "t": "MƯỜI LĂM NĂM"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "NGÃ RẼ HAI", "title": "MƯỜI LĂM NĂM", "sub": "ĐIỀU KIỆN LƯƠNG HƯU MỚI", "vid": "1793371", "illus": VM, "titleAt": [0, "Ngã"]},
    {"type": "bars", "at": 1, "title": "SỐ NĂM ĐÓNG TỐI THIỂU ĐỂ CÓ LƯƠNG HƯU", "unit": LAW.split(" · ")[0],
     "items": [{"k": "TRƯỚC 07/2025", "v": 20, "lbl": "20 NĂM", "at": [1, "phải"]}, {"k": "TỪ 07/2025", "v": 15, "lbl": "15 NĂM", "at": 2, "acc": True}]},
    {"type": "ledger", "at": 3, "title": "CHỊ HẠNH ĐÃ ĐÓNG 10 NĂM", "srcnote": HYPO, "rows": [{"k": "LUẬT CŨ", "v": "CẦN THÊM 10 NĂM", "at": 4}, {"k": "LUẬT MỚI", "v": "CẦN THÊM 5 NĂM", "at": 5}]},
    {"type": "question", "at": 6, "text": "Đủ 15 năm thì lương hưu\nđược bao nhiêu?"},
    {"type": "ledger", "at": 7, "title": "TỶ LỆ HƯỞNG LƯƠNG HƯU", "srcnote": "PLO 01/12/2024 · LUẬT BHXH 2024", "rows": [
        {"k": "NỮ · 15 NĂM", "v": "45% · +2%/NĂM", "at": 7}, {"k": "NỮ · TỐI ĐA", "v": "75% Ở 30 NĂM", "at": 9},
        {"k": "NAM · 15 NĂM", "v": "40% · +1%/NĂM TỚI 20", "at": 11}, {"k": "NAM · TỐI ĐA", "v": "75% Ở 35 NĂM", "at": [12, "ba"]}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "NẾU LÀ NAM · CÙNG 15 NĂM, 10 TRIỆU", "at": 13, "sm": True}, {"text": "≈ 4 TRIỆU/THÁNG", "at": [13, "lương"], "acc": True},
                                           {"text": "ít hơn 500 nghìn mỗi tháng", "at": 14, "sm": True}]},
    {"type": "bars", "at": 15, "title": "LƯƠNG HƯU CỦA CHỊ HẠNH (TRIỆU/THÁNG)", "unit": "GIÁ HÔM NAY · VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "15 NĂM · ĐỦ NĂM 2031", "v": F["15"]["pension"], "lbl": "4,5", "at": 16, "acc": True}, {"k": "20 NĂM", "v": F["20"]["pension"], "lbl": "5,5", "at": 17},
               {"k": "25 NĂM", "v": F["25"]["pension"], "lbl": "6,5", "at": 18}, {"k": "30 NĂM · MỨC TRẦN", "v": F["30"]["pension"], "lbl": "7,5", "at": 19}]},
    {"type": "ledger", "at": 20, "title": "GIÁ CỦA 5 NĂM ĐÓNG THÊM", "srcnote": HYPO, "rows": [
        {"k": "ĐI LÀM · PHẦN TỰ ĐÓNG 8%", "v": "≈ 48 TRIỆU", "at": 21}, {"k": "TỰ NGUYỆN · 22%", "v": "≈ 132 TRIỆU", "at": 22}],
     "total": {"k": "TỰ NGUYỆN", "v": "TRƯỚC HỖ TRỢ CỦA NN", "at": 23}},
    {"type": "myth", "at": 24, "mythLab": "MỘT BÊN", "myth": "200 TRIỆU CẦM NGAY", "truthLab": "BÊN KIA", "truth": "4,5 TRIỆU/THÁNG · CHƯA PHẢI BÂY GIỜ",
     "strikeAt": [25, "Bên"], "truthAt": [25, "bốn"]},
    {"type": "question", "at": 26, "text": "Chính xác thì\nbao giờ?"},
]}

CH["ch03"] = {"hud": {"k": "NGÃ RẼ 3", "t": "HAI MƯƠI LĂM NĂM CHỜ"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "NGÃ RẼ BA", "title": "HAI MƯƠI LĂM\nNĂM CHỜ", "sub": "TUỔI NGHỈ HƯU · 2026 → 2051", "vid": "35830059", "illus": VM, "titleAt": [0, "Ngã"]},
    {"type": "ledger", "at": 2, "title": "TUỔI NGHỈ HƯU (ĐIỀU KIỆN BÌNH THƯỜNG)", "srcnote": "NGHỊ ĐỊNH 135/2020/NĐ-CP · ĐIỀU 4", "rows": [
        {"k": "NỮ · 2026", "v": "57 TUỔI · +4 THÁNG/NĂM", "at": 2}, {"k": "NỮ · TỪ 2035", "v": "60 TUỔI", "at": 3},
        {"k": "NAM · 2026", "v": "61 TUỔI 6 THÁNG", "at": [2, "lao", 1]}, {"k": "NAM · TỪ 2028", "v": "62 TUỔI", "at": 4}]},
    {"type": "timeline", "at": 5, "title": "CON ĐƯỜNG CỦA CHỊ HẠNH", "items": [{"year": "1991", "text": "sinh", "at": 5}, {"year": "2026", "text": "35 tuổi · nghỉ việc", "at": 6},
                                                                         {"year": "2051", "text": "60 tuổi · lương hưu", "at": 7}]},
    {"type": "slam", "at": 8, "text": "25 NĂM NỮA", "sub": "DÀI HƠN CẢ QUÃNG ĐÃ ĐI LÀM"},
    {"type": "question", "at": 10, "text": "Bao lâu mới nhận lại\nđủ 200 triệu?"},
    {"type": "bars", "at": 11, "title": "SỐ THÁNG LƯƠNG HƯU ĐỂ BẰNG 200 TRIỆU", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "15 NĂM · 4,5 TR", "v": F["15"]["months_to_match_lump"], "lbl": "≈ 44 · TỚI ≈ 63 TUỔI 8 THÁNG", "at": 11, "acc": True},
               {"k": "30 NĂM · 7,5 TR", "v": F["30"]["months_to_match_lump"], "lbl": "≈ 27 · TỚI ≈ 62 TUỔI", "at": 13}]},
    {"type": "ledger", "at": 15, "title": "SAU MỐC ẤY", "rows": [{"k": "MỖI THÁNG", "v": "LÀ PHẦN NHẬN THÊM", "at": 15}, {"k": "TRẢ", "v": "HẰNG THÁNG · TỚI HẾT ĐỜI", "at": 16},
                                                              {"k": "KÈM", "v": "THẺ BẢO HIỂM Y TẾ", "at": 17}]},
    {"type": "counter", "at": 19, "from": 77.3, "to": 77.3, "suffix": " TUỔI", "label": "TUỔI THỌ TRUNG BÌNH LÚC SINH · PHỤ NỮ VN 2024", "sub": {"text": "CỤC THỐNG KÊ · NGƯỜI ĐÃ 60 TUỔI THƯỜNG SỐNG LÂU HƠN", "at": 20}},
    {"type": "bars", "at": 21, "title": "TỚI 77 TUỔI (TRIỆU ĐỒNG · GIÁ HÔM NAY)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "RÚT MỘT LẦN", "v": 200, "lbl": "200", "at": [22, "so"]}, {"k": "17 NĂM LƯƠNG HƯU 4,5 TR", "v": F["15"]["sum_to_77"], "lbl": "≈ 934", "at": 21, "acc": True}]},
    {"type": "kinetic", "at": 23, "items": [{"text": "SO NHƯ VẬY CHƯA CÔNG BẰNG", "at": 23}, {"text": "200 TRIỆU CŨNG CÓ THỂ LỚN LÊN", "at": 24, "acc": True}]},
    {"type": "question", "at": 25, "text": "Lớn tới đâu?"},
]}

CH["ch04"] = {"hud": {"k": "PHÉP THỬ", "t": "NẾU 200 TRIỆU ĐƯỢC ĐEM ĐI GỬI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "PHÉP THỬ", "title": "NẾU 200 TRIỆU\nĐƯỢC ĐEM ĐI GỬI", "sub": "LÃI THỰC · 25 NĂM", "vid": "12033695", "illus": VM, "titleAt": [0, "Giả"]},
    {"type": "myth", "at": 2, "mythLab": "KHÔNG PHẢI", "myth": "LÃI GHI TRÊN SỔ", "truthLab": "MÀ LÀ", "truth": "LÃI THỰC = SAU KHI TRỪ GIÁ CẢ TĂNG", "strikeAt": [2, "mà"], "truthAt": 3},
    {"type": "bars", "at": 5, "title": "200 TRIỆU SAU 25 NĂM · GIÁ HÔM NAY (TRIỆU)", "unit": "LÃI THỰC GIẢ ĐỊNH",
     "items": [{"k": "LÃI THỰC 0%", "v": G["0%"], "lbl": "200", "at": 5}, {"k": "1%/NĂM", "v": G["1%"], "lbl": "≈ 256", "at": 6},
               {"k": "2%/NĂM", "v": G["2%"], "lbl": "≈ 328", "at": 7, "acc": True}, {"k": "3%/NĂM", "v": G["3%"], "lbl": "≈ 419", "at": 8},
               {"k": "−1%/NĂM", "v": G["-1%"], "lbl": "≈ 156", "at": 10}]},
    {"type": "slam", "at": 11, "text": "NHỎ ĐI GẦN 1/4", "sub": "KHI LÃI THỰC ÂM 1%/NĂM"},
    {"type": "question", "at": 12, "text": "Lãi thực 2–3%\ncó dễ không?"},
    {"type": "kinetic", "at": 13, "items": [{"text": "KHÔNG DỄ · KHÔNG CHẮC CHẮN", "at": 13, "acc": True}, {"text": "mức giả định để so sánh · không phải lời hứa của kênh nào", "at": 14, "sm": True}]},
    {"type": "ledger", "at": 15, "title": "328 TRIỆU Ở TUỔI 60 · RÚT 4,5 TRIỆU/THÁNG", "srcnote": "LÃI THỰC 2% · VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH",
     "rows": [{"k": "ĐỦ TRẢ", "v": "≈ 78 THÁNG", "at": 17}, {"k": "TỨC", "v": "≈ 6,5 NĂM · TỚI ≈ 66,5 TUỔI", "at": 18}], "total": {"k": "SAU ĐÓ", "v": "SỔ VỀ KHÔNG", "at": 19}},
    {"type": "kinetic", "at": 20, "items": [{"text": "LƯƠNG HƯU VẪN TIẾP TỤC", "at": 20, "acc": True}, {"text": "mỗi tháng · tới hết đời", "at": [20, "mỗi"], "sm": True}]},
    {"type": "broll", "at": 21, "vid": "8970851", "veil": 0.55, "illus": VM,
     "kin": [{"text": "KHÁC BIỆT BẢNG TÍNH HAY BỎ QUA", "at": 21, "sm": True}, {"text": "MÌNH SẼ SỐNG BAO LÂU?", "at": [23, "mình"], "acc": True}]},
    {"type": "myth", "at": 24, "mythLab": "LƯƠNG HƯU", "myth": "SỐNG TỚI 70 HAY 90 · CÙNG MỘT MỨC", "truthLab": "MỘT CUỐN SỔ", "truth": "CHỈ ĐỦ TỚI NGÀY NÓ CẠN",
     "strikeAt": [25, "Còn"], "truthAt": [25, "chỉ"]},
    {"type": "kinetic", "at": 26, "items": [{"text": "KHÔNG CÓ NGHĨA RÚT MỘT LẦN LUÔN SAI", "at": 26, "acc": True}, {"text": "có lúc 200 triệu là nhu cầu thật", "at": 27, "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "KHI 200 TRIỆU LÀ NHU CẦU THẬT"}, "bgm": {"mood": "mystery", "gain": 0.09}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "KHI 200 TRIỆU\nLÀ NHU CẦU THẬT", "sub": "CÔNG BẰNG VỚI NGƯỜI ĐÃ RÚT", "vid": "3192916", "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "ledger", "at": 2, "title": "KHÔNG PHẢI AI CŨNG TÍNH SAI", "rows": [{"k": "1", "v": "CHỮA BỆNH CHO MÌNH, CHO CON", "at": 2},
                                                                              {"k": "2", "v": "MỘT KHOẢN NỢ LÃI RẤT CAO", "at": 3},
                                                                              {"k": "3", "v": "KHÔNG QUAY LẠI LÀM CÓ HỢP ĐỒNG", "at": 4}]},
    {"type": "bars", "at": 5, "title": "NỢ 200 TRIỆU · LÃI 30%/NĂM (TRIỆU)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "TIỀN LÃI MỘT NĂM", "v": 60, "lbl": "≈ 60", "at": 6, "acc": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "BÀI TOÁN CỦA MỖI NGƯỜI KHÔNG GIỐNG NHAU", "at": 7, "acc": True}]},
    {"type": "bars", "at": 8, "title": "NGƯỜI NHẬN MỘT LẦN 2016–2022 (%)", "unit": "BỘ LĐ-TB&XH · QUA VNECONOMY",
     "items": [{"k": "20 – 40 TUỔI", "v": 77.5, "lbl": "≈ 77,5", "at": 9}, {"k": "ĐÓNG DƯỚI 5 NĂM", "v": 66.6, "lbl": "66,6", "at": 10, "acc": True}]},
    {"type": "counter", "at": 11, "from": 0, "to": 1.3, "suffix": " TRIỆU NGƯỜI", "label": "QUAY LẠI ĐÓNG BHXH SAU KHI RÚT · 2016–2022", "sub": {"text": "ĐỒNG HỒ NĂM ĐÓNG BẮT ĐẦU TỪ SỐ KHÔNG", "at": 12}},
    {"type": "myth", "at": 13, "mythLab": "25 TUỔI", "myth": "CÒN KỊP ĐẾM LẠI", "truthLab": "45 TUỔI", "truth": "ĐẾM LẠI 15 NĂM LÀ CHUYỆN KHÁC", "strikeAt": [14, "Với"], "truthAt": [14, "đếm"]},
    {"type": "question", "at": 15, "text": "Tới 60 mà chưa đủ\n15 năm thì sao?"},
    {"type": "ledger", "at": 16, "title": "LUẬT MỚI MỞ THÊM VÀI LỐI", "srcnote": "LUẬT BHXH 41/2024/QH15 · ĐIỀU 21, 23, 33, 70", "rows": [
        {"k": "ĐỦ TUỔI", "v": "MỘT LẦN HOẶC TRỢ CẤP THÁNG", "at": 17}, {"k": "ĐÓNG TIẾP", "v": "KỂ CẢ TỰ NGUYỆN, CHO ĐỦ 15", "at": 18},
        {"k": "TỪ 75 TUỔI", "v": "TRỢ CẤP HƯU TRÍ XÃ HỘI", "at": 19}]},
    {"type": "counter", "at": 20, "from": 500, "to": 540, "suffix": " NGHÌN/THÁNG", "label": "TRỢ CẤP HƯU TRÍ XÃ HỘI · TỪ 05/10/2026 (NĐ 335/2026)", "sub": {"text": "LƯỚI ĐỠ CUỐI CÙNG · KHÔNG PHẢI LƯƠNG HƯU", "at": 21}},
    {"type": "slam", "at": 22, "text": "KHÔNG PHẢI RÚT HAY KHÔNG RÚT", "sub": "200 TRIỆU SẼ LÀM GÌ · MÌNH ĐÁNH ĐỔI GÌ"},
]}

CH["ch06"] = {"hud": {"k": "PHẦN CUỐI", "t": "BA NGÃ RẼ CỦA CHỊ HẠNH"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "BA NGÃ RẼ\nCỦA CHỊ HẠNH", "sub": "VÀ KHI NÀO PHÉP TÍNH KHÔNG ĐÚNG", "vid": "8865613", "illus": VM, "titleAt": [0, "Quay"]},
    {"type": "timeline", "at": 1, "title": "BA NGÃ RẼ · GIÁ HÔM NAY · VÍ DỤ GIẢ ĐỊNH", "items": [
        {"year": "2027", "text": "rút ≈ 200 triệu · 10 năm khép lại", "at": 1}, {"year": "2031 → 2051", "text": "đóng thêm 5 năm · ≈ 4,5 triệu/tháng từ 60 tuổi", "at": 2},
        {"year": "2051", "text": "bảo lưu · quyết định lại khi tới tuổi hưu", "at": 3}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "MỖI NGÃ RẼ ĐÚNG VỚI MỘT KIỂU NGƯỜI", "at": 4}, {"text": "KHÔNG NGÃ NÀO ĐÚNG VỚI TẤT CẢ", "at": 5, "acc": True}]},
    {"type": "ledger", "at": 6, "title": "KHI NÀO PHÉP TÍNH KHÔNG ĐÚNG", "rows": [{"k": "1", "v": "GIẢ ĐỊNH ĐIỀU CHỈNH THEO GIÁ", "at": 7}, {"k": "2", "v": "LÃI THỰC LÀ GIẢ ĐỊNH", "at": 8},
                                                                               {"k": "3", "v": "LUẬT CÓ THỂ CÒN ĐỔI", "at": 9}]},
    {"type": "ledger", "at": 10, "title": "BA CÂU TRƯỚC KHI KÝ ĐƠN RÚT MỘT LẦN", "rows": [{"k": "1", "v": "ĐÃ ĐÓNG BAO NHIÊU · THIẾU MẤY NĂM?", "at": 11},
                                                                                      {"k": "2", "v": "TIỀN ẤY DÙNG VIỆC GÌ, CỤ THỂ?", "at": 12},
                                                                                      {"k": "3", "v": "SỐNG TỚI 80, 90: THU NHẬP TỪ ĐÂU?", "at": 13}]},
    {"type": "broll", "at": 14, "vid": "6183991", "veil": 0.55, "illus": VM,
     "kin": [{"text": "SỐ NĂM ĐÓNG · MỨC LƯƠNG ĐÓNG", "at": 14, "sm": True}, {"text": "ỨNG DỤNG BHXH · CƠ QUAN BHXH NƠI BẠN SỐNG", "at": [14, "ứng"], "acc": True},
             {"text": "con số đầu tiên cần có", "at": 16, "sm": True}]},
    {"type": "myth", "at": 17, "mythLab": "200 TRIỆU TRƯỚC MẶT", "myth": "LUÔN TRÔNG TO HƠN", "truthLab": "4,5 TRIỆU/THÁNG · 25 NĂM NỮA", "truth": "TRÔNG RẤT XA",
     "strikeAt": [18, "Bốn"], "truthAt": [18, "thì"]},
    {"type": "timeline", "at": 19, "title": "CÙNG MỘT ĐƯỜNG THẲNG", "items": [dict(x, at=a) for x, a in zip(ROAD, [19, [19, "cả"], [19, "đường"], [19, "nhìn"]])]},
    {"type": "question", "at": 20, "text": "Ở chỗ chị Hạnh,\nbạn đi ngã rẽ nào?"},
    {"type": "kinetic", "at": 21, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 21}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [21, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
TITLES = ["Rút BHXH Một Lần Được Bao Nhiêu? Đóng 10 Năm, Lương 10 Triệu",
          "Đóng BHXH 10 Năm Rồi Nghỉ Việc: Cầm 200 Triệu Năm 2027 Hay Chờ Lương Hưu Năm 2051?",
          "Luật BHXH Mới 15 Năm Là Có Lương Hưu: Phép Tính Cho Người Đã Đóng 10 Năm"]
FORMULA = ("📐 CÁCH TÍNH (ví dụ giả định · giá hôm nay · thay bằng số của bạn)\n• BHXH một lần = lương bình quân × (1,5 × số năm trước 2014 + 2 × số năm từ 2014)\n"
           "• Lương hưu nữ = lương bình quân × (45% + 2% × số năm trên 15), tối đa 75%; nam: 40% ở 15 năm, +1%/năm tới 20 năm, rồi +2%/năm, tối đa 75%\n"
           "• Chị Hạnh: 10 năm × 2 × 10 triệu = 200 triệu; đóng đủ 15 năm → 4,5 triệu/tháng từ 60 tuổi; 200 triệu = 44 tháng lương hưu\n"
           "• 200 triệu × (1 + lãi thực)^25: 0% → 200; 1% → 256; 2% → 328; 3% → 419 triệu (lãi thực là giả định, không phải dự báo)")
SPEC = {
    "title": TITLES[0],
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["rút", "lần", "lương", "hưu", "năm", "triệu", "bảo"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": TITLES,
        "summary": "Chị Hạnh (ví dụ giả định) 35 tuổi, đóng bảo hiểm xã hội 10 năm với lương đóng 10 triệu rồi nghỉ việc: rút một lần được khoảng 200 "
                   "triệu. Video đi dọc con đường 25 năm tới năm chị 60 tuổi (2051) với ba ngã rẽ: cách luật tính khoản một lần và điều kiện mới từ "
                   "01/07/2025, mốc 15 năm để có lương hưu và tỷ lệ hưởng, tuổi nghỉ hưu theo lộ trình, nếu đem 200 triệu đi gửi với lãi thực 0–3% thì "
                   "được bao nhiêu, và khi nào 200 triệu là nhu cầu thật. Mọi số tiền quy về giá hôm nay.",
        "more": ["Nội dung giáo dục, không phải tư vấn đầu tư. Kênh không khuyên rút hay không rút bảo hiểm xã hội. Chị Hạnh, mức lương, số năm đóng và "
                 "các mức lãi thực là ví dụ giả định do kênh tự tính; giả định lương bình quân và lương hưu được điều chỉnh theo giá. Quy định mô tả "
                 "theo thời điểm làm video (10/2026) và có thể thay đổi; trường hợp của bạn hãy kiểm tra trên ứng dụng bảo hiểm xã hội hoặc với cơ "
                 "quan bảo hiểm xã hội. Nội dung do kênh biên soạn từ nguồn công khai; giọng đọc tổng hợp.", FORMULA],
        "chapter_titles": {"ch00": "Mở đầu: hai trăm triệu ở ngay trước mặt", "ch01": "Ngã rẽ 1: rút một lần được bao nhiêu, khi nào",
                           "ch02": "Ngã rẽ 2: mười lăm năm là có lương hưu", "ch03": "Ngã rẽ 3: tuổi nghỉ hưu và 25 năm chờ",
                           "ch04": "Nếu 200 triệu được đem đi gửi: lãi thực 25 năm", "ch05": "Khi 200 triệu là nhu cầu thật",
                           "ch06": "Ba ngã rẽ của chị Hạnh và khi nào phép tính không đúng"},
        "sources": [
            "Công báo — Luật Bảo hiểm xã hội số 41/2024/QH15 (văn bản gốc): https://congbao.chinhphu.vn/van-ban/luat-so-41-2024-qh15-42576.htm",
            "PLO 01/12/2024 — Cách tính lương hưu theo Luật BHXH 2024: https://tuoitre.vn/plo/cach-tinh-luong-huu-theo-luat-bhxh-2024-post821894.html",
            "LuatVietnam — Điều kiện hưởng BHXH một lần (Điều 70 Luật BHXH 2024): https://luatvietnam.vn/bao-hiem/dieu-kien-huong-bao-hiem-xa-hoi-1-lan-563-23984-article.html",
            "MISA meInvoice 16/11/2025 — BHXH tự nguyện từ 01/7/2025 (22% thu nhập chọn, hỗ trợ của Nhà nước): https://www.meinvoice.vn/tin-tuc/32269/bao-hiem-xa-hoi-tu-nguyen/",
            "Nghị định 135/2020/NĐ-CP — tuổi nghỉ hưu (Điều 4): https://vnuf.edu.vn/wp-content/uploads/2021/01/Nghi-dinh_135-2020-ND-CP..pdf",
            "VnEconomy 03/07/2023 — Phần lớn người rút BHXH một lần là lao động trẻ: https://vneconomy.vn/phan-lon-nguoi-lao-dong-rut-bao-hiem-xa-hoi-mot-lan-la-lao-dong-tre.htm",
            "Tuoi Tre News 21/02/2025 — Tuổi thọ trung bình Việt Nam 2024 (nữ 77,3): https://news.tuoitre.vn/average-life-expectancy-in-vietnam-reaches-747-years-in-2024-10384693.htm",
            "Báo Điện tử Chính phủ 01/10/2026 — Chính sách mới từ tháng 10/2026 (trợ cấp hưu trí xã hội 500.000 → 540.000 đồng/tháng từ 05/10/2026, Nghị định 335/2026/NĐ-CP): https://baochinhphu.vn/chinh-sach-moi-co-hieu-luc-tu-thang-10-2026-102261001102816112.htm",
            "Cổng TTĐT Chính phủ — Nghị định 176/2025/NĐ-CP về trợ cấp hưu trí xã hội: https://vanban.chinhphu.vn/?pageid=27160&docid=214435"],
        "hashtags": ["BảoHiểmXãHội", "LươngHưu", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["rút bảo hiểm xã hội một lần", "rút bhxh 1 lần được bao nhiêu", "cách tính lương hưu", "luật bảo hiểm xã hội 2024", "đóng bhxh 15 năm",
                 "tuổi nghỉ hưu", "bảo lưu bảo hiểm xã hội", "bảo hiểm xã hội tự nguyện", "tài chính cá nhân", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: quy định theo Luật Bảo hiểm xã hội 2024 và Nghị định 135/2020 (qua các nguồn ở trên); thống kê người hưởng một lần "
                       "theo báo cáo của Bộ Lao động (qua báo chí); ví dụ chị Hạnh và phép tính do kênh tự lập.",
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
