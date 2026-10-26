from pathlib import Path
import time
stier = Path(r"D:/Tools/Youtube Creator v2/Youtube_Creator_V2/output/stier")
items = sorted(stier.rglob("*"), key=lambda p: p.stat().st_mtime, reverse=True)[:40]
for p in items:
    if p.is_file():
        print(time.ctime(p.stat().st_mtime), p.relative_to(stier), p.stat().st_size)
# also data/stier recent
base = Path(r"D:/Tools/Youtube Creator v2/Youtube_Creator_V2/data/stier")
items2 = sorted([p for p in base.iterdir() if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)[:20]
print("--- data/stier ---")
for p in items2:
    print(time.ctime(p.stat().st_mtime), p.name, p.stat().st_size)
