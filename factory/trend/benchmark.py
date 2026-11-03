"""Independent benchmark recall for the read-only trend scanner."""
from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .cluster import GENERIC_ENTITIES, generic_entities, is_generic_entity
from .report import _belongs, _keywords, _valid_event_label
from .scan import DEFAULT_DB
from .sources import source_map


# Function words and broad topic words do not identify a news event.  This
# deliberately includes "gia": price-only matches were the main source of
# misleading benchmark matches before the entity rule was introduced.
_STOPWORDS = {
    "a", "an", "and", "at", "by", "cho", "cua", "da", "dang", "de", "duoc", "for", "from", "gia", "in", "is",
    "la", "là", "nhung", "nhung", "of", "or", "sau", "su", "tai", "the", "thi", "to", "trong", "tu", "va", "voi",
    "về", "và", "với", "đã", "đang", "được", "tại", "từ", "các", "có", "khi", "một", "những", "ngày", "hôm",
    "nay", "moi", "mới", "nhat", "nhất", "binh", "bình", "quan", "quân", "ban", "bán", "le", "lẻ", "tap", "tập",
    "doan", "đoàn", "cong", "công", "ty", "company", "doanh", "nghiep", "nghiệp", "he", "hệ", "thong", "thống",
}
_NAME_PREFIXES = {"bo", "cong", "doanh", "gia", "he", "lo", "nguoi", "quy", "san", "tap", "ve"}


def _fold(value: str) -> str:
    """Lowercase Vietnamese/English text without diacritics."""
    decomposed = unicodedata.normalize("NFD", value.lower().replace("đ", "d"))
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", _fold(value)) if token not in _STOPWORDS}


def _label(target: dict[str, Any]) -> str:
    # Older test fixtures predate the explicit benchmark label.  Joining the
    # entities keeps those fixtures useful without changing the benchmark JSON.
    return str(target.get("label") or " ".join(target["entities"]))


def _core_entities(values: list[str]) -> tuple[set[str], list[frozenset[str]]]:
    """Return meaningful entity tokens and abbreviation/proper-name anchors.

    An anchor is either an abbreviation written in parentheses/all caps or a
    proper-name core.  The latter is capped at three meaningful tokens so a
    long descriptive entity cannot turn into a substring-style match.
    """
    cores: set[str] = set()
    anchors: list[frozenset[str]] = []
    for value in values:
        raw_tokens = _tokens(value)
        # Keep the most specific-looking words in a long descriptive entity.
        core = sorted(raw_tokens, key=lambda token: (-any(char.isdigit() for char in token), -len(token), token))[:3]
        cores.update(core)

        abbreviations = re.findall(r"\(([A-Za-z0-9]{2,})\)", value)
        abbreviations.extend(re.findall(r"\b[A-Z]{2,}[A-Z0-9]*\b", value))
        for abbreviation in abbreviations:
            token_set = _tokens(abbreviation)
            if token_set:
                anchors.append(frozenset(token_set))

        # Only names, rather than descriptive entity phrases, can satisfy the
        # entity rule.  E.g. "giá vàng" is useful context but is not a named
        # anchor; "Apple", "Phó Đức Nam", and "Dung Quất" are.
        capitalized = [
            token for token in (_fold(part) for part in re.findall(r"[\w-]+", value) if part[0].isupper())
            if token not in _STOPWORDS and token not in _NAME_PREFIXES
        ]
        proper_core = [token for token in core if token in capitalized]
        if len(proper_core) >= 2:
            anchors.append(frozenset(proper_core))
        elif len(proper_core) == 1 and len(raw_tokens) == 1:
            anchors.append(frozenset(proper_core))
    return cores, anchors


def _jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 0.0


def _generic_entity_tokens(common: set[str]) -> set[str]:
    return set().union(*(_tokens(entity) for entity in common), set())


def _is_generic_benchmark_entity(value: str, common: set[str]) -> bool:
    """Recognize a whole generic entity, including a generic multiword phrase."""
    folded = _fold(value)
    if is_generic_entity(folded, common):
        return True
    # Keep stop words for this containment check.  Otherwise "giá vàng" is
    # reduced to one token and accidentally turns "giá vàng thế giới" into a
    # one-word specific anchor ("giới").
    raw_words = lambda text: set(re.findall(r"[a-z0-9]+", _fold(text)))
    value_words = raw_words(value)
    return any(len(raw_words(entity)) >= 2 and raw_words(entity) <= value_words for entity in GENERIC_ENTITIES | common)


