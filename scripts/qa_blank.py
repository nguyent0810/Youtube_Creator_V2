"""Dò "màn trống" trong video đã dựng: đoạn ≥ N giây mà vùng giữa khung hình chỉ còn nền (không chữ, không biểu đồ, không ảnh).

    python scripts/qa_blank.py <video.mp4> [--min 1.0] [--fps 4] [--topic <topic>]

--topic (retro 3 mục 7, 14): đọc output/long/<topic>/chNN/data.js -> đoạn nằm TRỌN trong cảnh biểu đồ đang vẽ (candles/race)
hoặc thẻ có khung (quote/ledger), dài ≤ SOFT_MAX giây, in riêng "ĐANG HIỆN DẦN" và KHÔNG tính vào số đoạn trống. Mọi đoạn
khác (kể cả đoạn dài hơn SOFT_MAX trong cảnh biểu đồ) vẫn là TRỐNG -> cổng giữ nguyên độ chặt. Không có --topic: y như cũ.

Lỗi hay gặp nhất khi soát (retro 06/10/2026): chữ của cảnh neo vào một từ ở CUỐI câu -> đầu cảnh trống 1–3 giây. Công cụ
này lấy mẫu khung hình, đo độ "có nội dung" của vùng giữa (bỏ HUD trên và phụ đề dưới): độ lệch chuẩn độ sáng sau khi làm mờ
nền lưới mảnh. Đoạn liên tiếp dưới ngưỡng ≥ --min giây được liệt kê kèm mốc thời gian để mở đúng cảnh mà sửa.
Dùng như thư viện: `scan(video)` -> [(giây đầu, giây cuối)] (motion/stier/build.py gọi sau mỗi Short, retro 2 mục 12).
Dòng CUỐI luôn là "<tên>: N đoạn trống ≥ Xs" (chuỗi PM grep ": 0 đoạn").
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

THRESH = 9.0      # độ lệch chuẩn độ sáng (0–255) của vùng giữa sau khi làm mờ; nền trơn + lưới mờ < ~6


def frames(video: Path, fps: float, tmp: Path, ffmpeg: str = "ffmpeg") -> list[Path]:
    subprocess.run([ffmpeg, "-v", "error", "-i", str(video), "-vf", f"fps={fps},scale=480:-1", str(tmp / "f_%05d.png")], check=True)
    return sorted(tmp.glob("f_*.png"))


def content(p: Path) -> float:
    im = Image.open(p).convert("L")
    w, h = im.size
    mid = im.crop((int(w * 0.04), int(h * 0.12), int(w * 0.96), int(h * 0.80))).filter(ImageFilter.GaussianBlur(2))
    return float(np.asarray(mid, dtype=np.float32).std())


def scan(video: Path, mn: float = 1.0, fps: float = 4.0, ffmpeg: str = "ffmpeg") -> list[tuple[float, float]]:
    with tempfile.TemporaryDirectory() as t:
        vals = [content(p) for p in frames(Path(video), fps, Path(t), ffmpeg)]
    runs, start = [], None
    for i, v in enumerate(vals + [THRESH + 1]):
        if v < THRESH and start is None:
            start = i
        elif v >= THRESH and start is not None:
            if (i - start) / fps >= mn:
                runs.append((start / fps, i / fps))
            start = None
    return runs


def fmt(s: float, e: float, tag: str = "TRỐNG") -> str:
    return f"{tag} {int(s // 60):02d}:{s % 60:05.2f} → {int(e // 60):02d}:{e % 60:05.2f}  ({e - s:.1f}s)"


# ---------- phân loại theo data.js (retro 3 mục 7, 14) ----------
CHART_DRAW = {"candles", "race"}     # khung + trục hiện ngay, nến / thanh mọc dần
CARD_FRAME = {"quote", "ledger"}     # khung thẻ hiện ngay, chữ gõ / dòng hiện dần
SOFT_MAX = 5.0                       # đoạn dài hơn vẫn là TRỐNG dù nằm trong cảnh biểu đồ/thẻ
EDGE = 0.3                           # dung sai mép cảnh (lấy mẫu 4 fps + làm tròn khung khi nối chương)


def spans(topic: str, root: Path | None = None) -> list[tuple[float, float, str]]:
    """[(giây đầu, giây cuối, loại)] TUYỆT ĐỐI trong final.mp4 của các cảnh biểu đồ/thẻ, nối chương theo thứ tự spec."""
    root = root or Path(__file__).resolve().parents[1]
    spec = json.loads((root / "data" / "long" / topic / "spec.json").read_text(encoding="utf-8"))
    out, off = [], 0.0
    for name in spec["chapters"]:
        f = root / "output" / "long" / topic / name / "data.js"
        if not f.exists():
            raise SystemExit(f"qa_blank --topic: thiếu {f} (chạy build_long html)")
        case = json.loads(f.read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
        for s in case["scenes"]:
            if s.get("type") in CHART_DRAW | CARD_FRAME:
                out.append((off + s["t0"], off + s["t1"], s["type"]))
        off += case["dur"]
    return out


def classify(runs: list[tuple[float, float]], sp: list[tuple[float, float, str]]) -> tuple[list, list]:
    """-> (trống thật, [(s, e, loại)] đang hiện dần). Chỉ "mềm" khi đoạn nằm TRỌN trong MỘT cảnh biểu đồ/thẻ và ≤ SOFT_MAX."""
    hard, soft = [], []
    for s, e in runs:
        hit = next((ty for a, b, ty in sp if a - EDGE <= s and e <= b + EDGE), None)
        if hit and e - s <= SOFT_MAX:
            soft.append((s, e, hit))
        else:
            hard.append((s, e))
    return hard, soft


def main() -> None:
    a = sys.argv[1:]
    video = Path(a[0])
    mn = float(a[a.index("--min") + 1]) if "--min" in a else 1.0
    fps = float(a[a.index("--fps") + 1]) if "--fps" in a else 4.0
    runs = scan(video, mn, fps)
    soft = []
    if "--topic" in a:
        runs, soft = classify(runs, spans(a[a.index("--topic") + 1]))
    for s, e in runs:
        print(fmt(s, e))
    for s, e, ty in soft:
        print(fmt(s, e, f"ĐANG HIỆN DẦN ({'chart' if ty in CHART_DRAW else 'card'} {ty})"))
    extra = f" (+{len(soft)} đoạn chart/card đang hiện dần, không tính)" if soft else ""
    print(f"{video.name}: {len(runs)} đoạn trống ≥ {mn}s{extra}")      # dòng CUỐI giữ dạng cũ: chuỗi grep ": 0 đoạn"


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # site-packages có gói "factory" khác (factory_boy)
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7; trước đây sửa riêng từng file)
    main()
