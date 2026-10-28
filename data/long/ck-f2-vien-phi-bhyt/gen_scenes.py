"""Dựng cảnh cho ck-f2-vien-phi-bhyt. Mọi số của hoá đơn giả định lấy từ results.json.

27/10/2026 (Claude, vòng 3): dựng lại toàn bộ 7 chương. Bản trước sinh cảnh bằng vòng lặp (khuôn "· CHƯƠNG 0N"
lặp ở 6 chương và ~80 counter đi vòng qua các số của hoá đơn, không khớp lời đọc). Mỗi cảnh dưới đây neo vào đúng
câu đang đọc con số hoặc dữ kiện của nó.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
W, T, O = R["waterfall"], R["five_year_threshold"], R["out_of_pocket"]
HH = R["household_discount"]
IMGS = {f"ai{i:02}": f"EXT:ai:ai_{i:02}" for i in range(1, 7)}

HYP = "VÍ DỤ GIẢ ĐỊNH · TRIỆU ĐỒNG"
VM = "VIDEO MINH HỌA"
ILL = "ẢNH MINH HỌA"
S_BHXH = "NGUỒN: BHXH VIỆT NAM"
S_LAW = "NGUỒN: LUẬT 51/2024/QH15 · BHXH VIỆT NAM"
S_GOV = "NGUỒN: BÁO CHÍNH PHỦ"


def vn(x):
    """Số kiểu Việt: 2.53 -> "2,53", 30.0 -> "30"."""
    return f"{x:g}".replace(".", ",")


TOT, COV, FUND, COPAY = W["total"], W["covered"], W["fund"], W["copay"]
OUT, BILL, EXTRA, BURDEN = W["outside_scope"], W["on_bill"], W["outside_invoice"], W["burden"]
RATE = FUND / COV                                   # 0,8 -- mức hưởng ví dụ
PCT_BURDEN = BURDEN / (TOT + EXTRA) * 100           # 37,5 -- "khoảng ba mươi tám phần trăm"
TR = lambda x: f"{vn(x)} TRIỆU"

SAY = {"bhyt": "bảo hiểm y tế", "bhxh": "bảo hiểm xã hội", "kcb": "khám chữa bệnh",
       "nd": "nghị định", "tt": "thông tư", "nq": "nghị quyết", "cp": "chính phủ"}


# ---------------- helper ----------------
def bars(at, title, items, unit="TRIỆU ĐỒNG", src=HYP, calls=None):
    s = {"type": "bars", "at": at, "title": title, "unit": unit, "srcnote": src,
         "items": [{"k": k, "v": v, "lbl": l, "at": a, **({"acc": True} if acc else {})} for k, v, l, a, acc in items]}
    if calls:
        s["calls"] = [{"i": i, "text": t, "at": a} for i, t, a in calls]
    return s


def wf(at, title, start, steps, end=None, calls=(), rng=HYP):
    """start=(k, v, at); steps=[(k, v, at)]; end=(k, at[, tone]); calls=[(i, text, at)] -- i: 0 cột đầu, 1..n bước, n+1 cột cuối."""
    s = {"type": "waterfall", "at": at, "title": title, "range": rng, "unit": "TRIỆU",
         "start": {"k": start[0], "v": start[1], "at": start[2]},
         "steps": [{"k": k, "v": v, "at": a} for k, v, a in steps],
         "calls": [{"i": i, "text": t, "at": a} for i, t, a in calls]}
    if end:
        s["end"] = {"k": end[0], "at": end[1], **({"tone": end[2]} if len(end) > 2 else {})}
    return s


def stack(at, title, keys, groups, calls=()):
    return {"type": "stack", "at": at, "title": title, "range": HYP, "unit": "TRIỆU",
            "keys": [{"k": k} for k in keys], "groups": [{"k": k, "vals": v, "at": a} for k, v, a in groups],
            "calls": [{"i": i, "text": t, "at": a} for i, t, a in calls]}


def counter(at, to, suffix, label, sub=None, src=S_BHXH, frm=0):
    s = {"type": "counter", "at": at, "from": frm, "to": to, "suffix": suffix, "label": label, "srcnote": src}
    if sub:
        s["sub"] = {"text": sub[0], "at": sub[1]}
    return s


def dots(at, title, total, cols, groups):
    """groups=[(from, n, cls, label, at)] -- n phải khớp số trong label."""
    return {"type": "dots", "at": at, "title": title, "total": total, "cols": cols,
            "groups": [{"from": f, "n": n, "cls": c, "label": l, "at": a} for f, n, c, l, a in groups]}


def ledger(at, title, rows, src=HYP, total=None):
    s = {"type": "ledger", "at": at, "title": title, "srcnote": src, "rows": [{"k": k, "v": v, "at": a} for k, v, a in rows]}
    if total:
        s["total"] = {"k": total[0], "v": total[1], "at": total[2]}
    return s


def timeline(at, title, items, src=None):
    s = {"type": "timeline", "at": at, "title": title, "items": [{"year": y, "text": t, "at": a} for y, t, a in items]}
    if src:
        s["srcnote"] = src
    return s


def kin(at, big, *small):
    """small=[(text, at)] -- chữ lớn là từ khoá, không chép lời đọc."""
    return {"type": "kinetic", "at": at, "items": [{"text": big, "at": at, "acc": True}] +
            [{"text": t, "at": a, "sm": True} for t, a in small]}


def question(at, text):
    return {"type": "question", "at": at, "text": text}


def myth(at, m, t, strike, truth, mlab=None, tlab=None):
    s = {"type": "myth", "at": at, "myth": m, "truth": t, "strikeAt": strike, "truthAt": truth}
    if mlab:
        s["mythLab"] = mlab
    if tlab:
        s["truthLab"] = tlab
    return s


def broll(at, vid, kins):
    """kins=[(text, at, "acc"|"sm")]"""
    return {"type": "broll", "at": at, "vid": vid, "veil": 0.55, "illus": VM,
            "kin": [{"text": t, "at": a, ("acc" if f == "acc" else "sm"): True} for t, a, f in kins]}


def photo(img, at, focus, kins=(), **fx):
    s = {"type": "photo", "img": img, "at": at, "credit": False, "illus": ILL, "focus": focus, **fx}
    if kins:
        s["kin"] = [{"text": t, "at": a, ("acc" if f == "acc" else "sm"): True} for t, a, f in kins]
    return s


def chap(no, word, title, sub, bg=None, vid=None):
    s = {"type": "chapter", "no": no, "k": word, "title": title, "sub": sub, "titleAt": 0}
    if bg:
        s["bg"] = bg
    if vid:
        s.update({"vid": vid, "illus": VM})
    return s


# ---------------- cảnh ----------------
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MƯỜI HAI TRIỆU Ở ĐÂU"}, "bgm": {"mood": "calm", "gain": 0.1}, "scenes": [
    # câu 0–1: hai số thật có nguồn, biểu đồ ngay giây đầu
    counter(0, 94.29, "%", "DÂN SỐ CÓ BHYT · CUỐI 2024"),
    bars(1, "CÓ THẺ VẪN TRẢ TIỀN TÚI", [("BAO PHỦ BHYT · CUỐI 2024", 94.29, "94,29%", 1, False),
                                         ("TIỀN TÚI / TỔNG CHI Y TẾ · 2025", O["year_2025"], f"≈{O['year_2025']}%", [1, "bốn"], True)],
         unit="PHẦN TRĂM", src=S_BHXH, calls=[(1, "VẪN ≈40%", [2, "hai"])]),
    kin(3, "NGHỊCH LÝ", ("có thẻ, vẫn trả từ túi", 3)),
    ledger(4, "BA THỨ KHÔNG GIỐNG NHAU", [("1", "TỶ LỆ TRÊN THẺ", 4), ("2", "KHOẢN TRÊN HÓA ĐƠN", [4, "hóa"]),
                                           ("3", "KHOẢN GIA ĐÌNH PHẢI XOAY", [4, "gia"])], src="VIDEO NÀY TÁCH TỪNG LỚP"),
    question(5, "CÓ THẺ RỒI\nVÌ SAO VẪN TỰ TRẢ?"),
    broll(6, "36718656", [("NẰM Ở ĐÂU TRÊN HÓA ĐƠN?", 6, "acc"), ("tỷ lệ cả nước không đoán được hóa đơn của bạn", 7, "sm")]),
    timeline([8, "từng"], "BỐN LỚP TIỀN CẦN TÁCH", [("LỚP 1", "trong phạm vi", [8, "từng"]), ("LỚP 2", "đồng chi trả", [8, "đồng"]),
                                                   ("LỚP 3", "ngoài phạm vi", [8, "ngoài"]), ("LỚP 4", "chi phí đi cùng", [8, "cùng"])]),
    question(10, "LỘ TRÌNH 2030\nCHẠM ĐƯỢC LỚP NÀO?"),
    {"type": "brand", "at": [10, "vẫn"], "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "TỔNG HÓA ĐƠN NHIỀU LỚP"}, "bgm": {"mood": "curious", "gain": 0.1}, "scenes": [
    chap("1", "CHƯƠNG MỘT", "TỔNG HÓA ĐƠN\nNHIỀU LỚP", "VÍ DỤ GIẢ ĐỊNH · ANH MINH", bg="ai01"),
    counter([1, "tổng"], TOT, " TRIỆU", "TỔNG CHI PHÍ · 7 NGÀY NẰM VIỆN", sub=("VÍ DỤ GIẢ ĐỊNH", [1, "tổng"]), src=HYP),
    photo("ai02", 2, [0.55, 0.3], [("CHỈ ĐỂ VẼ THÁC CHI PHÍ", 2, "sm"), ("KHÔNG PHẢI BÁO GIÁ", 3, "acc")], move="pan"),
    ledger([4, "tách"], "HAI CHIẾC HỘP", [("HỘP 1", "TRONG PHẠM VI BHYT", [4, "tách"]), ("HỘP 2", "KHOẢN ĐI CÙNG ĐỢT NẰM VIỆN", 6)]),
    kin([6, "nhưng"], "KHÔNG PHẢI “BẢO HIỂM TỪ CHỐI”", ("ranh giới giữa hai hộp", 7)),
    wf(8, "HAI DÒNG THÀNH HÓA ĐƠN", ("TRONG PHẠM VI", COV, 8), [("NGOÀI PHẠM VI", OUT, 9)], ("TỔNG HÓA ĐƠN", 10),
       [(2, TR(TOT), [10, "ba"])]),
    photo("ai05", 11, [0.5, 0.28], [("HÓA ĐƠN ≠ GÁNH NẶNG", 11, "acc")], reveal={"kind": "circle", "at": 11, "d": 0.9}),
    bars(12, "CỘNG THÊM NGOÀI HÓA ĐƠN", [("TỔNG HÓA ĐƠN", TOT, vn(TOT), 12, False),
                                         ("ĐI LẠI · ĂN Ở · NGHỈ LÀM", EXTRA, TR(EXTRA), [12, "hai"], True)]),
    myth(13, "“QUỸ KHÔNG TRẢ” 2 TRIỆU", "NGOÀI CHI PHÍ KCB BHYT", [14, "gộp"], 15, mlab="ĐỪNG GỘP VÀO"),
    timeline(16, "MỘT LẦN NẰM VIỆN", [("7 NGÀY", "nằm viện", 16), ("5 DÒNG", "chi khám chữa bệnh", 17),
                                     ("3 KHOẢN", "ngoài hóa đơn", [17, "ba"])]),
    ledger(18, "HỒ SƠ CỦA VÍ DỤ", [("NGÀY NẰM VIỆN", "7", 18), ("DÒNG CHI KCB", "5", [18, "năm"]),
                                    ("KHOẢN NGOÀI HÓA ĐƠN", "3", [18, "ba"])]),
    bars(19, "CHƯA TRỪ ĐỒNG NÀO", [("TỔNG HÓA ĐƠN", TOT, vn(TOT), 19, False), ("ĐÃ TRỪ", 0, "0", [19, "đồng"], True)]),
    question(21, "“TRONG PHẠM VI”\nDO LUẬT NÀO ĐỊNH NGHĨA?"),
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "ĐỌC ĐÚNG MỐC LUẬT"}, "bgm": {"mood": "calm", "gain": 0.1}, "scenes": [
    chap("2", "CHƯƠNG HAI", "ĐỌC ĐÚNG\nMỐC LUẬT", "LUẬT 51/2024/QH15", vid="6011532"),
    timeline(1, "LUẬT 51/2024/QH15", [("27/11/2024", "ban hành", 1), ("01/07/2025", "có hiệu lực", 2)], src=S_LAW),
    ledger(3, "LUẬT 51 SỬA GÌ", [("SỬA ĐỔI", "LUẬT BHYT CŨ", 3), ("CÙNG VỚI", "CÁC LẦN SỬA TRƯỚC ĐÓ", [3, "các"])], src=S_LAW),
    kin(4, "MỐC HIỆU LỰC", ("không dừng ở một quy tắc cũ", 5)),
    bars(6, "TRƯỚC KHI TRỪ TIỀN QUỸ", [("TỔNG VÍ DỤ", TOT, vn(TOT), 6, False),
                                        ("QUỸ TRẢ?", FUND, f"{vn(FUND)} · NẾU ĐÚNG PHẠM VI", [7, "trừ"], True)],
         calls=[(1, "PHẢI HỎI TRƯỚC", [7, "hỏi"])]),
    broll(8, "7598737", [("QUY TẮC", 8, "acc"), ("không phải mẹo tối ưu hóa đơn", [8, "không"], "sm")]),
    timeline(9, "BA MỐC CẦN ĐỂ RIÊNG", [("ĐẦU 2025", "một số quy định của nghị định", 9),
                                        ("07/2025", "luật mới và nghị định hướng dẫn", 11)], src=S_BHXH),
    timeline(12, "MỐC THỨ BA: 07/2026", [("01/07/2026", "mức tham chiếu thay đổi", 12), ("NGOẠI TRÚ", "một số quy tắc mới", [12, "ngoại"])],
             src=S_BHXH),
    ledger(14, "HAI VĂN BẢN HƯỚNG DẪN", [("NĐ 188/2025/NĐ-CP", "HƯỚNG DẪN LUẬT BHYT", 14),
                                         ("TT 01/2025/TT-BYT", "ĐĂNG KÝ, CHUYỂN CƠ SỞ", 15)], src=S_BHXH),
    myth(16, "MỌI HÓA ĐƠN THÀNH MIỄN PHÍ", "XÁC ĐỊNH ĐƯỜNG ĐI VÀ PHẠM VI", [16, "biến"], 17),
    ledger(18, "MỖI MỐC MỘT VIỆC", [("ĐẦU 2025", "QUY ĐỊNH CỦA NGHỊ ĐỊNH", 18), ("07/2025", "LUẬT MỚI", [18, "tháng"]),
                                    ("07/2026", "MỘT MỐC KHÁC", 19)], src=S_BHXH),
    wf(20, "THÁC CỦA MINH · CHỈ GẮN NHÃN", ("TỔNG", TOT, 20), [("QUỸ TRẢ", -FUND, [20, "nhãn"])],
       calls=[(1, "NHÃN 01/07/2025", [20, "biểu"])]),
    question(22, "80% · 95% · 100%\nCỦA PHẦN NÀO?"),
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "TỶ LỆ KHÔNG PHỦ CẢ HÓA ĐƠN"}, "bgm": {"mood": "curious", "gain": 0.1}, "scenes": [
    chap("3", "CHƯƠNG BA", "TỶ LỆ KHÔNG PHỦ\nCẢ HÓA ĐƠN", "MỨC HƯỞNG TRONG PHẠM VI", bg="ai02"),
    bars([0, "cột"], "BA MỨC HƯỞNG BHYT", [("MỨC 80%", 80, "80%", [0, "cột"], False), ("MỨC 95%", 95, "95%", [0, "dễ"], False),
                                           ("MỨC 100%", 100, "100%", [0, "nhìn"], True)],
         unit="% CHI PHÍ TRONG PHẠM VI", src=S_BHXH, calls=[(2, "TRONG PHẠM VI", [1, "phạm"])]),
    photo("ai03", 2, [0.5, 0.35], [("KHÔNG DÁN LÊN CẢ HÓA ĐƠN", 2, "acc"), (f"bóc từng lớp của {vn(TOT)} triệu", 3, "sm")], move="pan"),
    wf(5, "LỚP TRONG PHẠM VI", ("TRONG PHẠM VI", COV, 5), [(f"QUỸ TRẢ {RATE:.0%}", -FUND, [6, "quỹ"])], ("ĐỒNG CHI TRẢ", 7, "down"),
       [(2, f"CÒN {TR(COPAY)}", [7, "đồng"])]),
    stack(8, f"BA LỚP CỦA {TR(TOT)}", ["QUỸ TRẢ", "ĐỒNG CHI TRẢ", "NGOÀI PHẠM VI"], [("HÓA ĐƠN", [FUND, COPAY, OUT], 8)],
          [(0, f"LỚP KHÁC: {vn(OUT)}", [8, "lớp"])]),
    bars([9, "tám"], "80% CỦA PHẦN NÀO?", [(f"{RATE:.0%} × {vn(COV)} TRIỆU", FUND, f"{vn(FUND)} · ĐÚNG", [9, "tám"], True),
                                           (f"{RATE:.0%} × {vn(TOT)} TRIỆU", RATE * TOT, f"{vn(RATE * TOT)} · KHÔNG PHẢI", [9, "ba"], False)]),
    myth(11, "100% = 7 NGÀY MIỄN HẾT", "100% TRONG PHẠM VI · CÓ ĐIỀU KIỆN", [11, "không"], 12),
    ledger(12, "MỨC 100%: ĐỦ CÁC ĐIỀU KIỆN", [("1", "THAM GIA 5 NĂM LIÊN TỤC", 12), ("2", "KCB ĐÚNG QUY ĐỊNH", 13),
                                               ("3", "CÙNG CHI TRẢ > 6 LẦN THAM CHIẾU", 14)], src=S_BHXH),
    counter(15, T["reference_monthly"], " TRIỆU", "MỨC THAM CHIẾU MỖI THÁNG", sub=("TỪ 01/07/2026", 15)),
    bars(16, "NGƯỠNG 6 LẦN THAM CHIẾU", [("THAM CHIẾU / THÁNG", T["reference_monthly"], vn(T["reference_monthly"]), 16, False),
                                          (f"{T['multiple']} LẦN · CÙNG CHI TRẢ / NĂM", T["threshold"], vn(T["threshold"]), [16, "mười"], True)],
         unit="TRIỆU ĐỒNG", src=S_BHXH),
    kin(17, "KHÔNG PHẢI BẢNG GIÁ", (f"5 năm · 6 lần · {vn(T['reference_monthly'])} · {vn(T['threshold'])} đi cùng nhau", 18)),
    broll(20, "36718656", [("KHÔNG KHẲNG ĐỊNH ĐẠT NGƯỠNG", 20, "acc")]),
    dots([21, "vẽ"], f"{int(COV)} CHẤM = {int(COV)} TRIỆU TRONG PHẠM VI", int(COV), 5,
         [(0, int(FUND), "gold", f"{int(FUND)} TRIỆU QUỸ TRẢ", [21, "vẽ"])]),
    counter(22, T["threshold"], " TRIỆU", "NGƯỠNG CÙNG CHI TRẢ TRONG NĂM", sub=(f"6 × {vn(T['reference_monthly'])} TRIỆU", 22)),
    question(24, "NƠI · TUYẾN · ĐIỀU KIỆN\nĐỔI CÁCH ĐỌC THẾ NÀO?"),
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "ĐIỀU KIỆN ĐI CÙNG TỶ LỆ"}, "bgm": {"mood": "calm", "gain": 0.1}, "scenes": [
    chap("4", "CHƯƠNG BỐN", "ĐIỀU KIỆN\nĐI CÙNG TỶ LỆ", "NHÃN: TRONG PHẠM VI · ĐÚNG QUY ĐỊNH", bg="ai03"),
    wf(1, f"NHÃN MỚI TRÊN CỘT {vn(FUND)}", ("TỔNG HÓA ĐƠN", TOT, 1), [("QUỸ TRẢ", -FUND, [1, "cột"])],
       calls=[(1, "ĐÚNG QUY ĐỊNH", [1, "phạm"])]),
    photo("ai04", 2, [0.45, 0.45], [("ĐIỀU KIỆN TRƯỚC, SỐ SAU", 3, "acc")], zoom={"x": 0.45, "y": 0.55, "z": 1.5, "at": 3, "d": 1.2}),
    kin(4, "KHÔNG PHẢI LỜI KHUYÊN", ("chỉ là cách đọc chữ trên biểu đồ", 5), ("điều kiện đi cùng tỷ lệ", 6)),
    bars(7, "100% Ở HAI NƠI", [("KCB CẤP BAN ĐẦU · TOÀN QUỐC", 100, "100%", 7, True), ("NỘI TRÚ CẤP CƠ BẢN", 100, "100%", 8, True)],
         unit="% MỨC HƯỞNG", src=S_LAW),
    myth(9, "100% = QUỸ TRẢ CẢ ĐI LẠI", "NGOÀI HÓA ĐƠN VẪN ĐỨNG RIÊNG", 10, 11),
    timeline(12, "NGOẠI TRÚ TỪ 01/07/2026", [("01/07/2026", "quy tắc ngoại trú mới", 12), ("CẤP CƠ BẢN", "quỹ trả 50% mức hưởng", 13),
                                             ("50%", "của mức hưởng, không phải nửa hóa đơn", 14)], src=S_BHXH),
    bars(15, "BA CỘT · BA NHÃN", [("CẤP BAN ĐẦU", 100, "100%", 15, False), ("NỘI TRÚ CẤP CƠ BẢN", 100, "100%", [15, "một", 1], False),
                                  ("NGOẠI TRÚ CẤP CƠ BẢN", 50, "50%", [15, "năm"], True)],
         unit="% MỨC HƯỞNG", src=S_BHXH, calls=[(2, "TỪ 01/07/2026", 16), (0, f"≠ CẢ {TR(TOT)}", 17)]),
    ledger(18, "DANH MỤC CÓ QUY TẮC RIÊNG", [("1", "BỆNH HIẾM", 18), ("2", "HIỂM NGHÈO", [18, "hiểm"]),
                                              ("3", "CẦN PHẪU THUẬT, KỸ THUẬT CAO", [18, "phẫu"])], src=S_BHXH),
    counter(19, 62, " BỆNH", "BỆNH HOẶC NHÓM BỆNH TRONG DANH MỤC"),
    broll(20, "8381605", [("HỒ SƠ CỤ THỂ", 20, "acc"), ("một ví dụ không thay được", 21, "sm")]),
    bars(22, "ĐƯỜNG THÁC GIỮ NGUYÊN", [("TRONG PHẠM VI", COV, vn(COV), 22, False), ("QUỸ TRẢ", FUND, vn(FUND), [22, "quỹ"], True)]),
    question(23, "TRÊN HÓA ĐƠN\nANH THỰC SỰ THẤY GÌ?"),
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "MƯỜI TRIỆU TRÊN HÓA ĐƠN"}, "bgm": {"mood": "mystery", "gain": 0.1}, "scenes": [
    chap("5", "CHƯƠNG NĂM", "MƯỜI TRIỆU\nTRÊN HÓA ĐƠN", f"VÍ DỤ GIẢ ĐỊNH · {TR(TOT)} · 7 NGÀY", vid="8381605"),
    bars(1, "NHẮC LẠI VÍ DỤ CỦA MINH", [("TỔNG 7 NGÀY", TOT, vn(TOT), 1, False), ("TRONG PHẠM VI", COV, vn(COV), 2, True)]),
    wf(3, "PHẦN KHÔNG DO QUỸ TRẢ", ("TỔNG", TOT, 3), [(f"QUỸ TRẢ {RATE:.0%}", -FUND, [3, "quỹ"])], ("KHÔNG DO QUỸ", 4, "down"),
       [(2, TR(BILL), [4, "mười"])]),
    wf(6, f"{vn(BILL)} TRIỆU CÓ HAI LỚP", ("ĐỒNG CHI TRẢ", COPAY, 6), [("NGOÀI PHẠM VI", OUT, 7)], ("TRÊN HÓA ĐƠN", 8, "down"),
       [(2, f"{vn(COPAY)} + {vn(OUT)} = {vn(BILL)}", [8, "mười"])]),
    dots(9, f"MỖI CHẤM 1 TRIỆU · HÓA ĐƠN {vn(TOT)}", int(TOT), 10,
         [(0, int(FUND), "ghost", f"{int(FUND)} TRIỆU QUỸ TRẢ", 9), (int(FUND), int(BILL), "red", f"{int(BILL)} TRIỆU · MỘT PHẦN BA", [9, "phần"])]),
    photo("ai05", 11, [0.45, 0.3], [(TR(EXTRA), 11, "acc"), ("đi lại · ăn ở người nhà · nghỉ làm", [11, "đi"], "sm"),
                                     ("ngoài hóa đơn", 12, "sm")], move="out"),
    wf(13, "GÁNH NẶNG RỘNG HƠN", ("TRÊN HÓA ĐƠN", BILL, 13), [("NGOÀI HÓA ĐƠN", EXTRA, [13, "hai"])], ("GÁNH NẶNG", [13, "thành"]),
       [(2, TR(BURDEN), [13, "thành"])]),
    bars(14, "GẦN CON SỐ ĐẦU VIDEO", [(f"VÍ DỤ: {vn(BURDEN)} / {vn(TOT + EXTRA)} TRIỆU", PCT_BURDEN, f"≈{int(PCT_BURDEN + 0.5)}%", 14, True),
                                      ("CẢ NƯỚC · 2025", O["year_2025"], f"≈{O['year_2025']}%", [14, "bốn"], False)],
         unit="PHẦN TRĂM", src="VÍ DỤ GIẢ ĐỊNH · NGUỒN 40%: BHXH VIỆT NAM"),
    broll(15, "8122597", [("KHÔNG CHỈ “QUỸ TRẢ BAO NHIÊU”", 15, "sm"), ("SỨC ÉP TIỀN MẶT", 16, "acc"), ("gia đình còn xoay bao nhiêu", 17, "sm")]),
    bars(18, "TIỀN TÚI / TỔNG CHI Y TẾ", [("ĐẦU NHỮNG NĂM 2000", O["early_2000s"], f"≈{O['early_2000s']}%", 19, False),
                                          ("NĂM 2025", O["year_2025"], f"≈{O['year_2025']}%", 18, True)],
         unit="PHẦN TRĂM", src=S_BHXH),
    myth(20, f"MINH TRẢ {O['year_2025']}% HAY {O['early_2000s']}%", "CHỈ SỐ TOÀN HỆ THỐNG", [21, "suy"], [21, "trả"], mlab="ĐỪNG SUY RA"),
    ledger(22, "MỖI LỚP ĐỌC RIÊNG", [("ĐỒNG CHI TRẢ", TR(COPAY), 22), ("NGOÀI PHẠM VI", TR(OUT), [22, "ví"]),
                                     ("NGOÀI HÓA ĐƠN", TR(EXTRA), [22, "đọc"])], total=("TỶ LỆ CHUNG CHO MINH", "KHÔNG CÓ", 23)),
    timeline(24, "TRÁCH NHIỆM CỦA CƠ SỞ KCB", [("KIỂM TRA", "quyền lợi, mức hưởng", 24), ("TRƯỚC KHI", "kết thúc lượt KCB hoặc ra viện", [24, "trước"]),
                                               ("VIDEO NÀY", "không xem được hồ sơ của Minh", 25)], src=S_BHXH),
    stack(26, f"{vn(COPAY)} + {vn(OUT)} = {vn(BILL)} · {vn(BILL)} + {vn(EXTRA)} = {vn(BURDEN)}", ["ĐỒNG CHI TRẢ", "NGOÀI PHẠM VI", "NGOÀI HÓA ĐƠN"],
          [("TRÊN HÓA ĐƠN", [COPAY, OUT, 0], 26), ("GÁNH NẶNG", [COPAY, OUT, EXTRA], [26, "rồi"])], [(1, TR(BURDEN), [26, "triệu"])]),
    question(28, "MỌI NGƯỜI ĐÓNG QUỸ RA SAO?\nLỘ TRÌNH 2030 NÓI GÌ?"),
]}

CH["ch06"] = {"hud": {"k": "PHẦN CUỐI", "t": "LỘ TRÌNH KHÔNG XÓA MỌI LỚP"}, "bgm": {"mood": "calm", "gain": 0.1}, "scenes": [
    chap("6", "PHẦN CUỐI", "LỘ TRÌNH KHÔNG\nXÓA MỌI LỚP", "NGHỊ QUYẾT 72-NQ/TW · MỤC TIÊU 2030", bg="ai04"),
    bars(1, "MỨC ĐÓNG BHYT HẰNG THÁNG", [("PHỔ BIẾN", 4.5, "4,5%", 1, True), ("TỐI ĐA", 6, "6%", 2, False)],
         unit="% TIỀN LƯƠNG LÀM CĂN CỨ ĐÓNG", src="NGUỒN: NGHỊ ĐỊNH 188/2025/NĐ-CP · BHXH VIỆT NAM"),
    kin(3, "TỶ LỆ ĐÓNG", ("không phải thước đo quyền lợi của Minh", [3, "công"])),
    wf(4, f"THÁC {vn(TOT)} → {vn(BURDEN)} · VÍ DỤ", ("TỔNG HÓA ĐƠN", TOT, 4),
       [("QUỸ TRẢ", -FUND, [4, "triệu"]), ("NGOÀI HÓA ĐƠN", EXTRA, [4, "và"])], ("GÁNH NẶNG", [4, "mười"]),
       [(3, TR(BURDEN), [4, "mười"])]),
    bars(6, "ĐÓNG THEO HỘ GIA ĐÌNH", [("NGƯỜI 1", HH[0], f"{HH[0]}%", 6, False), ("NGƯỜI 2", HH[1], f"{HH[1]}%", [6, "bảy"], False),
                                      ("NGƯỜI 3", HH[2], f"{HH[2]}%", 7, False), ("NGƯỜI 4", HH[3], f"{HH[3]}%", [8, "năm"], False),
                                      ("TỪ NGƯỜI 5", HH[4], f"{HH[4]}%", [8, "bốn"], True)],
         unit="% MỨC NGƯỜI THỨ NHẤT", src=S_BHXH, calls=[(4, "≠ MỨC HƯỞNG", 10)]),
    counter(11, 95.525, " TRIỆU NGƯỜI", "THAM GIA BHYT · CUỐI 2024", sub=("≈ 94,29% DÂN SỐ", 12)),
    bars(13, "LƯỢT KCB BHYT", [("2024", 183.6, "183,6", 13, False), ("2025", 195.1, "195,1", 14, True)],
         unit="TRIỆU LƯỢT", src="NGUỒN: BÁO CHÍNH PHỦ (2024) · BHXH VIỆT NAM (2025)"),
    bars(15, "CHI TỪ QUỸ BHYT", [("2024 · CHI QUỸ", 140, "≈140", 15, False), ("2025 · ĐỀ NGHỊ THANH TOÁN", 166.4, "166,4", [15, "một"], True)],
         unit="NGHÌN TỶ ĐỒNG", src="NGUỒN: BÁO CHÍNH PHỦ (2024) · BHXH VIỆT NAM (2025)"),
    broll(16, "8122597", [("QUY MÔ HỆ THỐNG", 16, "acc"), ("không dự báo hóa đơn của một người", [16, "không"], "sm")]),
    timeline(18, "NGHỊ QUYẾT 72-NQ/TW", [("09/09/2025", "ban hành", 18), ("ĐẾN 2030", "miễn chi phí KCB cơ bản trong phạm vi", 19)], src=S_GOV),
    myth(20, "MIỄN PHÍ TUYỆT ĐỐI MỌI KHOẢN", "MỨC CƠ BẢN · TRONG PHẠM VI", [20, "tuyệt"], [20, "đi"]),
    ledger(21, "ĐỊNH HƯỚNG TỪ 2026", [("1", "TĂNG DẦN TỶ LỆ VÀ MỨC THANH TOÁN", 21), ("2", "TĂNG CHI PHÒNG BỆNH, CHẨN ĐOÁN SỚM", 22),
                                      ("3", "MỘT SỐ BỆNH, ĐỐI TƯỢNG ƯU TIÊN", [22, "ưu"])], src=S_GOV),
    kin(23, "LỘ TRÌNH", ("chưa phải quyền lợi đồng loạt", [23, "chưa"]), ("mục tiêu ≠ hóa đơn hôm nay", 24)),
    bars(25, "TIỀN TÚI: THỰC TẾ VÀ MỤC TIÊU", [("ĐẦU NHỮNG NĂM 2000", O["early_2000s"], f"≈{O['early_2000s']}%", 25, False),
                                               ("NĂM 2025", O["year_2025"], f"≈{O['year_2025']}%", [25, "bốn"], True),
                                               ("MỤC TIÊU 2028–2030", O["target_2028_2030_less_than"], f"< {O['target_2028_2030_less_than']}%", 26, False)],
         unit="% TỔNG CHI Y TẾ", src="NGUỒN: BHXH VIỆT NAM · BÁO CHÍNH PHỦ"),
    broll(27, "7598737", [(f"DƯỚI {O['target_2028_2030_less_than']}% LÀ MỤC TIÊU", 27, "acc"), ("chưa phải quyền lợi hôm nay", [27, "chưa"], "sm")]),
    photo("ai06", 28, [0.5, 0.32], [("PHẦN CƠ BẢN TRONG PHẠM VI", 29, "acc"), ("từng lớp vẫn nhìn riêng", 30, "sm")],
          move="in", reveal={"kind": "wipe", "at": 28, "d": 0.9}),
    bars(31, "BA LỚP KHÔNG TỰ BIẾN MẤT", [("ĐỒNG CHI TRẢ", COPAY, vn(COPAY), 31, True), ("NGOÀI PHẠM VI", OUT, vn(OUT), [31, "ngoài"], True),
                                          ("NGOÀI HÓA ĐƠN", EXTRA, vn(EXTRA), [31, "hai"], True)]),
    stack(32, "BỐN CON SỐ CỦA VÍ DỤ", ["QUỸ TRẢ", "TRÊN HÓA ĐƠN", "NGOÀI HÓA ĐƠN"],
          [("HÓA ĐƠN 7 NGÀY", [FUND, BILL, 0], 32), ("GÁNH NẶNG", [0, BILL, EXTRA], [32, "gánh"])], [(1, TR(BURDEN), [32, "gánh"])]),
    ledger(33, "BỐN SỐ NHÌN CÙNG LÚC", [("TỔNG HÓA ĐƠN", TR(TOT), 33), ("QUỸ TRẢ", TR(FUND), [33, "con"]),
                                        ("TRÊN HÓA ĐƠN", TR(BILL), [33, "nhìn"]), ("GÁNH NẶNG", TR(BURDEN), [33, "trước"])]),
]}


SOURCES = [
 "https://vanban.chinhphu.vn/default.aspx?docid=212479&pageid=27160",
 "https://vbpl.moj.gov.vn/vanphongchinhphu/Pages/vbpq-toanvan.aspx?ItemID=172923&Keyword=",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/chuyen-doi-so.aspx?CateID=0&ItemID=25140",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/linh-vuc-bao-hiem-y-te.aspx?CateID=169&ItemID=24217&OtItem=date",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/linh-vuc-bao-hiem-y-te.aspx?CateID=0&ItemID=27248&OtItem=date",
 "https://baohiemxahoi.gov.vn/tintuc/Pages/linh-vuc-bao-hiem-y-te.aspx?CateID=169&ItemID=24202",
 "https://baohiemxahoi.gov.vn/chidaodieuhanh/Pages/thong-tin-bao-chi.aspx?CateID=0&ItemID=26332&OtItem=date",
 "https://baochinhphu.vn/du-kien-lo-trinh-trien-khai-chinh-sach-mien-vien-phi-102251201192347856.htm",
 "https://baochinhphu.vn/nghi-quyet-72-nq-tw-cu-the-hoa-duong-loi-phat-trien-y-te-ben-vung-102250916111514137.htm"]

SPEC = {"title": "Có Bảo Hiểm Y Tế Vẫn Trả 40%: Tiền Viện Phí Đi Đâu?", "channel": "CK",
 "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
 "chart_rules": True, "say": SAY, "imgs": IMGS, "chapters": [f"ch{i:02}" for i in range(7)],
 "youtube": {"titles": ["Có Bảo Hiểm Y Tế Vẫn Trả 40%: Tiền Viện Phí Đi Đâu?", "Tiền Viện Phí Đi Đâu Khi Có Bảo Hiểm Y Tế?", "BHYT Trả Phần Nào Của Hóa Đơn?"],
 "publish_at": "2026-11-20T13:00:00Z", "playlist": "Tiền Bạc 2026 Nói Gì", "category": "27", "thumb": "t1.jpg",
 "summary": "Cuối năm 2024, 94,29% dân số có bảo hiểm y tế, nhưng tiền túi vẫn chiếm khoảng 40% tổng chi y tế. Video bóc một hóa đơn 30 triệu đồng trong ví dụ giả định thành từng lớp: phần trong phạm vi, đồng chi trả, phần ngoài phạm vi và chi phí ngoài hóa đơn, để thấy tiền viện phí đi đâu.",
 "more": ["Nội dung giáo dục, không phải tư vấn đầu tư.", "Anh Minh và toàn bộ con số hóa đơn là ví dụ giả định, không phải báo giá hay tư vấn y tế. Quyền lợi thực tế phụ thuộc hồ sơ và quy định áp dụng."],
 "chapter_titles": {"ch00": "Con số không nằm ở đầu hóa đơn", "ch01": "Tổng hóa đơn không phải một cục tiền", "ch02": "Đọc đúng mốc luật",
                    "ch03": "Tỷ lệ không phủ cả hóa đơn", "ch04": "Điều kiện đi cùng tỷ lệ", "ch05": "Mười triệu trên hóa đơn",
                    "ch06": "Lộ trình không xóa mọi lớp tiền"},
 "sources": SOURCES, "tags": ["bảo hiểm y tế", "viện phí", "chi phí y tế", "tài chính cá nhân"], "hashtags": ["BảoHiểmYTế", "ViệnPhí", "BiểuĐồBiếtNói"],
 "data_credit": "Quy định và số liệu từ các nguồn công khai; hóa đơn của anh Minh là ví dụ giả định.",
 "video_credits": "Video minh họa: Pexels. Ảnh minh họa: AI."}}


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, chapter in CH.items():
        path = D / f"{name}.json"
        old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        old.update(chapter)
        path.write_text(json.dumps(old, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương,", sum(len(c["scenes"]) for c in CH.values()), "cảnh")


if __name__ == "__main__":
    main()
