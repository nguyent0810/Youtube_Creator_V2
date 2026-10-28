"""E6 "Rút BHXH một lần hay chờ lương hưu" — phép tính minh hoạ (VÍ DỤ GIẢ ĐỊNH, mọi số quy về giá hôm nay).

    python data/long/ck-e6-luong-huu-rut-mot-lan/analysis.py      # in kết quả + ghi results.json

Luật (nguồn trong factcheck.md): Luật BHXH 2024 (41/2024/QH15, hiệu lực 01/07/2025):
- Lương hưu: tối thiểu 15 năm đóng. Nữ: 45% mức bình quân tiền lương đóng BHXH ứng với 15 năm, mỗi năm thêm +2%, tối đa 75% (30 năm).
  Nam: 40% ứng với 15 năm, +1%/năm tới 20 năm, rồi +2%/năm, tối đa 75% (35 năm).
- BHXH một lần (người đã đóng trước 01/07/2025, nghỉ đủ 12 tháng, chưa đủ 20 năm): mỗi năm đóng trước 2014 = 1,5 tháng bình quân,
  từ 2014 = 2 tháng bình quân. Bình quân tiền lương được điều chỉnh theo chỉ số giá (hệ số trượt giá) -> giả định "đã quy về giá hôm nay".
- Tuổi nghỉ hưu (NĐ 135/2020): nữ 57 tuổi năm 2026, 60 tuổi từ 2035; nam 61 tuổi 6 tháng năm 2026, 62 từ 2028.
Ví dụ (chị Hạnh, nhân vật giả định): sinh 1991, đóng BHXH bắt buộc từ 2016 tới giữa 2026 = 10 năm, lương đóng bình quân 10 tr/tháng
(đã điều chỉnh theo giá), nghỉ việc giữa 2026. Nghỉ hưu ở 60 tuổi = năm 2051. Lương hưu được giả định giữ sức mua (điều chỉnh theo giá).
Tuổi thọ trung bình lúc sinh của phụ nữ Việt Nam 2024: 77,3 (Cục Thống kê) -> chỉ dùng làm mốc minh hoạ, không phải dự báo đời một người.
Kiểm độc lập: check.py.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, YEARS0, BIRTH = 10.0, 10, 1991              # triệu đồng/tháng, năm đã đóng, năm sinh
RETIRE_AGE, LIFE = 60, 77.3


def rate_female(y):
    return 0.0 if y < 15 else min(0.75, 0.45 + 0.02 * (y - 15))


def rate_male(y):
    if y < 15:
        return 0.0
    if y < 20:
        return 0.40 + 0.01 * (y - 15)
    return min(0.75, 0.45 + 0.02 * (y - 20))


def lump(years_before_2014, years_from_2014, w=W):
    return w * (1.5 * years_before_2014 + 2 * years_from_2014)


res = {"assume": {"wage": W, "years_paid": YEARS0, "birth": BIRTH, "retire_age": RETIRE_AGE, "retire_year": BIRTH + RETIRE_AGE}}
L = lump(0, YEARS0)
res["lump_now"] = L                                            # 200 tr
res["lump_if_pre2014_mix"] = lump(4, 6)                        # minh hoạ: 4 năm trước 2014 + 6 năm sau -> 180 tr
opts = {}
for y in (15, 20, 25, 30):
    p = W * rate_female(y)
    months_to_match = L / p
    years_paid_more = y - YEARS0
    opts[str(y)] = {"rate": round(rate_female(y), 2), "pension": round(p, 2), "months_to_match_lump": round(months_to_match, 1),
                    "age_match": round(RETIRE_AGE + months_to_match / 12, 1),
                    "sum_to_77": round(p * 12 * (LIFE - RETIRE_AGE)),
                    "employee_contrib_more": round(0.08 * W * 12 * years_paid_more, 1),     # phần người lao động đóng thêm (8%)
                    "voluntary_contrib_more": round(0.22 * W * 12 * years_paid_more, 1),   # nếu tự đóng tự nguyện 22% (chưa trừ hỗ trợ)
                    "year_reach": 2026 + years_paid_more}
res["female"] = opts
res["male_rates"] = {str(y): round(rate_male(y), 2) for y in (15, 18, 20, 25, 30, 35)}
# nếu cầm 200 tr đi gửi/đầu tư, lãi THỰC (sau lạm phát) r mỗi năm, 24 năm tới 2051 -> bao nhiêu (giá hôm nay)
res["lump_grow_2051"] = {f"{r:.0%}": round(L * (1 + r) ** 25) for r in (-0.01, 0.0, 0.01, 0.02, 0.03)}  # giữa 2026 -> giữa 2051 = 25 năm
# số tháng lương hưu 4,5 tr mà khoản ấy (lãi thực 2%) trả được nếu rút đều từ 60 tuổi
import math
r_m = 0.02 / 12
pv = res["lump_grow_2051"]["2%"]
pay = 4.5
n = -math.log(1 - pv * r_m / pay) / math.log(1 + r_m) if pv * r_m < pay else float("inf")
res["lump_2pct_as_4_5_months"] = round(n, 1)
res["own_contrib_10y"] = round(0.08 * W * 12 * YEARS0, 1)          # phần người lao động tự đóng BHXH (8%) trong 10 năm: 96 tr
res["lump_vs_own"] = round(L / res["own_contrib_10y"], 2)
res["male_15y_pension"] = round(W * rate_male(15), 2)              # nam cùng hoàn cảnh, 15 năm: 4 tr
res["debt30_interest_saved_1y"] = round(L * 0.30, 1)              # trả 200 tr nợ lãi 30%/năm: bớt ~60 tr lãi một năm (giả định)
res["life_years_after_60"] = round(LIFE - RETIRE_AGE, 1)
res["retire_age_2026"] = {"female": "57", "male": "61 tuổi 6 tháng"}
res["stats_2016_2022"] = {"recipients_million": 4.8, "returned_million": 1.3, "left_million": 3.5, "age20_40_pct": 77.5,
                          "under5y_pct": 66.6, "5to10y_pct": 23.8, "under10y_pct": round(66.6 + 23.8, 1)}
(HERE / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
