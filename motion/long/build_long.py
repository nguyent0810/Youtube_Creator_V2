"""Dựng video DÀI 16:9 từ spec theo chương: giọng đọc -> mốc từng từ -> ảnh/video -> HTML -> render -> âm thanh -> ghép.

    python motion/long/build_long.py <topic> tts                # đọc hết các chương (cache theo từng câu), in thời lượng
    python motion/long/build_long.py <topic> html [chNN ...]    # dựng data.js + composition (không render)
    python motion/long/build_long.py <topic> render [chNN ...] [--draft]
    python motion/long/build_long.py <topic> final              # nối các chương + nhạc nền + loudnorm -> final.mp4

Spec: data/long/<topic>/spec.json (chung: title, accent, acc, imgs{key: "File:..."}, geo{name: {...}}, chapters[])
      data/long/<topic>/chNN.json (mỗi chương: hud{k,t}, bgm{file, at, gain}, lines[], scenes[]).
Một câu (line) là chuỗi, hoặc {"t": "...", "p": giây_nghỉ_sau}. Nghỉ mặc định 0.32s, sau câu hỏi 0.6s.
Mốc thời gian trong scenes giống motion/stier/build.py: i = đầu câu i; [i, "từ", n, lệch]; số thực = giây tuyệt đối.
Cảnh có "vid": "<id Pexels>" (+ "ms" giây bắt đầu trong clip) -> thẻ <video> nướng tĩnh vào HTML.
Ảnh Commons nhận PD/CC0/CC BY/CC BY-SA (không NC/ND); ghi công tự động vào credits.json cho mô tả video.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HF = ROOT / "motion" / "hf"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "motion"))
sys.path.insert(0, str(ROOT / "motion" / "stier"))
sys.path.insert(0, str(HERE))

import hf_align  # noqa: E402
import hf_geo  # noqa: E402
import build as BLD  # noqa: E402
from build import Anchors, resolve, norm  # noqa: E402  (cùng cú pháp mốc với Short S-tier)

BLD.ANCHORS |= {"sumAt", "zeroAt", "titleAt", "hAt", "countAt", "hitAt", "typeAt", "burnAt", "decodeAt", "endAt", "voiceAt", "voiceEnd"}      # mốc riêng của cảnh video dài
BLD.ANCHOR_LISTS |= {"flips", "readAt"}
import sfx_long  # noqa: E402

FF = r"C:\Tools\Youtuber\video-editor\vendor\ffmpeg"
FFMPEG = FF + r"\ffmpeg.exe"
VOICE = "Anh Khôi"
QUOTE_VOICE = "Minh Đức"     # câu {"q": 1}: lời trích nguyên văn/diễn ý, giọng khác + lọc radio
UA = {"User-Agent": "yt-factory/1.0 (documentary research; contact via channel)"}
FREE = re.compile(r"public domain|^pd|cc0|no restrictions|^cc by(-sa)? ?\d|^cc-by", re.I)
# mastering giọng đọc (đã duyệt ở bản thử Mafia): cắt ù, bớt đục 200Hz, sáng 3.2kHz, khử xì, nén nhẹ.
# Chỉ áp ở bước trộn — mốc chữ vẫn lấy từ voice.wav thô. spec "master": false để tắt (Yakuza đã đăng bản thô).
VOICE_FX = ("highpass=f=70,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.4:g=2.5,deesser=i=0.4,"
            "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2")
TAIL = 0.9          # giây thở cuối mỗi chương
_engine = None


def paths(topic):
    return ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic


SAY_EXACT = {}
SAY = {}   # chữ hiển thị -> cách đọc cho TTS (spec["say"]); phụ đề vẫn giữ chữ gốc


def load(topic):
    sd, od = paths(topic)
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    SAY.clear()
    SAY_EXACT.clear()
    for k, v in (spec.get("say") or {}).items():   # "=Di": khớp ĐÚNG hoa/thường (tránh "di cư" thành "Đi cư")
        (SAY_EXACT.__setitem__(k[1:], v) if k.startswith("=") else SAY.__setitem__(k.lower(), v))
    chs = [(c, json.loads((sd / f"{c}.json").read_text(encoding="utf-8"))) for c in spec["chapters"] if (sd / f"{c}.json").exists()]
    return spec, chs, od


def line_text(x):
    return x["t"] if isinstance(x, dict) else x


def _core(tok):
    m = re.match(r"^([\"“(]*)(.*?)([\"”)…,.;:?!]*)$", tok)
    return m.group(1), m.group(2), m.group(3)


def spoken(text: str) -> str:
    out = []
    for tok in text.split():
        a, c, z = _core(tok)
        out.append(a + SAY_EXACT.get(c, SAY.get(c.lower(), c)) + z)
    return " ".join(out)


def line_pause(x):
    if isinstance(x, dict) and "p" in x:
        return x["p"]
    t = line_text(x).rstrip()
    return 0.6 if t.endswith("?") else 0.45 if t.endswith("…") else 0.32


# ---------------- giọng đọc: cache THEO CÂU (sửa một câu không phải đọc lại cả chương) ----------------
def _key(text: str, take: int = 0, voice: str = VOICE) -> str:
    """take 0 giữ đúng hash cũ (cache Yakuza còn dùng được); take k>0 là bản đọc lại khác của cùng câu."""
    return hashlib.sha1((voice + "|" + text + (f"|t{take}" if take else "")).encode("utf-8")).hexdigest()[:16]


def line_voice(x) -> str:
    return QUOTE_VOICE if isinstance(x, dict) and x.get("q") else VOICE


def radio(a, sr):
    """Lời trích: băng thông điện thoại/radio cũ 300-3400 Hz -> tách hẳn khỏi giọng kể."""
    from scipy.signal import butter, sosfilt
    sos = butter(4, [300, 3400], btype="bandpass", fs=sr, output="sos")
    return (sosfilt(sos, a) * 1.4).astype("float32")


def tts_line(text: str, cache: Path, take: int = 0, voice: str = VOICE):
    import soundfile as sf
    global _engine
    p = cache / f"{_key(text, take, voice)}.wav"
    if not p.exists():
        from factory import speak as SP
        if _engine is None:
            _engine = SP._load_engine()
        a = _engine.infer(text, voice=voice)     # vieneu 3.8.3: "Anh Khôi" là alias của "Thiện Minh" (cùng embedding)
        cache.mkdir(parents=True, exist_ok=True)
        sf.write(str(p), a, SP.SAMPLE_RATE)
    a, sr = sf.read(str(p), dtype="float32")
    return a, sr


def _picks(cache: Path) -> dict:
    f = cache / "picks.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def speak(ch_lines, od: Path, name: str) -> dict:
    import numpy as np
    import soundfile as sf
    picks = _picks(od / "tts")       # câu nào đã chấm best-of-N thì dùng bản thắng, chưa chấm thì take 0
    parts, segs, cur, sr0 = [], [], 0.0, None
    for i, x in enumerate(ch_lines):
        sp, v = spoken(line_text(x)), line_voice(x)
        a, sr = tts_line(sp, od / "tts", picks.get(_key(sp, 0, v), 0), v)
        if v != VOICE:
            a = radio(a, sr)
        sr0 = sr
        d = len(a) / sr
        segs.append({"index": i, "text": line_text(x), "start": round(cur, 3), "end": round(cur + d, 3)})
        gap = np.zeros(int(line_pause(x) * sr), dtype="float32")
        parts += [a, gap]
        cur += d + len(gap) / sr
    parts.append(np.zeros(int(TAIL * sr0), dtype="float32"))
    wav = od / name / "voice.wav"
    wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(wav), np.concatenate(parts), sr0)
    return {"duration": round(cur + TAIL, 3), "segments": segs}


# ---------------- best-of-N: đọc mỗi câu N lần, Whisper nghe lại, chọn bản khớp chữ nhất ----------------
# vieneu không tất định: cùng câu mỗi lần đọc một khác, đôi khi đọc sai số ("57" -> "27") hay nuốt chữ.
#   1) build_long.py <topic> takes [N=3]      (venv vieneu)  -> tts/takes.json
#   2) stt_takes.py <topic>                   (.venv-video, CUDA) -> tts/transcripts.json
#   3) build_long.py <topic> pick             (venv vieneu)  -> tts/picks.json, rồi chạy lại `tts`
def do_takes(topic, n=3, only=None):
    spec, chs, od = load(topic)
    cache, rows, t0 = od / "tts", [], time.time()
    for name, ch in chs:
        if only and name not in only:
            continue
        for x in ch["lines"]:
            sp, v = spoken(line_text(x)), line_voice(x)
            files = []
            for k in range(n):
                tts_line(sp, cache, k, v)
                files.append(f"{_key(sp, k, v)}.wav")
            rows.append({"key": _key(sp, 0, v), "ch": name, "text": sp, "files": files})
        print(f"{name}: {len(ch['lines'])} câu x{n} ({time.time() - t0:.0f}s)", flush=True)
    (cache / "takes.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"takes.json: {len(rows)} câu")


def _chars(text: str, nz) -> str:
    """So theo KÝ TỰ, bỏ khoảng trắng/dấu câu: tên Ý Whisper viết dính ("Capachy" ~ "Ca pa chi") chỉ lệch 1-2 ký tự,
    còn đọc sai số ("hai mươi bảy" thay "năm mươi bảy") vẫn lệch rõ."""
    return "".join(re.findall(r"[^\W_]+", nz.normalize(text).lower()))


def _edit(a, b) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def do_pick(topic):
    """Lỗi = khoảng cách sửa theo KÝ TỰ / độ dài (cả hai phía qua cùng bộ chuẩn hoá của vieneu: số -> chữ).
    Hoà thì chọn bản có độ dài gần trung vị nhất (tránh bản kéo lê / đọc vội)."""
    import soundfile as sf
    from vieneu_utils.phonemize_text import PuncNormalizer
    nz = PuncNormalizer()
    spec, chs, od = load(topic)
    cache = od / "tts"
    rows = json.loads((cache / "takes.json").read_text(encoding="utf-8"))
    hyp = json.loads((cache / "transcripts.json").read_text(encoding="utf-8"))
    picks, bad, gain = _picks(cache), [], 0
    for r in rows:
        ref = _chars(r["text"], nz)
        sc = []
        for k, f in enumerate(r["files"]):
            if f not in hyp:
                continue
            e = _edit(ref, _chars(hyp[f], nz)) / max(1, len(ref))
            sc.append((k, e, sf.info(str(cache / f)).duration))
        if not sc:
            continue
        med = sorted(d for _, _, d in sc)[len(sc) // 2]
        k, e, _ = min(sc, key=lambda z: (round(z[1], 3), abs(z[2] - med)))
        gain += sc[0][1] > e
        picks[r["key"]] = k
        if e > 0.08:
            bad.append((r["ch"], e, r["text"], hyp[r["files"][k]]))
    (cache / "picks.json").write_text(json.dumps(picks, indent=1), encoding="utf-8")
    print(f"picks.json: {len(picks)} câu; {gain} câu bản 0 kém hơn bản được chọn")
    for ch, e, t, h in sorted(bad, key=lambda z: -z[1]):
        print(f"  ! {ch} {e:.0%}\n    viết: {t}\n    nghe: {h}")


def word_lines(t: dict, wav: Path) -> list[dict]:
    env, hop = hf_align.energy_envelope(wav)
    out = []
    for seg in t["segments"]:
        toks = seg["text"].split()
        wts = [sum(hf_align.token_weight(y) for y in spoken(x).split()) for x in toks]   # chữ đọc khác -> trọng số theo cách đọc
        times = hf_align.word_times(env, hop, seg["start"], seg["end"], wts)
        out.append({"text": seg["text"], "start": seg["start"], "end": seg["end"],
                    "words": [{"w": x, "t": a, "d": d} for x, (a, d) in zip(toks, times)]})
    return out


# ---------------- ảnh Commons (dùng tự do, có ghi công) ----------------
def fetch_img(file: str, dst: Path, credits: dict) -> dict:
    from PIL import Image
    meta = dst.with_suffix(".json")
    if not dst.exists() or not meta.exists():
        def info(width=None):
            prm = {"action": "query", "prop": "imageinfo", "titles": file, "iiprop": "url|size|extmetadata", "format": "json", "formatversion": "2"}
            if width:
                prm["iiurlwidth"] = width
            with urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(prm), headers=UA), timeout=60) as r:
                return json.loads(r.read())["query"]["pages"][0]["imageinfo"][0]
        for k in range(6):
            try:
                ii = info()
                Wd = next((w for w in (1920, 1280, 960, 500, 330) if w < ii["width"]), None)   # bản gốc bị 429 -> thumb cỡ chuẩn
                if Wd:
                    ii = info(Wd)
                md = ii.get("extmetadata", {})
                lic = md.get("LicenseShortName", {}).get("value", "")
                if not FREE.search(lic) or re.search(r"\bNC\b|\bND\b|fair use", lic, re.I):
                    raise SystemExit(f"{file}: giấy phép '{lic}' không dùng tự do được")
                artist = re.sub(r"<[^>]+>", "", md.get("Artist", {}).get("value", "")).strip()[:120]
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
        meta.write_text(json.dumps({"file": file, "license": lic, "artist": artist}, ensure_ascii=False), encoding="utf-8")
        time.sleep(1.0)
    m = json.loads(meta.read_text(encoding="utf-8"))
    if not re.search(r"public domain|^pd|cc0|no restrictions", m["license"], re.I):
        credits[file] = m
    with Image.open(dst) as im:
        return {"w": im.size[0], "h": im.size[1], "lic": m["license"], "by": m.get("artist", ""),
                "pd": bool(re.search(r"public domain|^pd|cc0|no restrictions", m["license"], re.I))}


def probe_dur(p: Path) -> float:
    r = subprocess.run([FF + r"\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------------- kế hoạch cảnh ----------------
def plan(ch: dict, lines: list[dict], dur: float) -> list[dict]:
    A = Anchors(lines)
    sc = []
    for i, s in enumerate(ch["scenes"]):
        r = resolve({k: v for k, v in s.items() if k != "at"}, A)
        r["t0"] = 0.0 if i == 0 else A(s["at"])
        sc.append(r)
    for i, r in enumerate(sc):
        r["t1"] = sc[i + 1]["t0"] if i + 1 < len(sc) else dur
        if r["t1"] <= r["t0"] + 0.6:
            raise ValueError(f"cảnh {i} ({r['type']}) quá ngắn: {r['t0']:.2f}-{r['t1']:.2f}")
        t0, t1, ty = r["t0"], r["t1"], r["type"]
        if ty == "date":
            r.setdefault("dayAt", t0 + 0.15)
            ng = len("".join(c if c.isdigit() else " " for c in r["date"]).split())
            r.setdefault("groupAt", [t0 + 0.4 + 0.3 * g for g in range(ng)])
        if ty == "quote":
            if "typeAt" in r:
                r["at"] = r.pop("typeAt")
            r.setdefault("at", t0 + 0.45)
            r.setdefault("typeDur", round(min(len(r["text"]) * 0.035, (t1 - r["at"]) * 0.75), 3))
        if ty == "counter":
            if "countAt" in r:
                r["at"] = r.pop("countAt")
            r.setdefault("at", t0 + 0.2)
            r.setdefault("until", round(r["at"] + min(1.8, (t1 - t0) * 0.6), 3))
        if ty == "map":
            for k, p in enumerate(r.get("pins") or []):
                p.setdefault("at", round(t0 + 0.5 + 0.35 * k, 3))
            for q in r.get("routes") or []:
                q.setdefault("until", round(q["at"] + 1.0, 3))
        if ty == "slam":
            if "hitAt" in r:
                r["at"] = r.pop("hitAt")
            r.setdefault("at", round(t0 + 0.15, 3))
        if ty == "split":
            r["a"].setdefault("at", t0 + 0.15); r["b"].setdefault("at", t0 + 0.5)
            if r.get("sign"):
                r.setdefault("signAt", t0 + 0.9)
        if ty == "bars":
            for k, q in enumerate(r["items"]):
                q.setdefault("at", round(t0 + 0.4 + 0.35 * k, 3))
        if ty == "timeline":
            for k, q in enumerate(r["items"]):
                q.setdefault("at", round(t0 + 0.3 + 0.5 * k, 3))
        if ty == "org":
            for k, q in enumerate(r["nodes"]):
                q.setdefault("at", round(t0 + 0.3 + 0.3 * k, 3))
        if ty == "cards":
            r.setdefault("flips", [round(t0 + 0.8 + 0.5 * k, 3) for k in range(len(r["cards"]))])
        if ty in ("kinetic",) or r.get("kin"):
            for k, q in enumerate(r.get("items") or r.get("kin") or []):
                q.setdefault("at", round(t0 + 0.2 + 0.4 * k, 3))
        if ty == "print" and r.get("side"):
            for k, q in enumerate(r["side"].get("lines") or []):
                q.setdefault("at", round(t0 + 0.8 + 0.6 * k, 3))
        if ty == "quote" and r.get("qline") is not None:     # câu đọc giọng trích -> sóng âm chạy đúng lúc giọng vang
            q = lines[r["qline"]]
            r.setdefault("voiceAt", q["start"]); r.setdefault("voiceEnd", q["end"]); r["radio"] = True
        if ty == "seismo":
            r.setdefault("hitAt", round(t0 + 2.0, 3))
        if ty == "saint":
            r.setdefault("burnAt", round(t0 + 1.5, 3))
            r.setdefault("burnDur", round(max(1.5, min(4.5, t1 - r["burnAt"] - 0.4)), 3))
        if ty == "pizzini":
            for k, q in enumerate(r.get("notes") or []):
                q.setdefault("at", round(t0 + 0.5 + 1.2 * k, 3))
                q.setdefault("typeDur", round(min(len(q["text"]) * 0.045, 2.6), 3))
            if r.get("cipher"):
                r["cipher"].setdefault("at", round(t0 + 0.6, 3))
                r["cipher"].setdefault("decodeAt", round(r["cipher"]["at"] + 0.3 + 0.18 * len(r["cipher"]["word"]), 3))
        if ty == "dots":
            for k, q in enumerate(r.get("groups") or []):
                q.setdefault("at", round(t0 + 1.8 + 1.2 * k, 3))
        if ty == "board":
            for k, q in enumerate(r.get("pins") or []):
                q.setdefault("at", round(t0 + 0.3 + 0.45 * k, 3))
            for k, q in enumerate(r.get("links") or []):
                q.setdefault("at", round(t0 + 0.6 + 0.45 * k, 3))
        if ty == "memorial":
            for k, q in enumerate(r["names"]):
                q.setdefault("at", round(t0 + 0.8 + 0.7 * k, 3))
        if ty == "calendar":
            r.setdefault("endAt", round(t1 - 1.0, 3))
        if ty == "sticker":
            for k, q in enumerate(r["items"]):
                q.setdefault("at", round(t0 + 0.4 + 0.7 * k, 3))
        if ty == "file":
            for k, q in enumerate(r.get("rows") or []):
                q.setdefault("at", round(t0 + 0.9 + 0.5 * k, 3))
        if ty == "ledger":
            for k, q in enumerate(r.get("rows") or []):
                q.setdefault("at", round(t0 + 0.6 + 0.5 * k, 3))
    return sc


HTML = """<!doctype html>
<html lang="vi" data-resolution="landscape">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,600;0,700;0,800;0,900;1,600&family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="assets/engine/casewide.css" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="{data}"></script>
</head>
<body>
<!-- Video dài: {title} — sinh bởi motion/long/build_long.py, đừng sửa tay. -->
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080" data-fps="30">
  <div class="layer" id="bed"></div>
{videos}
  <div class="layer" id="motes"></div>
  <div class="layer" id="stage"></div>
  <div class="layer" id="leak"></div>
  <svg class="layer" id="grain" width="1920" height="1080"><filter id="gn"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"/></filter><rect width="100%" height="100%" filter="url(#gn)"/></svg>
  <div class="layer" id="vig"></div>
  <div class="layer" id="scrims"></div>
  <div id="prog"><i></i></div>
  <div id="hud"><div class="bar"></div><div class="t"></div></div>
  <div id="caps"></div>
  <div class="layer" id="flash"></div>
</div>
<script src="assets/engine/casewide.js"></script>
</body>
</html>
"""


def run(cmd, **kw):
    env = os.environ.copy()
    env["PATH"] = FF + os.pathsep + env["PATH"]
    return subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def do_tts(topic, only=None):
    spec, chs, od = load(topic)
    tot, rows = 0.0, []
    for name, ch in chs:
        if only and name not in only:
            continue
        t = speak(ch["lines"], od, name)
        (od / name / "timing.json").write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
        syl = sum(len(line_text(x).split()) for x in ch["lines"])
        rows.append((name, syl, t["duration"]))
        tot += t["duration"]
    for name, syl, d in rows:
        print(f"{name}: {syl:5d} âm tiết  {d / 60:5.2f} phút  ({syl / (d / 60):.0f}/phút)")
    print(f"TỔNG: {sum(r[1] for r in rows)} âm tiết, {tot / 60:.2f} phút")


def do_html(topic, only=None):
    spec, chs, od = load(topic)
    durs = {}
    for name, ch in chs:
        tj = od / name / "timing.json"
        durs[name] = json.loads(tj.read_text(encoding="utf-8"))["duration"] if tj.exists() else 150.0   # chương chưa đọc: ước lượng
    total, acc_t = sum(durs.values()), 0.0
    credits = {}
    imgs = {}
    for key, file in spec.get("imgs", {}).items():
        wh = fetch_img(file, od / "img" / f"{key}.jpg", credits)
        imgs[key] = {"src": f"assets/long/{topic}/img/{key}.jpg", **wh}
    geo = {}
    for gname, g in (spec.get("geo") or {}).items():
        hf_geo.BOX = tuple(g.get("box", (180, 130, 1740, 850)))
        geo[gname] = hf_geo.bake({"countries": g["countries"], "context": g.get("context", []), "labels": g.get("labels", {}),
                                  "bbox": g["bbox"], "pins": g["pins"]})["_geo"]
    (od / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
    vdur = {}
    for name, ch in chs:
        d = durs[name]
        if only and name not in only:
            acc_t += d
            continue
        t = json.loads((od / name / "timing.json").read_text(encoding="utf-8"))
        lines = word_lines(t, od / name / "voice.wav")
        scenes = plan(ch, lines, d)
        vids = []
        for k, s in enumerate(scenes):
            if s.get("vid"):
                vid = str(s["vid"])
                src = od / "broll" / f"{vid}.mp4"
                if vid not in vdur:
                    vdur[vid] = probe_dur(src)
                ms = float(s.get("ms", 0))
                need = s["t1"] - s["t0"] + 0.5
                if ms + need > vdur[vid] + 0.05:
                    raise SystemExit(f"{name} cảnh {k}: clip {vid} dài {vdur[vid]:.1f}s, cần {ms:.1f}+{need:.1f}s")
                s["vid"] = f"v{k}"
                tone = {"bw": "bw", "noir": "noir", "color": "color", "night": "night", "dim": "dimbg", "sepia": "sepia"}[s.get("tone", "night")]
                st = max(0.0, s["t0"] - 0.2)
                vids.append(f'  <video id="v{k}" class="clip bv {tone}" src="assets/long/{topic}/broll/{vid}.mp4" data-start="{st:.3f}" '
                            f'data-duration="{min(need, d - st):.3f}" data-media-start="{ms:.2f}" muted playsinline data-track-index="1"></video>')
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(topic + name)) % 100000 + 7
        case = {"topic": topic, "ch": name, "dur": d, "seed": seed, "accent": spec.get("accent", "#e2402d"), "theme": spec.get("theme"), "hud": ch.get("hud", {}),
                "acc": spec.get("acc", []) + ch.get("acc", []), "lines": lines, "imgs": imgs, "geo": geo, "scenes": scenes,
                "prog0": round(acc_t / total, 5), "prog1": round((acc_t + d) / total, 5)}
        (od / name / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
        comp = HF / "compositions" / "long" / f"{topic}_{name}.html"
        comp.parent.mkdir(parents=True, exist_ok=True)
        comp.write_text(HTML.replace("{data}", f"assets/long/{topic}/{name}/data.js").replace("{dur}", f"{d:.3f}")
                        .replace("{title}", spec["title"]).replace("{videos}", "\n".join(vids)), encoding="utf-8")
        sfx_long.build(case, od / name / "sfx.wav")
        mix_chapter(ch, od / name, d, [(s["t0"], s["t1"]) for s in scenes if s["type"] == "question"], spec.get("master", True),
                    bgm_items(ch, lines, d))
        print(f"{name}: {len(scenes)} cảnh, {len(vids)} clip, {d:.1f}s -> {comp.name}", flush=True)
        acc_t += d


def bgm_items(ch, lines, dur) -> list[dict]:
    """bgm: một dict (cả chương) hoặc danh sách đoạn {file, at (giây trong file), gain, start, end (mốc lời), fin, fout}."""
    b = ch.get("bgm") or []
    A = Anchors(lines)
    out = []
    for q in ([b] if isinstance(b, dict) else b):
        if not q.get("file"):
            continue
        st = A(q["start"]) if q.get("start") is not None else 0.0
        en = A(q["end"]) if q.get("end") is not None else dur
        out.append({**q, "start": round(st, 3), "end": round(min(en, dur), 3)})
    return out


def mix_chapter(ch, cd: Path, dur: float, quiet=(), master=True, items=None):
    """voice + sfx + nhạc nền (né giọng) -> mix.wav 48k stereo, CHƯA loudnorm (làm một lần cho cả video).
    Nhạc nền có thể nhiều đoạn (bgm_items). Cảnh `question`: nhạc nền gần như tắt (khoảng lặng là cú đấm)."""
    if items is None:
        b = ch.get("bgm") or {}
        items = [{**b, "start": 0.0, "end": dur}] if b.get("file") else []
    duck = "".join(f",volume=enable='between(t,{a - 0.1:.2f},{z:.2f})':volume=0.12" for a, z in quiet)
    inputs = ["-i", str(cd / "voice.wav"), "-i", str(cd / "sfx.wav")]
    fc = "[0:a]aresample=48000," + (VOICE_FX + "," if master else "") + "pan=stereo|c0=c0|c1=c0,apad," + ("asplit=3[v][vk][vk2];" if items else "asplit=2[v][vk];") + "[1:a]volume=0.42[s0];[s0][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[s];"
    if items:
        tags = []
        for k, q in enumerate(items):
            inputs += ["-ss", str(q.get("at", 0)), "-i", str(cd.parent / "bgm" / q["file"])]
            L = max(0.5, q["end"] - q["start"])
            fi, fo = q.get("fin", 1.5), q.get("fout", 2.0)
            ms = int(q["start"] * 1000)
            fc += (f"[{k + 2}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{L:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={fi},"
                   f"afade=t=out:st={max(0, L - fo):.3f}:d={fo},volume={q.get('gain', 0.16)},adelay={ms}|{ms},apad[b{k}];")
            tags.append(f"[b{k}]")
        fc += "".join(tags) + f"amix=inputs={len(tags)}:normalize=0:duration=longest,atrim=0:{dur:.3f}{duck}[m0];"
        fc += ("[m0][vk2]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[m];"
               "[v][s][m]amix=inputs=3:weights='1 1 1':normalize=0:duration=first[a]")
    else:
        fc += "[v][s]amix=inputs=2:weights='1 1':normalize=0:duration=first[a]"
    r = run([FFMPEG, "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[a]", "-t", f"{dur:.3f}", "-ar", "48000", "-ac", "2", str(cd / "mix.wav")])
    if r.returncode != 0:
        raise SystemExit(f"mix hỏng {cd}: {r.stderr[-1500:]}")


def do_render(topic, only=None, draft=False):
    spec, chs, od = load(topic)
    for name, ch in chs:
        if only and name not in only:
            continue
        t0 = time.time()
        out = od / name / ("draft.mp4" if draft else "silent.mp4")
        cmd = ["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
               f"compositions/long/{topic}_{name}.html", "-o", str(out), "--fps", "30", "--quiet"]
        cmd += ["-q", "draft"] if draft else ["--crf", "20"]
        r = run(cmd, cwd=HF)
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"{name}: render hỏng\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
        if draft:   # bản nháp có tiếng để xem nhanh
            run([FFMPEG, "-v", "error", "-y", "-i", str(out), "-i", str(od / name / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                 "-c:a", "aac", "-b:a", "160k", "-shortest", str(od / name / "draft_av.mp4")])
        print(f"{name}: {out.name} ({time.time() - t0:.0f}s)", flush=True)


def do_final(topic):
    spec, chs, od = load(topic)
    lst = od / "concat.txt"
    lst.write_text("".join(f"file '{(od / n / 'silent.mp4').as_posix()}'\n" for n, _ in chs), encoding="utf-8")
    # hình render làm tròn lên khung 1/30s -> đệm tiếng từng chương cho ĐÚNG bằng hình, không thì lệch cộng dồn (~0,2s ở chương cuối)
    for n, _ in chs:
        vd = probe_dur(od / n / "silent.mp4")
        r = run([FFMPEG, "-v", "error", "-y", "-i", str(od / n / "mix.wav"), "-af", f"apad=whole_dur={vd:.6f}", "-t", f"{vd:.6f}", str(od / n / "mixpad.wav")])
        if r.returncode != 0:
            raise SystemExit(r.stderr[-1500:])
    alst = od / "concat_a.txt"
    alst.write_text("".join(f"file '{(od / n / 'mixpad.wav').as_posix()}'\n" for n, _ in chs), encoding="utf-8")
    r = run([FFMPEG, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-f", "concat", "-safe", "0", "-i", str(alst),
             "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
             "-shortest", "-movflags", "+faststart", str(od / "final.mp4")])
    if r.returncode != 0:
        raise SystemExit(r.stderr[-2000:])
    print(od / "final.mp4", f"{probe_dur(od / 'final.mp4') / 60:.2f} phút")


if __name__ == "__main__":
    topic, cmd, *rest = sys.argv[1:]
    only = [x for x in rest if not x.startswith("--")] or None
    if cmd == "tts":
        do_tts(topic, only)
    elif cmd == "html":
        do_html(topic, only)
    elif cmd == "render":
        do_render(topic, only, draft="--draft" in rest)
    elif cmd == "takes":
        nums = [x for x in rest if x.isdigit()]
        do_takes(topic, int(nums[0]) if nums else 3, [x for x in (only or []) if not x.isdigit()] or None)
    elif cmd == "pick":
        do_pick(topic)
    elif cmd == "final":
        do_final(topic)
