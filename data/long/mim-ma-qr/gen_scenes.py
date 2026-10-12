"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #8 "Mã QR".

    python data/long/mim-ma-qr/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Ảnh: chỉ PD / CC0 / CC BY. Clip: Pexels (ngang), gắn "VIDEO MINH HỌA".
Cảnh "qr" / "barcode" (lab.js) là HÌNH MINH HOẠ do engine tự vẽ, không phải mã thật. beat2 bật.
Chuẩn phối 12/10/2026: xen cảnh quay, ảnh tư liệu, sơ đồ (qr / barcode / go), số liệu; cảnh thuần chữ ở mức thấp.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

IMGS = {
    "qrdamaged": "File:QR Code Damaged.jpg",                 # CC0
    "weiqi": "File:Playing weiqi in Shanghai.jpg",           # CC BY 2.0
    "pepsi": "File:QR code on Pepsi Diet can.jpg",           # CC BY 2.0
}
SAY = {"qr": "quy a", "denso": "Đen-xô", "masahiro": "Ma-xa-hi-rô", "hara": "Ha-ra", "quick": "quých", "response": "rít-xpon",
       "vietqr": "Việt quy a", "logo": "lô-gô", "camera": "ca-mê-ra", "web": "oép", "ting": "ting"}
VM = "VIDEO MINH HỌA"
MOCK = "HÌNH MINH HOẠ · KHÔNG PHẢI MÃ THẬT"
IEEE = "NGUỒN: IEEE SPECTRUM, 11.2020"
NAPAS = "NGUỒN: NAPAS (QUA BÁO CHÍ), 2025"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "TỜ GIẤY TRÊN QUẦY TRÀ ĐÁ"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "30320695", "veil": 0.45, "illus": VM + " · KHÔNG PHẢI QUÁN TRONG LỜI KỂ",
     "kin": [{"text": "QUÁN TRÀ ĐÁ VỈA HÈ", "at": 0, "acc": True}, {"text": "một tờ giấy ép nhựa", "at": [1, "có"], "sm": True}]},
    {"type": "qr", "at": 2, "modulesAt": [2, None, 0, 0.1], "modulesUntil": [2, "Một"], "scanAt": [2, "Ting."],
     "side": {"k": "1 GIÂY", "v": "TING", "at": [2, "Ting."]}, "label": {"k": "", "v": MOCK, "at": 2}},
    {"type": "ledger", "at": 3, "title": "5.000 ĐỒNG", "rows": [{"k": "VÍ", "v": "KHÔNG CẦN", "at": [3, "ví,"]}, {"k": "TIỀN LẺ", "v": "KHÔNG CẦN", "at": [3, "lẻ,"]},
                                                              {"k": "MÁY CÀ THẺ", "v": "KHÔNG CẦN", "at": [3, "máy"]}]},
    {"type": "counter", "at": 4, "from": 0, "to": 15, "suffix": " TRIỆU", "until": [4, "triệu"], "label": "LẦN QUÉT MỖI NGÀY Ở VIỆT NAM",
     "sub": {"text": "ƯỚC TÍNH · " + NAPAS, "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "KHÔNG SINH RA CHO QUÁN TRÀ ĐÁ", "at": [5, "không"]},
                                          {"text": "KHÔNG SINH RA CHO ĐIỆN THOẠI", "at": [6, "không"], "acc": True}]},
    {"type": "broll", "at": 7, "vid": "6447409", "veil": 0.5, "illus": VM,
     "kin": [{"text": "1994", "at": [7, "năm"], "acc": True}, {"text": "nhà máy linh kiện ô tô · Nhật Bản", "at": [7, "trong"], "sm": True}]},
    {"type": "go", "at": 8, "stones": 34, "label": {"k": "Ý TƯỞNG", "v": "TỪ MỘT VÁN CỜ GIỜ NGHỈ TRƯA", "at": [8, "trong"]}},
    {"type": "qr", "at": 9, "modulesAt": [12, None, 0, 0.05], "modulesUntil": [12, "ở"], "hlAt": [11, "Ba"],
     "damage": {"at": [13, "dính"], "okAt": [13, "vẫn"], "text": "DÍNH BẨN · NHÀU NÁT"},
     "side": {"k": "3 CHI TIẾT", "v": "ít ai hỏi vì sao", "at": [10, "ba"]}, "label": {"k": "", "v": MOCK, "at": 9}},
    {"type": "kinetic", "at": 14, "items": [{"text": "MỖI CHI TIẾT", "at": 14, "sm": True}, {"text": "MỘT BÀI TOÁN", "at": [14, "một"]},
                                           {"text": "MỘT LỜI GIẢI RẤT ĐỜI THƯỜNG", "at": [14, "lời"], "acc": True}]},
    {"type": "question", "at": 15, "text": "Vì sao người làm ra nó\nkhông thu một đồng nào?", "showAt": 16},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MƯỜI MÃ VẠCH TRÊN MỘT THÙNG HÀNG"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MƯỜI MÃ VẠCH\nTRÊN MỘT THÙNG HÀNG", "sub": "DENSO · ĐẦU NHỮNG NĂM 1990", "vid": "6447409", "ms": 8,
     "illus": VM, "titleAt": [0, "Đầu"]},
    {"type": "barcode", "at": 2, "n": 1, "label": {"k": "MÃ VẠCH", "v": "LOẠI PHỔ BIẾN: ~12 CHỮ SỐ", "at": [3, "khoảng"]}},
    {"type": "kinetic", "at": 4, "items": [{"text": "MỘT THÙNG LINH KIỆN", "at": 4, "sm": True}, {"text": "CẦN NHIỀU HƠN THẾ", "at": [4, "nhiều"], "acc": True}]},
    {"type": "barcode", "at": 5, "n": 10, "until": [7, "mười"], "label": {"k": "DÁN THÊM · RỒI DÁN THÊM NỮA", "v": MOCK, "at": [5, "Rồi"]}},
    {"type": "quote", "at": 7, "text": "Có những thùng mang tới hơn mười mã vạch. Công nhân phát mệt vì phải quét đi quét lại.",
     "by": "MASAHIRO HARA · NIPPON.COM, 2020 · TRÍCH DỊCH", "qline": 7},
    {"type": "counter", "at": 8, "from": 1, "to": 10, "suffix": " LẦN QUÉT", "until": [8, "quét"], "label": "CHO MỘT THÙNG HÀNG",
     "sub": {"text": "× CẢ MỘT NHÀ MÁY", "at": [8, "Nhân"]}},
    {"type": "ledger", "at": 9, "title": "ĐỀ BÀI NĂM 1992", "srcnote": IEEE,
     "rows": [{"k": "CHỨA", "v": "THẬT NHIỀU THÔNG TIN", "at": [10, "chứa"]}, {"k": "CHỈ CẦN", "v": "QUÉT MỘT LẦN", "at": [10, "chỉ"]}]},
    {"type": "question", "at": 11, "text": "Nhét thêm thông tin vào đâu,\nkhi những cái sọc đã chật kín?"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "VÁN CỜ GIỜ NGHỈ TRƯA"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "photo", "img": "weiqi", "tone": "color", "focus": [0.5, 0.5], "move": "in", "veil": 0.45, "illus": "ẢNH MINH HỌA · CC BY 2.0",
     "kin": [{"text": "BÀN CỜ VÂY", "at": [0, "Bàn"], "acc": True}, {"text": "Hara chơi cờ vào giờ nghỉ trưa", "at": 1, "sm": True}]},
    {"type": "quote", "at": 2, "text": "Khi đang xếp những quân đen trắng lên bàn cờ, tôi chợt nhận ra, đó là một cách truyền thông tin rất gọn.",
     "by": "MASAHIRO HARA · NIPPON.COM, 2020 · TRÍCH DỊCH", "qline": 2},
    {"type": "barcode", "at": 3, "n": 1, "digits": "→  ĐỌC MỘT CHIỀU  →", "label": {"k": "MÃ VẠCH", "v": "CHỈ DÙNG MỘT CHIỀU", "at": [3, "một"]}},
    {"type": "go", "at": 4, "stones": 60, "label": {"k": "BÀN CỜ: HAI CHIỀU", "v": "NGANG × DỌC → CHỨA NHIỀU HƠN", "at": [5, "hai"]}},
    {"type": "ledger", "at": 6, "title": "VỚI MÁY TÍNH, THẾ LÀ ĐỦ", "rows": [{"k": "Ô ĐEN", "v": "1", "at": [7, "Đen"]}, {"k": "Ô TRẮNG", "v": "0", "at": [7, "Trắng"]}]},
    {"type": "go", "at": 8, "stones": 26, "hitAt": [9, "lệch"], "move": "LỆCH MỘT CHÚT", "prob": "vẫn biết thuộc điểm nào",
     "label": {"k": "BÀI HỌC THỨ HAI", "v": "CHỊU ĐƯỢC SAI LỆCH", "at": [10, "vẫn"]}},
    {"type": "ledger", "at": 11, "title": "MỘT LOẠI MÃ TỐT", "rows": [{"k": "IN HƠI LỆCH", "v": "VẪN HIỂU", "at": [11, "In"]},
                                                                    {"k": "QUÉT HƠI NGHIÊNG", "v": "VẪN HIỂU", "at": [11, "quét"]}]},
    {"type": "qr", "at": 12, "modulesAt": [12, None, 0, 0.1], "modulesUntil": [13, "đang"], "hlAt": [13, "ba"],
     "side": {"k": "BÀI TOÁN KHÓ HƠN", "v": "ba ô vuông ở góc", "at": [13, "ba"]}, "label": {"k": "", "v": MOCK, "at": 12}},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "BA Ô VUÔNG Ở GÓC"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "BA Ô VUÔNG\nỞ GÓC", "sub": "MÁY BIẾT MÃ NẰM Ở ĐÂU BẰNG CÁCH NÀO?", "vid": "7287312", "illus": VM,
     "titleAt": [0, "Hãy"]},
    {"type": "question", "at": 2, "text": "Mã nằm ở đâu?\nĐầu nào là đầu trên?"},
    {"type": "ledger", "at": 3, "title": "HAI ĐỜI MÃ", "rows": [{"k": "MÃ VẠCH", "v": "PHẢI XOAY THÙNG CHO ĐÚNG CHIỀU", "at": 3},
                                                             {"k": "HARA MUỐN", "v": "QUÉT TỪ MỌI GÓC · TRONG CHỚP MẮT", "at": 4}]},
    {"type": "broll", "at": 5, "vid": "4832768", "veil": 0.4, "illus": VM,
     "kin": [{"text": "NGOÀI PHÒNG THÍ NGHIỆM", "at": 5, "sm": True}, {"text": "TRÊN MỘT CHUYẾN TÀU", "at": [6, "ngồi"], "acc": True}]},
    {"type": "quote", "at": 7, "text": "Tôi thấy một toà nhà cao nổi bật giữa xung quanh. Cái mã cũng cần một ký hiệu đặc biệt, để nổi bật giữa chữ nghĩa.",
     "by": "MASAHIRO HARA · IEEE SPECTRUM, 2020 · TRÍCH DỊCH", "qline": 7},
    {"type": "kinetic", "at": 8, "items": [{"text": "MỘT HÌNH", "at": 8, "sm": True}, {"text": "GẦN NHƯ KHÔNG CÓ TRONG CHỮ IN", "at": [8, "gần"], "acc": True}]},
    {"type": "ledger", "at": 9, "title": "TÌM BẰNG CÁCH NÀO?", "srcnote": IEEE,
     "rows": [{"k": "QUÉT", "v": "HÀNG LOẠT TRANG BÁO, TỜ RƠI", "at": [10, "quét"]}, {"k": "VIẾT PHẦN MỀM", "v": "ĐẾM TỶ LỆ ĐEN / TRẮNG", "at": [11, "đếm"]}],
     "total": {"k": "SAU 3 THÁNG", "v": "MỘT TỶ LỆ HIẾM GẶP NHẤT", "at": 12}},
    {"type": "qr", "at": 13, "ratio": {"at": [13, "Một"]}, "hlAt": [14, "ô"],
     "side": {"k": "Ô VUÔNG LỒNG Ô VUÔNG", "v": "ở ba góc của mọi mã QR", "at": [14, "ba"]}, "label": {"k": "", "v": MOCK + " · " + IEEE, "at": 13}},
    {"type": "ledger", "at": 15, "title": "THẤY BA GÓC LÀ BIẾT", "rows": [{"k": "1", "v": "MÃ NẰM Ở ĐÂU", "at": [16, "mã"]}, {"k": "2", "v": "TO BAO NHIÊU", "at": [16, "to"]},
                                                                       {"k": "3", "v": "ĐANG XOAY HƯỚNG NÀO", "at": [16, "đang"]}]},
    {"type": "counter", "at": 17, "from": 1, "to": 5, "prefix": "×", "until": [17, "năm"], "label": "NHANH HƠN MÃ VẠCH THÔNG THƯỜNG", "sub": {"text": IEEE, "at": 17}},
    {"type": "kinetic", "at": 18, "items": [{"text": "QR", "at": [18, "QR"], "acc": True}, {"text": "QUICK RESPONSE", "at": [18, "Quick"]},
                                           {"text": "phản hồi nhanh", "at": [18, "Phản"], "sm": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "BẨN MỘT PHẦN BA VẪN ĐỌC ĐƯỢC"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "qr", "modulesAt": [0, None, 0, 0.1], "modulesUntil": [0, "ở"],
     "side": {"k": "CHI TIẾT THỨ HAI", "v": "những chấm đen trắng", "at": [0, "những"]}, "label": {"k": "", "v": MOCK, "at": 0}},
    {"type": "bars", "at": 1, "title": "CHỨA ĐƯỢC BAO NHIÊU CHỮ SỐ?", "unit": "",
     "items": [{"k": "MÃ VẠCH PHỔ BIẾN", "v": 12, "lbl": "12", "at": [2, "mười"]}, {"k": "MÃ QR LỚN NHẤT", "v": 7089, "lbl": "> 7.000", "at": [1, "hơn"], "acc": True}],
     "label": {"k": "", "v": IEEE, "at": 1}},
    {"type": "kinetic", "at": 3, "items": [{"text": "CHI TIẾT THỨ BA", "at": [3, "chi"], "acc": True}]},
    {"type": "broll", "at": 4, "vid": "6447409", "ms": 3, "veil": 0.5, "illus": VM,
     "kin": [{"text": "NHÀ MÁY KHÔNG PHẢI PHÒNG SẠCH", "at": 4}, {"text": "dầu · bụi · trầy xước", "at": [4, "dầu,"], "sm": True}]},
    {"type": "barcode", "at": 5, "n": 1, "digits": "BẨN MỘT SỌC = HỎNG", "label": {"k": "MÃ VẠCH", "v": "BẨN MỘT SỌC LÀ COI NHƯ HỎNG", "at": [5, "bẩn"]}},
    {"type": "print", "at": 6, "img": "qrdamaged", "tone": "color", "illus": "ẢNH: MÃ QR BỊ HỎNG MỘT PHẦN (CC0)",
     "side": {"k": "MÃ QR", "h": "BẨN / RÁCH\nTỚI 30%", "lines": [{"text": "*vẫn đọc ra đúng*", "at": [7, "vẫn"]}]}},
    {"type": "ledger", "at": 8, "title": "BÍ QUYẾT", "rows": [{"k": "KHÔNG GHI", "v": "MỘT LẦN DUY NHẤT", "at": 8}, {"k": "THÊM", "v": "DỮ LIỆU DỰ PHÒNG", "at": 9},
                                                             {"k": "ĐỦ ĐỂ", "v": "TÍNH NGƯỢC LẠI PHẦN ĐÃ MẤT", "at": [9, "đủ"]}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "nghe mất vài chữ", "at": [10, "nhiễu"], "sm": True}, {"text": "VẪN ĐOÁN RA CẢ CÂU", "at": [10, "vẫn"], "acc": True}]},
    {"type": "qr", "at": 11, "damage": {"at": [12, "che"], "okAt": [12, "vẫn"], "text": "LOGO CHE MẤT DỮ LIỆU"},
     "side": {"k": "LOGO GIỮA MÃ", "v": "", "at": [11, "logo"]}, "label": {"k": "", "v": MOCK, "at": 11}},
    {"type": "broll", "at": 13, "vid": "30320695", "ms": 9, "veil": 0.45, "illus": VM,
     "kin": [{"text": "THIẾT KẾ CHO NHÀ XƯỞNG DẦU MỠ", "at": 13, "sm": True}, {"text": "HỢP VỚI QUẦY TRÀ ĐÁ", "at": [13, "hợp"], "acc": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "MÓN QUÀ KHÔNG THU PHÍ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "MÃ QR RA MẮT", "date": "1994"},
    {"type": "ledger", "at": 1, "title": "DENSO ĐỨNG TRƯỚC MỘT LỰA CHỌN", "rows": [{"k": "HỌ CÓ", "v": "BẰNG SÁNG CHẾ", "at": 2},
                                                                                 {"k": "HỌ CÓ THỂ", "v": "THU TIỀN MỖI LẦN DÙNG", "at": [2, "thu"]}]},
    {"type": "slam", "at": 3, "text": "HỌ KHÔNG LÀM THẾ"},
    {"type": "timeline", "at": 4, "items": [{"year": "1994", "text": "ra mắt · công bố tiêu chuẩn", "at": [4, "công"]},
                                           {"year": "—", "text": "*không thu phí* với mã làm đúng chuẩn", "at": [4, "tuyên"]},
                                           {"year": "2000", "text": "thành *tiêu chuẩn quốc tế*", "at": 5}]},
    {"type": "ledger", "at": 6, "title": "KHÔNG CẦN XIN PHÉP", "rows": [{"k": "AI CŨNG", "v": "ĐƯỢC DÙNG", "at": 6}, {"k": "AI CŨNG", "v": "ĐƯỢC IN", "at": [6, "in."]}]},
    {"type": "quote", "at": 7, "text": "Chúng tôi không nhận được đồng hoa hồng nào mỗi lần nó được dùng.",
     "by": "MASAHIRO HARA · THE GUARDIAN, 2020 · TRÍCH DỊCH", "qline": 8},
    {"type": "kinetic", "at": 9, "items": [{"text": "CÂU TRẢ LỜI", "at": 9, "sm": True}, {"text": "MIỄN PHÍ", "at": [10, "miễn"], "acc": True},
                                          {"text": "ai cũng làm được máy đọc · ai cũng tự in được", "at": [10, "ai"], "sm": True}]},
    {"type": "print", "at": 11, "img": "pepsi", "tone": "color", "illus": "ẢNH MINH HỌA · CC BY 2.0",
     "side": {"k": "LAN ĐI", "h": "TỚI NƠI\nKHÔNG AI NGỜ", "lines": [{"text": "lon nước · bao bì · *quầy hàng*", "at": [12, "lan"]}]}},
    {"type": "ledger", "at": 13, "title": "ĐIỀU HARA KHÔNG NGỜ", "srcnote": "DIỄN Ý LỜI HARA TRONG CÁC BÀI PHỎNG VẤN",
     "rows": [{"k": "ÔNG NGHĨ", "v": "PHỔ BIẾN TRONG CÔNG NGHIỆP", "at": 13}], "total": {"k": "BẤT NGỜ", "v": "NGƯỜI TA DÙNG ĐỂ TRẢ TIỀN", "at": 14}},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "TỪ NHÀ MÁY RA VỈA HÈ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "TỪ NHÀ MÁY\nRA VỈA HÈ", "sub": "HAI BƯỚC NGOẶT", "vid": "4121750", "illus": VM, "titleAt": [0, "Bước"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "MÁY QUÉT", "at": 1, "sm": True}, {"text": "NẰM TRONG TÚI MỖI NGƯỜI", "at": 2, "acc": True}]},
    {"type": "date", "at": 3, "day": "BƯỚC NGOẶT THỨ HAI · TRUNG QUỐC", "date": "ĐẦU 2010s"},
    {"type": "kinetic", "at": 4, "items": [{"text": "VÍ ĐIỆN TỬ", "at": 4, "sm": True}, {"text": "TRẢ TIỀN BẰNG CÁCH QUÉT MÃ", "at": [4, "trả"], "acc": True}]},
    {"type": "question", "at": 5, "text": "Ai được lợi nhiều nhất?"},
    {"type": "ledger", "at": 6, "title": "NGƯỜI BÁN CẦN GÌ?", "rows": [{"k": "NHẬN THẺ", "v": "MÁY · ĐƯỜNG TRUYỀN · PHÍ", "at": 6}],
     "total": {"k": "NHẬN QUA MÃ QR", "v": "MỘT TỜ GIẤY IN", "at": 7}},
    {"type": "broll", "at": 8, "vid": "35746954", "veil": 0.45, "illus": VM,
     "kin": [{"text": "MỘT GÁNH HÀNG RONG", "at": 8}, {"text": "CŨNG NHẬN TIỀN KHÔNG TIỀN MẶT", "at": [8, "cũng"], "acc": True}]},
    {"type": "broll", "at": 9, "vid": "6327104", "veil": 0.45, "illus": VM,
     "kin": [{"text": "ĐẠI DỊCH", "at": 9, "acc": True}, {"text": "thực đơn giấy → một ô vuông ở góc bàn", "at": 10, "sm": True}]},
    {"type": "date", "at": 11, "day": "VIETQR · 14 NGÂN HÀNG ĐẦU TIÊN", "date": "15.06.2021"},
    {"type": "kinetic", "at": 12, "items": [{"text": "MỘT MÃ", "at": 12, "acc": True}, {"text": "quét bằng ứng dụng của nhiều ngân hàng", "at": [12, "quét"], "sm": True}]},
    {"type": "counter", "at": 13, "from": 0, "to": 3.6, "suffix": " TỶ", "until": [13, "sáu"], "label": "GIAO DỊCH CHUYỂN TIỀN BẰNG MÃ · 10 THÁNG ĐẦU 2025",
     "sub": {"text": "+52% SO VỚI CÙNG KỲ · " + NAPAS, "at": 14}},
    {"type": "timeline", "at": 15, "items": [{"year": "1994", "text": "thùng linh kiện ô tô", "at": [15, "Từ"]},
                                            {"year": "NAY", "text": "tờ giấy trên *quầy trà đá*", "at": [15, "tới"]}]},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "MẶT TRÁI CỦA MỘT TỜ GIẤY"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "kinetic", "items": [{"text": "DỄ IN", "at": [0, "dễ"]}, {"text": "KẺ GIAN CŨNG IN ĐƯỢC", "at": [0, "kẻ"], "acc": True}]},
    {"type": "qr", "at": 1, "modulesAt": [1, None, 0, 0.1], "modulesUntil": [1, "là"], "damage": {"at": [2, "dán"], "text": "MÃ GIẢ DÁN ĐÈ"},
     "side": {"k": "KHÁCH QUÉT", "v": "tiền sang tài khoản người lạ", "at": [2, "tiền"]}, "label": {"k": "", "v": MOCK, "at": 1}},
    {"type": "ledger", "at": 3, "title": "CÔNG AN HÀ NỘI CẢNH BÁO", "srcnote": "NGUỒN: CÔNG AN TP HÀ NỘI (QUA BÁO CHÍ)",
     "rows": [{"k": "MÃ", "v": "DẪN TỚI TRANG WEB GIẢ", "at": [4, "Có"]}, {"k": "MÃ", "v": "QUA TIN NHẮN GIẢ DANH", "at": [4, "tin"]}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "MẮT NGƯỜI KHÔNG ĐỌC ĐƯỢC", "at": 5}, {"text": "ĐIỂM YẾU CỦA NÓ", "at": [5, "điểm"], "acc": True}]},
    {"type": "ledger", "at": 6, "title": "BA THÓI QUEN NHỎ", "rows": [{"k": "1", "v": "NHÌN TÊN NGƯỜI NHẬN TRƯỚC KHI BẤM", "at": 7},
                                                                    {"k": "2", "v": "MÃ DÁN CHỒNG? HỎI LẠI NGƯỜI BÁN", "at": 8},
                                                                    {"k": "3", "v": "KHÔNG QUÉT MÃ LẠ BỊ GIỤC LÀM NGAY", "at": 9}]},
    {"type": "qr", "at": 10, "modulesAt": [10, None, 0, 0.1], "modulesUntil": [10, "bạn"], "hlAt": [11, "Ba"],
     "side": {"k": "BA Ô Ở GÓC", "v": "toà nhà cao nhìn từ cửa sổ tàu", "at": [11, "là"]}, "label": {"k": "", "v": MOCK, "at": 10}},
    {"type": "go", "at": 12, "stones": 44, "label": {"k": "NHỮNG CHẤM ĐEN TRẮNG", "v": "MỘT VÁN CỜ GIỜ NGHỈ TRƯA", "at": [12, "là"]}},
    {"type": "slam", "at": 13, "text": "MIỄN PHÍ", "sub": "MỘT LỰA CHỌN CỦA NHỮNG NGƯỜI LÀM RA NÓ"},
    {"type": "question", "at": 14, "text": "Lần gần nhất bạn\ntrả tiền mặt là khi nào?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 15}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [15, "ở"], "acc": True}]},
]}

SPEC = {
    "title": "Mã QR: Ô Vuông Sinh Ra Để Đếm Linh Kiện Ô Tô, Giờ Nằm Trên Mọi Quầy Hàng Việt Nam",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["qr", "mã", "vạch", "cờ", "góc", "bẩn", "miễn", "phí"],
    "say": SAY, "imgs": IMGS, "chapters": [f"ch{i:02d}" for i in range(8)],
    "youtube": {
        "titles": ["Mã QR: Ô Vuông Sinh Ra Để Đếm Linh Kiện Ô Tô, Giờ Nằm Trên Mọi Quầy Hàng Việt Nam",
                   "Vì Sao Mã QR Có 3 Ô Vuông Ở Góc? Câu Chuyện Từ Một Ván Cờ Vây Giờ Nghỉ Trưa",
                   "Người Phát Minh Mã QR Không Thu Một Đồng: Chuyện Ô Vuông Trên Quầy Trà Đá"],
        "summary": "Ô vuông đen trắng trên quầy trà đá không sinh ra cho quán xá, cũng không sinh ra cho điện thoại. Nó ra đời năm 1994 trong một "
                   "nhà máy linh kiện ô tô ở Nhật, từ một ván cờ vây giờ nghỉ trưa và một toà nhà cao nhìn qua cửa sổ tàu. Vì sao mã QR có ba ô "
                   "vuông ở góc, vì sao bẩn một phần ba vẫn quét được, vì sao người làm ra nó không thu phí, và nó đi từ thùng linh kiện tới "
                   "VietQR như thế nào.",
        "more": ["Hình \"mã QR\" và \"mã vạch\" trong video là hình minh hoạ do kênh tự vẽ, không phải mã thật, quét sẽ không ra gì. Con số dung "
                 "lượng: IEEE Spectrum ghi 7.087 chữ số, tiêu chuẩn ghi 7.089 cho phiên bản lớn nhất; video nói \"hơn bảy nghìn\". Số liệu Việt "
                 "Nam do NAPAS công bố qua báo chí (2025). Mốc thanh toán bằng mã QR ở Trung Quốc: các nguồn ghi 2011–2013. Lời trích được dịch "
                 "và đọc bằng giọng máy của kênh. Video không hướng dẫn cách tạo mã giả."],
        "chapter_titles": {"ch00": "Mở đầu: tờ giấy trên quầy trà đá", "ch01": "Mười mã vạch trên một thùng hàng (Denso, 1992)",
                           "ch02": "Ván cờ vây giờ nghỉ trưa", "ch03": "Ba ô vuông ở góc: tỷ lệ 1:1:3:1:1",
                           "ch04": "Bẩn một phần ba vẫn đọc được", "ch05": "Món quà không thu phí",
                           "ch06": "Từ nhà máy ra vỉa hè: điện thoại, Trung Quốc, VietQR", "ch07": "Mặt trái: mã giả dán đè và ba thói quen"},
        "sources": [
            "https://spectrum.ieee.org/how-a-board-game-and-skyscrapers-inspired-the-development-of-the-qr-code",
            "https://vnba.org.vn/vi/napas-va-cac-ngan-hang-chinh-thuc-ra-mat-thuong-hieu-vietqr-va-dich-vu-chuyen-tien-nhanh-napas247-bang-ma-qr-513.htm",
            "https://thitruongtaichinhtiente.vn/cong-dong-ngan-hang-va-trung-gian-thanh-toan-cam-ket-dong-hanh-thuc-day-thanh-toan-noi-dia-va-xuyen-bien-gioi-73937.html",
            "https://thoibaotaichinhvietnam.vn/vietqrpay-mo-duong-cho-chuan-thanh-toan-moi-giup-minh-bach-va-quan-ly-dong-tien-187247.html",
            "https://vneconomy.vn/cong-an-tp-ha-noi-canh-bao-ve-hinh-thuc-lua-dao-quishing-dang-bung-phat.htm",
            "https://en.wikipedia.org/wiki/QR_code_payment",
        ],
        "hashtags": ["MãQR", "CôngNghệ", "VietQR", "LịchSửCôngNghệ", "MindInTheMachine"],
        "tags": ["mã QR", "QR code", "mã QR hoạt động thế nào", "ai phát minh ra mã QR", "Masahiro Hara", "Denso", "VietQR", "thanh toán không tiền mặt",
                 "lừa đảo mã QR", "mã vạch", "lịch sử công nghệ", "công nghệ thay đổi thế giới"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
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
