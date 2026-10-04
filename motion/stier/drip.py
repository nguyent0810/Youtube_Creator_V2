"""Upload rải từng video một lên CL (private + publishAt), cách nhau GAP giờ — không bao giờ đổ cả lô.

    python motion/stier/drip.py motion/stier/drip_2026-10.json [--gap 3]

File kế hoạch: [{"slug": "btk", "vn": "2026-10-06 18:30"}, ...] theo thứ tự upload.
- Video đầu upload ngay, mỗi video sau chờ đủ GAP giờ kể từ lần upload trước.
- Video nào đã có video_id (upload_one từ chối) thì bỏ qua, không tính là một lần upload.
- Dừng an toàn: tạo file output/stier/STOP_DRIP (kiểm tra mỗi phút).
- Log: output/stier/drip.log; kết quả từng video: output/stier/uploads.json (do upload_one ghi).
Chạy tách rời (sống qua khi đóng phiên, không qua khởi động lại máy):
    Start-Process python -ArgumentList 'motion/stier/drip.py','motion/stier/drip_2026-10.json' -WindowStyle Hidden
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STOP = ROOT / "output/stier/STOP_DRIP"
LOG = ROOT / "output/stier/drip.log"


def log(msg: str):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def main():
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    gap = float(sys.argv[sys.argv.index("--gap") + 1]) * 3600 if "--gap" in sys.argv else 3 * 3600
    log(f"BẮT ĐẦU {len(plan)} video, cách {gap / 3600:g} giờ")
    last = 0.0
    for p in plan:
        while time.time() < last + gap:
            if STOP.exists():
                log("THẤY STOP_DRIP -> dừng"); return
            time.sleep(60)
        if STOP.exists():
            log("THẤY STOP_DRIP -> dừng"); return
        r = subprocess.run([sys.executable, str(ROOT / "motion/stier/upload_one.py"), p["slug"], p["vn"]], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
        out = (r.stdout + r.stderr).strip().splitlines()
        tail = " | ".join(out[-3:])
        if r.returncode == 0:
            log(f"OK {p['slug']} -> {p['vn']} VN :: {tail}")
            last = time.time()
        elif "đã đăng rồi" in tail:
            log(f"BỎ QUA {p['slug']} (đã có video) :: {tail}")
        else:
            log(f"LỖI {p['slug']} (rc={r.returncode}) :: {tail}")
            last = time.time()              # vẫn giãn cách sau một lần thử hỏng
    log("XONG")


if __name__ == "__main__":
    main()
