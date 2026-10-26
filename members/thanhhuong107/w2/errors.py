"""Feasibility checks and their domain-specific error."""

from collections.abc import Iterable

from .models import Task


class InfeasiblePlan(Exception):
    """Raised when the planned work exceeds the available study hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Store the plan totals used to explain the feasibility failure."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(str(self))

    def __str__(self) -> str:
        """Format the required and available hours for the error message."""
        return (
            f"Plan needs {self.needed_h:g} hours, "
            f"but only {self.available_h:g} hours are available."
        )


def check_feasible(tasks: Iterable[Task], available_h: float) -> None:
    """Raise InfeasiblePlan if task effort exceeds available study time."""
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
