import importlib.util
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "motion" / "long" / "scene_params.py"
SPEC = importlib.util.spec_from_file_location("scene_params", MODULE)
scene_params = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(scene_params)


def check(scenes, imgs=None, theme=None, **kwargs):
    return scene_params.validate_topic([("ch00", scenes)], imgs or {}, theme, **kwargs)


def test_known_casewide_keys_and_a_valid_scene_pass():
    result = check([
        {"type": "print", "t0": 0, "t1": 3, "img": "portrait", "maxW": 760, "maxH": 700,
         "side": {"k": "HỒ SƠ", "h": "TÊN", "lines": [{"text": "DÒNG", "at": 1}]}},
        {"type": "kinetic", "t0": 3, "t1": 6, "items": [{"text": "AMELIO", "at": 3.2}], "accent": "AMELIO", "lay": "stack"},
    ], {"portrait": "File:portrait"})
    assert result["errors"] == []


def test_print_head_and_tiny_dimensions_are_blocking():
    result = check([{"type": "print", "t0": 0, "t1": 3, "img": "x", "head": "MẤT", "maxH": 0.52}])
    assert any("head của print bị engine bỏ qua" in item for item in result["errors"])
    assert any("maxH phải là số pixel >= 50" in item for item in result["errors"])


def test_sculley_regression_array_pos_and_small_maxh_are_blocking():
    result = check([{"type": "print", "t0": 0, "t1": 3, "img": "sculley", "pos": [0.5, 0.2], "maxH": 0.52}])
    assert any("pos phải là chuỗi CSS" in item for item in result["errors"])
    assert any("maxH phải là số pixel >= 50" in item for item in result["errors"])


def test_focus_type_kinetic_accent_and_quote_label_are_checked():
    result = check([
        {"type": "photo", "t0": 0, "t1": 3, "img": "a", "focus": "50% 20%"},
        {"type": "kinetic", "t0": 3, "t1": 6, "items": [{"text": "MÁY TÍNH", "at": 3.1}], "accent": "AMELIO"},
        {"type": "quote", "t0": 6, "t1": 9, "text": "x", "at": 6.1, "typeDur": 1, "label": "TRÍCH"},
    ])
    assert any("focus phải là [x, y]" in item for item in result["errors"])
    assert any("accent kinetic 'AMELIO'" in item for item in result["errors"])
    assert any("label phải là object" in item for item in result["errors"])


def test_duration_bounds_and_image_usage_are_blocking_without_exceptions():
    result = check([
        {"type": "chapter", "t0": 0, "t1": 2.4, "no": "1", "title": "X"},
        {"type": "endcard", "t0": 2.4, "t1": 11.5},
        {"type": "photo", "t0": 11.5, "t1": 14.5, "img": "used"},
    ], {"used": "File:used", "orphan": "File:orphan"})
    assert sum("thời lượng" in item for item in result["errors"]) == 2
    assert any("ảnh 'orphan' không có cảnh nào dùng" in item for item in result["errors"])


def test_ledger_rows_plus_total_follow_css_caption_limit():
    rows = [{"k": str(i), "v": str(i), "at": i / 10} for i in range(6)]
    passing = check([{"type": "ledger", "t0": 0, "t1": 3, "rows": rows}], theme="chart")
    failing = check([{"type": "ledger", "t0": 0, "t1": 3, "rows": rows, "total": {"k": "T", "v": "6", "at": 1}}], theme="chart")
    assert passing["errors"] == []
    assert any("7 dòng (rows + total), tối đa 6" in item for item in failing["errors"])


def test_theme_owned_type_is_a_warning_not_a_guessed_contract():
    result = check([{"type": "race", "t0": 0, "t1": 3, "title": "X", "mystery": 1}])
    assert result["errors"] == []
    assert len(result["warnings"]) == 1


def test_planned_aliases_and_string_labels_pass_with_counter_image():
    result = check([
        {"type": "slam", "t0": 0, "t1": 3, "text": "X", "at": 0.2},
        {"type": "quote", "t0": 3, "t1": 6, "text": "X", "at": 3.2, "typeDur": 1},
        {"type": "counter", "t0": 6, "t1": 9, "to": 100, "at": 6.2, "img": "portrait"},
        {"type": "calendar", "t0": 9, "t1": 12, "from": "2020", "days": 3, "label": "THÁNG"},
        {"type": "seismo", "t0": 12, "t1": 15, "read": "X", "hit": "Y", "label": "RUNG"},
    ], {"portrait": "File:portrait"})
    assert result["errors"] == []


def test_raw_aliases_are_only_checked_after_plan():
    raw = [
        {"type": "slam", "hitAt": [0, "x"]},
        {"type": "quote", "text": "x", "typeAt": [0, "x"]},
        {"type": "counter", "to": 100, "countAt": [0, "x"], "img": "portrait"},
        {"type": "calendar", "from": "2020", "days": 3, "label": "THÁNG"},
        {"type": "seismo", "read": "x", "hit": "y", "label": "RUNG"},
    ]
    assert check(raw, {"portrait": "File:portrait"}, check_scenes=False)["errors"] == []
    planned = [
        {"type": "slam", "at": 0.2, "t0": 0, "t1": 3},
        {"type": "quote", "text": "x", "at": 3.2, "t0": 3, "t1": 6},
        {"type": "counter", "to": 100, "at": 6.2, "img": "portrait", "t0": 6, "t1": 9},
        {"type": "calendar", "from": "2020", "days": 3, "label": "THÁNG", "t0": 9, "t1": 12},
        {"type": "seismo", "read": "x", "hit": "y", "label": "RUNG", "t0": 12, "t1": 15},
    ]
    assert check(planned, {"portrait": "File:portrait"})["errors"] == []
