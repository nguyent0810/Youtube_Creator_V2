"""Khoá luật: chỉ ĐẠT khi mọi claim ngoài nguồn đã được xác minh.

Mỗi test dựng lại một trong ba claim sai THẬT đã lọt qua trước khi có bộ
kiểm này, và khẳng định giờ nó bị bắt. Nếu ai đó nới lỏng bộ kiểm, những
test này đổ.
"""
from datetime import date

import pytest

from factory.claims import check_declared, check_statistics


def _fails(issues) -> list[str]:
    return [i.msg for i in issues if not i.ok]


# ─── Suy diễn thành fact ──────────────────────────────────────────────────

def test_undeclared_interpretation_is_rejected():
    """Câu định nghĩa nghĩa chữ mà chưa khai báo căn cứ -> CẦN SỬA.

    Đây là dạng nguy hiểm nhất: nghe như dữ kiện, nhưng nguồn lịch không hề
    có. Muốn dùng thì phải gõ ra căn cứ trong factory/claims.py."""
    bad = "Sao là Thanh Long. Chữ long nghĩa là rồng thiêng, mang điềm lành."
    assert _fails(check_declared(bad)), "câu diễn giải chưa khai báo phải bị bắt"


def test_declared_interpretation_passes():
    ok = "Trực là Trực bế, chữ bế nghĩa là bịt lại."
    assert not _fails(check_declared(ok))


@pytest.mark.parametrize("phrase", [
    "Bạch Hổ là sao bị kiêng nhiều nhất trong lịch.",
    "Người xưa thường tránh ngày này.",
    "Ngày này được cho là mang lại may mắn.",
    "Có lẽ vì vậy mà ai cũng chọn ngày này.",
])
def test_speculation_can_never_be_declared(phrase):
    """Suy đoán KHÔNG có đường khai báo -- không đếm được, không tra được.

    Khác diễn giải (tra từ điển ra) và thống kê (đếm lại được), nhóm này
    chỉ có một cách xử lý: không dùng."""
    assert _fails(check_declared(phrase)), f"phải loại: {phrase!r}"


# ─── Thống kê phải đếm lại toàn bộ dữ liệu ────────────────────────────────

def test_wrong_month_statistic_is_caught():
    """Thống kê sai phải bị đếm lại và báo con số THẬT.

    Trực thành tháng 10/2026 rơi vào 11/10 (Mậu Ngọ) và 23/10 (Canh Ngọ):
    tháng Tuất bắt đầu ở tiết Hàn Lộ 08/10, Trực thành của tháng Tuất là
    ngày Ngọ. Bản cũ của test này ghi "02, 18, 30/10, cách nhau 16 ngày" --
    đó là output của vnlunar <= 1.0.4, tính SAI, và test đã khoá luôn dữ
    kiện sai (chu kỳ Trực là 12 ngày, không bao giờ 16)."""
    bad = "Cả tháng Mười chỉ có năm ngày Trực thành."
    fails = _fails(check_statistics(bad, date(2026, 10, 2)))
    assert fails and "2 ngày" in fails[0] and "2026-10-11" in fails[0] and "2026-10-23" in fails[0]


def test_correct_month_statistic_passes():
    ok = "Cả tháng Mười chỉ có hai ngày Trực thành."
    assert not _fails(check_statistics(ok, date(2026, 10, 2)))


@pytest.mark.parametrize("phrase", [
    "Tháng này có tới chín ngày Trực trừ.",
    "Cả tháng mười một chỉ có năm ngày Trực trừ.",
    "Thuộc nhóm 8 sao hắc đạo.",
])
def test_other_phrasings_are_recounted_too(phrase):
    """Bản cũ chỉ nhận đúng MỘT lối nói; mấy câu này lọt qua không ai đếm."""
    target = date(2026, 11, 2) if "mười một" in phrase else date(2026, 10, 2)
    assert _fails(check_statistics(phrase, target)), phrase


def test_recurrence_claim_cannot_be_declared():
    """'Sáu ngày nữa mới lại có ngày như ngày mai' -- claim sai thật đã lọt."""
    assert _fails(check_declared("Sáu ngày nữa mới lại có ngày như ngày mai."))


def test_statistic_about_another_month_is_rejected():
    """Nói về tháng khác với ngày lịch đang dựng -> không xác minh được
    trong ngữ cảnh này, nên không được cho qua."""
    bad = "Cả tháng Chín chỉ có ba ngày Trực thành."
    assert _fails(check_statistics(bad, date(2026, 10, 2)))


def test_god_count_statistic_is_verified():
    assert not _fails(check_statistics("thuộc nhóm sáu sao hắc đạo", date(2026, 10, 3)))
    assert _fails(check_statistics("thuộc nhóm tám sao hắc đạo", date(2026, 10, 3)))


def test_statistics_are_recounted_not_trusted():
    """Bất biến cốt lõi: bộ kiểm ĐẾM LẠI từ vnlunar chứ không tin lời khai.

    Cùng một câu, đổi con số thì kết quả phải đổi theo -- chứng tỏ nó thật
    sự đếm, không chỉ kiểm cú pháp."""
    tmpl = "Cả tháng Mười chỉ có {} ngày Trực thành."
    assert not _fails(check_statistics(tmpl.format("hai"), date(2026, 10, 2)))
    for wrong in ("một", "ba", "bốn", "năm", "sáu"):
        assert _fails(check_statistics(tmpl.format(wrong), date(2026, 10, 2))), wrong
