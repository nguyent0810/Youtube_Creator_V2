"""Các phép tính cho ck-c6-gia-tran-san-t2.

Toàn bộ số tiền và 100 cổ phiếu dưới đây là VÍ DỤ GIẢ ĐỊNH, không phải
minh hoạ một cổ phiếu, tài khoản hay một quyết định giao dịch thực tế.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = 20_000
SHARES = 100
BAND = 0.07

floor_price = REFERENCE * (1 - BAND)
ceiling_price = REFERENCE * (1 + BAND)
order_value = REFERENCE * SHARES
res = {
    "assume": {"reference_vnd": REFERENCE, "shares": SHARES, "market": "HOSE", "band": BAND},
    "band": {"floor_vnd": int(floor_price), "reference_vnd": REFERENCE, "ceiling_vnd": int(ceiling_price)},
    "order": {"value_vnd": order_value, "fees_included": False},
    "apr_3_2025": {"down_total": 517, "floor_down": 263, "other_down": 517 - 263, "up": 13, "ceiling_up": 3},
    "index": {"apr_3": 1229.84, "apr_3_change": -87.99, "apr_3_pct": -6.68,
              "apr_9": 1094.30, "apr_9_change": -38.49, "apr_9_pct": -3.40},
    "settlement": {"t2_complete_start": "11:00", "t2_complete_end": "11:30", "allocation_before": "13:00",
                   "sell_from": "afternoon T+2"},
    "tuan_ledger": {"T": {"cash_matched_vnd": order_value, "shares_sellable": 0},
                    "T1": {"cash_matched_vnd": order_value, "shares_sellable": 0},
                    "T2_afternoon": {"cash_matched_vnd": order_value, "shares_sellable": SHARES}},
    "special_band": {"hose_first_or_resume": 0.20, "upcom_first_or_resume": 0.40, "upcom_regular": 0.15},
}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=2))
