"""26/10/2026: đợt 1 học từ vietneu-tts (docs/pm/2026-10-26-tai-danh-gia-workflow-ai-learning.md) -- khoá năm counter,
limiter đỉnh thật, render_key băm ảnh."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "motion"))
sys.path.insert(0, str(ROOT / "motion" / "long"))
from long.studio_lint import year_counter_issues  # noqa: E402
import build_long  # noqa: E402

ENGINE = ROOT / "motion" / "hf" / "assets" / "engine"


def test_year_counter_must_declare():
    turing = {"type": "counter", "from": 1950, "to": 2000, "label": "NĂM TURING HẸN"}
    assert year_counter_issues([turing])                                   # Short Turing hiện "1.996"
    assert not year_counter_issues([{**turing, "year": True}])
    assert not year_counter_issues([{"type": "counter", "to": 2000, "year": False}])   # yakuza: số lượng
    assert not year_counter_issues([{"type": "counter", "to": 2000, "suffix": " NGƯỜI"}])
    assert not year_counter_issues([{"type": "counter", "to": 85}, {"type": "slam", "to": 1990}])


def test_engines_skip_thousands_dot_for_year():
    for n in ("casewide.js", "casefile.js"):
        assert '(s.year ? a : a.replace(' in (ENGINE / n).read_text(encoding="utf-8"), n


def test_final_mix_has_true_peak_limiter():
    for f in ("motion/long/build_long.py", "motion/stier/build.py", "motion/stier/themes.py"):
        t = (ROOT / f).read_text(encoding="utf-8")
        assert t.count("loudnorm=I=-14") == t.count("alimiter=limit=0.78:level=0"), f


def test_render_key_changes_when_image_replaced(tmp_path, monkeypatch):
    hf = tmp_path / "hf"
    (hf / "compositions" / "long").mkdir(parents=True)
    (hf / "assets" / "engine").mkdir(parents=True)
    for n in ("casewide.js", "casewide.css", "beat.js", "beat.css"):
        (hf / "assets" / "engine" / n).write_text(n)
    (hf / "compositions" / "long" / "t_ch01.html").write_text("<html></html>")
    img = hf / "assets" / "long" / "t" / "img" / "a.jpg"
    img.parent.mkdir(parents=True)
    img.write_bytes(b"cu")
    od = tmp_path / "out"
    (od / "ch01").mkdir(parents=True)
    (od / "ch01" / "data.js").write_text('D={img:"assets/long/t/img/a.jpg"}')
    monkeypatch.setattr(build_long, "HF", hf)
    k1 = build_long.render_key("t", "ch01", od, False)
    img.write_bytes(b"moi")
    assert build_long.render_key("t", "ch01", od, False) != k1
