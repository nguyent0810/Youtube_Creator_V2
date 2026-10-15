"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #15 "Máy thắng poker" (chuỗi Trận đấu Người – Máy).

    python data/long/mim-may-thang-poker/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Video về nghiên cứu AI, KHÔNG hướng dẫn chơi bài, không cổ vũ cờ bạc: mọi con số là "phỉnh" của thử nghiệm.
Clip: Pexels (ngang), gắn "VIDEO MINH HỌA", không phải hình ảnh trận đấu. Áp luật studio (14/10/2026): myth / source / units.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"libratus": "Li-bra-tút", "pluribus": "Plu-ri-bút", "deepstack": "Đíp-xtác", "claudico": "Clo-đi-cô", "polaris": "Pô-la-rít", "cepheus": "Xê-phê-út",
       "pittsburgh": "Pít-xbớc", "carnegie": "Các-nơ-ghi", "mellon": "Me-lần", "alberta": "An-béc-ta", "canada": "Ca-na-đa", "tuomas": "Tu-ô-mát",
       "sandholm": "Xen-hôm", "noam": "Nô-am", "brown": "Brao", "john": "Giôn", "von": "phôn", "neumann": "Nôi-man", "darren": "Đa-rần", "elias": "Ê-lai-ất",
       "facebook": "Phây-búc", "openai": "Ô-pần Ây-ai", "science": "Xai-ần", "poker": "pô-cơ", "deep": "Đíp", "blue": "Blu", "alphago": "An-pha Gô",
       "=AlphaGo": "An-pha Gô", "=AI": "ây ai", "chatbot": "chát-bót"}
