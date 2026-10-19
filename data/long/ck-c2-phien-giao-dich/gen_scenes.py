"""Sinh spec.json + scenes/hud/bgm cho video dài CK C2 "Vì sao có ngày muốn bán cổ phiếu mà không bán được? Một phiên HOSE
từ 9 giờ tới 15 giờ" (Chứng khoán từ số 0 · Bài 2; kênh Biểu Đồ Biết Nói, theme "chart"). Kể qua phiên thứ Hai 09/03/2026.

    python data/long/ck-c2-phien-giao-dich/gen_scenes.py     # giữ nguyên "lines" + "title" trong chNN.json (script_lines ghi)

Dữ kiện + nguồn: docs/channels/chung-khoan/2026-10-07-long-c2-research.md; kiểm chứng: factcheck.md (cùng thư mục) — chữ trên
màn hình theo mục 1c (đã sửa: "KHÔNG CÒN NGƯỜI MUA Ở GIÁ SÀN", nguồn QĐ 22/QĐ-HĐTV, "TRƯỚC 13:00 NGÀY T+2", "TỐI ĐA 0,45%",
thẻ HNX → HOSE 28/12/2026, "TRƯỚC KHI BẤM NÚT", nhãn "VÍ DỤ GIẢ ĐỊNH" bắt buộc trên hàng đợi giá sàn 09/03).
Mô-típ lộ trình = ĐỒNG HỒ PHIÊN (cảnh timeline 8 mốc, cùng chữ mọi lần, mốc hiện tại vàng, mốc khác xám): CH00 (câu lộ trình,
hiện lần lượt theo lời), đầu CH02–CH05, giữa CH03 (nghỉ trưa), CH06 (trọn vẹn).
Cảnh mới theme chart: `book` (sổ lệnh giả định: bảng MUA|GIÁ|BÁN, hàng đợi ở giá sàn) và `breadth` base "prev" (màu theo %
trong ngày, thang kiểu bảng giá: xanh lơ ≈ sàn) — chart.js + casewide.css, dữ liệu chartdata._attach_breadth_prev.
Luật kênh: chỉ giáo dục, không khuyến nghị, không dự báo; không tên công ty chứng khoán / ngân hàng / ứng dụng / mã cổ phiếu.
Clip: Pexels (ngang), mọi b-roll ghi "VIDEO MINH HỌA". Neo: chữ ĐẦU TIÊN của mỗi cảnh neo vào từ ĐẦU câu; slam không chờ chữ
muộn (dùng kinetic có dòng dẫn nhỏ); counter đếm từ đầu cảnh; mọi số trên màn hình có nguồn (srcnote/source).
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

UP, DN, GOLD, BLUE, CYAN, GREY = "#4ade80", "#f87171", "#fbbf24", "#38bdf8", "#22d3ee", "#64748b"
ILL = "VIDEO MINH HỌA"
SRC_DAY = "Dữ liệu: giá đóng cửa HOSE (vnstock/VCI), kênh tự tính · minh hoạ quá khứ, không phải khuyến nghị"
SRC_RULE = "Quy chế Niêm yết và giao dịch CK niêm yết — VNX, QĐ 22/QĐ-HĐTV ngày 18/04/2025"
SRC_HOURS = "Giờ: tài liệu thành viên tóm tắt quy định giao dịch HOSE (05/2025) · quy định tại thời điểm làm video (10/2026)"

# Bảng đọc: giữ các mục C1/D1 (đổi bảng = đổi khoá cache TTS; sjc không cần) + thuật ngữ phiên giao dịch.
SAY = {"vn-index": "Vi En In-đéc", "hose": "hô-dê", "vic": "vi ai xi", "vhm": "vi hát em", "vre": "vi rờ e", "vpl": "vi pê en",
       "ree": "rê ê ê", "sam": "xam", "gdp": "gi đi pi", "etf": "i ti ép", "hnx": "hát en ích", "upcom": "úp-com",
       "margin": "ma-gin", "app": "áp", "vingroup": "Vin-grúp", "vietnambiz": "Việt Nam Biz",
       "fomo": "phô-mô", "vnexpress": "Vi En Ếch-prét",
       "ato": "a tê ô", "atc": "a tê xê", "krx": "ca e-rờ ích", "mtl": "em tê eo", "=LO": "eo ô", "vsd": "vi ét đê",
       "vnx": "vi en ích", "ccp": "xê xê pê", "ubcknn": "Uỷ ban Chứng khoán Nhà nước", "=T": "tê"}

# ---------------- mô-típ ĐỒNG HỒ PHIÊN ----------------
CLOCK = [("9:00", "MỞ CỬA · ATO"), ("9:15", "KHỚP LIÊN TỤC"), ("11:30", "NGHỈ TRƯA"), ("13:00", "KHỚP LIÊN TỤC"),
         ("14:30", "ĐÓNG CỬA · ATC"), ("14:45", "THOẢ THUẬN"), ("15:00", "HẾT GIỜ"), ("T+2", "CỔ PHIẾU, TIỀN VỀ")]
CLOCK_NOTE = "Giờ giao dịch cổ phiếu HOSE (tài liệu thành viên, 05/2025) · T+2: VSD · quy định tại thời điểm làm video (10/2026)"


def clock(line, word, now=None, seq=None, tag="ĐỒNG HỒ PHIÊN · HOSE"):
    """now: chỉ số các mốc đang sáng (vàng), mốc khác xám; None = mọi mốc vàng. seq: mốc thời gian riêng cho từng mốc
    (mặc định: hiện liền nhau ngay đầu cảnh, 0,07 s một mốc)."""
    items = []
    for k, (t, lbl) in enumerate(CLOCK):
        it = {"year": t, "text": lbl, "at": seq[k] if seq else [line, word, 0, round(0.1 + 0.07 * k, 2)]}
        if now is not None:
            it["color"] = GOLD if k in now else GREY
        items.append(it)
    return {"type": "timeline", "at": [line, word], "items": items, "tag": {"text": tag, "at": [line, word]},
            "srcnote": CLOCK_NOTE}


# ---------------- sổ lệnh giả định (ATO, CH02) ----------------
ATO_BUY = [(20100, 300), (20000, 500), (19900, 700)]
ATO_SELL = [(19900, 400), (20000, 600), (20100, 800)]
BAND = {"ref": 20000, "ceil": 21400, "floor": 18600}


def ato_rows(line, w_buy, w_sell, step=0.15):
    return ([{"side": "buy", "price": p, "qty": q, "at": [line, w_buy, 0, round(step * k, 2)]} for k, (p, q) in enumerate(ATO_BUY)]
            + [{"side": "sell", "price": p, "qty": q, "at": [line, w_sell, 0, round(step * k, 2)]} for k, (p, q) in enumerate(ATO_SELL)])


# Gain nhạc nền: chuẩn hoá theo độ to trung bình từng bài (volumedetect 90 s) về mức của C1 (≈ −19,3 dB ở gain 0,11).
CH = {}

# ---------------- CH00 · Thứ Hai, chín tháng ba (cold open → lộ trình đồng hồ phiên → nhận diện kênh) ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MUỐN BÁN MÀ KHÔNG BÁN ĐƯỢC"}, "bgm": {"mood": "calm", "gain": 0.085}, "scenes": [
    {"type": "date", "vid": "35124446", "illus": ILL, "day": "CHIỀU THỨ HAI", "date": "09.03.2026",
     "sub": {"text": "VIDEO GIÁO DỤC · KHÔNG PHẢI LỜI KHUYÊN MUA, BÁN CỔ PHIẾU", "at": [0, "Giả"]}},
    {"type": "breadth", "at": 1, "base": "prev", "date": "2026-03-09", "title": "395 CỔ PHIẾU HOSE · MỖI Ô MỘT MÃ",
     "range": "09/03/2026 · SO VỚI PHIÊN TRƯỚC", "drawAt": [1, "Hơn"], "until": [1, "xanh"],
     "chipAt": [2, "Trên"], "chip": "XANH LƠ = GIÁ SÀN"},
    {"type": "candles", "at": 3, "series": "vnindex", "from": "2026-02-02", "to": "2026-04-03", "drawAt": [3, "Hôm"],
     "until": [3, "căng"], "title": "VN-INDEX · KHUNG NGÀY", "range": "02/2026 – 04/2026", "ind": [],
     "source": "DỮ LIỆU: VN-INDEX (VNSTOCK/VCI) · \"LẦN ĐẦU > 100 ĐIỂM\": NHÂN DÂN, MEKONG ASEAN 09/03/2026 · KHÔNG PHẢI KHUYẾN NGHỊ",
     "marks": [{"date": "2026-03-09", "text": "09/03: −115,05 ĐIỂM · ĐÓNG CỬA 1.652,79", "pos": "below", "tone": "down",
                "at": [3, "mất"], "dx": -120, "dy": 30},
               {"date": "2026-03-09", "text": "LẦN ĐẦU GIẢM > 100 ĐIỂM / PHIÊN", "pos": "above", "tone": "gold",
                "at": [4, "Đây"], "dx": 260, "dy": -30}]},
    {"type": "ledger", "at": 5, "title": "HOSE · 09/03/2026", "rows": [
        {"k": "GIẢM", "v": "366 MÃ", "at": [5, "Trên"]},
        {"k": "ĐỨNG GIÁ", "v": "10 MÃ", "at": [5, "Trên", 0, 0.3]},
        {"k": "TĂNG", "v": "11 MÃ", "at": [5, "mười"]}],
     "total": {"k": "TRONG ĐÓ GIẢM SÀN", "v": "233 MÃ", "at": [5, "hai"]},
     "srcnote": "Báo Nhân Dân, Thời báo Tài chính 09/03/2026 · toàn sàn HOSE"},
    {"type": "breadth", "at": 6, "base": "prev", "date": "2026-03-09", "title": "XẾP HÀNG: GIẢM NHIỀU NHẤT → TĂNG NHIỀU NHẤT",
     "range": "09/03/2026 · SO VỚI PHIÊN TRƯỚC", "drawAt": [6, "Theo"], "until": [6, "giữa"],
     "medianAt": [6, "sáu"], "medianText": "TRUNG VỊ −6,8% · SÀN = −7%"},
    {"type": "kinetic", "at": 7, "vid": "3191576", "illus": ILL,
     "items": [{"text": "CHI TIẾT LẠ NHẤT", "at": [7, "Nhưng"], "sm": True},
               {"text": "HÀNG LOẠT MÃ DƯ BÁN SÀN", "at": [8, "Hết"]},
               {"text": "HÀNG TRIỆU CỔ PHIẾU", "at": [8, "triệu"], "acc": True},
               {"text": "KHÔNG CÒN NGƯỜI MUA Ở GIÁ SÀN", "at": [8, "không"]}],
     "srcnote": "Thời báo Tài chính, 09/03/2026"},
    {"type": "question", "at": 9, "text": "Cổ phiếu của mình,\nmình muốn bán mà cũng\nkhông bán được à?"},
    {"type": "slam", "at": 10, "text": "ĐÚNG VẬY", "hitAt": [10, "Đúng"]},
    {"type": "kinetic", "at": 11, "items": [{"text": "CÓ NGƯỜI CÒN KHÔNG ĐƯỢC ĐẶT LỆNH BÁN", "at": [11, "Và"]},
                                           {"text": "DÙ ĐÃ MUA TỪ THỨ SÁU TUẦN TRƯỚC", "at": [11, "dù"], "acc": True}]},
    clock(12, "Để", seq=[[12, "Để", 0, round(0.1 + 0.35 * k, 2)] for k in range(8)]),   # lộ trình hiện dần ngay đầu câu, xong khi tới "đồng hồ"
    {"type": "brand", "at": 13, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 14, "items": [{"text": "BÀI 2 · CHỨNG KHOÁN TỪ SỐ 0", "at": [14, "Và"], "acc": True},
                                           {"text": "chỉ nhằm giáo dục · không phải lời khuyên mua hay bán", "at": [15, "Video"], "sm": True},
                                           {"text": "quy định mô tả theo thời điểm làm video: 10/2026", "at": [15, "Video", 0, 0.6], "sm": True}]},
]}

# ---------------- CH01 · Trước chín giờ: một lệnh gồm những gì ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "TRƯỚC CHÍN GIỜ: MỘT LỆNH GỒM NHỮNG GÌ"}, "bgm": {"mood": "upbeat", "gain": 0.083}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "TRƯỚC CHÍN GIỜ:\nMỘT LỆNH GỒM NHỮNG GÌ", "sub": "LỆNH · LÔ · BƯỚC GIÁ · KHUNG GIÁ",
     "vid": "15169256", "illus": ILL, "titleAt": [0, "Ở"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "ỨNG DỤNG", "at": [1, "Lệnh"]},
                                          {"text": "→ CÔNG TY CHỨNG KHOÁN", "at": [1, "qua"]},
                                          {"text": "→ HỆ THỐNG CỦA SỞ GIAO DỊCH (KRX)", "at": [1, "vào"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "MỘT LỆNH · VÍ DỤ GIẢ ĐỊNH", "rows": [
        {"k": "MÃ CỔ PHIẾU", "v": "MÃ A", "at": [2, "mã"]},
        {"k": "MUA HAY BÁN", "v": "MUA", "at": [2, "mua"]},
        {"k": "BAO NHIÊU CỔ PHIẾU", "v": "100", "at": [2, "bao"]},
        {"k": "GIÁ", "v": "20.000 Đ", "at": [2, "giá"]}],
     "total": {"k": "LOẠI LỆNH", "v": "GIỚI HẠN (LO)", "at": [3, "Loại"]}},
    {"type": "kinetic", "at": 5, "items": [{"text": "SỐ LƯỢNG KHÔNG TUỲ Ý", "at": [5, "Số"]},
                                          {"text": "LÔ CHẴN = 100 CỔ PHIẾU", "at": [6, "Trên"]},
                                          {"text": "LÔ LẺ = 1–99 CỔ PHIẾU", "at": [7, "Muốn"]},
                                          {"text": "LÔ LẺ: KHỚP CÙNG PHIÊN · CHỈ LỆNH GIỚI HẠN (LO)", "at": [8, "Từ"], "acc": True}],
     "srcnote": SRC_RULE + ", Điều 32 · lô 100: HOSE"},
    {"type": "question", "at": 9, "text": "Một lô 100 cổ phiếu\nthì tốn bao nhiêu tiền?"},
    {"type": "kinetic", "at": 10, "items": [{"text": "TUỲ MÃ", "at": [10, "Tuỳ"]},
                                           {"text": "CỔ PHIẾU ĐỨNG GIỮA SÀN HOSE · CUỐI THÁNG 9", "at": [11, "Theo"], "sm": True},
                                           {"text": "≈ 15.400 Đ", "at": [11, "mười"], "acc": True}],
     "srcnote": "Trung vị giá 406 cổ phiếu HOSE, giá đóng cửa gần nhất tới 30/09/2026 (vnstock/VCI) · kênh tự tính"},
    {"type": "counter", "at": 12, "from": 0, "to": 1540000, "suffix": " đ", "countAt": [12, "Vậy"], "until": [12, "rưỡi"],
     "label": "1 LÔ · 100 × ≈ 15.400 Đ · CHƯA GỒM PHÍ",
     "sub": {"text": "CHƯA TỚI 1/5 THU NHẬP BÌNH QUÂN THÁNG ≈ 9 TRIỆU", "at": [12, "chưa", 1]},
     "srcnote": "Kênh tự tính · thu nhập bình quân lao động quý I/2026: Tổng cục Thống kê (NSO)"},
    {"type": "bars", "at": 13, "title": "BƯỚC GIÁ · CỔ PHIẾU HOSE", "unit": "SỐ MÃ · KÊNH TỰ TÍNH · n = 406", "items": [
        {"k": "DƯỚI 10.000 Đ · BƯỚC 10 Đ", "v": 126, "lbl": "126 MÃ", "at": [14, "Cổ"]},
        {"k": "10.000–49.950 Đ · BƯỚC 50 Đ", "v": 234, "lbl": "234 MÃ", "at": [15, "Từ"]},
        {"k": "TỪ 50.000 Đ · BƯỚC 100 Đ", "v": 46, "lbl": "46 MÃ", "at": [16, "Từ"]}],
     "srcnote": "Bước giá: quy định HOSE · số mã: giá đóng cửa gần nhất tới 30/09/2026 (vnstock/VCI), kênh tự tính"},
    {"type": "kinetic", "at": 17, "items": [{"text": "MỘT KHUNG GIÁ MỖI NGÀY", "at": [17, "Và"], "sm": True},
                                           {"text": "THAM CHIẾU = GIÁ ĐÓNG CỬA PHIÊN TRƯỚC", "at": [18, "Mỗi"]},
                                           {"text": "thường vậy · trừ ngày điều chỉnh quyền", "at": [18, "thường"], "sm": True},
                                           {"text": "TRẦN +7% · SÀN −7%", "at": [19, "Trên"], "acc": True}],
     "srcnote": SRC_RULE + ", Điều 31 · biên độ ±7%: HOSE"},
    {"type": "ledger", "at": 21, "title": "KHUNG GIÁ · VÍ DỤ GIẢ ĐỊNH", "rows": [
        {"k": "TRẦN · MÀU TÍM", "v": "21.400", "at": [21, "trần"]},
        {"k": "THAM CHIẾU · MÀU VÀNG", "v": "20.000", "at": [21, "Ví"]},
        {"k": "SÀN · MÀU XANH LƠ", "v": "18.600", "at": [21, "sàn"]}],
     "total": {"k": "HOSE", "v": "±7% MỖI NGÀY", "at": [22, "Bảng"]},
     "srcnote": "20.000 × 1,07 = 21.400 · × 0,93 = 18.600 · màu: quy ước hiển thị phổ biến của bảng giá"},
    {"type": "slam", "at": 23, "text": "GIÁ SÀN", "hitAt": [23, "giá"], "sub": "GIỮ HAI CHỮ NÀY TRONG ĐẦU"},
]}

# ---------------- CH02 · Chín giờ: phiên mở cửa, một cái giá cho tất cả ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "9:00 · PHIÊN MỞ CỬA (ATO)"}, "bgm": {"mood": "warm", "gain": 0.14}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "CHÍN GIỜ:\nPHIÊN MỞ CỬA", "sub": "MỘT CÁI GIÁ CHO TẤT CẢ · ATO",
     "vid": "39488470", "illus": ILL, "titleAt": [0, "Chín"]},
    clock(1, "Đây", now={0}),
    {"type": "kinetic", "at": 2, "items": [{"text": "9:00 – 9:15 · ATO", "at": [2, "Hệ"], "sm": True},
                                          {"text": "HỆ THỐNG CHỈ GOM LỆNH", "at": [2, "Hệ", 0, 0.15]},
                                          {"text": "9:15 · MỘT GIÁ DUY NHẤT", "at": [3, "Đúng"], "acc": True},
                                          {"text": "GIÁ KHỚP ĐƯỢC NHIỀU CỔ PHIẾU NHẤT", "at": [3, "mức", 1]}],
     "srcnote": SRC_RULE + ", Điều 20 · giờ: tài liệu thành viên (05/2025)"},
    {"type": "book", "at": 4, "title": "SỔ LỆNH GIẢ ĐỊNH · PHIÊN ATO", **BAND, "rows": ato_rows(4, "sổ", "giá")},
    {"type": "bars", "at": 5, "title": "NẾU CHỌN GIÁ NÀY · KHỚP ĐƯỢC BAO NHIÊU?", "unit": "CỔ PHIẾU · VÍ DỤ GIẢ ĐỊNH", "items": [
        {"k": "GIÁ 19.900", "v": 400, "lbl": "400", "at": [5, "Khớp"]},
        {"k": "GIÁ 20.000", "v": 800, "lbl": "800", "at": [7, "Ở"], "acc": True},
        {"k": "GIÁ 20.100", "v": 300, "lbl": "300", "at": [6, "Khớp"]}],
     "srcnote": "Ví dụ giả định · khớp được = min(tổng mua ở giá đó trở lên, tổng bán ở giá đó trở xuống)"},
    {"type": "book", "at": 8, "title": "SỔ LỆNH GIẢ ĐỊNH · PHIÊN ATO", **BAND, "rows": ato_rows(8, "Đó", "Đó", step=0.06),
     "match": {"price": 20000, "at": [8, "giá"], "text": "GIÁ MỞ CỬA 20.000 · KHỚP 800 CỔ PHIẾU",
               "sub": {"text": "ĐẶT MUA 20.100 CŨNG CHỈ TRẢ 20.000", "at": [10, "Kể"]}}},
    {"type": "kinetic", "at": 11, "items": [{"text": "15 PHÚT GOM LỆNH", "at": [11, "Trong"]},
                                           {"text": "KHÔNG SỬA · KHÔNG HUỶ", "at": [11, "không"], "acc": True}],
     "srcnote": SRC_RULE + ", Điều 21"},
    {"type": "question", "at": 12, "text": "Sao không đợi\nxem giá rồi mới đặt?"},
    {"type": "kinetic", "at": 13, "items": [{"text": "CHƯA CÓ GIÁ KHỚP THẬT", "at": [13, "Vì"]},
                                           {"text": "BẢNG GIÁ CHỈ HIỆN GIÁ DỰ KIẾN", "at": [13, "Bảng"], "acc": True},
                                           {"text": "còn đổi cho tới 9:15", "at": [13, "còn"], "sm": True},
                                           {"text": "MỌI LỆNH ĐẶT TRƯỚC GIỜ MỞ CỬA: CÙNG MỘT GIÁ", "at": [14, "Cách"]}],
     "srcnote": "Giá khớp dự kiến trong ATO/ATC: tài liệu thành viên tóm tắt quy định HOSE (05/2025)"},
    {"type": "date", "at": 15, "day": "HOSE CHẠY HỆ THỐNG GIAO DỊCH MỚI (KRX)", "date": "05.05.2025",
     "srcnote": "Báo Chính phủ, 05/05/2025"},
    {"type": "kinetic", "at": 16, "items": [{"text": "LỆNH ATO KHÔNG CHEN TRƯỚC", "at": [16, "Lệnh"]},
                                           {"text": "LỆNH MUA TRẦN · LỆNH BÁN SÀN ĐÃ ĐẶT TỪ TRƯỚC", "at": [16, "những"]},
                                           {"text": "Ở GIÁ SÀN: AI ĐẾN TRƯỚC, ĐỨNG TRƯỚC", "at": [17, "Nghĩa"], "acc": True}],
     "srcnote": SRC_RULE + ", Điều 17"},
    {"type": "kinetic", "at": 18, "items": [{"text": "09/03/2026 · NHỮNG MÃ NẰM SÀN", "at": [18, "Hôm"], "sm": True},
                                           {"text": "THỨ TỰ XẾP HÀNG", "at": [18, "thứ"]},
                                           {"text": "QUYẾT ĐỊNH AI BÁN ĐƯỢC TRƯỚC", "at": [18, "quyết"], "acc": True}]},
]}

# ---------------- CH03 · Chín giờ mười lăm: khớp liên tục, và hàng đợi ở giá sàn ----------------
QUEUE = ["09:00", "09:00", "09:03", "09:07", "09:12", "09:16", "09:21", "09:30", "09:42", "09:55", "10:08", "10:20"]
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "9:15 · KHỚP LIÊN TỤC, HÀNG ĐỢI GIÁ SÀN"}, "bgm": {"mood": "calm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CHÍN GIỜ MƯỜI LĂM:\nKHỚP LIÊN TỤC", "sub": "VÀ HÀNG ĐỢI Ở GIÁ SÀN",
     "vid": "39488470", "ms": 5, "illus": ILL, "titleAt": [0, "Từ"]},
    clock(1, "Lệnh", now={1}),
    {"type": "ledger", "at": 2, "title": "HAI LUẬT KHỚP LỆNH", "rows": [
        {"k": "01", "v": "GIÁ TỐT HƠN ĐI TRƯỚC", "at": [2, "Một"]},
        {"k": "02", "v": "CÙNG GIÁ: AI ĐẾN TRƯỚC ĐI TRƯỚC", "at": [3, "Hai"]}],
     "total": {"k": "GIÁ KHỚP", "v": "= GIÁ LỆNH ĐANG CHỜ", "at": [4, "Và"]},
     "srcnote": "Tài liệu thành viên tóm tắt quy định HOSE (05/2025)"},
    {"type": "book", "at": 5, "title": "SỔ LỆNH GIẢ ĐỊNH · KHỚP LIÊN TỤC", **BAND,
     "rows": [{"side": "sell", "price": 20100, "qty": 500, "at": [5, "Ví"]},
              {"side": "buy", "price": 20000, "qty": 400, "at": [5, "Ví", 0, 0.15]},
              {"side": "buy", "price": 20100, "qty": 100, "at": [5, "bạn"]},
              {"side": "sell", "price": 20050, "qty": 300, "at": [5, "đang"]}],
     "match": {"price": 20050, "at": [6, "Bạn"], "text": "KHỚP Ở 20.050 · RẺ HƠN GIÁ BẠN ĐẶT"}},
    {"type": "kinetic", "at": 7, "items": [{"text": "LỆNH THỊ TRƯỜNG (MTL)", "at": [7, "Còn"]},
                                          {"text": "KHỚP NGAY GIÁ TỐT NHẤT ĐANG CHỜ", "at": [7, "giá"]},
                                          {"text": "KHÔNG BIẾT TRƯỚC CHÍNH XÁC GIÁ", "at": [7, "không"], "acc": True},
                                          {"text": "phần chưa khớp chuyển thành lệnh giới hạn", "at": [7, "nhưng"], "sm": True}],
     "srcnote": SRC_RULE + ", Điều 17"},
    clock(8, "Mười", now={2, 3}),
    {"type": "kinetic", "at": 9, "items": [{"text": "TRONG KHỚP LIÊN TỤC: SỬA GIÁ · SỬA SỐ LƯỢNG · HUỶ", "at": [9, "Trong"], "sm": True},
                                          {"text": "SỬA GIÁ / TĂNG SỐ LƯỢNG", "at": [10, "Nhưng"]},
                                          {"text": "→ XẾP LẠI CUỐI HÀNG", "at": [10, "xếp"], "acc": True},
                                          {"text": "giảm số lượng → giữ chỗ", "at": [10, "xếp", 0, 0.5], "sm": True}],
     "srcnote": SRC_RULE + ", Điều 21 · thông báo HOSE 13/03/2025"},
    {"type": "date", "at": 11, "day": "QUAY LẠI THỨ HAI", "date": "09.03.2026"},
    {"type": "book", "at": 12, "title": "HÀNG ĐỢI Ở GIÁ SÀN", "range": "THAM CHIẾU 20.000 · SÀN 18.600", **BAND,
     "queue": {"price": 18600, "label": "GIÁ SÀN", "times": QUEUE, "mine": 9, "at": [12, "Khi", 0, 0.3], "until": [13, "thời"],
               "labelAt": [14, "Trên"], "hlAt": [15, "Lệnh"], "buy": {"text": "BÊN MUA Ở GIÁ SÀN: RẤT ÍT", "at": [16, "Hôm"]},
               "eat": [{"at": [16, "nhích"], "k": 2}, {"at": [16, "vẫn"], "k": 1}]},
     "source": "VÍ DỤ GIẢ ĐỊNH · MINH HOẠ THỨ TỰ ƯU TIÊN Ở GIÁ SÀN, KHÔNG PHẢI SỔ LỆNH THẬT CỦA MÃ NÀO NGÀY 09/03"},
    {"type": "question", "at": 17, "text": "Giá sàn để bảo vệ ai?\nGiữ người ta không bán được\nthì có ích gì?"},
    {"type": "kinetic", "at": 18, "items": [{"text": "BIÊN ĐỘ KHÔNG CHẶN GIẢM GIÁ", "at": [18, "Biên"]},
                                           {"text": "NÓ GIỚI HẠN MỖI NGÀY GIÁ ĐI BAO XA", "at": [18, "Nó"], "acc": True},
                                           {"text": "và cho mọi người một đêm để đọc thêm thông tin", "at": [19, "Hết"], "sm": True}]},
    {"type": "broll", "at": 20, "vid": "5699953", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "MẶT TRÁI", "at": [20, "Mặt"]},
             {"text": "XẾP SAU RẤT NHIỀU NGƯỜI", "at": [20, "xếp"], "acc": True},
             {"text": "hết ngày vẫn chưa tới lượt", "at": [20, "hết"], "sm": True}]},
    {"type": "kinetic", "at": 21, "items": [{"text": "GIỜ BẠN ĐÃ HIỂU VÌ SAO", "at": [21, "Giờ"]}]},
    {"type": "slam", "at": [21, "muốn"], "text": "MUỐN BÁN ≠ BÁN ĐƯỢC", "sub": "KHI KHÔNG CÒN NGƯỜI MUA Ở GIÁ SÀN"},
    {"type": "kinetic", "at": 22, "items": [{"text": "PHIÊN CHƯA HẾT", "at": [22, "Nhưng"]},
                                           {"text": "15 PHÚT QUYẾT ĐỊNH GIÁ SÁNG HÔM SAU", "at": [22, "Còn"], "acc": True}]},
]}

# ---------------- CH04 · Hai giờ rưỡi: chốt giá, và ngày hôm sau ----------------
SRC_VNI = "DỮ LIỆU: VN-INDEX (VNSTOCK/VCI) · KÊNH TỰ TÍNH · NHÌN LẠI, KHÔNG AI BIẾT TRƯỚC · KHÔNG PHẢI KHUYẾN NGHỊ"
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "14:30 · CHỐT GIÁ, VÀ NGÀY HÔM SAU"}, "bgm": {"mood": "warm", "gain": 0.13}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "HAI GIỜ RƯỠI:\nCHỐT GIÁ", "sub": "VÀ NGÀY HÔM SAU · ATC",
     "vid": "9160920", "illus": ILL, "titleAt": [0, "Hai"]},
    clock(0, "Đây", now={4}),
    {"type": "kinetic", "at": 1, "items": [{"text": "14:45 · GIÁ ĐÓNG CỬA", "at": [1, "Đúng"]},
                                          {"text": "LUẬT: KHỚP ĐƯỢC NHIỀU NHẤT", "at": [1, "luật"], "sm": True},
                                          {"text": "ATC CŨNG KHÔNG CHEN TRƯỚC LỆNH TRẦN, SÀN ĐẶT TRƯỚC", "at": [2, "Lệnh"], "acc": True}],
     "srcnote": SRC_RULE + ", Điều 17, 20 · giờ: tài liệu thành viên (05/2025)"},
    {"type": "kinetic", "at": 3, "items": [{"text": "GIÁ ĐÓNG CỬA = GIÁ THAM CHIẾU NGÀY MAI", "at": [3, "Giá"], "acc": True},
                                          {"text": "LỆNH CHƯA KHỚP → HẾT HIỆU LỰC", "at": [4, "Lệnh"]},
                                          {"text": "sáng mai muốn mua bán tiếp phải đặt lại", "at": [4, "Muốn"], "sm": True},
                                          {"text": "14:45 – 15:00 · CHỈ CÒN THOẢ THUẬN", "at": [5, "Từ"]}],
     "srcnote": SRC_RULE + ", Điều 31 · giờ: tài liệu thành viên (05/2025)"},
    {"type": "candles", "at": 6, "series": "vnindex", "from": "2026-02-23", "to": "2026-04-03", "drawAt": [6, "Vậy"],
     "until": [6, "khép"], "title": "VN-INDEX · 09/03/2026 KHÉP LẠI", "range": "02/2026 – 04/2026", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2026-03-09", "text": "ĐÓNG CỬA 1.652,79 · ĐÁY PHIÊN 1.650,75", "pos": "below", "tone": "down",
                "at": [7, "gần"], "dx": 60, "dy": 20}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "SÁNG THỨ BA", "at": [8, "Sáng"], "sm": True},
                                          {"text": "THAM CHIẾU MỚI = GIÁ SÀN HÔM TRƯỚC", "at": [8, "giá"], "acc": True},
                                          {"text": "KHUNG ±7% TÍNH TỪ ĐÓ", "at": [8, "Khung"]}],
     "srcnote": SRC_RULE + ", Điều 31"},
    {"type": "ledger", "at": 9, "title": "SAU NGÀY 09/03 · VN-INDEX", "rows": [
        {"k": "10/03 · THỨ BA", "v": "+1,45%", "at": [9, "thứ"]},
        {"k": "11/03 · THỨ TƯ", "v": "+3,08%", "at": [9, "thứ", 1]}],
     "total": {"k": "LẤY LẠI", "v": "≈ 2/3 SỐ ĐIỂM ĐÃ MẤT", "at": [10, "Tới"]},
     "srcnote": "Giá đóng cửa VN-Index (vnstock/VCI) · kênh tự tính · nhìn lại, không ai biết trước"},
    {"type": "question", "at": 11, "text": "Vậy ai bán hôm thứ Hai\nlà bán hớ rồi?"},
    {"type": "candles", "at": 12, "series": "vnindex", "from": "2026-02-23", "to": "2026-04-03", "drawAt": [12, "Nhìn"],
     "until": [12, "dễ"], "title": "VN-INDEX · NHÌN LẠI", "range": "02/2026 – 04/2026", "ind": [], "source": SRC_VNI,
     "marks": [{"date": "2026-03-11", "text": "11/03: 1.728,34 · LẤY LẠI ≈ 2/3", "pos": "above", "tone": "up",
                "at": [12, "Nhìn"], "dx": 300, "dy": -120},
               {"date": "2026-03-23", "text": "23/03: 1.591,17 · THẤP HƠN 09/03 ≈ 62 ĐIỂM", "pos": "below", "tone": "down",
                "at": [13, "thấp"], "dx": 40, "dy": 10}]},
    {"type": "slam", "at": 14, "text": "KHÔNG AI BIẾT TRƯỚC NGÀY MAI", "hitAt": [14, "Không"]},
    {"type": "kinetic", "at": 15, "items": [{"text": "VIDEO KHÔNG CHẤM ĐÚNG SAI", "at": [15, "Video"]},
                                           {"text": "CHO NGƯỜI BÁN HAY NGƯỜI GIỮ", "at": [15, "người"], "sm": True},
                                           {"text": "CHỈ CHO THẤY CHỢ VẬN HÀNH RA SAO", "at": [15, "Nó"], "acc": True}]},
]}

# ---------------- CH05 · Sau tiếng chuông: hai ngày chờ, và tiền phí ----------------
SRC_VSD = "VSD, thông báo hiệu lực 29/08/2022 (qua báo LSVN, VnBusiness)"
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "T+2 · HAI NGÀY CHỜ, VÀ TIỀN PHÍ"}, "bgm": {"mood": "upbeat", "gain": 0.15}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "SAU TIẾNG CHUÔNG:\nHAI NGÀY CHỜ", "sub": "VÀ TIỀN PHÍ · T+2",
     "titleAt": [0, "Giờ"]},
    clock(1, "Ở", now={7}),
    {"type": "kinetic", "at": 2, "items": [{"text": "CHU KỲ THANH TOÁN", "at": [2, "Chu"], "sm": True},
                                          {"text": "T+2", "at": [2, "hai"], "acc": True},
                                          {"text": "T = NGÀY KHỚP · +2 NGÀY LÀM VIỆC MỚI ĐỔI CHỦ", "at": [3, "T"]}],
     "srcnote": "Chu kỳ thanh toán cổ phiếu T+2: tài liệu thành viên tóm tắt quy định HOSE (05/2025)"},
    {"type": "kinetic", "at": 4, "items": [{"text": "TỪ 29/08/2022", "at": [4, "Từ"], "sm": True},
                                          {"text": "CỔ PHIẾU VỀ TÀI KHOẢN TRƯỚC 13:00 NGÀY T+2", "at": [4, "cổ"]},
                                          {"text": "→ BÁN ĐƯỢC TỪ PHIÊN CHIỀU", "at": [4, "bán"], "acc": True}],
     "srcnote": SRC_VSD},
    {"type": "timeline", "at": 5, "tag": {"text": "TUẦN 05–10/03/2026 · VÍ DỤ GIẢ ĐỊNH", "at": [5, "Áp"]}, "items": [
        {"year": "05/03", "text": "THỨ NĂM · NGƯỜI A MUA", "at": [6, "Ai"]},
        {"year": "06/03", "text": "THỨ SÁU · NGƯỜI B MUA", "at": [8, "Ai"]},
        {"year": "09/03", "text": "THỨ HAI · A BÁN ĐƯỢC TỪ CHIỀU, XẾP SAU LỆNH ĐẶT TỪ SÁNG", "at": [6, "Chiều"], "color": CYAN},
        {"year": "10/03", "text": "THỨ BA · B MỚI BÁN ĐƯỢC TỪ CHIỀU", "at": [8, "chiều"], "color": GOLD}],
     "srcnote": "Lịch T+2 theo ngày làm việc · 05–10/03/2026 đều có phiên · cổ phiếu về trước 13:00 ngày T+2 (VSD)"},
    {"type": "question", "at": 10, "text": "Mua sáng bán chiều,\nnhư ở nhiều nước khác, thì sao?"},
    {"type": "kinetic", "at": 11, "items": [{"text": "GIAO DỊCH TRONG NGÀY (T+0)", "at": [11, "Cái"]},
                                           {"text": "đã có điều khoản: Thông tư 120/2020, Điều 10", "at": [12, "Quy"], "sm": True},
                                           {"text": "T+0 · BÁN CHỜ VỀ: CHƯA TRIỂN KHAI (10/2026)", "at": [12, "chưa"], "acc": True}],
     "srcnote": "UBCKNN (ssc.gov.vn), 2026 · TT 120/2020/TT-BTC"},
    {"type": "kinetic", "at": 13, "items": [{"text": "CƠ CHẾ BÙ TRỪ MỚI (CCP)", "at": [13, "Cơ"]},
                                           {"text": "DỰ KIẾN QUÝ I/2027", "at": [13, "quý"], "acc": True},
                                           {"text": "KHÔNG ĐỒNG NGHĨA CÓ NGAY T+0", "at": [14, "Nhưng"]},
                                           {"text": "khi nào có: UBCKNN quyết định theo tình hình thị trường", "at": [15, "Khi"], "sm": True}],
     "srcnote": "UBCKNN (ssc.gov.vn) — bản tiếp thu, giải trình dự thảo thông tư thay TT 119/2020, 2026"},
    {"type": "kinetic", "at": 16, "items": [{"text": "CHIỀU BÁN CŨNG VẬY", "at": [16, "Chiều"], "sm": True},
                                           {"text": "TIỀN BÁN VỀ SAU 2 NGÀY LÀM VIỆC", "at": [16, "tiền"], "acc": True},
                                           {"text": "ví dụ: bán 09/03 → tiền về 11/03", "at": [16, "hai"], "sm": True}],
     "srcnote": "Chu kỳ thanh toán T+2 · lịch tính theo ngày làm việc"},
    {"type": "ledger", "at": 17, "title": "MỖI LẦN MUA / BÁN", "rows": [
        {"k": "PHÍ MÔI GIỚI · MỖI CHIỀU", "v": "TỐI ĐA 0,45%", "at": [18, "Mỗi"]},
        {"k": "→ THỰC TẾ", "v": "THƯỜNG THẤP HƠN", "at": [18, "thực"]},
        {"k": "THUẾ TNCN · MỖI LẦN BÁN", "v": "0,1% GIÁ BÁN", "at": [19, "Mỗi"]},
        {"k": "→ KỂ CẢ KHI", "v": "BÁN LỖ", "at": [19, "kể"]}],
     "srcnote": "Phí: TT 102/2021/TT-BTC · thuế: Luật Thuế TNCN 109/2025/QH15, Điều 13"},
    {"type": "quote", "at": 20, "qline": 21, "lbl": "NGUYÊN VĂN",
     "text": "Thuế thu nhập cá nhân đối với thu nhập từ chuyển nhượng chứng khoán được xác định bằng giá chuyển nhượng nhân (x) với thuế suất 0,1% theo từng lần chuyển nhượng.",
     "by": "Luật Thuế TNCN số 109/2025/QH15, Điều 13 khoản 2 (hiệu lực 01/07/2026)"},
    {"type": "ledger", "at": 22, "title": "MỘT LÔ · GIẢ ĐỊNH PHÍ 0,15%/CHIỀU", "rows": [
        {"k": "MUA 100 × 20.000 + PHÍ", "v": "2.003.000 Đ", "at": [23, "Mua"]},
        {"k": "BÁN 20.000", "v": "−8.000 Đ", "at": [23, "bạn"]},
        {"k": "BÁN 20.050 (+1 BƯỚC)", "v": "≈ −3.000 Đ", "at": [24, "Bán"]},
        {"k": "BÁN 20.100 (+2 BƯỚC)", "v": "≈ +2.000 Đ", "at": [25, "Phải"]}],
     "srcnote": "Ví dụ giả định · phí tuỳ công ty · thuế 0,1% giá bán · kênh tự tính"},
    {"type": "kinetic", "at": 26, "items": [{"text": "+2 BƯỚC GIÁ MỚI BẮT ĐẦU CÓ LÃI", "at": [26, "Số"], "acc": True},
                                           {"text": "ví dụ giả định · phí tuỳ công ty", "at": [26, "Số", 0, 0.3], "sm": True},
                                           {"text": "LỚN DẦN THEO SỐ LẦN MUA BÁN", "at": [26, "lớn"]}]},
]}

# ---------------- CH06 · Áp dụng cho bạn, và khi nào không đúng ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "ÁP DỤNG CHO BẠN"}, "bgm": {"mood": "curious", "gain": 0.16}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "ÁP DỤNG CHO BẠN —\nVÀ KHI NÀO KHÔNG ĐÚNG",
     "sub": "KHÔNG PHẢI LỜI KHUYÊN MUA HAY BÁN", "titleAt": [0, "Mình"]},
    {"type": "ledger", "at": 1, "title": "5 CÂU TRƯỚC LỆNH ĐẦU TIÊN", "rows": [
        {"k": "01", "v": "THAM CHIẾU · TRẦN · SÀN HÔM NAY?", "at": [2, "Một"]},
        {"k": "02", "v": "ĐÚNG LÔ, BƯỚC GIÁ? KHÔNG KHỚP THÌ SAO?", "at": [3, "Hai"]},
        {"k": "03", "v": "PHIÊN NÀO? CÒN SỬA, HUỶ ĐƯỢC KHÔNG?", "at": [4, "Ba"]},
        {"k": "04", "v": "CÓ CẦN TIỀN NÀY TRONG VÀI NGÀY?", "at": [5, "Bốn"]},
        {"k": "05", "v": "PHÍ + THUẾ: MẤY BƯỚC MỚI HOÀ VỐN?", "at": [6, "Năm"]}]},
    {"type": "ledger", "at": 7, "title": "BIÊN ĐỘ MỖI NGÀY · KHI NÀO KHÁC", "rows": [
        {"k": "HOSE", "v": "±7%", "at": [8, "Biên"]},
        {"k": "HNX (TỚI 23/12/2026)", "v": "±10%", "at": [8, "Sàn"]},
        {"k": "UPCOM", "v": "±15%", "at": [8, "sàn", 1]},
        {"k": "NGÀY ĐẦU · SAU NGỪNG ≥ 25 PHIÊN", "v": "±20%", "at": [9, "Ngày"]}],
     "srcnote": "HOSE ±7%, ±20%: tài liệu thành viên (05/2025) · HNX, UPCoM: tổng hợp (Thư viện Pháp luật)"},
    {"type": "kinetic", "at": 10, "items": [{"text": "CỔ PHIẾU BỊ HẠN CHẾ: KHỚP ĐỊNH KỲ 15 PHÚT", "at": [10, "Cổ"]},
                                           {"text": "TỔ CHỨC NƯỚC NGOÀI", "at": [11, "Nhà"], "sm": True},
                                           {"text": "CÓ THỂ MUA KHÔNG CẦN ĐỦ TIỀN TRƯỚC", "at": [11, "có"], "acc": True}],
     "srcnote": "Thông báo HOSE 13/03/2025 · TT 68/2024/TT-BTC (NPF)"},
    {"type": "kinetic", "at": 12, "items": [{"text": "QUY ĐỊNH ĐANG ĐỔI", "at": [12, "Và"], "acc": True},
                                           {"text": "TT 145/2026 · HIỆU LỰC 16/11/2026", "at": [13, "Một"]},
                                           {"text": "CỔ PHIẾU NIÊM YẾT HNX → HOSE TỪ 28/12/2026 (DỰ KIẾN)", "at": [14, "Cuối"]},
                                           {"text": "kiểm lại quy định hiện hành trước khi đặt lệnh", "at": [15, "Nên"], "sm": True}],
     "srcnote": "TT 145/2026/TT-BTC (chinhphu.vn) · TT 139/2025/TT-BTC (Thời báo Tài chính, 30/09/2026)"},
    clock(16, "Tóm", seq=[[16, "Tóm", 0, round(0.1 + 0.25 * k, 2)] for k in range(7)] + [[17, "hai"]], tag="ĐỒNG HỒ PHIÊN · TRỌN VẸN"),
    {"type": "kinetic", "at": 18, "items": [{"text": "09/03/2026", "at": [18, "Hôm"], "sm": True},
                                           {"text": "NHIỀU NGƯỜI KHÔNG BÁN ĐƯỢC ĐÚNG LÚC", "at": [18, "những"]},
                                           {"text": "NHƯNG MỖI NGÀY CHỈ RƠI TỐI ĐA 7%", "at": [19, "Cũng"], "acc": True}]},
    {"type": "slam", "at": 20, "text": "HIỂU LUẬT CHƠI TRƯỚC", "hitAt": [20, "Hiểu"], "sub": "TRƯỚC KHI BẤM NÚT"},
    {"type": "broll", "at": 21, "vid": "3191576", "ms": 10, "veil": 0.55, "illus": ILL,
     "kin": [{"text": "BÀI 3", "at": [21, "Bài"], "sm": True},
             {"text": "ĐỌC BIỂU ĐỒ ĐẦU TIÊN", "at": [21, "đọc"]},
             {"text": "ĐƯỜNG · CỘT · NẾN", "at": [21, "đường"], "acc": True}]},
    {"type": "question", "at": 22, "text": "Lần đầu đặt lệnh, điều gì\nlàm bạn bất ngờ nhất?\nLô 100 cổ phiếu, bước giá,\nhay hai ngày chờ?"},
]}

TITLE = "Vì Sao Có Ngày Muốn Bán Cổ Phiếu Mà Không Bán Được? Một Phiên HOSE Từ 9 Giờ Tới 15 Giờ"
DISCLAIMER = ("Nội dung giáo dục, không phải tư vấn đầu tư hay tư vấn tài chính cá nhân. Không khuyến nghị mua/bán bất kỳ "
              "tài sản nào. Ví dụ dùng dữ liệu quá khứ; quá khứ không đảm bảo tương lai. Nội dung do kênh biên soạn từ nguồn "
              "công khai; giọng đọc tổng hợp. Quy định mô tả theo thời điểm làm video (10/2026) và có thể thay đổi.")
METHOD = ("📐 CÁCH TÍNH (kênh tự tính, giá đóng cửa đã điều chỉnh, truy xuất qua vnstock/VCI): VN-Index 06/03 → 09/03/2026: "
          "1.767,84 → 1.652,79 (−115,05 điểm, −6,51%), đáy phiên 1.650,75; 10/03 +1,45%, 11/03 +3,08% (lấy lại ≈ 65,7% số điểm "
          "mất); 23/03 đóng 1.591,17. Ô màu ngày 09/03: 395 cổ phiếu HOSE có phiên ngày đó, so với phiên trước của chính mã "
          "(giảm 368 · tăng 11 · đứng 16, trung vị −6,80%). Số mã giảm sàn (233) theo báo Nhân Dân, không tự đếm. Giá trung vị "
          "406 cổ phiếu HOSE (giá đóng cửa gần nhất tới 30/09/2026): 15.400 đ; bước giá 10/50/100 đ: 126/234/46 mã. Sổ lệnh, "
          "giá 20.000 đ, phí 0,15%/chiều là ví dụ giả định để minh hoạ cơ chế.")
SPEC = {
    "title": TITLE, "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO",
    "acc": ["hose", "vn-index", "ato", "atc", "krx", "sàn", "trần", "khớp", "phí", "thuế"],
    "say": SAY, "imgs": {}, "chapters": list(CH),
    "youtube": {
        "titles": [TITLE, "Ngày VN-Index Mất 115 Điểm: Một Phiên Giao Dịch HOSE Vận Hành Thế Nào?",
                   "Giá Trần, Giá Sàn, ATO, ATC, T+2: Đi Hết Một Phiên Chứng Khoán Cùng Người Mới"],
        "summary": "Chiều thứ Hai 09/03/2026, VN-Index mất 115 điểm, 233 mã trên HOSE nằm sàn, và hết phiên vẫn còn hàng triệu cổ "
                   "phiếu chờ bán ở giá sàn mà không còn ai đặt mua ở giá ấy. Bài 2 khoá Chứng khoán từ số 0 đi cùng một phiên HOSE "
                   "từ 9 giờ tới 15 giờ: một lệnh gồm những gì, lô và bước giá, giá tham chiếu – trần – sàn, phiên ATO chọn giá thế "
                   "nào, khớp liên tục và hàng đợi ở giá sàn, phiên ATC, rồi hai ngày chờ T+2 và tiền phí, thuế. Dữ liệu thật, ví dụ "
                   "giả định, giải thích dễ hiểu.",
        "more": [DISCLAIMER, METHOD],
        "chapter_titles": {"ch00": "Mở đầu: thứ Hai, chín tháng ba", "ch01": "Trước chín giờ: một lệnh gồm những gì",
                           "ch02": "Chín giờ: phiên mở cửa, một cái giá cho tất cả",
                           "ch03": "Chín giờ mười lăm: khớp liên tục, và hàng đợi ở giá sàn",
                           "ch04": "Hai giờ rưỡi: chốt giá, và ngày hôm sau", "ch05": "Sau tiếng chuông: hai ngày chờ, và tiền phí",
                           "ch06": "Áp dụng cho bạn, và khi nào không đúng"},
        "sources": [
            "VNX — Quy chế Niêm yết và giao dịch chứng khoán niêm yết (QĐ 22/QĐ-HĐTV ngày 18/04/2025): https://luatvietnam.vn/chung-khoan/quyet-dinh-22-qd-hdtv-2025-ban-hanh-quy-che-niem-yet-va-giao-dich-chung-khoan-399805-d1.html",
            "UBCKNN — Bản tiếp thu, giải trình dự thảo Thông tư thay TT 119/2020 (CCP, T+0, bán chứng khoán chờ về): https://ssc.gov.vn/cs/idcplg?IdcService=GET_FILE&allowInterrupt=1&dDocName=APPSSCGOVVN1620170388&dID=180856&filename=Ban+tiep+thu+giai+trinh+y+kien.pdf",
            "Cổng chinhphu.vn — Thông tư 145/2026/TT-BTC (hiệu lực 16/11/2026): https://xaydungchinhsach.chinhphu.vn/mot-so-noi-dung-chinh-cua-thong-tu-145-2026-tt-btc-quy-dinh-hoat-dong-dang-ky-luu-ky-bu-tru-va-thanh-toan-giao-dich-chung-khoan-119261005165752419.htm",
            "Luật Thuế thu nhập cá nhân số 109/2025/QH15, Điều 13: https://thuvienphapluat.vn/van-ban/thue-phi-le-phi/Luat-Thue-thu-nhap-ca-nhan-2025-so-109-2025-QH15-665870.aspx",
            "Thông tư 102/2021/TT-BTC (giá dịch vụ môi giới tối đa 0,45%): https://luatvietnam.vn/chung-khoan/thong-tu-102-2021-tt-btc-213084-d1.html",
            "Dữ liệu kênh tự tính — giá đóng cửa HOSE và VN-Index qua Vnstock (nguồn VCI): https://vnstocks.com/docs/vnstock-data/du-lieu-giao-dich",
            "Nhân Dân 09/03/2026 — Hơn 230 cổ phiếu \"xanh lơ\", VN-Index giảm kỷ lục: https://nhandan.vn/ocop/chung-khoan-ngay-93-hon-230-co-phieu-xanh-lo-vn-index-giam-ky-luc-post947238.html",
            "Thời báo Tài chính 09/03/2026 — Áp lực bán hoàn toàn áp đảo: https://thoibaotaichinhvietnam.vn/chung-khoan-ngay-93-ap-luc-ban-hoan-toan-ap-dao-vn-index-giam-diem-manh-193376.html",
            "Mekong ASEAN 09/03/2026 — Gần 350 mã chứng khoán giảm sàn: https://mekongasean.vn/ga-n-350-ma-chung-khoan-gia-m-sa-n-nhom-da-u-khi-cung-quay-xe-52517.html",
            "Thời báo Tài chính 30/09/2026 — Chuyển toàn bộ cổ phiếu niêm yết về HOSE (TT 139/2025/TT-BTC): https://thoibaotaichinhvietnam.vn/chot-thoi-diem-chuyen-toan-bo-co-phieu-niem-yet-ve-hose-204623.html",
            "LSVN 29/08/2022 — Bán cổ phiếu từ phiên chiều T+2 (thông báo VSD): https://lsvn.vn/nha-dau-tu-duoc-ban-co-phieu-nhan-tien-som-hon-1-ngay1661739512-a123157.html",
            "LSVN 15/02/2021 — Giao dịch trong ngày, TT 120/2020/TT-BTC Điều 10: https://lsvn.vn/nguyen-tac-hoat-dong-giao-dich-chung-khoan-trong-ngay1613406397-a100508.html",
            "Vietstock 13/03/2025 — HOSE thông tin quy định giao dịch của hệ thống mới: https://vietstock.vn/2025/03/hose-thong-tin-ve-quy-dinh-giao-dich-cua-he-thong-moi-143-1281145.htm",
            "Báo Chính phủ 05/05/2025 — Ngày đầu vận hành KRX: https://baochinhphu.vn/ngay-dau-van-hanh-krx-thuan-loi-vung-nen-tang-mo-tuong-lai-102250505193825737.htm",
            "Giờ giao dịch, bước giá, lô, ±20%: tài liệu của công ty chứng khoán thành viên tóm tắt quy định HOSE dưới KRX (05/2025)",
            "Biên độ HNX ±10%, UPCoM ±15% — Thư viện Pháp luật: https://thuvienphapluat.vn/phap-luat-doanh-nghiep/cau-hoi-thuong-gap/bien-do-dao-dong-gia-co-phieu-tai-san-hose-hnx-upcom-4008.html",
            "Caixin Global 09/03/2026 — Asia stocks dive as oil spikes on Iran crisis: https://www.caixinglobal.com/2026-03-09/asia-stocks-dive-as-oil-spikes-on-iran-crisis-102421276.html",
            "Tổng cục Thống kê (NSO) — thu nhập bình quân lao động quý I/2026 (9,0 triệu đồng/tháng)",
        ],
        "hashtags": ["ChứngKhoán", "HOSE", "ChứngKhoánTừSố0", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["chứng khoán cho người mới", "chứng khoán từ số 0", "phiên giao dịch HOSE", "giá trần giá sàn", "ATO ATC là gì",
                 "khớp lệnh liên tục", "lệnh giới hạn LO", "lô chẵn lô lẻ", "bước giá", "T+2 là gì", "giao dịch T+0",
                 "VN-Index 9/3/2026", "phí giao dịch chứng khoán", "thuế bán chứng khoán 0,1%", "tài chính cá nhân"],
        "category": "27",
        "data_credit": "📊 DỮ LIỆU BIỂU ĐỒ: VN-Index và giá đóng cửa cổ phiếu trên HOSE, truy xuất qua Vnstock (nguồn VCI); số mã "
                       "tăng/giảm/giảm sàn ngày 09/03/2026 theo báo Nhân Dân; số liệu tổng hợp do kênh tự tính. Sổ lệnh và các ví "
                       "dụ giá là giả định.",
        "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels"],
    },
}

if __name__ == "__main__":
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec + %d chương, %d cảnh" % (len(CH), sum(len(c["scenes"]) for c in CH.values())))
