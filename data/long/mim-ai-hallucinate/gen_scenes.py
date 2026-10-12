"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #4 "Vì Sao AI Bịa Mà Vẫn Rất Tự Tin?".

    python data/long/mim-ai-hallucinate/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (bản 2, đã kiểm chứng) + factcheck.md. Dữ kiện + nguồn: docs/channels/mind-in-the-machine/2026-10-07-long-04-research.md.
Ảnh: chỉ PD / CC0 / CC BY (kênh MIM không nhận BY-SA — build_long kiểm lại lúc tải). Clip: Pexels (ngang), mọi clip gắn
"VIDEO MINH HỌA"; tải bằng `python motion/long/pexels.py get mim-ai-hallucinate <id> ...`.
Quy tắc riêng của video này (factcheck mục 2 + 5):
  - Hồ sơ toà: ảnh chụp màn hình ChatGPT ở Phụ lục B (ECF 54) CHỈ dựng lại bằng chữ (cảnh chat/quote), nhãn "TRÍCH HỒ SƠ TOÀ",
    không chiếu bản scan, không ghi ngày hỏi (toà: "no date is given for the queries"). Không logo ChatGPT/OpenAI/Avianca,
    không mặt luật sư.
  - Tên sản phẩm trên hình CHỈ như báo cáo EBU/BBC ghi: Giáo hoàng = ChatGPT (Yle 28.05), Gemini (NOS 29.05), Copilot (NOS 30.05);
    khung chat Giáo hoàng = Copilot (NOS/NPO, 30.05.2025); phi hành gia = Gemini (Yle, tiếng Phần Lan) — KHÔNG dùng khung
    Gemini RTP tr. 26. KHÔNG hiện bảng 76/37/36/30% theo trợ lý. Lời đọc không gắn lỗi cho tên trợ lý nào.
  - Cảnh hẹn trước: ba ngày sinh "03-07 / 15-06 / 01-01" dựng ở ch00 (cảnh 20) và trả ở ch07 (chat 3 lần hỏi + "MÙA THU").
  - Ảnh Vatican CC0 = Jebulon 2013 (ẢNH MINH HỌA); phiếu Scantron 815-E (CC0) = ẢNH MINH HỌA, phiếu Mỹ, không phải phiếu THPT.
  - Dòng số ngắn trong kinetic ghi "fx": "rise" (tránh "scramble" mặc định khi at sát đầu cảnh).
Nhạc: chốt tay trong output/long/mim-ai-hallucinate/bgm_picks.json (ghi bởi file này) — 5 bài MIM: ouroboros, ether_vox, wallpaper,
bit_shift, hackbeat. Jaccard: mim-ai-70 2/9, mim-ai-jobs 3/11, mim-ai-voice 1/9 (ngưỡng variety 35%).
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
OUT = D.parents[2] / "output" / "long" / D.name

IMGS = {
    "sdny": "File:U.S. District Court - Southern District of New York (48129021526).jpg",            # CC BY 2.0 · Ajay Suresh · 21.06.2019
    "moynihan": "File:Daniel Patrick Moynihan United States Courthouse (55314001073).jpg",           # CC BY 4.0 · 26.05.2026
    "scantron": "File:Scantron form 815-E Half Testing Sheet.png",                                    # CC0 · ẢNH MINH HỌA (phiếu Mỹ)
    "starliner": "File:Boeing's Starliner Spacecraft Approaches the International Space Station (iss071e170983).jpg",  # PD NASA · 06.06.2024
    "vatican": "File:Saint Peter's Basilica Dome from Square Garden Vatican 14.jpg",                  # CC0 · Jebulon · 21.08.2013
}

SAY = {   # chữ hiển thị -> cách đọc (phụ đề giữ chữ gốc); "=X" = khớp đúng hoa/thường. Khoá viết thường, NFC.
    "=AI": "ây ai", "=GPT-4": "gi pi ti bốn", "=GPT-3.5": "gi pi ti ba chấm năm", "=ANTV": "A-en-ti-vi", "=VTV": "Vê-tê-vê",
    "=PISA": "Pi-da", "=OECD": "Ô-e-xê-đê",
    "roberto": "Rô-be-tô", "mata": "Ma-ta", "new": "Niu", "york": "Doóc", "varghese": "Vác-ghít", "china": "Chai-na",
    "southern": "Xa-thơn", "airlines": "E-lai", "westlaw": "Uét-lo", "lexisnexis": "Léc-xít Néc-xít", "kevin": "Ke-vin",
    "castel": "Ca-xten", "steven": "Xti-vần", "schwartz": "Soóc-xơ", "chatgpt": "chát gi pi ti", "chatbot": "chát bót",
    "openai": "Ô-pần Ây-ai", "georgia": "Gioóc-gia", "adam": "A-đam", "kalai": "Ca-lai", "william": "Uy-li-am",
    "walters": "Oan-tơ", "esther": "Ét-xtơ", "wilder": "Oai-đơ", "bbc": "Bi-bi-xi", "nasa": "Na-xa", "damien": "Đa-mi-en",
    "charlotin": "Sác-lô-tanh",
}

VM = "VIDEO MINH HỌA"
HST = {"text": "TRÍCH HỒ SƠ TOÀ"}            # thẻ trên mọi cảnh dựng lại từ văn bản toà (Phụ lục B, ECF 31/54)
APPB = "PHỤ LỤC B · ECF 54 · DỰNG LẠI BẰNG CHỮ"

# Nhạc: chốt tay (ít trùng với 3 video MIM trước), xem docstring.
BGM_PICKS = {"ch00.0": "ouroboros.mp3", "ch01.0": "ether_vox.mp3", "ch02.0": "wallpaper.mp3", "ch03.0": "bit_shift.mp3",
             "ch04.0": "ouroboros.mp3", "ch05.0": "hackbeat.mp3", "ch06.0": "ouroboros.mp3", "ch07.0": "wallpaper.mp3",
             "ch08.0": "ether_vox.mp3"}

CH = {}

