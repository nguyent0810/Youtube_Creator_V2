import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import precommit_size as PS  # noqa: E402


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def test_checks_staged_blob_not_worktree_file(tmp_path):
    git(tmp_path, "init")
    p = tmp_path / "large.bin"
    p.write_bytes(b"x" * 11)
    git(tmp_path, "add", p.name)
    p.write_bytes(b"x")                 # worktree đổi sau git add: index vẫn là blob 11 bytes
    assert PS.oversized_staged(tmp_path, limit=10) == [("large.bin", 11)]


def test_ignores_small_staged_blob_and_reports_oversize(tmp_path, capsys):
    git(tmp_path, "init")
    (tmp_path / "small.bin").write_bytes(b"1234567890")
    git(tmp_path, "add", "small.bin")
    assert PS.oversized_staged(tmp_path, limit=10) == []
    (tmp_path / "large.bin").write_bytes(b"x" * (PS.LIMIT + 1))
    git(tmp_path, "add", "large.bin")
    assert PS.main(tmp_path) == 1
    assert "large.bin" in capsys.readouterr().err
