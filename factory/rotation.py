"""Thí nghiệm xoay giờ đăng -- lần ghi tự động duy nhất của vòng phản hồi.

VÌ SAO: mỗi dòng nội dung luôn đăng CÙNG một giờ (PILLARS của từng kênh), nên
"dòng kém" và "giờ kém" là một biến -- không số liệu nào tách được. Xoay vòng
Latin: ngày d, dòng thứ i nhận giờ thứ (i + d) mod n trong các giờ không ghim.
Sau n ngày mỗi dòng đã qua mọi giờ, mỗi giờ mỗi ngày vẫn đúng một dòng. Số bài
mỗi dòng không đổi (1/ngày), nên không làm cạn pack hữu hạn -- chỉ hoán giờ.

Dòng ghim (Lịch) giữ giờ hẹn quen của khán giả. Bật/tắt theo kênh trong
factory/channels.py. Thiết kế: docs/audit/2026-10-05-feedback-loop-design.md.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta

from factory import channels

VN_UTC = timedelta(hours=7)


def _vn_day(publish_at: str) -> date:
    return (datetime.strptime(publish_at, "%Y-%m-%dT%H:%M:%SZ") + VN_UTC).date()


def _vn_hhmm(publish_at: str) -> str:
    return (datetime.strptime(publish_at, "%Y-%m-%dT%H:%M:%SZ") + VN_UTC).strftime("%H:%M")


def plan_day(code: str, pillars: dict, history: list[dict], day: date) -> list[tuple[str, str]]:
    """Các (dòng, "HH:MM" giờ VN) còn phải sinh cho `day`.

    Chống trùng theo (dòng, NGÀY VN), không theo (dòng, giờ): đổi giờ không
    được đẻ video thứ hai cho dòng đã có bài hôm đó, và bundle đã ghi không
    bao giờ bị dời giờ."""
    done = {(h["pillar"], _vn_day(h["publish_at"])) for h in history}
    cfg = channels.CHANNELS[code]
    pinned = set(cfg.get("pinned", ()))
    movers = [p for p in pillars if p not in pinned]
    slots = sorted(pillars[p][1] for p in movers)
    todo = [p for p in pillars if (p, day) not in done]
    if not cfg.get("rotate"):
        return [(p, pillars[p][1]) for p in todo]
    # Ngày làm dở (vd. đã có bài theo giờ cố định cũ): giờ đã có video trong
    # ngày là của nó -- dòng còn lại lấy giờ theo công thức nếu còn trống,
    # không thì lấy giờ trống còn lại. Không bao giờ hai video cùng một phút.
    taken = {_vn_hhmm(h["publish_at"]) for h in history if _vn_day(h["publish_at"]) == day}
    want = {p: slots[(movers.index(p) + day.toordinal()) % len(slots)] for p in todo if p in movers}
    got: dict[str, str] = {}
    for p, s in want.items():
        if s not in taken:
            got[p] = s
            taken.add(s)
    free = [s for s in slots if s not in taken]
    for p in want:
        if p not in got and free:
            got[p] = free.pop(0)
    return [(p, got.get(p, pillars[p][1]) if p in movers else pillars[p][1])
            for p in todo if p not in movers or p in got]
