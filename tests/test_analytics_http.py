"""HttpAnalytics: chi tiết HTTP của YouTube Analytics / Data API (đọc). Mạng là stub."""
import io
import json
import urllib.error
import urllib.parse
from datetime import date

import pytest

from factory.analytics import HttpAnalytics, ReportRejected
from factory.youtube_api import HttpYouTube

CREDS = {"client_id": "c", "client_secret": "s", "refresh_token": "r"}


class Resp:
    def __init__(self, body):
        self._b = json.dumps(body).encode()
        self.headers = {}

    def read(self):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class Net:
    def __init__(self, *script):
        self.script, self.urls = list(script), []

    def __call__(self, req, timeout=None):
        if "oauth2" in req.full_url:
            return Resp({"access_token": "tok"})
        self.urls.append(req.full_url)
        nxt = self.script.pop(0)
        if isinstance(nxt, Exception):
            raise nxt
        return Resp(nxt)

    def params(self, i):
        return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.urls[i]).query))


def make(net, **kw):
    return HttpAnalytics(HttpYouTube(CREDS, urlopen=net, sleep=lambda s: None), **kw)


def page(*rows):
    return {"columnHeaders": [{"name": "video"}, {"name": "views"}], "rows": [list(r) for r in rows]}


def test_report_follows_every_page_and_names_columns():
    net = Net(page(("a", 1), ("b", 2)), page(("c", 3)))
    rows = make(net, page_size=2).report(start=date(2026, 10, 6), end=date(2026, 10, 8), metrics="views",
                                         dimensions="video", video_ids=["a", "b", "c"])

    assert rows == [{"video": "a", "views": 1}, {"video": "b", "views": 2}, {"video": "c", "views": 3}]
    p0, p1 = net.params(0), net.params(1)
    assert p0["ids"] == "channel==MINE" and p0["filters"] == "video==a,b,c"
    assert (p0["startDate"], p0["endDate"]) == ("2026-10-06", "2026-10-08")
    assert (p0["startIndex"], p1["startIndex"]) == ("1", "3")


def test_a_400_from_analytics_is_a_rejected_report():
    err = urllib.error.HTTPError("u", 400, "x", {}, io.BytesIO(b'{"error": "Unknown identifier (engagedViews)"}'))
    with pytest.raises(ReportRejected):
        make(Net(err)).report(start=date(2026, 10, 6), end=date(2026, 10, 8), metrics="engagedViews",
                              dimensions="video", video_ids=["a"])


def test_video_facts_are_fetched_50_at_a_time_and_parsed():
    ids = [f"v{i}" for i in range(51)]
    item = lambda v: {"id": v, "status": {"privacyStatus": "private", "publishAt": "2026-10-20T04:30:00Z"},
                      "snippet": {"publishedAt": "2026-10-05T01:00:00Z"},
                      "contentDetails": {"duration": "PT1M5S"}}
    net = Net({"items": [item(v) for v in ids[:50]]}, {"items": [item(ids[50])]})

    facts = make(net).video_facts(ids)

    assert len(net.urls) == 2 and len(facts) == 51
    assert facts["v0"] == {"privacy": "private", "publish_at": "2026-10-20T04:30:00Z",
                           "published_at": "2026-10-05T01:00:00Z", "duration_s": 65}


def test_id_filtered_reports_send_no_sort_the_api_could_reject():
    # Grok vòng 3: sort=-engagedViews trên báo cáo theo video -> 400 -> cột quyết định NULL mãi.
    net = Net(page(("a", 1)))
    make(net).report(start=date(2026, 10, 6), end=date(2026, 10, 12), metrics="engagedViews,views",
                     dimensions="video", video_ids=["a"])
    assert "sort" not in net.params(0)


def test_top_search_terms_is_a_single_capped_sorted_request():
    net = Net({"columnHeaders": [{"name": "insightTrafficSourceDetail"}, {"name": "views"}],
               "rows": [["ai là gì", 9]]})
    rows = make(net, page_size=2).top_search_terms(start=date(2026, 9, 5), end=date(2026, 10, 2))
    assert rows == [{"insightTrafficSourceDetail": "ai là gì", "views": 9}]
    p = net.params(0)
    assert (p["filters"], p["sort"], p["maxResults"]) == ("insightTrafficSourceType==YT_SEARCH", "-views", "25")
    assert "startIndex" not in p and len(net.urls) == 1
