"""HttpYouTube: chi tiết HTTP của upload resumable, token, phân loại lỗi.

Mạng là một stub `urlopen` theo kịch bản. Chính sách (giãn nhịp, sổ, merge)
test ở test_channel.py; ở đây chỉ còn: YouTube trả gì thì adapter làm gì.
"""
import io
import json
import urllib.error

import pytest

from factory.youtube_api import (HttpYouTube, QuotaExceeded, SessionDead, UploadInDoubt,
                                 UploadInterrupted)

CREDS = {"client_id": "c", "client_secret": "s", "refresh_token": "r"}
SESSION = "https://upload.example/session/abc"


class Resp:
    def __init__(self, status=200, body=b"", headers=None):
        self.status = status
        self._body = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.headers = headers or {}
        self.length = len(self._body)

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def close(self):
        pass


def http_error(code, body="", headers=None):
    return urllib.error.HTTPError("u", code, "x", headers or {}, io.BytesIO(body.encode()))


class Net:
    """urlopen giả: mỗi lời gọi lấy phản hồi kế tiếp trong `script` và ghi lại request."""

    def __init__(self, *script):
        self.script = list(script)
        self.calls = []

    def __call__(self, req, timeout=None):
        self.calls.append((req.get_method(), req.full_url, dict(req.header_items()), req.data))
        if req.full_url.startswith("https://oauth2.googleapis.com/token"):
            return Resp(200, {"access_token": f"tok{sum(1 for c in self.calls if 'oauth2' in c[1])}"})
        nxt = self.script.pop(0)
        if isinstance(nxt, Exception):
            raise nxt
        return nxt

    def uploads(self):
        return [c for c in self.calls if "oauth2" not in c[1]]


def make(net, **kw):
    return HttpYouTube(CREDS, urlopen=net, sleep=lambda s: None, chunk=4, **kw)


@pytest.fixture
def video(tmp_path):
    p = tmp_path / "v.mp4"
    p.write_bytes(b"ABCDEFGHIJ")          # 10 byte -> chunk 4: 0-3, 4-7, 8-9
    return p


def test_resumable_upload_saves_the_session_before_the_first_byte(video):
    order = []
    net = Net(Resp(200, b"", {"Location": SESSION}),
              http_error(308, headers={"Range": "bytes=0-3"}),
              http_error(308, headers={"Range": "bytes=0-7"}),
              Resp(201, {"id": "vid1"}))
    yt = make(net)

    def on_session(uri):
        order.append(("session", uri, len(net.uploads())))

    vid = yt.insert_video({"snippet": {}, "status": {}}, video, resume_uri=None, on_session=on_session)

    assert vid == "vid1"
    assert order == [("session", SESSION, 1)]               # chỉ mới có request khởi tạo
    ranges = [c[2].get("Content-range") for c in net.uploads()[1:]]
    assert ranges == ["bytes 0-3/10", "bytes 4-7/10", "bytes 8-9/10"]


def _interrupt_last_chunk(video, failure):
    """Upload tới chunk cuối thì `failure`. Trả (yt, net, uri đã lưu)."""
    saved = []
    net = Net(Resp(200, b"", {"Location": SESSION}),
              http_error(308, headers={"Range": "bytes=0-3"}),
              http_error(308, headers={"Range": "bytes=0-7"}),
              failure)
    yt = make(net)
    with pytest.raises(UploadInterrupted):
        yt.insert_video({"snippet": {}, "status": {}}, video, resume_uri=None, on_session=saved.append)
    return yt, net, saved[0]


def test_network_drop_on_last_chunk_then_query_says_done_adopts_without_a_second_insert(video):
    # Grok test 1: mất phản hồi 201 -> hỏi phiên -> 201 -> nhận id, chỉ MỘT lần khởi tạo.
    yt, net, uri = _interrupt_last_chunk(video, urllib.error.URLError("connection reset"))
    net.script = [Resp(201, {"id": "vidDONE"})]

    vid = yt.insert_video({"snippet": {}, "status": {}}, video, resume_uri=uri, on_session=pytest.fail)

    assert vid == "vidDONE"
    assert sum(1 for c in net.uploads() if c[0] == "POST") == 1
    assert net.uploads()[-1][2]["Content-range"] == "bytes */10"


def test_503_on_last_chunk_keeps_the_session_and_resumes_from_what_youtube_has(video):
    # Grok test 2: 5xx ở chunk cuối KHÔNG phải "upload hỏng" -- có thể đã xong.
    yt, net, uri = _interrupt_last_chunk(video, http_error(503, "backend error"))
    net.script = [http_error(308, headers={"Range": "bytes=0-7"}), Resp(201, {"id": "vid9"})]

    vid = yt.insert_video({"snippet": {}, "status": {}}, video, resume_uri=uri, on_session=pytest.fail)

    assert vid == "vid9"
    assert net.uploads()[-1][2]["Content-range"] == "bytes 8-9/10"
    assert sum(1 for c in net.uploads() if c[0] == "POST") == 1


