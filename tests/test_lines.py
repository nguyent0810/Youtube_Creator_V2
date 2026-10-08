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


# ─── Toàn vẹn văn bản (chuyển thể S8 từ branch feat) ───────────────────────

def test_integrity_blocks_repeat_and_markup_not_truncation():
    from factory import integrity
    assert integrity.blocking("Câu một. Câu hai. câu MỘT!")                       # lặp sau chuẩn hoá
    assert integrity.blocking("Mở bài. Phương án B: kết.")                         # nhãn ứng viên lọt vào
    assert integrity.blocking("Xem thêm tại https://example.com nhé.")             # URL
    assert not integrity.blocking("Đây là **điểm nhấn** hợp lệ. Hết.")             # ** được bóc như TTS
    tr = integrity.check("Một câu. Câu cuối bị cụt")
    assert tr and not tr[0].blocking and tr[0].code == "INT_TRUNCATED"


def test_every_existing_script_passes_integrity():
    """Không chặn nhầm kịch bản đang có của cả 3 kênh."""
    import json
    from pathlib import Path
    from factory import integrity
    bad = []
    for f in Path("bundles").glob("*/*.json"):
        s = json.loads(f.read_text(encoding="utf-8"))["script"]
        if integrity.blocking(s):
            bad.append((f.name, [x.code for x in integrity.blocking(s)]))
    assert not bad, bad[:5]


def test_signals_are_record_only():
    from factory.script_signals import signals
    s = signals("Án treo có phải là trắng án? Không. Án treo vẫn là một bản án tù.")
    assert s["hook_is_question"] and s["first_answer_sec"] is not None and "score" not in s


def test_novelty_catches_real_duplicates_not_false_ones():
    """Các cặp lấy từ kênh thật 30/09/2026."""
    from factory.lines.novelty import similar
    dup = [("Vì sao tượng Phật có dái tai dài?", "Vì sao tượng Phật có đôi tai dài?"),
           ("Vì sao Địa Tạng cầm tích trượng có vòng?", "Vì sao Bồ Tát Địa Tạng cầm tích trượng?"),
           ("Niết-bàn có phải là thiên đường?", "Niết bàn có phải là thiên đường sau khi chết?"),
           ("Tứ vô lượng tâm: từ, bi, hỷ, xả", "Tứ vô lượng tâm là gì?"),
           ("Năm giới: vì sao không có giới phải đi chùa?", "Năm giới của Phật tử là gì?")]
    ok = [("Pháp Cú kệ 50: đừng soi lỗi người", "Cha mẹ già kể mãi chuyện cũ, mình có đủ kiên nhẫn?"),
          ("Điều 125: Tội giết người trong trạng thái tinh thần bị kích động mạnh", "Điều 172: Tội công nhiên chiếm đoạt tài sản"),
          ("Chuyến xe buýt cuối lúc 11 giờ đêm", "Cuộc gọi lúc 3 giờ sáng từ số của mẹ"),
          ("14 tuổi phạm tội có bị xử lý hình sự?", "Nhặt được của rơi không trả có phạm tội?")]
    assert all(similar(a, b) for a, b in dup)
    assert not any(similar(a, b) for a, b in ok)


def test_penalty_sentence_wrapped_across_lines_is_read_in_full():
    """Lỗi thật (audit 08/10/2026): chỉ đọc dòng vật lý đầu của khoản, nên
    Điều 301 bị viết 'khoản 1: 3–7 năm, luật chia 3 khung' (thật: 01–04 năm, 4 khung)."""
    law = packs.blhs()
    ks = [k for k in cl._khoan(law["301"]["noi_dung"]) if not k.startswith("Pháp nhân")]
    assert cl._phat(ks[0]) == "phạt tù từ 1 năm đến 4 năm"
    hist = [{"pillar": "dieu", "key": k, "angle": "", "script": "", "publish_at": ""} for k in law if k != "301"]
    d = cl.dieu_luat(hist, None)
    assert d.key == "301"
    assert "khoản 1, mức nhẹ nhất là phạt tù từ 1 năm đến 4 năm" in d.script
    assert "Luật chia 4 khung" in d.script


def test_split_number_typo_in_source_is_rejoined():
    ks = cl._khoan(packs.blhs()["205"]["noi_dung"])
    assert cl._phat(ks[1]) == "phạt tiền từ 100 triệu đồng đến 500 triệu đồng hoặc phạt tù từ 1 năm đến 5 năm"


def test_article_317_is_its_own_article():
    """Tiêu đề 'Ðiều 317.' (chữ Ð U+00D0) từng làm Điều 317 dính vào Điều 316."""
    law = packs.blhs()
    assert law["317"]["ten"] == "Tội vi phạm quy định về an toàn thực phẩm"
    assert "an toàn thực phẩm" not in law["316"]["noi_dung"]
    assert not any("không có trong" in m for m in packs.check_citations("Theo Điều 317 Bộ luật Hình sự."))
