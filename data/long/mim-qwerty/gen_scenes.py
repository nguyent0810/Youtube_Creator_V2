"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #11 "Bàn phím QWERTY".

    python data/long/mim-qwerty/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Cảnh "keyboard" (lab.js) là bàn phím do kênh TỰ VẼ. Clip: Pexels (ngang), gắn "VIDEO MINH HỌA".
Vì sao phím nằm đúng chỗ ấy: giới sử học chưa thống nhất -> màn hình luôn ghi "MỘT CÁCH GIẢI THÍCH". beat2 bật.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"=QWERTY": "quớt-ti", "qwerty": "quớt-ti", "=Q": "quy", "=W": "vê kép", "=E": "e", "=R": "e-rờ", "=T": "tê", "=Y": "i dài",
       "=A": "a", "=B": "bê", "=C": "xê", "=S": "ét", "=Â": "ớ", "milwaukee": "Miu-oa-ki", "christopher": "Crít-xtô-phơ", "sholes": "Sôn",
       "piano": "pi-a-nô", "kyoto": "Ki-ô-tô", "morse": "Moóc-xơ", "remington": "Rem-minh-tần", "typewriter": "tai-rai-tơ", "shift": "síp",
       "cincinnati": "Xin-xi-na-ti", "frank": "Phreng", "mcgurrin": "Mác Gơ-rin", "august": "Âu-gớt", "dvorak": "Đờ-vo-rắc", "telex": "Tê-lếch", "paul": "Pôn", "david": "Đây-vít", "azerty": "a-déc-ti", "=AZERTY": "a-déc-ti"}
