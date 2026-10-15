"""Bản rời của đoạn nhận diện kênh (cảnh `brand`) để duyệt: 1920x1080, ~3 giây, có âm hiệu.

    python motion/long/brand_sting.py [--theme lab] [--name "MIND IN THE MACHINE"] [--sub "AI · CÔNG NGHỆ · DỄ HIỂU"]

Dùng đúng engine casewide.js + sfx_long.py như video dài, nên bản duyệt = bản sẽ xuất hiện sau cold open.
Ra output/long/_brand_<theme>/brand.mp4.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "motion"), str(ROOT)]

import build_long as BL  # noqa: E402
import sfx_long  # noqa: E402
import variety  # noqa: E402


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main() -> None:
    theme = arg("--theme", "lab")
    name, sub = arg("--name", "MIND IN THE MACHINE"), arg("--sub", "AI · CÔNG NGHỆ · DỄ HIỂU")
    key = f"_brand_{theme}"
    od = ROOT / "output" / "long" / key
    od.mkdir(parents=True, exist_ok=True)
    dur = 3.4
    case = {"topic": key, "ch": "brand", "dur": dur, "seed": 2026, "accent": {"lab": "#22d3ee", "chart": "#fbbf24"}.get(theme, "#e2402d"),
            "look": variety.look(None), "theme": theme, "brand": name, "hud": {}, "acc": [], "lines": [], "imgs": {},
            "geo": None, "scenes": [{"type": "brand", "t0": 0.2, "t1": dur, "name": name, "sub": sub}],
            "prog0": 0, "prog1": 0}
    (od / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
    comp = BL.HF / "compositions" / "long" / f"{key}.html"
    comp.parent.mkdir(parents=True, exist_ok=True)
    comp.write_text(BL.HTML.replace("{fonts}", variety.fonts_url(None)).replace("{data}", f"assets/long/{key}/data.js")
                    .replace("{dur}", f"{dur:.3f}").replace("{title}", name).replace("{videos}", ""), encoding="utf-8")
    sfx_long.build(case, od / "sfx.wav")
    silent = od / "silent.mp4"
    r = BL.subprocess.run(["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
                           f"compositions/long/{key}.html", "-o", str(silent), "--fps", "30", "--quiet", "--crf", "18"],
                          cwd=BL.HF, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not silent.exists():
        raise SystemExit(f"render hỏng\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    out = od / "brand.mp4"
    subprocess.run([BL.FFMPEG, "-v", "error", "-y", "-i", str(silent), "-i", str(od / "sfx.wav"),
                    "-filter_complex", "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[a]", "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main()