VM = "VIDEO MINH HỌA · KHÔNG PHẢI HÌNH ẢNH TRẬN ĐẤU"
CHIP = "PHỈNH LÀ ĐƠN VỊ TÍNH ĐIỂM CỦA THỬ NGHIỆM · KHÔNG PHẢI TIỀN THẬT"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI MƯƠI NGÀY Ở PITTSBURGH"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "6813541", "veil": 0.55, "illus": VM,
     "kin": [{"text": "01.2017 · PITTSBURGH", "at": [0, "Tháng"], "sm": True}, {"text": "BỐN CAO THỦ POKER", "at": [1, "Bốn"], "acc": True}, {"text": "cùng đấu tay đôi với một đối thủ", "at": 2, "sm": True}]},
    {"type": "ledger", "at": 3, "title": "THỬ NGHIỆM", "rows": [{"k": "THỜI GIAN", "v": "20 NGÀY", "at": 3}, {"k": "SỐ VÁN", "v": "120.000", "at": 4}, {"k": "ĐỐI THỦ", "v": "KHÔNG ĂN · KHÔNG NGỦ · KHÔNG MỆT", "at": 5}],
     "total": {"k": "TÊN", "v": "LIBRATUS", "at": 6}},
    {"type": "counter", "at": 7, "from": 0, "to": 1766250, "suffix": " PHỈNH", "until": [7, "trăm"], "label": "CỖ MÁY DẪN TRƯỚC KHI VÁN CUỐI KẾT THÚC", "sub": {"text": CHIP, "at": 8}},
    {"type": "quote", "at": 10, "text": "Cứ như đang chơi với một kẻ gian lận, như thể nó nhìn thấy bài của tôi.", "who": "MỘT TRONG BỐN NGƯỜI CHƠI", "note": "DIỄN Ý · THEO BÁO CHÍ, 2017"},
    {"type": "slam", "at": 12, "text": "NÓ KHÔNG NHÌN THẤY", "sub": "ĐÓ MỚI LÀ ĐIỀU ĐÁNG NÓI", "subAt": 12},
    {"type": "ledger", "at": 15, "title": "BA LÁ BÀI ÚP", "rows": [{"k": "1", "v": "NHỮNG GÌ BẠN KHÔNG ĐƯỢC THẤY", "at": 17}, {"k": "2", "v": "NGHỆ THUẬT TỐ BỊP", "at": 18},
                                                                {"k": "3", "v": "ĐỐI THỦ BIẾT HỌC TỪ BẠN", "at": 19}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "VIDEO VỀ NGHIÊN CỨU AI", "at": 20, "acc": True}, {"text": "không hướng dẫn chơi bài · không cổ vũ cờ bạc", "at": [20, "Nó"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "VÌ SAO POKER KHÁC CỜ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG 01", "title": "VÌ SAO POKER\nKHÁC CỜ", "sub": "THÔNG TIN HOÀN HẢO · VÀ KHÔNG", "vid": "6813811", "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "myth", "at": 1, "mythLab": "CỜ VUA · CỜ VÂY", "myth": "MỌI QUÂN ĐỀU TRÊN BÀN", "truthLab": "POKER", "truth": "BÀI ÚP · THIẾU THÔNG TIN", "strikeAt": [5, "Poker"], "truthAt": [6, "lá"]},
    {"type": "ledger", "at": 9, "title": "ĐIỀU ĐÓ THAY ĐỔI MỌI THỨ", "rows": [{"k": "TRONG CỜ", "v": "KHÔNG CẦN BIẾT ĐỐI THỦ NGHĨ GÌ", "at": 10},
                                                                            {"k": "TRONG POKER", "v": "PHẢI ĐOÁN ĐỐI THỦ ĐOÁN GÌ", "at": 11}]},
    {"type": "source", "at": 12, "source": "JOHN VON NEUMANN · 1944", "ref": "LÝ THUYẾT TRÒ CHƠI", "snippet": "dùng poker làm ví dụ để hiểu [[hành vi tố bịp]]", "hlAt": [13, "tố"],
     "seal": "HƠN 70 NĂM SAU MÁY MỚI THẮNG", "sealAt": 14},
]}

CH["ch02"] = {"hud": {"k": "LÁ BÀI ÚP 01", "t": "NHỮNG GÌ BẠN KHÔNG ĐƯỢC THẤY"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "LÁ BÀI ÚP THỨ NHẤT", "title": "NHỮNG GÌ BẠN\nKHÔNG ĐƯỢC THẤY", "sub": "THỬ NGHĨ NHƯ MỘT CỖ MÁY", "vid": "6813811", "ms": 10, "illus": VM, "titleAt": [0, "Lá"]},
    {"type": "question", "at": 2, "text": "Đối thủ cược rất lớn.\nBài mạnh hơn? Hay đang doạ?", "showAt": 3},
    {"type": "myth", "at": 6, "mythLab": "MÁY CHƠI CỜ", "myth": "BIẾT CHẮC THẾ CỜ", "truthLab": "MÁY CHƠI POKER", "truth": "MỌI KHẢ NĂNG · MỖI CÁI MỘT XÁC SUẤT", "strikeAt": [7, "Một"], "truthAt": [8, "Nó"]},
    {"type": "ledger", "at": 9, "title": "CÁI BẪY", "rows": [{"k": "BÀI MẠNH", "v": "LUÔN CƯỢC LỚN", "at": [10, "luôn"]}, {"k": "BÀI YẾU", "v": "LUÔN CƯỢC NHỎ", "at": [10, "và"]}],
     "total": {"k": "KẾT QUẢ", "v": "BỊ ĐỌC VỊ", "at": [10, "đọc"]}},
    {"type": "slam", "at": 11, "text": "KHÓ ĐOÁN THEO ĐÚNG TỈ LỆ", "sub": "KHÔNG PHẢI NGẪU NHIÊN", "subAt": 12},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "PHÒNG THÍ NGHIỆM Ở CANADA"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG 03", "title": "PHÒNG THÍ NGHIỆM\nỞ CANADA", "sub": "ĐẠI HỌC ALBERTA", "vid": "1085656", "illus": VM, "titleAt": [0, "Một"]},
    {"type": "timeline", "at": 1, "items": [{"year": "2008", "text": "Polaris thắng cao thủ · poker giới hạn", "at": 1}, {"year": "01.2015", "text": "Cepheus gần như giải xong poker giới hạn tay đôi", "at": 3}]},
    {"type": "source", "at": 4, "source": "TẠP CHÍ SCIENCE · 01.2015", "ref": "POKER GIỚI HẠN, CHƠI TAY ĐÔI", "snippet": "[[gần như đã được giải]] · về lâu dài không ai thắng nổi một cách đáng kể", "hlAt": [4, "gần"], "seal": "CEPHEUS", "sealAt": 5},
    {"type": "ledger", "at": 6, "title": "ĐỂ LÀM ĐƯỢC", "rows": [{"k": "BỘ XỬ LÝ", "v": "4.800", "at": [6, "bốn"]}, {"k": "CHẠY LIÊN TỤC", "v": "68 NGÀY", "at": [6, "sáu"]}],
     "total": {"k": "KẾT QUẢ", "v": "GẦN NHƯ HOÀN HẢO", "at": 7}},
    {"type": "myth", "at": 9, "mythLab": "POKER GIỚI HẠN", "myth": "CƯỢC MỘT MỨC CỐ ĐỊNH", "truthLab": "KHÔNG GIỚI HẠN", "truth": "CƯỢC BAO NHIÊU CŨNG ĐƯỢC", "strikeAt": [10, "Kiểu"], "truthAt": [11, "Bạn"]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "MỘT CON SỐ 160 CHỮ SỐ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG 04", "title": "MỘT CON SỐ\nCÓ 160 CHỮ SỐ", "sub": "POKER KHÔNG GIỚI HẠN", "vid": "7608213", "illus": VM, "titleAt": [0, "Trong"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "10 · 11 · 12 · … · TẤT CẢ", "at": 1, "acc": True}, {"text": "mỗi mức cược mở ra một nhánh mới", "at": 2, "sm": True}]},
    {"type": "bars", "at": 3, "title": "SỐ CHỮ SỐ CỦA HAI CON SỐ", "unit": "ƯỚC TÍNH CỦA NHÓM LIBRATUS · ƯỚC TÍNH THƯỜNG DÙNG",
     "items": [{"k": "TÌNH HUỐNG RA QUYẾT ĐỊNH · POKER KHÔNG GIỚI HẠN TAY ĐÔI", "v": 161, "lbl": "≈161", "at": [3, "mười"], "acc": True},
               {"k": "NGUYÊN TỬ TRONG VŨ TRỤ QUAN SÁT ĐƯỢC", "v": 80, "lbl": "≈80", "at": 5}]},
    {"type": "ledger", "at": 6, "title": "CÁCH LÀM KHÉO", "rows": [{"k": "1", "v": "GỘP TÌNH HUỐNG GẦN GIỐNG NHAU", "at": 8}, {"k": "2", "v": "TÌM CÁCH CHƠI CHO BẢN THU NHỎ", "at": 10},
                                                                 {"k": "3", "v": "CHƠI THẬT: TÍNH LẠI CHO ĐÚNG", "at": 11}]},
    {"type": "slam", "at": 12, "text": "THU NHỎ MÀ KHÔNG MẤT", "sub": "ĐIỀU QUAN TRỌNG", "subAt": 12},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "LẦN THUA NĂM 2015"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG 05", "title": "LẦN THUA\nNĂM 2015", "sub": "CLAUDICO · CARNEGIE MELLON", "vid": "7330178", "illus": VM, "titleAt": [0, "Năm"]},
    {"type": "counter", "at": 3, "from": 0, "to": 732713, "suffix": " PHỈNH", "until": [3, "trăm"], "label": "CON NGƯỜI THẮNG CLAUDICO · 2015", "sub": {"text": "HỌ TÌM RA CHỖ YẾU VÀ KHAI THÁC", "at": 4}},
    {"type": "ledger", "at": 5, "title": "NHÓM NGHIÊN CỨU", "rows": [{"k": "GIÁO SƯ", "v": "TUOMAS SANDHOLM", "at": 5}, {"k": "NGHIÊN CỨU SINH", "v": "NOAM BROWN", "at": [5, "Noam"]}],
     "total": {"k": "CHƯA ĐẦY HAI NĂM SAU", "v": "QUAY LẠI", "at": 7}},
    {"type": "kinetic", "at": 8, "items": [{"text": "HAI NGƯỜI CHƠI NĂM ẤY CŨNG QUAY LẠI", "at": 8, "sm": True}, {"text": "LẦN NÀY: LIBRATUS", "at": [8, "Libratus"], "acc": True}]},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "HỌC BẰNG SỰ HỐI TIẾC"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG 06", "title": "HỌC BẰNG\nSỰ HỐI TIẾC", "sub": "TỰ CHƠI VỚI CHÍNH MÌNH", "vid": "5028622", "illus": VM, "titleAt": [0, "Libratus"]},
    {"type": "myth", "at": 1, "mythLab": "KHÔNG HỌC BẰNG", "myth": "XEM NGƯỜI KHÁC CHƠI", "truthLab": "MÀ", "truth": "TỰ CHƠI VỚI CHÍNH MÌNH", "strikeAt": [1, "Nó"], "truthAt": [1, "tự"]},
    {"type": "timeline", "at": 4, "items": [{"year": "SAU MỖI VÁN", "text": "giá như chọn cách khác, được thêm bao nhiêu?", "at": 4}, {"year": "CON SỐ ẤY", "text": "gọi là sự hối tiếc", "at": 5},
                                           {"year": "LẦN SAU", "text": "chọn nhiều hơn cách mình hối tiếc đã bỏ qua", "at": 6}]},
    {"type": "slam", "at": 7, "text": "CÂN BẰNG", "sub": "ĐỐI THỦ KHÓ TÌM CHỖ ĐỂ KHAI THÁC", "subAt": 8},
    {"type": "kinetic", "at": 9, "items": [{"text": "GIỐNG CON NGƯỜI HỌC TỪ SAI LẦM", "at": 9, "sm": True}, {"text": "NHƯNG SAI VÀ HỌC LẠI VÔ SỐ LẦN", "at": 10, "acc": True}]},
]}

