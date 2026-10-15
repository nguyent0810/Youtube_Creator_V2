"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho video dài MIM "AI nhận ra khuôn mặt bạn thế nào" (chuỗi AI Giải Thích Dễ Hiểu, loại 9-12 phút).

    python data/long/mim-ai-khuon-mat/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản + nguồn: script.md (mục Ghi chú). Lộ trình "theo chân một tấm ảnh qua bốn trạm": mỗi trạm một cảnh units 4 ô sáng dần.
Clip: Pexels (ngang), gắn "VIDEO MINH HỌA". Không logo ngân hàng/ứng dụng. Gender Shades = PHÂN LOẠI GIỚI TÍNH (ghi rõ trên hình).
Luật 15/10: "≈" thay "~" trước số; counter có prefix đứng yên; không counter năm.
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
SAY = {"=AI": "ây ai", "=NIST": "Ni-xtơ", "nist": "Ni-xtơ", "facenet": "Phết-nét", "=FaceNet": "Phết-nét", "google": "Gu-gồ", "apple": "Áp-pồ", "face": "Phết",
       "=ID": "ai đi", "joy": "Gioi", "buolamwini": "Bu-ô-lam-uy-ni", "timnit": "Tim-nít", "gebru": "Ghê-bru", "gender": "Gien-đơ", "shades": "Sết",
       "robert": "Rô-bớt", "williams": "Uy-li-ơm", "detroit": "Đi-troi"}
VM = "VIDEO MINH HỌA"
SCAN, SCAN2, CROWD, CCTV, POLICE, DIGI, GLITCH, NUM, SCAN3 = ("8090199", "8090198", "4122942", "38779095", "32538553", "854323", "30036967", "12920674", "8090193")


def station(at, k, at_lit):
    return {"type": "units", "at": at, "title": f"TRẠM {k}/4 · HÀNH TRÌNH CỦA MỘT TẤM ẢNH", "total": 4, "cols": 4, "lit": k, "litAt": at_lit, "unitLabel": "TRẠM"}


CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "KHUÔN MẶT MƯỜI TRIỆU ĐỒNG"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": SCAN3, "veil": 0.55, "illus": VM,
     "kin": [{"text": "LỆNH CHUYỂN 12 TRIỆU", "at": [0, "Bạn"], "sm": True}, {"text": "MỘT KHUNG BẦU DỤC", "at": [1, "màn"], "acc": True},
             {"text": "đưa khuôn mặt vào đây", "at": 2, "sm": True}]},
    {"type": "source", "at": 3, "source": "QUYẾT ĐỊNH 2345/QĐ-NHNN · HIỆU LỰC 01/07/2024", "ref": "CHUYỂN TIỀN TRỰC TUYẾN",
     "snippet": "trên [[10 triệu đồng một lần]] phải xác thực bằng sinh trắc học", "hlAt": [4, "mười"], "seal": "THEO BÁO CHÍ", "sealAt": 5},
    {"type": "broll", "at": 6, "vid": CROWD, "veil": 0.55, "illus": VM,
     "kin": [{"text": "VÔ SỐ KHUÔN MẶT MỖI NGÀY", "at": 6, "sm": True}, {"text": "CỖ MÁY THẬT RA NHÌN GÌ?", "at": 7, "acc": True}]},
    {"type": "myth", "at": 8, "mythLab": "KHÔNG NHÌN NHƯ", "myth": "MẸ BẠN NHÌN BẠN", "truthLab": "VỚI CỖ MÁY", "truth": "MỘT DÃY CON SỐ", "strikeAt": [9, "Nó"], "truthAt": [10, "một"]},
    {"type": "timeline", "at": 11, "items": [{"year": "TRẠM 1", "text": "tìm khuôn mặt", "at": [11, None, 0, 0.05]}, {"year": "TRẠM 2", "text": "căn cho thẳng", "at": [11, "từ"]},
                                            {"year": "TRẠM 3", "text": "biến thành con số", "at": 12}, {"year": "TRẠM 4", "text": "đo khoảng cách", "at": [12, "bốn"]}]},
    {"type": "kinetic", "at": 13, "items": [{"text": "RẤT GIỎI", "at": [13, "giỏi"], "acc": True}, {"text": "mà vẫn có lúc nhầm người", "at": [13, "mà"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "TRẠM 1", "t": "TÌM KHUÔN MẶT"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "TRẠM MỘT", "title": "TÌM KHUÔN MẶT", "sub": "NGHE THÌ HIỂN NHIÊN", "vid": SCAN, "illus": VM, "titleAt": [0, "Trạm"]},
    station(1, 1, [1, "Nhưng"]),
    {"type": "ledger", "at": 2, "title": "MỘT TẤM ẢNH, VỚI MÁY", "rows": [{"k": "LÀ", "v": "LƯỚI HÀNG TRIỆU Ô VUÔNG", "at": 2}, {"k": "MỖI Ô", "v": "MỘT CON SỐ · SÁNG, TỐI, MÀU", "at": 3}],
     "total": {"k": "Ô NÀO GHI “MẮT”?", "v": "KHÔNG CÓ", "at": 4}},
    {"type": "ledger", "at": 5, "title": "CÁCH LÀM ĐỜI ĐẦU · MẪU SÁNG TỐI", "rows": [{"k": "VÙNG MẮT", "v": "TỐI HƠN VÙNG MÁ", "at": [6, "Vùng"]}, {"k": "SỐNG MŨI", "v": "SÁNG HƠN HAI BÊN", "at": [6, "Sống"]}],
     "total": {"k": "NĂM 2000", "v": "CHẠY TRÊN MÁY ẢNH", "at": 7}},
    {"type": "broll", "at": 8, "vid": SCAN2, "veil": 0.5, "illus": VM,
     "kin": [{"text": "Ô VUÔNG NHẢY QUANH MẶT NGƯỜI", "at": 8, "sm": True}, {"text": "NAY: MẠNG NƠ-RON · NHANH HƠN, CHÍNH XÁC HƠN", "at": 9, "acc": True}]},
    {"type": "slam", "at": 10, "text": "MỘT CÁI KHUNG", "sub": "“HÃY NHÌN VÀO ĐÂY”", "subAt": 11},
]}

CH["ch02"] = {"hud": {"k": "TRẠM 2", "t": "CĂN CHO THẲNG"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "TRẠM HAI", "title": "CĂN CHO THẲNG", "sub": "NHƯ NGƯỜI THỢ ẢNH CHỈNH HÌNH", "vid": SCAN3, "ms": 10, "illus": VM, "titleAt": [0, "Bạn"]},
    station(1, 2, [1, "Hôm"]),
    {"type": "ledger", "at": 2, "title": "ĐIỂM MỐC TRÊN KHUÔN MẶT", "rows": [{"k": "HAI KHOÉ MẮT", "v": "·  ·", "at": [3, "hai"]}, {"k": "ĐẦU MŨI", "v": "·", "at": [3, "đầu"]},
                                                                       {"k": "HAI KHOÉ MIỆNG", "v": "·  ·", "at": [3, "khoé", 1]}], "total": {"k": "RỒI", "v": "XOAY · PHÓNG · THU VỀ CHUẨN", "at": 4}},
    {"type": "source", "at": 6, "source": "FACENET · GOOGLE · CVPR 2015", "ref": "TRÊN BỘ ẢNH THỬ NGHIỆM LFW",
     "snippet": "chỉ cắt giữa ảnh: 98,87% · thêm bước căn thẳng: [[99,63%]]", "hlAt": [8, "chín"], "seal": "MỘT BỘ ẢNH THỬ · KHÔNG PHẢI NGOÀI ĐỜI", "sealAt": 9},
    {"type": "bars", "at": 9, "title": "TỈ LỆ SAI TRÊN BỘ ẢNH THỬ (%)", "unit": "KÊNH TỰ TÍNH TỪ BÀI BÁO FACENET 2015",
     "items": [{"k": "CHỈ CẮT GIỮA", "v": 1.13, "lbl": "1,13", "at": [10, "tính"]}, {"k": "CÓ CĂN THẲNG", "v": 0.37, "lbl": "0,37", "at": [10, "giảm"], "acc": True}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "SAI ÍT HƠN HƠN BA LẦN", "at": 11, "acc": True}, {"text": "với hàng triệu người, chừng ấy là rất nhiều", "at": [11, "hàng"], "sm": True}]},
]}

