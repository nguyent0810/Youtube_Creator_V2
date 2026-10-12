"""Mô tả YouTube ≤ 5000 ký tự: danh sách nguồn tự co cho vừa (D1 07/10/2026 bị chặn upload vì mô tả 8.199 ký tự)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion" / "long"))
import describe as D  # noqa: E402


def test_fit_keeps_all_sources_when_they_fit():
    src = ["CafeF 29/01/2026 — Tên bài: https://a.vn/x"]
    assert D.fit_sources(src, 1000) == src


def test_fit_drops_titles_before_dropping_sources():
    src = [f"Báo {i} 01/01/2026 — Một tiêu đề bài báo khá dài số {i}: https://b.vn/{i}" for i in range(5)]
    out = D.fit_sources(src, 200)
    assert out == [f"Báo {i} 01/01/2026: https://b.vn/{i}" for i in range(5)]


def test_fit_truncates_with_a_count_line_inside_budget():
    src = [f"Báo {i} 01/01/2026 — Tiêu đề: https://c.vn/{'x' * 60}{i}" for i in range(40)]
    out = D.fit_sources(src, 800)
    assert len("\n".join(out)) + 1 <= 800
    assert out[-1].startswith("…và ") and str(40 - (len(out) - 1)) in out[-1]
