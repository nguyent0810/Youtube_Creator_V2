"""Chống trùng CHỦ ĐỀ với mọi video trên kênh — kể cả video không do v2 đăng.

LỖI THẬT (30/09/2026): 7/28 kịch bản Phật Giáo của v2 trùng chủ đề với video
nguồn khác đã có/đang hẹn trên kênh — có bài trùng nguyên tiêu đề ("Vì sao
tượng Phật có dái tai dài?"). Bộ chống trùng cũ chỉ so với lịch sử của v2.

CÁCH SO (bản 3): tiếng Việt mang nghĩa ở TỪ GHÉP -> so CẶP ÂM TIẾT liền nhau
(bigram), GIỮ DẤU. Bản 1 (bỏ dấu, từ đơn) bắt nhầm hàng loạt ("Pháp Cú" đụng
"chuyện cũ"); bản 2 (1 cụm hiếm là đủ) vẫn nhầm vì đo thật cho thấy độ hiếm
KHÔNG tách được trùng thật ("tai dài": 2 tiêu đề) với trùng nhầm ("tử tế": 3).
Trùng khi một trong ba:
  - chung >= 2 cụm âm tiết       ("tứ vô lượng tâm", "Phổ Hiền cưỡi voi")
  - Jaccard âm tiết >= 0.6          ("dái tai dài" ~ "đôi tai dài")
  - cùng MỞ ĐẦU bằng một cụm chủ thể ("Năm giới: …" ~ "Năm giới của Phật tử…")
Chấp nhận bắt thừa đôi chút: cái giá là bỏ một kịch bản, còn bỏ sót là đăng
lặp chủ đề lên kênh.

Danh sách tiêu đề: data/channel_titles/<KÊNH>.json, làm mới bằng
`python scripts/schedule_audit.py` (đọc toàn bộ playlist uploads).
"""
from __future__ import annotations

import collections
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TITLES_DIR = ROOT / "data" / "channel_titles"
GENERIC_TOP = 30
STOP = set("có là không và của một những các cho được với thì mà vì sao hay này đó trong khi người bạn "
           "mình phải thật chỉ lại gì ai nào đi ra vào thế như từ đến tại để lên ở nhé ơi rồi đã sẽ "
           "đang cũng rất quá nên còn nữa hơn nhất".split())


def _tokens(t: str) -> list[str | None]:
    """Âm tiết (giữ dấu); số và ký hiệu thành None để NGẮT cụm ("lúc 11 giờ"
    không được dính thành "lúc giờ")."""
    t = unicodedata.normalize("NFC", t.lower())
    return [None if w.isdigit() else w for w in re.split(r"[^\w]+", t) if w]


def syllables(t: str) -> list[str]:
    return [w for w in _tokens(t) if w]


def bigrams(t: str) -> set[str]:
    s = _tokens(t)
    return {f"{a} {b}" for a, b in zip(s, s[1:]) if a and b and a not in STOP and b not in STOP}


def _head(t: str) -> str | None:
    """Cụm chủ thể mở đầu tiêu đề (2 âm tiết đầu không phải hư từ)."""
    s = [w for w in syllables(t) if w not in STOP]
    return f"{s[0]} {s[1]}" if len(s) >= 2 else None


@lru_cache(maxsize=None)
def _load(ch: str) -> tuple[list[dict], frozenset]:
    p = TITLES_DIR / f"{ch}.json"
    if not p.exists():
        return [], frozenset()
    vids = json.loads(p.read_text(encoding="utf-8"))["videos"]
    freq = collections.Counter(bg for v in vids for bg in bigrams(v["title"]))
    return vids, frozenset(bg for bg, _ in freq.most_common(GENERIC_TOP))


def similar(a: str, b: str, generic: frozenset = frozenset()) -> bool:
    if len(bigrams(a) & bigrams(b)) >= 2:
        return True
    sa, sb = set(syllables(a)), set(syllables(b))
    if sa and sb and len(sa & sb) / len(sa | sb) >= 0.6:
        return True
    ha, hb = _head(a), _head(b)
    return bool(ha) and ha == hb and ha not in generic


def duplicate_on_channel(ch: str, title: str, exclude_ids: set | None = None) -> dict | None:
    """Video trên kênh trùng chủ đề với `title` (None nếu không có)."""
    vids, generic = _load(ch)
    for v in vids:
        if exclude_ids and v["id"] in exclude_ids:
            continue
        if similar(title, v["title"], generic):
            return v
    return None
