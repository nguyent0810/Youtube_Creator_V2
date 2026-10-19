"""Bảng điểm -- nửa sau của vòng phản hồi: đo đúng tuổi, so trong tuần, gợi ý có điều kiện.

VÌ SAO (audit 05/10/2026, docs/audit/2026-10-05-feedback-loop-design.md):
scripts/analytics_report.py đã đo được views / % xem / nguồn traffic, nhưng so
video 1 ngày tuổi với video 2 tuần tuổi, ghi ra file rồi để đó. Không quyết
định nào của máy (chủ đề, giờ, số bài mỗi dòng) đọc lại số liệu.

Module này:
  - đo MỖI video ở CÙNG một tuổi: 3 ngày đầu kể từ giờ lên sóng thật, tính
    theo ngày giờ Thái Bình Dương như YouTube Analytics;
  - so bằng thứ hạng engagedViews TRONG CÙNG TUẦN của cùng kênh -- cú sốc cấp
    kênh (CL dồn upload 30/09, cập nhật Shorts 01/10) không bị tính vào dòng;
  - chỉ gợi ý giờ đăng khi thí nghiệm xoay giờ (factory/rotation.py) đã cho
    đủ dữ liệu; không bao giờ tự áp.
"""
from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

from factory.analytics import ReportRejected
from factory.publish import PublishError


def _nth_sunday(year: int, month: int, n: int) -> date:
    d = date(year, month, 1)
    d += timedelta(days=(6 - d.weekday()) % 7)        # Chủ nhật đầu tiên
    return d + timedelta(weeks=n - 1)


def pacific_date(t: datetime) -> date:
    """Ngày lịch giờ Thái Bình Dương của một thời điểm UTC.

    YouTube Analytics chia ngày theo giờ PT. Windows không có tzdata nên tự
    tính luật giờ mùa hè của Mỹ: PDT (UTC-7) từ 02:00 giờ chuẩn Chủ nhật thứ
    hai tháng 3 (= 10:00 UTC) tới 02:00 giờ mùa hè Chủ nhật đầu tháng 11
    (= 09:00 UTC); còn lại PST (UTC-8)."""
    t = t.astimezone(timezone.utc)
    start = datetime.combine(_nth_sunday(t.year, 3, 2), datetime.min.time(), timezone.utc) + timedelta(hours=10)
    end = datetime.combine(_nth_sunday(t.year, 11, 1), datetime.min.time(), timezone.utc) + timedelta(hours=9)
    offset = -7 if start <= t < end else -8
    return (t + timedelta(hours=offset)).date()


# ── Đo: mỗi video một dòng, cửa sổ 3 ngày đầu ─────────────────────────────

# 7 ngày PT, không phải 3: dữ liệu chỉ có theo NGÀY PT, nên cửa sổ "3 ngày" thật
# ra dài 51 giờ nếu lên sóng 20:30 PT nhưng 71 giờ nếu 00:30 PT -- thí nghiệm
# xoay giờ sẽ đo nhầm độ dài cửa sổ. 7 ngày: 147-167 giờ, lệch ~7%.
WINDOW_DAYS = 7
_ISO = "%Y-%m-%dT%H:%M:%SZ"
_COHORT = 500                     # filters=video tối đa 500 id mỗi truy vấn

_SCHEMA = """
CREATE TABLE IF NOT EXISTS video_metrics (
    channel        TEXT NOT NULL,
    slug           TEXT NOT NULL,
    video_id       TEXT NOT NULL,
    kind           TEXT NOT NULL,          -- short | long
    go_live        TEXT NOT NULL,          -- UTC, giờ lên sóng thật
    pacific_date   TEXT NOT NULL,          -- ngày PT của go_live = ngày 0 của cửa sổ
    slot_vn        TEXT NOT NULL,          -- HH:MM giờ VN lúc lên sóng
    views          INTEGER NOT NULL,
    engaged_views  INTEGER,                -- NULL = API từ chối engagedViews: KHÔNG xếp hạng
    shorts_views   INTEGER,                -- NULL = không đọc được nguồn traffic
    avd            REAL,                   -- giây, cả cửa sổ (không lấy trung bình theo ngày)
    avp            REAL,
    duration_s     INTEGER,
    collected_at   TEXT NOT NULL,
    PRIMARY KEY (channel, slug)
);
CREATE TABLE IF NOT EXISTS metrics_meta (
    channel   TEXT PRIMARY KEY,
    frontier  TEXT                         -- ngày PT mới nhất Analytics đã có số, lần đo gần nhất
);
"""


