"""Load and print the sample study plan with ``python -m members.thanhhuong107.w2``."""

from pathlib import Path

from .io_utils import load_tasks


def main() -> None:
    sample_csv = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"
    for task in load_tasks(sample_csv):
        print(task)


if __name__ == "__main__":
    main()
