"""Gallery chữ có dấu khó (retro 2 mục 4 + 5, lặp retro 1 = LỖI QUY TRÌNH): mọi hiệu ứng chữ trong beat.js × theme lab/chart.

Không render ở đây (render đi qua factory/render_lock, PM chạy khi sửa engine). Test giữ cho gallery luôn PHỦ ĐỦ: thêm hiệu
ứng mới vào beat.js mà gallery không có là đỏ ngay.
"""
import inspect
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT / "motion" / "stier"), str(ROOT)]
import build_long as BL  # noqa: E402
import diacritics_gallery as G  # noqa: E402

HARD = set("ẦẪỴỆỞỮẶ")


def test_every_beat_and_slam_effect_is_in_both_themes():
    js = (ROOT / "motion" / "hf" / "assets" / "engine" / "beat.js").read_text(encoding="utf-8")
    beat_js = set(re.findall(r"^    (\w+): \(", js.split("const BEAT = {", 1)[1].split("\n  };", 1)[0], re.M))
    beat, slam = G.effects()
    assert set(beat) == beat_js and {"punch", "glitch", "zoom"} <= set(slam)
    for th in ("lab", "chart"):
        sc = G.build_case(th)["scenes"]
        assert {q["fx"] for s in sc if s["type"] == "kinetic" for q in s["items"]} == set(beat)
        assert {s["fx"] for s in sc if s["type"] == "slam"} == set(slam)
        assert {"chapter", "quote", "ledger", "bars", "timeline", "counter", "date", "question", "brand", "endcard"} <= {s["type"] for s in sc}


def test_every_text_effect_carries_the_hard_capitals():
    for s in G.build_case("lab")["scenes"]:
        if s["type"] == "kinetic":
            for q in s["items"]:
                assert len(HARD & set(q["text"])) >= 3, q
        if s["type"] == "slam":
            assert len(HARD & set(s["text"])) >= 4


def test_scenes_are_back_to_back_and_stills_are_inside_each_scene():
    case = G.build_case("chart")
    sc = case["scenes"]
    assert sc[0]["t0"] == 0 and all(a["t1"] == b["t0"] for a, b in zip(sc, sc[1:])) and sc[-1]["t1"] == case["dur"]
    for (label, t), s in zip(G.still_times(case), sc):
        assert s["t0"] < t < s["t1"] and label == s["gallery"]
    assert "label" not in sc[0] and next(s for s in sc if s["type"] == "counter")["label"].startswith("VIỆC LÀM")


def test_gallery_itself_has_no_late_first_text():
    assert BL.late_first(G.build_case("lab")["scenes"]) == []


def test_render_goes_through_the_render_lock_and_records_engine_hash():
    src = inspect.getsource(G.render)
    assert "with render_lock(" in src and "engine.sha" in src


def test_stale_until_rendered_with_current_engine(tmp_path):
    assert G.stale(tmp_path) == ["lab", "chart"]
    for th in ("lab", "chart"):
        (tmp_path / f"_diacritics_{th}").mkdir()
        (tmp_path / f"_diacritics_{th}" / "engine.sha").write_text(G.engine_hash(), encoding="utf-8")
    assert G.stale(tmp_path) == []
    (tmp_path / "_diacritics_lab" / "engine.sha").write_text("old", encoding="utf-8")
    assert G.stale(tmp_path) == ["lab"]
