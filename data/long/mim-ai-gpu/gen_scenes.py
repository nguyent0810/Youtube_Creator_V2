"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM #6 "GPU: Con Chip Chơi Game Đã Trở Thành Trái Tim Của AI Như Thế Nào?".

    python data/long/mim-ai-gpu/gen_scenes.py        # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md (bản 2, đã kiểm chứng) + factcheck.md. Dữ kiện + nguồn: docs/channels/mind-in-the-machine/2026-10-09-long-06-research.md.
Ảnh: chỉ PD / CC0 / CC BY (kênh MIM không nhận BY-SA). Clip: Pexels (ngang), gắn "VIDEO MINH HỌA".
Video đầu tiên chạy beat2 (spec "beat2": true): bố cục cảnh chữ xoay vòng, từ nhấn, sync 1/3 cảnh — chữ trên màn hình là
TỪ KHOÁ / CON SỐ / VẾ ĐỐI LẬP, không chép nguyên câu đọc (build_long cảnh báo khi > 40%).
BƯỚC 1 (09/10): chỉ spec để thu giọng; scenes viết sau khi có timing.json.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

IMGS = {
    "gf256": "File:VisionTek GeForce 256.jpg",                     # Public domain
    "jensen": "File:Jensen Huang (cropped) (2024).jpg",            # CC BY 4.0
    "feifei": "File:Fei-Fei Li at AI for Good 2017.jpg",           # CC BY 2.0
    "hinton": "File:Geoffrey Hinton at Collision 2024 in Toronto (cropped).jpg",   # CC BY 2.0 (ảnh Nobel trên Commons là BY-SA -> không dùng)
    "sutskever": "File:Naveen Rao and Ilya Sutskever Stanford 2014.jpg",           # CC BY 2.0
    "gf110": "File:NVIDIA@40nm@Fermi@GF110@GeForce GTX 580@UA10B338 1041A1 N2Y540.000 GF110-375-A1 Stack-DSC06316-DSC06399 - ZS-retouched (27576810474).jpg",  # CC0, nhân GTX 580
    "gp100": "File:Nvidia@16nm@Pascal@GP100@Tesla P100@T Taiwan 1912A1 PN9G70.S6W GP100-897-A1 DSC06333-DSC06333.jpg",   # CC0, GPU trong DGX-1
}

SAY = {
    "krizhevsky": "Cri-giép-xki", "sutskever": "Xút-xke-vơ", "hinton": "Hin-tơn", "nvidia": "En-vi-đi-a", "geforce": "Di-pho",
    "cuda": "Cu-đa", "jensen": "Gien-xần", "huang": "Hoang", "malachowsky": "Ma-la-cốp-xki", "priem": "Prim", "curtis": "Cớt-tịt",
    "chris": "Crít", "denny's": "Đen-nis", "toronto": "Tô-rôn-tô", "san": "Xan", "jose": "Hô-dê", "california": "Ca-li-phoóc-ni-a",
    "mythbusters": "Mít-bớt-tơ", "mona": "Mô-na", "lisa": "Li-da", "imagenet": "Im-mịt-nét", "alexnet": "A-léch-nét",
    "alex": "A-léch", "ilya": "I-li-a", "andrew": "An-đru", "ng": "Ng", "stanford": "Xten-phơ", "openai": "Âu-pần Ây-ai",
    "dgx-1": "Đi-gi-ích một", "chatgpt": "Chát-gi-pi-ti", "gtx": "Gi-ti-ích", "rtx": "A-ti-ích", "vinbrain": "Vin-brên",
    "full": "Phun", "hd": "ếch-đi", "gpu": "Gi-pi-iu", "cpu": "Xi-pi-iu", "ian": "I-an", "buck": "Bắc", "brook": "Brúc",
    "fei-fei": "Phây-phây", "li": "Li", "geoffrey": "Giép-phri", "francisco": "Phran-xít-xcô", "google": "Gu-gồ",
    "tahoe": "Ta-hô", "cade": "Kết", "metz": "Mét", "viettel": "Viettel", "gigabyte": "gi-ga-bai",
}

VM = "VIDEO MINH HỌA"
NIPS = "KRIZHEVSKY, SUTSKEVER, HINTON · NEURIPS 2012"
CHM = "BẢO TÀNG LỊCH SỬ MÁY TÍNH (CHM) · IEEE SPECTRUM 03.2025"
CH = {}

