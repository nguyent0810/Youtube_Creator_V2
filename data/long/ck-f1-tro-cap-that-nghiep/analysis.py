"""Phép tính minh hoạ cho ck-f1-tro-cap-that-nghiep (VÍ DỤ GIẢ ĐỊNH)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
wage, rate, cost, months_paid = 15, 0.60, 13, 7
benefit = wage * rate
shortfall = cost - benefit
minimum_wages = {"I": 5.31, "II": 4.73, "III": 4.14, "IV": 3.70}

result = {
    "assumption": {"insured_wage_million": wage, "living_cost_million": cost, "paid_months": 84},
    "monthly_benefit_million": benefit,
    "monthly_shortfall_million": shortfall,
    "duration": {"first_36_paid_months": 3, "extra_48_paid_months": 4, "total_months": months_paid, "cap_months": 12},
    "total_benefit_million": benefit * months_paid,
    "cumulative_shortfall_million": [shortfall * m for m in range(1, months_paid + 1)],
    "regional_caps_million": {region: round(value * 5, 2) for region, value in minimum_wages.items()},
    "waiting_days": {"current_law": 11, "previous_law": 16, "waiting_period": 10},
}
(HERE / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
