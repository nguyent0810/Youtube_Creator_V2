"""Vết hỏng do vá file qua heredoc bash (retro 2 mục 8 — lặp 3 lần: describe.py, gen_scenes.py, render_lock.py).

Heredoc/echo có dấu "\\" biến `\\1` trong regex thành ký tự điều khiển chr(1), `\\n` trong chuỗi thành xuống dòng thật
(vỡ cú pháp). Luật PM: chỉ vá .py/.js bằng Edit/Write. Test này bắt dấu vết nếu luật bị quên.
"""
import ast
import re
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _sources():
    pats = ["factory/**/*.py", "motion/*.py", "motion/long/*.py", "motion/stier/*.py", "scripts/*.py",
            "data/long/*/gen_scenes.py", "motion/hf/assets/engine/*.js", "tests/*.py"]
    for p in pats:
        yield from ROOT.glob(p)


def test_no_control_characters_in_source():
    bad = [str(f.relative_to(ROOT)) for f in _sources() if CTRL.search(f.read_text(encoding="utf-8"))]
    assert not bad, f"ký tự điều khiển trong mã nguồn (vết heredoc làm hỏng '\\1', '\\t'...): {bad}"


def test_every_python_source_parses():
    bad = []
    for f in _sources():
        if f.suffix != ".py":
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                ast.parse(f.read_text(encoding="utf-8"))
            except SyntaxError as e:
                bad.append(f"{f.relative_to(ROOT)}:{e.lineno} {e.msg}")
    assert not bad, bad
