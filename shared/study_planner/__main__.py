"""Command-line entry point for the study planner."""

import argparse
import sys
from datetime import date

from .allocate import allocate
from .parse import parse_csv
from .prioritise import prioritise
from .render import render
from .validate import validate_inputs


def main() -> int:
    """Build and print a study plan from a task CSV file."""
    parser = argparse.ArgumentParser(
        description="Create a study plan from a CSV task list."
    )
    parser.add_argument("csv_path", help="path to the task CSV file")
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="number of study hours available",
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="current date used for prioritisation (default: today)",
    )
    args = parser.parse_args()

    try:
        tasks = parse_csv(args.csv_path)
        validate_inputs(tasks, args.hours)
        prioritised_tasks = prioritise(tasks, args.today)
        blocks = allocate(prioritised_tasks, args.hours)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(render(blocks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
