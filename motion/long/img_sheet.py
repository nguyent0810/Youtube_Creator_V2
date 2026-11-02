"""Tờ soát ảnh tĩnh của một video dài.

    python motion/long/img_sheet.py <topic>        # -> qa_imgs.jpg
    python motion/long/img_sheet.py <topic> --ok   # sau khi đã xem tờ
"""
import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from factory.console import utf8_console

ROOT = Path(__file__).resolve().parents[2]
W, H = 1920, 1080  # kích thước canvas của casewide.js
FONT_PATH = Path(r"C:\Windows\Fonts\arial.ttf")  # hỗ trợ tiếng Việt; font Long dùng Be Vietnam Pro.


def _font(size: int, bold=False):
    path = Path(r"C:\Windows\Fonts\arialbd.ttf") if bold else FONT_PATH
    return ImageFont.truetype(str(path), size)


def _focus(value):
    focus = value.get("focus")
    if isinstance(focus, (list, tuple)) and len(focus) == 2:
        return [float(focus[0]), float(focus[1])]
    return None


def image_uses(data: Path) -> list[dict]:
    """Ảnh cảnh dùng thật, gồm img và bg trùng key trong spec.imgs."""
    spec = json.loads((data / "spec.json").read_text(encoding="utf-8"))
    keys = set((spec.get("imgs") or {}).keys())
    uses = []

    def walk(value, chapter, index, scene_type):
        if isinstance(value, dict):
            for field in ("img", "bg"):
                key = value.get(field)
                if isinstance(key, str) and key in keys:
                    uses.append({"key": key, "focus": _focus(value), "chapter": chapter,
                                 "index": index, "type": scene_type, "field": field,
                                 "right": value.get("right"), "maxW": value.get("maxW"),
                                 "maxH": value.get("maxH"), "caption": value.get("caption")})
            for child in value.values():
                walk(child, chapter, index, scene_type)
        elif isinstance(value, list):
            for child in value:
                walk(child, chapter, index, scene_type)

    for f in sorted(data.glob("ch[0-9][0-9].json")):
        scenes = json.loads(f.read_text(encoding="utf-8")).get("scenes", [])
        for index, scene in enumerate(scenes):
            walk(scene, f.stem, index, str(scene.get("type", "scene")))
    return uses


