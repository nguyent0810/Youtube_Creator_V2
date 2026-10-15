"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK B4 "Mua xe".

    python data/long/ck-b4-mua-xe/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (VÍ DỤ GIẢ ĐỊNH: xe 700 triệu, đăng ký Hà Nội, trả góp 70% / 84 tháng).
Luật kênh: chỉ giáo dục; không tên hãng/mẫu xe/đại lý/ngân hàng/công ty bảo hiểm; mọi cảnh số của ví dụ ghi "VÍ DỤ GIẢ ĐỊNH".
Lộ trình "đồng hồ chạy dần": cuối mỗi chương một cảnh counter là số đồng hồ đang chỉ. Luật 15/10: "≈" thay "~" trước số; counter có prefix đứng yên.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
B3 = json.loads((D.parent / "ck-b3-tra-gop-0" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(B3["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
assert R["onroad"]["lan_banh"] == 800 and round(R["own_total_month_y1"]) == 10 and round(R["breakeven_taxi"]) == 15
assert round(R["loan"]["interest_5y"]) == 184 and round(R["net_5y"]["tra_thang"]) == 689 and round(R["net_5y"]["tra_gop"]) == 873
H1 = "VÍ DỤ GIẢ ĐỊNH"
HX = "VÍ DỤ GIẢ ĐỊNH · XE 700 TRIỆU · ĐĂNG KÝ HÀ NỘI"
VM = "VIDEO MINH HỌA"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "CHIẾC ĐỒNG HỒ TÍNH TIỀN"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "34539090", "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỘT CHUYẾN XE CÔNG NGHỆ", "at": [0, "Bạn"], "sm": True}, {"text": "CON SỐ NHẢY THEO TỪNG CÂY SỐ", "at": [1, "có"], "acc": True},
             {"text": "ai cũng thấy chiếc đồng hồ ấy", "at": 2, "sm": True}]},
    {"type": "counter", "at": 3, "from": 4, "to": 4, "suffix": " TRIỆU", "label": "MỖI THÁNG · TIỀN XE CÔNG NGHỆ", "sub": {"text": H1, "at": 3}},
    {"type": "question", "at": 4, "text": "Bốn triệu một tháng,\nsao không mua hẳn một chiếc xe?"},
    {"type": "broll", "at": 5, "vid": "9100884", "veil": 0.55, "illus": VM,
     "kin": [{"text": "XE CỦA BẠN CŨNG CÓ ĐỒNG HỒ", "at": 5, "acc": True}, {"text": "chỉ là không hiện lên màn hình nào", "at": 6, "sm": True},
             {"text": "và nó chạy cả khi xe nằm im", "at": 7, "sm": True}]},
    {"type": "ledger", "at": 8, "title": "BA LỐI ĐI · MỘT CHIẾC XE 700 TRIỆU", "srcnote": H1,
     "rows": [{"k": "1", "v": "TRẢ THẲNG", "at": [10, "trả"]}, {"k": "2", "v": "TRẢ GÓP", "at": [10, "trả", 1]}, {"k": "3", "v": "CHƯA MUA", "at": [10, "chưa"]}],
     "total": {"k": "MỖI CHƯƠNG", "v": "ĐỒNG HỒ CỘNG THÊM MỘT KHOẢN", "at": 9}},
    {"type": "brand", "at": 11, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "BẢY TRĂM THÀNH TÁM TRĂM"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "BẢY TRĂM\nTHÀNH TÁM TRĂM", "sub": "TRƯỚC KHI BÁNH XE KỊP LĂN", "vid": "7154229", "illus": VM, "titleAt": [0, "Khoản"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "GIÁ NIÊM YẾT 700 TRIỆU", "at": [1, "Giá"], "acc": True}, {"text": "muốn ra đường còn vài khoản phải nộp", "at": [1, "muốn"], "sm": True}]},
    {"type": "ledger", "at": 2, "title": "LỆ PHÍ TRƯỚC BẠ · Ô TÔ ≤ 9 CHỖ, LẦN ĐẦU", "srcnote": "THEO QUY ĐỊNH HIỆN HÀNH",
     "rows": [{"k": "MỨC CHUNG", "v": "10%", "at": [3, "mức"]}, {"k": "HÀ NỘI", "v": "12%", "at": [4, "Ở"]}], "total": {"k": "XE VÍ DỤ · HÀ NỘI", "v": "84 TRIỆU", "at": [5, "tám"]}},
    {"type": "bars", "at": 6, "title": "LỆ PHÍ TRƯỚC BẠ CỦA XE 700 TRIỆU (TRIỆU ĐỒNG)", "unit": H1,
     "items": [{"k": "NƠI THU 10%", "v": 70, "lbl": "70", "at": [6, "bảy"]}, {"k": "HÀ NỘI · 12%", "v": 84, "lbl": "84", "at": [6, "ít"], "acc": True}]},
    {"type": "myth", "at": 8, "mythLab": "TƯỞNG LÀ TÍNH THEO", "myth": "GIÁ TRÊN HỢP ĐỒNG", "truthLab": "THẬT RA THEO", "truth": "BẢNG GIÁ NHÀ NƯỚC", "strikeAt": [8, "không"], "truthAt": [8, "bảng"]},
    {"type": "source", "at": 10, "source": "THÔNG TƯ 155/2025 · TỪ 01/01/2026", "ref": "LỆ PHÍ CẤP BIỂN Ô TÔ ≤ 9 CHỖ · HÀ NỘI, TP.HCM",
     "snippet": "giảm từ 20 triệu xuống còn [[14 triệu đồng]] mỗi lần, mỗi xe", "hlAt": [11, "mười"], "seal": "ĐÃ ĐỐI CHIẾU BÁO CHÍ", "sealAt": 12},
    {"type": "ledger", "at": 13, "title": "LĂN BÁNH · XE VÍ DỤ", "srcnote": HX,
     "rows": [{"k": "GIÁ XE", "v": "700", "at": [13, None, 0, 0.05]}, {"k": "TRƯỚC BẠ + BIỂN + KHÁC", "v": "84 + 14 + 2", "at": [13, "bảy"]}],
     "total": {"k": "LĂN BÁNH (TRIỆU)", "v": "800", "at": [13, "tám"]}},
    {"type": "counter", "at": 14, "from": 0, "to": 100, "suffix": " TRIỆU", "until": 15, "label": "ĐỒNG HỒ · KHOẢN KHÔNG MUA THÊM ĐƯỢC GÌ", "sub": {"text": "VÀ KHÔNG AI TRẢ LẠI KHI BÁN XE", "at": 15}},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "TIỀN NUÔI XE"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "TIỀN NUÔI XE", "sub": "ĐỒNG HỒ CHUYỂN SANG TÍNH THEO THÁNG", "vid": "15341182", "illus": VM, "titleAt": [0, "Bây"]},
    {"type": "ledger", "at": 1, "title": "HAI KHOẢN AI CÓ XE CŨNG NỘP", "srcnote": "NĐ 90/2023 · NĐ 67/2023",
     "rows": [{"k": "PHÍ ĐƯỜNG BỘ", "v": "130 NGHÌN/THÁNG", "at": 2}, {"k": "BẢO HIỂM TNDS BẮT BUỘC", "v": "437 NGHÌN/NĂM · CHƯA THUẾ", "at": 3}],
     "total": {"k": "CỘNG LẠI", "v": "< 200 NGHÌN/THÁNG", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "KHOẢN LỚN NẰM Ở CHỖ KHÁC", "at": 5, "acc": True}, {"text": "và tuỳ cách bạn dùng xe", "at": [5, "và"], "sm": True}]},
    {"type": "broll", "at": 7, "vid": "5982899", "veil": 0.55, "illus": VM,
     "kin": [{"text": "GỬI XE · 1,5 TRIỆU/THÁNG", "at": 7, "sm": True}, {"text": "12.000 KM · 7 LÍT/100 KM · 24.000 Đ/LÍT", "at": 8, "sm": True},
             {"text": "≈ 1,7 TRIỆU TIỀN XĂNG MỖI THÁNG", "at": 9, "acc": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "CẦU ĐƯỜNG · RỬA XE · GỬI XE KHI ĐI CHƠI", "at": 10, "sm": True}, {"text": "những khoản nhỏ ít ai ghi lại", "at": [10, "những"], "acc": True}]},
    {"type": "bars", "at": 11, "title": "TIỀN NUÔI XE MỖI THÁNG · NĂM ĐẦU (TRIỆU ĐỒNG)", "unit": HX,
     "items": [{"k": "XĂNG", "v": 1.68, "lbl": "1,7", "at": [11, None, 0, 0.05]}, {"k": "GỬI XE", "v": 1.5, "lbl": "1,5", "at": [11, None, 0, 0.3]},
               {"k": "BẢO HIỂM VẬT CHẤT", "v": 0.875, "lbl": "≈ 0,9", "at": [12, "bảo"]}, {"k": "BẢO DƯỠNG", "v": 0.5, "lbl": "0,5", "at": [11, "sáu"]},
               {"k": "PHÍ + BẢO HIỂM BẮT BUỘC", "v": 0.17, "lbl": "0,2", "at": [12, "thêm"]}]},
    {"type": "counter", "at": 13, "from": 4.7, "to": 4.7, "suffix": " TRIỆU/THÁNG", "label": "ĐỒNG HỒ · TIỀN NUÔI XE NĂM ĐẦU", "sub": {"text": "ĐÃ NHIỀU HƠN 4 TRIỆU TIỀN XE CÔNG NGHỆ", "at": 14}},
    {"type": "question", "at": 15, "text": "Nhưng chiếc xe\nvẫn là của mình mà?"},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "KHOẢN KHÔNG AI GỬI HOÁ ĐƠN"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "KHOẢN KHÔNG AI\nGỬI HOÁ ĐƠN", "sub": "MẤT GIÁ", "vid": "32161278", "illus": VM, "titleAt": [0, "Khoản"]},
    {"type": "myth", "at": 1, "mythLab": "TƯỞNG LÀ", "myth": "XĂNG · GỬI XE", "truthLab": "THƯỜNG LỚN NHẤT", "truth": "MẤT GIÁ", "strikeAt": [1, "Mà"], "truthAt": [1, "mất"]},
    {"type": "kinetic", "at": 2, "items": [{"text": "KHÔNG AI GỬI HOÁ ĐƠN MẤT GIÁ", "at": 2, "acc": True}, {"text": "bạn chỉ thấy nó vào ngày bán xe", "at": 3, "sm": True},
                                          {"text": "giá xe cũ tuỳ dòng xe · tình trạng · thị trường", "at": 4, "sm": True}]},
    {"type": "bars", "at": 6, "title": "CHIẾC XE SAU 5 NĂM (TRIỆU ĐỒNG)", "unit": H1 + " · BÁN LẠI 55% GIÁ BAN ĐẦU",
     "items": [{"k": "MUA MỚI", "v": 700, "lbl": "700", "at": [6, None, 0, 0.05]}, {"k": "BÁN LẠI", "v": 385, "lbl": "385", "at": [7, "ba"]}, {"k": "MẤT GIÁ", "v": 315, "lbl": "315", "at": [8, "ba"], "acc": True}]},
    {"type": "counter", "at": 9, "from": 5.25, "to": 5.25, "suffix": " TRIỆU/THÁNG", "label": "TIỀN MẤT GIÁ · CHIA CHO 60 THÁNG", "sub": {"text": H1, "at": 9}},
    {"type": "kinetic", "at": 10, "items": [{"text": "CHO AI ĐÓ THUÊ XE VỚI GIÁ ẤY", "at": [10, "nếu"], "sm": True}, {"text": "CHỈ VỪA ĐỦ BÙ PHẦN MẤT GIÁ", "at": [10, "tiền"], "acc": True}]},
    {"type": "ledger", "at": 11, "title": "ĐỒNG HỒ ĐANG CHỈ · MỖI THÁNG", "srcnote": HX,
     "rows": [{"k": "TIỀN NUÔI XE", "v": "≈ 4,7 TRIỆU", "at": [12, "Tiền"]}, {"k": "TIỀN MẤT GIÁ", "v": "≈ 5,2 TRIỆU", "at": [12, "mất"]}],
     "total": {"k": "CỘNG", "v": "GẦN 10 TRIỆU", "at": 13}},
    {"type": "counter", "at": 14, "from": 11.5, "to": 11.5, "suffix": " TRIỆU/THÁNG", "label": "TRẢ THẲNG · CHI RÒNG 5 NĂM ≈ 689 TRIỆU", "sub": {"text": "GỒM CẢ 100 TRIỆU LĂN BÁNH · KÊNH TỰ TÍNH", "at": 15}},
    {"type": "bars", "at": 17, "title": "MỖI THÁNG (TRIỆU ĐỒNG)", "unit": H1,
     "items": [{"k": "XE CÔNG NGHỆ", "v": 4, "lbl": "4", "at": [17, "bốn"]}, {"k": "TRẢ THẲNG", "v": 11.5, "lbl": "≈ 11,5", "at": [17, "Gần"], "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "TRẢ GÓP: THÊM MỘT CHIẾC ĐỒNG HỒ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "TRẢ GÓP", "sub": "THÊM MỘT CHIẾC ĐỒNG HỒ", "vid": "7154228", "illus": VM, "titleAt": [0, "Nhưng"]},
    {"type": "ledger", "at": 1, "title": "KHOẢN VAY VÍ DỤ", "srcnote": H1,
     "rows": [{"k": "TRẢ TRƯỚC 30% + LĂN BÁNH", "v": "310 TRIỆU", "at": 2}, {"k": "VAY", "v": "490 TRIỆU · 7 NĂM · GỐC ĐỀU", "at": 3}]},
    {"type": "source", "at": 4, "source": "BÁO CHÍ · THÁNG 10/2026 · LÃI VAY MUA XE", "ref": "ƯU ĐÃI NĂM ĐẦU ≈ 7–9%/NĂM",
     "snippet": "hết ưu đãi, nhiều khoản thả nổi lên [[12–15% một năm]], có người gần 20%", "hlAt": [5, "mười"], "seal": "KHÔNG NÊU TÊN NGÂN HÀNG", "sealAt": 6},
    {"type": "bars", "at": 7, "title": "KHOẢN TRẢ MỖI THÁNG (TRIỆU ĐỒNG)", "unit": H1 + " · 8% NĂM ĐẦU, RỒI 13%",
     "items": [{"k": "THÁNG 1", "v": 9.1, "lbl": "9,1", "at": [7, "chín"]}, {"k": "THÁNG 12", "v": 8.67, "lbl": "8,7", "at": [8, "tám"]},
               {"k": "THÁNG 13", "v": 10.38, "lbl": "10,4", "at": [9, "mười"], "acc": True}]},
    {"type": "slam", "at": 10, "text": "+ 1,7 TRIỆU", "sub": "CHỈ SAU MỘT THÁNG · " + H1, "subAt": 10},
    {"type": "kinetic", "at": 12, "items": [{"text": "CÓ BÁO · TRONG HỢP ĐỒNG", "at": 12, "acc": True}, {"text": "lãi cơ sở + biên độ", "at": [12, "Lãi"], "sm": True},
                                           {"text": "lãi cơ sở có thể lên hoặc xuống", "at": [12, "lãi", 2], "sm": True}]},
    {"type": "counter", "at": 13, "from": 0, "to": 184, "suffix": " TRIỆU", "until": [13, "một"], "label": "TIỀN LÃI 5 NĂM ĐẦU", "sub": {"text": "CẢ 7 NĂM ≈ 203 TRIỆU · " + H1, "at": 14}},
    {"type": "bars", "at": 15, "title": "CHI RÒNG 5 NĂM (TRIỆU ĐỒNG)", "unit": "KÊNH TỰ TÍNH · " + H1,
     "items": [{"k": "TRẢ THẲNG", "v": 689, "lbl": "689", "at": [15, None, 0, 0.05]}, {"k": "TRẢ GÓP", "v": 873, "lbl": "873", "at": [15, "tám"], "acc": True}]},
    {"type": "counter", "at": 16, "from": 14.5, "to": 14.5, "suffix": " TRIỆU/THÁNG", "label": "ĐỒNG HỒ · NGƯỜI TRẢ GÓP", "sub": {"text": "CHƯA TRỪ LÃI GỬI CỦA PHẦN GIỮ LẠI", "at": 17}},
    {"type": "myth", "at": 18, "mythLab": "TRẢ GÓP KHÔNG LÀM", "myth": "CHIẾC XE ĐẮT HƠN", "truthLab": "NÓ LÀM", "truth": "VIỆC CÓ XE ĐẮT HƠN", "strikeAt": [19, "Nó"], "truthAt": [19, "việc"]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "LỐI THỨ BA: CHƯA MUA"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "LỐI THỨ BA:\nCHƯA MUA", "sub": "ÍT AI TÍNH ĐẾN", "vid": "36556681", "illus": VM, "titleAt": [0, "Còn"]},
    {"type": "ledger", "at": 1, "title": "NGƯỜI CHƯA MUA", "srcnote": H1,
     "rows": [{"k": "ĐI LẠI", "v": "XE CÔNG NGHỆ · TAXI · XE MÁY", "at": 1}, {"k": "MỖI THÁNG", "v": "4 TRIỆU", "at": 2}, {"k": "800 TRIỆU", "v": "TRONG SỔ TIẾT KIỆM", "at": 3}]},
    {"type": "counter", "at": 4, "from": 6.8, "to": 6.8, "suffix": "%/NĂM", "label": "TIẾT KIỆM 12 THÁNG · NHÓM NGÂN HÀNG LỚN", "sub": {"text": "THÁNG 9/2026", "at": 4}},
    {"type": "bars", "at": 5, "title": "MỖI THÁNG (TRIỆU ĐỒNG)", "unit": H1,
     "items": [{"k": "LÃI CỦA 800 TRIỆU", "v": 4.53, "lbl": "≈ 4,5", "at": [5, "bốn"], "acc": True}, {"k": "TIỀN XE CÔNG NGHỆ", "v": 4, "lbl": "4", "at": [5, "gần"]}]},
    {"type": "question", "at": 6, "text": "Phải đi nhiều tới mức nào\nthì mua xe mới đáng?"},
    {"type": "counter", "at": 7, "from": 15, "to": 15, "prefix": "≈ ", "suffix": " TRIỆU/THÁNG", "label": "MỨC CHI ĐI LẠI ĐỂ HAI BÊN NGANG NHAU SAU 5 NĂM", "sub": {"text": "KÊNH TỰ TÍNH · CÓ TÍNH LÃI TIẾT KIỆM · " + H1, "at": 8}},
    {"type": "broll", "at": 10, "vid": "11785816", "veil": 0.55, "illus": VM,
     "kin": [{"text": "CON SỐ ẤY CHỈ NÓI VỀ TIỀN", "at": 10, "acc": True}, {"text": "một đêm con ốm · một chuyến về quê ngày Tết", "at": 11, "sm": True},
             {"text": "những ngày mưa ngập không gọi được xe", "at": [11, "những"], "sm": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "VỚI NHIỀU GIA ĐÌNH", "at": 12, "sm": True}, {"text": "ĐÓ MỚI LÀ LÝ DO THẬT", "at": [12, "đó"], "acc": True},
                                           {"text": "có người chọn lối ở giữa: xe công nghệ + thuê xe tự lái", "at": 13, "sm": True}]},
]}

