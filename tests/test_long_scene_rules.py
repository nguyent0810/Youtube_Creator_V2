import importlib.util
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "motion" / "long" / "scene_rules.py"
SPEC = importlib.util.spec_from_file_location("scene_rules", MODULE)
scene_rules = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(scene_rules)


def timing(duration=16.0):
    return {
        "duration": duration,
        "segments": [
            {"index": 0, "start": 0.0, "end": 3.0},
            {"index": 1, "start": 3.0, "end": 6.0},
            {"index": 2, "start": 6.0, "end": 9.0},
            {"index": 3, "start": 9.0, "end": 12.0},
            {"index": 4, "start": 12.0, "end": duration},
        ],
    }


def test_default_in_is_an_actual_effect_and_repetition_gets_move_patch():
    result = scene_rules.analyze_chapter("ch00", [
        {"type": "photo", "at": 0, "img": "first"},
        {"type": "photo", "at": 1, "img": "second"},
        {"type": "slam", "at": 2, "text": "NEXT"},
    ], timing())
    proposals = result["proposals"]
    repeated = next(item for item in proposals if item["kind"] == "same_still_effect")
    assert repeated["effective_effect"] == repeated["previous_effect"] == "in"
    assert repeated["patch"] == {"move": "out"}
    assert "missing_motion" not in {item["kind"] for item in proposals}


def test_long_photo_gets_zoom_at_middle_and_splits_only_after_12_seconds():
    result = scene_rules.analyze_chapter("ch01", [
        {"type": "photo", "at": 0, "img": "one"},
    ], timing())
    proposals = result["proposals"]
    zoom = next(item for item in proposals if item["kind"] == "long_photo_zoom")
    assert zoom["duration_s"] == 16.0
    assert zoom["patch"]["zoom"]["at"] == 3
    split = next(item for item in proposals if item["kind"] == "split_still")
    assert [scene["at"] for scene in split["replacement_scenes"]] == [0, 2, 4]
    assert [scene.get("move") for scene in split["replacement_scenes"]] == [None, "out", "in"]


def test_8_to_12_second_print_gets_circles_but_never_a_split():
    result = scene_rules.analyze_chapter("ch02", [
        {"type": "print", "at": 0, "img": "document"},
        {"type": "slam", "at": 3, "text": "NEXT"},
    ], timing())
    proposals = result["proposals"]
    circle = next(item for item in proposals if item["kind"] == "long_print_circles")
    assert circle["duration_s"] == 9.0
    assert circle["patch"]["circles"][0]["at"] == 1
    assert "split_still" not in {item["kind"] for item in proposals}


def test_existing_zoom_uses_reveal_instead_of_a_second_zoom():
    result = scene_rules.analyze_chapter("ch03", [
        {"type": "photo", "at": 0, "img": "one", "zoom": {"x": 0.5}},
        {"type": "slam", "at": 3, "text": "NEXT"},
    ], timing())
    proposal = next(item for item in result["proposals"] if item["kind"] == "long_photo_reveal")
    assert proposal["patch"] == {"reveal": {"kind": "wipe", "at": 1, "d": 0.9}}
