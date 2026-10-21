from datetime import date

import pytest

from shared.contract import Task
from shared.study_planner.validate import validate_inputs


def test_validate_inputs_accepts_valid_tasks_and_zero_hours():
    tasks = [Task("Review notes", 3, 1.5, date(2026, 10, 30))]

    assert validate_inputs(tasks, 0) is None


@pytest.mark.parametrize("available_h", [-1, float("nan"), float("inf"), True])
def test_validate_inputs_rejects_invalid_available_hours(available_h):
    with pytest.raises(ValueError, match="available_h"):
        validate_inputs([], available_h)


@pytest.mark.parametrize(
    ("task", "message"),
    [
        (Task("   ", 3, 1.0, date(2026, 10, 30)), "title"),
        (Task("Review", 6, 1.0, date(2026, 10, 30)), "importance"),
        (Task("Review", 3, 0, date(2026, 10, 30)), "effort_h"),
        (Task("Review", 3, float("inf"), date(2026, 10, 30)), "effort_h"),
    ],
)
def test_validate_inputs_rejects_invalid_task_fields(task, message):
    with pytest.raises(ValueError, match=message):
        validate_inputs([task], 2.0)


def test_validate_inputs_rejects_non_task_items():
    with pytest.raises(ValueError, match="must be a Task"):
        validate_inputs([object()], 2.0)


def test_validate_inputs_rejects_non_list_tasks():
    with pytest.raises(ValueError, match="list of Task"):
        validate_inputs((), 2.0)
