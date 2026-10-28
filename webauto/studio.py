"""YouTube Studio analytics: export every report as CSV and merge them into one summary for LLMs.

Why this and not the Analytics API (factory/analytics.py): Studio's Advanced mode has numbers the API
does not return (thumbnail impressions and CTR, per-video tables, audience splits), and the export is one
clean CSV per report with every row, so a script can collect "everything" without an LLM reading screens.

How: for each (report, period) open the Advanced-mode URL (it is fully parameterised: channel, period,
metrics, dimension), click "Export current view" > ".csv", unzip. `webauto studio summarize` then merges
the CSVs into summary.md / summary.json / videos.csv (see studio_summary.py).

Studio ids for periods / dimensions are not documented; the ones below were read off Studio's own pickers (the URL
it navigates to after a click). A wrong id renders a blank page, so "export button never appears" = wrong id.
Candidates are tried in order and the one that works is cached in ~/.webauto/studio_catalog.json, so when Studio
changes an id, add the new one to the lists below.

Uses the user's signed-in Chrome through Browsentic; needs guardrail `file-download` = Allow. Read-only:
nothing is changed in Studio.
"""
import asyncio
import csv
import io
import json
import re
import time
import zipfile
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode

from . import auth
from .browsentic import browser, newest_download, run
from .common import default_out, home
from . import studio_summary

STUDIO = "https://studio.youtube.com/"
BASE = "https://studio.youtube.com/channel/{ch}/analytics/tab-overview/period-default/explore"

# metric ids seen in Studio's own Advanced-mode links; shorter sets are the fallback when a dimension
# does not support impressions / CTR
METRICS_FULL = ["EXTERNAL_VIEWS", "EXTERNAL_WATCH_TIME", "SUBSCRIBERS_NET_CHANGE", "VIDEO_THUMBNAIL_IMPRESSIONS",
                "VIDEO_THUMBNAIL_IMPRESSIONS_VTR", "AVERAGE_WATCH_TIME", "AVERAGE_WATCH_PERCENTAGE"]
METRICS_BASE = ["EXTERNAL_VIEWS", "EXTERNAL_WATCH_TIME", "SUBSCRIBERS_NET_CHANGE", "AVERAGE_WATCH_TIME",
                "AVERAGE_WATCH_PERCENTAGE"]
METRICS_MIN = ["EXTERNAL_VIEWS", "EXTERNAL_WATCH_TIME"]
METRICS_SUBS = ["SUBSCRIBERS_NET_CHANGE", "SUBSCRIBERS_GAINED", "SUBSCRIBERS_LOST"]  # subscription source has no views
METRICS_DEVICE = ["EXTERNAL_VIEWS", "EXTERNAL_WATCH_TIME", "AVERAGE_WATCH_TIME", "UNIQUE_REACH"]
METRIC_SETS = [METRICS_FULL, METRICS_BASE, METRICS_MIN, METRICS_SUBS, METRICS_DEVICE]
# order in which metric sets are tried for a report (indexes into METRIC_SETS); default is full > base > min
REPORT_METRIC_SETS = {"videos": [0], "daily": [0], "subscription_source": [3],
                      "device": [4, 1, 2], "operating_system": [4, 1, 2]}

