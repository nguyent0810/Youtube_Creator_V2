"""Cổng CHẤT LƯỢNG cho video dài, chặn trước khi render (26/10/2026, sau thử nghiệm Codex T1/T1b).

    python scripts/long_gate.py <topic> [--min-syl 1900]

`studio_lint` chỉ bắt lỗi kỹ thuật. Bài T1b (5 phút, một clip máy đánh chữ lặp 8 lần) vẫn ra "0 lỗi".
Cổng này đo những thứ review đã phải bắt bằng mắt. Ngưỡng đặt theo bài mẫu:
- Petrov: 7,6 giây/cảnh, ít nhất 7 loại cảnh/chương.
- KAL 007: 7,7 giây/cảnh, ít nhất 6 loại cảnh/chương.
Thoát 1 khi có LỖI.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYL_PER_MIN = 210                      # nhịp đọc đo trên các Long MIM (docs/pm/2026-10-23-mim-long-moi.md)
MAX_SEC_PER_SCENE = 9.0
MIN_TYPES_PER_CHAPTER = 5
MAX_SAME_CLIP = 2                      # bài 9–12 phút; bài dài hơn cho phép ~1 lần lặp mỗi 6 phút (Petrov 22 phút: 4)
MAX_SAME_IMAGE = 3
# Câu đệm thêm vào chỉ để qua tỉ lệ câu ngắn của lint (review T1, 26/10/2026)
FILLER = ["Rất chậm.", "Không có thời gian chờ.", "Mâu thuẫn là dấu hiệu tốt.", "Không hề tức thì.",
          "Đó là lợi thế lớn.", "Việc ấy rất cụ thể.", "Đó là câu hỏi khó.", "Phần còn lại mới đáng xem.",
          "Nó chỉ mở cửa.", "Họ không vô hình.", "Không chỉ nhờ ý tưởng."]
BANNED_PUBLIC = ["<", ">", "CẦN", "cần kiểm", "WebFetch", "factcheck", "data/long", "tìm kiếm", "agent"]


def text_of(line) -> str:
    return line if isinstance(line, str) else str(line.get("t", ""))


def gate(topic: str, min_syl: int) -> tuple[list[str], list[str], dict]:
    d = ROOT / "data" / "long" / topic
    od = ROOT / "output" / "long" / topic
    err, warn = [], []
    chs = sorted(d.glob("ch*.json"))
    if not chs:
        return [f"không có chNN.json trong {d}"], [], {}
    syl, dur, scenes = 0, 0.0, 0
    no_tts = []
    clips, images = collections.Counter(), collections.Counter()
    for f in chs:
        ch = json.loads(f.read_text(encoding="utf-8"))
        if not (ch.get("hud") or {}).get("t"):      # T2D: thiếu hud -> describe.py KeyError, mô tả không có danh sách chương
            err.append(f"{f.stem}: thiếu hud {{k, t}} (describe.py lấy tiêu đề chương từ đây)")
        syl +=sum(len(text_of(x).split()) for x in ch.get("lines", []))
        body = [s for s in ch.get("scenes", []) if s.get("type") not in ("chapter", "brand", "endcard")]
        scenes += len(body)
        kinds = {s["type"] for s in body}
        if len(kinds) < MIN_TYPES_PER_CHAPTER:
            err.append(f"{f.stem}: chỉ {len(kinds)} loại cảnh {sorted(kinds)}; cần >= {MIN_TYPES_PER_CHAPTER}")
        for s in body:
            if s.get("vid"):
                clips[str(s["vid"])] += 1
            for k in ("img", "photo", "src"):
                if isinstance(s.get(k), str):
                    images[s[k]] += 1
        tj = od / f.stem / "timing.json"
        if tj.exists():
            dur += json.loads(tj.read_text(encoding="utf-8"))["duration"]
        else:
            no_tts.append(f.stem)
    # T2B render (26/10/2026): thẻ chương ghi "number" thay vì "no"/"k" -> engine in chữ "undefined" giữa màn hình;
    # gen_scenes dùng một khuôn 9 cảnh cho mọi chương -> "SÁU RĂNG CỦA MỘT KHÓA" hiện 7 lần. Lint đếm loại cảnh không thấy.
    # T5W2 (26/10/2026): cảnh map gọi ghim "Harvard" nhưng spec.geo chỉ có "Cambridge, Massachusetts" -> engine lỗi,
    # cả chương 2 đứng hình 72 giây ở thẻ chương. Ghim của cảnh phải có trong spec.geo[geo].pins.
    geo_spec = (json.loads((d / "spec.json").read_text(encoding="utf-8")).get("geo") or {}) if (d / "spec.json").exists() else {}
    for f in chs:
        for s in json.loads(f.read_text(encoding="utf-8")).get("scenes", []):
            if s.get("type") == "map" and s.get("geo"):
                g = geo_spec.get(s["geo"])
                if g is None:
                    err.append(f"{f.stem}: map geo '{s['geo']}' không có trong spec.geo")
                    continue
                names = {p.get("name") for p in g.get("pins", [])}
                for p in s.get("pins", []):
                    if p.get("name") not in names:
                        err.append(f"{f.stem}: ghim '{p.get('name')}' không có trong spec.geo['{s['geo']}'] {sorted(names)}")
    # T6W2 (27/10/2026): ảnh dọc của Jobs cắt giữa thành 16:9 -> chỉ còn vest và tay. Ảnh dọc cần "focus" [x, y].
    try:
        from PIL import Image
        for f in chs:
            for s in json.loads(f.read_text(encoding="utf-8")).get("scenes", []):
                k = s.get("img") if s.get("type") in ("photo", "chapter") else None
                k = k or (s.get("bg") if s.get("type") == "chapter" else None)
                p = od / "img" / f"{k}.jpg" if k else None
                if p and p.exists() and "focus" not in s:
                    with Image.open(p) as im:
                        if im.size[1] > im.size[0] * 1.15:
                            warn.append(f"{f.stem}: ảnh dọc '{k}' {im.size[0]}x{im.size[1]} không có focus -- dễ cắt mất mặt")
    except ImportError:
        pass
    seen = collections.Counter()
    for f in chs:
        for s in json.loads(f.read_text(encoding="utf-8")).get("scenes", []):
            if s.get("type") == "chapter":
                miss = [k for k in ("no", "k", "title") if not s.get(k)]
                if miss:
                    err.append(f"{f.stem}: thẻ chương thiếu {miss} (engine hiện 'undefined'; xem mẫu Petrov)")
                continue
            keys = ("text", "q", "label") if s.get("type") == "ledger" else ("text", "title", "q", "label")   # tiêu đề sổ cái là mô-típ (Petrov "GHẾ TRỰC"), dòng mới thì khác
            texts = [s.get(k) for k in keys if isinstance(s.get(k), str)]
            texts += [i.get("text") for i in s.get("items") or [] if isinstance(i, dict) and isinstance(i.get("text"), str)]
            for t in texts:
                if len(t) >= 8:
                    seen[t.strip().upper()] += 1
    # T4W2 (26/10/2026): "PAUL DEP ODESTA" -- tên riêng bị chèn dấu cách trên màn hình. So với khoá SAY (tên đã biết).
    say_keys = [k.lstrip("=").upper() for k in (json.loads((d / "spec.json").read_text(encoding="utf-8")).get("say") or {})
                if (d / "spec.json").exists()] if (d / "spec.json").exists() else []
    for t in seen:
        for k in say_keys:
            if len(k) >= 6 and k.isalpha() and k not in t and k in t.replace(" ", ""):
                err.append(f"tên '{k}' bị tách trên màn hình: {t[:50]!r}")
    for t, n in seen.items():
        if n > 2:
            err.append(f"chữ hiển thị lặp {n} lần: {t[:50]!r} (mỗi cảnh phải gắn với dữ kiện của chương đó)")
    if no_tts:
        # T4W2 (26/10/2026): TTS mới chạy 3/8 chương -> cộng thiếu thời lượng, "2,7 giây/cảnh" ĐẠT giả
        err.append(f"chưa TTS: {no_tts} -- chạy build_long.py <topic> tts cho đủ")
        dur = syl / SYL_PER_MIN * 60
    if syl < min_syl:
        err.append(f"lời đọc {syl} âm tiết (~{syl / SYL_PER_MIN:.1f} phút) < {min_syl}: thiếu nội dung, thêm chi tiết có nguồn, không thêm câu đệm")
    sps = dur / max(scenes, 1)
    if sps > MAX_SEC_PER_SCENE:
        err.append(f"{sps:.1f} giây/cảnh > {MAX_SEC_PER_SCENE}: cần thêm cảnh (bài mẫu ~7,6)")
    cap = max(MAX_SAME_CLIP, round(dur / 60 / 6))
    for v, n in clips.items():
        if n > cap:
            err.append(f"clip {v} dùng {n} lần (> {cap})")
    for v, n in images.items():
        if n > MAX_SAME_IMAGE:
            err.append(f"ảnh {v} dùng {n} lần (> {MAX_SAME_IMAGE})")
    script = (d / "script.md").read_text(encoding="utf-8") if (d / "script.md").exists() else ""
    fc = (d / "factcheck.md").read_text(encoding="utf-8") if (d / "factcheck.md").exists() else ""
    for x in FILLER:
        if x in script:
            err.append(f"câu đệm rỗng nghĩa: {x!r}")
    # T5W1 (26/10/2026): lời đọc "Kho nguồn không có xác nhận…" -- ghi chú làm việc lọt vào câu đọc
    spoken = "\n".join(text_of(x) for f in chs for x in json.loads(f.read_text(encoding="utf-8")).get("lines", []))
    for x in re.findall(r"(?i)\b(kho nguồn|trong kho|kho dữ kiện|facts\.md|factcheck|độ tin mạnh)\b", spoken):
        err.append(f"lời đọc lộ ghi chú nội bộ: {x!r}")
    body_lines = [ln for ln in script.splitlines() if ln and not ln.startswith(("#", "**", "Quy ước", "---"))]
    missing = set()
    for ln in body_lines:
        for y in re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", ln):           # năm phải có trong factcheck
            if y not in fc:
                missing.add(y)
    if missing:
        err.append(f"năm trong kịch bản không có trong factcheck.md: {sorted(missing)}")
    if len(re.findall(r"https?://", fc)) < 8:
        err.append("factcheck.md có ít hơn 8 URL nguồn")
    spec = json.loads((d / "spec.json").read_text(encoding="utf-8")) if (d / "spec.json").exists() else {}
    pub = json.dumps({k: v for k, v in (spec.get("youtube") or {}).items() if k != "sources_internal"}, ensure_ascii=False)
    bad = [b for b in BANNED_PUBLIC if b in pub]
    if bad:
        err.append(f"spec.youtube (công khai) chứa chuỗi cấm: {bad}")
    yt = spec.get("youtube") or {}
    # T2B (26/10/2026): spec.youtube chỉ có titles/summary/2 nguồn -> mô tả công khai trống, không hẹn giờ, không playlist
    lack = [k for k in ("publish_at", "playlist", "chapter_titles", "tags", "video_credits") if not yt.get(k)]
    if lack:
        err.append(f"spec.youtube thiếu {lack} (xem mẫu mim-ke-huy-diet-petrov)")
    if len(yt.get("sources") or []) < 8:
        err.append(f"spec.youtube.sources chỉ {len(yt.get('sources') or [])} URL công khai (< 8)")
    # Tên nước ngoài không có bảng phát âm: giọng Việt đọc thô "Welchman", "Bletchley" (T2B: 0 mục say cho ~40 tên)
    foreign = set()
    for f in chs:
        for x in json.loads(f.read_text(encoding="utf-8")).get("lines", []):
            foreign |= {w for w in re.findall(r"\b[A-Z][a-zA-Z\-]{2,}\b", text_of(x)) if w.isascii()}
    if len(foreign) >= 8 and not spec.get("say"):
        err.append(f"{len(foreign)} tên/thuật ngữ nước ngoài trong lời đọc mà spec không có bảng say")
    title = (yt.get("titles") or [spec.get("title", "")])[0]
    if len(title) > 60:
        err.append(f"tiêu đề {len(title)} ký tự > 60")
    stats = {"âm tiết": syl, "phút": round(dur / 60, 1), "cảnh": scenes, "giây/cảnh": round(sps, 1),
             "clip khác": len(clips), "ảnh khác": len(images), "URL nguồn": len(re.findall(r"https?://", fc))}
    return err, warn, stats


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--min-syl", type=int, default=1900)
    a = ap.parse_args()
    err, warn, stats = gate(a.topic, a.min_syl)
    print(f"{a.topic}: " + ", ".join(f"{k} {v}" for k, v in stats.items()))
    for w in warn:
        print(f"  cảnh báo: {w}")
    for e in err:
        print(f"  LỖI: {e}")
    print("ĐẠT" if not err else f"TRƯỢT ({len(err)} lỗi)")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
