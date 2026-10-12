"""C4 "Đường trung bình động (MA)" — kênh tự tính trên VN-Index (data/ck/vnindex_1d.csv, vnstock/VCI, 08/10/2018 → 06/10/2026).

    python data/long/ck-c4-duong-trung-binh/analysis.py      # in bảng + ghi results.json cạnh file này

1. Ví dụ cửa sổ trượt: 5 phiên đầu 01/2022 (quanh đỉnh 06/01/2022) -> MA5 tính tay.
2. Độ trễ ở đỉnh 06/01/2022 và đáy 15/11/2022: giá đóng cửa cắt xuống/lên MA20, MA50, MA200 sau bao nhiêu phiên, ở mức nào,
   cách đỉnh/đáy bao nhiêu %.
3. Quy tắc minh hoạ "đóng cửa trên MA200 thì giữ chỉ số, dưới thì đứng ngoài (tiền nằm yên, lãi 0)", quyết định theo giá đóng
   cửa hôm trước, KHÔNG phí/thuế/cổ tức, so với giữ suốt. Đếm số lần đổi trạng thái và số lần "cắt giả" (đổi lại trong <= 10 phiên).
   CẢNH BÁO: MỘT chỉ số, MỘT giai đoạn, MỘT quy tắc chọn sẵn -> minh hoạ cơ chế trễ/cắt giả, KHÔNG phải bằng chứng quy tắc tốt/xấu.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
rows = [(r["time"], float(r["close"])) for r in csv.DictReader(open(ROOT / "data" / "ck" / "vnindex_1d.csv", encoding="utf-8"))]
d = [x[0] for x in rows]
v = [x[1] for x in rows]


def sma(n):
    out, s = [None] * len(v), 0.0
    for i, x in enumerate(v):
        s += x
        if i >= n:
            s -= v[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


MA = {n: sma(n) for n in (5, 20, 50, 200)}
res = {}

i0 = d.index("2021-12-30")
res["window5"] = [{"date": d[i], "close": v[i], "ma5": round(MA[5][i], 2)} for i in range(i0, i0 + 6)]


def cross(after, n, down=True):
    i = d.index(after)
    for j in range(i + 1, len(v)):
        if MA[n][j] is not None and ((v[j] < MA[n][j]) if down else (v[j] > MA[n][j])):
            return {"date": d[j], "sessions": j - i, "close": v[j], "ma": round(MA[n][j], 2), "from_extreme_pct": round((v[j] / v[i] - 1) * 100, 1)}


res["peak2022"] = {"date": "2022-01-06", "close": v[d.index("2022-01-06")], **{f"ma{n}": cross("2022-01-06", n, True) for n in (20, 50, 200)}}
res["trough2022"] = {"date": "2022-11-15", "close": v[d.index("2022-11-15")], **{f"ma{n}": cross("2022-11-15", n, False) for n in (20, 50, 200)}}

start = 199 + 1          # phiên đầu có MA200 hôm trước
eq_rule, eq_hold, state, flips, fakes, last_flip = 1.0, 1.0, None, 0, 0, None
flip_days = []
for i in range(start, len(v)):
    r = v[i] / v[i - 1]
    eq_hold *= r
    inside = v[i - 1] > MA[200][i - 1]          # quyết định theo đóng cửa HÔM TRƯỚC (không nhìn trước)
    if inside:
        eq_rule *= r
    if state is not None and inside != state:
        flips += 1
        if last_flip is not None and i - last_flip <= 10:
            fakes += 1
        last_flip = i
        flip_days.append(d[i])
    state = inside
res["rule_ma200"] = {"from": d[start], "to": d[-1], "hold_pct": round((eq_hold - 1) * 100, 1), "rule_pct": round((eq_rule - 1) * 100, 1),
                     "flips": flips, "fake_flips_le10": fakes, "days_inside_pct": round(100 * sum(v[i - 1] > MA[200][i - 1] for i in range(start, len(v))) / (len(v) - start)),
                     "first_flips": flip_days[:6]}


def rule(n, fee=0.0, tax=0.0, start_i=start):
    """Như trên với MA n; mỗi lần vào trừ fee, mỗi lần ra trừ fee + tax (giả định minh hoạ)."""
    m = MA[n] if n in MA else sma(n)
    eq, st = 1.0, False
    for i in range(start_i, len(v)):
        inside = m[i - 1] is not None and v[i - 1] > m[i - 1]
        if inside != st:
            eq *= (1 - fee) if inside else (1 - fee - tax)
            st = inside
        if inside:
            eq *= v[i] / v[i - 1]
    return round((eq - 1) * 100, 1)


# Phí giả định 0,15%/chiều + thuế bán 0,1% (luật thuế TNCN); cùng giai đoạn cho mọi n (bắt đầu khi MA250 đã có)
S250 = 250
res["sensitivity"] = {"from": d[S250], "hold_pct": round((v[-1] / v[S250 - 1] - 1) * 100, 1),
                      **{f"ma{n}": {"no_cost": rule(n, start_i=S250), "with_cost": rule(n, 0.0015, 0.001, S250)} for n in (20, 50, 100, 150, 200, 250)}}
res["latest"] = {"date": d[-1], "close": v[-1], **{f"ma{n}": round(MA[n][-1], 2) for n in (20, 50, 200)}}

if __name__ == "__main__":
    print(json.dumps(res, ensure_ascii=False, indent=1))
    (HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