VM = "VIDEO MINH HỌA"
MOCK = "BÀN PHÍM DO KÊNH TỰ VẼ"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HÀNG PHÍM KỲ LẠ"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "4973401", "veil": 0.45, "illus": VM, "kin": [{"text": "NHÌN XUỐNG BÀN PHÍM", "at": [0, "nhìn"], "acc": True}]},
    {"type": "keyboard", "at": 1, "layout": "qwerty", "hl": "QWERTY", "hlAt": [1, "Q,"], "hlGap": 0.42,
     "label": {"k": "HÀNG CHỮ ĐẦU TIÊN", "v": MOCK, "at": 1}},
    {"type": "keyboard", "at": 2, "layout": "abc", "hl": "ABC", "hlAt": [2, "A,"], "hlGap": 0.35,
     "label": {"k": "KHÔNG PHẢI A B C", "v": MOCK, "at": 2}},
    {"type": "kinetic", "at": 3, "items": [{"text": "KHÔNG THEO THỨ TỰ NÀO", "at": 3, "acc": True}, {"text": "bạn từng học ở trường", "at": [3, "bạn"], "sm": True}]},
    {"type": "counter", "at": 4, "from": 0, "to": 150, "prefix": "~", "suffix": " NĂM", "until": [4, "mươi"], "label": "CẢ THẾ GIỚI GÕ THEO ĐÚNG THỨ TỰ ẤY"},
    {"type": "kinetic", "at": 5, "items": [{"text": "MỘT LỜI GIẢI THÍCH QUEN TAI", "at": 5, "sm": True},
                                          {"text": "“ĐỂ BẠN GÕ CHẬM LẠI”", "at": [6, "để"], "acc": True}, {"text": "vô lý · nên lan rất xa", "at": 7, "sm": True}]},
    {"type": "broll", "at": 8, "vid": "6699964", "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỘT PHIÊN TOÀ NHỎ", "at": [8, "một"], "acc": True}, {"text": "xử hàng phím này", "at": [8, "xử"], "sm": True}]},
    {"type": "ledger", "at": 9, "title": "BA LỜI BUỘC TỘI", "rows": [{"k": "1", "v": "SINH RA ĐỂ LÀM BẠN GÕ CHẬM", "at": 10},
                                                                   {"k": "2", "v": "THẮNG KHÔNG PHẢI VÌ TỐT", "at": 11},
                                                                   {"k": "3", "v": "VÙI DẬP BÀN PHÍM TỐT HƠN", "at": 12}]},
    {"type": "question", "at": 13, "text": "Phán quyết:\nbạn là người quyết."},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CHIẾC MÁY CỦA ÔNG CHỦ NHÀ IN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CHIẾC MÁY CỦA\nÔNG CHỦ NHÀ IN", "sub": "MILWAUKEE · CUỐI NHỮNG NĂM 1860", "vid": "29906414", "illus": VM,
     "titleAt": [0, "Bị"]},
    {"type": "ledger", "at": 1, "title": "CHA ĐẺ CỦA BỊ CÁO", "rows": [{"k": "TÊN", "v": "CHRISTOPHER SHOLES", "at": [1, "Christopher"]},
                                                                     {"k": "NGHỀ", "v": "LÀM NGHỀ IN", "at": [1, "một"]},
                                                                     {"k": "Ý ĐỊNH", "v": "MÁY ĐÁNH SỐ TRANG SÁCH", "at": 2}],
     "total": {"k": "GỢI Ý", "v": "SAO KHÔNG IN CẢ CHỮ?", "at": [3, "sao"]}},
    {"type": "broll", "at": 4, "vid": "1795798", "veil": 0.45, "illus": VM,
     "kin": [{"text": "BÀN PHÍM NHƯ PHÍM ĐÀN PIANO", "at": [4, "bàn"], "acc": True}]},
    {"type": "keyboard", "at": 5, "layout": "abc", "hl": "ABCDEFG", "hlAt": [5, "A,"], "hlGap": 0.22,
     "label": {"k": "MẪU ĐẦU TIÊN: THEO THỨ TỰ A B C", "v": MOCK + " · THEO MÔ TẢ", "at": 5}},
    {"type": "counter", "at": 7, "from": 0, "to": 5, "prefix": "~", "suffix": " NĂM", "until": [7, "năm", 1], "label": "SỬA ĐI SỬA LẠI BỐ CỤC PHÍM",
     "sub": {"text": "chữ này lên hàng trên · chữ kia sang phải", "at": 8}},
    {"type": "keyboard", "at": 9, "layout": "qwerty", "hl": "QWERTYUIOP", "hlAt": [9, "bố"], "hlGap": 0.1,
     "label": {"k": "NĂM 1873: GẦN GIỐNG HÔM NAY", "v": MOCK, "at": 9}},
    {"type": "question", "at": 10, "text": "Ông sửa để làm gì?"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "LỜI BUỘC TỘI THỨ NHẤT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "broll", "vid": "6980925", "veil": 0.5, "illus": VM,
     "kin": [{"text": "LỜI BUỘC TỘI 1", "at": 0, "sm": True}, {"text": "“LÀM BẠN GÕ CHẬM”", "at": [0, "kể"], "acc": True},
             {"text": "cần chữ bằng kim loại · gõ nhanh là kẹt", "at": 2, "sm": True}]},
    {"type": "ledger", "at": 3, "title": "CÁCH GIẢI THÍCH QUEN THUỘC", "srcnote": "MỘT CÁCH GIẢI THÍCH · CHƯA NGÃ NGŨ",
     "rows": [{"k": "VẤN ĐỀ", "v": "HAI CẦN CHỮ VA NHAU, KẸT", "at": 3}, {"k": "CÁCH SỬA", "v": "TÁCH CẶP CHỮ HAY ĐI LIỀN", "at": [3, "tách"]}],
     "total": {"k": "MỤC ĐÍCH", "v": "MÁY ĐỪNG KẸT, GÕ LIÊN TỤC", "at": 5}},
    {"type": "keyboard", "at": 6, "layout": "qwerty", "hl": "ER", "hlAt": [8, "E"], "hlGap": 0.5,
     "label": {"k": "LỖ HỔNG: E VÀ R NẰM SÁT NHAU", "v": MOCK, "at": 7}},
    {"type": "ledger", "at": 9, "title": "ĐẠI HỌC KYOTO · 2011", "srcnote": "YASUOKA & YASUOKA · ZINBUN, 03.2011",
     "rows": [{"k": "NGƯỜI DÙNG THỬ", "v": "CÁC ĐIỆN TÍN VIÊN", "at": 11}, {"k": "VIỆC CỦA HỌ", "v": "NGHE MORSE, CHÉP THÀNH CHỮ", "at": [11, "những"]},
              {"k": "BỐ CỤC", "v": "SỬA THEO YÊU CẦU CỦA HỌ", "at": 12}],
     "total": {"k": "KẾT QUẢ", "v": "THÀNH QWERTY KHÁ TÌNH CỜ", "at": 13}},
    {"type": "slam", "at": 14, "text": "“VÔ NGHĨA”", "sub": "CHUYỆN CỐ TÌNH LÀM NGƯỜI GÕ CHẬM · THEO HAI TÁC GIẢ"},
    {"type": "broll", "at": 15, "vid": "6101367", "veil": 0.5, "illus": VM,
     "kin": [{"text": "PHÁN QUYẾT 1", "at": 15, "sm": True}, {"text": "VÔ TỘI", "at": [15, "vô"], "acc": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "VÌ SAO TỪNG PHÍM NẰM ĐÚNG CHỖ ẤY?", "at": 17, "sm": True},
                                           {"text": "GIỚI SỬ HỌC CHƯA THỐNG NHẤT", "at": [17, "giới"], "acc": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "HÃNG SÚNG VÀ CHỮ TYPEWRITER"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "HÃNG SÚNG VÀ\nCHỮ TYPEWRITER", "sub": "CÓ MÁY · KHÔNG CÓ TIỀN", "vid": "3977979", "illus": VM,
     "titleAt": [0, "Sholes"]},
    {"type": "date", "at": 1, "day": "HỢP ĐỒNG LÀM 1.000 CHIẾC ĐẦU TIÊN", "date": "01.03.1873"},
    {"type": "slam", "at": 2, "text": "REMINGTON", "sub": "MỘT HÃNG SẢN XUẤT SÚNG"},
    {"type": "keyboard", "at": 3, "layout": "qwerty", "hl": "TYPEWRITER", "hlAt": [5, "gõ"], "hlGap": 0.32,
     "label": {"k": "T-Y-P-E-W-R-I-T-E-R: TRỌN TRÊN MỘT HÀNG", "v": MOCK + " · THEO LỜI KỂ", "at": [5, "để"]}},
    {"type": "ledger", "at": 7, "title": "CHIẾC MÁY BÁN RA", "srcnote": "THEO TƯ LIỆU VỀ MÁY SHOLES & GLIDDEN",
     "rows": [{"k": "NGÀY", "v": "01.07.1874", "at": 7}, {"k": "GIÁ", "v": "KHOẢNG 125 ĐÔ LA", "at": [7, "giá"]},
              {"k": "CHỮ", "v": "CHỈ CÓ CHỮ IN HOA", "at": 8}],
     "total": {"k": "CUỐI NĂM", "v": "CHỈ ~400 CHIẾC", "at": [9, "chỉ"]}},
    {"type": "timeline", "at": 10, "items": [{"year": "1874", "text": "bán ra · *rất chậm*", "at": 10},
                                            {"year": "1878", "text": "đời hai: có *phím Shift*, gõ cả chữ thường", "at": [10, "có"]},
                                            {"year": "nhưng", "text": "QWERTY *chưa hề thắng*", "at": 11}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "NHIỀU MÁY KHÁC · NHIỀU BÀN PHÍM KHÁC", "at": 12, "sm": True},
                                           {"text": "QUYẾT ĐỊNH: MỘT CUỘC THI", "at": [13, "một"], "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "LỜI BUỘC TỘI THỨ HAI"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "CINCINNATI · CUỘC THI GÕ MÁY", "date": "25.07.1888"},
    {"type": "ledger", "at": 2, "title": "HAI ĐỐI THỦ", "srcnote": "THEO TƯ LIỆU VỀ CUỘC THI NĂM 1888",
     "rows": [{"k": "NGƯỜI THỨ NHẤT", "v": "BÀN PHÍM ĐÔI, NHÌN PHÍM", "at": 2}, {"k": "McGURRIN", "v": "REMINGTON · QWERTY", "at": 4}],
     "total": {"k": "BÍ QUYẾT", "v": "MƯỜI NGÓN, KHÔNG NHÌN", "at": [5, "Gõ"]}},
    {"type": "broll", "at": 6, "vid": "6979935", "veil": 0.5, "illus": VM,
     "kin": [{"text": "McGURRIN THẮNG ÁP ĐẢO", "at": 6, "acc": True}, {"text": "kết quả lên trang nhất nhiều tờ báo", "at": 7, "sm": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "KẾT LUẬN HƠI VỘI", "at": 8, "sm": True}, {"text": "“BÀN PHÍM NHANH NHẤT”", "at": [8, "bàn"]},
                                          {"text": "THẬT RA: CÁCH GÕ MƯỜI NGÓN THẮNG", "at": [9, "thứ"], "acc": True}]},
    {"type": "ledger", "at": 10, "title": "VÒNG XOÁY", "rows": [{"k": "TRƯỜNG DẠY", "v": "DẠY THEO MÁY REMINGTON", "at": 10},
                                                              {"k": "NGƯỜI HỌC", "v": "MUỐN MUA MÁY QWERTY", "at": 11},
                                                              {"k": "HÃNG KHÁC", "v": "PHẢI LÀM BÀN PHÍM QWERTY", "at": 12}]},
    {"type": "counter", "at": 13, "from": 0, "to": 5, "suffix": " HÃNG", "until": [13, "hãng"], "label": "LỚN NHẤT NƯỚC MỸ SÁP NHẬP · CHỌN QWERTY",
     "sub": {"text": "NĂM 1893 · CUỘC ĐUA KHÉP LẠI", "at": 14}},
    {"type": "broll", "at": 15, "vid": "6699964", "veil": 0.5, "illus": VM,
     "kin": [{"text": "PHÁN QUYẾT 2", "at": 15, "sm": True}, {"text": "CÓ TỘI MỘT PHẦN", "at": [15, "có"], "acc": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "THẮNG VÌ TỚI TRƯỚC", "at": 17, "acc": True},
                                           {"text": "và vì hàng triệu người đã lỡ học nó rồi", "at": [17, "và"], "sm": True}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "LỜI BUỘC TỘI THỨ BA"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "KẺ THÁCH THỨC", "sub": "AUGUST DVORAK · 1936", "vid": "6980918", "illus": VM,
     "titleAt": [0, "August"]},
    {"type": "keyboard", "at": 2, "layout": "qwerty", "row": 1, "rowAt": [2, "hàng"], "hl": "A", "hlAt": [3, "là"],
     "label": {"k": "QWERTY: HÀNG GIỮA CHỈ CÓ MỘT NGUYÊN ÂM", "v": MOCK, "at": 3}},
    {"type": "keyboard", "at": 4, "layout": "dvorak", "row": 1, "rowAt": [4, "về"], "hl": "AOEUI", "hlAt": [4, "hàng"], "hlGap": 0.2,
     "label": {"k": "DVORAK: ĐỔI CHỖ 23 / 26 CHỮ CÁI", "v": MOCK + " · CHỈ VẼ PHÍM CHỮ", "at": [4, "Ông"]}},
    {"type": "ledger", "at": 5, "title": "THỬ NGHIỆM NĂM 1944", "srcnote": "THEO TƯỜNG THUẬT CỦA CHÍNH DVORAK",
     "rows": [{"k": "AI LÀM", "v": "HẢI QUÂN MỸ", "at": 6}, {"k": "AI THI", "v": "14 NHÂN VIÊN ĐÁNH MÁY", "at": [6, "mười"]}],
     "total": {"k": "KẾT QUẢ", "v": "NHANH HƠN TỚI 74%", "at": [7, "Họ"]}},
    {"type": "kinetic", "at": 8, "items": [{"text": "NẾU ĐÚNG THẾ", "at": 8, "sm": True}, {"text": "CẢ THẾ GIỚI DÙNG THỨ KÉM HƠN", "at": 9, "acc": True}]},
    {"type": "question", "at": 10, "text": "Còn một nhân chứng nữa."},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "NGƯỜI CHẤM THI"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "HAI NHÀ KINH TẾ LẬT LẠI HỒ SƠ", "date": "1990"},
    {"type": "ledger", "at": 2, "title": "NGƯỜI PHỤ TRÁCH THỬ NGHIỆM", "srcnote": "LIEBOWITZ & MARGOLIS · 1990",
     "rows": [{"k": "CHỨC VỤ", "v": "THIẾU TÁ HẢI QUÂN", "at": [2, "là"]}], "total": {"k": "TÊN", "v": "AUGUST DVORAK", "at": [3, "August"]}},
    {"type": "slam", "at": 4, "text": "NGƯỜI CHẤM = NGƯỜI DỰ THI", "sub": "VÀ AI ĐƯỢC LUYỆN LẠI THÌ CŨNG GÕ NHANH LÊN", "subAt": 5},
    {"type": "timeline", "at": 6, "items": [{"year": "1956", "text": "thử nghiệm khác: *không thấy Dvorak hơn*", "at": 6},
                                           {"year": "phía Dvorak", "text": "cho rằng thử nghiệm ấy *thiên vị*", "at": 8},
                                           {"year": "hai nhà kinh tế", "text": "*không nói* QWERTY tốt hơn", "at": 9}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "HỌ CHỈ NÓI", "at": 10, "sm": True}, {"text": "CHƯA CÓ BẰNG CHỨNG NÓ KÉM", "at": [10, "chưa"], "acc": True}]},
    {"type": "broll", "at": 11, "vid": "6101367", "veil": 0.5, "illus": VM,
     "kin": [{"text": "PHÁN QUYẾT 3", "at": 11, "sm": True}, {"text": "CHƯA ĐỦ CHỨNG CỨ", "at": [11, "chưa"], "acc": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "TỐT HƠN MỘT CHÚT?", "at": 13, "sm": True},
                                           {"text": "CHƯA ĐÁNG ĐỂ CẢ THẾ GIỚI HỌC LẠI", "at": [13, "đáng"], "acc": True}]},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "VÌ SAO KHÔNG AI ĐỔI ĐƯỢC"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "MỘT BÀI BÁO NGẮN CỦA NHÀ KINH TẾ PAUL DAVID", "date": "1985"},
    {"type": "slam", "at": 1, "text": "PHỤ THUỘC VÀO LỐI MÒN", "sub": "MỘT LỰA CHỌN NHỎ TỪ SỚM · KHOÁ CHẶT CẢ TƯƠNG LAI", "subAt": 2},
    {"type": "ledger", "at": 3, "title": "ĐỔI BÀN PHÍM: KHÔNG CHỈ MÌNH BẠN", "rows": [{"k": "BẠN ĐỔI", "v": "MÁY Ở CHỖ LÀM VẪN THẾ", "at": [4, "máy"]},
                                                                                   {"k": "", "v": "MÁY CỦA BẠN BÈ VẪN THẾ", "at": [4, "Máy"]}],
     "total": {"k": "CÙNG ĐỔI", "v": "KHÔNG AI TỔ CHỨC NỔI", "at": 5}},
    {"type": "keyboard", "at": 6, "layout": "qwerty", "hl": "QWAZ", "hlAt": [7, "AZERTY."], "hlGap": 0.2,
     "label": {"k": "PHÁP: AZERTY ĐỔI CHỖ MẤY PHÍM NÀY", "v": MOCK + " · VẼ TRÊN NỀN QWERTY", "at": 7}},
    {"type": "ledger", "at": 8, "title": "NƯỚC PHÁP · 2019", "srcnote": "AFNOR · TIÊU CHUẨN NF Z71-300, 04.2019",
     "rows": [{"k": "PHÀN NÀN", "v": "KHÓ GÕ CHỮ HOA CÓ DẤU", "at": [8, "Muốn"]}, {"k": "TIÊU CHUẨN MỚI", "v": "CHỈ LÀ TỰ NGUYỆN", "at": 10}],
     "total": {"k": "CHỮ CÁI", "v": "VẪN NẰM NGUYÊN CHỖ CŨ", "at": [11, "các"]}},
    {"type": "broll", "at": 12, "vid": "6963836", "ms": 8, "veil": 0.5, "illus": VM,
     "kin": [{"text": "BÀN PHÍM CHO HAI NGÓN CÁI", "at": [13, "một", 1], "acc": True}, {"text": "thiết kế lại từ đầu · 2013", "at": 13, "sm": True}]},
    {"type": "counter", "at": 14, "from": 0, "to": 34, "prefix": "+", "suffix": "%", "until": [14, "ba."], "label": "TỐC ĐỘ GÕ SAU KHI LUYỆN TẬP · THỬ NGHIỆM CỦA NHÓM",
     "sub": {"text": "ĐH ST ANDREWS · VIỆN MAX PLANCK, 2013", "at": 14}},
    {"type": "question", "at": 15, "text": "Hơn mười năm sau,\nbạn đã thấy ai dùng nó chưa?"},
    {"type": "kinetic", "at": 16, "items": [{"text": "THỨ GIỮ QWERTY Ở LẠI", "at": 17, "sm": True}, {"text": "KHÔNG CÒN LÀ CHIẾC MÁY", "at": [17, "không"]},
                                           {"text": "HÀNG TỶ ĐÔI TAY ĐÃ QUEN", "at": 18, "acc": True}]},
]}

CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "THỨ NẰM DƯỚI NGÓN TAY BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "THỨ NẰM DƯỚI\nNGÓN TAY BẠN", "sub": "MÁY ĐÁNH CHỮ BIẾN MẤT · BÀN PHÍM Ở LẠI", "vid": "6980925", "ms": 8, "illus": VM,
     "titleAt": [0, "Máy"]},
    {"type": "timeline", "at": 3, "items": [{"year": "1870s", "text": "*máy đánh chữ*", "at": 3}, {"year": "sau đó", "text": "*máy điện báo* · *máy tính*", "at": [3, "sang"]},
                                           {"year": "hôm nay", "text": "*màn hình cảm ứng* · không còn phím thật", "at": 4}]},
    {"type": "broll", "at": 5, "vid": "6963836", "veil": 0.5, "illus": VM,
     "kin": [{"text": "NGƯỜI VIỆT CÒN MỘT LỚP CHUYỆN NỮA", "at": 5, "sm": True}, {"text": "KIỂU GÕ TELEX", "at": [6, "Telex,"], "acc": True}]},
    {"type": "ledger", "at": 6, "title": "TELEX", "srcnote": "GỐC TỪ THỜI ĐIỆN TÍN · KHOẢNG 100 NĂM TRƯỚC",
     "rows": [{"k": "A + A", "v": "→ Â", "at": [6, "gõ"]}, {"k": "THÊM S", "v": "→ DẤU SẮC", "at": [6, "thêm"]}],
     "total": {"k": "VÌ", "v": "MÁY CHỈ BIẾT CHỮ KHÔNG DẤU", "at": [7, "khi"]}},
    {"type": "ledger", "at": 8, "title": "MỖI TIN NHẮN: HAI PHÁT MINH THỜI ĐIỆN TÍN",
     "rows": [{"k": "1", "v": "HÀNG PHÍM · MỸ, 1870s", "at": 9}, {"k": "2", "v": "CÁCH BỎ DẤU · VIỆT NAM", "at": 10}]},
    {"type": "ledger", "at": 11, "title": "BA PHÁN QUYẾT", "rows": [{"k": "1", "v": "VÔ TỘI", "at": [11, "Một"]}, {"k": "2", "v": "CÓ TỘI MỘT PHẦN", "at": [11, "một", 1]},
                                                                  {"k": "3", "v": "CHƯA ĐỦ CHỨNG CỨ", "at": [11, "một", 2]}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "KHÔNG PHẢI TỐT NHẤT", "at": 12}, {"text": "CHỈ LÀ CÓ MẶT ĐÚNG LÚC", "at": 13, "acc": True}]},
    {"type": "question", "at": 14, "text": "Bạn gõ mười ngón,\nhay vẫn mổ cò bằng hai ngón?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 15}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [15, "ở"], "acc": True}]},
]}

