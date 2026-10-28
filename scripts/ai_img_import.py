"""Chép ảnh minh hoạ (do chủ kênh nhờ bot tạo) vào chỗ engine đọc (26/10/2026).

    python scripts/ai_img_import.py <topic>

Chủ kênh thả ảnh vào `motion/hf/assets/long/<topic>/img/ai/ai_NN.png`. Đường dẫn này có trong `AGENTS.md`
và trong tin nhắn gửi bot.

Engine (`build_long.fetch_img`) chỉ đọc ảnh ngoài Commons ở `output/long/<topic>/img/<key>.jpg`, kèm `<key>.json`.
Script này đổi ảnh sang RGB 1920x1080 (cover), lưu thành `ai0N.jpg` và ghi `.json`.
- License ghi "no restrictions": ảnh không vào danh sách ghi công Commons.
- Cảnh dùng ảnh AI phải đặt `"credit": false`, để engine không in "TƯ LIỆU · PHẠM VI CÔNG CỘNG" lên tranh minh hoạ.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()
    topic = sys.argv[1]
    src_dir = ROOT / "motion" / "hf" / "assets" / "long" / topic / "img" / "ai"
    dst_dir = ROOT / "output" / "long" / topic / "img"
    dst_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src_dir.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))
    if not files:
        print(f"chưa có ảnh trong {src_dir}")
        return 1
    for p in files:
        m = re.search(r"(\d+)", p.stem)
        if not m:
            print(f"bỏ qua {p.name}: tên không có số")
            continue
        key = f"ai{int(m.group(1)):02d}"
        im = ImageOps.fit(Image.open(p).convert("RGB"), (1920, 1080), Image.LANCZOS)
        im.save(dst_dir / f"{key}.jpg", quality=92)
        (dst_dir / f"{key}.json").write_text(json.dumps(
            {"file": f"EXT:ai:{p.stem}", "license": "no restrictions", "artist": ""}, ensure_ascii=False), encoding="utf-8")
        print(f"{p.name} -> {key}.jpg ({Image.open(p).size[0]}x{Image.open(p).size[1]} -> 1920x1080)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
