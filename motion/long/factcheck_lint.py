"""Soát đối chiếu dữ kiện giữa kịch bản/cảnh và factcheck.

    python motion/long/factcheck_lint.py <topic>

Không suy diễn sự thật từ mạng: công cụ chỉ kiểm rằng số, ngày và TRÍCH DỊCH
đã có dấu vết trong factcheck.md hoặc research.md của chính topic.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from factory.console import utf8_console
NUMBER = re.compile(r"(?<![\w#])(?:\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{1,2}[./-]\d{4}|\d[\d.,]*)(?!\w)")
URL = re.compile(r"https?://\S+")
SPOKEN_UNIT = re.compile(r"\b(\d[\d.,]*)[ \t]+(nghìn|ngàn|triệu|tỷ|tỉ)\b", re.I)
UNITS = {"nghìn": 1_000, "ngàn": 1_000, "triệu": 1_000_000, "tỷ": 1_000_000_000, "tỉ": 1_000_000_000}
CHAPTER_ORDINAL = re.compile(r"\bchương\s+\d+\b", re.I)
MONTH_LABEL = re.compile(r"\btháng\s+(0?[1-9]|1[0-2])\b", re.I)


def _normal_number(value: str) -> str:
    return re.sub(r"[.,]", "", value).lstrip("0") or "0"


def _spoken_amount(raw: str, unit: int) -> str:
    """Normalize Vietnamese spoken amounts without treating decimal commas as thousands."""
    if "," in raw:
        whole, fraction = raw.rsplit(",", 1)
        if 1 <= len(fraction) <= 2:
            numerator = int(re.sub(r"[.,]", "", whole) + fraction)
            return str(numerator * unit // (10 ** len(fraction)))
    return str(int(_normal_number(raw)) * unit)


def _standalone_month_number_spans(text: str) -> set[tuple[int, int]]:
    """Return month-label numbers, but retain dates with a year or a day.

    A calendar label such as ``LỊCH TỚI THÁNG 8`` is interface text, not a
    factual claim.  Its number may normalize to the same value as a decimal
    amount (``0,8``), so callers must compare source spans rather than values.
    """
    spans = set()
    for match in MONTH_LABEL.finditer(text):
        suffix = text[match.end():]
        prefix = text[:match.start()]
        has_year = re.match(r"\s*(?:năm\s*)?\d{4}\b", suffix, re.I)
        has_day_after = re.match(r"\s*ngày\s+\d{1,2}\b", suffix, re.I)
        has_day_before = re.search(r"\bngày\s+\d{1,2}\s*$", prefix, re.I)
        if not (has_year or has_day_after or has_day_before):
            spans.add(match.span(1))
    return spans


def numbers(text: str) -> set[str]:
    out = set()
    spoken = list(SPOKEN_UNIT.finditer(text))
    spoken_number_spans = {(match.start(1), match.end(1)) for match in spoken}
    chapter_number_spans = {(match.start(), match.end()) for match in CHAPTER_ORDINAL.finditer(text)}
    standalone_month_number_spans = _standalone_month_number_spans(text)
    for match in NUMBER.finditer(text):
        if (match.span() in spoken_number_spans
                or match.span() in standalone_month_number_spans
                or any(start <= match.start() < end for start, end in chapter_number_spans)):
            continue
        value = match.group(0)
        # Đối chiếu ngày theo từng thành phần để 07.02.1997 và 7/2/1997 là một
        # mốc, còn 50.000 vẫn là một số lượng duy nhất.
        if re.fullmatch(r"\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{1,2}[./-]\d{4}", value):
            out.update(_normal_number(part) for part in re.split(r"[./-]", value))
        else:
            normalized = _normal_number(value)
            if normalized != "0":  # giá trị trục 0 không phải một khẳng định dữ kiện
                out.add(normalized)
    # Giữ một dạng duy nhất: "50 nghìn" và "50.000" đều là 50000.
    for match in spoken:
        normalized = _spoken_amount(match.group(1), UNITS[match.group(2).casefold()])
        if normalized != "0":
            out.add(normalized)
    return out


def _display_strings(value, key="") -> list[str]:
    """Lấy chữ sẽ hiện trong scene, bỏ khoá kỹ thuật và tên asset."""
    skip = {"type", "img", "bg", "vid", "at", "focus", "credit", "move", "year", "geo", "class", "id", "src",
            "no", "dates", "xlab", "xstep"}
    if key in skip:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [s for item in value for s in _display_strings(item, key)]
    if isinstance(value, dict):
        # A fully-labelled example is not an externally checkable claim.
        # Its numbers are assumptions, not facts to source.
        if "type" in value and any("GIẢ ĐỊNH" in str(value.get(field, "")).upper()
                                  for field in ("title", "unit", "range")):
            return []
        local_skip = set(skip)
        if value.get("type") == "calendar":
            local_skip.update({"title", "from", "days", "months", "endAt"})
        return [s for k, item in value.items() if k not in local_skip for s in _display_strings(item, k)]
    return []


def _script_text(topic_dir: Path) -> str:
    script = topic_dir / "script.md"
    if not script.exists():
        return ""
    # Header CH01, bảng số thứ tự và URL nguồn không phải lời đọc.
    return "\n".join(line for line in script.read_text(encoding="utf-8").splitlines()
                     if not line.lstrip().startswith(("#", "|", "http")))


def article_text(topic_dir: Path) -> str:
    text = _script_text(topic_dir)
    for path in sorted(topic_dir.glob("ch[0-9][0-9].json")):
        ch = json.loads(path.read_text(encoding="utf-8"))
        text += "\n" + "\n".join(str(x.get("t", x)) if isinstance(x, dict) else str(x) for x in ch.get("lines") or [])
        text += "\n" + "\n".join(_display_strings(ch.get("scenes") or []))
    return text


def evidence_text(topic_dir: Path) -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in (topic_dir / "factcheck.md", topic_dir / "research.md") if path.exists())


def translation_issues(article: str, factcheck: str) -> list[str]:
    # script.md và chNN.json cùng chứa lời đọc sau script_lines.py; cùng một câu
    # chỉ tính một lần, không biến bản sao kỹ thuật thành hai yêu cầu nguồn.
    labels = len({line.strip() for line in article.splitlines() if re.search(r"TRÍCH\s+DỊCH", line, re.I)})
    tagged = [line for line in factcheck.splitlines() if re.search(r"TRÍCH\s+DỊCH", line, re.I)]
    valid = [line for line in tagged if URL.search(line) and re.search(r"(?:nguyên\s+văn|original)\s*[:—-].*[A-Za-z]{3}", line, re.I)]
    if not labels:
        return []
    if len(valid) < labels:
        return [f"TRÍCH DỊCH: {labels} câu trong bài nhưng chỉ {len(valid)} mục có nguyên văn tiếng gốc và URL trong factcheck.md"]
    return []


def stale_factcheck_issues(article: str, factcheck: str) -> list[str]:
    """Mỗi dòng bảng theo chương có số phải còn ít nhất một số đó trong bản cuối.

    Đây là kiểm tra bảo thủ: mục không có số không bị kết luận là stale vì có thể
    đã được diễn đạt lại; một số biến mất hoàn toàn là dấu hiệu lệch bản rõ ràng.
    """
    article_numbers = numbers(article)
    out = []
    for line in factcheck.splitlines():
        if not re.match(r"\|\s*CH\d{2}\s*\|", line, re.I):
            continue
        claim = line.split("|")[2] if len(line.split("|")) > 2 else ""
        claimed = numbers(claim)
        material = {n for n in claimed if not (len(n) == 4 and 1500 <= int(n) <= 2100)}
        stale = bool(material - article_numbers) if material else not bool(claimed & article_numbers)
        if claimed and stale:
            chapter = re.search(r"CH\d{2}", line, re.I).group(0).upper()
            out.append(f"lệch bản final: mục {chapter} không còn số/ngày nào trong bài: {claim.strip()[:90]}")
    return out


def lint_content(article: str, evidence: str, factcheck: str) -> list[str]:
    """Phiên bản thuần để test luật mà không phải tạo topic giả trên đĩa."""
    if not evidence:
        return ["thiếu factcheck.md và research.md"]
    missing = sorted(numbers(article) - numbers(evidence), key=lambda n: (len(n), n))
    out = [f"số/ngày không có trong factcheck.md hoặc research.md: {n}" for n in missing]
    out += translation_issues(article, factcheck)
    out += stale_factcheck_issues(article, factcheck)
    return out


def lint_path(topic_dir: Path) -> list[str]:
    evidence = evidence_text(topic_dir)
    factcheck = (topic_dir / "factcheck.md").read_text(encoding="utf-8") if (topic_dir / "factcheck.md").exists() else ""
    return lint_content(article_text(topic_dir), evidence, factcheck)


def lint(topic: str) -> list[str]:
    return lint_path(ROOT / "data" / "long" / topic)


def main() -> int:
    utf8_console()
    topic = sys.argv[1]
    issues = lint(topic)
    for issue in issues:
        print("  LỖI " + issue)
    print(f"{topic}: {len(issues)} lỗi (factcheck)")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