PERIOD_CANDIDATES = {  # all five read off Studio's own period picker (the URL it navigates to)
    "7d": ["week"], "28d": ["4_weeks"], "90d": ["quarter"], "365d": ["year"], "lifetime": ["lifetime"],
}
DIMENSION_CANDIDATES = {
    "videos": ["VIDEO"], "daily": ["DAY"],
    "traffic_source": ["TRAFFIC_SOURCE_TYPE", "TRAFFIC_TYPE", "TRAFFIC_SOURCE"],
    "geography": ["COUNTRY", "COUNTRY_CODE"],
    "content_type": ["CREATOR_CONTENT_TYPE", "VIDEO_CONTENT_TYPE", "CONTENT_TYPE"],
    "playlist": ["PLAYLIST"],
    "city": ["CITY", "CITY_NAME"],
    "age": ["VIEWER_AGE", "AGE_GROUP", "VIEWER_AGE_GROUP"],
    "gender": ["VIEWER_GENDER", "GENDER"],
    "new_vs_returning": ["LOYALTY_STATE"],
    "subscription_status": ["SUBSCRIBED_TO_UPLOADER_STATE"],
    "subscription_source": ["SUBSCRIPTION_SOURCE_TYPE"],
    "youtube_product": ["PRODUCT"],
    "device": ["DEVICE_PLATFORM_TYPE"],
    "operating_system": ["DEVICE_OS_TYPE"],
}
# which periods each kind of report is collected for (a full per-video table for every period; the
# audience splits only for the recent and lifetime views, to keep the number of exports small)
REPORT_PERIODS = {"videos": ["7d", "28d", "90d", "365d", "lifetime"], "daily": ["28d", "90d", "365d", "lifetime"]}
DEFAULT_DIM_PERIODS = ["28d", "lifetime"]
PERIOD_ORDER = ["28d", "lifetime", "7d", "90d", "365d"]  # 28d first: ids for new dimensions are resolved on it


def build_url(channel, period_id, dimension, metrics):
    q = [("entity_type", "CHANNEL"), ("entity_id", channel), ("time_period", period_id),
         ("explore_type", "TABLE_AND_CHART"), ("metric", metrics[0]), ("granularity", "DAY")]
    q += [("t_metrics", m) for m in metrics]
    q += [("dimension", dimension), ("o_column", metrics[0]), ("o_direction", "ANALYTICS_ORDER_DIRECTION_DESC")]
    return BASE.format(ch=channel) + "?" + urlencode(q)


def catalog_path():
    return home() / "studio_catalog.json"


def load_catalog(refresh=False):
    p = catalog_path()
    if refresh or not p.exists():
        return {"periods": {}, "dimensions": {}, "metric_sets": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def save_catalog(cat):
    p = catalog_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cat, indent=1), encoding="utf-8")


def classify(entries, report):
    """entries: [(index, header)] of the CSVs in one export -> {index: kind}. Kinds: table, chart, totals.

    The zip holds the table (all rows), a chart file (Date + top-5 items) and a daily-totals file (Date,
    <metric>). File names are localised, headers are English, so classify by header.
    """
    kinds, taken = {}, set()
    order = sorted(entries, key=lambda e: -len(e[1])) if report == "daily" else entries
    for i, h in order:
        if h and h[0] == "Date" and len(h) == 2:
            kinds[i] = "totals"
        elif h and h[0] == "Date" and report != "daily":
            kinds[i] = "chart"
        elif "table" not in taken:
            kinds[i] = "table"
            taken.add("table")
        else:
            kinds[i] = "chart"
    return kinds


def extract(zip_path, dest, report):
    """Unzip the .csv members of an export into dest as table.csv / chart.csv / totals.csv; return {kind: path}."""
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        members = [(i, info) for i, info in enumerate(z.infolist()) if info.filename.lower().endswith(".csv")
                   and info.file_size < 50_000_000]
        raw = {i: z.read(info) for i, info in members}
    heads = {}
    for i, data in raw.items():
        first = next(csv.reader(io.StringIO(data.decode("utf-8-sig"))), [])
        heads[i] = first
    out = {}
    for i, kind in classify(list(heads.items()), report).items():
        path = dest / f"{kind}.csv"
        if path.exists():
            continue
        path.write_bytes(raw[i])  # names come from `kind`, never from the zip, so no path traversal
        out[kind] = path
    return out


async def ready(b, tries=2):
    """The export button shows up once the report rendered; a wrong period/dimension id renders nothing."""
    for _ in range(tries):
        try:
            await b.call("page_waitForElement", target={"selector": "#export-button"})
            return True
        except RuntimeError:
            pass
    return False


