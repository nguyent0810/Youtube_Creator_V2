"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #14 "Watson thắng Jeopardy!" (chuỗi Trận đấu Người – Máy).

    python data/long/mim-watson-jeopardy/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Các cảnh "ba thanh độ tự tin" là HÌNH MINH HOẠ cách Watson hiện đáp án, không phải số đo thật của một câu hỏi
cụ thể (ghi rõ trên hình). Clip: Pexels (ngang), gắn "VIDEO MINH HỌA", không phải hình ảnh chương trình. Áp luật studio (14/10/2026): myth / source / units.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"watson": "Oát-xần", "ibm": "ai bi em", "=IBM": "ai bi em", "jeopardy": "Gie-pơ-đi", "toronto": "To-rôn-tô", "chicago": "Si-ca-gô", "canada": "Ca-na-đa",
       "ken": "Ken", "jennings": "Gien-ninh", "brad": "Brát", "rutter": "Rắt-tơ", "david": "Đây-vít", "ferrucci": "Phe-ru-chi", "thomas": "Tô-mát",
       "deep": "Đíp", "blue": "Blu", "garry": "Ga-ri", "kasparov": "Cát-xpa-rốp", "texas": "Tếch-xát", "stat": "Xtát", "bloomberg": "Blum-bớc",
       "olympia": "Ô-lim-pi-a", "washington": "Oa-sinh-tơn", "rush": "Rắt", "holt": "Hôn", "project": "Prô-giếch", "debater": "Đi-bây-tơ", "harish": "Ha-rít", "natarajan": "Na-ta-ra-gian", "francisco": "Phran-xi-xcô", "afp": "a ép pê", "lee": "Li", "sedol": "Xê-đôn", "=AI": "ây ai", "chatbot": "chát-bót"}
VM = "VIDEO MINH HỌA · KHÔNG PHẢI HÌNH ẢNH CHƯƠNG TRÌNH"
CONF = "MINH HOẠ CÁCH WATSON HIỆN ĐÁP ÁN · KHÔNG PHẢI SỐ ĐO THẬT"


def three(at, title, items, **kw):
    """Ba thanh độ tự tin (cảnh bars), hình minh hoạ."""
    return {"type": "bars", "at": at, "title": title, "unit": CONF,
            "items": [{"k": k, "v": v, "lbl": lbl, "at": a, **({"acc": True} if i == 0 else {})} for i, (k, v, lbl, a) in enumerate(items)], **kw}


CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "TORONTO?????"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "1534965", "veil": 0.55, "illus": VM,
     "kin": [{"text": "15.02.2011 · TRUYỀN HÌNH MỸ", "at": [0, "Ngày"], "sm": True}, {"text": "BA NGƯỜI CHƠI · BA CÁI BỤC", "at": [1, "Ba"], "acc": True}]},
    {"type": "ledger", "at": 2, "title": "BA NGƯỜI CHƠI", "rows": [{"k": "HAI NGƯỜI", "v": "NHÀ VÔ ĐỊCH GIỎI NHẤT", "at": 2}, {"k": "NGƯỜI THỨ BA", "v": "KHÔNG PHẢI NGƯỜI", "at": 3}]},
    {"type": "source", "at": 4, "source": "CÂU HỎI CUỐI · CHỦ ĐỀ: CÁC THÀNH PHỐ CỦA NƯỚC MỸ", "ref": "GỢI Ý (DIỄN Ý)",
     "snippet": "Sân bay lớn nhất mang tên [[một người hùng]] Thế chiến II; sân bay lớn thứ hai mang tên [[một trận đánh]]", "hlAt": [6, "người"], "seal": "ĐÁP ÁN ĐÚNG: CHICAGO", "sealAt": 7},
    {"type": "myth", "at": 8, "mythLab": "CỖ MÁY VIẾT", "myth": "TORONTO?????", "truthLab": "TORONTO Ở ĐÂU?", "truth": "CANADA, KHÔNG PHẢI MỸ", "strikeAt": [10, "Toronto"], "truthAt": [10, "Nó"]},
    {"type": "kinetic", "at": 11, "items": [{"text": "HÀNG TRIỆU KHÁN GIẢ BẬT CƯỜI", "at": 11, "sm": True}, {"text": "VẬY MÀ CỖ MÁY THẮNG", "at": [12, "chính"], "acc": True},
                                           {"text": "gấp hơn ba lần người về nhì", "at": [12, "gấp"], "sm": True}]},
    {"type": "broll", "at": 13, "vid": "5028622", "veil": 0.55, "illus": VM,
     "kin": [{"text": "WATSON · IBM", "at": 13, "acc": True}, {"text": "chuỗi dấu hỏi = “tôi không chắc”", "at": 15, "sm": True}]},
    three(16, "BA ĐÁP ÁN HÀNG ĐẦU · BA THANH ĐỘ TỰ TIN", [("1 · MÁY HIỂU CÂU HỎI THẾ NÀO", 90, "?", 18), ("2 · MÁY CHẮC TỚI ĐÂU", 60, "?", 19), ("3 · RA ĐỜI THẬT ĐƯỢC KHÔNG", 30, "?", 20)]),
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "SAU DEEP BLUE"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "SAU DEEP BLUE", "sub": "IBM CẦN MỘT THỬ THÁCH MỚI", "vid": "1085656", "illus": VM, "titleAt": [0, "Năm"]},
    {"type": "myth", "at": 3, "mythLab": "CỜ VUA", "myth": "LUẬT RÕ · 64 Ô", "truthLab": "THỬ THÁCH MỚI", "truth": "NGÔN NGỮ CON NGƯỜI", "strikeAt": [6, "IBM"], "truthAt": [8, "ngôn"]},
    {"type": "broll", "at": 9, "vid": "8089117", "veil": 0.55, "illus": VM,
     "kin": [{"text": "KHOẢNG 2004 · THEO LỜI KỂ", "at": 9, "sm": True}, {"text": "CẢ NHÀ HÀNG IM LẶNG NHÌN TIVI", "at": 11, "acc": True}]},
    {"type": "units", "at": 13, "title": "KEN JENNINGS · NĂM 2004", "total": 74, "cols": 15, "lit": 74, "litAt": [14, "thắng"], "unitLabel": "VÁN THẮNG LIỀN · KỶ LỤC"},
    {"type": "question", "at": 15, "text": "Một cỗ máy có thể\nchơi trò này không?"},
]}

CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "MỘT TRÒ CHƠI KHÓ CHO MÁY"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "MỘT TRÒ CHƠI\nKHÓ CHO MÁY", "sub": "JEOPARDY! · TỪ 1964", "vid": "33684363", "illus": VM, "titleAt": [0, "Chương"]},
    {"type": "myth", "at": 1, "mythLab": "THÔNG THƯỜNG", "myth": "HỎI → TRẢ LỜI", "truthLab": "JEOPARDY", "truth": "GỢI Ý → ĐÁP BẰNG CÂU HỎI", "strikeAt": [2, "Người"], "truthAt": [2, "phải"]},
    {"type": "ledger", "at": 3, "title": "VÍ DỤ", "rows": [{"k": "GỢI Ý", "v": "THỦ ĐÔ CỦA NƯỚC PHÁP", "at": 3}, {"k": "NGƯỜI CHƠI", "v": "“PARIS LÀ GÌ?”", "at": 4}]},
    {"type": "ledger", "at": 5, "title": "GỢI Ý THẬT THÌ", "rows": [{"k": "1", "v": "CHƠI CHỮ · NÓI LÁI", "at": 6}, {"k": "2", "v": "TÊN CHỦ ĐỀ LÀ CÂU ĐÙA", "at": 7}, {"k": "3", "v": "GHÉP HAI Ý KHÔNG LIÊN QUAN", "at": 8}]},
    {"type": "ledger", "at": 9, "title": "VÀ CÒN TỐC ĐỘ", "rows": [{"k": "BIẾT", "v": "CHƯA ĐỦ", "at": 10}, {"k": "BẤM CHUÔNG", "v": "NHANH HƠN HAI NGƯỜI", "at": [10, "Phải"]}],
     "total": {"k": "TRẢ LỜI SAI", "v": "BỊ TRỪ TIỀN", "at": 11}},
    {"type": "slam", "at": 12, "text": "GẦN NHƯ KHÔNG THỂ", "sub": "VỚI MỘT CỖ MÁY NĂM 2007", "subAt": 13},
]}

CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CON NGỰA ĐÁ CON NGỰA ĐÁ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CON NGỰA ĐÁ\nCON NGỰA ĐÁ", "sub": "VÌ SAO NGÔN NGỮ KHÓ CHO MÁY", "vid": "11833936", "ms": 30, "illus": VM, "titleAt": [0, "Để"]},
    {"type": "slam", "at": 1, "text": "CON NGỰA ĐÁ CON NGỰA ĐÁ", "sub": "MỘT CHỮ “ĐÁ” · HAI NGHĨA", "subAt": 4},
    {"type": "ledger", "at": 2, "title": "BẠN HIỂU NGAY", "rows": [{"k": "NGỰA THẬT", "v": "ĐÁ", "at": [2, "một"]}, {"k": "NGỰA BẰNG ĐÁ", "v": "BỊ ĐÁ", "at": [2, "bằng"]}],
     "total": {"k": "NHỜ HIỂU ĐỜI", "v": "NGỰA ĐÁ KHÔNG ĐÁ", "at": 6}},
    {"type": "myth", "at": 7, "mythLab": "“ÔNG GIÀ ĐI NHANH QUÁ”", "myth": "ÔNG CỤ ĐI BỘ RẤT NHANH?", "truthLab": "HAY LÀ", "truth": "ÔNG ẤY GIÀ ĐI RẤT NHANH?", "strikeAt": [8, "Hay"], "truthAt": [8, "già"]},
    {"type": "kinetic", "at": 10, "items": [{"text": "MÁY KHÔNG CÓ HIỂU BIẾT ẤY SẴN", "at": 10, "acc": True}, {"text": "nó chỉ có chữ, và những gì nó đã đọc", "at": 11, "sm": True},
                                           {"text": "mỗi gợi ý Jeopardy đầy bẫy như vậy", "at": 12, "sm": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHƯƠNG 03", "t": "MỘT TIẾNG CHUÔNG"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "MỘT TIẾNG CHUÔNG", "sub": "AI BẤM TRƯỚC, NGƯỜI ẤY TRẢ LỜI", "vid": "3255224", "illus": VM, "titleAt": [0, "Nếu"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "ĐƯỜNG LÊN ĐỈNH OLYMPIA", "at": [1, "Đường"], "acc": True}, {"text": "tay đặt sẵn trên nút bấm", "at": [1, "tay"], "sm": True}]},
    {"type": "timeline", "at": 4, "items": [{"year": "ĐỌC XONG", "text": "người dẫn đọc hết gợi ý", "at": 4}, {"year": "BẤM SỚM", "text": "chuông bị khoá trong khoảnh khắc", "at": 5},
                                           {"year": "VÔ ĐỊCH", "text": "giỏi kiến thức · giỏi canh nhịp", "at": 6}]},
    {"type": "ledger", "at": 7, "title": "VỚI MỘT CỖ MÁY", "rows": [{"k": "DỄ", "v": "KHÔNG BAO GIỜ RUN TAY", "at": 8}, {"k": "KHÓ", "v": "TÌM ĐÁP ÁN TRONG VÀI GIÂY", "at": 9}]},
    {"type": "ledger", "at": 10, "title": "SAU TRẬN: HAI Ý KIẾN", "rows": [{"k": "MỘT SỐ NGƯỜI", "v": "LỢI THẾ KHÔNG CÔNG BẰNG", "at": 10}, {"k": "NGƯỜI KHÁC", "v": "BIẾT NHANH LÀ LUẬT CHƠI", "at": 11}],
     "total": {"k": "TỚI NAY", "v": "VẪN CÒN TRANH CÃI", "at": 12}},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 04", "t": "BỐN NĂM VÀ MỘT NHÓM NHỎ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "BỐN NĂM\nVÀ MỘT NHÓM NHỎ", "sub": "DAVID FERRUCCI · TỪ 2007", "vid": "7088466", "ms": 4, "illus": VM, "titleAt": [0, "Khoảng"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "PHIÊN BẢN ĐẦU: RẤT TỆ", "at": 1, "acc": True}, {"text": "đúng một phần nhỏ · chậm tới mức không thể thi đấu", "at": 2, "sm": True}]},
    {"type": "myth", "at": 3, "mythLab": "KHÔNG TÌM", "myth": "MỘT THUẬT TOÁN THẦN KỲ", "truthLab": "MÀ GHÉP", "truth": "HÀNG TRĂM CÁCH NHỎ", "strikeAt": [4, "Họ"], "truthAt": [5, "hàng"]},
    {"type": "kinetic", "at": 7, "items": [{"text": "TÊN DỰ ÁN: WATSON", "at": 7, "acc": True}, {"text": "theo người sáng lập IBM, Thomas Watson", "at": 8, "sm": True}]},
    {"type": "ledger", "at": 10, "title": "WATSON · 2011", "rows": [{"k": "MÁY CHỦ", "v": "90", "at": 10}, {"k": "LÕI XỬ LÝ", "v": "2.880", "at": 11}, {"k": "BỘ NHỚ", "v": "16 TERABYTE", "at": [11, "mười"]}],
     "total": {"k": "KÍCH THƯỚC", "v": "MỘT CĂN PHÒNG", "at": 12}},
]}

