"""Kiểm độc lập CK F4: dùng công thức viết lại, không gọi analysis.py."""
import json
from pathlib import Path

r = json.loads((Path(__file__).resolve().parent / "results.json").read_text(encoding="utf-8"))
ok = []
ok += [r["total_income"] == 15 + 25, r["remaining_after_cost"] == 40 - 26]
ok += [r["equal"]["thao_left"] == 15 - 26/2, r["equal"]["nam_left"] == 25 - 26/2]
ok += [r["proportional"]["thao_contrib"] == 26 * 15/40, r["proportional"]["nam_contrib"] == 26 * 25/40]
ok += [r["proportional"]["thao_left"] == 15 - 26*15/40, r["proportional"]["nam_left"] == 25 - 26*25/40]
ok += [r["pool"]["after_cost"] == 40-26, r["pool"]["common_left"] == 14-3.5-3.5]
ok += [r["equal"]["month_12"] == {"thao_left": 24.0, "nam_left": 144.0}]
ok += [r["proportional"]["month_12"] == {"thao_left": 63.0, "nam_left": 105.0}]
ok += [r["pool"]["month_12"] == {"thao_left": 42.0, "nam_left": 42.0, "common_left": 84.0}]
last = r["monthly_chart"][-1]
ok += [last["equal"] == {"thao": 24.0, "nam": 144.0}, last["proportional"] == {"thao": 63.0, "nam": 105.0}]
ok += [last["pool"] == {"thao": 42.0, "nam": 42.0, "common": 84.0}]
ok += [r["cost_share_pct"] == {"equal_thao": 86.7, "equal_nam": 52.0, "proportional_thao": 65.0, "proportional_nam": 65.0}]
assert all(ok), [i for i, x in enumerate(ok) if not x]
print(f"CK F4 check: OK ({len(ok)} phép)")
