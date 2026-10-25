from dataclasses import dataclass
from datetime import date

@dataclass
class Task:
    """A study task with an importance, effort estimate, and deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Validate the task importance range."""
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")

    def days_left(self, today: date) -> int:
        """Return remaining days until the deadline, never below zero."""
        return max(0,(self.deadline - today).days)