CH["ch06"] = {"hud": {"k": "GIỚI HẠN", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "KHI NÀO PHÉP TÍNH\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": "9130073", "illus": VM, "titleAt": [0, "Và"]},
    {"type": "ledger", "at": 2, "title": "ĐỒNG HỒ CHẠY KHÁC ĐI KHI", "rows": [{"k": "1", "v": "BẠN ĐI RẤT NHIỀU", "at": 2}, {"k": "2", "v": "CÓ CHỖ ĐỖ MIỄN PHÍ · PHÍ THẤP HƠN", "at": 3},
                                                                          {"k": "3", "v": "XE ĐIỆN: TRƯỚC BẠ 0% TỚI HẾT 02/2027", "at": 4}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "LÃI VAY · LÃI TIẾT KIỆM · GIÁ XE CŨ", "at": 5, "sm": True}, {"text": "ĐỀU THAY ĐỔI · KÊNH KHÔNG DỰ BÁO", "at": 6, "acc": True}]},
    {"type": "ledger", "at": 7, "title": "BA CÂU TỰ ĐIỀN", "rows": [{"k": "1", "v": "ĐI LẠI MỖI THÁNG BAO NHIÊU?", "at": 8}, {"k": "2", "v": "THÁNG ĐẦU SAU ƯU ĐÃI · % THU NHẬP?", "at": 9},
                                                                {"k": "3", "v": "XE CŨ CÙNG LOẠI · CÒN BAO NHIÊU %?", "at": 10}], "total": {"k": "TRẢ LỜI XONG", "v": "BẠN CÓ ĐỒNG HỒ CỦA RIÊNG MÌNH", "at": 11}},
    {"type": "broll", "at": 12, "vid": "15510261", "veil": 0.5, "illus": VM,
     "kin": [{"text": "ĐỒNG HỒ XE CÔNG NGHỆ · AI CŨNG THẤY", "at": 12}, {"text": "ĐỒNG HỒ XE CỦA MÌNH · CHỈ NGƯỜI CHỊU TÍNH MỚI THẤY", "at": 13, "acc": True}]},
    {"type": "question", "at": 14, "text": "Có tám trăm triệu hôm nay,\nbạn chọn lối nào?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 15}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [15, "ở"], "acc": True}]},
]}

