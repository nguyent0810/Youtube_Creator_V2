"""Gallery chữ có dấu khó: mọi hiệu ứng chữ × theme "lab" (MIM) và "chart" (CK) -> ảnh tĩnh để soát MẤT DẤU.

    python motion/long/diacritics_gallery.py                 # chỉ dựng data.js + composition (không render)
    python motion/long/diacritics_gallery.py render [lab|chart]
        -> output/long/_diacritics_<theme>/{gallery.mp4, stills/NN_<cảnh>.png, sheet.png}

VÌ SAO (retro 2 mục 4, lặp retro 1 "lockup brand bị cắt dấu" = LỖI QUY TRÌNH): clip-path / mask / overflow của hiệu ứng chữ
cắt dấu chồng tiếng Việt (LẦN -> LÂN, TIỆM mất dấu) — chỉ lộ ra ở bản nháp, sau khi đã tốn render. Gallery này đặt chữ hoa
có dấu khó nhất (Ầ Ẫ Ỵ Ệ Ở Ữ Ặ: dấu trên + dấu dưới cùng lúc) qua MỌI hiệu ứng của beat.js (đọc thẳng danh sách BEAT/SLAM
trong file JS -> hiệu ứng mới tự có mặt) và mọi loại cảnh chữ, trên cả hai theme kênh.
CHẠY KHI: sửa motion/hf/assets/engine/* (beat.js/.css, casewide.*, lab.js, chart.js, theme-*.css) hoặc thêm theme/hiệu ứng.
Soát sheet.png: mọi ô phải đủ dấu, không chữ nào bị cắt nửa trên/dưới, không nhãn nào bị đè.
Render đi qua factory/render_lock.py (một render một lúc trên cả máy) — nếu đang có render khác, lệnh này XẾP HÀNG chờ.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "motion"), str(ROOT)]

ENGINE = ROOT / "motion" / "hf" / "assets" / "engine"
THEMES = {"lab": {"brand": "MIND IN THE MACHINE", "accent": "#22d3ee"},
          "chart": {"brand": "BIỂU ĐỒ BIẾT NÓI", "accent": "#fbbf24"}}
HARD = "Ầ Ẫ Ỵ Ệ Ở Ữ Ặ"
BIG = "LẦN TIỆM ẪN Ỵ Ở"            # dòng thường (chữ to)
ACC = "NGỮ ẦM Ặ ỆỞ"                # dòng nhấn (acc) — ngắn để hợp cả stamp/tape (có khung)
SM = "Ầ Ẫ Ỵ Ệ Ở Ữ Ặ · dấu khó"     # dòng nhỏ (sm)
STEP = 2.0                          # giây mỗi cảnh; ảnh tĩnh lấy ở t1 - HOLD (mọi animation đã xong)
HOLD = 0.25


def effects() -> tuple[list[str], list[str]]:
    """Tên hiệu ứng BEAT (dòng chữ) và SLAM (cú đập) đọc từ beat.js — nguồn sự thật, không chép tay."""
    js = (ENGINE / "beat.js").read_text(encoding="utf-8")

    def keys(name):
        body = js.split(f"const {name} = {{", 1)[1].split("\n  };", 1)[0]
        return re.findall(r"^    (\w+): \(", body, re.M)
    return keys("BEAT"), ["punch"] + keys("SLAM")     # "punch" = slam mặc định (không nằm trong bảng SLAM)


def _kin(fx: str, t0: float) -> dict:
    items = [{"text": BIG, "at": t0 + 0.2}, {"text": ACC, "acc": True, "at": t0 + 0.4}, {"text": SM, "sm": True, "at": t0 + 0.6}]
    for q in items:
        q["fx"] = fx
        if fx == "sync":       # sync cần mốc từng chữ
            q["wt"] = [round(q["at"] + 0.08 * k, 3) for k in range(len(q["text"].split()))]
    return {"type": "kinetic", "items": items}


def scenes() -> list[tuple[str, dict]]:
    beat_fx, slam_fx = effects()
    out = [(f"beat-{fx}", _kin(fx, 0)) for fx in beat_fx]
    out += [(f"slam-{fx}", {"type": "slam", "text": "LẦN ẪN\nỴ Ở Ữ Ặ", "fx": fx, "_at": 0.2}) for fx in slam_fx]
    out += [
        ("chapter", {"type": "chapter", "no": "4", "k": "CHƯƠNG BỐN", "title": "ẦM ẪM\nỶ Ỵ Ệ Ở", "sub": HARD}),
        ("quote-radio", {"type": "quote", "text": "Lần ấy, tiệm ẫm ỵ — giọng đọc thử dấu khó.", "by": "NGUỒN · " + HARD,
                         "lbl": "TRÍCH DỊCH", "radio": True, "tag": {"text": "GIỌNG MÁY TẠO"}}),
        ("quote-diy", {"type": "quote", "text": "ẦM ẪM Ỵ Ệ Ở Ữ Ặ", "dy": True, "by": "DIỄN Ý"}),
        ("ledger", {"type": "ledger", "title": "SỔ ẦM Ẫ Ỵ", "srcnote": "NGUỒN: " + HARD,
                    "rows": [{"k": "LẦN", "v": "TIỆM ẪN"}, {"k": "Ỵ Ở", "v": "Ữ Ặ Ệ"}], "total": {"k": "TỔNG", "v": HARD}}),
        ("bars", {"type": "bars", "title": "BIỂU ĐỒ ẦM Ẫ", "unit": "ĐƠN VỊ · " + HARD,
                  "items": [{"k": "LẦN", "v": 3, "lbl": "Ầ 3"}, {"k": "TIỆM", "v": 5, "lbl": "Ệ 5", "acc": True}, {"k": "Ở", "v": 2}]}),
        ("timeline", {"type": "timeline", "items": [{"year": "1770", "text": "*Lần* ẫn"}, {"year": "1939", "text": "Tiệm *ỵ*"},
                                                    {"year": "2026", "text": "Ở Ữ Ặ"}]}),
        ("counter", {"type": "counter", "from": 0, "to": 47, "suffix": "%", "label": "VIỆC LÀM ẦM Ẫ Ỵ", "_at": 0.2,
                     "sub": {"text": "NGUỒN · " + HARD}}),
        ("date", {"type": "date", "day": "THỨ HAI · ẦM Ẫ Ỵ Ệ Ở", "date": "09.03.2026"}),
        ("question", {"type": "question", "text": "Vậy LẦN NÀY\nai ẪN Ở ĐÂU?"}),
        ("brand", {"type": "brand", "sub": "ẦM ẪM · Ỵ Ệ Ở Ữ Ặ"}),
        ("endcard", {"type": "endcard"}),
    ]
    return out


def build_case(theme: str) -> dict:
    """data.js (window.CASE) của gallery cho một theme — thuần, không IO ngoài đọc beat.js (test dùng)."""
    sc, t = [], 0.0
    for label, s in scenes():
        s = json.loads(json.dumps(s))
        dt = STEP + (1.0 if s["type"] in ("chapter", "brand", "endcard", "quote") else 0.0)
        s.update(t0=round(t, 3), t1=round(t + dt, 3), gallery=label)     # KHÔNG dùng khoá "label" (counter/ảnh có label riêng)
        at = s.pop("_at", None)
        if at is not None:
            s["at"] = round(t + at, 3)
        if s["type"] == "kinetic":
            for q in s["items"]:
                q["at"] = round(q["at"] + t, 3)
                if "wt" in q:
                    q["wt"] = [round(w + t, 3) for w in q["wt"]]
        if s["type"] == "counter":
            s["until"] = round(s["at"] + 0.9, 3)
            s["sub"]["at"] = round(t + 0.6, 3)
        if s["type"] == "quote":
            s.update(at=round(t + 0.3, 3), typeDur=0.8, voiceAt=round(t + 0.3, 3), voiceEnd=round(t + 1.6, 3))
        if s["type"] == "ledger":
            for k, r in enumerate(s["rows"]):
                r["at"] = round(t + 0.3 + 0.2 * k, 3)
            s["total"]["at"] = round(t + 0.8, 3)
        if s["type"] in ("bars", "timeline"):
            for k, q in enumerate(s["items"]):
                q["at"] = round(t + 0.3 + 0.2 * k, 3)
        if s["type"] == "date":
            s.update(dayAt=round(t + 0.1, 3), groupAt=[round(t + 0.3 + 0.2 * g, 3) for g in range(3)])
        if s["type"] == "chapter":
            s["titleAt"] = round(t + 0.2, 3)
        sc.append(s)
        t += dt
    th = THEMES[theme]
    return {"topic": f"_diacritics_{theme}", "ch": "gallery", "dur": round(t, 3), "seed": 7, "accent": th["accent"],
            "look": None, "theme": theme, "brand": th["brand"], "autoTr": False,
            "hud": {"k": "GALLERY", "t": "DẤU KHÓ · " + HARD}, "acc": [], "lines": [], "imgs": {}, "geo": None, "scenes": sc,
            "prog0": 0, "prog1": 1}


def engine_hash() -> str:
    """Băm toàn bộ engine (js/css) — gallery được render với engine nào thì ghi lại băm đó."""
    import hashlib
    h = hashlib.sha1()
    for f in sorted(ENGINE.glob("*")):
        if f.suffix in (".js", ".css"):
            h.update(f.name.encode() + f.read_bytes())
    return h.hexdigest()[:16]


def stale(out_root: Path | None = None) -> list[str]:
    """Theme nào CHƯA có gallery render với engine hiện tại (engine đã sửa sau lần soát cuối). build_long `render` in cảnh báo."""
    base = out_root or ROOT / "output" / "long"
    cur = engine_hash()
    return [th for th in THEMES if not (base / f"_diacritics_{th}" / "engine.sha").exists()
            or (base / f"_diacritics_{th}" / "engine.sha").read_text(encoding="utf-8").strip() != cur]


def still_times(case: dict) -> list[tuple[str, float]]:
    return [(s["gallery"], round(s["t1"] - HOLD, 3)) for s in case["scenes"]]


def write(theme: str) -> tuple[dict, Path, Path]:
    import build_long as BL
    import variety
    case = build_case(theme)
    case["look"] = variety.look(None)
    od = ROOT / "output" / "long" / case["topic"]
    od.mkdir(parents=True, exist_ok=True)
    (od / "data.js").write_text("window.CASE = " + json.dumps(case, ensure_ascii=False) + ";\n", encoding="utf-8")
    comp = BL.HF / "compositions" / "long" / f"{case['topic']}.html"
    comp.parent.mkdir(parents=True, exist_ok=True)
    comp.write_text(BL.HTML.replace("{fonts}", variety.fonts_url(None)).replace("{data}", f"assets/long/{case['topic']}/data.js")
                    .replace("{dur}", f"{case['dur']:.3f}").replace("{title}", "diacritics gallery").replace("{videos}", ""),
                    encoding="utf-8")
    return case, od, comp


def render(theme: str) -> Path:
    import build_long as BL
    from PIL import Image, ImageDraw
    from factory.render_lock import render_lock
    eh = engine_hash()
    case, od, comp = write(theme)
    mp4 = od / "gallery.mp4"
    with render_lock(f"diacritics gallery {theme}"):      # một render một lúc trên cả máy; render khác đang chạy -> chờ
        r = subprocess.run(["npx.cmd", "-y", "-p", "node@22", "-p", "hyperframes@0.8.75", "hyperframes", "render", ".", "-c",
                            f"compositions/long/{comp.name}", "-o", str(mp4), "--fps", "30", "--quiet", "-q", "draft"],
                           cwd=BL.HF, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not mp4.exists():
        raise SystemExit(f"render hỏng\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    sd = od / "stills"
    sd.mkdir(exist_ok=True)
    tiles = []
    for k, (label, t) in enumerate(still_times(case)):
        p = sd / f"{k:02d}_{label}.png"
        subprocess.run([BL.FFMPEG, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", str(p)], check=True)
        tiles.append((label, p))
    W, H, cols = 480, 270, 5
    sheet = Image.new("RGB", (cols * W, ((len(tiles) + cols - 1) // cols) * (H + 22)), "black")
    dr = ImageDraw.Draw(sheet)
    for k, (label, p) in enumerate(tiles):
        x, y = (k % cols) * W, (k // cols) * (H + 22)
        sheet.paste(Image.open(p).convert("RGB").resize((W, H)), (x, y + 22))
        dr.text((x + 6, y + 4), label, fill="white")
    out = od / "sheet.png"
    sheet.save(out)
    (od / "engine.sha").write_text(eh, encoding="utf-8")    # băm engine LÚC render; PM soát sheet.png xong mới coi là đạt
    return out


if __name__ == "__main__":
    from factory.console import utf8_console  # noqa: E402
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    a = sys.argv[1:]
    themes = [x for x in a if x in THEMES] or list(THEMES)
    for th in themes:
        if "render" in a:
            print(render(th))
        else:
            case, od, comp = write(th)
            print(f"{th}: {len(case['scenes'])} cảnh, {case['dur']:.0f}s -> {comp}  (render: thêm 'render')")
