"""Build a study plan using the personal W2 loader and shared planning tools."""

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from math import isfinite
from pathlib import Path

from shared.contract import Task
from shared.study_planner.allocate import allocate
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render

from ..w2.io_utils import load_tasks


def _hours(text: str) -> float:
    """Accept a finite, non-negative study budget for argparse."""
    try:
        hours = float(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("hours must be a number") from error
    if not isfinite(hours) or hours < 0:
        raise argparse.ArgumentTypeError("hours must be finite and non-negative")
    return hours


def main(argv: Sequence[str] | None = None) -> int:
    """Print a greedy study plan; report file/data errors with exit code 1."""
    parser = argparse.ArgumentParser(description="Plan your available study hours.")
    parser.add_argument("csv_path", type=Path, help="task CSV file")
    parser.add_argument("--hours", type=_hours, required=True, help="available hours")
    parser.add_argument(
        "--today", type=date.fromisoformat, default=date.today(), metavar="YYYY-MM-DD"
    )
    args = parser.parse_args(argv)

    try:
        tasks = [
            Task(task.title, task.importance, task.effort_h, task.deadline)
            for task in load_tasks(args.csv_path)
        ]
        blocks = allocate(prioritise(tasks, args.today), args.hours)
    except FileNotFoundError:
        print(f"Error: CSV file not found: {args.csv_path}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(render(blocks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
