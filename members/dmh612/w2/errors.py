"""A custom exception for study plans that exceed available time."""

from .models import Task


class InfeasiblePlan(Exception):
    """Report the required and available number of study hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Keep the required and available hours on the exception."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        """Explain the time shortfall in a readable message."""
        return (
            f"Plan needs {self.needed_h:g} hours, "
            f"but only {self.available_h:g} hours are available."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan when total effort exceeds available hours."""
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
