"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK C4 "Đường Trung Bình Động (MA) Là Gì?".

    python data/long/ck-c4-duong-trung-binh/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (đã kiểm chứng vòng 1). Số liệu: analysis.py -> results.json (kênh tự tính, VN-Index vnstock/VCI).
Luật kênh: chỉ giáo dục; KHÔNG nói VN-Index hiện trên/dưới MA nào; phép thử quy tắc = minh hoạ trên chỉ số, ghi "KÊNH TỰ TÍNH · QUÁ KHỨ ·
KHÔNG PHẢI TÍN HIỆU". beat2 bật. BƯỚC 1: chỉ spec để thu giọng; scenes viết sau khi có timing.json.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C3 = json.loads((D.parent / "ck-c3-bieu-do-nen" / "spec.json").read_text(encoding="utf-8"))
SAY = {**C3["say"], "ma": "em a", "moving": "mu-vinh", "average": "e-vơ-rịt", "brock": "Brốc", "lakonishok": "La-cô-ni-sốc",
       "lebaron": "Lơ-ba-rông", "sullivan": "Xu-li-vần", "timmermann": "Tim-mơ-man", "white": "Oai", "dow": "Đao", "jones": "Giôn",
       "ema": "i em a"}

R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, VIOLET, UP, DOWN = "#38bdf8", "#fbbf24", "#a78bfa", "#22c55e", "#ef4444"
SELF = "KÊNH TỰ TÍNH · QUÁ KHỨ · KHÔNG PHẢI TÍN HIỆU"
DATA = "DỮ LIỆU: HOSE (VNSTOCK/VCI), KÊNH TỰ TÍNH. MINH HOẠ QUÁ KHỨ, KHÔNG PHẢI KHUYẾN NGHỊ."
VM = "VIDEO MINH HỌA"
MA20, MA50, MA200 = {"k": "sma", "n": 20, "color": BLUE}, {"k": "sma", "n": 50, "color": VIOLET}, {"k": "sma", "n": 200, "color": GOLD}
S = R["sensitivity"]
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "ĐƯỜNG KẺ ĐẾN SAU"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "candles", "series": "vnindex", "from": "2021-11-01", "to": "2022-04-29", "drawAt": [0, None, 0, 0.1], "until": [1, "chu"],
     "title": "VN-INDEX · KHUNG NGÀY", "range": "11/2021 → 04/2022", "ind": [],
     "marks": [{"date": "2022-01-06", "text": "ĐỈNH 1.528,57", "at": [0, "đóng"], "pos": "above", "tone": "gold"}], "source": DATA},
    {"type": "quote", "at": 3, "text": "Giá thủng đường MA hai trăm là phải chạy.", "by": "LỜI TRUYỀN MIỆNG", "dy": True, "qline": 3},
    {"type": "kinetic", "at": 4, "items": [{"text": "MA200", "at": 4, "acc": True}, {"text": "trung bình 200 phiên gần nhất", "at": [4, "trung"], "sm": True}]},
    {"type": "question", "at": 5, "text": "Lần ấy, giá thủng\nMA200 lúc nào?"},
    {"type": "candles", "at": 6, "series": "vnindex", "from": "2021-11-01", "to": "2022-04-29", "drawAt": [6, None, 0, 0.1], "until": [6, "tư"],
     "title": "VN-INDEX + MA200", "range": "11/2021 → 04/2022", "ind": [dict(MA200, at=[6, "ngày"])],
     "marks": [{"date": "2022-01-06", "text": "ĐỈNH", "at": [6, "ngày"], "pos": "above", "tone": "gold"},
               {"date": "2022-04-19", "text": "THỦNG MA200 · 19/04", "at": [6, "tư"], "pos": "below", "tone": "down"}], "source": DATA},
    {"type": "kinetic", "at": 7, "items": [{"text": "+67 PHIÊN", "at": 7, "acc": True}, {"text": "−8% từ đỉnh", "at": [7, "tám"]}]},
    {"type": "slam", "at": 8, "text": "NÓ CHỈ ĐẾN SAU", "sub": "ĐƯỜNG KẺ KHÔNG SAI"},
    {"type": "kinetic", "at": 10, "items": [{"text": "TRUNG BÌNH CỦA NGÀY ĐÃ QUA", "at": 10}, {"text": "NGÀY MAI?", "at": 11, "acc": True}]},
    {"type": "brand", "at": 13, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 14, "items": [{"text": "CHỨNG KHOÁN TỪ SỐ 0 · BÀI 4", "at": 14, "acc": True}, {"text": "chỉ giáo dục · không khuyên mua/bán · không dự báo", "at": 15, "sm": True}]},
]}

