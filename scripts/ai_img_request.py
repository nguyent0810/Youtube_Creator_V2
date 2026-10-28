"""Nhờ bot tạo ảnh (Grok Bot, routine "CLI Trigger") tạo các ảnh AI trong ai_prompts.md, chờ ảnh về rồi chép vào engine (26/10/2026).

    python scripts/ai_img_request.py <topic> [--wait 900]

- Đọc `GROKBOT_WEBHOOK_URL` / `GROKBOT_WEBHOOK_KEY`: lấy từ biến môi trường, nếu không có thì đọc registry cấp User (Windows).
  Không in giá trị ra màn hình, không ghi vào repo. Hướng dẫn: `docs/tools/grokbot-webhook.md`.
- POST tới webhook: `data/long/<topic>/ai_prompts.md` -> ảnh lưu vào `motion/hf/assets/long/<topic>/img/ai/`.
- Chờ đủ số ảnh `## ai_NN.png` khai trong prompt, rồi chạy `scripts/ai_img_import.py`.
- Bot mất khoảng 2 phút cho mỗi ảnh. Ảnh về vẫn phải được soát bằng mắt trước khi render.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def env(name: str) -> str:
    v = os.environ.get(name)
    if not v and sys.platform == "win32":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                v = winreg.QueryValueEx(k, name)[0]
        except OSError:
            v = None
    if not v:
        raise SystemExit(f"thiếu {name} (xem docs/tools/grokbot-webhook.md)")
    return v


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--wait", type=int, default=900, help="giây chờ tối đa")
    ap.add_argument("--faces", action="store_true",
                    help="nhân vật VÍ DỤ GIẢ ĐỊNH (người hư cấu, CK 27/10/2026): được vẽ rõ mặt, giữ đúng hồ sơ nhân vật trong prompt_file")
    a = ap.parse_args()
    prompts = ROOT / "data" / "long" / a.topic / "ai_prompts.md"
    out = ROOT / "motion" / "hf" / "assets" / "long" / a.topic / "img" / "ai"
    names = re.findall(r"^#+\s+(ai_\d+\.png)", prompts.read_text(encoding="utf-8"), re.M)
    if not names:
        raise SystemExit(f"{prompts}: không có mục '## ai_NN.png'")
    out.mkdir(parents=True, exist_ok=True)
    missing = [n for n in names if not (out / n).exists()]
    if missing:
        body = json.dumps({
            "task": "generate_images", "prompt_file": str(prompts), "output_dir": str(out),
            "instructions": (f"Đọc prompt_file, tạo đúng các ảnh còn thiếu: {', '.join(missing)}. Mỗi ảnh 16:9 cỡ 1920x1080, "
                             "phong cách tranh minh hoạ, không chữ, không số, không logo, "
                             + ("nhân vật là người hư cấu: vẽ rõ mặt, mọi ảnh giữ cùng một gương mặt theo 'Hồ sơ nhân vật' trong file. "
                                if a.faces else "không thấy rõ mặt người (người chỉ vẽ nghiêng quay đi hoặc từ phía sau). ")
                             + "Lưu đúng tên file vào output_dir."),
        }, ensure_ascii=False).encode("utf-8")
        key = env("GROKBOT_WEBHOOK_KEY")
        req = urllib.request.Request(env("GROKBOT_WEBHOOK_URL"), data=body, method="POST", headers={
            "Content-Type": "application/json; charset=utf-8", "Authorization": f"Bearer {key}", "X-Webhook-Secret": key})
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"đã gửi bot: HTTP {r.status}, {len(missing)} ảnh", flush=True)
        t0 = time.time()
        while time.time() - t0 < a.wait:
            left = [n for n in names if not (out / n).exists()]
            if not left:
                break
            time.sleep(15)
        left = [n for n in names if not (out / n).exists()]
        if left:
            print(f"hết {a.wait}s, còn thiếu: {left}")
            return 1
        time.sleep(5)                                   # file vừa xuất hiện có thể đang ghi dở
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "ai_img_import.py"), a.topic]).returncode


if __name__ == "__main__":
    sys.exit(main())
