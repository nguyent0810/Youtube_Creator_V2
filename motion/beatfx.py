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


def assign_beats(sc: list[dict], key: str, boxed_max: int = 18) -> None:
    """Tất định theo tên chương; mỗi nhóm xoay vòng (xáo trộn theo seed), không lặp kiểu vừa dùng.
    Spec ghi sẵn "fx" thì giữ nguyên (kể cả "strike" + "strikeAt")."""
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
    cN, cA, cS, cD, cX = cycler(BEAT_N), cycler(BEAT_A), cycler(BEAT_S), cycler(BEAT_D), cycler(SLAM_FX)
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
                else:
                    shared = shared or cN()
                    q["fx"] = shared
        if r["type"] == "slam" and not r.get("fx"):
            r["fx"] = cX()


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
