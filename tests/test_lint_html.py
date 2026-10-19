"""Bốn kiểm tra cơ học của bước html: mực con dấu, con dấu trong thẻ, tiêu đề thẻ, HDR."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion" / "long"))
import lint_html as L

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "long"
OUT = ROOT / "output" / "long"


def _file(**kw):
    scene = {"type": "file", "name": "CHIẾN DỊCH\nGIẤY", "k": "HỒ SƠ", "desc": "Operation Paper",
             "rows": [{"k": "A", "v": "1"}, {"k": "B", "v": "2"}, {"k": "C", "v": "3"}]}
    scene.update(kw)
    return scene


def _stamp(text="MẬT", **kw):
    stamp = {"text": text, "ink": True, "x": 960, "y": 600}
    stamp.update(kw)
    return stamp


def test_fsz_matches_engine():
    # fsz("MẬT", 84, 760, 0.72): 3 ký tự, 84 vẫn dưới ngưỡng co.
    assert L.fsz("MẬT", 84, 760, 0.72) == 84
    assert L.fsz("LONG QUYỂN PHONG", 100, 860, 0.58) == int(860 / (16 * 0.58))


def test_ink_stamp_inside_card_passes():
    assert L.check_scenes("ch03", [_file(stamp=_stamp())]) == []


def test_file_stamp_without_ink_fails():
    msgs = L.check_scenes("ch03", [_file(stamp=_stamp(ink=False))])
    assert any("stamp.ink" in m for m in msgs)


def test_stamp_on_a_photo_may_skip_ink():
    scene = {"type": "photo", "stamp": {"text": "MẬT", "x": 200, "y": 200}}
    assert L.check_scenes("ch01", [scene]) == []


def test_default_stamp_on_a_plain_card_is_outside():
    # Toạ độ mặc định của engine (1150, 560) trên thẻ không ảnh (x 460–1460).
    scene = _file(stamp={"text": "HƯ CẤU", "at": 1.0}, t0=0.0, t1=8.0)
    msgs = L.check_scenes("ch12", [scene])
    assert any("tràn khỏi thẻ" in m for m in msgs)
    assert any("stamp.ink" in m for m in msgs)


def test_title_that_would_wrap_fails_and_a_broken_line_passes():
    long = _file(name="LONG QUYỂN PHONG", stamp=_stamp())
    assert any("xuống dòng" in m for m in L.check_scenes("ch12", [long]))
    broken = _file(name="LONG QUYỂN\nPHONG", stamp=_stamp())
    assert L.check_scenes("ch12", [broken]) == []


def test_hdr_tags():
    assert L.hdr_reason({"color_transfer": "bt709", "color_primaries": "bt709", "color_space": "bt709"}) is None
    assert L.hdr_reason({"color_transfer": "unknown", "color_primaries": "unknown"}) is None
    assert L.hdr_reason({"color_transfer": "smpte170m", "color_primaries": "bt709", "color_space": "smpte170m"}) is None
    assert "smpte2084" in L.hdr_reason({"color_transfer": "smpte2084", "color_primaries": "bt2020"})
    msg = L.hdr_problem("ch02", 3, "12345", {"color_transfer": "arib-std-b67"})
    assert "12345" in msg and "HDR" in msg
    assert L.hdr_problem("ch02", 3, "9", {"_error": "boom"}) == "ch02 cảnh 3: không đọc được màu của clip 9 (boom)."


def test_published_golden_file_cards_pass():
    """Tam Giác Vàng đã soi contact sheet và chấp nhận. Lint không được bắt lại những thẻ đó."""
    for ch in sorted((DATA / "golden").glob("ch*.json")):
        data = json.loads(ch.read_text(encoding="utf-8"))
        dj = OUT / "golden" / ch.stem / "data.js"
        if not dj.exists():
            pytest.skip("chưa có data.js của golden")
        text = dj.read_text(encoding="utf-8")
        case = json.loads(text[len("window.CASE = "):].rstrip().rstrip(";"))
        scenes = data["scenes"]
        for i, planned in enumerate(case["scenes"]):
            if i >= len(scenes) or scenes[i].get("type") != "file":
                continue
            scenes[i]["t0"] = planned.get("t0")
            scenes[i]["t1"] = planned.get("t1")
            if scenes[i].get("stamp") and isinstance(planned.get("stamp"), dict):
                scenes[i]["stamp"]["at"] = planned["stamp"].get("at")
        assert L.check_scenes(ch.stem, scenes) == []