W5 = R["window5"]
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "ĐIỂM TRUNG BÌNH HỌC KỲ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "ĐIỂM TRUNG BÌNH\nHỌC KỲ", "sub": "MA = MOVING AVERAGE", "vid": "7140937", "illus": VM, "titleAt": [0, "hồi"]},
    {"type": "ledger", "at": 1, "title": "ĐIỂM KIỂM TRA · VÍ DỤ GIẢ ĐỊNH", "srcnote": "VÍ DỤ GIẢ ĐỊNH",
     "rows": [{"k": "1 BÀI KÉM", "v": "TB GẦN NHƯ KHÔNG ĐỔI", "at": 1}, {"k": "KÉM LIÊN TỤC", "v": "TB ĐI XUỐNG DẦN", "at": 2}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "MA", "at": 4, "acc": True}, {"text": "moving average · trung bình trượt", "at": [4, "moving"], "sm": True}]},
    {"type": "ledger", "at": 6, "title": "MA5 · TÍNH TAY BẰNG SỐ THẬT", "srcnote": "VN-INDEX ĐÓNG CỬA · " + SELF,
     "rows": [{"k": x["date"][8:] + "/" + x["date"][5:7], "v": f'{x["close"]:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), "at": 7}
              for x in W5[:5]],
     "total": {"k": "÷ 5", "v": "≈ 1.512", "at": 9}},
    {"type": "kinetic", "at": 10, "items": [{"text": "1 ĐIỂM TRÊN MA5", "at": 10, "acc": True}, {"text": "đặt ở ngày 06/01/2022", "at": [10, "đặt"], "sm": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "BỎ PHIÊN CŨ NHẤT", "at": 11}, {"text": "THÊM PHIÊN MỚI NHẤT", "at": [11, "thêm"], "acc": True}]},
    {"type": "candles", "at": 12, "series": "vnindex", "from": "2021-12-01", "to": "2022-01-31", "drawAt": [12, None, 0, 0.1], "until": [13, "nối"],
     "title": "VN-INDEX + MA5", "range": "12/2021 → 01/2022", "ind": [{"k": "sma", "n": 5, "color": BLUE, "at": [13, "nối"]}], "source": DATA},
    {"type": "question", "at": 14, "text": "MA20, MA50, MA200\nkhác nhau ở đâu?"},
    {"type": "ledger", "at": 15, "title": "CHỈ KHÁC ĐỘ RỘNG CỬA SỔ", "rows": [{"k": "MA20", "v": "≈ 1 THÁNG GIAO DỊCH", "at": 16},
                                                                          {"k": "MA200", "v": "≈ GẦN 1 NĂM", "at": [16, "hai"]}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "20 · 50 · 200", "at": 17, "acc": True}, {"text": "23? 187?", "at": [17, "chứ"]}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "ĐỊNH LUẬT", "at": 18, "fx": "strike", "strikeAt": [18, "đó"]}, {"text": "THÓI QUEN", "at": [18, "quen"], "acc": True}]},
    {"type": "ledger", "at": 20, "title": "HAI CÁCH ĐỌC MỘT ĐƯỜNG MA", "rows": [{"k": "1", "v": "ĐỘ DỐC: LÊN · NGANG · XUỐNG", "at": 21},
                                                                             {"k": "2", "v": "GIÁ TRÊN HAY DƯỚI · CÁCH BAO XA", "at": 22}]},
    {"type": "kinetic", "at": 23, "items": [{"text": "CỬA SỔ RỘNG", "at": 23, "sm": True}, {"text": "MƯỢT HƠN · CHẬM HƠN", "at": [23, "mượt"], "acc": True}]},
]}

