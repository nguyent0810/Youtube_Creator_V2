"""Lệnh chạy hằng tuần: thu -> bảng điểm -> brief. Mạng là FakeAnalytics."""
import importlib.util
from datetime import date, datetime, timezone
from pathlib import Path

from factory import scoreboard, store
from factory.analytics_fake import FakeAnalytics
from factory.channel import Channel

ROOT = Path(__file__).resolve().parent.parent


def test_weekly_run_collects_and_writes_the_channel_brief(tmp_path):
    spec = importlib.util.spec_from_file_location("feedback_loop", ROOT / "scripts" / "feedback_loop.py")
    fl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fl)
    api = FakeAnalytics(frontier=date(2026, 10, 19))
    api.add_video("v1", published_at="2026-10-07T04:30:00Z")
    api.add_views("v1", date(2026, 10, 6), 120, engaged=100)
    with store.connect(tmp_path / "state.sqlite") as conn:
        Channel("FS", None, conn)
        conn.execute("INSERT INTO upload_log (channel, slug, title, state, video_id, started_at) "
                     "VALUES ('FS', 'giap-a', 'A', 'done', 'v1', '2026-10-01T00:00:00Z')")

        path, summary = fl.run("FS", conn, api, now=datetime(2026, 10, 20, 3, tzinfo=timezone.utc),
                               out_dir=tmp_path / "briefs")

    assert summary["stored"] == 1
    assert path == tmp_path / "briefs" / "FS.md" and "# Bảng điểm kênh FS" in path.read_text(encoding="utf-8")


def test_no_collect_still_writes_the_demand_sections(tmp_path):
    spec = importlib.util.spec_from_file_location("feedback_loop", ROOT / "scripts" / "feedback_loop.py")
    fl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fl)
    from tests.test_demand import FakeWiki
    api = FakeAnalytics(frontier=date(2026, 10, 2))
    api.search_terms = [("ai là gì", 9)]
    (tmp_path / "demand").mkdir()
    (tmp_path / "demand" / "MIM.json").write_text('{"topics": [{"topic": "ChatGPT", "articles": ["ChatGPT"]}]}',
                                                   encoding="utf-8")
    wiki = FakeWiki()
    wiki.set("ChatGPT", date(2026, 9, 1), date(2026, 10, 4), 120)
    with store.connect(tmp_path / "state.sqlite") as conn:
        scoreboard.prepare(conn, "MIM")                 # mốc Analytics đã có từ lần đo trước
        conn.execute("INSERT INTO metrics_meta (channel, frontier) VALUES ('MIM', '2026-10-02')")

        path, _ = fl.run("MIM", conn, api, now=datetime(2026, 10, 5, 3, tzinfo=timezone.utc),
                         out_dir=tmp_path / "briefs", collect=False, wiki=wiki,
                         demand_dir=tmp_path / "demand", sleep=lambda s: None)

    md = path.read_text(encoding="utf-8")
    assert "ai là gì" in md and "ChatGPT" in md and "120" in md
