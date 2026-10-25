"""Parse due-date expressions used by the Week 3 homework."""

import re
from datetime import date, timedelta

_WEEKDAYS = {
    "mon": 0,
    "monday": 0,
    "tue": 1,
    "tuesday": 1,
    "wed": 2,
    "wednesday": 2,
    "thu": 3,
    "thursday": 3,
    "fri": 4,
    "friday": 4,
    "sat": 5,
    "saturday": 5,
    "sun": 6,
    "sunday": 6,
}


def parse_due(text: str, today: date) -> date:
    """Return an ISO, relative, or next-weekday due date; reject other text."""
    value = text.strip().lower()

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return date.fromisoformat(value)
    if value == "tomorrow":
        return today + timedelta(days=1)

    relative = re.fullmatch(r"in\s+(\d+)\s+days?", value)
    if relative:
        return today + timedelta(days=int(relative.group(1)))

    if value in _WEEKDAYS:
        offset = (_WEEKDAYS[value] - today.weekday()) % 7 or 7
        return today + timedelta(days=offset)

    raise ValueError(f"Unknown due date: {text!r}")
