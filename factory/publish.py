"""Upload lên YouTube: video + metadata + thumbnail + hẹn giờ.

KHÔNG CÓ LLM. Tiêu đề/mô tả/tag đã nằm sẵn trong Bundle.

Dùng urllib của stdlib, không kéo google-api-python-client: ta chỉ cần vài
endpoint, và thêm một dependency nặng chỉ để gọi REST là đi ngược tinh thần
HIT & RUN.

QUOTA (kiểm chứng ngày 19/09/2026 trên tài liệu chính thức):
  videos.insert      -- hạn mức RIÊNG, tài liệu ghi 100 lần/ngày, THỰC TẾ
                        chặn ở lượt thứ 93 (HTTP 429, đo ngày 20/09/2026).
                        Reset nửa đêm giờ Thái Bình Dương.
  playlistItems.insert, thumbnails.set, videos.update -- 50 đơn vị
  videos.list, playlistItems.list, channels.list      -- 1 đơn vị
  search.list        -- 100 lần/ngày, RẤT CHẬT -> không dùng

AN TOÀN -- ba chốt, đều ở tầng THẤP NHẤT để mọi đường đăng (Shorts, S-tier,
video dài) cùng đi qua:

  1. Luôn private + publishAt. Không bao giờ đăng public ngay.
  2. publishAt phải ở TƯƠNG LAI (>= 15 phút). Tài liệu YouTube (Videos,
     status.publishAt): hẹn giờ ở quá khứ thì video được công khai NGAY.
     Item bị hoãn vì quota, bị bỏ qua vì "ngày bận", hay chạy lại muộn đều
     có thể mang giờ đã qua -- trước đây chúng được upload và lên sóng tức
     thì, sai giờ, và verify không thấy gì bất thường.
  3. Chống trùng KHÔNG tự nhận video người khác. Mỗi upload mang một tag
     dấu `yf<bundle.id>`. Thấy video cùng tiêu đề trên kênh: có dấu của
     chính bundle -> nhận lại (bản đã upload mà store chưa kịp ghi, hoặc bản
     probe chờ gán lịch); không có dấu -> DuplicateTitle, không upload, không
     đánh dấu "đã đăng". Trước đây mọi video cùng tiêu đề đều bị nhận, kể cả
     video của nguồn khác trên cùng kênh.
"""
from __future__ import annotations

import http.client
import json
import mimetypes
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from factory.credits import final_description

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
API = "https://www.googleapis.com/youtube/v3"

CHUNK = 8 * 1024 * 1024          # bội số của 256 KiB, đúng yêu cầu resumable upload
MIN_LEAD = timedelta(minutes=15)  # publishAt phải muộn hơn "bây giờ" ít nhất chừng này
UPLOAD_RETRIES = 6


class PublishError(RuntimeError):
    pass


class QuotaExceeded(PublishError):
    """Hết hạn mức NGÀY -- lỗi TẠM, video không có gì sai. Gọi tiếp chỉ phí thời
    gian: mọi lời gọi sau đều sẽ nhận đúng lỗi này tới lúc reset."""


class RateLimited(PublishError):
    """403 rateLimitExceeded / userRateLimitExceeded: giới hạn TỐC ĐỘ ngắn hạn.

    Khác QuotaExceeded: chờ vài chục giây là gọi lại được. Trước đây bị gộp
    vào hết quota nên cả lô còn lại bị hoãn ~24 giờ."""


class PublishAtPassed(PublishError):
    """Giờ hẹn đã qua hoặc quá sát. Gửi đi thì YouTube công khai NGAY."""


class DuplicateTitle(PublishError):
    """Kênh đã có video cùng tiêu đề mà KHÔNG mang dấu của bundle này."""

    def __init__(self, msg: str, video_id: str):
        super().__init__(msg)
        self.video_id = video_id


class _Transient(Exception):
    """Lỗi mạng/5xx giữa chừng upload: hỏi lại tiến độ rồi gửi tiếp."""


def _raise(prefix: str, code: int, body: str) -> None:
    if code == 429 or "quotaExceeded" in body or "uploadLimitExceeded" in body:
        raise QuotaExceeded(f"{prefix} HTTP {code}: {body[:400]}")
    if "ratelimitexceeded" in body.lower():   # gồm cả userRateLimitExceeded
        raise RateLimited(f"{prefix} HTTP {code}: {body[:400]}")
    raise PublishError(f"{prefix} HTTP {code}: {body[:400]}")


