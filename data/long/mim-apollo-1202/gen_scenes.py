"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #18 "Mã 1202, máy tính dẫn đường Apollo 11".

    python data/long/mim-apollo-1202/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md và factcheck.md. Pha 1: chỉ viết file; chưa dựng, chưa tải ảnh (imgs ghi tên File: Commons, license đã đọc qua API 20/10/2026,
phải đọc lại ở pha 2). Không có clip Pexels: toàn bộ hình là ảnh NASA (công cộng) + chữ/bảng/sơ đồ của kênh. Không có cảnh DSKY riêng: bảng "ledger" thay.
Lộ trình dạng "nhật ký hai cột MÁY | NGƯỜI": ledger ở CH00 (hứa), CH03 (cột NGƯỜI), CH04 (cột MÁY), CH05 (bảng năm báo động), CH06 (dòng cuối).
Mọi neo [dòng, "từ"] chỉ dùng chữ nằm trong lời đọc; không neo vào chữ số hay chữ có trong bảng "say".
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"=GO": "gô", "1202": "một hai không hai", "1201": "một hai không một", "eagle": "i-gồ", "mit": "em ai ti", "nasa": "na-sa",
       "apollo": "a-pô-lô", "houston": "Hiu-xtần", "neil": "Nin", "armstrong": "Am-xtrông", "kranz": "Cranh", "gene": "Gin", "steve": "Xtiv",
       "bales": "Bây-lơ", "jack": "Giắc", "garman": "Gạc-man", "buzz": "Bớt", "aldrin": "Ôn-drin", "margaret": "Mác-gơ-rét",
       "hamilton": "Hem-min-tần", "laning": "Lê-ning", "polaris": "Pô-la-ris", "executive": "Ích-xếch-kiu-tiv", "radar": "ra-đa",
       "hertz": "héc", "tranquility": "Tran-quy-li-ti", "tomayko": "Tô-mây-cô", "james": "Giêm", "don": "Đôn", "eyles": "Ai-lơ",
       "feet": "phít", "kilobyte": "ki-lô-bai", "logic": "lô-gíc"}
VM = "ẢNH MINH HỌA"
SELF = "TỰ TÍNH"
CH = {}

IMGS = {
    "launch": "File:Apollo 11 Launch - GPN-2000-000630.jpg",                                                      # Public domain (NASA)
    "agc": "File:Apollo Guidance Computer (AGC).jpg",                                                               # CC BY 2.0 (Steve Jurvetson)
    "lm": "File:Apollo 11 Lunar Module after separation from the Command Module (AS11-44-6584).jpg",               # Public domain (NASA)
    "lm2": "File:Earth, Moon and Lunar Module, AS11-44-6643.jpg",                                                  # Public domain (NASA / Apollo 11)
    "mcc": "File:Inflight - Apollo XI (Mission Control Center -MCC-) - MSC (S69-40302).jpg",                       # Public domain (NASA JSC)
    "mcctraj": "File:Apollo 11 Mission Control Center - landing trajectory.jpg",                                   # Public domain (NASA)
    "site": "File:LRO Gets Additional View of Apollo 11 Landing Site (4092985062).jpg",                            # Public domain (NASA Goddard)
}

# ---------------------------------------------------------------- CH00: đèn báo thứ nhất (cold open)
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "ĐÈN BÁO THỨ NHẤT"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "date", "bg": "lm", "day": "EAGLE ĐANG HẠ XUỐNG MẶT TRĂNG", "date": "20.07.1969",
     "sub": {"text": "ĐỘNG CƠ HẠ CÁNH MỞ MÁY · GET 102:33:05", "at": 2}},
    {"type": "ledger", "at": 3, "title": "BÁO ĐỘNG CHƯƠNG TRÌNH THỨ NHẤT", "srcnote": "NASA SP-238 · BẢNG 5-I",
     "rows": [{"k": "GET", "v": "102:38:22", "at": 3}, {"k": "SAU KHI MỞ MÁY", "v": "5 PHÚT 17 GIÂY", "at": [3, "bỗng"]},
              {"k": "MÃ", "v": "1202", "at": [4, "một"]}]},
    {"type": "slam", "at": 5, "text": "1202", "sub": "MÃ BÁO ĐỘNG CỦA MÁY TÍNH DẪN ĐƯỜNG · CÒN HƠN 7 PHÚT NỮA MỚI CHẠM ĐẤT"},
    {"type": "photo", "at": 6, "img": "lm", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "CÒN CAO HƠN 9.000 MÉT", "at": 6, "acc": True}],
     "label": {"k": "EAGLE SAU KHI TÁCH KHỎI TÀU MẸ", "v": "NASA · AS11-44-6584", "at": 6}},
    {"type": "quote", "at": 10, "text": "We're GO on that alarm.", "by": "HOUSTON · BẢN GHI KHÔNG-ĐỐI-ĐẤT KỸ THUẬT · APOLLO 11",
     "lbl": "TRÍCH DỊCH", "qline": 10, "typeAt": [10, "chúng"]},
    {"type": "kinetic", "at": 11, "items": [{"text": "GO = CỨ TIẾP TỤC", "at": 11, "acc": True},
                                           {"text": "đèn báo sẽ sáng thêm bốn lần nữa", "at": [13, "đèn"], "sm": True}]},
    {"type": "ledger", "at": 14, "title": "NHẬT KÝ HẠ CÁNH · HAI CỘT", "srcnote": "KÊNH TỰ KẺ BẢNG · MỖI LẦN ĐÈN BÁO SÁNG, THÊM MỘT DÒNG",
     "rows": [{"k": "MÁY", "v": "MỖI LẦN KÊU, NÓ TỰ LÀM GÌ", "at": [15, "cuốn"]},
              {"k": "NGƯỜI", "v": "AI TRẢ LỜI · DỰA VÀO ĐÂU", "at": [16, "cuốn"]}],
     "total": {"k": "DÒNG CUỐI", "v": "VÌ SAO LÀ MÁY CHẠY ĐÚNG", "at": 18}},
]}

