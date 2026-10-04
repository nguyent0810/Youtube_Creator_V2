"""Độ đa dạng giữa các video của một kênh — chống bị coi là "mass-produced / repetitive".

Chính sách Spam của YouTube nêu đích danh ví dụ: kênh dùng "the exact same background music and repetitive
AI generated imagery across many videos" (motion/long/RESEARCH-million-views.md §2). Module này giữ cho mỗi
video dài khác các video trước về NHẠC NỀN và DIỆN MẠO (bảng màu + cặp font), và kiểm tra trước khi dựng.

  python motion/variety.py audit <topic>     so với 3 video gần nhất cùng kênh trong sổ (thoát 1 nếu quá giống)
  python motion/variety.py record <topic>    ghi video vào sổ (publish_long.py gọi sau khi upload)
  python motion/variety.py next-look [CH]    gợi ý look ít dùng gần đây nhất
  python motion/variety.py library           kho nhạc: số lần mỗi bài đã dùng trong sổ

Sổ: data/variety/ledger.json (commit). Danh mục nhạc + mood: motion/long/music_catalog.json (commit).
File nhạc: output/music/ (không commit; tải về theo danh mục).
Trong chNN.json, bgm có thể ghi {"mood": "tense", "gain": .., "at": ..} thay vì "file": build_long chọn bài
qua resolve_bgm() — ít dùng nhất trong các video gần đây, không lặp trong cùng video — và cache vào
output/long/<topic>/bgm_picks.json để render lại vẫn ra đúng bài cũ.
"""
import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "variety" / "ledger.json"
CATALOG = ROOT / "motion" / "long" / "music_catalog.json"
LIB = ROOT / "output" / "music"
WINDOW = 3            # so với bao nhiêu video gần nhất cùng kênh
MAX_BGM_OVERLAP = 0.35  # Jaccard bộ nhạc nền giữa hai video

# Diện mạo: chỉ font có bộ ký tự tiếng Việt trên Google Fonts (đã kiểm 04/10/2026).
# "classic" = diện mạo của mọi video trước ngày có module này (spec không ghi look -> classic, render y như cũ).
LOOKS = {
    "classic": {"serif": ("Playfair Display", "0,700;0,900;1,700"), "sans": ("Be Vietnam Pro", "0,400;0,600;0,700;0,800;0,900;1,600"),
                "vars": {}},
    "amber": {"serif": ("Literata", "0,700;0,900;1,700"), "sans": ("Montserrat", "0,400;0,600;0,700;0,800;0,900;1,600"),
              "vars": {"--red": "#e39a2d", "--gold": "#f2cf86", "--paper": "#f2e7cf", "--bed1": "#1d150c", "--bed2": "#0c0905"}},
    "steel": {"serif": ("Noto Serif Display", "0,700;0,900;1,700"), "sans": ("Inter", "0,400;0,600;0,700;0,800;0,900;1,600"),
              "vars": {"--red": "#3d9ad6", "--gold": "#bcd0dc", "--paper": "#e8ecef", "--ink": "#121619", "--bed1": "#0f151b", "--bed2": "#07090c"}},
    "jade": {"serif": ("Source Serif 4", "0,700;0,900;1,700"), "sans": ("Barlow Condensed", "0,400;0,600;0,700;0,800;0,900;1,600"),
             "vars": {"--red": "#2fb489", "--gold": "#d6c07a", "--paper": "#ebe5d0", "--bed1": "#0e1713", "--bed2": "#060a08"}},
    "rose": {"serif": ("Spectral", "0,700;0,800;1,700"), "sans": ("Archivo", "0,400;0,600;0,700;0,800;0,900;1,600"),
             "vars": {"--red": "#c9457d", "--gold": "#e7c58f", "--paper": "#efe3d6", "--bed1": "#170d12", "--bed2": "#09060a"}},
    "sulfur": {"serif": ("Noto Serif", "0,700;0,900;1,700"), "sans": ("Roboto Condensed", "0,400;0,600;0,700;0,800;0,900;1,600"),
               "vars": {"--red": "#e2c534", "--gold": "#f0e2a0", "--paper": "#efe8cf", "--bed1": "#15140b", "--bed2": "#090905"}},
}


def look(name: str | None) -> dict:
    """Look cho data.js (casewide.js đọc C.look) + URL Google Fonts."""
    L = LOOKS[name or "classic"]
    v = dict(L["vars"])
    v["--serif"] = f"'{L['serif'][0]}'"
    v["--sans"] = f"'{L['sans'][0]}'"
    return {"name": name or "classic", "vars": v}


def fonts_url(name: str | None) -> str:
    L = LOOKS[name or "classic"]
    fam = [f"family={L['sans'][0].replace(' ', '+')}:ital,wght@{L['sans'][1]}",
           f"family={L['serif'][0].replace(' ', '+')}:ital,wght@{L['serif'][1]}",
           "family=JetBrains+Mono:wght@500;700", "family=Noto+Serif+SC:wght@900"]
    return "https://fonts.googleapis.com/css2?" + "&".join(fam) + "&display=swap"


# ---------------- sổ ----------------
def ledger() -> list[dict]:
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else []