P, T = R["peak2022"], R["trough2022"]
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "MƯỢT NHƯNG CHẬM"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "MƯỢT\nNHƯNG CHẬM", "sub": "MA20 · MA50 · MA200 · NĂM 2022", "vid": "1085656", "illus": VM, "titleAt": [0, "hãy"]},
    {"type": "candles", "at": 1, "series": "vnindex", "from": "2021-11-01", "to": "2023-07-31", "drawAt": [1, None, 0, 0.1], "until": [2, "phẳng"],
     "title": "VN-INDEX + MA20 · MA50 · MA200", "range": "11/2021 → 07/2023",
     "ind": [dict(MA20, at=[1, "bám"]), dict(MA50, at=[1, "uốn"]), dict(MA200, at=[2, "thoai"])], "source": DATA},
    {"type": "bars", "at": 3, "title": "SAU ĐỈNH 06/01/2022: BAO NHIÊU PHIÊN GIÁ MỚI THỦNG?",
     "items": [{"k": "MA20", "v": P["ma20"]["sessions"], "lbl": f'{P["ma20"]["sessions"]} phiên · −5%', "at": 3},
               {"k": "MA50", "v": P["ma50"]["sessions"], "lbl": f'{P["ma50"]["sessions"]} phiên · −5%', "at": [3, "năm"]},
               {"k": "MA200", "v": P["ma200"]["sessions"], "lbl": f'{P["ma200"]["sessions"]} phiên · −8%', "at": 4, "acc": True}],
     "label": {"k": "", "v": SELF, "at": 3}},
    {"type": "bars", "at": 5, "title": "SAU ĐÁY 15/11/2022: BAO NHIÊU PHIÊN GIÁ MỚI VƯỢT LÊN?",
     "items": [{"k": "MA20", "v": T["ma20"]["sessions"], "lbl": f'{T["ma20"]["sessions"]} phiên · +10%', "at": 6},
               {"k": "MA50", "v": T["ma50"]["sessions"], "lbl": f'{T["ma50"]["sessions"]} phiên · +15%', "at": 7},
               {"k": "MA200", "v": T["ma200"]["sessions"], "lbl": f'{T["ma200"]["sessions"]} phiên · +18%', "at": 8, "acc": True}],
     "label": {"k": "", "v": SELF, "at": 5}},
    {"type": "kinetic", "at": 9, "items": [{"text": "ĐỘ DỐC MA200", "at": 9, "acc": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "VẪN CẮM ĐẦU", "at": 10, "acc": True}, {"text": "thêm hơn 7 tháng sau đáy", "at": [10, "thêm"], "sm": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "17/07/2023", "at": 11, "acc": True}, {"text": "165 phiên sau đáy · mới ngóc lên", "at": [11, "một"], "sm": True}]},
    {"type": "slam", "at": 12, "text": "ĐÁY Ở RẤT XA PHÍA SAU"},
    {"type": "kinetic", "at": 14, "items": [{"text": "TÍNH TỪ NGÀY ĐÃ QUA", "at": 14}, {"text": "→ LUÔN ĐI SAU GIÁ", "at": [14, "nên"], "acc": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "200 PHIÊN ≈ 1 NĂM QUÁ KHỨ", "at": 15, "acc": True}, {"text": "vài tuần chưa đủ kéo nó đổi hướng", "at": [15, "một"], "sm": True}]},
    {"type": "question", "at": 17, "text": "MA biết gì\nvề ngày mai?"},
    {"type": "slam", "at": 18, "text": "KHÔNG GÌ CẢ", "sub": "NÓ TÓM TẮT QUÁ KHỨ CHO GỌN"},
    {"type": "kinetic", "at": 20, "items": [{"text": "CHẬM VẬY SAO VẪN DÙNG?", "at": 20}, {"text": "NHANH HƠN = SAI NHIỀU HƠN", "at": 21, "acc": True}]},
]}

