"""Run with python -m members.dmh612.w2 [tasks.csv]."""

import sys
from pathlib import Path

from .io_utils import load_tasks


def main() -> int:
    """Load the sample CSV by default and print each task."""
    sample = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else sample
    try:
        tasks = load_tasks(path)
    except (OSError, ValueError) as error:
        print(f"Cannot load tasks: {error}", file=sys.stderr)
        return 1
    for task in tasks:
        print(
            f"{task.title} | importance={task.importance} | "
            f"effort_h={task.effort_h:g} | deadline={task.deadline.isoformat()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
