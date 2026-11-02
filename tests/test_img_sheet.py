import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long")]
import img_sheet as IS  # noqa: E402


def test_image_hash_is_stable_and_focus_change_invalidates_it():
    uses = [{"key": "portrait", "focus": [0.2, 0.3]}, {"key": "paper", "focus": None}]
    assert IS.uses_hash(uses) == IS.uses_hash(list(reversed(uses)))
    assert IS.uses_hash(uses) != IS.uses_hash([{**uses[0], "focus": [0.7, 0.3]}, uses[1]])


def test_jobs_sheet_inventory_has_background_print_and_no_old_nextcube():
    uses = IS.image_uses(ROOT / "data" / "long" / "mim-jobs-1985")
    assert any(x["type"] == "chapter" and x["field"] == "bg" for x in uses)
    assert any(x["type"] == "print" for x in uses)
    assert "nextcube" not in {x["key"] for x in uses}


def test_crop_box_matches_cover_focus_math():
    left, top, right, bottom = IS.crop_box((1000, 2000), [0.5, 0.2])
    assert (left, right) == (0, 1000)
    assert round(top, 2) == 118.75
    assert round(bottom - top, 2) == 562.5