# ---------------------------------------------------------------- CH01: chiếc máy đặt hàng khi chưa có bản vẽ
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "CHIẾC MÁY ĐẶT HÀNG KHI CHƯA CÓ BẢN VẼ"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "CHIẾC MÁY ĐẶT HÀNG\nKHI CHƯA CÓ BẢN VẼ", "sub": "MIT · 1961", "bg": "launch",
     "titleAt": [0, "Chuyện"]},
    {"type": "date", "at": 1, "day": "NASA KÝ HỢP ĐỒNG VỚI PHÒNG THÍ NGHIỆM DỤNG CỤ MIT", "date": "09.08.1961",
     "sub": {"text": "THIẾT KẾ + CHẾ TẠO HỆ DẪN ĐƯỜNG, KỂ CẢ PHẦN MỀM", "at": 2}},
    {"type": "photo", "at": 3, "img": "agc", "tone": "color", "move": "in", "veil": 0.5, "illus": VM,
     "kin": [{"text": "NHÓM LÀM HỆ DẪN ĐƯỜNG TÊN LỬA POLARIS", "at": 3, "acc": True},
             {"text": "nên được chọn cho Apollo", "at": [3, "nên"], "sm": True}],
     "label": {"k": "MÁY TÍNH DẪN ĐƯỜNG APOLLO", "v": "ẢNH: STEVE JURVETSON · CC BY 2.0", "at": 3}},
    {"type": "timeline", "at": 4, "items": [{"year": "1961", "text": "*ký hợp đồng* · chưa có đặc tả đầy đủ", "at": 4},
                                           {"year": "CUỐI 1962", "text": "*mới hình dung* Apollo cần gì", "at": 5}]},
    {"type": "quote", "at": 6, "dy": True, "text": "Nếu biết trước những gì sẽ học được, họ có lẽ đã kết luận là với công nghệ đầu những năm 1960, bài toán này vô nghiệm.",
     "by": "MỘT NGƯỜI TRONG NHÓM MIT NHỚ LẠI · QUA TOMAYKO, NASA CR-182505 (1988)", "lbl": "DIỄN Ý", "typeAt": [6, None, 0, 0.05], "typeDur": 3.0},
    {"type": "ledger", "at": 7, "title": "BỘ NHỚ · THIẾT KẾ ĐẦU → BẢN BAY", "srcnote": "TOMAYKO · NASA CR-182505 · CHƯƠNG 2",
     "rows": [{"k": "CỐ ĐỊNH", "v": "4K TỪ → 36.864 TỪ", "at": 7}, {"k": "GHI ĐƯỢC", "v": "256 TỪ → 2.048 TỪ", "at": [8, "hai"]}]},
    {"type": "counter", "at": 9, "from": 78, "to": 78, "prefix": "≈ ", "suffix": " KILOBYTE", "tag": SELF,
     "label": "TOÀN BỘ BỘ NHỚ CỦA MÁY · 38.912 TỪ × 16 BIT", "sub": {"text": "CHƯA TỚI 80 KB · KÊNH TỰ TÍNH", "at": 10}},
    {"type": "kinetic", "at": 11, "items": [{"text": "32 KG · 70 OÁT", "at": 11, "acc": True},
                                            {"text": "gần 5.000 mạch logic đơn giản bên trong", "at": [12, "gần"], "sm": True}]},
    {"type": "slam", "at": 13, "text": "60%", "sub": "SỐ VI MẠCH CẢ NƯỚC MỸ SẢN XUẤT · NGUYÊN MẪU APOLLO DÙNG · MÙA HÈ 1963"},
    {"type": "photo", "at": 14, "img": "agc", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "BỘ NHỚ DÂY THỪNG", "at": [16, "bộ"], "acc": True}],
     "label": {"k": "MÁY TÍNH DẪN ĐƯỜNG APOLLO", "v": "BẢN TRƯNG BÀY", "at": 14}},
    {"type": "kinetic", "at": 17, "items": [{"text": "LÀM XONG LÀ KHÓ SỬA", "at": 17, "acc": True},
                                            {"text": "giao trước chuyến bay nhiều tháng", "at": 18, "sm": True},
                                            {"text": "PHẢI ĐÚNG NGAY LẦN ĐẦU", "at": 19}]},
    {"type": "question", "at": 20, "text": "Máy bé như vậy, khó sửa như vậy,\nlàm sao lo nổi cả chuyến hạ cánh?"},
]}

