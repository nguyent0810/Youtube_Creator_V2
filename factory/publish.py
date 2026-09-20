"""Upload lên YouTube: video + metadata + thumbnail + hẹn giờ.

KHÔNG CÓ LLM. Tiêu đề/mô tả/tag đã nằm sẵn trong Bundle.

Dùng urllib của stdlib, không kéo google-api-python-client: ta chỉ cần đúng
bốn endpoint, và thêm một dependency nặng chỉ để gọi REST là đi ngược tinh
thần HIT & RUN.

QUOTA (kiểm chứng ngày 19/09/2026 trên tài liệu chính thức):
  videos.insert      -- hạn mức RIÊNG 100 lần/ngày, chỉ 1 đơn vị mỗi lần
  playlistItems.insert, thumbnails.set, videos.update -- 50 đơn vị
  videos.list, playlistItems.list                     -- 1 đơn vị
  search.list        -- 100 lần/ngày, RẤT CHẬT

  15 short/ngày = 15/100 lượt upload + ~900/10.000 đơn vị. Thoải mái.
  Nhưng search.list thì TRÁNH DÙNG -- mọi việc tra cứu ở đây đều đi qua
  videos.list / playlistItems.list (1 đơn vị) thay vì search.

AN TOÀN: mặc định privacy_status = "private" + publishAt. Video lên lịch
sẽ tự chuyển public đúng giờ. Không bao giờ đăng public ngay -- một lần
nhầm là công khai thật, không rút lại được.
"""
from __future__ import annotations

import json
import mimetypes
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
API = "https://www.googleapis.com/youtube/v3"

# Short: YouTube nhận diện qua tỉ lệ dọc + độ dài <= 3 phút. Không có
# tham số API nào để "đánh dấu là Short" -- thêm #Shorts vào mô tả là quy
# ước phổ biến và vô hại.
SHORTS_MARKER = "#Shorts"

CHUNK = 8 * 1024 * 1024


class PublishError(RuntimeError):
    pass


@dataclass
class PublishResult:
    video_id: str
    url: str
    scheduled_at: str


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
        raise PublishError(f"{method} {path} -> HTTP {e.code}: {e.read().decode()[:400]}") from e


def upload_video(bundle, video_path: Path, token: str) -> str:
    """Upload resumable, trả về video_id.

    Đặt privacy=private + publishAt, KHÔNG public ngay. Resumable chứ không
    upload một phát: file 15-60 MB qua mạng nhà dễ đứt, và upload lại từ
    đầu thì tốn cả hạn mức lẫn thời gian."""
    if not video_path.exists():
        raise PublishError(f"không thấy video: {video_path}")

    description = bundle.description
    if bundle.kind == "short" and SHORTS_MARKER.lower() not in description.lower():
        description = f"{description}\n\n{SHORTS_MARKER}".strip()

    meta = {
        "snippet": {
            "title": bundle.title,
            "description": description,
            "tags": list(bundle.tags),
            "categoryId": "22",           # People & Blogs
            "defaultLanguage": "vi",
            "defaultAudioLanguage": "vi",
        },
        "status": {
            "privacyStatus": "private",   # KHÔNG BAO GIỜ public ngay
            "publishAt": bundle.publish_at,
            "selfDeclaredMadeForKids": False,
        },
    }

    size = video_path.stat().st_size
    mime = mimetypes.guess_type(str(video_path))[0] or "video/mp4"
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
    except urllib.error.HTTPError as e:
        raise PublishError(f"khởi tạo upload lỗi HTTP {e.code}: {e.read().decode()[:400]}") from e
    if not session_url:
        raise PublishError("YouTube không trả Location cho phiên upload")

    sent = 0
    with open(video_path, "rb") as fh:
        while sent < size:
            chunk = fh.read(CHUNK)
            end = sent + len(chunk) - 1
            put = urllib.request.Request(session_url, data=chunk, method="PUT")
            put.add_header("Content-Length", str(len(chunk)))
            put.add_header("Content-Range", f"bytes {sent}-{end}/{size}")
            try:
                with urllib.request.urlopen(put, timeout=600) as r:
                    payload = json.load(r)
                    return payload["id"]
            except urllib.error.HTTPError as e:
                if e.code == 308:      # còn tiếp -- đúng luồng resumable
                    sent = end + 1
                    continue
                raise PublishError(f"upload lỗi HTTP {e.code}: {e.read().decode()[:400]}") from e
    raise PublishError("upload kết thúc mà YouTube không trả video id")


