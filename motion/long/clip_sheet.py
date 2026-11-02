"""Tờ soát clip Pexels và dấu xác nhận QA của một video dài.

    python motion/long/clip_sheet.py <topic>        # -> qa_clips.jpg
    python motion/long/clip_sheet.py <topic> --ok   # sau khi đã xem tờ
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from factory.console import utf8_console

ROOT = Path(__file__).resolve().parents[2]


def clip_uses(data: Path) -> list[dict]:
    """Danh sách tối thiểu quyết định nội dung tờ clip, theo thứ tự ổn định."""
    uses = []
    for f in sorted(data.glob("ch[0-9][0-9].json")):
        scenes = json.loads(f.read_text(encoding="utf-8")).get("scenes", [])
        for scene in scenes:
            if scene.get("vid") is not None:
                uses.append({"id": str(scene["vid"]), "ms": float(scene.get("ms", 0))})
    return sorted(uses, key=lambda x: (x["id"], x["ms"]))


def uses_hash(uses: list[dict]) -> str:
    raw = json.dumps(uses, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def ok_path(out: Path) -> Path:
    return out / "qa_clips.ok"


def mark_ok(topic: str, data: Path | None = None, out: Path | None = None) -> Path:
    data = data or ROOT / "data" / "long" / topic
    out = out or ROOT / "output" / "long" / topic
    if not clip_uses(data):
        raise SystemExit(f"{topic}: không có clip nào, không cần qa_clips.ok")
    sheet = out / "qa_clips.jpg"
    if not sheet.exists():
        raise SystemExit(f"thiếu {sheet} -- chạy python motion/long/clip_sheet.py {topic}, xem tờ rồi mới thêm --ok")
    path = ok_path(out)
    path.write_text(uses_hash(clip_uses(data)) + "\n", encoding="utf-8")
    print(f"{path}  (đã ghi dấu sau khi soát)")
    return path


def render_sheet(topic: str, data: Path | None = None, out: Path | None = None) -> Path:
    data = data or ROOT / "data" / "long" / topic
    out = out or ROOT / "output" / "long" / topic
    uses = clip_uses(data)
    if not uses:
        raise SystemExit(f"{topic}: không có clip nào trong ch*.json")
    by_video: dict[str, list[float]] = {}
    for item in uses:
        by_video.setdefault(item["id"], []).append(item["ms"])
    tmp = out / "qa_clips"
    tmp.mkdir(parents=True, exist_ok=True)
    rows = []
    for vid, starts in by_video.items():
        src = out / "broll" / f"{vid}.mp4"
        if not src.exists():
            raise SystemExit(f"thiếu {src} -- chạy pexels.py get {topic} {vid}")
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                                   capture_output=True, text=True).stdout or 0)
        ms = min(starts)
        cells = []
        for k, t in enumerate((ms + 0.5, (ms + dur) / 2, max(ms, dur - 1))):
            p = tmp / f"{vid}_{k}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(src), "-vf", "scale=640:360,setsar=1",
                            "-frames:v", "1", str(p)], check=True)
            cells.append(p)
        row = tmp / f"{vid}_row.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum((["-i", str(c)] for c in cells), []), "-filter_complex", "hstack=3", str(row)], check=True)
        rows.append(row)
        print(f"{vid}: {dur:.1f}s  dùng ở {', '.join(f'{m:g}s' for m in starts)}")
    sheet = out / "qa_clips.jpg"
    args = sum((["-i", str(r)] for r in rows), [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", f"vstack={len(rows)}" if len(rows) > 1 else "null", str(sheet)], check=True)
    print(f"{sheet}  ({len(rows)} clip, thứ tự như trên) -- soát logo / mã cổ phiếu / tên công ty / chữ đọc được")
    return sheet


def main(argv=None):
    utf8_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic")
    parser.add_argument("--ok", action="store_true", help="ghi dấu sau khi đã xem tờ soát")
    args = parser.parse_args(argv)
    if args.ok:
        mark_ok(args.topic)
    else:
        render_sheet(args.topic)


if __name__ == "__main__":
    main()
