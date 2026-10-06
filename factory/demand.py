"""Đọc nhu cầu -- bước 3 lộ trình audit: 3 mục thêm vào brief tuần, cho pha sinh trong chat.

VÌ SAO: chủ đề hiện được chọn theo "dòng chưa dùng tiếp theo" trong bảng cố định;
không gì cho biết người xem đang quan tâm gì. Nghiên cứu nguồn hợp lệ, miễn phí:
docs/audit/2026-10-05-demand-sources-research.md. Thiết kế chốt với Grok:
docs/audit/2026-10-05-demand-design.md.

  (A) Từ khoá ĐÃ dẫn người xem tới kênh (Analytics của chính kênh, YT_SEARCH). Đây là
      nhu cầu kênh đã đáp ứng -- không phải "khoảng trống". Một truy vấn, top 25.
  (B) Mức quan tâm trên Wikipedia tiếng Việt cho danh sách chủ đề theo dõi (CC0).
      Mức = trung vị lượt xem/ngày 28 ngày; so cùng kỳ năm trước (mùa học, tin tức).
  (C) Khoảng trống thật: tab Trends của YouTube Studio, KHÔNG có API -> người dán tay.

Không đụng next_draft, không tự áp gì: chuyển nhu cầu thành chủ đề là việc của Claude
khi viết pack trong chat.
"""
from __future__ import annotations

import http.client
import json
import re
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

from factory.publish import PublishError

WINDOW = 28
MIN_FOR_YOY = 20                # lượt xem/ngày tối thiểu ở CẢ hai năm thì mới so
THROTTLE = 1.0                  # giây giữa hai request Wikimedia (0,4 s vẫn dính 429 khi đo thật 05/10)
FRESH = 2                       # 2 ngày gần nhất không cache: Wikimedia có thể chưa chốt số
STUDIO_MAX_AGE = 14


class WikiError(Exception):
    """Wikimedia không trả lời được (429/5xx/mạng) sau khi đã lùi."""


class ArticleMissing(WikiError):
    """404: sai tên bài, hoặc bài chưa có dữ liệu trong khoảng ngày đó."""


# ── (A) ──────────────────────────────────────────────────────────────────

@dataclass
class SearchTerms:
    rows: list[tuple[str, int]] = field(default_factory=list)
    note: str = ""


def search_terms(api, frontier: date | None) -> SearchTerms:
    """Top 25 từ khoá YT_SEARCH trong 28 ngày (gồm cả hai đầu) tới mốc Analytics.

    Mốc là mốc của bảng điểm (metrics_meta), không phải "hôm qua - 2" đoán mò.
    Rỗng thì nói rõ là rỗng; không thử lùi ngày để "tìm cho ra"."""
    if frontier is None:
        return SearchTerms(note="chưa có mốc Analytics -- chạy feedback_loop có đo trước")
    try:
        rows = api.top_search_terms(start=frontier - timedelta(days=WINDOW - 1), end=frontier)
    except PublishError:
        # 400, rate limit kéo dài, mất mạng, 5xx: mục này ghi "lỗi", brief và các
        # kênh sau vẫn chạy tiếp.
        return SearchTerms(note="lỗi")
    if not rows:
        return SearchTerms(note="không có dữ liệu (kênh chủ yếu có view từ feed Shorts, "
                                "hoặc lượt tìm dưới ngưỡng riêng tư của YouTube)")
    return SearchTerms(rows=[(r["insightTrafficSourceDetail"], int(r["views"])) for r in rows])


# ── (B) ──────────────────────────────────────────────────────────────────

_SCHEMA = """
CREATE TABLE IF NOT EXISTS wiki_daily (
    article  TEXT NOT NULL,
    day      TEXT NOT NULL,
    views    INTEGER NOT NULL,      -- 0 = Wikimedia không có số ngày đó (bài có tồn tại)
    PRIMARY KEY (article, day)
);
"""


@dataclass
class Interest:
    topic: str
    articles: list[str]
    level: float | None            # trung vị lượt xem/ngày (tổng các bài) 28 ngày gần nhất
    yoy: float | None              # level / cùng kỳ năm trước
    label: str                     # "" | "chưa có cùng kỳ" | "chưa đủ" | "thiếu: <bài>"

    @property
    def n_articles(self) -> int:
        return len(self.articles)


def _days(start: date, end: date) -> list[date]:
    return [start + timedelta(days=k) for k in range((end - start).days + 1)]


