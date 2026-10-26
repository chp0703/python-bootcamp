"""T-W3 member 6: test the shared CLI through real subprocesses.

Run: python -m pytest -q tests/test_tw3_cli.py
Requires the shared study planner entry point to be integrated first.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HEADER = "title,importance,effort_h,deadline\n"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the public module without a developer-specific PYTHONPATH."""
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "shared.study_planner", *args],
        cwd=ROOT, env=environment, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=15, check=False,
    )


def assert_failure(result: subprocess.CompletedProcess[str]) -> None:
    """Require an error on stderr and no successful plan or traceback."""
    assert result.returncode != 0, (result.stdout, result.stderr)
    assert result.stderr.strip(), "Expected an error on stderr"
    assert "Traceback" not in result.stderr, result.stderr
    assert not result.stdout.strip(), result.stdout


@pytest.fixture
def task_csv(tmp_path: Path) -> Path:
    """Create a valid task in a file whose path contains spaces."""
    path = tmp_path / "tasks with spaces.csv"
    path.write_text(HEADER + "Read notes,3,1.5,2026-10-30\n", encoding="utf-8")
    return path


def test_help_without_required_arguments() -> None:
    """Allow help without supplying required planning arguments."""
    result = run_cli("--help")
    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout.lower()
    assert "--hours" in result.stdout and "--today" in result.stdout
    assert not result.stderr.strip()


@pytest.mark.parametrize(
    "args", [(), ("samples/tasks.csv",), ("--hours", "8")],
    ids=["no-arguments", "missing-hours", "missing-csv"],
)
def test_required_arguments(args: tuple[str, ...]) -> None:
    """Missing required inputs must produce an argparse usage error."""
    result = run_cli(*args)
    assert_failure(result)
    assert result.returncode == 2
    assert "usage:" in result.stderr.lower()


@pytest.mark.parametrize("hours", ["abc", "", "1,5"])
def test_non_numeric_hours(task_csv: Path, hours: str) -> None:
    """Reject text that cannot be converted to a floating-point number."""
    result = run_cli(str(task_csv), f"--hours={hours}")
    assert_failure(result)
    assert result.returncode == 2
    assert "--hours" in result.stderr


@pytest.mark.parametrize("hours", ["-1", "nan", "inf", "-inf"])
def test_invalid_numeric_budget(task_csv: Path, hours: str) -> None:
    """Reject negative/non-finite hours without a traceback.

    Zero is omitted because the existing shared validator permits it and
    the team's infeasible-plan policy is still being integrated.
    """
    result = run_cli(str(task_csv), f"--hours={hours}")
    assert_failure(result)
    assert "hour" in result.stderr.lower() or "available_h" in result.stderr.lower()


@pytest.mark.parametrize("today", ["tomorrow", "2026-02-30", "2026-13-01"])
def test_invalid_today(task_csv: Path, today: str) -> None:
    """Reject unsupported dates and invalid calendar values."""
    result = run_cli(str(task_csv), "--hours", "2", f"--today={today}")
    assert_failure(result)
    assert result.returncode == 2
    assert "--today" in result.stderr


def test_unknown_option(task_csv: Path) -> None:
    """Reject a misspelled option instead of silently ignoring it."""
    result = run_cli(str(task_csv), "--hours", "2", "--todai", "2026-10-26")
    assert_failure(result)
    assert result.returncode == 2
    assert "--todai" in result.stderr


def test_fractional_budget_and_path_with_spaces(task_csv: Path) -> None:
    """Accept fractional hours and a file path containing spaces."""
    result = run_cli(str(task_csv), "--hours", "1.5", "--today", "2026-10-26")
    assert result.returncode == 0, result.stderr
    assert "Read notes" in result.stdout and "1.5 h" in result.stdout
    assert not result.stderr.strip()


def test_default_today(task_csv: Path) -> None:
    """Allow the optional --today argument to be omitted."""
    result = run_cli(str(task_csv), "--hours", "2")
    assert result.returncode == 0, result.stderr
    assert "Read notes" in result.stdout
    assert not result.stderr.strip()


def test_sample_from_repository_root() -> None:
    """Run the sample without installing the project as a package."""
    result = run_cli("samples/tasks.csv", "--hours", "8", "--today", "2026-10-26")
    assert result.returncode == 0, result.stderr
    assert "Assignment" in result.stdout and "DS exam" in result.stdout
    assert result.stdout.index("Assignment") < result.stdout.index("DS exam")
    assert not result.stderr.strip()


def test_today_changes_priority(tmp_path: Path) -> None:
    """Verify --today affects scheduling rather than just parsing."""
    path = tmp_path / "priority.csv"
    path.write_text(
        HEADER + "Later,5,1,2026-10-30\nEarlier,4,1,2026-10-27\n",
        encoding="utf-8",
    )
    early = run_cli(str(path), "--hours", "2", "--today", "2026-10-26")
    late = run_cli(str(path), "--hours", "2", "--today", "2026-10-30")
    assert early.returncode == late.returncode == 0, (early.stderr, late.stderr)
    assert early.stdout.index("Earlier") < early.stdout.index("Later")
    assert late.stdout.index("Later") < late.stdout.index("Earlier")


def test_missing_input_file(tmp_path: Path) -> None:
    """A missing file must name its path without a Python traceback."""
    path = tmp_path / "missing.csv"
    result = run_cli(str(path), "--hours", "8")
    assert_failure(result)
    assert path.name in result.stderr


def test_directory_as_input(tmp_path: Path) -> None:
    """Reject a directory supplied in place of a CSV file."""
    assert_failure(run_cli(str(tmp_path), "--hours", "8"))


def test_empty_input_file(tmp_path: Path) -> None:
    """An empty file must produce a readable error, not an empty plan."""
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    result = run_cli(str(path), "--hours", "8")
    assert_failure(result)
    assert "header" in result.stderr.lower() or "empty" in result.stderr.lower()
