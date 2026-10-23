"""Âm thanh cho hồ sơ S-tier — tổng hợp thủ tục (numpy), bám CÙNG mốc với hình.

Mỗi loại cảnh trong casefile.js ghi chú tiếng động + độ lệch; ở đây đặt đúng
các độ lệch đó. Ngữ pháp: nền trầm liên tục dày dần, tiếng "đập" chỉ ở
khoảnh khắc lật, cảnh `question` thì LẶNG hẳn.
"""
from __future__ import annotations

import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
FADE_CUT = int(0.005 * SR)   # 23/10/2026: 5 ms fade khi Mix.put cắt tiếng ở mép (chống tiếng tách)


def soft_clip(x: np.ndarray, knee: float = 0.8, ceil: float = 1.0) -> np.ndarray:
    """23/10/2026: thay np.clip cứng (cú boom/rumble chồng nhau -> vài chục mẫu vuông đầu = tiếng rè).
    Dưới `knee` giữ NGUYÊN (mức cũ không đổi); trên knee nén mềm bằng tanh, không bao giờ vượt `ceil`."""
    a = np.abs(x)
    over = a > knee
    if not over.any():
        return x
    y = x.copy()
    y[over] = np.sign(x[over]) * (knee + (ceil - knee) * np.tanh((a[over] - knee) / (ceil - knee)))
    return y

# ---- nen moi truong that (CC0): mua / nuoc / chuong -- motion/stier/ambience/LICENSES.json ----
AMB_DIR = Path(__file__).resolve().parent / "ambience"


def _read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        if w.getframerate() != SR or w.getsampwidth() != 2:
            raise SystemExit(f"{p.name}: can 48 kHz / 16-bit")
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
        return x.reshape(-1, 2) if w.getnchannels() == 2 else np.repeat(x[:, None], 2, 1)


