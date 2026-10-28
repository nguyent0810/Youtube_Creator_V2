"""Remove the Gemini sparkle baked into the corner of a Google Flow image.

Nano Banana Pro previews (measured 2026-10-28 on 1376×768 frames) carry a
translucent white four-petal sparkle, about 40–48 px across, in the
bottom-right corner. The petals run up, down, left and right and the sides
curve inward. It is not a flat sticker and not a fixed pixel: the samples
land near (1278, 671). A straight rhombus, an 8-point star, or the same
shape sitting away from that corner is not the mark.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

# Search only this bottom-right window. A strict 12%×15% clip cuts the top tip
# of the measured mark (its top sits ~84% down the frame), so the window is
# a little wider than the ticket's "about 12% × 15%".
CORNER_W = 0.16
CORNER_H = 0.22
# Normalised correlation with a diamond. The four real samples scored
# 0.73–0.93. After the real mark is removed, the busiest corner (the red
# band on fs_compass) still correlates at 0.55, so the cut sits above that
# and below the weakest real mark.
SCORE_MIN = 0.62
# Mean min-channel lift on the diamond's core and on its four tips.
# A clear mark sits around 50. The faintest real one (a sparkle on a
# grey-to-white ramp) still lifts the core by about 16, so the cut is 16.
# A round blob can correlate with an oversized diamond, but that match
# leaves the tips dark.
LIFT_MIN = 16.0
# Mean lift in the four diagonal shoulders (inside the circumscribed circle,
# outside the diamond) divided by the core. A diamond is near 0 here
# (measured ≤ 0.12 on the samples); a disc of the same size is above 0.5.
SHOULDER_MAX = 0.35
# Sparkle centre on the 1376×768 previews, stored as a fraction of the frame
# so other sizes scale. Tolerance is ±25 px on that same frame.
_REF_W, _REF_H = 1376.0, 768.0
ANCHOR_X = 1.0 - 97.0 / _REF_W
ANCHOR_Y = 1.0 - 98.0 / _REF_H
ANCHOR_TOL_X = 25.0 / _REF_W
ANCHOR_TOL_Y = 25.0 / _REF_H
# Outline of the bright core (lift ≥ 45% of the centre). A curved sparkle is
# concave: solidity stays under ~0.76 on the real previews and the synthetic
# petal, while a straight rhombus is 1. At least three diagonals must end
# well inside the axial tips (≤ 0.80 of that length). One diagonal may be
# bright because of the picture behind the mark. The bright area over its
# bounding box sits around 0.3–0.5; a filled block is higher.
SOLIDITY_MAX = 0.88
DIAG_RADIUS_MAX = 0.80
DIAG_DARK_MIN = 3
AXIAL_TIP_MIN = 0.55
AREA_MIN = 0.15
AREA_MAX = 0.65
# Fixed sparkle box on a fresh Flow download, as a fraction of the width.
# The six measured boxes are about 55 px on a 1376-wide frame. The pad is
# extra margin so a crop cannot leave a bright sliver when detection misses.
MARK_SIDE = 55.0 / _REF_W
MARK_PAD = 8.0 / _REF_W
# Ray fallback for a sparkle the outline test drops: a dark edge can split
# the bright core (wood), or the core lift can sit under the outline cut
# while the four tips are still there (grey ramp). Diagonals must be shorter
# than on the outline test, because this path has no solidity check — a
# straight rhombus reaches about 0.71 of the axial length.
RAY_CORE_MIN = 8.0
RAY_FRAC = 0.25
RAY_DIAG_MAX = 0.65
RAY_GAP = 3


def find_mark(img):
    """Return the sparkle box as (x0, y0, x1, y1), or None.

    `img` is a PIL image, a file path, or an HxWx3 array. The box is in
    full-image pixels, end-exclusive, and includes a small halo around the
    diamond so a later crop does not leave a bright sliver. Nothing outside
    the bottom-right corner is considered.
    """
    rgb = _as_rgb(img)
    hit = _locate(rgb)
    if hit is None:
        return None
    x, y, n, _score, _lift = hit
    return _box(rgb.shape[1], rgb.shape[0], x, y, n)


def fixed_mark_box(w, h):
    """Square that covers the Flow sparkle, in full-image pixels.

    The centre is `(w - 97/1376·w, h - 98/768·h)` and the side is
    `55/1376·w`, plus `8/1376·w` of padding on every side. End-exclusive.
    """
    cx = w * ANCHOR_X
    cy = h * ANCHOR_Y
    half = w * (MARK_SIDE / 2.0 + MARK_PAD)
    return (
        max(0, int(np.floor(cx - half))),
        max(0, int(np.floor(cy - half))),
        min(w, int(np.ceil(cx + half))),
        min(h, int(np.ceil(cy + half))),
    )


def strip_mark(path, mode="crop", known_flow=False):
    """Overwrite `path` with the sparkle removed. Return that path.

    `crop` (the default) cuts the bottom and the right far enough to drop
    the sparkle, and keeps the original aspect ratio (the two cuts stay
    proportional). `fill` inpaints the sparkle and keeps the frame size.
    No sparkle: the file is not opened for writing.

    `known_flow` is for a file just downloaded by `flow generate`. Those
    always carry the sparkle at `fixed_mark_box`, so `crop` cuts that box
    even when `find_mark` misses it, and widens the cut if detection sticks
    out past the fixed box. `fill` still requires a detection: otherwise the
    file is left as-is and a warning is printed. Calling this again on an
    already-cropped Flow image cuts a second corner; `flow generate` calls
    it once, on the fresh download.
    """
    if mode not in ("fill", "crop"):
        raise ValueError("mode must be 'fill' or 'crop'")
    path = Path(path)
    rgb = _as_rgb(path)
    hit = _locate(rgb)
    h, w = rgb.shape[:2]
    seen = None
    if hit is not None:
        x, y, n, _score, _lift = hit
        seen = _box(w, h, x, y, n)
    if seen is None and not (known_flow and mode == "crop"):
        if known_flow and mode == "fill":
            print(f"cảnh báo: không thấy dấu ✦, không vá {path}", file=sys.stderr)
        return path
    if mode == "crop":
        if known_flow:
            box = fixed_mark_box(w, h)
            if seen is not None:
                box = (
                    min(box[0], seen[0]),
                    min(box[1], seen[1]),
                    max(box[2], seen[2]),
                    max(box[3], seen[3]),
                )
        else:
            box = seen
        new_w, new_h = _crop_size(w, h, box)
        out = np.ascontiguousarray(rgb[:new_h, :new_w])
        if known_flow and find_mark(out) is not None:
            print(f"cảnh báo: sau khi cắt vẫn còn dấu ✦ trong {path}", file=sys.stderr)
    else:
        import cv2
        mask = _diamond_mask(h, w, seen)
        out = cv2.inpaint(rgb, mask, 5, cv2.INPAINT_NS)
    _save_rgb(path, out)
    return path


def _locate(rgb):
    """Return (x, y, n, score, lift) of the best diamond, or None.

    `x, y` is the top-left of the matched template and `n` its side.
    """
    import cv2

    h, w = rgb.shape[:2]
    if w < 80 or h < 80:
        return None
    k = _kernel(w, h)
    lift = _min_lift(rgb, k)
    x0 = int(round(w * (1.0 - CORNER_W)))
    y0 = int(round(h * (1.0 - CORNER_H)))
    roi = lift[y0:, x0:]
    lo = max(20, int(w * 0.02))
    hi = max(lo + 4, int(w * 0.06))
    best = None
    for n in range(lo, hi, 2):
        if n >= roi.shape[0] - 1 or n >= roi.shape[1] - 1:
            continue
        tmpl = _diamond(n)
        score_map = cv2.matchTemplate(roi, tmpl, cv2.TM_CCOEFF_NORMED)
        _min_s, mx, _min_at, loc = cv2.minMaxLoc(score_map)
        if not np.isfinite(mx) or mx < SCORE_MIN:
            continue
        x, y = x0 + loc[0], y0 + loc[1]
        patch = lift[y:y + n, x:x + n]
        shape = _shape_lifts(patch, tmpl)
        if shape is None:
            continue
        core, tips, shoulder_ratio = shape
        if tips < LIFT_MIN or core < LIFT_MIN or shoulder_ratio > SHOULDER_MAX:
            continue
        cx = x + (n - 1) / 2.0
        cy = y + (n - 1) / 2.0
        if not _near_anchor(w, h, cx, cy):
            continue
        if not _curved_petals(lift, x, y, n) and not _ray_petals(lift, x, y, n):
            continue
        if best is None or mx > best[0]:
            best = (float(mx), x, y, n, core)
    if best is None:
        return None
    score, x, y, n, core = best
    return x, y, n, score, core


def _near_anchor(w, h, cx, cy):
    """True when (cx, cy) is the sparkle's usual centre, scaled to this frame."""
    return (
        abs(cx / w - ANCHOR_X) <= ANCHOR_TOL_X
        and abs(cy / h - ANCHOR_Y) <= ANCHOR_TOL_Y
    )