RM = R["rule_ma200"]
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CẮT GIẢ"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CẮT GIẢ", "sub": "KHI ĐƯỜNG KẺ BÁO ĐỘNG NHẦM", "vid": "5467579", "illus": VM, "titleAt": [0, "muốn"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "CỬA SỔ NGẮN", "at": 1, "sm": True}, {"text": "NHẠY VỚI NHIỄU", "at": [1, "nhạy"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "KÊNH ĐẾM · MA200 · 07/2019 → 10/2026", "srcnote": SELF,
     "rows": [{"k": "ĐỔI PHÍA", "v": f'{RM["flips"]} LẦN', "at": 4}, {"k": "ĐỔI LẠI ≤ 10 PHIÊN", "v": f'{RM["fake_flips_le10"]} LẦN', "at": 5}]},
    {"type": "slam", "at": 6, "text": "CẮT GIẢ", "sub": f'{RM["fake_flips_le10"]}/{RM["flips"]} LẦN ĐỔI PHÍA · ' + SELF},
    {"type": "candles", "at": 7, "series": "vnindex", "from": "2019-10-01", "to": "2020-03-31", "drawAt": [7, None, 0, 0.1], "until": [10, "rơi"],
     "title": "VN-INDEX + MA200 · TRƯỚC DỊCH", "range": "10/2019 → 03/2020", "ind": [dict(MA200, at=[7, "ví"])],
     "marks": [{"date": "2019-11-25", "text": "THỦNG", "at": 8, "pos": "below", "tone": "down"},
               {"date": "2020-01-20", "text": "VƯỢT LẠI", "at": 9, "pos": "above", "tone": "up"},
               {"date": "2020-01-31", "text": "THỦNG · 9 PHIÊN SAU", "at": 10, "pos": "below", "tone": "down"}], "source": DATA},
    {"type": "kinetic", "at": 11, "items": [{"text": "BÁO ĐỘNG GIẢ", "at": 11}, {"text": "HAY THẬT?", "at": [11, "thật"], "acc": True},
                                           {"text": "đường kẻ không cho biết trước", "at": 12, "sm": True}]},
    {"type": "ledger", "at": 13, "title": "MỖI LẦN CẮT GIẢ", "rows": [{"k": "1", "v": "BÁN → MUA LẠI GIÁ CAO HƠN", "at": 13},
                                                                     {"k": "2", "v": "+ PHÍ GIAO DỊCH · + THUẾ KHI BÁN", "at": 14}]},
    {"type": "candles", "at": 15, "series": "vnindex", "from": "2022-01-03", "to": "2023-07-31", "drawAt": [15, None, 0, 0.1], "until": [16, "xuống"],
     "title": "DƯỚI MA200 · 279 PHIÊN LIỀN", "range": "19/04/2022 → 31/05/2023", "ind": [dict(MA200, at=[15, "dưới"])], "source": DATA},
    {"type": "kinetic", "at": 17, "items": [{"text": "CHỈ THẤY KHI ĐÃ ĐI MỘT ĐOẠN", "at": 17, "acc": True}, {"text": "không phân biệt trước thật / giả", "at": [17, "không"], "sm": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "THỊ TRƯỜNG ĐI NGANG", "at": 18, "acc": True}, {"text": "giá lắc lư quanh đường trung bình", "at": [18, "giá"], "sm": True}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "LÚC TIN ĐƯỜNG KẺ NHẤT", "at": 20}, {"text": "= LÚC NÓ SAI NHIỀU NHẤT", "at": [20, "vì"], "acc": True}]},
]}

