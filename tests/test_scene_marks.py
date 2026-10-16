"""Dấu cảnh trong script.md, mốc neo, và cổng chống đọc/hình lặp."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion" / "long"))

import anchors
import craft
import scenes_from
import script_lines


MD = """## CH00 · Mở
Súng nổ. ‖ {date: 29.07.1967}
Ông nói. » muốn giữ quân đội thì phải buôn. {quote}
Mười sáu tấn trên lưng la. {counter: 16 | TẤN}
Vì sao bốn con vật vẫn ở lại? {question: Vì sao bốn con vẫn ở sông?}
Chương sáu. Mười sáu tấn. {chapter: 6 | MƯỜI SÁU TẤN}
Một nhát. {slam: NÉM BOM}
Câu không dấu thứ nhất đứng riêng.
Câu không dấu thứ hai cũng đứng riêng.
"""


def _chs():
    return script_lines.parse(MD)


def test_mark_strips_spoken_line_and_keeps_pause():
    line = _chs()[0]["lines"][0]
    assert line["t"] == "Súng nổ."
    assert line["p"] == 1.0
    spoken = " ".join(x if isinstance(x, str) else x["t"] for x in _chs()[0]["lines"])
    assert "{" not in spoken
    assert _chs()[0]["marks"][0]["raw"] == "date: 29.07.1967"


def test_quote_mark_lands_on_the_quoted_sentence():
    ch = _chs()[0]
    quote = next(m for m in ch["marks"] if m["raw"] == "quote")
    assert ch["lines"][quote["i"]]["q"] == 1
    assert "Muốn giữ" in ch["lines"][quote["i"]]["t"]


def test_scenes_from_table():
    ch = _chs()[0]
    sc = scenes_from.scenes_from(ch["lines"], ch["marks"])
    by = {s["type"]: s for s in sc}
    assert by["date"]["date"] == "29.07.1967"
    assert by["date"]["at"] == 0
    assert by["quote"]["qline"] == by["quote"]["at"]
    assert "Muốn giữ" in by["quote"]["text"]
    assert by["counter"]["to"] == 16 and by["counter"]["label"] == "TẤN"
    assert by["question"]["text"].endswith("?")
    assert by["chapter"]["no"] == "6" and "MƯỜI SÁU" in by["chapter"]["title"]
    assert by["slam"]["text"] == "NÉM BOM"
    assert anchors.check(ch["lines"], sc) == []


def test_date_with_label_splits_day_and_date():
    lines = ["Súng nổ."]
    sc = scenes_from.scenes_from(lines, [{"i": 0, "raw": "date: NHÃN | 29.07.1967"}])
    assert sc[0]["day"] == "NHÃN" and sc[0]["date"] == "29.07.1967"


def test_unmarked_chapter_is_all_kinetic():
    lines = ["Một câu dài ở đây.", "Câu thứ hai cũng vậy."]
    sc = scenes_from.scenes_from(lines, [])
    assert len(sc) == 2
    assert all(s["type"] == "kinetic" for s in sc)
    assert [s["at"] for s in sc] == [0, 1]
    assert scenes_from.unmarked_count(lines, []) == 2
    assert anchors.check(lines, sc) == []


def test_anchor_ok_then_one_missing_word():
    lines = [{"t": "Muốn giữ quân đội.", "q": 1}]
    ok = [{"type": "quote", "at": [0, "giữ"]}]
    assert anchors.check(lines, ok) == []
    bad = anchors.check(lines, [{"type": "quote", "at": [0, "không-có"]}])
    assert len(bad) == 1
    assert "không có chữ" in bad[0]
    assert "không-có" in bad[0]


def test_anchor_ignores_zoom_and_reads_nested_at():
    lines = ["Hà mã vẫn ở sông."]
    scenes = [{"type": "photo", "at": 0, "zoom": [0, "không-có"], "label": {"at": [0, "sông"], "k": "SÔNG"}}]
    assert anchors.check(lines, scenes) == []
    bad = anchors.check(lines, [{"label": {"at": [0, "tàu"]}}])
    assert len(bad) == 1 and "label" in bad[0]


def test_audio_craft_catches_long_sentence_and_quy_vi():
    words = " ".join(["từ"] * 36)
    chs = [{"name": "ch00", "lines": [words + "?", {"t": "Dạ quý vị.", "p": 1.0}, "Bạn thấy không?"]}]
    msgs = craft.audio_problems(chs)
    assert any("vượt 35" in m for m in msgs)
    assert any("quý vị" in m for m in msgs)


def test_audio_craft_wants_question_you_and_pause():
    chs = [{"name": "ch00", "lines": ["Một câu trần thuật.", "Câu nữa không hỏi."]}]
    msgs = " ".join(craft.audio_problems(chs))
    assert "câu hỏi" in msgs
    assert "bạn" in msgs
    assert "nghỉ dài" in msgs


def test_list_over_three_fails():
    lines = ["Một là tàu.", "Hai là sông.", "Ba là cầu.", "Bốn là chợ.", {"t": "Bạn thấy không?", "p": 1.0}]
    msgs = craft.audio_problems([{"name": "ch00", "lines": lines}])
    assert any("liệt kê" in m for m in msgs)


def test_graphic_run_and_missing_interrupt():
    kin = [{"type": "kinetic"}] * 6
    assert any("liên tiếp" in m for m in craft.graphic_problems("ch00", kin))
    assert any("không có cảnh ngắt" in m for m in craft.graphic_problems("ch00", kin))
    mixed = [{"type": "slam"}, *([{"type": "kinetic"}] * 3), {"type": "question"}]
    assert craft.graphic_problems("ch00", mixed) == []
