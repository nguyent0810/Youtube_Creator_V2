"""Gom tư liệu cho hồ sơ S-tier: bài Wikipedia (EN) + ảnh THUỘC PHẠM VI CÔNG CỘNG.

    python motion/stier/research.py              # mọi hồ sơ trong data/stier/cases.tsv
    python motion/stier/research.py gardner ...  # chỉ vài hồ sơ

Ghi data/stier/research/<slug>.json (bài viết + ảnh ứng viên kèm giấy phép)
và <slug>.jpg (bảng ảnh đánh số để chọn bằng mắt). Chỉ giữ ảnh có giấy phép
Public domain / CC0 trên Commons — không ảnh AI, không ảnh có bản quyền.
Trùng chủ đề với kênh thì đánh dấu, KHÔNG làm tiếp (factory.lines.novelty +
từ khoá tên riêng: trùng tiêu đề chưa chắc bắt được trùng nhân vật).
"""
from __future__ import annotations

import html
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "stier" / "research"
UA = {"User-Agent": "yt-factory/1.0 (documentary research; contact via channel)"}
PD = re.compile(r"public domain|^pd|cc0|no restrictions", re.I)
SKIP = re.compile(r"(logo|icon|flag_of|commons-|question_book|wiki|edit-clear|symbol|padlock|ambox|crystal|nuvola|"
                  r"folder|stub|disambig|portal|\.svg$|signature_of|coat_of_arms|red_pog|blank|map_marker)", re.I)


def get(url: str, tries: int = 5) -> bytes:
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:  # 429/5xx: lùi dần
            if k == tries - 1:
                raise
            time.sleep(3 * (k + 1) + (10 if "429" in str(e) else 0))
    raise RuntimeError


def api(host: str, **params) -> dict:
    params |= {"format": "json", "formatversion": "2"}
    time.sleep(0.4)
    return json.loads(get(f"https://{host}/w/api.php?" + urllib.parse.urlencode(params)))


def article(title: str) -> dict:
    a = _article(title)
    if not a["text"]:   # tiêu đề đoán sai -> lấy kết quả tìm kiếm đầu tiên
        hit = api("en.wikipedia.org", action="query", list="search", srsearch=title, srlimit=1)["query"]["search"]
        if hit:
            a = _article(hit[0]["title"])
    return a


def commons_search(q: str, n: int = 30) -> list[str]:
    d = api("commons.wikimedia.org", action="query", list="search", srsearch=q, srnamespace=6, srlimit=n)
    return [h["title"] for h in d["query"]["search"]]


def _article(title: str) -> dict:
    d = api("en.wikipedia.org", action="query", prop="extracts|images|pageimages", explaintext=1,
            titles=title, redirects=1, imlimit=100, piprop="name")
    p = d["query"]["pages"][0]
    return {"title": p.get("title"), "text": p.get("extract", ""),
            "images": [i["title"] for i in p.get("images", [])], "lead": p.get("pageimage")}


def imageinfo(files: list[str]) -> list[dict]:
    out = []
    for i in range(0, len(files), 40):
        d = api("commons.wikimedia.org", action="query", prop="imageinfo", titles="|".join(files[i:i + 40]),
                iiprop="url|size|mime|extmetadata", iiurlwidth=360)
        for p in d["query"]["pages"]:
            ii = (p.get("imageinfo") or [None])[0]
            if not ii:
                continue
            md = ii.get("extmetadata", {})
            lic = md.get("LicenseShortName", {}).get("value", "")
            desc = re.sub(r"<[^>]+>", "", html.unescape(md.get("ImageDescription", {}).get("value", "")))[:220]
            out.append({"file": p["title"], "url": ii["url"], "thumb": ii.get("thumburl"), "w": ii["width"],
                        "h": ii["height"], "mime": ii["mime"], "license": lic,
                        "date": re.sub(r"<[^>]+>", "", md.get("DateTimeOriginal", {}).get("value", ""))[:40],
                        "desc": desc.strip()})
    return out


def sheet(slug: str, imgs: list[dict]) -> None:
    cells = []
    for k, im in enumerate(imgs):
        try:
            b = get(im["thumb"])
            t = Image.open(io.BytesIO(b)).convert("RGB")
            t.thumbnail((300, 300))
            cells.append((k, t))
        except Exception:
            continue
    if not cells:
        return
    cols = 6
    rows = (len(cells) + cols - 1) // cols
    S = Image.new("RGB", (cols * 310, rows * 330), (20, 20, 20))
    dr = ImageDraw.Draw(S)
    try:
        f = ImageFont.truetype("arial.ttf", 26)
    except OSError:
        f = ImageFont.load_default()
    for n, (k, t) in enumerate(cells):
        x, y = (n % cols) * 310 + 5, (n // cols) * 330 + 28
        S.paste(t, (x, y))
        dr.text((x, y - 27), f"#{k} {imgs[k]['w']}x{imgs[k]['h']}", fill=(255, 220, 90), font=f)
    S.save(OUT / f"{slug}.jpg", quality=80)


def main() -> None:
    sys.path.insert(0, str(ROOT))
    OUT.mkdir(parents=True, exist_ok=True)
    titles_ch = json.loads((ROOT / "data" / "channel_titles" / "CL.json").read_text(encoding="utf-8"))["videos"]
    rows = [l.split("\t") for l in (ROOT / "data" / "stier" / "cases.tsv").read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]
    want = set(sys.argv[1:])
    for slug, pages, keys in rows:
        if want and slug not in want:
            continue
        dst = OUT / f"{slug}.json"
        if dst.exists() and not want:
            continue
        hits = [v["title"] for v in titles_ch for k in keys.split("|") if k.lower() in v["title"].lower()]
        arts = [article(t) for t in pages.split("|")]
        files = list(dict.fromkeys(f for a in arts for f in a["images"]))
        if len(files) < 12:   # bài ít ảnh -> tìm thêm trên Commons theo tên bài
            files += [f for a in arts if a["title"] for f in commons_search(a["title"]) if f not in files]
        imgs = [i for i in imageinfo(files) if PD.search(i["license"]) and not SKIP.search(i["file"])
                and i["mime"] in ("image/jpeg", "image/png", "image/tiff", "image/gif") and min(i["w"], i["h"]) >= 400]
        imgs.sort(key=lambda i: -i["w"] * i["h"])
        rec = {"slug": slug, "channel_hits": sorted(set(hits)), "articles": arts, "images": imgs}
        dst.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        sheet(slug, imgs)
        print(f"{slug:12} chars={sum(len(a['text']) for a in arts):6} pd_imgs={len(imgs):3} "
              f"{'TRÙNG KÊNH: ' + '; '.join(sorted(set(hits)))[:120] if hits else ''}", flush=True)


if __name__ == "__main__":
    main()
