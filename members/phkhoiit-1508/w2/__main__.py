from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    sample_path = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"

    for task in load_tasks(sample_path):
        print(task)


if __name__ == "__main__":
    main()
