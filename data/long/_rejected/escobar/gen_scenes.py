"""Đổ script.md -> chNN.json. Không đụng topic khác.

    python data/long/escobar/gen_scenes.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "motion" / "long"))
import anchors
import craft
import scenes_from
import script_lines

TOPIC = "escobar"
SD = ROOT / "data" / "long" / TOPIC
MOODS = ["mystery", "dark", "tense", "quiet", "sad", "epic", "mystery", "tense", "dark", "quiet", "sad"]
HUD = [
    "SÔNG MAGDALENA · 2026",
    "RIONEGRO · 1949",
    "MEDELLÍN · 1976",
    "HACIENDA NÁPOLES",
    "QUỐC HỘI · 1982",
    "LA CATEDRAL",
    "PEPE · 2009",
    "GONACON · 2021",
    "NGOÀI HÀNG RÀO",
    "QUỐC HỘI · 2026",
    "ĐẢO IM LẶNG",
]


def main():
    chs = script_lines.parse((SD / "script.md").read_text(encoding="utf-8"))
    bad = craft.audio_problems(chs)
    if bad:
        raise SystemExit("audio:\n  " + "\n  ".join(bad))
    for n, ch in enumerate(chs):
        scenes = scenes_from.scenes_from(ch["lines"], ch["marks"])
        for s, line in zip(scenes, ch["lines"]):
            t = line if isinstance(line, str) else line["t"]
            if t.startswith("Đây là hồ sơ"):
                at = s["at"]
                s.clear()
                s.update({"type": "brand", "at": at, "sub": "HỒ SƠ · PABLO ESCOBAR"})
        err = anchors.check(ch["lines"], scenes) + craft.graphic_problems(ch["name"], scenes)
        if err:
            raise SystemExit(ch["name"] + ":\n  " + "\n  ".join(err))
        plain = scenes_from.unmarked_count(ch["lines"], ch["marks"])
        out = {
            "title": ch["title"],
            "lines": ch["lines"],
            "hud": {"k": "HỒ SƠ", "t": HUD[n]},
            "bgm": {"mood": MOODS[n], "gain": 0.11},
            "scenes": scenes,
        }
        (SD / f"{ch['name']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        words = sum(len((x if isinstance(x, str) else x["t"]).split()) for x in ch["lines"])
        print(f"{ch['name']}: {len(ch['lines'])} câu, {words} từ, {plain} câu không dấu, {len(scenes)} cảnh")
    total = sum(len((x if isinstance(x, str) else x["t"]).split()) for c in chs for x in c["lines"])
    print(f"TỔNG {total} từ, ~{total / 220:.1f} phút nếu đọc 220 từ/phút")


if __name__ == "__main__":
    main()
