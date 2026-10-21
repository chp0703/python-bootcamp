from datetime import date

import pytest

from members.chp0703.w2.errors import InfeasiblePlan, check_feasible
from members.chp0703.w2.models import Task


def make_task(effort_h: float) -> Task:
    """Create a valid task with the requested effort."""
    return Task("Study", 3, effort_h, date(2026, 10, 30))


def test_feasible_plan_does_not_raise() -> None:
    check_feasible([make_task(2), make_task(3)], 6)


def test_infeasible_plan_exposes_hours_and_message() -> None:
    with pytest.raises(InfeasiblePlan) as caught:
        check_feasible([make_task(6), make_task(2)], 5)

    error = caught.value
    assert error.needed_h == 8
    assert error.available_h == 5
    assert str(error) == "Plan needs 8 hours, but only 5 hours are available."


def test_exact_budget_is_feasible() -> None:
    check_feasible([make_task(2.5), make_task(1.5)], 4)


def test_empty_plan_is_feasible() -> None:
    check_feasible([], 0)
