"""Command-line study planner for a CSV task list."""

import argparse
from datetime import date
from importlib import import_module
from pathlib import Path
from typing import Sequence

from shared.study_planner.allocate import allocate
from shared.study_planner.prioritise import prioritise

load_tasks = import_module("members.phkhoiit-1508.w2.io_utils").load_tasks


def _date_argument(value: str) -> date:
    """Parse an ISO date for argparse."""
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD format") from error


def build_parser() -> argparse.ArgumentParser:
    """Build the study planner argument parser."""
    parser = argparse.ArgumentParser(description="Allocate study time across tasks.")
    parser.add_argument("csv_file", type=Path, help="path to the tasks CSV file")
    parser.add_argument("--hours", type=float, required=True, help="available study hours")
    parser.add_argument("--today", type=_date_argument, default=None, metavar="YYYY-MM-DD")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Load tasks, allocate available hours, and print a readable plan."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.hours < 0:
        parser.error("--hours must be non-negative")
    try:
        tasks = load_tasks(args.csv_file)
    except FileNotFoundError:
        parser.exit(1, f"error: file not found: {args.csv_file}\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"error: could not read {args.csv_file}: {error}\n")
    today = args.today or date.today()
    blocks = allocate(prioritise(tasks, today), args.hours)
    print(f"Tonight ({args.hours:.1f} h):")
    for index, block in enumerate(blocks, start=1):
        print(f"  {index}. {block.task.title} ........ {block.hours:.1f} h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
