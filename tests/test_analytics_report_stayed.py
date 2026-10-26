"""scripts/analytics_report.py: cột % ở lại (engagedViews / views)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _mod():
    spec = importlib.util.spec_from_file_location("analytics_report", ROOT / "scripts" / "analytics_report.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def vid(slug, views, engaged, avp=60.0):
    return {"slug": slug, "views": views, "engaged": engaged, "avp": avp, "curve": None, "sources": {}}


def test_summary_prints_median_stayed_and_count_reaching_45_percent():
    out = "\n".join(_mod().summarize("CK", [
        vid("ck-a", 2900, 1421), vid("ck-b", 1000, 200), vid("ck-c", 1000, 300),
        vid("ck-it-view", 20, 19),                     # < 50 view: không tính
        vid("ck-thieu", 1000, None),                   # engagedViews bị từ chối: không tính
    ]))
    assert "%ở lại" in out
    assert "% ở lại trung vị 30%; 1/3 video đạt 45%" in out
    assert out.index("ck-a (49%, 2900)") < out.index("Ở lại thấp nhất")
    assert "ck-it-view (" not in out.split("Top view")[1].split("\n")[1]
