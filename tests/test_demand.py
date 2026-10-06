"""Bước 3 — đọc nhu cầu: 3 mục thêm vào brief tuần. Không đụng next_draft, không tự áp gì.

Thiết kế: docs/audit/2026-10-05-demand-design.md. Mạng là fake.
"""
from datetime import date, timedelta

import pytest

from factory import store
from factory.analytics import ReportRejected
from factory.analytics_fake import FakeAnalytics
from factory.demand import (ArticleMissing, WikiError, interest, render_demand, search_terms,
                            studio_gaps)

FRONTIER = date(2026, 10, 2)
TODAY = date(2026, 10, 5)                      # Wikipedia: tới hôm qua UTC = 04/10


# ── (A) từ khoá đã dẫn người xem tới kênh ─────────────────────────────────

def test_search_terms_is_one_capped_request_over_28_inclusive_days_ending_at_the_frontier():
    api = FakeAnalytics(frontier=FRONTIER)
    api.search_terms = [("robot framework with python", 42), ("playwright locators", 15)]

    out = search_terms(api, FRONTIER)

    assert out.rows == [("robot framework with python", 42), ("playwright locators", 15)]
    [q] = api.queries
    assert (q["start"], q["end"]) == (FRONTIER - timedelta(days=27), FRONTIER)
    assert (q["dimensions"], q["metrics"]) == ("insightTrafficSourceDetail", "views")
    assert q["search"] is True


def test_no_search_rows_says_so_explicitly_and_a_400_says_error():
    api = FakeAnalytics(frontier=FRONTIER)
    assert "không có dữ liệu" in search_terms(api, FRONTIER).note
    api.reject_dimensions = {"insightTrafficSourceDetail"}
    assert search_terms(api, FRONTIER).note == "lỗi"


def test_without_a_frontier_no_search_request_is_made():
    api = FakeAnalytics(frontier=FRONTIER)
    out = search_terms(api, None)
    assert api.queries == [] and "chưa có mốc" in out.note


# ── (B) mức quan tâm Wikipedia ────────────────────────────────────────────

class FakeWiki:
    """Lượt xem theo ngày của từng bài; ngày không có = 0 (Wikimedia bỏ trống ngày 0)."""

    def __init__(self):
        self.days: dict[str, dict[date, int]] = {}
        self.missing: set[str] = set()          # bài không tồn tại -> 404
        self.fail: dict[str, int] = {}          # bài -> số lần ném WikiError
        self.calls: list[tuple[str, date, date]] = []

    def set(self, article, start, end, per_day):
        d = start
        while d <= end:
            self.days.setdefault(article, {})[d] = per_day
            d += timedelta(days=1)

    def daily(self, article, start, end):
        self.calls.append((article, start, end))
        if self.fail.get(article):
            self.fail[article] -= 1
            raise WikiError("429 sau 3 lần lùi")
        if article in self.missing:
            raise ArticleMissing(article)
        days = self.days.get(article, {})
        got = {d: v for d, v in days.items() if start <= d <= end}
        if not got and not days:
            raise ArticleMissing(article)
        return got


@pytest.fixture
def conn(tmp_path):
    with store.connect(tmp_path / "state.sqlite") as c:
        yield c


Y = TODAY - timedelta(days=1)                   # 04/10/2026
RECENT = (Y - timedelta(days=27), Y)
PRIOR = (RECENT[0] - timedelta(days=365), Y - timedelta(days=365))


def test_yoy_is_shown_only_when_both_years_have_at_least_20_a_day(conn):
    w = FakeWiki()
    w.set("ChatGPT", *RECENT, 120)
    w.set("ChatGPT", *PRIOR, 60)
    w.set("Gemini", *RECENT, 40)                # sản phẩm mới: năm ngoái chưa có bài
    w.set("Ít_người_xem", *RECENT, 5)
    w.set("Ít_người_xem", *PRIOR, 3)
    topics = [{"topic": "ChatGPT", "articles": ["ChatGPT"]},
              {"topic": "Gemini", "articles": ["Gemini"]},
              {"topic": "Ít", "articles": ["Ít_người_xem"]}]

    rows = {r.topic: r for r in interest(conn, w, topics, today=TODAY, sleep=lambda s: None)}

    assert (rows["ChatGPT"].level, rows["ChatGPT"].yoy) == (120, 2.0)
    assert rows["Gemini"].level == 40 and rows["Gemini"].label == "chưa có cùng kỳ"
    assert rows["Ít"].level == 5 and rows["Ít"].label == "chưa đủ"


