import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "motion" / "long"))
import branch_gate as BG  # noqa: E402
import build_long as BL  # noqa: E402


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def commit(repo, name, text):
    (repo / name).write_text(text, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", name)


def test_branch_gate_accepts_head_containing_origin_main(tmp_path):
    git(tmp_path, "init")
    commit(tmp_path, "base.txt", "base")
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "HEAD")
    assert BG.problem(tmp_path) is None


def test_branch_gate_rejects_missing_or_newer_origin_main(tmp_path):
    git(tmp_path, "init")
    assert "không có ref origin/main" in BG.problem(tmp_path)
    commit(tmp_path, "base.txt", "base")
    git(tmp_path, "branch", "local")
    git(tmp_path, "checkout", "-b", "remote-main")
    commit(tmp_path, "main.txt", "new main")
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(tmp_path, "checkout", "local")
    assert "git fetch origin && git merge origin/main" in BG.problem(tmp_path)
    with pytest.raises(SystemExit, match="chặn nhánh"):
        BG.refuse(tmp_path)


def test_branch_gate_rejects_non_repository(tmp_path):
    assert "không phải repository Git" in BG.problem(tmp_path)


def test_final_commit_records_head_dirty_state_and_time(tmp_path, monkeypatch):
    git(tmp_path, "init")
    commit(tmp_path, "base.txt", "base")
    out = tmp_path / "output"
    out.mkdir()
    (out / "x.txt").write_text("untracked", encoding="utf-8")  # git bỏ qua thư mục rỗng
    monkeypatch.setattr(BL, "ROOT", tmp_path)
    BL._write_final_commit(out)
    mark = (out / "final.commit").read_text(encoding="utf-8")
    assert f"commit: {git(tmp_path, 'rev-parse', 'HEAD')}" in mark
    assert "working_tree: dirty" in mark and "created_at: " in mark


def test_final_commit_records_clean_working_tree(tmp_path, monkeypatch):
    git(tmp_path, "init")
    commit(tmp_path, "base.txt", "base")
    out = tmp_path / "output"
    out.mkdir()
    monkeypatch.setattr(BL, "ROOT", tmp_path)
    BL._write_final_commit(out)
    mark = (out / "final.commit").read_text(encoding="utf-8")
    assert "working_tree: clean" in mark
