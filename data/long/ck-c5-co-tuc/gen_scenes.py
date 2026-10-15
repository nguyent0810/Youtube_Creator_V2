"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK C5 "Cổ tức".

    python data/long/ck-c5-co-tuc/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (VÍ DỤ GIẢ ĐỊNH: cổ phiếu 40.000 đ, cổ tức tiền 10% mệnh giá, cổ phiếu 20%).
Luật kênh: chỉ giáo dục; không mã cổ phiếu/tên doanh nghiệp/công ty chứng khoán; cảnh số ví dụ ghi "VÍ DỤ GIẢ ĐỊNH".
Lộ trình "giải mã từng cụm chữ trên một tờ thông báo"; mô-típ cái bánh. Luật 15/10: "≈" thay "~" trước số; counter có prefix đứng yên.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
assert R["yield_pct"] == 2.5 and R["dividend_capture"]["result"] == -326000 and R["ex_stock"]["after_price"] == 33333
H1 = "VÍ DỤ GIẢ ĐỊNH"
HX = "VÍ DỤ GIẢ ĐỊNH · GIÁ 40.000 Đ · CỔ TỨC 10% MỆNH GIÁ"
VM = "VIDEO MINH HỌA"
CAKE, DOC, LAPTOP, MKT, MAG = "5615174", "8731555", "5466766", "5253412", "6980366"   # MKT: 38905686 lộ mã cổ phiếu + tên công ty -> thay 15/10; LAPTOP: 8480232 lộ cặp DOGE/USD, Bitcoin/USD -> thay 15/10
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MỘT TỜ THÔNG BÁO"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": DOC, "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỘT TỜ THÔNG BÁO CỔ TỨC", "at": [0, "Một"], "acc": True}, {"text": "ba cụm chữ", "at": 1, "sm": True}]},
    {"type": "ledger", "at": 2, "title": "TỜ THÔNG BÁO · BA CỤM CHỮ", "srcnote": H1,
     "rows": [{"k": "1", "v": "CỔ TỨC BẰNG TIỀN · 10%", "at": 2}, {"k": "2", "v": "NGÀY GIAO DỊCH KHÔNG HƯỞNG QUYỀN", "at": 3}, {"k": "3", "v": "CỔ TỨC BẰNG CỔ PHIẾU", "at": 4}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "MƯỜI PHẦN TRĂM", "at": [6, "Mười"], "acc": True}, {"text": "cao hơn cả lãi tiết kiệm?", "at": [6, "cao"], "sm": True}]},
    {"type": "question", "at": 7, "text": "Cứ mua vào\nrồi nhận 10%?"},
    {"type": "broll", "at": 9, "vid": CAKE, "veil": 0.55, "illus": VM,
     "kin": [{"text": "CỔ PHIẾU VÍ DỤ · 40.000 Đ", "at": 9, "sm": True}, {"text": "CHIA CỔ TỨC = CẮT BÁNH", "at": [10, "giống"], "acc": True},
             {"text": "không làm cái bánh to ra", "at": [10, "chứ"], "sm": True}]},
    {"type": "brand", "at": 11, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MƯỜI PHẦN TRĂM CỦA CÁI GÌ?"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CỤM CHỮ THỨ NHẤT", "title": "MƯỜI PHẦN TRĂM\nCỦA CÁI GÌ?", "sub": "CỔ TỨC BẰNG TIỀN · 10%", "vid": MAG, "illus": VM, "titleAt": [0, "Cụm"]},
    {"type": "myth", "at": 1, "mythLab": "KHÔNG TÍNH TRÊN", "myth": "TIỀN BẠN BỎ RA", "truthLab": "MÀ TÍNH TRÊN", "truth": "MỆNH GIÁ", "strikeAt": [1, "không"], "truthAt": [2, "mệnh"]},
    {"type": "counter", "at": 3, "from": 10000, "to": 10000, "suffix": " Đ", "label": "MỆNH GIÁ MỖI CỔ PHIẾU · THƯỜNG LÀ", "sub": {"text": "GẦN NHƯ KHÔNG LIÊN QUAN GIÁ TRÊN SÀN", "at": 4}},
    {"type": "ledger", "at": 6, "title": "CỔ TỨC 10% · MỖI CỔ PHIẾU", "srcnote": HX,
     "rows": [{"k": "10% × 10.000 Đ", "v": "1.000 Đ", "at": [6, "một"]}, {"k": "SO VỚI GIÁ MUA 40.000 Đ", "v": "2,5%", "at": [7, "hai"]}]},
    {"type": "slam", "at": 8, "text": "10% → 2,5%", "sub": "VỚI NGƯỜI MUA GIÁ 40.000 Đ · " + H1, "subAt": 8},
    {"type": "bars", "at": 10, "title": "TỶ SUẤT CỔ TỨC (% GIÁ MUA)", "unit": "CÙNG 1.000 Đ · " + H1,
     "items": [{"k": "GIÁ 20.000 Đ", "v": 5, "lbl": "5%", "at": [11, "năm"]}, {"k": "GIÁ 40.000 Đ", "v": 2.5, "lbl": "2,5%", "at": [10, "tỷ"], "acc": True},
               {"k": "GIÁ 100.000 Đ", "v": 1, "lbl": "1%", "at": [12, "một"]}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "THÔNG BÁO GHI TRÊN MỆNH GIÁ", "at": 13, "sm": True}, {"text": "NGƯỜI MUA TỰ ĐỔI RA TỶ SUẤT", "at": 14, "acc": True},
                                           {"text": "cụm thứ hai mới là chỗ bất ngờ", "at": 16, "sm": True}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "NGÀY GIÁ TỰ GIẢM"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CỤM CHỮ THỨ HAI", "title": "NGÀY GIÁ TỰ GIẢM", "sub": "NGÀY GIAO DỊCH KHÔNG HƯỞNG QUYỀN", "vid": MKT, "illus": VM, "titleAt": [0, "Giờ"]},
    {"type": "timeline", "at": 2, "items": [{"year": "NGÀY KHÔNG HƯỞNG QUYỀN", "text": "mua từ ngày này: không nhận đợt cổ tức", "at": [2, None, 0, 0.05]},
                                           {"year": "MỘT PHIÊN SAU", "text": "ngày đăng ký cuối cùng", "at": 4},
                                           {"year": "VÀI TUẦN · VÀI THÁNG", "text": "tiền cổ tức về tài khoản", "at": 5}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "SÁNG HÔM ẤY", "at": 6, "sm": True}, {"text": "GIÁ THAM CHIẾU ĐƯỢC ĐIỀU CHỈNH XUỐNG", "at": [7, "Giá"], "acc": True},
                                          {"text": "đúng bằng phần cổ tức sắp chia", "at": [7, "đúng"], "sm": True}]},
    {"type": "bars", "at": 8, "title": "GIÁ THAM CHIẾU (Đ)", "unit": "GIÁ ĐÓNG CỬA − CỔ TỨC TIỀN · " + H1,
     "items": [{"k": "PHIÊN TRƯỚC", "v": 40000, "lbl": "40.000", "at": [8, "bốn"]}, {"k": "NGÀY KHÔNG HƯỞNG QUYỀN", "v": 39000, "lbl": "39.000", "at": [9, "ba"], "acc": True}]},
    {"type": "question", "at": 10, "text": "Sao lại phải hạ giá?"},
    {"type": "broll", "at": 11, "vid": CAKE, "ms": 6, "veil": 0.55, "illus": VM,
     "kin": [{"text": "TIỀN ĐI RA KHỎI DOANH NGHIỆP", "at": 12, "sm": True}, {"text": "MỖI CỔ PHIẾU ĐÁNG ÍT HƠN ĐÚNG CHỪNG ẤY", "at": 13, "acc": True}]},
    {"type": "ledger", "at": 14, "title": "NGƯỜI CẦM 1.000 CỔ PHIẾU", "srcnote": H1,
     "rows": [{"k": "TRƯỚC", "v": "40 TRIỆU CỔ PHIẾU", "at": 15}, {"k": "SAU", "v": "39 TRIỆU + 1 TRIỆU CỔ TỨC", "at": 16}], "total": {"k": "CỘNG", "v": "VẪN 40 TRIỆU", "at": 17}},
    {"type": "slam", "at": 18, "text": "CẮT RA MỘT MIẾNG", "sub": "CÁI BÁNH KHÔNG TO THÊM", "subAt": 19},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "MUA ĐỂ ĂN CỔ TỨC"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "MUA ĐỂ\nĂN CỔ TỨC", "sub": "MỘT CHIẾN THUẬT NGHE RẤT HỢP LÝ", "vid": LAPTOP, "illus": VM, "titleAt": [0, "Vậy"]},
    {"type": "timeline", "at": 1, "items": [{"year": "1", "text": "mua ngay trước ngày không hưởng quyền", "at": [1, "Mua"]}, {"year": "2", "text": "nhận cổ tức", "at": [1, "nhận"]},
                                           {"year": "3", "text": "bán ra", "at": [1, "rồi"]}]},
    {"type": "ledger", "at": 2, "title": "1.000 CỔ PHIẾU · TỪNG BƯỚC (Đ)", "srcnote": H1 + " · PHÍ 0,3% MỖI CHIỀU · THUẾ BÁN 0,1%",
     "rows": [{"k": "MUA 40.000 + PHÍ", "v": "− 40.120.000", "at": 3}, {"k": "CỔ TỨC SAU THUẾ 5%", "v": "+ 950.000", "at": 5}, {"k": "BÁN 39.000 − PHÍ, THUẾ", "v": "+ 38.844.000", "at": 7}],
     "total": {"k": "KẾT QUẢ", "v": "− 326.000", "at": 8}},
    {"type": "counter", "at": 9, "from": 326, "to": 326, "prefix": "− ", "suffix": " NGHÌN Đ", "label": "LỖ · NẾU BÁN Ở 39.000 KHI CỔ PHIẾU VỀ", "sub": {"text": "KÊNH TỰ TÍNH · " + H1, "at": 9}},
    {"type": "question", "at": 10, "text": "Nếu lúc ấy giá tăng lại?"},
    {"type": "myth", "at": 11, "mythLab": "LỜI NHỜ", "myth": "CỔ TỨC", "truthLab": "THẬT RA NHỜ", "truth": "GIÁ TĂNG", "strikeAt": [11, "lời"], "truthAt": [11, "nhờ"]},
    {"type": "kinetic", "at": 12, "items": [{"text": "GIÁ CŨNG CÓ THỂ GIẢM THÊM", "at": 12, "acc": True}, {"text": "tiền cổ tức về sau vài tuần, có khi vài tháng", "at": 13, "sm": True}]},
    {"type": "slam", "at": 15, "text": "KHÔNG PHẢI QUÀ MIỄN PHÍ", "sub": "TIỀN CỦA BẠN · TỪ TÚI NÀY SANG TÚI KIA · ĐÃ TRỪ THUẾ"},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "CỔ TỨC BẰNG CỔ PHIẾU"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CỤM CHỮ THỨ BA", "title": "CỔ TỨC\nBẰNG CỔ PHIẾU", "sub": "KHÔNG ĐỒNG TIỀN NÀO ĐI RA", "vid": CAKE, "ms": 12, "illus": VM, "titleAt": [0, "Cụm"]},
    {"type": "units", "at": 2, "title": "CỨ 100 CỔ PHIẾU · NHẬN THÊM 20 · " + H1, "total": 12, "cols": 12, "lit": 10, "litAt": [3, "Cứ"], "unitLabel": "PHẦN TRƯỚC KHI CHIA"},
    {"type": "counter", "at": 4, "from": 1200, "to": 1200, "suffix": " CỔ PHIẾU", "label": "TỪ 1.000 CỔ PHIẾU · TỶ LỆ 20%", "sub": {"text": "NGHE NHƯ ĐƯỢC CHO KHÔNG 200 CỔ PHIẾU", "at": 5}},
    {"type": "bars", "at": 6, "title": "GIÁ THAM CHIẾU (Đ)", "unit": "GIÁ ÷ (1 + 20%) · " + H1,
     "items": [{"k": "TRƯỚC", "v": 40000, "lbl": "40.000", "at": [7, "Bốn"]}, {"k": "NGÀY KHÔNG HƯỞNG QUYỀN", "v": 33333, "lbl": "≈ 33.333", "at": [7, "ba"], "acc": True}]},
    {"type": "ledger", "at": 8, "title": "NHÂN LÊN", "srcnote": H1,
     "rows": [{"k": "TRƯỚC", "v": "1.000 × 40.000 = 40 TRIỆU", "at": [8, None, 0, 0.05]}, {"k": "SAU", "v": "1.200 × ≈ 33.333 ≈ 40 TRIỆU", "at": [8, "mỗi"]}],
     "total": {"k": "CÁI BÁNH", "v": "CẮT NHỎ HƠN · KHÔNG TO RA", "at": 9}},
    {"type": "question", "at": 10, "text": "Vậy sao doanh nghiệp\nlại làm thế?"},
    {"type": "kinetic", "at": 11, "items": [{"text": "GIỮ TIỀN LẠI CHO KINH DOANH", "at": 11, "acc": True}, {"text": "giá thấp hơn · trông dễ mua hơn", "at": 12, "sm": True}]},
    {"type": "myth", "at": 13, "mythLab": "TRÔNG", "myth": "RẺ HƠN", "truthLab": "CHƯA CÓ NGHĨA LÀ", "truth": "RẺ HƠN", "strikeAt": [13, "chưa"], "truthAt": [13, "nó"]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "VẬY CỔ TỨC CÓ NGHĨA LÝ GÌ?"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "VẬY CỔ TỨC\nCÓ NGHĨA LÝ GÌ?", "sub": "Ý NGHĨA NẰM Ở CHỖ KHÁC", "vid": MKT, "ms": 14, "illus": VM, "titleAt": [0, "Nếu"]},
    {"type": "ledger", "at": 2, "title": "CỔ TỨC TIỀN MẶT ĐỀU ĐẶN NÓI GÌ", "rows": [{"k": "1", "v": "CÓ TIỀN THẬT ĐỂ TRẢ", "at": 2}, {"k": "2", "v": "TIỀN MẶT KHÓ LÀM ĐẸP HƠN LỢI NHUẬN", "at": 3},
                                                                                  {"k": "3", "v": "MỘT DÒNG TIỀN ĐỀU · KHÔNG CẦN BÁN", "at": 5}]},
    {"type": "source", "at": 7, "source": "VN-INDEX", "ref": "LÀ MỘT CHỈ SỐ GIÁ", "snippet": "giá giảm khi chia cổ tức được ghi nhận, nhưng [[tiền cổ tức không được cộng lại]] vào chỉ số",
     "hlAt": [9, "không"], "seal": "VÌ THẾ KÊNH LUÔN GHI: CHƯA TÍNH CỔ TỨC", "sealAt": [9, "chỉ"]},
    {"type": "kinetic", "at": 10, "items": [{"text": "VN-INDEX ĐI NGANG NHIỀU NĂM", "at": 10, "sm": True}, {"text": "CỔ ĐÔNG VẪN CÓ THỂ ĐÃ NHẬN CỔ TỨC", "at": [10, "người"], "acc": True},
                                          {"text": "phần ấy nằm ngoài biểu đồ", "at": [10, "nằm"], "sm": True}]},
    {"type": "slam", "at": 12, "text": "SO CÔNG BẰNG", "sub": "CỘNG CẢ PHẦN CỔ TỨC VÀO", "subAt": 12},
]}

