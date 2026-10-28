"""Dựng cảnh cho ck-f4-vo-chong-chia-tien. Số của Thảo–Nam chỉ lấy từ results.json; số nghiên cứu/luật lấy từ facts.md.

27/10 (dựng lại): mở bằng câu hỏi thật + nghiên cứu thật (không nhân vật ở CH00); mỗi cảnh hiện đúng con số đang đọc.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
A, EQ, PRO, POOL = R["assume"], R["equal"], R["proportional"], R["pool"]
MC, PCT, SENS = R["monthly_chart"], R["cost_share_pct"], R["sensitivity"]
TH, NA, COST, MON = A["thao_income"], A["nam_income"], A["common_cost"], A["months"]
LEFT = R["remaining_after_cost"]

# kiểm khớp ngay khi sinh cảnh (check.py kiểm độc lập)
assert TH + NA == R["total_income"] and R["total_income"] - COST == LEFT
assert EQ["thao_contrib"] + EQ["nam_contrib"] == COST == PRO["thao_contrib"] + PRO["nam_contrib"]
assert POOL["thao_left"] + POOL["nam_left"] + POOL["common_left"] == LEFT
TOTAL12 = LEFT * MON
for plan in (EQ, PRO, POOL):
    assert sum(plan["month_12"].values()) == TOTAL12
assert PCT["proportional_thao"] == PCT["proportional_nam"]

GOLD, BLUE = "#fbbf24", "#38bdf8"
VM, ILL, HYP = "VIDEO MINH HỌA", "ẢNH MINH HỌA", "VÍ DỤ GIẢ ĐỊNH"
RANGE = "TRIỆU ĐỒNG · " + HYP
SRC_HYP = HYP + " · KÊNH TỰ TÍNH"
# nguồn thật (facts.md S1–S9, factcheck.md)
GLAD = "NGUỒN: GLADSTONE, GARBINSKY & MOGILNER · JPSP 2022"
VOG = "NGUỒN: VOGLER, LYONETTE & WIGGINS · 2008"
BUR = "NGUỒN: BURGOYNE VÀ CỘNG SỰ · 2006"
LAUER = "NGUỒN: LAUER · JOURNAL OF MARRIAGE AND FAMILY 2011"
BLEK = "NGUỒN: BLEKESAUNE · PLOS ONE 2018"
LAW = "NGUỒN: LUẬT HÔN NHÂN VÀ GIA ĐÌNH 52/2014/QH13"
GSO24 = "NGUỒN: TỔNG CỤC THỐNG KÊ · THÔNG CÁO NĂM 2024"
GSO22 = "NGUỒN: TỔNG CỤC THỐNG KÊ · KSMS 2022"
GLAD_N, GLAD_STUDIES = 38534, 6                   # facts #21
GLAD_SEP, GLAD_JOINT = 22, 18                    # facts #23: +22% (tách), −18% (gộp) so với gộp một phần
BUR_COUPLES = [("GỘP TOÀN BỘ / HẦU HẾT", 6), ("GỘP MỘT PHẦN", 15), ("ĐỘC LẬP", 20), ("MỘT BÊN KIỂM SOÁT", 1)]   # facts #25
LAUER_N, LAUER_CTX = 18587, 31                   # facts #26
MIN_LIVING_2024 = 2.3                            # facts #30


def vn(x):
    """Số kiểu Việt: 5.25 -> "5,25", 38534 -> "38.534"."""
    x = round(float(x), 2)
    if x == int(x):
        return f"{int(x):,}".replace(",", ".")
    return f"{x:.2f}".rstrip("0").replace(".", ",")


def cum(plan, who):
    """Cộng dồn tháng 0..12 (tháng 0 = 0) từ results.json monthly_chart."""
    return [0.0] + [m[plan][who] for m in MC]


EQ12, PRO12, POOL12 = EQ["month_12"], PRO["month_12"], POOL["month_12"]
B6 = {"eq": [EQ12["thao_left"], EQ12["nam_left"], 0], "pro": [PRO12["thao_left"], PRO12["nam_left"], 0],
      "pool": [POOL12["thao_left"], POOL12["nam_left"], POOL12["common_left"]]}
K3 = [{"k": "THẢO"}, {"k": "NAM"}, {"k": "QUỸ CHUNG"}]
K2 = [{"k": "THẢO"}, {"k": "NAM"}]
S = {x["cost"]: x for x in SENS}


# ---------------- helper cảnh ----------------
def chap(no, word, title, sub, vid):
    return {"type": "chapter", "no": no, "k": "PHẦN CUỐI" if no == "6" else f"CHƯƠNG {word}", "title": title, "sub": sub,
            "vid": vid, "illus": VM, "titleAt": 0}


def bars(at, title, items, unit="TRIỆU · " + HYP, src=SRC_HYP):
    """items: (nhãn, giá trị, chữ trên cột, at, nhấn?)"""
    return {"type": "bars", "at": at, "title": title, "unit": unit, "srcnote": src,
            "items": [{"k": k, "v": v, "lbl": l, "at": a, **({"acc": True} if acc else {})} for k, v, l, a, acc in items]}


def stack(at, title, groups, calls=(), keys=K3):
    """groups: (nhãn cột, vals, at); calls: (chỉ số cột, chữ, at[, tone])"""
    return {"type": "stack", "at": at, "title": title, "range": RANGE, "unit": "TRIỆU", "keys": keys,
            "groups": [{"k": k, "vals": v, "at": a} for k, v, a in groups],
            "calls": [{"i": c[0], "text": c[1], "at": c[2], **({"tone": c[3]} if len(c) > 3 else {})} for c in calls]}


def wf(at, title, start, steps, end, calls):
    """start: (nhãn, v>0, at); steps: (nhãn, v, at); end: (nhãn, at[, tone]); calls i: 0 đầu, 1..n bước, n+1 cuối."""
    e = {"k": end[0], "at": end[1], **({"tone": end[2]} if len(end) > 2 else {})}
    return {"type": "waterfall", "at": at, "title": title, "range": RANGE, "unit": "TRIỆU",
            "start": {"k": start[0], "v": start[1], "at": start[2]},
            "steps": [{"k": k, "v": v, "at": a} for k, v, a in steps], "end": e,
            "calls": [{"i": c[0], "text": c[1], "at": c[2], **({"tone": c[3]} if len(c) > 3 else {})} for c in calls]}


def race(at, title, series, calls):
    """12 tháng cộng dồn, trục THÁNG 0..12; calls: (series, tháng, chữ, at)"""
    return {"type": "race", "at": at, "abs": True, "unit": "TRIỆU", "xlab": "THÁNG ", "xstep": 3,
            "dates": [str(i) for i in range(MON + 1)], "title": title, "range": "CỘNG DỒN · " + RANGE,
            "series": [{"label": l, "color": c, "vals": v} for l, c, v in series],
            "calls": [{"s": s, "i": i, "text": t, "at": a} for s, i, t, a in calls]}


def dots(at, title, total, cols, groups, src):
    """groups: (from, n, cls, nhãn, at) -- mỗi chấm một triệu đồng / một phần trăm"""
    return {"type": "dots", "at": at, "title": title, "total": total, "cols": cols, "srcnote": src,
            "groups": [{"from": f, "n": n, "cls": c, "label": l, "at": a} for f, n, c, l, a in groups]}


def ledger(at, title, rows, src=SRC_HYP):
    return {"type": "ledger", "at": at, "title": title, "srcnote": src, "rows": [{"k": k, "v": v, "at": a} for k, v, a in rows]}


def counter(at, to, label, src, suffix="", sub=None):
    s = {"type": "counter", "at": at, "from": 0, "to": to, "label": label, "srcnote": src}
    if suffix:
        s["suffix"] = suffix
    if sub:
        s["sub"] = {"text": sub[0], "at": sub[1]}
    return s


def kin_items(items):
    out = []
    for t, a, style in items:
        x = {"text": t, "at": a}
        if style:
            x[style] = True
        out.append(x)
    return out


def broll(at, vid, items):
    """b-roll luôn mang từ khoá (kin), không để clip trống thông tin"""
    return {"type": "broll", "at": at, "vid": vid, "veil": .55, "illus": VM, "kin": kin_items(items)}


def photo(img, at, focus, items=None, move=None, reveal=None, zoom=None, label=None):
    s = {"type": "photo", "img": img, "at": at, "credit": False, "illus": ILL, "focus": focus}
    for k, v in (("move", move), ("reveal", reveal), ("zoom", zoom), ("label", label)):
        if v:
            s[k] = v
    if items:
        s["veil"] = .35
        s["kin"] = kin_items(items)
    return s


def kinetic(at, items):
    return {"type": "kinetic", "at": at, "items": kin_items(items)}


def question(at, text):
    return {"type": "question", "at": at, "text": text}


def timeline(at, title, items, src=None):
    s = {"type": "timeline", "at": at, "title": title, "items": [{"year": y, "text": t, "at": a} for y, t, a in items]}
    if src:
        s["srcnote"] = src
    return s


# ---------------- số dùng nhiều lần ----------------
GAP_M = EQ["nam_left"] - EQ["thao_left"]            # 10 triệu/tháng
SHIFT = PRO12["thao_left"] - EQ12["thao_left"]      # +39
assert SHIFT == EQ12["nam_left"] - PRO12["nam_left"]
PAID12 = EQ["thao_contrib"] * MON                   # 156
SH_T = PRO["thao_contrib"] / COST * 100             # 37,5
SH_N = PRO["nam_contrib"] / COST * 100              # 62,5

CH = {}
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "GỘP HAY GIỮ RIÊNG?"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    # mở bằng câu hỏi thật và nghiên cứu thật -- Thảo–Nam chỉ vào từ CH01
    broll(0, "6963493", [("GỘP CHUNG?", 0, "acc"), ("HAY GIỮ RIÊNG?", [0, "giữ"], None)]),
    counter(1, GLAD_N, f"NGƯỜI THAM GIA · {GLAD_STUDIES} NGHIÊN CỨU", GLAD, sub=("CÙNG ĐO MỘT CÂU HỎI", [1, "đo"])),
    ledger(2, "NHÓM NÀO HÀI LÒNG HƠN?", [("GỘP TOÀN BỘ", "HÀI LÒNG QUAN HỆ CAO HƠN", [2, "gộp"]),
                                        ("TÁCH MỘT PHẦN / TOÀN BỘ", "THẤP HƠN", [2, "tách"])], GLAD),
    broll(3, "6963962", [("LIÊN HỆ TRONG NGHIÊN CỨU", 3, "sm"), ("KHÔNG PHẢI LỜI HỨA", [3, "lời"], "acc")]),
    question(4, "Chia tiền vợ chồng:\nvì sao không có một đáp án?"),
    bars(5, f"CHIA ĐÔI HÓA ĐƠN {vn(COST)} TRIỆU", [
        (f"LƯƠNG {vn(NA)} TRIỆU", EQ["nam_left"], f"CÒN {vn(EQ['nam_left'])}", [5, "chia"], False),
        (f"LƯƠNG {vn(TH)} TRIỆU", EQ["thao_left"], f"CÒN {vn(EQ['thao_left'])}", [5, "thấp"], True)],
        unit="TRIỆU CÒN LẠI · " + HYP),
    timeline(6, "BA BẢNG · MỘT HÓA ĐƠN", [("1 HÓA ĐƠN", "giữ nguyên", 6), ("BẢNG 1", "cùng số tiền", [6, "tiền"]),
                                         ("BẢNG 2", "cùng tỷ lệ thu nhập", [6, "tỷ"]), ("BẢNG 3", "riêng hay chung", [6, "riêng"])]),
    kinetic(7, [("CHIA ĐÔI = CÔNG BẰNG?", 7, "acc"), ("ai hết tiền trước?", [7, "hết"], "sm")]),
    {"type": "brand", "at": 8, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "VÍ THỨ NHẤT · CÙNG GÓP MỘT SỐ"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    chap("1", "MỘT", "VÍ THỨ NHẤT\nCÙNG GÓP MỘT SỐ", HYP, "6963962"),
    photo("ai01", 1, [.5, .32], reveal={"kind": "circle", "at": 1, "d": .9},
          label={"k": HYP, "v": f"THẢO {vn(TH)} TRIỆU · NAM {vn(NA)} TRIỆU", "at": [1, "thảo"]}),
    bars(2, "THU NHẬP VÀ CHI CHUNG", [("THẢO", TH, vn(TH), 2, False), ("NAM", NA, vn(NA), 2, False),
                                      ("CHI CHUNG", COST, vn(COST), [2, "sáu"], True)], unit="TRIỆU/THÁNG · " + HYP),
    stack(3, f"CHIA ĐỀU {vn(COST)} TRIỆU", [("MỖI THÁNG", [EQ["thao_contrib"], EQ["nam_contrib"]], 3)],
          [(0, f"{vn(COST)} ÷ 2 = {vn(EQ['thao_contrib'])}", 4)], keys=K2),
    wf(7, "THẢO · CHIA ĐỀU", ("LƯƠNG THẢO", TH, 7), [("GÓP CHUNG", -EQ["thao_contrib"], [7, "mất"])], ("CÒN LẠI", 8, "down"),
       [(2, f"CÒN {vn(EQ['thao_left'])} TRIỆU", 8, "down")]),
    wf(9, "NAM · CHIA ĐỀU", ("LƯƠNG NAM", NA, 9), [("GÓP CHUNG", -EQ["nam_contrib"], [9, "mất"])], ("CÒN LẠI", 10),
       [(2, f"CÒN {vn(EQ['nam_left'])} TRIỆU", 10)]),
    bars(11, "CÒN LẠI MỖI THÁNG", [("THẢO", EQ["thao_left"], vn(EQ["thao_left"]), 11, False),
                                    ("NAM", EQ["nam_left"], vn(EQ["nam_left"]), 11, False),
                                    ("CHÊNH LỆCH", GAP_M, vn(GAP_M), 12, True)]),
    photo("ai04", 13, [.42, .32], [("KHÔNG PHẢI LỖI TÍNH", 13, "sm"), ("KẾT QUẢ CỦA QUY TẮC", 14, "acc")], move="in"),
    race(15, "CHIA ĐỀU · 12 THÁNG", [("THẢO", "#f472b6", cum("equal", "thao")), ("NAM", BLUE, cum("equal", "nam"))],
         [(0, MON, f"THẢO {vn(EQ12['thao_left'])}", [15, "để"]), (1, MON, f"NAM {vn(EQ12['nam_left'])}", 16)]),
    stack(17, "12 THÁNG: GÓP VÀ CÒN", [("CÒN RIÊNG", [EQ12["thao_left"], EQ12["nam_left"]], 17),
                                       ("ĐÃ GÓP CHI CHUNG", [PAID12, EQ["nam_contrib"] * MON], 18)],
          [(0, f"{vn(EQ12['thao_left'])} ≠ {vn(EQ12['nam_left'])}", 19, "down")], keys=K2),
    ledger(21, "QUẢN LÝ ĐỘC LẬP", [("NGHIÊN CỨU", "VOGLER, LYONETTE & WIGGINS · 2008", 21),
                                   ("THU NHẬP", "MỖI NGƯỜI GIỮ PHẦN RIÊNG", 22), ("MỤC CHI", "MỖI NGƯỜI CHỊU PHẦN ĐÃ ĐỊNH", [22, "chịu"])], VOG),
    broll(23, "6963484", [("“CÔNG BẰNG”", 23, "sm"), ("GÓP BẰNG NHAU", [23, "góp"], "acc"), ("mô tả, không chấm điểm", 24, "sm")]),
    dots(26, f"LƯƠNG THẢO: {vn(TH)} CHẤM", int(TH), int(TH),
         [(0, int(EQ["thao_contrib"]), "red", f"GÓP {vn(EQ['thao_contrib'])} ≈ {vn(PCT['equal_thao'])}% LƯƠNG", 26),
          (int(EQ["thao_contrib"]), int(EQ["thao_left"]), "hollow", f"CÒN {vn(EQ['thao_left'])}", [26, "lương"])],
         "MỖI CHẤM = 1 TRIỆU · " + HYP),
    dots(27, f"LƯƠNG NAM: {vn(NA)} CHẤM", int(NA), int(NA),
         [(0, int(EQ["nam_contrib"]), "red", f"GÓP {vn(EQ['nam_contrib'])} = {vn(PCT['equal_nam'])}% LƯƠNG", 27),
          (int(EQ["nam_contrib"]), int(EQ["nam_left"]), "hollow", f"CÒN {vn(EQ['nam_left'])}", [27, "lương"])],
         "MỖI CHẤM = 1 TRIỆU · " + HYP),
    bars(28, f"{vn(EQ['thao_contrib'])} TRIỆU NẶNG BAO NHIÊU?", [
        ("THẢO", PCT["equal_thao"], f"{vn(PCT['equal_thao'])}%", 28, True),
        ("NAM", PCT["equal_nam"], f"{vn(PCT['equal_nam'])}%", [28, "chấm"], False)], unit="% LƯƠNG ĐEM GÓP · " + HYP),
    broll(30, "6963478", [("AI PHẢI ĐỔI CÁCH?", 30, "sm"),
                          (f"VÍ THỨ NHẤT: CÒN {vn(EQ['thao_left'])} VÀ {vn(EQ['nam_left'])}", [31, "hai"], "acc")]),
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "VÍ THỨ HAI · CÙNG CHỊU MỘT TỶ LỆ"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    chap("2", "HAI", "VÍ THỨ HAI\nCÙNG CHỊU MỘT TỶ LỆ", HYP + " · THEO THU NHẬP", "7735859"),
    bars(1, "TỶ TRỌNG THU NHẬP", [("THẢO", SH_T, f"{vn(SH_T)}%", [1, "bảy"], False), ("NAM", SH_N, f"{vn(SH_N)}%", [2, "sáu"], False),
                                  ("CỘNG LẠI", SH_T + SH_N, f"{vn(SH_T + SH_N)}%", [4, "một"], True)],
         unit=f"% CỦA {vn(TH + NA)} TRIỆU · " + HYP),
    wf(5, f"{vn(COST)} TRIỆU THEO TỶ TRỌNG", ("CHI CHUNG", COST, 5),
       [("THẢO GÓP", -PRO["thao_contrib"], [5, "thảo"]), ("NAM GÓP", -PRO["nam_contrib"], 6)], ("CÒN PHẢI TRẢ", 7),
       [(3, "ĐỦ HÓA ĐƠN", 8)]),
    bars(9, "TỶ TRỌNG: CÒN MỖI THÁNG", [("THẢO", PRO["thao_left"], vn(PRO["thao_left"]), 9, False),
                                         ("NAM", PRO["nam_left"], vn(PRO["nam_left"]), 10, True)]),
    dots(12, "MỖI 100 ĐỒNG LƯƠNG", 100, 20,
         [(0, int(PCT["proportional_thao"]), "gold", f"CẢ HAI: {vn(PCT['proportional_thao'])}% VÀO CHI CHUNG", 12),
          (int(PCT["proportional_thao"]), 100 - int(PCT["proportional_thao"]), "hollow",
           f"{vn(100 - PCT['proportional_thao'])}% CÒN LẠI", [12, "thu"])], "MỖI CHẤM = 1% LƯƠNG · " + HYP),
    photo("ai03", 14, [.5, .35], [("ĐỔI NGHĨA CHỮ “CÙNG”", 15, "acc"), ("tổng tiền không đổi", 16, "sm")], move="pan"),
    race(17, "TỶ TRỌNG · 12 THÁNG", [("THẢO", "#f472b6", cum("proportional", "thao")), ("NAM", BLUE, cum("proportional", "nam"))],
         [(0, 6, f"6 THÁNG: {vn(MC[5]['proportional']['thao'])}", [17, "thảo"]), (1, 6, f"6 THÁNG: {vn(MC[5]['proportional']['nam'])}", 18),
          (0, MON, f"THẢO {vn(PRO12['thao_left'])}", 19), (1, MON, f"NAM {vn(PRO12['nam_left'])}", [19, "trăm"])]),
    stack(20, "THÁNG 12: HAI NHÁNH", [("CHIA ĐỀU", B6["eq"][:2], 20), ("TỶ TRỌNG", B6["pro"][:2], [20, "thứ"])],
          [(1, f"THẢO +{vn(SHIFT)} · NAM −{vn(SHIFT)}", 22)], keys=K2),
    counter(23, sum(PRO12.values()), "TỔNG HAI KHOẢN RIÊNG · 12 THÁNG", SRC_HYP, " TRIỆU",
            (f"= {vn(LEFT)} TRIỆU × {MON} THÁNG", 25)),
    broll(26, "6963967", [("KHÔNG CÓ TIỀN MỚI", 26, "acc"), ("chỉ đổi cách phân phần còn lại", 27, "sm")]),
    ledger(28, "NHÃN TRONG NGHIÊN CỨU", [("GỘP", "TIỀN VÀO MỘT CHỖ", [28, "gộp"]), ("TÁCH", "MỖI NGƯỜI GIỮ RIÊNG", [28, "tách"]),
                                         ("GỘP MỘT PHẦN", "VỪA CHUNG VỪA RIÊNG", [28, "phần"])],
           "NGUỒN: VOGLER VÀ CỘNG SỰ 2008 · GLADSTONE VÀ CỘNG SỰ 2022"),
    kinetic(30, [("KHÔNG PHẢI CÔNG THỨC", 30, "acc"), ("cho mọi gia đình ở Việt Nam", [30, "mọi"], "sm")]),
    ledger(32, "VÍ THỨ HAI · PHẠM VI HẸP", [("PHẠM VI", "MỘT BỘ SỐ " + HYP, 32),
                                            ("THU NHẬP", f"{vn(TH)} VÀ {vn(NA)}", [33, "mười"]), ("CHI CHUNG", vn(COST), [33, "sáu"]),
                                            ("SỐ DƯ", f"{vn(PRO['thao_left'])} VÀ {vn(PRO['nam_left'])}", [33, "số"])]),
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "VÍ THỨ BA · MỘT QUỸ, HAI PHẦN RIÊNG"}, "bgm": {"mood": "warm", "gain": .10}, "scenes": [
    chap("3", "BA", "VÍ THỨ BA\nMỘT QUỸ, HAI PHẦN RIÊNG", HYP + " · GỘP MỘT PHẦN", "6963485"),
    wf(1, "QUỸ CHUNG MỘT THÁNG", ("CẢ HAI LƯƠNG", R["total_income"], 1), [("CHI CHUNG", -COST, 2)], ("QUỸ CÒN", 3),
       [(2, f"CÒN {vn(POOL['after_cost'])}", 3)]),
    wf(4, f"{vn(POOL['after_cost'])} TRIỆU CHIA BA PHẦN", ("SAU CHI CHUNG", POOL["after_cost"], 4),
       [("THẢO RIÊNG", -POOL["thao_left"], [4, "thảo"]), ("NAM RIÊNG", -POOL["nam_left"], 6)], ("QUỸ CHUNG", [7, "quỹ"]),
       [(3, f"QUỸ GIỮ {vn(POOL['common_left'])}", [7, "quỹ"])]),
    stack(9, "MỖI THÁNG: BA PHẦN", [("THÁNG 1", [POOL["thao_left"], POOL["nam_left"], POOL["common_left"]], 9)],
          [(0, f"TỔNG {vn(POOL['after_cost'])}", 10)]),
    photo("ai02", 11, [.5, .5], [("QUỸ CHUNG ≠ VÍ RIÊNG", [11, "cộng"], "acc"), ("không của Thảo, không của Nam", 12, "sm")],
          zoom={"x": .5, "y": .55, "z": 1.35, "at": 11, "d": 1.2}),
    kinetic(14, [("KHÁC BIỆT QUAN TRỌNG NHẤT", 14, "sm"), ("KHÔNG ĐẾM TRÙNG", 15, "acc")]),
    stack(16, "CỘNG DỒN: THÁNG 3 VÀ 6", [("THÁNG 3", list(MC[2]["pool"].values()), 16), ("THÁNG 6", list(MC[5]["pool"].values()), 18)],
          [(0, f"QUỸ {vn(MC[2]['pool']['common'])}", 17), (1, f"QUỸ {vn(MC[5]['pool']['common'])}", 19)]),
    race(20, "BA CỘT CÙNG LỚN LÊN", [("THẢO = NAM", "#f472b6", cum("pool", "thao")), ("QUỸ CHUNG", GOLD, cum("pool", "common"))],
         [(0, MON, f"{vn(POOL12['thao_left'])} MỖI NGƯỜI", 21), (1, MON, f"QUỸ {vn(POOL12['common_left'])}", 22)]),
    counter(23, sum(POOL12.values()), "THẢO + NAM + QUỸ · THÁNG 12", SRC_HYP, " TRIỆU", ("CÁI GỌI LÀ “CỦA RIÊNG” ĐÃ ĐỔI", 24)),
    ledger(25, "GỘP MỘT PHẦN", [("NGHIÊN CỨU", "VOGLER, LYONETTE & WIGGINS", 25), ("LỚP 1", "CHI CHUNG", [25, "chi"]),
                                ("LỚP 2", "QUYỀN TỰ CHỦ", [25, "tự"])], VOG),
    kinetic(27, [(f"MỐC {vn(POOL['thao_left'])} TRIỆU", 27, "acc"), ("chỉ là ví dụ giả định", 28, "sm")]),
    broll(29, "6964248", [("ĐỔI MỐC → ĐỔI CỘT THÁNG 12", 29, "acc"), ("ĐỔI CHI → ĐỔI QUỸ", 30, "acc")]),
    photo("ai06", 31, [.5, .45], [("KHÔNG PHẢI ĐÁP ÁN", 31, "sm"), ("MỘT CÁCH GỌI", 32, "acc")], move="out"),
    question(33, "Phần nào để dùng chung,\nphần nào là khoản riêng?"),
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "KHI BA BẢNG GẶP CHỮ CHUNG"}, "bgm": {"mood": "mystery", "gain": .09}, "scenes": [
    chap("4", "BỐN", "KHI BA BẢNG\nGẶP CHỮ “CHUNG”", "LUẬT 52/2014/QH13 · ĐIỀU 33–35", "9870505"),
    stack(1, "BA NHÁNH · THÁNG 12", [("CHIA ĐỀU", B6["eq"], 1), ("TỶ TRỌNG", B6["pro"], 2), ("QUỸ CHUNG", B6["pool"], 3)]),
    ledger(4, "MỘT TỔNG · BA NHÃN", [
        ("CHIA ĐỀU", f"{vn(B6['eq'][0])} + {vn(B6['eq'][1])} = {vn(TOTAL12)}", 4),
        ("TỶ TRỌNG", f"{vn(B6['pro'][0])} + {vn(B6['pro'][1])} = {vn(TOTAL12)}", [4, "tổng"]),
        ("QUỸ CHUNG", " + ".join(vn(v) for v in B6["pool"]) + f" = {vn(TOTAL12)}", [4, "trăm"])]),
    kinetic(6, [("ĐỨNG CẠNH NHAU", 6, "acc"), ("không phải bảng xếp hạng", [6, "xếp"], "sm"), ("KHÔNG CÓ NGÔI NHẤT", 7, "acc")]),
    ledger(8, "LUẬT HÔN NHÂN VÀ GIA ĐÌNH 2014", [("VĂN BẢN", "LUẬT 52/2014/QH13", 8),
                                                 ("ĐIỀU 33", "THU NHẬP DO LAO ĐỘNG TRONG HÔN NHÂN", 9),
                                                 ("LÀ", "TÀI SẢN CHUNG · TRỪ NGOẠI LỆ LUẬT ĐỊNH", [9, "tài"])], LAW),
    broll(10, "7646693", [("THÔNG TIN VĂN BẢN", 10, "acc"), ("không phải tư vấn cho trường hợp cụ thể", [10, "tư"], "sm")]),
    timeline(12, "ĐIỀU 34 VÀ ĐIỀU 35", [("ĐIỀU 34", "giấy chứng nhận tài sản chung", 12), ("ĐIỀU 35", "vợ chồng thỏa thuận", 13),
                                        ("VĂN BẢN", "một số giao dịch", 14)], LAW),
    broll(15, "9869607", [("MỘT LỚP KHÁC", 15, "sm"), ("CHỈ DỪNG Ở BA ĐIỀU", 16, "acc"), ("KHÔNG ÁP CHO TỪNG NHÀ", 18, "acc")]),
    photo("ai05", 19, [.5, .32], [("“VÍ RIÊNG” = NHÃN CỦA VÍ DỤ", 19, "acc"), ("không thay tên gọi pháp lý", 20, "sm")], move="in"),
    stack(21, f"{vn(POOL12['common_left'])} TRIỆU LÀ CỦA AI?", [("QUỸ CHUNG T12", B6["pool"], 21)],
          [(0, f"{vn(POOL12['common_left'])} VẪN LÀ CHUNG", [21, "không"])]),
    ledger(22, "HAI CON SỐ MINH HỌA", [(f"{MON} THÁNG", "MINH HỌA · KHÔNG PHẢI THỜI HẠN LUẬT", 22),
                                       (f"{vn(COST)} TRIỆU", "CHI GIẢ ĐỊNH, KHÔNG PHẢI CHUẨN", 23)]),
    counter(24, MIN_LIVING_2024, "MỨC SỐNG TỐI THIỂU SƠ BỘ · THÀNH THỊ 2024", GSO24, " TRIỆU",
            ("MỘT NGƯỜI MỖI THÁNG · KHÔNG PHẢI NGÂN SÁCH", 25)),
    broll(26, "4052868", [("MINH HỌA ≠ CHUẨN", 26, "sm"), ("BIỂU ĐỒ KHÔNG RA LỆNH", 27, "acc")]),
    question(28, "Ba cách gọi “của mình”:\nnghiên cứu thấy gì?"),
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "NGHIÊN CỨU THẤY GÌ, KHÔNG THẤY GÌ"}, "bgm": {"mood": "curious", "gain": .10}, "scenes": [
    chap("5", "NĂM", "NGHIÊN CỨU\nTHẤY GÌ, KHÔNG THẤY GÌ", "GLADSTONE VÀ CỘNG SỰ · 2022", "7735862"),
    ledger(1, "GLADSTONE, GARBINSKY & MOGILNER", [("SỐ NGHIÊN CỨU", str(GLAD_STUDIES), 1), ("TỔNG SỐ NGƯỜI", vn(GLAD_N), [1, "ba"]),
                                                  ("SO SÁNH", "GỘP HẾT ↔ TÁCH MỘT PHẦN / HẾT", 2)], GLAD),
    broll(3, "6963493", [("NHÓM GỘP TOÀN BỘ", 3, "sm"), ("HÀI LÒNG QUAN HỆ CAO HƠN", [3, "hài"], "acc")]),
    kinetic(4, [("LIÊN HỆ ĐƯỢC BÁO CÁO", 4, "acc"), ("KHÔNG PHẢI NHÂN QUẢ", 5, "acc"), ("ranh giới của một bảng tính", 6, "sm")]),
    bars(7, "NGUY CƠ CHẤM DỨT QUAN HỆ", [("TÀI KHOẢN TÁCH", 100 + GLAD_SEP, f"+{GLAD_SEP}%", [7, "cao"], False),
                                         ("GỘP MỘT PHẦN", 100, "MỐC SO SÁNH", [8, "so"], False),
                                         ("GỘP TOÀN BỘ", 100 - GLAD_JOINT, f"−{GLAD_JOINT}%", [8, "thấp"], True)],
         unit="CHỈ SỐ · GỘP MỘT PHẦN = 100", src=GLAD + " · PHÂN TÍCH DỌC"),
    broll(9, "6963976", [("MỘT NGHIÊN CỨU QUỐC TẾ", 9, "sm"), ("KHÔNG PHẢI DỰ BÁO CHO TỪNG NHÀ", 10, "acc")]),
    {"type": "myth", "at": 11, "mythLab": "HIỆU ỨNG MẠNH HƠN KHI KHAN HIẾM NGUỒN LỰC", "myth": "MỌI NHÀ THU NHẬP THẤP PHẢI GỘP?",
     "truthLab": "THẬT RA", "truth": "KHÔNG SUY RA ĐƯỢC", "strikeAt": [12, "không"], "truthAt": [12, "suy"], "srcnote": GLAD},
    photo("ai05", 13, [.5, .32], [("GIỚI HẠN ĐỨNG CẠNH CON SỐ", 13, "sm"), ("KHÔNG SUY RỘNG", 14, "acc")], move="out"),
    bars(15, "MẪU PHỎNG VẤN · SỐ CẶP", [(k, v, vn(v), a, False) for (k, v), a in
                                        zip(BUR_COUPLES, [[15, "sáu"], 16, 17, 18])], unit="CẶP · MẪU ĐỊNH TÍNH", src=BUR),
    broll(19, "8122601", [("MẪU ĐỊNH TÍNH NHỎ", 19, "acc"), ("không đại diện cho Việt Nam", 21, "sm")]),
    counter(22, LAUER_N, f"NGƯỜI · {LAUER_CTX} BỐI CẢNH QUỐC GIA", LAUER, sub=("DỮ LIỆU NĂM 2002", [22, "gồm"])),
    ledger(23, "CÁC YẾU TỐ ĐƯỢC QUAN SÁT", [("1", "THU NHẬP", [23, "thu"]), ("2", "CON PHỤ THUỘC", [23, "con"]),
                                            ("3", "LỊCH SỬ QUAN HỆ", [23, "lịch"]), ("4", "THÁI ĐỘ GIỚI", [23, "thái"])], BLEK),
    kinetic(24, [("DANH SÁCH QUAN SÁT", 24, "sm"), ("KHÔNG CÓ CÔNG THỨC CHUNG", 25, "acc")]),
    timeline(26, "BA NHÃN · KHÔNG HUY CHƯƠNG", [("ĐỘC LẬP", "mỗi người giữ riêng", 26),
                                                ("GỘP MỘT PHẦN", "chung và riêng", [26, "phần"]),
                                                ("GỘP TOÀN BỘ", "một ví chung", [26, "toàn"])]),
    stack(28, "QUAY LẠI THẢO VÀ NAM", [("CHIA ĐỀU", B6["eq"], 28), ("TỶ TRỌNG", B6["pro"], [28, "cột"]), ("QUỸ CHUNG", B6["pool"], [28, "giả"])]),
]}

CH["ch06"] = {"hud": {"k": "PHẦN CUỐI", "t": "KHI HÓA ĐƠN ĐỔI, CÂU HỎI CŨNG ĐỔI"}, "bgm": {"mood": "calm", "gain": .10}, "scenes": [
    chap("6", "SÁU", "KHI HÓA ĐƠN ĐỔI", "CÂU HỎI CŨNG ĐỔI", "6963483"),
    bars(1, "BỐN MỨC CHI CHUNG THỬ", [(f"CHI {vn(c)}", c, vn(c), a, c == COST) for c, a in
                                      zip(S, [[1, "mức"], [1, "sáu"], [1, "tám"], [1, "ba"]])], unit="TRIỆU/THÁNG · " + HYP),
    bars(2, f"CHI {vn(SENS[0]['cost'])} · CHIA ĐỀU", [("THẢO CÒN", S[24]["equal_thao"], vn(S[24]["equal_thao"]), [2, "thảo"], True),
                                                   ("NAM CÒN", S[24]["equal_nam"], vn(S[24]["equal_nam"]), 3, False)]),
    stack(4, "CHIA ĐỀU · KHI CHI TĂNG", [(f"CHI {vn(c)}", [S[c]["equal_thao"], S[c]["equal_nam"]], a) for c, a in
                                         zip(S, [4, [4, "số"], 5, 6])],
          [(3, f"THẢO CÒN {vn(S[30]['equal_thao'])}", [6, "không"], "down")], keys=K2),
    bars(8, f"CHI {vn(SENS[0]['cost'])} · TỶ TRỌNG", [("THẢO CÒN", S[24]["pro_thao"], vn(S[24]["pro_thao"]), [8, "sáu"], True),
                                                   ("NAM CÒN", S[24]["pro_nam"], vn(S[24]["pro_nam"]), [8, "nam"], False)]),
    stack(9, "TỶ TRỌNG · KHI CHI TĂNG", [(f"CHI {vn(c)}", [S[c]["pro_thao"], S[c]["pro_nam"]], a) for c, a in
                                         zip(S, [9, [9, "để"], 10, 11])],
          [(3, f"THẢO CÒN {vn(S[30]['pro_thao'])}", [11, "để"])], keys=K2),
    bars(12, "CHI +6: THẢO MẤT BAO NHIÊU", [
        (f"CHIA ĐỀU · {vn(S[24]['equal_thao'])} → {vn(S[30]['equal_thao'])}", S[24]["equal_thao"] - S[30]["equal_thao"],
         f"−{vn(S[24]['equal_thao'] - S[30]['equal_thao'])} · CHẠM 0", 12, True),
        (f"TỶ TRỌNG · {vn(S[24]['pro_thao'])} → {vn(S[30]['pro_thao'])}", S[24]["pro_thao"] - S[30]["pro_thao"],
         f"−{vn(S[24]['pro_thao'] - S[30]['pro_thao'])}", [13, "độ"], False)]),
    photo("ai04", 15, [.42, .32], [("ĐƯỜNG NHẠY CHI", 15, "sm"), ("KHÔNG BẢO AI PHẢI CHỌN", 16, "acc")], move="pan"),
    stack(17, "THÁNG 12 · BA VÍ", [("CÙNG SỐ", B6["eq"], 18), ("CÙNG TỶ LỆ", B6["pro"], 19), ("QUỸ CHUNG", B6["pool"], 20)]),
    wf(21, "MỖI THÁNG · CẢ NHÀ", ("VÀO", R["total_income"], 21), [("RA", -COST, [21, "sáu"])], ("CÒN LẠI", [21, "còn"]),
       [(2, f"VẪN {vn(LEFT)} TRIỆU", 22)]),
    kinetic(23, [("VÒNG MỞ ĐÃ KHÉP", 23, "sm"), ("CÔNG BẰNG KHÔNG NẰM TRONG MỘT CON SỐ", 24, "acc")]),
    ledger(25, "BA BẢNG · BA CÂU HỎI", [("BẢNG 1", "CÙNG SỐ TIỀN?", 25), ("BẢNG 2", "CÙNG TỶ LỆ THU NHẬP?", 26),
                                        ("→", "HAI CÂU KHÁC NHAU", 27)]),
    question(28, "Bao nhiêu phần riêng,\nbao nhiêu phần chung?"),
    timeline(30, "KSMS 2022 · CÁC NHÓM DỮ LIỆU", [("CHI TIÊU", "", 30), ("NHÀ Ở", "", [30, "nhà"]), ("GIÁO DỤC", "", [30, "giáo"]),
                                                   ("Y TẾ", "", [30, "y"]), ("VIỆC LÀM", "", [30, "việc"])], GSO22),
    photo("ai01", 31, [.5, .4], [("GỌI TÊN TỪNG PHẦN", 31, "acc"), ("cái giá và phần còn lại của từng định nghĩa", 32, "sm")],
          zoom={"x": .5, "y": .6, "z": 1.35, "at": 31, "d": 1.2}),
    kinetic(33, [("NHÌN BA CÁI VÍ", 33, "acc"), ("trước khi gọi một con số là công bằng", [33, "trước"], "sm")]),
]}

SAY = {"vhlss": "vi êch en ét ét", "doi": "đôi ai", "issp": "ai ét ét pê", "gladstone": "gờ-lát-xtôn", "garbinsky": "ga-bin-xki", "mogilner": "mô-ghiu-nơ", "vogler": "vốc-lơ", "lyonette": "li-ô-nét", "wiggins": "uých-ghin", "burgoyne": "bơ-goi", "lauer": "lao-ơ", "blekesaune": "blê-kơ-xau-nơ"}
TITLE = "Vợ 15 Triệu, Chồng 25 Triệu: Chia Tiền Nhà Sao Công Bằng?"   # Content Brief bản 2, F4
TITLES = [TITLE, "Chia Đôi Tiền Nhà: Vì Sao Người Lương Thấp Hết Tiền Trước?", "Gộp Hay Tách Tiền Vợ Chồng: Nghiên Cứu Nói Gì?"]
SOURCES = [
 "Tổng cục Thống kê — Thông cáo năm 2024: https://www.nso.gov.vn/du-lieu-va-so-lieu-thong-ke/2025/01/thong-cao-bao-chi-tinh-hinh-kinh-te-xa-hoi-quy-iv-va-nam-2024/",
 "Tổng cục Thống kê — Khảo sát mức sống 2022: https://www.nso.gov.vn/default/2024/04/ket-qua-khao-sat-muc-song-dan-cu-viet-nam-nam-2022/",
 "VBPL — Luật Hôn nhân và gia đình 52/2014/QH13: https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/36870/VanBanGoc_52.2014.QH13.pdf",
 "Gladstone, Garbinsky & Mogilner (2022): https://www.anderson.ucla.edu/sites/default/files/document/2022-05/Pooling_finances_and_relations.pdf",
 "Vogler, Lyonette & Wiggins (2008): https://journals.sagepub.com/doi/10.1111/j.1467-954X.2008.00779.x",
 "Burgoyne et al. (2006): https://journals.sagepub.com/doi/10.1111/j.1467-954X.2006.00663.x",
 "Lauer (2011): https://doi.org/10.1111/j.1741-3737.2011.00836.x",
 "Blekesaune (2018): https://pmc.ncbi.nlm.nih.gov/articles/PMC6469846/",
 "van der Lippe et al. (2014): https://www.demographic-research.org/volumes/vol30/55/30-55.pdf",
]
SPEC = {"title":TITLE,"channel":"CK","accent":GOLD,"master":True,"endcard":20,"endcardSub":"VIDEO TIẾP THEO","beat2":True,"chart_rules":True,
 "acc":["vợ","chồng","tiền","chung","riêng","công","bằng"],"say":SAY,"imgs":{f"ai0{i}":f"EXT:ai:ai_0{i}" for i in range(1,7)},"chapters":[f"ch{i:02d}" for i in range(7)],
 "youtube":{"titles":TITLES,"summary":"Gộp hết lương vào một ví chung, hay mỗi người giữ phần của mình? Một tổng hợp sáu nghiên cứu với gần 39 nghìn người đã đo câu hỏi ấy. Video dùng một ví dụ giả định, vợ 15 triệu, chồng 25 triệu, chi chung 26 triệu, để đặt cạnh nhau ba cách chia: góp bằng số tiền, góp theo tỷ lệ thu nhập và gộp vào quỹ chung, suốt 12 tháng; đồng thời nêu rõ giới hạn của nghiên cứu quốc tế và thông tin văn bản pháp luật.","more":["Nội dung giáo dục, không phải tư vấn đầu tư. Các khoản tiền của Thảo và Nam là VÍ DỤ GIẢ ĐỊNH, chỉ nhằm minh họa phép tính; không phải ngân sách đề xuất cho bất kỳ gia đình nào.","Nghiên cứu quốc tế được nêu như dữ liệu quan sát, không là lời hứa hay công thức áp dụng cho từng cặp đôi. Thông tin luật chỉ có tính khái quát."],"chapter_titles":{"ch00":"Gộp chung hay giữ riêng: nghiên cứu nói gì","ch01":"Ví thứ nhất: cùng góp một số","ch02":"Ví thứ hai: cùng chịu một tỷ lệ","ch03":"Ví thứ ba: một quỹ, hai phần riêng","ch04":"Khi ba bảng gặp chữ chung","ch05":"Nghiên cứu nhìn thấy gì, và không nhìn thấy gì","ch06":"Khi hóa đơn đổi, câu hỏi cũng đổi"},"sources":SOURCES,"hashtags":["TàiChínhCáNhân","ChiTiêuGiaĐình","BiểuĐồBiếtNói"],"tags":["chia tiền vợ chồng","tài chính vợ chồng","cách quản lý tài chính vợ chồng","tài chính gia đình","quỹ chung","tiền riêng","chi tiêu gia đình"],"category":"27","thumb":"t1.jpg","data_credit":"Số liệu nghiên cứu và thông tin công khai được ghi trong phần nguồn; các phép tính minh họa dùng giả định nêu trong video.","video_credits":"Video minh họa: Pexels. Ảnh minh họa nhân vật giả định: AI."}}

SPEC["youtube"].update({"publish_at": "2026-11-22T13:00:00Z", "playlist": "Quyết Định Lớn"})


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
