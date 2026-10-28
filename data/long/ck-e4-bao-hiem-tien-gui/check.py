"""Kiểm độc lập cho analysis.py (E4): tính lại bằng cách khác (Decimal, công thức đóng, không dùng lại vòng lặp của analysis),
so với results.json.

    python data/long/ck-e4-bao-hiem-tien-gui/check.py
"""
import json
from decimal import Decimal as D, ROUND_CEILING
from pathlib import Path

H = Path(__file__).resolve().parent
R = json.loads((H / "results.json").read_text(encoding="utf-8"))
cap, save, r = D(350), D(1200), D("0.07")
ok = []
ok.append(R["thu"]["uncovered"] == float(save - cap) == 850)
ok.append(R["thu"]["uncovered_old"] == 1075)
ok.append(abs(R["thu"]["with_interest_1y"] - float(save * (1 + r))) < 0.05)
ok.append(abs(R["max_principal_1y"] - float(cap / (1 + r))) < 0.05)                                   # 327,1
ok.append(R["institutions_needed"] == int((save * (1 + r) / cap).to_integral_value(ROUND_CEILING)))     # 4
n = next(k for k in range(1, 10) if D(300) * (1 + r) ** k > cap)                                     # năm đầu tiên vượt 350
ok.append(R["roll_300_cross_year"] == n == 3)
ok.append(abs(R["roll_300_after"] - float(D(300) * (1 + r) ** 3)) < 0.05)
cpi = {x["date"]: D(str(x["value"])) for x in json.loads((H / "wb_cpi_index.json").read_text(encoding="utf-8"))[1] if x["value"]}
for y, v in (("1999", 30), ("2005", 50), ("2017", 75), ("2021", 125)):
    ok.append(abs(R["limit_real_2025"][y] - float(D(v) * cpi["2025"] / cpi[y])) < 0.06)
ok.append(R["cap_change_pct"] == 180 and abs(R["one_in_n_over"] - 100 / 6.32) < 0.05)
print("E4 check:", "OK" if all(ok) else f"LỖI ở mục {[i for i, x in enumerate(ok) if not x]}", f"({len(ok)} phép)")
assert all(ok)