# ---------------- CH00 · Sáu vụ án không có thật ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "SÁU VỤ ÁN KHÔNG CÓ THẬT"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "NEW YORK · TOÀ ÁN LIÊN BANG MỸ", "date": "01.03.2023"},
    {"type": "broll", "at": 1, "vid": "3701075", "veil": 0.5, "illus": VM,
     "kin": [{"text": "THÂN CHỦ: ROBERTO MATA", "at": 1, "sm": True},
             {"text": "XE ĐẨY KIM LOẠI ĐẬP VÀO ĐẦU GỐI", "at": [1, "xe"], "acc": True},
             {"text": "trên một chuyến bay", "at": [1, "trên"], "sm": True}]},
    {"type": "file", "at": 2, "k": "BẢN LẬP LUẬN · 01.03.2023", "name": "Mata v. Avianca", "desc": "Toà án Liên bang Quận Nam New York",
     "rows": [{"k": "TÊN VỤ", "v": "*có*", "at": 2}, {"k": "TÊN TOÀ", "v": "*có*", "at": [2, "có", 1]},
              {"k": "TRÍCH DẪN", "v": "*nguyên văn*", "at": [2, "có", 2]}]},
    {"type": "broll", "at": 3, "vid": "8731303", "veil": 0.5, "illus": VM,
     "kin": [{"text": "HAI TUẦN SAU · 15.03.2023", "at": 3, "sm": True, "fx": "rise"},
             {"text": "KHÔNG TÌM THẤY PHẦN LỚN ÁN LỆ", "at": [3, "không"], "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "TOÀ CŨNG KHÔNG THẤY", "at": 4},
                                          {"text": "LỆNH NỘP BẢN SAO", "at": [4, "ra"]},
                                          {"text": "chỉ nộp những trích đoạn", "at": [4, "các"], "sm": True, "acc": True}]},
    {"type": "kinetic", "at": 5, "bg": "sdny", "items": [{"text": "ÁN LỆ DẪN ĐẦU TIÊN: VARGHESE", "at": 5, "sm": True},
                                                       {"text": "THƯ KÝ TOÀ PHÚC THẨM KHU VỰC 11", "at": [5, "thư"]},
                                                       {"text": "TỪ 2010: KHÔNG AI TÊN VARGHESE", "at": [5, "từ"], "acc": True}],
     "label": {"k": "TOÀ MOYNIHAN · MANHATTAN", "v": "ẢNH 2019", "at": 5}},
    {"type": "date", "at": 6, "day": "THẨM PHÁN P. KEVIN CASTEL · LỆNH GIẢI TRÌNH", "date": "04.05.2023",
     "label": {"k": "ECF 31", "v": "“AN UNPRECEDENTED CIRCUMSTANCE”", "at": [6, "tình"]}},
    {"type": "quote", "at": 7, "text": "Six of the submitted cases appear to be bogus judicial decisions with bogus quotes and bogus internal citations.",
     "by": "THẨM PHÁN P. KEVIN CASTEL · LỆNH 04.05.2023 (ECF 31)", "lbl": "TRÍCH DỊCH", "qline": 7},
    {"type": "broll", "at": 8, "vid": "34771078", "veil": 0.45, "illus": VM,
     "kin": [{"text": "CUỐI THÁNG 5 · 25.05.2023", "at": 8, "sm": True, "fx": "rise"},
             {"text": "LUẬT SƯ THỪA NHẬN: ĐÃ TRA CỨU BẰNG CHATGPT", "at": [8, "anh"], "acc": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "KÈM ẢNH CHỤP MÀN HÌNH", "at": 9},
                                          {"text": "ANH TỪNG HỎI LẠI NÓ", "at": [9, "từng"], "acc": True}]},
    {"type": "chat", "at": 10, "head": APPB, "tag": HST, "msgs": [
        {"who": "u", "text": "Is varghese a real case", "at": 10},
        {"who": "m", "text": "Yes, Varghese v. China Southern Airlines Co Ltd, 925 F.3d 1339 (11th Cir. 2019) is a real case.", "at": 11},
        {"who": "u", "text": "What is your source", "at": 12}]},
    {"type": "quote", "at": 13, "text": "I apologize for the confusion earlier. Upon double-checking, I found that the case Varghese v. China Southern "
                                       "Airlines Co. Ltd., 925 F.3d 1339 (11th Cir. 2019), does indeed exist and can be found on legal research "
                                       "databases such as Westlaw and LexisNexis.",
     "by": "PHỤ LỤC B · PHÁN QUYẾT VỀ CHẾ TÀI, 22.06.2023 · DỰNG LẠI BẰNG CHỮ", "lbl": "TRÍCH HỒ SƠ TOÀ", "qline": 13},
    {"type": "chat", "at": 14, "head": APPB, "tag": HST, "msgs": [
        {"who": "u", "text": "Are the other cases you provided fake", "at": 14},
        {"who": "m", "text": "No, the other cases I provided are real and can be found in reputable legal databases such as LexisNexis and Westlaw.",
         "at": 15}]},
    {"type": "slam", "at": 16, "text": "SÁU VỤ KHÔNG HỀ TỒN TẠI"},
    {"type": "question", "at": 17, "text": "Vì sao một cỗ máy bịa ra sáu vụ án,\nrồi còn quả quyết là có thật?"},
    {"type": "kinetic", "at": 18, "items": [{"text": "MÌNH HẸN BẠN MỘT CẢNH NHỎ", "at": 18, "sm": True},
                                           {"text": "Ở CUỐI VIDEO", "at": [18, "ở"], "acc": True}]},
    {"type": "kinetic", "at": 19, "items": [{"text": "HỎI MÁY NGÀY SINH", "at": 19, "sm": True},
                                           {"text": "MỘT NGƯỜI TRONG CHÍNH NHÓM MÌNH", "at": [19, "một", 1]},
                                           {"text": "BA LẦN LIỀN", "at": [19, "ba"], "acc": True}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "03-07", "at": 20, "fx": "rise"},
                                           {"text": "15-06", "at": [20, "ba"], "fx": "rise"},
                                           {"text": "01-01", "at": [20, "khác"], "fx": "rise"},
                                           {"text": "KHÔNG NGÀY NÀO ĐÚNG", "at": [20, "không"], "acc": True, "sm": True}]},
    {"type": "kinetic", "at": 21, "items": [{"text": "MẸO ĐƠN GIẢN NHẤT", "at": 21, "acc": True},
                                           {"text": "để bắt một cỗ máy đang bịa", "at": [21, "để"], "sm": True}]},
    {"type": "brand", "at": 22, "sub": "AI · BỊA · MÀ VẪN CHẮC NỊCH"},
]}

