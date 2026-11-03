from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from factory.trend.benchmark import _jaccard, _match_article, _tokens, evaluate_benchmark
from factory.trend.cluster import _matching_signals, cluster_articles, cluster_db, event_from_group
from factory.trend.independence import independent_sources
from factory.trend.report import _belongs, vn_impact, write_report
from factory.trend.scan import _article, _rate_limited, _wiki_history, init_db, normalize_stored_articles, parse_gdelt_json, parse_rss, parse_trends_articles, parse_trends_rss, parse_wiki_pageviews, scan_sources
from factory.trend.sources import load_sources


ROOT = Path(__file__).parent / "fixtures" / "trend"
NOW = datetime(2026, 11, 2, 12, tzinfo=UTC)


def source(source_id: str, status: str = "ok", role: str = "article", kind: str = "rss") -> dict[str, object]:
    return {"id": source_id, "url": f"https://{source_id}.test/rss", "kind": kind, "role": role,
            "owner_group": source_id, "channels": ["MIM", "CK"], "tos_status": status, "tos_note": "fixture", "trial": "internal"}


def test_parse_rss_limits_summary_and_atom() -> None:
    items = parse_rss((ROOT / "rss.xml").read_bytes(), source("rss"), NOW)
    atom = parse_rss((ROOT / "atom.xml").read_bytes(), source("atom"), NOW)
    assert items[0]["url"] == "https://example.test/one" and len(items[0]["summary"]) <= 300
    assert items[1]["title"] == "Gi\u00e1 v\u00e0ng 'h\u00f4m nay'" and items[1]["summary"] == "Gi\u00e1 \u00e1 m\u1edbi"
    assert atom[0]["url"] == "https://example.test/two"


def test_stored_articles_are_migrated() -> None:
    conn = init_db(":memory:")
    conn.execute("INSERT INTO article(url,title,summary,published_at,source_id,owner_group,fetched_at,undated) VALUES(?,?,?,?,?,?,?,?)", (
        "https://example.test/entity", "Gi&aacute; v&amp;agrave;ng", "&lt;p&gt;N\u1ed9i dung&lt;/p&gt;", NOW.isoformat(), "s1", "s1", NOW.isoformat(), 0,
    ))
    assert normalize_stored_articles(conn) == 1
    row = conn.execute("SELECT title, summary FROM article").fetchone()
    assert tuple(row) == ("Gi\u00e1 v\u00e0ng", "N\u1ed9i dung")


def test_google_trends_news_items_become_articles_with_publisher_owner() -> None:
    trends = source("google_trends_vn", role="article+signal")
    payload = (ROOT / "google_trends_vn.xml").read_bytes()
    articles = parse_trends_articles(payload, trends, NOW)
    signals = parse_trends_rss(payload, trends, NOW)
    assert articles == [{"url": "https://www.24h.com.vn/tin-tuc-trong-ngay/mien-bac-sap-chuyen-ret-do-khong-khi-lanh-manh-c46a1807791.html", "title": "Miền Bắc sắp chuyển rét do không khí lạnh mạnh", "summary": "", "published_at": "2026-11-02T12:00:00+00:00", "source_id": "google_trends_vn", "owner_group": "Tin tức 24h", "fetched_at": "2026-11-02T12:00:00+00:00", "undated": 1, "trend_title": "du bao thoi tiet da nang"}]
    assert signals[0]["title"] == "dự báo thời tiết đà nẵng" and signals[0]["value"] == 200000
    assert _matching_signals(articles, signals) == [{"source_id": "google_trends_vn", "title": "dự báo thời tiết đà nẵng", "value": 200000.0, "baseline": None, "kind": "trends"}]


def test_wiki_is_signal_only_and_filters_namespaces() -> None:
    payload = json.dumps({"items": [{"articles": [
        {"article": "Artificial intelligence", "views": 12345}, {"article": "Special:Search", "views": 999},
        {"article": "Trang_Chính", "views": 999}, {"article": "File:Logo.svg", "views": 999},
    ]}]}).encode()
    signals = parse_wiki_pageviews(payload, source("wiki", kind="wiki_pageviews", role="signal"), NOW)
    assert [item["title"] for item in signals] == ["Artificial intelligence"]