def save_ledger(rows: list[dict]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")


def catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def _chapters(topic: str):
    d = ROOT / "data" / "long" / topic
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8"))
    return spec, [(n, json.loads((d / f"{n}.json").read_text(encoding="utf-8"))) for n in spec["chapters"]]


def _bgm_files(topic: str, chs) -> set[str]:
    picks = _picks(topic)
    out = set()
    for name, ch in chs:
        b = ch.get("bgm") or []
        for k, q in enumerate([b] if isinstance(b, dict) else b):
            f = q.get("file") or picks.get(f"{name}.{k}")
            if f:
                out.add(Path(f).stem)
    return out


def profile(topic: str) -> dict:
    spec, chs = _chapters(topic)
    return {"topic": topic, "channel": spec.get("channel", "CL"), "theme": spec.get("theme") or "", "look": spec.get("look") or "classic",
            "bgm": sorted(_bgm_files(topic, chs))}


def recent(channel: str, exclude: str, n: int = WINDOW) -> list[dict]:
    rows = [r for r in ledger() if r["channel"] == channel and r["topic"] != exclude]
    return sorted(rows, key=lambda r: r.get("date", ""))[-n:]


# ---------------- nhạc nền theo mood ----------------
def _picks_path(topic: str) -> Path:
    return ROOT / "output" / "long" / topic / "bgm_picks.json"


def _picks(topic: str) -> dict:
    p = _picks_path(topic)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def resolve_bgm(topic: str, spec: dict, chs, od: Path) -> None:
    """Điền "file" cho mọi đoạn bgm chỉ có "mood". Tất định + cache: chọn một lần, render lại vẫn giữ."""
    picks, cat = _picks(topic), None
    used_recent = {}
    for r in recent(spec.get("channel", "CL"), topic, WINDOW):
        for f in r["bgm"]:
            used_recent[f] = used_recent.get(f, 0) + 1
    in_video = {Path(q["file"]).stem for _, ch in chs for q in _items(ch) if q.get("file")}
    changed = False
    for name, ch in chs:
        for k, q in enumerate(_items(ch)):
            if q.get("file") or not q.get("mood"):
                continue
            key = f"{name}.{k}"
            if key not in picks:
                cat = cat or catalog()
                cands = [t for t, m in cat["tracks"].items() if q["mood"] in m["mood"] and (LIB / m["file"]).exists()]
                if not cands:
                    raise SystemExit(f"variety: không có bài nào mood '{q['mood']}' trong {LIB} ({name})")
                h = lambda t: int(hashlib.md5(f"{topic}|{key}|{t}".encode()).hexdigest()[:8], 16)
                best = min(cands, key=lambda t: (t in in_video, used_recent.get(t, 0), h(t)))
                picks[key] = cat["tracks"][best]["file"]
                changed = True
            q["file"] = picks[key]
            in_video.add(Path(q["file"]).stem)
            dst = od / "bgm" / q["file"]
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(LIB / q["file"], dst)
    if changed:
        _picks_path(topic).write_text(json.dumps(picks, indent=1), encoding="utf-8")


def _items(ch: dict) -> list[dict]:
    b = ch.get("bgm") or []
    return [b] if isinstance(b, dict) else b


# ---------------- kiểm tra ----------------
def audit(topic: str) -> list[str]:
    me = profile(topic)
    problems = []
    prev = recent(me["channel"], topic)
    for r in prev:
        a, b = set(me["bgm"]), set(r["bgm"])
        j = len(a & b) / max(1, len(a | b))
        if j > MAX_BGM_OVERLAP:
            problems.append(f"nhạc nền trùng {j:.0%} với '{r['topic']}' ({len(a & b)}/{len(a | b)} bài) — ngưỡng {MAX_BGM_OVERLAP:.0%}")
    if prev and prev[-1]["look"] == me["look"]:
        problems.append(f"look '{me['look']}' giống video ngay trước ('{prev[-1]['topic']}') — đổi \"look\" trong spec (gợi ý: {next_look(me['channel'], topic)})")
    return problems


def next_look(channel: str = "CL", exclude: str = "") -> str:
    rows = [r for r in ledger() if r["channel"] == channel and r["topic"] != exclude]
    last = {}
    for i, r in enumerate(sorted(rows, key=lambda r: r.get("date", ""))):
        last[r["look"]] = i
    return min(LOOKS, key=lambda k: (last.get(k, -1), k))


def record(topic: str, when: str | None = None) -> dict:
    row = {**profile(topic), "date": when or date.today().isoformat()}
    rows = [r for r in ledger() if r["topic"] != topic] + [row]
    save_ledger(rows)
    return row


def main():
    cmd, *rest = sys.argv[1:] or ["help"]
    if cmd == "audit":
        p = audit(rest[0])
        print(json.dumps(profile(rest[0]), ensure_ascii=False))
        for x in p:
            print("  !", x)
        print("OK: đủ khác các video gần đây" if not p else f"{len(p)} vấn đề")
        sys.exit(1 if p else 0)
    elif cmd == "record":
        print(record(rest[0], rest[1] if len(rest) > 1 else None))
    elif cmd == "next-look":
        print(next_look(rest[0] if rest else "CL"))
    elif cmd == "library":
        cat, uses = catalog(), {}
        for r in ledger():
            for f in r["bgm"]:
                uses[f] = uses.get(f, 0) + 1
        for t, m in sorted(cat["tracks"].items(), key=lambda x: uses.get(x[0], 0)):
            have = "✓" if (LIB / m["file"]).exists() else "thiếu"
            print(f"{uses.get(t, 0):3d} lần  {have:5s} {t:28s} {','.join(m['mood'])}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
