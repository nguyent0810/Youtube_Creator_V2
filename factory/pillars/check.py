"""Bộ kiểm cho 4 pillar: Fact → Logic → Hook → Chốt → Độ mới → Độ dài.

TÁI DÙNG TỪ LỊCH, không viết lại:
  - luật "mọi claim ngoài nguồn phải xác minh" (claims.py) -> ở đây mọi câu
    trần thuật phải gắn với một Claim, và Claim tự TÍNH LẠI từ tables.py
  - danh sách cấm tuyệt đối / so sánh nhất / suy đoán (factcheck, claims)
  - kiểm chéo lô chống lặp khuôn (batchcheck) -> mở rộng thành kiểm với
    LỊCH SỬ của pillar, vì người xem hằng ngày nhớ cả tuần trước

Kịch bản là dữ liệu có cấu trúc: mỗi câu trần thuật phải trỏ về một Claim
có `verify()` trả True. Câu không có Claim đứng sau là câu tự bịa -> CẦN SỬA.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Callable

from factory.factcheck import ABSOLUTE, SUPERLATIVE
from factory.claims import SPECULATIVE

MIN_WORDS, MAX_WORDS = 65, 90
MAX_HOOK_WORDS, MAX_CLOSER_WORDS = 22, 14
OPENING_WORDS = 4

# Không khẳng định mệnh lý/chiêm tinh là khoa học; không hứa hẹn kết quả.
BANNED = ABSOLUTE + SUPERLATIVE + SPECULATIVE + (
    r"\b100\s*%", r"khoa học (?:đã )?chứng minh", r"\bchắc chắn (?:giàu|gặp)",
    r"\bđịnh mệnh đã\b", r"\bsẽ giàu\b", r"\bgặp họa\b")

# Hook phải có ít nhất một: câu hỏi, nghịch lý, đối lập, điều tưởng sai.
HOOK_MARKERS = ("?", "chưa chắc", "vậy mà", "nhưng", "lại", "tưởng",
                "ngược", "không phải", "mới là")

# Câu diễn giải truyền thống phải tự nói rõ đó là quan niệm, không phải fact.
HEDGES = ("theo cách luận", "truyền thống", "quan niệm", "trong lịch pháp",
          "theo", "được xem", "thường được", "xếp", "gọi là", "có thể", "thường gọi")


def _norm(s: str) -> str:
    d = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in d if not unicodedata.combining(c)).replace("đ", "d")


@dataclass(frozen=True)
class Claim:
    fragment: str                  # cụm chữ có trong câu
    verify: Callable[[], bool]     # tự tính lại từ tables / SOURCED
    basis: str                     # căn cứ, người đọc lại kiểm được
    kind: str = "table"            # table | source | doctrine | rhetoric


@dataclass
class Draft:
    pillar: str
    key: str                       # định danh chủ đề -> slug, lịch sử
    title: str
    script: str
    claims: list[Claim]
    sources: list[str]
    broll: list[str]
    angle: str                     # góc khai thác, để chống lặp góc
    names: set[str] = field(default_factory=set)   # tên riêng được phép


@dataclass
class Finding:
    ok: bool
    area: str
    msg: str


_SENT = re.compile(r"(?<=[.!?…])\s+")


def sentences(script: str) -> list[str]:
    return [s.strip() for s in _SENT.split(script.strip()) if s.strip()]


def check(d: Draft, all_names: set[str], history: list[dict]) -> list[Finding]:
    out: list[Finding] = []
    sents = sentences(d.script)
    words = len(d.script.split())

    # ─── FACT: mỗi claim tự tính lại ──────────────────────────────────────
    bad = [c.fragment for c in d.claims if not c.verify()]
    out.append(Finding(not bad, "FACT", f"claim sai khi tính lại: {bad}" if bad
                       else f"{len(d.claims)} claim đều tính lại khớp"))
    missing = [c.fragment for c in d.claims if _norm(c.fragment) not in _norm(d.script)]
    out.append(Finding(not missing, "FACT", f"claim khai mà không có trong script: {missing}"
                       if missing else "mọi claim đều có mặt trong script"))

    # Câu trần thuật không có claim đứng sau = tự bịa.
    orphan = [s for s in sents[1:] if not s.endswith("?")
              and not any(_norm(c.fragment) in _norm(s) for c in d.claims)]
    out.append(Finding(not orphan, "FACT", f"câu không có căn cứ: {orphan}"
                       if orphan else "mọi câu trần thuật đều có căn cứ"))

    # Tên riêng lạ (copy nhầm từ chủ đề khác).
    stray = sorted(n for n in all_names - d.names
                   if re.search(rf"(?<!\w){re.escape(n)}(?!\w)", d.script))
    out.append(Finding(not stray, "FACT", f"tên ngoài chủ đề: {stray}" if stray
                       else "không có tên riêng lạc chủ đề"))

    # ─── LOGIC ────────────────────────────────────────────────────────────
    hits = [p for p in BANNED if re.search(p, d.script, re.IGNORECASE)]
    out.append(Finding(not hits, "LOGIC", f"câu tuyệt đối/suy đoán: {hits}" if hits
                       else "không có câu tuyệt đối, so sánh nhất hay suy đoán"))
    unhedged = [c.fragment for c in d.claims if c.kind == "doctrine" and not any(
        h in next((s.lower() for s in sents if _norm(c.fragment) in _norm(s)), "")
        for h in HEDGES)]
    out.append(Finding(not unhedged, "LOGIC", f"quan niệm nói như fact: {unhedged}"
                       if unhedged else "quan niệm truyền thống đều có rào đón"))
    nosrc = [c.fragment for c in d.claims if c.kind == "source" and not d.sources]
    out.append(Finding(not nosrc, "LOGIC", "trích dẫn mà không ghi nguồn" if nosrc
                       else "trích dẫn đều có nguồn"))

    # ─── HOOK ─────────────────────────────────────────────────────────────
    hook = sents[0] if sents else ""
    hw = len(hook.split())
    hm = [m for m in HOOK_MARKERS if m in hook.lower()]
    out.append(Finding(bool(hm) and hw <= MAX_HOOK_WORDS, "HOOK",
                       f"hook {hw} từ, dấu hiệu {hm}" if hm and hw <= MAX_HOOK_WORDS
                       else f"hook yếu: {hw} từ, dấu hiệu {hm or 'không có'}"))

    # ─── CHỐT ─────────────────────────────────────────────────────────────
    closer = sents[-1] if sents else ""
    cw = len(closer.split())
    out.append(Finding(cw <= MAX_CLOSER_WORDS, "CHỐT", f"chốt {cw} từ"
                       if cw <= MAX_CLOSER_WORDS else f"chốt dài {cw} từ"))
    out.append(Finding(closer.endswith("?") or any(
        k in closer.lower() for k in ("comment", "bình luận", "video sau", "tập sau")),
        "CHỐT", "chốt mời tương tác" if closer.endswith("?") else
        "chốt không mời comment/xem tiếp"))

    # ─── ĐỘ MỚI: so với lịch sử cùng pillar ───────────────────────────────
    same = [h for h in history if h["pillar"] == d.pillar]
    dup_key = [h["key"] for h in same if h["key"] == d.key]
    out.append(Finding(not dup_key, "ĐỘ MỚI", f"chủ đề đã làm: {dup_key}" if dup_key
                       else f"chủ đề mới (lịch sử pillar: {len(same)} bài)"))
    op = " ".join(d.script.split()[:OPENING_WORDS]).lower()
    dup_op = [h["key"] for h in history
              if " ".join(h["script"].split()[:OPENING_WORDS]).lower() == op]
    out.append(Finding(not dup_op, "ĐỘ MỚI", f"mở bài trùng: {dup_op}" if dup_op
                       else "mở bài chưa dùng"))
    recent = [h["angle"] for h in same[-3:]]
    out.append(Finding(d.angle not in recent, "ĐỘ MỚI",
                       f"góc '{d.angle}' vừa dùng trong 3 bài gần nhất" if d.angle in recent
                       else f"góc '{d.angle}' khác 3 bài gần nhất"))

    # ─── ĐỘ DÀI ───────────────────────────────────────────────────────────
    out.append(Finding(MIN_WORDS <= words <= MAX_WORDS, "ĐỘ DÀI",
                       f"{words} từ (khung {MIN_WORDS}–{MAX_WORDS})"))
    return out


def verdict(findings: list[Finding]) -> bool:
    return all(f.ok for f in findings)
