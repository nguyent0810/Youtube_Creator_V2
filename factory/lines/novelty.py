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

THIẾU HOẶC CŨ THÌ DỪNG (audit 08/10/2026): file này bị gitignore và chỉ
schedule_audit.py ghi ra; bản cũ thiếu file thì coi như kênh TRỐNG -- chống
trùng tắt im lặng trên mọi máy mới. Giờ thiếu file, hoặc file cũ hơn
MAX_AGE, là ném TitlesUnavailable. Đặt YF_ALLOW_STALE_TITLES=1 nếu cố ý
chạy không có dữ liệu kênh (chỉ để thử nghiệm, có cảnh báo).

KIỂU BỎ DẤU CŨ/MỚI: "Hoà thượng" và "Hòa thượng" là cùng một chữ. So khớp
trên dạng chuẩn hoá (dấu thanh dời về cuối âm tiết), nên hai lối gõ không
còn lọt nhau.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TITLES_DIR = ROOT / "data" / "channel_titles"
MAX_AGE = timedelta(days=3)
GENERIC_TOP = 30
_TONES = {"\u0300", "\u0301", "\u0303", "\u0309", "\u0323"}   # huyền sắc ngã hỏi nặng


class TitlesUnavailable(RuntimeError):
    """Không có (hoặc quá cũ) danh sách tiêu đề kênh: không kiểm trùng được thì không đi tiếp."""


def _canon(w: str) -> str:
    """Âm tiết dạng chuẩn: dấu thanh dời về cuối -> "hoà" == "hòa", "thuỷ" == "thủy"."""
    d = unicodedata.normalize("NFD", w)
    return "".join(c for c in d if c not in _TONES) + "".join(c for c in d if c in _TONES)


STOP = {_canon(w) for w in (
    "có là không và của một những các cho được với thì mà vì sao hay này đó trong khi người bạn "
    "mình phải thật chỉ lại gì ai nào đi ra vào thế như từ đến tại để lên ở nhé ơi rồi đã sẽ "
    "đang cũng rất quá nên còn nữa hơn nhất").split()}


def _tokens(t: str) -> list[str | None]:
    """Âm tiết (giữ dấu, dạng chuẩn); số và ký hiệu thành None để NGẮT cụm
    ("lúc 11 giờ" không được dính thành "lúc giờ")."""
    t = unicodedata.normalize("NFC", t.lower())
    return [None if w.isdigit() else _canon(w) for w in re.split(r"[^\w]+", t) if w]


def syllables(t: str) -> list[str]:
    return [w for w in _tokens(t) if w]


def bigrams(t: str) -> set[str]:
    s = _tokens(t)
    return {f"{a} {b}" for a, b in zip(s, s[1:]) if a and b and a not in STOP and b not in STOP}


def _head(t: str) -> str | None:
    """Cụm chủ thể mở đầu: cặp âm tiết LIỀN NHAU đầu tiên, không hư từ, không bị
    số ngắt. (Lỗi thật: "Điều 172: Tội…" bỏ số thành "điều tội" -> mọi bài
    điều luật đều bị coi là trùng nhau.)"""
    s = [w if (w and w not in STOP) else None for w in _tokens(t)]
    return next((f"{a} {b}" for a, b in zip(s, s[1:]) if a and b), None)


@lru_cache(maxsize=None)
def _load(ch: str) -> tuple[list[dict], frozenset]:
    p = TITLES_DIR / f"{ch}.json"
    allow = os.environ.get("YF_ALLOW_STALE_TITLES") == "1"
    fix = f"chạy `python scripts/schedule_audit.py --channel {ch}` để làm mới"
    if not p.exists():
        if allow:
            print(f"CẢNH BÁO: thiếu {p} -- KHÔNG kiểm trùng chủ đề với kênh {ch}", file=sys.stderr)
            return [], frozenset()
        raise TitlesUnavailable(f"thiếu danh sách tiêu đề kênh {ch} ({p}) -- {fix}")
    data = json.loads(p.read_text(encoding="utf-8"))
    saved = datetime.fromisoformat(data.get("saved_at", "1970-01-01T00:00:00+00:00"))
    if saved.tzinfo is None:
        saved = saved.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) - saved > MAX_AGE and not allow:
        raise TitlesUnavailable(f"danh sách tiêu đề kênh {ch} đã cũ ({saved:%d/%m %H:%M}) -- {fix}")
    vids = data["videos"]
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
