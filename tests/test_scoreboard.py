"""Vòng phản hồi analytics: đo đúng tuổi, so trong tuần, đề xuất có điều kiện.

Thiết kế: docs/audit/2026-10-05-feedback-loop-design.md. Mạng thay bằng FakeAnalytics.
"""
from datetime import date, datetime, timezone

from factory.scoreboard import pacific_date


def utc(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def test_morning_vietnam_slots_fall_on_the_previous_pacific_day():
    # 11:30 giờ VN ngày 06/10 = 04:30 UTC = 21:30 PDT ngày 05/10.
    assert pacific_date(utc("2026-10-06T04:30:00Z")) == date(2026, 10, 5)
    # 22:00 giờ VN ngày 06/10 = 15:00 UTC = 08:00 PDT cùng ngày 06/10.
    assert pacific_date(utc("2026-10-06T15:00:00Z")) == date(2026, 10, 6)


def test_pacific_date_switches_from_daylight_to_standard_time_on_1_november_2026():
    # PDT (UTC-7) kết thúc 09:00 UTC ngày 01/11/2026; sau đó PST (UTC-8).
    assert pacific_date(utc("2026-11-01T07:30:00Z")) == date(2026, 11, 1)    # 00:30 PDT
    assert pacific_date(utc("2026-11-01T08:30:00Z")) == date(2026, 11, 1)    # 01:30 PDT
    assert pacific_date(utc("2026-11-02T07:30:00Z")) == date(2026, 11, 1)    # 23:30 PST
    assert pacific_date(utc("2026-11-02T08:30:00Z")) == date(2026, 11, 2)    # 00:30 PST


def test_pacific_date_switches_to_daylight_time_in_march():
    # 2027: PDT bắt đầu 10:00 UTC Chủ nhật 14/03.
    assert pacific_date(utc("2027-03-14T07:30:00Z")) == date(2027, 3, 13)    # 23:30 PST
    assert pacific_date(utc("2027-03-15T06:30:00Z")) == date(2027, 3, 14)    # 23:30 PDT
    assert pacific_date(utc("2027-03-15T07:30:00Z")) == date(2027, 3, 15)    # 00:30 PDT


# ── thu số liệu (collect) ─────────────────────────────────────────────────

import pytest  # noqa: E402

from factory import store  # noqa: E402
from factory.analytics_fake import FakeAnalytics  # noqa: E402
from factory.channel import Channel  # noqa: E402
from factory.scoreboard import collect  # noqa: E402

NOW = utc("2026-10-20T03:00:00Z")


@pytest.fixture
def db(tmp_path):
    with store.connect(tmp_path / "state.sqlite") as conn:
        Channel("FS", None, conn)                       # tạo sổ upload_log
        yield conn


def published(conn, slug, video_id, code="FS"):
    conn.execute("INSERT INTO upload_log (channel, slug, title, state, video_id, started_at) "
                 "VALUES (?, ?, ?, 'done', ?, '2026-10-01T00:00:00Z')", (code, slug, slug, video_id))


def metrics(conn):
    return {r["slug"]: dict(r) for r in conn.execute("SELECT * FROM video_metrics")}


def test_window_is_go_live_pacific_day_through_plus_two_queried_once_per_cohort(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 17))
    for slug, vid in (("giap-a", "v1"), ("tru-b", "v2")):
        published(db, slug, vid)
        yt.add_video(vid, published_at="2026-10-07T04:30:00Z")   # 11:30 VN -> 06/10 PT
    yt.add_views("v1", date(2026, 10, 6), 100, engaged=90)
    yt.add_views("v1", date(2026, 10, 8), 50, engaged=40)
    yt.add_views("v1", date(2026, 10, 13), 999, engaged=999)       # ngày thứ 8: ngoài cửa sổ

    collect(db, "FS", yt, now=NOW)

    m = metrics(db)
    assert m["giap-a"]["pacific_date"] == "2026-10-06" and m["giap-a"]["slot_vn"] == "11:30"
    assert (m["giap-a"]["views"], m["giap-a"]["engaged_views"]) == (150, 130)
    assert (m["tru-b"]["views"], m["tru-b"]["engaged_views"]) == (0, 0)
    video_queries = [q for q in yt.queries if q["dimensions"] == "video"]
    assert [(q["start"], q["end"], sorted(q["video_ids"])) for q in video_queries] == \
        [(date(2026, 10, 6), date(2026, 10, 12), ["v1", "v2"])]


