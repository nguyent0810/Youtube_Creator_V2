"""Tiếng động cho video dài 16:9 — tổng hợp thủ tục, bám CÙNG mốc với casewide.js.

Khác Short: không có nền trầm tự tổng hợp (nhạc nền thật lo không khí, mix trong build_long.mix_chapter);
ở đây chỉ còn các "điểm chạm" — màn trập khi ảnh hiện, thud khi chữ đập, tick khi dòng hồ sơ hiện,
boom ở thẻ chương và cú slam. Tiết chế: video 30+ phút mà cảnh nào cũng đập thì tai mỏi -> gain thấp hơn Short.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "stier"))
from sfx import Mix, SR  # noqa: E402
from scipy.signal import butter, sosfilt  # noqa: E402


class NoirMix(Mix):
    """Thêm tiếng cho theme noir (Mafia Ý): diêm, lửa, chuông nhà thờ, búa toà, nhịp tim, tĩnh điện radio, máy chiếu phim…
    Lọc bằng scipy (nhanh) thay cho lp() vòng lặp của Mix khi tín hiệu dài."""

    def bp(self, x, lo, hi):
        return sosfilt(butter(2, [lo, hi], btype="bandpass", fs=SR, output="sos"), x)

    def lowp(self, x, f):
        return sosfilt(butter(2, f, btype="lowpass", fs=SR, output="sos"), x)

    def fade(self, x, a=0.05, r=0.3):
        n = len(x); i = np.arange(n)
        return x * np.minimum(1, i / max(1, a * SR)) * np.minimum(1, (n - i) / max(1, r * SR))

    def match(self):
        n = int(0.9 * SR); t = np.arange(n) / SR
        rasp = self.bp(self.rng.standard_normal(n), 1800, 7000) * np.exp(-t / 0.035) * 2.2
        flare = self.bp(self.rng.standard_normal(n), 300, 3000) * np.minimum(1, t / 0.06) * np.exp(-t / 0.35) * 1.2
        return rasp + flare

    def fire(self, dur):
        n = int(dur * SR); t = np.arange(n) / SR
        roar = self.lowp(self.rng.standard_normal(n), 500) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * t) ** 2) * 1.6
        crack = np.zeros(n)
        for _ in range(int(dur * 22)):
            i = int(self.rng.uniform(0, n - 2000)); m = int(self.rng.uniform(200, 1500))
            crack[i:i + m] += self.rng.standard_normal(m) * np.exp(-np.arange(m) / (m / 5)) * self.rng.uniform(0.3, 1.2)
        return self.fade(roar + self.bp(crack, 1200, 9000) * 1.4, 0.5, 0.8)

    def bell(self, f0=196, dur=6.0):
        n = int(dur * SR); t = np.arange(n) / SR
        parts = ((0.5, 1.0, 3.2), (1.0, 0.8, 2.4), (1.183, 0.5, 1.8), (1.506, 0.45, 1.5), (2.0, 0.35, 1.2), (2.514, 0.25, 0.9), (3.011, 0.18, 0.7))
        s = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / d) for r, a, d in parts)
        return (s + self.bp(self.rng.standard_normal(n), 2000, 6000) * np.exp(-t / 0.01) * 0.8) * 0.35

    def gavel(self):
        def knock():
            n = int(0.25 * SR); t = np.arange(n) / SR
            return (np.sin(2 * np.pi * 420 * t) + 0.6 * np.sin(2 * np.pi * 1150 * t)) * np.exp(-t / 0.04) + self.rng.standard_normal(n) * np.exp(-t / 0.004)
        a = knock(); out = np.zeros(int(0.5 * SR)); out[:len(a)] += a; k = int(0.19 * SR); out[k:k + len(a)] += knock() * 0.8
        return out * 0.8

    def slap(self):
        n = int(0.3 * SR); t = np.arange(n) / SR
        return self.bp(self.rng.standard_normal(n), 400, 8000) * np.exp(-t / 0.018) * 2.5 + self.boom(0.3, 110, 60) * 0.5

    def heart(self):
        n = int(0.6 * SR); t = np.arange(n) / SR

        def lub(f, d):
            return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.006) * np.exp(-t / d)
        out = lub(58, 0.06); k = int(0.26 * SR); out[k:] += lub(48, 0.05)[: n - k] * 0.75
        return out * 1.4

    def paper(self, dur=0.45):
        n = int(dur * SR); t = np.arange(n) / SR
        am = np.abs(self.lowp(self.rng.standard_normal(n), 30)) * 4
        return self.bp(self.rng.standard_normal(n), 1500, 9000) * am * np.sin(np.pi * t / dur) * 0.9

    def static(self, dur):
        n = int(dur * SR)
        hiss = self.bp(self.rng.standard_normal(n), 900, 4200) * 0.5
        for _ in range(int(dur * 9)):
            i = int(self.rng.uniform(0, n - 400)); hiss[i:i + 300] += self.rng.standard_normal(300) * self.rng.uniform(0.5, 1.6)
        return self.fade(hiss, 0.15, 0.3)

    def projector(self, dur):
        n = int(dur * SR); t = np.arange(n) / SR
        out = self.lowp(self.rng.standard_normal(n), 300) * 0.25 + np.sin(2 * np.pi * 48 * t) * 0.05
        c = self.tick(1100, 0.012) * 0.8
        for k in range(int(dur * 24)):
            i = int(k * SR / 24)
            m = min(len(c), n - i)
            if m > 0:
                out[i:i + m] += c[:m]
        return self.fade(out, 0.3, 0.4)

    def needle(self, dur):
        n = int(dur * SR); t = np.arange(n) / SR
        return self.fade(self.bp(self.rng.standard_normal(n), 2500, 9000) * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t) ** 2) * 0.35, 0.3, 0.5)

    def rumble(self, dur):
        n = int(dur * SR); t = np.arange(n) / SR
        return self.lowp(self.rng.standard_normal(n), 90) * np.minimum(1, t / 0.02) * np.exp(-t / (dur / 3)) * 4

    CUES = ("match", "bell", "gavel", "slap", "heart", "paper", "boom", "thud", "whoosh", "shutter", "clank")


def build(case: dict, dst: Path) -> None:
    dur = case["dur"]
    M = NoirMix(dur, case.get("seed", 1995))
    for i, s in enumerate(case["scenes"]):
        T0, T1, ty = s["t0"], s["t1"], s["type"]
        if i > 0 and ty not in ("question", "broll", "chapter"):
            M.put(T0 - 0.3, M.whoosh(0.45), 0.16, 0.3 if i % 2 else -0.3)
        for q in s.get("kin") or []:
            M.put(q["at"] - 0.02, M.thud(0.35), 0.3)
        if isinstance(s.get("label"), dict):
            M.put(s["label"]["at"], M.tick(2600, 0.04), 0.35)
        if s.get("stamp"):
            M.put(s["stamp"]["at"] + 0.16, M.thud(0.6), 0.8)
            M.put(s["stamp"]["at"] + 0.16, M.boom(1.2, 70, 40), 0.4)
        if ty == "chapter":
            M.put(T0 - 0.35, M.whoosh(0.8), 0.45)
            M.put(T0 + 0.05, M.boom(2.4, 52, 30), 0.9)
            M.put(s.get("titleAt", T0 + 0.35) - 0.02, M.thud(0.5), 0.5)
        elif ty in ("photo", "evidence"):
            M.put(T0, M.shutter(), 0.35)
            M.put(T0 + 0.02, M.boom(1.2, 50, 32), 0.25)
            for c in s.get("circles") or []:
                M.put(c["at"], M.scratch(0.22), 0.45)
            for c in s.get("callouts") or []:
                M.put(c["at"], M.tick(3000, 0.04), 0.5)
        elif ty == "print":
            M.put(T0 - 0.1, M.whoosh(0.4), 0.3, -0.2)
            M.put(T0 + 0.35, M.thud(0.35), 0.35)
            for q in (s.get("side") or {}).get("lines") or []:
                M.put(q["at"], M.tick(2400, 0.035), 0.3)
            for c in s.get("circles") or []:
                M.put(c["at"], M.scratch(0.22), 0.45)
        elif ty == "file":
            M.put(T0 - 0.1, M.whoosh(0.5), 0.3, -0.2)
            for r in s.get("rows") or []:
                for k in range(2):
                    M.put(r["at"] + k * 0.06, M.key(), 0.3)
        elif ty == "kinetic":
            for q in s["items"]:
                M.put(q["at"] - 0.02, M.thud(0.4), 0.42)
        elif ty == "slam":
            M.put(s["at"] + 0.05, M.boom(1.8), 0.85)
        elif ty == "counter":
            n = 28
            span = s["until"] - s["at"]
            for m in range(n):
                M.put(s["at"] + span * (1 - (1 - (m + 1) / n) ** 0.5), M.tick(2200 + m * 30, 0.03), 0.28)
            M.put(s["until"], M.thud(0.6), 0.7)
        elif ty == "bars":
            for q in s["items"]:
                M.put(q["at"], M.tone(0.45, 180, 360), 0.8)
                M.put(q["at"] + 0.45, M.thud(0.3), 0.3)
        elif ty == "timeline":
            for q in s["items"]:
                M.put(q["at"], M.tick(2400, 0.04), 0.5)
                M.put(q["at"], M.thud(0.3), 0.25)
        elif ty == "map":
            M.put(T0 - 0.3, M.whoosh(0.6), 0.3)
            for r in s.get("routes") or []:
                M.put(r["at"], M.tone(max(0.3, r["until"] - r["at"])), 0.9)
            for p in s.get("pins") or []:
                M.put(p["at"] + 0.25, M.blip(), 0.5, 0.3)
        elif ty == "quote":
            L = len(s["text"])
            n = min(40, L)
            for k in range(n):
                M.put(s["at"] + (k / n) * s["typeDur"], M.key(), 0.3, ((k % 5) - 2) * 0.08)
        elif ty == "org":
            for q in s["nodes"]:
                M.put(q["at"], M.tick(2800, 0.04), 0.45)
                M.put(q["at"] + 0.02, M.thud(0.3), 0.22)
        elif ty == "ledger":
            for r in s.get("rows") or []:
                for k in range(3):
                    M.put(r["at"] + k * 0.05, M.key(), 0.35)
            if s.get("total"):
                M.put(s["total"]["at"], M.thud(0.6), 0.8)
        elif ty == "split":
            M.put(s["a"]["at"], M.thud(0.4), 0.5, -0.3)
            M.put(s["b"]["at"], M.thud(0.4), 0.5, 0.3)
            if s.get("sign"):
                M.put(s["signAt"] + 0.05, M.boom(1.4, 60, 36), 0.7)
        elif ty == "date":
            for k in range(len(s.get("day") or "")):
                M.put(s["dayAt"] + k * 0.045, M.key(), 0.35, (k - 3) * 0.04)
            groups = "".join(c if c.isdigit() else " " for c in s["date"]).split()
            for gi, grp in enumerate(groups):
                for j in range(len(grp)):
                    for m in range(8):
                        M.put(s["groupAt"][gi] - 0.05 + j * 0.07 + 0.55 * (1 - (1 - m / 8) ** 2.2), M.tick(2600 + 200 * j), 0.22, 0.1 * (j - 1))
        elif ty == "cards":
            for k, f in enumerate(s["flips"]):
                M.put(f - 0.05, M.whoosh(0.3), 0.35, (k - 1) * 0.4)
                M.put(f + 0.4, M.tick(1800, 0.05), 0.5, (k - 1) * 0.4)
            if s.get("sumAt") is not None:
                M.put(s["sumAt"], M.thud(0.5), 0.6)
            if s.get("zeroAt") is not None:
                M.put(s["zeroAt"] + 0.05, M.boom(2.0), 0.9)
        # ---- cảnh noir ----
        if s.get("film"):
            M.put(T0, M.projector(T1 - T0), 0.16)
        if ty == "seismo":
            M.put(T0, M.needle(T1 - T0), 0.3)
            M.put(s["hitAt"], M.boom(3.2, 46, 24), 1.0)
            M.put(s["hitAt"], M.rumble(3.5), 0.7)
        elif ty == "saint":
            M.put(s["burnAt"] - 0.5, M.match(), 0.7, 0.15)
            M.put(s["burnAt"], M.fire(s["burnDur"] + 1.2), 0.45)
            M.put(s["burnAt"] - 0.1, M.whoosh(0.5), 0.25)
        elif ty == "paper":
            M.put(T0, M.whoosh(0.9), 0.4)
            M.put(T0 + 0.85, M.paper(0.5), 0.6)
            M.put(T0 + 0.9, M.thud(0.5), 0.6)
        elif ty == "pizzini":
            for q in s.get("notes") or []:
                M.put(q["at"] - 0.4, M.paper(0.4), 0.45)
                n = min(40, len(q["text"]))
                for k in range(n):
                    M.put(q["at"] + (k / n) * q["typeDur"], M.key(), 0.3, ((k % 5) - 2) * 0.08)
            c = s.get("cipher")
            if c:
                for k in range(len(c["word"])):
                    M.put(c["at"] + k * 0.18, M.tick(2600, 0.04), 0.45)
                M.put(c["decodeAt"], M.thud(0.5), 0.6)
        elif ty == "dots":
            for k in range(24):
                M.put(T0 + 0.2 + k * s.get("appearDur", 1.2) / 24, M.tick(2400 + 40 * k, 0.03), 0.25)
            for g in s.get("groups") or []:
                M.put(g["at"], M.tone(0.8, 160, 320), 0.8)
                M.put(g["at"] + 0.8, M.thud(0.4), 0.4)
        elif ty == "board":
            for q in s.get("pins") or []:
                M.put(q["at"], M.thud(0.35), 0.45, 0.2)
            for q in s.get("links") or []:
                M.put(q["at"], M.scratch(0.4), 0.45)
        elif ty == "memorial":
            M.put(T0 + 0.2, M.bell(), 0.55)
            for q in s["names"]:
                M.put(q["at"], M.thud(0.3), 0.15)
        elif ty == "calendar":
            a, N = T0 + 0.7, s["days"]
            for k in range(N):
                t = a + (s["endAt"] - a) * (0.5 - 0.5 * np.cos(np.pi * (k + 1) / N)) - 0.3
                M.put(t, M.paper(0.12), 0.35, ((k % 3) - 1) * 0.2)
            t, gap = a, 0.9
            while t < s["endAt"] - 0.3:
                M.put(t, M.heart(), 0.55)
                t += gap; gap = max(0.5, gap * 0.94)
            M.put(s["endAt"], M.boom(2.4, 50, 28), 0.9)
        elif ty == "sticker":
            for q in s["items"]:
                M.put(q["at"], M.slap(), 0.6, ((q.get("x", 960) - 960) / 960) * 0.5)
        if ty == "quote" and s.get("radio"):
            M.put(s["voiceAt"] - 0.3, M.static(s["voiceEnd"] - s["voiceAt"] + 0.6), 0.12)
        for q in s.get("sfx") or []:          # tiếng đặt tay: [{"k": "gavel"|"bell"|"heart"|…, "at": mốc, "gain": 0.6}]
            if q["k"] not in NoirMix.CUES:
                raise ValueError(f"sfx lạ: {q['k']}")
            M.put(q["at"], getattr(M, q["k"])(), q.get("gain", 0.6), q.get("pan", 0.0))
    # KHÔNG chuẩn hoá theo đỉnh như Short: mỗi chương phải cùng một mức, chương ít tiếng động không được to lên
    import wave
    out = (np.clip(M.bed * 0.5, -1, 1) * 32767).astype("<i2")
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
