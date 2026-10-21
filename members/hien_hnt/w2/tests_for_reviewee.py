import pytest

from members.khoi_ph.w1 import grades, rules, text_tools, timetable, translate


def test_summary_handles_odd_count_without_changing_scores():
    scores = [9, 4, 1]
    assert grades.summary(scores) == {
        "min": 1,
        "max": 9,
        "mean": 4.67,
        "median": 4,
    }
    assert scores == [9, 4, 1]


def test_summary_rejects_empty_scores():
    with pytest.raises(ValueError):
        grades.summary([])


def test_word_count_handles_case_punctuation_and_whitespace():
    assert text_tools.word_count("Git,\tgit!\nIS; is: fun?") == {
        "git": 2,
        "is": 2,
        "fun": 1,
    }


def test_top_k_orders_ties_alphabetically():
    assert text_tools.top_k("pear apple pear apple banana", 10) == [
        ("apple", 2),
        ("pear", 2),
        ("banana", 1),
    ]


def test_top_k_with_zero_returns_no_words():
    assert text_tools.top_k("git git python", 0) == []


@pytest.mark.parametrize(
    ("credits", "gpa", "expected"),
    [(120, 2.0, True), (119, 3.0, False), (130, 1.99, False)],
)
def test_thesis_eligibility_at_boundaries(credits, gpa, expected):
    assert rules.can_register_thesis(credits, gpa) is expected


def test_missing_reports_unmet_requirements():
    assert rules.missing(118, 3.1) == ["need 2 more credits"]
    assert rules.missing(120, 2.0) == []
    assert len(rules.missing(100, 1.5)) == 2
    reasons = rules.missing(120, 1.5)
    assert len(reasons) == 1 and "gpa" in reasons[0].lower()


def test_transpose_rectangular_matrix_without_changing_input():
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
def test_transpose_empty_rows_and_single_dimensions(matrix, expected):
    assert translate.transpose(matrix) == expected


def test_timetable_groups_sorts_and_preserves_duplicates():
    pairs = [("B", "Mon"), ("C", "Tue"), ("A", "Mon"), ("A", "Mon")]
    assert timetable.by_day(pairs) == {"Mon": ["A", "A", "B"], "Tue": ["C"]}
    assert pairs == [("B", "Mon"), ("C", "Tue"), ("A", "Mon"), ("A", "Mon")]
