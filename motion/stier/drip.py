"""Upload rải từng video một lên CL (private + publishAt), cách nhau GAP giờ — không bao giờ đổ cả lô.

    python motion/stier/drip.py motion/stier/drip_2026-10.json [--gap 3]

File kế hoạch: [{"slug": "btk", "vn": "2026-10-06 18:30"}, ...] theo thứ tự upload.
- Video đầu upload ngay, mỗi video sau chờ đủ GAP giờ kể từ lần upload trước.
- Video nào đã có video_id (upload_one từ chối) thì bỏ qua, không tính là một lần upload.
- Dừng an toàn: tạo file output/stier/STOP_DRIP (kiểm tra mỗi phút).
- Log: output/stier/drip.log; kết quả từng video: output/stier/uploads.json (do upload_one ghi).
Chạy tách rời (sống qua khi đóng phiên, không qua khởi động lại máy):
    Start-Process python -ArgumentList 'motion/stier/drip.py','motion/stier/drip_2026-10.json' -WindowStyle Hidden

AN TOÀN KHI CHẠY LẠI (audit 08/10/2026): khoảng cách giữa hai lần upload tính
từ lần upload THẬT gần nhất trong uploads.json, không phải từ lúc khởi động
-- bản cũ khởi động lại là upload ngay. Và chỉ MỘT tiến trình drip được
chạy (khoá trong state.sqlite): hai bản cùng chạy từng có thể cùng qua chốt
"đã có video_id" và upload trùng.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory import store  # noqa: E402

STOP = ROOT / "output/stier/STOP_DRIP"
LOG = ROOT / "output/stier/drip.log"
UPLOADS = ROOT / "output/stier/uploads.json"


def last_upload_ts() -> float:
    """Thời điểm upload thật gần nhất (uploads.json do upload_one.py ghi)."""
    try:
        rows = json.loads(UPLOADS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0.0
    ts = [datetime.strptime(x["uploaded"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
          for x in rows if x.get("uploaded")]
    return max(ts, default=0.0)


def log(msg: str):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def main():
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    gap = float(sys.argv[sys.argv.index("--gap") + 1]) * 3600 if "--gap" in sys.argv else 3 * 3600
    ttl = int((gap * (len(plan) + 1)) / 60) + 360
    with store.connect() as conn:
        try:
            with store.locked(conn, "drip-CL", ttl_minutes=ttl):
                run(plan, gap)
        except store.LockBusy as exc:
            log(f"KHÔNG CHẠY: {exc}")


def run(plan, gap):
    log(f"BẮT ĐẦU {len(plan)} video, cách {gap / 3600:g} giờ")
    last = last_upload_ts()
    if last:
        log(f"lần upload gần nhất: {datetime.fromtimestamp(last):%d/%m %H:%M} -- giữ đủ khoảng cách từ mốc đó")
    for p in plan:
        while time.time() < last + gap:
            if STOP.exists():
                log("THẤY STOP_DRIP -> dừng"); return
            time.sleep(60)
        if STOP.exists():
            log("THẤY STOP_DRIP -> dừng"); return
        r = subprocess.run([sys.executable, str(ROOT / "motion/stier/upload_one.py"), p["slug"], p["vn"]], cwd=ROOT,
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        out = (r.stdout + r.stderr).strip().splitlines()
        tail = " | ".join(out[-3:])
        if r.returncode == 0:
            log(f"OK {p['slug']} -> {p['vn']} VN :: {tail}")
            last = max(time.time(), last_upload_ts())
        elif "đã đăng rồi" in tail:
            log(f"BỎ QUA {p['slug']} (đã có video) :: {tail}")
        else:
            log(f"LỖI {p['slug']} (rc={r.returncode}) :: {tail}")
            last = time.time()              # vẫn giãn cách sau một lần thử hỏng
    log("XONG")


if __name__ == "__main__":
    main()
