import pathlib, sys  # noqa: E401
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from factory.console import utf8_console  # noqa: E402
utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
import json, sys, glob
for f in sorted(glob.glob("data/stier/specs/*.json")):
    d = json.load(open(f, encoding="utf-8")); n = sum(len(l.split()) for l in d["lines"])
    print(f"{f.split(chr(92))[-1].split('/')[-1][:-5]:14} {n:4} từ ~{n/3.75:4.1f}s {'QUÁ DÀI' if n > 132 else ''}")
