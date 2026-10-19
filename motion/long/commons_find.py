"""Tìm ảnh tự do trên Wikimedia Commons THEO TỪ KHÓA (bổ sung cho research_long.py, vốn chỉ lấy ảnh gắn trong bài Wikipedia).

    python motion/long/commons_find.py <topic> "từ khóa 1" "từ khóa 2" ... [--n 12]

Chỉ giữ Public domain / CC0 / CC BY / CC BY-SA (cùng bộ lọc với research_long), ảnh ngang hoặc dọc từ 800px.
Ghi nối vào output/long/<topic>/commons.json (không trùng) + csheet_<n>.jpg (bảng ảnh đánh số).
Trong gen_scenes ghi thẳng tên "File:…" vào IMGS.
"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stier"))
import research as R  # noqa: E402

FREE = re.compile(r"public domain|^pd|cc0|no restrictions|^cc by(-sa)? ?\d|^cc-by", re.I)
BAD = re.compile(r"nc|nd|fair use", re.I)
ROOT = Path(__file__).resolve().parents[2]


def main():
    args = sys.argv[1:]
    n = 12
    if "--n" in args:
        i = args.index("--n")
        n = int(args[i + 1])
        del args[i:i + 2]
    topic, qs = args[0], args[1:]
    od = ROOT / "output" / "long" / topic
    od.mkdir(parents=True, exist_ok=True)
    f = od / "commons.json"
    rec = json.loads(f.read_text(encoding="utf-8")) if f.exists() else []
    seen = {r["file"] for r in rec}
    start = len(rec)
    for q in qs:
        try:
            files = [x for x in R.commons_search(q, n) if x not in seen and re.search(r"\.(jpe?g|png|tiff?)$", x, re.I)]
            got = 0
            for im in R.imageinfo(files):
                lic = im["license"]
                if not FREE.search(lic) or BAD.search(lic.replace("Public domain", "")) or max(im["w"], im["h"]) < 800:
                    continue
                im["q"] = q
                rec.append(im)
                seen.add(im["file"])
                got += 1
            print(f"{q[:48]:48s} +{got}", flush=True)
        except Exception as e:   # 429 / mạng: bỏ qua từ khóa này, giữ phần đã có
            print(f"{q[:48]:48s} LỖI {str(e)[:80]}", flush=True)
        time.sleep(1.2)
    f.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    R.OUT = od
    for k in range(start // 36, (len(rec) + 35) // 36):
        part = rec[k * 36:(k + 1) * 36]
        R.sheet(f"csheet_{k}", part)
    for i, im in enumerate(rec[start:], start):
        print(i, (im["license"] or "")[:13].ljust(13), im["file"][5:85])


if __name__ == "__main__":
    main()
