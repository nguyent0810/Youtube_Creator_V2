"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK E1 "Mua Đều Mỗi Tháng".

    python data/long/ck-e1-mua-deu-moi-thang/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Số liệu: analysis.py -> results.json (kênh tự tính, VN-Index vnstock/VCI). Luật kênh: chỉ giáo dục; "mua theo chỉ
số" = minh hoạ cơ chế; ghi "KÊNH TỰ TÍNH · QUÁ KHỨ · KHÔNG PHẢI KHUYẾN NGHỊ". Ba nhân vật là giả định. beat2 bật.
Chuẩn phối 12/10/2026: ưu tiên cảnh số liệu (bars / race / candles / counter / ledger) và cảnh quay, cảnh thuần chữ ở mức thấp.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = {**C4["say"], "dollar": "đô-la", "cost": "cót", "averaging": "e-vơ-rịt-ging", "vanguard": "Van-gát"}

R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444"
SELF = "KÊNH TỰ TÍNH · QUÁ KHỨ · KHÔNG PHẢI KHUYẾN NGHỊ"
HYPO = "MINH HOẠ TRÊN CHỈ SỐ · KHÔNG PHÍ, THUẾ, CỔ TỨC · " + SELF
DATA = "DỮ LIỆU: VN-INDEX (VNSTOCK/VCI), KÊNH TỰ TÍNH. MINH HOẠ QUÁ KHỨ, KHÔNG PHẢI KHUYẾN NGHỊ."
VM = "VIDEO MINH HỌA"
PATH = R["path_monthly"]


def acc(m0: str, m1: str) -> dict:
    """Đường 'lãi/lỗ của tài khoản cô Đều so với tiền đã nộp' theo tháng, từ m0 tới m1 (YYYY-MM)."""
    seg = [p for p in PATH if m0 <= p["m"] <= m1]
    return {"dates": [p["m"] + "-01" for p in seg],
            "series": [{"label": "TÀI KHOẢN SO VỚI TIỀN ĐÃ NỘP", "color": GOLD, "vals": [round((p["value"] / p["paid"] - 1) * 100, 1) for p in seg]}]}


CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "TIN NHẮN NGÀY 24 THÁNG 3"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "day": "MỘT TIN NHẮN", "date": "24.03.2020"},
    {"type": "broll", "at": 1, "vid": "6466354", "veil": 0.5, "illus": VM,
     "kin": [{"text": "ĐIỆN THOẠI BÁO MỘT CON SỐ", "at": 1, "acc": True}]},
    {"type": "ledger", "at": 2, "title": "18 THÁNG · MỖI THÁNG 3 TRIỆU", "srcnote": "VÍ DỤ GIẢ ĐỊNH · " + HYPO,
     "rows": [{"k": "ĐÃ NỘP", "v": "54 TRIỆU", "at": 3}], "total": {"k": "TÀI KHOẢN CÒN", "v": "≈ 37 TRIỆU", "at": 4}},
    {"type": "counter", "at": 5, "from": 54000000, "to": 37200000, "suffix": " đ", "countAt": [5, "Mười"], "until": [5, "hơi"],
     "label": "17 TRIỆU ĐÃ BỐC HƠI", "sub": {"text": "≈ 6 THÁNG TIỀN ĐỂ DÀNH", "at": 6}},
    {"type": "kinetic", "at": 7, "items": [{"text": "TUẦN SAU", "at": 7, "sm": True}, {"text": "TỚI KỲ NỘP TIẾP", "at": [7, "tới"], "acc": True}]},
    {"type": "question", "at": 8, "text": "Bạn có nộp tiếp\n3 triệu nữa không?"},
    {"type": "kinetic", "at": 9, "items": [{"text": "GIỮ CÂU TRẢ LỜI", "at": 9, "acc": True},
                                          {"text": "cuối video: chuyện xảy ra sau ngày hôm đó", "at": [9, "Cuối"], "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "BA NHÂN VẬT GIẢ ĐỊNH", "at": [10, "ba"], "acc": True},
                                           {"text": "cùng một số tiền · trong đúng 8 năm", "at": 11, "sm": True}]},
    {"type": "ledger", "at": 12, "title": "BA NHÂN VẬT · CÙNG SỐ TIỀN · 8 NĂM", "srcnote": "NHÂN VẬT GIẢ ĐỊNH · " + SELF,
     "rows": [{"k": "CÔ ĐỀU", "v": "THÁNG NÀO CŨNG MUA", "at": 12}, {"k": "ANH XUI", "v": "MUA ĐÚNG NGÀY ĐẮT NHẤT NĂM", "at": 13},
              {"k": "CHỊ MAY", "v": "MUA ĐÚNG NGÀY RẺ NHẤT NĂM", "at": 14}]},
    {"type": "question", "at": 15, "text": "Ai về đích với bao nhiêu?\nAi mất ngủ nhiều nhất?"},
    {"type": "brand", "at": 16, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 17, "items": [{"text": "CHỈ NHẰM GIÁO DỤC", "at": 17, "acc": True},
                                           {"text": "không khuyên mua/bán · không dự báo thị trường", "at": [17, "không"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "LUẬT CHƠI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "LUẬT CHƠI", "sub": "MUA ĐỀU LÀ GÌ?", "vid": "13107027", "illus": VM, "titleAt": [0, "Trước"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "SỐ TIỀN CỐ ĐỊNH", "at": [1, "một"]}, {"text": "NGÀY CỐ ĐỊNH", "at": [1, "và"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "TỚI NGÀY LÀ MUA", "rows": [{"k": "GIÁ CAO", "v": "CŨNG MUA", "at": [2, "Giá"]},
                                                                    {"k": "GIÁ THẤP", "v": "CŨNG MUA", "at": [2, "thấp"]}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "dollar cost averaging", "at": [3, "dollar"], "sm": True}, {"text": "MUA ĐỀU", "at": [4, "mua"], "acc": True}]},
    {"type": "broll", "at": 5, "vid": "6282372", "veil": 0.5, "illus": VM,
     "kin": [{"text": "KHÔNG HẲN LÀ CHIẾN LƯỢC", "at": 5}, {"text": "LÀ HOÀN CẢNH", "at": 6, "acc": True},
             {"text": "lương về theo tháng · tiền để dành cũng về theo tháng", "at": [6, "Lương"], "sm": True}]},
    {"type": "ledger", "at": 7, "title": "LUẬT CHƠI CỦA PHÉP THỬ", "srcnote": HYPO,
     "rows": [{"k": "MỖI THÁNG", "v": "3 TRIỆU ĐỒNG", "at": 8}, {"k": "NGÀY MUA", "v": "PHIÊN ĐẦU THÁNG · GIÁ ĐÓNG CỬA", "at": [8, "mua"]},
              {"k": "GIAI ĐOẠN", "v": "10/2018 → 10/2026", "at": 9}, {"k": "SỐ LẦN MUA", "v": "97", "at": 10}],
     "total": {"k": "TỔNG NỘP", "v": "291 TRIỆU", "at": 11}},
    {"type": "ledger", "at": 12, "title": "3 ĐIỀU PHẢI NÓI RÕ", "srcnote": SELF,
     "rows": [{"k": "1", "v": "KHÔNG AI MUA TRỰC TIẾP ĐƯỢC MỘT CHỈ SỐ", "at": 13}, {"k": "2", "v": "CHƯA TÍNH PHÍ · THUẾ · CỔ TỨC", "at": 14},
              {"k": "3", "v": "MỘT CHỈ SỐ · MỘT GIAI ĐOẠN", "at": 15}]},
    {"type": "race", "at": 16, "from": "2018-10-08", "to": "2026-10-06", "title": "VN-INDEX · 8 NĂM", "range": "08/10/2018 → 06/10/2026",
     "drawAt": [16, None, 0, 0.05], "until": [16, "khoảng"], "series": [{"key": "vnindex", "label": "VN-INDEX", "color": BLUE}], "source": DATA},
    {"type": "kinetic", "at": 18, "items": [{"text": "ĐƯỜNG ĐI Ở GIỮA", "at": 18}, {"text": "KHÔNG HỀ THẲNG", "at": [18, "không"], "acc": True}]},
]}

