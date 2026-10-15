"""C5 "Cổ tức" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH, kênh tự tính).

    python data/long/ck-c5-co-tuc/analysis.py      # in bảng + ghi results.json

Quy tắc (có nguồn, xem script.md Ghi chú): tỷ lệ cổ tức tính trên mệnh giá 10.000 đ · cổ tức tiền mặt cá nhân bị khấu trừ thuế TNCN 5% ·
ngày giao dịch không hưởng quyền: giá tham chiếu = giá đóng cửa phiên trước − cổ tức tiền (tiền mặt), hoặc ÷ (1 + tỷ lệ) (cổ phiếu).
GIẢ ĐỊNH (ghi trên màn hình): cổ phiếu giá 40.000 đ; cổ tức tiền 10% mệnh giá; cổ tức cổ phiếu 20%; nắm 1.000 cổ phiếu; phí giao dịch mua + bán
0,3% mỗi chiều, thuế bán 0,1% (mức ví dụ, mỗi công ty chứng khoán một khác).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAR, P, CASH_PCT, STOCK_PCT, N = 10_000, 40_000, 0.10, 0.20, 1_000
TAX, FEE, SELLTAX = 0.05, 0.003, 0.001

div = PAR * CASH_PCT                       # 1.000 đ/cp
net = div * (1 - TAX)                      # 950
yield_ = div / P                            # 2,5%
p_ex_cash = P - div                         # 39.000
p_ex_stock = P / (1 + STOCK_PCT)            # 33.333
# "Mua để ăn cổ tức": mua 1.000 cp phiên trước ngày không hưởng quyền, bán ở đúng giá tham chiếu ngày không hưởng quyền
buy = N * P * (1 + FEE)
sell = N * p_ex_cash * (1 - FEE - SELLTAX)
got = N * net
res = {"div_per_share": div, "net_per_share": net, "tax_per_share": div * TAX, "yield_pct": round(yield_ * 100, 2),
       "headline_vs_yield": {"headline_pct": CASH_PCT * 100, "yield_pct": round(yield_ * 100, 2)},
       "ex_cash": {"before": P, "after": p_ex_cash, "holding_before": N * P, "holding_after_plus_div": N * p_ex_cash + N * div,
                   "holding_after_plus_net": N * p_ex_cash + N * net},
       "ex_stock": {"before_shares": N, "after_shares": round(N * (1 + STOCK_PCT)), "before_price": P, "after_price": round(p_ex_stock),
                    "value_before": N * P, "value_after": round(N * (1 + STOCK_PCT) * p_ex_stock)},
       "dividend_capture": {"buy": round(buy), "sell": round(sell), "dividend_net": round(got), "result": round(sell + got - buy)},
       "same_yield_price": {"p20000": round(div / 20_000 * 100, 2), "p100000": round(div / 100_000 * 100, 2)}}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
