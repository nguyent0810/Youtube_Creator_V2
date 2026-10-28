"""Dựng cảnh cho ck-f1-tro-cap-that-nghiep. Số liệu chỉ lấy từ results.json."""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
V = R["assumption"]
BEN = R["monthly_benefit_million"]
SHORT = R["monthly_shortfall_million"]
DUR = R["duration"]
CAP = R["regional_caps_million"]
WAIT = R["waiting_days"]
RUN = R["cumulative_shortfall_million"]

VM = "VIDEO MINH HỌA"
ILL = "ẢNH MINH HỌA"
HYP = "VÍ DỤ GIẢ ĐỊNH"

SAY = {
    "bhtn": "bảo hiểm thất nghiệp", "bhxh": "bảo hiểm xã hội",
    "bhyt": "bảo hiểm y tế", "q h": "quốc hội", "nd-cp": "nghị định",
}

IMGS = {f"ai{i:02d}": f"EXT:ai:ai_{i:02d}" for i in range(1, 7)}

def photo(img, at, focus, move=None, reveal=None, zoom=None):
    s = {"type": "photo", "img": img, "at": at, "credit": False,
         "illus": ILL, "focus": focus}
    if move:
        s["move"] = move
    if reveal:
        s["reveal"] = reveal
    if zoom:
        s["zoom"] = zoom
    return s

LAW = "LUẬT VIỆC LÀM 74/2025/QH15 · HIỆU LỰC 01/01/2026"

def waterfall(at, title, end_at, cost_at=None):
    # 27/10 (Claude): thác đi từ CHI PHÍ 13 xuống, TRỢ CẤP 9 bù vào, còn THIẾU 4 -- số dương, "range" là chữ đầu biểu đồ
    return {"type": "waterfall", "at": at, "title": title, "range": "TRIỆU ĐỒNG · " + HYP, "unit": "TRIỆU",
            "start": {"k": "CHI PHÍ", "v": V["living_cost_million"], "at": cost_at if cost_at is not None else at},
            "steps": [{"k": "TRỢ CẤP BÙ", "v": -BEN, "at": end_at}],
            "end": {"k": "CÒN THIẾU", "at": end_at},
            "calls": [{"i": 2, "text": f"THIẾU {SHORT:g} TRIỆU", "at": end_at}]}

def race(at, title, vals, calls):
    return {"type": "race", "at": at, "abs": True, "unit": "TRIỆU", "xlab": "THÁNG ", "xstep": 1,
            "dates": [str(i) for i in range(1, len(vals) + 1)], "title": title, "range": "THIẾU CỘNG DỒN · " + HYP,
            "series": [{"label": "THIẾU CỘNG DỒN", "color": "#ef4444", "vals": vals}], "calls": calls}

