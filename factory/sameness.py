"""Độ lặp khuôn theo DÒNG nội dung -- đo, không chặn.

VÌ SAO (bước 5, docs/audit/2026-10-05-variety-design.md): chính sách YouTube về
nội dung "sản xuất hàng loạt / lặp lại" nhắm vào video theo khuôn, ít khác
nhau. Đo 05/10/2026 trên 347 bundle: Lịch (FS, sinh bằng code) trung vị 50% câu
trùng một bài gần đây, menh-tue 83%, cl-dieu 43%; các dòng còn lại gần 0.

Cố ý KHÔNG làm cổng chặn ở store: chặn trong enqueue làm kẹt sync_from_disk và
bỏ rơi video đã dựng (Grok, 2 vòng). Thay vào đó số đo vào brief tuần -- pha
sinh (chat) đọc trước khi viết lô mới, và người sửa bộ sinh (compose.py...).

Số chính của mỗi dòng: với MỖI video, tỉ lệ câu của nó trùng KHUÔN với MỘT
video khác cùng dòng (lấy hàng xóm trùng nhiều nhất), rồi lấy trung vị. Trung
vị của mọi cặp sẽ giấu đúng hàng xóm đáng sợ.
"""
from __future__ import annotations

import re
import statistics
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

from factory import channels

WINDOW_DAYS = 28
_SENT = re.compile(r"(?<=[.!?…])\s+")


def shape(sentence: str) -> str:
    """Khuôn câu: bỏ số, phần trong ngoặc, và chữ viết hoa giữa câu (tên sao,
    tên giờ, con giáp...) -- "giờ Tý (23-1h)" và "giờ Dần (3-5h)" là MỘT khuôn."""
    s = unicodedata.normalize("NFC", sentence.strip())
    s = re.sub(r"\([^)]*\)", "()", s)
    s = re.sub(r"\d+", "#", s)
    words = s.split()
    words = words[:1] + ["X" if w[:1].isupper() else w for w in words[1:]]
    s = " ".join(words).lower()
    s = re.sub(r"[^\w#()\s]", " ", s)
    return re.sub(r"(\bx\b\s*)+", "x ", re.sub(r"\s+", " ", s)).strip()


def shapes(script: str) -> set[str]:
    return {shape(x) for x in _SENT.split(script.strip()) if x.strip()}


def line_of(channel: str, slug: str) -> str | None:
    return next((p for p in channels.prefixes(channel) if slug.startswith(p)), None)


@dataclass
class LineStat:
    channel: str
    line: str
    n: int
    median_share: float
    top: list[tuple[str, int]] = field(default_factory=list)   # (khuôn câu, số bài)
    bgm_share: float | None = None    # tỉ lệ bài dùng nhạc nền phổ biến nhất (None: không dựng bằng assemble)
    broll_share: float | None = None  # tỉ lệ bài dùng BỘ từ khoá hình phổ biến nhất (không kể thứ tự)


def _when(b) -> datetime:
    return datetime.strptime(b.publish_at, "%Y-%m-%dT%H:%M:%SZ")


def line_stats(bundles, *, channel: str) -> list[LineStat]:
    """Một LineStat cho mỗi dòng, trên 28 ngày cuối (theo publish_at) của dòng đó."""
    by: dict[str, list] = {}
    for b in bundles:
        ln = line_of(channel, b.slug) if b.channel == channel else None
        if ln:
            by.setdefault(ln, []).append(b)
    out = []
    for ln, bs in by.items():
        end = max(_when(b) for b in bs)
        bs = [b for b in bs if _when(b) > end - timedelta(days=WINDOW_DAYS)]
        sh = [shapes(b.script) for b in bs]
        shares = []
        for i, s in enumerate(sh):
            others = [len(s & t) / len(s) for j, t in enumerate(sh) if j != i and s]
            shares.append(max(others, default=0.0))
        top = Counter(x for s in sh for x in s).most_common(3)
        # Nhạc nền / bộ hình chỉ có nghĩa với short dựng bằng assemble; hồ sơ
        # S-tier và video dài dựng theo spec riêng (không bgm, không broll_queries).
        from factory.store import _engine
        asm = [b for b in bs if _engine(b) == "assemble"]
        bgm = Counter(b.bgm for b in asm).most_common(1)[0][1] / len(asm) if asm else None
        broll = (Counter(frozenset(b.broll_queries) for b in asm).most_common(1)[0][1] / len(asm)
                 if asm else None)
        out.append(LineStat(channel, ln, len(bs), round(statistics.median(shares), 2),
                            [t for t in top if t[1] > 1],
                            None if bgm is None else round(bgm, 2), None if broll is None else round(broll, 2)))
    return sorted(out, key=lambda s: -s.median_share)


def render(stats: list[LineStat]) -> str:
    lines = ["", "## Độ lặp khuôn (28 ngày cuối mỗi dòng)", "",
             "Trung vị, qua các video, của tỉ lệ câu trùng KHUÔN với một video khác cùng dòng. "
             "Cao = người xem hằng ngày nhận ra công thức (rủi ro chính sách 'nội dung lặp lại').", "",
             "| Dòng | Video | Câu trùng khuôn | Nhạc nền phổ biến nhất | Bộ hình phổ biến nhất |",
             "|---|---|---|---|---|"]
    if not stats:
        return "\n## Độ lặp khuôn\n\nchưa có bundle nào của kênh này.\n"
    pct = lambda x: "—" if x is None else f"{x:.0%}"  # noqa: E731
    for s in stats:
        lines.append(f"| `{s.line}` | {s.n} | {s.median_share:.0%} | {pct(s.bgm_share)} | {pct(s.broll_share)} |")
    for s in stats:
        if s.median_share >= 0.3 and s.top:
            lines.append(f"\nKhuôn lặp nhiều nhất ở `{s.line}`: "
                         + "; ".join(f"“{t}” ({c} bài)" for t, c in s.top))
    return "\n".join(lines) + "\n"


def render_for(channel: str, base: Path | None = None) -> str:
    """Khối cho brief tuần. Không bao giờ ném: một file bundle hỏng không được
    làm mất cả brief (phần YouTube/nhu cầu vẫn phải ra)."""
    from factory import store
    try:
        return render(line_stats(list(store.iter_bundles(channel, base)), channel=channel))
    except Exception as exc:
        return f"\n## Độ lặp khuôn\n\nlỗi khi đọc bundle: {type(exc).__name__}: {exc}\n"
