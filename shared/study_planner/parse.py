import csv
from datetime import date
from pathlib import Path

from shared.contract import Task


def parse_csv(path: str | Path) -> list[Task]:
    """Parse a CSV file into a list of Task objects."""
    tasks = []

    expected_header = [
        "title",
        "importance",
        "effort_h",
        "deadline",
    ]

    with open(path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != expected_header:
            raise ValueError(
                "Invalid CSV header at line 1. "
                f"Expected: {','.join(expected_header)}"
            )

        for row in reader:
            line_number = reader.line_num

            try:
                if None in row:
                    raise ValueError("too many columns")

                title = row["title"]
                importance_text = row["importance"]
                effort_text = row["effort_h"]
                deadline_text = row["deadline"]

                if title is None:
                    raise ValueError("missing title")

                if any(
                    value is None or not value.strip()
                    for value in (
                        importance_text,
                        effort_text,
                        deadline_text,
                    )
                ):
                    raise ValueError("missing required field")

                task = Task(
                    title=title.strip(),
                    importance=int(importance_text),
                    effort_h=float(effort_text),
                    deadline=date.fromisoformat(deadline_text.strip()),
                )

                tasks.append(task)

            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(
                    f"Invalid CSV row at line {line_number}: {error}"
                ) from error

    return tasks