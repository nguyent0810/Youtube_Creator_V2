"""Sinh spec.json + scenes/hud/bgm của từng chNN.json cho CK E5 "Lương 25 triệu nộp thuế bao nhiêu năm 2026? Bảng tra thuế TNCN mới".

    python motion/long/script_lines.py ck-e5-thue-tncn-2026      # lines + title từ script.md
    python data/long/ck-e5-thue-tncn-2026/gen_scenes.py         # scenes/hud/bgm + spec.json (giữ nguyên lines)

Kịch bản: script.md. Phép tính: analysis.py -> results.json (kiểm độc lập check.py, công thức rút gọn). Kiểm chứng + URL: factcheck.md.
Luật kênh: chỉ giải thích luật + phép tính, không tư vấn thuế; anh Khang, lương 25 tr, thưởng 50 tr = VÍ DỤ GIẢ ĐỊNH (nhãn mọi cảnh ví dụ);
bảng tra giả định đóng bảo hiểm trên toàn bộ lương, không phụ cấp miễn thuế, không thu nhập khác (ghi ở chân bảng).
B-roll: id Pexels từ kho đã soát của các Long CK trước — trước khi dựng: `pexels.py get` + `clip_sheet.py ck-e5-thue-tncn-2026`, cân nhắc thay
để không lặp diện mạo Long CK gần nhất (variety.py audit).
"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent
C4 = json.loads((D.parent / "ck-c4-duong-trung-binh" / "spec.json").read_text(encoding="utf-8"))
SAY = dict(C4["say"])
R = json.loads((D / "results.json").read_text(encoding="utf-8"))
BLUE, GOLD, UP, DOWN, VIOLET = "#38bdf8", "#fbbf24", "#22c55e", "#ef4444", "#a78bfa"
HYPO = "VÍ DỤ GIẢ ĐỊNH · ANH KHANG · 25 TRIỆU · 1 NGƯỜI PHỤ THUỘC"
LAW26 = "LUẬT THUẾ TNCN 109/2025/QH15 · ĐIỀU 10"
VM = "VIDEO MINH HỌA"
K = R["khang"]
assert round(1000 * K["2026"]["tax"]) == 34 and round(1000 * K["2025"]["tax"]) == 448 and round(1000 * K["2019"]["tax"]) == 728
T = R["table_k_vnd"]


def kd(x):                      # nghìn đồng -> "1.530"
    return f"{x:,}".replace(",", ".")


def row(g, at):
    return {"k": f"{g} TR", "v": " · ".join(kd(T[str(g)][str(d)]["2026"]) for d in (0, 1, 2)), "at": at}


CH = {}

CH["ch00"] = {"hud": {"k": "MỞ ĐẦU", "t": "HAI TỜ PHIẾU LƯƠNG"}, "bgm": {"mood": "curious", "gain": 0.10}, "scenes": [
    {"type": "broll", "vid": "8731555", "veil": 0.55, "illus": VM,
     "kin": [{"text": "ANH KHANG · KẾ TOÁN", "at": [0, "Anh"], "sm": True}, {"text": "LƯƠNG GỘP 25 TRIỆU", "at": [1, "Lương"], "acc": True},
             {"text": "1 con là người phụ thuộc · " + "ví dụ giả định", "at": [2, "Vợ"], "sm": True}]},
    {"type": "bars", "at": 3, "title": "DÒNG THUẾ TNCN TRÊN PHIẾU LƯƠNG (NGHÌN ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "THÁNG 12/2025", "v": 448, "lbl": "≈ 448", "at": [5, "Dòng"]}, {"k": "THÁNG 10/2026", "v": 34, "lbl": "≈ 34", "at": [7, "Dòng"], "acc": True}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "CÙNG MỨC LƯƠNG · CÙNG GIA ĐÌNH", "at": 8}, {"text": "không đổi việc · không tăng lương", "at": 9, "sm": True},
                                          {"text": "CHỈ CÓ LUẬT THAY ĐỔI", "at": 10, "acc": True}]},
    {"type": "broll", "at": 11, "vid": "7490451", "veil": 0.55, "illus": VM,
     "kin": [{"text": "tưởng phòng nhân sự tính nhầm", "at": 11, "sm": True}, {"text": "KHÔNG CÓ DÒNG NÀO SAI", "at": 13, "acc": True}]},
    {"type": "question", "at": 14, "text": "Sao có thể giảm\nhơn 13 lần như vậy?"},
    {"type": "slam", "at": 15, "text": "2019: ≈ 727.500 Đ", "sub": "CÙNG 25 TRIỆU · CÙNG 1 NGƯỜI PHỤ THUỘC"},
    {"type": "ledger", "at": 17, "title": "CUỐI VIDEO: BẢNG TRA", "rows": [{"k": "HÀNG", "v": "MỨC LƯƠNG GỘP", "at": [18, "Hàng"]},
                                                                       {"k": "CỘT", "v": "SỐ NGƯỜI PHỤ THUỘC", "at": [18, "cột"]}],
     "total": {"k": "BẠN", "v": "DỪNG HÌNH · TÌM Ô CỦA MÌNH", "at": 19}},
    {"type": "kinetic", "at": 20, "items": [{"text": "ĐI CÙNG MỘT ĐỒNG LƯƠNG", "at": 20, "acc": True}, {"text": "trên con đường nó thành tiền thuế", "at": [20, "trên"], "sm": True}]},
    {"type": "brand", "at": 21, "sub": "TIỀN BẠC · GIẢI THÍCH BẰNG DỮ LIỆU"},
    {"type": "kinetic", "at": 22, "items": [{"text": "CHỈ NHẰM GIÁO DỤC", "at": 22, "acc": True}, {"text": "giải thích luật bằng phép tính · không phải tư vấn thuế", "at": [22, "giải"], "sm": True}]},
]}

CH["ch01"] = {"hud": {"k": "CHẶNG 01", "t": "TỪ LƯƠNG GỘP TỚI THU NHẬP TÍNH THUẾ"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "1", "k": "CHẶNG MỘT", "title": "TỪ LƯƠNG GỘP\nTỚI THU NHẬP TÍNH THUẾ", "sub": "BẢO HIỂM · GIẢM TRỪ GIA CẢNH", "vid": "5466772", "illus": VM, "titleAt": [0, "Con"]},
    {"type": "ledger", "at": 2, "title": "TRẠM 1 · BẢO HIỂM BẮT BUỘC (NGƯỜI LAO ĐỘNG)", "rows": [{"k": "BẢO HIỂM XÃ HỘI", "v": "8%", "at": 3},
                                                                                             {"k": "BẢO HIỂM Y TẾ", "v": "1,5%", "at": 4},
                                                                                             {"k": "BẢO HIỂM THẤT NGHIỆP", "v": "1%", "at": 5}],
     "total": {"k": "CỘNG", "v": "10,5%", "at": 6}},
    {"type": "counter", "at": 7, "from": 25, "to": 22.375, "suffix": " TRIỆU", "until": [9, "Còn"], "label": "SAU BẢO HIỂM (25 − 2,625)", "sub": {"text": HYPO, "at": 8}},
    {"type": "bars", "at": 10, "title": "TRẠM 2 · GIẢM TRỪ GIA CẢNH (TRIỆU ĐỒNG/THÁNG)", "unit": "2025 → 2026",
     "items": [{"k": "BẢN THÂN · 2025", "v": 11, "lbl": "11", "at": [13, "Năm"]}, {"k": "BẢN THÂN · 2026", "v": 15.5, "lbl": "15,5", "at": [11, "mười"], "acc": True},
               {"k": "PHỤ THUỘC · 2025", "v": 4.4, "lbl": "4,4", "at": [13, "bốn"]}, {"k": "PHỤ THUỘC · 2026", "v": 6.2, "lbl": "6,2", "at": [12, "sáu"], "acc": True}],
     "label": {"k": LAW26, "v": "", "at": 11}},
    {"type": "question", "at": 14, "text": "Người phụ thuộc là ai\nmới được tính?"},
    {"type": "ledger", "at": 15, "title": "NGƯỜI PHỤ THUỘC", "rows": [{"k": "THƯỜNG LÀ", "v": "CON NHỎ · CHA MẸ · VỢ/CHỒNG", "at": 15},
                                                                   {"k": "NGƯỠNG THU NHẬP", "v": "1 → 3 TRIỆU/THÁNG", "at": [16, "một"]},
                                                                   {"k": "PHẢI", "v": "ĐĂNG KÝ MỚI ĐƯỢC TRỪ", "at": 17}]},
    {"type": "source", "at": 19, "source": "LUẬT THUẾ TNCN 109/2025/QH15", "ref": "ĐIỀU 10 · KHOẢN 3",
     "snippet": "mỗi người phụ thuộc chỉ được tính giảm trừ [[một lần vào một người nộp thuế]]", "hlAt": [20, "một"], "seal": "ANH HOẶC VỢ · KHÔNG CẢ HAI", "sealAt": 21},
    {"type": "bars", "at": 22, "title": "THUẾ CỦA ANH KHANG MỖI THÁNG (NGHÌN ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "CON ĐĂNG KÝ CHO ANH", "v": 33.75, "lbl": "≈ 34", "at": [22, "Giả"]},
               {"k": "CON ĐĂNG KÝ CHO VỢ (KHÔNG PHẢI NỘP)", "v": 343.75, "lbl": "≈ 344", "at": [24, "Còn"], "acc": True}]},
    {"type": "slam", "at": 25, "text": "≈ 3,7 TRIỆU/NĂM", "sub": "KHÁC NHAU Ở MỘT TỜ ĐĂNG KÝ"},
    {"type": "ledger", "at": 27, "title": "THU NHẬP TÍNH THUẾ CỦA ANH KHANG", "srcnote": HYPO, "rows": [{"k": "SAU BẢO HIỂM", "v": "22,375 TRIỆU", "at": [29, "Lấy"]},
                                                                                                {"k": "GIẢM TRỪ 15,5 + 6,2", "v": "− 21,7 TRIỆU", "at": [28, "Mười"]}],
     "total": {"k": "CÒN", "v": "675 NGHÌN", "at": [30, "Còn"]}},
    {"type": "kinetic", "at": 31, "items": [{"text": "KHÔNG PHẢI 25 TRIỆU", "at": 32}, {"text": "CHỈ HƠN NỬA TRIỆU", "at": 33, "acc": True},
                                           {"text": "qua một cái thang có năm bậc", "at": 34, "sm": True}]},
]}

CH["ch02"] = {"hud": {"k": "CHẶNG 02", "t": "CÁI THANG NĂM BẬC"}, "bgm": {"mood": "curious", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "2", "k": "CHẶNG HAI", "title": "CÁI THANG\nNĂM BẬC", "sub": "BIỂU THUẾ LUỸ TIẾN TỪNG PHẦN · 2026", "vid": "7593898", "illus": VM, "titleAt": [0, "Hãy"]},
    {"type": "bars", "at": 2, "title": "THUẾ SUẤT TỪNG BẬC (%)", "unit": "THU NHẬP TÍNH THUẾ/THÁNG · TỪ 2026",
     "items": [{"k": "ĐẾN 10 TR", "v": 5, "lbl": "5", "at": [2, "Bậc"]}, {"k": "10 – 30 TR", "v": 10, "lbl": "10", "at": [3, "Bậc"]},
               {"k": "30 – 60 TR", "v": 20, "lbl": "20", "at": [4, "Bậc"]}, {"k": "60 – 100 TR", "v": 30, "lbl": "30", "at": [6, "Từ"]},
               {"k": "TRÊN 100 TR", "v": 35, "lbl": "35", "at": [7, "Trên"], "acc": True}],
     "label": {"k": "LUẬT THUẾ TNCN 109/2025/QH15 (QUA TẠP CHÍ CÔNG THƯƠNG)", "v": "", "at": 2}},
    {"type": "question", "at": 8, "text": "Lên bậc hai thì cả lương\nbị tính 10% à?"},
    {"type": "myth", "at": 9, "mythLab": "NHIỀU NGƯỜI NGHĨ", "myth": "CẢ LƯƠNG CHỊU MỨC BẬC CAO", "truthLab": "THẬT RA", "truth": "CHỈ PHẦN TRÀN SANG BẬC ĐÓ",
     "strikeAt": [10, "Đây"], "truthAt": [11, "Chỉ"]},
    {"type": "counter", "at": 13, "from": 0, "to": 33750, "suffix": " Đ", "label": "675 NGHÌN × 5% · DÒNG THUẾ THÁNG 10", "sub": {"text": HYPO, "at": 14}},
    {"type": "bars", "at": 16, "title": "BIỂU 7 BẬC CŨ · NGƯỠNG TRÊN CỦA TỪNG BẬC (TRIỆU)", "unit": "ĐẾN HẾT 2025",
     "items": [{"k": "BẬC 1 · 5%", "v": 5, "lbl": "5", "at": [17, "Bậc"]}, {"k": "BẬC 2 · 10%", "v": 10, "lbl": "10", "at": [18, "Bậc"]},
               {"k": "BẬC 3 · 15%", "v": 18, "lbl": "18", "at": [18, "năm"]}, {"k": "BẬC 7 · 35% TỪ", "v": 80, "lbl": "80", "at": [19, "tám"], "acc": True}]},
    {"type": "bars", "at": 20, "title": "TNTT 20 TRIỆU/THÁNG · THUẾ (TRIỆU)", "unit": "KÊNH TỰ TÍNH",
     "items": [{"k": "THANG 7 BẬC CŨ", "v": 2.35, "lbl": "2,35", "at": [21, "Theo"]}, {"k": "THANG 5 BẬC MỚI", "v": 1.5, "lbl": "1,5", "at": [22, "Theo"], "acc": True}]},
    {"type": "ledger", "at": 23, "title": "LƯƠNG GỘP 50 TRIỆU · CHƯA CÓ NGƯỜI PHỤ THUỘC", "srcnote": "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH",
     "rows": [{"k": "THU NHẬP TÍNH THUẾ", "v": "≈ 29,25 TRIỆU", "at": 25}, {"k": "BẬC CAO NHẤT CHẠM", "v": "10%", "at": [25, "bậc"]},
              {"k": "TỔNG THUẾ", "v": "≈ 2,425 TRIỆU", "at": 26}], "total": {"k": "TRÊN LƯƠNG GỘP", "v": "≈ 4,85%", "at": 27}},
    {"type": "slam", "at": 28, "text": "BẬC CAO NHẤT ≠ TỈ LỆ THUẾ THẬT", "sub": ""},
    {"type": "kinetic", "at": 29, "items": [{"text": "BẬC RỘNG HƠN · TRÀN LÊN CHẬM HƠN", "at": 29}, {"text": "NỬA THỨ NHẤT CỦA CÂU TRẢ LỜI", "at": 30, "acc": True},
                                           {"text": "nửa thứ hai: hai tờ phiếu lương cũ", "at": 31, "sm": True}]},
]}

CH["ch03"] = {"hud": {"k": "CHẶNG 03", "t": "BA TỜ PHIẾU LƯƠNG"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "3", "k": "CHẶNG BA", "title": "BA TỜ PHIẾU LƯƠNG\nCÙNG MỘT CON SỐ", "sub": "2019 · 2025 · 2026", "vid": "6963972", "illus": VM, "titleAt": [0, "Bây"]},
    {"type": "ledger", "at": 2, "title": "THÁNG BẤT KỲ NĂM 2019", "srcnote": HYPO, "rows": [{"k": "GIẢM TRỪ", "v": "9 + 3,6 TRIỆU", "at": [2, "giảm"]},
                                                                                       {"k": "THU NHẬP TÍNH THUẾ", "v": "≈ 9,775 TRIỆU", "at": 3}],
     "total": {"k": "THUẾ", "v": "≈ 727.500 Đ", "at": 4}},
    {"type": "ledger", "at": 5, "title": "THÁNG 12/2025", "srcnote": HYPO, "rows": [{"k": "GIẢM TRỪ (TỪ 07/2020)", "v": "11 + 4,4 TRIỆU", "at": [5, "giảm"]},
                                                                                {"k": "THU NHẬP TÍNH THUẾ", "v": "≈ 6,975 TRIỆU", "at": 6}],
     "total": {"k": "THUẾ", "v": "≈ 447.500 Đ", "at": 7}},
    {"type": "bars", "at": 8, "title": "25 TRIỆU · 1 NPT · THUẾ/THÁNG (NGHÌN Đ)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "2019", "v": 727.5, "lbl": "727,5", "at": [8, "Năm"]}, {"k": "2025", "v": 447.5, "lbl": "447,5", "at": [8, "với"]},
               {"k": "2026", "v": 33.75, "lbl": "33,75", "at": 9, "acc": True}]},
    {"type": "counter", "at": 10, "from": 0, "to": 4.965, "suffix": " TRIỆU", "label": "GIỮ LẠI THÊM MỖI NĂM SO VỚI 2025", "sub": {"text": "12 × 413.750 Đ · " + HYPO.split(" · ")[0], "at": 11}},
    {"type": "question", "at": 12, "text": "Sao giảm trừ lại được\nnâng mạnh như vậy?"},
    {"type": "source", "at": 13, "source": "BỘ TÀI CHÍNH (QUA LSVN 05/01/2021)", "ref": "LUẬT CŨ · LUẬT 2025 XÉT THEO GIÁ CẢ VÀ THU NHẬP",
     "snippet": "CPI biến động [[trên 20%]] thì điều chỉnh mức giảm trừ gia cảnh", "hlAt": [14, "hai"], "seal": "CPI 2013 → 2020: +22%", "sealAt": 15},
    {"type": "bars", "at": 16, "title": "GIẢM TRỪ BẢN THÂN · QUY VỀ GIÁ 2026 (TRIỆU ĐỒNG)", "unit": "CPI · KÊNH TỰ TÍNH",
     "items": [{"k": "9 TR · 2013", "v": R["ded_real_2026"]["9_2013"], "lbl": "≈ 13,4", "at": [16, "Chín"]},
               {"k": "11 TR · 2020", "v": R["ded_real_2026"]["11_2020"], "lbl": "≈ 13,4", "at": [17, "Mười"]},
               {"k": "15,5 TR · 2026", "v": 15.5, "lbl": "15,5", "at": 19, "acc": True}],
     "label": {"k": "CPI BÌNH QUÂN NĂM: WORLD BANK WDI (TỪ SỐ LIỆU CỤC THỐNG KÊ) · 2026 GIẢ ĐỊNH +4,52%", "v": "", "at": 16}},
    {"type": "question", "at": 20, "text": "Lương bao nhiêu thì\nbắt đầu phải nộp thuế?"},
    {"type": "bars", "at": 21, "title": "LƯƠNG GỘP BẮT ĐẦU NỘP THUẾ", "unit": "TRIỆU/THÁNG",
     "items": [{"k": "0 NGƯỜI · 2026", "v": 17.32, "lbl": "≈ 17,3", "at": [21, "mười"], "acc": True}, {"k": "1 NGƯỜI · 2026", "v": 24.25, "lbl": "≈ 24,3", "at": 22, "acc": True},
               {"k": "2 NGƯỜI · 2026", "v": 31.17, "lbl": "≈ 31,2", "at": 23, "acc": True}, {"k": "0 / 1 / 2 · 2025", "v": 12.29, "lbl": "12,3 · 17,2 · 22,1", "at": 24}],
     "label": {"k": "GIẢ ĐỊNH ĐÓNG BẢO HIỂM 10,5% TRÊN TOÀN BỘ LƯƠNG · KÊNH TỰ TÍNH", "v": "", "at": 21}},
    {"type": "counter", "at": 25, "from": 9.2, "to": 9.2, "suffix": " TRIỆU", "label": "THU NHẬP BÌNH QUÂN THÁNG · QUÝ III/2026", "sub": {"text": "CỤC THỐNG KÊ · THẤP HƠN NGƯỠNG THẤP NHẤT", "at": 26}},
    {"type": "broll", "at": 27, "vid": "5615174", "veil": 0.55, "illus": VM,
     "kin": [{"text": "MƯỜI HAI THÁNG KHÔNG GIỐNG NHAU", "at": 27, "sm": True}, {"text": "THÁNG CÓ THƯỞNG TẾT", "at": 29, "acc": True}]},
]}

CH["ch04"] = {"hud": {"k": "CHẶNG 04", "t": "THÁNG CÓ THƯỞNG TẾT"}, "bgm": {"mood": "mystery", "gain": 0.10}, "scenes": [
    {"type": "chapter", "no": "4", "k": "CHẶNG BỐN", "title": "THÁNG CÓ\nTHƯỞNG TẾT", "sub": "KHẤU TRỪ THÁNG · QUYẾT TOÁN NĂM", "vid": "36112100", "illus": VM, "titleAt": [0, "Giả"]},
    {"type": "ledger", "at": 1, "title": "THÁNG CÓ THƯỞNG", "srcnote": "VÍ DỤ GIẢ ĐỊNH · THƯỞNG 50 TRIỆU", "rows": [{"k": "LƯƠNG", "v": "25 TRIỆU", "at": [1, "phiếu"]},
                                                                                                         {"k": "THƯỞNG", "v": "50 TRIỆU", "at": [1, "tổng"]}],
     "total": {"k": "TỔNG THÁNG ĐÓ", "v": "75 TRIỆU", "at": [1, "bảy"]}},
    {"type": "kinetic", "at": 2, "items": [{"text": "KHẤU TRỪ THEO TỪNG THÁNG", "at": 2}, {"text": "chưa ai biết chắc cả năm kiếm bao nhiêu", "at": 3, "sm": True},
                                          {"text": "MỖI THÁNG = MỘT NĂM THU NHỎ", "at": 4, "acc": True}]},
    {"type": "counter", "at": 6, "from": 0, "to": 6.635, "suffix": " TRIỆU", "label": "KHẤU TRỪ THÁNG CÓ THƯỞNG", "sub": {"text": "TNTT ≈ 50,675 TRIỆU · LÊN BẬC 3 (20%)", "at": [6, "lên"]}},
    {"type": "question", "at": 8, "text": "Gần 7 triệu tiền thuế\nchỉ cho một cái thưởng?"},
    {"type": "myth", "at": 9, "mythLab": "SỐ BỊ KHẤU TRỪ", "myth": "≈ 7 TRIỆU CẢ NĂM", "truthLab": "CHƯA CHẮC", "truth": "LÀ SỐ PHẢI NỘP THẬT", "strikeAt": [10, "Cộng"], "truthAt": [11, "Nhưng"]},
    {"type": "ledger", "at": 12, "title": "QUYẾT TOÁN CẢ NĂM", "srcnote": "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH", "rows": [
        {"k": "THU NHẬP CẢ NĂM", "v": "350 TRIỆU", "at": 13}, {"k": "THU NHẬP TÍNH THUẾ", "v": "≈ 58,1 TRIỆU", "at": 14},
        {"k": "MỖI THÁNG", "v": "< 5 TRIỆU · BẬC 1", "at": 15}], "total": {"k": "THUẾ ĐÚNG CẢ NĂM", "v": "≈ 2,905 TRIỆU", "at": 16}},
    {"type": "bars", "at": 17, "title": "CẢ NĂM CỦA ANH KHANG (TRIỆU ĐỒNG)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "ĐÃ BỊ KHẤU TRỪ", "v": 7.006, "lbl": "≈ 7,0", "at": [17, "Đã"]}, {"k": "THUẾ ĐÚNG", "v": 2.905, "lbl": "≈ 2,9", "at": [17, "Thuế"]},
               {"k": "NỘP THỪA · CÓ THỂ ĐƯỢC HOÀN", "v": 4.101, "lbl": "≈ 4,1", "at": 18, "acc": True}]},
    {"type": "date", "at": 20, "date": "2027", "sub": {"text": "QUYẾT TOÁN THUẾ CỦA NĂM 2026 · UỶ QUYỀN HOẶC TỰ LÀM", "at": 20}},
    {"type": "slam", "at": 23, "text": "CHƯA PHẢI CON SỐ CUỐI CÙNG", "sub": "KHẤU TRỪ TRONG THÁNG CÓ THƯỞNG"},
    {"type": "timeline", "at": 25, "title": "CON ĐƯỜNG CỦA MỘT ĐỒNG LƯƠNG", "items": [{"year": "1", "text": "bảo hiểm", "at": [25, "Bốn"]}, {"year": "2", "text": "giảm trừ", "at": [25, "từ"]},
                                                                                {"year": "3", "text": "cái thang", "at": [25, "bảo"]}, {"year": "4", "text": "quyết toán", "at": [25, "quyết"]}]},
]}

CH["ch05"] = {"hud": {"k": "BẢNG TRA", "t": "DỪNG HÌNH VÀ TÌM Ô CỦA BẠN"}, "bgm": {"mood": "calm", "gain": 0.09}, "scenes": [
    {"type": "chapter", "no": "5", "k": "BẢNG TRA", "title": "DỪNG HÌNH\nTÌM Ô CỦA BẠN", "sub": "THUẾ TNCN TIỀN LƯƠNG/THÁNG · TỪ 07/2026", "vid": "6962707", "illus": VM, "titleAt": [0, "Bảng"]},
    {"type": "ledger", "at": 1, "title": "THUẾ/THÁNG (NGHÌN Đ) · 0 · 1 · 2 NGƯỜI PHỤ THUỘC", "srcnote": "GIẢ ĐỊNH: BH 10,5% TOÀN BỘ LƯƠNG · KHÔNG PHỤ CẤP MIỄN THUẾ",
     "rows": [row(15, [1, "Hàng"]), row(20, 4), row(25, [4, "chưa"]), row(30, 6)]},
    {"type": "kinetic", "at": 7, "items": [{"text": "NĂM NGOÁI · 30 TR · 1 NGƯỜI", "at": 7, "sm": True}, {"text": "≈ 968 NGHÌN", "at": [7, "gần"], "acc": True}]},
    {"type": "ledger", "at": 8, "title": "THUẾ/THÁNG (NGHÌN Đ) · 0 · 1 · 2 NGƯỜI PHỤ THUỘC", "srcnote": "GIẢ ĐỊNH: BH 10,5% (TRẦN 50,6 TR) · KHÔNG THU NHẬP KHÁC",
     "rows": [row(40, 8), row(50, 11), row(70, 12), row(100, 13)]},
    {"type": "kinetic", "at": 14, "items": [{"text": "BẢO HIỂM CHẠM TRẦN", "at": 14}, {"text": "phần trừ không tăng theo lương nữa", "at": [14, "phần"], "sm": True}]},
    {"type": "ledger", "at": 15, "title": "CÁCH ĐỌC BẢNG", "rows": [{"k": "8 HÀNG", "v": "LƯƠNG 15 → 100 TRIỆU", "at": 15}, {"k": "Ô SỐ 0", "v": "THÁNG ẤY KHÔNG NỘP THUẾ", "at": 16},
                                                                 {"k": "+1 NGƯỜI PHỤ THUỘC", "v": "NGƯỠNG +≈ 6,9 TR LƯƠNG", "at": 18}]},
    {"type": "myth", "at": 19, "mythLab": "LỜI ĐỒN", "myth": "TĂNG LƯƠNG MÀ CẦM VỀ ÍT ĐI", "truthLab": "THẬT RA", "truth": "THUẾ CHỈ ĂN VÀO PHẦN TĂNG THÊM",
     "strikeAt": [20, "Nhưng"], "truthAt": [20, "không"]},
    {"type": "ledger", "at": 21, "title": "THUẾ/THÁNG (NGHÌN Đ) · DỪNG HÌNH ĐỂ TRA", "srcnote": "VÍ DỤ GIẢ ĐỊNH · KÊNH TỰ TÍNH · KHÔNG PHẢI TƯ VẤN THUẾ",
     "rows": [row(20, 21), row(30, 22), row(50, 23), row(100, 24)]},
]}

CH["ch06"] = {"hud": {"k": "GIỚI HẠN", "t": "KHI NÀO BẢNG TRA KHÔNG ĐÚNG"}, "bgm": {"mood": "calm", "gain": 0.11}, "scenes": [
    {"type": "chapter", "no": "6", "k": "PHẦN CUỐI", "title": "KHI NÀO BẢNG TRA\nKHÔNG ĐÚNG VỚI BẠN", "sub": "PHẦN GIỮ Ở CUỐI MỖI VIDEO", "vid": "8479054", "illus": VM, "titleAt": [0, "Như"]},
    {"type": "ledger", "at": 1, "title": "BẢNG CÒN GIẢ ĐỊNH", "rows": [{"k": "1", "v": "LƯƠNG ĐÓNG BH = LƯƠNG GỘP", "at": 1}, {"k": "2", "v": "KHÔNG CÓ KHOẢN MIỄN THUẾ", "at": 4},
                                                                    {"k": "3", "v": "CHỈ LƯƠNG Ở MỘT NƠI", "at": 7}]},
    {"type": "kinetic", "at": 8, "items": [{"text": "LÀM THÊM · HỢP ĐỒNG NGẮN · CHO THUÊ NHÀ", "at": 8, "sm": True}, {"text": "MỖI LOẠI MỘT CÁCH TÍNH RIÊNG", "at": [8, "đều"], "acc": True}]},
    {"type": "date", "at": 10, "date": "01/07/2026", "sub": {"text": "LUẬT CÓ HIỆU LỰC · PHẦN TIỀN LƯƠNG ÁP CHO CẢ KỲ TÍNH THUẾ 2026", "at": 10}},
    {"type": "ledger", "at": 13, "title": "BA CÂU TỰ HỎI TRƯỚC PHIẾU LƯƠNG", "rows": [{"k": "1", "v": "LƯƠNG ĐÓNG BH CỦA TÔI?", "at": 14}, {"k": "2", "v": "ĐĂNG KÝ NGƯỜI PHỤ THUỘC CHƯA?", "at": 15},
                                                                                   {"k": "3", "v": "THÁNG NÀO NHẬN KHOẢN LỚN?", "at": 16}]},
    {"type": "bars", "at": 17, "title": "BA TỜ PHIẾU LƯƠNG · CÙNG 25 TRIỆU (NGHÌN Đ)", "unit": "VÍ DỤ GIẢ ĐỊNH",
     "items": [{"k": "2019", "v": 727.5, "lbl": "727", "at": [19, "Bảy"]}, {"k": "2025", "v": 447.5, "lbl": "448", "at": [19, "Bốn"]},
               {"k": "2026", "v": 33.75, "lbl": "34", "at": [19, "Ba"], "acc": True}]},
    {"type": "kinetic", "at": 20, "items": [{"text": "CON SỐ TRÊN HỢP ĐỒNG KHÔNG ĐỔI", "at": 20}, {"text": "THỨ ĐỔI LÀ NHỮNG DÒNG NHỎ Ở GIỮA", "at": 21, "acc": True},
                                           {"text": "cả năm ≈ 5 triệu của một gia đình", "at": 22, "sm": True}]},
    {"type": "question", "at": 23, "text": "Phiếu lương tháng này của bạn,\ndòng thuế ghi bao nhiêu?"},
    {"type": "kinetic", "at": 24, "items": [{"text": "KỂ CHO MÌNH NGHE", "at": 24}, {"text": "Ở PHẦN BÌNH LUẬN", "at": [24, "ở"], "acc": True}]},
]}

Y4 = C4["youtube"]
TITLES = ["Lương 25 Triệu Nộp Thuế Bao Nhiêu Năm 2026?",
          "Cùng Lương 25 Triệu: Năm 2019 Nộp 727 Nghìn Thuế, Năm 2026 Còn 34 Nghìn. Vì Sao?",
          "Thưởng Tết 50 Triệu Bị Trừ Thuế Hơn 6 Triệu? Cách Tính Thuế TNCN 2026 Và Tiền Hoàn Thuế"]
FORMULA = ("📐 CÁCH TÍNH (ví dụ giả định · kênh tự tính · thay bằng số của bạn)\n• Thu nhập tính thuế/tháng = lương gộp − bảo hiểm bắt buộc (8% + 1,5% + 1%) "
           "− 15,5 triệu − 6,2 triệu × số người phụ thuộc\n• Thuế = cộng dồn từng bậc: đến 10 tr × 5%; 10–30 tr × 10%; 30–60 tr × 20%; 60–100 tr × 30%; trên 100 tr × 35%\n"
           "• Anh Khang 25 tr, 1 người phụ thuộc: 25 − 2,625 − 21,7 = 0,675 tr → 33.750 đ/tháng (2025: 447.500 đ; 2019: 727.500 đ)\n"
           "• Bảng tra giả định đóng bảo hiểm trên toàn bộ lương (trần 50,6 tr từ 07/2026), không phụ cấp miễn thuế, không thu nhập khác.")
SPEC = {
    "title": TITLES[0],
    "channel": "CK", "accent": "#fbbf24", "master": True, "endcard": 20, "endcardSub": "VIDEO TIẾP THEO", "beat2": True,
    "acc": ["thuế", "giảm", "trừ", "bậc", "lương", "triệu", "nghìn"],
    "say": SAY, "imgs": {}, "chapters": [f"ch{i:02d}" for i in range(7)],
    "youtube": {
        "titles": TITLES,
        "summary": "Cùng lương gộp 25 triệu và một người phụ thuộc: tháng 12/2025 dòng thuế thu nhập cá nhân khoảng 448 nghìn, tháng 10/2026 chỉ còn "
                   "khoảng 34 nghìn. Video đi cùng một đồng lương: trừ bảo hiểm bắt buộc, giảm trừ gia cảnh mới 15,5 triệu và 6,2 triệu cho mỗi "
                   "người phụ thuộc, biểu thuế 5 bậc, vì sao tháng có thưởng Tết bị khấu trừ nhiều hơn và phần nộp thừa được tính lại khi quyết toán, "
                   "rồi một bảng tra thuế theo mức lương và số người phụ thuộc để bạn dừng hình tìm ô của mình.",
        "more": ["Nội dung giáo dục, không phải tư vấn đầu tư. Cũng không phải tư vấn thuế: kênh chỉ giải thích quy định bằng phép tính. Anh Khang, mức lương, "
                 "khoản thưởng là ví dụ giả định do kênh tự tính; bảng tra giả định đóng bảo hiểm trên toàn bộ lương, không có phụ cấp miễn thuế và thu "
                 "nhập khác. Quy định mô tả theo thời điểm làm video (10/2026) và có thể thay đổi; số thuế thật của bạn theo hợp đồng, bảng lương và "
                 "hướng dẫn của cơ quan thuế. Nội dung do kênh biên soạn từ nguồn công khai; giọng đọc tổng hợp.", FORMULA],
        "chapter_titles": {"ch00": "Mở đầu: hai tờ phiếu lương", "ch01": "Từ lương gộp tới thu nhập tính thuế (giảm trừ 15,5 / 6,2 triệu)",
                           "ch02": "Cái thang năm bậc: biểu thuế mới 2026", "ch03": "Ba tờ phiếu lương 2019 · 2025 · 2026 và ngưỡng bắt đầu nộp thuế",
                           "ch04": "Tháng có thưởng Tết: khấu trừ và quyết toán", "ch05": "Bảng tra thuế theo lương và người phụ thuộc",
                           "ch06": "Khi nào bảng tra không đúng với bạn"},
        "sources": [
            "Công báo — Luật Thuế thu nhập cá nhân số 109/2025/QH15 (văn bản gốc; Điều 9 biểu thuế, Điều 10 giảm trừ, Điều 29 hiệu lực): https://congbao.chinhphu.vn/van-ban/luat-so-109-2025-qh15-468671.htm",
            "Cổng TTĐT Chính phủ 07/07/2026 — Mức thu nhập của người phụ thuộc không vượt quá 3 triệu đồng (Thông tư 87/2026/TT-BTC): https://xaydungchinhsach.chinhphu.vn/muc-thu-nhap-cua-nguoi-phu-thuoc-ma-nguoi-nop-thue-duoc-ap-dung-giam-tru-gia-canh-119260707113118697.htm",
            "Tạp chí Công Thương 15/10/2026 — Những điểm mới của Luật Thuế TNCN 2025 (biểu 5 bậc, giảm trừ 15,5/6,2 triệu): https://tapchicongthuong.vn/nhung-diem-moi-cua-luat-thue-thu-nhap-ca-nhan-nam-2025-va-tac-dong-den-doi-song-kinh-te-xa-hoi-556804.htm",
            "Hệ thống pháp luật — Thu nhập bao nhiêu thì phải nộp thuế TNCN năm 2026: https://hethongphapluat.com/phap-luat/huong-dan-chinh-sach-phap-luat/thu-nhap-bao-nhieu-thi-phai-nop-thue-tncn-nam-2026.html",
            "LuatVietnam 01/02/2026 — Mức đóng BHXH, BHYT, BHTN 2026: https://luatvietnam.vn/bao-hiem/tu-2026-muc-dong-bhxh-bhyt-bhtn-cua-nld-va-nsdld-duoc-tinh-nhu-the-nao-563-106906-article.html",
            "LSVN — Nghị định 161/2026/NĐ-CP, lương cơ sở 2,53 triệu từ 01/7/2026, trần đóng BHXH 50,6 triệu: https://lsvn.vn/tag/nghi-dinh-so-1612026ndcp.html",
            "BHTGVN 26/06/2020 — Giảm trừ gia cảnh 11/4,4 triệu và quy định người phụ thuộc: https://div.gov.vn/nguoi-lao-dong-can-biet-tang-muc-giam-tru-gia-canh-va-ho-so-chung-minh-nguoi-phu-thuoc-khi-nop-thue-thu-nhap-ca-nhan",
            "LSVN 05/01/2021 — Điều chỉnh giảm trừ khi CPI biến động trên 20%: https://lsvn.vn/giam-tru-gia-canh-tang-len-11-trieu-dong-thu-nhap-bao-nhieu-thi-phai-nop-thue-a44930.html",
            "Cục Thống kê — Thông cáo báo chí lao động việc làm quý III/2026: https://www.nso.gov.vn/wp-content/uploads/2026/10/Thong-cao-bao-chi-ve-tinh-hinh-lao-dong-viec-lam-QIII-nam-2026.pdf",
            "World Bank WDI — Consumer price index (2010 = 100), Viet Nam: https://data.worldbank.org/indicator/FP.CPI.TOTL?locations=VN"],
        "hashtags": ["ThuếThuNhậpCáNhân", "GiảmTrừGiaCảnh", "TàiChínhCáNhân", "BiểuĐồBiếtNói"],
        "tags": ["thuế thu nhập cá nhân 2026", "cách tính thuế thu nhập cá nhân", "giảm trừ gia cảnh 15,5 triệu", "biểu thuế 5 bậc", "lương 25 triệu đóng thuế bao nhiêu",
                 "quyết toán thuế TNCN", "hoàn thuế thu nhập cá nhân", "người phụ thuộc", "tài chính cá nhân", "biểu đồ biết nói"],
        "category": Y4["category"], "thumb": "t1.jpg",
        "data_credit": "📊 SỐ LIỆU: quy định thuế và bảo hiểm theo các nguồn ở trên; chỉ số giá tiêu dùng theo World Bank WDI (từ số liệu Cục Thống kê); "
                       "ví dụ anh Khang và bảng tra do kênh tự tính.",
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