def _loop(x: np.ndarray, n: int, xf: int) -> np.ndarray:
    """Lap ban ghi cho du n mau, noi vong bang crossfade dang-cong-suat (khong nghe 'cu' noi)."""
    xf = max(1, min(xf, len(x) // 3))
    f = np.sin(np.linspace(0, np.pi / 2, xf))[:, None]
    out = x[: min(n, len(x))].copy()
    while len(out) < n:
        out[-xf:] = out[-xf:] * f[::-1] + x[:xf] * f
        out = np.concatenate([out, x[xf:]])
    return out[:n]


def ambience(amb, N: int):
    """spec "ambience": "rain" | {"bed": "rain"|"water", "gain": 1.0,
    "hits": [{"at": giay, "kind": "bell"|"gong", "gain": 1.0}]}.
    Tra lop (N,2) o MUC TUYET DOI (khong bi chuan hoa dinh cung sfx), hoac None."""
    if not amb:
        return None
    if isinstance(amb, str):
        amb = {"bed": amb}
    out = np.zeros((N, 2))
    if amb.get("bed"):
        b = _loop(_read_wav(AMB_DIR / f"{amb['bed']}.wav"), N, int(1.5 * SR))
        i = np.arange(N)
        env = np.minimum(1, i / (0.8 * SR)) * np.minimum(1, (N - i) / (1.2 * SR))
        out += b * env[:, None] * float(amb.get("gain", 1.0))
    for h in amb.get("hits") or []:
        x = _read_wav(AMB_DIR / f"{h.get('kind', 'bell')}.wav") * float(h.get("gain", 1.0))
        i = int(h["at"] * SR)
        if 0 <= i < N:
            x = x[: N - i]
            out[i:i + len(x)] += x
    return out


def ambience_credits(amb) -> list[str]:
    """Dong ghi cong cho credits.json (CC0: khong bat buoc, van ghi)."""
    if not amb:
        return []
    import json
    lic = json.loads((AMB_DIR / "LICENSES.json").read_text(encoding="utf-8"))
    amb = {"bed": amb} if isinstance(amb, str) else amb
    names = ([amb["bed"]] if amb.get("bed") else []) + [h.get("kind", "bell") for h in amb.get("hits") or []]
    seen, res = set(), []
    for k in names:
        if k in seen:
            continue
        seen.add(k)
        m = lic[f"{k}.wav"]
        res.append(f"Sound: {m['title'].split(' (')[0]} - {m['author'].split(' (')[0]}, {m['license']} ({m['source']})")
    return res


class Mix:
    def __init__(self, dur: float, seed: int):
        self.dur = dur
        self.N = int(dur * SR)
        self.bed = np.zeros((self.N, 2))
        self.rng = np.random.default_rng(seed)

    # ---- nguyên liệu ----
    def env(self, n, a=0.002, r=0.2):
        t = np.arange(n) / SR
        return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)

    @staticmethod
    def lp(x, k):
        # lọc một cực, vector hoá bằng lfilter-thủ công qua cumsum xấp xỉ: dùng vòng lặp numpy nhanh vừa đủ
        y = np.empty_like(x)
        acc = 0.0
        for i in range(len(x)):
            acc += k * (x[i] - acc)
            y[i] = acc
        return y

    def put(self, t, sig, gain=1.0, pan=0.0):
        i = int(t * SR)
        if i >= self.N or i + len(sig) <= 0:
            return
        # 23/10/2026: tiếng bị cắt đầu/đuôi (vd. whoosh thẻ chương đặt ở T0-0.35 với T0=0) bắt đầu giữa đường bao
        # -> bước nhảy = tiếng "tách" ở đầu mỗi chương (CL lẫn MIM). Fade 5 ms ở chỗ cắt.
        fi = fo = 0
        if i < 0:
            sig, i, fi = sig[-i:], 0, FADE_CUT
        if len(sig) > self.N - i:
            fo = FADE_CUT
        sig = sig[: self.N - i] * gain
        if fi or fo:     # sig đã là mảng mới (phép nhân gain) -> sửa tại chỗ không đụng tín hiệu gốc
            k = min(FADE_CUT, len(sig))
            if fi:
                sig[:k] *= np.linspace(0, 1, k)
            if fo:
                sig[-k:] *= np.linspace(1, 0, k)
        self.bed[i:i + len(sig), 0] += sig * (1 - max(0, pan))
        self.bed[i:i + len(sig), 1] += sig * (1 + min(0, pan))

    def boom(self, dur=1.6, f0=58, f1=34):
        n = int(dur * SR); t = np.arange(n) / SR
        f = f1 + (f0 - f1) * np.exp(-t * 6)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * self.env(n, 0.003, 0.45)
        click = self.lp(self.rng.standard_normal(n), 0.25) * self.env(n, 0.001, 0.018)
        return s + 0.6 * click

    def thud(self, dur=0.5):
        n = int(dur * SR)
        return self.lp(self.rng.standard_normal(n), 0.04) * self.env(n, 0.001, 0.07) * 4 + self.boom(dur, 90, 50) * 0.5

    def whoosh(self, dur=0.6, rise=True):
        n = int(dur * SR); t = np.linspace(0, 1, n)
        u = t if rise else 1 - t
        shape = np.sin(np.pi * u ** 0.8) ** 2
        k = 0.02 + 0.2 * u
        x = self.rng.standard_normal(n); y = np.empty(n); acc = 0.0
        for i in range(n):
            acc += k[i] * (x[i] - acc); y[i] = acc
        return y * shape * 2.2

    def tick(self, f=3200, dur=0.03):
        n = int(dur * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * f * t) * 0.5 + self.rng.standard_normal(n) * 0.5) * self.env(n, 0.0005, 0.006)

    def key(self):
        n = int(0.05 * SR)
        return self.tick(1800, 0.05) * 1.3 + self.lp(self.rng.standard_normal(n), 0.3) * self.env(n, 0.0005, 0.01)

    def scratch(self, dur=0.28):
        n = int(dur * SR); t = np.arange(n) / SR
        x = self.rng.standard_normal(n) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t))
        return (x - self.lp(x, 0.15)) * np.sin(np.pi * t / dur) * 0.35

    def shutter(self):
        return self.tick(5200, 0.06) * 3

    def clank(self):
        n = int(1.2 * SR); t = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((213, 1), (587, .6), (1142, .45), (1893, .3)))
        return s * self.env(n, 0.001, 0.18) * 0.35

    def blip(self):
        return self.tick(1500, 0.08) * 2

    def tone(self, dur, f0=220, f1=440):
        n = int(dur * SR); tr = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * tr / dur) / SR) * np.sin(np.pi * tr / dur) * 0.18

    def murmur(self, dur):
        n = int(dur * SR); x = self.rng.standard_normal(n); i = np.arange(n)
        m = (self.lp(x, 0.08) - self.lp(x, 0.012)) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * i / SR) ** 2)
        return m * np.minimum(1, i / (0.4 * SR)) * np.minimum(1, (n - i) / (0.3 * SR))

    def pad(self, freqs, dur, a=0.25, r=1.2):
        n = int(dur * SR); t = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate(freqs)) / len(freqs)
        return s * np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t)) / r)

    def write(self, dst: Path, extra=None):
        peak = np.max(np.abs(self.bed)) or 1.0
        mix = self.bed / peak * 0.9
        if extra is not None:   # nen moi truong: cong SAU chuan hoa -> muc on dinh giua cac video
            mix = soft_clip(mix + extra, 0.9, 0.99)   # 23/10/2026: thay np.clip (≤ 0,9 vẫn y như cũ)
        k = min(FADE_CUT, len(mix) // 2)   # 23/10/2026: nền trầm/tiếng chạm mép file bị cắt cụt (đuôi −24 dBFS) -> fade 5 ms hai đầu
        if k:
            mix = mix.copy()
            mix[:k] *= np.linspace(0, 1, k)[:, None]
            mix[-k:] *= np.linspace(1, 0, k)[:, None]
        out = (mix * 32767).astype("<i2")
        with wave.open(str(dst), "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from beatfx import beat_sfx  # noqa: E402


def build(case: dict, dst: Path, drone: bool = True) -> None:
    """drone=False: kênh có nhạc nền thật (MIM, motion/stier/themes.py) -- bỏ nền trầm,
    chỉ giữ tiếng động theo cảnh/chữ; nhạc trộn riêng ở build.py."""
    dur = case["dur"]
    M = Mix(dur, case.get("seed", 1911))
    scenes = case["scenes"]
    t = np.arange(M.N) / SR

    # nền trầm: dày dần về cao trào, LẶNG ở cảnh question
    bed = (np.sin(2 * np.pi * 43.65 * t) * 0.55 + np.sin(2 * np.pi * 65.4 * t + 1) * 0.25
             + np.sin(2 * np.pi * 87.3 * t * (1 + 0.002 * np.sin(2 * np.pi * 0.1 * t))) * 0.12)
    air = M.lp(M.rng.standard_normal(M.N), 0.01) * 0.9
    g = np.clip(t / 1.5, 0, 1) * (0.7 + 0.3 * np.clip((t - dur * 0.55) / 4, 0, 1))
    for s in scenes:
        if s["type"] == "question":
            q0, q1 = s["t0"] - 0.12, s["t1"]
            g = np.where((t > q0) & (t < q1), 0, g)
            g = np.where((t >= q0 - 0.3) & (t <= q0), g * np.clip((q0 - t) / 0.3, 0, 1), g)
            g = np.where((t >= q1) & (t <= q1 + 0.8), g * np.clip((t - q1) / 0.8, 0, 1), g)
    if drone:
        M.bed[:, 0] += (bed + air) * g * 0.22
        M.bed[:, 1] += (bed * 0.97 + air) * g * 0.22

    for i, s in enumerate(scenes):
        T0, T1, ty = s["t0"], s["t1"], s["type"]
        if i > 0 and ty != "question":
            M.put(T0 - 0.3, M.whoosh(0.45), 0.3, 0.3 if i % 2 else -0.3)
        if ty == "hero":
            if s.get("strike") is not None:
                M.put(s["strike"] - 0.02, M.scratch(0.34), 1.0, -0.2)
            if s.get("tape"):
                M.put(s["tape"]["at"] - 0.05, M.thud(0.4), 0.35)
            if s.get("shatter"):
                tb = s["shatter"]["at"]
                M.put(tb - 0.62, M.whoosh(0.7), 0.55)
                M.put(tb + 0.05, M.boom(2.0), 1.0)
            if s.get("intro"):
                M.put(T0, M.boom(1.2, 50, 34), 0.35)
            if s.get("loop"):
                M.put(T0 - 0.02, M.boom(1.6, 48, 36), 0.5)
                M.put(T0, M.pad([130.8, 164.8, 196.0, 261.6], dur - T0 + 0.1), 0.35)
        elif ty == "date":
            for k in range(len(s.get("day") or "")):
                M.put(s["dayAt"] + k * 0.045, M.key(), 0.5, (k - 3) * 0.05)
            groups = [g2 for g2 in "".join(c if c.isdigit() else " " for c in s["date"]).split()]
            for gi, grp in enumerate(groups):
                for j in range(len(grp)):
                    for m in range(8):
                        M.put(s["groupAt"][gi] - 0.05 + j * 0.07 + 0.55 * (1 - (1 - m / 8) ** 2.2), M.tick(2600 + 200 * j), 0.28, 0.1 * (j - 1))
            if s.get("stamp"):
                M.put(s["stamp"]["at"] + 0.16, M.thud(0.6), 1.0)
                M.put(s["stamp"]["at"] + 0.16, M.boom(1.2, 70, 40), 0.5)
        elif ty == "doc":
            M.put(T0, M.shutter(), 0.5)
            for q in (s.get("moves") or [])[1:]:
                M.put(q["at"] - 0.35, M.whoosh(0.8), 0.28, -0.3)
            tg = s.get("tag") or {}
            if tg.get("reveal") is not None:
                M.put(tg["reveal"], M.scratch(0.3), 0.8)
        elif ty == "photo":
            M.put(T0, M.shutter(), 0.5)
            M.put(T0 + 0.02, M.boom(1.4, 50, 32), 0.5)
            for c in s.get("circles") or []:
                M.put(c["at"], M.scratch(0.22), 0.5)
            if s.get("stamp"):
                M.put(s["stamp"]["at"] + 0.16, M.thud(0.6), 1.0)
        elif ty == "counter":
            steps = int(min(28, max(6, abs(s["to"] - s.get("from", 0))))) if abs(s["to"] - s.get("from", 0)) < 28 else 28
            span = s["until"] - s["at"]
            for m in range(steps):
                M.put(s["at"] + span * (1 - (1 - (m + 1) / steps) ** 0.5), M.tick(2200 + m * 30, 0.03), 0.35)
            M.put(s["until"], M.thud(0.6), 0.8)
        elif ty == "calendar":
            for k in range(min(s["n"], s.get("cross", s["n"]))):
                M.put(s["at"] + k * s["step"], M.scratch(0.12), 0.8, ((k % 7) - 3) * 0.1)
                M.put(s["at"] + k * s["step"] + 0.06, M.scratch(0.12), 0.8, ((k % 7) - 3) * 0.1)
        elif ty == "clock":
            tt, k = T0, 0
            while tt < T1:
                M.put(tt, M.tick(4200 if k % 2 else 3000, 0.025), 0.45, 0.15 if k % 2 else -0.15)
                tt += 0.075 + 0.06 * abs(np.sin(k * 0.4)); k += 1
            if s.get("plus"):
                M.put(s["plusAt"] - 0.1, M.thud(0.35), 0.55)
        elif ty == "file":
            M.put(T0 - 0.1, M.whoosh(0.5), 0.35, -0.2)
            if s.get("stamp"):
                M.put(s["stamp"]["at"] + 0.16, M.thud(0.6), 0.9)
        elif ty == "crowd":
            M.put(T0 - 0.1, M.murmur(T1 - T0 + 0.4), 1.3)
        elif ty in ("map", "mug"):
            if ty == "map":
                for r in s.get("routes") or []:
                    M.put(r["at"], M.tone(max(0.3, r["until"] - r["at"])), 1.0)
                for p in s.get("pins") or []:
                    M.put(p["at"] + 0.25, M.blip(), 0.6, 0.3)
            if s.get("mug"):
                M.put(s["mug"]["at"] - 0.55, M.whoosh(0.35), 0.5)
                M.put(s["mug"]["at"] - 0.13, M.thud(0.5), 0.8)
            if s.get("stamp"):
                M.put(s["stamp"]["at"] + 0.16, M.boom(2.2, 62, 30), 1.1)
            if s.get("bars"):
                for k in range(8):
                    M.put(s["bars"]["at"] + 0.35 + k * 0.035, M.clank(), 0.45, (k - 3.5) * 0.12)
            if s.get("big"):
                M.put(s["big"]["at"] - 0.1, M.thud(0.4), 0.4)
        elif ty == "quote":
            L = len(s["text"])
            n = min(40, L)
            for k in range(n):
                M.put(s["at"] + (k / n) * s["typeDur"], M.key(), 0.4, ((k % 5) - 2) * 0.08)
        elif ty == "kinetic":
            for q in s["items"]:
                beat_sfx(M, q, 1.15)
        elif ty == "evidence":
            M.put(T0, M.shutter(), 0.5)
            for c in s.get("callouts") or []:
                M.put(c["at"], M.tick(3000, 0.04), 0.6)
        elif ty == "split":
            M.put(s["a"]["at"], M.thud(0.4), 0.6, -0.3)
            M.put(s["b"]["at"], M.thud(0.4), 0.6, 0.3)
            if s.get("sign"):
                M.put(s["signAt"] + 0.05, M.boom(1.4, 60, 36), 0.8)
        elif ty == "timeline":
            for q in s["items"]:
                M.put(q["at"], M.tick(2400, 0.04), 0.6)
                M.put(q["at"], M.thud(0.3), 0.3)
        elif ty == "ledger":
            for r in s.get("rows") or []:
                for k in range(3):
                    M.put(r["at"] + k * 0.05, M.key(), 0.4)
            if s.get("total"):
                M.put(s["total"]["at"], M.thud(0.6), 0.9)
        elif ty == "chart":      # kênh CK: cột mọc / đường vẽ dần (casefile.js B.chart)
            for b in s.get("bars") or []:
                M.put(b["at"] - 0.1, M.whoosh(0.35), 0.18)
                M.put(b["at"] + 0.3, M.thud(0.35), 0.35)
                if b.get("gapAt") is not None:
                    M.put(b["gapAt"], M.scratch(0.3), 0.5)
            for k, p in enumerate(s.get("points") or []):
                M.put(p["at"], M.blip(), 0.35 if k else 0.2, 0.2)
            if s.get("badge"):
                M.put(s["badge"]["at"] - 0.1, M.thud(0.5), 0.7)
        elif ty == "board":      # bảng trắng: tiếng bút theo từng ô, vút theo mũi tên (casefile.js B.board)
            for q in s.get("nodes") or []:
                M.put(q["at"] - 0.1, M.scratch(0.3), 0.4)
                if q.get("cross") is not None:
                    M.put(q["cross"], M.scratch(0.3), 0.6)
            for a in s.get("arrows") or []:
                M.put(a["at"] - 0.05, M.whoosh(0.3), 0.2)
        elif ty == "table":      # bảng tra: hàng trượt vào (gõ phím nhẹ), ô sáng lên (thud + blip) -- casefile.js B.table
            for i, r in enumerate(s["rows"]):
                at = r.get("at", T0 + 0.25 + i * 0.08)
                for k in range(2):
                    M.put(at + k * 0.05, M.key(), 0.3)
            for h in s.get("hl") or []:
                M.put(h["at"], M.thud(0.4), 0.55)
                M.put(h["at"] + 0.02, M.blip(), 0.35)
        elif ty == "cards3d":    # thẻ 3D lật lên
            for c in s["cards"]:
                M.put(c["at"] - 0.15, M.whoosh(0.35), 0.22)
                M.put(c["at"] + 0.25, M.thud(0.4), 0.5)
        elif ty == "slam":
            fx = s.get("fx", "punch")
            if fx in ("slice", "zoom"):
                M.put(s["at"] - 0.35, M.whoosh(0.4), 0.5)
            elif fx == "glitch":
                M.put(s["at"] - 0.05, M.scratch(0.35), 0.6)
            M.put(s["at"] + 0.05, M.boom(1.8 if fx != "outline" else 1.4), 1.0)
    M.write(dst, extra=ambience(case.get("ambience"), M.N))
