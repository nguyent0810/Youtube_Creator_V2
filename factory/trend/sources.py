"""Source configuration helpers.  Configuration, not code, decides what may run."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SOURCES_PATH = Path(__file__).with_name("sources.json")


def load_sources(path: Path | str = SOURCES_PATH) -> list[dict[str, Any]]:
    """Return validated source entries in their configured order."""
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("sources.json must contain a list")
    required = {"id", "url", "kind", "owner_group", "channels", "tos_status", "tos_note", "role"}
    allowed_kinds = {"rss", "json_gdelt", "json_hn", "json_reddit", "wiki_pageviews"}
    seen: set[str] = set()
    for source in data:
        missing = required - set(source)
        if missing:
            raise ValueError(f"source missing fields: {sorted(missing)}")
        if source["id"] in seen or source["kind"] not in allowed_kinds:
            raise ValueError(f"invalid source: {source['id']}")
        if source["tos_status"] not in {"ok", "pending", "blocked"}:
            raise ValueError(f"invalid ToS status: {source['id']}")
        if source["role"] not in {"article", "article+signal", "primary", "signal"}:
            raise ValueError(f"invalid source role: {source['id']}")
        seen.add(source["id"])
    return data


def source_map(path: Path | str = SOURCES_PATH) -> dict[str, dict[str, Any]]:
    return {source["id"]: source for source in load_sources(path)}