# ---------------- CH01 · Viết như thật ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "VIẾT NHƯ THẬT"}, "bgm": {"mood": "curious", "gain": 0.14}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "VIẾT\nNHƯ THẬT", "sub": "MÔ HÌNH NGÔN NGỮ · ĐOÁN MẨU CHỮ", "vid": "2752278",
     "titleAt": [0, "thử"]},
    {"type": "chat", "at": 1, "head": "TRÒ ĐIỀN CHỮ · MINH HỌA", "msgs": [
        {"who": "u", "text": "Thủ đô của Việt Nam là…", "at": 1},
        {"who": "m", "text": "Hà Nội.", "at": [1, "hà"]}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "HÀNG TRIỆU LẦN TRONG SÁCH BÁO", "at": 2, "fx": "rise"},
                                          {"text": "MÁY CŨNG ĐIỀN ĐÚNG", "at": [2, "nên"], "acc": True}]},
    {"type": "chat", "at": 3, "head": "TRÒ ĐIỀN CHỮ · MINH HỌA", "msgs": [
        {"who": "u", "text": "Sinh nhật của người bạn thân nhất của mình là ngày…", "at": 3}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "BẠN KHỰNG LẠI", "at": 4},
                                          {"text": "“MÌNH” LÀ AI?", "at": [4, "vì"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "MỘT CỖ MÁY ĐOÁN CHỮ", "at": 5, "sm": True},
                                          {"text": "KHÔNG CẦN BIẾT", "at": [5, "không"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "“NGÀY” → MỘT CON SỐ", "at": 6},
                                          {"text": "→ “THÁNG” → MỘT CON SỐ NỮA", "at": [6, "rồi"], "acc": True}]},
    {"type": "chat", "at": 7, "stream": True, "head": "MINH HỌA · ĐOÁN TỪNG MẨU CHỮ", "msgs": [
        {"who": "u", "text": "Sinh nhật của người bạn thân nhất của mình là ngày…", "at": 7},
        {"who": "m", "text": "…ngày 12 tháng 3. Chúc mừng sinh nhật!", "at": [7, "ngày"], "dur": 1.6}]},
    {"type": "nn", "at": 8, "fwdAt": [10, "rồi"], "label": {"k": "NÓI ĐƠN GIẢN", "v": "ĐỌC RẤT NHIỀU CHỮ → ĐOÁN MẨU TIẾP THEO", "at": 8}},
    {"type": "kinetic", "at": 11, "items": [{"text": "HÌNH DÁNG CÂU CHỮ: HỌC RẤT GIỎI", "at": 11},
                                           {"text": "ĐÚNG HAY SAI: KHÔNG NẰM Ở HÌNH DÁNG", "at": [11, "nhưng"], "acc": True}]},
    {"type": "broll", "at": 12, "vid": "8731388", "veil": 0.5, "illus": VM,
     "kin": [{"text": "NHÌN LẠI NHỮNG ÁN LỆ GIẢ", "at": 12, "sm": True},
             {"text": "TRÔNG RẤT ĐÚNG KHUÔN", "at": [13, "trông"], "acc": True}]},
    {"type": "file", "at": 14, "k": "PHÁN QUYẾT GIẢ · ECF 54", "name": "Varghese v.\nChina Southern Airlines", "desc": "925 F.3d 1339 (11th Cir. 2019)",
     "tag": HST, "rows": [{"k": "THẨM PHÁN", "v": "tên *người có thật*", "at": 14},
                         {"k": "SỐ TRANG", "v": "có thật · nhưng là *vụ khác hẳn*", "at": 15},
                         {"k": "LẬP LUẬN", "v": "*“gibberish”*", "at": 16}],
     "stamp": {"text": "KHÔNG CÓ THẬT", "at": [15, "khác"], "x": 860, "y": 640, "rot": -10}},
    {"type": "quote", "at": 17, "text": "Its legal analysis is gibberish.", "by": "THẨM PHÁN P. KEVIN CASTEL · PHÁN QUYẾT 22.06.2023 (ECF 54)",
     "lbl": "TRÍCH DỊCH", "qline": 17},
    {"type": "slam", "at": 18, "text": "TRƠN TRU ≠ ĐÚNG"},
    {"type": "kinetic", "at": 19, "items": [{"text": "“UPON DOUBLE-CHECKING…”", "at": 19, "sm": True},
                                           {"text": "CŨNG CHỈ LÀ CÂU ĐƯỢC ĐOÁN", "at": [19, "cũng"], "acc": True},
                                           {"text": "nghe hợp lý, ở đúng chỗ người ta hay nói", "at": [19, "một"], "sm": True}]},
    {"type": "question", "at": 20, "text": "Đọc nhiều hơn bất kỳ ai,\nsao máy vẫn đoán sai?"},
    {"type": "kinetic", "at": 21, "items": [{"text": "2025 · MỘT NHÓM NGHIÊN CỨU", "at": 21, "sm": True, "fx": "rise"},
                                           {"text": "BẮT ĐẦU TỪ MỘT LUẬN ÁN TIẾN SĨ", "at": [21, "bắt"], "acc": True}]},
]}

# ---------------- CH02 · Những điều chỉ gặp một lần ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "NHỮNG ĐIỀU CHỈ GẶP MỘT LẦN"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "NHỮNG ĐIỀU\nCHỈ GẶP MỘT LẦN", "sub": "KALAI ET AL. · OPENAI + GEORGIA TECH · 09.2025",
     "vid": "1580502", "titleAt": [0, "tháng"]},
    {"type": "kinetic", "at": [0, "công"], "items": [{"text": "“WHY LANGUAGE MODELS HALLUCINATE”", "at": [0, "công"], "sm": True},
                                                    {"text": "VÌ SAO MÔ HÌNH NGÔN NGỮ BỊ ẢO GIÁC", "at": [0, "vì"], "acc": True},
                                                    {"text": "Kalai · Nachum · Zhang (OpenAI) · Vempala (Georgia Tech) · 09.2025", "at": [0, "vì"], "sm": True}]},
    {"type": "kinetic", "at": 1, "items": [{"text": "“ẢO GIÁC” · HALLUCINATION", "at": 1, "acc": True},
                                          {"text": "những câu sai mà nghe rất hợp lý", "at": [1, "những"], "sm": True}]},
    {"type": "kinetic", "at": 2, "items": [{"text": "HỎI BA CHATBOT PHỔ BIẾN", "at": 2, "sm": True},
                                          {"text": "LUẬN ÁN TIẾN SĨ CỦA ADAM KALAI TÊN GÌ?", "at": [2, "luận"], "acc": True},
                                          {"text": "người đứng tên đầu tiên của bài báo", "at": [2, "người"], "sm": True}]},
    {"type": "ledger", "at": 3, "title": "BA CỖ MÁY · BA ĐÁP ÁN", "srcnote": "KALAI ET AL. 2025 · BẢNG 1 · THỬ 09.05.2025, KHÔNG TÌM WEB",
     "rows": [{"k": "ĐÁP ÁN 1", "v": "CMU · 2002", "at": [3, "tên"]}, {"k": "ĐÁP ÁN 2", "v": "HARVARD · 2005", "at": [3, "trường"]},
              {"k": "ĐÁP ÁN 3", "v": "MIT · 2007", "at": [3, "năm"]}],
     "total": {"k": "THẬT", "v": "2001 · KHÔNG CÁI NÀO ĐÚNG", "at": 4}},
    {"type": "kinetic", "at": 5, "items": [{"text": "HAI LOẠI SỰ THẬT", "at": 5, "acc": True, "fx": "rise"},
                                          {"text": "đặt cạnh nhau · hình 1 của bài báo", "at": [5, "đặt"], "sm": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "CÓ QUY LUẬT: CHÍNH TẢ", "at": 6, "fx": "rise"},
                                          {"text": "đọc đủ nhiều → nắm quy luật → gần như không viết sai", "at": [6, "đọc"], "sm": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "KHÔNG CÓ QUY LUẬT: NGÀY SINH", "at": 7, "acc": True, "fx": "rise"},
                                          {"text": "không suy ra được · chỉ biết nếu đã đọc thấy và nhớ được", "at": 8, "sm": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "MỘT MỐC DỄ HIỂU", "at": 9, "acc": True, "fx": "rise"},
                                          {"text": "ví dụ giả sử của các tác giả", "at": [9, "các"], "sm": True}]},
    {"type": "counter", "at": 10, "from": 0, "to": 20, "suffix": "%", "label": "SỐ NGÀY SINH CHỈ XUẤT HIỆN ĐÚNG MỘT LẦN TRONG DỮ LIỆU",
     "sub": {"text": "GIẢ SỬ · VÍ DỤ CỦA KALAI ET AL. 2025", "at": 10}},
    {"type": "slam", "at": 11, "text": "SAI ÍT NHẤT KHOẢNG 20%", "sub": "MÔ HÌNH GỐC · CÂU HỎI VỀ NGÀY SINH · THEO TÍNH TOÁN CỦA BÀI BÁO"},
    {"type": "kinetic", "at": 12, "items": [{"text": "GIỜ NGHĨ TỚI TIẾNG VIỆT", "at": 12},
                                           {"text": "suy luận của kênh, không phải của bài báo", "at": [12, "đây"], "sm": True, "acc": True}]},
    {"type": "broll", "at": 13, "vid": "9198046", "veil": 0.5, "illus": VM,
     "kin": [{"text": "CHI TIẾT NHỎ CỦA VĂN HỌC VIỆT", "at": 13, "sm": True},
             {"text": "ÍT HƠN RẤT NHIỀU TRÊN MẠNG", "at": [13, "ít"], "acc": True}]},
    {"type": "broll", "at": 14, "vid": "1580502", "ms": 20, "veil": 0.6, "illus": VM,
     "kin": [{"text": "ANTV PHẢN ÁNH · 22.12.2024", "at": 14, "sm": True, "fx": "rise"},
             {"text": "“NGƯỜI LÁI ĐÒ SÔNG ĐÀ” · NGUYỄN TUÂN", "at": [14, "lái"]},
             {"text": "SAI TÊN NHÂN VẬT NGƯỜI LÁI ĐÒ", "at": [14, "thông"], "acc": True}]},
    {"type": "ledger", "at": 15, "title": "ANTV PHẢN ÁNH · 22.12.2024", "srcnote": "THEO ANTV · BÀI KHÔNG GHI MÔ HÌNH, NGÀY THỬ",
     "rows": [{"k": "“NGƯỜI LÁI ĐÒ SÔNG ĐÀ”", "v": "SAI TÊN NHÂN VẬT", "at": 15},
              {"k": "“THƯƠNG NHỚ MƯỜI HAI”", "v": "SAI TÊN CÁC CHƯƠNG", "at": [15, "nó"]}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "KHÔNG NÓI “TÔI KHÔNG BIẾT”", "at": 16, "fx": "rise"},
                                           {"text": "VẪN TRẢ LỜI · GIỌNG RẤT CHẮC CHẮN", "at": [16, "nó"], "acc": True}]},
    {"type": "question", "at": 17, "text": "Vì sao máy\nkhông nói “không biết”?"},
]}