def test_a_window_whose_last_day_analytics_has_not_published_stays_open(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 11))                # mới có số tới 11/10 PT
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-06T15:00:00Z")        # 06/10 PT -> cần tới 12/10
    yt.add_views("v1", date(2026, 10, 6), 100, engaged=90)

    out = collect(db, "FS", yt, now=NOW)

    assert metrics(db) == {} and out["open"] == 1
    yt.frontier = date(2026, 10, 12)
    collect(db, "FS", yt, now=NOW)
    assert metrics(db)["giap-a"]["views"] == 100


def test_videos_not_live_yet_are_not_measured(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 19))
    published(db, "giap-later", "v1")
    yt.add_video("v1", privacy="private", publish_at="2026-11-01T04:30:00Z")   # hẹn giờ tương lai
    published(db, "giap-probe", "v2")
    yt.add_video("v2", privacy="private")                                       # private không lịch

    out = collect(db, "FS", yt, now=NOW)

    assert metrics(db) == {} and out["not_live"] == 2


def test_a_scheduled_video_is_anchored_on_its_publish_at(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 19))
    published(db, "giap-a", "v1")
    # Còn ghi private + publishAt đã qua (YouTube chưa kịp đổi trạng thái): lên sóng lúc publishAt.
    yt.add_video("v1", privacy="private", publish_at="2026-10-10T12:00:00Z")
    collect(db, "FS", yt, now=NOW)
    assert metrics(db)["giap-a"]["pacific_date"] == "2026-10-10" and metrics(db)["giap-a"]["slot_vn"] == "19:00"


def test_rejected_engaged_views_is_stored_as_null_never_copied_from_views(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 19), reject={"engagedViews"})
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-07T04:30:00Z")
    yt.add_views("v1", date(2026, 10, 6), 100, engaged=90)

    collect(db, "FS", yt, now=NOW)

    m = metrics(db)["giap-a"]
    assert m["views"] == 100 and m["engaged_views"] is None


def test_shorts_feed_views_are_summed_from_one_multi_video_source_query(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 19))
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-07T04:30:00Z")
    yt.add_views("v1", date(2026, 10, 6), 70, engaged=60, source="SHORTS")
    yt.add_views("v1", date(2026, 10, 7), 30, engaged=20, source="YT_SEARCH")

    collect(db, "FS", yt, now=NOW)

    assert metrics(db)["giap-a"]["shorts_views"] == 70
    assert len([q for q in yt.queries if q["dimensions"] == "video,insightTrafficSourceType"]) == 1


def test_a_failed_source_query_leaves_shorts_views_null_not_zero(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 19), reject_dimensions={"video,insightTrafficSourceType",
                                                                       "insightTrafficSourceType"})
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-07T04:30:00Z")
    yt.add_views("v1", date(2026, 10, 6), 70, engaged=60)

    collect(db, "FS", yt, now=NOW)

    assert metrics(db)["giap-a"]["views"] == 70 and metrics(db)["giap-a"]["shorts_views"] is None


def test_measured_videos_are_never_queried_again(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 19))
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-07T04:30:00Z")
    collect(db, "FS", yt, now=NOW)
    before = len(yt.queries)

    collect(db, "FS", yt, now=NOW)

    assert [q["dimensions"] for q in yt.queries[before:]] == ["day"]     # chỉ còn thăm dò ngày mới nhất


# ── so sánh (board) ───────────────────────────────────────────────────────

from datetime import timedelta  # noqa: E402