def _parse(s: str) -> datetime:
    return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)


def _go_live(facts: dict, now: datetime) -> datetime | None:
    """Giờ lên sóng thật, hoặc None nếu chưa lên sóng.

    Public: snippet.publishedAt (YouTube đặt bằng giờ công khai). Private có
    publishAt: lên sóng lúc publishAt -- chưa tới thì chưa sống. Private không
    lịch (probe, gỡ lịch) hay unlisted: không đo."""
    if facts.get("privacy") == "public" and facts.get("published_at"):
        return _parse(facts["published_at"])
    if facts.get("privacy") == "private" and facts.get("publish_at"):
        t = _parse(facts["publish_at"])
        return t if t <= now else None
    return None


def _kind(slug: str) -> str:
    return "long" if slug.startswith("long-") else "short"


def _frontier(api, now: datetime) -> date | None:
    """Ngày PT mới nhất Analytics đã có số. Không có tài liệu nào hứa độ trễ
    cố định, nên hỏi thẳng: một truy vấn theo ngày cho cả kênh."""
    today = pacific_date(now)
    rows = api.report(start=today - timedelta(days=30), end=today, metrics="views", dimensions="day")
    days = [date.fromisoformat(r["day"]) for r in rows]
    return max(days) if days else None


def collect(conn, code: str, api, *, now: datetime) -> dict:
    """Đo mọi video đã đăng của kênh mà cửa sổ 3 ngày đã ĐÓNG và chưa đo.

    Gom theo ngày lên sóng (PT): cả nhóm chung một cửa sổ nên một truy vấn
    cho tất cả. Chạy lại bao nhiêu lần cũng vô hại: video đã đo không hỏi lại."""
    prepare(conn, code)
    rows = list(conn.execute(
        "SELECT slug, video_id FROM upload_log WHERE channel = ? AND state = 'done' "
        "AND video_id IS NOT NULL AND slug NOT IN (SELECT slug FROM video_metrics WHERE channel = ?)",
        (code, code)))
    out = {"stored": 0, "open": 0, "not_live": 0, "gone": 0, "failed": 0, "frontier": _frontier(api, now)}
    if out["frontier"]:
        conn.execute("INSERT OR REPLACE INTO metrics_meta (channel, frontier) VALUES (?, ?)",
                     (code, out["frontier"].isoformat()))
    if not rows:
        return out
    facts = api.video_facts([r["video_id"] for r in rows])
    cohorts: dict[date, list[tuple[str, str, datetime, dict]]] = {}
    for r in rows:
        f = facts.get(r["video_id"])
        if f is None:
            out["gone"] += 1                 # video đã xoá khỏi kênh
            continue
        live = _go_live(f, now)
        if live is None:
            out["not_live"] += 1
            continue
        cohorts.setdefault(pacific_date(live), []).append((r["slug"], r["video_id"], live, f))
    for day0, members in sorted(cohorts.items()):
        end = day0 + timedelta(days=WINDOW_DAYS - 1)
        if out["frontier"] is None or end > out["frontier"]:
            out["open"] += len(members)
            continue
        for i in range(0, len(members), _COHORT):
            chunk = members[i:i + _COHORT]
            try:
                out["stored"] += _store_cohort(conn, code, api, day0, end, chunk, now)
            except PublishError:
                # 400 lần hai, rate limit kéo dài, 5xx...: không ghi gì cho nhóm
                # này (lần chạy sau thử lại), các nhóm khác vẫn đo tiếp.
                out["failed"] += len(chunk)
    return out


