"""Phân loại lỗi đăng -- quyết định item bị HOÃN hay bị tính là HỎNG."""
from datetime import datetime, timezone

import pytest

from factory import publish


def test_429_is_quota_not_failure():
    with pytest.raises(publish.QuotaExceeded):
        publish._raise("upload", 429, "Video Uploads per day")


def test_403_quota_exceeded_body_is_quota():
    with pytest.raises(publish.QuotaExceeded):
        publish._raise("x", 403, '{"reason": "quotaExceeded"}')


def test_other_http_errors_are_real_failures():
    with pytest.raises(publish.PublishError) as e:
        publish._raise("x", 400, "invalid title")
    assert not isinstance(e.value, publish.QuotaExceeded)


def test_quota_reset_is_never_before_pacific_midnight():
    # 06:50 UTC ngày 20/09 -- đúng lúc tháng 12 dính 429. Reset thật 07:00.
    t = publish.next_quota_reset(datetime(2026, 9, 20, 6, 50, tzinfo=timezone.utc))
    assert t == "2026-09-20T08:05:00Z"
    t = publish.next_quota_reset(datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc))
    assert t == "2026-09-21T08:05:00Z"
