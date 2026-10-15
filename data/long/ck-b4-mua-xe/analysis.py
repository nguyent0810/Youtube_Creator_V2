"""B4 "Mua xe" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH, kênh tự tính).

    python data/long/ck-b4-mua-xe/analysis.py      # in bảng + ghi results.json

Số thật (có nguồn, xem script.md Ghi chú): lệ phí trước bạ ô tô chở người ≤ 9 chỗ lần đầu: mức chung 10%, Hà Nội 12% · lệ phí cấp biển
Hà Nội/TP.HCM 14 triệu (TT 155/2025, từ 01/01/2026) · phí sử dụng đường bộ 130 nghìn/tháng (NĐ 90/2023) · bảo hiểm TNDS bắt buộc
< 6 chỗ không kinh doanh 437 nghìn/năm chưa VAT (NĐ 67/2023) · lãi vay mua xe: ưu đãi năm đầu ~7–9%, thả nổi sau ưu đãi ~12–15%
(báo chí 10/2026) · tiết kiệm 12 tháng nhóm ngân hàng lớn 6,8%/năm (09/2026, hồ sơ B1).
GIẢ ĐỊNH (ghi trên màn hình): xe 700 triệu, giá tính lệ phí = giá xe, đăng ký ở Hà Nội; khoản khác lúc lăn bánh 2 triệu; bảo hiểm vật
chất 1,5%/năm giá trị xe; gửi xe 1,5 triệu/tháng; 12.000 km/năm, 7 lít/100 km, 24.000 đ/lít; bảo dưỡng 6 triệu/năm; giá bán lại sau 5 năm
= 55% giá xe; trả góp: trả trước 30% giá xe, vay 70% trong 84 tháng, gốc đều, lãi 8% năm đầu rồi 13%; "chưa mua": đi xe công nghệ/taxi
4 triệu/tháng; tiền chưa tiêu gửi tiết kiệm 6,8%/năm, ghép tháng.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V, LPTB, PLATE, OTHER = 700.0, 0.12, 14.0, 2.0
ROAD, TNDS = 0.13 * 12, 0.437 * 1.1
BHVC, PARK, KM, L100, FUEL, MAINT = 0.015, 1.5, 12000, 7, 0.024, 6.0
RESALE5, DOWN, N, R1, R2 = 0.55, 0.30, 84, 0.08, 0.13
TAXI, SAVE = 4.0, 0.068
YEARS = 5


def car_value(y):            # giá trị xe đầu năm y (y=0: mới) — chỉ để tính bảo hiểm vật chất; nội suy tuyến tính tới RESALE5
    return V * (1 - (1 - RESALE5) * y / YEARS)


onroad = V * LPTB + PLATE + OTHER                     # chi phí lăn bánh ngoài giá xe (không gồm phí năm đầu)
fuel_y = KM / 100 * L100 * FUEL
run = [ROAD + TNDS + BHVC * car_value(y) + PARK * 12 + fuel_y + MAINT for y in range(YEARS)]
run_m = [round(r / 12, 2) for r in run]

# Trả góp: lịch trả 84 tháng, gốc đều
loan = V * (1 - DOWN)
bal, interest, pays = loan, [], []
for m in range(1, N + 1):
    r = (R1 if m <= 12 else R2) / 12
    i = bal * r
    pays.append(loan / N + i); interest.append(i); bal -= loan / N
int5 = sum(interest[:60]); bal5 = loan - loan / N * 60

# Ba lối đi qua 5 năm
r_m = SAVE / 12
fv = lambda pv, n=60: pv * (1 + r_m) ** n
cash0 = V + onroad                                     # lăn bánh, trả thẳng
inst0 = V * DOWN + onroad                              # trả góp: trả trước + chi phí lăn bánh
own_month = [run[m // 12] / 12 for m in range(60)]
resale = V * RESALE5
net_cash = cash0 + sum(own_month) - resale             # chi ròng 5 năm, CHƯA tính lãi tiết kiệm bỏ lỡ
net_inst = net_cash + int5                             # cùng xe, cùng gốc; thêm tiền lãi vay 5 năm (chưa trừ lãi gửi của phần giữ lại)
res = {"onroad": {"lptb": round(V * LPTB, 1), "plate": PLATE, "other": OTHER, "total_extra": round(onroad, 1), "lan_banh": round(cash0, 1),
                  "road_y": round(ROAD, 2), "tnds_y": round(TNDS, 3)},
       "run_year": [round(x, 1) for x in run], "run_month_y1": run_m[0], "fuel_y": round(fuel_y, 2),
       "loan": {"amount": loan, "pay_m1": round(pays[0], 2), "pay_m12": round(pays[11], 2), "pay_m13": round(pays[12], 2), "jump": round(pays[12] - pays[11], 2),
                "interest_5y": round(int5, 1), "interest_all": round(sum(interest), 1), "balance_5y": round(bal5, 1), "upfront": round(inst0, 1)},
       "resale_5y": resale, "depreciation_5y": round(V - resale, 1),
       "net_5y": {"tra_thang": round(net_cash, 1), "tra_gop": round(net_inst, 1)}, "per_month": {"tra_thang": round(net_cash / 60, 2), "tra_gop": round(net_inst / 60, 2)},
       "run_5y": round(sum(own_month), 1),
       "own_total_month_y1": round((run[0] + (V - resale) / YEARS) / 12, 2),
       "breakeven_taxi": None}
# mức chi đi lại mỗi tháng (taxi) để "chưa mua" bằng "trả thẳng"
lo, hi = 0.0, 40.0
for _ in range(100):
    t = (lo + hi) / 2
    w = fv(cash0) + sum((own_month[k] - t) * (1 + r_m) ** (60 - k - 1) for k in range(60))
    lo, hi = (t, hi) if w > resale else (lo, t)
res["breakeven_taxi"] = round(t, 2)
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