M = R["mechanism"]
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "CÔ ĐỀU VỀ ĐÍCH"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "CÔ ĐỀU\nVỀ ĐÍCH", "sub": "97 LẦN MUA · KHÔNG SÓT THÁNG NÀO", "vid": "7710771", "illus": VM,
     "titleAt": [0, "Mình"]},
    {"type": "counter", "at": 1, "from": 0, "to": 97, "suffix": " LẦN MUA", "until": [1, "mua"], "label": "KHÔNG SÓT THÁNG NÀO", "sub": {"text": HYPO, "at": 1}},
    {"type": "bars", "at": 2, "title": "CÔ ĐỀU · SAU 8 NĂM (TRIỆU ĐỒNG)",
     "items": [{"k": "ĐÃ NỘP VÀO", "v": 291, "lbl": "291", "at": 2}, {"k": "TÀI KHOẢN 10/2026", "v": 437, "lbl": "≈ 437", "at": [3, "bốn"], "acc": True}],
     "label": {"k": "", "v": SELF, "at": 2}},
    {"type": "kinetic", "at": 4, "items": [{"text": "+146 TRIỆU", "at": 4, "acc": True}, {"text": "≈ +50% trên tổng tiền đã nộp", "at": 5, "sm": True}]},
    {"type": "question", "at": 6, "text": "Chỉ số +77%,\nsao cô ấy chỉ +50%?"},
    {"type": "ledger", "at": 7, "title": "MỖI KHOẢN 3 TRIỆU ĐƯỢC HƯỞNG BAO LÂU?", "srcnote": "TIỀN KHÔNG NẰM TRONG THỊ TRƯỜNG NGAY TỪ ĐẦU",
     "rows": [{"k": "KHOẢN ĐẦU TIÊN", "v": "TRỌN 8 NĂM", "at": 8}, {"k": "KHOẢN CUỐI CÙNG", "v": "VÀI NGÀY", "at": [8, "Còn"]}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "MỘT CƠ CHẾ", "at": 9, "sm": True}, {"text": "ÍT NGƯỜI ĐỂ Ý", "at": [9, "ít"], "acc": True}]},
    {"type": "ledger", "at": 10, "title": "CÙNG 3 TRIỆU ĐỒNG", "rows": [{"k": "LÚC GIÁ RẺ", "v": "MUA ĐƯỢC NHIỀU HƠN", "at": [10, "lúc"]},
                                                                      {"k": "LÚC GIÁ ĐẮT", "v": "MUA ĐƯỢC ÍT HƠN", "at": [10, "Lúc"]}]},
    {"type": "bars", "at": 11, "title": "CÙNG 3 TRIỆU MUA ĐƯỢC BAO NHIÊU “PHẦN CHỈ SỐ”?",
     "items": [{"k": "04/2020 · CHỈ SỐ ~680", "v": M["cheap"]["units_x1000"], "lbl": "4,41", "at": 11, "acc": True},
               {"k": "07/2026 · CHỈ SỐ ~1.867", "v": M["dear"]["units_x1000"], "lbl": "1,61", "at": 12}],
     "label": {"k": "THÁNG RẺ MUA ĐƯỢC", "v": "GẤP ~2,7 LẦN THÁNG ĐẮT", "at": 13}},
    {"type": "question", "at": 14, "text": "Kết quả là gì?"},
    {"type": "bars", "at": 15, "title": "GIÁ MUA CỦA CÔ ĐỀU (ĐIỂM CHỈ SỐ)",
     "items": [{"k": "TRUNG BÌNH CỘNG GIÁ 97 NGÀY MUA", "v": 1231, "lbl": "≈ 1.231", "at": 15},
               {"k": "GIÁ VỐN THẬT", "v": 1170, "lbl": "≈ 1.170", "at": 16, "acc": True}],
     "label": {"k": "", "v": SELF, "at": 15}},
    {"type": "kinetic", "at": 17, "items": [{"text": "KHÔNG CẦN ĐOÁN", "at": 17, "acc": True},
                                           {"text": "tiền cố định tự mua nhiều hơn khi rẻ", "at": [17, "Chỉ"], "sm": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "CHƯA PHẢI", "at": 18, "sm": True}, {"text": "PHẦN HAY NHẤT", "at": [18, "phần"], "acc": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "ANH XUI VÀ CHỊ MAY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "ANH XUI\nVÀ CHỊ MAY", "sub": "MỖI NĂM MUA ĐÚNG MỘT LẦN", "vid": "38484636", "illus": VM,
     "titleAt": [0, "Bây"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "KHÔNG MUA HẰNG THÁNG", "at": 1}, {"text": "MỖI NĂM · MUA ĐÚNG MỘT LẦN", "at": 2, "acc": True}]},
    {"type": "candles", "at": 3, "series": "vnindex", "from": "2021-10-01", "to": "2022-06-30", "drawAt": [3, None, 0, 0.1], "until": [4, "cao"],
     "title": "ANH XUI · NĂM 2022", "range": "10/2021 → 06/2022", "ind": [],
     "marks": [{"date": "2022-01-06", "text": "MUA ĐÚNG ĐỈNH · 06/01", "at": [5, "sáu"], "pos": "above", "tone": "down"}], "source": DATA},
    {"type": "candles", "at": 6, "series": "vnindex", "from": "2026-02-02", "to": "2026-08-31", "drawAt": [6, None, 0, 0.1], "until": [6, "giữa"],
     "title": "ANH XUI · NĂM 2026", "range": "02/2026 → 08/2026", "ind": [],
     "marks": [{"date": "2026-05-18", "text": "MUA 18/05 · KỶ LỤC", "at": [6, "lúc"], "pos": "above", "tone": "down"}], "source": DATA},
    {"type": "candles", "at": 7, "series": "vnindex", "from": "2020-01-02", "to": "2020-07-31", "drawAt": [7, None, 0, 0.1], "until": [8, "thấp"],
     "title": "CHỊ MAY · NĂM 2020", "range": "01/2020 → 07/2020", "ind": [],
     "marks": [{"date": "2020-03-24", "text": "MUA 24/03 · ĐÁY NĂM", "at": [9, "hai"], "pos": "below", "tone": "gold"}], "source": DATA},
    {"type": "bars", "at": 10, "title": "VỀ ĐÍCH SAU 8 NĂM (TRIỆU ĐỒNG) · CÙNG NỘP 291",
     "items": [{"k": "CHỊ MAY · MUA ĐÚNG ĐÁY MỖI NĂM", "v": 526, "lbl": "≈ 526", "at": 11}, {"k": "CÔ ĐỀU · MUA ĐỀU", "v": 437, "lbl": "≈ 437", "at": 12},
               {"k": "ANH XUI · MUA ĐÚNG ĐỈNH MỖI NĂM", "v": 381, "lbl": "≈ 381", "at": 14, "acc": True}],
     "label": {"k": "", "v": HYPO, "at": 10}},
    {"type": "slam", "at": 15, "text": "VẪN +31%", "sub": "NGƯỜI XUI NHẤT · 8 NĂM LIỀN MUA ĐÚNG ĐỈNH · " + SELF},
    {"type": "question", "at": 16, "text": "Vậy cứ mua là lãi à?"},
    {"type": "kinetic", "at": 17, "items": [{"text": "KHÔNG", "at": 17, "acc": True}, {"text": "kết quả này không phải một lời hứa", "at": [17, "vì"], "sm": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "MUA ĐÚNG NGÀY NÀO", "at": [19, "chuyện"]}, {"text": "ÍT QUAN TRỌNG HƠN MÌNH TƯỞNG", "at": [19, "ít"], "acc": True}]},
    {"type": "bars", "at": 20, "title": "ĐỔI NGÀY MUA TRONG THÁNG · LÃI CỦA CÔ ĐỀU (%)",
     "items": [{"k": "PHIÊN ĐẦU THÁNG", "v": 50.3, "lbl": "+50,3%", "at": 20}, {"k": "PHIÊN THỨ 6", "v": 49.7, "lbl": "+49,7%", "at": [20, "sáu"]},
               {"k": "PHIÊN THỨ 11", "v": 49.5, "lbl": "+49,5%", "at": [20, "mười"]}, {"k": "PHIÊN THỨ 16", "v": 50.2, "lbl": "+50,2%", "at": [20, "hay"]}],
     "label": {"k": "GẦN NHƯ KHÔNG ĐỔI", "v": SELF, "at": 21}},
    {"type": "question", "at": 22, "text": "Vậy thứ gì\nmới quan trọng?"},
    {"type": "broll", "at": 23, "vid": "35830059", "veil": 0.5, "illus": VM,
     "kin": [{"text": "CÒN NGỒI TRÊN GHẾ TỚI CUỐI", "at": [23, "bạn"], "acc": True}, {"text": "chiếc ghế ấy có những đoạn rất nóng", "at": 24, "sm": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "CÁI GIÁ CỦA SỰ ĐỀU ĐẶN"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "CÁI GIÁ CỦA\nSỰ ĐỀU ĐẶN", "sub": "QUAY LẠI TIN NHẮN 24/03/2020", "vid": "6689151", "illus": VM,
     "titleAt": [0, "Hãy"]},
    {"type": "ledger", "at": 1, "title": "24/03/2020", "srcnote": HYPO,
     "rows": [{"k": "ĐÃ NỘP", "v": "54 TRIỆU", "at": 1}, {"k": "CÒN", "v": "≈ 37 TRIỆU", "at": [1, "còn"]}], "total": {"k": "", "v": "−31%", "at": [1, "Âm"]}},
    {"type": "race", "at": 2, **acc("2018-10", "2020-12"), "title": "CÔ ĐỀU: LÃI/LỖ SO VỚI TIỀN ĐÃ NỘP", "range": "10/2018 → 12/2020",
     "drawAt": [2, "Và"], "until": [4, "tám"], "source": "171 PHIÊN LIỀN DƯỚI TIỀN ĐÃ NỘP (30/01 → 30/09/2020) · " + HYPO},
    {"type": "kinetic", "at": 5, "items": [{"text": "8 THÁNG", "at": 5, "acc": True},
                                          {"text": "tháng nào cũng nộp · tháng nào mở ra cũng thấy lỗ", "at": [5, "tháng"], "sm": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "CHUYỆN CHƯA HẾT", "at": 6, "acc": True}]},
    {"type": "bars", "at": 7, "title": "06/01/2022 · MỌI THỨ RẤT ĐẸP (TRIỆU ĐỒNG)",
     "items": [{"k": "ĐÃ NỘP", "v": 120, "lbl": "120", "at": [8, "nộp"]}, {"k": "TÀI KHOẢN", "v": 181, "lbl": "≈ 181", "at": [8, "tài"], "acc": True}],
     "label": {"k": "LÃI", "v": "+51%", "at": [8, "Lãi"]}},
    {"type": "bars", "at": 9, "title": "15/11/2022 · MƯỜI THÁNG SAU (TRIỆU ĐỒNG)",
     "items": [{"k": "ĐÃ NỘP", "v": 150, "lbl": "150", "at": 10}, {"k": "TÀI KHOẢN", "v": 129, "lbl": "≈ 129", "at": 11, "acc": True}],
     "label": {"k": "", "v": HYPO, "at": 9}},
    {"type": "slam", "at": 12, "text": "+51% → −14%", "sub": "DÙ VẪN NỘP THÊM 30 TRIỆU · " + SELF},
    {"type": "race", "at": 13, **acc("2018-10", "2022-12"), "title": "CÔ ĐỀU: LÃI/LỖ SO VỚI TIỀN ĐÃ NỘP", "range": "10/2018 → 12/2022",
     "drawAt": [13, "Hãy"], "until": [14, "mười"], "source": HYPO},
    {"type": "broll", "at": 15, "vid": "6466354", "ms": 12, "veil": 0.55, "illus": VM,
     "kin": [{"text": "BÁO CHÍ · BẠN BÈ · NGƯỜI THÂN", "at": 15, "sm": True}, {"text": "ĐỀU NÓI THỊ TRƯỜNG SỤP", "at": [15, "đều"], "acc": True}]},
    {"type": "counter", "at": 16, "from": 0, "to": 19, "suffix": "%", "until": [16, "gần"], "label": "SỐ PHIÊN TÀI KHOẢN NẰM DƯỚI TIỀN ĐÃ NỘP",
     "sub": {"text": "379 / 1.995 PHIÊN · " + SELF, "at": 16}},
    {"type": "kinetic", "at": 17, "items": [{"text": "+50% Ở VẠCH ĐÍCH LÀ THẬT", "at": 17}, {"text": "CHỈ AI ĐI HẾT QUÃNG ĐƯỜNG", "at": 18, "acc": True}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "CÂU HỎI ĐẦU VIDEO", "at": 19, "sm": True}, {"text": "BẠN CÓ NỘP TIẾP KHÔNG?", "at": [19, "bạn"], "acc": True}]},
    {"type": "candles", "at": 20, "series": "vnindex", "from": "2020-01-02", "to": "2020-12-31", "drawAt": [20, None, 0, 0.1], "until": [20, "tháng"],
     "title": "VN-INDEX · NĂM 2020", "range": "01/2020 → 12/2020", "ind": [],
     "marks": [{"date": "2020-04-01", "text": "3 TRIỆU THÁNG 4 · LẦN MUA RẺ NHẤT 8 NĂM", "at": [20, "rẻ"], "pos": "below", "tone": "gold"}], "source": DATA},
    {"type": "kinetic", "at": 21, "items": [{"text": "HÔM ĐÓ KHÔNG AI BIẾT", "at": 21}, {"text": "ĐẤY LÀ ĐÁY", "at": [21, "đấy"], "acc": True}]},
    {"type": "kinetic", "at": 22, "items": [{"text": "có thị trường · có giai đoạn", "at": 22, "sm": True}, {"text": "GIÁ CÒN XUỐNG RẤT LÂU", "at": [22, "giá"], "acc": True}]},
]}

