import argparse
import sys
from datetime import date
from pathlib import Path

from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.allocate import allocate
from shared.study_planner.render import render


def main() -> int:
    """Generate and print a study plan from a task CSV file."""
    parser = argparse.ArgumentParser(
        description="Generate a study plan from a CSV file"
    )

    parser.add_argument("csv_path", help="Path to the tasks CSV file")
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Available study hours",
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Current date in YYYY-MM-DD format",
    )

    args = parser.parse_args()

    file_path = Path(args.csv_path)

    if not file_path.is_file():
        print(
            f"Error: file not found: {file_path}",
            file=sys.stderr,
        )
        return 1
    try:
        tasks = parse_csv(file_path)
        ordered_tasks = prioritise(tasks, args.today)
        blocks = allocate(ordered_tasks, args.hours)
        result = render(blocks)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(result)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
