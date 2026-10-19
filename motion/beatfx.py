"""Beat text: chọn hiệu ứng chữ (engine/beat.js) và tiếng tay đi kèm — dùng chung cho video dài (build_long) và Short (stier/build).

Kiểu dòng thường: rise · blur · slice · drop · pop (cả cảnh dùng chung một kiểu)
Kiểu dòng nhấn (acc): marker · redact · stamp · tape · outline · flicker
Dòng nhỏ (sm): type · rise · blur      Dòng ngắn có số: scramble · type
Slam: punch · glitch · zoom · slice · outline
Spec ghi sẵn "fx" thì giữ nguyên (vd "strike" + "strikeAt" cho câu "không phải X").
"""
import re

BEAT_N = ["rise", "blur", "slice", "drop", "pop"]                  # dòng thường: cả cảnh dùng chung một kiểu
BEAT_A = ["marker", "redact", "stamp", "tape", "outline", "flicker"]  # dòng nhấn (acc)
BEAT_S = ["type", "rise", "blur"]                                  # dòng nhỏ (sm)
BEAT_D = ["scramble", "type"]                                      # dòng ngắn có con số / năm
SLAM_FX = ["punch", "glitch", "zoom", "slice", "outline"]
BOXED = {"stamp", "tape"}                                          # có khung/đệm -> chỉ cho dòng ngắn (khỏi tràn mép)


def assign_beats(sc: list[dict], key: str, boxed_max: int = 18, pools: dict | None = None) -> None:
    """Tất định theo tên chương; mỗi nhóm xoay vòng (xáo trộn theo seed), không lặp kiểu vừa dùng.
    Spec ghi sẵn "fx" thì giữ nguyên (kể cả "strike" + "strikeAt").

    pools (theo kênh, motion/stier/themes.py): {"N","A","S","D","X": [...], "per_line": bool}.
    None = bộ cũ, kết quả y hệt từng byte (CL, video dài). per_line=True: dòng thường
    mỗi dòng một kiểu thay vì cả cảnh dùng chung."""
    P = pools or {}
    import random, zlib
    rng = random.Random(zlib.crc32(key.encode()))

    def cycler(pool):
        order, st = pool[:], {"i": 0, "last": None}
        rng.shuffle(order)

        def nxt(ok=lambda v: True):
            for _ in range(len(order) * 2):
                v = order[st["i"] % len(order)]
                st["i"] += 1
                if v != st["last"] and ok(v):
                    st["last"] = v
                    return v
            return "pop"
        return nxt
    cN, cA, cS, cD, cX = (cycler(P.get("N", BEAT_N)), cycler(P.get("A", BEAT_A)), cycler(P.get("S", BEAT_S)),
                          cycler(P.get("D", BEAT_D)), cycler(P.get("X", SLAM_FX)))
    for r in sc:
        items = r.get("items") if r["type"] == "kinetic" else r.get("kin")
        if items:
            shared = None
            for q in items:
                if q.get("fx"):
                    continue
                t = q.get("text", "")
                if re.search(r"\d", t) and len(t) <= 16 and not q.get("acc"):
                    q["fx"] = cD()
                elif q.get("acc"):
                    q["fx"] = cA(lambda v: v not in BOXED or len(t) <= boxed_max)
                elif q.get("sm"):
                    q["fx"] = cS()
                elif P.get("per_line"):
                    q["fx"] = cN()
                else:
                    shared = shared or cN()
                    q["fx"] = shared
        if r["type"] == "slam" and not r.get("fx"):
            r["fx"] = cX()


def _norm(w: str) -> str:
    import unicodedata
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFC", str(w).lower()))


class SyncCursor:
    """Ghép chữ của một dòng chữ lớn với lời đọc trong MỘT cảnh (Beat Text "sync", kênh MIM).

    Mọi chữ của dòng phải khớp, theo thứ tự, một chữ được đọc CHƯA dùng, trong [t0, t1) của cảnh
    và không sớm hơn at - 0.35 s. Thiếu một chữ -> None (dòng giữ hiệu ứng cũ): không bao giờ làm
    hiện một chữ chưa được đọc, không mượn chữ của cảnh trước (Grok, vòng 4)."""

    def __init__(self, words: list[dict], t0: float, t1: float):
        self.w = [w for w in words if t0 <= w["t"] < t1]
        self.used: set[int] = set()

    def take(self, text: str, at: float) -> list[float] | None:
        toks = [k for k in (_norm(x) for x in text.split()) if k]
        if not toks:
            return None
        got, i = [], 0
        for tok in toks:
            hit = next((k for k in range(i, len(self.w)) if k not in self.used
                        and self.w[k]["t"] >= at - 0.35 and _norm(self.w[k]["w"]) == tok), None)
            if hit is None:
                return None
            got.append(hit)
            i = hit + 1
        self.used.update(got)
        return [self.w[k]["t"] for k in got]