def test_a_day_missing_from_the_response_counts_as_zero_before_the_median(conn):
    w = FakeWiki()
    w.set("A", *RECENT, 100)
    for k in range(15):                         # 15/28 ngày không có số -> trung vị là 0
        del w.days["A"][RECENT[0] + timedelta(days=k)]
    [r] = interest(conn, w, [{"topic": "A", "articles": ["A"]}], today=TODAY, sleep=lambda s: None)
    assert r.level == 0


def test_topic_level_is_the_median_of_the_daily_sum_not_a_sum_of_medians(conn):
    w = FakeWiki()
    # Bài 1 cao ngày lẻ, bài 2 cao ngày chẵn: tổng mỗi ngày = 100; tổng hai trung vị sẽ là 0 hoặc 200.
    d = RECENT[0]
    while d <= RECENT[1]:
        odd = d.toordinal() % 2
        w.days.setdefault("X1", {})[d] = 100 if odd else 0
        w.days.setdefault("X2", {})[d] = 0 if odd else 100
        d += timedelta(days=1)
    [r] = interest(conn, w, [{"topic": "X", "articles": ["X1", "X2"]}], today=TODAY, sleep=lambda s: None)
    assert r.level == 100 and r.n_articles == 2


def test_a_missing_article_is_never_cached_as_zeros_and_marks_the_topic_incomplete(conn):
    w = FakeWiki()
    w.set("Đúng", *RECENT, 50)
    w.missing.add("Sai_tên")
    topics = [{"topic": "T", "articles": ["Đúng", "Sai_tên"]}]

    [r] = interest(conn, w, topics, today=TODAY, sleep=lambda s: None)

    assert r.label.startswith("thiếu") and r.level is None
    assert conn.execute("SELECT COUNT(*) FROM wiki_daily WHERE article = 'Sai_tên'").fetchone()[0] == 0


def test_the_365_day_shift_survives_29_february(conn):
    w = FakeWiki()
    leap = date(2028, 3, 30)                    # cửa sổ năm trước chạm 29/02/2027? không có -> vẫn chạy
    w.set("A", leap - timedelta(days=28), leap - timedelta(days=1), 30)
    w.set("A", leap - timedelta(days=28 + 365), leap - timedelta(days=1 + 365), 30)
    [r] = interest(conn, w, [{"topic": "A", "articles": ["A"]}], today=leap, sleep=lambda s: None)
    assert r.yoy == 1.0


def test_a_second_run_fetches_only_the_uncached_tail(conn):
    w = FakeWiki()
    w.set("A", PRIOR[0], RECENT[1] + timedelta(days=3), 30)
    topics = [{"topic": "A", "articles": ["A"]}]
    interest(conn, w, topics, today=TODAY, sleep=lambda s: None)
    w.calls.clear()

    interest(conn, w, topics, today=TODAY + timedelta(days=2), sleep=lambda s: None)

    # Cả hai cửa sổ trượt 2 ngày: chỉ lấy phần đuôi chưa có (ngày gần nhất không cache
    # vì Wikimedia có thể chưa chốt số), không lấy lại 28 + 28 ngày.
    assert len(w.calls) == 2
    assert sum((e - s).days + 1 for _, s, e in w.calls) <= 6
    assert max(e for _, _, e in w.calls) == TODAY + timedelta(days=1)


def test_a_wikimedia_error_shows_as_error_and_writes_nothing(conn):
    w = FakeWiki()
    w.set("A", *RECENT, 30)
    w.fail["A"] = 99
    [r] = interest(conn, w, [{"topic": "A", "articles": ["A"]}], today=TODAY, sleep=lambda s: None)
    assert r.label.startswith("thiếu")
    assert conn.execute("SELECT COUNT(*) FROM wiki_daily").fetchone()[0] == 0


