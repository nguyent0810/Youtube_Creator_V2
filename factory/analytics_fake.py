"""FakeAnalytics -- adapter in-memory của port AnalyticsApi, cho test.

Mô phỏng đúng những thứ bảng điểm phải xử lý: số theo NGÀY giờ PT, độ trễ
(không có số sau `frontier`), truy vấn bị từ chối cả cục (400), báo cáo nguồn
traffic nhiều video một lần. Ghi lại mọi truy vấn để test kiểm cửa sổ ngày.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta

from factory.analytics import ReportRejected


class FakeAnalytics:
    def __init__(self, *, frontier: date, reject: set[str] | None = None,
                 reject_dimensions: set[str] | None = None):
        self.frontier = frontier
        self.reject = set(reject or ())
        self.reject_dimensions = set(reject_dimensions or ())
        self.videos: dict[str, dict] = {}
        self.daily: list[tuple[str, date, str, int, int, float]] = []
        self.queries: list[dict] = []
        self.search_terms: list[tuple[str, int]] = []   # (từ khoá, view) cho top_search_terms

    def add_video(self, video_id: str, *, privacy: str = "public", published_at: str | None = None,
                  publish_at: str | None = None, duration_s: int = 30) -> None:
        self.videos[video_id] = {"privacy": privacy, "published_at": published_at,
                                 "publish_at": publish_at, "duration_s": duration_s}

    def add_views(self, video_id: str, day: date, views: int, *, engaged: int | None = None,
                  source: str = "SHORTS", watch_s: float | None = None) -> None:
        engaged = views if engaged is None else engaged
        watch_s = views * 20.0 if watch_s is None else watch_s
        self.daily.append((video_id, day, source, views, engaged, watch_s))

    # ── port ─────────────────────────────────────────────────────────────
    def top_search_terms(self, *, start: date, end: date) -> list[dict]:
        self.queries.append({"start": start, "end": end, "metrics": "views",
                             "dimensions": "insightTrafficSourceDetail", "search": True})
        if "insightTrafficSourceDetail" in self.reject_dimensions:
            raise ReportRejected("400: insightTrafficSourceDetail")
        return [{"insightTrafficSourceDetail": t, "views": v} for t, v in self.search_terms[:25]]

    def video_facts(self, video_ids: list[str]) -> dict[str, dict]:
        return {v: dict(self.videos[v]) for v in video_ids if v in self.videos}

    def report(self, *, start: date, end: date, metrics: str, dimensions: str,
               video_ids: list[str] | None = None) -> list[dict]:
        self.queries.append({"start": start, "end": end, "metrics": metrics,
                             "dimensions": dimensions, "video_ids": list(video_ids or [])})
        wanted = metrics.split(",")
        if self.reject & set(wanted) or dimensions in self.reject_dimensions:
            raise ReportRejected(f"400: {metrics} / {dimensions}")
        rows = [r for r in self.daily if start <= r[1] <= min(end, self.frontier)
                and (video_ids is None or r[0] in video_ids)]
        keyf = {"day": lambda r: (r[1].isoformat(),),
                "video": lambda r: (r[0],),
                "insightTrafficSourceType": lambda r: (r[2],),
                "video,insightTrafficSourceType": lambda r: (r[0], r[2])}[dimensions]
        groups: dict[tuple, list] = defaultdict(list)
        if dimensions == "day" and video_ids is None:
            # Kênh thật (hàng nghìn video) ngày nào cũng có view: mọi ngày tới
            # frontier đều có dòng -- đó là cách đọc ra "Analytics có số tới đâu".
            d = start
            while d <= min(end, self.frontier):
                groups[(d.isoformat(),)]
                d += timedelta(days=1)
        for r in rows:
            groups[keyf(r)].append(r)
        out = []
        for key, rs in sorted(groups.items()):
            row = dict(zip(dimensions.split(","), key))
            views = sum(r[3] for r in rs)
            calc = {"views": views, "engagedViews": sum(r[4] for r in rs)}
            if views:
                avd = sum(r[5] for r in rs) / views
                calc["averageViewDuration"] = avd
                dur = self.videos.get(rs[0][0], {}).get("duration_s") or 30
                calc["averageViewPercentage"] = avd / dur * 100
            row.update({m: calc.get(m) for m in wanted})
            out.append(row)
        return out
