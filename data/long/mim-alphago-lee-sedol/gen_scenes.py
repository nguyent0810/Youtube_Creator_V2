"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #12 "AlphaGo đấu Lee Sedol" (loại 20-30 phút đầu tiên của kênh).

    python data/long/mim-alphago-lee-sedol/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Cảnh "go" (lab.js) là BÀN CỜ MINH HOẠ, quân đặt ngẫu nhiên, KHÔNG phải thế cờ thật của trận đấu:
mọi cảnh go đều ghi rõ điều đó. Clip: Pexels (ngang), gắn "VIDEO MINH HỌA", không phải hình ảnh của trận đấu. Bảng tỉ số = cảnh slam lặp lại.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

D = Path(__file__).resolve().parent
SAY = {"seoul": "Xơ-un", "lee": "Li", "sedol": "Xê-đôn", "alphago": "An-pha Gô", "=AlphaGo": "An-pha Gô", "deep": "Đíp", "blue": "Blu", "ibm": "ai bi em",
       "garry": "Ga-ri", "kasparov": "Cát-xpa-rốp", "bigeum": "Bi-gưm", "london": "Luân Đôn", "deepmind": "Đíp-mai", "google": "Gu-gồ",
       "fan": "Phan", "hui": "Huy", "nature": "Nây-chờ", "four": "Pho", "seasons": "Xi-dần", "aja": "A-gia", "huang": "Hoàng",
       "michael": "Mai-cồ", "redmond": "Rét-mần", "wired": "Oai-ợt", "demis": "Đe-mít", "hassabis": "Ha-xa-bít", "won": "uôn", "master": "Mát-xtơ",
       "zero": "Di-rô", "alphazero": "An-pha Di-rô", "alphafold": "An-pha Phôn", "nobel": "Nô-ben", "protein": "prô-tê-in", "kellin": "Ke-lin",
       "pelrine": "Peo-rin", "=AI": "ây ai", "=Go": "Gô"}
VM = "VIDEO MINH HỌA · KHÔNG PHẢI HÌNH ẢNH TRẬN ĐẤU"
MOCK = "BÀN CỜ MINH HOẠ · KHÔNG PHẢI THẾ CỜ THẬT"
REAL = "THẾ CỜ THẬT · DỰNG TỪ BIÊN BẢN VÁN ĐẤU"
import goban  # noqa: E402  (cùng thư mục)


def real(game, upto, hit=None, **kw):
    """Cảnh go với thế cờ thật của ván `game` sau `upto` nước. hit = số nước được nhấn (mặc định: không nhấn); nước nhấn không vẽ sẵn."""
    pos = goban.position(game, upto)
    sc = {"type": "go", "pos": pos, **kw}
    if hit:
        h = goban.move(game, hit)
        sc["pos"] = [q for q in pos if q[:2] != h[:2]]
        assert len(sc["pos"]) == len(pos) - 1, "quân của nước nhấn đã bị bắt"
        sc.update(hit=h, move=str(hit))
    return sc
DM = "THEO DEEPMIND"
CH = {}


def score(at, lee, ai, sub="LEE SEDOL – ALPHAGO", **kw):
    return {"type": "slam", "at": at, "text": f"{lee} – {ai}", "sub": sub, **kw}


CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "NƯỚC THỨ BA MƯƠI BẢY"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "day": "SEOUL · HÀN QUỐC", "date": "10.03.2016"},
    {"type": "broll", "at": 1, "vid": "39277761", "veil": 0.45, "illus": VM,
     "kin": [{"text": "MỘT BÀN CỜ VÂY", "at": [1, "một"], "acc": True}, {"text": "một bên: Lee Sedol", "at": 2, "sm": True},
             {"text": "bên kia: một cái màn hình", "at": [3, "đặt"], "sm": True}]},
    real(2, 37, hit=37, at=4, hitAt=[5, "đặt"], label={"k": "VÁN 2 · NƯỚC THỨ 37", "v": REAL, "at": 4}),
    {"type": "kinetic", "at": 6, "items": [{"text": "KỲ THỦ 9 ĐẲNG KHỰNG LẠI", "at": [6, "khựng"]}, {"text": "“ĐẶT NHẦM QUÂN?”", "at": 7, "acc": True}]},
    {"type": "counter", "at": 8, "from": 1, "to": 10000, "prefix": "1 / ", "until": [9, "vạn"], "label": "XÁC SUẤT MỘT CON NGƯỜI CHỌN NƯỚC NÀY",
     "sub": {"text": "ƯỚC TÍNH CỦA CHÍNH CỖ MÁY · " + DM, "at": 9}},
    {"type": "broll", "at": 10, "vid": "34504411", "veil": 0.5, "illus": VM,
     "kin": [{"text": "LEE SEDOL ĐỨNG DẬY", "at": [10, "Rồi"], "acc": True}, {"text": "và đi ra khỏi phòng", "at": [10, "và"], "sm": True}]},
    {"type": "ledger", "at": 11, "title": "NĂM VÁN CỜ", "rows": [{"k": "BAO LÂU", "v": "BẢY NGÀY", "at": [12, "bảy"]}, {"k": "AI ĐẤU", "v": "MỘT NGƯỜI · MỘT CỖ MÁY", "at": [12, "giữa"]},
                                                               {"k": "THEO DÕI", "v": "BẰNG MỘT BẢNG TỈ SỐ", "at": 13}],
     "total": {"k": "CÓ HAI NƯỚC", "v": "MỘT PHẦN VẠN", "at": 14}},
    {"type": "kinetic", "at": 15, "items": [{"text": "MỘT NƯỚC CỦA MÁY", "at": 15}, {"text": "MỘT NƯỚC CỦA NGƯỜI", "at": [15, "Và"], "acc": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "VÌ SAO LẠI LÀ CỜ VÂY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "VÌ SAO LẠI LÀ\nCỜ VÂY", "sub": "LÙI LẠI GẦN HAI MƯƠI NĂM", "vid": "855386", "illus": VM, "titleAt": [0, "Để"]},
    {"type": "timeline", "at": 1, "items": [{"year": "1997", "text": "*Deep Blue* thắng nhà vô địch cờ vua", "at": 1},
                                           {"year": "nhiều người nghĩ", "text": "*thế là xong*", "at": 2},
                                           {"year": "nhưng", "text": "còn *cờ vây*", "at": 3}]},
    {"type": "go", "at": 4, "stones": 30, "label": {"k": "19 × 19 ĐƯỜNG · VÂY NHIỀU ĐẤT HƠN THÌ THẮNG", "v": MOCK, "at": 5}},
    {"type": "bars", "at": 7, "title": "SỐ NƯỚC CÓ THỂ CHỌN MỖI LƯỢT · ƯỚC LƯỢNG", "unit": "",
     "items": [{"k": "CỜ VUA", "v": 35, "lbl": "VÀI CHỤC", "at": 8}, {"k": "CỜ VÂY", "v": 250, "lbl": "VÀI TRĂM", "at": 9, "acc": True}],
     "label": {"k": "CÁI KHÓ NẰM Ở SỐ KHẢ NĂNG", "v": "CON SỐ MINH HOẠ CHO HAI MỨC ĐỘ", "at": 7}},
    {"type": "counter", "at": 10, "from": 1, "to": 171, "suffix": " CHỮ SỐ", "until": [10, "mốt"], "label": "ĐỘ DÀI CỦA CON SỐ ĐẾM THẾ CỜ HỢP LỆ",
     "sub": {"text": "NHIỀU HƠN SỐ NGUYÊN TỬ TRONG VŨ TRỤ QUAN SÁT ĐƯỢC", "at": 11}},
    {"type": "kinetic", "at": 12, "items": [{"text": "DEEP BLUE: TÍNH THẬT NHIỀU NƯỚC", "at": 12, "sm": True}, {"text": "VỚI CỜ VÂY: VÔ DỤNG", "at": 13, "acc": True}]},
    {"type": "ledger", "at": 14, "title": "CÁI KHÓ THỨ HAI", "rows": [{"k": "CỜ VUA", "v": "ĐẾM QUÂN LÀ BIẾT AI HƠN", "at": 15},
                                                                    {"k": "CỜ VÂY", "v": "MỌI QUÂN GIỐNG HỆT NHAU", "at": 16}],
     "total": {"k": "NÊN", "v": "KHÓ BIẾT AI ĐANG THẮNG", "at": 18}},
    {"type": "broll", "at": 19, "vid": "39277761", "veil": 0.5, "illus": VM,
     "kin": [{"text": "GẦN 20 NĂM SAU DEEP BLUE", "at": 19, "sm": True}, {"text": "MÁY VẪN CHỈ NGANG NGHIỆP DƯ", "at": [19, "vẫn"], "acc": True},
             {"text": "“cảm giác về hình cờ”", "at": [20, "Cảm"], "sm": True}]},
    {"type": "counter", "at": 21, "from": 0, "to": 10, "prefix": "≥ ", "suffix": " NĂM NỮA", "until": [21, "năm"], "label": "DỰ ĐOÁN CỦA GIỚI CHUYÊN GIA TRƯỚC NĂM 2016"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "CẬU BÉ TỪ HÒN ĐẢO"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "CẬU BÉ TỪ\nHÒN ĐẢO", "sub": "LEE SEDOL", "vid": "6034203", "illus": VM, "titleAt": [0, "Lee"]},
    {"type": "timeline", "at": 1, "items": [{"year": "1983", "text": "sinh ra · lớn lên trên đảo *Bigeum*", "at": 1},
                                           {"year": "12 tuổi", "text": "thành *kỳ thủ chuyên nghiệp*", "at": 2},
                                           {"year": "2016", "text": "*18 danh hiệu* quốc tế", "at": 3}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "LỐI ĐÁNH TÁO BẠO", "at": 4, "acc": True}, {"text": "tìm ra nước không ai nghĩ tới", "at": [4, "hay"], "sm": True},
                                          {"text": "đủ sức làm cỗ máy bối rối", "at": 5, "sm": True}]},
    {"type": "broll", "at": 6, "vid": "37448949", "veil": 0.5, "illus": VM,
     "kin": [{"text": "Ở HÀN QUỐC", "at": 6, "sm": True}, {"text": "CỜ VÂY CÓ KÊNH TRUYỀN HÌNH RIÊNG", "at": 7, "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "NHƯ MỘT TRẬN CHUNG KẾT", "at": [8, "giống"], "acc": True}, {"text": "mà cả nước cùng xem", "at": [8, "mà"], "sm": True}]},
    {"type": "ledger", "at": 9, "title": "TRƯỚC TRẬN", "rows": [{"k": "LEE SEDOL", "v": "ĐOÁN MÌNH THẮNG ÁP ĐẢO", "at": 10},
                                                              {"k": "NHIỀU CHUYÊN GIA", "v": "CŨNG NGHĨ THẾ", "at": 12}]},
    {"type": "ledger", "at": 13, "title": "THỂ THỨC", "rows": [{"k": "GIẢI THƯỞNG", "v": "1 TRIỆU ĐÔ LA", "at": 13}, {"k": "SỐ VÁN", "v": "NĂM VÁN", "at": 14},
                                                             {"k": "THỜI GIAN", "v": "MỖI BÊN 2 GIỜ MỖI VÁN", "at": [14, "Mỗi"]}]},
    {"type": "counter", "at": 15, "from": 0, "to": 200, "prefix": "> ", "suffix": " TRIỆU", "until": [15, "triệu"], "label": "NGƯỜI THEO DÕI TRẬN ĐẤU",
     "sub": {"text": DM, "at": [15, "theo"]}},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CỖ MÁY HỌC TỪ 30 TRIỆU NƯỚC CỜ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CỖ MÁY HỌC TỪ\n30 TRIỆU NƯỚC CỜ", "sub": "LONDON · DEEPMIND", "vid": "855761", "illus": VM, "titleAt": [0, "Đối"]},
    {"type": "question", "at": 1, "text": "Một mạng nơ-ron\nchơi cờ vây tới mức nào?", "showAt": 2},
    {"type": "ledger", "at": 3, "title": "KHÁC HẲN DEEP BLUE", "rows": [{"k": "KHÔNG DẠY", "v": "LUẬT ĐÁNH, MẸO ĐÁNH", "at": 4}],
     "total": {"k": "CHỈ CHO XEM", "v": "~30 TRIỆU NƯỚC CỜ", "at": [5, "ba"]}},
    {"type": "kinetic", "at": 6, "items": [{"text": "NHIỆM VỤ: ĐOÁN", "at": 6, "acc": True}, {"text": "người chơi giỏi sẽ đi nước nào?", "at": [6, "một"], "sm": True}]},
    {"type": "go", "at": 7, "stones": 60, "label": {"k": "TỰ CHƠI VỚI CHÍNH MÌNH · THẮNG THÌ NHỚ, THUA THÌ SỬA", "v": MOCK, "at": 7}},
    {"type": "nn", "at": 9, "fwdAt": [10, "gợi"], "label": {"k": "HAI BỘ NÃO NHỎ", "v": "SƠ ĐỒ MINH HOẠ", "at": 9}},
    {"type": "ledger", "at": 10, "title": "HAI BỘ NÃO NHỎ", "rows": [{"k": "BỘ THỨ NHẤT", "v": "GỢI Ý NƯỚC ĐÁNG XEM", "at": 10},
                                                                   {"k": "BỘ THỨ HAI", "v": "ƯỚC LƯỢNG AI ĐANG THẮNG", "at": 11}],
     "total": {"k": "NHỜ THẾ", "v": "CHỈ ĐÀO SÂU VÀI HƯỚNG", "at": 12}},
    {"type": "kinetic", "at": 14, "items": [{"text": "MỘT CHI TIẾT NÊN NHỚ", "at": 14, "sm": True}, {"text": "KHÔNG CỐ THẮNG ĐẬM", "at": 15, "acc": True},
                                           {"text": "chỉ cố cho khả năng thắng cao nhất", "at": 16, "sm": True}]},
    {"type": "date", "at": 18, "day": "ĐẤU THỬ VỚI FAN HUI · VÔ ĐỊCH CHÂU ÂU", "date": "10.2015"},
    score(19, 0, 5, "FAN HUI – ALPHAGO"),
    {"type": "kinetic", "at": 20, "items": [{"text": "LẦN ĐẦU TIÊN", "at": 20, "sm": True}, {"text": "MÁY THẮNG MỘT KỲ THỦ CHUYÊN NGHIỆP", "at": [20, "một"], "acc": True},
                                           {"text": "công bố trên tạp chí Nature · 01.2016", "at": 21, "sm": True}]},
    {"type": "question", "at": 22, "text": "Còn Fan Hui thì sao?"},
    {"type": "bars", "at": 23, "title": "THỨ HẠNG THẾ GIỚI CỦA FAN HUI · SỐ NHỎ HƠN LÀ CAO HƠN", "unit": "",
     "items": [{"k": "TRƯỚC KHI GẶP MÁY", "v": 633, "lbl": "~633", "at": [26, "sáu"]}, {"k": "VÀI THÁNG SAU", "v": 300, "lbl": "~300", "at": [26, "vọt"], "acc": True}],
     "label": {"k": "THUA NĂM VÁN · RỒI ĐÁNH HAY LÊN", "v": "THEO TƯ LIỆU VỀ TRẬN ĐẤU · WIRED", "at": 25}},
    {"type": "kinetic", "at": 27, "items": [{"text": "HÃY NHỚ CHI TIẾT NÀY", "at": 27, "acc": True}, {"text": "nó sẽ quay lại ở cuối video", "at": [27, "Nó"], "sm": True}]},
    {"type": "bars", "at": 28, "title": "ĐẲNG CẤP CHUYÊN NGHIỆP", "unit": "",
     "items": [{"k": "FAN HUI", "v": 2, "lbl": "2 ĐẲNG", "at": 28}, {"k": "LEE SEDOL", "v": 9, "lbl": "9 ĐẲNG", "at": 29, "acc": True}],
     "label": {"k": "9 ĐẲNG LÀ BẬC CAO NHẤT", "v": "", "at": 29}},
    {"type": "kinetic", "at": 31, "items": [{"text": "GẦN NHƯ AI CŨNG TIN", "at": 31, "sm": True}, {"text": "LẦN NÀY MÁY SẼ THUA", "at": [31, "lần"], "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "VÁN MỘT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "VÁN MỘT · KHÁCH SẠN FOUR SEASONS, SEOUL", "date": "09.03.2016"},
    {"type": "kinetic", "at": 1, "items": [{"text": "13 GIỜ · VÁN THỨ NHẤT", "at": 1, "sm": True}, {"text": "LEE SEDOL CẦM ĐEN, ĐI TRƯỚC", "at": 2, "acc": True}]},
    {"type": "ledger", "at": 3, "title": "NGƯỜI NGỒI ĐỐI DIỆN", "rows": [{"k": "TÊN", "v": "AJA HUANG", "at": 4}, {"k": "LÀ", "v": "KỸ SƯ CỦA DEEPMIND", "at": [4, "một"]}],
     "total": {"k": "VIỆC", "v": "ĐẶT QUÂN THAY CHO MÁY", "at": 5}},
    real(1, 7, hit=7, at=6, hitAt=[6, "một"], label={"k": "VÁN 1 · LEE THỬ MỘT NƯỚC ÍT GẶP", "v": REAL, "at": 7}),
    {"type": "kinetic", "at": 9, "items": [{"text": "BÌNH LUẬN VIÊN ĐỔI GIỌNG", "at": 9, "sm": True}, {"text": "CHƠI NHƯ MỘT KỲ THỦ HÀNG ĐẦU", "at": [9, "Cỗ"], "acc": True}]},
    real(1, 102, hit=102, at=10, hitAt=[11, "một"], label={"k": "VÁN 1 · NƯỚC 102 CỦA MÁY · LEE NGHĨ HƠN 10 PHÚT", "v": REAL, "at": 12}),
    {"type": "broll", "at": 14, "vid": "33972359", "veil": 0.5, "illus": VM,
     "kin": [{"text": "20 PHÚT CUỐI", "at": 15, "acc": True}, {"text": "AlphaGo vượt lên", "at": [15, "AlphaGo"], "sm": True},
             {"text": "nước 186: Lee Sedol xin thua", "at": 16, "sm": True}]},
    score(17, 0, 1),
    {"type": "ledger", "at": 18, "title": "HỌP BÁO SAU VÁN MỘT", "rows": [{"k": "LEE SEDOL", "v": "SAI LẦM QUAN TRỌNG TỪ SỚM", "at": 18},
                                                                        {"k": "VẪN TIN", "v": "THẮNG CÁC VÁN CÒN LẠI", "at": 19}]},
    {"type": "question", "at": 20, "text": "Con người\ncó thắng nổi không?", "showAt": 22},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "VÁN HAI: NƯỚC 37"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "VÁN HAI · ALPHAGO CẦM ĐEN", "date": "10.03.2016"},
    {"type": "kinetic", "at": 2, "items": [{"text": "LEE SEDOL CHƠI CHẬM HƠN, CHẮC HƠN", "at": 2, "sm": True}, {"text": "QUAY LẠI KHOẢNH KHẮC Ở ĐẦU VIDEO", "at": 3, "acc": True}]},
    real(2, 37, hit=37, at=4, hitAt=[5, "đặt"], prob="đường thứ năm", label={"k": "VÁN 2 · NƯỚC 37 · ÉP VAI Ở ĐƯỜNG THỨ NĂM", "v": REAL, "at": 5}),
    {"type": "ledger", "at": 6, "title": "VỚI NGƯỜI HỌC CỜ VÂY", "srcnote": "LỜI BÌNH: MICHAEL REDMOND, 9 ĐẲNG",
     "rows": [{"k": "SÁCH DẠY", "v": "ĐƯỜNG NĂM: NHƯỜNG NHIỀU ĐẤT", "at": 7}, {"k": "REDMOND", "v": "“SÁNG TẠO, ĐỘC NHẤT”", "at": [8, "gọi"]}],
     "total": {"k": "DÂN CHUYÊN", "v": "ÍT AI NGHĨ TỚI NƯỚC NÀY", "at": 9}},
    {"type": "counter", "at": 10, "from": 1, "to": 10000, "prefix": "1 / ", "until": [11, "nghìn."], "label": "XÁC SUẤT MỘT CON NGƯỜI ĐI NƯỚC NÀY",
     "sub": {"text": "ƯỚC TÍNH BÊN TRONG ALPHAGO · " + DM, "at": 11}},
    {"type": "kinetic", "at": 12, "items": [{"text": "NÓ BIẾT CON NGƯỜI SẼ KHÔNG ĐÁNH THẾ", "at": 12, "sm": True}, {"text": "VÀ NÓ VẪN ĐÁNH", "at": 13, "acc": True}]},
    {"type": "broll", "at": 14, "vid": "34504411", "ms": 5, "veil": 0.5, "illus": VM,
     "kin": [{"text": "LEE SEDOL RỜI BÀN CỜ", "at": 14, "acc": True}, {"text": "quay lại · suy nghĩ rất lâu", "at": 15, "sm": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "FAN HUI · THEO TẠP CHÍ WIRED", "at": 16, "sm": True}, {"text": "lúc đầu: thật kỳ quặc", "at": 17, "sm": True}]},
    {"type": "quote", "at": 18, "text": "Đẹp quá.", "who": "FAN HUI", "note": "TRÍCH DỊCH · THEO WIRED, 03.2016"},
    real(2, 150, hit=37, at=20, hitAt=[20, "quân"], prob="sau hơn 100 nước", label={"k": "VÁN 2 · SAU NƯỚC 150: QUÂN ẤY NỐI CÁC ĐÁM QUÂN ĐEN", "v": REAL, "at": 20}),
    {"type": "kinetic", "at": 22, "items": [{"text": "CUỐI VÁN: MỘT CHUYỆN LẠ NỮA", "at": 22, "sm": True}, {"text": "MÁY ĐI NHỮNG NƯỚC LỎNG TAY", "at": 23, "acc": True}]},
    {"type": "bars", "at": 24, "title": "ALPHAGO CHỌN CÁCH THẮNG NÀO?", "unit": "",
     "items": [{"k": "99% THẮNG · CÁCH BIỆT 1,5 ĐIỂM", "v": 99, "lbl": "CHỌN", "at": [26, "chín"], "acc": True},
               {"k": "80% THẮNG · CÁCH BIỆT 20 ĐIỂM", "v": 80, "lbl": "BỎ", "at": [26, "tám"]}],
     "label": {"k": "KHÔNG CỐ THẮNG ĐẬM", "v": "VÍ DỤ CỦA NHÓM LÀM RA ALPHAGO", "at": 25}},
    {"type": "kinetic", "at": 27, "items": [{"text": "LỜI TUYÊN BỐ: VÁN CỜ ĐÃ XONG", "at": 27, "acc": True},
                                           {"text": "máy tự tin thắng từ giữa ván", "at": 28, "sm": True}, {"text": "bình luận viên còn chưa biết ai hơn", "at": 29, "sm": True}]},
    score(30, 0, 2, "NƯỚC 211: LEE SEDOL XIN THUA", subAt=31),
    {"type": "quote", "at": 32, "text": "Hôm nay, AlphaGo đã chơi một ván gần như hoàn hảo.", "who": "LEE SEDOL", "note": "TRÍCH DỊCH · HỌP BÁO 10.03.2016"},
    {"type": "ledger", "at": 34, "title": "NƯỚC 37 TRẢ LỜI CÂU HỎI LỚN NHẤT", "rows": [{"k": "KHÔNG CHỈ", "v": "BẮT CHƯỚC 30 TRIỆU NƯỚC", "at": 35}],
     "total": {"k": "MÀ CÒN", "v": "ĐI NƯỚC GẦN NHƯ CHƯA AI ĐI", "at": 36}},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "VÁN BA: BẤT LỰC"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "VÁN BA · THUA LÀ THUA CẢ TRẬN", "date": "12.03.2016"},
    {"type": "kinetic", "at": 2, "items": [{"text": "CẦM ĐEN · TẤN CÔNG NGAY TỪ ĐẦU", "at": 2, "acc": True}, {"text": "kéo máy vào đánh giáp lá cà", "at": 3, "sm": True}]},
    real(3, 100, at=4, label={"k": "VÁN 3 · SAU 100 NƯỚC: MÁY ĐỠ TỪNG ĐÒN RỒI PHẢN CÔNG", "v": REAL, "at": 4}),
    {"type": "ledger", "at": 6, "title": "TÌNH HUỐNG “CƯỚP”", "rows": [{"k": "LÀ GÌ", "v": "GIÀNH ĐI GIÀNH LẠI MỘT ĐIỂM", "at": 6},
                                                                     {"k": "NHIỀU NGƯỜI NGHĨ", "v": "MÁY SẼ RỐI", "at": 7}],
     "total": {"k": "THỰC TẾ", "v": "NÓ KHÔNG RỐI", "at": 8}},
    {"type": "kinetic", "at": 9, "items": [{"text": "ĐANG GIÀNH GIẬT", "at": 9, "sm": True}, {"text": "MÁY BỎ ĐI ĐÁNH CHỖ KHÁC", "at": [9, "AlphaGo"], "acc": True},
                                          {"text": "dấu hiệu của sự tự tin tuyệt đối", "at": 10, "sm": True}]},
    score(11, 0, 3, "NƯỚC 176: LEE SEDOL XIN THUA · TRẬN ĐẤU NGÃ NGŨ", subAt=12),
    {"type": "kinetic", "at": 13, "items": [{"text": "GIỚI BÌNH LUẬN VIẾT", "at": 13, "sm": True}, {"text": "MẠNH HƠN MỌI KỲ THỦ TỪNG BIẾT", "at": [13, "mạnh"], "acc": True},
                                           {"text": "1 triệu đô · đem làm từ thiện", "at": 14, "sm": True}]},
    {"type": "broll", "at": 15, "vid": "33191999", "veil": 0.55, "illus": VM, "kin": [{"text": "HỌP BÁO · LEE SEDOL CÚI ĐẦU", "at": 15, "acc": True}]},
    {"type": "quote", "at": 16, "text": "Tôi đã đánh giá sai khả năng của AlphaGo, và tôi cảm thấy bất lực.", "who": "LEE SEDOL", "note": "TRÍCH DỊCH · HỌP BÁO 12.03.2016"},
    {"type": "quote", "at": 18, "text": "Tôi, Lee Sedol, đã thua. Chứ không phải loài người.", "who": "LEE SEDOL", "note": "TRÍCH DỊCH · THE KOREA TIMES, 13.03.2016"},
    {"type": "question", "at": 20, "text": "Một con người có thắng nổi\ncỗ máy này, dù chỉ một ván?", "showAt": 22},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "VÁN BỐN: NƯỚC 78"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "VÁN BỐN · LEE SEDOL CẦM TRẮNG", "date": "13.03.2016"},
    {"type": "ledger", "at": 1, "title": "ĐỔI HẲN CÁCH ĐÁNH", "rows": [{"k": "NHƯỜNG MÁY", "v": "THẬT NHIỀU ĐẤT Ở BIÊN", "at": 2},
                                                                    {"k": "CÒN MÌNH", "v": "CHỜ ĐÁNH VÀO TRUNG TÂM", "at": 3}],
     "total": {"k": "RỦI RO", "v": "SAI MỘT NƯỚC LÀ THUA", "at": 4}},
    real(4, 77, at=5, label={"k": "VÁN 4 · SAU 77 NƯỚC: BỨC TƯỜNG ĐEN Ở TRUNG TÂM", "v": REAL, "at": 8}),
    {"type": "kinetic", "at": 9, "items": [{"text": "BÌNH LUẬN VIÊN NÓI VỀ", "at": 9, "sm": True}, {"text": "MỘT TỈ SỐ 5 – 0", "at": [9, "một"], "acc": True}]},
    real(4, 78, hit=78, at=10, hitAt=[11, "chêm"], prob="chêm giữa hai quân đen", label={"k": "VÁN 4 · NƯỚC 78 CỦA LEE SEDOL", "v": REAL, "at": 11}),
    {"type": "kinetic", "at": 12, "items": [{"text": "KHÔNG AI THẤY TRƯỚC", "at": 12, "sm": True}, {"text": "“NƯỚC CỜ CỦA THẦN”", "at": [13, "nước"], "acc": True},
                                           {"text": "lời kỳ thủ Cổ Lực", "at": [13, "gọi"], "sm": True}]},
    {"type": "counter", "at": 14, "from": 1, "to": 10000, "prefix": "1 / ", "until": [16, "nghìn."], "label": "XÁC SUẤT MỘT CON NGƯỜI ĐI NƯỚC ẤY",
     "sub": {"text": "ƯỚC TÍNH CỦA ALPHAGO · " + DM, "at": 16}},
    {"type": "bars", "at": 17, "title": "ALPHAGO TỰ ƯỚC TÍNH KHẢ NĂNG THẮNG (%)", "unit": "",
     "items": [{"k": "TRƯỚC NƯỚC 79", "v": 70, "lbl": "70", "at": 18, "acc": True}, {"k": "LÚC XIN THUA", "v": 20, "lbl": "< 20", "at": 20}],
     "label": {"k": "VÀI NƯỚC SAU: CON SỐ SỤP ĐỔ", "v": "THEO DEEPMIND VÀ TƯỜNG THUẬT TRẬN ĐẤU", "at": 20}},
    real(4, 101, at=21, label={"k": "VÁN 4 · NƯỚC 87–101: MÁY ĐI NHỮNG NƯỚC RẤT YẾU", "v": REAL, "at": 22}),
    {"type": "ledger", "at": 23, "title": "VÌ SAO MÁY ĐÁNH NHƯ VẬY?", "srcnote": "GIẢI THÍCH CỦA CÁC NHÀ PHÂN TÍCH CỜ VÂY",
     "rows": [{"k": "NÓ CHỈ ĐÀO SÂU", "v": "HƯỚNG NÓ CHO LÀ ĐÁNG XEM", "at": 25}, {"k": "NƯỚC “KHÔNG THỂ”", "v": "NẰM NGOÀI TẦM NHÌN", "at": 26}],
     "total": {"k": "KHI XẢY RA", "v": "MỌI TÍNH TOÁN ĐỀU ĐỔ", "at": 27}},
    {"type": "kinetic", "at": 28, "items": [{"text": "KHÁN PHÒNG XÔN XAO", "at": 28, "sm": True}, {"text": "CỖ MÁY ĐANG CUỐNG", "at": [29, "đang"], "acc": True},
                                           {"text": "dưới 20% thắng: tự xin thua", "at": 31, "sm": True}]},
    {"type": "slam", "at": 32, "text": "ALPHAGO XIN THUA", "sub": "NƯỚC THỨ 180", "subAt": 33},
    {"type": "broll", "at": 34, "vid": "3255107", "veil": 0.5, "illus": VM,
     "kin": [{"text": "PHÒNG HỌP BÁO VỠ OÀ", "at": 34, "acc": True}, {"text": "nhà báo đứng dậy vỗ tay", "at": 35, "sm": True}]},
    score(36, 1, 3),
    {"type": "quote", "at": 38, "text": "Đây là một ván thắng vô giá, tôi sẽ không đổi nó lấy bất cứ thứ gì.", "who": "LEE SEDOL", "note": "TRÍCH DỊCH · HỌP BÁO 13.03.2016"},
    {"type": "ledger", "at": 39, "title": "MỘT PHẦN MƯỜI NGHÌN · HAI LẦN", "rows": [{"k": "NƯỚC 37", "v": "MÁY ĐI NƯỚC NGƯỜI KHÔNG ĐI", "at": 41}],
     "total": {"k": "NƯỚC 78", "v": "NGƯỜI ĐI NƯỚC MÁY KHÔNG TIN", "at": 42}},
]}

CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "VÁN NĂM"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "VÁN CUỐI CÙNG", "date": "15.03.2016"},
    {"type": "ledger", "at": 1, "title": "MỘT ĐỀ NGHỊ LẠ", "rows": [{"k": "THEO THỂ THỨC", "v": "LEE ĐƯỢC CẦM TRẮNG", "at": 1}, {"k": "ÔNG XIN", "v": "ĐỔI SANG QUÂN ĐEN", "at": 2}],
     "total": {"k": "LÝ DO", "v": "THẮNG BẰNG ĐEN MỚI ĐÁNG GIÁ", "at": 5}},
    real(5, 58, at=6, label={"k": "VÁN 5 · SAU 58 NƯỚC: MÁY MẮC SAI LẦM NẶNG, LEE DẪN TRƯỚC", "v": REAL, "at": 7}),
    {"type": "kinetic", "at": 9, "items": [{"text": "MÁY LẶNG LẼ GỠ LẠI", "at": 9, "acc": True}, {"text": "khoảng nước 90: cân bằng", "at": 10, "sm": True},
                                          {"text": "đòn liều cuối cùng: máy đỡ được", "at": 11, "sm": True}]},
    {"type": "counter", "at": 12, "from": 0, "to": 280, "suffix": " NƯỚC", "until": [13, "mươi,"], "label": "VÁN DÀI NHẤT TRONG NĂM VÁN · LEE SEDOL XIN THUA"},
    score(14, 1, 4, "TỈ SỐ CHUNG CUỘC · LEE SEDOL – ALPHAGO"),
    {"type": "ledger", "at": 15, "title": "SAU TIẾNG CÒI", "rows": [{"k": "LEE SEDOL NHẬN", "v": "170.000 ĐÔ LA", "at": 15}, {"k": "ALPHAGO NHẬN", "v": "9 ĐẲNG DANH DỰ", "at": 16}],
     "total": {"k": "HÀN QUỐC", "v": "1.000 TỶ WON CHO AI", "at": 17}},
    {"type": "quote", "at": 19, "text": "Tôi không hẳn nghĩ rằng AlphaGo giỏi hơn tôi. Tôi tin con người vẫn còn làm được nhiều hơn thế.", "who": "LEE SEDOL",
     "note": "TRÍCH DỊCH · AP, 15.03.2016"},
    {"type": "kinetic", "at": 20, "items": [{"text": "MÁY HƠN Ở CHỖ KHÁC", "at": 20, "sm": True}, {"text": "KHÔNG MỆT · KHÔNG RUN", "at": [20, "Nó"], "acc": True}]},
    {"type": "kinetic", "at": 21, "items": [{"text": "CHƯA DỪNG Ở SEOUL", "at": 21}, {"text": "SẮP BỊ CHÍNH HẬU DUỆ HẠ GỤC", "at": [22, "sắp"], "acc": True}]},
]}

