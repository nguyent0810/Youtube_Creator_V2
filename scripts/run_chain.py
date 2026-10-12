"""Chạy một chuỗi tự động (.sh: render -> final -> QA -> upload ...) AN TOÀN: chạy BẢN CHỤP, và chỉ một bản mỗi chuỗi.

    python scripts/run_chain.py <chuoi.sh> [--log <file>] [--multi-channel] [--unchecked-pipes]

VÌ SAO (retro 2 mục 18, 07/10/2026): bash đọc file .sh DẦN DẦN trong lúc chạy. PM viết lại publish_d1.sh (16:18) khi bản
cũ (13:00) vẫn đang chạy -> bản cũ đọc file mới ở vị trí byte cũ, nhảy thẳng vào vòng Short và đăng 2 Short D1 TRƯỚC khi
video dài D1 được upload, rồi chết vì lỗi cú pháp; bản mới chạy song song. Hai lỗi gốc, hai chốt:
  1. bash chạy BẢN CHỤP output/.chains/<tên>.<giờ>.sh -> sửa file gốc không ảnh hưởng tiến trình đang chạy;
  2. khoá HĐH theo tên chuỗi (giống factory/render_lock.py) -> bản thứ hai của cùng chuỗi bị TỪ CHỐI ngay (in ai đang giữ).
Muốn thay chuỗi đang chạy: dừng nó trước (taskkill /PID <pid> /T /F), rồi chạy lại lệnh này.

  3. MỘT KÊNH MỖI CHUỖI (retro 3 mục 2, 09/10/2026): final_r4, final_r6 gọi publish cho cả MIM lẫn CK; MIM hết 6 lượt/24 h
     -> `--wait` chặn luôn C3/D2 của CK ~18 h. Chuỗi gọi publish_long.py / publish_batch.py cho > 1 kênh bị TỪ CHỐI
     (thêm --multi-channel nếu thật sự cố ý, vd. chuỗi không có --wait).
  4. Bước build_long html/render/tts qua ống `| grep/tail` mà không kiểm mã thoát -> TỪ CHỐI (retro 3 mục 13).
  5. Chuỗi có publish_long.py mà không có `playlists.py sync` -> WARNING (retro 3 mục 16: tiến trình chờ lượt lâu chạy code
     cũ, video lên không vào playlist).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from factory.render_lock import _release, _try  # noqa: E402

CHAINS = ROOT / "output" / ".chains"
_GIT_BASH = Path(r"C:\Program Files\Git\bin\bash.exe")


def bash() -> str:
    """Git Bash trước (C:\\Windows\\System32\\bash.exe là WSL — môi trường khác hẳn), rồi bash trong PATH."""
    b = os.environ.get("CHAIN_BASH") or (str(_GIT_BASH) if _GIT_BASH.exists() else shutil.which("bash"))
    if not b:
        raise SystemExit("không tìm thấy bash (đặt CHAIN_BASH)")
    return b


_PUB = re.compile(r"publish_long\.py|publish_batch\.py")
_FALLBACK_CODES = ("FS", "CL", "BUD", "MIM", "CK")


def _codes() -> tuple[str, ...]:
    try:
        from factory.channels import CHANNELS
        return tuple(CHANNELS)
    except Exception:       # noqa: BLE001  (thiếu phụ thuộc -> vẫn kiểm được với danh sách cố định)
        return _FALLBACK_CODES


def _code_lines(text: str) -> list[str]:
    """Dòng lệnh thật: bỏ dòng chú thích (#...), phần chú thích cuối dòng (' #'), và dòng echo (chỉ in chữ)."""
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        s = re.split(r"\s#\s", s, maxsplit=1)[0]
        if re.match(r"echo\b", s):
            continue
        out.append(s)
    return out


def publish_channels(text: str) -> set[str]:
    """Các kênh mà chuỗi có thể đăng lên. Rỗng = chuỗi không gọi publish_long/publish_batch.
    Mã kênh lấy từ MỌI dòng lệnh (không chỉ dòng publish): chuỗi hay gọi qua hàm `one <topic> <KÊNH> <giờ>` với
    `publish_long.py $T $CH`, nên chỉ nhìn dòng publish sẽ không thấy kênh nào."""
    lines = _code_lines(text)
    if not any(_PUB.search(s) for s in lines):
        return set()
    pat = re.compile(r"(?<![\w-])(" + "|".join(_codes()) + r")(?![\w-])")
    return {m for s in lines for m in pat.findall(s)}


_STEP = re.compile(r"build_long\.py\s+\S+\s+(html|render|tts)\b")
_PIPE = re.compile(r"(?<!\|)\|(?!\|)")


def swallowed_steps(text: str) -> list[str]:
    """Bước build_long html/render/tts bị đưa qua ống `| grep/tail` mà không kiểm mã thoát (không `set -o pipefail`, dòng sau
    không có PIPESTATUS) -> bước hỏng mà chuỗi vẫn đi tiếp (retro 3 mục 13: MIM #7 r8 html chết ở ch05/ch06, chuỗi tới render
    mới hỏng; cùng họ retro 2 mục 19: chuỗi chỉ grep "PacingHold", không thấy publish_long sập)."""
    lines = _code_lines(text)
    if any(re.match(r"set\s+(-\w*o\s+pipefail|-o\s+pipefail)", s) or "pipefail" in s for s in lines):
        return []
    out = []
    for i, s in enumerate(lines):
        m = _STEP.search(s)
        if m and _PIPE.search(s[m.end():]):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if "PIPESTATUS" not in s and "PIPESTATUS" not in nxt:
                out.append(s)
    return out


def check(text: str, multi: bool = False, unchecked: bool = False) -> list[str]:
    """Kiểm tĩnh trước khi chạy: lỗi chặn -> SystemExit; trả về danh sách WARNING."""
    bad = swallowed_steps(text)
    if bad and not unchecked:
        raise SystemExit("bước dựng đi qua ống `|` mà không kiểm mã thoát — hỏng vẫn chạy tiếp (retro 3 mục 13):\n  " + "\n  ".join(bad)
                         + "\nGhi log ra file + `|| { ...; return 1; }`, hoặc thêm `[ \"${PIPESTATUS[0]}\" = 0 ] || ...` ngay dòng sau, "
                         "hoặc `set -o pipefail`. (--unchecked-pipes nếu cố ý.)")
    chans = publish_channels(text)
    if len(chans) > 1 and not multi:
        raise SystemExit(f"chuỗi gọi publish cho {len(chans)} kênh ({', '.join(sorted(chans))}) — MỘT kênh mỗi chuỗi: lượt upload của "
                         "kênh này (--wait) sẽ chặn kênh kia (retro 3: final_r4/r6 kẹt C3, D2 ~18 h). Tách thành một chuỗi/kênh, "
                         "hoặc thêm --multi-channel nếu cố ý.")
    warn = []
    lines = _code_lines(text)
    if any("qa_blank.py" in s and "final.mp4" in s and "--topic" not in s for s in lines):
        warn.append("qa_blank.py chạy trên final.mp4 không có `--topic <topic>` -> biểu đồ đang vẽ / thẻ có khung bị tính là TRỐNG "
                    "(retro 3 mục 7, 14: C3 4 đoạn, D2 3, C4 4 phải duyệt tay)")
    if any("publish_long.py" in s for s in lines) and not any(re.search(r"playlists\.py\s+sync", s) for s in lines):
        warn.append("chuỗi có publish_long.py nhưng không gọi `python scripts/playlists.py sync --channel <KÊNH>` sau khi đăng "
                    "(tiến trình chờ lượt lâu chạy code cũ -> video không vào playlist, retro 3 mục 16)")
    return warn


def run(script: Path, log: Path | None = None, base: Path | None = None, multi: bool = False, unchecked: bool = False) -> int:
    for w in check(script.read_text(encoding="utf-8", errors="replace"), multi, unchecked):
        print(f"  ! WARNING {w}", flush=True)
    base = base or CHAINS
    base.mkdir(parents=True, exist_ok=True)
    name = script.stem
    lock, who = base / f"{name}.lock", base / f"{name}.who"
    fd = os.open(str(lock), os.O_RDWR | os.O_CREAT)
    try:
        if not _try(fd):
            held = who.read_text(encoding="utf-8") if who.exists() else "?"
            raise SystemExit(f"chuỗi {name} ĐANG CHẠY ({held}) — không chạy bản thứ hai. Dừng nó trước nếu muốn thay.")
        snap = base / f"{name}.{time.strftime('%Y%m%d-%H%M%S')}.sh"
        shutil.copyfile(script, snap)
        who.write_text(f"pid {os.getpid()}, bản chụp {snap.name}, từ {time.strftime('%H:%M:%S')}", encoding="utf-8")
        out = open(log, "a", encoding="utf-8") if log else None
        try:
            return subprocess.run([bash(), snap.as_posix()], stdout=out, stderr=subprocess.STDOUT if out else None).returncode
        finally:
            if out:
                out.close()
            _release(fd)
    finally:
        os.close(fd)


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    lg = Path(a[a.index("--log") + 1]) if "--log" in a else None
    sys.exit(run(Path(a[0]).resolve(), lg, multi="--multi-channel" in a, unchecked="--unchecked-pipes" in a))
