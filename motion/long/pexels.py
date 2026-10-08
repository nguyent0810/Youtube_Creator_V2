"""B-roll Pexels cho video dài (ngang 16:9). Giấy phép Pexels: dùng tự do, không bắt buộc ghi công
(vẫn ghi "Video: Pexels" trong mô tả cho minh bạch).

    python motion/long/pexels.py search <topic> "tokyo night rain" ...   -> in danh sách ứng viên (id, giây, slug)
    python motion/long/pexels.py get <topic> <id> [<id> ...]            -> tải bản 1920x1080 (hoặc gần nhất) về broll/

Chỉ lấy bản HD ≤1920 rộng (4K làm Chrome giải mã chậm, render lâu gấp nhiều lần).
"""
import json
import os
import re
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]


def headers() -> dict:
    """Khoá Pexels: biến môi trường PEXELS_API_KEY, không có thì đọc ../video-editor/.env (như cũ).
    Đọc lúc cần, không đọc lúc import (import không còn chết khi máy không có file .env)."""
    key = os.environ.get("PEXELS_API_KEY")
    env = ROOT.parent / "video-editor" / ".env"
    if not key and env.exists():
        m = re.search(r"PEXELS_API_KEY=(.+)", env.read_text(encoding="utf-8-sig"))
        key = m.group(1).strip() if m else None
    if not key:
        raise SystemExit("thiếu PEXELS_API_KEY (biến môi trường hoặc ../video-editor/.env)")
    return {"Authorization": key}


def out(topic):
    d = ROOT / "output" / "long" / topic / "broll"
    d.mkdir(parents=True, exist_ok=True)
    return d


def search(topic, queries):
    idx_p = out(topic) / "index.json"
    idx = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else {}
    for q in queries:
        r = httpx.get("https://api.pexels.com/videos/search", headers=headers(), timeout=30,
                      params={"query": q, "orientation": "landscape", "per_page": 30, "size": "medium"})
        r.raise_for_status()
        print(f"\n== {q} ({r.json().get('total_results')})")
        for v in r.json()["videos"]:
            slug = v["url"].rstrip("/").split("/")[-1]
            idx[str(v["id"])] = {"dur": v["duration"], "slug": slug, "user": v["user"]["name"], "q": q,
                                 "files": [{"w": f["width"], "h": f["height"], "link": f["link"]} for f in v["video_files"] if f.get("width")]}
            print(f"{v['id']:>10} {v['duration']:>3}s  {slug[:70]}")
    idx_p.write_text(json.dumps(idx, ensure_ascii=False, indent=0), encoding="utf-8")


def get(topic, ids):
    idx = json.loads((out(topic) / "index.json").read_text(encoding="utf-8"))
    for i in ids:
        dst = out(topic) / f"{i}.mp4"
        if dst.exists():
            continue
        v = idx[i]
        fs = sorted((f for f in v["files"] if f["w"] <= 1920 and f["w"] >= f["h"]), key=lambda f: -f["w"])
        f = fs[0]
        # httpx dùng follow_redirects (allow_redirects là tham số của requests -> TypeError
        # ngay lần tải đầu). Tải vào .part rồi mới đổi tên: một lần đứt mạng không để lại
        # .mp4 cụt mà lần chạy sau tưởng là đã tải xong (dst.exists() ở trên).
        part = dst.with_suffix(".mp4.part")
        with httpx.stream("GET", f["link"], timeout=120, follow_redirects=True) as r:
            r.raise_for_status()
            with open(part, "wb") as fh:
                for ch in r.iter_bytes():
                    fh.write(ch)
        part.replace(dst)
        print(f"{i}: {f['w']}x{f['h']} {v['dur']}s {dst.stat().st_size // 1024}KB  {v['slug'][:50]}")


if __name__ == "__main__":
    cmd, topic, *rest = sys.argv[1:]
    (search if cmd == "search" else get)(topic, rest)
