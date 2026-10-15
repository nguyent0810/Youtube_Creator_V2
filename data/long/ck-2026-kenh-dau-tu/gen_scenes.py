"""Sinh spec.json + scenes/hud/bgm cho video dài CK #1 "Năm 2026: chứng khoán, vàng, coin, nhà đất đều đỏ — chỉ sổ tiết
kiệm xanh. Nhưng thắng thật không?" (kênh Biểu Đồ Biết Nói, theme "chart").

    python data/long/ck-2026-kenh-dau-tu/gen_scenes.py     # giữ nguyên "lines" (script_lines.py ghi)

Dữ kiện + nguồn: docs/channels/chung-khoan/2026-10-06-long-01-research.md; kiểm chứng: factcheck.md (cùng thư mục).
Biểu đồ vẽ từ data/ck/ (vnstock: HOSE, SJC; CoinGecko: Bitcoin USD) -- motion/long/chartdata.py. Clip: Pexels (ngang).
Luật kênh: không khuyến nghị, không dự báo, không nêu tên ngân hàng/sàn; giai đoạn thị trường chốt 30/09/2026.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

UP, DN, GOLD, BLUE, ORANGE = "#4ade80", "#f87171", "#fbbf24", "#38bdf8", "#f97316"
# Sổ 12 tháng 4 NH lớn cuộn mỗi tháng 10 (hồ sơ mục 7.1 + factcheck: VCB 10/2020 6,0%, 10/2024 4,6%)
ROLL = [["2018-10-01", .066], ["2019-10-01", .068], ["2020-10-01", .060], ["2021-10-01", .055], ["2022-10-01", .064],
        ["2023-10-01", .053], ["2024-10-01", .046], ["2025-10-01", .047]]

SAY = {"vn-index": "Vi En In-đéc", "hose": "hô-dê", "sjc": "ét giây xi", "bitcoin": "Bít-coi", "kevin": "Ke-vin",
       "warsh": "Óoc", "trump": "Tờ-răm", "qr": "kiu a"}

CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "100 TRIỆU, NĂM KÊNH, MỘT NĂM"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "counter", "from": 0, "to": 100000000, "suffix": " đ", "countAt": [0, "một"], "label": "ĐẦU NĂM 2026"},
    {"type": "ledger", "at": 1, "title": "CHIA ĐỀU 5 KÊNH", "rows": [
        {"k": "CHỨNG KHOÁN", "v": "20 TRIỆU", "at": [2, "chứng"]}, {"k": "VÀNG MIẾNG", "v": "20 TRIỆU", "at": [3, "vàng"]},
        {"k": "BITCOIN", "v": "20 TRIỆU", "at": [4, "Bitcoin."]}, {"k": "NHÀ ĐẤT", "v": "20 TRIỆU", "at": [5, "nhà"]},
        {"k": "TIẾT KIỆM 12 THÁNG", "v": "20 TRIỆU", "at": [6, "tiết"]}]},
    {"type": "race", "at": 7, "from": "2026-01-01", "to": "2026-09-30", "money": 20, "title": "100 TRIỆU, CHIA ĐỀU",
     "range": "01/01 → 30/09/2026", "drawAt": [7, "mở"], "until": [11, "khó"],
     "series": [{"key": "vnindex", "label": "CHỨNG KHOÁN (VN-INDEX)", "color": BLUE},
                {"key": "sjc", "label": "VÀNG MIẾNG SJC", "color": GOLD},
                {"key": "btc", "label": "BITCOIN (GIÁ USD)", "color": ORANGE},
                {"key": "deposit", "rate": 0.052, "label": "TIẾT KIỆM 5,2%", "color": UP}],
     "source": "DỮ LIỆU: HOSE, SJC (QUA VNSTOCK), COINGECKO · TIẾT KIỆM: 4 NH LỚN 01/2026, LÃI DỒN TÍCH · NHÀ ĐẤT: KHÔNG CÓ CHỈ SỐ NGÀY · MINH HOẠ"},
    {"type": "question", "at": 13, "text": "Vậy năm nay cứ gửi ngân hàng\nlà thắng à?"},
    {"type": "slam", "at": 14, "text": "THẮNG TRÊN GIẤY", "sub": "NHƯNG ÍT HƠN BẠN TƯỞNG"},
    {"type": "ledger", "at": 15, "title": "BA CÂU HỎI", "rows": [
        {"k": "01", "v": "CHUYỆN GÌ XẢY RA VỚI TỪNG KÊNH?", "at": [16, "chuyện"]},
        {"k": "02", "v": "VÌ SAO TIẾT KIỆM VỀ NHẤT?", "at": [17, "vì"]},
        {"k": "03", "v": "NÓI GÌ VỚI TIỀN CỦA BẠN?", "at": [18, "nói"]}]},
    {"type": "brand", "at": 19, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CHỨNG KHOÁN: ĐỨNG YÊN MÀ ĐI MỘT VÒNG"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CHỨNG KHOÁN:\nĐỨNG YÊN MÀ ĐI MỘT VÒNG", "sub": "VN-INDEX · 2026",
     "vid": "38736271", "titleAt": [0, "Cuối"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "1.784 → 1.769", "at": [1, "quanh"], "acc": True},
                                          {"text": "31/12/2025 → 30/09/2026", "at": [1, "Cuối"], "sm": True},
                                          {"text": "−0,9%", "at": [2, "Giảm"]}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "CẢ NĂM CHẲNG CÓ GÌ?", "at": [3, "chẳng"], "acc": True}]},
    {"type": "candles", "at": 4, "series": "vnindex", "from": "2025-12-01", "to": "2026-09-30", "drawAt": [4, "nhìn"],
     "until": [6, "xuống"], "title": "VN-INDEX · KHUNG NGÀY", "range": "12/2025 – 09/2026", "ind": [],
     "marks": [{"date": "2026-03-23", "text": "Đáy 1.586 (trong phiên)", "pos": "below", "tone": "down", "at": [6, "xuống"], "dx": -160, "dy": 30},
               {"date": "2026-05-19", "text": "Đỉnh 1.933 (trong phiên)", "pos": "above", "tone": "up", "at": [7, "chạm"], "dx": 200, "dy": -10}]},
    {"type": "slam", "at": 9, "text": "HƠN 20%", "sub": "TỪ ĐÁY LÊN ĐỈNH · TRONG PHIÊN"},
    {"type": "kinetic", "at": 10, "items": [{"text": "MUA THEO CHỈ SỐ ĐÚNG ĐỈNH THÁNG 5", "at": [10, "đỉnh"]},
                                           {"text": "CUỐI THÁNG 9: ≈ −8,5%", "at": [10, "lỗ"], "acc": True}]},
    {"type": "question", "at": 11, "text": "Được nâng hạng thị trường,\nsao không tăng?"},
    {"type": "date", "at": 12, "day": "NÂNG HẠNG FTSE CÓ HIỆU LỰC", "date": "21.09.2026"},
    {"type": "ledger", "at": 13, "title": "9 THÁNG 2026", "rows": [
        {"k": "TIỀN QUỸ CHỈ SỐ · ĐỢT 1", "v": "≈ 10%", "at": [13, "mười"]},
        {"k": "KHỐI NGOẠI BÁN RÒNG (HOSE)", "v": "> 95.000 TỶ", "at": [13, "chín"]},
        {"k": "THÁNG BÁN RÒNG LIÊN TIẾP", "v": "9", "at": [13, "liên"]}]},
    {"type": "broll", "at": 14, "vid": "38557069", "veil": 0.55, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "THANH KHOẢN THẤP NHẤT 19 THÁNG", "at": [14, "thấp"], "acc": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "MỘT CHI TIẾT NỮA", "at": [15, "chi"], "sm": True},
                                           {"text": "MỘT NHÓM CỔ PHIẾU VỐN HOÁ RẤT LỚN", "at": [16, "vốn"], "acc": True}]},
    {"type": "ledger", "at": 17, "title": "NỬA ĐẦU 2026", "rows": [
        {"k": "VN-INDEX", "v": "+4,23%", "at": [17, "tăng"]},
        {"k": "BỎ NHÓM VỐN HOÁ LỚN ĐÓ RA", "v": "≈ −1,81%", "at": [17, "âm"]}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "CHỈ SỐ TRÊN TIN TỨC", "at": [18, "tin"]},
                                           {"text": "≠ TÀI KHOẢN CỦA BẠN", "at": [18, "tài"], "acc": True}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "KHOÁ CHỨNG KHOÁN TỪ SỐ 0", "at": [19, "khoá"], "acc": True},
                                           {"text": "sẽ giải thích vì sao", "at": [19, "giải"], "sm": True}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "VÀNG: TỪ HÀNG DÀI ĐẾN 51 TRIỆU"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "VÀNG: TỪ HÀNG DÀI\nĐẾN 51 TRIỆU", "sub": "VÀNG MIẾNG · 2026",
     "vid": "8733007", "titleAt": [0, "Ngày"]},
    {"type": "broll", "at": 1, "vid": "6229548", "veil": 0.5, "illus": "VIDEO MINH HỌA, KHÔNG PHẢI CẢNH Ở HÀ NỘI",
     "kin": [{"text": "29/01/2026 · HÀ NỘI", "at": [1, "chờ"]}, {"text": "XẾP HÀNG NHIỀU GIỜ MUA VÀNG", "at": [1, "tiệm"], "acc": True}]},
    {"type": "date", "at": 2, "day": "VÀNG MIẾNG SJC LẬP ĐỈNH", "date": "29.01.2026",
     "sub": {"text": "191,3 TRIỆU/LƯỢNG (GIÁ BÁN RA)", "at": [2, "một"]}},
    {"type": "kinetic", "at": 3, "items": [{"text": "30/01 · MỸ", "at": [3, "Ngày"], "sm": True},
                                          {"text": "KEVIN WARSH ĐƯỢC ĐỀ CỬ CHỦ TỊCH FED", "at": [3, "đề"], "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "ĐÔ LA TĂNG", "at": [4, "đô"]}, {"text": "VÀNG THẾ GIỚI RƠI MẠNH", "at": [4, "rơi"], "acc": True}]},
    {"type": "broll", "at": 5, "vid": "29576552", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "THÁNG 3 · GIÁ DẦU TĂNG VỌT", "at": [5, "dầu"]}, {"text": "HY VỌNG LÃI SUẤT MỸ GIẢM: GẦN NHƯ HẾT", "at": [5, "xoá"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "VÀNG KHÔNG TRẢ LÃI", "at": [6, "lãi"], "acc": True}]},
    {"type": "race", "at": 7, "from": "2026-01-01", "to": "2026-10-06", "title": "VÀNG MIẾNG SJC 2026", "range": "01/01 → 06/10",
     "drawAt": [7, "Đến"], "until": [9, "tám"], "money": 20,
     "series": [{"key": "sjc", "label": "MUA ĐẦU NĂM, BÁN LẠI CHO TIỆM", "color": GOLD}],
     "source": "GIÁ NIÊM YẾT SJC THEO NGÀY (QUA VNSTOCK): MUA Ở GIÁ BÁN RA 01/01, ĐỊNH GIÁ BẰNG GIÁ MUA VÀO · MINH HOẠ"},
    {"type": "kinetic", "at": 10, "items": [{"text": "MỘT CHI TIẾT ÍT NGƯỜI ĐỂ Ý", "at": [10, "chi"], "acc": True}]},
    {"type": "ledger", "at": 11, "title": "MUA – BÁN VÀNG MIẾNG · 06/10", "rows": [
        {"k": "BẠN MUA (GIÁ BÁN RA)", "v": "142,9 TR", "at": [11, "bán"]},
        {"k": "BẠN BÁN LẠI (GIÁ MUA VÀO)", "v": "139,9 TR", "at": [11, "chênh"]}],
     "total": {"k": "VỪA MUA ĐÃ LỖ", "v": "≈ 2%", "at": [12, "lỗ"]}},
    {"type": "question", "at": 14, "text": "Vậy vàng là kênh tệ à?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "VẪN CAO HƠN CÙNG KỲ NĂM NGOÁI", "at": [15, "cao"]},
                                           {"text": "2025: VÀNG THẾ GIỚI +65%", "at": [15, "sáu"], "acc": True}]},
    {"type": "slam", "at": 16, "text": "MUA SAU CƠN SỐT", "sub": "TRẢ GIÁ CHO CƠN SỐT"},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "COIN VÀ NHÀ ĐẤT: HAI KIỂU ĐỎ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "COIN VÀ NHÀ ĐẤT:\nHAI KIỂU ĐỎ", "sub": "BITCOIN · BẤT ĐỘNG SẢN",
     "vid": "38905688", "titleAt": [0, "Bitcoin"]},
    {"type": "race", "at": 1, "from": "2025-10-07", "to": "2026-09-30", "title": "BITCOIN · 12 THÁNG (GIÁ USD)",
     "range": "07/10/2025 → 30/09/2026", "drawAt": [1, "Đỉnh"], "until": [3, "bốn"],
     "series": [{"key": "btc", "label": "BITCOIN", "color": ORANGE}],
     "source": "DỮ LIỆU: COINGECKO (GIÁ USD) · MINH HOẠ, KHÔNG PHẢI KHUYẾN NGHỊ"},
    {"type": "ledger", "at": 4, "title": "BITCOIN · GIÁ USD", "rows": [
        {"k": "TỪ ĐẦU NĂM", "v": "≈ −4 ĐẾN −5%", "at": [4, "đầu"]},
        {"k": "12 THÁNG", "v": "≈ −27%", "at": [4, "mười"]},
        {"k": "ĐÁY 2026 SO VỚI ĐỈNH", "v": "≈ −54%", "at": [4, "Tính"]}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "TÀI SẢN MÃ HOÁ = TÀI SẢN", "at": [5, "tài"]},
                                          {"text": "NHƯNG KHÔNG PHẢI LÀ TIỀN", "at": [5, "tiền"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "CHƯA TỔ CHỨC NÀO ĐƯỢC CẤP PHÉP", "at": [6, "cấp"], "acc": True},
                                          {"text": "sàn nước ngoài: không được bảo hiểm tiền gửi Việt Nam chi trả", "at": [6, "bảo"], "sm": True}]},
    {"type": "broll", "at": 7, "vid": "32636373", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "NHÀ ĐẤT: GIAO DỊCH CHẬM HẲN", "at": [7, "giao"], "acc": True}]},
    {"type": "bars", "at": 8, "title": "SỐ GIAO DỊCH QUÝ II/2026 · SO VỚI CÙNG KỲ 2025", "unit": "BỘ XÂY DỰNG", "items": [
        {"k": "CÙNG KỲ 2025", "v": 100, "lbl": "100%", "at": [8, "Bộ"]},
        {"k": "TỔNG", "v": 63.7, "lbl": "63,7%", "at": [8, "sáu"], "acc": True},
        {"k": "ĐẤT NỀN", "v": 59.9, "lbl": "59,9%", "at": [9, "đất"], "acc": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "ĐẤT NỀN CẢ NƯỚC: −2 ĐẾN −3%", "at": [10, "Giá"]},
                                           {"text": "HÀ NỘI (GIÁ RAO, Q3 SO Q1): −14%", "at": [10, "mười"], "acc": True}]},
    {"type": "question", "at": 11, "text": "Giá chỉ giảm vài phần trăm\nthì đâu đáng lo?"},
    {"type": "kinetic", "at": 12, "items": [{"text": "BÁN ĐƯỢC KHÔNG?", "at": [12, "Với"]},
                                           {"text": "BÁN MẤT BAO LÂU?", "at": [12, "mất"], "acc": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "LÃI VAY MUA NHÀ SAU ƯU ĐÃI", "at": [13, "vay"]},
                                           {"text": "13 – 15% / NĂM", "at": [13, "mười"], "acc": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "NGƯỜI GỬI TIỀN VUI", "at": [14, "Lãi"]},
                                           {"text": "NGƯỜI ĐI VAY Ở PHÍA NGƯỢC LẠI", "at": [14, "vay"], "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "SỔ TIẾT KIỆM THẮNG — NHƯNG THẮNG THẬT KHÔNG?"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "SỔ TIẾT KIỆM THẮNG\nNHƯNG THẮNG THẬT KHÔNG?", "sub": "LÃI SUẤT · LẠM PHÁT",
     "vid": "5909916", "titleAt": [0, "Vậy"]},
    {"type": "bars", "at": 1, "title": "LÃI SUẤT 12 THÁNG · 4 NGÂN HÀNG LỚN", "unit": "%/NĂM", "items": [
        {"k": "01/2026", "v": 5.2, "lbl": "5,2%", "at": [2, "năm"]},
        {"k": "03/2026", "v": 5.9, "lbl": "5,9%", "at": [2, "lên"]},
        {"k": "06/2026", "v": 6.8, "lbl": "6,8%", "at": [2, "sáu"], "acc": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "4 NGÂN HÀNG LỚN: 6,8%", "at": [3, "Nhiều"]},
                                          {"text": "NHIỀU NGÂN HÀNG KHÁC: KHOẢNG 7 – 8%", "at": [3, "bảy"], "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "CHO VAY RA NHANH HƠN", "at": [4, "cho"]},
                                          {"text": "TIỀN HUY ĐỘNG VÀO", "at": [4, "huy"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "CUỐI THÁNG 4 · SO CÙNG KỲ", "at": [5, "Có"], "sm": True},
                                          {"text": "TÍN DỤNG TĂNG ~GẤP ĐÔI TIỀN GỬI", "at": [5, "gấp"], "acc": True}]},
    {"type": "broll", "at": 6, "vid": "6266262", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "TRẢ LÃI CAO HƠN ĐỂ GIỮ NGƯỜI GỬI", "at": [6, "giữ"], "acc": True},
             {"text": "+ TỶ GIÁ, LẠM PHÁT", "at": [7, "tỷ"]}]},
    {"type": "slam", "at": 8, "text": "PHẦN QUAN TRỌNG NHẤT", "white": True},
    {"type": "ledger", "at": 9, "title": "20 TRIỆU GỬI TỪ 01/01", "rows": [
        {"k": "LÃI SUẤT (4 NH LỚN)", "v": "5,2%/NĂM", "at": [9, "năm"]},
        {"k": "LÃI DỒN TÍCH 9 THÁNG", "v": "+3,9% ≈ 780 NGHÌN", "at": [10, "ba"]}],
     "total": {"k": "GIÁ CẢ 9 THÁNG (CPI)", "v": "+4,2%", "at": [11, "bốn"]}},
    {"type": "broll", "at": 12, "vid": "31144326", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "XĂNG ↑   ĐỒ ĂN ↑   THUÊ NHÀ ↑", "at": [12, "Xăng"], "acc": True}]},
    {"type": "slam", "at": 13, "text": "XANH TRÊN GIẤY", "sub": "SỨC MUA GẦN NHƯ ĐỨNG YÊN"},
    {"type": "kinetic", "at": 14, "items": [{"text": "KÊNH \"THẮNG\"", "at": [14, "thắng"]},
                                           {"text": "= KÊNH NGHÈO ĐI ÍT NHẤT", "at": [14, "ít"], "acc": True}]},
    {"type": "question", "at": 15, "text": "Gửi ngân hàng\ncó rủi ro gì không?"},
    {"type": "ledger", "at": 16, "title": "3 ĐIỀU NÊN BIẾT VỀ TIỀN GỬI", "rows": [
        {"k": "01", "v": "LẠM PHÁT", "at": [17, "lạm"]},
        {"k": "02", "v": "RÚT TRƯỚC HẠN: < 1%/NĂM", "at": [18, "rút"]},
        {"k": "03", "v": "BẢO HIỂM ≤ 350 TR / NGƯỜI / NH", "at": [19, "ba"]}]},
    {"type": "slam", "at": 20, "text": "\"GÓI NỘI BỘ 15–20%\"", "sub": "CÔNG AN CẢNH BÁO: LỪA ĐẢO"},
    {"type": "kinetic", "at": 21, "items": [{"text": "LÃI THẬT: NIÊM YẾT CÔNG KHAI", "at": [21, "Theo"], "acc": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "MỘT NĂM KHÁC MƯỜI NĂM"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "MỘT NĂM\nKHÁC MƯỜI NĂM", "sub": "2018 — 2026",
     "vid": "35561857", "titleAt": [0, "Nếu"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "LÙI LẠI MỘT NĂM", "at": [1, "lùi"], "acc": True}]},
    {"type": "bars", "at": 2, "title": "NĂM 2025", "unit": "%", "items": [
        {"k": "VN-INDEX", "v": 40.9, "lbl": "+40,9%", "at": [2, "bốn"], "acc": True},
        {"k": "VÀNG THẾ GIỚI", "v": 65, "lbl": "+65%", "at": [2, "sáu"], "acc": True},
        {"k": "TIẾT KIỆM 4 NH LỚN", "v": 4.7, "lbl": "< 5%", "at": [3, "năm"]}]},
    {"type": "race", "at": 4, "from": "2018-10-08", "to": "2026-10-06", "money": 100, "unit": "đ", "title": "100 ĐỒNG SAU 8 NĂM",
     "range": "10/2018 → 10/2026", "drawAt": [4, "tám"], "until": [7, "bốn."],
     "series": [{"key": "deposit", "rates": ROLL, "label": "TIẾT KIỆM CUỘN 12 THÁNG", "color": UP},
                {"key": "vnindex", "label": "VN-INDEX (CHƯA GỒM CỔ TỨC)", "color": BLUE},
                {"key": "sjc", "interp": True, "label": "VÀNG MIẾNG SJC", "color": GOLD}],
     "source": "DỮ LIỆU: HOSE, SJC (QUA VNSTOCK) · TIẾT KIỆM: MỨC 12 THÁNG NH LỚN TỪNG NĂM, CUỘN MỖI THÁNG 10 (ƯỚC TÍNH) · MINH HOẠ"},
    {"type": "question", "at": 8, "text": "Vàng thắng đậm,\nsao còn ai gửi tiết kiệm?"},
    {"type": "kinetic", "at": 9, "items": [{"text": "CON ĐƯỜNG RẤT KHÁC NHAU", "at": [9, "đường"], "acc": True}]},
    {"type": "candles", "at": 10, "series": "vnindex", "from": "2018-10-08", "to": "2026-10-06", "drawAt": [10, "Trên"],
     "until": [10, "rơi"], "title": "VN-INDEX · 8 NĂM", "range": "10/2018 – 10/2026", "ind": [],
     "marks": [{"date": "2020-03-24", "text": "Đại dịch: 659", "pos": "below", "tone": "down", "at": [10, "dịch,"], "dx": 120, "dy": 20},
               {"date": "2022-11-15", "text": "2022: −40% từ đỉnh", "pos": "below", "tone": "down", "at": [10, "hai"], "dx": 60, "dy": 10}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "VÀNG 2026: −26% TỪ ĐỈNH", "at": [11, "Vàng"], "acc": True},
                                           {"text": "trong khoảng tám tháng", "at": [11, "tám"], "sm": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "TIẾT KIỆM: GẦN NHƯ ĐƯỜNG THẲNG", "at": [12, "Còn"], "acc": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "VÀNG LÚC NÀO CŨNG THẮNG?", "at": [13, "thắng"], "acc": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "09/2011 → 12/2015", "at": [14, "Từ"], "sm": True},
                                           {"text": "VÀNG THẾ GIỚI ≈ −45%", "at": [14, "bốn"], "acc": True},
                                           {"text": "GẦN 9 NĂM MỚI VƯỢT LẠI ĐỈNH", "at": [14, "vượt"]}]},
    {"type": "slam", "at": 15, "text": "QUÁ KHỨ ≠ TƯƠNG LAI", "sub": "VỚI BẤT KỲ KÊNH NÀO"},
    {"type": "kinetic", "at": 16, "items": [{"text": "TĂNG NHIỀU ⇄ RƠI SÂU", "at": [16, "tăng"], "acc": True},
                                           {"text": "thời gian giữ tiền quan trọng không kém chỗ để tiền", "at": [16, "thời"], "sm": True}]},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "VẬY TIỀN CỦA BẠN THÌ SAO?"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "VẬY TIỀN CỦA BẠN\nTHÌ SAO?", "sub": "5 CÂU TỰ HỎI", "titleAt": [0, "Mình"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "5 CÂU TỰ HỎI", "at": [1, "năm"], "acc": True},
                                          {"text": "không phải lời khuyên mua bán", "at": [1, "quyết"], "sm": True}]},
    {"type": "ledger", "at": 2, "title": "TRƯỚC KHI ĐẶT TIỀN", "rows": [
        {"k": "01", "v": "ĐÃ CÓ QUỸ KHẨN CẤP?", "at": [2, "quỹ"]},
        {"k": "02", "v": "BAO LÂU NỮA CẦN DÙNG?", "at": [3, "bao"]},
        {"k": "03", "v": "GIẢM 30% CÓ PHẢI BÁN?", "at": [4, "giảm"]},
        {"k": "04", "v": "HIỂU THỨ MÌNH ĐANG MUA?", "at": [5, "hiểu"]},
        {"k": "05", "v": "VƯỢT HẠN MỨC BẢO HIỂM?", "at": [6, "hạn"]}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHI NÀO ĐIỀU NÀY", "at": [7, "những"]},
                                          {"text": "KHÔNG ĐÚNG VỚI BẠN?", "at": [7, "đúng"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "ĐANG VAY LÃI CAO", "at": [8, "vay"]},
                                          {"text": "LÃI TĂNG = TIN XẤU", "at": [8, "xấu"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "MUA VÀNG TỪ LÂU", "at": [9, "vàng"]},
                                          {"text": "CHẶNG DÀI VẪN XANH", "at": [9, "chặng"], "acc": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "XEM LẠI VÀO NĂM SAU?", "at": [10, "Và"]},
                                           {"text": "BỨC TRANH CÓ THỂ ĐẢO NGƯỢC", "at": [10, "đảo"], "acc": True}]},
    {"type": "broll", "at": 11, "vid": "34081856", "veil": 0.5, "illus": "VIDEO MINH HỌA",
     "kin": [{"text": "TIỀN ĐỂ DÀNH CHỮNG LẠI", "at": [11, "chững"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "BẠN KHÔNG ĐƠN ĐỘC", "at": [12, "Nếu"], "acc": True},
                                           {"text": "và đó không phải lỗi của bạn", "at": [12, "lỗi"], "sm": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "MỖI TUẦN · 1 CÂU HỎI TIỀN BẠC", "at": [13, "tuần"], "acc": True},
                                           {"text": "để dữ liệu trả lời", "at": [13, "dữ"], "sm": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "TUẦN SAU · BÀI 1 · CHỨNG KHOÁN TỪ SỐ 0", "at": [14, "Tuần"], "acc": True},
                                           {"text": "VN-Index đứng yên, sao tài khoản vẫn lỗ?", "at": [14, "đứng"], "sm": True}]},
    {"type": "question", "at": 15, "text": "Năm nay bạn đang cất tiền ở đâu,\nvà bạn thấy thế nào?"},
]}

TITLE = "Năm 2026: Chứng Khoán, Vàng, Coin, Nhà Đất Đều Đỏ — Chỉ Sổ Tiết Kiệm Xanh. Nhưng Thắng Thật Không?"
SPEC = {
    "title": TITLE, "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20,
    "acc": ["vn-index", "sjc", "bitcoin", "vàng", "tiết", "kiệm", "lạm", "phát", "thắng", "đỏ", "xanh"],
    "say": SAY, "imgs": {}, "chapters": list(CH),
    "youtube": {
        "titles": [TITLE, "Năm 2026 Ai Cũng Thấy Nghèo Đi? Dữ Liệu Nói Gì Về Tiền Của Bạn",
                   "100 Triệu Chia 5 Kênh Đầu Tư Năm 2026: Chỉ Một Kênh Còn Xanh"],
        "summary": "Đầu năm 2026, chia 100 triệu cho 5 kênh: chứng khoán, vàng miếng, Bitcoin, nhà đất, tiết kiệm. Chín tháng sau, "
                   "chỉ cuốn sổ tiết kiệm còn xanh — nhưng sau lạm phát, nó thắng thật không? Dữ liệu thật, giải thích dễ hiểu.",
        "more": ["Nội dung giáo dục, không phải tư vấn đầu tư hay tư vấn tài chính cá nhân. Không khuyến nghị mua/bán bất kỳ "
                 "tài sản nào. Ví dụ dùng dữ liệu quá khứ; quá khứ không đảm bảo tương lai. Nội dung do kênh biên soạn từ nguồn "
                 "công khai; giọng đọc tổng hợp."],
        "chapter_titles": {"ch00": "Mở đầu: 100 triệu, năm kênh, một năm", "ch01": "Chứng khoán: đứng yên mà đi một vòng",
                           "ch02": "Vàng: từ hàng dài xếp hàng đến 51 triệu", "ch03": "Coin và nhà đất: hai kiểu đỏ",
                           "ch04": "Sổ tiết kiệm thắng — nhưng thắng thật không?", "ch05": "Một năm khác mười năm",
                           "ch06": "Kết: vậy tiền của bạn thì sao?"},
        "sources": [
            "Tổng cục Thống kê (NSO) — CPI tháng 9 và 9 tháng 2026: https://www.nso.gov.vn/wp-content/uploads/2026/10/Tong-quan-CPI-chi-so-gia-vang-do-la-My-thang-9-QIII-va-9-thang-nam-2026.pdf",
            "Bộ Xây dựng qua Báo Chính phủ — thị trường BĐS quý II/2026",
            "Tuổi Trẻ 30/09/2026 — Kênh đầu tư: VND đang 'sáng' hơn đất, vàng, chứng khoán: https://tuoitre.vn/kenh-dau-tu-vnd-dang-sang-hon-dat-vang-chung-khoan-100260930194210942.htm",
            "Bảo hiểm tiền gửi Việt Nam — hạn mức 350 triệu từ 13/07/2026 (TT 05/2026/TT-NHNN)",
            "Dữ liệu VN-Index: HOSE, vàng SJC: sjc.com.vn (truy xuất qua Vnstock); Bitcoin: CoinGecko",
            "Hồ sơ dữ kiện đầy đủ (147 nguồn) do kênh lưu trữ; liên hệ qua bình luận nếu cần nguồn cụ thể.",
        ],
        "hashtags": ["TàiChínhCáNhân", "GửiTiếtKiệm", "GiáVàng", "VNIndex", "BiểuĐồBiếtNói"],
        "tags": ["tài chính cá nhân", "gửi tiết kiệm", "lãi suất tiết kiệm 2026", "giá vàng 2026", "vàng miếng SJC", "VN-Index 2026",
                 "chứng khoán 2026", "bitcoin 2026", "bất động sản 2026", "lạm phát 2026", "kênh đầu tư 2026", "nên để tiền ở đâu"],
        "category": "27", "thumb": "t1.jpg",
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
    print("spec + %d chương" % len(CH))