def _store_cohort(conn, code, api, day0, end, members, now) -> int:
    ids = [m[1] for m in members]
    base = "views,averageViewDuration,averageViewPercentage"
    try:
        per = api.report(start=day0, end=end, metrics="engagedViews," + base, dimensions="video", video_ids=ids)
        engaged_ok = True
    except ReportRejected:
        # Lấy lại không có engagedViews. Lần này được -> chính metric đó bị từ
        # chối: lưu NULL, không bao giờ chép views sang cột xếp hạng. Lần này
        # cũng hỏng -> lỗi khác: ném ra, nhóm này để lần chạy sau.
        per = api.report(start=day0, end=end, metrics=base, dimensions="video", video_ids=ids)
        engaged_ok = False
    by_video = {r["video"]: r for r in per}
    shorts = _shorts_views(api, day0, end, ids)
    stamp = now.strftime(_ISO)
    for slug, vid, live, f in members:
        r = by_video.get(vid, {})           # không có dòng = 0 view trong cửa sổ
        conn.execute(
            "INSERT OR REPLACE INTO video_metrics (channel, slug, video_id, kind, go_live, pacific_date, "
            "slot_vn, views, engaged_views, shorts_views, avd, avp, duration_s, collected_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (code, slug, vid, _kind(slug), live.strftime(_ISO), day0.isoformat(),
             (live + timedelta(hours=7)).strftime("%H:%M"), int(r.get("views") or 0),
             int(r.get("engagedViews") or 0) if engaged_ok else None,
             shorts.get(vid, 0) if shorts is not None else None,
             r.get("averageViewDuration"), r.get("averageViewPercentage"), f.get("duration_s"), stamp))
    return len(members)


def _shorts_views(api, day0, end, ids) -> dict[str, int] | None:
    """View từ feed Shorts của từng video. Một truy vấn cho cả nhóm; bị từ
    chối thì hỏi từng video; vẫn hỏng thì None (không biết), không phải 0."""
    try:
        rows = api.report(start=day0, end=end, metrics="views", video_ids=ids,
                          dimensions="video,insightTrafficSourceType")
        out: dict[str, int] = {}
        for r in rows:
            if r["insightTrafficSourceType"] == "SHORTS":
                out[r["video"]] = out.get(r["video"], 0) + int(r["views"] or 0)
        return out
    except ReportRejected:
        pass
    try:
        out = {}
        for vid in ids:
            rows = api.report(start=day0, end=end, metrics="views", video_ids=[vid],
                              dimensions="insightTrafficSourceType")
            out[vid] = sum(int(r["views"] or 0) for r in rows if r["insightTrafficSourceType"] == "SHORTS")
        return out
    except ReportRejected:
        return None


def prepare(conn, code: str) -> None:
    """Tạo bảng (và sổ upload_log) nếu chưa có."""
    from factory.channel import Channel
    Channel(code, None, conn)
    conn.executescript(_SCHEMA)


# ── So sánh: thứ hạng trong tuần, bảng điểm, gợi ý có điều kiện ───────────

REGIME_START = date(2026, 10, 5)  # thứ Hai đầu tiên SAU cú dồn upload 30/09 + cập nhật Shorts 01/10
MIN_POOL = 15                     # tuần ít video hơn: hiển thị, không dùng để gợi ý
MIN_CELL = 5                      # mỗi ô (dòng × giờ) cần ít nhất 5 video ...
MIN_CELL_WEEKS = 2                # ... từ ít nhất 2 tuần khác nhau
MIN_GAP = 0.25                    # chênh thứ hạng tối thiểu để gợi ý (≈ 9 bậc trong tuần 35 video)
# Bảng điểm và gợi ý chỉ nhìn 4 TUẦN ĐÃ ĐÓNG gần nhất (dòng có thể "mỏi", giờ cũ
# hết hiệu lực). Không dùng "28 ngày lịch": một tuần chỉ đóng sau 6 + 7 - 1 = 12
# ngày, nên 28 ngày lịch chỉ còn ~16 ngày dùng được -- mỗi ô giờ ~4 video, gợi ý
# không bao giờ đạt n ≥ 5 (Grok vòng 4).
LOOKBACK_WEEKS = 4


