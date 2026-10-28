"""Merge the CSVs exported from YouTube Studio into one compact summary for LLMs (pure python, no browser).

Input: the folder `webauto studio collect` wrote (manifest.json + one sub-folder per report/period).
Output: summary.md (short, written to be read by a model instead of raw tables), summary.json (all the
numbers) and videos.csv (one wide row per video, for tools).

Everything here is derived from the exported numbers; thresholds that classify (Short vs long, "enough
impressions") are explicit constants below, not facts from YouTube.
"""
import csv
import json
import statistics
from datetime import date, datetime
from pathlib import Path

SHORT_MAX_S = 180  # YouTube's Shorts limit; a video at or under it is counted as a Short (a heuristic)
MIN_IMPRESSIONS = 500  # below this a click-through rate is mostly noise
TOP_N = 7  # rows per ranking table; keeps summary.md around 10 KB for a ~140-video channel
PERIOD_ORDER = ["7d", "28d", "90d", "365d", "lifetime"]
# export column -> short key
METRICS = {
    "Views": "views",
    "Watch time (hours)": "watch_h",
    "Subscribers": "subs",
    "Thumbnail impressions": "impressions",
    "Thumbnail click-through rate (%)": "ctr",
    "Average view duration": "avd_s",
    "Average percentage viewed (%)": "avp",
}


