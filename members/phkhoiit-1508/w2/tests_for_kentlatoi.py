from members.kentlatoi.w1.grades import summary
from members.kentlatoi.w1.rules import can_register_thesis, missing
from members.kentlatoi.w1.text_tools import top_k, word_count
from members.kentlatoi.w1.timetable import by_day
from members.kentlatoi.w1.translate import primes_up_to


def test_summary_even_number_of_scores():
    assert summary([7.5, 9, 6, 8]) == {
        "min": 6,
        "max": 9,
        "mean": 7.62,
        "median": 7.75,
    }


def test_summary_empty_scores_raises():
    try:
        summary([])
    except ValueError:
        pass
    else:
        raise AssertionError("summary([]) should raise ValueError")


def test_word_count_is_case_insensitive():
    assert word_count("Git git PYTHON") == {
        "git": 2,
        "python": 1,
    }


def test_top_k_sorts_alphabetically_on_tie():
    assert top_k("python git", 2) == [
        ("git", 1),
        ("python", 1),
    ]


def test_thesis_requires_credits_and_gpa():
    assert can_register_thesis(120, 2.0)
    assert not can_register_thesis(119, 2.0)
    assert not can_register_thesis(120, 1.9)


def test_missing_reports_both_requirements():
    assert missing(119, 1.9) == [
        "need 1 more credits",
        "GPA must be at least 2.0",
    ]


def test_by_day_sorts_courses():
    assert by_day(
        [
            ("CSC10014", "Mon"),
            ("MTH00003", "Tue"),
            ("CSC10001", "Mon"),
        ]
    ) == {
        "Mon": ["CSC10001", "CSC10014"],
        "Tue": ["MTH00003"],
    }


def test_primes_up_to_handles_small_numbers():
    assert primes_up_to(1) == []
    assert primes_up_to(10) == [2, 3, 5, 7]
