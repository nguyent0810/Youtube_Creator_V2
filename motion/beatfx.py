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


# ---------- beat2 (09/10/2026): bố cục cảnh chữ + từ nhấn ----------
# Trước beat2, MỌI cảnh kinetic là một khuôn: dòng nhỏ trên + dòng IN HOA lớn dưới, căn giữa (35–50% số cảnh mỗi video).
# engine/casewide.js đọc r["lay"]; thiếu "lay" = "stack" (khuôn cũ), nên video cũ render y hệt.
LAYOUTS = ["stack", "hero", "split", "corner", "ladder", "frame"]
STACK_MAX = 0.3          # "stack" tối đa 30% số cảnh kinetic của một chương


def _fits(lay: str, main: list[dict], items: list[dict]) -> bool:
    n = sum(len(q.get("text", "")) for q in items)
    if lay == "split":       # hai vế đối nhau, mỗi vế nửa màn hình
        return len(main) == 2 and all(len(q.get("text", "")) <= 22 for q in main)
    if lay == "hero":        # một chữ/số khổng lồ; tối đa 3 dòng (MIM #6 09/10: 4 dòng -> dòng cuối đè phụ đề)
        return len(items) <= 3 and any(len(q.get("text", "")) <= 14 for q in main)
    if lay == "ladder":      # các dòng so le chéo
        return len(items) >= 2 and len(items) <= 4
    if lay == "frame":       # khung ngắm bao quanh
        return n <= 46 and len(items) <= 3
    return True


def assign_layouts(sc: list[dict], key: str) -> None:
    """Cảnh kinetic chưa có "lay" -> chọn bố cục tất định theo key; không trùng cảnh kinetic liền trước,
    "stack" không quá STACK_MAX. Spec ghi sẵn "lay" thì giữ."""
    import random, zlib
    rng = random.Random(zlib.crc32(("lay|" + key).encode()))
    ks = [r for r in sc if r["type"] == "kinetic" and r.get("items")]
    last, n_stack = None, 0
    for i, r in enumerate(ks):
        if r.get("lay"):
            last = r["lay"]
            continue
        main = [q for q in r["items"] if not q.get("sm")]
        opts = [x for x in LAYOUTS if x != last and _fits(x, main, r["items"])
                and not (x == "stack" and n_stack + 1 > STACK_MAX * len(ks))]
        pref = [x for x in opts if x in ("split", "hero")]      # bố cục "có nghĩa" ưu tiên khi nội dung hợp
        r["lay"] = rng.choice(pref if pref and rng.random() < 0.6 else (opts or ["stack"]))
        n_stack += r["lay"] == "stack"
        last = r["lay"]


K_CAPS = 0.72   # bề rộng TB 1 ký tự IN HOA đậm (Be Vietnam Pro 900) / cỡ chữ; 0,62 làm tràn "KHÔNG THAY ĐỔI" (MIM #7 09/10). beat2.js còn tự co khi vẫn tràn.


