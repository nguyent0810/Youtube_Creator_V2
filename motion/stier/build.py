"""Dựng một hồ sơ S-tier từ spec: giọng đọc -> mốc từng từ -> ảnh -> bản đồ -> HTML -> render -> âm thanh.

    python motion/stier/build.py <slug> [<slug> ...] [--no-render] [--draft]

Spec: data/stier/specs/<slug>.json (người viết), gồm
  title, description, tags, kicker, sub, accent?, acc[], lines[] (mỗi phần tử MỘT câu đọc),
  imgs {key: "File:....jpg"}, map? {countries, context, labels, bbox, pins}, scenes[],
  sources[] (link bài gốc để truy vết).
Mốc thời gian trong scenes: số nguyên i = đầu câu i; [i, "từ"] = lúc đọc chữ đó;
[i, "từ", n] = lần thứ n; [i, "từ", n, lệch] cộng thêm giây; [i, null, 0, lệch] = đầu câu + lệch.
Sai chữ neo là LỖI CỨNG (bắt lỗi gõ trước khi tốn render).

Ra: output/stier/<slug>/{voice.wav, timing.json, sfx.wav, silent.mp4, final.mp4}.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HF = ROOT / "motion" / "hf"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "motion"))
sys.path.insert(0, str(HERE))

import hf_align  # noqa: E402
import hf_geo  # noqa: E402
import sfx  # noqa: E402
from factory import paths  # noqa: E402

SPECS = ROOT / "data" / "stier" / "specs"
OUT = ROOT / "output" / "stier"
FF, FFMPEG = str(paths.FFMPEG_DIR), paths.FFMPEG   # YF_FFMPEG_DIR (factory/paths.py)
VOICE = "Anh Khôi"
UA = {"User-Agent": "yt-factory/1.0 (documentary research; contact via channel)"}
ANCHORS = {"at", "until", "reveal", "strike", "swap", "plusAt", "dayAt", "headAt", "signAt", "labelAt", "imgAt", "dimAt"}
ANCHOR_LISTS = {"groupAt", "headTimes"}
_engine = None


def norm(w: str) -> str:
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


# ---------------- giọng đọc ----------------
def speak(lines: list[str], wav: Path, tjson: Path) -> dict:
    global _engine
    if tjson.exists() and wav.exists():
        t = json.loads(tjson.read_text(encoding="utf-8"))
        if [s["text"] for s in t["segments"]] == lines:
            return t
    import numpy as np
    import soundfile as sf
    from factory import speak as SP
    if _engine is None:
        _engine = SP._load_engine()
    chunks, segs, cur = [], [], 0.0
    for i, ln in enumerate(lines):
        a = _engine.infer(ln, voice=VOICE)
        d = len(a) / SP.SAMPLE_RATE
        segs.append({"index": i, "text": ln, "start": round(cur, 3), "end": round(cur + d, 3)})
        chunks.append(a); cur += d
    wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(wav), np.concatenate(chunks), SP.SAMPLE_RATE)
    t = {"sample_rate": SP.SAMPLE_RATE, "duration": round(cur, 3), "segments": segs}
    tjson.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    return t


def word_lines(t: dict, wav: Path) -> list[dict]:
    env, hop = hf_align.energy_envelope(wav)
    out = []
    for seg in t["segments"]:
        toks = seg["text"].split()
        times = hf_align.word_times(env, hop, seg["start"], seg["end"], [hf_align.token_weight(x) for x in toks])
        out.append({"text": seg["text"], "start": seg["start"], "end": seg["end"],
                    "words": [{"w": x, "t": a, "d": d} for x, (a, d) in zip(toks, times)]})
    return out


# ---------------- ảnh (Commons, phạm vi công cộng) ----------------
def fetch_img(file: str, dst: Path) -> dict:
    from PIL import Image
    src = dst.with_suffix(".src")       # tên file Commons của ảnh đang cache (ảnh cache theo KHOÁ spec)
    if dst.exists() and (not src.exists() or src.read_text(encoding="utf-8").strip() != file):
        # spec đổi ảnh cho cùng khoá -> bản cũ là ảnh khác (audit 08/10/2026, L16). Cache cũ chưa
        # ghi nguồn thì không kiểm được -> tải lại một lần cho chắc.
        dst.unlink()
    if not dst.exists():
        def info(width=None):
            prm = {"action": "query", "prop": "imageinfo", "titles": file, "iiprop": "url|size|extmetadata",
                   "format": "json", "formatversion": "2"}
            if width:
                prm["iiurlwidth"] = width
            q = urllib.parse.urlencode(prm)
            with urllib.request.urlopen(urllib.request.Request(f"https://commons.wikimedia.org/w/api.php?{q}", headers=UA), timeout=60) as r:
                return json.loads(r.read())["query"]["pages"][0]["imageinfo"][0]
        for k in range(6):
            try:
                ii = info()
                # upload.wikimedia.org chặn tải bản gốc (429) -> luôn xin ảnh thu nhỏ CỠ CHUẨN, nhỏ hơn bản gốc
                W = next((w for w in (1920, 1280, 960, 500, 330) if w < ii["width"]), None)
                if W:
                    ii = info(W)
                lic = ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
                if not re.search(r"public domain|^pd|cc0|no restrictions", lic, re.I):
                    raise SystemExit(f"{file}: giấy phép '{lic}' KHÔNG phải phạm vi công cộng")
                url = ii.get("thumburl") or ii["url"]
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                    raw = r.read()
                break
            except SystemExit:
                raise
            except Exception as e:
                if k == 5:
                    raise
                time.sleep(4 * (k + 1) + (10 if "429" in str(e) else 0))
        im = Image.open(io.BytesIO(raw))
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255)); im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400))
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
        src.write_text(file, encoding="utf-8")
        time.sleep(1.0)
    with Image.open(dst) as im:
        return {"w": im.size[0], "h": im.size[1]}


# ---------------- mốc thời gian ----------------
class Anchors:
    def __init__(self, lines):
        self.L = lines

    def __call__(self, a):
        if isinstance(a, bool):
            raise ValueError(f"mốc lạ {a!r}")
        if isinstance(a, int):
            return self.L[a]["start"]
        if isinstance(a, float):
            return a
        if isinstance(a, list):
            i, w = a[0], a[1] if len(a) > 1 else None
            n = a[2] if len(a) > 2 else 0
            off = a[3] if len(a) > 3 else 0.0
            if w is None:
                return round(self.L[i]["start"] + off, 3)
            c = 0
            for x in self.L[i]["words"]:
                if norm(x["w"]) == norm(w):
                    if c == n:
                        return round(x["t"] + off, 3)
                    c += 1
            raise ValueError(f"câu {i} không có chữ {w!r} (lần {n}): {self.L[i]['text']}")
        raise ValueError(f"mốc lạ {a!r}")


def resolve(obj, A):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ANCHORS and isinstance(v, (int, float, list)) and not isinstance(v, bool):
                out[k] = A(v)
            elif k in ANCHOR_LISTS and v is not None:
                out[k] = [A(x) for x in v]
            else:
                out[k] = resolve(v, A)
        return out
    if isinstance(obj, list):
        return [resolve(x, A) for x in obj]
    return obj


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from beatfx import assign_beats  # noqa: E402  (motion/beatfx.py — dùng chung với video dài)


def plan(spec: dict, lines: list[dict], dur: float) -> list[dict]:
    A = Anchors(lines)
    sc = []
    for i, s in enumerate(spec["scenes"]):
        r = resolve({k: v for k, v in s.items() if k != "at"}, A)
        r["t0"] = 0.0 if i == 0 else A(s["at"])
        sc.append(r)
    for i, r in enumerate(sc):
        r["t1"] = sc[i + 1]["t0"] if i + 1 < len(sc) else dur
        if r["t1"] <= r["t0"] + 0.25:
            raise ValueError(f"cảnh {i} ({r['type']}) quá ngắn: {r['t0']:.2f}-{r['t1']:.2f}")
        t0, t1, ty = r["t0"], r["t1"], r["type"]
        if ty == "hero" and r.get("head") and not r.get("headTimes"):
            # tiêu đề đồng bộ với lời: từng chữ trên màn hình bật đúng lúc được đọc (nếu có trong cảnh)
            words = [w for ln in lines for w in ln["words"] if t0 - 0.05 <= w["t"] < t1]
            hs = r["head"].replace("\n", " ").split()
            times, j = [], 0
            for h in hs:
                hit = next((k for k in range(j, len(words)) if norm(words[k]["w"]) == norm(h)), None)
                if hit is None:
                    times.append((times[-1] + 0.14) if times else r.get("headAt", t0 + 0.25)); continue
                times.append(words[hit]["t"]); j = hit + 1
            r["headTimes"] = times
        if ty == "date":
            r.setdefault("dayAt", t0 + 0.1)
            ng = len("".join(c if c.isdigit() else " " for c in r["date"]).split())
            r.setdefault("groupAt", [t0 + 0.35 + 0.3 * g for g in range(ng)])
        if ty == "calendar":
            r.setdefault("at", t0 + 0.45)
            r.setdefault("step", round(min(0.1, 1.2 / r["n"]), 3))
        if ty == "quote":
            r.setdefault("at", t0 + 0.4)
            r.setdefault("typeDur", round(min(len(r["text"]) * 0.035, (t1 - r["at"]) * 0.75), 3))
        if ty == "counter":
            r.setdefault("at", t0 + 0.1)
            r.setdefault("until", round(r["at"] + min(1.6, (t1 - t0) * 0.7), 3))
        if ty == "clock":
            r.setdefault("swap", round(t0 + (t1 - t0) * 0.45, 3))
            r.setdefault("plusAt", round(r["swap"] + 0.3, 3))
        if ty == "map":
            for k, p in enumerate(r.get("pins") or []):
                p.setdefault("at", round(t0 + 0.35 + 0.3 * k, 3))
            for q in r.get("routes") or []:
                q.setdefault("until", round(q["at"] + 0.9, 3))
        if ty == "slam":
            r.setdefault("at", round(t0 + 0.12, 3))
        if ty == "split":
            r["a"].setdefault("at", t0 + 0.1); r["b"].setdefault("at", t0 + 0.4)
            if r.get("sign"):
                r.setdefault("signAt", t0 + 0.8)
    assign_beats(sc, spec.get("title", ""), boxed_max=12)   # màn dọc hẹp: con dấu/băng dán chỉ cho dòng thật ngắn
    return sc


HTML = """<!doctype html>
<html lang="vi" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,600;0,700;0,800;0,900;1,600&family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="assets/engine/casefile.css" />
<link rel="stylesheet" href="assets/engine/beat.css" />
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/cases/{slug}/data.js"></script>
</head>
<body>
<!-- Hồ sơ S-tier: {title} — sinh bởi motion/stier/build.py, đừng sửa tay. -->
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920" data-fps="30">
  <div class="layer" id="bed"></div>
  <div class="layer" id="motes"></div>
  <div class="layer" id="stage"></div>
  <div class="layer" id="leak"></div>
  <svg class="layer" id="grain" width="1080" height="1920"><filter id="gn"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"/></filter><rect width="100%" height="100%" filter="url(#gn)"/></svg>
  <div class="layer" id="vig"></div>
  <div class="layer" id="scrims"></div>
  <div id="prog"><i></i></div>
  <div id="kicker"><div class="bar"></div><div class="t"></div></div>
  <div id="caps"></div>
  <div class="layer" id="flash"></div>
</div>
<script src="assets/engine/beat.js"></script>
<script src="assets/engine/casefile.js"></script>
</body>
</html>
"""


def run(cmd, **kw):
    env = os.environ.copy()
    env["PATH"] = FF + os.pathsep + env["PATH"]
    return subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def build(slug: str, render: bool = True, draft: bool = False) -> Path:
    spec = json.loads((SPECS / f"{slug}.json").read_text(encoding="utf-8"))
    od = OUT / slug
    od.mkdir(parents=True, exist_ok=True)
    lines_txt = spec["lines"]
    nw = sum(len(l.split()) for l in lines_txt)
    if not 55 <= nw <= 135:
        raise SystemExit(f"{slug}: {nw} từ — ngoài 55-135")
    t = speak(lines_txt, od / "voice.wav", od / "timing.json")
    lines = word_lines(t, od / "voice.wav")
    dur = round(t["duration"] + 0.6, 2)                         # 0.6s thở cuối cho vòng lặp
    adir = HF / "assets" / "cases" / slug
    imgs = {}
    for key, file in spec.get("imgs", {}).items():
        wh = fetch_img(file, adir / f"{key}.jpg")
        imgs[key] = {"src": f"assets/cases/{slug}/{key}.jpg", **wh}
    geo = None
    if spec.get("map"):
        hf_geo.BOX = (70, 330, 1010, 1330)
        mp = spec["map"]
        geo = hf_geo.bake({"countries": mp["countries"], "context": mp.get("context", []), "labels": mp.get("labels", {}),
                           "bbox": mp["bbox"], "pins": mp["pins"]})["_geo"]
    scenes = plan(spec, lines, dur)
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(slug)) % 100000 + 7
    case = {"slug": slug, "dur": dur, "seed": seed, "accent": spec.get("accent", "#e2402d"), "kicker": spec["kicker"],
            "sub": spec.get("sub", ""), "acc": spec.get("acc", []), "lines": lines, "imgs": imgs, "geo": geo, "scenes": scenes}
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
    comp = HF / "compositions" / "cases" / f"{slug}.html"
    comp.parent.mkdir(parents=True, exist_ok=True)
    comp.write_text(HTML.replace("{slug}", slug).replace("{dur}", str(dur)).replace("{title}", re.sub(r"-{2,}", "—", spec["title"])), encoding="utf-8")   # "--" trong tiêu đề sẽ đóng comment HTML sớm
    sfx.build(case, od / "sfx.wav")
    if not render:
        return comp
    silent = od / ("draft.mp4" if draft else "silent.mp4")
    cmd = ["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
           f"compositions/cases/{slug}.html", "-o", str(silent), "--fps", "30", "--quiet"]
    cmd += ["-q", "draft"] if draft else ["--crf", "19"]
    r = run(cmd, cwd=HF)
    if r.returncode != 0 or not silent.exists():
        raise SystemExit(f"{slug}: render hỏng\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    final = od / ("draft_av.mp4" if draft else "final.mp4")
    fc = ("[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad,asplit=2[v][vk];[2:a]volume=0.5[s0];"
          "[s0][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[s];"
          "[v][s]amix=inputs=2:weights='1 1':normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    r = run([FFMPEG, "-v", "error", "-y", "-i", str(silent), "-i", str(od / "voice.wav"), "-i", str(od / "sfx.wav"),
             "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
             "-shortest", "-movflags", "+faststart", str(final)])
    if r.returncode != 0:
        raise SystemExit(f"{slug}: mux hỏng {r.stderr[-2000:]}")
    return final


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for s in args:
        t0 = time.time()
        p = build(s, render="--no-render" not in sys.argv, draft="--draft" in sys.argv)
        print(f"{s}: {p}  ({time.time() - t0:.0f}s)", flush=True)
