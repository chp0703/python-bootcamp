import csv
import json
from datetime import date
from pathlib import Path

from members.kentlatoi.w2.models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load tasks from the bootcamp CSV format."""
    tasks = []

    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                task = Task(
                    title=row["title"],
                    importance=int(row["importance"]),
                    effort_h=float(row["effort_h"]),
                    deadline=date.fromisoformat(row["deadline"]),
                )

                tasks.append(task)

            except (ValueError, TypeError, KeyError) as error:
                raise ValueError(
                    f"Invalid data at line {reader.line_num}: {error}"
                ) from error

    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Write tasks as readable JSON with ISO-formatted deadlines."""
    data = []

    for task in tasks:
        task_data = {
            "title": task.title,
            "importance": task.importance,
            "effort_h": task.effort_h,
            "deadline": task.deadline.isoformat(),
        }

        data.append(task_data)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
