from dataclasses import asdict
from datetime import date, timedelta

import pytest

from shared.contract import Task
from shared.study_planner.prioritise import prioritise

TODAY = date(2026, 10, 26)


def _task(title: str, importance: int, days: int) -> Task:
    return Task(title, importance, 1.0, TODAY + timedelta(days=days))


def test_empty_input_returns_a_new_empty_list():
    tasks = []
    result = prioritise(tasks, TODAY)
    assert result == []
    assert result is not tasks


def test_single_task_keeps_the_original_object():
    task = _task("Only task", 3, 2)
    result = prioritise([task], TODAY)
    assert len(result) == 1
    assert result[0] is task


def test_score_combines_importance_and_deadline_urgency():
    important_later = _task("Important later", 5, 10)
    soon = _task("Soon", 3, 2)
    tomorrow = _task("Tomorrow", 1, 1)
    assert prioritise([important_later, tomorrow, soon], TODAY) == [
        soon,
        tomorrow,
        important_later,
    ]


def test_higher_importance_wins_with_equal_deadlines():
    low = _task("Low", 1, 3)
    high = _task("High", 5, 3)
    assert prioritise([low, high], TODAY) == [high, low]


def test_nearer_deadline_wins_with_equal_importance():
    later = _task("Later", 3, 5)
    sooner = _task("Sooner", 3, 2)
    assert prioritise([later, sooner], TODAY) == [sooner, later]


@pytest.mark.parametrize("days", [-7, 0, 1])
def test_overdue_today_and_tomorrow_use_the_one_day_guard(days):
    urgent = _task("Urgent", 4, days)
    lower_priority = _task("Lower priority", 3, 1)
    assert prioritise([lower_priority, urgent], TODAY) == [urgent, lower_priority]


def test_equal_scores_preserve_input_order():
    first = _task("First", 2, 2)
    second = _task("Second", 1, 1)
    third = _task("Third", 3, 3)
    assert prioritise([first, second, third], TODAY) == [first, second, third]


def test_input_list_and_task_fields_are_not_modified():
    later = _task("Later", 5, 10)
    sooner = _task("Sooner", 3, 1)
    tasks = [later, sooner]
    before = [asdict(task) for task in tasks]
    result = prioritise(tasks, TODAY)
    assert result is not tasks
    assert result == [sooner, later]
    assert tasks[0] is later and tasks[1] is sooner
    assert [asdict(task) for task in tasks] == before


def test_deadline_arithmetic_across_a_year_boundary():
    today = date(2026, 12, 31)
    tomorrow = Task("Tomorrow", 2, 1.0, date(2027, 1, 1))
    later = Task("Later", 5, 1.0, date(2027, 1, 5))
    assert prioritise([later, tomorrow], today) == [tomorrow, later]
