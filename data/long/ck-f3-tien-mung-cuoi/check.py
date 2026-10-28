"""Kiểm độc lập: không dùng các biến hoặc phép cộng của analysis.py."""
import json
from pathlib import Path

r = json.loads((Path(__file__).resolve().parent / "results.json").read_text(encoding="utf-8"))
ok = [
    r["wedding_total_million"] == 3.5,
    r["other_total_million"] == 2.1,
    r["annual_total_million"] == 5.6,
    r["share_of_monthly_wage_pct"] == round(5600000 / 12000000 * 100, 2),
    r["envelope_500k_share_pct"] == round(500000 / 12000000 * 100, 2),
    r["running_million"] == [0, .8, .8, 1.5, 2, 2, 2.3, 2.8, 2.8, 3.6, 4.6, 5.6],
    r["event_count"] == 14 and r["buffer_million"] == .4,
    r["scenario_million"] == {
        "one_less_close_friend_wedding": .7,
        "one_more_colleague_wedding": 2.0,
        "one_less_lucky_envelope_other_total": 1.9,
        "one_less_lucky_envelope_annual_total": 5.4,
    },
]
print("F3 check:", "OK" if all(ok) else "LỖI")
assert all(ok)
