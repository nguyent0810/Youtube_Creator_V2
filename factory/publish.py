"""Gọi YouTube Data API -- phần ĐỌC (token, playlist uploads, tiêu đề kênh)
và lớp lỗi dùng chung.

MỌI LẦN GHI (upload, thumbnail, sửa lịch, sửa tiêu đề) đi qua
factory/channel.py từ 05/10/2026: giãn nhịp, sổ chống upload trùng, merge khi
sửa. Các hàm ghi cũ ở đây (upload_video, publish_bundle, set_schedule...) đã
bị xoá để không đường nào lách được Channel. Lý do:
docs/audit/2026-10-05-channel-design.md.

Dùng urllib của stdlib, không kéo google-api-python-client: ta chỉ cần đúng
bốn endpoint, và thêm một dependency nặng chỉ để gọi REST là đi ngược tinh
thần HIT & RUN.

QUOTA (kiểm chứng ngày 19/09/2026 trên tài liệu chính thức):
  videos.insert      -- hạn mức RIÊNG, tài liệu ghi 100 lần/ngày, THỰC TẾ
                        chặn ở lượt thứ 93 (HTTP 429, đo ngày 20/09/2026).
                        Reset nửa đêm giờ Thái Bình Dương.
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
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
API = "https://www.googleapis.com/youtube/v3"


class PublishError(RuntimeError):
    pass


class QuotaExceeded(PublishError):
    """Hết hạn mức -- lỗi TẠM, video không có gì sai. Gọi tiếp chỉ phí thời
    gian: mọi lời gọi sau đều sẽ nhận đúng lỗi này tới lúc reset."""


def _raise(prefix: str, code: int, body: str) -> None:
    if code == 429 or "quotaExceeded" in body or "uploadLimitExceeded" in body             or "rateLimitExceeded" in body:
        raise QuotaExceeded(f"{prefix} HTTP {code}: {body[:400]}")
    raise PublishError(f"{prefix} HTTP {code}: {body[:400]}")


def next_quota_reset(now=None) -> str:
    """Mốc reset quota kế tiếp, ISO UTC.

    Reset lúc 00:00 giờ Thái Bình Dương = 07:00 UTC (mùa hè) hoặc 08:00 UTC
    (mùa đông). Lấy 08:05 UTC cho cả năm: muộn nhất một giờ vào mùa hè,
    nhưng không bao giờ thử lại TRƯỚC khi reset -- và không cần tzdata, thứ
    Windows không có sẵn."""
    from datetime import datetime, timedelta, timezone
    now = now or datetime.now(timezone.utc)
    t = now.replace(hour=8, minute=5, second=0, microsecond=0)
    if t <= now:
        t += timedelta(days=1)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


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


def add_to_playlist(video_id: str, playlist_id: str, token: str) -> None:
    _api(token, "POST", "playlistItems", {"part": "snippet"}, {
        "snippet": {"playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id}},
    })


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


def uploads_playlist_id(token: str) -> str:
    data = _api(token, "GET", "channels", {"part": "contentDetails", "mine": "true"})
    try:
        return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except (KeyError, IndexError) as e:
        raise PublishError(f"không đọc được playlist uploads: {data}") from e
