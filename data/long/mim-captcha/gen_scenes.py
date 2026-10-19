"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #10 "CAPTCHA".

    python data/long/mim-captcha/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Cảnh "captcha" (lab.js) là hình do kênh TỰ VẼ để minh hoạ, không phải giao diện của dịch vụ nào.
Clip: Pexels (ngang), gắn "VIDEO MINH HỌA". Không hướng dẫn cách vượt mã, không nêu tên dịch vụ giải thuê. beat2 bật.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"=CAPTCHA": "cáp-cha", "captcha": "cáp-cha", "yahoo": "Da-hu", "carnegie": "Các-nê-gi", "mellon": "Me-lần", "luis": "Lu-ít", "von": "phôn",
       "ahn": "An", "manuel": "Ma-nu-en", "blum": "Blum", "alan": "A-lần", "turing": "Tiu-rinh", "altavista": "An-ta Vít-xta",
       "new": "Niu", "york": "Doóc", "times": "Thai", "google": "Gu-gồ", "duolingo": "Đu-ô-linh-gô", "tick": "tích", "california": "Ca-li-pho-ni-a",
       "irvine": "Ơ-vai", "=AI": "ây ai", "robot": "rô-bốt", "cloudflare": "Clao-phle"}
VM = "VIDEO MINH HỌA"
MOCK = "HÌNH MINH HOẠ DO KÊNH TỰ VẼ · KHÔNG PHẢI GIAO DIỆN CỦA DỊCH VỤ NÀO"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "Ô VUÔNG NHỎ"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "captcha", "mode": "tick", "tickAt": [1, "tick"], "label": {"k": "", "v": MOCK, "at": [0, "Bên"]}},
    {"type": "kinetic", "at": 2, "items": [{"text": "MÁY HỎI: BẠN CÓ PHẢI NGƯỜI KHÔNG?", "at": 3, "sm": True},
                                          {"text": "NGƯỜI PHẢI CHỨNG MINH", "at": [4, "phải"], "acc": True}, {"text": "cho một cỗ máy", "at": [4, "Cho"], "sm": True}]},
    {"type": "broll", "at": 5, "vid": "7999451", "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỘT VIỆC KHÔNG CÔNG", "at": [6, "một"], "acc": True}, {"text": "mà bạn không hề biết", "at": [6, "mà"], "sm": True}]},
    {"type": "ledger", "at": 8, "title": "BA VÒNG THI", "rows": [{"k": "1", "v": "CHỮ MÉO", "at": [8, "Chữ"]}, {"k": "2", "v": "Ô ẢNH", "at": [8, "Ô"]},
                                                                 {"k": "3", "v": "MỘT DẤU TICK", "at": [8, "Rồi"]}]},
    {"type": "question", "at": 10, "text": "Ai đang chấm ai?"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MƯỜI BÀI TOÁN CỦA YAHOO"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MƯỜI BÀI TOÁN\nCỦA YAHOO", "sub": "MÙA THU NĂM 2000", "vid": "8198514", "illus": VM,
     "titleAt": [0, "Mùa"]},
    {"type": "ledger", "at": 2, "title": "TRONG KHÁN PHÒNG", "srcnote": "THEO THE NEW YORKER · NPR",
     "rows": [{"k": "AI", "v": "LUIS VON AHN · 22 TUỔI", "at": [2, "hai"]}, {"k": "BÀI TOÁN", "v": "MÁY ĐĂNG KÝ HỘP THƯ", "at": 4},
              {"k": "ĐỂ", "v": "GỬI THƯ RÁC", "at": [4, "để"]}],
     "total": {"k": "KHÓ", "v": "ĐÂU LÀ NGƯỜI, ĐÂU LÀ MÁY?", "at": [5, "đâu"]}},
    {"type": "kinetic", "at": 6, "items": [{"text": "RA MỘT ĐỀ", "at": 7, "sm": True}, {"text": "NGƯỜI LÀM RẤT DỄ", "at": [7, "con"], "acc": True},
                                          {"text": "MÁY CHƯA LÀM ĐƯỢC", "at": [7, "còn"]}]},
    {"type": "captcha", "at": 8, "mode": "text", "words": ["overlooks", "inquiry"], "typeAt": [8, "Đọc"], "until": [9, "tên"],
     "label": {"k": "ĐỌC CHỮ BỊ BÓP MÉO", "v": MOCK, "at": [8, "Đọc"]}},
    {"type": "slam", "at": 10, "text": "PHÉP THỬ TURING", "sub": "BA CHỮ NẰM TRONG CÁI TÊN CAPTCHA"},
    {"type": "ledger", "at": 11, "title": "ĐẢO CHIỀU", "rows": [{"k": "1950", "v": "NGƯỜI CHẤM · MÁY ĐI THI", "at": [11, "con"]},
                                                              {"k": "2000", "v": "MÁY CHẤM · NGƯỜI ĐI THI", "at": [12, "Cỗ"]}]},
    {"type": "timeline", "at": 13, "items": [{"year": "1997", "text": "AltaVista dùng *cách tương tự*", "at": 14},
                                            {"year": "2000", "text": "Yahoo nhận mã *miễn phí* · chạy sau ~2 tuần", "at": 13},
                                            {"year": "vài năm sau", "text": "gần như *trang lớn nào cũng có*", "at": 15}]},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "VÒNG MỘT: CHỮ MÉO"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "kinetic", "items": [{"text": "VÒNG MỘT", "at": [0, "Vòng"], "sm": True}, {"text": "THÀNH CÔNG RỰC RỠ", "at": [0, "thành"], "acc": True},
                                 {"text": "tới mức người làm ra nó thấy áy náy", "at": [1, "chính"], "sm": True}]},
    {"type": "counter", "at": 2, "from": 0, "to": 200, "suffix": " TRIỆU", "until": [3, "triệu"], "label": "MÃ ĐƯỢC GÕ MỖI NGÀY · MỖI MÃ ~10 GIÂY",
     "sub": {"text": "THEO LUIS VON AHN · NPR, 08.2008", "at": 4}},
    {"type": "counter", "at": 5, "from": 0, "to": 500000, "suffix": " GIỜ", "until": [5, "giờ."], "label": "CỦA CON NGƯỜI · MỖI NGÀY",
     "sub": {"text": "GÕ NHỮNG CHỮ VÔ NGHĨA", "at": 6}},
    {"type": "question", "at": 7, "text": "Mười giây ấy\nlàm được việc gì có ích không?", "showAt": 8},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "VIỆC KHÔNG CÔNG CỦA BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "VIỆC KHÔNG CÔNG\nCỦA BẠN", "sub": "NHỮNG CUỐN SÁCH CŨ", "vid": "5224014", "illus": VM,
     "titleAt": [0, "Câu"]},
    {"type": "broll", "at": 1, "vid": "4061896", "veil": 0.5, "illus": VM,
     "kin": [{"text": "CHỤP LẠI SÁCH BÁO CŨ", "at": [1, "chụp"], "acc": True}, {"text": "máy đọc ảnh · chuyển thành chữ", "at": 2, "sm": True}]},
    {"type": "counter", "at": 3, "from": 0, "to": 5, "prefix": "1 / ", "until": [4, "năm"], "label": "SỐ TỪ MÁY ĐỌC SAI Ở SÁCH CŨ · CÓ KHI",
     "sub": {"text": "THEO NHÓM CỦA VON AHN · 2008", "at": 4}},
    {"type": "captcha", "at": 5, "mode": "text", "words": ["morning", "upon"], "labels": ["MÁY ĐÃ BIẾT ĐÁP ÁN", "MÁY ĐỌC KHÔNG RA"],
     "labelAt": 6, "labelGap": 4.2, "typeAt": [8, "Nên"], "until": [9, "một", 1],
     "label": {"k": "PHIÊN BẢN 2007: HAI TỪ", "v": MOCK, "at": [5, "Lần"]}},
    {"type": "slam", "at": 10, "text": "VIỆC KHÔNG CÔNG CỦA BẠN", "sub": "MỖI LẦN GÕ = ĐỌC HỘ MỘT TỪ TRONG SÁCH CŨ", "subAt": 11},
    {"type": "bars", "at": 12, "title": "NĂM ĐẦU TIÊN CỦA PHIÊN BẢN HAI TỪ", "unit": "",
     "items": [{"k": "TRIỆU TỪ ĐÃ GIẢI", "v": 440, "lbl": "> 440", "at": [12, "hơn"]}, {"k": "NGHÌN CUỐN SÁCH", "v": 17.6, "lbl": "> 17", "at": [13, "hơn"], "acc": True}],
     "label": {"k": "CHÍNH XÁC > 99%", "v": "CARNEGIE MELLON · SCIENCE, 2008", "at": [13, "với"]}},
    {"type": "timeline", "at": 14, "items": [{"year": "báo cũ", "text": "kho *New York Times* được số hoá", "at": 14},
                                            {"year": "09.2009", "text": "*Google* mua lại dự án", "at": 15},
                                            {"year": "vài năm sau", "text": "von Ahn làm *Duolingo*", "at": 16}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "MỌI NGƯỜI CHĂM CHỈ GÕ CHỮ", "at": 17, "sm": True}, {"text": "MÁY CŨNG ĐANG HỌC ĐỌC", "at": [17, "máy"], "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "VÒNG HAI: Ô ẢNH"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "GOOGLE CÔNG BỐ MỘT CON SỐ", "date": "12.2014"},
    {"type": "counter", "at": 1, "from": 0, "to": 99.8, "suffix": "%", "until": [1, "tám"], "label": "AI GIẢI ĐÚNG LOẠI CHỮ MÉO KHÓ NHẤT",
     "sub": {"text": "GOOGLE SECURITY BLOG · 03.12.2014", "at": [1, "phần"]}},
    {"type": "slam", "at": 2, "text": "VÒNG MỘT ĐÃ VỠ", "sub": "ĐỀ CHỈ NGƯỜI LÀM ĐƯỢC · GIỜ MÁY LÀM GẦN NHƯ HOÀN HẢO", "subAt": 3},
    {"type": "kinetic", "at": 4, "items": [{"text": "TRỚ TRÊU", "at": 4, "sm": True}, {"text": "HÀNG TỶ LẦN GÕ CỦA TA", "at": [4, "hàng"]},
                                          {"text": "DẠY MÁY ĐỌC GIỎI LÊN", "at": [4, "lại"], "acc": True}]},
    {"type": "captcha", "at": 5, "mode": "grid", "head": "Chọn tất cả ô có đèn giao thông", "pick": [1, 3, 8], "selAt": [6, "Chọn"], "selGap": 0.9,
     "label": {"k": "VÒNG HAI: Ô ẢNH", "v": MOCK, "at": [5, "Vòng"]}},
    {"type": "broll", "at": 7, "vid": "12570193", "veil": 0.5, "illus": VM,
     "kin": [{"text": "ẢNH CHỤP ĐƯỜNG PHỐ", "at": [7, "ảnh"], "acc": True}, {"text": "một phần · từ năm 2012", "at": [7, "từ"], "sm": True}]},
    {"type": "ledger", "at": 8, "title": "DẠY XE TỰ LÁI?", "srcnote": "LỜI ĐẠI DIỆN GOOGLE: THEO BÁO CHÍ, 2021",
     "rows": [{"k": "NHIỀU NGƯỜI TIN", "v": "DẠY XE NHẬN RA ĐƯỜNG", "at": [8, "bạn"]}, {"k": "THỰC TẾ", "v": "CHƯA ĐƯỢC XÁC NHẬN", "at": [9, "Nhưng"]},
              {"k": "GOOGLE NÓI", "v": "CHỈ ĐỂ CẢI THIỆN BẢN ĐỒ", "at": [10, "chỉ"]}],
     "total": {"k": "CHẮC CHẮN", "v": "BẠN LẠI DÁN NHÃN HỘ MÁY", "at": [11, "bạn"]}},
    {"type": "kinetic", "at": 12, "items": [{"text": "MỘT LỐI TẮT", "at": [12, "một"], "acc": True},
                                           {"text": "chẳng cần tới trí tuệ nhân tạo nào", "at": 13, "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "MỘT ĐÔ CHO MỘT NGHÌN MÃ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "MỘT ĐÔ CHO\nMỘT NGHÌN MÃ", "sub": "MÁY KHÔNG QUA ĐƯỢC THÌ THUÊ NGƯỜI", "vid": "8865787", "illus": VM,
     "titleAt": [0, "Nếu"]},
    {"type": "broll", "at": 1, "vid": "8865787", "ms": 6, "veil": 0.5, "illus": VM,
     "kin": [{"text": "NGƯỜI THẬT NGỒI GÕ MÃ", "at": [2, "người"], "acc": True}, {"text": "thay cho các chương trình tự động", "at": [2, "thay"], "sm": True}]},
    {"type": "counter", "at": 3, "from": 0, "to": 1000, "suffix": " MÃ", "until": [3, "nghìn"], "label": "GIÁ KHOẢNG 1 ĐÔ LA",
     "sub": {"text": "NGHIÊN CỨU USENIX SECURITY, 2010", "at": 4}},
    {"type": "bars", "at": 5, "title": "THU NHẬP MỘT NGÀY CỦA NGƯỜI GÕ MÃ (USD)", "unit": "",
     "items": [{"k": "THẤP", "v": 2, "lbl": "~2", "at": [5, "hai,"]}, {"k": "CAO", "v": 3, "lbl": "~3", "at": [5, "ba"], "acc": True}],
     "label": {"k": "", "v": "THEO LỜI ĐỒNG TÁC GIẢ NGHIÊN CỨU · NPR, 2010", "at": 5}},
    {"type": "ledger", "at": 6, "title": "BÀI KIỂM TRA NÀY", "rows": [{"k": "SINH RA ĐỂ", "v": "PHÂN BIỆT NGƯỜI VỚI MÁY", "at": 7},
                                                                    {"k": "KHÔNG THẤY", "v": "NGƯỜI MỞ CỬA CHO MÁY", "at": [8, "với"]}]},
    {"type": "question", "at": 9, "text": "Bạn là người.\nNhưng bạn đang làm việc cho ai?", "showAt": 10},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "VÒNG BA: MỘT DẤU TICK"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "captcha", "mode": "tick", "tickAt": [2, "tick"], "label": {"k": "VÒNG BA · 12.2014", "v": MOCK, "at": [1, "Chỉ"]}},
    {"type": "ledger", "at": 3, "title": "THỨ ĐƯỢC CHẤM", "srcnote": "THEO GOOGLE, 12.2014",
     "rows": [{"k": "KHÔNG PHẢI", "v": "CÁI TICK", "at": [3, "không"]}, {"k": "MÀ LÀ", "v": "CÁCH BẠN TƯƠNG TÁC", "at": [4, "cách"]},
              {"k": "KHI NÀO", "v": "TRƯỚC · TRONG · SAU", "at": [4, "trước,"]}],
     "total": {"k": "NẾU NGHI", "v": "QUAY LẠI Ô ẢNH", "at": [5, "Nếu", 1]}},
    {"type": "kinetic", "at": 6, "items": [{"text": "KHÔNG HỎI BẠN GIỎI VIỆC GÌ", "at": 6, "sm": True},
                                          {"text": "XEM BẠN CƯ XỬ CÓ GIỐNG NGƯỜI", "at": [7, "bạn"], "acc": True}]},
    {"type": "question", "at": 8, "text": "Còn hai vòng cũ thì sao?"},
    {"type": "ledger", "at": 9, "title": "NGƯỜI THI VỚI MÁY · 2023", "srcnote": "ĐẠI HỌC CALIFORNIA, IRVINE · USENIX SECURITY 2023",
     "rows": [{"k": "NGƯỜI THI", "v": "HƠN 1.000 NGƯỜI", "at": [9, "hơn"]}, {"k": "ĐỀ", "v": "CÁC LOẠI MÃ XÁC NHẬN", "at": [9, "với"]}],
     "total": {"k": "RỒI", "v": "SO VỚI MÁY", "at": [9, "rồi"]}},
    {"type": "bars", "at": 10, "title": "GIẢI CHỮ MÉO: ĐÚNG BAO NHIÊU %", "unit": "",
     "items": [{"k": "MÁY", "v": 99, "lbl": "GẦN 100", "at": [10, "máy"], "acc": True}, {"k": "NGƯỜI · THẤP NHẤT", "v": 50, "lbl": "50", "at": [11, "năm"]},
               {"k": "NGƯỜI · CAO NHẤT", "v": 84, "lbl": "84", "at": [11, "tám"]}],
     "label": {"k": "NGƯỜI: TỚI 15 GIÂY · MÁY: < 1 GIÂY", "v": "THEO TƯỜNG THUẬT NGHIÊN CỨU UC IRVINE, 2023", "at": 12}},
    {"type": "counter", "at": 13, "from": 0, "to": 100, "suffix": "%", "until": [13, "trăm"], "label": "Ô ẢNH ĐƯỢC THỬ · MÁY GIẢI HẾT",
     "sub": {"text": "NHÓM NGHIÊN CỨU Ở THUỴ SĨ · 2024", "at": [13, "một", 1]}},
    {"type": "kinetic", "at": 14, "items": [{"text": "MỘT CHUYỆN NGHE NHƯ ĐÙA", "at": 14, "acc": True},
                                           {"text": "thử nghiệm an toàn · có người hướng dẫn · 2023", "at": 15, "sm": True}]},
    {"type": "chat", "at": 16, "head": "THỬ NGHIỆM AN TOÀN · 2023 · DIỄN LẠI",
     "msgs": [{"who": "u", "text": "Bạn là robot à, mà không tự giải được?", "at": 16},
              {"who": "m", "text": "Không, tôi không phải robot. Tôi bị khiếm thị, nên khó nhìn rõ các hình ảnh.", "at": 18}]},
    {"type": "slam", "at": 19, "text": "VÀ NGƯỜI KIA GIẢI HỘ", "sub": "NGUỒN: TÀI LIỆU CÔNG BỐ KÈM MÔ HÌNH, 03.2023"},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "KHI ĐỀ THI BIẾN MẤT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "THÊM MỘT PHIÊN BẢN NỮA", "date": "10.2018"},
    {"type": "ledger", "at": 1, "title": "LẦN NÀY", "rows": [{"k": "KHÔNG CÒN", "v": "CHỮ MÉO", "at": [1, "không"]}, {"k": "KHÔNG CÒN", "v": "Ô ẢNH", "at": [1, "Không"]},
                                                           {"k": "KHÔNG CÒN", "v": "Ô VUÔNG ĐỂ TICK", "at": [1, "Cũng"]}]},
    {"type": "broll", "at": 2, "vid": "1085656", "ms": 8, "veil": 0.55, "illus": VM,
     "kin": [{"text": "CHẠY NGẦM TRONG TRANG WEB", "at": [2, "chạy"], "acc": True}, {"text": "không hỏi bạn câu nào", "at": 3, "sm": True}]},
    {"type": "counter", "at": 4, "from": 0.0, "to": 0.9, "until": [4, "số,"], "label": "ĐIỂM SỐ CHO MỖI LƯỢT TRUY CẬP · CON SỐ MINH HOẠ",
     "sub": {"text": "ĐÁNG NGỜ TỚI ĐÂU · CHỦ TRANG WEB TỰ QUYẾT", "at": 5}},
    {"type": "ledger", "at": 6, "title": "ĐIỀU VỪA ĐỔI", "rows": [{"k": "TRƯỚC ĐÂY", "v": "BẠN BIẾT MÌNH ĐANG THI", "at": 8}],
     "total": {"k": "GIỜ", "v": "BỊ CHẤM MÀ KHÔNG HAY BIẾT", "at": 9}},
    {"type": "question", "at": 10, "text": "Còn người nghĩ ra\ntất cả chuyện này thì sao?"},
    {"type": "kinetic", "at": 11, "items": [{"text": "KHÔNG DỪNG Ở SÁCH CŨ", "at": 11, "sm": True}, {"text": "CÙNG Ý TƯỞNG · DỰ ÁN MỚI", "at": 12, "acc": True},
                                           {"text": "hàng triệu người · mỗi người mười giây", "at": 13, "sm": True}]},
    {"type": "broll", "at": 14, "vid": "6963836", "veil": 0.5, "illus": VM,
     "kin": [{"text": "DUOLINGO · 2012", "at": [14, "Duolingo"], "acc": True}, {"text": "người học dịch câu từ trang web thật", "at": [14, "dịch"], "sm": True}]},
    {"type": "ledger", "at": 16, "title": "VẪN LÀ CÔNG THỨC CŨ", "srcnote": "Ô ẢNH: THEO LỜI ĐẠI DIỆN GOOGLE, 2021",
     "rows": [{"k": "CHỮ MÉO", "v": "→ SÁCH CŨ ĐƯỢC ĐỌC LẠI", "at": 18}, {"k": "BÀI TẬP DỊCH", "v": "→ TRANG WEB ĐƯỢC DỊCH", "at": 19}],
     "total": {"k": "Ô ẢNH", "v": "→ BẢN ĐỒ CHÍNH XÁC HƠN", "at": 20}},
]}

CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "AI ĐANG CHẤM AI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "AI ĐANG CHẤM AI", "sub": "BÀI KIỂM TRA NÀY ĐO CÁI GÌ?", "vid": "1085656", "illus": VM,
     "titleAt": [0, "Vậy"]},
    {"type": "ledger", "at": 1, "title": "ĐỀ THI ĐÃ ĐỔI NGHĨA", "rows": [{"k": "LÚC ĐẦU", "v": "NGƯỜI LÀM ĐƯỢC, MÁY CHƯA", "at": 1},
                                                                       {"k": "GIỜ", "v": "KHÓ VỚI MÁY = KHÓ VỚI NGƯỜI", "at": 2}]},
    {"type": "counter", "at": 3, "from": 0, "to": 32, "suffix": " GIÂY", "until": [4, "hai"], "label": "TRUNG BÌNH MỖI LẦN GIẢI MÃ",
     "sub": {"text": "ƯỚC TÍNH CỦA CLOUDFLARE · 05.2021", "at": 4}},
    {"type": "counter", "at": 5, "from": 0, "to": 500, "suffix": " NĂM", "until": [5, "trăm"], "label": "LOÀI NGƯỜI TIÊU MẤT · MỖI NGÀY",
     "sub": {"text": "CHỈ LÀ ƯỚC TÍNH · CLOUDFLARE, 2021", "at": 6}},
    {"type": "timeline", "at": 7, "items": [{"year": "2000", "text": "ra đề để *máy không qua được*", "at": 7},
                                           {"year": "hôm nay", "text": "máy qua đề ấy *nhanh hơn ta*", "at": 8},
                                           {"year": "trên đường đi", "text": "*chính ta* đã dạy nó", "at": 9}]},
    {"type": "captcha", "at": 10, "mode": "tick", "tickAt": [10, "tick"], "label": {"k": "", "v": MOCK, "at": 10}},
    {"type": "kinetic", "at": 11, "items": [{"text": "TURING HỎI: MÁY GIỐNG NGƯỜI ĐẾN ĐÂU?", "at": 11, "sm": True},
                                           {"text": "Ô VUÔNG NÀY HỎI NGƯỢC LẠI BẠN", "at": [12, "hỏi"], "acc": True}]},
    {"type": "question", "at": 13, "text": "Lần gần nhất bạn trượt\n“tôi không phải người máy” là khi nào?"},
    {"type": "kinetic", "at": 14, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 14}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [14, "ở"], "acc": True}]},
]}