CH["ch07"] = {"hud": {"k": "LÁ BÀI ÚP 02", "t": "TỐ BỊP"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "7", "k": "LÁ BÀI ÚP THỨ HAI", "title": "TỐ BỊP", "sub": "CƯỢC LỚN VỚI BÀI YẾU", "vid": "6813807", "illus": VM, "titleAt": [0, "Tố"]},
    {"type": "myth", "at": 1, "mythLab": "VỚI CON NGƯỜI", "myth": "TÂM LÝ · GAN DẠ · NÉT MẶT", "truthLab": "VỚI LIBRATUS", "truth": "TOÁN HỌC", "strikeAt": [2, "Với"], "truthAt": [2, "toán"]},
    {"type": "units", "at": 5, "title": "MINH HOẠ: TRONG MỘT SỐ LẦN CƯỢC LỚN, BÀI ĐANG YẾU", "total": 10, "cols": 10, "lit": 3, "litAt": [5, "bạn"], "unitLabel": "LẦN CƯỢC LỚN LÀ TỐ BỊP",
     "label": {"k": "TỈ LỆ ĐƯỢC TÍNH RA · CON SỐ TRÊN HÌNH CHỈ ĐỂ MINH HOẠ", "v": "", "at": 6}},
    {"type": "ledger", "at": 7, "title": "CỖ MÁY", "rows": [{"k": "KHÔNG", "v": "RUN · THỞ GẤP · LIẾC PHỈNH", "at": 8}, {"k": "CHỈ", "v": "DOẠ ĐÚNG TẦN SUẤT", "at": 9}]},
    {"type": "broll", "at": 10, "vid": "7608213", "ms": 6, "veil": 0.55, "illus": VM,
     "kin": [{"text": "NHỮNG MỨC CƯỢC LỚN BẤT THƯỜNG", "at": 11, "acc": True}, {"text": "ban đầu bị coi là sai lầm · rồi thành thứ khó đối phó", "at": 12, "sm": True}]},
]}