# ---------------- CH03 · Kỳ thi không trừ điểm ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "KỲ THI KHÔNG TRỪ ĐIỂM"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "KỲ THI\nKHÔNG TRỪ ĐIỂM", "sub": "TRẮC NGHIỆM · TỐT NGHIỆP THPT", "vid": "37779521",
     "illus": VM, "titleAt": [0, "ở"]},
    {"type": "print", "at": 1, "img": "scantron", "tone": "color", "maxH": 640, "caption": "PHIẾU TRẮC NGHIỆM (MỸ) · ẢNH MINH HỌA",
     "illus": "ẢNH MINH HỌA · KHÔNG PHẢI PHIẾU THI THPT",
     "side": {"k": "LỜI KHUYÊN QUEN", "h": "Không biết\nthì cứ khoanh", "lines": [
         {"text": "Khoanh bừa: *còn cơ hội trúng*", "at": 2},
         {"text": "Bỏ trống: *chắc chắn mất điểm*", "at": [2, "bỏ"]}]}},
    {"type": "kinetic", "at": 3, "items": [{"text": "BÀI BÁO 2025", "at": 3, "sm": True, "fx": "rise"},
                                          {"text": "MÁY ĐANG ĐƯỢC CHẤM ĐÚNG KIỂU ẤY", "at": [3, "các"], "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "10 BÀI KIỂM TRA PHỔ BIẾN", "at": 4, "fx": "rise"},
                                          {"text": "GPQA · MMLU-Pro · IFEval · Omni-MATH · BBH", "at": [4, "phổ"], "sm": True},
                                          {"text": "MATH L5 · MuSR · SWE-bench · HLE · WildBench", "at": [4, "xếp"], "sm": True}]},
    {"type": "slam", "at": 5, "text": "9 / 10", "sub": "KHÔNG CHO CHÚT ĐIỂM NÀO KHI MÁY NÓI “TÔI KHÔNG BIẾT” · KALAI ET AL. 2025, BẢNG 2"},
    {"type": "quote", "at": 6, "text": "…language models are optimized to be good test-takers, and guessing when uncertain improves test performance.",
     "by": "KALAI ET AL. · “WHY LANGUAGE MODELS HALLUCINATE”, 09.2025", "lbl": "TRÍCH DỊCH", "qline": 6},
    {"type": "kinetic", "at": 7, "items": [{"text": "MÔ HÌNH A: KHÔNG CHẮC → “KHÔNG BIẾT”", "at": 7, "fx": "rise"},
                                          {"text": "MÔ HÌNH B: LÚC NÀO CŨNG ĐOÁN", "at": 8, "acc": True}]},
    {"type": "ledger", "at": 9, "title": "CHẤM KIỂU 0 – 1", "rows": [
        {"k": "ĐÚNG", "v": "1 ĐIỂM", "at": [9, "đúng"]}, {"k": "SAI", "v": "0", "at": [9, "sai"]},
        {"k": "“KHÔNG BIẾT”", "v": "0", "at": [9, "bỏ"]}],
     "total": {"k": "THẮNG", "v": "MÔ HÌNH B", "at": [9, "thắng"]}},
    {"type": "kinetic", "at": 10, "items": [{"text": "HỎI MỘT NGÀY THÁNG", "at": 10, "sm": True},
                                           {"text": "“NGÀY 30 THÁNG 9”", "at": [10, "ngày", 1], "acc": True, "fx": "rise"},
                                           {"text": "chứ không: “khoảng mùa thu”", "at": [10, "chứ"], "sm": True}]},
    {"type": "slam", "at": 11, "text": "CHẮC NỊCH ≠ ĐÚNG", "white": True},
    {"type": "kinetic", "at": 12, "items": [{"text": "OPENAI · GPT-4 TECHNICAL REPORT · 2023", "at": 12, "sm": True, "fx": "rise"},
                                           {"text": "BẢN GỐC: CHẮC BAO NHIÊU, ĐÚNG CHỪNG ẤY", "at": [12, "khá"], "acc": True},
                                           {"text": "đo trên câu hỏi trắc nghiệm", "at": [12, "đo"], "sm": True}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "TINH CHỈNH ĐỂ TRÒ CHUYỆN", "at": 13, "sm": True},
                                           {"text": "ĐỘ KHỚP GIẢM", "at": [13, "độ"], "acc": True}]},
    {"type": "quote", "at": 14, "text": "GPT-4 can also be confidently wrong in its predictions…", "by": "OPENAI · GPT-4 TECHNICAL REPORT, 2023, TR. 10",
     "lbl": "TRÍCH DỊCH", "qline": 15},
    {"type": "kinetic", "at": 16, "items": [{"text": "ĐỀ NGHỊ CỦA CÁC TÁC GIẢ", "at": 16, "sm": True},
                                           {"text": "SAI → BỊ TRỪ ĐIỂM", "at": [16, "trả"]},
                                           {"text": "“KHÔNG BIẾT” → KHÔNG BỊ PHẠT", "at": [16, "nói"], "acc": True}]},
    {"type": "broll", "at": 17, "vid": "6100011", "veil": 0.5, "illus": VM,
     "kin": [{"text": "QUAY LẠI NEW YORK", "at": 17, "sm": True},
             {"text": "CÂU HỎI ĐÁNG GIÁ NHẤT", "at": [17, "câu"], "acc": True}]},
]}

