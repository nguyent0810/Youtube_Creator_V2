"""Tìm ảnh PHẠM VI CÔNG CỘNG trên Commons: python motion/stier/find.py "truy vấn" [số lượng] [--sheet tên]

In danh sách file (tên, cỡ, giấy phép, mô tả); --sheet lưu bảng ảnh vào data/stier/research/find_<tên>.jpg.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import research as R  # noqa: E402

q = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 20
files = R.commons_search(q, n)
imgs = [i for i in R.imageinfo(files) if R.PD.search(i["license"]) and i["mime"] in ("image/jpeg", "image/png", "image/tiff", "image/gif")]
for k, i in enumerate(imgs):
    print(f"#{k} {i['file']} {i['w']}x{i['h']} [{i['license'][:18]}] [{i['date'][:12]}] {i['desc'][:80]}")
if "--sheet" in sys.argv:
    R.OUT.mkdir(parents=True, exist_ok=True)
    R.sheet("find_" + sys.argv[sys.argv.index("--sheet") + 1], imgs)