CH["ch09"] = {"hud": {"k": "CHƯƠNG 09", "t": "SÁU MƯƠI VÁN THẮNG"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "9", "k": "CHƯƠNG CHÍN", "title": "SÁU MƯƠI\nVÁN THẮNG", "sub": "MỘT TÀI KHOẢN LẠ · CUỐI THÁNG 12.2016", "vid": "6804656", "illus": VM, "titleAt": [0, "Cuối"]},
    {"type": "counter", "at": 2, "from": 0, "to": 60, "suffix": " – 0", "until": [3, "sáu"], "label": "THẮNG LIÊN TIẾP CÁC KỲ THỦ HÀNG ĐẦU · KHOẢNG MỘT TUẦN",
     "sub": {"text": "DEEPMIND XÁC NHẬN: PHIÊN BẢN MỚI, TÊN LÀ MASTER", "at": 5}},
    {"type": "date", "at": 6, "day": "MASTER GẶP KHA KHIẾT · SỐ MỘT THẾ GIỚI", "date": "05.2017"},
    {"type": "ledger", "at": 7, "title": "KHA KHIẾT ĐỔI GIỌNG", "rows": [{"k": "03.2016", "v": "“KHÔNG THẮNG NỔI TÔI”", "at": 7}, {"k": "SAU BA VÁN ĐẦU", "v": "“RẤT CÓ THỂ TÔI THUA”", "at": 8}]},
    score(9, 0, 3, "KHA KHIẾT – ALPHAGO MASTER"),
    {"type": "quote", "at": 11, "text": "Chưa một con người nào chạm tới rìa của chân lý cờ vây.", "who": "KHA KHIẾT", "note": "TRÍCH DỊCH"},
    {"type": "kinetic", "at": 12, "items": [{"text": "ALPHAGO GIẢI NGHỆ", "at": 12, "acc": True}, {"text": "không đấu với con người nữa", "at": 13, "sm": True}]},
    {"type": "question", "at": 14, "text": "Nếu không cho máy xem\nmột ván cờ nào của con người?", "showAt": 16},
]}

