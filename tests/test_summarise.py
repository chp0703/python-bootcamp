"""Tests for Hung's assigned shared function."""

from datetime import date

import pytest

from shared.contract import Block, Task
from shared.study_planner.summarise import summarise_plan


def test_empty_plan():
    assert summarise_plan([], 3.0) == {
        "task_count": 0,
        "planned_h": 0.0,
        "available_h": 3.0,
        "remaining_h": 3.0,
    }


def test_counts_blocks_even_for_same_task():
    task = Task("Exam", 5, 6, date(2026, 10, 30))
    blocks = [Block(task, 1.25), Block(task, 0.5)]
    assert summarise_plan(blocks, 3.0) == {
        "task_count": 2,
        "planned_h": 1.75,
        "available_h": 3.0,
        "remaining_h": 1.25,
    }
    assert [block.hours for block in blocks] == [1.25, 0.5]


@pytest.mark.parametrize("available,remaining", [(1.5, 0.0), (1.0, -0.5)])
def test_remaining_is_direct_subtraction(available, remaining):
    task = Task("Exam", 5, 6, date(2026, 10, 30))
    assert summarise_plan([Block(task, 1.5)], available)["remaining_h"] == remaining