CH["ch03"] = {"hud": {"k": "TRẠM 3", "t": "128 CON SỐ"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "TRẠM BA", "title": "MỘT TRĂM HAI MƯƠI\nTÁM CON SỐ", "sub": "TRẠM QUAN TRỌNG NHẤT", "vid": DIGI, "illus": VM, "titleAt": [0, "Đây"]},
    station(1, 3, [1, "giờ"]),
    {"type": "myth", "at": 2, "mythLab": "ĐẦU RA KHÔNG PHẢI", "myth": "MỘT CÁI TÊN", "truthLab": "MÀ LÀ", "truth": "128 CON SỐ", "strikeAt": [3, "Mà"], "truthAt": [3, "một"]},
    {"type": "broll", "at": 4, "vid": NUM, "veil": 0.6, "illus": VM,
     "kin": [{"text": "MỖI KHUÔN MẶT = MỘT ĐIỂM", "at": 4, "acc": True}, {"text": "trong không gian 128 chiều", "at": [4, "trong"], "sm": True},
             {"text": "không ai vẽ được · ý tưởng thì đơn giản", "at": 5, "sm": True}]},
    {"type": "ledger", "at": 6, "title": "LUẬT CỦA KHÔNG GIAN ẤY", "rows": [{"k": "CÙNG MỘT NGƯỜI", "v": "HAI ĐIỂM GẦN NHAU", "at": 6}, {"k": "HAI NGƯỜI KHÁC", "v": "HAI ĐIỂM XA NHAU", "at": 7}]},
    {"type": "timeline", "at": 8, "items": [{"year": "ẢNH GỐC", "text": "một khuôn mặt", "at": [8, None, 0, 0.3]}, {"year": "CÙNG NGƯỜI", "text": "kéo lại gần", "at": [9, "một", 1]},
                                           {"year": "NGƯỜI KHÁC", "text": "đẩy ra xa", "at": [9, "và"]}]},
    {"type": "kinetic", "at": 11, "items": [{"text": "LẶP LẠI VỚI HÀNG TRIỆU KHUÔN MẶT", "at": 11, "sm": True}, {"text": "KHÔNG AI DẠY · MẠNG TỰ CHỌN THƯỚC ĐO", "at": [11, "mạng"], "acc": True},
                                           {"text": "mắt · gò má · đường viền hàm?", "at": 12, "sm": True}]},
    {"type": "slam", "at": 13, "text": "KHÔNG AI BIẾT CHÍNH XÁC", "sub": "TỪNG CON SỐ TRONG 128 CON SỐ ĐO CÁI GÌ", "subAt": 13},
    {"type": "kinetic", "at": 14, "items": [{"text": "CÂU TRẢ LỜI Ở ĐẦU VIDEO", "at": 14, "sm": True}, {"text": "CỖ MÁY KHÔNG NHÌN THẤY BẠN", "at": 15, "sm": True}, {"text": "MÁY CHỈ THẤY MỘT ĐIỂM · 128 CON SỐ", "at": [15, "Nó"], "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "TRẠM 4", "t": "ĐO KHOẢNG CÁCH"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "TRẠM BỐN", "title": "ĐO KHOẢNG CÁCH", "sub": "LÚC RA QUYẾT ĐỊNH", "vid": SCAN2, "ms": 14, "illus": VM, "titleAt": [0, "Trạm"]},
    station(1, 4, [1, "Khi"]),
    {"type": "ledger", "at": 2, "title": "MỘT PHÉP TÍNH", "rows": [{"k": "LÚC ĐĂNG KÝ", "v": "DÃY SỐ A · CẤT ĐI", "at": [2, None, 0, 0.05]}, {"k": "HÔM NAY", "v": "DÃY SỐ B", "at": 2}],
     "total": {"k": "A–B < NGƯỠNG", "v": "CÙNG MỘT NGƯỜI", "at": 4}},
    {"type": "myth", "at": 5, "mythLab": "NGƯỠNG KHÔNG PHẢI", "myth": "SỰ THẬT TỰ NHIÊN", "truthLab": "MÀ LÀ", "truth": "MỘT LỰA CHỌN", "strikeAt": [5, "chứ"], "truthAt": [5, "một"]},
    {"type": "ledger", "at": 6, "title": "CHỌN NGƯỠNG", "rows": [{"k": "CHẶT", "v": "KHÓ LỌT · CÓ KHI TỪ CHỐI CHỦ", "at": 6},
                                                             {"k": "LỎNG", "v": "CHỦ DỄ QUA · LẠ DỄ LỌT", "at": 7}]},
    {"type": "bars", "at": 9, "title": "XÁC SUẤT NGƯỜI LẠ MỞ ĐƯỢC MÁY", "unit": "APPLE · FACE ID SECURITY GUIDE · 11/2017",
     "items": [{"k": "VÂN TAY", "v": 20, "lbl": "1 / 50.000", "at": [10, "vân"]}, {"k": "KHUÔN MẶT", "v": 1, "lbl": "1 / 1.000.000", "at": [9, "một"], "acc": True}]},
    {"type": "ledger", "at": 11, "title": "XÁC SUẤT CAO HƠN VỚI", "srcnote": "CÙNG TÀI LIỆU · HÃNG KHUYÊN DÙNG MẬT MÃ",
     "rows": [{"k": "1", "v": "SINH ĐÔI", "at": [12, "sinh"]}, {"k": "2", "v": "ANH CHỊ EM RUỘT TRÔNG GIỐNG", "at": [12, "ruột"]}, {"k": "3", "v": "TRẺ DƯỚI 13 TUỔI", "at": [12, "trẻ"]}]},
]}

CH["ch05"] = {"hud": {"k": "CHƯƠNG 05", "t": "HAI MƯƠI LẦN GIỎI HƠN"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "CHƯƠNG NĂM", "title": "HAI MƯƠI LẦN\nGIỎI HƠN", "sub": "BỐN NĂM CỦA MẠNG NƠ-RON SÂU", "vid": CCTV, "illus": VM, "titleAt": [0, "Cách"]},
    {"type": "kinetic", "at": 1, "items": [{"text": "TRƯỚC ĐÂY: ĐẶC ĐIỂM DO NGƯỜI CHỌN SẴN", "at": 1, "sm": True}, {"text": "VÀ SAI KHÁ NHIỀU", "at": 2, "acc": True}]},
    {"type": "source", "at": 3, "source": "NIST · NISTIR 8238 · 11/2018", "ref": "127 THUẬT TOÁN · 39 NHÀ PHÁT TRIỂN",
     "snippet": "tìm một người trong kho ảnh lớn: tỉ lệ thất bại [[≈ 4% (2014) → 0,2% (2018)]]", "hlAt": [5, None, 0, 0.05], "seal": "THỬ NGHIỆM ĐỘC LẬP", "sealAt": [5, "kho"]},
    {"type": "bars", "at": 6, "title": "TỈ LỆ THẤT BẠI KHI TÌM (%)", "unit": "NIST FRVT · THUẬT TOÁN TỐT NHẤT",
     "items": [{"k": "2014", "v": 4, "lbl": "≈ 4", "at": [6, "bốn"]}, {"k": "2018", "v": 0.2, "lbl": "0,2", "at": [7, "không"], "acc": True}]},
    {"type": "counter", "at": 8, "from": 20, "to": 20, "prefix": "≈ ", "suffix": " LẦN", "label": "GIỎI HƠN TRONG BỐN NĂM", "sub": {"text": "NHỜ MẠNG NƠ-RON TÍCH CHẬP SÂU · NIST", "at": 9}},
    {"type": "ledger", "at": 10, "title": "NIST CŨNG LƯU Ý", "rows": [{"k": "KẾT QUẢ TỐT NHẤT", "v": "VỚI ẢNH CHẤT LƯỢNG TỐT", "at": [10, "kết"]},
                                                                 {"k": "GIỮA CÁC HÃNG", "v": "CHÊNH NHAU RẤT XA", "at": [10, "giữa"]}]},
    {"type": "slam", "at": 11, "text": "ẢNH CHẤT LƯỢNG TỐT", "sub": "NGOÀI ĐỜI KHÔNG PHẢI ẢNH NÀO CŨNG VẬY", "subAt": 12},
]}

CH["ch06"] = {"hud": {"k": "CHƯƠNG 06", "t": "KHI CỖ MÁY NHÌN NHẦM"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "CHƯƠNG SÁU", "title": "KHI CỖ MÁY\nNHÌN NHẦM", "sub": "ĐỘ CHÍNH XÁC PHỤ THUỘC VÀO BẠN LÀ AI", "vid": GLITCH, "illus": VM, "titleAt": [0, "Năm"]},
    {"type": "ledger", "at": 1, "title": "GENDER SHADES · BUOLAMWINI & GEBRU · 2018", "srcnote": "BA HỆ THỐNG THƯƠNG MẠI · ĐOÁN GIỚI TÍNH TỪ KHUÔN MẶT",
     "rows": [{"k": "VIỆC CẦN LÀM", "v": "ĐOÁN NAM HAY NỮ", "at": [1, "đoán"]}]},
    {"type": "bars", "at": 2, "title": "SAI TỆ NHẤT · BA HỆ THỐNG (%)", "unit": "GENDER SHADES 2018 · ĐOÁN GIỚI TÍNH",
     "items": [{"k": "NAM DA SÁNG", "v": 0.8, "lbl": "0,8", "at": [2, "không"]}, {"k": "NỮ DA SẪM MÀU", "v": 34.7, "lbl": "34,7", "at": [3, "ba"], "acc": True}]},
    {"type": "kinetic", "at": 4, "items": [{"text": "CÙNG MỘT CỖ MÁY", "at": 4, "sm": True}, {"text": "CHÍNH XÁC TUỲ VÀO BẠN LÀ AI", "at": [4, "độ"], "acc": True},
                                          {"text": "một lý do hay được nhắc: dữ liệu huấn luyện", "at": 5, "sm": True}]},
    {"type": "broll", "at": 6, "vid": POLICE, "veil": 0.55, "illus": VM,
     "kin": [{"text": "DETROIT · 01/2020", "at": 7, "acc": True}, {"text": "ROBERT WILLIAMS BỊ BẮT TRƯỚC NHÀ", "at": [7, "Robert"], "sm": True},
             {"text": "ảnh bằng lái cũ ↔ video camera mờ nhoè", "at": 8, "sm": True}]},
    {"type": "counter", "at": 9, "from": 30, "to": 30, "prefix": "≈ ", "suffix": " GIỜ", "label": "BỊ GIỮ · ANH KHÔNG PHẢI NGƯỜI TRONG VIDEO", "sub": {"text": "THEO BÁO CHÍ MỸ", "at": 10}},
    {"type": "source", "at": 11, "source": "THOẢ THUẬN · 06/2024", "ref": "CẢNH SÁT DETROIT",
     "snippet": "không được bắt người [[chỉ dựa trên kết quả nhận diện khuôn mặt]]", "hlAt": [11, "chỉ"], "seal": "VỤ KIỆN CỦA ROBERT WILLIAMS", "sealAt": [11, "nhận"]},
    {"type": "myth", "at": 12, "mythLab": "CỖ MÁY KHÔNG SAI VÌ", "myth": "NÓ XẤU", "truthLab": "MÀ VÌ NGƯỜI TA", "truth": "TIN CON SỐ QUÁ MỨC", "strikeAt": [12, "xấu"], "truthAt": [13, "tin"]},
]}

