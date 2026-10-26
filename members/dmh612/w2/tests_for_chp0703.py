"""W2-4: Hung's cross-tests for chp0703's actual Week 1 functions.

Run explicitly: python -m pytest -q members/dmh612/w2/tests_for_chp0703.py
The odd-length median, punctuation-only text, duplicate search keys, and
repeated timetable entries are not covered by tests/test_w1.py.
"""

import pytest

from members.chp0703.w1.grades import summary
from members.chp0703.w1.rules import can_register_thesis, missing
from members.chp0703.w1.text_tools import top_k, word_count
from members.chp0703.w1.timetable import by_day
from members.chp0703.w1.translate import binary_search


def test_summary_odd_count_rounds_mean_and_preserves_input() -> None:
    """Check summary odd count rounds mean and preserves input."""
    scores = [9.0, 4.5, 7.0]
    assert summary(scores) == {
        "min": 4.5,
        "max": 9.0,
        "mean": 6.83,
        "median": 7.0,
    }
    assert scores == [9.0, 4.5, 7.0]


def test_summary_rejects_empty_scores() -> None:
    """Check summary rejects empty scores."""
    with pytest.raises(ValueError):
        summary([])


def test_word_count_punctuation_only_is_empty() -> None:
    """Check word count punctuation only is empty."""
    assert word_count(".,!?;: \t\n") == {}


def test_word_count_handles_adjacent_punctuation_and_vietnamese() -> None:
    """Check word count handles adjacent punctuation and vietnamese."""
    assert word_count("Học,Python! HỌC;Git:python?") == {
        "học": 2,
        "python": 2,
        "git": 1,
    }


def test_top_k_sorts_ties_alphabetically_even_if_seen_in_reverse_order() -> None:
    """Check top k sorts ties alphabetically even if seen in reverse order."""
    assert top_k("zebra apple zebra apple mango", 2) == [
        ("apple", 2),
        ("zebra", 2),
    ]


def test_top_k_zero_and_more_than_distinct_word_count() -> None:
    """Check top k zero and more than distinct word count."""
    assert top_k("Git Python", 0) == []
    assert top_k("Git git Python", 10) == [("git", 2), ("python", 1)]


def test_thesis_rejects_gpa_just_below_threshold_with_enough_credits() -> None:
    """Check thesis rejects gpa just below threshold with enough credits."""
    assert not can_register_thesis(120, 1.99)
    assert len(missing(120, 1.99)) == 1
    assert can_register_thesis(120, 2.0)
    assert missing(120, 2.0) == []


def test_binary_search_first_and_last_elements_and_outside_range() -> None:
    """Check binary search first and last elements and outside range."""
    values = [-5, 0, 3, 8]
    assert binary_search(values, -5) == 0
    assert binary_search(values, 8) == 3
    assert binary_search(values, -6) == -1
    assert binary_search(values, 9) == -1


def test_binary_search_duplicate_keys_returns_a_matching_index() -> None:
    """Check binary search duplicate keys returns a matching index."""
    values = [1, 2, 2, 2, 5]
    index = binary_search(values, 2)
    assert index in (1, 2, 3)
    assert values[index] == 2
    assert values == [1, 2, 2, 2, 5]


def test_timetable_preserves_repeated_entries_and_input_order() -> None:
    """Check timetable preserves repeated entries and input order."""
    entries = [("B", "Mon"), ("A", "Mon"), ("A", "Mon"), ("C", "Tue")]
    assert by_day(entries) == {"Mon": ["A", "A", "B"], "Tue": ["C"]}
    assert entries == [("B", "Mon"), ("A", "Mon"), ("A", "Mon"), ("C", "Tue")]
