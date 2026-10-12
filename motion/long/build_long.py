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
import shutil
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
from factory.render_lock import render_lock  # noqa: E402

import hf_align  # noqa: E402
import hf_geo  # noqa: E402
import build as BLD  # noqa: E402
from build import Anchors, resolve, norm  # noqa: E402  (cùng cú pháp mốc với Short S-tier)

BLD.ANCHORS |= {"sumAt", "zeroAt", "titleAt", "hAt", "countAt", "hitAt", "typeAt", "burnAt", "decodeAt", "endAt", "voiceAt", "voiceEnd", "startAt", "statAt", "fwdAt", "backAt", "drawAt",
                "chipAt", "medianAt", "hlAt", "colorAt", "strikeAt"}      # mốc riêng của cảnh video dài (breadth/basket theme chart; strikeAt: fx strike)
BLD.ANCHOR_LISTS |= {"flips", "readAt"}
import sfx_long  # noqa: E402
import chartdata  # noqa: E402

# ffmpeg: FFMPEG_DIR, rồi bản vendor của máy sản xuất, rồi ffmpeg trong PATH (máy khác).
_FF_VENDOR = r"C:\Tools\Youtuber\video-editor\vendor\ffmpeg"
FF = (os.environ.get("FFMPEG_DIR") or (_FF_VENDOR if os.path.isdir(_FF_VENDOR) else None)
      or os.path.dirname(shutil.which("ffmpeg") or "") or _FF_VENDOR)
FFMPEG = FF + r"\ffmpeg.exe"
VOICE = "Anh Khôi"
QUOTE_VOICE = "Minh Đức"     # câu {"q": 1}: lời trích nguyên văn/diễn ý, giọng khác + lọc radio
ASK_VOICE = None              # câu {"ask": 1}: "người hỏi" chen ngang (câu hỏi của người xem) -- giọng khác, KHÔNG lọc radio
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


# Bảng kênh (Grok, 06/10/2026). Spec không ghi "channel" = kênh Hình Sự, y như trước.
# MIM: giọng/theme/tên kênh/màu nhấn/bộ Beat Text riêng; ảnh chỉ PD/CC0/CC BY (không BY-SA).
def _channels() -> dict:
    sys.path.insert(0, str(ROOT / "motion" / "stier"))
    import themes
    return {"CL": {"voice": "Anh Khôi", "quote": "Minh Đức"},
            "MIM": {"voice": "Thanh Bình", "quote": "Ngọc Huyền", "theme": "lab", "brand": "MIND IN THE MACHINE",
                    "accent": "#22d3ee", "pools": themes.THEMES["mim"]["pools"], "no_sa": True},
            # Biểu Đồ Biết Nói (tài chính cá nhân): theme "chart" (chart.js: brand, candles, race, breadth, basket), vàng = giá tham chiếu
            # giọng (người dùng chọn 06/10/2026): dẫn chính Ngọc Huyền · người hỏi Phạm Tuyên · lời trích Xuân Vĩnh
            "CK": {"voice": "Ngọc Huyền", "quote": "Xuân Vĩnh", "ask": "Phạm Tuyên", "theme": "chart", "brand": "BIỂU ĐỒ BIẾT NÓI",
                   "accent": "#fbbf24", "pools": themes.THEMES["mim"]["pools"], "no_sa": True}}


CHAN: dict = {}


def license_allowed(lic: str) -> bool:
    if not FREE.search(lic) or re.search(r"\bNC\b|\bND\b|fair use", lic, re.I):
        return False
    return not (CHAN.get("no_sa") and re.search(r"by-sa|\bsa\b", lic, re.I))