CH = {}
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "TRỢ CẤP ĐỠ ĐƯỢC BAO LÂU"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    # 27/10 (Content Brief bản 2): mở bằng số thật, không nhân vật trong CH00
    {"type": "counter", "at": 0, "from": 0, "to": 332629, "label": "QUYẾT ĐỊNH HƯỞNG TRỢ CẤP THẤT NGHIỆP · 6 THÁNG ĐẦU 2026",
     "srcnote": "NGUỒN: BẢO HIỂM XÃ HỘI VIỆT NAM"},
    {"type": "bars", "at": 1, "title": "TRỢ CẤP MỖI THÁNG SO VỚI LƯƠNG ĐÓNG", "unit": "%", "srcnote": LAW,
     "items": [{"k": "BÌNH QUÂN LƯƠNG ĐÓNG 6 THÁNG", "v": 100, "lbl": "100%", "at": [1, "bình"]}, {"k": "TRỢ CẤP", "v": 60, "lbl": "60%", "at": [1, "sáu"], "acc": True}],
     "calls": [{"i": 1, "text": "60%", "at": [1, "sáu"]}]},
    {"type": "broll", "vid": "4068575", "at": 3, "veil": .55, "illus": VM,
     "kin": [{"text": "ĐÓNG NHIỀU NĂM", "at": 3, "sm": True}, {"text": "CÓ TRẦN · CÓ HẠN", "at": [3, "trần"], "acc": True}]},
    {"type": "question", "at": 4, "text": "Trợ cấp đỡ được\nbao nhiêu tháng?"},
    {"type": "bars", "at": 6, "title": "SỐ THÁNG HƯỞNG THEO SỐ NĂM ĐÓNG", "unit": "THÁNG", "srcnote": LAW,
     "items": [{"k": "ĐÓNG 3 NĂM", "v": 3, "lbl": "3", "at": [6, "bốn"]}, {"k": "ĐÓNG 6 NĂM", "v": 6, "lbl": "6", "at": [6, "ngày"]},
               {"k": "ĐÓNG 12 NĂM TRỞ LÊN", "v": DUR["cap_months"], "lbl": "12 (TỐI ĐA)", "at": [6, "bậc"], "acc": True}],
     "calls": [{"i": 2, "text": "TỐI ĐA 12", "at": [6, "bậc"]}]},
    {"type": "timeline", "at": 7, "title": "ĐƯỜNG ĐI CỦA MỘT HỒ SƠ", "items": [{"year": "LƯƠNG ĐÓNG", "text": "60%", "at": 7}, {"year": "4 CỬA", "text": "điều kiện", "at": [7, "bảy"]},
                                                                         {"year": "CHỜ", "text": "10 ngày làm việc", "at": [7, "tháng"]}, {"year": "HỞ", "text": "cộng dồn", "at": [7, "khoảng"]}]},
    {"type": "brand", "at": 8, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MỘT THÁNG ĐẦU TIÊN"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MỘT THÁNG\nĐẦU TIÊN", "sub": "CÔNG THỨC 60%", "vid": "8004282", "illus": VM, "titleAt": 0},
    photo("ai01", 1, [.30, .22], reveal={"kind": "circle", "at": 1, "d": .9}),
    {"type": "ledger", "at": 2, "title": "LUẬT VIỆC LÀM MỚI", "srcnote": LAW,
     "rows": [{"k": "HIỆU LỰC", "v": "01/01/2026", "at": 2}, {"k": "MỨC HƯỞNG", "v": "60% BÌNH QUÂN 6 THÁNG", "at": 3}]},
    {"type": "bars", "at": 5, "title": "PHÉP TÍNH CỦA CHỊ LAN", "unit": "TRIỆU · " + HYP, "items": [
      {"k": "LƯƠNG ĐÓNG", "v": V["insured_wage_million"], "lbl": "15", "at": 5}, {"k": "TRỢ CẤP 60%", "v": BEN, "lbl": "9", "at": 6, "acc": True},
      {"k": "CHI PHÍ", "v": V["living_cost_million"], "lbl": "13", "at": 7}],
      "calls": [{"i": 1, "text": "TRỢ CẤP 9", "at": 6}]},
    waterfall(9, "THÁC TIỀN THÁNG ĐẦU", 11, cost_at=10),
    photo("ai02", 13, [.62, .24], move="pan"),
    {"type": "bars", "at": 14, "title": "TRẦN TRỢ CẤP THEO VÙNG", "unit": "TRIỆU/THÁNG", "srcnote": LAW,
     "items": [{"k": "VÙNG I", "v": CAP["I"], "lbl": "26,55", "at": 14}, {"k": "VÙNG II", "v": CAP["II"], "lbl": "23,65", "at": 14},
               {"k": "VÙNG III", "v": CAP["III"], "lbl": "20,7", "at": 15}, {"k": "VÙNG IV", "v": CAP["IV"], "lbl": "18,5", "at": 15},
               {"k": "CHỊ LAN", "v": BEN, "lbl": "9", "at": [15, "chín"], "acc": True}],
     "calls": [{"i": 4, "text": "CHƯA CHẠM TRẦN", "at": [15, "chín"]}]},
    {"type": "question", "at": 16, "text": "Đồng hồ phải qua\nnhững cửa nào?"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BỐN CỬA TRƯỚC KHI ĐỒNG HỒ CHẠY"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "BỐN CỬA\nĐIỀU KIỆN", "sub": "HỒ SƠ ĐỦ MỚI MỞ ĐỒNG HỒ", "vid": "5434539", "illus": VM, "titleAt": 0},
    photo("ai03", 1, [.49, .20], move="pan"),
    {"type": "ledger", "at": 2, "title": "BỐN CỬA ĐIỀU KIỆN", "srcnote": LAW, "rows": [{"k": "1", "v": "CHẤM DỨT HỢP ĐỒNG ĐÚNG LUẬT", "at": 2}, {"k": "2", "v": "ĐÓNG ĐỦ 12 THÁNG / 24", "at": 3}, {"k": "3", "v": "NỘP HỒ SƠ TRONG 3 THÁNG", "at": 4}, {"k": "4", "v": "10 NGÀY CHỜ KHÔNG CÓ VIỆC", "at": 5}]},
    {"type": "bars", "at": 6, "title": "CỬA SỔ THỜI GIAN ĐÓNG", "unit": "THÁNG", "items": [{"k": "HỢP ĐỒNG THƯỜNG", "v": 24, "lbl": "24", "at": 6}, {"k": "ĐÓNG TỐI THIỂU", "v": 12, "lbl": "12", "at": 7}, {"k": "HỢP ĐỒNG NGẮN", "v": 36, "lbl": "36", "at": 8}], "calls": [{"i": 1, "text": "ĐỦ 12", "at": 7}]},
    {"type": "broll", "vid": "5434539", "at": 8, "veil": .55, "illus": VM},
    {"type": "timeline", "at": 9, "title": "CỬA THỨ TƯ: 10 NGÀY LÀM VIỆC", "items": [{"year": "3 THÁNG", "text": "hạn nộp hồ sơ", "at": 9}, {"year": "10 NGÀY", "text": "làm việc chờ", "at": [9, "mười"]}, {"year": "KHÔNG CÓ VIỆC", "text": "thuộc diện bắt buộc", "at": 10}]},
    {"type": "counter", "at": 12, "from": 0, "to": WAIT["current_law"], "suffix": " NGÀY", "label": "ĐIỂM BẮT ĐẦU", "sub": {"text": "SAU HỒ SƠ ĐỦ", "at": 12}},
    waterfall(13, "CỘT TRỢ CẤP CHƯA HIỆN", 15),
    {"type": "bars", "at": 15, "title": "ĐIỀU KIỆN VÀ KHOẢN TRỢ CẤP", "unit": "CỬA", "items": [{"k": "ĐỦ 4 CỬA", "v": 4, "lbl": "4", "at": 15, "acc": True}], "calls": [{"i": 0, "text": "ĐỦ BỐN", "at": 15}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "HỒ SƠ ĐỦ MỚI BẮT ĐẦU", "at": 17, "acc": True}]},
    {"type": "counter", "at": 18, "from": 0, "to": WAIT["waiting_period"], "suffix": " NGÀY", "label": "QUÃNG CHỜ", "sub": {"text": "SAU KHI NỘP ĐỦ", "at": 18}},
    {"type": "timeline", "at": 19, "title": "MỐC TIẾP THEO", "items": [{"year": "0", "text": "nộp đủ", "at": 19}, {"year": "10", "text": "ngày chờ", "at": 20}, {"year": "11", "text": "mốc hưởng", "at": 21}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "NGÀY THỨ MƯỜI MỘT"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "NGÀY THỨ\nMƯỜI MỘT", "sub": "SAU KHI HỒ SƠ ĐỦ", "vid": "7801968", "illus": VM, "titleAt": 0},
    photo("ai04", 1, [.50, .22], reveal={"kind": "wipe", "at": 1, "d": .9}),
    {"type": "timeline", "at": 2, "title": "TỪ NGÀY NỘP TỚI NGÀY HƯỞNG", "items": [{"year": "NGÀY 1", "text": "nộp đủ hồ sơ", "at": 2}, {"year": "10 NGÀY", "text": "làm việc chờ", "at": [2, "thứ"]}, {"year": "NGÀY 11", "text": "bắt đầu hưởng", "at": [2, "hưởng"]}]},
    {"type": "counter", "at": 4, "from": 0, "to": WAIT["waiting_period"], "suffix": " NGÀY", "label": "NGÀY KIỂM TRA", "sub": {"text": "TRƯỚC ĐIỂM HƯỞNG", "at": 4}},
    {"type": "bars", "at": 5, "title": "MỐC HƯỞNG CŨ VÀ MỚI", "unit": "NGÀY LÀM VIỆC", "items": [{"k": "LUẬT 2013", "v": WAIT["previous_law"], "lbl": "16", "at": 6}, {"k": "LUẬT 2025", "v": WAIT["current_law"], "lbl": "11", "at": 7, "acc": True}], "calls": [{"i": 1, "text": "GIẢM 5", "at": 7}]},
    {"type": "bars", "at": 8, "title": "CHÊNH LỆCH THỜI GIAN", "unit": "NGÀY", "items": [{"k": "RÚT NGẮN", "v": WAIT["previous_law"]-WAIT["current_law"], "lbl": "5", "at": 8, "acc": True}], "calls": [{"i": 0, "text": "GIẢM 5", "at": 8}]},
    {"type": "timeline", "at": 9, "title": "KHÔNG TỰ ĐIỀN NGÀY NHẬN", "items": [{"year": "THÁNG 11", "text": "nghỉ việc giả định", "at": 9}, {"year": "HỒ SƠ ĐỦ", "text": "mở đồng hồ", "at": 10}, {"year": "NGÀY 11", "text": "mốc hưởng", "at": 11}]},
    {"type": "broll", "vid": "6443909", "at": 12, "veil": .55, "illus": VM},
    waterfall(13, "SAU NGÀY 11, THÁC MỚI CÓ CỘT", 15),
    {"type": "counter", "at": 16, "from": 0, "to": WAIT["current_law"], "suffix": " NGÀY", "label": "MỐC THEO LUẬT MỚI", "sub": {"text": "KHÔNG PHẢI NGÀY NGHỈ", "at": 16}},
    {"type": "ledger", "at": 17, "title": "CÁC MỐC LUẬT", "rows": [{"k": "2013", "v": "KHUNG CŨ", "at": 17}, {"k": "2015", "v": "CÓ HIỆU LỰC", "at": 18}, {"k": "2026", "v": "KHUNG MỚI", "at": 19}]},
    {"type": "question", "at": 21, "text": "Bảy năm đóng\nđổi ra mấy tháng?"},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "BẢY NĂM ĐỔI THÀNH BẢY THÁNG"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "BẢY NĂM ĐÓNG\nBẢY THÁNG HƯỞNG", "sub": "VÍ DỤ 84 THÁNG", "vid": "8125994", "illus": VM, "titleAt": 0},
    photo("ai05", 1, [.48, .22], zoom={"x": .55, "y": .36, "z": 1.5, "at": 1, "d": 1.2}),
    {"type": "bars", "at": 2, "title": "TỪ THÁNG ĐÓNG SANG THÁNG HƯỞNG", "unit": "THÁNG · VÍ DỤ GIẢ ĐỊNH", "items": [{"k": "36 THÁNG ĐẦU", "v": DUR["first_36_paid_months"], "lbl": "3 HƯỞNG", "at": 4}, {"k": "48 THÁNG SAU", "v": DUR["extra_48_paid_months"], "lbl": "4 HƯỞNG", "at": 6}, {"k": "TỔNG", "v": DUR["total_months"], "lbl": "7", "at": 9, "acc": True}], "calls": [{"i": 2, "text": "TỔNG 7", "at": 9}]},
    {"type": "broll", "vid": "8125994", "at": 10, "veil": .55, "illus": VM},
    {"type": "bars", "at": 11, "title": "THỜI GIAN HƯỞNG VÀ TRẦN", "unit": "THÁNG", "items": [{"k": "VÍ DỤ", "v": DUR["total_months"], "lbl": "7", "at": 11}, {"k": "TRẦN", "v": DUR["cap_months"], "lbl": "12", "at": 14}], "calls": [{"i": 0, "text": "CÒN 5", "at": 14}]},
    {"type": "waterfall", "at": 15, "title": "7 THÁNG CÒN CÁCH TRẦN", "range": HYP, "unit": "THÁNG", "start": {"k": "ĐÃ HƯỞNG", "v": DUR["total_months"], "at": 15}, "steps": [{"k": "CÒN LẠI", "v": DUR["cap_months"]-DUR["total_months"], "at": 15}], "end": {"k": "TRẦN", "at": 15}, "calls": [{"i": 1, "text": "CÒN 5", "at": 15}]},
    race(16, "KHOẢN THIẾU TỚI THÁNG 7", RUN[:4], [{"i": 0, "text": "BẮT ĐẦU 4", "at": 16}, {"i": 3, "text": "THÁNG 4: 16", "at": 18}]),
    {"type": "bars", "at": 19, "title": "DÒNG TIỀN 7 THÁNG", "unit": "TRIỆU · VÍ DỤ GIẢ ĐỊNH", "items": [{"k": "MỖI THÁNG", "v": BEN, "lbl": "9", "at": 19}, {"k": "7 THÁNG", "v": R["total_benefit_million"], "lbl": "63", "at": 19, "acc": True}], "calls": [{"i": 1, "text": "TỔNG 63", "at": 19}]},
    {"type": "counter", "at": 20, "from": 0, "to": R["total_benefit_million"], "suffix": " TRIỆU", "label": "7 THÁNG × 9 TRIỆU · VÍ DỤ GIẢ ĐỊNH", "sub": {"text": "KHÔNG PHẢI BẢY NĂM LƯƠNG", "at": 21}},
    waterfall(22, "MỖI THÁNG VẪN THIẾU 4", 23),
    {"type": "kinetic", "at": 23, "items": [{"text": "CẦN KIỂM TRA ĐƯỜNG TRẦN", "at": 23, "acc": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "ĐƯỜNG TRẦN Ở BỐN VÙNG"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "ĐƯỜNG TRẦN\nỞ BỐN VÙNG", "sub": "5 LẦN LƯƠNG TỐI THIỂU", "vid": "5439068", "illus": VM, "titleAt": 0},
    {"type": "bars", "at": 1, "title": "LƯƠNG TỐI THIỂU VÙNG TỪ 01/01/2026", "unit": "TRIỆU/THÁNG", "srcnote": "NGUỒN: MỨC LƯƠNG TỐI THIỂU VÙNG 2026",
     "items": [{"k": "VÙNG I", "v": 5.31, "lbl": "5,31", "at": 1}, {"k": "VÙNG II", "v": 4.73, "lbl": "4,73", "at": 2},
               {"k": "VÙNG III", "v": 4.14, "lbl": "4,14", "at": 3}, {"k": "VÙNG IV", "v": 3.70, "lbl": "3,70", "at": [3, "còn"]}],
     "calls": [{"i": 0, "text": "CAO NHẤT", "at": 1}]},
    {"type": "bars", "at": 4, "title": "TRẦN TRỢ CẤP = 5 × LƯƠNG TỐI THIỂU", "unit": "TRIỆU/THÁNG", "srcnote": LAW,
     "items": [{"k": "VÙNG I", "v": CAP["I"], "lbl": "26,55", "at": 5}, {"k": "VÙNG II", "v": CAP["II"], "lbl": "23,65", "at": 6},
               {"k": "VÙNG III", "v": CAP["III"], "lbl": "20,7", "at": 7}, {"k": "VÙNG IV", "v": CAP["IV"], "lbl": "18,5", "at": [7, "và"]}],
     "calls": [{"i": 3, "text": "THẤP NHẤT 18,5", "at": [7, "và"]}]},
    {"type": "bars", "at": 8, "title": "9 TRIỆU CẠNH TRẦN THẤP NHẤT", "unit": "TRIỆU · " + HYP,
     "items": [{"k": "TRỢ CẤP CHỊ LAN", "v": BEN, "lbl": "9", "at": 8, "acc": True}, {"k": "TRẦN VÙNG IV", "v": CAP["IV"], "lbl": "18,5", "at": [8, "dưới"]}],
     "calls": [{"i": 0, "text": "CHƯA CHẠM TRẦN", "at": 9}]},
    photo("ai05", 10, [.47, .22], move="out"),
    waterfall(12, "TRẦN KHÔNG XOÁ KHOẢN THIẾU", 13),
    {"type": "broll", "vid": "5439068", "at": 15, "veil": .55, "illus": VM},
    {"type": "kinetic", "at": 16, "items": [{"text": "CÓ ĐỆM KHÁC KHÔNG?", "at": 16, "acc": True}, {"text": "video này chỉ theo trợ cấp", "at": 17, "sm": True}]},
    race(18, "ĐƯỜNG THIẾU VẪN TĂNG", RUN[:5], [{"i": 4, "text": "THÁNG 5: 20", "at": [18, "theo"]}]),
    {"type": "question", "at": 19, "text": "Đến tháng cuối,\nkhoản thiếu là bao nhiêu?"},
]}