S21 = next(s for s in R["sens_start"] if s["start"] == "2021-10")
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "MUA ĐỀU HAY DỒN MỘT LẦN?"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "MUA ĐỀU HAY\nDỒN MỘT LẦN?", "sub": "NẾU CÓ SẴN 291 TRIỆU TỪ ĐẦU", "vid": "11321634", "illus": VM,
     "titleAt": [0, "Nếu"]},
    {"type": "bars", "at": 1, "title": "CÙNG 291 TRIỆU · SAU 8 NĂM (TRIỆU ĐỒNG)",
     "items": [{"k": "DỒN MỘT LẦN NGAY NGÀY ĐẦU", "v": 514, "lbl": "≈ 514", "at": 1, "acc": True}, {"k": "MUA ĐỀU", "v": 437, "lbl": "≈ 437", "at": 2}],
     "label": {"k": "CHÊNH", "v": "≈ 77 TRIỆU · " + SELF, "at": 2}},
    {"type": "kinetic", "at": 3, "items": [{"text": "TIỀN VÀO SỚM", "at": [3, "tiền"]}, {"text": "ĐƯỢC HƯỞNG LÂU HƠN", "at": [3, "được"], "acc": True}]},
    {"type": "ledger", "at": 4, "title": "VANGUARD · 2012", "srcnote": "VANGUARD (2012) · NGHIÊN CỨU VỀ KHOẢN TIỀN CÓ SẴN · QUÁ KHỨ",
     "rows": [{"k": "DỮ LIỆU", "v": "MỸ · ANH · ÚC", "at": [4, "trên"]}, {"k": "≈ 2/3 SỐ LẦN", "v": "DỒN MỘT LẦN CAO HƠN", "at": 5}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "HAI ĐIỀU CẦN ĐỂ Ý", "at": 6}, {"text": "2/3 KHÔNG PHẢI LUÔN LUÔN", "at": 7, "acc": True}]},
    {"type": "bars", "at": 8, "title": "BẮT ĐẦU TỪ 10/2021, NGAY TRƯỚC ĐỈNH · LÃI (%)",
     "items": [{"k": "MUA ĐỀU", "v": S21["gain_pct"], "lbl": "+33,1%", "at": [9, "ba"], "acc": True},
               {"k": "DỒN MỘT LẦN", "v": S21["lump_pct"], "lbl": "+31,8%", "at": [9, "Người"]}],
     "label": {"k": "GẦN NHƯ HOÀ", "v": SELF, "at": [9, "Gần"]}},
    {"type": "kinetic", "at": 10, "items": [{"text": "ĐIỀU THỨ HAI", "at": 10, "sm": True}, {"text": "QUAN TRỌNG HƠN NHIỀU", "at": [10, "quan"], "acc": True}]},
    {"type": "broll", "at": 11, "vid": "1793371", "veil": 0.5, "illus": VM,
     "kin": [{"text": "NGHIÊN CỨU: NGƯỜI ĐÃ CÓ SẴN TIỀN", "at": 11, "sm": True}, {"text": "LĨNH LƯƠNG HẰNG THÁNG", "at": 12},
             {"text": "KHÔNG CÓ LỰA CHỌN ẤY", "at": [12, "gần"], "acc": True}]},
    {"type": "slam", "at": 13, "text": "KHÔNG THỂ DỒN", "sub": "SỐ TIỀN 8 NĂM NỮA MỚI KIẾM ĐƯỢC"},
    {"type": "ledger", "at": 14, "title": "MUA ĐỀU LÀ GÌ, VỚI ĐA SỐ CHÚNG TA?",
     "rows": [{"k": "KHÔNG PHẢI", "v": "MẸO THẮNG THỊ TRƯỜNG", "at": 14}, {"k": "MÀ LÀ", "v": "BIẾN ĐỂ DÀNH THÀNH VIỆC TỰ ĐỘNG", "at": 15},
              {"k": "VÀ BỎ ĐI", "v": "“HÔM NAY CÓ PHẢI LÚC MUA?”", "at": 16}]},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "KHI NÀO PHÉP THỬ\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN QUAN TRỌNG NHẤT", "vid": "8865613", "illus": VM,
     "titleAt": [0, "Giờ"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "KHI CON SỐ", "at": 1, "sm": True}, {"text": "KHÔNG CÒN ĐÚNG VỚI BẠN", "at": [1, "không"], "acc": True}]},
    {"type": "race", "at": 2, **acc("2018-10", "2026-10"), "title": "CÔ ĐỀU · 8 NĂM · LÃI/LỖ SO VỚI TIỀN ĐÃ NỘP", "range": "10/2018 → 10/2026",
     "drawAt": [2, "Thứ"], "until": [3, "lỗ"], "source": "KẾT THÚC Ở VÙNG GIÁ CAO · DỪNG Ở 11/2022 THÌ ĐANG LỖ · " + HYPO},
    {"type": "kinetic", "at": 4, "items": [{"text": "PHỤ THUỘC", "at": 4, "sm": True}, {"text": "NGÀY BẠN CẦN RÚT TIỀN", "at": [4, "ngày"], "acc": True}]},
    {"type": "ledger", "at": 5, "title": "PHÉP THỬ NÀY CHƯA TÍNH", "srcnote": SELF,
     "rows": [{"k": "2", "v": "MỘT CHỈ SỐ · MỘT THỊ TRƯỜNG", "at": 5}, {"k": "", "v": "CÓ THỊ TRƯỜNG ĐI NGANG HÀNG CHỤC NĂM", "at": 6},
              {"k": "3", "v": "PHÍ · THUẾ (TIỀN NHỎ, PHÍ ĂN NHIỀU)", "at": 7}, {"k": "4", "v": "KHÔNG MUA ĐƯỢC NGUYÊN CHỈ SỐ", "at": 8}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "THỨ NĂM", "at": 9, "sm": True}, {"text": "ĐIỀU KHÓ NHẤT", "at": [9, "điều"], "acc": True}]},
    {"type": "counter", "at": 10, "from": 0, "to": 97, "suffix": " THÁNG", "until": [10, "tháng"], "label": "KHÔNG BỎ CUỘC LẦN NÀO", "sub": {"text": "GIẢ ĐỊNH CỦA PHÉP THỬ", "at": 10}},
    {"type": "broll", "at": 11, "vid": "35830059", "ms": 30, "veil": 0.5, "illus": VM,
     "kin": [{"text": "KỂ CẢ 8 THÁNG LIỀN THẤY LỖ", "at": 11}, {"text": "KỂ CẢ LÚC CẦN TIỀN GẤP", "at": [11, "lúc"], "acc": True}]},
    {"type": "ledger", "at": 12, "title": "BA CÂU TỰ HỎI",
     "rows": [{"k": "1", "v": "BAO NHIÊU NĂM NỮA MỚI CẦN DÙNG?", "at": 13}, {"k": "2", "v": "ĐÃ CÓ QUỸ KHẨN CẤP CHƯA?", "at": 14},
              {"k": "3", "v": "THẤY −30% CÓ CHỊU NỔI KHÔNG?", "at": 15}]},
    {"type": "date", "at": 16, "day": "TIN NHẮN BÁO LỖ 17 TRIỆU", "date": "24.03.2020"},
    {"type": "kinetic", "at": 17, "items": [{"text": "AI ĐI TIẾP", "at": [17, "ai"]}, {"text": "8 NĂM SAU ĐÃ ỔN", "at": [17, "tám"], "acc": True}]},
    {"type": "slam", "at": 18, "text": "NGỒI YÊN MỚI KHÓ", "sub": "PHÉP TÍNH THÌ DỄ"},
    {"type": "question", "at": 19, "text": "Bạn đã bao giờ dừng để dành\nvì thấy đang lỗ chưa?"},
    {"type": "kinetic", "at": 20, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 20}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [20, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
SPEC = {
    "title": "Mỗi Tháng 3 Triệu Theo VN-Index Suốt 8 Năm: Người Xui Nhất Vẫn Lãi, Nhưng Có 8 Tháng Liền Âm",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["vn-index", "đều", "xui", "may", "lỗ", "lãi", "nộp"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Mỗi Tháng 3 Triệu Theo VN-Index Suốt 8 Năm: Người Xui Nhất Vẫn Lãi, Nhưng Có 8 Tháng Liền Âm",
                   "Mua Đều Mỗi Tháng Là Gì? Kênh Thử Trên 8 Năm VN-Index: 291 Triệu Thành Bao Nhiêu",
                   "Ba Người, Cùng 291 Triệu, 8 Năm: Mua Đều, Mua Xui Nhất, Mua May Nhất"],
        "summary": "Mua đều mỗi tháng (dollar cost averaging) là gì, và nó chạy thế nào trên dữ liệu thật? Kênh cho ba nhân vật giả định cùng nộp "
                   "291 triệu trong 8 năm (10/2018–10/2026) theo VN-Index: người mua đều mỗi tháng, người năm nào cũng mua đúng đỉnh, và người "
                   "năm nào cũng mua đúng đáy. Kết quả ở vạch đích, và cái giá trên đường đi: 171 phiên liền tài khoản nằm dưới số tiền đã nộp. "
                   "Kèm phần quan trọng nhất: khi nào phép thử này không đúng với bạn.",
        "more": [Y4["more"][0],
                 "📐 CÁCH KÊNH TÍNH (quá khứ, không phải khuyến nghị): VN-Index đóng cửa 08/10/2018–06/10/2026 (vnstock/VCI). Mua đều: 3 triệu "
                 "vào phiên đầu tiên của mỗi tháng (97 lần, 291 triệu). \"Xui nhất\"/\"may nhất\": mỗi năm gom tiền cả năm, mua đúng ngày đóng "
                 "cửa cao nhất/thấp nhất năm (biết trước, không ai làm được ngoài đời; chỉ để đo hai đầu mút). Dồn một lần: 291 triệu mua ngày "
                 "đầu. Không phí, thuế, cổ tức; chỉ số không mua trực tiếp được. Một chỉ số, một giai đoạn: minh hoạ cơ chế, KHÔNG phải bằng "
                 "chứng rằng cách nào tốt hay xấu.",
                 "📚 Nghiên cứu nhắc trong video: Vanguard (2012), \"Dollar-cost averaging just means taking risk later\" — về khoản tiền có sẵn, "
                 "dữ liệu Mỹ/Anh/Úc; kết quả quá khứ."],
        "chapter_titles": {"ch00": "Mở đầu: tin nhắn ngày 24/03/2020", "ch01": "Luật chơi: mua đều là gì", "ch02": "Cô Đều về đích: 291 → 437 triệu",
                           "ch03": "Anh Xui và chị May: mua đúng đỉnh, mua đúng đáy", "ch04": "Cái giá của sự đều đặn: 8 tháng liền âm",
                           "ch05": "Mua đều hay dồn một lần?", "ch06": "Khi nào phép thử này không đúng với bạn"},
        "sources": ["https://benefitspro.com/2012/10/31/lump-sum-investing-vs-dollar-cost-averaging",
                    "https://robberger.com/lump-sum-investing-vs-dollar-cost-averaging"],
        "hashtags": ["TàiChínhCáNhân", "MuaĐều", "DCA", "VNIndex", "BiểuĐồBiếtNói"],
        "tags": ["mua đều mỗi tháng", "DCA là gì", "dollar cost averaging", "tích sản", "để dành mỗi tháng", "VN-Index", "tài chính cá nhân",
                 "chứng khoán cho người mới", "lãi lỗ", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 DỮ LIỆU BIỂU ĐỒ: VN-Index, truy xuất qua Vnstock (nguồn VCI); mọi phép tính mua đều, dồn một lần, \"xui nhất\", \"may nhất\" do kênh tự tính trên giá đóng cửa. Ba nhân vật là giả định.",
        "video_credits": Y4["video_credits"],
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
