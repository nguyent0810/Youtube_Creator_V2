"""Theo dõi hằng ngày tuần test 3 short/ngày trên CL (05–11/10/2026). Chỉ ĐỌC kênh, không sửa video.

Ngoại lệ trên máy: Long đã public đủ 9 ngày thì ghi một lần ret1 và % đề xuất của 7 ngày đầu
vào data/variety/ledger.json (so với video ngay trước). Không ghi đè số đã chốt.

    python motion/stier/monitor.py            # chụp số liệu + viết báo cáo
    python motion/stier/monitor.py --quiet    # chỉ ghi file (dùng cho lịch chạy tự động)

Mỗi lần chạy:
- Data API: view/like/comment hiện tại của 21 video tuần test (tuần test = WEEK trong week_2026-10-05.py
  + kế hoạch drip_2026-10.json), giờ lên sóng thật (status.publishAt / snippet.publishedAt).
- Analytics: theo từng video đã public — view từ Shorts feed (insightTrafficSourceType=SHORTS), % xem TB.
  Analytics trễ 1–2 ngày, ngày tính theo giờ Thái Bình Dương -> số của 1–2 ngày gần nhất còn thiếu.
- Kênh: view Shorts theo ngày + view từ Shorts feed theo ngày, 21 ngày gần nhất, so với mốc trước sự cố
  (25–28/09: 8–10k view/ngày từ Shorts feed).
Ghi: output/analysis/monitor/snapshots.jsonl (lịch sử view từng video), report_<ngày>.md, latest.md.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "motion"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory import channels, publish, store  # noqa: E402
import variety  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("week", Path(__file__).resolve().parent / "week_2026-10-05.py")
_week = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_week)
WEEK = _week.WEEK

DATA = "https://www.googleapis.com/youtube/v3/videos"
ANA = "https://youtubeanalytics.googleapis.com/v2/reports"
OUT = ROOT / "output/analysis/monitor"
DRIP = Path(__file__).resolve().parent / "drip_2026-10.json"
BASELINE = 9000          # view/ngày từ Shorts feed trước sự cố (25–28/09)


def utc(vn: str) -> str:
    return (datetime.strptime(vn, "%Y-%m-%d %H:%M") - timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")


def plan() -> dict[str, str]:
    """slug -> giờ lên sóng dự kiến (UTC)."""
    p = {s: utc(v[0]) for s, v in WEEK.items()}
    p.update({d["slug"]: utc(d["vn"]) for d in json.loads(DRIP.read_text(encoding="utf-8"))})
    return p


def ana(H, cid, **q):
    r = requests.get(ANA, params={"ids": f"channel=={cid}", **q}, headers=H, timeout=60)
    if r.status_code >= 300:
        return None
    d = r.json()
    heads = [h["name"] for h in d.get("columnHeaders", [])]
    return [dict(zip(heads, row)) for row in d.get("rows") or []]


def long_section(H, cid, now) -> list[str]:
    """Long đã đăng (output/long/*/pub/result.json): view, % xem TB, giữ chân ở phút 1/2, tỷ trọng view từ đề xuất.
    Mốc so sánh: Yakuza giữ 64% ở phút 1 và 49% ở phút 2, 89% view từ RELATED_VIDEO."""
    rows = []
    for rp in sorted((ROOT / "output/long").glob("*/pub/result.json")):
        vid = json.loads(rp.read_text(encoding="utf-8")).get("video_id")
        if vid:
            rows.append((rp.parts[-3], vid))
    if not rows:
        return []
    items = {}
    r = requests.get(DATA, params={"part": "snippet,status,statistics,contentDetails", "id": ",".join(v for _, v in rows)}, headers=H, timeout=60)
    if r.ok:
        items = {it["id"]: it for it in r.json()["items"]}
    L = ["", "## Long (giữ chân đầu video là điểm yếu cần theo dõi)", "",
         "| Long | Lên sóng | View | % xem TB | Còn ở phút 1 | Còn ở phút 2 | Từ đề xuất |", "|---|---|---:|---:|---:|---:|---:|"]
    for topic, vid in rows:
        it = items.get(vid)
        if not it or it["status"]["privacyStatus"] != "public":
            pa = it["status"].get("publishAt", "") if it else ""
            L.append(f"| {topic} | hẹn {pa[:16]} | | | | | |")
            continue
        live = it["snippet"]["publishedAt"][:10]
        start = (datetime.strptime(live, "%Y-%m-%d") - timedelta(days=1)).date().isoformat()
        end = now.date().isoformat()
        dur = 0
        m = __import__("re").match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", it["contentDetails"]["duration"])
        if m:
            dur = int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)
        tot = ana(H, cid, startDate=start, endDate=end, metrics="views,averageViewPercentage", filters=f"video=={vid}") or []
        cur = ana(H, cid, startDate=start, endDate=end, metrics="audienceWatchRatio", dimensions="elapsedVideoTimeRatio", filters=f"video=={vid}") or []
        src = ana(H, cid, startDate=start, endDate=end, metrics="views", dimensions="insightTrafficSourceType", filters=f"video=={vid}") or []

        def pct(x):
            return "—" if x is None else f"{x:.0f}%"
        avp = f"{float(tot[0]['averageViewPercentage']):.1f}" if tot else "—"
        L.append(f"| [{topic}](https://youtu.be/{vid}) | {live} | {int(it['statistics'].get('viewCount', 0)):,} | {avp} | "
                 f"{pct(variety.minute_retention(cur, dur, 60))} | {pct(variety.minute_retention(cur, dur, 120))} | {pct(variety.suggested_share(src))} |")
    return L