# ---------------------------------------------------------------- CH02: bộ điều hành, phòng nhớ, khởi động lại
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "CỖ MÁY KHÔNG BAO GIỜ LÀM MỘT VIỆC"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "CỖ MÁY KHÔNG BAO GIỜ\nLÀM MỘT VIỆC", "sub": "BỘ ĐIỀU HÀNH · EXECUTIVE", "titleAt": [0, "Hạ"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "HÀNG CHỤC VIỆC", "at": 1, "acc": True}, {"text": "chạy gần như cùng lúc", "at": [1, "chạy"], "sm": True}]},
    {"type": "ledger", "at": 2, "title": "VIỆC CỦA MÁY LÚC HẠ CÁNH", "srcnote": "NASA SP-238 · MỤC 16 · TOMAYKO",
     "rows": [{"k": "1", "v": "ĐỌC GIA TỐC KẾ", "at": 2}, {"k": "2", "v": "LÁI ĐỘNG CƠ", "at": [2, "lái"]}, {"k": "3", "v": "CẬP NHẬT MÀN HÌNH", "at": [2, "cập"]}],
     "total": {"k": "MỖI 2 GIÂY", "v": "DẪN ĐƯỜNG TÍNH LẠI 1 LẦN", "at": 3}},
    {"type": "slam", "at": 4, "text": "EXECUTIVE", "sub": "BỘ ĐIỀU HÀNH · VIỆC QUAN TRỌNG HƠN ĐƯỢC CHẠY TRƯỚC"},
    {"type": "counter", "at": 6, "from": 0, "to": 20, "suffix": " MILI GIÂY", "until": [6, "nghìn"], "label": "CỨ CHỪNG ĐÓ LẠI XEM CÓ VIỆC QUAN TRỌNG HƠN KHÔNG",
     "sub": {"text": "TOMAYKO · NASA CR-182505", "at": 6}},
    {"type": "ledger", "at": 8, "title": "MỘT VIỆC = MỘT “PHÒNG” NHỚ", "srcnote": "TOMAYKO · GRUMMAN LAV-500-940 · Ô DÙNG CHUNG BẢY VIỆC: THEO HỒI KÝ MỘT KỸ SƯ MIT",
     "rows": [{"k": "PHÒNG", "v": "12 Ô NHỚ", "at": [10, "mười"]}, {"k": "KHI XONG", "v": "TRẢ PHÒNG", "at": 11}, {"k": "CẢ MÁY", "v": "CHỈ 8 PHÒNG", "at": [11, "tám"]},
              {"k": "Ô DÙNG CHUNG", "v": "CÓ Ô GÁNH TỚI 7 VIỆC", "at": [12, "bảy"]}]},
    {"type": "question", "at": 13, "text": "Phòng đã hết thì sao?\nHãy nhớ câu hỏi này."},
    {"type": "photo", "at": 15, "img": "agc", "tone": "bw", "move": "out", "veil": 0.55,
     "kin": [{"text": "KHÔNG ĐƯỢC ĐỂ MÁY CHẾT", "at": 15, "acc": True}, {"text": "giữa lúc đang đốt động cơ", "at": [15, "giữa"], "sm": True}],
     "label": {"k": "MÁY TÍNH DẪN ĐƯỜNG APOLLO", "v": "BẢN TRƯNG BÀY", "at": 15}},
    {"type": "ledger", "at": 17, "title": "KHỞI ĐỘNG LẠI · BA BƯỚC", "srcnote": "TOMAYKO · NASA CR-182505 · “HANDLING RESTARTS”",
     "rows": [{"k": "1", "v": "XOÁ MỌI LỆNH RA NGOÀI", "at": 17}, {"k": "2", "v": "TRA BẢNG ĐIỂM KHỞI ĐỘNG LẠI", "at": [18, "tra"]},
              {"k": "3", "v": "DỰNG LẠI VIỆC QUAN TRỌNG", "at": [18, "dựng"]}]},
    {"type": "source", "at": 19, "source": "AIAA 75-593 · M. HAMILTON & S. ZELDIN · 04/1975", "ref": "“HIGHER ORDER SOFTWARE” · NTRS 19750042668",
     "snippet": "phần mềm hệ thống Apollo: [[bộ lập lịch · mô-đun màn hình · mô-đun khởi động lại]]", "hlAt": 20,
     "seal": "DIỄN Ý TỪ BÀI BÁO · KHÔNG PHẢI TRÍCH NGUYÊN VĂN", "sealAt": 22},
    {"type": "kinetic", "at": 24, "items": [{"text": "SẮP PHẢI LÀM VIỆC", "at": 24, "sm": True}, {"text": "NĂM LẦN LIỀN", "at": [24, "năm"], "acc": True}]},
]}

