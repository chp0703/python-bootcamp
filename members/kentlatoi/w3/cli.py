"""Command-line study planner for the personal Week 3 homework."""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from members.kentlatoi.w2.io_utils import load_tasks
from shared.study_planner.allocate import allocate
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render


def iso_date(text: str) -> date:
    """Convert an ISO date for argparse with a useful error message."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise argparse.ArgumentTypeError("--today must be YYYY-MM-DD")
    try:
        return date.fromisoformat(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--today must be YYYY-MM-DD") from error


def nonnegative_hours(text: str) -> float:
    """Convert available hours and reject negative or nonfinite values."""
    try:
        hours = float(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--hours must be a number") from error
    if not 0 <= hours < float("inf"):
        raise argparse.ArgumentTypeError("--hours must be finite and non-negative")
    return hours


def main(argv: list[str] | None = None) -> int:
    """Read tasks, allocate study time, and print the resulting plan."""
    parser = argparse.ArgumentParser(description="Create a study plan from task CSV")
    parser.add_argument("csv_path", type=Path, help="task CSV file")
    parser.add_argument("--hours", type=nonnegative_hours, required=True)
    parser.add_argument("--today", type=iso_date, default=date.today())
    args = parser.parse_args(argv)

    try:
        tasks = load_tasks(args.csv_path)
    except (OSError, ValueError) as error:
        print(f"Error reading {args.csv_path}: {error}", file=sys.stderr)
        return 1

    print(render(allocate(prioritise(tasks, args.today), args.hours)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
