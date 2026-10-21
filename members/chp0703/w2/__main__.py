"""Run the Week 2 task loader with the repository sample data."""
from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    """Load and display the bundled task sample."""
    repository_root = Path(__file__).resolve().parents[3]
    sample_path = repository_root / "samples" / "tasks.csv"
    if not sample_path.is_file():
        raise FileNotFoundError(f"Task sample was not found: {sample_path}")

    tasks = load_tasks(sample_path)
    for task in tasks:
        print(
            f"- {task.title}: importance {task.importance}, "
            f"{task.effort_h:g} hours, due {task.deadline.isoformat()}"
        )


if __name__ == "__main__":
    main()
