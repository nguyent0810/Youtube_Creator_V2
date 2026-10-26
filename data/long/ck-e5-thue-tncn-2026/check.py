"""Kiểm độc lập cho analysis.py (E5): tính thuế bằng CÔNG THỨC RÚT GỌN (thuế = TNTT × thuế suất bậc − số trừ), khác cách cộng dồn
từng bậc của analysis.py, rồi so với results.json.

    python data/long/ck-e5-thue-tncn-2026/check.py
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = json.loads((H / "results.json").read_text(encoding="utf-8"))
# (ngưỡng trên, thuế suất, số trừ); số trừ = Σ (thuế suất bậc − thuế suất bậc trước) × ngưỡng dưới của bậc
NEW = [(10, .05, 0), (30, .10, .5), (60, .20, 3.5), (100, .30, 9.5), (1e9, .35, 14.5)]
OLD = [(5, .05, 0), (10, .10, .25), (18, .15, .75), (32, .20, 1.65), (52, .25, 3.25), (80, .30, 5.85), (1e9, .35, 9.85)]


def tax(ti, t):
    if ti <= 0:
        return 0.0
    for hi, rate, sub in t:
        if ti <= hi:
            return ti * rate - sub


def ins26(g):
    return 0.095 * min(g, 50.6) + 0.01 * min(g, 106.2)


ok = []
ins = 25 * 0.105
ok.append(abs(R["khang"]["2026"]["tax"] - tax(25 - ins - 15.5 - 6.2, NEW)) < 1e-6)     # 0,03375
ok.append(abs(R["khang"]["2025"]["tax"] - tax(25 - ins - 11 - 4.4, OLD)) < 1e-6)       # 0,4475
ok.append(abs(R["khang"]["2019"]["tax"] - tax(25 - ins - 9 - 3.6, OLD)) < 1e-6)        # 0,7275
ok.append(abs(R["khang"]["save_year"] - 12 * (0.4475 - 0.03375)) < 1e-6)
for d, g in R["threshold_gross_2026"].items():
    dd = int(d)
    ok.append(tax(g - 0.105 * g - 15.5 - 6.2 * dd, NEW) < 0.002 and tax(g + 0.1 - 0.105 * (g + 0.1) - 15.5 - 6.2 * dd, NEW) > 0)
ok.append(abs(R["ti20"]["old"] - tax(20, OLD)) < 1e-9 and abs(R["ti20"]["new"] - tax(20, NEW)) < 1e-9)
b = R["bonus"]
wh = tax(75 - ins - 21.7, NEW) + 11 * tax(25 - ins - 21.7, NEW)
ann = 12 * tax((350 - 12 * ins - 12 * 21.7) / 12, NEW)
ok.append(abs(b["withheld_year"] - wh) < 1e-3 and abs(b["annual_tax"] - ann) < 1e-3 and abs(b["refund"] - (wh - ann)) < 1e-3)
for g, d in ((20, 0), (25, 0), (30, 1), (40, 2), (50, 0), (70, 1), (100, 2)):
    ok.append(R["table_k_vnd"][str(g)][str(d)]["2026"] == round(1000 * tax(g - ins26(g) - 15.5 - 6.2 * d, NEW)))
ok.append(abs(R["g50d0"]["tax"] - tax(50 - ins26(50) - 15.5, NEW)) < 1e-6 and abs(R["g50d0"]["effective_pct"] - 100 * tax(50 - ins26(50) - 15.5, NEW) / 50) < 0.01)
ok.append(abs(R["khang_no_dep"]["diff_year"] - 12 * (tax(25 - ins - 15.5, NEW) - tax(25 - ins - 21.7, NEW))) < 1e-6)
idx = {x["date"]: x["value"] for x in json.loads((H / "wb_cpi_index.json").read_text(encoding="utf-8"))[1] if x["value"]}
c26 = idx["2025"] * 1.0452
ok.append(abs(R["ded_real_2026"]["9_2013"] - 9 * c26 / idx["2013"]) < 0.01 and abs(R["ded_real_2026"]["11_2020"] - 11 * c26 / idx["2020"]) < 0.01)
print("E5 check:", "OK" if all(ok) else f"LỖI ở mục {[i for i, x in enumerate(ok) if not x]}", f"({len(ok)} phép)")
assert all(ok)
