"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK B2 "Lãi Kép".

    python data/long/ck-b2-lai-kep/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (VÍ DỤ GIẢ ĐỊNH 6%/năm; hai số thật: sổ 12 tháng cuộn 8 năm, CPI 2018–2025).
Luật kênh: chỉ giáo dục; mọi cảnh số của ví dụ ghi "VÍ DỤ GIẢ ĐỊNH"; không tên ngân hàng/sản phẩm. Lan, Minh là nhân vật giả định. beat2 bật.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN, VIOLET = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444", "#a78bfa"
HYPO = "VÍ DỤ GIẢ ĐỊNH · LÃI 6%/NĂM KHÔNG ĐỔI, KHÔNG RÚT · KHÔNG PHẢI DỰ BÁO"
REAL = "SỐ THẬT · KÊNH TỰ TÍNH TỪ NGUỒN CÔNG KHAI · QUÁ KHỨ"
VM = "VIDEO MINH HỌA"
YEARS = [f"nam__{y:02d}" for y in range(0, 31)]


def fv(months, pay=3.0, start=0.0, rate=0.005):
    v = start
    for _ in range(months):
        v = v * (1 + rate) + pay
    return v


LAN = [fv(12 * y) if y <= 10 else fv(12 * (y - 10), pay=0.0, start=fv(120)) for y in range(31)]
MINH = [0.0 if y <= 10 else fv(12 * (y - 10)) for y in range(31)]
SNOW = [fv(12 * y) for y in range(31)]
PAID = [36.0 * y for y in range(31)]
assert round(LAN[30], 1) == R["lan_minh"]["lan_final"] and round(MINH[30], 1) == R["lan_minh"]["minh_final"]
rnd = lambda xs: [round(x, 1) for x in xs]
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI NGƯỜI BẠN, MỘT CÂU ĐỐ"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "7010559", "veil": 0.5, "illus": VM + " · NHÂN VẬT GIẢ ĐỊNH",
     "kin": [{"text": "LAN VÀ MINH", "at": [0, "Lan"], "acc": True}, {"text": "mỗi người 3 triệu mỗi tháng · cùng một mức lãi", "at": 1, "sm": True}]},
    {"type": "ledger", "at": 2, "title": "LAN", "srcnote": "NHÂN VẬT GIẢ ĐỊNH", "rows": [{"k": "BẮT ĐẦU", "v": "NĂM 25 TUỔI", "at": 2}, {"k": "ĐỂ DÀNH", "v": "ĐÚNG 10 NĂM", "at": 3}],
     "total": {"k": "RỒI", "v": "DỪNG HẲN · ĐỂ YÊN", "at": [3, "rồi"]}},
    {"type": "ledger", "at": 4, "title": "MINH", "srcnote": "NHÂN VẬT GIẢ ĐỊNH", "rows": [{"k": "BẮT ĐẦU", "v": "NĂM 35 TUỔI", "at": 4}],
     "total": {"k": "NỘP", "v": "SUỐT 20 NĂM · KHÔNG NGHỈ", "at": [5, "suốt"]}},
    {"type": "bars", "at": 6, "title": "TỚI NĂM 55 TUỔI · TỔNG TIỀN ĐÃ NỘP (TRIỆU ĐỒNG)",
     "items": [{"k": "LAN · NỘP 10 NĂM", "v": 360, "lbl": "360", "at": 7}, {"k": "MINH · NỘP 20 NĂM", "v": 720, "lbl": "720", "at": 8, "acc": True}],
     "label": {"k": "GẤP ĐÔI", "v": "VÍ DỤ GIẢ ĐỊNH", "at": [8, "Gấp"]}},
    {"type": "question", "at": 9, "text": "Ai có nhiều tiền hơn?"},
    {"type": "kinetic", "at": 10, "items": [{"text": "CÂU TRẢ LỜI NẰM TRONG HAI CHỮ", "at": [10, "Và"], "sm": True}, {"text": "LÃI KÉP", "at": [10, "lãi"], "acc": True}]},
    {"type": "ledger", "at": 11, "title": "TRONG VIDEO NÀY", "rows": [{"k": "1 CON SỐ", "v": "NĂM THỨ MẤY LÃI VƯỢT TIỀN NỘP?", "at": 12},
                                                                    {"k": "1 CẢNH BÁO", "v": "THỨ LẶNG LẼ ĂN MÒN LÃI KÉP", "at": 13}]},
    {"type": "brand", "at": 14, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 15, "items": [{"text": "CHỈ NHẰM GIÁO DỤC", "at": 15, "acc": True},
                                           {"text": "mức lãi trong ví dụ là giả định · không phải lời khuyên · không dự báo", "at": [15, "Mức"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "LÃI ĐẺ RA LÃI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "LÃI ĐẺ RA LÃI", "sub": "LÃI KÉP LÀ GÌ?", "vid": "8479054", "illus": VM, "titleAt": [0, "Lãi"]},
    {"type": "ledger", "at": 2, "title": "THỬ MỘT PHÉP TÍNH", "srcnote": HYPO,
     "rows": [{"k": "GỐC", "v": "100 TRIỆU", "at": [2, "một"]}, {"k": "LÃI GIẢ ĐỊNH", "v": "6%/NĂM", "at": [2, "sáu"]},
              {"k": "HẾT NĂM 1", "v": "106 TRIỆU", "at": 3}, {"k": "NĂM 2: 6% TÍNH TRÊN", "v": "106 TRIỆU, KHÔNG PHẢI 100", "at": 5}],
     "total": {"k": "LÃI NĂM 2", "v": "6,36 TRIỆU", "at": 6}},
    {"type": "counter", "at": 7, "from": 0, "to": 360000, "suffix": " đ", "until": [7, "nghìn"], "label": "LÃI CỦA TIỀN LÃI", "sub": {"text": "nghe chẳng đáng là bao", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "HÃY CHO NÓ", "at": 9, "sm": True}, {"text": "THỜI GIAN", "at": [9, "thời"], "acc": True}]},
    {"type": "bars", "at": 10, "title": "100 TRIỆU SAU 30 NĂM (TRIỆU ĐỒNG)",
     "items": [{"k": "NĂM NÀO CŨNG RÚT LÃI RA TIÊU", "v": 280, "lbl": "280", "at": [10, "hai"]}, {"k": "ĐỂ LÃI NHẬP VÀO GỐC", "v": 574, "lbl": "≈ 574", "at": [11, "năm"], "acc": True}],
     "label": {"k": "HƠN GẤP ĐÔI", "v": HYPO, "at": 12}},
    {"type": "broll", "at": 13, "vid": "6415314", "veil": 0.5, "illus": VM,
     "kin": [{"text": "QUẢ CẦU TUYẾT", "at": [13, "quả"], "acc": True}, {"text": "mỗi vòng dính thêm nhiều tuyết hơn vòng trước", "at": [14, "mỗi"], "sm": True}]},
    {"type": "question", "at": 15, "text": "3 triệu mỗi tháng:\nquả cầu ấy lăn thế nào?"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "NĂM THỨ MƯỜI BA"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "race", "abs": True, "unit": "TRIỆU", "xlab": "NĂM ", "xstep": 5, "dates": YEARS, "title": "NỘP 3 TRIỆU MỖI THÁNG · 30 NĂM", "range": "NĂM 0 → 30 · TRIỆU ĐỒNG",
     "drawAt": [0, None, 0, 0.1], "until": [5, "nộp"],
     "series": [{"label": "TÀI KHOẢN (LÃI 6%)", "color": GOLD, "vals": rnd(SNOW)}, {"label": "TIỀN ĐÃ NỘP", "color": BLUE, "vals": rnd(PAID)}], "source": HYPO},
    {"type": "bars", "at": 6, "title": "SAU 10 · 20 · 30 NĂM (TRIỆU ĐỒNG)",
     "items": [{"k": "10 NĂM · NỘP 360", "v": 492, "lbl": "≈ 492", "at": [6, None, 0, 0.05]}, {"k": "20 NĂM · NỘP 720", "v": 1386, "lbl": "≈ 1.386", "at": [6, None, 0, 0.25]},
               {"k": "30 NĂM · NỘP 1.080", "v": 3014, "lbl": "≈ 3.014", "at": [6, "ba"], "acc": True}],
     "label": {"k": "GẦN 2/3 LÀ TIỀN LÃI", "v": HYPO, "at": 7}},
    {"type": "kinetic", "at": 8, "items": [{"text": "CON SỐ MÌNH HỨA", "at": 8, "sm": True}]},
    {"type": "counter", "at": 9, "from": 1, "to": 13, "prefix": "NĂM THỨ ", "until": [9, "ba"], "label": "TIỀN LÃI MỘT NĂM > 36 TRIỆU BẠN NỘP TRONG NĂM",
     "sub": {"text": HYPO, "at": 10}},
    {"type": "slam", "at": 11, "text": "TIỀN LÀM VIỆC CHĂM HƠN BẠN", "sub": "TỪ NĂM THỨ 13 · VÍ DỤ GIẢ ĐỊNH"},
    {"type": "question", "at": 12, "text": "Mười ba năm cơ à?"},
    {"type": "broll", "at": 13, "vid": "37127207", "veil": 0.5, "illus": VM,
     "kin": [{"text": "10 NĂM ĐẦU: GẦN NHƯ VÔ HÌNH", "at": 14, "acc": True}, {"text": "phần lớn người ta bỏ cuộc trước khi thấy nó", "at": [14, "Phần"], "sm": True}]},
    {"type": "ledger", "at": 15, "title": "QUY TẮC 72 · TÍNH NHẨM", "srcnote": "MẸO ƯỚC LƯỢNG · 6% → CHÍNH XÁC LÀ 11,9 NĂM",
     "rows": [{"k": "72 ÷ LÃI SUẤT", "v": "SỐ NĂM ĐỂ TIỀN GẤP ĐÔI", "at": 16}], "total": {"k": "72 ÷ 6", "v": "≈ 12 NĂM", "at": 17}},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "LỜI GIẢI CHO LAN VÀ MINH"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "LỜI GIẢI CHO\nLAN VÀ MINH", "sub": "NỘP ÍT HƠN MỘT NỬA", "vid": "7010559", "ms": 6, "illus": VM,
     "titleAt": [0, "Giờ"]},
    {"type": "race", "at": 2, "abs": True, "unit": "TRIỆU", "xlab": "NĂM ", "xstep": 5, "dates": YEARS, "title": "LAN VÀ MINH · TỪ 25 ĐẾN 55 TUỔI", "range": "NĂM 0 = 25 TUỔI · TRIỆU ĐỒNG",
     "drawAt": [2, None, 0, 0.1], "until": [4, "Khoảng"],
     "series": [{"label": "LAN · NỘP 10 NĂM RỒI ĐỂ YÊN", "color": GOLD, "vals": rnd(LAN)}, {"label": "MINH · NỘP 20 NĂM", "color": BLUE, "vals": rnd(MINH)}], "source": HYPO},
    {"type": "bars", "at": 5, "title": "NĂM 55 TUỔI (TRIỆU ĐỒNG)",
     "items": [{"k": "MINH · ĐÃ NỘP 720", "v": 1386, "lbl": "≈ 1.386", "at": [5, None, 0, 0.05]}, {"k": "LAN · ĐÃ NỘP 360", "v": 1627, "lbl": "≈ 1.627", "at": [5, "lại"], "acc": True}],
     "label": {"k": "NỘP ÍT HƠN MỘT NỬA", "v": "CÓ NHIỀU HƠN ≈ 240 TRIỆU · " + HYPO, "at": [5, "hai"]}},
    {"type": "question", "at": 6, "text": "Sao lại thế được?"},
    {"type": "ledger", "at": 7, "title": "LAN Ở TUỔI 35", "srcnote": HYPO,
     "rows": [{"k": "ĐÃ CÓ SẴN", "v": "GẦN 500 TRIỆU", "at": [7, "gần"]}, {"k": "CÒN", "v": "20 NĂM ĐỂ LĂN", "at": 8}], "total": {"k": "20 NĂM · 6%", "v": "GẤP HƠN 3 LẦN", "at": 9}},
    {"type": "kinetic", "at": 10, "items": [{"text": "TIỀN MINH NỘP NĂM CUỐI", "at": 10, "sm": True}, {"text": "MỚI LĂN VÀI THÁNG", "at": [10, "mới"], "acc": True}]},
    {"type": "counter", "at": 11, "from": 3.0, "to": 3.5, "suffix": " TRIỆU", "until": [11, "rưỡi,"], "label": "MỖI THÁNG · MINH PHẢI NỘP ĐỂ ĐUỔI KỊP LAN", "sub": {"text": "SUỐT 20 NĂM · " + HYPO, "at": 11}},
    {"type": "slam", "at": 12, "text": "10 NĂM ĐI TRƯỚC", "sub": "THỨ QUÝ NHẤT KHÔNG PHẢI SỐ TIỀN", "subAt": 12},
    {"type": "kinetic", "at": 14, "items": [{"text": "KHOAN KẾT LUẬN", "at": 14, "acc": True}, {"text": "còn hai thứ phép tính này chưa nhắc tới", "at": [14, "Vì"], "sm": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "THỨ LẶNG LẼ ĂN MÒN"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "broll", "vid": "37127207", "ms": 12, "veil": 0.5, "illus": VM,
     "kin": [{"text": "LẠM PHÁT", "at": [0, "lạm"], "acc": True}, {"text": "3 tỷ của 30 năm sau ≠ 3 tỷ hôm nay", "at": 1, "sm": True}]},
    {"type": "bars", "at": 2, "title": "GIÁ CẢ TĂNG BÌNH QUÂN MỖI NĂM (%) · VIỆT NAM", "unit": "",
     "items": [{"k": y, "v": v, "lbl": str(v).replace(".", ","), "at": [3, None, 0, 0.1 + 0.18 * i]} for i, (y, v) in
               enumerate(zip(["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"], [3.54, 2.79, 3.23, 1.84, 3.15, 3.25, 3.63, 3.31]))],
     "label": {"k": "BÌNH QUÂN ≈ 3,1%/NĂM", "v": "NGUỒN: CỤC THỐNG KÊ (QUA BÁO CHÍ)", "at": [3, "khoảng"]}},
    {"type": "kinetic", "at": 4, "items": [{"text": "CŨNG LÀ LÃI KÉP", "at": [4, "Nhưng"]}, {"text": "CHẠY NGƯỢC CHIỀU", "at": [4, "chạy"], "acc": True}]},
    {"type": "counter", "at": 5, "from": 0, "to": 23, "suffix": " NĂM", "until": [5, "ba"], "label": "SỨC MUA CỦA MỘT ĐỒNG CÒN MỘT NỬA", "sub": {"text": "VỚI LẠM PHÁT 3,1%/NĂM · PHÉP TÍNH", "at": 5}},
    {"type": "bars", "at": 6, "title": "3 TRIỆU/THÁNG SAU 30 NĂM (TRIỆU ĐỒNG)",
     "items": [{"k": "TRÊN BẢNG TÍNH", "v": 3014, "lbl": "≈ 3.014", "at": [6, None, 0, 0.05]}, {"k": "THEO SỨC MUA HÔM NAY", "v": 1206, "lbl": "≈ 1.206", "at": [6, "chỉ"], "acc": True},
               {"k": "TIỀN ĐÃ NỘP", "v": 1080, "lbl": "1.080", "at": 7}],
     "label": {"k": "", "v": HYPO + " · LẠM PHÁT 3,1%", "at": 6}},
    {"type": "bars", "at": 8, "title": "SỐ THẬT 8 NĂM QUA: 100 ĐỒNG GỬI 12 THÁNG, ĐÁO HẠN GỬI TIẾP",
     "items": [{"k": "GỐC 10/2018", "v": 100, "lbl": "100", "at": 8}, {"k": "10/2026 · DANH NGHĨA", "v": 156, "lbl": "≈ 156", "at": [9, "một", 1]},
               {"k": "SAU LẠM PHÁT", "v": 121, "lbl": "≈ 121", "at": 10, "acc": True}],
     "label": {"k": "NHÓM NGÂN HÀNG LỚN", "v": REAL, "at": 9}},
    {"type": "slam", "at": 11, "text": "HƠN 2%/NĂM", "sub": "LÃI THẬT SAU LẠM PHÁT · KHÔNG PHẢI 6", "subAt": 12},
    {"type": "kinetic", "at": 13, "items": [{"text": "LÃI KÉP VẪN CHẠY", "at": 13}, {"text": "NHƯNG CHẬM HƠN BẢNG TÍNH TRÊN MẠNG", "at": [13, "Nhưng"], "acc": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "KHI QUẢ CẦU TUYẾT LĂN NGƯỢC"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "KHI QUẢ CẦU TUYẾT\nLĂN NGƯỢC", "sub": "LÃI KÉP KHÔNG ĐỨNG VỀ PHÍA AI", "vid": "6963972", "illus": VM,
     "titleAt": [0, "Thứ"]},
    {"type": "ledger", "at": 1, "title": "CHỈ LÀ MỘT PHÉP NHÂN", "rows": [{"k": "BẠN GỬI TIỀN", "v": "NÓ NHÂN CHO BẠN", "at": 2}, {"k": "BẠN NỢ TIỀN", "v": "NÓ NHÂN CHO NGƯỜI CHO VAY", "at": [2, "Bạn", 1]}]},
    {"type": "bars", "at": 3, "title": "NỢ 30 TRIỆU · LÃI 25%/NĂM · KHÔNG TRẢ (TRIỆU ĐỒNG)",
     "items": [{"k": "BAN ĐẦU", "v": 30, "lbl": "30", "at": 4}, {"k": "SAU 1 NĂM", "v": 38.4, "lbl": "> 38", "at": 5}, {"k": "SAU 3 NĂM", "v": 63, "lbl": "63", "at": 6},
               {"k": "SAU 5 NĂM", "v": 103.4, "lbl": "> 100", "at": 7, "acc": True}],
     "label": {"k": "GẤP HƠN 3 LẦN", "v": "VÍ DỤ GIẢ ĐỊNH · KHÔNG GÁN CHO LOẠI VAY NÀO", "at": [7, "Gấp"]}},
    {"type": "broll", "at": 8, "vid": "6415314", "ms": 10, "veil": 0.55, "illus": VM,
     "kin": [{"text": "CÙNG MỘT QUẢ CẦU TUYẾT", "at": 8}, {"text": "LẦN NÀY LĂN VỀ PHÍA BẠN", "at": [8, "lần"], "acc": True}]},
    {"type": "question", "at": 9, "text": "Mình có khoản nợ nào\nlãi cao hơn mức mình kiếm được?", "showAt": 10},
    {"type": "kinetic", "at": 11, "items": [{"text": "TRẢ BỚT NỢ LÃI CAO", "at": 11}, {"text": "= DỪNG MỘT QUẢ CẦU LĂN NGƯỢC", "at": [11, "cũng"], "acc": True}]},
]}

SR = {s["rate"]: s["value"] for s in R["sens_rate"]}
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "KHI NÀO PHÉP TÍNH\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": "8970851", "illus": VM,
     "titleAt": [0, "Và"]},
    {"type": "bars", "at": 2, "title": "3 TRIỆU/THÁNG · 30 NĂM · ĐỔI MỨC LÃI GIẢ ĐỊNH (TRIỆU ĐỒNG)",
     "items": [{"k": "4%/NĂM", "v": SR[0.04], "lbl": "≈ 2.082", "at": [4, "bốn"], "acc": True}, {"k": "6%/NĂM", "v": SR[0.06], "lbl": "≈ 3.014", "at": 2},
               {"k": "8%/NĂM", "v": SR[0.08], "lbl": "≈ 4.471", "at": [3, "hơn"]}],
     "label": {"k": "8 NĂM QUA: LÃI 12 THÁNG TỪ < 5% TỚI > 7%", "v": HYPO.split(" · ")[0] + " · " + REAL, "at": 3}},
    {"type": "ledger", "at": 5, "title": "PHÉP TÍNH CÒN GIẢ ĐỊNH", "rows": [{"k": "2", "v": "KHÔNG RÚT RA LẦN NÀO TRONG 30 NĂM", "at": 5},
                                                                          {"k": "", "v": "KHÔNG ỐM ĐAU · MẤT VIỆC · VIỆC GẤP", "at": 6},
                                                                          {"k": "3", "v": "3 TRIỆU HÔM NAY ≠ 3 TRIỆU 20 NĂM NỮA", "at": 7}]},
    {"type": "ledger", "at": 8, "title": "BA CÂU TỰ HỎI TRƯỚC MỘT BẢNG TÍNH", "rows": [{"k": "1", "v": "MỨC LÃI LÀ THẬT HAY GIẢ ĐỊNH?", "at": 9}, {"k": "2", "v": "ĐÃ TRỪ LẠM PHÁT CHƯA?", "at": 10},
                                                                                     {"k": "3", "v": "MÌNH CÓ KHOẢN NỢ NÀO LĂN NGƯỢC?", "at": 11}]},
    {"type": "broll", "at": 12, "vid": "35563650", "veil": 0.5, "illus": VM,
     "kin": [{"text": "LAN KHÔNG GIỎI HƠN MINH", "at": 12}, {"text": "CHỈ SỚM HƠN 10 NĂM", "at": [12, "chỉ"], "acc": True},
             {"text": "quả cầu tuyết cần nhất là thời gian", "at": 13, "sm": True}]},
    {"type": "question", "at": 14, "text": "Bạn bắt đầu để dành\ntừ năm bao nhiêu tuổi?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 15}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [15, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
SPEC = {
    "title": "Lãi Kép: Nộp Ít Hơn Một Nửa Mà Cuối Cùng Có Nhiều Hơn? Phép Tính 3 Triệu Mỗi Tháng",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["lãi", "kép", "lan", "minh", "lạm", "phát", "ngược"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Lãi Kép: Nộp Ít Hơn Một Nửa Mà Cuối Cùng Có Nhiều Hơn? Phép Tính 3 Triệu Mỗi Tháng",
                   "3 Triệu Mỗi Tháng Trong 30 Năm Thành Bao Nhiêu? Lãi Kép, Và Thứ Lặng Lẽ Ăn Mòn Nó",
                   "Lãi Kép Là Gì? Năm Thứ 13, Tiền Lãi Bắt Đầu Vượt Tiền Bạn Nộp"],
        "summary": "Lan để dành 10 năm rồi dừng. Minh bắt đầu muộn 10 năm nhưng để dành suốt 20 năm, số tiền gấp đôi. Vì sao trong phép tính, "
                   "Lan lại có nhiều hơn? Video giải thích lãi kép bằng một ví dụ 3 triệu mỗi tháng, chỉ ra năm thứ mấy tiền lãi vượt tiền nộp, "
                   "rồi đặt cạnh hai con số thật của 8 năm qua: lạm phát và lãi tiền gửi sau lạm phát. Kèm phần lãi kép chạy ngược khi bạn "
                   "mang nợ, và khi nào phép tính này không đúng với bạn.",
        "more": [Y4["more"][0],
                 "📐 CÁCH KÊNH TÍNH: mọi con số của ví dụ dùng lãi suất GIẢ ĐỊNH 6%/năm, nhập gốc hằng tháng, nộp cuối tháng, lãi suất không đổi và "
                 "không rút — đây là phép tính, không phải mức lãi của sản phẩm nào và không phải dự báo. Lan, Minh là nhân vật giả định. Lạm phát ví "
                 "dụ 3,1%/năm = trung bình cộng CPI bình quân năm 2018–2025 (Cục Thống kê, qua báo chí). Số thật: tiền gửi 12 tháng ở nhóm ngân "
                 "hàng lớn, đáo hạn gửi tiếp từ 10/2018 tới 10/2026 ≈ ×1,56; giá cả cùng kỳ ≈ +29% → sau lạm phát ≈ ×1,21 (kênh tự tính từ biểu lãi "
                 "suất niêm yết qua báo chí, vài mốc suy từ tháng lân cận). Khoản nợ 25%/năm là ví dụ giả định, không gán cho loại vay nào."],
        "chapter_titles": {"ch00": "Mở đầu: câu đố Lan và Minh", "ch01": "Lãi đẻ ra lãi: lãi kép là gì", "ch02": "Năm thứ 13: khi tiền lãi vượt tiền nộp",
                           "ch03": "Lời giải cho Lan và Minh", "ch04": "Thứ lặng lẽ ăn mòn: lạm phát", "ch05": "Khi quả cầu tuyết lăn ngược: nợ",
                           "ch06": "Khi nào phép tính này không đúng với bạn"},
        "sources": ["https://topi.vn/ty-le-lam-phat-o-viet-nam-qua-cac-nam.html",
                    "https://vov.gov.vn/cpi-nam-2023-tang-325-lam-phat-co-ban-tang-416-dtnew-610891",
                    "https://baoquangninh.vn/cpi-binh-quan-nam-2024-tang-3-63-dat-muc-tieu-quoc-hoi-de-ra-3338442.html",
                    "https://www.vietnamplus.vn/toan-bo-big4-tiep-tuc-giam-lai-suat-huy-dong-cao-nhat-chi-con-53/901571.vnp",
                    "https://vneconomy.vn/lai-suat-tiet-kiem-ngan-hang-nao-cao-nhat-thang-92026.htm"],
        "hashtags": ["TàiChínhCáNhân", "LãiKép", "TiếtKiệm", "LạmPhát", "BiểuĐồBiếtNói"],
        "tags": ["lãi kép", "lãi kép là gì", "quy tắc 72", "để dành mỗi tháng", "tiết kiệm", "lạm phát", "lãi suất thực", "tài chính cá nhân",
                 "bắt đầu để dành sớm", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: phép tính lãi kép do kênh tự lập (ví dụ giả định); CPI bình quân năm theo Cục Thống kê (qua báo chí); lãi tiền gửi 12 "
                       "tháng theo biểu niêm yết được báo chí dẫn.",
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
