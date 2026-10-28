"""Tự kiểm spec v2-T8 (build.py KHÔNG có cờ --lint-only): mốc chữ [câu,"chữ"], luật câu mở/chốt, 55-135 chữ, dòng phụ <= 52,
mix_lint của build.py chạy trên giờ ƯỚC LƯỢNG (4 âm tiết/giây + khoảng lặng tts.pauses). Chạy: python specs-v2-T8/_selfcheck.py
Chỉ đọc spec, không dựng, không TTS, không ghi gì."""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "motion/stier"))
sys.path.insert(0, str(ROOT / "motion"))
import build  # noqa
from build import mix_lint, scene_mode, norm  # noqa

SPECS = sorted(Path(__file__).resolve().parent.glob("*.json"))
SYL = {"chatgpt": 4, "google": 2, "gemini": 3, "samsung": 2, "openai": 4, "anthropic": 4, "claude": 1, "chatbot": 2,
       "bloomberg": 2, "hack": 1, "ai": 2, "gpt": 3}
RATE = 4.0
ANCH = build.ANCHORS | {"cross"}


def syl(tok):
    t = norm(tok)
    if t in SYL:
        return SYL[t]
    if t.isdigit():
        return 8 if len(t) == 4 else 2.5
    return 1


def check(path):
    sp = json.loads(path.read_text(encoding="utf-8"))
    errs, warns = [], []
    L = sp["lines"]
    toks = [l.split() for l in L]
    nw = sum(len(t) for t in toks)
    if not 55 <= nw <= 135:
        errs.append(f"{nw} từ ngoài 55-135")
    if len(toks[0]) > 9:
        errs.append(f"câu mở {len(toks[0])} chữ > 9")
    if L[-1].rstrip().endswith("?"):
        errs.append("kết bằng câu hỏi")
    if re.search(r"mẹo", " ".join(L) + sp["title"], re.I):
        errs.append("có chữ mẹo")
    if re.search(r"video (đầy đủ|dài)|xem (thêm|bản)|link", " ".join(L), re.I):
        errs.append("lời đọc mời xem video")
    if len(sp["title"]) > 100:
        errs.append(f"title {len(sp['title'])} > 100")
    pause = sp["tts"]["pauses"]
    # thời lượng ước lượng
    starts, t = [], 0.0
    for i, tk in enumerate(toks):
        starts.append(t)
        t += sum(syl(x) for x in tk) / RATE + float(pause.get(str(i), 0.0))
    total = t + 0.6
    est_syl = sum(sum(syl(x) for x in tk) for tk in toks)

    def A(a):
        if isinstance(a, (int, float)):
            return starts[int(a)] if float(a).is_integer() and a < len(L) else a
        i, w = a[0], a[1]
        n = a[2] if len(a) > 2 else 0
        off = a[3] if len(a) > 3 else 0
        if w is None:
            return starts[i] + off
        c = 0
        acc = 0.0
        for x in toks[i]:
            if norm(x) == norm(w):
                if c == n:
                    return starts[i] + acc / RATE + off
                c += 1
            acc += syl(x)
        errs.append(f"mốc [{i},{w!r},{n}] không có trong câu {i}: {L[i]}")
        return starts[i]

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ANCH and isinstance(v, (int, list)) and not isinstance(v, bool):
                    A(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(sp["scenes"])
    sc = []
    for k, r in enumerate(sp["scenes"]):
        t0 = 0.0 if k == 0 and "at" not in r else A(r.get("at", 0))
        sc.append({"type": r["type"], "t0": t0, **{x: r[x] for x in ("clip", "vid") if x in r}})
    for k, r in enumerate(sc):
        r["t1"] = sc[k + 1]["t0"] if k + 1 < len(sc) else total
    bad = mix_lint(sc)
    if bad:
        errs += ["mix: " + b for b in bad]
    modes = "".join(scene_mode(r) for r in sc)
    dur = {m: sum(r["t1"] - r["t0"] for r, x in zip(sc, modes) if x == m) / total for m in "TMDG"}
    # dòng phụ ≤ 52, năm trong counter, ~
    for r in sp["scenes"]:
        for tx in ((r.get("sub") or {}).get("text") if r["type"] == "counter" else r.get("sub") if r["type"] == "slam" else r.get("unit") if r["type"] == "chart" else None,):
            if isinstance(tx, str) and len(tx) > 52:
                errs.append(f"sub > 52: {tx}")
        if r["type"] == "counter":
            if any(ch.isdigit() or ch in "<>≈~" for ch in str(r.get("prefix") or "")) and r.get("from", 0) != r["to"]:
                errs.append("counter prefix có chữ số")
            if float(r["to"]).is_integer() and 1500 <= r["to"] <= 2100 and not str(r.get("suffix") or "").strip():
                errs.append("counter hiện năm")
    if "~" in json.dumps(sp["scenes"], ensure_ascii=False):
        errs.append("có dấu ~")
    if sp["scenes"][0]["type"] != "kinetic" and sp["scenes"][0]["type"] != "slam":
        warns.append("cảnh đầu không phải kinetic/slam")
    return nw, est_syl, total, modes, dur, errs, warns, sp


if __name__ == "__main__":
    allbad = 0
    for p in SPECS:
        nw, es, total, modes, dur, errs, warns, sp = check(p)
        print(f"{p.stem}: {nw} chữ · ~{es:.0f} âm tiết · ~{total:.0f}s · cảnh {modes} · T{dur['T']:.0%} M{dur['M']:.0%} D{dur['D']:.0%} G{dur['G']:.0%} · mở {len(sp['lines'][0].split())} chữ")
        for e in errs:
            print("   LỖI", e)
        for w in warns:
            print("   cảnh báo", w)
        allbad += len(errs)
    print("TỔNG LỖI", allbad)