def _series(conn, wiki, article: str, start: date, end: date, cutoff: date, sleep) -> dict[date, int]:
    """Lượt xem từng ngày [start, end]; chỉ hỏi Wikimedia phần chưa có trong cache.

    Ngày Wikimedia bỏ trống = 0 khi TÍNH, nhưng chỉ GHI cache khi chắc chắn: ngày có
    trong payload, hoặc có một ngày muộn hơn trong cùng payload (dump đã chạy qua nó).
    404 khi cache đã có phần còn lại của cửa sổ = phần đuôi chưa có số: tính 0, không
    ghi. 404 khi cache trống: ném ArticleMissing, không ghi gì. Lỗi hay không thì vẫn
    giãn nhịp trước request kế tiếp."""
    cached = {date.fromisoformat(d): v for d, v in conn.execute(
        "SELECT day, views FROM wiki_daily WHERE article = ? AND day BETWEEN ? AND ?",
        (article, start.isoformat(), end.isoformat()))}
    missing = [d for d in _days(start, end) if d not in cached]
    if missing:
        try:
            got = wiki.daily(article, missing[0], missing[-1])
        except ArticleMissing:
            if not cached:
                raise
            got = {}
        finally:
            sleep(THROTTLE)
        last = max(got) if got else None
        for d in _days(missing[0], missing[-1]):
            v = int(got.get(d, 0))
            cached[d] = v
            if d <= cutoff and (d in got or (last is not None and d < last)):
                conn.execute("INSERT OR REPLACE INTO wiki_daily (article, day, views) VALUES (?, ?, ?)",
                             (article, d.isoformat(), v))
    return {d: cached.get(d, 0) for d in _days(start, end)}


def interest(conn, wiki, topics: list[dict], *, today: date, sleep=time.sleep) -> list[Interest]:
    """Mức quan tâm từng chủ đề, sắp giảm dần. Mức của chủ đề = trung vị của TỔNG
    theo ngày các bài (cộng trung vị từng bài sẽ thưởng chủ đề bị tách nhiều bài)."""
    conn.executescript(_SCHEMA)
    end = today - timedelta(days=1)                        # Wikimedia: tới hôm qua UTC
    start = end - timedelta(days=WINDOW - 1)
    p_start, p_end = start - timedelta(days=365), end - timedelta(days=365)   # 365 ngày: 29/02 vô hại
    cutoff = end - timedelta(days=FRESH)
    out = []
    for t in topics:
        arts = list(t["articles"])
        recent, failed = [], []
        for a in arts:
            try:
                recent.append(_series(conn, wiki, a, start, end, cutoff, sleep))
            except WikiError:
                failed.append(a)          # 404 = sai tên? lỗi mạng? -- ghi tên để chủ kênh sửa
        if failed:
            out.append(Interest(t["topic"], arts, None, None, "thiếu: " + ", ".join(failed)))
            continue
        level = statistics.median(sum(s[d] for s in recent) for d in _days(start, end))
        prior, failed = [], []
        for a in arts:
            try:
                prior.append(_series(conn, wiki, a, p_start, p_end, cutoff, sleep))
            except ArticleMissing:
                # Bài chưa có năm ngoái: chuỗi 0 trong bộ nhớ (không ghi) -- không
                # được xoá phép so của các bài cùng chủ đề.
                prior.append({d: 0 for d in _days(p_start, p_end)})
            except WikiError:
                failed.append(a)
        if failed:
            out.append(Interest(t["topic"], arts, level, None, "thiếu năm trước: " + ", ".join(failed)))
            continue
        p_level = statistics.median(sum(s[d] for s in prior) for d in _days(p_start, p_end))
        p_total = sum(sum(s.values()) for s in prior)
        if not p_total:
            out.append(Interest(t["topic"], arts, level, None, "chưa có cùng kỳ"))
        elif level >= MIN_FOR_YOY and p_level >= MIN_FOR_YOY:
            out.append(Interest(t["topic"], arts, level, round(level / p_level, 2), ""))
        else:
            out.append(Interest(t["topic"], arts, level, None, "chưa đủ"))
    return sorted(out, key=lambda r: (r.level is None, -(r.level or 0)))


