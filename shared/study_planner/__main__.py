"""Command-line entry point for the study planner."""

import argparse
from datetime import date

from .allocate import allocate
from .parse import parse_csv
from .prioritise import prioritise
from .render import render


def main() -> None:
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

    tasks = parse_csv(args.csv_path)
    prioritised_tasks = prioritise(tasks, args.today)
    blocks = allocate(prioritised_tasks, args.hours)
    print(render(blocks))


if __name__ == "__main__":
    main()