def test_429_before_the_session_is_quota_and_no_session_is_reported(video):
    # Grok test 3a: trần upload ngày (lượt 93) trả 429 ngay lúc khởi tạo.
    net = Net(http_error(429, '{"error": {"message": "Video Uploads per day"}}'))
    called = []
    with pytest.raises(QuotaExceeded):
        make(net).insert_video({"snippet": {}, "status": {}}, video, resume_uri=None,
                               on_session=called.append)
    assert called == []
    assert len(net.uploads()) == 1                     # không thử lại 429 trần ngày


def test_expired_session_404_is_in_doubt(video):
    # Grok test 3b.
    net = Net(http_error(404, "Not Found"))
    with pytest.raises(UploadInDoubt):
        make(net).insert_video({}, video, resume_uri=SESSION, on_session=pytest.fail)


def test_permanent_4xx_on_session_query_means_the_session_is_dead(video):
    net = Net(http_error(400, "Invalid upload session"))
    with pytest.raises(SessionDead):
        make(net).insert_video({}, video, resume_uri=SESSION, on_session=pytest.fail)


def test_rate_limit_is_retried_with_backoff_but_never_turned_into_quota(video):
    slept = []
    net = Net(http_error(403, '{"reason": "rateLimitExceeded"}'),
              Resp(200, {"items": [{"id": "v1", "status": {}}]}))
    yt = HttpYouTube(CREDS, urlopen=net, sleep=slept.append)

    assert yt.get_video("v1", "status")["id"] == "v1"
    assert slept == [2]


def test_expired_access_token_is_refreshed_once_on_401(video):
    net = Net(http_error(401, "Invalid Credentials"), Resp(200, {"items": []}))
    yt = make(net)

    assert yt.get_video("v1", "status") is None
    tokens = [c[2]["Authorization"] for c in net.uploads()]
    assert tokens == ["Bearer tok1", "Bearer tok2"]


def test_token_is_reused_for_40_minutes_then_refreshed():
    now = [0.0]
    net = Net(Resp(200, {"items": []}), Resp(200, {"items": []}), Resp(200, {"items": []}))
    yt = HttpYouTube(CREDS, urlopen=net, clock=lambda: now[0])

    yt.get_video("a", "status")
    now[0] = 39 * 60
    yt.get_video("b", "status")
    now[0] = 41 * 60
    yt.get_video("c", "status")

    assert [c[2]["Authorization"] for c in net.uploads()] == ["Bearer tok1", "Bearer tok1", "Bearer tok2"]


# ── hồi quy từ review ─────────────────────────────────────────────────────

def test_rate_limit_on_the_session_query_is_retried_never_called_a_dead_session(video):
    # Trước đây 403 rateLimitExceeded lúc hỏi phiên -> SessionDead -> xoá sổ -> upload lần hai.
    slept = []
    net = Net(http_error(403, '{"reason": "rateLimitExceeded"}'),
              http_error(308, headers={"Range": "bytes=0-9"}),
              Resp(201, {"id": "vidOK"}))
    yt = HttpYouTube(CREDS, urlopen=net, sleep=slept.append, chunk=4)

    assert yt.insert_video({}, video, resume_uri=SESSION, on_session=pytest.fail) == "vidOK"
    assert slept == [2]


@pytest.mark.parametrize("code, reason", [(403, "quotaExceeded"), (400, "uploadLimitExceeded")])
def test_quota_on_the_session_query_is_quota_not_a_dead_session(video, code, reason):
    net = Net(http_error(code, f'{{"reason": "{reason}"}}'))
    with pytest.raises(QuotaExceeded):
        make(net).insert_video({}, video, resume_uri=SESSION, on_session=pytest.fail)


def test_rate_limited_429_on_a_chunk_backs_off_and_resumes_instead_of_waiting_for_tomorrow(video):
    slept = []
    net = Net(Resp(200, b"", {"Location": SESSION}),
              http_error(429, '{"reason": "rateLimitExceeded"}'),
              http_error(308, headers={"Range": "bytes=0-3"}),       # hỏi lại phiên
              http_error(308, headers={"Range": "bytes=0-7"}),
              Resp(201, {"id": "vidRL"}))
    yt = HttpYouTube(CREDS, urlopen=net, sleep=slept.append, chunk=4)

    assert yt.insert_video({}, video, resume_uri=None, on_session=lambda u: None) == "vidRL"
    assert slept == [2]


