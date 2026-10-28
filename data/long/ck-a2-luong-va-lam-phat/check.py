"""Kiểm độc lập cho analysis.py (A2): nhân chuỗi lạm phát từng năm (file % năm) thay cho tỷ số chỉ số (file chỉ số) mà analysis.py
dùng, rồi so với results.json. Hai chuỗi World Bank riêng -> lệch nhau ≤ 0,3% là chấp nhận.

    python data/long/ck-a2-luong-va-lam-phat/check.py
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = json.loads((H / "results.json").read_text(encoding="utf-8"))
inf = {int(x["date"]): x["value"] for x in json.loads((H / "wb_cpi_inflation.json").read_text(encoding="utf-8"))[1] if x["value"]}
m = 1.0
for y in range(2017, 2026):
    m *= 1 + inf[y] / 100
ok = [abs(m / R["mult_2016_2025"] - 1) < 0.003]
m26 = m * 1.0452
ok.append(abs(10 * m26 - R["salary_equiv_2026"]) < 0.05)                 # 13,8
ok.append(abs(10 / m26 - R["power_left_2026"]) < 0.05)                   # 7,25
for s in (12, 13, 14, 15):
    ok.append(abs(100 * (s / 10 / m26 - 1) - R[f"real_{s}"]) < 0.3)
ok.append(abs(100 * (5.31 / 3.5 / m26 - 1) - R["minwage_real_pct"]) < 0.3)
ok.append(abs(R["income_q3_nominal_pct"] - 100 * 0.8238 / (9.2 - 0.8238)) < 0.05)
for p, v in R["need_2036"].items():
    ok.append(abs(10 * m26 * (1 + float(p.rstrip("%")) / 100) ** 10 - v) < 0.15)
ok.append(abs(R["raise_real"]["5%"] - 100 * (1.05 / 1.0452 - 1)) < 0.01)
ok.append(abs(R["halve_years"]["3%"] - 23.4) < 0.05)
t = 0.30 * 4.88 + 0.25 * 7.40 + 0.15 * 3.89 + 0.10 * 23.96 + 0.05 * 4.98 + 0.10 * 0.33 + 0.05 * 1.47
mai = 0.40 * 3.89 + 0.10 * 0.81 + 0.15 * 2.93 + 0.10 * 1.47 + 0.10 * 4.98 + 0.15 * 0.33
ok += [abs(t - R["tuan_inflation"]) < 0.01, abs(mai - R["mai_inflation"]) < 0.01]
ok.append(abs(R["peak"]["2008"] - inf[2008]) < 0.01 and abs(R["mult_1996_2025"] - 4.617) < 0.01)
ok.append(abs(R["salary13_in_2016_money"] - 13 / m26) < 0.05)
ok += [abs(R["salary13_2036"]["7%"] - 13 * 1.07 ** 10) < 0.06, abs(R["salary13_2036"]["3%"] - 13 * 1.03 ** 10) < 0.06]
ok += [R["min_infl_2016_2025"][1] == 2021, R["max_infl_2016_2025"][1] == 2024]
ok += [abs(R["tuan_fuel_points"] - 2.396) < 0.01, abs(R["tuan_yoy_real_pct"] - 100 * (1.04 / 1.0452 - 1)) < 0.01]
print("A2 check:", "OK" if all(ok) else f"LỖI ở mục {[i for i, x in enumerate(ok) if not x]}", f"({len(ok)} phép)")
assert all(ok)
