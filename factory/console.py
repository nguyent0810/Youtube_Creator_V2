"""Console UTF-8 cho mọi CLI in tiếng Việt (retro 2 mục 7: console Windows cp1252 làm sập qa_blank, render_lock -- 2 lần/1 ngày).

    from factory.console import utf8_console
    utf8_console()          # dòng đầu của khối `if __name__ == "__main__":`

Không có nó, `print("TRỐNG …")` ném UnicodeEncodeError khi stdout là pipe/file mà Python chọn mã cp1252 (chạy từ
Git Bash/Task Scheduler không có PYTHONIOENCODING). Sau lời gọi: stdout/stderr ghi UTF-8, ký tự nào không mã hoá được thì
thay bằng "?" chứ không bao giờ làm sập tiến trình. tests/test_console.py chặn CLI mới quên gọi.
"""
from __future__ import annotations

import sys


def utf8_console() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):     # stream thay thế (pytest, IDLE...) không có reconfigure: bỏ qua
            pass
