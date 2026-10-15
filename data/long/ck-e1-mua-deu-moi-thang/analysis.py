"""E1 "Mua đều mỗi tháng" — kênh tự tính trên VN-Index (data/ck/vnindex_1d.csv, vnstock/VCI, 08/10/2018 → 06/10/2026).

    python data/long/ck-e1-mua-deu-moi-thang/analysis.py      # in bảng + ghi results.json cạnh file này

Giả định CHUNG (ghi trên màn hình): "mua theo chỉ số" là MINH HOẠ (không mua trực tiếp được chỉ số), giá đóng cửa, KHÔNG phí,
thuế, cổ tức, trượt giá; tiền chưa mua nằm yên lãi 0. MỘT chỉ số, MỘT giai đoạn -> minh hoạ cơ chế, không phải bằng chứng.

1. DCA: mỗi tháng 3 triệu, mua ở phiên đầu tiên của tháng (từ 10/2018). Giá trị cuối kỳ, tổng nộp, giá vốn bình quân.
2. Dồn một lần: toàn bộ số tiền ấy mua ngay phiên đầu.
3. "Xui nhất": mỗi năm gom 12 tháng tiền, mua đúng ngày đóng cửa CAO nhất năm đó. "May nhất": đúng ngày THẤP nhất.
4. Đường đi của tài khoản DCA: những lúc giá trị thấp hơn tổng tiền đã nộp (âm bao nhiêu %, kéo dài bao lâu).
5. Cơ chế: cùng 3 triệu mua được bao nhiêu "đơn vị chỉ số" ở tháng đắt nhất / rẻ nhất; trung bình cộng giá vs giá vốn bình quân.
"""
import csv
import json
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
rows = [(r["time"], float(r["close"])) for r in csv.DictReader(open(ROOT / "data" / "ck" / "vnindex_1d.csv", encoding="utf-8"))]
d = [x[0] for x in rows]
v = [x[1] for x in rows]
M = 3.0                                   # triệu đồng mỗi tháng
first = OrderedDict()                     # phiên đầu tiên của mỗi tháng
for i, day in enumerate(d):
    first.setdefault(day[:7], i)
buys = list(first.values())
N = len(buys)
last = len(v) - 1
res = {"period": {"from": d[0], "to": d[last], "months": N, "per_month": M, "paid": M * N, "start": v[0], "end": v[last],
                  "index_change_pct": round((v[last] / v[0] - 1) * 100, 1)}}

# 1. DCA
units = sum(M / v[i] for i in buys)
val = units * v[last]
res["dca"] = {"value": round(val, 1), "gain": round(val - M * N, 1), "gain_pct": round((val / (M * N) - 1) * 100, 1),
              "avg_cost": round(M * N / units, 2), "avg_price": round(sum(v[i] for i in buys) / N, 2)}
# 2. dồn một lần
lump = M * N / v[0] * v[last]
res["lump"] = {"value": round(lump, 1), "gain_pct": round((lump / (M * N) - 1) * 100, 1)}
# 3. xui nhất / may nhất theo từng năm lịch (tiền của năm đó = 3 triệu x số tháng có trong dữ liệu của năm)
years = OrderedDict()
for m, i in first.items():
    years.setdefault(m[:4], []).append(i)
out = {"worst": 0.0, "best": 0.0}
detail = []
for y, idx in years.items():
    money = M * len(idx)
    ys = [i for i, day in enumerate(d) if day[:4] == y]
    hi = max(ys, key=lambda i: v[i])
    lo = min(ys, key=lambda i: v[i])
    out["worst"] += money / v[hi]
    out["best"] += money / v[lo]
    detail.append({"year": y, "money": money, "high": {"date": d[hi], "close": v[hi]}, "low": {"date": d[lo], "close": v[lo]}})
res["worst"] = {"value": round(out["worst"] * v[last], 1), "gain_pct": round((out["worst"] * v[last] / (M * N) - 1) * 100, 1)}
res["best"] = {"value": round(out["best"] * v[last], 1), "gain_pct": round((out["best"] * v[last] / (M * N) - 1) * 100, 1)}
res["years"] = detail
# 4. đường đi tài khoản DCA (theo ngày)
u, paid, path, k = 0.0, 0.0, [], 0
under = []                                 # các đoạn giá trị < tiền đã nộp
for i in range(len(v)):
    if k < N and buys[k] == i:
        u += M / v[i]
        paid += M
        k += 1
    path.append((d[i], round(paid, 1), round(u * v[i], 2)))
worst_i = min(range(len(path)), key=lambda i: path[i][2] / path[i][1] - 1)
res["deepest"] = {"date": path[worst_i][0], "paid": path[worst_i][1], "value": round(path[worst_i][2], 1),
                  "pct": round((path[worst_i][2] / path[worst_i][1] - 1) * 100, 1)}
days_under = sum(1 for _, p, val_ in path if val_ < p)
res["under"] = {"days": days_under, "share_pct": round(days_under / len(path) * 100, 1)}
seg, cur = [], None
for day, p, val_ in path:
    if val_ < p:
        cur = cur or {"from": day, "min_pct": 0.0, "n": 0}
        cur["to"], cur["n"] = day, cur["n"] + 1
        cur["min_pct"] = min(cur["min_pct"], round((val_ / p - 1) * 100, 1))
    elif cur:
        seg.append(cur); cur = None
if cur:
    seg.append(cur)
res["under_segments"] = sorted(seg, key=lambda s: -s["n"])[:5]
for tag, day in (("covid", "2020-03-24"), ("nov2022", "2022-11-15"), ("peak2022", "2022-01-06")):
    i = d.index(day)
    res[tag] = {"date": day, "close": v[i], "paid": path[i][1], "value": round(path[i][2], 1), "pct": round((path[i][2] / path[i][1] - 1) * 100, 1)}
res["path_monthly"] = [{"m": m, "paid": path[i][1], "value": round(path[i][2], 1)} for m, i in first.items()]
# 5. cơ chế: tháng đắt nhất / rẻ nhất
hi = max(buys, key=lambda i: v[i]); lo = min(buys, key=lambda i: v[i])
res["mechanism"] = {"dear": {"date": d[hi], "close": v[hi], "units_x1000": round(M / v[hi] * 1000, 3)},
                    "cheap": {"date": d[lo], "close": v[lo], "units_x1000": round(M / v[lo] * 1000, 3)},
                    "ratio": round(v[hi] / v[lo], 2)}
# 6. độ nhạy: đổi ngày mua trong tháng (phiên thứ 1, 6, 11, 16) và đổi tháng bắt đầu (lệch 0..11 tháng) -> kết quả đổi bao nhiêu
sens = []
for off in (0, 5, 10, 15):
    bb = []
    for m in first:
        ys = [i for i, day in enumerate(d) if day[:7] == m]
        bb.append(ys[min(off, len(ys) - 1)])
    uu = sum(M / v[i] for i in bb)
    sens.append({"session": off + 1, "gain_pct": round((uu * v[last] / (M * N) - 1) * 100, 1)})
res["sens_day"] = sens
starts = []
for s in range(0, 61, 12):
    bb = buys[s:]
    uu = sum(M / v[i] for i in bb)
    starts.append({"start": d[bb[0]][:7], "months": len(bb), "gain_pct": round((uu * v[last] / (M * len(bb)) - 1) * 100, 1),
                   "lump_pct": round((v[last] / v[bb[0]] - 1) * 100, 1)})
res["sens_start"] = starts
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
show = {k: res[k] for k in res if k not in ("path_monthly", "years")}
print(json.dumps(show, ensure_ascii=False, indent=1))
