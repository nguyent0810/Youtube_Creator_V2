"""--wait cho upload (retro 2 mục 10, 15): ngủ tới Channel.next_upload_at rồi đăng, không ném PacingHold, không để chuỗi
tự đoán "thử lại 30 × 5 phút" (D1 07/10: lượt mở sau 4,2 h, vòng thử hết sau 2,5 h).

Đồng hồ giả CHẠY khi ngủ (luật retro 1 mục 5: test thời gian phải có ca đồng hồ chạy).
"""
import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from factory import publish, store
from factory.bundle import Bundle
from factory.channel import Channel, Pacing, Upload, upload_when_free, wait_turn
from factory.youtube_fake import FakeYouTube

ROOT = Path(__file__).resolve().parent.parent
T0 = datetime(2026, 10, 7, 9, 0, tzinfo=timezone.utc)


class Clock:
    def __init__(self):
        self.t, self.slept = T0, []

    def now(self):
        return self.t

    def sleep(self, s):
        self.slept.append(s)
        self.t += timedelta(seconds=s)


@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "DB_PATH", tmp_path / "state.sqlite")
    monkeypatch.setattr(store, "BUNDLE_DIR", tmp_path / "bundles")
    v = tmp_path / "v.mp4"
    v.write_bytes(b"\0")
    return v


def up(video, slug):
    return Upload(slug=slug, video=video, title=f"Tiêu đề {slug}", description="d", tags=("t",), kind="long",
                  publish_at="2026-10-31T13:00:00Z", category="27")


def test_wait_turn_sleeps_until_next_upload_at_and_prints_target(db):
    clk, said = Clock(), []
    with store.connect() as conn:
        ch = Channel("CK", FakeYouTube(), conn, now=clk.now, pacing=Pacing(timedelta(hours=4, minutes=12), 6))
        ch.upload(up(db, "long-a"))
        target = ch.next_upload_at(clk.now())
        assert target == T0 + timedelta(hours=4, minutes=12)
        wait_turn(ch, sleep=clk.sleep, say=said.append)
        assert clk.now() >= target and clk.now() - target < timedelta(seconds=30)
        assert len(clk.slept) == 1 and "2026-10-07T13:12:00Z" in said[0] and "20:12" in said[0]   # giờ VN


def test_wait_turn_returns_at_once_when_free(db):
    clk = Clock()
    with store.connect() as conn:
        wait_turn(Channel("CK", FakeYouTube(), conn, now=clk.now), sleep=clk.sleep, say=lambda m: None)
    assert clk.slept == []


def test_upload_when_free_never_raises_pacing_hold(db):
    clk = Clock()
    yt = FakeYouTube()
    with store.connect() as conn:
        ch = Channel("CK", yt, conn, now=clk.now, pacing=Pacing(timedelta(hours=1), 6))
        ch.upload(up(db, "long-a"))
        res = upload_when_free(ch, up(db, "long-b"), sleep=clk.sleep, say=lambda m: None)
    assert res.video_id and yt.inserts == 2 and sum(clk.slept) >= 3600


def test_publish_batch_run_wait_uploads_whole_lot_across_the_daily_cap(db, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["publish_batch.py", "run", "--wait"])
    spec = importlib.util.spec_from_file_location("publish_batch_wait", ROOT / "scripts" / "publish_batch.py")
    pb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pb)
    clk, yt = Clock(), FakeYouTube()
    monkeypatch.setattr(publish, "access_token", lambda creds: "tok")
    monkeypatch.setattr(publish, "uploads_playlist_id", lambda tok: "UU")
    monkeypatch.setattr(publish, "channel_titles", lambda u, tok: {})
    monkeypatch.setattr(pb, "_creds", lambda: {})
    monkeypatch.setattr(pb, "_foreign_days", lambda tok, conn: set())
    monkeypatch.setattr(pb.time, "sleep", clk.sleep)      # wait_turn ngủ bằng time.sleep -> đồng hồ giả chạy
    monkeypatch.setattr(pb.Channel, "open", classmethod(
        lambda cls, code, conn, channel_titles=None: Channel(code, yt, conn, now=clk.now, channel_titles=channel_titles)))
    with store.connect() as conn:
        for i in range(26):
            b = Bundle(channel="FS", kind="short", slug=f"lich-202611{i:02d}", script="Câu kể đủ dài cho một short phong thủy. " * 6,
                       title=f"Ngày {i} tháng 11", description="d", tags=["phong thuy"], thumbnail_text="",
                       publish_at=f"2026-11-{i + 1:02d}T23:00:00Z", voice="Phạm Tuyên", bgm="", broll_queries=["silver"])
            store.save_bundle(b)
            store.enqueue(b, conn)
            store.mark(conn, b.id, "assembled", video_path=str(db))
    pb.do_run(500)
    with store.connect() as conn:
        stages = [r["stage"] for r in conn.execute("SELECT stage FROM item")]
    assert stages.count("published") == 26 and yt.inserts == 26      # không hoãn: chờ qua mốc 24 h rồi đăng tiếp
    assert any(s >= 23 * 3600 for s in clk.slept)


def test_publish_long_has_wait_flag():
    src = (ROOT / "motion" / "long" / "publish_long.py").read_text(encoding="utf-8")
    assert '"--wait" in rest' in src and "upload_when_free(chan, u) if wait" in src
