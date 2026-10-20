from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    importance: int  # 1–5
    effort_h: float
    deadline: date


@dataclass
class Block:
    task: Task
    hours: float