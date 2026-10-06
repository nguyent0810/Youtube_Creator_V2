"""FakeYouTube -- adapter in-memory của port YouTubeApi, cho test.

Mô phỏng đúng những thứ đã từng làm hỏng kênh thật, không mô phỏng HTTP:
  - videos.update GHI ĐÈ cả part (thiếu trường nào là trường đó mất);
  - phiên upload: đứt sau khi đã có URI, có thể video đã tạo xong;
  - phiên hết hạn (hỏi lại thì không trả lời được).
Chi tiết HTTP (308, 401, chunk) test riêng cho HttpYouTube.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from factory.youtube_api import UploadInDoubt


@dataclass
class _Planned:
    exc: Exception
    after_session: bool
    completed: bool


class FakeYouTube:
    def __init__(self):
        self.videos: dict[str, dict] = {}
        self.inserts = 0                    # số video THẬT SỰ được tạo
        self.sessions: dict[str, dict] = {}
        self.thumbnails: dict[str, Path] = {}
        self._insert_failures: list[_Planned] = []
        self._thumb_failures: list[Exception] = []
        self._n = 0
        # Gọi MỘT lần ngay trước khi mở phiên mới: chỗ để test chen một tiến
        # trình thứ hai vào giữa lúc giữ slot và lúc có session URI.
        self.before_session: Callable[[], None] | None = None
        # Mô phỏng truyền nhiều chunk: gọi on_progress() rồi during_upload(bước)
        # sau mỗi chunk, trước khi video được tạo.
        self.progress_steps = 0
        self.during_upload: Callable[[int], None] | None = None

    # ── kịch bản lỗi ──────────────────────────────────────────────────────
    def fail_next_insert(self, exc: Exception, *, after_session: bool = True,
                         completed: bool = False) -> None:
        """Lần insert kế tiếp ném `exc`. after_session=False: ném trước khi có
        URI (vd 429 lúc khởi tạo). completed=True: video đã tạo xong trên
        YouTube nhưng phản hồi bị mất."""
        self._insert_failures.append(_Planned(exc, after_session, completed))

    def expire_session(self, uri: str) -> None:
        self.sessions.pop(uri, None)

    def fail_next_thumbnail(self, exc: Exception) -> None:
        self._thumb_failures.append(exc)

    def add_video(self, snippet: dict, status: dict) -> str:
        """Video có sẵn trên kênh mà sổ không biết (đăng tay, v1, upload dở)."""
        return self._create({"snippet": snippet, "status": status})

    def go_live(self, video_id: str) -> None:
        """Tới giờ hẹn: YouTube tự chuyển public và xoá publishAt."""
        st = self.videos[video_id]["status"]
        st["privacyStatus"] = "public"
        st.pop("publishAt", None)

    # ── port ─────────────────────────────────────────────────────────────
    def insert_video(self, meta: dict, path: Path, *, resume_uri: str | None,
                     on_session: Callable[[str], None],
                     on_progress: Callable[[], None] | None = None) -> str:
        if resume_uri is not None:
            s = self.sessions.get(resume_uri)
            if s is None:
                raise UploadInDoubt(f"phiên {resume_uri} không còn (404)")
            if s["video_id"] is None:
                s["video_id"] = self._create(s["meta"])
            return s["video_id"]

        plan = self._insert_failures.pop(0) if self._insert_failures else None
        if plan and not plan.after_session:
            raise plan.exc
        if self.before_session:
            hook, self.before_session = self.before_session, None
            hook()
        self._n += 1
        uri = f"fake://session/{self._n}"
        self.sessions[uri] = {"meta": copy.deepcopy(meta), "video_id": None}
        on_session(uri)
        for step in range(self.progress_steps):
            if self.during_upload:
                self.during_upload(step)
            if on_progress:
                on_progress()
        if plan:
            if plan.completed:
                self.sessions[uri]["video_id"] = self._create(meta)
            raise plan.exc
        vid = self._create(meta)
        self.sessions[uri]["video_id"] = vid
        return vid

    def get_video(self, video_id: str, parts: str) -> dict | None:
        v = self.videos.get(video_id)
        if v is None:
            return None
        return {"id": video_id, **{p: copy.deepcopy(v[p]) for p in parts.split(",")}}

    def update_video(self, part: str, body: dict) -> None:
        v = self.videos[body["id"]]
        for p in part.split(","):
            v[p] = copy.deepcopy(body[p])

    def set_thumbnail(self, video_id: str, jpg: Path) -> None:
        if self._thumb_failures:
            raise self._thumb_failures.pop(0)
        self.thumbnails[video_id] = jpg

    def list_uploads(self, limit: int) -> list[dict]:
        newest = list(self.videos)[::-1][:limit]
        return [self.get_video(v, "snippet,status") for v in newest]

    def _create(self, meta: dict) -> str:
        self.inserts += 1
        vid = f"vid{self.inserts:04d}"
        status = {"uploadStatus": "uploaded", "embeddable": True, "license": "youtube",
                  "publicStatsViewable": True, **copy.deepcopy(meta["status"])}
        snippet = {"publishedAt": "2026-10-05T03:00:00Z", "channelId": "UCfake",
                   **copy.deepcopy(meta["snippet"])}
        self.videos[vid] = {"snippet": snippet, "status": status}
        return vid
