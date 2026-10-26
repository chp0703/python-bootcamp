"""Define and validate the personal Week 2 task model."""

from dataclasses import dataclass
from datetime import date
from math import isfinite


@dataclass
class Task:
    """A named task with importance, positive effort, and a deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Reject empty titles, invalid importance, and invalid effort."""
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be between 1 and 5")
        if not isfinite(self.effort_h) or self.effort_h <= 0:
            raise ValueError("effort_h must be a positive finite number")

    def days_left(self, today: date) -> int:
        """Count remaining days, returning zero for overdue tasks."""
        return max((self.deadline - today).days, 0)
