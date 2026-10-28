"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho MIM #7 "AI Có Học Từ Cuộc Trò Chuyện Của Bạn Không?".

    python data/long/mim-ai-chat-privacy/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (đã kiểm chứng vòng 1). Nguồn: trang trợ giúp / chính sách OpenAI, Google (Gemini Apps Privacy Hub), Anthropic, đọc 09/10/2026.
Ảnh: chỉ PD / CC0 / CC BY (no_sa). Menu ứng dụng = MÔ PHỎNG dựng bằng chữ, không logo, không chụp giao diện thật. beat2 bật.
BƯỚC 1: chỉ spec để thu giọng; scenes viết sau khi có timing.json.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

SAY = {"chatgpt": "Chát-gi-pi-ti", "openai": "Âu-pần Ây-ai", "google": "Gu-gồ", "gemini": "Giê-mi-nai", "claude": "Cờ-lốt",
       "anthropic": "En-thờ-ro-píc", "samsung": "Xam-xung", "bloomberg": "Blum-bớc", "keep": "Kíp", "activity": "Ác-ti-vi-ti",
       "improve": "Im-pruv", "the": "đờ", "model": "mo-đồ", "for": "pho", "everyone": "e-vri-oan", "hack": "hách", "link": "linh"}

VM = "VIDEO MINH HỌA"
MOCK = "MÔ PHỎNG · DỰNG BẰNG CHỮ THEO TRANG TRỢ GIÚP, ĐỌC 09.10.2026"
OA, GG, AN = "OPENAI HELP CENTER", "GEMINI APPS PRIVACY HUB", "ANTHROPIC · 28.08.2025"
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "BỐN NGHÌN RƯỠI CUỘC TRÒ CHUYỆN"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "day": "NHÓM PHÓNG VIÊN · MỘT CÂU TÌM KIẾM", "date": "07.2025"},
    {"type": "counter", "at": 1, "from": 0, "to": 4500, "prefix": "> ", "suffix": " CUỘC TRÒ CHUYỆN", "label": "CHATGPT · CÔNG KHAI TRÊN GOOGLE",
     "sub": {"text": "FAST COMPANY, QUA SEARCH ENGINE JOURNAL · 08.2025", "at": 1}},
    {"type": "ledger", "at": 2, "title": "TRONG ĐÓ CÓ", "rows": [{"k": "1", "v": "HỒ SƠ XIN VIỆC · TÊN THẬT", "at": 2},
                                                              {"k": "2", "v": "TÂM SỰ SỨC KHOẺ TINH THẦN", "at": 3},
                                                              {"k": "3", "v": "MÃ NGUỒN CÔNG TY", "at": 4}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "BỊ HACK", "at": 5, "fx": "strike", "strikeAt": [5, "cả"]}, {"text": "TỰ BẤM CHIA SẺ", "at": 6, "acc": True},
                                          {"text": "+ bật ô cho công cụ tìm kiếm thấy", "at": [6, "bật"], "sm": True}]},
    {"type": "broll", "at": 7, "vid": "6689151", "veil": 0.55, "illus": VM,
     "kin": [{"text": "Ô ẤY NGHĨA LÀ GÌ?", "at": 7, "acc": True}]},
    {"type": "date", "at": 8, "day": "OPENAI GỠ TÍNH NĂNG", "date": "31.07.2025"},
    {"type": "quote", "at": 10, "text": "…introduced too many opportunities for folks to accidentally share things they didn't intend to.",
     "by": "GIÁM ĐỐC AN NINH THÔNG TIN OPENAI · QUA TECHRADAR, 08.2025", "lbl": "TRÍCH DỊCH", "qline": 10},
    {"type": "question", "at": 12, "text": "AI có học từ\ncuộc trò chuyện của mình?"},
    {"type": "ledger", "at": 14, "title": "MỘT TIN NHẮN · BA NGẢ", "rows": [{"k": "1", "v": "TRÍ NHỚ CỦA TRỢ LÝ", "at": 15},
                                                                         {"k": "2", "v": "DỮ LIỆU DẠY PHIÊN BẢN SAU", "at": [15, "dữ"]},
                                                                         {"k": "3", "v": "MẮT MỘT CON NGƯỜI", "at": [15, "trước"]}]},
    {"type": "brand", "at": 16, "sub": "TỪNG NGẢ · VÀ CÁCH BẬT TẮT"},
]}

CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "HỌC VÀ TRÒ CHUYỆN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "HỌC VÀ\nTRÒ CHUYỆN", "sub": "HAI CHUYỆN KHÁC NHAU", "vid": "1085656", "illus": VM, "titleAt": [0, "trước"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "HUẤN LUYỆN", "at": 1, "acc": True}, {"text": "chữ khổng lồ · nhiều tuần, nhiều tháng", "at": [1, "trên"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "→ KHỐI SỐ CỐ ĐỊNH", "at": 2, "acc": True}, {"text": "trọng số", "at": [2, "trọng"], "sm": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "LÚC TRÒ CHUYỆN", "at": 3, "sm": True}, {"text": "KHÔNG THAY ĐỔI", "at": [3, "không"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "TỰ SỬA SAU MỖI CÂU", "at": 5, "fx": "strike", "strikeAt": [5, "câu"]}]},
    {"type": "broll", "at": 6, "vid": "34771078", "veil": 0.55, "illus": VM,
     "kin": [{"text": "ĐỌC LẠI CẢ ĐOẠN", "at": 6, "acc": True}, {"text": "mỗi lần trả lời", "at": [6, "mỗi"], "sm": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "CUỘC MỚI", "at": 8, "sm": True}, {"text": "TỜ GIẤY TRỐNG", "at": [8, "tờ"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "TỜ GIẤY CÓ GIỚI HẠN", "at": 9, "acc": True}, {"text": "đầu cuộc dài có thể bị cắt / tóm tắt", "at": 10, "sm": True}]},
    {"type": "slam", "at": 12, "text": "MÁY KHÔNG HỌC", "sub": "NÓ CHỈ ĐỌC · XONG CUỘC LÀ THÔI"},
    {"type": "question", "at": 14, "text": "“AI học từ tôi”\nlà sai?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "HAI CÁCH ĐI XA HƠN", "at": 15, "acc": True}, {"text": "cách thứ nhất: trí nhớ", "at": 16, "sm": True}]},
]}

