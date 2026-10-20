"""Input validation for the shared Week 2 study planner."""

import math
from numbers import Real

from shared.contract import Task


def validate_inputs(tasks: list[Task], available_h: float) -> None:
    """Validate tasks and the number of available study hours.

    Raises:
        ValueError: If available hours or any task field is invalid.
    """
    if (
        isinstance(available_h, bool)
        or not isinstance(available_h, Real)
        or not math.isfinite(available_h)
        or available_h < 0
    ):
        raise ValueError("available_h must be a finite, non-negative number")

    if not isinstance(tasks, list):
        raise ValueError("tasks must be a list of Task objects")

    for index, task in enumerate(tasks, start=1):
        if not isinstance(task, Task):
            raise ValueError(f"tasks[{index - 1}] must be a Task")

        if not isinstance(task.title, str) or not task.title.strip():
            raise ValueError(f"Task {index}: title must not be empty or whitespace")

        if (
            isinstance(task.importance, bool)
            or not isinstance(task.importance, int)
            or not 1 <= task.importance <= 5
        ):
            raise ValueError(
                f"Task {index} ({task.title!r}): importance must be an integer from 1 to 5"
            )

        if (
            isinstance(task.effort_h, bool)
            or not isinstance(task.effort_h, Real)
            or not math.isfinite(task.effort_h)
            or task.effort_h <= 0
        ):
            raise ValueError(
                f"Task {index} ({task.title!r}): effort_h must be a finite number greater than 0"
            )
