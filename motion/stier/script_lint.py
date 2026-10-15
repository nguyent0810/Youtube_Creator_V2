"""Lint kịch bản Short BUD (14/10/2026) -- 10 luật rút từ audit #35-#104 + nghiên cứu hook/open-loop/loop.
Gọi từ build.py (theme bud) sau khi đo giọng. Spec "v2": true -> vi phạm là LỖI (dừng build); spec cũ -> cảnh báo.
Chạy tay: python motion/stier/script_lint.py <slug> [...]   (không cần TTS: luật nhịp dùng ước lượng 3,3 từ/giây)."""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path

SPECS = Path(__file__).resolve().parents[2] / "data" / "stier" / "specs"
STOP = set("""và là của có không cho với thì mà một những các này đó ấy rồi được đã đang sẽ cũng như khi nếu vì nên để
ta mình bạn tôi người ai gì nào đâu chỉ còn lại ra vào lên xuống thật rất hay hoặc nhé nha không? đi""".split())
NUMW = set("một hai ba bốn năm sáu bảy tám chín mười mươi trăm nghìn ngàn lẻ linh mốt tư lăm".split())
CITE = re.compile(r"\b(kinh|kệ|đức phật dạy|phật dạy|diễn ý)\b", re.I)
REHOOK = ("nhưng", "điều thứ hai", "phép thử", "thật ra", "mấu chốt", "điều lạ", "bí mật", "còn điều", "chưa hết",
          "vì sao", "điều quan trọng", "cái hay", "bất ngờ", "ngược lại", "đoán xem", "thử xem", "khoan")
GENERIC_CTA = re.compile(r"bình luận nhé\s*[.!]?\s*$", re.I)
GREET = re.compile(r"^(xin chào|chào|hôm nay|các bạn|mọi người ơi)\b", re.I)
WHITE3 = {"kinh pháp cú", "pháp cú kệ", "kinh tăng chi", "kinh tương ưng", "kinh trung bộ", "đức phật dạy", "quán thế âm"}


def nfc(s): return unicodedata.normalize("NFC", s)
def words(s): return re.findall(r"[\wÀ-ỹ]+", nfc(s).lower())


def recent(slug: str, n: int = 15, base: str | None = None) -> list[list[str]]:
    """Kịch bản bud gần nhất theo mtime (trừ chính nó / bản gốc của nó)."""
    me = {slug, base or "", slug.removesuffix("-v2")}
    fs = [f for f in SPECS.glob("bud-*.json") if f.stem not in me and f.stem.removesuffix("-v2") not in me]
    fs.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    out, seen = [], set()
    for f in fs:
        k = f.stem.removesuffix("-v2")
        if k in seen:
            continue
        seen.add(k)
        try:
            out.append(json.loads(f.read_text(encoding="utf-8"))["lines"])
        except Exception:     # noqa: BLE001
            continue
        if len(out) >= n:
            break
    return out


def grams(L, k=3):
    g = set()
    for l in L:
        w = words(l)
        g |= {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}
    return g


