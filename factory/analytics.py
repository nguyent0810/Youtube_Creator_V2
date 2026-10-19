"""Port đọc số liệu YouTube cho bảng điểm (factory/scoreboard.py), và adapter HTTP thật.

Hai adapter: HttpAnalytics (dưới đây) và FakeAnalytics (factory/analytics_fake.py).
Chính sách (cửa sổ, tuổi video, xếp hạng) nằm ở scoreboard; ở đây chỉ hỏi và
trả lời. Thiết kế: docs/audit/2026-10-05-feedback-loop-design.md.
"""
from __future__ import annotations

import re
import urllib.parse
from datetime import date
from typing import Protocol

from factory.publish import PublishError


class ReportRejected(PublishError):
    """YouTube Analytics trả 400 cho truy vấn (metric/dimension không hợp lệ
    với kênh/báo cáo này). Cả truy vấn hỏng, không có dòng nào trả về."""


class AnalyticsApi(Protocol):
    def video_facts(self, video_ids: list[str]) -> dict[str, dict]:
        """video_id -> {"privacy", "publish_at", "published_at", "duration_s"}.
        Video không còn (xoá) thì vắng mặt."""

    def report(self, *, start: date, end: date, metrics: str, dimensions: str,
               video_ids: list[str] | None = None) -> list[dict]:
        """Một truy vấn reports.query (ids=channel==MINE), MỌI trang. Mỗi dòng
        là dict tên cột -> giá trị. Ném ReportRejected nếu API trả 400."""

    def top_search_terms(self, *, start: date, end: date) -> list[dict]:
        """Top 25 từ khoá YT_SEARCH đã dẫn người xem tới kênh: MỘT truy vấn, không đi
        trang (báo cáo này buộc sort và tối đa 25 dòng). Ném ReportRejected nếu 400."""


ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
VIDEOS = "https://www.googleapis.com/youtube/v3/videos"
_DURATION = re.compile(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def _seconds(iso: str | None) -> int | None:
    m = _DURATION.fullmatch(iso or "")
    if not m:
        return None
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return ((d * 24 + h) * 60 + mi) * 60 + s


class HttpAnalytics:
    """Adapter thật. Dùng chung token + lùi khi rate limit của HttpYouTube --
    credential của cả 3 kênh đã có quyền đọc Analytics (thử 30/09/2026)."""

    def __init__(self, http, *, page_size: int = 200):
        self._http = http
        self._page = page_size

    @classmethod
    def open(cls, code: str) -> "HttpAnalytics":
        import json
        from factory import channels
        from factory.youtube_api import HttpYouTube
        return cls(HttpYouTube(json.loads(channels.creds_path(code).read_text(encoding="utf-8"))))

    def _get(self, url: str) -> dict:
        try:
            return self._http.get_json(url)
        except PublishError as e:
            if getattr(e, "status", None) == 400:
                raise ReportRejected(str(e)) from e
            raise

    def video_facts(self, video_ids: list[str]) -> dict[str, dict]:
        out = {}
        for i in range(0, len(video_ids), 50):          # videos.list: tối đa 50 id, 1 đơn vị quota
            q = urllib.parse.urlencode({"part": "status,snippet,contentDetails",
                                        "id": ",".join(video_ids[i:i + 50])})
            for it in self._http.get_json(f"{VIDEOS}?{q}").get("items", []):
                st, sn = it.get("status", {}), it.get("snippet", {})
                out[it["id"]] = {"privacy": st.get("privacyStatus"), "publish_at": st.get("publishAt"),
                                 "published_at": sn.get("publishedAt"),
                                 "duration_s": _seconds(it.get("contentDetails", {}).get("duration"))}
        return out

    def top_search_terms(self, *, start: date, end: date) -> list[dict]:
        q = urllib.parse.urlencode({
            "ids": "channel==MINE", "startDate": start.isoformat(), "endDate": end.isoformat(),
            "metrics": "views", "dimensions": "insightTrafficSourceDetail",
            "filters": "insightTrafficSourceType==YT_SEARCH", "sort": "-views", "maxResults": 25})
        d = self._get(f"{ANALYTICS}?{q}")
        names = [h["name"] for h in d.get("columnHeaders", [])]
        return [dict(zip(names, r)) for r in d.get("rows") or []]

    def report(self, *, start: date, end: date, metrics: str, dimensions: str,
               video_ids: list[str] | None = None) -> list[dict]:
        params = {"ids": "channel==MINE", "startDate": start.isoformat(), "endDate": end.isoformat(),
                  "metrics": metrics, "dimensions": dimensions, "maxResults": self._page}
        if video_ids:
            # KHÔNG gửi `sort`: báo cáo lọc theo danh sách id không đòi sort, còn
            # báo cáo "top video" chỉ nhận sort theo views/watch time -- sort theo
            # engagedViews sẽ bị 400 và cột quyết định thành NULL vĩnh viễn.
            params["filters"] = "video==" + ",".join(video_ids)
        rows, start_index = [], 1
        while True:
            q = urllib.parse.urlencode({**params, "startIndex": start_index})
            d = self._get(f"{ANALYTICS}?{q}")
            names = [h["name"] for h in d.get("columnHeaders", [])]
            got = [dict(zip(names, r)) for r in d.get("rows") or []]
            rows += got
            # Không có tài liệu nào nói trang mặc định dài bao nhiêu: tự đi
            # hết trang, nếu không một nhóm 500 video sẽ bị lưu thiếu âm thầm.
            if len(got) < self._page:
                return rows
            start_index += len(got)
