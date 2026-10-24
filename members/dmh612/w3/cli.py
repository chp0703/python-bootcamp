"""Build a partial evening plan using the individual's Week 2 task loader."""

import argparse
import sys
from datetime import date
from math import isfinite
from pathlib import Path

from ..w2.io_utils import load_tasks
from ..w2.models import Task


def positive_hours(text: str) -> float:
    """Convert an argparse value into a finite, positive number of hours."""
    try:
        hours = float(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("hours must be a number") from error
    if not isfinite(hours) or hours <= 0:
        raise argparse.ArgumentTypeError("hours must be finite and positive")
    return hours


def plan(tasks: list[Task], hours: float, today: date) -> list[tuple[Task, float]]:
    """Prioritise by importance/days left and allocate up to the time budget.

    Due and overdue tasks use a denominator of one. Equal priorities retain
    CSV order. A task can receive only part of its requested effort.
    """
    if not isfinite(hours) or hours <= 0:
        raise ValueError("hours must be finite and positive")
    ordered = sorted(
        tasks, key=lambda task: task.importance / max(task.days_left(today), 1),
        reverse=True,
    )
    remaining = hours
    blocks = []
    for task in ordered:
        if remaining <= 0:
            break
        allocated = min(task.effort_h, remaining)
        if allocated > 0:
            blocks.append((task, allocated))
            remaining -= allocated
    return blocks


def main(argv: list[str] | None = None) -> int:
    """Read CSV tasks, print tonight's plan, and report file errors on stderr."""
    parser = argparse.ArgumentParser(description="Plan tonight's study tasks.")
    parser.add_argument("path", type=Path, help="task CSV file")
    parser.add_argument("--hours", required=True, type=positive_hours)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)
    try:
        tasks = load_tasks(args.path)
    except FileNotFoundError:
        print(f"File not found: {args.path}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Cannot load tasks: {error}", file=sys.stderr)
        return 1
    blocks = plan(tasks, args.hours, args.today)
    print(f"Tonight ({args.hours:.1f} h):")
    for index, (task, hours) in enumerate(blocks, start=1):
        print(f"{index}. {task.title} ...... {hours:g} h")
    if not blocks:
        print("No tasks to schedule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
