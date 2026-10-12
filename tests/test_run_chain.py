"""Chuỗi .sh chạy bản chụp + một bản mỗi chuỗi (retro 2 mục 18: sửa publish_d1.sh khi bản cũ còn chạy -> bản cũ đọc lệch,
đăng 2 Short D1 trước video dài)."""
import importlib.util
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_chain", ROOT / "scripts" / "run_chain.py")
RC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RC)

try:
    BASH = RC.bash()
except SystemExit:
    BASH = None
pytestmark = pytest.mark.skipif(BASH is None, reason="cần bash")


def _child(script, log, base):
    code = (f"import importlib.util,sys; s=importlib.util.spec_from_file_location('rc', r'{ROOT / 'scripts' / 'run_chain.py'}'); "
            f"m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
            f"sys.exit(m.run(__import__('pathlib').Path(r'{script}'), __import__('pathlib').Path(r'{log}'), __import__('pathlib').Path(r'{base}')))")
    return subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_editing_the_script_while_it_runs_does_not_change_the_running_chain(tmp_path):
    sh, log, base = tmp_path / "chain.sh", tmp_path / "chain.log", tmp_path / "chains"
    sh.write_text("sleep 2\necho BAN-GOC\n", encoding="utf-8", newline="\n")
    p = _child(sh, log, base)
    time.sleep(1.0)
    sh.write_text("echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\necho DA-SUA\n", encoding="utf-8", newline="\n")
    p.communicate(timeout=60)
    out = log.read_text(encoding="utf-8")
    assert "BAN-GOC" in out and "DA-SUA" not in out and "XXX" not in out
    assert len(list(base.glob("chain.*.sh"))) == 1


def test_second_instance_of_the_same_chain_is_refused(tmp_path):
    sh, log, base = tmp_path / "chain.sh", tmp_path / "chain.log", tmp_path / "chains"
    sh.write_text("sleep 3\necho XONG\n", encoding="utf-8", newline="\n")
    p = _child(sh, log, base)
    time.sleep(1.0)
    with pytest.raises(SystemExit, match="ĐANG CHẠY"):
        RC.run(sh, log, base)
    p.communicate(timeout=60)
    assert p.returncode == 0 and log.read_text(encoding="utf-8").count("XONG") == 1