CH["ch10"] = {"hud": {"k": "CHƯƠNG 10", "t": "CỖ MÁY KHÔNG CẦN THẦY"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "DEEPMIND CÔNG BỐ ALPHAGO ZERO", "date": "10.2017"},
    {"type": "ledger", "at": 1, "title": "ZERO = SỐ KHÔNG", "rows": [{"k": "KHÔNG", "v": "30 TRIỆU NƯỚC CỜ CỦA NGƯỜI", "at": 3}, {"k": "KHÔNG", "v": "MỘT VÁN ĐẤU MẪU NÀO", "at": 4}],
     "total": {"k": "CHỈ CÓ", "v": "LUẬT CHƠI · VÀ TỰ ĐÁNH", "at": 5}},
    {"type": "go", "at": 6, "stones": 90, "label": {"k": "NHỮNG VÁN ĐẦU: ĐẶT QUÂN HOÀN TOÀN NGẪU NHIÊN", "v": MOCK, "at": 6}},
    {"type": "counter", "at": 8, "from": 0, "to": 4.9, "suffix": " TRIỆU VÁN", "until": [9, "triệu"], "label": "TỰ CHƠI TRONG BA NGÀY", "sub": {"text": DM + " · 10.2017", "at": 9}},
    score(10, 100, 0, "ALPHAGO ZERO – BẢN ĐÃ THẮNG LEE SEDOL", subAt=12),
    {"type": "kinetic", "at": 13, "items": [{"text": "CỖ MÁY TỪNG LÀM THẾ GIỚI SỬNG SỐT", "at": 14, "sm": True}, {"text": "THUA TRẮNG 100 VÁN", "at": [14, "đã"], "acc": True},
                                           {"text": "trước một cỗ máy chưa học nước cờ nào của người", "at": 15, "sm": True}]},
    {"type": "bars", "at": 16, "title": "SỐ CHIP CHUYÊN DỤNG ĐỂ CHẠY", "unit": "",
     "items": [{"k": "BẢN ĐẤU LEE SEDOL", "v": 48, "lbl": "48", "at": 16}, {"k": "ALPHAGO ZERO", "v": 4, "lbl": "4", "at": [16, "một"], "acc": True}],
     "label": {"k": "", "v": "THEO BÀI BÁO TRÊN NATURE, 10.2017", "at": 16}},
    {"type": "ledger", "at": 17, "title": "TRÊN ĐƯỜNG TỰ HỌC", "rows": [{"k": "TÌM LẠI", "v": "THẾ CỜ NGHÌN NĂM CỦA NGƯỜI", "at": 17}],
     "total": {"k": "RỒI", "v": "DÙNG THẾ CHƯA AI TỪNG ĐÁNH", "at": 18}},
    {"type": "counter", "at": 19, "from": 3, "to": 40, "suffix": " NGÀY", "until": [20, "ngày,"], "label": "TỰ HỌC TIẾP · RỒI GẶP BẢN MASTER"},
    score(21, 89, 11, "ALPHAGO ZERO – MASTER · 100 VÁN"),
    {"type": "kinetic", "at": 22, "items": [{"text": "MÁY CÓ HỌC ĐƯỢC TỪ CON NGƯỜI KHÔNG?", "at": 22, "sm": True},
                                           {"text": "NÓ KHÔNG CẦN CON NGƯỜI ĐỂ HỌC", "at": [23, "nó"], "acc": True}]},
]}

