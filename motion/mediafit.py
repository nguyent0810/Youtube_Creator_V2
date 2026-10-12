"""Căn ảnh / video vào đúng khung (Short 9:16, Long 16:9, hay một ô cửa sổ bên trong) -- chủ kênh, 12/10/2026.

VÌ SAO: clip ngang đem phủ khung dọc bị cắt mất ~2/3 hình (và ngược lại: clip dọc trên khung ngang). Trước đây mọi clip Short
đều bị cắt giữa về 1080x1920, không ai kiểm phần còn lại có nghĩa hay không.

Cách quyết định (một chỗ duy nhất, dùng chung cho Short và Long):
    loss = phần diện tích nguồn bị cắt bỏ nếu PHỦ KÍN ô (cover)
    loss <= MAX_LOSS  -> "cover": phóng vừa đủ rồi cắt mép (mất ít, hình đầy ô)
    loss >  MAX_LOSS  -> "blur":  đặt TRỌN hình vào ô (contain) trên nền là chính hình đó phóng to + làm nhoè + tối đi
                                 (không viền đen, không méo, không mất chủ thể)

    python motion/mediafit.py check <file ảnh/video> short|long      # in kích thước, hướng, loss, cách xử lý
    python motion/mediafit.py fit <src> <dst.mp4> short|long          # dựng bản đã căn (video)

Ảnh trong Short: cảnh `photo` kiểu "full" mà loss > MAX_LOSS_IMG thì build.py tự chuyển sang "print" (ảnh in, hiện trọn hình).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MAX_LOSS = 0.45        # video: mất hơn 45% diện tích thì không cắt nữa (ngang 16:9 -> ô vuông 44% vẫn cắt; -> khung dọc 68% thì không)
MAX_LOSS_IMG = 0.40    # ảnh tràn khung: mất hơn 40% thì chuyển sang ảnh in
FRAMES = {"short": (1080, 1920), "long": (1920, 1080)}


def probe(path: Path | str, ffprobe: str = "ffprobe") -> tuple[int, int]:
    """(rộng, cao) HIỂN THỊ của ảnh/video (đã tính cờ xoay của video quay bằng điện thoại)."""
    r = subprocess.run([ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation:stream_tags=rotate", "-of", "default=nw=1", str(path)],
                       capture_output=True, text=True)
    kv = dict(ln.split("=", 1) for ln in r.stdout.splitlines() if "=" in ln)
    if "width" not in kv:
        raise SystemExit(f"{path}: ffprobe không đọc được kích thước: {r.stderr[-200:]}")
    w, h = int(kv["width"]), int(kv["height"])
    rot = abs(int(float(kv.get("rotation", kv.get("TAG:rotate", 0)) or 0))) % 180
    return (h, w) if rot == 90 else (w, h)


def orientation(w: int, h: int) -> str:
    r = w / h
    return "ngang" if r > 1.15 else "dọc" if r < 0.87 else "vuông"


def crop_loss(sw: int, sh: int, bw: int, bh: int) -> float:
    """Phần diện tích nguồn bị cắt bỏ khi phủ kín ô bw x bh (0 = cùng tỉ lệ)."""
    k = max(bw / sw, bh / sh)
    return max(0.0, 1 - (bw * bh) / (sw * k * sh * k))


def decide(sw: int, sh: int, bw: int, bh: int, max_loss: float = MAX_LOSS) -> str:
    return "cover" if crop_loss(sw, sh, bw, bh) <= max_loss else "blur"


def vf(mode: str, bw: int, bh: int, canvas: tuple[int, int] | None = None, pos: tuple[int, int] = (0, 0), fps: int = 30) -> str:
    """Chuỗi -vf: căn vào ô bw x bh theo `mode`; có `canvas` thì đặt ô vào toạ độ `pos` trên nền đen canvas (cửa sổ video Short)."""
    bw, bh = bw // 2 * 2, bh // 2 * 2
    if mode == "cover":
        g = f"scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh}"
    else:
        g = (f"split[a][b];[a]scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh},gblur=sigma=30,eq=brightness=-0.14:saturation=0.85[bg];"
             f"[b]scale={bw}:{bh}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    if canvas and (canvas != (bw, bh) or pos != (0, 0)):
        g += f",pad={canvas[0]}:{canvas[1]}:{pos[0]}:{pos[1]}:black"
    return g + f",fps={fps}"


def fit_video(src: Path, dst: Path, bw: int, bh: int, canvas: tuple[int, int] | None = None, pos: tuple[int, int] = (0, 0),
              ffmpeg: str = "ffmpeg", seconds: float = 60, pre_vf: str = "", max_loss: float = MAX_LOSS) -> str:
    """Dựng bản đã căn; trả về mode đã dùng. Ghi vào file tạm rồi đổi tên (ffmpeg chết giữa chừng không để lại file dở)."""
    ffprobe = str(Path(ffmpeg).with_name("ffprobe" + Path(ffmpeg).suffix)) if Path(ffmpeg).parent != Path(".") else "ffprobe"
    sw, sh = probe(src, ffprobe)
    mode = decide(sw, sh, bw, bh, max_loss)
    tmp = dst.with_name(dst.stem + ".tmp.mp4")
    cmd = [ffmpeg, "-v", "error", "-y", "-i", str(src), "-t", f"{seconds:g}", "-vf", (pre_vf + "," if pre_vf else "") + vf(mode, bw, bh, canvas, pos),
           "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0 or not tmp.exists():
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"{dst.name}: căn clip hỏng {str(p.stderr)[-600:]}")
    tmp.replace(dst)
    return mode


def report(path: Path | str, fmt: str) -> str:
    sw, sh = probe(path)
    bw, bh = FRAMES[fmt]
    loss = crop_loss(sw, sh, bw, bh)
    act = "phủ kín (cắt mép)" if loss <= MAX_LOSS else "đặt trọn hình trên nền nhoè"
    return f"{Path(path).name}: {sw}x{sh} ({orientation(sw, sh)}) -> khung {fmt} {bw}x{bh}: cắt mất {loss:.0%} -> {act}"


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from factory.console import utf8_console  # noqa: E402
    utf8_console()
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "check":
        print(report(a[1], a[2]))
    elif len(a) >= 4 and a[0] == "fit":
        W, H = FRAMES[a[3]]
        print(a[2], fit_video(Path(a[1]), Path(a[2]), W, H))
    else:
        raise SystemExit(__doc__)
