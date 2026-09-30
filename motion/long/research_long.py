"""Gom tư liệu cho video DÀI: nhiều bài Wikipedia + ảnh Commons dùng tự do.

    python motion/long/research_long.py <topic> "Bài 1" "Bài 2" ...

Khác bản Short: video dài cần nhiều hình hơn nên nhận cả CC BY / CC BY-SA
(bắt buộc ghi công trong mô tả — lưu artist + license để in credit tự động),
ngoài Public domain / CC0. Không nhận NC/ND, không nhận "Fair use".
Ghi output/long/<topic>/research.json + sheet_<n>.jpg (bảng ảnh đánh số).
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


def keep(rec, seen, files, src):
    for im in R.imageinfo([f for f in files if f not in seen]):
        lic = im["license"]
        if FREE.search(lic) and not BAD.search(lic.replace("CC BY", "")) and not R.SKIP.search(im["file"]) \
                and im["mime"] in ("image/jpeg", "image/png", "image/tiff", "image/gif") and min(im["w"], im["h"]) >= 400:
            im["from"] = src
            rec["images"].append(im)
            seen.add(im["file"])


def main():
    """Đối số bắt đầu bằng "?" là truy vấn tìm ảnh Commons (vd "?Sugamo Prison"), còn lại là tên bài Wikipedia."""
    topic, pages = sys.argv[1], sys.argv[2:]
    out = Path(__file__).resolve().parents[2] / "output" / "long" / topic
    out.mkdir(parents=True, exist_ok=True)
    dst = out / "research.json"
    rec = json.loads(dst.read_text(encoding="utf-8")) if dst.exists() else {"articles": [], "images": []}
    have = {a["title"] for a in rec["articles"]}
    seen = {i["file"] for i in rec["images"]}
    n0 = len(rec["images"])
    for p in pages:
        if p.startswith("?"):
            keep(rec, seen, R.commons_search(p[1:], 20), p)
            print(f"{p:50} ảnh={len(rec['images'])}", flush=True)
        elif p not in have:
            a = R.article(p)
            rec["articles"].append({"title": a["title"], "text": a["text"]})
            keep(rec, seen, a["images"], a["title"])
            print(f"{a['title']:50} chars={len(a['text']):6} ảnh={len(rec['images'])}", flush=True)
        dst.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(2)
    R.OUT = out
    for k in range(n0 // 36 * 36, len(rec["images"]), 36):   # chỉ vẽ lại các bảng có ảnh mới
        R.sheet(f"sheet_{k // 36}", rec["images"][k:k + 36])


if __name__ == "__main__":
    main()