CH["ch06"] = {"hud": {"k": "THANH 01", "t": "HIỂU CÂU HỎI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "THANH THỨ NHẤT", "title": "HIỂU CÂU HỎI", "sub": "TẠO RẤT NHIỀU ĐÁP ÁN, RỒI CHẤM ĐIỂM", "vid": "11833936", "illus": VM, "titleAt": [0, "Vậy"]},
    {"type": "myth", "at": 1, "mythLab": "WATSON KHÔNG", "myth": "HIỂU NHƯ BẠN HIỂU", "truthLab": "NÓ", "truth": "TẠO NHIỀU ĐÁP ÁN · CHẤM ĐIỂM", "strikeAt": [2, "Nó"], "truthAt": [2, "tạo"]},
    {"type": "timeline", "at": 3, "items": [{"year": "BƯỚC 1", "text": "mổ xẻ gợi ý: hỏi về người, nơi chốn hay năm?", "at": 3},
                                           {"year": "BƯỚC 2", "text": "lục tìm trong kho kiến thức", "at": 6}, {"year": "BƯỚC 3", "text": "tìm bằng chứng cho từng đáp án", "at": 10}]},
    {"type": "counter", "at": 7, "from": 200, "to": 200, "suffix": " TRIỆU", "label": "TRANG VĂN BẢN · NẠP SẴN VÀO BỘ NHỚ", "sub": {"text": "BÁCH KHOA TOÀN THƯ · TỪ ĐIỂN · SÁCH · BÁO", "at": 7}},
    three(9, "HÀNG TRĂM ĐÁP ÁN CÓ THỂ → MỖI CÁI MỘT ĐIỂM", [("ĐÁP ÁN A", 72, "72%", 12), ("ĐÁP ÁN B", 21, "21%", [12, "cho"]), ("ĐÁP ÁN C", 7, "7%", 13)]),
    {"type": "slam", "at": 14, "text": "ĐIỂM ẤY = ĐỘ TỰ TIN", "sub": "PHẦN QUAN TRỌNG NHẤT", "subAt": 14},
]}

CH["ch07"] = {"hud": {"k": "THANH 02", "t": "BIẾT MÌNH CHẮC TỚI ĐÂU"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "THANH THỨ HAI", "title": "BIẾT MÌNH\nCHẮC TỚI ĐÂU", "sub": "TRẢ LỜI SAI BỊ TRỪ TIỀN", "vid": "1085656", "ms": 6, "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "WATSON CẦN BIẾT", "at": 1, "sm": True}, {"text": "KHI NÀO MÌNH KHÔNG BIẾT", "at": 2, "acc": True}]},
    {"type": "counter", "at": 3, "from": 50, "to": 50, "suffix": "%", "prefix": "~", "label": "NGƯỠNG ĐỘ TỰ TIN ĐỂ BẤM CHUÔNG", "sub": {"text": "THEO TÀI LIỆU VỀ HỆ THỐNG · TỰ ĐIỀU CHỈNH THEO VÁN", "at": 5}},
    {"type": "ledger", "at": 6, "title": "MỘT CỖ MÁY BIẾT CÂN NHẮC RỦI RO", "rows": [{"k": "DẪN XA", "v": "THẬN TRỌNG HƠN", "at": 6}, {"k": "BỊ BÁM ĐUỔI", "v": "LIỀU HƠN", "at": 7}]},
    three(9, "KHI THANH ĐẦU DÀI VƯỢT HẲN → BẤM CHUÔNG", [("ĐÁP ÁN HÀNG ĐẦU", 88, "88%", 11), ("THỨ HAI", 9, "9%", [10, "đáp"]), ("THỨ BA", 3, "3%", [10, "ba"])]),
    three(12, "KHI BA THANH ĐỀU NGẮN → IM LẶNG", [("ĐÁP ÁN HÀNG ĐẦU", 31, "31%", 12), ("THỨ HAI", 26, "26%", [12, "nó"]), ("THỨ BA", 22, "22%", [12, "im"])]),
    {"type": "slam", "at": 13, "text": "BIẾT IM LẶNG KHI KHÔNG CHẮC", "sub": "HÃY NHỚ ĐIỀU NÀY", "subAt": 14},
]}