def _fsz(text: str, mx: float, width: float = 1700, k: float = 0.6) -> int:
    """= casewide.js fsz: cỡ chữ lớn nhất để dòng vừa `width` px."""
    return int(min(mx, width // (max(1, len(text)) * k)))


def layout_items(sc: list[dict]) -> None:
    """Cảnh kinetic có "lay" (khác "stack") -> mỗi dòng q["L"] = {cls, style} (vị trí, cỡ chữ), dòng đầu q["D"] = trang trí
    của cả cảnh. engine/beat2.js áp sau khi casewide.js đặt dòng theo khuôn cũ. Toạ độ khung 1920×1080."""
    px = lambda v: f"{round(v)}px"
    for r in sc:
        lay, items = r.get("lay"), r.get("items") or []
        if r["type"] != "kinetic" or not items or lay in (None, "stack"):
            continue
        t0 = r.get("t0", 0.0)
        first = min(q["at"] for q in items)
        first = t0 + 0.5 if first - t0 > 2.0 else first     # casewide B.kinetic kéo dòng đầu đến muộn về sớm
        main = [q for q in items if not q.get("sm")] or items
        deco = []
        if lay == "hero":
            h = min(main, key=lambda q: len(q["text"]))
            hs = h.get("size") or _fsz(h["text"], 290, 1640, K_CAPS)
            above = [q for q in items if q is not h and q["at"] < h["at"]]
            below = [q for q in items if q is not h and q["at"] >= h["at"]]
            # cả khối (dòng trên + chữ lớn + dòng dưới) phải nằm trong 130..840 px (dưới 840 là vùng phụ đề) -> co chữ lớn nếu cần
            block = lambda s: len(above) * (74 + s * 0.16) + s * 1.18 + len(below) * 104
            while block(hs) > 700 and hs > 90:
                hs = int(hs * 0.94)
            step = 74 + hs * 0.16     # chữ khổng lồ có dấu chồng (Á, À, Ế) nhô lên trên mép khối -> chừa thêm (snapshot 09/10: đè dòng nhỏ)
            y = max(130, 480 - block(hs) / 2)     # căn giữa CẢ khối (trước đây neo chữ lớn ở 520 -> dòng dưới tụt vào phụ đề)
            for q in above:
                q["L"] = {"style": {"top": px(y), "fontSize": px(q.get("size") or _fsz(q["text"], 60, 1500, 0.62))}}
                y += step
            h["L"] = {"style": {"top": px(y), "fontSize": px(hs)}}
            y += hs * 1.18
            deco.append({"kind": "rule", "style": {"top": px(y - hs * 0.08)}, "at": round(h["at"] + 0.1, 3)})
            for q in below:
                y += 26
                q["L"] = {"style": {"top": px(y), "fontSize": px(q.get("size") or _fsz(q["text"], 64, 1500, 0.62))}}
                y += 78
        elif lay == "split":
            for k, q in enumerate([q for q in items if q.get("sm")]):
                q["L"] = {"style": {"top": px(150 + k * 66), "fontSize": px(q.get("size") or 52)}}
            for k, q in enumerate(main[:2]):
                s = q.get("size") or _fsz(q["text"], 120, 740, K_CAPS)
                q["L"] = {"cls": "kR" if k else "kL", "style": {"top": px(470 - s * 0.6), "fontSize": px(s)}}
            deco.append({"kind": "split", "style": {}, "at": round(min(q["at"] for q in main) - 0.3, 3)})
        elif lay == "corner":
            sizes = [q.get("size") or _fsz(q["text"], 50 if q.get("sm") else 118, 1350, K_CAPS) for q in items]
            tot = sum(s * 1.3 for s in sizes)
            y = max(170, 880 - tot)
            deco.append({"kind": "bar", "style": {"top": px(y), "height": px(tot - 20)}, "at": round(first - 0.25, 3)})
            for q, s in zip(items, sizes):
                q["L"] = {"cls": "kC", "style": {"top": px(y), "fontSize": px(s)}}
                y += s * 1.3
        elif lay == "ladder":
            y = 250
            for k, q in enumerate(items):
                s = q.get("size") or _fsz(q["text"], 58 if q.get("sm") else 104 + k * 10, 1500 - k * 170, K_CAPS)
                q["L"] = {"cls": "kC", "style": {"top": px(y), "fontSize": px(s), "left": px(140 + k * 170)}}
                y += s * 1.34 + 18
        elif lay == "frame":
            sizes = [q.get("size") or _fsz(q["text"], 54 if q.get("sm") else 124, 1300, K_CAPS) for q in items]
            tot = sum(s * 1.32 for s in sizes)
            y = 520 - tot / 2
            w = min(1500, max(len(q["text"]) * s * 0.62 for q, s in zip(items, sizes)) + 160)
            deco.append({"kind": "frame", "style": {"top": px(y - 76), "height": px(tot + 130), "width": px(w), "left": px((1920 - w) / 2)},
                         "at": round(first - 0.3, 3)})
            for q, s in zip(items, sizes):
                q["L"] = {"style": {"top": px(y), "fontSize": px(s)}}
                y += s * 1.32
        if deco:
            min(items, key=lambda q: q["at"])["D"] = deco


# ---------- QA tràn chữ beat2 (retro 3 mục 15: "KHÔNG THAY ĐỔI", "ĐẮT HAY RẺ?", "ĐỘ DỐC MA200" cắt mép — QA năng lượng khung hình không bắt) ----------
# Ước lượng bề rộng từng ký tự (em) cho Be Vietnam Pro 900: chữ hoa đậm rộng ~0,80 em (K_CAPS 0,72 là hệ số CỠ CHỮ, đã chừa lề 80 px).
# Hiệu chỉnh 10/10: "KHÔNG THAY ĐỔI" cỡ 85 px (k cũ 0,62) trong ô split 820 px -> vượt; cỡ 73 px (K_CAPS 0,72) -> vừa.
_CW = {" ": 0.25, "I": 0.36, "1": 0.5, ".": 0.3, ",": 0.3, ":": 0.3, ";": 0.3, "!": 0.34, "'": 0.25, "·": 0.3, "|": 0.3,
       "M": 0.98, "W": 1.05, "→": 0.95, "?": 0.62, "-": 0.42, "%": 0.95, "/": 0.45}
BOX_PAD = {"stamp": 0.64 + 0.15, "tape": 0.84}      # beat.css .stp / .tp: đệm + viền (em)
FIT_MIN = 0.4                                        # beat2.js fitTo co tối đa còn 40% cỡ đặt; dưới đó chữ vẫn tràn
OVER_TOL = 1.03                                      # sai số ước lượng: MIM #6 bản đã duyệt có 2 dòng 98% (ô vừa khít) -> không báo


def text_em(text: str) -> float:
    """Bề rộng ước lượng (theo em) của một dòng .kin (nowrap) — chữ thường ~0,6 em, số ~0,7 em."""
    w = 0.0
    for c in text:
        if c in _CW:
            w += _CW[c]
        elif c.isdigit():
            w += 0.7
        elif c.isalpha():
            w += 0.8 if c.isupper() else 0.6
        else:
            w += 0.6
    return w


def _box(q: dict) -> float:
    """Bề rộng ô của dòng theo beat2.css / casewide.css (.kin: left 100 right 100; kL/kR: 820; kC: left..1840)."""
    L = q.get("L") or {}
    cls = (L.get("cls") or "").split()
    if "kL" in cls or "kR" in cls:
        return 820.0
    if "kC" in cls:
        left = float(str((L.get("style") or {}).get("left", "190px")).rstrip("px") or 190)
        return 1920.0 - left - 80.0
    return 1720.0


def overflow_lines(sc: list[dict], ch: str = "") -> list[str]:
    """beat2: dòng chữ có q["L"] mà bề rộng ước lượng > ô của nó -> cảnh báo (beat2.js sẽ co chữ; dưới 40% vẫn bị cắt).
    Gọi trên cảnh đã layout_items (data.js)."""
    out = []
    for k, r in enumerate(sc):
        if r.get("type") != "kinetic":
            continue
        for q in r.get("items") or []:
            L = q.get("L")
            if not L:
                continue
            try:
                fs = float(str((L.get("style") or {}).get("fontSize", "0")).rstrip("px"))
            except ValueError:
                continue
            em = text_em(q.get("text", "")) + 0.32 + BOX_PAD.get(q.get("fx"), 0.0)      # .kt padding 0 .16em
            need, box = em * fs, _box(q)
            if fs and need > box * OVER_TOL:
                fate = "CẮT MÉP (vượt cả mức co 40%)" if need * FIT_MIN > box else f"beat2.js sẽ co còn ~{box / need:.0%} cỡ"
                out.append(f"{ch} cảnh {k} {r.get('lay')}: \"{q.get('text')}\" cỡ {fs:.0f}px cần ~{need:.0f}px > ô {box:.0f}px — {fate}; "
                           f"rút gọn chữ hoặc bỏ \"size\"")
    return out


def pick_em(sc: list[dict]) -> None:
    """Dòng lớn ≥ 3 chữ chưa có "em" -> một từ nhấn: chữ có số trước, rồi chữ dài nhất (≥ 4 ký tự).
    Không áp cho fx gõ chữ (type/scramble: chữ thay từng ký tự, không bọc được)."""
    for r in sc:
        if r.get("lay") == "hero":      # hero đã có vạch nhấn riêng; thêm vạch dưới từ nhấn = hai vạch chồng nhau (snapshot 09/10)
            continue
        items = r.get("items") if r["type"] == "kinetic" else r.get("kin")
        for q in items or []:
            if q.get("sm") or q.get("em") or q.get("fx") in ("type", "scramble"):
                continue
            ws = [w for w in q.get("text", "").split() if _norm(w)]
            if len(ws) < 3:
                continue
            num = [w for w in ws if re.search(r"\d", w)]
            long = max(ws, key=lambda w: len(_norm(w)))
            q["em"] = num[0] if num else (long if len(_norm(long)) >= 4 else None)
            if not q["em"]:
                del q["em"]


def pull_main(sc: list[dict], max_s: float = 0.8) -> None:      # 0,8 (không phải 1,2 như light_start): D2 09/10 dòng chính hiện ở 1,0 s vẫn bị qa_blank bắt
    """beat2: dòng CHÍNH đầu tiên của cảnh kinetic hiện muộn > max_s (neo vào từ giữa câu) -> kéo về sớm: 0,4 s sau dòng nhỏ đầu
    tiên (tối thiểu t0 + 0,3). Dòng sync bị kéo thì bỏ sync (không thể hiện từng chữ trước khi được đọc). Gọi SAU assign_beats.
    light_start vẫn là chốt kiểm (render từ chối) cho trường hợp còn sót."""
    for r in sc:
        if r["type"] != "kinetic" or not r.get("items"):
            continue
        main = [q for q in r["items"] if not q.get("sm")]
        if not main:
            continue
        t0 = r["t0"]
        show = lambda q: q["wt"][0] if q.get("fx") == "sync" and q.get("wt") else q["at"]
        q = min(main, key=show)
        if show(q) - t0 <= max_s:
            continue
        sm_at = min((x["at"] for x in r["items"] if x.get("sm")), default=t0)
        q["at"] = round(max(t0 + 0.3, min(sm_at + 0.4, t0 + max_s - 0.1)), 3)
        if q.get("fx") == "sync":
            q.pop("wt", None)
            q.pop("t0", None)
            q["fx"] = "rise"


def light_start(sc: list[dict], ch: str = "", max_s: float = 1.2) -> list[str]:
    """beat2: cảnh kinetic mà dòng CHÍNH (không "sm") đầu tiên hiện rõ muộn hơn max_s sau t0 -> chỉ có chữ nhỏ / trang trí
    trên nền tối = qa_blank coi là màn trống (MIM #6 09/10/2026: "chưa ai nhắc tới" một mình 2 s). late_first chỉ nhìn phần tử
    ĐẦU TIÊN nên không bắt được. Dòng sync hiện rõ ở wt[0]."""
    out = []
    for k, r in enumerate(sc):
        if r["type"] != "kinetic" or not r.get("items"):
            continue
        main = [q for q in r["items"] if not q.get("sm")]
        if not main:
            continue
        t0 = r["t0"]
        first = min((q["wt"][0] if q.get("fx") == "sync" and q.get("wt") else q["at"]) for q in main)
        if first - t0 > 2.0 and min(q["at"] for q in r["items"]) - t0 > 2.0:
            first = t0 + 0.5        # casewide kéo dòng đầu đến muộn về sớm
        if first - t0 > max_s:
            out.append(f"{ch} cảnh {k} kinetic: dòng chính hiện sau {first - t0:.1f}s (trước đó chỉ chữ nhỏ) — neo cảnh vào đúng từ của dòng chính")
    return out


def verbatim_share(sc: list[dict], lines: list[dict]) -> tuple[int, int]:
    """(số dòng chữ lớn chép nguyên lời đọc, tổng số dòng chữ lớn). Chữ trên màn hình nên là từ khoá / con số / vế
    đối lập, không phải phụ đề phóng to -- build_long in WARNING khi tỉ lệ cao."""
    spoken = " " + " ".join(_norm(w["w"]) for ln in lines for w in ln["words"]) + " "
    tot = hit = 0
    for r in sc:
        if r["type"] != "kinetic":
            continue
        for q in r.get("items") or []:
            if q.get("sm"):
                continue
            toks = [k for k in (_norm(x) for x in q.get("text", "").split()) if k]
            if len(toks) < 3:
                continue
            tot += 1
            hit += (" " + " ".join(toks) + " ") in spoken
    return hit, tot


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


def _per_token(text: str, wt: list[float]) -> list[float]:
    """Mốc cho TỪNG chữ theo cách beat.js tách (split(" ")): ký hiệu không đọc ("→", "·", "=", "/") lấy mốc của chữ đọc kế
    tiếp (hết chữ thì chữ trước). Thiếu bước này, wt ngắn hơn số chữ trên màn hình -> chữ cuối dòng không bao giờ hiện
    (lỗi C2 07/10/2026: "→ CÔNG TY CHỨNG KHOÁN" mất chữ KHOÁN)."""
    toks = text.split(" ")
    real = [bool(_norm(t)) for t in toks]
    if sum(real) != len(wt) or all(real):
        return wt
    out, j = [], 0
    for k, r in enumerate(toks):
        if r and real[k]:
            out.append(wt[j]); j += 1
        else:
            out.append(wt[min(j, len(wt) - 1)])
    return out


def apply_sync(sc: list[dict], lines: list[dict], min_at: float = 0.3, every: int = 1, max_lead: float | None = None) -> None:
    """Dòng chữ lớn (kinetic, không phải dòng nhỏ "sm", chưa ghi fx) mà MỌI chữ đều được đọc trong
    cảnh -> fx "sync" + q["wt"] (mốc từng chữ). Gọi TRƯỚC assign_beats (nó bỏ qua dòng đã có fx).
    every > 1 (beat2): chỉ 1 trong `every` cảnh có chữ được dùng sync -- 40–50% số dòng cùng một kiểu hiện chữ
    là nguồn chính của cảm giác lặp (PM 09/10/2026); các cảnh còn lại để assign_beats xoay vòng."""
    words = sorted((w for ln in lines for w in ln["words"]), key=lambda w: w["t"])
    k_scene = -1
    for r in sc:
        items = r.get("items") if r["type"] == "kinetic" else r.get("kin")   # video dài: chữ phủ "kin" trên ảnh/clip
        if not items:
            continue
        k_scene += 1
        if every > 1 and k_scene % every:
            continue
        cur = SyncCursor(words, r["t0"], r["t1"])
        for q in sorted(items, key=lambda q: q["at"]):
            if q.get("fx") or q.get("sm") or q["at"] < min_at:   # khung 0 (hook, thumbnail) phải có chữ
                continue
            wt = cur.take(q.get("text", ""), q["at"])
            if wt and max_lead is not None and wt[0] - r["t0"] > max_lead:
                continue      # chữ đầu đọc muộn -> sync hiện cả dòng mờ 16% chờ lời = màn gần trống (MIM #6 09/10: 11 đoạn qa_blank)
            if wt:
                wt = _per_token(q.get("text", ""), wt)
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
