"""Soát một video dài theo luật mượn từ bộ skill shorts-studio / long-video (vietneu-tts, nhánh feat/shorts-studio; áp dụng 14/10/2026).

    python motion/long/studio_lint.py <topic> [--strict]

Đọc data/long/<topic>/chNN.json (lines + scenes, sau script_lines.py + gen_scenes.py). In cảnh báo; --strict thoát 1 khi có LỖI.

LỖI (đã từng tới tay người xem):
  - câu đọc dài hơn 35 tiếng (TTS hụt hơi, người nghe mất mạch);
  - counter đếm tới một NĂM (1500-2100) mà không đứng yên ("năm không đếm từ 0");
  - counter có from/to 1000-2100, không suffix, không khai "year" (engine chấm nghìn: 1996 -> "1.996");
  - counter có chữ số hoặc "<" trong prefix mà không đứng yên (số trung gian đọc như dữ kiện thật).
CẢNH BÁO (giữ chân):
  - cả chương ít câu ngắn (<= 6 tiếng): cần khoảng 1 câu mỗi 4-6 câu, đặt sau phán định hoặc khoảnh khắc cảm xúc;
  - liệt kê quá 3 mục trong một câu đọc (phần còn lại đưa lên màn hình);
  - 3 cảnh liền nhau cùng một loại, hoặc cả chương có ít hơn 3 loại cảnh;
  - quá 1 cảnh "tròn"/đếm (counter) liền nhau; mốc hiện phần tử cuối cách hết cảnh dưới 1,5 giây thì build_long đã báo riêng.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def year_counter_issues(scenes) -> list[str]:
    """Counter có số 1000-2100 mà không suffix phải khai "year": true (năm, không chấm nghìn) hoặc false (số lượng).

    26/10/2026: Short Turing đếm 1950 -> 2000 hiện "1.996". Không đoán bằng nhãn như vietneu-tts: "THÀNH VIÊN BỊ LOẠI
    MỖI NĂM" (yakuza, 2000) và "MẶT NẠ PHÒNG ĐỘC" (shanghai, 1000) là số lượng. Dùng chung cho build.py (Short)."""
    out = []
    for i, s in enumerate(scenes or []):
        if s.get("type") != "counter" or "year" in s or str(s.get("suffix") or "").strip():
            continue
        nums = [n for n in (s.get("from", 0), s["to"]) if float(n).is_integer() and 1000 <= n <= 2100]
        if nums:
            out.append(f"cảnh {i}: counter {int(nums[-1])} -- khai \"year\": true (năm, hiện 1996) hoặc false (số lượng, hiện 1.996)")
    return out


def text_of(ln) -> str:
    return ln["t"] if isinstance(ln, dict) else ln


def sentences(t: str) -> list[str]:
    return [x.strip() for x in re.split(r"(?<=[.!?…])\s+", t.replace("‖", " ")) if x.strip()]


def lint(topic: str) -> tuple[list[str], list[str]]:
    err, warn = [], []
    for p in sorted((ROOT / "data" / "long" / topic).glob("ch[0-9][0-9].json")):
        ch = json.loads(p.read_text(encoding="utf-8"))
        name, sents = p.stem, []
        for i, ln in enumerate(ch.get("lines") or []):
            for s in sentences(text_of(ln)):
                n = len(s.split())
                sents.append(n)
                if n > 35:
                    err.append(f"{name} dòng {i}: câu {n} tiếng (> 35): {s[:70]}…")
                if s.count(",") >= 4 and not re.search(r"\d", s) and n < 30:
                    warn.append(f"{name} dòng {i}: có vẻ liệt kê hơn 3 mục trong một câu: {s[:70]}…")
        if len(sents) >= 10:
            short = sum(1 for n in sents if n <= 6)
            if short * 7 < len(sents):
                warn.append(f"{name}: {short}/{len(sents)} câu ngắn (<= 6 tiếng); cần khoảng 1 câu mỗi 4-6 câu")
        types = [s["type"] for s in ch.get("scenes") or []]
        body = [t for t in types if t not in ("chapter", "brand", "endcard")]
        if len(body) >= 5 and len(set(body)) < 3:
            warn.append(f"{name}: chỉ {len(set(body))} loại cảnh ({sorted(set(body))}); cần >= 3")
        for i in range(2, len(types)):
            if types[i] == types[i - 1] == types[i - 2] and types[i] not in ("broll",):
                warn.append(f"{name} cảnh {i - 2}-{i}: ba cảnh '{types[i]}' liền nhau")
        err += [f"{name} {m}" for m in year_counter_issues(ch.get("scenes"))]
        for i, s in enumerate(ch.get("scenes") or []):
            if s["type"] != "counter":
                continue
            moving = s.get("from", 0) != s["to"]
            if moving and float(s["to"]).is_integer() and 1500 <= s["to"] <= 2100 and not s.get("suffix") and s.get("year") is not False:
                err.append(f"{name} cảnh {i}: counter đếm tới năm {int(s['to'])} (đặt from = to hoặc dùng kinetic/date)")
            if moving and re.search(r"[\d<>≈~]", str(s.get("prefix") or "")):
                err.append(f"{name} cảnh {i}: counter prefix {s['prefix']!r} mà số còn chạy")
    return err, warn


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from factory.console import utf8_console
    utf8_console()  # console Windows cp1252 không in được tiếng Việt (retro 2 mục 7)
    topic = sys.argv[1]
    err, warn = lint(topic)
    out = sys.stdout
    try:
        out.reconfigure(encoding="utf-8")
    except Exception:
        pass
    for w in warn:
        print("  ! " + w)
    for e in err:
        print("  LỖI " + e)
    print(f"{topic}: {len(err)} lỗi, {len(warn)} cảnh báo (luật studio)")
    return 1 if err and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
