"""Kiểm mốc neo của một chương giả lập. Không đọc, không ghi data/long.

Mốc hợp lệ, đúng README:

- số nguyên ``i``: đầu câu i
- ``[i, "từ"]`` hoặc ``[i, "từ", n, lệch]``: chữ đó có trong câu i
- ``[i, null, 0, lệch]``: đầu câu i
- số thực: giây tuyệt đối, không soi chữ

``zoom`` không tính. Soi ``at``, ``titleAt``, ``hitAt``, ``countAt``, ``hAt`` ở mọi tầng,
kể cả ``at`` trong ``rows`` / ``kin`` / ``stamp`` / ``label`` / ``side.lines`` / ``items``.
"""
from __future__ import annotations

import re
import unicodedata

_KEYS = {"at", "titleAt", "hitAt", "countAt", "hAt"}


def norm(w: str) -> str:
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", str(w).lower()))


def line_text(line) -> str:
    return line if isinstance(line, str) else line.get("t", "")


def _word_hit(line, word, n: int) -> bool:
    seen = 0
    for tok in line_text(line).split():
        if norm(tok) == norm(word):
            if seen == n:
                return True
            seen += 1
    return False


def _one(lines, anchor, field: str) -> str | None:
    if isinstance(anchor, bool) or not isinstance(anchor, (int, float, list)):
        return f"mốc lạ {anchor!r}, trường {field}"
    if isinstance(anchor, float):
        return None
    if isinstance(anchor, int):
        if anchor < 0 or anchor >= len(lines):
            return f"câu {anchor} vượt ngoài kịch bản ({len(lines)} câu), trường {field}"
        return None
    if not anchor or isinstance(anchor[0], bool) or not isinstance(anchor[0], int):
        return f"mốc lạ {anchor!r}, trường {field}"
    i = anchor[0]
    if i < 0 or i >= len(lines):
        return f"câu {i} vượt ngoài kịch bản ({len(lines)} câu), trường {field}"
    word = anchor[1] if len(anchor) > 1 else None
    if word is None:
        return None
    n = anchor[2] if len(anchor) > 2 and anchor[2] is not None else 0
    if not isinstance(n, int) or isinstance(n, bool):
        return f"lần xuất hiện lạ {n!r}, trường {field}"
    if not _word_hit(lines[i], word, n):
        return f"câu {i} không có chữ {word!r} (lần {n}), trường {field}"
    return None


def _walk(lines, node, field: str, out: list[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "zoom":
                continue
            path = f"{field}.{k}" if field else k
            if k in _KEYS:
                msg = _one(lines, v, path)
                if msg:
                    out.append(msg)
                continue
            _walk(lines, v, path, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(lines, v, f"{field}[{i}]", out)


def check(lines, scenes) -> list[str]:
    """Danh sách lỗi tiếng Việt. Rỗng nghĩa là mọi mốc chữ đều có trong câu."""
    out: list[str] = []
    _walk(lines, scenes, "", out)
    return out
