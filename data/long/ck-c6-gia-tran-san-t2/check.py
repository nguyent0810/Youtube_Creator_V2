"""Tính lại độc lập các phép tính của ck-c6-gia-tran-san-t2."""
import json
from pathlib import Path

R = json.loads((Path(__file__).resolve().parent / "results.json").read_text(encoding="utf-8"))
ok = []
# Dùng phép cộng/trừ thay vì công thức của analysis.py.
ok += [R["band"]["floor_vnd"] == 20_000 - 1_400]
ok += [R["band"]["ceiling_vnd"] == 20_000 + 1_400]
ok += [R["order"]["value_vnd"] == sum([20_000] * 100)]
ok += [R["apr_3_2025"]["other_down"] == 254]
ok += [R["apr_3_2025"]["floor_down"] + R["apr_3_2025"]["other_down"] == R["apr_3_2025"]["down_total"]]
ok += [R["index"]["apr_3"] - R["index"]["apr_3_change"] == 1317.83]
ok += [R["index"]["apr_9"] - R["index"]["apr_9_change"] == 1132.79]
ok += [R["tuan_ledger"]["T"]["shares_sellable"] == 0, R["tuan_ledger"]["T1"]["shares_sellable"] == 0]
ok += [R["tuan_ledger"]["T2_afternoon"]["shares_sellable"] == 100]
ok += [R["special_band"] == {"hose_first_or_resume": .20, "upcom_first_or_resume": .40, "upcom_regular": .15}]
print("C6 check:", "OK" if all(ok) else "LỖI", f"({len(ok)} phép)")
assert all(ok)