def _specific_entity_anchors(values: list[str], common: set[str]) -> list[frozenset[str]]:
    """Keep only concrete names or multiword identifiers for the entity rule."""
    generic_tokens = _generic_entity_tokens(common)
    anchors: list[frozenset[str]] = []
    for value in values:
        if _is_generic_benchmark_entity(value, common):
            continue
        core = frozenset(_tokens(value) - generic_tokens)
        # A proper single-token name is useful (for example, a named person or
        # local place); descriptive single words are not.
        if len(core) >= 2:
            anchors.append(core)
        elif len(core) == 1 and len(_tokens(value)) == 1 and re.search(r"\b[A-ZÀ-ỴĐ][\wÀ-ỹ.-]*\b", value):
            anchors.append(core)
    return anchors


def _match_article(article: dict[str, Any], target: dict[str, Any], common_entities: set[str] | None = None) -> dict[str, Any] | None:
    """Apply the documented article-to-benchmark rule and return its evidence."""
    title_tokens = _tokens(str(article["title"]))
    label_tokens = _tokens(_label(target))
    common = common_entities or GENERIC_ENTITIES
    anchors = _specific_entity_anchors(target["entities"], common)
    jaccard = _jaccard(title_tokens, label_tokens)
    # The entity branch must be anchored in a non-generic identifier and have
    # at least two meaningful label terms in the headline.  Generic entities
    # (brands, amounts, sectors) never supply either kind of evidence.
    content_hits = (label_tokens - _generic_entity_tokens(common)) & title_tokens
    if any(anchor <= title_tokens for anchor in anchors) and len(content_hits) >= 2:
        return {"score": jaccard, "rule": "entity", "content_hits": len(content_hits)}
    if jaccard >= 0.25:
        return {"score": jaccard, "rule": "jaccard"}
    return None


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _best_match(matches: list[tuple[dict[str, Any], dict[str, Any]]]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Prefer stronger evidence; use publication time only as a stable tie-break."""
    return max(matches, key=lambda item: (item[1]["score"], item[0]["published_at"]))


def _event_rows(conn: sqlite3.Connection) -> list[tuple[sqlite3.Row, list[dict[str, Any]]]]:
    result = []
    for event in conn.execute("SELECT * FROM event"):
        ids = json.loads(event["article_ids"])
        if not ids:
            continue
        placeholders = ",".join("?" for _ in ids)
        articles = [dict(row) for row in conn.execute(f"SELECT * FROM article WHERE id IN ({placeholders})", ids)]
        result.append((event, articles))
    return result


def evaluate_benchmark(benchmark_path: Path | str, db_path: Path | str | sqlite3.Connection = DEFAULT_DB, sources_path: Path | str | None = None) -> dict[str, Any]:
    """Evaluate fixed benchmark events without modifying the benchmark or scanner state."""
    benchmark = json.loads(Path(benchmark_path).read_text(encoding="utf-8-sig"))
    lookup = source_map(sources_path) if sources_path else source_map()
    keywords = _keywords()
    close_connection = not isinstance(db_path, sqlite3.Connection)
    conn = sqlite3.connect(db_path) if close_connection else db_path
    conn.row_factory = sqlite3.Row
    try:
        events = _event_rows(conn)
        articles = [dict(row) for row in conn.execute("SELECT * FROM article")]
    finally:
        if close_connection:
            conn.close()
    results: list[dict[str, Any]] = []
    for target in benchmark["events"]:
        channel = target["channel"]
        reported = _parse(target["first_reported"])
        window_articles = [article for article in articles if abs(_parse(article["published_at"]) - reported) <= timedelta(hours=48)]
        common = generic_entities(window_articles)
        coverage_matches = [(article, evidence) for article in window_articles if (evidence := _match_article(article, target, common))]
        candidate_matches: list[tuple[dict[str, Any], dict[str, Any], str]] = []
        for event, event_articles in events:
            if not _valid_event_label(event):
                continue
            for article in event_articles:
                if abs(_parse(article["published_at"]) - reported) > timedelta(hours=48) or not _belongs(article, channel, lookup, keywords):
                    continue
                evidence = _match_article(article, target, common)
                if evidence:
                    candidate_matches.append((article, evidence, event["id"]))
        candidate_ids = sorted({event_id for _, _, event_id in candidate_matches})
        coverage_caught = bool(coverage_matches)
        candidate_caught = bool(candidate_matches)
        reason = ""
        best_title = ""
        if not candidate_caught:
            if not coverage_matches:
                reason = "không có nguồn đưa tin"
            elif not any(_belongs(article, channel, lookup, keywords) for article, _ in coverage_matches):
                best_article, _ = _best_match(coverage_matches)
                best_title = str(best_article["title"])
                reason = f"bị lọc từ khóa: {best_title}"
            else:
                best_article, _ = _best_match(coverage_matches)
                best_title = str(best_article["title"])
                reason = f"không gom được: {best_title}"
        results.append({
            "id": target["id"], "channel": channel, "hotness": target["hotness"],
            # Keep caught as an alias while callers migrate to the explicit metric.
            "caught": candidate_caught, "coverage_caught": coverage_caught,
            "candidate_caught": candidate_caught, "event_ids": candidate_ids,
            "reason": reason, "best_title": best_title,
        })
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        grouped[result["channel"]].append(result)
    false_positives = []
    for target in benchmark["events"]:
        reported = _parse(target["first_reported"])
        window_articles = [article for article in articles if abs(_parse(article["published_at"]) - reported) <= timedelta(hours=48)]
        common = generic_entities(window_articles)
        for article in window_articles:
            if abs(_parse(article["published_at"]) - reported) <= timedelta(hours=48):
                evidence = _match_article(article, target, common)
                if evidence:
                    false_positives.append({"benchmark_id": target["id"], "article_title": article["title"], "score": evidence["score"], "rule": evidence["rule"]})
    false_positives.sort(key=lambda item: (item["score"], item["benchmark_id"], item["article_title"]))
    summary: dict[str, Any] = {"events": results, "channels": {}, "false_positives": false_positives[:10]}
    for channel, values in grouped.items():
        by_hotness = {}
        for hotness in ("high", "medium"):
            subset = [value for value in values if value["hotness"] == hotness]
            by_hotness[hotness] = {
                "coverage_caught": sum(value["coverage_caught"] for value in subset),
                "candidate_caught": sum(value["candidate_caught"] for value in subset), "total": len(subset),
            }
        summary["channels"][channel] = {
            "coverage_caught": sum(value["coverage_caught"] for value in values),
            "candidate_caught": sum(value["candidate_caught"] for value in values), "total": len(values), "hotness": by_hotness,
            "missed": [value for value in values if not value["candidate_caught"]],
        }
    return summary


def render_benchmark(summary: dict[str, Any]) -> str:
    lines = ["# Trend benchmark recall", ""]
    for channel in ("MIM", "CK"):
        result = summary["channels"].get(channel, {"coverage_caught": 0, "candidate_caught": 0, "total": 0, "hotness": {}, "missed": []})
        total = result["total"]
        if total:
            lines.append(f"## {channel}")
            lines.append(f"- Recall bao phủ: {result['coverage_caught']}/{total} ({result['coverage_caught'] / total:.1%})")
            lines.append(f"- Recall ứng viên: {result['candidate_caught']}/{total} ({result['candidate_caught'] / total:.1%})")
        else:
            lines.append(f"## {channel}: 0/0")
        for hotness in ("high", "medium"):
            item = result["hotness"].get(hotness, {"coverage_caught": 0, "candidate_caught": 0, "total": 0})
            if item["total"]:
                lines.append(f"- {hotness}: bao phủ {item['coverage_caught']}/{item['total']} ({item['coverage_caught'] / item['total']:.1%}); ứng viên {item['candidate_caught']}/{item['total']} ({item['candidate_caught'] / item['total']:.1%})")
            else:
                lines.append(f"- {hotness}: 0/0")
        lines.append("- Bỏ lỡ:")
        if result["missed"]:
            lines.extend(f"  - {item['id']}: {item['reason']}" for item in result["missed"])
        else:
            lines.append("  - Không")
        lines.append("")
    lines.append("## Khớp dương tính giả cần soát tay (10 điểm thấp nhất)")
    if summary["false_positives"]:
        for item in summary["false_positives"]:
            lines.append(f"- {item['benchmark_id']} — {item['article_title']} (điểm {item['score']:.3f}; {item['rule']})")
    else:
        lines.append("- Không")
    return "\n".join(lines)
