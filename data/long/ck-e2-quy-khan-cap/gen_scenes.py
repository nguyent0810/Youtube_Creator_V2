"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK E2 "Quỹ khẩn cấp".

    python data/long/ck-e2-quy-khan-cap/gen_scenes.py     # giữ nguyên "lines" + "title" (do motion/long/script_lines.py ghi)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (VÍ DỤ GIẢ ĐỊNH: An, lương 12 triệu, thiết yếu 8 triệu, để dành 1,5 triệu/tháng).
Luật kênh: chỉ giáo dục; không chỉ định sản phẩm, không tên ngân hàng; An là nhân vật giả định; mọi cảnh số của ví dụ ghi "VÍ DỤ GIẢ ĐỊNH".
Áp luật studio (14/10/2026): cảnh myth / source / units; lộ trình "tờ phiếu ba ô trống".
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
assert R["months"]["three_months"] == 16 and R["months"]["bill15"] == 10 and R["card15"]["months"] == 104
GOLD, UP = "#fbbf24", "#22c55e"
HYPO = "VÍ DỤ GIẢ ĐỊNH · AN LÀ NHÂN VẬT GIẢ ĐỊNH"
H2 = "VÍ DỤ GIẢ ĐỊNH · THIẾT YẾU 8 TRIỆU, ĐỂ DÀNH 1,5 TRIỆU MỖI THÁNG"
VM = "VIDEO MINH HỌA"
MONTHS = [f"thang__{m:02d}" for m in range(0, 17)]
CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "MỘT HOÁ ĐƠN 15 TRIỆU"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "3192916", "veil": 0.55, "illus": VM + " · NHÂN VẬT GIẢ ĐỊNH",
     "kin": [{"text": "AN · 28 TUỔI · LƯƠNG 12 TRIỆU", "at": [0, "An"], "sm": True}, {"text": "MỘT TỜ HOÁ ĐƠN 15 TRIỆU", "at": [2, "một"], "acc": True}]},
    {"type": "ledger", "at": 3, "title": "HAI PHIÊN BẢN CỦA AN", "srcnote": HYPO, "rows": [{"k": "PHIÊN BẢN 1", "v": "CÓ SẴN MỘT KHOẢN ĐỂ RIÊNG", "at": 5}, {"k": "PHIÊN BẢN 2", "v": "KHÔNG CÓ · QUẸT THẺ, TRẢ TỐI THIỂU", "at": 7}],
     "total": {"k": "CÙNG LƯƠNG · CÙNG HOÁ ĐƠN", "v": "HAI CON ĐƯỜNG", "at": 9}},
    {"type": "kinetic", "at": 10, "items": [{"text": "KHOẢN TIỀN TẠO RA KHÁC BIỆT", "at": 10, "sm": True}, {"text": "QUỸ KHẨN CẤP", "at": [11, "Quỹ"], "acc": True}]},
    {"type": "question", "at": 12, "text": "Cần bao nhiêu thì đủ?\nLương 12 triệu thì lấy đâu ra?"},
    {"type": "ledger", "at": 13, "title": "TỜ PHIẾU BA Ô TRỐNG", "rows": [{"k": "Ô 1", "v": "MỘT THÁNG THIẾT YẾU = ?", "at": 15}, {"k": "Ô 2", "v": "CẦN MẤY THÁNG = ?", "at": 16}, {"k": "Ô 3", "v": "MỖI THÁNG ĐỂ DÀNH = ?", "at": 17}],
     "total": {"k": "ĐIỀN XONG", "v": "CẦN BAO NHIÊU · MẤT BAO LÂU", "at": 18}},
    {"type": "brand", "at": 19, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
]}

