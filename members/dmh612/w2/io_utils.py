"""Read tasks from CSV and write them as JSON."""

import csv
import json
from dataclasses import asdict
from datetime import date
from math import isfinite
from pathlib import Path

from .models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Read the task CSV; report invalid rows with their physical line number."""
    tasks = []
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        try:
            if reader.fieldnames != ["title", "importance", "effort_h", "deadline"]:
                raise ValueError("line 1: expected title,importance,effort_h,deadline")
            for row in reader:
                try:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError("expected four fields")
                    title = row["title"].strip()
                    effort_h = float(row["effort_h"])
                    if not title:
                        raise ValueError("title must not be empty")
                    if not isfinite(effort_h) or effort_h < 0:
                        raise ValueError("effort_h must be finite and non-negative")
                    tasks.append(
                        Task(
                            title=title,
                            importance=int(row["importance"]),
                            effort_h=effort_h,
                            deadline=date.fromisoformat(row["deadline"]),
                        )
                    )
                except (ValueError, TypeError) as error:
                    raise ValueError(f"line {reader.line_num}: {error}") from error
        except csv.Error as error:
            raise ValueError(f"line {reader.line_num}: {error}") from error
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Save tasks as UTF-8 JSON, using ISO dates for deadlines."""
    rows = [dict(asdict(task), deadline=task.deadline.isoformat()) for task in tasks]
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(rows, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
