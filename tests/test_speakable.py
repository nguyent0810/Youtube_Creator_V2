"""Chặn markup sót NGAY TRƯỚC TTS ở hai bộ dựng chưa có cổng nào (bước 5).

run_batch đã chạy integrity trước TTS cho short thường; motion/stier (hồ sơ
S-tier) và motion/long (video dài) gọi thẳng engine.infer. Chỉ soi markup --
câu lặp ở đó có thể cố ý (câu chốt nhắc lại), và chỉ soi CHUỖI SẮP ĐỌC, không
soi spec (tiêu đề cảnh "*7 NGÀY*", nguồn có URL là hợp lệ).
"""
import sys
from pathlib import Path

import pytest

from factory import integrity

ROOT = Path(__file__).resolve().parents[1]


class Engine:
    def __init__(self):
        self.calls = []

    def infer(self, text, voice=None):
        import numpy as np
        self.calls.append(text)
        return np.zeros(240, dtype="float32")


def test_leftover_markup_ignores_deliberate_repetition():
    assert integrity.leftover_markup("Yakuza. Yakuza.") == []
    assert [f.code for f in integrity.leftover_markup("Xem https://x.vn nhé.")] == ["INT_LEFTOVER_MARKUP:url"]


@pytest.fixture
def long_mod(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "motion"))
    monkeypatch.syspath_prepend(str(ROOT / "motion" / "long"))
    import build_long
    eng = Engine()
    monkeypatch.setattr(build_long, "_engine", eng)
    return build_long, eng


def test_long_refuses_markup_before_the_engine_and_before_the_cache(long_mod, tmp_path):
    bl, eng = long_mod
    with pytest.raises(ValueError, match="markup"):
        bl.tts_line("Chương **một** bắt đầu.", tmp_path)
    assert eng.calls == [] and not list(tmp_path.glob("*.wav"))


def test_long_clean_line_is_spoken_once_then_cached(long_mod, tmp_path):
    bl, eng = long_mod
    bl.tts_line("Chương một bắt đầu.", tmp_path)
    bl.tts_line("Chương một bắt đầu.", tmp_path)
    assert eng.calls == ["Chương một bắt đầu."]


def test_stier_refuses_a_line_with_markup_before_speaking_anything(monkeypatch, tmp_path):
    monkeypatch.syspath_prepend(str(ROOT / "motion"))
    monkeypatch.syspath_prepend(str(ROOT / "motion" / "stier"))
    import build
    eng = Engine()
    monkeypatch.setattr(build, "_engine", eng)
    with pytest.raises(ValueError, match="markup"):
        build.speak(["Câu đầu sạch.", "Nguồn: https://vi.wikipedia.org"], tmp_path / "a.wav", tmp_path / "t.json")
    assert eng.calls == []


def test_a_bare_dien_y_tag_is_stripped_and_kept_as_a_flag(monkeypatch):
    # Lỗi thật (ripper ch12): script.md ghi "[DIỄN Ý]" không có ** -> parser chỉ bóc
    # "**[DIỄN Ý]**" nên nhãn lọt vào lời đọc, TTS đọc thành tiếng.
    monkeypatch.syspath_prepend(str(ROOT / "motion" / "long"))
    import script_lines
    md = "## CH01 · Mở\nCâu thường.\nTác giả nói vậy. [DIỄN Ý]\nCâu khác. **[DIỄN Ý]**\n"
    lines = script_lines.parse(md)[0]["lines"]
    assert lines[1] == {"t": "Tác giả nói vậy.", "diy": 1}
    assert lines[2] == {"t": "Câu khác.", "diy": 1}
    assert all(not integrity.leftover_markup(x["t"] if isinstance(x, dict) else x) for x in lines)


def test_no_long_chapter_on_disk_has_markup_in_a_spoken_line():
    import json
    bad = []
    for p in (ROOT / "data" / "long").glob("*/ch*.json"):
        for x in json.loads(p.read_text(encoding="utf-8")).get("lines", []):
            t = x["t"] if isinstance(x, dict) else x
            if integrity.leftover_markup(t):
                bad.append((p.parent.name, p.name, t[:60]))
    assert not bad, bad
