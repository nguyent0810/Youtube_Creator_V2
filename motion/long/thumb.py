"""Render thumbnail từ mẫu HTML: motion/long/thumbs/<topic>_tN.html -> output/long/<topic>/tN.jpg (1280x720, < 2 MB)
+ tN_small.jpg (320x180) để soi ở cỡ mobile.

    python motion/long/thumb.py <topic> [t1 t2 ...]
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


# Chữ thumbnail tràn mép (MIM #5 t1/t2 09/10/2026: "CHƯA BẤM Đ…", "1 TRIỆU ĐO…" bị cắt): template ghi cỡ chữ cố định + nowrap.
# Chặn bằng máy: mọi phần tử chữ (.big, .pill, .tag hoặc data-fit; .pill thêm sau khi D2 t1 tràn nhãn 09/10) tự thu nhỏ (tối đa còn 40% cỡ gốc) tới khi nằm trong khung an toàn 40 px.
# Chạy lúc nạp và lại khi webfont nạp xong (số đo font dự phòng khác font thật). Tất định: chỉ đo DOM.
# Vẫn soát bằng mắt ở tN_small.jpg (cỡ điện thoại).
FIT = """<script>(function(){const M=40,W=1920,H=1080;const fit=function(){
document.querySelectorAll('.big,.pill,.tag,[data-fit]').forEach(function(e){if(!e.dataset.f0)e.dataset.f0=parseFloat(getComputedStyle(e).fontSize);
const f0=+e.dataset.f0;let f=f0;e.style.fontSize=f+'px';let r=e.getBoundingClientRect();
while((r.right>W-M||r.left<M||r.bottom>H-M)&&f>f0*0.4){f*=0.97;e.style.fontSize=f+'px';r=e.getBoundingClientRect();}});};
fit();if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);})();</script>
"""


def main(topic: str, only: list[str]) -> None:
    od = ROOT / "output" / "long" / topic
    for src in sorted((HERE / "thumbs").glob(f"{topic}_t*.html")):
        t = src.stem.rsplit("_", 1)[1]
        if only and t not in only:
            continue
        comp = BL.HF / "compositions" / "long" / f"_{topic}_{t}.html"
        html = src.read_text(encoding="utf-8")
        assert "</body>" in html, f"{src.name}: thiếu </body>"
        comp.write_text(html.replace("</body>", FIT + "</body>", 1), encoding="utf-8")
        mp4 = od / f"_{t}.mp4"
        from factory.render_lock import render_lock      # một render một lúc trên cả máy
        with render_lock(f"thumb {topic} {t}"):
            r = subprocess.run(["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
                                f"compositions/long/{comp.name}", "-o", str(mp4), "--fps", "30", "--quiet", "--crf", "12"],
                               cwd=BL.HF, capture_output=True, text=True, encoding="utf-8", errors="replace")
        comp.unlink(missing_ok=True)
        if r.returncode != 0 or not mp4.exists():
            raise SystemExit(f"{t}: render hỏng\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
        for name, w, q in ((f"{t}.jpg", 1280, 2), (f"{t}_small.jpg", 320, 3)):
            subprocess.run([BL.FFMPEG, "-v", "error", "-y", "-i", str(mp4), "-frames:v", "1", "-vf", f"scale={w}:-2:flags=lanczos",
                            "-q:v", str(q), str(od / name)], check=True)
        mp4.unlink()
        print(od / f"{t}.jpg")


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    main(sys.argv[1], sys.argv[2:])