# ---------------------------------------------------------------- CH03: cuốn nhật ký thứ hai, căn phòng ở Houston
# 22/10/2026 (sửa qa_blank): thẻ trích dẫn chỉ bắt đầu ở câu có chữ gõ; câu dẫn vào có ảnh riêng; thẻ ledger có dòng ngay từ đầu câu
# và đổ thêm nội dung CÓ NGUỒN (factcheck.md mục 4, 30, 33–36). Lời đọc KHÔNG đổi.
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "CUỐN NHẬT KÝ THỨ HAI: CĂN PHÒNG Ở HOUSTON"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "CUỐN NHẬT KÝ THỨ HAI\nCĂN PHÒNG Ở HOUSTON", "sub": "CỘT BÊN PHẢI · CON NGƯỜI", "bg": "mcc",
     "titleAt": [0, "Giờ"]},
    {"type": "photo", "at": 1, "img": "mcctraj", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "GIÁM ĐỐC BAY: GENE KRANZ", "at": [1, "giám"], "acc": True}],
     "label": {"k": "TRUNG TÂM ĐIỀU KHIỂN HOUSTON", "v": "NASA · APOLLO 11", "at": 1}},
    {"type": "photo", "at": 2, "img": "mcc", "tone": "color", "move": "out", "veil": 0.5,
     "kin": [{"text": "BẢN TIN PAO CỦA NASA", "at": 2, "acc": True}, {"text": "ghi lại lời ông kết thúc", "at": [2, "ghi"], "sm": True}],
     "label": {"k": "TRUNG TÂM ĐIỀU KHIỂN HOUSTON", "v": "NASA JSC · S69-40302", "at": 2}},
    {"type": "quote", "at": 3, "text": "Good luck to all of you.", "by": "GENE KRANZ · BẢN TIN PAO · GET 102:12 · TRƯỚC GIỜ ĐỐT ĐỘNG CƠ",
     "lbl": "TRÍCH DỊCH", "qline": 3, "typeAt": [3, "chúc"]},
    {"type": "ledger", "at": 4, "title": "HAI NGƯỜI TRÔNG MÁY TÍNH", "srcnote": "TOMAYKO · NASA CR-182505 · CHƯƠNG 2",
     "rows": [{"k": "TRONG PHÒNG", "v": "HAI NGƯỜI · MỘT CHIẾC MÁY", "at": 4},
              {"k": "STEVE BALES", "v": "THEO DÕI MÁY TÍNH TỪ HOUSTON", "at": [4, "steve"]},
              {"k": "JACK GARMAN", "v": "THEO DÕI MÁY TÍNH TỪ HOUSTON", "at": [4, "jack"]},
              {"k": "BÁO CÁO NASA", "v": "HỌ NHẬN RA NGUỒN GỐC SỰ CỐ", "at": 5}],
     "total": {"k": "NASA GHI", "v": "BALES BÁO GIÁM ĐỐC BAY: GO", "at": 6}},
    {"type": "kinetic", "at": 7, "items": [{"text": "CHƯA ĐẦY MỘT PHÚT", "at": 7, "acc": True}, {"text": "từ đèn báo đến câu trả lời", "at": [7, "chỉ"], "sm": True}]},
    {"type": "ledger", "at": 8, "title": "QUY TẮC VIẾT TRƯỚC CHUYẾN BAY", "srcnote": "NASA SP-238 · MỤC 13",
     "rows": [{"k": "QUY TẮC", "v": "ĐẶT SẴN TRƯỚC KHI BAY", "at": 8},
              {"k": "BÁO ĐỘNG KIỂU NÀY", "v": "KHÔNG TỰ NÓ BUỘC HUỶ", "at": 9},
              {"k": "LÝ DO 1", "v": "KHÔNG XUẤT HIỆN LIÊN TỤC", "at": [11, "không"]},
              {"k": "LÝ DO 2", "v": "MÁY VẪN DẪN ĐƯỜNG ĐÚNG", "at": [11, "máy"]}],
     "total": {"k": "QUYẾT ĐỊNH", "v": "TIẾP TỤC", "at": 12}},
    {"type": "photo", "at": 13, "img": "lm2", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "TRÊN TÀU EAGLE", "at": 13, "sm": True}, {"text": "phi hành đoàn cũng tự quan sát", "at": [13, "phi"], "acc": True}],
     "label": {"k": "TÀU ĐỔ BỘ", "v": "NASA · AS11-44-6643", "at": 13}},
    {"type": "photo", "at": 14, "img": "lm", "tone": "color", "move": "out", "veil": 0.5,
     "kin": [{"text": "BUZZ ALDRIN", "at": [14, "buzz"], "acc": True}, {"text": "phi công module Mặt Trăng · nói với Houston", "at": [14, "nói"], "sm": True}],
     "label": {"k": "TÀU ĐỔ BỘ EAGLE", "v": "NASA · AS11-44-6584", "at": 14}},
    {"type": "quote", "at": 15, "text": "Same alarm, and it appears to come up when we have a 1668 up.",
     "by": "PHI CÔNG MODULE MẶT TRĂNG (BUZZ ALDRIN) · BẢN GHI KHÔNG-ĐỐI-ĐẤT KỸ THUẬT", "lbl": "TRÍCH DỊCH", "qline": 15, "typeAt": [15, "cùng"]},
    {"type": "ledger", "at": 17, "title": "BẢN GHI NHỚ GRUMMAN · 31.07.1969", "srcnote": "GRUMMAN LAV-500-940 · “PROGRAM ALARMS IN POWERED DESCENT” · NỘI BỘ HÃNG",
     "rows": [{"k": "NHÀ CHẾ TẠO", "v": "GRUMMAN · TÀU ĐỔ BỘ", "at": 17},
              {"k": "VIẾT SAU", "v": "11 NGÀY · 31.07 SAU 20.07", "at": [17, "viết"]},
              {"k": "GHI NHẬN", "v": "4 × 1202 · 1 × 1201", "at": [17, "ghi"]},
              {"k": "BÁO ĐỘNG 1", "v": "≈ 12 GIÂY SAU LỆNH THEO DÕI", "at": [18, "hai"]},
              {"k": "BÁO ĐỘNG 2", "v": "≈ 12 GIÂY SAU LỆNH THEO DÕI", "at": [18, "mười"]},
              {"k": "XEM LẦN BA", "v": "≈ 10 GIÂY · KHÔNG BÁO ĐỘNG", "at": 19}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "LỆNH THEO DÕI = GÁNH NẶNG ĐÁNG KỂ", "at": [20, "gánh"], "acc": True},
                                            {"text": "bản ghi nhớ Grumman · Houston đã nhận ra", "at": [20, "houston"], "sm": True}]},
    {"type": "quote", "at": 21, "text": "Eagle, Houston. We'll monitor your DELTA-H.", "by": "HOUSTON · BẢN GHI KHÔNG-ĐỐI-ĐẤT KỸ THUẬT · APOLLO 11",
     "lbl": "TRÍCH DỊCH", "qline": 21, "typeAt": [21, "chúng"]},
    {"type": "kinetic", "at": 22, "items": [{"text": "THEO DÕI ĐỘ CAO: VIỆC CỦA HOUSTON", "at": 22, "acc": True}]},
    {"type": "ledger", "at": 23, "title": "SAU CHUYẾN BAY", "srcnote": "NASA SP-238 · MỤC 16 · GRUMMAN LAV-500-940 TR. 5",
     "rows": [{"k": "NASA", "v": "ĐỔI PHẦN MỀM", "at": 23},
              {"k": "PHI HÀNH ĐOÀN", "v": "VẪN THEO DÕI HẠ CÁNH", "at": [23, "phi"]},
              {"k": "THỜI GIAN MÁY", "v": "TỐN ÍT HƠN", "at": [23, "tốn"]}]},
    {"type": "question", "at": 24, "text": "Vì sao một chiếc radar\nlại làm máy tính quá tải?"},
]}

