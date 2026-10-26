"""Task model used by the Week 2 study planner."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Reject task importance values outside the supported 1–5 range."""
        if (
            isinstance(self.importance, bool)
            or not isinstance(self.importance, int)
            or not 1 <= self.importance <= 5
        ):
            raise ValueError("importance must be between 1 and 5")

    def days_left(self, today: date) -> int:
        """Return the non-negative number of days until the deadline."""
        return max(0, (self.deadline - today).days)
