"""Bốn kiểm tra cơ học chạy trước render (bước html và render).

Bắt lỗi từng phải soi contact sheet mới thấy:

- thẻ ``file`` có con dấu mà không bật ``stamp.ink`` — trên giấy ``mix-blend-mode: screen`` làm nhạt mực;
- con dấu (kể cả khi xoay) tràn ra ngoài thẻ giấy;
- tiêu đề thẻ ``name`` rộng hơn lòng thẻ ở cỡ chữ engine sẽ chọn, nên tự xuống dòng;
- clip B-roll HDR (PQ, HLG, hoặc primaries/matrix bt.2020) — lỗi màu của tập Thượng Hải.

Số đo bám ``casewide.css`` / ``casewide.js``: thẻ 1000×tối thiểu 600, padding 54/64,
lòng chữ 872px; con dấu padding 10/34, viền 10, ``letter-spacing: .04em``.
Cỡ chữ dùng cùng công thức ``fsz`` của engine. Bề rộng chữ đo trên font thật
(Playfair Display 900 cho tiêu đề, Be Vietnam Pro Black cho con dấu).
"""
from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

FONT_DIR = Path(__file__).resolve().parent / "fonts"

# Thẻ giấy .fcard — box-sizing: border-box, nghỉ ở rotation 1.5° quanh mép dưới.
CARD_W = 1000.0
CARD_TOP = 150.0
CARD_MIN_H = 600.0
CARD_LEFT_WITH_IMG = 760.0
CARD_LEFT_PLAIN = 460.0
CARD_PAD_X = 64.0
CARD_PAD_Y = 54.0
CARD_INNER_W = CARD_W - 2 * CARD_PAD_X  # 872
CARD_REST_ROT = 1.5
# casewide.js: thẻ phóng 1 → 1.03 từ t0+0.6 cho tới hết cảnh. Con dấu chỉ cần nằm trong thẻ lúc nó đã đóng.
CARD_SCALE_END = 1.03

# Tiêu đề .fcard .n — fsz(longest, 100, 860, 0.58), line-height 1, Playfair 900.
NAME_MAX = 100
NAME_TRACK = 860
NAME_K = 0.58
NAME_MARGIN_TOP = 26.0
TITLE_SLACK_PX = 4.0  # dưới một nét chữ: trình duyệt không xuống dòng

# Con dấu .stamp — fsz(text, 84, 760, 0.72). Toạ độ là mép trên-trái trên sân khấu 1920×1080.
STAMP_MAX = 84
STAMP_TRACK = 760
STAMP_K = 0.72
STAMP_PAD_X = 34.0
STAMP_PAD_Y = 10.0
STAMP_BORDER = 10.0
STAMP_TRACKING = 0.04
STAMP_DEFAULT_X = 1150.0
STAMP_DEFAULT_Y = 560.0
STAMP_DEFAULT_ROT = -8.0

# HDR: PQ / HLG, hoặc không gian bt.2020. bt709, unknown, smpte170m, bt470bg là SDR.
HDR_TRANSFER = {"smpte2084", "arib-std-b67"}
HDR_PRIMARIES = {"bt2020"}
HDR_MATRIX = {"bt2020nc", "bt2020c"}

# Khung bo góc + làm tròn subpixel. Frame đã duyệt của Tam Giác Vàng lệch mô hình khoảng 3px
# mà mắt vẫn thấy con dấu nằm trong thẻ. Lỗi thật (con dấu mặc định) lệch hơn 100px.
_OUTSIDE_PX = 4.0


def fsz(text: str, max_px: float, width: float, k: float) -> int:
    """Cùng công thức ``fsz`` trong casewide.js: co chữ để ước lượng ``width`` theo ``k`` em/ký tự."""
    n = max(1, len(text))
    return int(min(max_px, math.floor(width / (n * k))))


@lru_cache(maxsize=64)
def _playfair(px: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(FONT_DIR / "PlayfairDisplay-wght.ttf"), px)
    font.set_variation_by_axes([900])
    return font


@lru_cache(maxsize=64)
def _sans(px: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / "BeVietnamPro-Black.ttf"), px)


def _advance(text: str, font: ImageFont.FreeTypeFont, px: int, tracking_em: float = 0.0) -> float:
    w = float(font.getlength(text))
    if tracking_em and len(text) > 1:
        w += (len(text) - 1) * tracking_em * px
    return w


def _line_box(font: ImageFont.FreeTypeFont) -> float:
    ascent, descent = font.getmetrics()
    return float(ascent + descent)


def _num(value, default: float) -> float:
    return default if value is None else float(value)