CH["ch06"] = {"hud": {"k": "PHẦN CUỐI", "t": "THÁNG CUỐI VÀ ĐIỂM DỪNG"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    # 27/10 (Claude): dựng lại -- neo cũ lệch sau khi W1-1b thêm câu
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "THÁNG CUỐI\nVÀ ĐIỂM DỪNG", "sub": "ĐƯỜNG THIẾU TỚI 28 TRIỆU", "vid": "9841386", "illus": VM, "titleAt": 0},
    race(1, "THIẾU CỘNG DỒN TỪNG THÁNG", RUN[:4], [{"i": 1, "text": "THÁNG 2: 8", "at": 1}, {"i": 3, "text": "THÁNG 4: 16", "at": [2, "bốn"]}]),
    photo("ai06", 3, [.50, .21], move="in"),
    {"type": "bars", "at": 4, "title": "BA THÁNG CUỐI", "unit": "TRIỆU THIẾU · " + HYP,
     "items": [{"k": "THÁNG 5", "v": RUN[4], "lbl": "20", "at": 4}, {"k": "THÁNG 6", "v": RUN[5], "lbl": "24", "at": 5}, {"k": "THÁNG 7", "v": RUN[6], "lbl": "28", "at": 6, "acc": True}],
     "calls": [{"i": 2, "text": "28 TRIỆU", "at": 6}]},
    {"type": "counter", "at": 7, "from": 0, "to": RUN[6], "suffix": " TRIỆU", "label": "4 TRIỆU × 7 THÁNG", "sub": {"text": HYP, "at": 7}},
    {"type": "ledger", "at": 8, "title": "NGOÀI CỘT 9 TRIỆU", "srcnote": LAW,
     "rows": [{"k": "BẢO HIỂM Y TẾ", "v": "QUỸ BHTN ĐÓNG THAY", "at": 8}, {"k": "LÀ QUYỀN LỢI", "v": "KHÔNG CỘNG VÀO 9 TRIỆU", "at": 9}]},
    {"type": "counter", "at": 10, "from": 0, "to": 332629, "label": "QUYẾT ĐỊNH HƯỞNG · 6 THÁNG ĐẦU 2026",
     "sub": {"text": "TOÀN HỆ THỐNG · KHÔNG PHẢI SỐ NGƯỜI", "at": 11}, "srcnote": "NGUỒN: BẢO HIỂM XÃ HỘI VIỆT NAM"},
    {"type": "broll", "vid": "9841386", "at": 12, "veil": .55, "illus": VM, "kin": [{"text": "ĐIỂM DỪNG SỚM", "at": 12, "acc": True}]},
    {"type": "timeline", "at": 13, "title": "KHI CÓ VIỆC LÀM", "items": [{"year": "CÓ VIỆC", "text": "đang hưởng", "at": 13},
                                                                    {"year": "3 NGÀY", "text": "phải thông báo", "at": [13, "ba"]},
                                                                    {"year": "≥ 1 THÁNG", "text": "hợp đồng = có việc", "at": 14}]},
    race(15, "NẾU CÓ VIỆC Ở THÁNG 5", RUN[:5], [{"i": 4, "text": "DỪNG Ở THÁNG 5", "at": [15, "năm"]}]),
    {"type": "ledger", "at": 16, "title": "CÁC ĐIỂM CHẤM DỨT KHÁC", "srcnote": LAW,
     "rows": [{"k": "1", "v": "TỰ ĐỀ NGHỊ CHẤM DỨT", "at": 16}, {"k": "2", "v": "CÓ VIỆC CÓ BẢO HIỂM BẮT BUỘC", "at": [16, "việc"]},
              {"k": "3", "v": "TỪ CHỐI VIỆC 2 LẦN", "at": 17}]},
    photo("ai03", 18, [.40, .24], move="pan"),
    waterfall(20, "VÒNG KHÉP LẠI: 13 − 9 = 4", 21, cost_at=20),
    race([21, "bảy"], "THIẾU CỘNG DỒN TỚI THÁNG 7", RUN, [{"i": 6, "text": "THÁNG 7: 28", "at": [21, "thành"]}]),
    {"type": "timeline", "at": 22, "title": "ĐỒNG HỒ TRỢ CẤP", "items": [{"year": "4 CỬA", "text": "điều kiện", "at": 22}, {"year": "10 NGÀY", "text": "chờ", "at": [22, "mười"]},
                                                                      {"year": "7 THÁNG", "text": "hưởng", "at": [22, "bảy"]}, {"year": "DỪNG", "text": "khi có việc", "at": [22, "dừng"]}]},
    {"type": "kinetic", "at": 23, "items": [{"text": "HIỂU QUYỀN LỢI CỦA MÌNH", "at": 23, "acc": True}, {"text": "trước khi nộp hồ sơ", "at": 23, "sm": True}]},
]}

