"""Feasibility checks and their domain-specific error."""

from collections.abc import Iterable

from .models import Task


class InfeasiblePlan(Exception):
    """Raised when the tasks need more time than the available study hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Store the hour totals and initialize the exception message."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(str(self))

    def __str__(self) -> str:
        """Describe the plan's required and available hours."""
        return (
            f"Plan needs {self.needed_h:g} hours, "
            f"but only {self.available_h:g} hours are available."
        )


def check_feasible(tasks: Iterable[Task], available_h: float) -> None:
    """Raise InfeasiblePlan when total task effort exceeds available time."""
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
