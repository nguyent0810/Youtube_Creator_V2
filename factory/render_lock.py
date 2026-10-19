"""Hàng đợi render duy nhất cho cả máy (retro 06/10/2026 mục 9: render song song làm mỗi chương chậm gấp đôi).

    with render_lock("long ck-d1 ch03"):
        subprocess.run([... "hyperframes", "render", ...])

Khoá là một file mở + khoá byte của HĐH (msvcrt trên Windows, flock trên POSIX): tiến trình chết thì HĐH tự nhả, không
có khoá "mồ côi". Người đến sau chờ (in ra ai đang giữ) rồi chạy tiếp -- không cần agent tự đọc log của nhau.
"""
from __future__ import annotations

import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

LOCK = Path(__file__).resolve().parents[1] / "output" / ".render.lock"


def _say(msg: str) -> None:
    """In không bao giờ làm sập tiến trình: console Windows (cp1252) không mã hoá được tiếng Việt (lỗi đã gặp 2 lần)."""
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    sys.stdout.write(msg.encode(enc, "replace").decode(enc) + "\n")
    sys.stdout.flush()


def _try(fd: int) -> bool:
    try:
        if sys.platform == "win32":
            import msvcrt
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError:
        return False


def _release(fd: int) -> None:
    if sys.platform == "win32":
        import msvcrt
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN)


_held: dict[str, int] = {}   # khoá đang giữ trong CHÍNH tiến trình này -> lồng nhau không tự chặn mình


@contextmanager
def render_lock(label: str, poll: float = 5.0, path: Path | None = None):
    """Lồng được: build_long giữ khoá cho CẢ lượt render nhiều chương (ngoài), từng chương gọi lại (trong) -> không bị
    tiến trình khác chen giữa các chương; người chờ vào ngay khi lượt kết thúc (C2 07/10: khoá theo chương + chờ 15 s làm
    một lượt render nhiều chương giành khoá liên tục, người chờ trễ 1,5 giờ)."""
    p = path or LOCK
    key = str(p.resolve()) if p.exists() else str(p)
    if _held.get(key):
        _held[key] += 1
        try:
            yield
        finally:
            _held[key] -= 1
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(p), os.O_RDWR | os.O_CREAT)
    holder = p.with_suffix(".who")
    try:
        said = False
        while not _try(fd):
            if not said:
                who = holder.read_text(encoding="utf-8") if holder.exists() else "?"
                _say(f"[render] chờ hàng đợi — đang render: {who}")
                said = True
            time.sleep(poll)
        holder.write_text(f"{label} (pid {os.getpid()}, từ {time.strftime('%H:%M:%S')})", encoding="utf-8")
        key = str(p.resolve())
        _held[key] = 1
        try:
            yield
        finally:
            _held.pop(key, None)
            _release(fd)
    finally:
        os.close(fd)