CH["ch07"] = {"hud": {"k": "CHƯƠNG 07", "t": "KHUÔN MẶT Ở QUẦY GIAO DỊCH"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "7", "k": "CHƯƠNG BẢY", "title": "KHUÔN MẶT\nỞ QUẦY GIAO DỊCH", "sub": "QUAY LẠI LỆNH CHUYỂN 12 TRIỆU", "vid": SCAN, "ms": 12, "illus": VM, "titleAt": [0, "Quay"]},
    {"type": "ledger", "at": 1, "title": "PHẢI XÁC THỰC SINH TRẮC HỌC KHI", "srcnote": "QĐ 2345/QĐ-NHNN · TỪ 01/07/2024 · THEO BÁO CHÍ",
     "rows": [{"k": "MỘT LẦN CHUYỂN", "v": "TRÊN 10 TRIỆU", "at": [1, "mười"]}, {"k": "TỔNG TRONG NGÀY", "v": "TRÊN 20 TRIỆU", "at": 2}]},
    {"type": "ledger", "at": 3, "title": "DỮ LIỆU ĐỂ SO", "rows": [{"k": "1", "v": "CHIP CĂN CƯỚC CÔNG DÂN", "at": [3, "con"]}, {"k": "2", "v": "TÀI KHOẢN ĐỊNH DANH ĐIỆN TỬ", "at": [3, "tài"]},
                                                              {"k": "3", "v": "DỮ LIỆU NGÂN HÀNG ĐÃ THU", "at": [3, "dữ", 1]}], "total": {"k": "MỤC TIÊU", "v": "CHẶN TÀI KHOẢN “MƯỢN”", "at": 4}},
    {"type": "question", "at": 5, "text": "Vì sao phải quay đầu,\nhay chớp mắt?"},
    {"type": "myth", "at": 7, "mythLab": "BỐN TRẠM HỎI", "myth": "CÓ PHẢI NGƯỜI NÀY?", "truthLab": "BƯỚC KIỂM TRA HỎI", "truth": "CÓ PHẢI NGƯỜI THẬT?", "strikeAt": [8, "Bước"], "truthAt": [8, "có"]},
    {"type": "ledger", "at": 9, "title": "MỌI THỨ ĐỀU CÓ MẶT", "rows": [{"k": "1", "v": "MỘT NGƯỠNG · AN TOÀN ↔ TIỆN LỢI", "at": 10}, {"k": "2", "v": "RẤT CHÍNH XÁC · VỚI ẢNH TỐT", "at": 11},
                                                                    {"k": "3", "v": "MỘT DÃY SỐ CỦA BẠN · CẤT Ở ĐÂU ĐÓ", "at": 12}]},
]}

