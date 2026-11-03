"""Deterministic event clustering; deliberately no model or remote service."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import unicodedata
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .scan import DEFAULT_DB, normal, normalize_stored_articles, utc_now
from .sources import source_map

ALIASES = {"open ai": "openai", "chat gpt": "chatgpt", "u s": "us", "u s a": "us"}
STOP = {"the", "a", "an", "va", "cua", "voi", "trong", "cho", "tai", "la", "da", "moi", "news", "gia"}
WEAK_ENTITIES = {"ai", "api", "usd", "usa"}
NOISY_ENTITY_TOKENS = {"hai", "ket", "qua", "hom", "nay", "ngay", "thang", "nam", "thu", "tuan", "ong", "ba", "dai", "dau", "don", "ep", "ve", "gia", "day"}
CAPITALIZED = re.compile(r"\b(?:[A-ZÀ-ỴĐ][\wÀ-ỹ.-]*)(?:\s+[A-ZÀ-ỴĐ][\wÀ-ỹ.-]*)*\b")
MONEY = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:tỷ|triệu|usd|%|billion|million)\b", re.I)
# These are deliberately broad anchors, not event identifiers.  The list is
# kept here (rather than inferred from capitalization) because a major brand,
# a bare amount, or a sector noun frequently appears in unrelated headlines.
GENERIC_ENTITIES = {
    "google", "alphabet", "apple", "samsung", "lg", "openai", "microsoft", "nvidia", "meta",
    "amazon", "tesla", "intel", "huawei", "xiaomi", "tiktok", "youtube", "android", "iphone",
    "ios", "windows", "chrome", "ai", "ngan", "ngan hang", "chung khoan", "co phieu",
    "gia vang", "gia usd", "ty gia", "usd", "vnd", "fed", "lo hong bao mat", "an ninh mang ai",
    "he thong ngan hang", "dong viet nam", "tien gui doanh nghiep", "bo tai chinh", "bo cong thuong",
    "gia ban le dien binh quan", "khai thac lo hong tu dong", "phong thu mang", "doanh nghiep xang dau",
    "loc hoa dau",
}
GENERIC_LINK_JACCARD = 0.35
COHESION_JACCARD = 0.30


def normal(text: str) -> str:
    value = "".join(char for char in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(char) != "Mn")
    value = value.replace("đ", "d")
    value = re.sub(r"[^a-z0-9%]+", " ", value).strip()
    return ALIASES.get(value, value)


def tokens(text: str) -> set[str]:
    return {part for part in normal(text).split() if len(part) > 1 and not part.isdigit() and part not in STOP}


def extract_entities(title: str) -> set[str]:
    found = {normal(match.group()) for match in CAPITALIZED.finditer(title)}
    found.update(normal(match.group()) for match in MONEY.finditer(title))
    return {entity for entity in found if len(entity) > 1 and entity not in STOP and entity not in WEAK_ENTITIES}


def _is_money_entity(entity: str) -> bool:
    return bool(re.fullmatch(r"\d+(?:\s+\d+)*(?:\s+(?:ty|trieu|usd|billion|million)|%)", entity))


def generic_entities(articles: list[dict[str, Any]]) -> set[str]:
    """Return static and window-wide common entities.

    A headline window is intentionally the unit for the frequency rule: an
    entity occurring in more than 5% of articles cannot by itself establish a
    news event in that window.
    """
    counts = Counter(entity for article in articles for entity in extract_entities(article["title"]))
    limit = len(articles) * 0.05
    return GENERIC_ENTITIES | {entity for entity, count in counts.items() if count > limit}


def is_generic_entity(entity: str, common: set[str] | None = None) -> bool:
    value = normal(entity)
    return value in NOISY_ENTITY_TOKENS or value in (common or GENERIC_ENTITIES) or _is_money_entity(value)


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a and b else 0.0


def _linkable(left: dict[str, Any], right: dict[str, Any], left_entities: set[str], right_entities: set[str], common: set[str], threshold: float) -> bool:
    shared = left_entities & right_entities
    if not shared:
        return False
    score = similarity(left["title"], right["title"])
    if score < threshold:
        return False
    # A shared broad brand/amount/sector is only useful with substantially
    # overlapping headline language.  A proper, non-common entity may use the
    # normal threshold.
    return any(not is_generic_entity(entity, common) for entity in shared) or score >= GENERIC_LINK_JACCARD


def _mean_pair_similarity(group: list[dict[str, Any]]) -> float:
    if len(group) < 3:
        return 1.0
    scores = [similarity(left["title"], right["title"])
              for index, left in enumerate(group) for right in group[index + 1:]]
    return sum(scores) / len(scores) if scores else 1.0


def _split_low_cohesion(group: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Break a transitive component when its members no longer agree.

    Connected components are susceptible to A--B--C bridges.  Only low
    cohesion components are re-partitioned, and the re-partition uses complete
    linkage so every member of a resulting event agrees with its peers.
    """
    if _mean_pair_similarity(group) >= COHESION_JACCARD:
        return [group]
    parts: list[list[dict[str, Any]]] = []
    for article in group:
        compatible = [part for part in parts if all(similarity(article["title"], member["title"]) >= COHESION_JACCARD for member in part)]
        if compatible:
            max(compatible, key=lambda part: sum(similarity(article["title"], member["title"]) for member in part) / len(part)).append(article)
        else:
            parts.append([article])
    return parts


