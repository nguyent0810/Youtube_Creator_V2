"""Port YouTube Data API mà Channel dùng, và adapter HTTP thật.

Channel (factory/channel.py) giữ CHÍNH SÁCH: giãn nhịp, sổ upload, bất biến
privacy, merge khi sửa. File này chỉ biết NÓI CHUYỆN với YouTube: bốn thao
tác, phân loại lỗi, upload resumable, làm mới token.

Hai adapter thoả port này: HttpYouTube (dưới đây, dùng thật) và FakeYouTube
(factory/youtube_fake.py, in-memory cho test). Thiết kế + lý do:
docs/audit/2026-10-05-channel-design.md.
"""
from __future__ import annotations

import json
import mimetypes
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Protocol

from factory.publish import API, TOKEN_URL, UPLOAD_URL, PublishError, QuotaExceeded


class UploadInterrupted(PublishError):
    """Đứt giữa chừng SAU khi đã có session URI (mất mạng, 5xx). Video có thể
    đã tạo xong mà mất phản hồi -- KHÔNG upload lại; lần sau hỏi lại phiên.
    Lỗi tạm: caller hoãn, không tính là hỏng."""


class UploadInDoubt(PublishError):
    """Phiên upload không trả lời được nữa (404 / hết hạn) mà chưa biết video
    đã tạo hay chưa. Máy không tự quyết: người kiểm kênh rồi `resolve`."""


class SessionDead(PublishError):
    """Hỏi phiên nhận 4xx vĩnh viễn (khác 401/404/429): YouTube nói phiên này
    hỏng và không có video nào. Xoá dòng sổ, lần sau upload lại từ đầu."""


class YouTubeApi(Protocol):
    def insert_video(self, meta: dict, path: Path, *, resume_uri: str | None,
                     on_session: Callable[[str], None],
                     on_progress: Callable[[], None] | None = None) -> str:
        """Upload resumable, trả video_id.

        `on_session(uri)` PHẢI được gọi sau khi có URI và TRƯỚC byte đầu
        tiên. Có `resume_uri` thì hỏi lại phiên đó thay vì mở phiên mới.
        `on_progress()` gọi sau mỗi chunk YouTube nhận (nhịp tim để Channel
        gia hạn lease); nó ném thì dừng gửi."""

    def get_video(self, video_id: str, parts: str) -> dict | None: ...

    def update_video(self, part: str, body: dict) -> None:
        """videos.update: GHI ĐÈ toàn bộ từng part gửi lên."""

    def set_thumbnail(self, video_id: str, jpg: Path) -> None: ...


class RateLimited(PublishError):
    """rateLimitExceeded vẫn còn sau khi đã lùi 2/6/18 giây. Lỗi TẠM: chậm
    lại vài phút là hết -- caller hoãn ngắn, không tính là hỏng, và tuyệt
    đối không coi là hết quota tới ngày mai."""


def classify(prefix: str, code: int, body: str) -> PublishError:
    """Đọc BODY trước status. 429 không lý do trên insert là trần upload thật
    (chặn ở lượt 93) -- thử lại vô ích tới lúc reset quota; còn 429/403 có
    lý do rateLimitExceeded thì chỉ cần chậm lại."""
    if "rateLimitExceeded" in body:
        return RateLimited(f"{prefix} HTTP {code}: {body[:400]}")
    if code == 429 or "quotaExceeded" in body or "uploadLimitExceeded" in body:
        return QuotaExceeded(f"{prefix} HTTP {code}: {body[:400]}")
    return PublishError(f"{prefix} HTTP {code}: {body[:400]}")


_NETWORK = (urllib.error.URLError, TimeoutError, ConnectionError)
_BACKOFF = (2, 6, 18)          # giây, cho rateLimitExceeded
_MAX_STALLS = 3                # 308 liên tiếp mà YouTube không nhận thêm byte nào