def uses_hash(uses: list[dict]) -> str:
    """Chỉ băm key/focus theo hợp đồng QA; giữ số lần dùng để không bỏ sót cảnh mới."""
    items = sorted(({"key": u["key"], "focus": u["focus"]} for u in uses),
                   key=lambda x: (x["key"], json.dumps(x["focus"])))
    raw = json.dumps(items, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def ok_path(out: Path) -> Path:
    return out / "qa_imgs.ok"


def mark_ok(topic: str, data: Path | None = None, out: Path | None = None) -> Path:
    data = data or ROOT / "data" / "long" / topic
    out = out or ROOT / "output" / "long" / topic
    if not image_uses(data):
        raise SystemExit(f"{topic}: không có ảnh nào, không cần qa_imgs.ok")
    sheet = out / "qa_imgs.jpg"
    if not sheet.exists():
        raise SystemExit(f"thiếu {sheet} -- chạy python motion/long/img_sheet.py {topic}, xem tờ rồi mới thêm --ok")
    path = ok_path(out)
    path.write_text(uses_hash(image_uses(data)) + "\n", encoding="utf-8")
    print(f"{path}  (đã ghi dấu sau khi soát)")
    return path


def crop_box(size, focus=None):
    """Vùng 16:9 giống B.photo: cover rồi ghim focus vào giữa trong phạm vi ảnh."""
    width, height = size
    fx, fy = focus or (0.5, 0.4)
    scale = max(W / width, H / height)
    iw, ih = width * scale, height * scale
    left = min(0, max(W - iw, W / 2 - fx * iw))
    top = min(0, max(H - ih, H / 2 - fy * ih))
    return (-left / scale, -top / scale, (W - left) / scale, (H - top) / scale)


def _fit(im, size):
    copy = im.copy()
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, "#151922")
    canvas.paste(copy, ((size[0] - copy.width) // 2, (size[1] - copy.height) // 2))
    return canvas


def _crop_preview(im, focus, size=(320, 180)):
    box = crop_box(im.size, focus)
    return im.crop(tuple(round(x) for x in box)).resize(size, Image.Resampling.LANCZOS)


def _print_preview(im, scene, size=(320, 180)):
    """B.print: ảnh nguyên tỉ lệ, pad 20px, đặt bên trái/phải trong canvas 1920×1080."""
    page = Image.new("RGB", (W, H), "#24262b")
    page.paste(_fit(im, (W, H)).filter(ImageFilter.GaussianBlur(18)))
    max_w, max_h = scene.get("maxW") or 760, scene.get("maxH") or 700
    scale = min(max_w / im.width, max_h / im.height)
    iw, ih = round(im.width * scale), round(im.height * scale)
    pw, ph = iw + 40, ih + 40 + (50 if scene.get("caption") else 0)
    px0 = W - 130 - pw if scene.get("right") else 130
    py0 = max(110, round(470 - ph / 2))
    page.paste(im.resize((iw, ih), Image.Resampling.LANCZOS), (px0 + 20, py0 + 20))
    ImageDraw.Draw(page).rectangle((px0, py0, px0 + pw, py0 + ph), outline="#f1e6d2", width=8)
    return page.resize(size, Image.Resampling.LANCZOS)


def _image_path(out: Path, key: str) -> Path | None:
    for suffix in (".jpg", ".jpeg", ".png", ".webp"):
        path = out / "img" / f"{key}{suffix}"
        if path.exists():
            return path
    return None


def _text(draw, xy, text, font, fill, width):
    words, line, y = text.split(), "", xy[1]
    for word in words or [""]:
        candidate = (line + " " + word).strip()
        if line and draw.textbbox((0, 0), candidate, font=font)[2] > width:
            draw.text((xy[0], y), line, font=font, fill=fill)
            y += font.size + 6
            line = word
        else:
            line = candidate
    if line:
        draw.text((xy[0], y), line, font=font, fill=fill)
        y += font.size + 6
    return y


def render_sheet(topic: str, data: Path | None = None, out: Path | None = None) -> Path:
    data = data or ROOT / "data" / "long" / topic
    out = out or ROOT / "output" / "long" / topic
    uses = image_uses(data)
    if not uses:
        raise SystemExit(f"{topic}: không có ảnh nào trong ch*.json")
    grouped = defaultdict(list)
    for use in uses:
        grouped[use["key"]].append(use)
    cards = []
    for key in sorted(grouped):
        source = _image_path(out, key)
        if not source:
            raise SystemExit(f"thiếu ảnh {out / 'img' / (key + '.jpg')} -- chạy build_long.py {topic} html trước")
        with Image.open(source) as opened:
            im = opened.convert("RGB")
        variants = grouped[key]
        card_h = max(360, 72 + 196 * len(variants))
        card = Image.new("RGB", (1600, card_h), "#10151d")
        draw = ImageDraw.Draw(card)
        draw.rounded_rectangle((0, 0, 1599, card_h - 1), radius=18, outline="#394554", width=3)
        draw.text((28, 22), key, font=_font(34, True), fill="#f5f7fa")
        card.paste(_fit(im, (430, 242)), (28, 78))
        preview = im.copy(); preview.thumbnail((430, 242), Image.Resampling.LANCZOS)
        sx, sy = preview.width / im.width, preview.height / im.height
        px, py = 28 + (430 - preview.width) // 2, 78 + (242 - preview.height) // 2
        for n, use in enumerate(variants):
            if use["type"] == "print":
                draw.rectangle((px, py, px + preview.width, py + preview.height), outline="#fbbf24", width=3)
                continue
            x0, y0, x1, y1 = crop_box(im.size, use["focus"])
            color = (34 + n * 67 % 190, 211, 238)
            draw.rectangle((px + x0 * sx, py + y0 * sy, px + x1 * sx, py + y1 * sy), outline=color, width=3)
        draw.text((28, 330), "GỐC · khung màu = crop 16:9", font=_font(18), fill="#aebaca")
        for n, use in enumerate(variants):
            y = 28 + n * 196
            is_print = use["type"] == "print"
            tile = _print_preview(im, use) if is_print else _crop_preview(im, use["focus"])
            card.paste(tile, (500, y))
            draw.rectangle((500, y, 819, y + 179), outline="#fbbf24" if is_print else "#22d3ee", width=2)
            kind = "B.print · ảnh nguyên tỉ lệ" if is_print else "crop 16:9 thực tế"
            draw.text((850, y + 10), f"{use['chapter']}#{use['index']} · {use['type']} · {kind}", font=_font(23, True), fill="#f5f7fa")
            focus = "không cắt" if is_print else f"focus {use['focus'] or [0.5, 0.4]}"
            draw.text((850, y + 47), focus, font=_font(20), fill="#b8c5d6")
        where = ", ".join(f"{u['chapter']}#{u['index']}" for u in variants)
        types = ", ".join(sorted({u["type"] for u in variants}))
        _text(draw, (28, card_h - 46), f"DÙNG: {where} · LOẠI: {types} · {len(variants)} lần", _font(18), "#aebaca", 1530)
        cards.append(card)
    sheet = Image.new("RGB", (1600, 42 + sum(c.height + 18 for c in cards)), "#080b10")
    ImageDraw.Draw(sheet).text((28, 12), f"QA ẢNH · {topic} · {len(cards)} ảnh", font=_font(22, True), fill="#f5f7fa")
    y = 42
    for card in cards:
        sheet.paste(card, (0, y)); y += card.height + 18
    out.mkdir(parents=True, exist_ok=True)
    path = out / "qa_imgs.jpg"
    sheet.save(path, quality=92, subsampling=0)
    print(f"{path}  ({len(cards)} ảnh) -- soát crop / người / chữ đọc được / logo")
    return path


def main(argv=None):
    utf8_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic")
    parser.add_argument("--ok", action="store_true", help="ghi dấu sau khi đã xem tờ soát")
    args = parser.parse_args(argv)
    if args.ok:
        mark_ok(args.topic)
    else:
        render_sheet(args.topic)


if __name__ == "__main__":
    main()
