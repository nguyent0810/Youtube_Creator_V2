"""D2 "FOMO" — kênh tự tính trên VN-Index (data/ck/vnindex_1d.csv, vnstock/VCI, 08/10/2018 → 06/10/2026).

    python data/long/ck-d2-fomo/analysis.py            # in bảng + ghi results.json cạnh file này

1. Chu kỳ 2020–2022: đáy 03/2020, đỉnh 01/2022, đáy sau đỉnh, ngày đầu tiên đóng cửa vượt lại đỉnh.
2. Người vào tháng kỷ lục mở tài khoản (03/2022, VSD): mức chỉ số cuối tháng, mức thấp nhất sau đó.
3. "Sau một năm tăng mạnh": chia mọi phiên theo mức tăng 12 tháng trước đó (250 phiên), xem 12 tháng sau.
   CẢNH BÁO PHƯƠNG PHÁP: cửa sổ chồng lấn — nhóm "> +40%" gần như chỉ là MỘT giai đoạn (03/2021 → 02/2022).
   Lời đọc phải nói rõ "một lần trong tám năm", không được trình bày như quy luật.
Chỉ là đo quá khứ trên chỉ số (không mua bán trực tiếp được), không tính phí/thuế/cổ tức. Không phải dự báo.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
N = 250   # ~12 tháng giao dịch

c = [(r["time"], float(r["close"])) for r in csv.DictReader(open(ROOT / "data" / "ck" / "vnindex_1d.csv", encoding="utf-8"))]
d = [x[0] for x in c]
v = [x[1] for x in c]


def at(day):
    return [x for x in c if x[0] <= day][-1]


def first_at_or_above(after, level):
    return next((x for x in c if x[0] > after and x[1] >= level), None)


res = {}
seg = [x for x in c if "2020-03-01" <= x[0] <= "2023-01-01"]
low20 = min((x for x in seg if x[0] < "2020-12-31"), key=lambda x: x[1])
peak = max(seg, key=lambda x: x[1])
trough = min((x for x in seg if x[0] > peak[0]), key=lambda x: x[1])
res["cycle"] = {"low2020": low20, "peak": peak, "trough": trough,
                "up_pct": round((peak[1] / low20[1] - 1) * 100, 1), "down_pct": round((trough[1] / peak[1] - 1) * 100, 1),
                "recover_peak": first_at_or_above(peak[0], peak[1])}
m = at("2022-03-31")
res["mar2022"] = {"close": m, "low_after": trough, "drop_pct": round((trough[1] / m[1] - 1) * 100, 1)}
buckets = {}
for i in range(N, len(c) - N):
    tr, fw = v[i] / v[i - N] - 1, v[i + N] / v[i] - 1
    b = ">40" if tr > 0.4 else "20-40" if tr > 0.2 else "0-20" if tr > 0 else "<0"
    buckets.setdefault(b, []).append((d[i], fw))
res["after_12m"] = {}
for b, xs in buckets.items():
    fws = sorted(f for _, f in xs)
    res["after_12m"][b] = {"days": len(xs), "first": xs[0][0], "last": xs[-1][0],
                           "median_fwd_pct": round(fws[len(fws) // 2] * 100, 1),
                           "share_neg_pct": round(sum(f < 0 for f in fws) / len(fws) * 100)}
lo25 = min((x for x in c if "2025-01-01" <= x[0] <= "2025-12-31"), key=lambda x: x[1])
hi26 = max((x for x in c if x[0] > lo25[0]), key=lambda x: x[1])
res["run2025"] = {"low": lo25, "high": hi26, "up_pct": round((hi26[1] / lo25[1] - 1) * 100), "last": c[-1],
                  "from_high_pct": round((c[-1][1] / hi26[1] - 1) * 100, 1)}

if __name__ == "__main__":
    print(json.dumps(res, ensure_ascii=False, indent=1))
    (HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