CH["ch02"] = {"hud": {"k": "NGẢ 01", "t": "TRÍ NHỚ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "NGẢ THỨ NHẤT", "title": "TRÍ NHỚ", "sub": "MEMORY · THEO " + OA, "vid": "6963823", "illus": VM, "titleAt": [0, "nhiều"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "SỞ THÍCH · CHI TIẾT", "at": 1, "acc": True}, {"text": "từ các cuộc trò chuyện · theo " + OA, "at": [1, "chatgpt"], "sm": True}]},
    {"type": "ledger", "at": 3, "title": "TRÍ NHỚ LẤY TỪ", "rows": [{"k": "1", "v": "ĐIỀU BẠN BẢO NÓ GHI LẠI", "at": 3},
                                                                   {"k": "2", "v": "LỊCH SỬ TRÒ CHUYỆN CŨ", "at": [3, "lịch"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "“MÌNH ĂN CHAY”", "at": 4}, {"text": "→ THỰC ĐƠN KHÔNG THỊT", "at": [4, "tuần"], "acc": True}]},
    {"type": "slam", "at": 5, "text": "MỘT HỒ SƠ NHỎ VỀ BẠN", "sub": "GHI LẠI DẦN DẦN"},
    {"type": "kinetic", "at": 7, "items": [{"text": "MÁY TỰ QUYẾT", "at": 7, "acc": True}, {"text": "điều nó nhớ có thể thay đổi", "at": [7, "điều"], "sm": True}]},
    {"type": "file", "at": 9, "k": MOCK, "name": "Cài đặt → Trí nhớ", "desc": "Tên mục có thể khác theo gói / phiên bản",
     "rows": [{"k": "XEM", "v": "đang nhớ gì", "at": [10, "xem"]}, {"k": "XOÁ", "v": "từng mục", "at": [10, "xoá"]}, {"k": "TẮT", "v": "hẳn", "at": [10, "tắt"]}],
     "label": {"k": "LƯU Ý", "v": "NHẬT KÝ MỤC ĐÃ XOÁ CÓ THỂ GIỮ TỚI 30 NGÀY · " + OA, "at": 11}},
    {"type": "kinetic", "at": 12, "items": [{"text": "CHỈ PHỤC VỤ BẠN", "at": 12}, {"text": "NGẢ HAI: BÀI HỌC CHO PHIÊN BẢN SAU", "at": 13, "acc": True}]},
]}

CH["ch03"] = {"hud": {"k": "NGẢ 02", "t": "DỮ LIỆU HUẤN LUYỆN"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "2", "k": "NGẢ THỨ HAI", "title": "DỮ LIỆU\nHUẤN LUYỆN", "sub": "KHI CUỘC TRÒ CHUYỆN THÀNH BÀI HỌC", "vid": "38496193", "illus": VM, "titleAt": [0, "openai"]},
    {"type": "quote", "at": 1, "text": "ChatGPT, for instance, improves by further training on the conversations people have with it, unless you opt out.",
     "by": "OPENAI · HOW YOUR DATA IS USED TO IMPROVE MODEL PERFORMANCE (13.03.2026)", "lbl": "TRÍCH DỊCH", "qline": 1},
    {"type": "kinetic", "at": 2, "items": [{"text": "DỊCH VỤ CÁ NHÂN", "at": 2, "sm": True}, {"text": "MẶC ĐỊNH: CÓ THỂ DÙNG", "at": [2, "mặc"], "acc": True}]},
    {"type": "file", "at": 3, "k": MOCK, "name": "ChatGPT", "desc": "Settings → Data controls",
     "rows": [{"k": "CÔNG TẮC", "v": "*Improve the model for everyone*", "at": [3, "improve"]}, {"k": "TẮT", "v": "cuộc trò chuyện mới không dùng huấn luyện", "at": 4}],
     "label": {"k": "NGUỒN", "v": OA + " · DATA CONTROLS", "at": 3}},
    {"type": "file", "at": 5, "k": AN, "name": "Claude", "desc": "Gói cá nhân: Free · Pro · Max",
     "rows": [{"k": "TỰ CHỌN", "v": "cho dùng huấn luyện hay không", "at": 6}, {"k": "ĐỒNG Ý", "v": "giữ tới *5 năm*", "at": 7}, {"k": "KHÔNG", "v": "*30 ngày*", "at": [7, "nếu"]}],
     "label": {"k": "NGUỒN", "v": "ANTHROPIC · UPDATES TO OUR CONSUMER TERMS", "at": 5}},
    {"type": "file", "at": 8, "k": MOCK, "name": "Gemini", "desc": "Keep Activity · giữ lại hoạt động",
     "rows": [{"k": "TẮT + KHÔNG GỬI PHẢN HỒI", "v": "cuộc trò chuyện sau không dùng cải thiện mô hình", "at": 9}],
     "label": {"k": "NGUỒN", "v": GG, "at": 8}},
    {"type": "kinetic", "at": 11, "items": [{"text": "GÓI DOANH NGHIỆP", "at": 11, "sm": True}, {"text": "MẶC ĐỊNH KHÔNG HUẤN LUYỆN", "at": [11, "dữ"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "NGƯỜI DÙNG THƯỜNG", "at": 12, "sm": True}, {"text": "TẮT LÀ VIỆC CỦA MÌNH", "at": [12, "việc"], "acc": True}]},
    {"type": "broll", "at": 13, "vid": "5916730", "veil": 0.5, "illus": VM,
     "kin": [{"text": "DẶN TRƯỚC KHI GỬI", "at": 13, "acc": True}]},
    {"type": "question", "at": 14, "text": "Ngả thứ ba:\nai đọc?"},
]}

CH["ch04"] = {"hud": {"k": "NGẢ 03", "t": "MỘT CON NGƯỜI"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "3", "k": "NGẢ THỨ BA", "title": "MỘT\nCON NGƯỜI", "sub": "NGƯỜI ĐÁNH GIÁ", "vid": "13375774", "illus": VM, "titleAt": [0, "nhiều"]},
    {"type": "quote", "at": 2, "text": "A subset of chats are reviewed by human reviewers (including Google's trained service providers) to help improve Google services.",
     "by": GG, "lbl": "TRÍCH DỊCH", "qline": 2},
    {"type": "ledger", "at": 3, "title": "NGƯỜI ĐÁNH GIÁ LÀM GÌ", "rows": [{"k": "1", "v": "XEM CÂU TRẢ LỜI KÉM · SAI · GÂY HẠI", "at": 3},
                                                                        {"k": "2", "v": "GỢI Ý CÂU TRẢ LỜI TỐT HƠN", "at": [3, "gợi"]}]},
    {"type": "counter", "at": 5, "from": 0, "to": 3, "suffix": " NĂM", "label": "CHAT ĐÃ ĐƯỢC NGƯỜI XEM · KHÔNG XOÁ KHI BẠN XOÁ LỊCH SỬ",
     "sub": {"text": GG, "at": 5}},
    {"type": "quote", "at": 7, "text": "Please don't enter confidential information that you wouldn't want a reviewer to see…", "by": GG, "lbl": "TRÍCH DỊCH", "qline": 7},
    {"type": "kinetic", "at": 8, "items": [{"text": "CÂU THẬT LÒNG NHẤT", "at": 8, "acc": True}]},
    {"type": "ledger", "at": 9, "title": "DÙ ĐÃ TẮT / DÙNG TRÒ CHUYỆN TẠM THỜI", "srcnote": GG + " · " + OA,
     "rows": [{"k": "GEMINI", "v": "VẪN GIỮ 72 GIỜ", "at": 9}, {"k": "CHATGPT", "v": "BẢN SAO TỐI ĐA 30 NGÀY · AN TOÀN", "at": 10}]},
    {"type": "question", "at": 11, "text": "Khi đó là bí mật\ncủa cả một công ty?"},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "BA LẦN TRONG MỘT THÁNG"}, "bgm": {"mood": "calm", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "BA LẦN\nTRONG MỘT THÁNG", "sub": "SAMSUNG · NƯỚC Ý · 2023", "vid": "38493702", "illus": VM, "titleAt": [0, "tháng"]},
    {"type": "ledger", "at": 1, "title": "SAMSUNG · BỘ PHẬN BÁN DẪN · 04.2023", "srcnote": "BLOOMBERG, QUA THE REGISTER · 02.05.2023",
     "rows": [{"k": "1", "v": "DÁN MÃ NGUỒN NỘI BỘ", "at": 1}, {"k": "2", "v": "DÁN GHI CHÉP CUỘC HỌP", "at": 2},
              {"k": "=", "v": "3 LẦN TRONG MỘT THÁNG", "at": 3}]},
    {"type": "date", "at": 4, "day": "TẠM CẤM AI TẠO SINH TRÊN MÁY TÍNH CÔNG TY", "date": "05.2023"},
    {"type": "kinetic", "at": 5, "items": [{"text": "AI HỌC NGAY", "at": 5, "fx": "strike", "strikeAt": [5, "ngay"]},
                                          {"text": "MÁY CHỦ BÊN NGOÀI", "at": 6, "acc": True}, {"text": "khó lấy lại · khó xoá · có thể lộ", "at": [6, "khó"], "sm": True}]},
    {"type": "date", "at": 8, "day": "Ý TẠM CHẶN CHATGPT", "date": "31.03.2023"},
    {"type": "ledger", "at": 9, "title": "LÝ DO CỦA CƠ QUAN BẢO VỆ DỮ LIỆU Ý", "srcnote": "PRIVACYLAWS.COM · FOX BUSINESS",
     "rows": [{"k": "1", "v": "NGƯỜI DÙNG KHÔNG ĐƯỢC THÔNG BÁO ĐỦ", "at": 9}, {"k": "2", "v": "THIẾU CƠ SỞ PHÁP LÝ ĐỂ HUẤN LUYỆN", "at": [9, "thu"]}]},
    {"type": "timeline", "at": 10, "items": [{"year": "31.03", "text": "Ý *chặn*", "at": 10}, {"year": "25.04", "text": "OpenAI cho *tắt lịch sử*", "at": 11},
                                            {"year": "28.04", "text": "Ý *mở lại*", "at": [10, "chatgpt"]}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "TIỀN THÂN CỦA CÔNG TẮC", "at": 12, "acc": True}]},
    {"type": "broll", "at": 14, "vid": "13375774", "ms": 4, "veil": 0.5, "illus": VM,
     "kin": [{"text": "BẤM GỬI RỒI", "at": 14, "sm": True}, {"text": "HỘP THƯ CỦA NGƯỜI KHÁC", "at": 15, "acc": True}]},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "Ở VIỆT NAM"}, "bgm": {"mood": "warm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "Ở VIỆT NAM", "sub": "LUẬT BẢO VỆ DỮ LIỆU CÁ NHÂN", "vid": "7504263", "illus": VM, "titleAt": [0, "ở"]},
    {"type": "date", "at": [0, "luật"], "day": "LUẬT 91/2025/QH15 CÓ HIỆU LỰC", "date": "01.01.2026"},
    {"type": "timeline", "at": 2, "items": [{"year": "07.2023", "text": "*Nghị định 13*", "at": 2}, {"year": "06.2025", "text": "Quốc hội *thông qua luật*", "at": [2, "giờ"]},
                                           {"year": "01.2026", "text": "Luật *có hiệu lực*", "at": [2, "luật"]}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "ĐÚNG PHẠM VI", "at": 3, "acc": True}, {"text": "ĐÚNG MỤC ĐÍCH", "at": [3, "mục"], "acc": True}]},
    {"type": "counter", "at": 4, "from": 0, "to": 10, "prefix": "× ", "label": "MỨC PHẠT TỐI ĐA · MUA BÁN DỮ LIỆU CÁ NHÂN", "sub": {"text": "SO VỚI KHOẢN THU TỪ VI PHẠM", "at": 4}},
    {"type": "slam", "at": 6, "text": "THỨ CHƯA TỪNG GÕ VÀO", "sub": "DỄ BẢO VỆ NHẤT"},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "BẬT TẮT TỪNG NGẢ"}, "bgm": {"mood": "upbeat", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "BẬT TẮT\nTỪNG NGẢ", "sub": "TÊN NÚT CÓ THỂ KHÁC THEO GÓI / VÙNG / PHIÊN BẢN", "vid": "6963823", "ms": 20, "illus": VM, "titleAt": [0, "quay"]},
    {"type": "file", "at": 2, "k": MOCK, "name": "Ngả 1 · Trí nhớ", "desc": "Cài đặt → Cá nhân hoá / Trí nhớ",
     "rows": [{"k": "XEM", "v": "đang nhớ gì về bạn", "at": 3}, {"k": "XOÁ / TẮT", "v": "những gì không muốn giữ", "at": [3, "xoá"]}]},
    {"type": "file", "at": 4, "k": MOCK, "name": "Ngả 2 · Huấn luyện", "desc": "Mỗi ứng dụng một công tắc",
     "rows": [{"k": "CHATGPT", "v": "*Improve the model for everyone* · Data controls", "at": 4}, {"k": "CLAUDE", "v": "cài đặt huấn luyện · Privacy", "at": 5},
              {"k": "GEMINI", "v": "*Keep Activity*", "at": 6}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "NGẢ 3 · CON NGƯỜI", "at": 7, "sm": True}, {"text": "KHÔNG CÓ CÔNG TẮC", "at": [7, "không"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "TRÒ CHUYỆN TẠM THỜI", "at": 9, "acc": True}, {"text": "không lưu lịch sử · không huấn luyện · vẫn giữ ngắn hạn", "at": [9, "không"], "sm": True}]},
    {"type": "ledger", "at": 10, "title": "5 THỨ KHÔNG DÁN VÀO CHATBOT NÀO",
     "rows": [{"k": "1", "v": "SỐ CĂN CƯỚC", "at": 11}, {"k": "2", "v": "MẬT KHẨU · MÃ XÁC THỰC", "at": [11, "mật"]},
              {"k": "3", "v": "SỐ TÀI KHOẢN · SỐ THẺ", "at": [11, "tài"]}, {"k": "4", "v": "THÔNG TIN RIÊNG CỦA NGƯỜI KHÁC", "at": 12},
              {"k": "5", "v": "TÀI LIỆU NỘI BỘ NƠI LÀM VIỆC", "at": [12, "tài"]}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "NÚT CHIA SẺ", "at": 13, "sm": True}, {"text": "= CÁNH CỬA MỞ", "at": 14, "acc": True}]},
    {"type": "slam", "at": 15, "text": "KHÔNG HỌC TỪNG CÂU", "sub": "NHƯNG ĐI XA HƠN CUỘC TRÒ CHUYỆN RẤT NHIỀU"},
    {"type": "question", "at": 17, "text": "Bạn từng dán thứ gì\nmà giờ thấy hơi lo?"},
]}