# ---------------- CH00 · Hai chiếc card trong phòng ngủ ----------------
CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI CHIẾC CARD TRONG PHÒNG NGỦ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "date", "day": "TORONTO · CANADA", "date": "2012"},
    {"type": "broll", "at": 1, "vid": "10620285", "veil": 0.55, "illus": VM,
     "kin": [{"text": "PHÒNG NGỦ · NHÀ BỐ MẸ", "at": 1, "sm": True}, {"text": "CHẠY SUỐT NHIỀU NGÀY", "at": [1, "chạy"], "acc": True}]},
    {"type": "photo", "at": 2, "img": "gf110", "tone": "color", "focus": [0.5, 0.5], "move": "in", "veil": 0.45,
     "kin": [{"text": "2 × GTX 580", "at": [2, "hai"]}, {"text": "card chơi game · ~499 USD mỗi chiếc lúc ra mắt (2010)", "at": [2, "năm"], "sm": True}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "ALEX KRIZHEVSKY", "at": 3, "acc": True}, {"text": "nghiên cứu sinh · Đại học Toronto", "at": [3, "nghiên"], "sm": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "KHÔNG CHƠI GAME", "at": 4, "fx": "strike", "strikeAt": [5, "dạy"]},
                                          {"text": "DẠY MÁY NHÌN ẢNH", "at": [5, "dạy"], "acc": True}]},
    {"type": "counter", "at": 6, "from": 0, "to": 1200000, "prefix": "> ", "suffix": " ẢNH", "label": "GỌI TÊN · 1.000 LOẠI",
     "sub": {"text": "CUỘC THI ILSVRC 2012 · DỮ LIỆU IMAGENET", "at": 6}},
    {"type": "kinetic", "at": 7, "items": [{"text": "MÈO", "at": [7, "mèo"]}, {"text": "NẤM", "at": [7, "nấm"]},
                                          {"text": "XE CỨU HOẢ", "at": [7, "xe"]}, {"text": "CON VE", "at": [7, "ve"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "ĐOÁN 5 LẦN", "at": 8, "acc": True}, {"text": "trượt cả năm = sai", "at": [8, "không"], "sm": True}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "5–6 NGÀY", "at": 9, "acc": True}, {"text": "huấn luyện trên 2 card · " + NIPS, "at": [9, "huấn"], "sm": True}]},
    {"type": "bars", "at": 11, "title": "TỈ LỆ SAI (TOP-5) · CÀNG THẤP CÀNG TỐT",
     "items": [{"k": "ĐỘI THỨ HAI", "v": 26.2, "lbl": "26,2%", "at": 11}, {"k": "ALEXNET", "v": 15.3, "lbl": "15,3%", "at": 12, "acc": True}],
     "label": {"k": "NGUỒN", "v": NIPS, "at": 11}},
    {"type": "slam", "at": 13, "text": "MỘT CÚ NHẢY", "sub": "CÁC ĐỘI THƯỜNG HƠN NHAU VÀI ĐIỂM"},
    {"type": "kinetic", "at": 14, "items": [{"text": "NGƯỜI CHỈ CHO MÁY", "at": 14}, {"text": "cạnh · góc · mảng màu", "at": [14, "cạnh"], "sm": True},
                                           {"text": "MÁY TỰ HỌC", "at": 15, "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "2012", "at": 16, "acc": True}, {"text": "AI HIỆN ĐẠI BẮT ĐẦU", "at": [16, "trí"]}]},
    {"type": "question", "at": 18, "text": "Đồ vẽ game\nsao thành thứ quý nhất của AI?"},
    {"type": "brand", "at": 19, "sub": "QUAY LẠI 20 NĂM · MỘT QUÁN ĂN VEN ĐƯỜNG"},
]}

# ---------------- CH01 · Một quán ăn ven đường ----------------
CH["ch01"] = {"hud": {"k": "CHƯƠNG 01", "t": "MỘT QUÁN ĂN VEN ĐƯỜNG"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHƯƠNG MỘT", "title": "MỘT QUÁN ĂN\nVEN ĐƯỜNG", "sub": "SAN JOSE · CUỐI 1992", "vid": "36139323", "illus": VM, "titleAt": [0, "san"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "DENNY'S", "at": 1, "acc": True}, {"text": "mở thâu đêm · cà phê rót thêm miễn phí", "at": [1, "mở"], "sm": True}]},
    {"type": "ledger", "at": 2, "title": "BA NGƯỜI SÁNG LẬP", "rows": [{"k": "1", "v": "JENSEN HUANG", "at": [2, "jensen"]},
                                                                      {"k": "2", "v": "CHRIS MALACHOWSKY", "at": [2, "chris"]},
                                                                      {"k": "3", "v": "CURTIS PRIEM", "at": [2, "curtis"]}]},
    {"type": "date", "at": 4, "day": "CÔNG TY RA ĐỜI · NVIDIA", "date": "04.1993"},
    {"type": "kinetic", "at": 5, "items": [{"text": "MỤC TIÊU", "at": 5, "sm": True}, {"text": "CHIP ĐỒ HOẠ 3D", "at": [5, "chip"], "acc": True},
                                          {"text": "cho máy tính cá nhân", "at": [5, "máy"], "sm": True}]},
    {"type": "broll", "at": 6, "vid": "7914862", "veil": 0.55, "illus": VM,
     "kin": [{"text": "GAME 3D ĐANG LÊN", "at": 6}, {"text": "VIỆC CỰC NẶNG", "at": [6, "cực"], "acc": True}]},
    {"type": "print", "at": 7, "img": "gf256", "side": {"k": "1999", "h": "GEFORCE 256", "hAt": 7,
     "lines": [{"text": "“GPU đầu tiên trên thế giới”", "at": 8}, {"text": "tên do chính Nvidia đặt và định nghĩa", "at": 9}]}},
    {"type": "kinetic", "at": 9, "items": [{"text": "LỜI QUẢNG CÁO", "at": [9, "quảng"], "acc": True}, {"text": "→ TÊN CẢ NGÀNH DÙNG", "at": 10}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "NHIỆM VỤ", "at": 11, "sm": True}, {"text": "NHANH · MƯỢT", "at": [11, "nhanh"], "acc": True}]},
    {"type": "kinetic", "at": 12, "items": [{"text": "TRÍ TUỆ NHÂN TẠO?", "at": [12, "trí"], "fx": "strike", "strikeAt": [12, "tạo"]},
                                           {"text": "chưa ai nhắc tới", "at": [12, "không"], "sm": True}]},
    {"type": "question", "at": 13, "text": "Một khung hình\nđược vẽ ra thế nào?"},
]}

