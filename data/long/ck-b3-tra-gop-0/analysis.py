"""B3 "Trả góp 0%" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH).

    python data/long/ck-b3-tra-gop-0/analysis.py      # in bảng + ghi results.json

Giả định: máy 20 triệu; trả thẳng giảm 1,5 triệu (18,5); trả góp 0% 12 tháng đều (20); phí chuyển đổi 3% trả cùng các kỳ (20,6).
"Lãi suất tương đương" = lãi suất tháng r sao cho giá trị hiện tại của 12 kỳ trả đều bằng số tiền thật sự được ứng hôm nay, nhân 12 (lãi đơn năm).
Ước lượng nhanh: phần trả thêm ÷ số thật sự vay × 2n/(n+1).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRICE, DISC, FEE, N = 20.0, 1.5, 0.03, 12


def irr(pv, pay, n=N):
    lo, hi = 0.0, 0.5
    for _ in range(200):
        r = (lo + hi) / 2
        v = sum(pay / (1 + r) ** k for k in range(1, n + 1))
        lo, hi = (r, hi) if v > pv else (lo, r)
    return r


cash, plain, withfee = PRICE - DISC, PRICE, PRICE * (1 + FEE)
apr = lambda pv, total: round(irr(pv, total / N) * 1200, 2)
res = {"prices": {"cash": cash, "installment": plain, "installment_fee": withfee, "monthly": round(withfee / N, 3)},
       "apr": {"both": apr(cash, withfee), "discount_only": apr(cash, plain), "fee_only": apr(PRICE, withfee), "none": 0.0},
       "quick": {"ratio": round((withfee - cash) / cash * 100, 2), "estimate": round((withfee - cash) / cash * 100 * 2 * N / (N + 1), 2)}}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(res)
