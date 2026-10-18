"""Week 2 peer-review tests for dmh612's Week 1 work."""

import pytest

from members.dmh612.w1 import grades, rules, text_tools, timetable, translate


def test_grade_summary_even_and_single_inputs():
    assert grades.summary([7.5, 9, 6, 8]) == {
        "min": 6,
        "max": 9,
        "mean": 7.62,
        "median": 7.75,
    }
    assert grades.summary([5]) == {
        "min": 5,
        "max": 5,
        "mean": 5.0,
        "median": 5,
    }


def test_grade_summary_rejects_empty_input():
    with pytest.raises(ValueError):
        grades.summary([])


def test_thesis_eligibility_and_missing_requirements_boundaries():
    assert rules.can_register_thesis(120, 2.0)
    assert not rules.can_register_thesis(119, 2.0)
    assert not rules.can_register_thesis(120, 1.99)
    assert rules.missing(100, 1.5) == [
        "need 20 more credits",
        "need 0.5 higher GPA",
    ]
    assert rules.missing(120, 2.0) == []


def test_text_tools_count_punctuation_and_sort_top_k_ties():
    text = "Git is fun. Git is fast!"
    assert text_tools.word_count(text) == {
        "git": 2,
        "is": 2,
        "fun": 1,
        "fast": 1,
    }
    assert text_tools.top_k(text, 2) == [("git", 2), ("is", 2)]


def test_timetable_groups_days_sorts_courses_and_does_not_mutate_input():
    entries = [
        ("CSC10014", "Mon"),
        ("MTH00003", "Tue"),
        ("CSC10001", "Mon"),
    ]
    original = entries.copy()
    assert timetable.by_day(entries) == {
        "Mon": ["CSC10001", "CSC10014"],
        "Tue": ["MTH00003"],
    }
    assert entries == original


def test_merge_sorted_vectors_handles_duplicates_and_empty_inputs():
    assert translate.merge_sorted_vectors([1, 2, 2], [2, 3]) == [1, 2, 2, 2, 3]
    assert translate.merge_sorted_vectors([], [1, 3]) == [1, 3]
    assert translate.merge_sorted_vectors([], []) == []


def test_timetable_preserves_duplicate_course_entries_edge_case():
    """Duplicate timetable entries are not covered by the instructor tests."""
    assert timetable.by_day(
        [("CSC10001", "Mon"), ("CSC10001", "Mon")]
    ) == {"Mon": ["CSC10001", "CSC10001"]}
