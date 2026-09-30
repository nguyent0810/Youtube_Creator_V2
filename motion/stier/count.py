import json, sys, glob
for f in sorted(glob.glob("data/stier/specs/*.json")):
    d = json.load(open(f, encoding="utf-8")); n = sum(len(l.split()) for l in d["lines"])
    print(f"{f.split(chr(92))[-1].split('/')[-1][:-5]:14} {n:4} từ ~{n/3.75:4.1f}s {'QUÁ DÀI' if n > 132 else ''}")