def test_scan_never_calls_pending_or_blocked_sources(monkeypatch) -> None:
    sources = [source("allowed"), source("pending", "pending"), source("blocked", "blocked")]
    called: list[str] = []
    def fetch(url: str) -> bytes:
        called.append(url); return (ROOT / "rss.xml").read_bytes()
    conn = init_db(":memory:")
    monkeypatch.setattr("factory.trend.scan.load_sources", lambda: sources)
    monkeypatch.setattr("factory.trend.scan.init_db", lambda _path: conn)
    result = scan_sources(fetch=fetch, pause_seconds=0, now=NOW)
    assert result == {"sources": 1, "articles": 2, "signals": 0, "errors": 0}
    assert called == ["https://allowed.test/robots.txt", "https://allowed.test/rss"]


def test_gdelt_empty_json_is_successful_and_records_zero_articles(monkeypatch) -> None:
    gdelt = source("gdelt_vi_news", kind="json_gdelt")
    waited: list[float] = []
    conn = init_db(":memory:")
    monkeypatch.setattr("factory.trend.scan.load_sources", lambda: [gdelt])
    monkeypatch.setattr("factory.trend.scan.init_db", lambda _path: conn)
    monkeypatch.setattr("factory.trend.scan.time.sleep", waited.append)
    result = scan_sources(fetch=lambda _url: b'{"articles": []}', pause_seconds=0, now=NOW)
    assert result == {"sources": 1, "articles": 0, "signals": 0, "errors": 0}
    assert waited == [5.0]
    assert parse_gdelt_json(b'{"articles": []}', gdelt, NOW) == []


def test_gdelt_uses_publisher_domain_for_independence() -> None:
    gdelt = source("gdelt_vi_news")
    first = _article("https://www.publisher.test/a", "AI update", "", "", gdelt, NOW)
    second = _article("https://publisher.test/b", "AI update", "", "", gdelt, NOW)
    other = _article("https://other.test/c", "AI update", "", "", gdelt, NOW)
    assert first["owner_group"] == "publisher.test"
    assert independent_sources([first, second, other], duplicate_threshold=1.1) == 2


def test_wiki_falls_back_when_yesterday_is_not_ready() -> None:
    calls: list[str] = []
    payload = json.dumps({"items": [{"articles": [{"article": "Artificial intelligence", "views": 12345}]}]}).encode()
    wiki = source("wiki", kind="wiki_pageviews", role="signal")
    wiki["url"] = "https://wiki.test/top/vi.wikipedia/all-access/{YYYY}/{MM}/{DD}"
    def fetch(url: str) -> bytes:
        calls.append(url)
        if len(calls) == 1:
            raise OSError("404 not ready")
        return payload
    signals = _wiki_history(wiki, NOW, fetch)
    assert signals[0]["title"] == "Artificial intelligence"
    assert "/2026/11/01" in calls[0] and "/2026/10/31" in calls[1]


def test_cluster_fixture_precision_is_at_least_point_eight() -> None:
    articles = json.loads((ROOT / "cluster_40.json").read_text(encoding="utf-8"))
    groups = cluster_articles(articles)
    correct = sum(1 for group in groups if len({article["event"] for article in group}) == 1)
    assert correct / len(groups) >= 0.8 and len(groups) == 20


def test_cluster_does_not_link_on_static_or_window_common_entity_alone() -> None:
    def article(article_id: int, title: str) -> dict[str, object]:
        return {"id": article_id, "title": title, "published_at": f"2026-11-01T{article_id:02}:00:00+00:00"}

    articles = [
        article(1, "Google climate platform satellite mission"),
        article(2, "Google finance platform market report"),
        article(3, "Nexus climate platform satellite mission"),
        article(4, "Nexus finance platform market report"),
    ]
    articles.extend(article(index, f"bản tin thường nhật số {index}") for index in range(5, 21))
    groups = cluster_articles(articles)
    by_id = {item["id"]: group for group in groups for item in group}
    assert by_id[1] != by_id[2]  # Google is a static generic entity.
    assert by_id[3] != by_id[4]  # Nexus occurs in >5% of this window.


def test_cluster_splits_low_cohesion_bridge_chain() -> None:
    articles = [
        {"id": 1, "title": "Orion lunar satellite sends aurora images", "published_at": "2026-11-01T00:00:00+00:00"},
        {"id": 2, "title": "Orion lunar satellite sends climate data from orbit", "published_at": "2026-11-01T01:00:00+00:00"},
        {"id": 3, "title": "Orion climate data predict crop failures", "published_at": "2026-11-01T02:00:00+00:00"},
    ]
    groups = cluster_articles(articles)
    assert sorted(sorted(item["id"] for item in group) for group in groups) == [[1, 2], [3]]