# ---------------------------------------------------------------- CH04: thủ phạm là radar, cột bên trái
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "THỦ PHẠM LÀ MỘT CÁI RADAR ĐANG KHÔNG CÓ VIỆC"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "THỦ PHẠM LÀ MỘT CÁI RADAR\nĐANG KHÔNG CÓ VIỆC", "sub": "CỘT BÊN TRÁI · CỖ MÁY", "bg": "site", "titleAt": [0, "Con"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "TÍN HIỆU CỦA NÓ LÚC NÀY", "at": 1, "sm": True}, {"text": "VÔ NGHĨA", "at": [1, "hoàn"], "acc": True},
                                           {"text": "báo cáo NASA gọi là “meaningless”", "at": 2, "sm": True}]},
    {"type": "ledger", "at": 3, "title": "MỘT SAI LỆCH NHỎ VỀ ĐIỆN", "srcnote": "NASA SP-238 · MỤC 16 · GRUMMAN LAV-500-940",
     "rows": [{"k": "2 NGUỒN", "v": "28 V · 800 HZ", "at": 4}, {"k": "CÙNG", "v": "TẦN SỐ", "at": [4, "cùng"]}, {"k": "NHƯNG LỆCH", "v": "PHA", "at": [4, "lệch"]}],
     "total": {"k": "HẬU QUẢ", "v": "ĂNG-TEN ĐANG ĐỔI GÓC", "at": 5}},
    {"type": "slam", "at": 7, "text": "11,7 µS", "sub": "MỖI XUNG CHIẾM MỘT NHỊP NHỚ CỦA MÁY · SP-238"},
    {"type": "counter", "at": 8, "from": 0, "to": 12800, "suffix": " XUNG/GIÂY", "until": [8, "nghìn"], "label": "TỐI ĐA TỪ HAI BỘ ĐỔI CỦA RADAR HẸN GẶP",
     "sub": {"text": "6,4 NGHÌN XUNG/GIÂY MỖI BỘ ĐỔI", "at": 8}},
    {"type": "ledger", "at": 9, "title": "PHÉP NHÂN", "srcnote": "NASA SP-238 · KÊNH TỰ NHÂN LẠI: 12.800 × 11,7 µS ≈ 0,15",
     "rows": [{"k": "12.800 XUNG/GIÂY", "v": "× 11,7 µS", "at": 9}, {"k": "=", "v": "≈ 0,15 GIÂY MỖI GIÂY", "at": [9, "nhân"]}],
     "total": {"k": "TỨC", "v": "≈ 15% THỜI GIAN CỦA MÁY", "at": [9, "phần"]}},
    {"type": "bars", "at": 10, "title": "XUNG THỪA · % THỜI GIAN CỦA MÁY", "unit": "GRUMMAN LAV-500-940 · NASA SP-238", "max": 20,
     "items": [{"k": "DỰ PHÒNG KHI THỬ", "v": 10, "lbl": "≈ 10", "at": 10}, {"k": "THỰC TẾ LÚC HẠ CÁNH", "v": 15, "lbl": "≈ 15", "at": [11, "khoản"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "MÁY VỐN ĐÃ CHẠY ≈ 90%", "at": 12}, {"text": "+ 15% XUNG THỪA", "at": [13, "chín"]},
                                            {"text": "= HƠN 100%", "at": [13, "hơn"], "acc": True}]},
    {"type": "ledger", "at": 14, "title": "CHƯƠNG TRÌNH HẠ CÁNH VỚI 15% XUNG", "srcnote": "GRUMMAN LAV-500-940 · TRANG 4",
     "rows": [{"k": "P63 · PHANH", "v": "QUÁ TẢI KHI CÓ THEO DÕI", "at": 14}, {"k": "P64 · TIẾP CẬN CUỐI", "v": "SÁT GIỚI HẠN", "at": 15}]},
    {"type": "timeline", "at": 16, "items": [{"year": "BƯỚC 1", "text": "*xếp lịch* việc dẫn đường mỗi 2 giây", "at": 16},
                                            {"year": "BƯỚC 2", "text": "lần trước *chưa xong*", "at": 18},
                                            {"year": "BƯỚC 3", "text": "*xếp thêm* một bản · xin thêm phòng", "at": 19}]},
    {"type": "ledger", "at": 20, "title": "KHI HẾT CHỖ", "srcnote": "GRUMMAN LAV-500-940 · TRANG 1–2",
     "rows": [{"k": "8", "v": "PHÒNG (CORE SET)", "at": 20}, {"k": "5", "v": "VÙNG VÉC-TƠ (VAC)", "at": [20, "năm"]},
              {"k": "1202", "v": "VIỆC THỨ 9 XIN PHÒNG", "at": 21}, {"k": "1201", "v": "XIN VÙNG VÉC-TƠ KHI ĐÃ HẾT", "at": 22}]},
    {"type": "kinetic", "at": 23, "items": [{"text": "XOÁ DANH SÁCH VIỆC · DỰNG LẠI", "at": 23},
                                            {"text": "không mất vị trí · không mất vận tốc", "at": 24, "sm": True},
                                            {"text": "NĂM LẦN TỰ ĐỨNG DẬY", "at": [26, "năm"], "acc": True}]},
    {"type": "quote", "at": 27, "text": "The Executive overflow alarms that occurred during descent are now known to be normal for the existing situation "
                                        "and are indicative of the proper performance of the guidance computer.",
     "by": "NASA SP-238 · APOLLO 11 MISSION REPORT · MỤC 9", "lbl": "TRÍCH", "typeAt": [27, None, 0, 0.05], "typeDur": 3.4},
    {"type": "slam", "at": 29, "text": "3.000 FEET", "sub": "EAGLE VẪN CÒN PHẢI XUỐNG"},
]}

