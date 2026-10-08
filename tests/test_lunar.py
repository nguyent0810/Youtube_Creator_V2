"""Khoá sự thật lịch bằng HAI nguồn độc lập.

LỖI THẬT (08/10/2026): 92 video Lịch nói sai Trực vì vnlunar <= 1.0.4 tính
sai, và mọi test cũ đều so với chính vnlunar -- nên chúng xanh trong khi
dữ kiện sai. Test ở đây so với giá trị TRA TAY theo quy tắc truyền thống
(và đã đối chiếu với vnlunar 1.0.5), cùng các tính chất mà bất kỳ lịch
đúng nào cũng phải thoả.
"""
from datetime import date, timedelta

import pytest

from factory import lunar
from factory.compose import script_for
from factory.factcheck import check, report
from factory.lunar import LunarMismatch, facts_for

# (ngày, can chi, trực, sao) -- đã kiểm bằng tay theo quy tắc:
#   Trực = (chi ngày - chi tháng tiết khí) mod 12; 12 thần khởi Thanh Long theo tháng âm.
GOLDEN = [
    (date(2026, 10, 1), "Mậu Thân", "Trực bế", "Bạch Hổ"),       # video cũ: Kim Quỹ, Trực nguy
    (date(2026, 10, 4), "Tân Hợi", "Trực mãn", "Huyền Vũ"),      # video cũ: Ngọc Đường (hoàng đạo)
    (date(2026, 10, 5), "Nhâm Tý", "Trực bình", "Tư Mệnh"),      # video cũ: Thiên Lao (hắc đạo)
    (date(2026, 10, 7), "Giáp Dần", "Trực chấp", "Thanh Long"),
    (date(2026, 10, 8), "Ất Mão", "Trực chấp", "Minh Đường"),    # Hàn Lộ: Trực lặp lại
    (date(2026, 10, 11), "Mậu Ngọ", "Trực thành", "Thiên Hình"),
    (date(2026, 10, 23), "Canh Ngọ", "Trực thành", None),
]


@pytest.mark.parametrize("day,cc,truc,god", GOLDEN)
def test_golden_days(day, cc, truc, god):
    f = facts_for(day)
    assert (f.can_chi_day, f.truc_name) == (cc, truc)
    if god:
        assert f.god_name == god


def test_truc_thanh_october_2026_is_the_11th_and_23rd():
    days = [date(2026, 10, d) for d in range(1, 32) if facts_for(date(2026, 10, d)).truc_name == "Trực thành"]
    assert days == [date(2026, 10, 11), date(2026, 10, 23)]


def test_truc_kien_falls_on_the_month_branch_day():
    """Định nghĩa của Trực kiến: chi ngày trùng chi tháng (theo tiết khí)."""
    d = date(2026, 1, 1)
    while d < date(2028, 1, 1):
        _, chi = lunar.day_can_chi(d)
        m, sure = lunar.solar_month_chi(d)
        if sure:
            assert (lunar.truc_index(d)[0] == 0) == (chi == m), d
        d += timedelta(days=1)


def test_truc_repeats_exactly_on_solar_term_days():
    """Trực đi tuần tự từng ngày, chỉ LẶP LẠI đúng ngày giao tiết (12 lần/năm)."""
    repeats = []
    d = date(2026, 1, 2)
    while d < date(2027, 1, 1):
        a, b = facts_for(d - timedelta(days=1)).truc_name, facts_for(d).truc_name
        ia, ib = lunar.TRUC_ORDER.index(a), lunar.TRUC_ORDER.index(b)
        assert ib in (ia, (ia + 1) % 12), d
        if ia == ib:
            repeats.append(d)
            assert lunar.solar_month_chi(d)[0] != lunar.solar_month_chi(d - timedelta(days=1))[0]
        d += timedelta(days=1)
    assert len(repeats) == 12
    assert date(2026, 10, 8) in repeats          # Hàn Lộ 2026


def test_mismatch_with_library_stops_everything(monkeypatch):
    """Thư viện nói khác phép tính độc lập -> DỪNG, không âm thầm chọn một bên."""
    import vnlunar
    real = vnlunar.get_full_info

    def wrong(d, m, y):
        info = real(d, m, y)
        info["12_constructions"] = dict(info["12_constructions"], name="Trực Nguy")
        return info

    monkeypatch.setattr(vnlunar, "get_full_info", wrong)
    with pytest.raises(LunarMismatch, match="trực"):
        facts_for(date(2026, 10, 1))


def test_activity_list_is_pinned_not_taken_from_library(monkeypatch):
    """Danh mục việc là quyết định NỘI DUNG -- thư viện đổi danh mục thì kịch bản không đổi theo."""
    import vnlunar
    real = vnlunar.get_full_info

    def other_list(d, m, y):
        info = real(d, m, y)
        info["12_constructions"] = dict(info["12_constructions"], good_for=["Gặp gỡ đối tác"])
        return info

    before = facts_for(date(2026, 10, 1)).truc_good_for
    monkeypatch.setattr(vnlunar, "get_full_info", other_list)
    assert facts_for(date(2026, 10, 1)).truc_good_for == before == ("Trúc đê phòng", "đắp lỗ", "sửa tường")


def test_every_generated_script_passes_factcheck():
    d = date(2026, 10, 1)
    while d < date(2027, 1, 1):
        f = facts_for(d)
        ok, text = report(script_for(f)["script"], f, f.publish_at)
        assert ok, text
        d += timedelta(days=1)


def _fails(script, f):
    return [x.msg for x in check(script, f, f.publish_at) if not x.ok]


@pytest.mark.parametrize("old,new", [
    ("giờ Tý (23-1h)", "giờ Sửu (1-3h)"),                 # giờ không phải giờ tốt đầu tiên
    ("Trực bế — 閉, nghĩa là bịt lại", "Trực bế — 閉, nghĩa là gom về"),   # chú giải của trực khác
    ("Bạch Hổ", "Kim Quỹ"),                               # sao của ngày khác
    ("trúc đê phòng, đắp lỗ, sửa tường", "trúc đê phòng, đắp lỗ, an táng"),  # việc bịa thêm
])
def test_factcheck_catches_tampered_facts(old, new):
    """Mấy kiểu sửa này trước đây đều ĐẠT -- bộ kiểm không soi giờ, chú giải, việc ngoài danh sách tay."""
    f = facts_for(date(2026, 10, 1))
    script = script_for(f)["script"]
    assert old in script
    assert _fails(script.replace(old, new), f)


def test_factcheck_catches_wrong_mansion_claim():
    f = facts_for(date(2026, 10, 1))            # tú Khuê, con Sói, nhóm xấu
    script = script_for(f)["script"] + " Nhị thập bát tú là tú Khuê, con Sói, lịch xếp vào nhóm tốt."
    assert _fails(script, f)


def test_mai_tang_is_not_tomorrow():
    """'mai táng' không phải 'ngày mai'."""
    f = facts_for(date(2026, 10, 1))
    script = script_for(f)["script"].replace("Ngày mai", "Hôm ấy").replace("ngày mai", "hôm ấy") + " Kiêng mai táng."
    assert any("ngày mai" in m for m in _fails(script, f))