class HttpYouTube:
    """Adapter thật: urllib của stdlib (không kéo google-api-python-client --
    xem publish.py). Token lấy lười ở lời gọi đầu, làm mới sau 40 phút hoặc
    khi nhận 401; nhờ vậy dựng Channel để hỏi giãn nhịp không tốn mạng.

    Mọi vòng lặp ở đây đều có giới hạn: 401 làm mới token MỘT lần,
    rateLimitExceeded lùi tối đa 3 lần, 308 không tiến tối đa 3 lần."""

    TOKEN_TTL = 40 * 60
    CHUNK = 8 * 1024 * 1024

    def __init__(self, creds: dict, *, urlopen=urllib.request.urlopen, sleep=time.sleep,
                 clock=time.monotonic, chunk: int | None = None):
        for key in ("client_id", "client_secret", "refresh_token"):
            if not creds.get(key):
                raise PublishError(f"credential thiếu {key}")
        self._creds = creds
        self._urlopen = urlopen
        self._sleep = sleep
        self._clock = clock
        self._chunk = chunk or self.CHUNK
        self._token: str | None = None
        self._token_at = 0.0

    # ── token ────────────────────────────────────────────────────────────
    def _tok(self, *, fresh: bool = False) -> str:
        if fresh or self._token is None or self._clock() - self._token_at > self.TOKEN_TTL:
            body = urllib.parse.urlencode({
                "client_id": self._creds["client_id"], "client_secret": self._creds["client_secret"],
                "refresh_token": self._creds["refresh_token"], "grant_type": "refresh_token"}).encode()
            try:
                with self._urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=60) as r:
                    self._token = json.loads(r.read())["access_token"]
            except urllib.error.HTTPError as e:
                raise PublishError(f"đổi token lỗi HTTP {e.code}: "
                                   f"{e.read().decode(errors='replace')[:400]}") from e
            self._token_at = self._clock()
        return self._token

    def _request(self, method: str, url: str, *, data: bytes | None = None,
                 headers: dict | None = None) -> urllib.request.Request:
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self._tok()}")
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        return req

    def _send(self, method: str, url: str, *, data: bytes | None = None,
              headers: dict | None = None, timeout: int = 120) -> tuple[bytes, dict]:
        """Một lời gọi KHÔNG phải gửi byte video: trả (body, headers).
        401 -> token mới, thử lại một lần; rateLimitExceeded -> lùi; còn lại
        phân loại rồi ném."""
        refreshed = False
        backoff = iter(_BACKOFF)
        while True:
            req = self._request(method, url, data=data, headers=headers)
            try:
                with self._urlopen(req, timeout=timeout) as r:
                    return r.read(), r.headers
            except urllib.error.HTTPError as e:
                if e.code == 401 and not refreshed:
                    self._tok(fresh=True)
                    refreshed = True
                    continue
                err = classify(f"{method} {url.split('?')[0]} ->", e.code,
                               e.read().decode(errors="replace"))
                wait = next(backoff, None) if isinstance(err, RateLimited) else None
                if wait is None:
                    err.status = e.code
                    raise err from e
                self._sleep(wait)

    def get_json(self, url: str) -> dict:
        """GET một URL Google API bất kỳ bằng token của kênh này (đọc
        Analytics, videos.list...). Lỗi mang `.status` = mã HTTP."""
        raw, _ = self._send("GET", url)
        return json.loads(raw) if raw else {}

    def _json(self, method: str, path: str, params: dict, payload: dict | None = None) -> dict:
        url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
        data = json.dumps(payload).encode() if payload is not None else None
        raw, _ = self._send(method, url, data=data,
                            headers={"Content-Type": "application/json"} if data else None)
        return json.loads(raw) if raw else {}

    # ── port ─────────────────────────────────────────────────────────────
    def get_video(self, video_id: str, parts: str) -> dict | None:
        items = self._json("GET", "videos", {"part": parts, "id": video_id}).get("items") or []
        return items[0] if items else None

    def update_video(self, part: str, body: dict) -> None:
        self._json("PUT", "videos", {"part": part}, body)

    def set_thumbnail(self, video_id: str, jpg: Path) -> None:
        url = ("https://www.googleapis.com/upload/youtube/v3/thumbnails/set?"
               + urllib.parse.urlencode({"videoId": video_id}))
        self._send("POST", url, data=jpg.read_bytes(), headers={"Content-Type": "image/jpeg"})

    def insert_video(self, meta: dict, path: Path, *, resume_uri: str | None,
                     on_session: Callable[[str], None],
                     on_progress: Callable[[], None] | None = None) -> str:
        if not path.exists():
            raise PublishError(f"không thấy video: {path}")
        size = path.stat().st_size
        if resume_uri is None:
            uri = self._open_session(meta, path, size)
            on_session(uri)              # TRƯỚC byte đầu tiên
            offset = 0
        else:
            uri = resume_uri
            done, offset = self._query_session(uri, size)
            if done:
                return done
        return self._send_from(uri, path, size, offset, on_progress or (lambda: None))

    def _open_session(self, meta: dict, path: Path, size: int) -> str:
        """Chưa có phiên -> lỗi nào ở đây cũng chắc chắn chưa có video."""
        mime = mimetypes.guess_type(str(path))[0] or "video/mp4"
        url = UPLOAD_URL + "?" + urllib.parse.urlencode({"part": "snippet,status",
                                                         "uploadType": "resumable"})
        _, headers = self._send("POST", url, data=json.dumps(meta).encode(), timeout=60, headers={
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": mime})
        loc = headers.get("Location") if headers else None
        if not loc:
            raise PublishError("YouTube không trả Location cho phiên upload")
        return loc

    def _query_session(self, uri: str, size: int) -> tuple[str | None, int]:
        """Hỏi phiên đã nhận tới đâu: (video_id nếu đã xong, offset gửi tiếp).

        Chỉ báo SessionDead (Channel được xoá dòng sổ) khi YouTube trả 4xx
        vĩnh viễn: không phải 401, 404, quota hay rate limit. 404 = hết hạn,
        không biết video có hay chưa -> UploadInDoubt, người quyết."""
        refreshed = False
        backoff = iter(_BACKOFF)
        while True:
            req = self._request("PUT", uri, data=b"", headers={"Content-Range": f"bytes */{size}"})
            try:
                with self._urlopen(req, timeout=60) as r:
                    return json.loads(r.read())["id"], size
            except urllib.error.HTTPError as e:
                if e.code == 308:
                    return None, _next_offset(e.headers)
                if e.code == 401:
                    if refreshed:
                        raise UploadInterrupted("hỏi phiên: vẫn 401 sau khi làm mới token") from e
                    self._tok(fresh=True)
                    refreshed = True
                    continue
                if e.code == 404:
                    raise UploadInDoubt(f"phiên upload hết hạn (404): {uri}") from e
                err = classify("hỏi phiên ->", e.code, e.read().decode(errors="replace"))
                if isinstance(err, RateLimited):
                    wait = next(backoff, None)
                    if wait is None:
                        raise err from e
                    self._sleep(wait)
                    continue
                if isinstance(err, QuotaExceeded):
                    raise err from e
                if e.code >= 500:
                    raise UploadInterrupted(f"hỏi phiên HTTP {e.code}") from e
                raise SessionDead(f"phiên upload hỏng: {err}") from e
            except _NETWORK as e:
                raise UploadInterrupted(f"hỏi phiên: {e}") from e

    def _send_from(self, uri: str, path: Path, size: int, offset: int,
                   on_progress: Callable[[], None]) -> str:
        """Gửi từ `offset` tới hết. Đã có phiên nên KHÔNG lỗi nào ở đây được
        coi là "không có video": 5xx/mất mạng ở chunk cuối có thể là video đã
        tạo xong mà mất phản hồi -- tất cả thành UploadInterrupted (giữ sổ)."""
        refreshed = False
        backoff = iter(_BACKOFF)
        stalls = 0
        with open(path, "rb") as fh:
            while True:
                fh.seek(offset)
                chunk = fh.read(self._chunk)
                end = offset + len(chunk) - 1
                req = self._request("PUT", uri, data=chunk, headers={
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {offset}-{end}/{size}"})
                try:
                    with self._urlopen(req, timeout=600) as r:
                        return json.loads(r.read())["id"]
                except urllib.error.HTTPError as e:
                    if e.code == 308:
                        nxt = _next_offset(e.headers)
                        stalls = stalls + 1 if nxt <= offset else 0
                        if stalls >= _MAX_STALLS:
                            raise UploadInterrupted(f"YouTube không nhận thêm byte nào sau {offset}") from e
                        offset = nxt
                        on_progress()
                        continue
                    if e.code == 401:
                        if refreshed:
                            raise UploadInterrupted("upload: vẫn 401 sau khi làm mới token") from e
                        self._tok(fresh=True)
                        refreshed = True
                    else:
                        err = classify(f"upload chunk {offset}-{end} ->", e.code,
                                       e.read().decode(errors="replace"))
                        if isinstance(err, QuotaExceeded):
                            raise err from e
                        wait = next(backoff, None) if isinstance(err, RateLimited) else None
                        if wait is None:
                            raise UploadInterrupted(str(err)) from e
                        self._sleep(wait)
                    # Sau 401 / rate limit: hỏi lại phiên đã nhận tới đâu.
                    done, offset = self._query_session(uri, size)
                    if done:
                        return done
                except _NETWORK as e:
                    raise UploadInterrupted(f"upload chunk {offset}-{end}: {e}") from e


def _next_offset(headers) -> int:
    """308 + Range "bytes=0-N" -> gửi tiếp từ N+1. Không có Range = chưa nhận byte nào."""
    rng = headers.get("Range") if headers else None
    if not rng:
        return 0
    return int(rng.rsplit("-", 1)[1]) + 1
