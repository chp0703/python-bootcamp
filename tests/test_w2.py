import json
from datetime import date
from pathlib import Path

import pytest

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_w2_1_task(load):
    m = load("w2", "models")
    t = m.Task("DS exam", 5, 6.0, date(2026, 10, 30))
    assert t.days_left(date(2026, 10, 26)) == 4
    assert t.days_left(date(2026, 11, 2)) == 0
    with pytest.raises(ValueError):
        m.Task("bad", 9, 1.0, date(2026, 10, 30))


def test_w2_2_load_and_save(load, tmp_path):
    io = load("w2", "io_utils")
    tasks = io.load_tasks(SAMPLES / "tasks.csv")
    assert [t.title for t in tasks] == ["DS exam", "Assignment"]
    out = tmp_path / "plan.json"
    io.save_json(tasks, out)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data[0]["title"] == "DS exam" and data[0]["deadline"] == "2026-10-30"
    with pytest.raises(ValueError, match="line 3"):
        io.load_tasks(SAMPLES / "tasks_bad.csv")


def test_w2_3_infeasible(load):
    e = load("w2", "errors")
    m = load("w2", "models")
    tasks = [m.Task("a", 3, 6, date(2026, 10, 30)), m.Task("b", 3, 4, date(2026, 10, 30))]
    with pytest.raises(e.InfeasiblePlan) as exc:
        e.check_feasible(tasks, 2)
    assert exc.value.needed_h == 10 and exc.value.available_h == 2
    assert "10" in str(exc.value)
    e.check_feasible(tasks, 12)   # no exception