def num(s):
    """'1234' / '3.2' -> float; '', '—', '-' -> None."""
    s = (s or "").strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def parse_date(s):
    for fmt in ("%b %d, %Y", "%Y-%m-%d", "%d %b %Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except (ValueError, AttributeError):
            pass
    return None


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    return (rows[0], rows[1:]) if rows else ([], [])


def clean(header, rows):
    """Full-width rows only. Returns (rows, truncated): Studio appends 'Showing top 500 results' when it cut the table."""
    return [r for r in rows if len(r) >= len(header)], any(r and r[0].startswith("Showing top") for r in rows)


def load(folder):
    """{report: {period: {"table": (header, rows), ...}}} from the manifest written by collect."""
    folder = Path(folder)
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    data = {}
    for item in manifest["reports"]:
        if item.get("status") != "ok":
            continue
        files = {}
        for kind, rel in item["files"].items():
            files[kind] = read_csv(folder / rel)
        data.setdefault(item["report"], {})[item["period"]] = files
    return manifest, data


def video_rows(table):
    """Per-video rows of a `videos` table: ([{id, title, published, duration_s, <metrics>}], Total row, truncated)."""
    header, rows = table
    rows, truncated = clean(header, rows)
    idx = {h: i for i, h in enumerate(header)}
    out, total = [], {}
    for r in rows:
        rec = {k: num(r[idx[h]]) for h, k in METRICS.items() if h in idx and idx[h] < len(r)}
        if r[0] == "Total":
            total = rec
            continue
        rec.update(id=r[0], title=r[idx.get("Video title", 1)] if "Video title" in idx else "",
                   published=parse_date(r[idx["Video publish time"]]) if "Video publish time" in idx else None,
                   duration_s=num(r[idx["Duration"]]) if "Duration" in idx else None)
        out.append(rec)
    return out, total, truncated


def merge_videos(data, today=None):
    """One record per video with every period's metrics under rec[period] plus derived fields."""
    today = today or date.today()
    videos, totals, truncated = {}, {}, []
    for period, files in data.get("videos", {}).items():
        if "table" not in files:
            continue
        rows, total, cut = video_rows(files["table"])
        totals[period] = total
        if cut:
            truncated.append(period)
        for r in rows:
            v = videos.setdefault(r["id"], {"id": r["id"]})
            v.update(title=r["title"] or v.get("title", ""), published=r["published"], duration_s=r["duration_s"])
            v[period] = {k: r.get(k) for k in METRICS.values()}
    for v in videos.values():
        d = v.get("duration_s")
        v["format"] = None if d is None else ("short" if d <= SHORT_MAX_S else "long")
        v["age_days"] = (today - v["published"]).days if v.get("published") else None
        for p in PERIOD_ORDER:
            m = v.get(p)
            if m and m.get("views"):
                m["subs_per_1k_views"] = round(1000 * (m["subs"] or 0) / m["views"], 2)
                m["hours_per_1k_views"] = round(1000 * (m["watch_h"] or 0) / m["views"], 2)
    return videos, totals, truncated


def pick_period(videos, preferred=("28d", "lifetime", "90d", "365d", "7d")):
    for p in preferred:
        if any(p in v for v in videos.values()):
            return p
    return None


def rank(videos, period, key, n=TOP_N, reverse=True, min_views=0, min_impr=0):
    pool = []
    for v in videos.values():
        m = v.get(period) or {}
        val = m.get(key)
        if val is None or (m.get("views") or 0) < min_views or (m.get("impressions") or 0) < min_impr:
            continue
        pool.append((val, v))
    pool.sort(key=lambda t: t[0], reverse=reverse)
    return [{"id": v["id"], "title": v["title"][:55], key: val, "views": (v.get(period) or {}).get("views"),
             "format": v["format"], "age_days": v["age_days"]} for val, v in pool[:n]]


def by_format(videos, period):
    out = {}
    for fmt in ("short", "long"):
        ms = [v[period] for v in videos.values() if v.get("format") == fmt and period in v]
        if not ms:
            continue
        views = sum(m["views"] or 0 for m in ms)
        out[fmt] = {
            "videos": len(ms), "views": views,
            "watch_h": round(sum(m["watch_h"] or 0 for m in ms), 1),
            "subs": sum(m["subs"] or 0 for m in ms),
            "median_views": statistics.median([m["views"] or 0 for m in ms]),
            "subs_per_1k_views": round(1000 * sum(m["subs"] or 0 for m in ms) / views, 2) if views else None,
        }
    return out


def by_age(videos, period):
    """Views by how old the video is (days since publish), to see whether fresh uploads or the back catalogue carry the channel."""
    buckets = [("0-7d", 0, 7), ("8-28d", 8, 28), ("29-90d", 29, 90), ("91-365d", 91, 365), (">365d", 366, 10**6)]
    out = []
    tot = sum((v.get(period) or {}).get("views") or 0 for v in videos.values()) or 1
    for name, lo, hi in buckets:
        vs = [v for v in videos.values() if v.get("age_days") is not None and lo <= v["age_days"] <= hi and period in v]
        views = sum(v[period]["views"] or 0 for v in vs)
        out.append({"age": name, "videos": len(vs), "views": views, "share_pct": round(100 * views / tot, 1)})
    return out


def distribution(videos, period):
    vals = sorted((v[period]["views"] or 0) for v in videos.values() if period in v)
    if not vals:
        return {}
    n = len(vals)
    top10 = vals[-max(1, n // 10):]
    return {"videos": n, "median": statistics.median(vals), "mean": round(statistics.mean(vals), 1),
            "p90": vals[int(0.9 * (n - 1))], "max": vals[-1],
            "top10pct_share_pct": round(100 * sum(top10) / (sum(vals) or 1), 1)}


def daily_trend(files):
    """From the `daily` report table: totals, last-7 vs previous-7 and last-28 vs previous-28 change, best/worst day."""
    header, rows = files["table"]
    rows, _ = clean(header, rows)
    idx = {h: i for i, h in enumerate(header)}
    series = []
    for r in rows:
        d = parse_date(r[0])
        if d:
            series.append((d, {k: num(r[idx[h]]) or 0 for h, k in METRICS.items() if h in idx}))
    series.sort()
    if not series:
        return {}

    def window(a, b):
        part = [m for _, m in series[a:b]]
        return {k: round(sum(m.get(k, 0) for m in part), 1) for k in ("views", "watch_h", "subs")}

    def change(cur, prev):
        return {k: (round(100 * (cur[k] - prev[k]) / prev[k], 1) if prev[k] else None) for k in cur}

    n = len(series)
    out = {"from": series[0][0].isoformat(), "to": series[-1][0].isoformat(), "days": n}
    for w in (7, 28, 90):
        if n >= 2 * w:
            cur, prev = window(n - w, n), window(n - 2 * w, n - w)
            out[f"last_{w}d"], out[f"prev_{w}d"], out[f"change_{w}d_pct"] = cur, prev, change(cur, prev)
    best = max(series, key=lambda t: t[1].get("views", 0))
    worst = min(series, key=lambda t: t[1].get("views", 0))
    out["best_day"] = {"date": best[0].isoformat(), "views": best[1].get("views")}
    out["worst_day"] = {"date": worst[0].isoformat(), "views": worst[1].get("views")}
    return out


def dimension_table(files, top=8):
    """Top rows of a dimension report (traffic source, country, device...) with each row's share of the primary
    column (Views; the first metric when there is no Views column, e.g. subscription source). Columns keep the
    export's own header names."""
    header, rows = files["table"]
    rows, _ = clean(header, rows)
    cols = header[1:]
    primary = "Views" if "Views" in cols else (cols[0] if cols else None)
    recs, total = [], None
    for r in rows:
        rec = {"name": r[0], **{h: num(r[i]) for i, h in enumerate(header) if i}}
        if r[0] == "Total":
            total = rec
        else:
            recs.append(rec)
    recs.sort(key=lambda x: (x.get(primary) or 0) if primary else 0, reverse=True)
    base = ((total or {}).get(primary) if primary else None) or sum((x.get(primary) or 0) for x in recs) or 0
    for x in recs:
        x["share_pct"] = round(100 * (x.get(primary) or 0) / base, 1) if base and primary else None
    return {"column": header[0] if header else "", "primary": primary, "columns": cols, "rows": recs[:top],
            "row_count": len(recs)}


def summarize(folder, today=None):
    manifest, data = load(folder)
    videos, totals, truncated = merge_videos(data, today)
    main = pick_period(videos)
    s = {"channel": manifest.get("channel_name") or manifest.get("channel_id"), "collected": manifest.get("collected"),
         "main_period": main, "channel_totals": totals, "truncated_at_500_videos": truncated, "missing": [
             f"{r['report']}/{r['period']}: {r.get('reason', r.get('status'))}" for r in manifest["reports"] if r.get("status") != "ok"]}
    if main:
        s["distribution"] = distribution(videos, main)
        s["by_format"] = {p: by_format(videos, p) for p in PERIOD_ORDER if any(p in v for v in videos.values())}
        s["by_age"] = by_age(videos, main)
        s["top_views"] = rank(videos, main, "views")
        s["bottom_views"] = rank(videos, main, "views", reverse=False, min_views=0)
        s["best_ctr"] = rank(videos, main, "ctr", min_impr=MIN_IMPRESSIONS)
        s["worst_ctr"] = rank(videos, main, "ctr", reverse=False, min_impr=MIN_IMPRESSIONS)
        s["best_retention"] = rank(videos, main, "avp", min_views=100)
        s["best_subs_per_1k"] = rank(videos, main, "subs_per_1k_views", min_views=500)
    if "daily" in data:
        s["daily"] = {p: daily_trend(f) for p, f in data["daily"].items() if "table" in f}
    s["dimensions"] = {rep: {p: dimension_table(f) for p, f in per.items() if "table" in f}
                       for rep, per in data.items() if rep not in ("videos", "daily")}
    s["video_count"] = len(videos)
    return s, videos


def _f(v):
    """Cell text: whole numbers without '.0', other floats to 1 decimal, None as empty."""
    if v is None:
        return ""
    if isinstance(v, float):
        return str(int(v)) if v == int(v) else str(round(v, 1))
    return str(v)


def _t(rows, cols, head):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        out.append("| " + " | ".join(_f(r.get(c)) for c in cols) + " |")
    return "\n".join(out)


def to_markdown(s):
    L = [f"# Số liệu YouTube Studio: {s['channel']}", "",
         f"Thu thập: {s['collected']}. {s['video_count']} video có số liệu. Kỳ chính: **{s['main_period']}**.",
         "Số liệu lấy từ Studio (Chế độ nâng cao > xuất CSV); Short = video <= "
         f"{SHORT_MAX_S}s (quy ước của script, không phải nhãn của YouTube).", ""]
    if s.get("truncated_at_500_videos"):
        L += [f"> Cảnh báo: bảng video của kỳ {', '.join(s['truncated_at_500_videos'])} bị Studio cắt ở 500 dòng; "
              "bảng xếp hạng và phân bố của kỳ đó chỉ gồm 500 video đứng đầu theo lượt xem, còn dòng 'tổng kênh' vẫn đủ.", ""]
    tcols = [(k, h) for k, h in (("views", "views"), ("watch_h", "giờ xem"), ("subs", "sub"), ("impressions", "hiển thị"),
                                 ("ctr", "CTR %"), ("avd_s", "AVD s"), ("avp", "% xem TB"))
             if any(t.get(k) is not None for t in s["channel_totals"].values())]
    L += ["## Tổng kênh theo kỳ", "", _t([{"period": p, **t} for p, t in s["channel_totals"].items()],
                                          ["period"] + [k for k, _ in tcols], ["kỳ"] + [h for _, h in tcols]), ""]
    d = s.get("distribution")
    if d:
        L += [f"## Phân bố lượt xem ({s['main_period']})", "",
              f"{d['videos']} video; trung vị {d['median']:.0f}, trung bình {d['mean']}, p90 {d['p90']:.0f}, "
              f"max {d['max']:.0f}. 10% video đứng đầu giữ {d['top10pct_share_pct']}% lượt xem.", ""]
    for p, f in s.get("by_format", {}).items():
        if f:
            L += [f"### Short vs long ({p})", "", _t([{"format": k, **v} for k, v in f.items()],
                  ["format", "videos", "views", "watch_h", "subs", "median_views", "subs_per_1k_views"],
                  ["loại", "video", "views", "giờ xem", "sub", "views trung vị", "sub/1k views"]), ""]
    if s.get("by_age"):
        L += [f"## Lượt xem theo tuổi video ({s['main_period']})", "",
              _t(s["by_age"], ["age", "videos", "views", "share_pct"], ["tuổi", "video", "views", "% tổng"]), ""]
    daily = {p: d for p, d in s.get("daily", {}).items() if d}
    if daily:
        longest = max(daily, key=lambda p: daily[p].get("days", 0))
        d = daily[longest]
        L += [f"## Xu hướng theo ngày ({d['from']} đến {d['to']}, {d['days']} ngày)", ""]
        for w in (7, 28, 90):
            if f"change_{w}d_pct" in d:
                L.append(f"- {w} ngày gần nhất so với {w} ngày trước: views {d[f'last_{w}d']['views']:.0f} vs {d[f'prev_{w}d']['views']:.0f} "
                         f"({d[f'change_{w}d_pct']['views']}%), giờ xem {d[f'last_{w}d']['watch_h']:.0f} vs {d[f'prev_{w}d']['watch_h']:.0f}, "
                         f"sub {d[f'last_{w}d']['subs']:.0f} vs {d[f'prev_{w}d']['subs']:.0f}")
        L.append("- Ngày cao / thấp nhất theo kỳ: " + "; ".join(
            f"{p}: {x['best_day']['date']} ({x['best_day']['views']:.0f}) / {x['worst_day']['date']} ({x['worst_day']['views']:.0f})"
            for p, x in daily.items()))
        L.append("")
    # bottom_views stays in summary.json only: the tail is long and rarely actionable
    for name, key, col in (("Top lượt xem", "top_views", "views"),
                           ("CTR hình thu nhỏ cao nhất", "best_ctr", "ctr"), ("CTR thấp nhất", "worst_ctr", "ctr"),
                           ("Giữ chân người xem tốt nhất (% xem TB)", "best_retention", "avp"),
                           ("Kéo sub tốt nhất (sub / 1k views)", "best_subs_per_1k", "subs_per_1k_views")):
        if s.get(key):
            cols = ["id", "title", col] + ([] if col == "views" else ["views"]) + ["format", "age_days"]
            heads = ["id", "tiêu đề", col] + ([] if col == "views" else ["views"]) + ["loại", "tuổi (ngày)"]
            note = ["_avp > 100% là bình thường với Short: người xem xem lại vòng lặp, một lượt xem tính nhiều hơn một lần xem hết._", ""] \
                if key == "best_retention" else []
            L += [f"## {name} ({s['main_period']})", ""] + note + [_t(s[key], cols, heads), ""]
    for rep, per in s.get("dimensions", {}).items():
        # the main period gets the full table; other periods only a one-line top list (to compare shares)
        first = s["main_period"] if s["main_period"] in per else next(iter(per), None)
        for p in ([first] if first else []):
            tb = per[p]
            if tb["rows"]:
                cols = tb["columns"][:5]
                L += [f"## {tb['column']} ({p})", "", _t(tb["rows"][:6], ["name", "share_pct"] + cols,
                                                         [tb["column"], f"% {tb['primary']}"] + cols), ""]
        for p, tb in per.items():
            if p != first and tb["rows"]:
                top = "; ".join(f"{r['name']} {_f(r.get('share_pct'))}%" for r in tb["rows"][:5])
                L.append(f"- {tb['column']} ({p}): {top}")
        if len(per) > 1:
            L.append("")
    if s.get("missing"):
        L += ["## Không lấy được", ""] + [f"- {m}" for m in s["missing"]] + [""]
    return "\n".join(L)


def write_outputs(folder, out=None, today=None):
    out = Path(out or folder)
    out.mkdir(parents=True, exist_ok=True)
    s, videos = summarize(folder, today)
    (out / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (out / "summary.md").write_text(to_markdown(s), encoding="utf-8")
    cols = ["id", "title", "published", "duration_s", "format", "age_days"]
    periods = [p for p in PERIOD_ORDER if any(p in v for v in videos.values())]
    keys = list(METRICS.values()) + ["subs_per_1k_views", "hours_per_1k_views"]
    with open(out / "videos.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols + [f"{p}_{k}" for p in periods for k in keys])
        for v in sorted(videos.values(), key=lambda v: -((v.get(pick_period(videos) or "28d") or {}).get("views") or 0)):
            w.writerow([v.get(c) for c in cols] + [(v.get(p) or {}).get(k) for p in periods for k in keys])
    return out / "summary.md", out / "summary.json", out / "videos.csv"
