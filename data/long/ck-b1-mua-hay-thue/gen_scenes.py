"""Sinh spec.json + scenes/hud/bgm cho video dài CK B1 "Hai căn hộ giống hệt nhau, một mua một thuê: 10 năm sau ai khá hơn?"
(chuỗi Quyết định lớn · Bài 1; kênh Biểu Đồ Biết Nói, theme "chart").

    python data/long/ck-b1-mua-hay-thue/gen_scenes.py     # giữ nguyên "lines" + "title" trong chNN.json (script_lines ghi)

Dữ kiện + nguồn: docs/channels/chung-khoan/2026-10-07-long-b1-research.md; kiểm chứng: factcheck.md (cùng thư mục) — lượt 1
(mục 1c) + lượt 2 (mục 9, thắng khi trùng): bars giá CH01 giữ CBRE 60 với nhãn đúng cách đo, giá rao 84; "PHỔ BIẾN ≈ 10,9%";
ưu đãi 2026 8,5–11 → cột 9,75; "KHI BÁN" có dòng miễn thuế nhà ở duy nhất; CPI thuê nhà "so cùng kỳ"; "khu nội thành cũ";
bỏ "LẦN ĐẦU"; counter 70% "THÁNG 25"; slam ≈ 7,5% kèm dòng giả định; slam "PHẦN CHÊNH PHẢI ĐƯỢC ĐỂ DÀNH THẬT"; kết chung.
Ví dụ giả định TÍNH LẠI NGAY TRONG FILE NÀY (mô hình tháng của factcheck mục 4, b1_model.py) — mọi số trên màn hình của ví dụ
lấy từ đây và có assert khớp lời đọc. Mô-típ HAI CÁNH CỬA: trái = MUA (cam), phải = THUÊ (tím); hành lang Pexels ở CH00,
CH05, CH07. Luật kênh: chỉ giáo dục, không khuyến nghị, không dự báo; không tên ngân hàng / chủ đầu tư / dự án (tên đơn vị
NGUỒN chỉ ở dòng nguồn). Mọi b-roll "VIDEO MINH HỌA"; mọi cảnh của ví dụ "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH".
Neo: chữ ĐẦU TIÊN của mỗi cảnh neo vào từ ĐẦU câu; slam đặt cảnh ngay ở chữ đập; counter đếm từ đầu cảnh.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

UP, DN, GOLD, BLUE = "#4ade80", "#f87171", "#fbbf24", "#38bdf8"
BUY, RENT = "#fb923c", "#a78bfa"            # cánh cửa TRÁI (mua) cam · cánh cửa PHẢI (thuê) tím
ILL = "VIDEO MINH HỌA"
HYPO = "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH"
# Bảng đọc: GIỐNG HỆT C1 (đổi bảng = đổi khoá cache TTS; "vn-index" -> "Vi En In-đéc").
SAY = {"vn-index": "Vi En In-đéc", "hose": "hô-dê", "vic": "vi ai xi", "vhm": "vi hát em", "vre": "vi rờ e", "vpl": "vi pê en",
       "ree": "rê ê ê", "sam": "xam", "gdp": "gi đi pi", "etf": "i ti ép", "hnx": "hát en ích", "upcom": "úp-com",
       "margin": "ma-gin", "app": "áp", "vingroup": "Vin-grúp", "vietnambiz": "Việt Nam Biz", "sjc": "ét giây xi"}

# ---------------- mô hình ví dụ (triệu đồng, theo tháng) — factcheck mục 4 ----------------
V0, DOWN, LOAN, N = 2500.0, 1000.0, 1500.0, 300
R1, R2, PROMO = 0.11, 0.14, 24
BUY_COST, REPAIR, SELL_TAX, YLD, RENT_G, DEP = 0.01, 0.005, 0.02, 0.03, 0.05, 0.068


def schedule(r1=R1, r2=R2):
    """[(khoản trả, lãi, dư nợ sau kỳ)] — gốc chia đều, lãi trên dư nợ."""
    out, bal = [], LOAN
    for m in range(1, N + 1):
        intr = bal * (r1 if m <= PROMO else r2) / 12
        bal -= LOAN / N
        out.append((LOAN / N + intr, intr, bal))
    return out


SCH = schedule()


def rent(m):                       # tiền thuê tháng m (1..), +5% mỗi 12 tháng
    return V0 * YLD / 12 * (1 + RENT_G) ** ((m - 1) // 12)


def paths(g, years=10, dep=DEP, spend_gap=False):
    """Số dư hai nhà theo tháng 0..12·years: (người thuê W, người mua nếu bán = giá × 98% − dư nợ)."""
    W, w_path, b_path = DOWN + BUY_COST * V0, [], []
    w_path.append(W)
    b_path.append(V0 * (1 - SELL_TAX) - LOAN)
    for m in range(1, 12 * years + 1):
        pay, _, bal = SCH[m - 1]
        cost = pay + V0 * (1 + g) ** ((m - 1) / 12) * REPAIR / 12
        W = W * (1 + dep / 12) + (0 if spend_gap else cost - rent(m))
        w_path.append(W)
        b_path.append(V0 * (1 + g) ** (m / 12) * (1 - SELL_TAX) - bal)
    return w_path, b_path


def breakeven(**kw):
    lo, hi = -0.05, 0.30
    for _ in range(80):
        mid = (lo + hi) / 2
        w, b = paths(mid, **kw)
        lo, hi = (mid, hi) if b[-1] < w[-1] else (lo, mid)
    return mid


PAY = {m: SCH[m - 1][0] for m in (1, 12, 24, 25, 36, 60, 120)}
W10, B0 = paths(0.0)
_, B3 = paths(0.03)
_, B5 = paths(0.05)
G_STAR = breakeven()
GAP1 = SCH[0][0] + V0 * REPAIR / 12 - rent(1)
GAP25 = SCH[24][0] + V0 * REPAIR / 12 - rent(25)
GAP120 = SCH[119][0] + V0 * REPAIR / 12 - rent(120)
SPENT = paths(0.0, spend_gap=True)[0][-1]
INT24 = sum(x[1] for x in SCH[:24])
RENT24 = sum(rent(m) for m in range(1, 25))
# khớp lời đọc / factcheck (sai khác ≤ 0,01)
assert [round(PAY[m], 2) for m in (1, 24, 25)] == [18.75, 17.70, 21.10]
assert round(PAY[25] - PAY[24], 2) == 3.40 and round(100 * (PAY[25] / PAY[24] - 1)) == 19
assert round(W10[-1]) == 4054 and [round(x[-1]) for x in (B0, B3, B5)] == [1550, 2393, 3091]
assert round(100 * G_STAR, 2) == 7.45 and round(SPENT) == 2019
assert (round(GAP1, 2), round(GAP25, 2), round(GAP120, 1)) == (13.54, 15.25, 6.9)
assert round(INT24) == 317 and round(RENT24, 2) == 153.75
BASE = W10[0]                                   # 1.025 tr: cả hai nhà bắt đầu với cùng số tiền (trả trước + phí mua)
pct = lambda xs: [round(100 * (x / BASE - 1), 2) for x in xs]
# trục ngang của race tự tính: nhãn "T1, T25, T49, T73, T97" (engine in "T" + 2 số ở vị trí 5–6 khi nhóm đổi)
RACE_DATES = [f"thang{1 + 24 * ((max(i, 1) - 1) // 24):02d}" for i in range(121)]
vn = lambda x, nd=2: f"{x:.{nd}f}".replace(".", ",")

# Sổ 12 tháng 4 NH lớn cuộn mỗi tháng 10 (A1 §7.1 + factcheck A1) — cùng ROLL với A1
ROLL = [["2018-10-01", .066], ["2019-10-01", .068], ["2020-10-01", .060], ["2021-10-01", .055], ["2022-10-01", .064],
        ["2023-10-01", .053], ["2024-10-01", .046], ["2025-10-01", .047]]
SRC_RACE = ("DỮ LIỆU: HOSE, SJC (QUA VNSTOCK) · TIẾT KIỆM: MỨC 12 THÁNG NH LỚN TỪNG NĂM, CUỘN MỖI THÁNG 10 (ƯỚC TÍNH) · "
            "VN-INDEX CHƯA GỒM CỔ TỨC · KÊNH TỰ TÍNH · NHÌN LẠI, KHÔNG PHẢI DỰ BÁO")
SRC_LOAN = "DKRA qua Dân trí 03/09/2026 (11 NH, cố định 12–24 tháng) · VARS-IRE qua VnExpress 04/08/2026"
SRC_YIELD = "REFI qua CafeBiz 29/08/2026 (một nguồn) · tỷ suất gộp = tiền thuê năm ÷ giá"
SRC_SAV = "Savills qua Người Quan Sát 16/01/2026 · giá căn hộ, chưa trừ lãi vay, chưa gồm tiền thuê"

CH = {}

# ---------------- CH00 · Hai cánh cửa cạnh nhau (cold open → nghịch lý → nhận diện kênh) ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI CÁNH CỬA CẠNH NHAU"}, "bgm": {"mood": "calm", "gain": 0.057}, "scenes": [
    {"type": "broll", "vid": "1509536", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "HAI CĂN HỘ GIỐNG HỆT NHAU", "at": [0, "Giả"]},
             {"text": "CỬA SÁT CỬA", "at": [0, "cửa"], "acc": True}],
     "label": {"k": "VIDEO GIÁO DỤC", "v": "KHÔNG PHẢI LỜI KHUYÊN MUA HAY THUÊ NHÀ", "s": "KHÔNG DỰ BÁO GIÁ NHÀ · " + HYPO,
               "at": [0, "Giả", 0, 0.3]}},
    {"type": "broll", "at": 1, "vid": "31751335", "veil": 0.55, "illus": ILL, "tag": {"text": "VÍ DỤ GIẢ ĐỊNH", "at": [1, "Cùng"]},
     "kin": [{"text": "CÙNG 2 PHÒNG NGỦ · CÙNG HƯỚNG · CÙNG THANG MÁY", "at": [1, "Cùng"], "sm": True},
             {"text": "≈ 2,5 TỶ MỖI CĂN", "at": [1, "hai", 1], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "MỖI THÁNG", "illus": HYPO, "rows": [
        {"k": "TRÁI · MUA → NGÂN HÀNG", "v": f"≈ {vn(PAY[1])} TR", "at": [2, "chuyển"]},
        {"k": "PHẢI · THUÊ → CHỦ NHÀ", "v": f"≈ {vn(rent(1))} TR", "at": [3, "trả"]}],
     "total": {"k": "THU NHẬP · CẢ HAI NHÀ", "v": "≈ 30 TR", "at": [4, "cùng"]}},
    {"type": "question", "at": 5, "text": "Mười năm sau,\nnhà nào khá hơn?"},
    {"type": "kinetic", "at": 6, "items": [{"text": "CÂU TRẢ LỜI QUEN TAI", "at": [6, "Câu"], "sm": True},
                                          {"text": "MUA CHỨ · TIỀN THUÊ LÀ TIỀN MẤT", "at": [6, "mua"]},
                                          {"text": "nhìn kỹ hai con số ấy…", "at": [7, "Nhưng"], "sm": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "TIỀN THUÊ CẢ NĂM ≈ 3% GIÁ NHÀ", "at": [8, "Tiền"]},
                                          {"text": "LÃI VAY SAU ƯU ĐÃI ≈ 13–15%/NĂM", "at": [9, "lãi"], "acc": True}],
     "srcnote": "Tỷ suất: REFI qua CafeBiz 29/08/2026 (cả nước 3,05%) · lãi: VARS-IRE qua VnExpress 04/08/2026"},
    {"type": "counter", "at": 10, "from": 0, "to": 26, "suffix": "%/NĂM", "until": [10, "đậm"],
     "label": "GIÁ CĂN HỘ HÀ NỘI · 5 NĂM QUA", "sub": {"text": "SAVILLS · 2019 → 2025", "at": [10, "thắng"]}, "srcnote": SRC_SAV},
    {"type": "kinetic", "at": 11, "items": [{"text": "BÊN PHẢI TRẢ ÍT HƠN HẲN", "at": [11, "Một"]},
                                           {"text": "BÊN TRÁI GIÀU LÊN NHANH HƠN", "at": [11, "bên", 1], "acc": True}]},
    {"type": "slam", "at": [12, "nghịch"], "text": "NGHỊCH LÝ", "sub": "TRẢ ÍT HƠN · NHƯNG GIÀU CHẬM HƠN?"},
    {"type": "broll", "at": 13, "vid": "10577994", "veil": 0.6, "illus": ILL,
     "kin": [{"text": "ĐIỀU GÌ PHẢI ĐÚNG", "at": [13, "Mình"], "sm": True},
             {"text": "ĐỂ CÁNH CỬA TRÁI THẮNG?", "at": [13, "trái"]},
             {"text": "ĐỂ CÁNH CỬA PHẢI THẮNG?", "at": [13, "phải", 2], "acc": True}]},
    {"type": "brand", "at": 14, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 15, "items": [{"text": "QUYẾT ĐỊNH LỚN · BÀI 1", "at": [15, "Và"], "acc": True},
                                           {"text": "chỉ nhằm giáo dục · không phải lời khuyên mua hay thuê", "at": [16, "Video"], "sm": True},
                                           {"text": "không dự báo giá nhà", "at": [16, "không", 1], "sm": True}]},
]}

# ---------------- CH01 · Con số ba phần trăm ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CON SỐ BA PHẦN TRĂM"}, "bgm": {"mood": "curious", "gain": 0.092}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CON SỐ\nBA PHẦN TRĂM", "sub": "GIÁ NHÀ · GIÁ THUÊ · TỶ SUẤT",
     "vid": "36287412", "illus": ILL, "titleAt": [0, "Bắt"]},
    {"type": "bars", "at": 1, "title": "GIÁ CĂN HỘ HÀ NỘI · GIỮA NĂM 2026", "unit": "TRIỆU Đ/M² · MỖI CỘT MỘT CÁCH ĐO", "items": [
        {"k": "THỨ CẤP · CBRE", "v": 60, "lbl": "≈ 60", "at": [2, "sáu"]},
        {"k": "SƠ CẤP · CBRE", "v": 95, "lbl": "≈ 95", "at": [3, "mới"]},
        {"k": "GIÁ RAO · QUÝ III", "v": 84, "lbl": "≈ 84", "at": [3, "rao"]},
        {"k": "THỨ CẤP · BỘ XD", "v": 123, "lbl": "≈ 123", "at": [2, "trăm"], "acc": True}],
     "srcnote": "CBRE (TC KTTC 07/07/2026): thứ cấp TB, m² thông thủy, chưa VAT · sơ cấp chưa VAT, trước chiết khấu · "
                "Batdongsan.com.vn: giá rao · Bộ XD qua VnExpress 02/09/2026 · KHÔNG SO TRỰC TIẾP"},
    {"type": "kinetic", "at": 4, "items": [{"text": "QUÝ II/2026 · HÀ NỘI", "at": [4, "Có"], "sm": True},
                                          {"text": "KHÔNG CÓ CĂN MỚI MỞ BÁN", "at": [4, "không"]},
                                          {"text": "DƯỚI 60 TR/M²", "at": [4, "dưới"], "acc": True},
                                          {"text": "CBRE: quý thứ 2 liên tiếp (chưa VAT) · Savills: mọi hàng sơ cấp trên 70 tr/m²",
                                           "at": [4, "dưới", 0, 0.6], "sm": True}],
     "srcnote": "CBRE qua TC Kinh tế Tài chính, VietnamFinance 07/07/2026 · Savills qua CafeF 14/08/2026"},
    {"type": "ledger", "at": 5, "title": "CĂN VÍ DỤ", "illus": HYPO, "rows": [
        {"k": "DIỆN TÍCH", "v": "≈ 50 M²", "at": [6, "Khoảng"]},
        {"k": "ĐƠN GIÁ", "v": "≈ 50 TR/M²", "at": [6, "vuông"]},
        {"k": "GIÁ CĂN", "v": "≈ 2,5 TỶ", "at": [6, "hai"]}],
     "total": {"k": "RẺ HƠN MỌI MỨC Ở TRÊN", "v": "NHỎ · XA · CŨ", "at": [6, "nhỏ"]}},
    {"type": "kinetic", "at": 7, "items": [{"text": "GIỜ TỚI GIÁ THUÊ", "at": [7, "Giờ"], "sm": True},
                                          {"text": "TỶ SUẤT CHO THUÊ", "at": [8, "tỷ"], "acc": True},
                                          {"text": "= TIỀN THUÊ 1 NĂM ÷ GIÁ NHÀ", "at": [9, "Nó"]},
                                          {"text": "tỷ suất gộp · chưa trừ chi phí", "at": [9, "chia"], "sm": True}]},
    {"type": "bars", "at": 10, "title": "TỶ SUẤT CHO THUÊ CĂN HỘ", "unit": "% / NĂM", "items": [
        {"k": "HÀ NỘI · 2023", "v": 4.5, "lbl": "≈ 4–5", "at": [12, "bốn"]},
        {"k": "HÀ NỘI · Q2/2026", "v": 2.32, "lbl": "2,32", "at": [10, "hai"], "acc": True},
        {"k": "TP.HCM · Q2/2026", "v": 3.30, "lbl": "3,30", "at": [11, "ba"]},
        {"k": "ĐÀ NẴNG · Q2/2026", "v": 4.34, "lbl": "4,34", "at": [11, "phần"]},
        {"k": "CẢ NƯỚC · Q2/2026", "v": 3.05, "lbl": "3,05", "at": [11, "trăm"]}],
     "srcnote": "REFI qua CafeBiz 29/08/2026 (một nguồn) · HN 2023: REFI ≈ 4,2%, Batdongsan.com.vn 4,9–5% (Báo Xây dựng 15/04/2026)"},
    {"type": "question", "at": 13, "text": "Sao lại giảm nhanh vậy?"},
    {"type": "kinetic", "at": 14, "items": [{"text": "GIÁ BÁN CHẠY NHANH", "at": [14, "Vì"]},
                                           {"text": "GIÁ THUÊ PHẢI VỪA TÚI NGƯỜI THUÊ", "at": [15, "tiền"], "acc": True},
                                           {"text": "lương không chạy kịp", "at": [15, "lương"], "sm": True}]},
    {"type": "counter", "at": 16, "from": 0, "to": 33, "suffix": " NĂM", "until": [17, "năm"],
     "label": "GIÁ NHÀ = 33 NĂM TIỀN THUÊ", "sub": {"text": "TỶ SUẤT 3% · HÀ NỘI 2,32% → ≈ 43 NĂM", "at": [18, "Với"]},
     "srcnote": "Kênh tự tính: 1 ÷ 3% ≈ 33,3 · 1 ÷ 2,32% ≈ 43,1"},
    {"type": "ledger", "at": 19, "title": "TIỀN THUÊ · CÁNH CỬA PHẢI", "illus": HYPO, "rows": [
        {"k": "GIÁ CĂN", "v": "2,5 TỶ", "at": [19, "căn"]},
        {"k": "TỶ SUẤT", "v": "3% / NĂM", "at": [19, "ba"]}],
     "total": {"k": "PHẢI · THUÊ", "v": f"≈ {vn(rent(1))} TR/THÁNG", "at": [19, "sáu"]}},
    {"type": "question", "at": 21, "text": "Thế thì người cho thuê\nlấy gì mà lãi?"},
    {"type": "kinetic", "at": 22, "items": [{"text": "CHẤP NHẬN TIỀN THUÊ THẤP", "at": [22, "Nhiều"]},
                                           {"text": "KỲ VỌNG GIÁ NHÀ TĂNG", "at": [22, "kỳ"], "acc": True}],
     "srcnote": "Diễn giải từ REFI (CafeBiz 29/08/2026) và Batdongsan.com.vn (Báo Xây dựng 15/04/2026)"},
    {"type": "slam", "at": [23, "cánh"], "text": "CHỜ GIÁ NHÀ TĂNG", "sub": "CẢ HAI CÁNH CỬA", "fx": "zoom"},
]}

# ---------------- CH02 · Khoản vay, và cú nhảy năm thứ ba ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "KHOẢN VAY, VÀ CÚ NHẢY NĂM THỨ BA"}, "bgm": {"mood": "mystery", "gain": 0.145}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "KHOẢN VAY,\nVÀ CÚ NHẢY NĂM THỨ BA", "sub": "CÁNH CỬA BÊN TRÁI · MUA",
     "vid": "8293504", "illus": ILL, "titleAt": [0, "Giờ"]},
    {"type": "ledger", "at": 1, "title": "CÁNH CỬA TRÁI · MUA", "illus": HYPO, "rows": [
        {"k": "GIÁ CĂN", "v": "2,5 TỶ", "at": [1, "Căn"]},
        {"k": "TRẢ TRƯỚC", "v": "1 TỶ (40%)", "at": [1, "trả"]}],
     "total": {"k": "VAY · 25 NĂM", "v": "1,5 TỶ", "at": [2, "vay"]}},
    {"type": "ledger", "at": 3, "title": "LÃI VAY MUA NHÀ · 09/2026", "rows": [
        {"k": "CỐ ĐỊNH", "v": "1–2 NĂM ĐẦU", "at": [3, "cố"]},
        {"k": "PHỔ BIẾN (11 NH)", "v": "≈ 10,9%", "at": [4, "phổ"]}],
     "srcnote": SRC_LOAN},
    {"type": "ledger", "at": 5, "title": "SAU ƯU ĐÃI: THẢ NỔI", "rows": [
        {"k": "LÃI CƠ SỞ", "v": "NGÂN HÀNG CÔNG BỐ", "at": [6, "lãi"]},
        {"k": "+ BIÊN ĐỘ (HỢP ĐỒNG)", "v": "3,3–3,5 ĐIỂM", "at": [7, "Biên"]}],
     "total": {"k": "THỰC TRẢ · QUÝ II/2026", "v": "≈ 13–15%", "at": [8, "mười"]},
     "srcnote": "VARS-IRE qua VnExpress 04/08/2026 · khảo sát 10 ngân hàng"},
    {"type": "kinetic", "at": 9, "items": [{"text": "MỘT KIỂU TRẢ HAY GẶP", "at": [9, "Thử"], "sm": True},
                                          {"text": "GỐC CHIA ĐỀU MỖI THÁNG", "at": [9, "gốc"]},
                                          {"text": "LÃI TÍNH TRÊN NỢ CÒN LẠI", "at": [9, "lãi"]},
                                          {"text": "1,5 TỶ ÷ 300 THÁNG = 5 TR GỐC", "at": [10, "Một"], "acc": True}],
     "illus": HYPO},
    {"type": "counter", "at": 11, "from": 0, "to": round(PAY[1] * 1e6), "suffix": " Đ", "until": [12, "mười"],
     "label": "THÁNG 1 · LÃI 11%", "sub": {"text": "= 5 TR GỐC + 13,75 TR LÃI · ≈ 62% THU NHẬP 30 TR", "at": [12, "sáu"]},
     "illus": HYPO},
    {"type": "bars", "at": 13, "title": "KHOẢN TRẢ MỖI THÁNG · BÊN TRÁI", "unit": "TRIỆU Đ", "items": [
        {"k": "THÁNG 1", "v": PAY[1], "lbl": vn(PAY[1]), "at": [13, "Mỗi"]},
        {"k": "THÁNG 12", "v": PAY[12], "lbl": vn(PAY[12]), "at": [13, "nợ"]},
        {"k": "THÁNG 24", "v": PAY[24], "lbl": vn(PAY[24]), "at": [14, "hai"]},
        {"k": "THÁNG 25", "v": PAY[25], "lbl": vn(PAY[25]), "at": [16, "nhảy"], "acc": True},
        {"k": "THÁNG 36", "v": PAY[36], "lbl": vn(PAY[36]), "at": [16, "triệu"]},
        {"k": "THÁNG 60", "v": PAY[60], "lbl": vn(PAY[60]), "at": [16, "trăm"]},
        {"k": "THÁNG 120", "v": PAY[120], "lbl": vn(PAY[120]), "at": [16, "nghìn"]}],
     "illus": HYPO, "srcnote": "Vay 1,5 tỷ, 25 năm, gốc đều · 11% tháng 1–24, giả sử 14% từ tháng 25 · kênh tự tính"},
    {"type": "slam", "at": [17, "thêm"], "text": "+3,4 TRIỆU / THÁNG", "sub": f"17,70 → 21,10 TR · ≈ +19% · CHỈ SAU MỘT KỲ",
     "illus": HYPO},
    {"type": "counter", "at": 18, "from": 0, "to": 70, "suffix": "%", "label": "THU NHẬP ĐI VÀO NGÂN HÀNG · THÁNG 25",
     "sub": {"text": "21,10 TR ÷ 30 TR ≈ 70,3%", "at": [18, "thu"]}, "illus": HYPO},
    {"type": "question", "at": 19, "text": "Đã ký hợp đồng rồi,\nsao lãi vẫn nhảy được?"},
    {"type": "kinetic", "at": 20, "items": [{"text": "THẢ NỔI = LÃI CƠ SỞ + BIÊN ĐỘ", "at": [20, "Vì"]},
                                           {"text": "lãi cơ sở: ngân hàng điều chỉnh theo kỳ", "at": [20, "mà"], "sm": True},
                                           {"text": "biên độ: cố định theo hợp đồng", "at": [20, "mà", 0, 0.5], "sm": True},
                                           {"text": "CÓ THỂ LÊN · CŨNG CÓ THỂ XUỐNG", "at": [21, "Nó"], "acc": True}]},
    {"type": "bars", "at": 22, "title": "LÃI ƯU ĐÃI MUA NHÀ", "unit": "%/NĂM · CỘT = GIỮA DẢI", "items": [
        {"k": "NĂM 2025", "v": 6.1, "lbl": "5,5–6,7", "at": [22, "Năm"]},
        {"k": "NĂM 2026", "v": 9.75, "lbl": "8,5–11", "at": [23, "Năm"], "acc": True}],
     "srcnote": "VARS-IRE qua VnExpress 04/08/2026 (quý II/2026)"},
    {"type": "ledger", "at": 24, "title": "24 THÁNG ĐẦU", "illus": HYPO, "rows": [
        {"k": "TRÁI · TIỀN LÃI", "v": f"≈ {INT24:.0f} TR", "at": [24, "ba"]},
        {"k": "PHẢI · TIỀN THUÊ", "v": f"≈ {RENT24:.0f} TR", "at": [25, "một"]}],
     "srcnote": f"Kênh tự tính: tổng lãi 24 tháng = {vn(INT24)} tr · thuê 6,25 × 12 + 6,5625 × 12 = {vn(RENT24)} tr"},
    {"type": "kinetic", "at": 26, "items": [{"text": "NHƯNG KHOAN KẾT LUẬN", "at": [26, "Nhưng"]},
                                           {"text": "TIỀN LÃI CHƯA PHẢI TOÀN BỘ CÂU CHUYỆN", "at": [26, "tiền"], "acc": True}]},
]}

# ---------------- CH03 · Những khoản không nằm trong giá ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "NHỮNG KHOẢN KHÔNG NẰM TRONG GIÁ"}, "bgm": {"mood": "warm", "gain": 0.14}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "NHỮNG KHOẢN\nKHÔNG NẰM TRONG GIÁ", "sub": "PHÍ · THUẾ · SỬA CHỮA · TIỀN THUÊ TĂNG",
     "vid": "8293019", "illus": ILL, "titleAt": [0, "Mua"]},
    {"type": "ledger", "at": 1, "title": "KHI MUA", "rows": [
        {"k": "LỆ PHÍ TRƯỚC BẠ", "v": "0,5%", "at": [1, "Lệ"]},
        {"k": "CÔNG CHỨNG · THẨM ĐỊNH · THẾ CHẤP", "v": "+", "at": [2, "Thêm"]},
        {"k": "MUA CỦA CHỦ ĐẦU TƯ: BẢO TRÌ", "v": "+ 2%", "at": [4, "hai"]}],
     "total": {"k": "VÍ DỤ GỘP · LÀM TRÒN", "v": "≈ 1% = 25 TR", "at": [3, "một"]},
     "srcnote": "NĐ 10/2022/NĐ-CP (0,5%) · Luật Nhà ở 2023, Đ152 k1 (bảo trì 2%, tính riêng với tiền bán) · bảo trì 2%: CHƯA GỒM TRONG VÍ DỤ"},
    {"type": "ledger", "at": 5, "title": "KHI BÁN", "rows": [
        {"k": "THUẾ TNCN", "v": "2% GIÁ BÁN", "at": [5, "thuế"]},
        {"k": "AI NỘP", "v": "THƯỜNG LÀ BÊN BÁN", "at": [5, "người"]},
        {"k": "NHÀ Ở DUY NHẤT", "v": "CÓ THỂ ĐƯỢC MIỄN", "at": [6, "căn"]}],
     "total": {"k": "VÍ DỤ CỦA KÊNH", "v": "VẪN TÍNH 2%", "at": [6, "ví"]},
     "srcnote": "Luật Thuế TNCN 109/2025/QH15, Đ14 k1 (2%), Đ4 k2 (miễn: nhà ở duy nhất, có điều kiện) · hiệu lực 01/07/2026"},
    {"type": "kinetic", "at": 7, "items": [{"text": "Ở TRONG NHÀ CŨNG TỐN TIỀN", "at": [7, "Ở"]},
                                          {"text": "phí quản lý chung cư Hà Nội · có thang máy", "at": [8, "Phí"], "sm": True},
                                          {"text": "1.200–16.500 Đ/M²/THÁNG", "at": [9, "Khung"], "acc": True},
                                          {"text": "ai ở thì trả → để ra ngoài phép so", "at": [10, "Khoản"], "sm": True}],
     "srcnote": "QĐ 25/2026/QĐ-UBND Hà Nội (hiệu lực 23/02/2026), qua VnEconomy"},
    {"type": "broll", "at": 11, "vid": "9890448", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "SỬA CHỮA: CHỦ NHÀ TỰ LO", "at": [11, "Tiền"]},
             {"text": "≈ 0,5% GIÁ TRỊ / NĂM", "at": [12, "nửa"], "acc": True},
             {"text": "giả định của kênh", "at": [12, "giả"], "sm": True}]},
    {"type": "question", "at": 13, "text": "Còn người thuê thì sao?\nĐâu phải không mất gì."},
    {"type": "ledger", "at": 14, "title": "GIÁ CỦA NGƯỜI THUÊ", "rows": [
        {"k": "01 · TIỀN THUÊ TĂNG", "v": "+4,91%", "at": [15, "Thứ"]},
        {"k": "02 · HẾT HỢP ĐỒNG", "v": "CÓ THỂ PHẢI CHUYỂN", "at": [17, "Thứ"]}],
     "srcnote": "CPI nhóm nhà ở thuê 9 tháng 2026: +4,91% so cùng kỳ (bình quân) — NSO 30/09/2026"},
    {"type": "broll", "at": 18, "vid": "4569393", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "03 · MỖI LẦN CHUYỂN NHÀ", "at": [18, "Thứ"]},
             {"text": "TIỀN · SỨC · ĐƯỜNG ĐI LÀM", "at": [18, "tốn"], "acc": True}]},
    {"type": "bars", "at": 19, "title": "TIỀN THUÊ CĂN VÍ DỤ · +5%/NĂM", "unit": "TRIỆU Đ / THÁNG", "items": [
        {"k": "NĂM 1", "v": rent(1), "lbl": vn(rent(1)), "at": [19, "Ví"]},
        {"k": "NĂM 4", "v": rent(37), "lbl": vn(rent(37)), "at": [19, "tăng"]},
        {"k": "NĂM 7", "v": rent(73), "lbl": vn(rent(73)), "at": [19, "mỗi"]},
        {"k": "NĂM 10", "v": rent(109), "lbl": vn(rent(109)), "at": [20, "chín"], "acc": True}],
     "illus": HYPO, "srcnote": "6,25 × 1,05^(năm − 1) · kênh tự tính"},
    {"type": "slam", "at": 21, "text": "BÊN NÀO ĐƯỢC BÙ LẠI?", "sub": "HAI BÊN ĐỀU CÓ CHI PHÍ", "fx": "zoom"},
]}

# ---------------- CH04 · Một tỷ trả trước cũng có giá ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "MỘT TỶ TRẢ TRƯỚC CŨNG CÓ GIÁ"}, "bgm": {"mood": "curious", "gain": 0.17}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "MỘT TỶ TRẢ TRƯỚC\nCŨNG CÓ GIÁ", "sub": "CHI PHÍ CƠ HỘI",
     "vid": "6963972", "illus": ILL, "titleAt": [0, "Có"]},
    {"type": "ledger", "at": 1, "title": "1 TỶ GỬI 12 THÁNG", "rows": [
        {"k": "LÃI · 4 NH LỚN · 09/2026", "v": "6,8% / NĂM", "at": [2, "sáu"]},
        {"k": "MỖI NĂM", "v": "≈ 68 TR", "at": [3, "sáu"]},
        {"k": "THUẾ TNCN TRÊN LÃI", "v": "MIỄN", "at": [3, "không"]}],
     "total": {"k": "MỖI THÁNG", "v": "≈ 5,67 TR", "at": [4, "năm"]},
     "srcnote": "Lãi 12 tháng 4 NH lớn 09/2026 (VietNamNet 09/09/2026) · miễn thuế: Luật 109/2025/QH15, Đ4 k6"},
    {"type": "ledger", "at": 5, "title": "ĐẶT CẠNH NHAU", "illus": HYPO, "rows": [
        {"k": "LÃI CỦA 1 TỶ", "v": "≈ 5,67 TR", "at": [5, "Đặt"]},
        {"k": "PHẢI · TIỀN THUÊ", "v": f"≈ {vn(rent(1))} TR", "at": [5, "sáu"]}]},
    {"type": "slam", "at": 6, "text": "GẦN BẰNG NHAU", "sub": "LÃI CỦA KHOẢN TRẢ TRƯỚC ≈ 91% TIỀN THUÊ", "illus": HYPO},
    {"type": "kinetic", "at": 8, "items": [{"text": "NGHỊCH LÝ BẮT ĐẦU GỠ", "at": [8, "Nghịch"], "sm": True},
                                          {"text": "TỶ SUẤT THUÊ ≈ 3% < LÃI GỬI ≈ 6,8%", "at": [8, "tỷ"]},
                                          {"text": "→ ĐI THUÊ RẺ HƠN", "at": [8, "thuê", 1], "acc": True},
                                          {"text": "nếu chỉ tính tiền ra tiền vào", "at": [8, "nếu"], "sm": True}]},
    {"type": "question", "at": 9, "text": "Nhưng mấy năm qua,\nai mua nhà cũng giàu lên cơ mà?"},
    {"type": "kinetic", "at": 10, "items": [{"text": "ĐÚNG · DỮ LIỆU CŨNG CHO THẤY VẬY", "at": [10, "Đúng"]},
                                           {"text": "NHÌN LẠI 8 NĂM: 10/2018 → 09/2026", "at": [11, "tám"], "acc": True}]},
    {"type": "race", "at": 12, "from": "2018-10-08", "to": "2026-09-30", "money": 1000, "unit": "TR", "title": "1 TỶ SAU 8 NĂM",
     "range": "08/10/2018 → 30/09/2026", "drawAt": [12, "Một"], "until": [14, "chín"],
     "series": [{"key": "deposit", "rates": ROLL, "label": "TIẾT KIỆM 12 THÁNG", "color": UP},
                {"key": "vnindex", "label": "VN-INDEX, CHƯA CỔ TỨC", "color": BLUE},
                {"key": "sjc", "interp": True, "label": "VÀNG MIẾNG SJC", "color": GOLD}],
     "source": SRC_RACE},
    {"type": "counter", "at": 15, "from": 0, "to": 3, "suffix": " LẦN", "label": "GIÁ CĂN HỘ HÀ NỘI SO VỚI 2019",
     "sub": {"text": "SAVILLS · 2019 → 2025 · KHÁC KỲ, KHÁC CÁCH ĐO", "at": [15, "cuối"]}, "srcnote": SRC_SAV},
    {"type": "kinetic", "at": 16, "items": [{"text": "ĐÒN BẨY", "at": [16, "Người"], "sm": True},
                                           {"text": "BỎ 40% TIỀN · HƯỞNG 100% PHẦN TĂNG GIÁ", "at": [16, "đòn"]},
                                           {"text": "VÀ 100% PHẦN GIẢM GIÁ", "at": [16, "căn", 1], "acc": True}]},
    {"type": "race", "at": 17, "from": "2025-12-31", "to": "2026-09-30", "money": 1000, "unit": "TR", "title": "9 THÁNG 2026",
     "range": "31/12/2025 → 30/09/2026", "drawAt": [17, "Nhưng"], "until": [20, "tám"],
     "series": [{"key": "deposit", "rate": 0.052, "label": "TIẾT KIỆM 5,2%", "color": UP},
                {"key": "vnindex", "label": "VN-INDEX", "color": BLUE},
                {"key": "sjc", "label": "VÀNG MIẾNG SJC", "color": GOLD}],
     "source": "DỮ LIỆU: HOSE, SJC (QUA VNSTOCK) · TIẾT KIỆM: MỨC 12 THÁNG NH LỚN THÁNG 1/2026 (VNECONOMY), LÃI DỒN TÍCH · "
               "KÊNH TỰ TÍNH · KHÔNG PHẢI DỰ BÁO"},
    {"type": "kinetic", "at": 21, "items": [{"text": "CĂN HỘ CŨ HÀ NỘI · QUÝ II/2026", "at": [21, "Giá"], "sm": True},
                                           {"text": "−3% SO VỚI QUÝ I", "at": [21, "giảm"], "acc": True}],
     "srcnote": "CBRE qua TC Kinh tế Tài chính 07/07/2026 (giá thứ cấp)"},
    {"type": "slam", "at": 22, "text": "KHÔNG KÊNH NÀO THẮNG MÃI", "sub": "QUÁ KHỨ KHÔNG HỨA GÌ CHO 10 NĂM TỚI", "fx": "zoom"},
    {"type": "kinetic", "at": 23, "items": [{"text": "GIÁ THUÊ RẺ · NGƯỜI MUA VẪN THẮNG", "at": [23, "Giờ"], "sm": True},
                                           {"text": "VÌ GIÁ NHÀ TĂNG ĐỦ NHANH", "at": [23, "giá", 1], "acc": True}]},
    {"type": "question", "at": 24, "text": "Vậy phải nhanh\ntới mức nào mới đủ?"},
]}

# ---------------- CH05 · Mười năm sau hai cánh cửa (cảnh mạnh ~75%) ----------------
RACE10 = {"type": "race", "at": 7, "title": "10 NĂM · HAI CÁNH CỬA", "range": "THÁNG 0 → 120 · % SO VỚI 1,025 TỶ BAN ĐẦU",
          "money": round(BASE), "unit": "TR", "dates": RACE_DATES, "drawAt": [7, "Sau"], "until": [7, "sổ"], "illus": HYPO,
          "series": [{"label": "PHẢI · THUÊ + GỬI", "color": RENT, "vals": pct(W10)},
                     {"label": "TRÁI · GIÁ +5%/NĂM", "color": BUY, "vals": pct(B5)},
                     {"label": "TRÁI · GIÁ +3%/NĂM", "color": "#fdba74", "vals": pct(B3)},
                     {"label": "TRÁI · GIÁ ĐỨNG YÊN", "color": "#fed7aa", "vals": pct(B0)}],
          "source": "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH · TRÁI: GIÁ NHÀ × 98% − NỢ CÒN LẠI (NẾU BÁN) · PHẢI: SỔ TIẾT KIỆM 6,8% · "
                    "KHÔNG PHẢI DỰ BÁO"}
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "MƯỜI NĂM SAU HAI CÁNH CỬA"}, "bgm": {"mood": "mystery", "gain": 0.145}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "MƯỜI NĂM SAU\nHAI CÁNH CỬA", "sub": "CÙNG MỘT NGÂN SÁCH NHÀ Ở",
     "vid": "10577994", "ms": 12, "illus": ILL, "titleAt": [0, "Trở"]},
    {"type": "ledger", "at": 1, "title": "CÙNG MỘT NGÂN SÁCH", "illus": HYPO, "rows": [
        {"k": "TRÁI · MUA", "v": "NGÂN HÀNG + SỬA CHỮA", "at": [2, "Nhà"]},
        {"k": "PHẢI · THUÊ", "v": "THUÊ + GỬI PHẦN CHÊNH", "at": [3, "Nhà"]}],
     "total": {"k": "PHẢI GỬI TỪ NGÀY ĐẦU", "v": "1 TỶ + 25 TR", "at": [4, "một"]},
     "srcnote": "Gửi tiết kiệm 6,8%/năm, ghép lãi hằng tháng · ví dụ giả định"},
    {"type": "counter", "at": 5, "from": 0, "to": round(GAP1 * 1e6, -4), "suffix": " Đ", "until": [5, "rưỡi"],
     "label": "PHẦN CHÊNH THÁNG ĐẦU · BÊN PHẢI ĐỂ DÀNH",
     "sub": {"text": f"THÁNG 25: ≈ {vn(GAP25, 1)} TR · THÁNG 120: ≈ {vn(GAP120, 1)} TR", "at": [6, "Đầu"]},
     "illus": HYPO, "srcnote": f"{vn(PAY[1])} trả NH + {vn(V0 * REPAIR / 12)} sửa chữa − {vn(rent(1))} thuê ≈ {vn(GAP1)} tr · kênh tự tính"},
    RACE10,
    {"type": "ledger", "at": 9, "title": "BÊN TRÁI · BÁN, NỘP THUẾ, TRẢ NỢ", "illus": HYPO, "rows": [
        {"k": "GIÁ ĐỨNG YÊN", "v": f"≈ {vn(B0[-1] / 1000)} TỶ", "at": [9, "đứng"]},
        {"k": "GIÁ +3%/NĂM", "v": f"≈ {vn(B3[-1] / 1000)} TỶ", "at": [10, "ba"]},
        {"k": "GIÁ +5%/NĂM", "v": f"≈ {vn(B5[-1] / 1000)} TỶ", "at": [11, "năm"]}],
     "total": {"k": "BÊN PHẢI · SỔ TIẾT KIỆM", "v": f"≈ {vn(W10[-1] / 1000)} TỶ", "at": [11, "mốt"]},
     "srcnote": "Sau 10 năm: nợ còn 0,9 tỷ · thuế bán 2% · kênh tự tính"},
    {"type": "question", "at": 12, "text": "Vậy giá phải tăng bao nhiêu\nthì hai nhà mới ngang nhau?"},
    {"type": "slam", "at": [13, "bảy"], "text": "≈ 7,5% / NĂM", "sub": "ĐỀU ĐẶN 10 NĂM · KÊNH TỰ TÍNH · VÍ DỤ GIẢ ĐỊNH", "fx": "zoom",
     "label": {"k": "GIẢ ĐỊNH CỦA PHÉP TÍNH", "v": "GIỮ NGUYÊN LÃI VAY 14%, LÃI GỬI 6,8%, THUÊ +5%/NĂM",
               "s": "CHƯA GỒM MÔI GIỚI, NỘI THẤT", "at": [13, "bảy", 0, 0.7]},
     "srcnote": f"Hoà vốn = mức tăng giá làm hai bên bằng nhau sau 10 năm: {vn(100 * G_STAR)}%/năm · kênh tự tính"},
    {"type": "bars", "at": 14, "title": "HOÀ VỐN KHI ĐỔI MỘT GIẢ ĐỊNH", "unit": "%/NĂM · KÊNH TỰ TÍNH", "items": [
        {"k": "LÃI GỬI 5,2%", "v": 6.34, "lbl": "6,34", "at": [14, "tiết"]},
        {"k": "Ở 20 NĂM", "v": 6.64, "lbl": "6,64", "at": [14, "ở"]},
        {"k": "THẢ NỔI 12%", "v": 6.89, "lbl": "6,89", "at": [14, "thả"]},
        {"k": "THUÊ +8%/NĂM", "v": 7.06, "lbl": "7,06", "at": [14, "tăng"]},
        {"k": "VÍ DỤ GỐC", "v": round(100 * G_STAR, 2), "lbl": vn(100 * G_STAR), "at": [14, "Đổi"], "acc": True},
        {"k": "THẢ NỔI 15%", "v": 7.72, "lbl": "7,72", "at": [14, "nổi"]},
        {"k": "Ở 5 NĂM", "v": 8.08, "lbl": "8,08", "at": [14, "ở", 0, 0.3]},
        {"k": "LÃI GỬI 8%", "v": 8.32, "lbl": "8,32", "at": [14, "kiệm"]}],
     "illus": HYPO, "srcnote": "Mỗi cột đổi MỘT giả định, giữ nguyên phần còn lại · ví dụ giả định · kênh tự tính"},
    {"type": "kinetic", "at": 15, "items": [{"text": "Ở CÀNG LÂU · HOÀ VỐN CÀNG THẤP", "at": [15, "Ở"]},
                                           {"text": "5 NĂM 8,08% → 10 NĂM 7,45% → 20 NĂM 6,64%", "at": [15, "lâu"], "acc": True},
                                           {"text": "phí mua bán chia cho nhiều năm hơn", "at": [15, "phí"], "sm": True},
                                           {"text": "tiền thuê năm nào cũng tăng", "at": [15, "tiền"], "sm": True}],
     "illus": HYPO},
    {"type": "kinetic", "at": 16, "items": [{"text": "MUA NHÀ = ĐẶT CƯỢC", "at": [16, "Đó"], "fx": "pop"},   # sync sẽ hiện mờ tới chữ "mua" (~1,9 s) -> qa_blank
                                           {"text": "GIÁ TĂNG NHANH HƠN ≈ 7,5%/NĂM", "at": [16, "giá"], "acc": True},
                                           {"text": "5 năm qua (Hà Nội): ≈ 26%/năm", "at": [17, "Năm"], "sm": True},
                                           {"text": "quý II/2026: căn cũ −3% so quý I", "at": [18, "Còn"], "sm": True}],
     "srcnote": "Savills qua Người Quan Sát 16/01/2026 · CBRE qua TC Kinh tế Tài chính 07/07/2026"},
    {"type": "broll", "at": 19, "vid": "1509536", "ms": 8, "veil": 0.6, "illus": ILL,
     "kin": [{"text": "NỬA THỨ HAI", "at": [19, "Nửa"], "sm": True},
             {"text": "SAU CÁNH CỬA BÊN PHẢI", "at": [19, "cánh"], "acc": True},
             {"text": "giả định: để dành đủ từng đồng chênh lệch, suốt 120 tháng", "at": [20, "Phép"], "sm": True}]},
    {"type": "question", "at": 21, "text": "Nếu họ tiêu mất\nphần chênh thì sao?"},
    {"type": "ledger", "at": 22, "title": "NẾU TIÊU MẤT PHẦN CHÊNH", "illus": HYPO, "rows": [
        {"k": "SỔ TIẾT KIỆM SAU 10 NĂM", "v": f"≈ {vn(SPENT / 1000)} TỶ", "at": [22, "hai"]},
        {"k": "= 1 TỶ + 25 TR PHÍ MUA", "v": "+ TIỀN LÃI", "at": [22, "một"]}],
     "total": {"k": "HOÀ VỐN CỦA BÊN TRÁI", "v": "≈ 1,8%/NĂM", "at": [23, "hai"]},
     "srcnote": "1,025 tỷ × (1 + 6,8%/12)^120 ≈ 2,02 tỷ · hoà vốn 1,77%/năm · kênh tự tính"},
    {"type": "counter", "at": 24, "from": 0, "to": 600, "suffix": " TR", "until": [24, "trăm"],
     "label": "TIỀN GỐC BÊN TRÁI ĐÃ TRẢ SAU 10 NĂM", "sub": {"text": "120 THÁNG × 5 TR · TIẾT KIỆM BẮT BUỘC", "at": [24, "gốc"]},
     "illus": HYPO},
    {"type": "kinetic", "at": 25, "items": [{"text": "NGƯỜI THUÊ PHẢI TỰ ÉP MÌNH", "at": [25, "Người"], "acc": True}]},
    {"type": "slam", "at": 26, "text": "PHẦN CHÊNH PHẢI\nĐƯỢC ĐỂ DÀNH THẬT", "sub": "LỢI THẾ CỦA NGƯỜI THUÊ NẰM Ở ĐÓ", "fx": "zoom"},
]}

# ---------------- CH06 · Phần không nằm trong bảng tính ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "PHẦN KHÔNG NẰM TRONG BẢNG TÍNH"}, "bgm": {"mood": "calm", "gain": 0.17}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "PHẦN KHÔNG NẰM\nTRONG BẢNG TÍNH", "sub": "ỔN ĐỊNH · CƯ TRÚ · TRƯỜNG HỌC · SỨC CHỊU ĐỰNG",
     "vid": "5125499", "illus": ILL, "titleAt": [0, "Nhưng"]},
    {"type": "ledger", "at": 1, "title": "KHÔNG ĐO BẰNG TIỀN", "rows": [
        {"k": "01", "v": "ỔN ĐỊNH", "at": [1, "Có", 0, 0.3]},
        {"k": "02", "v": "CƯ TRÚ", "at": [1, "Có", 0, 0.7]},
        {"k": "03", "v": "TRƯỜNG HỌC", "at": [1, "Có", 0, 1.1]},
        {"k": "04", "v": "SỨC CHỊU ĐỰNG", "at": [1, "Có", 0, 1.5]}]},
    {"type": "broll", "at": 2, "vid": "7677492", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "01 · CẢM GIÁC ỔN ĐỊNH", "at": [2, "Thứ"]},
             {"text": "SỬA BẾP · NUÔI CHÓ · Ở TỚI GIÀ", "at": [3, "sửa"], "acc": True},
             {"text": "bên phải: mỗi lần gia hạn là một lần thương lượng", "at": [4, "Nhà"], "sm": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "02 · CƯ TRÚ", "at": [5, "Thứ"], "sm": True},
                                          {"text": "“HỘ KHẨU”", "at": [5, "hộ"], "acc": True}]},
    {"type": "date", "at": 6, "day": "SỔ HỘ KHẨU GIẤY HẾT GIÁ TRỊ", "date": "01.01.2023",
     "sub": {"text": "GIỜ: CƠ SỞ DỮ LIỆU CƯ TRÚ", "at": [6, "cơ"]}, "srcnote": "Luật Cư trú 2020, Điều 38 khoản 3"},
    {"type": "ledger", "at": 7, "title": "ĐĂNG KÝ THƯỜNG TRÚ", "rows": [
        {"k": "NHÀ CỦA MÌNH", "v": "KHÔNG ĐÒI DIỆN TÍCH", "at": [7, "Ở"]},
        {"k": "NHÀ THUÊ", "v": "CHỦ NHÀ ĐỒNG Ý + ≥ 8 M²/NGƯỜI", "at": [8, "Ở"]}],
     "total": {"k": "HÀ NỘI · NỘI THÀNH CŨ", "v": "≥ 15 M²/NGƯỜI", "at": [9, "mười"]},
     "srcnote": "Luật Cư trú 2020, Đ20 (≥ 8 m² sàn/người) · NQ 10/2023/NQ-HĐND Hà Nội, áp dụng tới 2030 (khu nội thành cũ)"},
    {"type": "kinetic", "at": 10, "items": [{"text": "03 · TRƯỜNG HỌC CHO CON", "at": [10, "Thứ"], "sm": True},
                                           {"text": "HÀ NỘI 2026–2027: MẦM NON, LỚP 1, LỚP 6", "at": [11, "Hà"]},
                                           {"text": "XÉT THEO NƠI CƯ TRÚ + KHOẢNG CÁCH", "at": [11, "nơi"], "acc": True},
                                           {"text": "thường trú hoặc tạm trú", "at": [11, "khoảng"], "sm": True}],
     "srcnote": "Công văn 1161/SGDĐT-QLT, Sở GD&ĐT Hà Nội (25/03/2026) · VietNamNet 12/03/2026"},
    {"type": "quote", "at": 12, "qline": 13, "lbl": "TRÍCH BÀI BÁO",
     "text": "Nơi cư trú được hiểu có thể là thường trú hoặc tạm trú.",
     "by": "VietNamNet, 12/03/2026 — tuyển sinh đầu cấp Hà Nội · Công văn 1161/SGDĐT-QLT (25/03/2026)"},
    {"type": "kinetic", "at": 14, "items": [{"text": "TP.HCM: CŨNG XÉT THEO NƠI CƯ TRÚ", "at": [14, "Thành"]},
                                           {"text": "cách xếp ưu tiên riêng", "at": [14, "cách"], "sm": True},
                                           {"text": "ĐỌC KẾ HOẠCH TUYỂN SINH CỦA PHƯỜNG MÌNH", "at": [15, "đọc"], "acc": True}],
     "srcnote": "QĐ 1700/QĐ-UBND TP.HCM (27/03/2026) · Cổng TTBC TP.HCM 25/03/2026"},
    {"type": "counter", "at": 16, "from": 0, "to": 70, "suffix": "%", "label": "04 · THU NHẬP DÀNH TRẢ NỢ · THÁNG 25",
     "sub": {"text": "MỘT LẦN MẤT VIỆC LÀ CHUYỆN KHÁC", "at": [17, "mất"]}, "illus": HYPO},
    {"type": "broll", "at": 18, "vid": "7347884", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "NGƯỜI THUÊ DỄ CHUYỂN THEO VIỆC, THEO TRƯỜNG", "at": [18, "Ngược"]},
             {"text": "NHƯNG CHƯA CÓ CHỖ CỦA RIÊNG MÌNH", "at": [18, "nhưng"], "acc": True}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "KHÔNG CỘT NÀO TRONG BẢNG TÍNH", "at": [19, "Không"]},
                                           {"text": "ĐO ĐƯỢC CẢM GIÁC ẤY", "at": [19, "đo"], "acc": True}]},
    {"type": "slam", "at": 20, "text": "CHỈ BẠN TỰ CÂN", "sub": "KHÔNG PHẢI LỜI KHUYÊN MUA HAY THUÊ", "fx": "zoom"},
]}

# ---------------- CH07 · Bảng tính của riêng bạn ----------------
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "BẢNG TÍNH CỦA RIÊNG BẠN"}, "bgm": {"mood": "warm", "gain": 0.155}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "BẢNG TÍNH\nCỦA RIÊNG BẠN", "sub": "KHÔNG PHẢI LỜI KHUYÊN MUA HAY THUÊ",
     "vid": "6963972", "ms": 12, "illus": ILL, "titleAt": [0, "Phép"]},
    {"type": "ledger", "at": 1, "title": "KHI NÀO VÍ DỤ NÀY KHÔNG ĐÚNG", "rows": [
        {"k": "01", "v": "GIA ĐÌNH CHO · KHÔNG CẦN VAY", "at": [2, "Nếu"]},
        {"k": "02", "v": "TỶ SUẤT CAO HƠN (ĐÀ NẴNG ≈ 4,3%)", "at": [3, "Nếu"]},
        {"k": "03", "v": "CĂN ĐANG XÂY: RỦI RO BÀN GIAO", "at": [4, "Nếu"]},
        {"k": "04", "v": "LÃI VAY ĐỔI (2025 THẤP HƠN 2026)", "at": [5, "Và"]}],
     "srcnote": "Đà Nẵng 4,34%: REFI qua CafeBiz 29/08/2026 · với tỷ suất này, hoà vốn ví dụ ≈ 6,1%/năm (kênh tự tính)"},
    {"type": "ledger", "at": 6, "title": "6 CÂU TỰ ĐIỀN · 1–3", "rows": [
        {"k": "01", "v": "TỶ SUẤT THUÊ CỦA BẠN?", "at": [7, "Một"]},
        {"k": "02", "v": "KHOẢN TRẢ: ƯU ĐÃI VÀ +3 ĐIỂM", "at": [9, "Hai"]},
        {"k": "03", "v": "PHẦN CHÊNH TỰ VÀO TIẾT KIỆM?", "at": [10, "Ba"]}]},
    {"type": "ledger", "at": 11, "title": "6 CÂU TỰ ĐIỀN · 4–6", "rows": [
        {"k": "04", "v": "Ở BAO LÂU: 5 HAY 20 NĂM?", "at": [11, "Bốn"]},
        {"k": "05", "v": "GIÁ PHẢI TĂNG BAO NHIÊU?", "at": [12, "Năm"]},
        {"k": "06", "v": "NGOÀI TIỀN, ĐIỀU GÌ QUAN TRỌNG?", "at": [13, "Sáu"]}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "CÔNG THỨC: XEM MÔ TẢ VIDEO", "at": [14, "Các"], "acc": True},
                                           {"text": "thay bằng số của chính bạn", "at": [14, "thay"], "sm": True}]},
    {"type": "broll", "at": 15, "vid": "31751335", "ms": 8, "veil": 0.55, "illus": ILL,
     "kin": [{"text": "HAI CÁNH CỬA", "at": [15, "Giờ"]},
             {"text": "HAI CUỘC ĐẶT CƯỢC", "at": [16, "cuộc"], "acc": True}]},
    {"type": "ledger", "at": 17, "title": "HAI CÁNH CỬA", "rows": [
        {"k": "TRÁI · MUA", "v": "CƯỢC VÀO GIÁ NHÀ", "at": [17, "Bên"]},
        {"k": "PHẢI · THUÊ", "v": "CƯỢC VÀO KỶ LUẬT", "at": [18, "Bên"]}]},
    {"type": "slam", "at": 19, "text": "HIỂU MÌNH ĐANG\nCƯỢC VÀO ĐIỀU GÌ", "sub": "KHÔNG BÊN NÀO CHẮC THẮNG", "fx": "zoom"},
    {"type": "kinetic", "at": 20, "items": [{"text": "QUYẾT ĐỊNH LỚN · CÒN TIẾP", "at": [20, "Chuỗi"], "acc": True},
                                           {"text": "những phép tính cho những khoản tiền lớn khác", "at": [20, "những"], "sm": True}]},
    {"type": "question", "at": 21, "text": "Nếu được chọn lại,\nbạn sẽ đứng sau cánh cửa nào,\nvà vì sao?"},
]}

TITLE = "Trả Góp 19 Triệu Hay Thuê 6 Triệu: 10 Năm Sau Ai Khá Hơn?"
DISCLAIMER = ("Nội dung giáo dục, không phải tư vấn tài chính, không phải lời khuyên mua hay thuê nhà, không dự báo giá nhà hay "
              "lãi suất. Căn hộ 2,5 tỷ, khoản vay, tiền thuê, mức tăng giá là ví dụ giả định do kênh tự tính. Số liệu thị trường "
              "lấy từ nguồn công khai (đa số qua báo chí dẫn lại); quá khứ không đảm bảo tương lai. Giọng đọc tổng hợp. Quy định "
              "mô tả theo thời điểm làm video (10/2026) và có thể thay đổi.")
# factcheck mục 4b (486 ký tự) + lượt 2 mục 9.3 (dòng người mua: thuế bán có thể được miễn) — describe.py giữ "more" nguyên vẹn
FORMULA = ("🧮 CÔNG THỨC (ví dụ giả định trong video · kênh tự tính · thay bằng số của bạn)\n"
           "• Tỷ suất cho thuê = tiền thuê 1 năm ÷ giá nhà\n"
           "• Trả gốc đều: gốc/tháng = khoản vay ÷ số tháng; lãi/tháng = dư nợ × lãi năm ÷ 12\n"
           "• Người thuê, mỗi tháng: Sổ = Sổ tháng trước × (1 + lãi gửi ÷ 12) + (trả ngân hàng + sửa chữa − tiền thuê); "
           "sổ ban đầu = tiền trả trước + phí mua\n"
           "• Người mua sau N năm = giá nhà × (1 + g)^N × (1 − 2% thuế bán) − dư nợ (thuế bán 2% — có thể được miễn nếu là nhà ở duy nhất)\n"
           "• Hoà vốn = mức g làm hai bên bằng nhau (ví dụ: ≈ 7,45%/năm)")
SPEC = {
    "title": TITLE, "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO",
    "acc": ["mua", "thuê", "lãi", "vốn", "tỷ", "triệu", "vn-index"],
    "say": SAY, "imgs": {}, "chapters": list(CH),
    "youtube": {
        "titles": [TITLE, "Mua Nhà Hay Thuê Rồi Để Dành Phần Chênh? Phép Tính 10 Năm Với Thu Nhập 30 Triệu",
                   "Giá Nhà Phải Tăng Bao Nhiêu Mỗi Năm Thì Mua Mới Bằng Thuê? Một Phép Tính 10 Năm"],
        "summary": "Hai căn hộ giống hệt nhau trên cùng một hành lang, khoảng 2,5 tỷ: nhà bên trái mua và trả ngân hàng gần 19 "
                   "triệu mỗi tháng, nhà bên phải đi thuê khoảng 6 triệu. Tiền thuê một năm chỉ bằng khoảng 3% giá nhà, lãi vay "
                   "sau ưu đãi 13–15%, vậy mà 5 năm qua người mua căn hộ Hà Nội lại thắng đậm. Bài 1 chuỗi Quyết định lớn tính "
                   "trọn 10 năm cho hai cánh cửa: tỷ suất cho thuê, cú nhảy khoản trả ở tháng thứ 25, phí và thuế, chi phí cơ hội "
                   "của 1 tỷ trả trước, rồi mức tăng giá nhà phải đạt để hai bên ngang nhau — và điều gì xảy ra nếu người thuê "
                   "không để dành phần chênh. Ví dụ giả định, số liệu có nguồn, không phải lời khuyên mua hay thuê.",
        "more": [DISCLAIMER, FORMULA],
        "chapter_titles": {"ch00": "Mở đầu: hai cánh cửa cạnh nhau", "ch01": "Con số ba phần trăm",
                           "ch02": "Khoản vay, và cú nhảy năm thứ ba", "ch03": "Những khoản không nằm trong giá",
                           "ch04": "Một tỷ trả trước cũng có giá", "ch05": "Mười năm sau hai cánh cửa",
                           "ch06": "Phần không nằm trong bảng tính", "ch07": "Bảng tính của riêng bạn"},
        "sources": [
            "CafeBiz 29/08/2026 — lợi suất cho thuê căn hộ quý II/2026 (REFI): https://cafebiz.vn/loi-suat-cho-thue-nha-chi-con-tu-2-3-bat-dong-san-con-hap-dan-176260829091836212.chn",
            "Tạp chí Kinh tế Tài chính 07/07/2026 — CBRE, căn hộ Hà Nội quý II/2026: https://tapchikinhtetaichinh.vn/nguon-cung-can-ho-ha-noi-lap-ky-luc-gia-thu-cap-lan-dau-giam-sau-gan-4-nam-161086.html",
            "VnExpress 02/09/2026 — Bộ Xây dựng, giá căn hộ quý II/2026: https://vnexpress.net/gia-chung-cu-dat-nen-ha-nhiet-5112330.html",
            "Người Quan Sát 16/01/2026 — Savills, giá chung cư Hà Nội so với 2019: https://nguoiquansat.vn/gia-chung-cu-ha-noi-tang-hon-200-so-voi-nam-2019-268972.html",
            "Dân trí 03/09/2026 — lãi vay mua nhà tháng 9 (DKRA, 11 ngân hàng): https://dantri.com.vn/bat-dong-san/thang-9-cac-ngan-hang-dang-cho-vay-mua-nha-lai-suat-bao-nhieu-20260903083127075.htm",
            "VnExpress 04/08/2026 — VARS-IRE, lãi vay 13–15% sau ưu đãi: https://vnexpress.net/nguoi-mua-nha-doi-mat-lai-vay-13-15-sau-uu-dai-5104630.html",
            "Báo Xây dựng 15/04/2026 — lợi nhuận cho thuê căn hộ (Batdongsan.com.vn): https://batdongsan.baoxaydung.vn/loi-nhuan-cho-thue-can-ho-giam-192260414222043956.htm",
            "NSO — CPI tháng 9 và 9 tháng 2026: https://www.nso.gov.vn/wp-content/uploads/2026/10/Tong-quan-CPI-chi-so-gia-vang-do-la-My-thang-9-QIII-va-9-thang-nam-2026.pdf",
            "Luật Thuế thu nhập cá nhân số 109/2025/QH15 (Điều 4, 14): https://thuvienphapluat.vn/van-ban/thue-phi-le-phi/Luat-Thue-thu-nhap-ca-nhan-2025-so-109-2025-QH15-665870.aspx",
            "Thư viện Pháp luật — lệ phí trước bạ nhà đất 2026: https://thuvienphapluat.vn/phap-luat-nha-dat/le-phi-truoc-ba-nha-dat-nam-2026-hien-nay-la-bao-nhieu-14934.html",
            "Thư viện Pháp luật — kinh phí bảo trì căn hộ (Luật Nhà ở 2023, Điều 152): https://thuvienphapluat.vn/phap-luat-nha-dat/nguoi-mua-can-ho-chung-cu-co-bat-buoc-phai-dong-phi-bao-tri-chung-cu-khong-8987.html",
            "VnEconomy — Hà Nội khung giá dịch vụ nhà chung cư từ 23/02/2026: https://vneconomy.vn/ha-noi-quy-dinh-khung-gia-dich-vu-nha-chung-cu-tu-2322026.htm",
            "Tuổi Trẻ 08/01/2026 — diện tích tối thiểu đăng ký thường trú: https://tuoitre.vn/nha-31m2-nhung-khong-duoc-dang-ky-thuong-tru-cho-4-nguoi-co-dung-khong-20260108105123535.htm",
            "Báo Chính phủ 06/07/2023 — Hà Nội 15 m² sàn/người nội thành: https://thanglong.chinhphu.vn/ha-noi-dien-tich-nha-o-toi-thieu-de-dang-ky-thuong-tru-tai-noi-thanh-la-15m2-san-nguoi-103230706102726962.htm",
            "PLO — sổ hộ khẩu hết giá trị từ 01/01/2023: https://plo.vn/tu-1-1-2023-se-khong-thu-hoi-so-ho-khau-nua-post695521.html",
            "VietNamNet 12/03/2026 — tuyển sinh mầm non, lớp 1, lớp 6 Hà Nội theo nơi cư trú: https://vietnamnet.vn/ha-noi-lan-dau-tien-tuyen-sinh-mam-non-lop-1-va-lop-6-theo-noi-cu-tru-2496868.html",
            "Cổng TTBC TP.HCM 25/03/2026 — quy định tuyển sinh đầu cấp: https://ttbc-hcm.gov.vn/ubnd-tp-hcm-chinh-thuc-cong-bo-quy-dinh-tuyen-sinh-dau-cap-lop-1-6-10-1020933.html",
            "Dữ liệu kênh tự tính — VN-Index và giá vàng miếng SJC qua Vnstock (nguồn VCI): https://vnstocks.com/docs/vnstock-data/du-lieu-giao-dich",
            "Sở GD&ĐT Hà Nội — Công văn 1161/SGDĐT-QLT ngày 25/03/2026 (tuyển sinh theo nơi cư trú và khoảng cách)",
            "VietnamFinance 07/07/2026 và CafeF 14/08/2026 — CBRE, Savills: không có dự án mới dưới 60 triệu/m², mọi hàng sơ cấp trên 70 triệu/m²",
            "VietNamNet 09/09/2026 — lãi tiền gửi 12 tháng 4 ngân hàng lớn 6,8%; VnEconomy 27/01/2026 — mức 5,2% tháng 1/2026",
        ],
        "hashtags": ["MuaNhàHayThuêNhà", "TàiChínhCáNhân", "QuyếtĐịnhLớn", "BiểuĐồBiếtNói"],
        "tags": ["mua nhà hay thuê nhà", "có nên mua nhà", "thuê nhà hay mua nhà", "tỷ suất cho thuê", "lãi vay mua nhà 2026",
                 "lãi thả nổi", "trả góp mua nhà", "giá căn hộ Hà Nội", "chi phí cơ hội", "tiết kiệm phần chênh",
                 "điểm hoà vốn mua nhà", "thuế bán nhà 2%", "tài chính cá nhân", "quyết định lớn"],
        "category": "27",
        "data_credit": "📊 DỮ LIỆU BIỂU ĐỒ: VN-Index và giá vàng miếng SJC truy xuất qua Vnstock (nguồn VCI); số liệu thị trường bất động "
                       "sản, lãi vay, thuế phí theo các nguồn ở trên; ví dụ hai căn hộ (giá, khoản vay, tiền thuê, mức tăng giá) là giả "
                       "định do kênh tự tính.",
        "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels"],
    },
}

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(D.parents[2]))
    from factory.console import utf8_console
    utf8_console()
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec + %d chương, %d cảnh · hoà vốn %.3f%% · công thức %d ký tự" % (
        len(CH), sum(len(c["scenes"]) for c in CH.values()), 100 * G_STAR, len(FORMULA)))
