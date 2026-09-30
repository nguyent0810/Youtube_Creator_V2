"""Xem nhanh tư liệu một hồ sơ: đoạn mở bài + ảnh PD + dòng khớp từ khoá.

    python motion/stier/peek.py <slug> [số ký tự mở bài] [regex ...]
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2] / "data" / "stier" / "research"
slug = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 1800
d = json.loads((R / f"{slug}.json").read_text(encoding="utf-8"))
for a in d["articles"]:
    print(f"=== {a['title']} ({len(a['text'])} ký tự)")
    print(a["text"][:n])
for pat in sys.argv[3:]:
    print(f"--- /{pat}/")
    for a in d["articles"]:
        for s in re.split(r"(?<=[.!?])\s+", a["text"]):
            if re.search(pat, s, re.I):
                print("  •", s[:400])
print("--- ảnh PD")
for k, i in enumerate(d["images"]):
    print(f"#{k} {i['file'][5:80]} {i['w']}x{i['h']} [{i['date'][:20]}] {i['desc'][:90]}")
