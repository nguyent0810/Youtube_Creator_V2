"""python data/long/capone/gen_scenes.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "motion" / "long"))
import anchors
import craft
import scenes_from
import script_lines

TOPIC = "capone"
SD = ROOT / "data" / "long" / TOPIC
MOODS = ["mystery", "dark", "tense", "quiet", "sad", "epic", "tense", "mystery", "dark", "quiet"]
HUD = [
    "CHICAGO · 1929",
    "BROOKLYN · 1899",
    "VẾT SẸO",
    "HAI SÁU TUỔI",
    "RICHARD HART",
    "CỬA HÀNG HOA",
    "14.02.1929",
    "17.10.1931",
    "PHÒNG 181",
    "TỜ KHAI",
]


def break_runs(scenes):
    """Cắt một chuỗi kinetic trước khi nó đủ sáu, bằng chính cụm chữ của câu đó."""
    run = 1
    for i in range(1, len(scenes)):
        same = scenes[i].get("type") == scenes[i - 1].get("type") == "kinetic"
        run = run + 1 if same else 1
        if run == 5:
            phrase = scenes[i]["items"][0]["text"]
            at = scenes[i]["at"]
            scenes[i].clear()
            scenes[i].update({"type": "slam", "at": at, "text": phrase, "white": True})
            run = 1


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
                s.update({"type": "brand", "at": at, "sub": "HỒ SƠ · AL CAPONE"})
        break_runs(scenes)
        err = anchors.check(ch["lines"], scenes) + craft.graphic_problems(ch["name"], scenes)
        if err:
            raise SystemExit(ch["name"] + ":\n  " + "\n  ".join(err))
        out = {
            "title": ch["title"],
            "lines": ch["lines"],
            "hud": {"k": "HỒ SƠ", "t": HUD[n]},
            "bgm": {"mood": MOODS[n], "gain": 0.11},
            "scenes": scenes,
        }
        (SD / f"{ch['name']}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        words = sum(len((x if isinstance(x, str) else x["t"]).split()) for x in ch["lines"])
        print(f"{ch['name']}: {words} từ")
    total = sum(len((x if isinstance(x, str) else x["t"]).split()) for c in chs for x in c["lines"])
    print(f"TỔNG {total} từ, ~{total / 220:.1f} phút")


if __name__ == "__main__":
    main()