SPEC = {
    "title": "\"Tôi Không Phải Người Máy\": Ô Tick Nhỏ Đã Bắt Bạn Làm Việc Không Công Suốt Nhiều Năm",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["máy", "người", "tick", "méo", "ảnh", "chấm", "không", "công"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(9)],
    "youtube": {
        "titles": ["\"Tôi Không Phải Người Máy\": Ô Tick Nhỏ Đã Bắt Bạn Làm Việc Không Công Suốt Nhiều Năm",
                   "CAPTCHA: Bài Kiểm Tra Mà Máy Giờ Làm Giỏi Hơn Người",
                   "Mỗi Lần Gõ Mã Xác Nhận, Bạn Đã Giúp Số Hoá Một Cuốn Sách Cũ"],
        "summary": "Một cỗ máy hỏi bạn có phải là người không, và bạn phải chứng minh. Video kể lại ba \"vòng thi\" của mã xác nhận CAPTCHA: chữ "
                   "méo, ô ảnh, rồi một dấu tick. Vì sao nó ra đời năm 2000, vì sao suốt nhiều năm mỗi lần gõ mã bạn đã giúp đọc một từ trong "
                   "sách cũ, và vì sao hôm nay máy vượt bài kiểm tra ấy nhanh hơn con người.",
        "more": ["Hình \"mã xác nhận\" trong video là hình minh hoạ do kênh tự vẽ, không phải giao diện của dịch vụ nào. Chuyện ô ảnh \"dùng để "
                 "dạy xe tự lái\" là suy đoán phổ biến; theo báo chí, đại diện Google nói dữ liệu chỉ dùng để cải thiện bản đồ. Vụ mô hình AI nhờ "
                 "người giải mã là một thử nghiệm an toàn có người hướng dẫn (tài liệu công bố kèm mô hình, 03/2023), không phải máy tự ý làm "
                 "ngoài đời. Con số \"500 năm mỗi ngày\" là ước tính của Cloudflare (2021). Số liệu nghiên cứu 2023 lấy theo tường thuật báo chí. "
                 "Video không hướng dẫn cách vượt mã xác nhận. Lời trích được dịch và đọc bằng giọng máy."],
        "chapter_titles": {"ch00": "Mở đầu: ô vuông \"Tôi không phải người máy\"", "ch01": "Mười bài toán của Yahoo (2000)",
                           "ch02": "Vòng một: chữ méo, 500.000 giờ mỗi ngày", "ch03": "Việc không công của bạn: đọc hộ sách cũ",
                           "ch04": "Vòng hai: ô ảnh", "ch05": "Một đô cho một nghìn mã", "ch06": "Vòng ba: một dấu tick, và máy vượt người",
                           "ch07": "Khi đề thi biến mất: chấm điểm ngầm, và Duolingo", "ch08": "Ai đang chấm ai"},
        "sources": [
            "https://en.wikipedia.org/wiki/ReCAPTCHA",
            "https://www.sciencedaily.com/releases/2008/08/080814154329.htm",
            "https://www.npr.org/2008/08/14/93605988/web-security-words-help-digitize-old-books",
            "https://security.googleblog.com/2014/12/are-you-robot-introducing-no-captcha.html",
            "https://usenix.org/conference/usenixsecurity10/re-captchas%E2%80%94understanding-captcha-solving-services-economic-context",
            "https://www.usenix.org/conference/usenixsecurity23/presentation/searles",
            "https://arxiv.org/abs/2409.08831",
            "https://blog.cloudflare.com/introducing-cryptographic-attestation-of-personhood/",
            "https://security.googleblog.com/2018/10/introducing-recaptcha-v3-new-way-to.html",
            "https://www.technologyreview.com/2012/06/25/185211/startup-has-language-learners-translating-the-web/",
        ],
        "hashtags": ["CAPTCHA", "CôngNghệ", "TríTuệNhânTạo", "CôngNghệQuanhTa", "MindInTheMachine"],
        "tags": ["captcha", "captcha là gì", "tôi không phải người máy", "recaptcha", "mã xác nhận", "luis von ahn", "phép thử turing",
                 "trí tuệ nhân tạo", "công nghệ quanh ta", "lịch sử công nghệ"],
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