class HttpPageviews:
    """Wikimedia Pageviews REST API (vi.wikipedia, agent=user). Dữ liệu CC0; phải có
    User-Agent định danh kèm liên hệ; lùi khi 429."""

    BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/vi.wikipedia/all-access/user"
    UA = "yt-factory-demand/1.0 (https://github.com/nguyent0810/Youtube_Creator_V2)"

    def __init__(self, *, urlopen=urllib.request.urlopen, sleep=time.sleep):
        self._urlopen, self._sleep = urlopen, sleep

    def daily(self, article: str, start: date, end: date) -> dict[date, int]:
        url = (f"{self.BASE}/{urllib.parse.quote(article, safe='')}/daily/"
               f"{start:%Y%m%d}00/{end:%Y%m%d}00")
        for wait in (2, 6, 18, None):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": self.UA})
                with self._urlopen(req, timeout=30) as r:
                    items = json.loads(r.read()).get("items", [])
                return {date(int(i["timestamp"][:4]), int(i["timestamp"][4:6]), int(i["timestamp"][6:8])):
                        int(i["views"]) for i in items}
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    raise ArticleMissing(article) from e
                if wait is None or (e.code != 429 and e.code < 500):
                    raise WikiError(f"{article}: HTTP {e.code}") from e
            except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException) as e:
                if wait is None:
                    raise WikiError(f"{article}: {e}") from e
            except (ValueError, KeyError, TypeError) as e:     # JSON hỏng / thiếu trường
                raise WikiError(f"{article}: phản hồi lạ ({e})") from e
            self._sleep(wait)


# ── (C) ──────────────────────────────────────────────────────────────────

def studio_gaps(path: Path, *, today: date) -> str:
    """Khoảng trống nội dung từ YouTube Studio → Analytics → Research/Trends. Không có API
    nên người dán tay; chỉ dùng khi dòng 'Ngày: YYYY-MM-DD' trong file còn ≤ 14 ngày."""
    howto = (f"mở YouTube Studio → Analytics → tab Research (Trends), dán các chủ đề người xem đang tìm "
             f"vào `{path.as_posix()}`, dòng đầu ghi `Ngày: YYYY-MM-DD`.")
    if not path.exists():
        return f"_Chưa có. Mỗi tuần: {howto}_"
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*Ngày:\s*(\d{4}-\d{2}-\d{2})", text)          # chỉ dòng đầu
    when = date.fromisoformat(m.group(1)) if m else None
    if when is None or not 0 <= (today - when).days <= STUDIO_MAX_AGE:
        return f"_Bản dán đã cũ hoặc thiếu ngày ({when or 'không ghi ngày'}). Cập nhật: {howto}_"
    return f"_Dán tay ngày {when}:_\n\n{text.strip()}"


# ── Brief ────────────────────────────────────────────────────────────────

def load_watchlist(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))["topics"]


def render_demand(conn, code: str, api, wiki, *, frontier: date | None, today: date,
                  watchlist: list[dict], studio_file: Path, sleep=time.sleep) -> str:
    L = ["", "## Nhu cầu: từ khoá đã dẫn người xem tới kênh", "",
         "Đây là nhu cầu kênh **đã** đáp ứng (người ta tìm và ra video của mình), không phải khoảng trống. "
         f"28 ngày tới mốc Analytics {frontier or '—'}, top 25.", ""]
    st = search_terms(api, frontier)
    if st.rows:
        L += ["| Từ khoá | View |", "|---|---:|"] + [f"| {t.replace('|', chr(92) + '|')} | {v:,} |"
                                                      for t, v in st.rows]
    else:
        L.append(f"_{st.note}_")

    L += ["", "## Nhu cầu: mức quan tâm (Wikipedia tiếng Việt)", "",
          "Lượt xem/ngày (trung vị 28 ngày, người dùng thật) của các chủ đề theo dõi; so với cùng kỳ năm trước "
          f"khi cả hai năm ≥ {MIN_FOR_YOY}/ngày. Đo mức quan tâm tìm hiểu, không phải nhu cầu xem video. "
          "Nguồn: Wikimedia Pageviews (CC0).", ""]
    if not watchlist:
        L.append(f"_Chưa có danh sách theo dõi: tạo `data/demand/{code}.json`._")
    else:
        L += ["| Chủ đề | Lượt xem/ngày | So cùng kỳ | Số bài |", "|---|---:|---|---:|"]
        for r in interest(conn, wiki, watchlist, today=today, sleep=sleep):
            lvl = "—" if r.level is None else f"{r.level:,.0f}"
            cmp_ = f"×{r.yoy:.2f}" if r.yoy is not None else r.label
            L.append(f"| {r.topic} | {lvl} | {cmp_} | {r.n_articles} |")

    L += ["", "## Nhu cầu: khoảng trống (YouTube Studio → Trends, dán tay)", "", studio_gaps(studio_file, today=today)]
    return "\n".join(L) + "\n"