async def export_zip(b, settle=2):
    await asyncio.sleep(settle)  # let the table finish rendering
    # A real (trusted) click: Chrome allows one automatic download per user interaction and refuses the
    # next ones silently ("Nothing downloaded"); a script-dispatched click does not count as interaction.
    await b.call("page_trustedClick", target={"selector": "#export-button"})
    await b.call("page_waitForElement", target={"text": "(.csv)"})
    t0 = time.time() - 2
    await b.call("page_captureDownload", target={"text": "(.csv)"}, timeoutMs=45000)
    return newest_download(t0)


async def ensure_login(b):
    """Signed out, Studio redirects to accounts.google.com. Wait for the owner; never type credentials."""
    async def ok():
        url = ((await b.call("browsentic_status")).get("activeTab") or {}).get("url", "")
        return url.startswith(STUDIO) and not auth.url_is_login(url)

    await auth.ensure(ok, "YouTube Studio", STUDIO)


async def current_channel(b):
    await b.call("page_navigate", url=STUDIO)
    for _ in range(10):
        st = await b.call("browsentic_status")
        m = re.search(r"/channel/(UC[\w-]{22})", (st.get("activeTab") or {}).get("url", ""))
        if m:
            return m.group(1)
        await asyncio.sleep(2)
    raise SystemExit("could not detect the Studio channel; pass --channel-id UC...")


async def fetch(b, channel, report, period, cat, dest):
    """Try known ids first, then the candidates; cache whatever works. Returns (files, ids) or (None, reason)."""
    known_p = cat["periods"].get(period)
    known_d = cat["dimensions"].get(report)
    pids = ([known_p] if known_p else []) + [p for p in PERIOD_CANDIDATES[period] if p != known_p]
    dids = ([known_d] if known_d else []) + [d for d in DIMENSION_CANDIDATES[report] if d != known_d]
    known_m = cat["metric_sets"].get(report)
    order = REPORT_METRIC_SETS.get(report, [0, 1, 2])
    msets = ([known_m] if known_m in order else []) + [i for i in order if i != known_m]
    last = "no candidate id rendered"
    for pid in pids:
        for did in dids:
            for mi in msets:
                # a NEW tab per attempt: Chrome refuses a second automatic download in the same tab
                tab = await b.call("page_openTab", url=build_url(channel, pid, did, METRIC_SETS[mi]))
                try:
                    if not await ready(b, 1 if (pid != known_p or did != known_d) else 2):
                        continue
                    z = None
                    for attempt in range(2):  # big reports (lifetime) sometimes are not ready on the first click
                        try:
                            z = await export_zip(b, settle=2 + 6 * attempt)
                            break
                        except RuntimeError as e:
                            last = f"export failed ({str(e)[:80]}); the report may be empty"
                            await b.call("page_navigate", url=build_url(channel, pid, did, METRIC_SETS[mi]))
                            if not await ready(b, 2):
                                break
                    if not z:
                        last = "export produced no file"
                        continue
                    files = extract(z, dest, report)
                    if not files.get("table"):
                        last = "export had no table"
                        continue
                    cat["periods"][period], cat["dimensions"][report], cat["metric_sets"][report] = pid, did, mi
                    return files, {"period_id": pid, "dimension_id": did, "metrics": len(METRIC_SETS[mi])}
                finally:
                    if tab.get("tabId"):
                        try:
                            await b.call("page_closeTab", tabId=tab["tabId"])
                        except Exception:
                            pass
    return None, last


def plan(reports, periods):
    out = []
    for rep in reports:
        allowed = REPORT_PERIODS.get(rep, DEFAULT_DIM_PERIODS)
        out += [(rep, p) for p in PERIOD_ORDER if p in periods and p in allowed]
    return out