CH["ch01"] = {"hud": {"k": "Ô 01", "t": "MỘT THÁNG THIẾT YẾU"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "Ô THỨ NHẤT", "title": "MỘT THÁNG\nTHIẾT YẾU", "sub": "Ô HAY BỊ ĐIỀN SAI NHẤT", "vid": "7490451", "illus": VM, "titleAt": [0, "Ô"]},
    {"type": "myth", "at": 1, "mythLab": "NHIỀU NGƯỜI ĐIỀN", "myth": "MỨC LƯƠNG", "truthLab": "CON SỐ CẦN ĐIỀN", "truth": "CHI TIÊU THIẾT YẾU", "strikeAt": [2, "Nhưng"], "truthAt": [4, "chi"]},
    {"type": "ledger", "at": 5, "title": "THIẾT YẾU GỒM", "rows": [{"k": "✓", "v": "TIỀN NHÀ · TIỀN ĂN", "at": [5, "Tiền"]}, {"k": "✓", "v": "ĐIỆN NƯỚC · ĐI LẠI · NỢ HẰNG THÁNG", "at": [5, "Điện"]}],
     "total": {"k": "KHÔNG TÍNH", "v": "CÀ PHÊ · QUẦN ÁO MỚI · DU LỊCH", "at": 6}},
    {"type": "bars", "at": 7, "title": "MỘT THÁNG CỦA AN (TRIỆU ĐỒNG)", "unit": HYPO,
     "items": [{"k": "LƯƠNG", "v": 12, "lbl": "12", "at": [7, "lương"]}, {"k": "PHẦN THIẾT YẾU", "v": 8, "lbl": "≈ 8", "at": [7, "nhưng"], "acc": True}]},
    {"type": "slam", "at": 9, "text": "GẦN LẠI MỘT PHẦN BA", "sub": "CHỈ NHỜ ĐIỀN ĐÚNG Ô THỨ NHẤT", "subAt": 9},
    {"type": "source", "at": 10, "source": "CỤC THỐNG KÊ · QUÝ I NĂM 2026", "ref": "THU NHẬP BÌNH QUÂN NGƯỜI LAO ĐỘNG", "snippet": "khoảng [[9 triệu đồng một tháng]]",
     "hlAt": [11, "khoảng"], "seal": "SỐ THẬT", "sealAt": [12, "bạn"]},
    {"type": "ledger", "at": 13, "title": "MẸO ĐIỀN Ô THỨ NHẤT", "rows": [{"k": "1", "v": "XEM SAO KÊ BA THÁNG GẦN NHẤT", "at": 13}, {"k": "2", "v": "ĐÁNH DẤU KHOẢN VẪN PHẢI TRẢ DÙ MẤT VIỆC", "at": 14},
                                                                         {"k": "3", "v": "CỘNG LẠI · CHIA BA", "at": 15}], "total": {"k": "KẾT QUẢ", "v": "THẬT HƠN MỌI ƯỚC ĐOÁN", "at": 16}},
]}

CH["ch02"] = {"hud": {"k": "Ô 02", "t": "MẤY THÁNG?"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "Ô THỨ HAI", "title": "MẤY THÁNG?", "sub": "3 – 6 THÁNG: QUY TẮC, KHÔNG PHẢI ĐỊNH LUẬT", "vid": "6997938", "illus": VM, "titleAt": [0, "ba"]},
    {"type": "units", "at": 1, "title": "QUY TẮC KINH NGHIỆM: 3 TỚI 6 THÁNG CHI TIÊU THIẾT YẾU", "total": 6, "cols": 6, "lit": 3, "litAt": [1, "một"], "unitLabel": "THÁNG · MỨC ĐẦU TIÊN"},
    {"type": "kinetic", "at": 3, "items": [{"text": "BA HAY SÁU?", "at": 3, "acc": True}, {"text": "hãy nghĩ như độ dày của một tấm đệm", "at": 4, "sm": True}]},
    {"type": "ledger", "at": 6, "title": "TẤM ĐỆM DÀY BAO NHIÊU?", "rows": [{"k": "THU NHẬP ĐỀU · HAI NGƯỜI ĐI LÀM", "v": "CÓ THỂ MỎNG HƠN", "at": 7}, {"k": "THU NHẬP THẤT THƯỜNG · MỘT MÌNH NUÔI NHÀ", "v": "CẦN DÀY HƠN", "at": 9}]},
    {"type": "bars", "at": 10, "title": "ĐÍCH CỦA AN (TRIỆU ĐỒNG)", "unit": HYPO + " · THIẾT YẾU 8 TRIỆU/THÁNG",
     "items": [{"k": "3 THÁNG", "v": 24, "lbl": "24", "at": [11, "hai"], "acc": True}, {"k": "6 THÁNG", "v": 48, "lbl": "48", "at": [12, "bốn"]}]},
    {"type": "source", "at": 13, "source": "KHẢO SÁT NGƯỜI TIÊU DÙNG · 2025 · 1.000 NGƯỜI VIỆT", "ref": "CÓ DỰ PHÒNG ĐỦ HƠN 3 THÁNG CHI TIÊU", "snippet": "[[chưa tới một nửa]] · khoảng 5% không có dự phòng hay bảo hiểm nào",
     "hlAt": [16, "Chưa"], "seal": "QUA BÁO CHÍ · 11/2025", "sealAt": [17, "khoảng"]},
    {"type": "question", "at": 18, "text": "Từ số 0, đi tới đó\nbằng cách nào?"},
]}

