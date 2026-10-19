"""Soát mốc neo của mọi cảnh TRƯỚC khi có giọng đọc: dựng giờ giả (0,27 s/từ) rồi chạy plan().

    python motion/long/dryplan.py <topic>
Bắt được: chữ neo không có trong câu, cảnh quá ngắn, khóa cảnh sai. Chạy sau mỗi lần sửa gen_scenes.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_long as B  # noqa: E402
import floor  # noqa: E402


def main(topic):
    spec, chs, _ = B.load(topic)
    bad = 0
    for name, ch in chs:
        lines, t = [], 0.0
        for ln in ch["lines"]:
            txt = ln["t"] if isinstance(ln, dict) else ln
            ws = []
            for w in txt.split():
                ws.append({"w": w, "t": round(t, 3), "d": 0.25})
                t += 0.27
            lines.append({"text": txt, "start": ws[0]["t"], "end": t, "words": ws})
            t += 0.6
        try:
            B.plan(ch, lines, t + 1)
            print(name, "ok", round(t), "s")
        except Exception as e:
            bad += 1
            print(name, "LỖI", e)
    print("floor:", floor.report(chs))
    for x in floor.problems(chs):
        print("  ! floor:", x)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1])
