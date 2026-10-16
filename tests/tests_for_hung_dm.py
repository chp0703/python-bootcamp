"""Week 2 peer-review tests for Member 6 (hung_dm), Week 1 work."""

import pytest

from members.hung_dm.w1 import grades, rules, text_tools, timetable, translate


def test_grade_summary_handles_even_and_single_lists():
    assert grades.summary([7.5, 9, 6, 8]) == {
        "min": 6,
        "max": 9,
        "mean": 7.62,
        "median": 7.75,
    }
    assert grades.summary([5])["median"] == 5


def test_grade_summary_rejects_empty_input():
    with pytest.raises(ValueError):
        grades.summary([])


def test_thesis_rules_cover_boundaries_and_both_missing_requirements():
    assert rules.can_register_thesis(120, 2.0)
    assert not rules.can_register_thesis(119, 2.0)
    assert not rules.can_register_thesis(120, 1.99)
    assert rules.missing(100, 1.5) == [
        "need 20 more credits",
        "need 0.5 higher GPA",
    ]


def test_word_count_and_top_k_order_ties_alphabetically():
    text = "Git is fun. Git is fast!"
    assert text_tools.word_count(text) == {"git": 2, "is": 2, "fun": 1, "fast": 1}
    assert text_tools.top_k(text, 2) == [("git", 2), ("is", 2)]


def test_timetable_sorts_courses_and_preserves_duplicates():
    entries = [("CSC10014", "Mon"), ("CSC10001", "Mon"), ("CSC10001", "Mon")]
    assert timetable.by_day(entries) == {"Mon": ["CSC10001", "CSC10001", "CSC10014"]}
    assert entries[0] == ("CSC10014", "Mon")


def test_merge_sorted_vectors_merges_duplicates_and_empty_inputs():
    assert translate.merge_sorted_vectors([1, 2, 2], [2, 3]) == [1, 2, 2, 2, 3]
    assert translate.merge_sorted_vectors([], [1, 3]) == [1, 3]
    assert translate.merge_sorted_vectors([], []) == []


def test_top_k_negative_count_returns_empty_edge_case():
    """Negative k should behave like zero; current review branch returns items."""
    assert text_tools.top_k("alpha beta", -1) == []
