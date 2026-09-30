import pytest


@pytest.fixture(autouse=True)
def _no_channel_titles(monkeypatch, request):
    """Test không phụ thuộc tiêu đề THẬT trên kênh (data/channel_titles thay đổi
    theo ngày). Test nào cần thì tự nạp dữ liệu giả."""
    if "real_titles" in request.keywords:
        return
    from factory.lines import novelty
    monkeypatch.setattr(novelty, "_load", lambda ch: ([], frozenset()))
