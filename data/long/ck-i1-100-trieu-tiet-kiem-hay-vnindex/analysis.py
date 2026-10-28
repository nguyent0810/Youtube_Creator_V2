"""Backtest minh hoa: 100 trieu, chi so gia VN-Index, 09/04/2018–06/10/2026.

Du lieu: hai CSV ticket cap. Gia tri B/C la VI DU GIA DINH, da ap phi giao dich
0,15% luc mua va ban, va thue chuyen nhuong 0,1% luc ban. Khong co chuoi lai
suat binh quan nam da duoc kiem chung -> A (tiet kiem) dung 3 kich ban lai CO DINH 5/6/7%/nam
(khoang cac moc quan sat trong facts.md: 6,55% dau 2018 ... 4,9% 01/2024), ky han 12 thang cuon moi nam,
nam le tinh theo ti le ngay (Claude chot 27/10/2026, W1-6b). Day la VI DU GIA DINH, khong phai lai cua ngan hang nao.
"""
import csv
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INITIAL = 100_000_000
FEE = 0.0015
TAX = 0.001
START = date(2018, 4, 9)
END = date(2026, 10, 6)

def load(path):
    with path.open(encoding="utf-8", newline="") as f:
        return [(date.fromisoformat(r["time"]), float(r["close"])) for r in csv.DictReader(f)]

rows = sorted(load(ROOT / "data" / "ck" / "vnindex_1d_2016_2018.csv") + load(ROOT / "data" / "ck" / "vnindex_1d.csv"))
prices = {d: p for d, p in rows}
window = [(d, p) for d, p in rows if START <= d <= END]
assert prices[START] == 1204.33 and prices[END] == 1759.08

# B: mua mot lan. Phi mua lam giam so don vi; khi ban tru phi va thue.
b_units = INITIAL * (1 - FEE) / prices[START]
def b_value(p): return b_units * p * (1 - FEE - TAX)

# C: 24 lenh, phien dau tien moi thang 04/2018–03/2020.
months = {(d.year, d.month) for d, _ in window}
buy_dates = []
for y, m in [(2018, m) for m in range(4, 13)] + [(2019, m) for m in range(1, 13)] + [(2020, m) for m in range(1, 4)]:
    buy_dates.append(next(d for d, _ in window if (d.year, d.month) == (y, m)))
assert len(buy_dates) == 24 and all((d.year, d.month) in months for d in buy_dates)
piece = INITIAL / 24
c_units = sum(piece * (1 - FEE) / prices[d] for d in buy_dates)
def n_bought(d): return sum(1 for b in buy_dates if b <= d)
def c_units_upto(d): return sum(piece * (1 - FEE) / prices[b] for b in buy_dates if b <= d)   # phan chua mua giu tien mat (khong lai)
def c_value(p): return c_units * p * (1 - FEE - TAX)

def at(d): return prices[date.fromisoformat(d)]
def money(x): return round(x / 1_000_000, 2)

b_series = [(d, b_value(p)) for d, p in window]
c_after = [(d, c_value(p)) for d, p in window if d >= buy_dates[-1]]
b_low_d, b_low = min(b_series, key=lambda x: x[1])
c_low_d, c_low = min(c_after, key=lambda x: x[1])
def recover(series, start):
    return next(d for d, v in series if d >= start and v >= INITIAL)

points = ["2018-04-09", "2020-03-24", "2021-12-31", "2022-01-06", "2022-11-15", "2025-04-09", "2026-10-06"]
race = [{"date": d, "mot_lan": money(b_value(at(d))), "mua_deu": money(c_value(at(d))) if date.fromisoformat(d) >= buy_dates[-1] else None} for d in points]
# A: tiet kiem 12 thang cuon moi nam, lai co dinh r; phan nam le tinh lai don theo ngay
def a_value(d, r):
    yrs = (d - START).days / 365.0
    full = int(yrs)
    return INITIAL * (1 + r) ** full * (1 + r * (yrs - full))
RATES = {"tiet_kiem_5": 0.05, "tiet_kiem_6": 0.06, "tiet_kiem_7": 0.07}
# chuoi cuoi moi thang (phien cuoi cua thang) cho canh race
last = {}
for d, p in window:
    last[(d.year, d.month)] = (d, p)
month_pts = [last[k] for k in sorted(last)]
monthly = {"dates": [f"{d.month:02d}/{d.year}" for d, _ in month_pts], "iso": [d.isoformat() for d, _ in month_pts],
           "mot_lan": [money(b_value(p)) for _, p in month_pts],
           "mua_deu": [money(c_units_upto(d) * p * (1 - FEE - TAX) + piece * (24 - n_bought(d))) for d, p in month_pts]}
for k, r in RATES.items():
    monthly[k] = [money(a_value(d, r)) for d, _ in month_pts]
res = {
  "assumptions": {"initial_million": 100, "purchase_fee_pct": 0.15, "sale_fee_pct": 0.15, "sale_tax_pct": 0.1,
                  "savings": "3 kich ban lai co dinh 5/6/7%/nam, ky han 12 thang cuon moi nam (VI DU GIA DINH, trong khoang lai da quan sat)",
                  "mua_deu_cash": "phan chua mua giu tien mat, khong lai"},
  "race": race,
  "mot_lan": {"end_million": money(b_value(prices[END])), "low_date": b_low_d.isoformat(), "low_million": money(b_low),
              "low_pct": round((b_low / INITIAL - 1) * 100, 2), "recover_date": recover(b_series, START).isoformat()},
  "mua_deu": {"instalments": 24, "piece_million": round(piece / 1e6, 4), "end_million": money(c_value(prices[END])),
              "low_after_full_date": c_low_d.isoformat(), "low_after_full_million": money(c_low),
              "low_after_full_pct": round((c_low / INITIAL - 1) * 100, 2), "recover_after_full_date": recover(c_after, buy_dates[-1]).isoformat()},
}
res["tiet_kiem"] = {k: {"rate_pct": r * 100, "end_million": money(a_value(END, r))} for k, r in RATES.items()}
res["monthly"] = monthly
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "monthly"}, ensure_ascii=False, indent=2)); print("monthly points:", len(monthly["dates"]))
