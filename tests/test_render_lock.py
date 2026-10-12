"""Hàng đợi render duy nhất (retro mục 9): người thứ hai chờ tới khi người thứ nhất nhả khoá."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from factory.render_lock import render_lock  # noqa: E402


def test_second_process_waits_for_the_first(tmp_path):
    lock = tmp_path / "r.lock"
    child = (f"import sys,time; sys.path.insert(0, r'{ROOT}'); from factory.render_lock import render_lock; "
             f"t=time.time()\nwith render_lock('child', poll=0.1, path=__import__('pathlib').Path(r'{lock}')): print(round(time.time()-t,1))")
    with render_lock("parent", poll=0.1, path=lock):
        # mã hoá cố định: con in "[render] chờ…" theo PYTHONIOENCODING của máy; đọc bằng cp1252 mặc định thì sập (retro 2 mục 7)
        p = subprocess.Popen([sys.executable, "-c", child], stdout=subprocess.PIPE, encoding="utf-8", errors="replace")
        time.sleep(1.5)
    out = p.communicate(timeout=20)[0]
    waited = float(out.strip().splitlines()[-1])
    assert waited >= 1.0                      # con phải chờ cha nhả khoá


def test_lock_is_reentrant_across_sequential_uses(tmp_path):
    lock = tmp_path / "r.lock"
    for _ in range(2):
        with render_lock("x", poll=0.1, path=lock):
            pass


def test_nested_use_in_one_process_does_not_block_itself(tmp_path):
    lock = tmp_path / "r.lock"
    with render_lock("outer", poll=0.1, path=lock):
        with render_lock("inner", poll=0.1, path=lock):   # build_long: cả lượt (ngoài) + từng chương (trong)
            pass
    with render_lock("again", poll=0.1, path=lock):        # đã nhả hẳn sau khi ra khỏi lớp ngoài
        pass
