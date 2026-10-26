"""Display the sample CSV using the personal Week 2 package."""

from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    """Load and print each task from the repository sample."""
    sample = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"
    for task in load_tasks(sample):
        print(
            f"{task.title} | importance: {task.importance} | "
            f"effort: {task.effort_h:g} h | deadline: {task.deadline.isoformat()}"
        )


if __name__ == "__main__":
    main()
