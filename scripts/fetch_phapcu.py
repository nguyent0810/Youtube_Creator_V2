"""Lấy 423 bài kệ Kinh Pháp Cú (Dhammapada): nguyên văn Pali + bản dịch Anh của
Bhikkhu Sujato (CC0, phạm vi công cộng) từ SuttaCentral.

    python scripts/fetch_phapcu.py   -> data/phapcu.json

Kịch bản tiếng Việt là DIỄN Ý từ bản CC0 này, ghi rõ nguồn và số kệ — không
trích bản dịch Việt còn bản quyền, không tự thêm lời Phật.
"""
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "phapcu.json"
RANGES = ["1-20", "21-32", "33-43", "44-59", "60-75", "76-89", "90-99", "100-115", "116-128",
          "129-145", "146-156", "157-166", "167-178", "179-196", "197-208", "209-220", "221-234",
          "235-255", "256-272", "273-289", "290-305", "306-319", "320-333", "334-359", "360-382",
          "383-423"]
PHAM = ["Song Yếu", "Không Phóng Dật", "Tâm", "Hoa", "Ngu", "Hiền Trí", "A-la-hán", "Ngàn",
        "Ác", "Hình Phạt", "Già", "Tự Ngã", "Thế Gian", "Phật Đà", "An Lạc", "Hỷ Ái", "Phẫn Nộ",
        "Cấu Uế", "Pháp Trụ", "Đạo", "Tạp Lục", "Địa Ngục", "Voi", "Tham Ái", "Tỳ-kheo", "Bà-la-môn"]


def get(uid: str) -> dict:
    url = f"https://suttacentral.net/api/bilarasuttas/{uid}/sujato?lang=en"
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "yt-factory/1.0"})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"không lấy được {uid}")


def main() -> None:
    verses = {}
    for k, rg in enumerate(RANGES):
        d = get(f"dhp{rg}")
        root, tr = d.get("root_text", {}), d.get("translation_text", {})
        by_verse: dict[int, dict] = {}
        for seg, txt in tr.items():
            m = re.match(r"dhp(\d+):(\d+)", seg)
            if not m or m.group(2) == "0":
                continue
            v = by_verse.setdefault(int(m.group(1)), {"en": [], "pi": []})
            v["en"].append(txt.strip())
            v["pi"].append(root.get(seg, "").strip())
        for n, v in by_verse.items():
            verses[str(n)] = {"so": n, "pham": k + 1, "ten_pham": PHAM[k],
                              "en": " ".join(x for x in v["en"] if x),
                              "pi": " ".join(x for x in v["pi"] if x),
                              "url": f"https://suttacentral.net/dhp{rg}/en/sujato#dhp{n}"}
        print(f"  phẩm {k + 1:2d} {PHAM[k]:14s} {len(by_verse):3d} kệ")
        time.sleep(1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"nguon": "SuttaCentral, Bhikkhu Sujato, 'Sayings of the Dhamma' (CC0)",
                               "ke": verses}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(verses)}/423 kệ -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
