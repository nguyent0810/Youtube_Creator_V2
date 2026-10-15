"""Dọn file NẶNG của video đã lên YouTube (đã có video_id: private + hẹn giờ hoặc đã công khai) để không đầy ổ đĩa.

    python scripts/cleanup_published.py            # chỉ liệt kê (mặc định, không xoá gì)
    python scripts/cleanup_published.py --apply    # chuyển các file đó vào THÙNG RÁC Windows (khôi phục được)

Chỉ đụng tới:
- Video dài: output/long/<topic>/ có pub/result.json mang "video_id" -> *.mp4, *.wav (chương, bản ghép, giọng), broll/,
  tts/ (cache giọng). GIỮ: description.txt, captions.vi.srt, thumbnail *.jpg, pub/, *.json, data.js.
- Short: item trong kho có stage = published và video_id -> output/stier/<slug>/ và output/manual/<KÊNH>/<slug>/: *.mp4, *.wav.
Video chưa upload (chưa có video_id) KHÔNG BAO GIỜ bị đụng. Không xoá vĩnh viễn: dọn Thùng rác là việc của người dùng.
"""
from __future__ import annotations

import ctypes
import json
import sys
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from factory import store  # noqa: E402

HEAVY = {".mp4", ".wav", ".mov", ".webm", ".mkv"}


def long_targets() -> list[Path]:
    out = []
    for rp in (ROOT / "output" / "long").glob("*/pub/result.json"):
        if not json.loads(rp.read_text(encoding="utf-8")).get("video_id"):
            continue
        od = rp.parent.parent
        out += [f for f in od.rglob("*") if f.is_file() and (f.suffix.lower() in HEAVY or f.parent.name in ("broll", "tts"))
                and f.suffix.lower() not in (".json", ".srt", ".txt", ".jpg", ".png")]
    return out


def short_targets() -> list[Path]:
    out = []
    with store.connect() as conn:
        rows = conn.execute("SELECT channel, slug FROM item WHERE stage = 'published' AND video_id IS NOT NULL "
                            "AND slug NOT LIKE 'long-%'").fetchall()
    for ch, slug in rows:
        for d in (ROOT / "output" / "stier" / slug, ROOT / "output" / "manual" / ch / slug):
            if d.is_dir():
                out += [f for f in d.rglob("*") if f.is_file() and f.suffix.lower() in HEAVY]
    return out


class _SHFILEOPSTRUCTW(ctypes.Structure):
    _fields_ = [("hwnd", wintypes.HWND), ("wFunc", wintypes.UINT), ("pFrom", wintypes.LPCWSTR), ("pTo", wintypes.LPCWSTR),
                ("fFlags", ctypes.c_uint16), ("fAnyOperationsAborted", wintypes.BOOL), ("hNameMappings", ctypes.c_void_p),
                ("lpszProgressTitle", wintypes.LPCWSTR)]


def to_recycle_bin(paths: list[Path]) -> None:
    """SHFileOperationW + FOF_ALLOWUNDO = vào Thùng rác (không xoá vĩnh viễn)."""
    FO_DELETE, FOF_SILENT, FOF_NOCONFIRMATION, FOF_ALLOWUNDO, FOF_NOERRORUI = 3, 0x4, 0x10, 0x40, 0x400
    for i in range(0, len(paths), 200):
        op = _SHFILEOPSTRUCTW(wFunc=FO_DELETE, pFrom="\0".join(str(p) for p in paths[i:i + 200]) + "\0\0",
                              fFlags=FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT | FOF_NOERRORUI)
        rc = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
        if rc:
            raise SystemExit(f"SHFileOperation lỗi {rc}")


def main() -> None:
    files = sorted(set(long_targets() + short_targets()))
    total = sum(f.stat().st_size for f in files)
    by_dir: dict[Path, int] = {}
    for f in files:
        k = f.relative_to(ROOT).parts[:3]
        by_dir[Path(*k)] = by_dir.get(Path(*k), 0) + f.stat().st_size
    for d, n in sorted(by_dir.items()):
        print(f"{n / 1e6:9.1f} MB  {d}")
    print(f"TỔNG {len(files)} file, {total / 1e9:.2f} GB")
    if "--apply" in sys.argv and files:
        to_recycle_bin(files)
        print("đã chuyển vào Thùng rác — dọn Thùng rác để giải phóng ổ đĩa")


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main()
