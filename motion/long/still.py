"""Render một khung tĩnh (logo, ảnh bìa, thumbnail) từ HTML HyperFrames ra PNG đúng kích thước khai báo.

    python motion/long/still.py <file.html> <out.png> [--preview <out_small.png> <px>]

HTML phải là composition 1 khung (data-duration nhỏ, timeline rỗng) — xem motion/long/brand/ck/logo_a.html.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "motion"), str(ROOT)]

import build_long as BL  # noqa: E402


def render(src: Path, out: Path) -> Path:
    comp = BL.HF / "compositions" / "long" / f"_still_{src.stem}.html"
    shutil.copyfile(src, comp)
    mp4 = out.with_suffix(".tmp.mp4")
    try:
        r = subprocess.run(["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
                            f"compositions/long/{comp.name}", "-o", str(mp4), "--fps", "30", "--quiet", "--crf", "8"],
                           cwd=BL.HF, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0 or not mp4.exists():
            raise SystemExit(f"{src.name}: render hỏng\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([BL.FFMPEG, "-v", "error", "-y", "-i", str(mp4), "-frames:v", "1", str(out)], check=True)
    finally:
        comp.unlink(missing_ok=True)
        mp4.unlink(missing_ok=True)
    return out


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    a = sys.argv[1:]
    out = render(Path(a[0]).resolve(), Path(a[1]).resolve())
    if "--preview" in a:
        i = a.index("--preview")
        subprocess.run([BL.FFMPEG, "-v", "error", "-y", "-i", str(out), "-vf", f"scale={a[i + 2]}:-1:flags=lanczos", a[i + 1]], check=True)
    print(out)