def _published(it) -> datetime:
    return datetime.strptime(it["snippet"]["publishedAt"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)


def _duration_s(it) -> int:
    m = __import__("re").match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", it["contentDetails"]["duration"])
    if not m:
        return 0
    return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0)


def sync_long_feedback(H, cid, now) -> list[str]:
    """Ghi một lần số 7 ngày đầu vào sổ. Bỏ qua video chưa đủ hạn, đã chốt, hoặc Analytics còn trống."""
    found = []
    for rp in sorted((ROOT / "output/long").glob("*/pub/result.json")):
        vid = json.loads(rp.read_text(encoding="utf-8")).get("video_id")
        if vid:
            found.append((rp.parts[-3], vid))
    if not found:
        return []
    r = requests.get(DATA, params={"part": "snippet,status,contentDetails", "id": ",".join(v for _, v in found)}, headers=H, timeout=60)
    items = {it["id"]: it for it in r.json()["items"]} if r.ok else {}
    rows = variety.ledger()
    by_topic = {row["topic"]: row for row in rows}
    pending = []
    notes = []
    for topic, vid in found:
        it = items.get(vid)
        if not it or it["status"]["privacyStatus"] != "public":
            continue
        published = _published(it)
        if not variety.feedback_ready(published, now):
            continue
        row = by_topic.get(topic)
        if row is None:
            notes.append(f"{topic}: chưa có trong sổ, chưa ghi")
            continue
        if row.get("ret1") is not None:
            continue
        pending.append((row.get("date", ""), topic, vid, published, _duration_s(it)))
    changed = False
    for _, topic, vid, published, dur in sorted(pending):
        start, end = variety.feedback_window(published)
        cur = ana(H, cid, startDate=start, endDate=end, metrics="audienceWatchRatio", dimensions="elapsedVideoTimeRatio", filters=f"video=={vid}")
        src = ana(H, cid, startDate=start, endDate=end, metrics="views", dimensions="insightTrafficSourceType", filters=f"video=={vid}")
        ret1 = variety.minute_retention(cur, dur, 60)
        suggested = variety.suggested_share(src)
        if ret1 is None or suggested is None:
            notes.append(f"{topic}: Analytics chưa có đủ số 7 ngày đầu ({start} → {end}), để lần sau")
            continue
        age_days = round((now - published).total_seconds() / 86400, 1)
        rows, stamped = variety.stamp_feedback(rows, topic, ret1=ret1, suggested=suggested, age_days=age_days, today=now.date().isoformat())
        if stamped is None:
            continue
        changed = True
        vs = ""
        if stamped.get("ret1_vs_prev") is not None and stamped.get("suggested_vs_prev") is not None:
            vs = f", phút 1 {stamped['ret1_vs_prev']:+.1f} điểm, đề xuất {stamped['suggested_vs_prev']:+.1f} điểm so với video trước"
        notes.append(f"{topic}: ghi sổ {ret1:.0f}% còn ở phút 1, {suggested:.0f}% từ đề xuất{vs}")
    if changed:
        variety.save_ledger(rows)
    return notes