from factory.scoreboard import board, prepare  # noqa: E402

MON = date(2026, 10, 12)                       # thứ Hai, sau mốc 01/10
CLOSED = utc("2026-11-20T03:00:00Z")           # mọi tuần tháng 10 đã đóng
# Hai tuần 12/10 + 19/10 đã đóng (19/10 + 6 ngày + 7 ngày cửa sổ) và còn trong 28 ngày gần nhất.
RECENT = utc("2026-11-02T03:00:00Z")
RECENT_FRONTIER = date(2026, 11, 1)


def put(conn, slug, day, engaged, *, slot="11:30", views=None, code="FS"):
    conn.execute("INSERT INTO video_metrics (channel, slug, video_id, kind, go_live, pacific_date, slot_vn, "
                 "views, engaged_views, shorts_views, avd, avp, duration_s, collected_at) "
                 "VALUES (?, ?, ?, 'short', '2026-10-01T00:00:00Z', ?, ?, ?, ?, NULL, NULL, NULL, 30, 'x')",
                 (code, slug, "id-" + slug, day.isoformat(), slot,
                  engaged if views is None else views, engaged))


def week(conn, prefix, n=15, start=MON, code="FS", **kw):
    """n video của một dòng trong một tuần; engaged tăng dần 100, 200, ..."""
    for i in range(n):
        put(conn, f"{prefix}{start:%m%d}-{i}", start + timedelta(days=i % 7), 100 * (i + 1), code=code, **kw)


@pytest.fixture
def sb(db):
    prepare(db, "FS")
    prepare(db, "CL")
    return db


def test_ties_share_the_midrank(sb):
    for i, e in enumerate([10, 50, 50, 90] + [1000 + i for i in range(11)]):
        put(sb, f"giap-{i}", MON, e)
    b = board(sb, "FS", frontier=date(2026, 11, 18))
    r = {v.slug: v.rank for v in b.ranked}
    assert r["giap-1"] == r["giap-2"] == pytest.approx(1.5 / 14)
    assert r["giap-0"] == 0.0


def test_an_open_week_and_the_regime_break_week_are_never_ranked(sb):
    week(sb, "giap-", start=date(2026, 9, 28))                     # tuần lẫn cú sốc 30/09 + 01/10
    week(sb, "tru-", start=MON)
    b = board(sb, "FS", frontier=date(2026, 10, 19))   # CN 18/10 + 2 = 20/10
    assert b.ranked == []
    assert {w.start for w in b.weeks if not w.ranked} == {date(2026, 9, 28), MON}


def test_longest_prefix_wins_so_cl_hoso_is_not_s_tier(sb):
    put(sb, "cl-hoso-tamhoang", MON, 500, code="CL")
    put(sb, "cl-hs-alcatraz", MON, 900, code="CL")
    week(sb, "cl-dieu-", n=15, code="CL")
    lines = {v.slug: v.line for v in board(sb, "CL", frontier=date(2026, 11, 18)).ranked}
    assert (lines["cl-hoso-tamhoang"], lines["cl-hs-alcatraz"]) == ("cl-hoso-", "cl-hs-")


def test_slot_suggestion_needs_rotation_data_from_two_full_weeks_and_a_real_gap(sb):
    # giap ở 19:00 luôn top, ở 11:30 luôn đáy; mỗi tuần có đủ 15+ video để xếp hạng.
    for wk in (MON, MON + timedelta(days=7)):
        for i in range(5):
            put(sb, f"giap-hi-{wk:%d}-{i}", wk + timedelta(days=i), 5000 + i, slot="19:00", views=4000)
            put(sb, f"giap-lo-{wk:%d}-{i}", wk + timedelta(days=i), 10 + i, slot="11:30", views=300)
        week(sb, "tru-", n=10, start=wk, slot="15:00")
    b = board(sb, "FS", frontier=RECENT_FRONTIER)
    [s] = [s for s in b.suggestions if s.line == "giap-"]
    assert (s.best_slot, s.worst_slot) == ("19:00", "11:30")
    assert (s.best_views, s.worst_views) == (4000, 300)            # view thô in kèm


