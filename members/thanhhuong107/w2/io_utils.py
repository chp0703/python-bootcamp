"""CSV and JSON helpers for study-planner tasks."""

import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from .models import Task

PathLike = str | Path
HEADERS = ["title", "importance", "effort_h", "deadline"]


def load_tasks(path: PathLike) -> list[Task]:
    """Load tasks from a CSV file, reporting malformed data with its line."""
    tasks: list[Task] = []
    with Path(path).open("r", newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != HEADERS:
            raise ValueError(f"line 1: expected CSV header {','.join(HEADERS)}")

        try:
            for row in reader:
                line = reader.line_num
                if None in row or any(row.get(name) is None for name in HEADERS):
                    raise ValueError(f"line {line}: expected exactly four columns")
                try:
                    task = Task(
                        title=row["title"].strip(),
                        importance=int(row["importance"].strip()),
                        effort_h=float(row["effort_h"].strip()),
                        deadline=date.fromisoformat(row["deadline"].strip()),
                    )
                    if not task.title:
                        raise ValueError("title cannot be empty")
                    tasks.append(task)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"line {line}: invalid task row ({exc})") from exc
        except csv.Error as exc:
            raise ValueError(f"line {reader.line_num}: invalid CSV ({exc})") from exc

    return tasks


def save_json(tasks: list[Task], path: PathLike) -> None:
    """Save tasks as readable JSON, with deadlines in ISO date format."""
    records = []
    for task in tasks:
        record = asdict(task)
        record["deadline"] = task.deadline.isoformat()
        records.append(record)

    with Path(path).open("w", encoding="utf-8") as stream:
        json.dump(records, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