# ---------------- CH04 · Hỏi đúng câu, nhầm người ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "HỎI ĐÚNG CÂU, NHẦM NGƯỜI"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "HỎI ĐÚNG CÂU,\nNHẦM NGƯỜI", "sub": "MATA v. AVIANCA · 2023", "bg": "sdny",
     "illus": "TOÀ MOYNIHAN, MANHATTAN · ẢNH 2019", "titleAt": [0, "là"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "“VARGHESE CÓ THẬT KHÔNG?”", "at": 1},
                                          {"text": "HỎI NHẦM NGƯỜI", "at": [1, "hỏi"], "acc": True}]},
    {"type": "chat", "at": 2, "head": APPB, "tag": HST, "msgs": [
        {"who": "u", "text": "Is varghese a real case", "at": 2},
        {"who": "m", "text": "Yes, … is a real case.", "at": [3, "câu", 1]}]},
    {"type": "date", "at": 4, "day": "PHIÊN ĐIỀU TRẦN · LUẬT SƯ STEVEN SCHWARTZ", "date": "08.06.2023"},
    {"type": "quote", "at": 5, "text": "…I falsely assumed was like a super search engine…", "by": "S. SCHWARTZ · PHIÊN ĐIỀU TRẦN 08.06.2023 · ECF 54 ¶37",
     "lbl": "TRÍCH DỊCH", "qline": 5},
    {"type": "quote", "at": 6, "text": "My reaction was, ChatGPT is finding that case somewhere… I just never thought it could be made up.",
     "by": "S. SCHWARTZ · ECF 54 ¶11 · “IT” = VỤ ÁN", "lbl": "TRÍCH DỊCH", "qline": 6},
    {"type": "kinetic", "at": 7, "items": [{"text": "NHƯNG TOÀ GHI LẠI", "at": 7, "sm": True},
                                          {"text": "ĐÃ TỰ TRA · KHÔNG THẤY", "at": [7, "anh"]},
                                          {"text": "VẪN IM LẶNG NỘP", "at": [7, "mà"], "acc": True}]},
    {"type": "broll", "at": 8, "vid": "6101367", "veil": 0.5, "illus": VM,
     "kin": [{"text": "KHÔNG PHẠT VÌ DÙNG AI", "at": 8, "acc": True},
             {"text": "“nothing inherently improper” · dùng công cụ AI đáng tin cậy để hỗ trợ", "at": 9, "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "PHẠT VÌ BỎ VAI TRÒ", "at": 10, "sm": True},
                                           {"text": "NGƯỜI GÁC CỔNG", "at": [10, "người"], "acc": True},
                                           {"text": "và vẫn bảo vệ phán quyết giả sau khi toà đặt nghi vấn", "at": 11, "sm": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "BÀI HỌC KHÔNG PHẢI", "at": 12, "sm": True},
                                           {"text": "ĐỪNG DÙNG AI", "at": [12, "đừng"], "fx": "strike", "strikeAt": [12, "dùng"]},
                                           {"text": "HỎI “CÓ THẬT KHÔNG” Ở MỘT NGUỒN KHÁC", "at": 13, "acc": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "CUỐI VIDEO", "at": 14, "sm": True},
                                           {"text": "HÌNH PHẠT ĐÁNG NHỚ NHẤT", "at": [14, "hình"], "acc": True}]},
    {"type": "question", "at": 15, "text": "Máy bịa thường tới mức nào?\nCó ai đã thật sự đếm?"},
]}

# ---------------- CH05 · Đếm những trích dẫn ma ----------------
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "ĐẾM NHỮNG TRÍCH DẪN MA"}, "bgm": {"mood": "upbeat", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "ĐẾM NHỮNG\nTRÍCH DẪN MA", "sub": "2023 — 2024", "vid": "1580502", "ms": 12,
     "illus": VM, "titleAt": [0, "cũng"]},
    {"type": "counter", "at": 1, "from": 0, "to": 636, "suffix": " TÀI LIỆU", "label": "TRONG 84 BÀI TỔNG QUAN NGẮN DO CHATGPT VIẾT",
     "sub": {"text": "WALTERS & WILDER · SCIENTIFIC REPORTS, 09.2023", "at": 1}},
    {"type": "bars", "at": 2, "title": "TÀI LIỆU THAM KHẢO BỊA (KHÔNG TỒN TẠI)", "unit": "636 TÀI LIỆU · WALTERS & WILDER 2023", "max": 100,
     "items": [{"k": "GPT-3.5", "v": 55, "lbl": "55%", "at": [2, "năm"]}, {"k": "GPT-4", "v": 18, "lbl": "18%", "at": [3, "con"], "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "JOURNAL OF LEGAL ANALYSIS · 2024", "at": 4, "sm": True, "fx": "rise"},
                                          {"text": "CÂU HỎI KIỂM CHỨNG ĐƯỢC VỀ ÁN LIÊN BANG", "at": [4, "hỏi"], "acc": True},
                                          {"text": "vụ án chọn ngẫu nhiên", "at": [4, "chọn"], "sm": True}]},
    {"type": "bars", "at": 5, "title": "TỈ LỆ TRẢ LỜI BỊA · TUỲ MÔ HÌNH", "unit": "DAHL ET AL. 2024 · ÁN LIÊN BANG · MÔ HÌNH 2023", "max": 100,
     "items": [{"k": "THẤP NHẤT · GPT-4", "v": 58, "lbl": "58%", "at": [5, "tuỳ"]},
               {"k": "CAO NHẤT · LLAMA 2", "v": 88, "lbl": "88%", "at": [5, "tới"], "acc": True}]},
    {"type": "kinetic", "at": [6, "nhiều"], "items": [{"text": "NHIỀU KHI KHÔNG BIẾT", "at": [6, "nhiều"], "acc": True, "fx": "rise"},
                                          {"text": "lúc nào chính mình đang bịa", "at": [6, "lúc"], "sm": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "ĐÓ LÀ MÔ HÌNH 2023", "at": 7, "sm": True, "fx": "rise"},
                                          {"text": "VỀ SAU: KHÁ HƠN", "at": [7, "các"]},
                                          {"text": "NHƯNG CHƯA HẾT BỊA", "at": [7, "nhưng"], "acc": True}]},
    {"type": "slam", "at": 8, "text": "“AI SAI BAO NHIÊU PHẦN TRĂM?”", "white": True},
    {"type": "kinetic", "at": 9, "items": [{"text": "KHÔNG CÓ MỘT CON SỐ CHUNG", "at": 9},
                                          {"text": "MÔ HÌNH · NGÔN NGỮ · CÂU HỎI", "at": 10, "sm": True},
                                          {"text": "CÀNG HIẾM, CÀNG DỄ BỊ BỊA", "at": [10, "điều"], "acc": True}]},
    {"type": "broll", "at": 11, "vid": "8731289", "veil": 0.5, "illus": VM,
     "kin": [{"text": "TRỢ LÝ AI · 2025", "at": 11, "sm": True, "fx": "rise"},
             {"text": "HỎI TIN TỨC THÌ SAO?", "at": [11, "hỏi"], "acc": True}]},
]}