@dataclass
class Ranked:
    slug: str
    kind: str
    line: str
    slot: str
    pacific_date: date
    views: int
    engaged: int
    rank: float                   # 0 = đáy tuần, 1 = đỉnh tuần
    pool: int


@dataclass
class Week:
    start: date
    kind: str
    n: int
    ranked: bool
    why: str = ""


@dataclass
class Suggestion:
    line: str
    best_slot: str
    worst_slot: str
    best_rank: float
    worst_rank: float
    best_views: float
    worst_views: float
    n_best: int
    n_worst: int


@dataclass
class Board:
    code: str
    frontier: date | None
    weeks: list[Week]
    ranked: list[Ranked]          # mọi video đã xếp hạng (sau mốc 05/10)
    recent: list[Ranked]          # 4 tuần đã đóng gần nhất -- dùng cho bảng điểm và gợi ý
    unranked: int                 # đã đo nhưng không xếp hạng (tuần mở, engagedViews NULL, ...)
    suggestions: list[Suggestion]
    slot_note: str
    rows: dict[str, dict] = field(default_factory=dict)   # slug -> dòng video_metrics


def _line(code: str, slug: str) -> str:
    from factory import channels
    prefixes = list(channels.CHANNELS[code]["prefixes"]) + ["long-"]
    match = [p for p in prefixes if slug.startswith(p)]
    return max(match, key=len) if match else slug.split("-")[0] + "-"


def _midranks(values: list[float]) -> list[float]:
    """Thứ hạng phần trăm 0..1, hoà thì chia đều (midrank). Nhiều short nằm
    cùng một "sàn" view: xếp ổn định sẽ bịa ra khoảng cách giữa các giờ."""
    n = len(values)
    if n == 1:
        return [0.5]
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        mid = (i + j) / 2               # vị trí 0-based trung bình của nhóm hoà
        for k in range(i, j + 1):
            ranks[order[k]] = mid / (n - 1)
        i = j + 1
    return ranks


def board(conn, code: str, *, frontier: date | None) -> Board:
    """frontier=None: dùng mốc đã ghi ở lần đo gần nhất (dựng lại brief không cần mạng)."""
    prepare(conn, code)
    if frontier is None:
        row = conn.execute("SELECT frontier FROM metrics_meta WHERE channel = ?", (code,)).fetchone()
        frontier = date.fromisoformat(row[0]) if row and row[0] else None
    rows = [dict(r) for r in conn.execute("SELECT * FROM video_metrics WHERE channel = ?", (code,))]
    groups: dict[tuple[date, str], list[dict]] = {}
    for r in rows:
        d = date.fromisoformat(r["pacific_date"])
        groups.setdefault((d - timedelta(days=d.weekday()), r["kind"]), []).append(r)

    weeks, ranked = [], []
    for (start, kind), members in sorted(groups.items()):
        pool = [m for m in members if m["engaged_views"] is not None]
        if start < REGIME_START:
            weeks.append(Week(start, kind, len(members), False, "trước mốc 05/10 (lẫn cú sốc 30/09, 01/10)"))
            continue
        if frontier is None or frontier < start + timedelta(days=6 + WINDOW_DAYS - 1):
            weeks.append(Week(start, kind, len(members), False, "tuần chưa đóng"))
            continue
        if len(pool) < MIN_POOL:
            # Pool 2 video thì hạng chỉ là 0 hoặc 1: một video dài sẽ đứng đầu
            # brief của Shorts. Hiển thị trong danh sách tuần, không xếp hạng.
            weeks.append(Week(start, kind, len(members), False, f"dưới {MIN_POOL} video có engagedViews"))
            continue
        weeks.append(Week(start, kind, len(members), True))
        for m, rk in zip(pool, _midranks([m["engaged_views"] for m in pool])):
            ranked.append(Ranked(m["slug"], kind, _line(code, m["slug"]), m["slot_vn"],
                                 date.fromisoformat(m["pacific_date"]), m["views"], m["engaged_views"],
                                 rk, len(pool)))
    recent_weeks = set()
    if frontier is not None:
        last = frontier - timedelta(days=6 + WINDOW_DAYS - 1)      # thứ Hai muộn nhất của tuần đã đóng
        last -= timedelta(days=last.weekday())
        recent_weeks = {last - timedelta(weeks=k) for k in range(LOOKBACK_WEEKS)}
    recent = [r for r in ranked if r.pacific_date - timedelta(days=r.pacific_date.weekday()) in recent_weeks]

    from factory import channels
    rotates = bool(channels.CHANNELS[code].get("rotate"))
    # Gợi ý chỉ từ 4 tuần đã đóng gần nhất và chỉ Shorts -- thí nghiệm xoay
    # giờ chỉ áp cho Shorts.
    suggestions = _suggest([r for r in recent if r.kind == "short"]) if rotates else []
    note = ("" if rotates else
            f"Kênh {code} không xoay giờ: dòng và giờ đăng vẫn là một biến -- chưa tách được hiệu ứng giờ.")
    return Board(code, frontier, weeks, ranked, recent, len(rows) - len(ranked), suggestions, note,
                 {r["slug"]: r for r in rows})


