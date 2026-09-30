"""Mô tả YouTube cho video dài: tóm tắt + mốc chương (tính từ timing thật) + nguồn + ghi công ảnh/nhạc/video.

    python motion/long/describe.py <topic>   -> output/long/<topic>/description.txt
Chỉ ghi công ảnh THỰC SỰ xuất hiện trong cảnh (không phải mọi ảnh đã tải).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUSIC = {  # file -> tên gốc trên incompetech (Kevin MacLeod, CC BY 4.0)
    "oppressive_gloom.mp3": "Oppressive Gloom", "ossuary_6_air.mp3": "Ossuary 6 - Air", "echoes_of_time_v2.mp3": "Echoes of Time v2",
    "darkest_child.mp3": "Darkest Child", "gathering_darkness.mp3": "Gathering Darkness", "lightless_dawn.mp3": "Lightless Dawn",
    "dark_times.mp3": "Dark Times", "crypto.mp3": "Crypto", "heart_of_nowhere.mp3": "Heart of Nowhere", "deep_haze.mp3": "Deep Haze",
    "long_note_four.mp3": "Long Note Four", "despair_and_triumph.mp3": "Despair and Triumph", "night_cave.mp3": "Night Cave",
    "impact_lento.mp3": "Impact Lento"}


def main(topic):
    sd, od = ROOT / "data" / "long" / topic, ROOT / "output" / "long" / topic
    spec = json.loads((sd / "spec.json").read_text(encoding="utf-8"))
    meta = spec.get("youtube", {})
    used, music, chapters, t = set(), [], [], 0.0
    for c in spec["chapters"]:
        ch = json.loads((sd / f"{c}.json").read_text(encoding="utf-8"))
        for s in ch["scenes"]:
            for k in (s.get("img"), s.get("bg"), (s.get("a") or {}).get("img"), (s.get("b") or {}).get("img")):
                if k:
                    used.add(k)
        b = (ch.get("bgm") or {}).get("file")
        if b and b not in music:
            music.append(b)
        title = ch["hud"]["t"].title() if c != "ch00" else "Mở đầu: Kobe, 5 giờ 46 phút"
        chapters.append(f"{int(t // 60):02d}:{int(t % 60):02d} {title}")
        t += json.loads((od / c / "timing.json").read_text(encoding="utf-8"))["duration"]
    lines = [meta.get("summary", ""), "", "⏱ CHƯƠNG", *chapters, "", "📚 NGUỒN THAM KHẢO (Wikipedia tiếng Anh và các nguồn được trích trong đó)",
             *meta.get("sources", []), "",
             "Lời dẫn là bản viết mới dựa trên tư liệu công khai; những câu có nhãn DIỄN Ý là diễn đạt lại, không phải nguyên văn.",
             "Hình ảnh/video có nhãn MINH HỌA chỉ mang tính minh họa bối cảnh.", "", "🖼 ẢNH (Wikimedia Commons)"]
    pd = 0
    for k in sorted(used):
        f = spec["imgs"][k]
        mp = od / "img" / f"{k}.json"
        m = json.loads(mp.read_text(encoding="utf-8"))
        if m["license"].lower().startswith(("public", "pd", "cc0", "no restr")):
            pd += 1
            continue
        by = re.sub(r"\s*\d\d:\d\d, .*UTC\)", "", m["artist"].split("\n")[0]).strip() or "không rõ tác giả"
        lines.append(f"• {f[5:]} — {by} — {m['license']}")
    lines += [f"• Và {pd} ảnh tư liệu thuộc phạm vi công cộng (Public domain / CC0).", "",
              "🎬 VIDEO B-ROLL: Pexels (pexels.com) — giấy phép Pexels, dùng tự do.", "", "🎵 NHẠC NỀN"]
    for b in music:
        n = MUSIC.get(b, b)
        lines.append(f"\"{n}\" by Kevin MacLeod (incompetech.com) — Licensed under Creative Commons: By Attribution 4.0 License — http://creativecommons.org/licenses/by/4.0/")
    lines += ["", " ".join("#" + x for x in meta.get("hashtags", []))]
    (od / "description.txt").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print((od / "description.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main(sys.argv[1])