def feedback_table() -> list[str]:
    """Bảng số đã chốt trong sổ, để lần nghiên cứu sau đọc cùng báo cáo."""
    rows = sorted((r for r in variety.ledger() if r.get("ret1") is not None), key=lambda r: r.get("date", ""))
    L = ["", "### Sổ giữ chân (7 ngày đầu, đã chốt)", ""]
    if not rows:
        L.append("Chưa có số 7 ngày trong sổ.")
        return L
    L += ["| Long | Ngày sổ | Còn ở phút 1 | Từ đề xuất | So với video trước |", "|---|---|---:|---:|---|"]
    for r in rows:
        if r.get("ret1_vs_prev") is None:
            vs = "—"
        else:
            vs = f"phút 1 {r['ret1_vs_prev']:+.1f} điểm, đề xuất {r['suggested_vs_prev']:+.1f} điểm"
        L.append(f"| {r['topic']} | {r['date']} | {r['ret1']:.0f}% | {r['suggested']:.0f}% | {vs} |")
    return L


def verdict(views: int, hours: float) -> str:
    if hours < 6:
        return "mới lên"
    if hours >= 24 and views < 100:
        return "❌ feed không phân phối"
    if views >= 1000:
        return "✅ feed đang đẩy"
    return "… vòng test đầu" if hours < 48 else ("⚠️ kẹt dưới 1k" if views >= 100 else "❌ feed không phân phối")


