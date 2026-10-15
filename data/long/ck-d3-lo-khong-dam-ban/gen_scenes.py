"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK D3 "Lỗ rồi càng không dám bán".

    python data/long/ck-d3-lo-khong-dam-ban/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Số: analysis.py -> results.json (VN-Index 2022 kênh tự tính; toán hoà vốn; ví dụ giả định hai cổ phiếu A, B).
Luật kênh: chỉ giáo dục; không mã cổ phiếu; không "nên cắt lỗ/nên giữ"; không dự báo. Lộ trình "chiếc cân hai đĩa".
Luật 15/10: "≈" thay "~" trước số; counter có prefix đứng yên; không counter năm.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
D2 = json.loads((D.parent / "ck-d2-fomo" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(D2["say"])
SAY.update({"kahneman": "Ca-nơ-men", "amos": "A-mốt", "tversky": "Tơ-véc-xki", "hersh": "Hớt", "shefrin": "Sép-phrin", "meir": "Me-ia",
            "statman": "Xtét-mần", "terrance": "Te-rần", "odean": "Ô-đin"})
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
V = R["vnindex"]
assert V["drop_pct"] == -40.3 and V["need_from_trough_pct"] == 67.6 and V["back"][0] == "2025-07-25"
H1 = "VÍ DỤ GIẢ ĐỊNH"
KT = "KÊNH TỰ TÍNH · VN-INDEX ĐÓNG CỬA"
VM = "VIDEO MINH HỌA"
SCALE, MKT, WORRY, PHONE, ANCHOR, CLIMB, CHESS = "8061659", "8486622", "7534958", "6183991", "6979840", "4163540", "8431825"   # MKT: 38736271 lộ cặp BTC/USDT -> thay 15/10
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI CỔ PHIẾU, MỘT CUỘC GỌI"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "ledger", "title": "TÀI KHOẢN CỦA BẠN · MỖI MÃ MUA 50 TRIỆU", "srcnote": H1,
     "rows": [{"k": "CỔ PHIẾU A · +20%", "v": "60 TRIỆU", "at": [1, None, 0, 0.05]}, {"k": "CỔ PHIẾU B · −20%", "v": "40 TRIỆU", "at": [2, None, 0, 0.05]}]},
    {"type": "broll", "at": 3, "vid": PHONE, "veil": 0.55, "illus": "VÍ DỤ GIẢ ĐỊNH · " + VM,
     "kin": [{"text": "MỘT CUỘC GỌI", "at": 3, "sm": True}, {"text": "NHÀ CẦN 40 TRIỆU", "at": [3, "Nhà"], "acc": True}, {"text": "bán cổ phiếu nào?", "at": 4, "sm": True}]},
    {"type": "ledger", "at": 5, "title": "PHẦN LỚN MỌI NGƯỜI CHỌN BÁN A", "rows": [{"k": "BÁN A", "v": "CHỐT LÃI · DỄ CHỊU", "at": 6}, {"k": "BÁN B", "v": "LỖ THÀNH THẬT · KHÓ CHỊU", "at": 7}]},
    {"type": "question", "at": 8, "text": "Bán cái đang lãi.\nCó gì sai đâu?"},
    {"type": "broll", "at": 9, "vid": SCALE, "veil": 0.55, "illus": VM,
     "kin": [{"text": "LÝ DO KHÔNG NẰM Ở HAI CỔ PHIẾU", "at": [9, "Nhưng"], "sm": True}, {"text": "MỘT CHIẾC CÂN LỆCH", "at": [10, "một"], "acc": True},
             {"text": "đặt từng thứ lên cân", "at": 11, "sm": True}]},
    {"type": "brand", "at": 12, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CHIẾC CÂN LỆCH"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CHIẾC CÂN LỆCH", "sub": "ĐƯỢC MỘT TRIỆU · MẤT MỘT TRIỆU", "vid": CHESS, "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "myth", "at": 2, "mythLab": "VỀ CON SỐ", "myth": "HAI THỨ BẰNG NHAU", "truthLab": "VỀ CẢM GIÁC", "truth": "THÌ KHÔNG", "strikeAt": [3, "Nhưng"], "truthAt": [3, "thì"]},
    {"type": "source", "at": 4, "source": "KAHNEMAN & TVERSKY · 1979 · 1992", "ref": "LÝ THUYẾT TRIỂN VỌNG",
     "snippet": "nỗi đau khi mất nặng hơn niềm vui khi được · hệ số ước tính [[≈ 2,25]]", "hlAt": [6, "hai"], "seal": "NGHIÊN CỨU KHÁC: THƯỜNG QUANH ×2", "sealAt": 8},
    {"type": "bars", "at": 7, "title": "CẢM GIÁC · CÙNG MỘT TRIỆU", "unit": "MINH HOẠ HỆ SỐ ≈ 2 · KHÔNG PHẢI SỐ ĐO CỦA RIÊNG AI",
     "items": [{"k": "VUI KHI ĐƯỢC", "v": 1, "lbl": "×1", "at": [7, "được"]}, {"k": "ĐAU KHI MẤT", "v": 2.25, "lbl": "≈ ×2", "at": [7, "mất"], "acc": True}]},
    {"type": "question", "at": 9, "text": "Liên quan gì tới\nviệc bán cổ phiếu?"},
    {"type": "ledger", "at": 10, "title": "CHIẾC CÂN KHI BẠN BẤM BÁN", "rows": [{"k": "CHƯA BÁN", "v": "CON SỐ TRÊN MÀN HÌNH · CÒN HY VỌNG", "at": 11},
                                                                             {"k": "BÁN ĐI", "v": "MỘT KHOẢN MẤT THẬT", "at": 12}], "total": {"k": "NÊN", "v": "TA TRÌ HOÃN", "at": 13}},
    {"type": "kinetic", "at": 14, "items": [{"text": "CỔ PHIẾU ĐANG LÃI THÌ NGƯỢC LẠI", "at": 14, "sm": True}, {"text": "CHỐT LÃI = NẾM NIỀM VUI NGAY", "at": [14, "Chốt"], "acc": True}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "MƯỜI NGHÌN TÀI KHOẢN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "MƯỜI NGHÌN\nTÀI KHOẢN", "sub": "NGOÀI ĐỜI CÓ THẬT VẬY KHÔNG?", "vid": MKT, "illus": VM, "titleAt": [0, "Đó"]},
    {"type": "ledger", "at": 1, "title": "HIỆU ỨNG PHÂN BỔ · SHEFRIN & STATMAN 1985", "rows": [{"k": "BÁN CỔ PHIẾU LÃI", "v": "QUÁ SỚM", "at": [2, "bán"]}, {"k": "GIỮ CỔ PHIẾU LỖ", "v": "QUÁ LÂU", "at": [2, "giữ"]}]},
    {"type": "source", "at": 3, "source": "ODEAN · JOURNAL OF FINANCE · 1998", "ref": "10.000 TÀI KHOẢN · 7 NĂM",
     "snippet": "nhà đầu tư [[thích chốt lãi hơn hẳn cắt lỗ]] · dữ liệu một công ty môi giới tại Mỹ", "hlAt": [4, "mười"], "seal": "ĐO TRÊN GIAO DỊCH THẬT", "sealAt": 5},
    {"type": "bars", "at": 6, "title": "TỶ LỆ ĐƯỢC BÁN RA (%)", "unit": "ODEAN 1998 · 10.000 TÀI KHOẢN",
     "items": [{"k": "KHOẢN ĐANG LÃI", "v": 14.8, "lbl": "14,8%", "at": [6, "mười"], "acc": True}, {"k": "KHOẢN ĐANG LỖ", "v": 9.8, "lbl": "9,8%", "at": [7, "chín"]}]},
    {"type": "counter", "at": 8, "from": 1.5, "to": 1.5, "prefix": "≈ ", "suffix": " LẦN", "label": "KHẢ NĂNG BÁN KHOẢN LÃI SO VỚI KHOẢN LỖ", "sub": {"text": "ĐÚNG NHƯ CÂU TRẢ LỜI Ở ĐẦU VIDEO", "at": 9}},
    {"type": "question", "at": 10, "text": "Biết đâu họ có\nlý do chính đáng?"},
    {"type": "ledger", "at": 11, "title": "ODEAN ĐÃ KIỂM TRA", "rows": [{"k": "CÂN BẰNG DANH MỤC?", "v": "KHÔNG GIẢI THÍCH ĐƯỢC", "at": [12, "cân"]},
                                                                     {"k": "TRÁNH PHÍ?", "v": "KHÔNG GIẢI THÍCH ĐƯỢC", "at": [12, "phí"]},
                                                                     {"k": "CỔ PHIẾU LÃI ĐÃ BÁN", "v": "VỀ SAU KHÔNG KÉM HƠN", "at": 13}]},
    {"type": "slam", "at": 14, "text": "TRONG TÀI KHOẢN THẬT", "sub": "KHÔNG CHỈ TRONG PHÒNG THÍ NGHIỆM", "subAt": 14},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "PHÉP TOÁN CỦA HỐ SÂU"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "PHÉP TOÁN\nCỦA HỐ SÂU", "sub": "CHỜ VỀ BỜ RỒI BÁN", "vid": CLIMB, "illus": VM, "titleAt": [0, "Giữ"]},
    {"type": "bars", "at": 2, "title": "CẦN LÃI BAO NHIÊU ĐỂ HOÀ VỐN (%)", "unit": "LÃI CẦN = LỖ ÷ (1 − LỖ)",
     "items": [{"k": "LỖ 10%", "v": 11.1, "lbl": "+11", "at": 3}, {"k": "LỖ 20%", "v": 25, "lbl": "+25", "at": 4}, {"k": "LỖ 40%", "v": 66.7, "lbl": "+67", "at": 5, "acc": True},
               {"k": "LỖ 50%", "v": 100, "lbl": "+100", "at": 6}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "HỐ CÀNG SÂU", "at": 8, "sm": True}, {"text": "LEO LÊN DỐC HƠN RƠI XUỐNG", "at": [8, "đường"], "acc": True}]},
    {"type": "question", "at": 9, "text": "Có ví dụ thật nào không?"},
    {"type": "bars", "at": 11, "title": "VN-INDEX (ĐIỂM)", "unit": KT,
     "items": [{"k": "ĐỈNH 06/01/2022", "v": 1528.57, "lbl": "1.529", "at": [11, "một"]}, {"k": "ĐÁY 15/11/2022", "v": 911.9, "lbl": "912 · −40%", "at": [12, "chín"], "acc": True}]},
    {"type": "counter", "at": 13, "from": 67.6, "to": 67.6, "prefix": "+", "suffix": "%", "label": "TỪ ĐÁY PHẢI TĂNG ĐỂ VỀ LẠI ĐỈNH", "sub": {"text": KT, "at": 13}},
    {"type": "slam", "at": 14, "text": "25/07/2025", "sub": "VỀ LẠI ĐỈNH · HƠN 3 NĂM RƯỠI SAU · " + KT, "subAt": 15},
    {"type": "kinetic", "at": 16, "items": [{"text": "TỪNG CỔ PHIẾU: CÓ MÃ VỀ NHANH HƠN", "at": [16, "Với"], "sm": True}, {"text": "CÓ MÃ TỚI GIỜ VẪN CHƯA VỀ", "at": [16, "có", 1], "acc": True},
                                           {"text": "trong lúc chờ, tiền không làm được việc khác", "at": [17, "trong"], "sm": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "MỎ NEO GIÁ MUA"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "MỎ NEO GIÁ MUA", "sub": "THỨ NẶNG NHẤT TRÊN CÂN", "vid": ANCHOR, "illus": VM, "titleAt": [0, "Thứ"]},
    {"type": "ledger", "at": 1, "title": "CỔ PHIẾU B", "srcnote": H1, "rows": [{"k": "GIÁ BẠN TRẢ", "v": "50 TRIỆU", "at": [1, "mua"]}, {"k": "HÔM NAY", "v": "40 TRIỆU", "at": [1, "giờ"]}],
     "total": {"k": "THỊ TRƯỜNG BIẾT GIÁ BẠN MUA?", "v": "KHÔNG", "at": 2}},
    {"type": "kinetic", "at": 3, "items": [{"text": "GIÁ NGÀY MAI KHÔNG PHỤ THUỘC", "at": 3, "sm": True}, {"text": "VÀO VIỆC BẠN ĐANG LỖ HAY LÃI", "at": [3, "vào"], "acc": True}]},
    {"type": "myth", "at": 5, "mythLab": "CÂU HỎI QUEN", "myth": "BAO GIỜ VỀ 50?", "truthLab": "CÂU HỎI CỦA TIỀN", "truth": "40 TRIỆU NÊN Ở ĐÂU?", "strikeAt": [6, "Trong"], "truthAt": [7, "từ"]},
    {"type": "question", "at": 8, "text": "Chưa bán thì chưa lỗ mà?"},
    {"type": "ledger", "at": 9, "title": "TÀI KHOẢN HÔM NAY", "srcnote": H1, "rows": [{"k": "NẾU BÁN", "v": "40 TRIỆU", "at": 10}, {"k": "NẾU KHÔNG BÁN", "v": "VẪN 40 TRIỆU", "at": [10, "dù"]}],
     "total": {"k": "KHÔNG BÁN", "v": "KHÓ THẤY HƠN · VẪN CÒN ĐÓ", "at": 11}},
    {"type": "broll", "at": 12, "vid": WORRY, "veil": 0.55, "illus": VM,
     "kin": [{"text": "MỘT CÁCH GỠ MỎ NEO", "at": 12, "sm": True}, {"text": "CẦM 40 TRIỆU TIỀN MẶT HÔM NAY", "at": 13, "sm": True},
             {"text": "CÓ MUA LẠI ĐÚNG CỔ PHIẾU NÀY KHÔNG?", "at": 14, "acc": True}]},
    {"type": "slam", "at": 15, "text": "KHÔNG NHẮC TỚI 50 TRIỆU", "sub": "CÂU TRẢ LỜI CHỈ NHÌN VỀ PHÍA TRƯỚC", "subAt": 15},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "KHI GIỮ LẠI LÀ CÓ LÝ DO"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "KHI GIỮ LẠI\nLÀ CÓ LÝ DO", "sub": "KHÔNG PHẢI CỨ LỖ LÀ PHẢI BÁN", "vid": MKT, "ms": 12, "illus": VM, "titleAt": [0, "Nói"]},
    {"type": "ledger", "at": 1, "title": "GIỮ CỔ PHIẾU LỖ CÓ THỂ HỢP LÝ, NẾU", "rows": [{"k": "1", "v": "LÝ DO MUA BAN ĐẦU VẪN CÒN", "at": 2}, {"k": "2", "v": "TIỀN NHÀN RỖI · ĐỦ KIÊN NHẪN", "at": 3}, {"k": "3", "v": "CHỈ LÀ MỘT PHẦN VỪA PHẢI", "at": 4}]},
    {"type": "myth", "at": 5, "mythLab": "VẤN ĐỀ KHÔNG NẰM Ở", "myth": "GIỮ HAY BÁN", "truthLab": "MÀ Ở", "truth": "VÌ LÝ DO GÌ", "strikeAt": [6, "Mà"], "truthAt": [6, "lý"]},
    {"type": "kinetic", "at": 7, "items": [{"text": "ĐÃ PHÂN TÍCH LẠI", "at": 7, "sm": True}, {"text": "HAY CHỈ VÌ KHÔNG CHỊU NỔI CẢM GIÁC?", "at": [7, "hay"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "CỔ PHIẾU LÃI CŨNG VẬY", "at": 8, "sm": True}, {"text": "SỢ LÃI BIẾN MẤT = CHIẾC CÂN LÊN TIẾNG", "at": [9, "Nhưng"], "acc": True}]},
    {"type": "ledger", "at": 10, "title": "BÁN A HAY BÁN B?", "rows": [{"k": "TUỲ VÀO", "v": "HAI DOANH NGHIỆP", "at": [10, "tuỳ"]}, {"k": "KHÔNG TUỲ VÀO", "v": "MÃ NÀO XANH · MÃ NÀO ĐỎ", "at": [10, "không"]}]},
]}

CH["ch06"] = {"hud": {"k": "GIỚI HẠN", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "KHI NÀO NHỮNG ĐIỀU NÀY\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": SCALE, "ms": 8, "illus": VM, "titleAt": [0, "Và"]},
    {"type": "ledger", "at": 2, "title": "GIỚI HẠN", "rows": [{"k": "1", "v": "NGHIÊN CỨU Ở MỸ · HƠN 30 NĂM TRƯỚC", "at": 2}, {"k": "2", "v": "HỆ SỐ LÀ SỐ TRUNG BÌNH", "at": 4},
                                                         {"k": "3", "v": "A, B CHỈ LÀ VÍ DỤ", "at": 5}]},
    {"type": "ledger", "at": 6, "title": "BA CÂU TRƯỚC KHI BÁN HAY GIỮ", "rows": [{"k": "1", "v": "CẦM TIỀN MẶT, CÓ MUA LẠI KHÔNG?", "at": 7}, {"k": "2", "v": "VÌ DOANH NGHIỆP HAY VÌ CON SỐ?", "at": 8},
                                                                             {"k": "3", "v": "CHỜ VỀ BỜ BAO LÂU · MẤT CƠ HỘI GÌ?", "at": 9}]},
    {"type": "broll", "at": 10, "vid": SCALE, "ms": 2, "veil": 0.5, "illus": VM,
     "kin": [{"text": "CHIẾC CÂN SẼ KHÔNG BAO GIỜ CÂN HOÀN TOÀN", "at": 10, "sm": True}, {"text": "BIẾT NÓ LỆCH VỀ ĐÂU", "at": [11, "biết"], "acc": True}]},
    {"type": "question", "at": 12, "text": "Bạn đã bao giờ ôm một cổ phiếu lỗ\nlâu hơn mình định?"},
    {"type": "kinetic", "at": 13, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 13}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [13, "ở"], "acc": True}]},
]}

