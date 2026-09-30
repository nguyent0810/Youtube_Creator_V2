"""python motion/stier/grab.py <slug> "regex1" "regex2" ... — đoạn trích quanh từ khoá + danh sách ảnh PD."""
import json, re, sys
slug, keys = sys.argv[1], sys.argv[2:]
d = json.load(open(f"data/stier/research/{slug}.json", encoding="utf-8"))
t = " ".join(a["text"] for a in d["articles"])
print(f"== {slug}: {[a['title'] for a in d['articles']]} hits={d.get('channel_hits')}")
print(t[:500].replace("\n", " "))
for k in keys:
    ms = list(re.finditer(k, t))[:2]
    for m in ms:
        print(f"[{k}] >>", t[max(0, m.start() - 130):m.start() + 230].replace("\n", " "))
for i, im in enumerate(d["images"][:16]):
    print(f"  #{i} {im['file'][5:100]} {im['w']}x{im['h']} [{im['date'][:12]}]")