# ---------------- CH02 · Hai triệu điểm ảnh ----------------
CH["ch02"] = {"hud": {"k": "CHƯƠNG 02", "t": "HAI TRIỆU ĐIỂM ẢNH"}, "bgm": {"mood": "upbeat", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHƯƠNG HAI", "title": "HAI TRIỆU\nĐIỂM ẢNH", "sub": "FULL HD · 60 KHUNG HÌNH MỖI GIÂY", "vid": "5466792", "illus": VM, "titleAt": [0, "full"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "1.920 × 1.080", "at": 1, "acc": True}, {"text": "ngang × dọc", "at": [1, "dọc"], "sm": True}]},
    {"type": "counter", "at": 2, "from": 0, "to": 2073600, "suffix": " ĐIỂM ẢNH", "label": "MỘT KHUNG HÌNH"},
    {"type": "broll", "at": 3, "vid": "36139323", "veil": 0.5, "illus": VM,
     "kin": [{"text": "ÁNH SÁNG · BÓNG ĐỔ · PHẢN CHIẾU", "at": 3}, {"text": "MỖI ĐIỂM ẢNH MỘT PHÉP TÍNH", "at": [3, "mỗi"], "acc": True}]},
    {"type": "counter", "at": 4, "from": 0, "to": 124416000, "prefix": "> ", "suffix": " / GIÂY", "label": "2.073.600 ĐIỂM × 60 KHUNG HÌNH",
     "sub": {"text": "KÊNH TỰ TÍNH", "at": 5}},
    {"type": "kinetic", "at": 6, "items": [{"text": "GIỐNG HỆT NHAU", "at": [6, "giống"], "acc": True}, {"text": "chỉ khác con số đầu vào", "at": 7, "sm": True},
                                          {"text": "KHÔNG CHỜ NHAU", "at": [8, "không"]}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "MỘT NHÀ BẾP", "at": 9, "acc": True}]},
    {"type": "dots", "at": 10, "total": 120, "cols": 20, "title": "MỘT NHÀ BẾP",
     "groups": [{"from": 0, "n": 4, "cls": "gold", "label": "CPU · VÀI ĐẦU BẾP GIỎI", "at": 10},
                {"from": 4, "n": 116, "cls": "red", "label": "GPU · HÀNG NGHÌN PHỤ BẾP", "at": [12, "gpu"]}],
     "srcnote": "HÌNH ẢNH SO SÁNH · KHÔNG PHẢI SỐ LÕI THẬT"},
    {"type": "kinetic", "at": 13, "items": [{"text": "MỘT VIỆC ĐƠN GIẢN", "at": 13, "sm": True}, {"text": "THÁI HÀNH", "at": [13, "thái"], "acc": True}]},
    {"type": "slam", "at": 14, "text": "MỘT NÚI HÀNH", "sub": "HÀNG NGHÌN NGƯỜI LÀM CÙNG LÚC"},
    {"type": "kinetic", "at": 15, "items": [{"text": "GPU > CPU ?", "at": 15, "fx": "strike", "strikeAt": [15, "cpu"]}, {"text": "KHÔNG PHẢI", "at": [15, "không"], "acc": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "ĐẦU BẾP", "at": 17, "acc": True}, {"text": "VIỆC RẼ NHÁNH", "at": [17, "rẽ"], "sm": True},
                                           {"text": "PHỤ BẾP", "at": [17, "phụ"], "acc": True}, {"text": "VIỆC LẶP LẠI", "at": [17, "lặp"], "sm": True}]},
    {"type": "kinetic", "at": 18, "items": [{"text": "VẼ GAME", "at": 18}, {"text": "→ PHỤ BẾP", "at": [18, "phụ"], "acc": True}]},
    {"type": "date", "at": 19, "day": "NVISION 08 · SAN JOSE · MYTHBUSTERS", "date": "08.2008"},
    {"type": "kinetic", "at": 20, "items": [{"text": "MÁY 1", "at": 20, "sm": True}, {"text": "TỪNG VIÊN MỘT", "at": [20, "từng"]}]},
    {"type": "counter", "at": 21, "from": 0, "to": 1100, "suffix": " NÒNG", "label": "MÁY 2 · BẮN CÙNG MỘT LÚC"},
    {"type": "slam", "at": 22, "text": "< 0,1 GIÂY", "sub": "BỨC MONA LISA HIỆN RA · KỂ LẠI, KHÔNG PHẢI HÌNH GỐC"},
    {"type": "kinetic", "at": 23, "items": [{"text": "1 VIÊN BI = 1 ĐIỂM ẢNH", "at": 23, "acc": True}]},
    {"type": "question", "at": 24, "text": "Thay điểm ảnh\nbằng con số khác?"},
]}

