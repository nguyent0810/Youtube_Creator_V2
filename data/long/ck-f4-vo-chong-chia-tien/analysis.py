"""Phép tính cho CK F4. Mọi khoản tiền là triệu đồng, VÍ DỤ GIẢ ĐỊNH."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
thao, nam, chi, months = 15.0, 25.0, 26.0, 12
total = thao + nam
equal = {"thao_contrib": chi / 2, "nam_contrib": chi / 2}
equal.update({"thao_left": thao - equal["thao_contrib"], "nam_left": nam - equal["nam_contrib"]})
share = {"thao": thao / total, "nam": nam / total}
pro = {"thao_contrib": chi * share["thao"], "nam_contrib": chi * share["nam"]}
pro.update({"thao_left": thao - pro["thao_contrib"], "nam_left": nam - pro["nam_contrib"]})
pool = {"after_cost": total - chi, "thao_left": 3.5, "nam_left": 3.5}
pool["common_left"] = pool["after_cost"] - pool["thao_left"] - pool["nam_left"]

res = {"assume": {"thao_income": thao, "nam_income": nam, "common_cost": chi, "months": months},
       "total_income": total, "remaining_after_cost": total - chi,
       "equal": equal, "proportional": pro, "pool": pool}
for name, plan in (("equal", equal), ("proportional", pro), ("pool", pool)):
    res[name]["month_12"] = {k: round(v * months, 2) for k, v in plan.items() if k.endswith("left")}
res["monthly_chart"] = [{"month": m,
    "equal": {"thao": equal["thao_left"] * m, "nam": equal["nam_left"] * m},
    "proportional": {"thao": pro["thao_left"] * m, "nam": pro["nam_left"] * m},
    "pool": {"thao": pool["thao_left"] * m, "nam": pool["nam_left"] * m, "common": pool["common_left"] * m}}
    for m in range(1, months + 1)]
res["cost_share_pct"] = {"equal_thao": round(equal["thao_contrib"] / thao * 100, 1),
                          "equal_nam": round(equal["nam_contrib"] / nam * 100, 1),
                          "proportional_thao": round(pro["thao_contrib"] / thao * 100, 1),
                          "proportional_nam": round(pro["nam_contrib"] / nam * 100, 1)}
res["sensitivity"] = [{"cost": x, "equal_thao": thao-x/2, "equal_nam": nam-x/2,
                       "pro_thao": thao-x*share["thao"], "pro_nam": nam-x*share["nam"]}
                      for x in (24, 26, 28, 30)]
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=2))
