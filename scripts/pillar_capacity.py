"""Mô phỏng: 4 pillar chạy được bao nhiêu ngày liên tục trước khi cạn?

    python scripts/pillar_capacity.py 2026-09-30 400

Chạy đúng hàm chọn chủ đề + bộ kiểm như khi sản xuất thật, ngày nối ngày,
lịch sử tăng dần (kể cả lịch sử thật trên đĩa). KHÔNG ghi gì. Báo:
  - số ngày có chủ đề CỐ ĐỊNH (chưa phải dùng loại hằng ngày)
  - ngày đầu tiên pillar bị chặn hẳn (nếu có)
  - bài nào trượt bộ kiểm trong lúc mô phỏng (phải là 0)
"""
import collections
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from factory import store  # noqa: E402
from factory.pillars import check as C  # noqa: E402
from factory.pillars import topics as P  # noqa: E402

start = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date(2026, 9, 30)
days = int(sys.argv[2]) if len(sys.argv) > 2 else 365

history = P.load_history(store.BUNDLE_DIR)
stat = {p: {"co_dinh": 0, "hang_ngay": 0, "chan": None, "truot": [], "goc": collections.Counter()}
        for p in P.PILLARS}
for n in range(days):
    day = start + timedelta(days=n)
    for p, (_, hhmm, _) in P.PILLARS.items():
        st = stat[p]
        if st["chan"]:
            continue
        d, why = P.next_draft(p, history, day)
        if d is None:
            st["chan"] = day
            continue
        f = C.check(d, P.ALL_NAMES, history)
        if not C.verdict(f):
            st["truot"].append((day, d.key, [x.msg for x in f if not x.ok]))
        daily = d.angle.startswith("hằng ngày")
        st["hang_ngay" if daily else "co_dinh"] += 1
        st["goc"][d.angle] += 1
        h, m = map(int, hhmm.split(":"))
        history.append({"pillar": p, "key": d.key, "angle": d.angle, "script": d.script,
                        "publish_at": (datetime(day.year, day.month, day.day, h, m)
                                       - timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")})

print(f"Mô phỏng {days} ngày từ {start}:\n")
for p, st in stat.items():
    total = st["co_dinh"] + st["hang_ngay"]
    print(f"{p:5s} {P.PILLARS[p][2]:18s} cố định {st['co_dinh']:3d} ngày · hằng ngày {st['hang_ngay']:3d} · "
          f"{'CHẶN từ ' + str(st['chan']) if st['chan'] else 'chạy đủ ' + str(total) + ' ngày'} · "
          f"trượt kiểm {len(st['truot'])}")
    print("      góc:", ", ".join(f"{g} {c}" for g, c in st["goc"].most_common()))
    for t in st["truot"][:3]:
        print("      TRƯỢT", t)
