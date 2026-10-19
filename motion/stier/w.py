"""Ghi spec gọn: python motion/stier/w.py <slug> < spec.json (kiểm JSON + đếm từ)."""
import pathlib, sys  # noqa: E401
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from factory.console import utf8_console  # noqa: E402
utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
import json, sys
from pathlib import Path
d = json.loads(sys.stdin.read())
n = sum(len(l.split()) for l in d["lines"])
p = Path("data/stier/specs") / f"{sys.argv[1]}.json"
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{sys.argv[1]}: {n} từ ~{n/3.75:.1f}s {'QUÁ DÀI' if n > 132 else 'ok'}")
