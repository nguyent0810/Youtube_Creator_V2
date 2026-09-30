"""Thiết kế âm thanh cho composition "Mona Lisa" — tổng hợp thủ tục (numpy), không thư viện âm.

    python motion/build_monalisa_sfx.py        -> output/stier/sfx.wav (48 kHz stereo)

Mỗi tiếng động đặt theo CÙNG mốc từng từ mà composition dùng (data.js), nên
hình và tiếng khớp nhau từng khung. Ngữ pháp âm theo xu hướng tài liệu tối
giản: nền trầm liên tục, tiếng "đập" chỉ ở khoảnh khắc lật (biến mất, đóng
cửa, bị bắt), và LẶNG hẳn trước câu chốt "Còn bức tranh?".
"""
from __future__ import annotations

import json
import re
import unicodedata
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SR = 48000
rng = np.random.default_rng(1911)

src = (HERE / "hf" / "assets" / "monalisa" / "data.js").read_text(encoding="utf-8")
ML = json.loads(src[src.index("{"): src.rindex("}") + 1])
L = ML["lines"]
DUR = 34.2
N = int(DUR * SR)
bed = np.zeros((N, 2))


def norm(w):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", w.lower()))


def S(i): return L[i]["start"]
def E(i): return L[i]["end"]


def T(i, w, n=0):
    c = 0
    for x in L[i]["words"]:
        if norm(x["w"]) == norm(w):
            if c == n:
                return x["t"]
            c += 1
    return S(i)


def env(n, a=0.002, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)


def lp(x, k):
    """Lọc thông thấp một cực (k nhỏ = tối hơn)."""
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc); y[i] = acc
    return y


def put(t, sig, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i] * gain
    bed[i:i + len(sig), 0] += sig * (1 - max(0, pan))
    bed[i:i + len(sig), 1] += sig * (1 + min(0, pan))


def boom(dur=1.6, f0=58, f1=34):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.45)
    click = lp(rng.standard_normal(n), 0.25) * env(n, 0.001, 0.018)
    return s + 0.6 * click


def thud(dur=0.5):
    n = int(dur * SR)
    return lp(rng.standard_normal(n), 0.04) * env(n, 0.001, 0.07) * 4 + boom(dur, 90, 50) * 0.5


def whoosh(dur=0.6, rise=True):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    shape = np.sin(np.pi * (t if rise else 1 - t) ** 0.8) ** 2
    k = 0.02 + 0.2 * (t if rise else 1 - t)
    x = rng.standard_normal(n); y = np.empty(n); acc = 0.0
    for i in range(n):
        acc += k[i] * (x[i] - acc); y[i] = acc
    return y * shape * 2.2


def tick(f=3200, dur=0.03):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * 0.5 + rng.standard_normal(n) * 0.5) * env(n, 0.0005, 0.006)


def key():   # gõ máy chữ
    return tick(1800, 0.05) * 1.3 + lp(rng.standard_normal(int(0.05 * SR)), 0.3) * env(int(0.05 * SR), 0.0005, 0.01)


def scratch(dur=0.28):   # bút dạ vạch giấy
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t))
    return (x - lp(x, 0.15)) * np.sin(np.pi * t / dur) * 0.35


def clank():   # song sắt: phổ không hài
    n = int(1.2 * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((213, 1), (587, .6), (1142, .45), (1893, .3)))
    return s * env(n, 0.001, 0.18) * 0.35


def pad(freqs, dur, a=1.2, r=2.5):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate(freqs)) / len(freqs)
    return s * np.minimum(1, t / a) * np.minimum(1, (dur - t) / r)


# ---------- nền trầm: drone + hơi phòng, lặng hẳn ở câu hỏi ----------
t = np.arange(N) / SR
drone = (np.sin(2 * np.pi * 43.65 * t) * 0.55 + np.sin(2 * np.pi * 65.4 * t + 1) * 0.25
         + np.sin(2 * np.pi * 87.3 * t * (1 + 0.002 * np.sin(2 * np.pi * 0.1 * t))) * 0.12)
air = lp(rng.standard_normal(N), 0.01) * 0.9
g = np.clip(t / 1.5, 0, 1) * (0.7 + 0.3 * np.clip((t - S(9)) / 4, 0, 1))   # dày dần về cao trào
q0, q1 = S(12) - 0.12, S(13)
g = np.where((t > q0) & (t < q1), 0, g)                                     # LẶNG
g = np.where((t >= q0 - 0.3) & (t <= q0), g * (q0 - t) / 0.3, g)
g = np.where((t >= q1) & (t <= q1 + 0.8), g * (t - q1) / 0.8, g)
bed[:, 0] += (drone + air) * g * 0.22
bed[:, 1] += (drone * 0.97 + air) * g * 0.22

# ---------- S0 ----------
put(T(0, "từng") - 0.02, scratch(0.34), 1.0, -0.2)
put(T(0, "một") - 0.05, thud(0.4), 0.35)
tb = T(1, "biến")
put(tb - 0.62, whoosh(0.7), 0.55)
put(tb + 0.05, boom(2.0), 1.0)