SPEC = {
    "title": "Bạn Gõ Gì Vào Chatbot, Ai Được Đọc? AI Có Học Từ Đó?",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["chatgpt", "gemini", "claude", "huấn", "luyện", "nhớ", "riêng", "tư"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(8)],
    "youtube": {
        "titles": ["Bạn Gõ Gì Vào Chatbot, Ai Được Đọc? AI Có Học Từ Đó?",
                   "Những Gì Bạn Gõ Vào ChatGPT, Gemini, Claude Đi Đâu? Ba Ngả Và Cách Tắt Từng Ngả",
                   "4.500 Cuộc Trò Chuyện ChatGPT Hiện Trên Google: Quyền Riêng Tư Khi Dùng Chatbot"],
        "summary": "Tháng 7/2025, hơn 4.500 cuộc trò chuyện ChatGPT được chia sẻ hiện công khai trên Google. AI có học từ những gì bạn gõ không? "
                   "Video tách ba ngả một tin nhắn có thể đi — trí nhớ của trợ lý, dữ liệu huấn luyện, và người đánh giá là con người — theo đúng "
                   "trang trợ giúp của OpenAI, Google và Anthropic (đọc 09/10/2026), kể chuyện Samsung 2023, Ý tạm chặn ChatGPT, Luật Bảo vệ dữ liệu "
                   "cá nhân của Việt Nam, và chỉ cách bật tắt từng ngả.",
        "more": ["Cài đặt và tên nút có thể khác theo gói, vùng và phiên bản; thông tin theo trang trợ giúp của từng hãng đọc ngày 09/10/2026. "
                 "Menu ứng dụng trong video là mô phỏng dựng bằng chữ, không phải ảnh chụp giao diện. Lời trích được đọc bằng giọng máy của kênh."],
        "chapter_titles": {"ch00": "Mở đầu: 4.500 cuộc trò chuyện trên Google", "ch01": "Học và trò chuyện là hai chuyện khác nhau",
                           "ch02": "Ngả 1: trí nhớ", "ch03": "Ngả 2: dữ liệu huấn luyện", "ch04": "Ngả 3: người đánh giá",
                           "ch05": "Samsung và nước Ý (2023)", "ch06": "Luật Bảo vệ dữ liệu cá nhân Việt Nam", "ch07": "Bật tắt từng ngả + 5 thứ không nên dán"},
        "sources": ["https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt",
                    "https://help.openai.com/en/articles/8914046-temporary-chat-in-chatgpt",
                    "https://help.openai.com/en/articles/8590148-memory-faq",
                    "https://openai.com/policies/how-your-data-is-used-to-improve-model-performance/",
                    "https://support.google.com/gemini/answer/13594961?hl=en",
                    "https://www.anthropic.com/news/updates-to-our-consumer-terms",
                    "https://openai.com/index/new-ways-to-manage-your-data-in-chatgpt",
                    "https://www.searchenginejournal.com/openai-is-pulling-shared-chatgpt-chats-from-google-search/552671/",
                    "https://www.theregister.com/2023/05/02/samsung_generative_ai_ban/",
                    "https://www.privacylaws.com/news/italy-s-garante-imposes-and-then-withdraws-a-ban-on-chatgpt/",
                    "https://luatvietnam.vn/tin-van-ban-moi/da-co-luat-bao-ve-du-lieu-ca-nhan-2025-so-91-2025-qh15-186-102925-article.html"],
        "hashtags": ["AI", "QuyềnRiêngTư", "ChatGPT", "Gemini", "MindInTheMachine"],
        "tags": ["AI có học từ cuộc trò chuyện", "ChatGPT quyền riêng tư", "tắt huấn luyện ChatGPT", "Gemini Keep Activity", "Claude quyền riêng tư",
                 "trò chuyện tạm thời", "bộ nhớ ChatGPT", "Luật bảo vệ dữ liệu cá nhân", "an toàn khi dùng AI", "trí tuệ nhân tạo"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}


# Nhạc chốt tay (PM 09/10): tự chọn theo mood ra 70% trùng mim-ai-jobs; bộ 5 bài này Jaccard tối đa 0,27 với 6 video MIM trước.
BGM_PICKS = {"ch00.0": "equatorial_complex.mp3", "ch01.0": "chill_wave.mp3", "ch02.0": "fluidscape.mp3", "ch03.0": "bit_shift.mp3",
             "ch04.0": "equatorial_complex.mp3", "ch05.0": "fluidscape.mp3", "ch06.0": "chill_wave.mp3", "ch07.0": "hackbeat.mp3"}
OUT = D.parents[2] / "output" / "long" / D.name


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "bgm_picks.json").write_text(json.dumps(BGM_PICKS, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")


if __name__ == "__main__":
    main()
