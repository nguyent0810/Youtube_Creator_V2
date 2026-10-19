"""Toàn vẹn văn bản — cổng CỨNG ngay trước TTS, chung cho cả 3 kênh.

Chuyển thể từ S8 của branch feat/improve-short-content-pipeline (28/09/2026).
Lỗi thật ở v1: một script E2E lặp một câu ba lần mà vẫn đi tới TTS; mảnh
markup/nhãn "Phương án" lọt vào lời đọc. Bộ kiểm của v2 soi độ dài, hook,
trích dẫn... nhưng chưa soi mấy lỗi "chắc chắn sai" này.

Kiểm trên TEXT SẼ THẬT SỰ ĐƯỢC ĐỌC (đã bóc `**` giống speak.strip_emphasis):
  CHẶN     câu lặp (nguyên văn hoặc sau chuẩn hoá)          INT_REPEATED_SENTENCE
  CHẶN     markup/ký hiệu sót (*, [], {}, #, `, URL, JSON)  INT_LEFTOVER_MARKUP
  KHÔNG    câu cuối thiếu dấu kết câu (có thể cố ý)         INT_TRUNCATED
Đặt ở run_batch trước TTS: MỘT điểm cho mọi kênh, mọi dòng, mọi đường vào.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

_SENT = re.compile(r"[^.!?…\n]+(?:[.!?…]+[\"'”’»)]*)?")
_TERMINAL = re.compile(r"[.!?…][\"'”’»)]*\s*$")
_MARKUP = [
    ("asterisk", re.compile(r"\*+")),
    ("square_bracket", re.compile(r"[\[\]]")),
    ("curly_brace", re.compile(r"[{}]")),
    ("hash", re.compile(r"#")),
    ("backtick", re.compile(r"`")),
    ("angle_token", re.compile(r"<\||\|>")),
    ("json_key", re.compile(r"\"\w+\"\s*:")),
    ("candidate_label", re.compile(r"\bPhương án\s+[A-D]\b", re.IGNORECASE)),
    ("url", re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)),
]


@dataclass(frozen=True)
class Finding:
    code: str
    span: str
    blocking: bool


def spoken(script: str) -> str:
    """Bóc `**nhấn mạnh**` như bước TTS (speak.strip_emphasis) rồi mới kiểm."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", script or "")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def check(script: str) -> list[Finding]:
    text = spoken(script)
    sents = [m.group(0).strip() for m in _SENT.finditer(text) if m.group(0).strip()]
    out: list[Finding] = []
    seen: set[str] = set()
    for s in sents:
        n = _norm(s)
        if n and n in seen:
            out.append(Finding("INT_REPEATED_SENTENCE", s, True))
        seen.add(n)
    # Quét markup trên TOÀN text: cắt câu theo dấu chấm làm vỡ URL trước khi nhận ra.
    for kind, pat in _MARKUP:
        for m in pat.finditer(text):
            out.append(Finding(f"INT_LEFTOVER_MARKUP:{kind}", m.group(0), True))
    if sents and not _TERMINAL.search(sents[-1]):
        out.append(Finding("INT_TRUNCATED", sents[-1], False))
    return out


def blocking(script: str) -> list[Finding]:
    return [f for f in check(script) if f.blocking]


def leftover_markup(text: str) -> list[Finding]:
    """Chỉ markup sót -- cho motion/stier và motion/long (bước 5). Ở đó câu lặp
    có thể cố ý (câu chốt nhắc lại tên vụ án), nên không soi. Soi chuỗi THÔ:
    hai bộ dựng đó không bóc `**nhấn mạnh**` như speak.strip_emphasis."""
    return [Finding(f"INT_LEFTOVER_MARKUP:{kind}", m.group(0), True)
            for kind, pat in _MARKUP for m in pat.finditer(text or "")]


def require_speakable(text: str) -> None:
    """Ném ValueError nếu chuỗi SẮP ĐƯA VÀO TTS còn markup (*, [], URL...).
    Gọi ngay trước engine.infer -- không soi spec (tiêu đề cảnh, nguồn)."""
    bad = leftover_markup(text)
    if bad:
        raise ValueError(f"markup sót trong câu sắp đọc ({bad[0].code} «{bad[0].span}»): {text[:80]!r}")