def test_channel_keyword_filter_rejects_unrelated_event() -> None:
    sources = {"s1": source("s1")}
    keywords = {"MIM": ["ai", "chip"], "CK": ["thuế"]}
    ai_article = {"source_id": "s1", "title": "AI chip update", "summary": ""}
    false_ai = {"source_id": "s1", "title": "Hai người cập nhật", "summary": ""}
    festival = {"source_id": "s1", "title": "Local festival", "summary": ""}
    assert _belongs(ai_article, "MIM", sources, keywords)
    assert not _belongs(false_ai, "MIM", sources, keywords)
    assert not _belongs(festival, "MIM", sources, keywords)


def test_sources_file_loads_with_utf8_bom() -> None:
    assert any(item["id"] == "google_trends_vn" for item in load_sources())


def test_stale_and_primary_articles_do_not_create_events(monkeypatch) -> None:
    conn = init_db(":memory:")
    try:
        primary = source("primary", role="primary")
        article = source("article")
        conn.executemany("INSERT INTO article(url,title,summary,published_at,source_id,owner_group,fetched_at,undated) VALUES(:url,:title,:summary,:published_at,:source_id,:owner_group,:fetched_at,:undated)", [
            _article("https://primary.test/one", "OpenAI Update", "", "Sun, 02 Nov 2026 11:00:00 +0000", primary, NOW),
            _article("https://article.test/old", "OpenAI Update", "", "Thu, 29 Oct 2026 11:00:00 +0000", article, NOW),
        ])
        conn.commit()
    finally:
        conn.commit()
    monkeypatch.setattr("factory.trend.cluster.source_map", lambda *_args: {"primary": primary, "article": article})
    monkeypatch.setattr("factory.trend.cluster.sqlite3.connect", lambda _path: conn)
    assert cluster_db(":memory:", now=NOW) == 0


def test_robots_disallow_records_block_without_fetching_feed(monkeypatch) -> None:
    calls: list[str] = []
    def fetch(url: str) -> bytes:
        calls.append(url)
        return b"User-agent: *\nDisallow: /rss\n"
    conn = init_db(":memory:")
    monkeypatch.setattr("factory.trend.scan.init_db", lambda _path: conn)
    monkeypatch.setattr("factory.trend.scan.load_sources", lambda _path=None: [source("blocked")])
    result = scan_sources(fetch=fetch, pause_seconds=0, now=NOW)
    assert result == {"sources": 0, "articles": 0, "signals": 0, "errors": 0}
    assert calls == ["https://blocked.test/robots.txt"]


def test_rate_skip_uses_persisted_successful_feed_time() -> None:
    conn = init_db(":memory:")
    conn.execute("INSERT INTO run(started_at,ended_at,source_id,status) VALUES(?,?,?,?)", (NOW.isoformat(), NOW.isoformat(), "trial", "ok"))
    assert _rate_limited(conn, "trial", NOW.replace(hour=13))
    assert not _rate_limited(conn, "trial", NOW.replace(hour=16))


def test_vn_impact_requires_direct_or_global_pair() -> None:
    keywords = {"vn_impact": {"direct": ["Vietnam"], "MIM": {"entities": ["OpenAI"], "events": ["launch"]}, "CK": {"entities": ["Fed"], "events": ["rate cut"]}}}
    assert vn_impact({"title": "OpenAI launch reaches Vietnam", "summary": ""}, "MIM", keywords)
    assert vn_impact({"title": "OpenAI launch", "summary": ""}, "MIM", keywords)
    assert not vn_impact({"title": "OpenAI hires a designer", "summary": ""}, "MIM", keywords)


def test_benchmark_counts_matching_relevant_candidate_articles(monkeypatch) -> None:
    conn = init_db(":memory:")
    item = _article("https://example.test/story", "OpenAI launches Gemini", "", "2026-11-02T12:00:00Z", source("s1"), NOW)
    conn.execute("INSERT INTO article(url,title,summary,published_at,source_id,owner_group,fetched_at,undated,trend_title) VALUES(:url,:title,:summary,:published_at,:source_id,:owner_group,:fetched_at,:undated,:trend_title)", item)
    article = dict(conn.execute("SELECT * FROM article").fetchone())
    event = event_from_group([article])
    conn.execute("INSERT INTO event(id,label,entities,first_seen,last_seen,article_ids,signals) VALUES(:id,:label,:entities,:first_seen,:last_seen,:article_ids,'[]')", event)
    conn.commit()
    monkeypatch.setattr("factory.trend.benchmark.source_map", lambda *_args: {"s1": {**source("s1"), "lang": "vi", "channels": ["MIM"]}})
    result = evaluate_benchmark(ROOT / "benchmark_small.json", conn)
    assert [event["caught"] for event in result["events"]] == [True, True]


