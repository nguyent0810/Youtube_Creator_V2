"""B2 "Lãi kép" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH) + hai con số thật của 8 năm qua.

    python data/long/ck-b2-lai-kep/analysis.py      # in bảng + ghi results.json

Giả định ví dụ: lãi 6%/năm, nhập gốc hằng tháng (0,5%/tháng), nộp cuối mỗi tháng, lãi suất KHÔNG ĐỔI, không rút. Đây là phép tính,
không phải mức lãi của sản phẩm nào và không phải dự báo. Lạm phát ví dụ 3,1%/năm = trung bình cộng CPI bình quân năm 2018–2025
(3,54 · 2,79 · 3,23 · 1,84 · 3,15 · 3,25 · 3,63 · 3,31; hồ sơ A1 mục 6.3). Số thật: sổ 12 tháng nhóm ngân hàng lớn cuộn 10/2018 → 10/2026
= ×1,56; CPI cùng kỳ ≈ +29% (hồ sơ A1 mục 7.1).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R, M = 0.06, 3.0
m = R / 12
res = {"assume": {"rate": R, "monthly": M}}


def fv(months, pay=M, start=0.0, rate=m):
    v = start
    for _ in range(months):
        v = v * (1 + rate) + pay
    return v


# 1. 100 triệu để yên: lãi đơn vs lãi kép (ghép năm cho dễ nói)
res["simple_vs_compound"] = [{"year": y, "simple": round(100 * (1 + R * y), 1), "compound": round(100 * (1 + R) ** y, 1)} for y in (1, 2, 10, 20, 30)]
res["year2_interest"] = round(100 * (1 + R) * R, 2)
# 2. nộp 3 triệu/tháng
rows = []
for y in (10, 20, 30):
    v = fv(12 * y)
    rows.append({"years": y, "paid": M * 12 * y, "value": round(v, 1), "interest": round(v - M * 12 * y, 1), "interest_share_pct": round((1 - M * 12 * y / v) * 100, 1)})
res["monthly"] = rows
# năm đầu tiên mà tiền lãi sinh ra trong năm vượt tiền nộp trong năm (36 triệu)
v, cross = 0.0, None
yearly = []
for y in range(1, 31):
    start = v
    v = fv(12, start=start)
    interest = v - start - M * 12
    yearly.append({"year": y, "value": round(v, 1), "interest_in_year": round(interest, 1)})
    if cross is None and interest > M * 12:
        cross = y
res["cross_year"] = cross
res["yearly"] = yearly
# 3. Lan (nộp 10 năm đầu rồi để yên 20 năm) vs Minh (bắt đầu muộn 10 năm, nộp 20 năm)
lan10 = fv(120)
lan = fv(240, pay=0.0, start=lan10)
minh = fv(240)
res["lan_minh"] = {"lan_paid": M * 120, "lan_at10": round(lan10, 1), "lan_final": round(lan, 1), "minh_paid": M * 240, "minh_final": round(minh, 1),
                   "minh_needs_monthly_to_match": round(lan / (fv(240, pay=1.0)), 2)}
# 4. quy tắc 72
import math
res["rule72"] = {"at6_exact_years": round(math.log(2) / math.log(1 + R), 1), "rule": 72 / 6,
                 "inflation_3_1_halves_years": round(math.log(2) / math.log(1.031), 1)}
# 5. lạm phát
cpi = [3.54, 2.79, 3.23, 1.84, 3.15, 3.25, 3.63, 3.31]
avg = sum(cpi) / len(cpi)
cum = 1.0
for c in cpi:
    cum *= 1 + c / 100
res["inflation"] = {"avg_pct": round(avg, 2), "cum_2018_2025_pct": round((cum - 1) * 100, 1),
                    "real_value_30y": round(rows[2]["value"] / (1.031 ** 30), 1), "real_value_20y": round(rows[1]["value"] / (1.031 ** 20), 1),
                    "paid_real_note": "so với sức mua hôm nay", "actual_8y_nominal_x": 1.56, "actual_8y_cpi_pct": 29, "actual_8y_real_x": round(1.56 / 1.29, 2)}
# 6. lãi kép chạy ngược: khoản nợ 30 triệu, 25%/năm, không trả (ghép tháng)
debt = [{"year": y, "value": round(30 * (1 + 0.25 / 12) ** (12 * y), 1)} for y in (1, 2, 3, 5)]
res["debt"] = debt
# 7. độ nhạy lãi suất: 3 triệu/tháng, 30 năm
res["sens_rate"] = [{"rate": r, "value": round(fv(360, rate=r / 12), 1)} for r in (0.04, 0.05, 0.06, 0.07, 0.08)]
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "yearly"}, ensure_ascii=False, indent=1))
