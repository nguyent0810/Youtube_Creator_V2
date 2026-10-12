"""Sinh spec.json + scenes/hud/bgm cho video dài CK D1 "Xếp hàng mua vàng có phải là đỉnh? Đọc lại 11 đợt đổ xô (2011–2026)
bằng dữ liệu" (chuỗi Tâm lý tiền bạc · D1; kênh Biểu Đồ Biết Nói, theme "chart").

    python data/long/ck-d1-vang-dinh/gen_scenes.py     # giữ nguyên "lines" + "title" trong chNN.json (script_lines ghi)

Dữ kiện + nguồn: docs/channels/chung-khoan/2026-10-07-long-d1-research.md; kiểm chứng: factcheck.md (cùng thư mục) — chữ trên
màn hình theo mục 1c "Chữ và cảnh trên màn hình" (đã sửa: 2 CHỈ, "không còn hiện tượng…", "cao bất thường", "trên 4 chỉ", …).
Biểu đồ vàng: cảnh race key "sjc" (motion/long/chartdata.attach_race; điểm 30/09/2026 sửa theo data/ck/sjc_overrides.csv) —
CHỈ dùng khi hai đầu mút là điểm có thật trong CSV (04/06/2024 → 03/06/2025, 29/01 → 30/09/2026). Mọi biểu đồ/số vàng tự tính
ghi NOTE (race: "source"; cảnh khác: "srcnote" -> dòng nhỏ góc dưới phải, casewide.js common()).
Luật kênh: chỉ giáo dục, không khuyến nghị mua/bán/giữ, không dự báo; không tên tiệm vàng/ngân hàng ngoài SJC (thước đo giá);
không chế giễu người mua ngày vía. Clip: Pexels (ngang), mọi b-roll ghi "VIDEO MINH HỌA"; cảnh hàng người là cảnh chung.
Neo: chữ ĐẦU TIÊN của mỗi cảnh neo vào từ ĐẦU câu (retro: neo cuối câu -> 1–3 s màn trống).
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

UP, DN, GOLD, BLUE, ORANGE = "#4ade80", "#f87171", "#fbbf24", "#38bdf8", "#f97316"
ILL = "VIDEO MINH HỌA"
ILLQ = "VIDEO MINH HỌA, KHÔNG PHẢI CẢNH Ở VIỆT NAM"     # b-roll hàng người: cảnh chung, không phải ngày 29/01
NOTE = "Tính từ dữ liệu giá niêm yết SJC (kênh tự tính). Minh hoạ quá khứ, không phải khuyến nghị."

# Bảng đọc: giữ các mục C1 (đổi bảng = đổi khoá cache TTS) + tên riêng của D1.
SAY = {"vn-index": "Vi En In-đéc", "hose": "hô-dê", "vic": "vi ai xi", "vhm": "vi hát em", "vre": "vi rờ e", "vpl": "vi pê en",
       "ree": "rê ê ê", "sam": "xam", "gdp": "gi đi pi", "etf": "i ti ép", "hnx": "hát en ích", "upcom": "úp-com",
       "margin": "ma-gin", "app": "áp", "vingroup": "Vin-grúp", "vietnambiz": "Việt Nam Biz", "sjc": "ét giây xi",
       "fomo": "phô-mô", "vnexpress": "Vi En Ếch-prét", "tversky": "Tvéc-xki", "kahneman": "Ca-nơ-men", "barber": "Ba-bơ",
       "odean": "Âu-đin", "greenwood": "Grin-gút", "shleifer": "Sờ-lai-phơ", "zalo": "Da-lô"}

RACE_2026 = {"from": "2026-01-29", "to": "2026-09-30",
             "series": [{"key": "sjc", "label": "MUA 29/01", "color": GOLD}], "source": NOTE}

CH = {}

# ---------------- CH00 · Hai mươi chín tháng một (cold open → "không hẳn" → 3 câu hỏi → nhận diện kênh) ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HÀNG DÀI VÀ ĐỈNH GIÁ"}, "bgm": {"mood": "mystery", "gain": 0.07}, "scenes": [
    {"type": "date", "vid": "6229548", "illus": ILLQ, "day": "3–4 GIỜ SÁNG · PHỐ TRẦN NHÂN TÔNG, HÀ NỘI", "date": "29.01.2026",
     "sub": {"text": "VIDEO GIÁO DỤC · KHÔNG PHẢI LỜI KHUYÊN MUA, BÁN VÀNG", "at": [0, "Ba,"]}},
    {"type": "broll", "at": 1, "vid": "8849053", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "CÓ TIỆM: HẾT HÀNG", "at": [1, "Có"]},
             {"text": "CÓ NƠI TRÊN 4 CHỈ: LẤY PHIẾU HẸN", "at": [1, "Có", 1], "acc": True}]},
    {"type": "counter", "at": 2, "from": 152800000, "to": 191300000, "suffix": " đ", "countAt": [2, "Một"], "until": [2, "đồng"],
     "label": "GIÁ BÁN RA SJC · 13:25 · 29/01/2026", "sub": {"text": "CAO NHẤT LỊCH SỬ · TÍNH TỚI LÚC LÀM VIDEO", "at": [3, "Đó"]},
     "srcnote": "Từ 152,8 triệu ngày 01/01/2026 · giá báo chí (webgia, Công Luận)"},
    {"type": "race", "at": 4, **RACE_2026, "title": "MUA VÀNG MIẾNG NGÀY 29/01/2026", "range": "29/01 → 30/09/2026 · BÁN LẠI CHO TIỆM",
     "drawAt": [4, "Đầu"], "until": [4, "nhận"]},
    {"type": "slam", "at": 5, "text": "≈ −51 TRIỆU / LƯỢNG", "hitAt": [5, "Mất"],
     "sub": "BÁN LẠI ĐẦU THÁNG 10 (GIÁ MUA VÀO 140,5) · HƠN 1/4 SỐ TIỀN"},
    {"type": "question", "at": 6, "text": "Cứ thấy xếp hàng mua vàng\nlà giá sắp đỉnh?"},
    {"type": "kinetic", "at": 7, "items": [{"text": "NGHE RẤT HỢP LÝ", "at": [7, "Nghe"]},
                                          {"text": "NHƯNG ĐỌC LẠI BÁO CHÍ 15 NĂM QUA…", "at": [7, "Nhưng"], "sm": True}]},
    {"type": "slam", "at": [7, "không"], "text": "KHÔNG HẲN", "sub": "VÀ CHỖ \"KHÔNG HẲN\" ẤY MỚI ĐÁNG HỌC"},
    {"type": "question", "at": 9, "text": "11 lần đổ xô mua vàng.\nBao nhiêu lần\nrơi đúng vùng đỉnh?"},
    {"type": "ledger", "at": 10, "title": "THỬ ĐOÁN TRƯỚC", "rows": [
        {"k": "?", "v": "SỐ LẦN RƠI ĐÚNG VÙNG ĐỈNH · ĐÁP ÁN Ở CHƯƠNG 1", "at": [10, "Giữ"]},
        {"k": "02", "v": "VÌ SAO AI CŨNG MUỐN XẾP HÀNG?", "at": [11, "Rồi"]},
        {"k": "03", "v": "TRẢ THÊM GÌ? 5 CÂU TỰ KIỂM", "at": [12, "Và"]}]},
    {"type": "brand", "at": 13, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 14, "items": [{"text": "TÂM LÝ TIỀN BẠC · BÀI 1", "at": [14, "Video"], "acc": True},
                                           {"text": "chỉ nhằm giáo dục · không phải lời khuyên mua hay bán vàng",
                                            "at": [14, "Video"], "sm": True}]},
]}

# ---------------- CH01 · Mười một lần xếp hàng: bảng điểm ----------------
# 11 đợt (hồ sơ 1.1): A 08/2011 · B 07–08/2020 · C 19/02/2024 · D 04/06/2024 · E 07/02/2025 · F 22/04/2025 · G 06/09/2025 ·
# H 29/01/2026 · I 26/02/2026 · J 02/03/2026 · K 21/03/2026. Vùng đỉnh: A B H J · giá còn lên: C–G · lỗ, không phải đỉnh: I K.
WAVES = [("2011", "23/08", DN, "ĐỈNH"), ("2020", "07–08", DN, "ĐỈNH"), ("2024", "VÍA THẦN TÀI", UP, "CÒN LÊN"),
         ("2024", "04/06 · NGÂN HÀNG", UP, "CÒN LÊN"), ("2025", "VÍA THẦN TÀI", UP, "CÒN LÊN"), ("2025", "22/04", UP, "CÒN LÊN"),
         ("2025", "06/09", UP, "CÒN LÊN"), ("2026", "29/01", DN, "ĐỈNH"), ("2026", "VÍA THẦN TÀI", ORANGE, "LỖ"),
         ("2026", "02/03", DN, "ĐỈNH"), ("2026", "21/03", ORANGE, "LỖ")]


def _waves(colored: bool, line: int, word: str):
    out = []
    for k, (yr, tx, col, res) in enumerate(WAVES):
        short = "VÍA" if "VÍA" in tx else tx.split(" · ")[0]
        q = {"year": yr, "text": f"{short} · {res}" if colored else tx,
             "at": [line, word, 0, round(0.22 * k, 2)]}
        if colored:
            q["color"] = col
        out.append(q)
    return out


CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MƯỜI MỘT LẦN XẾP HÀNG: BẢNG ĐIỂM"}, "bgm": {"mood": "curious", "gain": 0.09}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MƯỜI MỘT LẦN XẾP HÀNG:\nBẢNG ĐIỂM", "sub": "11 ĐỢT ĐỔ XÔ MUA VÀNG · 2011 — 2026",
     "vid": "8733007", "illus": ILL, "titleAt": [0, "Kênh"]},
    {"type": "timeline", "at": 1, "items": _waves(False, 1, "Câu"),
     "srcnote": "11 đợt kênh tìm được trên báo chí, có ghi ngày và giá — không phải tổng số lần xếp hàng"},
    {"type": "kinetic", "at": 2, "items": [{"text": "THÁNG 8/2011 · XẾP HÀNG Ở PHỐ VÀNG", "at": [2, "Tháng"], "sm": True},
                                          {"text": "23/08/2011 · ĐỈNH 49,12 TRIỆU", "at": [3, "Ngày"], "acc": True},
                                          {"text": "CUỐI 2013: 34,77 TRIỆU (−29%)", "at": [3, "đồng"]}],
     "srcnote": "Vàng trong nước theo báo chí (Báo Đắk Lắk, SGGP) · minh hoạ quá khứ, không phải khuyến nghị"},
    {"type": "date", "at": 4, "day": "HÀNG DÀI GIỮA TRƯA · CUỐI THÁNG 7", "date": "2020",
     "sub": {"text": "ĐỈNH 62,45 TRIỆU · ĐẦU THÁNG 8/2020", "at": [5, "Còn"]}},
    {"type": "quote", "at": 6, "qline": 6, "lbl": "NGUYÊN VĂN",
     "text": "Không còn hiện tượng đổ xô, xếp hàng mua vàng như những năm trước.",
     "by": "Người Lao Động, 09/02/2021 (nhìn lại đỉnh 08/2020)"},
    {"type": "race", "at": 7, "from": "2024-06-04", "to": "2025-06-03", "title": "VÍ DỤ: XẾP HÀNG Ở NGÂN HÀNG 04/06/2024",
     "range": "12 THÁNG SAU · GIÁ NIÊM YẾT SJC", "drawAt": [7, "Sang"], "until": [7, "kỷ"], "source": NOTE,
     "series": [{"key": "sjc", "interp": True, "label": "MUA 04/06/2024", "color": GOLD}]},
    {"type": "ledger", "at": 8, "title": "MƯỜI HAI THÁNG SAU", "rows": [
        {"k": "VÍA THẦN TÀI 2024", "v": "+11%", "at": [8, "mười"]},
        {"k": "NGÂN HÀNG 06/2024", "v": "+45%", "at": [8, "mười", 0, 0.35]},
        {"k": "VÍA THẦN TÀI 2025", "v": "+93%", "at": [8, "mười", 0, 0.7]},
        {"k": "22/04/2025", "v": "+35%", "at": [8, "mười", 0, 1.05]},
        {"k": "06/09/2025", "v": "+7%", "at": [8, "mười", 0, 1.4]}],
     "srcnote": "Mua = giá bán ra ngày xếp hàng; 12 tháng sau = giá mua vào · vài mốc từ dữ liệu SJC 2 điểm/tháng, sai số vài triệu"},
    {"type": "date", "at": 9, "day": "VÀNG MIẾNG 124 TRIỆU · CAO NHẤT TỚI KHI ĐÓ", "date": "22.04.2025",
     "sub": {"text": "CÓ NƠI CHỈ BÁN TỐI ĐA 2 CHỈ MỖI NGƯỜI", "at": [9, "có"]}},
    {"type": "counter", "at": 10, "from": 124000000, "to": 167500000, "suffix": " đ", "countAt": [10, "Ai"], "until": [10, "cao"],
     "label": "GIÁ BÁN RA 22/04/2025 → GIÁ MUA VÀO 22/04/2026", "sub": {"text": "+35% SAU 12 THÁNG", "at": [10, "ba"]},
     "srcnote": NOTE},
    {"type": "ledger", "at": 11, "title": "2026 · TỚI ĐẦU THÁNG 10", "rows": [
        {"k": "29/01", "v": "−26,6%", "at": [11, "chín"]},
        {"k": "26/02 · VÍA THẦN TÀI", "v": "−23,6%", "at": [11, "vía"]},
        {"k": "02/03", "v": "−26,4%", "at": [11, "hai", 3]},
        {"k": "21/03 · \"BẮT ĐÁY\"", "v": "−17,8%", "at": [11, "mốt"]}],
     "srcnote": "Mua = giá bán ra ngày đó (báo chí); đầu tháng 10 = giá mua vào SJC 140,5 (sáng 06/10/2026) · kênh tự tính"},
    {"type": "bars", "at": 13, "title": "11 ĐỢT ĐỔ XÔ · SAU ĐÓ GIÁ ĐI ĐÂU?", "unit": "SỐ ĐỢT · KÊNH TỰ TÍNH", "items": [
        {"k": "VÙNG ĐỈNH", "v": 4, "lbl": "4", "at": [13, "bốn"], "acc": True},
        {"k": "GIÁ CÒN LÊN", "v": 5, "lbl": "5", "at": [13, "Năm"]},
        {"k": "LỖ, KHÔNG PHẢI ĐỈNH", "v": 2, "lbl": "2", "at": [13, "Hai"]}]},
    {"type": "slam", "at": 14, "text": "HÀNG DÀI ≠ CHUÔNG BÁO ĐỈNH", "hitAt": [14, "hàng"], "sub": "THƯỜNG ĐẾN SAU MỘT CÚ TĂNG NHANH"},
    {"type": "timeline", "at": 15, "items": _waves(True, 15, "Có"),
     "srcnote": "Đỏ: vùng đỉnh · xanh: giá sau đó còn lên · cam: lỗ, dù không phải đỉnh · kênh tự tính"},
    {"type": "question", "at": 16, "text": "Sao cứ thấy đổ xô\nlà mua đúng đỉnh?"},
    {"type": "kinetic", "at": 17, "items": [{"text": "MỘT PHẦN LÝ DO: TRÍ NHỚ", "at": [17, "Mình"], "acc": True},
                                           {"text": "VNEXPRESS 2025 (Ý KIẾN BẠN ĐỌC)", "at": [18, "VnExpress"], "sm": True},
                                           {"text": "\"NỖI ÁM ẢNH\" SAU CÚ SỐC VÀNG 2011", "at": [18, "nỗi"]}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "XẾP HÀNG RỒI GIÁ LÊN TIẾP", "at": [19, "Còn"]},
                                           {"text": "ÍT AI NHẮC LẠI", "at": [19, "ít"], "acc": True}]},
    {"type": "slam", "at": 20, "text": "BẪY ĐẦU TIÊN", "sub": "CỦA BỘ NÃO"},
]}

# ---------------- CH02 · Bốn cái bẫy của bộ não ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "BỐN CÁI BẪY CỦA BỘ NÃO"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "BỐN CÁI BẪY\nCỦA BỘ NÃO", "sub": "DỄ NHỚ · SỢ BỎ LỠ · THEO ĐÁM ĐÔNG · VỪA TĂNG = SẼ TĂNG",
     "vid": "34645311", "illus": ILL, "titleAt": [0, "Bẫy"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "BẪY 1 · DỄ NHỚ ≠ THƯỜNG XẢY RA", "at": [1, "Hai"], "acc": True},
                                          {"text": "Tversky & Kahneman (1973) · lối tắt \"dễ nhớ\"", "at": [1, "Tversky"], "sm": True}]},
    {"type": "broll", "at": 2, "vid": "8846989", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "NGHE TIN HÀNG XÓM BỊ TRỘM", "at": [2, "Nghe"]},
             {"text": "CẢ TUẦN THẤY KHU PHỐ NGUY HIỂM", "at": [2, "cả"], "acc": True}]},
    {"type": "broll", "at": 3, "vid": "35888104", "veil": 0.6, "illus": ILL,
     "kin": [{"text": "Barber & Odean (2008) · dữ liệu Mỹ", "at": [3, "Nghiên"], "sm": True},
             {"text": "NHÀ ĐẦU TƯ CÁ NHÂN MUA RÒNG", "at": [3, "nhà", 1]},
             {"text": "CỔ PHIẾU \"GÂY CHÚ Ý\"", "at": [3, "gây"], "acc": True}]},
    {"type": "broll", "at": 4, "vid": "10467868", "veil": 0.55, "illus": ILLQ,
     "kin": [{"text": "NHIỀU LẦN VÀNG LẬP KỶ LỤC", "at": [4, "Nhiều"]},
             {"text": "ẢNH HÀNG DÀI LẠI LÊN BÁO", "at": [4, "ảnh"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "BẪY 2 · SỢ BỊ BỎ LỠ", "at": [5, "Bẫy"]},
                                          {"text": "FOMO", "at": [5, "FOMO"], "acc": True},
                                          {"text": "Przybylski và cộng sự, 2013 · lo người khác đang có trải nghiệm đáng giá, còn mình vắng mặt",
                                           "at": [6, "Tức"], "sm": True}]},
    {"type": "broll", "at": 7, "vid": "39494892", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "NHÓM CHAT: \"MUA ĐƯỢC HAI CHỈ RỒI\"", "at": [7, "Cả"]},
             {"text": "CHẲNG AI LẤY GÌ CỦA MÌNH", "at": [7, "Chẳng"], "sm": True},
             {"text": "VẪN THẤY NHƯ BỊ BỎ LẠI", "at": [7, "bị"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "BẪY 3 · ĐI THEO ĐÁM ĐÔNG", "at": [8, "Bẫy"], "acc": True}]},
    {"type": "broll", "at": 9, "vid": "32980016", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "HAI QUÁN PHỞ CẠNH NHAU", "at": [9, "Hai"]},
             {"text": "MÌNH VÀO QUÁN ĐÔNG", "at": [9, "mình"], "acc": True},
             {"text": "có khi chỉ vì vài người đầu tiên tình cờ chọn", "at": [9, "Có"], "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "1992: LÀM THEO ĐÁM ĐÔNG", "at": [10, "Các"]},
                                           {"text": "CÓ THỂ HỢP LÝ VỚI TỪNG NGƯỜI", "at": [10, "hợp"]},
                                           {"text": "CẢ ĐÁM ĐÔNG VẪN CÓ THỂ CÙNG SAI", "at": [11, "cả"], "acc": True},
                                           {"text": "Banerjee; Bikhchandani, Hirshleifer & Welch", "at": [10, "Các"], "sm": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "BẪY 4 · VỪA TĂNG = SẼ TĂNG", "at": [12, "Bẫy"], "acc": True}]},
    {"type": "broll", "at": 13, "vid": "13292544", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "MƯA BA HÔM LIỀN", "at": [13, "Mưa"]}, {"text": "→ \"CẢ TUẦN SẼ MƯA\"", "at": [13, "cả"], "acc": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "01/01 → 29/01/2026 · GIÁ BÁN RA SJC", "at": [14, "Bốn"], "sm": True},
                                           {"text": "152,8 → 191,3 TRIỆU", "at": [14, "giá"]},
                                           {"text": "+25% TRONG 4 TUẦN", "at": [14, "tăng"], "acc": True}],
     "srcnote": "Giá báo chí: 01/01 (Công Luận), 29/01 13:25 (webgia) · minh hoạ quá khứ, không phải khuyến nghị"},
    {"type": "kinetic", "at": 15, "items": [{"text": "Greenwood & Shleifer (2014) · chứng khoán Mỹ 1963–2011", "at": [15, "Greenwood"], "sm": True},
                                           {"text": "VỪA TĂNG MẠNH", "at": [15, "thị"]},
                                           {"text": "→ CÀNG KỲ VỌNG TĂNG TIẾP", "at": [15, "càng"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "THEO CÁC MÔ HÌNH KINH TẾ", "at": [16, "Trong"]},
                                           {"text": "LỢI NHUẬN KỲ VỌNG PHÍA TRƯỚC: THẤP HƠN", "at": [16, "lợi"], "acc": True}]},
    {"type": "question", "at": 17, "text": "Người đứng trong hàng\nlà dại à?"},
    {"type": "slam", "at": 18, "text": "KHÔNG"},
    {"type": "kinetic", "at": 19, "items": [{"text": "29/01: QUÀ CƯỚI CHO CON, CHO EM", "at": [19, "Hôm"]},
                                           {"text": "LÝ DO RẤT THẬT", "at": [19, "Đó"], "acc": True},
                                           {"text": "CafeF, 29/01/2026", "at": [19, "Hôm"], "sm": True}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "HỌC THEO NGƯỜI XUNG QUANH: PHẢN XẠ TỰ NHIÊN", "at": [20, "Học"]},
                                           {"text": "TRÊN THỊ TRƯỜNG, PHẢN XẠ ẤY CÓ GIÁ", "at": [20, "Chỉ"], "acc": True}]},
]}

# ---------------- CH03 · Hàng dài không chỉ là "cả nước đổ xô" ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "HÀNG DÀI KHÔNG CHỈ LÀ \"CẢ NƯỚC ĐỔ XÔ\""}, "bgm": {"mood": "warm", "gain": 0.19}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "HÀNG DÀI KHÔNG CHỈ LÀ\n\"CẢ NƯỚC ĐỔ XÔ\"", "sub": "NHU CẦU · KHAN HÀNG · NGÀY VÍA",
     "vid": "6229548", "ms": 4, "illus": ILLQ, "titleAt": [0, "Có"]},
    {"type": "bars", "at": 1, "title": "NHU CẦU VÀNG MIẾNG & XU · VIỆT NAM", "unit": "TẤN · HỘI ĐỒNG VÀNG THẾ GIỚI (WGC)", "items": [
        {"k": "2024", "v": 42.1, "lbl": "42,1", "at": [1, "Theo"]},
        {"k": "2025", "v": 36.1, "lbl": "36,1 (−14%)", "at": [1, "giảm"], "acc": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "HÀNG DÀI TỪ ĐÂU RA?", "at": [2, "Vậy"]},
                                          {"text": "MỘT PHẦN: KHAN HÀNG", "at": [2, "Một"], "acc": True}]},
    {"type": "kinetic", "at": 3, "vid": "8733007", "illus": ILL,
     "items": [{"text": "THIẾU VÀNG MIẾNG SJC", "at": [3, "Hội"]},
               {"text": "→ CAO HƠN THẾ GIỚI > 550 USD/OZ", "at": [3, "cao"], "acc": True},
               {"text": "WGC, cuối 2025", "at": [3, "Hội"], "sm": True}]},
    {"type": "ledger", "at": 4, "title": "GIỚI HẠN MỖI NGƯỜI", "rows": [
        {"k": "04/06/2024", "v": "1 LƯỢNG", "at": [4, "giới"]},
        {"k": "22/04/2025", "v": "2 CHỈ (CÓ NƠI)", "at": [4, "hai"]},
        {"k": "06/09/2025", "v": "1 LƯỢNG / NGÀY", "at": [4, "lượng"]},
        {"k": "29/01/2026", "v": "TRÊN 4 CHỈ: PHIẾU HẸN (CÓ NƠI)", "at": [4, "ngày"]}]},
    {"type": "slam", "at": 5, "text": "ĐƯỢC MUA LÀ MAY?", "sub": "MÀ NHIỀU LẦN, ĐÓ LẠI LÀ LÚC GIÁ ĐANG LẬP KỶ LỤC"},
    {"type": "kinetic", "at": 6, "items": [{"text": "23/03/2026", "at": [6, "Còn"], "sm": True},
                                          {"text": "GIÁ THẤP HƠN ĐỈNH > 20 TRIỆU", "at": [6, "thấp"]},
                                          {"text": "CÓ TIỆM BỎ GIỚI HẠN", "at": [6, "bỏ"], "acc": True}]},
    {"type": "kinetic", "at": 7, "vid": "6229548", "ms": 2, "illus": ILLQ,
     "items": [{"text": "HÀNG DÀI CŨNG CÓ NGƯỜI BÁN", "at": [7, "Hàng"]},
               {"text": "29/01: XẾP HÀNG 11H → 15H", "at": [7, "mười"]},
               {"text": "VẪN CHƯA TỚI LƯỢT BÁN 2 CHỈ", "at": [7, "vẫn"], "acc": True}]},
    {"type": "question", "at": 8, "text": "Mua vàng ngày vía Thần Tài\ncó phải để cả năm may mắn?"},
    {"type": "broll", "at": 9, "vid": "36468399", "veil": 0.5, "illus": ILL,
     "kin": [{"text": "MÙNG 10 THÁNG GIÊNG · VÍA THẦN TÀI", "at": [9, "Mua"]},
             {"text": "MỘT NÉT VĂN HOÁ", "at": [9, "nét"], "acc": True}]},
    {"type": "broll", "at": 10, "vid": "36112100", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "TÍN NGƯỠNG DÂN GIAN", "at": [10, "Nhà"]},
             {"text": "TIN VÀ HY VỌNG VÀO NĂM MỚI", "at": [10, "tin"], "acc": True},
             {"text": "Ngô Hương Giang, nhà nghiên cứu văn hoá (Tiền Phong)", "at": [10, "Nhà"], "sm": True}]},
    {"type": "ledger", "at": 11, "title": "MUA NGÀY VÍA THẦN TÀI", "rows": [
        {"k": "VÍA 2024 → 12 THÁNG SAU", "v": "+11%", "at": [11, "lãi"]},
        {"k": "VÍA 2025 → 12 THÁNG SAU", "v": "+93%", "at": [12, "gần"]},
        {"k": "VÍA 2026 → ĐẦU THÁNG 10", "v": "−24%", "at": [13, "lỗ"]}],
     "srcnote": NOTE},
    {"type": "slam", "at": 14, "text": "3 NĂM · 3 KẾT QUẢ", "sub": "NGÀY VÍA KHÔNG CHO BIẾT GÌ VỀ HƯỚNG GIÁ"},
    {"type": "kinetic", "at": 15, "items": [{"text": "MỘT CHỈ LẤY LỘC = CHI TIÊU CHO NIỀM VUI", "at": [15, "Mua"]},
                                           {"text": "KHÁC KHI KHOẢN TIỀN LỚN ĐI THEO NGÀY VÍA", "at": [15, "Chuyện"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "VÍA THẦN TÀI 2026", "at": [16, "Ngày"], "sm": True},
                                           {"text": "NHIỀU NGƯỜI CHỌN VÀNG RẤT NHỎ", "at": [16, "nhiều"], "acc": True}]},
    {"type": "quote", "at": 17, "qline": 17, "lbl": "NGUYÊN VĂN", "text": "Một chỉ vàng bằng cả tháng lương.",
     "by": "Một khách hàng, VnExpress 26/02/2026"},
]}

# ---------------- CH04 · Ba khoản trả thêm của người đứng trong hàng ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "BA KHOẢN TRẢ THÊM"}, "bgm": {"mood": "curious", "gain": 0.1}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "BA KHOẢN\nTRẢ THÊM",
     "sub": "CỦA NGƯỜI ĐỨNG TRONG HÀNG · CHÊNH MUA–BÁN · CHÊNH THẾ GIỚI · MUA TRÊN GIẤY", "vid": "5705007", "illus": ILL, "titleAt": [0, "Giả"]},
    {"type": "ledger", "at": 1, "title": "01 · CHÊNH MUA – BÁN", "rows": [
        {"k": "29/01 · TIỆM BÁN RA", "v": "191,3 TR", "at": [2, "bán"]},
        {"k": "29/01 · TIỆM MUA VÀO", "v": "188,3 TR", "at": [2, "mua"]}],
     "total": {"k": "BƯỚC RA KHỎI CỬA", "v": "−3 TR ≈ 1,6%", "at": [3, "lỗ"]},
     "srcnote": "Giá SJC lúc 13:25 ngày 29/01/2026 (webgia) · đơn vị: triệu đồng/lượng"},
    {"type": "question", "at": 4, "text": "Ba triệu trên gần 200 triệu\nthì có đáng gì đâu?"},
    {"type": "kinetic", "at": 5, "items": [{"text": "RIÊNG NÓ THÌ NHỎ", "at": [5, "Riêng"]},
                                          {"text": "NHƯNG KHÔNG ĐỨNG YÊN", "at": [5, "Nhưng"], "acc": True}]},
    {"type": "bars", "at": 6, "title": "CHÊNH MUA – BÁN VÀNG MIẾNG SJC", "unit": "TRIỆU Đ/LƯỢNG · BÁO CHÍ", "items": [
        {"k": "01/01/2026", "v": 2, "lbl": "2", "at": [6, "Ngày"]},
        {"k": "29/01/2026", "v": 3, "lbl": "3", "at": [6, "Ngày", 0, 0.35]},
        {"k": "10/06/2026", "v": 5, "lbl": "5", "at": [6, "năm"]},
        {"k": "23/07/2026", "v": 6, "lbl": "5 – 6", "at": [6, "sáu"], "acc": True}],
     "srcnote": "23/07/2026: chuyên gia gọi là \"cao bất thường\" (Thanh Niên) · số liệu báo chí, minh hoạ quá khứ"},
    {"type": "kinetic", "at": 7, "items": [{"text": "NÓ NỚI RỘNG", "at": [7, "Nó"]},
                                          {"text": "ĐÚNG LÚC NGƯỜI TA HOẢNG MUỐN BÁN", "at": [7, "đúng"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "02 · PHẦN TRẢ THÊM SO VỚI THẾ GIỚI", "at": [8, "Thứ"]},
                                          {"text": "GIÁ SJC = THẾ GIỚI QUY ĐỔI + CHÊNH TRONG NƯỚC", "at": [9, "Giá"], "acc": True}]},
    {"type": "bars", "at": 10, "title": "VÀNG MIẾNG SJC CAO HƠN THẾ GIỚI", "unit": "TRIỆU Đ/LƯỢNG · BÁO CHÍ", "items": [
        {"k": "06/09/2025", "v": 20.8, "lbl": "20,8", "at": [10, "Ngày"]},
        {"k": "26/02/2026 · VÍA", "v": 20, "lbl": "≈ 20 (≈ 1/10 GIÁ)", "at": [10, "hai"], "acc": True},
        {"k": "19/08/2026", "v": 2, "lbl": "≈ 2", "at": [12, "Ngày"]}],
     "srcnote": "Số liệu báo chí (SGGP, VnExpress, Dân trí) · minh hoạ quá khứ, không phải khuyến nghị"},
    {"type": "kinetic", "at": 13, "items": [{"text": "PHẦN TRẢ THÊM CÓ THỂ BỐC HƠI", "at": [13, "Phần"], "acc": True},
                                           {"text": "kể cả khi giá thế giới đứng yên", "at": [13, "kể"], "sm": True}]},
    {"type": "broll", "at": 14, "vid": "39431258", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "VÉ XE TẾT MUA LẠI GIÁ CAO", "at": [14, "Như"]},
             {"text": "QUA TẾT, KHÔNG AI TRẢ LẠI PHẦN CHÊNH", "at": [14, "qua"], "acc": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "KHOẢN CHÊNH KHÔNG ĐI MỘT CHIỀU", "at": [15, "Và"]},
                                           {"text": "ĐẦU THÁNG 10: KHOẢNG 12–13 TRIỆU", "at": [15, "đầu"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "03 · KHAN HÀNG & \"MUA TRÊN GIẤY\"", "at": [16, "Thứ"], "acc": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "MUA TRÊN GIẤY · CUỐI 01 – ĐẦU 02/2026", "at": [17, "Quanh"], "sm": True},
                                           {"text": "ĐẶT CỌC HOẶC TRẢ ĐỦ 100%", "at": [17, "thu"]},
                                           {"text": "GIAO SAU 7–10 NGÀY · ĐƠN LỚN TỚI 90 NGÀY", "at": [17, "bảy"], "acc": True}]},
    {"type": "slam", "at": 18, "text": "CHƯA CÓ VÀNG ĐỂ BÁN", "sub": "NẾU GIÁ RƠI TRONG LÚC CHỜ"},
    {"type": "kinetic", "at": 19, "items": [{"text": "THU NHẬP BÌNH QUÂN · QUÝ I/2026", "at": [19, "Quy"], "sm": True},
                                           {"text": "9 TRIỆU / THÁNG", "at": [19, "chín"], "acc": True}]},
    {"type": "ledger", "at": 20, "title": "1 CHỈ · QUY THEO GIÁ VÀNG MIẾNG", "rows": [
        {"k": "MUA 29/01/2026", "v": "19,13 TR", "at": [20, "mua"]},
        {"k": "BÁN LẠI ĐẦU THÁNG 10", "v": "14,05 TR", "at": [21, "Đầu"]}],
     "srcnote": "1 chỉ = 1/10 lượng vàng miếng SJC · vàng nhẫn, vàng miếng 1 chỉ có giá khác"},
    {"type": "counter", "at": 22, "from": 0, "to": 5080000, "suffix": " đ", "countAt": [22, "Mất"], "until": [22, "triệu."],
     "label": "MẤT TRÊN 1 CHỈ", "sub": {"text": "≈ 56% THÁNG LƯƠNG 9 TRIỆU (THU NHẬP BÌNH QUÂN QUÝ I/2026)", "at": [22, "Hơn"]},
     "srcnote": "Vàng nhẫn, vàng miếng 1 chỉ có giá khác · kênh tự tính"},
]}

# ---------------- CH05 · Khi chẳng may là đỉnh: vì sao khó buông ----------------
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "KHI CHẲNG MAY LÀ ĐỈNH"}, "bgm": {"mood": "calm", "gain": 0.27}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "KHI CHẲNG MAY LÀ ĐỈNH:\nVÌ SAO KHÓ BUÔNG", "sub": "ĐIỂM MỐC · TÂM LÝ SỢ THUA LỖ",
     "titleAt": [0, "Giả"]},
    {"type": "broll", "at": 1, "vid": "7594029", "veil": 0.55, "illus": ILL,
     "kin": [{"text": "ĐÁNH RƠI 500 NGHÌN: TIẾC CẢ TUẦN", "at": [1, "Đánh"]},
             {"text": "NHẶT ĐƯỢC 500 NGHÌN: VUI MỘT BUỔI", "at": [1, "Nhặt"], "acc": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "Kahneman & Tversky (1979) · tâm lý sợ thua lỗ", "at": [2, "Kahneman"], "sm": True},
                                          {"text": "ĐO ĐƯỢC – MẤT SO VỚI MỘT ĐIỂM MỐC", "at": [2, "đo"]},
                                          {"text": "MẤT ĐAU HƠN ĐƯỢC", "at": [2, "mất", 1], "acc": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "Tversky & Kahneman (1992) · trung vị λ ≈ 2,25", "at": [3, "Ước"], "sm": True},
                                          {"text": "LỖ 500 NGHÌN ≈ ĐAU GẤP ĐÔI", "at": [3, "lỗ"]},
                                          {"text": "NIỀM VUI LÃI 500 NGHÌN", "at": [3, "lãi"], "acc": True}]},
    {"type": "race", "at": 4, **RACE_2026, "title": "ĐIỂM MỐC: GIÁ ĐÃ TRẢ NGÀY 29/01", "range": "29/01 → 30/09/2026 · BÁN LẠI CHO TIỆM",
     "drawAt": [4, "Với"], "until": [5, "Bán"]},
    {"type": "kinetic", "at": 6, "items": [{"text": "KÊNH KHÔNG NÓI CHỜ LÀ ĐÚNG HAY SAI", "at": [6, "Kênh"]},
                                          {"text": "CHỜ BAO LÂU? LỊCH SỬ TRẢ LỜI RẤT KHÁC NHAU", "at": [6, "Chỉ"], "acc": True}]},
    {"type": "timeline", "at": 7, "items": [
        {"year": "08/2011", "text": "ĐỈNH 49,12 TRIỆU", "at": [8, "Người"]},
        {"year": "07/2020", "text": "GẦN 9 NĂM SAU: VỀ LẠI", "at": [8, "gần"], "color": UP},
        {"year": "08/2020", "text": "ĐỈNH 62,45 TRIỆU", "at": [7, "Theo"]},
        {"year": "03/2022", "text": "≈ 19 THÁNG SAU: VỀ LẠI", "at": [7, "mười"], "color": UP}],
     "srcnote": "Về lại = giá mua vào SJC vượt giá đỉnh đã trả · kênh tự tính · hai lần này giá đều về lại, không bảo đảm lần sau"},
    {"type": "question", "at": 9, "text": "Lỡ mua đúng đỉnh:\nnên bán hay nên giữ?"},
    {"type": "slam", "at": 10, "text": "KÊNH KHÔNG TRẢ LỜI THAY BẠN", "white": True,
     "sub": "TUỲ KHOẢN TIỀN ẤY CÓ Ý NGHĨA GÌ VỚI BẠN"},
    {"type": "kinetic", "at": 11, "items": [{"text": "MỘT CÂU HỎI", "at": [11, "Nhưng"]},
                                           {"text": "TÁCH ĐIỂM MỐC KHỎI QUYẾT ĐỊNH", "at": [11, "tách"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "NẾU ĐANG CẦM TIỀN MẶT,", "at": [12, "Nếu"]},
                                           {"text": "MÌNH CÓ MUA ĐÚNG CHỪNG NÀY VÀNG?", "at": [12, "mua"], "acc": True},
                                           {"text": "TIỀN NÀY CẦN LẠI KHI NÀO?", "at": [12, "Và"]}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "CÓ HAY KHÔNG ≠ TỰ THÀNH QUYẾT ĐỊNH BÁN HAY GIỮ", "at": [13, "Trả"]},
                                           {"text": "BÁN RỒI MUA LẠI: MẤT THÊM CHÊNH MUA – BÁN", "at": [13, "và"], "acc": True}]},
]}

# ---------------- CH06 · Áp dụng cho bạn, và khi nào không đúng ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "ÁP DỤNG CHO BẠN"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "ÁP DỤNG CHO BẠN —\nVÀ KHI NÀO KHÔNG ĐÚNG",
     "sub": "KHÔNG PHẢI LỜI KHUYÊN MUA, BÁN HAY GIỮ VÀNG", "titleAt": [0, "Mình"]},
    {"type": "ledger", "at": 1, "title": "5 CÂU TRƯỚC KHI ĐỨNG VÀO HÀNG", "rows": [
        {"k": "01", "v": "TIỀN NÀY CẦN LẠI KHI NÀO?", "at": [2, "Một:"]},
        {"k": "02", "v": "GIẢM 10% THÌ MÌNH LÀM GÌ?", "at": [3, "Hai:"]},
        {"k": "03", "v": "ĐANG TRẢ THÊM BAO NHIÊU?", "at": [4, "Ba:"]},
        {"k": "04", "v": "ĐÃ SO VỚI LỰA CHỌN KHÁC?", "at": [5, "Bốn:"]},
        {"k": "05", "v": "CÓ NHẬN VÀNG NGAY KHÔNG?", "at": [6, "Năm:"]}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHI NÀO ĐIỀU NÀY", "at": [7, "Và"]},
                                          {"text": "KHÔNG ĐÚNG VỚI BẠN?", "at": [7, "không"], "acc": True}]},
    {"type": "ledger", "at": 8, "title": "KHI NÀO KHÔNG ĐÚNG", "rows": [
        {"k": "GIỮ RẤT LÂU", "v": "≈ 7,2%/NĂM (DANH NGHĨA)", "at": [8, "Nếu"]},
        {"k": "VÀNG CƯỚI, HỒI MÔN", "v": "ĐỦ TIỀN, KHÔNG VAY?", "at": [9, "Nếu"]},
        {"k": "MUA ĐỀU, MUA NHỎ", "v": "ÍT PHỤ THUỘC NGÀY MUA", "at": [10, "Nếu"]},
        {"k": "KÝ ỨC LẠM PHÁT", "v": "LÝ DO RẤT THẬT", "at": [11, "Nếu"]}],
     "srcnote": "Đỉnh 2011 → 06/10/2026 ≈ 7,2%/năm danh nghĩa, chưa trừ lạm phát, gần 9 năm âm · kênh tự tính · quá khứ ≠ tương lai"},
    {"type": "slam", "at": 12, "text": "KHÔNG CÓ HÀNG DÀI ≠ AN TOÀN", "hitAt": [12, "Và"],
     "sub": "QUANH ĐỈNH 2020: \"KHÔNG CÒN HIỆN TƯỢNG ĐỔ XÔ\""},
    {"type": "kinetic", "at": 13, "items": [{"text": "NGƯỜI ĐỨNG TRONG HÀNG", "at": [13, "Tóm"]},
                                           {"text": "KHÔNG DẠI", "at": [13, "không"], "acc": True}]},
    {"type": "ledger", "at": 14, "title": "BỘ NÃO VẪN LÀM VẬY", "rows": [
        {"k": "01", "v": "NHỚ ĐIỀU DỄ NHỚ", "at": [14, "nhớ"]},
        {"k": "02", "v": "SỢ BỊ BỎ LẠI", "at": [14, "sợ"]},
        {"k": "03", "v": "THEO ĐÁM ĐÔNG", "at": [14, "theo"]},
        {"k": "04", "v": "VỪA TĂNG = SẼ TĂNG", "at": [14, "tin"]}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "LẦN TỚI THẤY ẢNH HÀNG DÀI", "at": [15, "Lần"]},
                                           {"text": "\"ĐỈNH CHƯA?\" — KHÔNG AI BIẾT", "at": [15, "không", 1], "acc": True}]},
    {"type": "slam", "at": 16, "text": "KẾ HOẠCH CỦA MÌNH,\nKHÔNG PHẢI ĐỘ DÀI CỦA HÀNG"},
    {"type": "question", "at": 17, "text": "Bạn hay người nhà\nđã từng xếp hàng mua vàng?\nĐiều gì khiến bạn đứng vào hàng?"},
]}

TITLE = "Xếp Hàng Mua Vàng Có Phải Là Đỉnh? Đọc Lại 11 Đợt Đổ Xô (2011–2026) Bằng Dữ Liệu"
DISCLAIMER = ("Nội dung giáo dục, không phải tư vấn đầu tư hay tư vấn tài chính cá nhân. Không khuyến nghị mua/bán/giữ vàng hay "
              "bất kỳ tài sản nào, không dự báo giá. Ví dụ dùng dữ liệu quá khứ; quá khứ không đảm bảo tương lai. Nội dung do kênh "
              "biên soạn từ nguồn công khai; giọng đọc tổng hợp. SJC chỉ được dùng làm thước đo giá vàng miếng.")
METHOD = ("📐 CÁCH TÍNH (kênh tự tính): người mua trả GIÁ BÁN RA ngày xếp hàng; giá trị về sau tính bằng GIÁ MUA VÀO của tiệm "
          "(giá niêm yết vàng miếng SJC, truy xuất qua vnstock; trước 2026 dữ liệu ~2 điểm/tháng nên vài mốc có sai số vài triệu). "
          "\"Đầu tháng mười\" = giá mua vào SJC sáng 06/10/2026: 140,5 triệu/lượng (VietnamPlus). Biểu đồ dừng ở 30/09/2026; điểm "
          "30/09 lấy giá chốt chiều 141,1/144,1 (Báo Đà Nẵng) vì dữ liệu gốc lặp giá 29/09. Đợt 04/06/2024: biểu đồ dùng giá "
          "niêm yết SJC 79,98 (không phải giá bình ổn 78,98) nên ra ≈ +44% thay vì +45,5%. Về lại giá đã trả = giá mua vào SJC "
          "vượt giá đỉnh (đỉnh 2011 là giá \"vàng trong nước\" theo báo chí). 1 chỉ = 1/10 lượng theo giá vàng miếng; vàng nhẫn có "
          "giá khác. Bảng 11 đợt là các đợt kênh tìm được trên báo chí có ghi ngày và giá, không phải mọi lần xếp hàng.")
SPEC = {
    "title": TITLE, "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO",
    "acc": ["sjc", "vàng", "đỉnh", "lỗ", "lãi", "chênh", "fomo", "bẫy", "vía"],
    "say": SAY, "imgs": {}, "chapters": list(CH),
    "youtube": {
        "titles": [TITLE, "Đứng Trong Hàng Mua Vàng: Bộ Não Nghĩ Gì, Và Bạn Trả Thêm Những Gì?",
                   "11 Đợt Xếp Hàng Mua Vàng (2011–2026): Sau Đó Giá Đã Đi Đâu?"],
        "summary": "Rạng sáng 29/01/2026, người ta đã xếp hàng chờ mua vàng ở phố Trần Nhân Tông; chiều hôm đó vàng miếng SJC lập "
                   "đỉnh 191,3 triệu/lượng. Vậy cứ thấy xếp hàng là giá sắp đỉnh? Kênh đọc lại 11 đợt đổ xô mua vàng được báo chí "
                   "ghi lại từ 2011 đến 2026: 4 đợt rơi vào vùng đỉnh, 5 đợt giá sau đó còn lên, 2 đợt lỗ dù không phải đỉnh. Video "
                   "giải thích 4 cái bẫy tâm lý khiến ai cũng muốn đứng vào hàng, 3 khoản trả thêm ít ai thấy, và 5 câu tự hỏi "
                   "trước khi bạn đứng vào một hàng dài. Dữ liệu thật, kênh tự tính, giải thích dễ hiểu.",
        "more": [DISCLAIMER, METHOD],
        "chapter_titles": {"ch00": "Mở đầu: hai mươi chín tháng một", "ch01": "Mười một lần xếp hàng: bảng điểm",
                           "ch02": "Bốn cái bẫy của bộ não", "ch03": "Hàng dài không chỉ là \"cả nước đổ xô\"",
                           "ch04": "Ba khoản trả thêm của người đứng trong hàng", "ch05": "Khi chẳng may là đỉnh: vì sao khó buông",
                           "ch06": "Áp dụng cho bạn, và khi nào không đúng"},
        "sources": [
            "CafeF 29/01/2026 — Cảnh tượng khó tin trên phố Trần Nhân Tông: https://cafef.vn/canh-tuong-kho-tin-tren-pho-tran-nhan-tong-vi-sao-nguoi-dan-ha-noi-kien-nhan-xep-hang-dai-suot-nhieu-gio-dong-ho-188260129162833892.chn",
            "Phụ Nữ Online 29/01/2026 — Người dân Hà Nội xếp hàng chờ mua, bán vàng: https://tuoitre.vn/phunuonline/nguoi-dan-ha-noi-kien-nhan-xep-hang-gan-ca-chuc-tieng-dong-ho-cho-mua-ban-vang-1101573603.htm",
            "Webgia — giá vàng SJC ngày 29/01/2026: https://webgia.com/gia-vang/sjc/29-01-2026.html",
            "VietnamPlus 06/10/2026 — bảng giá vàng (SJC 140,5/143,5): https://www.vietnamplus.vn/gia-vang-ngay-610-bang-gia-tai-cac-cong-ty-vang-bac-da-quy-trong-nuoc-post1140249.vnp",
            "Báo Đà Nẵng 30/09/2026 — SJC 141,1/144,1: https://baodanang.vn/gia-vang-ngay-30092026-sjc-tang-len-1411-1441-trieu-dongluong-3353622.html",
            "Báo Đắk Lắk 09/2011 — tháng 8/2011 giá vàng (đỉnh 49,12 ngày 23/08): https://baodaklak.vn/channel/3543/201109/thang-8-2011-gia-vang-tang-7-trieu-dongluong-2092596/",
            "SGGP — Năm 2013 giá vàng giảm 11,53 triệu đồng/lượng: https://www.sggp.org.vn/nam-2013-gia-vang-giam-1153-trieu-dongluong-post68199.html",
            "VnExpress 20/03/2025 — Nỗi ám ảnh sau cú sốc vàng năm 2011 (ý kiến bạn đọc): https://vnexpress.net/noi-am-anh-sau-cu-soc-vang-len-50-trieu-roi-lao-doc-nam-2011-4863794.html",
            "Báo Pháp luật 11/08/2020 — đỉnh 62,45 triệu: https://doanhnhan.baophapluat.vn/chi-sau-1-dem-gia-vang-sjc-boc-hoi-tiep-12-trieu-dongluong-31995.html",
            "Người Lao Động 09/02/2021 — 1 năm sóng gió của giá vàng SJC khi vượt đỉnh 62 triệu: https://tuoitre.vn/nld/kinh-te/1-nam-song-gio-cua-gia-vang-sjc-khi-vuot-dinh-62-trieu-dong-luong-20210209002616492.htm",
            "Tuổi Trẻ 04/06/2024 — SJC giới hạn mỗi khách 1 lượng: https://tuoitre.vn/sjc-gioi-han-moi-khach-duoc-mua-1-luong-mua-vang-o-nhieu-ngan-hang-phai-dang-ky-truoc-20240604163846603.htm",
            "Tuổi Trẻ 07/02/2025 — giá vàng ngày vía Thần Tài 2025: https://tuoitre.vn/gia-vang-tang-nua-trieu-dong-luong-ngay-via-than-tai-20250207094603859.htm",
            "VOV 22/04/2025 — vàng SJC lên 124 triệu: https://vov.vn/thi-truong/gia-vang/vang-sjc-len-muc-cao-nhat-tu-truoc-toi-nay-124-trieu-dongluong-post1193911.vov",
            "SGGP 07/09/2025 — xếp hàng dài dù giá lập đỉnh: https://www.sggp.org.vn/xep-hang-dai-cho-mua-vang-du-gia-lap-dinh-post811937.html",
            "Vietnambiz 04/02/2026 — xếp hàng mua vàng \"trên giấy\": https://vietnambiz.vn/xep-hang-mua-vang-bac-tren-giay-chua-duoc-cam-trong-tay-da-lo-nang-chuyen-gia-canh-bao-gi-202624131025160.htm",
            "VnExpress 26/02/2026 — giá vàng ngày vía Thần Tài: https://vnexpress.net/gia-vang-hom-nay-26-2-ngay-via-than-tai-5044187.html",
            "VietNamNet 02/03/2026 — SJC 187,9/190,9: https://vietnamnet.vn/gia-vang-hom-nay-2-3-2026-nong-bong-tay-vang-mieng-sjc-leo-len-dinh-2493734.html",
            "Phụ Nữ Online 21/03/2026 — chen nhau giữa trưa chờ \"bắt đáy\": https://tuoitre.vn/phunuonline/gia-vang-giam-manh-nguoi-dan-chen-nhau-giua-trua-nang-cho-bat-day-1101577945.htm",
            "Vietstock (đăng lại trên Investing) 23/03/2026 — tiệm vàng bỏ giới hạn: https://vn.investing.com/news/commodities-news/tiem-vang-o-at-xa-hang-cho-mua-thoai-mai-khi-gia-chenh-toi-gan-30-trieuluong-2568859",
            "VietNamNet 10/06/2026 — chênh mua–bán 5 triệu: https://vietnamnet.vn/gia-vang-hom-nay-10-6-2026-sjc-roi-xuong-day-6-thang-ap-luc-giam-tiep-2524437.html",
            "Thanh Niên 23/07/2026 — chênh 5–6 triệu \"cao bất thường\": https://thanhnien.vn/vi-sao-gia-vang-giam-7-trieu-luong-trong-sang-237-185260723133329149.htm",
            "Dân trí 19/08/2026 — khoảng cách SJC – thế giới còn 2 triệu: https://dantri.com.vn/kinh-doanh/khoang-cach-gia-vang-sjc-va-the-gioi-thu-hep-con-2-trieu-dongluong-20260819195145057.htm",
            "Kenh14 06/10/2026 — SJC cao hơn thế giới gần 13 triệu: https://kenh14.vn/vang-sjc-cao-hon-the-gioi-gan-13-trieu-dong-luong-215261006102618401.chn",
            "Công Luận 01/01/2026 — giá vàng đầu năm: https://congluan.vn/gia-vang-hom-nay-01-01-2026-gia-vang-mieng-vang-nhan-trong-nuoc-va-gia-vang-the-gioi-post326855.html",
            "Tiền Phong 05/02/2025 — Ngô Hương Giang về tục mua vàng ngày vía: https://tienphong.vn/co-nen-mua-vang-ngay-via-than-tai-post1714576.tpo",
            "Hội đồng Vàng Thế giới (WGC) — Gold Demand Trends Full Year 2025: https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-full-year-2025",
            "Tổng cục Thống kê (NSO) — thu nhập bình quân lao động quý I/2026 (9,0 triệu đồng/tháng)",
            "Tversky & Kahneman (1973), Availability, Cognitive Psychology 5(2) · Kahneman & Tversky (1979), Prospect Theory, Econometrica 47(2) · Tversky & Kahneman (1992), Journal of Risk and Uncertainty 5(4)",
            "Barber & Odean (2008), All That Glitters, Review of Financial Studies 21(2): https://econpapers.repec.org/RePEc:oup:rfinst:v:21:y:2008:i:2:p:785-818",
            "Przybylski và cộng sự (2013), Fear of missing out, Computers in Human Behavior 29(4) · Banerjee (1992), QJE 107(3) · Bikhchandani, Hirshleifer & Welch (1992), JPE 100(5)",
            "Greenwood & Shleifer (2014), Expectations of Returns and Expected Returns, Review of Financial Studies 27(3): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2199762",
            "Hồ sơ dữ kiện đầy đủ do kênh lưu trữ; liên hệ qua bình luận nếu cần nguồn cụ thể.",
        ],
        "hashtags": ["GiáVàng", "VàngSJC", "TâmLýTiềnBạc", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["giá vàng", "giá vàng 2026", "vàng miếng SJC", "xếp hàng mua vàng", "đỉnh giá vàng", "lịch sử giá vàng Việt Nam",
                 "ngày vía Thần Tài", "tâm lý đám đông", "FOMO", "tài chính hành vi", "chênh lệch giá mua bán vàng",
                 "tâm lý tiền bạc", "tài chính cá nhân"],
        "category": "27",
        "data_credit": "📊 DỮ LIỆU BIỂU ĐỒ: giá vàng miếng niêm yết SJC (sjc.com.vn), truy xuất qua Vnstock; điểm 30/09/2026 sửa theo "
                       "báo chí. Nhu cầu vàng: Hội đồng Vàng Thế giới (WGC). Các mốc giá khác: báo chí (link ở trên). Số liệu tổng hợp "
                       "do kênh tự tính.",
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