def main():
    quiet = "--quiet" in sys.argv
    creds = json.loads(channels.creds_path("CL").read_text(encoding="utf-8"))
    tok = publish.access_token(creds)
    H = {"Authorization": f"Bearer {tok}"}
    cid = publish._api(tok, "GET", "channels", {"part": "id", "mine": "true"})["items"][0]["id"]
    now = datetime.now(timezone.utc)
    pl = plan()
    with store.connect() as c:
        vid = {r["slug"][6:]: r["video_id"] for r in c.execute(
            "SELECT slug, video_id FROM item WHERE channel='CL' AND slug LIKE 'cl-hs-%' AND video_id IS NOT NULL AND video_id!=''")}
    ids = [vid[s] for s in pl if s in vid]
    items = {}
    for i in range(0, len(ids), 50):
        r = requests.get(DATA, params={"part": "snippet,status,statistics", "id": ",".join(ids[i:i + 50])}, headers=H, timeout=60)
        r.raise_for_status()
        items.update({it["id"]: it for it in r.json()["items"]})

    OUT.mkdir(parents=True, exist_ok=True)
    hist_f = OUT / "snapshots.jsonl"
    prev = {}
    if hist_f.exists():
        for ln in hist_f.read_text(encoding="utf-8").splitlines():
            d = json.loads(ln)
            prev[d["id"]] = d
    end = (now.date()).isoformat()
    rows, snaps = [], []
    for s, when in sorted(pl.items(), key=lambda kv: kv[1]):
        v = vid.get(s)
        it = items.get(v) if v else None
        if not it:
            rows.append({"slug": s, "id": v or "-", "when": when, "state": "chưa upload"})
            continue
        st, sn, stt = it["status"], it["snippet"], it.get("statistics", {})
        public = st["privacyStatus"] == "public"
        live = st.get("publishAt") or sn["publishedAt"]
        views = int(stt.get("viewCount", 0))
        hours = (now - datetime.strptime(live[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)).total_seconds() / 3600
        row = {"slug": s, "id": v, "title": sn["title"], "when": live, "state": st["privacyStatus"],
               "views": views, "likes": int(stt.get("likeCount", 0)), "comments": int(stt.get("commentCount", 0)),
               "hours": round(hours, 1), "delta": views - prev[v]["views"] if v in prev else None}
        if public:
            start = (datetime.strptime(live[:10], "%Y-%m-%d") - timedelta(days=1)).date().isoformat()
            src = ana(H, cid, startDate=start, endDate=end, metrics="views", dimensions="insightTrafficSourceType", filters=f"video=={v}")
            tot = ana(H, cid, startDate=start, endDate=end, metrics="views,averageViewPercentage", filters=f"video=={v}")
            row["feed"] = next((int(x["views"]) for x in src or [] if x["insightTrafficSourceType"] == "SHORTS"), None) if src is not None else None
            row["avp"] = round(float(tot[0]["averageViewPercentage"]), 1) if tot else None
            row["verdict"] = verdict(views, hours)
            snaps.append({"ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "id": v, "slug": s, "views": views})
        rows.append(row)
    with hist_f.open("a", encoding="utf-8") as f:
        for x in snaps:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")

    # kênh: Shorts theo ngày + Shorts feed theo ngày
    start = (now.date() - timedelta(days=21)).isoformat()
    daily = ana(H, cid, startDate=start, endDate=end, metrics="views", dimensions="day", filters="creatorContentType==shorts") or []
    feed = ana(H, cid, startDate=start, endDate=end, metrics="views", dimensions="day,insightTrafficSourceType") or []
    feed_by_day = {}
    for x in feed:
        if x["insightTrafficSourceType"] == "SHORTS":
            feed_by_day[x["day"]] = int(x["views"])

    L = [f"# CL · theo dõi tuần test 3 short/ngày — {datetime.now():%Y-%m-%d %H:%M} (giờ máy)", "",
         "## Từng video (giờ VN)", "",
         "| Lên sóng (VN) | Video | Trạng thái | View | +từ lần trước | Shorts feed | % xem TB | Giờ | Nhận định |",
         "|---|---|---|---:|---:|---:|---:|---:|---|"]
    for r in rows:
        vn = (datetime.strptime(r["when"][:16], "%Y-%m-%dT%H:%M") + timedelta(hours=7)).strftime("%d/%m %H:%M")
        if r["state"] != "public":
            L.append(f"| {vn} | {r['slug']} | {r['state']} | | | | | | |")
            continue
        f = lambda k: "—" if r.get(k) is None else f"{r[k]:,}" if isinstance(r[k], int) else str(r[k])
        L.append(f"| {vn} | [{r['slug']}](https://youtu.be/{r['id']}) | public | {f('views')} | {f('delta')} | {f('feed')} | "
                 f"{f('avp')} | {r['hours']} | {r['verdict']} |")
    pub = [r for r in rows if r["state"] == "public"]
    if pub:
        old = [r for r in pub if r["hours"] >= 24]
        L += ["", f"Đã lên: {len(pub)}/21 · ≥24h: {len(old)} · trong đó ≥1k view: {sum(r['views'] >= 1000 for r in old)}, "
                  f"<100 view: {sum(r['views'] < 100 for r in old)}"]
    L += ["", f"## Kênh: view Shorts theo ngày (mốc trước sự cố ≈ {BASELINE:,}/ngày từ Shorts feed)", "",
          "| Ngày (giờ Mỹ PT) | View Shorts | Từ Shorts feed |", "|---|---:|---:|"]
    by_day = {x["day"]: int(x["views"]) for x in daily}
    for k in range(14, -1, -1):
        d = (now.date() - timedelta(days=k)).isoformat()
        fb = feed_by_day.get(d)
        L.append(f"| {d} | {'chưa có số' if d not in by_day else f'{by_day[d]:,}'} | {'—' if fb is None else f'{fb:,}'} |")
    notes = sync_long_feedback(H, cid, now)
    L += long_section(H, cid, now)
    L += feedback_table()
    L += ["", "### Lần chạy này", ""]
    L += [f"- {n}" for n in notes] or ["- Không có số mới để ghi."]
    L += ["", "_Analytics trễ 1–2 ngày; ngày gần nhất thường thiếu số. Sổ giữ chân chỉ lấy 7 ngày đầu và ghi một lần._"]
    md = "\n".join(L) + "\n"
    (OUT / f"report_{now:%Y-%m-%d}.md").write_text(md, encoding="utf-8")
    (OUT / "latest.md").write_text(md, encoding="utf-8")
    if not quiet:
        print(md)


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main()