SOURCES = [
 "https://vanban.chinhphu.vn/?classid=1&docid=214560&pageid=27160",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/hoat-dong-bhxh-viet-nam.aspx?CateID=0&ItemID=25249",
 "https://chinhsachonline.chinhphu.vn/bon-dieu-kien-huong-tro-cap-that-nghiep-tu-2026-83780.htm",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/linh-vuc-bao-hiem-xa-hoi.aspx?CateID=0&ItemID=25791",
 "https://vbpl.moj.gov.vn/bonoivu/Pages/vbpq-vanbanlienquan.aspx?ItemID=179273&Keyword=&dvid=320",
 "https://vanban.chinhphu.vn/?docid=215832&pageid=27160",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/linh-vuc-bao-hiem-y-te.aspx?CateID=0&ItemID=26844",
 "https://baohiemxahoi.gov.vn/tintuc/pages/linh-vuc-bao-hiem-xa-hoi.aspx?CateID=168&ItemID=27245",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/cai-cach-chinh-sach-bhxh.aspx?CateID=0&ItemID=25208",
]
TITLE = "Nghỉ Việc Lương 15 Triệu: Trợ Cấp Thất Nghiệp Mấy Tháng?"   # Content Brief bản 2 (27/10)
SPEC = {"title": TITLE, "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True, "chart_rules": True, "acc": ["trợ", "cấp", "thiếu", "tháng", "triệu"], "say": SAY, "imgs": IMGS, "chapters": [f"ch{i:02d}" for i in range(7)], "youtube": {"titles": [TITLE, "Mất Việc Năm 2026: Trợ Cấp Đỡ Bạn Được Bao Lâu?", "Hơn 330 Nghìn Người Nhận Trợ Cấp Thất Nghiệp: Đủ Sống Không?"], "publish_at": "2026-11-18T13:00:00Z", "playlist": "Tiền Bạc 2026 Nói Gì", "summary": "Sáu tháng đầu năm 2026 có hơn 330 nghìn quyết định hưởng trợ cấp thất nghiệp. Nhưng trợ cấp chỉ bằng 60% bình quân lương đóng, có trần theo vùng và chạy trong số tháng giới hạn. Video dùng biểu đồ đi qua Luật Việc làm 2025: bốn điều kiện, ngày chờ, số tháng hưởng theo năm đóng, trần theo vùng, rồi đặt trợ cấp cạnh chi phí sống trong một ví dụ giả định để thấy khoản hở cộng dồn.", "more": ["Nội dung giáo dục, không phải tư vấn đầu tư. Mọi số tiền của chị Lan là VÍ DỤ GIẢ ĐỊNH để minh họa công thức; quyền lợi thực tế phụ thuộc hồ sơ, thời điểm và khu vực."], "chapter_titles": {"ch00": "Mở đầu: hơn 330 nghìn quyết định trợ cấp", "ch01": "Một tháng đầu tiên", "ch02": "Bốn cửa trước khi đồng hồ chạy", "ch03": "Ngày thứ mười một", "ch04": "Bảy năm đổi thành bảy tháng", "ch05": "Đường trần ở bốn vùng", "ch06": "Tháng cuối và điểm dừng"}, "sources": SOURCES, "hashtags": ["TrợCấpThấtNghiệp", "TàiChínhCáNhân", "BiểuĐồBiếtNói"], "tags": ["trợ cấp thất nghiệp", "bảo hiểm thất nghiệp", "tài chính cá nhân", "quyền lợi người lao động"], "category": "27", "thumb": "t1.jpg", "data_credit": "Quy định từ các nguồn công khai; các phép tính của chị Lan là ví dụ giả định.", "video_credits": "Video minh họa: Pexels. Ảnh minh họa: AI."}}

def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, chapter in CH.items():
        path = D / f"{name}.json"
        old = json.loads(path.read_text(encoding="utf-8"))
        old.update(chapter)
        path.write_text(json.dumps(old, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")

if __name__ == "__main__":
    main()
