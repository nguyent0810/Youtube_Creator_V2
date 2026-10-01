"""Bước 2 của best-of-N: Whisper (large-v3-turbo, CUDA) nghe lại mọi bản đọc trong tts/takes.json.

    C:\Tools\Youtuber\video-editor\.venv-video\Scripts\python.exe motion/long/stt_takes.py <topic>

Ghi tts/transcripts.json {tên_file: chữ nghe được}; file đã nghe rồi thì bỏ qua (chạy lại an toàn).
Chấm điểm + chọn bản ở `build_long.py <topic> pick` (cần bộ chuẩn hoá số->chữ của vieneu).
"""
import json
import os
import sys
import time
from pathlib import Path

for _d in (Path(sys.prefix) / "Lib" / "site-packages" / "nvidia").glob("*/bin"):
    os.add_dll_directory(str(_d))
    os.environ["PATH"] = str(_d) + os.pathsep + os.environ["PATH"]
from faster_whisper import WhisperModel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
cache = ROOT / "output" / "long" / sys.argv[1] / "tts"
rows = json.loads((cache / "takes.json").read_text(encoding="utf-8"))
out_f = cache / "transcripts.json"
hyp = json.loads(out_f.read_text(encoding="utf-8")) if out_f.exists() else {}
todo = [(r["text"], f) for r in rows for f in r["files"] if f not in hyp]
print(f"{len(todo)} bản cần nghe ({len(hyp)} đã có)", flush=True)
m = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
t0 = time.time()
for i, (_, f) in enumerate(todo, 1):
    # KHÔNG dùng initial_prompt = câu viết: Whisper sẽ "nghe" theo chữ mẫu và che mất lỗi đọc sai số/nuốt chữ
    segs, _ = m.transcribe(str(cache / f), language="vi", beam_size=5, vad_filter=False, condition_on_previous_text=False)
    hyp[f] = " ".join(s.text.strip() for s in segs)
    if i % 100 == 0 or i == len(todo):
        out_f.write_text(json.dumps(hyp, ensure_ascii=False, indent=0), encoding="utf-8")
        print(f"  {i}/{len(todo)} ({time.time() - t0:.0f}s)", flush=True)
