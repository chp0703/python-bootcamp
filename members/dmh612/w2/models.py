"""Task model for the individual Week 2 exercises."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """A study task with importance from 1 to 5 and a deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Validate the importance range after dataclass initialisation."""
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")

    def days_left(self, today: date) -> int:
        """Return days until the deadline, or zero if already due."""
        return max((self.deadline - today).days, 0)
