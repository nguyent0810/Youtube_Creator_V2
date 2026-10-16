"""Sàn sản xuất của video dài: một Long mới không được kém các Long đã chứng minh.

Ngày 11/10/2026 có 4 Long (escobar, capone, bulger, namcam) được dựng cách nhau ~25 phút: kịch bản
1.300–2.100 âm tiết (7–11 phút), 0 ảnh, 0 b-roll, 0 bản đồ, 94% cảnh là chữ trên nền trống — mỗi cảnh
là 4 từ đầu câu do scenes_from tự cắt. Cổng `craft` không chặn vì nó chỉ soi từng câu, không soi tư liệu.

Sàn này đo đúng những thứ đó. Ngưỡng lấy từ 6 Long đã đăng (yakuza, mafia, shanghai, ripper, kowloon,
golden) — cả 6 đều qua, nên sàn áp cho MỌI topic, không cần cờ bật/tắt:

                      thấp nhất trong 6 Long     sàn
  âm tiết kịch bản            5.610             5.000   (≈ 23 phút ở 215 âm tiết/phút)
  số chương                      12                10
  số loại cảnh                   19                14
  ảnh khác nhau dùng             49                40
  cảnh có b-roll                 35                30
  tỷ lệ kinetic (cao nhất)      34%            ≤ 38%
  chữ trên nền trống (cao nhất) 10%            ≤ 12%

`build_long.py html` in cảnh báo; `render` (bản thật), `final` và `publish_long.py` TỪ CHỐI.
Hàm thuần: nhận spec + chương đã đọc, không đụng đĩa (trừ has_research).
"""
from __future__ import annotations

from pathlib import Path

MIN_SYL = 5000
MIN_CHAPTERS = 10
MIN_TYPES = 14
MIN_IMGS = 40
MIN_VID_SCENES = 30
MAX_KINETIC = 0.38
MAX_NAKED = 0.12
MIN_FINAL_MIN = 20.0          # final.mp4 ngắn hơn thế này thì không đăng như một Long
_TEXT_ONLY = {"kinetic", "slam", "date", "counter", "question", "quote"}


def _text(line) -> str:
    return line if isinstance(line, str) else line.get("t", "")


def _imgs(s: dict) -> list[str]:
    out = [s.get("img"), s.get("bg"), (s.get("a") or {}).get("img"), (s.get("b") or {}).get("img")]
    return [x for x in out if x]


def measure(chapters) -> dict:
    """chapters: [(name, ch_dict)] như build_long.load trả về."""
    syl = total = kinetic = naked = vid = auto = 0
    types, imgs = set(), set()
    for _, ch in chapters:
        syl += sum(len(_text(ln).split()) for ln in ch.get("lines", []))
        for s in ch.get("scenes", []):
            total += 1
            types.add(s.get("type"))
            imgs.update(_imgs(s))
            kinetic += s.get("type") == "kinetic"
            vid += bool(s.get("vid"))
            auto += bool(s.get("auto"))
            if s.get("type") in _TEXT_ONLY and not _imgs(s) and not s.get("vid"):
                naked += 1
    return {"syl": syl, "chapters": len(chapters), "scenes": total, "types": len(types), "imgs": len(imgs),
            "vid_scenes": vid, "auto": auto, "kinetic": kinetic / total if total else 1.0, "naked": naked / total if total else 1.0}


def problems(chapters) -> list[str]:
    m = measure(chapters)
    out = []
    if m["auto"]:
        out.append(f"{m['auto']} cảnh do scenes_from tự cắt 4 từ đầu câu (\"auto\") chưa ai biên tập: đó là bản nháp, không phải cảnh")
    if m["syl"] < MIN_SYL:
        out.append(f"kịch bản {m['syl']} âm tiết (≈{m['syl'] / 215:.0f} phút), sàn {MIN_SYL} (≈23 phút)")
    if m["chapters"] < MIN_CHAPTERS:
        out.append(f"{m['chapters']} chương, sàn {MIN_CHAPTERS}")
    if m["types"] < MIN_TYPES:
        out.append(f"chỉ {m['types']} loại cảnh, sàn {MIN_TYPES} (photo, map, file, split, ledger, bars, sketch, broll…)")
    if m["imgs"] < MIN_IMGS:
        out.append(f"dùng {m['imgs']} ảnh tư liệu, sàn {MIN_IMGS} — chạy research_long.py / media_search.py trước khi viết cảnh")
    if m["vid_scenes"] < MIN_VID_SCENES:
        out.append(f"{m['vid_scenes']} cảnh có b-roll, sàn {MIN_VID_SCENES}")
    if m["kinetic"] > MAX_KINETIC:
        out.append(f"{m['kinetic']:.0%} cảnh là kinetic, trần {MAX_KINETIC:.0%}")
    if m["naked"] > MAX_NAKED:
        out.append(f"{m['naked']:.0%} cảnh là chữ trên nền trống (không ảnh, không b-roll), trần {MAX_NAKED:.0%}")
    return out


def has_research(od: Path) -> bool:
    return (od / "research.json").exists()


def report(chapters) -> str:
    m = measure(chapters)
    return (f"{m['syl']} âm tiết · {m['chapters']} chương · {m['scenes']} cảnh · {m['types']} loại · {m['imgs']} ảnh · "
            f"{m['vid_scenes']} cảnh b-roll · kinetic {m['kinetic']:.0%} · chữ nền trống {m['naked']:.0%}")
