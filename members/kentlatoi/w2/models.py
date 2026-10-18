from dataclasses import dataclass
from datetime import date

@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self):
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be between 1 and 5")

    def days_left(self, today: date) -> int:
        remaining_days = (self.deadline - today).days
        return max(0, remaining_days)
