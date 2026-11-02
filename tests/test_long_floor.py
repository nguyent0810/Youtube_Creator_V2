"""Hồi quy sàn Long theo kênh, hoàn toàn dùng dữ liệu giả."""
from __future__ import annotations

from unittest.mock import patch

from motion.long import floor


def _coverage(percent: float, longest_run: float) -> dict:
    return {"text_only_percent": percent, "longest_text_only_run_s": longest_run}


def _published_cl() -> list[tuple[str, dict]]:
    """Một fixture đạt đúng các ngưỡng CL cũ, không đọc Long thật."""
    scene_types = ["photo", "map", "file", "split", "ledger", "bars", "sketch",
                   "broll", "timeline", "org", "print", "date", "counter", "question"]
    scenes = [{"type": scene_types[index % len(scene_types)], "img": f"img-{index}"}
              for index in range(40)]
    scenes.extend({"type": "broll", "vid": f"clip-{index}"} for index in range(30))
    scenes.extend({"type": "kinetic", **({"img": f"kinetic-{index}"} if index < 20 else {})}
                  for index in range(30))
    return [(f"ch{index:02d}", {"lines": ["lời"] * 500, "scenes": scenes if index == 0 else []})
            for index in range(10)]


def test_published_style_cl_passes_unchanged_floor() -> None:
    assert floor.problems(_published_cl()) == []


def test_october_incident_cl_fails_for_short_script_blank_text_and_auto() -> None:
    scenes = [{"type": "kinetic", "auto": index == 0} for index in range(94)]
    scenes.extend({"type": "photo", "img": f"img-{index}"} for index in range(6))
    problems = floor.problems([("ch00", {"lines": ["lời"] * 1500, "scenes": scenes})])
    assert any("1500 âm tiết" in problem for problem in problems)
    assert any("94% cảnh là chữ trên nền trống" in problem for problem in problems)
    assert any('"auto"' in problem for problem in problems)


def test_mim_rejects_twenty_five_percent_empty_background() -> None:
    with patch.object(floor, "_coverage_report", return_value=_coverage(25, 10)):
        problems = floor.problems([("ch00", {"scenes": [{"type": "bars"}]})], "MIM", "mim-fake")
    assert any("25.00% > 22%" in problem for problem in problems)


def test_mim_rejects_twenty_second_text_run_at_twenty_percent() -> None:
    with patch.object(floor, "_coverage_report", return_value=_coverage(20, 20)):
        problems = floor.problems([("ch00", {"scenes": [{"type": "bars"}]})], "MIM", "mim-fake")
    assert any("20.00s > 17s" in problem for problem in problems)


def test_mim_accepts_twenty_percent_and_ten_second_text_run() -> None:
    with patch.object(floor, "_coverage_report", return_value=_coverage(20, 10)):
        assert floor.problems([("ch00", {"scenes": [{"type": "bars"}]})], "MIM", "mim-fake") == []


def test_mim_requires_timing() -> None:
    problems = floor.problems([("ch00", {"scenes": [{"type": "bars"}]})], "MIM")
    assert problems == ["chưa có timing"]


def test_mim_auto_scene_always_fails() -> None:
    with patch.object(floor, "_coverage_report", return_value=_coverage(0, 0)):
        problems = floor.problems([("ch00", {"scenes": [{"type": "bars", "auto": True}]})], "MIM", "mim-fake")
    assert any('"auto"' in problem for problem in problems)


def test_ck_uses_the_same_content_floor_as_mim() -> None:
    with patch.object(floor, "_coverage_report", return_value=_coverage(25, 18)):
        problems = floor.problems([("ch00", {"scenes": [{"type": "bars"}]})], "CK", "ck-fake")
    assert any("25.00% > 22%" in problem for problem in problems)
    assert any("18.00s > 17s" in problem for problem in problems)


def test_missing_channel_keeps_cl_floor() -> None:
    assert floor.problems(_published_cl()) == []
