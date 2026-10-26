"""E4 "Bảo hiểm tiền gửi 350 triệu" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH) + quy đổi hạn mức theo chỉ số giá.

    python data/long/ck-e4-bao-hiem-tien-gui/analysis.py      # in kết quả + ghi results.json

Giả định ví dụ (chị Thu, nhân vật giả định): 1,2 tỷ tiền để dành, cùng một sổ ở một tổ chức tham gia bảo hiểm tiền gửi, lãi giả định
7%/năm (đầu 10/2026, sổ 12 tháng niêm yết phổ biến từ gần 6% tới hơn 7%) — KHÔNG phải mức của tổ chức nào. Hạn mức: 350 triệu đồng / một người /
một tổ chức, gồm cả gốc và lãi (Thông tư 05/2026/TT-NHNN, từ 13/07/2026); trước đó 125 triệu (QĐ 32/2021/QĐ-TTg).
Quy đổi hạn mức các thời kỳ về giá năm 2025 bằng chỉ số giá tiêu dùng bình quân năm (World Bank WDI FP.CPI.TOTL, 2010 = 100,
lấy từ số liệu Cục Thống kê; file wb_cpi_index.json cùng thư mục). Kiểm độc lập: check.py.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAP, CAP_OLD = 350.0, 125.0            # triệu đồng
SAVE, R = 1200.0, 0.07                 # ví dụ giả định

cpi = {x["date"]: x["value"] for x in json.loads((HERE / "wb_cpi_index.json").read_text(encoding="utf-8"))[1] if x["value"]}
# mốc hạn mức: (năm bắt đầu áp dụng, triệu đồng). 1999: NĐ 89/1999 · 2005: NĐ 109/2005 · 2017: QĐ 21/2017 (từ 05/08/2017) · 2021: QĐ 32/2021
LIMITS = [(1999, 30.0), (2005, 50.0), (2017, 75.0), (2021, 125.0)]
real = {str(y): round(v * cpi["2025"] / cpi[str(y)], 1) for y, v in LIMITS}

res = {"assume": {"cap": CAP, "cap_old": CAP_OLD, "save": SAVE, "rate": R}}
res["thu"] = {
    "covered": CAP, "uncovered": SAVE - CAP,                      # gửi cả 1,2 tỷ ở một nơi: phần ngoài hạn mức (tính trên gốc)
    "uncovered_old": SAVE - CAP_OLD,
    "with_interest_1y": round(SAVE * (1 + R), 1),                 # gốc + lãi sau 1 năm
    "uncovered_1y": round(SAVE * (1 + R) - CAP, 1),
}
res["max_principal_1y"] = round(CAP / (1 + R), 1)                 # gốc tối đa để gốc + lãi 12 tháng vẫn trong hạn mức
res["max_principal_1y_6pct"] = round(CAP / 1.06, 1)
res["institutions_needed"] = math.ceil(SAVE * (1 + R) / CAP)      # số tổ chức để mọi sổ (gốc + lãi 1 năm) nằm trong hạn mức
# một sổ 300 triệu để cuộn lãi 7%/năm: năm thứ mấy vượt 350?
bal, yrs = 300.0, 0
while bal <= CAP:
    bal *= 1 + R
    yrs += 1
res["roll_300_cross_year"] = yrs
res["roll_300_after"] = round(bal, 1)
res["limit_real_2025"] = real                                     # hạn mức cũ quy về giá 2025
res["cpi_mult_1999_2025"] = round(cpi["2025"] / cpi["1999"], 3)
res["cap_change_pct"] = round(100 * (CAP / CAP_OLD - 1))          # +180%
res["share_over_cap_pct"] = round(100 - 93.68, 2)                 # 93,68% người gửi được bảo vệ toàn bộ -> 6,32% có tiền vượt
res["one_in_n_over"] = round(100 / (100 - 93.68), 1)              # cứ ~15,8 người gửi có 1 người vượt
res["couple_one_bank"] = 2 * CAP                                  # hai vợ chồng, mỗi người một sổ đứng tên mình
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