def card_size(scene: dict) -> tuple[float, float, float, float]:
    """(left, top, width, height) của thẻ giấy trước khi xoay 1.5°."""
    left = CARD_LEFT_WITH_IMG if scene.get("img") else CARD_LEFT_PLAIN
    name = scene.get("name") or ""
    lines = name.split("\n")
    longest = max(lines, key=len) if lines else ""
    fs = fsz(longest, NAME_MAX, NAME_TRACK, NAME_K) if name else NAME_MAX
    height = CARD_PAD_Y
    height += 22 * 1.2  # nhãn .k, JetBrains Mono
    height += NAME_MARGIN_TOP + fs * max(1, len(lines))
    if scene.get("desc"):
        row = _line_box(_sans(30))
        desc_w = _advance(scene["desc"], _sans(30), 30)
        height += 18 + row * max(1, math.ceil(desc_w / CARD_INNER_W - 1e-6))
    height += 28 + 3  # gạch .ln
    row_h = _line_box(_sans(30))
    for _row in scene.get("rows") or []:
        height += 18 + row_h
    height += CARD_PAD_Y
    return left, CARD_TOP, CARD_W, max(CARD_MIN_H, height)


def stamp_size(stamp: dict) -> tuple[float, float, float, float, float]:
    """(left, top, width, height, rot độ) của khung con dấu, tính cả padding và viền."""
    text = stamp.get("text") or ""
    fs = fsz(text, STAMP_MAX, STAMP_TRACK, STAMP_K)
    text_w = _advance(text, _sans(fs), fs, STAMP_TRACKING)
    width = text_w + STAMP_PAD_X * 2 + STAMP_BORDER * 2
    # Khung đo trên frame đã duyệt (ch09 “TỪ CHỐI”): line box xấp xỉ đúng font-size,
    # không phải ascent+descent của rasterizer (cái đó cao hơn ~23px).
    height = fs + STAMP_PAD_Y * 2 + STAMP_BORDER * 2
    return (
        _num(stamp.get("x"), STAMP_DEFAULT_X),
        _num(stamp.get("y"), STAMP_DEFAULT_Y),
        width,
        height,
        _num(stamp.get("rot"), STAMP_DEFAULT_ROT),
    )


