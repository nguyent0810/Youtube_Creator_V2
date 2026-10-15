"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK E3 "Nợ thẻ tín dụng: chỉ trả tối thiểu".

    python data/long/ck-e3-no-the-tin-dung/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (VÍ DỤ GIẢ ĐỊNH 30%/năm, tối thiểu 5%, không tiêu thêm, không phí).
Luật kênh: chỉ giáo dục; mọi cảnh số của ví dụ ghi "VÍ DỤ GIẢ ĐỊNH"; không tên ngân hàng/sản phẩm; vụ 8,8 tỷ chỉ thuật theo báo chí, không phán đúng sai.
Áp luật studio (14/10/2026): cảnh mới myth / source / units; năm không đếm; mỗi phán định có một nhịp tĩnh phía trước.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN, VIOLET = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444", "#a78bfa"
HYPO = "VÍ DỤ GIẢ ĐỊNH · LÃI 30%/NĂM, KHÔNG TIÊU THÊM, KHÔNG PHÍ"
PRESS = "THEO BÁO CHÍ, 03/2024 · KÊNH KHÔNG PHÁN ĐÚNG SAI"
VM = "VIDEO MINH HỌA"
MONTHS = [f"thang__{m:03d}" for m in range(0, 121)]
MIN, FIX = R["min_only"]["balance"], R["fixed_2m"]["balance"]
assert R["min_only"]["months"] == 115 and R["fixed_2m"]["months"] == 12
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "8,5 TRIỆU THÀNH 8,8 TỶ"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "5916730", "veil": 0.55, "illus": VM,
     "kin": [{"text": "THÁNG 3 NĂM 2024", "at": [0, "Tháng"], "sm": True}, {"text": "MỘT KHOẢN NỢ THẺ TÍN DỤNG", "at": [1, "Một"], "acc": True}]},
    {"type": "bars", "at": 1, "title": "MỘT KHOẢN NỢ THẺ (TRIỆU ĐỒNG)",
     "items": [{"k": "NỢ GỐC", "v": 8.55, "lbl": "≈ 8,5", "at": [1, "gốc"]}, {"k": "SAU 11 NĂM", "v": 8830, "lbl": "≈ 8.830", "at": [2, "hơn"], "acc": True}],
     "label": {"k": PRESS, "v": "", "at": 2}},
    {"type": "slam", "at": 3, "text": "HƠN 1.000 LẦN", "sub": "TỪ 8,5 TRIỆU TỚI 8,8 TỶ", "subAt": 3},
    {"type": "ledger", "at": 4, "title": "HAI PHÍA NÓI GÌ", "srcnote": "DIỄN Ý THEO BÁO CHÍ, 03/2024", "rows": [{"k": "CHỦ THẺ", "v": "KHÔNG TIÊU KHOẢN ẤY", "at": 4}, {"k": "NGÂN HÀNG", "v": "TÍNH ĐÚNG THOẢ THUẬN", "at": 5}],
     "total": {"k": "VIDEO NÀY", "v": "KHÔNG PHÁN AI ĐÚNG", "at": 6}},
    {"type": "question", "at": 7, "text": "Về con số, làm sao 8 triệu\ncó thể thành 8 tỷ?"},
    {"type": "broll", "at": 9, "vid": "6700014", "veil": 0.5, "illus": VM,
     "kin": [{"text": "CÂU TRẢ LỜI NẰM TRÊN", "at": 9, "sm": True}, {"text": "TỜ SAO KÊ", "at": [10, "Tờ"], "acc": True}]},
    {"type": "ledger", "at": 11, "title": "BỐN DÒNG ĐÁNG ĐỌC", "rows": [{"k": "1", "v": "NGÀY ĐẾN HẠN", "at": [12, "Ngày"]}, {"k": "2", "v": "SỐ TIỀN TỐI THIỂU", "at": [12, "Số"]},
                                                                       {"k": "3", "v": "LÃI SUẤT", "at": [12, "Lãi"]}, {"k": "4", "v": "PHÍ CHẬM TRẢ", "at": [12, "Và"]}],
     "total": {"k": "ĐỌC", "v": "TỪNG DÒNG · TỪ TRÊN XUỐNG", "at": 13}},
    {"type": "ledger", "at": 14, "title": "MỜI BẠN ĐOÁN", "srcnote": HYPO, "rows": [{"k": "NỢ THẺ", "v": "20 TRIỆU · KHÔNG TIÊU THÊM", "at": 15},
                                                                                  {"k": "MỖI THÁNG", "v": "CHỈ TRẢ MỨC TỐI THIỂU", "at": 16}],
     "total": {"k": "BAO LÂU", "v": "THÌ HẾT NỢ?", "at": [17, "Bao"]}},
    {"type": "brand", "at": 18, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 19, "items": [{"text": "CHỈ NHẰM GIÁO DỤC", "at": 19, "acc": True},
                                           {"text": "phép tính là ví dụ giả định · không phải lời khuyên tài chính", "at": [19, "Đây"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "DÒNG 01", "t": "NGÀY ĐẾN HẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "DÒNG MỘT", "title": "NGÀY ĐẾN HẠN", "sub": "“MIỄN LÃI 55 NGÀY” LÀ GÌ?", "vid": "11158789", "illus": VM, "titleAt": [0, "ngày"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "MIỄN LÃI TỚI", "at": [2, "Miễn"], "sm": True}, {"text": "45 – 55 NGÀY", "at": [2, "bốn"], "acc": True}]},
    {"type": "slam", "at": 3, "text": "LỜI HỨA ẤY LÀ THẬT", "sub": "NHƯNG CÓ ĐIỀU KIỆN", "subAt": 3},
    {"type": "units", "at": 4, "title": "55 NGÀY = 30 NGÀY KỲ SAO KÊ + 25 NGÀY ĐỂ TRẢ", "total": 55, "cols": 11, "lit": 30, "litAt": [6, "Ba"], "unitLabel": "NGÀY LÀ KỲ SAO KÊ",
     "label": {"k": "VÍ DỤ LOẠI 55 NGÀY · MỖI THẺ MỘT KHÁC", "v": "", "at": 5}},
    {"type": "bars", "at": 7, "title": "SỐ NGÀY MIỄN LÃI BẠN THẬT SỰ CÓ", "unit": "VÍ DỤ LOẠI 55 NGÀY",
     "items": [{"k": "QUẸT THẺ NGÀY ĐẦU KỲ", "v": 55, "lbl": "55 NGÀY", "at": [7, "đủ"], "acc": True}, {"k": "QUẸT THẺ NGÀY CUỐI KỲ", "v": 25, "lbl": "25 NGÀY", "at": [9, "Chỉ"]}]},
    {"type": "myth", "at": 10, "mythLab": "ĐIỀU KIỆN", "myth": "TRẢ MỘT PHẦN", "truthLab": "PHẢI LÀ", "truth": "TRẢ ĐỦ · ĐÚNG HẠN", "strikeAt": [12, "Không"], "truthAt": [12, "Trả"]},
    {"type": "broll", "at": 13, "vid": "8657613", "veil": 0.5, "illus": VM,
     "kin": [{"text": "TRẢ ĐỦ MỖI KỲ", "at": 13, "acc": True}, {"text": "= mượn tiền miễn phí", "at": [13, "thật"], "sm": True},
             {"text": "rắc rối bắt đầu ở dòng thứ hai", "at": 15, "sm": True}]},
]}

CH["ch02"] = {"hud": {"k": "DÒNG 02", "t": "SỐ TIỀN TỐI THIỂU"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "DÒNG HAI", "title": "SỐ TIỀN\nTỐI THIỂU", "sub": "CON SỐ NHỎ NHẤT TRÊN SAO KÊ", "vid": "6962707", "illus": VM, "titleAt": [1, "Số"]},
    {"type": "counter", "at": 2, "from": 5, "to": 5, "suffix": "%", "label": "SỐ NỢ · MỨC TỐI THIỂU THƯỜNG GẶP Ở VIỆT NAM", "sub": {"text": "MỖI THẺ MỘT MỨC · THƯỜNG 2–5%", "at": 2}},
    {"type": "bars", "at": 3, "title": "NỢ 20 TRIỆU (TRIỆU ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH · TỐI THIỂU 5%",
     "items": [{"k": "SỐ NỢ", "v": 20, "lbl": "20", "at": [3, None, 0, 0.05]}, {"k": "TỐI THIỂU THÁNG NÀY", "v": 1, "lbl": "≈ 1", "at": [3, "tối"], "acc": True}]},
    {"type": "myth", "at": 5, "mythLab": "NHIỀU NGƯỜI HIỂU", "myth": "TRẢ TỐI THIỂU LÀ XONG", "truthLab": "THẬT RA", "truth": "CHỈ LÀ KHÔNG BỊ PHẠT", "strikeAt": [6, "Thật"], "truthAt": [7, "không"]},
    {"type": "counter", "at": 9, "from": 19, "to": 19, "suffix": " TRIỆU", "label": "CÒN LẠI · VẪN BỊ TÍNH LÃI", "sub": {"text": HYPO.split(" · ")[0], "at": 9}},
    {"type": "ledger", "at": 10, "title": "CHI TIẾT ÍT NGƯỜI ĐỂ Ý", "srcnote": "Ở NHIỀU THẺ · XEM HỢP ĐỒNG CỦA BẠN",
     "rows": [{"k": "KHÔNG TRẢ ĐỦ", "v": "MẤT MIỄN LÃI CỦA KỲ ẤY", "at": 11}, {"k": "LÃI TÍNH TỪ", "v": "NGÀY BẠN QUẸT THẺ", "at": [12, "tiền"]}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "TỐI THIỂU ≠ SỐ BẠN NỢ THÁNG NÀY", "at": 13, "acc": True},
                                           {"text": "nó là mức thấp nhất để chưa bị gọi là quá hạn", "at": 14, "sm": True}]},
    {"type": "question", "at": 15, "text": "Tháng nào cũng chỉ trả mức ấy\nthì chuyện gì xảy ra?"},
]}

