import json, glob, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"D:\Tools\Youtube Creator v2\Youtube_Creator_V2"
src = open(ROOT + r"\motion\stier\build.py", encoding="utf-8").read()
a = src.index("MODE = {"); b = src.index("# ---- BUD v2 (Shorts Studio port")
ns = {}
exec(src[a:b], ns)
mix_lint = ns["mix_lint"]
def norm(w): return re.sub(r"[^\wÀ-ỹ]", "", unicodedata.normalize("NFC", w).lower())
for f in sorted(glob.glob(ROOT + r"\docs\pm\tickets\2026-10-20-mim-nov\specs-v2-T5\*.json")):
    d = json.load(open(f, encoding="utf-8")); L = d["lines"]; n = len(L); err = []
    W = [[norm(w) for w in l.split() if norm(w)] for l in L]
    nw = sum(len(l.split()) for l in L)
    if not 55 <= nw <= 135: err.append(f"{nw} từ")
    if len(L[0].split()) > 9: err.append(f"mở {len(L[0].split())} chữ")
    if L[-1].rstrip().endswith("?"): err.append("kết bằng ?")
    if any(ch.isdigit() for l in L for ch in l): err.append("lời đọc có chữ số")
    if "~" in json.dumps(d["scenes"], ensure_ascii=False): err.append("có ~")
    # thời gian ước: 4,2 âm tiết/s + 0.22 nghỉ
    st = []; t = 0.0
    for w in W: st.append(t); t += len(w) / 4.2 + 0.25
    dur = t + 0.6
    def anchor(v):
        if isinstance(v, list):
            i = v[0]; wd = v[1] if len(v) > 1 else None; k = v[2] if len(v) > 2 else 0; off = v[3] if len(v) > 3 else 0
            if wd is None: return st[i] + off
            hits = [j for j, x in enumerate(W[i]) if x == norm(wd)]
            if len(hits) <= k: err.append(f"neo sai {v}"); return st[i]
            return st[i] + hits[k] / 4.2 + off
        return st[v]
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("at", "until") and isinstance(v, list) and v and isinstance(v[0], int) and len(v) > 1 and isinstance(v[1], (str, type(None))): anchor(v)
                else: walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    sc = []
    for i, s in enumerate(d["scenes"]):
        walk({k: v for k, v in s.items() if k != "at"})
        r = {"type": s["type"], "clip": s.get("clip"), "t0": 0.0 if i == 0 else anchor(s["at"])}
        sc.append(r)
    for i, r in enumerate(sc): r["t1"] = sc[i + 1]["t0"] if i + 1 < len(sc) else dur
    for r in sc:
        if r["t1"] < r["t0"] + 0.9: err.append(f"cảnh {r['type']} ngắn {r['t1']-r['t0']:.1f}s")
    for s in d["scenes"]:
        if s["type"] == "counter":
            if any(c.isdigit() for c in str(s.get("prefix", ""))) and s.get("from", 0) != s["to"]: err.append("prefix số")
            if 1500 <= s["to"] <= 2100 and not s.get("suffix", "").strip(): err.append("counter năm")
            if len(s.get("sub", {}).get("text", "")) > 52: err.append("sub>52")
        if s["type"] == "slam" and len(s.get("sub", "")) > 52: err.append("slam sub>52")
    err += mix_lint(sc)
    modes = "".join(ns["scene_mode"](r) for r in sc)
    print(f"{f.split(chr(92))[-1]:38s} {nw:3d}từ ~{dur:4.1f}s modes={modes} {'OK' if not err else err}")
