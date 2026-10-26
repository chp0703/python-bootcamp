"""Cross-test Member 3's Week 1 homework and boundary behaviour."""

from importlib import import_module

import pytest

grades = import_module("members.phkhoiit-1508.w1.grades")
rules = import_module("members.phkhoiit-1508.w1.rules")
text_tools = import_module("members.phkhoiit-1508.w1.text_tools")
timetable = import_module("members.phkhoiit-1508.w1.timetable")
translate = import_module("members.phkhoiit-1508.w1.translate")


def test_summary_handles_odd_count_without_changing_scores() -> None:
    """Odd-length summaries preserve their input."""
    scores = [9, 4, 1]
    assert grades.summary(scores) == {
        "min": 1,
        "max": 9,
        "mean": 4.67,
        "median": 4,
    }
    assert scores == [9, 4, 1]


def test_summary_rejects_empty_scores() -> None:
    """An empty grade list has no summary."""
    with pytest.raises(ValueError):
        grades.summary([])


def test_word_count_handles_case_punctuation_and_whitespace() -> None:
    """Case, punctuation, and whitespace do not split equivalent words."""
    assert text_tools.word_count("Git,\tgit!\nIS; is: fun?") == {
        "git": 2,
        "is": 2,
        "fun": 1,
    }


def test_top_k_orders_ties_alphabetically() -> None:
    """Tied word counts use alphabetical order."""
    assert text_tools.top_k("pear apple pear apple banana", 10) == [
        ("apple", 2),
        ("pear", 2),
        ("banana", 1),
    ]


def test_top_k_with_zero_returns_no_words() -> None:
    """A zero-size request returns no ranked words."""
    assert text_tools.top_k("git git python", 0) == []


@pytest.mark.parametrize(
    ("credits", "gpa", "expected"),
    [(120, 2.0, True), (119, 3.0, False), (130, 1.99, False)],
)
def test_thesis_eligibility_at_boundaries(
    credits: int, gpa: float, expected: bool
) -> None:
    """Check both eligibility thresholds exactly."""
    assert rules.can_register_thesis(credits, gpa) is expected


def test_missing_reports_unmet_requirements() -> None:
    """Report each unmet thesis requirement."""
    assert rules.missing(118, 3.1) == ["need 2 more credits"]
    assert rules.missing(120, 2.0) == []
    assert len(rules.missing(100, 1.5)) == 2
    reasons = rules.missing(120, 1.5)
    assert len(reasons) == 1 and "gpa" in reasons[0].lower()


def test_transpose_rectangular_matrix_without_changing_input() -> None:
    """Rectangular transposition preserves the source matrix."""
    matrix = [[1, 2], [3, 4], [5, 6]]
    assert translate.transpose(matrix) == [[1, 3, 5], [2, 4, 6]]
    assert matrix == [[1, 2], [3, 4], [5, 6]]


@pytest.mark.parametrize(
    ("matrix", "expected"),
    [
        ([[]], []),
        ([[], []], []),
        ([[1, 2, 3]], [[1], [2], [3]]),
        ([[1], [2], [3]], [[1, 2, 3]]),
    ],
)
def test_transpose_empty_rows_and_single_dimensions(
    matrix: list[list[int]], expected: list[list[int]]
) -> None:
    """Handle empty rows and single-row or single-column matrices."""
    assert translate.transpose(matrix) == expected


def test_timetable_groups_sorts_and_preserves_duplicates() -> None:
    """Grouping sorts course names and preserves duplicate registrations."""
    pairs = [("B", "Mon"), ("C", "Tue"), ("A", "Mon"), ("A", "Mon")]
    assert timetable.by_day(pairs) == {"Mon": ["A", "A", "B"], "Tue": ["C"]}
    assert pairs == [("B", "Mon"), ("C", "Tue"), ("A", "Mon"), ("A", "Mon")]
