"""Regression tests for Week 3 boundary cases and reproducible CLI output."""

from collections import Counter
from datetime import date
from importlib import import_module

import pytest

dates = import_module("members.AIVIETNAM-AIO-TheHien.w3.dates")
log_stats = import_module("members.AIVIETNAM-AIO-TheHien.w3.log_stats")


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


def test_log_stats_use_nearest_rank_without_mutating_input() -> None:
    """With 20 requests, p95 is the 19th value rather than the maximum."""
    pairs = [("fee", float(value)) for value in range(20, 0, -1)]
    original = pairs.copy()
    result = log_stats.analyse(pairs)
    assert isinstance(result["counts"], Counter)
    assert result == {"counts": {"fee": 20}, "p95": {"fee": 19}, "slowest": "fee"}
    assert pairs == original


def test_log_stats_group_routes_and_keep_first_seen_ties() -> None:
    """Interleaved routes are grouped and equal p95 keeps the first route."""
    result = log_stats.analyse(iter([("rag", 10), ("fee", 10), ("rag", 1)]))
    assert result == {
        "counts": {"rag": 2, "fee": 1},
        "p95": {"rag": 10, "fee": 10},
        "slowest": "rag",
    }


def test_empty_log_has_no_slowest_route() -> None:
    """Empty logs return empty mappings and a None route."""
    assert log_stats.analyse([]) == {"counts": {}, "p95": {}, "slowest": None}


@pytest.mark.parametrize("latency", [-1, float("nan"), float("inf")])
def test_log_stats_reject_invalid_latencies(latency: float) -> None:
    """Invalid measurements cannot silently corrupt the reported percentile."""
    with pytest.raises(ValueError, match="latency"):
        log_stats.analyse([("fee", latency)])