CH["ch11"] = {"hud": {"k": "CHƯƠNG 11", "t": "TỪ BÀN CỜ TỚI PHÒNG THÍ NGHIỆM"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "11", "k": "CHƯƠNG MƯỜI MỘT", "title": "TỪ BÀN CỜ TỚI\nPHÒNG THÍ NGHIỆM", "sub": "KHÔNG DỪNG Ở CỜ VÂY", "vid": "4121129", "illus": VM, "titleAt": [0, "Nếu"]},
    {"type": "ledger", "at": 2, "title": "ALPHAZERO · 12.2017", "srcnote": "THEO DEEPMIND",
     "rows": [{"k": "CÁCH HỌC", "v": "CHỈ BIẾT LUẬT, TỰ CHƠI", "at": 4}, {"k": "HỌC THÊM", "v": "CẢ CỜ VUA", "at": [4, "Nhưng"]}],
     "total": {"k": "SAU ~4 GIỜ", "v": "VƯỢT PHẦN MỀM MẠNH NHẤT", "at": 5}},
    {"type": "bars", "at": 6, "title": "100 VÁN CỜ VUA · ALPHAZERO VỚI PHẦN MỀM MẠNH NHẤT LÚC ẤY", "unit": "",
     "items": [{"k": "THẮNG", "v": 28, "lbl": "28", "at": [6, "hai"], "acc": True}, {"k": "HOÀ", "v": 72, "lbl": "72", "at": [6, "hoà"]}, {"k": "THUA", "v": 0, "lbl": "0", "at": [6, "không"]}],
     "label": {"k": "", "v": "THEO DEEPMIND, 12.2017", "at": 6}},
    {"type": "broll", "at": 7, "vid": "34499231", "veil": 0.5, "illus": VM,
     "kin": [{"text": "RA KHỎI BÀN CỜ", "at": 7, "sm": True}, {"text": "BÀI TOÁN TREO 50 NĂM", "at": 8, "acc": True}, {"text": "hình dạng của một phân tử protein", "at": 9, "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "ALPHAFOLD", "at": [10, "tên"], "acc": True}, {"text": "giải được phần lớn bài toán ấy", "at": [10, "đã"], "sm": True}]},
    {"type": "ledger", "at": 11, "title": "NOBEL HOÁ HỌC 2024", "rows": [{"k": "TRAO CHO", "v": "BA NGƯỜI", "at": 11}, {"k": "CỦA DEEPMIND", "v": "HAI NGƯỜI", "at": 12}],
     "total": {"k": "MỘT NGƯỜI LÀ", "v": "DEMIS HASSABIS", "at": 13}},
    {"type": "counter", "at": 15, "from": 0, "to": 8, "suffix": " NĂM", "until": [15, "tám"], "label": "TỪ BÀN CỜ 19 ĐƯỜNG TỚI MỘT GIẢI NOBEL", "sub": {"text": "2016 → 2024", "at": 15}},
]}

CH["ch12"] = {"hud": {"k": "CHƯƠNG 12", "t": "CON NGƯỜI THẮNG LẠI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "question", "text": "Con người có bao giờ\nthắng lại máy không?"},
    {"type": "date", "at": 1, "day": "CÓ", "date": "02.2023"},
    {"type": "ledger", "at": 2, "title": "MƯỜI LĂM VÁN", "srcnote": "THEO FINANCIAL TIMES, 02.2023",
     "rows": [{"k": "NGƯỜI", "v": "KELLIN PELRINE · NGHIỆP DƯ", "at": 2}, {"k": "MÁY", "v": "ĐỜI SAU · KHÔNG PHẢI ALPHAGO", "at": 3}],
     "total": {"k": "KẾT QUẢ", "v": "NGƯỜI THẮNG 14 VÁN", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "ANH KHÔNG GIỎI HƠN LEE SEDOL", "at": 5, "sm": True}, {"text": "BÍ QUYẾT TỪ MỘT CHƯƠNG TRÌNH KHÁC", "at": 6, "acc": True}]},
    {"type": "counter", "at": 7, "from": 0, "to": 1, "prefix": "> ", "suffix": " TRIỆU VÁN", "until": [7, "triệu"], "label": "ĐẤU THỬ CHỈ ĐỂ TÌM MỘT ĐIỂM MÙ", "sub": {"text": "VÀ NÓ TÌM RA", "at": 8}},
    {"type": "go", "at": 9, "stones": 84, "label": {"k": "XẾP MỘT VÒNG LỚN QUANH QUÂN CỦA MÁY · ĐÁNH LẠC HƯỚNG CHỖ KHÁC", "v": MOCK, "at": 9}},
    {"type": "kinetic", "at": 10, "items": [{"text": "NGƯỜI CHƠI KHÁ: NHẬN RA NGAY", "at": 10, "sm": True}, {"text": "CỖ MÁY: KHÔNG THẤY", "at": 11, "acc": True},
                                           {"text": "trước đó chưa ai biết để thử", "at": 13, "sm": True}]},
    {"type": "ledger", "at": 14, "title": "GIỐNG HỆT NƯỚC 78", "rows": [{"k": "CỖ MÁY", "v": "GIỎI HƠN Ở HẦU HẾT THẾ CỜ", "at": 15}, {"k": "NHƯNG", "v": "VẪN CÓ CHỖ KHÔNG NHÌN THẤY", "at": 16}],
     "total": {"k": "AI TÌM RA", "v": "NGƯỜI + MỘT CỖ MÁY KHÁC", "at": 17}},
]}

CH["ch13"] = {"hud": {"k": "CHƯƠNG 13", "t": "LỜI CHIA TAY"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "LEE SEDOL TUYÊN BỐ GIẢI NGHỆ", "date": "19.11.2019"},
    {"type": "kinetic", "at": 1, "items": [{"text": "36 TUỔI", "at": 1, "acc": True}, {"text": "24 năm làm kỳ thủ chuyên nghiệp", "at": [1, "Đã"], "sm": True}]},
    {"type": "quote", "at": 2, "text": "Dù tôi có trở thành số một, vẫn có một thực thể không thể bị đánh bại.", "who": "LEE SEDOL", "note": "TRÍCH DỊCH · YONHAP, 11.2019"},
    {"type": "kinetic", "at": 4, "items": [{"text": "KHÔNG PHẢI LÝ DO DUY NHẤT", "at": 4, "acc": True}, {"text": "còn mâu thuẫn với hiệp hội cờ vây", "at": 5, "sm": True}]},
    {"type": "ledger", "at": 6, "title": "BA VÁN CHIA TAY · 12.2019", "rows": [{"k": "ĐỐI THỦ", "v": "LẠI LÀ MỘT CỖ MÁY", "at": 7}, {"k": "VÁN 1 · CHẤP 2 QUÂN", "v": "ÔNG THẮNG", "at": 8}],
     "total": {"k": "HAI VÁN SAU", "v": "ÔNG THUA", "at": 9}},
    {"type": "broll", "at": 10, "vid": "6034203", "ms": 14, "veil": 0.5, "illus": VM,
     "kin": [{"text": "VÁN CUỐI CÙNG", "at": 10, "sm": True}, {"text": "Ở QUÊ NHÀ", "at": [10, "ở"], "acc": True}, {"text": "vùng đảo nơi ông lớn lên", "at": 11, "sm": True}]},
]}