def test_no_suggestion_from_a_single_week_or_a_small_pool(sb):
    for i in range(5):
        put(sb, f"giap-hi-{i}", MON + timedelta(days=i), 5000 + i, slot="19:00")
        put(sb, f"giap-lo-{i}", MON + timedelta(days=i), 10 + i, slot="11:30")
    b = board(sb, "FS", frontier=RECENT_FRONTIER)  # một tuần, pool 10 < 15
    assert b.suggestions == []


def test_no_suggestion_when_the_gap_is_small(sb):
    for wk in (MON, MON + timedelta(days=7)):
        for i in range(8):
            put(sb, f"giap-a-{wk:%d}-{i}", wk + timedelta(days=i % 7), 100 + 2 * i, slot="19:00")
            put(sb, f"giap-b-{wk:%d}-{i}", wk + timedelta(days=i % 7), 101 + 2 * i, slot="11:30")
    b = board(sb, "FS", frontier=RECENT_FRONTIER)
    assert b.suggestions == []


def test_a_channel_that_does_not_rotate_says_the_slot_effect_is_not_identified(sb):
    for wk in (MON, MON + timedelta(days=7)):
        week(sb, "cl-dieu-", n=15, start=wk, code="CL", slot="11:30")
    b = board(sb, "CL", frontier=date(2026, 11, 18))
    assert b.suggestions == [] and "chưa tách" in b.slot_note


def test_rejected_engaged_views_rows_are_shown_but_not_ranked(sb):
    week(sb, "giap-", n=15)
    sb.execute("UPDATE video_metrics SET engaged_views = NULL WHERE slug = 'giap-1012-0'")
    b = board(sb, "FS", frontier=date(2026, 11, 18))
    assert "giap-1012-0" not in {v.slug for v in b.ranked}
    assert b.unranked >= 1


# ── brief cho pha sinh trong chat ──────────────────────────────────────────

from factory.bundle import Bundle  # noqa: E402
from factory.scoreboard import render_brief  # noqa: E402


def bundle(tmp, slug, angle, title, first, code="FS"):
    b = Bundle(channel=code, kind="short", slug=slug, script=f"{first} " + "Câu tiếp theo đủ dài cho short. " * 6,
               title=title, description="d", tags=["x"], thumbnail_text="", publish_at="2026-10-13T04:30:00Z",
               voice="Anh Khôi", bgm="", broll_queries=["x"],
               source_note=f"pillar=giap;key=k-{slug};angle={angle} | nguồn")
    store.save_bundle(b, base=tmp / "bundles")


def test_brief_shows_top_and_bottom_with_title_first_sentence_and_topic(sb, tmp_path, monkeypatch):
    monkeypatch.setattr(store, "BUNDLE_DIR", tmp_path / "bundles")
    for i in range(15):
        slug = f"giap-v{i}"
        bundle(tmp_path, slug, "lục xung" if i >= 8 else "tam hợp", f"Tiêu đề {i}", f"Câu mở đầu số {i}?")
        put(sb, slug, MON + timedelta(days=i % 7), 100 * (i + 1))
    b = board(sb, "FS", frontier=date(2026, 10, 24))

    md = render_brief(b)

    assert "Tiêu đề 14" in md and "Câu mở đầu số 14?" in md and "k-giap-v14" in md     # cao nhất
    assert "Tiêu đề 0" in md and "Câu mở đầu số 0?" in md                              # thấp nhất
    angles = md.split("## Góc")[1]
    assert angles.index("lục xung") < angles.index("tam hợp")   # lục xung (i ≥ 8) xếp trên


def test_brief_for_a_non_rotating_channel_says_the_slot_effect_is_not_identified(sb):
    week(sb, "cl-dieu-", n=15, code="CL")
    md = render_brief(board(sb, "CL", frontier=date(2026, 11, 18)))
    assert "chưa tách được hiệu ứng giờ" in md


