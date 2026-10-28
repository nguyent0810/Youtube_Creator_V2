"""Dựng cảnh cho CK I1; toàn bộ chuỗi đường đua lấy từ results.json."""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
M = R["monthly"]
SRC = "DỮ LIỆU: HOSE QUA VNSTOCK · KÊNH TỰ TÍNH · VÍ DỤ GIẢ ĐỊNH 100 TRIỆU"
VIDS = ["39600116", "6963484", "7688068", "32347897", "8951964", "6964247", "7651886", "33585547"]

N = len(M["iso"])
LAST = N - 1
COL = {"tiet_kiem_6": ("TIẾT KIỆM 6%", "#22c55e"), "mot_lan": ("BỎ MỘT LẦN", "#ef4444"), "mua_deu": ("MUA ĐỀU", "#38bdf8"),
       "tiet_kiem_5": ("TIẾT KIỆM 5%", "#166534"), "tiet_kiem_7": ("TIẾT KIỆM 7%", "#86efac")}

def race(at, n, keys, title, calls):
    """keys: thứ tự series; calls: [(chỉ số series, tháng, nhãn, at)] -- dữ liệu lấy từ results.json."""
    return {"type": "race", "at": at, "abs": True, "unit": "TRIỆU ĐỒNG", "xlab": "THÁNG ", "xstep": 12,
            "dates": M["iso"][:n], "title": title, "range": SRC,
            "series": [{"label": COL[k][0], "color": COL[k][1], "vals": M[k][:n]} for k in keys],
            "calls": [{"s": a, "i": b, "text": t, "at": c} for a, b, t, c in calls]}

def candle(at, start, end, text):
    return {"type": "candles", "at": at, "series": "vnindex", "from": start, "to": end,
            "title": f"VN-INDEX · {start[5:7]}/{start[:4]}–{end[5:7]}/{end[:4]}", "range": "DỮ LIỆU: HOSE QUA VNSTOCK",
            "calls": [{"i": -1, "text": text, "at": at}]}

def broll(at, i, text):
    return {"type": "broll", "at": at, "vid": VIDS[i], "loop": True, "veil": 0.56,
            "illus": "VIDEO MINH HỌA", "kin": [{"text": text, "at": at, "acc": True}]}

def bars(at, title, items, unit="TRIỆU ĐỒNG", source=SRC):
    return {"type": "bars", "at": at, "title": title, "unit": unit, "srcnote": source,
            "items": [{"k": k, "v": v, "lbl": l, "at": a, **({"acc": True} if acc else {})} for k, v, l, a, acc in items]}

def kin(at, big, small, at2=None):
    return {"type": "kinetic", "at": at, "items": [{"text": big, "at": at, "acc": True}, {"text": small, "at": at2 if at2 is not None else at, "sm": True}]}

def ledger(at, title, rows, src=SRC):
    return {"type": "ledger", "at": at, "title": title, "srcnote": src, "rows": [{"k": k, "v": v, "at": a} for k, v, a in rows]}

def chap(no, word, title, sub, vid):
    return {"type": "chapter", "no": no, "k": f"CHƯƠNG {word}" if no != "6" else "PHẦN CUỐI", "title": title, "sub": sub,
            "vid": vid, "illus": "VIDEO MINH HỌA", "titleAt": 0}

CPI = "NGUỒN: CỤC THỐNG KÊ"
IDX = "DỮ LIỆU: HOSE QUA VNSTOCK"
ML, MD, T6 = R["mot_lan"], R["mua_deu"], R["tiet_kiem"]
RC = {r["date"]: r for r in R["race"]}
PICES = [f"T{int(d[5:7])}/{d[2:4]}" for d in M["iso"][:24]]

