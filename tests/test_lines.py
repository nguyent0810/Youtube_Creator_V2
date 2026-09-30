"""Kênh CL + BUD: gói kịch bản, khuôn điều luật, lịch Phật giáo."""
import re
from datetime import date, timedelta

import pytest

from factory.lines import bud, cl, packs
from factory.pillars.check import Draft, verdict


def _hist(d):
    return {"pillar": d.pillar, "key": d.key, "script": d.script, "publish_at": "x", "angle": ""}


@pytest.mark.parametrize("mod", [cl, bud])
def test_every_pack_script_passes(mod):
    for line in mod.PILLARS:
        for e in packs.load(mod.CHANNEL, line):
            d = packs.to_draft(e, line, mod.BROLL[line])
            f = [x.msg for x in packs.check(d, [], fiction=line in mod.FICTION, cite_ke=e.get("cite_ke")) if not x.ok]
            assert not f, (mod.CHANNEL, line, e["key"], f)


def test_dieu_luat_heaviest_is_really_heaviest():
    """Lỗi thật: Điều 302 từng bị đọc 'nặng nhất 1–5 năm' (khoản chuẩn bị phạm tội)."""
    law, hist, n = packs.blhs(), [], 0
    while (d := cl.dieu_luat(hist, None)) is not None:
        a = law[d.key]
        assert not a["sua_2025"], d.key
        khoan = [k for k in cl._khoan(a["noi_dung"]) if cl._phat(k) and "chuẩn bị phạm tội" not in k[:80]
                 and not k.startswith("Pháp nhân")]
        best = max(cl._nang(cl._phat(k)) for k in khoan)
        said = re.search(r"khung nặng nhất, người phạm tội có thể bị (.+?)\.", d.script).group(1)
        assert cl._nang(said) == best, (d.key, said)
        hist.append(_hist(d))
        n += 1
    assert n >= 40


def test_citation_checker_catches_fake_and_amended():
    assert packs.check_citations("Theo Điều 999 Bộ luật Hình sự.")
    amended = next(so for so, a in packs.blhs().items() if a["sua_2025"])
    assert packs.check_citations(f"Điều {amended} quy định phạt tù từ 5 năm đến 10 năm.")
    assert not packs.check_citations("Theo Điều 65, án treo áp dụng khi phạt tù không quá ba năm.")
    assert packs.check_citations("x", cite_ke=[999])


def test_money_is_spoken_not_truncated():
    """Lỗi thật: '10.000.000 đồng' bị cắt thành 'phạt tiền từ 10.'"""
    s = cl._phat("Người nào ..., thì bị phạt tiền từ 10.000.000 đồng đến 50.000.000 đồng:")
    assert s == "phạt tiền từ 10 triệu đồng đến 50 triệu đồng"


def test_lich_countdown_is_real():
    """'Còn N ngày' phải đúng trên lịch âm thật, không ước lượng."""
    from factory.lunar import facts_for
    for k in range(20):
        day = date(2026, 9, 24) + timedelta(days=k)
        d = bud.lich_ngay([], day)
        m = re.match(r"Còn (\d+) ngày nữa là", d.script)
        if m:
            n = int(m.group(1))
            assert bud._event(facts_for(day + timedelta(days=n)))
            assert all(bud._event(facts_for(day + timedelta(days=j))) is None for j in range(1, n))
        assert verdict(bud.check_draft(d, []))


def test_fiction_label_and_rotation():
    d, _ = cl.next_draft("truyen", [])
    assert d is not None and d.angle == "hư cấu"
    d2, _ = cl.next_draft("truyen", [_hist(d)])
    assert d2.key != d.key