# ── (C) khoảng trống dán tay từ YouTube Studio ────────────────────────────

def test_studio_gaps_are_included_only_when_their_own_date_is_at_most_14_days_old(tmp_path):
    f = tmp_path / "MIM-studio.md"
    f.write_text("Ngày: 2026-09-25\n- AI agent là gì\n", encoding="utf-8")
    assert "AI agent là gì" in studio_gaps(f, today=TODAY)
    f.write_text("Ngày: 2026-09-01\n- AI agent là gì\n", encoding="utf-8")
    assert "AI agent là gì" not in studio_gaps(f, today=TODAY)
    assert "dán" in studio_gaps(tmp_path / "chưa-có.md", today=TODAY)


def test_render_puts_all_three_sections_in_the_brief(conn, tmp_path):
    api = FakeAnalytics(frontier=FRONTIER)
    api.search_terms = [("ai là gì", 9)]
    w = FakeWiki()
    w.set("ChatGPT", *RECENT, 120)
    md = render_demand(conn, "MIM", api, w, frontier=FRONTIER, today=TODAY,
                       watchlist=[{"topic": "ChatGPT", "articles": ["ChatGPT"]}],
                       studio_file=tmp_path / "none.md", sleep=lambda s: None)
    assert "ai là gì" in md and "ChatGPT" in md and "YouTube Studio" in md


# ── hồi quy từ review (Grok vòng 3 + review hai trục) ─────────────────────

class StrictWiki(FakeWiki):
    """Như Wikimedia thật: khoảng ngày KHÔNG có dòng nào -> 404, kể cả bài có tồn tại."""

    def daily(self, article, start, end):
        got = super().daily(article, start, end)
        if not got:
            raise ArticleMissing(article)
        return got


def test_an_empty_tail_on_a_later_run_keeps_the_cached_level(conn):
    # Grok: lần 2 chỉ hỏi vài ngày cuối; Wikimedia chưa có số -> 404 -> cả chủ đề "thiếu".
    w = StrictWiki()
    w.set("A", PRIOR[0], RECENT[1] - timedelta(days=3), 50)     # dump dừng sớm 3 ngày
    topics = [{"topic": "A", "articles": ["A"]}]
    interest(conn, w, topics, today=TODAY, sleep=lambda s: None)

    [r] = interest(conn, w, topics, today=TODAY + timedelta(days=2), sleep=lambda s: None)

    assert r.level == 50 and r.label != "thiếu"


def test_days_missing_from_a_payload_are_not_frozen_as_zero_unless_a_later_day_proves_it(conn):
    w = FakeWiki()
    w.set("A", PRIOR[0], RECENT[1] - timedelta(days=5), 40)     # 5 ngày cuối chưa có trong dump
    interest(conn, w, [{"topic": "A", "articles": ["A"]}], today=TODAY, sleep=lambda s: None)
    cached = {r[0] for r in conn.execute("SELECT day FROM wiki_daily WHERE article='A'")}
    assert (RECENT[1] - timedelta(days=3)).isoformat() not in cached


def test_one_article_without_last_year_does_not_erase_its_siblings_comparison(conn):
    w = FakeWiki()
    w.set("Cũ", *RECENT, 100)
    w.set("Cũ", *PRIOR, 50)
    w.set("Mới", *RECENT, 20)                    # bài mới: năm ngoái 404

    class W(FakeWiki):
        def daily(self, article, start, end):
            if article == "Mới" and end < RECENT[0]:
                raise ArticleMissing(article)
            return w.daily(article, start, end)

    [r] = interest(conn, W(), [{"topic": "T", "articles": ["Cũ", "Mới"]}], today=TODAY, sleep=lambda s: None)
    assert r.yoy == round(120 / 50, 2)


