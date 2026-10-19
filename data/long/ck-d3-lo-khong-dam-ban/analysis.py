"""D3 "Lỗ rồi càng không dám bán" — phép tính minh hoạ (kênh tự tính).

    python data/long/ck-d3-lo-khong-dam-ban/analysis.py      # in bảng + ghi results.json

Số thật: VN-Index đóng cửa (data/ck/vnindex_1d.csv, cùng nguồn video D2): đỉnh 06/01/2022, đáy 15/11/2022, ngày đầu vượt lại đỉnh.
Toán: lỗ x% thì cần lãi x/(1−x) để về lại điểm cũ. Ví dụ giả định "hai cổ phiếu": 50 triệu mỗi mã, A +20%, B −20%, cần rút 50 triệu.
"""
import csv
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
rows = [(r["time"], float(r["close"])) for r in csv.DictReader(open(ROOT / "data/ck/vnindex_1d.csv", encoding="utf-8"))]
peak = max((r for r in rows if "2021-06-01" <= r[0] <= "2022-06-30"), key=lambda r: r[1])
trough = min((r for r in rows if peak[0] < r[0] <= "2023-06-30"), key=lambda r: r[1])
back = next(r for r in rows if r[0] > trough[0] and r[1] >= peak[1])
d = lambda s: date.fromisoformat(s)
need = lambda x: x / (1 - x)
res = {"vnindex": {"peak": peak, "trough": trough, "drop_pct": round((trough[1] / peak[1] - 1) * 100, 1),
                   "need_from_trough_pct": round((peak[1] / trough[1] - 1) * 100, 1), "back": back,
                   "months_peak_to_back": round((d(back[0]) - d(peak[0])).days / 30.44, 1), "months_trough_to_back": round((d(back[0]) - d(trough[0])).days / 30.44, 1)},
       "recovery_math": {f"-{int(x * 100)}%": round(need(x) * 100, 1) for x in (0.1, 0.2, 0.3, 0.4, 0.5)},
       "two_stocks": {"A_value": 60, "B_value": 40, "sell_A_left": {"A": 10, "B": 40}, "sell_B_left": {"A": 60, "B": 0},
                      "note": "mỗi mã mua 50 triệu; A +20% = 60; B −20% = 40; cần 50 triệu: bán hết B (40) + 10 của A, hoặc bán 50 của A"}}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
