"""Kịch bản đã duyệt (data/long/<topic>/script.md) -> "lines" của từng chNN.json (giữ nguyên mọi khoá khác: hud, bgm, scenes…).

    python motion/long/script_lines.py <topic>

Quy ước script.md: "## CHnn · Tên chương"; mỗi dòng một câu; "‖" cuối dòng = nghỉ dài; "**[DIỄN Ý]**" = trích diễn ý; "[TRÍCH DỊCH]" = văn bản thật đã dịch;
"»" = phần sau là LỜI TRÍCH (đọc giọng trích, xem build_long.QUOTE_VOICE). Dòng "a: » b" tách thành 2 câu.
Dừng ở "## Ghi chú". Câu -> chuỗi, hoặc {"t", "p": nghỉ, "q": 1 (lời trích), "diy": 1}.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LONG_PAUSE = 1.0


def parse(md: str):
    chs, cur = [], None
    for raw in md.split("\n"):
        s = raw.strip()
        if s.startswith("## Ghi chú"):
            break
        m = re.match(r"^## (CH\d\d) · (.+)$", s)
        if m:
            cur = {"name": m.group(1).lower(), "title": m.group(2), "lines": []}
            chs.append(cur)
            continue
        if not cur or not s or s == "---" or s.startswith("#"):
            continue
        diy = "**[DIỄN Ý]**" in s
        tr = "[TRÍCH DỊCH]" in s            # văn bản thật dịch sang tiếng Việt (nhãn TRÍCH DỊCH trên cảnh quote)
        s = s.replace("**[DIỄN Ý]**", "").replace("[TRÍCH DỊCH]", "").strip()
        pause = s.endswith("‖")
        s = s.rstrip("‖").strip()
        parts = [p.strip() for p in s.split("»")]
        out = []
        if len(parts) == 2:
            if parts[0]:
                out.append({"t": parts[0]})
            q = parts[1][:1].upper() + parts[1][1:]
            out.append({"t": q, "q": 1, **({"diy": 1} if diy else {}), **({"tr": 1} if tr else {})})
        else:
            out.append({"t": s, **({"diy": 1} if diy else {})})
        if pause:
            out[-1]["p"] = LONG_PAUSE
        cur["lines"] += out
    for c in chs:
        x0 = c["lines"][0]
        if c["name"] != "ch00" and set(x0) == {"t"}:     # "Chương N. Tên." -> nghỉ để màn tên chương thở
            x0["p"] = 0.8
        c["lines"] = [x["t"] if set(x) == {"t"} else x for x in c["lines"]]
    return chs


if __name__ == "__main__":
    topic = sys.argv[1]
    sd = ROOT / "data" / "long" / topic
    chs = parse((sd / "script.md").read_text(encoding="utf-8"))
    tot = 0
    for c in chs:
        f = sd / f"{c['name']}.json"
        d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
        d["title"] = c["title"]
        d["lines"] = c["lines"]
        d.setdefault("scenes", [])
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        syl = sum(len((x if isinstance(x, str) else x["t"]).split()) for x in c["lines"])
        tot += syl
        print(f"{c['name']}: {len(c['lines'])} câu, {syl} âm tiết, ~{syl / 200:.1f} phút  {c['title']}")
    print(f"TỔNG {sum(len(c['lines']) for c in chs)} câu, {tot} âm tiết")
