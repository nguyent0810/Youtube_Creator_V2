"""Dựng ``scenes`` từ lời đọc và dấu cuối câu. Hàm thuần: không đọc, không ghi đĩa.

Dấu không có thì ra ``kinetic`` (cụm chữ cắt từ chính câu đó). Lệnh in số câu không dấu
để khỏi dựng một video toàn một kiểu mà không ai thấy.
"""
from __future__ import annotations


def _text(line) -> str:
    return line if isinstance(line, str) else line.get("t", "")


def _kind(raw: str) -> tuple[str, str]:
    if ":" in raw:
        kind, arg = raw.split(":", 1)
        return kind.strip().lower(), arg.strip()
    return raw.strip().lower(), ""


def _nl(s: str) -> str:
    return s.replace("\\n", "\n")


def _kinetic(i: int, line) -> dict:
    words = _text(line).split()
    if not words:
        raise ValueError(f"câu {i} rỗng, không cắt được chữ")
    phrase = " ".join(words[:4]).strip(".,;:!?…\"“”").upper()
    if len(phrase) > 32 and " " in phrase:
        phrase = phrase[:32].rsplit(" ", 1)[0]
    return {"type": "kinetic", "at": i, "items": [{"text": phrase, "at": [i, words[0]]}]}


def _marked(i: int, line, raw: str, lines) -> dict:
    kind, arg = _kind(raw)
    if kind == "quote":
        qline = i if isinstance(line, dict) and line.get("q") else next(
            (j for j, ln in enumerate(lines) if isinstance(ln, dict) and ln.get("q")), None)
        if qline is None:
            raise ValueError(f"câu {i}: dấu quote nhưng không có câu »")
        src = lines[qline]
        scene = {"type": "quote", "at": i, "text": _text(src), "qline": qline}
        if isinstance(src, dict) and src.get("diy"):
            scene["dy"] = True
            scene["by"] = "DIỄN Ý"
        elif isinstance(src, dict) and src.get("tr"):
            scene["by"] = "TRÍCH DỊCH"
        return scene
    if kind == "slam":
        if not arg:
            raise ValueError(f"câu {i}: slam thiếu chữ")
        return {"type": "slam", "at": i, "text": _nl(arg), "white": True}
    if kind == "date":
        if "|" in arg:
            day, date = [x.strip() for x in arg.split("|", 1)]
        else:
            day, date = arg, arg
        if not date:
            raise ValueError(f"câu {i}: date thiếu nhãn")
        return {"type": "date", "at": i, "day": day, "date": date}
    if kind == "counter":
        if "|" not in arg:
            raise ValueError(f"câu {i}: counter cần 'số | đơn vị'")
        num, label = [x.strip() for x in arg.split("|", 1)]
        return {"type": "counter", "at": i, "from": 0, "to": int(num), "suffix": " " + label, "label": label}
    if kind == "question":
        if not arg:
            raise ValueError(f"câu {i}: question thiếu câu hỏi")
        return {"type": "question", "at": i, "text": _nl(arg)}
    if kind == "chapter":
        if "|" not in arg:
            raise ValueError(f"câu {i}: chapter cần 'số | tiêu đề'")
        no, title = [x.strip() for x in arg.split("|", 1)]
        return {"type": "chapter", "at": i, "no": no, "k": f"CHƯƠNG {no}", "title": _nl(title)}
    raise ValueError(f"câu {i}: dấu lạ {kind!r}")


def scenes_from(lines, marks) -> list[dict]:
    by_i = {m["i"]: m["raw"] for m in marks}
    out = []
    for i, line in enumerate(lines):
        raw = by_i.get(i)
        out.append(_marked(i, line, raw, lines) if raw else _kinetic(i, line))
    return out


def unmarked_count(lines, marks) -> int:
    marked = {m["i"] for m in marks}
    return sum(1 for i in range(len(lines)) if i not in marked)
