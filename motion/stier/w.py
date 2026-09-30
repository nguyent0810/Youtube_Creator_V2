"""Ghi spec gọn: python motion/stier/w.py <slug> < spec.json (kiểm JSON + đếm từ)."""
import json, sys
from pathlib import Path
d = json.loads(sys.stdin.read())
n = sum(len(l.split()) for l in d["lines"])
p = Path("data/stier/specs") / f"{sys.argv[1]}.json"
p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{sys.argv[1]}: {n} từ ~{n/3.75:.1f}s {'QUÁ DÀI' if n > 132 else 'ok'}")