CH["ch08"] = {"hud": {"k": "CHƯƠNG 07", "t": "TRẬN ĐẤU"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "TRẬN ĐẤU", "sub": "14 – 16.02.2011", "vid": "8089117", "ms": 10, "illus": VM, "titleAt": [0, "Trận"]},
    {"type": "ledger", "at": 1, "title": "ĐỐI THỦ CỦA WATSON", "rows": [{"k": "KEN JENNINGS", "v": "74 VÁN THẮNG LIỀN", "at": 1}, {"k": "BRAD RUTTER", "v": "NHIỀU TIỀN THƯỞNG NHẤT", "at": 2}]},
    {"type": "ledger", "at": 3, "title": "WATSON KHÔNG CÓ MẮT, KHÔNG CÓ TAI", "rows": [{"k": "NHẬN GỢI Ý", "v": "DƯỚI DẠNG CHỮ", "at": 4}, {"k": "BẤM CHUÔNG", "v": "BẰNG CÁNH TAY CƠ KHÍ", "at": 5}]},
    {"type": "timeline", "at": 6, "items": [{"year": "NGÀY 1", "text": "ngang ngửa với Rutter", "at": 6}, {"year": "NGÀY 2", "text": "bắt đầu bứt lên", "at": 7}]},
    {"type": "myth", "at": 8, "mythLab": "CÓ LÚC", "myth": "NHANH VÀ ĐÚNG ĐẾN KHÓ TIN", "truthLab": "CÓ LÚC", "truth": "SAI KIỂU KHÔNG AI SAI", "strikeAt": [9, "Nhưng"], "truthAt": [9, "sai"]},
    {"type": "kinetic", "at": 10, "items": [{"text": "LẶP LẠI ĐÁP ÁN SAI VỪA NGHE", "at": 10, "acc": True}, {"text": "vì nó không nghe thấy người khác nói gì", "at": [10, "Vì"], "sm": True}]},
]}

CH["ch09"] = {"hud": {"k": "CHƯƠNG 08", "t": "TORONTO"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "TORONTO", "sub": "CÂU HỎI CUỐI CỦA VÁN MỘT", "vid": "18757432", "illus": VM, "titleAt": [0, "Và"]},
    {"type": "ledger", "at": 3, "title": "CÂU TRẢ LỜI", "rows": [{"k": "HAI NGƯỜI CHƠI", "v": "CHICAGO", "at": 3}, {"k": "WATSON", "v": "TORONTO?????", "at": 4}]},
    {"type": "counter", "at": 6, "from": 947, "to": 947, "suffix": " ĐÔ LA", "label": "SỐ TIỀN WATSON ĐẶT CƯỢC", "sub": {"text": "MỘT CON SỐ NHỎ · NÓ KHÔNG TIN VÀO ĐÁP ÁN", "at": 9}},
    {"type": "ledger", "at": 10, "title": "GIẢI THÍCH CỦA DAVID FERRUCCI", "rows": [{"k": "1", "v": "TÊN CHỦ ĐỀ CHỈ GỢI Ý LỎNG", "at": 11}, {"k": "2", "v": "MỸ CÓ VÀI NƠI TÊN TORONTO", "at": 12},
                                                                                     {"k": "3", "v": "ĐỘI BÓNG CHÀY Ở GIẢI MỸ", "at": 13}]},
    {"type": "myth", "at": 14, "mythLab": "NGƯỜI CHƠI TỒI", "myth": "SAI VÀ CƯỢC LỚN", "truthLab": "WATSON", "truth": "SAI NHƯNG CƯỢC ÍT", "strikeAt": [15, "Nhưng"], "truthAt": [15, "cược"]},
]}

CH["ch10"] = {"hud": {"k": "CHƯƠNG 09", "t": "NHỮNG ÔNG CHỦ MÁY TÍNH MỚI"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "9", "k": "CHƯƠNG CHÍN", "title": "NHỮNG ÔNG CHỦ\nMÁY TÍNH MỚI", "sub": "16.02.2011", "vid": "3255224", "ms": 2, "illus": VM, "titleAt": [0, "Ván"]},
    {"type": "quote", "at": 3, "text": "Tôi, về phần mình, xin chào đón những ông chủ máy tính mới của chúng ta.", "who": "KEN JENNINGS", "note": "TRÍCH DỊCH · DÒNG VIẾT THÊM Ở CÂU HỎI CUỐI"},
    {"type": "bars", "at": 6, "title": "TỔNG TIỀN SAU HAI VÁN (ĐÔ LA)", "unit": "THEO BÁO CHÍ, 02.2011",
     "items": [{"k": "WATSON", "v": 77147, "lbl": "77.147", "at": [6, "Watson"], "acc": True}, {"k": "JENNINGS", "v": 24000, "lbl": "24.000", "at": [7, "Jennings"]}, {"k": "RUTTER", "v": 21600, "lbl": "21.600", "at": [7, "Rutter"]}]},
    {"type": "ledger", "at": 9, "title": "GIẢI NHẤT", "rows": [{"k": "TIỀN THƯỞNG", "v": "1 TRIỆU ĐÔ LA", "at": 9}, {"k": "IBM", "v": "LÀM TỪ THIỆN TOÀN BỘ", "at": 10}]},
    {"type": "timeline", "at": 11, "items": [{"year": "1997", "text": "Deep Blue thắng cờ vua", "at": 11}, {"year": "2011", "text": "Watson thắng đố vui", "at": [11, "một"]}]},
]}

CH["ch11"] = {"hud": {"k": "CHƯƠNG 10", "t": "NGƯỜI THUA LÊN TIẾNG"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "10", "k": "CHƯƠNG MƯỜI", "title": "NGƯỜI THUA\nLÊN TIẾNG", "sub": "KEN JENNINGS", "vid": "6951391", "illus": VM, "titleAt": [0, "Hai"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "NGƯỜI ĐẦU TIÊN", "at": 2, "sm": True}, {"text": "BỊ MÁY LẤY MẤT VIỆC MÌNH GIỎI NHẤT", "at": [2, "bị"], "acc": True}, {"text": "diễn ý lời Ken Jennings, 2013", "at": [2, "giỏi"], "sm": True}]},
    {"type": "myth", "at": 3, "mythLab": "TƯỞNG LÀ", "myth": "HẾT CHỖ CHO NGƯỜI", "truthLab": "NHIỀU NĂM SAU", "truth": "ÔNG DẪN CHÍNH CHƯƠNG TRÌNH ẤY", "strikeAt": [4, "Nhiều"], "truthAt": [4, "dẫn"]},
    {"type": "timeline", "at": 8, "items": [{"year": "KASPAROV", "text": "cờ vua · 1997", "at": 8}, {"year": "JENNINGS", "text": "đố vui · 2011", "at": [8, "từ"]}, {"year": "LEE SEDOL", "text": "cờ vây · 2016", "at": [8, "Lee"]}],
     "tag": {"text": "CHỖ CỦA CON NGƯỜI THAY ĐỔI", "at": [8, None, 0, 0.6]}},
]}