# ---------------- CH03 · Giả làm bức tranh ----------------
CH["ch03"] = {"hud": {"k": "CHƯƠNG 03", "t": "GIẢ LÀM BỨC TRANH"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHƯƠNG BA", "title": "GIẢ LÀM\nBỨC TRANH", "sub": "ĐẦU NHỮNG NĂM 2000 · GPGPU", "vid": "7140937", "illus": VM, "titleAt": [0, "card"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "SỨC MẠNH BỎ PHÍ", "at": 1, "acc": True}]},
    {"type": "ledger", "at": 2, "title": "MUỐN TÍNH THỨ KHÁC", "rows": [{"k": "1", "v": "DÒNG CHẢY CHẤT LỎNG", "at": [2, "dòng"]},
                                                                      {"k": "2", "v": "SÓNG ĐỊA CHẤN", "at": [2, "sóng"]},
                                                                      {"k": "3", "v": "PHÂN TỬ THUỐC", "at": [2, "phân"]}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "CHỈ HIỂU MỘT NGÔN NGỮ", "at": 3, "sm": True}, {"text": "HÌNH VẼ", "at": [3, "hình"], "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "CON SỐ → MÀU ĐIỂM ẢNH", "at": 5}, {"text": "BÀI TOÁN → HIỆU ỨNG ÁNH SÁNG", "at": [5, "bài"], "acc": True}]},
    {"type": "slam", "at": 6, "text": "TƯỞNG ĐANG VẼ", "sub": "THẬT RA ĐANG LÀM TOÁN"},
    {"type": "kinetic", "at": 8, "items": [{"text": "VẬT LÝ", "at": 8}, {"text": "+ MẸO DÂN LÀM GAME", "at": [8, "mẹo"], "acc": True}]},
    {"type": "file", "at": 9, "k": "STANFORD · NGHIÊN CỨU SINH", "name": "Ian Buck", "desc": "Mê card đồ hoạ từ hồi chơi game",
     "rows": [{"k": "VIẾT", "v": "ngôn ngữ *Brook*", "at": 11}, {"k": "2004", "v": "về *Nvidia*, dẫn một nhóm nhỏ", "at": 12}],
     "label": {"k": "NGUỒN", "v": "HPCWIRE · 35 HPC LEGENDS", "at": 12}},
    {"type": "date", "at": 13, "day": "NVIDIA RA MẮT CUDA · GEFORCE 8800", "date": "08.11.2006"},
    {"type": "kinetic", "at": 14, "items": [{"text": "RA LỆNH TÍNH TRỰC TIẾP", "at": 14, "acc": True},
                                           {"text": "GIẢ LÀM BỨC TRANH", "at": [14, "giả"], "fx": "strike", "strikeAt": [14, "nữa"]}]},
    {"type": "slam", "at": 15, "text": "MỘT CANH BẠC"},
    {"type": "quote", "at": 16, "text": "Mỗi con chip gánh thêm chi phí cho phần tính toán, trong khi phần lớn người mua chỉ cần chơi game.",
     "by": "JENSEN HUANG KỂ LẠI · LEX FRIDMAN PODCAST", "lbl": "DIỄN Ý", "qline": 16},
    {"type": "kinetic", "at": 18, "items": [{"text": "KHÁCH HÀNG CUDA", "at": 18, "sm": True}, {"text": "PHÒNG THÍ NGHIỆM KHOA HỌC", "at": [18, "phòng"], "acc": True}]},
    {"type": "question", "at": 19, "text": "Ai cần\nmột núi phép nhân?"},
]}

# ---------------- CH04 · Một núi phép nhân ----------------
CH["ch04"] = {"hud": {"k": "CHƯƠNG 04", "t": "MỘT NÚI PHÉP NHÂN"}, "bgm": {"mood": "curious", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "MỘT NÚI\nPHÉP NHÂN", "sub": "MẠNG NƠ-RON TỪ BÊN TRONG", "vid": "1085656", "illus": VM, "titleAt": [0, "mạng"]},
    {"type": "kinetic", "at": [0, "nhưng"], "items": [{"text": "BỘ NÃO", "at": [0, "nhưng"], "fx": "strike", "strikeAt": [0, "bảng"]}, {"text": "BẢNG TÍNH KHỔNG LỒ", "at": [0, "bảng"], "acc": True}]},
    {"type": "kinetic", "at": 1, "items": [{"text": "1 KẾT NỐI = 1 CON SỐ", "at": 1, "acc": True}, {"text": "trọng số", "at": [1, "trọng"], "sm": True}]},
    {"type": "ledger", "at": 2, "title": "MỘT LỚP", "rows": [{"k": "1", "v": "ẢNH × TRỌNG SỐ", "at": [2, "nhân"]}, {"k": "2", "v": "CỘNG LẠI", "at": [2, "cộng"]},
                                                         {"k": "3", "v": "SANG LỚP SAU", "at": [2, "chuyển"]}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "ĐOÁN SAI → CHỈNH → ĐOÁN LẠI", "at": 4, "acc": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "MÈO", "at": 5}, {"text": "→ “CÁO”", "at": [5, "cáo"], "acc": True}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "LẦN NGƯỢC", "at": 6, "acc": True}, {"text": "vặn mỗi trọng số một chút", "at": [6, "vặn"], "sm": True}]},
    {"type": "counter", "at": 7, "from": 0, "to": 90, "prefix": "≈ ", "suffix": " LƯỢT", "label": "LẶP LẠI CẢ BỘ > 1 TRIỆU ẢNH", "sub": {"text": NIPS, "at": 7}},
    {"type": "counter", "at": 8, "from": 0, "to": 60000000, "suffix": " TRỌNG SỐ", "label": "MẠNG CỦA ALEX", "sub": {"text": NIPS, "at": 8}},
    {"type": "slam", "at": 9, "text": "HÀNG TRĂM TRIỆU PHÉP NHÂN", "sub": "CHO MỖI BỨC ẢNH"},
    {"type": "kinetic", "at": 10, "items": [{"text": "NHỎ · GIỐNG NHAU · KHÔNG CHỜ NHAU", "at": [10, "hàng"], "acc": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "NÚI HÀNH", "at": 11, "acc": True}, {"text": "chờ hàng nghìn phụ bếp", "at": [11, "chờ"], "sm": True}]},
    {"type": "file", "at": 12, "k": "ICML 2009 · RAINA, MADHAVAN, NG", "name": "Đại học Stanford", "desc": "Dạy mạng nơ-ron trên card đồ hoạ",
     "rows": [{"k": "TỐC ĐỘ", "v": "nhanh hơn *tới 55 lần*", "at": 13}, {"k": "SO VỚI", "v": "CPU 2 lõi thời ấy", "at": [13, "hai"]},
              {"k": "THỜI GIAN", "v": "*vài tuần → ~1 ngày*", "at": 14}],
     "label": {"k": "LƯU Ý", "v": "TRONG BÀI TOÁN HỌ CHỌN", "at": 13}},
    {"type": "kinetic", "at": 15, "items": [{"text": "TỐC ĐỘ", "at": 15}, {"text": "CHƯA ĐỦ", "at": [15, "chưa"], "acc": True}]},
    {"type": "kinetic", "at": 16, "items": [{"text": "THỨ HAI", "at": 16, "sm": True}, {"text": "RẤT NHIỀU ẢNH CÓ TÊN", "at": [16, "rất"], "acc": True}]},
]}