CH["ch06"] = {"hud": {"k": "GIỚI HẠN", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "KHI NÀO PHÉP TÍNH\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": MAG, "ms": 10, "illus": VM, "titleAt": [0, "Và"]},
    {"type": "ledger", "at": 2, "title": "PHÉP TÍNH CÒN GIẢ ĐỊNH", "rows": [{"k": "1", "v": "GIÁ, CỔ TỨC, PHÍ: VÍ DỤ", "at": 2}, {"k": "2", "v": "NGÀY CHỐT: ĐỌC THÔNG BÁO GỐC", "at": 3},
                                                                          {"k": "3", "v": "GIÁ THAM CHIẾU = ĐIỂM XUẤT PHÁT", "at": 4}]},
    {"type": "ledger", "at": 5, "title": "BA CÂU KHI ĐỌC THÔNG BÁO CỔ TỨC", "rows": [{"k": "1", "v": "ĐỔI RA TỶ SUẤT TRÊN GIÁ MUA?", "at": 6}, {"k": "2", "v": "NGÀY NÀO · GIÁ CHỈNH BAO NHIÊU?", "at": 7},
                                                                                    {"k": "3", "v": "TIỀN HAY CỔ PHIẾU · SAU THUẾ?", "at": 8}]},
    {"type": "broll", "at": 9, "vid": CAKE, "ms": 16, "veil": 0.5, "illus": VM,
     "kin": [{"text": "KHÔNG NÓI CỔ PHIẾU NÀO TỐT", "at": 9, "sm": True}, {"text": "MIẾNG BÁNH CẮT RA ≠ CÁI BÁNH TO THÊM", "at": 10, "acc": True}]},
    {"type": "question", "at": 11, "text": "Lần đầu nhận cổ tức, bạn có bất ngờ\nkhi giá giảm đúng hôm ấy?"},
    {"type": "kinetic", "at": 12, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 12}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [12, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
SPEC = {
    "title": "Cổ Tức 10% Là 10% Của Cái Gì? Giải Mã Một Tờ Thông Báo Cổ Tức",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 25, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["cổ", "tức", "mệnh", "giá", "bánh", "quyền", "thuế"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Cổ Tức 10% Là 10% Của Cái Gì? Giải Mã Một Tờ Thông Báo Cổ Tức",
                   "Vì Sao Giá Cổ Phiếu Tự Giảm Đúng Ngày Chia Cổ Tức? Ngày Không Hưởng Quyền Giải Thích Bằng Số",
                   "Mua Cổ Phiếu Để “Ăn Cổ Tức” Có Lời Không? Phép Tính Trên 1.000 Cổ Phiếu"],
        "summary": "Một tờ thông báo cổ tức có ba cụm chữ: “cổ tức bằng tiền 10%”, “ngày giao dịch không hưởng quyền”, “cổ tức bằng cổ phiếu”. Video giải "
                   "mã từng cụm bằng một cổ phiếu ví dụ giá 40.000 đ: 10% là 10% mệnh giá (tỷ suất chỉ 2,5%), vì sao giá tham chiếu tự giảm đúng ngày không "
                   "hưởng quyền, phép tính “mua để ăn cổ tức” trên 1.000 cổ phiếu, cổ tức bằng cổ phiếu cắt bánh thành miếng nhỏ hơn, và vì sao VN-Index "
                   "chưa tính cổ tức.",
        "more": [Y4["more"][0],
                 "📐 CÁCH KÊNH TÍNH: VÍ DỤ GIẢ ĐỊNH: mệnh giá 10.000 đ; cổ tức tiền 10% = 1.000 đ/cp; thuế TNCN 5% → thực nhận 950 đ; giá 40.000 đ → tỷ "
                 "suất 2,5%. Ngày không hưởng quyền: giá tham chiếu 40.000 − 1.000 = 39.000. “Mua để ăn cổ tức” 1.000 cp, phí 0,3% mỗi chiều, thuế bán "
                 "0,1%, bán khi cổ phiếu về tài khoản (T+2), giả sử giá vẫn 39.000: −326.000 đ. Cổ tức cổ phiếu 20%: 1.000 → 1.200 cp, giá 40.000 ÷ 1,2 ≈ 33.333, tổng vẫn ≈ 40 triệu. "
                 "Mức phí là ví dụ, mỗi công ty chứng khoán một khác; ngày chốt quyền đọc trong thông báo của từng doanh nghiệp."],
        "chapter_titles": {"ch00": "Mở đầu: một tờ thông báo, ba cụm chữ", "ch01": "Cổ tức 10% là 10% của cái gì?", "ch02": "Ngày giá tự giảm: ngày không hưởng quyền",
                           "ch03": "Mua để ăn cổ tức: phép tính 1.000 cổ phiếu", "ch04": "Cổ tức bằng cổ phiếu", "ch05": "Vậy cổ tức có nghĩa lý gì?",
                           "ch06": "Khi nào phép tính này không đúng với bạn"},
        "sources": ["https://vnexpress.net/gia-tham-chieu-4297099.html", "https://luatminhkhue.vn/cach-tinh-thue-thu-nhap-ca-nhan-khi-nhan-co-tuc-bang-co-phieu-loi-tuc-ghi-tang-von.aspx",
                    "https://luatduonggia.vn/phap-luat/co-tuc-bang-co-phieu-la-gi-cach-tinh-gia-dieu-chinh-khi-chia/"],
        "hashtags": ["ChứngKhoán", "CổTức", "NgàyKhôngHưởngQuyền", "ChứngKhoánTừSố0", "BiểuĐồBiếtNói"],
        "tags": ["cổ tức là gì", "cổ tức 10% là bao nhiêu", "ngày giao dịch không hưởng quyền", "tỷ suất cổ tức", "cổ tức bằng cổ phiếu", "giá tham chiếu",
                 "thuế cổ tức 5%", "chứng khoán cho người mới", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: phép tính do kênh tự lập (ví dụ giả định); quy tắc cổ tức, thuế và giá tham chiếu theo quy định và tài liệu hướng dẫn hiện hành.",
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
