"""E2 "Quỹ khẩn cấp" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH).

    python data/long/ck-e2-quy-khan-cap/analysis.py      # in bảng + ghi results.json

Giả định: chi thiết yếu 8 triệu/tháng; đích 3 tháng = 24 triệu; để dành 1,5 triệu/tháng (không tính lãi cho đơn giản).
Phiên bản không có quỹ: nợ thẻ 15 triệu, lãi giả định 30%/năm (2,5%/tháng), trả tối thiểu 5% (sàn 100 nghìn), không tiêu thêm, không phí (như bài E3).
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ESS, SAVE = 8.0, 1.5
res = {"target3": ESS * 3, "target6": ESS * 6,
       "months": {"one_month": round(ESS / SAVE, 1), "bill15": math.ceil(15 / SAVE), "three_months": math.ceil(ESS * 3 / SAVE), "at_1m": math.ceil(ESS * 3 / 1.0)},
       "path": [round(min(ESS * 3, SAVE * m), 1) for m in range(0, 17)]}
bal, m, intr = 15.0, 0, 0.0
while bal > 1e-6 and m < 600:
    i = bal * 0.025
    intr += i
    bal += i
    bal -= min(bal, max(0.05 * bal, 0.1))
    m += 1
res["card15"] = {"months": m, "years": round(m / 12, 1), "interest": round(intr, 2)}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(res)