def apply_sync(sc: list[dict], lines: list[dict]) -> None:
    """Dòng chữ lớn (kinetic, không phải dòng nhỏ "sm", chưa ghi fx) mà MỌI chữ đều được đọc trong
    cảnh -> fx "sync" + q["wt"] (mốc từng chữ). Gọi TRƯỚC assign_beats (nó bỏ qua dòng đã có fx)."""
    words = sorted((w for ln in lines for w in ln["words"]), key=lambda w: w["t"])
    for r in sc:
        if r["type"] != "kinetic":
            continue
        cur = SyncCursor(words, r["t0"], r["t1"])
        for q in sorted(r["items"], key=lambda q: q["at"]):
            if q.get("fx") or q.get("sm") or q["at"] < 0.3:   # khung 0 (hook, thumbnail) phải có chữ
                continue
            wt = cur.take(q.get("text", ""), q["at"])
            if wt:
                q["fx"], q["wt"], q["t0"] = "sync", [round(t, 3) for t in wt], r["t0"]


def beat_sfx(M, q, g=1.0):
    """Tiếng tay theo kiểu chữ (q.fx do assign_beats chọn). Mix nào thiếu paper/static thì thay bằng tiếng gần nhất."""
    fx, t = q.get("fx", "pop"), q["at"]
    if fx in ("rise", "slice", "blur"):
        M.put(t - 0.3, M.whoosh(0.4 if fx != "blur" else 0.6), 0.22 * g)
        if fx == "slice":
            M.put(t - 0.02, M.thud(0.3), 0.25 * g)
    elif fx == "drop":
        for k in range(min(4, len(q.get("text", "").split()))):
            M.put(t - 0.05 + 0.07 * k, M.thud(0.25), 0.22 * g)
    elif fx == "marker":
        M.put(t, M.scratch(0.38), 0.55 * g)
    elif fx == "redact":
        M.put(t - 0.32, M.scratch(0.16), 0.4 * g)
        M.put(t, M.paper(0.3) if hasattr(M, "paper") else M.scratch(0.25), 0.45 * g)
    elif fx == "stamp":
        M.put(t + 0.01, M.thud(0.55), 0.7 * g)
        M.put(t + 0.01, M.boom(1.0, 70, 40), 0.3 * g)
    elif fx == "tape":
        M.put(t - 0.22, M.paper(0.35) if hasattr(M, "paper") else M.whoosh(0.3), 0.55 * g)
    elif fx == "flicker":
        M.put(t - 0.2, M.static(0.45) if hasattr(M, "static") else M.scratch(0.4), 0.35 * g)
    elif fx == "outline":
        M.put(t - 0.3, M.whoosh(0.35), 0.2 * g)
        M.put(t + 0.05, M.thud(0.35), 0.3 * g)
    elif fx == "sync":       # tiếng gõ nhẹ đúng lúc từng chữ hiện (theo lời đọc)
        for t in q.get("wt") or [q["at"]]:
            M.put(t - 0.02, M.tick(3200, 0.02), 0.12 * g)
    elif fx == "glitch":     # glitch chỉ trên chữ (MIM), không rung khung
        M.put(t - 0.05, M.static(0.3) if hasattr(M, "static") else M.scratch(0.3), 0.3 * g)
    elif fx == "type":
        n = len(q.get("text", ""))
        span = min(0.9, 0.045 * n)
        for k in range(min(n, 22)):
            M.put(t - 0.05 + span * (k / max(1, min(n, 22))), M.key(), 0.3 * g)
    elif fx == "scramble":
        for k in range(14):
            M.put(t - 0.35 + 0.035 * k, M.tick(2400 + 90 * k, 0.025), 0.22 * g)
    else:   # pop, strike
        M.put(t - 0.02, M.thud(0.4), 0.42 * g)
