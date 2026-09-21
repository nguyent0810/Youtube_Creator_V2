"""Lấy lời kinh + bản dịch Ngô Tất Tố từ Wikisource tiếng Việt.

    python scripts/fetch_kinhdich.py

VÌ SAO: luật kênh cấm tự bịa lời quẻ, hào từ. Lấy NGUYÊN VĂN chữ Hán và
DỊCH NGHĨA của Ngô Tất Tố (mất 1954, tác phẩm đã thuộc phạm vi công cộng),
kèm URL từng trang. Script kịch bản chỉ được trích từ file này.

HƯỚNG MỞ RỘNG TỰ ĐỘNG: ngày 21/09/2026 Wikisource mới có 9/64 quẻ. Chạy
lại script này định kỳ -- quẻ nào tình nguyện viên gõ thêm sẽ tự vào kho,
mỗi quẻ thêm khoảng 8 chủ đề (lời kinh, 6 hào, Tượng).
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "kinhdich_ntt.json"
API = "https://vi.wikisource.org/w/api.php"
UA = {"User-Agent": "yt-factory/1.0 (content research; contact via repo)"}
HAO_POS = {"初": 1, "二": 2, "三": 3, "四": 4, "五": 5, "上": 6}


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def _clean(s: str) -> str:
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"\{\{khác\|([^|}]*)\|[^}]*\}\}", r"\1", s)
    s = re.sub(r"\[\[Hình:[^\]]*\]\]", "", s)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    return re.sub(r"\s+", " ", s.replace("'''", "").replace("''", "")).strip(" .-")


def parse(raw: str) -> dict:
    num = re.search(r"Iching-hexagram-(\d+)", raw)
    blocks = re.findall(r"\{\{g\|LỜI KINH\s*'''(.*?)'''\}\}(.*?)(?=\{\{g\|LỜI KINH|\Z)", raw, re.S)
    out = {"so": int(num.group(1)) if num else None, "quai_tu": None, "hao": {},
           "thoan": None, "tuong": None}
    for zh, rest in blocks:
        m = re.search(r"'''Dịch nghĩa\. -'''(.*?)(?:\n\n|\Z)", rest, re.S)
        if not m:
            continue
        item = {"zh": _clean(zh), "vi": _clean(m.group(1))}
        z = item["zh"]
        hm = re.match(r"(初|上)[六九]|[六九](二|三|四|五)", z)
        if out["quai_tu"] is None:
            out["quai_tu"] = item
        elif hm and re.match(r"^[初上六九二三四五]+\s*[:：]", z):
            pos = HAO_POS[hm.group(1) or hm.group(2)]
            out["hao"].setdefault(str(pos), item)
        elif z.startswith("彖曰") and out["thoan"] is None:
            out["thoan"] = item
        elif z.startswith("象曰") and out["tuong"] is None:
            out["tuong"] = item
    return out


def main() -> None:
    q = urllib.parse.urlencode({"action": "query", "list": "allpages", "format": "json",
                                "apprefix": "Kinh Dịch/Chu Dịch", "aplimit": 500})
    titles = [p["title"] for p in json.loads(_get(f"{API}?{q}"))["query"]["allpages"]
              if "/Quẻ " in p["title"]]
    data = {}
    for t in titles:
        raw = _get("https://vi.wikisource.org/w/index.php?" +
                   urllib.parse.urlencode({"title": t, "action": "raw"}))
        rec = parse(raw)
        rec["ten"] = t.rsplit("/Quẻ ", 1)[1]
        rec["url"] = "https://vi.wikisource.org/wiki/" + urllib.parse.quote(t.replace(" ", "_"))
        if rec["so"]:
            data[str(rec["so"])] = rec
        print(f"  {rec['so']!s:>3} {rec['ten']:10s} lời kinh={'có' if rec['quai_tu'] else '—'} "
              f"hào={len(rec['hao'])}/6 tượng={'có' if rec['tuong'] else '—'}")
        time.sleep(1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(data)}/64 quẻ có bản dịch -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