# ---------------- CH05 · Lời giải ----------------
CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "LỜI GIẢI"}, "bgm": {"mood": "warm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "LỜI GIẢI", "sub": "IMAGENET · ALEXNET · 2012", "vid": "5028622", "illus": VM, "titleAt": [0, "năm"]},
    {"type": "print", "at": [0, "bắt"], "img": "feifei", "side": {"k": "2006", "h": "FEI-FEI LI", "hAt": [0, "bắt"],
     "lines": [{"text": "ảnh cho mọi danh từ tiếng Anh", "at": 1}, {"text": "người gọi tên từng ảnh", "at": [1, "nhờ"]}]}},
    {"type": "date", "at": 2, "day": "IMAGENET HOÀN THÀNH", "date": "2009"},
    {"type": "ledger", "at": 4, "title": "BA THỨ GẶP NHAU · 2012", "rows": [{"k": "1", "v": "DỮ LIỆU · IMAGENET", "at": 5},
                                                                           {"k": "2", "v": "THUẬT TOÁN · HINTON", "at": 6},
                                                                           {"k": "3", "v": "2 CARD GAME · CUDA", "at": 7}]},
    {"type": "kinetic", "at": 9, "items": [{"text": "3 GB", "at": 9, "acc": True}, {"text": "không chứa nổi cả mạng", "at": [9, "không"], "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "CẮT ĐÔI", "at": 10, "acc": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "NỬA TRÁI · CARD 1", "at": 11}, {"text": "NỬA PHẢI · CARD 2", "at": [11, "kia"]},
                                           {"text": "chỉ nói chuyện ở vài tầng", "at": [11, "trao"], "sm": True}]},
    {"type": "slam", "at": 12, "text": "HAI BÁN CẦU", "sub": NIPS + " · §3.2"},
    {"type": "kinetic", "at": 13, "items": [{"text": "> 1 NĂM", "at": 13, "acc": True}, {"text": "chỉnh → dạy lại → chỉnh → dạy lại", "at": [13, "chỉnh"], "sm": True}]},
    {"type": "question", "at": 14, "text": "Vậy lời giải\nlà gì?"},
    {"type": "kinetic", "at": 15, "items": [{"text": "THÔNG MINH", "at": [15, "thông"], "fx": "strike", "strikeAt": [16, "mà"]},
                                           {"text": "CÙNG MỘT KIỂU VIỆC", "at": [16, "cùng"], "acc": True}]},
    {"type": "kinetic", "at": 17, "items": [{"text": "VẼ KHUNG HÌNH = DẠY MẠNG NƠ-RON", "at": 17, "acc": True},
                                           {"text": "hàng triệu phép tính nhỏ, làm cùng lúc", "at": [17, "hàng"], "sm": True}]},
    {"type": "slam", "at": 18, "text": "ĐIỂM ẢNH = TRỌNG SỐ", "sub": "VỚI CON CHIP, CHỈ LÀ NHỮNG CON SỐ"},
    {"type": "kinetic", "at": 19, "items": [{"text": "ALEXNET", "at": [19, "alexnet"], "acc": True}]},
    {"type": "print", "at": 20, "img": "hinton", "side": {"k": "2024", "h": "NOBEL VẬT LÝ", "hAt": 20,
     "lines": [{"text": "Geoffrey Hinton", "at": 20}, {"text": "2025: CHM công bố mã nguồn AlexNet", "at": 21}]}},
    {"type": "quote", "at": 22, "text": "Ilya thought we should do it, Alex made it work, and I got the Nobel prize.",
     "by": "GEOFFREY HINTON · " + CHM, "lbl": "TRÍCH DỊCH", "qline": 22},
    {"type": "print", "at": 23, "img": "sutskever", "side": {"k": "NHÓM ALEXNET", "h": "ILYA SUTSKEVER", "hAt": [23, "ilya"],
     "lines": [{"text": "nghiên cứu sinh thứ hai", "at": [23, "nghiên"]}]}},
    {"type": "kinetic", "at": 24, "items": [{"text": "VÀI THÁNG SAU", "at": 24, "sm": True}, {"text": "MÓN HÀNG ĐẮT GIÁ NHẤT", "at": [24, "món"], "acc": True}]},
]}

