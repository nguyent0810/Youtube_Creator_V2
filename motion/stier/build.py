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
import shutil
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
import clips  # noqa: E402
import themes  # noqa: E402

SPECS = ROOT / "data" / "stier" / "specs"
OUT = ROOT / "output" / "stier"
# ffmpeg: FFMPEG_DIR, rồi bản vendor của máy sản xuất, rồi ffmpeg trong PATH (máy khác).
_FF_VENDOR = r"C:\Tools\Youtuber\video-editor\vendor\ffmpeg"
FF = (os.environ.get("FFMPEG_DIR") or (_FF_VENDOR if os.path.isdir(_FF_VENDOR) else None)
      or os.path.dirname(shutil.which("ffmpeg") or "") or _FF_VENDOR)
VOICE = "Anh Khôi"
UA = {"User-Agent": "yt-factory/1.0 (documentary research; contact via channel)"}
ANCHORS = {"at", "until", "reveal", "strike", "swap", "plusAt", "dayAt", "headAt", "signAt", "labelAt", "imgAt", "dimAt"}
ANCHOR_LISTS = {"groupAt", "headTimes"}
_engine = None


def norm(w: str) -> str:
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


# ---------------- giọng đọc ----------------
def speak(lines: list[str], wav: Path, tjson: Path, voice: str = VOICE) -> dict:
    """Đọc từng câu, ghép wav + mốc câu. Cache theo CẢ lời lẫn giọng (Grok: đổi giọng mà
    lời giữ nguyên thì trước đây vẫn trả wav giọng cũ). timing.json cũ không ghi giọng
    là của VOICE mặc định (Anh Khôi) -- cache CL cũ vẫn dùng được."""
    global _engine
    if tjson.exists() and wav.exists():
        t = json.loads(tjson.read_text(encoding="utf-8"))
        if [s["text"] for s in t["segments"]] == lines and t.get("voice", VOICE) == voice:
            return t
    import numpy as np
    import soundfile as sf
    from factory import integrity, speak as SP
    for ln in lines:                      # cả hồ sơ, trước khi đọc câu nào
        integrity.require_speakable(ln)
    if _engine is None:
        _engine = SP._load_engine()
    chunks, segs, cur = [], [], 0.0
    for i, ln in enumerate(lines):
        a = _engine.infer(ln, voice=voice)
        d = len(a) / SP.SAMPLE_RATE
        segs.append({"index": i, "text": ln, "start": round(cur, 3), "end": round(cur + d, 3)})
        chunks.append(a); cur += d
    wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(wav), np.concatenate(chunks), SP.SAMPLE_RATE)
    t = {"sample_rate": SP.SAMPLE_RATE, "duration": round(cur, 3), "voice": voice, "segments": segs}
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


# ---------------- ảnh (Commons theo giấy phép của kênh; NASA) ----------------
def license_ok(lic: str, mode: str = "pd") -> bool:
    """mode "pd": chỉ phạm vi công cộng / CC0 (kênh Hình Sự, như cũ). mode "by": thêm CC BY (mọi phiên bản),
    KHÔNG BY-SA (share-alike: ghi công trong mô tả không đủ), không NC/ND (themes.py, kênh MIM)."""
    if re.search(r"public domain|^pd|cc0|no restrictions", lic, re.I):
        return True
    return mode == "by" and bool(re.fullmatch(r"cc[ -]by(?:[ -]\d(?:\.\d)?)?", lic.strip(), re.I))


def _plain(html: str) -> str:
    import html as H
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", html or ""))).strip()


def fetch_nasa(nasa_id: str, dst: Path) -> dict:
    """Ảnh NASA Image Library (không có bản quyền ở Mỹ; không dùng logo NASA). Ghi công NASA/<trung tâm>."""
    from PIL import Image
    meta = dst.with_suffix(".json")
    if not dst.exists():
        def get(url, timeout=60):
            for k in range(4):
                try:
                    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                        return r.read()
                except Exception:
                    if k == 3:
                        raise
                    time.sleep(3 * (k + 1))
        q = urllib.parse.urlencode({"nasa_id": nasa_id})
        items = json.loads(get(f"https://images-api.nasa.gov/search?{q}"))["collection"]["items"]
        if not items:
            raise SystemExit(f"NASA:{nasa_id}: không có ảnh này")
        m = items[0]["data"][0]
        # tên file thật lấy từ danh sách asset (không phải ảnh nào cũng có ~large)
        hrefs = [i["href"] for i in json.loads(get(f"https://images-api.nasa.gov/asset/{urllib.parse.quote(nasa_id)}"))["collection"]["items"]]
        url = next((h for tag in ("~large.jpg", "~orig.jpg", "~medium.jpg") for h in hrefs if h.endswith(tag)), None)
        if not url:
            raise SystemExit(f"NASA:{nasa_id}: không có bản jpg")
        raw = get(url.replace("http://", "https://"), timeout=120)
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
        who = "NASA/" + m["center"] if m.get("center") else "NASA"
        meta.write_text(json.dumps({"credit": f"Ảnh: {m.get('title', nasa_id)} — {who} (images.nasa.gov)"},
                                   ensure_ascii=False), encoding="utf-8")
    with Image.open(dst) as im:
        return {"w": im.size[0], "h": im.size[1]}