# ---------------------------------------------------------------- CH05: ba nghìn feet và đồng hồ nhiên liệu
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "BA NGHÌN FEET VÀ ĐỒNG HỒ NHIÊN LIỆU"}, "bgm": {"mood": "epic", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "BA NGHÌN FEET VÀ\nĐỒNG HỒ NHIÊN LIỆU", "sub": "GET 102:42 → 102:45:40", "bg": "lm2", "titleAt": [0, "Houston"]},
    {"type": "ledger", "at": 1, "title": "NĂM LẦN ĐÈN BÁO · GET (GIỜ TÍNH TỪ LÚC PHÓNG)", "srcnote": "NASA SP-238 · BẢNG 5-I (MÁY TỰ GHI)",
     "rows": [{"k": "102:38:22", "v": "1202", "at": 1}, {"k": "102:39:02", "v": "1202", "at": [1, "phi"]}, {"k": "102:42:18", "v": "1201", "at": [2, "ngay"]}]},
    {"type": "quote", "at": 3, "text": "Roger. 1201 alarm. We're GO. Same type. We're GO.", "by": "HOUSTON · BẢN GHI KHÔNG-ĐỐI-ĐẤT KỸ THUẬT · APOLLO 11",
     "lbl": "TRÍCH DỊCH", "qline": 3, "typeAt": [3, "rõ"]},
    {"type": "ledger", "at": 4, "title": "BA LẦN CUỐI · KHÔNG AI CHẠM MÀN HÌNH", "srcnote": "NASA SP-238 · BẢNG 5-I · GRUMMAN LAV-500-940",
     "rows": [{"k": "102:42:43", "v": "1202", "at": 4}, {"k": "102:42:58", "v": "1202", "at": [4, "mười"]},
              {"k": "LỆNH THEO DÕI CỦA PHI HÀNH ĐOÀN", "v": "KHÔNG CÓ", "at": 5}],
     "total": {"k": "3 BÁO ĐỘNG", "v": "TRONG 40 GIÂY", "at": 6}},
    {"type": "photo", "at": 8, "img": "site", "tone": "color", "move": "in", "veil": 0.5, "focus": [0.5, 0.5],
     "kin": [{"text": "DẪN VÀO MỘT MIỆNG HỐ LỚN", "at": 8, "acc": True}],
     "label": {"k": "KHU VỰC HẠ CÁNH APOLLO 11", "v": "ẢNH LRO · NASA", "at": 8}},
    {"type": "ledger", "at": 9, "title": "ARMSTRONG LÁI TAY", "srcnote": "NASA SP-238 · MỤC 5",
     "rows": [{"k": "≈ 600 FT", "v": "BẮT ĐẦU LÁI BẰNG TAY", "at": 9}, {"k": "HƯỚNG", "v": "KÉO TÀU ĐỨNG HƠN · BAY XA", "at": 10}],
     "total": {"k": "KẾT QUẢ", "v": "LỆCH ĐIỂM ≈ 1.100 FT", "at": 11}},
    {"type": "kinetic", "at": 12, "items": [{"text": "MỘT ĐỒNG HỒ KHÁC", "at": 12, "acc": True}, {"text": "đang chạy cùng lúc", "at": [12, "đang"], "sm": True}]},
    {"type": "date", "at": 13, "day": "ĐÈN BÁO NHIÊN LIỆU THẤP · GET", "date": "102:44:30", "sub": {"text": "CÒN ≈ 116 GIÂY ĐỘNG CƠ THEO CẢM BIẾN", "at": 13}},
    {"type": "slam", "at": 15, "text": "60 GIÂY", "sub": "HOUSTON ĐỌC · GET 102:45:02 · BẢN GHI KHÔNG-ĐỐI-ĐẤT"},
    {"type": "slam", "at": 17, "text": "30 GIÂY", "sub": "HOUSTON ĐỌC · GET 102:45:32 · BẢN GHI KHÔNG-ĐỐI-ĐẤT", "white": True},
    {"type": "kinetic", "at": 18, "items": [{"text": "CONTACT LIGHT", "at": 18, "acc": True}, {"text": "ENGINE STOP", "at": 19}]},
    {"type": "slam", "at": 20, "text": "45–50 GIÂY", "sub": "NHIÊN LIỆU CÒN LẠI KHI CHẠM ĐẤT · TÍNH LẠI SAU CHUYẾN BAY · SP-238"},
    {"type": "photo", "at": 21, "img": "lm2", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "TIN ĐẦU TIÊN TỪ MẶT TRĂNG", "at": 21, "acc": True}],
     "label": {"k": "TÀU ĐỔ BỘ · TRÁI ĐẤT · MẶT TRĂNG", "v": "NASA · AS11-44-6643", "at": 21}},
    {"type": "quote", "at": 22, "text": "Houston, Tranquility Base here. The Eagle has landed.", "by": "NEIL ARMSTRONG · BẢN GHI KHÔNG-ĐỐI-ĐẤT KỸ THUẬT",
     "lbl": "TRÍCH DỊCH", "qline": 22, "typeAt": [22, "houston"]},
    {"type": "photo", "at": 23, "img": "mcc", "tone": "color", "move": "in", "veil": 0.5,
     "kin": [{"text": "CÂU TRẢ LỜI CỦA HOUSTON", "at": 23, "acc": True}, {"text": "bản ghi không-đối-đất kỹ thuật", "at": [23, "một"], "sm": True}],
     "label": {"k": "TRUNG TÂM ĐIỀU KHIỂN HOUSTON", "v": "NASA JSC · S69-40302", "at": 23}},
    {"type": "quote", "at": 24, "text": "Roger, Tranquility, we copy you on the ground. You got a bunch of guys about to turn blue. We're breathing again. Thanks a lot.",
     "by": "HOUSTON · BẢN GHI KHÔNG-ĐỐI-ĐẤT KỸ THUẬT", "lbl": "TRÍCH DỊCH", "qline": 24, "typeAt": [24, "rõ"]},
    {"type": "kinetic", "at": 25, "items": [{"text": "“HƠI BẬN, LO VỀ CÁC BÁO ĐỘNG”", "at": [26, "chúng"], "acc": True},
                                            {"text": "từ Eagle · bản tin PAO · GET ≈ 103:03", "at": 25, "sm": True}]},
]}

