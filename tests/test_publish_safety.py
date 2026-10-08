"""Khoá các chốt an toàn của đường đăng (audit 08/10/2026).

Mỗi test dựng lại một cách hỏng có thật hoặc có đường dẫn thật trong mã:
  - publishAt quá khứ -> YouTube công khai NGAY;
  - chống trùng theo tiêu đề nhận nhầm video của người khác;
  - "resumable" không resume;
  - rate limit bị coi là hết quota ngày;
  - set_schedule xoá trường không gửi lại.
Không test nào gọi mạng: mọi lời gọi API đều bị thay bằng bản giả.
"""
import json
from datetime import datetime, timedelta, timezone

import pytest

from factory import publish
from factory.bundle import Bundle


def _future(hours=48) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _bundle(**over) -> Bundle:
    base = dict(
        channel="FS", kind="short", slug="giap-test-an-toan",
        script=" ".join(["chữ"] * 60), title="Tiêu đề thử an toàn", description="Mô tả.",
        tags=["phong thuy"], thumbnail_text="", publish_at=_future(), voice="Anh Khôi",
        bgm="asian_drums.mp3", broll_queries=["x"])
    base.update(over)
    return Bundle(**base)


@pytest.fixture
def no_network(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("không được gọi mạng")
    monkeypatch.setattr(publish.urllib.request, "urlopen", boom)


# ─── Giờ hẹn ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("delta", [timedelta(days=-1), timedelta(minutes=-1), timedelta(minutes=10)])
def test_past_or_too_close_publish_at_is_refused(delta):
    when = (datetime.now(timezone.utc) + delta).strftime("%Y-%m-%dT%H:%M:%SZ")
    with pytest.raises(publish.PublishAtPassed):
        publish.check_publish_at(when)


def test_upload_with_past_publish_at_never_touches_the_network(no_network, tmp_path):
    video = tmp_path / "v.mp4"
    video.write_bytes(b"0" * 10)
    with pytest.raises(publish.PublishAtPassed):
        publish.upload_video(_bundle(publish_at="2020-01-01T00:00:00Z"), video, "tok")
    with pytest.raises(publish.PublishAtPassed):
        publish.publish_bundle(_bundle(publish_at="2020-01-01T00:00:00Z"), video, {}, token="tok",
                               known_titles={})


def test_probe_metadata_has_no_publish_at_and_never_goes_public():
    meta = publish.video_meta(_bundle(publish_at="2020-01-01T00:00:00Z"), schedule=False)
    assert meta["status"]["privacyStatus"] == "private" and "publishAt" not in meta["status"]


def test_metadata_carries_marker_credit_and_shorts_tag():
    b = _bundle()
    meta = publish.video_meta(b)
    assert meta["status"] == {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                              "publishAt": b.publish_at}
    assert f"yf{b.id}" in meta["snippet"]["tags"]
    desc = meta["snippet"]["description"]
    assert "Asian Drums" in desc and "Kevin MacLeod" in desc and "creativecommons.org/licenses/by/4.0" in desc
    assert desc.rstrip().endswith("#Shorts")


# ─── Chống trùng: không nhận video người khác ─────────────────────────────

def _fake_status(monkeypatch, tags, status):
    calls = {"schedule": []}
    monkeypatch.setattr(publish, "video_status", lambda vid, tok: {"snippet": {"tags": tags}, "status": status})
    monkeypatch.setattr(publish, "set_schedule", lambda vid, when, tok: calls["schedule"].append((vid, when)))
    monkeypatch.setattr(publish, "upload_video", lambda *a, **k: (_ for _ in ()).throw(AssertionError("upload")))
    return calls


def test_same_title_from_someone_else_is_not_adopted(monkeypatch, tmp_path):
    """Lỗi thật đang chờ: 'Vì sao tượng Phật có dái tai dài?' của nguồn khác trên kênh BUD."""
    b = _bundle()
    _fake_status(monkeypatch, ["phat giao"], {"privacyStatus": "public"})
    with pytest.raises(publish.DuplicateTitle) as e:
        publish.publish_bundle(b, tmp_path / "v.mp4", {}, token="tok", known_titles={b.title: "OTHER"})
    assert e.value.video_id == "OTHER"


def test_own_probe_upload_is_adopted_and_scheduled(monkeypatch, tmp_path):
    b = _bundle()
    calls = _fake_status(monkeypatch, ["phong thuy", f"yf{b.id}"], {"privacyStatus": "private"})
    res = publish.publish_bundle(b, tmp_path / "v.mp4", {}, token="tok", known_titles={b.title: "MINE"})
    assert res.adopted and res.video_id == "MINE" and calls["schedule"] == [("MINE", b.publish_at)]


def test_own_scheduled_upload_is_adopted_without_rescheduling(monkeypatch, tmp_path):
    b = _bundle()
    calls = _fake_status(monkeypatch, [f"yf{b.id}"], {"privacyStatus": "private", "publishAt": b.publish_at})
    res = publish.publish_bundle(b, tmp_path / "v.mp4", {}, token="tok", known_titles={b.title: "MINE"})
    assert res.adopted and calls["schedule"] == [] and res.scheduled_at == b.publish_at


def test_errors_after_upload_do_not_lose_the_video_id(monkeypatch, tmp_path):
    b = _bundle()
    thumb = tmp_path / "t.jpg"
    thumb.write_bytes(b"x")
    monkeypatch.setattr(publish, "upload_video", lambda *a, **k: "NEWVID")
    monkeypatch.setattr(publish, "set_thumbnail", lambda *a: (_ for _ in ()).throw(publish.PublishError("403")))
    res = publish.publish_bundle(b, tmp_path / "v.mp4", {}, thumb_path=thumb, token="tok", known_titles={})
    assert res.video_id == "NEWVID" and res.warnings


# ─── Phân loại lỗi ────────────────────────────────────────────────────────

@pytest.mark.parametrize("body", ['{"reason": "rateLimitExceeded"}', '{"reason": "userRateLimitExceeded"}'])
def test_rate_limit_is_not_daily_quota(body):
    with pytest.raises(publish.RateLimited) as e:
        publish._raise("x", 403, body)
    assert not isinstance(e.value, publish.QuotaExceeded)


# ─── Resumable upload thật sự resume ──────────────────────────────────────

def _script_put(monkeypatch, responses):
    """Thay _put bằng kịch bản phản hồi; ghi lại Content-Range đã gửi."""
    sent = []

    def fake(url, data, content_range):
        sent.append(content_range)
        r = responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    monkeypatch.setattr(publish, "_put", fake)
    return sent


def test_upload_resumes_from_the_byte_the_server_confirmed(monkeypatch, tmp_path):
    monkeypatch.setattr(publish, "CHUNK", 4)
    f = tmp_path / "v.mp4"
    f.write_bytes(b"0123456789")
    sent = _script_put(monkeypatch, [
        ("next", 4),                         # chunk 1 nhận đủ
        publish._Transient("mạng đứt"),      # chunk 2 đứt giữa chừng
        ("next", 6),                         # hỏi lại: server mới giữ tới byte 5
        ("next", 10),                        # gửi tiếp TỪ byte 6, không phải từ 0 hay 8
        ("done", "VID"),                     # hỏi lại khi đủ byte -> có id
    ])
    assert publish._send_file("u", f, 10, sleep=lambda s: None) == "VID"
    assert sent == ["bytes 0-3/10", "bytes 4-7/10", "bytes */10", "bytes 6-9/10", "bytes */10"]


def test_upload_gives_up_when_nothing_progresses(monkeypatch, tmp_path):
    f = tmp_path / "v.mp4"
    f.write_bytes(b"0123456789")
    _script_put(monkeypatch, [publish._Transient("đứt"), ("next", 0)] * 20)
    with pytest.raises(publish.PublishError):
        publish._send_file("u", f, 10, retries=3, sleep=lambda s: None)


# ─── set_schedule giữ nguyên mọi trường ───────────────────────────────────

def test_set_schedule_keeps_every_field(monkeypatch):
    sent = {}
    current = {"snippet": {"title": "T", "description": "D", "tags": ["a"], "categoryId": "27",
                           "defaultLanguage": "vi", "defaultAudioLanguage": "vi"},
               "status": {"privacyStatus": "private", "embeddable": False, "license": "creativeCommon",
                          "publicStatsViewable": False, "selfDeclaredMadeForKids": False}}
    monkeypatch.setattr(publish, "video_status", lambda vid, tok: json.loads(json.dumps(current)))
    monkeypatch.setattr(publish, "_api", lambda tok, method, path, params=None, payload=None: sent.update(payload))
    when = _future()
    publish.set_schedule("VID", when, "tok")
    assert sent["snippet"] == current["snippet"]
    assert sent["status"]["publishAt"] == when and sent["status"]["embeddable"] is False
    assert sent["status"]["license"] == "creativeCommon"


def test_set_schedule_refuses_past_time(no_network):
    with pytest.raises(publish.PublishAtPassed):
        publish.set_schedule("VID", "2020-01-01T00:00:00Z", "tok")
