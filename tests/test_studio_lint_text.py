"""Luật strict cho chữ hiển thị: không đọc lại lời, không mất dấu tiếng Việt."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion" / "long"))
import studio_lint as S  # noqa: E402


def test_spoken_prefix_is_an_error_after_four_words():
    issues = S.spoken_prefix_issues(
        "ch00", ["Bốn từ đầu xuất hiện trong câu đang đọc."],
        [{"type": "kinetic", "at": [0, "Bốn"], "text": "Bốn từ đầu xuất hiện trên hình"}],
    )
    assert len(issues) == 1


def test_spoken_prefix_allows_translation_label_and_different_text():
    translated = S.spoken_prefix_issues(
        "ch00", ["[TRÍCH DỊCH] Bốn từ đầu xuất hiện trong câu đọc."],
        [{"type": "kinetic", "at": [0, "Bốn"], "text": "Bốn từ đầu xuất hiện trên hình"}],
    )
    different = S.spoken_prefix_issues(
        "ch00", ["Bốn từ đầu xuất hiện trong câu đang đọc."],
        [{"type": "kinetic", "at": [0, "Bốn"], "text": "Một hình minh họa khác hẳn"}],
    )
    assert translated == []
    assert different == []


def test_unaccented_vietnamese_label_is_an_error_but_english_names_are_not():
    issues = S.unaccented_vietnamese_issues(
        "ch00", [{"type": "kinetic", "text": "CONG TY NAM 2026"}, {"type": "kinetic", "text": "APPLE CEO"}],
    )
    assert len(issues) == 1
    assert "CONG TY, NAM" in issues[0]
