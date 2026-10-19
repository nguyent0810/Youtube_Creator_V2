"""B-roll Pexels cho video dài (ngang 16:9). Giấy phép Pexels: dùng tự do, không bắt buộc ghi công
(vẫn ghi "Video: Pexels" trong mô tả cho minh bạch).

    python motion/long/pexels.py search <topic> "tokyo night rain" ...   -> in danh sách ứng viên (id, giây, slug)
    python motion/long/pexels.py get <topic> <id> [<id> ...]            -> tải bản 1920x1080 (hoặc gần nhất) về broll/
    thêm --portrait: clip dọc 9:16 (Short), cạnh dài ≤1920

Chỉ lấy bản HD ≤1920 (4K làm Chrome giải mã chậm, render lâu gấp nhiều lần).
Key: biến môi trường PEXELS_API_KEY, rồi ../.local.env (PEXELS_API_KEY hoặc PEXEL_KEY), rồi
../video-editor/.env (máy sản xuất). Đọc lúc cần, không in ra.
"""
import os
import json
import re
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
KEY_FILES = (ROOT.parent / ".local.env", ROOT.parent / "video-editor" / ".env")


def key(files=KEY_FILES) -> str:
    if os.environ.get("PEXELS_API_KEY"):
        return os.environ["PEXELS_API_KEY"].strip()
    for f in files:
        if f.exists():
            m = re.search(r"^(?:PEXELS_API_KEY|PEXEL_KEY)\s*=\s*(.+)$", f.read_text(encoding="utf-8-sig"), re.M)
            if m and m.group(1).strip().strip('"'):
                return m.group(1).strip().strip('"')
    raise SystemExit("không thấy Pexels key (PEXELS_API_KEY / PEXEL_KEY trong .local.env)")


def _h() -> dict:
    return {"Authorization": key()}


def out(topic):
    d = Path(topic) if Path(topic).is_absolute() else ROOT / "output" / "long" / topic / "broll"
    d.mkdir(parents=True, exist_ok=True)
    return d


def search(topic, queries, orientation="landscape"):
    idx_p = out(topic) / "index.json"
    idx = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else {}
    for q in queries:
        r = httpx.get("https://api.pexels.com/videos/search", headers=_h(), timeout=30,
                      params={"query": q, "orientation": orientation, "per_page": 30, "size": "medium"})
        r.raise_for_status()
        print(f"\n== {q} ({r.json().get('total_results')})")
        for v in r.json()["videos"]:
            slug = v["url"].rstrip("/").split("/")[-1]
            idx[str(v["id"])] = {"dur": v["duration"], "slug": slug, "user": v["user"]["name"], "q": q,
                                 "files": [{"w": f["width"], "h": f["height"], "link": f["link"]} for f in v["video_files"] if f.get("width")]}
            print(f"{v['id']:>10} {v['duration']:>3}s  {slug[:70]}")
    idx_p.write_text(json.dumps(idx, ensure_ascii=False, indent=0), encoding="utf-8")


def get(topic, ids, portrait=False):
    idx = json.loads((out(topic) / "index.json").read_text(encoding="utf-8"))
    for i in ids:
        dst = out(topic) / f"{i}.mp4"
        if dst.exists():
            continue
        v = idx[i]
        fs = sorted((f for f in v["files"] if max(f["w"], f["h"]) <= 1920 and (f["h"] > f["w"]) == portrait),
                    key=lambda f: -max(f["w"], f["h"]))
        if not fs:
            print(f"{i}: không có bản {'dọc' if portrait else 'ngang'} ≤1920 -- bỏ qua")
            continue
        f = fs[0]
        with httpx.stream("GET", f["link"], timeout=120, follow_redirects=True) as r:
            r.raise_for_status()
            with open(dst, "wb") as fh:
                for ch in r.iter_bytes():
                    fh.write(ch)
        print(f"{i}: {f['w']}x{f['h']} {v['dur']}s {dst.stat().st_size // 1024}KB  {v['slug'][:50]}")


if __name__ == "__main__":
    portrait = "--portrait" in sys.argv
    cmd, topic, *rest = [a for a in sys.argv[1:] if a != "--portrait"]
    if cmd == "search":
        search(topic, rest, "portrait" if portrait else "landscape")
    else:
        get(topic, rest, portrait)