# ---------------- CH06 · Từ phòng ngủ đến siêu máy tính ----------------
CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "TỪ PHÒNG NGỦ ĐẾN SIÊU MÁY TÍNH"}, "bgm": {"mood": "epic", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "TỪ PHÒNG NGỦ\nĐẾN SIÊU MÁY TÍNH", "sub": "2012 → 2022", "vid": "3147349", "illus": VM, "titleAt": [0, "tháng"]},
    {"type": "date", "at": [0, "khách"], "day": "HỒ TAHOE · ĐẤU GIÁ KÍN", "date": "12.2012"},
    {"type": "file", "at": 1, "k": "THEO LỜI KỂ CỦA CADE METZ", "name": "Công ty 3 người", "desc": "Lập vội · chưa có sản phẩm",
     "rows": [{"k": "NGƯỜI", "v": "Hinton · Alex · Ilya", "at": [1, "hinton"]}, {"k": "TRẢ GIÁ", "v": "*4 công ty* · qua thư điện tử", "at": 2},
              {"k": "BƯỚC GIÁ", "v": "≥ 1 triệu USD", "at": [2, "mỗi"]}],
     "label": {"k": "NGUỒN", "v": "WIRED 2021 · GENIUS MAKERS", "at": 2}},
    {"type": "counter", "at": 3, "from": 0, "to": 44000000, "suffix": " USD", "label": "HINTON DỪNG Ở ĐÂY · CHỌN GOOGLE"},
    {"type": "kinetic", "at": 4, "items": [{"text": "GIÁ CAO NHẤT", "at": 4, "fx": "strike", "strikeAt": [4, "hơn"]}, {"text": "NƠI HỢP NGHIÊN CỨU", "at": [4, "nơi"], "acc": True}]},
    {"type": "broll", "at": 5, "vid": "7380236", "veil": 0.55, "illus": VM,
     "kin": [{"text": "PHÒNG THÍ NGHIỆM AI", "at": 5, "sm": True}, {"text": "ĐUA NHAU MUA CARD", "at": [5, "đua"], "acc": True}]},
    {"type": "date", "at": 6, "day": "SAN FRANCISCO · GIAO TẬN TAY", "date": "08.2016"},
    {"type": "kinetic", "at": 7, "items": [{"text": "OPENAI", "at": 7, "acc": True}, {"text": "mới thành lập vài tháng · Sutskever đồng sáng lập", "at": [7, "ilya"], "sm": True}]},
    {"type": "photo", "at": 8, "img": "gp100", "tone": "color", "focus": [0.5, 0.5], "move": "in", "veil": 0.5,
     "kin": [{"text": "DGX-1", "at": [8, "dgx-1"], "acc": True}, {"text": "8 GPU XẾP SÁT NHAU", "at": 9}]},
    {"type": "date", "at": 10, "day": "CHÍNH PHÒNG THÍ NGHIỆM ẤY RA MẮT CHATGPT", "date": "30.11.2022"},
    {"type": "timeline", "at": 11, "items": [{"year": "2012", "text": "*2 card* · phòng ngủ", "at": [11, "hai"]},
                                            {"year": "2016", "text": "*8 GPU* · một chiếc hộp", "at": [11, "tám"]},
                                            {"year": "NAY", "text": "*hàng nghìn GPU* · toà nhà", "at": [11, "toà"]}]},
    {"type": "bars", "at": 13, "title": "LÕI TÍNH TOÁN · CARD CHƠI GAME", "unit": "",
     "items": [{"k": "GTX 580 · 2010", "v": 512, "at": 14}, {"k": "RTX 4090 · 2022", "v": 16384, "at": 15, "acc": True}],
     "label": {"k": "NGUỒN", "v": "THÔNG SỐ CỦA NVIDIA", "at": 14}},
    {"type": "slam", "at": 16, "text": "× 32", "sub": "TRONG 12 NĂM"},
    {"type": "kinetic", "at": 17, "items": [{"text": "LÕI GPU ≠ LÕI CPU", "at": 17, "acc": True}, {"text": "nhỏ và đơn giản hơn nhiều", "at": [18, "nhỏ"], "sm": True}]},
    {"type": "broll", "at": 19, "vid": "5028622", "veil": 0.5, "illus": VM,
     "kin": [{"text": "NHÀ BẾP", "at": 19}, {"text": "→ NHÀ MÁY", "at": [19, "nhà"], "acc": True}]},
    {"type": "question", "at": 20, "text": "Nhà máy ấy\nnhìn về đâu?"},
]}

