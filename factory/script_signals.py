"""Tín hiệu chẩn đoán của kịch bản — CHỈ GHI, không chấm điểm, không chặn.

Rút từ branch feat/improve-short-content-pipeline (S10, 28/09/2026): chưa có
dữ liệu retention thì mọi ngưỡng đều đoán mò. Ghi tín hiệu cạnh số liệu thật
(scripts/analytics_report.py) để sau này biết tín hiệu nào đi cùng retention.
"""
from __future__ import annotations

import re

from factory.pillars.check import sentences

WPM = (170, 200)          # tốc độ đọc tiếng Việt dùng để quy từ -> giây


def signals(script: str) -> dict:
    s = sentences(script)
    words = script.split()
    first = s[0] if s else ""
    nums = re.findall(r"\d+", script)
    caps = re.findall(r"(?<![.!?]\s)(?<!^)\b[A-ZĐÀ-Ỹ][a-zà-ỹđ]+", script)
    return {
        "words": len(words),
        "sentences": len(s),
        "first_sentence_words": len(first.split()),
        "hook_is_question": first.endswith("?"),
        "first_answer_sec": _first_answer_sec(s),
        "max_sentence_words": max((len(x.split()) for x in s), default=0),
        "digits": len(nums),
        "capitalized_terms": len(caps),
        "ends_with_question": bool(s) and s[-1].endswith("?"),
        "est_seconds": [round(len(words) / w * 60, 1) for w in WPM],
    }


def _first_answer_sec(sents: list[str]) -> float | None:
    """Hook là câu hỏi thì câu trả lời bắt đầu sau bao nhiêu giây (≈170 từ/phút).

    Audit v1 (branch feat, research.md): 6/8 Short mất 4–8 giây đầu mới vào ý."""
    if not sents or not sents[0].endswith("?"):
        return None
    return round(len(sents[0].split()) / WPM[0] * 60, 1)
