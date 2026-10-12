"""Độ rộng thị trường HOSE 2026 (video C1 "Cả năm VN-Index gần như đứng yên — sao tài khoản của bạn vẫn lỗ?").

Câu hỏi: bao nhiêu % cổ phiếu thường niêm yết trên HOSE đang ở dưới giá "đầu năm", trung vị thay đổi là bao nhiêu, và mã
nào kéo/đè VN-Index nhiều điểm nhất -- TỰ TÍNH từ giá cuối ngày lấy qua vnstock (nguồn VCI).

    python motion/long/breadth.py universe        # 1 lượt gọi: danh sách mã HOSE (VCI), lọc cổ phiếu
    python motion/long/breadth.py shares          # vài lượt: số cổ phiếu niêm yết (bảng giá VCI, theo lô 50 mã)
    python motion/long/breadth.py fetch           # 1 lượt/mã, nghỉ 3,6 s; chạy lại vô hại (bỏ qua mã đã có)
    python motion/long/breadth.py compute         # không gọi mạng: breadth_2026.csv, breadth_daily.csv, summary.json

Tệp ở data/ck/breadth_2026/. Quy ước tính (ghi lại trong summary.json):
- Vũ trụ: mã có exchange = HSX và type = STOCK trong danh sách VCI ngày chạy. LOẠI: ETF, chứng quyền (CW), quỹ đóng /
  quỹ BĐS (UNIT_TRUST), trái phiếu. Hạn chế: mã đã huỷ niêm yết hoặc chuyển sàn trong năm KHÔNG có trong danh sách
  (survivorship) -> thường làm số "dưới giá đầu năm" thấp đi chứ không cao lên.
- Mốc đầu năm: giá đóng cửa 31/12/2025 (cách tính "từ đầu năm" chuẩn của VN-Index) và, để đối chiếu, phiên đầu tiên của
  2026 (05/01/2026 -- 01/01 và 02/01 nghỉ). Mã chưa niêm yết tại mốc thì loại khỏi phép so sánh (đếm riêng).
- Mốc cuối: 30/09/2026 (hết quý, giai đoạn đã kết thúc) và phiên mới nhất <= 06/10/2026.
- Giá VCI là giá ĐÃ ĐIỀU CHỈNH cho cổ tức/chia tách [kiểm bằng cờ: ngày nào |biến động| > 7,6% (vượt biên độ HOSE ±7%)
  bị đánh dấu "gap" trong CSV để soát tay]. -> % thay đổi gần với "lợi nhuận giá + cổ tức tái đầu tư" chứ không phải giá
  danh nghĩa trên bảng điện.
- Đóng góp điểm VN-Index là XẤP XỈ: VNI_0 × (vốn hoá_i,0 / Σ vốn hoá_0) × % thay đổi_i, với vốn hoá = giá × số cổ phiếu
  niêm yết HIỆN TẠI (không điều chỉnh free-float, không tính phát hành thêm trong năm). Tổng các đóng góp được so với mức
  thay đổi thật của VN-Index để biết sai số.
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "ck" / "breadth_2026"
VNI = ROOT / "data" / "ck" / "vnindex_1d.csv"
PAUSE = 3.6             # vnstock Cộng đồng: ~20 lượt/phút, vượt là vnai tự kết thúc tiến trình -> 16–17 lượt/phút
START, END = "2025-12-20", "2026-10-06"
BASE_YTD, END_Q3 = "2025-12-31", "2026-09-30"
GAP = 7.6               # % một phiên; HOSE biên độ ±7% (ngày đầu niêm yết ±20%)


def _w(path: Path, rows: list[dict], cols: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _r(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- mạng (vnstock)
def universe() -> Path:
    from vnstock import Listing
    df = Listing(source="VCI").symbols_by_exchange()
    hsx = df[df["exchange"] == "HSX"]
    excl = hsx[hsx["type"] != "STOCK"].groupby("type").size().to_dict()
    st = hsx[hsx["type"] == "STOCK"].sort_values("symbol")
    rows = [{"symbol": r.symbol, "name": r.organ_short_name, "icb_code2": r.icb_code2} for r in st.itertuples()]
    _w(OUT / "universe.csv", rows, ["symbol", "name", "icb_code2"])
    (OUT / "universe_excluded.json").write_text(json.dumps({"source": "vnstock Listing(source='VCI').symbols_by_exchange()",
        "date": time.strftime("%Y-%m-%d"), "kept_HSX_STOCK": len(rows), "excluded_HSX_by_type": excl},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(rows)} cổ phiếu HSX; loại {excl}")
    return OUT / "universe.csv"


def shares() -> Path:
    from vnstock.explorer.vci.trading import Trading
    syms = [r["symbol"] for r in _r(OUT / "universe.csv")]
    rows = []
    for i in range(0, len(syms), 50):
        pb = Trading().price_board(syms[i:i + 50])["listing"]
        for r in pb.to_dict("records"):
            rows.append({"symbol": r["symbol"], "listed_share": r.get("listed_share"), "ref_price": r.get("ref_price"),
                         "trading_status": r.get("trading_status"), "security_status": r.get("security_status")})
        time.sleep(PAUSE)
    _w(OUT / "shares.csv", rows, ["symbol", "listed_share", "ref_price", "trading_status", "security_status"])
    print(f"shares: {len(rows)} mã")
    return OUT / "shares.csv"


def fetch() -> None:
    """Giá đóng cửa ngày START..END cho từng mã -> prices.csv (dài: symbol,time,close,volume) + status.csv (chạy lại an toàn)."""
    from vnstock import Quote
    syms = [r["symbol"] for r in _r(OUT / "universe.csv")]
    done = {r["symbol"] for r in _r(OUT / "status.csv")}
    todo = [s for s in syms if s not in done]
    print(f"{len(syms)} mã, đã có {len(done)}, còn {len(todo)} (~{len(todo) * PAUSE / 60:.0f} phút)", flush=True)
    pf, sf = OUT / "prices.csv", OUT / "status.csv"
    new_p, new_s = not pf.exists(), not sf.exists()
    with open(pf, "a", encoding="utf-8", newline="") as fp, open(sf, "a", encoding="utf-8", newline="") as fs:
        wp, ws = csv.writer(fp), csv.writer(fs)
        if new_p:
            wp.writerow(["symbol", "time", "close", "volume"])
        if new_s:
            ws.writerow(["symbol", "status", "bars", "first", "last"])
        for k, s in enumerate(todo, 1):
            t0 = time.time()
            try:
                df = Quote(symbol=s, source="VCI").history(start=START, end=END, interval="1D")
                df["time"] = df["time"].astype(str).str[:10]
                df = df[(df["time"] >= START) & (df["time"] <= END)]
                for r in df.itertuples():
                    wp.writerow([s, r.time, r.close, r.volume])
                st = ("ok", len(df), df["time"].min() if len(df) else "", df["time"].max() if len(df) else "")
            except Exception as e:  # noqa: BLE001 -- mã không có dữ liệu trong khoảng: ghi lại, đi tiếp
                st = ("err:" + str(e).replace("\n", " ")[:80], 0, "", "")
            fp.flush()
            ws.writerow([s, *st])
            fs.flush()
            if k % 25 == 0:
                print(f"  {k}/{len(todo)} {s}", flush=True)
            time.sleep(max(0.0, PAUSE - (time.time() - t0)) + 0.2)
    print("xong fetch", flush=True)


# ---------------------------------------------------------------- tính (không mạng)
def _vni() -> dict[str, float]:
    return {r["time"][:10]: float(r["close"]) for r in _r(VNI)}


def _at(series: dict[str, float], d: str) -> tuple[str, float] | None:
    """Giá đóng cửa gần nhất <= d."""
    ks = [k for k in series if k <= d]
    return (max(ks), series[max(ks)]) if ks else None


def compute() -> dict:
    vni = _vni()
    days = sorted(d for d in vni if BASE_YTD <= d <= END)
    first26 = min(d for d in days if d >= "2026-01-01")
    last = max(days)
    names = {r["symbol"]: r for r in _r(OUT / "universe.csv")}
    sh = {r["symbol"]: float(r["listed_share"]) for r in _r(OUT / "shares.csv") if r.get("listed_share") not in (None, "", "None")}
    px: dict[str, dict[str, float]] = {}
    for r in _r(OUT / "prices.csv"):
        px.setdefault(r["symbol"], {})[r["time"]] = float(r["close"])
    status = {r["symbol"]: r for r in _r(OUT / "status.csv")}

    rows, missing = [], []
    for s in sorted(names):
        p = px.get(s)
        if not p:
            missing.append({"symbol": s, "reason": status.get(s, {}).get("status", "chưa lấy")})
            continue
        ds = sorted(p)
        rets = [(ds[i], 100 * (p[ds[i]] / p[ds[i - 1]] - 1)) for i in range(1, len(ds))]
        gaps = [f"{d}:{x:+.1f}" for d, x in rets if abs(x) > GAP]
        row = {"symbol": s, "name": names[s]["name"], "icb_code2": names[s]["icb_code2"], "first_bar": ds[0],
               "last_bar": ds[-1], "gaps": " ".join(gaps), "listed_share": sh.get(s, "")}
        for tag, d0 in (("ytd", BASE_YTD), ("s1", first26)):
            # chỉ so sánh nếu mã đã có giao dịch tại/ trước mốc (đã niêm yết)
            a = _at(p, d0) if ds[0] <= d0 else None
            for etag, d1 in (("q3", END_Q3), ("now", last)):
                b = _at(p, d1)
                key = f"{tag}_{etag}"
                row[f"pct_{key}"] = round(100 * (b[1] / a[1] - 1), 2) if a and b else ""
            row[f"c0_{tag}"] = a[1] if a else ""
        b = _at(p, last)
        row["c_now"], row["c_now_date"] = (b[1], b[0]) if b else ("", "")
        row["stale"] = int(bool(b) and b[0] < last)
        rows.append(row)

    def stats(key: str) -> dict:
        xs = [r[f"pct_{key}"] for r in rows if r[f"pct_{key}"] != ""]
        below = sum(x < 0 for x in xs)
        return {"n": len(xs), "below": below, "pct_below": round(100 * below / len(xs), 1),
                "flat": sum(x == 0 for x in xs), "above": sum(x > 0 for x in xs),
                "median_pct": round(statistics.median(xs), 2), "mean_pct": round(statistics.mean(xs), 2),
                "down_20_or_more": sum(x <= -20 for x in xs), "up_20_or_more": sum(x >= 20 for x in xs)}

    summ = {"universe": len(names), "with_prices": len(rows), "missing": missing, "first_session_2026": first26,
            "last_session": last, "vni": {BASE_YTD: vni[BASE_YTD], first26: vni[first26], END_Q3: vni[END_Q3], last: vni[last]}}
    for key in ("ytd_q3", "ytd_now", "s1_q3", "s1_now"):
        summ[key] = stats(key)

    # đóng góp điểm (xấp xỉ, vốn hoá đầy đủ, số CP niêm yết hiện tại), mốc 31/12/2025 -> last và -> 30/09
    for etag, d1 in (("now", last), ("q3", END_Q3)):
        pool = [r for r in rows if r["c0_ytd"] != "" and r["listed_share"] != "" and r[f"pct_ytd_{etag}"] != ""]
        cap0 = sum(r["c0_ytd"] * r["listed_share"] for r in pool)
        v0 = vni[BASE_YTD]
        for r in pool:
            r[f"w0_pct"] = round(100 * r["c0_ytd"] * r["listed_share"] / cap0, 3)
            r[f"pts_{etag}"] = round(v0 * (r["c0_ytd"] * r["listed_share"] / cap0) * r[f"pct_ytd_{etag}"] / 100, 2)
        tot = sum(r[f"pts_{etag}"] for r in pool)
        ranked = sorted(pool, key=lambda r: r[f"pts_{etag}"])
        summ[f"points_{etag}"] = {
            "approx_total_pts": round(tot, 1), "actual_vni_pts": round(vni[d1] - v0, 2), "pool": len(pool),
            "top_up": [(r["symbol"], r[f"pts_{etag}"], r[f"pct_ytd_{etag}"], r["w0_pct"]) for r in ranked[::-1][:10]],
            "top_down": [(r["symbol"], r[f"pts_{etag}"], r[f"pct_ytd_{etag}"], r["w0_pct"]) for r in ranked[:10]],
            "top10_weight_pct": round(sum(sorted((r["w0_pct"] for r in pool), reverse=True)[:10]), 1),
        }
        for grp, members in (("vingroup", ("VIC", "VHM", "VRE", "VPL")),):
            g = [r for r in pool if r["symbol"] in members]
            gp = sum(r[f"pts_{etag}"] for r in g)
            summ[f"points_{etag}"][grp] = {"members": [r["symbol"] for r in g], "pts": round(gp, 1),
                                           "rest_pts": round(tot - gp, 1),
                                           "weight_pct": round(sum(r["w0_pct"] for r in g), 1)}

    # độ rộng theo ngày: % mã dưới giá 31/12/2025, trung vị, so với VN-Index
    daily = []
    base = {r["symbol"]: r["c0_ytd"] for r in rows if r["c0_ytd"] != ""}
    for d in days[1:]:
        xs = []
        for s, c0 in base.items():
            b = _at(px[s], d)
            if b:
                xs.append(100 * (b[1] / c0 - 1))
        daily.append({"date": d, "n": len(xs), "pct_below": round(100 * sum(x < 0 for x in xs) / len(xs), 1),
                      "median_pct": round(statistics.median(xs), 2),
                      "vnindex": vni[d], "vnindex_pct": round(100 * (vni[d] / vni[BASE_YTD] - 1), 2)})
    _w(OUT / "breadth_daily.csv", daily, list(daily[0]))
    summ["daily_pct_below_range"] = [min(x["pct_below"] for x in daily), max(x["pct_below"] for x in daily)]
    summ["gap_flagged_symbols"] = sum(1 for r in rows if r["gaps"])

    cols = ["symbol", "name", "icb_code2", "first_bar", "last_bar", "c0_ytd", "c0_s1", "c_now", "c_now_date", "stale",
            "pct_ytd_q3", "pct_ytd_now", "pct_s1_q3", "pct_s1_now", "listed_share", "w0_pct", "pts_q3", "pts_now", "gaps"]
    _w(OUT / "breadth_2026.csv", rows, cols)
    summ["method"] = __doc__.split("Quy ước tính")[1].strip()
    (OUT / "summary.json").write_text(json.dumps(summ, ensure_ascii=False, indent=1), encoding="utf-8")
    return summ


if __name__ == "__main__":
    import pathlib, sys  # noqa: E401
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    cmd = sys.argv[1]
    if cmd == "universe":
        universe()
    elif cmd == "shares":
        shares()
    elif cmd == "fetch":
        fetch()
    elif cmd == "compute":
        s = compute()
        print(json.dumps({k: v for k, v in s.items() if k not in ("method", "missing")}, ensure_ascii=False, indent=1))
        print("missing:", len(s["missing"]))
