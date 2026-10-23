"""Command-line study planner for a CSV task list."""

import argparse
from datetime import date
from pathlib import Path
from typing import Sequence

from members.thanhhuong107.w2.io_utils import load_tasks
from members.thanhhuong107.w2.models import Task


def _date_argument(value: str) -> date:
    """Convert an ISO date argument or raise an argparse-friendly error."""
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD format") from exc


def _allocate(
    tasks: list[Task], available_h: float, today: date
) -> list[tuple[str, float]]:
    """Prioritize by deadline then importance and fit work into available hours."""
    ordered = sorted(tasks, key=lambda task: (task.days_left(today), -task.importance))
    blocks: list[tuple[str, float]] = []
    remaining = available_h
    for task in ordered:
        if remaining <= 0:
            break
        hours = min(task.effort_h, remaining)
        blocks.append((task.title, hours))
        remaining -= hours
    return blocks


def build_parser() -> argparse.ArgumentParser:
    """Build the study planner's argument parser."""
    parser = argparse.ArgumentParser(description="Allocate study time across tasks.")
    parser.add_argument("csv_file", type=Path, help="path to the tasks CSV file")
    parser.add_argument(
        "--hours", type=float, required=True, help="available study hours"
    )
    parser.add_argument(
        "--today", type=_date_argument, default=None, metavar="YYYY-MM-DD",
        help="reference date for prioritization (defaults to today)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the planner, printing an allocation or a clear input error."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.hours < 0:
        parser.error("--hours must be non-negative")
    try:
        tasks = load_tasks(args.csv_file)
    except FileNotFoundError:
        parser.exit(1, f"error: file not found: {args.csv_file}\n")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"error: could not read {args.csv_file}: {exc}\n")

    today = args.today or date.today()
    blocks = _allocate(tasks, args.hours, today)
    print(f"Tonight ({args.hours:.1f} h):")
    for index, (title, hours) in enumerate(blocks, start=1):
        print(f"  {index}. {title} ........ {hours:.1f} h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
