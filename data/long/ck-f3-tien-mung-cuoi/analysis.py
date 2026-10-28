"""Phép tính cho ck-f3-tien-mung-cuoi. Mọi đầu vào là VÍ DỤ GIẢ ĐỊNH."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
wage = 12.0
wedding = {"ban_than": 2 * 0.7, "dong_nghiep": 3 * 0.5, "ho_hang": 2 * 0.3}
other = {"li_xi": 4 * 0.2, "tan_gia": 0.5, "day_thang": 0.3, "dam_hieu": 0.5}
heat = [0, .8, 0, .7, .5, 0, .3, .5, 0, .8, 1, 1]
total_wedding = round(sum(wedding.values()), 1)
total_other = round(sum(other.values()), 1)
total = round(total_wedding + total_other, 1)
running, acc = [], 0
for value in heat:
    acc = round(acc + value, 1)
    running.append(acc)
result = {
    "assumption": {"monthly_wage_million": wage, "label": "VÍ DỤ GIẢ ĐỊNH"},
    "wedding_million": wedding, "other_million": other,
    "wedding_total_million": total_wedding, "other_total_million": total_other,
    "annual_total_million": total, "share_of_monthly_wage_pct": round(total / wage * 100, 2),
    "envelope_500k_share_pct": round(.5 / wage * 100, 2),
    "heat_monthly_million": heat, "running_million": running,
    "event_count": 14, "cap_million": 6.0, "buffer_million": round(6 - total, 1),
    "scenario_million": {
        "one_less_close_friend_wedding": round(wedding["ban_than"] - .7, 1),
        "one_more_colleague_wedding": round(wedding["dong_nghiep"] + .5, 1),
        "one_less_lucky_envelope_other_total": round(total_other - .2, 1),
        "one_less_lucky_envelope_annual_total": round(total - .2, 1),
    },
}
(HERE / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
