"""Tính lại độc lập các số minh hoạ của ck-f2-vien-phi-bhyt.

27/10/2026 (Claude): bản cũ chỉ so với số gõ cứng nên để lọt một hoá đơn không cộng khớp
(16 quỹ + 4 đồng chi trả + 5 ngoài phạm vi = 25, không phải 30). Bản này kiểm tính khớp của cả thác tiền."""
import json
from pathlib import Path

R = json.loads((Path(__file__).resolve().parent / "results.json").read_text(encoding="utf-8"))
w = R["waterfall"]
fund = round(w["covered"] * 0.80, 6)
ok = [
    w["fund"] == fund,                                                    # quỹ = 80% phần trong phạm vi
    w["copay"] == w["covered"] - fund,                                    # đồng chi trả = phần còn lại trong phạm vi
    w["covered"] + w["outside_scope"] == w["total"],                      # hai lớp của hoá đơn cộng đủ tổng
    w["fund"] + w["copay"] + w["outside_scope"] == w["total"],            # thác tiền không còn khoản không tên
    w["on_bill"] == w["total"] - w["fund"],                               # tự trả trên hoá đơn = tổng − quỹ
    w["burden"] == w["on_bill"] + w["outside_invoice"],
    abs(w["burden"] / (w["total"] + w["outside_invoice"]) - 0.375) < 1e-9,  # lời đọc: "khoảng ba mươi tám phần trăm"
    R["five_year_threshold"]["threshold"] == round(6 * 2.53, 2),
    R["out_of_pocket"]["year_2025"] < R["out_of_pocket"]["early_2000s"],
]
print("F2 check:", "OK" if all(ok) else f"LỖI ở {[i for i, x in enumerate(ok) if not x]}", f"({len(ok)} phép)")
assert all(ok)
