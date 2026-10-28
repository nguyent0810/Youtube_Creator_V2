"""Dò đoạn đứng hình trong các chương đã render, chạy SAU `build_long.py render`, trước `final` (26/10/2026).

    python scripts/freeze_check.py <topic> [--max 12]

Lỗi đã gặp:
- Social Network ch02: ghim bản đồ sai tên làm engine lỗi, cả chương đứng ở thẻ chương 72 giây.
- Moneyball ch06: cảnh `question` bị neo kéo dài 20 giây.
Contact sheet thưa (1 khung/11 giây) dễ bỏ sót, và `long_gate.py` không thấy được vì lỗi chỉ lộ ra sau khi render.

Dùng ffmpeg freezedetect (n=0.003). Đoạn đứng yên > --max giây thì báo LỖI và thoát mã 1.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--max", type=float, default=12.0)
    a = ap.parse_args()
    bad = 0
    for mp4 in sorted((ROOT / "output" / "long" / a.topic).glob("ch*/silent.mp4")):
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-vf", f"freezedetect=n=0.003:d={a.max}",
                            "-map", "0:v", "-f", "null", "-"], capture_output=True, text=True, errors="replace")
        starts = re.findall(r"freeze_start: ([\d.]+)", r.stderr)
        durs = re.findall(r"freeze_duration: ([\d.]+)", r.stderr)
        for s, d in zip(starts, durs):
            bad += 1
            print(f"  LỖI {mp4.parent.name}: đứng hình {float(d):.1f}s từ {float(s):.1f}s")
    print("ĐẠT" if not bad else f"TRƯỢT ({bad} đoạn đứng hình > {a.max:g}s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
