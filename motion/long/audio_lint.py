"""Lint âm thanh trước khi ra final (23/10/2026, docs/pm/2026-10-22-cl-am-thanh-set-set.md mục S4).

Khán giả CL chê "sẹt sẹt": giọng Anh Khôi có xung buzz > 5 kHz theo từng chu kỳ cao độ, tiếng động noir có cạnh vuông,
mỗi đầu chương có tiếng "tách". Lint này đo lại đúng các chỉ số của bản chẩn đoán để lỗi không quay lại âm thầm:
- buzz: khung 20 ms có lời, phần > 5 kHz -> độ nổi xung (đỉnh HF so với RMS toàn dải, dB), kurtosis, % khung crest > 6;
- true peak (ffmpeg ebur128) của thành phẩm;
- mẫu đầu/cuối mỗi đoạn ghép (mixpad) + số mẫu clip cứng của sfx;
- số click/phút (đỉnh đường bao > 6 kHz vượt 12 dB trung vị cục bộ 50 ms, như set/voicem.py).
CL: vượt ngưỡng -> CHẶN. Kênh khác: chỉ cảnh báo (MIM/CK/BUD/FS chưa ai chê, ngưỡng lấy theo CL).

CLI đo tay: python motion/long/audio_lint.py <file.wav|mp4> ...
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 48000

# ---- ngưỡng (số đo 22–23/10/2026, bảng 1b/1d/mục 5 của bản chẩn đoán + đo lại 5 giọng Anh Khôi/Thiện Minh) ----
# Đo trên GIỌNG ĐÃ QUA chuỗi lọc của kênh (không đo trên thành phẩm: sfx/nhạc dải cao làm số vô nghĩa, MIM final −15 dB).
# kurtosis HF trung vị: Anh Khôi/Thiện Minh 4,8–6,8 (lọc không hạ được: lọc chỉ hạ MỨC xung), Thanh Bình 3,3–4,1,
# Ngọc Huyền ~1,6. > KURT_BUZZ = giọng kiểu buzz -> cảnh báo, và xét tiếp độ nổi xung:
KURT_BUZZ = 4.5
# độ nổi xung HF (đỉnh > 5 kHz so với RMS toàn dải, trung vị, dB) của giọng buzz: thô −18,9…−20,6, VOICE_FX cũ −16,5…−18,0,
# bộ lọc CL mới (chủ kênh chọn) −21,8…−23,3. Giọng buzz mà nổi hơn −21,0 dB = chưa qua bộ lọc CL -> LỖI.
PROM_MAX = -21.0
CREST_WARN = 35.0    # % khung crest HF > 6: Anh Khôi 35–45 %, Thanh Bình 16–22 % -> chỉ cảnh báo
TP_MAX = -1.0        # dBTP thành phẩm (loudnorm đặt −1,5; AAC có thể vọt lên)
EDGE_MAX = -60.0     # dBFS mẫu đầu/cuối mỗi đoạn ghép: trước sửa −11…−33 dBFS (tiếng "tách")
CLIP_MAX = 0         # số mẫu |x| ≥ 0,999 cho phép trong sfx.wav (Long CL cũ: 8–99)
JUMP_LO, JUMP_HI = 0.001, 0.03   # "tách": lặng (< −60 dBFS suốt 1 ms) rồi một mẫu nhảy > −30 dBFS (đầu chương cũ: −17…−33)


def _ffmpeg() -> str:
    """Người gọi (build_long / stier build) truyền ffmpeg của pipeline; CLI dùng FFMPEG_DIR hoặc ffmpeg trong PATH."""
    import os
    import shutil
    d = os.environ.get("FFMPEG_DIR")
    return os.path.join(d, "ffmpeg") if d else (shutil.which("ffmpeg") or "ffmpeg")


def load(p: Path, ffmpeg: str | None = None) -> np.ndarray:
    """(N, 2) float32 48 kHz: wav đọc thẳng, file khác (mp4/m4a) giải mã bằng ffmpeg."""
    p = Path(p)
    if p.suffix.lower() == ".wav":
        import soundfile as sf
        x, sr = sf.read(str(p), dtype="float32", always_2d=True)
        if sr == SR:
            return x if x.shape[1] == 2 else np.repeat(x[:, :1], 2, 1)
    r = subprocess.run([ffmpeg or _ffmpeg(), "-v", "error", "-i", str(p), "-vn", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"không giải mã được {p}: {r.stderr[-300:]!r}")
    return np.frombuffer(r.stdout, "<f4").reshape(-1, 2)


def buzz(x: np.ndarray, sr: int = SR) -> dict:
    """Chỉ số xung HF trong khung có lời (y như set/pulse.py của bản chẩn đoán)."""
    from scipy.signal import butter, sosfilt
    from scipy.stats import kurtosis
    m = x.mean(1).astype("float64") if x.ndim == 2 else x.astype("float64")
    y = sosfilt(butter(6, 5000, btype="high", fs=sr, output="sos"), m)
    w = int(0.02 * sr); n = len(y) // w
    if n == 0:
        return {"prom": None, "kurt": None, "crest6": None}
    Y = y[:n * w].reshape(n, w); X = m[:n * w].reshape(n, w)
    e = np.sqrt((X ** 2).mean(1)); sp = e > e.max() * 0.05
    if not sp.any():
        return {"prom": None, "kurt": None, "crest6": None}
    prom = 20 * np.log10(np.abs(Y[sp]).max(1) / e[sp] + 1e-20)
    cr = np.abs(Y[sp]).max(1) / (np.sqrt((Y[sp] ** 2).mean(1)) + 1e-20)
    return {"prom": round(float(np.median(prom)), 1), "kurt": round(float(np.median(kurtosis(Y[sp], axis=1))), 2),
            "crest6": round(float((cr > 6).mean() * 100), 1)}


def clicks_per_min(x: np.ndarray, sr: int = SR) -> float:
    """Đỉnh đường bao > 6 kHz (bước 2 ms) vượt 12 dB so với trung vị cục bộ 50 ms (như set/voicem.py)."""
    from scipy.ndimage import median_filter
    from scipy.signal import butter, sosfilt
    m = x.mean(1).astype("float64") if x.ndim == 2 else x.astype("float64")
    y = sosfilt(butter(4, 6000, btype="high", fs=sr, output="sos"), m)
    hop = int(0.002 * sr)
    k = len(y) // hop
    env = np.sqrt((y[:k * hop] ** 2).reshape(k, hop).mean(1) + 1e-20)
    med = median_filter(env, size=25)
    sp = (20 * np.log10(env / (med + 1e-12)) > 12) & (env > env.max() * 0.02)
    return round(float((sp[1:] & ~sp[:-1]).sum()) / max(len(m) / sr, 1) * 60, 1)


def edges_db(x: np.ndarray) -> tuple[float, float]:
    """dBFS của mẫu đầu và cuối (lớn nhất giữa hai kênh)."""
    f = lambda v: round(float(20 * np.log10(np.abs(v).max() + 1e-12)), 1)
    return f(x[0]), f(x[-1])


def n_clip(x: np.ndarray) -> int:
    return int((np.abs(x) >= 0.999).sum())


def true_peak(p: Path, ffmpeg: str | None = None) -> tuple[float | None, float | None]:
    """(true peak dBTP, độ to tích hợp LUFS) bằng ffmpeg ebur128=peak=true."""
    r = subprocess.run([ffmpeg or _ffmpeg(), "-hide_banner", "-nostats", "-i", str(p), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    s = r.stderr[r.stderr.rfind("Summary:"):]
    tp = re.search(r"True peak:\s*Peak:\s*(-?[\d.]+|-inf)", s)
    li = re.search(r"Integrated loudness:\s*I:\s*(-?[\d.]+)", s)
    num = lambda m: (None if not m else (-999.0 if m.group(1) == "-inf" else float(m.group(1))))
    return num(tp), num(li)


def n_jumps(x: np.ndarray) -> int:
    """Số chỗ "tách": 1 ms trước gần như lặng (< JUMP_LO) rồi một mẫu nhảy lên > JUMP_HI (tiếng bắt đầu giữa đường bao)."""
    a = np.abs(x).max(1) if x.ndim == 2 else np.abs(x)
    if not len(a):
        return 0
    edge = int(a[0] > JUMP_HI) + int(a[-1] > JUMP_HI)   # mép file = chỗ nối với đoạn lặng/đoạn khác (đầu chương)
    w = int(0.001 * SR)                     # 48 mẫu (chẵn)
    hit = np.flatnonzero(a[w:] > JUMP_HI) + w
    if not len(hit):
        return edge
    from scipy.ndimage import maximum_filter1d
    mf = maximum_filter1d(a, size=w)        # cửa sổ giữa: tâm c phủ c-w/2 … c+w/2-1
    return edge + int((mf[hit - w // 2] < JUMP_LO).sum())   # tâm hit-w/2 = đúng w mẫu NGAY TRƯỚC mẫu nhảy


def measure(p: Path, ffmpeg: str | None = None) -> dict:
    """Mọi chỉ số của một file (dùng cho A/B trước/sau và CLI)."""
    x = load(p, ffmpeg)
    tp, li = true_peak(p, ffmpeg)
    return {**buzz(x), "tp": tp, "lufs": li, "clicks_min": clicks_per_min(x), "jumps": n_jumps(x), "edge": edges_db(x), "clip": n_clip(x)}


def mastered_voice(voice: Path, fx: str | None, ffmpeg: str | None = None) -> np.ndarray:
    """Giọng sau đúng chuỗi lọc của kênh (fx None = giọng thô, như Short MIM/CK)."""
    if not fx:
        return load(voice, ffmpeg)
    r = subprocess.run([ffmpeg or _ffmpeg(), "-v", "error", "-i", str(voice), "-af", f"aresample={SR},{fx}", "-f", "f32le", "-ac", "1", "-"],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"lọc giọng hỏng {voice}: {r.stderr[-300:]!r}")
    return np.frombuffer(r.stdout, "<f4")


def check_voices(voices: list[tuple[str, Path]], fx: str | None, ffmpeg: str | None = None) -> tuple[list[str], list[str], dict]:
    """Xung buzz của giọng đã lọc, từng đoạn (Short: 1, Long: mỗi chương): (lỗi theo đoạn, cảnh báo gộp, số đo theo đoạn)."""
    err, ms = [], {}
    for name, p in voices:
        b = ms[name] = buzz(mastered_voice(p, fx, ffmpeg))
        if b["kurt"] is not None and b["kurt"] > KURT_BUZZ and b["prom"] > PROM_MAX:
            err.append(f"{name}: xung buzz HF nổi {b['prom']} dB > {PROM_MAX} dB, kurtosis {b['kurt']} "
                       "(giọng buzz chưa qua bộ lọc CL? themes.VOICE_FX_CL)")
    warn = []
    ks = [b["kurt"] for b in ms.values() if b["kurt"] is not None]
    cs = [b["crest6"] for b in ms.values() if b["crest6"] is not None]
    if ks and max(ks) > KURT_BUZZ:   # gộp một dòng: video dài 15 chương không in 15 lần
        warn.append(f"giọng kiểu buzz: kurtosis HF đến {max(ks)} > {KURT_BUZZ} (lọc chỉ hạ mức xung, đổi giọng mới hết)")
    if cs and max(cs) > CREST_WARN:
        warn.append(f"đến {max(cs)} % khung có crest HF > 6 (ngưỡng {CREST_WARN} %)")
    return err, warn, ms


def check_final(p: Path, ffmpeg: str | None = None) -> tuple[list[str], dict]:
    """Thành phẩm: true peak + mẫu đầu/cuối -> (lỗi, số đo)."""
    tp, li = true_peak(p, ffmpeg)
    err = [f"true peak {tp} dBTP > {TP_MAX}"] if tp is not None and tp > TP_MAX else []
    return err, {"tp": tp, "lufs": li}


def check_parts(parts: list[Path], sfx: list[Path] = ()) -> list[str]:
    """Long: mẫu đầu/cuối mỗi đoạn ghép (mixpad.wav) và clip cứng trong sfx.wav -> danh sách lỗi."""
    err = []
    for p in parts:
        a, z = edges_db(load(p))
        if max(a, z) > EDGE_MAX:
            err.append(f"{p.parent.name}/{p.name}: mẫu đầu {a} / cuối {z} dBFS > {EDGE_MAX} (tiếng tách ở chỗ nối)")
    for p in sfx:
        c = n_clip(load(p))
        if c > CLIP_MAX:
            err.append(f"{p.parent.name}/{p.name}: {c} mẫu clip cứng (≥ 0,999)")
    return err


def report(tag: str, err: list[str], warn: list[str], block: bool) -> None:
    """In kết quả; `block` (kênh CL) + có lỗi -> SystemExit. Kênh khác: lỗi in thành cảnh báo."""
    for w in warn:
        print(f"  ! audio_lint {tag}: {w}", flush=True)
    for e in err:
        print(f"  ! audio_lint {tag}: {'LỖI' if block else 'WARNING'} {e}", flush=True)
    if err and block:
        raise SystemExit(f"{tag}: audio_lint chặn (CL): " + " | ".join(err))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from factory.console import utf8_console  # noqa: E402
    utf8_console()
    for a in sys.argv[1:]:
        print(a, measure(Path(a)), flush=True)