async def collect(channel, out, periods, reports, refresh=False, resume=False):
    cat = load_catalog(refresh)
    items = []
    async with browser() as b:
        tab = await b.call("page_openTab", url=STUDIO)
        try:
            await asyncio.sleep(3)
            await ensure_login(b)
            channel = channel or await current_channel(b)
            folder = Path(out) / channel / date.today().isoformat()
            done = {}
            if resume and (folder / "manifest.json").exists():  # keep what already worked, retry the rest
                prev = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
                done = {(r["report"], r["period"]): r for r in prev["reports"] if r["status"] == "ok"}
            for n, (rep, per) in enumerate(plan(reports, periods), 1):
                if (rep, per) in done:
                    items.append(done[(rep, per)])
                    print(f"[{n}] {rep} / {per}: already collected", flush=True)
                    continue
                rel = Path("raw") / f"{rep}__{per}"
                print(f"[{n}] {rep} / {per} ...", flush=True)
                files, info = await fetch(b, channel, rep, per, cat, folder / rel)
                if files:
                    items.append({"report": rep, "period": per, "status": "ok", **info,
                                  "files": {k: (rel / v.name).as_posix() for k, v in files.items()}})
                    print(f"     ok: {info['dimension_id']} / {info['period_id']} ({len(files)} files)", flush=True)
                else:
                    items.append({"report": rep, "period": per, "status": "failed", "reason": info})
                    print(f"     failed: {info}", flush=True)
                save_catalog(cat)
        finally:
            if tab.get("tabId"):
                try:
                    await b.call("page_closeTab", tabId=tab["tabId"])
                except Exception:
                    pass
    manifest = {"channel_id": channel, "collected": datetime.now().isoformat(timespec="seconds"),
                "reports": items}
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    return folder


def _run_collect(a):
    periods = [p.strip() for p in a.periods.split(",") if p.strip()]
    reports = [r.strip() for r in a.reports.split(",") if r.strip()]
    bad = [r for r in reports if r not in DIMENSION_CANDIDATES] + [p for p in periods if p not in PERIOD_CANDIDATES]
    if bad:
        raise SystemExit(f"unknown report/period: {bad}; reports={list(DIMENSION_CANDIDATES)} periods={list(PERIOD_CANDIDATES)}")
    folder = run(collect(a.channel_id, a.out, periods, reports, a.refresh_catalog, a.resume))
    print("collected into", folder)
    if not a.no_summary:
        for p in studio_summary.write_outputs(folder):
            print("wrote", p)


def _run_summarize(a):
    for p in studio_summary.write_outputs(a.dir, a.out):
        print("wrote", p)


def add_parser(sub):
    ap = sub.add_parser("studio", help="YouTube Studio analytics: export every report, merge into one summary for LLMs")
    s = ap.add_subparsers(dest="cmd", required=True)
    c = s.add_parser("collect", help="export the reports (read-only) and write the summary")
    c.add_argument("--channel-id", help="UC... (default: the channel Studio opens with)")
    c.add_argument("--out", default=str(default_out("studio")), help="<out>/<channel>/<date>/")
    c.add_argument("--periods", default="7d,28d,90d,365d,lifetime")
    c.add_argument("--reports", default=",".join(DIMENSION_CANDIDATES), help="comma list; default all")
    c.add_argument("--refresh-catalog", action="store_true", help="forget cached Studio ids and probe again")
    c.add_argument("--resume", action="store_true", help="reuse today's folder: only (re)try reports that are missing or failed")
    c.add_argument("--no-summary", action="store_true")
    c.set_defaults(func=_run_collect)
    m = s.add_parser("summarize", help="merge an already collected folder into summary.md/json + videos.csv")
    m.add_argument("--dir", required=True, help="the <out>/<channel>/<date> folder with manifest.json")
    m.add_argument("--out", help="default: the same folder")
    m.set_defaults(func=_run_summarize)
