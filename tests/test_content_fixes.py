"""Khoá các lỗi nội dung tìm thấy trong audit 08/10/2026 (mỗi test = một lỗi thật)."""
from datetime import date, timedelta

import pytest

from factory import integrity
from factory.batchcheck import report_batch
from factory.bundle import Bundle
from factory.lines import bud, novelty, packs
from factory.speak import strip_unspeakable


def test_thousands_separator_is_not_a_sentence_break():
    """'1.000 ... 3.000 thành viên' từng bị chặn cứng là câu lặp ('000 thành viên.')."""
    s = "Băng này có hơn 1.000 thành viên. Mười năm sau, con số lên tới 3.000 thành viên."
    assert integrity.blocking(s) == []
    assert integrity.blocking("Câu lặp. Câu lặp.")              # lặp thật vẫn bị chặn


def test_same_closing_question_is_detected():
    """Kịch bản kết bằng '?' từng bị lấy nhầm câu áp chót -> 'câu chốt đa dạng'."""
    def b(i):
        return Bundle(channel="BUD", kind="short", slug=f"bud-test-{i}",
                      script=f"Mở bài số {i} rất khác. Thân bài {i} cũng khác. Bạn nghĩ sao về điều này?",
                      title=f"Tiêu đề {i}", description="x", tags=["x"], thumbnail_text="",
                      publish_at="2026-12-01T00:00:00Z", voice="v", bgm="", broll_queries=["x"])
    ok, text = report_batch([b(i) for i in range(6)], label="t")
    assert "câu chốt" in text and "6/6" in text


def test_han_characters_are_shown_not_spoken():
    assert strip_unspeakable("Trực là Trực bế — 閉, nghĩa là bịt lại.") == "Trực là Trực bế, nghĩa là bịt lại."


def test_leap_month_is_named_as_leap_month():
    """2028 nhuận tháng 5: bản cũ ra hai 'rằm tháng 5' cách nhau một tháng."""
    from factory.lunar import facts_for
    names = []
    d = date(2028, 6, 1)
    while d < date(2028, 8, 10):
        e = bud._event(facts_for(d))
        if e and ("rằm" in e[0] or "mùng 1" in e[0]):
            names.append(e[0])
        d += timedelta(days=1)
    assert names.count("rằm tháng 5 âm lịch") == 1
    assert "rằm tháng 5 nhuận âm lịch" in names


def test_countdown_titles_never_repeat_across_years():
    """'Còn 13 ngày tới vía Phật Dược Sư' lặp lại sau một năm âm -> chống trùng chặn video năm sau."""
    seen = set()
    d = date(2026, 10, 26)
    while d < date(2028, 1, 1):
        x = bud.lich_ngay([], d)
        if x:
            assert x.title not in seen, x.title
            seen.add(x.title)
        d += timedelta(days=1)


@pytest.mark.real_titles
def test_missing_channel_titles_stop_instead_of_disabling_dedupe(monkeypatch, tmp_path):
    novelty._load.cache_clear()
    monkeypatch.setattr(novelty, "TITLES_DIR", tmp_path)
    monkeypatch.delenv("YF_ALLOW_STALE_TITLES", raising=False)
    with pytest.raises(novelty.TitlesUnavailable):
        novelty.duplicate_on_channel("BUD", "Một tiêu đề bất kỳ")
    novelty._load.cache_clear()


def test_old_and_new_tone_placement_are_the_same_word():
    assert novelty.similar("Hoà thượng Thích Quảng Đức là ai?", "Hòa thượng Quảng Đức tự thiêu vì sao?")


@pytest.mark.parametrize("text", [
    "Theo điều 999 Bộ luật Hình sự.",                                   # viết thường
    "Theo Ðiều 999 Bộ luật Hình sự.",                               # chữ Ð giả
    "Điều 353 quy định tội tham ô tài sản. Mức cao nhất vẫn là tử hình.",  # khung phạt ở câu sau
])
def test_citation_checker_catches_more_forms(text):
    assert packs.check_citations(text)


def test_spoken_verse_number_must_match_source():
    assert packs.check_citations("Pháp Cú kệ 500 dạy rằng hận thù không dập được hận thù.", cite_ke=[5])
    assert not packs.check_citations("Pháp Cú kệ 5 dạy rằng hận thù không dập được hận thù.", cite_ke=[5])
