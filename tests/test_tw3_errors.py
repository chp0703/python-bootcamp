"""Error-path tests for the shared Week 3 study planner."""

from datetime import date
from pathlib import Path
import re

import pytest

from members.thanhhuong107.w2.errors import InfeasiblePlan, check_feasible
from members.thanhhuong107.w2.models import Task
from shared.study_planner.parse import parse_csv


def test_missing_csv_reports_the_missing_path(tmp_path: Path) -> None:
    missing_csv = tmp_path / "missing-tasks.csv"

    with pytest.raises(FileNotFoundError, match=re.escape(missing_csv.name)):
        parse_csv(missing_csv)


def test_empty_csv_reports_the_required_header(tmp_path: Path) -> None:
    empty_csv = tmp_path / "empty-tasks.csv"
    empty_csv.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid CSV header at line 1"):
        parse_csv(empty_csv)


def test_infeasible_plan_reuses_clear_domain_error_message() -> None:
    tasks = [Task("Prepare report", 4, 5.0, date(2026, 10, 30))]

    with pytest.raises(InfeasiblePlan) as caught:
        check_feasible(tasks, available_h=2.0)

    assert caught.value.needed_h == 5.0
    assert caught.value.available_h == 2.0
    assert str(caught.value) == "Plan needs 5 hours, but only 2 hours are available."
