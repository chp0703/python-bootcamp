import importlib.util
from pathlib import Path

import pytest


W1_DIRECTORY = Path(__file__).resolve().parents[2] / "AIVIETNAM-AIO-TheHien" / "w1"


def load_module(module_name: str):
    """Load one of Hien's actual Week 1 modules from its source path."""
    module_path = W1_DIRECTORY / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"hien_w1_{module_name}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


grades = load_module("grades")
rules = load_module("rules")
text_tools = load_module("text_tools")
timetable = load_module("timetable")
translate = load_module("translate")


def test_summary_handles_odd_and_even_scores_without_mutating_input() -> None:
    scores = [9.0, 6.0, 8.0]
    assert grades.summary(scores) == {"min": 6.0, "max": 9.0, "mean": 7.67, "median": 8.0}
    assert scores == [9.0, 6.0, 8.0]
    assert grades.summary([9.0, 6.0, 8.0, 7.0])["median"] == 7.5


def test_summary_rejects_empty_scores() -> None:
    with pytest.raises(ValueError):
        grades.summary([])


def test_thesis_rules_cover_each_missing_requirement() -> None:
    assert rules.can_register_thesis(120, 2.0)
    assert rules.missing(120, 2.0) == []
    assert rules.missing(119, 2.5) == ["need 1 more credits"]
    assert rules.missing(130, 1.9) == ["need GPA at least 2.0"]
    assert rules.missing(100, 1.5) == ["need 20 more credits", "need GPA at least 2.0"]


def test_text_tools_count_punctuation_and_break_ties_alphabetically() -> None:
    text = "Python, python! code: code; test?"
    assert text_tools.word_count(text) == {"python": 2, "code": 2, "test": 1}
    assert text_tools.top_k(text, 2) == [("code", 2), ("python", 2)]
    assert text_tools.top_k(text, 0) == []
    assert text_tools.top_k(text, -1) == []


def test_timetable_groups_sorts_and_keeps_duplicate_courses() -> None:
    pairs = [("CSC2", "Mon"), ("CSC1", "Mon"), ("CSC1", "Mon"), ("MAT1", "Tue")]
    assert timetable.by_day(pairs) == {"Mon": ["CSC1", "CSC1", "CSC2"], "Tue": ["MAT1"]}
    assert timetable.by_day([]) == {}


def test_insertion_sort_returns_and_mutates_the_same_list() -> None:
    values = [3, 1, 2, 1]
    result = translate.insertion_sort(values)
    assert result is values
    assert values == [1, 1, 2, 3]
    assert translate.insertion_sort([1, 2, 3]) == [1, 2, 3]
    assert translate.insertion_sort([]) == []