# ---------------- CH07 · Ngôi nhà thứ hai ----------------
CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "NGÔI NHÀ THỨ HAI"}, "bgm": {"mood": "warm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "NGÔI NHÀ\nTHỨ HAI", "sub": "NVIDIA · VIỆT NAM", "vid": "7140937", "illus": VM, "titleAt": [0, "jensen"]},
    {"type": "print", "at": [0, "lần"], "img": "jensen", "side": {"k": "12.2023", "h": "LẦN ĐẦU TỚI VIỆT NAM", "hAt": [0, "lần"],
     "lines": [{"text": "gặp Thủ tướng", "at": [1, "thủ"]}, {"text": "thăm Trung tâm Đổi mới sáng tạo quốc gia", "at": [1, "trung"]},
               {"text": "gặp các công ty công nghệ trong nước", "at": [1, "công"]}]}},
    {"type": "kinetic", "at": 2, "items": [{"text": "“NGÔI NHÀ THỨ HAI”", "at": [2, "ngôi"], "acc": True}, {"text": "báo chí ghi lại · 12.2023", "at": [2, "báo"], "sm": True}]},
    {"type": "date", "at": 3, "day": "CHÍNH PHỦ VIỆT NAM – NVIDIA KÝ THOẢ THUẬN", "date": "05.12.2024"},
    {"type": "ledger", "at": 4, "title": "THOẢ THUẬN", "srcnote": "VIETNAM NEWS · VNECONOMY 06.12.2024",
     "rows": [{"k": "1", "v": "TRUNG TÂM NGHIÊN CỨU & PHÁT TRIỂN AI", "at": [4, "nghiên"]},
              {"k": "2", "v": "TRUNG TÂM DỮ LIỆU AI", "at": [4, "dữ"]},
              {"k": "+", "v": "NVIDIA MUA VINBRAIN · AI Y TẾ", "at": 5}]},
    {"type": "kinetic", "at": 6, "items": [{"text": "MỞ RỘNG TỪ TTDL VIETTEL", "at": [6, "viettel"]}, {"text": "theo báo chí đưa tin", "at": 6, "sm": True}]},
    {"type": "kinetic", "at": 7, "items": [{"text": "BƯỚC ĐẦU", "at": 7, "acc": True}, {"text": "làm được gì · cần thêm thời gian", "at": 8, "sm": True}]},
    {"type": "kinetic", "at": 10, "items": [{"text": "PHÒNG NGỦ", "at": 10}, {"text": "→ CHÍNH PHỦ", "at": [10, "chính"], "acc": True}]},
    {"type": "question", "at": 11, "text": "Nhiều chip\n= có AI?"},
]}

# ---------------- CH08 · Không chỉ là con chip ----------------
CH["ch08"] = {"hud": {"k": "CHƯƠNG 08", "t": "KHÔNG CHỈ LÀ CON CHIP"}, "bgm": {"mood": "calm", "gain": 0.12}, "scenes": [
    {"type": "chapter", "no": "8", "k": "CHƯƠNG TÁM", "title": "KHÔNG CHỈ\nLÀ CON CHIP", "sub": "MỘT TRONG BA THỨ", "vid": "5467579", "illus": VM, "titleAt": [0, "nhìn"]},
    {"type": "ledger", "at": 1, "title": "THIẾU MỘT THỨ THÌ SAO?", "rows": [{"k": "−", "v": "KHÔNG IMAGENET → CHẲNG CÓ GÌ ĐỂ HỌC", "at": 1},
                                                                            {"k": "−", "v": "KHÔNG THUẬT TOÁN → TÍNH NHANH VÔ ÍCH", "at": 2}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "CON ĐƯỜNG DUY NHẤT", "at": 3, "fx": "strike", "strikeAt": [3, "duy"]},
                                          {"text": "CHIP RIÊNG CHO AI", "at": 4, "acc": True}, {"text": "chỉ làm đúng việc nhân ma trận", "at": [4, "nhân"], "sm": True}]},
    {"type": "kinetic", "at": 5, "items": [{"text": "ĐÚNG LÚC", "at": [5, "đúng"], "acc": True}, {"text": "+ CÔNG CỤ MÀI GIŨA NHIỀU NĂM", "at": [5, "công"]}]},
    {"type": "broll", "at": 6, "vid": "1085656", "veil": 0.55, "illus": VM,
     "kin": [{"text": "ĐIỆN · NƯỚC LÀM MÁT", "at": 7, "acc": True}, {"text": "câu hỏi cho nhiều nước, kể cả Việt Nam", "at": [7, "việt"], "sm": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "GIẢI BÀI TOÁN TỐC ĐỘ", "at": 8}, {"text": "MỞ BÀI TOÁN KHÁC", "at": [8, "mở"], "acc": True}]},
    {"type": "slam", "at": 10, "text": "DÙNG SAI MỤC ĐÍCH", "sub": "ĐÔI KHI LÀ BƯỚC NGOẶT"},
    {"type": "kinetic", "at": 11, "items": [{"text": "CARD ĐỒ HOẠ → LÀM TOÁN", "at": 11}, {"text": "CÔNG CỤ THÍ NGHIỆM → DẠY MÁY NHÌN", "at": 12, "acc": True}]},
    {"type": "broll", "at": 13, "vid": "5466792", "veil": 0.5, "illus": VM,
     "kin": [{"text": "HÀNG NGHÌN PHỤ BẾP", "at": [13, "hàng"], "acc": True}, {"text": "đang chờ một núi hành", "at": [13, "chờ"], "sm": True}]},
    {"type": "kinetic", "at": 14, "items": [{"text": "2.073.600 ĐIỂM ẢNH", "at": 14}, {"text": "60.000.000 TRỌNG SỐ", "at": 15, "acc": True}]},
    {"type": "question", "at": 16, "text": "Bạn đang dùng món đồ nào\nsai mục đích?"},
]}

