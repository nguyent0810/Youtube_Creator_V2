"""Lấy toàn văn Bộ luật Hình sự 2015 (sửa đổi 2017) + đánh dấu điều bị Luật 86/2025/QH15 sửa.

    python scripts/fetch_blhs.py   -> data/blhs.json

Văn bản quy phạm pháp luật không thuộc đối tượng bảo hộ quyền tác giả
(Luật SHTT Điều 15), nên được trích nguyên văn.

VÌ SAO PHẢI ĐÁNH DẤU 2025: bản hợp nhất trên Wikisource dừng ở 2017. Luật
86/2025/QH15 (hiệu lực 01/07/2025) sửa ~30 điều, trong đó bỏ tử hình ở 8 tội.
Đọc khung hình phạt từ bản 2017 cho các điều đó là SAI -- đúng loại lỗi
nguồn đã gặp với vnlunar. Điều nào có số xuất hiện trong phần sửa đổi thì
gắn `sua_2025 = true`; khuôn "điều luật" CHẶN các điều này. Đánh dấu thừa
(điều chỉ được nhắc tới) còn hơn bỏ sót.
"""
import html
import json
import re
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "blhs.json"
BASE = "Bộ luật Hình sự nước Cộng hòa xã hội chủ nghĩa Việt Nam 2015 (sửa đổi, bổ sung 2017)"
AMEND = "Luật sửa đổi, bổ sung một số điều của Bộ luật Hình sự nước Cộng hòa xã hội chủ nghĩa Việt Nam 2025"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV",
         "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI"]


def page_text(title: str) -> str:
    q = urllib.parse.urlencode({"action": "parse", "page": title, "prop": "text",
                                "format": "json", "formatversion": 2})
    req = urllib.request.Request("https://vi.wikisource.org/w/api.php?" + q,
                                 headers={"User-Agent": "yt-factory/1.0 (content research)"})
    for attempt in range(5):                      # Wikimedia trả 429 khi gọi dồn
        try:
            h = json.load(urllib.request.urlopen(req, timeout=60))["parse"]["text"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S)
    h = re.sub(r"<sup[^>]*>.*?</sup>", "", h, flags=re.S)          # chú thích [12]
    h = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</h\d>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace("​", "")
    return re.sub(r"\n\s*\n+", "\n", t)


def parse_articles(text: str, chuong: str) -> dict:
    out = {}
    parts = re.split(r"(?m)^\s*Điều (\d+[a-z]?)\.\s*", text)
    for i in range(1, len(parts) - 1, 2):
        so, body = parts[i], parts[i + 1]
        lines = [ln.strip() for ln in body.strip().split("\n") if ln.strip()]
        if not lines:
            continue
        ten = re.sub(r"\[\d+\]", "", lines[0]).strip()
        noi_dung = "\n".join(re.sub(r"\[\d+\]", "", ln) for ln in lines[1:])
        noi_dung = re.split(r"(?m)^(?:Chương|Mục) [IVXLC\d]+", noi_dung)[0].strip()
        out[so] = {"so": so, "ten": ten, "chuong": chuong, "noi_dung": noi_dung}
    return out


def main() -> None:
    arts = {}
    for k, r in enumerate(ROMAN):
        phan = "Phần thứ nhất" if k < 12 else "Phần thứ hai"
        title = f"{BASE}/{phan}/Chương {r}"
        try:
            t = page_text(title)
        except Exception as exc:
            print(f"  lỗi {title}: {exc}")
            continue
        got = parse_articles(t, f"Chương {r}")
        arts.update(got)
        print(f"  Chương {r:5s} {len(got):3d} điều")
        time.sleep(2)

    amend = page_text(AMEND)
    i, j = amend.find("Điều 1."), amend.find("Điều 2.")
    body = amend[i:j]
    touched = set(re.findall(r"Điều (\d+[a-z]?)", body))
    for m in re.finditer(r"các điều ([\d,\s và]+)", body):
        touched |= set(re.findall(r"\d+", m.group(1)))
    for so, a in arts.items():
        a["sua_2025"] = so in touched
    data = {"nguon": f"https://vi.wikisource.org/wiki/{urllib.parse.quote(BASE)}",
            "nguon_sua_doi": "Luật 86/2025/QH15, https://vi.wikisource.org/wiki/" + urllib.parse.quote(AMEND),
            "ghi_chu": "sua_2025=true: điều bị Luật 86/2025 sửa hoặc nhắc tới — KHÔNG đọc khung phạt từ bản 2017",
            "dieu": arts}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(arts)} điều · {sum(a['sua_2025'] for a in arts.values())} điều gắn sua_2025 -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