CH["ch12"] = {"hud": {"k": "CHƯƠNG 12", "t": "MỘT TRẬN NHỎ Ở WASHINGTON"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "12", "k": "CHƯƠNG MƯỜI HAI", "title": "MỘT TRẬN NHỎ\nỞ WASHINGTON", "sub": "28.02.2011", "vid": "6951391", "ms": 4, "illus": VM, "titleAt": [0, "Hai"]},
    {"type": "ledger", "at": 2, "title": "ĐỐI THỦ: NGHỊ SĨ QUỐC HỘI MỸ", "rows": [{"k": "RUSH HOLT", "v": "NHÀ VẬT LÝ", "at": 3}, {"k": "THỜI TRẺ", "v": "5 LẦN THẮNG JEOPARDY", "at": [3, "năm"]}]},
    {"type": "bars", "at": 4, "title": "VÒNG ĐẦU (ĐÔ LA)", "unit": "THEO BÁO CHÍ, 03.2011",
     "items": [{"k": "RUSH HOLT", "v": 8600, "lbl": "8.600", "at": [4, "Tám"], "acc": True}, {"k": "WATSON", "v": 6200, "lbl": "6.200", "at": [4, "sáu"]}]},
    {"type": "quote", "at": 7, "text": "Tôi tự hỏi có phải tối nay Watson hơi yếu điện không, vì tôi thật sự không nghĩ mình ghi điểm cao hơn cỗ máy.", "who": "RUSH HOLT", "note": "TRÍCH DỊCH · 03.2011"},
    {"type": "kinetic", "at": 9, "items": [{"text": "TRẬN ĐẤU KHÔNG LÊN SÓNG", "at": 9, "sm": True}, {"text": "CHIẾN THẮNG CỦA MÁY KHÔNG TUYỆT ĐỐI", "at": 11, "acc": True}]},
]}

CH["ch13"] = {"hud": {"k": "CHƯƠNG 11", "t": "TỪ TRƯỜNG QUAY TỚI BỆNH VIỆN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "11", "k": "CHƯƠNG MƯỜI MỘT", "title": "TỪ TRƯỜNG QUAY\nTỚI BỆNH VIỆN", "sub": "KẾ HOẠCH LỚN CỦA IBM", "vid": "5406015", "illus": VM, "titleAt": [0, "Sau"]},
    {"type": "myth", "at": 1, "mythLab": "ĐỌC 200 TRIỆU TRANG", "myth": "ĐỂ TRẢ LỜI CÂU ĐỐ", "truthLab": "SAO KHÔNG", "truth": "ĐỌC SÁCH Y KHOA?", "strikeAt": [1, "sao"], "truthAt": [1, "đọc"]},
    {"type": "ledger", "at": 3, "title": "LĨNH VỰC KHÓ NHẤT: UNG THƯ", "rows": [{"k": "KHOẢNG 2012", "v": "TRUNG TÂM UNG THƯ Ở TEXAS", "at": 4}, {"k": "MỤC TIÊU", "v": "ĐỌC HỒ SƠ · GỢI Ý ĐIỀU TRỊ", "at": 5}]},
    {"type": "broll", "at": 6, "vid": "7088466", "veil": 0.55, "illus": VM,
     "kin": [{"text": "“BÁC SĨ TƯƠNG LAI”", "at": 6, "acc": True}, {"text": "máy thắng đố vui · giờ được kỳ vọng cứu người", "at": 8, "sm": True}]},
]}

CH["ch14"] = {"hud": {"k": "CHƯƠNG 12", "t": "SÁU MƯƠI HAI TRIỆU ĐÔ LA"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "12", "k": "CHƯƠNG MƯỜI HAI", "title": "SÁU MƯƠI HAI\nTRIỆU ĐÔ LA", "sub": "ĐẦU NĂM 2017", "vid": "6998080", "illus": VM, "titleAt": [0, "Năm"]},
    {"type": "source", "at": 1, "source": "KIỂM TOÁN ĐẠI HỌC TEXAS · ĐẦU 2017", "ref": "DỰ ÁN Ở TRUNG TÂM UNG THƯ", "snippet": "dự án [[đã bị tạm dừng]] · chi phí khoảng 62 triệu đô la",
     "hlAt": [1, "tạm"], "seal": "KHOẢNG 62 TRIỆU ĐÔ LA", "sealAt": 2},
    {"type": "ledger", "at": 3, "title": "BẢN KIỂM TOÁN NÓI VỀ", "rows": [{"k": "CHỦ YẾU", "v": "HỢP ĐỒNG · CHI TIÊU · QUY TRÌNH", "at": 3}, {"k": "MỘT VẤN ĐỀ", "v": "HỒ SƠ BỆNH ÁN KHÔNG KHỚP", "at": 5}]},
    {"type": "ledger", "at": 6, "title": "CẦN NÓI CHO CÔNG BẰNG", "rows": [{"k": "KIỂM TOÁN", "v": "KHÔNG XÉT NĂNG LỰC KHOA HỌC", "at": 7}, {"k": "IBM", "v": "TRÙNG CHUYÊN GIA ≈90% SỐ LẦN", "at": 8}]},
    {"type": "myth", "at": 9, "mythLab": "THẮNG", "myth": "MỘT TRÒ ĐỐ VUI", "truthLab": "KHÁC HẲN", "truth": "LÀM VIỆC TRONG BỆNH VIỆN", "strikeAt": [11, "Làm"], "truthAt": [11, "bệnh"]},
]}

