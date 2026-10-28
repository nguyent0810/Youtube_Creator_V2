"""E5 "Thuế thu nhập cá nhân 2026" — phép tính thuế tiền lương hằng tháng (người cư trú, hợp đồng ≥ 3 tháng) theo hai bộ luật.

    python data/long/ck-e5-thue-tncn-2026/analysis.py      # in kết quả + ghi results.json

Luật (nguồn trong factcheck.md):
- 2026 (kỳ tính thuế 2026): giảm trừ bản thân 15,5 tr, mỗi người phụ thuộc 6,2 tr (NQ 110/2025/UBTVQH15); biểu 5 bậc/tháng
  10/30/60/100 tr: 5/10/20/30/35% (Luật Thuế TNCN 109/2025/QH15).
- 2020–2025: giảm trừ 11 / 4,4 tr (NQ 954/2020/UBTVQH14, từ 01/07/2020); 2013–06/2020: 9 / 3,6 tr. Biểu 7 bậc 5/10/18/32/52/80 tr:
  5/10/15/20/25/30/35%.
- Bảo hiểm bắt buộc người lao động trừ trước thuế: BHXH 8% + BHYT 1,5% + BHTN 1% = 10,5% lương đóng (giả định lương đóng = lương gộp).
  Trần BHXH/BHYT = 20 × lương cơ sở (2,53 tr từ 01/07/2026 -> 50,6 tr; 2,34 tr trước đó -> 46,8 tr); trần BHTN = 20 × lương tối thiểu vùng I
  (5,31 tr năm 2026 -> 106,2 tr). Ở mức lương ≤ 46,8 tr trần không chạm -> không ảnh hưởng ví dụ chính.
Ví dụ (anh Khang, nhân vật giả định): lương gộp 25 tr/tháng, một con là người phụ thuộc. Không phụ cấp miễn thuế, không từ thiện.
Kiểm độc lập: check.py.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEW = [(10, .05), (30, .10), (60, .20), (100, .30), (float("inf"), .35)]
OLD = [(5, .05), (10, .10), (18, .15), (32, .20), (52, .25), (80, .30), (float("inf"), .35)]
DED = {"2019": (9.0, 3.6), "2025": (11.0, 4.4), "2026": (15.5, 6.2)}


def progressive(ti, table):
    tax, lo = 0.0, 0.0
    for hi, r in table:
        if ti > lo:
            tax += (min(ti, hi) - lo) * r
        lo = hi
    return tax


def insurance(gross, base_cap=50.6, ui_cap=106.2):
    return 0.095 * min(gross, base_cap) + 0.01 * min(gross, ui_cap)


def monthly_tax(gross, deps, year="2026", ins=None):
    own, dep = DED[year]
    ins = insurance(gross) if ins is None else ins
    ti = max(0.0, gross - ins - own - dep * deps)
    return progressive(ti, NEW if year == "2026" else OLD), ti


res = {}
# ví dụ anh Khang: 25 tr, 1 người phụ thuộc
k = {}
for y in ("2019", "2025", "2026"):
    t, ti = monthly_tax(25, 1, y, ins=0.105 * 25)
    k[y] = {"taxable": round(ti, 4), "tax": round(t, 5)}
k["save_month"] = round(k["2025"]["tax"] - k["2026"]["tax"], 5)
k["save_year"] = round(12 * k["save_month"], 3)
k["insurance"] = round(0.105 * 25, 4)
res["khang"] = k
# ngưỡng lương gộp bắt đầu phải nộp (2026): giảm trừ / (1 − 10,5%)
res["threshold_gross_2026"] = {d: round((15.5 + 6.2 * d) / 0.895, 2) for d in (0, 1, 2)}
res["threshold_gross_2025"] = {d: round((11 + 4.4 * d) / 0.895, 2) for d in (0, 1, 2)}
# bảng tra 2026 (thuế/tháng, nghìn đồng) và 2025 để so
GROSS = [15, 20, 25, 30, 40, 50, 70, 100]
table = {}
for g in GROSS:
    row = {}
    for d in (0, 1, 2):
        t26, _ = monthly_tax(g, d, "2026")
        t25, _ = monthly_tax(g, d, "2025", ins=0.095 * min(g, 46.8) + 0.01 * min(g, 99.2))
        row[str(d)] = {"2026": round(1000 * t26), "2025": round(1000 * t25)}
    table[str(g)] = row
res["table_k_vnd"] = table
# cùng thu nhập tính thuế 20 tr/tháng: biểu cũ vs biểu mới
res["ti20"] = {"old": round(progressive(20, OLD), 3), "new": round(progressive(20, NEW), 3)}
# thưởng Tết 50 tr trả trong một tháng: khấu trừ theo tháng vs quyết toán năm (anh Khang)
BONUS = 50.0
ins_m = 0.105 * 25
wh_bonus, _ = monthly_tax(25 + BONUS, 1, "2026", ins=ins_m)
wh_norm, _ = monthly_tax(25, 1, "2026", ins=ins_m)
withheld = wh_bonus + 11 * wh_norm
annual_ti = 12 * 25 + BONUS - 12 * ins_m - 12 * (15.5 + 6.2)
annual_tax = progressive(annual_ti / 12, NEW) * 12             # biểu năm = biểu tháng × 12
res["bonus"] = {"bonus": BONUS, "withheld_bonus_month": round(wh_bonus, 4), "withheld_year": round(withheld, 4),
                "annual_taxable": round(annual_ti, 3), "annual_tax": round(annual_tax, 4), "refund": round(withheld - annual_tax, 4)}
# lương 50 tr, 2 con: biểu cũ (giảm trừ cũ) vs mới
t50o, _ = monthly_tax(50, 2, "2025", ins=0.095 * 46.8 + 0.01 * 50)
t50n, _ = monthly_tax(50, 2, "2026")
res["g50d2"] = {"2025": round(t50o, 4), "2026": round(t50n, 4), "save_year": round(12 * (t50o - t50n), 3)}
# giảm trừ bản thân các thời kỳ quy về giá 2026 (CPI bình quân năm World Bank WDI; 2026 = 2025 × (1 + 4,52%) GIẢ ĐỊNH theo CPI bình quân 9 tháng)
cpi = {int(x["date"]): x["value"] for x in json.loads((HERE / "wb_cpi_index.json").read_text(encoding="utf-8"))[1] if x["value"]}
cpi[2026] = cpi[2025] * 1.0452
res["ded_real_2026"] = {"9_2013": round(9 * cpi[2026] / cpi[2013], 2), "11_2020": round(11 * cpi[2026] / cpi[2020], 2), "15.5_2026": 15.5}
res["cpi_2013_2020_pct"] = round(100 * (cpi[2020] / cpi[2013] - 1), 1)
# thuế suất "bậc cao nhất chạm tới" và tỷ lệ thuế thật trên lương gộp: 50 tr, 0 NPT
t50, ti50 = monthly_tax(50, 0, "2026")
res["g50d0"] = {"tax": round(t50, 4), "taxable": round(ti50, 3), "marginal": 0.10, "effective_pct": round(100 * t50 / 50, 2)}
# nếu con được đăng ký giảm trừ cho người KHÔNG phải nộp thuế (vợ anh Khang, giả định lương 15 tr): anh Khang mất phần 6,2 tr
t_nodep, _ = monthly_tax(25, 0, "2026", ins=0.105 * 25)
res["khang_no_dep"] = {"tax": round(t_nodep, 5), "diff_month": round(t_nodep - k["2026"]["tax"], 5), "diff_year": round(12 * (t_nodep - k["2026"]["tax"]), 3)}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "table_k_vnd"}, ensure_ascii=False, indent=1))
for g in GROSS:
    print(g, [(table[str(g)][str(d)]["2025"], table[str(g)][str(d)]["2026"]) for d in (0, 1, 2)])