def next_quota_reset(now=None) -> str:
    """Mốc reset quota kế tiếp, ISO UTC.

    Reset lúc 00:00 giờ Thái Bình Dương = 07:00 UTC (giờ mùa hè của Mỹ) hoặc
    08:00 UTC (giờ mùa đông). Lấy 08:05 UTC cho cả năm: muộn nhất một giờ
    vào mùa hè, nhưng không bao giờ thử lại TRƯỚC khi reset -- và không cần
    tzdata, thứ Windows không có sẵn."""
    now = now or datetime.now(timezone.utc)
    t = now.replace(hour=8, minute=5, second=0, microsecond=0)
    if t <= now:
        t += timedelta(days=1)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_publish_at(publish_at: str) -> datetime:
    try:
        return datetime.strptime(publish_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError) as e:
        raise PublishError(f"publish_at phải là ISO-8601 UTC kết thúc bằng Z, nhận {publish_at!r}") from e


def check_publish_at(publish_at: str, now: datetime | None = None) -> datetime:
    """Ném PublishAtPassed nếu giờ hẹn không ở tương lai đủ xa."""
    when = parse_publish_at(publish_at)
    now = now or datetime.now(timezone.utc)
    if when <= now + MIN_LEAD:
        raise PublishAtPassed(
            f"giờ hẹn {publish_at} đã qua hoặc còn dưới {int(MIN_LEAD.total_seconds() // 60)} phút -- "
            "gửi publishAt quá khứ thì YouTube CÔNG KHAI NGAY. Không upload; dời lịch item này.")
    return when


def marker_tag(bundle) -> str | None:
    """Tag dấu nhận diện bản upload của CHÍNH bundle này (chỉ chữ + số)."""
    bid = getattr(bundle, "id", None)
    return f"yf{bid}" if bid else None


@dataclass
class PublishResult:
    video_id: str
    url: str
    scheduled_at: str
    adopted: bool = False                  # nhận lại bản đã có, không upload mới
    warnings: list[str] = field(default_factory=list)


def _post(url: str, data: dict) -> dict:
    body = urllib.parse.urlencode(data).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise PublishError(f"{url} -> HTTP {e.code}: {e.read().decode()[:400]}") from e


def access_token(creds: dict) -> str:
    """Đổi refresh_token lấy access_token. refresh_token dùng lại được vô
    hạn lần cho tới khi bị thu hồi tay -- không cần lưu access_token."""
    for key in ("client_id", "client_secret", "refresh_token"):
        if not creds.get(key):
            raise PublishError(f"credential thiếu {key}")
    tok = _post(TOKEN_URL, {
        "client_id": creds["client_id"], "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"], "grant_type": "refresh_token",
    })
    return tok["access_token"]


def _api(token: str, method: str, path: str, params: dict | None = None,
         payload: dict | None = None) -> dict:
    url = f"{API}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r) if r.length != 0 else {}
    except urllib.error.HTTPError as e:
        _raise(f"{method} {path} ->", e.code, e.read().decode(errors="replace"))


# ─── Upload ───────────────────────────────────────────────────────────────

def video_meta(bundle, schedule: bool = True) -> dict:
    """Metadata gửi kèm upload. schedule=False chỉ dành cho `probe`: private,
    KHÔNG publishAt -> không bao giờ tự công khai."""
    tags = list(bundle.tags)
    mk = marker_tag(bundle)
    if mk and mk not in tags:
        tags.append(mk)
    status = {"privacyStatus": "private",   # KHÔNG BAO GIỜ public ngay
              "selfDeclaredMadeForKids": False}
    if schedule:
        check_publish_at(bundle.publish_at)
        status["publishAt"] = bundle.publish_at
    return {
        "snippet": {
            "title": bundle.title,
            "description": final_description(bundle),
            "tags": tags,
            "categoryId": "22",           # People & Blogs
            "defaultLanguage": "vi",
            "defaultAudioLanguage": "vi",
        },
        "status": status,
    }


def _range_end(headers) -> int:
    """Byte kế tiếp cần gửi, đọc từ header Range của phản hồi 308."""
    rng = headers.get("Range") if headers else None
    if not rng:
        return 0
    return int(rng.split("-")[-1]) + 1


def _video_id(resp) -> str:
    payload = json.load(resp)
    if not payload.get("id"):
        raise PublishError(f"upload xong mà YouTube không trả video id: {str(payload)[:300]}")
    return payload["id"]