def _suggest(ranked: list[Ranked]) -> list[Suggestion]:
    cells: dict[tuple[str, str], list[Ranked]] = {}
    for r in ranked:
        cells.setdefault((r.line, r.slot), []).append(r)
    out = []
    for line in sorted({ln for ln, _ in cells}):
        ok = []
        for (ln, slot), rs in cells.items():
            weeks = {r.pacific_date - timedelta(days=r.pacific_date.weekday()) for r in rs}
            if ln == line and len(rs) >= MIN_CELL and len(weeks) >= MIN_CELL_WEEKS:
                ok.append((statistics.median(r.rank for r in rs), slot, rs))
        if len(ok) < 2:
            continue
        ok.sort()
        (lo_rank, lo_slot, lo), (hi_rank, hi_slot, hi) = ok[0], ok[-1]
        if hi_rank - lo_rank >= MIN_GAP:
            out.append(Suggestion(line, hi_slot, lo_slot, hi_rank, lo_rank,
                                  statistics.median(r.views for r in hi), statistics.median(r.views for r in lo),
                                  len(hi), len(lo)))
    return out


# ── Brief: thứ pha sinh trong chat đọc trước khi viết bundle mới ──────────

def _topic(code: str, slug: str, fallback_title: str | None) -> dict:
    """Tiêu đề, câu mở đầu, chủ đề (key/angle) từ bundle. Video dài không có
    bundle: chỉ còn tiêu đề trong sổ upload."""
    from factory import store
    from factory.bundle import BundleInvalid
    try:
        b = store.load_bundle(code, slug)
    except BundleInvalid:              # video dài / S-tier cũ: không có bundle
        return {"title": fallback_title or slug, "first": "", "key": "", "angle": ""}
    meta = {}
    if b.source_note.startswith("pillar="):
        meta = dict(kv.split("=", 1) for kv in b.source_note.split(" | ")[0].split(";") if "=" in kv)
    first = re.split(r"(?<=[.?!…])\s+", b.script.strip(), maxsplit=1)[0]
    return {"title": b.title, "first": first, "key": meta.get("key", ""), "angle": meta.get("angle", "")}