CH["ch03"] = {"hud": {"k": "Ô 03", "t": "MỖI THÁNG BAO NHIÊU?"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "Ô THỨ BA", "title": "MỖI THÁNG\nBAO NHIÊU?", "sub": "Ô DUY NHẤT BẠN ĐIỀU KHIỂN ĐƯỢC NGAY", "vid": "12033695", "illus": VM, "titleAt": [0, "Ô"]},
    {"type": "ledger", "at": 1, "title": "PHÉP CHIA CỦA AN", "srcnote": HYPO, "rows": [{"k": "ĐÍCH 3 THÁNG", "v": "24 TRIỆU", "at": [2, None, 0, 0.05]}, {"k": "MỖI THÁNG ĐỂ DÀNH", "v": "1,5 TRIỆU", "at": [2, "một"]}],
     "total": {"k": "24 ÷ 1,5", "v": "16 THÁNG", "at": [2, "mười"]}},
    {"type": "race", "at": 3, "abs": True, "unit": "TRIỆU", "xlab": "THÁNG ", "xstep": 4, "dates": MONTHS, "title": "TẤM ĐỆM CỦA AN DÀY DẦN", "range": "TRIỆU ĐỒNG · THEO THÁNG",
     "drawAt": [3, None, 0, 0.1], "until": [8, "tấm"],
     "series": [{"label": "QUỸ · 1,5 TR/THÁNG", "color": UP, "vals": R["path"]}], "source": H2},
    {"type": "timeline", "at": 9, "items": [{"year": "THÁNG 5", "text": "đủ một tháng thiết yếu", "at": [9, None, 0, 0.05]}, {"year": "THÁNG 10", "text": "đủ tờ hoá đơn 15 triệu", "at": 10},
                                           {"year": "THÁNG 16", "text": "xong tấm đệm ba tháng", "at": 11}], "tag": {"text": H2, "at": 9}},
    {"type": "broll", "at": 12, "vid": "6771532", "veil": 0.55, "illus": VM,
     "kin": [{"text": "MỘT MẸO NHỎ", "at": 12, "sm": True}, {"text": "CHUYỂN ĐI NGAY NGÀY NHẬN LƯƠNG", "at": [14, "ngay"], "acc": True}, {"text": "trả cho mình trước", "at": 16, "sm": True}]},
    {"type": "bars", "at": 17, "title": "SỐ THÁNG ĐỂ CÓ 24 TRIỆU", "unit": HYPO,
     "items": [{"k": "ĐỂ DÀNH 1,5 TRIỆU/THÁNG", "v": 16, "lbl": "16", "at": [17, None, 0, 0.05], "acc": True}, {"k": "ĐỂ DÀNH 1 TRIỆU/THÁNG", "v": 24, "lbl": "24", "at": [18, "Hai"]}]},
    {"type": "question", "at": 20, "text": "Không có tấm đệm ấy,\ncái giá là bao nhiêu?"},
]}