def cluster_articles(articles: list[dict[str, Any]], threshold: float = 0.25) -> list[list[dict[str, Any]]]:
    """Connected components constrained by a 48-hour, entity-bearing link."""
    ordered = sorted(articles, key=lambda item: (item["published_at"], item.get("id", 0)))
    parents = list(range(len(ordered)))
    parsed = [datetime.fromisoformat(item["published_at"].replace("Z", "+00:00")) for item in ordered]
    entities = [extract_entities(item["title"]) for item in ordered]
    common = generic_entities(ordered)

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]; index = parents[index]
        return index
    def union(left: int, right: int) -> None:
        left, right = find(left), find(right)
        if left != right: parents[right] = left

    for later in range(len(ordered)):
        for earlier in range(later):
            if parsed[later] - parsed[earlier] > timedelta(hours=48):
                continue
            if _linkable(ordered[later], ordered[earlier], entities[later], entities[earlier], common, threshold):
                union(earlier, later)
    groups: dict[int, list[dict[str, Any]]] = {}
    for index, article in enumerate(ordered):
        groups.setdefault(find(index), []).append(article)
    return [part for group in groups.values() for part in _split_low_cohesion(group)]


def event_from_group(group: list[dict[str, Any]]) -> dict[str, Any]:
    entities = sorted(set().union(*(extract_entities(article["title"]) for article in group)))
    meaningful = [entity for entity in entities if set(tokens(entity)) - NOISY_ENTITY_TOKENS - WEAK_ENTITIES]
    label = " · ".join(meaningful[:2])
    ids = [int(article["id"]) for article in group]
    fingerprint = "|".join(map(str, ids))
    return {"id": hashlib.sha1(fingerprint.encode()).hexdigest()[:16], "label": label, "entities": json.dumps(entities, ensure_ascii=False),
            "first_seen": min(article["published_at"] for article in group), "last_seen": max(article["published_at"] for article in group),
            "article_ids": json.dumps(ids)}


def cluster_db(db_path: Path | str = DEFAULT_DB, threshold: float = 0.25, sources_path: Path | str | None = None, now: datetime | None = None) -> int:
    """Cluster only fresh editorial articles; primary sources remain factcheck material."""
    now = now or utc_now()
    cutoff = now - timedelta(hours=72)
    lookup = source_map(sources_path) if sources_path else source_map()
    conn = sqlite3.connect(db_path); conn.row_factory = sqlite3.Row
    try:
        normalize_stored_articles(conn)
        articles = [dict(row) for row in conn.execute("SELECT * FROM article")
                    if datetime.fromisoformat(row["published_at"].replace("Z", "+00:00")).astimezone(UTC) >= cutoff
                    and lookup.get(row["source_id"], {}).get("role") != "primary"]
        groups = cluster_articles(articles, threshold)
        events = [event_from_group(group) for group in groups]
        # Chỉ lấy signal của lần quét mới nhất mỗi nguồn; các lần cũ giữ lại làm lịch sử.
        signals = [dict(row) for row in conn.execute("SELECT s.* FROM signal s WHERE s.run_id=(SELECT MAX(run_id) FROM signal WHERE source_id=s.source_id)")]
        for event, group in zip(events, groups):
            event["signals"] = json.dumps(_matching_signals(group, signals), ensure_ascii=False)
        conn.execute("DELETE FROM event")
        conn.executemany("INSERT INTO event(id,label,entities,first_seen,last_seen,article_ids,signals) VALUES(:id,:label,:entities,:first_seen,:last_seen,:article_ids,:signals)", events)
        conn.commit()
        return len(events)
    finally:
        conn.close()


def _matching_signals(group: list[dict[str, Any]], signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Signals may enrich an existing event, never create one."""
    matches = []
    for signal in signals:
        if signal["kind"] == "trends":
            if any(article.get("trend_title", "") == signal["normalized_title"] for article in group):
                matches.append({key: signal[key] for key in ("source_id", "title", "value", "baseline", "kind")})
            continue
        signal_title = signal["normalized_title"]
        signal_terms = {term for term in signal_title.split() if len(term) >= 3}
        if any(signal_terms & {term for term in normal(article["title"]).split() if len(term) >= 3} for article in group):
            matches.append({key: signal[key] for key in ("source_id", "title", "value", "baseline", "kind")})
    return matches
