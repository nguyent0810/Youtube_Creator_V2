"""Sequential, read-only scanner for approved editorial trend sources."""
from __future__ import annotations

import json
import html
import re
import sqlite3
import statistics
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from .sources import load_sources

DEFAULT_DB = Path("data/trend/trend.sqlite")
GDELT_MIN_WAIT_SECONDS = 5.0
ROBOTS_CACHE_HOURS = 24
FEED_MIN_INTERVAL = timedelta(hours=3)
# Lead replaces this contact before a production scan. SEC and Wikimedia require one.
USER_AGENT = "Youtube-Creator-Trend-Scanner/1.0 trend-contact@example.invalid"
WIKI_NAMESPACES = {"special:", "wikipedia:", "file:", "image:", "category:", "template:", "help:", "portal:", "module:", "draft:", "talk:", "user:", "media:", "thành viên:", "đặc biệt:", "tập tin:", "thể loại:", "bản mẫu:", "trợ giúp:"}
WIKI_NON_ARTICLES = {"main page", "main_page", "trang chinh", "trang_chinh"}
HTML_ENTITY = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]+);")
HTML_TAG = re.compile(r"<[^>]+>")


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat()


def normal(value: str) -> str:
    value = "".join(char for char in unicodedata.normalize("NFD", value.lower()) if unicodedata.category(char) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", value.replace("đ", "d")).strip()


def normalize_text(value: str, *, strip_html: bool = False) -> str:
    """Decode up to two HTML-entity layers and make stored text comparable."""
    cleaned = value
    for _ in range(2):
        decoded = html.unescape(cleaned)
        if decoded == cleaned:
            break
        cleaned = decoded
        if not HTML_ENTITY.search(cleaned):
            break
    if strip_html:
        cleaned = HTML_TAG.sub(" ", cleaned)
    return " ".join(unicodedata.normalize("NFC", cleaned).split())


def normalize_stored_articles(conn: sqlite3.Connection) -> int:
    """Migrate previously stored article text without changing article identity."""
    updates = []
    for row in conn.execute("SELECT id, title, summary FROM article"):
        title = normalize_text(str(row["title"]))
        summary = normalize_text(str(row["summary"]), strip_html=True)
        if title != row["title"] or summary != row["summary"]:
            updates.append((title, summary, row["id"]))
    if updates:
        conn.executemany("UPDATE article SET title=?, summary=? WHERE id=?", updates)
    return len(updates)


def valid_wiki_title(title: str) -> bool:
    folded = normal(title)
    return bool(folded) and folded not in WIKI_NON_ARTICLES and not any(folded.startswith(normal(prefix)) for prefix in WIKI_NAMESPACES)


def init_db(db_path: Path | str = DEFAULT_DB) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS article (
          id INTEGER PRIMARY KEY, url TEXT NOT NULL UNIQUE, title TEXT NOT NULL, summary TEXT NOT NULL,
          published_at TEXT NOT NULL, source_id TEXT NOT NULL, owner_group TEXT NOT NULL, fetched_at TEXT NOT NULL,
          undated INTEGER NOT NULL DEFAULT 0, trend_title TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS signal (
          id INTEGER PRIMARY KEY, source_id TEXT NOT NULL, title TEXT NOT NULL, normalized_title TEXT NOT NULL,
          observed_at TEXT NOT NULL, value REAL, baseline REAL, kind TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS run (
          id INTEGER PRIMARY KEY, started_at TEXT NOT NULL, ended_at TEXT, source_id TEXT, status TEXT NOT NULL,
          error TEXT, article_count INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS event (
          id TEXT PRIMARY KEY, label TEXT NOT NULL, entities TEXT NOT NULL, first_seen TEXT NOT NULL,
          last_seen TEXT NOT NULL, article_ids TEXT NOT NULL, signals TEXT NOT NULL DEFAULT '[]'
        );
        CREATE TABLE IF NOT EXISTS robots_cache (
          domain TEXT PRIMARY KEY, fetched_at TEXT NOT NULL, body TEXT NOT NULL
        );
        """)
    event_columns = {row[1] for row in conn.execute("PRAGMA table_info(event)")}
    if "signals" not in event_columns:
        conn.execute("ALTER TABLE event ADD COLUMN signals TEXT NOT NULL DEFAULT '[]'")
    article_columns = {row[1] for row in conn.execute("PRAGMA table_info(article)")}
    if "undated" not in article_columns:
        conn.execute("ALTER TABLE article ADD COLUMN undated INTEGER NOT NULL DEFAULT 0")
    if "trend_title" not in article_columns:
        conn.execute("ALTER TABLE article ADD COLUMN trend_title TEXT NOT NULL DEFAULT ''")
    conn.commit()
    return conn


def _robots_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


def _robots_rules(body: str, user_agent: str = USER_AGENT) -> tuple[list[tuple[str, bool]], float | None]:
    """Return the most-specific robots rules and Crawl-delay for our named agent."""
    groups: list[tuple[list[str], list[tuple[str, str]]]] = []
    agents: list[str] = []
    directives: list[tuple[str, str]] = []
    for raw_line in body.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if directives:
                groups.append((agents, directives)); agents, directives = [], []
            agents.append(value.lower())
        elif key in {"allow", "disallow", "crawl-delay"} and agents:
            directives.append((key, value))
    if agents:
        groups.append((agents, directives))
    agent = user_agent.split("/", 1)[0].lower()
    matches = [(max((len(name) for name in names if name != "*" and agent.startswith(name)), default=0), rules)
               for names, rules in groups if "*" in names or any(agent.startswith(name) for name in names)]
    if not matches:
        return [], None
    specificity = max(score for score, _rules in matches)
    selected = [rule for score, rules in matches if score == specificity for rule in rules]
    paths = [(value, key == "allow") for key, value in selected if key in {"allow", "disallow"} and value]
    delay = next((float(value) for key, value in selected if key == "crawl-delay" and value.replace(".", "", 1).isdigit()), None)
    return paths, delay


def robots_allows(body: str, url: str, user_agent: str = USER_AGENT) -> tuple[bool, float | None]:
    """Apply Allow/Disallow precedence to one configured feed URL."""
    rules, delay = _robots_rules(body, user_agent)
    path = urlparse(url).path or "/"
    matching: list[tuple[int, bool]] = []
    for pattern, allowed in rules:
        expression = "^" + re.escape(pattern).replace(r"\*", ".*")
        if pattern.endswith("$"):
            expression = expression[:-2] + "$"
        if re.match(expression, path):
            matching.append((len(pattern.rstrip("$")), allowed))
    if not matching:
        return True, delay
    longest = max(size for size, _allowed in matching)
    return any(allowed for size, allowed in matching if size == longest), delay


def _robots_body(conn: sqlite3.Connection, source: dict[str, Any], now: datetime, fetch: Callable[[str], bytes]) -> str:
    domain = urlparse(source["url"]).netloc.lower()
    cached = conn.execute("SELECT fetched_at, body FROM robots_cache WHERE domain=?", (domain,)).fetchone()
    if cached and _parse_iso(cached["fetched_at"]) >= now - timedelta(hours=ROBOTS_CACHE_HOURS):
        return str(cached["body"])
    body = fetch(_robots_url(source["url"])).decode("utf-8", errors="replace")
    conn.execute("INSERT INTO robots_cache(domain,fetched_at,body) VALUES(?,?,?) ON CONFLICT(domain) DO UPDATE SET fetched_at=excluded.fetched_at,body=excluded.body", (domain, iso(now), body))
    conn.commit()
    return body


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _rate_limited(conn: sqlite3.Connection, source_id: str, now: datetime) -> bool:
    row = conn.execute("SELECT ended_at FROM run WHERE source_id=? AND status='ok' ORDER BY id DESC LIMIT 1", (source_id,)).fetchone()
    return bool(row and row["ended_at"] and _parse_iso(row["ended_at"]) > now - FEED_MIN_INTERVAL)


def _text(element: ET.Element | None, names: tuple[str, ...]) -> str:
    if element is None:
        return ""
    for child in element:
        if child.tag.rsplit("}", 1)[-1] in names and child.text:
            return child.text.strip()
    return ""


def _published(value: str, fallback: datetime) -> tuple[str, bool]:
    if not value:
        return iso(fallback), True
    try:
        parsed = parsedate_to_datetime(value)
        return iso(parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)), False
    except (TypeError, ValueError):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return iso(parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)), False
        except ValueError:
            for pattern in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S"):
                try:
                    return iso(datetime.strptime(value, pattern).replace(tzinfo=UTC)), False
                except ValueError:
                    pass
            return iso(fallback), True


def _article(url: str, title: str, summary: str, published: str, source: dict[str, Any], now: datetime, owner_group: str | None = None, trend_title: str = "") -> dict[str, Any]:
    published_at, undated = _published(published, now)
    owner_group = owner_group or ((urlparse(url).hostname or "").lower().removeprefix("www.") if source["id"] == "gdelt_vi_news" else source["owner_group"])
    return {"url": url.strip(), "title": normalize_text(title), "summary": normalize_text(summary, strip_html=True)[:300],
            "published_at": published_at, "source_id": source["id"],
            "owner_group": owner_group or source["owner_group"], "fetched_at": iso(now), "undated": int(undated), "trend_title": trend_title}


def parse_rss(payload: bytes, source: dict[str, Any], now: datetime | None = None) -> list[dict[str, str]]:
    """Parse RSS 2.0 and Atom feeds into source articles only."""
    now = now or utc_now()
    root = ET.fromstring(payload)
    entries = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] in {"item", "entry"}]
    articles: list[dict[str, str]] = []
    for entry in entries:
        title = _text(entry, ("title",))
        url = _text(entry, ("link", "guid", "id"))
        if not url:
            url = next((child.attrib["href"] for child in entry if child.tag.rsplit("}", 1)[-1] == "link" and child.attrib.get("href")), "")
        if title and url:
            summary = re.sub(r"<[^>]+>", " ", _text(entry, ("description", "summary", "content")))
            articles.append(_article(url, title, summary, _text(entry, ("pubDate", "published", "updated")), source, now))
    return articles


def parse_trends_rss(payload: bytes, source: dict[str, Any], now: datetime | None = None) -> list[dict[str, Any]]:
    now = now or utc_now()
    root = ET.fromstring(payload)
    signals: list[dict[str, Any]] = []
    for item in (node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "item"):
        title = normalize_text(_text(item, ("title",)))
        traffic = _text(item, ("approx_traffic",)).replace("+", "").replace(",", "")
        match = re.search(r"\d+(?:\.\d+)?", traffic)
        if title:
            signals.append({"source_id": source["id"], "title": title, "normalized_title": normal(title), "observed_at": iso(now), "value": float(match.group()) if match else None, "baseline": None, "kind": "trends"})
    return signals


def parse_trends_articles(payload: bytes, source: dict[str, Any], now: datetime | None = None) -> list[dict[str, Any]]:
    """Extract linked Vietnamese news items from a Google Trends RSS item."""
    now = now or utc_now()
    root = ET.fromstring(payload)
    articles: list[dict[str, Any]] = []
    for item in (node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "item"):
        trend_title = normalize_text(_text(item, ("title",)))
        for news in (node for node in item if node.tag.rsplit("}", 1)[-1] == "news_item"):
            title = normalize_text(_text(news, ("news_item_title",)))
            url = _text(news, ("news_item_url",))
            publisher = _text(news, ("news_item_source",))
            if title and url:
                owner_group = " ".join(publisher.split()) or (urlparse(url).hostname or "").lower().removeprefix("www.")
                articles.append(_article(url, title, "", "", source, now, owner_group=owner_group, trend_title=normal(trend_title)))
    return articles


def parse_wiki_pageviews(payload: bytes, source: dict[str, Any], now: datetime | None = None) -> list[dict[str, Any]]:
    now = now or utc_now()
    value = json.loads(payload.decode("utf-8"))
    return [{"source_id": source["id"], "title": normalize_text(item["article"]), "normalized_title": normal(normalize_text(item["article"])), "observed_at": iso(now), "value": float(item.get("views", 0)), "baseline": None, "kind": "pageviews"}
            for item in value.get("items", [{}])[0].get("articles", []) if valid_wiki_title(item.get("article", ""))]


def parse_json(payload: bytes, source: dict[str, Any], now: datetime | None = None, fetch: Callable[[str], bytes] | None = None) -> list[dict[str, str]]:
    now = now or utc_now()
    value = json.loads(payload.decode("utf-8"))
    if source["kind"] != "json_hn" or not isinstance(value, list) or fetch is None:
        return []
    articles = []
    for item_id in value[:60]:
        item = json.loads(fetch(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").decode("utf-8"))
        if item.get("type") == "story" and item.get("title") and item.get("url"):
            articles.append(_article(item["url"], item["title"], "", datetime.fromtimestamp(item.get("time", now.timestamp()), UTC).isoformat(), source, now))
    return articles


def parse_gdelt_json(payload: bytes, source: dict[str, Any], now: datetime | None = None) -> list[dict[str, Any]]:
    """Accept GDELT's empty JSON response as a successful no-result scan."""
    now = now or utc_now()
    value = json.loads(payload.decode("utf-8"))
    if not isinstance(value, dict):
        return []
    articles = []
    for item in value.get("articles", []):
        if not isinstance(item, dict) or not item.get("title") or not item.get("url"):
            continue
        articles.append(_article(item["url"], item["title"], "", item.get("seendate") or item.get("published_at") or "", source, now))
    return articles


def _fetch(url: str, timeout: int = 20) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json, application/xml, text/xml;q=0.9"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310: configured URLs only
        return response.read()


def _source_url(source: dict[str, Any], now: datetime) -> str:
    yesterday = now - timedelta(days=1)
    return source["url"].replace("{YYYY}", f"{yesterday:%Y}").replace("{MM}", f"{yesterday:%m}").replace("{DD}", f"{yesterday:%d}")


def _wiki_history(source: dict[str, Any], now: datetime, fetch: Callable[[str], bytes]) -> list[dict[str, Any]]:
    days: list[list[dict[str, Any]]] = []
    last_error: Exception | None = None
    for offset in range(8):
        day = now - timedelta(days=1 + offset)
        url = source["url"].replace("{YYYY}", f"{day:%Y}").replace("{MM}", f"{day:%m}").replace("{DD}", f"{day:%d}")
        try:
            pageviews = parse_wiki_pageviews(fetch(url), source, day)
        except Exception as exc:
            last_error = exc
            continue
        # The top endpoint can return no items before its daily dataset is ready.
        if pageviews:
            days.append(pageviews)
    if not days:
        raise last_error or ValueError("Wikimedia returned no pageview data")
    history: dict[str, list[float]] = {}
    for day in days[1:]:
        for item in day:
            history.setdefault(item["normalized_title"], []).append(float(item["value"] or 0))
    for item in days[0]:
        item["baseline"] = statistics.median(history.get(item["normalized_title"], [0]))
    return days[0]


def scan_sources(db_path: Path | str = DEFAULT_DB, sources_path: Path | str | None = None, fetch: Callable[[str], bytes] | None = None, pause_seconds: float = 0.2, now: datetime | None = None) -> dict[str, int]:
    """Scan only reviewed sources explicitly enabled for the internal trial."""
    now = now or utc_now()
    fetch = fetch or _fetch
    sources = load_sources(sources_path) if sources_path else load_sources()
    conn = init_db(db_path)
    outcome = {"sources": 0, "articles": 0, "signals": 0, "errors": 0}
    try:
        # Retain a 72-hour window when a scheduled run is rate-skipped.
        conn.execute("DELETE FROM article WHERE published_at < ?", (iso(now - timedelta(hours=72)),))
        conn.execute("DELETE FROM signal")
        conn.execute("DELETE FROM event")
        conn.commit()
        for source in sources:
            # `trial` is an explicit activation switch.  Older approved sources remain
            # approved in the registry but are not enabled by this P0 trial.
            if source["tos_status"] != "ok" or source.get("trial") != "internal":
                continue
            started = iso(now)
            try:
                if _rate_limited(conn, source["id"], now):
                    conn.execute("INSERT INTO run(started_at,ended_at,source_id,status) VALUES(?,?,?,?)", (started, iso(now), source["id"], "rate_skip"))
                    conn.commit()
                    continue
                robots = _robots_body(conn, source, now, fetch)
                allowed, crawl_delay = robots_allows(robots, source["url"])
                if not allowed:
                    conn.execute("INSERT INTO run(started_at,ended_at,source_id,status) VALUES(?,?,?,?)", (started, iso(now), source["id"], "robots_blocked"))
                    conn.commit()
                    continue
                # A just-fetched robots.txt is itself a request to the domain.
                if crawl_delay:
                    time.sleep(crawl_delay)
                if source["kind"] == "wiki_pageviews":
                    signals, records = _wiki_history(source, now, fetch), []
                else:
                    if source["id"] == "gdelt_vi_news":
                        time.sleep(GDELT_MIN_WAIT_SECONDS)
                    payload = fetch(_source_url(source, now))
                    if source["id"] == "google_trends_vn":
                        signals = parse_trends_rss(payload, source, now)
                        records = parse_trends_articles(payload, source, now)
                    elif source["kind"] == "json_gdelt":
                        signals, records = [], parse_gdelt_json(payload, source, now)
                    else:
                        signals = []
                        records = parse_rss(payload, source, now) if source["kind"] == "rss" and source["role"] in {"article", "primary"} else parse_json(payload, source, now, fetch)
                if records:
                    conn.executemany("""INSERT INTO article(url,title,summary,published_at,source_id,owner_group,fetched_at,undated,trend_title) VALUES(:url,:title,:summary,:published_at,:source_id,:owner_group,:fetched_at,:undated,:trend_title) ON CONFLICT(url) DO UPDATE SET title=excluded.title,summary=excluded.summary,published_at=excluded.published_at,source_id=excluded.source_id,owner_group=excluded.owner_group,fetched_at=excluded.fetched_at,undated=excluded.undated,trend_title=excluded.trend_title""", records)
                if signals:
                    conn.executemany("INSERT INTO signal(source_id,title,normalized_title,observed_at,value,baseline,kind) VALUES(:source_id,:title,:normalized_title,:observed_at,:value,:baseline,:kind)", signals)
                conn.execute("INSERT INTO run(started_at,ended_at,source_id,status,article_count) VALUES(?,?,?,?,?)", (started, iso(utc_now()), source["id"], "ok", len(records)))
                outcome["sources"] += 1; outcome["articles"] += len(records); outcome["signals"] += len(signals)
            except Exception as exc:  # one endpoint must not stop later sources
                conn.execute("INSERT INTO run(started_at,ended_at,source_id,status,error) VALUES(?,?,?,?,?)", (started, iso(utc_now()), source["id"], "error", str(exc)[:500]))
                outcome["errors"] += 1
            conn.commit()
            if pause_seconds:
                time.sleep(pause_seconds)
    finally:
        conn.close()
    return outcome
