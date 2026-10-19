"""publish_batch run: phản ứng với lỗi của Channel đúng loại -- HOÃN thì không tính hỏng.

Mạng thay bằng FakeYouTube; store là SQLite tạm.
"""
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

import pytest

from factory import publish, store
from factory.bundle import Bundle
from factory.channel import Channel
from factory.youtube_fake import FakeYouTube

ROOT = Path(__file__).resolve().parent.parent
T0 = datetime(2026, 10, 5, 3, 0, tzinfo=timezone.utc)


@pytest.fixture
def batch(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "DB_PATH", tmp_path / "state.sqlite")
    monkeypatch.setattr(store, "BUNDLE_DIR", tmp_path / "bundles")
    spec = importlib.util.spec_from_file_location("publish_batch", ROOT / "scripts" / "publish_batch.py")
    pb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pb)

    yt = FakeYouTube()
    monkeypatch.setattr(publish, "access_token", lambda creds: "tok")
    monkeypatch.setattr(publish, "uploads_playlist_id", lambda tok: "UU")
    monkeypatch.setattr(pb, "_creds", lambda: {})
    monkeypatch.setattr(pb, "_foreign_days", lambda tok, conn: set())
    monkeypatch.setattr(pb.time, "sleep", lambda s: None)
    titles: dict[str, str] = {}
    monkeypatch.setattr(publish, "channel_titles", lambda up, tok: dict(titles))
    monkeypatch.setattr(pb.Channel, "open", classmethod(
        lambda cls, code, conn, channel_titles=None: Channel(code, yt, conn, now=lambda: T0,
                                                             channel_titles=channel_titles)))

    video = tmp_path / "v.mp4"
    video.write_bytes(b"\0")

    def assembled(n):
        with store.connect() as conn:
            for i in range(n):
                b = Bundle(channel="FS", kind="short", slug=f"lich-202611{i:02d}",
                           script="Câu kể đủ dài cho một short phong thủy. " * 6,
                           title=f"Ngày {i} tháng 11", description="d", tags=["phong thuy"],
                           thumbnail_text="", publish_at=f"2026-11-{i + 1:02d}T23:00:00Z",
                           voice="Phạm Tuyên", bgm="", broll_queries=["silver"])
                store.save_bundle(b)
                store.enqueue(b, conn)
                store.mark(conn, b.id, "assembled", video_path=str(video))

    return pb, yt, titles, assembled


def _rows():
    with store.connect() as conn:
        return {r["slug"]: dict(r) for r in conn.execute("SELECT * FROM item")}


def test_hitting_the_daily_pacing_cap_defers_the_rest_without_counting_a_failure(batch):
    pb, yt, _, assembled = batch
    assembled(26)

    pb.do_run(500)

    rows = _rows()
    published = [r for r in rows.values() if r["stage"] == "published"]
    held = [r for r in rows.values() if r["stage"] == "assembled"]
    assert len(published) == 24 and yt.inserts == 24
    assert len(held) == 2
    assert all(r["attempts"] == 0 and r["retry_after"] == "2026-10-06T03:00:00Z" for r in held)


def test_a_title_already_on_the_channel_is_rejected_never_recorded_as_published(batch):
    # Trước đây: ghi video_id của video kia vào item -> "đã đăng" mà thật ra chưa (9 ngày Lịch).
    pb, yt, titles, assembled = batch
    assembled(2)
    titles["Ngày 1 tháng 11"] = "vidSOMEONE_ELSE"

    pb.do_run(500)

    rows = _rows()
    assert rows["lich-20261101"]["stage"] == "failed"
    assert rows["lich-20261101"]["video_id"] is None
    assert rows["lich-20261101"]["attempts"] == 99
    assert rows["lich-20261100"]["stage"] == "published"


def test_an_interrupted_upload_is_deferred_and_the_batch_stops_without_counting_a_failure(batch):
    from factory.youtube_api import UploadInterrupted
    pb, yt, _, assembled = batch
    assembled(3)
    yt.fail_next_insert(UploadInterrupted("mất mạng ở chunk cuối"), completed=True)

    pb.do_run(500)

    rows = _rows()
    first = rows["lich-20261100"]
    assert first["stage"] == "assembled" and first["attempts"] == 0 and first["retry_after"]
    assert rows["lich-20261101"]["stage"] == "assembled"      # lô dừng, item sau không bị đụng
    assert yt.inserts == 1                                   # video đã có trên YouTube, chưa ghi nhầm


def test_an_upload_in_doubt_waits_for_a_human_and_is_never_counted_as_failed(batch):
    from factory.youtube_api import UploadInterrupted
    pb, yt, _, assembled = batch
    assembled(1)
    yt.fail_next_insert(UploadInterrupted("mất mạng"), completed=False)
    pb.do_run(500)
    yt.expire_session(list(yt.sessions)[-1])
    with store.connect() as conn:
        conn.execute("UPDATE item SET retry_after = NULL")   # tới giờ thử lại

    pb.do_run(500)

    row = _rows()["lich-20261100"]
    assert row["stage"] == "assembled" and row["attempts"] == 0
    assert row["error"].startswith("UploadInDoubt")
    assert yt.inserts == 0
