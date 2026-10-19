"""Lịch đa dạng hơn mà vẫn đúng nguồn (bước 5, docs/audit/2026-10-05-variety-design.md).

Đo 05/10/2026: 92 bundle Lịch, trung vị 50% câu trùng nguyên văn với MỘT bài
gần đây; các câu thân bất biến ("Sao mở, trực siết.", "Ngoài danh mục ấy...",
"Giờ tốt đầu tiên...") lặp 20-34 lần. Ngày giả lập dưới đây theo đúng chu kỳ
thật: sao và trực cùng lặp mỗi 12 ngày.
"""
import sys
import types
from datetime import date, timedelta

import pytest

from factory import compose
from factory.lunar import AUSPICIOUS_GODS, DayFacts
from factory.vocab import SAO, TRUC

GODS, TRUCS = list(SAO), list(TRUC)
GOOD = {"Trực kiến": ("Động thổ", "Xuất hành", "Khai trương", "Nhập học"),
        "Trực trừ": ("Giải trừ", "Tắm gội", "Cạo đầu", "Quét dọn nhà cửa", "Cầu y trị bệnh"),
        "Trực mãn": ("Tế tự", "Cầu phúc", "Cầu tự", "Nạp tài", "Mở kho", "Khai trương", "Xuất hành"),
        "Trực bình": ("Sửa tường", "Bình trị đạo đồ"),
        "Trực định": ("Tế tự",), "Trực chấp": ("Bắt bớ",), "Trực phá": ("Cầu y trị bệnh",),
        "Trực nguy": ("An sàng", "Tế tự", "Cầu phúc"),
        "Trực thành": ("Nhập học", "Khai trương", "Xuất hành", "Nạp tài", "Tế tự", "Cầu phúc"),
        "Trực thu": ("Nạp tài", "Thu tất", "Tiến người"),
        "Trực khai": ("Tế tự", "Cầu phúc", "Cầu tự", "Lên sách lên chương biểu"),
        "Trực bế": ("Trúc đê phòng", "Đắp lỗ", "Sửa tường")}
HOURS = ["Tý (23-1h), Sửu (1-3h)", "Dần (3-5h), Mão (5-7h)", "Sửu (1-3h), Thìn (7-9h)"]


def day(i: int, start=date(2027, 1, 1)) -> DayFacts:
    g, t = GODS[i % 12], TRUCS[(i * 5) % 12]
    return DayFacts(
        target=start + timedelta(days=i), lunar_day=1 + i % 30, lunar_month=1, can_chi_day="Giáp Tý",
        day_type="", god_name=g, truc_name=t, truc_good_for=GOOD[t],
        truc_bad_for=("Mọi việc khác",) if i % 3 else ("Khai trương", "Xuất hành"),
        star_name="", star_desc="", mansion_name=["Giác", "Cang", "Đê", "Phòng", "Tâm"][i % 5],
        mansion_good=bool(i % 2), mansion_animal="Giao", mansion_element="Mộc", day_of_week="",
        nayin_name="", auspicious_hours=HOURS[i % 3], good_directions="",
        conflict_animal=["Ngựa", "Dê", "Khỉ", "Gà", "Chó", "Lợn"][i % 6], conflict_chi="Ngọ",
        day_animal=["Chuột", "Trâu", "Hổ", "Mèo", "Rồng", "Rắn"][i % 6],
        wealth_god_dir=["Nam", "Đông", "Tây Nam", "Bắc", "Đông Nam"][i % 5], joy_god_dir="Bắc")


DAYS = [day(i) for i in range(120)]


def compose_split(s):
    import re
    return [x for x in re.split(r"(?<=[.!?…])\s+", s.strip()) if x]


def test_the_same_sao_truc_pair_twelve_days_later_gets_another_closer():
    pairs = {}
    for f in DAYS:
        pairs.setdefault((f.god_name, f.truc_name), []).append(f)
    checked = 0
    for fs in pairs.values():
        for a, b in zip(fs, fs[1:]):
            sa, sb = compose.script_for(a)["script"], compose.script_for(b)["script"]
            assert compose_split(sa)[-1] != compose_split(sb)[-1], (a.target, b.target)
            checked += 1
    assert checked >= 50


def test_closers_are_spread_evenly_not_biased_to_the_first_two():
    # Bug cũ: v = (h + d) % 6 rồi chots[v % 4] -> chỉ số 0 và 1 trúng gấp đôi.
    from collections import Counter, defaultdict
    by_the = defaultdict(Counter)
    for f in DAYS:
        by_the[compose.the_cua_ngay(f)][compose_split(compose.script_for(f)["script"])[-1]] += 1
    for the, c in by_the.items():
        n = sum(c.values())
        if n >= 12:
            assert len(c) == 4 and max(c.values()) <= n / 4 * 1.75, (the, c)