CH["ch08"] = {"hud": {"k": "LÁ BÀI ÚP 03", "t": "ĐỐI THỦ BIẾT HỌC"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "8", "k": "LÁ BÀI ÚP THỨ BA", "title": "ĐỐI THỦ\nBIẾT HỌC", "sub": "TỪ 11.01.2017", "vid": "6961922", "illus": VM, "titleAt": [0, "Trận"]},
    {"type": "ledger", "at": 1, "title": "ĐỘI CON NGƯỜI", "rows": [{"k": "MỖI TỐI", "v": "SO GHI CHÉP · TÌM ĐIỂM YẾU", "at": 2}, {"k": "NHỮNG NGÀY ĐẦU", "v": "TÌM ĐƯỢC · DỒN SỨC VÀO ĐÓ", "at": 4}]},
    {"type": "ledger", "at": 6, "title": "ĐỘI CỖ MÁY", "rows": [{"k": "MỖI ĐÊM", "v": "PHÂN TÍCH LỖ HỔNG BỊ KHAI THÁC", "at": 7}, {"k": "TRƯỚC SÁNG", "v": "VÁ BA LỖ HỔNG LỚN NHẤT", "at": 8}]},
    {"type": "units", "at": 9, "title": "MỖI ĐÊM · BA LỖ HỔNG ĐƯỢC VÁ", "total": 3, "cols": 3, "lit": 3, "litAt": 9, "unitLabel": "LỖ HỔNG"},
    {"type": "slam", "at": 11, "text": "ĐỐI THỦ HỌC TỪ CHÍNH BẠN", "sub": "LÁ BÀI ÚP THỨ BA", "subAt": 11},
]}

CH["ch09"] = {"hud": {"k": "CHƯƠNG 09", "t": "GẦN 1,8 TRIỆU PHỈNH"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "9", "k": "CHƯƠNG 09", "title": "GẦN MỘT TRIỆU\nTÁM TRĂM NGHÌN", "sub": "30.01.2017", "vid": "6813541", "ms": 4, "illus": VM, "titleAt": [0, "Ngày"]},
    {"type": "counter", "at": 1, "from": 1766250, "to": 1766250, "suffix": " PHỈNH", "label": "LIBRATUS DẪN TRƯỚC · CHUNG CUỘC", "sub": {"text": CHIP, "at": 1}},
    {"type": "myth", "at": 2, "mythLab": "CÓ PHẢI", "myth": "MAY MẮN?", "truthLab": "NHÓM NGHIÊN CỨU", "truth": "CÓ Ý NGHĨA THỐNG KÊ", "strikeAt": [2, "khẳng"], "truthAt": [3, "Nghĩa"]},
    {"type": "ledger", "at": 4, "title": "THEO CÁC NHÀ NGHIÊN CỨU", "rows": [{"k": "MÁY THẮNG", "v": "CẢ BỐN NGƯỜI CHƠI", "at": 4}, {"k": "HAI NGƯỜI", "v": "TỪNG THẮNG CLAUDICO", "at": 5}]},
    {"type": "broll", "at": 7, "vid": "5028622", "ms": 12, "veil": 0.55, "illus": VM,
     "kin": [{"text": "MỘT SIÊU MÁY TÍNH", "at": 7, "acc": True}, {"text": "chỉ để chơi tay đôi với một người", "at": 8, "sm": True}, {"text": "hai năm sau, câu chuyện ấy thay đổi", "at": 9, "sm": True}]},
]}