def set_thumbnail(video_id: str, jpg_path: Path, token: str) -> None:
    url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
    req = urllib.request.Request(url, data=jpg_path.read_bytes(), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "image/jpeg")
    try:
        urllib.request.urlopen(req, timeout=120).close()
    except urllib.error.HTTPError as e:
        raise PublishError(f"đặt thumbnail lỗi HTTP {e.code}: {e.read().decode()[:400]}") from e


def add_to_playlist(video_id: str, playlist_id: str, token: str) -> None:
    _api(token, "POST", "playlistItems", {"part": "snippet"}, {
        "snippet": {"playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id}},
    })


def already_published(title: str, uploads_playlist_id: str, token: str) -> str | None:
    """Tìm video trùng tiêu đề trong playlist uploads của kênh.

    Dùng playlistItems.list (1 đơn vị) chứ KHÔNG dùng search.list (chỉ 100
    lần/ngày cho cả project). Đây là lớp chống đăng trùng khi chạy lại sau
    một lần đứt giữa chừng -- registry cục bộ có thể lệch thực tế, nên hỏi
    thẳng YouTube."""
    page = None
    for _ in range(10):  # ~500 video gần nhất là quá đủ để bắt trùng
        params = {"part": "snippet", "playlistId": uploads_playlist_id, "maxResults": 50}
        if page:
            params["pageToken"] = page
        data = _api(token, "GET", "playlistItems", params)
        for item in data.get("items", []):
            sn = item["snippet"]
            if sn.get("title", "").strip() == title.strip():
                return sn.get("resourceId", {}).get("videoId")
        page = data.get("nextPageToken")
        if not page:
            break
    return None


def uploads_playlist_id(token: str) -> str:
    data = _api(token, "GET", "channels", {"part": "contentDetails", "mine": "true"})
    try:
        return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except (KeyError, IndexError) as e:
        raise PublishError(f"không đọc được playlist uploads: {data}") from e


def publish_bundle(bundle, video_path: Path, creds: dict,
                   thumb_path: Path | None = None,
                   playlist_id: str | None = None,
                   skip_if_duplicate: bool = True) -> PublishResult:
    """Đăng một Bundle. Hẹn giờ, không public ngay."""
    token = access_token(creds)

    if skip_if_duplicate:
        existing = already_published(bundle.title, uploads_playlist_id(token), token)
        if existing:
            return PublishResult(video_id=existing,
                                 url=f"https://youtu.be/{existing}",
                                 scheduled_at=bundle.publish_at)

    video_id = upload_video(bundle, video_path, token)
    if thumb_path and thumb_path.exists():
        set_thumbnail(video_id, thumb_path, token)
    if playlist_id:
        add_to_playlist(video_id, playlist_id, token)
    return PublishResult(video_id=video_id,
                         url=f"https://youtu.be/{video_id}",
                         scheduled_at=bundle.publish_at)


def set_schedule(video_id: str, publish_at: str, token: str) -> None:
    """Gán publishAt cho video ĐÃ upload, không phải upload lại.

    Cần cho đúng một tình huống: video đăng bằng `probe` nằm trên kênh ở
    chế độ private KHÔNG có lịch (cố ý, để không tự công khai khi chưa ai
    duyệt). Sau khi người duyệt xong, nó cần được gán lịch -- mà upload lại
    thì vừa tốn hạn mức vừa tạo bản trùng.

    videos.update tốn 50 đơn vị, rẻ hơn nhiều so với một lượt upload mới.
    Bắt buộc gửi kèm `snippet` vì YouTube coi update là GHI ĐÈ toàn phần:
    thiếu trường nào là trường đó bị xoá trắng, kể cả tiêu đề.
    """
    cur = _api(token, "GET", "videos", {"part": "snippet,status", "id": video_id})
    items = cur.get("items") or []
    if not items:
        raise PublishError(f"không thấy video {video_id} trên kênh")
    snippet = items[0]["snippet"]
    status = items[0]["status"]

    _api(token, "PUT", "videos", {"part": "snippet,status"}, {
        "id": video_id,
        # Giữ nguyên snippet cũ -- update là ghi đè toàn phần.
        "snippet": {
            "title": snippet["title"],
            "description": snippet.get("description", ""),
            "tags": snippet.get("tags", []),
            "categoryId": snippet.get("categoryId", "22"),
            "defaultLanguage": snippet.get("defaultLanguage", "vi"),
        },
        "status": {
            "privacyStatus": "private",     # phải giữ private thì publishAt mới có tác dụng
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": status.get("selfDeclaredMadeForKids", False),
        },
    })