def test_benchmark_matching_uses_entity_cores_accentless_tokens_and_jaccard_threshold() -> None:
    evn_target = {
        "label": "Tập đoàn Điện lực Việt Nam (EVN) giảm giá bán lẻ điện bình quân",
        "entities": ["Tập đoàn Điện lực Việt Nam (EVN)", "Giá bán lẻ điện bình quân"],
    }
    assert _match_article({"title": "EVN giảm giá điện từ ngày 1.11", "summary": ""}, evn_target)

    accentless_target = {"label": "Giá vàng miếng SJC tăng đầu tuần", "entities": []}
    assert _match_article({"title": "Gia vang mieng SJC tang dau tuan", "summary": ""}, accentless_target)

    assert _jaccard(_tokens("Alpha delta"), _tokens("Alpha beta gamma")) == 0.25
    threshold_target = {"label": "Alpha beta gamma", "entities": []}
    assert _match_article({"title": "Alpha delta", "summary": ""}, threshold_target)
    assert not _match_article({"title": "Alpha delta epsilon", "summary": ""}, threshold_target)

    price_target = {"label": "Giá vàng trong nước", "entities": ["Giá vàng"]}
    assert not _match_article({"title": "Giá thịt heo giảm", "summary": ""}, price_target)


def test_lead_manual_match_pairs_are_regression_covered() -> None:
    benchmark = json.loads((Path("docs/pm/tickets/GH-31-benchmark.json")).read_text(encoding="utf-8"))
    targets = {item["id"]: item for item in benchmark["events"]}
    cases = json.loads((ROOT / "lead_match_regression.json").read_text(encoding="utf-8"))
    for case in cases:
        actual = _match_article({"title": case["title"], "summary": ""}, targets[case["id"]])
        assert bool(actual) is case["expected"], case["id"]


def test_benchmark_separates_coverage_from_candidate_recall(monkeypatch) -> None:
    conn = init_db(":memory:")
    article = _article("https://example.test/evn", "EVN giảm giá điện", "", NOW.isoformat(), source("s1"), NOW)
    conn.execute("INSERT INTO article(url,title,summary,published_at,source_id,owner_group,fetched_at,undated,trend_title) VALUES(:url,:title,:summary,:published_at,:source_id,:owner_group,:fetched_at,:undated,:trend_title)", article)
    monkeypatch.setattr("factory.trend.benchmark.source_map", lambda *_args: {"s1": source("s1")})
    result = evaluate_benchmark(ROOT / "benchmark_coverage.json", conn)
    assert result["channels"]["CK"] == {
        "coverage_caught": 1, "candidate_caught": 0, "total": 1,
        "hotness": {"high": {"coverage_caught": 1, "candidate_caught": 0, "total": 1}, "medium": {"coverage_caught": 0, "candidate_caught": 0, "total": 0}},
        "missed": [result["events"][0]],
    }
    assert result["events"][0]["reason"] == "không gom được: EVN giảm giá điện"


def test_benchmark_miss_reasons_distinguish_source_filter_and_clustering(monkeypatch) -> None:
    conn = init_db(":memory:")
    filtered = _article("https://filtered.test/story", "OpenAI update", "", NOW.isoformat(), source("filtered"), NOW)
    unclustered = _article("https://unclustered.test/story", "Gemini update", "", NOW.isoformat(), source("unclustered"), NOW)
    conn.executemany("INSERT INTO article(url,title,summary,published_at,source_id,owner_group,fetched_at,undated,trend_title) VALUES(:url,:title,:summary,:published_at,:source_id,:owner_group,:fetched_at,:undated,:trend_title)", [filtered, unclustered])
    conn.commit()
    monkeypatch.setattr("factory.trend.benchmark.source_map", lambda *_args: {
        "filtered": {**source("filtered"), "channels": ["CK"]},
        "unclustered": source("unclustered"),
    })
    monkeypatch.setattr("factory.trend.benchmark._keywords", lambda: {"MIM": ["openai", "gemini"], "CK": []})
    result = evaluate_benchmark(ROOT / "benchmark_reasons.json", conn)
    assert [item["reason"] for item in result["events"]] == [
        "kh\u00f4ng c\u00f3 ngu\u1ed3n \u0111\u01b0a tin",
        "b\u1ecb l\u1ecdc t\u1eeb kh\u00f3a: OpenAI update",
        "kh\u00f4ng gom \u0111\u01b0\u1ee3c: Gemini update",
    ]
