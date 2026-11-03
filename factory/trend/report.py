"""Markdown report writer for fresh editorial events and primary-source leads."""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .cluster import NOISY_ENTITY_TOKENS, STOP, WEAK_ENTITIES, normal, tokens
from .independence import independent_sources
from .scan import DEFAULT_DB
from .sources import source_map


LABEL_STOP = STOP | WEAK_ENTITIES | NOISY_ENTITY_TOKENS | {"co", "deere", "effect", "filer"}


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _keywords() -> dict[str, Any]:
    return json.loads(Path(__file__).with_name("keywords.json").read_text(encoding="utf-8"))


def _contains(haystack: str, phrase: str) -> bool:
    return f" {normal(phrase)} " in f" {normal(haystack)} "


def vn_impact(article: dict[str, Any], channel: str, keywords: dict[str, Any]) -> bool:
    """Keep international coverage only when it has a clear Vietnamese impact."""
    impact = keywords.get("vn_impact", {})
    haystack = article["title"] + " " + article["summary"]
    if any(_contains(haystack, word) for word in impact.get("direct", [])):
        return True
    channel_rules = impact.get(channel, {})
    return (any(_contains(haystack, word) for word in channel_rules.get("entities", []))
            and any(_contains(haystack, word) for word in channel_rules.get("events", [])))


def _belongs(article: dict[str, Any], channel: str, sources: dict[str, dict[str, Any]], keywords: dict[str, Any]) -> bool:
    source = sources.get(article["source_id"], {})
    haystack = f" {normal(article['title'] + ' ' + article['summary'])} "
    if channel not in source.get("channels", []) or not any(f" {normal(word)} " in haystack for word in keywords[channel]):
        return False
    return source.get("lang", "vi") == "vi" or vn_impact(article, channel, keywords)


def event_metrics(articles: list[dict[str, Any]], now: datetime) -> tuple[int, float]:
    day = [article for article in articles if _parse(article["published_at"]) >= now - timedelta(hours=24)]
    recent = [article for article in day if _parse(article["published_at"]) >= now - timedelta(hours=3)]
    baseline = len(day) / 8
    return independent_sources(day), (len(recent) / baseline if baseline else 0.0)


def _signals(event: sqlite3.Row) -> list[dict[str, Any]]:
    return json.loads(event["signals"])


def _trend_traffic(event: sqlite3.Row) -> float:
    return max((float(signal["value"] or 0) for signal in _signals(event) if signal["kind"] == "trends"), default=0.0)


def _signal_lines(event: sqlite3.Row) -> list[str]:
    result = []
    for signal in _signals(event):
        if signal["kind"] == "trends":
            traffic = f"; khoảng {int(signal['value']):,} lượt tìm" if signal["value"] is not None else ""
            result.append(f"- Tín hiệu Trends VN: {signal['title']}{traffic}")
        else:
            baseline = signal["baseline"] or 0
            ratio = (signal["value"] or 0) / baseline if baseline else None
            change = f"{ratio:.2f}× trung vị 7 ngày" if ratio is not None else "chưa có mốc 7 ngày"
            result.append(f"- Tín hiệu pageviews: {signal['title']} — {int(signal['value'] or 0):,}; {change}")
    return result


def _valid_event_label(event: sqlite3.Row) -> bool:
    try:
        entities = json.loads(event["entities"])
    except json.JSONDecodeError:
        return False
    return any(set(tokens(str(entity))) - LABEL_STOP for entity in entities)


UNIT_NUMBER = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:%|tỷ|triệu|nghìn|trăm|USD|VND|đồng|dollar|million|billion|GB|TB|CPU|GPU|ngày|tháng|năm)\b", re.I)


def _opportunity(event: sqlite3.Row, articles: list[dict[str, Any]]) -> bool:
    entities = json.loads(event["entities"])
    concrete = any(set(tokens(str(entity))) - LABEL_STOP for entity in entities)
    return concrete and any(UNIT_NUMBER.search(article["title"] + " " + article["summary"]) for article in articles)


def _render_event(event: sqlite3.Row, articles: list[dict[str, Any]], independent: int, velocity: float, hot: bool, opportunity: bool) -> list[str]:
    flags = ", ".join(flag for flag, enabled in (("nóng", hot), ("cơ hội", opportunity)) if enabled) or "—"
    lines = [f"#### {event['label']}", f"- Cờ: {flags}", f"- Nguồn độc lập (24h): {independent}; tốc độ: {velocity:.2f}×", f"- Thấy lần đầu: {event['first_seen']}"]
    lines.extend(f"- {article['title']} — {article['url']}" for article in sorted(articles, key=lambda item: item["published_at"], reverse=True))
    return lines + _signal_lines(event) + [""]