def test_invariant_body_sentences_are_no_longer_one_fixed_line():
    from collections import Counter
    c = Counter(s for f in DAYS for s in set(compose_split(compose.script_for(f)["script"])))
    worst = c.most_common(1)[0]
    assert worst[1] <= len(DAYS) * 0.2, worst        # trước: câu kiêng chung ~37% số bài


def test_no_variant_reuses_one_truc_gloss_for_every_truc():
    # Grok vòng 3: "trực lại thu vào" là nghĩa của riêng Trực thu, mà thế
    # "sao mở / trực siết" gồm cả Trực nguy, định, chấp, phá, bình, bế.
    from factory.vocab import TRUC
    glosses = {t: TRUC[t].gloss.lower() for t in TRUC}
    for f in DAYS:
        body = " ".join(compose_split(compose.script_for(f)["script"])[1:-1]).lower()   # thân: nơi nói nghĩa trực
        s = body
        for t, g in glosses.items():
            if t != f.truc_name and len(g.split()) >= 2:
                assert g not in s, (f.target, f.truc_name, t, g)


def test_data_slots_still_come_from_the_day():
    for f in DAYS:
        s = compose.script_for(f)["script"]
        first_hour = f.auspicious_hours.split(",")[0].strip()
        if "giờ" in s.lower() and "tốt" in s.lower():
            assert first_hour in s, (f.target, s)
        # Câu kiêng xoay cách nói, nhưng chỉ nói "mọi việc khác" khi nguồn ghi đúng như vậy,
        # và danh mục kiêng cụ thể luôn là của chính ngày đó.
        # (_fit có thể bỏ câu kiêng ở ngày danh mục dài -- nên chỉ kiểm chiều "có nói thì phải đúng".)
        if "mọi việc khác" in s.lower():
            assert f.truc_bad_for == ("Mọi việc khác",), (f.target, s)
        elif "kiêng" in s.lower():
            assert compose._liet_ke(f.truc_bad_for, 3) in s, (f.target, s)


def test_the_same_day_always_gives_the_same_script():
    assert [compose.script_for(f) for f in DAYS[:30]] == [compose.script_for(f) for f in DAYS[:30]]


@pytest.fixture
def no_vnlunar(monkeypatch):
    # check_statistics chỉ cần vnlunar khi kịch bản nêu thống kê theo tháng; Lịch không nêu.
    monkeypatch.setitem(sys.modules, "vnlunar", types.SimpleNamespace())


def test_every_variant_still_passes_the_source_check(no_vnlunar):
    from factory.factcheck import check
    bad = {}
    for f in DAYS:
        s = compose.script_for(f)["script"]
        fails = [x.msg for x in check(s, f, f.publish_at) if not x.ok]
        if fails:
            bad[str(f.target)] = (fails, s)
    assert not bad, list(bad.items())[:3]


@pytest.mark.parametrize("n", [3])   # 2 file: đổi mỗi ngày thì ngày D và D+12 (chẵn) buộc trùng
def test_lich_bed_rotates_daily_and_never_locks_to_the_sao_truc_cycle(n):
    # Grok vòng 3: pool co lại khi thiếu file (12 % 4 == 0, 12 % 3 == 0...) thì
    # chỉ số ordinal % n khoá cặp (sao, trực) vào một nhạc.
    pool = list(compose.LICH_BGM[:n])
    beds = [compose.lich_bgm(f.target, pool) for f in DAYS]
    assert all(x != y for x, y in zip(beds, beds[1:]))                 # hai ngày liền nhau khác nhạc
    assert all(beds[i] != beds[i + 12] for i in range(len(beds) - 12))  # cùng cặp sao/trực -> khác nhạc
    assert set(beds) == set(pool)


def test_lich_never_borrows_another_fs_lines_bed():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    other = {"thinking_music.mp3", "deliberate_thought.mp3", "comfortable_mystery_4.mp3",
             "meditation_impromptu_02.mp3"}     # make_pillars_day.STYLE (giáp, trụ, dịch, mệnh)
    assert not other & set(compose.LICH_BGM)


def test_lich_bed_uses_only_files_that_exist():
    assert compose.lich_bgm(date(2027, 1, 1), ["only.mp3"]) == "only.mp3"
    with pytest.raises(ValueError):
        compose.lich_bgm(date(2027, 1, 1), [])


def test_every_phrasing_of_the_shared_kieng_line_is_actually_used():
    seen = {s for f in DAYS if f.truc_bad_for == ("Mọi việc khác",)
            for s in compose_split(compose.script_for(f)["script"]) if "mọi việc khác" in s.lower()}
    assert len(seen) == 4, seen
