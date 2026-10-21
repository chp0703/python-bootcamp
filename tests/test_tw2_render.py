from datetime import date

from shared.contract import Block, Task
from shared.study_planner.render import render


def make_block(title: str, hours: float) -> Block:
    task = Task(
        title=title,
        importance=3,
        effort_h=hours,
        deadline=date(2026, 10, 30),
    )
    return Block(task=task, hours=hours)


def test_render_empty():
    assert render([]) == "No study blocks allocated."


def test_render_one_block():
    blocks = [make_block("DS exam", 2.0)]

    expected = (
        "STUDY PLAN\n"
        "1. DS exam - 2.0 h\n"
        "\n"
        "Total: 2.0 h"
    )

    assert render(blocks) == expected


def test_render_multiple_blocks():
    blocks = [
        make_block("DS exam", 2.0),
        make_block("Assignment", 1.5),
    ]

    result = render(blocks)

    assert "1. DS exam - 2.0 h" in result
    assert "2. Assignment - 1.5 h" in result
    assert "Total: 3.5 h" in result


def test_render_fractional_hours():
    blocks = [make_block("Calculus", 0.75)]

    result = render(blocks)

    assert "1. Calculus - 0.8 h" in result
    assert "Total: 0.8 h" in result