def load(topic):
    global VOICE, QUOTE_VOICE, ASK_VOICE
    sd, od = paths(topic)
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    CHAN.clear()
    CHAN.update(_channels()[spec.get("channel", "CL")])
    VOICE, QUOTE_VOICE, ASK_VOICE = CHAN["voice"], CHAN["quote"], CHAN.get("ask")
    THEME["name"] = spec.get("theme", CHAN.get("theme", ""))
    BEAT2["on"] = bool(spec.get("beat2"))
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
    if isinstance(x, dict) and x.get("ask") and ASK_VOICE:
        return ASK_VOICE
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
        from factory import integrity, speak as SP
        integrity.require_speakable(text)    # trước engine VÀ trước cache: câu hỏng không được lưu lại
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
        if isinstance(x, dict) and x.get("q"):      # chỉ lời TRÍCH mới lọc radio; giọng "người hỏi" để tự nhiên
            a = radio(a, sr)
        sr0 = sr
        d = len(a) / sr
        segs.append({"index": i, "text": line_text(x), "start": round(cur, 3), "end": round(cur + d, 3),
                     **({"ask": 1} if isinstance(x, dict) and x.get("ask") else {})})
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
        out.append({"text": seg["text"], "start": seg["start"], "end": seg["end"], **({"ask": 1} if seg.get("ask") else {}),
                    "words": [{"w": x, "t": a, "d": d} for x, (a, d) in zip(toks, times)]})
    return out


# ---------------- ảnh Commons (dùng tự do, có ghi công) ----------------
def fetch_img(file: str, dst: Path, credits: dict) -> dict:
    from PIL import Image
    meta = dst.with_suffix(".json")
    if file.startswith("EXT:") and not (dst.exists() and meta.exists()):   # ảnh ngoài Commons: tải trước bằng media_search.py
        raise SystemExit(f"{file}: chưa có {dst.name} — chạy motion/long/media_search.py get/sat trước")
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
                if not license_allowed(lic):
                    raise SystemExit(f"{file}: giấy phép '{lic}' không dùng được cho kênh này")
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


# ---------------- beat text: motion/beatfx.py chọn hiệu ứng chữ (engine/beat.js), dùng chung với Short ----------------
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from beatfx import assign_beats as _assign_beats  # noqa: E402
import variety  # noqa: E402  (nhạc nền theo mood + diện mạo riêng từng video, chống "repetitive content")
THEME = {"name": ""}
BEAT2 = {"on": False}    # spec "beat2": true -> bố cục cảnh chữ + từ nhấn + giới hạn sync (PM 09/10/2026). Video cũ: tắt, y hệt từng byte.


def assign_beats(sc: list[dict], ch: dict, lines: list[dict] | None = None) -> None:
    pools = CHAN.get("pools")
    if pools and pools.get("sync") and lines:   # MIM: dòng lớn được đọc trọn -> hiện từng chữ theo giọng
        from beatfx import apply_sync
        apply_sync(sc, lines, every=3 if BEAT2["on"] else 1, max_lead=1.2 if BEAT2["on"] else None)
    _assign_beats(sc, THEME["name"] + "|" + ch.get("title", ""), pools=pools)
    if BEAT2["on"]:
        from beatfx import assign_layouts, layout_items, pick_em, pull_main
        pull_main(sc)
        assign_layouts(sc, THEME["name"] + "|" + ch.get("title", ""))
        layout_items(sc)
        pick_em(sc)


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
            if i + 1 < len(sc):     # lỗi nằm ở mốc "at" của cảnh SAU, không phải cảnh bị báo (retro 3 mục 13: "cảnh 0 (chapter) quá ngắn" ×3)
                nxt = ch["scenes"][i + 1]
                why = (f" — cảnh {i + 1} ({nxt.get('type')}) neo at={nxt.get('at')!r} trùng mốc với cảnh {i}"
                       + (" (thẻ chương luôn bắt đầu ở 0): neo cảnh sau vào câu 1 hoặc một từ ≥ 0,6 s sau đầu câu 0" if i == 0 and r["type"] == "chapter" else ""))
            else:
                why = " — cảnh cuối chạm hết chương"
            raise ValueError(f"cảnh {i} ({r['type']}) quá ngắn: {r['t0']:.2f}-{r['t1']:.2f}{why}")
        t0, t1, ty = r["t0"], r["t1"], r["type"]
        if ty == "candles":            # dữ liệu nến + chỉ báo tính ở Python (motion/long/chartdata.py), JS chỉ vẽ
            chartdata.attach(r)
        if ty == "race":
            chartdata.attach_race(r)
        if ty in ("breadth", "basket"):   # độ rộng / treemap vốn hoá HOSE (chartdata.attach_breadth / attach_basket)
            r.setdefault("drawAt", round(t0 + 0.4, 3))
            r.setdefault("until", round(max(r["drawAt"] + 0.3, min(t1 - 0.8, r["drawAt"] + (2.4 if ty == "breadth" else 2.2))), 3))
            if ty == "breadth" and r.get("animate"):
                r["animate"].setdefault("at", round(r["until"] + 0.4, 3))
                r["animate"].setdefault("until", round(max(r["animate"]["at"] + 0.5, min(t1 - 0.6, r["animate"]["at"] + 4)), 3))
            (chartdata.attach_breadth if ty == "breadth" else chartdata.attach_basket)(r)
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
    assign_beats(sc, ch, lines)
    return sc