Y2 = D2["youtube"]
SPEC = {
    "title": "Vì Sao Lỗ Rồi Lại Càng Không Dám Bán? Chiếc Cân Lệch Trong Đầu Người Đầu Tư",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 25, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["lỗ", "lãi", "cân", "bán", "neo", "bờ", "đau"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Vì Sao Lỗ Rồi Lại Càng Không Dám Bán? Chiếc Cân Lệch Trong Đầu Người Đầu Tư",
                   "Lãi Thì Bán Ngay, Lỗ Thì Ôm Mãi: Nghiên Cứu Trên 10.000 Tài Khoản Nói Gì",
                   "Lỗ 40% Cần Lãi Bao Nhiêu Để Hoà Vốn? Bài Toán VN-Index Năm 2022"],
        "summary": "Hai cổ phiếu, một đang lãi 20%, một đang lỗ 20%, nhà cần tiền: bạn bán mã nào? Video đặt từng thứ lên “chiếc cân” trong đầu người đầu "
                   "tư: nỗi đau mất nặng gấp khoảng đôi niềm vui được (Kahneman & Tversky), nghiên cứu 10.000 tài khoản của Odean (1998), phép toán hoà vốn "
                   "(lỗ 40% cần lãi gần 67%) với ví dụ VN-Index 2022, mỏ neo giá mua, và khi nào giữ lại là có lý do. Kèm ba câu tự hỏi trước khi bán hay giữ.",
        "more": [Y2["more"][0],
                 "📐 CÁCH KÊNH TÍNH: VN-Index đóng cửa: đỉnh 06/01/2022 1.528,57; đáy 15/11/2022 911,90 (−40,3%); từ đáy cần +67,6%; vượt lại đỉnh lần "
                 "đầu 25/07/2025 (≈ 42,6 tháng sau đỉnh). Toán hoà vốn: lãi cần = lỗ ÷ (1 − lỗ). Hai cổ phiếu A, B là ví dụ giả định. Nghiên cứu: "
                 "Kahneman & Tversky (1979); Tversky & Kahneman (1992), hệ số ngại thua lỗ ≈ 2,25; Shefrin & Statman (1985); Odean (1998), Journal of "
                 "Finance: tỷ lệ chốt lãi ≈ 14,8% so với cắt lỗ ≈ 9,8% (tính cả năm; riêng tháng Mười Hai thì ngược lại)."],
        "chapter_titles": {"ch00": "Mở đầu: hai cổ phiếu, một cuộc gọi", "ch01": "Chiếc cân lệch: mất đau gấp đôi được", "ch02": "Mười nghìn tài khoản: nghiên cứu Odean",
                           "ch03": "Phép toán của hố sâu: VN-Index 2022", "ch04": "Mỏ neo giá mua", "ch05": "Khi giữ lại là có lý do",
                           "ch06": "Khi nào những điều này không đúng với bạn"},
        "sources": ["https://faculty.haas.berkeley.edu/odean/papers/disposition/disposition.html", "https://en.wikipedia.org/wiki/Disposition_effect",
                    "https://ideas.repec.org/a/kap/jrisku/v5y1992i4p297-323.html"],
        "hashtags": ["TâmLýĐầuTư", "ChứngKhoán", "CắtLỗ", "TâmLýTiềnBạc", "BiểuĐồBiếtNói"],
        "tags": ["vì sao không dám cắt lỗ", "hiệu ứng phân bổ", "disposition effect", "ngại thua lỗ", "loss aversion", "lỗ bao nhiêu thì hoà vốn",
                 "tâm lý đầu tư chứng khoán", "vn-index 2022", "biểu đồ biết nói"],
        "category": Y2["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: VN-Index đóng cửa (kênh tự tính); nghiên cứu Kahneman & Tversky, Shefrin & Statman, Odean.",
        "video_credits": Y2["video_credits"],
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
