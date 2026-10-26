"""T-W3 Member 2: verify successful CSV-to-plan flows through the real CLI."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_planner(csv_path: Path, hours: float) -> subprocess.CompletedProcess[str]:
    """Run the integrated CLI with a fixed date and portable UTF-8 output."""
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "shared.study_planner",
            str(csv_path),
            "--hours",
            str(hours),
            "--today",
            "2026-10-26",
        ],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )


@pytest.mark.parametrize(
    ("hours", "expected_lines"),
    [
        (
            2.0,
            [
                "STUDY PLAN",
                "1. Assignment - 1.5 h",
                "2. DS exam - 0.5 h",
                "",
                "Total: 2.0 h",
            ],
        ),
        (
            8.0,
            [
                "STUDY PLAN",
                "1. Assignment - 1.5 h",
                "2. DS exam - 6.0 h",
                "",
                "Total: 7.5 h",
            ],
        ),
    ],
    ids=["partial-plan", "all-tasks-fit"],
)
def test_sample_csv_to_rendered_plan(hours: float, expected_lines: list[str]) -> None:
    """Verify parsing, priority, greedy allocation, and rendering together."""
    result = run_planner(ROOT / "samples" / "tasks.csv", hours)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.splitlines() == expected_lines


def test_quoted_unicode_csv_to_fractional_plan(tmp_path: Path) -> None:
    """Preserve CSV titles and allocate a fractional final block in order."""
    csv_path = tmp_path / "tasks with spaces.csv"
    csv_path.write_text(
        "title,importance,effort_h,deadline\n"
        '"Project, part A",3,1.5,2026-10-30\n'
        "Ôn thi,5,2,2026-10-27\n"
        "Review,4,1,2026-10-28\n",
        encoding="utf-8",
    )
    result = run_planner(csv_path, 3.5)
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.splitlines() == [
        "STUDY PLAN",
        "1. Ôn thi - 2.0 h",
        "2. Review - 1.0 h",
        "3. Project, part A - 0.5 h",
        "",
        "Total: 3.5 h",
    ]