CH["ch10"] = {"hud": {"k": "CHƯƠNG 10", "t": "LÀM SAO LOẠI BỎ MAY MẮN?"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "10", "k": "CHƯƠNG 10", "title": "LÀM SAO LOẠI BỎ\nMAY MẮN?", "sub": "HAI CÁCH CỦA CÁC NHÀ NGHIÊN CỨU", "vid": "6813811", "ms": 8, "illus": VM, "titleAt": [0, "Poker"]},
    {"type": "question", "at": 3, "text": "Thắng vì giỏi,\nhay vì hên?"},
    {"type": "ledger", "at": 4, "title": "HAI CÁCH", "rows": [{"k": "1", "v": "CHƠI THẬT NHIỀU VÁN · 120.000", "at": 5}, {"k": "2", "v": "CHIA BÀI ĐỐI XỨNG", "at": 6}]},
    {"type": "timeline", "at": 8, "items": [{"year": "PHÒNG A", "text": "người 1 nhận tay bài X · máy nhận tay bài Y", "at": 8}, {"year": "PHÒNG B", "text": "người 2 nhận tay bài Y · máy nhận tay bài X", "at": [8, "người"]}]},
    {"type": "myth", "at": 9, "mythLab": "BÀI ĐẸP Ở BÀN NÀY", "myth": "CỖ MÁY HÊN", "truthLab": "THÌ Ở BÀN KIA", "truth": "PHẢI CẦM BÀI XẤU", "strikeAt": [10, "Phần"], "truthAt": [11, "Cái"]},
    {"type": "slam", "at": 12, "text": "KHÔNG PHẢI MỘT ĐÊM HÊN", "sub": "MÀ LÀ HAI MƯƠI NGÀY GIỎI HƠN", "subAt": 13},
]}

CH["ch11"] = {"hud": {"k": "CHƯƠNG 11", "t": "MỘT CỖ MÁY KHÁC Ở CANADA"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "11", "k": "CHƯƠNG 11", "title": "MỘT CỖ MÁY KHÁC\nỞ CANADA", "sub": "DEEPSTACK", "vid": "6346228", "illus": VM, "titleAt": [0, "Cùng"]},
    {"type": "ledger", "at": 2, "title": "THỬ NGHIỆM CỦA DEEPSTACK", "rows": [{"k": "NGƯỜI CHƠI", "v": "33 · TỪ 17 QUỐC GIA", "at": 2}, {"k": "MỖI TRẬN", "v": "3.000 VÁN · ≈4 TUẦN", "at": 3},
                                                                              {"k": "CHƠI HẾT TRẬN", "v": "11 NGƯỜI", "at": 4}], "total": {"k": "KẾT QUẢ", "v": "THẮNG CẢ 11", "at": 5}},
    {"type": "source", "at": 6, "source": "TẠP CHÍ SCIENCE · 03.2017", "ref": "DEEPSTACK", "snippet": "mỗi lượt [[tính lại cách chơi]] cho đúng tình huống đang gặp", "hlAt": [9, "tính"], "seal": "ĐẠI HỌC ALBERTA", "sealAt": 10},
    {"type": "myth", "at": 11, "mythLab": "HAI CỖ MÁY", "myth": "HAI CÁCH LÀM", "truthLab": "MỘT KẾT LUẬN", "truth": "POKER TAY ĐÔI: NGƯỜI ĐÃ THUA", "strikeAt": [12, "Ở"], "truthAt": [12, "con"]},
    {"type": "kinetic", "at": 13, "items": [{"text": "PHÁO ĐÀI CUỐI CÙNG", "at": 13, "sm": True}, {"text": "MỘT BÀN CÓ NHIỀU NGƯỜI", "at": [13, "một"], "acc": True}]},
]}

CH["ch12"] = {"hud": {"k": "CHƯƠNG 12", "t": "SÁU NGƯỜI MỘT BÀN"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "12", "k": "CHƯƠNG 12", "title": "SÁU NGƯỜI\nMỘT BÀN", "sub": "TOÁN HỌC TRỞ NÊN RỐI RẮM", "vid": "6961922", "ms": 12, "illus": VM, "titleAt": [0, "Poker"]},
    {"type": "myth", "at": 1, "mythLab": "TAY ĐÔI", "myth": "NGƯỜI NÀY THẮNG = NGƯỜI KIA THUA", "truthLab": "SÁU NGƯỜI", "truth": "KHÔNG CÒN CÁCH CHƠI ĐẢM BẢO", "strikeAt": [3, "Nhưng"], "truthAt": [5, "Không"]},
    {"type": "ledger", "at": 6, "title": "BÀN ĐÔNG NGƯỜI", "rows": [{"k": "1", "v": "LIÊN MINH NGẦM", "at": [6, "Liên"]}, {"k": "2", "v": "NGƯỜI CHƠI TỆ ĐỔI CẢ BÀN", "at": [6, "những"]}, {"k": "3", "v": "TÌNH HUỐNG KHÔNG AI ĐOÁN ĐƯỢC", "at": [6, "tình"]}]},
    {"type": "slam", "at": 7, "text": "MÁY CÒN LÂU MỚI THẮNG?", "sub": "HỌ ĐÃ NHẦM", "subAt": 8},
]}