# ---------------- CH06 · Giáo hoàng nào? ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "GIÁO HOÀNG NÀO?"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "GIÁO HOÀNG\nNÀO?", "sub": "EBU · BBC · 24.05 — 10.06.2025", "bg": "vatican",
     "illus": "ẢNH MINH HỌA · VATICAN, 2013", "titleAt": [0, "cuối"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "22 ĐÀI CÔNG CỘNG · 18 NƯỚC", "at": 1, "fx": "rise"},
                                          {"text": "4 TRỢ LÝ AI · BẢN MIỄN PHÍ", "at": [1, "bốn"], "acc": True, "fx": "rise"},
                                          {"text": "14 ngôn ngữ · câu hỏi thời sự", "at": [1, "những"], "sm": True}]},
    {"type": "counter", "at": 2, "from": 0, "to": 2709, "suffix": " CÂU TRẢ LỜI", "label": "NHÀ BÁO CỦA TỪNG ĐÀI CHẤM",
     "sub": {"text": "271 NHÀ BÁO · “NEWS INTEGRITY IN AI ASSISTANTS”, EBU/BBC 2025", "at": 2}},
    {"type": "question", "at": 3, "text": "Giáo hoàng hiện nay là ai?"},
    {"type": "timeline", "at": 4, "items": [{"year": "21.04", "text": "Giáo hoàng *Phanxicô* qua đời", "at": 4},
                                           {"year": "08.05", "text": "*Lêô XIV* được bầu", "at": [4, "đầu"]}]},
    {"type": "ledger", "at": 5, "title": "“GIÁO HOÀNG HIỆN NAY LÀ PHANXICÔ”", "srcnote": "VÍ DỤ TRONG BÁO CÁO EBU/BBC, TR. 15–16 · KHÔNG PHẢI TỈ LỆ",
     "rows": [{"k": "CHATGPT", "v": "YLE · 28.05.2025", "at": [5, "ít"]}, {"k": "GEMINI", "v": "NOS · 29.05.2025", "at": [5, "ba"]},
              {"k": "COPILOT", "v": "NOS · 30.05.2025", "at": [5, "vẫn"]}]},
    {"type": "chat", "at": 6, "head": "COPILOT · NOS/NPO · 30.05.2025 · DỊCH TỪ TIẾNG HÀ LAN · EBU/BBC", "msgs": [
        {"who": "u", "text": "Who is the Pope?", "at": 6},
        {"who": "m", "text": "The current pope is Francis…", "at": [6, "rằng"]},
        {"who": "m", "text": "…He died on April 21, 2025.", "at": 7}]},
    {"type": "photo", "at": 8, "img": "starliner", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "“VÌ SAO PHI HÀNH GIA NASA BỊ KẸT NGOÀI KHÔNG GIAN?”", "at": 8, "sm": True}],
     "label": {"k": "TÀU STARLINER TIẾN VÀO TRẠM VŨ TRỤ", "v": "06.06.2024 · ẢNH NASA", "at": 8}},
    {"type": "kinetic", "at": 9, "bg": "starliner", "items": [{"text": "DỰ KIẾN: 8 NGÀY", "at": 9, "fx": "rise"},
                                                           {"text": "THỰC TẾ: HƠN 9 THÁNG", "at": [9, "đã"], "acc": True, "fx": "rise"},
                                                           {"text": "vì tàu của họ trục trặc", "at": [9, "vì"], "sm": True}]},
    {"type": "chat", "at": 10, "head": "GEMINI · YLE (TIẾNG PHẦN LAN) · EBU/BBC 2025, TR. 25", "msgs": [
        {"who": "u", "text": "Why were NASA astronauts stuck in space?", "at": 10},
        {"who": "m", "text": "NASA astronauts have not been stuck in space.", "at": [10, "không"]},
        {"who": "m", "text": "You might be confusing this with a sci-fi movie or news that discussed a potential scenario…", "at": 11}]},
    {"type": "slam", "at": 12, "text": "MÁY SAI, RỒI BẢO NGƯỜI ĐÚNG LÀ NHẦM"},
    {"type": "counter", "at": 13, "from": 0, "to": 45, "suffix": "%", "label": "CÂU TRẢ LỜI CÓ ÍT NHẤT MỘT LỖI ĐÁNG KỂ",
     "sub": {"text": "CÂU HỎI TIN TỨC · BẢN MIỄN PHÍ · 05–06.2025 · 22 ĐÀI", "at": 13}},
    {"type": "counter", "at": 14, "from": 0, "to": 31, "suffix": "%", "label": "CÓ VẤN ĐỀ LỚN VỀ NGUỒN",
     "sub": {"text": "LỖI NHIỀU NHẤT · EBU/BBC 2025, TR. 10", "at": 14}},
    {"type": "ledger", "at": 15, "title": "VẤN ĐỀ VỀ NGUỒN", "srcnote": "EBU/BBC 2025, TR. 10",
     "rows": [{"k": "1", "v": "KHÔNG GHI NGUỒN", "at": [15, "không"]}, {"k": "2", "v": "GHI SAI NGUỒN", "at": [15, "ghi", 1]},
              {"k": "3", "v": "NGUỒN KHÔNG HỀ NÓI ĐIỀU ẤY", "at": [15, "dẫn"]}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "CON SỐ ĐÁNG NHỚ NHẤT", "at": 16, "acc": True, "fx": "rise"}]},
    {"type": "counter", "at": 17, "from": 0, "to": 17, "suffix": " / 3.113", "label": "LẦN TRỢ LÝ TỪ CHỐI TRẢ LỜI",
     "sub": {"text": "CHƯA TỚI 1% (0,5%) · EBU/BBC 2025", "at": [17, "chưa"]}},
    {"type": "quote", "at": 18, "text": "Many of the issues identified in this research are exacerbated by the confidence with which assistants deliver their responses.",
     "by": "EBU/BBC · NEWS INTEGRITY IN AI ASSISTANTS, 2025, TR. 24", "lbl": "TRÍCH BÁO CÁO"},
    {"type": "broll", "at": 19, "vid": "37779521", "ms": 8, "veil": 0.55, "illus": VM,
     "kin": [{"text": "GẦN NHƯ KHÔNG BAO GIỜ “TÔI KHÔNG BIẾT”", "at": 19, "sm": True},
             {"text": "NHƯ KỲ THI KHÔNG TRỪ ĐIỂM", "at": [19, "đúng"], "acc": True}]},
    {"type": "question", "at": 20, "text": "Vậy bạn nên làm gì?"},
]}

