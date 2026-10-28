"""Kiem doc lap results.json bang cach tinh lai truc tiep tu CSV."""
import csv, json
from datetime import date
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[2]
def read(p):
    with p.open(encoding="utf-8", newline="") as f:
        return {date.fromisoformat(r["time"]): float(r["close"]) for r in csv.DictReader(f)}
p = read(ROOT / "data" / "ck" / "vnindex_1d_2016_2018.csv") | read(ROOT / "data" / "ck" / "vnindex_1d.csv")
r = json.loads((H / "results.json").read_text(encoding="utf-8"))
start, end, fee, tax = date(2018,4,9), date(2026,10,6), .0015, .001
units = 100_000_000 * (1-fee) / p[start]
end_b = round(units * p[end] * (1-fee-tax) / 1e6, 2)
dates = []
for y, ms in ((2018, range(4,13)), (2019, range(1,13)), (2020, range(1,4))):
    for m in ms: dates.append(min(d for d in p if d >= start and d.year == y and d.month == m))
units_c = sum((100_000_000/24)*(1-fee)/p[d] for d in dates)
end_c = round(units_c*p[end]*(1-fee-tax)/1e6, 2)
ok = [p[start] == 1204.33, p[end] == 1759.08, len(dates) == 24, r["mot_lan"]["end_million"] == end_b,
      r["mua_deu"]["end_million"] == end_c]
# tiet kiem: cong lai tung nam bang vong lap theo ngay ky han (cach khac voi cong thuc mu trong analysis.py)
for k, rate in (("tiet_kiem_5", .05), ("tiet_kiem_6", .06), ("tiet_kiem_7", .07)):
    bal, t = 100_000_000, start
    while date(t.year + 1, t.month, t.day) <= end:
        bal *= 1 + rate; t = date(t.year + 1, t.month, t.day)
    bal *= 1 + rate * (end - t).days / 365
    ok.append(abs(r["tiet_kiem"][k]["end_million"] - bal / 1e6) < 0.6)   # analysis dung 365 ngay/nam, vong lap dung ngay ky han that
m = r["monthly"]
ok += [len(m["dates"]) == len(m["mot_lan"]) == len(m["mua_deu"]) == len(m["tiet_kiem_6"]), m["mua_deu"][0] == 100.0 or m["mua_deu"][0] < 100.5]
print("I1 check:", "OK" if all(ok) else f"LOI o {[i for i, x in enumerate(ok) if not x]}", f"({len(ok)} phep)")
assert all(ok)
