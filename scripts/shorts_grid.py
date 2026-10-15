"""Lưới Short theo ngày: mỗi kênh đã có mấy Short/ngày, còn trống slot nào (giờ VN).

    python scripts/shorts_grid.py                      # MIM + CK, từ mai tới hết lịch hiện có
    python scripts/shorts_grid.py 2026-10-13 2026-10-20 --channel CK
    python scripts/shorts_grid.py ... --free           # chỉ in "ngày giờ" còn trống, mỗi dòng một slot

Chỉ đọc store (state.sqlite) + data/shorts_slots.json. Short đã có được xếp vào slot GẦN NHẤT còn trống.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.console import utf8_console  # noqa: E402

VN = timedelta(hours=7)
CFG = json.loads((ROOT / "data" / "shorts_slots.json").read_text(encoding="utf-8"))


def mins(hhmm: str) -> int:
    return int(hhmm[:2]) * 60 + int(hhmm[3:])


def grid(ch: str, d0: date, d1: date) -> dict[date, dict[str, str | None]]:
    """{ngày: {slot: slug | None}}; Short thừa ngoài 5 slot nằm ở khoá '+HH:MM'."""
    slots = CFG[ch]
    out = {d0 + timedelta(days=i): {s: None for s in slots} for i in range((d1 - d0).days + 1)}
    with store.connect() as conn:
        rows = conn.execute("select slug, publish_at from item where channel=? and kind='short' order by publish_at",
                            (ch,)).fetchall()
    for slug, at in rows:
        t = datetime.strptime(at, "%Y-%m-%dT%H:%M:%SZ") + VN
        day = out.get(t.date())
        if day is None:
            continue
        free = [s for s in slots if day[s] is None]
        if free:
            day[min(free, key=lambda s: abs(mins(s) - t.hour * 60 - t.minute))] = slug
        else:
            day[f"+{t:%H:%M}"] = slug
    return out


def main() -> None:
    utf8_console()
    pos = [a for a in sys.argv[1:] if a[:1].isdigit()]
    chs = [sys.argv[sys.argv.index("--channel") + 1]] if "--channel" in sys.argv else ["MIM", "CK"]
    d0 = date.fromisoformat(pos[0]) if pos else date.today() + timedelta(days=1)
    for ch in chs:
        if len(pos) > 1:
            d1 = date.fromisoformat(pos[1])
        else:
            with store.connect() as conn:
                last = conn.execute("select max(publish_at) from item where channel=? and kind='short'", (ch,)).fetchone()[0]
            d1 = max(d0, (datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ") + VN).date())
        g = grid(ch, d0, d1)
        if "--free" in sys.argv:
            for d, day in g.items():
                for s, slug in day.items():
                    if slug is None:
                        print(f"{ch} {d} {s}")
            continue
        have = sum(1 for day in g.values() for v in day.values() if v)
        need = sum(1 for day in g.values() for v in day.values() if v is None)
        print(f"\n{ch}: {d0} -> {d1} · đã có {have} · thiếu {need} (mục tiêu {CFG['target']}/ngày, slot {' '.join(CFG[ch])})")
        for d, day in g.items():
            n = sum(1 for v in day.values() if v)
            cells = "  ".join(f"{s} {'■ ' + v if v else '·'}" for s, v in day.items())
            print(f"  {d:%a %d/%m} {n}/{CFG['target']}  {cells}")


if __name__ == "__main__":
    main()
