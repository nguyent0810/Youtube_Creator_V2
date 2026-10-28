"""Kênh Phật Giáo (BUD) -- hệ thống ĐA DẠNG cho short TikTok (09/10/2026).

Mục tiêu: chạy tự động, không ai duyệt từng video mà vẫn KHÔNG lặp khuôn.
  * 10 format (FORMATS), mỗi format có kiểu hook, nhịp (gap), độ dài, cảnh, màu nhấn, giọng, nhạc riêng.
  * Luật liền kề (RULES): hai video liên tiếp KHÔNG trùng format, kiểu hook, cảnh mở đầu, bài nhạc, giọng.
  * Luật cửa sổ: clip mở đầu không lặp trong 20 video gần nhất; mỗi bài nhạc chọn theo "lâu chưa dùng nhất".

Dùng ở 2 chỗ:
  1. build.py gọi apply(slug, spec) cho spec theme "bud": điền giọng / màu / gap / nhạc theo format,
     kiểm luật so với video BUD dựng ngay trước (sổ data/variety/bud_variety.json), vi phạm -> dừng dựng.
     Dựng lại CÙNG slug: giữ nguyên lựa chọn cũ (ra y hệt). Tắt kiểm: BUD_VARIETY=off (chỉ khi cố ý).
  2. python motion/stier/bud_variety.py check data/stier/tiktok_calendar_2026-11.json
     -> kiểm cả lịch đăng theo đúng thứ tự giờ đăng.
Spec BUD có thêm các khoá (build.py bỏ qua khoá lạ): "format", "hook_type", "open_shot", "music", "series".
Spec cũ không có "format" (vd. bud-phapcu-204-biet-du) được coi là "kinh-giai" và không bị chặn.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "data" / "variety" / "bud_variety.json"

# Nhạc MacLeod CC BY 4.0 có sẵn trong output/music -- chỉ bài chậm/êm, không trùng thư viện CK/MIM.
TRACKS = {
    "healing.mp3": "Healing", "at_rest.mp3": "At Rest", "clean_soul.mp3": "Clean Soul",
    "floating_cities.mp3": "Floating Cities", "fluidscape.mp3": "Fluidscape", "perspectives.mp3": "Perspectives",
    "frost_waltz.mp3": "Frost Waltz", "ether_vox.mp3": "Ether Vox", "arcadia.mp3": "Arcadia",
}

# Kiểu hook (3 giây đầu). Mỗi format chỉ dùng vài kiểu -> hook xoay vòng độc lập với format.
HOOKS = {
    "noi-dau": "câu hỏi chạm nỗi đau đời thường (Lương tăng mà vẫn thấy thiếu?)",
    "nghich-ly": "phát biểu ngược số đông (Buông bỏ KHÔNG phải là bỏ cuộc.)",
    "con-so": "con số cụ thể (3 điều / 2.500 năm / 1 câu)",
    "noi-thang": "nói thẳng với người xem (Nếu bạn đang...)",
    "do-vui": "đố người xem trả lời trước (Đoán xem: ...?)",
    "pov": "POV / đặt người xem vào tình huống (POV: bạn vừa bị chê...)",
    "dem-nguoc": "đếm ngược ngày âm (Còn 3 ngày nữa là Rằm...)",
    "vi-sao": "tò mò về biểu tượng (Vì sao tượng Phật...?)",
    "giua-truyen": "mở giữa câu chuyện (Một người mẹ ôm con đi khắp làng...)",
    "menh-lenh": "câu mệnh lệnh nhẹ (Dừng lướt 20 giây. Thở cùng mình.)",
}

# Nhóm cảnh mở đầu (scene 0). Liền kề không trùng nhóm.
OPEN_SHOTS = ["tien-bac", "pho-dem", "dien-thoai", "ban-tay", "hoa-sen", "tuong-phat", "nen-huong",
              "mat-nuoc", "rung-nui", "bau-troi", "nguoi-than", "cong-viec", "trang", "chu-tren-nen"]

FORMATS = {
    "kinh-giai": {"name": "Lời Kinh giải mã", "hooks": ["noi-dau", "nghich-ly", "con-so"],
                  "len": (25, 35), "words": (100, 132), "gap": 0.0, "accent": "#f5b041",
                  "voices": ["Ngọc Huyền", "Đoan Trang"], "music": ["healing.mp3", "clean_soul.mp3", "at_rest.mp3"],
                  "scenes": "kinetic 60% · slam ×2 (đảo nhịp) · quote ×1 (lời kệ diễn ý) · clip dưới mọi cảnh",
                  "pacing": "1 cảnh / câu (1,5–4 s), open loop ở giây ~7, trả lời ở câu kệ"},
    "chuyen-xua": {"name": "Chuyện xưa 60 giây (series, có số tập)", "hooks": ["giua-truyen", "pov", "noi-dau"],
                   "len": (35, 45), "words": (115, 135), "gap": 0.45, "accent": "#e07a5f",
                   "voices": ["Thiền Tâm Đức", "Thanh Bình", "Thục Đoan"],
                   "music": ["perspectives.mp3", "floating_cities.mp3", "fluidscape.mp3"],
                   "scenes": "clip 70% (chữ ngắn 1–3 từ) · slam ×1 ở cú xoay · quote ×1 ở bài học",
                   "pacing": "kể chậm, cảnh 3–5 s, cú xoay ở 60–70% thời lượng, kết bằng câu hỏi"},
    "hieu-lam": {"name": "Hiểu đúng – sai lầm phổ biến (series)", "hooks": ["nghich-ly", "do-vui", "menh-lenh"],
                 "len": (22, 32), "words": (85, 118), "gap": 0.0, "accent": "#ef8354",
                 "voices": ["Thiện Minh", "Đoan Trang", "Quang Sơn"],
                 "music": ["clean_soul.mp3", "arcadia.mp3", "floating_cities.mp3"],
                 "scenes": "slam 'SAI' ×1 + ledger ✓/✗ ×1 · kinetic nhanh · clip",
                 "pacing": "nhanh nhất kênh, cảnh 1,2–3 s, hiểu lầm → bằng chứng → hiểu đúng"},
    "nhan-gui": {"name": "Nếu bạn đang… (thư chữa lành)", "hooks": ["noi-thang", "pov"],
                 "len": (20, 30), "words": (60, 90), "gap": 0.5, "accent": "#f4a6b8",
                 "voices": ["Ngọc Linh", "Mỹ Duyên", "Ngọc Huyền"],
                 "music": ["healing.mp3", "at_rest.mp3", "ether_vox.mp3"],
                 "scenes": "clip 80% · kinetic chữ nhỏ · KHÔNG slam · quote ×1",
                 "pacing": "chậm, nghỉ giữa câu 0,5 s, 1 ý / câu, kết bằng lời mời lưu video"},
    "ba-dieu": {"name": "3–5 điều (danh sách đánh số)", "hooks": ["con-so", "menh-lenh", "noi-dau"],
                "len": (28, 38), "words": (110, 135), "gap": 0.15, "accent": "#ffb703",
                "voices": ["Thiện Minh", "Ngọc Trân", "Đoan Trang"],
                "music": ["arcadia.mp3", "frost_waltz.mp3", "clean_soul.mp3"],
                "scenes": "kinetic số lớn (1/2/3) mỗi điều · counter ×1 · slam ×1 điều cuối",
                "pacing": "mỗi điều 6–9 s, điều quan trọng nhất để CUỐI (giữ người xem)"},
    "do-vui": {"name": "Đố vui Phật pháp #N", "hooks": ["do-vui", "vi-sao"],
               "len": (20, 30), "words": (60, 95), "gap": 0.0, "accent": "#7fb7e8",
               "voices": ["Mỹ Duyên", "Thục Đoan", "Quang Sơn"],
               "music": ["frost_waltz.mp3", "arcadia.mp3", "floating_cities.mp3"],
               "scenes": "question ×1 (nhạc lặng) · counter 3-2-1 · slam đáp án · clip",
               "pacing": "câu đố ở 0 s, 3 phương án, đếm 3-2-1, đáp án + nguồn, mời comment đáp án"},
    "truoc-sau": {"name": "Trước / Sau khi hiểu", "hooks": ["pov", "nghich-ly", "noi-dau"],
                  "len": (22, 32), "words": (80, 115), "gap": 0.1, "accent": "#9ccc65",
                  "voices": ["Ngọc Trân", "Đoan Trang", "Thanh Bình"],
                  "music": ["clean_soul.mp3", "at_rest.mp3", "perspectives.mp3"],
                  "scenes": "split TRƯỚC|SAU ×2–3 · kinetic · quote nguồn",
                  "pacing": "3 cặp đối lập, mỗi cặp 6–8 s, cặp mạnh nhất cuối"},
    "lich-am": {"name": "Lịch âm & ngày vía (đếm ngược)", "hooks": ["dem-nguoc", "menh-lenh", "con-so"],
                "len": (20, 28), "words": (60, 95), "gap": 0.05, "accent": "#ffd166",
                "voices": ["Thục Đoan", "Ngọc Linh"],
                "music": ["frost_waltz.mp3", "at_rest.mp3", "ether_vox.mp3"],
                "scenes": "date ×1 (ngày dương + âm) · calendar/counter · kinetic · clip chùa/trăng",
                "pacing": "ngày âm ở 0 s, ý nghĩa có nguồn, 1 việc thiện cụ thể, KHÔNG xem ngày/bói toán"},
    "vi-sao": {"name": "Vì sao? – giải mã biểu tượng", "hooks": ["vi-sao", "do-vui"],
               "len": (20, 30), "words": (80, 112), "gap": 0.0, "accent": "#d4a373",
               "voices": ["Thiền Tâm Đức", "Quang Sơn", "Thanh Bình"],
               "music": ["ether_vox.mp3", "perspectives.mp3", "fluidscape.mp3"],
               "scenes": "clip cận biểu tượng · kinetic · slam ý nghĩa · quote nguồn",
               "pacing": "câu hỏi 0 s, đoán sai phổ biến, ý nghĩa thật + nguồn, liên hệ đời sống"},
    "tinh-lang": {"name": "Tĩnh lặng 30 giây (thở / âm thanh chùa)", "hooks": ["menh-lenh", "noi-thang"],
                  "len": (38, 48), "words": (55, 75), "gap": 1.6, "accent": "#b8c4a8",
                  "voices": ["Ngọc Huyền", "Ngọc Linh"],
                  "music": ["fluidscape.mp3", "ether_vox.mp3", "healing.mp3"],
                  "scenes": "clip 100% (nước, nến, lá, chuông) · chữ nhỏ hướng dẫn thở · KHÔNG slam",
                  "pacing": "rất chậm, nghỉ 1,6 s giữa 14–16 câu rất ngắn, dẫn hít-thở theo MN 118, kết mời lưu để dùng lại"},
}

RULES = [
    "Hai video liên tiếp (theo giờ đăng) KHÔNG trùng: format, kiểu hook, nhóm cảnh mở đầu, bài nhạc, giọng đọc.",
    "Không 2 video cùng format trong một ngày; mỗi format tối đa 3 lần trong 7 ngày liên tiếp.",
    "Clip Pexels mở đầu không lặp lại trong 20 video gần nhất; clip bất kỳ không dùng lại trong 6 video gần nhất.",
    "Nhạc: chọn trong danh sách của format, bỏ bài vừa dùng, ưu tiên bài lâu chưa dùng nhất.",
    "Giọng: chọn trong danh sách của format, bỏ giọng vừa dùng.",
    "Độ dài 20–48 s theo khoảng của format (ước tính ~4 từ/giây + gap × số câu); số từ trong khoảng 'words' của format (build.py vẫn giữ 55–135).",
    "Nội dung: có nguồn (SuttaCentral / nguồn Phật giáo uy tín), ghi 'diễn ý' khi diễn giải, không mê tín/bói toán, "
    "không xưng là tu sĩ.",
]


def _load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {"builds": []}


def _first_clip(spec: dict) -> str | None:
    sc = spec.get("scenes") or []
    return sc[0].get("clip") if sc else None


def _clips(spec: dict) -> list[str]:
    return [s["clip"] for s in spec.get("scenes") or [] if s.get("clip")]


def _pick(options: list[str], avoid: str | None, history: list[str]) -> str:
    ok = [o for o in options if o != avoid] or options
    last = {v: i for i, v in enumerate(history)}
    return min(ok, key=lambda o: (last.get(o, -1), ok.index(o)))


def check_pair(prev: dict, cur: dict) -> list[str]:
    """Các vi phạm luật liền kề giữa 2 mục (spec hoặc mục lịch) -- dùng chung cho build và lịch."""
    bad = []
    for k in ("format", "hook_type", "open_shot", "music", "voice"):
        if prev.get(k) and cur.get(k) and prev[k] == cur[k]:
            bad.append(f"trùng {k} = {cur[k]!r} với video liền trước ({prev.get('slug')})")
    return bad


def apply(slug: str, spec: dict) -> dict:
    """Điền mặc định theo format + kiểm luật so với video BUD dựng trước. Trả spec (đã điền)."""
    if "format" not in spec:   # spec cũ (trước hệ thống đa dạng): giữ nguyên, không đổi giọng/nhạc -> dựng lại y hệt
        print(f"  [bud_variety] {slug}: spec không có 'format' -- giữ nguyên, không kiểm luật", flush=True)
        return spec
    fmt_name = spec["format"]
    if fmt_name not in FORMATS:
        raise SystemExit(f"{slug}: format lạ {fmt_name!r} (có: {', '.join(FORMATS)})")
    fmt = FORMATS[fmt_name]
    led = _load()
    builds = led["builds"]
    mine = next((b for b in builds if b["slug"] == slug), None)
    before = builds[:builds.index(mine)] if mine else builds
    prev = before[-1] if before else {}
    spec = dict(spec)
    spec.setdefault("accent", fmt["accent"])
    spec.setdefault("gap", fmt["gap"])
    if "voice" not in spec:
        spec["voice"] = mine["voice"] if mine else _pick(fmt["voices"], prev.get("voice"), [b.get("voice") for b in before])
    if spec.get("music") not in TRACKS:
        spec["music"] = mine["music"] if mine and mine.get("music") in TRACKS else \
            _pick(fmt["music"], prev.get("music"), [b.get("music") for b in before])
    if "hook_type" in spec and spec["hook_type"] not in fmt["hooks"]:
        raise SystemExit(f"{slug}: hook {spec['hook_type']!r} không thuộc format {fmt_name} ({fmt['hooks']})")
    rec = {"slug": slug, "format": spec["format"], "hook_type": spec.get("hook_type"), "open_shot": spec.get("open_shot"),
           "music": spec["music"], "voice": spec["voice"], "first_clip": _first_clip(spec), "clips": _clips(spec)}
    bad = check_pair(prev, rec) if prev else []
    recent = before[-20:]
    if rec["first_clip"] and any(b.get("first_clip") == rec["first_clip"] for b in recent):
        bad.append(f"clip mở đầu {rec['first_clip']} đã mở đầu 1 video trong 20 video gần nhất")
    reused = {c for b in before[-6:] for c in b.get("clips", [])} & set(rec["clips"])
    if reused:
        bad.append(f"clip dùng lại trong 6 video gần nhất: {sorted(reused)}")
    if bad and os.environ.get("BUD_VARIETY", "").lower() != "off" and not mine:
        raise SystemExit(f"{slug}: vi phạm luật đa dạng BUD:\n  - " + "\n  - ".join(bad)
                         + "\n(sửa spec; cố ý bỏ qua: đặt BUD_VARIETY=off)")
    for m in bad:
        print(f"  [bud_variety] cảnh báo: {m}", flush=True)
    if mine:
        builds[builds.index(mine)] = rec
    else:
        builds.append(rec)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1), encoding="utf-8")
    return spec


def check_calendar(path: str) -> int:
    cal = json.loads(Path(path).read_text(encoding="utf-8"))
    items = sorted(cal["entries"], key=lambda e: (e["date"], e["time"]))
    prev, bad, days = cal.get("seed_previous") or {}, 0, {}
    for e in items:
        for m in check_pair(prev, e):
            print(f"{e['date']} {e['time']} {e['slug']}: {m}"); bad += 1
        f = FORMATS.get(e["format"])
        if not f:
            print(f"{e['slug']}: format lạ {e['format']}"); bad += 1; continue
        if e["hook_type"] not in f["hooks"]:
            print(f"{e['slug']}: hook {e['hook_type']} không thuộc {e['format']}"); bad += 1
        if e["voice"] not in f["voices"] or e["music"] not in f["music"]:
            print(f"{e['slug']}: giọng/nhạc ngoài danh sách format"); bad += 1
        days.setdefault(e["date"], []).append(e["format"])
        prev = e
    for d, fs in days.items():
        if len(fs) != len(set(fs)):
            print(f"{d}: 2 video cùng format"); bad += 1
    from datetime import date, timedelta
    ds = sorted(days)
    for d in ds:
        d0 = date.fromisoformat(d)
        win = [f for x in ds if 0 <= (date.fromisoformat(x) - d0).days < 7 for f in days[x]]
        for f in set(win):
            if win.count(f) > 3:
                print(f"7 ngày từ {d}: format {f} xuất hiện {win.count(f)} lần (>3)"); bad += 1
    print(f"{len(items)} mục, {bad} vi phạm")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "check":
        raise SystemExit(check_calendar(sys.argv[2]))
    print(__doc__)
    for k, f in FORMATS.items():
        print(f"{k:11s} {f['len'][0]}-{f['len'][1]}s  hooks={f['hooks']}  voices={f['voices']}  music={f['music']}")