def _css_rotate(x: float, y: float, cx: float, cy: float, deg: float) -> tuple[float, float]:
    """Xoay theo CSS: độ dương là chiều kim đồng hồ, trục y hướng xuống."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    dx, dy = x - cx, y - cy
    return cx + dx * c - dy * s, cy + dx * s + dy * c


def _rect_corners(x: float, y: float, w: float, h: float) -> list[tuple[float, float]]:
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def _card_scale(scene: dict, stamp: dict) -> float:
    t0, t1, at = scene.get("t0"), scene.get("t1"), stamp.get("at")
    if not all(isinstance(v, (int, float)) for v in (t0, t1, at)):
        return 1.0
    dur = max(0.2, float(t1) - float(t0) - 0.6)
    u = min(1.0, max(0.0, (float(at) - (float(t0) + 0.6)) / dur))
    return 1.0 + (CARD_SCALE_END - 1.0) * u


def _card_poly(left: float, top: float, w: float, h: float, scale: float = 1.0) -> list[tuple[float, float]]:
    # Phóng quanh mép dưới (transform-origin 50% 100%) rồi mới xoay 1.5°.
    cx, bottom = left + w / 2, top + h
    w, h = w * scale, h * scale
    left, top = cx - w / 2, bottom - h
    return [_css_rotate(px, py, cx, bottom, CARD_REST_ROT) for px, py in _rect_corners(left, top, w, h)]


def _stamp_points(x: float, y: float, w: float, h: float, rot: float, radius: float = 16.0) -> list[tuple[float, float]]:
    """Mép ngoài của con dấu bo góc 16px: giữa bốn cạnh và đỉnh cung, không phải góc vuông."""
    r = min(radius, w / 2, h / 2)
    inset = r * (1 - math.cos(math.pi / 4))
    local = (
        (x + w / 2, y),
        (x + w, y + h / 2),
        (x + w / 2, y + h),
        (x, y + h / 2),
        (x + inset, y + inset),
        (x + w - inset, y + inset),
        (x + w - inset, y + h - inset),
        (x + inset, y + h - inset),
    )
    cx, cy = x + w / 2, y + h / 2
    return [_css_rotate(px, py, cx, cy, rot) for px, py in local]


def _inside(poly: list[tuple[float, float]], x: float, y: float, eps: float = _OUTSIDE_PX) -> bool:
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        edge = math.hypot(x2 - x1, y2 - y1) or 1.0

        def side(px: float, py: float, x1=x1, y1=y1, x2=x2, y2=y2) -> float:
            return (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)

        interior = side(cx, cy)
        dist = side(x, y) / edge
        if interior >= 0 and dist < -eps:
            return False
        if interior < 0 and dist > eps:
            return False
    return True


def _fmt_box(poly: list[tuple[float, float]]) -> str:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return f"{min(xs):.0f}–{max(xs):.0f} × {min(ys):.0f}–{max(ys):.0f}"


def check_scenes(chapter: str, scenes: list[dict]) -> list[str]:
    """Lỗi con dấu và tiêu đề trên các cảnh ``file``. Cảnh khác không bị bắt mực."""
    out: list[str] = []
    for i, scene in enumerate(scenes):
        if scene.get("type") != "file":
            continue
        out.extend(_file_problems(chapter, i, scene))
    return out


def _file_problems(chapter: str, index: int, scene: dict) -> list[str]:
    out: list[str] = []
    where = f"{chapter} cảnh {index}"
    stamp = scene.get("stamp")
    if isinstance(stamp, dict):
        label = stamp.get("text") or ""
        if not stamp.get("ink"):
            shown = f" “{label}”" if label else ""
            out.append(f"{where}: thẻ giấy có con dấu{shown} nhưng không bật stamp.ink — trên giấy màu đỏ sẽ bị nhạt.")
        if not label:
            out.append(f"{where}: con dấu không có chữ.")
        else:
            left, top, cw, ch = card_size(scene)
            sx, sy, sw, sh, rot = stamp_size(stamp)
            card = _card_poly(left, top, cw, ch, _card_scale(scene, stamp))
            mark = _stamp_points(sx, sy, sw, sh, rot)
            if any(not _inside(card, x, y) for x, y in mark):
                out.append(
                    f"{where}: con dấu “{label}” tràn khỏi thẻ giấy "
                    f"(dấu {_fmt_box(mark)}, thẻ {_fmt_box(card)})."
                )
    name = scene.get("name") or ""
    if name:
        lines = name.split("\n")
        longest = max(lines, key=len)
        fs = fsz(longest, NAME_MAX, NAME_TRACK, NAME_K)
        font = _playfair(fs)
        for line in lines:
            if not line:
                continue
            width = _advance(line, font, fs)
            if width > CARD_INNER_W + TITLE_SLACK_PX:
                out.append(
                    f"{where}: tiêu đề “{line}” rộng {width:.0f}px, lòng thẻ {CARD_INNER_W:.0f}px "
                    f"— sẽ tự xuống dòng. Chia dòng bằng \\n hoặc rút ngắn."
                )
    return out


def hdr_reason(tags: dict) -> str | None:
    """Chuỗi mô tả nếu ``tags`` (ffprobe stream) là HDR. SDR và tag trống trả None."""
    if not tags or tags.get("_error"):
        return None
    transfer = str(tags.get("color_transfer") or "").lower()
    primaries = str(tags.get("color_primaries") or "").lower()
    matrix = str(tags.get("color_space") or tags.get("color_matrix") or "").lower()
    hits = []
    if transfer in HDR_TRANSFER:
        hits.append(f"color_transfer={transfer}")
    if primaries in HDR_PRIMARIES:
        hits.append(f"color_primaries={primaries}")
    if matrix in HDR_MATRIX:
        hits.append(f"color_space={matrix}")
    return ", ".join(hits) or None


def hdr_problem(chapter: str, index: int, vid: str, tags: dict) -> str | None:
    if tags.get("_error"):
        return f"{chapter} cảnh {index}: không đọc được màu của clip {vid} ({tags['_error']})."
    reason = hdr_reason(tags)
    if not reason:
        return None
    return (
        f"{chapter} cảnh {index}: clip {vid} là HDR ({reason}). "
        "Chuyển sang SDR bt709 yuv420p rồi chạy lại html."
    )


def lint_chapters(chapters: list[tuple[str, dict]], color_of) -> list[str]:
    """``color_of(vid)`` trả dict ffprobe, hoặc None nếu file chưa có (để bước html báo thiếu file như cũ)."""
    problems: list[str] = []
    for name, chapter in chapters:
        scenes = chapter.get("scenes") or []
        problems.extend(check_scenes(name, scenes))
        seen: set[str] = set()
        for i, scene in enumerate(scenes):
            if not scene.get("vid"):
                continue
            vid = str(scene["vid"])
            if vid in seen:
                continue
            seen.add(vid)
            tags = color_of(vid)
            if tags is None:
                continue
            msg = hdr_problem(name, i, vid, tags)
            if msg:
                problems.append(msg)
    return problems
