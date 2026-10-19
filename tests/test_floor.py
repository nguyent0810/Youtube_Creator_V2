"""Sàn sản xuất của Long: 6 video đã đăng phải qua, 4 video hỏng ngày 11/10/2026 phải bị chặn."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "motion" / "long"))

import floor
import scenes_from


def _load(topic):
    d = ROOT / "data" / "long" / topic
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    return [(n, json.loads((d / f"{n}.json").read_text(encoding="utf-8"))) for n in spec["chapters"]]


@pytest.mark.parametrize("topic", ["yakuza", "mafia", "shanghai", "ripper", "kowloon", "golden"])
def test_published_longs_pass_the_floor(topic):
    assert floor.problems(_load(topic)) == []


def _text_only_video(n_lines=200, words=10):
    lines = [" ".join(["chữ"] * words) for _ in range(n_lines)]
    return [(f"ch{i:02d}", {"lines": lines[i::10], "scenes": scenes_from.scenes_from(lines[i::10], [])}) for i in range(10)]


def test_auto_kinetic_draft_is_refused():
    bad = floor.problems(_text_only_video())
    assert any("auto" in x for x in bad)
    assert any("ảnh tư liệu" in x for x in bad)
    assert any("b-roll" in x for x in bad)
    assert any("nền trống" in x for x in bad)


def test_short_script_is_refused():
    chs = _load("golden")
    short = [(n, {**c, "lines": c["lines"][:5]}) for n, c in chs]
    assert any("âm tiết" in x for x in floor.problems(short))


def test_scenes_from_marks_unmarked_lines_as_draft():
    sc = scenes_from.scenes_from(["Câu không dấu đứng riêng một mình."], [])
    assert sc[0]["type"] == "kinetic" and sc[0]["auto"] is True