# ── hồi quy từ review (Grok vòng 3 + review hai trục) ─────────────────────

def test_pacific_date_flips_exactly_at_0900_utc_on_1_november():
    assert pacific_date(utc("2026-11-01T08:59:00Z")) == date(2026, 11, 1)    # 01:59 PDT
    assert pacific_date(utc("2026-11-01T09:00:00Z")) == date(2026, 11, 1)    # 01:00 PST
    assert pacific_date(utc("2026-11-02T07:59:00Z")) == date(2026, 11, 1)    # 23:59 PST


def test_window_is_seven_pacific_days_so_the_go_live_hour_barely_changes_its_length(db):
    # Review: 3 ngày PT = 51 giờ nếu lên sóng 20:30 PT, 71 giờ nếu 00:30 PT -> thí nghiệm giờ
    # đo nhầm độ dài cửa sổ. 7 ngày: 147-167 giờ, lệch ~7%.
    yt = FakeAnalytics(frontier=date(2026, 10, 19))
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-07T04:30:00Z")
    yt.add_views("v1", date(2026, 10, 12), 10, engaged=10)         # ngày thứ 7: trong cửa sổ
    yt.add_views("v1", date(2026, 10, 13), 999, engaged=999)       # ngày thứ 8: ngoài
    collect(db, "FS", yt, now=NOW)
    [q] = [q for q in yt.queries if q["dimensions"] == "video"]
    assert (q["start"], q["end"]) == (date(2026, 10, 6), date(2026, 10, 12))
    assert metrics(db)["giap-a"]["views"] == 10


def test_id_filtered_cohort_queries_never_depend_on_a_sort_the_report_may_reject(db):
    yt = FakeAnalytics(frontier=date(2026, 10, 19))
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-07T04:30:00Z")
    yt.add_views("v1", date(2026, 10, 6), 100, engaged=90)
    collect(db, "FS", yt, now=NOW)
    assert metrics(db)["giap-a"]["engaged_views"] == 90


def test_a_cohort_whose_views_only_retry_also_fails_is_left_for_the_next_run(db):
    # Lỗi không phải do engagedViews: không ghi NULL vĩnh viễn, không làm hỏng nhóm khác.
    yt = FakeAnalytics(frontier=date(2026, 10, 19), reject_dimensions={"video"})
    published(db, "giap-a", "v1")
    yt.add_video("v1", published_at="2026-10-07T04:30:00Z")
    out = collect(db, "FS", yt, now=NOW)
    assert metrics(db) == {} and out["failed"] == 1


def test_a_brief_rebuilt_without_collecting_still_knows_how_far_analytics_had_data(sb):
    yt = FakeAnalytics(frontier=date(2026, 11, 18))
    collect(sb, "FS", yt, now=CLOSED)                               # ghi lại frontier
    week(sb, "giap-", n=15)
    b = board(sb, "FS", frontier=None)                  # --no-collect
    assert len(b.ranked) == 15


def test_weeks_with_fewer_than_15_videos_of_a_kind_are_never_ranked(sb):
    # Một video dài trong tuần có hạng 0 hoặc 1: không được lên đầu brief của Shorts.
    week(sb, "giap-", n=15)
    sb.execute("INSERT INTO video_metrics (channel, slug, video_id, kind, go_live, pacific_date, slot_vn, "
               "views, engaged_views, collected_at) VALUES ('FS', 'long-kowloon', 'L1', 'long', 'x', "
               "'2026-10-13', '20:00', 50000, 40000, 'x')")
    b = board(sb, "FS", frontier=date(2026, 11, 18))
    assert "long-kowloon" not in {r.slug for r in b.ranked}
    assert all(r.kind == "short" for r in b.ranked)


