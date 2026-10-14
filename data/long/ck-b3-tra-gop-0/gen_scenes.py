"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK B3 "Trả góp 0%".

    python data/long/ck-b3-tra-gop-0/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (VÍ DỤ GIẢ ĐỊNH: máy 20 triệu, giảm 1,5 triệu khi trả thẳng, phí chuyển đổi 3%).
Luật kênh: chỉ giáo dục; không tên cửa hàng/ngân hàng/công ty tài chính/sản phẩm; mọi cảnh số của ví dụ ghi "VÍ DỤ GIẢ ĐỊNH".
Áp luật studio (14/10/2026): cảnh myth / source / units; bốn cột giá dựng dần trên cùng một dạng biểu đồ (lộ trình "bốn cái giá").
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
assert round(R["apr"]["both"]) == 20 and round(R["apr"]["discount_only"]) == 15
HYPO = "VÍ DỤ GIẢ ĐỊNH · MÁY 20 TRIỆU, GIẢM 1,5 TRIỆU KHI TRẢ THẲNG, PHÍ 3%"
H1 = "VÍ DỤ GIẢ ĐỊNH"
VM = "VIDEO MINH HỌA"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI TẤM BIỂN"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "7568745", "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỘT CHIẾC ĐIỆN THOẠI", "at": [0, "Bạn"], "sm": True}, {"text": "20 TRIỆU ĐỒNG", "at": [1, "hai"], "acc": True}, {"text": "và hai tấm biển", "at": 2, "sm": True}]},
    {"type": "ledger", "at": 3, "title": "HAI TẤM BIỂN", "srcnote": H1, "rows": [{"k": "BIỂN 1 · TRẢ THẲNG", "v": "GIẢM NGAY 1,5 TRIỆU", "at": 3}, {"k": "BIỂN 2 · TRẢ GÓP", "v": "0% LÃI SUẤT · 12 THÁNG", "at": 4}],
     "total": {"k": "MỖI THÁNG", "v": "KHOẢNG 1,7 TRIỆU", "at": 5}},
    {"type": "bars", "at": 6, "title": "NGHE THÌ NHẸ HƠN HẲN (TRIỆU ĐỒNG)", "unit": H1,
     "items": [{"k": "TRẢ MỘT LẦN", "v": 18.5, "lbl": "18,5", "at": [6, "mười"]}, {"k": "MỖI THÁNG", "v": 1.7, "lbl": "≈ 1,7", "at": [6, None, 0, 0.05], "acc": True}]},
    {"type": "question", "at": 8, "text": "Nếu lãi là 0,\nthì ai trả tiền lãi?"},
    {"type": "kinetic", "at": 11, "items": [{"text": "CÙNG MỘT CHIẾC ĐIỆN THOẠI", "at": [12, "Cùng"], "sm": True}, {"text": "BỐN CÁI GIÁ", "at": [12, "bốn"], "acc": True},
                                           {"text": "dựng lên từng cột một", "at": 13, "sm": True}]},
    {"type": "units", "at": 14, "title": "TỚI CỘT THỨ TƯ: SỐ 0 TƯƠNG ĐƯƠNG BAO NHIÊU % MỘT NĂM?", "total": 4, "cols": 4, "lit": 4, "litAt": [14, "Tới"], "unitLabel": "CÁI GIÁ"},
    {"type": "brand", "at": 15, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "AI TRẢ TIỀN LÃI?"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "AI TRẢ\nTIỀN LÃI?", "sub": "TIỀN KHÔNG BAO GIỜ MIỄN PHÍ", "vid": "4109601", "illus": VM, "titleAt": [0, "tiền"]},
    {"type": "timeline", "at": 1, "items": [{"year": "BƯỚC 1", "text": "một bên ứng tiền cho cửa hàng thay bạn", "at": 1},
                                           {"year": "BÊN ẤY", "text": "công ty tài chính, hoặc ngân hàng qua thẻ", "at": 2},
                                           {"year": "VÀ", "text": "họ không cho vay không công", "at": 3}]},
    {"type": "question", "at": 4, "text": "Vậy tiền lãi đi đâu?"},
    {"type": "ledger", "at": 5, "title": "CÓ NGƯỜI TRẢ HỘ BẠN", "rows": [{"k": "AI", "v": "HÃNG SẢN XUẤT · HOẶC CỬA HÀNG", "at": 6}, {"k": "VỚI HỌ", "v": "MỘT KHOẢN CHI ĐỂ BÁN HÀNG", "at": 7}]},
    {"type": "myth", "at": 8, "mythLab": "TRÊN TẤM BIỂN", "myth": "LÃI SUẤT 0%", "truthLab": "VỀ BẢN CHẤT", "truth": "MỘT DẠNG KHUYẾN MÃI", "strikeAt": [8, "thường"], "truthAt": [8, "một"]},
    {"type": "broll", "at": 10, "vid": "6114643", "veil": 0.55, "illus": VM,
     "kin": [{"text": "HOÀN TOÀN BÌNH THƯỜNG", "at": 10, "sm": True}, {"text": "NHƯNG KHUYẾN MÃI THƯỜNG KHÔNG CỘNG DỒN", "at": [12, "thường"], "acc": True},
             {"text": "và cái giá thứ hai xuất hiện", "at": 13, "sm": True}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "CÁI GIÁ THỨ NHẤT VÀ THỨ HAI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "CÁI GIÁ THỨ NHẤT\nVÀ THỨ HAI", "sub": "TRẢ THẲNG · TRẢ GÓP", "vid": "5644247", "illus": VM, "titleAt": [0, "Cái"]},
    {"type": "bars", "at": 1, "title": "CÙNG MỘT CHIẾC MÁY (TRIỆU ĐỒNG)", "unit": H1,
     "items": [{"k": "① TRẢ THẲNG · GIẢM 1,5", "v": 18.5, "lbl": "18,5", "at": [1, "Bạn"]}, {"k": "② TRẢ GÓP 0% · 12 THÁNG", "v": 20, "lbl": "20", "at": [4, "Tổng"], "acc": True}]},
    {"type": "counter", "at": 5, "from": 1.5, "to": 1.5, "suffix": " TRIỆU", "label": "KHOẢN GIẢM GIÁ BẠN KHÔNG CÒN ĐƯỢC NHẬN", "sub": {"text": "CÁI GIÁ CỦA VIỆC ĐƯỢC TRẢ CHẬM · " + H1, "at": 7}},
    {"type": "myth", "at": 8, "mythLab": "KHÔNG AI GỌI NÓ LÀ", "myth": "TIỀN LÃI", "truthLab": "NHƯNG NÓ LÀM ĐÚNG VIỆC ẤY", "truth": "TRẢ THÊM ĐỂ TRẢ MUỘN", "strikeAt": [9, "Nhưng"], "truthAt": [10, "Bạn"]},
    {"type": "source", "at": 11, "source": "BÁO CHÍ · NĂM 2013 · SO GIÁ MỘT MẪU ĐIỆN THOẠI", "ref": "GIÁ TRẢ GÓP ĐƯỢC BÁO", "snippet": "cao hơn giá mua đứt ngoài thị trường [[khoảng 2 triệu đồng]]",
     "hlAt": [13, "cao"], "seal": "CHUYỆN CŨ · CÁCH KIỂM TRA VẪN DÙNG ĐƯỢC", "sealAt": [14, "Chuyện"]},
    {"type": "kinetic", "at": 15, "items": [{"text": "TA CÓ HAI CỘT", "at": 15, "sm": True}, {"text": "NHƯNG CÒN NHỮNG DÒNG CHỮ NHỎ", "at": [15, "Nhưng"], "acc": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CÁI GIÁ THỨ BA: CÁC LOẠI PHÍ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CÁI GIÁ THỨ BA", "sub": "LÃI LÀ 0 · PHÍ THÌ CHƯA CHẮC", "vid": "8471105", "illus": VM, "titleAt": [0, "Nhưng"]},
    {"type": "ledger", "at": 1, "title": "PHÍ CÓ THỂ ĐI KÈM TRẢ GÓP", "srcnote": "THEO BÁO CHÍ VÀ BÀI HƯỚNG DẪN TÀI CHÍNH · MỖI CHƯƠNG TRÌNH MỘT KHÁC",
     "rows": [{"k": "QUA THẺ TÍN DỤNG", "v": "PHÍ CHUYỂN ĐỔI TRẢ GÓP", "at": 2}, {"k": "QUA CÔNG TY TÀI CHÍNH", "v": "PHÍ HỒ SƠ · BẢO HIỂM KHOẢN VAY", "at": 3},
              {"k": "CÓ NƠI", "v": "PHÍ THU HỘ MỖI THÁNG", "at": 4}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "CÓ CHƯƠNG TRÌNH MIỄN HẾT", "at": [6, "Có"]}, {"text": "CÓ CHƯƠNG TRÌNH THU MỘT, HAI LOẠI", "at": [6, "thu"], "acc": True}]},
    {"type": "myth", "at": 7, "mythLab": "CÂU HAY HỎI", "myth": "LÃI SUẤT BAO NHIÊU?", "truthLab": "CÂU CẦN HỎI", "truth": "TỔNG CỘNG TÔI TRẢ BAO NHIÊU?", "strikeAt": [7, "không"], "truthAt": [8, "tổng"]},
    {"type": "counter", "at": 9, "from": 0, "to": 600, "suffix": " NGHÌN", "until": [10, "sáu"], "label": "PHÍ CHUYỂN ĐỔI 3% CỦA 20 TRIỆU", "sub": {"text": H1 + " · KHÔNG PHẢI MỨC CỦA CHƯƠNG TRÌNH NÀO", "at": 9}},
    {"type": "bars", "at": 11, "title": "CÙNG MỘT CHIẾC MÁY (TRIỆU ĐỒNG)", "unit": HYPO,
     "items": [{"k": "① TRẢ THẲNG", "v": 18.5, "lbl": "18,5", "at": [11, None, 0, 0.05]}, {"k": "② TRẢ GÓP 0%", "v": 20, "lbl": "20", "at": [11, None, 0, 0.3]},
               {"k": "③ TRẢ GÓP + PHÍ", "v": 20.6, "lbl": "20,6", "at": [12, "Hai"], "acc": True}]},
    {"type": "slam", "at": 13, "text": "+ 2,1 TRIỆU", "sub": "SO VỚI TRẢ THẲNG · " + H1, "subAt": 13},
    {"type": "question", "at": 14, "text": "2,1 triệu ấy là\nbao nhiêu % một năm?"},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "SỐ 0 TƯƠNG ĐƯƠNG BAO NHIÊU?"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "CON SỐ 0\nTƯƠNG ĐƯƠNG BAO NHIÊU?", "sub": "NHÌN NÓ NHƯ MỘT KHOẢN VAY", "vid": "8479058", "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "myth", "at": 1, "mythLab": "TƯỞNG LÀ VAY", "myth": "20 TRIỆU", "truthLab": "THẬT SỰ VAY", "truth": "18,5 TRIỆU", "strikeAt": [1, "không"], "truthAt": [2, "mười"]},
    {"type": "ledger", "at": 3, "title": "KHOẢN VAY NÀY", "srcnote": HYPO, "rows": [{"k": "NHẬN HÔM NAY", "v": "18,5 TRIỆU", "at": [3, None, 0, 0.05]}, {"k": "TRẢ LẠI", "v": "20,6 TRIỆU · 12 THÁNG ĐỀU", "at": [3, "hai"]}],
     "total": {"k": "LÃI SUẤT?", "v": "…", "at": 4}},
    {"type": "counter", "at": 5, "from": 0, "to": 20, "prefix": "≈ ", "suffix": "%", "until": [6, "hai"], "label": "MỘT NĂM · LÃI SUẤT TƯƠNG ĐƯƠNG", "sub": {"text": "KÊNH TỰ TÍNH · " + HYPO, "at": 7}},
    {"type": "kinetic", "at": 8, "items": [{"text": "TẤM BIỂN KHÔNG SAI", "at": [8, "và"], "acc": True}, {"text": "lãi suất trong hợp đồng đúng là 0", "at": 9, "sm": True},
                                          {"text": "chi phí của bạn không nằm ở dòng lãi suất", "at": 10, "sm": True}]},
    {"type": "ledger", "at": 11, "title": "ƯỚC LƯỢNG KHÔNG CẦN MÁY TÍNH", "srcnote": "CÁCH TÍNH GẦN ĐÚNG CHO TRẢ GÓP ĐỀU · " + H1,
     "rows": [{"k": "PHẦN TRẢ THÊM ÷ SỐ THẬT SỰ VAY", "v": "2,1 ÷ 18,5 ≈ 11%", "at": 13}, {"k": "NHÂN GẦN GẤP ĐÔI", "v": "VÌ TRUNG BÌNH CHỈ NỢ MỘT NỬA", "at": 16}],
     "total": {"k": "KẾT QUẢ", "v": "≈ 20%/NĂM", "at": 17}},
    {"type": "bars", "at": 18, "title": "LÃI SUẤT TƯƠNG ĐƯƠNG (% MỘT NĂM)", "unit": HYPO,
     "items": [{"k": "MẤT GIẢM GIÁ + PHÍ", "v": 20.3, "lbl": "≈ 20", "at": [18, None, 0, 0.05], "acc": True}, {"k": "CHỈ MẤT GIẢM GIÁ", "v": 14.6, "lbl": "≈ 15", "at": [19, "mười"]},
               {"k": "CHỈ CHỊU PHÍ", "v": 5.5, "lbl": "≈ 5,5", "at": [20, "năm"]}, {"k": "KHÔNG MẤT GÌ", "v": 0.2, "lbl": "0", "at": [22, "không"]}]},
    {"type": "broll", "at": 23, "vid": "6114643", "ms": 2, "veil": 0.55, "illus": VM,
     "kin": [{"text": "0% THẬT CŨNG CÓ · VÀ KHÔNG HIẾM", "at": 23, "acc": True}, {"text": "khi ấy tiền của bạn còn sinh lãi thêm vài tháng", "at": 24, "sm": True},
             {"text": "con số 0 không nói dối · nó chưa phải cả câu chuyện", "at": 25, "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "CÁI GIÁ THỨ TƯ: TRỄ MỘT KỲ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "CÁI GIÁ THỨ TƯ", "sub": "KHI BẠN TRỄ MỘT KỲ", "vid": "7841584", "illus": VM, "titleAt": [0, "Mọi"]},
    {"type": "units", "at": 1, "title": "GIẢ ĐỊNH CỦA MỌI PHÉP TÍNH: 12 THÁNG, TRẢ ĐỦ, ĐÚNG NGÀY", "total": 12, "cols": 12, "lit": 12, "litAt": [1, "Mười"], "unitLabel": "KỲ TRẢ ĐÚNG HẠN"},
    {"type": "ledger", "at": 3, "title": "TRỄ MỘT KỲ", "srcnote": "TUỲ TỪNG HỢP ĐỒNG · ĐỌC ĐIỀU KHOẢN CỦA BẠN",
     "rows": [{"k": "ƯU ĐÃI", "v": "CÓ THỂ KHÔNG CÒN", "at": 3}, {"k": "THÊM", "v": "PHÍ PHẠT TRẢ CHẬM", "at": 4}, {"k": "Ở MỘT SỐ HỢP ĐỒNG", "v": "PHẦN CÒN LẠI BỊ TÍNH LÃI", "at": 5}]},
    {"type": "timeline", "at": 6, "items": [{"year": "QUA THẺ", "text": "khoản góp mỗi tháng cộng vào sao kê", "at": 6}, {"year": "TRẢ THIẾU", "text": "phần còn thiếu bị tính lãi thẻ", "at": 7},
                                           {"year": "LÃI THẺ", "text": "thường 20–40% một năm", "at": [8, "thường"]}]},
    {"type": "broll", "at": 9, "vid": "8471105", "ms": 4, "veil": 0.55, "illus": VM,
     "kin": [{"text": "1,7 TRIỆU MỖI THÁNG NGHE NHỎ", "at": 10, "sm": True}, {"text": "RỒI THÊM MỘT MÓN · RỒI MỘT MÓN NỮA", "at": [11, "Rồi"], "acc": True},
             {"text": "từng khoản đều nhỏ · cộng lại thì không nhỏ", "at": 12, "sm": True}]},
    {"type": "slam", "at": 13, "text": "CỘNG MỌI KHOẢN GÓP LẠI", "sub": "CON SỐ ẤY MỚI LÀ THỨ BẠN CAM KẾT", "subAt": 14},
    {"type": "ledger", "at": 15, "title": "LỊCH TRẢ TIỀN IN SẴN", "rows": [{"k": "MỖI KỲ", "v": "BAO NHIÊU?", "at": [16, "mỗi"]}, {"k": "NGÀY NÀO", "v": "TRẢ?", "at": [16, "vào"]},
                                                                          {"k": "TỔNG CỘNG", "v": "BAO NHIÊU?", "at": [16, "tổng"]}], "total": {"k": "MỘT TỜ GIẤY", "v": "TRẢ LỜI ĐIỀU TẤM BIỂN KHÔNG NHẮC", "at": 18}},
]}

CH["ch06"] = {"hud": {"k": "GIỚI HẠN", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "KHI NÀO PHÉP TÍNH\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": "8479058", "ms": 8, "illus": VM, "titleAt": [0, "Và"]},
    {"type": "ledger", "at": 1, "title": "PHÉP TÍNH CÒN GIẢ ĐỊNH", "rows": [{"k": "1", "v": "MÁY, MỨC GIẢM, MỨC PHÍ: GIẢ ĐỊNH", "at": 1}, {"k": "2", "v": "TRẢ THẲNG CHƯA CHẮC ĐƯỢC GIẢM", "at": 3},
                                                                          {"k": "3", "v": "TRẢ THẲNG CŨNG CÓ CÁI GIÁ", "at": 5}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "DỒN HẾT TIỀN DỰ PHÒNG VÀO MỘT MÓN ĐỒ", "at": 6, "sm": True}, {"text": "CÓ KHI CÒN ĐẮT HƠN MỌI KHOẢN PHÍ", "at": [6, "có"], "acc": True},
                                          {"text": "kênh không nói cách nào tốt hơn", "at": 7, "sm": True}]},
    {"type": "ledger", "at": 8, "title": "BA CÂU HỎI MANG RA CỬA HÀNG", "rows": [{"k": "1", "v": "TRẢ THẲNG: GIÁ BAO NHIÊU, Ở ĐÂY VÀ NƠI KHÁC?", "at": 9}, {"k": "2", "v": "TRẢ GÓP: TỔNG CỘNG TRẢ BAO NHIÊU?", "at": 10},
                                                                               {"k": "3", "v": "TRỄ MỘT KỲ THÌ SAO?", "at": 11}], "total": {"k": "CÂU 2 − CÂU 1", "v": "GIÁ THẬT CỦA VIỆC TRẢ CHẬM", "at": 12}},
    {"type": "broll", "at": 14, "vid": "5644247", "ms": 2, "veil": 0.5, "illus": VM,
     "kin": [{"text": "CON SỐ 0 TRÊN TẤM BIỂN LÀ THẬT", "at": 14}, {"text": "HÃY TÌM NHỮNG CON SỐ NGOÀI TẤM BIỂN", "at": [15, "tìm"], "acc": True}]},
    {"type": "question", "at": 16, "text": "Lần mua trả góp ấy, bạn có hỏi\ntổng số tiền phải trả không?"},
    {"type": "kinetic", "at": 17, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 17}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [17, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
SPEC = {
    "title": "Trả Góp 0%: Bạn Thật Sự Trả Bao Nhiêu? Một Chiếc Điện Thoại, Bốn Cái Giá",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 25, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["không", "phí", "giá", "lãi", "thẳng", "góp", "tổng"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Trả Góp 0%: Bạn Thật Sự Trả Bao Nhiêu? Một Chiếc Điện Thoại, Bốn Cái Giá",
                   "Trả Góp 0% Có Thật Là 0%? Ba Chỗ Tiền Của Bạn Có Thể Đi Mất",
                   "“Lãi Suất 0%” Nhưng Tương Đương 20% Một Năm: Phép Tính Trả Góp Ít Ai Làm"],
        "summary": "Trả góp lãi suất 0%: nếu lãi là 0 thì ai trả tiền lãi? Video dựng bốn cái giá của cùng một chiếc điện thoại 20 triệu (ví dụ giả "
                   "định): trả thẳng có giảm giá, trả góp 0%, trả góp có phí, và cái giá khi trễ một kỳ. Kèm cách tự ước lượng lãi suất tương đương "
                   "mà không cần máy tính, trường hợp 0% đúng là 0%, và ba câu hỏi nên mang theo ra cửa hàng.",
        "more": [Y4["more"][0],
                 "📐 CÁCH KÊNH TÍNH: VÍ DỤ GIẢ ĐỊNH: máy 20 triệu; trả thẳng được giảm 1,5 triệu (trả 18,5); trả góp 0% trong 12 tháng (trả 20); phí "
                 "chuyển đổi 3% (trả 20,6). Lãi suất tương đương là lãi suất của khoản “nhận 18,5 hôm nay, trả 20,6 chia đều 12 tháng” (IRR theo tháng "
                 "× 12) ≈ 20%/năm; nếu chỉ mất khoản giảm giá ≈ 15%; nếu chỉ chịu phí ≈ 5,5%; không mất gì = 0%. Mức giảm giá và mức phí là giả định, "
                 "không phải của chương trình nào: chương trình bạn gặp có thể không có phí, hoặc không có giảm giá khi trả thẳng."],
        "chapter_titles": {"ch00": "Mở đầu: hai tấm biển", "ch01": "Ai trả tiền lãi?", "ch02": "Cái giá thứ nhất và thứ hai: mất giảm giá",
                           "ch03": "Cái giá thứ ba: các loại phí", "ch04": "Con số 0 tương đương bao nhiêu % một năm?", "ch05": "Cái giá thứ tư: khi bạn trễ một kỳ",
                           "ch06": "Khi nào phép tính này không đúng với bạn"},
        "sources": ["https://vov.vn/kinh-te/su-that-lai-suat-tra-gop-0-cai-bay-bi-an-614131.vov",
                    "https://vnexpress.net/map-mo-khuyen-mai-mua-hang-tra-gop-2695052.html",
                    "https://vietnamfinance.vn/tra-gop-lai-suat-0-tro-thanh-con-dau-dau-voi-cac-cong-ty-tai-chinh-d9588.html"],
        "hashtags": ["TàiChínhCáNhân", "TrảGóp", "TrảGóp0", "LãiSuất", "BiểuĐồBiếtNói"],
        "tags": ["trả góp 0%", "trả góp 0% có thật không", "phí chuyển đổi trả góp", "mua điện thoại trả góp", "lãi suất thật trả góp", "trả góp qua thẻ tín dụng",
                 "tài chính cá nhân", "chi phí ẩn trả góp", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: phép tính trả góp do kênh tự lập (ví dụ giả định); các loại phí và ví dụ giá theo báo chí.",
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