# ---------------------------------------------------------------- CH06: dòng cuối của hai cuốn nhật ký
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "DÒNG CUỐI CỦA HAI CUỐN NHẬT KÝ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "DÒNG CUỐI CỦA\nHAI CUỐN NHẬT KÝ", "sub": "SAU APOLLO 11", "bg": "mcc", "titleAt": [0, "Vậy"]},
    {"type": "ledger", "at": 1, "title": "NASA SỬA HAI THỨ", "srcnote": "NASA SP-238 · MỤC 13 VÀ 16",
     "rows": [{"k": "1", "v": "TẮT HẲN RADAR HẸN GẶP", "at": 2},
              {"k": "2", "v": "BỎ XUNG VÔ NGHĨA", "at": 4}]},
    {"type": "bars", "at": 6, "title": "BÁO ĐỘNG LÚC HẠ CÁNH", "unit": "SP-238 · BÁO CÁO APOLLO 12 (MSC-01855)", "max": 6,
     "items": [{"k": "APOLLO 11", "v": 5, "lbl": "5", "at": 6}, {"k": "APOLLO 12", "v": 0, "lbl": "0", "at": [6, "không"], "acc": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "CẢI TIẾN CÓ TÁC DỤNG", "at": 7, "acc": True}]},
    {"type": "ledger", "at": 8, "title": "APOLLO 14 · CÔNG TẮC HUỶ NHIỆM VỤ", "srcnote": "BÁO CÁO 5 NGÀY APOLLO 14 (NTRS 19710027929) · TÊN NGƯỜI VÁ: HỒI KÝ MỘT KỸ SƯ MIT",
     "rows": [{"k": "TRƯỚC HẠ", "v": "4 LẦN NHẬN TÍN HIỆU “HUỶ”", "at": 9}, {"k": "CÁCH XỬ LÝ", "v": "NẠP TAY · MÁY BỎ QUA TÍN HIỆU", "at": 10},
              {"k": "NGƯỜI NGHĨ RA", "v": "DON EYLES · THEO HỒI KÝ", "at": 11}]},
    {"type": "quote", "at": 12, "text": "…a philosophy that has appeared deeply embedded in all NASA manned spaceflight software since then.",
     "by": "J. E. TOMAYKO · NASA CR-182505 · 1988", "lbl": "TRÍCH", "typeAt": [12, None, 0, 0.05], "typeDur": 2.6},
    {"type": "ledger", "at": 13, "title": "HAI CUỐN NHẬT KÝ · DÒNG CUỐI", "srcnote": "KÊNH TỰ KẺ BẢNG TỪ NASA SP-238",
     "rows": [{"k": "MÁY", "v": "5 LẦN KÊU · 5 LẦN TỰ KHỞI ĐỘNG LẠI", "at": 14}, {"k": "NGƯỜI", "v": "5 LẦN QUYẾT ĐỊNH VẪN LÀ TIẾP TỤC", "at": 15}],
     "total": {"k": "KẾT QUẢ", "v": "HẠ CÁNH · GET 102:45:40", "at": 15}},
    {"type": "kinetic", "at": 16, "items": [{"text": "KHÔNG CẦN CHẠY HOÀN HẢO", "at": 16}, {"text": "BIẾT ĐỨNG DẬY ĐÚNG CÁCH", "at": 17, "acc": True}]},
    {"type": "question", "at": 18, "text": "Thiết bị của bạn báo động:\ndừng hẳn, hay tự đứng dậy làm tiếp?"},
    {"type": "kinetic", "at": 19, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 19}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [19, "ở"], "acc": True}]},
]}

