"""Focused edge cases for the personal Week 3 helpers."""

from datetime import date

import pytest

from members.kentlatoi.w3.dates import parse_due
from members.kentlatoi.w3.log_stats import analyse


def test_due_dates_handle_next_weekday_and_invalid_iso() -> None:
    today = date(2026, 10, 6)
    assert parse_due("  TUE  ", today) == date(2026, 10, 13)
    assert parse_due("In 0 Days", today) == today
    with pytest.raises(ValueError):
        parse_due("2026-02-30", today)


def test_latency_empty_and_nearest_rank() -> None:
    assert analyse([]) == {"counts": {}, "p95": {}, "slowest": None}
    assert analyse([("a", 10), ("a", 20), ("a", 30)])["p95"]["a"] == 30
