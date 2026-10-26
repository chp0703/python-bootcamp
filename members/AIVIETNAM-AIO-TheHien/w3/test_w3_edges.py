"""Regression tests for Week 3 boundary cases and reproducible CLI output."""

from datetime import date
from importlib import import_module

import pytest

dates = import_module("members.AIVIETNAM-AIO-TheHien.w3.dates")


@pytest.mark.parametrize(
    ("text", "today", "expected"),
    [
        ("Tue", date(2026, 10, 6), date(2026, 10, 13)),
        ("  FRIDAY  ", date(2026, 10, 6), date(2026, 10, 9)),
        ("Mon", date(2026, 10, 11), date(2026, 10, 12)),
        ("tomorrow", date(2026, 12, 31), date(2027, 1, 1)),
        ("in 1 day", date(2028, 2, 28), date(2028, 2, 29)),
        ("in 0 days", date(2026, 10, 6), date(2026, 10, 6)),
    ],
)
def test_due_dates_cross_boundaries(text: str, today: date, expected: date) -> None:
    """Relative dates handle same weekdays, leap days, and year boundaries."""
    assert dates.parse_due(text, today) == expected


@pytest.mark.parametrize("text", ["", "someday", "2026-02-29", "in -1 days", "20261030"])
def test_due_dates_reject_unknown_or_invalid_text(text: str) -> None:
    """Invalid inputs consistently report ValueError."""
    with pytest.raises(ValueError):
        dates.parse_due(text, date(2026, 10, 6))