SPEC = {
    "title": "Apollo 11, Mã 1202: Máy Tính Báo Động 5 Lần Khi Hạ Cánh",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["1202", "1201", "radar", "phòng", "báo", "máy", "người", "tiếp"],
    "say": SAY, "imgs": IMGS, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Apollo 11, Mã 1202: Máy Tính Báo Động 5 Lần Khi Hạ Cánh",
                   "Năm Lần Đèn Báo Động Sáng, Và Houston Chỉ Có Vài Chục Giây Để Quyết Định",
                   "Máy Tính Apollo 11 Nhỏ Hơn Một Bức Ảnh Điện Thoại, Vậy Mà Nó Đưa Hai Người Xuống Mặt Trăng"],
        "summary": "Ngày 20/07/1969, năm phút mười bảy giây sau khi động cơ hạ cánh mở máy, chiếc máy tính dẫn đường của tàu Eagle báo động lần đầu: mã 1202. "
                   "Nó sẽ còn báo bốn lần nữa. Video mở hai cuốn nhật ký cạnh nhau: máy đã tự làm gì mỗi lần kêu, và người ở Houston đã quyết định dựa vào đâu. "
                   "Từ hợp đồng năm 1961 với MIT, bộ nhớ chưa tới 80 kilobyte, bộ điều hành chia việc, tới một con radar gửi xung không có thật "
                   "và đồng hồ nhiên liệu những giây cuối. Mọi giờ, mọi lời thoại lấy từ báo cáo và bản ghi của NASA.",
        "more": ["Giờ báo động (GET, giờ tính từ lúc phóng) lấy từ bảng 5-I của báo cáo NASA SP-238; lời thoại lấy từ bản ghi không-đối-đất kỹ thuật và "
                 "bản tin PAO của NASA (bản quét, giờ từng câu chỉ chắc tới chừng chục giây). Video không dùng bản \"corrected transcript\" có bản quyền. "
                 "Ý nghĩa mã 1201 và 1202, ô nhớ dùng chung bảy việc và tên người vá Apollo 14 dựa trên hồi ký của một kỹ sư MIT, chỉ có một nguồn. "
                 "Vai Bales, Garman, Kranz chỉ nêu những gì tài liệu NASA ghi; vai Margaret Hamilton chỉ nêu qua bài báo kỹ thuật năm 1975 của chính bà. "
                 "Các con số dung lượng bộ nhớ, tải 90% + 15% và phép nhân 12.800 xung do kênh tự tính từ số liệu của NASA."],
        "chapter_titles": {"ch00": "Mở đầu: đèn báo thứ nhất", "ch01": "Chiếc máy đặt hàng khi chưa có bản vẽ", "ch02": "Cỗ máy không bao giờ làm một việc",
                           "ch03": "Cuốn nhật ký thứ hai: căn phòng ở Houston", "ch04": "Thủ phạm là một cái radar đang không có việc",
                           "ch05": "Ba nghìn feet và đồng hồ nhiên liệu", "ch06": "Dòng cuối của hai cuốn nhật ký"},
        "sources": [
            "https://ntrs.nasa.gov/citations/19710015566",
            "https://www.nasa.gov/history/mission-transcripts-mercury-gemini-and-apollo/",
            "https://www.nasa.gov/wp-content/uploads/static/history/computers/Ch2-2.html",
            "https://www.nasa.gov/wp-content/uploads/static/history/computers/Ch2-5.html",
            "https://www.nasa.gov/wp-content/uploads/static/history/computers/Ch2-6.html",
            "https://ntrs.nasa.gov/citations/19750042668",
            "https://ntrs.nasa.gov/citations/19760072997",
            "https://ntrs.nasa.gov/citations/19710027929",
            "https://history.nasa.gov/wp-content/uploads/static/history/alsj/a11/a11.1201-pa.html",
        ],
        "hashtags": ["Apollo11", "MáyTínhApollo", "CôngNghệ", "CôngNghệQuanhTa", "MindInTheMachine"],
        "tags": ["mã 1202", "apollo 11", "máy tính dẫn đường apollo", "báo động 1202", "hạ cánh mặt trăng", "eagle hạ cánh", "lịch sử máy tính",
                 "công nghệ quanh ta", "lịch sử công nghệ", "apollo guidance computer"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Ảnh NASA (phần lớn thuộc phạm vi công cộng); ảnh máy tính dẫn đường Apollo: Steve Jurvetson, CC BY 2.0 (ghi tự động theo ảnh)"],
    },
}


def _norm(w):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


def _anchors(o, path=""):
    """Duyệt mọi mốc dạng int / [dòng, từ, n, lệch] để kiểm tra. Khoá nhận mốc: at, *At, until, hlAt..."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("at", "until", "titleAt", "hlAt", "sealAt", "typeAt", "qline") or k.endswith("At"):
                yield (path + "/" + k, v)
            else:
                yield from _anchors(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _anchors(v, path + f"[{i}]")


def check():
    """Kiểm neo với lines (sau script_lines.py): lỗi nếu dòng không có, hoặc từ neo không nằm trong dòng. Trả về danh sách lỗi."""
    bad = []
    for name, c in CH.items():
        f = D / f"{name}.json"
        if not f.exists():
            bad.append(f"{name}: chưa có {f.name} (chạy script_lines.py trước)")
            continue
        lines = json.loads(f.read_text(encoding="utf-8"))["lines"]
        text = [(x if isinstance(x, str) else x["t"]) for x in lines]
        for si, s in enumerate(c["scenes"]):
            for p, v in _anchors(s):
                if isinstance(v, bool) or not isinstance(v, (int, list)):
                    continue
                cands = v if (isinstance(v, list) and v and isinstance(v[0], list)) else [v]
                for a in cands:
                    i = a if isinstance(a, int) else (a[0] if a else None)
                    if not isinstance(i, int) or isinstance(i, bool) or not (0 <= i < len(text)):
                        bad.append(f"{name} cảnh {si} {p}: dòng {a!r} ngoài phạm vi 0..{len(text) - 1}")
                        continue
                    if isinstance(a, list) and len(a) > 1 and isinstance(a[1], str):
                        toks = [_norm(t) for t in text[i].split()]
                        n = a[2] if len(a) > 2 else 0
                        if toks.count(_norm(a[1])) <= n:
                            bad.append(f"{name} cảnh {si} {p}: dòng {i} không có chữ {a[1]!r} (lần {n}): {text[i]}")
    return bad


def main():
    (D / "spec.json").write_text(json.dumps(SPEC, ensure_ascii=False, indent=1), encoding="utf-8")
    for name, c in CH.items():
        p = D / f"{name}.json"
        d = json.loads(p.read_text(encoding="utf-8"))
        d.update(c)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print("spec +", len(CH), "chương")
    bad = check()
    if bad:
        print("NEO LỖI:\n  " + "\n  ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
