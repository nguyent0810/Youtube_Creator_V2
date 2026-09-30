"""Chuẩn bị dữ liệu cho composition S-tier "Mona Lisa": mốc từng từ + bản đồ.

    python motion/build_monalisa_data.py [khoi|binh]

- Mốc từng từ: hf_align (v1) — năng lượng RMS của chính file TTS + trọng số âm
  tiết tiếng Việt, không Whisper. Phụ đề và mọi hiệu ứng "đánh đúng chữ" bám vào đây.
- Bản đồ: hf_geo (v1) — biên giới thật từ world-atlas, nướng sẵn thành SVG path
  (composition không được fetch mạng lúc render: phải tất định).
Ghi ra motion/hf/assets/monalisa/data.js (window.ML = {...}).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hf_align  # noqa: E402
import hf_geo  # noqa: E402

VOICE = sys.argv[1] if len(sys.argv) > 1 else "khoi"
OUT = HERE.parent / "output" / "stier"
timing = json.loads((OUT / f"timing_{VOICE}.json").read_text(encoding="utf-8"))
env, hop = hf_align.energy_envelope(OUT / f"voice_{VOICE}.wav")

lines = []
for seg in timing["segments"]:
    toks = seg["text"].split()
    wts = [hf_align.token_weight(t) for t in toks]
    times = hf_align.word_times(env, hop, seg["start"], seg["end"], wts)
    lines.append({"text": seg["text"], "start": round(seg["start"], 3), "end": round(seg["end"], 3),
                  "words": [{"w": t, "t": a, "d": d} for t, (a, d) in zip(toks, times)]})

# Bản đồ dọc: vùng vẽ trong khung 1080x1920 (nửa trên màn hình).
hf_geo.BOX = (70, 330, 1010, 1330)
geo = hf_geo.bake({
    "countries": ["France", "Italy"],
    "context": ["Switzerland", "Germany", "Belgium", "Spain", "Austria", "Luxembourg", "Slovenia"],
    "bbox": [-1.8, 41.6, 14.6, 51.3],
    "pins": [{"name": "Paris", "lon": 2.3522, "lat": 48.8566},
             {"name": "Florence", "lon": 11.2558, "lat": 43.7696}],
})["_geo"]

data = {"voice": VOICE, "duration": round(timing["duration"], 3), "lines": lines, "geo": geo}
dst = HERE / "hf" / "assets" / "monalisa" / "data.js"
dst.write_text("window.ML = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"{len(lines)} câu, {sum(len(l['words']) for l in lines)} từ, "
      f"{len(geo['countries'])} nước -> {dst}  ({dst.stat().st_size // 1024} KB)")
for l in lines[:3]:
    print("  ", [(w["w"], w["t"]) for w in l["words"][:6]])