CH["ch04"] = {"hud": {"k": "CÁI GIÁ", "t": "KHI KHÔNG CÓ TẤM ĐỆM"}, "bgm": {"mood": "mystery", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "4", "k": "PHIÊN BẢN HAI", "title": "CÁI GIÁ CỦA VIỆC\nKHÔNG CÓ TẤM ĐỆM", "sub": "QUAY LẠI TỜ HOÁ ĐƠN 15 TRIỆU", "vid": "5466772", "illus": VM, "titleAt": [0, "Ở"]},
    {"type": "ledger", "at": 1, "title": "AN Ở PHIÊN BẢN THỨ HAI", "srcnote": "VÍ DỤ GIẢ ĐỊNH · LÃI 30%/NĂM, TỐI THIỂU 5%, KHÔNG TIÊU THÊM · CÁCH TÍNH NHƯ BÀI NỢ THẺ",
     "rows": [{"k": "QUẸT THẺ", "v": "15 TRIỆU", "at": [1, None, 0, 0.05]}, {"k": "MỖI THÁNG", "v": "CHỈ TRẢ MỨC TỐI THIỂU", "at": [1, "chỉ"]}], "total": {"k": "HẾT NỢ SAU", "v": "HƠN 8 NĂM", "at": [3, "hơn"]}},
    {"type": "bars", "at": 4, "title": "TIỀN LÃI PHẢI TRẢ CHO HOÁ ĐƠN 15 TRIỆU (TRIỆU ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH · LÃI THẺ 30%/NĂM",
     "items": [{"k": "PHIÊN BẢN 2 · KHÔNG CÓ QUỸ", "v": 13.2, "lbl": "≈ 13", "at": [4, "khoảng"], "acc": True}, {"k": "PHIÊN BẢN 1 · CÓ QUỸ", "v": 0.1, "lbl": "0", "at": [6, "không."]}]},
    {"type": "myth", "at": 8, "mythLab": "KHÁC BIỆT KHÔNG PHẢI Ở", "myth": "AI KIẾM TIỀN GIỎI HƠN", "truthLab": "MÀ Ở CHỖ", "truth": "TIỀN CÓ TRƯỚC HAY VAY SAU", "strikeAt": [8, "không"], "truthAt": [9, "tiền"]},
    {"type": "kinetic", "at": 10, "items": [{"text": "QUỸ KHẨN CẤP KHÔNG SINH LỜI NHIỀU", "at": 10, "sm": True}, {"text": "NÓ GIÚP BẠN KHỎI TRẢ LÃI CHO NGƯỜI KHÁC", "at": [11, "giúp"], "acc": True}]},
    {"type": "broll", "at": 12, "vid": "7490451", "ms": 6, "veil": 0.55, "illus": VM,
     "kin": [{"text": "HƠN 8 NĂM · THÁNG NÀO CŨNG CÓ MỘT KHOẢN NỢ", "at": 13, "sm": True}, {"text": "TẤM ĐỆM MUA CẢ SỰ YÊN TÂM", "at": [15, "mua"], "acc": True}]},
    {"type": "question", "at": 16, "text": "Khoản tiền này\nnên nằm ở đâu?"},
]}

