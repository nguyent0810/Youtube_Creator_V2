"""Chặn render/final/publish khi HEAD chưa chứa ``origin/main``.

Không tự fetch hay merge: người dựng phải đồng bộ nhánh trước, để các cổng
mới trên main không bị bỏ qua bởi một working tree cũ.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def problem(root: Path = ROOT) -> str | None:
    """Trả lỗi cổng, hoặc ``None`` khi ``origin/main`` đã là tổ tiên HEAD."""
    try:
        repo = _git(root, "rev-parse", "--is-inside-work-tree")
    except OSError as e:
        return f"không chạy được git: {e}"
    if repo.returncode != 0 or repo.stdout.strip() != "true":
        return f"{root}: không phải repository Git; không kiểm được origin/main"
    ref = _git(root, "rev-parse", "--verify", "--quiet", "origin/main")
    if ref.returncode != 0:
        return "không có ref origin/main; hãy git fetch origin rồi kiểm lại"
    merged = _git(root, "merge-base", "--is-ancestor", "origin/main", "HEAD")
    if merged.returncode == 0:
        return None
    if merged.returncode == 1:
        return "HEAD chưa chứa origin/main; chạy: git fetch origin && git merge origin/main"
    detail = (merged.stderr or merged.stdout).strip()
    return f"không kiểm được quan hệ origin/main và HEAD{': ' + detail if detail else ''}"


def refuse(root: Path = ROOT) -> None:
    """Dừng pipeline khi nhánh thiếu main; không có cờ bỏ qua."""
    bad = problem(root)
    if bad:
        raise SystemExit("chặn nhánh: " + bad)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()
    refuse()
    print("branch_gate: ĐẠT (HEAD đã chứa origin/main)")