CH["ch08"] = {"hud": {"k": "PHẦN CUỐI", "t": "128 CON SỐ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "8", "k": "PHẦN CUỐI", "title": "MỘT TRĂM HAI MƯƠI\nTÁM CON SỐ", "sub": "NHÌN LẠI HÀNH TRÌNH", "vid": DIGI, "ms": 14, "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "timeline", "at": 1, "items": [{"year": "TRẠM 1", "text": "tìm khuôn mặt", "at": [1, "Trạm"]}, {"year": "TRẠM 2", "text": "căn cho thẳng", "at": [1, "Trạm", 1]},
                                           {"year": "TRẠM 3", "text": "128 con số", "at": [2, "Trạm"]}, {"year": "TRẠM 4", "text": "đo khoảng cách", "at": [2, "Trạm", 1]}]},
    {"type": "kinetic", "at": 3, "items": [{"text": "4 TRẠM · 0 TRẠM HIỂU BẠN", "at": 3, "acc": True}, {"text": "chỉ biết hai dãy số gần nhau tới đâu", "at": 5, "sm": True}]},
    {"type": "ledger", "at": 6, "title": "VỪA LÀ", "rows": [{"k": "SỨC MẠNH", "v": "NHANH · CHÍNH XÁC HƠN NGƯỜI", "at": 7},
                                                          {"k": "GIỚI HẠN", "v": "SAI MÀ VẪN RẤT TỰ TIN", "at": 8}]},
    {"type": "broll", "at": 9, "vid": SCAN3, "ms": 20, "veil": 0.55, "illus": VM,
     "kin": [{"text": "NÓ KHÔNG NHÌN BẠN", "at": 10, "sm": True}, {"text": "NÓ ĐANG ĐO MỘT KHOẢNG CÁCH", "at": [10, "Nó", 1], "acc": True},
             {"text": "một con người đã chọn: gần tới mức nào thì đủ", "at": 11, "sm": True}]},
    {"type": "question", "at": 12, "text": "Yên tâm hơn, hay lo hơn,\nkhi khuôn mặt chỉ là một dãy số?"},
    {"type": "kinetic", "at": 13, "items": [{"text": "YÊN TÂM · HAY LO?", "at": 13}, {"text": "VIẾT XUỐNG BÌNH LUẬN", "at": [13, "ở"], "acc": True}]},
]}

