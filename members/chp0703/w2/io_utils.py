import csv
import json
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load valid task rows from a CSV file."""
    tasks = []

    with open(path, "r" , newline = "", encoding= "utf-8-sig") as file:
        reader  = csv.DictReader(file)

        expected_header =[ 
            "title",
            "importance",
            "effort_h",
            "deadline",
        ]
        if reader.fieldnames != expected_header:
            raise ValueError("Invalid CSV header at line 1")

        for line_number, row in enumerate(reader, start =2):
            try:
                task = Task(
                    title=row["title"].strip(),
                    importance=int(row["importance"]),
                    effort_h= float(row["effort_h"]),
                    deadline=date.fromisoformat(row["deadline"]),
                )

                tasks.append(task)
            except (ValueError, TypeError, AttributeError) as error:
                raise ValueError(
                f"Invalid row at line {line_number}: {error}"
                ) from error
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Serialize tasks to a UTF-8 JSON file."""
    data = []

    for task in tasks:
        data.append({
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            "deadline": task.deadline.isoformat(),
        })

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
