"""A2 "Lương 10 triệu năm 2016 bằng bao nhiêu hôm nay" — quy đổi sức mua bằng chỉ số giá tiêu dùng (CPI).

    python data/long/ck-a2-luong-va-lam-phat/analysis.py      # in kết quả + ghi results.json

Dữ liệu: wb_cpi_index.json (World Bank WDI FP.CPI.TOTL, 2010 = 100, bình quân năm, từ số liệu Cục Thống kê; cập nhật 08/10/2026) và
wb_cpi_inflation.json (FP.CPI.TOTL.ZG, % bình quân năm). Năm 2026 chưa hết -> dùng CPI bình quân 9 tháng 2026 +4,52% so cùng kỳ
(Cục Thống kê, 30/09/2026) làm GIẢ ĐỊNH cho cả năm. Lương tối thiểu vùng I: 3,5 tr (2016, NĐ 122/2015) -> 5,31 tr (2026, NĐ 293/2025).
Thu nhập bình quân tháng người lao động quý III/2026: 9,2 tr, +823,8 nghìn so cùng kỳ (Cục Thống kê).
Nhân vật: anh Tuấn (VÍ DỤ GIẢ ĐỊNH), lương 10 tr năm 2016. Mức lạm phát 2027–2036 là GIẢ ĐỊNH 3/4/5%, không phải dự báo.
Kiểm độc lập: check.py.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
idx = {int(x["date"]): x["value"] for x in json.loads((HERE / "wb_cpi_index.json").read_text(encoding="utf-8"))[1] if x["value"]}
inf = {int(x["date"]): x["value"] for x in json.loads((HERE / "wb_cpi_inflation.json").read_text(encoding="utf-8"))[1] if x["value"]}
P26 = 0.0452
idx[2026] = idx[2025] * (1 + P26)

res = {}
m16_25 = idx[2025] / idx[2016]
m16_26 = idx[2026] / idx[2016]
res["mult_2016_2025"] = round(m16_25, 4)
res["mult_2016_2026"] = round(m16_26, 4)
res["salary_equiv_2026"] = round(10 * m16_26, 2)                 # 10 tr 2016 -> ? 2026
res["power_left_2026"] = round(10 / m16_26, 2)                   # 10 tr để yên từ 2016 -> sức mua bằng ? tr của 2016
res["avg_infl_2016_2025"] = round(100 * (m16_25 ** (1 / 9) - 1), 2)
res["avg_infl_2016_2026"] = round(100 * (m16_26 ** (1 / 10) - 1), 2)
res["yearly"] = {y: round(inf[y], 2) for y in range(2005, 2026)}
res["peak"] = {"2008": round(inf[2008], 2), "2011": round(inf[2011], 2)}
res["mult_1996_2025"] = round(idx[2025] / idx[1996], 3)
res["mult_2007_2008"] = round(idx[2008] / idx[2007], 4)
res["mult_2007_2012"] = round(idx[2012] / idx[2007], 4)           # 5 năm 2007 -> 2012
# lương 13 tr năm 2026: thực tăng hay giảm so 10 tr 2016?
for s in (12, 13, 14, 15):
    res[f"real_{s}"] = round(100 * (s / 10 / m16_26 - 1), 1)
# lương tối thiểu vùng I
mw = 5.31 / 3.5
res["minwage_mult"] = round(mw, 4)
res["minwage_real_pct"] = round(100 * (mw / m16_26 - 1), 1)
# thu nhập bình quân quý III/2026 vs cùng kỳ
q3, d = 9.2, 0.8238
nom = d / (q3 - d)
res["income_q3_nominal_pct"] = round(100 * nom, 1)
res["income_q3_real_pct_vs_cpi_sep"] = round(100 * ((1 + nom) / 1.0508 - 1), 1)      # so với CPI tháng 9 +5,08% y/y
res["income_q3_real_pct_vs_cpi_9m"] = round(100 * ((1 + nom) / (1 + P26) - 1), 1)
# 2036: giữ sức mua 10 tr 2016 -> cần bao nhiêu nếu lạm phát 2027–2036 là 3/4/5%/năm (giả định)
base = 10 * m16_26
res["need_2036"] = {f"{p:.0%}": round(base * (1 + p) ** 10, 1) for p in (0.03, 0.04, 0.05)}
# tăng lương danh nghĩa x% khi lạm phát 4,52%: tăng thực
res["raise_real"] = {f"{x}%": round(100 * ((1 + x / 100) / (1 + P26) - 1), 2) for x in (3, 5, 7, 10)}
# quy tắc 70: mất nửa sức mua sau bao năm
res["halve_years"] = {f"{p}%": round(math.log(2) / math.log(1 + p / 100), 1) for p in (3, 3.14, 4.52, 5)}
# lạm phát của riêng hai người (tháng 9/2026 so cùng kỳ, mức tăng từng nhóm/mặt hàng của Cục Thống kê; TỶ TRỌNG là GIẢ ĐỊNH của ví dụ)
TUAN = {"thuê nhà": (0.30, 4.88), "ăn uống ngoài gia đình": (0.25, 7.40), "thực phẩm tự nấu": (0.15, 3.89), "xăng xe (nhiên liệu)": (0.10, 23.96),
        "điện sinh hoạt": (0.05, 4.98), "điện thoại, internet": (0.10, 0.33), "thuốc, khám bệnh": (0.05, 1.47)}
MAI = {"thực phẩm tự nấu": (0.40, 3.89), "gạo, lương thực": (0.10, 0.81), "học phí, đồ dùng học cho con": (0.15, 2.93),
       "thuốc, khám bệnh": (0.10, 1.47), "điện sinh hoạt": (0.10, 4.98), "điện thoại, internet": (0.15, 0.33)}
for nm, g in (("tuan", TUAN), ("mai", MAI)):
    assert abs(sum(w for w, _ in g.values()) - 1) < 1e-9
    res[nm + "_basket"] = g
    res[nm + "_inflation"] = round(sum(w * x for w, x in g.values()), 2)
res["salary13_in_2016_money"] = round(13 / m16_26, 2)                       # 13 tr hôm nay = ? tr theo giá 2016
res["salary13_2036"] = {f"{g:.0%}": round(13 * (1 + g) ** 10, 1) for g in (0.03, 0.05, 0.07)}   # lương tăng danh nghĩa đều (giả định)
res["min_infl_2016_2025"] = min((round(inf[y], 2), y) for y in range(2016, 2026))
res["max_infl_2016_2025"] = max((round(inf[y], 2), y) for y in range(2016, 2026))
res["tuan_fuel_points"] = round(0.10 * 23.96, 2)                       # điểm % do xăng đóng góp vào 6,65
res["tuan_fuel_share_pct"] = round(100 * 0.10 * 23.96 / res["tuan_inflation"], 1)
res["tuan_yoy_real_pct"] = round(100 * (13 / 12.5 / (1 + P26) - 1), 2)       # ví dụ: năm ngoái 12,5 tr -> năm nay 13 tr
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "yearly"}, ensure_ascii=False, indent=1))