def lint(slug: str, spec: dict, lines: list[dict] | None = None, dur: float | None = None) -> tuple[list[str], list[str]]:
    """-> (errors, warnings). lines/dur (đo từ giọng) có thì luật nhịp dùng số đo thật."""
    E, W = [], []
    L = spec["lines"]
    strict = bool(spec.get("v2"))
    bad = E if strict else W
    rec = recent(slug, 15, spec.get("based_on"))
    hook, last = L[0], L[-1]
    nw = [len(words(l)) for l in L]
    tot = sum(nw)
    cum = [sum(nw[:i]) / tot for i in range(len(L))]          # vị trí bắt đầu từng câu (tỉ lệ)
    if lines and dur:
        cum = [ln["start"] / dur for ln in lines]
    # R1 hook
    if nw[0] > 12:
        bad.append(f"R1 hook {nw[0]} từ (> 12): {hook!r}")
    if GREET.search(hook) and not spec.get("special_date"):
        bad.append(f"R1 hook mở bằng chào/ngày ('{GREET.search(hook).group(0)}') -- vào thẳng tình huống")
    op = " ".join(words(hook)[:2])
    if any(" ".join(words(r[0])[:2]) == op for r in rec[:10]):
        bad.append(f"R1 hai chữ mở đầu '{op}' trùng 1 trong 10 kịch bản gần nhất")
    # R2 open loop + re-hook
    ci = next((i for i, l in enumerate(L) if CITE.search(l)), None)
    if ci is not None and cum[ci] < 0.25:
        bad.append(f"R2 trích dẫn/đáp án tới quá sớm (câu {ci}, {cum[ci]:.0%} < 25%) -- giữ vòng mở")
    mid = [i for i in range(1, len(L) - 1) if 0.3 <= cum[i] <= 0.75]
    if not any(any(m in nfc(L[i]).lower() for m in REHOOK) for i in mid):
        bad.append("R2 không có câu móc lại giữa video (30-75%): thêm 'nhưng…', 'phép thử…', 'thật ra…'")
    # R3 trích dẫn nói ngắn
    for i, l in enumerate(L):
        if CITE.search(l):
            head = re.split(r"diễn ý|:", nfc(l), maxsplit=1)[0]
            if len(words(head)) > 8:
                bad.append(f"R3 câu {i}: phần dẫn nguồn nói {len(words(head))} từ (> 8) -- số kệ để thẻ nguồn")
            run = mx = 0
            for w in words(head):
                run = run + 1 if w in NUMW else 0; mx = max(mx, run)
            if mx > 3:
                bad.append(f"R3 câu {i}: số đọc thành {mx} chữ -- đưa số lên màn hình")
    # R4 loop callback
    hk = {w for w in words(hook) if w not in STOP and len(w) > 1}
    if not hk & {w for w in words(last) if w not in STOP and len(w) > 1}:
        bad.append("R4 câu cuối không gọi lại chữ nào của hook (loop callback)")
    # R5 CTA
    if "?" not in last:
        bad.append("R5 câu cuối phải là câu hỏi")
    if GENERIC_CTA.search(last) and (strict or sum(bool(GENERIC_CTA.search(r[-1])) for r in rec[:5]) >= 2):
        bad.append("R5 CTA chung chung 'Bình luận nhé' -- hỏi một chữ/một số cụ thể")
    # R6 nhịp
    rate = (tot / (dur - 1.0)) if dur else 3.3
    if dur and not 2.6 <= rate <= 3.8:
        bad.append(f"R6 nhịp {rate:.2f} từ/giây (ngoài 2,6-3,8)")
    for i, l in enumerate(L):
        if nw[i] > 22:
            bad.append(f"R6 câu {i} dài {nw[i]} từ (> 22)")
        for sen in re.split(r"[.!?]", nfc(l)):
            if len(words(sen)) > 14:
                bad.append(f"R6 câu {i}: một mệnh đề {len(words(sen))} từ (> 14) -- cắt cho giọng đọc")
    # R7 TTS
    for i, l in enumerate(L):
        if re.match(r"^\s*(trước|sau)\s*:", l, re.I):
            bad.append(f"R7 câu {i}: nhãn 'Trước:/Sau:' đọc lên rất máy")
        if re.search(r"[()/\[\]]|\b[A-Z]{2,}\b", l):
            bad.append(f"R7 câu {i}: ngoặc/gạch chéo/viết tắt -> TTS đọc sai: {l!r}")
        if re.search(r"\d", l):
            W.append(f"R7 câu {i}: có chữ số -- kiểm tra cách đọc")
    # R8 lặp cụm 3 từ
    mine = grams(L) - WHITE3
    hot = sorted(g for g in mine if sum(g in grams(r) for r in rec) > 3)
    if hot:
        bad.append(f"R8 cụm lặp ở > 3/15 kịch bản gần nhất: {hot[:5]}")
    # R9 cụ thể (chỉ cảnh báo)
    if not (re.search(r"\d", " ".join(L)) or any(w in NUMW for w in words(" ".join(L)))):
        W.append("R9 không có con số/chi tiết đếm được -- kiểm tra độ cụ thể bằng mắt")
    # R10 nguồn
    if not spec.get("sources"):
        E.append("R10 thiếu sources")
    if ci is not None and "diễn ý" not in nfc(" ".join(L)).lower() and not any(s.get("type") == "source" for s in spec.get("scenes", [])):
        bad.append("R10 có trích kinh nhưng không ghi 'diễn ý' (lời hoặc thẻ nguồn)")
    wv = tuple(spec.get("lint_waive") or ())   # miễn có ghi lý do trong spec (lint_waive_why), chỉ hạ thành cảnh báo
    if wv:
        W += [f"(miễn) {e}" for e in E if e.split()[0] in wv]
        E[:] = [e for e in E if e.split()[0] not in wv]
    return E, W


if __name__ == "__main__":
    rc = 0
    for slug in sys.argv[1:]:
        sp = json.loads((SPECS / f"{slug}.json").read_text(encoding="utf-8"))
        e, w = lint(slug, sp)
        print(f"{slug}: {len(e)} lỗi, {len(w)} cảnh báo")
        for x in e: print("  ERR ", x)
        for x in w: print("  warn", x)
        rc |= bool(e)
    sys.exit(rc)