def _curved_petals(lift, x, y, n):
    """True for a concave 4-petal sparkle. False for a rhombus or a star.

    The outline must have four tips on the vertical and horizontal axes, and
    the diagonals must fall short of those tips (the sides curve inward).
    A straight rhombus is convex, so its solidity is rejected. An 8-point
    or 5-point star keeps long diagonal tips, so those are rejected too.
    """
    import cv2

    h, w = lift.shape
    pad = 6
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(w, x + n + pad), min(h, y + n + pad)
    patch = lift[y0:y1, x0:x1]
    cx = (x + (n - 1) / 2.0) - x0
    cy = (y + (n - 1) / 2.0) - y0
    icx, icy = int(round(cx)), int(round(cy))
    if not (1 <= icx < patch.shape[1] - 1 and 1 <= icy < patch.shape[0] - 1):
        return False
    core = float(patch[icy - 1:icy + 2, icx - 1:icx + 2].mean())
    if core < LIFT_MIN:
        return False
    mask = (patch >= 0.45 * core).astype(np.uint8)
    _nlab, labels = cv2.connectedComponents(mask)
    lab = int(labels[icy, icx])
    if lab == 0:
        return False
    comp = (labels == lab).astype(np.uint8)
    contours, _hier = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return False
    cnt = max(contours, key=cv2.contourArea)
    area = float(cv2.contourArea(cnt))
    hull = float(cv2.contourArea(cv2.convexHull(cnt)))
    if hull < 1 or area / hull > SOLIDITY_MAX:
        return False
    _bx, _by, bw, bh = cv2.boundingRect(cnt)
    if bw < 8 or bh < 8:
        return False
    if not (AREA_MIN <= area / float(bw * bh) <= AREA_MAX):
        return False
    pts = cnt.reshape(-1, 2).astype(np.float64)
    ang = (np.degrees(np.arctan2(pts[:, 1] - cy, pts[:, 0] - cx)) + 360.0) % 360.0
    rad = np.hypot(pts[:, 0] - cx, pts[:, 1] - cy)
    axial = np.array([_sector_radius(ang, rad, a) for a in (0, 90, 180, 270)])
    diag = np.array([_sector_radius(ang, rad, a) for a in (45, 135, 225, 315)])
    if not np.isfinite(axial).all():
        return False
    ax = float(np.median(axial))
    if ax < 6 or float(axial.min()) < AXIAL_TIP_MIN * ax:
        return False
    if not np.isfinite(diag).all():
        return False
    dark = int(np.sum(diag <= DIAG_RADIUS_MAX * ax))
    return dark >= DIAG_DARK_MIN