CH["ch03"] = {"hud": {"k": "PHÉP TÍNH", "t": "NỢ 20 TRIỆU"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "ĐÁP ÁN", "title": "PHÉP TÍNH\n20 TRIỆU", "sub": "CHỈ TRẢ TỐI THIỂU THÌ BAO LÂU?", "vid": "6700014", "ms": 8, "illus": VM, "titleAt": [0, "Quay"]},
    {"type": "ledger", "at": 1, "title": "ĐỀ BÀI", "srcnote": HYPO, "rows": [{"k": "NỢ", "v": "20 TRIỆU · KHÔNG TIÊU THÊM", "at": [1, "Nợ"]}, {"k": "MỖI THÁNG TRẢ", "v": "TỐI THIỂU 5%", "at": [1, "mỗi"]},
                                                                           {"k": "LÃI GIẢ ĐỊNH", "v": "30%/NĂM", "at": [2, "ba"]}]},
    {"type": "bars", "at": 3, "title": "THÁNG ĐẦU TIÊN (NGHÌN ĐỒNG)", "unit": HYPO.split(" · ")[0],
     "items": [{"k": "BẠN TRẢ", "v": 1000, "lbl": "1.000", "at": [3, "bạn"]}, {"k": "TRONG ĐÓ LÀ TIỀN LÃI", "v": 500, "lbl": "500", "at": [4, "năm"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "MỘT NỬA SỐ TIỀN BẠN TRẢ", "at": 5, "sm": True}, {"text": "CHƯA CHẠM VÀO GỐC", "at": [5, "chưa"], "acc": True}]},
    {"type": "race", "at": 6, "abs": True, "unit": "TRIỆU", "xlab": "THÁNG ", "xstep": 24, "dates": MONTHS, "title": "SỐ NỢ CÒN LẠI · CHỈ TRẢ TỐI THIỂU", "range": "TRIỆU ĐỒNG · THEO THÁNG",
     "drawAt": [6, None, 0, 0.1], "until": [10, "một"],
     "series": [{"label": "TỐI THIỂU 5%", "color": DOWN, "vals": MIN}], "source": HYPO},
    {"type": "counter", "at": 10, "from": 0, "to": 115, "suffix": " THÁNG", "until": [10, "lăm"], "label": "MỚI HẾT NỢ · GẦN 10 NĂM", "sub": {"text": HYPO, "at": 11}},
    {"type": "bars", "at": 12, "title": "MÓN NỢ 20 TRIỆU, TRẢ TỐI THIỂU (TRIỆU ĐỒNG)", "unit": HYPO.split(" · ")[0],
     "items": [{"k": "NỢ GỐC", "v": 20, "lbl": "20", "at": [12, None, 0, 0.05]}, {"k": "TỔNG TIỀN LÃI", "v": 17.9, "lbl": "≈ 17,9", "at": [12, "gần"], "acc": True},
               {"k": "TỔNG ĐÃ TRẢ", "v": 37.9, "lbl": "≈ 37,9", "at": [14, "cuối"]}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "GIỜ ĐỔI MỘT CHI TIẾT", "at": 15, "sm": True}, {"text": "THÁNG NÀO CŨNG TRẢ 2 TRIỆU", "at": [16, "tháng"], "acc": True}]},
    {"type": "race", "at": 17, "abs": True, "unit": "TRIỆU", "xlab": "THÁNG ", "xstep": 24, "dates": MONTHS, "title": "CÙNG MÓN NỢ 20 TRIỆU · HAI CÁCH TRẢ", "range": "TRIỆU ĐỒNG · THEO THÁNG",
     "drawAt": [17, None, 0, 0.1], "until": [18, "Chỉ"],
     "series": [{"label": "TỐI THIỂU", "color": DOWN, "vals": MIN}, {"label": "2 TRIỆU/THÁNG", "color": UP, "vals": FIX}], "source": HYPO},
    {"type": "slam", "at": 19, "text": "9 NĂM · GẦN 15 TRIỆU", "sub": "KHOẢNG CHÊNH GIỮA HAI CÁCH TRẢ", "subAt": 19},
    {"type": "question", "at": 20, "text": "Con số 30% ấy\ntừ đâu ra?"},
]}