# ---------------- CH07 · Ba thói quen ----------------
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "BA THÓI QUEN"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "BA THÓI QUEN", "sub": "TRƯỚC KHI TIN MỘT CÂU TRẢ LỜI", "vid": "8198820",
     "illus": VM, "titleAt": [0, "ở"]},
    {"type": "counter", "at": 1, "from": 0, "to": 96, "prefix": "≈ ", "suffix": "%", "label": "HỌC SINH 15 TUỔI Ở VIỆT NAM DÙNG CHATBOT AI ĐỂ HỌC",
     "sub": {"text": "OECD · PISA 2025 · CHỈ 4% KHÔNG BAO GIỜ / HẦU NHƯ KHÔNG DÙNG (TB OECD 14%)", "at": 1}},
    {"type": "broll", "at": 2, "vid": "7683480", "veil": 0.5, "illus": VM,
     "kin": [{"text": "VTV · 04.10.2026", "at": 2, "sm": True, "fx": "rise"},
             {"text": "CHATBOT GIẢI MỘT BÀI TOÁN CƠ BẢN", "at": [2, "cho"], "acc": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "TÍNH TỪ TRÁI SANG PHẢI", "at": 3},
                                          {"text": "THAY VÌ NHÂN CHIA TRƯỚC, CỘNG TRỪ SAU", "at": [3, "thay"], "acc": True},
                                          {"text": "một ứng dụng AI khác thì giải đúng", "at": [3, "một"], "sm": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "BA THÓI QUEN", "at": 4, "sm": True},
                                          {"text": "THÓI QUEN 1", "at": 5, "fx": "rise"},
                                          {"text": "BẮT GHI NGUỒN, RỒI TỰ BẤM VÀO", "at": [5, "bắt"], "acc": True}]},
    {"type": "broll", "at": 6, "vid": "9198046", "ms": 6, "veil": 0.5, "illus": VM,
     "kin": [{"text": "MỞ NGUỒN · TÌM ĐÚNG CÂU NÓ TRÍCH", "at": 6},
             {"text": "CÂU ẤY CÓ THẬT NÓI VẬY KHÔNG?", "at": [6, "xem"], "acc": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "LUẬT SƯ Ở NEW YORK ĐÃ LÀM DỞ", "at": 7, "sm": True},
                                          {"text": "TRA KHÔNG THẤY — VẪN NỘP", "at": [7, "tra"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "THÓI QUEN 2", "at": 8, "sm": True, "fx": "rise"},
                                          {"text": "HỎI LẠI", "at": [8, "hỏi"], "acc": True},
                                          {"text": "cảnh đã hẹn với bạn từ đầu video", "at": 9, "sm": True}]},
    {"type": "chat", "at": 10, "head": "KALAI ET AL. 2025 · MÔ HÌNH MÃ NGUỒN MỞ · 3 LẦN HỎI", "tag": {"text": "TRÍCH BÀI BÁO"}, "msgs": [
        {"who": "u", "text": "What is Adam Tauman Kalai's birthday? If you know, just respond with DD-MM.", "at": 10},
        {"who": "m", "text": "Lần 1:  03-07", "at": [11, "mùng"]},
        {"who": "m", "text": "Lần 2:  15-06", "at": [11, "ngày"]},
        {"who": "m", "text": "Lần 3:  01-01", "at": [11, "rồi"]}]},
    {"type": "slam", "at": 12, "text": "SINH NHẬT THẬT: MÙA THU", "sub": "“THE CORRECT DATE IS IN AUTUMN” · KALAI ET AL. 2025"},
    {"type": "kinetic", "at": 13, "items": [{"text": "BIẾT THẬT → HỎI MẤY LẦN THƯỜNG VẪN NHƯ NHAU", "at": 13, "sm": True},
                                           {"text": "ĐANG ĐOÁN → CÂU TRẢ LỜI HAY LUNG LAY", "at": [13, "khi", 1], "acc": True}]},
    {"type": "broll", "at": 14, "vid": "34913409", "veil": 0.55, "illus": VM,
     "kin": [{"text": "HỎI LẠI: CUỘC TRÒ CHUYỆN MỚI · HOẶC AI KHÁC", "at": 14, "sm": True},
             {"text": "LỆCH NHAU = ĐÈN ĐỎ", "at": [14, "hai"], "acc": True}]},
    {"type": "kinetic", "at": 15, "items": [{"text": "NHƯNG: GIỐNG NHAU", "at": 15},
                                           {"text": "CHƯA CHẮC ĐÃ ĐÚNG", "at": [15, "chưa"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "THÓI QUEN 3", "at": 16, "sm": True, "fx": "rise"},
                                           {"text": "DÙNG AI LÀM NHÁP", "at": [16, "dùng"]},
                                           {"text": "ĐỪNG COI NÓ LÀ NGUỒN CỦA SỰ THẬT", "at": [16, "đừng"], "acc": True}]},
    {"type": "ledger", "at": 17, "title": "NHÁP ↔ NGUỒN", "rows": [
        {"k": "VIẾT THƯ · SẮP Ý", "v": "ĐỌC LẠI LÀ TỰ KIỂM ĐƯỢC", "at": 17},
        {"k": "TÊN · SỐ · LUẬT", "v": "PHẢI QUA MỘT NGUỒN GỐC", "at": 18}]},
    {"type": "chat", "at": 19, "head": "BẠN CŨNG CÓ THỂ DẶN", "msgs": [
        {"who": "u", "text": "Nếu không chắc, hãy nói là không biết.", "at": 19}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "ĐỪNG TRÔNG CẢ VÀO CÂU DẶN", "at": 20, "acc": True},
                                           {"text": "câu hỏi ngày sinh cũng đã dặn “if you know” — máy vẫn đoán", "at": [20, "câu"], "sm": True}]},
]}

# ---------------- CH08 · Người gác cổng ----------------
CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "NGƯỜI GÁC CỔNG"}, "bgm": {"mood": "curious", "gain": 0.14}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "NGƯỜI\nGÁC CỔNG", "sub": "NEW YORK · 22.06.2023", "bg": "moynihan",
     "illus": "TOÀ MOYNIHAN, MANHATTAN · ẢNH 2026", "titleAt": [0, "quay"]},
    {"type": "counter", "at": 1, "from": 0, "to": 5000, "prefix": "$", "label": "TIỀN PHẠT · HAI LUẬT SƯ VÀ VĂN PHÒNG (MỘT KHOẢN CHUNG)",
     "sub": {"text": "HƠN 120 TRIỆU ĐỒNG (TỈ GIÁ ≥ 24.000 Đ/USD) · ECF 54", "at": [1, "tức"]}},
    {"type": "kinetic", "at": 2, "items": [{"text": "HÌNH PHẠT ĐÁNG NHỚ NHẤT", "at": 2, "sm": True},
                                          {"text": "MẤY LÁ THƯ", "at": [2, "mấy"], "acc": True}]},
    {"type": "file", "at": 3, "k": "KẾT LUẬN (b) · ECF 54", "name": "Thư gửi từng\nthẩm phán", "tag": HST,
     "rows": [{"k": "GỬI", "v": "từng *thẩm phán có thật*", "at": 3},
              {"k": "BỊ GHI TÊN", "v": "tác giả *phán quyết giả*", "at": [3, "tác"]},
              {"k": "KÈM THEO", "v": "*bản phán quyết bịa* mang tên họ", "at": [3, "kèm"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "CÙNG NGÀY: VỤ KIỆN CỦA ÔNG MATA BỊ BÁC", "at": 4},
                                          {"text": "VÌ QUÁ HẠN HAI NĂM", "at": [4, "vì"], "acc": True},
                                          {"text": "không liên quan gì tới ChatGPT", "at": [4, "lý"], "sm": True}]},
    {"type": "counter", "at": 5, "from": 0, "to": 2149, "suffix": " QUYẾT ĐỊNH", "label": "CỦA CÁC TOÀ ÁN TRÊN THẾ GIỚI · TÍNH TỚI 05.10.2026",
     "sub": {"text": "CƠ SỞ DỮ LIỆU CỦA NHÀ NGHIÊN CỨU LUẬT DAMIEN CHARLOTIN", "at": [5, "cơ"]}},
    {"type": "kinetic", "at": [5, "nơi"], "items": [{"text": "TOÀ NHẬN THẤY — HOẶC NGẦM CHO RẰNG", "at": [5, "nơi"], "sm": True},
                                                   {"text": "CÓ NGƯỜI DỰA VÀO NỘI DUNG DO AI BỊA", "at": [5, "có"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "KHÔNG NÓI DỐI THEO NGHĨA CON NGƯỜI", "at": 6},
                                          {"text": "NHIỀU KHI KHÔNG BIẾT MÌNH ĐANG BỊA", "at": [6, "nhiều"], "acc": True}]},
    {"type": "broll", "at": 7, "vid": "6672451", "veil": 0.55, "illus": VM,
     "kin": [{"text": "VIẾT TIẾP CÂU NGHE HỢP LÝ NHẤT", "at": 7, "sm": True},
             {"text": "ĐỪNG BỎ TRỐNG", "at": [7, "đừng"], "acc": True}]},
    {"type": "slam", "at": 8, "text": "NGƯỜI GÁC CỔNG VẪN LÀ BẠN"},
    {"type": "kinetic", "at": 9, "items": [{"text": "“CÓ THẬT KHÔNG?”", "at": 9, "acc": True},
                                          {"text": "vẫn là câu hỏi đáng giá nhất", "at": [9, "vẫn"], "sm": True}]},
    {"type": "broll", "at": 10, "vid": "5636977", "veil": 0.5, "illus": VM,
     "kin": [{"text": "HỎI ĐÚNG CHỖ", "at": 10, "acc": True},
             {"text": "một nguồn bạn tự mở ra — không phải cỗ máy vừa trả lời bạn", "at": [10, "một"], "sm": True}]},
    {"type": "question", "at": 11, "text": "Lần gần nhất AI trả lời rất chắc chắn\nmà hoá ra sai, là chuyện gì?"},
    {"type": "broll", "at": 12, "vid": "13375774", "veil": 0.35, "illus": VM,
     "kin": [{"text": "KỂ Ở PHẦN BÌNH LUẬN", "at": 12, "acc": True}]},
]}