def test_missing_label_names_the_article_that_failed(conn):
    w = FakeWiki()
    w.set("Đúng", *RECENT, 50)
    w.missing.add("Sai_tên")
    [r] = interest(conn, w, [{"topic": "T", "articles": ["Đúng", "Sai_tên"]}], today=TODAY, sleep=lambda s: None)
    assert "Sai_tên" in r.label


def test_throttle_also_follows_a_failed_request(conn):
    w = FakeWiki()
    w.missing.add("X")
    w.set("Y", *RECENT, 10)
    slept = []
    interest(conn, w, [{"topic": "X", "articles": ["X"]}, {"topic": "Y", "articles": ["Y"]}],
             today=TODAY, sleep=slept.append)
    assert len(slept) >= 3                       # sau 404 của X vẫn giãn nhịp trước khi hỏi Y


def test_any_analytics_failure_on_search_terms_is_shown_as_error_not_a_crash():
    from factory.youtube_api import NetworkDown, RateLimited

    class Down(FakeAnalytics):
        def __init__(self, exc):
            super().__init__(frontier=FRONTIER)
            self.exc = exc

        def top_search_terms(self, **kw):
            raise self.exc

    for exc in (RateLimited("429"), NetworkDown("dns")):
        assert search_terms(Down(exc), FRONTIER).note == "lỗi"


def test_studio_date_must_be_on_the_first_line_and_not_in_the_future(tmp_path):
    f = tmp_path / "s.md"
    f.write_text("- XYZ_DAN_TAY\nNgày: 2026-10-01\n", encoding="utf-8")           # ngày không ở dòng đầu
    assert "XYZ_DAN_TAY" not in studio_gaps(f, today=TODAY)
    f.write_text("Ngày: 2026-12-01\n- XYZ_DAN_TAY\n", encoding="utf-8")           # ngày ở tương lai
    assert "XYZ_DAN_TAY" not in studio_gaps(f, today=TODAY)


def test_a_pipe_in_a_search_term_does_not_break_the_table(conn, tmp_path):
    api = FakeAnalytics(frontier=FRONTIER)
    api.search_terms = [("a | b", 3)]
    md = render_demand(conn, "MIM", api, FakeWiki(), frontier=FRONTIER, today=TODAY, watchlist=[],
                       studio_file=tmp_path / "x.md", sleep=lambda s: None)
    assert "| a \\| b | 3 |" in md


# ── HttpPageviews: chi tiết HTTP ─────────────────────────────────────────

import io  # noqa: E402
import json as _json  # noqa: E402
import urllib.error  # noqa: E402

from factory.demand import HttpPageviews  # noqa: E402


class _Resp:
    def __init__(self, body: bytes):
        self._b = body

    def read(self):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _net(*script):
    seen = []

    def urlopen(req, timeout=None):
        seen.append(req)
        nxt = script[len(seen) - 1]
        if isinstance(nxt, Exception):
            raise nxt
        return _Resp(nxt)
    return urlopen, seen


def _http(code):
    return urllib.error.HTTPError("u", code, "x", {}, io.BytesIO(b""))


def test_pageviews_backs_off_on_429_and_sends_an_identifying_user_agent():
    body = _json.dumps({"items": [{"timestamp": "2026100100", "views": 7}]}).encode()
    urlopen, seen = _net(_http(429), body)
    slept = []
    got = HttpPageviews(urlopen=urlopen, sleep=slept.append).daily("A", date(2026, 10, 1), date(2026, 10, 1))
    assert got == {date(2026, 10, 1): 7} and slept == [2]
    assert "github.com" in seen[0].get_header("User-agent")


def test_pageviews_404_is_article_missing_and_garbage_is_a_wiki_error():
    urlopen, _ = _net(_http(404))
    with pytest.raises(ArticleMissing):
        HttpPageviews(urlopen=urlopen, sleep=lambda s: None).daily("A", date(2026, 10, 1), date(2026, 10, 1))
    urlopen, _ = _net(b"not json")
    with pytest.raises(WikiError):
        HttpPageviews(urlopen=urlopen, sleep=lambda s: None).daily("A", date(2026, 10, 1), date(2026, 10, 1))