def _render_primary(articles: list[dict[str, Any]]) -> list[str]:
    lines = ["#### SƠ CẤP MỚI"]
    if not articles:
        return lines + ["_Chưa có tiêu đề nguồn sơ cấp mới phù hợp._", ""]
    lines.extend(f"- {article['title']} — {article['url']}" for article in articles[:5])
    return lines + [""]


def write_report(db_path: Path | str = DEFAULT_DB, output_root: Path | str = "output/trend", sources_path: Path | str | None = None, now: datetime | None = None) -> Path:
    now = now or datetime.now(UTC)
    lookup = source_map(sources_path) if sources_path else source_map()
    keywords = _keywords()
    conn = sqlite3.connect(db_path); conn.row_factory = sqlite3.Row
    try:
        events: list[tuple[int, float, float, sqlite3.Row, list[dict[str, Any]]]] = []
        for event in conn.execute("SELECT * FROM event"):
            if not _valid_event_label(event):
                continue
            ids = json.loads(event["article_ids"])
            if not ids:
                continue
            placeholders = ",".join("?" for _ in ids)
            articles = [dict(row) for row in conn.execute(f"SELECT * FROM article WHERE id IN ({placeholders})", ids)]
            independent, velocity = event_metrics(articles, now)
            events.append((independent, _trend_traffic(event), velocity, event, articles))
        primary = [dict(row) for row in conn.execute("SELECT * FROM article ORDER BY published_at DESC")
                   if lookup.get(row["source_id"], {}).get("role") == "primary" and _parse(row["published_at"]) >= now - timedelta(hours=72)]
        last_runs = {row["source_id"]: row for row in conn.execute("SELECT r.* FROM run r JOIN (SELECT source_id, MAX(id) id FROM run GROUP BY source_id) latest ON r.id=latest.id")}
    finally:
        conn.close()
    target = Path(output_root) / now.strftime("%Y-%m-%d")
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{now:%H}.md"
    lines = [f"# Trend scan — {now:%Y-%m-%d %H:00 UTC}", "", "Tín hiệu biên tập chỉ đọc; không phải hàng đợi xuất bản.", ""]
    for channel in ("MIM", "CK"):
        channel_articles = [article for _independent, _traffic, _velocity, _event, articles in events for article in articles
                            if channel in lookup.get(article["source_id"], {}).get("channels", []) and _parse(article["published_at"]) >= now - timedelta(hours=72)]
        valid = [(independent, traffic, velocity, event, articles) for independent, traffic, velocity, event, articles in events
                 if _valid_event_label(event) and any(article.get("url") for article in articles)
                 and any(channel in lookup.get(article["source_id"], {}).get("channels", []) for article in articles)]
        candidates = [(independent, traffic, velocity, event, [article for article in articles if _belongs(article, channel, lookup, keywords)])
                      for independent, traffic, velocity, event, articles in valid]
        candidates = [item for item in candidates if item[4]]
        candidates.sort(key=lambda item: (-(item[0] >= 2 or item[1] > 0), -item[0], -item[1], -item[2], item[3]["first_seen"]))
        hot_count = sum(independent >= 2 or traffic > 0 for independent, traffic, _velocity, _event, _articles in candidates)
        opportunity_count = sum(_opportunity(event, articles) for _independent, _traffic, _velocity, event, articles in candidates)
        primary_for_channel = [article for article in primary if _belongs(article, channel, lookup, keywords)]
        lines.extend([f"## {channel}", "", "#### Bộ đếm 72 giờ", "", "| Bài | Sự kiện hợp lệ | Ứng viên liên quan | Sự kiện nóng | Cơ hội sản xuất |", "|---:|---:|---:|---:|---:|", f"| {len(channel_articles)} | {len(valid)} | {len(candidates)} | {hot_count} | {opportunity_count} |", "", "#### ỨNG VIÊN LIÊN QUAN"])
        if candidates:
            for independent, traffic, velocity, event, articles in candidates[:25]:
                lines.extend(_render_event(event, articles, independent, velocity, independent >= 2 or traffic > 0, _opportunity(event, articles)))
        else:
            lines.extend(["_Chưa có ứng viên liên quan._", ""])
        lines.extend(_render_primary(primary_for_channel))
    lines.extend(["## Trạng thái nguồn", "", "| Nguồn | ToS | Lần chạy | Bài |", "|---|---|---|---:|"])
    for source in lookup.values():
        run = last_runs.get(source["id"])
        if source.get("trial") != "internal":
            status, count = "không bật", 0
        else:
            status = run["status"] if run else "không gọi"
            count = run["article_count"] if run else 0
        lines.append(f"| {source['id']} | {source['tos_status']} | {status} | {count} |")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
