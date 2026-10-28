"""Phép tính cho ck-f2-vien-phi-bhyt. Toàn bộ hóa đơn Minh là VÍ DỤ GIẢ ĐỊNH."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
total, covered, rate, outside_invoice = 30.0, 25.0, 0.80, 2.0
fund = covered * rate
copay = covered - fund
outside_scope = total - covered
on_bill = copay + outside_scope
burden = on_bill + outside_invoice
res = {
    "assumption": "Minh va hoa don la VI DU GIA DINH, don vi trieu dong",
    "waterfall": {"total": total, "covered": covered, "fund": fund, "copay": copay,
                  "outside_scope": outside_scope, "on_bill": on_bill, "outside_invoice": outside_invoice,
                  "burden": burden},
    "five_year_threshold": {"reference_monthly": 2.53, "multiple": 6, "threshold": 6 * 2.53},
    "household_discount": [100, 70, 60, 50, 40],
    "out_of_pocket": {"early_2000s": 60, "year_2025": 40, "target_2028_2030_less_than": 30},
}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=2))
