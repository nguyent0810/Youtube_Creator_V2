"""Thư viện "look" cho Short phối (MIM/CK) -- để các Short KHÔNG một màu (chủ kênh, 12/10/2026).

Một look = một bộ lựa chọn trình bày đi cùng nhau: kiểu bảng vẽ, kiểu thẻ 3D, hình dạng cửa sổ video, kiểu xếp chữ động,
bộ chuyển cảnh. Màu nhấn và giọng vẫn theo kênh (nhận diện kênh không đổi); thứ đổi là CÁCH trình bày.

    spec "look": "chalk"        -> ép look (khi nội dung hợp một kiểu, vd. bài "giải thích cơ chế" hợp bảng phấn)
    không ghi                   -> look lâu chưa dùng nhất của kênh (sổ data/variety/short_looks.json), dựng lại ra y hệt

Sổ còn ghi "chữ ký" chuỗi cảnh (vd. "M G M D G M G"); resolve() trả cảnh báo khi Short mới trùng look HOẶC trùng chữ ký
với một trong 3 Short gần nhất của kênh -- đổi thứ tự/loại cảnh theo nội dung, đừng rập khuôn.

Gợi ý chọn cảnh theo nội dung: RECIPES (không ép; luật cứng là mix_lint trong build.py).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "data" / "variety" / "short_looks.json"

# board: paper (giấy trắng, bút dạ) · chalk (bảng phấn xanh) · blueprint (bản vẽ kỹ thuật) · lined (vở kẻ ngang) · glass (kính tối)
# cards: glass (kính mờ) · solid (khối màu, bóng cứng) · wire (khung nét đứt) · index (thẻ giấy) · gradient (chuyển màu)
# win:   top (khung bo góc nửa trên) · tilt (ảnh lấy liền, nghiêng) · band (dải ngang điện ảnh) · circle (ô tròn)
# kin:   stack (xếp giữa) · left (canh trái + vạch nhấn) · tilt (cả khối nghiêng nhẹ)
# tr:    whip (lia nhoè) · zoom (đẩy vào) · up (trượt lên) · flash (chớp sáng) · swipe (kéo rèm)
LOOKS = {
    "lab":       {"board": "paper",     "cards": "glass",    "win": "top",    "kin": "stack", "tr": ["whip", "zoom"]},
    "chalk":     {"board": "chalk",     "cards": "solid",    "win": "tilt",   "kin": "tilt",  "tr": ["up", "flash"]},
    "blueprint": {"board": "blueprint", "cards": "wire",     "win": "band",   "kin": "left",  "tr": ["zoom", "swipe"]},
    "notebook":  {"board": "lined",     "cards": "index",    "win": "circle", "kin": "stack", "tr": ["swipe", "up"]},
    "neon":      {"board": "glass",     "cards": "gradient", "win": "top",    "kin": "left",  "tr": ["flash", "whip"]},
    "studio":    {"board": "paper",     "cards": "solid",    "win": "band",   "kin": "tilt",  "tr": ["whip", "up"]},
    "archive":   {"board": "lined",     "cards": "glass",    "win": "tilt",   "kin": "stack", "tr": ["zoom", "flash"]},
    "terminal":  {"board": "blueprint", "cards": "gradient", "win": "circle", "kin": "left",  "tr": ["swipe", "whip"]},
}

# Ô cửa sổ video theo kiểu "win": (x, y, rộng, cao) trên khung 1080x1920 -- PHẢI khớp bảng G trong casefile.js (cảnh có "win").
WIN = {"top": (56, 215, 968, 795), "tilt": (120, 250, 840, 730), "band": (0, 330, 1080, 600), "circle": (150, 220, 780, 780)}

# Nội dung -> chuỗi cảnh gợi ý (T chữ · M ảnh/video · D số liệu · G sơ đồ/3D). Người viết spec chọn rồi biến tấu.
RECIPES = {
    "so-sanh":    "hook(M) · cards3d(G) · chart(D) · photo/clip(M) · board(G)",
    "co-che":     "hook(M) · board(G) · clip cửa sổ(M) · counter(D) · board(G)",
    "con-so":     "hook(M) · counter(D) · chart(D) · board(G) · clip(M)",
    "dong-thoi-gian": "hook(M) · photo(M) · timeline(D) · board(G) · cards3d(G)",
    "lam-tuong":  "hook(M) · board gạch chéo(G) · chart(D) · photo(M) · slam trên clip(M)",
    "ban-do":     "hook(M) · map(G) · counter(D) · photo(M) · cards3d(G)",
}


def _load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {"picks": []}


def resolve(spec: dict, slug: str, channel: str, signature: str) -> tuple[str, dict, list[str]]:
    """(tên look, tham số, cảnh báo). Ghi sổ ngay (dựng tuần tự như sổ nhạc)."""
    led = _load()
    mine = [p for p in led["picks"] if p["channel"] == channel]
    prev = next((p for p in mine if p["slug"] == slug), None)
    others = [p for p in mine if p["slug"] != slug]
    name = spec.get("look") or (prev and prev["look"])
    if name and name not in LOOKS:
        raise SystemExit(f"look lạ {name!r} (có: {', '.join(LOOKS)})")
    if not name:
        last = {p["look"]: i for i, p in enumerate(others)}
        name = min(LOOKS, key=lambda k: (last.get(k, -1), list(LOOKS).index(k)))
    warn = []
    recent = others[-3:]
    if any(p["look"] == name for p in recent[-2:]):
        warn.append(f"look {name!r} trùng với 1 trong 2 Short gần nhất của kênh {channel}")
    if any(p.get("sig") == signature for p in recent):
        warn.append(f"chuỗi cảnh {signature!r} trùng với 1 trong 3 Short gần nhất của kênh {channel} -- đổi thứ tự/loại cảnh")
    if prev:
        prev.update(look=name, sig=signature)
    else:
        led["picks"].append({"channel": channel, "slug": slug, "look": name, "sig": signature})
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1), encoding="utf-8")
    return name, LOOKS[name], warn
