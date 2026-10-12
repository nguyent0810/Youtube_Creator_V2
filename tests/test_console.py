"""Console cp1252 làm sập CLI khi in tiếng Việt (retro 2 mục 7 — lặp 2 lần trong một ngày: qa_blank, render_lock).

Một cách chung: factory.console.utf8_console() ở đầu MỌI entry point. Test chạy CLI thật với stdout cp1252 / không có
PYTHONIOENCODING, và quét mọi CLI để file mới không quên gọi.
"""
import ast
import io
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from factory.console import utf8_console  # noqa: E402

CLI_DIRS = ("scripts", "motion/long", "motion/stier")
MAIN = re.compile(r'^if __name__ == ["\']__main__["\']:\s*$', re.M)


def test_utf8_console_turns_cp1252_stream_into_utf8(monkeypatch):
    buf = io.BytesIO()
    out = io.TextIOWrapper(buf, encoding="cp1252")
    monkeypatch.setattr(sys, "stdout", out)
    utf8_console()
    print("TRỐNG Ầ Ẫ Ỵ Ệ Ở Ữ Ặ")
    out.flush()
    assert buf.getvalue().decode("utf-8").startswith("TRỐNG Ầ Ẫ Ỵ")


def test_utf8_console_ignores_streams_without_reconfigure(monkeypatch):
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    utf8_console()                       # không ném


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="cần ffmpeg trong PATH")
@pytest.mark.parametrize("pyioenc", ["cp1252", None])
def test_qa_blank_cli_prints_vietnamese_on_cp1252_console(tmp_path, pyioenc):
    vid = tmp_path / "blank.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=216x384:d=2", "-r", "10", str(vid)], check=True)
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    env["PYTHONUTF8"] = "0"
    if pyioenc:
        env["PYTHONIOENCODING"] = pyioenc
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "qa_blank.py"), str(vid)], env=env, capture_output=True, timeout=120)
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    out = r.stdout.decode("utf-8")
    assert "TRỐNG" in out and out.strip().splitlines()[-1].endswith("1 đoạn trống ≥ 1.0s")


def _is_cli(src: str) -> bool:
    if MAIN.search(src):
        return True
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print" for n in ast.walk(node)):
            return True
    return False


def test_every_cli_calls_utf8_console():
    missing = []
    for d in CLI_DIRS:
        for f in sorted((ROOT / d).glob("*.py")):
            src = f.read_text(encoding="utf-8")
            if _is_cli(src) and "utf8_console()" not in src:
                missing.append(str(f.relative_to(ROOT)))
    assert not missing, ("CLI in ra console mà không gọi factory.console.utf8_console() (console cp1252 sẽ làm sập khi in "
                         f"tiếng Việt): {missing}")


def test_no_adhoc_stdout_reconfigure():
    """reconfigure(encoding=...) không kèm errors= đặt lại errors='strict' -> lại sập. Chỉ một chỗ: factory/console.py."""
    bad = [str(f.relative_to(ROOT)) for d in CLI_DIRS + ("factory",) for f in (ROOT / d).glob("*.py")
           if f.name != "console.py" and "stdout.reconfigure(" in f.read_text(encoding="utf-8")]
    assert not bad, bad
