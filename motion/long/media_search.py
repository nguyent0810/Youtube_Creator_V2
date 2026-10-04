"""Tư liệu hình NGOÀI Wikimedia Commons cho video dài — chỉ các nguồn đã kiểm tra giấy phép dùng thương mại (04/10/2026).

    python motion/long/media_search.py search <topic> "opium den" [--src openverse,wellcome,artic,europeana]
    python motion/long/media_search.py get <topic> <key> X12          # tải ứng viên X12 thành ảnh <key>
    python motion/long/media_search.py sat <topic> <key> <minlon> <minlat> <maxlon> <maxlat> [2023-11-15/2024-01-31]   (mùa khô ít khói đốt nương: tháng 11–1)

Nguồn (xem motion/long/SOURCES.md):
- openverse : kho tổng hợp Creative Commons (Flickr, Wikimedia, bảo tàng…). Chỉ nhận CC0 / PDM / CC BY / CC BY-SA.
              Ảnh Flickr: cẩn thận "rửa giấy phép" (người đăng không phải tác giả) — xem kỹ trước khi dùng.
- wellcome  : Wellcome Collection — lịch sử y học, thuốc phiện, châu Á thế kỷ 19 (PDM / CC0 / CC BY).
- artic     : Art Institute of Chicago — tác phẩm phạm vi công cộng, CC0 (có ảnh Hồng Kông, Trung Hoa thế kỷ 19).
- europeana : thư viện/bảo tàng châu Âu (ảnh thuộc địa châu Á của KITLV, Tropenmuseum…). reusability=open.
              Đặt EUROPEANA_KEY (đăng ký miễn phí), không có thì dùng khóa demo "api2demo".
- sat       : ảnh vệ tinh Sentinel-2 L2A qua Microsoft Planetary Computer (truy cập ẩn danh).
              Dữ liệu Copernicus: dùng thương mại tự do, BẮT BUỘC ghi "Contains modified Copernicus Sentinel data <năm>".
KHÔNG dùng: EOX Sentinel-2 cloudless (thương mại phải mua), Gallica/BnF (thương mại phải trả phí), kho ảnh chính phủ
Hồng Kông GRS (phải xin phép), British Pathé / AP / Reuters / Getty (trả phí).

Ảnh tải về: output/long/<topic>/img/<key>.jpg + <key>.json {file, license, artist, title, source} — build_long.fetch_img
thấy đủ hai file thì dùng luôn; spec.json "imgs" được ghi "<key>": "EXT:<nguồn>:<id>"; describe.py in credit tự động.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
H = {"User-Agent": "yt-factory-research/1.0 (Into the Killer's Mind; educational documentaries)"}
OK_LIC = re.compile(r"^(cc0|pdm|by|by-sa)$")


def out(topic):
    d = ROOT / "output" / "long" / topic
    d.mkdir(parents=True, exist_ok=True)
    return d


def jget(url, **kw):
    for k in range(4):
        try:
            r = requests.get(url, headers=H, timeout=60, **kw)
            if r.status_code == 429:
                time.sleep(5 * (k + 1)); continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if k == 3:
                raise
            time.sleep(3 * (k + 1))


# ---------- nguồn: mỗi hàm trả về list ứng viên {src, id, title, license, artist, thumb, full, w, h, page} ----------
def s_openverse(q):
    d = jget("https://api.openverse.org/v1/images/", params={"q": q, "license": "cc0,pdm,by,by-sa", "page_size": 30, "mature": "false"})
    res = []
    for i in d.get("results", []):
        lic = i.get("license", "")
        if not OK_LIC.match(lic):
            continue
        lab = {"cc0": "CC0", "pdm": "Public domain"}.get(lic, f"CC {lic.upper()} {i.get('license_version') or ''}".strip())
        res.append({"src": "openverse:" + (i.get("source") or ""), "id": i["id"], "title": i.get("title") or "", "license": lab,
                    "artist": i.get("creator") or "", "thumb": i.get("thumbnail") or i["url"], "full": i["url"],
                    "w": i.get("width") or 0, "h": i.get("height") or 0, "page": i.get("foreign_landing_url") or ""})
    return res


def s_wellcome(q):
    d = jget("https://api.wellcomecollection.org/catalogue/v2/images", params={"query": q, "pageSize": 40, "locations.license": "cc-0,cc-by,pdm"})
    res = []
    for i in d.get("results", []):
        loc = (i.get("locations") or [{}])[0]
        lic = (loc.get("license") or {}).get("id", "")
        lab = {"cc-0": "CC0", "pdm": "Public domain", "cc-by": "CC BY 4.0"}.get(lic)
        if not lab:
            continue
        base = loc["url"].rsplit("/info.json", 1)[0]
        ar = i.get("aspectRatio") or 1.3
        res.append({"src": "wellcome", "id": i["id"], "title": (i.get("source") or {}).get("title", ""), "license": lab,
                    "artist": "Wellcome Collection", "thumb": base + "/full/300,/0/default.jpg", "full": base + "/full/1920,/0/default.jpg",
                    "w": 1920, "h": int(1920 / ar), "page": f"https://wellcomecollection.org/works/{(i.get('source') or {}).get('id', '')}"})
    return res


def s_artic(q):
    d = jget("https://api.artic.edu/api/v1/artworks/search", params={"q": q, "limit": 40, "fields": "id,title,image_id,artist_display,is_public_domain,thumbnail"})
    res = []
    for i in d.get("data", []):
        if not i.get("is_public_domain") or not i.get("image_id"):
            continue
        t = i.get("thumbnail") or {}
        w, h = t.get("width") or 1686, t.get("height") or 1200
        base = f"https://www.artic.edu/iiif/2/{i['image_id']}"
        res.append({"src": "artic", "id": str(i["id"]), "title": i.get("title", ""), "license": "CC0",
                    "artist": (i.get("artist_display") or "").split("\n")[0], "thumb": base + "/full/300,/0/default.jpg",
                    "full": base + "/full/1686,/0/default.jpg", "w": w, "h": h, "page": f"https://www.artic.edu/artworks/{i['id']}"})
    return res


def s_europeana(q):
    key = os.environ.get("EUROPEANA_KEY", "api2demo")
    d = jget("https://api.europeana.eu/record/v2/search.json", params={"wskey": key, "query": q, "reusability": "open", "media": "true",
                                                                       "qf": "TYPE:IMAGE", "rows": 40, "profile": "rich"})
    res = []
    for i in d.get("items", []):
        r = (i.get("rights") or [""])[0]
        if "publicdomain/mark" in r:
            lab = "Public domain"
        elif "publicdomain/zero" in r:
            lab = "CC0"
        elif m := re.search(r"licenses/(by(?:-sa)?)/(\d\.\d)", r):
            lab = f"CC {m.group(1).upper()} {m.group(2)}"
        else:
            continue
        full = (i.get("edmIsShownBy") or [None])[0]
        if not full:
            continue
        res.append({"src": "europeana:" + ((i.get("dataProvider") or [""])[0])[:40], "id": i["id"], "title": (i.get("title") or [""])[0],
                    "license": lab, "artist": ((i.get("dcCreator") or [""])[0])[:80] or ((i.get("dataProvider") or [""])[0]),
                    "thumb": (i.get("edmPreview") or [full])[0], "full": full, "w": 0, "h": 0, "page": (i.get("guid") or "")})
    return res


SRC = {"openverse": s_openverse, "wellcome": s_wellcome, "artic": s_artic, "europeana": s_europeana}


def sheet(path: Path, cands: list[dict], start: int):
    cells = []
    for k, c in enumerate(cands):
        try:
            b = requests.get(c["thumb"], headers=H, timeout=30).content
            t = Image.open(io.BytesIO(b)).convert("RGB")
            t.thumbnail((300, 300))
            cells.append((start + k, t, c))
        except Exception:
            continue
    if not cells:
        return
    cols = 6
    S = Image.new("RGB", (cols * 310, ((len(cells) + cols - 1) // cols) * 340), (20, 20, 20))
    dr = ImageDraw.Draw(S)
    try:
        f = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        f = ImageFont.load_default()
    for n, (k, t, c) in enumerate(cells):
        x, y = (n % cols) * 310 + 5, (n // cols) * 340 + 30
        S.paste(t, (x, y))
        dr.text((x, y - 26), f"X{k} {c['license'][:10]} {c['src'].split(':')[0][:9]}", fill=(255, 220, 90), font=f)
    S.save(path, quality=80)


def cmd_search(topic, q, srcs):
    od = out(topic)
    db_p = od / "ext.json"
    db = json.loads(db_p.read_text(encoding="utf-8")) if db_p.exists() else []
    seen = {(c["src"], c["id"]) for c in db}
    new = []
    for s in srcs:
        try:
            got = SRC[s](q)
        except Exception as e:
            print(f"  {s}: LỖI {e}")
            continue
        got = [c for c in got if (c["src"], c["id"]) not in seen]
        print(f"  {s}: {len(got)} ứng viên mới")
        new += got
        time.sleep(1)
    start = len(db)
    for k, c in enumerate(new):
        c["x"] = f"X{start + k}"
        c["q"] = q
        print(f"  {c['x']:5s} {c['license'][:13]:13s} {c['src'][:28]:28s} {c['title'][:70]}")
    db += new
    db_p.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    if new:
        sp = od / f"ext_sheet_{start}.jpg"
        sheet(sp, new[:48], start)
        print("bảng ảnh:", sp)


def save_img(raw: bytes, dst: Path):
    im = Image.open(io.BytesIO(raw))
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255)); im = im.convert("RGBA"); bg.paste(im, mask=im.split()[-1]); im = bg
    im = im.convert("RGB")
    if max(im.size) > 2400:
        im.thumbnail((2400, 2400))
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=90)
    return im.size


def register(topic, key, ref):
    sp = ROOT / "data" / "long" / topic / "spec.json"
    if sp.exists():
        s = json.loads(sp.read_text(encoding="utf-8"))
        s.setdefault("imgs", {})[key] = ref
        sp.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")


def cmd_get(topic, key, x):
    od = out(topic)
    db = json.loads((od / "ext.json").read_text(encoding="utf-8"))
    c = next((c for c in db if c["x"] == x), None)
    if not c:
        raise SystemExit(f"không có {x} trong ext.json")
    raw = requests.get(c["full"], headers=H, timeout=120).content
    w, h = save_img(raw, od / "img" / f"{key}.jpg")
    ref = f"EXT:{c['src'].split(':')[0]}:{c['id']}"
    (od / "img" / f"{key}.json").write_text(json.dumps({"file": ref, "license": c["license"], "artist": c["artist"], "title": c["title"],
                                                        "source": c["src"], "page": c["page"]}, ensure_ascii=False), encoding="utf-8")
    register(topic, key, ref)
    print(f"{key}: {w}x{h} {c['license']} · {c['src']} · {c['title'][:70]}")


def cmd_sat(topic, key, bbox, dates):
    """Sentinel-2 L2A ít mây nhất, chọn cảnh mà ô ảnh phủ trọn bbox; xuất ảnh màu thật theo đúng bbox."""
    st = requests.post("https://planetarycomputer.microsoft.com/api/stac/v1/search", headers=H, timeout=60, json={
        "collections": ["sentinel-2-l2a"], "bbox": bbox, "datetime": dates, "query": {"eo:cloud_cover": {"lt": 10}},
        "limit": 50, "sortby": [{"field": "eo:cloud_cover", "direction": "asc"}]}).json()
    pick = None
    for f in st.get("features", []):
        b = f["bbox"]
        if b[0] <= bbox[0] and b[1] <= bbox[1] and b[2] >= bbox[2] and b[3] >= bbox[3]:
            pick = f
            break
    if not pick:
        raise SystemExit("không có cảnh Sentinel-2 nào phủ trọn vùng này trong khoảng thời gian đã chọn — thu nhỏ bbox hoặc đổi thời gian")
    lon_span, lat_span = bbox[2] - bbox[0], bbox[3] - bbox[1]
    W = 1920
    Hh = max(400, int(W * lat_span / lon_span))
    u = f"https://planetarycomputer.microsoft.com/api/data/v1/item/bbox/{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}/{W}x{Hh}.jpg"
    r = requests.get(u, params={"collection": "sentinel-2-l2a", "item": pick["id"], "assets": "visual", "nodata": 0}, headers=H, timeout=180)
    r.raise_for_status()
    od = out(topic)
    w, h = save_img(r.content, od / "img" / f"{key}.jpg")
    year = pick["properties"]["datetime"][:4]
    ref = f"EXT:sentinel2:{pick['id']}"
    (od / "img" / f"{key}.json").write_text(json.dumps({"file": ref, "license": "Copernicus Sentinel data licence",
                                                        "artist": f"Contains modified Copernicus Sentinel data {year}", "title": f"Sentinel-2 {pick['properties']['datetime'][:10]}",
                                                        "source": "sentinel2", "page": "https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a"},
                                                       ensure_ascii=False), encoding="utf-8")
    register(topic, key, ref)
    print(f"{key}: {w}x{h} · {pick['id']} · mây {pick['properties']['eo:cloud_cover']:.1f}%")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    if a[0] == "search":
        srcs = a[a.index("--src") + 1].split(",") if "--src" in a else list(SRC)
        cmd_search(a[1], a[2], srcs)
    elif a[0] == "get":
        cmd_get(a[1], a[2], a[3])
    elif a[0] == "sat":
        cmd_sat(a[1], a[2], [float(v) for v in a[3:7]], a[7] if len(a) > 7 else "2023-11-15/2024-01-31")
    else:
        raise SystemExit(__doc__)