SPEC = {
    "title": "Khuôn Mặt Bạn Biến Thành 128 Con Số: AI Nhận Ra Bạn Thế Nào?",
    "channel": "MIM", "theme": "lab", "accent": "#22d3ee", "master": True, "endcard": 20, "autoTr": True, "beat2": True,
    "acc": ["khuôn", "mặt", "số", "trạm", "ngưỡng", "nhầm", "máy"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(9)],
    "youtube": {
        "titles": ["Khuôn Mặt Bạn Biến Thành 128 Con Số: AI Nhận Ra Bạn Thế Nào?",
                   "Chuyển Khoản Trên 10 Triệu Phải Quét Mặt: Cỗ Máy Đang Nhìn Gì Trên Khuôn Mặt Bạn?",
                   "Nhận Diện Khuôn Mặt: Giỏi Gấp 20 Lần Trong 4 Năm, Nhưng Vẫn Bắt Nhầm Người"],
        "summary": "Từ 01/07/2024, chuyển khoản trực tuyến trên 10 triệu đồng phải xác thực sinh trắc học, và nhiều người chọn khuôn mặt. Video theo chân "
                   "một tấm ảnh qua bốn trạm của hệ thống nhận diện khuôn mặt: tìm khuôn mặt, căn cho thẳng, biến thành 128 con số (FaceNet, 2015), đo "
                   "khoảng cách so với một ngưỡng. Kèm kết quả thử nghiệm NIST (giỏi hơn khoảng 20 lần từ 2014 tới 2018), nghiên cứu Gender Shades, vụ bắt "
                   "nhầm Robert Williams ở Detroit, và vì sao ứng dụng ngân hàng bắt bạn quay đầu, chớp mắt.",
        "more": ["Gender Shades (2018) đo hệ thống phân loại giới tính từ khuôn mặt, không phải nhận dạng danh tính; 34,7% và 0,8% là mức sai tệ nhất trong "
                 "ba hệ thống. Con số 1/1.000.000 của Face ID theo tài liệu bảo mật Apple 11/2017, cho một khuôn mặt đã đăng ký. Quy định ngân hàng theo "
                 "Quyết định 2345/QĐ-NHNN qua báo chí. Video làm nền là minh hoạ, không phải hình ảnh của hệ thống nào."],
        "chapter_titles": {"ch00": "Mở đầu: khuôn mặt mười triệu đồng", "ch01": "Trạm 1: tìm khuôn mặt", "ch02": "Trạm 2: căn cho thẳng",
                           "ch03": "Trạm 3: 128 con số", "ch04": "Trạm 4: đo khoảng cách và ngưỡng", "ch05": "Hai mươi lần giỏi hơn (NIST)",
                           "ch06": "Khi cỗ máy nhìn nhầm", "ch07": "Khuôn mặt ở quầy giao dịch", "ch08": "128 con số"},
        "sources": ["https://arxiv.org/abs/1503.03832", "https://apple.com/business-docs/FaceID_Security_Guide.pdf",
                    "https://www.nist.gov/node/1532616", "https://proceedings.mlr.press/v81/buolamwini18a.html",
                    "https://www.michiganpublic.org/criminal-justice-legal-system/2024-06-28/it-didnt-make-sense-at-all-wrongful-facial-recognition-arrest-leads-to-landmark-settlement",
                    "https://luatvietnam.vn/tin-van-ban-moi/tu-2024-chuyen-khoan-tren-10-trieu-dong-phai-xac-thuc-sinh-trac-hoc-186-96491-article.html"],
        "hashtags": ["NhậnDiệnKhuônMặt", "SinhTrắcHọc", "TríTuệNhânTạo", "AIGiảiThích", "MindInTheMachine"],
        "tags": ["nhận diện khuôn mặt", "ai nhận diện khuôn mặt hoạt động thế nào", "sinh trắc học chuyển khoản", "xác thực khuôn mặt ngân hàng",
                 "facenet", "face id", "gender shades", "trí tuệ nhân tạo", "mạng nơ-ron"],
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