CH["ch15"] = {"hud": {"k": "CHƯƠNG 13", "t": "NHỮNG CA BỆNH GIẢ ĐỊNH"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "13", "k": "CHƯƠNG MƯỜI BA", "title": "NHỮNG CA BỆNH\nGIẢ ĐỊNH", "sub": "TÀI LIỆU NỘI BỘ · 2018", "vid": "5406015", "ms": 6, "illus": VM, "titleAt": [0, "Năm"]},
    {"type": "source", "at": 1, "source": "STAT · 2018 · TÀI LIỆU NỘI BỘ CỦA IBM", "ref": "WATSON CHO UNG THƯ", "snippet": "các chuyên gia thấy [[khuyến nghị không an toàn và không chính xác]] khi thử nghiệm",
     "hlAt": [2, "khuyến"], "seal": "THEO TÀI LIỆU ĐƯỢC CÔNG BỐ", "sealAt": 3},
    {"type": "myth", "at": 3, "mythLab": "TƯỞNG HỌC TỪ", "myth": "RẤT NHIỀU BỆNH NHÂN THẬT", "truthLab": "CHỦ YẾU LÀ", "truth": "MỘT SỐ ÍT CA GIẢ ĐỊNH", "strikeAt": [4, "Hệ"], "truthAt": [4, "giả"]},
    {"type": "ledger", "at": 6, "title": "PHÍA IBM", "rows": [{"k": "BỆNH NHÂN", "v": "CHƯA AI BỊ TỔN HẠI", "at": 6}, {"k": "QUYẾT ĐỊNH CUỐI", "v": "LUÔN LÀ BÁC SĨ", "at": 7}]},
    {"type": "question", "at": 10, "text": "Cỗ máy có biết lúc nào\nmình không chắc không?"},
]}

CH["ch16"] = {"hud": {"k": "THANH 03", "t": "KHI ĐỜI THẬT KHÔNG PHẢI TRÒ CHƠI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "14", "k": "THANH THỨ BA", "title": "KHI ĐỜI THẬT\nKHÔNG PHẢI TRÒ CHƠI", "sub": "ĐỘ TỰ TIN CHỈ ĐÁNG TIN Ở NƠI ĐÃ THỬ", "vid": "11833936", "ms": 20, "illus": VM, "titleAt": [0, "Vì"]},
    {"type": "ledger", "at": 1, "title": "TRÒ JEOPARDY", "rows": [{"k": "MỖI GỢI Ý", "v": "ĐÚNG MỘT ĐÁP ÁN", "at": 2}, {"k": "ĐÁP ÁN", "v": "ĐÃ NẰM TRONG SÁCH VỞ", "at": [2, "Đáp"]}]},
    {"type": "ledger", "at": 3, "title": "BỆNH VIỆN", "rows": [{"k": "HỒ SƠ", "v": "VIẾT TẮT · THIẾU · MÂU THUẪN", "at": 4}, {"k": "NHIỀU CÂU HỎI", "v": "CHƯA CÓ TRONG SÁCH NÀO", "at": 5}],
     "total": {"k": "CÂU SAI", "v": "KHÔNG CÒN LÀ 947 ĐÔ LA", "at": 6}},
    {"type": "kinetic", "at": 7, "items": [{"text": "ĐỘ TỰ TIN CHỈ CÓ ÍCH", "at": 7, "sm": True}, {"text": "TRÊN ĐÚNG LOẠI CÂU HỎI ĐÃ THỬ", "at": [7, "trên"], "acc": True}]},
    {"type": "myth", "at": 10, "mythLab": "KHÔNG PHẢI", "myth": "MÁY BIẾT BAO NHIÊU", "truthLab": "MÀ LÀ", "truth": "NÓ ĐƯỢC THỬ Ở ĐÂU", "strikeAt": [11, "Không"], "truthAt": [12, "Mà"]},
]}

CH["ch17"] = {"hud": {"k": "CHƯƠNG 17", "t": "MỘT CỖ MÁY BIẾT TRANH LUẬN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "17", "k": "CHƯƠNG MƯỜI BẢY", "title": "MỘT CỖ MÁY\nBIẾT TRANH LUẬN", "sub": "PROJECT DEBATER · 02.2019", "vid": "8089117", "ms": 16, "illus": VM, "titleAt": [0, "IBM"]},
    {"type": "ledger", "at": 3, "title": "SAN FRANCISCO · 02.2019", "rows": [{"k": "CON NGƯỜI", "v": "HARISH NATARAJAN", "at": 3}, {"k": "CHỦ ĐỀ", "v": "TRỢ CẤP MẦM NON?", "at": 4}, {"k": "CHUẨN BỊ", "v": "15 PHÚT", "at": [4, "mười"]}],
     "total": {"k": "MÁY · NGƯỜI", "v": "ỦNG HỘ · PHẢN ĐỐI", "at": 5}},
    {"type": "timeline", "at": 7, "items": [{"year": "TRƯỚC", "text": "khán giả bỏ phiếu", "at": 7}, {"year": "SAU", "text": "bỏ phiếu lần nữa", "at": [7, "sau"]}, {"year": "THẮNG", "text": "bên làm nhiều người đổi ý về phía mình", "at": 8}]},
    {"type": "bars", "at": 9, "title": "KHÁN GIẢ ỦNG HỘ TRỢ CẤP (%)", "unit": "THEO AFP, 02.2019",
     "items": [{"k": "TRƯỚC TRANH LUẬN", "v": 79, "lbl": "79", "at": [10, "bảy"]}, {"k": "SAU TRANH LUẬN", "v": 62, "lbl": "62", "at": [10, "sáu"], "acc": True}]},
    {"type": "slam", "at": 12, "text": "CON NGƯỜI THẮNG", "sub": "TRÊN SÂN KHẤU CỦA NGÔN NGỮ", "subAt": 12},
]}