# ---------------- lint "chữ đầu tiên đến muộn" (retro 1 mục 4 -> lặp ở retro 2 mục 2 = LỖI QUY TRÌNH) ----------------
# Luật "neo dòng đầu vào từ ĐẦU câu" có từ 06/10 nhưng không có công cụ chặn -> D1 ×4, MIM #2 ×5 màn trống 1,7–4,2 s.
# Lint đọc chính danh sách cảnh sẽ nướng vào data.js: cảnh KHÔNG có nền (img/vid/bg) mà phần tử đầu tiên hiện > LATE_MAX
# giây sau đầu cảnh -> `html` cảnh báo, `render` từ chối (trừ khi --allow-late). Hiệu chỉnh 07/10 trên mim-ai-voice +
# ck-c2-phien-giao-dich: 0 cảnh vượt (kinetic sớm nhất ≤ 0,4 s; slam ≤ 0,76 s; counter ≤ 0,2 s).
LATE_MAX = 1.0
# Loại cảnh mà engine tự dựng khung/tiêu đề trong ≤ 0,5 s đầu cảnh, độc lập với mốc neo (casewide.js/lab.js/chart.js):
# thẻ chương, logo, màn kết, câu hỏi, giấy trích, sổ, khung biểu đồ (tiêu đề t0+0.1), cửa sổ chat, ảnh in/ảnh, hồ sơ, bản đồ.
FRAME_TYPES = {"chapter", "brand", "endcard", "question", "quote", "ledger", "bars", "chat", "print", "photo", "broll", "file",
               "candles", "race", "breadth", "basket", "book", "map", "guess", "nn", "go"}   # 3 cuối: lab.js (khung ≤ t0+0.2)
_NOT_START = {"t0", "t1", "until", "voiceEnd", "endAt", "typeDur", "burnDur", "dur"}
_DATA_LISTS = {"dots", "rects", "vals", "bars", "candles", "ohlc", "series"}     # mảng số liệu biểu đồ, không phải mốc


