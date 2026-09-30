"""Phụ đề SRT cho cả video dài, từ mốc từng từ của các chương (data.js) + độ dài hình đã render.

    python motion/long/srt.py <topic>  -> output/long/<topic>/captions.vi.srt
Phụ đề thật (không phải chữ in trên hình) giúp YouTube hiểu nội dung để xếp hạng tìm kiếm và dịch tự động.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FFPROBE = r"C:\Tools\Youtuber\video-editor\vendor\ffmpeg\ffprobe.exe"


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main(topic):
    sd, od = ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    cues, off = [], 0.0
    for c in spec["chapters"]:
        d = (od / c / "data.js").read_text(encoding="utf-8")
        case = json.loads(d[d.index("{"): d.rindex("}") + 1])
        for ln in case["lines"]:
            cur = []
            for k, w in enumerate(ln["words"]):
                cur.append(w)
                if (re.search(r"[.,…?!:;]$", w["w"]) and len(cur) >= 4) or len(cur) >= 10 or k == len(ln["words"]) - 1:
                    cues.append([off + cur[0]["t"], off + cur[-1]["t"] + cur[-1]["d"] + 0.15, " ".join(x["w"] for x in cur)])
                    cur = []
        off += float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                     str(od / c / "silent.mp4")], capture_output=True, text=True).stdout)
    for i in range(len(cues) - 1):
        cues[i][1] = min(cues[i][1], cues[i + 1][0] - 0.02)
    out = "\n".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(cues))
    (od / "captions.vi.srt").write_text(out, encoding="utf-8")
    print(len(cues), "cue,", ts(cues[-1][1]))


if __name__ == "__main__":
    main(sys.argv[1])