def _q(xs: list[float], p: float) -> float:
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def render_brief(b: Board) -> str:
    titles = {}
    L = [f"# Bảng điểm kênh {b.code}",
         "",
         f"Số liệu Analytics tới ngày PT **{b.frontier or '—'}**. Mỗi video đo ở cùng tuổi: `engagedViews` "
         f"{WINDOW_DAYS} ngày đầu kể từ giờ lên sóng (tính theo ngày giờ PT). **Hạng** = vị trí trong tuần của chính kênh (0 = đáy, 1 = đỉnh), "
         "nên cú sốc cả kênh không bị tính vào dòng. View thô luôn in kèm.",
         "",
         f"Đã xếp hạng {len(b.ranked)} video; {b.unranked} video đã đo nhưng chưa xếp hạng "
         f"(tuần chưa đóng, trước mốc 05/10, tuần dưới {MIN_POOL} video, hoặc thiếu engagedViews).",
         "",
         "## Theo dòng (4 tuần đã đóng gần nhất)",
         ""]
    by_line: dict[str, list[Ranked]] = {}
    for r in b.recent:
        by_line.setdefault(r.line, []).append(r)
    if by_line:
        L += ["| Dòng | n | Hạng trung vị | IQR | View trung vị | Engaged trung vị |",
              "|---|---|---|---|---|---|"]
        for line, rs in sorted(by_line.items(), key=lambda kv: -statistics.median(r.rank for r in kv[1])):
            ranks = [r.rank for r in rs]
            L.append(f"| `{line}` | {len(rs)} | {statistics.median(ranks):.2f} | "
                     f"{_q(ranks, .25):.2f}–{_q(ranks, .75):.2f} | {statistics.median(r.views for r in rs):,.0f} | "
                     f"{statistics.median(r.engaged for r in rs):,.0f} |")
    else:
        L.append("_Chưa có tuần nào đóng trong 4 tuần gần nhất._")

    def video_line(r: Ranked) -> str:
        t = titles.setdefault(r.slug, _topic(b.code, r.slug, None))
        topic = " · ".join(x for x in (t["key"], t["angle"]) if x)
        first = f' — "{t["first"]}"' if t["first"] else ""
        return (f"- **{r.rank:.2f}** · {r.views:,} view · {r.slot} · {t['title']}{first}"
                + (f" · _{topic}_" if topic else ""))

    ordered = sorted(b.recent, key=lambda r: r.rank, reverse=True)
    L += ["", "## Cao nhất (4 tuần đã đóng)", ""] + [video_line(r) for r in ordered[:5]]
    L += ["", "## Thấp nhất (4 tuần đã đóng)", ""] + [video_line(r) for r in ordered[5:][-5:][::-1]]

    L += ["", "## Góc trong từng dòng → viết thêm kiểu nào", "",
          "Góc xếp trên = trong 4 tuần đã đóng gần nhất thường đứng cao hơn trong tuần. n nhỏ thì chỉ là gợi ý.", ""]
    for line, rs in sorted(by_line.items()):
        angles: dict[str, list[float]] = {}
        for r in rs:
            t = titles.setdefault(r.slug, _topic(b.code, r.slug, None))
            angles.setdefault(t["angle"] or "(không ghi góc)", []).append(r.rank)
        L.append(f"### `{line}`")
        for angle, ranks in sorted(angles.items(), key=lambda kv: -statistics.median(kv[1])):
            L.append(f"- {angle}: hạng trung vị {statistics.median(ranks):.2f} (n={len(ranks)})")
        L.append("")

    L += ["## Giờ đăng", ""]
    if b.slot_note:
        L.append(b.slot_note)
    elif b.suggestions:
        L.append("Gợi ý (KHÔNG tự áp — người quyết). Chỉ hiện khi mỗi giờ có ≥ 5 video từ ≥ 2 tuần đủ 15 video "
                 "và chênh ≥ 0,25 hạng:")
        for s in b.suggestions:
            L.append(f"- `{s.line}`: {s.best_slot} tốt hơn {s.worst_slot} — hạng {s.best_rank:.2f} vs "
                     f"{s.worst_rank:.2f}; view trung vị {s.best_views:,.0f} vs {s.worst_views:,.0f} "
                     f"(n={s.n_best}/{s.n_worst})")
    else:
        L.append("Thí nghiệm xoay giờ đang chạy; chưa đủ dữ liệu để gợi ý giờ cố định.")

    L += ["", "## Các tuần", ""]
    for w in b.weeks:
        L.append(f"- {w.start} ({w.kind}, {w.n} video): " + ("đã xếp hạng" if w.ranked else w.why))
    return "\n".join(L) + "\n"