def _starts(o, key=None):
    """Mọi mốc BẮT ĐẦU hiện (at, *At, flips, wt[0]) trong một cảnh đã plan."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in _NOT_START:
                yield from _starts(v, k)
    elif isinstance(o, list):
        if key in _DATA_LISTS:
            return
        if key == "wt":
            if o and isinstance(o[0], (int, float)):
                yield float(o[0])
            return
        for v in o:
            yield from _starts(v, key)
    elif isinstance(o, (int, float)) and not isinstance(o, bool) and key and (key == "at" or key.endswith("At") or key == "flips"):
        yield float(o)


def first_delay(s: dict) -> float | None:
    """Giây từ đầu cảnh tới lúc phần tử đầu tiên của cảnh hiện (theo cách engine dựng). None = không có mốc nào."""
    ts = [t for t in _starts(s) if t >= s["t0"] - 0.5]
    if not ts:
        return None
    d = min(ts) - s["t0"]
    if s["type"] == "kinetic" and d > 2.0:     # casewide.js B.kinetic: dòng đầu đến muộn > 2 s -> kéo về t0+0.5
        d = 0.5
    return d


def late_first(scenes: list[dict], ch: str = "") -> list[str]:
    """Cảnh trống đầu: [chương, chỉ số cảnh, loại, độ trễ]. Counter: số đứng yên ở giá trị `from` (vd. "+0%") tới lúc đếm
    -> sai nghĩa dù có nền (retro 2 mục 3), nên soi cả khi có ảnh/clip."""
    out = []
    for i, s in enumerate(scenes):
        ty = s.get("type", "?")
        if ty == "counter":
            d = s.get("at", s["t0"]) - s["t0"]
            if d > LATE_MAX:
                out.append(f"{ch} cảnh {i} counter: số đứng yên ở {s.get('prefix', '')}{s.get('from', 0)}{s.get('suffix', '')} "
                           f"{d:.1f}s rồi mới đếm (bỏ countAt hoặc neo vào từ đầu câu)")
            continue
        if ty in FRAME_TYPES or s.get("img") or s.get("vid") or s.get("bg"):
            continue
        d = first_delay(s)
        if d is not None and d > LATE_MAX:
            out.append(f"{ch} cảnh {i} {ty}: phần tử đầu tiên hiện sau {d:.1f}s — màn trống (neo dòng đầu vào từ ĐẦU câu, "
                       f"hoặc thêm nền img/bg)")
    return out


def late_report(topic, only=None) -> list[str]:
    """Đọc data.js đã dựng của các chương (sẽ render) -> danh sách cảnh trống đầu."""
    spec, chs, od = load(topic)
    out = []
    for name, _ in chs:
        f = od / name / "data.js"
        if only and name not in only:
            continue
        if not f.exists():      # `html` hỏng giữa chừng -> chương không có data.js; trước đây bị bỏ qua và báo "OK" (MIM #7 09/10)
            out.append(f"{name}: THIẾU data.js — `html` chưa dựng được chương này (xem lỗi của lệnh html)")
            continue
        case = json.loads(f.read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
        out += late_first(case["scenes"], name)
        if BEAT2["on"]:      # beat2: cả dòng CHÍNH cũng phải hiện sớm (late_first chỉ nhìn phần tử đầu tiên)
            from beatfx import light_start, overflow_lines
            out += light_start(case["scenes"], name)
            # tràn chữ vượt cả mức beat2.js tự co (40%) = chắc chắn cắt mép -> render từ chối như màn trống (retro 3 mục 15, LỖI QUY TRÌNH)
            out += [w for w in overflow_lines(case["scenes"], name) if "CẮT MÉP" in w]
    return out


# ---------------- lint mốc cảnh trùng thẻ chương (retro 3 mục 13: lặp 3 lần trong một ngày — MIM #6 ch04–07, D2 ch01–02, MIM #7 ch06) -------
# Thẻ chương (cảnh 0) luôn bắt đầu ở 0; cảnh 1 neo vào câu 0 / chữ đầu câu 0 -> cũng ở ~0 -> plan() báo "cảnh 0 (chapter) quá ngắn"
# giữa lúc `html` (sau TTS, sau khi tải ảnh, có khi trong chuỗi render). Lint TĨNH (không cần timing) chạy trước TTS và trước html,
# báo MỌI chương cùng lúc, nêu đúng cảnh cần sửa.
EARLY_WORDS = 2       # chữ thứ 1–2 của câu 0 (≈ < 0,6 s) coi là trùng mốc thẻ chương


def chapter_collisions(chs) -> list[str]:
    out = []
    for name, ch in chs:
        scenes, lines = ch.get("scenes") or [], ch.get("lines") or []
        if len(scenes) < 2 or scenes[0].get("type") != "chapter":
            continue
        at, bad = scenes[1].get("at"), False
        if isinstance(at, bool) or at is None:
            bad = at is None
        elif isinstance(at, int):
            bad = at == 0
        elif isinstance(at, float):
            bad = at < 0.6
        elif isinstance(at, list) and at and at[0] == 0:
            off = at[3] if len(at) > 3 else 0.0
            if len(at) < 2 or at[1] is None:
                bad = off < 0.6
            elif lines:
                ws = [norm(w) for w in line_text(lines[0]).split()]
                hits = [k for k, w in enumerate(ws) if w == norm(str(at[1]))]
                n = at[2] if len(at) > 2 else 0
                bad = n < len(hits) and hits[n] < EARLY_WORDS and off < 0.6
        if bad:
            out.append(f"{name} cảnh 1 ({scenes[1].get('type')}) neo at={at!r} trùng mốc 0 với thẻ chương (cảnh 0) — neo vào câu 1, "
                       f"hoặc một chữ từ thứ {EARLY_WORDS + 1} trở đi của câu 0")
    return out


def scene_gate(chs) -> None:
    bad = chapter_collisions(chs)
    if bad:
        raise SystemExit("lint cảnh (sửa gen_scenes.py rồi chạy lại):\n  " + "\n  ".join(bad))


def integrity_gate(chs, allow_repeat: bool = False) -> None:
    """Cổng toàn vẹn TRƯỚC TTS (retro 2 mục 16) — cùng luật với motion/long/script_lines.py, cho cả chNN.json sửa tay."""
    import script_lines
    bad = script_lines.gate([{"name": n, "lines": c["lines"]} for n, c in chs], allow_repeat)
    if bad:
        raise SystemExit("integrity: lời đọc chưa qua cổng, chưa đọc câu nào:\n  " + "\n  ".join(bad)
                         + "\n(câu lặp cố ý: thêm --allow-repeat-line)")


HTML = """<!doctype html>
<html lang="vi" data-resolution="landscape">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="{fonts}" rel="stylesheet" />
<link rel="stylesheet" href="assets/engine/casewide.css" />
<link rel="stylesheet" href="assets/engine/beat.css" />
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
<script src="assets/engine/beat.js"></script>
<script src="assets/engine/lab.js"></script>
<script src="assets/engine/chart.js"></script>
<script src="assets/engine/casewide.js"></script>
</body>
</html>
"""


B2_CSS = '<link rel="stylesheet" href="assets/engine/beat2.css" />\n'
B2_JS = '<script src="assets/engine/beat2.js"></script>\n'


def beat2_advice(spec: dict) -> str | None:
    """Kênh MIM/CK mà spec chưa bật beat2 -> engine chữ cũ (sync mờ chờ lời, khuôn lặp): MIM #5 09/10 có 9 đoạn trống ở QA final,
    phải bật beat2 rồi render lại (retro 3 mục 17). Chỉ nhắc (video cũ dựng lại giữ đúng hình cũ)."""
    if spec.get("channel") in ("MIM", "CK") and not spec.get("beat2"):
        return f"spec chưa bật \"beat2\": true (kênh {spec['channel']}) — engine chữ cũ gây màn trống/lặp khuôn (retro 3 mục 17)"
    return None


def html_for() -> str:
    """HTML của composition; beat2 bật -> thêm beat2.css (sau beat.css) + beat2.js (sau beat.js, trước casewide.js).
    beat2 tắt -> đúng HTML cũ từng byte (render_key của video cũ không đổi)."""
    if not BEAT2["on"]:
        return HTML
    h = HTML.replace('beat.css" />\n', 'beat.css" />\n' + B2_CSS, 1).replace('beat.js"></script>\n', 'beat.js"></script>\n' + B2_JS, 1)
    assert B2_CSS in h and B2_JS in h
    return h


def run(cmd, extra_env=None, **kw):
    env = os.environ.copy()
    env["PATH"] = FF + os.pathsep + env["PATH"]
    env.update(extra_env or {})
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
    if beat2_advice(spec):
        print(f"  ! WARNING {beat2_advice(spec)}", flush=True)
    variety.resolve_bgm(topic, spec, chs, od)   # bgm {"mood": ...} -> file cụ thể, tối thiểu trùng với video gần đây (retro 3 mục 9)
    look = variety.look(spec.get("look"))
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
        ec = spec.get("endcard", 0) if name == spec["chapters"][-1] else 0
        if ec:   # 20 giây cuối cho end screen: kéo dài chương cuối, nhạc nền chạy tiếp rồi tắt dần
            scenes.append({"type": "endcard", "t0": d, "t1": d + ec, "bg": spec.get("endcardBg"),
                           "sub": spec.get("endcardSub", None if THEME["name"] == "lab" else "HỒ SƠ TIẾP THEO")})
            d = d + ec
        vids = []
        for k, s in enumerate(scenes):
            if s.get("vid"):
                vid = str(s["vid"])
                src = od / "broll" / f"{vid}.mp4"
                import mediafit
                if src.exists() and mediafit.decide(*mediafit.probe(src), 1920, 1080) == "blur":
                    fit = od / "broll" / f"{vid}fit.mp4"     # tên chỉ gồm số + "fit": khớp regex kiểm clip lúc render
                    if not fit.exists():
                        mediafit.fit_video(src, fit, 1920, 1080, seconds=600)
                        print(f"  mediafit: clip {vid} lệch khung ngang -> đặt trọn hình trên nền nhoè ({fit.name})")
                    src, vid = fit, f"{vid}fit"
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
        case = {"topic": topic, "ch": name, "dur": d, "seed": seed, "accent": spec.get("accent", CHAN.get("accent", "#e2402d")), "look": look,
                "theme": THEME["name"] or None, **({"brand": CHAN["brand"]} if CHAN.get("brand") else {}), "autoTr": spec.get("autoTr", spec.get("theme") == "shanghai"), "hud": ch.get("hud", {}),
                "acc": spec.get("acc", []) + ch.get("acc", []), "lines": lines, "imgs": imgs, "geo": geo, "scenes": scenes,
                "prog0": round(acc_t / total, 5), "prog1": min(1.0, round((acc_t + d) / total, 5))}
        (od / name / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
        comp = HF / "compositions" / "long" / f"{topic}_{name}.html"
        comp.parent.mkdir(parents=True, exist_ok=True)
        comp.write_text(html_for().replace("{fonts}", variety.fonts_url(spec.get("look"))).replace("{data}", f"assets/long/{topic}/{name}/data.js").replace("{dur}", f"{d:.3f}")
                        .replace("{title}", spec["title"]).replace("{videos}", "\n".join(vids)), encoding="utf-8")
        sfx_long.build(case, od / name / "sfx.wav")
        quiet = [(s["t0"], s["t1"]) for s in scenes if s["type"] == "question"]
        quiet += [(s["at"] - 1.0, s["at"] + 0.4) for s in scenes if s["type"] == "slam" and spec.get("slamDrop", True)]
        quiet += [(s["t0"] - 0.2, s["t1"]) for s in scenes if s["type"] == "brand"]   # né nhạc nền cho âm hiệu kênh
        mix_chapter(ch, od / name, d, quiet, spec.get("master", True), bgm_items(ch, lines, d))
        print(f"{name}: {len(scenes)} cảnh, {len(vids)} clip, {d:.1f}s -> {comp.name}", flush=True)
        for w in late_first(scenes, name):      # cảnh báo sớm; `render` sẽ từ chối nếu chưa sửa
            print(f"  ! WARNING màn trống đầu cảnh: {w}", flush=True)
        if BEAT2["on"]:
            from beatfx import light_start
            for w in light_start(scenes, name):
                print(f"  ! WARNING đầu cảnh chỉ có chữ nhỏ: {w}", flush=True)
        if BEAT2["on"]:    # tràn chữ beat2 (retro 3 mục 15: D2, C4 lên kênh mang lỗi cắt mép; QA khung hình không bắt)
            from beatfx import overflow_lines
            for w in overflow_lines(scenes, name):
                print(f"  ! WARNING tràn chữ beat2: {w}", flush=True)
        if BEAT2["on"]:    # chữ trên màn hình chép nguyên lời đọc = phụ đề phóng to (PM 09/10/2026)
            from beatfx import verbatim_share
            hit, tot = verbatim_share(scenes, lines)
            if tot and hit / tot > 0.4:
                print(f"  ! WARNING {name}: {hit}/{tot} dòng chữ lớn chép nguyên lời đọc — đổi thành từ khoá, con số, vế đối lập", flush=True)
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


def render_key(topic, name, od, draft) -> str:
    """Băm mọi thứ quyết định hình của chương: data.js, composition, engine js/css, các clip B-roll dùng tới."""
    hsh = hashlib.sha1(b"draft" if draft else b"final")
    comp = HF / "compositions" / "long" / f"{topic}_{name}.html"
    for f in [od / name / "data.js", comp] + [HF / "assets" / "engine" / n for n in ("casewide.js", "casewide.css", "beat.js", "beat.css")]:
        hsh.update(f.read_bytes())
    if "beat2.js" in comp.read_text(encoding="utf-8"):     # chỉ video beat2 nạp 2 file này -> key video cũ không đổi
        for n in ("beat2.js", "beat2.css"):
            hsh.update((HF / "assets" / "engine" / n).read_bytes())
    for vid in sorted(set(re.findall(r"broll/(\d+(?:fit)?)\.mp4", comp.read_text(encoding="utf-8")))):
        hsh.update(vid.encode())
    return hsh.hexdigest()[:16]


def do_render(topic, only=None, draft=False, force=False):
    spec, chs, od = load(topic)
    for name, ch in chs:
        if only and name not in only:
            continue
        t0 = time.time()
        out = od / name / ("draft.mp4" if draft else "silent.mp4")
        key, kf = render_key(topic, name, od, draft), out.with_suffix(".key")
        if not force and out.exists() and kf.exists() and kf.read_text() == key:
            print(f"{name}: không đổi, bỏ qua", flush=True)
            continue
        cmd = ["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
               f"compositions/long/{topic}_{name}.html", "-o", str(out), "--fps", "30", "--quiet"]
        cmd += ["-q", "draft"] if draft else ["--crf", "20"]
        with render_lock(f"long {topic} {name}"):   # một render một lúc trên cả máy (retro mục 9)
            r = run(cmd, cwd=HF, extra_env={"HF_CAPTURE_PARALLEL_STREAM": "true"} if spec.get("stream", True) else None)
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"{name}: render hỏng\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
        kf.write_text(key)
        if draft:   # bản nháp có tiếng để xem nhanh
            run([FFMPEG, "-v", "error", "-y", "-i", str(out), "-i", str(od / name / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                 "-c:a", "aac", "-b:a", "160k", "-shortest", str(od / name / "draft_av.mp4")])
        print(f"{name}: {out.name} ({time.time() - t0:.0f}s)", flush=True)


def cmd_render(topic, only=None, rest=()):
    """`render`: lint màn trống đầu cảnh TRƯỚC khi xếp hàng render (retro 1 mục 4 lặp ở retro 2 mục 2: chặn bằng máy)."""
    late = late_report(topic, only)
    if late and "--allow-late" not in rest:
        raise SystemExit("màn trống đầu cảnh (phần tử đầu tiên > %.1fs, cảnh không nền):\n  " % LATE_MAX + "\n  ".join(late)
                         + "\nSửa neo trong gen_scenes.py rồi chạy lại `html`, hoặc thêm --allow-late nếu đã xem và chấp nhận.")
    for w in late:
        print(f"  ! WARNING (--allow-late) {w}", flush=True)
    try:     # engine đổi mà chưa soát gallery chữ có dấu (retro 2 mục 4) -> nhắc, không chặn
        import diacritics_gallery
        th = THEME["name"]
        if th in diacritics_gallery.THEMES and th in diacritics_gallery.stale():
            print(f"  ! WARNING engine đã đổi từ lần soát dấu cuối: python motion/long/diacritics_gallery.py render {th}", flush=True)
    except Exception as e:      # noqa: BLE001
        print(f"  ! WARNING không kiểm được gallery dấu: {e}", flush=True)
    with render_lock(f"long {topic} (cả lượt)"):   # giữ khoá cả lượt: không bị render khác chen giữa các chương
        do_render(topic, only, draft="--draft" in rest, force="--force" in rest)


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
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    topic, cmd, *rest = sys.argv[1:]
    only = [x for x in rest if not x.startswith("--")] or None
    if cmd in ("tts", "takes"):     # cổng toàn vẹn trước MỌI lần gọi TTS (retro 2 mục 16)
        integrity_gate(load(topic)[1], allow_repeat="--allow-repeat-line" in rest)
    if cmd in ("tts", "takes", "html"):      # mốc cảnh trùng thẻ chương: báo mọi chương TRƯỚC khi tốn TTS/tải ảnh (retro 3 mục 13)
        scene_gate([(n, c) for n, c in load(topic)[1] if not only or n in only])
    if cmd == "tts":
        do_tts(topic, only)
    elif cmd == "html":
        do_html(topic, only)
        for x in variety.audit(topic):
            print("  ! variety:", x)
    elif cmd == "render":
        cmd_render(topic, only, rest)
    elif cmd == "takes":
        nums = [x for x in rest if x.isdigit()]
        do_takes(topic, int(nums[0]) if nums else 3, [x for x in (only or []) if not x.isdigit()] or None)
    elif cmd == "pick":
        do_pick(topic)
    elif cmd == "final":
        bad = variety.audit(topic)
        if bad and "--allow-repeat" not in rest:   # quá giống video gần đây: rủi ro "repetitive content" cho cả kênh
            raise SystemExit("variety audit:\n  " + "\n  ".join(bad) + "\nĐổi nhạc/look rồi dựng lại, hoặc thêm --allow-repeat nếu chấp nhận.")
        do_final(topic)
