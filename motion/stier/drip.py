"""Upload rải từng video một lên CL (private + publishAt) — không bao giờ đổ cả lô.

    python motion/stier/drip.py motion/stier/drip_2026-10.json

File kế hoạch: [{"slug": "btk", "vn": "2026-10-06 18:30"}, ...] theo thứ tự upload.
- Trước mỗi video, hỏi Channel (factory/channel.py) mốc được upload tiếp và chờ tới đó.
  Luật giãn nhịp (CL: 3 giờ/lần, tối đa 8/24 giờ) nằm ở Channel và áp cho MỌI đường
  đăng -- drip không còn đồng hồ riêng, nên publish_batch chạy song song cũng không
  làm vỡ nhịp, và một lần thử hỏng (chưa giữ slot) không bắt chờ thêm một vòng.
- Video nào đã có video_id (upload_one từ chối) thì bỏ qua.
- Dừng an toàn: tạo file output/stier/STOP_DRIP (kiểm tra mỗi phút).
- Log: output/stier/drip.log; kết quả từng video: bảng upload_log trong state.sqlite.
Chạy tách rời (sống qua khi đóng phiên, không qua khởi động lại máy):
    Start-Process python -ArgumentList 'motion/stier/drip.py','motion/stier/drip_2026-10.json' -WindowStyle Hidden
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory import store  # noqa: E402
from factory.channel import Channel  # noqa: E402

STOP = ROOT / "output/stier/STOP_DRIP"
LOG = ROOT / "output/stier/drip.log"


def next_slot() -> datetime:
    # api=None: chỉ đọc sổ giãn nhịp, không cần credential -- file creds bị
    # khoá/thiếu trong lúc chờ không làm chết vòng drip.
    with store.connect() as conn:
        return Channel("CL", None, conn).next_upload_at()


def log(msg: str):
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def main():
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if "--gap" in sys.argv:
        log("BỎ QUA --gap: nhịp do Channel quyết (factory/channels.py, mục pacing)")
    log(f"BẮT ĐẦU {len(plan)} video, nhịp theo Channel CL; lượt đầu sớm nhất {next_slot():%Y-%m-%d %H:%M} UTC")
    for p in plan:
        while datetime.now(timezone.utc) < next_slot():
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
        elif "đã đăng rồi" in tail:
            log(f"BỎ QUA {p['slug']} (đã có video) :: {tail}")
        else:
            # Lỗi đã giữ slot (upload đứt giữa chừng) thì Channel tự giãn
            # nhịp; lỗi chưa chạm YouTube thì không phải chờ thêm.
            log(f"LỖI {p['slug']} (rc={r.returncode}) :: {tail}")
    log("XONG")


if __name__ == "__main__":
    main()
