"""Additional Week 3 checks; run alongside tests/test_w3.py."""

import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import pytest

from members.dmh612.w2.models import Task
from members.dmh612.w3.cli import plan
from members.dmh612.w3.dates import parse_due
from members.dmh612.w3.log_stats import analyse

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.parametrize(
    ("text", "today", "expected"),
    [
        ("tomorrow", date(2028, 2, 28), date(2028, 2, 29)),
        ("in 3 days", date(2026, 12, 30), date(2027, 1, 2)),
        (" Tuesday ", date(2026, 10, 6), date(2026, 10, 13)),
        ("SUN", date(2026, 10, 10), date(2026, 10, 11)),
        ("in 0 days", date(2026, 10, 6), date(2026, 10, 6)),
    ],
)
def test_date_boundaries(text: str, today: date, expected: date) -> None:
    """Check calendar transitions and strictly future weekday occurrences."""
    assert parse_due(text, today) == expected


@pytest.mark.parametrize("text", ["", "2026-02-29", "in -1 days", "20261030", "soon"])
def test_unknown_dates(text: str) -> None:
    """Reject invalid calendar dates and unsupported expressions."""
    with pytest.raises(ValueError):
        parse_due(text, date(2026, 10, 6))


def test_p95_nearest_rank_with_twenty_samples() -> None:
    """Distinguish nearest-rank p95 from maximum and interpolation."""
    result = analyse(("route", latency) for latency in range(20, 0, -1))
    assert isinstance(result["counts"], Counter)
    assert result["counts"] == {"route": 20}
    assert result["p95"] == {"route": 19}


def test_empty_logs_and_tied_routes() -> None:
    """Define an empty result and order-independent tie handling."""
    assert analyse([]) == {"counts": {}, "p95": {}, "slowest": None}
    assert analyse([("z", 0), ("a", 0)])["slowest"] == "a"


@pytest.mark.parametrize("latency", [-1, float("nan"), float("inf")])
def test_invalid_latency(latency: float) -> None:
    """Reject measurements without a meaningful latency percentile."""
    with pytest.raises(ValueError):
        analyse([("route", latency)])


def test_plan_uses_today_and_preserves_tasks() -> None:
    """Changing the reference date can change priority without mutating tasks."""
    tasks = [
        Task("Later", 5, 3, date(2026, 10, 30)),
        Task("Earlier", 4, 1.5, date(2026, 10, 27)),
    ]
    blocks = plan(tasks, 2, date(2026, 10, 26))
    assert [(task.title, hours) for task, hours in blocks] == [
        ("Earlier", 1.5), ("Later", 0.5),
    ]
    assert plan(tasks, 2, date(2026, 10, 30)) == [(tasks[0], 2)]
    assert tasks[0].effort_h == 3
    assert tasks[0].title == "Later"


def test_plan_handles_overdue_zero_effort_and_unused_time() -> None:
    """Skip completed tasks and never allocate above the requested effort."""
    today = date(2026, 10, 26)
    tasks = [Task("Done", 5, 0, today), Task("Overdue", 4, 1, date(2026, 10, 1))]
    assert plan(tasks, 3, today) == [(tasks[1], 1)]
    assert plan([], 3, today) == []


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Execute the package exactly as a user would from the repository root."""
    return subprocess.run(
        [sys.executable, "-m", "members.dmh612.w3.cli", *args],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )


def test_cli_sample_and_missing_file(tmp_path: Path) -> None:
    """Check exact sample allocations and the required missing-file exit code."""
    result = run_cli("samples/tasks.csv", "--hours", "2", "--today", "2026-10-26")
    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        "Tonight (2.0 h):", "1. Assignment ...... 1.5 h", "2. DS exam ...... 0.5 h",
    ]
    missing = run_cli(str(tmp_path / "missing.csv"), "--hours", "2")
    assert missing.returncode == 1
    assert "File not found" in missing.stderr
    assert "Traceback" not in missing.stderr


@pytest.mark.parametrize("hours", ["0", "-1", "nan", "inf", "abc"])
def test_cli_invalid_budget(hours: str) -> None:
    """Reject invalid budgets through argparse with exit code two."""
    result = run_cli("samples/tasks.csv", f"--hours={hours}")
    assert result.returncode == 2
    assert "hours" in result.stderr


def test_cli_bad_csv_and_empty_tasks(tmp_path: Path) -> None:
    """Report malformed CSV and handle a valid header-only file."""
    csv_path = tmp_path / "tasks.csv"
    csv_path.write_text("invalid\n", encoding="utf-8")
    bad = run_cli(str(csv_path), "--hours", "2")
    assert bad.returncode == 1
    assert "line 1" in bad.stderr
    csv_path.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")
    empty = run_cli(str(csv_path), "--hours", "2")
    assert empty.returncode == 0
    assert "No tasks to schedule" in empty.stdout


def test_cli_invalid_today() -> None:
    """Report invalid dates without a traceback."""
    result = run_cli("samples/tasks.csv", "--hours", "2", "--today", "2026-02-30")
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
