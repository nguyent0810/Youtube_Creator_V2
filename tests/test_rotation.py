"""Thí nghiệm xoay giờ: lần ghi tự động duy nhất của vòng phản hồi.

Không xoay thì dòng và giờ mãi là một biến -- không bao giờ biết dòng kém hay giờ kém.
"""
from datetime import date, datetime, timedelta

from factory.lines import bud, cl
from factory.pillars import topics
from factory.rotation import plan_day

D0 = date(2026, 10, 12)


def test_rotation_off_keeps_todays_fixed_map():
    assert plan_day("CL", cl.PILLARS, [], D0) == [(p, hhmm) for p, (_, hhmm, _) in cl.PILLARS.items()]


def test_each_rotating_line_visits_each_slot_once_per_cycle_and_each_slot_keeps_one_line():
    base = sorted(hhmm for _, hhmm, _ in topics.PILLARS.values())
    seen = {p: set() for p in topics.PILLARS}
    for k in range(len(base)):
        day = plan_day("FS", topics.PILLARS, [], D0 + timedelta(days=k))
        assert sorted(hhmm for _, hhmm in day) == base          # mỗi giờ đúng một dòng
        for p, hhmm in day:
            seen[p].add(hhmm)
    assert all(s == set(base) for s in seen.values())          # mỗi dòng qua đủ mọi giờ


def test_the_lich_line_stays_pinned_while_the_others_rotate():
    for k in range(5):
        day = dict(plan_day("BUD", bud.PILLARS, [], D0 + timedelta(days=k)))
        assert day["lich"] == "06:30"
        assert "06:30" not in [h for p, h in day.items() if p != "lich"]


def test_a_line_that_already_has_its_video_that_day_is_skipped_even_if_its_slot_changed():
    # Bundle cũ: giap đăng 11:30 giờ VN ngày D0 (04:30 UTC). Lịch xoay hôm nay đặt giap giờ khác.
    history = [{"pillar": "giap", "key": "x", "angle": "", "script": "", "publish_at": "2026-10-12T04:30:00Z"}]
    day = dict(plan_day("FS", topics.PILLARS, history, D0))
    assert "giap" not in day
    assert len(day) == len(topics.PILLARS) - 1


def test_on_a_part_filled_day_the_remaining_lines_never_take_a_clock_time_already_used():
    # Review: một ngày đã có bài theo giờ cố định cũ (giap 11:30); công thức xoay có thể
    # đặt dòng khác vào đúng 11:30 -> hai video cùng một phút.
    taken = "2026-10-12T04:30:00Z"                      # 11:30 VN ngày D0
    history = [{"pillar": "giap", "key": "x", "angle": "", "script": "", "publish_at": taken}]
    for k in range(4):
        day = D0 + timedelta(days=k)
        h = [dict(history[0], publish_at=(datetime(day.year, day.month, day.day, 4, 30)).strftime("%Y-%m-%dT%H:%M:%SZ"))]
        slots = [hhmm for _, hhmm in plan_day("FS", topics.PILLARS, h, day)]
        assert "11:30" not in slots and len(set(slots)) == len(slots) == 3


def test_lines_still_to_do_keep_their_cycled_slot_when_it_is_free():
    full = dict(plan_day("FS", topics.PILLARS, [], D0 + timedelta(days=1)))
    p0 = next(iter(topics.PILLARS))
    hh, mm = map(int, full[p0].split(":"))
    done_at = (datetime(2026, 10, 13, hh, mm) - timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    part = dict(plan_day("FS", topics.PILLARS, [{"pillar": p0, "publish_at": done_at}], D0 + timedelta(days=1)))
    assert part == {p: s for p, s in full.items() if p != p0}