def _put(session_url: str, data: bytes, content_range: str) -> tuple[str, object]:
    req = urllib.request.Request(session_url, data=data, method="PUT")
    req.add_header("Content-Length", str(len(data)))
    req.add_header("Content-Range", content_range)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return "done", _video_id(r)
    except urllib.error.HTTPError as e:
        if e.code == 308:                 # còn tiếp -- đúng luồng resumable
            return "next", _range_end(e.headers)
        if e.code in (500, 502, 503, 504):
            raise _Transient(f"HTTP {e.code}") from e
        if e.code == 404:
            raise PublishError("phiên upload đã hết hạn -- phải upload lại từ đầu") from e
        _raise("upload lỗi", e.code, e.read().decode(errors="replace"))
    except (urllib.error.URLError, http.client.HTTPException, ConnectionError, socket.timeout,
            TimeoutError) as e:
        raise _Transient(str(e)) from e


def _send_file(session_url: str, video_path: Path, size: int,
               retries: int = UPLOAD_RETRIES, sleep=time.sleep) -> str:
    """Gửi file theo từng chunk; đứt thì HỎI LẠI TIẾN ĐỘ rồi gửi tiếp.

    Bản trước gọi là "resumable" nhưng không resume: bỏ qua header Range của
    308, và đứt mạng/5xx là bỏ cả phiên -- lần sau upload lại từ byte 0 và
    bị tính một lần hỏng.

    Bộ đếm lỗi chỉ về 0 khi server XÁC NHẬN có thêm byte, nên mạng chập chờn
    kiểu "gửi hỏng - hỏi được - gửi hỏng" không thể lặp vô hạn."""
    if size <= 0:
        raise PublishError(f"file video rỗng: {video_path}")
    sent, failures, need_status = 0, 0, False
    with open(video_path, "rb") as fh:
        while True:
            was_status = need_status
            try:
                if need_status:
                    state, val = _put(session_url, b"", f"bytes */{size}")
                else:
                    fh.seek(sent)
                    chunk = fh.read(CHUNK)
                    state, val = _put(session_url, chunk, f"bytes {sent}-{sent + len(chunk) - 1}/{size}")
            except _Transient as e:
                failures += 1
                if failures > retries:
                    raise PublishError(f"upload đứt {failures} lần liên tiếp: {e}") from e
                sleep(min(2 ** failures, 60))
                need_status = True
                continue
            if state == "done":
                return val
            need_status = False
            if val > sent:
                failures = 0
            elif not was_status or val >= size:
                failures += 1
                if failures > retries:
                    raise PublishError(f"upload không tiến triển (dừng ở byte {val}/{size})")
                sleep(min(2 ** failures, 60))
            sent = val
            if sent >= size:
                need_status = True        # đã đủ byte mà chưa nhận id -> hỏi lại


def upload_video(bundle, video_path: Path, token: str, schedule: bool = True) -> str:
    """Upload resumable, trả về video_id.

    private + publishAt (đã qua chốt giờ tương lai). Resumable vì file 15-60 MB
    qua mạng nhà dễ đứt; upload lại từ đầu thì tốn cả hạn mức lẫn thời gian."""
    if not video_path.exists():
        raise PublishError(f"không thấy video: {video_path}")
    meta = video_meta(bundle, schedule=schedule)

    size = video_path.stat().st_size
    mime = mimetypes.guess_type(str(video_path))[0] or "video/mp4"
    session_url = None
    for attempt in range(3):
        init = urllib.request.Request(
            UPLOAD_URL + "?" + urllib.parse.urlencode({"part": "snippet,status", "uploadType": "resumable"}),
            data=json.dumps(meta).encode(), method="POST",
        )
        init.add_header("Authorization", f"Bearer {token}")
        init.add_header("Content-Type", "application/json; charset=UTF-8")
        init.add_header("X-Upload-Content-Length", str(size))
        init.add_header("X-Upload-Content-Type", mime)
        try:
            with urllib.request.urlopen(init, timeout=60) as r:
                session_url = r.headers["Location"]
            break
        except urllib.error.HTTPError as e:
            _raise("khởi tạo upload lỗi", e.code, e.read().decode(errors="replace"))
        except (urllib.error.URLError, ConnectionError, socket.timeout, TimeoutError) as e:
            if attempt == 2:
                raise PublishError(f"không mở được phiên upload: {e}") from e
            time.sleep(5 * (attempt + 1))
    if not session_url:
        raise PublishError("YouTube không trả Location cho phiên upload")
    return _send_file(session_url, video_path, size)


def set_thumbnail(video_id: str, jpg_path: Path, token: str) -> None:
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
    req = urllib.request.Request(url, data=jpg_path.read_bytes(), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "image/jpeg")
    try:
        urllib.request.urlopen(req, timeout=120).close()
    except urllib.error.HTTPError as e:
        _raise("đặt thumbnail lỗi", e.code, e.read().decode(errors="replace"))


