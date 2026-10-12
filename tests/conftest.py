"""Shared fixtures for the Python bootcamp tests.

Usage:
    pytest -q python-bootcamp/tests/test_w1.py --member minh_nv --variant 1
"""
import importlib
import sys
from pathlib import Path

import pytest

BOOTCAMP = Path(__file__).resolve().parents[1]
if str(BOOTCAMP) not in sys.path:
    sys.path.insert(0, str(BOOTCAMP))


def pytest_addoption(parser):
    parser.addoption("--member", action="store", default=None, help="your folder under members/, e.g. minh_nv")
    parser.addoption("--variant", action="store", default="1", help="your member number 1-4 (W1-4)")


@pytest.fixture
def member(request):
    m = request.config.getoption("--member")
    if not m:
        pytest.skip("pass --member <your_folder>")
    return m


@pytest.fixture
def variant(request):
    return int(request.config.getoption("--variant"))


@pytest.fixture
def load(member):
    def _load(week: str, module: str):
        return importlib.import_module(f"members.{member}.{week}.{module}")
    return _load