CH["ch05"] = {"hud": {"k": "ĐỂ Ở ĐÂU", "t": "BA TIÊU CHÍ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "5", "k": "ĐỂ Ở ĐÂU", "title": "BA TIÊU CHÍ", "sub": "KÊNH KHÔNG CHỈ ĐỊNH NƠI NÀO", "vid": "1793337", "illus": VM, "titleAt": [1, "ba"]},
    {"type": "ledger", "at": 2, "title": "THEO THỨ TỰ QUAN TRỌNG", "rows": [{"k": "1 · AN TOÀN", "v": "KHÔNG MẤT GIÁ TRỊ KHI CẦN", "at": 2}, {"k": "2 · RÚT NHANH", "v": "TRONG MỘT, HAI NGÀY", "at": 3},
                                                                          {"k": "3 · CÓ LÃI", "v": "CHỈ SAU HAI ĐIỀU TRÊN", "at": 4}]},
    {"type": "bars", "at": 5, "title": "MỘT TÀI SẢN LÊN XUỐNG MẠNH · ĐÚNG THÁNG BẠN CẦN TIỀN", "unit": "MINH HOẠ · KHÔNG PHẢI SỐ LIỆU CỦA TÀI SẢN NÀO",
     "items": [{"k": "TRƯỚC ĐÓ", "v": 100, "lbl": "100", "at": [5, None, 0, 0.05]}, {"k": "THÁNG BẠN MẤT VIỆC", "v": 67, "lbl": "− 1/3", "at": [6, "giảm"], "acc": True}]},
    {"type": "slam", "at": 7, "text": "PHẢI BÁN LÚC GIÁ THẤP NHẤT", "sub": "VÌ THẾ: AN TOÀN ĐỨNG ĐẦU", "subAt": 7},
    {"type": "ledger", "at": 8, "title": "TIỀN GỬI CÓ KỲ HẠN", "srcnote": "THÔNG THƯỜNG · XEM ĐIỀU KHOẢN CỦA BẠN", "rows": [{"k": "RÚT TRƯỚC HẠN", "v": "CHỈ HƯỞNG LÃI KHÔNG KỲ HẠN", "at": 9}, {"k": "NÊN NHIỀU NGƯỜI", "v": "CHIA QUỸ THÀNH VÀI PHẦN NHỎ", "at": 10}]},
    {"type": "units", "at": 11, "title": "CẦN 10 TRIỆU: CHỈ RÚT MỘT PHẦN · CÁC PHẦN KHÁC GIỮ NGUYÊN LÃI", "total": 4, "cols": 4, "lit": 1, "litAt": [11, "chỉ"], "unitLabel": "PHẦN PHẢI RÚT",
     "label": {"k": "MINH HOẠ CƠ CHẾ · KHÔNG PHẢI LỜI KHUYÊN", "v": "", "at": 11}},
    {"type": "kinetic", "at": 12, "items": [{"text": "AN TOÀN · RÚT NHANH", "at": [13, "an"], "acc": True}, {"text": "rồi mới tới lãi", "at": [13, "rồi"], "sm": True}]},
]}

CH["ch06"] = {"hud": {"k": "GIỚI HẠN", "t": "KHI NÀO KHÔNG ĐÚNG VỚI BẠN"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "KHI NÀO PHÉP TÍNH\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": "7593898", "illus": VM, "titleAt": [0, "Như"]},
    {"type": "ledger", "at": 1, "title": "BA GIỚI HẠN", "rows": [{"k": "1", "v": "ĐANG NỢ LÃI CAO: THỨ TỰ CÓ THỂ KHÁC", "at": 1}, {"k": "2", "v": "3–6 THÁNG KHÔNG HỢP MỌI NGƯỜI", "at": 3},
                                                                {"k": "3", "v": "QUỸ KHÔNG THAY ĐƯỢC BẢO HIỂM", "at": 5}]},
    {"type": "bars", "at": 6, "title": "TẤM ĐỆM ĐỠ ĐƯỢC GÌ? (TRIỆU ĐỒNG)", "unit": "MINH HOẠ",
     "items": [{"k": "HOÁ ĐƠN 15 TRIỆU", "v": 15, "lbl": "ĐỠ ĐƯỢC", "at": [6, None, 0, 0.05]}, {"k": "HOÁ ĐƠN VÀI TRĂM TRIỆU", "v": 300, "lbl": "KHÔNG", "at": [6, "vài"], "acc": True}]},
    {"type": "ledger", "at": 8, "title": "TỜ PHIẾU CỦA BẠN", "rows": [{"k": "Ô 1", "v": "MỘT THÁNG THIẾT YẾU = ?", "at": 9}, {"k": "Ô 2", "v": "CẦN MẤY THÁNG = ?", "at": 10}, {"k": "Ô 3", "v": "THÁNG NÀY ĐỂ VÀO = ?", "at": 11}],
     "total": {"k": "Ô 1 × Ô 2 ÷ Ô 3", "v": "SỐ THÁNG CỦA RIÊNG BẠN", "at": 12}},
    {"type": "broll", "at": 14, "vid": "3192916", "ms": 8, "veil": 0.55, "illus": VM + " · NHÂN VẬT GIẢ ĐỊNH",
     "kin": [{"text": "AN Ở PHIÊN BẢN 1 KHÔNG GIÀU HƠN", "at": 15}, {"text": "CHỈ BẮT ĐẦU SỚM HƠN 16 THÁNG", "at": [16, "chỉ"], "acc": True}]},
    {"type": "question", "at": 17, "text": "Ô thứ nhất của bạn\nlà bao nhiêu?"},
]}

