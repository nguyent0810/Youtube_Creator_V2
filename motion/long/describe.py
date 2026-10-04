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
            for k in (s.get("img"), s.get("bg"), (s.get("a") or {}).get("img"), (s.get("b") or {}).get("img"), *[q.get("img") for q in s.get("pins") or []]):
                if k:
                    used.add(k)
        bg = ch.get("bgm") or []
        for b in [q.get("file") for q in ([bg] if isinstance(bg, dict) else bg)]:
            if b and b not in music:
                music.append(b)
        title = ch["hud"]["t"].title() if c != "ch00" else meta.get("ch00_title", "Mở đầu")
        if c == spec["chapters"][-1]:
            title = "Kết: " + title
        chapters.append(f"{int(t // 60):02d}:{int(t % 60):02d} {title}")
        t += json.loads((od / c / "timing.json").read_text(encoding="utf-8"))["duration"]
    lines = [meta.get("summary", ""), "", *meta.get("more", []), "", "⏱ CHƯƠNG", *chapters, "", "📚 NGUỒN THAM KHẢO (Wikipedia tiếng Anh và các nguồn được trích trong đó)",
             *meta.get("sources", [])[:8], "và các bài Wikipedia liên quan.", "",
             "Lời dẫn là bản viết mới dựa trên tư liệu công khai; những câu có nhãn DIỄN Ý là diễn đạt lại, không phải nguyên văn.",
             "Hình ảnh/video có nhãn MINH HỌA chỉ mang tính minh họa bối cảnh.", "", "🖼 ẢNH (Wikimedia Commons và các kho tư liệu mở)"]
    pd, bylic, pdsrc = 0, {}, set()
    INST = {"wellcome": "Wellcome Collection", "artic": "Art Institute of Chicago"}
    for k in sorted(used):
        f = spec["imgs"][k]
        mp = od / "img" / f"{k}.json"
        m = json.loads(mp.read_text(encoding="utf-8"))
        if m["license"].lower().startswith(("public", "pd", "cc0", "no restr")):
            pd += 1
            if m.get("source", "").split(":")[0] in INST:   # PD từ kho bảo tàng: vẫn ghi tên kho (lịch sự, không bắt buộc)
                pdsrc.add(INST[m["source"].split(":")[0]])
            continue
        by = re.sub(r"\s*\d\d:\d\d, .*UTC\)", "", m["artist"].split("\n")[0]).strip() or "không rõ tác giả"
        src = {"wellcome": " · Wellcome Collection", "artic": " · Art Institute of Chicago"}.get(m.get("source", "").split(":")[0], "")
        if m.get("source", "").startswith("europeana:"):
            src = " · " + m["source"].split(":", 1)[1]
        if m.get("source") == "sentinel2":                        # Copernicus: ghi đúng câu bắt buộc
            bylic.setdefault("Copernicus Sentinel data", []).append(m["artist"])
            continue
        name = re.sub(r"\s*\(\d{6,}\)|\.(jpe?g|png|tif)$|, Sicily, Italy| - panoramio", "", m.get("title") or f[5:], flags=re.I)[:meta.get("credit_name_len", 48)]
        by = re.sub(r"^The original uploader was |No machine-readable author provided\. ", "", by)
        bylic.setdefault(m["license"], []).append(f"{name.strip()} ({by[:meta.get('credit_by_len', 40)].strip()}{src})")
    if not any(str(spec["imgs"][k]).startswith("EXT:") for k in used):   # chỉ Commons -> giữ tiêu đề cũ
        lines = [x.replace("🖼 ẢNH (Wikimedia Commons và các kho tư liệu mở)", "🖼 ẢNH (Wikimedia Commons)") for x in lines]
    lines += [f"• {lic}: " + "; ".join(v) for lic, v in sorted(bylic.items())]   # gom theo giấy phép: đủ tác giả + giấy phép, ít byte hơn
    lines += [f"• Và {pd} ảnh tư liệu thuộc phạm vi công cộng (Public domain / CC0)" + (f", gồm ảnh từ {', '.join(sorted(pdsrc))}." if pdsrc else "."), "",
              "🎬 VIDEO B-ROLL: Pexels (pexels.com) — giấy phép Pexels, dùng tự do.", "", "🎵 NHẠC NỀN"]
    mac = [b for b in music if b in MUSIC]
    if mac:
        lines.append(", ".join(f"\"{MUSIC[b]}\"" for b in mac) + " by Kevin MacLeod (incompetech.com)")
        lines.append("Licensed under Creative Commons: By Attribution 4.0 License — http://creativecommons.org/licenses/by/4.0/")
    for b in music:   # bản thu tự do từ Commons: ghi tên file + giấy phép (json cạnh file nhạc)
        mj = od / "bgm" / (Path(b).stem + ".json")
        if b not in MUSIC and mj.exists():
            m = json.loads(mj.read_text(encoding="utf-8"))
            name = re.sub(r"\.(flac|ogg|oga|wav|mp3)$", "", m["file"][5:], flags=re.I)
            lines.append(f"Mascagni — Intermezzo (Cavalleria rusticana) · {m.get('short', name[:40])} — Wikimedia Commons — {m['license']}")
    lines += ["", " ".join("#" + x for x in meta.get("hashtags", []))]
    (od / "description.txt").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print((od / "description.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main(sys.argv[1])