Y3 = B3["youtube"]
SPEC = {
    "title": "Mua Xe 700 Triệu: Mỗi Tháng Thật Sự Tốn Bao Nhiêu? Trả Thẳng, Trả Góp Hay Chưa Mua",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 25, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["xe", "lăn", "bánh", "đồng", "hồ", "lãi", "tháng"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Mua Xe 700 Triệu: Mỗi Tháng Thật Sự Tốn Bao Nhiêu? Trả Thẳng, Trả Góp Hay Chưa Mua",
                   "Xe 700 Triệu Lăn Bánh Thành 800 Triệu: Phép Tính Mua Xe Ít Ai Làm Hết",
                   "Nuôi Một Chiếc Ô Tô Tốn Bao Nhiêu Mỗi Tháng? Ba Con Số Trước Khi Ký"],
        "summary": "Mua một chiếc ô tô 700 triệu (ví dụ giả định), mỗi tháng thật sự tốn bao nhiêu? Video bật “chiếc đồng hồ tính tiền” của chiếc xe: "
                   "100 triệu lăn bánh (lệ phí trước bạ, biển số), tiền nuôi xe mỗi tháng, tiền mất giá không ai gửi hoá đơn, khoản lãi và cú nhảy tháng "
                   "thứ 13 khi trả góp, và lối thứ ba: chưa mua. Kèm ba câu để bạn tự tính cho chiếc xe của mình.",
        "more": [Y3["more"][0],
                 "📐 CÁCH KÊNH TÍNH: VÍ DỤ GIẢ ĐỊNH: xe 700 triệu, giá tính lệ phí = giá xe, đăng ký Hà Nội (trước bạ 12% = 84; biển 14; khác 2 → lăn bánh "
                 "800). Nuôi xe năm đầu ≈ 4,7 triệu/tháng (gửi xe 1,5; xăng 12.000 km × 7 L/100 km × 24.000 đ; bảo dưỡng 6 triệu/năm; bảo hiểm vật chất "
                 "1,5%/năm; phí đường bộ, bảo hiểm bắt buộc). Bán lại sau 5 năm 55% → mất giá 315. Trả thẳng chi ròng 5 năm ≈ 689 triệu (≈ 11,5/tháng). "
                 "Trả góp: trả trước 30% + lăn bánh, vay 490 triệu 84 tháng gốc đều, 8% năm đầu rồi 13% → lãi 5 năm ≈ 184 triệu, chi ròng ≈ 873 (chưa trừ "
                 "lãi gửi của phần giữ lại). Người chưa mua gửi 800 triệu ở 6,8%/năm: mức chi đi lại hoà vốn ≈ 15 triệu/tháng."],
        "chapter_titles": {"ch00": "Mở đầu: chiếc đồng hồ tính tiền", "ch01": "Bảy trăm thành tám trăm: chi phí lăn bánh", "ch02": "Tiền nuôi xe mỗi tháng",
                           "ch03": "Khoản không ai gửi hoá đơn: mất giá", "ch04": "Trả góp: tiền lãi và cú nhảy tháng thứ 13", "ch05": "Lối thứ ba: chưa mua",
                           "ch06": "Khi nào phép tính này không đúng với bạn"},
        "sources": ["https://thoibaotaichinhvietnam.vn/le-phi-dang-ky-o-to-tai-ha-noi-tp-ho-chi-minh-giam-con-14-trieu-dong-190073.html",
                    "https://tienphong.vn/xe/634815/Ha-Noi-Phi-truoc-ba-oto-chinh-thuc-con-12-tpol.html",
                    "https://pbgdpl.cantho.gov.vn/quy-dinh-ve-muc-thu-phi-su-dung-duong-bo-tu-ngay-01022024",
                    "https://luatvietnam.vn/giao-thong/bao-hiem-o-to-bat-buoc-bao-nhieu-tien-863-89239-article.html",
                    "https://cafef.vn/khach-vay-mua-o-to-oan-minh-ganh-lai-suat-tha-noi-gan-20-188261008111845813.chn"],
        "hashtags": ["TàiChínhCáNhân", "MuaXe", "MuaXeTrảGóp", "ChiPhíNuôiXe", "BiểuĐồBiếtNói"],
        "tags": ["mua xe trả góp", "chi phí nuôi ô tô", "lăn bánh ô tô", "lệ phí trước bạ ô tô", "có nên mua ô tô", "chi phí sở hữu ô tô mỗi tháng",
                 "lãi vay mua xe", "tài chính cá nhân", "biểu đồ biết nói"],
        "category": Y3["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: phép tính do kênh tự lập (ví dụ giả định); các khoản phí theo văn bản pháp luật hiện hành; dải lãi vay theo báo chí 10/2026.",
        "video_credits": Y3["video_credits"],
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
