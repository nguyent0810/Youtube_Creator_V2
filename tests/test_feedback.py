"""Sổ giữ chân: số 7 ngày đầu ghi một lần, so với video trước, record() không xóa."""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion"))
import variety as V


def _row(topic, day, **kw):
    row = {"topic": topic, "channel": "CL", "theme": "", "look": "classic", "bgm": ["a"], "date": day}
    row.update(kw)
    return row


def test_window_and_ready_gate():
    pub = datetime(2026, 9, 30, 14, 0, tzinfo=timezone.utc)
    assert V.feedback_window(pub) == ("2026-09-29", "2026-10-07")
    assert not V.feedback_ready(pub, datetime(2026, 10, 9, 13, 59, tzinfo=timezone.utc))
    assert V.feedback_ready(pub, datetime(2026, 10, 9, 14, 0, tzinfo=timezone.utc))


def test_minute_retention_picks_nearest_ratio():
    dur = 1800
    curve = [
        {"elapsedVideoTimeRatio": 0.0, "audienceWatchRatio": 1},
        {"elapsedVideoTimeRatio": 60 / dur, "audienceWatchRatio": 0.64},
        {"elapsedVideoTimeRatio": 0.5, "audienceWatchRatio": 0.2},
    ]
    assert V.minute_retention(curve, dur, 60) == 64.0
    assert V.minute_retention([], dur, 60) is None
    assert V.minute_retention(curve, 0, 60) is None


def test_suggested_share():
    src = [
        {"insightTrafficSourceType": "RELATED_VIDEO", "views": 89},
        {"insightTrafficSourceType": "YT_SEARCH", "views": 11},
    ]
    assert V.suggested_share(src) == 89.0
    assert V.suggested_share([{"insightTrafficSourceType": "YT_SEARCH", "views": 10}]) == 0.0
    assert V.suggested_share([]) is None
    assert V.suggested_share(None) is None
    assert V.suggested_share([{"insightTrafficSourceType": "RELATED_VIDEO", "views": 0}]) is None


def test_stamp_once_keeps_look_and_compares_previous_same_channel():
    rows = [
        _row("yakuza", "2026-09-30", ret1=64.0, suggested=89.0),
        _row("other", "2026-09-29", channel="XX", ret1=10.0, suggested=10.0),
        _row("mafia", "2026-10-01", bgm=["b", "c"]),
    ]
    out, stamped = V.stamp_feedback(rows, "mafia", ret1=50.0, suggested=12.0, age_days=10.2, today="2026-10-11")
    assert stamped["look"] == "classic"
    assert stamped["bgm"] == ["b", "c"]
    assert stamped["date"] == "2026-10-01"
    assert stamped["ret1_vs_prev"] == -14.0
    assert stamped["suggested_vs_prev"] == -77.0
    assert stamped["feedback_on"] == "2026-10-11"
    again, second = V.stamp_feedback(out, "mafia", ret1=1, suggested=1, age_days=99, today="2026-10-20")
    assert second is None
    assert again[2]["ret1"] == 50.0


def test_first_video_has_no_delta_and_missing_topic_is_untouched():
    rows = [_row("yakuza", "2026-09-30")]
    out, stamped = V.stamp_feedback(rows, "yakuza", ret1=64.0, suggested=89.0, age_days=11, today="2026-10-11")
    assert "ret1_vs_prev" not in stamped
    assert "suggested_vs_prev" not in stamped
    same, missing = V.stamp_feedback(out, "khong-co", ret1=1, suggested=1, age_days=9, today="2026-10-11")
    assert missing is None
    assert [r["topic"] for r in same] == ["yakuza"]


def test_keep_feedback_survives_rerecord():
    old = _row("yakuza", "2026-09-30", ret1=64.0, suggested=89.0, ret1_vs_prev=None)
    # ret1_vs_prev is present even when None: keep it, because the key was stored.
    fresh = _row("yakuza", "2026-09-30", look="jade", bgm=["z"])
    kept = V.keep_feedback(fresh, old)
    assert kept["look"] == "jade"
    assert kept["bgm"] == ["z"]
    assert kept["ret1"] == 64.0
    assert kept["suggested"] == 89.0
    assert kept["ret1_vs_prev"] is None
