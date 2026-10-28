"""Dựng cảnh cho CK C6 (giá trần, giá sàn, T+2). Số liệu lấy từ results.json và facts.md.

27/10 (Claude): dựng lại toàn bộ -- bản trước có vòng lặp chèn "ĐIỂM DỮ LIỆU 00A/B" và "MỐC THEO DÕI".
Mỗi cảnh dưới đây neo vào đúng câu đang đọc con số / sự kiện của nó.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
B, IX, A3, TL = R["band"], R["index"], R["apr_3_2025"], R["tuan_ledger"]

VM = "VIDEO MINH HỌA"
ILL = "ẢNH MINH HỌA"
HYP = "VÍ DỤ GIẢ ĐỊNH"
IDX = "DỮ LIỆU: HOSE QUA VNSTOCK"
VTV = "NGUỒN: VTV"
VNP = "NGUỒN: VIETNAMPLUS"
HOSE = "NGUỒN: HOSE"
HNX = "NGUỒN: HNX"
VSDC = "NGUỒN: VSDC"
MOTIF = "100 CỔ PHIẾU ĐANG Ở ĐÂU?"

SAY = {"vn-index": "Vê en Index", "hose": "Hô-sê", "hnx": "Hà Nội X", "upcom": "Áp-côm", "vsdc": "Vê Sờ Đê Xê",
       "t+2": "T cộng hai", "t+1": "T cộng một", "t+0": "T cộng không", "ato": "A T O", "atc": "A T C"}
IMGS = {f"ai{i:02d}": f"EXT:ai:ai_{i:02d}" for i in range(1, 7)}


def vnd(v):
    return f"{v:,.0f}".replace(",", ".")


def photo(img, at, focus=(0.5, 0.32), move=None, reveal=None, zoom=None):
    s = {"type": "photo", "img": img, "at": at, "credit": False, "illus": ILL, "focus": list(focus)}
    if move:
        s["move"] = move
    if reveal:
        s["reveal"] = {"kind": reveal, "at": at, "d": 0.9}
    if zoom:
        s["zoom"] = {"x": zoom[0], "y": zoom[1], "z": 1.4, "at": at, "d": 1.2}
    return s


def broll(at, vid, *kin):
    """kin: (text, at, kiểu) -- kiểu 'acc' (chữ chính) hoặc 'sm' (chữ phụ)."""
    return {"type": "broll", "at": at, "vid": vid, "loop": True, "veil": 0.56, "illus": VM,
            "kin": [{"text": t, "at": a, k: True} for t, a, k in kin]}


def kin(at, big, small=None, at2=None):
    items = [{"text": big, "at": at, "acc": True}]
    if small:
        items.append({"text": small, "at": at2 if at2 is not None else at, "sm": True})
    return {"type": "kinetic", "at": at, "items": items}


def bars(at, title, unit, items, src, calls=()):
    """items: (nhãn, giá trị, chữ trên cột, at, nhấn)."""
    return {"type": "bars", "at": at, "title": title, "unit": unit, "srcnote": src,
            "items": [{"k": k, "v": v, "lbl": l, "at": a, **({"acc": True} if acc else {})} for k, v, l, a, acc in items],
            "calls": [{"i": i, "text": t, "at": a} for i, t, a in calls]}


def counter(at, to, suffix, label, src, sub=None, frm=0):
    s = {"type": "counter", "at": at, "from": frm, "to": to, "suffix": suffix, "label": label, "srcnote": src}
    if sub:
        s["sub"] = {"text": sub[0], "at": sub[1]}
    return s


def ledger(at, title, rows, src=HYP):
    return {"type": "ledger", "at": at, "title": title, "srcnote": src, "rows": [{"k": k, "v": v, "at": a} for k, v, a in rows]}


def timeline(at, title, items):
    return {"type": "timeline", "at": at, "title": title, "items": [{"year": y, "text": t, "at": a} for y, t, a in items]}


def heat(at, title, rng, unit, cells, total=None, calls=(), cols=None):
    """cells: (nhãn ô, giá trị, ghi chú, at) -- mọi ô cùng một đơn vị `unit`."""
    s = {"type": "heat", "at": at, "title": title, "range": rng, "unit": unit, "cols": cols or len(cells),
         "cells": [{"k": k, "v": v, "note": n, "at": a} for k, v, n, a in cells],
         "calls": [{"i": i, "text": t, "at": a} for i, t, a in calls]}
    if total:
        s["total"] = {"label": total[0], "at": total[1]}
    return s


def waterfall(at, title, rng, unit, start, steps, end, calls=()):
    return {"type": "waterfall", "at": at, "title": title, "range": rng, "unit": unit,
            "start": {"k": start[0], "v": start[1], "at": start[2]},
            "steps": [{"k": k, "v": v, "at": a} for k, v, a in steps],
            "end": {"k": end[0], "at": end[1]},
            "calls": [{"i": i, "text": t, "at": a} for i, t, a in calls]}


def candle(at, start, end, title, text, call_at=None):
    return {"type": "candles", "at": at, "series": "vnindex", "from": start, "to": end, "title": title, "range": IDX,
            "calls": [{"i": -1, "text": text, "at": call_at if call_at is not None else at}]}


def ladder(at, title, rng, match_price, match_text, match_at, sub=None):
    """Thang giá trần / tham chiếu / sàn của ví dụ giả định (cảnh book, không có lệnh)."""
    s = {"type": "book", "at": at, "title": title, "range": rng, "ref": B["reference_vnd"], "ceil": B["ceiling_vnd"],
         "floor": B["floor_vnd"], "prices": [B["ceiling_vnd"], B["reference_vnd"], B["floor_vnd"]], "rows": [],
         "match": {"price": match_price, "at": match_at, "text": match_text},
         "source": "VÍ DỤ GIẢ ĐỊNH · HOSE ±7% · KHÔNG PHẢI GIÁ CỦA MÃ NÀO"}
    if sub:
        s["match"]["sub"] = {"text": sub[0], "at": sub[1]}
    return s


def chap(no, word, title, sub, img, focus=(0.5, 0.32)):
    return {"type": "chapter", "no": no, "k": f"CHƯƠNG {word}", "title": title, "sub": sub, "img": img,
            "credit": False, "illus": ILL, "focus": list(focus), "titleAt": 0}


REF, FLOOR, CEIL = B["reference_vnd"], B["floor_vnd"], B["ceiling_vnd"]
ORDER = R["order"]["value_vnd"]

CH = {}

# ---------------------------------------------------------------- CH00: phiên thật 09/04/2025, chưa có nhân vật
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "PHIÊN ĐỎ VÀ NÚT BÁN"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    candle(0, "2025-03-03", "2025-04-09", "VN-INDEX · 03–04/2025", "1.094,3 · −3,4%", [0, "về"]),
    counter(1, 147, " MÃ GIẢM SÀN", "PHIÊN 09/04/2025", VTV),
    broll(2, "6794227", ("MỘT BẢNG GIÁ ĐỎ", 2, "acc"), ("người vừa mua thì sao?", 3, "sm")),
    {"type": "question", "at": 4, "text": "KHỚP LỆNH SÁNG THỨ HAI\nSAO CHIỀU THỨ TƯ MỚI BÁN?"},
    kin(5, "GIÁ RƠI ≠ CÓ HÀNG ĐỂ BÁN", "nghịch lý của video", 6),
    timeline(7, "HAI CHIẾC KHÓA", [("TRẦN · SÀN", "giới hạn giá trong một phiên", 7),
                                    ("LỊCH THANH TOÁN", "giới hạn lúc chứng khoán được phân bổ", 8),
                                    ("DỄ NHẦM", "hai khóa bị trộn thành một", 9)]),
    {"type": "question", "at": 10, "text": "CHỜ TỪ THỨ HAI ĐẾN THỨ TƯ\nĐÃ LÀM AI MẤT TIỀN?"},
    broll(11, "8195667", ("TÁCH TỪNG CHIẾC KHÓA", 11, "acc"), ("giá · thời điểm", 12, "sm")),
    {"type": "brand", "at": 12, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

# ---------------------------------------------------------------- CH01: khung giá quanh 20.000
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CÁI KHUNG QUANH GIÁ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap("1", "MỘT", "CÁI KHUNG QUANH\nGIÁ 20.000 ĐỒNG", "VÍ DỤ GIẢ ĐỊNH · KHÔNG KHUYẾN NGHỊ", "ai01", (0.45, 0.3)),
    ledger(1, "NHÂN VẬT HƯ CẤU", [("NGƯỜI MUA", "ANH TUẤN · HƯ CẤU", 1), ("CỔ PHIẾU", "100 · CÔNG TY HƯ CẤU", 2),
                                  ("GIÁ MỖI CỔ PHIẾU", "20.000 ĐỒNG", 3)]),
    counter(4, ORDER, " ĐỒNG", "100 × 20.000 ĐỒNG · VÍ DỤ GIẢ ĐỊNH", HYP, ("CHƯA GỒM PHÍ", [4, "phí"])),
    timeline(5, "LỊCH MINH HỌA", [("THỨ HAI", "ngày T", 5), ("THỨ BA", "T+1", [5, "Ba"]), ("THỨ TƯ", "T+2", [5, "Tư"])]),
    broll(7, "7148966", ("ĐỒNG HỒ PHÂN BỔ", 7, "acc"), ("không dự báo tuần nào", 7, "sm")),
    ledger(8, "HAI KHÁI NIỆM", [("GIÁ THAM CHIẾU", "MỐC SỞ GIAO DỊCH TÍNH DẢI", 8),
                                ("BIÊN ĐỘ", "GIỚI HẠN DAO ĐỘNG QUANH MỐC", 9),
                                ("GẦN NHAU", "NHƯNG KHÔNG PHẢI MỘT", 10)], "NGUỒN: TT 120/2020/TT-BTC"),
    counter(11, REF, " ĐỒNG", "GIÁ THAM CHIẾU · VÍ DỤ GIẢ ĐỊNH", HOSE, ("HOSE · BIÊN ĐỘ THÔNG THƯỜNG ±7%", 12)),
    waterfall(13, "TỪ THAM CHIẾU XUỐNG SÀN", "ĐỒNG · VÍ DỤ GIẢ ĐỊNH · ±7%", "ĐỒNG",
              ("THAM CHIẾU", REF, 13), [("−7%", -1400, 13)], ("GIÁ SÀN", 14),
              [(1, "7% = 1.400 ĐỒNG", 13), (2, "SÀN 18.600", 14)]),
    waterfall(15, "TỪ THAM CHIẾU LÊN TRẦN", "ĐỒNG · VÍ DỤ GIẢ ĐỊNH · ±7%", "ĐỒNG",
              ("THAM CHIẾU", REF, 15), [("+7%", 1400, 15)], ("GIÁ TRẦN", [15, "trần"]),
              [(2, "TRẦN 21.400", [15, "trần"])]),
    ladder(16, "DẢI GIÁ MỘT PHIÊN", "18.600 → 21.400 ĐỒNG", REF, "GIỮA DẢI: 20.000 ĐỒNG", 17),
    bars(18, "BA ĐIỂM TRÊN THANH GIÁ", "ĐỒNG", [("SÀN", FLOOR, "18.600", 18, False), ("THAM CHIẾU", REF, "20.000", 18, True),
                                               ("TRẦN", CEIL, "21.400", 18, False)], HYP,
         [(0, "ĐIỂM THẤP: SÀN", 19), (1, "GIỮA: THAM CHIẾU", 20), (2, "ĐIỂM CAO: TRẦN", 21)]),
    {"type": "stack", "at": 22, "title": MOTIF, "range": HYP, "unit": "CỔ PHIẾU",
     "keys": [{"k": "CHỜ PHÂN BỔ"}, {"k": "CÓ THỂ BÁN"}],
     "groups": [{"k": "SAU KHI KHỚP", "vals": [100, 0], "at": 22}],
     "calls": [{"i": 0, "text": "KHỚP 2 TRIỆU ĐỒNG", "at": 23}]},
    broll(24, "7688068", ("KHUNG GIÁ ≠ DỰ BÁO", 24, "acc"), ("chỉ là phép nhân", 26, "sm")),
    kin(27, "ATO · ATC · LÔ 100", "quy ước của phiên, như tập trước"),
    photo("ai02", 28, (0.55, 0.3), zoom=(0.6, 0.45)),
    kin(30, "GIÁ ≠ THỜI ĐIỂM", "ngày thường · ngày ngoại lệ", 31),
]}

# ---------------------------------------------------------------- CH02: 7% và các ngoại lệ
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BẢY PHẦN TRĂM KHÔNG PHẢI MỌI KHUNG"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    chap("2", "HAI", "BẢY PHẦN TRĂM\nKHÔNG PHẢI MỌI KHUNG", "NGÀY THƯỜNG VÀ NGOẠI LỆ · HOSE · HNX", "ai02", (0.55, 0.3)),
    kin(1, "±7% ≠ LỖ TỐI ĐA", "biên độ của một phiên"),
    photo("ai01", 2, (0.45, 0.3), move="pan"),
    bars(4, "MỘT PHIÊN GIẢM 7%", "ĐỒNG", [("THAM CHIẾU", REF, "20.000", 4, False), ("SAU GIẢM 7%", FLOOR, "18.600", [4, "còn"], True)],
         HYP, [(1, "18.600 ĐỒNG", [4, "còn"])]),
    broll(6, "11899304", ("MỘT NGÀY ≠ PHANH CẢ TUẦN", 6, "acc"), ("ngày sau: tham chiếu khác", 6, "sm")),
    kin(7, "SÀN = ĐÁY?", "không có đáy chung", 9),
    ladder(10, "ĐÁY CỦA MỘT PHIÊN", "KHÔNG PHẢI ĐÁY CHO MỌI TƯƠNG LAI", FLOOR, "SÀN: ĐÁY TRONG DẢI PHIÊN NÀY", 10),
    counter(11, 20, "%", "BIÊN ĐỘ HOSE · NGÀY ĐẦU HOẶC GIAO DỊCH LẠI", HOSE, ("±20% THAY CHO ±7%", 12), frm=7),
    bars(13, "DẢI ±20% QUANH 20.000", "ĐỒNG", [("THAM CHIẾU", REF, "20.000", 13, False), ("SÀN ±20%", 16000, "16.000", 14, False),
                                                ("TRẦN ±20%", 24000, "24.000", [14, "tới"], True)], HYP,
         [(0, "±4.000 ĐỒNG", 13)]),
    timeline(15, "UPCOM · THEO NGUỒN HNX", [("01/07/2015", "biên độ thông thường lên ±15%", 15),
                                             ("04/04/2011", "ngày đầu, giao dịch lại: ±40%", 16)]),
    bars(17, "MỨC DAO ĐỘNG QUANH 20.000", "ĐỒNG", [("±15%", 3000, "3.000", 17, False), ("±40%", 8000, "8.000", 18, True)], HYP),
    bars(19, "BỐN MỨC BIÊN ĐỘ", "%", [("HOSE THƯỜNG", 7, "7%", 19, False), ("HOSE NGÀY ĐẦU", 20, "20%", [19, "hai"], False),
                                      ("UPCOM THƯỜNG", 15, "15%", [19, "lăm"], False), ("UPCOM NGÀY ĐẦU", 40, "40%", [19, "bốn"], True)],
         "NGUỒN: HOSE · HNX"),
    broll(20, "7693395", ("BỐI CẢNH, KHÔNG PHẢI BẢNG CHỌN", 20, "acc")),
    ledger(22, "BA CÂU PHẢI HỎI", [("SÀN NÀO?", "HOSE HAY UPCOM", 22), ("NGÀY NÀO?", "THƯỜNG HAY NGÀY ĐẦU", [22, "ngày"]),
                                   ("TÌNH HUỐNG NÀO?", "CÓ GIAO DỊCH LẠI KHÔNG", [22, "tình"])], "NGUỒN: HOSE · HNX"),
    {"type": "question", "at": 23, "text": "PHIÊN NGHẸT Ở PHÍA SÀN\nNÚT BÁN CÓ TỰ MỞ?"},
]}

# ---------------------------------------------------------------- CH03: 03/04 và 09/04/2025
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "KHI CẢ BẢNG CÙNG CHẠM SÀN"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    chap("3", "BA", "KHI CẢ BẢNG\nCÙNG CHẠM SÀN", "PHIÊN 03/04/2025 · NGUỒN: VIETNAMPLUS", "ai03", (0.5, 0.3)),
    candle(1, "2025-03-03", "2025-04-03", "VN-INDEX · ĐẾN 03/04/2025", "1.229,84 ĐIỂM"),
    waterfall(2, "PHIÊN 03/04/2025", "ĐIỂM · " + VNP, "ĐIỂM", ("02/04", round(IX["apr_3"] - IX["apr_3_change"], 2), 2),
              [("PHIÊN 03/04", IX["apr_3_change"], 2)], ("ĐÓNG CỬA", 3), [(1, "−87,99 · −6,68%", 3)]),
    counter(4, A3["down_total"], " MÃ GIẢM", "HOSE · PHIÊN 03/04/2025", VNP),
    bars(5, "HOSE 03/04/2025", "MÃ", [("GIẢM SÀN", A3["floor_down"], "263", 5, True), ("GIẢM KHÁC", A3["other_down"], "254", 6, False),
                                      ("TĂNG", A3["up"], "13", 7, False), ("TĂNG TRẦN", A3["ceiling_up"], "3", 8, False)], VNP,
         [(0, "263 MÃ SÀN", 5), (1, "517 − 263 = 254", 6)]),
    {"type": "stack", "at": 9, "title": "PHIÊN 03/04 · CỘT CHỒNG", "range": "MÃ · " + VNP, "unit": "MÃ",
     "keys": [{"k": "GIẢM SÀN", "color": "#22d3ee"}, {"k": "GIẢM KHÁC", "color": "#ef4444"}, {"k": "TĂNG", "color": "#4ade80"}],
     "groups": [{"k": "MÃ GIẢM", "vals": [A3["floor_down"], A3["other_down"], 0], "at": 9},
                {"k": "MÃ TĂNG", "vals": [0, 0, A3["up"]], "at": 13}],
     "calls": [{"i": 0, "text": "263 SÁT SÀN", "at": 11}, {"i": 1, "text": "13 TĂNG · 3 TRẦN", "at": [13, "tăng"]}]},
    broll(14, "7148966", ("KHÔNG PHẢI LỜI KHUYÊN", 14, "sm"), ("NHIỀU MỨC GIÁ CÙNG CHẠM SÀN", 15, "acc")),
    candle(16, "2025-04-01", "2025-04-09", "VN-INDEX · 01–09/04/2025", "1.094,3 ĐIỂM", 17),
    waterfall(18, "PHIÊN 09/04/2025", "ĐIỂM · " + VTV, "ĐIỂM", ("08/04", round(IX["apr_9"] - IX["apr_9_change"], 2), 18),
              [("PHIÊN 09/04", IX["apr_9_change"], 18)], ("ĐÓNG CỬA", 19), [(1, "−38,49 · −3,40%", 19)]),
    bars(20, "MÃ GIẢM SÀN · HAI PHIÊN", "MÃ", [("09/04/2025", 147, "147", 20, True), ("03/04/2025", A3["floor_down"], "263", 21, False)],
         "NGUỒN: VTV · VIETNAMPLUS", [(0, "ÍT HƠN 263", 21)]),
    broll(22, "7651886", ("ÁP LỰC DỒN VỀ MỘT BÊN BẢNG", 22, "acc")),
    photo("ai03", 23, (0.5, 0.3), reveal="wipe"),
    ledger(24, MOTIF, [("HAI CỘT", "GIÁ ≠ QUYỀN ĐẶT LỆNH", 24), ("CỘT GIÁ", "18.600 – 21.400 ĐỒNG", 25),
                       ("CỘT LỊCH", "T · T+1 · CHIỀU T+2", 26)]),
    kin(27, "LỊCH KHÔNG ĐỔI", "cột thứ hai: thời điểm", 28),
]}

# ---------------------------------------------------------------- CH04: quy chế VSDC, T đến T+2
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "CHIẾC ĐỒNG HỒ PHÂN BỔ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    chap("4", "BỐN", "T, T+1\nVÀ ĐỒNG HỒ PHÂN BỔ", "QUY CHẾ VSDC · HIỆU LỰC 29/08/2022", "ai04", (0.5, 0.35)),
    timeline(1, "QUY CHẾ THANH TOÁN MỚI", [("19/08/2022", "quyết định ban hành", 1), ("29/08/2022", "quy chế có hiệu lực", [1, "quy"])]),
    counter(2, 13, " GIỜ", "MUA NGÀY T · NHẬN TRƯỚC 13 GIỜ T+2", VSDC, ("BÁN ĐƯỢC TỪ PHIÊN CHIỀU T+2", 3)),
    broll(4, "8195667", ("ĐỒNG HỒ VẪN CHẠY", 4, "sm"), ("MỐC QUAN TRỌNG NHẤT", 5, "acc")),
    photo("ai04", 6, (0.5, 0.4), zoom=(0.45, 0.6)),
    heat(7, "LỊCH CỦA 100 CỔ PHIẾU", HYP + " · THỨ HAI → THỨ TƯ", "CỔ PHIẾU",
         [("T · THỨ HAI", 0, "KHỚP 2 TRIỆU ĐỒNG", 7), ("T+1 · THỨ BA", 0, "VẪN 2 TRIỆU KHỚP", 9),
          ("T+2 · THỨ TƯ", 0, "CHỜ MỐC GIỜ", 12)],
         ("CÓ THỂ BÁN", 8), [(0, "Ô BÁN: 0", 8), (1, "Ô BÁN VẪN 0", 11)]),
    timeline(13, "NGÀY T+2 THEO VSDC", [("11:00 – 11:30", "hoàn tất với ngân hàng thanh toán", 13),
                                         ("TRƯỚC 13:00", "thành viên lưu ký phân bổ cho khách", 14)]),
    bars(15, "CÁC MỐC GIỜ NGÀY T+2", "GIỜ", [("HOÀN TẤT TỪ", 11, "11:00", 15, False), ("HOÀN TẤT ĐẾN", 11.5, "11:30", 15, False),
                                             ("PHÂN BỔ TRƯỚC", 13, "13:00", 15, True)], VSDC, [(2, "MỐC PHÂN BỔ", 16)]),
    kin(17, "KHÔNG PHẢI ĐẦU NGÀY", "nguồn nói: phiên chiều T+2", 18),
    ledger(19, "CÁCH NÓI VÀ MỐC NGUỒN", [("“T+2,5”", "CÁCH NÓI, KHÔNG CHÍNH THỨC", 19), ("TRƯỚC 13 GIỜ", "PHÂN BỔ", 20),
                                          ("PHIÊN CHIỀU", "CÓ THỂ BÁN", [20, "chiều"])], VSDC),
    {"type": "stack", "at": 21, "title": "CHIỀU THỨ TƯ ĐỔI Ô", "range": HYP, "unit": "CỔ PHIẾU",
     "keys": [{"k": "CHỜ PHÂN BỔ"}, {"k": "CÓ THỂ BÁN"}],
     "groups": [{"k": "TRƯỚC 13 GIỜ", "vals": [100, 0], "at": 21}, {"k": "CHIỀU T+2", "vals": [0, 100], "at": [21, "sang"]}],
     "calls": [{"i": 1, "text": "100 CÓ THỂ BÁN", "at": [21, "bán"]}]},
    broll(22, "7693395", ("GIÁ TĂNG HAY GIẢM", 22, "sm"), ("NÚT BÁN KHÔNG ĐỔI THEO MÀU GIÁ", 23, "acc")),
    kin(24, "ĐỒNG HỒ THANH TOÁN", "nơi khung giá gặp lịch", 25),
]}

# ---------------------------------------------------------------- CH05: theo chân 100 cổ phiếu
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "THEO CHÂN MỘT TRĂM CỔ PHIẾU"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    chap("5", "NĂM", "THEO CHÂN\n100 CỔ PHIẾU", "VÍ DỤ GIẢ ĐỊNH · T → CHIỀU T+2", "ai05", (0.5, 0.3)),
    ledger(1, "BẢNG HAI HÀNG", [("HÀNG ĐẦU", "TIỀN · GIÁ TRỊ KHỚP", 1), ("HÀNG DƯỚI", "100 CỔ PHIẾU HƯ CẤU", 2)]),
    counter(4, TL["T"]["cash_matched_vnd"], " ĐỒNG", "SÁNG THỨ HAI · 20.000 × 100", HYP, ("GIÁ TRỊ KHỚP · CHƯA GỒM PHÍ", 5)),
    {"type": "stack", "at": 6, "title": "Ô CÓ THỂ BÁN", "range": HYP, "unit": "CỔ PHIẾU",
     "keys": [{"k": "CHỜ PHÂN BỔ"}, {"k": "CÓ THỂ BÁN"}],
     "groups": [{"k": "T · THỨ HAI", "vals": [100, TL["T"]["shares_sellable"]], "at": 6},
                {"k": "T+1 · THỨ BA", "vals": [100, TL["T1"]["shares_sellable"]], "at": 8}],
     "calls": [{"i": 0, "text": "CỘT T: BÁN ĐƯỢC 0", "at": 7}, {"i": 1, "text": "CỘT T+1: VẪN 0", "at": [8, "không"]}]},
    kin(9, "2 TRIỆU = GIÁ TRỊ KHỚP", "không phải số dư thực tế", 9),
    broll(11, "7688068", ("VẪN CHỜ PHÂN BỔ", 11, "acc"), ("cột T+1", 12, "sm")),
    heat(13, "ĐẾN CHIỀU THỨ TƯ", HYP, "CỔ PHIẾU",
         [("T · THỨ HAI", TL["T"]["shares_sellable"], "CHỜ", 13), ("T+1 · THỨ BA", TL["T1"]["shares_sellable"], "CHỜ", 13),
          ("CHIỀU T+2 · THỨ TƯ", TL["T2_afternoon"]["shares_sellable"], "CÓ THỂ BÁN", [13, "thành"])],
         ("CÓ THỂ BÁN", 14), [(2, "CHIỀU T+2", 14)]),
    photo("ai05", 15, (0.5, 0.3), move="in"),
    ladder(18, "GIÁ VẪN TRONG DẢI PHIÊN", "TRẠNG THÁI GIÁ · KHÔNG PHẢI QUYỀN BÁN", FLOOR, "SÀN 18.600: MỘT TRẠNG THÁI GIÁ", 19,
           ("TRẦN 21.400 CŨNG VẬY", 20)),
    ledger(21, MOTIF, [("ĐẶT LỆNH BÁN", "THEO LỊCH PHÂN BỔ", 21), ("TỪNG Ô", "MỘT NHIỆM VỤ RIÊNG", 22),
                       ("HAI CÂU HỎI", "THƯỜNG BỊ TRỘN", 23)]),
    {"type": "question", "at": 24, "text": "CÂU 1: HÔM NAY\nGIÁ CHẠY TRONG DẢI NÀO?"},
    {"type": "question", "at": 25, "text": "CÂU 2: KHI NÀO CỔ PHIẾU\nNẰM Ở Ô CÓ THỂ BÁN?"},
    timeline(26, "CÂU 2 DẪN TỚI ĐÂU?", [("CHIỀU T+2", "mốc của ví dụ giả định", 26), ("GIÁ ĐỔI MÀU", "không phải", 27),
                                         ("MẸO THAO TÁC", "không phải", 28)]),
    broll(29, "7651886", ("MỐC VẬN HÀNH NGUỒN NÊU", 29, "acc")),
    {"type": "question", "at": 30, "text": "BÁN XONG, TIỀN THỰC NHẬN\nCÓ BẰNG GIÁ × SỐ CỔ PHIẾU?"},
]}

# ---------------------------------------------------------------- CH06: phí, thuế, T+0 và khép vòng
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "BA Ô CHƯA ĐƯỢC PHÉP ĐIỀN"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    chap("6", "SÁU", "BA Ô CHƯA ĐƯỢC\nPHÉP ĐIỀN", "PHÍ · THUẾ · T+0", "ai06", (0.5, 0.3)),
    {"type": "dots", "at": 1, "total": 100, "cols": 20, "title": "100 CỔ PHIẾU = 100 ĐƠN VỊ",
     "groups": [{"from": 0, "n": 100, "cls": "hollow", "label": "100 CỔ PHIẾU · VÍ DỤ GIẢ ĐỊNH", "at": 1}]},
    broll(2, "6794227", ("GIÁ BÁN × SỐ CỔ PHIẾU", 2, "sm"), ("KHÔNG CÓ MỘT CON SỐ CHUNG", 2, "acc")),
    ledger(3, "Ô 1 · PHÍ GIAO DỊCH", [("PHÍ", "THEO BIỂU PHÍ NƠI MỞ TÀI KHOẢN", 3),
                                      ("MỨC CHUNG", "KHÔNG CÓ KÈM NGÀY HIỆU LỰC", 4)], "TÀI LIỆU ĐANG DÙNG"),
    heat(5, "BA Ô KHÔNG GIỐNG NHAU", "CHỈ ĐIỀN KHI VĂN BẢN XÁC NHẬN", "Ô",
         [("PHÍ", 0, "CHƯA ĐIỀN", 5), ("THUẾ", 0, "CẦN KIỂM VĂN BẢN", 5), ("T+0", 0, "CHƯA XÁC NHẬN", 5)],
         ("ĐÃ ĐIỀN", 7), [(0, "CHƯA ĐIỀN", 6)]),
    photo("ai06", 8, (0.5, 0.3), move="pan"),
    timeline(9, "Ô 2 · THUẾ · MỐC VĂN BẢN", [("LUẬT 109/2025/QH15", "hiệu lực 01/07/2026", 9),
                                             ("NGHỊ ĐỊNH HƯỚNG DẪN", "hiệu lực 01/07/2026", 10)]),
    kin(11, "0,1%: CHƯA CHỐT", "chưa đọc như một khẳng định"),
    ledger(12, "Ô 2 · THUẾ", [("THUẾ", "CẦN KIỂM VĂN BẢN", 12), ("2.000.000 ĐỒNG", "KHÔNG TRỪ KHOẢN CHƯA CHỐT", 13)],
           "NGUỒN: BỘ TÀI CHÍNH · BỘ TƯ PHÁP"),
    broll(14, "11899304", ("KHÔNG NÉ SỐ", 14, "sm"), ("KHÔNG BIẾN VÍ DỤ THÀNH TIN SAI", 16, "acc")),
    timeline(17, "Ô 3 · T+0", [("Ô THỨ BA", "T+0", 17), ("CHIỀU T+2", "nguồn xác nhận khả năng bán", 18),
                               ("BÁN CHỜ VỀ · T+0", "nguồn không xác nhận", 19)]),
    heat(20, "LỊCH CHỈ KÉO TỚI T+2", HYP + " · " + VSDC, "CỔ PHIẾU",
         [("T", 0, "KHỚP", 20), ("T+1", 0, "CHỜ", 20), ("CHIỀU T+2", 100, "CÓ THỂ BÁN", 20), ("T+0", 0, "ĐỂ TRỐNG", 21)],
         ("CÓ THỂ BÁN", 20), [(3, "Ô TRỐNG", 21)], cols=4),
    kin(22, "KHÔNG ĐOÁN NGÀY ÁP DỤNG", "không hứa trên ô trống", 23),
    candle(24, "2025-03-17", "2025-04-09", "QUAY LẠI PHIÊN 09/04/2025", "PHIÊN MỞ ĐẦU"),
    ledger(25, MOTIF, [("ĐÃ KHỚP Ở T", "2.000.000 ĐỒNG", 25), ("CHƯA BÁN NGAY", "KHÔNG PHẢI VÌ GIÁ SÀN", 26)]),
    timeline(27, "HAI CHIẾC KHÓA, HAI VIỆC", [("GIÁ SÀN", "giới hạn giá của từng phiên", 27),
                                               ("T+2", "giới hạn lúc có chứng khoán để bán", 28)]),
    {"type": "dots", "at": 29, "total": 100, "cols": 20, "title": "CHIỀU T+2: 100 Ô SÁNG",
     "groups": [{"from": 0, "n": 100, "cls": "gold", "label": "100 CỔ PHIẾU CÓ THỂ BÁN · VÍ DỤ GIẢ ĐỊNH", "at": 29}]},
    photo("ai05", 30, (0.5, 0.3), move="out"),
    kin(31, "GIÁ · THỜI ĐIỂM: HAI HÀNG", "chỉ điền ô có văn bản xác nhận", 32),
]}

SOURCES = [
    "TT 120/2020/TT-BTC: https://staticfile.hsx.vn/Uploads/LocalFiles/d7f582e40a2c43528c8476092dd1f6ad/20210119_Thong%20tu%20120.2020%20TT-BTC.pdf",
    "HOSE, biên độ giá: https://staticfile.hsx.vn/Uploads/UploadDocuments/2372201/4.Bien%20do%20dao%20dong%20gia.pdf",
    "HNX, UPCoM: https://www.hnx.vn/vi-vn/m-tin-tuc-hnx/9%20nam%20hoat%20dong%20UPCoM%20lon%20manh%20khong%20ngung-60002643-0.html",
    "VietnamPlus 03/04/2025: https://www.vietnamplus.vn/vn-index-giam-manh-nhat-lich-su-sau-khi-my-cong-bo-thue-doi-ung-post1024606.vnp",
    "VTV 09/04/2025: https://vtv.vn/kinh-te/vn-index-giam-tiep-gan-40-diem-20250409171341275.htm",
    "VSDC, Quyết định 109: https://vsdc.vn/vi/ad/152750",
    "Bộ Tài chính, Luật thuế: https://vbpl.moj.gov.vn/botaichinh/Pages/vbpq-vanbanlienquan.aspx?ItemID=187045",
    "Bộ Tư pháp, nghị định hướng dẫn: https://moj.gov.vn/portal/tin-tuc/chi-tiet/quy-inh-chi-tiet-mot-so-dieu-va-bien-phap-de-to-chuc-huong-dan-thi-hanh-luat-thue-thu-nhap-ca-nhan-ti00o28d56.html"]

SPEC = {"title": "Mua Thứ Hai, Thứ Tư Mới Bán Được: T+2 Là Gì?", "channel": "CK", "accent": "#fbbf24", "master": True,
        "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True, "chart_rules": True, "say": SAY, "imgs": IMGS,
        "chapters": list(CH),
        "youtube": {"titles": ["Mua Thứ Hai, Thứ Tư Mới Bán Được: T+2 Là Gì?", "Bắt Đáy 9/4/2025: Vì Sao Không Bán Kịp?",
                               "Giá Trần, Giá Sàn, T+2: Ba Luật Người Mới Hay Trả Giá"],
                    "publish_at": "2026-11-21T13:00:00Z", "playlist": "Chứng Khoán Từ Số 0",
                    "summary": "Ngày 09/04/2025, VN-Index giảm 3,4% xuống 1.094,3 điểm, 147 mã giảm sàn. Phiên đó dẫn vào câu hỏi: mua cổ phiếu sáng thứ Hai vì sao tới chiều thứ Tư mới có thể bán? Video tách dải giá trần, giá sàn khỏi lịch phân bổ T, T+1, T+2 bằng số liệu công khai và ví dụ 100 cổ phiếu hư cấu.",
                    "more": ["Nội dung giáo dục, không phải tư vấn đầu tư. Ví dụ anh Tuấn, 100 cổ phiếu và các mức giá trong video là VÍ DỤ GIẢ ĐỊNH; không phải khuyến nghị mua, bán hay lựa chọn nơi giao dịch. Phí, thuế và quy định có thể thay đổi; chỉ dùng các mốc mà nguồn công khai trong video xác nhận."],
                    "chapter_titles": {"ch00": "Phiên đỏ và nút bán", "ch01": "Cái khung quanh giá hai mươi nghìn",
                                       "ch02": "Bảy phần trăm không phải mọi khung", "ch03": "Khi cả bảng cùng chạm sàn",
                                       "ch04": "Chiếc đồng hồ phân bổ", "ch05": "Theo chân một trăm cổ phiếu",
                                       "ch06": "Ba ô chưa được phép điền"},
                    "sources": SOURCES, "hashtags": ["ChứngKhoán", "Tplus2", "TàiChínhCáNhân"],
                    "tags": ["T+2 là gì", "giá trần giá sàn", "chứng khoán cho người mới", "thanh toán chứng khoán", "VN-Index"],
                    "category": "27", "thumb": "t1.jpg",
                    "data_credit": "Số liệu phiên 03/04/2025 và 09/04/2025 từ VietnamPlus, VTV; nến VN-Index từ HOSE qua vnstock; quy định từ HOSE, HNX, VSDC và văn bản công khai.",
                    "video_credits": "Clip minh họa từ Pexels; ảnh minh họa nhân vật hư cấu."}}


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
