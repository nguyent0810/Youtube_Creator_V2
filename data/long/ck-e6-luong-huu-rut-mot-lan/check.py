"""Kiểm độc lập cho analysis.py (E6): tính lại bằng bảng tỷ lệ viết tay theo lời luật và mô phỏng tháng (không dùng hàm của
analysis), so với results.json.

    python data/long/ck-e6-luong-huu-rut-mot-lan/check.py
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = json.loads((H / "results.json").read_text(encoding="utf-8"))
FEMALE = {15: 45, 20: 55, 25: 65, 30: 75}           # 45% + 2%/năm sau năm thứ 15, trần 75% ở năm 30
MALE = {15: 40, 18: 43, 20: 45, 25: 55, 30: 65, 35: 75}
ok = [R["lump_now"] == 10 * 2 * 10, R["lump_if_pre2014_mix"] == 10 * (4 * 1.5 + 6 * 2)]
for y, p in FEMALE.items():
    o = R["female"][str(y)]
    pen = 10 * p / 100
    ok += [abs(o["pension"] - pen) < 1e-9, abs(o["months_to_match_lump"] - 200 / pen) < 0.06,
           abs(o["sum_to_77"] - pen * 12 * 17.3) < 0.6, abs(o["employee_contrib_more"] - 0.8 * 12 * (y - 10)) < 1e-6, o["year_reach"] == 2016 + y]
ok += [abs(R["male_rates"][str(y)] - p / 100) < 1e-9 for y, p in MALE.items()]
ok += [R["lump_grow_2051"]["2%"] == round(200 * 1.02 ** 25), R["lump_grow_2051"]["3%"] == round(200 * 1.03 ** 25)]
bal, m = float(R["lump_grow_2051"]["2%"]), 0
while bal > 0:                                      # rút đều 4,5 tr/tháng, lãi thực 2%/năm
    bal = bal * (1 + 0.02 / 12) - 4.5
    m += 1
ok.append(abs(m - R["lump_2pct_as_4_5_months"]) <= 1)
ok += [R["own_contrib_10y"] == 96.0, R["male_15y_pension"] == 4.0, R["debt30_interest_saved_1y"] == 60.0, R["lump_grow_2051"]["-1%"] == round(200 * 0.99 ** 25)]
ok.append(R["stats_2016_2022"]["under10y_pct"] == 90.4)
print("E6 check:", "OK" if all(ok) else f"LỖI ở mục {[i for i, x in enumerate(ok) if not x]}", f"({len(ok)} phép)")
assert all(ok)