CH["ch14"] = {"hud": {"k": "CHƯƠNG 14", "t": "MỘT PHẦN MƯỜI NGHÌN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "14", "k": "CHƯƠNG MƯỜI BỐN", "title": "MỘT PHẦN\nMƯỜI NGHÌN", "sub": "VÁN THUA DUY NHẤT CỦA CỖ MÁY", "vid": "39277761", "ms": 2, "illus": VM, "titleAt": [0, "Trong"]},
    real(4, 78, hit=78, at=1, hitAt=[1, "nước"], label={"k": "VÁN 4 · SEOUL · NƯỚC 78", "v": REAL, "at": 1}),
    {"type": "ledger", "at": 2, "title": "HAI NƯỚC CỜ MỘT PHẦN VẠN", "rows": [{"k": "NƯỚC 37", "v": "MÁY TÌM RA THỨ NGƯỜI BỎ SÓT", "at": 4}],
     "total": {"k": "NƯỚC 78", "v": "NGƯỜI TÌM RA THỨ MÁY BỎ SÓT", "at": 5}},
    {"type": "kinetic", "at": 6, "items": [{"text": "MỘT ĐIỀU ÍT NGƯỜI KỂ", "at": 6, "sm": True}, {"text": "CÁC KỲ THỦ KHÔNG BỎ CỜ", "at": 7, "acc": True}]},
    {"type": "counter", "at": 8, "from": 0, "to": 5.8, "suffix": " TRIỆU", "until": [8, "triệu"], "label": "NƯỚC CỜ CHUYÊN NGHIỆP ĐƯỢC XEM LẠI · 1950 → 2021",
     "sub": {"text": "NGHIÊN CỨU ĐĂNG TRÊN PNAS, 2023", "at": [8, "từ"]}},
    {"type": "ledger", "at": 9, "title": "TỪ KHI CÓ CỖ MÁY VƯỢT TRỘI", "srcnote": "PNAS, 2023",
     "rows": [{"k": "CON NGƯỜI", "v": "ĐI NƯỚC TỐT HƠN HẲN", "at": 9}], "total": {"k": "VÀ", "v": "NHIỀU NƯỚC CHƯA TỪNG CÓ", "at": 10}},
    {"type": "quote", "at": 12, "text": "Chắc chắn rồi, AlphaGo có sáng tạo.", "who": "LEE SEDOL", "note": "TRÍCH DỊCH · " + DM},
    {"type": "kinetic", "at": 13, "items": [{"text": "KHÔNG KẾT THÚC MỘT TRÒ CHƠI 2.000 NĂM", "at": 13, "sm": True}, {"text": "NÓ CHỈ ĐỔI NGƯỜI THẦY", "at": 14, "acc": True}]},
    {"type": "question", "at": 15, "text": "Thua ba ván liền,\nbạn có ngồi vào đánh ván thứ tư?"},
    {"type": "kinetic", "at": 16, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 16}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [16, "ở"], "acc": True}]},
]}

