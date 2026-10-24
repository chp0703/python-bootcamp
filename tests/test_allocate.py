from datetime import date

import pytest

from shared.contract import Task
from shared.study_planner.allocate import allocate


def test_allocate_does_not_exceed_available_hours():
    tasks = [
        Task("A", 5, 3.0, date(2026, 10, 30)),
        Task("B", 4, 2.0, date(2026, 10, 31)),
    ]

    blocks = allocate(tasks, 4)

    assert [block.hours for block in blocks] == [3.0, 1.0]
    assert sum(block.hours for block in blocks) == 4


def test_allocate_with_no_available_hours_returns_no_blocks():
    task = Task("A", 5, 3.0, date(2026, 10, 30))

    assert allocate([task], 0) == []


def test_allocate_rejects_negative_hours():
    with pytest.raises(ValueError, match="non-negative"):
        allocate([], -1)
