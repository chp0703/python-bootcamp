"""Report plans whose full task effort exceeds the available hours."""

from .models import Task


class InfeasiblePlan(Exception):
    """A full plan requires more hours than the user has available."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Preserve both the required and available hour budgets."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        """Describe the hour shortfall in a readable message."""
        return (
            f"Plan needs {self.needed_h:g} hours, "
            f"but only {self.available_h:g} hours are available"
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan unless every task fits in the available budget."""
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
