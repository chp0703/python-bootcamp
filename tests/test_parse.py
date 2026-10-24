from datetime import date
import pytest
from shared.study_planner.parse import parse_csv


def test_parse_valid_csv(tmp_path):
    path = tmp_path / "tasks.csv"
    path.write_text(
        "title,importance,effort_h,deadline\n"
        "Study Python,5,3.0,2026-10-22\n"
        "Study Math,4,2.5,2026-10-23\n",
        encoding="utf-8",
    )

    tasks = parse_csv(path)

    assert len(tasks) == 2
    assert tasks[0].title == "Study Python"
    assert tasks[0].importance == 5
    assert tasks[0].effort_h == 3.0
    assert tasks[0].deadline == date(2026, 10, 22)


def test_parse_header_only_csv(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text(
        "title,importance,effort_h,deadline\n",
        encoding="utf-8",
    )

    assert parse_csv(path) == []


def test_parse_rejects_invalid_header(tmp_path):
    path = tmp_path / "bad_header.csv"
    path.write_text(
        "name,importance,effort_h,deadline\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 1"):
        parse_csv(path)


def test_parse_reports_invalid_row_number(tmp_path):
    path = tmp_path / "bad_row.csv"
    path.write_text(
        "title,importance,effort_h,deadline\n"
        "Study Python,high,3.0,2026-10-22\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 2"):
        parse_csv(path)


def test_parse_rejects_invalid_date(tmp_path):
    path = tmp_path / "bad_date.csv"
    path.write_text(
        "title,importance,effort_h,deadline\n"
        "Study Python,5,3.0,not-a-date\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 2"):
        parse_csv(path)


def test_parse_rejects_extra_columns(tmp_path):
    path = tmp_path / "extra.csv"
    path.write_text(
        "title,importance,effort_h,deadline\n"
        "Study Python,5,3.0,2026-10-22,unexpected\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 2"):
        parse_csv(path)