SPEC = {
    "title": "Năm Ván Cờ Thay Đổi AI: AlphaGo Đấu Lee Sedol, Và Nước Cờ Một Phần Vạn",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["alphago", "sedol", "nước", "thua", "thắng", "vạn", "nghìn", "máy"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(15)],
    "youtube": {
        "titles": ["Năm Ván Cờ Thay Đổi AI: AlphaGo Đấu Lee Sedol, Và Nước Cờ Một Phần Vạn",
                   "Nước 37 Và Nước 78: Hai Nước Cờ Một Phần Vạn Trong Trận Đấu Giữa Người Và Máy",
                   "Ván Thắng Duy Nhất Của Con Người Trước AlphaGo: Chuyện Năm Ván Cờ Ở Seoul"],
        "summary": "Tháng 3/2016 ở Seoul, kỳ thủ cờ vây Lee Sedol đấu năm ván với AlphaGo. Video kể lại từng ván theo bảng tỉ số: vì sao cờ vây "
                   "từng là thứ máy không thắng nổi, AlphaGo học thế nào, nước 37 khiến bình luận viên tưởng đặt nhầm quân, nước 78 làm cỗ máy "
                   "cuống, và chuyện sau trận đấu: AlphaGo Zero, giải Nobel 2024, và ngày Lee Sedol giải nghệ.",
        "more": ["Các bàn cờ ghi \"THẾ CỜ THẬT\" được dựng lại từ biên bản năm ván đấu (kho biên bản của Andries Brouwer, CWI); các bàn cờ ghi "
                 "\"MINH HOẠ\" có quân đặt ngẫu nhiên. Video dùng làm nền không phải hình ảnh trận đấu. Con số \"một phần mười nghìn\" cho nước 37 và nước 78 là ước tính của chính AlphaGo do DeepMind công bố; "
                 "\"hơn 200 triệu người xem\" cũng là số của DeepMind. Lời trích của Lee Sedol, Fan Hui, Kha Khiết được dịch từ báo chí và đọc bằng "
                 "giọng máy. Kỳ thủ nghiệp dư thắng máy năm 2023 đấu với một chương trình khác, không phải AlphaGo. Tên Gu Li, Ke Jie đọc theo cách "
                 "gọi quen ở Việt Nam: Cổ Lực, Kha Khiết."],
        "chapter_titles": {"ch00": "Mở đầu: nước thứ 37", "ch01": "Vì sao lại là cờ vây", "ch02": "Lee Sedol: cậu bé từ hòn đảo",
                           "ch03": "AlphaGo học từ 30 triệu nước cờ", "ch04": "Ván một: 0–1", "ch05": "Ván hai: nước 37",
                           "ch06": "Ván ba: \"tôi cảm thấy bất lực\"", "ch07": "Ván bốn: nước 78, AlphaGo xin thua", "ch08": "Ván năm: 4–1",
                           "ch09": "Sáu mươi ván thắng và Kha Khiết", "ch10": "AlphaGo Zero: cỗ máy không cần thầy",
                           "ch11": "Từ bàn cờ tới giải Nobel", "ch12": "Năm 2023: con người thắng lại", "ch13": "Lee Sedol giải nghệ",
                           "ch14": "Một phần mười nghìn"},
        "sources": [
            "https://en.wikipedia.org/wiki/AlphaGo_versus_Lee_Sedol",
            "https://deepmind.google/research/alphago/",
            "https://en.wikipedia.org/wiki/AlphaGo",
            "https://deepmind.google/blog/alphago-zero-starting-from-scratch/",
            "https://www.cbc.ca/news/science/google-deepmind-go-final-1.3491693",
            "https://www.theregister.com/2023/02/20/human_go_ai_defeat/",
            "https://arxiv.org/abs/2303.07462v2",
            "https://en.wikipedia.org/wiki/Lee_Sedol",
            "https://homepages.cwi.nl/~aeb/go/games/games/AlphaGo/",
        ],
        "hashtags": ["AlphaGo", "LeeSedol", "CờVây", "TríTuệNhânTạo", "MindInTheMachine"],
        "tags": ["alphago", "lee sedol", "alphago vs lee sedol", "cờ vây", "nước 37", "move 37", "nước 78", "deepmind", "alphago zero",
                 "trí tuệ nhân tạo", "lịch sử ai", "người đấu với máy"],
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