CH["ch04"] = {"hud": {"k": "DÒNG 03", "t": "LÃI SUẤT"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "DÒNG BA", "title": "LÃI SUẤT", "sub": "20 – 40% MỘT NĂM", "vid": "7568745", "illus": VM, "titleAt": [0, "lãi"]},
    {"type": "source", "at": 1, "source": "BIỂU PHÍ THẺ TÍN DỤNG · BÁO CHÍ TỔNG HỢP", "ref": "LÃI THẺ TÍN DỤNG", "snippet": "thường từ [[20 tới 40% một năm]] · mỗi thẻ một mức",
     "hlAt": [1, "hai"], "seal": "XEM HỢP ĐỒNG CỦA BẠN", "sealAt": [2, "Con"]},
    {"type": "bars", "at": 3, "title": "LÃI MỘT NĂM (%)", "unit": "KHOẢNG THƯỜNG GẶP · KHÔNG PHẢI MỨC CỦA SẢN PHẨM NÀO",
     "items": [{"k": "TIỀN GỬI 12 THÁNG", "v": 6, "lbl": "5 – 7", "at": [4, "năm"]}, {"k": "LÃI THẺ · MỨC THẤP", "v": 20, "lbl": "20", "at": [5, "Lãi"]},
               {"k": "LÃI THẺ · MỨC CAO", "v": 40, "lbl": "40", "at": [5, "bốn,"], "acc": True}]},
    {"type": "ledger", "at": 6, "title": "QUY TẮC 72", "srcnote": "72 ÷ LÃI SUẤT = SỐ NĂM ĐỂ GẤP ĐÔI", "rows": [{"k": "LÃI 6%/NĂM", "v": "≈ 12 NĂM", "at": [8, "mười"]}, {"k": "LÃI 30%/NĂM", "v": "≈ 2,5 NĂM", "at": [9, "chỉ"]}]},
    {"type": "broll", "at": 10, "vid": "5981296", "veil": 0.55, "illus": VM,
     "kin": [{"text": "CÙNG MỘT QUẢ CẦU TUYẾT", "at": 10}, {"text": "LẦN NÀY LĂN VỀ PHÍA BẠN", "at": [10, "Nhưng"], "acc": True}]},
    {"type": "ledger", "at": 11, "title": "RÚT TIỀN MẶT BẰNG THẺ TÍN DỤNG", "srcnote": "Ở NHIỀU THẺ · XEM BIỂU PHÍ CỦA BẠN",
     "rows": [{"k": "CÓ", "v": "PHÍ RÚT TIỀN", "at": [13, "phí"]}, {"k": "LÃI TÍNH", "v": "NGAY TỪ NGÀY RÚT", "at": [13, "bị"]}], "total": {"k": "NGÀY MIỄN LÃI", "v": "KHÔNG CÓ", "at": [13, "không"]}},
    {"type": "kinetic", "at": 14, "items": [{"text": "BA DÒNG CHƯA ĐỦ", "at": 14, "sm": True}, {"text": "ĐỂ 8 TRIỆU THÀNH 8 TỶ", "at": [14, "để"], "acc": True},
                                           {"text": "phải cần tới dòng thứ tư", "at": 15, "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "DÒNG 04", "t": "PHÍ CHẬM TRẢ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "DÒNG BỐN", "title": "PHÍ CHẬM TRẢ", "sub": "DÒNG NHỎ NHẤT · ÍT NGƯỜI ĐỌC", "vid": "6962701", "illus": VM, "titleAt": [1, "Phí"]},
    {"type": "ledger", "at": 2, "title": "KHÔNG TRẢ NỔI CẢ MỨC TỐI THIỂU", "srcnote": "MỨC CỤ THỂ TUỲ TỪNG HỢP ĐỒNG",
     "rows": [{"k": "1", "v": "PHÍ PHẠT CHẬM TRẢ", "at": 3}, {"k": "2", "v": "LÃI SUẤT QUÁ HẠN · CAO HƠN", "at": 4}]},
    {"type": "timeline", "at": 6, "title": "THÁNG SAU VẪN KHÔNG TRẢ", "items": [{"year": "BƯỚC 1", "text": "phí + lãi cộng vào số nợ", "at": 6}, {"year": "BƯỚC 2", "text": "lãi tính trên con số mới", "at": 7},
                                                                              {"year": "LẶP LẠI", "text": "lãi mẹ đẻ lãi con", "at": 8}]},
    {"type": "broll", "at": 9, "vid": "5916730", "ms": 6, "veil": 0.55, "illus": VM,
     "kin": [{"text": "QUAY LẠI CON SỐ ĐẦU VIDEO", "at": 9, "acc": True}, {"text": "bảng tính chi tiết không được công bố · kênh chỉ tính ngược", "at": 10, "sm": True}]},
    {"type": "counter", "at": 11, "from": 5.4, "to": 5.4, "suffix": "%", "label": "MỖI THÁNG · MỨC LỚN THÊM ĐỂ 8,5 TRIỆU THÀNH 8,8 TỶ SAU 11 NĂM",
     "sub": {"text": "KÊNH TỰ TÍNH NGƯỢC · KHÔNG PHẢI SỐ CỦA NGÂN HÀNG", "at": [12, "Tháng"]}},
    {"type": "kinetic", "at": 13, "items": [{"text": "5,4% MỘT THÁNG", "at": 13, "sm": True}, {"text": "GẤP GẦN ĐÔI SAU MỖI NĂM", "at": [14, "gấp"], "acc": True}]},
    {"type": "units", "at": 15, "title": "11 NĂM · MỖI NĂM GẤP GẦN ĐÔI", "total": 11, "cols": 11, "lit": 11, "litAt": [15, "mười"], "unitLabel": "LẦN GẤP GẦN ĐÔI → HƠN 1.000 LẦN",
     "label": {"k": "1,88 MŨ 11 ≈ 1.030 · KÊNH TỰ TÍNH", "v": "", "at": 15}},
    {"type": "myth", "at": 16, "mythLab": "ĐÁNG SỢ", "myth": "KHOẢN LỚN, TRẢ DẦN", "truthLab": "ĐÁNG SỢ HƠN", "truth": "KHOẢN NHỎ, BỊ BỎ QUÊN", "strikeAt": [17, "Một"], "truthAt": [17, "đáng"]},
    {"type": "kinetic", "at": 18, "items": [{"text": "HAI BÊN CHƯA THỐNG NHẤT · KÊNH KHÔNG KẾT LUẬN THAY AI", "at": 18, "sm": True},
                                           {"text": "ĐỪNG ĐỂ TỜ SAO KÊ NẰM IM", "at": [19, "đừng"], "acc": True}]},
    {"type": "broll", "at": 20, "vid": "6962707", "ms": 1, "veil": 0.55, "illus": VM,
     "kin": [{"text": "MỘT VIỆC NHỎ · NGAY HÔM NAY", "at": 20, "sm": True}, {"text": "TÌM DÒNG TIỀN LÃI TRÊN SAO KÊ", "at": [21, "tìm"], "acc": True},
             {"text": "quả cầu tuyết đang lăn nhanh tới đâu?", "at": 23, "sm": True}]},
]}

CH["ch06"] = {"hud": {"k": "GIỚI HẠN", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "PHẦN CUỐI", "title": "KHI NÀO PHÉP TÍNH\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": "6631688", "illus": VM, "titleAt": [0, "Và"]},
    {"type": "ledger", "at": 1, "title": "PHÉP TÍNH CÒN GIẢ ĐỊNH", "rows": [{"k": "1", "v": "LÃI 30%: THẺ BẠN CÓ THỂ KHÁC", "at": 1}, {"k": "2", "v": "KHÔNG TIÊU THÊM ĐỒNG NÀO", "at": 3},
                                                                          {"k": "3", "v": "MỖI HỢP ĐỒNG MỘT CÁCH TÍNH", "at": 5}]},
    {"type": "ledger", "at": 7, "title": "BA CÂU TỰ HỎI TRƯỚC TỜ SAO KÊ", "rows": [{"k": "1", "v": "TRẢ TỐI THIỂU: THÁNG NÀY BAO NHIÊU TIỀN LÃI?", "at": 8}, {"k": "2", "v": "LÃI SUẤT MỘT NĂM CỦA THẺ MÌNH?", "at": 9},
                                                                                 {"k": "3", "v": "LỠ MỘT KỲ: PHÍ VÀ LÃI QUÁ HẠN?", "at": 10}]},
    {"type": "myth", "at": 11, "mythLab": "TRẢ ĐỦ MỖI KỲ", "myth": "MƯỢN MIỄN PHÍ", "truthLab": "CHỈ TRẢ TỐI THIỂU", "truth": "KHOẢN VAY RẤT ĐẮT", "strikeAt": [13, "Chỉ"], "truthAt": [13, "nó"]},
    {"type": "broll", "at": 14, "vid": "11158789", "ms": 4, "veil": 0.5, "illus": VM,
     "kin": [{"text": "CÙNG MỘT TẤM THẺ", "at": 14}, {"text": "KHÁC NHAU Ở MỘT DÒNG TRÊN SAO KÊ", "at": [14, "Khác"], "acc": True}]},
    {"type": "question", "at": 15, "text": "Bạn đã bao giờ đọc hết\ntờ sao kê của mình chưa?"},
    {"type": "kinetic", "at": 16, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 16}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [16, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
SPEC = {
    "title": "Nợ Thẻ Tín Dụng: Chỉ Trả “Tối Thiểu” Thì Bao Giờ Hết Nợ? Phép Tính 20 Triệu",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["tối", "thiểu", "lãi", "sao", "kê", "đủ", "phí"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Nợ Thẻ Tín Dụng: Chỉ Trả “Tối Thiểu” Thì Bao Giờ Hết Nợ? Phép Tính 20 Triệu",
                   "8,5 Triệu Thành 8,8 Tỷ: Bốn Dòng Trên Tờ Sao Kê Thẻ Tín Dụng Mà Bạn Nên Đọc",
                   "“Miễn Lãi 55 Ngày” Và “Thanh Toán Tối Thiểu”: Thẻ Tín Dụng Tính Lãi Thế Nào?"],
        "summary": "Năm 2024, báo chí đưa tin một khoản nợ thẻ tín dụng gốc khoảng 8,5 triệu đồng thành hơn 8,8 tỷ sau 11 năm. Video không phán ai "
                   "đúng ai sai, chỉ hỏi: về mặt con số, vì sao có thể như vậy? Câu trả lời nằm ở bốn dòng trên tờ sao kê: ngày đến hạn, số tiền tối "
                   "thiểu, lãi suất và phí chậm trả. Kèm phép tính: nợ 20 triệu, chỉ trả tối thiểu thì bao lâu mới hết, và khi nào phép tính này "
                   "không đúng với bạn.",
        "more": [Y4["more"][0],
                 "📐 CÁCH KÊNH TÍNH: ví dụ dùng lãi suất GIẢ ĐỊNH 30%/năm (tính theo tháng 2,5%), mức tối thiểu 5% dư nợ (sàn 100 nghìn đồng), không tiêu "
                 "thêm, không phí: hết nợ sau 115 tháng, tổng lãi ≈ 17,9 triệu; trả đều 2 triệu/tháng: 12 tháng, lãi ≈ 3,3 triệu. Đây là phép tính, "
                 "không phải mức lãi của thẻ nào và không phải dự báo. Con số 5,4%/tháng là kênh tự tính ngược từ hai con số báo chí đăng (nợ gốc ≈ 8,55 "
                 "triệu, số thông báo ≈ 8,83 tỷ sau khoảng 11 năm), không phải số do ngân hàng công bố. Lãi suất, mức tối thiểu, phí và cách tính ngày "
                 "khác nhau theo từng hợp đồng: hãy đọc hợp đồng và biểu phí của chính bạn."],
        "chapter_titles": {"ch00": "Mở đầu: 8,5 triệu thành 8,8 tỷ", "ch01": "Dòng 1: ngày đến hạn và “miễn lãi 55 ngày”", "ch02": "Dòng 2: số tiền tối thiểu",
                           "ch03": "Phép tính 20 triệu: chỉ trả tối thiểu thì bao lâu?", "ch04": "Dòng 3: lãi suất 20–40%/năm", "ch05": "Dòng 4: phí chậm trả, lãi mẹ đẻ lãi con",
                           "ch06": "Khi nào phép tính này không đúng với bạn"},
        "sources": ["https://znews.vn/no-the-tin-dung-8-5-trieu-sau-11-nam-len-8-8-ty-tinh-lai-the-nao-post1465068.html",
                    "https://thitruongtaichinhtiente.vn/vu-no-8-5-trieu-bi-tinh-lai-hon-8-8-ty-nhung-dieu-can-biet-khi-dung-the-tin-dung-57760.html",
                    "https://nhadautu.vn/tuyet-chieu-xai-the-tin-dung-khong-he-lo-lai-suat-d29568.html",
                    "https://vnreview.vn/threads/chu-the-tin-dung-can-luu-y-du-thanh-toan-du-no-toi-thieu-khoan-no-con-lai-van-bi-tinh-lai-suat-20-40-nam.59503/"],
        "hashtags": ["TàiChínhCáNhân", "ThẻTínDụng", "NợThẻ", "LãiKép", "BiểuĐồBiếtNói"],
        "tags": ["nợ thẻ tín dụng", "thanh toán tối thiểu", "thẻ tín dụng tính lãi thế nào", "miễn lãi 55 ngày", "lãi suất thẻ tín dụng", "sao kê thẻ tín dụng",
                 "phí chậm thanh toán", "tài chính cá nhân", "lãi kép", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: phép tính trả nợ do kênh tự lập (ví dụ giả định); vụ nợ thẻ và khoảng lãi suất, mức tối thiểu theo báo chí tổng hợp.",
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