CH["ch18"] = {"hud": {"k": "CHƯƠNG 15", "t": "MỘT CÁI TÊN BỊ BÁN ĐI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "15", "k": "CHƯƠNG MƯỜI LĂM", "title": "MỘT CÁI TÊN\nBỊ BÁN ĐI", "sub": "01.2022", "vid": "5028622", "ms": 14, "illus": VM, "titleAt": [0, "Những"]},
    {"type": "ledger", "at": 1, "title": "THÁNG 1 NĂM 2022", "rows": [{"k": "IBM BÁN", "v": "PHẦN LỚN TÀI SẢN WATSON HEALTH", "at": 1}, {"k": "CHO", "v": "MỘT QUỸ ĐẦU TƯ", "at": [1, "cho"]},
                                                                      {"k": "GIÁ", "v": "> 1 TỶ ĐÔ LA · THEO BLOOMBERG", "at": 2}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "IBM VẪN GIỮ CÔNG NGHỆ AI MANG TÊN WATSON", "at": 3, "sm": True}, {"text": "GIẤC MƠ BÁC SĨ MÁY LẶNG LẼ KHÉP LẠI", "at": 5, "acc": True}]},
    {"type": "timeline", "at": 6, "items": [{"year": "2011", "text": "thắng trên sân khấu truyền hình", "at": 6}, {"year": "2017", "text": "dự án ung thư tạm dừng", "at": [6, "tới"]}, {"year": "2022", "text": "bán tài sản Watson Health", "at": [6, "một"]}]},
    {"type": "myth", "at": 7, "mythLab": "HAY ĐƯỢC KỂ NHƯ", "myth": "MỘT THẤT BẠI", "truthLab": "CHÍNH XÁC HƠN", "truth": "TRÌNH DIỄN ≠ CÔNG VIỆC THẬT", "strikeAt": [8, "Nhưng"], "truthAt": [8, "khoảng"]},
]}

CH["ch19"] = {"hud": {"k": "CHƯƠNG 16", "t": "CỖ MÁY KHÔNG BIẾT MÌNH KHÔNG BIẾT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "16", "k": "CHƯƠNG MƯỜI SÁU", "title": "CỖ MÁY KHÔNG BIẾT\nMÌNH KHÔNG BIẾT", "sub": "CUỐI NĂM 2022", "vid": "1085656", "ms": 12, "illus": VM, "titleAt": [0, "Mười"]},
    {"type": "ledger", "at": 1, "title": "MỘT CHATBOT MỚI · 2022", "rows": [{"k": "VIẾT", "v": "TRƠN TRU HƠN WATSON RẤT NHIỀU", "at": 1}, {"k": "TRẢ LỜI", "v": "GẦN NHƯ MỌI CÂU HỎI", "at": 2}]},
    {"type": "myth", "at": 3, "mythLab": "WATSON TRÊN SÂN KHẤU", "myth": "IM LẶNG KHI KHÔNG CHẮC", "truthLab": "CHATBOT ĐỜI ĐẦU", "truth": "LUÔN CHẮC CHẮN · KỂ CẢ KHI BỊA", "strikeAt": [5, "Các"], "truthAt": [6, "Chúng"]},
    {"type": "units", "at": 7, "title": "10 BÀI KIỂM TRA XẾP HẠNG MÔ HÌNH · CÓ CHO ĐIỂM “TÔI KHÔNG BIẾT”?", "total": 10, "cols": 10, "lit": 9, "litAt": 8, "unitLabel": "KHÔNG CHO ĐIỂM NÀO",
     "label": {"k": "THEO NGHIÊN CỨU 09.2025 · XEM VIDEO “AI BỊA” CỦA KÊNH", "v": "", "at": 8}},
    {"type": "slam", "at": 10, "text": "TORONTO?????", "sub": "MỘT CÂU SAI · NHƯNG TRUNG THỰC", "subAt": 11},
    {"type": "kinetic", "at": 12, "items": [{"text": "MÁY HÔM NAY ĐANG HỌC LẠI BÀI HỌC ẤY", "at": 12, "acc": True}, {"text": "nói “không chắc” · dẫn nguồn để người dùng tự kiểm", "at": 13, "sm": True},
                                           {"text": "chậm hơn mười mấy năm · nhưng đang tới", "at": 14, "sm": True}]},
]}

CH["ch20"] = {"hud": {"k": "CHƯƠNG 17", "t": "BA THANH ĐỘ TỰ TIN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "17", "k": "CHƯƠNG MƯỜI BẢY", "title": "BA THANH\nĐỘ TỰ TIN", "sub": "ĐẶT CẠNH NHAU", "vid": "33684363", "ms": 2, "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "ledger", "at": 1, "title": "BA THANH CỦA VIDEO NÀY", "rows": [{"k": "1", "v": "NHIỀU ĐÁP ÁN · TÌM BẰNG CHỨNG", "at": 1}, {"k": "2", "v": "CHỈ BẤM KHI ĐỦ CHẮC", "at": 2},
                                                                       {"k": "3", "v": "CHỈ TIN Ở NƠI ĐÃ THỬ", "at": 3}]},
    {"type": "ledger", "at": 4, "title": "BA CÂU TỰ HỎI KHI DÙNG TRỢ LÝ AI", "rows": [{"k": "1", "v": "CÂU TRẢ LỜI LẤY TỪ ĐÂU?", "at": [6, "Nó"]}, {"k": "2", "v": "NÓ CHO THẤY NÓ CHẮC TỚI ĐÂU?", "at": [6, "có"]},
                                                                                    {"k": "3", "v": "CÂU HỎI CỦA MÌNH CÓ HỢP NÓ?", "at": [6, "Câu"]}]},
    {"type": "myth", "at": 7, "mythLab": "CHƯA CHẮC ĐÚNG", "myth": "CÂU TRẢ LỜI TRƠN TRU", "truthLab": "ĐÔI KHI TRUNG THỰC NHẤT", "truth": "MỘT CHUỖI DẤU HỎI", "strikeAt": [8, "Một"], "truthAt": [8, "dấu"]},
]}

