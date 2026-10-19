"""Đo thật: mỗi DÒNG nội dung giữ người xem đến đâu. Chỉ đọc YouTube Analytics.

    python scripts/analytics_report.py --channel CL
    python scripts/analytics_report.py            # cả 3 kênh

VÌ SAO (rút từ branch feat/improve-short-content-pipeline, 28/09/2026): v1
"chấm rồi vứt" -- không ai biết kịch bản nào giữ được người xem, nên mọi
thay đổi rubric đều đoán mò. v2 cũng vậy cho tới file này: đăng xong là mất
dấu. Credential của cả 3 kênh đã có quyền đọc Analytics (đã thử 30/09).

Lấy cho từng video đã lên sóng: views, % xem trung bình, thời lượng xem trung
bình, retention curve (elapsedVideoTimeRatio -> audienceWatchRatio) và nguồn
traffic. Ghi thô vào data/analytics/<KÊNH>/ (gitignore), rồi gộp theo dòng.

Video quá ít view thì YouTube không trả curve -> ghi THIẾU, không phải 0.
Lỗi tạm (429/5xx) thử lại; lỗi vĩnh viễn ghi lý do, không làm hỏng cả lần chạy.
"""
from __future__ import annotations

import json
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import channels, publish, store  # noqa: E402
from factory.script_signals import signals  # noqa: E402

API = "https://youtubeanalytics.googleapis.com/v2/reports"
OUT = ROOT / "data" / "analytics"


def _report(tok, cid, vid, dim, metrics, start, end):
    q = urllib.parse.urlencode({"ids": f"channel=={cid}", "startDate": start, "endDate": end,
                                "metrics": metrics, "dimensions": dim, "filters": f"video=={vid}"})
    for attempt in range(3):
        try:
            req = urllib.request.Request(f"{API}?{q}", headers={"Authorization": f"Bearer {tok}"})
            d = json.load(urllib.request.urlopen(req, timeout=60))
            heads = [h["name"] for h in d.get("columnHeaders", [])]
            return {"ok": True, "rows": [dict(zip(heads, r)) for r in d.get("rows") or []]}
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504) or attempt == 2:
                return {"ok": False, "reason": f"http_{e.code}"}
        except urllib.error.URLError as e:
            if attempt == 2:
                return {"ok": False, "reason": f"network: {e}"}
        time.sleep(2 * 3 ** attempt)


def _at(curve, ratio):
    """audienceWatchRatio gần vị trí `ratio` nhất (curve 0..1)."""
    if not curve:
        return None
    p = min(curve, key=lambda r: abs(float(r["elapsedVideoTimeRatio"]) - ratio))
    return float(p["audienceWatchRatio"])


def fetch_channel(ch: str) -> list[dict]:
    tok = publish.access_token(json.loads(channels.creds_path(ch).read_text(encoding="utf-8")))
    cid = publish._api(tok, "GET", "channels", {"part": "id", "mine": "true"})["items"][0]["id"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with store.connect() as c:
        rows = [dict(r) for r in c.execute(
            "SELECT slug, video_id, publish_at FROM item WHERE channel=? AND stage='published' "
            "AND video_id IS NOT NULL AND publish_at <= ? ORDER BY publish_at", (ch, now))]
    end = datetime.now(timezone.utc).date().isoformat()
    out = []
    for r in rows:
        # Analytics tính ngày theo GIỜ THÁI BÌNH DƯƠNG. Video đăng 00:00 UTC 25/09 là
        # 24/09 giờ Mỹ -> lấy từ ngày đăng (UTC) sẽ BỎ MẤT ngày đầu, ngày nhiều view
        # nhất (lỗi thật: "Điều 125" ra 174 thay vì 1.263). Lùi 1 ngày cho chắc.
        start = (datetime.strptime(r["publish_at"][:10], "%Y-%m-%d") - timedelta(days=1)).date().isoformat()
        tot = _report(tok, cid, r["video_id"], "video", "views,averageViewPercentage,averageViewDuration", start, end)
        cur = _report(tok, cid, r["video_id"], "elapsedVideoTimeRatio", "audienceWatchRatio", start, end)
        src = _report(tok, cid, r["video_id"], "insightTrafficSourceType", "views", start, end)
        t = (tot.get("rows") or [{}])[0] if tot["ok"] else {}
        try:
            b = store.load_bundle(ch, r["slug"])
            sig = signals(b.script)
        except Exception:
            sig = {}
        out.append({**r, "views": t.get("views"), "avp": t.get("averageViewPercentage"),
                    "avd": t.get("averageViewDuration"),
                    "curve": cur.get("rows") if cur["ok"] else None,
                    "curve_missing": None if cur["ok"] and cur.get("rows") else (cur.get("reason") or "no_data"),
                    "sources": {s["insightTrafficSourceType"]: s["views"] for s in src.get("rows") or []},
                    "signals": sig})
    d = OUT / ch
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{datetime.now():%Y%m%dT%H%M}.json").write_text(
        json.dumps({"fetched_at": now, "channel": ch, "videos": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def summarize(ch: str, vids: list[dict]) -> list[str]:
    L = channels.CHANNELS[ch]
    lines = [f"\n== {L['ten']} ({ch}) — {len(vids)} video đã lên sóng"]
    by = {}
    for v in vids:
        pf = next((p for p in L["prefixes"] if v["slug"].startswith(p)), "?")
        by.setdefault(pf, []).append(v)
    lines.append(f"   {'dòng':14s} {'n':>3s} {'view TB':>8s} {'view max':>8s} {'%xem TB':>8s} "
                 f"{'giữ@25%':>8s} {'giữ@75%':>8s} {'%Shorts':>8s}")
    for pf, vs in by.items():
        views = [v["views"] or 0 for v in vs]
        avps = [v["avp"] for v in vs if v["avp"]]
        r25 = [x for v in vs if (x := _at(v["curve"], 0.25)) is not None]
        r75 = [x for v in vs if (x := _at(v["curve"], 0.75)) is not None]
        sh = [v["sources"].get("SHORTS", 0) / max(1, sum(v["sources"].values())) for v in vs if v["sources"]]
        f = lambda xs, pct=False: "—" if not xs else (f"{statistics.mean(xs):.0%}" if pct else f"{statistics.mean(xs):.0f}")
        lines.append(f"   {pf:14s} {len(vs):3d} {f(views):>8s} {max(views):>8d} "
                     f"{(f'{statistics.mean(avps):.0f}%' if avps else '—'):>8s} {f(r25, True):>8s} "
                     f"{f(r75, True):>8s} {f(sh, True):>8s}")
    top = sorted(vids, key=lambda v: v["views"] or 0, reverse=True)[:5]
    lines.append("   Top view: " + " · ".join(f"{v['slug']} ({v['views']}, {v['avp'] or 0:.0f}%)" for v in top))
    return lines


if __name__ == "__main__":
    chs = [channels.pick()] if "--channel" in sys.argv else channels.available()
    report = []
    for ch in chs:
        report += summarize(ch, fetch_channel(ch))
    print("\n".join(report))
