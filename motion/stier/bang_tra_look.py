"""Xoay giao diện Short bảng tra (8 look: 4 MIM + 4 CK), không dùng cùng look hai bài liền nhau của một kênh.

  python motion/stier/bang_tra_look.py next MIM|CK        in look nên dùng (ít dùng gần nhất, khác bài liền trước)
  python motion/stier/bang_tra_look.py apply <slug> [look]  ghi spec: profile/look/cls/extra_css + ghi sổ (không đổi nội dung)
  python motion/stier/bang_tra_look.py check              kiểm sổ: không trùng liền kề trong kênh, spec khớp sổ
Sổ: data/stier/bang_tra_looks.json. Nạp CSS+JS: build.py chỉ có extra_css, nên spec.extra_css chèn thêm thẻ <script>
(tạm; đề xuất thêm spec.extra_js vào build.py -- xem docs/pm/2026-10-22-bang-tra-looks.md).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "data" / "stier" / "bang_tra_looks.json"
SPECS = ROOT / "data" / "stier" / "specs"
EXTRA = 'bang-tra-looks.css" /><script src="assets/engine/bang-tra-looks.js"></script><link rel="x-end" href="x'


def load():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def pick(led, channel):
    names = [k for k, v in led["looks"].items() if v["channel"] == channel]
    hist = [p["look"] for p in led["picks"] if p["channel"] == channel]
    last = hist[-1] if hist else None
    # ít dùng nhất; hoà thì look dùng cách đây lâu nhất; không bao giờ trùng bài liền trước
    def key(n):
        return (hist.count(n), hist.index(n) if n in hist else -1)
    return sorted((n for n in names if n != last), key=key)[0]


def apply(slug, look=None):
    led = load()
    sp = SPECS / f"{slug}.json"
    spec = json.loads(sp.read_text(encoding="utf-8"))
    ch = "MIM" if spec.get("theme") == "mim" else "CK"
    look = look or spec.get("look") or pick(led, ch)
    if look not in led["looks"] or led["looks"][look]["channel"] != ch:
        raise SystemExit(f"look {look} không hợp kênh {ch}")
    hist = [p for p in led["picks"] if p["channel"] == ch and p["slug"] != slug]
    if hist and hist[-1]["look"] == look:
        raise SystemExit(f"{slug}: look {look} trùng bài liền trước của {ch} ({hist[-1]['slug']})")
    spec.update({"profile": "bang-tra", "look": look, "cls": f"btl btl-{look}", "extra_css": EXTRA})
    spec.pop("bt4", None)
    sp.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    led["picks"] = [p for p in led["picks"] if p["slug"] != slug] + [{"channel": ch, "slug": slug, "look": look}]
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{slug}: {look}")


def check():
    led = load(); bad = 0
    for ch in ("MIM", "CK"):
        seq = [p for p in led["picks"] if p["channel"] == ch]
        for a, b in zip(seq, seq[1:]):
            if a["look"] == b["look"]:
                print(f"TRÙNG {ch}: {a['slug']} -> {b['slug']} ({a['look']})"); bad += 1
    for p in led["picks"]:
        f = SPECS / f"{p['slug']}.json"
        if f.exists() and json.loads(f.read_text(encoding="utf-8")).get("look") != p["look"]:
            print(f"LỆCH sổ/spec: {p['slug']}"); bad += 1
    print("OK" if not bad else f"{bad} lỗi")
    return bad


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["next"]:
        print(pick(load(), a[1].upper()))
    elif a[:1] == ["apply"]:
        apply(a[1], a[2] if len(a) > 2 else None)
    elif a[:1] == ["check"]:
        sys.exit(1 if check() else 0)
    else:
        print(__doc__)