def _ray_petals(lift, x, y, n):
    """True when four axial rays outrun the diagonals.

    Unlike `_curved_petals`, the tips do not have to be one connected blob.
    A few dark pixels may sit between the centre and a tip (a wood edge
    crossing the sparkle). The centre only has to be faintly bright; the
    caller has already required a diamond-shaped lift.
    """
    h, w = lift.shape
    cx = x + (n - 1) / 2.0
    cy = y + (n - 1) / 2.0
    icx, icy = int(round(cx)), int(round(cy))
    if not (1 <= icx < w - 1 and 1 <= icy < h - 1):
        return False
    core = float(lift[icy - 1:icy + 2, icx - 1:icx + 2].mean())
    if core < RAY_CORE_MIN:
        return False
    reach = (n - 1) / 2.0
    thresh = RAY_FRAC * core

    def end(dx, dy):
        last = 0
        gap = 0
        for i in range(1, int(reach) + 1):
            px = int(round(cx + dx * i))
            py = int(round(cy + dy * i))
            if not (0 <= px < w and 0 <= py < h):
                break
            if float(lift[py, px]) >= thresh:
                last = i
                gap = 0
            else:
                gap += 1
                if gap > RAY_GAP and i > 4:
                    break
        return last

    axial = np.array([end(dx, dy) for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))])
    diag = np.array([
        end(dx, dy)
        for dx, dy in (
            (0.7071, 0.7071),
            (0.7071, -0.7071),
            (-0.7071, 0.7071),
            (-0.7071, -0.7071),
        )
    ])
    ax = float(np.median(axial))
    if ax < 6 or float(axial.min()) < AXIAL_TIP_MIN * ax:
        return False
    return int(np.sum(diag <= RAY_DIAG_MAX * ax)) >= DIAG_DARK_MIN


def _sector_radius(ang, rad, target):
    """Median radius of contour points within 18° of `target` (degrees)."""
    delta = np.minimum(np.abs(ang - target), 360.0 - np.abs(ang - target))
    picked = rad[delta <= 18.0]
    if picked.size < 3:
        return np.nan
    return float(np.median(picked))


def _box(w, h, x, y, n):
    """Square bounding box of the diamond plus a halo, clipped to the frame."""
    grow = max(4, int(round(n * 0.18)))
    return (
        max(0, x - grow),
        max(0, y - grow),
        min(w, x + n + grow),
        min(h, y + n + grow),
    )


