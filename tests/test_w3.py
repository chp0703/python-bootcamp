import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

BOOTCAMP = Path(__file__).resolve().parents[1]
TODAY = date(2026, 10, 6)   # a Tuesday


def test_w3_1_parse_due(load):
    d = load("w3", "dates")
    assert d.parse_due("2026-10-30", TODAY) == date(2026, 10, 30)
    assert d.parse_due("tomorrow", TODAY) == date(2026, 10, 7)
    assert d.parse_due("in 3 days", TODAY) == date(2026, 10, 9)
    assert d.parse_due("Fri", TODAY) == date(2026, 10, 9)
    assert d.parse_due("Tue", TODAY) == date(2026, 10, 13)   # next occurrence, not today
    with pytest.raises(ValueError):
        d.parse_due("someday", TODAY)


def test_w3_2_log_stats(load):
    ls = load("w3", "log_stats")
    pairs = [("fee", 100), ("fee", 300), ("rag", 900), ("rag", 1100), ("fee", 200)]
    res = ls.analyse(pairs)
    assert res["counts"] == {"fee": 3, "rag": 2}
    assert res["slowest"] == "rag"
    assert res["p95"]["fee"] == 300


def test_w3_3_cli(member):
    ok = subprocess.run([sys.executable, "-m", f"members.{member}.w3.cli", str(BOOTCAMP / "samples" / "tasks.csv"),
                         "--hours", "2", "--today", "2026-10-26"], capture_output=True, text=True, cwd=BOOTCAMP)
    assert ok.returncode == 0 and "Assignment" in ok.stdout
    bad = subprocess.run([sys.executable, "-m", f"members.{member}.w3.cli", "missing.csv", "--hours", "2"],
                         capture_output=True, text=True, cwd=BOOTCAMP)
    assert bad.returncode == 1