CH["ch13"] = {"hud": {"k": "CHƯƠNG 13", "t": "TÁM NGÀY, DƯỚI 150 ĐÔ LA"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "13", "k": "CHƯƠNG 13", "title": "TÁM NGÀY,\nDƯỚI 150 ĐÔ LA", "sub": "PLURIBUS · 07.2019", "vid": "1085656", "ms": 8, "illus": VM, "titleAt": [0, "Tháng"]},
    {"type": "source", "at": 1, "source": "TẠP CHÍ SCIENCE · 07.2019", "ref": "PLURIBUS", "snippet": "Carnegie Mellon cùng [[một nhóm nghiên cứu AI của Facebook]]", "hlAt": [1, "Facebook"], "seal": "SÁU NGƯỜI · KHÔNG GIỚI HẠN", "sealAt": 2},
    {"type": "ledger", "at": 4, "title": "HUẤN LUYỆN PLURIBUS", "rows": [{"k": "THỜI GIAN", "v": "8 NGÀY", "at": [5, "tám"]}, {"k": "MÁY", "v": "1 MÁY CHỦ 64 LÕI · KHÔNG GPU", "at": [5, "một"]},
                                                                         {"k": "CHI PHÍ", "v": "< 150 ĐÔ LA · GIÁ ĐÁM MÂY", "at": 6}]},
    {"type": "myth", "at": 7, "mythLab": "2017 · LIBRATUS", "myth": "CẢ MỘT SIÊU MÁY TÍNH", "truthLab": "2019 · PLURIBUS", "truth": "BẰNG MỘT BỮA ĂN NHÀ HÀNG", "strikeAt": [8, "Giờ"], "truthAt": [8, "bằng"]},
    {"type": "ledger", "at": 9, "title": "HAI THỬ NGHIỆM", "rows": [{"k": "1", "v": "5 NGƯỜI + PLURIBUS · 10.000 VÁN", "at": 10}, {"k": "2", "v": "2 CAO THỦ · MỖI NGƯỜI 5.000 VÁN", "at": 11}],
     "total": {"k": "KẾT QUẢ", "v": "PLURIBUS THẮNG", "at": 13}},
]}

CH["ch14"] = {"hud": {"k": "CHƯƠNG 14", "t": "MÁY CHƠI KHÁC NGƯỜI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "14", "k": "CHƯƠNG 14", "title": "MÁY CHƠI\nKHÁC NGƯỜI", "sub": "NHỮNG ĐIỀU SÁCH VỞ KHUYÊN TRÁNH", "vid": "7330178", "ms": 2, "illus": VM, "titleAt": [0, "Điều"]},
    {"type": "ledger", "at": 2, "title": "PLURIBUS ĐÔI KHI", "rows": [{"k": "1", "v": "MỞ VÒNG CƯỢC KIỂU BỊ COI LÀ DỞ", "at": 2}, {"k": "2", "v": "CƯỢC LỚN TRÔNG NHƯ LIỀU", "at": 3}],
     "total": {"k": "CỘNG HÀNG NGHÌN VÁN", "v": "LẠI CÓ LỢI", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "NHƯ NƯỚC 37 CỦA ALPHAGO", "at": 5, "acc": True}, {"text": "không bắt chước người · tìm cách của riêng mình", "at": 6, "sm": True}]},
    {"type": "myth", "at": 7, "mythLab": "CỖ MÁY TỪNG LÀ", "myth": "ĐỐI THỦ", "truthLab": "GIỜ LÀ", "truth": "NGƯỜI THẦY", "strikeAt": [8, "Họ"], "truthAt": [10, "Cỗ"]},
]}

CH["ch15"] = {"hud": {"k": "CHƯƠNG 15", "t": "CỖ MÁY KHÔNG ĐỌC VỊ AI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "15", "k": "CHƯƠNG 15", "title": "CỖ MÁY\nKHÔNG ĐỌC VỊ AI", "sub": "NGHE NGƯỢC ĐỜI", "vid": "6813807", "ms": 10, "illus": VM, "titleAt": [0, "Có"]},
    {"type": "ledger", "at": 2, "title": "CAO THỦ CON NGƯỜI", "rows": [{"k": "TÌM", "v": "THÓI QUEN CỦA ĐỐI THỦ", "at": 2}, {"k": "VÍ DỤ", "v": "HAY DOẠ · HAY BỎ KHI BỊ ÉP", "at": 3}],
     "total": {"k": "RỒI", "v": "KHAI THÁC THÓI QUEN ẤY", "at": 4}},
    {"type": "source", "at": 5, "source": "BÀI BÁO VỀ PLURIBUS · SCIENCE, 07.2019", "ref": "PLURIBUS", "snippet": "[[không điều chỉnh cách chơi]] theo thói quen quan sát được ở đối thủ", "hlAt": [5, "không"], "seal": "CHƠI CÂN BẰNG", "sealAt": 6},
    {"type": "myth", "at": 7, "mythLab": "NGHE NHƯ", "myth": "BỎ PHÍ CƠ HỘI", "truthLab": "THẬT RA", "truth": "KHÔNG ĐỂ LỘ SƠ HỞ", "strikeAt": [8, "Nhưng"], "truthAt": [10, "Cỗ"]},
    {"type": "slam", "at": 11, "text": "NÓ CHỈ CẦN KHÔNG SAI", "sub": "KHÔNG CẦN BIẾT BẠN LÀ AI", "subAt": 11},
]}