def _crop_size(w, h, box):
    """Largest top-left crop that excludes `box` and keeps w:h within 1 px."""
    x0, y0, _x1, _y1 = box
    max_w = x0  # columns [0, x0) sit strictly left of the box
    max_h = y0
    if max_w < 2 or max_h < 2:
        raise ValueError("sparkle covers too much of the frame to crop")
    new_h = min(max_h, int(max_w * h / w))
    new_w = int(round(new_h * w / h))
    if new_w > max_w:
        new_w = max_w
        new_h = int(round(new_w * h / w))
    while new_h > 1 and abs(new_w - new_h * w / h) > 1:
        new_h -= 1
        new_w = int(round(new_h * w / h))
        if new_w > max_w:
            new_w = max_w
            new_h = min(new_h, max_h)
    if new_w > max_w or new_h > max_h or new_w < 2 or new_h < 2:
        raise ValueError("could not keep the aspect ratio while dropping the sparkle")
    return new_w, new_h


def _kernel(w, h):
    """Odd median size, larger than the sparkle (~3.5% of the width).

    Sized from the width, because the mark scales with the frame width
    (about 48 px on a 1376-wide preview → kernel 61).
    """
    k = int(round(w * 0.044))
    if k % 2 == 0:
        k += 1
    k = min(81, max(31, k))
    limit = min(w, h)
    while k >= limit:
        k -= 2
    return max(k, 3)


def _min_lift(rgb, k):
    """How far every channel rose together versus a local median.

    A white overlay lifts R, G and B at once. A coloured highlight lifts one
    channel and leaves this map near zero.
    """
    import cv2

    bg = np.stack([cv2.medianBlur(rgb[:, :, c], k) for c in range(3)], axis=-1)
    delta = rgb.astype(np.float32) - bg.astype(np.float32)
    return np.clip(delta.min(axis=2), 0, None)


def _diamond(n):
    """Soft filled diamond in [0, 1], 1 at the centre. `n` is the side."""
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    c = (n - 1) / 2.0
    manhattan = (np.abs(xx - c) + np.abs(yy - c)) / max(c, 1.0)
    soft = 0.18
    return np.clip((1.0 + soft - manhattan) / (2.0 * soft), 0, 1).astype(np.float32)


def _shape_lifts(patch, tmpl):
    """Core lift, axial-tip lift, and shoulder/core ratio. None if undefined."""
    n = tmpl.shape[0]
    c = (n - 1) / 2.0
    yy, xx = np.mgrid[0:n, 0:n]
    core = tmpl > 0.75
    axial = (np.abs(yy - c) < 2.5) | (np.abs(xx - c) < 2.5)
    tips = (tmpl > 0.4) & (tmpl < 0.85) & axial
    euc = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / max(c, 1.0)
    shoulder = (euc < 0.92) & (tmpl < 0.15)
    if core.sum() < 4 or tips.sum() < 4 or shoulder.sum() < 8:
        return None
    core_lift = float(patch[core].mean())
    tip_lift = float(patch[tips].mean())
    if core_lift <= 1:
        return None
    return core_lift, tip_lift, float(patch[shoulder].mean()) / core_lift


def _diamond_mask(h, w, box):
    """uint8 mask, 255 on the diamond whose bounding square is `box`."""
    x0, y0, x1, y1 = box
    mask = np.zeros((h, w), np.uint8)
    cx = (x0 + x1 - 1) / 2.0
    cy = (y0 + y1 - 1) / 2.0
    rad = ((x1 - x0) + (y1 - y0)) / 4.0
    yy, xx = np.ogrid[y0:y1, x0:x1]
    on = (np.abs(xx - cx) + np.abs(yy - cy)) <= rad + 0.5
    mask[y0:y1, x0:x1] = np.where(on, 255, 0).astype(np.uint8)
    return mask


def _as_rgb(img):
    if isinstance(img, (str, Path)):
        from PIL import Image
        with Image.open(img) as im:
            return np.ascontiguousarray(im.convert("RGB"))
    if hasattr(img, "convert"):
        return np.ascontiguousarray(img.convert("RGB"))
    arr = np.asarray(img)
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    elif arr.shape[-1] == 4:
        arr = arr[..., :3]
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    return np.ascontiguousarray(arr)


def _save_rgb(path, rgb):
    from PIL import Image

    path = Path(path)
    tmp = path.with_name(path.name + ".strip.tmp")
    im = Image.fromarray(rgb)
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        im.save(tmp, format="JPEG", quality=95, subsampling=0)
    elif suffix == ".png":
        im.save(tmp, format="PNG")
    else:
        im.save(tmp)
    os.replace(tmp, path)