CH["ch21"] = {"hud": {"k": "PHẦN CUỐI", "t": "DẤU HỎI"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "18", "k": "PHẦN CUỐI", "title": "DẤU HỎI", "sub": "MỘT CỖ MÁY GIỎI LÀ GÌ?", "vid": "1534965", "ms": 6, "illus": VM, "titleAt": [0, "Watson"]},
    {"type": "ledger", "at": 1, "title": "WATSON THẮNG BẰNG", "rows": [{"k": "1", "v": "TỐC ĐỘ · KIẾN THỨC", "at": [1, None, 0, 0.05]}, {"k": "2", "v": "BIẾT LÚC NÊN DÈ DẶT", "at": [1, None, 0, 0.4]}],
     "total": {"k": "RỒI VẤP Ở", "v": "BỆNH VIỆN", "at": [1, "bệnh"]}},
    {"type": "myth", "at": 3, "mythLab": "CỖ MÁY GIỎI KHÔNG PHẢI", "myth": "LUÔN CÓ CÂU TRẢ LỜI", "truthLab": "MÀ LÀ", "truth": "CHO BIẾT KHI NÀO NÊN TIN", "strikeAt": [4, "Mà"], "truthAt": [4, "cho"]},
    {"type": "question", "at": 7, "text": "Lần gần nhất AI trả lời sai bạn\nmột cách rất tự tin là khi nào?"},
]}

SPEC = {
    "title": "Watson Thắng Jeopardy! 2011: Cỗ Máy Trả Lời “Toronto?????”",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["watson", "toronto", "tự", "tin", "máy", "chắc", "thắng", "sai"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(22)],
    "youtube": {
        "titles": ["Watson Thắng Jeopardy! 2011: Cỗ Máy Trả Lời “Toronto?????”",
                   "Ngày Máy Tính Thắng Hai Nhà Vô Địch Đố Vui: IBM Watson, 2011",
                   "Từ Jeopardy! Tới Bệnh Viện: Watson Thắng Trên Truyền Hình, Rồi Vấp Ngoài Đời Thật"],
        "summary": "Tháng 2/2011, cỗ máy Watson của IBM thắng hai nhà vô địch trò đố vui Jeopardy! trên truyền hình Mỹ, dù từng trả lời “Toronto” cho "
                   "câu hỏi về thành phố nước Mỹ. Video đi qua ba “thanh độ tự tin”: máy hiểu câu hỏi thế nào, máy biết mình chắc tới đâu, và độ tự tin "
                   "ấy có mang ra đời thật được không: dự án ung thư 62 triệu đô la bị tạm dừng, tài liệu nội bộ năm 2018, và việc IBM bán tài sản "
                   "Watson Health năm 2022. Kèm so sánh với các chatbot ngày nay.",
        "more": ["Các cảnh “ba thanh độ tự tin” là hình minh hoạ cách Watson hiện đáp án trên sóng, không phải số đo thật của một câu hỏi cụ thể. "
                 "Gợi ý câu hỏi Toronto được diễn ý. Lời trích được dịch và đọc bằng giọng máy. Video làm nền không phải hình ảnh chương trình. Chuyện "
                 "ý tưởng ra đời ở một nhà hàng năm 2004 là theo lời kể được báo chí ghi lại."],
        "chapter_titles": {"ch00": "Mở đầu: Toronto?????", "ch01": "Sau Deep Blue", "ch02": "Một trò chơi khó cho máy", "ch03": "Một tiếng chuông",
                           "ch04": "Bốn năm và một nhóm nhỏ", "ch05": "Thanh 1: máy hiểu câu hỏi thế nào", "ch06": "Thanh 2: biết mình chắc tới đâu",
                           "ch07": "Trận đấu", "ch08": "Toronto", "ch09": "Những ông chủ máy tính mới", "ch10": "Người thua lên tiếng",
                           "ch11": "Từ trường quay tới bệnh viện", "ch12": "Sáu mươi hai triệu đô la", "ch13": "Những ca bệnh giả định",
                           "ch14": "Thanh 3: khi đời thật không phải trò chơi", "ch15": "Một cái tên bị bán đi", "ch16": "Cỗ máy không biết mình không biết",
                           "ch17": "Ba thanh độ tự tin", "ch18": "Dấu hỏi"},
        "sources": ["https://en.wikipedia.org/wiki/IBM_Watson",
                    "https://www.pcworld.com/article/494966/ibm_watson_wins_jeopardy_humans_rally_back.html",
                    "https://techcrunch.com/2011/02/16/the-final-night-of-ibms-jeopardy-challenge-how-did-watson-do",
                    "https://www.ctvnews.ca/ibm-s-computer-wins-jeopardy-but-toronto-1.608022",
                    "https://www.engadget.com/2017-02-20-watson-cancer-research-runs-into-trouble.html",
                    "https://medcitynews.com/2017/02/rometty-himss-md-anderson-watson/",
                    "https://www.fiercehealthcare.com/tech/ibm-sells-watson-health-assets-to-investment-firm-francisco-partners"],
        "hashtags": ["IBMWatson", "Jeopardy", "TríTuệNhânTạo", "LịchSửAI", "MindInTheMachine"],
        "tags": ["ibm watson", "watson jeopardy", "jeopardy", "ken jennings", "máy tính thắng đố vui", "watson health", "ai trong y tế", "độ tự tin của ai",
                 "lịch sử ai", "người đấu với máy", "trí tuệ nhân tạo"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}


def renumber():
    """Sau khi chèn chương: số trên thẻ chương + nhãn HUD theo đúng thứ tự (ch00 = mở đầu, chương cuối = PHẦN CUỐI, nhãn THANH giữ nguyên)."""
    keys = sorted(CH)
    for k in keys:
        i = int(k[2:])
        for sc in CH[k]["scenes"]:
            if sc["type"] == "chapter":
                sc["no"] = str(i)
                if k != keys[-1] and not sc["k"].startswith("THANH"):
                    sc["k"] = f"CHƯƠNG {i:02d}"
        hk = CH[k]["hud"]["k"]
        if hk.startswith("CHƯƠNG"):
            CH[k]["hud"]["k"] = f"CHƯƠNG {i:02d}"


def main():
    renumber()
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