SPEC = {
    "title": "GPU: Con Chip Chơi Game Đã Trở Thành Trái Tim Của AI Như Thế Nào?",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["gpu", "cpu", "card", "nvidia", "alexnet", "cuda", "phòng", "ngủ"],
    "say": SAY, "imgs": IMGS,
    "chapters": [f"ch{i:02d}" for i in range(9)],
    "youtube": {
        "titles": ["GPU: Con Chip Chơi Game Đã Trở Thành Trái Tim Của AI Như Thế Nào?",
                   "Hai Card Chơi Game Trong Phòng Ngủ Đã Khởi Đầu Kỷ Nguyên AI",
                   "Vì Sao AI Cần GPU? Từ Card Đồ Hoạ Chơi Game Đến Siêu Máy Tính"],
        "summary": "Năm 2012, một nghiên cứu sinh ở Toronto huấn luyện mạng nơ-ron trên hai card đồ hoạ chơi game đặt trong phòng ngủ ở nhà bố mẹ — "
                   "và thắng cuộc thi nhận dạng ảnh lớn nhất thế giới với khoảng cách chưa từng có. Vì sao một con chip sinh ra để vẽ game lại "
                   "trở thành thứ quý nhất của ngành trí tuệ nhân tạo? Từ quán Denny's năm 1993, hai triệu điểm ảnh của một khung hình, CUDA, "
                   "AlexNet, cuộc đấu giá 44 triệu đô, tới siêu máy tính DGX-1 và thoả thuận Nvidia – Việt Nam.",
        "more": ["Số lõi GPU và lõi CPU không so ngang được (lõi GPU nhỏ, đơn giản hơn nhiều). Con số \"nhanh hơn X lần\" chỉ đúng trong bài toán "
                 "và cấu hình của nghiên cứu được dẫn. Video không nói về giá cổ phiếu. Lời trích được đọc bằng giọng máy của kênh."],
        "ch00_title": "Hai chiếc card trong phòng ngủ",
        "chapter_titles": {"ch00": "Mở đầu: hai card chơi game trong phòng ngủ (2012)", "ch01": "Quán Denny's và GeForce 256",
                           "ch02": "Hai triệu điểm ảnh: CPU và GPU", "ch03": "Giả làm bức tranh: GPGPU và CUDA",
                           "ch04": "Một núi phép nhân: mạng nơ-ron", "ch05": "Lời giải: ImageNet + AlexNet",
                           "ch06": "Từ phòng ngủ đến siêu máy tính", "ch07": "Nvidia và Việt Nam", "ch08": "Không chỉ là con chip"},
        "sources": [
            "https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf",
            "https://spectrum.ieee.org/alexnet-source-code",
            "https://diglib.eg.org/handle/10.2312/CGF.v26i1pp080-113",
            "https://mlanthology.org/icml/2009/raina2009icml-large/",
            "https://www.hpcwire.com/35-hpc-legends-ian-buck",
            "https://fortune.com/2016/08/15/elon-musk-artificial-intelligence-openai-nvidia-supercomputer",
            "https://www.bloomberg.com/news/articles/2023-12-11/nvidia-sees-vietnam-as-potential-second-home-reports-say",
            "https://vietnamnews.vn/economy/1688473/nvidia-to-build-ai-research-and-data-centres-in-vn.html",
        ],
        "hashtags": ["GPU", "AI", "Nvidia", "AlexNet", "MindInTheMachine"],
        "tags": ["GPU là gì", "vì sao AI cần GPU", "card đồ hoạ", "Nvidia", "AlexNet", "CUDA", "học sâu", "deep learning",
                 "mạng nơ-ron", "Geoffrey Hinton", "ImageNet", "Jensen Huang", "trí tuệ nhân tạo", "AI"],
        "category": "28", "thumb": "t1.jpg",
        "video_credits": ["Pexels (pexels.com) — giấy phép Pexels, dùng tự do"],
    },
}


# Nhạc chốt tay (PM 09/10): 5 bài, Jaccard tối đa 0,27 với 5 video MIM trước (ngưỡng variety 0,35; tự chọn theo mood ra 64% với mim-ai-jobs)
BGM_PICKS = {"ch00.0": "ether_vox.mp3", "ch01.0": "chill_wave.mp3", "ch02.0": "bit_shift.mp3", "ch03.0": "ether_vox.mp3",
             "ch04.0": "chill_wave.mp3", "ch05.0": "clean_soul.mp3", "ch06.0": "floating_cities.mp3", "ch07.0": "clean_soul.mp3",
             "ch08.0": "chill_wave.mp3"}
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
