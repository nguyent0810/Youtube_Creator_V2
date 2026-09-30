"""Mốc thời gian từng từ bám theo âm thanh TTS thật (video dài).

Trước đây mốc từ chia theo tỉ lệ số ký tự trong cả segment -- lệch khi câu có
khoảng lặng đầu/cuối, có số ("1979" đọc thành 7 âm tiết), hay ngắt hơi giữa
câu. Chữ động, bút dạ quang, ghim bản đồ... đều bám mốc từ, nên lệch là thấy.

Không dùng Whisper (không cài, không tải model): giọng TTS sạch và tiếng Việt
đơn âm tiết -- mỗi từ là một âm tiết. Cách làm:
  1. Đường năng lượng (RMS) của cả file, cắt khoảng lặng hai đầu mỗi câu.
  2. Trọng số mỗi từ = số âm tiết THỰC SỰ đọc (số đọc thành chữ), dấu câu thêm
     một nhịp ngắt.
  3. Chia khoảng có tiếng theo trọng số, rồi nắn từng ranh giới về chỗ năng
     lượng thấp nhất gần đó (khe giữa hai âm tiết) -- như đo "chỗ lấy hơi".
"""
from __future__ import annotations

import re

import numpy as np

HOP_S = 0.005
_DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def vi_number_syllables(n: int) -> int:
    """Số âm tiết khi đọc số nguyên kiểu Việt (1979 -> một nghìn chín trăm bảy
    mươi chín = 7). Đủ cho năm sinh, tuổi, số thứ tự trong kịch bản."""
    if n < 10:
        return 1
    if n < 20:
        return 1 + (1 if n % 10 else 0)            # mười / mười hai
    if n < 100:
        return 2 + (1 if n % 10 else 0)            # hai mươi / hai mươi mốt
    if n < 1000:
        h, r = divmod(n, 100)
        if r == 0:
            return 2                               # ba trăm
        if r < 10:
            return 2 + 1 + 1                       # ba trăm lẻ năm
        return 2 + vi_number_syllables(r)
    if n < 1_000_000:
        th, r = divmod(n, 1000)
        head = vi_number_syllables(th) + 1         # hai nghìn
        if r == 0:
            return head
        if r < 100:
            return head + 2 + (1 if r < 10 else 0) + vi_number_syllables(r)  # không trăm (lẻ) ...
        return head + vi_number_syllables(r)
    return max(1, len(str(n)))


def token_weight(tok: str) -> float:
    core = re.sub(r"[^\w]", "", tok, flags=re.UNICODE)
    pause = 0.6 if re.search(r"[,;:.!?…]$", tok.strip()) else 0.0
    if not core:
        return pause
    if core.isdigit():
        return vi_number_syllables(int(core)) + pause
    return 1.0 + pause


def energy_envelope(wav_path) -> tuple[np.ndarray, float]:
    """RMS 17ms, bước 5ms, làm mượt nhẹ. Trả (envelope, hop giây)."""
    import soundfile as sf  # noqa: PLC0415
    y, sr = sf.read(str(wav_path), dtype="float32", always_2d=False)
    if y.ndim > 1:
        y = y.mean(axis=1)
    hop, win = max(1, int(sr * HOP_S)), max(2, int(sr * 0.017))
    n = max(1, (len(y) - win) // hop + 1)
    idx = np.arange(win)[None, :] + hop * np.arange(n)[:, None]
    rms = np.sqrt((y[idx] ** 2).mean(axis=1))
    k = np.ones(5) / 5
    return np.convolve(rms, k, mode="same"), hop / sr


def word_times(env: np.ndarray, hop: float, start: float, end: float, weights: list[float]) -> list[tuple[float, float]]:
    """(t, d) cho từng từ trong [start, end] theo năng lượng thật."""
    n = len(weights)
    if n == 0:
        return []
    i0, i1 = int(start / hop), max(int(start / hop) + 2, int(end / hop))
    seg = env[i0:i1]
    if len(seg) < 4 or seg.max() <= 0:
        return _proportional(start, end, weights)
    thr = seg.max() * 0.12
    voiced = np.where(seg > thr)[0]
    v0 = start + voiced[0] * hop
    v1 = start + (voiced[-1] + 1) * hop
    if v1 - v0 < 0.15:
        v0, v1 = start, end
    w = np.array([max(x, 0.05) for x in weights], dtype=float)
    cum = np.concatenate([[0], np.cumsum(w)]) / w.sum()
    bounds = v0 + cum * (v1 - v0)
    avg = (v1 - v0) / max(1.0, w.sum())
    # Nắn ranh giới trong về khe năng lượng gần nhất; giữ thứ tự, cách nhau >= 60ms.
    for k in range(1, n):
        lo = max(bounds[k] - 0.45 * avg, bounds[k - 1] + 0.06)
        hi = min(bounds[k] + 0.45 * avg, v1 - 0.06)
        a, b = int(lo / hop) - i0, int(hi / hop) - i0
        if b - a >= 2:
            j = a + int(np.argmin(seg[a:b]))
            bounds[k] = start + j * hop
    return [(round(float(bounds[k]), 3), round(float(bounds[k + 1] - bounds[k]), 3)) for k in range(n)]


def _proportional(start: float, end: float, weights: list[float]) -> list[tuple[float, float]]:
    tot = sum(max(w, 0.05) for w in weights)
    out, t = [], start
    for w in weights:
        d = (end - start) * max(w, 0.05) / tot
        out.append((round(t, 3), round(d, 3))); t += d
    return out