def test_suggestions_stay_silent_with_four_per_cell(sb):
    for wk in (MON, MON + timedelta(days=7)):
        n_lo = 2                                                   # 2 + 2 = 4 < 5 ở 11:30
        for i in range(5):
            put(sb, f"giap-hi-{wk:%d}-{i}", wk + timedelta(days=i), 5000 + i, slot="19:00")
        for i in range(n_lo):
            put(sb, f"giap-lo-{wk:%d}-{i}", wk + timedelta(days=i), 10 + i, slot="11:30")
        week(sb, "tru-", n=10, start=wk, slot="15:00")
    b = board(sb, "FS", frontier=RECENT_FRONTIER)
    assert [s for s in b.suggestions if s.line == "giap-"] == []


def test_suggestions_stay_silent_when_a_cell_comes_from_one_week(sb):
    for i in range(5):
        put(sb, f"giap-hi-{i}", MON + timedelta(days=i), 5000 + i, slot="19:00")
        put(sb, f"giap-lo-{i}", MON + timedelta(days=7 + i), 10 + i, slot="11:30")
    for wk in (MON, MON + timedelta(days=7)):
        week(sb, "tru-", n=12, start=wk, slot="15:00")
    b = board(sb, "FS", frontier=RECENT_FRONTIER)
    assert [s for s in b.suggestions if s.line == "giap-"] == []


def test_suggestions_only_use_the_last_28_days(sb):
    for wk in (MON, MON + timedelta(days=7)):
        for i in range(5):
            put(sb, f"giap-hi-{wk:%d}-{i}", wk + timedelta(days=i), 5000 + i, slot="19:00")
            put(sb, f"giap-lo-{wk:%d}-{i}", wk + timedelta(days=i), 10 + i, slot="11:30")
        week(sb, "tru-", n=10, start=wk, slot="15:00")
    b = board(sb, "FS", frontier=date(2026, 12, 18))
    assert b.suggestions == []


def test_top_and_bottom_never_list_the_same_video(sb):
    week(sb, "giap-", n=15)
    md = render_brief(board(sb, "FS", frontier=date(2026, 10, 24)))
    top = md.split("## Cao nhất")[1].split("##")[0]
    bottom = md.split("## Thấp nhất")[1].split("##")[0]
    assert not ({ln for ln in top.splitlines() if ln.startswith("- ")}
                & {ln for ln in bottom.splitlines() if ln.startswith("- ")})


def test_suggestions_count_the_last_four_closed_weeks_not_28_calendar_days(sb):
    # Grok vòng 4: một tuần chỉ đóng sau 12 ngày, nên "28 ngày lịch" chỉ còn ~16 ngày dùng được
    # -> mỗi ô giờ ~4 video < 5 -> gợi ý không bao giờ xuất hiện.
    for wk in (MON, MON + timedelta(days=7)):
        for i in range(5):
            put(sb, f"giap-hi-{wk:%d}-{i}", wk + timedelta(days=i), 5000 + i, slot="19:00", views=4000)
            put(sb, f"giap-lo-{wk:%d}-{i}", wk + timedelta(days=i), 10 + i, slot="11:30", views=300)
        week(sb, "tru-", n=10, start=wk, slot="15:00")
    b = board(sb, "FS", frontier=date(2026, 11, 1))
    assert [s.line for s in b.suggestions] == ["giap-"]


def test_a_failing_cohort_for_any_api_reason_does_not_stop_the_others(db):
    from factory.youtube_api import RateLimited

    class Flaky(FakeAnalytics):
        def report(self, **kw):
            if kw["dimensions"] == "video" and kw["start"] == date(2026, 10, 6):
                raise RateLimited("429 rateLimitExceeded kéo dài")
            return super().report(**kw)

    yt = Flaky(frontier=date(2026, 10, 19))
    for slug, vid, live in (("giap-a", "v1", "2026-10-07T04:30:00Z"), ("giap-b", "v2", "2026-10-08T04:30:00Z")):
        published(db, slug, vid)
        yt.add_video(vid, published_at=live)
    out = collect(db, "FS", yt, now=NOW)
    assert set(metrics(db)) == {"giap-b"} and out["failed"] == 1
