"""Kiểm độc lập cho các phép tính VÍ DỤ GIẢ ĐỊNH trong analysis.py."""
import json
from pathlib import Path

R = json.loads((Path(__file__).resolve().parent / "results.json").read_text(encoding="utf-8"))
ok = []
ok.append(R["monthly_benefit_million"] == 9)
ok.append(R["monthly_shortfall_million"] == 4)
ok.append(R["duration"]["total_months"] == 3 + (84 - 36) // 12)
ok.append(R["total_benefit_million"] == 9 * 7)
ok.append(R["cumulative_shortfall_million"] == [4, 8, 12, 16, 20, 24, 28])
ok.append(R["regional_caps_million"] == {"I": 26.55, "II": 23.65, "III": 20.7, "IV": 18.5})
ok.append(R["waiting_days"] == {"current_law": 11, "previous_law": 16, "waiting_period": 10})
print("CK-F1 check:", "OK" if all(ok) else "LỖI", f"({len(ok)} phép)")
assert all(ok)
