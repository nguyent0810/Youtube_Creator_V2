"""E3 "Nợ thẻ tín dụng" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH).

    python data/long/ck-e3-no-the-tin-dung/analysis.py      # in bảng + ghi results.json

Giả định: nợ 20 triệu, lãi 30%/năm tính theo tháng (2,5%/tháng) trên dư nợ đầu tháng, trả cuối tháng, KHÔNG tiêu thêm, KHÔNG phí.
"Chỉ trả tối thiểu" = 5% dư nợ sau khi cộng lãi, sàn 100 nghìn đồng. Đây là phép tính, không phải cách tính của thẻ nào.
Phép tính ngược cho vụ báo chí đăng 03/2024: (8.830 / 8,55)^(1/132) - 1 (132 tháng = 11 năm), giả định lớn đều mỗi tháng, không lần trả nào.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEBT, APR = 20.0, 0.30          # triệu đồng
r = APR / 12


def run(pay):
    bal, m, intr, path = DEBT, 0, 0.0, [DEBT]
    while bal > 1e-6 and m < 600:
        i = bal * r
        intr += i
        bal += i
        bal -= min(bal, pay(bal))
        m += 1
        path.append(round(bal, 2))
    return m, intr, path


def pad(path, n=121):
    return (path + [0.0] * n)[:n]


res = {"assume": {"debt": DEBT, "apr": APR, "min_rate": 0.05, "min_floor": 0.1}}
m, intr, path = run(lambda b: max(0.05 * b, 0.1))
res["min_only"] = {"months": m, "interest": round(intr, 2), "balance": pad(path), "first_interest": round(DEBT * r, 3), "first_pay": round(max(0.05 * DEBT * (1 + r), 0.1), 3)}
m2, intr2, path2 = run(lambda b: 2.0)
res["fixed_2m"] = {"months": m2, "interest": round(intr2, 2), "balance": pad(path2)}
m3, intr3, _ = run(lambda b: 1.0)
res["fixed_1m"] = {"months": m3, "interest": round(intr3, 2)}
g = (8830 / 8.55) ** (1 / 132) - 1
res["reverse_8_8"] = {"monthly": round(g * 100, 2), "yearly_mult": round((1 + g) ** 12, 2), "total_mult": round(8830 / 8.55)}
res["rule72"] = {"6": 72 / 6, "30": 72 / 30}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: (v if "balance" not in v else {a: b for a, b in v.items() if a != "balance"}) for k, v in res.items()})
