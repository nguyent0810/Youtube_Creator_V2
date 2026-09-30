"""Chép lời audio tham khảo (chỉ để PHÂN TÍCH cách hành văn, không tái sử dụng câu chữ).

    <venv-video>/python motion/long/transcribe.py <audio.mp3> <out.json>

Dùng faster-whisper large-v3-turbo trên GPU, có mốc từng từ -> đo nhịp đọc, độ dài câu, khoảng lặng.
"""
import json
import os
import sys
import time
from pathlib import Path

# cuBLAS/cuDNN lấy từ wheel nvidia-*-cu12 trong venv (Windows không có CUDA toolkit hệ thống)
for _d in (Path(sys.prefix) / "Lib" / "site-packages" / "nvidia").glob("*/bin"):
    os.add_dll_directory(str(_d))
    os.environ["PATH"] = str(_d) + os.pathsep + os.environ["PATH"]

from faster_whisper import WhisperModel  # noqa: E402

src, dst = sys.argv[1], sys.argv[2]
t0 = time.time()
model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
segs, info = model.transcribe(src, language="vi", word_timestamps=True, vad_filter=True, beam_size=5)
out = []
for s in segs:
    out.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                "words": [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for w in (s.words or [])]})
    if len(out) % 50 == 0:
        print(f"{s.end/60:.1f} phút", flush=True)
json.dump({"duration": info.duration, "segments": out}, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"xong {len(out)} đoạn trong {time.time()-t0:.0f}s")
