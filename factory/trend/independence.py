"""Independence counting protects reports from syndicated repeats."""
from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from .cluster import similarity


def independent_sources(articles: list[dict[str, Any]], duplicate_threshold: float = 0.86) -> int:
    """Count ownership groups after collapsing near-identical headlines."""
    representatives: list[dict[str, Any]] = []
    for article in sorted(articles, key=lambda item: (item["title"].lower(), item.get("url", ""))):
        if any(similarity(article["title"], prior["title"]) >= duplicate_threshold for prior in representatives):
            continue
        representatives.append(article)
    return len({article["owner_group"] for article in representatives})


def root_domain(url: str) -> str:
    """Return the publisher hostname used to de-duplicate GDELT aggregation."""
    hostname = (urlparse(url).hostname or "").lower().removeprefix("www.")
    return hostname
