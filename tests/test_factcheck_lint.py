import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "motion" / "long"))
import factcheck_lint as F  # noqa: E402


def test_numbers_on_screen_and_in_script_must_have_evidence():
    issues = F.lint_content("Sự kiện năm 2020; chữ trên hình 2000.", "| CH00 | Sự kiện năm 2020 | #1 | https://example.test/a |", "")
    assert any("2000" in issue for issue in issues)


def test_translation_needs_original_and_url():
    evidence = "| CH00 | [TRÍCH DỊCH] câu nói năm 2020 | #1 | https://example.test/a |"
    assert any("nguyên văn tiếng gốc" in issue for issue in F.lint_content("[TRÍCH DỊCH] Câu nói năm 2020.", evidence, evidence))


def test_factcheck_translation_with_original_and_used_number_passes():
    factcheck = '| CH00 | [TRÍCH DỊCH]; Nguyên văn: "Stay hungry"; năm 2020 | #1 | https://example.test/a |'
    assert F.lint_content("[TRÍCH DỊCH] Câu nói năm 2020.", factcheck, factcheck) == []


def test_stale_factcheck_table_entry_is_reported():
    factcheck = "| CH08 | Khoản 150 triệu năm 1997 | #1 | https://example.test/a |"
    # Năm 1997 còn xuất hiện trong bản cuối nhưng khoản 150 triệu đã bị bỏ.
    assert any("lệch bản final" in issue and "CH08" in issue for issue in F.lint_content("Sự kiện năm 1997.", factcheck, factcheck))


def test_stale_check_recognizes_spoken_thousand_amount():
    factcheck = "| CH05 | Bán 50.000 máy năm 1993 | #1 | https://example.test/a |"
    assert F.stale_factcheck_issues("Bán 50 nghìn máy năm 1993.", factcheck) == []


def test_ck_f3_axis_labels_zero_and_spoken_amounts_are_not_duplicate_claims():
    article = "T1 T12 Q1 Q4, trục 0, CHƯƠNG 05, nhận 300 NGHÌN."
    evidence = "| CH00 | Nhận 300.000 | #1 | https://example.test/a |"
    assert F.lint_content(article, evidence, evidence) == []


def test_ck_f3_decimal_millions_and_labelled_examples():
    assert F.numbers("0,8 TRIỆU; 1,5 TRIỆU") == {"800000", "1500000"}
    example = {"type": "bars", "unit": "VÍ DỤ GIẢ ĐỊNH", "items": [{"lbl": "0,5"}]}
    assert F._display_strings(example) == []


def test_calendar_month_labels_do_not_hide_dates_or_decimal_amounts():
    assert F.lint_content("LỊCH TỪ THÁNG 1; LỊCH TỚI THÁNG 8", "có nguồn", "") == []

    dated_issues = F.lint_content("tháng 9 năm 1985", "có nguồn", "")
    assert any(issue.endswith(": 9") for issue in dated_issues)
    assert any(issue.endswith(": 1985") for issue in dated_issues)

    day_issues = F.lint_content("ngày 7 tháng 9", "có nguồn", "")
    assert any(issue.endswith(": 7") for issue in day_issues)
    assert any(issue.endswith(": 9") for issue in day_issues)

    amount_issues = F.lint_content("LỊCH TỚI THÁNG 8; 0,8 TRIỆU", "có nguồn", "")
    assert amount_issues == ["số/ngày không có trong factcheck.md hoặc research.md: 800000"]
