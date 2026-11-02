"""Chặn commit có blob *đang staged* lớn hơn 50 MB.

Chỉ đọc index qua ``:<path>`` thay vì stat file trên đĩa: một file có thể đã
bị sửa hoặc xoá sau ``git add`` mà blob chuẩn bị commit vẫn còn lớn.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIMIT = 50 * 1024 * 1024


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True)


def oversized_staged(root: Path = ROOT, limit: int = LIMIT) -> list[tuple[str, int]]:
    """Các file thêm/sửa trong index có blob vượt ``limit`` bytes."""
    changed = _git(root, "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR")
    if changed.returncode != 0:
        raise RuntimeError(changed.stderr.decode("utf-8", "replace").strip() or "không đọc được Git index")
    bad = []
    for raw in changed.stdout.split(b"\0"):
        if not raw:
            continue
        name = raw.decode("utf-8", "surrogateescape")
        blob = _git(root, "cat-file", "-s", f":{name}")
        if blob.returncode != 0:
            raise RuntimeError(f"không đọc được blob staged: {name}")
        size = int(blob.stdout.strip())
        if size > limit:
            bad.append((name, size))
    return bad


def main(root: Path = ROOT) -> int:
    try:
        bad = oversized_staged(root)
    except RuntimeError as e:
        print(f"pre-commit: {e}", file=sys.stderr)
        return 1
    if not bad:
        return 0
    print("pre-commit: chặn blob staged > 50 MB:", file=sys.stderr)
    for name, size in bad:
        print(f"  {name}: {size} bytes", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()
    sys.exit(main())
