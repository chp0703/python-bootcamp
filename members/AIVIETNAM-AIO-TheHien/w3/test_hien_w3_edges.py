"""Member 2 regression tests for Week 3 boundaries and reproducible CLI output."""

import subprocess
import sys
from collections import Counter
from datetime import date
from importlib import import_module
from pathlib import Path

import pytest

dates = import_module("members.AIVIETNAM-AIO-TheHien.w3.dates")
log_stats = import_module("members.AIVIETNAM-AIO-TheHien.w3.log_stats")
ROOT = Path(__file__).resolve().parents[3]
CLI = "members.AIVIETNAM-AIO-TheHien.w3.cli"


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


@pytest.mark.parametrize(
    "text", ["", "someday", "2026-02-29", "in -1 days", "20261030"]
)
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


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Run the public personal CLI in a fresh Python process."""
    return subprocess.run(
        [sys.executable, "-m", CLI, *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def test_cli_allocates_a_partial_plan_in_priority_order() -> None:
    """A two-hour budget succeeds even though all tasks need 7.5 hours."""
    result = run_cli("samples/tasks.csv", "--hours", "2", "--today", "2026-10-26")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.splitlines() == [
        "STUDY PLAN",
        "1. Assignment - 1.5 h",
        "2. DS exam - 0.5 h",
        "",
        "Total: 2.0 h",
    ]


def test_cli_uses_the_supplied_today_for_priority() -> None:
    """Changing today changes which task receives a limited budget."""
    result = run_cli("samples/tasks.csv", "--hours", "2", "--today", "2026-10-29")
    assert result.returncode == 0, result.stderr
    assert "1. DS exam - 2.0 h" in result.stdout
    assert "Assignment" not in result.stdout


def test_cli_reports_missing_file_without_traceback() -> None:
    """Missing CSV paths produce a useful error instead of a traceback."""
    result = run_cli("missing-w3.csv", "--hours", "2")
    assert result.returncode == 1
    assert result.stdout == ""
    assert "missing-w3.csv" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("hours", ["-1", "nan", "inf", "many"])
def test_cli_rejects_invalid_hour_budgets(hours: str) -> None:
    """argparse rejects invalid budgets before planning."""
    result = run_cli("samples/tasks.csv", "--hours", hours)
    assert result.returncode == 2
    assert "hours" in result.stderr


def test_cli_reports_bad_csv_with_its_line_number() -> None:
    """CSV diagnostics from the personal W2 loader reach the CLI user."""
    result = run_cli("samples/tasks_bad.csv", "--hours", "2")
    assert result.returncode == 1
    assert "line 3" in result.stderr
    assert "Traceback" not in result.stderr
