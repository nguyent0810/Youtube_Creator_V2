"""Tờ soát clip Pexels của một video dài: mỗi clip 3 khung (đầu · giữa · cuối đoạn được dùng), để soát logo hãng,
mã cổ phiếu, tên công ty, chữ trên màn hình TRƯỚC khi render (retro 15/10/2026: B4 lộ logo hãng xe, C5 lộ mã cổ phiếu,
D3 lộ cặp BTC/USDT -- contact sheet sau render 10 giây/khung bỏ sót chapter card).

    python motion/long/clip_sheet.py <topic>      # -> output/long/<topic>/qa_clips.jpg
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main(topic):
    data, out = ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic
    uses = {}
    for f in sorted(data.glob("ch[0-9][0-9].json")):
        for s in json.loads(f.read_text(encoding="utf-8")).get("scenes", []):
            if s.get("vid"):
                uses.setdefault(str(s["vid"]), []).append((f.stem, float(s.get("ms", 0))))
    if not uses:
        raise SystemExit(f"{topic}: không có clip nào trong ch*.json")
    tmp = out / "qa_clips"
    tmp.mkdir(parents=True, exist_ok=True)
    rows = []
    for vid, where in uses.items():
        src = out / "broll" / f"{vid}.mp4"
        if not src.exists():
            raise SystemExit(f"thiếu {src} -- chạy pexels.py get {topic} {vid}")
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                                   capture_output=True, text=True).stdout or 0)
        ms = min(m for _, m in where)
        cells = []
        for k, t in enumerate((ms + 0.5, (ms + dur) / 2, max(ms, dur - 1))):
            p = tmp / f"{vid}_{k}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(src), "-vf", "scale=640:360,setsar=1",
                            "-frames:v", "1", str(p)], check=True)
            cells.append(p)
        row = tmp / f"{vid}_row.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", str(c)] for c in cells), []), "-filter_complex", "hstack=3", str(row)], check=True)
        rows.append(row)
        print(f"{vid}: {dur:.1f}s  dùng ở {', '.join(f'{c}@{m:g}s' for c, m in where)}")
    sheet = out / "qa_clips.jpg"
    args = sum((["-i", str(r)] for r in rows), [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", f"vstack={len(rows)}" if len(rows) > 1 else "null", str(sheet)], check=True)
    print(f"{sheet}  ({len(rows)} clip, thứ tự như trên) -- soát logo / mã cổ phiếu / tên công ty / chữ đọc được")


if __name__ == "__main__":
    main(sys.argv[1])
