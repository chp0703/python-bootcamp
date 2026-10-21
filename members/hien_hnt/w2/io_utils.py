import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    tasks = []
    expected = ["title", "importance", "effort_h", "deadline"]
    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, strict=True)
        try:
            header = reader.fieldnames
            if header is None or len(header) != len(expected) or set(header) != set(expected):
                raise ValueError("line 1: expected header title,importance,effort_h,deadline")

            for row in reader:
                try:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("expected four fields")
                    task = Task(
                        title=row["title"].strip(),
                        importance=int(row["importance"]),
                        effort_h=float(row["effort_h"]),
                        deadline=date.fromisoformat(row["deadline"].strip()),
                    )
                except ValueError as error:
                    raise ValueError(f"line {reader.line_num}: {error}") from error
                tasks.append(task)
        except csv.Error as error:
            raise ValueError(f"line {max(reader.reader.line_num, 1)}: {error}") from error
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    data = [
        {**asdict(task), "deadline": task.deadline.isoformat()}
        for task in tasks
    ]
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