Y4 = C4["youtube"]
SPEC = {
    "title": "Quỹ Khẩn Cấp: Cần Bao Nhiêu, Mất Bao Lâu, Để Ở Đâu? Tờ Phiếu Ba Ô Trống",
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["quỹ", "khẩn", "cấp", "đệm", "thiết", "yếu", "tháng"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": ["Quỹ Khẩn Cấp: Cần Bao Nhiêu, Mất Bao Lâu, Để Ở Đâu? Tờ Phiếu Ba Ô Trống",
                   "Một Hoá Đơn 15 Triệu: Vì Sao Cùng Mức Lương Mà Hai Người Đi Hai Ngả?",
                   "Quỹ Khẩn Cấp 3–6 Tháng: Tính Thế Nào Với Lương 12 Triệu?"],
        "summary": "Một hoá đơn viện phí 15 triệu, hai phiên bản của cùng một người: một bên có quỹ khẩn cấp, một bên phải quẹt thẻ và trả tối thiểu. "
                   "Video đưa bạn một tờ phiếu ba ô trống: một tháng thiết yếu là bao nhiêu, cần mấy tháng, mỗi tháng để dành được bao nhiêu, để tự tính "
                   "cần bao nhiêu và mất bao lâu. Kèm ba tiêu chí chọn nơi để quỹ (an toàn, rút nhanh, rồi mới tới lãi) và khi nào phép tính này không "
                   "đúng với bạn.",
        "more": [Y4["more"][0],
                 "📐 CÁCH KÊNH TÍNH: An là nhân vật GIẢ ĐỊNH: lương 12 triệu, chi thiết yếu 8 triệu/tháng, để dành 1,5 triệu/tháng (không tính lãi): đủ 8 "
                 "triệu sau khoảng 5 tháng, 15 triệu sau 10 tháng, 24 triệu sau 16 tháng. Phiên bản không có quỹ: nợ thẻ 15 triệu, lãi GIẢ ĐỊNH 30%/năm, "
                 "trả tối thiểu 5% (sàn 100 nghìn), không tiêu thêm: 104 tháng, tổng lãi ≈ 13,2 triệu. Số thật: thu nhập bình quân người lao động quý "
                 "I/2026 ≈ 9,0 triệu đồng/tháng (Cục Thống kê); khảo sát người tiêu dùng 2025 trên 1.000 người Việt (qua báo chí). “3–6 tháng” là quy "
                 "tắc kinh nghiệm, không phải định luật. Kênh không chỉ định nơi gửi tiền hay sản phẩm nào."],
        "chapter_titles": {"ch00": "Mở đầu: một hoá đơn 15 triệu, hai phiên bản", "ch01": "Ô 1: một tháng thiết yếu là bao nhiêu", "ch02": "Ô 2: cần mấy tháng? (3–6 tháng)",
                           "ch03": "Ô 3: mỗi tháng để dành bao nhiêu, mất bao lâu", "ch04": "Cái giá của việc không có tấm đệm", "ch05": "Để ở đâu: ba tiêu chí",
                           "ch06": "Khi nào phép tính này không đúng với bạn"},
        "sources": ["https://www.vietnam-briefing.com/news/rising-confidence-vietnam-tops-asean-in-consumer-sentiment.html/",
                    "https://znews.vn/no-the-tin-dung-8-5-trieu-sau-11-nam-len-8-8-ty-tinh-lai-the-nao-post1465068.html"],
        "hashtags": ["TàiChínhCáNhân", "QuỹKhẩnCấp", "TiếtKiệm", "QuảnLýChiTiêu", "BiểuĐồBiếtNói"],
        "tags": ["quỹ khẩn cấp", "quỹ dự phòng", "quỹ khẩn cấp bao nhiêu là đủ", "tiết kiệm lương thấp", "3 đến 6 tháng chi tiêu", "tài chính cá nhân",
                 "để dành mỗi tháng", "quản lý chi tiêu", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: phép tính do kênh tự lập (ví dụ giả định); thu nhập bình quân theo Cục Thống kê; khảo sát người tiêu dùng 2025 qua báo chí.",
        "video_credits": Y4["video_credits"],
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