CH = {
"ch00": {"hud": {"k": "MỞ ĐẦU", "t": "ĐỈNH CAO VÀ CÂU HỎI KHÓ"}, "bgm": {"mood": "mystery", "gain": .10}, "scenes": [
    {"type": "counter", "at": 0, "from": 0, "to": 1204, "suffix": " ĐIỂM", "label": "VN-INDEX ĐÓNG CỬA · 09/04/2018",
     "sub": {"text": "1.204,33 ĐIỂM", "at": 0}, "srcnote": IDX},
    race(1, N, ["mot_lan"], "100 TRIỆU BỎ MỘT LẦN TỪ 09/04/2018",
         [(0, 0, "100 TRIỆU", 1), (0, 23, "TỪNG CÒN 54,5", 2), (0, LAST, "CUỐI: 145,5", 3)]),
    kin(4, "NGHỊCH LÝ", "kết quả cuối xanh, đoạn giữa rất khó chịu", 5),
    ledger(6, "VN-INDEX TRONG VIDEO NÀY", [("CỔ TỨC", "KHÔNG CỘNG", 6), ("MUA TRỰC TIẾP", "KHÔNG ĐƯỢC", 7), ("VAI TRÒ", "THƯỚC ĐO GIÁ", 8)], IDX),
    broll(9, 1, "VÍ DỤ GIẢ ĐỊNH · ĐÃ TÍNH PHÍ VÀ THUẾ"),
    race(11, N, ["tiet_kiem_6", "mot_lan"], "NẾU CHỈ GỬI TIẾT KIỆM",
         [(0, LAST, "SỔ 6%: 164", 11), (1, LAST, "ĐÚNG ĐỈNH: 145", 12)]),
    {"type": "question", "at": 13, "text": "CÁCH NÀO CÒN NHIỀU NHẤT?\nCÁCH NÀO KHÓ CHỊU NHẤT?"},
    {"type": "brand", "at": 14, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]},
"ch01": {"hud": {"k": "CHƯƠNG 01", "t": "BA LUẬT CHƠI"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    chap("1", "MỘT", "BA LUẬT CHƠI\nMỘT KHOẢN TIỀN", "VÍ DỤ GIẢ ĐỊNH 100 TRIỆU", "37165260"),
    broll(2, 2, "LUẬT 1 · GỬI 12 THÁNG RỒI TÁI TỤC"),
    bars(3, "LÃI 12 THÁNG GIẢ ĐỊNH", [("5%", 5, "5%", 5, False), ("6% · ĐƯỜNG CHÍNH", 6, "6%", 4, True), ("7%", 7, "7%", 5, False)],
         "% MỖI NĂM", "VÍ DỤ GIẢ ĐỊNH · DẢI LÃI KÊNH GHI LẠI 2018–2026"),
    kin(6, "GIẢ ĐỊNH ĐỂ TÍNH", "không phải lãi của một ngân hàng nào"),
    {"type": "timeline", "at": 7, "title": "LUẬT 2 · BỎ MỘT LẦN", "items": [
        {"year": "09/04/2018", "text": "100 triệu vào chỉ số", "at": 7}, {"year": "KHI MUA", "text": "phí 0,15%", "at": 8},
        {"year": "KHI BÁN", "text": "phí 0,15% + thuế 0,1%", "at": 9}]},
    ledger(10, "GIÁ TRỊ MỞ ĐẦU", [("VÀO TIỀN", "100 TRIỆU", 10), ("SAU PHÍ", "≈ 99,6 TRIỆU", 10), ("PHÍ", "CÓ NGAY TỪ ĐẦU", 11)]),
    bars(12, "LUẬT 3 · CHIA 24 PHẦN", [("TỔNG", 100, "100", 12, False), ("MỖI THÁNG", MD["piece_million"], "4,17", 13, True)]),
    {"type": "heat", "at": 14, "title": "24 LẦN MUA ĐỀU · 04/2018–03/2020", "range": "VÍ DỤ GIẢ ĐỊNH · PHIÊN ĐẦU MỖI THÁNG",
     "unit": "TRIỆU", "cols": 6, "cells": [{"k": k, "v": MD["piece_million"]} for k in PICES],
     "total": {"label": "ĐÃ GÓP", "at": 15}, "calls": [{"i": 23, "text": "LẦN 24", "at": 15}]},
    broll(16, 3, "KHÔNG PHẢI LỊCH SỬ GIAO DỊCH CỦA AI"),
    race(18, 24, ["tiet_kiem_6", "mot_lan", "mua_deu"], "BA LUẬT · CÙNG MỘT DỮ LIỆU GIÁ",
         [(1, 23, "BỎ MỘT LẦN", 19), (2, 23, "MUA ĐỀU", [19, "biến"])]),
]},
"ch02": {"hud": {"k": "CHƯƠNG 02", "t": "ĐOẠN RƠI SÂU"}, "bgm": {"mood": "mystery", "gain": .10}, "scenes": [
    chap("2", "HAI", "ĐOẠN RƠI\nKẾT QUẢ CUỐI CHE MẤT", "COVID · 03/2020", "10603138"),
    candle(1, "2019-12-02", "2020-03-24", "659,21 · 24/03/2020"),
    bars(2, "SO VỚI ĐIỂM VÀO", [("09/04/2018", 1204.33, "1.204", 2, False), ("24/03/2020", 659.21, "659 · −45,3%", 2, True)], "ĐIỂM", IDX),
    {"type": "waterfall", "at": 3, "title": "BỎ MỘT LẦN Ở ĐÁY", "range": SRC, "unit": "TRIỆU",
     "start": {"k": "VÀO TIỀN", "v": 100, "at": 3}, "steps": [{"k": "GIÁ GIẢM + PHÍ", "v": round(ML["low_million"] - 100, 2), "at": 3}],
     "end": {"k": "CÒN LẠI", "at": 4, "tone": "down"}, "calls": [{"i": 2, "text": "ĐÁY 54,52", "at": 4}]},
    kin(5, "CÚ RƠI SÂU", "kết quả cuối không kể hết", 6),
    ledger(7, "CHƯA ĐƯỢC TÍNH", [("BẢN CHẤT", "VÍ DỤ GIẢ ĐỊNH", 7), ("KHỚP LỆNH THẬT", "CHÊNH LỆCH GIÁ", 8)]),
    {"type": "timeline", "at": 9, "title": "LỊCH GÓP CỦA NGƯỜI MUA ĐỀU", "items": [
        {"year": "04/2018", "text": "lần 1", "at": 9}, {"year": "02/03/2020", "text": "lần 24, góp đủ", "at": 9},
        {"year": "24/03/2020", "text": "đáy, sau khi góp đủ", "at": 10}]},
    bars(11, "CÙNG NGÀY 24/03/2020", [("BỎ MỘT LẦN", ML["low_million"], "54,52", 11, False), ("MUA ĐỀU", MD["low_after_full_million"], "67,68", 11, True)]),
    race(13, 24, ["mot_lan", "mua_deu"], "MUA SAU KHI GIÁ ĐÃ GIẢM", [(1, 23, "MUA ĐỀU 68", 13)]),
    broll(14, 4, "KHÔNG XOÁ ĐƯỢC RỦI RO"),
    bars(16, "CPI BÌNH QUÂN NĂM 2020", [("2020", 3.23, "3,23%", 16, True)], "PHẦN TRĂM", CPI),
    broll(17, 5, "GIÁ CẢ VẪN ĐI TIẾP"),
    {"type": "question", "at": 20, "text": "BẠN CÓ GIỮ ĐƯỢC\nMỘT PHÉP TÍNH ĐANG ĐỎ?"},
]},
"ch03": {"hud": {"k": "CHƯƠNG 03", "t": "KHI ĐƯỜNG GIÁ QUAY LÊN"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    chap("3", "BA", "KHI ĐƯỜNG GIÁ\nQUAY LÊN", "PHỤC HỒI 2020–2021", "33646292"),
    candle(1, "2020-10-01", "2021-12-31", "1.498,28 · CUỐI 2021"),
    bars(2, "HAI PHIÊN CUỐI NĂM", [("CUỐI 2020", 1103.87, "1.104", 2, False), ("CUỐI 2021", 1498.28, "1.498", 3, True)], "ĐIỂM", IDX),
    race(4, 45, ["mot_lan"], "ĐƯỜNG BỎ MỘT LẦN ĐẾN CUỐI 2021", [(0, 44, "123,91", 4), (0, 36, "VỀ 100 · 01/04/2021", 5)]),
    kin(6, "CÁC THÁNG CŨ VẪN CÒN ĐÓ", "chỉ là lúc con số đi qua điểm xuất phát", 7),
    {"type": "timeline", "at": 8, "title": "HAI NGÀY VỀ LẠI 100 TRIỆU", "items": [
        {"year": "19/11/2020", "text": "mua đều", "at": 8}, {"year": "01/04/2021", "text": "bỏ một lần", "at": 9}]},
    race(10, 45, ["mot_lan", "mua_deu"], "CUỐI 2021 · HAI CÁCH NẠP TIỀN", [(1, 44, "MUA ĐỀU 153,84", 10)]),
    ledger(11, "HAI ĐƯỜNG NÀY", [("BẢN CHẤT", "VÍ DỤ GIẢ ĐỊNH", 11), ("CỔ TỨC", "KHÔNG CỘNG THÊM", 12)]),
    bars(13, "CPI BÌNH QUÂN", [("2020", 3.23, "3,23%", 13, False), ("2021", 1.84, "1,84%", 13, True)], "PHẦN TRĂM", CPI),
    broll(15, 6, "2026: MỚI CÓ CPI CHÍN THÁNG"),
    kin(17, "THIẾU DỮ LIỆU PHẢI NÓI THIẾU", "không kéo dài đường bằng một dự đoán", 18),
    {"type": "question", "at": 19, "text": "HỒI PHỤC CÓ PHẢI\nLỜI HỨA KHÔNG?"},
]},
"ch04": {"hud": {"k": "CHƯƠNG 04", "t": "ĐỈNH MỚI, LẦN THỬ MỚI"}, "bgm": {"mood": "mystery", "gain": .10}, "scenes": [
    chap("4", "BỐN", "ĐỈNH MỚI\nLẦN THỬ MỚI", "2022 · GIẢM SÂU LẦN NỮA", "3066241"),
    candle(1, "2021-09-01", "2022-01-06", "ĐỈNH 1.528,57"),
    race(2, 46, ["mot_lan", "mua_deu"], "TẠI ĐỈNH 06/01/2022",
         [(0, 45, f'{RC["2022-01-06"]["mot_lan"]:.2f}'.replace(".", ","), 2), (1, 45, f'{RC["2022-01-06"]["mua_deu"]:.2f}'.replace(".", ","), 3)]),
    broll(4, 7, "MỌI THỨ TRÔNG ỔN"),
    candle(6, "2022-01-04", "2022-11-15", "911,90 · 15/11/2022"),
    bars(7, "ĐỈNH VÀ ĐÁY 2022", [("06/01/2022", 1528.57, "1.529", 7, False), ("15/11/2022", 911.90, "912 · −40,35%", 7, True)], "ĐIỂM", IDX),
    bars(8, "GIÁ TRỊ Ở ĐÁY 15/11/2022", [("BỎ MỘT LẦN", RC["2022-11-15"]["mot_lan"], "75,42", 8, False),
                                         ("MUA ĐỀU", RC["2022-11-15"]["mua_deu"], "93,63", 9, True)]),
    kin(10, "ÍT RƠI HƠN ≠ KHÔNG RƠI", "không cách nào luôn tốt hơn", 11),
    broll(12, 0, "HAI QUY TẮC · CÁC PHIÊN ĐÃ XẢY RA"),
    bars(13, "CPI BÌNH QUÂN NĂM 2022", [("2022", 3.15, "3,15%", 13, True)], "PHẦN TRĂM", CPI),
    race(14, 56, ["tiet_kiem_6", "mot_lan", "mua_deu"], "SỔ TIẾT KIỆM KHÔNG CÓ NGÀY ĐỎ",
         [(0, 55, "SỔ ≈ 131 · 11/2022", 15)]),
    {"type": "question", "at": 16, "text": "CẦM CHỨNG KHOÁN\nMÀ THUA NGƯỜI ĐỨNG YÊN?"},
]},
"ch05": {"hud": {"k": "CHƯƠNG 05", "t": "SỔ TIẾT KIỆM THẮNG Ở ĐÂU"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    chap("5", "NĂM", "SỔ TIẾT KIỆM\nTHẮNG Ở ĐÂU, THUA Ở ĐÂU", "DẢI LÃI 5–7% GIẢ ĐỊNH", "29538541"),
    race(1, N, ["tiet_kiem_6", "mot_lan", "mua_deu"], "ĐỦ BA ĐƯỜNG · 04/2018–10/2026", [(0, LAST, "SỔ 6%: 164", 1)]),
    bars(2, "ĐÚNG ĐỈNH VS SỔ TIẾT KIỆM", [("BỎ MỘT LẦN", ML["end_million"], "145,48", 2, False),
                                         ("TIẾT KIỆM 6%", T6["tiet_kiem_6"]["end_million"], "164,15 · HƠN ≈ 19", 2, True)]),
    kin(3, "MUA ĐÚNG ĐỈNH VẪN CÓ LÃI", "nhưng thua một cuốn sổ không bao giờ đỏ", 4),
    bars(5, "NGƯỜI MUA ĐỀU VƯỢT SỔ", [("TIẾT KIỆM 6%", T6["tiet_kiem_6"]["end_million"], "164,15", 5, False),
                                     ("MUA ĐỀU", MD["end_million"], "180,61", 5, True)]),
    bars(6, "ĐỔI LÃI SUẤT GIẢ ĐỊNH", [("5%", T6["tiet_kiem_5"]["end_million"], "151,43", 6, False), ("6%", T6["tiet_kiem_6"]["end_million"], "164,15", 6, False),
                                     ("7%", T6["tiet_kiem_7"]["end_million"], "177,82", 7, True), ("MUA ĐỀU", MD["end_million"], "180,61", 7, False)],
         source="VÍ DỤ GIẢ ĐỊNH · KHÔNG PHẢI LÃI CỦA NGÂN HÀNG NÀO"),
    broll(8, 3, "THỨ HẠNG PHỤ THUỘC LÃI BẠN NHẬN"),
    bars(9, "LÃI 12 THÁNG KÊNH GHI LẠI", [("ĐẦU 2018", 6.5, "≈ 6,5%", 10, False), ("ĐẦU 2024", 5.0, "≈ 5%", 11, True)], "% MỖI NĂM",
         "MỐC THAM KHẢO · KÊNH TỔNG HỢP TỪ BÁO CHÍ"),
    race(12, N, ["tiet_kiem_7", "tiet_kiem_6", "tiet_kiem_5"], "MỘT DẢI, KHÔNG PHẢI MỘT ĐƯỜNG",
         [(0, LAST, "7%: 178", 12), (2, LAST, "5%: 151", [12, "đường"])]),
    broll(13, 4, "LẠM PHÁT ĂN VÀO CẢ BA"),
    bars(14, "CPI BÌNH QUÂN", [("2023", 3.25, "3,25%", 14, False), ("2024", 3.63, "3,63%", [14, "bốn"], True)], "PHẦN TRĂM", CPI),
    {"type": "question", "at": 15, "text": "ĐỔI GIẢ ĐỊNH\nĐỔI KẾT QUẢ?"},
]},
"ch06": {"hud": {"k": "PHẦN CUỐI", "t": "KẾT QUẢ KHÔNG PHẢI MỆNH LỆNH"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    chap("6", "", "KẾT QUẢ CUỐI\nKHÔNG PHẢI MỆNH LỆNH", "PHIÊN CUỐI 06/10/2026", "25392214"),
    candle(1, "2026-06-01", "2026-10-06", "1.759,08 · 06/10/2026"),
    race(2, N, ["tiet_kiem_6", "mot_lan", "mua_deu"], "PHIÊN CUỐI CỦA DỮ LIỆU", [(1, LAST, "145,48", 2), (2, LAST, "180,61", 3)]),
    kin(4, "QUÁ KHỨ ≠ DỰ BÁO", "dữ liệu dừng ở 06/10/2026", 5),
    broll(6, 0, "KHÔNG PHẢI LỜI KHUYÊN MUA, BÁN HAY GỬI"),
    race(7, N, ["mot_lan", "mua_deu"], "CẢ HAI TỪNG DƯỚI 100 TRIỆU", [(0, 23, "ĐÁY 54,52", 9), (1, 23, "ĐÁY 67,68", [9, "sáu"])]),
    bars(10, "ĐÁY TỪNG CÁCH", [("BỎ MỘT LẦN", ML["low_million"], "54,52", 10, False), ("MUA ĐỀU", MD["low_after_full_million"], "67,68", 10, False),
                              ("TIẾT KIỆM 6%", 100, "KHÔNG DƯỚI 100", 11, True)]),
    bars(12, "KẾT QUẢ CUỐI", [("BỎ MỘT LẦN", ML["end_million"], "145,48", 12, False), ("TIẾT KIỆM 6%", T6["tiet_kiem_6"]["end_million"], "164,15", 12, True),
                             ("MUA ĐỀU", MD["end_million"], "180,61", 12, False)]),
    ledger(13, "TRONG PHÉP TÍNH", [("CỔ TỨC", "CHƯA CỘNG", 13), ("THUẾ 0,1% + PHÍ", "ĐÃ TRỪ", 14)]),
    broll(15, 2, "QUÁ KHỨ KHÔNG PHẢI DỰ BÁO"),
    kin(17, "NỘI DUNG GIÁO DỤC", "không phải tư vấn đầu tư"),
    {"type": "timeline", "at": 19, "title": "100 TRIỆU KHÔNG CHỈ CÓ KẾT QUẢ CUỐI", "items": [
        {"year": "KẾT QUẢ CUỐI", "text": "chỉ là một phần", "at": 19}, {"year": "THỜI ĐIỂM VÀO", "text": "và đoạn rơi", "at": 20}, {"year": "PHÍ · THUẾ", "text": "và lãi thật nhận được", "at": 21},
        {"year": "SỨC CHỊU ĐỰNG", "text": "của chính bạn", "at": 22}]},
    {"type": "question", "at": 23, "text": "DỮ LIỆU NÀO?\nĐÃ BỎ SÓT ĐIỀU GÌ?"},
]}}

SOURCES = [
"https://chinhphu.vn/default.aspx?docid=169566&pageid=27160", "https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2021/12/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-12-quy-iv-va-nam-2021/", "https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2022/01/kiem-soat-lam-phat-thap-thanh-cong-cua-nam-2021-va-ap-luc-trong-nam-2022/", "https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2022/12/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-12-quy-iv-va-nam-2022/", "https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2023/12/thong-cao-bao-chi-ve-tinh-hinh-gia-thang-12-quy-iv-va-nam-2023/", "https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2025/01/chi-so-gia-tieu-dung-chi-so-gia-vang-va-chi-so-gia-do-la-my-thang-muoi-hai-quy-iv-va-nam-2024/", "https://www.nso.gov.vn/tin-tuc-khac/2026/01/kinh-te-viet-nam-dat-duoc-nhung-ket-qua-quan-trong-toan-dien-nhieu-diem-sang-noi-bat/", "https://cafef.vn/nhieu-ngan-hang-tang-lai-suat-huy-dong-2018030723375295.chn"]
SPEC = {"title":"100 Triệu Từ 2018: Gửi Tiết Kiệm Hay Mua VN-Index?", "channel":"CK", "accent":"#fbbf24", "master":True, "endcard":20, "endcardSub":"VIDEO TIẾP THEO", "beat2":True, "chart_rules":True, "say":{"vn-index":"vi en đếch","hose":"hô-sê","vnstock":"vi-en-stock","cpi":"xê pi ai"}, "imgs":{}, "chapters":list(CH), "youtube":{"titles":["100 Triệu Từ 2018: Gửi Tiết Kiệm Hay Mua VN-Index?"], "publish_at":"2026-11-19T20:00:00+07:00", "playlist":"Quyết Định Lớn", "summary":"Cùng 100 triệu từ tháng 4/2018, video mô phỏng ba luật chơi: gửi tiết kiệm lãi cố định, bỏ một lần theo chỉ số giá VN-Index và mua đều trong 24 tháng. Dữ liệu giá dùng VN-Index từ HOSE qua vnstock; các mức phí, thuế và lãi tiết kiệm được nêu rõ là giả định.", "more":["Nội dung giáo dục, không phải tư vấn đầu tư. Đây là ví dụ giả định, không phải khuyến nghị mua, bán hay gửi tiền ở bất kỳ đâu. VN-Index là chỉ số giá, không gồm cổ tức; kết quả quá khứ không dự báo tương lai."], "chapter_titles":{k:v["hud"]["t"] for k,v in CH.items()}, "sources":SOURCES, "hashtags":["TàiChínhCáNhân","VNIndex","BiểuĐồBiếtNói"], "tags":["100 triệu nên làm gì","gửi tiết kiệm hay đầu tư","vnindex","mua đều","tài chính cá nhân"], "category":"27", "thumb":"t1.jpg", "data_credit":SRC, "video_credits":"Pexels · Video minh họa"}}

def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, chapter in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(chapter)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")

if __name__ == "__main__":
    main()