def add_to_playlist(video_id: str, playlist_id: str, token: str) -> None:
    _api(token, "POST", "playlistItems", {"part": "snippet"}, {
        "snippet": {"playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id}},
    })


# ─── Tra cứu kênh ─────────────────────────────────────────────────────────

def channel_identity(token: str) -> dict:
    """ID + tên + playlist uploads của kênh mà token đang trỏ tới (1 đơn vị)."""
    data = _api(token, "GET", "channels", {"part": "id,snippet,contentDetails", "mine": "true"})
    try:
        it = data["items"][0]
        return {"id": it["id"], "title": it["snippet"]["title"],
                "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"]}
    except (KeyError, IndexError, TypeError) as e:
        raise PublishError(f"không đọc được thông tin kênh: {data}") from e


def uploads_playlist_id(token: str) -> str:
    return channel_identity(token)["uploads"]


def channel_titles(uploads_playlist_id: str, token: str, pages: int = 10) -> dict[str, str]:
    """Tiêu đề -> video_id của ~500 video gần nhất. Gọi MỘT LẦN mỗi lô.

    Trước đây mỗi video tự quét lại cả playlist uploads (tới 10 trang) để
    chống trùng: 31 video = ~340 lời gọi API, và con số tăng theo độ dài
    kênh. Chụp một lần rồi tự cập nhật sau mỗi upload là đủ -- trong một lô
    chỉ có chính ta ghi lên kênh."""
    out: dict[str, str] = {}
    page = None
    for _ in range(pages):
        params = {"part": "snippet", "playlistId": uploads_playlist_id, "maxResults": 50}
        if page:
            params["pageToken"] = page
        data = _api(token, "GET", "playlistItems", params)
        for item in data.get("items", []):
            sn = item["snippet"]
            out.setdefault(sn.get("title", "").strip(),
                           sn.get("resourceId", {}).get("videoId"))
        page = data.get("nextPageToken")
        if not page:
            break
    return out


def already_published(title: str, uploads_playlist_id: str, token: str) -> str | None:
    """Tìm video trùng tiêu đề trong playlist uploads của kênh (playlistItems.list,
    1 đơn vị -- KHÔNG dùng search.list)."""
    return channel_titles(uploads_playlist_id, token).get(title.strip())


def video_status(video_id: str, token: str) -> dict | None:
    items = _api(token, "GET", "videos", {"part": "snippet,status", "id": video_id}).get("items") or []
    return items[0] if items else None


# ─── Đăng một bundle ──────────────────────────────────────────────────────

def adopt_existing(bundle, video_id: str, token: str) -> PublishResult | None:
    """Kênh đã có video cùng tiêu đề. Chỉ NHẬN nếu nó mang dấu của bundle này.

    Trả None nếu video không còn (đã xoá) -> người gọi upload bình thường."""
    it = video_status(video_id, token)
    if it is None:
        return None
    mk = marker_tag(bundle)
    if not mk or mk not in (it.get("snippet", {}).get("tags") or []):
        raise DuplicateTitle(
            f"tiêu đề {bundle.title!r} đã có trên kênh (video {video_id}) nhưng KHÔNG phải bản "
            "upload của bundle này. Không tự nhận, không upload trùng: đổi tiêu đề bundle, "
            "hoặc xác nhận tay rồi ghi video_id vào store.", video_id)
    st = it.get("status", {})
    if st.get("privacyStatus") == "private" and not st.get("publishAt"):
        # Bản `probe` đã được người duyệt: gán lịch thay vì upload lại.
        set_schedule(video_id, bundle.publish_at, token)
        scheduled = bundle.publish_at
    else:
        scheduled = st.get("publishAt") or f"(đang {st.get('privacyStatus')})"
    return PublishResult(video_id=video_id, url=f"https://youtu.be/{video_id}",
                         scheduled_at=scheduled, adopted=True)