SPEC = {
    "title": "Vì Sao AI Bịa Mà Vẫn Rất Tự Tin? Sáu Vụ Án Không Hề Có Thật",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "endcardBg": "sdny",
    "acc": ["ai", "chatgpt", "varghese", "bịa", "ảo", "giác", "nguồn", "gác", "cổng", "đoán"],
    "say": SAY, "imgs": IMGS, "chapters": list(CH),
    "youtube": {
        "titles": ["Vì Sao AI Bịa Mà Vẫn Rất Tự Tin? Sáu Vụ Án Không Hề Có Thật",
                   "AI Bịa Ra 6 Vụ Án Rồi Khẳng Định Là Có Thật: Chuyện Gì Đang Xảy Ra Bên Trong?",
                   "Gần Nửa Câu Trả Lời Tin Tức Của Trợ Lý AI Có Lỗi Lớn: 3 Thói Quen Để Không Tin Nhầm"],
        "summary": "Năm 2023, một văn phòng luật ở New York nộp lên toà liên bang sáu án lệ không hề tồn tại; luật sư hỏi lại ChatGPT "
                   "\"có thật không\", máy trả lời \"có\". Vì sao mô hình ngôn ngữ bịa (\"ảo giác\") mà vẫn rất tự tin: viết theo hình dáng "
                   "câu chữ, những điều chỉ gặp một lần, và một kỳ thi không trừ điểm cho lời đoán. Các nghiên cứu đã đếm trích dẫn ma, "
                   "phép thử EBU/BBC 2025 với câu hỏi \"Giáo hoàng hiện nay là ai?\", và ba thói quen để không tin nhầm.",
        "more": ["Các tỉ lệ trong video luôn gắn với mô hình, năm và loại câu hỏi; không có một \"tỉ lệ bịa chung\" cho mọi AI. Số 2023 là "
                 "của các mô hình cũ. Số EBU/BBC là câu hỏi tin tức, bản miễn phí của bốn trợ lý, 24/05–10/06/2025. Ảnh chụp màn hình "
                 "trong hồ sơ toà được dựng lại bằng chữ (Phụ lục B, phán quyết 22/06/2023). Vụ Mata bị bác vì quá thời hạn hai năm, "
                 "không phải vì ChatGPT. Lời trích được đọc bằng giọng máy của kênh."],
        "ch00_title": "Sáu vụ án không có thật: luật sư hỏi ChatGPT \"có thật không?\"",
        "chapter_titles": {"ch00": "Mở đầu: luật sư nộp 6 án lệ do ChatGPT bịa (2023)",
                           "ch01": "AI viết như thật: đoán mẩu chữ tiếp theo",
                           "ch02": "Vì sao AI bịa: những điều chỉ gặp một lần",
                           "ch03": "Kỳ thi không trừ điểm: vì sao AI không nói \"không biết\"",
                           "ch04": "Hỏi AI \"có thật không\" có được không?",
                           "ch05": "AI bịa bao nhiêu trích dẫn? Các nghiên cứu đã đếm",
                           "ch06": "Nghiên cứu EBU/BBC 2025: Giáo hoàng nào?",
                           "ch07": "3 thói quen kiểm tra câu trả lời của AI",
                           "ch08": "Kết: người gác cổng"},
        "sources": [
            "https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.31.0.pdf",
            "https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0.pdf",
            "https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.55.0_2.pdf",
            "https://arxiv.org/abs/2509.04664",
            "https://arxiv.org/abs/2303.08774",
            "https://www.ebu.ch/files/live/sites/ebu/files/Publications/Intelligence/open/EBU-Intelligence-BBC_News_Integrity_in_AI_Assistants_Report_2025.pdf",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/",
            "https://arxiv.org/abs/2401.01301",
            "https://www.damiencharlotin.com/hallucinations/",
            "https://www.oecd.org/en/publications/pisa-2025-results-volume-i-country-notes_2d4ff9ea-en/viet-nam_d652623e-en.html",
            "https://thanhnien.vn/gan-96-hoc-sinh-viet-dung-ai-ty-le-cao-nhat-the-gioi-185260910183700006.htm",
            "https://vtv.vn/hoc-sinh-lam-dung-ai-khi-cong-cu-ho-tro-lam-suy-giam-tu-duy-100261003225835725.htm",
            "https://antv.gov.vn/van-hoa-6/canh-bao-chat-gpt-thong-tin-sai-lech-ve-nhieu-danh-tac-viet-nam-B94ECF548.html",
            "https://vqa.moet.gov.vn/vi/news/savefile/thong-bao/cau-truc-dinh-dang-de-thi-tot-nghiep-thpt-tu-nam-2025-74.html",
            "https://danviet.vn/cach-tinh-diem-thi-tot-nghiep-thpt-2026-tat-ca-cac-mon-ra-sao-d1434266.html",
        ],
        "hashtags": ["AI", "ChatGPT", "AoGiacAI", "KiemChung", "MindInTheMachine"],
        "tags": ["AI bịa", "ảo giác AI", "AI hallucination", "vì sao AI bịa", "ChatGPT bịa án lệ", "Mata v. Avianca",
                 "mô hình ngôn ngữ", "trí tuệ nhân tạo", "kiểm chứng thông tin", "EBU BBC AI", "trợ lý AI sai",
                 "cách dùng AI an toàn", "AI và học sinh", "PISA 2025 AI", "trích dẫn giả", "Why Language Models Hallucinate"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}

if __name__ == "__main__":
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    pk = OUT / "bgm_picks.json"           # nhạc chốt tay: resolve_bgm dùng picks có sẵn, không tự chọn lại
    old = json.loads(pk.read_text(encoding="utf-8")) if pk.exists() else {}
    if old != BGM_PICKS:
        pk.parent.mkdir(parents=True, exist_ok=True)
        pk.write_text(json.dumps(BGM_PICKS, indent=1), encoding="utf-8")
    print(f"spec + {len(CH)} chương")
