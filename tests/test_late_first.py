"""Lint "chữ đầu tiên đến muộn" + cổng toàn vẹn trước TTS (retro 2 mục 2, 3, 16).

Mục 2 lặp retro 1 mục 4 (luật "neo đầu câu" có mà không có công cụ) = LỖI QUY TRÌNH -> chặn bằng máy ở build_long.
"""
import contextlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "motion" / "long"), str(ROOT / "motion"), str(ROOT / "motion" / "stier"), str(ROOT)]
import build_long as BL  # noqa: E402
import script_lines as SL  # noqa: E402


def kin(t0, at, **kw):
    return {"type": "kinetic", "t0": t0, "t1": t0 + 6, "items": [{"text": "A", "at": at}, {"text": "B", "at": at + 1}], **kw}


def test_text_scene_without_background_must_show_something_within_one_second():
    late = BL.late_first([kin(10.0, 11.6)], "ch03")
    assert len(late) == 1 and "ch03 cảnh 0 kinetic" in late[0] and "1.6s" in late[0]
    assert BL.late_first([kin(10.0, 10.3)]) == []


def test_background_media_or_frame_scene_is_not_blank():
    assert BL.late_first([kin(10.0, 11.6, bg="turk")]) == []
    assert BL.late_first([{"type": "ledger", "t0": 0.0, "t1": 9, "title": "T", "rows": [{"k": "a", "v": "b", "at": 4.0}]}]) == []


def test_kinetic_line_later_than_two_seconds_is_pulled_forward_by_engine():
    assert BL.late_first([kin(10.0, 13.0)]) == []          # casewide.js: dòng đầu > 2 s -> hiện ở t0+0.5


def test_slam_waiting_for_last_word_is_flagged():
    s = {"type": "slam", "t0": 5.0, "t1": 9.0, "text": "MỘT TRÒ LỪA", "at": 7.1, "fx": "glitch"}
    assert BL.late_first([s]) and "slam" in BL.late_first([s])[0]


def test_counter_idle_at_zero_is_flagged_even_with_background():
    s = {"type": "counter", "t0": 0.0, "t1": 5.0, "from": 0, "to": 43, "prefix": "+", "suffix": "%", "at": 2.4, "bg": "x"}
    w = BL.late_first([s], "ch02")
    assert len(w) == 1 and "+0%" in w[0]
    assert BL.late_first([{**s, "at": 0.2}]) == []


@pytest.mark.parametrize("topic", ["mim-ai-voice", "ck-c2-phien-giao-dich"])
def test_calibrated_on_current_round(topic):
    if not (ROOT / "output" / "long" / topic / "ch00" / "data.js").exists():
        pytest.skip("chưa dựng html")
    assert BL.late_report(topic) == []


def test_render_refuses_late_scenes_unless_allowed(monkeypatch):
    calls = []
    monkeypatch.setattr(BL, "late_report", lambda topic, only=None: ["ch01 cảnh 4 slam: …"])
    monkeypatch.setattr(BL, "do_render", lambda *a, **k: calls.append(a))
    monkeypatch.setattr(BL, "render_lock", lambda label: contextlib.nullcontext())
    with pytest.raises(SystemExit, match="màn trống"):
        BL.cmd_render("t", None, [])
    assert calls == []
    BL.cmd_render("t", None, ["--allow-late"])
    assert len(calls) == 1


def _chs(*lines_per_ch):
    return [{"name": f"ch{i:02d}", "lines": list(ls)} for i, ls in enumerate(lines_per_ch)]


def test_script_gate_blocks_repeated_sentence_across_chapters():
    chs = _chs(["Mở đầu.", "Anh ta nghi ngờ."], ["Rồi sao?", {"t": "Anh ta nghi ngờ.", "p": 1.0}])
    bad = SL.gate(chs)
    assert len(bad) == 1 and "INT_REPEATED_SENTENCE" in bad[0] and "Anh ta nghi ngờ." in bad[0]
    assert SL.gate(chs, allow_repeat=True) == []


def test_script_gate_never_lets_markup_through():
    bad = SL.gate(_chs(["Xem https://example.com nhé."]), allow_repeat=True)
    assert bad and "url" in bad[0]


def test_script_gate_blocks_the_roadmap_cliche():
    """Retro 1 mục 14 (lặp ở A1, C1, D1, MIM #2): luật viết trong RETENTION.md + chốt bằng máy."""
    assert SL.gate(_chs(["Trong video này, mình cùng bạn trả lời ba câu hỏi."]))[0].startswith("ROADMAP_CLICHE [ch00]")
    assert SL.gate(_chs(["Video này trả lời 3 câu hỏi."]), allow_repeat=True)
    assert SL.gate(_chs(["Trước khi đoán, mình đi lại ba chặng đường."])) == []


def test_numbers_with_thousand_separators_are_not_sentence_breaks():
    """"Hơn 2.000 người." và "Còn 3.000 người." KHÔNG phải câu lặp ("000 người.") -- báo giả cũ ở kowloon/mafia."""
    assert SL.gate(_chs(["Hơn 2.000 người.", "Còn 3.000 người.", "Mất 1.000.000 đô la.", "Rồi 5.000.000 đô la."])) == []


@pytest.mark.parametrize("topic", ["mim-ai-voice", "ck-c2-phien-giao-dich", "ck-d1-vang-dinh", "mim-ai-jobs"])
def test_current_scripts_pass_the_gate(topic):
    md = ROOT / "data" / "long" / topic / "script.md"
    if not md.exists():
        pytest.skip("không có kịch bản")
    assert SL.gate(SL.parse(md.read_text(encoding="utf-8"))) == []


def test_build_long_tts_runs_the_gate():
    src = (ROOT / "motion" / "long" / "build_long.py").read_text(encoding="utf-8")
    assert 'if cmd in ("tts", "takes"):' in src and "integrity_gate(" in src
    with pytest.raises(SystemExit, match="integrity"):
        BL.integrity_gate([("ch00", {"lines": ["Một câu.", "Một câu."]})])
