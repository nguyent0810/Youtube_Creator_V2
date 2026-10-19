"""Clip nền cho Short S-tier (kênh MIM): Pexels + Coverr -> 1080x1920, 30 fps, không tiếng.

    python motion/stier/clips.py search "data center" [--src pexels,coverr] [--n 12]   # in ứng viên + bảng ảnh poster
    python motion/stier/clips.py get pexels:12345 [coverr:abc ...]                      # tải + cắt sẵn vào assets/clips/

Spec: cảnh nào có "clip": "pexels:<id>" (+ "ms": giây bắt đầu trong clip, "veil": 0..1 độ tối màn che) thì có nền
video. build.py nướng thẻ <video> TĨNH vào HTML (HyperFrames chỉ đếm media khai báo tĩnh -- như video dài).

Giấy phép (kiểm 06/10/2026):
- Pexels: dùng tự do, không bắt buộc ghi công -- vẫn ghi "Video: Pexels — <tác giả>". https://www.pexels.com/license/
- Coverr: dùng thương mại được; API BẮT BUỘC ghi công Coverr -> "Video: Coverr — <tiêu đề>". Bỏ clip
  is_ai_generated (tránh nhãn nội dung AI) và is_premium. Gói Demo: 50 lần gọi/giờ -> cache index.
Key: Pexels đọc như motion/long/pexels.py; Coverr: COVERR_API_KEY trong môi trường hoặc ../.local.env (tên bắt đầu COVERR).
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CLIPS = ROOT / "motion" / "hf" / "assets" / "clips"        # gitignore (motion/hf/.gitignore: assets/*)
INDEX = CLIPS / "index.json"
KEY_FILES = (ROOT.parent / ".local.env",)
PROVIDERS = ("pexels", "coverr")
_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def parse(ref: str) -> tuple[str, str]:
    prov, _, cid = str(ref).partition(":")
    if prov not in PROVIDERS or not _ID.match(cid):
        raise ValueError(f"clip lạ {ref!r} (dạng pexels:<id> hoặc coverr:<id>)")
    return prov, cid


def ffprobe_for(ffmpeg: str) -> str:
    """ffprobe cùng thư mục với ffmpeg được truyền vào (máy sản xuất: chỉ có trong vendor, không có trong PATH)."""
    d = os.path.dirname(ffmpeg)
    return os.path.join(d, "ffprobe") if d else (shutil.which("ffprobe") or "ffprobe")


def transcode(ffmpeg: str, src: Path, dst: Path) -> None:
    """Cắt vào file tạm rồi đổi tên: ffmpeg chết giữa chừng không để lại file trông như đã xong."""
    tmp = dst.with_name(dst.stem + ".tmp.mp4")
    p = subprocess.run(transcode_cmd(ffmpeg, src, tmp), capture_output=True, text=True)
    if p.returncode != 0 or not tmp.exists():
        tmp.unlink(missing_ok=True)
        dst.unlink(missing_ok=True)
        raise SystemExit(f"{dst.name}: cắt clip hỏng {str(p.stderr)[-800:]}")
    tmp.replace(dst)


def transcode_cmd(ffmpeg: str, src: Path, dst: Path, seconds: float = 60) -> list[str]:
    return [ffmpeg, "-v", "error", "-y", "-i", str(src), "-t", f"{seconds:g}",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(dst)]


def video_tags(scenes: list[dict], info: dict, dur: float) -> tuple[list[str], list[dict]]:
    """Thẻ <video> cho cảnh có "clip"; gán s["vid"] = id thẻ. Clip bắt đầu sớm 0,2 s (đã chạy khi cảnh hiện)."""
    tags = []
    for k, s in enumerate(scenes):
        if not s.get("clip"):
            continue
        ref, ms = s["clip"], float(s.get("ms", 0))
        st = max(0.0, s["t0"] - 0.2)
        need = s["t1"] - st + 0.3
        if ms + need > info[ref]["dur"] + 0.05:
            raise SystemExit(f"cảnh {k}: clip {ref} dài {info[ref]['dur']:.1f}s, cần {ms:.1f}+{need:.1f}s -- chọn clip dài hơn hoặc giảm ms")
        s["vid"] = f"v{k}"
        tags.append(f'  <video id="v{k}" class="clip bv" src="{info[ref]["src"]}" data-start="{st:.3f}" '
                    f'data-duration="{min(need, dur - st):.3f}" data-media-start="{ms:.2f}" muted playsinline data-track-index="1"></video>')
    return tags, scenes


# ---------------- mạng ----------------
def _env_key(names: tuple[str, ...], pattern: str) -> str | None:
    for n in names:
        if os.environ.get(n):
            return os.environ[n].strip()
    for f in KEY_FILES:
        if f.exists():
            m = re.search(pattern, f.read_text(encoding="utf-8-sig"), re.M)
            if m and m.group(1).strip().strip('"'):
                return m.group(1).strip().strip('"')
    return None


def _coverr_h() -> dict:
    k = _env_key(("COVERR_API_KEY",), r"^COVERR[A-Z_]*\s*=\s*(.+)$")
    if not k:
        raise SystemExit("không thấy Coverr key (COVERR_API_KEY trong .local.env)")
    return {"Authorization": f"Bearer {k}"}


def _pexels_h() -> dict:
    sys.path.insert(0, str(ROOT / "motion" / "long"))
    import pexels
    return {"Authorization": pexels.key()}


def _index() -> dict:
    return json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {}


def _save_index(idx: dict) -> None:
    CLIPS.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")


def search(q: str, srcs=PROVIDERS, n: int = 12) -> list[dict]:
    import httpx
    out = []
    if "pexels" in srcs:
        r = httpx.get("https://api.pexels.com/videos/search", headers=_pexels_h(), timeout=30,
                      params={"query": q, "orientation": "portrait", "per_page": n, "size": "medium"})
        r.raise_for_status()
        for v in r.json()["videos"]:
            out.append({"ref": f"pexels:{v['id']}", "dur": v["duration"], "author": v["user"]["name"],
                        "title": v["url"].rstrip("/").split("/")[-1][:60], "poster": v.get("image", ""),
                        "files": [{"w": f["width"], "h": f["height"], "link": f["link"]} for f in v["video_files"] if f.get("width")]})
    if "coverr" in srcs:
        r = httpx.get("https://api.coverr.co/videos", headers=_coverr_h(), timeout=30,
                      params={"query": q, "page_size": n, "urls": "true"})
        r.raise_for_status()
        for v in r.json().get("hits") or []:
            if v.get("is_ai_generated") or v.get("is_premium"):
                continue
            out.append({"ref": f"coverr:{v['id']}", "dur": float(v.get("duration") or 0), "author": "Coverr",
                        "title": v.get("title", "")[:60], "poster": v.get("poster", ""),
                        "files": [{"w": v.get("max_width") or 0, "h": v.get("max_height") or 0,
                                   "link": (v.get("urls") or {}).get("mp4_download") or (v.get("urls") or {}).get("mp4")}]})
    idx = _index()
    for c in out:
        idx[c["ref"]] = c
    _save_index(idx)
    return out


def credit(c: dict) -> str:
    prov = c["ref"].split(":")[0]
    return f"Video: Pexels — {c['author']}" if prov == "pexels" else f"Video: Coverr — {c['title']}"


def ensure(ref: str, ffmpeg: str = "ffmpeg") -> dict:
    """Clip đã cắt sẵn (tải + cắt nếu chưa có). Trả {src (đường dẫn trong project HyperFrames), dur, credit}."""
    import httpx
    prov, cid = parse(ref)
    dst = CLIPS / f"{prov}-{cid}.mp4"
    idx = _index()
    c = idx.get(ref)
    if c is None:
        if prov == "pexels":
            r = httpx.get(f"https://api.pexels.com/videos/videos/{cid}", headers=_pexels_h(), timeout=30)
            r.raise_for_status()
            v = r.json()
            c = {"ref": ref, "dur": v["duration"], "author": v["user"]["name"], "title": v["url"].rstrip("/").split("/")[-1][:60],
                 "files": [{"w": f["width"], "h": f["height"], "link": f["link"]} for f in v["video_files"] if f.get("width")]}
        else:
            r = httpx.get(f"https://api.coverr.co/videos/{cid}", headers=_coverr_h(), timeout=30, params={"urls": "true"})
            r.raise_for_status()
            v = r.json()
            if v.get("is_ai_generated") or v.get("is_premium"):
                raise SystemExit(f"{ref}: clip do AI tạo hoặc premium -- không dùng")
            c = {"ref": ref, "dur": float(v.get("duration") or 0), "author": "Coverr", "title": v.get("title", "")[:60],
                 "files": [{"w": v.get("max_width") or 0, "h": v.get("max_height") or 0,
                            "link": (v.get("urls") or {}).get("mp4_download") or (v.get("urls") or {}).get("mp4")}]}
        idx[ref] = c
        _save_index(idx)
    if not dst.exists():
        # bản nhẹ nhất mà vẫn phủ được 1080x1920 sau khi cắt
        fs = sorted((f for f in c["files"] if f.get("link")), key=lambda f: (min(f["w"], f["h"]) < 1080, max(f["w"], f["h"])))
        if not fs:
            raise SystemExit(f"{ref}: không có file tải được")
        raw = CLIPS / f"{prov}-{cid}.src.mp4"
        CLIPS.mkdir(parents=True, exist_ok=True)
        with httpx.stream("GET", fs[0]["link"], timeout=180, follow_redirects=True) as r:
            r.raise_for_status()
            with open(raw, "wb") as fh:
                for ch in r.iter_bytes():
                    fh.write(ch)
        try:
            transcode(ffmpeg, raw, dst)
        finally:
            raw.unlink(missing_ok=True)
    pr = subprocess.run([ffprobe_for(ffmpeg), "-v", "error", "-show_entries", "format=duration",
                         "-of", "csv=p=0", str(dst)], capture_output=True, text=True)
    if pr.returncode != 0 or not pr.stdout.strip():
        raise SystemExit(f"{ref}: ffprobe không đọc được {dst.name}: {pr.stderr[-300:]}")
    return {"src": f"assets/clips/{dst.name}", "dur": float(pr.stdout.strip()), "credit": credit(c)}


def sheet(cands: list[dict], path: Path) -> None:
    """Bảng ảnh poster để chọn clip bằng mắt."""
    import httpx
    from PIL import Image, ImageDraw
    cells = []
    for c in cands:
        try:
            im = Image.open(io.BytesIO(httpx.get(c["poster"], timeout=30, follow_redirects=True).content)).convert("RGB")
            im.thumbnail((320, 320))
            cells.append((c, im))
        except Exception:
            continue
    if not cells:
        return
    cols = 4
    S = Image.new("RGB", (cols * 330, ((len(cells) + cols - 1) // cols) * 360), (16, 16, 16))
    d = ImageDraw.Draw(S)
    for k, (c, im) in enumerate(cells):
        x, y = (k % cols) * 330 + 5, (k // cols) * 360 + 30
        S.paste(im, (x, y))
        d.text((x, y - 24), f"{c['ref']} {c['dur']:.0f}s", fill=(120, 230, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    S.save(path, quality=82)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("search", "get"):
        raise SystemExit(__doc__)
    if a[0] == "search":
        srcs = tuple(a[a.index("--src") + 1].split(",")) if "--src" in a else PROVIDERS
        n = int(a[a.index("--n") + 1]) if "--n" in a else 12
        got = search(a[1], srcs, n)
        for c in got:
            print(f"{c['ref']:22s} {c['dur']:5.1f}s  {c['title']}")
        slug = re.sub(r"[^a-z0-9]+", "-", a[1].lower()).strip("-")
        sheet(got, CLIPS / "sheets" / f"{slug}.jpg")
        print("bảng poster:", CLIPS / "sheets" / f"{slug}.jpg")
    else:
        for ref in a[1:]:
            print(ref, ensure(ref))
