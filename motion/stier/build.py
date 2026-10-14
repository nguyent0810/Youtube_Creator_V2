"""Dựng một hồ sơ S-tier từ spec: giọng đọc -> mốc từng từ -> ảnh -> bản đồ -> HTML -> render -> âm thanh.

    python motion/stier/build.py <slug> [<slug> ...] [--no-render] [--draft]

Spec: data/stier/specs/<slug>.json (người viết), gồm
  title, description, tags, kicker, sub, accent?, acc[], lines[] (mỗi phần tử MỘT câu đọc),
  imgs {key: "File:....jpg"}, map? {countries, context, labels, bbox, pins}, scenes[],
  sources[] (link bài gốc để truy vết).
  say? {chữ: cách đọc} chỉ đổi lời đưa vào TTS (phụ đề giữ chữ gốc); khoá thường = không phân biệt
  hoa/thường, khoá "=ABC" = khớp đúng hoa/thường. Vd. {"=ELIZA": "Ê-li-dơ", "seoul": "Xơ-un"}.
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
from factory.render_lock import render_lock  # noqa: E402

SPECS = ROOT / "data" / "stier" / "specs"
OUT = ROOT / "output" / "stier"
# ffmpeg: FFMPEG_DIR, rồi bản vendor của máy sản xuất, rồi ffmpeg trong PATH (máy khác).
_FF_VENDOR = r"C:\Tools\Youtuber\video-editor\vendor\ffmpeg"
FF = (os.environ.get("FFMPEG_DIR") or (_FF_VENDOR if os.path.isdir(_FF_VENDOR) else None)
      or os.path.dirname(shutil.which("ffmpeg") or "") or _FF_VENDOR)
VOICE = "Anh Khôi"
UA = {"User-Agent": "yt-factory/1.0 (documentary research; contact via channel)"}
ANCHORS = {"at", "until", "cross", "reveal", "strike", "swap", "plusAt", "dayAt", "headAt", "signAt", "labelAt", "imgAt", "dimAt",
           "gapAt"}   # gapAt: cảnh chart (CK) -- phần hụt của cột
ANCHOR_LISTS = {"groupAt", "headTimes"}
_engine = None


def norm(w: str) -> str:
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


# ---------------- bảng đọc (spec "say", như build_long.spoken) ----------------
def _core(tok: str) -> tuple[str, str, str]:
    m = re.match(r"^([\"“(]*)(.*?)([\"”)…,.;:?!]*)$", tok)
    return m.group(1), m.group(2), m.group(3)


def _say_tables(say: dict | None) -> tuple[dict, dict]:
    """spec "say": {"seoul": "Xơ-un"} khớp không phân biệt hoa/thường; {"=ELIZA": "Ê-li-dơ"} khớp ĐÚNG hoa/thường
    (tránh "di cư" thành "Đi cư" khi chỉ muốn đổi tên riêng "Di")."""
    exact, low = {}, {}
    for k, v in (say or {}).items():
        k = unicodedata.normalize("NFC", k)
        if k.startswith("="):
            exact[k[1:]] = v
        else:
            low[k.lower()] = v
    return exact, low


def spoken_word(tok: str, say: dict | None) -> str:
    """Cách đọc một chữ (giữ dấu câu/ngoặc quanh chữ). Không có trong bảng -> trả nguyên chữ."""
    if not say:
        return tok
    exact, low = _say_tables(say)
    a, c, z = _core(tok)
    c0 = unicodedata.normalize("NFC", c)
    r = exact.get(c0, low.get(c0.lower()))
    return tok if r is None else a + r + z


def spoken(text: str, say: dict | None) -> str:
    """Câu đưa vào TTS. Phụ đề/chữ trên màn hình vẫn dùng câu gốc. Câu không có chữ nào trong bảng -> trả
    NGUYÊN câu (kể cả khoảng trắng) để cache giọng cũ vẫn khớp."""
    if not say:
        return text
    toks = text.split()
    out = [spoken_word(x, say) for x in toks]
    return text if out == toks else " ".join(out)


# ---------------- giọng đọc ----------------
def _old_takes(wav: Path, tjson: Path, voice: str) -> dict:
    """{câu đọc: audio} lấy lại từ voice.wav cũ cùng giọng -- đổi bảng "say" chỉ đọc lại câu có cách đọc đổi."""
    if not (tjson.exists() and wav.exists()):
        return {}
    try:
        import soundfile as sf
        t = json.loads(tjson.read_text(encoding="utf-8"))
        if t.get("voice", VOICE) != voice:
            return {}
        a, sr = sf.read(str(wav), dtype="float32")
        if sr != t.get("sample_rate", sr) or getattr(a, "ndim", 1) != 1:
            return {}
        return {s.get("say", s["text"]): a[int(round(s["start"] * sr)):int(round(s["end"] * sr))] for s in t["segments"]}
    except Exception:
        return {}


def speak(lines: list[str], wav: Path, tjson: Path, voice: str = VOICE, gap: float = 0.0, say: dict | None = None,
          tts: dict | None = None) -> dict:
    """Đọc từng câu, ghép wav + mốc câu. Cache theo CẢ lời lẫn giọng (Grok: đổi giọng mà
    lời giữ nguyên thì trước đây vẫn trả wav giọng cũ). timing.json cũ không ghi giọng
    là của VOICE mặc định (Anh Khôi) -- cache CL cũ vẫn dùng được.
    gap: giây lặng chèn SAU mỗi câu (trừ câu cuối) -- theme "ck" (giọng nhanh, kênh 'người bạn' cần chỗ thở).
    0 = như cũ; timing.json chỉ ghi "gap" khi khác 0, nên cache cũ không đổi.
    say: bảng đọc của spec (xem spoken()). TTS đọc câu đã thay; segment vẫn ghi "text" = câu GỐC (phụ đề, mốc chữ)
    và chỉ thêm "say" khi cách đọc khác -- spec không có "say" giữ nguyên timing.json/cache. Lỡ cache thì câu
    nào có cách đọc (và giọng) y như bản cũ được cắt lại từ voice.wav cũ, chỉ câu đổi cách đọc mới đọc lại."""
    global _engine
    spk = [spoken(ln, say) for ln in lines]
    if tjson.exists() and wav.exists():
        t = json.loads(tjson.read_text(encoding="utf-8"))
        if ([s["text"] for s in t["segments"]] == lines and [s.get("say", s["text"]) for s in t["segments"]] == spk
                and t.get("voice", VOICE) == voice and t.get("gap", 0.0) == gap and t.get("tts") == (tts or None)):
            return t
    import numpy as np
    import soundfile as sf
    from factory import integrity, speak as SP
    for sp in spk:                        # cả hồ sơ, trước khi đọc câu nào (đúng chuỗi sắp đưa vào TTS)
        integrity.require_speakable(sp)
    # tts (spec "tts", Short kiểu mới 12/10/2026): {"temperature": .., "pauses": {"<chỉ số câu>": giây nghỉ SAU câu đó}} --
    # nghỉ dài ngắn khác nhau như người nói (trước câu chốt nghỉ lâu hơn), thay cho khoảng nghỉ đều tăm tắp.
    kw = {k: v for k, v in (tts or {}).items() if k in ("temperature", "top_k", "top_p")}
    pauses = {int(k): float(v) for k, v in ((tts or {}).get("pauses") or {}).items()}
    old = _old_takes(wav, tjson, voice) if say and not tts else {}
    if _engine is None and any(sp not in old for sp in spk):
        _engine = SP._load_engine()
    chunks, segs, cur = [], [], 0.0
    for i, (ln, sp) in enumerate(zip(lines, spk)):
        a = old[sp] if sp in old else _engine.infer(sp, voice=voice, **kw)
        d = len(a) / SP.SAMPLE_RATE
        segs.append({"index": i, "text": ln, **({"say": sp} if sp != ln else {}),
                     "start": round(cur, 3), "end": round(cur + d, 3)})
        chunks.append(a); cur += d
        g = pauses.get(i, gap)
        if g and i < len(lines) - 1:
            chunks.append(np.zeros(int(round(g * SP.SAMPLE_RATE)), dtype=a.dtype)); cur += int(round(g * SP.SAMPLE_RATE)) / SP.SAMPLE_RATE
    wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(wav), np.concatenate(chunks), SP.SAMPLE_RATE)
    t = {"sample_rate": SP.SAMPLE_RATE, "duration": round(cur, 3), "voice": voice, "segments": segs}
    if gap:
        t["gap"] = gap
    if tts:
        t["tts"] = tts
    tjson.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    return t


def _weight(tok: str, say: dict | None) -> float:
    """Trọng số thời lượng của MỘT chữ gốc: chữ có cách đọc riêng thì tính theo cách đọc ("Ê-li-dơ" = 3 âm tiết)."""
    sp = spoken_word(tok, say)
    if sp == tok:
        return hf_align.token_weight(tok)
    return sum(hf_align.token_weight(y) for y in re.split(r"[\s\-‐–]+", sp) if y)


def word_lines(t: dict, wav: Path, say: dict | None = None) -> list[dict]:
    """Mốc từng chữ GỐC (phụ đề, karaoke, neo [i, "chữ"] dùng chữ trên màn hình, không dùng cách đọc)."""
    env, hop = hf_align.energy_envelope(wav)
    out = []
    for seg in t["segments"]:
        toks = seg["text"].split()
        times = hf_align.word_times(env, hop, seg["start"], seg["end"], [_weight(x, say) for x in toks])
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


def fetch_local(rel: str, dst: Path) -> dict:
    """Ảnh của CHÍNH kênh trong máy (vd. "local:output/channels/CK/logo.png"): chép sang jpg, không ghi công."""
    from PIL import Image
    src = ROOT / rel
    if not src.exists():
        raise SystemExit(f"local:{rel}: không có file")
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (10, 20, 38)); im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(dst, quality=92)
    dst.with_suffix(".json").write_text(json.dumps({"credit": "", "license": "own"}), encoding="utf-8")
    with Image.open(dst) as im2:
        return {"w": im2.size[0], "h": im2.size[1]}


def fetch_img(file: str, dst: Path, mode: str = "pd") -> dict:
    from PIL import Image
    if file.startswith("NASA:"):
        return fetch_nasa(file[5:], dst)
    if file.startswith("local:"):
        return fetch_local(file[6:], dst)
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


# Luật phối cảnh cho Short MIM/CK (chủ kênh, 12/10/2026): video không được thuần chữ hay thuần ảnh -- chữ động, ảnh/video
# cộng đồng, số liệu (biểu đồ/bộ đếm) và sơ đồ (bảng trắng/thẻ 3D/bản đồ) phải đan nhau. Spec ghi "mix": true để bật.
MODE = {"kinetic": "T", "slam": "T", "question": "T", "quote": "T",
        "photo": "M", "doc": "M", "hero": "M", "evidence": "M", "mug": "M", "split": "M", "file": "M", "crowd": "M",
        "chart": "D", "counter": "D", "ledger": "D", "timeline": "D", "calendar": "D", "clock": "D", "date": "D",
        "map": "G", "board": "G", "cards3d": "G", "source": "G"}


def scene_mode(r: dict) -> str:
    """T = chữ, M = ảnh/video, D = số liệu, G = sơ đồ/3D. Cảnh chữ có clip nền tính là M."""
    m = MODE.get(r["type"], "T")
    return "M" if m == "T" and (r.get("clip") or r.get("vid")) else m


def mix_lint(sc: list[dict]) -> list[str]:
    modes = [scene_mode(r) for r in sc]
    dur = sc[-1]["t1"] - sc[0]["t0"]
    share = {m: sum(r["t1"] - r["t0"] for r, x in zip(sc, modes) if x == m) / dur for m in "TMDG"}
    out = []
    for m, name in (("M", "ảnh/video cộng đồng"), ("D", "số liệu (biểu đồ/bộ đếm/bảng)"), ("G", "sơ đồ (board/cards3d/map)")):
        if share[m] <= 0:
            out.append(f"thiếu cảnh {name}")
    if share["T"] > 0.35:
        out.append(f"cảnh thuần chữ chiếm {share['T']:.0%} thời lượng (> 35%)")
    if max(share.values()) > 0.6:
        out.append(f"một kiểu cảnh chiếm {max(share.values()):.0%} thời lượng (> 60%)")
    for i in range(len(modes) - 2):
        if modes[i] == modes[i + 1] == modes[i + 2]:
            out.append(f"3 cảnh liền cùng kiểu {modes[i]} (cảnh {i}–{i + 2})")
            break
    longest = max(sc, key=lambda r: r["t1"] - r["t0"])
    if longest["t1"] - longest["t0"] > 11:
        out.append(f"cảnh {longest['type']} dài {longest['t1'] - longest['t0']:.1f}s (> 11s): tách ra")
    return out


# ---- BUD v2 (Shorts Studio port, 14/10/2026): luật bố cục/hướng chuyển động (studio.py variety) -- chỉ theme bud ----
# framing = cách chiếm khung; axis = hướng chuyển động chính khi vào. Hai cảnh liền nhau không cùng framing, không cùng axis;
# >= 3 framing khác nhau mỗi video. Spec "v2": true -> lỗi chặn; Short bud cũ -> chỉ cảnh báo.
BUD_FRAME = {"kinetic": ("full-media", "Y"), "slam": ("center-hero", "Z"), "quote": ("card", "in-glyph"),
             "source": ("card-on-field", "X"), "board": ("card", "draw"), "cards3d": ("stack-3d", "3D"),
             "counter": ("center-hero", "count"), "question": ("center-hero", "Y")}


def bud_layout_lint(sc: list[dict]) -> list[str]:
    fr = [BUD_FRAME.get(r["type"], (r["type"], r["type"])) for r in sc if not r.get("loop")]
    fr = [("text-hero", "Y") if r["type"] == "kinetic" and not (r.get("clip") or r.get("vid")) else f
          for r, f in zip([r for r in sc if not r.get("loop")], fr)]
    out = []
    for i in range(1, len(fr)):
        if fr[i][0] == fr[i - 1][0]:
            out.append(f"cảnh {i - 1}-{i} cùng bố cục {fr[i][0]}")
        if fr[i][1] == fr[i - 1][1]:
            out.append(f"cảnh {i - 1}-{i} cùng hướng chuyển động {fr[i][1]}")
    if len({f[0] for f in fr}) < 3:
        out.append(f"chỉ {len({f[0] for f in fr})} kiểu bố cục (< 3)")
    return out


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
        if ty == "quote" and r.get("mode") == "karaoke":   # BUD v2: karaoke theo mốc từng chữ đo từ giọng (studio quote)
            ln = lines[r["line"]]
            r.setdefault("text", ln["text"])
            if r["text"] != ln["text"]:
                raise ValueError(f"quote karaoke: text phải trùng câu {r['line']} (để khớp mốc chữ)")
            r["wt"] = [w["t"] for w in ln["words"]]
            r.setdefault("at", t0)
            r.setdefault("typeDur", 0.0)
        if ty == "source":
            r.setdefault("hlAt", round(t0 + (t1 - t0) * 0.45, 3)); r.setdefault("sealAt", round(t0 + (t1 - t0) * 0.7, 3))
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
    # Khung 0 PHẢI có chữ (12/10/2026, quy tắc Short 1): dòng mở (at < 0,3 s) của cảnh kinetic đầu, kênh MIM/CK, chưa ghi
    # fx -> "hold" (hiện sẵn từ khung 0). Trước đây nó nhận rise/outline/scramble: khung 0 trống, và scramble đặt mốc ÂM
    # (at - 0,35) làm cảnh mở đè lên cảnh sau (ck-nha-dat-kho-ban). Spec "hold_open": false -> giữ cách cũ.
    if spec.get("theme") in ("mim", "ck", "bud"):   # "size" ghi tay vượt khung 980 px -> chữ bị cắt mép (100 ĐỒNG, NOBEL VẬT LÝ)
        from beatfx import text_em
        wide = [f'"{q["text"]}" size {q["size"]} ≈ {q["size"] * text_em(q["text"]):.0f}px'
                for r in sc if r["type"] == "kinetic" for q in r["items"]
                if q.get("size") and q["size"] * text_em(q["text"]) > 980]
        if wide:
            raise SystemExit("chữ kinetic rộng hơn khung (bỏ \"size\" để engine tự co): " + "; ".join(wide))
    # Retro 5 (14/10/2026): (a) dòng phụ của counter/slam là mono một dòng: engine tự co, nhưng dài quá 52 ký tự thì chữ nhỏ hơn
    # 22 px, không đọc được trên điện thoại ("…NEW YORK, 1" bị cắt mất năm); (b) "prefix" có chữ số + số đếm chạy -> khung giữa
    # chừng hiện "1 / 7.698" như một dữ kiện thật.
    long_sub = [f'cảnh {i} ({r["type"]}): "{t}" ({len(t)} ký tự)' for i, r in enumerate(sc)
                for t in [(r.get("sub") or {}).get("text") if r["type"] == "counter" else r.get("sub") if r["type"] == "slam"
                          else r.get("unit") if r["type"] == "chart" else None]   # chart.unit: "…KHÔNG PHẢI DỰ BÁO" từng bị cắt mép phải (14/10)
                if isinstance(t, str) and len(t) > 52]
    if long_sub:
        raise SystemExit("dòng phụ dài quá 52 ký tự (rút gọn hoặc đưa vào mô tả): " + "; ".join(long_sub))
    bad_pre = [f"cảnh {i}: prefix {r['prefix']!r}" for i, r in enumerate(sc)
               if r["type"] == "counter" and any(ch.isdigit() or ch == "<" for ch in str(r.get("prefix") or "")) and r.get("from", 0) != r["to"]]   # "<": "< 9 GIÂY" giữa chừng là sai chiều
    if bad_pre:
        raise SystemExit("counter có chữ số trong prefix: số trung gian sẽ đọc như dữ kiện thật (dùng kinetic/cards3d): " + "; ".join(bad_pre))
    # Cảnh chart cần khối CSS ".ch*" của theme (theme-ck.css, theme-mim.css). Theme chưa có khối ấy -> cột và chữ dồn lên
    # góc trên trái mà không lỗi nào báo (lô Short 3, 12/10/2026: 2 Short MIM đầu tiên dùng chart).
    if any(r["type"] == "chart" for r in sc):
        css = HF / "assets" / "engine" / f"theme-{spec.get('theme')}.css"
        if not (css.exists() and ".chbar" in css.read_text(encoding="utf-8")):
            raise SystemExit(f"cảnh chart: theme {spec.get('theme')!r} chưa có CSS biểu đồ (.chbar) trong {css.name}")
    if spec.get("theme") in ("mim", "ck", "bud") and spec.get("mix"):
        bad = mix_lint(sc)
        if bad:
            raise SystemExit("phối cảnh chưa đạt (luật mix 12/10/2026): " + "; ".join(bad))
    if spec.get("theme") == "bud":
        bad = bud_layout_lint(sc)
        if bad and spec.get("v2"):
            raise SystemExit("bố cục/hướng chuyển động chưa đạt (BUD v2): " + "; ".join(bad))
        for w in bad:
            print(f"  ! WARNING bố cục: {w}", flush=True)
    if spec.get("theme") in ("mim", "ck", "bud") and spec.get("hold_open", True) and sc and sc[0]["type"] == "kinetic":
        for q in sc[0]["items"]:
            if q["at"] < 0.3 and not q.get("fx"):
                q["fx"] = "hold"
    if pools and pools.get("sync"):   # Beat Text MIM: dòng chữ lớn được đọc trọn -> hiện từng chữ theo giọng
        apply_sync(sc, lines)
    if spec.get("mix"):   # dòng sync không phải dòng nhấn: chữ nằm trong "acc" của spec -> hộp màu quét sau chữ (beat.js q.emw; KHÔNG phải q.em của beat2 video dài)
        accs = {norm(a) for a in spec.get("acc", [])}
        for r in sc:
            for q in (r.get("items") or []) if r["type"] == "kinetic" else []:
                if q.get("fx") == "sync" and q.get("wt") and not q.get("acc") and not q.get("c"):
                    em = [k for k, w in enumerate(q["text"].split()) if norm(w) in accs][:2]
                    if em:
                        q["emw"] = em
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
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,600;0,700;0,800;0,900;1,600&family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=JetBrains+Mono:wght@500;700&family=Patrick+Hand&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="assets/engine/casefile.css" />
<link rel="stylesheet" href="assets/engine/beat.css" />
<link rel="stylesheet" href="assets/engine/theme-mim.css" />{css}
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
    if spec.get("rules") == 2 and lines_txt[-1].rstrip().endswith("?"):   # retro 5: luật chỉ nằm trong tài liệu nên đã lọt 1 Short
        raise SystemExit(f"{slug}: Short rules-2 không kết bằng câu hỏi: {lines_txt[-1]!r}")
    th = themes.theme(spec)
    if spec.get("theme") == "bud":   # BUD: luật đa dạng (format/hook/cảnh mở/nhạc/giọng) -- bud_variety.py
        import bud_variety
        spec = bud_variety.apply(slug, spec)
    t = speak(lines_txt, od / "voice.wav", od / "timing.json", voice=spec.get("voice", th["voice"]),
              gap=spec.get("gap", th.get("gap", 0.0)), say=spec.get("say"), tts=spec.get("tts"))
    lines = word_lines(t, od / "voice.wav", spec.get("say"))
    dur = round(t["duration"] + 0.6, 2)                         # 0.6s thở cuối cho vòng lặp
    adir = HF / "assets" / "cases" / slug
    imgs, credits = {}, []
    for key, file in spec.get("imgs", {}).items():
        wh = fetch_img(file, adir / f"{key}.jpg", th.get("img_license", "pd"))
        imgs[key] = {"src": f"assets/cases/{slug}/{key}.jpg", **wh}
        meta = adir / f"{key}.json"
        if meta.exists():
            cr = json.loads(meta.read_text(encoding="utf-8"))["credit"]
            if cr:      # ảnh của chính kênh (local:, vd. logo) không cần ghi công
                credits.append({"kind": "image", "text": cr})
        elif th.get("img_license", "pd") != "pd":
            # ảnh tải trước khi có ghi công: CC BY mà thiếu dòng ghi công là vi phạm giấy phép -> tải lại cho có
            raise SystemExit(f"{slug}: ảnh {key} thiếu {meta.name} (ghi công) -- xoá {key}.jpg rồi dựng lại")
    geo = None
    if spec.get("map"):
        hf_geo.BOX = (70, 330, 1010, 1330)
        mp = spec["map"]
        geo = hf_geo.bake({"countries": mp["countries"], "context": mp.get("context", []), "labels": mp.get("labels", {}),
                           "bbox": mp["bbox"], "pins": mp["pins"]})["_geo"]
    loop_main = None
    if spec.get("theme") == "bud" and spec.get("loop"):   # BUD v2: khung cuối quay về móc (studio loop) -> xem lại liền mạch
        loop_main, dur = dur, round(dur + 0.5, 2)
    scenes = plan(spec, lines, dur)
    if loop_main is not None:
        s0 = scenes[0]
        if s0["type"] != "kinetic" or not s0.get("clip"):
            raise SystemExit(f"{slug}: loop cần cảnh 0 là kinetic có clip")
        scenes[-1]["t1"] = loop_main
        lp = json.loads(json.dumps(s0)); lp.update({"t0": loop_main, "t1": dur, "loop": True, "tr": "cut"})
        for q in lp["items"]:
            q["at"] = round(loop_main + 0.02, 3); q["fx"] = "hold"
        scenes.append(lp)
    if th["sound"] == "music" and not any((themes.MUSIC_DIR / f).exists() for f in themes.tracks(th)):
        raise SystemExit(f"không có file nhạc nền nào trong {themes.MUSIC_DIR} -- kiểm tra trước khi render")
    look_cls, look = "", None
    if spec.get("mix"):   # thư viện look: mỗi Short một cách trình bày, xoay theo sổ (motion/stier/looks.py)
        import looks
        lname, look, lwarn = looks.resolve(spec, slug, spec["theme"].upper(), " ".join(scene_mode(r) for r in scenes))
        look_cls = f" look-{lname}"
        print(f"  look: {lname}", flush=True)
        for w in lwarn:
            print(f"  ! WARNING đa dạng: {w}", flush=True)
        # ảnh tràn khung mà lệch tỉ lệ nhiều -> ảnh in (hiện trọn hình) thay vì cắt mất chủ thể (motion/mediafit.py)
        import mediafit
        for s in scenes:
            if s["type"] == "photo" and s.get("mode", "full") == "full" and s.get("fit") != "cover":
                m = imgs[s["img"]]
                loss = mediafit.crop_loss(m["w"], m["h"], 1080, 1540)
                if loss > mediafit.MAX_LOSS_IMG:
                    s["mode"] = "print"
                    s["tone"] = s.get("tone", "color")
                    if s.get("label"):
                        s["label"].setdefault("y", 1290)
                    print(f"  mediafit: ảnh {s['img']} {m['w']}x{m['h']} tràn khung dọc sẽ cắt mất {loss:.0%} -> chuyển sang ảnh in", flush=True)
    cinfo = {}
    for s in scenes:
        if not s.get("clip"):
            continue
        slot = None
        if look is not None:
            wname = look.get("win", "top") if s.get("win") else None
            slot = {"name": f"win-{wname}", "box": looks.WIN[wname]} if wname else {"name": "full", "box": (0, 0, 1080, 1920)}
        s["ckey"] = s["clip"] + ("|" + slot["name"] if slot else "")
        if s["ckey"] not in cinfo:
            cinfo[s["ckey"]] = clips.ensure(s["clip"], ffmpeg=os.path.join(FF, "ffmpeg"), slot=slot)
            if not any(c["text"] == cinfo[s["ckey"]]["credit"] for c in credits):
                credits.append({"kind": "clip", "text": cinfo[s["ckey"]]["credit"]})
    vtags, scenes = clips.video_tags(scenes, cinfo, dur)
    for cr in sfx.ambience_credits(spec.get("ambience")):   # nen mua/nuoc/chuong CC0
        credits.append({"kind": "sound", "text": cr})
    (od / "credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(slug)) % 100000 + 7
    case = {"slug": slug, "dur": dur, "seed": seed, "accent": spec.get("accent", th["accent"]), "kicker": spec["kicker"],
            "sub": spec.get("sub", ""), "acc": spec.get("acc", []), "lines": lines, "imgs": imgs, "geo": geo, "scenes": scenes,
            "theme": th["js"], **({"mix": True} if spec.get("mix") else {}),
            **({"ambience": spec["ambience"]} if spec.get("ambience") else {})}
    if look is not None:
        case["look"] = look
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
    comp = HF / "compositions" / "cases" / f"{slug}.html"
    comp.parent.mkdir(parents=True, exist_ok=True)
    comp.write_text(HTML.replace("{slug}", slug).replace("{dur}", str(dur)).replace("{title}", spec["title"])
                    .replace("{cls}", th["js"].get("cls", "") + look_cls).replace("{videos}", "\n".join(vtags))
                    # CSS riêng của theme (CK: theme-ck.css); theme không khai báo -> HTML y hệt cũ
                    .replace("{css}", f'\n<link rel="stylesheet" href="assets/engine/{th["js"]["css"]}" />' if th["js"].get("css") else ""),
                    encoding="utf-8")
    sfx.build(case, od / "sfx.wav", drone=th["sound"] == "drone")
    if spec.get("theme") == "bud" and spec.get("v2"):
        check_gate(slug, comp, scenes, od, strict=True)
    if not render:
        return comp
    silent = od / ("draft.mp4" if draft else "silent.mp4")
    cmd = ["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
           f"compositions/cases/{slug}.html", "-o", str(silent), "--fps", "30", "--quiet"]
    cmd += ["-q", "draft"] if draft else ["--crf", "19"]
    with render_lock(f"short {slug}"):   # một render một lúc trên cả máy (retro mục 9)
        r = run(cmd, cwd=HF)
    if r.returncode != 0 or not silent.exists():
        raise SystemExit(f"{slug}: render hỏng\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    final = od / ("draft_av.mp4" if draft else "final.mp4")
    fc = ("[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad,asplit=2[v][vk];[2:a]volume=0.5[s0];"
          "[s0][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[s];"
          "[v][s]amix=inputs=2:weights='1 1':normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    music = []
    if th["sound"] == "music":
        # spec ghi "music" (BUD: bud_variety chọn) -> dùng đúng bài đó; không ghi -> như cũ (lâu chưa dùng nhất)
        track = (spec["music"] if spec.get("music") in themes.tracks(th) and (themes.MUSIC_DIR / spec["music"]).exists()
                 else themes.pick_track(slug, [f for f in themes.tracks(th) if (themes.MUSIC_DIR / f).exists()],
                                        th.get("ledger", themes.MUSIC_LEDGER)))
        quiet = [(s["t0"], s["t1"]) for s in scenes if s["type"] == "question"]
        # spec "music_gain" / "music_duck": nhạc nền nghe được hơn cho Short kiểu mới (12/10/2026: đo -40 LUFS sau khi nén,
        # thấp hơn giọng 20 dB -> gần như không nghe thấy trên loa điện thoại). Không ghi -> mặc định theme như cũ.
        fc = themes.music_filter(spec.get("music_gain", th["music_gain"]), quiet, spec.get("music_duck", 6), spec.get("sfx_gain", 0.5))
        moff = themes.track_offset(slug, track, t["duration"] + 2) if spec.get("mix") else 0
        music = (["-ss", str(moff)] if moff else []) + ["-i", str(themes.MUSIC_DIR / track)]
        (od / "music.json").write_text(json.dumps({"file": track, "credit": themes.music_credit(track), **({"offset": moff} if moff else {})},
                                                  ensure_ascii=False), encoding="utf-8")
    r = run([FF + r"\ffmpeg.exe", "-v", "error", "-y", "-i", str(silent), "-i", str(od / "voice.wav"), "-i", str(od / "sfx.wav"),
             *music, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
             "-shortest", "-movflags", "+faststart", str(final)])
    if r.returncode != 0:
        raise SystemExit(f"{slug}: mux hỏng {r.stderr[-2000:]}")
    for m in qa_short(final):
        print(f"  {m}", flush=True)
    return final


def check_gate(slug: str, comp: Path, scenes: list[dict], od: Path, strict: bool = True) -> dict:
    """BUD v2 (Shorts Studio port): `hyperframes check` (runtime JS / layout / contrast WCAG AA) ở giữa mỗi cảnh, TRƯỚC render.
    check chỉ nhận thư mục dự án -> dựng thư mục tạm od/check (index.html + junction assets -> motion/hf/assets)."""
    cd = od / "check"
    cd.mkdir(parents=True, exist_ok=True)
    html = comp.read_text(encoding="utf-8")
    # khai báo __timelines nội tuyến (StaticGuard chỉ quét HTML) + cờ __HF_CHECK (engine thay <video> bằng khung giữ chỗ)
    (cd / "index.html").write_text(html.replace("</head>", "<script>window.__HF_CHECK = 1; window.__timelines = window.__timelines || {};</script>\n</head>", 1), encoding="utf-8")
    shutil.copy(HF / "hyperframes.json", cd / "hyperframes.json")
    # trình kiểm chạy script ngoài trước khi có DOM -> nhúng nội tuyến engine (chỉ trong bản sao kiểm)
    for nm in re.findall(r'<script src="assets/engine/([^"]+\.js)"></script>', html):
        js = (HF / "assets/engine" / nm).read_text(encoding="utf-8")
        html = html.replace(f'<script src="assets/engine/{nm}"></script>', "<script>\n" + js + "\n</script>")
    (cd / "index.html").write_text(html.replace("</head>", "<script>window.__HF_CHECK = 1; window.__timelines = window.__timelines || {};</script>\n</head>", 1), encoding="utf-8")
    for rel in ["assets/engine", f"assets/cases/{slug}"]:   # check không theo junction -> chép thật (nhỏ)
        shutil.rmtree(cd / rel, ignore_errors=True); shutil.copytree(HF / rel, cd / rel)
    with open(cd / f"assets/cases/{slug}/data.js", "a", encoding="utf-8") as f:   # cờ đặt trong data.js (script nội tuyến bị trình kiểm sắp lại)
        f.write("\nwindow.__HF_CHECK = 1;\n")
    for m in set(re.findall(r'src="(assets/clips/[^"]+)"', html)):   # clip: hard link (cùng ổ, không tốn chỗ)
        dst = cd / m; dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            try:
                os.link(HF / m, dst)
            except OSError:
                shutil.copy(HF / m, dst)
    mids = ",".join(f"{(s['t0'] + s['t1']) / 2:.2f}" for s in scenes)
    r = subprocess.run(["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "check", ".", "--json", "--at", mids],
                       cwd=cd, timeout=900, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        cj = json.loads(r.stdout[r.stdout.find("{"):])
    except Exception:      # noqa: BLE001
        raise SystemExit(f"{slug}: check không đọc được JSON\n{(r.stdout + r.stderr)[-1500:]}")
    (od / "check.json").write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    def errs(k):
        sec = cj.get(k) or {}
        return [f for f in sec.get("findings", []) if f.get("severity") == "error"]
    rep = {k: errs(k) for k in ("lint", "runtime", "layout", "contrast")}
    # dòng chữ xếp tầng trong cùng cảnh kinetic: .rw chừa .3em trên cho dấu chồng (margin âm) -> hộp chồng nhau có chủ đích, không phải lỗi đọc
    def _sc(sel):
        m = re.match(r"#stage > div:nth-of-type\((\d+)\)", sel or "")
        return int(m.group(1)) - 1 if m else None
    keep = []
    for f in rep["layout"]:
        a, c = _sc(f.get("selector")), _sc(f.get("containerSelector"))
        if f.get("code") == "content_overlap" and a is not None and a == c and a < len(scenes) and scenes[a]["type"] == "kinetic":
            print(f"  check: bỏ qua chồng dòng kinetic (cảnh {a}, {f.get('text')!r})", flush=True); continue
        keep.append(f)
    rep["layout"] = keep
    if not (cj.get("layout") or {}).get("duration"):
        rep["runtime"].append({"code": "no_timeline", "message": "trình kiểm không đọc được timeline (duration 0)"})
    print(f"  check: lint {len(rep['lint'])} · runtime {len(rep['runtime'])} · layout {len(rep['layout'])} · contrast {len(rep['contrast'])} lỗi (ok={cj.get('ok')})", flush=True)
    bad = [f"{k}: {f.get('code') or f.get('rule')} {str(f.get('message') or f.get('selector') or '')[:120]}" for k, v in rep.items() for f in v]
    if bad and strict:
        raise SystemExit(f"{slug}: check chưa đạt -> " + " | ".join(bad[:8]))
    return rep


def qa_short(final: Path, ffmpeg: str | None = None) -> list[str]:
    """QA tự động sau MỖI Short (retro 2 mục 12: trước đây PM soát tay): scripts/qa_blank.py trên bản dựng + contact sheet
    `<final>_sheet.jpg` cạnh file (20 khung, mỗi 2 giây). KHÔNG chặn — trả về các dòng để in; lỗi công cụ cũng chỉ là cảnh báo."""
    ff = ffmpeg or os.path.join(FF, "ffmpeg")
    out = []
    try:
        if str(ROOT / "scripts") not in sys.path:
            sys.path.insert(0, str(ROOT / "scripts"))
        import qa_blank
        runs = qa_blank.scan(final, 1.0, 4.0, ffmpeg=ff)
        out.append(f"QA {final.name}: {len(runs)} đoạn trống ≥ 1.0s" + ("" if not runs else " — WARNING, xem lại neo chữ:"))
        out += [f"  ! {qa_blank.fmt(s, e)}" for s, e in runs]
    except Exception as e:      # noqa: BLE001 — QA không được làm hỏng bản dựng
        out.append(f"! WARNING qa_blank không chạy được: {e}")
    sheet = final.with_name(final.stem + "_sheet.jpg")
    try:
        r = subprocess.run([ff, "-v", "error", "-y", "-i", str(final), "-vf", "fps=1/2,scale=216:-1,tile=10x2:padding=4",
                            "-frames:v", "1", str(sheet)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        out.append(f"contact sheet: {sheet}" if r.returncode == 0 and sheet.exists() else f"! WARNING contact sheet hỏng: {r.stderr[-300:]}")
    except OSError as e:
        out.append(f"! WARNING contact sheet không chạy được: {e}")
    return out


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for s in args:
        t0 = time.time()
        p = build(s, render="--no-render" not in sys.argv, draft="--draft" in sys.argv)
        print(f"{s}: {p}  ({time.time() - t0:.0f}s)", flush=True)