CH["ch16"] = {"hud": {"k": "CHƯƠNG 16", "t": "SUY NGHĨ LÂU HƠN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "16", "k": "CHƯƠNG 16", "title": "SUY NGHĨ\nLÂU HƠN", "sub": "TỪ BÀN POKER TỚI CHATBOT", "vid": "6346228", "ms": 6, "illus": VM, "titleAt": [0, "Có"]},
    {"type": "ledger", "at": 1, "title": "LIBRATUS · DEEPSTACK · PLURIBUS", "rows": [{"k": "KHÔNG CHỈ", "v": "DỰA VÀO ĐIỀU ĐÃ HỌC SẴN", "at": 2}, {"k": "TỚI LƯỢT", "v": "TÍNH LẠI CHO ĐÚNG TÌNH HUỐNG", "at": 3}],
     "total": {"k": "NÓI CÁCH KHÁC", "v": "SUY NGHĨ LÂU HƠN", "at": 4}},
    {"type": "timeline", "at": 5, "items": [{"year": "2017", "text": "Libratus · Pittsburgh", "at": 5}, {"year": "2019", "text": "Pluribus · sáu người một bàn", "at": [5, "Noam"]},
                                           {"year": "2023", "text": "Noam Brown sang OpenAI", "at": [5, "OpenAI"]}, {"year": "2024", "text": "mô hình ngôn ngữ “suy nghĩ trước khi trả lời”", "at": 8}]},
    {"type": "slam", "at": 9, "text": "THÊM CHÚT THỜI GIAN ĐỂ NGHĨ", "sub": "ĐÔI KHI LÀ ĐỦ CHO CÂU TRẢ LỜI TỐT HƠN", "subAt": 10},
]}

CH["ch17"] = {"hud": {"k": "CHƯƠNG 17", "t": "NGOÀI BÀN BÀI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "17", "k": "CHƯƠNG 17", "title": "NGOÀI BÀN BÀI", "sub": "TRÒ CHƠI CÓ THÔNG TIN BỊ CHE", "vid": "6814372", "illus": VM, "titleAt": [0, "Poker"]},
    {"type": "ledger", "at": 2, "title": "GIỐNG POKER Ở ĐỜI THẬT", "rows": [{"k": "1", "v": "ĐÀM PHÁN HỢP ĐỒNG", "at": 2}, {"k": "2", "v": "ĐẤU GIÁ", "at": 3}, {"k": "3", "v": "AN NINH MẠNG", "at": 4}],
     "total": {"k": "ĐIỂM CHUNG", "v": "THÔNG TIN BỊ CHE", "at": 5}},
    {"type": "broll", "at": 6, "vid": "7584599", "veil": 0.55, "illus": VM,
     "kin": [{"text": "THUẬT TOÁN GHÉP CẶP HIẾN THẬN CHÉO", "at": 7, "acc": True}, {"text": "giáo sư Sandholm thiết kế · dùng ở Mỹ", "at": [7, "ở"], "sm": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "TỪ NHỮNG LÁ BÀI ÚP", "at": 8, "sm": True}, {"text": "TỚI NHỮNG QUẢ THẬN ĐƯỢC GHÉP ĐÚNG NGƯỜI", "at": [8, "tới"], "acc": True}]},
]}

CH["ch18"] = {"hud": {"k": "PHẦN CUỐI", "t": "BA LÁ BÀI ÚP"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "18", "k": "PHẦN CUỐI", "title": "BA LÁ BÀI ÚP", "sub": "LẬT LẠI TỪNG LÁ", "vid": "6813541", "ms": 8, "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "ledger", "at": 1, "title": "BA LÁ BÀI ÚP", "rows": [{"k": "1 · BỊ CHE", "v": "CÂN NHẮC MỌI KHẢ NĂNG", "at": 1}, {"k": "2 · TỐ BỊP", "v": "DOẠ ĐÚNG TẦN SUẤT", "at": 2},
                                                               {"k": "3 · ĐỐI THỦ BIẾT HỌC", "v": "VÁ LỖ HỔNG MỖI ĐÊM", "at": 3}]},
    {"type": "myth", "at": 4, "mythLab": "TỪNG ĐƯỢC COI LÀ", "myth": "TRỰC GIÁC · GAN DẠ · ĐỌC NGƯỜI", "truthLab": "HOÁ RA", "truth": "VIẾT ĐƯỢC THÀNH TOÁN HỌC", "strikeAt": [6, "Hoá"], "truthAt": [6, "toán"]},
    {"type": "kinetic", "at": 7, "items": [{"text": "NÓ KHÔNG NGỒI VÀO BÀN VÌ NÓ THÍCH", "at": 8, "sm": True}, {"text": "VỚI NÓ, CHỈ LÀ MỘT BÀI TOÁN", "at": 9, "acc": True}]},
    {"type": "question", "at": 10, "text": "Kỹ năng nào của con người\nlà thứ máy khó học nhất?"},
]}

