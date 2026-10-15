"""Dữ liệu cho cảnh biểu đồ (theme "chart", kênh Biểu Đồ Biết Nói): nến ngày + chỉ báo, TÍNH Ở PYTHON rồi nhúng vào
data.js -- engine JS chỉ vẽ, không tính (một nguồn sự thật, kiểm thử được).

Nguồn: data/ck/<series>_1d.csv (time,open,high,low,close,volume), lấy bằng vnstock (VCI) -- `python motion/long/chartdata.py
fetch VNINDEX`. Bản Cộng đồng của vnstock trả tối đa 8 năm. Giấy phép vnstock không cấp quyền với dữ liệu: chỉ dùng
dữ liệu QUÁ KHỨ để minh hoạ cách đọc chỉ báo, ghi "Dữ liệu: HOSE · truy xuất qua Vnstock"
(docs/channels/chung-khoan/2026-10-06-research.md, mục 4).

Cảnh: {"type": "candles", "series": "vnindex", "from": "2025-03-01", "to": "2025-05-15",
       "ind": [{"k": "sma", "n": 20}, {"k": "ema", "n": 50}], ...} -> attach() thêm "bars" + "lines".
Chỉ báo tính trên TOÀN lịch sử rồi mới cắt cửa sổ: MA20 ngày đầu cửa sổ đã đủ 20 phiên trước đó.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "ck"


def load(series: str) -> list[dict]:
    with open(DATA / f"{series.lower()}_1d.csv", encoding="utf-8") as f:
        return [{"t": r["time"][:10], "o": float(r["open"]), "h": float(r["high"]), "l": float(r["low"]),
                 "c": float(r["close"]), "v": float(r["volume"])} for r in csv.DictReader(f)]


def sma(xs: list[float], n: int) -> list[float | None]:
    out, s = [], 0.0
    for i, x in enumerate(xs):
        s += x
        if i >= n:
            s -= xs[i - n]
        out.append(s / n if i >= n - 1 else None)
    return out


def ema(xs: list[float], n: int) -> list[float | None]:
    """EMA chuẩn: hệ số 2/(n+1), mồi bằng SMA n phiên đầu."""
    k, out, prev = 2 / (n + 1), [], None
    for i, x in enumerate(xs):
        if i < n - 1:
            out.append(None)
            continue
        prev = sum(xs[:n]) / n if i == n - 1 else x * k + prev * (1 - k)
        out.append(prev)
    return out


IND = {"sma": sma, "ema": ema}


def weekly(rows: list[dict]) -> list[dict]:
    """Nến ngày -> nến TUẦN theo tuần ISO (T2→T6): mở = mở phiên đầu, cao/thấp = max/min, đóng = đóng phiên cuối, KL = tổng.
    Nhãn "t" = ngày của phiên ĐẦU TIÊN trong tuần (thường là thứ Hai) -- marks của cảnh nến tuần neo vào ngày này.
    "days" = số phiên trong tuần (tuần lễ / tuần dở dang ở cuối dữ liệu có ít phiên hơn)."""
    from datetime import date
    out: list[dict] = []
    key = None
    for r in rows:
        k = date.fromisoformat(r["t"]).isocalendar()[:2]
        if k != key:
            key = k
            out.append({"t": r["t"], "o": r["o"], "h": r["h"], "l": r["l"], "c": r["c"], "v": r["v"], "days": 1})
            continue
        w = out[-1]
        w["h"], w["l"], w["c"], w["v"], w["days"] = max(w["h"], r["h"]), min(w["l"], r["l"]), r["c"], w["v"] + r["v"], w["days"] + 1
    return out


TF = {"1d": lambda rows: rows, "1w": weekly}


def attach(scene: dict) -> dict:
    """tf: "1d" (mặc định) | "1w" -- nến tuần gộp từ nến ngày TRONG PYTHON (engine không đổi). Với "1w", cửa sổ from..to lấy
    mọi tuần có phiên đầu tuần nằm trong [tuần chứa `from`, `to`]; chỉ báo tính trên nến tuần (MA20 tuần = 20 tuần)."""
    tf = scene.get("tf", "1d")
    if tf not in TF:
        raise ValueError(f"tf lạ {tf!r} (chỉ có {', '.join(TF)})")
    rows = TF[tf](load(scene.get("series", "vnindex")))
    frm = scene["from"]
    if tf == "1w":   # tuần chứa `from` tính cả khi `from` rơi giữa tuần (nhãn tuần = phiên đầu tuần, có thể < from)
        from datetime import date
        wk = date.fromisoformat(frm).isocalendar()[:2]
        frm = next((r["t"] for r in rows if date.fromisoformat(r["t"]).isocalendar()[:2] >= wk), frm)
    closes = [r["c"] for r in rows]
    lines = []
    for spec in scene.get("ind", []):
        vals = IND[spec["k"]](closes, spec["n"])
        lines.append({**spec, "vals": vals})
    idx = [i for i, r in enumerate(rows) if frm <= r["t"] <= scene["to"]]
    if not idx:
        raise ValueError(f"không có phiên nào trong {scene['from']}..{scene['to']}")
    a, b = idx[0], idx[-1] + 1
    scene["bars"] = [[r["t"], r["o"], r["h"], r["l"], r["c"], r["v"]] for r in rows[a:b]]
    scene["lines"] = [{k: v for k, v in ln.items() if k != "vals"} | {"vals": [None if x is None else round(x, 2) for x in ln["vals"][a:b]]}
                      for ln in lines]
    return scene


def fetch(symbol: str) -> Path:
    from vnstock import Quote   # chỉ cần khi lấy dữ liệu mới
    df = Quote(symbol=symbol, source="VCI").history(start="2000-01-01", end="2100-01-01", interval="1D")
    df["time"] = df["time"].astype(str).str[:10]
    out = DATA / f"{symbol.lower()}_1d.csv"
    DATA.mkdir(parents=True, exist_ok=True)
    df[["time", "open", "high", "low", "close", "volume"]].to_csv(out, index=False)
    return out



# ---------- "race": so sánh nhiều kênh tài sản trên cùng trục % (video so sánh kênh đầu tư) ----------
def _series(key: str) -> dict[str, float]:
    """Giá trị theo ngày của một kênh, dạng {ngày: giá}. Vàng SJC: trả cặp (mua, bán) để tính đúng phía nhà đầu tư."""
    if key == "vnindex":
        return {r["t"]: r["c"] for r in load("vnindex")}
    p = DATA / {"btc": "btc_usd_1d.csv", "sjc": "sjc_1d.csv"}[key]   # Bitcoin theo giá USD (xem finance_data.btc)
    with open(p, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if key == "sjc":
        return overrides(fallbacks({r["time"]: (float(r["buy"]), float(r["sell"])) for r in rows}))
    return {r["time"]: float(r["close"]) for r in rows}


def fallbacks(series: dict, gap: int = 14, tail: int = 10, tol: float = 0.05, side: int = 2) -> dict:
    """Bỏ "ngày giả" của trang SJC: với ngày không lưu, trang trả NGUYÊN giá của một ngày khác -- giá hôm tải (01/01/2020,
    24/06/2024 = 140,5 triệu) hoặc giá một ngày đầu tháng trước đó (04/08/2020 = đúng 02/07/2020, 01/11/2024 = đúng 01/10).
    Nghi vấn: cặp (mua, bán) trùng y hệt một ngày SỚM hơn ≥ `gap` ngày, hoặc trùng một trong `tail` dòng cuối (giá hôm tải)
    dù cũ hơn 60 ngày. Chỉ bỏ nghi vấn lệch > `tol` so với trung vị `side` điểm kề mỗi bên (không tính điểm nghi vấn khác
    và điểm cùng giá) -- giá đứng yên nhiều tuần (giữa 2024) vẫn giữ.
    Thay cho despike + outliers (07/10/2026): hai bộ lọc đó bỏ nhầm cú tăng thật (08/2020, 04/2025, 10/2025) khi dữ liệu
    dày lên theo tuần."""
    from datetime import date
    from statistics import median
    keys = sorted(series)
    val = lambda k: series[k][0] if isinstance(series[k], tuple) else series[k]
    day = lambda k: date.fromisoformat(k)
    first: dict = {}
    for k in keys:
        first.setdefault(series[k], day(k))
    recent = {series[k] for k in keys[-tail:]}
    last = day(keys[-1]) if keys else None
    sus = {k for k in keys if (day(k) - first[series[k]]).days >= gap
           or (k not in keys[-tail:] and series[k] in recent and (last - day(k)).days > 60)}
    ok = [k for k in keys if k not in sus]
    bad = set()
    for k in sus:
        before = [val(x) for x in reversed(ok) if x < k and series[x] != series[k]][:side]
        after = [val(x) for x in ok if x > k and series[x] != series[k]][:side]
        near = before + after
        if near and abs(val(k) / median(near) - 1) > tol:
            bad.add(k)
    return {k: v for k, v in series.items() if k not in bad}


def overrides(series: dict) -> dict:
    """Sửa tay theo báo chí (`data/ck/sjc_overrides.csv`: time,buy,sell,source). Ô buy trống = bỏ ngày đó."""
    p = DATA / "sjc_overrides.csv"
    if not p.exists():
        return series
    out = dict(series)
    with open(p, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["buy"].strip():
                out[r["time"]] = (float(r["buy"]), float(r["sell"]))
            else:
                out.pop(r["time"], None)
    return out


def outliers(series: dict, tol: float = 0.10) -> dict:
    """Chuỗi THƯA (vàng SJC trước 2026: 2 điểm/tháng): bỏ điểm lệch > `tol` so với trung điểm hai điểm kề bên trong khi hai
    điểm kề bên gần nhau (< `tol`) -- vd 01/01/2020 hay 03/10/2023 mang đúng "giá hôm nay" 140,5 triệu do trang SJC trả thay."""
    keys = sorted(series)
    val = lambda k: series[k][0] if isinstance(series[k], tuple) else series[k]
    bad = set()
    for i in range(1, len(keys) - 1):
        a, b, c = val(keys[i - 1]), val(keys[i]), val(keys[i + 1])
        if abs(a / c - 1) < tol and abs(b / ((a + c) / 2) - 1) > tol:
            bad.add(keys[i])
    return {k: v for k, v in series.items() if k not in bad}


def despike(series: dict, jump: float = 0.08, back: float = 0.03, run: int = 3) -> dict:
    """Bỏ "gai" giả: trang SJC trả GIÁ HÔM NAY cho ngày nó không lưu (vd 17 & 20/04/2026 = đúng giá đầu tháng 10).
    Một chuỗi ≤ `run` ngày lệch > `jump` so với ngày hợp lệ trước đó, rồi ngày kế tiếp quay lại trong `back` -> bỏ chuỗi đó."""
    keys = sorted(series)
    val = lambda k: series[k][0] if isinstance(series[k], tuple) else series[k]
    bad, i = set(), 1
    while i < len(keys):
        prev = val(keys[i - 1])
        if abs(val(keys[i]) / prev - 1) > jump:
            for k in range(1, run + 1):
                j = i + k
                if j < len(keys) and abs(val(keys[j]) / prev - 1) <= back:
                    bad.update(keys[i:j])
                    i = j
                    break
            else:
                i += 1
            continue
        i += 1
    return {k: v for k, v in series.items() if k not in bad}


def _deposit(s: dict, d0: str, d: str) -> float:
    """Hệ số tiền gửi từ d0 tới d. "rate": lãi đơn một kỳ hạn; "rates": [[ngày, lãi năm], …] = sổ 12 tháng cuộn mỗi năm
    (đáo hạn nhập lãi vào gốc, kỳ mới theo mức của mốc gần nhất) -- lãi kỳ đang chạy tính theo ngày, chưa đáo hạn."""
    from datetime import date
    t0, t = date.fromisoformat(d0), date.fromisoformat(d)
    if "rate" in s:
        return 1 + s["rate"] * (t - t0).days / 365
    sched = sorted((date.fromisoformat(a), r) for a, r in s["rates"])
    f, start = 1.0, t0
    while True:
        rate = [r for a, r in sched if a <= start][-1]
        end = date(start.year + 1, start.month, min(start.day, 28))
        if t < end:
            return f * (1 + rate * (t - start).days / 365)
        f, start = f * (1 + rate), end


def attach_race(scene: dict) -> dict:
    """scene: {"from", "to", "series": [{"key": "vnindex"|"sjc"|"btc"|"deposit", "rate"?: 0.068, "label", "color"?}]}
    -> scene["dates"] (lịch = các phiên VN-Index trong khoảng) + mỗi series "vals" = % lãi/lỗ so với ngày đầu.
    Vàng: MUA ở giá bán ra của SJC ngày đầu, định giá bằng giá SJC mua vào -> đường vàng bắt đầu âm đúng bằng chênh lệch
    mua-bán (người mua vàng lỗ ngay khi vừa mua). Tiết kiệm: lãi đơn theo ngày với lãi suất năm `rate` (không kỳ hạn
    ngắn hơn, không tái tục -- ghi rõ "giả định" trên màn hình). Ngày thiếu giá (nghỉ lễ, cuối tuần): lấy giá gần nhất trước đó."""
    # Chuỗi TỰ TÍNH sẵn (ví dụ giả định, không theo lịch giao dịch — B1 "mua hay thuê"): gen_scenes nhúng "dates" (nhãn trục)
    # + "vals" từng series -> giữ nguyên, không đụng dữ liệu thị trường.
    if scene.get("dates") and scene.get("series") and all("vals" in s and "key" not in s for s in scene["series"]):
        if any(len(s["vals"]) != len(scene["dates"]) for s in scene["series"]):
            raise ValueError("race tự tính: mỗi series phải có đúng len(dates) giá trị")
        return scene
    # Mốc gốc = ngày `from` (vd 01/01): mỗi kênh lấy giá gần nhất TẠI/TRƯỚC ngày đó (VN-Index: phiên 31/12; vàng: niêm yết
    # ngày đó) -- không lấy phiên giao dịch đầu tiên (05/01/2026 giá vàng đã khác hẳn).
    d0 = scene["from"]
    days = [d0] + [r["t"] for r in load("vnindex") if d0 < r["t"] <= scene["to"]]
    if len(days) < 2:
        raise ValueError("không có phiên nào trong khoảng")
    scene["dates"] = days
    from datetime import date
    for s in scene["series"]:
        if s["key"] == "deposit":
            s["vals"] = [round(100 * (_deposit(s, d0, d) - 1), 2) for d in days]
            continue
        src = _series(s["key"])
        keys = sorted(src)
        def at(d, _k=keys, _s=src, _interp=s.get("interp")):
            prev = [k for k in _k if k <= d]
            if not prev:
                raise ValueError(f"{s['key']}: không có giá trước {d}")
            a = prev[-1]
            nxt = [k for k in _k if k > d]
            if not _interp or a == d or not nxt:
                return _s[a]
            # chuỗi thưa (vàng SJC trước 2026: 2 điểm/tháng) -> nội suy tuyến tính theo ngày, tránh hình bậc thang
            b = nxt[0]
            w = (date.fromisoformat(d) - date.fromisoformat(a)).days / (date.fromisoformat(b) - date.fromisoformat(a)).days
            mix = lambda x, y: x + (y - x) * w
            return tuple(mix(x, y) for x, y in zip(_s[a], _s[b])) if isinstance(_s[a], tuple) else mix(_s[a], _s[b])
        base = at(d0)
        if s["key"] == "sjc":
            s["vals"] = [round(100 * (at(d)[0] / base[1] - 1), 2) for d in days]
        else:
            s["vals"] = [round(100 * (at(d) / base - 1), 2) for d in days]
    return scene


# ---------- "breadth" + "basket": độ rộng & độ tập trung HOSE (dữ liệu motion/long/breadth.py, data/ck/breadth_2026/) ----------
# Vũ trụ = các mã có giá đóng cửa 31/12/2025 (c0_ytd) -- đúng 400 mã như summary.json (loại 6 mã niêm yết trong năm).
# % thay đổi tại ngày d = giá đóng cửa gần nhất <= d / c0_ytd - 1, làm tròn 2 số lẻ (cùng cách breadth.py đếm "dưới/đứng/trên").
BREADTH_DIR = "breadth_2026"
BASE_YTD = "2025-12-31"
# thang màu 9 bậc dùng chung cho chấm (breadth) và ô (basket): -4..-1 đỏ (giảm), 0 xám (đứng giá), 1..4 xanh (tăng).
# Ngưỡng |%|: < 5 -> bậc 1 · 5–15 -> 2 · 15–30 -> 3 · ≥ 30 -> 4.
BUCKET_EDGES = (5.0, 15.0, 30.0)


def bucket(p: float) -> int:
    """% thay đổi -> bậc màu -4..4. Mọi mã giảm (dù 0,01%) đều đỏ, mọi mã tăng đều xanh: số chấm đỏ = số mã "dưới giá"."""
    if p == 0:
        return 0
    a, s = abs(p), 1 if p > 0 else -1
    return s * (1 + sum(a >= e for e in BUCKET_EDGES))


def vn_num(x: float, nd: int = 1, sign: bool = True) -> str:
    """Số kiểu Việt: dấu phẩy thập phân, chấm ngăn nghìn, dấu trừ thật (−)."""
    s = f"{abs(x):,.{nd}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return (("+" if x > 0 else "−" if x < 0 else "") if sign else ("−" if x < 0 else "")) + s


def _bd() -> Path:
    return DATA / BREADTH_DIR


def _csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


_PX: dict = {}


def _prices() -> dict[str, tuple[list[str], list[float]]]:
    """prices.csv -> {mã: (ngày tăng dần, giá)}; nhớ đệm theo đường dẫn (test đổi DATA thì đọc lại)."""
    key = str(_bd())
    if key not in _PX:
        tmp: dict[str, dict[str, float]] = {}
        for r in _csv(_bd() / "prices.csv"):
            tmp.setdefault(r["symbol"], {})[r["time"][:10]] = float(r["close"])
        _PX.clear()
        _PX[key] = {s: (sorted(d), [d[k] for k in sorted(d)]) for s, d in tmp.items()}
    return _PX[key]


def _close_at(ds: list[str], cs: list[float], d: str) -> float | None:
    import bisect
    i = bisect.bisect_right(ds, d)
    return cs[i - 1] if i else None


def _universe() -> list[dict]:
    """Các mã so được với mốc 31/12/2025: symbol, c0 (giá 31/12/2025), shares (số CP niêm yết)."""
    out = []
    for r in _csv(_bd() / "breadth_2026.csv"):
        if r.get("c0_ytd", "") == "":
            continue
        sh = r.get("listed_share")
        out.append({"symbol": r["symbol"], "c0": float(r["c0_ytd"]), "shares": float(sh) if sh not in (None, "", "None") else None})
    return out


def snapshot(date: str) -> list[dict]:
    """[{symbol, pct, bucket, close, c0, cap, cap0}] tại ngày `date` (giá gần nhất <= date) cho toàn vũ trụ 400 mã."""
    px = _prices()
    out = []
    for u in _universe():
        ds, cs = px.get(u["symbol"], ([], []))
        c = _close_at(ds, cs, date) if date >= BASE_YTD else None
        if c is None:
            continue
        p = round(100 * (c / u["c0"] - 1), 2)
        sh = u["shares"]
        out.append({"symbol": u["symbol"], "pct": p, "bucket": bucket(p), "close": c, "c0": u["c0"],
                    "cap": c * sh if sh else None, "cap0": u["c0"] * sh if sh else None})
    return out


def breadth_counts(snap: list[dict]) -> dict:
    import statistics
    xs = [s["pct"] for s in snap]
    below = sum(x < 0 for x in xs)
    return {"n": len(xs), "below": below, "flat": sum(x == 0 for x in xs), "above": sum(x > 0 for x in xs),
            "pct_below": round(100 * below / len(xs), 1) if xs else 0.0,
            "median": round(statistics.median(xs), 2) if xs else 0.0}


def vni_pct(date: str) -> float:
    """% VN-Index tại ngày `date` (phiên gần nhất <= date) so với đóng cửa 31/12/2025."""
    rows = load("vnindex")
    base = [r["c"] for r in rows if r["t"] <= BASE_YTD][-1]
    cur = [r["c"] for r in rows if r["t"] <= date][-1]
    return round(100 * (cur / base - 1), 2)


def attach_breadth(scene: dict) -> dict:
    """scene: {"date"?: "2026-09-30", "animate"?: {"from", "to"?, "every"?: 5, "at", "until"}}
    -> "dots": [[pct, bậc]…] xếp từ giảm mạnh nhất -> tăng mạnh nhất (theo ngày `date`), "stats" (đếm, trung vị, VN-Index %),
    và nếu có animate: "frames": [{"d", "b": [bậc theo đúng thứ tự chấm], "below", "n", "pb" (% dưới), "vni"}] (các phiên trong khoảng,
    cách `every` phiên, luôn có phiên cuối) để JS đổi màu chấm theo ngày. Mã ("syms") chỉ để kiểm, không lên màn hình."""
    if scene.get("base") == "prev":
        return _attach_breadth_prev(scene)
    d = scene.get("date", "2026-09-30")
    snap = sorted(snapshot(d), key=lambda s: (s["pct"], s["symbol"]))
    if not snap:
        raise ValueError(f"breadth: không có giá nào tại {d}")
    scene["date"] = d
    scene["dots"] = [[s["pct"], s["bucket"]] for s in snap]
    scene["syms"] = [s["symbol"] for s in snap]
    scene["stats"] = {**breadth_counts(snap), "vni": vni_pct(d), "date": d}
    an = scene.get("animate")
    if an:
        days = [r["date"] for r in _csv(_bd() / "breadth_daily.csv") if an["from"] <= r["date"] <= an.get("to", d)]
        if not days:
            raise ValueError(f"breadth.animate: không có phiên nào trong {an['from']}..{an.get('to', d)}")
        every = max(1, int(an.get("every", 5)))
        pick = days[::every]
        if pick[-1] != days[-1]:
            pick.append(days[-1])
        frames = []
        for day in pick:
            fs = {s["symbol"]: s for s in snapshot(day)}
            c = breadth_counts(list(fs.values()))
            frames.append({"d": day, "b": [fs[s]["bucket"] if s in fs else 0 for s in scene["syms"]],
                           "below": c["below"], "n": c["n"], "pb": c["pct_below"], "vni": vni_pct(day)})
        scene["frames"] = frames
    return scene


# ---------- breadth theo % TRONG NGÀY (base "prev"): mỗi mã so với phiên giao dịch liền trước CỦA CHÍNH NÓ ----------
# Vũ trụ = mọi mã trong prices.csv có phiên đúng ngày `date` và có phiên trước đó (09/03/2026: 395 mã, giảm 368 · tăng 11 ·
# đứng 16, trung vị −6,80% -- khớp factcheck C2). Thang 9 bậc riêng cho biên độ ±7%: |%| < 1 -> 1 · 1–3 -> 2 · 3–6,5 -> 3 ·
# ≥ 6,5 -> 4 (bậc −4 ≈ sát sàn −7%; giá đã điều chỉnh nên không dùng để đếm "đúng giá sàn").
DAY_EDGES = (1.0, 3.0, 6.5)


def bucket_day(p: float) -> int:
    if p == 0:
        return 0
    a, s = abs(p), 1 if p > 0 else -1
    return s * (1 + sum(a >= e for e in DAY_EDGES))


def day_snapshot(date: str) -> list[dict]:
    """[{symbol, pct, bucket, close, prev}] -- mã có phiên đúng `date`, % so với phiên trước của chính mã đó."""
    import bisect
    out = []
    for sym, (ds, cs) in _prices().items():
        i = bisect.bisect_left(ds, date)
        if i < len(ds) and ds[i] == date and i > 0:
            p = round(100 * (cs[i] / cs[i - 1] - 1), 2)
            out.append({"symbol": sym, "pct": p, "bucket": bucket_day(p), "close": cs[i], "prev": cs[i - 1]})
    return out


def vni_day_pct(date: str) -> float:
    """% VN-Index phiên `date` so với phiên liền trước."""
    rows = load("vnindex")
    i = max(k for k, r in enumerate(rows) if r["t"] <= date)
    return round(100 * (rows[i]["c"] / rows[i - 1]["c"] - 1), 2)


def _attach_breadth_prev(scene: dict) -> dict:
    d = scene.get("date")
    if not d:
        raise ValueError("breadth base 'prev': cần 'date'")
    if scene.get("animate"):
        raise ValueError("breadth base 'prev': chưa hỗ trợ animate")
    snap = sorted(day_snapshot(d), key=lambda s: (s["pct"], s["symbol"]))
    if not snap:
        raise ValueError(f"breadth: không có mã nào giao dịch ngày {d}")
    scene["dots"] = [[s["pct"], s["bucket"]] for s in snap]
    scene["syms"] = [s["symbol"] for s in snap]
    st = {**breadth_counts(snap), "vni": vni_day_pct(d), "date": d, "base": "prev"}
    scene["stats"] = st
    scene.setdefault("palette", "board")
    scene.setdefault("legend", {"title": "% TRONG NGÀY · XANH LƠ ≈ SÀN −7%", "lo": "≤ −6,5%", "hi": "≥ +6,5%"})
    scene.setdefault("countNote", f"{vn_num(st['pct_below'], sign=False)}% · SO VỚI PHIÊN TRƯỚC")
    return scene


def squarify(values: list[float], x: float, y: float, w: float, h: float) -> list[tuple[float, float, float, float]]:
    """Treemap "squarified" (Bruls, Huizing, van Wijk 2000): diện tích ô tỉ lệ đúng với giá trị, ô gần vuông nhất có thể.
    `values` phải xếp GIẢM dần; trả [(x, y, w, h)] cùng thứ tự. Tất định (không ngẫu nhiên)."""
    tot = float(sum(values))
    if not values or tot <= 0:
        return [(x, y, 0.0, 0.0) for _ in values]
    areas = [v * w * h / tot for v in values]
    out: list[tuple[float, float, float, float]] = []

    def worst(row: list[float], side: float) -> float:
        s = sum(row)
        if s <= 0 or side <= 0 or min(row) <= 0:
            return float("inf")
        return max(side * side * max(row) / (s * s), s * s / (side * side * min(row)))

    i, row = 0, []
    while i < len(areas):
        a = areas[i]
        if not row or worst(row + [a], min(w, h)) <= worst(row, min(w, h)):
            row.append(a)
            i += 1
        else:
            x, y, w, h = _lay(row, x, y, w, h, out)
            row = []
    if row:
        _lay(row, x, y, w, h, out)
    return out


def _lay(row, x, y, w, h, out):
    s = sum(row)
    if w >= h:                       # cột dọc sát cạnh trái của phần còn lại
        cw = s / h if h else 0.0
        yy = y
        for a in row:
            rh = a / cw if cw else 0.0
            out.append((x, yy, cw, rh))
            yy += rh
        return x + cw, y, w - cw, h
    rh = s / w if w else 0.0         # hàng ngang sát cạnh trên
    xx = x
    for a in row:
        rw = a / rh if rh else 0.0
        out.append((xx, y, rw, rh))
        xx += rw
    return x, y + rh, w, h - rh


BASKET_BOX = (150.0, 178.0, 1090.0, 722.0)   # x, y, w, h trên khung 1920x1080 (cột phải 1290..1820 cho thẻ chú thích)


def attach_basket(scene: dict) -> dict:
    """scene: {"date"?: "2026-09-30", "groupSmall"?: 200, "labels"?: 10 | ["VIC", …], "box"?: [x, y, w, h]}
    Vốn hoá = giá đóng cửa tại ngày × số cổ phiếu niêm yết hiện tại (cùng quy ước breadth.py; ngày 31/12/2025 khớp cột w0_pct).
    -> "rects": [[mã, x, y, w, h, tỉ trọng %, % thay đổi, bậc màu, hạng]…] xếp vốn hoá giảm dần (ô gom N mã nhỏ nhất có mã "*",
       "hạng" = N, % thay đổi = theo vốn hoá cả nhóm), "labels": các mã được ghi tên trong ô,
       "stats": {"n", "top": [[mã, %]…10], "top10" %, "groupN", "group" %}."""
    d = scene.get("date", "2026-09-30")
    snap = [s for s in snapshot(d) if s["cap"]]
    if not snap:
        raise ValueError(f"basket: không có vốn hoá nào tại {d}")
    snap.sort(key=lambda s: (-s["cap"], s["symbol"]))
    tot = sum(s["cap"] for s in snap)
    share = {s["symbol"]: 100 * s["cap"] / tot for s in snap}
    gN = min(int(scene.get("groupSmall") or 0), max(0, len(snap) - 1))
    keep, grp = (snap[:-gN], snap[-gN:]) if gN else (snap, [])
    items = [(s["symbol"], s["cap"], s["pct"], i + 1) for i, s in enumerate(keep)]
    if grp:
        gcap = sum(s["cap"] for s in grp)
        items.append(("*", gcap, round(100 * (gcap / sum(s["cap0"] for s in grp) - 1), 2), len(grp)))
        items.sort(key=lambda t: -t[1])
    box = scene.get("box") or BASKET_BOX
    rects = squarify([t[1] for t in items], *box)
    scene["date"] = d
    scene["rects"] = [[sym, round(x, 2), round(y, 2), round(w, 2), round(h, 2), round(100 * cap / tot, 3), pct, bucket(pct), rank]
                      for (sym, cap, pct, rank), (x, y, w, h) in zip(items, rects)]
    lab = scene.get("labels", 10)
    scene["labels"] = [s["symbol"] for s in snap[:lab]] if isinstance(lab, int) else list(lab)
    scene["stats"] = {"n": len(snap), "top": [[s["symbol"], round(share[s["symbol"]], 2)] for s in snap[:10]],
                      "top10": round(sum(share[s["symbol"]] for s in snap[:10]), 2), "groupN": len(grp),
                      "group": round(sum(share[s["symbol"]] for s in grp), 2)}
    return scene


if __name__ == "__main__":
    import pathlib, sys  # noqa: E401
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    if sys.argv[1] == "fetch":
        print(fetch(sys.argv[2]))