def test_401_that_will_not_go_away_mid_upload_stops_instead_of_looping(video):
    net = Net(Resp(200, b"", {"Location": SESSION}),
              *[http_error(401, "Invalid Credentials") for _ in range(10)])
    with pytest.raises(UploadInterrupted):
        make(net).insert_video({}, video, resume_uri=None, on_session=lambda u: None)
    assert len(net.uploads()) <= 4


def test_308_that_never_moves_forward_stops_instead_of_looping(video):
    net = Net(Resp(200, b"", {"Location": SESSION}),
              *[http_error(308, headers={"Range": "bytes=0-3"}) for _ in range(20)])
    with pytest.raises(UploadInterrupted):
        make(net).insert_video({}, video, resume_uri=None, on_session=lambda u: None)
    assert len(net.uploads()) <= 6


def test_rate_limit_that_never_clears_is_temporary_not_an_internal_error(video):
    from factory.youtube_api import RateLimited
    net = Net(*[http_error(403, '{"reason": "rateLimitExceeded"}') for _ in range(4)])
    with pytest.raises(RateLimited):
        HttpYouTube(CREDS, urlopen=net, sleep=lambda s: None).get_video("v", "status")


def test_progress_is_reported_after_every_accepted_chunk(video):
    beats = []
    net = Net(Resp(200, b"", {"Location": SESSION}),
              http_error(308, headers={"Range": "bytes=0-3"}),
              http_error(308, headers={"Range": "bytes=0-7"}),
              Resp(201, {"id": "vid1"}))
    make(net).insert_video({}, video, resume_uri=None, on_session=lambda u: None,
                           on_progress=lambda: beats.append(1))
    assert len(beats) == 2


def test_a_dns_blip_on_a_read_is_retried_instead_of_killing_the_whole_run():
    # Lỗi thật lúc phân tích kênh MIM 05/10: getaddrinfo failed giữa chừng -> cả script chết.
    slept = []
    net = Net(urllib.error.URLError("getaddrinfo failed"), Resp(200, {"items": [{"id": "v1", "status": {}}]}))
    yt = HttpYouTube(CREDS, urlopen=net, sleep=slept.append)

    assert yt.get_video("v1", "status")["id"] == "v1"
    assert slept == [2]


def test_a_network_that_stays_down_ends_in_a_temporary_error_not_a_crash():
    from factory.youtube_api import NetworkDown
    net = Net(*[urllib.error.URLError("getaddrinfo failed") for _ in range(4)])
    with pytest.raises(NetworkDown):
        HttpYouTube(CREDS, urlopen=net, sleep=lambda s: None).get_video("v1", "status")


def test_a_dns_blip_while_fetching_the_first_token_is_retried_too():
    # Review: trong tiến trình mới, lời gọi mạng ĐẦU TIÊN là đổi token -- trước đây không được thử lại.
    calls = []

    def urlopen(req, timeout=None):
        calls.append(req.full_url)
        if "oauth2" in req.full_url and len(calls) == 1:
            raise urllib.error.URLError("getaddrinfo failed")
        if "oauth2" in req.full_url:
            return Resp(200, {"access_token": "tok"})
        return Resp(200, {"items": []})

    assert HttpYouTube(CREDS, urlopen=urlopen, sleep=lambda s: None).get_video("v", "status") is None
    assert sum("oauth2" in c for c in calls) == 2


def test_list_uploads_pages_the_uploads_playlist_and_reads_tags_in_batches_of_50():
    # Chế độ upload tay (factory/manual.py) nhận video bằng tag -> phải đi
    # qua videos.list (playlistItems không có tags). 3 unit cho 50 video,
    # không dùng search.list (100 unit).
    ids = [f"v{i:03d}" for i in range(60)]
    net = Net(
        Resp(200, {"items": [{"contentDetails": {"relatedPlaylists": {"uploads": "UUx"}}}]}),
        Resp(200, {"items": [{"contentDetails": {"videoId": v}} for v in ids[:50]], "nextPageToken": "p2"}),
        Resp(200, {"items": [{"contentDetails": {"videoId": v}} for v in ids[50:]]}),
        Resp(200, {"items": [{"id": v, "snippet": {"tags": [f"yf-{v}"]}, "status": {}} for v in ids[:50]]}),
        Resp(200, {"items": [{"id": v, "snippet": {}, "status": {}} for v in ids[50:55]]}),
    )
    got = make(net).list_uploads(55)
    assert [v["id"] for v in got] == ids[:55]
    assert got[0]["snippet"]["tags"] == ["yf-v000"]
    calls = [c[1] for c in net.uploads()]
    assert "pageToken=p2" in calls[2]
    assert calls[3].split("id=")[1].count("%2C") == 49 and "part=snippet%2Cstatus" in calls[3]
    assert all("search" not in c for c in calls)