# ---------- S2 Louvre ----------
put(S(2) - 0.25, whoosh(0.45), 0.35, 0.3)
for k in range(7):
    put(T(2, "thứ") + k * 0.045, key(), 0.5, (k - 3) * 0.05)
for t0, cnt in ((T(2, "21"), 2), (T(2, "8"), 2), (T(2, "1911"), 4)):
    for j in range(cnt):
        for m in range(8):
            put(t0 - 0.05 + j * 0.07 + 0.55 * (1 - (1 - m / 8) ** 2.2), tick(2600 + 200 * j), 0.28, 0.1 * (j - 1))
put(T(2, "đóng") + 0.1, thud(0.6), 1.0)
put(T(2, "đóng") + 0.1, boom(1.2, 70, 40), 0.5)

# ---------- S3 báo ----------
put(S(3), tick(5200, 0.06) * 3, 0.5)
for w, pan in (("người", -0.3), ("lắp", 0.3), ("lặng", -0.3)):
    put(T(3, w) - 0.35, whoosh(0.8), 0.28, pan)

# ---------- S4 đồng hồ ----------
k = 0; tt = S(4)
while tt < E(4):
    put(tt, tick(4200 if k % 2 else 3000, 0.025), 0.45, 0.15 if k % 2 else -0.15)
    tt += 0.075 + 0.06 * abs(np.sin(k * 0.4)); k += 1
put(T(4, "phát") - 0.1, thud(0.35), 0.55)

# ---------- S5 lịch: 14 nét gạch ----------
for c in range(7):
    put(S(5) + 0.45 + c * 0.1, scratch(0.12), 0.8, (c - 3) * 0.1)
    put(S(5) + 0.51 + c * 0.1, scratch(0.12), 0.8, (c - 3) * 0.1)

# ---------- S6 Picasso ----------
put(S(6) - 0.1, whoosh(0.5), 0.35, -0.2)
put(T(6, "thẩm") + 0.1, thud(0.6), 0.9)

# ---------- S7 đám đông rì rầm ----------
n = int((E(7) - S(7) + 0.4) * SR); x = rng.standard_normal(n)
mur = (lp(x, 0.08) - lp(x, 0.012)) * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * np.arange(n) / SR) ** 2)
put(S(7) - 0.1, mur * np.minimum(1, np.arange(n) / (0.4 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.3 * SR)), 1.3)

# ---------- S8 bức tường ----------
put(S(8), tick(5200, 0.06) * 3, 0.5)
put(S(8) + 0.02, boom(1.4, 50, 32), 0.55)
for kk in range(4):
    put(T(8, "trống") - 0.15 + kk * 0.1, scratch(0.22), 0.5, (kk - 1.5) * 0.2)

# ---------- S9 28 tháng + rương ----------
dur9 = T(9, "tháng") + 0.25 - S(9)
for m in range(28):
    tm = S(9) + dur9 * (1 - (1 - (m + 1) / 28) ** 0.5)   # khớp ease power2.out của bộ đếm
    put(tm, tick(2200 + m * 30, 0.03), 0.35)
put(T(9, "nằm") - 0.1, whoosh(0.45, False), 0.3)
put(T(9, "rương") + 0.03, thud(0.7), 1.0)

# ---------- S10 bản đồ + bị bắt ----------
put(S(10) - 0.3, whoosh(0.6), 0.4, 0.2)
d10 = T(10, "florence") - T(10, "mang") + 0.35
n = int(d10 * SR); tr = np.arange(n) / SR
put(T(10, "mang") - 0.1, np.sin(2 * np.pi * np.cumsum(220 + 220 * tr / d10) / SR) * np.sin(np.pi * tr / d10) * 0.18, 1.0)
put(T(10, "florence") + 0.25, tick(1500, 0.08) * 2, 0.6, 0.4)
tbat = T(10, "bắt")
put(tbat - 0.55, whoosh(0.35), 0.5)
put(tbat - 0.13, thud(0.5), 0.8)
put(tbat + 0.16, boom(2.2, 62, 30), 1.1)

# ---------- S11 song sắt ----------
for kk in range(8):
    put(S(11) + 0.05 + kk * 0.035 + 0.3, clank(), 0.45, (kk - 3.5) * 0.12)

# ---------- S13 trở lại: hợp âm ấm, khép vòng ----------
put(S(13) - 0.02, boom(1.6, 48, 36), 0.5)
put(S(13), pad([130.8, 164.8, 196.0, 261.6], DUR - S(13) + 0.1, 0.25, 1.2), 0.35)

peak = np.max(np.abs(bed)) or 1.0
out = (bed / peak * 0.9 * 32767).astype("<i2")
dst = HERE.parent / "output" / "stier" / "sfx.wav"
with wave.open(str(dst), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print(f"sfx {DUR}s -> {dst}")