pct = lambda x: f"+{x:.0f}%".replace(".", ",")
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "BẮN TÊN RỒI VẼ HỒNG TÂM"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "BẮN TÊN\nRỒI VẼ HỒNG TÂM", "sub": "KÊNH THỬ 6 ĐỘ DÀI MA", "vid": "5028622", "illus": VM, "titleAt": [0, "có"]},
    {"type": "ledger", "at": 1, "title": "QUY TẮC MINH HOẠ", "srcnote": "TRÊN CHỈ SỐ · KHÔNG MUA TRỰC TIẾP ĐƯỢC · QUÁ KHỨ",
     "rows": [{"k": "TRÊN MA", "v": "GIỮ CHỈ SỐ", "at": [1, "trên"]}, {"k": "DƯỚI MA", "v": "ĐỨNG NGOÀI (LÃI 0)", "at": [1, "dưới"]}]},
    {"type": "bars", "at": 3, "title": "10/2019 → 10/2026 · TRƯỚC PHÍ VÀ THUẾ",
     "items": [{"k": "GIỮ SUỐT", "v": S["hold_pct"], "lbl": pct(S["hold_pct"]), "at": 3},
               {"k": "MA200", "v": S["ma200"]["no_cost"], "lbl": pct(S["ma200"]["no_cost"]), "at": 4, "acc": True}],
     "label": {"k": "", "v": SELF, "at": 3}},
    {"type": "slam", "at": 5, "text": "NGHE HẤP DẪN"},
    {"type": "bars", "at": 6, "title": "SÁU ĐỘ DÀI MA · TRƯỚC PHÍ → SAU PHÍ VÀ THUẾ",
     "items": [{"k": "GIỮ SUỐT", "v": S["hold_pct"], "lbl": pct(S["hold_pct"]), "at": 6}] +
              [{"k": f"MA{n}", "v": S[f"ma{n}"]["with_cost"], "lbl": f'{pct(S[f"ma{n}"]["no_cost"])} → {pct(S[f"ma{n}"]["with_cost"])}',
                "at": a, **({"acc": True} if n == 200 else {})}
               for n, a in ((20, 8), (50, 7), (100, 6), (150, 9), (200, 9), (250, 9))],
     "label": {"k": "PHÍ GIẢ ĐỊNH", "v": "0,15%/CHIỀU + THUẾ BÁN 0,1% · " + SELF, "at": 7}},
    {"type": "kinetic", "at": 10, "items": [{"text": "CHỈ BIẾT SAU KHI", "at": 10, "sm": True}, {"text": "ĐÃ NHÌN HẾT DỮ LIỆU", "at": [10, "đã"], "acc": True}]},
    {"type": "slam", "at": 11, "text": "BẮN TÊN TRƯỚC", "sub": "RỒI VẼ HỒNG TÂM QUANH MŨI TÊN"},
    {"type": "kinetic", "at": 12, "items": [{"text": "ĐÀO DỮ LIỆU", "at": 12, "acc": True}, {"text": "data snooping", "at": [12, "đào"], "sm": True}]},
    {"type": "file", "at": 13, "k": "JOURNAL OF FINANCE · 1992", "name": "Brock, Lakonishok, LeBaron", "desc": "Dow Jones 1897–1986",
     "rows": [{"k": "QUY TẮC", "v": "đường trung bình · phá vùng giá", "at": [13, "thử"]}, {"k": "KẾT QUẢ", "v": "*khá tốt* · chưa tính phí", "at": [13, "thấy"]}]},
    {"type": "file", "at": 14, "k": "JOURNAL OF FINANCE · 1999", "name": "Sullivan, Timmermann, White", "desc": "Kiểm tra lại, tính tới đào dữ liệu",
     "rows": [{"k": "SỐ QUY TẮC", "v": "*7.846*", "at": [14, "gần"]}, {"k": "1987–1996", "v": "*hầu như không* còn giá trị kinh tế", "at": 15}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "VẬY MA DÙNG ĐỂ LÀM GÌ"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "VẬY MA\nDÙNG ĐỂ LÀM GÌ", "sub": "VÀ KHI NÀO NÓ SAI", "vid": "7914862", "illus": VM, "titleAt": [0, "ma"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "QUẢ CẦU PHA LÊ", "at": 1, "fx": "strike", "strikeAt": [1, "tóm"]}, {"text": "MỘT CÁCH TÓM TẮT", "at": [1, "tóm"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "MA DÙNG ĐỂ", "rows": [{"k": "1", "v": "LỌC BỚT NHIỄU · THẤY HƯỚNG CHUNG", "at": 2},
                                                             {"k": "2", "v": "MỘT MỐC ĐỂ TỰ HỎI: XA HAY GẦN, BAO LÂU", "at": 4}]},
    {"type": "question", "at": 6, "text": "Khi nào\nnó dễ sai?"},
    {"type": "ledger", "at": 7, "title": "MA DỄ SAI KHI", "rows": [{"k": "1", "v": "THỊ TRƯỜNG ĐI NGANG · CẮT GIẢ", "at": 7},
                                                                {"k": "2", "v": "CÚ SỐC: 03/04/2025 · −6,68%", "at": 8},
                                                                {"k": "3", "v": "CHỌN ĐỘ DÀI SAU KHI NHÌN KẾT QUẢ", "at": 10}]},
    {"type": "ledger", "at": 11, "title": "3 CÂU TỰ HỎI TRƯỚC KHI TIN MỘT ĐƯỜNG KẺ",
     "rows": [{"k": "1", "v": "BAO NHIÊU PHIÊN · VÌ SAO CON SỐ ẤY?", "at": 12}, {"k": "2", "v": "MỖI NĂM ĐỔI PHÍA MẤY LẦN · MẤT BAO NHIÊU PHÍ?", "at": 13},
              {"k": "3", "v": "NGƯỜI KHOE ĐÃ THỬ BAO NHIÊU QUY TẮC KHÁC?", "at": 14}]},
    {"type": "question", "at": 15, "text": "Bạn hay thấy đường MA nào\nđược nhắc nhiều nhất?"},
    {"type": "kinetic", "at": 16, "items": [{"text": "BÀI SAU", "at": 16, "sm": True}, {"text": "EMA: NHANH HƠN THẬT KHÔNG?", "at": [16, "ema"], "acc": True}]},
]}

SPEC = {
    "title": "Đường Trung Bình Động MA Là Gì? Một Đường Kẻ Tóm Tắt Quá Khứ, Và Điều Nó Không Biết",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["vn-index", "ma", "trung", "bình", "trễ", "giả"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(6)],
    "youtube": {
        "titles": ["Đường Trung Bình Động MA Là Gì? Một Đường Kẻ Tóm Tắt Quá Khứ, Và Điều Nó Không Biết",
                   "MA200 \"Thủng Là Bán\"? Kênh Thử Trên 7 Năm VN-Index",
                   "MA Cho Người Mới: Tính Tay, Đọc Đúng, Và Vì Sao Nó Luôn Đến Muộn"],
        "summary": "Đường trung bình động (MA) là đường kẻ gần như phần mềm biểu đồ nào cũng vẽ. Video tính tay một đường MA5 bằng giá VN-Index "
                   "thật, đo độ trễ của MA20, MA50, MA200 ở đỉnh và đáy năm 2022, đếm số lần \"cắt giả\", và thử một quy tắc đơn giản với sáu độ "
                   "dài MA khác nhau — để thấy kết quả thay đổi thế nào khi bạn chọn con số sau khi đã biết kết quả. Bài 4 khoá Chứng khoán từ số 0.",
        "more": [C3["youtube"]["more"][0],
                 "📐 CÁCH KÊNH TÍNH (quá khứ, không phải tín hiệu): VN-Index đóng cửa 08/10/2018–06/10/2026 (HOSE qua vnstock/VCI). Quy tắc minh hoạ: "
                 "đóng cửa hôm trước trên MA thì giữ chỉ số, dưới thì đứng ngoài (lãi 0); phí giả định 0,15%/chiều + thuế bán 0,1%; không cổ tức. "
                 "Một chỉ số, một giai đoạn, sáu độ dài chọn sẵn — minh hoạ cơ chế trễ và cắt giả, KHÔNG phải bằng chứng quy tắc tốt hay xấu."],
        "chapter_titles": {"ch00": "Mở đầu: đường kẻ đến sau (đỉnh 01/2022)", "ch01": "Điểm trung bình học kỳ: tính tay MA5",
                           "ch02": "Mượt nhưng chậm: MA20, MA50, MA200", "ch03": "Cắt giả", "ch04": "Bắn tên rồi vẽ hồng tâm: kênh thử 6 độ dài MA",
                           "ch05": "Vậy MA dùng để làm gì, và khi nào sai"},
        "sources": ["https://doi.org/10.1111/j.1540-6261.1992.tb04681.x", "https://doi.org/10.1111/0022-1082.00163",
                    "https://www.fmg.ac.uk/publications/discussion-papers/data-snooping-technical-trading-rule-performance-and-bootstrap"],
        "hashtags": ["ChứngKhoán", "MA", "ChứngKhoánTừSố0", "PhânTíchKỹThuật", "BiểuĐồBiếtNói"],
        "tags": ["đường trung bình động", "MA là gì", "MA200", "MA20", "moving average", "chứng khoán cho người mới", "phân tích kỹ thuật",
                 "VN-Index", "cắt giả", "backtest", "đào dữ liệu"],
        "category": C3["youtube"]["category"], "data_credit": C3["youtube"].get("data_credit"), "thumb": "t1.jpg",
        "video_credits": C3["youtube"]["video_credits"],
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