SPEC = {
    "title": "Vì Sao Bàn Phím Không Xếp Theo A B C? Ba Lời Buộc Tội Với QWERTY",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["qwerty", "chậm", "tội", "phím", "thắng", "dvorak", "telex"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(9)],
    "youtube": {
        "titles": ["Vì Sao Bàn Phím Không Xếp Theo A B C? Ba Lời Buộc Tội Với QWERTY",
                   "Bàn Phím QWERTY Có Thật Được Thiết Kế Để Bạn Gõ Chậm Lại?",
                   "150 Năm Trước, Một Chiếc Máy Đánh Chữ Đã Quyết Định Bạn Gõ Phím Thế Nào Hôm Nay"],
        "summary": "Hàng phím Q-W-E-R-T-Y dưới tay bạn có ba lời buộc tội: sinh ra để làm bạn gõ chậm, thắng không phải vì tốt, và vùi dập một bàn "
                   "phím tốt hơn. Video xét từng lời bằng tư liệu: chiếc máy đánh chữ của Sholes, hãng súng Remington, cuộc thi gõ máy năm 1888, "
                   "thử nghiệm Dvorak của Hải quân Mỹ, và kiểu gõ Telex của người Việt.",
        "more": ["Vì sao từng phím nằm đúng chỗ ấy thì giới sử học chưa thống nhất: video nêu cả cách giải thích chống kẹt cần chữ lẫn nghiên cứu của "
                 "Đại học Kyoto (2011) về điện tín viên. Tranh cãi QWERTY–Dvorak cũng chưa ngã ngũ; video nêu cả hai phía và không kết luận bố cục nào "
                 "tốt nhất. Chuyện dời chữ R để gõ \"TYPEWRITER\" trên một hàng là lời kể được nhiều tư liệu ghi lại. Bàn phím trong video do kênh tự "
                 "vẽ; bố cục Dvorak chỉ vẽ các phím chữ. Gốc điện tín của kiểu gõ Telex ghi theo Wikipedia."],
        "chapter_titles": {"ch00": "Mở đầu: vì sao không phải A B C", "ch01": "Chiếc máy của ông chủ nhà in",
                           "ch02": "Lời buộc tội 1: làm bạn gõ chậm", "ch03": "Hãng súng Remington và chữ TYPEWRITER",
                           "ch04": "Lời buộc tội 2: thắng không phải vì tốt (cuộc thi 1888)", "ch05": "Lời buộc tội 3: bàn phím Dvorak",
                           "ch06": "Người chấm thi", "ch07": "Vì sao không ai đổi được: lối mòn, AZERTY, bàn phím hai ngón cái", "ch08": "Thứ nằm dưới ngón tay bạn: QWERTY và Telex"},
        "sources": [
            "https://en.wikipedia.org/wiki/QWERTY",
            "https://en.wikipedia.org/wiki/Sholes_and_Glidden_typewriter",
            "https://repository.kulib.kyoto-u.ac.jp/dspace/handle/2433/139379",
            "https://en.wikipedia.org/wiki/Frank_Edward_McGurrin",
            "https://papers.ssrn.com/abstract=1069950",
            "https://en.wikipedia.org/wiki/Dvorak_keyboard_layout",
            "https://en.wikipedia.org/wiki/Telex_(input_method)",
            "https://www.afnor.org/en/news/electrotechnologies/french-keyboard-voluntary-standard/",
            "https://news.st-andrews.ac.uk/archive/thumbs-up-for-faster-texting/",
        ],
        "hashtags": ["QWERTY", "BànPhím", "CôngNghệ", "CôngNghệQuanhTa", "MindInTheMachine"],
        "tags": ["bàn phím qwerty", "vì sao bàn phím không xếp theo abc", "lịch sử bàn phím", "máy đánh chữ", "dvorak", "kiểu gõ telex",
                 "gõ mười ngón", "công nghệ quanh ta", "lịch sử công nghệ", "qwerty"],
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