def fetch_img(file: str, dst: Path, mode: str = "pd") -> dict:
    from PIL import Image
    if file.startswith("NASA:"):
        return fetch_nasa(file[5:], dst)
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
                em = ii.get("extmetadata", {})
                lic = em.get("LicenseShortName", {}).get("value", "")
                if not license_ok(lic, mode):
                    raise SystemExit(f"{file}: giấy phép '{lic}' không dùng được cho kênh này ({mode})")
                artist = _plain(em.get("Artist", {}).get("value", ""))[:80] or "không rõ tác giả"
                lic_url = em.get("LicenseUrl", {}).get("value", "")
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
        name = file.removeprefix("File:").rsplit(".", 1)[0]
        page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(file.replace(" ", "_"))
        dst.with_suffix(".json").write_text(json.dumps(
            {"credit": f"Ảnh: {name} — {artist}, {lic}{' (' + lic_url + ')' if lic_url else ''}, via Wikimedia Commons: {page}",
             "license": lic}, ensure_ascii=False), encoding="utf-8")
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
from beatfx import apply_sync, assign_beats  # noqa: E402  (motion/beatfx.py — dùng chung với video dài)


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
    pools = themes.theme(spec)["pools"]
    if pools and pools.get("sync"):   # Beat Text MIM: dòng chữ lớn được đọc trọn -> hiện từng chữ theo giọng
        apply_sync(sc, lines)
    assign_beats(sc, spec.get("title", ""), boxed_max=12,      # màn dọc hẹp: con dấu/băng dán chỉ cho dòng thật ngắn
                 pools=pools)
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
<link rel="stylesheet" href="assets/engine/theme-mim.css" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="assets/cases/{slug}/data.js"></script>
</head>
<body>
<!-- Hồ sơ S-tier: {title} — sinh bởi motion/stier/build.py, đừng sửa tay. -->
<div id="root" class="{cls}" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920" data-fps="30">
  <div class="layer" id="bed"></div>
{videos}
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
    th = themes.theme(spec)
    t = speak(lines_txt, od / "voice.wav", od / "timing.json", voice=spec.get("voice", th["voice"]))
    lines = word_lines(t, od / "voice.wav")
    dur = round(t["duration"] + 0.6, 2)                         # 0.6s thở cuối cho vòng lặp
    adir = HF / "assets" / "cases" / slug
    imgs, credits = {}, []
    for key, file in spec.get("imgs", {}).items():
        wh = fetch_img(file, adir / f"{key}.jpg", th.get("img_license", "pd"))
        imgs[key] = {"src": f"assets/cases/{slug}/{key}.jpg", **wh}
        meta = adir / f"{key}.json"
        if meta.exists():
            credits.append({"kind": "image", "text": json.loads(meta.read_text(encoding="utf-8"))["credit"]})
        elif th.get("img_license", "pd") != "pd":
            # ảnh tải trước khi có ghi công: CC BY mà thiếu dòng ghi công là vi phạm giấy phép -> tải lại cho có
            raise SystemExit(f"{slug}: ảnh {key} thiếu {meta.name} (ghi công) -- xoá {key}.jpg rồi dựng lại")
    geo = None
    if spec.get("map"):
        hf_geo.BOX = (70, 330, 1010, 1330)
        mp = spec["map"]
        geo = hf_geo.bake({"countries": mp["countries"], "context": mp.get("context", []), "labels": mp.get("labels", {}),
                           "bbox": mp["bbox"], "pins": mp["pins"]})["_geo"]
    scenes = plan(spec, lines, dur)
    if th["sound"] == "music" and not any((themes.MUSIC_DIR / f).exists() for f in themes.MIM_TRACKS):
        raise SystemExit(f"không có file nhạc nền nào trong {themes.MUSIC_DIR} -- kiểm tra trước khi render")
    cinfo = {}
    for ref in dict.fromkeys(s["clip"] for s in scenes if s.get("clip")):
        cinfo[ref] = clips.ensure(ref, ffmpeg=os.path.join(FF, "ffmpeg"))
        credits.append({"kind": "clip", "text": cinfo[ref]["credit"]})
    vtags, scenes = clips.video_tags(scenes, cinfo, dur)
    (od / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(slug)) % 100000 + 7
    case = {"slug": slug, "dur": dur, "seed": seed, "accent": spec.get("accent", th["accent"]), "kicker": spec["kicker"],
            "sub": spec.get("sub", ""), "acc": spec.get("acc", []), "lines": lines, "imgs": imgs, "geo": geo, "scenes": scenes,
            "theme": th["js"]}
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
    comp = HF / "compositions" / "cases" / f"{slug}.html"
    comp.parent.mkdir(parents=True, exist_ok=True)
    comp.write_text(HTML.replace("{slug}", slug).replace("{dur}", str(dur)).replace("{title}", spec["title"])
                    .replace("{cls}", th["js"].get("cls", "")).replace("{videos}", "\n".join(vtags)), encoding="utf-8")
    sfx.build(case, od / "sfx.wav", drone=th["sound"] == "drone")
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
    music = []
    if th["sound"] == "music":
        track = themes.pick_track(slug, [f for f in themes.MIM_TRACKS if (themes.MUSIC_DIR / f).exists()])
        quiet = [(s["t0"], s["t1"]) for s in scenes if s["type"] == "question"]
        fc = themes.music_filter(th["music_gain"], quiet)
        music = ["-i", str(themes.MUSIC_DIR / track)]
        (od / "music.json").write_text(json.dumps({"file": track, "credit": themes.music_credit(track)},
                                                  ensure_ascii=False), encoding="utf-8")
    r = run([FF + r"\ffmpeg.exe", "-v", "error", "-y", "-i", str(silent), "-i", str(od / "voice.wav"), "-i", str(od / "sfx.wav"),
             *music, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
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