SPEC = {
    "title": "Máy Thắng Poker: Cỗ Máy Học Cách Tố Bịp, Và Ba Lá Bài Úp",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["libratus", "pluribus", "bịp", "máy", "bài", "úp", "phỉnh", "thắng"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(19)],
    "youtube": {
        "titles": ["Máy Thắng Poker: Cỗ Máy Học Cách Tố Bịp, Và Ba Lá Bài Úp",
                   "Hai Mươi Ngày Ở Pittsburgh: Bốn Cao Thủ Poker Đấu Một Cỗ Máy, 2017",
                   "Vì Sao Poker Khó Cho Máy Hơn Cờ Vây? Libratus, Pluribus Và Nghệ Thuật Tố Bịp"],
        "summary": "Tháng 1/2017, bốn cao thủ poker đấu tay đôi 120.000 ván với chương trình Libratus của Đại học Carnegie Mellon, và thua. Video lật ba "
                   "“lá bài úp” làm poker khó cho máy: thông tin bị che, tố bịp, và một đối thủ biết vá lỗ hổng mỗi đêm. Kèm DeepStack, Pluribus thắng ở "
                   "bàn sáu người với chi phí huấn luyện dưới 150 đô la, vì sao máy không cần đọc vị ai, và sợi chỉ nối từ bàn poker tới những mô hình AI "
                   "“suy nghĩ trước khi trả lời”. Video về nghiên cứu AI, không hướng dẫn chơi bài, không cổ vũ cờ bạc.",
        "more": ["Các con số thắng thua là “phỉnh”, đơn vị tính điểm của thử nghiệm, không phải tiền thật. Cảm nhận của người chơi ở đầu video là diễn ý "
                 "theo báo chí. Số tình huống của poker không giới hạn (≈10^161) là ước tính của nhóm làm ra Libratus. Video làm nền không phải hình ảnh "
                 "trận đấu. Video không hướng dẫn chơi bài và không cổ vũ cờ bạc."],
        "chapter_titles": {"ch00": "Mở đầu: hai mươi ngày ở Pittsburgh", "ch01": "Vì sao poker khác cờ", "ch02": "Lá bài úp 1: những gì bạn không được thấy",
                           "ch03": "Phòng thí nghiệm ở Canada: Polaris, Cepheus", "ch04": "Một con số có 160 chữ số", "ch05": "Lần thua năm 2015",
                           "ch06": "Học bằng sự hối tiếc", "ch07": "Lá bài úp 2: tố bịp", "ch08": "Lá bài úp 3: đối thủ biết học", "ch09": "Gần 1,8 triệu phỉnh",
                           "ch10": "Làm sao loại bỏ may mắn?", "ch11": "DeepStack: một cỗ máy khác ở Canada", "ch12": "Sáu người một bàn",
                           "ch13": "Pluribus: tám ngày, dưới 150 đô la", "ch14": "Máy chơi khác người", "ch15": "Cỗ máy không đọc vị ai", "ch16": "Suy nghĩ lâu hơn",
                           "ch17": "Ngoài bàn bài", "ch18": "Ba lá bài úp"},
        "sources": ["https://www.cmu.edu/news/stories/archives/2017/january/AI-beats-poker-pros.html",
                    "https://money.cnn.com/2017/01/31/technology/poker-ai-tournament/index.html",
                    "https://www.engadget.com/2017-02-10-libratus-ai-poker-winner.html",
                    "https://www.ualberta.ca/computing-science/news-and-events/news/2015/january/solve-texas-holdem-poker.html",
                    "https://www.ualberta.ca/science/news/2017/march/artificial-intelligence-deepstack-outplays-poker-professionals.html",
                    "https://ai.facebook.com/blog/pluribus-first-ai-to-beat-pros-in-6-player-poker",
                    "https://www.theregister.com/2019/07/12/pluribus_ai_poker_human_pros"],
        "hashtags": ["Libratus", "Pluribus", "TríTuệNhânTạo", "LịchSửAI", "MindInTheMachine"],
        "tags": ["ai poker", "libratus", "pluribus", "deepstack", "máy thắng poker", "trí tuệ nhân tạo", "lý thuyết trò chơi", "tố bịp", "người đấu với máy",
                 "lịch sử ai", "noam brown"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        for sc in c["scenes"]:              # quote: "who" + "note" -> "by"; "qline" = dòng lời trích (dòng "at" hoặc dòng ngay sau)
            if sc["type"] == "quote" and "who" in sc:
                k = sc["at"]
                is_q = lambda i: isinstance(d["lines"][i], dict) and d["lines"][i].get("q")
                sc["qline"] = k if is_q(k) else k + 1
                assert is_q(sc["qline"]), (name, k)
                sc["by"] = f'{sc.pop("who")} · {sc.pop("note")}'
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")


if __name__ == "__main__":
    main()
