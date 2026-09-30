"""Bản đồ vector cho video dài (sơ đồ `map` của longform.js) -- nướng sẵn.

HyperFrames cấm mạng lúc render và cần tất định (skill motion-graphics, mục
maps, "vector lane"): biên giới được tải MỘT lần (world-atlas TopoJSON, cache
tại chunks_cache/geo/), giải mã, chiếu vào khung hình, rồi ghi thẳng đường SVG
+ toạ độ điểm vào plan lúc render. longform.js chỉ vẽ, không tính địa lý.

    bake(spec) -> spec + "_geo": {countries: [{name, d, label, focus}], pins: [{x, y, ...}]}

spec: {"countries": ["India", "Nepal"], "context": ["China", ...],
       "bbox": [lon_min, lat_min, lon_max, lat_max],
       "pins": [{"name": "Lâm Tỳ Ni", "lon": 83.28, "lat": 27.48, "at": 12, ...}]}
Tên nước theo world-atlas (tiếng Anh, vd "India", "Nepal").
"""
from __future__ import annotations

import json
import math
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
CACHE = ROOT / "chunks_cache" / "geo" / "countries-50m.json"
SOURCE = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json"
# Khung vẽ bản đồ trong khung 1920x1080 (chừa đáy cho phụ đề, trái cho tiêu đề)
BOX = (150, 120, 1770, 860)


def _topology() -> dict:
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(SOURCE, timeout=60) as r:
            CACHE.write_bytes(r.read())
    return json.loads(CACHE.read_text(encoding="utf-8"))


def _arcs(topo: dict) -> list[list[tuple[float, float]]]:
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    out = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:  # toạ độ lượng tử hoá, mã hoá delta
            x += dx; y += dy
            pts.append((x * sx + tx, y * sy + ty))
        out.append(pts)
    return out


def _ring(arcs, idx: list[int]) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in idx:
        seg = arcs[i] if i >= 0 else arcs[~i][::-1]
        pts.extend(seg[1:] if pts else seg)
    return pts


def _polygons(topo: dict, name: str) -> list[list[list[tuple[float, float]]]]:
    arcs = _arcs(topo)
    for g in topo["objects"]["countries"]["geometries"]:
        if (g.get("properties") or {}).get("name") != name:
            continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        return [[_ring(arcs, ring) for ring in poly] for poly in polys]
    raise KeyError(f"world-atlas không có nước {name!r}")


def _projector(bbox):
    """Mercator, khớp bbox vào BOX giữ đúng tỉ lệ."""
    lon0, lat0, lon1, lat1 = bbox
    merc = lambda lat: math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    x0, x1 = math.radians(lon0), math.radians(lon1)
    y0, y1 = merc(lat0), merc(lat1)
    bx0, by0, bx1, by1 = BOX
    k = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    ox = bx0 + ((bx1 - bx0) - k * (x1 - x0)) / 2
    oy = by0 + ((by1 - by0) - k * (y1 - y0)) / 2

    def p(lon, lat):
        lat = max(-85, min(85, lat))
        return ox + k * (math.radians(lon) - x0), oy + k * (y1 - merc(lat))
    return p


def _path(rings, proj, bbox, pad=6.0) -> str:
    lon0, lat0, lon1, lat1 = bbox
    out = []
    for ring in rings:
        # bỏ vòng nằm ngoài vùng nhìn (đảo xa, lãnh thổ hải ngoại)
        if not any(lon0 - pad <= x <= lon1 + pad and lat0 - pad <= y <= lat1 + pad for x, y in ring):
            continue
        last = None
        seg = []
        for lon, lat in ring:
            x, y = proj(lon, lat)
            if last and abs(x - last[0]) + abs(y - last[1]) < 1.2:
                continue  # rút gọn điểm dưới 1px
            seg.append(f"{x:.1f},{y:.1f}"); last = (x, y)
        if len(seg) >= 3:
            out.append("M" + " L".join(seg) + " Z")
    return " ".join(out)


def bake(spec: dict) -> dict:
    topo = _topology()
    bbox = spec["bbox"]
    proj = _projector(bbox)
    countries = []
    for name, focus in [(n, True) for n in spec.get("countries", [])] + [(n, False) for n in spec.get("context", [])]:
        polys = _polygons(topo, name)
        d = " ".join(_path(poly, proj, bbox) for poly in polys).strip()
        # nhãn nước: trọng tâm của PHẦN nằm trong khung (nước lớn như Trung Quốc
        # có trọng tâm cả nước rơi ra ngoài khung)
        bx0, by0, bx1, by1 = BOX
        vis = [(x, y) for poly in polys for ring in poly for x, y in (proj(lon, lat) for lon, lat in ring)
               if bx0 <= x <= bx1 and by0 <= y <= by1]
        cx = sum(x for x, _ in vis) / len(vis) if vis else -999
        cy = sum(y for _, y in vis) / len(vis) if vis else -999
        countries.append({"name": name, "label": spec.get("labels", {}).get(name, ""), "d": d, "focus": focus,
                          "lx": round(cx, 1), "ly": round(cy, 1)})
    pins = []
    for pin in spec.get("pins", []):
        x, y = proj(pin["lon"], pin["lat"])
        pins.append({**pin, "x": round(x, 1), "y": round(y, 1)})
    return {**spec, "_geo": {"countries": countries, "pins": pins}}


if __name__ == "__main__":
    demo = bake({"countries": ["India", "Nepal"], "context": ["China", "Bangladesh", "Bhutan"],
                 "bbox": [80.5, 23.2, 88.8, 29.2],
                 "pins": [{"name": "Lâm Tỳ Ni", "lon": 83.2767, "lat": 27.4833}]})
    for c in demo["_geo"]["countries"]:
        print(c["name"], len(c["d"]), c["lx"], c["ly"])
    print(demo["_geo"]["pins"])