def publish_bundle(bundle, video_path: Path, creds: dict,
                   thumb_path: Path | None = None,
                   playlist_id: str | None = None,
                   skip_if_duplicate: bool = True,
                   token: str | None = None,
                   known_titles: dict[str, str] | None = None) -> PublishResult:
    """Đăng một Bundle. Hẹn giờ, không public ngay.

    `known_titles` (từ channel_titles) thì chống trùng bằng bản chụp đó và
    ghi video mới vào luôn; không có thì tự quét kênh.

    Lỗi SAU khi upload thành công (thumbnail, playlist) không làm mất
    video_id: chúng thành cảnh báo trong kết quả, để người gọi vẫn ghi được
    video vào store."""
    check_publish_at(bundle.publish_at)
    token = token or access_token(creds)

    if skip_if_duplicate:
        title = bundle.title.strip()
        existing = (known_titles.get(title) if known_titles is not None
                    else already_published(title, uploads_playlist_id(token), token))
        if existing:
            res = adopt_existing(bundle, existing, token)
            if res is not None:
                return res

    video_id = upload_video(bundle, video_path, token)
    if known_titles is not None:
        known_titles[bundle.title.strip()] = video_id
    res = PublishResult(video_id=video_id, url=f"https://youtu.be/{video_id}",
                        scheduled_at=bundle.publish_at)
    if thumb_path and thumb_path.exists():
        try:
            set_thumbnail(video_id, thumb_path, token)
        except PublishError as e:
            res.warnings.append(f"thumbnail: {e}")
    if playlist_id:
        try:
            add_to_playlist(video_id, playlist_id, token)
        except PublishError as e:
            res.warnings.append(f"playlist: {e}")
    return res


def unschedule(video_id: str, token: str, title_prefix: str = "") -> dict:
    """Gỡ lịch video ĐÃ upload: private, KHÔNG publishAt -> không bao giờ tự công khai.

    Không xoá gì (xoá là vĩnh viễn). `title_prefix` (vd "[ĐÃ THAY] ") gắn vào đầu
    tiêu đề để lọc rồi xoá hàng loạt trong Studio; đã có thì không gắn lại.
    Video đã công khai, hoặc sắp tự công khai trong 2 phút (đang đua với giờ hẹn),
    thì KHÔNG đụng: gỡ lịch không phải là gỡ video đang phát. Mọi trường khác
    được gửi lại nguyên vẹn như set_schedule (update ghi đè toàn phần)."""
    it = video_status(video_id, token)
    if it is None:
        raise PublishError(f"không thấy video {video_id} trên kênh")
    sn, st = it["snippet"], it["status"]
    if st.get("privacyStatus") != "private":
        raise PublishError(f"video {video_id} đang {st.get('privacyStatus')} -- không gỡ lịch video đã công khai")
    pa = st.get("publishAt")
    if pa and datetime.fromisoformat(pa.replace("Z", "+00:00")) < datetime.now(timezone.utc) + timedelta(minutes=2):
        raise PublishError(f"video {video_id} sắp tự công khai ({pa}) -- không đua với giờ hẹn")
    snippet = {k: sn[k] for k in ("title", "description", "tags", "categoryId",
                                  "defaultLanguage", "defaultAudioLanguage") if k in sn}
    snippet.setdefault("categoryId", "22")
    if title_prefix and not snippet.get("title", "").startswith(title_prefix):
        snippet["title"] = (title_prefix + snippet.get("title", ""))[:100]
    status = {k: st[k] for k in ("embeddable", "license", "publicStatsViewable",
                                 "containsSyntheticMedia") if k in st}
    status.update({"privacyStatus": "private",
                   "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", st.get("madeForKids", False))})
    _api(token, "PUT", "videos", {"part": "snippet,status"},
         {"id": video_id, "snippet": snippet, "status": status})
    return {"title": snippet.get("title", ""), "was_scheduled": pa}


def set_schedule(video_id: str, publish_at: str, token: str) -> None:
    """Gán publishAt cho video ĐÃ upload, không phải upload lại.

    Dùng cho video `probe` (private, KHÔNG lịch) sau khi người duyệt xong.
    videos.update tốn 50 đơn vị, rẻ hơn nhiều so với một lượt upload mới.
    YouTube coi update là GHI ĐÈ toàn phần các part gửi lên: thiếu trường nào
    là trường đó bị xoá -- nên mọi trường đang có đều được gửi lại nguyên vẹn."""
    check_publish_at(publish_at)
    it = video_status(video_id, token)
    if it is None:
        raise PublishError(f"không thấy video {video_id} trên kênh")
    sn, st = it["snippet"], it["status"]
    snippet = {k: sn[k] for k in ("title", "description", "tags", "categoryId",
                                  "defaultLanguage", "defaultAudioLanguage") if k in sn}
    snippet.setdefault("categoryId", "22")
    status = {k: st[k] for k in ("embeddable", "license", "publicStatsViewable",
                                 "containsSyntheticMedia") if k in st}
    status.update({
        "privacyStatus": "private",     # phải giữ private thì publishAt mới có tác dụng
        "publishAt": publish_at,
        "selfDeclaredMadeForKids": st.get("selfDeclaredMadeForKids", st.get("madeForKids", False)),
    })
    _api(token, "PUT", "videos", {"part": "snippet,status"},
         {"id": video_id, "snippet": snippet, "status": status})
