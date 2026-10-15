"""C3 "Biểu đồ nến" — kênh tự tính trên VN-Index (data/ck/vnindex_1d.csv, vnstock/VCI, 08/10/2018 → 06/10/2026).

    python data/long/ck-c3-bieu-do-nen/analysis.py            # in bảng + ghi results.json cạnh file này

Ba phần:
  1. Tuần 09/03 → 13/03/2026 (gọi lại C2): OHLC, thân, bóng, màu nến vs màu bảng giá, nến tuần gộp.
  2. Thống kê màu nến: nến đỏ (đóng < mở) mà chỉ số vẫn tăng so với hôm trước, và ngược lại.
  3. Thử các mẫu nến phổ biến: sau mẫu, bao nhiêu % lần VN-Index cao hơn sau 5 / 20 phiên — so với TỈ LỆ NỀN (mọi ngày,
     và mọi ngày cùng bối cảnh "vừa giảm"). Khoảng tin cậy Wilson 95%. Chia hai giai đoạn để xem kết quả có ổn định không.
     3b nến dài · 3c độ nhạy định nghĩa · 3d doji "đổi hướng" · 3e kiểm tra ngày ngẫu nhiên (20.000 lần) · 3f các lần trong 2026.
  4. Khung thời gian: nến tuần 2026 -> vnindex_1w_2026.csv (cho cảnh nến tuần đề xuất).

Định nghĩa (đơn giản hoá từ sách phổ thông — Nison 1991; Bulkowski; Marshall, Young & Rose 2006 dùng xu hướng MA):
  R = H − L (biên phiên), B = |C − O| (thân), U = H − max(O, C) (bóng trên), D = min(O, C) − L (bóng dưới).
  * "Vừa giảm" (bối cảnh): đóng cửa hôm trước < đóng cửa 6 phiên trước (5 phiên trước tín hiệu đi xuống). "Vừa tăng": ngược lại.
  * Doji: B ≤ 0,1·R.
  * Búa (hammer): D ≥ 2·B, U ≤ 0,1·R, B > 0, R > 0; bản "đúng sách" thêm bối cảnh vừa giảm.
  * Ba chàng lính trắng (three white soldiers): 3 nến xanh liền (C > O); đóng cửa sau cao hơn đóng cửa trước; giá mở nằm trong
    thân nến trước (O_{t−1} ≤ O_t ≤ C_{t−1}); bóng trên mỗi nến ≤ 0,3·R. Bản "đúng sách" thêm bối cảnh vừa giảm (trước nến 1).
  * Nhấn chìm tăng (bullish engulfing, chỉ ghi hồ sơ): hôm trước đỏ, hôm nay xanh, O_t ≤ C_{t−1} và C_t ≥ O_{t−1}; bối cảnh vừa giảm.
  * Ba con quạ đen / sao băng (đối xứng, chỉ ghi hồ sơ): kỳ vọng "giảm" -> đo % lần THẤP hơn sau 5 / 20 phiên.
Lợi suất tương lai: đóng cửa phiên t+h / đóng cửa phiên tín hiệu t − 1 (tín hiệu chỉ biết sau khi phiên t đóng cửa).
Nến lỗi dữ liệu (H < max(O, C) hoặc L > min(O, C); 4 phiên: 24–26/06/2019 giá mở đứng yên 949,48; 23/08/2021) bị loại khỏi
việc nhận diện mẫu nhưng vẫn dùng làm giá đóng cửa.
Lưu ý thống kê: các cửa sổ 20 phiên chồng lên nhau -> các lần quan sát không độc lập; khoảng tin cậy Wilson là LẠC QUAN
(hẹp hơn thật). Không tính phí, thuế. Không phải chiến lược giao dịch — chỉ đo tần suất trong quá khứ.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CSV = ROOT / "data" / "ck" / "vnindex_1d.csv"
HORIZONS = (5, 20)


def load() -> pd.DataFrame:
    d = pd.read_csv(CSV)
    d["time"] = d["time"].str[:10]
    d = d.reset_index(drop=True)
    d["R"] = d.high - d.low
    d["B"] = (d.close - d.open).abs()
    d["U"] = d.high - d[["open", "close"]].max(axis=1)
    d["D"] = d[["open", "close"]].min(axis=1) - d.low
    d["green"] = d.close > d.open
    d["red"] = d.close < d.open
    d["chg"] = d.close / d.close.shift(1) - 1
    d["valid"] = (d.U >= -1e-9) & (d.D >= -1e-9) & (d.R > 0)
    d["down5"] = d.close.shift(1) < d.close.shift(6)       # 5 phiên TRƯỚC tín hiệu đi xuống
    d["up5"] = d.close.shift(1) > d.close.shift(6)
    for h in HORIZONS:
        d[f"f{h}"] = d.close.shift(-h) / d.close - 1
    return d


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    w = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (c - w, c + w)


def patterns(d: pd.DataFrame) -> dict[str, pd.Series]:
    v = d.valid
    doji = v & (d.B <= 0.1 * d.R)
    hammer_shape = v & (d.B > 0) & (d.D >= 2 * d.B) & (d.U <= 0.1 * d.R)
    hammer = hammer_shape & d.down5
    g = d.green & v
    o, c, u, r = d.open, d.close, d.U, d.R
    soldier = g & (u <= 0.3 * r)
    tws_shape = (soldier & soldier.shift(1, fill_value=False) & soldier.shift(2, fill_value=False)
                 & (c > c.shift(1)) & (c.shift(1) > c.shift(2))
                 & (o >= o.shift(1)) & (o <= c.shift(1)) & (o.shift(1) >= o.shift(2)) & (o.shift(1) <= c.shift(2)))
    tws = tws_shape & d.down5.shift(2, fill_value=False)
    engulf = (v & v.shift(1, fill_value=False) & d.red.shift(1, fill_value=False) & d.green
              & (o <= c.shift(1)) & (c >= o.shift(1)) & d.down5)
    # đối xứng phía giảm
    star = v & (d.B > 0) & (d.U >= 2 * d.B) & (d.D <= 0.1 * d.R) & d.up5
    rd = d.red & v & (d.D <= 0.3 * r)
    crows = (rd & rd.shift(1, fill_value=False) & rd.shift(2, fill_value=False)
             & (c < c.shift(1)) & (c.shift(1) < c.shift(2))
             & (o <= o.shift(1)) & (o >= c.shift(1)) & (o.shift(1) <= o.shift(2)) & (o.shift(1) >= c.shift(2))
             & d.up5.shift(2, fill_value=False))
    return {"doji": doji, "hammer_shape": hammer_shape, "hammer": hammer, "tws_shape": tws_shape, "tws": tws,
            "engulf": engulf, "shooting_star": star, "three_crows": crows}


BEARISH = {"shooting_star", "three_crows"}


def stat(d: pd.DataFrame, mask: pd.Series, h: int, bear: bool = False) -> dict:
    f = d.loc[mask, f"f{h}"].dropna()
    n = len(f)
    k = int((f < 0).sum() if bear else (f > 0).sum())
    lo, hi = wilson(k, n)
    return {"n": n, "k": k, "pct": round(100 * k / n, 1) if n else None,
            "ci95": [round(100 * lo, 1), round(100 * hi, 1)] if n else None,
            "mean_ret_pct": round(100 * f.mean(), 2) if n else None,
            "median_ret_pct": round(100 * f.median(), 2) if n else None}


def binom_p(k: int, n: int, p0: float) -> float:
    """p-value hai phía (xấp xỉ chuẩn, có hiệu chỉnh liên tục) — chỉ để tham khảo, quan sát không độc lập."""
    if n == 0:
        return float("nan")
    mu, sd = n * p0, math.sqrt(n * p0 * (1 - p0))
    z = (abs(k - mu) - 0.5) / sd if sd else 0
    return round(math.erfc(max(z, 0) / math.sqrt(2)), 3)


def main() -> None:
    d = load()
    out: dict = {"source": "data/ck/vnindex_1d.csv (vnstock/VCI)", "first": d.time.iloc[0], "last": d.time.iloc[-1],
                 "sessions": len(d), "invalid_candles": d.loc[~d.valid, "time"].tolist()}
    print(f"VN-Index {out['first']} → {out['last']}: {len(d)} phiên; nến lỗi dữ liệu: {out['invalid_candles']}")

    # ---- 1. tuần 09/03 → 13/03/2026
    wk = d[(d.time >= "2026-03-06") & (d.time <= "2026-03-13")].copy()
    print("\n1. Tuần 09–13/03/2026 (kèm 06/03 làm tham chiếu)")
    rows = []
    for _, r in wk.iterrows():
        row = {"date": r.time, "O": r.open, "H": r.high, "L": r.low, "C": r.close, "body": round(r.B, 2),
               "upper": round(r.U, 2), "lower": round(r.D, 2), "range": round(r.R, 2),
               "body_share": round(r.B / r.R, 3) if r.R else None, "candle": "xanh" if r.green else "đỏ" if r.red else "ngang",
               "chg_pct": round(100 * r.chg, 2)}
        rows.append(row)
        print("  ", row)
    w = d[(d.time >= "2026-03-09") & (d.time <= "2026-03-13")]
    weekly = {"O": float(w.open.iloc[0]), "H": float(w.high.max()), "L": float(w.low.min()), "C": float(w.close.iloc[-1]),
              "prev_week_close": float(d.loc[d.time == "2026-03-06", "close"].iloc[0])}
    weekly["chg_pct"] = round(100 * (weekly["C"] / weekly["prev_week_close"] - 1), 2)
    weekly["body"] = round(abs(weekly["C"] - weekly["O"]), 2)
    weekly["lower"] = round(min(weekly["O"], weekly["C"]) - weekly["L"], 2)
    weekly["upper"] = round(weekly["H"] - max(weekly["O"], weekly["C"]), 2)
    print("   nến TUẦN 09–13/03:", weekly)
    out["week_0309"] = {"days": rows, "weekly": weekly}

    # ---- 2. màu nến vs màu bảng giá (so với tham chiếu = đóng cửa hôm trước)
    vv = d[d.valid & d.chg.notna()]
    red_up = vv[vv.red & (vv.chg > 0)]
    green_down = vv[vv.green & (vv.chg < 0)]
    out["colour"] = {"valid_sessions": len(vv), "green": int(vv.green.sum()), "red": int(vv.red.sum()),
                     "red_but_index_up": len(red_up), "green_but_index_down": len(green_down),
                     "mismatch_pct": round(100 * (len(red_up) + len(green_down)) / len(vv), 1),
                     "examples_2026_red_up": red_up[red_up.time >= "2026-01-01"][["time", "open", "close", "chg"]]
                     .assign(chg=lambda x: (100 * x.chg).round(2)).to_dict("records"),
                     "examples_2026_green_down": green_down[green_down.time >= "2026-01-01"][["time", "open", "close", "chg"]]
                     .assign(chg=lambda x: (100 * x.chg).round(2)).to_dict("records")}
    print(f"\n2. Màu nến: {len(vv)} phiên hợp lệ, xanh {out['colour']['green']}, đỏ {out['colour']['red']}; "
          f"nến đỏ mà chỉ số tăng {len(red_up)}, nến xanh mà chỉ số giảm {len(green_down)} "
          f"({out['colour']['mismatch_pct']}% số phiên)")
    print("   2026 nến đỏ mà tăng:", out["colour"]["examples_2026_red_up"])
    print("   2026 nến xanh mà giảm:", out["colour"]["examples_2026_green_down"])
    # tỉ lệ nến xanh trong 2026
    y26 = vv[vv.time >= "2026-01-01"]
    out["colour"]["y2026"] = {"n": len(y26), "green": int(y26.green.sum()), "red": int(y26.red.sum())}

    # ---- 3. mẫu nến
    P = patterns(d)
    base_mask = d.valid
    out["patterns"] = {}
    print("\n3. Mẫu nến -> % lần VN-Index CAO hơn (mẫu giảm: THẤP hơn) sau h phiên (đóng cửa→đóng cửa)")
    ctx = {"all": base_mask, "down5": base_mask & d.down5, "up5": base_mask & d.up5}
    for h in HORIZONS:
        for name, m in ctx.items():
            s = stat(d, m, h)
            sb = stat(d, m, h, bear=True)
            out.setdefault("base", {})[f"{name}_f{h}"] = {"up": s, "down": sb}
            print(f"   NỀN {name:6s} f{h:<2d}: tăng {s['pct']}% (n={s['n']}), giảm {sb['pct']}%, TB {s['mean_ret_pct']}%")
    halves = [("2018-10-08", "2022-12-31"), ("2023-01-01", "2026-10-06")]
    for name, m in P.items():
        bear = name in BEARISH
        ref = ("up5" if name in ("shooting_star", "three_crows") else "down5" if name in ("hammer", "tws", "engulf") else "all")
        res = {"count": int(m.sum()), "count_2026": int(m[d.time >= "2026-01-01"].sum()),
               "dates_2026": d.loc[m & (d.time >= "2026-01-01"), "time"].tolist(), "ref_context": ref, "bear": bear}
        for h in HORIZONS:
            s = stat(d, m, h, bear)
            b = out["base"][f"{ref}_f{h}"]["down" if bear else "up"]
            ball = out["base"][f"all_f{h}"]["down" if bear else "up"]
            s["base_ctx_pct"], s["base_all_pct"] = b["pct"], ball["pct"]
            s["diff_vs_ctx_pp"] = round(s["pct"] - b["pct"], 1) if s["n"] else None
            s["p_vs_ctx"] = binom_p(s["k"], s["n"], b["pct"] / 100)
            s["halves"] = {f"{a[:4]}-{z[:4]}": stat(d, m & (d.time >= a) & (d.time <= z), h, bear) for a, z in halves}
            res[f"f{h}"] = s
        out["patterns"][name] = res
        print(f"   {name:14s} n={res['count']:4d} (2026: {res['count_2026']:2d})  "
              + "  ".join(f"f{h}: {res[f'f{h}']['pct']}% [{res[f'f{h}']['ci95'][0]}–{res[f'f{h}']['ci95'][1]}] "
                          f"nền({ref}) {res[f'f{h}']['base_ctx_pct']}% p≈{res[f'f{h}']['p_vs_ctx']}"
                          for h in HORIZONS if res[f'f{h}']['n']))
        for h in HORIZONS:
            print(f"        f{h} theo giai đoạn:", {k: (v['n'], v['pct']) for k, v in res[f'f{h}']['halves'].items()})

    # ---- 3b. "cây nến dài" (thân ≥ 2× trung vị thân 20 phiên trước) — câu hỏi phổ thông "nến xanh dài là tốt?"
    medB = d.B.rolling(20).median().shift(1)
    long_green = d.valid & d.green & (d.B >= 2 * medB)
    long_red = d.valid & d.red & (d.B >= 2 * medB)
    out["long_candles"] = {}
    for nm, m in (("long_green", long_green), ("long_red", long_red)):
        out["long_candles"][nm] = {f"f{h}": stat(d, m, h) for h in HORIZONS} | {"count": int(m.sum())}
        print(f"   {nm:14s} n={int(m.sum())}  " + "  ".join(f"f{h}: tăng {out['long_candles'][nm][f'f{h}']['pct']}%" for h in HORIZONS))

    # ---- 3c. độ nhạy: định nghĩa lỏng hơn / bối cảnh khác (để chắc kết luận không do một ngưỡng tình cờ)
    v, g, c, o = d.valid, d.green, d.close, d.open
    sma10 = c.rolling(10).mean()
    below10 = (c.shift(1) < sma10.shift(1))
    hammer_ma = P["hammer_shape"] & below10
    g3 = v & g & (d.U <= 0.3 * d.R)
    tws_loose = g3 & g3.shift(1, fill_value=False) & g3.shift(2, fill_value=False) & (c > c.shift(1)) & (c.shift(1) > c.shift(2))
    hammer_loose = v & (d.B > 0) & (d.D >= 2 * d.B) & (d.U <= d.B) & d.down5
    out["sensitivity"] = {}
    for nm, m, ref in (("hammer_below_sma10", hammer_ma, v & below10), ("hammer_loose", hammer_loose, v & d.down5),
                       ("tws_loose_3green", tws_loose, v)):
        r = {"count": int(m.sum())}
        for h in HORIZONS:
            s, b = stat(d, m, h), stat(d, ref, h)
            r[f"f{h}"] = s | {"base_pct": b["pct"], "base_mean_ret_pct": b["mean_ret_pct"],
                              "p_vs_base": binom_p(s["k"], s["n"], b["pct"] / 100),
                              "halves": {f"{a[:4]}-{z[:4]}": stat(d, m & (d.time >= a) & (d.time <= z), h) for a, z in halves}}
        out["sensitivity"][nm] = r
        print(f"   [độ nhạy] {nm:20s} n={r['count']:4d}  " + "  ".join(
            f"f{h}: {r[f'f{h}']['pct']}% (TB {r[f'f{h}']['mean_ret_pct']}%) vs nền {r[f'f{h}']['base_pct']}% "
            f"(TB {r[f'f{h}']['base_mean_ret_pct']}%) p≈{r[f'f{h}']['p_vs_base']} "
            f"{ {k: (x['n'], x['pct']) for k, x in r[f'f{h}']['halves'].items()} }" for h in HORIZONS))

    # ---- 3d. doji = "lưỡng lự, sắp đảo chiều"? đo % lần hướng 5 phiên SAU ngược hướng 5 phiên TRƯỚC
    prev5 = c / c.shift(5) - 1
    rev = (prev5 * d["f5"]) < 0
    okm = prev5.notna() & d["f5"].notna() & (prev5 != 0)
    dj = P["doji"] & okm
    out["doji_reversal"] = {"n": int(dj.sum()), "pct": round(100 * rev[dj].mean(), 1),
                            "base_n": int((v & okm).sum()), "base_pct": round(100 * rev[v & okm].mean(), 1)}
    out["doji_reversal"]["p"] = binom_p(int(rev[dj].sum()), int(dj.sum()), out["doji_reversal"]["base_pct"] / 100)
    print("   doji đảo chiều 5 phiên:", out["doji_reversal"])

    # ---- 3e. kiểm tra "ngày ngẫu nhiên": rút ngẫu nhiên đúng n ngày cùng bối cảnh, 20.000 lần — mẫu có nổi bật không?
    import random
    random.seed(20261009)
    out["random_dates"] = {}
    for nm, m, ref in (("engulf", P["engulf"], v & d.down5), ("doji", P["doji"], v), ("hammer", P["hammer"], v & d.down5),
                       ("long_green", long_green, v)):
        for h in HORIZONS:
            pool = d.loc[ref, f"f{h}"].dropna().tolist()
            f = d.loc[m, f"f{h}"].dropna()
            n, obs = len(f), (f > 0).mean()
            sims = [sum(x > 0 for x in random.sample(pool, n)) / n for _ in range(20000)]
            pv = sum(abs(s_ - sum(x > 0 for x in pool) / len(pool)) >= abs(obs - sum(x > 0 for x in pool) / len(pool)) - 1e-12
                     for s_ in sims) / len(sims)
            out["random_dates"][f"{nm}_f{h}"] = {"n": n, "obs_pct": round(100 * obs, 1), "p_two_sided": round(pv, 3)}
    print("   ngày ngẫu nhiên (p hai phía):", {k: (x["obs_pct"], x["p_two_sided"]) for k, x in out["random_dates"].items()})
    out["tests_run_note"] = ("8 mẫu × 2 khung (5, 20 phiên) = 16 phép so chính + 3 bản độ nhạy × 2; với ngưỡng p < 0,1 có thể "
                             "kỳ vọng ~1–2 kết quả 'đẹp' do may rủi dù không mẫu nào có thật.")

    # ---- 3f. các lần xuất hiện trong 2026 (để đánh dấu trên cảnh candles) + chuyện gì xảy ra sau đó
    def after(mask, nm):
        rows_ = d.loc[mask & (d.time >= "2026-01-01"), ["time", "close", "f5", "f20"]]
        return [{"date": r.time, "close": r.close, "f5_pct": None if pd.isna(r.f5) else round(100 * r.f5, 2),
                 "f20_pct": None if pd.isna(r.f20) else round(100 * r.f20, 2)} for r in rows_.itertuples()]
    out["cases_2026"] = {nm: after(P[nm], nm) for nm in ("hammer", "hammer_shape", "engulf", "doji", "shooting_star")}
    for nm, xs in out["cases_2026"].items():
        print(f"   2026 {nm}: " + "; ".join(f"{x['date']} f5 {x['f5_pct']} f20 {x['f20_pct']}" for x in xs))

    # ---- 4. khung thời gian: nến tuần 2026 (T2→T6), ghi CSV cho PM nếu cần dựng cảnh nến tuần
    d2 = d[d.time >= "2026-01-01"].copy()
    d2["wk"] = pd.to_datetime(d2.time).dt.to_period("W-SUN")
    wkly = d2.groupby("wk").agg(time=("time", "first"), open=("open", "first"), high=("high", "max"), low=("low", "min"),
                                close=("close", "last"), volume=("volume", "sum"), days=("time", "count")).reset_index(drop=True)
    wkly.to_csv(HERE / "vnindex_1w_2026.csv", index=False)
    out["timeframes_2026"] = {"daily_candles": len(d2), "weekly_candles": len(wkly),
                              "daily_green": int((d2.close > d2.open).sum()), "weekly_green": int((wkly.close > wkly.open).sum())}
    print("\n4. Khung thời gian 2026:", out["timeframes_2026"])
    lastc = d.close.iloc[-1]
    out["period_change_pct"] = round(100 * (lastc / d.close.iloc[0] - 1), 1)
    print("   VN-Index cả giai đoạn:", d.close.iloc[0], "→", lastc, f"({out['period_change_pct']}%)")

    (HERE / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    print("\n-> results.json")


if __name__ == "__main__":
    main()
